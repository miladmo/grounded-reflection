import json
from pathlib import Path
import tempfile
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'pilots' / 'v03'))

from reflectai_v03 import runner
from reflectai_v03.contracts import BackendConfig, RunConfig
from reflectai_v03.data import build_histories, build_tasks
from reflectai_v03.storage import (check_separation, read_json, review_template,
                                  seal_files, source_manifest, validate_review, verify_seal, write_json)

REPO = Path(__file__).resolve().parents[1]


class FailedBackend:
    def __init__(self):
        self.calls = 0

    def complete(self, *args, **kwargs):
        self.calls += 1
        return {'status': 'failed', 'response': None, 'error': 'Injected offline failure'}

    def budget_summary(self):
        return {'attempted_calls': self.calls, 'failed_calls': self.calls,
                'reported_tokens': 0, 'total_tokens': None}


class RunnerTests(unittest.TestCase):
    def test_offline_pipeline_freezes_before_future_tasks_and_preserves_budgets(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'run'
            original = runner.build_tasks

            def guarded_build(dataset, task_seed):
                frozen = read_json(output / 'F1.json')
                self.assertFalse(frozen['future_tasks_generated'])
                self.assertEqual(frozen['prepared_artifacts'], 16)
                verify_seal(output, frozen['files'])
                self.assertFalse((output / 'public/tasks.json').exists())
                return original(dataset, task_seed)

            with patch.object(runner, 'build_tasks', side_effect=guarded_build):
                result = runner.run_experiment(REPO, output, RunConfig(repetitions=1))
            self.assertEqual(result['status'], 'completed', result['error'])
            self.assertEqual(result['budget']['attempted_calls'], 96)
            for arm in ('C', 'D'):
                self.assertEqual(result['budget_by_arm_phase'][arm]['prepare']['attempted_calls'], 16)
                self.assertEqual(result['budget_by_arm_phase'][arm]['generation']['attempted_calls'], 16)
            self.assertEqual(result['planned_generation_attempts'], 64)
            self.assertFalse(result['calibration']['passed'])
            self.assertEqual(result['outcomes']['primary']['D_minus_C'], 0)
            for arm in ('B', 'C', 'D'):
                scores = result['outcomes']['by_arm'][arm]['diagnostic']
                self.assertEqual(scores['update_correct'], 4)
                self.assertEqual(scores['world_compliant'], 3)
            for request_file in (output / 'calls').glob('*/request.json'):
                request = read_json(request_file)
                prompt = request['prompt']
                for secret in ('candidate_targets', 'world_policy', 'admissible_policies', 'private-probe-'):
                    self.assertNotIn(secret, prompt)
            self.assertTrue((output / 'human_review/sample.json').is_file())
            self.assertTrue((output / 'evaluator/blind_key.json').is_file())
            candidates = read_json(output / 'candidate_scores.json')
            drafts = [row for row in candidates if row['arm'] == 'D' and row['step'] == 1]
            self.assertEqual(len(drafts), 8)
            self.assertTrue(all(row['scores']['target_status_metrics'] is None for row in drafts))
            self.assertIn('OFFLINE MOCK', (output / 'REPORT.md').read_text(encoding='utf-8'))

    def test_incomplete_preparation_blocks_future_tasks_and_keeps_all_denominators(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'run'
            with patch.object(runner, 'build_tasks') as future_tasks:
                result = runner.run_experiment(REPO, output, RunConfig(repetitions=1), backend=FailedBackend())
                future_tasks.assert_not_called()
            self.assertEqual(result['status'], 'incomplete')
            self.assertEqual(len(result['rows']), 64)
            self.assertTrue(all(not row['update_correct'] and not row['world_compliant'] for row in result['rows']))
            self.assertFalse((output / 'F1.json').exists())
            scores = read_json(output / 'candidate_scores.json')
            self.assertEqual(len(scores), 32)
            self.assertTrue(all(not row['scores']['preparation_present'] for row in scores))

    def test_live_is_blocked_before_backend_construction(self):
        config = RunConfig(phase='calibration', repetitions=1,
                           backend=BackendConfig(backend='codex', model='gpt-6-sol', max_calls=64))
        with tempfile.TemporaryDirectory() as directory, patch.object(runner, 'Backend') as backend:
            with self.assertRaisesRegex(ValueError, 'allow-live'):
                runner.run_experiment(REPO, Path(directory) / 'run', config)
            backend.assert_not_called()
            with self.assertRaisesRegex(ValueError, 'human rubric review'):
                runner.run_experiment(REPO, Path(directory) / 'run', config, allow_live=True)
            backend.assert_not_called()

    def test_existing_run_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileExistsError):
                runner.run_experiment(REPO, Path(directory), RunConfig(repetitions=1))

    def test_mock_cannot_be_a_scientific_run(self):
        for phase, repetitions in [('main', 3), ('calibration', 1)]:
            with self.assertRaises(ValueError):
                RunConfig(phase=phase, repetitions=repetitions)

    def test_pending_review_and_source_drift_cannot_approve_live_run(self):
        review = review_template(REPO)
        with self.assertRaisesRegex(ValueError, 'human rubric review'):
            validate_review(REPO, review)
        review.update(status='approved', reviewer='Unit test fixture, not a real reviewer', date='2026-09-29')
        for pair in review['pairs']:
            pair['approved'] = True
        validate_review(REPO, review)
        review['source_manifest']['pyproject.toml'] = 'wrong'
        with self.assertRaisesRegex(ValueError, 'source changed'):
            validate_review(REPO, review)

    def test_pair_duplicates_allowed_but_cross_split_reuse_rejected(self):
        data = build_tasks(build_histories(33, split='test_fixture'), task_seed=34)
        identities = check_separation(data, [])
        self.assertEqual(len(identities), 16)
        with self.assertRaisesRegex(ValueError, 'leakage'):
            check_separation(data, identities)

    def test_write_once_and_tampered_seal(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'artifact.json'
            write_json(path, {'value': 1})
            with self.assertRaises(FileExistsError):
                write_json(path, {'value': 2})
            with self.assertRaisesRegex(ValueError, 'frozen'):
                verify_seal(Path(directory), {'artifact.json': 'wrong'})

    def freeze_fixture(self, directory):
        repo = Path(directory) / 'repo'
        for name in ('docs/pilot-v03-protocol.md', 'docs/pilot-v03-design-review.md', 'pilots/v03/SCENARIOS.md',
                     'pyproject.toml', 'pilots/v03/run_pilot.py'):
            path = repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Unit test fixture', encoding='utf-8')
        review = review_template(repo)
        review.update(status='approved', reviewer='Unit test fixture, not a human review', date='2026-09-29')
        for pair in review['pairs']:
            pair['approved'] = True
        config = RunConfig(phase='main', repetitions=3, seed=900,
                           backend=BackendConfig(backend='codex', model='gpt-6-sol', max_calls=288))
        calibration = repo / 'pilots/v03/runs/calibration-fixture'
        calibration_config = RunConfig(phase='calibration', repetitions=1, seed=100,
            backend=BackendConfig(backend='codex', model='gpt-6-sol', max_calls=64))
        report = {'config': calibration_config.model_dump(mode='json'), 'status': 'completed',
                  'source_manifest': source_manifest(repo), 'rows': [], 'task_identities': ['development-fixture']}
        write_json(calibration / 'results.json', report)
        write_json(calibration / 'artifact_manifest.json', seal_files(calibration, ['results.json']))
        write_json(repo / 'pilots/v03/runs/calibration_registry/round-1.json', {'run_dir': str(calibration)})
        return repo, review, config, calibration

    def test_F0_requires_gates_and_registers_one_immutable_freeze(self):
        with tempfile.TemporaryDirectory() as directory:
            repo, review, config, calibration = self.freeze_fixture(directory)
            with patch.object(runner, 'calibration_gates', return_value={'passed': False}):
                with self.assertRaisesRegex(ValueError, 'calibration failed'):
                    runner.freeze_main(repo, repo / 'F0.json', config, review, [calibration])
            with patch.object(runner, 'calibration_gates', return_value={'passed': True}):
                frozen = runner.freeze_main(repo, repo / 'F0.json', config, review, [calibration])
                self.assertEqual(frozen['development_identities'], ['development-fixture'])
                runner._check_live(repo, config, True, None, frozen)
                with self.assertRaises(FileExistsError):
                    runner.freeze_main(repo, repo / 'another-F0.json', config, review, [calibration])

    def test_F0_rejects_duplicate_calibration_rounds_before_using_scores(self):
        with tempfile.TemporaryDirectory() as directory:
            repo, review, config, calibration = self.freeze_fixture(directory)
            with self.assertRaisesRegex(ValueError, 'every registered calibration'):
                runner.freeze_main(repo, repo / 'F0.json', config, review, [calibration, calibration])

    def test_F0_rejects_changed_primary_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            repo, review, config, calibration = self.freeze_fixture(directory)
            report_path = calibration / 'results.json'
            report_path.write_text(report_path.read_text(encoding='utf-8') + ' ', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'frozen'):
                runner.freeze_main(repo, repo / 'F0.json', config, review, [calibration])


if __name__ == '__main__':
    unittest.main()
