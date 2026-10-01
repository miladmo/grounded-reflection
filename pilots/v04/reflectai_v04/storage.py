"""Source bindings, append-only stage seals and separate approval records."""

import hashlib
import json
from pathlib import Path
import shutil

from .backend import write_json
from .config import MATERIAL_REVISION

LEGACY_DEPENDENCIES = (
    'src/grounded_reflection/__init__.py', 'src/grounded_reflection/models.py',
    'src/grounded_reflection/codex_backend.py',
    'src/grounded_reflection/workflow.py',
    'pilots/v03/reflectai_v03/__init__.py', 'pilots/v03/reflectai_v03/contracts.py',
    'pilots/v03/reflectai_v03/context.py', 'pilots/v03/reflectai_v03/evaluation.py',
    'pilots/v03/reflectai_v03/wire.py',
)


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     allow_nan=False).encode('utf-8')).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_files(repo: Path, pilot: Path, protocol: Path) -> dict[str, Path]:
    files = {name: repo / name for name in LEGACY_DEPENDENCIES}
    for folder, suffix in (('reflectai_v04', '.py'), ('prompts', '.txt')):
        files.update({f'pilots/v04/{folder}/{p.name}': p
                      for p in (pilot / folder).glob('*' + suffix)})
    files['pilots/v04/run.py'] = pilot / 'run.py'
    files.update({f'tests/{p.name}': p
                  for p in (pilot.parent.parent / 'tests').glob('test_pilot_v04*.py')})
    files['docs/pilot-v04-protocol.md'] = protocol
    files['docs/pilot-v04-amendment-03.md'] = protocol.with_name('pilot-v04-amendment-03.md')
    files['docs/pilot-v04-surface-repair.md'] = protocol.with_name('pilot-v04-surface-repair.md')
    files['docs/pilot-v04-transport-preflight.md'] = protocol.with_name('pilot-v04-transport-preflight.md')
    files['docs/pilot-v04-fhgenie-transport.md'] = protocol.with_name('pilot-v04-fhgenie-transport.md')
    files['docs/pilot-v04-amendment-04.md'] = protocol.with_name('pilot-v04-amendment-04.md')
    files['docs/pilot-v04-fhgenie-contract-test.md'] = protocol.with_name('pilot-v04-fhgenie-contract-test.md')
    files['docs/pilot-v04-amendment-05.md'] = protocol.with_name('pilot-v04-amendment-05.md')
    for name in ('model-catalog.json', 'runtime-attestation.json', 'fhgenie-request.ps1',
                 'test_fhgenie_request.ps1'):
        files[f'pilots/v04/transport/{name}'] = pilot / 'transport' / name
    if not files or any(not p.is_file() for p in files.values()):
        raise ValueError('Required version-bound source is missing.')
    return files


def source_binding(repo: Path, pilot: Path, protocol: Path) -> dict:
    files = source_files(repo, pilot, protocol)
    hashes = {name: file_hash(path) for name, path in sorted(files.items())}
    return {'sha256': digest(hashes), 'files': hashes}


def snapshot_sources(destination: Path, repo: Path, pilot: Path, protocol: Path) -> dict:
    binding = source_binding(repo, pilot, protocol)
    destination.mkdir(parents=True, exist_ok=False)
    for name, source in source_files(repo, pilot, protocol).items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if file_hash(target) != binding['files'][name]:
            raise ValueError('Source changed while copying its frozen snapshot.')
    if source_binding(repo, pilot, protocol) != binding:
        raise ValueError('Source changed during snapshot creation.')
    write_json(destination / 'binding.json', binding)
    return binding


def assert_sources(binding: dict, repo: Path, pilot: Path, protocol: Path) -> None:
    if binding != source_binding(repo, pilot, protocol):
        raise ValueError('Sources changed after the run freeze.')


def seal(directory: Path, manifest_path: Path) -> dict:
    if manifest_path.exists():
        raise FileExistsError('A seal cannot be overwritten.')
    files = {p.relative_to(directory).as_posix(): file_hash(p)
             for p in sorted(directory.rglob('*')) if p.is_file() and p != manifest_path}
    manifest = {'sha256': digest(files), 'files': files}
    write_json(manifest_path, manifest)
    return manifest


def verify_seal(directory: Path, manifest_path: Path) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    files = {p.relative_to(directory).as_posix(): file_hash(p)
             for p in sorted(directory.rglob('*')) if p.is_file() and p != manifest_path}
    if manifest != {'sha256': digest(files), 'files': files}:
        raise ValueError('Stage seal does not match its exact file set.')
    return manifest


def pending_approvals(source_hash: str, material_hash: str) -> dict:
    return {'source_sha256': source_hash, 'material_sha256': material_hash,
            'material_revision': MATERIAL_REVISION,
            'materials': {'approved': None, 'reviewer': None, 'date': None, 'response': None},
            'live': {'approved': None, 'reviewer': None, 'date': None, 'response': None,
                     'config_sha256': None}}


def validate_approvals(approval: dict, *, source_hash: str, material_hash: str,
                       config: dict) -> None:
    if approval.get('material_revision') != MATERIAL_REVISION:
        raise ValueError('Approval must identify the current material revision.')
    if approval.get('source_sha256') != source_hash or approval.get('material_sha256') != material_hash:
        raise ValueError('Approval is not bound to the current sources and reviewed materials.')
    for name in ('materials', 'live'):
        item = approval.get(name, {})
        if item.get('approved') is not True or item.get('reviewer') != 'Milad Morad':
            raise ValueError(f'Separate actual {name} approval is required.')
        if not all(isinstance(item.get(key), str) and item[key].strip()
                   for key in ('date', 'response')):
            raise ValueError('Approval must preserve the actual dated human response.')
    if approval['live'].get('config_sha256') != digest(config):
        raise ValueError('Live approval does not cover this exact run configuration.')
