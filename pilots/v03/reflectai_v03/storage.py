"""Write-once artifacts, source fingerprints and explicit experimental freezes."""

import hashlib
import json
from pathlib import Path


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def read_json(path: Path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write_json(path: Path, value) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n')


def source_manifest(repo: Path) -> dict[str, str]:
    repo = Path(repo)
    paths = [repo / 'docs/pilot-v03-protocol.md', repo / 'docs/pilot-v03-design-review.md',
             repo / 'pilots/v03/SCENARIOS.md',
             repo / 'pyproject.toml', repo / 'pilots/v03/run_pilot.py']
    for folder, pattern in [('src/grounded_reflection', '*.py'),
                            ('pilots/v03/reflectai_v03', '*.py'),
                            ('pilots/v03/prompts', '*.txt'),
                            ('tests', 'test_pilot_v03_*.py')]:
        paths.extend(sorted((repo / folder).rglob(pattern)))
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise ValueError(f'incomplete source manifest: {missing}')
    return {path.relative_to(repo).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(set(paths))}


def verify_sources(repo: Path, expected: dict) -> None:
    if source_manifest(repo) != expected:
        raise ValueError('source changed after recorded review or freeze')


def snapshot_sources(repo: Path, run_dir: Path, manifest: dict) -> None:
    for name, expected in manifest.items():
        content = (repo / name).read_bytes()
        if hashlib.sha256(content).hexdigest() != expected:
            raise ValueError('source changed while taking snapshot')
        target = run_dir / 'source_snapshot' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(content)


def review_template(repo: Path) -> dict:
    return {
        'status': 'pending', 'reviewer': '', 'date': '',
        'source_manifest': source_manifest(repo),
        'pairs': [{'pair': pair, 'approved': False, 'notes': ''}
                  for pair in ('P01', 'P02', 'P03', 'P04')],
        'notes': 'Offline human review of the warrant rubric. Not agent questioning. '
                 'Record disagreements and revise before approval.',
    }


def validate_review(repo: Path, review: dict) -> None:
    if review.get('status') != 'approved' or not review.get('reviewer', '').strip() or not review.get('date', '').strip():
        raise ValueError('live calibration requires a completed, named human rubric review')
    pairs = review.get('pairs', [])
    if len(pairs) != 4 or {pair.get('pair') for pair in pairs} != {'P01', 'P02', 'P03', 'P04'}:
        raise ValueError('review must cover all four scenario pairs exactly once')
    if any(pair.get('approved') is not True for pair in pairs):
        raise ValueError('a scenario pair remains unapproved')
    verify_sources(repo, review.get('source_manifest', {}))


def task_identity(history, task) -> str:
    """Paired current tasks are intentional; history+task reuse is not."""
    history_data = history.model_dump(mode='json')
    history_data.pop('history_id')
    for record in history_data['records']:
        record.pop('record_id')
    task_data = task.model_dump(mode='json')
    task_data.pop('task_id')
    return digest({'history': history_data, 'task': task_data})


def check_separation(dataset, previous_identities: list[str]) -> list[str]:
    histories = {history.history_id: history for history in dataset.histories}
    membership = {truth.task_id: truth.history_id for truth in dataset.task_truths}
    current = [task_identity(histories[membership[task.task_id]], task) for task in dataset.tasks]
    if len(current) != len(set(current)):
        raise ValueError('duplicate history-plus-task identity inside split')
    if set(current).intersection(previous_identities):
        raise ValueError('development/final history-plus-task leakage')
    return current


def seal_files(root: Path, relative_paths: list[str]) -> dict:
    return {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
            for name in sorted(relative_paths)}


def verify_seal(root: Path, manifest: dict) -> None:
    if seal_files(root, list(manifest)) != manifest:
        raise ValueError('frozen history or preparation changed before task revelation')
