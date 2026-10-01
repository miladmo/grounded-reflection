"""Deterministic evaluation and descriptive reporting after generation."""

from collections import defaultdict
import json
from pathlib import Path
import random

from .contracts import ARMS, FamilyTruth, Preparation, RunConfig, TaskTruth, WorkOutput
from .evaluation import score_preparation, score_task
from .storage import file_hash, read_json, write_json


def evaluate_stage(repo, run, tasks, phase):
    from .runner import records
    run = Path(run)
    cfg = RunConfig.model_validate(read_json(run / 'setup.json')['config'])
    gold_path = (run / 'heldout/ground_truth.json' if phase == 'final_test' else
                 Path(repo) / 'pilots/v02/data/ground_truth' / (phase + '.json'))
    truths = [TaskTruth.model_validate(x) for x in read_json(gold_path)]
    if len({t.case_id for t in truths}) != len(truths) or {t.case_id for t in truths} != {t.case_id for t in tasks}:
        raise ValueError('Gold case IDs must exactly match this evaluation stage')
    gold = {t.case_id: t for t in truths}
    saved = {r.call_id: r for r in records(run)}
    arms = ('no_adaptation',) if phase == 'calibration' else ARMS
    scores = []
    for repetition in range(cfg.repetitions):
        for task in tasks:
            for arm in arms:
                call_id = f'{phase}-r{repetition}-{task.case_id}-{arm}'
                record = saved.get(call_id)
                output = None
                if record and record.status == 'completed':
                    try:
                        output = WorkOutput.model_validate(record.response)
                    except ValueError:
                        pass
                score = score_task(task, gold[task.case_id], output)
                score.update(arm=arm, repetition=repetition, call_id=call_id,
                             call_status=record.status if record else 'missing')
                scores.append(score)
    return scores


def ratio(n, d):
    return n / d if d else None


def aggregate(scores):
    summary = {}
    for arm in ARMS:
        rows = [s for s in scores if s['arm'] == arm]
        if not rows:
            continue
        by_kind = {}
        for kind in ('hidden', 'explicit', 'generic'):
            passed = sum(s['by_kind'][kind]['passed'] for s in rows)
            total = sum(s['by_kind'][kind]['total'] for s in rows)
            by_kind[kind] = {'passed': passed, 'total': total, 'rate': ratio(passed, total)}
        by_family = {}
        for family in sorted({s['family'] for s in rows}):
            group = [s for s in rows if s['family'] == family]
            p, n = sum(s['passed_checks'] for s in group), sum(s['evaluated_checks'] for s in group)
            by_family[family] = {'passed': p, 'total': n, 'compliance': ratio(p, n),
                                 'task_passed': sum(s['task_passed'] for s in group), 'tasks': len(group)}
        boundary = [s for s in rows if s['category'] == 'boundary']
        by_category = {}
        for category in sorted({s['category'] for s in rows}):
            group = [s for s in rows if s['category'] == category]
            p, n = sum(s['passed_checks'] for s in group), sum(s['evaluated_checks'] for s in group)
            by_category[category] = {'passed': p, 'total': n, 'compliance': ratio(p, n),
                                     'task_passed': sum(s['task_passed'] for s in group), 'tasks': len(group),
                                     'abstentions': sum(s['unnecessary_abstention'] for s in group)}
        summary[arm] = {
            'attempts': len(rows), 'failed_calls': sum(s['call_status'] != 'completed' for s in rows),
            'invalid_outputs': sum(not s['output_valid'] for s in rows),
            'compliance': ratio(sum(s['passed_checks'] for s in rows), sum(s['evaluated_checks'] for s in rows)),
            'task_passed': sum(s['task_passed'] for s in rows),
            'task_success_rate': ratio(sum(s['task_passed'] for s in rows), len(rows)),
            'all_requirements_passed': sum(s['all_requirements_passed'] is True for s in rows),
            'delivered': sum(s['delivered'] for s in rows), 'completed': sum(s['completed'] for s in rows),
            'unnecessary_abstention': sum(s['unnecessary_abstention'] for s in rows),
            'missed_required_abstention': sum(s['missed_required_abstention'] for s in rows),
            'unsafe_guesses': sum(s.get('unsafe_guess', False) for s in rows),
            'appropriate_actions': sum(s['action_appropriate'] for s in rows),
            'distractor_adoptions': sum(s['distractor_adoptions'] or 0 for s in rows),
            'distractor_checks_evaluated': sum(s['distractor_checks_evaluated'] for s in rows),
            'boundary_success_rate': ratio(sum(s['task_passed'] for s in boundary), len(boundary)),
            'by_kind': by_kind, 'by_family': by_family, 'by_category': by_category,
        }
    return summary


def paired(scores):
    index = {(s['repetition'], s['case_id'], s['arm']): s for s in scores}
    comparisons = []
    for (rep, case, arm), row in index.items():
        if arm != 'grounded_reflection':
            continue
        for comparator in ('direct_adaptation', 'direct_evidence', 'no_adaptation'):
            baseline = index[(rep, case, comparator)]
            comparable = [(a, b) for a, b in zip(row['checks'], baseline['checks'])
                          if a['passed'] is not None and b['passed'] is not None]
            comparisons.append({
                'repetition': rep, 'case_id': case, 'family': row['family'], 'category': row['category'],
                'comparison': 'grounded_reflection_minus_' + comparator,
                'task_success_difference': int(row['task_passed']) - int(baseline['task_passed']),
                'check_difference': (sum(int(a['passed']) - int(b['passed']) for a, b in comparable)
                                     / len(comparable)) if comparable else None,
                'regressed_checks': sum(b['passed'] and not a['passed'] for a, b in comparable),
                'comparable_checks': len(comparable),
            })
    return comparisons


def inference_scores(repo, run):
    truths = {t.family: t for t in map(FamilyTruth.model_validate,
               read_json(Path(repo) / 'pilots/v02/data/ground_truth/families.json'))}
    cfg = RunConfig.model_validate(read_json(Path(run) / 'setup.json')['config'])
    scores = []
    for rep in range(cfg.repetitions):
        for family in truths:
            for arm in ('direct_adaptation', 'grounded_reflection'):
                artifact = read_json(Path(run) / 'prepared' / f'r{rep}-{family}-{arm}.json')
                for stage in ('raw', 'retained'):
                    prep = artifact[stage]
                    result = score_preparation(Preparation.model_validate(prep), truths[family]) if prep else None
                    scores.append({'arm': arm, 'family': family, 'repetition': rep, 'stage': stage,
                                   'status': artifact['status'], 'scores': result,
                                   'rejected_predictions': artifact['rejected']})
    return scores


def resource_rows(records):
    groups = defaultdict(list)
    for record in records:
        groups[(record.arm, record.phase)].append(record)
    rows = []
    for (arm, phase), group in sorted(groups.items()):
        values = {}
        for field in ('input_tokens', 'output_tokens', 'cached_input_tokens', 'reasoning_output_tokens'):
            counts = [getattr(r.usage, field) for r in group]
            values[field] = sum(counts) if all(x is not None for x in counts) else None
        rows.append({'arm': arm, 'phase': phase, 'calls': len(group),
                     'failed_calls': sum(r.status == 'failed' for r in group), **values,
                     'currency_cost': None, 'human_review_seconds': None})
    return rows


def human_sample(repo, run, tasks, scores, records, seed):
    rng = random.Random(seed)
    task_lookup = {t.case_id: t for t in tasks}
    record_lookup = {r.call_id: r for r in records}
    groups = defaultdict(list)
    for row in scores:
        groups[(row['family'], row['arm'])].append(row)
    selected = [rng.choice(group) for _, group in sorted(groups.items())]
    rng.shuffle(selected)
    sample, mapping = [], []
    for i, row in enumerate(selected, 1):
        sample_id = f'review-{i:02d}'
        record = record_lookup.get(row['call_id'])
        sample.append({'sample_id': sample_id,
                       'task': task_lookup[row['case_id']].public_payload(),
                       'output': record.response if record else None,
                       'human_assessment': None})
        mapping.append({'sample_id': sample_id, 'arm': row['arm'], 'repetition': row['repetition'],
                        'call_id': row['call_id'], 'automated_checks': row})
    write_json(Path(run) / 'human-review.json', {'status': 'not_reviewed',
               'origin': read_json(Path(run) / 'setup.json')['origin'],
               'instructions': 'Review decisions against the task and shared historical evidence. '
                               'Record plausible alternative interpretations and any disagreement with the task design. '
                               'Do not open the separate arm and automated-score key before reviewing.',
               'histories': read_json(Path(repo) / 'pilots/v02/data/histories.json'), 'samples': sample})
    write_json(Path(run) / 'human-review-key.json', mapping)


def report(repo, run):
    from .runner import existing, load_tasks, records, verify_freeze
    run, cfg, setup = existing(repo, run)
    verify_freeze(repo, run)
    if not (run / 'final.json').exists():
        raise ValueError('Final generation has not completed; preserve failures and diagnose before a new run')
    final_status = read_json(run / 'final.json')
    output_files = {p.relative_to(run).as_posix(): file_hash(p)
                    for call in (run / 'calls').glob('final_test-*')
                    for p in sorted(call.rglob('*')) if p.is_file()}
    if output_files != final_status['output_files']:
        raise ValueError('Final model outputs or call records changed')
    manifest = read_json(run / 'heldout/manifest.json')
    if (file_hash(run / 'heldout/tasks.json') != manifest['tasks_sha256'] or
            file_hash(run / 'heldout/ground_truth.json') != manifest['truth_sha256'] or
            file_hash(run / 'freeze.json') != manifest['generated_after_freeze']):
        raise ValueError('Final tasks, truth or freeze record changed')
    tasks = load_tasks(run / 'heldout/tasks.json', 'final_test')
    scores = evaluate_stage(repo, run, tasks, 'final_test')
    saved = records(run)
    result = {
        'protocol': 'pilot-v0.2', 'origin': setup['origin'], 'human_evaluation': 'not_performed',
        'calibration': read_json(run / 'freeze.json')['calibration'],
        'primary_comparison': 'grounded_reflection_minus_direct_adaptation',
        'summary': aggregate(scores), 'cases': scores, 'paired': paired(scores),
        'final_stage': final_status['budget'],
        'preparation': inference_scores(repo, run), 'resources': resource_rows(saved),
        'model': cfg.backend.model, 'repetitions': cfg.repetitions,
        'limitations': ['Synthetic restricted rules, not full professional quality',
                        'No human validation or real execution of tools',
                        'One preparation cycle per repetition, not recursive improvement',
                        'Small within-family sample; no significance claims',
                        'Budgets controlled by calls and audited tokens, not identical compute'],
    }
    write_json(run / 'results.json', result)
    human_sample(repo, run, tasks, scores, saved, cfg.human_sample_seed)
    lines = ['# Pilot v0.2 results', '',
             '**OFFLINE MOCK. Infrastructure check only. No empirical findings.**' if setup['origin'] == 'offline_mock'
             else 'Live model outputs on synthetic data. No human evaluation.', '',
             f'Model `{cfg.backend.model}`. {len(tasks)} final tasks. {cfg.repetitions} repetitions.', '',
             '| Condition | Compliance | Hidden checks | Task success | Abstention on specified tasks | Missed abstention |',
             '| --- | --- | --- | --- | --- | --- |']
    def pct(value):
        return 'not measured' if value is None else f'{100 * value:.1f}%'
    for arm, s in result['summary'].items():
        lines.append(f"| {arm} | {pct(s['compliance'])} | {pct(s['by_kind']['hidden']['rate'])} | "
                     f"{s['task_passed']}/{s['attempts']} | {s['unnecessary_abstention']} | {s['missed_required_abstention']} |")
    lines += ['', '## Requirement inference', '',
              'Body matching and scope recovery are scored separately. Values below pool counts across '
              'families and repetitions. Empty prediction sets have undefined precision.', '',
              '| Condition | Stage | Precision | Recall | Scope accuracy | Distractor adoptions | Unidentifiable adoptions |',
              '| --- | --- | --- | --- | --- | --- | --- |']
    for arm in ('direct_adaptation', 'grounded_reflection'):
        for stage in ('raw', 'retained'):
            rows = [r['scores'] for r in result['preparation']
                    if r['arm'] == arm and r['stage'] == stage and r['scores'] is not None]
            matched = sum(r['true_positives'] for r in rows)
            precision = ratio(matched, sum(r['precision_denominator'] for r in rows))
            recall = ratio(matched, sum(r['recoverable_bodies'] for r in rows))
            scope = ratio(sum(r['scope_correct'] for r in rows), sum(r['scope_probe_count'] for r in rows))
            lines.append(f"| {arm} | {stage} | {pct(precision)} | {pct(recall)} | {pct(scope)} | "
                         f"{sum(r['distractor_adoptions'] for r in rows)} | {sum(r['unidentifiable_adoptions'] for r in rows)} |")
    primary = [p for p in result['paired'] if p['comparison'] == result['primary_comparison']]
    wins = sum(p['task_success_difference'] > 0 for p in primary)
    losses = sum(p['task_success_difference'] < 0 for p in primary)
    lines += ['', '## Prespecified comparison and resources', '',
              f'Grounded reflection versus direct adaptation has {wins} task-level wins, '
              f'{losses} losses and {len(primary) - wins - losses} ties. '
              'These are paired descriptive observations, not independent samples or significance tests.', '',
              '| Condition | Phase | Calls | Failed calls | Input tokens | Output tokens |',
              '| --- | --- | --- | --- | --- | --- |']
    for row in result['resources']:
        input_tokens = row['input_tokens'] if row['input_tokens'] is not None else 'unknown'
        output_tokens = row['output_tokens'] if row['output_tokens'] is not None else 'unknown'
        lines.append(f"| {row['arm']} | {row['phase']} | {row['calls']} | {row['failed_calls']} | "
                     f'{input_tokens} | {output_tokens} |')
    if result['final_stage']['stopped']:
        lines += ['', '**Run stopped before all planned calls.** ' + result['final_stage']['stopped'] +
                  '. Missing outputs remain failed attempts; this run cannot establish a fair performance advantage.']
    lines += ['', 'Calibration is unmeasured for this mock run.' if setup['origin'] == 'offline_mock'
              else 'The frozen calibration run is linked in results.json. It must satisfy the baseline target before final testing.']
    lines += ['', '## Interpretation', '',
              'Compliance measures deterministic predicates. Appropriate abstention is reported separately. '
              'Consult results.json for all denominators, scope and distractor checks, raw and retained '
              'requirement inference, paired cases, regressions and preparation variability.', '',
              'Abstention on tasks with complete context metadata is a workflow completion measure. '
              'The JSON field retains the name unnecessary_abstention. In the no-adaptation condition, '
              'requesting private requirements absent from its inputs may be epistemically justified. '
              'Do not interpret that count as proof of irrational refusal.', '',
              'The mock does not infer requirements and behaves identically across conditions. '
              'Its outputs cannot support claims about reflection or calibration.' if setup['origin'] == 'offline_mock'
              else 'Inspect the prespecified D versus C comparison without selecting favourable tasks or repetitions.', '',
              '## Limits and next checks', '', *['* ' + x for x in result['limitations']], '',
              'Token usage is unavailable for the mock. Unknown live usage and cost remain null, not zero. '
              'human-review.json is a blinded review sample; the key is stored separately. No reviews have been collected.', '']
    with (run / 'REPORT.md').open('x', encoding='utf-8') as handle:
        handle.write('\n'.join(lines))
