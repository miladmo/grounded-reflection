"""Prospective measurement tests using fresh fixtures, never historical run outputs."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'pilots' / 'v03'))
sys.path.insert(0, str(ROOT / 'src'))

from grounded_reflection.models import Scope
from reflectai_v03.context import render_rules
from reflectai_v03.contracts import (
    Candidate, HistoryTruth, OutputField, Policy, Preparation, Rule, Task, TaskTruth, WorkOutput,
)
from reflectai_v03.evaluation import aggregate, evaluate_output


def fields(values):
    return [OutputField(name=name, value=value) for name, value in values.items()]


def fixture(*, control=False, ambiguous=False):
    def task(name, artifact):
        return Task(task_id=name, context={'workflow': 'analysis', 'artifact': artifact},
                    facts={'snapshot': 'Q7', 'source': 'Source Q7'},
                    baseline_fields=fields({'title': 'Overview', 'source': 'Source Q7'}),
                    request='Prepare the structured exhibit.')

    chart, table = task('fresh-chart', 'chart'), task('fresh-table', 'table')
    change = Rule(field='title', operation='append_fact', value='snapshot', separator=' / ',
                  scope=Scope(match={'workflow': ['analysis'], 'artifact': ['chart']}))
    world = Policy(policy_id='private-world', rules=[change])
    truth = HistoryTruth(history_id='fresh-history', scenario_id='fixture', pair_id='fresh-pair',
                         world_policy=world,
                         admissible_policies=[world, Policy(policy_id='rival')] if ambiguous else [world],
                         candidate_targets=[], scope_probes=[chart, table])
    current = table if control else chart
    key = TaskTruth(task_id=current.task_id, history_id=truth.history_id,
                    probe='control' if control else 'diagnostic',
                    expected_decision='keep' if control or ambiguous else 'apply',
                    recoverable=not ambiguous,
                    world_fields=fields(render_rules(current, world.rules)))
    return current, key, truth, change


def preparation(*rules):
    return Preparation(candidates=[
        Candidate(candidate_id=f'candidate-{index}', claim='Fresh test fixture.',
                  status='adopt', rule=rule, evidence_ids=['observed-record'])
        for index, rule in enumerate(rules)
    ])


def response(task, rules=(), *, decision=None, actual=None, **kwargs):
    actual = render_rules(task, list(rules)) if actual is None else actual
    baseline = {field.name: field.value for field in task.baseline_fields}
    return WorkOutput(task_id=task.task_id, decision=decision or ('apply' if actual != baseline else 'keep'),
                      applied_rules=list(rules), fields=fields(actual), **kwargs)


class ProspectiveOutputMeasurementTests(unittest.TestCase):
    def test_idempotent_rule_with_apply_label_is_effectively_keep_in_every_arm(self):
        task, key, truth, _ = fixture(control=True)
        noop = Rule(field='source', operation='set_fact', value='source',
                    scope=Scope(match={'workflow': ['analysis']}))
        output = response(task, [noop], decision='apply')
        for arm in ('A', 'B', 'C', 'D'):
            with self.subTest(arm=arm):
                score = evaluate_output(task, key, truth, output, arm,
                                        preparation(noop) if arm in ('C', 'D') else None)
                self.assertTrue(score['update_correct'])
                self.assertTrue(score['world_compliant'])
                self.assertTrue(score['completed_deliverable'])
                self.assertTrue(score['execution_consistent'])
                self.assertFalse(score['decision_label_correct'])
                self.assertFalse(score['valid_output'])
                self.assertEqual(score['effective_decision'], 'keep')
                self.assertEqual(score['declared_decision'], 'apply')
                self.assertEqual(score['errors'], ['declared_decision_disagrees_with_fields'])

    def test_idempotent_rule_with_keep_label_is_allowed_and_strictly_valid(self):
        task, key, truth, _ = fixture(control=True)
        noop = Rule(field='source', operation='set_fact', value='source',
                    scope=Scope(match={'workflow': ['analysis']}))
        score = evaluate_output(task, key, truth, response(task, [noop], decision='keep'),
                                'C', preparation(noop))
        self.assertTrue(score['valid_output'])
        self.assertTrue(score['update_correct'])
        self.assertTrue(score['retained_rules_consistent'])

    def test_real_supported_change_gets_effect_credit_despite_keep_label(self):
        task, key, truth, change = fixture()
        output = response(task, [change], decision='keep')
        for arm in ('B', 'C', 'D'):
            with self.subTest(arm=arm):
                score = evaluate_output(task, key, truth, output, arm,
                                        preparation(change) if arm in ('C', 'D') else None)
                self.assertTrue(score['update_correct'])
                self.assertTrue(score['world_compliant'])
                self.assertEqual(score['effective_decision'], 'apply')
                self.assertFalse(score['decision_label_correct'])
                self.assertFalse(score['valid_output'])
        # Removing the label penalty does not grant A history-based warrant.
        a = evaluate_output(task, key, truth, output, 'A')
        self.assertFalse(a['update_correct'])
        self.assertTrue(a['world_compliant'])

    def test_uncertain_retention_with_wrong_label_stays_world_incorrect(self):
        task, key, truth, _ = fixture(ambiguous=True)
        score = evaluate_output(task, key, truth, response(task, decision='apply'), 'B')
        self.assertTrue(score['update_correct'])
        self.assertTrue(score['execution_consistent'])
        self.assertFalse(score['decision_label_correct'])
        self.assertFalse(score['world_compliant'])

    def test_correct_fields_with_broken_rule_metadata_get_world_credit_only(self):
        task, key, truth, change = fixture()
        world = render_rules(task, [change])
        missing_fact = Rule(field='title', operation='set_fact', value='not_a_fact',
                            scope=change.scope)
        nonapplicable = change.model_copy(update={'scope': Scope(match={'artifact': ['table']})})
        contradiction = Rule(field='title', operation='set_literal', value='Conflicting title',
                             scope=change.scope)
        for rules in ([], [missing_fact], [nonapplicable], [change, contradiction]):
            with self.subTest(rules=rules):
                output = response(task, rules, actual=world)
                score = evaluate_output(task, key, truth, output, 'B')
                self.assertTrue(score['world_compliant'])
                self.assertTrue(score['completed_deliverable'])
                self.assertFalse(score['update_correct'])
                self.assertFalse(score['execution_consistent'])
                self.assertFalse(score['valid_output'])

    def test_unknown_scope_noop_does_not_earn_update_credit(self):
        task, key, truth, _ = fixture(control=True)
        unknown = Rule(field='source', operation='set_fact', value='source',
                       scope=Scope(match={'unobserved_attribute': ['yes']}))
        output = response(task, [unknown], decision='keep')
        score = evaluate_output(task, key, truth, output, 'B')
        self.assertTrue(score['world_compliant'])
        self.assertFalse(score['execution_consistent'])
        self.assertFalse(score['update_correct'])
        self.assertIn('nonapplicable_applied_rule', score['errors'])

    def test_wrong_fields_cannot_be_rescued_by_either_decision_label(self):
        task, key, truth, change = fixture()
        wrong = Rule(field='title', operation='set_literal', value='Wrong title', scope=change.scope)
        for decision in ('apply', 'keep'):
            score = evaluate_output(task, key, truth, response(task, [wrong], decision=decision), 'B')
            self.assertFalse(score['update_correct'])
            self.assertFalse(score['world_compliant'])
            self.assertFalse(score['applied_rules_supported_on_scope_probes'])

    def test_preparation_and_scope_guards_survive_independent_world_measurement(self):
        task, key, truth, change = fixture()
        broad = change.model_copy(update={'scope': Scope(match={'workflow': ['analysis']})})
        for arm in ('C', 'D'):
            cases = [
                (response(task, [change]), Preparation()),
                (response(task, [change]), None),
                (response(task, [broad]), preparation(change)),
            ]
            for output, prep in cases:
                with self.subTest(arm=arm, prep=prep, rules=output.applied_rules):
                    score = evaluate_output(task, key, truth, output, arm, prep)
                    self.assertTrue(score['world_compliant'])
                    self.assertFalse(score['update_correct'])
                    self.assertFalse(score['retained_rules_consistent'])
        score = evaluate_output(task, key, truth, response(task, [broad]), 'B')
        self.assertFalse(score['update_correct'])
        self.assertFalse(score['applied_rules_supported_on_scope_probes'])
        self.assertTrue(score['world_compliant'])

    def test_missing_wrong_task_questions_and_incomplete_never_get_success(self):
        task, key, truth, change = fixture()
        correct = response(task, [change])
        invalid = [
            None, {},
            correct.model_copy(update={'task_id': 'another-task'}),
            correct.model_copy(update={'questions': ['Ask an employee?']}),
            correct.model_copy(update={'completed': False}),
        ]
        for output in invalid:
            with self.subTest(output=output):
                score = evaluate_output(task, key, truth, output, 'B')
                self.assertFalse(score['update_correct'])
                self.assertFalse(score['world_compliant'])
                self.assertFalse(score['completed_deliverable'])
        self.assertEqual(evaluate_output(task, key, truth, None, 'B')['effective_decision'], None)

    def test_omitted_required_field_and_extra_field_fail_world_compliance(self):
        task, key, truth, change = fixture()
        world = render_rules(task, [change])
        for actual in ({'title': world['title']}, {**world, 'invented': 'extra'}):
            score = evaluate_output(task, key, truth,
                                    response(task, [change], actual=actual), 'B')
            self.assertFalse(score['world_compliant'])
            self.assertFalse(score['update_correct'])

    def test_aggregate_keeps_label_diagnostics_out_of_effect_success(self):
        task, key, truth, _ = fixture(control=True)
        score = evaluate_output(task, key, truth, response(task, decision='apply'),
                                'C', Preparation())
        row = {'arm': 'C', 'scenario_id': 'fixture', 'pair_id': 'fresh-pair',
               'probe': 'diagnostic', 'expected_decision': 'keep', 'recoverable': True,
               'repetition': 0, **score}
        summary = aggregate([row])['by_arm']['C']['diagnostic']
        self.assertEqual(summary['update_correct'], 1)
        self.assertEqual(summary['world_compliant'], 1)
        self.assertEqual(summary['execution_consistent'], 1)
        self.assertEqual(summary['decision_label_correct'], 0)
        self.assertEqual(summary['valid_output'], 0)


if __name__ == '__main__':
    unittest.main()
