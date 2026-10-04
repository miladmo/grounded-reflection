import json
import unittest
from collections import Counter

from reflectai_v03.context import render_rules
from reflectai_v04.data import (ALLOCATION, FAMILIES, NOISE_QUOTAS, TASK_TYPE_ALLOCATION,
                               generate_future_tasks, generate_histories)
from reflectai_v04.data_contracts import FamilyConfig, FieldOption, GeneratorConfig
from reflectai_v04.oracle import infer_policies, read_frame
from reflectai_v04.presentation import REVIEW_COMMENTS


class DataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = generate_histories(2917, split='test_fixture')

    def test_allocation_and_separate_seeds(self):
        self.assertEqual(len(self.cases), 24)
        self.assertEqual(len({case.seed for case in self.cases}), 24)
        for setting, allocation in ALLOCATION.items():
            group = [case for case in self.cases if case.setting == setting]
            self.assertEqual([case.family for case in group], list(FAMILIES))
            self.assertEqual([case.regime for case in group], list(allocation))
            self.assertEqual([case.material_audit['task_type'] for case in group],
                             list(TASK_TYPE_ALLOCATION[setting]))
            self.assertEqual(Counter(case.regime for case in group),
                             {'change': 2, 'resolved_keep': 1, 'unidentifiable': 1})

    def test_seed_reproducibility_and_namespace_separation(self):
        again = generate_histories(2917, split='test_fixture')
        self.assertEqual([case.model_dump() for case in self.cases], [case.model_dump() for case in again])
        alternative = generate_histories(2918, split='test_fixture')
        review = generate_histories(2917, split='review')
        first_ids = {case.history.history_id for case in self.cases}
        self.assertFalse(first_ids.intersection(case.history.history_id for case in alternative))
        self.assertFalse(first_ids.intersection(case.history.history_id for case in review))
        self.assertNotEqual(self.cases[0].history.initial_configuration,
                            alternative[0].history.initial_configuration)

    def test_counts_and_actual_raw_artifacts(self):
        for case in self.cases:
            self.assertEqual(len(case.history.records), 60 if case.setting in ('S2', 'S5') else 6)
            frame = read_frame(case.history)
            raw_reviews = [json.loads(record.observation) for record in case.history.records
                           if json.loads(record.observation).get('format') == 'raw']
            if case.setting in ('S1', 'S5'):
                self.assertTrue(raw_reviews)
                for review in raw_reviews:
                    before = review['artifacts']['draft']['fields']
                    after = review['artifacts']['replacement']['fields']
                    self.assertNotEqual((frame.field_option.field in before, before.get(frame.field_option.field)),
                                        (frame.field_option.field in after, after.get(frame.field_option.field)))
                    self.assertGreaterEqual(len(after), 1)
                    self.assertNotIn('option_index', review)
            else:
                self.assertFalse(raw_reviews)

    def test_world_is_admissible_without_passing_it_to_oracle(self):
        for case in self.cases:
            result = infer_policies(case.history)
            world = [render_rules(task, case.truth.world_policy.rules) for task in case.truth.scope_probes]
            self.assertTrue(any([render_rules(task, policy.rules) for task in case.truth.scope_probes] == world
                                for policy in result.policies))
            self.assertEqual([policy.model_dump() for policy in result.policies],
                             [policy.model_dump() for policy in case.truth.admissible_policies])

    def test_public_projection_has_no_case_or_gold_objects(self):
        forbidden = {'regime', 'setting', 'seed', 'truth', 'world_policy', 'admissible_policies',
                     'candidate_targets', 'expected_decision', 'scenario_id', 'option_index',
                     'is_stale', 'is_independent', 'supports_requirement'}
        def inspect(value):
            if isinstance(value, dict):
                self.assertFalse(set(value).intersection(forbidden))
                for item in value.values():
                    inspect(item)
            elif isinstance(value, list):
                for item in value:
                    inspect(item)
        for case in self.cases:
            inspect(case.history.model_dump())
            inspect(json.loads(case.history.initial_configuration))
            for record in case.history.records:
                inspect(json.loads(record.observation))
            self.assertNotIn('task_id', case.history.model_dump_json())
            self.assertNotIn('tasks', type(case).model_fields)

    def test_future_tasks_are_fresh_and_decisions_match_independent_oracle(self):
        diagnostic_decisions, recoverable = Counter(), Counter()
        for case in self.cases:
            tasks = generate_future_tasks(case, 913)
            self.assertEqual(tasks, generate_future_tasks(case, 913))
            self.assertNotEqual(tasks[0][0].task_id, generate_future_tasks(case, 914)[0][0].task_id)
            historical_ids = {json.loads(record.observation).get('document_id') for record in case.history.records}
            for task, truth in tasks:
                self.assertNotIn(task.facts['document_id'], historical_ids)
                self.assertNotIn(case.history.history_id, task.model_dump_json())
                self.assertEqual(truth.history_id, case.history.history_id)
                self.assertEqual(task.facts['date'], read_frame(case.history).as_of[:10])
            diagnostic_decisions[tasks[0][1].expected_decision] += 1
            recoverable[tasks[0][1].recoverable] += 1
            self.assertEqual(tasks[1][1].expected_decision, 'keep')
            self.assertTrue(tasks[1][1].recoverable)
            self.assertEqual(tasks[0][0].context['task_family'], tasks[1][0].context['task_family'])
            self.assertEqual(tasks[0][0].context['workflow'], tasks[1][0].context['workflow'])
            self.assertNotEqual(tasks[0][0].context, tasks[1][0].context)
        self.assertEqual(diagnostic_decisions, {'apply': 12, 'keep': 12})
        self.assertEqual(recoverable, {True: 18, False: 6})

    def test_controls_probe_resolved_or_ambiguous_retention_in_same_workflow(self):
        for case in self.cases:
            task, truth = generate_future_tasks(case, 913)[1]
            base = {field.name: field.value for field in task.baseline_fields}
            outcomes = [render_rules(task, policy.rules) for policy in case.truth.admissible_policies]
            if case.regime == 'unidentifiable':
                self.assertTrue(any(outcome != base for outcome in outcomes))
                self.assertTrue(any(outcome == base for outcome in outcomes))
            else:
                self.assertTrue(all(outcome == base for outcome in outcomes))
            self.assertEqual(render_rules(task, case.truth.world_policy.rules), base)

    def test_direction_and_sales_arithmetic(self):
        self.assertEqual({case.material_audit['reversed_option'] for case in self.cases}, {False, True})
        for case in self.cases:
            if case.family != 'sales':
                continue
            for record in case.history.records:
                facts = json.loads(record.observation).get('facts', {})
                if 'annual_total' in facts:
                    self.assertEqual(int(facts['annual_total']),
                                     int(facts['monthly_unit_price']) * int(facts['seats']) * 12)

    def test_review_facts_date_matches_record_date(self):
        for case in self.cases:
            for record in case.history.records:
                item = json.loads(record.observation)
                if item.get('event') == 'review' and case.oracle_audit[record.record_id]['constraint_applied']:
                    self.assertEqual(item['facts']['date'], record.timestamp[:10])

    def test_public_checksum_marker_and_configurable_vocabulary(self):
        retrieval = next(case for case in self.cases if case.family == 'retrieval')
        self.assertIn('required means verify', retrieval.history.field_dictionary['fact.checksum_check'])
        config = GeneratorConfig(families={'hr': FamilyConfig(
            task_family='benefit_document', dimensions={'recipient': ['staff', 'partner'],
            'appointment': ['fixed', 'temporary']}, field_option=FieldOption(
                field='booking_reference', operation='set_fact', value='booking_reference'),
            baseline_template={'message': '{message}'})})
        custom = generate_histories(317, settings=['S2'], config=config)[0]
        self.assertEqual(read_frame(custom.history).task_family, 'benefit_document')
        self.assertEqual(read_frame(custom.history).dimensions['appointment'], ['fixed', 'temporary'])
        self.assertEqual(custom.material_audit['additional_noise_counts'], NOISE_QUOTAS['S2'])

    def test_invalid_configuration_fails_without_redraw(self):
        with self.assertRaises(ValueError):
            GeneratorConfig(noise_weights={'hidden_gold': 1})
        with self.assertRaises(ValueError):
            generate_histories(1, settings=['S0', 'S0'])
        with self.assertRaisesRegex(ValueError, 'setting=S0, family=hr, seed='):
            generate_histories(1, settings=['S0'], config=GeneratorConfig(families={
                'hr': FamilyConfig(dimensions={'recipient': ['internal']})}))

    def test_future_generation_rejects_expired_or_mismatched_version(self):
        case = self.cases[0].model_copy(deep=True)
        frame = read_frame(case.history)
        frame.as_of = '2027-02-01T12:00:00Z'
        case.history.initial_configuration = frame.model_dump_json()
        with self.assertRaisesRegex(ValueError, 'exactly one'):
            generate_future_tasks(case, 17)
        case = self.cases[0].model_copy(deep=True)
        case.diagnostic_context['version'] = 'unregistered-edition'
        with self.assertRaisesRegex(ValueError, 'publicly current'):
            generate_future_tasks(case, 17)

    def test_three_current_approvals_and_identifiability(self):
        counts = {'transfer_change': 1, 'observed_change': 3,
                  'resolved_retention_transfer': 1, 'unidentifiable': 4}
        for case in self.cases:
            result = infer_policies(case.history)
            current = [row for row in result.constraints if row['version'] == result.current_version]
            self.assertEqual(len(current), 3)
            self.assertEqual(case.material_audit['current_admissible_count'],
                             counts[case.material_audit['task_type']])
            self.assertEqual(case.material_audit['diagnostic_observed'],
                             case.material_audit['task_type'] == 'observed_change')
            for row in current:
                record = next(record for record in case.history.records if record.record_id == row['record_id'])
                self.assertIn(json.loads(record.observation)['comment'], REVIEW_COMMENTS)
            if case.family == 'sales':
                self.assertIn('account_owner', read_frame(case.history).dimensions)
                self.assertNotIn('reviewer', read_frame(case.history).dimensions)

    def test_registered_noise_quotas_and_approval_boundaries(self):
        for case in self.cases:
            if case.setting not in NOISE_QUOTAS:
                continue
            self.assertEqual(case.material_audit['additional_noise_counts'], NOISE_QUOTAS[case.setting])
            result = infer_policies(case.history)
            for row in case.material_audit['counterfactual']['records']:
                if row['record_type'] not in ('old_approval', 'forward'):
                    self.assertFalse(result.evidence_audit[row['record_id']]['constraint_applied'])
            if case.setting == 'S5':
                forwards = [row for row in case.material_audit['counterfactual']['records']
                            if row['record_type'] == 'forward']
                old = sum(result.evidence_audit[row['record_id']]['validity'] == 'superseded' for row in forwards)
                self.assertEqual((len(forwards), old), (8, 4))

    def test_public_contract_does_not_coach_factor_exclusions(self):
        for case in self.cases:
            self.assertNotIn('its destination context is not a new review', case.history.assumptions)
            self.assertNotIn('Do not assume an old configuration carries', case.history.assumptions)
            frame = read_frame(case.history)
            self.assertEqual(frame.hypothesis_class, 'h14')
            self.assertIn('XOR and XNOR', frame.hypothesis_definition)


if __name__ == '__main__':
    unittest.main()
