"""Recorded, non-retrying completions with offline defaults and global stops."""

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from . import transport as codex_backend
from reflectai_v03.context import render_rules
from reflectai_v03.contracts import OutputField, Preparation, Rule, Task, WorkOutput
from reflectai_v03.wire import decode_response, strict_response_schema

from .config import RunConfig

USAGE_KEYS = ('input_tokens', 'output_tokens', 'cached_input_tokens', 'reasoning_output_tokens')
# Amendment 5: an intact exchange whose answer is unusable is an isolated response
# failure. Anything else (usage, model identity, tools, HTTP, timeout) stays systemic.
RESPONSE_ISSUES = frozenset({'response_invalid_json', 'response_finish_invalid', 'response_refusal',
                             'response_role_invalid', 'response_choice_invalid',
                             'response_content_invalid'})


def file_sha256(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_executable(config: RunConfig) -> None:
    """Fail before any reservation or key access if the pinned PowerShell 7 changed."""
    if config.backend != 'fhgenie':
        return
    path = Path(config.pwsh_executable)
    if not path.is_file() or file_sha256(path) != config.pwsh_sha256:
        raise ValueError('The pinned PowerShell 7 executable is missing or differs from its SHA-256.')


def _isolated_response_failure(metadata: dict, model: str) -> bool:
    issues = set(metadata.get('audit_issues') or [])
    usage = metadata.get('usage') or {}
    return (bool(issues) and issues <= RESPONSE_ISSUES
            and metadata.get('status') in ('process_failed', 'completed')
            and metadata.get('http_status') == 200 and metadata.get('network_requests') == 1
            and metadata.get('actual_model') == model and not metadata.get('tool_use_detected')
            and all(type(usage.get(key)) is int and usage[key] >= 0
                    for key in ('input_tokens', 'output_tokens')))


class BudgetStop(RuntimeError):
    pass


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n',
                    encoding='utf-8')


def normalise_usage(raw) -> dict:
    if raw is None:
        return dict.fromkeys(USAGE_KEYS)
    if not isinstance(raw, dict):
        raise ValueError('Usage must be an object or null.')
    usage = {key: raw.get(key) for key in USAGE_KEYS}
    if any(value is not None and (type(value) is not int or value < 0)
           for value in usage.values()):
        raise ValueError('Token counts must be nonnegative integers or unknown.')
    for subset, total in (('cached_input_tokens', 'input_tokens'),
                          ('reasoning_output_tokens', 'output_tokens')):
        if usage[subset] is not None and usage[total] is not None and usage[subset] > usage[total]:
            raise ValueError('Token subset exceeds its total.')
    return usage


def _wire(value):
    if isinstance(value, list):
        return [_wire(item) for item in value]
    if isinstance(value, dict):
        if set(value) == {'match'} and isinstance(value['match'], dict):
            return {'match': [{'attribute': k, 'values': v} for k, v in value['match'].items()]}
        return {key: _wire(item) for key, item in value.items()}
    return value


def mock_response(prompt: str, schema) -> dict:
    """Exercise serialization and execution, without an oracle or inference."""
    if schema is Preparation:
        return Preparation(notes='Offline mock. No requirement inference.').model_dump(mode='json')
    if schema is not WorkOutput:
        raise ValueError('Unsupported response contract.')
    payload = json.loads(prompt.split('\nPAYLOAD\n', 1)[1])
    task = Task.model_validate(payload['task'])
    rules = [Rule.model_validate(item) for item in payload.get('instructions', [])]
    fields = render_rules(task, rules)
    baseline = {item.name: item.value for item in task.baseline_fields}
    output = WorkOutput(task_id=task.task_id, decision='apply' if fields != baseline else 'keep',
                        applied_rules=rules, fields=[OutputField(name=k, value=v) for k, v in fields.items()],
                        completed=True, questions=[])
    return _wire(output.model_dump(mode='json'))


class Backend:
    def __init__(self, config: RunConfig, *, allow_live: bool = False,
                 failures: dict[str, str] | None = None):
        self.config = config.model_copy(deep=True)
        if config.is_live and not allow_live:
            raise ValueError('Live execution requires separate explicit approval.')
        if failures and config.backend != 'mock':
            raise ValueError('Failure injection is offline only.')
        self.failures = failures or {}
        self.records: list[dict] = []
        self.halt_reason: str | None = None

    def budget_summary(self) -> dict:
        known = sum((record['usage'][k] or 0) for record in self.records
                    for k in ('input_tokens', 'output_tokens'))
        unknown = sum(any(record['usage'][k] is None for k in ('input_tokens', 'output_tokens'))
                      for record in self.records)
        return {'attempted_calls': len(self.records), 'reported_tokens': known,
                'calls_with_unknown_usage': unknown, 'total_tokens': None if unknown else known,
                'failed_calls': sum(r['status'] != 'completed' for r in self.records),
                'response_failures': self.response_failures(),
                'max_response_failures': self.config.max_response_failures,
                'halt_reason': self.halt_reason, 'strict_token_cap': False}

    def response_failures(self) -> int:
        return sum(record.get('failure_class') == 'response' for record in self.records)

    def register_reference_failure(self, call_id: str) -> None:
        """Count a completed C2 whose evidence references cannot become instructions."""
        record = next(r for r in self.records if r['call_id'] == call_id)
        if record['status'] != 'completed' or record.get('failure_class'):
            raise ValueError('Only a completed, unclassified call can be marked.')
        record['failure_class'] = 'response'
        record['reference_invalid'] = True
        if self.halt_reason is None and self.response_failures() > self.config.max_response_failures:
            self.halt_reason = 'response_failure_limit'

    def check_budget(self) -> None:
        if self.halt_reason:
            raise BudgetStop(self.halt_reason)
        summary = self.budget_summary()
        if len(self.records) >= self.config.max_calls:
            self.halt_reason = 'call_limit'
        elif summary['reported_tokens'] >= self.config.max_reported_tokens:
            self.halt_reason = 'reported_token_limit'
        if self.halt_reason:
            raise BudgetStop(self.halt_reason)

    def complete(self, prompt: str, schema, directory: Path, *, call_id: str,
                 history_id: str, arm: str, phase: str, probe: str | None = None) -> dict:
        if arm not in ('A', 'B', 'C') or phase not in ('C1', 'C2', 'generate'):
            raise ValueError('Only the registered A/B/C stages are available.')
        if phase != 'generate' and (arm != 'C' or schema is not Preparation):
            raise ValueError('Preparation is available only for C.')
        if phase == 'generate' and schema is not WorkOutput:
            raise ValueError('Generation requires WorkOutput.')
        if not call_id or Path(call_id).name != call_id or call_id in ('.', '..'):
            raise ValueError('Call IDs must be safe nonempty filenames.')
        if any(record['call_id'] == call_id for record in self.records):
            raise ValueError('An attempted call cannot be repeated.')
        self.check_budget()
        response_schema = strict_response_schema(schema)
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=False)
        record = {'call_id': call_id, 'history_id': history_id, 'arm': arm,
                  'phase': phase, 'probe': probe, 'status': 'running', 'response': None,
                  'error': None, 'usage': normalise_usage(None), 'fatal': False,
                  'origin': 'offline_mock' if self.config.backend == 'mock' else 'model_generated',
                  'started_at': datetime.now(timezone.utc).isoformat()}
        self.records.append(record)
        write_json(directory / 'request.json', {'prompt': prompt, 'config': self.config.model_dump(),
                                              'schema': response_schema})
        write_json(directory / 'record.json', record)
        raw, metadata = None, {}
        try:
            if self.config.backend == 'mock':
                injected = self.failures.get(call_id)
                if injected == 'failure':
                    raise ValueError('Injected offline response failure.')
                if injected == 'integrity':
                    self.halt_reason = 'injected_integrity_failure'
                    raise ValueError('Injected offline integrity stop.')
                raw = mock_response(prompt, schema)
            else:
                if self.config.backend == 'fhgenie':
                    from . import fhgenie_transport
                    result = fhgenie_transport.run_completion(
                        prompt, response_schema, directory / 'transport', self.config.model,
                        self.config.reasoning_effort, self.config.timeout_seconds,
                        max_output_tokens=self.config.max_output_tokens,
                        executable=self.config.pwsh_executable)
                else:
                    result = codex_backend.run_completion(
                        prompt, response_schema, directory / 'transport', self.config.model,
                        self.config.reasoning_effort, self.config.timeout_seconds)
                raw, metadata = result['response'], result['metadata']
                if metadata.get('status') != 'completed' or metadata.get('audit_issues'):
                    self.halt_reason = 'transport_integrity_failure'
                    raise ValueError('Transport did not pass the tool-free completion audit.')
                if (self.config.backend == 'fhgenie'
                        and metadata.get('response_model') != self.config.model):
                    self.halt_reason = 'transport_integrity_failure'
                    raise ValueError('FHGenie response model differs from the registered model.')
                record['usage'] = normalise_usage(metadata.get('usage'))
                if any(record['usage'][k] is None for k in ('input_tokens', 'output_tokens')):
                    self.halt_reason = 'unknown_token_usage'
                    raise ValueError('Unknown usage prevents further live calls.')
            record['response'] = schema.model_validate(decode_response(schema, raw)).model_dump(mode='json')
            record['status'] = 'completed'
        except Exception as exc:
            record['status'] = 'failed'
            record['error'] = f'{type(exc).__name__}: {exc}'
            preserved = directory / 'transport' / 'metadata.json'
            if not metadata and preserved.is_file():
                try:
                    metadata = json.loads(preserved.read_text(encoding='utf-8-sig'))
                except (ValueError, OSError):
                    metadata = {}
            if self.config.is_live:
                try:
                    record['usage'] = normalise_usage(metadata.get('usage'))
                except ValueError:
                    self.halt_reason = 'invalid_token_usage'
                if any(record['usage'][k] is None for k in ('input_tokens', 'output_tokens')):
                    self.halt_reason = self.halt_reason or 'unknown_token_usage'
                isolated = (self.config.backend == 'fhgenie'
                            and _isolated_response_failure(metadata, self.config.model))
                if not isolated:
                    if metadata.get('tool_use_detected') or metadata.get('audit_issues'):
                        self.halt_reason = 'transport_integrity_failure'
                    if metadata.get('status') in ('launch_failed', 'timed_out', 'process_failed'):
                        self.halt_reason = self.halt_reason or 'systemic_transport_failure'
                raw_path = directory / 'transport' / 'final.json'
                if raw is None and raw_path.is_file():
                    try:
                        raw = json.loads(raw_path.read_text(encoding='utf-8-sig'))
                    except (ValueError, OSError):
                        pass
            # A failure that set no halt is an isolated response failure; it stays in
            # its denominator. The 20th such failure stops further scheduling.
            record['failure_class'] = 'systemic' if self.halt_reason else 'response'
            if (record['failure_class'] == 'response'
                    and self.response_failures() > self.config.max_response_failures):
                self.halt_reason = 'response_failure_limit'
        record['fatal'] = self.halt_reason is not None
        record['finished_at'] = datetime.now(timezone.utc).isoformat()
        write_json(directory / 'raw.json', raw)
        write_json(directory / 'transport-metadata.json', metadata)
        write_json(directory / 'record.json', record)
        return deepcopy(record)
