"""Calibration regression: observed output utility does not borrow warrant credit."""

from copy import deepcopy
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'pilots' / 'v03'))
sys.path.insert(0, os.environ.get('GROUNDED_REFLECTION_SRC', str(ROOT / 'src')))

from reflectai_v03.context import render_rules
from reflectai_v03.contracts import Candidate, OutputField, Preparation, WorkOutput
from reflectai_v03.data import build_histories, build_tasks
from reflectai_v03.evaluation import aggregate, calibration_gates, evaluate_output
from reflectai_v03.report import write_report

UTILITY_GATE = 'B_recoverable_world_compliant_at_least_A_plus_2'


def scored_calibration_rows(lucky_a=('S01', 'S04')):
    """Author-reference fixtures only: actually score A guesses without warrant."""
    data = build_tasks(build_histories(3301, 'test_fixture'), task_seed=7301)
    tasks = {task.task_id: task for task in data.tasks}
    histories = {history.history_id: history for history in data.histories}
    truths = {truth.history_id: truth for truth in data.truths}
    rows = []
    for key in data.task_truths:
        task, truth = tasks[key.task_id], truths[key.history_id]
        history = histories[key.history_id]
        reference = Preparation(candidates=[
            Candidate(candidate_id=f'author-reference-{index}', claim='Offline evaluator fixture.',
                      status=target.status, rule=target.rule,
                      evidence_ids=[history.records[0].record_id])
            for index, target in enumerate(truth.candidate_targets)
        ])
        for arm in ('A', 'B', 'C'):
            preparation = reference
            rules = [candidate.rule for candidate in reference.candidates
                     if candidate.status == 'adopt'
                     and candidate.rule.scope.applies_to(task.context) == 'match']
            if arm == 'A':
                rules = ([rule for rule in truth.world_policy.rules
                          if rule.scope.applies_to(task.context) == 'match']
                         if key.probe == 'diagnostic' and truth.scenario_id in lucky_a else [])
            elif key.probe == 'diagnostic' and (
                (arm == 'B' and truth.scenario_id == 'S08')
                or (arm == 'C' and truth.scenario_id == 'S01')
            ):
                # B gets exactly six of seven recoverable outputs; C stays below ceiling.
                preparation, rules = Preparation(), []
            fields = render_rules(task, rules)
            baseline = {field.name: field.value for field in task.baseline_fields}
            output = WorkOutput(task_id=task.task_id, decision='apply' if fields != baseline else 'keep',
                                applied_rules=rules,
                                fields=[OutputField(name=name, value=value) for name, value in fields.items()])
            score = evaluate_output(task, key, truth, output, arm,
                                    preparation if arm == 'C' else None)
            rows.append({'arm': arm, 'scenario_id': truth.scenario_id, 'pair_id': truth.pair_id,
                         'probe': key.probe, 'expected_decision': key.expected_decision,
                         'recoverable': key.recoverable, 'repetition': 0, **score})
    return rows


class CalibrationUtilityTests(unittest.TestCase):
    def test_lucky_A_successes_can_fail_relative_utility_despite_B_warranted_six(self):
        rows = scored_calibration_rows()
        guesses = [row for row in rows if row['arm'] == 'A' and row['probe'] == 'diagnostic'
                   and row['scenario_id'] in ('S01', 'S04')]
        self.assertEqual(len(guesses), 2)
        self.assertTrue(all(row['world_compliant'] and not row['warranted_world_compliant']
                            and not row['update_correct'] for row in guesses))
        result = calibration_gates(rows)
        self.assertEqual(result['scores']['A']['recoverable_world_compliant_deliverables'], 5)
        self.assertEqual(result['scores']['A']['recoverable_warranted_deliverables'], 3)
        self.assertEqual(result['scores']['B']['recoverable_world_compliant_deliverables'], 6)
        self.assertEqual(result['scores']['B']['recoverable_warranted_deliverables'], 6)
        self.assertTrue(result['checks']['B_recoverable_deliverables_at_least_6_of_7'])
        self.assertFalse(result['checks'][UTILITY_GATE])
        self.assertEqual(result['failed_checks'], [UTILITY_GATE])

    def test_exact_two_output_advantage_passes_without_adding_A_warrant(self):
        result = calibration_gates(scored_calibration_rows(lucky_a=('S01',)))
        self.assertTrue(result['passed'], result)
        self.assertEqual(result['scores']['A']['recoverable_world_compliant_deliverables'], 4)
        self.assertEqual(result['scores']['A']['recoverable_warranted_deliverables'], 3)
        self.assertTrue(result['checks'][UTILITY_GATE])

    def test_missing_actual_observation_cannot_make_A_look_worse(self):
        rows = scored_calibration_rows(lucky_a=('S01',))
        row = next(row for row in rows if row['arm'] == 'A' and row['probe'] == 'diagnostic'
                   and row['recoverable'])
        del row['world_compliant']
        result = calibration_gates(rows)
        self.assertFalse(result['passed'])
        self.assertIn('A_recoverable_world_compliant_missing_or_invalid', result['design_errors'])

    def test_truthy_labels_cannot_count_as_actual_world_success(self):
        rows = scored_calibration_rows()
        row = next(row for row in rows if row['arm'] == 'B' and row['probe'] == 'diagnostic'
                   and row['recoverable'] and not row['world_compliant'])
        row['world_compliant'] = 'successful'
        result = calibration_gates(rows)
        self.assertFalse(result['passed'])
        self.assertEqual(result['scores']['B']['recoverable_world_compliant_deliverables'], 6)
        self.assertIn('B_recoverable_world_compliant_missing_or_invalid', result['design_errors'])

    def test_unrecoverable_diagnostic_does_not_enter_either_utility_count(self):
        rows = scored_calibration_rows()
        expected = calibration_gates(rows)
        changed = deepcopy(rows)
        for row in changed:
            if row['probe'] == 'diagnostic' and not row['recoverable']:
                row['world_compliant'] = True
                row['warranted_world_compliant'] = True
        actual = calibration_gates(changed)
        for arm in ('A', 'B', 'C'):
            for key in ('recoverable_world_compliant_deliverables',
                        'recoverable_warranted_deliverables', 'recoverable_total'):
                self.assertEqual(actual['scores'][arm][key], expected['scores'][arm][key])

    def test_report_shows_actual_and_warranted_counts_and_narrow_measurement(self):
        rows = scored_calibration_rows()
        summary = {'config': {'phase': 'calibration'}, 'status': 'completed',
                   'planned_generation_attempts': len(rows), 'budget': {'attempted_calls': 64},
                   'outcomes': aggregate(rows), 'calibration': calibration_gates(rows)}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'REPORT.md'
            write_report(path, summary)
            report = path.read_text(encoding='utf-8')
        self.assertIn('| A | 5/7 | 3/7 |', report)
        self.assertIn('| B | 6/7 | 6/7 |', report)
        self.assertIn('Actual field-compliant | Warranted field-compliant', report)
        self.assertIn('do not establish professional quality', report)
        self.assertIn('World field-compliant', report)


if __name__ == '__main__':
    unittest.main()
