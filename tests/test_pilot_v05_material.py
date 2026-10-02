"""Offline tests for the v0.5 rule classes, oracle and generator. No model calls."""

from collections import Counter
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
for location in (ROOT / 'src', ROOT / 'pilots/v03', ROOT / 'pilots/v05'):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

from reflectai_v03.contracts import History, Record  # noqa: E402
from reflectai_v05 import hclass  # noqa: E402
from reflectai_v05.contracts import CLASS_DEFINITIONS, FieldOption, PublicFrame  # noqa: E402
from reflectai_v05.data import (ALLOCATION, DISTRACTOR_QUOTAS, FAMILIES, SETTINGS,  # noqa: E402
                                generate_future_tasks, generate_histories)
from reflectai_v05.oracle import infer  # noqa: E402

PRIVATE_MARKERS = ('world', 'hard_type', 'confusable', 'anchor', 'task_cells', 'oracle_status', 'expected_')


class RuleClassTests(unittest.TestCase):
    def test_class_sizes_and_exclusions(self):
        self.assertEqual(len(hclass.rule_class(6, range(6))), 134)
        self.assertEqual(len(hclass.rule_class(6, (2, 4))), 14)
        xor = hclass.literal_table(6, 0, True) ^ hclass.literal_table(6, 1, True)
        self.assertNotIn(xor, {f.table for f in hclass.rule_class(6, range(6))})

    def test_declared_pair_ignores_other_attributes(self):
        for f in hclass.rule_class(6, (1, 3)):
            for cell in range(64):
                self.assertEqual(hclass.value(f, cell), hclass.value(f, cell ^ 0b110101 & ~0b1010))

    def test_hand_checked_h14_templates(self):
        # Observed 00 -> 0, 01 -> 1, 10 -> 1 leaves only the disjunction; 11 is warranted.
        klass = hclass.rule_class(2, (0, 1))
        functions = hclass.compatible(klass, {0b00: 0, 0b01: 1, 0b10: 1})
        self.assertEqual(len(functions), 1)
        self.assertEqual(hclass.status_at(functions, 0b11), 'apply')
        # Observed 00 -> 0 and 11 -> 1 leaves x, y, x AND y, x OR y; 01 and 10 are unresolved.
        functions = hclass.compatible(klass, {0b00: 0, 0b11: 1})
        self.assertEqual(len(functions), 4)
        self.assertEqual({hclass.status_at(functions, c) for c in (0b01, 0b10)}, {'unresolved'})

    def test_confusable_attributes_keep_cells_unresolved(self):
        klass = hclass.rule_class(3, range(3))
        # Attribute 2 copies attribute 0 in every observation; truth depends on attribute 0 only.
        observations = {c: c & 1 for c in range(8) if (c >> 2) & 1 == c & 1}
        functions = hclass.compatible(klass, observations)
        for cell in range(8):
            if (cell >> 2) & 1 == cell & 1:
                self.assertEqual(hclass.status_at(functions, cell), 'apply' if cell & 1 else 'keep')
            else:  # the two attributes disagree: rules over either one fit the evidence
                self.assertEqual(hclass.status_at(functions, cell), 'unresolved')


def _frame(**changes):
    values = dict(task_family='sales_offer', workflow='workflow-x', version='edition-x', as_of='2026-06-15T12:00:00Z',
                  attributes={f'a{i}': ['v0', 'v1'] for i in range(6)}, candidate_attributes=['a0', 'a1'],
                  field_option=FieldOption(field='total', operation='omit'),
                  baseline_template={'text': '{text}', 'total': '{total}'}, fact_descriptions={},
                  hypothesis_class='h14-declared', hypothesis_definition=CLASS_DEFINITIONS['h14-declared'])
    values.update(changes)
    return PublicFrame(**values)


class OracleTests(unittest.TestCase):
    def history(self, reviews):
        frame = _frame()
        records = [Record(record_id='reg', timestamp='2026-01-01T00:00:00Z', kind='template', actor='workflow-registry',
                          context={}, observation=json.dumps({
                              'event': 'register_version', 'version': 'edition-x', 'workflow': 'workflow-x',
                              'task_family': 'sales_offer', 'valid_from': '2026-01-01T00:00:00Z',
                              'valid_until': '2027-01-01T00:00:00Z', 'authorised_reviewers': ['Ann', 'Ben']}))]
        for index, (cell, omit, actor, extra) in enumerate(reviews):
            fields = {'text': 't'} if omit else {'text': 't', 'total': '9'}
            event = {'event': 'review', 'authority_ref': 'reg', 'facts': {'text': 't', 'total': '9'},
                     'reviewed_fields': ['total'], 'decision': 'accept', 'accepted_fields': fields, **extra}
            records.append(Record(record_id=f'r{index}', timestamp='2026-03-01T10:00:00Z', kind='review', actor=actor,
                                  context=frame.context_of(cell), observation=json.dumps(event)))
        return History(history_id='h', initial_configuration=frame.model_dump_json(), assumptions='a',
                       field_dictionary={}, records=records)

    def test_only_binding_approvals_constrain(self):
        reviews = [(0b00, False, 'Ann', {}), (0b01, True, 'Ann', {}), (0b10, True, 'Ben', {}),
                   (0b11, False, 'Eve', {}),                                  # outside the roster
                   (0b11, False, 'Ann', {'reviewed_fields': ['other']}),       # target not reviewed
                   (0b11, False, 'Ann', {'decision': 'reject'})]
        result = infer(self.history(reviews))
        self.assertEqual(result.observations, {0b00: 0, 0b01: 1, 0b10: 1})
        self.assertEqual(result.status(0b11), 'apply')
        self.assertEqual(result.binding_records, ['r0', 'r1', 'r2'])

    def test_contradictory_binding_approvals_stop(self):
        with self.assertRaises(ValueError):
            infer(self.history([(0b00, False, 'Ann', {}), (0b00, True, 'Ben', {})]))

    def test_missing_definition_is_rejected(self):
        with self.assertRaises(ValueError):
            _frame(hypothesis_definition='abridged')
        with self.assertRaises(ValueError):
            _frame(hypothesis_class='h134')  # needs all six candidates


class GeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = generate_histories(45021, 'development')

    def test_design_allocation_and_balance(self):
        self.assertEqual(len(self.cases), 16)
        for setting in SETTINGS:
            slots = [(c.hard_type, c.direction) for c in self.cases if c.setting == setting]
            self.assertEqual(Counter(h for h, _ in slots), {'transfer_change': 2, 'unidentifiable': 2})
            for hard in ('transfer_change', 'unidentifiable'):
                self.assertEqual(sorted(d for h, d in slots if h == hard), ['add', 'omit'])
        for family in FAMILIES:
            hard = Counter(ALLOCATION[s][family][0] for s in SETTINGS)
            self.assertEqual(hard, {'transfer_change': 2, 'unidentifiable': 2})

    def test_record_quotas(self):
        for case in self.cases:
            quotas = DISTRACTOR_QUOTAS['small' if case.setting.endswith('S') else 'large']
            self.assertEqual(len(case.history.records), 1 + 12 + sum(quotas.values()))
            self.assertEqual(len(case.oracle_audit['binding_records']), 12)

    def test_every_task_status_is_rederived_from_public_evidence(self):
        required = {'observed_change': 'apply', 'observed_retention': 'keep', 'transfer_change': 'apply',
                    'unidentifiable': 'unresolved', 'control': 'out_of_scope'}
        for index, case in enumerate(self.cases):
            oracle = infer(case.history)
            self.assertTrue(any(f.table == int(case.world['table']) for f in oracle.compatible))
            for task, truth in generate_future_tasks(case, 45022 + index):
                self.assertEqual(truth.oracle_status, required[truth.task_type])
                if truth.cell is not None and truth.task_type in ('transfer_change', 'unidentifiable'):
                    self.assertNotIn(truth.cell, oracle.observations)

    def test_unknown6_ambiguity_comes_from_a_confusable_attribute(self):
        for case in self.cases:
            if case.setting.startswith('U') and case.hard_type == 'unidentifiable':
                cell = case.task_cells['unidentifiable']
                self.assertNotEqual(hclass.bit(cell, case.world['confusable']), hclass.bit(cell, case.world['anchor']))

    def test_known2_declares_exactly_the_relevant_pair(self):
        for case in self.cases:
            frame = PublicFrame.model_validate_json(case.history.initial_configuration)
            if case.setting.startswith('K'):
                self.assertEqual(sorted(frame.candidate_indices()), sorted(case.world['relevant']))
            else:
                self.assertEqual(len(frame.candidate_attributes), 6)

    def test_public_history_contains_no_evaluator_material(self):
        for case in self.cases:
            text = case.history.model_dump_json()
            for marker in PRIVATE_MARKERS:
                self.assertNotIn(f'"{marker}', text)

    def test_r2_hard_tasks_resist_shortcuts(self):
        from reflectai_v05.heuristics import all_references
        for case in self.cases:
            cell = case.task_cells[case.hard_type]
            required = 'apply' if case.hard_type == 'transfer_change' else 'keep'
            references = all_references(case.history, cell)
            for name in ('nearest_neighbour', 'all_accepted_reviews|b', 'inverted_rejections|b',
                         'rejections_as_assent|b', 'followed_preferences|b'):
                self.assertNotEqual(references[name], required, (case.setting, case.family, name))
            if case.hard_type == 'unidentifiable':
                functions = infer(case.history).compatible
                self.assertGreaterEqual(sum(hclass.value(f, cell) for f in functions) / len(functions), 0.5)
                if case.setting.startswith('U'):
                    via = [f for f in functions if case.world['confusable'] in f.attributes]
                    self.assertTrue(via and all(hclass.value(f, cell) for f in via))

    def test_r2_reviewers_names_and_reviewed_fields(self):
        from reflectai_v05.data import FAMILY_VOCABULARY
        from reflectai_v05.oracle import configuration_bit
        values = {v for vocab in FAMILY_VOCABULARY.values() for vs in vocab['attributes'].values() for v in vs}
        for case in self.cases:
            frame = PublicFrame.model_validate_json(case.history.initial_configuration)
            records = {r.record_id: r for r in case.history.records}
            approvals = Counter()
            for record_id in infer(case.history).binding_records:
                event = json.loads(records[record_id].observation)
                approvals[(records[record_id].actor, configuration_bit(frame, event['accepted_fields'], event['facts']))] += 1
            for actor in {a for a, _ in approvals}:
                self.assertTrue(approvals[(actor, 0)] and approvals[(actor, 1)])
            self.assertFalse({r.actor for r in case.history.records} & values)
            for record in case.history.records:
                event = json.loads(record.observation)
                for name in event.get('reviewed_fields', []):
                    self.assertIn(name, frame.baseline_template | {frame.field_option.field: ''})

    def _distractors(self, case):
        """(type, cell, agrees_with_world) for every non-binding distractor record."""
        from reflectai_v05.audit import _distractor_type, _fields_of
        from reflectai_v05.oracle import configuration_bit
        frame = PublicFrame.model_validate_json(case.history.initial_configuration)
        binding = set(infer(case.history).binding_records)
        roster = next(json.loads(r.observation)['authorised_reviewers'] for r in case.history.records
                      if json.loads(r.observation).get('event') == 'register_version')
        world, result = int(case.world['table']), []
        for record in case.history.records:
            event = json.loads(record.observation)
            if record.record_id in binding or event.get('event') == 'register_version':
                continue
            kind = _distractor_type(record, event, roster, frame.field_option.field)
            if kind is None:
                continue
            cell = frame.cell_of(record.context)
            bit = configuration_bit(frame, _fields_of(event), event['facts'])
            result.append((kind, cell, bit == hclass.value(world, cell)))
        return result

    def test_r3_no_rejection_near_the_hard_task(self):
        for case in self.cases:
            hard = case.task_cells[case.hard_type]
            frame = PublicFrame.model_validate_json(case.history.initial_configuration)
            records = {r.record_id: r for r in case.history.records}
            nearest = min(bin(frame.cell_of(records[i].context) ^ hard).count('1')
                          for i in infer(case.history).binding_records)
            for kind, cell, _ in self._distractors(case):
                if kind == 'rejected_artifact':
                    self.assertNotEqual(cell, hard)
                    self.assertGreater(bin(cell ^ hard).count('1'), nearest)

    def test_r3_distractors_outside_the_exact_context_carry_no_information(self):
        for case in self.cases:
            hard = case.task_cells[case.hard_type]
            relevant = case.world['relevant']
            balance = Counter()
            for kind, cell, agrees in self._distractors(case):
                if cell == hard:
                    continue
                place = 'relevant' if all(hclass.bit(cell, i) == hclass.bit(hard, i) for i in relevant) else 'rest'
                balance[(kind, place)] += 1 if agrees else -1
            for key, value in balance.items():
                self.assertLessEqual(abs(value), 1, (case.setting, case.family, key))
            if case.setting.endswith('S'):
                rejected = [(cell, agrees) for kind, cell, agrees in self._distractors(case)
                            if kind == 'rejected_artifact']
                self.assertEqual(sorted(a for _, a in rejected), [False, True])
                for cell, _ in rejected:
                    self.assertFalse(all(hclass.bit(cell, i) == hclass.bit(hard, i) for i in relevant))

    def test_generation_is_deterministic(self):
        again = generate_histories(45021, 'development')
        self.assertEqual([c.model_dump_json() for c in again], [c.model_dump_json() for c in self.cases])
        other = generate_histories(45031, 'review')
        self.assertFalse({c.history.history_id for c in other} & {c.history.history_id for c in self.cases})


if __name__ == '__main__':
    unittest.main()
