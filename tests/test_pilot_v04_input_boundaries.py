"""Keep amendment-specific evaluator information outside every model input."""

import json
import unittest

from reflectai_v03.contracts import Preparation
from reflectai_v04.data import generate_future_tasks, generate_histories
from reflectai_v04.payloads import generation_payload, preparation_payload


PRIVATE_KEYS = {
    'world_policy', 'admissible_policies', 'oracle_audit', 'material_audit',
    'task_type', 'regime', 'diagnostic_context', 'control_context',
    'counterfactual_audit', 'candidate_targets', 'scope_probes',
}


def nested_keys(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from nested_keys(item)
    elif isinstance(value, list):
        for item in value:
            yield from nested_keys(item)
    elif isinstance(value, str):
        try:
            decoded = json.loads(value)
        except (ValueError, TypeError):
            return
        if isinstance(decoded, (dict, list)):
            yield from nested_keys(decoded)


class AmendmentInputBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = generate_histories(44901, split='test_fixture')

    def test_private_counterfactuals_and_subtypes_never_enter_payloads(self):
        for case in self.cases:
            with self.subTest(history=case.history.history_id):
                payloads = [preparation_payload(case.history),
                            preparation_payload(case.history, Preparation())]
                for task, _ in generate_future_tasks(case, 44902):
                    payloads.extend(generation_payload(task, case.history, arm,
                                                       Preparation() if arm == 'C' else None)
                                    for arm in ('A', 'B', 'C'))
                for payload in payloads:
                    self.assertFalse(PRIVATE_KEYS.intersection(nested_keys(payload)))

    def test_every_arm_receives_the_same_public_class_and_semantics(self):
        for case in self.cases:
            task, _ = generate_future_tasks(case, 44903)[0]
            payloads = [generation_payload(task, case.history, arm,
                                           Preparation() if arm == 'C' else None)
                        for arm in ('A', 'B', 'C')]
            for payload in payloads:
                self.assertEqual(json.loads(payload['initial_configuration'])['hypothesis_class'], 'h14')
                self.assertEqual(payload['assumptions'], case.history.assumptions)
            self.assertNotIn('history', payloads[0])
            self.assertEqual(payloads[1]['history']['records'],
                             case.history.model_dump(mode='json')['records'])
            self.assertNotIn('history', payloads[2])

    def test_private_case_rejected_instead_of_implicitly_projected(self):
        case = self.cases[0]
        with self.assertRaises(TypeError):
            preparation_payload(case)
        task, _ = generate_future_tasks(case, 44904)[0]
        with self.assertRaises(TypeError):
            generation_payload(task, case, 'B')


if __name__ == '__main__':
    unittest.main()
