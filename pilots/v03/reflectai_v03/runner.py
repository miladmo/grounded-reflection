"""Paired pilot execution. Future tasks are instantiated only after preparation."""

import json
from pathlib import Path
import random

from .backend import Backend
from .context import generation_payload, retained_rules
from .contracts import Preparation, ReflectionDraft, RunConfig, WorkOutput
from .data import build_histories, build_tasks
from .evaluation import aggregate, calibration_gates, evaluate_output, evaluate_preparation
from .report import export_blinded_sample, write_report
from .storage import (check_separation, digest, read_json, seal_files, source_manifest, snapshot_sources,
                      validate_review, verify_seal, verify_sources, write_json)


PREPARATION_PROMPTS = {
    'C': {1: 'prepare_C_v2.txt', 2: 'review_C_v2.txt'},
    'D': {1: 'prepare_D_v3.txt', 2: 'review_D_v3.txt'},
}
GENERATION_PROMPT = 'generate_v2.txt'
SHARED_CONTRACT = 'shared_contract_v2.txt'
DESIGN_REVISION = 'v03-calibration-r2'


def _prompt(repo: Path, name: str, payload: dict) -> str:
    folder = repo / 'pilots/v03/prompts'
    template = (folder / name).read_text(encoding='utf-8')
    contract = (folder / SHARED_CONTRACT).read_text(encoding='utf-8')
    return (template.rstrip() + '\n\n' + contract.rstrip() + '\nPAYLOAD\n'
            + json.dumps(payload, ensure_ascii=False))


def _planned_rows(dataset, arms, repetitions):
    rows = []
    for truth in dataset.truths:
        for repetition in range(repetitions):
            for probe in ('diagnostic', 'control'):
                for arm in arms:
                    rows.append({
                        'history_id': truth.history_id, 'scenario_id': truth.scenario_id,
                        'pair_id': truth.pair_id, 'arm': arm, 'repetition': repetition,
                        'probe': probe, 'task_id': None,
                        'expected_decision': ('apply' if probe == 'diagnostic' and
                                              truth.scenario_id in ('S01', 'S04', 'S06', 'S08') else 'keep'),
                        'recoverable': not (truth.scenario_id == 'S02' and probe == 'diagnostic'),
                        'update_correct': False, 'warranted': False, 'world_compliant': False,
                        'warranted_world_compliant': False, 'completed_deliverable': False,
                        'valid_output': False, 'partial_field_correctness': 0.0,
                        'errors': ['not attempted'],
                    })
    return rows


def _candidate_score(truth, history, preparation, arm, step):
    if arm == 'D' and step == 1:
        return {'preparation_present': preparation is not None,
                'evaluation_mode': 'uncommitted_draft_not_status_scored',
                'candidate_count': len(preparation.candidates) if preparation else 0,
                'target_status_metrics': None}
    return evaluate_preparation(truth, history, preparation)


def _grouped_usage(records):
    groups = {}
    for record in records:
        group = groups.setdefault(record['arm'], {}).setdefault(record['phase'], {
            'attempted_calls': 0, 'failed_calls': 0, 'reported_tokens': 0,
            'calls_with_unknown_token_usage': 0,
        })
        group['attempted_calls'] += 1
        group['failed_calls'] += record['status'] == 'failed'
        usage = record['usage']
        counts = [usage.get('input_tokens'), usage.get('output_tokens')]
        group['reported_tokens'] += sum(value for value in counts if value is not None)
        group['calls_with_unknown_token_usage'] += any(value is None for value in counts)
    return groups


def _check_live(repo: Path, config: RunConfig, allow_live: bool, review, freeze) -> None:
    if config.phase == 'offline':
        return
    if not allow_live:
        raise ValueError('live phases require explicit --allow-live')
    if config.backend.model != 'gpt-6-sol' or config.backend.reasoning_effort != 'medium':
        raise ValueError('this protocol fixes gpt-6-sol with medium reasoning')
    if config.phase == 'calibration':
        validate_review(repo, review or {})
    else:
        if not freeze or freeze.get('stage') != 'F0':
            raise ValueError('main execution requires the reviewed and calibrated F0 freeze')
        verify_sources(repo, freeze['source_manifest'])
        if config.model_dump(mode='json') != freeze['config']:
            raise ValueError('main configuration differs from F0')
        validate_review(repo, freeze['human_review'])
        if freeze.get('calibration_passed') is not True:
            raise ValueError('main blocked because calibration has not passed')
        registry = repo / 'pilots/v03/runs/F0_registry.json'
        if not registry.is_file() or read_json(registry).get('F0_digest') != digest(freeze):
            raise ValueError('main requires the registered F0, not an unregistered or edited copy')


def run_experiment(repo: Path, run_dir: Path, config: RunConfig, *,
                   allow_live=False, review=None, freeze=None,
                   calibration_round: int | None = None, backend=None) -> dict:
    repo, run_dir = Path(repo), Path(run_dir)
    _check_live(repo, config, allow_live, review, freeze)
    if backend is not None and config.phase != 'offline':
        raise ValueError('injected backends are restricted to offline tests')
    arms = ['A', 'B', 'C'] if config.phase == 'calibration' else ['A', 'B', 'C', 'D']
    prep_arms = [arm for arm in arms if arm in ('C', 'D')]
    expected_calls = 8 * config.repetitions * (2 * len(prep_arms) + 2 * len(arms))
    if config.phase != 'offline' and config.backend.max_calls != expected_calls:
        raise ValueError(f'live call budget must equal the {expected_calls} planned logical calls')
    if config.backend.max_calls < expected_calls:
        raise ValueError(f'call budget must allow the {expected_calls} planned logical calls')
    if run_dir.exists():
        raise FileExistsError('use a new run directory; runs cannot be resumed or overwritten')
    if config.phase == 'calibration':
        if calibration_round not in (1, 2):
            raise ValueError('calibration requires round 1 or 2, at most two rounds')
        # Atomic reservation before any call. A failed round still consumes a round.
        ledger = repo / 'pilots/v03/runs/calibration_registry'
        if (repo / 'pilots/v03/runs/F0_registry.json').exists():
            raise ValueError('calibration cannot continue after F0')
        if calibration_round == 2 and not (ledger / 'round-1.json').is_file():
            raise ValueError('round 2 requires a recorded round 1')
        if calibration_round == 2:
            prior_dir = Path(read_json(ledger / 'round-1.json')['run_dir'])
            if not (prior_dir / 'results.json').is_file():
                raise ValueError('round 1 must have a terminal report before round 2')
        write_json(ledger / f'round-{calibration_round}.json', {
            'run_dir': str(run_dir.resolve()), 'config': config.model_dump(mode='json'),
            'review_digest': digest(review),
        })
    if config.phase == 'main':
        write_json(repo / 'pilots/v03/runs/main_registry.json', {
            'run_dir': str(run_dir.resolve()), 'F0_digest': digest(freeze),
            'config': config.model_dump(mode='json'),
        })
    run_dir.mkdir(parents=True)
    manifest = source_manifest(repo)
    write_json(run_dir / 'source_manifest.json', manifest)
    snapshot_sources(repo, run_dir, manifest)
    write_json(run_dir / 'config.json', config.model_dump(mode='json'))
    if review:
        write_json(run_dir / 'human_rubric_review.json', review)
    if freeze:
        write_json(run_dir / 'F0.json', freeze)
    split = 'final_test' if config.phase == 'main' else 'development'
    dataset = build_histories(config.seed, split=split)
    if dataset.tasks or dataset.task_truths:
        raise ValueError('history generator leaked future tasks before F1')
    write_json(run_dir / 'public/histories.json', [history.model_dump(mode='json') for history in dataset.histories])
    write_json(run_dir / 'evaluator/history_truth.json', [truth.model_dump(mode='json') for truth in dataset.truths])
    write_json(run_dir / 'evaluator/assignments.json', dataset.assignments)
    rows = _planned_rows(dataset, arms, config.repetitions)
    histories = {history.history_id: history for history in dataset.histories}
    truths = {truth.history_id: truth for truth in dataset.truths}
    preparations, outputs = {}, {}
    candidate_scores = [
        {'arm': arm, 'repetition': repetition, 'history_id': history_id,
         'scenario_id': truths[history_id].scenario_id, 'step': step,
         'scores': _candidate_score(truths[history_id], histories[history_id], None, arm, step)}
        for history_id in histories for arm in prep_arms
        for repetition in range(config.repetitions) for step in (1, 2)
    ]
    candidate_index = {(row['history_id'], row['arm'], row['repetition'], row['step']): row
                       for row in candidate_scores}
    engine = backend or Backend(config.backend, allow_live=allow_live)
    rng = random.Random(config.order_seed)
    status, error = 'completed', None
    task_identities = []
    seal_paths = ['public/histories.json', 'evaluator/history_truth.json', 'evaluator/assignments.json']
    try:
        preparation_order = [(history_id, arm, repetition) for history_id in histories
                             for arm in prep_arms for repetition in range(config.repetitions)]
        rng.shuffle(preparation_order)
        for history_id, arm, repetition in preparation_order:
            history, previous = histories[history_id], None
            for step in (1, 2):
                payload = {'history': history.model_dump(mode='json')}
                if previous is not None:
                    payload['previous_preparation'] = previous.model_dump(mode='json')
                name = PREPARATION_PROMPTS[arm][step]
                schema = ReflectionDraft if arm == 'D' and step == 1 else Preparation
                call_id = f'{arm}-{repetition}-{history_id}-prepare-{step}'
                record = engine.complete(_prompt(run_dir / 'source_snapshot', name, payload), schema,
                    run_dir / 'calls' / call_id, call_id=call_id, arm=arm,
                    phase='prepare', history_id=history_id, repetition=repetition)
                if record['status'] != 'completed':
                    raise RuntimeError(f"{call_id}: {record.get('error', 'failed response')}")
                previous = Preparation.model_validate(record['response'])
                score = _candidate_score(truths[history_id], history, previous, arm, step)
                candidate_index[(history_id, arm, repetition, step)]['scores'] = score
                name = f'preparations/{arm}-{repetition}-{history_id}-{step}.json'
                write_json(run_dir / name, previous.model_dump(mode='json'))
                seal_paths.append(name)
            retained_rules(previous, history)  # The same reference checks for C and D.
            preparations[(history_id, arm, repetition)] = previous

        verify_sources(repo, manifest)
        f1 = {'stage': 'F1', 'origin': 'offline_mock' if config.phase == 'offline' else 'model_generated',
              'source_manifest_digest': digest(manifest), 'files': seal_files(run_dir, seal_paths),
              'prepared_artifacts': len(preparations), 'future_tasks_generated': False}
        write_json(run_dir / 'F1.json', f1)
        verify_seal(run_dir, f1['files'])
        verify_sources(repo, manifest)
        # This is the first and only future-task generation in an experiment.
        dataset = build_tasks(dataset, task_seed=config.seed ^ 0x5A193)
        previous_identities = freeze.get('development_identities', []) if freeze else []
        task_identities = check_separation(dataset, previous_identities)
        write_json(run_dir / 'public/tasks.json', [task.model_dump(mode='json') for task in dataset.tasks])
        write_json(run_dir / 'evaluator/task_truth.json', [truth.model_dump(mode='json') for truth in dataset.task_truths])
        tasks = {task.task_id: task for task in dataset.tasks}
        task_truths = {truth.task_id: truth for truth in dataset.task_truths}
        membership = {(truth.history_id, truth.probe): truth for truth in dataset.task_truths}
        for row in rows:
            task_truth = membership[(row['history_id'], row['probe'])]
            row.update(task_id=task_truth.task_id, expected_decision=task_truth.expected_decision,
                       recoverable=task_truth.recoverable)
            row.update(evaluate_output(tasks[task_truth.task_id], task_truth,
                truths[row['history_id']], None, row['arm'],
                preparations.get((row['history_id'], row['arm'], row['repetition']))))
        generation_order = list(range(len(rows)))
        rng.shuffle(generation_order)
        for index in generation_order:
            row = rows[index]
            history_id, arm, repetition = row['history_id'], row['arm'], row['repetition']
            task = tasks[row['task_id']]
            preparation = preparations.get((history_id, arm, repetition))
            payload = generation_payload(task, histories[history_id], arm, preparation)
            call_id = f'{arm}-{repetition}-{task.task_id}'
            record = engine.complete(_prompt(run_dir / 'source_snapshot', GENERATION_PROMPT, payload), WorkOutput,
                run_dir / 'calls' / call_id, call_id=call_id, arm=arm, phase='generation',
                history_id=history_id, repetition=repetition)
            if record['status'] != 'completed':
                row['errors'] = [record.get('error', 'failed response')]
                raise RuntimeError(f"{call_id}: {record.get('error', 'failed response')}")
            output = WorkOutput.model_validate(record['response'])
            outputs[call_id] = output.model_dump(mode='json')
            row.update(evaluate_output(task, task_truths[task.task_id], truths[history_id],
                                       output, arm, preparation))
        verify_sources(repo, manifest)
        verify_seal(run_dir, f1['files'])
    except Exception as exc:
        status, error = 'incomplete', f'{type(exc).__name__}: {exc}'
    summary = {
        'status': status, 'error': error, 'config': config.model_dump(mode='json'),
        'design_revision': DESIGN_REVISION,
        'source_manifest': manifest, 'planned_logical_calls': expected_calls,
        'planned_generation_attempts': len(rows), 'budget': engine.budget_summary(),
        'budget_by_arm_phase': _grouped_usage(getattr(engine, 'records', [])),
        'task_identities': task_identities, 'outcomes': aggregate(rows),
        'candidate_comparison_step': 2,
        'calibration': (calibration_gates(rows) if config.phase == 'calibration' and status == 'completed'
                        else {'passed': False, 'reason': 'No completed live calibration in this run.'}),
        'rows': rows,
    }
    write_json(run_dir / 'candidate_scores.json', candidate_scores)
    write_json(run_dir / 'results.json', summary)
    export_blinded_sample(run_dir, dataset, rows, outputs, config.order_seed ^ 19)
    write_report(run_dir / 'REPORT.md', summary)
    write_json(run_dir / 'artifact_manifest.json', seal_files(run_dir, [
        path.relative_to(run_dir).as_posix() for path in run_dir.rglob('*') if path.is_file()
    ]))
    return summary


def freeze_main(repo: Path, output: Path, config: RunConfig, review: dict,
                calibration_dirs: list[Path]) -> dict:
    """F0 is allowed only after completed live calibration and human rubric review."""
    validate_review(repo, review)
    if output.exists() or (repo / 'pilots/v03/runs/F0_registry.json').exists():
        raise FileExistsError('F0 already exists; do not refreeze after seeing final evidence')
    if config.phase != 'main':
        raise ValueError('F0 requires a main configuration')
    if not 1 <= len(calibration_dirs) <= 2:
        raise ValueError('provide one or two completed calibration rounds')
    registry = repo / 'pilots/v03/runs/calibration_registry'
    registrations = sorted(registry.glob('round-*.json'))
    registered_paths = [Path(read_json(path)['run_dir']).resolve() for path in registrations]
    if [Path(path).resolve() for path in calibration_dirs] != registered_paths:
        raise ValueError('F0 must include every registered calibration round in order')
    reports = []
    for directory in calibration_dirs:
        directory = Path(directory)
        verify_seal(directory, read_json(directory / 'artifact_manifest.json'))
        report = read_json(directory / 'results.json')
        if report['config']['phase'] != 'calibration' or report['config']['backend']['backend'] != 'codex':
            raise ValueError('offline outputs cannot authorise F0')
        if any(report['config']['backend'][field] != getattr(config.backend, field)
               for field in ('backend', 'model', 'reasoning_effort', 'timeout_seconds')):
            raise ValueError('calibration and main model settings must match')
        reports.append(report)
    last = reports[-1]
    verify_sources(repo, last['source_manifest'])
    gates = calibration_gates(last['rows'])
    if last['status'] != 'completed' or not gates['passed']:
        raise ValueError('calibration failed; main comparison is not authorised')
    if config.seed in [report['config']['seed'] for report in reports]:
        raise ValueError('main must use a fresh instance seed')
    freeze = {'stage': 'F0', 'source_manifest': source_manifest(repo),
              'config': config.model_dump(mode='json'), 'human_review': review,
              'calibration_passed': True, 'calibration_gates': gates,
              'calibration_report_digests': [digest(report) for report in reports],
              'development_identities': [identity for report in reports for identity in report['task_identities']]}
    write_json(output, freeze)
    write_json(repo / 'pilots/v03/runs/F0_registry.json', {
        'path': str(output.resolve()), 'F0_digest': digest(freeze),
    })
    return freeze
