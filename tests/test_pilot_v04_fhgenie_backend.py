"""FHGenie integration regressions; every completion and approval is synthetic."""

import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
for location in (ROOT / 'src', ROOT / 'pilots/v03', ROOT / 'pilots/v04'):
    sys.path.insert(0, str(location))

from pydantic import ValidationError
from reflectai_v03.contracts import Preparation
from reflectai_v04 import runner, storage
from reflectai_v04.backend import RESPONSE_ISSUES, Backend, BudgetStop, write_json
from reflectai_v04.config import (DEVELOPMENT_FUTURE_SEED, DEVELOPMENT_HISTORY_SEED,
                                 FHGENIE_ENDPOINT, FHGENIE_MODEL, MATERIAL_REVISION,
                                 REVIEW_FUTURE_SEED, REVIEW_HISTORY_SEED, RunConfig)
from reflectai_v04.data import generate_histories
from reflectai_v04.storage import digest, pending_approvals, seal, source_binding, verify_seal


# Offline stand-in for the pinned PowerShell 7 binary; it is hashed, never executed.
_PWSH_FIXTURE = tempfile.TemporaryDirectory(prefix='v04-pwsh-fixture-')
PWSH = Path(_PWSH_FIXTURE.name) / 'pwsh.exe'
PWSH.write_bytes(b'offline PowerShell fixture; never executed')
PWSH_SHA256 = hashlib.sha256(PWSH.read_bytes()).hexdigest()


def fh_config(**overrides):
    values = dict(backend='fhgenie', model=FHGENIE_MODEL, reasoning_effort='high',
                  api_endpoint=FHGENIE_ENDPOINT, max_output_tokens=32768,
                  pwsh_executable=str(PWSH), pwsh_sha256=PWSH_SHA256)
    values.update(overrides)
    return RunConfig(**values)


def completion(**metadata):
    audit = {'backend': 'fhgenie', 'status': 'completed', 'audit_issues': [],
             'response_model': FHGENIE_MODEL,
             'usage': {'input_tokens': 11, 'output_tokens': 7}}
    audit.update(metadata)
    return {'response': Preparation(notes='Synthetic test fixture.').model_dump(),
            'metadata': audit}


class FHGenieConfigTests(unittest.TestCase):
    def test_registered_backends_and_limits(self):
        for config, live in ((RunConfig(), False),
                             (RunConfig(backend='codex', model='gpt-6-sol'), True),
                             (fh_config(), True)):
            with self.subTest(backend=config.backend):
                self.assertIs(config.is_live, live)
                self.assertNotIn('is_live', config.model_dump())
                self.assertEqual((config.max_calls, config.max_reported_tokens,
                                  config.timeout_seconds), (200, 6_000_000, 420))
                self.assertEqual(RunConfig.model_validate_json(config.model_dump_json()), config)
        self.assertIsNone(RunConfig().api_endpoint)
        self.assertIsNone(RunConfig().max_output_tokens)
        self.assertEqual(fh_config().max_output_tokens, 32768)
        self.assertEqual(fh_config().max_response_failures, 19)

    def test_fhgenie_requires_exact_model_reasoning_endpoint_and_output_limit(self):
        invalid = ({'model': 'gpt-6-sol'}, {'model': 'deepseek-ai/DeepSeek-V4-Flash'},
                   {'reasoning_effort': 'medium'}, {'reasoning_effort': 'low'},
                   {'reasoning_effort': 'max'}, {'api_endpoint': None},
                   {'pwsh_executable': None}, {'pwsh_sha256': None}, {'pwsh_sha256': 'ABC'},
                   {'max_response_failures': 20}, {'max_response_failures': -1},
                   {'api_endpoint': 'https://example.invalid/v1/chat/completions'},
                   {'max_output_tokens': None}, {'max_output_tokens': 2047},
                   {'max_output_tokens': 32769}, {'max_output_tokens': True},
                   {'max_output_tokens': '32768'}, {'max_output_tokens': 32768.0})
        for override in invalid:
            with self.subTest(override=override), self.assertRaises(ValidationError):
                fh_config(**override)
        self.assertEqual(fh_config(max_output_tokens=2048).max_output_tokens, 2048)

    def test_codex_and_mock_retain_registered_model_and_medium_reasoning(self):
        for backend, model in (('mock', 'offline-mock'), ('codex', 'gpt-6-sol')):
            for override in ({'reasoning_effort': 'high'}, {'api_endpoint': FHGENIE_ENDPOINT},
                             {'pwsh_executable': str(PWSH)}, {'pwsh_sha256': PWSH_SHA256},
                             {'max_output_tokens': 16384}, {'model': FHGENIE_MODEL}):
                values = dict(backend=backend, model=model)
                values.update(override)
                with self.subTest(values=values), self.assertRaises(ValidationError):
                    RunConfig(**values)


class FHGenieBackendTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.transport = patch('reflectai_v04.fhgenie_transport.run_completion',
                               return_value=completion()).start()
        self.codex = patch('reflectai_v04.backend.codex_backend.run_completion',
                           side_effect=AssertionError('No real Codex calls in this test.')).start()
        self.addCleanup(patch.stopall)

    def call(self, backend, call_id='one'):
        return backend.complete('Prepare synthetic guidance.', Preparation, self.root / call_id,
                                call_id=call_id, history_id='h1', arm='C', phase='C1')

    def test_live_flag_and_offline_failure_injection_gate_before_transport(self):
        with self.assertRaisesRegex(ValueError, 'explicit approval'):
            Backend(fh_config())
        with self.assertRaisesRegex(ValueError, 'offline only'):
            Backend(fh_config(), allow_live=True, failures={'one': 'failure'})
        self.transport.assert_not_called()
        self.codex.assert_not_called()

    def test_fhgenie_routes_one_call_with_registered_request_parameters(self):
        backend = Backend(fh_config(), allow_live=True)
        record = self.call(backend)
        self.assertEqual(record['status'], 'completed')
        self.assertEqual(record['origin'], 'model_generated')
        self.assertFalse(record['fatal'])
        self.assertEqual(record['usage']['input_tokens'], 11)
        self.assertIsNone(record['usage']['cached_input_tokens'])
        self.assertEqual(backend.budget_summary()['total_tokens'], 18)
        args, kwargs = self.transport.call_args
        self.assertEqual(args[0], 'Prepare synthetic guidance.')
        self.assertIsInstance(args[1], dict)
        self.assertEqual(args[2:], (self.root / 'one/transport', FHGENIE_MODEL, 'high', 420))
        self.assertEqual(kwargs, {'max_output_tokens': 32768, 'executable': str(PWSH)})
        self.transport.assert_called_once()
        self.codex.assert_not_called()
        request = json.loads((self.root / 'one/request.json').read_text(encoding='utf-8'))
        self.assertEqual(request['config']['api_endpoint'], FHGENIE_ENDPOINT)

    def test_offline_mock_never_dispatches_either_live_transport(self):
        record = self.call(Backend(RunConfig()))
        self.assertEqual(record['status'], 'completed')
        self.transport.assert_not_called()
        self.codex.assert_not_called()

    def test_unknown_usage_is_fatal_and_never_retried(self):
        self.transport.return_value = completion(usage={'input_tokens': 11, 'output_tokens': None})
        backend = Backend(fh_config(), allow_live=True)
        record = self.call(backend)
        self.assertEqual(backend.halt_reason, 'unknown_token_usage')
        self.assertTrue(record['fatal'])
        self.assertIsNone(record['response'])
        self.assertIsNone(backend.budget_summary()['total_tokens'])
        with self.assertRaises(BudgetStop):
            self.call(backend, 'two')
        self.transport.assert_called_once()
        self.assertFalse((self.root / 'two').exists())

    def test_wrong_or_missing_response_model_is_fatal(self):
        for index, response_model in enumerate(('other-model', None)):
            with self.subTest(response_model=response_model):
                self.transport.return_value = completion(response_model=response_model)
                backend = Backend(fh_config(), allow_live=True)
                record = self.call(backend, f'wrong-{index}')
                self.assertEqual(record['status'], 'failed')
                self.assertEqual(backend.halt_reason, 'transport_integrity_failure')
                self.assertTrue(record['fatal'])
                self.assertIsNone(record['response'])
                with self.assertRaises(BudgetStop):
                    self.call(backend, f'blocked-{index}')
        self.assertEqual(self.transport.call_count, 2)

    def test_audit_failure_and_invalid_usage_halt_further_dispatch(self):
        for index, metadata in enumerate(({'audit_issues': ['tool call']},
                                          {'status': 'process_failed'},
                                          {'usage': {'input_tokens': -1, 'output_tokens': 7}})):
            with self.subTest(metadata=metadata):
                self.transport.return_value = completion(**metadata)
                backend = Backend(fh_config(), allow_live=True)
                record = self.call(backend, f'bad-{index}')
                self.assertTrue(record['fatal'])
                self.assertIsNone(record['response'])
                with self.assertRaises(BudgetStop):
                    self.call(backend, f'blocked-{index}')
        self.assertEqual(self.transport.call_count, 3)

    def test_failed_transport_preserves_metadata_usage_and_stops(self):
        def failed(*args, **kwargs):
            transport_dir = args[2]
            transport_dir.mkdir()
            write_json(transport_dir / 'metadata.json', completion(status='timed_out')['metadata'])
            raise RuntimeError('Synthetic timeout, no request sent.')
        self.transport.side_effect = failed
        backend = Backend(fh_config(), allow_live=True)
        record = self.call(backend)
        self.assertTrue(record['fatal'])
        self.assertEqual(backend.halt_reason, 'systemic_transport_failure')
        self.assertEqual(backend.budget_summary()['total_tokens'], 18)
        with self.assertRaises(BudgetStop):
            self.call(backend, 'two')
        self.transport.assert_called_once()

    def test_reported_token_budget_remains_a_between_call_stop(self):
        backend = Backend(fh_config(max_reported_tokens=10), allow_live=True)
        self.assertEqual(self.call(backend)['status'], 'completed')
        with self.assertRaises(BudgetStop):
            self.call(backend, 'two')
        self.assertEqual(backend.budget_summary()['reported_tokens'], 18)
        self.transport.assert_called_once()


def failed_exchange(issue='response_invalid_json', **metadata):
    """Transport-like failure after a complete HTTP exchange (Amendment 5 fixtures)."""
    values = {'backend': 'fhgenie', 'status': 'process_failed', 'audit_issues': [issue],
              'http_status': 200, 'network_requests': 1, 'actual_model': FHGENIE_MODEL,
              'response_model': FHGENIE_MODEL, 'tool_use_detected': False,
              'finish_reason': 'length' if issue == 'response_finish_invalid' else 'stop',
              'usage': {'input_tokens': 11, 'output_tokens': 7}}
    values.update(metadata)

    def run(*args, **kwargs):
        transport_dir = args[2]
        transport_dir.mkdir()
        write_json(transport_dir / 'metadata.json', values)
        raise RuntimeError('Synthetic response failure, no request sent.')
    return run


class FHGenieResponseFailureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.transport = patch('reflectai_v04.fhgenie_transport.run_completion').start()
        self.addCleanup(patch.stopall)

    def call(self, backend, call_id):
        return backend.complete('Prepare synthetic guidance.', Preparation, self.root / call_id,
                                call_id=call_id, history_id='h1', arm='C', phase='C1')

    def test_isolated_response_failures_are_recorded_and_the_run_continues(self):
        for issue in sorted(RESPONSE_ISSUES):
            with self.subTest(issue=issue):
                self.transport.side_effect = failed_exchange(issue)
                backend = Backend(fh_config(), allow_live=True)
                record = self.call(backend, f'bad-{issue}')
                self.assertEqual((record['status'], record['failure_class']), ('failed', 'response'))
                self.assertFalse(record['fatal'])
                self.assertIsNone(backend.halt_reason)
                self.assertEqual(record['usage']['output_tokens'], 7)
                self.transport.side_effect = None
                self.transport.return_value = completion()
                self.assertEqual(self.call(backend, f'next-{issue}')['status'], 'completed')
                self.assertEqual(backend.budget_summary()['response_failures'], 1)

    def test_contract_violation_after_valid_json_counts_as_response_failure(self):
        self.transport.return_value = {'response': {'unexpected': True}, 'metadata': completion()['metadata']}
        backend = Backend(fh_config(), allow_live=True)
        record = self.call(backend, 'contract')
        self.assertEqual((record['status'], record['failure_class']), ('failed', 'response'))
        self.assertIsNone(backend.halt_reason)

    def test_twentieth_response_failure_stops_further_scheduling(self):
        self.transport.side_effect = failed_exchange()
        backend = Backend(fh_config(), allow_live=True)
        for index in range(19):
            self.assertFalse(self.call(backend, f'bad-{index}')['fatal'])
        self.assertIsNone(backend.halt_reason)
        last = self.call(backend, 'bad-19')
        self.assertTrue(last['fatal'])
        self.assertEqual(backend.halt_reason, 'response_failure_limit')
        with self.assertRaises(BudgetStop):
            self.call(backend, 'blocked')
        self.assertEqual(self.transport.call_count, 20)

    def test_reference_failure_counts_towards_the_limit(self):
        self.transport.return_value = completion()
        backend = Backend(fh_config(max_response_failures=0), allow_live=True)
        self.call(backend, 'c2')
        backend.register_reference_failure('c2')
        self.assertEqual(backend.budget_summary()['response_failures'], 1)
        self.assertEqual(backend.halt_reason, 'response_failure_limit')
        with self.assertRaises(ValueError):
            backend.register_reference_failure('c2')

    def test_incomplete_or_untrusted_exchanges_remain_systemic(self):
        cases = ({'usage': {'input_tokens': 11, 'output_tokens': None}},
                 {'actual_model': 'other-model'}, {'http_status': 500},
                 {'network_requests': 0}, {'tool_use_detected': True},
                 {'audit_issues': ['response_invalid_json', 'response_usage_invalid']},
                 {'audit_issues': ['http_completion_invalid']}, {'status': 'timed_out'})
        for index, metadata in enumerate(cases):
            with self.subTest(metadata=metadata):
                self.transport.side_effect = failed_exchange(**metadata)
                backend = Backend(fh_config(), allow_live=True)
                record = self.call(backend, f'systemic-{index}')
                self.assertTrue(record['fatal'])
                self.assertEqual(record['failure_class'], 'systemic')
                self.assertIsNotNone(backend.halt_reason)
                with self.assertRaises(BudgetStop):
                    self.call(backend, f'after-{index}')


class FHGenieRunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Development fixture only. Do not construct final-test material here.
        cls.cases = generate_histories(DEVELOPMENT_HISTORY_SEED, split='development')

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pilot = self.root / 'pilot'
        prompts = self.pilot / 'prompts'
        prompts.mkdir(parents=True)
        for name in ('prepare_C_v1.txt', 'review_C_v1.txt', 'generate_v1.txt', 'shared_contract_v1.txt'):
            shutil.copyfile(ROOT / 'pilots/v04/prompts' / name, prompts / name)
        self.protocol = self.root / 'fixture-protocol.md'
        self.protocol.write_text('Synthetic offline fixture; no actual human approval.\n', encoding='utf-8')
        files = {'docs/pilot-v04-protocol.md': self.protocol}
        files.update({f'pilots/v04/prompts/{item.name}': item for item in prompts.glob('*.txt')})
        patch('reflectai_v04.storage.source_files', return_value=files).start()
        patch('reflectai_v04.runner.generate_histories', return_value=self.cases).start()
        self.transport = patch('reflectai_v04.fhgenie_transport.run_completion',
                               return_value=completion()).start()
        self.codex = patch('reflectai_v04.backend.codex_backend.run_completion',
                           side_effect=AssertionError('No real Codex calls in this test.')).start()
        self.addCleanup(patch.stopall)

    def execute(self, config, name='run', **kwargs):
        return runner.run(self.root / name, config, repo=self.root, pilot=self.pilot,
                          protocol=self.protocol, **kwargs)

    def review_and_approval(self, config, *, history_ids=None, source_hash=None):
        review = self.root / 'review-fixture'
        review.mkdir()
        binding = source_binding(self.root, self.pilot, self.protocol)
        write_json(review / 'index.json', {
            'history_ids': history_ids or ['review-only-test-id'],
            'material_revision': MATERIAL_REVISION,
            'source_sha256': source_hash or binding['sha256']})
        manifest = seal(review, review / 'manifest.json')
        approval = pending_approvals(binding['sha256'], manifest['sha256'])
        for name in ('materials', 'live'):
            approval[name].update(approved=True, reviewer='Milad Morad', date='UNIT TEST ONLY',
                                  response='Synthetic fixture; not an actual human approval.')
        approval['live']['config_sha256'] = digest(config.model_dump())
        approval_path = self.root / 'fixture-approval.json'
        write_json(approval_path, approval)
        return review, approval_path, approval

    def test_missing_review_or_live_flag_stops_before_transport_or_output(self):
        for index, options in enumerate(({}, {'allow_live': True},
                                         {'allow_live': True, 'review_dir': self.root / 'absent'})):
            with self.subTest(options=options), self.assertRaisesRegex(ValueError, 'approval'):
                self.execute(fh_config(), name=f'blocked-{index}', **options)
            self.assertFalse((self.root / f'blocked-{index}').exists())
        self.transport.assert_not_called()
        self.codex.assert_not_called()
        self.assertFalse((self.pilot / '.authorizations').exists())

    def test_pending_material_or_live_approval_cannot_dispatch(self):
        config = fh_config(history_seed=5501, future_seed=5502)
        review, path, approval = self.review_and_approval(config)
        for name in ('materials', 'live'):
            candidate = json.loads(json.dumps(approval))
            candidate[name]['approved'] = None
            write_json(path, candidate)
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'actual .* approval'):
                self.execute(config, allow_live=True, review_dir=review, approval_path=path)
        self.transport.assert_not_called()
        self.assertFalse((self.root / 'run').exists())

    def test_changed_powershell_binary_stops_before_reservation_or_transport(self):
        config = fh_config(history_seed=5501, future_seed=5502, pwsh_sha256='0' * 64)
        review, path, _ = self.review_and_approval(config)
        with self.assertRaisesRegex(ValueError, 'PowerShell 7'):
            self.execute(config, allow_live=True, review_dir=review, approval_path=path)
        self.transport.assert_not_called()
        self.assertFalse((self.pilot / '.authorizations').exists())
        self.assertFalse((self.root / 'run').exists())

    def test_old_codex_configuration_approval_cannot_authorise_fhgenie(self):
        codex = RunConfig(backend='codex', model='gpt-6-sol', history_seed=5501, future_seed=5502)
        review, path, _ = self.review_and_approval(codex)
        frozen = path.read_bytes()
        with self.assertRaisesRegex(ValueError, 'exact run configuration'):
            self.execute(fh_config(history_seed=5501, future_seed=5502), allow_live=True,
                         review_dir=review, approval_path=path)
        self.assertEqual(path.read_bytes(), frozen)
        self.transport.assert_not_called()
        self.assertFalse((self.root / 'run').exists())

    def test_old_source_review_cannot_authorise_fhgenie(self):
        config = fh_config(history_seed=5501, future_seed=5502)
        review, path, _ = self.review_and_approval(config, source_hash='old-codex-source-binding')
        with self.assertRaisesRegex(ValueError, 'newly reviewed materials'):
            self.execute(config, allow_live=True, review_dir=review, approval_path=path)
        self.transport.assert_not_called()
        self.assertFalse((self.root / 'run').exists())

    def test_all_registered_development_and_review_seeds_remain_forbidden(self):
        candidates = [('history_seed', value) for value in
                      (4401, 4411, DEVELOPMENT_HISTORY_SEED, REVIEW_HISTORY_SEED)]
        candidates += [('future_seed', value) for value in
                       (4402, 4412, DEVELOPMENT_FUTURE_SEED, REVIEW_FUTURE_SEED)]
        config = fh_config(history_seed=5501, future_seed=5502)
        review, path, approval = self.review_and_approval(config)
        for key, value in candidates:
            values = {'history_seed': 5501, 'future_seed': 5502, key: value}
            candidate = fh_config(**values)
            approval['live']['config_sha256'] = digest(candidate.model_dump())
            write_json(path, approval)
            with self.subTest(key=key, value=value), self.assertRaisesRegex(ValueError, 'Live seeds'):
                self.execute(candidate, allow_live=True, review_dir=review, approval_path=path)
        self.transport.assert_not_called()
        self.assertFalse((self.pilot / '.authorizations').exists())

    def test_reviewed_history_overlap_stops_with_full_missing_denominators(self):
        config = fh_config(history_seed=5501, future_seed=5502, max_calls=1)
        review, path, _ = self.review_and_approval(config,
                                                  history_ids=[self.cases[0].history.history_id])
        result = self.execute(config, allow_live=True, review_dir=review, approval_path=path)
        self.assertIn('histories overlap', result['terminal_error']['message'])
        self.assertEqual(result['budget']['attempted_calls'], 0)
        self.assertEqual(result['blocked_generation_rows'], 144)
        self.assertEqual(result['blocked_preparation_rows'], 48)
        self.transport.assert_not_called()
        verify_seal(self.root / 'run', self.root / 'run/manifest.json')

    def test_copied_approval_cannot_authorise_a_second_output(self):
        config = fh_config(history_seed=5501, future_seed=5502, max_calls=1)
        review, path, approval = self.review_and_approval(config)
        copied = self.root / 'renamed-fixture-approval.json'
        shutil.copyfile(path, copied)
        reservation = self.pilot / '.authorizations' / f'{digest(approval)}.json'

        def fake(*args, **kwargs):
            self.assertTrue(reservation.is_file(), 'Reserve approval before transport/key access.')
            return completion()
        self.transport.side_effect = fake
        first = self.execute(config, name='first', allow_live=True, review_dir=review,
                             approval_path=path)
        frozen_reservation = reservation.read_bytes()
        second = self.execute(config, name='second', allow_live=True, review_dir=review,
                              approval_path=copied)
        self.assertEqual(first['budget']['attempted_calls'], 1)
        self.assertEqual(second['budget']['attempted_calls'], 0)
        self.assertEqual(second['terminal_error']['stage'], 'authorization_reservation')
        self.assertIn('already reserved', second['terminal_error']['message'])
        self.assertEqual(reservation.read_bytes(), frozen_reservation)
        self.transport.assert_called_once()
        for name, result in (('first', first), ('second', second)):
            self.assertEqual(result['report_type'], 'IncompleteReport')
            self.assertEqual(result['planned_calls'], 192)
            self.assertEqual(result['observed_generation_rows'], 144)
            verify_seal(self.root / name, self.root / name / 'manifest.json')


class FHGenieEntryPointAndBindingTests(unittest.TestCase):
    def test_cli_accepts_explicit_fhgenie_live_config_without_dispatching_inference(self):
        spec = importlib.util.spec_from_file_location('reflectai_v04_run_test', ROOT / 'pilots/v04/run.py')
        entry = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(entry)
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            config_path = directory / 'config.json'
            config_path.write_text(fh_config().model_dump_json(), encoding='utf-8')
            argv = ['run.py', 'live', '--output', str(directory / 'output'),
                    '--config', str(config_path), '--allow-live',
                    '--review-dir', str(directory / 'review'),
                    '--approvals', str(directory / 'approval.json')]
            with patch.object(sys, 'argv', argv), contextlib.redirect_stdout(io.StringIO()), \
                    patch.object(entry, 'run', return_value={
                        'offline': False, 'status': 'complete', 'planned_calls': 192,
                        'budget': {}, 'complete_schedule': True}) as mocked_runner:
                entry.main()
            self.assertEqual(mocked_runner.call_args.args[1].backend, 'fhgenie')
            self.assertTrue(mocked_runner.call_args.kwargs['allow_live'])

    def test_fhgenie_driver_harness_and_documentation_are_required_and_bound(self):
        required = ('docs/pilot-v04-fhgenie-transport.md',
                    'docs/pilot-v04-amendment-04.md', 'docs/pilot-v04-fhgenie-contract-test.md', 'docs/pilot-v04-amendment-05.md',
                    'pilots/v04/transport/fhgenie-request.ps1',
                    'pilots/v04/transport/test_fhgenie_request.ps1')
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            pilot = repo / 'pilots/v04'
            protocol = repo / 'docs/pilot-v04-protocol.md'
            relatives = [*storage.LEGACY_DEPENDENCIES, 'pilots/v04/run.py',
                         'pilots/v04/reflectai_v04/fhgenie_transport.py',
                         'docs/pilot-v04-protocol.md', 'docs/pilot-v04-amendment-03.md',
                         'docs/pilot-v04-surface-repair.md', 'docs/pilot-v04-transport-preflight.md',
                         'pilots/v04/transport/model-catalog.json',
                         'pilots/v04/transport/runtime-attestation.json', *required]
            for name in relatives:
                item = repo / name
                item.parent.mkdir(parents=True, exist_ok=True)
                item.write_text('Synthetic version-binding fixture.\n', encoding='utf-8')
            binding = source_binding(repo, pilot, protocol)
            self.assertIn('pilots/v04/reflectai_v04/fhgenie_transport.py', binding['files'])
            for name in required:
                with self.subTest(name=name):
                    self.assertIn(name, binding['files'])
                    item = repo / name
                    original = item.read_bytes()
                    item.write_text('Changed binding fixture.\n', encoding='utf-8')
                    self.assertNotEqual(source_binding(repo, pilot, protocol)['sha256'], binding['sha256'])
                    item.unlink()
                    with self.assertRaisesRegex(ValueError, 'source is missing'):
                        source_binding(repo, pilot, protocol)
                    item.write_bytes(original)


if __name__ == '__main__':
    unittest.main()
