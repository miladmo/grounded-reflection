"""Enumerate policies using public artifacts, authority and provenance only.

The model class is deliberately finite. An explicit authorised review fixes one
field option for one context in one version. Further consequences follow from H14.
No latent world, setting, intended regime or generator seed enters this module.
"""

import itertools
import json
from datetime import datetime

from grounded_reflection.models import Scope
from reflectai_v03.contracts import History, Policy, Rule

from .data_contracts import OracleResult, PublicFrame

H14_MASKS = tuple(mask for mask in range(16) if mask not in (6, 9))


def policy_complexity(mask: int) -> int:
    """Number of essential predicates of the Boolean function, not emitted rules."""
    if mask not in H14_MASKS:
        raise ValueError('policy is outside H14')
    if mask in (0, 15):
        return 0
    return 1 if mask in (3, 5, 10, 12) else 2


def read_frame(history: History) -> PublicFrame:
    data = json.loads(history.initial_configuration)
    if not {'hypothesis_class', 'hypothesis_definition'} <= data.keys():
        raise ValueError('the hypothesis class and its full definition must be present in public configuration')
    return PublicFrame.model_validate(data)


def context_cells(frame: PublicFrame) -> list[dict[str, str]]:
    keys = list(frame.dimensions)
    return [dict(zip(keys, values)) for values in itertools.product(
        *(frame.dimensions[key] for key in keys))]


def option_rule(frame: PublicFrame, context: dict[str, str]) -> Rule:
    return Rule(**frame.field_option.model_dump(),
                scope=Scope(match={key: [value] for key, value in context.items()}))


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


def policy_from_masks(frame: PublicFrame, masks: dict[str, int], policy_id: str) -> Policy:
    rules = []
    for version, mask in masks.items():
        if mask not in H14_MASKS:
            raise ValueError('world or hypothesis outside the public H14 class')
        for index, cell in enumerate(context_cells(frame)):
            if mask & (1 << index):
                scope = {'task_family': frame.task_family, 'workflow': frame.workflow,
                         'version': version, **cell}
                rules.append(option_rule(frame, scope))
    return Policy(policy_id=policy_id, rules=rules)


def approved_fields(event: dict) -> dict | None:
    if event.get('format') == 'raw':
        return event.get('artifacts', {}).get(event.get('accepted_artifact'), {}).get('fields')
    if event.get('format') == 'interpreted':
        return event.get('accepted_fields')
    return None


def field_option_index(frame: PublicFrame, fields: dict, facts: dict) -> int:
    """Recover the binary configuration from actual visible field values."""
    field = frame.field_option.field
    baseline, alternative = baseline_values(frame, facts), alternative_values(frame, facts)
    observed = (field in fields, fields.get(field))
    options = [(field in values, values.get(field)) for values in (baseline, alternative)]
    if options[0] == options[1]:
        raise ValueError('registered alternatives do not distinguish this artifact')
    if observed not in options:
        raise ValueError('artifact target field is outside the declared configurations')
    return options.index(observed)


def policy_option_at(policy: Policy, context: dict[str, str]) -> int:
    return int(any(rule.scope.applies_to(context) == 'match' for rule in policy.rules))


def _time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def _within(timestamp: str, registration: dict) -> bool:
    return (_time(registration['valid_from']) <= _time(timestamp)
            < _time(registration['valid_until']))


def infer_policies(history: History) -> OracleResult:
    frame = read_frame(history)
    records = {record.record_id: record for record in history.records}
    events = {}
    for record in history.records:
        try:
            events[record.record_id] = json.loads(record.observation)
        except (ValueError, TypeError) as error:
            raise ValueError(f'non-JSON public event {record.record_id}') from error
    versions, registry = {}, {}
    for record in history.records:
        event = events[record.record_id]
        if event.get('event') != 'register_version':
            continue
        if _time(record.timestamp) > _time(frame.as_of):
            continue
        if event.get('workflow') != frame.workflow or event.get('task_family') != frame.task_family:
            continue
        required = ('version', 'valid_from', 'valid_until', 'authorised_reviewers')
        if any(key not in event for key in required):
            continue
        if _time(event['valid_from']) >= _time(event['valid_until']):
            raise ValueError('empty version validity interval')
        version = event['version']
        if version in versions:
            raise ValueError('duplicate version registration')
        versions[version] = {**event, 'registry_id': record.record_id}
        registry[record.record_id] = versions[version]
    current = [version for version, registration in versions.items()
               if _within(frame.as_of, registration)]
    if len(current) != 1:
        raise ValueError('exactly one publicly registered current version is required')
    current_version = current[0]
    cells = context_cells(frame)
    constraints, audit, fixed = [], {}, {version: {} for version in versions}

    def origin(record_id):
        visited = set()
        while record_id in records and record_id not in visited:
            visited.add(record_id)
            if events[record_id].get('event') != 'forward':
                return record_id
            record_id = events[record_id].get('origin_ref')
        return None

    for record in history.records:
        event = events[record.record_id]
        kind = {'register_version': 'version_event', 'forward': 'copy',
                'review': 'authoritative_review', 'comment': 'comment',
                'execution': 'technical'}.get(event.get('event'), 'comment')
        root = origin(record.record_id)
        item = {'root_id': root, 'validity': 'unknown', 'kind': kind,
                'scope_context': dict(record.context), 'constraint_applied': False,
                'usable_current_support': False}
        audit[record.record_id] = item
        if _time(record.timestamp) > _time(frame.as_of):
            continue
        if event.get('event') == 'register_version':
            item['validity'] = ('active' if event.get('version') == current_version
                                else 'superseded') if record.record_id in registry else 'unknown'
            continue
        if event.get('event') != 'review':
            continue
        context = record.context
        if context.get('workflow') != frame.workflow or context.get('task_family') != frame.task_family:
            item['validity'] = 'out_of_scope'
            continue
        registration = registry.get(event.get('authority_ref'))
        version = context.get('version')
        if (registration is None or registration.get('version') != version
                or record.actor not in registration['authorised_reviewers']
                or not _within(record.timestamp, registration)
                or _time(records[registration['registry_id']].timestamp) > _time(record.timestamp)):
            continue
        if any(context.get(key) not in values for key, values in frame.dimensions.items()):
            continue
        item['validity'] = 'active' if version == current_version else 'superseded'
        if event.get('decision') != 'accept' or frame.field_option.field not in event.get('reviewed_fields', []):
            continue
        selected = approved_fields(event)
        if not isinstance(selected, dict) or not isinstance(event.get('facts'), dict):
            continue
        facts = event['facts']
        try:
            bit = field_option_index(frame, selected, facts)
        except KeyError:
            continue
        index = cells.index({key: context[key] for key in frame.dimensions})
        if index in fixed[version] and fixed[version][index] != bit:
            raise ValueError(f'contradictory authorised reviews in version {version}')
        fixed[version][index] = bit
        item['constraint_applied'] = True
        item['usable_current_support'] = version == current_version
        constraints.append({'record_id': record.record_id, 'root_id': record.record_id,
                            'version': version, 'scope_context': dict(context),
                            'option_index': bit})

    # Resolve forwards after originals. Their provenance is visible but no extra constraint is added.
    for record_id, item in audit.items():
        if (item['kind'] == 'copy' and item['root_id'] in audit
                and _time(records[record_id].timestamp) <= _time(frame.as_of)
                and _time(records[item['root_id']].timestamp) <= _time(records[record_id].timestamp)):
            source = audit[item['root_id']]
            item['validity'] = source['validity']
            item['scope_context'] = source['scope_context']
            item['usable_current_support'] = source['usable_current_support']
    possible = {version: [mask for mask in H14_MASKS
                         if all(bool(mask & (1 << index)) == bool(bit)
                                for index, bit in facts.items())]
                for version, facts in fixed.items()}
    ordered_versions = sorted(possible)
    policies = [policy_from_masks(frame, dict(zip(ordered_versions, masks)), f'policy-{index:03d}')
                for index, masks in enumerate(itertools.product(
                    *(possible[version] for version in ordered_versions)))]
    if not policies:
        raise ValueError('public evidence admits no policy')
    return OracleResult(policies=policies, evidence_audit=audit, constraints=constraints,
                        versions=versions, current_version=current_version)
