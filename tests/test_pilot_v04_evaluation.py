"""Independent behavioural, provenance and accounting fixtures; no model calls."""

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
from reflectai_v03.contracts import (Candidate, History, HistoryTruth, OutputField,
    Policy, Preparation, Record, Rule, Task, TaskTruth, WorkOutput)
from reflectai_v04.data_contracts import FieldOption, PublicFrame
from reflectai_v04.evaluation import (aggregate, amortisation, classify_error,
    score_output, score_preparation)
from reflectai_v04.oracle import infer_policies
from reflectai_v04.report import write_report


def fields(**values):
    return [OutputField(name=name, value=value) for name, value in values.items()]


def task(name, recipient):
    return Task(task_id=name, context={'family': 'work', 'recipient': recipient},
                facts={'name': 'Ada'}, baseline_fields=fields(detail='configured', title='Memo'),
                request='Create the configured document.')


def rule(recipient=None, **kwargs):
    scope = {'family': ['work']}
    if recipient:
        scope['recipient'] = [recipient]
    return Rule(field=kwargs.get('field', 'detail'), operation=kwargs.get('operation', 'omit'),
                value=kwargs.get('value', ''), scope=Scope(match=scope))


def fixture(ambiguous=False):
    h = History(history_id='h', initial_configuration='Configured detail and title.',
                assumptions='Only the scoped accepted reviews establish changes.',
                field_dictionary={'detail': 'Detail text', 'title': 'Title'},
                records=[Record(record_id='e', timestamp='2026-01-01', kind='review',
                                actor='reviewer', context={'family': 'work', 'recipient': 'a'},
                                observation='Remove detail for a; retain it for b.')])
    p = Policy(policy_id='scoped', rules=[rule('a')])
    policies = [p, Policy(policy_id='baseline', rules=[])] if ambiguous else [p]
    t = HistoryTruth(history_id='h', scenario_id='independent', pair_id='pair',
                     world_policy=p, admissible_policies=policies, candidate_targets=[],
                     scope_probes=[task('pa', 'a'), task('pb', 'b')])
    return h, t


def candidate(name='c', status='adopt', inferred=None, evidence=None, counter=None):
    return Candidate(candidate_id=name, claim='A scoped operational hypothesis.', status=status,
                     rule=inferred or rule('a'), evidence_ids=['e'] if evidence is None else evidence,
                     counterevidence_ids=counter or [])


def design_rows():
    rows, preps = [], []
    for setting in range(6):
        for index, regime in enumerate(('change', 'change', 'resolved_keep', 'unidentifiable')):
            hid = f'S{setting}-h{index}'
            task_type = ('transfer_change', 'observed_change', 'resolved_retention_transfer', 'unidentifiable')[index]
            for arm in 'ABC':
                for probe in ('diagnostic', 'control'):
                    rows.append({'setting': f'S{setting}', 'history_id': hid, 'regime': regime,
                                 'task_type': task_type,
                                 'arm': arm, 'probe': probe, 'update_correct': True,
                                 'world_compliant': True})
            for phase in ('C1', 'C2'):
                preps.append({'setting': f'S{setting}', 'history_id': hid, 'phase': phase,
                              'task_type': task_type,
                              'analysis': {'preparation_present': True, 'candidate_count': 0,
                                           'content_error_count': 0, 'content_error_rate': None,
                                           'unassessable_count': 0, 'technical_candidate_count': 0}})
    return rows, preps


def call(name, arm, phase, tokens, probe=None, **kwargs):
    return {'call_id': name, 'history_id': 'h', 'arm': arm, 'phase': phase, 'probe': probe,
            'status': kwargs.get('status', 'completed'), 'usage': None if tokens is None else
            {'input_tokens': tokens - 10, 'output_tokens': 10,
             'cached_input_tokens': 5, 'reasoning_output_tokens': 4}}


def metered_calls():
    return [call('p1', 'C', 'C1', 100), call('p2', 'C', 'C2', 100),
            call('bd', 'B', 'generate', 200, 'diagnostic'),
            call('bc', 'B', 'generate', 100, 'control'),
            call('cd', 'C', 'generate', 100, 'diagnostic'),
            call('cc', 'C', 'generate', 100, 'control')]


class OutputTests(unittest.TestCase):
    def test_actual_effect_not_declared_label_and_noop_is_allowed(self):
        h, ht = fixture()
        t = task('t', 'b')
        tt = TaskTruth(task_id='t', history_id='h', probe='control', expected_decision='keep',
                       recoverable=True, world_fields=t.baseline_fields)
        noop = rule('b', operation='set_literal', value='configured')
        prep = Preparation(candidates=[candidate(inferred=noop)])
        out = WorkOutput(task_id='t', decision='apply', applied_rules=[noop], fields=t.baseline_fields)
        score = score_output(t, tt, ht, out, 'C', prep)
        self.assertTrue(score['update_correct'])
        self.assertTrue(score['world_compliant'])
        self.assertFalse(score['decision_label_correct'])
        self.assertEqual(score['effective_decision'], 'keep')

    def test_lucky_world_compliance_does_not_imply_warrant(self):
        h, ht = fixture(ambiguous=True)
        t = task('t', 'a')
        tt = TaskTruth(task_id='t', history_id='h', probe='diagnostic', expected_decision='keep',
                       recoverable=False, world_fields=fields(title='Memo'))
        out = WorkOutput(task_id='t', decision='apply', applied_rules=[rule('a')], fields=tt.world_fields)
        score = score_output(t, tt, ht, out, 'B')
        self.assertTrue(score['world_compliant'])
        self.assertFalse(score['update_correct'])
        self.assertTrue(score['unsupported_lucky_success'])

    def test_missing_wrong_identity_questions_and_incomplete_cannot_succeed(self):
        _, ht = fixture()
        t = task('t', 'b')
        tt = TaskTruth(task_id='t', history_id='h', probe='control', expected_decision='keep',
                       recoverable=True, world_fields=t.baseline_fields)
        base = WorkOutput(task_id='t', decision='keep', fields=t.baseline_fields)
        for output in (None, base.model_copy(update={'task_id': 'wrong'}),
                       base.model_copy(update={'questions': ['Please clarify?']}),
                       base.model_copy(update={'completed': False})):
            with self.subTest(output=output):
                score = score_output(t, tt, ht, output, 'B')
                self.assertFalse(score['world_compliant'])
                self.assertFalse(score['update_correct'])
        with self.assertRaises(ValueError):
            score_output(t, tt, ht, base, 'D')

    def test_faithful_execution_and_scope_support_remain_required(self):
        _, ht = fixture()
        t = task('t', 'a')
        tt = TaskTruth(task_id='t', history_id='h', probe='diagnostic', expected_decision='apply',
                       recoverable=True, world_fields=fields(title='Memo'))
        broad = rule()
        out = WorkOutput(task_id='t', decision='apply', applied_rules=[broad], fields=tt.world_fields)
        score = score_output(t, tt, ht, out, 'B')
        self.assertTrue(score['world_compliant'])
        self.assertFalse(score['update_correct'])
        self.assertFalse(score['applied_rules_supported_on_scope_probes'])


class CandidateTests(unittest.TestCase):
    def test_scope_content_error_persists_despite_success_on_local_future_task(self):
        h, ht = fixture()
        analysis = score_preparation(h, ht, Preparation(candidates=[candidate(inferred=rule())]))
        self.assertEqual(analysis['content_error_count'], 1)
        self.assertEqual(analysis['content_error_rate'], 1)
        self.assertEqual(analysis['candidates'][0]['effect_assessment'], 'reject')

    def test_unsafe_adoption_is_not_a_rejected_or_unresolved_candidate_error(self):
        h, ht = fixture(ambiguous=True)
        unresolved = score_preparation(h, ht, Preparation(candidates=[candidate(status='unresolved')]))
        rejected = score_preparation(h, ht, Preparation(candidates=[candidate(status='reject')]))
        self.assertEqual(unresolved['content_error_count'], 0)
        self.assertEqual(rejected['content_error_count'], 1)
        self.assertEqual(rejected['candidates'][0]['content_error_tags'], ['rejects_still_admissible_hypothesis'])
        rejected_broad = score_preparation(h, ht, Preparation(candidates=[candidate(status='reject', inferred=rule())]))
        self.assertEqual(rejected_broad['content_error_count'], 0)

    def test_narrow_rules_need_no_exact_target_and_unknown_refs_are_technical(self):
        h, ht = fixture()
        analysis = score_preparation(h, ht, Preparation(candidates=[candidate(evidence=['unknown'])]))
        self.assertEqual(analysis['content_error_count'], 0)
        self.assertEqual(analysis['technical_candidate_count'], 1)
        self.assertFalse(analysis['candidates'][0]['traceable'])
        self.assertEqual(analysis['candidates'][0]['semantic_grounding'], 'pending_review')

    def test_empty_missing_uncovered_and_bad_fields_do_not_get_false_zero_rate(self):
        h, ht = fixture()
        for prep in (None, Preparation(), Preparation(candidates=[candidate(inferred=rule('unseen'))]),
                     Preparation(candidates=[candidate(inferred=rule(field='invalid'))])):
            with self.subTest(preparation=prep):
                score = score_preparation(h, ht, prep)
                self.assertIsNone(score['content_error_rate'])
                self.assertEqual(score['content_error_count'], 0)

    def test_wrong_operator_cannot_be_assumed_to_be_content_error(self):
        h, ht = fixture()
        prep = Preparation(candidates=[candidate(inferred=rule('a', operation='set_literal', value='nonsense'))])
        result = score_preparation(h, ht, prep)
        self.assertEqual(result['content_error_count'], 0)
        self.assertEqual(result['pending_semantic_attribution_count'], 1)
        self.assertIsNone(result['content_error_rate'])


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.frame = PublicFrame(task_family='work', workflow='process', as_of='2026-06-01T00:00:00Z',
            dimensions={'recipient': ['a', 'b'], 'form': ['x', 'y']},
            field_option=FieldOption(field='detail', operation='omit'),
            baseline_template={'detail': 'configured', 'title': '{title}'},
            fact_descriptions={'title': 'Document title'})
        records = []

        def add(name, event, context=None, when='2026-05-01T00:00:00Z', actor='reviewer'):
            records.append(Record(record_id=name, timestamp=when, kind='review', actor=actor,
                                  context=context or {}, observation=json.dumps(event)))

        for version, start, end in (('v1', '2025-01-01T00:00:00Z', '2026-01-01T00:00:00Z'),
                                     ('v2', '2026-01-01T00:00:00Z', '2027-01-01T00:00:00Z')):
            add('register-' + version, {'event': 'register_version', 'version': version,
                'workflow': 'process', 'task_family': 'work', 'valid_from': start,
                'valid_until': end, 'authorised_reviewers': ['reviewer']}, when=start)
        self.context = {'task_family': 'work', 'workflow': 'process', 'version': 'v2',
                        'recipient': 'a', 'form': 'x'}
        review = {'event': 'review', 'authority_ref': 'register-v2', 'decision': 'accept',
                  'reviewed_fields': ['detail'], 'format': 'interpreted',
                  'accepted_fields': {'title': 'Memo'}, 'facts': {'title': 'Memo'}}
        for recipient in ('a', 'b'):
            for form in ('x', 'y'):
                add(f'current-{recipient}{form}', review, {**self.context, 'recipient': recipient, 'form': form})
        add('old', {**review, 'authority_ref': 'register-v1'}, {**self.context, 'version': 'v1'},
            when='2025-06-01T00:00:00Z')
        add('comment', {'event': 'comment', 'text': 'Omit detail.'}, self.context)
        add('tool', {'event': 'execution', 'text': 'Omit detail.'}, self.context)
        add('copy', {'event': 'forward', 'origin_ref': 'current-ax'}, self.context)
        add('old-copy', {'event': 'forward', 'origin_ref': 'old'}, self.context)
        self.history = History(history_id='provenance', initial_configuration=self.frame.model_dump_json(),
            assumptions='Only registered authoritative reviews warrant changes within their version.',
            field_dictionary={'detail': 'Optional detail field', 'title': 'Title'}, records=records)
        oracle = infer_policies(self.history)
        probes = [Task(task_id=f'p-{version}-{r}-{f}', context={**self.context, 'version': version,
                          'recipient': r, 'form': f}, facts={'title': 'Memo'},
                       baseline_fields=fields(detail='configured', title='Memo'), request='Create memo.')
                  for version in ('v1', 'v2') for r in ('a', 'b') for f in ('x', 'y')]
        self.truth = HistoryTruth(history_id='provenance', scenario_id='fixture', pair_id='fixture',
            world_policy=oracle.policies[0], admissible_policies=oracle.policies,
            candidate_targets=[], scope_probes=probes)
        self.rule = Rule(field='detail', operation='omit', scope=Scope(match={
            key: [value] for key, value in self.context.items()}))

    def assess(self, refs, counter=None, inferred=None):
        prep = Preparation(candidates=[candidate(inferred=inferred or self.rule, evidence=refs, counter=counter)])
        return score_preparation(self.history, self.truth, prep)

    def test_non_authoritative_basis_counts_even_when_rule_is_correct(self):
        for reference in ('comment', 'tool', 'register-v2'):
            with self.subTest(reference=reference):
                result = self.assess([reference])
                self.assertEqual(result['candidates'][0]['effect_assessment'], 'adopt')
                self.assertEqual(result['content_error_count'], 1)
                self.assertIn('evidence_basis_error', result['candidates'][0]['content_error_tags'])

    def test_old_only_current_support_is_error_but_not_counterevidence(self):
        self.assertEqual(self.assess(['old'])['content_error_count'], 1)
        self.assertEqual(self.assess(['old-copy'])['content_error_count'], 1)
        self.assertEqual(self.assess(['current-ax'], ['old'])['content_error_count'], 0)
        self.assertEqual(self.assess(['old', 'current-ax'])['content_error_count'], 0)

    def test_valid_copy_inherits_origin_and_old_scope_remains_valid(self):
        result = self.assess(['copy', 'current-ax'])
        self.assertEqual(result['content_error_count'], 0)
        self.assertEqual(result['candidates'][0]['unique_cited_roots'], 1)
        old_rule = self.rule.model_copy(update={'scope': Scope(match={
            key: ['v1'] if key == 'version' else [value] for key, value in self.context.items()})})
        self.assertEqual(self.assess(['old'], inferred=old_rule)['content_error_count'], 0)


class AggregateTests(unittest.TestCase):
    def test_fixed_denominators_and_pairing_do_not_drop_missing_rows(self):
        rows, preps = design_rows()
        good = aggregate(rows, preps)
        self.assertTrue(good['design_valid'], good['design_errors'])
        partial = aggregate(rows[:-1], preps)
        self.assertFalse(partial['design_valid'])
        self.assertEqual(partial['by_arm']['C']['control']['n'], 24)
        self.assertEqual(partial['by_arm']['C']['control']['update_correct'], 23)
        self.assertIsNone(partial['headroom']['S0']['qualifies'])
        duplicated = aggregate(rows + [rows[0]], preps)
        self.assertFalse(duplicated['design_valid'])
        self.assertEqual(duplicated['by_arm']['A']['diagnostic']['update_correct'], 24)

    def test_pure_content_gate_keeps_mixed_and_unknown_in_denominator(self):
        rows, preps = design_rows()
        c = [r for r in rows if r['setting'] == 'S0' and r['arm'] == 'C' and r['probe'] == 'diagnostic']
        for row, category in zip(c[:3], ('content', 'content', 'mixed')):
            row.update(update_correct=False, error_attribution={'category': category, 'provisional': False,
                                                               'admissible_categories': [category]})
        result = aggregate(rows, preps)
        self.assertTrue(result['headroom']['S0']['qualifies'])
        self.assertEqual(result['headroom']['S0']['required_content_errors'], 2)
        c[1]['error_attribution'] = {'category': 'content', 'provisional': True,
                                      'admissible_categories': ['content', 'technical']}
        self.assertIsNone(aggregate(rows, preps)['headroom']['S0']['qualifies'])
        c[1]['error_attribution'] = {'category': 'mixed', 'provisional': False,
                                      'admissible_categories': ['mixed']}
        final = aggregate(rows, preps)['headroom']['S0']
        self.assertFalse(final['qualifies'])
        self.assertEqual(final['failure_attribution']['mixed_inclusive_sensitivity'], 1)

    def test_two_failures_require_two_content_and_controls_do_not_affect_gate(self):
        rows, preps = design_rows()
        for row in rows:
            if row['setting'] == 'S0' and row['arm'] == 'C':
                if row['probe'] == 'control' or row['history_id'].endswith(('h0', 'h1')):
                    row.update(update_correct=False, error_attribution={'category': 'content',
                        'provisional': False, 'admissible_categories': ['content']})
        result = aggregate(rows, preps)
        self.assertTrue(result['headroom']['S0']['qualifies'])
        self.assertEqual(result['headroom']['S0']['failure_attribution']['failure_count'], 2)

    def test_candidate_stages_and_history_mean_are_not_pooled(self):
        rows, preps = design_rows()
        preps[0]['analysis'].update(candidate_count=1, content_error_count=1, content_error_rate=1)
        preps[2]['analysis'].update(candidate_count=9, content_error_count=0, content_error_rate=0)
        result = aggregate(rows, preps)['candidate_analysis']['S0']
        self.assertEqual(result['C1']['mean_defined_history_rate'], .5)
        self.assertEqual(result['C1']['pooled_confirmed_lower_bound'], .1)
        self.assertIsNone(result['C2']['mean_defined_history_rate'])

    def test_four_failures_need_three_content_errors(self):
        rows, preps = design_rows()
        selected = [r for r in rows if r['setting'] == 'S0' and r['arm'] == 'C'
                    and r['probe'] == 'diagnostic']
        for row, category in zip(selected, ('content', 'content', 'technical', 'unresolved')):
            row.update(update_correct=False, error_attribution={'category': category,
                       'provisional': False, 'admissible_categories': [category]})
        result = aggregate(rows, preps)['headroom']['S0']
        self.assertEqual(result['required_content_errors'], 3)
        self.assertFalse(result['qualifies'])
        selected[3]['error_attribution'] = {'category': 'content', 'provisional': False,
                                           'admissible_categories': ['content']}
        self.assertTrue(aggregate(rows, preps)['headroom']['S0']['qualifies'])

    def test_unrelated_preparation_error_does_not_manufacture_task_cause(self):
        success = classify_error({'update_correct': True}, {'content_error_count': 3})
        self.assertIsNone(success['category'])
        failure = classify_error({'update_correct': False, 'errors': ['missing_or_invalid_output']},
                                 {'content_error_count': 3}, call_status='failed')
        self.assertEqual(failure['category'], 'technical')
        self.assertFalse(failure['provisional'])
        with self.assertRaises(ValueError):
            classify_error({'update_correct': False}, reviewed_category='content', reviewer='')


class ResourceTests(unittest.TestCase):
    def test_strict_inequality_mix_scenarios_and_subset_accounting(self):
        result = amortisation(metered_calls())
        scenarios = result['by_history']['h']['scenarios']
        self.assertEqual(scenarios['diagnostic_only']['first_strictly_cheaper_N'], 3)
        self.assertIsNone(scenarios['control_only']['first_strictly_cheaper_N'])
        self.assertEqual(scenarios['mix_50_50']['first_strictly_cheaper_N'], 5)
        self.assertEqual(result['reported_total_tokens'], 700)
        self.assertEqual(result['by_arm_phase']['C/C1']['total_tokens'], 100)

    def test_unknown_usage_and_failed_calls_are_not_zero_or_dropped(self):
        records = metered_calls()
        records[0]['status'] = 'failed'
        result = amortisation(records)
        self.assertEqual(result['by_history']['h']['failed_calls'], 1)
        self.assertEqual(result['by_history']['h']['preparation_tokens'], 200)
        records[1]['usage'] = None
        result = amortisation(records)
        self.assertIsNone(result['reported_total_tokens'])
        self.assertFalse(result['by_history']['h']['scenarios']['mix_50_50']['available'])
        self.assertEqual(result['unknown_or_invalid_usage_calls'], 1)

    def test_unknown_token_subsets_do_not_invalidate_known_input_output_total(self):
        records = metered_calls()
        records[0]['usage']['cached_input_tokens'] = None
        records[0]['usage']['reasoning_output_tokens'] = None
        result = amortisation(records)
        self.assertEqual(result['reported_total_tokens'], 700)
        self.assertIsNone(result['by_arm_phase']['C/C1']['cached_input_tokens'])
        self.assertTrue(result['by_history']['h']['scenarios']['mix_50_50']['available'])

    def test_invalid_subsets_duplicate_calls_and_wrong_arm_are_not_accepted(self):
        records = metered_calls()
        records[0]['usage']['cached_input_tokens'] = 1000
        self.assertEqual(amortisation(records)['unknown_or_invalid_usage_calls'], 1)
        with self.assertRaises(ValueError):
            amortisation(records + [records[0]])
        records[0]['arm'] = 'D'
        with self.assertRaises(ValueError):
            amortisation(records)

    def test_mock_report_keeps_limits_and_writes_once(self):
        rows, preps = design_rows()
        result = aggregate(rows, preps)
        result['amortisation'] = amortisation(metered_calls())
        with tempfile.TemporaryDirectory() as directory:
            path = write_report(Path(directory) / 'report.md', result, offline=True)
            text = path.read_text(encoding='utf-8')
            self.assertIn('OFFLINE MOCK', text)
            self.assertIn('no model efficacy evidence', text)
            self.assertIn('not measure professional quality', text)
            self.assertIn('semantic grounding', text)
            self.assertIn('first strictly cheaper integer', text)
            self.assertIn('not comparable', text)
            self.assertIn('No v0.5 mechanism is selected', text)
            with self.assertRaises(FileExistsError):
                write_report(path, result, offline=True)


if __name__ == '__main__':
    unittest.main()
