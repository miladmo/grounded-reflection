import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'pilots' / 'v03'))

from reflectai_v03.context import render_rules
from reflectai_v03.data import build_histories, build_tasks


class DataTests(unittest.TestCase):
    def setUp(self):
        self.histories = build_histories(3301, 'test_fixture')
        self.dataset = build_tasks(self.histories, 4419)

    def test_histories_are_deterministic_and_contain_no_future_tasks(self):
        self.assertEqual(self.histories, build_histories(3301, 'test_fixture'))
        self.assertEqual(len(self.histories.histories), 8)
        self.assertEqual(len(self.histories.truths), 8)
        self.assertEqual(self.histories.tasks, [])
        self.assertEqual(self.histories.task_truths, [])

    def test_tasks_are_a_separate_deterministic_instantiation(self):
        self.assertEqual(self.dataset, build_tasks(self.histories, 4419))
        self.assertEqual(self.histories.tasks, [])
        self.assertEqual(len(self.dataset.tasks), 16)
        self.assertEqual(len(self.dataset.task_truths), 16)
        other = build_tasks(self.histories, 4420)
        self.assertNotEqual(self.dataset.tasks, other.tasks)
        self.assertEqual(self.dataset.histories, other.histories)
        with self.assertRaisesRegex(ValueError, 'already'):
            build_tasks(self.dataset, 4420)

    def test_public_inputs_do_not_contain_truth_or_membership_fields(self):
        public = {'histories': [item.model_dump() for item in self.dataset.histories],
                  'tasks': [item.model_dump() for item in self.dataset.tasks]}
        text = json.dumps(public)
        for forbidden in ['scenario_id', 'pair_id', 'world_policy', 'admissible_policies',
                          'candidate_targets', 'expected_decision', 'recoverable',
                          'private-probe', 'S01', 'S02', 'P01']:
            self.assertNotIn(forbidden, text)
        for task in public['tasks']:
            self.assertNotIn('history_id', task)
        truth_ids = {target.target_id for truth in self.dataset.truths for target in truth.candidate_targets}
        self.assertTrue(all(identifier not in text for identifier in truth_ids))

    def test_opaque_ids_are_unique_and_split_specific(self):
        ids = [history.history_id for history in self.histories.histories]
        self.assertEqual(len(set(ids)), 8)
        development = build_histories(3301, 'development')
        self.assertTrue(set(ids).isdisjoint(history.history_id for history in development.histories))
        for history in self.histories.histories:
            self.assertEqual(len(history.records), len({record.record_id for record in history.records}))
            self.assertEqual([record.timestamp for record in history.records],
                             sorted(record.timestamp for record in history.records))

    def test_paired_future_inputs_identical_except_opaque_identifier(self):
        tasks = {task.task_id: task for task in self.dataset.tasks}
        histories = {truth.history_id: truth for truth in self.dataset.truths}
        groups = {}
        for truth in self.dataset.task_truths:
            key = histories[truth.history_id].pair_id, truth.probe
            groups.setdefault(key, []).append(tasks[truth.task_id].model_dump(exclude={'task_id'}))
        self.assertEqual(len(groups), 8)
        for pair in groups.values():
            self.assertEqual(len(pair), 2)
            self.assertEqual(pair[0], pair[1])

    def test_counterbalancing_preserves_registered_denominators(self):
        seen = {key: set() for key in ['hr_trigger', 'hr_baseline_reference',
                                       'sales_baseline_annual', 'report_baseline_tag', 'tag_separator']}
        for seed in range(30):
            dataset = build_tasks(build_histories(seed, 'test_fixture'), seed + 500)
            for key in seen:
                seen[key].add(dataset.assignments[key])
            diagnostic = [truth for truth in dataset.task_truths if truth.probe == 'diagnostic']
            controls = [truth for truth in dataset.task_truths if truth.probe == 'control']
            self.assertEqual(sum(truth.expected_decision == 'apply' for truth in diagnostic), 4)
            self.assertEqual(sum(truth.expected_decision == 'keep' for truth in diagnostic), 4)
            self.assertEqual(sum(truth.recoverable for truth in diagnostic), 7)
            self.assertTrue(all(truth.expected_decision == 'keep' and truth.recoverable for truth in controls))
            history_truths = {truth.history_id: truth for truth in dataset.truths}
            tasks = {task.task_id: task for task in dataset.tasks}
            for truth in dataset.task_truths:
                task = tasks[truth.task_id]
                baseline = {field.name: field.value for field in task.baseline_fields}
                world = {field.name: field.value for field in truth.world_fields}
                scenario = history_truths[truth.history_id].scenario_id
                world_change = truth.expected_decision == 'apply' or (scenario == 'S02' and truth.probe == 'diagnostic')
                self.assertEqual(world != baseline, world_change)
        self.assertTrue(all(len(values) >= 2 for values in seen.values()))

    def test_s02_uncertainty_disagrees_with_hidden_world_only_on_diagnostic(self):
        history_truth = next(item for item in self.dataset.truths if item.scenario_id == 'S02')
        self.assertEqual(len(history_truth.admissible_policies), 4)
        tasks = {task.task_id: task for task in self.dataset.tasks}
        for truth in self.dataset.task_truths:
            if truth.history_id != history_truth.history_id:
                continue
            task = tasks[truth.task_id]
            outputs = [render_rules(task, policy.rules) for policy in history_truth.admissible_policies]
            if truth.probe == 'diagnostic':
                self.assertEqual(truth.expected_decision, 'keep')
                self.assertFalse(truth.recoverable)
                self.assertNotEqual(outputs[0], outputs[1])
            else:
                self.assertTrue(all(output == outputs[0] for output in outputs))

    def test_partial_and_local_candidate_coverage_is_present(self):
        by_scenario = {truth.scenario_id: truth for truth in self.dataset.truths}
        partial = next(target for target in by_scenario['S02'].candidate_targets if target.status == 'adopt')
        self.assertIn('recipient', partial.rule.scope.match)
        self.assertIn('contract', partial.rule.scope.match)
        local = next(target for target in by_scenario['S03'].candidate_targets if target.status == 'adopt')
        self.assertEqual(local.rule.scope.match['reviewer'], [self.dataset.assignments['sales_local_reviewer']])
        chart = next(target for target in by_scenario['S07'].candidate_targets if target.status == 'adopt')
        self.assertEqual(chart.rule.scope.match['artifact'], ['chart'])

    def test_candidate_behaviour_is_distinguishable_on_private_probes(self):
        for truth in self.dataset.truths:
            fingerprints = []
            for target in truth.candidate_targets:
                outputs = [render_rules(probe, [target.rule]) for probe in truth.scope_probes]
                fingerprints.append(json.dumps(outputs, sort_keys=True))
            self.assertEqual(len(fingerprints), len(set(fingerprints)), truth.scenario_id)

    def test_scope_probes_cover_missing_context_and_worker_role_variation(self):
        for truth in self.dataset.truths:
            self.assertTrue(any('work_role' in probe.context for probe in truth.scope_probes))
            for target in truth.candidate_targets:
                self.assertNotIn('work_role', target.rule.scope.match)
                self.assertTrue(any(target.rule.scope.applies_to(probe.context) == 'unknown'
                                    for probe in truth.scope_probes))

    def test_fact_based_rules_cannot_match_by_memorising_one_historical_value(self):
        checked = 0
        for seed in range(5):
            for truth in build_histories(seed, 'test_fixture').truths:
                for target in truth.candidate_targets:
                    rule = target.rule
                    if rule.operation not in ['set_fact', 'append_fact']:
                        continue
                    matching = [probe for probe in truth.scope_probes
                                if rule.scope.applies_to(probe.context) == 'match']
                    values = {probe.facts[rule.value] for probe in matching}
                    self.assertGreaterEqual(len(values), 2, (truth.scenario_id, target.target_id))
                    checked += 1
        self.assertGreater(checked, 0)

    def test_fresh_report_snapshot_and_retrieval_plans_do_not_reveal_results(self):
        task_truths = {truth.task_id: truth for truth in self.dataset.task_truths}
        for task in self.dataset.tasks:
            if task.context['task_family'] == 'study_report':
                self.assertNotEqual(task.facts['snapshot'], self.dataset.assignments['history_snapshot'])
            if task.context['task_family'] == 'retrieval_plan':
                self.assertNotIn('checksum_result', task.facts)
                self.assertNotIn(self.dataset.assignments['route_alternative'], json.dumps(task.model_dump()))
                self.assertIn('Do not execute retrieval', task.request)
            self.assertIn(task.task_id, task_truths)

    def test_unknown_split_rejected(self):
        with self.assertRaises(ValueError):
            build_histories(1, 'validation')


if __name__ == '__main__':
    unittest.main()
