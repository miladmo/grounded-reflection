"""Strict output transport checks. All inference calls are patched offline."""

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from grounded_reflection.models import Contract
from grounded_reflection.pilot_v02.backend import Backend
from grounded_reflection.pilot_v02.contracts import BackendConfig, Preparation, WorkOutput
from grounded_reflection.pilot_v02.wire import decode_response, strict_response_schema


def nodes(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from nodes(child)


def preparation():
    return {'requirements': [{
        'rule': {'field': 'format', 'operator': 'equals', 'value': 'table',
                 'scope': {'match': [
                     {'attribute': 'audience', 'values': ['specialists', 'partners']},
                     {'attribute': 'channel', 'values': ['email']},
                 ]}},
        'decision': 'adopt', 'missing_fields': [],
        'hypothesis': {
            'hypothesis_id': 'h1', 'claim': 'Use a table in this context',
            'scope': {'match': [{'attribute': 'channel', 'values': ['email']}]},
            'support': [{'episode_id': 'e1', 'evidence_id': 'v1', 'quote': 'A table is clearer.'}],
            'counterevidence': [], 'alternatives': [], 'unresolved_questions': [],
            'origin': 'model_generated',
        },
    }], 'notes': 'Synthetic test response'}


class WireSchemaTests(unittest.TestCase):
    def test_generation_schema_requires_defaults_without_changing_contract(self):
        before = WorkOutput.model_json_schema()
        schema = strict_response_schema(WorkOutput)
        self.assertEqual(schema['required'], ['case_id', 'action', 'missing_fields', 'fields'])
        self.assertEqual(schema['$defs']['OutputField']['required'], ['name', 'value'])
        self.assertEqual(WorkOutput.model_json_schema(), before)
        self.assertEqual(schema['properties'], before['properties'])

    def test_all_nested_objects_are_closed_required_and_default_free(self):
        for contract in (Preparation, WorkOutput):
            schema = strict_response_schema(contract)
            for node in nodes(schema):
                self.assertNotIn('default', node)
                if node.get('type') == 'object':
                    self.assertFalse(node['additionalProperties'])
                    self.assertEqual(set(node['required']), set(node['properties']))
        schema = strict_response_schema(Preparation)
        match = schema['$defs']['Scope']['properties']['match']
        self.assertEqual(match['type'], 'array')
        self.assertEqual(match['items']['required'], ['attribute', 'values'])
        scope_union = schema['$defs']['Rule']['properties']['scope']['anyOf']
        self.assertIn({'type': 'null'}, scope_union)
        self.assertIn('scope', schema['$defs']['Rule']['required'])
        self.assertIn('hypothesis', schema['$defs']['RequirementPrediction']['required'])

    def test_unrelated_dictionary_contract_is_rejected_not_silently_closed(self):
        class Other(Contract):
            entries: dict[str, str]

        with self.assertRaisesRegex(ValueError, 'Open object mappings'):
            strict_response_schema(Other)

    def test_scope_conversion_is_lossless_and_preserves_raw_response(self):
        raw = preparation()
        before = deepcopy(raw)
        decoded = decode_response(Preparation, raw)
        result = Preparation.model_validate(decoded)
        self.assertEqual(result.requirements[0].rule.scope.match, {
            'audience': ['specialists', 'partners'], 'channel': ['email']})
        self.assertEqual(result.requirements[0].hypothesis.scope.match, {'channel': ['email']})
        self.assertEqual(raw, before)
        self.assertEqual(result.requirements[0].hypothesis.support[0].quote, 'A table is clearer.')
        self.assertEqual(result.requirements[0].decision, 'adopt')

    def test_duplicate_attributes_rejected_for_rule_and_hypothesis_scopes(self):
        for field in ('rule', 'hypothesis'):
            with self.subTest(field=field):
                raw = preparation()
                scope = raw['requirements'][0][field]['scope']['match']
                scope.append(deepcopy(scope[0]))
                with self.assertRaisesRegex(ValueError, 'Duplicate scope attribute'):
                    decode_response(Preparation, raw)

    def test_malformed_scope_entries_do_not_discard_information(self):
        for entry in ({'attribute': 'a', 'values': ['b'], 'unexpected': 'extra'},
                      {'attribute': 'a'}, {'attribute': 1, 'values': ['b']}):
            raw = preparation()
            raw['requirements'][0]['rule']['scope']['match'] = [entry]
            with self.subTest(entry=entry), self.assertRaises(ValueError):
                decode_response(Preparation, raw)
        raw = preparation()
        raw['requirements'][0]['rule']['scope']['match'] = {'a': ['b']}
        with self.assertRaisesRegex(ValueError, 'must be an array'):
            decode_response(Preparation, raw)

    def test_nullable_scopes_and_empty_preparation_keep_existing_meaning(self):
        raw = preparation()
        raw['requirements'][0]['rule']['scope'] = None
        raw['requirements'][0]['hypothesis'] = None
        result = Preparation.model_validate(decode_response(Preparation, raw))
        self.assertIsNone(result.requirements[0].rule.scope)
        self.assertIsNone(result.requirements[0].hypothesis)
        empty = {'requirements': [], 'notes': 'test'}
        self.assertEqual(decode_response(Preparation, empty), empty)
        output = {'case_id': 'c1', 'action': 'deliver', 'fields': [], 'missing_fields': []}
        self.assertEqual(decode_response(WorkOutput, output), output)

    def test_decoding_keeps_canonical_scope_validation(self):
        for values in ([], ['a', 'a'], ['   ']):
            raw = preparation()
            raw['requirements'][0]['rule']['scope']['match'][0]['values'] = values
            with self.subTest(values=values), self.assertRaises(ValueError):
                Preparation.model_validate(decode_response(Preparation, raw))


class WireBackendTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='reflection-v02-wire-')
        self.addCleanup(self.temp.cleanup)
        self.run = Path(self.temp.name) / 'call'
        self.backend = Backend(BackendConfig(backend='codex', model='test-model'), allow_live=True)

    def invoke(self):
        return self.backend.complete('Synthetic preparation', Preparation, self.run,
                                     call_id='wire-call', arm='grounded_reflection',
                                     phase='prepare', family='sales', repetition=0)

    def test_backend_sends_and_logs_wire_schema_preserving_raw_and_canonical_outputs(self):
        raw = preparation()
        with patch('grounded_reflection.codex_backend.run_completion', return_value={
            'response': raw, 'metadata': {'usage': {'input_tokens': 4, 'output_tokens': 7}},
        }) as transport:
            record = self.invoke()
        self.assertEqual(record.status, 'completed')
        sent_schema = transport.call_args.args[1]
        self.assertEqual(sent_schema, strict_response_schema(Preparation))
        self.assertEqual(json.loads((self.run / 'response.schema.json').read_text()), sent_schema)
        self.assertEqual(json.loads((self.run / 'response.json').read_text()), raw)
        self.assertIsInstance(record.response['requirements'][0]['rule']['scope']['match'], dict)
        self.assertIsInstance(raw['requirements'][0]['rule']['scope']['match'], list)
        self.assertEqual(record.usage.input_tokens, 4)
        request = json.loads((self.run / 'request.json').read_text())
        self.assertEqual(request['schema_format'], 'strict_scope_entries_v1')

    def test_duplicate_scope_failure_retains_raw_output_usage_and_attempt(self):
        raw = preparation()
        scope = raw['requirements'][0]['rule']['scope']['match']
        scope.append(deepcopy(scope[0]))
        with patch('grounded_reflection.codex_backend.run_completion', return_value={
            'response': raw, 'metadata': {'usage': {'input_tokens': 4, 'output_tokens': 7}},
        }) as transport:
            record = self.invoke()
        self.assertEqual(transport.call_count, 1)
        self.assertEqual(record.status, 'failed')
        self.assertIn('Duplicate scope attribute', record.error)
        self.assertEqual(self.backend.budget_summary()['reported_tokens'], 11)
        self.assertEqual(self.backend.budget_summary()['failed_calls'], 1)
        self.assertEqual(json.loads((self.run / 'response.json').read_text()), raw)


if __name__ == '__main__':
    unittest.main()
