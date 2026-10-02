"""Seeded synthetic v0.5 histories; future tasks are generated separately.

Construction follows docs/pilot-v05-protocol.md and the approved adjustment after the
constructibility check: per history three diagnostics (observed change, observed
retention, one hard task) and one control. A slot's design is searched
deterministically inside its own seeded stream; failure stops generation and no seed
is redrawn. The oracle re-derives every task status from public evidence only.
"""

from __future__ import annotations

import hashlib
import json
import random

from reflectai_v03.contracts import History, OutputField, Record, Task

from . import heuristics, hclass
from .contracts import CLASS_DEFINITIONS, Case, FieldOption, PublicFrame, TaskTruth
from .oracle import alternative_values, baseline_values, infer

SETTINGS = ('K-S', 'K-L', 'U-S', 'U-L')
FAMILIES = ('hr', 'sales', 'retrieval', 'reporting')
# (hard type, direction) per family and setting: every family appears once per
# setting; within each setting and hard type one omit and one add history.
ALLOCATION = {
    'K-S': {'hr': ('transfer_change', 'omit'), 'sales': ('transfer_change', 'add'),
            'retrieval': ('unidentifiable', 'omit'), 'reporting': ('unidentifiable', 'add')},
    'K-L': {'hr': ('unidentifiable', 'add'), 'sales': ('unidentifiable', 'omit'),
            'retrieval': ('transfer_change', 'add'), 'reporting': ('transfer_change', 'omit')},
    'U-S': {'hr': ('transfer_change', 'add'), 'sales': ('transfer_change', 'omit'),
            'retrieval': ('unidentifiable', 'add'), 'reporting': ('unidentifiable', 'omit')},
    'U-L': {'hr': ('unidentifiable', 'omit'), 'sales': ('unidentifiable', 'add'),
            'retrieval': ('transfer_change', 'omit'), 'reporting': ('transfer_change', 'add')},
}
BINDING_APPROVALS = 12
DISTRACTOR_QUOTAS = {
    'small': {'unauthorised_revision': 3, 'rejected_artifact': 2, 'target_field_preference': 2,
              'approval_without_target': 2, 'technical': 2},
    'large': {'unauthorised_revision': 49, 'rejected_artifact': 49, 'target_field_preference': 49,
              'approval_without_target': 49, 'technical': 31},
}
MAX_DESIGN_ATTEMPTS = 5000
AS_OF = '2026-06-15T12:00:00Z'
PERSON_NAMES = ('Anika', 'Robin', 'Theo', 'Daria', 'Jonas', 'Elena', 'Mira', 'Leon', 'Nora', 'Emil',
                'Sven', 'Lea', 'Paul', 'Ida', 'Malte', 'Greta')
COMMENTS = ('Approved.', 'Checked.', 'Reviewed.', 'Review complete.', 'Recorded.', 'Completed.')

FAMILY_VOCABULARY = {
    'hr': {
        'task_family': 'personnel_document',
        'attributes': {'recipient': ['internal', 'external'], 'contract': ['permanent', 'temporary'],
                       'location': ['onsite', 'remote'], 'seniority': ['junior', 'senior'],
                       'language': ['german', 'english'], 'channel': ['portal', 'email']},
        'fields': ('message', 'work_email'), 'target': 'booking_reference',
        'descriptions': {'message': 'Current personnel document text.', 'work_email': 'Current contact email.',
                         'booking_reference': 'Current booking reference.'}},
    'sales': {
        'task_family': 'sales_offer',
        'attributes': {'account_owner': ['Mira', 'Sada'], 'customer_segment': ['standard', 'strategic'],
                       'region': ['north', 'south'], 'contract_term': ['one_year', 'multi_year'],
                       'product_line': ['core', 'premium'], 'deal_source': ['direct', 'partner']},
        'fields': ('offer_text', 'contract_reference'), 'target': 'annual_total',
        'descriptions': {'offer_text': 'Current offer text.', 'contract_reference': 'Current offer reference.',
                         'monthly_unit_price': 'EUR per seat and month.', 'seats': 'Number of seats.',
                         'annual_total': 'EUR, monthly_unit_price times seats times twelve.'}},
    'retrieval': {
        'task_family': 'document_retrieval',
        'attributes': {'collection': ['active', 'archive'], 'document_class': ['protocol', 'assay_report'],
                       'site': ['lab_a', 'lab_b'], 'access': ['internal', 'partner'],
                       'file_format': ['pdf', 'xml'], 'priority': ['routine', 'urgent']},
        'fields': ('release_id', 'source_route'), 'target': 'checksum',
        'descriptions': {'release_id': 'Requested release.', 'source_route': 'Configured retrieval endpoint.',
                         'checksum': 'Checksum of the retrieved release.'}},
    'reporting': {
        'task_family': 'report_artifact',
        'attributes': {'artifact': ['chart', 'numeric_table'], 'audience': ['internal', 'external'],
                       'period': ['monthly', 'quarterly'], 'language': ['german', 'english'],
                       'department': ['finance', 'operations'], 'channel': ['portal', 'email']},
        'fields': ('title', 'source_footnote'), 'target': 'snapshot_label',
        'descriptions': {'title': 'Current report title.', 'source_footnote': 'Current source note.',
                         'snapshot_label': 'Current snapshot label.'}},
}

ASSUMPTIONS = (
    'This is a bounded synthetic workflow model. initial_configuration declares the field option, six '
    'binary context attributes, the candidate attributes and the complete hypothesis class. Facts provide '
    'current artifact values. Other fields retain their configured baseline. Outside the declared '
    'task_family, workflow and version, or without a complete declared context, no update is authorised by '
    'this model. A register_version event supplies trusted workflow metadata with the authority roster and '
    'half-open validity interval. Binding field approval is an event of type review with decision accept, '
    'performed by a listed reviewer within that interval, with the field included in reviewed_fields. Its '
    'accepted fields establish the field configuration at the recorded context. This explicit approval '
    'convention is a supplied synthetic assumption. A rejection records a whole-artifact decision and its '
    'stated grounds. A preference, an unreviewed field or a review by a person outside the roster supplies no '
    'approved assignment. The configured baseline is retained when the available evidence does not establish '
    'an update.'
)


def _json(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def _seed(*parts) -> int:
    return int.from_bytes(hashlib.sha256('|'.join(map(str, parts)).encode()).digest()[:8], 'big')


def _opaque(rng, prefix: str) -> str:
    return f'{prefix}-{rng.getrandbits(48):012x}'


def _fields(values: dict) -> list[OutputField]:
    return [OutputField(name=key, value=value) for key, value in values.items()]


def _frame(family: str, direction: str, condition: str, rng: random.Random):
    vocabulary = FAMILY_VOCABULARY[family]
    items = list(vocabulary['attributes'].items())
    rng.shuffle(items)
    attributes = {name: (values if rng.random() < 0.5 else values[::-1]) for name, values in items}
    target = vocabulary['target']
    template = {name: '{' + name + '}' for name in vocabulary['fields']}
    if direction == 'omit':
        template[target] = '{' + target + '}'
        option = FieldOption(field=target, operation='omit')
    else:
        option = FieldOption(field=target, operation='set_fact', value=target)
    relevant = sorted(rng.sample(range(6), 2))
    names = list(attributes)
    hclass_name = 'h14-declared' if condition == 'K' else 'h134'
    candidates = [names[i] for i in relevant] if condition == 'K' else names
    frame = PublicFrame(task_family=vocabulary['task_family'], workflow=_opaque(rng, 'workflow'),
                        version=_opaque(rng, 'edition'), as_of=AS_OF, attributes=attributes,
                        candidate_attributes=candidates, field_option=option, baseline_template=template,
                        fact_descriptions=dict(vocabulary['descriptions']), hypothesis_class=hclass_name,
                        hypothesis_definition=CLASS_DEFINITIONS[hclass_name])
    return frame, relevant


def _facts(family: str, rng: random.Random, date: str) -> dict:
    serial = rng.randrange(10000, 99999)
    common = {'document_id': f'DOC-{serial}', 'date': date}
    if family == 'hr':
        return {**common, 'message': f'Please prepare the appointment documents for case {serial}.',
                'work_email': f'contact{serial}@example.test', 'booking_reference': f'BK-{serial}'}
    if family == 'sales':
        price, seats = rng.choice([25, 40, 50, 65]), rng.choice([5, 10, 15, 20])
        return {**common, 'monthly_unit_price': str(price), 'seats': str(seats),
                'annual_total': str(price * seats * 12), 'contract_reference': f'OFF-{serial}',
                'offer_text': f'{seats} seats at EUR {price} per seat per month, billed annually.'}
    if family == 'retrieval':
        return {**common, 'release_id': f'REL-{serial}', 'source_route': f'index-{rng.getrandbits(24):06x}',
                'checksum': f'sha256:{rng.getrandbits(64):016x}'}
    return {**common, 'title': f'Quarterly allocation {serial}', 'source_footnote': f'Source: extract EX-{serial}.',
            'snapshot_label': f'SNAP-{serial}'}


def _project(cell: int, a: int, b: int) -> int:
    return hclass.bit(cell, a) | (hclass.bit(cell, b) << 1)


def _background_at_distance(rng, reference: int, mask: int, minimum: int) -> int:
    for _ in range(1000):
        background = rng.getrandbits(6)
        if bin((background ^ reference) & mask).count('1') >= minimum:
            return background
    raise ValueError('no background at the required distance')


def _known_design(relevant, hard_type, rng):
    """H14 over the two declared attributes (v0.4 templates) with r2 similarity placement.

    Within the relevant pair a warranted transfer always equals its two neighbour cells
    (an H14 property, reported as a limit). Over all six attributes, the irrelevant
    attributes are set so that the binding approvals nearest to the hard task come from
    the cell that shows the configuration that is *not* warranted there.
    """
    a, b = relevant
    mask = 0b111111 & ~((1 << a) | (1 << b))
    flip_a, flip_b = rng.randrange(2), rng.randrange(2)
    lit_a = hclass.literal_table(6, a, flip_a == 0)
    lit_b = hclass.literal_table(6, b, flip_b == 0)
    both = [p for p in range(4) if ((lit_a & lit_b) >> _cell_with(p, a, b, 0)) & 1][0]
    neither = [p for p in range(4) if not ((lit_a | lit_b) >> _cell_with(p, a, b, 0)) & 1][0]
    if hard_type == 'transfer_change':
        # Observing "neither" (0) and both single-literal cells (1) leaves only the
        # disjunction, so the unobserved "both" cell is warranted to change. Nearest
        # approvals: the diagonal "neither" cell (baseline); neighbours are far.
        world = lit_a | lit_b
        observed_projected = [neither] + [p for p in range(4) if p not in (both, neither)]
        hard_projected, near, far_minimum = both, neither, 2
    else:
        # Observing "neither" (0) and "both" (1) leaves x, y, x AND y, x OR y; a mixed
        # cell is unresolved (two of four functions change). Nearest approvals: "both"
        # (alternative); "neither" is far.
        world = rng.choice([lit_a, lit_b, lit_a & lit_b, lit_a | lit_b])
        observed_projected = [neither, both]
        hard_projected = rng.choice([p for p in range(4) if p not in observed_projected])
        near, far_minimum = both, 1
    hard_background = rng.getrandbits(6)
    per_cell = BINDING_APPROVALS // len(observed_projected)
    observed = []
    for projected in observed_projected:
        for copy in range(per_cell):
            if projected == near and copy < 2:
                background = hard_background
            elif projected != near:
                background = _background_at_distance(rng, hard_background, mask, far_minimum)
            else:
                background = rng.getrandbits(6)
            observed.append(_cell_with(projected, a, b, background))
    rng.shuffle(observed)
    hard_cell = _cell_with(hard_projected, a, b, hard_background)
    function = {'table': world, 'relevant': list(relevant), 'confusable': None}
    return function, observed, hard_cell


def _cell_with(projected: int, a: int, b: int, background: int) -> int:
    cell = background & ~((1 << a) | (1 << b))
    return cell | ((projected & 1) << a) | (((projected >> 1) & 1) << b)


def _unknown_design(relevant, hard_type, rng, klass):
    a, b = relevant
    confusable = rng.choice([x for x in range(6) if x not in relevant])
    anchor = rng.choice(relevant)
    for _ in range(MAX_DESIGN_ATTEMPTS):
        pa, pb = rng.random() < 0.5, rng.random() < 0.5
        la, lb = hclass.literal_table(6, a, pa), hclass.literal_table(6, b, pb)
        world = (la & lb) if rng.random() < 0.5 else (la | lb)
        observed = []
        for _ in range(BINDING_APPROVALS):
            cell = rng.getrandbits(6)
            cell = (cell & ~(1 << confusable)) | (hclass.bit(cell, anchor) << confusable)
            observed.append(cell)
        pairs = [(cell, hclass.value(world, cell)) for cell in observed]
        alternatives = sum(bit for _, bit in pairs)
        if alternatives < 2 or len(pairs) - alternatives < 2:   # r2: both configurations at least twice
            continue
        functions = hclass.compatible(klass, dict(pairs))
        seen = set(observed)
        unseen = [c for c in range(64) if c not in seen]
        if hard_type == 'transfer_change':
            # r2: the nearest binding approvals must show the baseline (not warranted here).
            hard = [c for c in unseen if hclass.status_at(functions, c) == 'apply'
                    and heuristics.nearest_neighbour(pairs, c) == 'keep']
        else:
            def probes_change(c):
                # r2: at least half of the compatible functions change, every function over
                # the confusable attribute changes, and the nearest approvals show the alternative.
                share = sum(hclass.value(f, c) for f in functions) / len(functions)
                via_confusable = [f for f in functions if confusable in f.attributes]
                return (share >= 0.5 and via_confusable and all(hclass.value(f, c) for f in via_confusable)
                        and heuristics.nearest_neighbour(pairs, c) == 'apply')
            hard = [c for c in unseen if hclass.status_at(functions, c) == 'unresolved'
                    and hclass.bit(c, confusable) != hclass.bit(c, anchor) and probes_change(c)]
        if hard:
            function = {'table': world, 'relevant': list(relevant), 'confusable': confusable, 'anchor': anchor}
            return function, observed, rng.choice(hard)
    raise ValueError('no constructible unknown-6 design within the registered attempt limit')


def _timestamp(rng) -> str:
    day = rng.randrange(5, 165)          # within the validity interval, before as_of
    month_days = [(1, 31), (2, 28), (3, 31), (4, 30), (5, 31), (6, 30)]
    for month, days in month_days:
        if day <= days:
            break
        day -= days
    return f'2026-{month:02d}-{max(day, 1):02d}T{rng.randrange(8, 18):02d}:{rng.randrange(60):02d}:00Z'


def make_case(seed: int, split: str, setting: str, family: str) -> Case:
    hard_type, direction = ALLOCATION[setting][family]
    condition, size = setting.split('-')
    rng = random.Random(seed)
    frame, relevant = _frame(family, direction, condition, rng)
    klass = hclass.rule_class(6, frame.candidate_indices())
    if condition == 'K':
        function, observed, hard_cell = _known_design(relevant, hard_type, rng)
    else:
        function, observed, hard_cell = _unknown_design(relevant, hard_type, rng, klass)
    world = function['table']
    records = []
    # r2: person names never coincide with attribute values.
    attribute_values = {v for vocab in FAMILY_VOCABULARY.values() for values in vocab['attributes'].values() for v in values}
    people = [name for name in PERSON_NAMES if name not in attribute_values]
    reviewers = rng.sample(people, 2)
    outsiders = [name for name in people if name not in reviewers]

    def add(kind, actor, context, event, timestamp):
        record = Record(record_id=_opaque(rng, 'record'), timestamp=timestamp, kind=kind, actor=actor,
                        context=context, observation=_json(event))
        records.append(record)
        return record.record_id

    registry = add('template', 'workflow-registry', {}, {
        'event': 'register_version', 'version': frame.version, 'workflow': frame.workflow,
        'task_family': frame.task_family, 'valid_from': '2026-01-01T00:00:00Z',
        'valid_until': '2027-01-01T00:00:00Z', 'authorised_reviewers': reviewers}, '2026-01-01T00:00:00Z')

    def review(cell, bit, actor, *, decision='accept', reviewed=None, comment=None, kind='review'):
        stamp = _timestamp(rng)
        facts = _facts(family, rng, stamp[:10])
        options = [baseline_values(frame, facts), alternative_values(frame, facts)]
        target = frame.field_option.field
        event = {'event': 'review', 'format': 'interpreted', 'document_id': facts['document_id'],
                 'authority_ref': registry, 'facts': facts,
                 'reviewed_fields': [target] if reviewed is None else reviewed, 'decision': decision,
                 'comment': comment or rng.choice(COMMENTS)}
        if decision == 'accept':
            event['accepted_fields'] = options[bit]
            event['change_summary'] = {'field': target, 'before': options[1 - bit].get(target),
                                       'after': options[bit].get(target)}
        return add(kind, actor, frame.context_of(cell), event, stamp)

    # r2: each listed reviewer approves both configurations (each occurs at least twice).
    approver = {}
    for bit in (0, 1):
        indices = [i for i, cell in enumerate(observed) if hclass.value(world, cell) == bit]
        start = rng.randrange(2)
        for k, i in enumerate(indices):
            approver[i] = reviewers[(start + k) % 2]
    for index, cell in enumerate(observed):
        review(cell, hclass.value(world, cell), approver[index])

    observed_set = set(observed)
    change_cells = sorted(c for c in observed_set if hclass.value(world, c))
    retention_cells = sorted(c for c in observed_set if not hclass.value(world, c))
    task_cells = {'observed_change': rng.choice(change_cells), 'observed_retention': rng.choice(retention_cells),
                  hard_type: hard_cell}

    quotas = DISTRACTOR_QUOTAS['small' if size == 'S' else 'large']
    required_bit = 1 if hard_type == 'transfer_change' else 0
    # r2: an existing non-target field of the artifact, not an invented one.
    other_field = next(name for name in frame.baseline_template if name != frame.field_option.field)
    counts = {}
    for record_type, count in quotas.items():
        for ordinal in range(count):
            # r2: in the exact context of the hard task, non-binding accepted reviews and
            # preferences show the configuration that is not warranted there; the rejected
            # version shows the warranted one. No misreading then reaches the warranted action.
            if ordinal == 0 and record_type != 'technical':
                cell = hard_cell
                bit = required_bit if record_type == 'rejected_artifact' else 1 - required_bit
            else:
                cell = rng.choice([c for c in range(64) if c != hard_cell])
                bit = rng.randrange(2)
            if record_type == 'unauthorised_revision':
                review(cell, bit, rng.choice(outsiders))
            elif record_type == 'approval_without_target':
                review(cell, bit, rng.choice(reviewers), reviewed=[other_field], comment=rng.choice(COMMENTS))
            elif record_type == 'rejected_artifact':
                stamp = _timestamp(rng)
                facts = _facts(family, rng, stamp[:10])
                fields = [baseline_values(frame, facts), alternative_values(frame, facts)][bit]
                add('review', rng.choice(reviewers), frame.context_of(cell), {
                    'event': 'review', 'format': 'interpreted', 'document_id': facts['document_id'],
                    'authority_ref': registry, 'facts': facts, 'reviewed_fields': [], 'decision': 'reject',
                    'rejected_fields': fields, 'rejection_grounds': 'The signature block is missing.',
                    'comment': rng.choice(COMMENTS)}, stamp)
            elif record_type == 'target_field_preference':
                stamp = _timestamp(rng)
                facts = _facts(family, rng, stamp[:10])
                fields = [baseline_values(frame, facts), alternative_values(frame, facts)][bit]
                target = frame.field_option.field
                wording = f'{target} should be {fields[target]!r}' if target in fields else f'{target} should be omitted'
                add('revision', 'work-item-author', frame.context_of(cell), {
                    'event': 'preference', 'facts': facts, 'proposed_fields': fields,
                    'message': f'My preference for this work item is that {wording}.'}, stamp)
            else:
                add('tool', 'runtime', frame.context_of(cell), {
                    'event': 'execution', 'request_id': _opaque(rng, 'request'),
                    'attempts': [{'attempt': 1, 'http_status': 503}, {'attempt': 2, 'http_status': 200}],
                    'log': 'The request completed on retry.'}, _timestamp(rng))
        counts[record_type] = count

    expected = 1 + BINDING_APPROVALS + sum(quotas.values())
    if len(records) != expected:
        raise ValueError(f'incorrect record quota: {len(records)} instead of {expected}')
    rng.shuffle(records)
    dictionary = {key: f'Configured output field {key}; preserve unless an applicable update is established.'
                  for key in frame.baseline_template}
    option = frame.field_option
    dictionary[option.field] = (f'Canonical field {option.field}. Available alternative operation {option.operation}, '
                                f'value={option.value!r}, separator={option.separator!r}. '
                                'Its requirement depends on the evidence.')
    dictionary.update({f'fact.{key}': value for key, value in frame.fact_descriptions.items()})
    history = History(history_id=_opaque(rng, 'history'), initial_configuration=frame.model_dump_json(),
                      assumptions=ASSUMPTIONS, field_dictionary=dictionary, records=records)

    oracle = infer(history)
    if not any(f.table == world for f in oracle.compatible):
        raise ValueError(f'generated world is incompatible with public evidence: seed={seed}')
    required = {'observed_change': 'apply', 'observed_retention': 'keep',
                'transfer_change': 'apply', 'unidentifiable': 'unresolved'}
    for task_type, cell in task_cells.items():
        if oracle.status(cell) != required[task_type]:
            raise ValueError(f'{task_type} not warranted by public evidence: seed={seed}')
    if hard_cell in oracle.observations:
        raise ValueError('the hard-task cell must be unobserved')
    references = heuristics.all_references(history, hard_cell)
    required = 'apply' if hard_type == 'transfer_change' else 'keep'
    shortcuts = ('nearest_neighbour', 'all_accepted_reviews', 'inverted_rejections', 'followed_preferences')
    reached = [name for name in shortcuts if references[name] == required]
    if reached:
        raise ValueError(f'hard task reachable by shortcut {reached}: seed={seed}')
    if hard_type == 'unidentifiable':
        share = sum(hclass.value(f, hard_cell) for f in oracle.compatible) / len(oracle.compatible)
        if share < 0.5:
            raise ValueError(f'unidentifiable probe changes under fewer than half of the functions: seed={seed}')
    return Case(case_id=_opaque(rng, 'case'), setting=setting, family=family, hard_type=hard_type,
                direction=direction, seed=seed, split=split, history=history,
                world={**function, 'table': str(world)}, task_cells=task_cells,
                oracle_audit={'observations': {str(k): v for k, v in oracle.observations.items()},
                              'binding_records': oracle.binding_records,
                              'compatible_count': len(oracle.compatible)},
                material_audit={'record_count': len(records), 'distractor_counts': counts,
                                'size': size, 'condition': condition, 'material_revision': 'v05-r2',
                                'hard_task_references': references})


def generate_histories(seed: int, split: str = 'development', settings=SETTINGS) -> list[Case]:
    if split not in ('development', 'review', 'final_test', 'test_fixture'):
        raise ValueError('unsupported material split')
    cases = []
    for setting in settings:
        for family in FAMILIES:
            case_seed = _seed('reflectai-v05-history', split, seed, setting, family)
            try:
                cases.append(make_case(case_seed, split, setting, family))
            except (ValueError, KeyError) as error:
                raise ValueError(f'material generation failed: setting={setting}, family={family}, '
                                 f'seed={case_seed}, split={split}: {error}') from error
    return cases


def generate_future_tasks(case: Case, seed: int) -> list[tuple[Task, TaskTruth]]:
    """Call only after preparations are sealed. Uses the public frame and the world."""
    rng = random.Random(_seed('reflectai-v05-future', case.split, case.seed, seed))
    oracle = infer(case.history)
    frame = oracle.frame
    world = int(case.world['table'])
    result = []
    plan = [(task_type, cell) for task_type, cell in case.task_cells.items()] + [('control', None)]
    for task_type, cell in plan:
        facts = _facts(case.family, rng, AS_OF[:10])
        base, alt = baseline_values(frame, facts), alternative_values(frame, facts)
        if cell is None:
            context = frame.context_of(rng.getrandbits(6))
            context['workflow'] = _opaque(rng, 'workflow')
            status, expected, world_fields = 'out_of_scope', base, base
        else:
            context = frame.context_of(cell)
            status = oracle.status(cell)
            expected = alt if status == 'apply' else base
            world_fields = alt if hclass.value(world, cell) else base
        task = Task(task_id=_opaque(rng, 'task'), context=context, facts=facts, baseline_fields=_fields(base),
                    request='Complete the current work item using the supplied facts and field dictionary. '
                            'Use only contextually supported adjustments. Retain all unaffected fields.')
        truth = TaskTruth(task_id=task.task_id, history_id=case.history.history_id, task_type=task_type, cell=cell,
                          expected_decision='apply' if status == 'apply' else 'keep', oracle_status=status,
                          expected_fields=expected, world_fields=world_fields)
        result.append((task, truth))
    return result
