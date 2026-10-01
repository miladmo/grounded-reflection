"""Offline runner regressions. Synthetic approvals are unit-test fixtures only."""

import json
from pathlib import Path
import random
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
for location in (ROOT / 'src', ROOT / 'pilots/v03', ROOT / 'pilots/v04'):
    sys.path.insert(0, str(location))

from reflectai_v03.contracts import Preparation
from reflectai_v04 import runner, storage
from reflectai_v04.backend import Backend, write_json
from reflectai_v04.config import (DEVELOPMENT_FUTURE_SEED, DEVELOPMENT_HISTORY_SEED,
                                 DEVELOPMENT_ORDER_SEED, MATERIAL_REVISION,
                                 REVIEW_FUTURE_SEED, REVIEW_HISTORY_SEED, RunConfig)
from reflectai_v04.data import generate_future_tasks, generate_histories
from reflectai_v04.review import export_review
from reflectai_v04.storage import digest, pending_approvals, seal, source_binding, verify_seal


class RunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = generate_histories(DEVELOPMENT_HISTORY_SEED, split='development')

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pilot = self.root / 'pilot'
        prompts = self.pilot / 'prompts'
        prompts.mkdir(parents=True)
        for name in ('prepare_C_v1.txt', 'review_C_v1.txt', 'generate_v1.txt',
                     'shared_contract_v1.txt'):
            shutil.copyfile(ROOT / 'pilots/v04/prompts' / name, prompts / name)
        self.source = self.root / 'fixture-source.py'
        self.source.write_text('# Synthetic runner test source.\n', encoding='utf-8')
        self.protocol = self.root / 'fixture-protocol.md'
        self.protocol.write_text('Offline unit-test fixture only.\n', encoding='utf-8')
        self.amendment = self.root / 'pilot-v04-amendment-03.md'
        self.amendment.write_text('Approved amendment fixture, not actual human approval.\n', encoding='utf-8')
        self.surface_repair = self.root / 'pilot-v04-surface-repair.md'
        self.surface_repair.write_text('Surface repair fixture, not actual human approval.\n', encoding='utf-8')
        files = {'fixture-source.py': self.source, 'docs/pilot-v04-protocol.md': self.protocol,
                 'docs/pilot-v04-amendment-03.md': self.amendment,
                 'docs/pilot-v04-surface-repair.md': self.surface_repair}
        files.update({f'pilots/v04/prompts/{item.name}': item for item in prompts.glob('*.txt')})
        self.addCleanup(patch.stopall)
        patch('reflectai_v04.storage.source_files', return_value=files).start()
        patch('reflectai_v04.runner.generate_histories', return_value=self.cases).start()
        self.transport = patch('reflectai_v04.backend.codex_backend.run_completion',
                               side_effect=AssertionError('No real model calls in runner tests.')).start()

    def execute(self, name='run', config=None, **kwargs):
        output = self.root / name
        result = runner.run(output, config or RunConfig(), repo=self.root, pilot=self.pilot,
                            protocol=self.protocol, **kwargs)
        return output, result

    def read(self, output, name):
        return json.loads((output / name).read_text(encoding='utf-8'))

    def assert_full_incomplete(self, output, result, attempted):
        self.assertEqual(result['report_type'], 'IncompleteReport')
        self.assertFalse(result['complete_schedule'])
        self.assertEqual(result['planned_calls'], 192)
        self.assertEqual(result['planned_generation_rows'], 144)
        self.assertEqual(result['observed_generation_rows'], 144)
        self.assertEqual(result['budget']['attempted_calls'], attempted)
        self.assertEqual(len(self.read(output, 'planned-calls.json')), 192)
        self.assertEqual(len(self.read(output, 'scores.json')), 144)
        self.assertEqual(len(self.read(output, 'candidate-scores.json')), 48)
        for setting in result['by_setting'].values():
            for arm in setting.values():
                self.assertEqual(arm['diagnostic']['n'], 4)
                self.assertEqual(arm['control']['n'], 4)
        self.assertTrue((output / 'incomplete-report.json').is_file())
        verify_seal(output, output / 'manifest.json')

    def test_full_mock_uses_snapshot_and_exports_reviewable_blind_inputs(self):
        output = self.root / 'run'
        prompt_paths = []
        actual_prompt = runner.prompt_for
        future_calls = []

        def prompt(stage, payload, directory):
            prompt_paths.append(directory)
            if stage in ('C1', 'C2'):
                self.assertNotIn('task', payload)
            return actual_prompt(stage, payload, directory)

        def future(case, seed):
            self.assertTrue((output / 'F1.json').is_file())
            verify_seal(output / 'preparation', output / 'preparation/manifest.json')
            self.assertEqual(len(list((output / 'preparation/calls').iterdir())), 48)
            future_calls.append(case.history.history_id)
            return generate_future_tasks(case, seed)

        with patch('reflectai_v04.runner.prompt_for', side_effect=prompt), \
             patch('reflectai_v04.runner.generate_future_tasks', side_effect=future):
            _, result = self.execute()
        self.assertTrue(result['complete_schedule'])
        self.assertTrue(result['design_valid'])
        self.assertEqual(result['budget']['attempted_calls'], 192)
        self.assertEqual(result['material_revision'], MATERIAL_REVISION)
        audits = {row['history_id']: row for row in result['material_audits']}
        for case in self.cases:
            self.assertEqual(audits[case.history.history_id]['counterfactual'], case.material_audit['counterfactual'])
            self.assertEqual(audits[case.history.history_id]['task_type'], case.material_audit['task_type'])
        for row in self.read(output, 'candidate-scores.json'):
            self.assertEqual(row['task_type'], audits[row['history_id']]['task_type'])
            self.assertIn('scope_analysis', row['analysis'])
        for row in self.read(output, 'scores.json'):
            self.assertEqual(row['task_type'], audits[row['history_id']]['task_type'])
            self.assertIn('transfer_analysis', row)
        self.assertEqual(len(set(future_calls)), 24)
        self.assertEqual(set(prompt_paths), {output / 'sources/pilots/v04/prompts'})
        self.transport.assert_not_called()
        sample = self.read(output, 'human_review/blinded-outputs.json')
        key = self.read(output, 'human_review/key.json')
        by_key = {item['sample_id']: item for item in key}
        histories = {case.history.history_id: case.history.model_dump(mode='json') for case in self.cases}
        self.assertEqual(len(sample), 24)
        for item in sample:
            identity = by_key[item['sample_id']]
            self.assertEqual(item['history'], histories[identity['history_id']])
            self.assertEqual(item['task']['task_id'], identity['task_id'])
            self.assertEqual(set(item['preparations']), {'preparation_1', 'preparation_2'})
            self.assertTrue(all(value is not None for value in item['preparations'].values()))
            self.assertIsNotNone(item['response'])
            self.assertFalse({'setting', 'family', 'regime', 'task_type', 'counterfactual', 'truth', 'gold', 'arm',
                              'expected_decision', 'analysis', 'world_policy'} & set(item))
            self.assertNotIn('truth', item['history'])
        frozen_manifest = (output / 'manifest.json').read_bytes()
        with self.assertRaises(FileExistsError):
            self.execute()
        self.assertEqual((output / 'manifest.json').read_bytes(), frozen_manifest)
        verify_seal(output, output / 'manifest.json')

    def test_source_mutation_stops_after_one_call_and_keeps_denominators(self):
        original = Backend.complete

        def mutate(backend, *args, **kwargs):
            record = original(backend, *args, **kwargs)
            self.source.write_text('# Changed after a frozen call.\n', encoding='utf-8')
            return record

        with patch.object(Backend, 'complete', new=mutate), \
             patch('reflectai_v04.runner.generate_future_tasks') as future:
            output, result = self.execute()
        self.assert_full_incomplete(output, result, 1)
        self.assertEqual(result['terminal_error']['stage'], 'source_verification')
        self.assertEqual(result['blocked_generation_rows'], 144)
        self.assertFalse(result['design_valid'])
        self.assertTrue(all(row['qualifies'] is None for row in result['headroom'].values()))
        future.assert_not_called()
        self.assertFalse((output / 'F1.json').exists())
        rows = self.read(output, 'scores.json')
        self.assertTrue(all(row['blocked'] and row['task_id'] is None for row in rows))
        self.assertTrue(all(not row['update_correct'] and not row['world_compliant'] for row in rows))

    def test_snapshot_prompt_tampering_cannot_change_the_first_request(self):
        original = runner.snapshot_sources

        def corrupt(destination, *args):
            binding = original(destination, *args)
            (destination / 'pilots/v04/prompts/prepare_C_v1.txt').write_text('tampered', encoding='utf-8')
            return binding

        with patch('reflectai_v04.runner.snapshot_sources', side_effect=corrupt):
            output, result = self.execute()
        self.assert_full_incomplete(output, result, 0)
        self.assertEqual(result['terminal_error']['stage'], 'snapshot_prompt_verification')
        self.transport.assert_not_called()

    def test_snapshot_creation_failure_has_a_terminal_report(self):
        with patch('reflectai_v04.runner.snapshot_sources', side_effect=ValueError('snapshot copy race')):
            output, result = self.execute()
        self.assert_full_incomplete(output, result, 0)
        self.assertEqual(result['terminal_error']['stage'], 'source_snapshot')
        self.assertTrue(all(not row['material_available'] for row in self.read(output, 'scores.json')))

    def test_history_generation_failure_preserves_fixed_slots_without_fake_truth(self):
        with patch('reflectai_v04.runner.generate_histories', side_effect=ValueError(
                'material generation failed: setting=S2, family=sales, seed=123')) as generator, \
             patch('reflectai_v04.runner.generate_future_tasks') as future:
            output, result = self.execute()
        generator.assert_called_once()
        future.assert_not_called()
        self.assert_full_incomplete(output, result, 0)
        self.assertEqual(result['terminal_error']['stage'], 'history_material_generation')
        self.assertIn('seed=123', self.read(output, 'terminal-error.json')['message'])
        rows = self.read(output, 'scores.json')
        self.assertEqual(len({row['slot_id'] for row in rows}), 24)
        self.assertTrue(all(row['expected_decision'] is None and row['task_id'] is None for row in rows))
        self.assertTrue(all(row['blocking_reason'] == 'history_material_generation' for row in rows))

    def test_bad_preparation_seal_blocks_future_material_and_all_generation(self):
        def tamper(directory, manifest):
            result = seal(directory, manifest)
            if directory.name == 'preparation':
                (directory / 'histories.json').write_text('[]', encoding='utf-8')
            return result

        with patch('reflectai_v04.runner.seal', side_effect=tamper), \
             patch('reflectai_v04.runner.generate_future_tasks') as future:
            output, result = self.execute()
        self.assert_full_incomplete(output, result, 48)
        self.assertEqual(result['terminal_error']['stage'], 'preparation_seal_verification')
        future.assert_not_called()
        self.assertEqual(result['blocked_generation_rows'], 144)

    def test_future_generation_failure_preserves_partial_material_without_redraw(self):
        seen = []

        def future(case, seed):
            seen.append(seed)
            if len(seen) == 2:
                raise ValueError('fixed future seed cannot generate')
            return generate_future_tasks(case, seed)

        with patch('reflectai_v04.runner.generate_future_tasks', side_effect=future):
            output, result = self.execute()
        self.assert_full_incomplete(output, result, 48)
        self.assertEqual(seen, [DEVELOPMENT_FUTURE_SEED, DEVELOPMENT_FUTURE_SEED + 1])
        self.assertEqual(result['terminal_error']['stage'], 'future_material_generation')
        self.assertEqual(len(self.read(output, 'evaluator/future-tasks.json')), 1)
        rows = self.read(output, 'scores.json')
        self.assertEqual(sum(row['task_material_available'] for row in rows), 6)
        self.assertTrue(all(row['blocked'] for row in rows))

    def test_isolated_failed_C1_blocks_only_its_scheduled_dependants(self):
        order = list(self.cases)
        random.Random(DEVELOPMENT_ORDER_SEED).shuffle(order)
        hid = order[0].history.history_id
        output, result = self.execute(failures={f'{hid}-C1': 'failure'})
        self.assert_full_incomplete(output, result, 189)
        self.assertIsNone(result['terminal_error'])
        self.assertEqual(result['budget']['failed_calls'], 1)
        self.assertEqual(result['blocked_generation_rows'], 2)
        rows = [row for row in self.read(output, 'scores.json') if row['history_id'] == hid]
        self.assertTrue(all(row['call_status'] == 'completed' for row in rows if row['arm'] in ('A', 'B')))
        self.assertTrue(all(row['blocked'] and not row['update_correct'] for row in rows if row['arm'] == 'C'))

    def test_live_approval_copy_cannot_authorise_another_output_directory(self):
        # The live transport is mocked; these responses are not human consent.
        config = RunConfig(backend='codex', model='gpt-6-sol', history_seed=5501,
                           future_seed=5502, max_calls=1)
        review = self.root / 'review-fixture'
        review.mkdir()
        binding = source_binding(self.root, self.pilot, self.protocol)
        write_json(review / 'index.json', {'history_ids': ['review-only-test-id'],
                                         'material_revision': MATERIAL_REVISION,
                                         'source_sha256': binding['sha256']})
        review_seal = seal(review, review / 'manifest.json')
        approval = pending_approvals(binding['sha256'], review_seal['sha256'])
        for name in ('materials', 'live'):
            approval[name].update(approved=True, reviewer='Milad Morad', date='UNIT TEST ONLY',
                                  response='Synthetic fixture; not an actual human approval.')
        approval['live']['config_sha256'] = digest(config.model_dump())
        first_approval = self.root / 'fixture-approval.json'
        copied_approval = self.root / 'renamed-fixture-approval.json'
        write_json(first_approval, approval)
        write_json(copied_approval, approval)
        reserved = self.pilot / '.authorizations' / f'{digest(approval)}.json'

        def fake_transport(*args, **kwargs):
            self.assertTrue(reserved.is_file(), 'reservation must precede the first model call')
            return {'response': Preparation().model_dump(),
                    'metadata': {'status': 'completed', 'audit_issues': [],
                                 'usage': {'input_tokens': 1, 'output_tokens': 1}}}

        self.transport.side_effect = fake_transport
        first, initial = self.execute('first', config, allow_live=True,
                                      review_dir=review, approval_path=first_approval)
        self.assert_full_incomplete(first, initial, 1)
        frozen_reservation = reserved.read_bytes()
        second, repeated = self.execute('second', config, allow_live=True,
                                       review_dir=review, approval_path=copied_approval)
        self.assert_full_incomplete(second, repeated, 0)
        self.assertEqual(repeated['terminal_error']['stage'], 'authorization_reservation')
        self.assertIn('already reserved', repeated['terminal_error']['message'])
        self.assertEqual(reserved.read_bytes(), frozen_reservation)
        self.assertEqual(self.transport.call_count, 1)

    def test_old_review_bundle_cannot_enter_revised_live_execution(self):
        config = RunConfig(backend='codex', model='gpt-6-sol', history_seed=5501, future_seed=5502)
        review = self.root / 'historical-review-fixture'
        review.mkdir()
        binding = source_binding(self.root, self.pilot, self.protocol)
        write_json(review / 'index.json', {'history_ids': ['historical-test-id'],
                                         'source_sha256': binding['sha256'],
                                         'material_revision': 'historical-v04'})
        seal(review, review / 'manifest.json')
        frozen = (review / 'manifest.json').read_bytes()
        with self.assertRaisesRegex(ValueError, 'newly reviewed materials'):
            self.execute('not-authorised', config, allow_live=True, review_dir=review,
                         approval_path=self.root / 'no-approval-created.json')
        self.assertFalse((self.root / 'not-authorised').exists())
        self.assertEqual((review / 'manifest.json').read_bytes(), frozen)
        verify_seal(review, review / 'manifest.json')
        self.transport.assert_not_called()

    def test_revised_review_selection_proof_and_promotions_are_pending_and_sealed(self):
        directory = self.root / 'review-amendment-03'
        result = export_review(directory, repo=self.root, pilot=self.pilot, protocol=self.protocol)
        self.assertEqual(result['material_revision'], MATERIAL_REVISION)
        index = self.read(directory, 'index.json')
        expected = [('S0', 'sales', 'observed_change', 3),
                    ('S1', 'sales', 'unidentifiable', 4),
                    ('S2', 'reporting', 'transfer_change', 1),
                    ('S3', 'hr', 'unidentifiable', 4),
                    ('S4', 'retrieval', 'resolved_retention_transfer', 1),
                    ('S5', 'retrieval', 'transfer_change', 1)]
        self.assertEqual([(row['setting'], row['family'], row['task_type']) for row in index['selection']],
                         [row[:3] for row in expected])
        self.assertEqual((index['history_seed'], index['future_seed']),
                         (REVIEW_HISTORY_SEED, REVIEW_FUTURE_SEED))
        surface = self.read(directory, 'surface-audit.json')
        self.assertEqual(surface['material_revision'], MATERIAL_REVISION)
        self.assertEqual((surface['development_history_seed'], surface['review_history_seed']),
                         (DEVELOPMENT_HISTORY_SEED, REVIEW_HISTORY_SEED))
        self.assertEqual(len(surface['development_history_ids']), 24)
        self.assertEqual(len(surface['review_history_ids']), 24)
        self.assertEqual(set(surface['selected_history_ids']), set(index['history_ids']))
        self.assertFalse(set(surface['development_history_ids']) & set(surface['review_history_ids']))
        self.assertEqual(index['surface_audit']['json'], 'surface-audit.json')
        self.assertTrue((directory / 'surface-audit.md').is_file())
        self.assertFalse(set(index['history_ids']) & {case.history.history_id for case in self.cases})
        for setting, family, task_type, functions in expected:
            exported = self.read(directory, f'{setting}-{family}.json')
            proof = exported['oracle_proof']
            self.assertEqual(exported['surface_audit']['history_id'], exported['case']['history']['history_id'])
            self.assertEqual(exported['surface_audit']['report'], 'surface-audit.json')
            self.assertEqual(proof['hypothesis_class'], 'h14')
            self.assertEqual(proof['current_compatible_function_count'], functions)
            current = next(table for table in proof['compatible_functions_by_version']
                           if table['version'] == proof['current_version'])
            self.assertEqual(len({tuple(item['values']) for item in current['functions']}), functions)
            self.assertGreaterEqual(proof['admissible_policy_count'], functions)
            self.assertEqual(exported['counterfactual'], exported['case']['material_audit']['counterfactual'])
            audit = exported['counterfactual']
            self.assertTrue(audit['passed'])
            expected_outcome = 'action_flip' if task_type == 'unidentifiable' else 'contradiction'
            self.assertEqual(audit['required_outcome'], expected_outcome)
            records = {row['record_id']: row for row in audit['records']}
            for kind, counts in audit['by_type'].items():
                self.assertGreater(counts['record_count'], 0)
                self.assertEqual(counts['record_count'], sum(row['record_type'] == kind for row in records.values()))
                self.assertGreater(counts[expected_outcome], 0)
                for identifier in counts['qualifying_record_ids']:
                    record = records[identifier]
                    self.assertEqual(record['outcome'], expected_outcome)
                    self.assertIn('selected_field_value', record)
                    self.assertIn('promotion', record)
            for record in records.values():
                if record['outcome'] == 'contradiction':
                    self.assertEqual(record['remaining_policy_count'], 0)
                    self.assertIsNone(record['diagnostic_action'])
                    self.assertIsNone(record['control_action'])
                elif record['outcome'] == 'action_flip':
                    self.assertGreater(record['remaining_policy_count'], 0)
                    self.assertTrue(any(record[f'{probe}_action'] != audit['baseline'][probe]
                                        for probe in ('diagnostic', 'control')))
            self.assertEqual(exported['human_review'], {'status': 'pending', 'reviewer': None, 'response': None})
        approval = json.loads(Path(result['approval_path']).read_text(encoding='utf-8'))
        self.assertEqual(approval['material_revision'], MATERIAL_REVISION)
        for phase in ('materials', 'live'):
            self.assertTrue(all(value is None for value in approval[phase].values()))
        frozen = (directory / 'manifest.json').read_bytes()
        approval_bytes = Path(result['approval_path']).read_bytes()
        with self.assertRaises(FileExistsError):
            export_review(directory, repo=self.root, pilot=self.pilot, protocol=self.protocol)
        self.assertEqual((directory / 'manifest.json').read_bytes(), frozen)
        self.assertEqual(Path(result['approval_path']).read_bytes(), approval_bytes)
        verify_seal(directory, directory / 'manifest.json')
        self.transport.assert_not_called()


class AmendmentBindingTests(unittest.TestCase):
    def test_revision_defaults_and_approved_amendment_and_tests_are_bound(self):
        config = RunConfig()
        self.assertEqual(config.material_revision, 'v04-amendment-03-r2')
        self.assertEqual((config.history_seed, config.future_seed, config.order_seed), (44321, 44322, 44323))
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            pilot = repo / 'pilots/v04'
            protocol = repo / 'docs/pilot-v04-protocol.md'
            relatives = [*storage.LEGACY_DEPENDENCIES, 'pilots/v04/run.py',
                         'pilots/v04/reflectai_v04/fixture.py', 'pilots/v04/prompts/fixture.txt',
                         'docs/pilot-v04-protocol.md', 'docs/pilot-v04-amendment-03.md',
                         'docs/pilot-v04-surface-repair.md', 'docs/pilot-v04-transport-preflight.md',
                         'docs/pilot-v04-fhgenie-transport.md',
                         'docs/pilot-v04-amendment-04.md', 'docs/pilot-v04-fhgenie-contract-test.md', 'docs/pilot-v04-amendment-05.md',
                         'pilots/v04/transport/model-catalog.json',
                         'pilots/v04/transport/runtime-attestation.json',
                         'pilots/v04/transport/fhgenie-request.ps1',
                         'pilots/v04/transport/test_fhgenie_request.ps1',
                         'tests/test_pilot_v04_amendment_fixture.py']
            for relative in relatives:
                path = repo / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('Unit-test source binding fixture.\n', encoding='utf-8')
            initial = source_binding(repo, pilot, protocol)
            self.assertIn('docs/pilot-v04-amendment-03.md', initial['files'])
            self.assertIn('docs/pilot-v04-surface-repair.md', initial['files'])
            self.assertIn('tests/test_pilot_v04_amendment_fixture.py', initial['files'])
            for name in ('model-catalog.json', 'runtime-attestation.json'):
                relative = 'pilots/v04/transport/' + name
                self.assertIn(relative, initial['files'])
                artifact = repo / relative
                original = artifact.read_bytes()
                artifact.write_text('Changed transport binding.\n', encoding='utf-8')
                self.assertNotEqual(source_binding(repo, pilot, protocol)['sha256'], initial['sha256'])
                artifact.write_bytes(original)
            amendment = protocol.with_name('pilot-v04-amendment-03.md')
            amendment.write_text('Changed approved contract fixture.\n', encoding='utf-8')
            self.assertNotEqual(source_binding(repo, pilot, protocol)['sha256'], initial['sha256'])
            amendment.unlink()
            with self.assertRaises(ValueError):
                source_binding(repo, pilot, protocol)


if __name__ == '__main__':
    unittest.main()
