"""Independent public fixtures and metamorphic checks for the finite oracle."""

import json
import unittest

from reflectai_v03.contracts import History, OutputField, Record, Task
from reflectai_v03.context import render_rules
from reflectai_v04.data import generate_histories
from reflectai_v04.data_contracts import FieldOption, PublicFrame
from reflectai_v04.oracle import H14_MASKS, infer_policies, policy_complexity, policy_option_at, read_frame


def event(record_id, body, context=None, actor='Asha', timestamp='2026-04-12T10:00:00Z', kind='review'):
    return Record(record_id=record_id, timestamp=timestamp, kind=kind, actor=actor,
                  context=context or {}, observation=json.dumps(body))


def independent_fixture():
    frame = PublicFrame(task_family='notification', workflow='workflow-cobalt',
        as_of='2026-04-15T12:00:00Z', dimensions={'recipient': ['staff', 'partner'],
        'region': ['north', 'south']}, field_option=FieldOption(
            field='reference', operation='set_fact', value='reference'),
        baseline_template={'body': '{body}'}, fact_descriptions={'reference': 'Current reference.', 'body': 'Text.'})
    registration = event('registry', {'event': 'register_version', 'version': 'edition-a',
        'task_family': 'notification', 'workflow': 'workflow-cobalt',
        'valid_from': '2026-01-01T00:00:00Z', 'valid_until': '2026-07-01T00:00:00Z',
        'authorised_reviewers': ['Asha']}, actor='registry', timestamp='2026-01-01T00:00:00Z', kind='template')
    context = {'task_family': 'notification', 'workflow': 'workflow-cobalt', 'version': 'edition-a',
               'recipient': 'partner', 'region': 'north'}
    review = event('review-one', {'event': 'review', 'format': 'raw', 'authority_ref': 'registry',
        'facts': {'reference': 'REF-317', 'body': 'Please confirm delivery.'},
        'reviewed_fields': ['reference'], 'decision': 'accept', 'accepted_artifact': 'corrected',
        'artifacts': {'draft': {'fields': {'body': 'Please confirm delivery.'}},
                      'corrected': {'fields': {'body': 'Please confirm delivery.', 'reference': 'REF-317'}}}}, context)
    return History(history_id='history-independent', initial_configuration=frame.model_dump_json(),
                   assumptions='Explicit authorised acceptance fixes only the reviewed fields in the recorded context.',
                   field_dictionary={'reference': 'Optional current reference.'}, records=[registration, review])


def witness(history, recipient='partner', region='north', version='edition-a'):
    frame = read_frame(history)
    return Task(task_id='witness', context={'task_family': frame.task_family, 'workflow': frame.workflow,
                'version': version, 'recipient': recipient, 'region': region},
                facts={'reference': 'REF-NEW', 'body': 'A fresh task.'},
                baseline_fields=[OutputField(name='body', value='A fresh task.')], request='Complete the task.')


def effects(history, task):
    return {tuple(sorted(render_rules(task, policy.rules).items())) for policy in infer_policies(history).policies}


def change_body(record, **updates):
    body = json.loads(record.observation)
    body.update(updates)
    return record.model_copy(update={'observation': json.dumps(body)})


def fixture_assignments(assignments):
    """Hand-authored assignments rendered as actual approved artifact variants."""
    history = independent_fixture()
    prototype = history.records[1]
    history.records = history.records[:1]
    for ordinal, (index, value) in enumerate(assignments):
        context = {**prototype.context, 'recipient': ['staff', 'partner'][index // 2],
                   'region': ['north', 'south'][index % 2]}
        record = prototype.model_copy(update={'record_id': f'review-{ordinal}', 'context': context})
        history.records.append(change_body(record, accepted_artifact='corrected' if value else 'draft'))
    return history


class OracleTests(unittest.TestCase):
    def test_public_class_must_be_explicit_and_unaltered(self):
        for key in ('hypothesis_class', 'hypothesis_definition'):
            history = independent_fixture()
            data = json.loads(history.initial_configuration)
            del data[key]
            history.initial_configuration = json.dumps(data)
            with self.assertRaisesRegex(ValueError, 'must be present'):
                infer_policies(history)
        history = independent_fixture()
        data = json.loads(history.initial_configuration)
        data['hypothesis_class'] = 'h16'
        history.initial_configuration = json.dumps(data)
        with self.assertRaises(ValueError):
            infer_policies(history)

    def test_all_fourteen_tables_and_both_out_of_class_tables(self):
        for mask in range(16):
            history = fixture_assignments([(index, (mask >> index) & 1) for index in range(4)])
            if mask in (6, 9):
                with self.assertRaisesRegex(ValueError, 'admits no policy'):
                    infer_policies(history)
            else:
                result = infer_policies(history)
                self.assertEqual(len(result.policies), 1)
                for index in range(4):
                    task = witness(history, recipient=['staff', 'partner'][index // 2],
                                   region=['north', 'south'][index % 2])
                    self.assertEqual(policy_option_at(result.policies[0], task.context), (mask >> index) & 1)

    def test_h14_closed_under_dimension_swaps_and_value_relabelling(self):
        for swap in (False, True):
            for flip_x in (0, 1):
                for flip_y in (0, 1):
                    transformed = set()
                    for mask in H14_MASKS:
                        value = 0
                        for index in range(4):
                            x, y = (index // 2) ^ flip_x, (index % 2) ^ flip_y
                            if swap:
                                x, y = y, x
                            value |= ((mask >> index) & 1) << (2 * x + y)
                        transformed.add(value)
                    self.assertEqual(transformed, set(H14_MASKS))

    def test_transfer_and_removing_a_decisive_witness(self):
        change = fixture_assignments([(0, 0), (1, 1), (2, 1)])
        self.assertEqual(effects(change, witness(change, region='south')),
                         {(('body', 'A fresh task.'), ('reference', 'REF-NEW'))})
        change.records = [record for record in change.records if record.record_id != 'review-1']
        self.assertEqual(len(effects(change, witness(change, region='south'))), 2)
        retain = fixture_assignments([(0, 1), (1, 0), (2, 0)])
        self.assertEqual(effects(retain, witness(retain, region='south')), {(('body', 'A fresh task.'),)})

    def test_confounded_evidence_preserves_simple_and_interacting_alternatives(self):
        history = fixture_assignments([(0, 0), (3, 1)])
        result = infer_policies(history)
        self.assertEqual(len(result.policies), 4)
        masks = {sum(policy_option_at(policy, witness(history, recipient=['staff', 'partner'][index // 2],
                     region=['north', 'south'][index % 2]).context) << index for index in range(4))
                 for policy in result.policies}
        self.assertEqual(masks, {8, 10, 12, 14})
        self.assertEqual({policy_complexity(mask) for mask in masks}, {1, 2})
        self.assertEqual({mask for mask in H14_MASKS if policy_complexity(mask) == 0}, {0, 15})
        self.assertEqual({mask for mask in H14_MASKS if policy_complexity(mask) == 1}, {3, 5, 10, 12})

    def test_independent_change_fixture_and_unobserved_scope(self):
        history = independent_fixture()
        self.assertEqual(len(infer_policies(history).policies), 7)
        self.assertEqual(len(effects(history, witness(history))), 1)
        self.assertIn(('reference', 'REF-NEW'), next(iter(effects(history, witness(history)))))
        self.assertEqual(len(effects(history, witness(history, region='south'))), 2)

    def test_explicit_approval_of_absence_establishes_retention(self):
        history = independent_fixture()
        body = json.loads(history.records[1].observation)
        body['accepted_artifact'] = 'draft'
        history.records[1] = history.records[1].model_copy(update={'observation': json.dumps(body)})
        self.assertEqual(effects(history, witness(history)), {(('body', 'A fresh task.'),)})

    def test_unreviewed_field_and_unknown_authority_are_unresolved(self):
        for update in ({'reviewed_fields': []}, {'authority_ref': 'unknown'}, {'decision': 'pending'}):
            history = independent_fixture()
            history.records[1] = change_body(history.records[1], **update)
            self.assertEqual(len(infer_policies(history).policies), 14)
        history = independent_fixture()
        history.records[1] = history.records[1].model_copy(update={'actor': 'Unauthorised'})
        self.assertEqual(len(infer_policies(history).policies), 14)

    def test_copy_cannot_add_a_new_context_and_keeps_origin_traceability(self):
        history = independent_fixture()
        before = infer_policies(history)
        context = {**history.records[1].context, 'region': 'south'}
        history.records.append(event('copy', {'event': 'forward', 'origin_ref': 'review-one'}, context,
                                     timestamp='2026-04-13T00:00:00Z', actor='forwarder'))
        history.records.append(event('copy-two', {'event': 'forward', 'origin_ref': 'copy'}, context,
                                     timestamp='2026-04-14T00:00:00Z', actor='forwarder'))
        after = infer_policies(history)
        self.assertEqual(before.policies, after.policies)
        self.assertEqual(len(before.constraints), len(after.constraints))
        self.assertEqual(after.evidence_audit['copy-two']['root_id'], 'review-one')
        self.assertTrue(after.evidence_audit['copy-two']['usable_current_support'])
        self.assertEqual(after.evidence_audit['copy-two']['scope_context']['region'], 'north')
        self.assertEqual(len(effects(history, witness(history, region='south'))), 2)

    def test_unknown_and_cyclic_origins_stay_unknown(self):
        history = independent_fixture()
        history.records += [event('copy', {'event': 'forward', 'origin_ref': 'missing'}),
                            event('cycle-a', {'event': 'forward', 'origin_ref': 'cycle-b'}),
                            event('cycle-b', {'event': 'forward', 'origin_ref': 'cycle-a'})]
        result = infer_policies(history)
        for name in ['copy', 'cycle-a', 'cycle-b']:
            self.assertIsNone(result.evidence_audit[name]['root_id'])
            self.assertEqual(result.evidence_audit[name]['validity'], 'unknown')
            self.assertFalse(result.evidence_audit[name]['usable_current_support'])

    def test_noise_and_independent_duplicate_do_not_change_admissible_policies(self):
        history = independent_fixture()
        before = infer_policies(history).policies
        history.records.append(event('comment', {'event': 'comment', 'message': 'I prefer no reference.'}))
        history.records.append(event('timeout', {'event': 'execution', 'http_status': 503}))
        history.records.append(history.records[1].model_copy(update={'record_id': 'independent-repeat'}))
        self.assertEqual(before, infer_policies(history).policies)

    def test_removing_witness_cannot_narrow_the_policy_set(self):
        history = independent_fixture()
        with_review = {policy.model_dump_json(exclude={'policy_id'}) for policy in infer_policies(history).policies}
        history.records = history.records[:1]
        without_review = {policy.model_dump_json(exclude={'policy_id'}) for policy in infer_policies(history).policies}
        self.assertLess(with_review, without_review)

    def test_interpreted_and_raw_are_equivalent(self):
        history = independent_fixture()
        before = infer_policies(history).policies
        body = json.loads(history.records[1].observation)
        selected = body.pop('artifacts')[body.pop('accepted_artifact')]['fields']
        body.update({'format': 'interpreted', 'accepted_fields': selected})
        history.records[1] = history.records[1].model_copy(update={'observation': json.dumps(body)})
        self.assertEqual(before, infer_policies(history).policies)

    def test_consistent_identifier_renaming_preserves_semantics(self):
        history = independent_fixture()
        before = infer_policies(history).policies
        history.records[0] = history.records[0].model_copy(update={'record_id': 'renamed-registry'})
        history.records[1] = change_body(history.records[1], authority_ref='renamed-registry')
        history.records[1] = history.records[1].model_copy(update={'record_id': 'renamed-review'})
        self.assertEqual(before, infer_policies(history).policies)

    def test_future_review_is_not_observed_evidence(self):
        history = independent_fixture()
        history.records[1] = history.records[1].model_copy(update={'timestamp': '2026-04-17T10:00:00Z'})
        result = infer_policies(history)
        self.assertEqual(len(result.policies), 14)
        self.assertFalse(result.evidence_audit['review-one']['constraint_applied'])

    def test_registry_not_yet_issued_cannot_authorise_an_earlier_review(self):
        history = independent_fixture()
        history.records[0] = history.records[0].model_copy(update={'timestamp': '2026-04-13T00:00:00Z'})
        self.assertEqual(len(infer_policies(history).policies), 14)
        history.records[0] = history.records[0].model_copy(update={'timestamp': '2026-04-17T00:00:00Z'})
        with self.assertRaisesRegex(ValueError, 'exactly one'):
            infer_policies(history)

    def test_expired_registration_does_not_silently_persist(self):
        history = independent_fixture()
        history.records[0] = change_body(history.records[0], valid_until='2026-04-01T00:00:00Z')
        with self.assertRaisesRegex(ValueError, 'exactly one'):
            infer_policies(history)

    def test_conflicting_authorised_reviews_fail_instead_of_majority_vote(self):
        history = independent_fixture()
        contradictory = change_body(history.records[1], accepted_artifact='draft')
        history.records.append(contradictory.model_copy(update={'record_id': 'contradictory'}))
        with self.assertRaisesRegex(ValueError, 'contradictory authorised'):
            infer_policies(history)

    def test_temporal_constraints_remain_in_their_recorded_versions(self):
        cases = generate_histories(123, split='test_fixture', settings=['S4'])
        for case in cases:
            result = infer_policies(case.history)
            old = [item for item in result.constraints if item['version'] != result.current_version]
            self.assertEqual(len(old), 1)
            old_audit = result.evidence_audit[old[0]['record_id']]
            self.assertEqual(old_audit['validity'], 'superseded')
            self.assertTrue(old_audit['constraint_applied'])
            self.assertFalse(old_audit['usable_current_support'])
            current = [item for item in result.constraints if item['version'] == result.current_version]
            self.assertEqual(len(current), 3)


if __name__ == '__main__':
    unittest.main()
