"""Heuristic audit for v0.5 material (no model calls); see analysis/heuristic_audit.py.

Over all 32 histories of the review and development seeds:
* hard tasks: nearest neighbour, compatible majority, simplest compatible function,
  always-keep, and four misreadings, each misreading with three readings: the oracle
  reading ('undefined' on contradiction, counted separately), fallback (a) and (b);
* distractor agreement with the world per record type, history size and location
  (exact hard-task context, relevant cell of the probe, rest);
* nearest rejection versus nearest binding approval (distance to the hard task);
* reviewer x configuration counts and name collisions.
"""

from collections import Counter, defaultdict
import json

from . import hclass
from .config import SEEDS
from .data import FAMILY_VOCABULARY, generate_histories
from .heuristics import MISREADINGS, all_references
from .oracle import configuration_bit, infer, read_frame

REFERENCES = ('nearest_neighbour', 'compatible_majority', 'simplest_compatible', 'always_keep')
TYPES = {'unauthorised_revision': 'review outside roster', 'approval_without_target': 'approval without target',
         'target_field_preference': 'preference', 'rejected_artifact': 'rejected version'}


def _distractor_type(record, event, roster, target):
    kind = event.get('event')
    if kind == 'preference':
        return 'target_field_preference'
    if kind == 'review' and event.get('decision') == 'reject':
        return 'rejected_artifact'
    if kind == 'review' and event.get('decision') == 'accept':
        if record.actor not in roster:
            return 'unauthorised_revision'
        if target not in event.get('reviewed_fields', []):
            return 'approval_without_target'
    return None


def _fields_of(event):
    return event.get('accepted_fields') or event.get('rejected_fields') or event.get('proposed_fields')


def audit(splits=('review', 'development')) -> dict:
    rows, reviewer_rows, collisions, agreement, distances = [], [], [], Counter(), []
    values = {v for vocab in FAMILY_VOCABULARY.values() for vs in vocab['attributes'].values() for v in vs}
    constructed = 0
    for split in splits:
        for case in generate_histories(SEEDS[split][0], split):
            constructed += 1
            cell = case.task_cells[case.hard_type]
            required = 'apply' if case.hard_type == 'transfer_change' else 'keep'
            references = all_references(case.history, cell)
            rows.append({'split': split, 'setting': case.setting, 'family': case.family,
                         'hard_type': case.hard_type, 'required': required, **references})
            frame, oracle = read_frame(case.history), infer(case.history)
            world, relevant = int(case.world['table']), case.world['relevant']
            roster = next(json.loads(r.observation)['authorised_reviewers'] for r in case.history.records
                          if json.loads(r.observation).get('event') == 'register_version')
            binding, approvals = set(oracle.binding_records), Counter()
            nearest = {'binding': 99, 'rejected': 99}
            for record in case.history.records:
                event = json.loads(record.observation)
                if event.get('event') == 'register_version':
                    continue
                try:
                    record_cell = frame.cell_of(record.context)
                except KeyError:
                    continue
                distance = bin(record_cell ^ cell).count('1')
                if record.record_id in binding:
                    approvals[(record.actor, configuration_bit(frame, event['accepted_fields'], event['facts']))] += 1
                    nearest['binding'] = min(nearest['binding'], distance)
                    continue
                kind = _distractor_type(record, event, roster, frame.field_option.field)
                if kind is None:
                    continue
                bit = configuration_bit(frame, _fields_of(event), event['facts'])
                location = ('exact' if record_cell == cell else 'relevant'
                            if all(hclass.bit(record_cell, i) == hclass.bit(cell, i) for i in relevant) else 'rest')
                size = 'small' if case.setting.endswith('S') else 'large'
                agree = 'world' if bit == hclass.value(world, record_cell) else 'counter'
                agreement[(TYPES[kind], size, location, agree)] += 1
                if kind == 'rejected_artifact':
                    nearest['rejected'] = min(nearest['rejected'], distance)
            distances.append({'split': split, 'setting': case.setting, 'family': case.family, **nearest,
                              'rejection_farther': nearest['rejected'] > nearest['binding']})
            reviewers = sorted({a for a, _ in approvals})
            reviewer_rows.append({'split': split, 'setting': case.setting, 'family': case.family,
                                  'each_reviewer_both': all(approvals[(a, 0)] and approvals[(a, 1)] for a in reviewers)})
            clash = sorted({r.actor for r in case.history.records} & values)
            if clash:
                collisions.append({'split': split, 'setting': case.setting, 'family': case.family, 'names': clash})
    return {'constructed_histories': constructed, 'rows': rows, 'shares': _shares(rows),
            'distractor_agreement': {'|'.join(k): v for k, v in sorted(agreement.items())},
            'rejection_distances': distances, 'reviewers': reviewer_rows, 'name_collisions': collisions}


def _shares(rows) -> dict:
    groups = defaultdict(list)
    for row in rows:
        groups[f"{row['setting']} {row['hard_type']}"].append(row)
    shares = {}
    for key, group in sorted(groups.items()):
        entry = {h: f"{sum(r[h] == r['required'] for r in group)}/{len(group)}" for h in REFERENCES}
        for name in MISREADINGS:
            hits = sum(r[name] == r['required'] for r in group)
            undefined = sum(r[name] == 'undefined' for r in group)
            entry[name] = f'{hits}/{len(group)} (undefined {undefined})'
            for rule in ('a', 'b'):
                entry[f'{name}|{rule}'] = f"{sum(r[f'{name}|{rule}'] == r['required'] for r in group)}/{len(group)}"
        shares[key] = entry
    return shares


def markdown(result: dict) -> str:
    lines = ['# v0.5 heuristic audit (material r3)', '',
             f"Histories constructed from the review and development seeds: {result['constructed_histories']} "
             '(generation stops on any failed condition). No model calls.', '',
             'Each cell gives how often a shortcut reaches the warranted action at the hard task. Shortcuts that '
             'must never succeed by construction: nearest neighbour and every misreading under fallback (b).', '',
             '## Reference lines', '', '| Setting and hard type | ' + ' | '.join(REFERENCES) + ' |',
             '| --- |' + ' ---: |' * len(REFERENCES)]
    for key, entry in result['shares'].items():
        lines.append(f'| {key} | ' + ' | '.join(entry[h] for h in REFERENCES) + ' |')
    lines += ['', '## Misreadings', '',
              'Oracle reading: the misread evidence fed to the oracle; a contradiction is "undefined" and is not a '
              'success. Fallback (a): a contradiction means keep, so unidentifiable tasks are structurally always '
              'right under (a), like always-keep. Fallback (b): majority of the misread evidence in the exact context, '
              'otherwise the nearest neighbour over binding plus misread evidence.', '']
    for name in MISREADINGS:
        lines += [f'### {name}', '', '| Setting and hard type | oracle reading | fallback (a) | fallback (b) |',
                  '| --- | ---: | ---: | ---: |']
        for key, entry in result['shares'].items():
            lines.append(f"| {key} | {entry[name]} | {entry[name + '|a']} | {entry[name + '|b']} |")
        lines.append('')
    lines += ['## Distractor agreement with the world', '',
              '| Type | Size | Location | World | Counter |', '| --- | --- | --- | ---: | ---: |']
    table = defaultdict(lambda: {'world': 0, 'counter': 0})
    for key, count in result['distractor_agreement'].items():
        kind, size, location, agree = key.split('|')
        table[(kind, size, location)][agree] = count
    for (kind, size, location), counts in sorted(table.items()):
        lines.append(f"| {kind} | {size} | {location} | {counts['world']} | {counts['counter']} |")
    farther = sum(d['rejection_farther'] for d in result['rejection_distances'])
    both = sum(r['each_reviewer_both'] for r in result['reviewers'])
    lines += ['', f"Nearest rejected version farther from the hard task than the nearest binding approval: "
              f"{farther} of {len(result['rejection_distances'])} histories.",
              f"Each listed reviewer approves both configurations in {both} of {len(result['reviewers'])} histories.",
              f"Name collisions between people and attribute values: {len(result['name_collisions'])}."]
    return '\n'.join(lines) + '\n'
