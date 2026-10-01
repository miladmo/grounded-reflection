"""Offline execution contracts and failure safeguards. No real API calls."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from reflectai_v03.contracts import History, OutputField, Preparation, Record, Task, WorkOutput
from reflectai_v04.backend import Backend, BudgetStop, normalise_usage
from reflectai_v04.config import RunConfig
from reflectai_v04.payloads import generation_payload, preparation_payload, prompt_for
from reflectai_v04.storage import (digest, pending_approvals, seal, snapshot_sources,
                                  validate_approvals, verify_seal)


def history():
    return History(history_id='public-history', initial_configuration='Keep the baseline.',
                   assumptions='Synthetic fixture.', field_dictionary={'title': 'Text'},
                   records=[Record(record_id='r1', timestamp='2026-01-01', kind='review',
                                   actor='reviewer', context={'family': 'test'},
                                   observation='Fixture record.')])


def task():
    return Task(task_id='future-task', context={'family': 'test'}, facts={},
                baseline_fields=[OutputField(name='title', value='Baseline')], request='Prepare the title.')


class PayloadTests(unittest.TestCase):
    def test_preparation_has_no_task_or_private_truth(self):
        self.assertEqual(set(preparation_payload(history())), {'history'})
        self.assertEqual(set(preparation_payload(history(), Preparation())),
                         {'history', 'previous_preparation'})
        with self.assertRaises(TypeError):
            preparation_payload({'history': history(), 'world_policy': 'secret'})

    def test_arm_access_and_exclusion(self):
        a = generation_payload(task(), history(), 'A')
        b = generation_payload(task(), history(), 'B')
        c = generation_payload(task(), history(), 'C', Preparation())
        self.assertNotIn('history', a)
        self.assertIn('history', b)
        self.assertNotIn('history', c)
        self.assertEqual(c['instructions'], [])
        with self.assertRaises(ValueError):
            generation_payload(task(), history(), 'D', Preparation())

    def test_prompt_rejects_private_additions_before_reading_files(self):
        with self.assertRaises(ValueError):
            prompt_for('C1', {'history': {}, 'truth': 'secret'}, Path('unused'))


class BackendTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def call(self, backend, call_id='one'):
        return backend.complete('Prepare reusable guidance.', Preparation, self.root / call_id,
                                call_id=call_id, history_id='h1', arm='C', phase='C1')

    def test_mock_preserves_unknown_usage_and_never_calls_transport(self):
        with patch('reflectai_v04.backend.codex_backend.run_completion') as live:
            backend = Backend(RunConfig())
            record = self.call(backend)
        live.assert_not_called()
        self.assertEqual(record['status'], 'completed')
        self.assertIsNone(backend.budget_summary()['total_tokens'])
        self.assertEqual(backend.budget_summary()['calls_with_unknown_usage'], 1)

    def test_failure_consumes_budget_without_retry(self):
        backend = Backend(RunConfig(max_calls=1), failures={'one': 'failure'})
        self.assertEqual(self.call(backend)['status'], 'failed')
        with self.assertRaises(BudgetStop):
            self.call(backend, 'two')
        self.assertEqual(len(backend.records), 1)

    def test_same_call_cannot_be_replaced(self):
        backend = Backend(RunConfig())
        self.call(backend)
        with self.assertRaises(ValueError):
            self.call(backend)

    def test_live_requires_explicit_allow_flag(self):
        with self.assertRaises(ValueError):
            Backend(RunConfig(backend='codex', model='gpt-6-sol'))

    def test_unknown_live_usage_stops_after_one_mocked_completion(self):
        backend = Backend(RunConfig(backend='codex', model='gpt-6-sol'), allow_live=True)
        fake = {'response': Preparation().model_dump(),
                'metadata': {'status': 'completed', 'audit_issues': [], 'usage': None}}
        with patch('reflectai_v04.backend.codex_backend.run_completion', return_value=fake) as live:
            record = self.call(backend)
            with self.assertRaises(BudgetStop):
                self.call(backend, 'two')
        self.assertEqual(live.call_count, 1)
        self.assertTrue(record['fatal'])
        self.assertEqual(record['status'], 'failed')

    def test_tool_audit_failure_stops_and_discards_response(self):
        backend = Backend(RunConfig(backend='codex', model='gpt-6-sol'), allow_live=True)
        fake = {'response': Preparation().model_dump(),
                'metadata': {'status': 'completed', 'audit_issues': ['tool use'],
                             'usage': {'input_tokens': 10, 'output_tokens': 5}}}
        with patch('reflectai_v04.backend.codex_backend.run_completion', return_value=fake):
            record = self.call(backend)
        self.assertTrue(record['fatal'])
        self.assertIsNone(record['response'])

    def test_token_threshold_is_checked_between_calls(self):
        backend = Backend(RunConfig(backend='codex', model='gpt-6-sol', max_reported_tokens=10),
                          allow_live=True)
        fake = {'response': Preparation().model_dump(),
                'metadata': {'status': 'completed', 'audit_issues': [],
                             'usage': {'input_tokens': 9, 'output_tokens': 5,
                                       'cached_input_tokens': 4, 'reasoning_output_tokens': 3}}}
        with patch('reflectai_v04.backend.codex_backend.run_completion', return_value=fake):
            self.assertEqual(self.call(backend)['status'], 'completed')
            with self.assertRaises(BudgetStop):
                self.call(backend, 'two')
        self.assertEqual(backend.budget_summary()['reported_tokens'], 14)

    def test_bad_usage_does_not_become_zero(self):
        for raw in ({'input_tokens': True}, {'output_tokens': -1},
                    {'input_tokens': 2, 'cached_input_tokens': 3}):
            with self.assertRaises(ValueError):
                normalise_usage(raw)

    def test_forbidden_arm_rejected_before_attempt(self):
        backend = Backend(RunConfig())
        with self.assertRaises(ValueError):
            backend.complete('test', Preparation, self.root / 'd', call_id='d',
                             history_id='h', arm='D', phase='C1')
        self.assertFalse(backend.records)


class StorageTests(unittest.TestCase):
    def test_seal_detects_changed_added_and_removed_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            item = root / 'item.json'
            item.write_text('{}')
            seal(root, root / 'manifest.json')
            verify_seal(root, root / 'manifest.json')
            item.write_text('{"changed":true}')
            with self.assertRaises(ValueError):
                verify_seal(root, root / 'manifest.json')
            item.write_text('{}')
            (root / 'extra').write_text('extra')
            with self.assertRaises(ValueError):
                verify_seal(root, root / 'manifest.json')

    def test_snapshot_checks_copied_content(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / 'source.txt'
            source.write_text('original')
            def corrupt_copy(src, dst):
                dst.write_text('corrupted')
            with patch('reflectai_v04.storage.source_files', return_value={'source.txt': source}), \
                 patch('reflectai_v04.storage.shutil.copyfile', side_effect=corrupt_copy):
                with self.assertRaises(ValueError):
                    snapshot_sources(root / 'snapshot', root, root, source)

    def test_separate_human_approvals_and_exact_config_are_required(self):
        config = RunConfig().model_dump()
        approvals = pending_approvals('source', 'material')
        with self.assertRaises(ValueError):
            validate_approvals(approvals, source_hash='source', material_hash='material', config=config)
        # Unit-test fixture only, never exported as an actual human response.
        for key in ('materials', 'live'):
            approvals[key].update(approved=True, reviewer='Milad Morad', date='TEST FIXTURE',
                                  response='Synthetic unit-test approval, not real consent.')
        approvals['live']['config_sha256'] = digest(config)
        validate_approvals(approvals, source_hash='source', material_hash='material', config=config)
        with self.assertRaises(ValueError):
            validate_approvals(approvals, source_hash='changed', material_hash='material', config=config)


if __name__ == '__main__':
    unittest.main()
