"""Hand-authored H14 transfer fixtures, independent of the case generator."""

import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT / 'src', ROOT / 'pilots' / 'v03', ROOT / 'pilots' / 'v04'):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from grounded_reflection.models import Scope
from reflectai_v03.context import render_rules
from reflectai_v03.contracts import (Candidate, History, HistoryTruth, OutputField,
    Preparation, Record, Rule, Task, TaskTruth, WorkOutput)
from reflectai_v04.data_contracts import FieldOption, PublicFrame
from reflectai_v04.evaluation import (aggregate, classify_error, score_output,
    score_preparation, score_scope)
from reflectai_v04.oracle import (context_cells, infer_policies, option_rule,
    policy_complexity)
from reflectai_v04.report import write_report
from test_pilot_v04_evaluation import design_rows


def fields(values):
    return [OutputField(name=key, value=value) for key, value in values.items()]


def fixture(observations, *, old_version=False, extra_records=()):
    frame = PublicFrame(task_family='work', workflow='workflow', as_of='2026-06-01T00:00:00Z',
        dimensions={'x': ['zero', 'one'], 'y': ['zero', 'one']},
        field_option=FieldOption(field='detail', operation='omit'),
        baseline_template={'detail': 'configured', 'title': '{title}'},
        fact_descriptions={'title': 'Current document title'})
    records = [Record(record_id='registry', timestamp='2026-01-01T00:00:00Z', kind='template',
        actor='registry', context={}, observation=json.dumps({'event': 'register_version',
        'task_family': 'work', 'workflow': 'workflow', 'version': 'v2',
        'valid_from': '2026-01-01T00:00:00Z', 'valid_until': '2027-01-01T00:00:00Z',
        'authorised_reviewers': ['approver']}))]
    if old_version:
        records.append(Record(record_id='old-registry', timestamp='2025-01-01T00:00:00Z', kind='template',
            actor='registry', context={}, observation=json.dumps({'event': 'register_version',
            'task_family': 'work', 'workflow': 'workflow', 'version': 'v1',
            'valid_from': '2025-01-01T00:00:00Z', 'valid_until': '2026-01-01T00:00:00Z',
            'authorised_reviewers': ['approver']})))
    probes = []
    for index, cell in enumerate(context_cells(frame)):
        context = {'task_family': 'work', 'workflow': 'workflow', 'version': 'v2', **cell}
        base = {'detail': 'configured', 'title': f'Memo {index}'}
        probes.append(Task(task_id=f'probe-{index}', context=context, facts={'title': f'Memo {index}'},
                           baseline_fields=fields(base), request='Create the document.'))
        if index in observations:
            selected = {'title': f'Memo {index}'} if observations[index] else base
            records.append(Record(record_id=f'review-{index}', timestamp='2026-05-01T00:00:00Z',
                kind='review', actor='approver', context=context, observation=json.dumps({
                'event': 'review', 'format': 'interpreted', 'authority_ref': 'registry',
                'decision': 'accept', 'reviewed_fields': ['detail'], 'facts': {'title': f'Memo {index}'},
                'accepted_fields': selected, 'comment': 'Approved.'})))
    for entry in extra_records:
        records.append(Record(record_id=entry['id'], timestamp='2026-05-02T00:00:00Z', kind='review',
            actor=entry.get('actor', 'approver'), context=probes[1].context,
            observation=json.dumps({'event': 'review', 'format': 'interpreted',
            'authority_ref': entry.get('authority_ref', 'registry'), 'reviewed_fields': ['detail'],
            'decision': entry.get('decision', 'accept'), 'facts': {'title': 'Memo 1'},
            'accepted_fields': {'title': 'Memo 1'}, 'rejection_scope': 'whole_artifact',
            'reason': 'Another field requires review.'})))
    history = History(history_id='h14', initial_configuration=frame.model_dump_json(),
        assumptions='Registered approval constrains the reviewed field in its recorded version.',
        field_dictionary={'detail': 'Optional detail', 'title': 'Current title'}, records=records)
    oracle = infer_policies(history)
    truth = HistoryTruth(history_id='h14', scenario_id='hand-authored', pair_id='fixture',
        world_policy=oracle.policies[0], admissible_policies=oracle.policies,
        candidate_targets=[], scope_probes=probes)
    return frame, history, truth, probes


def prep(frame, contexts, *, status='adopt', refs=None):
    return Preparation(candidates=[Candidate(candidate_id=f'candidate-{index}',
        claim='A possible scoped requirement.', status=status,
        rule=option_rule(frame, context), evidence_ids=['review-0'] if refs is None else refs)
        for index, context in enumerate(contexts)])


def mask_prep(frame, probes, mask, **kwargs):
    return prep(frame, [probe.context for index, probe in enumerate(probes) if mask & (1 << index)], **kwargs)


class ScopeDirectionTests(unittest.TestCase):
    def test_transfer_coverage_combines_equivalent_decompositions(self):
        frame, history, truth, probes = fixture({0: 0, 1: 1, 2: 1})
        fragments = mask_prep(frame, probes, 14)
        boundaries = {'task_family': 'work', 'workflow': 'workflow', 'version': 'v2'}
        overlapping = prep(frame, [{**boundaries, 'x': 'one'}, {**boundaries, 'y': 'one'}])
        left, right = score_scope(history, truth, fragments), score_scope(history, truth, overlapping)
        for score in (left, right):
            self.assertEqual(score['warranted_change_coverage'], 1)
            self.assertEqual(score['missed_warranted_transfer'], 0)
            self.assertEqual(score['unsupported_transfer'], 0)
            self.assertEqual(score['observed_contradiction'], 0)
            self.assertFalse(score['simplicity_association']['flag'])
        self.assertEqual(left['simplicity_association']['retained_effect_mask'],
                         right['simplicity_association']['retained_effect_mask'])
        self.assertEqual(score_preparation(history, truth, fragments)['content_error_count'], 0)

    def test_missed_transfer_is_set_level_not_error_in_each_valid_fragment(self):
        frame, history, truth, probes = fixture({0: 0, 1: 1, 2: 1})
        preparation = mask_prep(frame, probes, 6)  # Only the observed positive cells.
        result = score_preparation(history, truth, preparation)
        self.assertEqual(result['content_error_count'], 0)
        scope = result['scope_analysis']
        self.assertEqual(scope['missed_warranted_transfer'], 1)
        self.assertEqual(scope['observed_contradiction'], 0)
        self.assertEqual(scope['warranted_change_coverage'], 2 / 3)
        self.assertEqual(scope['cells'][3]['tags'], ['missed_warranted_transfer'])

    def test_unsupported_extension_and_observed_contradiction_are_distinct(self):
        frame, history, truth, probes = fixture({0: 0, 3: 1})
        scope = score_scope(history, truth, mask_prep(frame, probes, 15))
        self.assertEqual(scope['unsupported_transfer'], 2)
        self.assertEqual(scope['observed_contradiction'], 1)
        self.assertEqual(scope['cells'][0]['tags'], ['observed_contradiction'])
        self.assertFalse(scope['simplicity_association']['flag'])

    def test_missing_bad_reference_unrenderable_and_empty_are_distinct(self):
        frame, history, truth, probes = fixture({0: 0, 1: 1, 2: 1})
        bad_reference = mask_prep(frame, probes, 14, refs=['not-observed'])
        bad_operator = mask_prep(frame, probes, 14)
        bad_operator.candidates[0].rule = Rule(field='detail', operation='set_fact', value='unknown_fact',
                                              scope=bad_operator.candidates[0].rule.scope)
        for preparation in (None, bad_reference):
            scope = score_scope(history, truth, preparation)
            self.assertEqual(scope['assessed_cells'], 0)
            self.assertIsNone(scope['missed_warranted_transfer'])
            self.assertIsNone(scope['simplicity_association']['flag'])
        partial = score_scope(history, truth, bad_operator)
        self.assertEqual(partial['assessed_cells'], 3)
        self.assertIsNone(partial['warranted_change_coverage'])
        self.assertIsNone(partial['simplicity_association']['flag'])
        empty = score_scope(history, truth, Preparation())
        self.assertEqual(empty['assessed_cells'], 4)
        self.assertEqual(empty['missed_warranted_transfer'], 1)
        self.assertEqual(empty['observed_contradiction'], 2)

    def test_invalid_unresolved_reference_also_blocks_retained_guidance(self):
        frame, history, truth, probes = fixture({0: 0, 3: 1})
        preparation = mask_prep(frame, probes, 12)
        preparation.candidates.append(Candidate(candidate_id='unresolved', claim='Possible alternative',
            status='unresolved', rule=option_rule(frame, probes[1].context), evidence_ids=['unknown']))
        score = score_scope(history, truth, preparation)
        self.assertEqual(score['assessed_cells'], 0)
        self.assertIsNone(score['simplicity_association']['flag'])

    def test_resolved_retention_is_not_missed_transfer_when_baseline_is_kept(self):
        frame, history, truth, probes = fixture({0: 1, 1: 0, 2: 0})
        scope = score_scope(history, truth, mask_prep(frame, probes, 1))
        self.assertEqual(scope['cells'][3]['retention_basis'], 'resolved')
        self.assertEqual(scope['cells'][3]['effective_option'], 0)
        self.assertEqual(scope['missed_warranted_transfer'], 0)
        self.assertEqual(scope['warranted_change_coverage'], 1)


class SimplicityTests(unittest.TestCase):
    def test_all_tied_minima_preserved_without_inferred_motive(self):
        frame, history, truth, probes = fixture({0: 0, 3: 1})
        score = score_scope(history, truth, mask_prep(frame, probes, 12))
        marker = score['simplicity_association']
        self.assertTrue(marker['flag'])
        self.assertEqual(marker['compatible_function_count'], 4)
        self.assertEqual(marker['tied_minimum_masks'], [10, 12])
        self.assertEqual(marker['tied_minimum_count'], 2)
        self.assertEqual(marker['minimum_complexity'], 1)
        self.assertIn('not evidence of a causal strategy', marker['interpretation'])
        single_literal = prep(frame, [{'task_family': 'work', 'workflow': 'workflow', 'version': 'v2', 'x': 'one'}])
        self.assertEqual(score_scope(history, truth, single_literal)['simplicity_association'], marker)

    def test_complex_compatible_extension_is_not_minimum_pattern(self):
        frame, history, truth, probes = fixture({0: 0, 3: 1})
        score = score_scope(history, truth, mask_prep(frame, probes, 14))
        self.assertEqual(score['unsupported_transfer'], 2)
        self.assertFalse(score['simplicity_association']['flag'])

    def test_unresolved_simple_hypothesis_never_becomes_adopted_extension(self):
        frame, history, truth, probes = fixture({0: 0, 3: 1})
        adopted = mask_prep(frame, probes, 8)
        possible = Candidate(candidate_id='possible-x', claim='A possible simple explanation.',
            status='unresolved', rule=option_rule(frame, {'task_family': 'work', 'workflow': 'workflow',
            'version': 'v2', 'x': 'one'}), evidence_ids=['review-0', 'review-3'])
        adopted.candidates.append(possible)
        score = score_scope(history, truth, adopted)
        self.assertEqual(score['unsupported_transfer'], 0)
        self.assertFalse(score['simplicity_association']['flag'])

    def test_old_version_multiplicity_is_not_current_function_multiplicity(self):
        frame, history, truth, probes = fixture({0: 0, 1: 1, 2: 1}, old_version=True)
        self.assertEqual(len(truth.admissible_policies), 14)
        marker = score_scope(history, truth, mask_prep(frame, probes, 14))['simplicity_association']
        self.assertEqual(marker['compatible_function_count'], 1)
        self.assertEqual(marker['tied_minimum_masks'], [14])
        self.assertFalse(marker['flag'])

    def test_function_complexity_ignores_polarity_and_rule_count(self):
        self.assertEqual([policy_complexity(x) for x in (0, 15)], [0, 0])
        self.assertTrue(all(policy_complexity(x) == 1 for x in (3, 5, 10, 12)))
        self.assertTrue(all(policy_complexity(x) == 2 for x in (1, 2, 4, 7, 8, 11, 13, 14)))
        for checkerboard in (6, 9):
            with self.assertRaises(ValueError):
                policy_complexity(checkerboard)


class OutputDirectionTests(unittest.TestCase):
    def test_fields_and_actual_task_facts_determine_direction_not_label(self):
        frame, history, truth, probes = fixture({0: 0, 3: 1})
        task = probes[2].model_copy(update={'task_id': 'new-task', 'facts': {'title': 'Future'},
                     'baseline_fields': fields({'title': 'Future', 'detail': 'configured'})})
        policy = option_rule(frame, task.context)
        expected = TaskTruth(task_id=task.task_id, history_id='h14', probe='diagnostic',
                             expected_decision='keep', recoverable=False,
                             world_fields=fields({'title': 'Future'}))
        output = WorkOutput(task_id=task.task_id, decision='keep', applied_rules=[policy],
                            fields=fields({'title': 'Future'}))
        result = score_output(task, expected, truth, output, 'B', history=history)
        self.assertEqual(result['transfer_analysis']['tags'], ['unsupported_transfer'])
        self.assertFalse(result['decision_label_correct'])
        attribution = classify_error(result)
        self.assertTrue(attribution['provisional'])
        self.assertNotEqual(attribution['source'], 'human_review')
        missing = score_output(task, expected, truth, None, 'B', history=history)['transfer_analysis']
        self.assertFalse(missing['assessable'])
        self.assertFalse(missing['observed'])
        self.assertIsNone(missing['unsupported_transfer'])


class ProvenanceAndSummaryTests(unittest.TestCase):
    def test_explicit_unauthorised_and_rejection_sources_are_not_unknown_authority(self):
        extras = [{'id': 'unauthorised', 'actor': 'draft-author'},
                  {'id': 'rejected', 'decision': 'reject'},
                  {'id': 'unknown', 'authority_ref': 'missing-registry'}]
        frame, history, truth, probes = fixture({0: 0, 1: 1, 2: 1}, extra_records=extras)
        for record, error in (('unauthorised', True), ('rejected', True), ('unknown', False)):
            with self.subTest(record=record):
                preparation = mask_prep(frame, probes, 2, refs=[record])
                result = score_preparation(history, truth, preparation)
                self.assertEqual(result['candidates'][0]['evidence_basis_assessment']['has_error'], error)
        mixed = mask_prep(frame, probes, 2, refs=['unauthorised', 'review-1'])
        self.assertEqual(score_preparation(history, truth, mixed)['content_error_count'], 0)

    def test_scope_unknowns_do_not_become_zero_and_task_types_keep_six_denominator(self):
        rows, preparations = design_rows()
        result = aggregate(rows, preparations)
        self.assertTrue(result['design_valid'])
        self.assertEqual(result['by_task_type']['transfer_change']['C']['diagnostic']['n'], 6)
        group = result['scope_by_task_type']['transfer_change']['C1']
        self.assertEqual(group['planned_preparations'], 6)
        self.assertEqual(group['directions']['planned_cells_or_tasks'], 24)
        self.assertIsNone(group['simplicity_association_count'])
        self.assertIsNone(group['directions']['by_tag']['missed_warranted_transfer']['error_count'])
        self.assertIsNone(group['directions']['by_tag']['missed_warranted_transfer']['rate'])
        self.assertEqual(result['headroom']['S0']['C_correct'], 4)

    def test_report_distinguishes_material_contradiction_and_action_flip(self):
        rows, preparations = design_rows()
        result = aggregate(rows, preparations)
        result.update(source_sha256='test-source-binding', material_audits=[{
            'history_id': 'history-a', 'setting': 'S0', 'task_type': 'transfer_change',
            'counterfactual': {'required_outcome': 'contradiction', 'passed': True, 'by_type': {
                'forward': {'record_count': 2, 'action_flip': 0, 'contradiction': 1,
                            'unchanged_constraints': 1, 'narrower_same_actions': 0,
                            'retention_resolved': 0, 'unassessable': 0}}}}])
        with tempfile.TemporaryDirectory() as directory:
            text = write_report(Path(directory) / 'report.md', result, offline=True).read_text(encoding='utf-8')
        self.assertIn('test-source-binding', text)
        self.assertIn('forward | 2 | 0 | 1 | 1 | 0 | 0 | 0 | contradiction / True', text)
        self.assertIn('H14 excludes XOR and XNOR', text)
        self.assertIn('not prove a causal inference strategy', text)
        self.assertIn('undefined/undefined', text)


if __name__ == '__main__':
    unittest.main()
