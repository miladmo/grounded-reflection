"""Deterministic fixture tests, without model calls or empirical claims."""

import unittest

from grounded_reflection.models import Scope
from grounded_reflection.pilot_v02.contracts import (
    FamilyTruth, Preparation, RequirementPrediction, Rule, Task, TaskTruth, WorkOutput,
)
from grounded_reflection.pilot_v02.evaluation import score_preparation, score_task


def rule(field="opening", value="problem", operator="equals", scope=None):
    return Rule(field=field, value=value, operator=operator, scope=scope)


def task():
    return Task(case_id="case-1", family="recruiting", split="validation",
                context={"audience": "specialist"}, request="Prepare a short brief.",
                facts={"source": "S1"}, output_fields=["opening", "citation", "claim"])


def truth(**changes):
    fields = dict(case_id="case-1", family="recruiting", category="transfer",
                  checks=[rule(), rule("citation", "S1", "contains"),
                          rule("claim", "guaranteed", "excludes")],
                  check_kinds=["hidden", "explicit", "generic"], allowed_actions=["deliver"],
                  distractors=[rule("opening", "joke")])
    fields.update(changes)
    return TaskTruth(**fields)


def output(action="deliver", missing_fields=None, **changes):
    fields = {"opening": "problem", "citation": "Source S1", "claim": "Eligible for review"}
    fields.update(changes)
    return WorkOutput(case_id="case-1", action=action, missing_fields=missing_fields or [],
                      fields=[{"name": name, "value": value} for name, value in fields.items()])


def family_truth():
    return FamilyTruth(family="recruiting",
                       recoverable=[rule(scope=Scope(match={"audience": ["specialist"]}))],
                       unidentifiable=[rule("approval", "manager")],
                       distractors=[rule(value="joke")],
                       scope_probes=[{"audience": "specialist"}, {"audience": "apprentice"}, {}])


def preparation(*entries):
    return Preparation(requirements=[RequirementPrediction(rule=r, decision=decision)
                                     for r, decision in entries])


class TaskEvaluationTests(unittest.TestCase):
    def test_success_keeps_rule_kinds_and_denominators(self):
        result = score_task(task(), truth(), output())
        self.assertTrue(result["completed"])
        self.assertTrue(result["task_passed"])
        self.assertEqual(result["compliance"], 1)
        self.assertEqual(result["by_kind"]["hidden"], {"passed": 1, "total": 1, "rate": 1})
        self.assertEqual(result["distractor_adoptions"], 0)

    def test_empty_or_absent_field_never_satisfies_excludes(self):
        for missing in ("empty", "absent"):
            with self.subTest(missing=missing):
                value = output(claim="  ")
                if missing == "absent":
                    value.fields = [field for field in value.fields if field.name != "claim"]
                result = score_task(task(), truth(), value)
                self.assertFalse(result["checks"][2]["passed"])
                self.assertFalse(result["completed"])

    def test_trim_is_allowed_but_case_and_substring_semantics_are_literal(self):
        self.assertTrue(score_task(task(), truth(), output(opening=" problem "))["completed"])
        result = score_task(task(), truth(), output(opening="Problem", citation="Source s1"))
        self.assertFalse(result["checks"][0]["passed"])
        self.assertFalse(result["checks"][1]["passed"])
        self.assertFalse(score_task(task(), truth(), output(claim="Not guaranteed"))["checks"][2]["passed"])

    def test_generic_summary_contains_accepts_capitalized_subject(self):
        expected = truth(checks=[rule("summary", "synthetic assay study K123", "contains")],
                         check_kinds=["generic"])
        for text in ("Synthetic assay study K123 compares measurement runs.",
                     "The SYNTHETIC ASSAY STUDY K123 compares measurement runs."):
            with self.subTest(text=text):
                self.assertTrue(score_task(task(), expected, output(summary=text))["completed"])

    def test_generic_summary_contains_still_rejects_wrong_or_missing_subject(self):
        expected = truth(checks=[rule("summary", "synthetic assay study K123", "contains")],
                         check_kinds=["generic"])
        for text in ("Synthetic assay study K999 compares measurement runs.",
                     "Synthetic assay study compares measurement runs.", "  "):
            with self.subTest(text=text):
                self.assertFalse(score_task(task(), expected, output(summary=text))["completed"])
        self.assertFalse(score_task(task(), expected, output())["completed"])

    def test_source_identifier_case_stays_exact_despite_summary_casefold(self):
        expected = truth(checks=[rule("source_id", "Source-ABC"),
                                 rule("summary", "synthetic assay study K123", "contains")],
                         check_kinds=["explicit", "generic"])
        result = score_task(task(), expected, output(source_id="source-abc", summary="Synthetic assay study K123"))
        self.assertFalse(result["checks"][0]["passed"])
        self.assertTrue(result["checks"][1]["passed"])
        self.assertFalse(result["completed"])

    def test_contains_casefold_does_not_extend_to_other_fields_or_check_kinds(self):
        for field, kind in (("citation", "generic"), ("summary", "explicit"), ("summary", "hidden")):
            with self.subTest(field=field, kind=kind):
                expected = truth(checks=[rule(field, "subject", "contains")], check_kinds=[kind])
                self.assertFalse(score_task(task(), expected, output(**{field: "Subject"}))["completed"])
        expected = truth(checks=[rule("summary", "subject", "equals")], check_kinds=["generic"])
        self.assertFalse(score_task(task(), expected, output(summary="Subject"))["completed"])

    def test_invalid_none_wrong_case_and_wrong_type_fail_all_checks(self):
        wrong_case = output()
        wrong_case.case_id = "another-case"
        for value in (None, {}, wrong_case):
            with self.subTest(value=value):
                result = score_task(task(), truth(), value)
                self.assertFalse(result["output_valid"])
                self.assertEqual(result["compliance"], 0)
                self.assertTrue(all(check["passed"] is False for check in result["checks"]))
                self.assertIsNone(result["distractor_adoptions"])

    def test_normalized_duplicate_field_names_fail_closed(self):
        value = output()
        value.fields.append(type(value.fields[0])(name=" opening ", value="joke"))
        self.assertFalse(score_task(task(), truth(), value)["output_valid"])

    def test_ordinary_clarification_and_deferral_fail_all_checks(self):
        for action in ("clarify", "defer"):
            with self.subTest(action=action):
                result = score_task(task(), truth(), output(action=action))
                self.assertTrue(result["unnecessary_abstention"])
                self.assertFalse(result["action_correct"])
                self.assertEqual(result["compliance"], 0)

    def test_correct_ambiguous_action_does_not_guess_hidden_rule_or_complete_task(self):
        expected = truth(category="ambiguous", allowed_actions=["clarify", "defer"],
                         missing_fields=["audience"])
        for action in ("clarify", "defer"):
            with self.subTest(action=action):
                value = WorkOutput(case_id="case-1", action=action, missing_fields=["audience"])
                result = score_task(task(), expected, value)
                self.assertTrue(result["action_correct"])
                self.assertTrue(result["task_passed"])
                self.assertFalse(result["completed"])
                self.assertIsNone(result["compliance"])
                self.assertTrue(all(check["passed"] is None for check in result["checks"]))

    def test_ambiguous_case_requires_correct_missing_field(self):
        expected = truth(category="ambiguous", allowed_actions=["clarify"], missing_fields=["audience"])
        for fields in ([], ["approval"], ["audience", "irrelevant"]):
            with self.subTest(fields=fields):
                result = score_task(task(), expected, output(action="clarify", missing_fields=fields))
                self.assertTrue(result["action_allowed"])
                self.assertFalse(result["action_correct"])
                self.assertFalse(result["task_passed"])

    def test_asking_and_guessing_an_unresolved_field_is_not_appropriate(self):
        expected = truth(category="ambiguous", allowed_actions=["clarify", "defer"],
                         missing_fields=["audience"], unresolved_output_fields=["emphasis"])
        for action in ("clarify", "defer"):
            with self.subTest(action=action):
                result = score_task(task(), expected, output(action=action, missing_fields=["audience"],
                                                             emphasis="career progression"))
                self.assertTrue(result["action_correct"])
                self.assertFalse(result["action_appropriate"])
                self.assertTrue(result["unsafe_guess"])
                self.assertEqual(result["unsafe_guess_fields"], ["emphasis"])
                self.assertFalse(result["task_passed"])
                self.assertIsNone(result["compliance"])

    def test_unresolved_field_can_be_absent_blank_or_literal_undetermined(self):
        expected = truth(category="ambiguous", allowed_actions=["clarify"],
                         missing_fields=["audience"], unresolved_output_fields=["emphasis"])
        for extra in ({}, {"emphasis": "  "}, {"emphasis": " undetermined "}):
            with self.subTest(extra=extra):
                result = score_task(task(), expected, output(action="clarify", missing_fields=["audience"],
                                                             **extra))
                self.assertTrue(result["action_appropriate"])
                self.assertFalse(result["unsafe_guess"])
                self.assertTrue(result["task_passed"])

    def test_guessing_ambiguous_rule_never_receives_delivery_credit(self):
        expected = truth(category="ambiguous", allowed_actions=["clarify"], missing_fields=["audience"])
        result = score_task(task(), expected, output())
        self.assertTrue(result["missed_required_abstention"])
        self.assertFalse(result["task_passed"])
        self.assertFalse(result["completed"])
        self.assertIsNone(result["compliance"])

    def test_invalid_ambiguous_output_remains_a_failed_attempt(self):
        expected = truth(category="ambiguous", allowed_actions=["defer"], missing_fields=["audience"])
        result = score_task(task(), expected, None)
        self.assertEqual(result["compliance"], 0)
        self.assertTrue(all(check["passed"] is False for check in result["checks"]))

    def test_nonapplicable_and_unknown_checks_are_not_vacuous_passes(self):
        expected = truth(checks=[rule(), rule("x", "v", scope=Scope(match={"audience": ["apprentice"]})),
                                 rule("y", "v", scope=Scope(match={"region": ["west"]}))])
        result = score_task(task(), expected, output())
        self.assertEqual(result["evaluated_checks"], 1)
        self.assertIsNone(result["checks"][1]["passed"])
        self.assertEqual(result["checks"][1]["reason"], "out_of_scope")
        self.assertEqual(result["checks"][2]["reason"], "unknown_scope")

    def test_distractor_adoption_is_separate_from_compliance(self):
        result = score_task(task(), truth(), output(opening="joke"))
        self.assertEqual(result["distractor_adoptions"], 1)
        self.assertEqual(result["distractor_adoption_rate"], 1)
        self.assertEqual(result["by_kind"]["hidden"]["rate"], 0)

    def test_task_truth_mismatch_is_an_evaluator_error(self):
        with self.assertRaises(ValueError):
            score_task(task(), truth(case_id="wrong"), output())


class PreparationEvaluationTests(unittest.TestCase):
    def test_supported_exceptions_default_to_empty_for_existing_truth(self):
        self.assertEqual(family_truth().supported_exceptions, [])

    def test_valid_outside_channel_rules_are_separate_from_standing_requirements(self):
        expected = family_truth()
        outside = Scope(match={"role": ["recruiting"], "channel": ["internal"]})
        local_rules = [rule(value="internal_update", scope=outside),
                       rule("route", "team_owner", scope=outside)]
        expected.supported_exceptions = local_rules
        expected.distractors.extend(local_rules)
        result = score_preparation(preparation((expected.recoverable[0], "adopt"),
                                               *[(r, "adopt") for r in local_rules]), expected)
        self.assertEqual(result["accepted_local_observations"], 2)
        self.assertEqual(result["raw_accepted_local_adoptions"], 2)
        self.assertEqual(result["raw_adoption_count"], 3)
        self.assertEqual(result["unique_adopted_bodies"], 3)
        self.assertEqual(result["precision_denominator"], 1)
        self.assertEqual(result["precision"], 1)
        self.assertEqual(result["recall"], 1)
        self.assertEqual(result["scoped_precision"], 1)
        self.assertEqual(result["false_positives"], 0)
        self.assertEqual(result["distractor_adoptions"], 0)

    def test_local_showcase_preference_is_not_an_error_or_recall_target(self):
        expected = family_truth()
        scope = Scope(match={"role": ["recruiting"], "channel": ["external"],
                             "audience": ["specialist"], "occasion": ["showcase"]})
        local = rule(value="joke", scope=scope)
        expected.supported_exceptions = [local]
        reordered = rule(value="joke", scope=Scope(match=dict(reversed(list(scope.match.items())))))
        result = score_preparation(preparation((local, "adopt"), (reordered, "adopt")), expected)
        self.assertEqual(result["accepted_local_observations"], 1)
        self.assertEqual(result["raw_accepted_local_adoptions"], 2)
        self.assertEqual(result["duplicate_adopted_bodies"], 1)
        self.assertEqual(result["precision_denominator"], 0)
        self.assertIsNone(result["precision"])
        self.assertIsNone(result["scoped_precision"])
        self.assertEqual(result["recall"], 0)
        self.assertEqual(result["false_negatives"], 1)
        self.assertEqual(result["false_positives"], 0)
        self.assertEqual(result["distractor_adoptions"], 0)

    def test_narrower_exception_scope_remains_supported(self):
        expected = family_truth()
        exception = rule(value="joke", scope=Scope(match={"occasion": ["showcase", "workshop"]}))
        expected.supported_exceptions = [exception]
        local = rule(value="joke", scope=Scope(match={"occasion": ["showcase"], "audience": ["specialist"]}))
        result = score_preparation(preparation((local, "adopt")), expected)
        self.assertEqual(result["accepted_local_observations"], 1)
        self.assertEqual(result["false_positives"], 0)

    def test_missing_or_broader_exception_scope_remains_false_positive_and_distractor(self):
        expected = family_truth()
        exception = rule(value="joke", scope=Scope(match={"channel": ["external"], "occasion": ["showcase"]}))
        expected.supported_exceptions = [exception]
        for scope in (None, Scope(match={"channel": ["external"]}),
                      Scope(match={"channel": ["external"], "occasion": ["showcase", "routine"]}),
                      Scope(match={"channel": ["internal"], "occasion": ["showcase"]})):
            with self.subTest(scope=scope):
                result = score_preparation(preparation((rule(value="joke", scope=scope), "adopt")), expected)
                self.assertEqual(result["accepted_local_observations"], 0)
                self.assertEqual(result["precision_denominator"], 1)
                self.assertEqual(result["false_positives"], 1)
                self.assertEqual(result["distractor_adoptions"], 1)
                self.assertEqual(result["precision"], 0)

    def test_local_rule_does_not_exempt_same_body_with_overbroad_scope(self):
        expected = family_truth()
        local = rule(value="joke", scope=Scope(match={"occasion": ["showcase"]}))
        expected.supported_exceptions = [local]
        for mixed in ((local, rule(value="joke")), (rule(value="joke"), local, local)):
            with self.subTest(mixed=mixed):
                result = score_preparation(preparation((expected.recoverable[0], "adopt"),
                                                       *[(r, "adopt") for r in mixed]), expected)
                self.assertEqual(result["accepted_local_observations"], 1)
                self.assertEqual(result["unique_adopted_bodies"], 2)
                self.assertEqual(result["precision_denominator"], 2)
                self.assertEqual(result["false_positives"], 1)
                self.assertEqual(result["distractor_adoptions"], 1)
                self.assertEqual(result["precision"], 0.5)
                self.assertEqual(result["scoped_precision"], 0.5)
                self.assertEqual(result["recall"], 1)

    def test_exception_requires_matching_body_and_an_explicit_exception_scope(self):
        expected = family_truth()
        local_scope = Scope(match={"occasion": ["showcase"]})
        expected.supported_exceptions = [rule(value="joke", scope=local_scope)]
        for candidate in (rule(value="joke", operator="contains", scope=local_scope),
                          rule(value="Joke", scope=local_scope),
                          rule("different_field", "joke", scope=local_scope)):
            with self.subTest(candidate=candidate):
                result = score_preparation(preparation((candidate, "adopt")), expected)
                self.assertEqual(result["accepted_local_observations"], 0)
                self.assertEqual(result["false_positives"], 1)
        expected.supported_exceptions = [rule(value="joke")]
        result = score_preparation(preparation((rule(value="joke", scope=local_scope), "adopt")), expected)
        self.assertEqual(result["accepted_local_observations"], 0)
        self.assertEqual(result["false_positives"], 1)

    def test_unadopted_exception_is_not_counted_as_local_observation(self):
        expected = family_truth()
        local = rule(value="joke", scope=Scope(match={"occasion": ["showcase"]}))
        expected.supported_exceptions = [local]
        result = score_preparation(preparation((local, "defer"), (local, "clarify")), expected)
        self.assertEqual(result["accepted_local_observations"], 0)
        self.assertEqual(result["raw_accepted_local_adoptions"], 0)
        self.assertEqual(result["precision_denominator"], 0)

    def test_correct_body_and_scope_score_separately(self):
        expected = family_truth()
        result = score_preparation(preparation((expected.recoverable[0], "adopt")), expected)
        for key in ("precision", "recall", "scope_accuracy", "scoped_precision", "scoped_recall"):
            self.assertEqual(result[key], 1, key)
        self.assertEqual(result["unknown_scope_accuracy"], 1)

    def test_duplicates_do_not_increase_recall_or_precision(self):
        expected = family_truth()
        prediction = expected.recoverable[0]
        result = score_preparation(preparation((prediction, "adopt"), (prediction, "adopt")), expected)
        self.assertEqual(result["true_positives"], 1)
        self.assertEqual(result["unique_adopted_bodies"], 1)
        self.assertEqual(result["duplicate_adopted_bodies"], 1)
        self.assertEqual(result["recall"], 1)

    def test_empty_adoption_has_undefined_precision_and_zero_recall(self):
        result = score_preparation(Preparation(), family_truth())
        self.assertIsNone(result["precision"])
        self.assertEqual(result["recall"], 0)
        self.assertIsNone(result["scope_accuracy"])

    def test_unidentifiable_and_distractor_adoption_are_false_positives(self):
        expected = family_truth()
        result = score_preparation(preparation((expected.recoverable[0], "adopt"),
                                               (expected.unidentifiable[0], "adopt"),
                                               (expected.distractors[0], "adopt")), expected)
        self.assertEqual(result["precision"], 1 / 3)
        self.assertEqual(result["recall"], 1)
        self.assertEqual(result["false_positives"], 2)
        self.assertEqual(result["unidentifiable_adoptions"], 1)
        self.assertEqual(result["distractor_adoptions"], 1)

    def test_unidentifiable_deferral_is_not_false_negative(self):
        expected = family_truth()
        result = score_preparation(preparation((expected.recoverable[0], "adopt"),
                                               (expected.unidentifiable[0], "defer")), expected)
        self.assertEqual(result["false_negatives"], 0)
        self.assertEqual(result["unidentifiable_abstentions"], 1)
        self.assertEqual(result["precision"], 1)

    def test_recoverable_deferral_does_count_as_missed_requirement(self):
        expected = family_truth()
        result = score_preparation(preparation((expected.recoverable[0], "defer")), expected)
        self.assertEqual(result["false_negatives"], 1)
        self.assertEqual(result["recall"], 0)

    def test_missing_scope_is_overbroad_even_if_body_matches(self):
        result = score_preparation(preparation((rule(), "adopt")), family_truth())
        self.assertEqual(result["precision"], 1)
        self.assertEqual(result["scope_overbroad"], 2)
        self.assertEqual(result["scope_accuracy"], 1 / 3)
        self.assertEqual(result["scoped_precision"], 0)

    def test_excessive_scope_restriction_is_overnarrow(self):
        narrow = rule(scope=Scope(match={"audience": ["specialist"], "region": ["west"]}))
        result = score_preparation(preparation((narrow, "adopt")), family_truth())
        self.assertEqual(result["scope_overnarrow"], 1)
        self.assertEqual(result["scope_overbroad"], 0)

    def test_multiple_predicted_scopes_are_evaluated_as_union(self):
        expected = family_truth()
        broad = rule(scope=Scope(match={"audience": ["apprentice"]}))
        result = score_preparation(preparation((expected.recoverable[0], "adopt"), (broad, "adopt")), expected)
        self.assertEqual(result["unique_adopted_bodies"], 1)
        self.assertEqual(result["scope_overbroad"], 1)
        self.assertEqual(result["scoped_recall"], 0)

    def test_operator_and_value_are_part_of_body_match(self):
        for wrong in (rule(operator="contains"), rule(value="Problem"), rule(field="claim")):
            with self.subTest(wrong=wrong):
                result = score_preparation(preparation((wrong, "adopt")), family_truth())
                self.assertEqual(result["precision"], 0)
                self.assertEqual(result["recall"], 0)

    def test_absent_probe_or_gold_denominator_is_not_reported_as_perfect(self):
        expected = family_truth()
        expected.scope_probes = []
        result = score_preparation(preparation((expected.recoverable[0], "adopt")), expected)
        self.assertIsNone(result["scoped_precision"])
        self.assertIsNone(result["scope_accuracy"])
        expected.recoverable = []
        self.assertIsNone(score_preparation(Preparation(), expected)["recall"])


if __name__ == "__main__":
    unittest.main()
