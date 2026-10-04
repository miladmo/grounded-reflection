"""Prospective round-2 regressions; historical calibration outputs stay unchanged."""

import unittest

from reflectai_v03.context import render_rules
from reflectai_v03.contracts import OutputField, TaskTruth, WorkOutput
from reflectai_v03.data import build_histories, build_tasks
from reflectai_v03.evaluation import evaluate_output


def indexed(seed):
    dataset = build_tasks(build_histories(seed, 'test_fixture'), seed + 40000)
    histories = {history.history_id: history for history in dataset.histories}
    truths = {truth.scenario_id: truth for truth in dataset.truths}
    tasks = {task.task_id: task for task in dataset.tasks}
    task_truths = {(truth.history_id, truth.probe): truth for truth in dataset.task_truths}
    return dataset, histories, truths, tasks, task_truths


class RoundTwoDataTests(unittest.TestCase):
    def test_sales_pair_uses_same_new_case_for_an_observed_reviewer(self):
        for seed in range(12):
            dataset, histories, truths, tasks, task_truths = indexed(seed)
            paired = []
            for scenario in ('S03', 'S04'):
                history = histories[truths[scenario].history_id]
                task_truth = task_truths[(history.history_id, 'diagnostic')]
                task = tasks[task_truth.task_id]
                known_reviewers = {record.context.get('reviewer') for record in history.records}
                known_cases = {record.context.get('case_id') for record in history.records}
                self.assertIn(task.context['reviewer'], known_reviewers)
                self.assertEqual(task.context['reviewer'], dataset.assignments['sales_other_reviewer'])
                self.assertNotIn(task.context['case_id'], known_cases)
                self.assertNotIn(task.facts['contract_reference'], ('CS-441', 'CS-442'))
                self.assertNotIn('first renewal preview', task.request)
                paired.append(task.model_dump(exclude={'task_id'}))
            self.assertEqual(paired[0], paired[1])

    def test_both_sales_counterbalancings_preserve_the_required_contrast(self):
        seen = set()
        for seed in range(20):
            dataset, _, truths, tasks, task_truths = indexed(seed)
            baseline_state = dataset.assignments['sales_baseline_annual']
            seen.add(baseline_state)
            for scenario in ('S03', 'S04'):
                history_truth = truths[scenario]
                truth = task_truths[(history_truth.history_id, 'diagnostic')]
                task = tasks[truth.task_id]
                baseline = {field.name: field.value for field in task.baseline_fields}
                alternatives = [render_rules(task, policy.rules) for policy in history_truth.admissible_policies]
                self.assertTrue(all(output == alternatives[0] for output in alternatives))
                self.assertEqual(truth.expected_decision, 'keep' if scenario == 'S03' else 'apply')
                self.assertEqual(alternatives[0] == baseline, scenario == 'S03')
                self.assertEqual('annual_total' in alternatives[0],
                                 (baseline_state == 'present') == (scenario == 'S03'))
                if 'annual_total' in alternatives[0]:
                    self.assertEqual(alternatives[0]['annual_total'], task.facts['annual_total'])
        self.assertEqual(seen, {'present', 'absent'})

    def test_s04_admits_observed_only_and_shared_explanations(self):
        for seed in range(12):
            dataset, _, truths, _, _ = indexed(seed)
            truth = truths['S04']
            self.assertEqual(len(truth.admissible_policies), 2)
            by_status = {target.status: target for target in truth.candidate_targets}
            expected_reviewers = {dataset.assignments[key] for key in
                                  ('sales_local_reviewer', 'sales_other_reviewer', 'sales_third_reviewer')}
            self.assertEqual(set(by_status['adopt'].rule.scope.match['reviewer']), expected_reviewers)
            self.assertNotIn('reviewer', by_status['unresolved'].rule.scope.match)
            self.assertNotIn('reviewer', truth.world_policy.rules[0].scope.match)
            self.assertEqual(by_status['adopt'].rule.scope.match['task_family'], ['renewal_preview'])
            self.assertEqual(by_status['adopt'].rule.scope.match['workflow'], ['account_ops'])

    def test_unseen_reviewer_preserves_uncertainty_in_both_directions(self):
        seen = set()
        for seed in range(20):
            dataset, _, truths, _, _ = indexed(seed)
            seen.add(dataset.assignments['sales_baseline_annual'])
            truth = truths['S04']
            task = next(probe for probe in truth.scope_probes
                        if probe.context.get('reviewer') == dataset.assignments['sales_future_reviewer'])
            baseline = {field.name: field.value for field in task.baseline_fields}
            alternatives = [render_rules(task, policy.rules) for policy in truth.admissible_policies]
            self.assertNotEqual(alternatives[0], alternatives[1])
            world = render_rules(task, truth.world_policy.rules)
            oracle = TaskTruth(task_id=task.task_id, history_id=truth.history_id,
                               probe='diagnostic', expected_decision='keep', recoverable=False,
                               world_fields=[OutputField(name=key, value=value) for key, value in world.items()])
            output = WorkOutput(task_id=task.task_id, decision='keep', fields=task.baseline_fields)
            score = evaluate_output(task, oracle, truth, output, 'B')
            self.assertTrue(score['update_correct'])
            self.assertFalse(score['world_compliant'])
            self.assertEqual(score['expected_warranted_fields'], baseline)
            self.assertIn('annual_total', score['unresolved_fields'])
        self.assertEqual(seen, {'present', 'absent'})

    def test_scope_probes_distinguish_every_observed_reviewer_and_boundaries(self):
        dataset, _, truths, _, _ = indexed(3301)
        truth = truths['S04']
        adopted = next(target.rule for target in truth.candidate_targets if target.status == 'adopt')
        expected_reviewers = set(adopted.scope.match['reviewer'])
        matched_reviewers = {probe.context['reviewer'] for probe in truth.scope_probes
                             if adopted.scope.applies_to(probe.context) == 'match'}
        self.assertEqual(matched_reviewers, expected_reviewers)
        for missing in ('reviewer', 'workflow'):
            probe = next(probe for probe in truth.scope_probes if missing not in probe.context)
            self.assertEqual(adopted.scope.applies_to(probe.context), 'unknown')
        for field, value in [('workflow', 'other_team'), ('task_family', 'pipeline_forecast')]:
            probe = next(probe for probe in truth.scope_probes if probe.context.get(field) == value)
            self.assertEqual(render_rules(probe, [adopted]),
                             {item.name: item.value for item in probe.baseline_fields})
        unknown = dataset.assignments['sales_future_reviewer']
        self.assertNotIn(unknown, expected_reviewers)

    def test_registered_denominators_and_separate_controls_do_not_change(self):
        for seed in range(12):
            dataset, _, truths, _, _ = indexed(seed)
            self.assertEqual(len(dataset.histories), 8)
            self.assertEqual(len(dataset.tasks), 16)
            diagnostic = [truth for truth in dataset.task_truths if truth.probe == 'diagnostic']
            controls = [truth for truth in dataset.task_truths if truth.probe == 'control']
            self.assertEqual(len(diagnostic), 8)
            self.assertEqual(sum(truth.expected_decision == 'apply' for truth in diagnostic), 4)
            self.assertEqual(sum(truth.expected_decision == 'keep' for truth in diagnostic), 4)
            self.assertEqual(sum(truth.recoverable for truth in diagnostic), 7)
            self.assertEqual(len(controls), 8)
            self.assertTrue(all(truth.expected_decision == 'keep' for truth in controls))
            self.assertEqual([truth.history_id for truth in diagnostic if not truth.recoverable],
                             [truths['S02'].history_id])

    def test_checksum_marker_dictionary_is_canonical_and_route_neutral(self):
        _, histories, truths, _, _ = indexed(3301)
        descriptions = []
        for scenario in ('S05', 'S06'):
            description = histories[truths[scenario].history_id].field_dictionary['checksum_check']
            self.assertIn('"required"', description)
            self.assertIn('not a checksum result', description)
            self.assertNotIn('ep-', description)
            descriptions.append(description)
        self.assertEqual(descriptions[0], descriptions[1])


if __name__ == '__main__':
    unittest.main()
