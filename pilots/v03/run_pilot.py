"""Run from the repository root. Defaults never call a model provider."""

import argparse
import json
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from reflectai_v03.contracts import RunConfig
from reflectai_v03.data import build_histories, build_tasks
from reflectai_v03.runner import freeze_main, run_experiment
from reflectai_v03.storage import read_json, review_template, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    offline = commands.add_parser('offline', help='Integration check, no inference or calibration claims')
    offline.add_argument('--out', type=Path, required=True)
    offline.add_argument('--seed', type=int, default=3301)
    offline.add_argument('--repetitions', type=int, choices=(1, 2, 3), default=3)
    export = commands.add_parser('export-development', help='Export public examples and separate evaluator truth')
    export.add_argument('--out', type=Path, required=True)
    export.add_argument('--seed', type=int, default=3301)
    review = commands.add_parser('review-template', help='Create a pending rubric review, not an approval')
    review.add_argument('--out', type=Path, required=True)
    calibration = commands.add_parser('calibrate', help='Live A/B/C only, requires completed human rubric review')
    calibration.add_argument('--config', type=Path, required=True)
    calibration.add_argument('--review', type=Path, required=True)
    calibration.add_argument('--round', type=int, choices=(1, 2), required=True)
    calibration.add_argument('--allow-live', action='store_true')
    calibration.add_argument('--out', type=Path, required=True)
    freeze = commands.add_parser('freeze', help='F0 after human review and successful live calibration')
    freeze.add_argument('--config', type=Path, required=True)
    freeze.add_argument('--review', type=Path, required=True)
    freeze.add_argument('--calibration', type=Path, nargs='+', required=True)
    freeze.add_argument('--out', type=Path, required=True)
    final = commands.add_parser('main', help='One sealed final comparison, no tuning or retries')
    final.add_argument('--freeze', type=Path, required=True)
    final.add_argument('--allow-live', action='store_true')
    final.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.command == 'review-template':
        write_json(args.out, review_template(REPO))
        print(f'Pending human review template: {args.out}')
        return
    if args.command == 'export-development':
        if args.out.exists():
            raise FileExistsError('use a new export directory')
        dataset = build_tasks(build_histories(args.seed, split='development'), task_seed=args.seed ^ 0x5A193)
        write_json(args.out / 'public/histories.json', [history.model_dump(mode='json') for history in dataset.histories])
        write_json(args.out / 'public/tasks.json', [task.model_dump(mode='json') for task in dataset.tasks])
        write_json(args.out / 'evaluator/truth.json', {
            'split': dataset.split, 'seed': dataset.seed, 'assignments': dataset.assignments,
            'history_truths': [truth.model_dump(mode='json') for truth in dataset.truths],
            'task_truths': [truth.model_dump(mode='json') for truth in dataset.task_truths],
        })
        print(f'Development examples only: {args.out}')
        return
    if args.command == 'freeze':
        config = RunConfig.model_validate(read_json(args.config))
        freeze_main(REPO, args.out, config, read_json(args.review), args.calibration)
        print(f'F0 written: {args.out}')
        return
    if args.command == 'offline':
        config = RunConfig(seed=args.seed, repetitions=args.repetitions)
        summary = run_experiment(REPO, args.out, config)
    elif args.command == 'calibrate':
        config = RunConfig.model_validate(read_json(args.config))
        if config.phase != 'calibration':
            raise ValueError('calibrate requires phase=calibration')
        summary = run_experiment(REPO, args.out, config, allow_live=args.allow_live,
                                 review=read_json(args.review), calibration_round=args.round)
    else:
        frozen = read_json(args.freeze)
        config = RunConfig.model_validate(frozen['config'])
        summary = run_experiment(REPO, args.out, config, allow_live=args.allow_live, freeze=frozen)
    print(json.dumps({'status': summary['status'], 'phase': config.phase,
                      'attempted_calls': summary['budget']['attempted_calls'],
                      'planned_generation_attempts': summary['planned_generation_attempts'],
                      'error': summary['error'], 'report': str(args.out / 'REPORT.md')}, indent=2))
    if summary['status'] != 'completed':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
