"""Post-run analysis of the sealed v0.5 main run; offline, no model calls.

Reads only the sealed run folder, verifies its seal first and writes
`pilots/v05/analysis/main-analysis.json`. Covers the primary outcome by setting, arm
and task type, the prespecified expectations E1-E4, error types, B's retrieval
coverage, D's register accuracy and query yield, and the heuristic references on the
main-run material (protocol, Measurement and Prespecified expectations).

Usage: python -B pilots/v05/analysis/main_analysis.py [run folder]
"""

from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
for folder in (ROOT / 'src', ROOT / 'pilots/v03', ROOT / 'pilots/v04', ROOT / 'pilots/v05'):
    sys.path.insert(0, str(folder))

from reflectai_v03.contracts import History  # noqa: E402
from reflectai_v05 import hclass  # noqa: E402
from reflectai_v05.heuristics import all_references  # noqa: E402
from reflectai_v05.oracle import infer, read_frame  # noqa: E402
from reflectai_v05.storage import verify_seal  # noqa: E402

RUN = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'pilots/v05/runs/live-main-20261003'
OUT = ROOT / 'pilots/v05/analysis/main-analysis.json'
SETTINGS = ('K-S', 'K-L', 'U-S', 'U-L')
ARMS = ('A', 'B', 'C', 'D')
TYPES = ('observed_change', 'observed_retention', 'transfer_change', 'unidentifiable', 'control')
HARD = ('transfer_change', 'unidentifiable')
OBSERVED = ('observed_change', 'observed_retention')
RECORD_ID = re.compile(r'record-[0-9a-f]{12}')


def load(name):
    return json.loads((RUN / name).read_text(encoding='utf-8'))


def payload(request_path: Path) -> dict:
    prompt = json.loads(request_path.read_text(encoding='utf-8'))['prompt']
    return json.loads(prompt.split('\nPAYLOAD\n', 1)[1])


def correct_count(rows, setting, arm, types):
    selected = [r for r in rows if r['setting'] == setting and r['arm'] == arm and r['task_type'] in types]
    return sum(bool(r['correct']) for r in selected), len(selected)


def better_of_b_c(rows, setting, types):
    b, n = correct_count(rows, setting, 'B', types)
    c, _ = correct_count(rows, setting, 'C', types)
    return max(b, c), n, ('B' if b > c else 'C' if c > b else 'B=C')


def hypothesis_table(hypothesis: dict, frame) -> int | None:
    names, n = frame.attribute_names, len(frame.attributes)
    full = (1 << hclass.n_cells(n)) - 1
    if hypothesis['form'] == 'always_baseline':
        return 0
    if hypothesis['form'] == 'always_alternative':
        return full
    tables = []
    for literal in hypothesis['literals']:
        if literal['attribute'] not in frame.attributes or literal['value'] not in frame.attributes[literal['attribute']]:
            return None
        index = names.index(literal['attribute'])
        tables.append(hclass.literal_table(n, index, frame.attributes[literal['attribute']].index(literal['value']) == 1))
    if hypothesis['form'] == 'literal' and len(tables) == 1:
        return tables[0]
    if hypothesis['form'] in ('and', 'or') and len(tables) == 2:
        return tables[0] & tables[1] if hypothesis['form'] == 'and' else tables[0] | tables[1]
    return None


def main() -> dict:
    seal = verify_seal(RUN, RUN / 'manifest.json')['sha256']
    results = load('results.json')
    rows, summary = results['rows'], results['summary']
    cases = {c['history']['history_id']: c for c in load('evaluator/cases.json')}
    tasks = {h: {p['task']['task_id']: p for p in pairs} for h, pairs in load('evaluator/future-tasks.json').items()}
    calls = load('calls.json')
    calls = calls if isinstance(calls, list) else calls['calls']
    registers = load('preparation/registers.json')
    prep_logs = summary['preparation_logs']
    out = {'run': RUN.relative_to(ROOT).as_posix(), 'seal': seal, 'budget': summary['budget']}

    # Primary outcome, fixed denominators (blocked and failed calls count as incorrect).
    out['primary'] = {s: {a: {t: '%d/%d' % correct_count(rows, s, a, (t,)) for t in TYPES} for a in ARMS}
                      for s in SETTINGS}
    out['primary_totals'] = {a: {t: '%d/%d' % (sum(correct_count(rows, s, a, (t,))[0] for s in SETTINGS),
                                               sum(correct_count(rows, s, a, (t,))[1] for s in SETTINGS))
                                 for t in TYPES} for a in ARMS}
    out['by_group'] = {s: {a: {'observed': '%d/%d' % correct_count(rows, s, a, OBSERVED),
                               'hard': '%d/%d' % correct_count(rows, s, a, HARD),
                               'diagnostics': '%d/%d' % correct_count(rows, s, a, OBSERVED + HARD),
                               'control': '%d/%d' % correct_count(rows, s, a, ('control',))}
                           for a in ARMS} for s in SETTINGS}
    out['hard_by_direction'] = {}
    for a in ARMS:
        for direction in ('omit', 'add'):
            sel = [r for r in rows if r['arm'] == a and r['task_type'] in HARD and r['direction'] == direction]
            out['hard_by_direction'][f'{a}|{direction}'] = '%d/%d' % (sum(bool(r['correct']) for r in sel), len(sel))

    # E1 selection and E2 dimension uncertainty: better of B and C over the 12 diagnostics.
    diag = OBSERVED + HARD
    best = {s: better_of_b_c(rows, s, diag) for s in SETTINGS}
    best_hard = {s: better_of_b_c(rows, s, HARD) for s in SETTINGS}
    out['better_of_B_C'] = {s: {'diagnostics': '%d/%d' % best[s][:2], 'arm': best[s][2],
                                'hard': '%d/%d' % best_hard[s][:2], 'hard_arm': best_hard[s][2]} for s in SETTINGS}
    out['E1'] = {f'{k}-L vs {k}-S': {'large': best[f'{k}-L'][0], 'small': best[f'{k}-S'][0],
                                     'holds': best[f'{k}-L'][0] < best[f'{k}-S'][0]} for k in ('K', 'U')}
    out['E2'] = {f'U-{z} vs K-{z}': {'unknown': best[f'U-{z}'][0], 'known': best[f'K-{z}'][0],
                                     'unknown_hard': best_hard[f'U-{z}'][0], 'known_hard': best_hard[f'K-{z}'][0],
                                     'holds': best[f'U-{z}'][0] < best[f'K-{z}'][0]} for z in ('S', 'L')}
    out['E3'] = {}
    for s in SETTINGS:
        d = correct_count(rows, s, 'D', diag)[0]
        out['E3'][s] = {'D': d, 'better_of_B_C': best[s][0], 'difference': d - best[s][0],
                        'holds': d - best[s][0] >= 2,
                        'D_hard': correct_count(rows, s, 'D', HARD)[0], 'best_hard': best_hard[s][0],
                        'D_observed': correct_count(rows, s, 'D', OBSERVED)[0],
                        'best_observed': better_of_b_c(rows, s, OBSERVED)[0]}

    # Tokens per task over the four tasks of each history, including preparation (E4).
    per_history = defaultdict(int)
    for call in calls:
        usage = call.get('usage') or {}
        tokens = (usage.get('input_tokens') or 0) + (usage.get('output_tokens') or 0)
        per_history[(call['history_id'], call['arm'])] += tokens
    tokens = {s: {} for s in SETTINGS}
    for s in SETTINGS:
        hids = [h for h, c in cases.items() if c['setting'] == s]
        for a in ARMS:
            tokens[s][a] = round(sum(per_history[(h, a)] for h in hids) / (4 * len(hids)))
    out['tokens_per_task'] = tokens
    out['E4'] = {}
    for s in SETTINGS:
        d = correct_count(rows, s, 'D', diag)[0]
        arm = best[s][2] if best[s][2] in ('B', 'C') else min(('B', 'C'), key=lambda x: tokens[s][x])
        applies = d >= best[s][0]
        out['E4'][s] = {'D_at_least_as_accurate': applies, 'reference_arm': arm,
                        'D_tokens_per_task': tokens[s]['D'], 'reference_tokens_per_task': tokens[s][arm],
                        'ratio': round(tokens[s]['D'] / tokens[s][arm], 2),
                        'holds': (tokens[s]['D'] <= 0.7 * tokens[s][arm]) if applies else None}

    # Error types (v0.4 taxonomy where it applies) and a history-level polarity tag.
    errors = Counter()
    for r in rows:
        if r['correct']:
            continue
        reason = r['blocked_reason'] or r['reason'] or 'failed_call'
        if r['task_type'] == 'transfer_change' and reason == 'missed_change':
            reason = 'missed_transfer'
        errors[f"{r['arm']}|{r['task_type']}|{reason}"] += 1
    out['errors'] = dict(sorted(errors.items()))
    polarity = []
    by_history = defaultdict(dict)
    for r in rows:
        by_history[(r['history_id'], r['arm'])][r['task_type']] = r
    for (hid, arm), types in sorted(by_history.items()):
        change, keep = types.get('observed_change'), types.get('observed_retention')
        if change and keep and change['implied_decision'] == 'keep' and keep['implied_decision'] == 'apply':
            polarity.append({'history_id': hid, 'arm': arm, 'setting': cases[hid]['setting'],
                             'direction': cases[hid]['direction']})
    out['baseline_polarity_inversion_candidates'] = polarity

    # Failures in detail for the attribution review.
    detail = []
    for r in rows:
        if r['correct']:
            continue
        truth = tasks[r['history_id']][r['task_id']]['truth']
        detail.append({k: r.get(k) for k in ('setting', 'family', 'direction', 'history_id', 'arm', 'task_type',
                                            'task_id', 'call_status', 'blocked_reason', 'reason',
                                            'implied_decision', 'declared_decision')}
                      | {'expected_decision': truth['expected_decision'], 'oracle_status': truth['oracle_status']})
    out['failures'] = detail

    # B retrieval coverage of binding approvals (large histories), read from B's requests.
    coverage = []
    oracles = {h: infer(History.model_validate(c['history'])) for h, c in cases.items()}
    for r in rows:
        if r['arm'] != 'B' or not r['setting'].endswith('L') or r['task_type'] == 'control':
            continue
        request = RUN / 'generation' / f"{r['history_id']}-{r['task_type']}-B" / 'request.json'
        if not request.is_file():
            continue
        ids = set(RECORD_ID.findall(json.dumps(payload(request)['history_excerpt'])))
        binding = oracles[r['history_id']].binding_records
        coverage.append({'setting': r['setting'], 'task_type': r['task_type'], 'correct': r['correct'],
                         'binding_included': sum(b in ids for b in binding), 'binding_total': len(binding)})
    out['B_retrieval_coverage'] = {
        'tasks': len(coverage),
        'all_binding_included': sum(c['binding_included'] == c['binding_total'] for c in coverage),
        'mean_share': round(sum(c['binding_included'] / c['binding_total'] for c in coverage) / len(coverage), 3),
        'rows': coverage}

    # D: rounds, queries, binding records returned by queries, register vs oracle compatible set.
    dstats = []
    for hid, case in cases.items():
        log = prep_logs.get(f'{hid}|D', {})
        oracle, frame = oracles[hid], read_frame(History.model_validate(case['history']))
        compatible = {f.table for f in oracle.compatible}
        world = int(case['world']['table'])
        found = set()
        for request in sorted((RUN / 'preparation' / hid / 'D').glob('D-round-*/request.json')):
            for result in payload(request).get('results', []):
                found |= {rec['record_id'] for rec in result.get('records', [])}
        register = registers.get(hid)
        entry = {'history_id': hid, 'setting': case['setting'], 'hard_type': case['hard_type'],
                 'rounds': log.get('rounds'), 'queries': log.get('queries'), 'early_stop': log.get('early_stop'),
                 'failure': log.get('failure'), 'omitted_for_budget': log.get('omitted_for_budget'),
                 'binding_total': len(oracle.binding_records),
                 'binding_returned_by_queries': len(found & set(oracle.binding_records)),
                 'compatible_size': len(compatible)}
        if register:
            kept = [h for h in register['hypotheses'] if h['status'] in ('open', 'supported')]
            kept_tables = {t for t in (hypothesis_table(h, frame) for h in kept) if t is not None}
            listed = {t for t in (hypothesis_table(h, frame) for h in register['hypotheses']) if t is not None}
            entry |= {'hypotheses': len(register['hypotheses']), 'kept': len(kept),
                      'all_eliminated': not kept,
                      'kept_compatible': len(kept_tables & compatible),
                      'kept_incompatible': len(kept_tables - compatible),
                      'compatible_listed': len(listed & compatible),
                      'compatible_wrongly_eliminated': len((listed & compatible) - kept_tables),
                      'world_listed': world in listed, 'world_kept': world in kept_tables}
            # Attribution review, part 1: which literal values D used, the form counts, the
            # world function's polarity type and the share of binding records among citations.
            used = defaultdict(set)
            for h in register['hypotheses']:
                for literal in h['literals']:
                    values = frame.attributes.get(literal['attribute'], [])
                    if literal['value'] in values:
                        used[literal['attribute']].add(values.index(literal['value']))
            entry['literal_values_by_attribute'] = {
                name: {frozenset({1}): 'second', frozenset({0}): 'first'}.get(frozenset(v), 'both')
                for name, v in sorted(used.items())}
            entry['literal_value_use'] = ('none' if not used else 'second_only' if all(v == {1} for v in used.values())
                                          else 'first_only' if all(v == {0} for v in used.values()) else 'both')
            entry['forms'] = dict(Counter(h['form'] for h in register['hypotheses']))
            cited = [i for h in register['hypotheses'] for i in h['evidence_ids'] + h['counterevidence_ids']]
            entry['cited_records'] = len(cited)
            entry['cited_binding'] = sum(i in set(oracle.binding_records) for i in cited)
        klass = hclass.rule_class(len(frame.attributes), frame.candidate_indices())
        function = next(f for f in klass if f.table == world)
        signs = {positive for _, positive in function.literals}
        entry['world_polarity'] = ('constant' if not signs else 'second_only' if signs == {True}
                                   else 'first_only' if signs == {False} else 'mixed')
        full = (1 << hclass.n_cells(len(frame.attributes))) - 1
        entry['complement_listed'] = bool(register) and (full ^ world) in listed
        dstats.append(entry)
    out['D'] = dstats
    out['D_summary'] = {
        'literal_value_use': dict(Counter(d.get('literal_value_use') for d in dstats)),
        'hypotheses_per_register': {s: [d.get('hypotheses') for d in dstats if d['setting'] == s] for s in SETTINGS},
        'world_polarity_vs_listing': dict(Counter(
            f"{d['world_polarity']}|world_listed={d.get('world_listed')}|complement_listed={d['complement_listed']}"
            for d in dstats)),
        'cited_binding': '%d/%d' % (sum(d.get('cited_binding', 0) for d in dstats),
                                    sum(d.get('cited_records', 0) for d in dstats)),
        'register_collapsed': sum(bool(d.get('all_eliminated')) for d in dstats)}

    # Scope of adopted rules: does the retained guidance carry the declared workflow?
    retained = load('preparation/retained.json')
    scope = Counter()
    for key, prep in retained.items():
        for candidate in (prep or {}).get('candidates', []):
            if candidate['status'] == 'adopt' and candidate.get('rule'):
                match = candidate['rule'].get('scope', {}).get('match', {})
                scope[f"{key.split('|')[1]}|workflow_in_scope={'workflow' in match}"] += 1
    out['adopted_rule_scope'] = dict(sorted(scope.items()))

    # Heuristic references on the main-run material (hard tasks only).
    heuristics = []
    for hid, case in cases.items():
        cell = case['task_cells'][case['hard_type']]
        required = 'apply' if case['hard_type'] == 'transfer_change' else 'keep'
        refs = all_references(History.model_validate(case['history']), cell)
        heuristics.append({'setting': case['setting'], 'hard_type': case['hard_type'], 'required': required,
                           **refs})
    out['heuristics_hard'] = heuristics

    # Attribution review part 2: the hard tasks under the reading "a literal tests only the
    # second listed value" (D's reading), against the B and C results.
    reading = []
    for hid, case in cases.items():
        oracle, frame = oracles[hid], read_frame(History.model_validate(case['history']))
        klass = hclass.rule_class(len(frame.attributes), frame.candidate_indices())
        positive = [f for f in klass if all(p for _, p in f.literals)]
        fits = hclass.compatible(positive, oracle.observations)
        cell = case['task_cells'][case['hard_type']]
        status = hclass.status_at(fits, cell) if fits else 'no_function_fits'
        result = {a: next(bool(r['correct']) for r in rows if r['history_id'] == hid and r['arm'] == a
                          and r['task_type'] == case['hard_type']) for a in ('B', 'C')}
        blocked = {a: next(r['blocked_reason'] for r in rows if r['history_id'] == hid and r['arm'] == a
                           and r['task_type'] == case['hard_type']) for a in ('B', 'C')}
        reading.append({'history_id': hid, 'setting': case['setting'], 'hard_type': case['hard_type'],
                        'direction': case['direction'],
                        'required': 'apply' if case['hard_type'] == 'transfer_change' else 'keep',
                        'second_only_fitting': len(fits), 'second_only_status': status,
                        'B_correct': result['B'], 'C_correct': result['C'],
                        'C_blocked': blocked['C']})
    out['second_value_reading_hard'] = reading
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + chr(10), encoding='utf-8', newline=chr(10))
    return out


if __name__ == '__main__':
    result = main()
    print(json.dumps({k: result[k] for k in ('seal', 'better_of_B_C', 'E1', 'E2', 'E3', 'E4', 'tokens_per_task',
                                             'hard_by_direction', 'baseline_polarity_inversion_candidates')},
                     indent=1))
