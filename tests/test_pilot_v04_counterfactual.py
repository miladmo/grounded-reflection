import json
import unittest
from unittest.mock import patch

from reflectai_v04.counterfactual import assess_assignment, audit_counterfactuals
from reflectai_v04.data import generate_histories
from reflectai_v04.oracle import infer_policies
from test_pilot_v04_oracle import event, fixture_assignments, witness


class CounterfactualTests(unittest.TestCase):
    def test_all_eight_promotions_for_the_four_hand_authored_templates(self):
        templates = [
            ([(0, 0), (1, 1), (2, 1)], 3, 0, [1, 0, 0, 1, 0, 1, 0, 1], 0, 4),
            ([(0, 0), (2, 1)], 2, 0, [3, 0, 2, 1, 0, 3, 1, 2], 0, 2),
            ([(0, 1), (1, 0), (2, 0)], 3, 1, [0, 1, 1, 0, 1, 0, 1, 0], 0, 4),
            ([(0, 0), (3, 1)], 2, 1, [4, 0, 2, 2, 2, 2, 0, 4], 2, 2),
        ]
        for observations, diagnostic, control, counts, flips, contradictions in templates:
            history = fixture_assignments(observations)
            result = infer_policies(history)
            def context(index):
                return witness(history, recipient=['staff', 'partner'][index // 2],
                               region=['north', 'south'][index % 2]).context
            audits = [assess_assignment(result, context(index), bit, context(diagnostic), context(control))
                      for index in range(4) for bit in (0, 1)]
            self.assertEqual([row['remaining_policy_count'] for row in audits], counts)
            self.assertEqual(sum(row['outcome'] == 'action_flip' for row in audits), flips)
            self.assertEqual(sum(row['outcome'] == 'contradiction' for row in audits), contradictions)
            for row in audits:
                if row['remaining_policy_count'] == 0:
                    self.assertIsNone(row['diagnostic_action'])
                    self.assertIsNone(row['control_action'])

    def test_forward_uses_visible_source_value_and_destination_without_mutating_history(self):
        history = fixture_assignments([(0, 0), (3, 1)])
        diagnostic = witness(history).context
        control = witness(history, recipient='staff', region='south').context
        history.records.append(event('forward', {'event': 'forward', 'origin_ref': 'review-1'},
                                     diagnostic, actor='forwarder', timestamp='2026-04-13T00:00:00Z'))
        before = history.model_dump_json()
        audit = audit_counterfactuals(history, diagnostic, control, 'action_flip')
        self.assertEqual(history.model_dump_json(), before)
        self.assertEqual(len(infer_policies(history).policies), 4)
        row = audit['records'][0]
        self.assertEqual(row['origin_record_id'], 'review-1')
        self.assertEqual(row['context'], diagnostic)
        self.assertEqual(row['option_index'], 1)
        self.assertEqual(row['selected_field'], 'reference')
        self.assertEqual(row['selected_field_value'], 'REF-317')
        self.assertTrue(row['selected_field_present'])
        self.assertEqual(row['outcome'], 'action_flip')
        self.assertTrue(audit['passed'])

    def test_resolving_retention_is_not_an_action_flip(self):
        history = fixture_assignments([(0, 0), (3, 1)])
        diagnostic, control = witness(history).context, witness(history, recipient='staff', region='south').context
        history.records.append(event('forward', {'event': 'forward', 'origin_ref': 'review-0'},
                                     diagnostic, actor='forwarder', timestamp='2026-04-13T00:00:00Z'))
        audit = audit_counterfactuals(history, diagnostic, control, 'action_flip')
        self.assertEqual(audit['records'][0]['outcome'], 'retention_resolved')
        self.assertFalse(audit['passed'])

    def test_missing_origin_is_unassessable_and_cannot_qualify(self):
        history = fixture_assignments([(0, 0), (3, 1)])
        diagnostic, control = witness(history).context, witness(history, recipient='staff', region='south').context
        history.records.append(event('forward', {'event': 'forward', 'origin_ref': 'missing'}, diagnostic))
        audit = audit_counterfactuals(history, diagnostic, control, 'action_flip')
        self.assertEqual(audit['records'][0]['outcome'], 'unassessable')
        self.assertFalse(audit['passed'])

    def test_every_present_type_qualifies_and_every_record_is_accounted_for(self):
        expected_records = {'S0': 1, 'S1': 1, 'S2': 48, 'S3': 2, 'S4': 1, 'S5': 49}
        for case in generate_histories(44301, split='test_fixture'):
            audit = case.material_audit['counterfactual']
            self.assertTrue(audit['passed'])
            self.assertEqual(len(audit['records']), expected_records[case.setting])
            self.assertEqual(sum(row['record_count'] for row in audit['by_type'].values()),
                             expected_records[case.setting])
            required = 'action_flip' if case.regime == 'unidentifiable' else 'contradiction'
            self.assertEqual(audit['required_outcome'], required)
            for counts in audit['by_type'].values():
                self.assertGreater(counts[required], 0)
                self.assertEqual(len(counts['qualifying_record_ids']), counts[required])
            self.assertEqual(audit, audit_counterfactuals(case.history, case.diagnostic_context,
                                                        case.control_context, required))
            for row in audit['records']:
                self.assertIsNotNone(row['option_index'])
                self.assertEqual(row['context']['version'], infer_policies(case.history).current_version)
                if row['outcome'] == 'contradiction':
                    self.assertIsNone(row['diagnostic_action'])

    def test_public_rejection_has_no_negative_target_verdict(self):
        for case in generate_histories(44311, split='review', settings=['S2', 'S5']):
            records = {record.record_id: record for record in case.history.records}
            for row in case.material_audit['counterfactual']['records']:
                if row['record_type'] != 'rejected_opposite_artifact':
                    continue
                body = json.loads(records[row['record_id']].observation)
                self.assertEqual(body['reviewed_fields'], [])
                self.assertTrue(body['rejection_reason'].strip())
                self.assertNotIn('rejection_reason', body.get('reviewed_fields', []))
                self.assertFalse(case.oracle_audit[row['record_id']]['constraint_applied'])
                self.assertEqual(body['decision'], 'reject')

    def test_failed_qualification_stops_generation_without_seed_redraw(self):
        failure = {'passed': False, 'by_type': {'forward': {'qualifying_record_ids': []}}}
        with patch('reflectai_v04.data.audit_counterfactuals', return_value=failure) as audit:
            with self.assertRaisesRegex(ValueError, 'counterfactual qualification failed'):
                generate_histories(44301, settings=['S0'])
            self.assertEqual(audit.call_count, 1)


if __name__ == '__main__':
    unittest.main()
