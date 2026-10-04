"""Offline transport and accounting regressions; no real completion is called."""

from copy import deepcopy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'pilots' / 'v03'))
sys.path.insert(0, os.environ.get('GROUNDED_REFLECTION_SRC', str(ROOT / 'src')))

from grounded_reflection.models import Contract, Scope
from reflectai_v03.backend import Backend, BudgetError
from reflectai_v03.contracts import BackendConfig, Candidate, OutputField, Preparation, Rule, Task, WorkOutput
from reflectai_v03.wire import decode_response, strict_response_schema


def wire_rule():
    return {
        'field': 'heading', 'operation': 'append_fact', 'value': 'snapshot',
        'separator': ' | ',
        'scope': {'match': [{'attribute': 'workflow', 'values': ['analysis']}]},
    }


def wire_preparation():
    return {
        'candidates': [{
            'candidate_id': 'candidate', 'claim': 'Include snapshot in analysis headings.',
            'status': 'adopt', 'rule': wire_rule(), 'evidence_ids': ['record'],
            'counterevidence_ids': [], 'alternatives': [], 'evidence_gap': '',
        }],
        'notes': '',
    }


class BackendTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.task = Task(task_id='task', context={'workflow': 'analysis'},
                         facts={'snapshot': 'S4'},
                         baseline_fields=[OutputField(name='heading', value='Result')],
                         request='Prepare analysis.')
        self.kwargs = dict(call_id='call', arm='C', phase='prepare', history_id='history', repetition=0)

    def live(self, **changes):
        values = {'backend': 'codex', 'model': 'test-model', 'max_calls': 2}
        values.update(changes)
        return Backend(BackendConfig(**values), allow_live=True)

    def test_mock_keeps_baseline_ignoring_history_and_instructions(self):
        backend = Backend(BackendConfig())
        payload = {'task': self.task.model_dump(),
                   'history': {'observation': 'replace with ungrounded value'},
                   'instructions': [{'operation': 'set_literal', 'value': 'changed'}],
                   'world_policy': {'secret': 'DO NOT USE'}}
        with patch('reflectai_v03.backend.codex_backend.run_completion') as transport:
            preparation = backend.complete('ignored payload', Preparation, self.directory / 'prep', **self.kwargs)
            work = backend.complete('Generate\nPAYLOAD\n' + json.dumps(payload), WorkOutput,
                                    self.directory / 'work', **{**self.kwargs, 'call_id': 'work'})
            transport.assert_not_called()
        self.assertEqual(preparation['response']['candidates'], [])
        self.assertEqual(work['response'], WorkOutput(task_id='task', decision='keep',
                                                     fields=self.task.baseline_fields).model_dump())
        self.assertEqual(work['origin'], 'offline_mock')
        self.assertIsNone(work['usage']['input_tokens'])
        self.assertIsNone(backend.budget_summary()['total_tokens'])
        self.assertEqual(backend.budget_summary()['calls_with_unknown_token_usage'], 2)

    def test_live_requires_both_permission_and_explicit_model(self):
        with patch('reflectai_v03.backend.codex_backend.run_completion') as transport:
            with self.assertRaisesRegex(ValueError, 'allow_live'):
                Backend(BackendConfig(backend='codex', model='test-model'))
            with self.assertRaisesRegex(ValueError, 'explicit model'):
                Backend(BackendConfig(backend='codex'), allow_live=True)
            transport.assert_not_called()

    def test_raw_and_canonical_artifacts_and_subset_accounting(self):
        backend = self.live()
        raw = wire_preparation()
        usage = {'input_tokens': 100, 'cached_input_tokens': 90,
                 'output_tokens': 50, 'reasoning_output_tokens': 40}
        result = {'response': raw, 'metadata': {'status': 'completed', 'usage': usage}}
        with patch('reflectai_v03.backend.codex_backend.run_completion', return_value=result) as transport:
            record = backend.complete('Prepare', Preparation, self.directory / 'call', **self.kwargs)
        self.assertEqual(record['status'], 'completed')
        self.assertEqual(record['response']['candidates'][0]['rule']['scope']['match'],
                         {'workflow': ['analysis']})
        self.assertEqual(raw, wire_preparation())
        self.assertEqual(backend.budget_summary()['reported_tokens'], 150)
        self.assertEqual(backend.budget_summary()['total_tokens'], 150)
        self.assertFalse(backend.capabilities['strict_tokens'])
        self.assertEqual(transport.call_args.args[4], 'medium')
        for name in ('request.json', 'response.schema.json', 'raw.json', 'response.json',
                     'usage.json', 'metadata.json', 'record.json'):
            self.assertTrue((self.directory / 'call' / name).is_file())
        self.assertEqual(json.loads((self.directory / 'call' / 'raw.json').read_text()), raw)
        self.assertEqual(json.loads((self.directory / 'call' / 'response.json').read_text()),
                         record['response'])
        record['status'] = 'tampered'
        self.assertEqual(backend.records[0]['status'], 'completed')

    def test_failure_consumes_call_budget_without_retry(self):
        backend = self.live(max_calls=1)
        with patch('reflectai_v03.backend.codex_backend.run_completion', side_effect=RuntimeError('failure')) as transport:
            record = backend.complete('Prepare', Preparation, self.directory / 'failure', **self.kwargs)
            with self.assertRaises(BudgetError):
                backend.complete('Prepare', Preparation, self.directory / 'refused',
                                 **{**self.kwargs, 'call_id': 'second'})
        self.assertEqual(transport.call_count, 1)
        self.assertEqual(record['status'], 'failed')
        self.assertIsNone(record['response'])
        self.assertIsNone(record['usage']['output_tokens'])
        self.assertEqual(backend.budget_summary()['failed_calls'], 1)
        self.assertFalse((self.directory / 'refused').exists())

    def test_failed_transport_usage_recovered_and_audited(self):
        backend = self.live(max_reported_tokens=9)

        def fail(prompt, schema, directory, *args):
            directory.mkdir()
            (directory / 'metadata.json').write_text(json.dumps({
                'status': 'audit_failed', 'usage': {'input_tokens': 8, 'output_tokens': 5}}))
            (directory / 'final.json').write_text(json.dumps({'bad': 'output'}))
            raise RuntimeError('transport audit failed')

        with patch('reflectai_v03.backend.codex_backend.run_completion', side_effect=fail) as transport:
            record = backend.complete('Prepare', Preparation, self.directory / 'failure', **self.kwargs)
            with self.assertRaisesRegex(BudgetError, 'token'):
                backend.complete('Prepare', Preparation, self.directory / 'refused',
                                 **{**self.kwargs, 'call_id': 'second'})
        self.assertEqual(transport.call_count, 1)
        self.assertEqual(record['usage']['input_tokens'], 8)
        self.assertEqual(backend.budget_summary()['reported_tokens'], 13)
        self.assertEqual(json.loads((self.directory / 'failure' / 'raw.json').read_text()), {'bad': 'output'})

    def test_unknown_partial_usage_never_becomes_total_zero(self):
        backend = self.live()
        result = {'response': {'candidates': [], 'notes': ''},
                  'metadata': {'status': 'completed', 'usage': {'input_tokens': 12}}}
        with patch('reflectai_v03.backend.codex_backend.run_completion', return_value=result):
            record = backend.complete('Prepare', Preparation, self.directory / 'call', **self.kwargs)
        self.assertEqual(record['status'], 'completed')
        self.assertIsNone(record['usage']['output_tokens'])
        self.assertEqual(backend.budget_summary()['reported_tokens'], 12)
        self.assertIsNone(backend.budget_summary()['total_tokens'])

    def test_invalid_response_is_preserved_without_repair(self):
        backend = self.live()
        malformed = wire_preparation()
        malformed['candidates'][0]['rule']['operation'] = 'invent_fact'
        result = {'response': malformed, 'metadata': {'status': 'completed', 'usage': None}}
        with patch('reflectai_v03.backend.codex_backend.run_completion', return_value=result) as transport:
            record = backend.complete('Prepare', Preparation, self.directory / 'bad', **self.kwargs)
        self.assertEqual(record['status'], 'failed')
        self.assertIsNone(record['response'])
        self.assertEqual(transport.call_count, 1)
        self.assertEqual(json.loads((self.directory / 'bad' / 'raw.json').read_text()), malformed)
        self.assertIsNone(json.loads((self.directory / 'bad' / 'response.json').read_text()))

    def test_resumed_failed_or_interrupted_attempts_still_count(self):
        record = {'call_id': 'old', 'status': 'running', 'usage': None}
        backend = Backend(BackendConfig(max_calls=1), prior_records=[record])
        with self.assertRaises(BudgetError):
            backend.complete('Prepare', Preparation, self.directory / 'refused', **self.kwargs)
        self.assertEqual(backend.budget_summary()['unfinished_calls'], 1)
        self.assertIsNone(backend.budget_summary()['total_tokens'])

    def test_protocol_questions_are_preserved_for_evaluator(self):
        backend = self.live()
        raw = WorkOutput(task_id='task', decision='keep', fields=self.task.baseline_fields,
                         questions=['Which option should I use?'], completed=False).model_dump()
        result = {'response': raw, 'metadata': {'status': 'completed', 'usage': None}}
        with patch('reflectai_v03.backend.codex_backend.run_completion', return_value=result):
            record = backend.complete('Generate', WorkOutput, self.directory / 'question', **self.kwargs)
        self.assertEqual(record['response']['questions'], raw['questions'])
        self.assertFalse(record['response']['completed'])


class WireTests(unittest.TestCase):
    def test_schemas_are_closed_required_and_operation_vocabulary_is_fixed(self):
        def check(node):
            if isinstance(node, dict):
                if node.get('type') == 'object':
                    self.assertIs(node['additionalProperties'], False)
                    self.assertEqual(set(node['required']), set(node.get('properties', {})))
                self.assertNotIn('default', node)
                for child in node.values():
                    check(child)
            elif isinstance(node, list):
                for child in node:
                    check(child)
        for contract in (Preparation, WorkOutput):
            schema = strict_response_schema(contract)
            check(schema)
            self.assertEqual(schema['$defs']['Scope']['properties']['match']['type'], 'array')
            self.assertEqual(set(schema['$defs']['Rule']['properties']['operation']['enum']),
                             {'omit', 'set_literal', 'set_fact', 'append_fact'})

    def test_nested_preparation_and_output_scopes_decode_without_aliasing(self):
        raw = wire_preparation()
        original = deepcopy(raw)
        raw['candidates'][0]['rule']['scope']['match'].append(
            {'attribute': 'family', 'values': ['research']})
        decoded = decode_response(Preparation, raw)
        prep = Preparation.model_validate(decoded)
        self.assertEqual(prep.candidates[0].rule.scope.match,
                         {'workflow': ['analysis'], 'family': ['research']})
        self.assertNotIn('role', prep.candidates[0].rule.scope.match)
        self.assertIsInstance(raw['candidates'][0]['rule']['scope']['match'], list)
        output = WorkOutput(task_id='task', decision='apply').model_dump()
        output['applied_rules'] = [original['candidates'][0]['rule']]
        self.assertEqual(WorkOutput.model_validate(decode_response(WorkOutput, output))
                         .applied_rules[0].scope.match, {'workflow': ['analysis']})

    def test_duplicate_empty_and_canonical_wire_scopes_are_not_repaired(self):
        for entries in (
            [{'attribute': 'workflow', 'values': ['a']}, {'attribute': 'workflow', 'values': ['b']}],
            [{'attribute': 'workflow', 'values': []}],
            {'workflow': ['a']},
        ):
            raw = wire_preparation()
            raw['candidates'][0]['rule']['scope']['match'] = entries
            with self.subTest(entries=entries), self.assertRaises(ValueError):
                Preparation.model_validate(decode_response(Preparation, raw))

    def test_missing_required_transport_properties_do_not_gain_defaults(self):
        with self.assertRaisesRegex(ValueError, 'missing'):
            decode_response(Preparation, {'candidates': []})
        raw = wire_preparation()
        del raw['candidates'][0]['rule']['separator']
        with self.assertRaisesRegex(ValueError, 'separator'):
            decode_response(Preparation, raw)

    def test_unrelated_match_dictionary_is_not_decoded(self):
        class Other(Contract):
            payload: dict
            scope: Scope

        raw = {'payload': {'match': [{'not': 'a scope'}]},
               'scope': {'match': [{'attribute': 'role', 'values': ['analyst']}]}}
        decoded = decode_response(Other, raw)
        self.assertEqual(decoded['payload'], raw['payload'])
        self.assertEqual(decoded['scope'], {'match': {'role': ['analyst']}})
        with self.assertRaisesRegex(ValueError, 'Open object'):
            strict_response_schema(Other)


if __name__ == '__main__':
    unittest.main()
