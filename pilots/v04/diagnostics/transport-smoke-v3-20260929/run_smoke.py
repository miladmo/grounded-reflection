"""One separately approved connection check; never loads research materials."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys
from unittest.mock import patch
from types import SimpleNamespace

from observation import observe_https
from proxy_connection import proxy_https
from sse_compat import compatibility_https

HERE = Path(__file__).resolve().parent
PROMPT = 'Return exactly this JSON object: {"status":"ok"}. This is a connection test. Do not use tools.'
SCHEMA = {'type': 'object', 'properties': {'status': {'type': 'string'}},
          'required': ['status'], 'additionalProperties': False}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def validate_plan(repo):
    plan = json.loads((HERE / 'plan.json').read_text(encoding='utf-8'))
    assert plan['model'] == 'gpt-6-sol' and plan['reasoning_effort'] == 'medium'
    assert plan['max_calls'] == 1 and plan['timeout_seconds'] == 60
    assert plan['prompt'] == PROMPT and plan['schema'] == SCHEMA
    for name, expected in plan['diagnostic_files'].items():
        assert digest(HERE / name) == expected, f'Diagnostic file changed: {name}'
    attestation = repo / 'pilots/v04/transport/runtime-attestation.json'
    assert digest(attestation) == plan['runtime_attestation_sha256']
    return plan


def reserve(approval, plan_sha256):
    if not (approval.get('approved') is True and approval.get('reviewer') == 'Milad Morad'
            and approval.get('plan_sha256') == plan_sha256
            and isinstance(approval.get('response'), str) and approval['response'].strip()
            and isinstance(approval.get('date'), str) and approval['date'].strip()):
        raise ValueError('Separate explicit approval for this one connection check is required.')
    with (HERE / 'reservation.json').open('x', encoding='utf-8') as stream:
        json.dump({'plan_sha256': plan_sha256, 'reserved_at': datetime.now(timezone.utc).isoformat(),
                   'approval': approval, 'max_attempts': 1}, stream, ensure_ascii=False, indent=2)


def shadow_gateway_http(gateway, factory):
    # HTTPSConnection.__init__ refers to the class in http.client. Keep that
    # module unchanged and replace only this gateway's connection lookup.
    scoped = SimpleNamespace(client=SimpleNamespace(
        HTTPSConnection=factory, HTTPException=gateway.http.client.HTTPException))
    return patch.object(gateway, 'http', scoped)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=HERE.parents[3])
    parser.add_argument('--execute-one-live-smoke', action='store_true')
    args = parser.parse_args()
    repo = args.repo.resolve(strict=True)
    plan = validate_plan(repo)
    for name in ('src', 'pilots/v04'):
        sys.path.insert(0, str(repo / name))
    from reflectai_v04 import transport
    executable = shutil.which('codex')
    if not executable:
        raise ValueError('Installed Codex CLI not found.')
    transport._attest(executable, transport.TRANSPORT_DIR / 'model-catalog.json')
    if not args.execute_one_live_smoke:
        print(json.dumps({'plan_verified': True, 'runtime_attestation_verified': True,
                          'model_calls': 0, 'execution': 'not requested'}))
        return

    approval = json.loads((HERE / 'approval.json').read_text(encoding='utf-8'))
    reserve(approval, digest(HERE / 'plan.json'))
    output = HERE / 'attempt'
    output.mkdir(exist_ok=False)
    observations = {}
    original_https = transport.gateway.http.client.HTTPSConnection
    observed = observe_https(proxy_https(original_https, observations), observations)
    factory = compatibility_https(observed, observations, validate_event=transport.gateway._event_kind,
                                 error_type=transport.gateway.GatewayError)
    result, error = None, None
    try:
        with shadow_gateway_http(transport.gateway, factory):
            result = transport.run_completion(PROMPT, SCHEMA, output / 'transport',
                                              plan['model'], plan['reasoning_effort'],
                                              plan['timeout_seconds'], executable=executable)
    except Exception as exc:
        error = f'{type(exc).__name__}: {exc}'
    finally:
        write(output / 'http-observations.json', observations)
        metadata_file = output / 'transport/metadata.json'
        metadata = json.loads(metadata_file.read_text(encoding='utf-8')) if metadata_file.exists() else {}
        summary = {'purpose': 'Connection diagnostic only; no research data or result',
                   'attempts': 1, 'retries': 0, 'expected_json_received': bool(
                       result and result['response'] == {'status': 'ok'}),
                   'transport_status': metadata.get('status'), 'gateway': metadata.get('gateway'),
                   'usage': metadata.get('usage'), 'error': error,
                   'http_observations': observations}
        write(output / 'summary.json', summary)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not result or result['response'] != {'status': 'ok'}:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
