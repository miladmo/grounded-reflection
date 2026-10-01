"""Stage separation and end-to-end checks, entirely offline."""

import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from grounded_reflection.models import Hypothesis, Scope
from grounded_reflection.pilot_v02.context import render_context, retained_preparation
from grounded_reflection.pilot_v02.contracts import Preparation, RequirementPrediction, Rule
from grounded_reflection.pilot_v02.data import generate_histories
from grounded_reflection.pilot_v02.report import report
from grounded_reflection.pilot_v02.runner import (
    calibrate, final, freeze, generation_payload, load_histories, load_tasks,
    prepare, records, validate, verify_freeze,
)
from grounded_reflection.pilot_v02.storage import (
    check_run_directory, check_task_separation, read_json, write_json,
)

SOURCE = Path(__file__).resolve().parents[1]


class PilotRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='reflection-v02-runner-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repo'
        for relative in ('src', 'pilots/v02'):
            shutil.copytree(SOURCE / relative, self.repo / relative,
                            ignore=shutil.ignore_patterns('__pycache__', 'runs'))
        for relative in ('pyproject.toml', 'docs/pilot-v02-protocol.md'):
            destination = self.repo / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SOURCE / relative, destination)
        self.run = self.root / 'experiment'
        self.config = self.root / 'config.json'
        config = read_json(self.repo / 'pilots/v02/config.mock.json')
        config['repetitions'] = 1
        write_json(self.config, config)
        self.transport = patch('grounded_reflection.codex_backend.run_completion',
                               side_effect=AssertionError('Unexpected live model call')).start()
        self.addCleanup(patch.stopall)

    def through_freeze(self):
        prepare(self.repo, self.run, self.config)
        validate(self.repo, self.run)
        freeze(self.repo, self.run)

    def test_full_offline_run_records_all_arms_and_preserves_unknown_metrics(self):
        self.through_freeze()
        self.assertFalse((self.run / 'heldout').exists())
        final(self.repo, self.run)
        report(self.repo, self.run)
        result = read_json(self.run / 'results.json')
        self.assertEqual(result['origin'], 'offline_mock')
        self.assertEqual(result['human_evaluation'], 'not_performed')
        self.assertEqual(len(result['cases']), 48)
        self.assertEqual(len(result['paired']), 36)
        self.assertEqual(len(records(self.run)), 84)
        self.assertTrue(all(r.origin == 'offline_mock' for r in records(self.run)))
        self.assertEqual(result['final_stage']['attempted_calls'], 84)
        for summary in result['summary'].values():
            categories = summary['by_category']
            self.assertEqual(set(categories), {'transfer', 'boundary', 'override', 'ambiguous'})
            self.assertEqual(sum(row['tasks'] for row in categories.values()), summary['attempts'])
        self.assertEqual(len(result['preparation']), 12)
        for row in result['preparation']:
            self.assertIsNone(row['scores']['precision'])
            self.assertEqual(row['scores']['recall'], 0)
        for row in result['resources']:
            self.assertIsNone(row['input_tokens'])
            self.assertIsNone(row['currency_cost'])
        sample = read_json(self.run / 'human-review.json')
        self.assertEqual(sample['status'], 'not_reviewed')
        self.assertEqual(len(sample['samples']), 12)
        self.assertEqual(len(sample['histories']), 3)
        for row in sample['samples']:
            self.assertIsNone(row['human_assessment'])
            self.assertNotIn('arm', row)
            self.assertNotIn('automated_checks', row)
        self.assertIn('OFFLINE MOCK', (self.run / 'REPORT.md').read_text(encoding='utf-8'))
        self.transport.assert_not_called()

    def test_mock_calibration_is_never_empirical_calibration(self):
        calibrate(self.repo, self.run, self.config)
        result = read_json(self.run / 'calibration.json')
        self.assertFalse(result['calibrated'])
        self.assertTrue(result['complete'])
        self.assertEqual(result['origin'], 'offline_mock')
        self.assertEqual(result['budget']['attempted_calls'], 6)
        with self.assertRaisesRegex(ValueError, 'rounds'):
            calibrate(self.repo, self.root / 'bad-round', self.config, round_number=3)

    def test_failed_live_calibration_stops_after_one_attempt_and_counts_missing_outputs(self):
        cfg = read_json(self.config)
        cfg['backend'].update(backend='codex', model='unit-test-model')
        cfg['repetitions'] = 2
        self.config.write_text(json.dumps(cfg), encoding='utf-8')
        with patch('grounded_reflection.codex_backend.run_completion',
                   side_effect=RuntimeError('HTTP 400: invalid response schema')) as transport:
            calibrate(self.repo, self.run, self.config, allow_live=True)
        transport.assert_called_once()
        saved = records(self.run)
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0].status, 'failed')
        self.assertIn('invalid response schema', saved[0].error)
        result = read_json(self.run / 'calibration.json')
        self.assertFalse(result['complete'])
        self.assertFalse(result['calibrated'])
        self.assertEqual(result['budget']['attempted_calls'], 1)
        self.assertEqual(result['budget']['expected_stage_outputs'], 12)
        self.assertIn(saved[0].call_id, result['budget']['stopped'])
        self.assertIn('invalid response schema', result['budget']['stopped'])
        self.assertEqual(result['summary']['no_adaptation']['attempts'], 12)
        self.assertEqual(result['summary']['no_adaptation']['failed_calls'], 12)
        from grounded_reflection.pilot_v02.report import evaluate_stage
        tasks = load_tasks(self.repo / 'pilots/v02/data/calibration.json', 'calibration')
        scored = evaluate_stage(self.repo, self.run, tasks, 'calibration')
        self.assertEqual(sum(row['call_status'] == 'missing' for row in scored), 11)
        self.assertEqual(sum(row['call_status'] == 'failed' for row in scored), 1)

    def test_failed_live_preparation_stops_outer_loop_and_preserves_failed_artifact(self):
        cfg = read_json(self.config)
        cfg['backend'].update(backend='codex', model='unit-test-model')
        self.config.write_text(json.dumps(cfg), encoding='utf-8')
        with patch('grounded_reflection.codex_backend.run_completion',
                   side_effect=RuntimeError('HTTP 400: invalid response schema')) as transport:
            prepare(self.repo, self.run, self.config, allow_live=True)
        transport.assert_called_once()
        saved = records(self.run)
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0].status, 'failed')
        result = read_json(self.run / 'prepare.json')
        self.assertFalse(result['complete'])
        self.assertIn(saved[0].call_id, result['stopped'])
        self.assertIn('invalid response schema', result['stopped'])
        self.assertEqual(result['budget']['attempted_calls'], 1)
        self.assertEqual(result['budget']['failed_calls'], 1)
        artifacts = list((self.run / 'prepared').glob('*.json'))
        self.assertEqual(len(artifacts), 1)
        artifact = read_json(artifacts[0])
        self.assertEqual(artifact['status'], 'failed')
        self.assertIsNone(artifact['raw'])
        self.assertEqual(artifact['retained']['requirements'], [])
        with self.assertRaisesRegex(ValueError, 'Incomplete preparation'):
            validate(self.repo, self.run, allow_live=True)

    def test_live_freeze_requires_calibration_and_binds_its_call_artifacts(self):
        cfg = read_json(self.config)
        cfg['backend'].update(backend='codex', model='unit-test-model')
        self.config.write_text(json.dumps(cfg), encoding='utf-8')
        calibration_run = self.root / 'calibration'

        def fake_transport(prompt, schema, *args):
            payload = json.loads(prompt.split('\nPAYLOAD\n', 1)[1])
            if schema['title'] == 'Preparation':
                response = {'requirements': [], 'notes': 'Test transport only'}
            else:
                task = payload['task']
                response = {'case_id': task['case_id'], 'action': 'deliver', 'fields': [
                    {'name': 'source_id', 'value': task['facts']['source_id']},
                    {'name': 'summary', 'value': task['facts']['subject']}], 'missing_fields': []}
            return {'response': response, 'metadata': {'usage': {'input_tokens': 1, 'output_tokens': 1}}}

        with patch('grounded_reflection.codex_backend.run_completion', side_effect=fake_transport):
            calibrate(self.repo, calibration_run, self.config, allow_live=True)
            prepare(self.repo, self.run, self.config, allow_live=True)
            validate(self.repo, self.run, allow_live=True)
        self.assertEqual(read_json(calibration_run / 'calibration.json')['summary']['no_adaptation']['compliance'], .5)
        with self.assertRaisesRegex(ValueError, 'requires a completed live calibration'):
            freeze(self.repo, self.run)
        freeze(self.repo, self.run, calibration_run)
        verify_freeze(self.repo, self.run)
        request = next((calibration_run / 'calls').glob('*/request.json'))
        request.write_text(request.read_text(encoding='utf-8') + '\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Calibration record changed'):
            verify_freeze(self.repo, self.run)

    def test_live_config_without_opt_in_makes_no_run_or_transport_call(self):
        cfg = read_json(self.config)
        cfg['backend'].update(backend='codex', model='unit-test-model')
        self.config.write_text(json.dumps(cfg), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'allow_live'):
            prepare(self.repo, self.run, self.config)
        self.transport.assert_not_called()
        self.assertFalse(self.run.exists())

    def test_final_requires_freeze_and_does_not_create_cases_early(self):
        prepare(self.repo, self.run, self.config)
        with patch('grounded_reflection.pilot_v02.runner.generate_tasks') as generator:
            with self.assertRaises(FileNotFoundError):
                final(self.repo, self.run)
            generator.assert_not_called()
        self.assertFalse((self.run / 'heldout').exists())
        with self.assertRaisesRegex(ValueError, 'validation'):
            freeze(self.repo, self.run)

    def test_freeze_refuses_existing_test_data(self):
        prepare(self.repo, self.run, self.config)
        validate(self.repo, self.run)
        (self.run / 'heldout').mkdir()
        with self.assertRaisesRegex(ValueError, 'must not exist'):
            freeze(self.repo, self.run)

    def test_frozen_preparation_changes_block_final_generation(self):
        self.through_freeze()
        artifact = next((self.run / 'prepared').glob('*.json'))
        artifact.write_text(artifact.read_text(encoding='utf-8') + '\n', encoding='utf-8')
        with patch('grounded_reflection.pilot_v02.runner.generate_tasks') as generator:
            with self.assertRaisesRegex(ValueError, 'Frozen preparation'):
                final(self.repo, self.run)
            generator.assert_not_called()

    def test_frozen_prompt_changes_block_final_generation(self):
        self.through_freeze()
        prompt = self.repo / 'pilots/v02/prompts/generation.txt'
        prompt.write_text(prompt.read_text(encoding='utf-8') + '\nchanged', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Frozen source'):
            final(self.repo, self.run)
        self.assertFalse((self.run / 'heldout').exists())

    def test_no_rerunning_validation_or_final_and_no_overwriting_runs(self):
        self.through_freeze()
        with self.assertRaises(FileExistsError):
            prepare(self.repo, self.run, self.config)
        with self.assertRaisesRegex(ValueError, 'closed'):
            validate(self.repo, self.run)
        final(self.repo, self.run)
        before = (self.run / 'heldout/tasks.json').read_bytes()
        with self.assertRaisesRegex(ValueError, 'already started'):
            final(self.repo, self.run)
        self.assertEqual(before, (self.run / 'heldout/tasks.json').read_bytes())

    def test_output_or_test_tampering_is_detected_before_reporting(self):
        self.through_freeze()
        final(self.repo, self.run)
        output = next((self.run / 'calls').glob('final_test-*/record.json'))
        before = output.read_text(encoding='utf-8')
        output.write_text(before + '\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Final model outputs'):
            report(self.repo, self.run)
        output.write_text(before, encoding='utf-8')
        truth = self.run / 'heldout/ground_truth.json'
        truth.write_text(truth.read_text(encoding='utf-8') + '\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Final tasks'):
            report(self.repo, self.run)

    def test_budget_stop_is_reported_with_missing_attempts_not_dropped(self):
        cfg = read_json(self.config)
        cfg['backend']['max_calls'] = 40  # 12 prepare + 24 validation + 4 final
        self.config.write_text(json.dumps(cfg), encoding='utf-8')
        self.through_freeze()
        final(self.repo, self.run)
        report(self.repo, self.run)
        result = read_json(self.run / 'results.json')
        self.assertEqual(len(records(self.run)), 40)
        self.assertEqual(len(result['cases']), 48)
        self.assertEqual(sum(s['call_status'] == 'missing' for s in result['cases']), 44)
        self.assertIsNotNone(result['final_stage']['stopped'])
        self.assertEqual(sum(s['failed_calls'] for s in result['summary'].values()), 44)

    def test_history_access_is_arm_specific_and_oracles_are_not_loaded(self):
        prepare(self.repo, self.run, self.config)
        task = load_tasks(self.repo / 'pilots/v02/data/calibration.json', 'calibration')[0]
        histories = load_histories(self.repo)
        actual_reader = read_json
        accessed = []

        def guarded_reader(path):
            accessed.append(str(path))
            self.assertNotIn('ground_truth', str(path))
            self.assertNotIn('heldout', str(path))
            return actual_reader(path)

        with patch('grounded_reflection.pilot_v02.runner.read_json', side_effect=guarded_reader):
            for arm in ('no_adaptation', 'direct_evidence', 'direct_adaptation', 'grounded_reflection'):
                payload = generation_payload(self.repo, self.run, task, arm, 0, histories)
                self.assertEqual('history' in payload, arm == 'direct_evidence')
                self.assertEqual('guidance' in payload, arm in ('direct_adaptation', 'grounded_reflection'))
                self.assertNotIn('split', payload['task'])
                self.assertNotIn('recoverable', json.dumps(payload))
                self.assertNotIn('check_kinds', json.dumps(payload))
        self.assertEqual(len(accessed), 2)
        for record in (self.run / 'calls').glob('*/request.json'):
            request = read_json(record)['prompt']
            self.assertNotIn('scope_probes', request)
            self.assertNotIn('allowed_actions', request)

    def test_relabelled_task_cannot_cross_splits(self):
        task = load_tasks(self.repo / 'pilots/v02/data/calibration.json', 'calibration')[0]
        copied = task.model_copy(update={'case_id': 'new-id', 'split': 'final_test'})
        with self.assertRaisesRegex(ValueError, 'relabelled'):
            check_task_separation([[task], [copied]])

    def test_run_directory_cannot_target_original_pilot_or_source(self):
        for name in ('pilots/hr_v01', 'pilots/hr_v01/new', 'src/new', 'pilots/v02/data/new'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                check_run_directory(self.repo, self.repo / name)


class ContextRenderingTests(unittest.TestCase):
    def test_common_renderer_omits_outside_rules_and_requests_missing_scope(self):
        scoped = Rule(field='format', value='table', scope=Scope(match={'audience': ['specialists']}))
        prep = Preparation(requirements=[RequirementPrediction(rule=scoped, decision='adopt')],
                           notes='This free text must never become instructions')
        self.assertEqual(render_context(prep, {'audience': 'starters'}),
                         {'rules': [], 'unresolved_context_fields': []})
        self.assertEqual(render_context(prep, {}),
                         {'rules': [], 'unresolved_context_fields': ['audience']})
        self.assertEqual(render_context(prep, {'audience': 'specialists'})['rules'],
                         [{'field': 'format', 'operator': 'equals', 'value': 'table'}])

    def test_reflection_filter_checks_quotes_but_does_not_use_oracles(self):
        history = generate_histories()[0]
        episode = history.episodes[0]
        evidence = episode.evidence[0]
        scope = Scope(match={'family': [history.family]})
        hypothesis = Hypothesis(hypothesis_id='h1', claim='Test hypothesis', scope=scope,
                                support=[{'episode_id': episode.episode_id, 'evidence_id': evidence.evidence_id,
                                          'quote': 'A fabricated quote absent from the evidence'}],
                                origin='model_generated')
        item = RequirementPrediction(rule=Rule(field='format', value='table', scope=scope),
                                     decision='adopt', hypothesis=hypothesis)
        raw = Preparation(requirements=[item])
        kept, rejected = retained_preparation(raw, history, grounded=True)
        self.assertFalse(kept.requirements)
        self.assertTrue(rejected)
        self.assertEqual(retained_preparation(raw, history, grounded=False)[0], raw)
        hypothesis.support[0].quote = evidence.text
        self.assertEqual(len(retained_preparation(raw, history, grounded=True)[0].requirements), 1)


if __name__ == '__main__':
    unittest.main()
