import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'pilots' / 'v03'))

from grounded_reflection.models import Scope
from reflectai_v03.context import generation_payload, render_rules, retained_rules
from reflectai_v03.contracts import Candidate, History, OutputField, Preparation, Record, Rule, Task


class ContextTests(unittest.TestCase):
    def setUp(self):
        self.task = Task(task_id='t', context={'workflow': 'report', 'family': 'research',
                                              'work_role': 'analyst'}, facts={'snapshot': 'L8'},
                         baseline_fields=[OutputField(name='title', value='Result')], request='Create title')
        self.history = History(history_id='h', initial_configuration='Use untagged title.',
            assumptions='Use baseline when evidence is unresolved.', field_dictionary={'title': 'Title'},
            records=[Record(record_id='e', timestamp='2026-01-01', kind='revision',
                            actor='r', context={'workflow': 'report'}, observation='Title accepted.')])
        self.rule = Rule(field='title', operation='append_fact', value='snapshot', separator=' | ',
                         scope=Scope(match={'workflow': ['report']}))

    def candidate(self, status):
        return Candidate(candidate_id=status, claim='Use title tag.', status=status,
                         rule=self.rule, evidence_ids=['e'], evidence_gap='SECRET GAP ask someone')

    def test_uncertainty_is_not_an_instruction_or_blocker(self):
        prep = Preparation(candidates=[self.candidate('unresolved'), self.candidate('reject')],
                           notes='SECRET GAP')
        for arm in ('C', 'D'):
            payload = generation_payload(self.task, self.history, arm, prep)
            self.assertEqual(payload['instructions'], [])
            self.assertNotIn('SECRET GAP', json.dumps(payload))
            self.assertNotIn('history', payload)
            self.assertEqual(render_rules(self.task, retained_rules(prep, self.history)), {'title': 'Result'})

    def test_supported_rule_applies_even_if_other_candidate_is_unresolved(self):
        prep = Preparation(candidates=[self.candidate('adopt'), self.candidate('unresolved')])
        self.assertEqual(render_rules(self.task, retained_rules(prep, self.history)), {'title': 'Result | L8'})

    def test_unknown_scope_does_not_apply_and_role_is_not_family(self):
        wrong = self.rule.model_copy(update={'scope': Scope(match={'work_role': ['research']})})
        missing = self.rule.model_copy(update={'scope': Scope(match={'audience': ['external']})})
        self.assertEqual(render_rules(self.task, [wrong, missing]), {'title': 'Result'})

    def test_contradictory_guidance_is_invalid_independent_of_order(self):
        other = self.rule.model_copy(update={'operation': 'omit', 'value': '', 'separator': ''})
        for rules in ([self.rule, other], [other, self.rule]):
            with self.assertRaisesRegex(ValueError, 'conflicting'):
                render_rules(self.task, rules)

    def test_fabricated_reference_rejected_for_either_preparation_arm(self):
        candidate = self.candidate('adopt')
        candidate.evidence_ids = ['fabricated']
        with self.assertRaisesRegex(ValueError, 'unknown evidence'):
            retained_rules(Preparation(candidates=[candidate]), self.history)

    def test_a_no_history_b_full_history(self):
        self.assertNotIn('history', generation_payload(self.task, self.history, 'A'))
        self.assertEqual(generation_payload(self.task, self.history, 'B')['history'],
                         self.history.model_dump(mode='json'))


if __name__ == '__main__':
    unittest.main()
