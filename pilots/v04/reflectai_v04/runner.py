"""One frozen A/B/C schedule. Future tasks follow the preparation seal."""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import random
import traceback

import pydantic
from reflectai_v03.context import retained_rules
from reflectai_v03.contracts import Preparation, WorkOutput

from .backend import Backend, BudgetStop, verify_executable, write_json
from .config import (DEVELOPMENT_FUTURE_SEED, DEVELOPMENT_HISTORY_SEED, MATERIAL_REVISION,
                     REVIEW_FUTURE_SEED, REVIEW_HISTORY_SEED, RunConfig)
from .data import ALLOCATION, FAMILIES, TASK_TYPE_ALLOCATION, generate_future_tasks, generate_histories
from .evaluation import METRICS, aggregate, amortisation, classify_error, score_output, score_preparation
from .payloads import generation_payload, preparation_payload, prompt_for
from .report import write_report
from .storage import (assert_sources, digest, file_hash, seal, snapshot_sources, source_binding,
                      validate_approvals, verify_seal)


def _load_completed(record: dict | None, contract):
    if not record or record['status'] != 'completed':
        return None
    return contract.model_validate(record['response'])


def _slots(cases=()) -> list[dict]:
    """Register the design even when no material could be constructed."""
    by_cell = {(case.setting, case.family): case for case in cases}
    return [{'setting': setting, 'family': family, 'regime': regimes[index],
             'task_type': TASK_TYPE_ALLOCATION[setting][index],
             'slot_id': f'{setting}-{family}',
             'history_id': (by_cell[(setting, family)].history.history_id
                            if (setting, family) in by_cell else f'planned-{setting}-{family}'),
             'material_available': (setting, family) in by_cell}
            for setting, regimes in ALLOCATION.items() for index, family in enumerate(FAMILIES)]


def _schedule(slots: list[dict]) -> list[dict]:
    result = []
    for slot in slots:
        hid = slot['history_id']
        result.extend({**slot, 'call_id': f'{hid}-{phase}', 'arm': 'C',
                       'phase': phase, 'probe': None} for phase in ('C1', 'C2'))
        result.extend({**slot, 'call_id': f'{hid}-{probe}-{arm}', 'arm': arm,
                       'phase': 'generate', 'probe': probe}
                      for probe in ('diagnostic', 'control') for arm in ('A', 'B', 'C'))
    return result


def _reserve_live_authorization(pilot: Path, approval: dict, output_dir: Path) -> dict:
    """Atomically consume an approval, independently of filename or output path.

    The central registry is outside the version-bound source file set. A stopped
    attempt keeps its reservation; only a separately documented approval permits
    another attempt. This never creates or modifies a human approval.
    """
    approval_hash = digest(approval)
    folder = pilot / '.authorizations'
    folder.mkdir(parents=True, exist_ok=True)
    reservation = {'approval_sha256': approval_hash,
                   'source_sha256': approval['source_sha256'],
                   'material_sha256': approval['material_sha256'],
                   'config_sha256': approval['live']['config_sha256'],
                   'output_dir': str(output_dir.resolve()),
                   'reserved_at': datetime.now(timezone.utc).isoformat()}
    path = folder / f'{approval_hash}.json'
    try:
        with path.open('x', encoding='utf-8') as stream:
            json.dump(reservation, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.flush()
            os.fsync(stream.fileno())
    except FileExistsError as exc:
        raise ValueError('This live approval was already reserved; a new documented approval is required.') from exc
    return {**reservation, 'reservation_path': str(path.resolve())}


def _frozen_prompt(stage: str, payload: dict, snapshot: Path, binding: dict) -> str:
    """Read the snapshot and verify the exact prompt bytes used by a call."""
    names = {'C1': 'prepare_C_v1.txt', 'C2': 'review_C_v1.txt', 'generate': 'generate_v1.txt'}
    relatives = [f'pilots/v04/prompts/{name}'
                 for name in (names[stage], 'shared_contract_v1.txt')]

    def verify():
        for relative in relatives:
            if file_hash(snapshot / relative) != binding['files'][relative]:
                raise ValueError('A frozen prompt differs from its source binding.')

    verify()
    prompt = prompt_for(stage, payload, snapshot / 'pilots/v04/prompts')
    verify()
    return prompt


def _complete_blocked_rows(slots, cases, tasks, prep_rows, generation_rows, calls, reason):
    """Keep all planned denominators without inventing missing tasks or truth."""
    by_history = {case.history.history_id: case for case in cases}
    by_call = {record['call_id']: record for record in calls}
    prep_keys = {(row['history_id'], row['phase']) for row in prep_rows}
    output_keys = {(row['history_id'], row['arm'], row['probe']) for row in generation_rows}
    for slot in slots:
        hid = slot['history_id']
        case = by_history.get(hid)
        for phase in ('C1', 'C2'):
            if (hid, phase) in prep_keys:
                continue
            analysis = (score_preparation(case.history, case.truth, None,
                                          task_type=case.material_audit['task_type']) if case else {
                'history_id': hid, 'preparation_present': False, 'candidate_count': None,
                'candidates': [], 'content_error_count': 0, 'content_error_rate': None,
                'assessable_count': 0, 'unassessable_count': 0, 'technical_candidate_count': 0})
            record = by_call.get(f'{hid}-{phase}')
            prep_rows.append({**slot, 'phase': phase, 'analysis': analysis,
                              'call_status': record['status'] if record else 'blocked',
                              'blocked': True, 'blocking_reason': reason})
        available = {truth.probe: (task, truth) for task, truth in tasks.get(hid, [])}
        for probe in ('diagnostic', 'control'):
            for arm in ('A', 'B', 'C'):
                if (hid, arm, probe) in output_keys:
                    continue
                task, truth = available.get(probe, (None, None))
                # Missing output fails even when baseline retention was warranted.
                # Missing material has no invented expected decision or world truth.
                score = {metric: False for metric in METRICS}
                score.update(errors=['missing_or_invalid_output'], effective_decision=None)
                record = by_call.get(f'{hid}-{probe}-{arm}')
                row = {**slot, **score, 'arm': arm, 'probe': probe,
                       'task_id': task.task_id if task else None,
                       'task_material_available': task is not None,
                       'expected_decision': truth.expected_decision if truth else None,
                       'recoverable': truth.recoverable if truth else None,
                       'call_status': record['status'] if record else 'blocked',
                       'blocked': True, 'blocking_reason': reason}
                row['error_attribution'] = classify_error(score, call_status='blocked')
                generation_rows.append(row)


def run(output_dir: Path, config: RunConfig, *, repo: Path, pilot: Path,
        protocol: Path, allow_live: bool = False, review_dir: Path | None = None,
        approval_path: Path | None = None, failures: dict | None = None) -> dict:
    """Never resume an output directory; stopped attempts retain the whole ledger.

    Approval validation remains a preflight gate. Once an attempt starts, source,
    stage-seal and material failures terminate it with all planned denominators.
    """
    output_dir, repo, pilot, protocol = map(Path, (output_dir, repo, pilot, protocol))
    binding = source_binding(repo, pilot, protocol)
    approvals = None
    if config.is_live:
        if not allow_live or review_dir is None or approval_path is None:
            raise ValueError('Material review and separate live approval are required.')
        review_dir = Path(review_dir)
        review_seal = verify_seal(review_dir, review_dir / 'manifest.json')
        review_index = json.loads((review_dir / 'index.json').read_text(encoding='utf-8'))
        if (review_index.get('material_revision') != MATERIAL_REVISION
                or review_index.get('source_sha256') != binding['sha256']):
            raise ValueError('Live execution requires newly reviewed materials from this frozen revision.')
        approvals = json.loads(Path(approval_path).read_text(encoding='utf-8'))
        validate_approvals(approvals, source_hash=binding['sha256'],
                           material_hash=review_seal['sha256'], config=config.model_dump())
        if (config.history_seed in (4401, 4411, DEVELOPMENT_HISTORY_SEED, REVIEW_HISTORY_SEED)
                or config.future_seed in (4402, 4412, DEVELOPMENT_FUTURE_SEED, REVIEW_FUTURE_SEED)):
            raise ValueError('Live seeds must differ from registered offline/review seeds.')
        verify_executable(config)
    backend = Backend(config, allow_live=allow_live, failures=failures)
    output_dir.mkdir(parents=True, exist_ok=False)
    write_json(output_dir / 'config.json', config.model_dump())
    write_json(output_dir / 'runtime.json', {'python': platform.python_version(),
                                          'pydantic': pydantic.__version__})
    slots, cases, tasks_by_history = _slots(), [], {}
    prep_rows, generation_rows = [], []
    preparations, preparation_errors = {}, {}
    write_json(output_dir / 'planned-calls.json', _schedule(slots))
    prepared, private = output_dir / 'preparation', output_dir / 'evaluator'
    prepared.mkdir()
    private.mkdir()
    snapshot_dir = output_dir / 'sources'
    terminal_error = None
    stage = 'authorization_reservation'

    def check_sources():
        nonlocal stage
        stage = 'source_verification'
        assert_sources(binding, repo, pilot, protocol)

    def call(payload, schema, phase, arm, case, parent, probe=None):
        nonlocal stage
        check_sources()
        stage = 'snapshot_prompt_verification'
        prompt = _frozen_prompt(phase, payload, snapshot_dir, binding)
        hid = case.history.history_id
        call_id = f'{hid}-{phase}' if phase != 'generate' else f'{hid}-{probe}-{arm}'
        stage = f'call:{call_id}'
        try:
            return backend.complete(prompt, schema, parent / call_id, call_id=call_id,
                                    history_id=hid, arm=arm, phase=phase, probe=probe)
        except BudgetStop:
            return None

    try:
        if approvals is not None:
            reservation = _reserve_live_authorization(pilot, approvals, output_dir)
            write_json(output_dir / 'authorization-reservation.json', reservation)
        stage = 'source_snapshot'
        snapshot = snapshot_sources(snapshot_dir, repo, pilot, protocol)
        if snapshot != binding:
            raise ValueError('Source changed during snapshot.')
        stage = 'history_material_generation'
        split = 'development' if config.backend == 'mock' else 'final_test'
        cases = generate_histories(config.history_seed, split=split)
        if (len(cases) != 24 or len({c.history.history_id for c in cases}) != 24
                or {(c.setting, c.family, c.regime, c.material_audit['task_type']) for c in cases}
                != {(s['setting'], s['family'], s['regime'], s['task_type']) for s in slots}):
            raise ValueError('The fixed design requires its 24 distinct allocated histories.')
        slots = _slots(cases)
        write_json(output_dir / 'planned-calls.json', _schedule(slots))
        if config.is_live:
            review_ids = set(review_index['history_ids'])
            if review_ids & {case.history.history_id for case in cases}:
                raise ValueError('Live and reviewed development histories overlap.')
        write_json(private / 'cases.json', [case.model_dump(mode='json') for case in cases])
        write_json(prepared / 'histories.json', [case.history.model_dump(mode='json') for case in cases])
        order = list(cases)
        random.Random(config.order_seed).shuffle(order)
        for case in order:
            hid = case.history.history_id
            previous, preparation_error = None, None
            for phase in ('C1', 'C2'):
                record = None
                if phase == 'C1' or previous is not None:
                    record = call(preparation_payload(case.history, previous), Preparation,
                                  phase, 'C', case, prepared / 'calls')
                current = _load_completed(record, Preparation)
                stage = 'preparation_scoring'
                analysis = score_preparation(case.history, case.truth, current,
                                             task_type=case.material_audit['task_type'])
                prep_rows.append({'setting': case.setting, 'history_id': hid, 'phase': phase,
                                  'family': case.family, 'regime': case.regime,
                                  'task_type': case.material_audit['task_type'],
                                  'control_basis': case.material_audit['control_basis'],
                                  'call_status': record['status'] if record else 'blocked',
                                  'blocked': record is None,
                                  'blocking_reason': (backend.halt_reason or 'missing_C1') if record is None else None,
                                  'analysis': analysis})
                if current is not None:
                    try:
                        retained_rules(current, case.history)
                    except ValueError as exc:
                        preparation_error = str(exc)
                        # C1 remains available to the scheduled review; invalid C2
                        # references cannot become runtime instructions.
                        if phase == 'C2':
                            current = None
                            backend.register_reference_failure(record['call_id'])
                previous = current
            preparations[hid] = previous
            preparation_errors[hid] = preparation_error if previous is None else None
        write_json(prepared / 'retained.json', {
            hid: prep.model_dump(mode='json') if prep else None for hid, prep in preparations.items()})
        write_json(prepared / 'validation-errors.json', preparation_errors)
        write_json(prepared / 'analysis.json', prep_rows)
        stage = 'preparation_seal'
        prep_seal = seal(prepared, prepared / 'manifest.json')
        write_json(output_dir / 'F1.json', {'source_sha256': binding['sha256'],
                                          'preparation_sha256': prep_seal['sha256'],
                                          'sealed_at': datetime.now(timezone.utc).isoformat()})
        check_sources()
        stage = 'preparation_seal_verification'
        verify_seal(prepared, prepared / 'manifest.json')

        # No future task instance exists before the preparation seal is verified.
        for index, case in enumerate(cases):
            stage = 'future_material_generation'
            future = generate_future_tasks(case, config.future_seed + index)
            if sorted(truth.probe for _, truth in future) != ['control', 'diagnostic']:
                raise ValueError('Each history requires one diagnostic and one control.')
            tasks_by_history[case.history.history_id] = future
            # Preserve partial material if a later fixed seed cannot generate.
            write_json(private / 'future-tasks.json', {
                hid: [{'task': task.model_dump(mode='json'), 'truth': truth.model_dump(mode='json')}
                      for task, truth in pairs] for hid, pairs in tasks_by_history.items()})
        stage = 'evaluator_seal'
        seal(private, private / 'manifest.json')
        future_schedule = [(case, task, truth, arm) for case in cases
                           for task, truth in tasks_by_history[case.history.history_id]
                           for arm in ('A', 'B', 'C')]
        random.Random(config.order_seed + 1).shuffle(future_schedule)
        prep_lookup = {(row['history_id'], row['phase']): row['analysis'] for row in prep_rows}
        for case, task, truth, arm in future_schedule:
            hid = case.history.history_id
            prep = preparations[hid] if arm == 'C' else None
            record, payload_error = None, None
            if arm != 'C' or prep is not None:
                try:
                    payload = generation_payload(task, case.history, arm, prep)
                except ValueError as exc:
                    payload_error = str(exc)
                else:
                    record = call(payload, WorkOutput, 'generate', arm, case,
                                  output_dir / 'generation', truth.probe)
            output = _load_completed(record, WorkOutput)
            stage = 'output_scoring'
            score = score_output(task, truth, case.truth, output, arm, prep,
                                 history=case.history, task_type=case.material_audit['task_type'])
            status = record['status'] if record else 'blocked'
            attribution = classify_error(score, prep_lookup[(hid, 'C2')] if arm == 'C' else None,
                                         call_status=status)
            generation_rows.append({'setting': case.setting, 'family': case.family,
                                    'regime': case.regime, 'history_id': hid, 'arm': arm,
                                    'task_type': case.material_audit['task_type'],
                                    'control_basis': case.material_audit['control_basis'],
                                    'probe': truth.probe, 'task_id': task.task_id,
                                    'expected_decision': truth.expected_decision,
                                    'call_status': status, 'payload_error': payload_error,
                                    'blocked': record is None,
                                    'blocking_reason': (backend.halt_reason or payload_error or 'missing_C_preparation') if record is None else None,
                                    'preparation_error': preparation_errors[hid] if arm == 'C' else None,
                                    **score, 'error_attribution': attribution})
        check_sources()
        stage = 'preparation_seal_verification'
        verify_seal(prepared, prepared / 'manifest.json')
        stage = 'evaluator_seal_verification'
        verify_seal(private, private / 'manifest.json')
    except Exception as exc:
        terminal_error = {'stage': stage, 'exception_type': type(exc).__name__,
                          'message': str(exc), 'traceback': traceback.format_exc(),
                          'stopped_at': datetime.now(timezone.utc).isoformat()}
        write_json(output_dir / 'terminal-error.json', terminal_error)

    reason = terminal_error['stage'] if terminal_error else backend.halt_reason or 'unavailable_scheduled_call'
    _complete_blocked_rows(slots, cases, tasks_by_history, prep_rows, generation_rows,
                           backend.records, reason)
    write_json(output_dir / 'calls.json', backend.records)
    write_json(output_dir / 'scores.json', generation_rows)
    write_json(output_dir / 'candidate-scores.json', prep_rows)
    result = aggregate(generation_rows, prep_rows)
    if terminal_error:
        result['design_valid'] = False
        result['design_errors'].append('terminal_run_failure:' + terminal_error['stage'])
        for headroom in result['headroom'].values():
            headroom.update(qualifies=None, provisional=True, conservative_flag=False)
    complete = (terminal_error is None and len(backend.records) == 192
                and all(r['status'] == 'completed' for r in backend.records))
    result.update({'protocol': 'pilot-v0.4', 'offline': config.backend == 'mock',
                   'material_revision': MATERIAL_REVISION,
                   'origin': 'offline_mock' if config.backend == 'mock' else 'model_generated',
                   'report_type': 'CompleteReport' if complete else 'IncompleteReport',
                   'status': 'complete' if complete else 'incomplete',
                   'terminal_error': terminal_error, 'planned_calls': 192,
                   'budget': backend.budget_summary(), 'complete_schedule': complete,
                   'blocked_generation_rows': sum(row.get('blocked', False) for row in generation_rows),
                   'blocked_preparation_rows': sum(row.get('blocked', False) for row in prep_rows),
                   'amortisation': amortisation(backend.records),
                   'source_sha256': binding['sha256'], 'human_output_review': 'pending'})
    result['material_audits'] = [
        {'history_id': case.history.history_id, 'setting': case.setting, 'family': case.family,
         'task_type': case.material_audit['task_type'],
         'control_basis': case.material_audit['control_basis'],
         'counterfactual': case.material_audit['counterfactual']}
        for case in cases]
    write_json(output_dir / 'results.json', result)
    if not complete:
        write_json(output_dir / 'incomplete-report.json', result)
    write_report(output_dir / 'REPORT.md', result, offline=config.backend == 'mock')
    _human_sample(output_dir, generation_rows, backend.records, cases, tasks_by_history,
                  order_seed=config.order_seed + 2)
    seal(output_dir, output_dir / 'manifest.json')
    return result


def _human_sample(directory: Path, rows: list[dict], calls: list[dict], cases,
                  tasks_by_history: dict, *, order_seed: int) -> None:
    """Public evidence and responses for semantic review; design key stays separate."""
    by_id = {call['call_id']: call for call in calls}
    histories = {case.history.history_id: case.history for case in cases}
    tasks = {task.task_id: task for pairs in tasks_by_history.values() for task, _ in pairs}
    sample, key = [], []
    selected = [row for row in rows if row['arm'] == 'C' and row['probe'] == 'diagnostic']
    # Neither presentation order nor the sample ID encodes the setting allocation.
    selected.sort(key=lambda row: row['history_id'])
    random.Random(order_seed).shuffle(selected)
    for index, row in enumerate(selected):
        sample_id = f'case-{index + 1:02d}'
        hid = row['history_id']
        history, task = histories.get(hid), tasks.get(row['task_id'])
        call = by_id.get(f'{hid}-diagnostic-C', {})
        preparations = {f'preparation_{index}': by_id.get(f'{hid}-{phase}', {}).get('response')
                        for index, phase in enumerate(('C1', 'C2'), 1)}
        sample.append({'sample_id': sample_id,
                       'history': history.model_dump(mode='json') if history else None,
                       'task': task.model_dump(mode='json') if task else None,
                       'preparations': preparations, 'response': call.get('response'),
                       'masking': 'Design labels withheld; procedure may be inferable from preparation structure.',
                       'review_status': 'pending', 'human_response': None})
        key.append({'sample_id': sample_id, 'history_id': hid,
                    'setting': row['setting'], 'family': row['family'], 'regime': row['regime'],
                    'task_type': row['task_type'],
                    'arm': row['arm'], 'probe': row['probe'], 'task_id': row['task_id']})
    folder = directory / 'human_review'
    folder.mkdir()
    write_json(folder / 'blinded-outputs.json', sample)
    write_json(folder / 'key.json', key)
