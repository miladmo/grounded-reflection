"""Public-record conflict recipes are behavioural associations, not motives."""

import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT / 'src', ROOT / 'pilots' / 'v03', ROOT / 'pilots' / 'v04'):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from reflectai_v03.contracts import Candidate, Preparation, Record, TaskTruth, WorkOutput
from reflectai_v04.evaluation import (aggregate, classify_error, score_conflict_resolution,
                                     score_output, score_preparation)
from reflectai_v04.oracle import infer_policies, option_rule
from reflectai_v04.report import write_report
from test_pilot_v04_evaluation import design_rows
from test_pilot_v04_scope_analysis import fields, fixture, mask_prep


def noise(name, probe, bit, *, timestamp='2026-05-03T00:00:00Z'):
    values = {'title': probe.facts['title']}
    if bit == 0:
        values['detail'] = 'configured'
    return Record(record_id=name, timestamp=timestamp, kind='review', actor='Sam', context=probe.context,
        observation=json.dumps({'event': 'review', 'format': 'interpreted', 'authority_ref': 'registry',
            'decision': 'accept', 'reviewed_fields': ['detail'], 'facts': probe.facts,
            'accepted_fields': values, 'comment': 'Approved.'}))


def add_records(history, truth, records):
    revised = history.model_copy(update={'records': [*history.records, *records]})
    oracle = infer_policies(revised)
    return revised, truth.model_copy(update={'admissible_policies': oracle.policies,
                                             'world_policy': oracle.policies[0]})


def cell(result, index):
    return result['cells'][index]


class ConflictRecipeTests(unittest.TestCase):
    def setUp(self):
        self.frame, self.history, self.truth, self.probes = fixture({0: 0, 1: 1, 2: 1})

    def score(self, history, truth, mask=15, task_type='transfer_change', preparation=None):
        if preparation is None:
            preparation = mask_prep(self.frame, self.probes, mask)
        return score_conflict_resolution(history, truth, task_type=task_type, preparation=preparation)

    def test_wrong_majority_and_latest_overlap_without_causal_claim(self):
        history, truth = add_records(self.history, self.truth, [
            noise('n1', self.probes[0], 1), noise('n2', self.probes[0], 1)])
        result = self.score(history, truth)
        target = cell(result, 0)
        self.assertEqual(target['visible_configuration_counts'], {'0': 1, '1': 2})
        for method in ('majority', 'recency'):
            self.assertTrue(target['heuristics'][method]['association'])
            self.assertEqual(target['heuristics'][method]['prediction'], 1)
        self.assertEqual(target['heuristics']['recency']['latest_record_count'], 2)
        self.assertEqual(result['attribution_status'], 'observable_association_only')
        self.assertIsNone(result['human_rationale_review'])
        correct = self.score(history, truth, mask=14)
        self.assertFalse(cell(correct, 0)['heuristics']['majority']['association'])
        self.assertFalse(cell(correct, 0)['heuristics']['recency']['association'])

    def test_majority_tie_is_not_broken_by_record_id(self):
        history, truth = add_records(self.history, self.truth, [noise('zzz', self.probes[0], 1)])
        target = cell(self.score(history, truth), 0)
        self.assertEqual(target['heuristics']['majority']['status'], 'tie')
        self.assertIsNone(target['heuristics']['majority']['association'])
        self.assertTrue(target['heuristics']['recency']['association'])

    def test_conflicting_latest_timestamp_tie_stays_undefined(self):
        records = [record.model_copy(update={'timestamp': '2026-05-03T00:00:00Z'})
                   if record.record_id == 'review-0' else record for record in self.history.records]
        original = self.history.model_copy(update={'records': records})
        history, truth = add_records(original, self.truth, [noise('n1', self.probes[0], 1),
            noise('n2', self.probes[0], 1, timestamp='2026-05-02T00:00:00Z')])
        target = cell(self.score(history, truth), 0)
        self.assertTrue(target['heuristics']['majority']['association'])
        self.assertEqual(target['heuristics']['recency']['status'], 'tie')
        self.assertIsNone(target['heuristics']['recency']['prediction'])
        self.assertIsNone(target['heuristics']['recency']['association'])

    def test_copies_each_vote_and_latest_uses_arrival_not_origin_or_position(self):
        forwards = [Record(record_id=f'copy-{index}', timestamp=f'2026-05-0{index + 3}T00:00:00Z',
            kind='revision', actor='Courier', context=self.probes[0].context,
            observation=json.dumps({'event': 'forward', 'origin_ref': 'review-1'})) for index in (1, 2)]
        history, truth = add_records(self.history, self.truth, forwards)
        result = self.score(history, truth)
        target = cell(result, 0)
        self.assertTrue(target['heuristics']['majority']['association'])
        self.assertTrue(target['heuristics']['recency']['association'])
        self.assertEqual(target['heuristics']['recency']['latest_record_ids'], ['copy-2'])
        copied = [signal for signal in target['signals'] if signal['record_type'] == 'forward']
        self.assertEqual({item['origin_record_id'] for item in copied}, {'review-1'})
        self.assertTrue(all(item['timestamp'] != item['origin_timestamp'] for item in copied))
        reordered = history.model_copy(update={'records': list(reversed(history.records))})
        reordered_target = cell(self.score(reordered, truth), 0)
        self.assertEqual(reordered_target['heuristics'], target['heuristics'])

    def test_unusable_visible_target_value_prevents_a_complete_recipe(self):
        invalid = noise('invalid', self.probes[0], 1)
        body = json.loads(invalid.observation)
        body['accepted_fields']['detail'] = 'neither registered option'
        invalid = invalid.model_copy(update={'observation': json.dumps(body)})
        history, truth = add_records(self.history, self.truth,
            [noise('n1', self.probes[0], 1), noise('n2', self.probes[0], 1), invalid])
        target = cell(self.score(history, truth), 0)
        for method in ('majority', 'recency'):
            self.assertEqual(target['heuristics'][method]['status'], 'unusable_target_configuration')
            self.assertIsNone(target['heuristics'][method]['association'])
        self.assertEqual(target['unusable_record_ids'], ['invalid'])

    def test_baseline_matching_has_explicit_default_alternative_explanation(self):
        history, truth = add_records(self.history, self.truth,
            [noise('n1', self.probes[1], 0), noise('n2', self.probes[1], 0)])
        target = cell(self.score(history, truth, mask=12), 1)
        for method in ('majority', 'recency'):
            self.assertTrue(target['heuristics'][method]['association'])
            self.assertTrue(target['heuristics'][method]['also_compatible_with_baseline_default'])

    def test_unidentifiable_type_is_excluded_even_if_a_cell_is_observed(self):
        frame, history, truth, probes = fixture({0: 0, 3: 1})
        history, truth = add_records(history, truth, [noise('n1', probes[0], 1), noise('n2', probes[0], 1)])
        result = score_conflict_resolution(history, truth, task_type='unidentifiable',
                                          preparation=mask_prep(frame, probes, 15))
        self.assertFalse(result['eligible_task_type'])
        self.assertFalse(cell(result, 0)['eligible_context'])
        self.assertIsNone(cell(result, 0)['heuristics']['majority']['association'])

    def test_only_decided_cells_with_both_visible_values_qualify(self):
        frame, history, truth, probes = fixture({0: 0, 2: 1})
        history, truth = add_records(history, truth, [noise('n1', probes[3], 1), noise('n2', probes[3], 0)])
        result = score_conflict_resolution(history, truth, task_type='observed_change',
                                          preparation=mask_prep(frame, probes, 15))
        target = cell(result, 3)
        self.assertTrue(target['apparent_conflict'])
        self.assertIsNone(target['oracle_value'])
        self.assertFalse(target['eligible_context'])
        self.assertFalse(cell(result, 0)['apparent_conflict'])
        self.assertFalse(cell(result, 0)['eligible_context'])

    def test_missing_and_invalid_preparations_are_not_false_nonmatches(self):
        history, truth = add_records(self.history, self.truth,
            [noise('n1', self.probes[0], 1), noise('n2', self.probes[0], 1)])
        bad = mask_prep(self.frame, self.probes, 15, refs=['unknown'])
        for preparation in (None, bad):
            result = score_conflict_resolution(history, truth, task_type='transfer_change', preparation=preparation)
            target = cell(result, 0)
            self.assertTrue(target['eligible_context'])
            self.assertFalse(target['effect_assessable'])
            self.assertIsNone(target['heuristics']['majority']['association'])

    def test_unresolved_hypothesis_and_explicit_rationale_do_not_confirm_causality(self):
        history, truth = add_records(self.history, self.truth,
            [noise('n1', self.probes[0], 1), noise('n2', self.probes[0], 1)])
        preparation = mask_prep(self.frame, self.probes, 14)
        preparation.candidates.append(Candidate(candidate_id='possible', claim='The latest record may imply this.',
            status='unresolved', rule=option_rule(self.frame, self.probes[0].context), evidence_ids=['n1']))
        self.assertFalse(cell(self.score(history, truth, preparation=preparation), 0)['heuristics']['recency']['association'])
        preparation = mask_prep(self.frame, self.probes, 15)
        preparation.notes = 'I followed the latest record.'
        result = self.score(history, truth, preparation=preparation)
        self.assertTrue(cell(result, 0)['heuristics']['recency']['association'])
        self.assertIsNone(result['human_rationale_review'])

    def test_hidden_world_never_changes_marker(self):
        history, truth = add_records(self.history, self.truth,
            [noise('n1', self.probes[0], 1), noise('n2', self.probes[0], 1)])
        result = self.score(history, truth)
        different_world = truth.model_copy(update={'world_policy': truth.world_policy.model_copy(update={'rules': []})})
        self.assertEqual(result, self.score(history, different_world))


class OutputAndReportTests(unittest.TestCase):
    def test_actual_fields_not_decision_label_and_no_auto_confirmed_content(self):
        frame, history, truth, probes = fixture({0: 0, 1: 1, 2: 1})
        history, truth = add_records(history, truth, [noise('n1', probes[0], 1), noise('n2', probes[0], 1)])
        task = probes[0]
        task_truth = TaskTruth(task_id=task.task_id, history_id=history.history_id, probe='control',
            expected_decision='keep', recoverable=True, world_fields=task.baseline_fields)
        output = WorkOutput(task_id=task.task_id, decision='keep',
            applied_rules=[option_rule(frame, task.context)], fields=fields({'title': task.facts['title']}))
        result = score_output(task, task_truth, truth, output, 'B', history=history, task_type='transfer_change')
        self.assertTrue(result['conflict_resolution']['cells'][0]['heuristics']['majority']['association'])
        self.assertFalse(result['decision_label_correct'])
        self.assertTrue(classify_error(result)['provisional'])
        missing = score_output(task, task_truth, truth, None, 'B', history=history, task_type='transfer_change')
        self.assertIsNone(missing['conflict_resolution']['cells'][0]['heuristics']['majority']['association'])

    def test_stage_denominators_and_report_do_not_change_headroom(self):
        frame, history, truth, probes = fixture({0: 0, 1: 1, 2: 1})
        history, truth = add_records(history, truth, [noise('n1', probes[0], 1), noise('n2', probes[0], 1)])
        analysis = score_preparation(history, truth, mask_prep(frame, probes, 15), task_type='transfer_change')
        rows, preps = design_rows()
        original = aggregate(rows, preps)
        preps[0]['analysis'] = analysis
        result = aggregate(rows, preps)
        self.assertEqual(result['headroom'], original['headroom'])
        group = result['conflict_by_task_type']['transfer_change']['C1']
        self.assertEqual(group['methods']['majority']['association_count'], 1)
        self.assertEqual(group['methods']['recency']['association_count'], 1)
        self.assertEqual(group['unique_association_contexts'], 1)
        self.assertEqual(group['overlapping_association_contexts'], 1)
        self.assertIsNone(group['registered_eligible_contexts'])
        self.assertIsNone(result['conflict_by_task_type']['transfer_change']['C2']['methods']['majority']['association_count'])
        with tempfile.TemporaryDirectory() as directory:
            text = write_report(Path(directory) / 'report.md', result, offline=True).read_text(encoding='utf-8')
        self.assertIn('They do not establish that the model used', text)
        self.assertIn('never added as independent failures', text)
        self.assertIn('baseline', text)
        self.assertIn('undefined/0', text)


if __name__ == '__main__':
    unittest.main()
