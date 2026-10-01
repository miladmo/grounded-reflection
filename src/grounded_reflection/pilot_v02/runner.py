"""Explicit experiment stages. Only evaluation opens the separate truth files."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import random
import secrets
import sys

import pydantic

from .backend import Backend, BudgetError
from .context import render_context, retained_preparation
from .contracts import ARMS, CallRecord, History, Preparation, RunConfig, Task, WorkOutput
from .data import generate_tasks
from .storage import (check_run_directory, check_task_separation, file_hash, read_json,
                      repo_manifest, verify_repo, write_json)


def prompt(repo, name, payload):
    folder = Path(repo) / 'pilots/v02/prompts'
    text = (folder / (name + '.txt')).read_text(encoding='utf-8')
    return text + '\nPAYLOAD\n' + json.dumps(payload, ensure_ascii=False, sort_keys=True)


def load_histories(repo):
    items = read_json(Path(repo) / 'pilots/v02/data/histories.json')
    histories = [History.model_validate(x) for x in items]
    if len({h.family for h in histories}) != len(histories):
        raise ValueError('Duplicate history family')
    return {h.family: h for h in histories}


def load_tasks(path, split):
    tasks = [Task.model_validate(x) for x in read_json(path)]
    if not tasks or any(t.split != split for t in tasks):
        raise ValueError('Wrong task split or empty task set')
    check_task_separation([tasks])
    return tasks


def records(run):
    return [CallRecord.model_validate(read_json(p))
            for p in sorted((Path(run) / 'calls').glob('*/record.json'))]


def initialise(repo, run, config, kind, allow_live):
    config = RunConfig.model_validate(read_json(config))
    Backend(config.backend, allow_live=allow_live)
    run = check_run_directory(repo, run)
    run.mkdir(parents=True, exist_ok=False)
    write_json(run / 'setup.json', {
        'kind': kind, 'config': config.model_dump(), 'source_files': repo_manifest(repo),
        'created_at': datetime.now(timezone.utc).isoformat(),
        'environment': {'python': sys.version, 'platform': platform.platform(),
                        'pydantic': pydantic.__version__},
        'origin': 'offline_mock' if config.backend.backend == 'mock' else 'model_generated',
    })
    return run, config


def existing(repo, run, kind='experiment'):
    run = check_run_directory(repo, run)
    setup = read_json(run / 'setup.json')
    if setup['kind'] != kind:
        raise ValueError('This stage requires a ' + kind + ' run')
    verify_repo(repo, setup['source_files'])
    return run, RunConfig.model_validate(setup['config']), setup


def prepare(repo, run, config, allow_live=False):
    run, cfg = initialise(repo, run, config, 'experiment', allow_live)
    backend = Backend(cfg.backend, allow_live=allow_live)
    histories = load_histories(repo)
    jobs = [(r, f, a) for r in range(cfg.repetitions) for f in sorted(histories)
            for a in ('direct_adaptation', 'grounded_reflection')]
    random.Random(cfg.order_seed).shuffle(jobs)
    statuses = []
    stopped = None
    for repetition, family, arm in jobs:
        previous = None
        for pass_number in (1, 2):
            payload = {'family': family, 'history': histories[family].model_dump(mode='json'),
                       'pass': 'initial' if pass_number == 1 else 'review',
                       'previous': previous}
            call_id = f'prepare-r{repetition}-{family}-{arm}-{pass_number}'
            result = backend.complete(prompt(repo, arm, payload), Preparation,
                                      run / 'calls' / call_id, call_id=call_id, arm=arm,
                                      phase='prepare', family=family, repetition=repetition)
            if result.status != 'completed':
                stopped = f'Call {call_id} failed: {result.error or "unknown error"}'
                break
            previous = result.response
        status = result.status
        statuses.append(status)
        raw = Preparation.model_validate(previous) if status == 'completed' else None
        kept, rejected = retained_preparation(raw, histories[family], arm == 'grounded_reflection') \
            if raw else (Preparation(), [])
        write_json(run / 'prepared' / f'r{repetition}-{family}-{arm}.json', {
            'origin': result.origin, 'status': status, 'raw': raw.model_dump(mode='json') if raw else None,
            'retained': kept.model_dump(mode='json'), 'rejected': rejected,
        })
        if stopped:
            break
    write_json(run / 'prepare.json', {'complete': stopped is None and len(statuses) == len(jobs)
                                                and all(x == 'completed' for x in statuses),
                                    'stopped': stopped,
                                    'budget': backend.budget_summary()})


def generation_payload(repo, run, task, arm, repetition, histories):
    payload = {'baseline': (Path(repo) / 'pilots/v02/prompts/baseline.txt').read_text(encoding='utf-8'),
               'task': task.public_payload()}
    if arm == 'direct_evidence':
        payload['history'] = histories[task.family].model_dump(mode='json')
    elif arm in ('direct_adaptation', 'grounded_reflection'):
        saved = read_json(Path(run) / 'prepared' / f'r{repetition}-{task.family}-{arm}.json')
        if saved['status'] != 'completed':
            raise ValueError('Preparation failed; start a separately labelled run')
        payload['guidance'] = render_context(Preparation.model_validate(saved['retained']), task.context)
    return payload


def generate(repo, run, cfg, tasks, phase, allow_live, arms=ARMS):
    backend = Backend(cfg.backend, allow_live=allow_live, prior_records=records(run))
    histories = load_histories(repo) if any(a != 'no_adaptation' for a in arms) else {}
    jobs = [(r, t, a) for r in range(cfg.repetitions) for t in tasks for a in arms]
    random.Random(cfg.order_seed).shuffle(jobs)
    stopped = None
    for repetition, task, arm in jobs:
        call_id = f'{phase}-r{repetition}-{task.case_id}-{arm}'
        payload = generation_payload(repo, run, task, arm, repetition, histories)
        try:
            result = backend.complete(prompt(repo, 'generation', payload), WorkOutput,
                                      Path(run) / 'calls' / call_id, call_id=call_id, arm=arm,
                                      phase=phase, family=task.family, repetition=repetition)
        except BudgetError as exc:
            stopped = str(exc)
            break
        if result.status == 'failed':
            stopped = f'Call {call_id} failed: {result.error or "unknown error"}'
            break
    return {**backend.budget_summary(), 'stopped': stopped, 'expected_stage_outputs': len(jobs)}


def calibrate(repo, run, config, allow_live=False, round_number=1, rationale='Initial calibration'):
    if round_number not in (1, 2):
        raise ValueError('Protocol permits only calibration rounds 1 and 2')
    run, cfg = initialise(repo, run, config, 'calibration', allow_live)
    tasks = load_tasks(Path(repo) / 'pilots/v02/data/calibration.json', 'calibration')
    usage = generate(repo, run, cfg, tasks, 'calibration', allow_live, ('no_adaptation',))
    from .report import evaluate_stage, aggregate
    scored = evaluate_stage(repo, run, tasks, 'calibration')
    summary = aggregate(scored)
    rate = summary['no_adaptation']['compliance']
    live = cfg.backend.backend != 'mock'
    complete = not usage['stopped'] and summary['no_adaptation']['failed_calls'] == 0
    write_json(run / 'calibration.json', {
        'origin': 'model_generated' if live else 'offline_mock',
        'round': round_number, 'rationale': rationale, 'summary': summary, 'budget': usage,
        'target': [0.3, 0.7], 'within_band': rate is not None and 0.3 <= rate <= 0.7,
        'complete': complete,
        'calibrated': live and complete and rate is not None and 0.3 <= rate <= 0.7,
        'limitation': 'Mock results cannot establish calibration. Inspect hidden and explicit checks separately.',
    })


def validate(repo, run, allow_live=False):
    run, cfg, _ = existing(repo, run)
    if (run / 'freeze.json').exists() or (run / 'validation.json').exists():
        raise ValueError('Validation is closed or already recorded')
    if not read_json(run / 'prepare.json')['complete']:
        raise ValueError('Incomplete preparation')
    tasks = load_tasks(Path(repo) / 'pilots/v02/data/validation.json', 'validation')
    usage = generate(repo, run, cfg, tasks, 'validation', allow_live)
    from .report import evaluate_stage, aggregate
    scored = evaluate_stage(repo, run, tasks, 'validation')
    write_json(run / 'validation.json', {'summary': aggregate(scored), 'budget': usage,
                                       'selection': 'No candidate search. Second preparation pass retained as prespecified.'})


def run_inputs(run):
    files = [Path(run) / 'setup.json', Path(run) / 'prepare.json', Path(run) / 'validation.json']
    files += list((Path(run) / 'prepared').glob('*.json'))
    for call in (Path(run) / 'calls').iterdir():
        if call.name.startswith(('prepare-', 'validation-')):
            files += [p for p in call.rglob('*') if p.is_file()]
    return {p.relative_to(run).as_posix(): file_hash(p) for p in sorted(files)}


def freeze(repo, run, calibration_run=None):
    run, cfg, setup = existing(repo, run)
    if (run / 'heldout').exists():
        raise ValueError('Final tasks must not exist before the freeze')
    if not read_json(run / 'prepare.json')['complete'] or not (run / 'validation.json').is_file():
        raise ValueError('Complete preparation and validation before freezing')
    calibration = None
    if cfg.backend.backend != 'mock':
        if calibration_run is None:
            raise ValueError('A live run requires a completed live calibration run')
        cal, cal_cfg, _ = existing(repo, calibration_run, 'calibration')
        result = read_json(cal / 'calibration.json')
        if not result['calibrated']:
            raise ValueError('Calibration did not satisfy the protocol target')
        if (cfg.backend.backend, cfg.backend.model, cfg.backend.reasoning_effort) != \
                (cal_cfg.backend.backend, cal_cfg.backend.model, cal_cfg.backend.reasoning_effort):
            raise ValueError('Calibration model and settings do not match')
        calibration = {'path': str(cal), 'files': {
            p.relative_to(cal).as_posix(): file_hash(p) for p in sorted(cal.rglob('*')) if p.is_file()}}
    write_json(run / 'freeze.json', {
        'frozen_at': datetime.now(timezone.utc).isoformat(), 'origin': setup['origin'],
        'source_files': setup['source_files'], 'run_files': run_inputs(run),
        'calibration': calibration, 'final_tasks_exist_at_freeze': False,
    })


def verify_freeze(repo, run):
    locked = read_json(Path(run) / 'freeze.json')
    verify_repo(repo, locked['source_files'])
    if run_inputs(run) != locked['run_files']:
        raise ValueError('Frozen preparation, configuration or validation changed')
    if locked['calibration']:
        cal = locked['calibration']
        root = Path(cal['path'])
        current = {p.relative_to(root).as_posix(): file_hash(p)
                   for p in sorted(root.rglob('*')) if p.is_file()}
        if current != cal['files']:
            raise ValueError('Calibration record changed')
    return locked


def final(repo, run, allow_live=False):
    run, cfg, _ = existing(repo, run)
    Backend(cfg.backend, allow_live=allow_live, prior_records=records(run))
    verify_freeze(repo, run)
    if (run / 'heldout').exists():
        raise ValueError('Final evaluation already started; no reruns or replacement of test cases')
    seed = secrets.randbits(63)
    tasks, truth = generate_tasks('final_test', seed)
    calibration_tasks = load_tasks(Path(repo) / 'pilots/v02/data/calibration.json', 'calibration')
    validation_tasks = load_tasks(Path(repo) / 'pilots/v02/data/validation.json', 'validation')
    check_task_separation([calibration_tasks, validation_tasks, tasks])
    write_json(run / 'heldout' / 'tasks.json', [t.model_dump() for t in tasks])
    write_json(run / 'heldout' / 'ground_truth.json', [t.model_dump() for t in truth])
    write_json(run / 'heldout' / 'manifest.json', {
        'seed': seed, 'generated_after_freeze': file_hash(run / 'freeze.json'),
        'tasks_sha256': file_hash(run / 'heldout/tasks.json'),
        'truth_sha256': file_hash(run / 'heldout/ground_truth.json'),
        'note': 'Generated only after freeze. Test content is never supplied to preparation.',
    })
    usage = generate(repo, run, cfg, tasks, 'final_test', allow_live)
    output_files = {p.relative_to(run).as_posix(): file_hash(p)
                    for call in (run / 'calls').glob('final_test-*')
                    for p in sorted(call.rglob('*')) if p.is_file()}
    write_json(run / 'final.json', {'budget': usage, 'output_files': output_files,
                                  'expected_outputs': len(tasks) * len(ARMS) * cfg.repetitions})


def main(repo, argv=None):
    parser = argparse.ArgumentParser(description='Synthetic pilot v0.2; offline by default')
    sub = parser.add_subparsers(dest='stage', required=True)
    for name in ('calibrate', 'prepare', 'validate', 'freeze', 'final', 'report'):
        child = sub.add_parser(name)
        child.add_argument('--run-dir', type=Path, required=True)
        if name in ('calibrate', 'prepare'):
            child.add_argument('--config', type=Path, default=Path(repo) / 'pilots/v02/config.mock.json')
        if name in ('calibrate', 'prepare', 'validate', 'final'):
            child.add_argument('--allow-live', action='store_true', help='Use only after agreeing provider and budget')
        if name == 'calibrate':
            child.add_argument('--round', type=int, choices=(1, 2), default=1)
            child.add_argument('--rationale', default='Initial calibration')
        if name == 'freeze':
            child.add_argument('--calibration-run', type=Path)
    args = parser.parse_args(argv)
    try:
        if args.stage == 'calibrate':
            calibrate(repo, args.run_dir, args.config, args.allow_live, args.round, args.rationale)
        elif args.stage == 'prepare':
            prepare(repo, args.run_dir, args.config, args.allow_live)
        elif args.stage == 'validate':
            validate(repo, args.run_dir, args.allow_live)
        elif args.stage == 'freeze':
            freeze(repo, args.run_dir, args.calibration_run)
        elif args.stage == 'final':
            final(repo, args.run_dir, args.allow_live)
        else:
            from .report import report
            report(repo, args.run_dir)
    except (ValueError, FileExistsError, FileNotFoundError, RuntimeError) as exc:
        parser.exit(2, str(exc) + '\n')
    print('Completed ' + args.stage + '. See ' + str(args.run_dir))
