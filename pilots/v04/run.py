"""Run the offline pilot or export material review. Live requires bound approvals."""

import argparse
import json
from pathlib import Path
import sys

PILOT = Path(__file__).resolve().parent
REPO = PILOT.parent.parent
# The isolated pilot is intentionally not part of the published package.
for folder in (REPO / 'src', REPO / 'pilots' / 'v03', PILOT):
    sys.path.insert(0, str(folder))

from reflectai_v04.backend import write_json
from reflectai_v04.config import RunConfig
from reflectai_v04.review import export_review
from reflectai_v04.runner import run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('offline', 'review', 'live'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--config', type=Path)
    parser.add_argument('--review-dir', type=Path)
    parser.add_argument('--approvals', type=Path)
    parser.add_argument('--allow-live', action='store_true')
    args = parser.parse_args()
    paths = {'repo': REPO, 'pilot': PILOT, 'protocol': REPO / 'docs' / 'pilot-v04-protocol.md'}
    if args.command == 'review':
        if args.allow_live or args.config:
            parser.error('Material export does not use a model configuration.')
        print(json.dumps(export_review(args.output, **paths), indent=2))
        return
    config = RunConfig.model_validate_json(args.config.read_text()) if args.config else RunConfig()
    if args.command == 'offline' and (config.backend != 'mock' or args.allow_live):
        parser.error('Offline runs cannot use live inference.')
    if args.command == 'live' and (not config.is_live or not args.allow_live):
        parser.error('Live execution requires an explicit live config and separate approvals.')
    output_existed = args.output.exists()
    try:
        result = run(args.output, config, **paths, allow_live=args.allow_live,
                     review_dir=args.review_dir, approval_path=args.approvals)
    except (Exception, KeyboardInterrupt) as exc:
        if (not output_existed and args.output.is_dir()
                and (args.output / 'planned-calls.json').is_file()
                and not (args.output / 'manifest.json').exists()):
            marker = args.output / 'INCOMPLETE.json'
            if not marker.exists():
                write_json(marker, {'status': 'incomplete', 'error': f'{type(exc).__name__}: {exc}',
                                    'planned_generation_attempts': 144,
                                    'planned_diagnostics_per_arm': 24,
                                    'planned_controls_per_arm': 24,
                                    'instruction': 'Preserve all records. Missing attempts remain in denominators. '
                                                   'No resume or replacement is authorised.'})
        raise
    print(json.dumps({'output': str(args.output), 'offline': result['offline'],
                      'status': result.get('status', 'unknown'),
                      'planned_calls': result['planned_calls'], 'budget': result['budget']}, indent=2))
    if not result.get('complete_schedule'):
        raise SystemExit(2)


if __name__ == '__main__':
    main()
