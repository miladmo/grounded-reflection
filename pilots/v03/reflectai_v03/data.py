"""Seeded synthetic histories, with evaluator truth kept out of public inputs.

Future tasks are instantiated separately, after the runner freezes preparations.
The bounded policies are author assumptions, not claims about real organisations.
"""

from __future__ import annotations

import hashlib
import random
from datetime import datetime, timedelta, timezone

from grounded_reflection.models import Scope

from .contracts import (
    CandidateTarget, Dataset, History, HistoryTruth, OutputField, Policy, Record,
    Rule, Task, TaskTruth,
)


def _id(seed: int, split: str, namespace: str) -> str:
    return hashlib.sha256(f'{seed}|{split}|{namespace}'.encode()).hexdigest()[:16]


def _fields(values: dict[str, str]) -> list[OutputField]:
    return [OutputField(name=key, value=value) for key, value in values.items()]


def _rule(field: str, operation: str, scope: dict[str, list[str]],
          value: str = '', separator: str = '') -> Rule:
    return Rule(field=field, operation=operation, scope=Scope(match=scope),
                value=value, separator=separator)


def _policy(name: str, *rules: Rule) -> Policy:
    return Policy(policy_id=name, rules=list(rules))


def _target(name: str, status: str, rule: Rule) -> CandidateTarget:
    return CandidateTarget(target_id=name, status=status, rule=rule)


def _scope(base: dict[str, list[str]], **extra: str | list[str]) -> dict[str, list[str]]:
    return {**base, **{key: value if isinstance(value, list) else [value]
                     for key, value in extra.items()}}


def _records(seed: int, split: str, scenario: str,
             events: list[tuple[str, str, dict[str, str], str]]) -> list[Record]:
    start = datetime(2026, 8, 3, 9, 30, tzinfo=timezone.utc)
    offsets = [timedelta(minutes=index) for index in range(len(events))]
    if scenario == 'S05':
        offsets = [timedelta(), timedelta(seconds=20), timedelta(minutes=2),
                   timedelta(minutes=3), timedelta(days=1)]
    elif scenario == 'S06':
        offsets[-2:] = [timedelta(days=2), timedelta(days=3)]
    return [Record(record_id=_id(seed, split, f'{scenario}:record:{index}'),
                   timestamp=(start + offsets[index]).isoformat(), kind=kind,
                   actor=actor, context=context, observation=observation)
            for index, (kind, actor, context, observation) in enumerate(events)]


ASSUMPTIONS = (
    'All records and people are synthetic. Reviewers have authority for their '
    'recorded local workflow and period. Separate record identifiers denote separate '
    'reviews unless an observation explicitly describes a repeated attempt. The '
    'workflow is stable during this period except for changes recorded in the events. '
    'Future tasks occur within that same stable workflow period. In this bounded '
    'experiment, evaluated worker roles use the same local workflow rules. work_role '
    'records performer provenance, not a requirement trigger. This role invariance '
    'is supplied as a precondition, not inferred from the records. Reviewer-specific '
    'sign-off conditions may still differ. task_family and workflow are separate '
    'scope attributes. '
    'An accepted baseline remains applicable where no supported exception changes it. '
    'Do not infer an organisation-wide rule from a local review. Missing evidence is '
    'an internal uncertainty, not a reason to ask an employee or stop this synthetic task.'
)


def _probe(scenario: str, index: int, context: dict[str, str],
           baseline: dict[str, str], facts: dict[str, str]) -> Task:
    return Task(task_id=f'private-probe-{scenario}-{index}', context=context,
                facts=facts, baseline_fields=_fields(baseline),
                request='Evaluator-only scope probe; never send to a model.')


def build_histories(seed: int, split: str = 'development') -> Dataset:
    """Create eight public histories and separate truth, but no future tasks."""
    if split not in ('development', 'final_test', 'test_fixture'):
        raise ValueError('unknown dataset split')
    rng = random.Random(seed)
    names = rng.sample(['Ari', 'Bea', 'Cleo', 'Dara', 'Elio', 'Faye', 'Gita',
                        'Hugo', 'Inez', 'Jori', 'Kian', 'Lena'], 9)
    a = {
        'hr_trigger': rng.choice(['recipient', 'contract']),
        'hr_baseline_reference': rng.choice(['present', 'absent']),
        'sales_baseline_annual': rng.choice(['present', 'absent']),
        'report_baseline_tag': rng.choice(['present', 'absent']),
        'tag_separator': rng.choice([' | ', ' / ', ' :: ']),
        'route_initial': f'ep-{rng.randrange(10000, 99999)}',
        'route_alternative': f'ep-{rng.randrange(10000, 99999)}',
        'hr_reviewer_1': names[0], 'hr_reviewer_2': names[1],
        'sales_local_reviewer': names[2], 'sales_other_reviewer': names[3],
        'sales_third_reviewer': names[4], 'sales_future_reviewer': names[5],
        'report_reviewer_1': names[6], 'report_reviewer_2': names[7],
        'history_snapshot': f'V{rng.randrange(100, 900)}',
    }
    # Opaque endpoints must differ even under an unlucky seeded draw.
    if a['route_initial'] == a['route_alternative']:
        a['route_alternative'] += 'x'
    histories, truths = [], []

    def add(scenario, pair, config, dictionary, events, world, admissible, targets, probes):
        history_id = _id(seed, split, f'history:{scenario}')
        histories.append(History(history_id=history_id, initial_configuration=config,
                                 assumptions=ASSUMPTIONS, field_dictionary=dictionary,
                                 records=_records(seed, split, scenario, events)))
        truths.append(HistoryTruth(history_id=history_id, scenario_id=scenario,
                                   pair_id=pair, world_policy=world,
                                   admissible_policies=admissible,
                                   candidate_targets=targets, scope_probes=probes))

    # HR: recipient and contract are distinct context variables, independent of role.
    base = {'task_family': ['contact_pack'], 'workflow': ['talent_ops']}
    op = 'omit' if a['hr_baseline_reference'] == 'present' else 'set_fact'
    value = '' if op == 'omit' else 'booking_reference'
    recipient = _rule('booking_reference', op, _scope(base, recipient='external'), value)
    contract = _rule('booking_reference', op, _scope(base, contract='temporary'), value)
    conjunction = _rule('booking_reference', op,
                        _scope(base, recipient='external', contract='temporary'), value)
    policies = [_policy('recipient', recipient), _policy('contract', contract),
                _policy('conjunction', conjunction), _policy('disjunction', recipient, contract)]
    true_rule = recipient if a['hr_trigger'] == 'recipient' else contract
    wrong_rule = contract if a['hr_trigger'] == 'recipient' else recipient
    true_policy = policies[0 if a['hr_trigger'] == 'recipient' else 1]
    hr_facts = {'booking_reference': 'BK-271', 'work_email': 'example@synthetic.invalid'}
    hr_baseline = {'work_email': hr_facts['work_email']}
    if a['hr_baseline_reference'] == 'present':
        hr_baseline['booking_reference'] = hr_facts['booking_reference']
    changed = 'removed booking_reference; work_email unchanged' if op == 'omit' else (
        'added booking_reference from source; work_email unchanged')
    restored = 'restored booking_reference from source' if op == 'omit' else (
        'removed the added booking_reference')

    def hr_context(recipient_value, contract_value, **extra):
        return {'task_family': 'contact_pack', 'workflow': 'talent_ops',
                'work_role': 'recruitment_coordinator', 'recipient': recipient_value,
                'contract': contract_value, **extra}

    hr_probes = []
    for rec, con in [('external', 'temporary'), ('external', 'permanent'),
                     ('internal', 'temporary'), ('internal', 'permanent'),
                     ('unclassified', 'permanent'), ('internal', 'unclassified')]:
        hr_probes.append(_probe('hr', len(hr_probes), hr_context(rec, con), hr_baseline, hr_facts))
    for override in [{'workflow': 'other_team'}, {'task_family': 'onboarding_note'},
                     {'work_role': 'department_coordinator'}]:
        hr_probes.append(_probe('hr', len(hr_probes), hr_context('external', 'temporary', **override),
                               hr_baseline, hr_facts))
    for missing in ['recipient', 'contract', 'workflow']:
        context = hr_context('external', 'temporary')
        del context[missing]
        hr_probes.append(_probe('hr', len(hr_probes), context, hr_baseline, hr_facts))
    fresh_hr_facts = {**hr_facts, 'booking_reference': 'BK-918'}
    fresh_hr_baseline = {**hr_baseline}
    if 'booking_reference' in fresh_hr_baseline:
        fresh_hr_baseline['booking_reference'] = fresh_hr_facts['booking_reference']
    hr_probes.append(_probe('hr', len(hr_probes), hr_context('external', 'temporary'),
                           fresh_hr_baseline, fresh_hr_facts))
    for scenario in ['S01', 'S02']:
        first, second = a['hr_reviewer_1'], a['hr_reviewer_2']
        events = [
            ('retrieval', 'records_service', hr_context('external', 'temporary'),
             'Pack P31 source contains booking_reference=BK-271 and work_email=example@synthetic.invalid.'),
            ('revision', first, hr_context('external', 'temporary'),
             f'P31 diff: {changed}. Approved. Undoing this sole change was rejected.'),
            ('review', first, hr_context('internal', 'permanent'),
             f'P32 approved with the configured booking_reference state ({a["hr_baseline_reference"]}); work_email retained.'),
            ('revision', second, hr_context('external', 'temporary'),
             f'Independent pack P33 diff: {changed}. Approved with its own source values.'),
        ]
        if scenario == 'S01':
            for rec, con in [('internal', 'temporary'), ('external', 'permanent')]:
                positive = (rec == 'external') if a['hr_trigger'] == 'recipient' else (con == 'temporary')
                events.append(('revision', second if rec == 'internal' else first,
                               hr_context(rec, con),
                               f'Pack P{len(events) + 30} diff: {changed if positive else restored}. '
                               'Approved with all other fields unchanged. Undo rejected.'))
            targets = [_target('identified-trigger', 'adopt', true_rule),
                       _target('rival-trigger', 'reject', wrong_rule)]
            admissible = [true_policy]
        else:
            events.extend([
                ('revision', second, hr_context('internal', 'permanent'),
                 f'P34 diff: {restored}. Approved, all other fields unchanged.'),
                ('revision', first, hr_context('external', 'temporary'),
                 f'P35 diff: {changed}. Approved, all other fields unchanged.'),
            ])
            targets = [_target('partial-intersection', 'adopt', conjunction),
                       _target('recipient-trigger', 'unresolved', recipient),
                       _target('contract-trigger', 'unresolved', contract)]
            admissible = policies
        add(scenario, 'P01',
            f'Contact packs in talent_ops always include work_email. The configured '
            f'booking_reference field is {a["hr_baseline_reference"]}. Source values remain available in facts. '
            'Formatting is a stable function of recipient and contract in this local workflow.',
            {'booking_reference': 'Neutral coordination token, not private candidate data.',
             'work_email': 'Synthetic work address.', 'recipient': 'internal or external',
             'contract': 'permanent or temporary', 'work_role': 'Worker role, distinct from task_family.'},
            events, true_policy, admissible, targets, hr_probes)

    # Sales: transfer to known reviewers; agreement does not identify unseen preferences.
    sales_base = {'task_family': ['renewal_preview'], 'workflow': ['account_ops']}
    sales_op = 'omit' if a['sales_baseline_annual'] == 'present' else 'set_fact'
    sales_value = '' if sales_op == 'omit' else 'annual_total'
    local = _rule('annual_total', sales_op,
                  _scope(sales_base, reviewer=a['sales_local_reviewer']), sales_value)
    shared = _rule('annual_total', sales_op, sales_base, sales_value)
    observed_reviewers = [a['sales_local_reviewer'], a['sales_other_reviewer'], a['sales_third_reviewer']]
    observed = _rule('annual_total', sales_op, _scope(sales_base, reviewer=observed_reviewers), sales_value)
    sales_facts = {'monthly_unit_price': '40', 'seat_count': '10', 'annual_total': '4800',
                   'contract_reference': 'CS-441'}
    sales_baseline = {key: sales_facts[key] for key in ['monthly_unit_price', 'seat_count', 'contract_reference']}
    if a['sales_baseline_annual'] == 'present':
        sales_baseline['annual_total'] = sales_facts['annual_total']

    def sales_context(reviewer, **extra):
        return {'task_family': 'renewal_preview', 'workflow': 'account_ops',
                'work_role': 'account_executive', 'reviewer': reviewer, **extra}

    sales_probes = []
    for reviewer in [*observed_reviewers, a['sales_future_reviewer']]:
        sales_probes.append(_probe('sales', len(sales_probes), sales_context(reviewer), sales_baseline, sales_facts))
    for override in [{'task_family': 'pipeline_forecast'}, {'workflow': 'other_team'},
                     {'work_role': 'renewals_specialist'}]:
        sales_probes.append(_probe('sales', len(sales_probes), sales_context(a['sales_local_reviewer'], **override),
                                  sales_baseline, sales_facts))
    for key in ['reviewer', 'workflow']:
        missing = sales_context(a['sales_local_reviewer'])
        del missing[key]
        sales_probes.append(_probe('sales', len(sales_probes), missing, sales_baseline, sales_facts))
    fresh_sales_facts = {**sales_facts, 'monthly_unit_price': '50', 'annual_total': '6000',
                         'contract_reference': 'CS-442'}
    fresh_sales_baseline = {field: fresh_sales_facts[field] for field in sales_baseline}
    sales_probes.append(_probe('sales', len(sales_probes), sales_context(a['sales_local_reviewer']),
                              fresh_sales_baseline, fresh_sales_facts))
    action = 'removes the annual_total line' if sales_op == 'omit' else 'adds the validated annual_total line'
    inverse = 'restores the validated annual_total line' if sales_op == 'omit' else 'removes the annual_total line'
    for scenario in ['S03', 'S04']:
        mira, leon, sada = (a[key] for key in ['sales_local_reviewer', 'sales_other_reviewer', 'sales_third_reviewer'])
        events = []
        reviewers = [mira, leon] if scenario == 'S03' else [mira, leon, sada]
        for case, role, monthly, amount, reference in [
            ('D41', 'account_executive', '40', '4800', 'CS-441'),
            ('D42', 'renewals_specialist', '50', '6000', 'CS-442'),
        ]:
            events.append(('tool', 'contract_calculator',
                           sales_context(mira, case_id=case, work_role=role),
                           f'{case} calculation: {monthly} per seat per month x 10 seats x 12 months '
                           f'= annual_total {amount}. Contract {reference} valid. Independent review '
                           'copies contain the same customer, contract, source metadata and document '
                           'content. Each reviewer receives the identical pair of drafts differing '
                           'only in the annual_total line, without the other reviewers\' decisions.'))
            for reviewer in reviewers:
                review_action = inverse if scenario == 'S03' and reviewer == leon else action
                approved_state = (a['sales_baseline_annual'] if scenario == 'S03' and reviewer == leon
                                  else 'absent' if sales_op == 'omit' else 'present')
                events.append(('revision', reviewer,
                               sales_context(reviewer, case_id=case, work_role=role),
                               f'{case} independent sign-off: {review_action}; all other fields '
                               f'unchanged. Approved annual_total state={approved_state}. '
                               'Approves this version and rejects the otherwise identical '
                               'alternative. The review concerns this reviewer\'s own sign-off.'))
        if scenario == 'S03':
            world = _policy('reviewer-specific', local)
            admissible = [world]
            targets = [_target('local-exception', 'adopt', local), _target('shared-convention', 'reject', shared)]
        else:
            world = _policy('workflow-convention', shared)
            admissible = [world, _policy('observed-reviewers', observed)]
            targets = [_target('observed-reviewer-convention', 'adopt', observed),
                       _target('shared-convention', 'unresolved', shared)]
        add(scenario, 'P02', f'Renewal preview baseline contains monthly_unit_price, seat_count, '
            f'contract_reference, with annual_total {a["sales_baseline_annual"]}. '
            'Reviewers have equal local sign-off authority for these previews. Each sign-off is '
            'independent and concerns the named reviewer. The same workflow and template version '
            'remain in effect throughout the recorded cases and future tasks. '
            'Use the configured baseline for a reviewer without a demonstrated exception. '
            'Pipeline forecasts have their own established template.',
            {'annual_total': 'Validated annual amount from the contract calculator.',
             'reviewer': 'Person approving this document, not its author.',
             'case_id': 'Source case identity used to match independent reviews of the same content.',
             'workflow': 'Local team process.', 'task_family': 'Document kind, distinct from worker role.'},
            events, world, admissible, targets, sales_probes)

    # Retrieval: recorded tool responses distinguish a transient incident from relocation.
    initial, alternative = a['route_initial'], a['route_alternative']
    route_base = {'task_family': ['retrieval_plan'], 'workflow': ['evidence_collection']}
    active = _rule('endpoint', 'set_literal', _scope(route_base, collection='active'), alternative)
    all_routes = _rule('endpoint', 'set_literal', route_base, alternative)
    route_facts = {'release_id': 'REL-42', 'checksum_check': 'required'}
    route_baseline = {'endpoint': initial, **route_facts}

    def route_context(collection, **extra):
        return {'task_family': 'retrieval_plan', 'workflow': 'evidence_collection',
                'work_role': 'research_scientist', 'collection': collection, **extra}

    route_probes = [_probe('route', index, route_context(collection), route_baseline, route_facts)
                    for index, collection in enumerate(['active', 'archive', 'unclassified'])]
    for override in [{'workflow': 'other_collection'}, {'task_family': 'literature_summary'},
                     {'work_role': 'research_associate'}]:
        route_probes.append(_probe('route', len(route_probes), route_context('active', **override), route_baseline, route_facts))
    for key in ['collection', 'workflow']:
        missing = route_context('active')
        del missing[key]
        route_probes.append(_probe('route', len(route_probes), missing, route_baseline, route_facts))
    for scenario in ['S05', 'S06']:
        if scenario == 'S05':
            events = [
                ('retrieval', initial, route_context('active'), 'I17 at 09:30:00 returns HTTP 503.'),
                ('tool', 'service_monitor', route_context('active'), f'{alternative} and ep-unrelated return HTTP 503 in the same minute as the I17 failure.'),
                ('retrieval', initial, route_context('active'), 'I17 retry two minutes after the incident returns requested release REL-41 with matching checksum CH-417.'),
                ('review', 'source_reviewer', route_context('active'), f'I17 cached REL-40 draft rejected; otherwise unchanged draft using recovered {initial} REL-41 accepted.'),
                ('retrieval', initial, route_context('active'), 'On the next workday, I18 returns requested current release REL-42 and matching checksum CH-428.'),
            ]
            world = _policy('unchanged-service')
            admissible = [world, _policy('active-alternative', active)]
            targets = [_target('durable-route-change', 'unresolved', active)]
        else:
            events = [
                ('retrieval', initial, route_context('active'), 'I17 returns REL-40. Requested release REL-41 check fails.'),
                ('tool', 'collection_inventory', route_context('active'), f'Active-collection inventory snapshot lists I17 REL-41 at {alternative}; retrieval there returns REL-41 with matching checksum CH-417.'),
                ('review', 'source_reviewer', route_context('active'), f'I17 draft using {initial} REL-40 rejected; replacement using {alternative} REL-41 accepted.'),
                ('retrieval', 'query_log', route_context('active'), f'Independent queries on two later days: I18 requests REL-41, '
                 f'{initial} returns REL-40 and {alternative} returns REL-41 with matching checksum CH-418; '
                 f'I19 requests REL-42, {initial} returns REL-40 and {alternative} returns REL-42 with matching checksum CH-429.'),
                ('retrieval', initial, route_context('archive'), 'Archived I02 returns its requested archived release REL-16 and matching checksum CH-162.'),
            ]
            world = _policy('active-relocation', active)
            admissible = [world, _policy('all-collections-alternative', all_routes)]
            targets = [_target('active-route', 'adopt', active), _target('global-route', 'unresolved', all_routes)]
        add(scenario, 'P03', f'The configured endpoint is {initial} for active and archived records. '
            'Every retrieval plan must name the requested release and require checksum verification. '
            'A source can return acceptable records without being uniquely preferred. Review '
            'approval certifies record correctness, not a mandatory endpoint, and does not '
            'by itself establish that another route is invalid. '
            'Plans are synthetic selections; no live retrieval takes place.',
            {'endpoint': 'Opaque service address.', 'collection': 'active or archive',
             'release_id': 'Requested record release, not merely the latest observed release.',
             'checksum_check': 'Verification marker. The canonical value "required" means that checksum verification must be performed; it is not a checksum result.'},
            events, world, admissible, targets, route_probes)

    # Reporting: parameterised title operations transfer to a fresh snapshot.
    sep, snapshot = a['tag_separator'], a['history_snapshot']
    report_base = {'task_family': ['study_report'], 'workflow': ['study_delta']}
    tag_present = a['report_baseline_tag'] == 'present'
    report_op, report_value = ('set_fact', 'base_title') if tag_present else ('append_fact', 'snapshot')
    chart = _rule('title', report_op, _scope(report_base, artifact='chart'), report_value,
                  '' if tag_present else sep)
    broad = _rule('title', report_op, _scope(report_base, artifact=['chart', 'numeric_table']),
                  report_value, '' if tag_present else sep)
    report_facts = {'base_title': 'Response distribution', 'snapshot': snapshot,
                    'source_footnote': f'Source dataset {snapshot}'}
    report_baseline = {'title': report_facts['base_title'] + (sep + snapshot if tag_present else ''),
                       'source_footnote': report_facts['source_footnote']}

    def report_context(artifact, **extra):
        return {'task_family': 'study_report', 'workflow': 'study_delta',
                'work_role': 'research_scientist', 'artifact': artifact, **extra}

    narrative_baseline = {'paragraph': 'The study records the response distribution.',
                           'source_footnote': report_facts['source_footnote']}
    report_probes = [_probe('report', index, report_context(artifact),
                            narrative_baseline if artifact == 'narrative' else report_baseline, report_facts)
                     for index, artifact in enumerate(['chart', 'numeric_table', 'narrative', 'image'])]
    for override in [{'workflow': 'other_study'}, {'task_family': 'presentation'},
                     {'work_role': 'research_associate'}]:
        report_probes.append(_probe('report', len(report_probes), report_context('chart', **override), report_baseline, report_facts))
    missing = report_context('chart')
    del missing['artifact']
    report_probes.append(_probe('report', len(report_probes), missing, report_baseline, report_facts))
    fresh_report_facts = {'base_title': 'Response by cohort', 'snapshot': 'V9999',
                          'source_footnote': 'Source dataset V9999'}
    fresh_report_baseline = {'title': fresh_report_facts['base_title'] + (sep + 'V9999' if tag_present else ''),
                             'source_footnote': fresh_report_facts['source_footnote']}
    report_probes.append(_probe('report', len(report_probes), report_context('chart'),
                               fresh_report_baseline, fresh_report_facts))
    action = f'removes the title suffix {sep!r} + {snapshot}' if tag_present else f'appends {sep!r} + {snapshot} to the title'
    inverse = f'restores the title suffix {sep!r} + {snapshot}' if tag_present else f'removes the title suffix {sep!r} + {snapshot}'
    for scenario in ['S07', 'S08']:
        hana, idris = a['report_reviewer_1'], a['report_reviewer_2']
        events = [
            ('retrieval', 'dataset_catalog', report_context('chart'), f'Dataset resolves to snapshot {snapshot}. Initial title has tag {a["report_baseline_tag"]}; source footnote already correct.'),
            ('revision', hana, report_context('chart'), f'Chart C11: {action}; source footnote unchanged; approved.'),
            ('revision', idris, report_context('chart'), f'Chart C12: rejects undoing that title change and {action}; source footnote unchanged; approved.'),
        ]
        table_action = inverse if scenario == 'S07' else action
        events.extend([
            ('revision', hana, report_context('numeric_table'), f'Table T21: {table_action}; source footnote unchanged; approved.'),
            ('review', idris, report_context('numeric_table'), f'Table T22: rejects undoing that title change; {table_action}; source footnote unchanged.'),
        ])
        world = _policy('chart-only' if scenario == 'S07' else 'exhibits', chart if scenario == 'S07' else broad)
        targets = ([_target('chart-rule', 'adopt', chart), _target('broader-rule', 'reject', broad)]
                   if scenario == 'S07' else [_target('exhibit-rule', 'adopt', broad)])
        add(scenario, 'P04', f'Study_delta exhibit titles start with snapshot tag {a["report_baseline_tag"]}. '
            f'The configured tag syntax is base_title + {sep!r} + snapshot when present. '
            'All outputs preserve the source footnote. Narrative paragraphs have no exhibit title.',
            {'title': 'Exhibit title.', 'base_title': 'Title before any snapshot suffix.',
             'snapshot': 'Current dataset identifier.', 'artifact': 'chart, numeric_table or narrative',
             'source_footnote': 'Required source reference independent of title formatting.'},
            events, world, [world], targets, report_probes)

    rng.shuffle(histories)
    return Dataset(split=split, seed=seed, histories=histories, truths=truths, assignments=a)


def build_tasks(dataset: Dataset, task_seed: int) -> Dataset:
    """Instantiate paired future inputs; caller must enforce the F1 freeze first."""
    from .context import render_rules

    if dataset.tasks or dataset.task_truths:
        raise ValueError('future tasks have already been instantiated')
    a = dataset.assignments
    rng = random.Random(task_seed)
    suffix = rng.randrange(10000, 99999)
    tasks, truths = [], []
    by_scenario = {truth.scenario_id: truth for truth in dataset.truths}
    for pair, scenarios in [('hr', ['S01', 'S02']), ('sales', ['S03', 'S04']),
                            ('retrieval', ['S05', 'S06']), ('reporting', ['S07', 'S08'])]:
        for probe in ['diagnostic', 'control']:
            context, facts, baseline, request = _future_input(pair, probe, a, suffix)
            for scenario in scenarios:
                truth = by_scenario[scenario]
                task_id = _id(task_seed, dataset.split, f'future:{scenario}:{probe}')
                task = Task(task_id=task_id, context=context, facts=facts,
                            baseline_fields=_fields(baseline), request=request)
                fields = render_rules(task, truth.world_policy.rules)
                decision = 'apply' if probe == 'diagnostic' and scenario in ['S01', 'S04', 'S06', 'S08'] else 'keep'
                tasks.append(task)
                truths.append(TaskTruth(task_id=task_id, history_id=truth.history_id, probe=probe,
                                        expected_decision=decision,
                                        recoverable=not (scenario == 'S02' and probe == 'diagnostic'),
                                        world_fields=_fields(fields)))
    rng.shuffle(tasks)
    return dataset.model_copy(update={'tasks': tasks, 'task_truths': truths}, deep=True)


def _future_input(pair: str, probe: str, a: dict[str, str], suffix: int):
    diagnostic = probe == 'diagnostic'
    if pair == 'hr':
        rec = 'external' if diagnostic and a['hr_trigger'] == 'recipient' else 'internal'
        con = 'temporary' if diagnostic and a['hr_trigger'] == 'contract' else 'permanent'
        context = {'task_family': 'contact_pack', 'workflow': 'talent_ops',
                   'work_role': 'recruitment_coordinator', 'recipient': rec, 'contract': con}
        facts = {'booking_reference': f'BK-{suffix}', 'work_email': f'worker{suffix}@synthetic.invalid'}
        baseline = {'work_email': facts['work_email']}
        if a['hr_baseline_reference'] == 'present':
            baseline['booking_reference'] = facts['booking_reference']
        request = 'Prepare the contact pack for this recipient and contract using these source values.'
    elif pair == 'sales':
        context = {'task_family': 'renewal_preview' if diagnostic else 'pipeline_forecast',
                   'workflow': 'account_ops', 'work_role': 'account_executive',
                   'reviewer': a['sales_other_reviewer'], 'case_id': f'D{suffix}'}
        facts = {'monthly_unit_price': '55', 'seat_count': '12', 'annual_total': '7920',
                 'contract_reference': f'CS-{suffix}'}
        if diagnostic:
            baseline = {key: facts[key] for key in ['monthly_unit_price', 'seat_count', 'contract_reference']}
            if a['sales_baseline_annual'] == 'present':
                baseline['annual_total'] = facts['annual_total']
            request = 'Prepare a renewal preview for this new case and the named reviewer using the validated contract values.'
        else:
            baseline = {'forecast_quarter': 'Q4', 'pipeline_total': '35000', 'currency': 'EUR'}
            request = 'Prepare this quarterly pipeline forecast using its established forecast fields.'
    elif pair == 'retrieval':
        context = {'task_family': 'retrieval_plan', 'workflow': 'evidence_collection',
                   'work_role': 'research_scientist', 'collection': 'active' if diagnostic else 'archive'}
        facts = {'release_id': 'REL-42' if diagnostic else 'REL-16', 'checksum_check': 'required'}
        baseline = {'endpoint': a['route_initial'], **facts}
        request = f'Prepare a structured retrieval plan for new record I{suffix}. Select the endpoint and preserve the requested release and checksum verification. Do not execute retrieval.'
    else:
        context = {'task_family': 'study_report', 'workflow': 'study_delta',
                   'work_role': 'research_scientist', 'artifact': 'numeric_table' if diagnostic else 'narrative'}
        snapshot = f'V{suffix}'
        facts = {'snapshot': snapshot, 'base_title': 'Response distribution',
                 'source_footnote': f'Source dataset {snapshot}'}
        if diagnostic:
            baseline = {'title': facts['base_title'] + (a['tag_separator'] + snapshot if a['report_baseline_tag'] == 'present' else ''),
                        'source_footnote': facts['source_footnote']}
            request = 'Prepare a numeric table title for the current snapshot and preserve its source footnote.'
        else:
            baseline = {'paragraph': 'The study records the response distribution.', 'source_footnote': facts['source_footnote']}
            request = 'Write the narrative paragraph with its established source reference; it has no exhibit title.'
    return context, facts, baseline, request
