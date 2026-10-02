"""One v0.5 phase: preparations, seal, future tasks, generations, scoring, seal.

Calibration (A, B, C on 8 development histories), the D technical check (D
preparation only, 2 development histories, no scoring) and the main run (A-D on
16 final-test histories). No resumption: an existing output directory is refused.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import random

import pydantic
from reflectai_v03.context import retained_rules
from reflectai_v03.contracts import Preparation, WorkOutput

from .backend import Backend, Stop, write_json
from .config import MAX_OUTPUT_TOKENS, RunConfig
from .data import generate_future_tasks, generate_histories
from .dcontracts import MAX_ROUNDS, Register
from .dquery import build_index, execute
from .oracle import infer, read_frame
from .payloads import (CALL_INPUT_TOKENS, BudgetExceeded, chunk_prompt, consolidation_prompt, d_final_prompt,
                       d_index_prompt, d_round_prompt, d_round_room, generation_prompt)
from .retrieval import coverage
from .scoring import score_task
from .storage import digest, reserve, seal, source_binding, validate_approval

MAX_CALL_TOKENS = CALL_INPUT_TOKENS + MAX_OUTPUT_TOKENS
HARD_TYPES = ('transfer_change', 'unidentifiable')
# Calibration: per setting one transfer and one unidentifiable history, directions alternating.
CALIBRATION_SLOTS = {'K-S': {('transfer_change', 'omit'), ('unidentifiable', 'add')},
                     'K-L': {('transfer_change', 'add'), ('unidentifiable', 'omit')},
                     'U-S': {('transfer_change', 'omit'), ('unidentifiable', 'add')},
                     'U-L': {('transfer_change', 'add'), ('unidentifiable', 'omit')}}
DCHECK_SLOTS = {('U-S', 'transfer_change'), ('U-L', 'unidentifiable')}


def select_cases(config: RunConfig, cases):
    indexed = list(enumerate(cases))
    if config.phase == 'calibration':
        return [(i, c) for i, c in indexed if (c.hard_type, c.direction) in CALIBRATION_SLOTS[c.setting]]
    if config.phase == 'dcheck':
        return [(i, c) for i, c in indexed if (c.setting, c.hard_type) in DCHECK_SLOTS and c.direction == 'omit'] \
            or [(i, c) for i, c in indexed if (c.setting, c.hard_type) in DCHECK_SLOTS][:2]
    return indexed


class PrepBudget:
    """Preparation cap per history and arm; generation is reserved outside it."""

    def __init__(self, cap: int):
        self.cap, self.used = cap, 0

    def add(self, record: dict) -> None:
        self.used += sum((record['usage'][k] or 0) for k in ('input_tokens', 'output_tokens'))

    def can_start_round(self, offline: bool) -> bool:
        if offline:  # mock usage is unknown, never zero; the round limit still applies
            return True
        return self.cap - self.used >= 2 * MAX_CALL_TOKENS


def _parsed(record, contract):
    return contract.model_validate(record['response']) if record and record['status'] == 'completed' else None


def prepare_c(backend, history, folder, offline, cap):
    budget, log = PrepBudget(cap), {'chunks': 0, 'records_unread': 0, 'early_stop': False, 'failure': None}
    remaining = [r for r in history.records if json.loads(r.observation).get('event') != 'register_version']
    previous, index = None, 0
    while remaining:
        if index and not budget.can_start_round(offline):
            log['early_stop'] = True
            break
        prompt, count = chunk_prompt(history, remaining, previous, index)
        record = backend.complete('C1', prompt, folder / f'C1-{index:02d}', call_id=f'{history.history_id}-C1-{index:02d}',
                                  history_id=history.history_id, arm='C')
        budget.add(record)
        parsed = _parsed(record, Preparation)
        if parsed is None:
            log['failure'] = f'C1-{index:02d}'
            return None, log
        previous, remaining, index = parsed, remaining[count:], index + 1
    log['chunks'], log['records_unread'] = index, len(remaining)
    prompt, info = consolidation_prompt(history, previous)
    record = backend.complete('C2', prompt, folder / 'C2', call_id=f'{history.history_id}-C2',
                              history_id=history.history_id, arm='C')
    budget.add(record)
    log.update(info, preparation_tokens=budget.used)
    final = _parsed(record, Preparation)
    if final is None:
        log['failure'] = 'C2'
        return None, log
    try:
        retained_rules(final, history)
    except ValueError:
        log['failure'] = 'C2_reference_invalid'
        return None, log
    return final, log


def prepare_d(backend, history, frame, folder, offline, cap):
    budget = PrepBudget(cap)
    log = {'rounds': 0, 'queries': 0, 'early_stop': False, 'failure': None, 'omitted_for_budget': 0}
    record = backend.complete('D-index', d_index_prompt(history, build_index(history, frame)), folder / 'D-index',
                              call_id=f'{history.history_id}-D-index', history_id=history.history_id, arm='D')
    budget.add(record)
    register = _parsed(record, Register)
    if register is None:
        log['failure'] = 'D-index'
        return None, log, None
    for round_number in range(1, MAX_ROUNDS + 1):
        if not register.queries or register.no_further_discrimination:
            break
        if not budget.can_start_round(offline):
            log['early_stop'] = True
            break
        room = d_round_room(history, register, round_number, MAX_ROUNDS - round_number)
        results = execute(history, register.queries, room)
        log['queries'] += len(register.queries)
        log['omitted_for_budget'] += sum(r['omitted_for_budget'] for r in results)
        prompt = d_round_prompt(history, register, round_number, MAX_ROUNDS - round_number, results)
        record = backend.complete('D-round', prompt, folder / f'D-round-{round_number}',
                                  call_id=f'{history.history_id}-D-round-{round_number}',
                                  history_id=history.history_id, arm='D')
        budget.add(record)
        register = _parsed(record, Register)
        log['rounds'] = round_number
        if register is None:
            log['failure'] = f'D-round-{round_number}'
            return None, log, None
    prompt, cited = d_final_prompt(history, register)
    record = backend.complete('D-final', prompt, folder / 'D-final', call_id=f'{history.history_id}-D-final',
                              history_id=history.history_id, arm='D')
    budget.add(record)
    log.update(final_cited_records=cited, preparation_tokens=budget.used)
    final = _parsed(record, Preparation)
    if final is None:
        log['failure'] = 'D-final'
        return None, log, register
    try:
        retained_rules(final, history)
    except ValueError:
        log['failure'] = 'D-final_reference_invalid'
        return None, log, register
    return final, log, register


def headroom(rows) -> dict:
    """No headroom only if the better of B and C solves every hard calibration diagnostic in every setting."""
    by_setting = defaultdict(lambda: defaultdict(list))
    for row in rows:
        if row['task_type'] in HARD_TYPES and row['arm'] in ('B', 'C'):
            by_setting[row['setting']][row['arm']].append(row['correct'])
    settings = {}
    for setting, arms in sorted(by_setting.items()):
        best = max(sum(v) for v in arms.values())
        total = max(len(v) for v in arms.values())
        settings[setting] = {'best_of_B_C_hard_correct': best, 'hard_total': total, 'ceiling': best == total}
    no_headroom = bool(settings) and all(s['ceiling'] for s in settings.values())
    return {'settings': settings, 'no_headroom': no_headroom,
            'consequence': ('amendment permitted before D sees v0.5 data' if no_headroom
                            else 'main run follows; E3 evaluated descriptively in all settings')}


def run(output_dir: Path, config: RunConfig, *, allow_live: bool = False, approval: dict | None = None,
        failures: dict | None = None) -> dict:
    output_dir = Path(output_dir)
    binding = source_binding()
    config_sha = digest(config.model_dump())
    if config.is_live:
        if not allow_live or approval is None:
            raise PermissionError('live execution requires an explicit, matching approval')
        validate_approval(approval, phase=config.phase, config_sha256=config_sha, source_sha256=binding['sha256'])
        from .preflight import verify_executable
        verify_executable(config)
    backend = Backend(config, allow_live=allow_live, failures=failures)
    output_dir.mkdir(parents=True, exist_ok=False)
    if config.is_live:
        write_json(output_dir / 'authorization-reservation.json', reserve(approval, output_dir))
    write_json(output_dir / 'config.json', {**config.model_dump(), 'config_sha256': config_sha})
    write_json(output_dir / 'runtime.json', {'python': platform.python_version(), 'pydantic': pydantic.VERSION,
                                            'source_sha256': binding['sha256']})
    write_json(output_dir / 'source-binding.json', binding)
    cases = generate_histories(config.history_seed, config.split)
    selected = select_cases(config, cases)
    prepared, private = output_dir / 'preparation', output_dir / 'evaluator'
    prepared.mkdir()
    private.mkdir()
    write_json(private / 'cases.json', [c.model_dump(mode='json') for _, c in selected])
    write_json(prepared / 'histories.json', [c.history.model_dump(mode='json') for _, c in selected])
    preparations, prep_logs, registers = {}, {}, {}
    order = list(selected)
    random.Random(config.order_seed).shuffle(order)
    offline = not config.is_live
    try:
        for _, case in order:
            hid = case.history.history_id
            frame = read_frame(case.history)
            if 'C' in config.arms:
                preparations[(hid, 'C')], prep_logs[(hid, 'C')] = prepare_c(
                    backend, case.history, prepared / hid / 'C', offline, config.preparation_cap)
            if 'D' in config.arms:
                result, log, register = prepare_d(backend, case.history, frame, prepared / hid / 'D', offline,
                                                  config.preparation_cap)
                preparations[(hid, 'D')], prep_logs[(hid, 'D')] = result, log
                registers[hid] = register.model_dump(mode='json') if register else None
    except (Stop, BudgetExceeded) as stop:
        backend.halt_reason = backend.halt_reason or f'{type(stop).__name__}: {stop}'
    write_json(prepared / 'retained.json', {f'{h}|{a}': p.model_dump(mode='json') if p else None
                                           for (h, a), p in preparations.items()})
    write_json(prepared / 'logs.json', {f'{h}|{a}': log for (h, a), log in prep_logs.items()})
    write_json(prepared / 'registers.json', registers)
    prep_seal = seal(prepared, prepared / 'manifest.json')

    rows = []
    if config.phase != 'dcheck':
        tasks = {c.history.history_id: generate_future_tasks(c, config.future_seed + i) for i, c in selected}
        write_json(private / 'future-tasks.json', {h: [{'task': t.model_dump(mode='json'), 'truth': tr.model_dump(mode='json')}
                                                      for t, tr in pairs] for h, pairs in tasks.items()})
        seal(private, private / 'manifest.json')
        schedule = [(case, task, truth, arm) for _, case in selected for task, truth in tasks[case.history.history_id]
                    for arm in config.arms]
        random.Random(config.order_seed + 1).shuffle(schedule)
        generation = output_dir / 'generation'
        for case, task, truth, arm in schedule:
            hid = case.history.history_id
            row = {'setting': case.setting, 'family': case.family, 'hard_type': case.hard_type,
                   'direction': case.direction, 'history_id': hid, 'arm': arm, 'task_type': truth.task_type,
                   'task_id': task.task_id, 'call_status': 'blocked', 'blocked_reason': None}
            output = None
            if backend.halt_reason:
                row['blocked_reason'] = backend.halt_reason
            elif arm in ('C', 'D') and preparations.get((hid, arm)) is None:
                row['blocked_reason'] = f'{arm}_preparation_unavailable'
            else:
                try:
                    prompt, info = generation_prompt(arm, task, case.history, read_frame(case.history),
                                                     preparations.get((hid, arm)))
                    record = backend.complete('generate', prompt, generation / f'{hid}-{truth.task_type}-{arm}',
                                              call_id=f'{hid}-{truth.task_type}-{arm}', history_id=hid, arm=arm)
                    row['call_status'] = record['status']
                    row['usage'] = record['usage']
                    output = _parsed(record, WorkOutput)
                    if arm == 'B':
                        row['coverage'] = coverage([r for r in case.history.records
                                                    if r.record_id in set(info['selected_record_ids'])],
                                                   infer(case.history).binding_records)
                except Stop as stop:
                    row['blocked_reason'] = str(stop)
                except (BudgetExceeded, ValueError) as error:
                    row['blocked_reason'] = f'payload: {error}'
            rows.append({**row, **score_task(task, truth, output)})
    summary = summarise(rows, backend, prep_logs, config)
    write_json(output_dir / 'calls.json', backend.records)
    write_json(output_dir / 'results.json', {'rows': rows, 'summary': summary,
                                             'preparation_seal': prep_seal['sha256'],
                                             'finished_at': datetime.now(timezone.utc).isoformat()})
    (output_dir / 'REPORT.md').write_text(render_report(summary, config), encoding='utf-8')
    manifest = seal(output_dir, output_dir / 'manifest.json')
    return {'summary': summary, 'manifest_sha256': manifest['sha256']}


def summarise(rows, backend, prep_logs, config) -> dict:
    table = defaultdict(lambda: [0, 0])
    for row in rows:
        key = f"{row['setting']}|{row['arm']}|{row['task_type']}"
        table[key][0] += int(row['correct'])
        table[key][1] += 1
    tokens = Counter()
    for record in backend.records:
        tokens[f"{record['arm']}|{record['stage']}"] += sum((record['usage'][k] or 0) for k in ('input_tokens', 'output_tokens'))
    result = {'phase': config.phase, 'budget': backend.summary(),
              'correct': {key: f'{hits}/{total}' for key, (hits, total) in sorted(table.items())},
              'tokens_by_arm_stage': dict(sorted(tokens.items())),
              'preparation_logs': {f'{h}|{a}': log for (h, a), log in prep_logs.items()},
              'complete': backend.halt_reason is None}
    if config.phase == 'calibration':
        result['headroom'] = headroom(rows)
    return result


def render_report(summary: dict, config: RunConfig) -> str:
    lines = [f"# Pilot v0.5 {config.phase} ({config.backend})", '',
             'Primary outcome: decision implied by the executed output fields. Mock runs test the pipeline only.', '',
             f"Calls: {summary['budget']['attempted_calls']}, reported tokens: {summary['budget']['reported_tokens']}, "
             f"halt: {summary['budget']['halt_reason']}.", '', '| Setting | Arm | Task type | Correct |',
             '| --- | --- | --- | ---: |']
    for key, value in summary['correct'].items():
        setting, arm, task_type = key.split('|')
        lines.append(f'| {setting} | {arm} | {task_type} | {value} |')
    if 'headroom' in summary:
        h = summary['headroom']
        lines += ['', f"Headroom decision: no headroom = {h['no_headroom']} ({h['consequence']})."]
    return '\n'.join(lines) + '\n'
