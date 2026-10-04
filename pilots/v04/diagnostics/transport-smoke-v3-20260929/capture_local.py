"""Local request inspection only. Never forwards to any inference service."""
import argparse
import gzip
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import threading
from unittest.mock import patch

REPO = Path(r'%USERPROFILE%\Downloads\RWTH\RWTH\Research\PostDoc\05_Software\grounded-reflection')
sys.path.insert(0, str(REPO / 'src'))
sys.path.insert(0, str(REPO / 'pilots/v04'))
from reflectai_v04 import transport as codex_backend
from run_smoke import shadow_gateway_http
from observation import observe_https
from sse_compat import compatibility_https
observations = {}

parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--hardened', action='store_true')
parser.add_argument('--attested', action='store_true')
parser.add_argument('--reply', choices=['reject', 'success', 'retryable', 'question'], default='reject')
args = parser.parse_args()
root = args.output.resolve()
root.mkdir(parents=True, exist_ok=False)
captures = []


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get('Content-Length', '0')))
        encoding = self.headers.get('Content-Encoding', '')
        if encoding == 'gzip':
            body = gzip.decompress(body)
        elif encoding == 'zstd':
            import zstandard
            body = zstandard.ZstdDecompressor().decompress(body)
        captures.append({'path': self.path, 'body': json.loads(body)})
        if args.reply == 'success' or (args.reply == 'question' and len(captures) == 1):
            if args.reply == 'success':
                item = {'id': 'msg_local', 'type': 'message', 'role': 'assistant', 'status': 'completed',
                        'content': [{'type': 'output_text', 'text': '{"answer":"local"}', 'annotations': []}]}
            else:
                item = {'id': 'fc_local', 'type': 'function_call', 'call_id': 'call_local',
                        'name': 'request_user_input', 'arguments': json.dumps({'questions': []}),
                        'status': 'completed'}
            response = {'id': 'resp_local', 'object': 'response', 'created_at': 1790680000,
                        'status': 'completed', 'model': 'gpt-6-sol', 'output': [item],
                        'usage': {'input_tokens': 1, 'output_tokens': 1, 'total_tokens': 2}}
            events = [
                {'type': 'response.created', 'response': {**response, 'status': 'in_progress', 'output': []}},
                {'type': 'response.output_item.added', 'output_index': 0, 'item': item},
                {'type': 'response.output_item.done', 'output_index': 0, 'item': item},
                {'type': 'response.completed', 'response': response},
            ]
            payload = ''.join('event: '+event['type']+'\ndata: '+json.dumps(event)+'\n\n' for event in events).encode()
            self.send_response(200)
            # Deliberately omit MIME to exercise the diagnostic compatibility path.
            self.send_header('Content-Length', str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        # Deliberately no inference, no synthetic success and no forwarding.
        payload = json.dumps({'error': {'message': 'LOCAL PREFLIGHT STOP. No model exists at this endpoint.',
                                        'type': 'invalid_request_error', 'code': 'local_preflight'}}).encode()
        self.send_response(503 if args.reply == 'retryable' else 400)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
worker = threading.Thread(target=server.serve_forever, daemon=True)
worker.start()
port = server.server_address[1]
real_run = subprocess.run
real_temporary_directory = codex_backend.tempfile.TemporaryDirectory

def diagnostic_workspace(*args, **kwargs):
    return real_temporary_directory(*args, dir=root, **kwargs)
diagnostic_overrides = ['model_providers.reflectai_codex.requires_openai_auth=false']
real_http_connection = __import__('http.client', fromlist=['HTTPConnection']).HTTPConnection

def local_connection(host, *, timeout):
    if host != 'chatgpt.com':
        raise AssertionError('Unexpected production destination')
    return real_http_connection('127.0.0.1', port, timeout=timeout)

hardening = []
invocation = {}


def launch(command, **kwargs):
    if command[1] != 'exec' or command[-1] != '-':
        raise AssertionError('Only the inspected transport invocation is allowed.')
    for folder, value in [('evaluator', 'PRIVATE_EVALUATOR_CANARY_06f81a7b'),
                           ('future', 'PRIVATE_FUTURE_CANARY_4ae3c172')]:
        destination = root / folder
        destination.mkdir()
        (destination / 'private.txt').write_text(value, encoding='utf-8')
    (root / 'AGENTS.md').write_text('PRIVATE_ANCESTOR_DOC_CANARY_46ddc80e', encoding='utf-8')
    invocation.update(original_command=command, cwd=str(kwargs['cwd']),
                      workspace_was_empty=not any(Path(kwargs['cwd']).iterdir()),
                      diagnostics_only=diagnostic_overrides, proposed_hardening=hardening,
                      gateway_upstream_replaced_with_loopback_fixture=True,
                      temporary_parent_controlled_for_ancestor_canary=True)
    probe = command[:-1]
    for override in diagnostic_overrides + hardening:
        probe.extend(['-c', override])
    probe.append('-')
    # No API keys or access tokens are needed or sent to the local provider.
    environment = {key: value for key, value in os.environ.items()
                   if not any(token in key.upper() for token in ('API_KEY', 'ACCESS_TOKEN', 'AUTH_TOKEN'))
                   and key.upper() not in ('OPENAI_BASE_URL', 'OPENAI_ORG_ID', 'OPENAI_PROJECT_ID')}
    kwargs['env'] = {key: value for key, value in kwargs.get('env', environment).items() if key in environment}
    kwargs['timeout'] = 45
    return real_run(probe, **kwargs)


error = None
try:
    from contextlib import nullcontext
    context = nullcontext() if args.attested else patch.object(codex_backend, '_attest', return_value={'diagnostic_only': 'unattested preliminary transport inspection', 'allowed_request_tools': []})
    with context, patch.object(codex_backend.subprocess, 'run', side_effect=launch), shadow_gateway_http(codex_backend.gateway, compatibility_https(observe_https(local_connection, observations), observations, validate_event=codex_backend.gateway._event_kind, error_type=codex_backend.gateway.GatewayError)), patch.object(codex_backend.tempfile, 'TemporaryDirectory', side_effect=diagnostic_workspace):
        codex_backend.run_completion(
            'PUBLIC_PREFLIGHT_CANARY_8a7f. Return a JSON object with answer set to local.',
            {'type': 'object', 'properties': {'answer': {'type': 'string'}},
             'required': ['answer'], 'additionalProperties': False},
            root / 'transport', 'gpt-6-sol', 'medium', executable=shutil.which('codex'))
except Exception as exc:
    error = f'{type(exc).__name__}: {exc}'
finally:
    server.shutdown()
    server.server_close()

(root / 'requests.json').write_text(json.dumps(captures, indent=2), encoding='utf-8')
(root / 'invocation.json').write_text(json.dumps(invocation, indent=2), encoding='utf-8')
text = json.dumps(captures)
def advertised_tools(body):
    result = list(body.get('tools', []))
    for item in body.get('input', []):
        if item.get('type') == 'additional_tools':
            result.extend(item.get('tools', []))
    return result


summary = {'purpose': 'Local request capture without a model or external inference endpoint.',
           'http_observations': observations, 'model_calls': 0, 'local_requests': len(captures), 'expected_transport_error': error,
           'workspace_was_empty': invocation.get('workspace_was_empty'),
           'private_evaluator_visible': 'PRIVATE_EVALUATOR_CANARY_06f81a7b' in text,
           'private_future_visible': 'PRIVATE_FUTURE_CANARY_4ae3c172' in text,
           'ancestor_document_visible': 'PRIVATE_ANCESTOR_DOC_CANARY_46ddc80e' in text,
           'public_prompt_visible': 'PUBLIC_PREFLIGHT_CANARY_8a7f' in text,
           'tools': [advertised_tools(request['body']) for request in captures]}
(root / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps({key: value for key, value in summary.items() if key != 'tools'}, indent=2))
print(json.dumps({'advertised_tools': [[{'name': tool.get('name'), 'type': tool.get('type')}
                                      for tool in group] for group in summary['tools']]}, indent=2))




