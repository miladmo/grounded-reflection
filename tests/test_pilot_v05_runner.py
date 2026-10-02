"""Offline tests for the v0.5 runner, D queries, budgets and live gating. No real calls."""

import glob
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
for location in (ROOT / 'src', ROOT / 'pilots/v03', ROOT / 'pilots/v04', ROOT / 'pilots/v05'):
    if str(location) not in sys.path:
        sys.path.insert(0, str(location))

from reflectai_v04 import fhgenie_transport  # noqa: E402
from reflectai_v05 import runner, storage  # noqa: E402
from reflectai_v05.backend import mock_response  # noqa: E402
from reflectai_v05.config import FHGENIE_MODEL, phase_config  # noqa: E402
from reflectai_v05.data import generate_histories  # noqa: E402
from reflectai_v05.dcontracts import AttributeValue, RecordQuery  # noqa: E402
from reflectai_v05.dquery import build_index, execute  # noqa: E402
from reflectai_v05.oracle import read_frame  # noqa: E402
from reflectai_v05.payloads import CALL_INPUT_CHARS, input_chars, prompt_for, schema_for  # noqa: E402

PRIVATE = ('"world"', 'hard_type', 'task_cells', 'oracle_status', 'expected_fields', '"confusable"', 'binding_records')


class MockRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='v05-run-')
        cls.root = Path(cls.temp.name)
        cls.result = runner.run(cls.root / 'calibration', phase_config('calibration'))

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def requests(self, name):
        return [json.loads(Path(p).read_text(encoding='utf-8')) for p in glob.glob(str(self.root / name / '**/request.json'), recursive=True)]

    def test_calibration_completes_with_registered_arms_and_histories(self):
        summary = self.result['summary']
        self.assertTrue(summary['complete'])
        rows = json.loads((self.root / 'calibration/results.json').read_text(encoding='utf-8'))['rows']
        self.assertEqual(len(rows), 8 * 4 * 3)  # 8 histories, 4 tasks, arms A/B/C
        self.assertEqual({r['arm'] for r in rows}, {'A', 'B', 'C'})
        hard = [r for r in rows if r['task_type'] in ('transfer_change', 'unidentifiable') and r['arm'] == 'B']
        self.assertEqual(len(hard), 8)
        self.assertIn('headroom', summary)

    def test_unidentifiable_breakdown_covers_every_arm(self):
        breakdown = self.result['summary']['unidentifiable_breakdown']
        arms = {key.split('|')[1] for key in breakdown}
        self.assertEqual(arms, {'A', 'B', 'C'})
        for key, counts in breakdown.items():
            for label in counts:
                self.assertIn('declared=', label)
                self.assertEqual('prep_unresolved=' in label, key.endswith('|C'))

    def test_every_prompt_is_within_budget_and_public(self):
        for record in glob.glob(str(self.root / 'calibration/**/record.json'), recursive=True):
            self.assertLessEqual(json.loads(Path(record).read_text(encoding='utf-8'))['input_chars'], CALL_INPUT_CHARS)
        for request in self.requests('calibration'):
            for marker in PRIVATE:
                self.assertNotIn(marker, request['prompt'])

    def test_preparations_never_see_future_tasks(self):
        tasks = json.loads((self.root / 'calibration/evaluator/future-tasks.json').read_text(encoding='utf-8'))
        task_ids = [item['task']['task_id'] for pairs in tasks.values() for item in pairs]
        for request in self.requests('calibration/preparation'):
            for task_id in task_ids:
                self.assertNotIn(task_id, request['prompt'])

    def test_seals_verify(self):
        storage.verify_seal(self.root / 'calibration/preparation', self.root / 'calibration/preparation/manifest.json')
        storage.verify_seal(self.root / 'calibration', self.root / 'calibration/manifest.json')

    def test_existing_output_is_never_resumed(self):
        with self.assertRaises(FileExistsError):
            runner.run(self.root / 'calibration', phase_config('calibration'))


class FailureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='v05-fail-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        cases = generate_histories(45021, 'development')
        self.small = next(c for c in cases if c.setting == 'K-S' and (c.hard_type, c.direction) == ('transfer_change', 'omit'))

    def test_response_failure_blocks_only_that_preparation(self):
        hid = self.small.history.history_id
        result = runner.run(self.root / 'r', phase_config('calibration'), failures={f'{hid}-C1-00': 'failure'})
        rows = json.loads((self.root / 'r/results.json').read_text(encoding='utf-8'))['rows']
        blocked = [r for r in rows if r['history_id'] == hid and r['arm'] == 'C']
        self.assertTrue(all(r['blocked_reason'] == 'C_preparation_unavailable' and not r['correct'] for r in blocked))
        self.assertTrue(result['summary']['complete'])
        self.assertEqual(result['summary']['budget']['response_failures'], 1)

    def test_systemic_failure_stops_and_keeps_denominators(self):
        hid = self.small.history.history_id
        result = runner.run(self.root / 's', phase_config('calibration'), failures={f'{hid}-C1-00': 'systemic'})
        rows = json.loads((self.root / 's/results.json').read_text(encoding='utf-8'))['rows']
        self.assertFalse(result['summary']['complete'])
        self.assertEqual(len(rows), 96)
        self.assertTrue(all(not r['correct'] for r in rows if r['blocked_reason']))


class QueryAndBudgetTests(unittest.TestCase):
    def test_query_filters_and_truncation(self):
        case = next(c for c in generate_histories(45021, 'development') if c.setting == 'U-L')
        frame = read_frame(case.history)
        name, values = next(iter(frame.attributes.items()))
        query = RecordQuery(query_id='q', attributes=[AttributeValue(attribute=name, value=values[0])],
                            event='review', decision='accept', reviewed_field=frame.field_option.field)
        full = execute(case.history, [query], 10 ** 9)[0]
        self.assertTrue(all(r['context'][name] == values[0] for r in full['records']))
        self.assertEqual(full['omitted_for_budget'], 0)
        small = execute(case.history, [query], 3_000)[0]
        self.assertEqual(small['matches_total'], full['matches_total'])
        self.assertEqual(len(small['records']) + small['omitted_for_budget'], small['matches_total'])
        index = build_index(case.history, frame)
        self.assertNotIn('records', {k for k in index if k != 'records_total'})
        self.assertEqual(index['records_total'], 240)

    def test_preparation_budget_reserves_one_round_and_the_final_call(self):
        budget = runner.PrepBudget(300_000)
        budget.used = 300_000 - 2 * runner.MAX_CALL_TOKENS
        self.assertTrue(budget.can_start_round(offline=False))
        budget.used += 1
        self.assertFalse(budget.can_start_round(offline=False))


class LiveGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='v05-live-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pwsh = self.root / 'pwsh.exe'
        self.pwsh.write_bytes(b'offline fixture')
        self.config = phase_config('dcheck', backend='fhgenie', model=FHGENIE_MODEL, pwsh_executable=str(self.pwsh),
                                   pwsh_sha256=hashlib.sha256(self.pwsh.read_bytes()).hexdigest())

    def approval(self, **changes):
        base = {'approved': True, 'reviewer': 'Milad Morad', 'phase': 'dcheck', 'date': '2026-10-02',
                'response': 'offline fixture', 'config_sha256': storage.digest(self.config.model_dump()),
                'source_sha256': storage.source_binding()['sha256']}
        return base | changes

    def test_no_or_mismatched_approval_makes_no_output(self):
        for approval in (None, self.approval(phase='main'), self.approval(config_sha256='0' * 64),
                         self.approval(reviewer='someone')):
            with self.subTest(approval=approval), self.assertRaises(PermissionError):
                runner.run(self.root / 'x', self.config, allow_live=True, approval=approval)
            self.assertFalse((self.root / 'x').exists())

    def test_matching_approval_is_reserved_once_and_uses_the_bound_transport(self):
        calls = []

        def fake(prompt, schema, output_dir, model, effort, timeout, *, max_output_tokens, executable):
            calls.append((model, effort, max_output_tokens, executable))
            stage = 'D-index' if 'hypothesis register for one target field' in prompt else (
                'D-round' if 'Continue maintaining' in prompt else 'D-final')
            return {'response': mock_response(stage, prompt),
                    'metadata': {'response_model': model, 'usage': {'input_tokens': 10, 'output_tokens': 5},
                                 'wall_seconds': 1.0}}
        folder = self.root / 'auth'
        with patch.object(fhgenie_transport, 'run_completion', side_effect=fake), \
                patch.object(runner, 'reserve', side_effect=lambda a, o: storage.reserve(a, o, folder)):
            result = runner.run(self.root / 'first', self.config, allow_live=True, approval=self.approval())
            self.assertTrue(result['summary']['complete'])
            with self.assertRaises(PermissionError):
                runner.run(self.root / 'second', self.config, allow_live=True, approval=self.approval())
        self.assertEqual({c[:3] for c in calls}, {(FHGENIE_MODEL, 'high', 32768)})
        self.assertEqual({c[3] for c in calls}, {str(self.pwsh)})

    def test_changed_powershell_binary_stops_before_reservation(self):
        self.pwsh.write_bytes(b'changed')
        with self.assertRaises(PermissionError):
            runner.run(self.root / 'y', self.config, allow_live=True, approval=self.approval())
        self.assertFalse((self.root / 'y').exists())


class TransportSyncTests(unittest.TestCase):
    def test_input_chars_match_the_bound_transport(self):
        endpoint = 'https://fhgenie.invalid/v1/chat/completions'
        prompt = prompt_for('generate', {'task': {'task_id': 't'}})
        with tempfile.TemporaryDirectory() as temp, \
                patch.object(fhgenie_transport, 'ENDPOINT_SHA256', hashlib.sha256(endpoint.encode()).hexdigest()), \
                patch.dict(os.environ, {fhgenie_transport.ENDPOINT_ENV: endpoint}), \
                patch.object(fhgenie_transport.subprocess, 'run', side_effect=subprocess.TimeoutExpired('pwsh', 1)):
            target = Path(temp) / 'call'
            pwsh = Path(temp) / 'pwsh.exe'
            pwsh.write_bytes(b'x')
            with self.assertRaises(fhgenie_transport.InferenceRunError):
                fhgenie_transport.run_completion(prompt, schema_for('generate'), target, FHGENIE_MODEL, 'high',
                                                 executable=str(pwsh))
            request = json.loads((target / 'request.json').read_text(encoding='utf-8'))
        self.assertEqual(sum(len(m['content']) for m in request['messages']), input_chars('generate', prompt))


if __name__ == '__main__':
    unittest.main()
