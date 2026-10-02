"""Heuristic audit for v0.5 material r2 (no model calls); see analysis/heuristic_audit.py."""

from collections import Counter, defaultdict
import json

from .config import SEEDS
from .data import FAMILY_VOCABULARY, generate_histories
from .heuristics import all_references
from .oracle import configuration_bit, infer, read_frame

HEURISTICS = ('nearest_neighbour', 'compatible_majority', 'simplest_compatible', 'always_keep',
              'all_accepted_reviews', 'inverted_rejections', 'followed_preferences')


def audit(splits=('review', 'development')) -> dict:
    rows, reviewer_rows, collisions = [], [], []
    values = {v for vocab in FAMILY_VOCABULARY.values() for vs in vocab['attributes'].values() for v in vs}
    for split in splits:
        for case in generate_histories(SEEDS[split][0], split):
            cell = case.task_cells[case.hard_type]
            required = 'apply' if case.hard_type == 'transfer_change' else 'keep'
            references = all_references(case.history, cell)
            rows.append({'split': split, 'setting': case.setting, 'family': case.family, 'hard_type': case.hard_type,
                         'required': required, **{h: references[h] for h in HEURISTICS}})
            frame, oracle = read_frame(case.history), infer(case.history)
            records = {r.record_id: r for r in case.history.records}
            counts = Counter()
            for record_id in oracle.binding_records:
                record = records[record_id]
                event = json.loads(record.observation)
                counts[(record.actor, configuration_bit(frame, event['accepted_fields'], event['facts']))] += 1
            reviewers = sorted({actor for actor, _ in counts})
            reviewer_rows.append({'split': split, 'setting': case.setting, 'family': case.family,
                                  'counts': {f'{a}:{"alternative" if b else "baseline"}': n
                                             for (a, b), n in sorted(counts.items())},
                                  'each_reviewer_both': all(counts[(a, 0)] and counts[(a, 1)] for a in reviewers)})
            actors = {r.actor for r in case.history.records}
            clash = sorted(actors & values)
            if clash:
                collisions.append({'split': split, 'setting': case.setting, 'family': case.family, 'names': clash})
    shares = defaultdict(dict)
    for (setting, hard_type), group in _group(rows).items():
        for h in HEURISTICS:
            hits = sum(r[h] == r['required'] for r in group)
            shares[f'{setting} {hard_type}'][h] = f'{hits}/{len(group)}'
    return {'rows': rows, 'shares': dict(shares), 'reviewers': reviewer_rows, 'name_collisions': collisions}


def _group(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[(row['setting'], row['hard_type'])].append(row)
    return dict(sorted(groups.items()))


def markdown(result: dict) -> str:
    lines = ['# v0.5 heuristic audit (material r2)', '',
             'Share of hard tasks where a shortcut gives the warranted action. Review and development seeds; '
             'no model calls. Shortcuts that must never succeed by construction: nearest_neighbour, '
             'all_accepted_reviews, inverted_rejections, followed_preferences. The others are reference lines.', '',
             '| Setting and hard type | ' + ' | '.join(HEURISTICS) + ' |', '| --- |' + ' ---: |' * len(HEURISTICS)]
    for key, shares in result['shares'].items():
        lines.append(f'| {key} | ' + ' | '.join(shares[h] for h in HEURISTICS) + ' |')
    both = sum(r['each_reviewer_both'] for r in result['reviewers'])
    lines += ['', f"Each listed reviewer approves both configurations in {both} of {len(result['reviewers'])} histories.",
              f"Name collisions between people and attribute values: {len(result['name_collisions'])}."]
    return '\n'.join(lines) + '\n'
