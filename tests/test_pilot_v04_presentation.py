import json
import unittest
from datetime import datetime

from reflectai_v04.data import generate_histories
from reflectai_v04.oracle import infer_policies, read_frame
from reflectai_v04.presentation import PERSON_NAMES, REVIEW_COMMENTS, present_history


def instant(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


class PresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.batches = {
            (44321, 'development'): generate_histories(44321, split='development'),
            (44331, 'review'): generate_histories(44331, split='review'),
            (880123, 'test_fixture'): generate_histories(880123, split='test_fixture'),
        }
        cls.cases = [case for cases in cls.batches.values() for case in cases]

    def test_dates_versions_registry_and_origin_chronology(self):
        for case in self.cases:
            result, frame = infer_policies(case.history), read_frame(case.history)
            records = {record.record_id: record for record in case.history.records}
            for record in case.history.records:
                body = json.loads(record.observation)
                self.assertLessEqual(instant(record.timestamp), instant(frame.as_of))
                if body['event'] == 'register_version':
                    continue
                registration = result.versions[record.context['version']]
                self.assertGreaterEqual(instant(record.timestamp), instant(registration['valid_from']))
                self.assertLess(instant(record.timestamp), instant(registration['valid_until']))
                self.assertGreaterEqual(instant(record.timestamp),
                                        instant(records[registration['registry_id']].timestamp))
                if body['event'] == 'forward':
                    self.assertGreater(instant(record.timestamp), instant(records[body['origin_ref']].timestamp))
                if 'facts' in body:
                    self.assertEqual(body['facts']['date'], record.timestamp[:10])
                fields = [body.get(key) for key in ('accepted_fields', 'rejected_fields', 'proposed_fields')]
                fields += [item.get('fields') for item in body.get('artifacts', {}).values()]
                for values in fields:
                    if isinstance(values, dict) and 'delivery_timestamp' in values:
                        self.assertEqual(values['delivery_timestamp'], record.timestamp)

    def test_constructive_surface_overlap_in_both_hard_negative_categories(self):
        for case in self.cases:
            if case.setting not in ('S2', 'S5'):
                continue
            oracle = infer_policies(case.history)
            records = {record.record_id: record for record in case.history.records}
            positives = [records[key] for key, value in oracle.evidence_audit.items()
                         if value['constraint_applied'] and value['validity'] == 'active']
            positive_comments = {json.loads(record.observation)['comment'] for record in positives}
            self.assertIn('Approved.', positive_comments)
            self.assertEqual(len(positive_comments), 3)
            frame = read_frame(case.history)
            roster = oracle.versions[oracle.current_version]['authorised_reviewers']
            groups = {'unauthorised': [], 'unreviewed': []}
            for record in case.history.records:
                body = json.loads(record.observation)
                if (body['event'] != 'review' or body.get('decision') != 'accept'
                        or record.context['version'] != oracle.current_version):
                    continue
                if record.actor not in roster:
                    groups['unauthorised'].append(record)
                elif frame.field_option.field not in body['reviewed_fields']:
                    groups['unreviewed'].append(record)
            for group in groups.values():
                negative_comments = {json.loads(record.observation)['comment'] for record in group}
                self.assertTrue(positive_comments <= negative_comments)
                for positive in positives:
                    comment = json.loads(positive.observation)['comment']
                    matches = [negative for negative in group
                               if negative.timestamp[:13] == positive.timestamp[:13]
                               and json.loads(negative.observation)['comment'] == comment]
                    self.assertTrue(any(instant(record.timestamp) < instant(positive.timestamp) for record in matches))
                    self.assertTrue(any(instant(record.timestamp) > instant(positive.timestamp) for record in matches))

    def test_unauthorised_actors_have_ordinary_names_and_the_same_record_kind(self):
        for case in self.cases:
            oracle = infer_policies(case.history)
            for record in case.history.records:
                body = json.loads(record.observation)
                if body['event'] != 'review':
                    continue
                self.assertEqual(record.kind, 'review')
                self.assertIn(record.actor, PERSON_NAMES)
                self.assertIn(body['comment'], REVIEW_COMMENTS)
                if body.get('decision') == 'reject':
                    self.assertTrue(body['rejection_reason'])
                    self.assertEqual(body['reviewed_fields'], [])
                    self.assertFalse(oracle.evidence_audit[record.record_id]['constraint_applied'])

    def test_genuine_minutes_are_not_confined_to_the_middle_of_the_hour(self):
        minutes = []
        for case in self.cases:
            for record in case.history.records:
                audit = case.oracle_audit[record.record_id]
                if audit['constraint_applied'] and audit['validity'] == 'active':
                    minutes.append(instant(record.timestamp).minute)
        self.assertTrue(any(value < 20 for value in minutes))
        self.assertTrue(any(value >= 40 for value in minutes))

    def test_dedicated_stream_is_deterministic_nonmutating_and_semantically_invariant(self):
        for case in self.batches[(44321, 'development')]:
            original = case.history.model_dump_json()
            first = present_history(case.history, 731)
            repeated = present_history(case.history, 731)
            second = present_history(case.history, 732)
            self.assertEqual(case.history.model_dump_json(), original)
            self.assertEqual(first, repeated)
            self.assertNotEqual(first, second)
            before, after = infer_policies(case.history), infer_policies(first)
            self.assertEqual(before.policies, after.policies)
            signature = lambda rows: sorted(json.dumps(row, sort_keys=True) for row in rows)
            self.assertEqual(signature(before.constraints), signature(after.constraints))

    def test_order_and_wording_vary_without_changing_quotas_or_gates(self):
        unsorted_histories, preference_texts, execution_texts, forward_texts = 0, set(), set(), set()
        genuine_dates = set()
        for case in self.cases:
            self.assertEqual(len(case.history.records), 60 if case.setting in ('S2', 'S5') else 6)
            self.assertEqual(case.material_audit['material_revision'], 'v04-amendment-03-r2')
            self.assertTrue(case.material_audit['counterfactual']['passed'])
            timestamps = [record.timestamp for record in case.history.records]
            unsorted_histories += timestamps != sorted(timestamps)
            for record in case.history.records:
                body = json.loads(record.observation)
                if body['event'] == 'preference':
                    preference_texts.add(body['message'])
                elif body['event'] == 'execution':
                    execution_texts.add(body['log'])
                elif body['event'] == 'forward':
                    forward_texts.add(body['message'])
                elif case.oracle_audit[record.record_id]['constraint_applied']:
                    genuine_dates.add(record.timestamp[:10])
        self.assertGreater(unsorted_histories, 0)
        self.assertGreater(len(preference_texts), 1)
        self.assertGreater(len(execution_texts), 1)
        self.assertGreater(len(forward_texts), 1)
        self.assertTrue(genuine_dates - {'2026-05-10', '2026-06-10', '2026-06-11', '2026-06-12'})


if __name__ == '__main__':
    unittest.main()
