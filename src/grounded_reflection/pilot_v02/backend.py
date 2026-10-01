"""Recorded offline completions and explicitly enabled Codex inference.

The ledger limits attempts, including failed calls. Reported token totals are
audited after each call; the Codex transport cannot enforce a hard token cap.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import time
from typing import Any

from .. import codex_backend
from ..models import Contract
from .contracts import BackendConfig, CallRecord, Preparation, Usage, WorkOutput
from .wire import decode_response, strict_response_schema


class BudgetError(RuntimeError):
    """A call was refused before inference because its budget was exhausted."""


def _write_json(path: Path, value: Any) -> None:
    with path.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n')


def _usage(raw: Any) -> Usage:
    if raw is None:
        return Usage()
    if not isinstance(raw, dict):
        raise ValueError('reported usage must be an object or null')
    values = {}
    for key in Usage.model_fields:
        value = raw.get(key)
        if value is not None and (type(value) is not int or value < 0):
            raise ValueError(f'{key} must be a nonnegative integer or null')
        values[key] = value
    usage = Usage(**values)
    for subset, total in (
        ('cached_input_tokens', 'input_tokens'),
        ('reasoning_output_tokens', 'output_tokens'),
    ):
        part, whole = getattr(usage, subset), getattr(usage, total)
        if part is not None and whole is not None and part > whole:
            raise ValueError(f'{subset} cannot exceed {total}')
    return usage


def _mock_response(prompt: str, schema: type[Contract]) -> dict:
    if schema is Preparation:
        return {'requirements': [], 'notes': 'Offline mock. No requirement inference performed.'}
    if schema is not WorkOutput:
        raise ValueError('offline mock supports Preparation and WorkOutput only')
    marker = '\nPAYLOAD\n'
    if marker not in prompt:
        raise ValueError('generation prompt is missing its PAYLOAD section')
    payload = json.loads(prompt.split(marker, 1)[1])
    task = payload['task']
    return {
        'case_id': task['case_id'],
        'action': 'deliver',
        'missing_fields': [],
        'fields': [
            {'name': name, 'value': task['facts'].get(name, '')}
            for name in task['output_fields']
        ],
    }


class Backend:
    """One ledger shared across phases; restore it using prior call records."""

    def __init__(
        self,
        config: BackendConfig,
        allow_live: bool = False,
        prior_records: list[CallRecord] | None = None,
    ) -> None:
        self.config = BackendConfig.model_validate(config.model_dump())
        self.allow_live = allow_live is True
        self.records = [CallRecord.model_validate(r.model_dump()) for r in prior_records or []]
        if len({r.call_id for r in self.records}) != len(self.records):
            raise ValueError('prior records contain duplicate call IDs')
        for record in self.records:
            _usage(record.usage.model_dump())
        self._check_live_permission()

    def _check_live_permission(self) -> None:
        if self.config.backend == 'codex' and not self.allow_live:
            raise ValueError('live inference requires explicit allow_live=True')
        if self.config.backend == 'codex' and (
            not self.config.model.strip() or self.config.model == 'offline-mock'
        ):
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
        }

    def budget_summary(self) -> dict:
        known = sum(
            value
            for record in self.records
            for value in (record.usage.input_tokens, record.usage.output_tokens)
            if value is not None
        )
        unknown = sum(
            r.usage.input_tokens is None or r.usage.output_tokens is None
            for r in self.records
        )
        return {
            'attempted_calls': len(self.records),
            'failed_calls': sum(r.status == 'failed' for r in self.records),
            'reported_tokens': known,
            'calls_with_unknown_token_usage': unknown,
            'total_tokens': None if unknown else known,
            'max_calls': self.config.max_calls,
            'max_reported_tokens': self.config.max_reported_tokens,
            'strict_tokens': False,
        }

    def complete(
        self,
        prompt: str,
        schema: type[Contract],
        run_dir: Path,
        *,
        call_id: str,
        arm: str,
        phase: str,
        family: str,
        repetition: int,
    ) -> CallRecord:
        self._check_live_permission()
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError('prompt must be a nonempty string')
        if not isinstance(schema, type) or not issubclass(schema, Contract):
            raise TypeError('schema must be a Contract class')
        if any(record.call_id == call_id for record in self.records):
            raise ValueError(f'call ID already recorded: {call_id}')
        budget = self.budget_summary()
        if budget['attempted_calls'] >= self.config.max_calls:
            raise BudgetError('maximum number of attempted calls reached')
        if budget['reported_tokens'] >= self.config.max_reported_tokens:
            raise BudgetError('reported token limit reached; no further calls allowed')
        record = CallRecord(
            call_id=call_id, arm=arm, phase=phase, family=family,
            repetition=repetition, status='failed',
            origin='offline_mock' if self.config.backend == 'mock' else 'model_generated',
        )
        run_dir = Path(run_dir)
        run_dir.mkdir(parents=True, exist_ok=False)
        started_at = datetime.now(timezone.utc).isoformat()
        started = time.perf_counter()
        response_schema = (strict_response_schema(schema) if self.config.backend == 'codex'
                           else schema.model_json_schema())
        _write_json(run_dir / 'request.json', {
            'prompt': prompt,
            'schema_name': schema.__name__,
            'schema_format': ('strict_scope_entries_v1' if self.config.backend == 'codex'
                              else 'canonical'),
            'config': self.config.model_dump(),
            'call': record.model_dump(exclude={'response', 'error', 'usage', 'status'}),
            'capabilities': self.capabilities,
            'started_at': started_at,
        })
        _write_json(run_dir / 'response.schema.json', response_schema)
        # Reserve the attempt before the transport, including any failure.
        self.records.append(record)
        metadata: dict = {}
        raw_response = None
        raw_usage = None
        try:
            if self.config.backend == 'mock':
                raw_response = _mock_response(prompt, schema)
            else:
                result = codex_backend.run_completion(
                    prompt, response_schema, run_dir / 'transport',
                    self.config.model, self.config.reasoning_effort,
                    self.config.timeout_seconds,
                )
                raw_response = result['response']
                if not isinstance(result['metadata'], dict):
                    raise ValueError('transport metadata must be an object')
                metadata = result['metadata']
                raw_usage = metadata.get('usage')
            record.usage = _usage(raw_usage)
            decoded = (decode_response(schema, raw_response) if self.config.backend == 'codex'
                       else raw_response)
            record.response = schema.model_validate(decoded).model_dump(mode='json')
            record.status = 'completed'
        except Exception as exc:
            record.error = f'{type(exc).__name__}: {exc}'
            # The unchanged Codex wrapper writes metadata even when it raises.
            metadata_path = run_dir / 'transport' / 'metadata.json'
            if not metadata and metadata_path.is_file():
                try:
                    recovered = json.loads(metadata_path.read_text(encoding='utf-8-sig'))
                    if not isinstance(recovered, dict):
                        raise ValueError('preserved transport metadata must be an object')
                    metadata = recovered
                    raw_usage = metadata.get('usage')
                    record.usage = _usage(raw_usage)
                except (OSError, ValueError, AttributeError) as usage_error:
                    record.error += f'; unavailable valid usage: {usage_error}'
        if raw_response is not None:
            _write_json(run_dir / 'response.json', raw_response)
        _write_json(run_dir / 'usage.json', {
            'reported': record.usage.model_dump(),
            'raw': raw_usage,
            'total_tokens': (
                record.usage.input_tokens + record.usage.output_tokens
                if record.usage.input_tokens is not None and record.usage.output_tokens is not None
                else None
            ),
            'cache_and_reasoning_are_subsets': True,
        })
        _write_json(run_dir / 'metadata.json', {
            'started_at': started_at,
            'finished_at': datetime.now(timezone.utc).isoformat(),
            'wall_seconds': round(time.perf_counter() - started, 6),
            'requested_model': self.config.model,
            'returned_model': metadata.get('returned_model'),
            'origin': record.origin,
            'capabilities': self.capabilities,
            'transport_metadata': metadata,
            'budget_after_call': self.budget_summary(),
        })
        _write_json(run_dir / 'record.json', record.model_dump(mode='json'))
        return record
