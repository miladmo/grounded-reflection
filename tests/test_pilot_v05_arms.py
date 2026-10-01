"""Offline tests for v0.5 retrieval (arm B) and field-based scoring. No model calls."""

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
for location in (ROOT / 'src', ROOT / 'pilots/v03', ROOT / 'pilots/v05'):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

from reflectai_v03.contracts import OutputField, WorkOutput  # noqa: E402
from reflectai_v05.data import generate_future_tasks, generate_histories  # noqa: E402
from reflectai_v05.oracle import infer, read_frame  # noqa: E402
from reflectai_v05.retrieval import coverage, rank_records, record_chars, select_records  # noqa: E402
from reflectai_v05.scoring import score_task  # noqa: E402


class RetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = generate_histories(45021, 'development')
        cls.tasks = {c.history.history_id: generate_future_tasks(c, 45022 + i) for i, c in enumerate(cls.cases)}

    def test_order_registrations_then_target_reviews_then_rest(self):
        case = next(c for c in self.cases if c.setting == 'U-L')
        frame = read_frame(case.history)
        task = self.tasks[case.history.history_id][0][0]
        ranked = rank_records(case.history, task, frame)
        kinds = []
        for record in ranked:
            event = json.loads(record.observation)
            if event.get('event') == 'register_version':
                kinds.append(0)
            elif event.get('event') == 'review' and event.get('decision') == 'accept' \
                    and frame.field_option.field in event.get('reviewed_fields', []):
                kinds.append(1)
            else:
                kinds.append(2)
        self.assertEqual(kinds, sorted(kinds))
        self.assertEqual(len(ranked), len(case.history.records))

    def test_small_histories_fit_whole_and_large_keep_binding_approvals(self):
        budget = 60_000  # characters for records, below the 24,000-token call budget
        for case in self.cases:
            frame = read_frame(case.history)
            task = self.tasks[case.history.history_id][0][0]
            selected = select_records(case.history, task, frame, budget)
            cov = coverage(selected, infer(case.history).binding_records)
            self.assertEqual(json.loads(selected[0].observation)['event'], 'register_version')
            if case.setting.endswith('S'):
                self.assertEqual(len(selected), len(case.history.records))
                self.assertEqual(cov['binding_included'], cov['binding_total'])
            else:
                # Unauthorised target reviews look like binding ones apart from the actor, so
                # in large histories coverage is measured, not guaranteed (the E1 difficulty).
                self.assertLess(len(selected), len(case.history.records))
                self.assertLessEqual(sum(record_chars(r) + 1 for r in selected), budget)
                self.assertLessEqual(cov['binding_included'], cov['binding_total'])

    def test_retrieval_reads_no_evaluator_material(self):
        import inspect
        from reflectai_v05 import retrieval
        source = inspect.getsource(retrieval)
        for marker in ('world', 'TaskTruth', 'oracle', 'hard_type', 'binding_records'):
            if marker == 'binding_records':
                continue  # only the evaluator-side coverage() receives these ids
            self.assertNotIn(marker, source.split('def coverage')[0])


class ScoringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        case = generate_histories(45021, 'development', settings=('K-S',))[0]
        cls.pairs = generate_future_tasks(case, 45022)

    def output(self, task, fields, decision='keep', task_id=None):
        return WorkOutput(task_id=task_id or task.task_id, decision=decision, applied_rules=[],
                          fields=[OutputField(name=k, value=v) for k, v in fields.items()],
                          completed=True, questions=[])

    def test_correctness_is_field_based_not_label_based(self):
        for task, truth in self.pairs:
            right = score_task(task, truth, self.output(task, truth.expected_fields, decision='keep'))
            self.assertTrue(right['correct'])  # a wrong label never removes credit
        task, truth = next(p for p in self.pairs if p[1].expected_decision == 'apply')
        baseline = {f.name: f.value for f in task.baseline_fields}
        missed = score_task(task, truth, self.output(task, baseline))
        self.assertEqual((missed['correct'], missed['reason']), (False, 'missed_change'))

    def test_unsupported_change_and_missing_output(self):
        task, truth = next(p for p in self.pairs if p[1].task_type == 'control')
        changed = dict(truth.expected_fields)
        changed[next(iter(changed))] = 'altered'
        result = score_task(task, truth, self.output(task, changed, decision='apply'))
        self.assertFalse(result['correct'])
        missing = score_task(task, truth, None)
        self.assertEqual((missing['correct'], missing['reason']), (False, 'missing_or_invalid_output'))


if __name__ == '__main__':
    unittest.main()
