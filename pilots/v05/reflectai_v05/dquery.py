"""Deterministic index and query execution for arm D. Public record fields only.

The model never executes anything; it emits RecordQuery objects and this module
filters the public history. Results are ordered by timestamp and truncated to the
character budget; the number of omitted matches is reported to D.
"""

from __future__ import annotations

import json
from collections import Counter

from reflectai_v03.contracts import History, Record

from .contracts import PublicFrame
from .dcontracts import RecordQuery
from .retrieval import record_chars


def _event(record: Record) -> dict:
    try:
        return json.loads(record.observation)
    except (TypeError, ValueError):
        return {}


def build_index(history: History, frame: PublicFrame) -> dict:
    """Counts only: event types and decisions, and per attribute value the number of
    accepted reviews that list the target field. No record contents."""
    target = frame.field_option.field
    by_event, by_value = Counter(), {name: Counter() for name in frame.attributes}
    for record in history.records:
        event = _event(record)
        kind = event.get('event', 'unknown')
        by_event[f"{kind}:{event.get('decision', '-')}"] += 1
        if kind == 'review' and event.get('decision') == 'accept' and target in event.get('reviewed_fields', []):
            for name in frame.attributes:
                if name in record.context:
                    by_value[name][record.context[name]] += 1
    return {'records_total': len(history.records), 'target_field': target,
            'records_by_event_and_decision': dict(sorted(by_event.items())),
            'accepted_target_reviews_by_attribute_value': {
                name: {value: by_value[name].get(value, 0) for value in values}
                for name, values in frame.attributes.items()}}


def matches(record: Record, query: RecordQuery) -> bool:
    event = _event(record)
    if any(record.context.get(pair.attribute) != pair.value for pair in query.attributes):
        return False
    if query.event != 'any' and event.get('event') != query.event:
        return False
    if query.decision != 'any' and event.get('decision') != query.decision:
        return False
    if query.actor and record.actor != query.actor:
        return False
    if query.reviewed_field and query.reviewed_field not in event.get('reviewed_fields', []):
        return False
    return True


def execute(history: History, queries: list[RecordQuery], available_chars: int) -> list[dict]:
    """Run queries in order; the shared character budget is spent first come, first served."""
    results, used = [], 0
    for query in queries:
        found = sorted((r for r in history.records if matches(r, query)), key=lambda r: (r.timestamp, r.record_id))
        shown = []
        for record in found:
            size = record_chars(record)
            if used + size > available_chars:
                break
            shown.append(record.model_dump(mode='json'))
            used += size
        results.append({'query': query.model_dump(mode='json'), 'matches_total': len(found),
                        'records': shown, 'omitted_for_budget': len(found) - len(shown)})
    return results
