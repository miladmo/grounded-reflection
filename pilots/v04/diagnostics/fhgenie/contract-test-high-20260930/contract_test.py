"""FHGenie contract test: 16 development calls, technical measurements only.

Commands (run from any directory with the pinned Python runtime):

  plan    --pwsh PATH            write plan.json; offline, no credential, no network
  verify  --pwsh PATH            recompute the plan and compare it byte-for-byte
  execute --pwsh PATH --once     requires approval.json and an unused reservation

The evaluator is never applied to model outputs: no scores, headroom values or
error attributions are computed. Only development seeds are used. Every call is
attempted at most once. There are no retries, repairs or replacement calls.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import sys

HERE = Path(__file__).resolve().parent
PILOT = HERE.parents[2]
REPO = PILOT.parent.parent
for folder in (REPO / 'src', REPO / 'pilots' / 'v03', PILOT):
    if str(folder) not in sys.path:
        sys.path.insert(0, str(folder))

import pydantic  # noqa: E402
from reflectai_v03.context import retained_rules  # noqa: E402
from reflectai_v03.contracts import Preparation, WorkOutput  # noqa: E402
from reflectai_v03.wire import decode_response, strict_response_schema  # noqa: E402
from reflectai_v04 import fhgenie_transport  # noqa: E402
from reflectai_v04.config import (DEVELOPMENT_FUTURE_SEED, DEVELOPMENT_HISTORY_SEED,  # noqa: E402
                                  DEVELOPMENT_ORDER_SEED, FHGENIE_ENDPOINT, FHGENIE_MODEL,
                                  MATERIAL_REVISION)
from reflectai_v04.data import generate_future_tasks, generate_histories  # noqa: E402
from reflectai_v04.payloads import generation_payload, preparation_payload, prompt_for  # noqa: E402
from reflectai_v04.storage import source_binding  # noqa: E402

REASONING_EFFORT = 'high'
NEXT_LEVEL = {'low': 'high', 'high': 'max', 'max': None}
FINAL_SEEDS = (44361, 44362, 44363)
MAX_OUTPUT_TOKENS = 16384
TIMEOUT_SECONDS = 420
TOKEN_STOP = 600_000
MAX_INVALID = 1
PROJECTION_LIMIT = 4_800_000
FINAL_TOKEN_STOP = 6_000_000
WALL_LIMIT_SECONDS = 336
LARGE_SETTINGS = ('S2', 'S5')
HISTORIES = {'H1': ('S0', 'sales'), 'H2': ('S1', 'sales'),
             'H3': ('S2', 'reporting'), 'H4': ('S5', 'retrieval')}
CALLS = ([('C1', 'C', h) for h in HISTORIES] + [('C2', 'C', h) for h in HISTORIES]
         + [('generate', 'C', h) for h in HISTORIES]
         + [('generate', 'B', 'H2'), ('generate', 'B', 'H4'),
            ('generate', 'A', 'H1'), ('generate', 'A', 'H3')])
# Same system-message prefix as fhgenie_transport; a test keeps both in sync.
SYSTEM_PREFIX = ('Return one JSON object conforming to the JSON schema below. '
                 'Return only the JSON object, without markdown fences or extra text. '
                 'Do not use tools. JSON schema: ')
BASE_PREPARATION = Preparation(notes='Offline mock. No requirement inference.')
FORMAT_REASONS = ('invalid_json', 'contract_invalid')
LIMIT_REASONS = ('truncated',)
SYSTEMIC_ISSUES = frozenset({
    'request_invalid', 'credential_unavailable', 'credential_invalid', 'http_error',
    'http_completion_invalid', 'response_rejected', 'response_model_invalid',
    'response_model_mismatch', 'response_usage_invalid', 'response_usage_unknown',
    'response_tool_call', 'local_error', 'driver_envelope_invalid', 'driver_status_invalid',
    'driver_error_invalid', 'driver_flags_invalid', 'driver_identifiers_invalid',
    'driver_http_metadata_invalid', 'driver_output_invalid', 'driver_not_completed',
})
OTHER_ISSUES = frozenset({'response_refusal', 'response_role_invalid', 'response_choice_invalid',
                          'response_content_invalid'})


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode('utf-8'))


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n',
                    encoding='utf-8')


def render_plan(plan: dict) -> bytes:
    return (json.dumps(plan, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8')


def input_chars(prompt: str, schema: dict) -> int:
    schema_text = json.dumps(schema, ensure_ascii=False, allow_nan=False, separators=(',', ':'))
    return len(SYSTEM_PREFIX) + len(schema_text) + len(prompt)


def call_type(phase: str, arm: str, setting: str) -> str:
    size = 'large' if setting in LARGE_SETTINGS else 'small'
    if phase in ('C1', 'C2'):
        return f'{phase}_{size}'
    if arm == 'B':
        return f'B_{size}'
    return 'C_gen' if arm == 'C' else 'A'


def call_label(index: int, phase: str, arm: str, history: str) -> str:
    return f'{index:02d}-{"gen" if phase == "generate" else phase}-{arm}-{history}'


def schema_for(phase: str) -> tuple[type, dict]:
    contract = WorkOutput if phase == 'generate' else Preparation
    return contract, strict_response_schema(contract)


def load_material() -> dict:
    """Public development histories and diagnostic tasks; truth stays in memory only."""
    if (DEVELOPMENT_HISTORY_SEED, DEVELOPMENT_FUTURE_SEED, DEVELOPMENT_ORDER_SEED) == FINAL_SEEDS \
            or {DEVELOPMENT_HISTORY_SEED, DEVELOPMENT_FUTURE_SEED} & set(FINAL_SEEDS):
        raise ValueError('The contract test must never use the final seeds.')
    cases = generate_histories(DEVELOPMENT_HISTORY_SEED, split='development')
    if len(cases) != 24:
        raise ValueError('Development material must contain the 24 allocated histories.')
    # Same per-history future seeds as the offline runner: base seed + list index.
    tasks = [generate_future_tasks(case, DEVELOPMENT_FUTURE_SEED + index)
             for index, case in enumerate(cases)]
    index = {(case.setting, case.family): position for position, case in enumerate(cases)}
    selected = {}
    for label, cell in HISTORIES.items():
        position = index[cell]
        diagnostic = [task for task, truth in tasks[position] if truth.probe == 'diagnostic']
        if len(diagnostic) != 1:
            raise ValueError('Each history requires exactly one diagnostic task.')
        selected[label] = {'case': cases[position], 'task': diagnostic[0]}
    return {'cases': cases, 'tasks': tasks, 'selected': selected}


def base_prompt(phase: str, arm: str, history, task=None) -> str:
    """Prompt as sent, with an empty preparation where a model output would follow."""
    if phase == 'C1':
        payload, stage = preparation_payload(history), 'C1'
    elif phase == 'C2':
        payload, stage = preparation_payload(history, BASE_PREPARATION), 'C2'
    else:
        preparation = BASE_PREPARATION if arm == 'C' else None
        payload, stage = generation_payload(task, history, arm, preparation), 'generate'
    return prompt_for(stage, payload, PILOT / 'prompts')


def projection_base(material: dict) -> dict:
    """Input characters and call counts of the registered 192-call schedule."""
    counts, chars = Counter(), Counter()
    for case, pairs in zip(material['cases'], material['tasks']):
        for phase in ('C1', 'C2'):
            kind = call_type(phase, 'C', case.setting)
            counts[kind] += 1
            chars[kind] += input_chars(base_prompt(phase, 'C', case.history), schema_for(phase)[1])
        for task, _truth in pairs:
            for arm in ('A', 'B', 'C'):
                kind = call_type('generate', arm, case.setting)
                counts[kind] += 1
                chars[kind] += input_chars(base_prompt('generate', arm, case.history, task),
                                           schema_for('generate')[1])
    if sum(counts.values()) != 192:
        raise ValueError('The registered schedule has 192 calls.')
    return {'calls_by_type': dict(sorted(counts.items())),
            'base_input_chars_by_type': dict(sorted(chars.items())),
            'base_input_chars_total': sum(chars.values()),
            'c2_calls_with_previous_preparation': counts['C2_small'] + counts['C2_large'],
            'c_generation_calls_with_guidance': counts['C_gen']}


def build_plan(pwsh: Path, material: dict | None = None) -> dict:
    pwsh = Path(pwsh).resolve()
    if not pwsh.is_file():
        raise FileNotFoundError('PowerShell 7 executable not found.')
    material = material or load_material()
    calls = []
    for index, (phase, arm, label) in enumerate(CALLS, start=1):
        item = material['selected'][label]
        case, task = item['case'], item['task']
        entry = {'index': index, 'label': call_label(index, phase, arm, label), 'phase': phase,
                 'arm': arm, 'history': label, 'setting': case.setting, 'family': case.family,
                 'history_id': case.history.history_id,
                 'task_id': task.task_id if phase == 'generate' else None,
                 'type': call_type(phase, arm, case.setting)}
        prompt = base_prompt(phase, arm, case.history, task)
        chars = input_chars(prompt, schema_for(phase)[1])
        if phase == 'C2' or (phase == 'generate' and arm == 'C'):
            # Depends on an earlier model output; only its empty-preparation base is fixed.
            entry.update(prompt_sha256=None, base_input_chars=chars)
        else:
            entry.update(prompt_sha256=sha256_text(prompt), base_input_chars=chars)
        calls.append(entry)
    protocol = REPO / 'docs' / 'pilot-v04-protocol.md'
    return {
        'purpose': 'Technical contract test only; no evaluator, scores or material changes',
        'protocol': 'pilot-v0.4', 'amendment': 'docs/pilot-v04-amendment-04.md',
        'contract_test_plan': 'docs/pilot-v04-fhgenie-contract-test.md',
        'material_revision': MATERIAL_REVISION, 'split': 'development',
        'seeds': {'history': DEVELOPMENT_HISTORY_SEED, 'future': DEVELOPMENT_FUTURE_SEED,
                  'order': DEVELOPMENT_ORDER_SEED, 'final_seeds_excluded': list(FINAL_SEEDS)},
        'backend': 'fhgenie', 'endpoint': FHGENIE_ENDPOINT, 'model': FHGENIE_MODEL,
        'reasoning_effort': REASONING_EFFORT, 'next_level': NEXT_LEVEL[REASONING_EFFORT],
        'temperature': 1, 'top_p': 1, 'max_output_tokens': MAX_OUTPUT_TOKENS,
        'timeout_seconds': TIMEOUT_SECONDS, 'planned_calls': len(CALLS), 'retries': 0,
        'contract_token_stop': TOKEN_STOP,
        'decision_rule': {'max_invalid_of_16': MAX_INVALID,
                          'projection_limit_tokens': PROJECTION_LIMIT,
                          'final_token_stop': FINAL_TOKEN_STOP,
                          'wall_limit_seconds': WALL_LIMIT_SECONDS,
                          'format_reasons': list(FORMAT_REASONS), 'limit_reasons': list(LIMIT_REASONS)},
        'histories': {label: {'setting': item['case'].setting, 'family': item['case'].family,
                              'history_id': item['case'].history.history_id,
                              'record_count': len(item['case'].history.records),
                              'history_sha256': sha256_text(json.dumps(
                                  item['case'].history.model_dump(mode='json'), ensure_ascii=False,
                                  sort_keys=True)),
                              'diagnostic_task_id': item['task'].task_id}
                      for label, item in material['selected'].items()},
        'calls': calls,
        'projection_base': projection_base(material),
        'sources': {'v04_source_binding_sha256': source_binding(REPO, PILOT, protocol)['sha256'],
                    'contract_test_py_sha256': sha256_bytes(Path(__file__).read_bytes()),
                    'transport_sha256': sha256_bytes(Path(fhgenie_transport.__file__).read_bytes()),
                    'driver_sha256': sha256_bytes(fhgenie_transport.DRIVER.read_bytes())},
        'runtime': {'python': platform.python_version(), 'pydantic': pydantic.VERSION,
                    'pwsh_path': str(pwsh), 'pwsh_sha256': sha256_bytes(pwsh.read_bytes())},
    }


def load_approval(path: Path, plan_sha256: str) -> dict:
    if not path.is_file():
        raise PermissionError('No approval file: model calls are not authorised.')
    approval = json.loads(path.read_text(encoding='utf-8'))
    expected = {'approved': True, 'reviewer': 'Milad Morad', 'plan_sha256': plan_sha256,
                'reasoning_effort': REASONING_EFFORT, 'planned_calls': len(CALLS)}
    if any(approval.get(key) != value for key, value in expected.items()) \
            or not isinstance(approval.get('response'), str) or not approval['response'].strip() \
            or not isinstance(approval.get('date'), str):
        raise PermissionError('The approval does not match this exact plan and reasoning level.')
    return approval


def reserve(path: Path, plan_sha256: str, approval: dict) -> dict:
    """Consume the approval once; a stopped attempt keeps its reservation."""
    reservation = {'status': 'reserved', 'plan_sha256': plan_sha256,
                   'approval_sha256': sha256_text(json.dumps(approval, sort_keys=True,
                                                             ensure_ascii=False)),
                   'reserved_at_utc': datetime.now(timezone.utc).isoformat()}
    try:
        with path.open('x', encoding='utf-8') as stream:
            json.dump(reservation, stream, indent=2, ensure_ascii=False)
    except FileExistsError:
        raise PermissionError('This approval was already reserved; a new approval is required.') from None
    return reservation


def _usage_known(usage: dict) -> bool:
    return all(type(usage.get(key)) is int for key in ('input_tokens', 'output_tokens'))


def classify(metadata: dict, raised: bool, response, contract, history, phase: str):
    """Return (outcome, reason, parsed). Systemic outcomes stop the whole test."""
    if not metadata:
        return 'systemic', 'transport_metadata_missing', None
    if metadata.get('status') == 'timed_out':
        return 'systemic', 'timeout_usage_unknown', None
    issues = set(metadata.get('audit_issues') or [])
    systemic = sorted(issues & SYSTEMIC_ISSUES)
    if systemic:
        return 'systemic', systemic[0], None
    if not _usage_known(metadata.get('usage') or {}):
        return 'systemic', 'usage_unknown', None
    if 'response_finish_invalid' in issues:
        if metadata.get('finish_reason') == 'length':
            return 'invalid', 'truncated', None
        return 'invalid', 'finish_invalid', None
    if 'response_invalid_json' in issues:
        return 'invalid', 'invalid_json', None
    other = sorted(issues & OTHER_ISSUES)
    if other:
        return 'invalid', other[0], None
    if issues or raised or metadata.get('status') != 'completed':
        return 'systemic', 'unexpected_transport_state', None
    try:
        parsed = contract.model_validate(decode_response(contract, response))
    except (ValueError, TypeError, pydantic.ValidationError):
        return 'invalid', 'contract_invalid', None
    if phase == 'C2':
        try:
            retained_rules(parsed, history)
        except ValueError:
            # As in the runner: invalid C2 references cannot become instructions.
            return 'invalid', 'contract_invalid', None
    return 'valid', None, parsed


def _read_metadata(directory: Path) -> dict:
    try:
        return json.loads((directory / 'metadata.json').read_text(encoding='utf-8-sig'))
    except (OSError, ValueError):
        return {}


def execute(pwsh: Path, root: Path = HERE, *, transport=None, material: dict | None = None) -> dict:
    transport = transport or fhgenie_transport.run_completion
    material = material or load_material()
    plan_path = root / 'plan.json'
    plan_bytes = plan_path.read_bytes()
    if render_plan(build_plan(pwsh, material)) != plan_bytes:
        raise ValueError('Sources, runtime or material differ from plan.json; no call was made.')
    plan = json.loads(plan_bytes)
    plan_sha256 = sha256_bytes(plan_bytes)
    approval = load_approval(root / 'approval.json', plan_sha256)
    reservation = reserve(root / 'attempt.json', plan_sha256, approval)
    run_dir = root / 'run'
    run_dir.mkdir(exist_ok=False)
    (run_dir / 'calls').mkdir()
    records, preparations, halt = [], {}, None
    for entry in plan['calls']:
        phase, arm, label = entry['phase'], entry['arm'], entry['history']
        record = {key: entry[key] for key in ('index', 'label', 'phase', 'arm', 'history',
                                              'setting', 'type', 'base_input_chars')}
        record.update(outcome=None, reason=None, usage=None, wall_seconds=None,
                      finish_reason=None, system_fingerprint=None, input_chars=None)
        records.append(record)
        if halt is None and sum(r['usage']['input_tokens'] + r['usage']['output_tokens']
                                for r in records if r['usage'] and _usage_known(r['usage'])) >= TOKEN_STOP:
            halt = 'contract_token_limit'
        if halt is not None:
            record.update(outcome='not_attempted', reason=halt)
            continue
        case, task = material['selected'][label]['case'], material['selected'][label]['task']
        blocked = None
        if phase == 'C1':
            payload, stage = preparation_payload(case.history), 'C1'
        elif phase == 'C2':
            previous = preparations.get((label, 'C1'))
            blocked = None if previous is not None else 'blocked_by_C1'
            payload, stage = (preparation_payload(case.history, previous) if previous else None), 'C2'
        else:
            stage, payload = 'generate', None
            if arm == 'C':
                preparation = preparations.get((label, 'C2'))
                if preparation is None:
                    blocked = 'blocked_by_C2'
                else:
                    try:
                        payload = generation_payload(task, case.history, 'C', preparation)
                    except ValueError:
                        blocked = 'guidance_not_executable'
            else:
                payload = generation_payload(task, case.history, arm)
        if blocked:
            record.update(outcome='blocked', reason=blocked)
            continue
        prompt = prompt_for(stage, payload, PILOT / 'prompts')
        contract, schema = schema_for(phase)
        if entry['prompt_sha256'] is not None and sha256_text(prompt) != entry['prompt_sha256']:
            record.update(outcome='systemic', reason='prompt_differs_from_plan')
            halt = 'prompt_differs_from_plan'
            continue
        record['input_chars'] = input_chars(prompt, schema)
        directory = run_dir / 'calls' / entry['label']
        result, raised = None, False
        try:
            result = transport(prompt, schema, directory, FHGENIE_MODEL, REASONING_EFFORT,
                               TIMEOUT_SECONDS, max_output_tokens=MAX_OUTPUT_TOKENS,
                               executable=plan['runtime']['pwsh_path'])
        except fhgenie_transport.InferenceRunError:
            raised = True
        except Exception:  # never log messages; they may carry process details
            record.update(outcome='systemic', reason='harness_transport_error')
            halt = 'harness_transport_error'
            continue
        metadata = result['metadata'] if result else _read_metadata(directory)
        usage = metadata.get('usage') or {}
        record.update(usage={key: usage.get(key) for key in fhgenie_transport.USAGE_KEYS},
                      wall_seconds=metadata.get('wall_seconds'),
                      finish_reason=metadata.get('finish_reason'),
                      system_fingerprint=metadata.get('system_fingerprint'),
                      actual_model=metadata.get('actual_model'),
                      reasoning_content_present=metadata.get('reasoning_content_present'))
        outcome, reason, parsed = classify(metadata, raised, result['response'] if result else None,
                                           contract, case.history, phase)
        record.update(outcome=outcome, reason=reason)
        if phase in ('C1', 'C2') and parsed is not None:
            preparations[(label, phase)] = parsed
        if outcome == 'systemic':
            halt = reason
        write_json(directory.parent / f'{entry["label"]}.record.json', record)
    projection = project(records, plan['projection_base'])
    decision = decide(records, projection, REASONING_EFFORT)
    result = {'plan_sha256': plan_sha256, 'reservation': reservation, 'halt_reason': halt,
              'records': records, 'projection': projection, 'decision': decision,
              'finished_at_utc': datetime.now(timezone.utc).isoformat(),
              'meaning': 'Technical suitability only. Model decisions were not scored.'}
    write_json(run_dir / 'results.json', result)
    (run_dir / 'REPORT.md').write_text(render_report(result, plan), encoding='utf-8')
    return result


def project(records: list[dict], base: dict) -> dict:
    """Token projection for 192 calls, following the approved contract-test rule."""
    measured = [r for r in records if r.get('usage') and _usage_known(r['usage'])]
    ratios = [r['input_chars'] / r['usage']['input_tokens'] for r in measured
              if r['input_chars'] and r['usage']['input_tokens'] > 0]
    if not ratios:
        return {'status': 'not_computable', 'passes': False,
                'reason': 'No call reported input tokens with a known input length.'}
    ratio = min(ratios)
    input_tokens = math.ceil(base['base_input_chars_total'] / ratio)
    outputs = defaultdict(list)
    for record in measured:
        outputs[record['type']].append(record['usage']['output_tokens'])
    generation = [v for k, vs in outputs.items() if k in ('A', 'B_small', 'B_large', 'C_gen') for v in vs]
    preparation = [v for k, vs in outputs.items() if k.startswith(('C1', 'C2')) for v in vs]
    output_by_type, basis = {}, {}
    for kind, count in base['calls_by_type'].items():
        values = outputs.get(kind, [])
        pool = generation if kind in ('A', 'B_small', 'B_large', 'C_gen') else preparation
        if len(values) >= 2:
            per_call, basis[kind] = max(values), 'max_of_type'
        elif pool:
            per_call, basis[kind] = max(pool), 'max_of_stage'
        else:
            per_call, basis[kind] = MAX_OUTPUT_TOKENS, 'output_limit'
        output_by_type[kind] = per_call * count
    extras = {}
    for kind, phase, arm, count_key in (
            ('C2_previous_preparation', 'C2', 'C', 'c2_calls_with_previous_preparation'),
            ('C_generation_guidance', 'generate', 'C', 'c_generation_calls_with_guidance')):
        deltas = [r['input_chars'] - r['base_input_chars'] for r in records
                  if r['phase'] == phase and r['arm'] == arm and r.get('input_chars') is not None]
        count = base[count_key]
        if deltas:
            extras[kind] = math.ceil(max(0, sum(deltas) / len(deltas)) * count / ratio)
        else:
            extras[kind] = MAX_OUTPUT_TOKENS * count
    total = input_tokens + sum(output_by_type.values()) + sum(extras.values())
    walls = defaultdict(list)
    for record in records:
        if isinstance(record.get('wall_seconds'), (int, float)):
            walls[record['type']].append(record['wall_seconds'])
    runtime = sum((max(walls[kind]) if walls.get(kind) else TIMEOUT_SECONDS) * count
                  for kind, count in base['calls_by_type'].items())
    return {'status': 'computed', 'chars_per_token_min': round(ratio, 4),
            'input_tokens': input_tokens, 'output_tokens_by_type': output_by_type,
            'output_basis_by_type': basis, 'extra_input_tokens': extras,
            'projected_total_tokens': total, 'limit': PROJECTION_LIMIT,
            'passes': total <= PROJECTION_LIMIT, 'exceeds_final_stop': total > FINAL_TOKEN_STOP,
            'runtime_upper_estimate_seconds': round(runtime, 1)}


def decide(records: list[dict], projection: dict, level: str) -> dict:
    """Apply the pre-registered rule. It is never relaxed after results are known."""
    counts = Counter(r['outcome'] for r in records)
    reasons = Counter(r['reason'] for r in records if r['outcome'] == 'invalid')
    invalid_total = counts['invalid'] + counts['blocked'] + counts['not_attempted']
    format_failures = sum(reasons[r] for r in FORMAT_REASONS)
    limit_failures = sum(reasons[r] for r in LIMIT_REASONS)
    other_failures = counts['invalid'] - format_failures - limit_failures
    slow = [r['label'] for r in records
            if isinstance(r.get('wall_seconds'), (int, float)) and r['wall_seconds'] > WALL_LIMIT_SECONDS]
    summary = {'level': level, 'planned': len(records), 'valid': counts['valid'],
               'invalid_including_blocked': invalid_total,
               'invalid_rate': round(invalid_total / len(records), 4),
               'format_failures': format_failures, 'limit_failures': limit_failures,
               'other_failures': other_failures, 'blocked': counts['blocked'],
               'not_attempted': counts['not_attempted'], 'calls_over_wall_limit': slow,
               'projection_passes': bool(projection.get('passes'))}
    if counts['systemic']:
        verdict = 'stopped_systemic'
    elif counts['not_attempted']:
        verdict = 'stopped_token_limit'
    elif invalid_total > MAX_INVALID:
        escalable = (format_failures > limit_failures + other_failures
                     and projection.get('passes') and not slow)
        if not escalable:
            verdict = 'stop_no_escalation'
        elif NEXT_LEVEL[level]:
            verdict = 'escalate_requires_new_approval'
        else:
            verdict = 'unsuitable_stop'
    elif not projection.get('passes'):
        verdict = 'stop_budget'
    elif slow:
        verdict = 'stop_runtime'
    else:
        verdict = 'passed'
    return {**summary, 'verdict': verdict,
            'next_level': NEXT_LEVEL[level] if verdict == 'escalate_requires_new_approval' else None}


VERDICT_TEXT = {
    'passed': 'Bestanden. Die Stufe kann für den finalen Lauf festgelegt werden (separate Live-Freigabe nötig).',
    'escalate_requires_new_approval': 'Nicht bestanden, Formatfehler überwiegen. Test der nächsthöheren Stufe nur nach neuer Freigabe.',
    'unsuitable_stop': 'Nicht bestanden auf der höchsten Stufe. Stopp: technisch ungeeignet über diesen Transport.',
    'stop_no_escalation': 'Nicht bestanden. Keine Eskalation (Abbrüche/andere Fehler überwiegen oder Budget/Laufzeit verletzt). Stopp.',
    'stop_budget': 'Gültigkeit ausreichend, aber Tokenhochrechnung über 4.800.000. Stopp, Entscheidung durch Milad.',
    'stop_runtime': 'Gültigkeit ausreichend, aber mindestens ein Aufruf über 336 Sekunden. Stopp.',
    'stopped_systemic': 'Systemischer Stopp (unbekannter Verbrauch, Integrität oder Transport). Kein Ergebnis.',
    'stopped_token_limit': 'Token-Stopp des Vertragstests (600.000) erreicht. Unvollständig.',
}


def render_report(result: dict, plan: dict) -> str:
    decision, projection = result['decision'], result['projection']
    lines = ['# FHGenie-Vertragstest, Stufe ' + plan['reasoning_effort'], '',
             'Nur technische Tauglichkeit. Modellentscheidungen wurden nicht bewertet.',
             f'Plan-SHA-256 `{result["plan_sha256"]}`.', '',
             f'**Ergebnis: {decision["verdict"]}.** {VERDICT_TEXT[decision["verdict"]]}', '',
             f'Gültig {decision["valid"]} von {decision["planned"]}; ungültig einschließlich '
             f'blockierter {decision["invalid_including_blocked"]} ({decision["invalid_rate"]:.1%}). '
             f'Format {decision["format_failures"]}, Output-Grenze {decision["limit_failures"]}, '
             f'andere {decision["other_failures"]}, blockiert {decision["blocked"]}, '
             f'nicht versucht {decision["not_attempted"]}.', '',
             '| Nr. | Aufruf | Typ | Ergebnis | Grund | finish | Input | Output | Reasoning | Sekunden |',
             '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |']
    for r in result['records']:
        usage = r.get('usage') or {}
        lines.append('| {index} | {label} | {type} | {outcome} | {reason} | {finish} | {i} | {o} | {z} | {w} |'.format(
            index=r['index'], label=r['label'], type=r['type'], outcome=r['outcome'],
            reason=r['reason'] or '', finish=r.get('finish_reason') or '',
            i=usage.get('input_tokens', ''), o=usage.get('output_tokens', ''),
            z=usage.get('reasoning_output_tokens', '') if usage.get('reasoning_output_tokens') is not None else '',
            w=r.get('wall_seconds') if r.get('wall_seconds') is not None else ''))
    lines += ['', '## Tokenhochrechnung für 192 Aufrufe', '']
    if projection.get('status') == 'computed':
        lines += [f'Kleinstes Verhältnis Zeichen je Token: {projection["chars_per_token_min"]}.',
                  f'Eingabe: {projection["input_tokens"]:,}. Zusätze: {projection["extra_input_tokens"]}.',
                  f'Ausgabe je Typ: {projection["output_tokens_by_type"]} (Basis {projection["output_basis_by_type"]}).',
                  f'**Projektion: {projection["projected_total_tokens"]:,} Tokens** gegenüber Grenze '
                  f'{PROJECTION_LIMIT:,}: {"bestanden" if projection["passes"] else "nicht bestanden"}.',
                  f'Obere Laufzeitschätzung: {projection["runtime_upper_estimate_seconds"] / 3600:.1f} Stunden.']
    else:
        lines.append('Nicht berechenbar: ' + projection.get('reason', ''))
    lines += ['', 'Kein Retry, keine Reparatur, kein Ersatzaufruf. Verbrauch dieses Tests zählt nicht '
              'zum Budget des finalen Laufs.', '']
    return '\n'.join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('command', choices=('plan', 'verify', 'execute'))
    parser.add_argument('--pwsh', type=Path, required=True)
    parser.add_argument('--once', action='store_true')
    args = parser.parse_args(argv)
    plan_path = HERE / 'plan.json'
    if args.command == 'plan':
        if plan_path.exists():
            parser.error('plan.json exists and is never overwritten.')
        plan_path.write_bytes(render_plan(build_plan(args.pwsh)))
        print(json.dumps({'plan_sha256': sha256_bytes(plan_path.read_bytes()), 'model_calls': 0}))
    elif args.command == 'verify':
        same = render_plan(build_plan(args.pwsh)) == plan_path.read_bytes()
        print(json.dumps({'plan_matches': same, 'plan_sha256': sha256_bytes(plan_path.read_bytes()),
                          'approval_present': (HERE / 'approval.json').is_file(),
                          'reserved': (HERE / 'attempt.json').exists(), 'model_calls': 0}))
        if not same:
            raise SystemExit(1)
    else:
        if not args.once:
            parser.error('execute requires --once.')
        result = execute(args.pwsh)
        print(json.dumps(result['decision'], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
