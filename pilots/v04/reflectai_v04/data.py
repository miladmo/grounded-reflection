"""Seeded synthetic work histories; future instances are generated separately."""

import hashlib
import json
import random
from collections import Counter

from reflectai_v03.context import render_rules
from reflectai_v03.contracts import (
    CandidateTarget, History, HistoryTruth, OutputField, Record, Task, TaskTruth,
)

from .data_contracts import Case, FieldOption, GeneratorConfig, PublicFrame
from .counterfactual import assess_assignment, audit_counterfactuals
from .presentation import PERSON_NAMES, present_history
from .oracle import (
    H14_MASKS, alternative_values, baseline_values, context_cells, infer_policies,
    option_rule, policy_from_masks, read_frame, policy_option_at,
)

FAMILIES = ('hr', 'sales', 'retrieval', 'reporting')
ALLOCATION = {
    'S0': ('change', 'change', 'resolved_keep', 'unidentifiable'),
    'S1': ('resolved_keep', 'unidentifiable', 'change', 'change'),
    'S2': ('change', 'resolved_keep', 'unidentifiable', 'change'),
    'S3': ('unidentifiable', 'change', 'change', 'resolved_keep'),
    'S4': ('change', 'change', 'resolved_keep', 'unidentifiable'),
    'S5': ('resolved_keep', 'unidentifiable', 'change', 'change'),
}
TASK_TYPE_ALLOCATION = {
    'S0': ('transfer_change', 'observed_change', 'resolved_retention_transfer', 'unidentifiable'),
    'S1': ('resolved_retention_transfer', 'unidentifiable', 'observed_change', 'transfer_change'),
    'S2': ('observed_change', 'resolved_retention_transfer', 'unidentifiable', 'transfer_change'),
    'S3': ('unidentifiable', 'transfer_change', 'observed_change', 'resolved_retention_transfer'),
    'S4': ('transfer_change', 'observed_change', 'resolved_retention_transfer', 'unidentifiable'),
    'S5': ('resolved_retention_transfer', 'unidentifiable', 'transfer_change', 'observed_change'),
}
NOISE_QUOTAS = {
    'S2': {'unauthorised_revision': 12, 'rejected_opposite_artifact': 12,
           'target_field_preference': 12, 'approval_without_target': 12, 'technical': 8},
    'S5': {'unauthorised_revision': 10, 'rejected_opposite_artifact': 10,
           'target_field_preference': 10, 'approval_without_target': 10, 'technical': 6,
           'forward_current': 4, 'forward_old': 4},
}

ASSUMPTIONS = (
    'This is a bounded synthetic workflow model. initial_configuration declares the field '
    'options, two context dimensions and the complete H14 hypothesis class. Each registered '
    'version has one class member. A field observation constrains the member indexed by its '
    'recorded version. Broader consequences follow from the declared class. Facts provide '
    'current artifact values. Other fields retain their configured baseline. Outside the '
    'declared task_family and workflow, or without a complete declared context, no update '
    'is authorised by this model. A register_version event supplies trusted workflow metadata '
    'with the authority roster and half-open validity interval. Binding field approval is an '
    'event of type review with decision accept, performed by a listed reviewer within that '
    'interval, with the field included in reviewed_fields. Its accepted artifact establishes '
    'the field configuration at the recorded context. This explicit approval convention is '
    'a supplied synthetic assumption. A forward has an origin_ref identifying the record '
    'whose content it reproduces. Raw artifacts expose named revisions and a selected artifact '
    'reference; interpreted records expose the selected fields directly. A rejection records '
    'a whole-artifact decision and its stated grounds. An artifact field whose review is not '
    'recorded has no approved assignment. The configured baseline is retained when the '
    'available evidence does not establish an update. Dates and version labels in new work '
    'identify the applicable registration.'
)


def _json(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def _seed(*parts):
    digest = hashlib.sha256('|'.join(map(str, parts)).encode()).digest()
    return int.from_bytes(digest[:8], 'big')


def _opaque(rng, prefix):
    return f'{prefix}-{rng.getrandbits(48):012x}'


def _fields(values):
    return [OutputField(name=key, value=value) for key, value in values.items()]


def _frame(family, rng, config):
    reverse = bool(rng.getrandbits(1))
    workflow = _opaque(rng, 'workflow')
    if family == 'hr':
        dimensions = {'recipient': ['internal', 'external'], 'contract': ['permanent', 'temporary']}
        target, template = 'booking_reference', {'message': '{message}', 'work_email': '{work_email}'}
        option = FieldOption(field=target, operation='set_fact', value=target)
        if reverse:
            template[target] = '{booking_reference}'
            option = FieldOption(field=target, operation='omit')
        descriptions = {'message': 'Current personnel document text.',
                        'work_email': 'Current contact email.', target: 'Current booking reference.'}
        task_family = 'personnel_document'
    elif family == 'sales':
        names = rng.sample(['Mira', 'Leon', 'Sada', 'Nora', 'Emil', 'Alex'], 2)
        dimensions = {'account_owner': names, 'customer_segment': ['standard', 'strategic']}
        target, template = 'annual_total', {'offer_text': '{offer_text}', 'contract_reference': '{contract_reference}'}
        option = FieldOption(field=target, operation='set_fact', value=target)
        if reverse:
            template[target] = '{annual_total}'
            option = FieldOption(field=target, operation='omit')
        descriptions = {'offer_text': 'Current offer text.', 'contract_reference': 'Current offer reference.',
                        'monthly_unit_price': 'EUR per seat and month.', 'seats': 'Number of seats.',
                        target: 'EUR, monthly_unit_price times seats times twelve.'}
        task_family = 'sales_offer'
    elif family == 'retrieval':
        dimensions = {'collection': ['active', 'archive'], 'document_class': ['protocol', 'assay_report']}
        target = 'source_route'
        template = {target: '{configured_route}', 'release_id': '{release_id}', 'checksum_check': 'required'}
        option = FieldOption(field=target, operation='set_fact', value='alternative_route')
        descriptions = {'configured_route': 'Endpoint selected by the initial configuration.',
                        'alternative_route': 'The other available endpoint.', 'release_id': 'Requested release.',
                        'checksum_check': 'The exact canonical marker required means verify the retrieved checksum.'}
        task_family = 'document_retrieval'
    else:
        dimensions = {'artifact': ['chart', 'numeric_table'], 'audience': ['internal', 'external']}
        target = 'title'
        template = {target: '{base_title}', 'source_footnote': '{source_footnote}'}
        option = FieldOption(field=target, operation='append_fact', value='snapshot', separator=' | ')
        if reverse:
            template[target] = '{base_title} | {snapshot}'
            option = FieldOption(field=target, operation='set_fact', value='base_title')
        descriptions = {'base_title': 'Current title without a snapshot suffix.',
                        'snapshot': 'Current snapshot label.', 'source_footnote': 'Current source note.'}
        task_family = 'report_artifact'
    replacement = config.families.get(family)
    if replacement:
        task_family = replacement.task_family or task_family
        dimensions = replacement.dimensions or dimensions
        if replacement.field:
            if target in template:
                template[replacement.field] = template.pop(target)
            option = option.model_copy(update={'field': replacement.field})
        option = replacement.field_option or option
        template = replacement.baseline_template or template
        descriptions = replacement.fact_descriptions or descriptions
    return PublicFrame(task_family=task_family, workflow=workflow, as_of='2026-06-15T12:00:00Z',
                       dimensions=dimensions, field_option=option, baseline_template=template,
                       fact_descriptions=descriptions), reverse


def _facts(family, frame, rng):
    serial = rng.randrange(10000, 99999)
    common = {'document_id': f'DOC-{serial}', 'date': '2026-06-15'}
    if family == 'hr':
        return {**common, 'message': f'Please prepare the appointment documents for case {serial}.',
                'work_email': f'contact{serial}@example.test', 'booking_reference': f'BK-{serial}'}
    if family == 'sales':
        price, seats = rng.choice([25, 40, 50, 65]), rng.choice([5, 10, 15, 20])
        return {**common, 'monthly_unit_price': str(price), 'seats': str(seats),
                'annual_total': str(price * seats * 12), 'contract_reference': f'OFF-{serial}',
                'offer_text': f'{seats} seats at EUR {price} per seat per month, billed annually.'}
    if family == 'retrieval':
        token = frame.workflow.split('-')[-1]
        # The ordered route names vary independently of a case's intended action.
        routes = sorted([f'index-{token[:6]}', f'index-{token[6:]}'])
        if int(token, 16) % 2:
            routes.reverse()
        return {**common, 'configured_route': routes[0], 'alternative_route': routes[1],
                'release_id': f'REL-{serial}', 'checksum': f'sha256:{rng.getrandbits(128):032x}'}
    return {**common, 'base_title': f'Quarterly allocation {serial}', 'snapshot': f'SNAP-{serial}',
            'source_footnote': f'Source: approved extract EX-{serial}.'}


def _task(frame, family, context, rng, task_id):
    facts = _facts(family, frame, rng)
    facts['date'] = frame.as_of[:10]
    return Task(task_id=task_id, context=context, facts=facts,
                baseline_fields=_fields(baseline_values(frame, facts)),
                request='Complete the current work item using the supplied facts and field dictionary. '
                        'Use only contextually supported adjustments. Retain all unaffected fields.')


def _scope_probes(frame, family, versions, rng):
    contexts = []
    for version in versions:
        for cell in context_cells(frame):
            context = {'task_family': frame.task_family, 'workflow': frame.workflow, 'version': version, **cell}
            contexts.append(context)
            for key in context:
                missing = dict(context)
                del missing[key]
                contexts.append(missing)
                contexts.append({**context, key: 'outside-registered-domain'})
    unique = {_json(context): context for context in contexts}
    probes = []
    for context in unique.values():
        task = _task(frame, family, context, rng, _opaque(rng, 'witness'))
        if context.get('version') in versions[:-1]:
            task.facts['date'] = '2026-05-15'
        probes.append(task)
    return probes


def _make_case(seed, split, setting, family, regime, config):
    rng = random.Random(seed)
    frame, reverse = _frame(family, rng, config)
    case_id, history_id = _opaque(rng, 'case'), _opaque(rng, 'history')
    task_type = TASK_TYPE_ALLOCATION[setting][FAMILIES.index(family)]
    cells = context_cells(frame)
    flip_x, flip_y, swap = rng.randrange(2), rng.randrange(2), bool(rng.getrandbits(1))

    def mapped(index):
        x, y = (index // 2) ^ flip_x, (index % 2) ^ flip_y
        if swap:
            x, y = y, x
        return 2 * x + y

    templates = {
        'transfer_change': ([(0, 0), (1, 1), (2, 1)], 3, 0, 14),
        'observed_change': ([(0, 0), (2, 1), (2, 1)], 2, 0, 12),
        'resolved_retention_transfer': ([(0, 1), (1, 0), (2, 0)], 3, 1, 1),
        'unidentifiable': ([(0, 0), (3, 1), (0, 0)], 2, 1, 12),
    }
    observations, diagnostic_abstract, control_abstract, abstract_world = templates[task_type]
    observations = [(mapped(index), bit) for index, bit in observations]
    diagnostic, control_index = mapped(diagnostic_abstract), mapped(control_abstract)
    current_mask = sum(1 << mapped(index) for index in range(4) if abstract_world & (1 << index))
    temporal, raw = setting in ('S4', 'S5'), setting in ('S1', 'S5')
    current_version = _opaque(rng, 'edition')
    old_version = _opaque(rng, 'edition') if temporal else None
    versions = [old_version, current_version] if temporal else [current_version]
    world_masks = {current_version: current_mask}
    records, registry, reviewers = [], {}, {}
    record_options = {}
    dictionary = {key: f'Configured output field {key}; preserve unless an applicable update is established.'
                  for key in frame.baseline_template}
    dictionary[frame.field_option.field] = (
        f'Canonical field {frame.field_option.field}. Available alternative operation '
        f'{frame.field_option.operation}, value={frame.field_option.value!r}, '
        f'separator={frame.field_option.separator!r}. Its requirement depends on the evidence.')
    dictionary.update({f'fact.{key}': value for key, value in frame.fact_descriptions.items()})

    def make_history():
        return History(history_id=history_id, initial_configuration=frame.model_dump_json(),
                       assumptions=ASSUMPTIONS, field_dictionary=dictionary, records=list(records))

    def context_for(version, index):
        return {'task_family': frame.task_family, 'workflow': frame.workflow,
                'version': version, **cells[index]}

    def add(kind, actor, context, event, timestamp):
        record = Record(record_id=_opaque(rng, 'record'), timestamp=timestamp, kind=kind,
                        actor=actor, context=context, observation=_json(event))
        records.append(record)
        return record.record_id

    def register(version, old=False):
        reviewers[version] = rng.sample(PERSON_NAMES, 2)
        start = '2026-01-01T00:00:00Z' if old or not temporal else '2026-06-01T00:00:00Z'
        end = '2026-06-01T00:00:00Z' if old else '2027-01-01T00:00:00Z'
        registry[version] = add('template', 'workflow-registry', {}, {
            'event': 'register_version', 'version': version, 'workflow': frame.workflow,
            'task_family': frame.task_family, 'valid_from': start, 'valid_until': end,
            'authorised_reviewers': reviewers[version],
            'supersedes': registry.get(old_version) if not old else None,
        }, start)

    def review_event(version, index, bit, ordinal=0, timestamp=None):
        stamp = timestamp or (f'2026-05-{10 + ordinal:02d}T10:00:00Z' if version == old_version
                              else f'2026-06-{10 + ordinal:02d}T10:00:00Z')
        facts = _facts(family, frame, rng)
        facts['date'] = stamp[:10]
        choices = [baseline_values(frame, facts), alternative_values(frame, facts)]
        before, after = choices[1 - bit], choices[bit]
        event = {'event': 'review', 'format': 'raw' if raw else 'interpreted',
                 'document_id': facts['document_id'], 'authority_ref': registry[version],
                 'facts': facts, 'reviewed_fields': [frame.field_option.field],
                 'decision': 'accept', 'comment': 'Approved.'}
        if raw:
            event.update({'artifacts': {'draft': {'revision': 'draft', 'fields': before},
                                        'replacement': {'revision': 'reviewed', 'fields': after}},
                          'accepted_artifact': 'replacement'})
        else:
            field = frame.field_option.field
            event.update({'accepted_fields': after,
                          'change_summary': {'field': field, 'before': before.get(field), 'after': after.get(field)}})
        return event, stamp

    def authorised_review(version, index, bit, ordinal=0):
        event, stamp = review_event(version, index, bit, ordinal)
        record_id = add('review', reviewers[version][ordinal % 2], context_for(version, index), event, stamp)
        record_options[record_id] = bit
        return record_id

    if temporal:
        register(old_version, old=True)
    register(current_version)
    current_reviews = [authorised_review(current_version, index, bit, ordinal)
                       for ordinal, (index, bit) in enumerate(observations)]
    diagnostic_context = context_for(current_version, diagnostic)
    control_context = context_for(current_version, control_index)
    required_outcome = 'action_flip' if task_type == 'unidentifiable' else 'contradiction'
    core_oracle = infer_policies(make_history())
    qualifying = []
    for index in range(4):
        for bit in (0, 1):
            effect = assess_assignment(core_oracle, context_for(current_version, index), bit,
                                       diagnostic_context, control_context)
            if effect['outcome'] == required_outcome:
                qualifying.append((index, bit))
    if not qualifying:
        raise ValueError('the public core admits no registered counterfactual qualification')
    # This selection searches eight public assignments, not model outcomes or replacement seeds.
    rng.shuffle(qualifying)
    old_record = None
    if temporal:
        index, bit = qualifying[0]
        old_masks = [mask for mask in H14_MASKS if int(bool(mask & (1 << index))) == bit]
        world_masks[old_version] = rng.choice(old_masks)
        old_record = authorised_review(old_version, index, bit)

    def forward(origin, index, ordinal):
        return add('revision', 'forwarding-service', context_for(current_version, index), {
            'event': 'forward', 'origin_ref': origin,
            'message': 'Forwarded artifact for the next work item.',
        }, f'2026-06-14T11:{ordinal % 60:02d}:00Z')

    def destination_for(source, ordinal, qualify):
        bit = record_options[source]
        candidates = [(index, value) for index, value in qualifying if value == bit]
        if qualify:
            if not candidates:
                raise ValueError('visible origin has no qualifying current-context promotion')
            return candidates[ordinal % len(candidates)][0]
        return rng.randrange(4)

    def manipulated(record_type, ordinal):
        index, bit = qualifying[ordinal % len(qualifying)] if ordinal == 0 else (rng.randrange(4), rng.randrange(2))
        event, stamp = review_event(current_version, index, bit, timestamp='2026-06-14T09:00:00Z')
        context = context_for(current_version, index)
        actor, kind = reviewers[current_version][ordinal % 2], 'review'
        if record_type == 'unauthorised_revision':
            actor, kind = 'document-editor', 'revision'
            event['comment'] = 'Updated the proposed export.'
        elif record_type == 'rejected_opposite_artifact':
            event['decision'] = 'reject'
            event['comment'] = 'Rejected because the signature block is missing. Field-level review was not completed.'
            event['reviewed_fields'] = []
            if raw:
                event['rejected_artifact'] = event.pop('accepted_artifact')
            else:
                event['rejected_fields'] = event.pop('accepted_fields')
        elif record_type == 'approval_without_target':
            event['reviewed_fields'] = ['delivery_timestamp']
            event['comment'] = 'Delivery timestamp approved.'
            if raw:
                selected = event['artifacts'][event['accepted_artifact']]['fields']
            else:
                selected = event['accepted_fields']
            selected['delivery_timestamp'] = '2026-06-14T08:00:00Z'
        elif record_type == 'target_field_preference':
            if raw:
                fields = event['artifacts'][event['accepted_artifact']]['fields']
            else:
                fields = event['accepted_fields']
            field = frame.field_option.field
            wording = f'{field} should be {fields[field]!r}' if field in fields else f'{field} should be omitted'
            event = {'event': 'preference', 'facts': event['facts'], 'proposed_fields': fields,
                     'message': f'My preference for this work item is that {wording}.'}
            actor, kind = 'work-item-author', 'revision'
        else:
            raise ValueError(f'unsupported registered record type {record_type}')
        return add(kind, actor, context, event, stamp)

    def technical(ordinal):
        return add('tool', 'runtime', context_for(current_version, rng.randrange(4)), {
            'event': 'execution', 'request_id': _opaque(rng, 'request'),
            'attempts': [{'attempt': 1, 'http_status': 503}, {'attempt': 2, 'http_status': 200}],
            'log': 'The request completed on retry.',
        }, f'2026-06-14T08:{ordinal % 60:02d}:00Z')

    additional_counts = Counter()
    if setting in ('S0', 'S1'):
        manipulated('target_field_preference', 0)
        technical(0)
        additional_counts.update({'target_field_preference': 1, 'technical': 1})
    elif setting == 'S3':
        for ordinal in range(2):
            index, bit = qualifying[ordinal % len(qualifying)]
            source = next(record_id for record_id in current_reviews if record_options[record_id] == bit)
            forward(source, index, ordinal)
        additional_counts['forward_current'] = 2
    elif setting in NOISE_QUOTAS:
        for record_type, count in NOISE_QUOTAS[setting].items():
            for ordinal in range(count):
                if record_type == 'technical':
                    technical(ordinal)
                elif record_type == 'forward_old':
                    forward(old_record, destination_for(old_record, ordinal, qualify=(ordinal == 0)), ordinal)
                elif record_type == 'forward_current':
                    if ordinal == 0:
                        index, bit = qualifying[0]
                        source = next(record_id for record_id in current_reviews if record_options[record_id] == bit)
                    else:
                        source = rng.choice(current_reviews)
                        index = destination_for(source, ordinal, qualify=False)
                    forward(source, index, ordinal + 4)
                else:
                    manipulated(record_type, ordinal)
            additional_counts[record_type] = count

    expected_records = 60 if setting in ('S2', 'S5') else 6
    if len(records) != expected_records:
        raise ValueError(f'incorrect record quota: {len(records)} instead of {expected_records}')
    history = present_history(make_history(), _seed('reflectai-v04-amendment3-r2-presentation', seed))
    oracle = infer_policies(history)
    counterfactual = audit_counterfactuals(history, diagnostic_context, control_context, required_outcome)
    if not counterfactual['passed']:
        failed = [key for key, value in counterfactual['by_type'].items() if not value['qualifying_record_ids']]
        raise ValueError(f'counterfactual qualification failed for {failed}')
    world = policy_from_masks(frame, world_masks, 'actual-world')
    probes = _scope_probes(frame, family, versions, rng)
    world_signature = [render_rules(probe, world.rules) for probe in probes]
    if not any([render_rules(probe, policy.rules) for probe in probes] == world_signature
               for policy in oracle.policies):
        raise ValueError(f'generated world is incompatible with public evidence: seed={seed}')
    targets = []
    for version in versions:
        for index in range(4):
            context = context_for(version, index)
            changes = [policy_option_at(policy, context) for policy in oracle.policies]
            status = 'adopt' if all(changes) else 'reject' if not any(changes) else 'unresolved'
            targets.append(CandidateTarget(target_id=f'target-{len(targets)}', status=status,
                                           rule=option_rule(frame, context)))
    truth = HistoryTruth(history_id=history_id, scenario_id=f'{setting}-{family}', pair_id=case_id,
                         world_policy=world, admissible_policies=oracle.policies,
                         candidate_targets=targets, scope_probes=probes)
    intended_target = targets[(4 if temporal else 0) + diagnostic].status
    expected_status = {'change': 'adopt', 'resolved_keep': 'reject', 'unidentifiable': 'unresolved'}[regime]
    if intended_target != expected_status:
        raise ValueError(f'intended regime not warranted: seed={seed}, intended={regime}, derived={intended_target}')
    current_masks = {sum(policy_option_at(policy, context_for(current_version, index)) << index
                         for index in range(4)) for policy in oracle.policies}
    return Case(case_id=case_id, setting=setting, family=family, regime=regime, seed=seed, split=split,
                history=history, truth=truth, diagnostic_context=diagnostic_context,
                control_context=control_context, oracle_audit=oracle.evidence_audit,
                material_audit={'material_revision': 'v04-amendment-03-r2', 'task_type': task_type,
                                'record_count': len(records), 'rendering': 'raw' if raw else 'interpreted',
                                'additional_noise_counts': dict(additional_counts), 'reversed_option': reverse,
                                'current_witness_contexts': [context_for(current_version, index)
                                                             for index, _ in observations],
                                'diagnostic_observed': diagnostic in {index for index, _ in observations},
                                'control_basis': ('unidentifiable_baseline_world' if regime == 'unidentifiable'
                                                  else 'resolved_keep'),
                                'registered_versions': versions, 'admissible_count': len(oracle.policies),
                                'current_admissible_count': len(current_masks),
                                'counterfactual': counterfactual})

def generate_histories(seed: int, split='development', settings=None,
                       config: GeneratorConfig | None = None) -> list[Case]:
    """Generate histories and private evaluator material, never final task instances.

    Namespace separation is intrinsic to the seed derivation. No rejected seed is
    redrawn; construction errors carry the exact case seed in the exception.
    """
    if split not in ('development', 'review', 'final_test', 'test_fixture'):
        raise ValueError('unsupported material split')
    selected = list(ALLOCATION) if settings is None else list(settings)
    if not selected or len(set(selected)) != len(selected) or any(item not in ALLOCATION for item in selected):
        raise ValueError('settings must be a nonempty unique subset of S0..S5')
    config = config or GeneratorConfig()
    cases = []
    for setting in selected:
        for index, family in enumerate(FAMILIES):
            case_seed = _seed('reflectai-v04-amendment3-r2-history', split, seed, setting, family)
            try:
                cases.append(_make_case(case_seed, split, setting, family, ALLOCATION[setting][index], config))
            except (ValueError, KeyError, TypeError) as error:
                raise ValueError(f'material generation failed: setting={setting}, family={family}, '
                                 f'seed={case_seed}, split={split}: {error}') from error
    return cases


def generate_future_tasks(case: Case, seed: int) -> list[tuple[Task, TaskTruth]]:
    """Call only after preparation is sealed. This API has no preparation input."""
    rng = random.Random(_seed('reflectai-v04-amendment3-r2-future', case.split, case.seed, seed))
    frame = read_frame(case.history)
    diagnostic = dict(case.diagnostic_context)
    control = dict(case.control_context)
    current = infer_policies(case.history).current_version
    if any(context.get('version') != current for context in (diagnostic, control)):
        raise ValueError('future task version must be publicly current at its recorded date')
    result = []
    for probe, context in [('diagnostic', diagnostic), ('control', control)]:
        task = _task(frame, case.family, context, rng, _opaque(rng, 'task'))
        base = {field.name: field.value for field in task.baseline_fields}
        outcomes = [render_rules(task, policy.rules) for policy in case.truth.admissible_policies]
        consensus = outcomes[0] if all(value == outcomes[0] for value in outcomes) else base
        world = render_rules(task, case.truth.world_policy.rules)
        truth = TaskTruth(task_id=task.task_id, history_id=case.history.history_id, probe=probe,
                          expected_decision='apply' if consensus != base else 'keep',
                          recoverable=consensus == world, world_fields=_fields(world))
        result.append((task, truth))
    return result
