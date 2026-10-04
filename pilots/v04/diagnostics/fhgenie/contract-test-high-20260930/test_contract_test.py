"""Offline tests for the contract-test harness. Transport, credential and HTTP are faked."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import contract_test as ct  # noqa: E402
from reflectai_v03.contracts import Preparation, WorkOutput  # noqa: E402
from reflectai_v04.backend import mock_response  # noqa: E402

PRIVATE_MARKERS = ('world_policy', 'expected_decision', 'admissible_policies', 'oracle_audit',
                   'material_audit', 'TaskTruth')


class FakeTransport:
    """Writes transport-like metadata; never launches a process or reads a key."""

    def __init__(self, modes=None, input_divisor=3, output_tokens=500, wall=12.0):
        self.modes, self.calls = modes or {}, []
        self.input_divisor, self.output_tokens, self.wall = input_divisor, output_tokens, wall

    def __call__(self, prompt, schema, output_dir, model, effort, timeout, *, max_output_tokens, executable):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=False)
        label = output_dir.name
        self.calls.append({'label': label, 'model': model, 'effort': effort, 'timeout': timeout,
                           'max_output_tokens': max_output_tokens, 'prompt': prompt})
        mode = self.modes.get(label, 'valid')
        contract = WorkOutput if '-gen-' in label else Preparation
        usage = {'input_tokens': len(prompt) // self.input_divisor, 'output_tokens': self.output_tokens,
                 'cached_input_tokens': None, 'reasoning_output_tokens': self.output_tokens // 2}
        metadata = {'status': 'completed', 'audit_issues': [], 'usage': usage, 'finish_reason': 'stop',
                    'wall_seconds': self.wall, 'system_fingerprint': 'offline-fp',
                    'actual_model': model, 'reasoning_content_present': True}
        response = mock_response(prompt, contract)
        if mode == 'big':
            usage['output_tokens'] = 300_000
        if mode == 'slow':
            metadata['wall_seconds'] = 400.0
        if mode == 'contract':
            response = {'unexpected': True}
        failures = {'invalid_json': ['response_invalid_json'], 'truncated': ['response_finish_invalid'],
                    'refusal': ['response_refusal'], 'unknown_usage': ['response_usage_unknown']}
        if mode in failures:
            metadata.update(status='process_failed', audit_issues=failures[mode])
            if mode == 'truncated':
                metadata['finish_reason'] = 'length'
                usage['output_tokens'] = max_output_tokens
            if mode == 'unknown_usage':
                usage.update(input_tokens=None, output_tokens=None)
            (output_dir / 'metadata.json').write_text(json.dumps(metadata), encoding='utf-8')
            raise ct.fhgenie_transport.InferenceRunError('offline failure')
        (output_dir / 'metadata.json').write_text(json.dumps(metadata), encoding='utf-8')
        return {'response': response, 'metadata': metadata}


class HarnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.material = ct.load_material()
        cls.shared = tempfile.TemporaryDirectory(prefix='v04-contract-test-')
        cls.pwsh = Path(cls.shared.name) / 'pwsh.exe'
        cls.pwsh.write_bytes(b'offline fixture; never executed')
        cls.plan = ct.build_plan(cls.pwsh, cls.material)
        cls.plan_bytes = ct.render_plan(cls.plan)

    @classmethod
    def tearDownClass(cls):
        cls.shared.cleanup()

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='v04-contract-run-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / 'plan.json').write_bytes(self.plan_bytes)

    def approve(self, **changes):
        approval = {'approved': True, 'reviewer': 'Milad Morad', 'date': '2026-09-30',
                    'response': 'offline fixture approval', 'reasoning_effort': 'high', 'planned_calls': 16,
                    'plan_sha256': ct.sha256_bytes(self.plan_bytes)} | changes
        (self.root / 'approval.json').write_text(json.dumps(approval), encoding='utf-8')

    def execute(self, transport):
        return ct.execute(self.pwsh, self.root, transport=transport, material=self.material)

    # Plan and material

    def test_plan_uses_development_seeds_high_reasoning_and_sixteen_fixed_calls(self):
        plan = self.plan
        self.assertEqual(plan['split'], 'development')
        self.assertEqual((plan['seeds']['history'], plan['seeds']['future'], plan['seeds']['order']),
                         (44321, 44322, 44323))
        self.assertFalse({44361, 44362, 44363} & {plan['seeds']['history'], plan['seeds']['future']})
        self.assertEqual(plan['reasoning_effort'], 'high')
        self.assertEqual(plan['next_level'], 'max')
        self.assertEqual((plan['max_output_tokens'], plan['timeout_seconds'], plan['retries']), (16384, 420, 0))
        self.assertEqual([c['label'] for c in plan['calls']], [
            '01-C1-C-H1', '02-C1-C-H2', '03-C1-C-H3', '04-C1-C-H4',
            '05-C2-C-H1', '06-C2-C-H2', '07-C2-C-H3', '08-C2-C-H4',
            '09-gen-C-H1', '10-gen-C-H2', '11-gen-C-H3', '12-gen-C-H4',
            '13-gen-B-H2', '14-gen-B-H4', '15-gen-A-H1', '16-gen-A-H3'])
        self.assertEqual({k: (v['setting'], v['family']) for k, v in plan['histories'].items()},
                         {'H1': ('S0', 'sales'), 'H2': ('S1', 'sales'),
                          'H3': ('S2', 'reporting'), 'H4': ('S5', 'retrieval')})
        self.assertEqual(plan['histories']['H3']['record_count'], 60)
        self.assertEqual(plan['histories']['H4']['record_count'], 60)

    def test_projection_base_covers_the_registered_192_calls(self):
        base = self.plan['projection_base']
        self.assertEqual(base['calls_by_type'], {'A': 48, 'B_large': 16, 'B_small': 32, 'C1_large': 8,
                                                 'C1_small': 16, 'C2_large': 8, 'C2_small': 16, 'C_gen': 48})
        self.assertEqual(sum(base['base_input_chars_by_type'].values()), base['base_input_chars_total'])
        self.assertEqual((base['c2_calls_with_previous_preparation'],
                          base['c_generation_calls_with_guidance']), (24, 48))

    def test_plan_is_deterministic_and_contains_no_evaluator_material(self):
        self.assertEqual(ct.render_plan(ct.build_plan(self.pwsh, ct.load_material())), self.plan_bytes)
        text = self.plan_bytes.decode('utf-8')
        for marker in PRIVATE_MARKERS:
            self.assertNotIn(marker, text)
        fixed = [c for c in self.plan['calls'] if c['prompt_sha256']]
        self.assertEqual([c['phase'] if c['phase'] != 'generate' else c['arm'] for c in fixed],
                         ['C1', 'C1', 'C1', 'C1', 'B', 'B', 'A', 'A'])

    def test_input_chars_match_the_actual_transport_messages(self):
        item = self.material['selected']['H4']
        prompt = ct.base_prompt('generate', 'B', item['case'].history, item['task'])
        schema = ct.schema_for('generate')[1]
        target = self.root / 'transport'
        endpoint = 'https://fhgenie.invalid/v1/chat/completions'  # offline fixture
        with patch.object(ct.fhgenie_transport, 'ENDPOINT_SHA256',
                          hashlib.sha256(endpoint.encode('utf-8')).hexdigest()), \
                patch.dict(os.environ, {ct.fhgenie_transport.ENDPOINT_ENV: endpoint}), \
                patch.object(ct.fhgenie_transport.subprocess, 'run',
                             side_effect=subprocess.TimeoutExpired('pwsh', 1)) as launch:
            with self.assertRaises(ct.fhgenie_transport.InferenceRunError):
                ct.fhgenie_transport.run_completion(prompt, schema, target, ct.FHGENIE_MODEL, 'high',
                                                    executable=str(self.pwsh))
        launch.assert_called_once()
        request = json.loads((target / 'request.json').read_text(encoding='utf-8'))
        self.assertEqual(request['reasoning_effort'], 'high')
        self.assertEqual(sum(len(m['content']) for m in request['messages']), ct.input_chars(prompt, schema))

    # Approval, reservation and plan binding

    def test_no_call_without_matching_approval(self):
        for changes in (None, {'approved': False}, {'plan_sha256': '0' * 64},
                        {'reasoning_effort': 'low'}, {'reasoning_effort': 'max'},
                        {'reviewer': 'someone else'}, {'response': ' '}):
            with self.subTest(changes=changes):
                (self.root / 'approval.json').unlink(missing_ok=True)
                if changes is not None:
                    self.approve(**changes)
                fake = FakeTransport()
                with self.assertRaises(PermissionError):
                    self.execute(fake)
                self.assertEqual(fake.calls, [])
                self.assertFalse((self.root / 'attempt.json').exists())

    def test_changed_plan_makes_no_call_and_no_reservation(self):
        (self.root / 'plan.json').write_bytes(self.plan_bytes.replace(b'"high"', b'"low"', 1))
        self.approve()
        fake = FakeTransport()
        with self.assertRaises(ValueError):
            self.execute(fake)
        self.assertEqual(fake.calls, [])
        self.assertFalse((self.root / 'attempt.json').exists())

    def test_approval_is_consumed_once(self):
        self.approve()
        self.execute(FakeTransport())
        second = FakeTransport()
        with self.assertRaises(PermissionError):
            self.execute(second)
        self.assertEqual(second.calls, [])

    # Execution

    def test_all_valid_run_passes_with_high_reasoning_and_single_attempts(self):
        self.approve()
        fake = FakeTransport()
        result = self.execute(fake)
        self.assertEqual(len(fake.calls), 16)
        self.assertEqual(len({c['label'] for c in fake.calls}), 16)
        self.assertEqual({(c['model'], c['effort'], c['timeout'], c['max_output_tokens']) for c in fake.calls},
                         {(ct.FHGENIE_MODEL, 'high', 420, 16384)})
        for call in fake.calls:
            for marker in PRIVATE_MARKERS:
                self.assertNotIn(marker, call['prompt'])
        self.assertEqual(result['decision']['verdict'], 'passed')
        self.assertEqual(result['decision']['valid'], 16)
        self.assertTrue(result['projection']['passes'])
        saved = (self.root / 'run' / 'results.json').read_text(encoding='utf-8')
        for marker in PRIVATE_MARKERS:
            self.assertNotIn(marker, saved)
        self.assertTrue((self.root / 'run' / 'REPORT.md').is_file())
        self.assertTrue((self.root / 'attempt.json').is_file())

    def test_fixed_prompts_equal_planned_hashes(self):
        self.approve()
        fake = FakeTransport()
        self.execute(fake)
        planned = {c['label']: c['prompt_sha256'] for c in self.plan['calls']}
        for call in fake.calls:
            if planned[call['label']]:
                self.assertEqual(ct.sha256_text(call['prompt']), planned[call['label']])

    def test_invalid_c1_blocks_dependants_and_format_failures_allow_escalation(self):
        self.approve()
        fake = FakeTransport({'01-C1-C-H1': 'invalid_json'})
        result = self.execute(fake)
        outcomes = {r['label']: (r['outcome'], r['reason']) for r in result['records']}
        self.assertEqual(outcomes['01-C1-C-H1'], ('invalid', 'invalid_json'))
        self.assertEqual(outcomes['05-C2-C-H1'], ('blocked', 'blocked_by_C1'))
        self.assertEqual(outcomes['09-gen-C-H1'], ('blocked', 'blocked_by_C2'))
        self.assertEqual(len(fake.calls), 14)
        self.assertEqual(result['decision']['invalid_including_blocked'], 3)
        self.assertEqual(result['decision']['verdict'], 'escalate_requires_new_approval')
        self.assertEqual(result['decision']['next_level'], 'max')

    def test_one_contract_failure_still_passes(self):
        self.approve()
        result = self.execute(FakeTransport({'16-gen-A-H3': 'contract'}))
        self.assertEqual(result['decision']['invalid_including_blocked'], 1)
        self.assertEqual(result['decision']['verdict'], 'passed')

    def test_truncations_stop_without_escalation(self):
        self.approve()
        result = self.execute(FakeTransport({'13-gen-B-H2': 'truncated', '14-gen-B-H4': 'truncated'}))
        self.assertEqual(result['decision']['limit_failures'], 2)
        self.assertEqual(result['decision']['verdict'], 'stop_no_escalation')

    def test_unknown_usage_stops_all_later_calls(self):
        self.approve()
        fake = FakeTransport({'03-C1-C-H3': 'unknown_usage'})
        result = self.execute(fake)
        self.assertEqual(len(fake.calls), 3)
        self.assertEqual(result['halt_reason'], 'response_usage_unknown')
        self.assertEqual(sum(r['outcome'] == 'not_attempted' for r in result['records']), 13)
        self.assertEqual(result['decision']['verdict'], 'stopped_systemic')

    def test_contract_token_stop_is_checked_between_calls(self):
        self.approve()
        fake = FakeTransport({'01-C1-C-H1': 'big', '02-C1-C-H2': 'big'})
        result = self.execute(fake)
        self.assertEqual(len(fake.calls), 2)
        self.assertEqual(result['halt_reason'], 'contract_token_limit')
        self.assertEqual(result['decision']['verdict'], 'stopped_token_limit')

    def test_slow_call_fails_runtime_criterion(self):
        self.approve()
        result = self.execute(FakeTransport({'14-gen-B-H4': 'slow'}))
        self.assertEqual(result['decision']['calls_over_wall_limit'], ['14-gen-B-H4'])
        self.assertEqual(result['decision']['verdict'], 'stop_runtime')

    # Pure rules

    def test_projection_arithmetic(self):
        base = {'calls_by_type': {'A': 2, 'C1_small': 1, 'C2_small': 1, 'C_gen': 1},
                'base_input_chars_total': 3000, 'c2_calls_with_previous_preparation': 1,
                'c_generation_calls_with_guidance': 1}

        def record(kind, phase, arm, chars, base_chars, inp, out, wall):
            return {'type': kind, 'phase': phase, 'arm': arm, 'input_chars': chars,
                    'base_input_chars': base_chars, 'wall_seconds': wall,
                    'usage': {'input_tokens': inp, 'output_tokens': out}}
        records = [record('A', 'generate', 'A', 400, 400, 100, 50, 10),
                   record('A', 'generate', 'A', 600, 600, 200, 70, 20),
                   record('C1_small', 'C1', 'C', 900, 900, 300, 1000, 30),
                   record('C2_small', 'C2', 'C', 1200, 900, 400, 2000, 40)]
        projection = ct.project(records, base)
        self.assertEqual(projection['chars_per_token_min'], 3.0)
        self.assertEqual(projection['input_tokens'], 1000)
        self.assertEqual(projection['output_tokens_by_type'],
                         {'A': 140, 'C1_small': 2000, 'C2_small': 2000, 'C_gen': 70})
        self.assertEqual(projection['extra_input_tokens'],
                         {'C2_previous_preparation': 100, 'C_generation_guidance': 16384})
        self.assertEqual(projection['projected_total_tokens'], 21694)
        self.assertEqual(projection['runtime_upper_estimate_seconds'], 530)

    def test_projection_without_usage_is_not_computable(self):
        self.assertFalse(ct.project([], self.plan['projection_base'])['passes'])

    def test_highest_level_never_escalates(self):
        records = [{'outcome': 'invalid', 'reason': 'invalid_json', 'label': str(i), 'wall_seconds': 1}
                   for i in range(2)] + [{'outcome': 'valid', 'reason': None, 'label': 'x', 'wall_seconds': 1}]
        self.assertEqual(ct.decide(records, {'passes': True}, 'max')['verdict'], 'unsuitable_stop')
        self.assertEqual(ct.decide(records, {'passes': False}, 'high')['verdict'], 'stop_no_escalation')
        self.assertEqual(ct.decide(records, {'passes': True}, 'high')['verdict'],
                         'escalate_requires_new_approval')


if __name__ == '__main__':
    unittest.main()
