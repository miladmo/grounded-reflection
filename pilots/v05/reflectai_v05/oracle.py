"""Compatible requirements from public evidence only.

The approval convention is the v0.4 one, unchanged: a binding approval is an
accepted review by a reviewer listed in the registration, within its validity
interval, with the target field in reviewed_fields. Its accepted fields fix the
configuration of one cell. Further consequences follow from the declared class.
No world, setting, slot plan or seed enters this module.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime

from reflectai_v03.contracts import History

from . import hclass
from .contracts import PublicFrame


def read_frame(history: History) -> PublicFrame:
    return PublicFrame.model_validate_json(history.initial_configuration)


def baseline_values(frame: PublicFrame, facts: dict[str, str]) -> dict[str, str]:
    return {key: value.format_map(facts) for key, value in frame.baseline_template.items()}


def alternative_values(frame: PublicFrame, facts: dict[str, str]) -> dict[str, str]:
    fields = baseline_values(frame, facts)
    option = frame.field_option
    if option.operation == 'omit':
        fields.pop(option.field, None)
    elif option.operation == 'set_literal':
        fields[option.field] = option.value
    elif option.operation == 'set_fact':
        fields[option.field] = facts[option.value]
    else:
        fields[option.field] = fields[option.field] + option.separator + facts[option.value]
    return fields


def configuration_bit(frame: PublicFrame, fields: dict, facts: dict) -> int:
    """0 if the visible fields match the baseline configuration, 1 for the alternative."""
    target = frame.field_option.field
    options = [(target in values, values.get(target))
               for values in (baseline_values(frame, facts), alternative_values(frame, facts))]
    observed = (target in fields, fields.get(target))
    if options[0] == options[1]:
        raise ValueError('declared alternatives do not distinguish this artifact')
    if observed not in options:
        raise ValueError('artifact target field is outside the declared configurations')
    return options.index(observed)


def _time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


@dataclass
class OracleResult:
    frame: PublicFrame
    observations: dict[int, int]
    binding_records: list[str]
    compatible: list
    audit: dict[str, str] = field(default_factory=dict)

    def status(self, cell: int) -> str:
        return hclass.status_at(self.compatible, cell)


def infer(history: History) -> OracleResult:
    frame = read_frame(history)
    events = {}
    for record in history.records:
        try:
            events[record.record_id] = json.loads(record.observation)
        except (TypeError, ValueError) as error:
            raise ValueError(f'non-JSON public event {record.record_id}') from error
    registrations = {}
    for record in history.records:
        event = events[record.record_id]
        if (event.get('event') == 'register_version' and event.get('workflow') == frame.workflow
                and event.get('task_family') == frame.task_family and _time(record.timestamp) <= _time(frame.as_of)):
            if _time(event['valid_from']) >= _time(event['valid_until']):
                raise ValueError('empty version validity interval')
            registrations[record.record_id] = event
    current = [rid for rid, e in registrations.items()
               if e.get('version') == frame.version
               and _time(e['valid_from']) <= _time(frame.as_of) < _time(e['valid_until'])]
    if len(current) != 1:
        raise ValueError('exactly one current registration of the declared version is required')
    observations, binding, audit = {}, [], {}
    for record in history.records:
        event = events[record.record_id]
        kind = event.get('event')
        audit[record.record_id] = 'not_binding'
        if kind == 'register_version':
            audit[record.record_id] = 'registration'
            continue
        if kind != 'review' or event.get('decision') != 'accept':
            continue
        registration = registrations.get(event.get('authority_ref'))
        context = record.context
        if (registration is None or event.get('authority_ref') not in current
                or context.get('workflow') != frame.workflow or context.get('task_family') != frame.task_family
                or context.get('version') != frame.version
                or record.actor not in registration['authorised_reviewers']
                or not (_time(registration['valid_from']) <= _time(record.timestamp) < _time(registration['valid_until']))
                or _time(record.timestamp) > _time(frame.as_of)
                or frame.field_option.field not in event.get('reviewed_fields', [])):
            continue
        fields, facts = event.get('accepted_fields'), event.get('facts')
        if not isinstance(fields, dict) or not isinstance(facts, dict):
            continue
        try:
            cell = frame.cell_of(context)
            value = configuration_bit(frame, fields, facts)
        except (KeyError, ValueError):
            continue
        if observations.get(cell, value) != value:
            raise ValueError('contradictory binding approvals for one cell')
        observations[cell] = value
        binding.append(record.record_id)
        audit[record.record_id] = 'binding'
    klass = hclass.rule_class(len(frame.attributes), frame.candidate_indices())
    compatible = hclass.compatible(klass, observations)
    if not compatible:
        raise ValueError('public evidence admits no requirement in the declared class')
    return OracleResult(frame=frame, observations=observations, binding_records=binding,
                        compatible=compatible, audit=audit)
