"""Stage files and integrity checks. No loader combines inputs with gold data."""

import hashlib
import json
from pathlib import Path


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write('\n')


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def repo_manifest(repo):
    repo = Path(repo)
    files = list((repo / 'src/grounded_reflection').rglob('*.py'))
    files += list((repo / 'pilots/v02/prompts').glob('*.txt'))
    files += list((repo / 'pilots/v02/data').rglob('*.json'))
    files += [repo / 'pyproject.toml', repo / 'docs/pilot-v02-protocol.md',
              repo / 'pilots/v02/run_pilot.py']
    return {p.relative_to(repo).as_posix(): file_hash(p) for p in sorted(files)}


def verify_repo(repo, manifest):
    if repo_manifest(repo) != manifest:
        raise ValueError('Frozen source, prompts or development data changed')


def check_run_directory(repo, run):
    repo, run = Path(repo).resolve(), Path(run).resolve()
    protected = [repo / 'pilots/hr_v01', repo / 'src', repo / 'tests', repo / 'docs',
                 repo / 'pilots/v02/data', repo / 'pilots/v02/prompts']
    if run == repo or any(run == p or run.is_relative_to(p) for p in protected):
        raise ValueError('Run directory must not overwrite source, dataset or v0.1 files')
    return run


def task_fingerprint(task):
    payload = task.public_payload()
    payload.pop('case_id')
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def check_task_separation(groups):
    ids, fingerprints = set(), set()
    for tasks in groups:
        for task in tasks:
            fingerprint = task_fingerprint(task)
            if task.case_id in ids or fingerprint in fingerprints:
                raise ValueError('Duplicated or relabelled task across evaluation splits')
            ids.add(task.case_id)
            fingerprints.add(fingerprint)
