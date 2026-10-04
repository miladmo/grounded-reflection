"""Hand-authored shortcut fixtures and group-held-out surface diagnostics."""

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
for location in (ROOT / 'src', ROOT / 'pilots/v03', ROOT / 'pilots/v04'):
    sys.path.insert(0, str(location))

from reflectai_v03.contracts import History, Record
from reflectai_v04.data_contracts import FieldOption, PublicFrame
from reflectai_v04.surface_audit import FEATURES, _predict, _project, audit_surfaces, surface_audit_markdown


def history_fixture(history_id, specifications):
    """Labels affect only authored public authority/scope, never predictor input."""
    temporal = any(spec.get('old') for spec in specifications)
    frame = PublicFrame(task_family='fixture', workflow='fixture-workflow', as_of='2026-06-30T23:59:59Z',
                        dimensions={'x': ['zero', 'one'], 'y': ['zero', 'one']},
                        field_option=FieldOption(field='target', operation='set_literal', value='alternative'),
                        baseline_template={'target': 'baseline', 'other': 'fixed'}, fact_descriptions={})
    records = []
    for version in (['old', 'current'] if temporal else ['current']):
        start = '2026-06-01T00:00:00Z' if temporal and version == 'current' else '2026-01-01T00:00:00Z'
        event = {'event': 'register_version', 'version': version, 'task_family': frame.task_family,
                 'workflow': frame.workflow, 'valid_from': start,
                 'valid_until': '2026-06-01T00:00:00Z' if version == 'old' else '2027-01-01T00:00:00Z',
                 'authorised_reviewers': ['Ava']}
        records.append(Record(record_id=f'{history_id}-registry-{version}', timestamp=start,
                              kind='template', actor='registry', context={}, observation=json.dumps(event)))
    for index, spec in enumerate(specifications):
        version = 'old' if spec.get('old') else 'current'
        binding = spec['binding']
        unreviewed = spec.get('negative_kind') == 'unreviewed_target'
        event = {'event': 'review', 'decision': 'accept', 'format': 'interpreted',
                 'authority_ref': f'{history_id}-registry-{version}',
                 'reviewed_fields': ['other'] if unreviewed else ['target'],
                 'accepted_fields': {'target': 'baseline', 'other': 'fixed'}, 'facts': {},
                 'comment': spec.get('comment', 'Approved.')}
        actor = 'Ava' if binding or unreviewed or spec.get('old') else 'Milo'
        stamp = f"2026-{'05' if version == 'old' else '06'}-{spec.get('day', 12):02d}T{spec.get('hour', 10):02d}:{spec.get('minute', 0):02d}:{spec.get('second', 30):02d}Z"
        records.append(Record(record_id=f'{history_id}-record-{index}', timestamp=stamp,
                              kind='review', actor=actor,
                              context={'task_family': frame.task_family, 'workflow': frame.workflow,
                                       'version': version, 'x': 'zero', 'y': 'zero'}, observation=json.dumps(event)))
    return History(history_id=history_id, initial_configuration=frame.model_dump_json(),
                   assumptions='Synthetic fixture: only authorised, field-scoped current approvals bind.',
                   field_dictionary={'target': 'Target field.', 'other': 'Unaffected field.'}, records=records)


def matched_history(history_id):
    specs = []
    for hour, comment in zip((10, 11, 12), ('Approved.', 'Checked.', 'Recorded.')):
        specs.extend({'binding': positive, 'comment': comment, 'hour': hour, 'second': second}
                     for positive, second in ((False, 10), (True, 30), (False, 50)))
    return history_fixture(history_id, specs)


class SurfaceAuditTests(unittest.TestCase):
    def test_old_fixed_date_comment_shortcut_is_detected_on_heldout_groups(self):
        specs = ([{'binding': True, 'comment': 'Approved.', 'day': 10, 'hour': 10}] * 3
                 + [{'binding': False, 'comment': 'Updated export.', 'day': 14, 'hour': 9}] * 8)
        audit = audit_surfaces([history_fixture('development', specs)],
                               [history_fixture('review', specs)], ['review'])
        hard = audit['populations']['current_accepted_reviews']
        self.assertEqual(hard['family_winners']['comment_equality']['review']['balanced_accuracy'], 1)
        self.assertEqual(hard['family_winners']['date_threshold']['review']['balanced_accuracy'], 1)
        self.assertTrue(audit['readiness']['requires_investigation'])
        self.assertTrue(audit['readiness']['perfect_heldout_selectors'])
        self.assertTrue(audit['readiness']['construction_failures'])

    def test_minute_and_clock_thresholds_detect_a_shortcut_hidden_from_hour(self):
        specs = ([{'binding': True, 'comment': 'Neutral.', 'minute': 4}] * 3
                 + [{'binding': False, 'comment': 'Neutral.', 'minute': 55}] * 8)
        audit = audit_surfaces([history_fixture('development', specs)],
                               [history_fixture('review', specs)], ['review'])
        families = audit['populations']['current_accepted_reviews']['family_winners']
        self.assertEqual(families['hour_threshold']['review']['balanced_accuracy'], .5)
        self.assertEqual(families['minute_threshold']['review']['balanced_accuracy'], 1)
        self.assertEqual(families['clock_quarter_hour_threshold']['review']['balanced_accuracy'], 1)

    def test_predictor_selection_is_development_only_when_review_reverses_the_relation(self):
        training = [{'binding': True, 'comment': 'Approved.'}, {'binding': False, 'comment': 'Other.'}]
        reversed_review = [{'binding': True, 'comment': 'Other.'}, {'binding': False, 'comment': 'Approved.'}]
        dev = history_fixture('development', training)
        matching = audit_surfaces([dev], [history_fixture('review', training)], ['review'])
        reversed_result = audit_surfaces([dev], [history_fixture('review', reversed_review)], ['review'])
        for population in matching['populations']:
            original = matching['populations'][population]
            reversed_analysis = reversed_result['populations'][population]
            for family, fit in original['family_winners'].items():
                self.assertEqual(fit['selector'], reversed_analysis['family_winners'][family]['selector'])
            self.assertEqual(original['overall_winner']['selector'], reversed_analysis['overall_winner']['selector'])
        comment = reversed_result['populations']['current_accepted_reviews']['family_winners']['comment_equality']
        self.assertEqual(comment['development']['balanced_accuracy'], 1)
        self.assertEqual(comment['review']['balanced_accuracy'], 0)
        self.assertFalse(reversed_result['selection']['review_selection_performed'])

    def test_imbalance_does_not_replace_balanced_accuracy_with_majority_accuracy(self):
        specs = [{'binding': True, 'comment': 'Neutral.'}] + [{'binding': False, 'comment': 'Neutral.'}] * 9
        audit = audit_surfaces([history_fixture('development', specs)],
                               [history_fixture('review', specs)], ['review'])
        negative, positive = audit['populations']['current_accepted_reviews']['constant_baselines']
        metrics = negative['review']
        self.assertEqual((metrics['tp'], metrics['fp'], metrics['tn'], metrics['fn']), (0, 0, 9, 1))
        self.assertEqual(metrics['balanced_accuracy'], .5)
        self.assertEqual(metrics['history_macro_balanced_accuracy'], .5)
        self.assertIsNone(metrics['precision'])
        self.assertEqual(metrics['recall'], 0)
        self.assertEqual(positive['review']['precision'], .1)

    def test_single_class_groups_and_empty_selection_have_explicit_undefined_denominators(self):
        specs = [{'binding': True}] * 3
        audit = audit_surfaces([history_fixture('development', specs)],
                               [history_fixture('review', specs)], [])
        hard = audit['populations']['current_accepted_reviews']
        self.assertIsNone(hard['overall_winner']['selector'])
        reference = hard['source_oracle_reference']['review']
        self.assertIsNone(reference['balanced_accuracy'])
        self.assertIsNone(reference['history_macro_balanced_accuracy'])
        self.assertEqual(reference['undefined_balanced_accuracy_groups'], 1)
        self.assertEqual(reference['negative_records'], 0)
        self.assertEqual(hard['source_oracle_reference']['selected_review']['records'], 0)
        self.assertFalse(audit['readiness']['hardnegative_evidence_available'])

    def test_legitimate_old_version_date_signal_is_only_a_broad_population_diagnostic(self):
        specs = [{'binding': True}] * 3 + [{'binding': False, 'old': True}] * 3
        audit = audit_surfaces([history_fixture('development', specs)],
                               [history_fixture('review', specs)], ['review'])
        broad = audit['populations']['all_non_registration']
        hard = audit['populations']['current_accepted_reviews']
        self.assertEqual(broad['family_winners']['date_threshold']['review']['balanced_accuracy'], 1)
        self.assertEqual(hard['source_oracle_reference']['review']['negative_records'], 0)
        self.assertFalse(audit['readiness']['construction_failures'])
        self.assertFalse(audit['readiness']['perfect_heldout_selectors'])

    def test_exact_signature_memorisation_is_not_a_hard_failure(self):
        audit = audit_surfaces([matched_history('development')], [matched_history('review')], ['review'])
        hard = audit['populations']['current_accepted_reviews']
        self.assertTrue(hard['overlap']['review']['joint_signature']['exact_observed_separation'])
        self.assertGreater(hard['overlap']['review']['comment']['cross_class_shared_values'], 0)
        self.assertTrue(audit['construction_checks']['review']['passed'])
        self.assertFalse(audit['readiness']['requires_investigation'])

    def test_predictors_cannot_read_private_case_metadata_or_public_semantic_fields(self):
        class CaseEnvelope:
            split = 'development'

            def __init__(self, history):
                self.history = history

            @property
            def truth(self):
                raise AssertionError('Private truth must not be read.')

            @property
            def material_audit(self):
                raise AssertionError('Private material labels must not be read.')

        history = matched_history('development')
        populations, _ = _project([history])
        features = populations['current_accepted_reviews'][0]['surface']
        self.assertEqual(set(features), set(FEATURES))
        with self.assertRaises(ValueError):
            _predict({'operation': 'eq', 'feature': 'actor', 'value': 'Ava', 'polarity': True}, features)
        with self.assertRaises(ValueError):
            _predict({'operation': 'constant', 'value': False}, {**features, 'label': True})
        report = audit_surfaces([CaseEnvelope(history)], [CaseEnvelope(matched_history('review'))], ['review'])
        self.assertEqual(report['development_history_ids'], ['development'])
        self.assertIn('not independent validation', surface_audit_markdown(report))
        json.dumps(report, allow_nan=False)

    def test_history_overlap_unknown_selected_ids_and_final_test_cases_are_rejected(self):
        history = matched_history('same')
        with self.assertRaises(ValueError):
            audit_surfaces([history], [history], ['same'])
        with self.assertRaises(ValueError):
            audit_surfaces([history], [matched_history('other')], ['unknown'])
        envelope = type('FinalCase', (), {'split': 'final_test', 'history': history})()
        with self.assertRaises(ValueError):
            audit_surfaces([envelope], [matched_history('review')], ['review'])


if __name__ == '__main__':
    unittest.main()
