"""Bounded recorded inference; mocks never consult evaluator truth.

Attempts, including failures, consume the hard call budget. Reported tokens are
audited after completion: this transport cannot enforce a hard token ceiling.
Unknown usage stays unknown. There are no logical retries or response repairs.
"""

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import time
from typing import Any

from grounded_reflection import codex_backend
from grounded_reflection.models import Contract

from .contracts import BackendConfig, Preparation, ReflectionDraft, Task, WorkOutput
from .wire import decode_response, strict_response_schema

USAGE_FIELDS = ('input_tokens', 'cached_input_tokens', 'output_tokens', 'reasoning_output_tokens')


class BudgetError(RuntimeError):
    """A new call was refused before inference because its budget was exhausted."""


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n',
                    encoding='utf-8')


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _usage(raw: Any) -> dict:
    if raw is None:
        return dict.fromkeys(USAGE_FIELDS)
    if not isinstance(raw, dict):
        raise ValueError('reported usage must be an object or null')
    values = {key: raw.get(key) for key in USAGE_FIELDS}
    for key, value in values.items():
        if value is not None and (type(value) is not int or value < 0):
            raise ValueError(f'{key} must be a nonnegative integer or null')
    for subset, total in (('cached_input_tokens', 'input_tokens'),
                          ('reasoning_output_tokens', 'output_tokens')):
        if values[subset] is not None and values[total] is not None and values[subset] > values[total]:
            raise ValueError(f'{subset} cannot exceed {total}')
    return values


def _mock_response(prompt: str, schema: type[Contract]) -> dict:
    if schema in (Preparation, ReflectionDraft):
        return schema(notes='Offline mock; no inference performed.').model_dump(mode='json')
    if schema is not WorkOutput:
        raise ValueError('offline mock supports Preparation, ReflectionDraft and WorkOutput only')
    marker = '\nPAYLOAD\n'
    if marker not in prompt:
        raise ValueError('generation prompt is missing its PAYLOAD section')
    payload = json.loads(prompt.split(marker, 1)[1])
    task = Task.model_validate(payload['task'])
    return WorkOutput(task_id=task.task_id, decision='keep', applied_rules=[],
                      fields=task.baseline_fields, completed=True, questions=[]).model_dump(mode='json')


class Backend:
    """One in-process ledger, optionally restored from existing record dictionaries."""

    def __init__(self, config: BackendConfig, allow_live: bool = False,
                 prior_records: list[dict] | None = None) -> None:
        self.config = BackendConfig.model_validate(config.model_dump())
        self.allow_live = allow_live is True
        self.records = deepcopy(prior_records or [])
        ids = [record['call_id'] for record in self.records]
        if len(ids) != len(set(ids)):
            raise ValueError('prior records contain duplicate call IDs')
        for record in self.records:
            record['usage'] = _usage(record.get('usage'))
            if record.get('status') not in {'completed', 'failed', 'running'}:
                raise ValueError('invalid prior record status')
        self._check_live_permission()

    def _check_live_permission(self) -> None:
        if self.config.backend == 'codex' and not self.allow_live:
            raise ValueError('live inference requires explicit allow_live=True')
        if self.config.backend == 'codex' and self.config.model.strip() == 'offline-mock':
            raise ValueError('live inference requires an explicit model')

    @property
    def capabilities(self) -> dict:
        return {
            'backend': self.config.backend,
            'strict_tokens': False,
            'provider_enforced_per_call_token_limit': False,
            'budget_control': 'call-budget-controlled and token-audited',
            'compute_matched': False,
            'usage_reporting': 'unavailable' if self.config.backend == 'mock' else 'when_reported',
            'model_sampling_seed_supported': False,
            'automatic_retries': False,
            'transport_reconnects': 'inspect preserved transport logs; not controlled by this ledger',
        }

    def budget_summary(self) -> dict:
        known = sum(record['usage'][key] for record in self.records
                    for key in ('input_tokens', 'output_tokens')
                    if record['usage'][key] is not None)
        unknown = sum(any(record['usage'][key] is None for key in ('input_tokens', 'output_tokens'))
                      for record in self.records)
        return {
            'attempted_calls': len(self.records),
            'failed_calls': sum(record['status'] == 'failed' for record in self.records),
            'unfinished_calls': sum(record['status'] == 'running' for record in self.records),
            'reported_tokens': known,
            'calls_with_unknown_token_usage': unknown,
            'total_tokens': None if unknown else known,
            'max_calls': self.config.max_calls,
            'max_reported_tokens': self.config.max_reported_tokens,
            'strict_tokens': False,
        }

    def complete(self, prompt: str, schema: type[Contract], run_dir: Path, *,
                 call_id: str, arm: str, phase: str, history_id: str, repetition: int) -> dict:
        self._check_live_permission()
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError('prompt must be a nonempty string')
        if not isinstance(schema, type) or not issubclass(schema, Contract):
            raise TypeError('schema must be a Contract class')
        if arm not in {'A', 'B', 'C', 'D'}:
            raise ValueError('arm must be A, B, C or D')
        if any(not isinstance(value, str) or not value.strip() for value in (call_id, phase, history_id)):
            raise ValueError('call_id, phase and history_id must be nonempty strings')
        if type(repetition) is not int or repetition < 0:
            raise ValueError('repetition must be a nonnegative integer')
        if any(record['call_id'] == call_id for record in self.records):
            raise ValueError(f'call ID already recorded: {call_id}')
        budget = self.budget_summary()
        if budget['attempted_calls'] >= self.config.max_calls:
            raise BudgetError('maximum number of attempted calls reached')
        if budget['reported_tokens'] >= self.config.max_reported_tokens:
            raise BudgetError('reported token limit reached; no further calls allowed')
        response_schema = strict_response_schema(schema)
        run_dir = Path(run_dir)
        run_dir.mkdir(parents=True, exist_ok=False)
        started_at, started = _now(), time.perf_counter()
        record = {
            'call_id': call_id, 'arm': arm, 'phase': phase, 'history_id': history_id,
            'repetition': repetition, 'status': 'running', 'response': None, 'error': None,
            'usage': _usage(None),
            'origin': 'offline_mock' if self.config.backend == 'mock' else 'model_generated',
        }
        _write_json(run_dir / 'request.json', {
            'prompt': prompt, 'schema_name': schema.__name__, 'schema_format': 'strict_scope_entries_v1',
            'config': self.config.model_dump(mode='json'),
            'call': {key: record[key] for key in ('call_id', 'arm', 'phase', 'history_id', 'repetition')},
            'capabilities': self.capabilities, 'started_at': started_at,
        })
        _write_json(run_dir / 'response.schema.json', response_schema)
        self.records.append(record)
        # Preserve the attempt before calling transport; interrupted calls cannot disappear on resume.
        _write_json(run_dir / 'record.json', record)
        metadata, raw_response, raw_usage = {}, None, None
        try:
            if self.config.backend == 'mock':
                raw_response = _mock_response(prompt, schema)
            else:
                result = codex_backend.run_completion(
                    prompt, response_schema, run_dir / 'transport', self.config.model,
                    self.config.reasoning_effort, self.config.timeout_seconds,
                )
                raw_response = result['response']
                if not isinstance(result['metadata'], dict):
                    raise ValueError('transport metadata must be an object')
                metadata = result['metadata']
                raw_usage = metadata.get('usage')
                if metadata.get('status') != 'completed':
                    raise ValueError('transport did not report a completed call')
            record['usage'] = _usage(raw_usage)
            decoded = decode_response(schema, raw_response)
            record['response'] = schema.model_validate(decoded).model_dump(mode='json')
            record['status'] = 'completed'
        except Exception as exc:
            record['status'] = 'failed'
            record['error'] = f'{type(exc).__name__}: {exc}'
            metadata_path = run_dir / 'transport' / 'metadata.json'
            if not metadata and metadata_path.is_file():
                try:
                    metadata = json.loads(metadata_path.read_text(encoding='utf-8-sig'))
                    if not isinstance(metadata, dict):
                        raise ValueError('preserved transport metadata must be an object')
                except (OSError, ValueError) as metadata_error:
                    metadata = {}
                    record['error'] += f'; unavailable transport metadata: {metadata_error}'
            raw_usage = metadata.get('usage', raw_usage)
            try:
                record['usage'] = _usage(raw_usage)
            except ValueError as usage_error:
                record['error'] += f'; unavailable valid usage: {usage_error}'
            # The unchanged transport may have preserved invalid/nonconforming JSON before raising.
            raw_path = run_dir / 'transport' / 'final.json'
            if raw_response is None and raw_path.is_file():
                try:
                    raw_response = json.loads(raw_path.read_text(encoding='utf-8-sig'))
                except (OSError, ValueError):
                    pass  # The raw file itself remains preserved under transport/.
        _write_json(run_dir / 'raw.json', raw_response)
        _write_json(run_dir / 'response.json', record['response'])
        _write_json(run_dir / 'usage.json', {
            'reported': record['usage'], 'raw': raw_usage,
            'total_tokens': (record['usage']['input_tokens'] + record['usage']['output_tokens']
                             if all(record['usage'][key] is not None
                                    for key in ('input_tokens', 'output_tokens')) else None),
            'cache_and_reasoning_are_subsets': True,
        })
        _write_json(run_dir / 'metadata.json', {
            'started_at': started_at, 'finished_at': _now(),
            'wall_seconds': round(time.perf_counter() - started, 6),
            'requested_model': self.config.model, 'returned_model': metadata.get('returned_model'),
            'status': record['status'], 'error': record['error'], 'origin': record['origin'],
            'capabilities': self.capabilities, 'transport_metadata': metadata,
            'budget_after_call': self.budget_summary(),
        })
        _write_json(run_dir / 'record.json', record)
        return deepcopy(record)
