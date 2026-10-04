"""Pilot v0.5 entry point. Offline mock runs need no approval; live runs need one."""

import argparse
import json
from pathlib import Path
import sys

PILOT = Path(__file__).resolve().parent
REPO = PILOT.parent.parent
for folder in (REPO / 'src', REPO / 'pilots' / 'v03', REPO / 'pilots' / 'v04', PILOT):
    if str(folder) not in sys.path:
        sys.path.insert(0, str(folder))

from reflectai_v05.config import RunConfig, phase_config  # noqa: E402
from reflectai_v05.runner import run  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('offline', 'live', 'review'))
    parser.add_argument('--phase', choices=('calibration', 'dcheck', 'main'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--config', type=Path)
    parser.add_argument('--approval', type=Path)
    parser.add_argument('--allow-live', action='store_true')
    args = parser.parse_args()
    if args.command == 'review':
        from reflectai_v05.review import export_review
        print(json.dumps(export_review(args.output), indent=2))
        return
    if not args.phase:
        parser.error('--phase is required')
    if args.command == 'offline':
        if args.allow_live or args.config or args.approval:
            parser.error('offline runs use the mock backend only')
        result = run(args.output, phase_config(args.phase))
    else:
        if not (args.allow_live and args.config and args.approval):
            parser.error('live runs require --allow-live, --config and --approval')
        config = RunConfig.model_validate_json(args.config.read_text(encoding='utf-8'))
        if config.phase != args.phase:
            parser.error('the configuration belongs to another phase')
        approval = json.loads(args.approval.read_text(encoding='utf-8'))
        result = run(args.output, config, allow_live=True, approval=approval)
    print(json.dumps({'manifest_sha256': result['manifest_sha256'], 'budget': result['summary']['budget'],
                      'complete': result['summary']['complete']}, indent=2))


if __name__ == '__main__':
    main()
