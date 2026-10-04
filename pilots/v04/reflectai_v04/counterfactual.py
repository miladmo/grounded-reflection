"""Single-record approval promotions, derived from public records only."""

import json
from collections import Counter

from reflectai_v03.contracts import History

from .oracle import approved_fields, field_option_index, infer_policies, policy_option_at, read_frame

MANIPULATED_TYPES = (
    'forward', 'old_approval', 'unauthorised_revision', 'rejected_opposite_artifact',
    'target_field_preference', 'approval_without_target',
)
OUTCOMES = ('action_flip', 'contradiction', 'unchanged_constraints',
            'narrower_same_actions', 'retention_resolved', 'unassessable')


def action_summary(policies, context):
    if not policies:
        return {'action': None, 'basis': 'contradiction'}
    values = {policy_option_at(policy, context) for policy in policies}
    if values == {1}:
        return {'action': 'apply', 'basis': 'resolved_change'}
    return {'action': 'keep', 'basis': 'resolved_keep' if values == {0} else 'unresolved'}


def assess_assignment(result, context, option_index, diagnostic_context, control_context):
    """Filter the public compatible set without replacing genuine observations."""
    if option_index not in (0, 1):
        raise ValueError('a promotion must specify a recovered binary field configuration')
    remaining = [policy for policy in result.policies
                 if policy_option_at(policy, context) == option_index]
    base = {name: action_summary(result.policies, scope) for name, scope in
            [('diagnostic', diagnostic_context), ('control', control_context)]}
    changed = {name: action_summary(remaining, scope) for name, scope in
               [('diagnostic', diagnostic_context), ('control', control_context)]}
    if not remaining:
        outcome = 'contradiction'
    elif any(changed[name]['action'] != base[name]['action'] for name in base):
        outcome = 'action_flip'
    elif any(base[name]['basis'] == 'unresolved' and changed[name]['basis'] == 'resolved_keep' for name in base):
        outcome = 'retention_resolved'
    elif len(remaining) == len(result.policies):
        outcome = 'unchanged_constraints'
    else:
        outcome = 'narrower_same_actions'
    return {'remaining_policy_count': len(remaining), 'outcome': outcome,
            'diagnostic_action': changed['diagnostic']['action'],
            'control_action': changed['control']['action'],
            'diagnostic_basis': changed['diagnostic']['basis'],
            'control_basis': changed['control']['basis']}


def _type(record, body, result, field):
    if body.get('event') == 'forward':
        return 'forward'
    audit = result.evidence_audit[record.record_id]
    if audit['constraint_applied'] and audit['validity'] == 'superseded':
        return 'old_approval'
    if body.get('event') == 'preference':
        return 'target_field_preference'
    if body.get('event') != 'review':
        return None
    if body.get('decision') == 'reject':
        return 'rejected_opposite_artifact'
    if body.get('decision') == 'accept' and field not in body.get('reviewed_fields', []):
        return 'approval_without_target'
    registration = result.versions.get(record.context.get('version'), {})
    if body.get('decision') == 'accept' and record.actor not in registration.get('authorised_reviewers', []):
        return 'unauthorised_revision'
    return None


def _visible_fields(body):
    if body.get('event') == 'preference':
        return body.get('proposed_fields')
    if body.get('decision') == 'reject':
        if body.get('format') == 'raw':
            return body.get('artifacts', {}).get(body.get('rejected_artifact'), {}).get('fields')
        return body.get('rejected_fields')
    return approved_fields(body)


def audit_counterfactuals(history: History, diagnostic_context: dict, control_context: dict,
                         required_outcome: str | None = None) -> dict:
    """No world, intended label, latent event stream or future instance is accepted."""
    if required_outcome not in (None, 'action_flip', 'contradiction'):
        raise ValueError('unknown qualification outcome')
    frame, result = read_frame(history), infer_policies(history)
    records = {record.record_id: record for record in history.records}
    bodies = {record_id: json.loads(record.observation) for record_id, record in records.items()}
    audited = []
    for record_id, record in records.items():
        body = bodies[record_id]
        record_type = _type(record, body, result, frame.field_option.field)
        if record_type is None:
            continue
        source_id = result.evidence_audit[record_id]['root_id'] if record_type == 'forward' else record_id
        context = {**record.context, 'version': result.current_version}
        item = {'record_id': record_id, 'record_type': record_type, 'origin_record_id': source_id,
                'context': context, 'option_index': None, 'selected_field': frame.field_option.field,
                'selected_field_present': None, 'selected_field_value': None,
                'promotion': 'Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations.',
                'remaining_policy_count': None, 'outcome': 'unassessable',
                'diagnostic_action': None, 'control_action': None}
        try:
            if (source_id not in bodies or context.get('task_family') != frame.task_family
                    or context.get('workflow') != frame.workflow
                    or any(context.get(key) not in values for key, values in frame.dimensions.items())):
                raise ValueError('unresolved source or context outside the declared model')
            source = bodies[source_id]
            fields = _visible_fields(source)
            if not isinstance(fields, dict) or not isinstance(source.get('facts'), dict):
                raise ValueError('source does not expose an artifact configuration and its facts')
            bit = field_option_index(frame, fields, source['facts'])
            item.update({'option_index': bit, 'selected_field_present': frame.field_option.field in fields,
                         'selected_field_value': fields.get(frame.field_option.field)})
            item.update(assess_assignment(result, context, bit, diagnostic_context, control_context))
        except (KeyError, TypeError, ValueError) as error:
            item['reason'] = str(error)
        audited.append(item)
    by_type = {}
    for record_type in MANIPULATED_TYPES:
        group = [item for item in audited if item['record_type'] == record_type]
        if not group:
            continue
        counts = Counter(item['outcome'] for item in group)
        by_type[record_type] = {'record_count': len(group), **{key: counts[key] for key in OUTCOMES},
                               'qualifying_record_ids': [item['record_id'] for item in group
                                                         if item['outcome'] == required_outcome]}
    passed = (all(counts['qualifying_record_ids'] for counts in by_type.values())
              if required_outcome else None)
    return {'baseline': {name: action_summary(result.policies, context)['action'] for name, context in
                         [('diagnostic', diagnostic_context), ('control', control_context)]},
            'records': audited, 'by_type': by_type, 'required_outcome': required_outcome, 'passed': passed}
