"""Source binding, directory seals and exclusive approval reservations for v0.5."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
PILOT = REPO / 'pilots' / 'v05'
SHARED = ('src/grounded_reflection/__init__.py', 'src/grounded_reflection/models.py',
          'src/grounded_reflection/codex_backend.py',
          'pilots/v03/reflectai_v03/__init__.py', 'pilots/v03/reflectai_v03/contracts.py',
          'pilots/v03/reflectai_v03/context.py', 'pilots/v03/reflectai_v03/wire.py',
          'pilots/v04/reflectai_v04/__init__.py', 'pilots/v04/reflectai_v04/fhgenie_transport.py',
          'pilots/v04/transport/fhgenie-request.ps1', 'pilots/v04/transport/test_fhgenie_request.ps1',
          'docs/pilot-v05-protocol.md')


def file_hash(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()


def source_files(repo: Path = REPO) -> dict[str, Path]:
    files = {name: repo / name for name in SHARED}
    pilot = repo / 'pilots' / 'v05'
    for folder, pattern in (('reflectai_v05', '*.py'), ('prompts', '*.txt')):
        files.update({f'pilots/v05/{folder}/{p.name}': p for p in (pilot / folder).glob(pattern)})
    files['pilots/v05/run.py'] = pilot / 'run.py'
    files.update({f'tests/{p.name}': p for p in (repo / 'tests').glob('test_pilot_v05*.py')})
    missing = [name for name, path in files.items() if not path.is_file()]
    if missing:
        raise ValueError(f'required version-bound source is missing: {missing}')
    return files


def source_binding(repo: Path = REPO) -> dict:
    hashes = {name: file_hash(path) for name, path in sorted(source_files(repo).items())}
    return {'sha256': digest(hashes), 'files': hashes}


def seal(directory: Path, manifest: Path) -> dict:
    directory = Path(directory)
    files = {p.relative_to(directory).as_posix(): file_hash(p)
             for p in sorted(directory.rglob('*')) if p.is_file() and p != manifest}
    result = {'sha256': digest(files), 'files': files, 'sealed_at': datetime.now(timezone.utc).isoformat()}
    manifest.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    return result


def verify_seal(directory: Path, manifest: Path) -> dict:
    recorded = json.loads(Path(manifest).read_text(encoding='utf-8'))
    files = {p.relative_to(directory).as_posix(): file_hash(p)
             for p in sorted(Path(directory).rglob('*')) if p.is_file() and p != Path(manifest)}
    if files != recorded['files'] or digest(files) != recorded['sha256']:
        raise ValueError('seal verification failed')
    return recorded


def validate_approval(approval: dict, *, phase: str, config_sha256: str, source_sha256: str) -> None:
    expected = {'approved': True, 'reviewer': 'Milad Morad', 'phase': phase,
                'config_sha256': config_sha256, 'source_sha256': source_sha256}
    if any(approval.get(k) != v for k, v in expected.items()) \
            or not isinstance(approval.get('response'), str) or not approval['response'].strip() \
            or not isinstance(approval.get('date'), str):
        raise PermissionError('the live approval does not match this phase, configuration and sources')


def reserve(approval: dict, output_dir: Path, folder: Path = PILOT / '.authorizations') -> dict:
    folder.mkdir(parents=True, exist_ok=True)
    key = digest(approval)
    reservation = {'approval_sha256': key, 'phase': approval['phase'], 'output_dir': str(Path(output_dir).name),
                   'reserved_at': datetime.now(timezone.utc).isoformat()}
    try:
        with (folder / f'{key}.json').open('x', encoding='utf-8') as stream:
            json.dump(reservation, stream, indent=2)
    except FileExistsError:
        raise PermissionError('this approval was already reserved; a new approval is required') from None
    return reservation
