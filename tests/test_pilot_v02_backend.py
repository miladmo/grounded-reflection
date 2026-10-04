"""Offline checks of attempt budgets, provenance and recorded inference."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from grounded_reflection.pilot_v02.backend import Backend, BudgetError
from grounded_reflection.pilot_v02.contracts import BackendConfig, Preparation, WorkOutput


class PilotBackendTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='reflection-v02-backend-')
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def invoke(self, backend, call_id='call-1', schema=Preparation, prompt='Prepare.', **kwargs):
        parameters = dict(arm='direct_adaptation', phase='prepare', family='sales', repetition=0)
        parameters.update(kwargs)
        return backend.complete(prompt, schema, self.root / call_id, call_id=call_id, **parameters)

    def live(self, **kwargs):
        return Backend(BackendConfig(backend='codex', model='test-model', **kwargs), allow_live=True)

    def reply(self, usage=None, response=None):
        return {'response': response if response is not None else {'requirements': [], 'notes': 'test'},
                'metadata': {'usage': usage, 'returned_model': 'test-model-returned'}}

    def test_mock_does_not_launch_transport_and_never_claims_measured_usage(self):
        backend = Backend(BackendConfig())
        with patch('grounded_reflection.codex_backend.run_completion') as transport:
            record = self.invoke(backend)
        transport.assert_not_called()
        self.assertEqual(record.status, 'completed')
        self.assertEqual(record.origin, 'offline_mock')
        self.assertEqual(record.response['requirements'], [])
        self.assertIn('Offline mock', record.response['notes'])
        self.assertIsNone(record.usage.input_tokens)
        self.assertIsNone(backend.budget_summary()['total_tokens'])
        self.assertEqual(backend.budget_summary()['calls_with_unknown_token_usage'], 1)
        self.assertFalse(backend.capabilities['strict_tokens'])
        self.assertFalse(backend.capabilities['compute_matched'])
        for filename in ('request.json', 'response.schema.json', 'response.json',
                         'record.json', 'usage.json', 'metadata.json'):
            self.assertTrue((self.root / 'call-1' / filename).is_file())

    def test_mock_generation_uses_only_public_facts_and_is_condition_independent(self):
        task = {'case_id': 'public-1', 'facts': {'recipient': 'Public person'},
                'output_fields': ['recipient', 'summary']}
        backend = Backend(BackendConfig())
        responses = []
        with patch('grounded_reflection.codex_backend.subprocess.run') as subprocess:
            for index, arm in enumerate(('no_adaptation', 'direct_evidence',
                                         'direct_adaptation', 'grounded_reflection')):
                prompt = 'Condition ' + arm + '\nPAYLOAD\n' + json.dumps({
                    'task': task, 'oracle': {'summary': 'ORACLE MUST NOT BE USED'},
                    'condition': arm,
                })
                record = self.invoke(backend, f'generate-{index}', WorkOutput, prompt,
                                     arm=arm, phase='validation')
                self.assertEqual(record.status, 'completed')
                responses.append(record.response)
        subprocess.assert_not_called()
        self.assertTrue(all(response == responses[0] for response in responses))
        self.assertEqual(responses[0]['fields'], [
            {'name': 'recipient', 'value': 'Public person'}, {'name': 'summary', 'value': ''}])
        self.assertNotIn('ORACLE', json.dumps(responses))

    def test_live_requires_explicit_opt_in_and_model(self):
        with self.assertRaisesRegex(ValueError, 'allow_live'):
            Backend(BackendConfig(backend='codex', model='test-model'))
        with self.assertRaisesRegex(ValueError, 'explicit model'):
            BackendConfig(backend='codex')
        with self.assertRaisesRegex(ValueError, 'allow_live'):
            Backend(BackendConfig(backend='codex', model='test-model'), allow_live=1)

    def test_reported_total_counts_input_and_output_not_their_subsets(self):
        backend = self.live(max_reported_tokens=100)
        usage = {'input_tokens': 80, 'output_tokens': 25,
                 'cached_input_tokens': 30, 'reasoning_output_tokens': 10}
        with patch('grounded_reflection.codex_backend.run_completion',
                   return_value=self.reply(usage)) as transport:
            record = self.invoke(backend)
            with self.assertRaisesRegex(BudgetError, 'token limit'):
                self.invoke(backend, 'refused')
        self.assertEqual(record.status, 'completed')
        self.assertEqual(transport.call_count, 1)
        self.assertEqual(backend.budget_summary()['reported_tokens'], 105)
        self.assertEqual(backend.budget_summary()['total_tokens'], 105)
        self.assertFalse((self.root / 'refused').exists())
        metadata = json.loads((self.root / 'call-1' / 'metadata.json').read_text())
        self.assertEqual(metadata['returned_model'], 'test-model-returned')
        self.assertFalse(metadata['capabilities']['provider_enforced_per_call_token_limit'])

    def test_partial_usage_remains_unknown_but_known_tokens_count(self):
        backend = self.live(max_reported_tokens=10)
        with patch('grounded_reflection.codex_backend.run_completion',
                   return_value=self.reply({'input_tokens': 10})):
            self.invoke(backend)
        summary = backend.budget_summary()
        self.assertEqual(summary['reported_tokens'], 10)
        self.assertIsNone(summary['total_tokens'])
        with self.assertRaises(BudgetError):
            self.invoke(backend, 'refused')

    def test_invalid_usage_is_failed_not_coerced_or_silently_accepted(self):
        invalid = [
            {'input_tokens': -1}, {'output_tokens': True}, {'input_tokens': 2.5},
            {'input_tokens': '12'}, {'input_tokens': 3, 'cached_input_tokens': 4},
            {'output_tokens': 2, 'reasoning_output_tokens': 5}, ['unknown'],
        ]
        backend = self.live()
        for index, usage in enumerate(invalid):
            with self.subTest(usage=usage), patch(
                'grounded_reflection.codex_backend.run_completion',
                return_value=self.reply(usage),
            ) as transport:
                record = self.invoke(backend, f'invalid-{index}')
                self.assertEqual(record.status, 'failed')
                self.assertIn('ValueError', record.error)
                self.assertEqual(transport.call_count, 1)
        self.assertEqual(backend.budget_summary()['failed_calls'], len(invalid))
        self.assertEqual(backend.budget_summary()['calls_with_unknown_token_usage'], len(invalid))

    def test_failure_records_count_across_phases_and_restored_ledger(self):
        backend = self.live(max_calls=2)
        with patch('grounded_reflection.codex_backend.run_completion',
                   side_effect=RuntimeError('transport failed')) as transport:
            failed = self.invoke(backend)
        self.assertEqual(transport.call_count, 1)
        self.assertEqual(failed.status, 'failed')
        self.assertIn('transport failed', failed.error)
        restored = Backend(backend.config, allow_live=True, prior_records=[failed])
        with patch('grounded_reflection.codex_backend.run_completion',
                   return_value=self.reply()) as transport:
            self.invoke(restored, 'second', phase='validation')
            with self.assertRaisesRegex(BudgetError, 'attempted calls'):
                self.invoke(restored, 'third', phase='final_test')
        self.assertEqual(transport.call_count, 1)
        self.assertEqual(restored.budget_summary()['attempted_calls'], 2)
        self.assertEqual(restored.budget_summary()['failed_calls'], 1)

    def test_failed_transport_usage_is_recovered_from_preserved_metadata(self):
        def fail(prompt, schema, run_dir, *args):
            run_dir.mkdir()
            (run_dir / 'metadata.json').write_text(json.dumps({
                'usage': {'input_tokens': 13, 'output_tokens': 4}, 'status': 'audit_failed'}))
            raise RuntimeError('audit rejected')

        backend = self.live()
        with patch('grounded_reflection.codex_backend.run_completion', side_effect=fail):
            record = self.invoke(backend)
        self.assertEqual(record.status, 'failed')
        self.assertEqual(backend.budget_summary()['reported_tokens'], 17)
        self.assertIn('audit rejected', record.error)

    def test_schema_failure_preserves_response_and_usage_without_repair(self):
        backend = self.live()
        with patch('grounded_reflection.codex_backend.run_completion', return_value=self.reply(
            {'input_tokens': 5, 'output_tokens': 3}, {'unexpected': 'invalid response'},
        )) as transport:
            record = self.invoke(backend)
        self.assertEqual(record.status, 'failed')
        self.assertEqual(transport.call_count, 1)
        self.assertEqual(backend.budget_summary()['reported_tokens'], 8)
        raw = json.loads((self.root / 'call-1' / 'response.json').read_text())
        self.assertEqual(raw, {'unexpected': 'invalid response'})

    def test_malformed_transport_metadata_is_a_recorded_failure(self):
        backend = self.live()
        with patch('grounded_reflection.codex_backend.run_completion', return_value={
            'response': {'requirements': [], 'notes': 'test'}, 'metadata': None,
        }) as transport:
            record = self.invoke(backend)
        self.assertEqual(record.status, 'failed')
        self.assertIn('metadata must be an object', record.error)
        self.assertEqual(transport.call_count, 1)
        self.assertIsNone(backend.budget_summary()['total_tokens'])

    def test_no_overwrite_or_duplicate_call_ids(self):
        backend = Backend(BackendConfig())
        record = self.invoke(backend)
        before = (self.root / 'call-1' / 'record.json').read_bytes()
        with self.assertRaisesRegex(ValueError, 'already recorded'):
            self.invoke(backend)
        another = Backend(BackendConfig())
        with self.assertRaises(FileExistsError):
            self.invoke(another)
        self.assertEqual(before, (self.root / 'call-1' / 'record.json').read_bytes())
        self.assertEqual(another.budget_summary()['attempted_calls'], 0)
        with self.assertRaisesRegex(ValueError, 'duplicate call IDs'):
            Backend(BackendConfig(), prior_records=[record, record])


if __name__ == '__main__':
    unittest.main()
