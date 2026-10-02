"""Deterministic retrieval for arm B, from public record fields only.

Order (protocol, change 1): all registrations; all accepted reviews that list the
target field in reviewed_fields; then every other record. Within the second and third
group, records are ranked by the number of context attributes shared with the task,
then by recency. Records are added in that order while they fit the character budget.
Whether a review is binding (roster, validity) is deliberately not decided here.
"""

from __future__ import annotations

import json

from reflectai_v03.contracts import History, Record, Task

from .contracts import PublicFrame


def _event(record: Record) -> dict:
    try:
        return json.loads(record.observation)
    except (TypeError, ValueError):
        return {}


def _shared(record: Record, task: Task, frame: PublicFrame) -> int:
    return sum(record.context.get(name) == task.context.get(name) for name in frame.attributes)


def record_chars(record: Record) -> int:
    # Same serialisation as the prompt payload (json.dumps defaults), plus the list separator.
    return len(json.dumps(record.model_dump(mode='json'), ensure_ascii=False)) + 2


def rank_records(history: History, task: Task, frame: PublicFrame) -> list[Record]:
    target = frame.field_option.field
    registrations, target_reviews, others = [], [], []
    for record in history.records:
        event = _event(record)
        if event.get('event') == 'register_version':
            registrations.append(record)
        elif (event.get('event') == 'review' and event.get('decision') == 'accept'
              and target in event.get('reviewed_fields', [])):
            target_reviews.append(record)
        else:
            others.append(record)

    def key(record):
        return (-_shared(record, task, frame), _negate(record.timestamp), record.record_id)

    return (sorted(registrations, key=lambda r: (r.timestamp, r.record_id))
            + sorted(target_reviews, key=key) + sorted(others, key=key))


def _negate(timestamp: str) -> tuple:
    # Most recent first, as a sortable key without parsing dates.
    return tuple(-ord(ch) for ch in timestamp)


def select_records(history: History, task: Task, frame: PublicFrame, available_chars: int) -> list[Record]:
    """Prefix of the ranking that fits; registrations are never dropped."""
    selected, used = [], 0
    for record in rank_records(history, task, frame):
        size = record_chars(record)
        if used + size > available_chars:
            if _event(record).get('event') == 'register_version':
                raise ValueError('the call budget cannot hold the registrations')
            break
        selected.append(record)
        used += size
    return selected


def coverage(selected: list[Record], binding_record_ids: list[str]) -> dict:
    """Evaluator-side measure: share of binding approvals present in B's context."""
    chosen = {record.record_id for record in selected}
    present = [rid for rid in binding_record_ids if rid in chosen]
    return {'binding_total': len(binding_record_ids), 'binding_included': len(present),
            'records_included': len(selected)}
