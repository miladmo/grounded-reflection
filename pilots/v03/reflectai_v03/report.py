"""Small, explicit reporting helpers. Mock output is never research evidence."""

import random
from pathlib import Path

from .storage import write_json


def write_report(path: Path, summary: dict) -> None:
    offline = summary['config']['phase'] == 'offline'
    lines = ['# Pilot v0.3 offline integration report' if offline else '# Pilot v0.3 results', '',
             '**OFFLINE MOCK. No inference, calibration or efficacy evidence.**' if offline else
             '**Synthetic pilot. Not enterprise validation or evidence of recursive improvement.**', '',
             f"Run status: {summary['status']}",
             f"Planned generation attempts: {summary['planned_generation_attempts']}",
             f"Logical calls attempted: {summary['budget']['attempted_calls']}", '',
             '## Outcomes', '',
             'Update decisions and synthetic world field compliance are separate. Diagnostic probes '
             'and controls are not pooled. All planned attempts remain in the denominator.', '',
             'A is judged against current-task information only. Its update-warrant score '
             'is not directly comparable with B/C/D, which are judged against the shared '
             'history. Downstream field compliance uses the same synthetic world obligations. '
             'A completed deliverable is a decoded output for the correct task, marked completed '
             'and containing no employee questions. Field compliance additionally requires the '
             'expected fields and values, independently of rule and decision-label metadata. '
             'Update warrant also requires consistent execution and supported rule scope. These checks '
             'do not establish professional quality or successful real-world execution.', '',
             'Detailed outcomes are in results.json. Raw requests, responses and failures '
             'are retained in calls/. Candidate metrics are in candidate_scores.json.', '',
             '## Interpretation', '',
             'The mock copies the baseline and learns no requirements. Its scores only '
             'exercise the pipeline.' if offline else
             'Compare D against strong C first. Inspect missed updates and harmful generalisation '
             'alongside correct retention. A result at ceiling cannot establish equivalence.', '',
             '## Limitations', '',
             'Four designed pairs, eight dependent history variants, a bounded hypothesis class, '
             'synthetic outputs and no real tool execution. No human spot-check results are '
             'assumed. Model sampling may be nondeterministic. Logical-call limits do not '
             'enforce equal computation or a hard token cap.', '',
             '## Human checks', '',
             'The blinded sample and separate key are prepared for later review. '
             'An exported review sheet is not a completed review.', '']
    outcomes = summary['outcomes']['by_arm']
    table = ['## Diagnostic results', '',
             '| Arm | Justified decisions | Change cases | Retention cases | World field-compliant | Controls justified |',
             '| --- | --- | --- | --- | --- | --- |']
    for arm, result in outcomes.items():
        diagnostic, control = result['diagnostic'], result['control']
        if not diagnostic['n']:
            continue
        change, keep = diagnostic['by_expected_decision']['apply'], diagnostic['by_expected_decision']['keep']
        table.append(f"| {arm} | {diagnostic['update_correct']}/{diagnostic['n']} | "
                     f"{change['update_correct']}/{change['n']} | {keep['update_correct']}/{keep['n']} | "
                     f"{diagnostic['world_compliant']}/{diagnostic['n']} | "
                     f"{control['update_correct']}/{control['n']} |")
    table.extend(['', 'All per-variant, paired and repetition summaries are retained in results.json.', ''])
    lines.extend(table)
    if summary.get('design_revision'):
        lines.extend(['## Measurement contract', '',
                      f"Design revision: {summary['design_revision']}", '',
                      'The effective update is derived from the output fields and baseline. '
                      'A declared decision mismatch is reported separately. Strict output validity '
                      'can therefore fail even when actual field compliance or update warrant passes.', '',
                      '| Arm | Declared decision mismatches | Execution checks failed |',
                      '| --- | --- | --- |'])
        for arm in outcomes:
            rows = [row for row in summary['rows'] if row['arm'] == arm]
            label_errors = sum('declared_decision_disagrees_with_fields' in row.get('errors', [])
                               for row in rows)
            execution_errors = sum(row.get('execution_consistent') is False for row in rows)
            lines.append(f'| {arm} | {label_errors}/{len(rows)} | {execution_errors}/{len(rows)} |')
        lines.extend(['', 'Both diagnostic and control attempts are included only in this contract table. '
                      'These counts do not replace the separate scientific outcomes.', ''])
    calibration = summary.get('calibration', {})
    if calibration.get('scores'):
        lines.extend([
            '## Calibration utility', '',
            'The fixed recoverable subset contains seven diagnostic cases. The absolute B floor '
            'requires at least six warranted, field-compliant deliverables. The separate B-minus-A '
            'gate requires at least two more actual field-compliant deliverables; a lucky A output '
            'counts here even when its update lacks warrant. These are selection gates, not '
            'validation of professional quality.', '',
            '| Arm | Actual field-compliant | Warranted field-compliant |',
            '| --- | --- | --- |',
        ])
        for arm, scores in calibration['scores'].items():
            total = scores['recoverable_total']
            actual = scores.get('recoverable_world_compliant_deliverables', 'unavailable')
            warranted = scores['recoverable_warranted_deliverables']
            lines.append(f'| {arm} | {actual}/{total} | {warranted}/{total} |')
        lines.extend(['', f"Calibration gates passed: {calibration['passed']}", ''])
    if summary.get('error'):
        lines.extend(['## Run failure', '', summary['error'], ''])
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write('\n'.join(lines))


def export_blinded_sample(run_dir: Path, dataset, rows: list[dict], outputs: dict,
                          seed: int, limit: int = 16) -> None:
    tasks = {task.task_id: task for task in dataset.tasks}
    histories = {history.history_id: history for history in dataset.histories}
    membership = {truth.task_id: truth.history_id for truth in dataset.task_truths}
    eligible = [row for row in rows if row.get('task_id') in tasks]
    random.Random(seed).shuffle(eligible)
    sample, key = [], []
    for index, row in enumerate(eligible[:limit]):
        label = f'review-{index + 1:03d}'
        output_key = f"{row['arm']}-{row['repetition']}-{row['task_id']}"
        task = tasks[row['task_id']]
        output = outputs.get(output_key)
        sample.append({'review_id': label, 'task': task.model_dump(mode='json'),
                       'history': histories[membership[task.task_id]].model_dump(mode='json'),
                       'output': output, 'human_assessment': None})
        key.append({'review_id': label, 'arm': row['arm'], 'repetition': row['repetition'],
                    'task_id': row['task_id'], 'scenario_id': row['scenario_id'],
                    'automated_scores': row})
    write_json(run_dir / 'human_review/sample.json', sample)
    write_json(run_dir / 'evaluator/blind_key.json', key)
