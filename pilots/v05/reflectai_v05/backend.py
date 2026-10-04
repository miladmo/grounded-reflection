"""Recorded, non-retrying completions for v0.5 with call, token and failure stops.

Live calls use the bound FHGenie transport from v0.4 unchanged. Failure handling
follows v0.4 Amendment 5: an intact exchange with an unusable answer is an isolated
response failure that stays in its denominator; anything else (usage, model
identity, tools, HTTP, timeout) is systemic and stops further scheduling.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

from reflectai_v03.context import render_rules
from reflectai_v03.contracts import OutputField, Preparation, Rule, Task, WorkOutput
from reflectai_v03.wire import decode_response

from .config import RunConfig
from .dcontracts import AttributeValue, RecordQuery, Register
from .payloads import CONTRACTS, input_chars, schema_for

USAGE_KEYS = ('input_tokens', 'output_tokens', 'cached_input_tokens', 'reasoning_output_tokens')
RESPONSE_ISSUES = frozenset({'response_invalid_json', 'response_finish_invalid', 'response_refusal',
                             'response_role_invalid', 'response_choice_invalid', 'response_content_invalid'})


class Stop(RuntimeError):
    pass


def write_json(path: Path, value) -> None:
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8')


def _usage(raw) -> dict:
    usage = {key: (raw or {}).get(key) for key in USAGE_KEYS}
    if any(v is not None and (type(v) is not int or v < 0) for v in usage.values()):
        raise ValueError('invalid usage')
    return usage


def _isolated(metadata: dict, model: str) -> bool:
    issues = set(metadata.get('audit_issues') or [])
    usage = metadata.get('usage') or {}
    return (bool(issues) and issues <= RESPONSE_ISSUES
            and metadata.get('status') in ('process_failed', 'completed')
            and metadata.get('http_status') == 200 and metadata.get('network_requests') == 1
            and metadata.get('actual_model') == model and not metadata.get('tool_use_detected')
            and all(type(usage.get(k)) is int and usage[k] >= 0 for k in ('input_tokens', 'output_tokens')))


def mock_response(stage: str, prompt: str) -> dict:
    """Exercises serialisation and execution only; no inference and no oracle."""
    payload = json.loads(prompt.split('\nPAYLOAD\n', 1)[1])
    if stage == 'generate':
        task = Task.model_validate(payload['task'])
        rules = [Rule.model_validate(item) for item in payload.get('instructions', [])]
        fields = render_rules(task, rules)
        baseline = {f.name: f.value for f in task.baseline_fields}
        out = WorkOutput(task_id=task.task_id, decision='apply' if fields != baseline else 'keep', applied_rules=rules,
                         fields=[OutputField(name=k, value=v) for k, v in fields.items()], completed=True, questions=[])
        data = out.model_dump(mode='json')
        for rule in data['applied_rules']:
            rule['scope']['match'] = [{'attribute': k, 'values': v} for k, v in rule['scope']['match'].items()]
        return data
    if stage == 'D-index':
        target = json.loads(payload['initial_configuration'])['field_option']['field']
        query = RecordQuery(query_id='q1', event='review', decision='accept', reviewed_field=target,
                            attributes=[], purpose='offline mock')
        return Register(queries=[query], notes='Offline mock.').model_dump(mode='json')
    if stage == 'D-round':
        return Register(no_further_discrimination=True, notes='Offline mock.').model_dump(mode='json')
    return Preparation(notes='Offline mock. No requirement inference.').model_dump(mode='json')


class Backend:
    def __init__(self, config: RunConfig, *, allow_live: bool = False, failures: dict | None = None):
        if config.is_live and not allow_live:
            raise ValueError('live execution requires separate explicit approval')
        if failures and config.is_live:
            raise ValueError('failure injection is offline only')
        self.config, self.failures = config, failures or {}
        self.records: list[dict] = []
        self.halt_reason: str | None = None

    def reported_tokens(self, records=None) -> int:
        return sum((r['usage'][k] or 0) for r in (records or self.records) for k in ('input_tokens', 'output_tokens'))

    def response_failures(self) -> int:
        return sum(r.get('failure_class') == 'response' for r in self.records)

    def summary(self) -> dict:
        return {'attempted_calls': len(self.records), 'reported_tokens': self.reported_tokens(),
                'calls_with_unknown_usage': sum(any(r['usage'][k] is None for k in ('input_tokens', 'output_tokens'))
                                                for r in self.records),
                'failed_calls': sum(r['status'] != 'completed' for r in self.records),
                'response_failures': self.response_failures(), 'halt_reason': self.halt_reason}

    def check(self) -> None:
        if self.halt_reason:
            raise Stop(self.halt_reason)
        if len(self.records) >= self.config.max_calls:
            self.halt_reason = 'call_limit'
        elif self.config.is_live and self.reported_tokens() >= self.config.max_reported_tokens:
            self.halt_reason = 'reported_token_limit'
        if self.halt_reason:
            raise Stop(self.halt_reason)

    def complete(self, stage: str, prompt: str, directory: Path, *, call_id: str, history_id: str, arm: str) -> dict:
        if stage not in CONTRACTS:
            raise ValueError('unknown stage')
        if any(r['call_id'] == call_id for r in self.records):
            raise ValueError('an attempted call cannot be repeated')
        self.check()
        contract, schema = CONTRACTS[stage], schema_for(stage)
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=False)
        record = {'call_id': call_id, 'history_id': history_id, 'arm': arm, 'stage': stage, 'status': 'running',
                  'response': None, 'error': None, 'usage': _usage(None), 'failure_class': None,
                  'input_chars': input_chars(stage, prompt), 'wall_seconds': None,
                  'origin': 'offline_mock' if not self.config.is_live else 'model_generated',
                  'started_at': datetime.now(timezone.utc).isoformat()}
        self.records.append(record)
        write_json(directory / 'request.json', {'stage': stage, 'prompt': prompt,
                                                'prompt_sha256': hashlib.sha256(prompt.encode('utf-8')).hexdigest()})
        raw, metadata = None, {}
        try:
            if not self.config.is_live:
                injected = self.failures.get(call_id)
                if injected == 'failure':
                    raise ValueError('injected offline response failure')
                if injected == 'systemic':
                    self.halt_reason = 'injected_systemic_failure'
                    raise ValueError('injected offline systemic failure')
                raw = mock_response(stage, prompt)
            else:
                from reflectai_v04 import fhgenie_transport
                result = fhgenie_transport.run_completion(
                    prompt, schema, directory / 'transport', self.config.model, self.config.reasoning_effort,
                    self.config.timeout_seconds, max_output_tokens=self.config.max_output_tokens,
                    executable=os.path.expandvars(self.config.pwsh_executable))
                raw, metadata = result['response'], result['metadata']
                if metadata.get('response_model') != self.config.model:
                    self.halt_reason = 'transport_integrity_failure'
                    raise ValueError('response model differs from the registered model')
                record['usage'] = _usage(metadata.get('usage'))
                record['wall_seconds'] = metadata.get('wall_seconds')
                if any(record['usage'][k] is None for k in ('input_tokens', 'output_tokens')):
                    self.halt_reason = 'unknown_token_usage'
                    raise ValueError('unknown usage prevents further live calls')
            record['response'] = contract.model_validate(decode_response(contract, raw)).model_dump(mode='json')
            record['status'] = 'completed'
        except Exception as exc:  # recorded, never retried
            record['status'], record['error'] = 'failed', f'{type(exc).__name__}: {exc}'
            if self.config.is_live:
                if not metadata:
                    try:
                        metadata = json.loads((directory / 'transport' / 'metadata.json').read_text(encoding='utf-8-sig'))
                    except (OSError, ValueError):
                        metadata = {}
                try:
                    record['usage'] = _usage(metadata.get('usage'))
                except ValueError:
                    self.halt_reason = self.halt_reason or 'invalid_token_usage'
                record['wall_seconds'] = metadata.get('wall_seconds')
                if any(record['usage'][k] is None for k in ('input_tokens', 'output_tokens')):
                    self.halt_reason = self.halt_reason or 'unknown_token_usage'
                if not _isolated(metadata, self.config.model) and (
                        metadata.get('audit_issues') or metadata.get('tool_use_detected')
                        or metadata.get('status') in ('launch_failed', 'timed_out', 'process_failed')):
                    self.halt_reason = self.halt_reason or 'systemic_transport_failure'
            record['failure_class'] = 'systemic' if self.halt_reason else 'response'
            if record['failure_class'] == 'response' and self.response_failures() > self.config.max_response_failures:
                self.halt_reason = 'response_failure_limit'
        record['finished_at'] = datetime.now(timezone.utc).isoformat()
        write_json(directory / 'raw.json', raw)
        write_json(directory / 'record.json', record)
        return deepcopy(record)
