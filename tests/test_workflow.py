"""Protocol regression tests; every datum and rating here is invented.

Some records deliberately use ``origin='human_rating'`` to exercise the branch
for caller-supplied non-fixture ratings. They are NOT empirical human ratings and
must never be reported as evidence that the proposed research method works.
"""

from __future__ import annotations

import unittest

from pydantic import ValidationError

from grounded_reflection.models import (
    CandidateUpdate, EvidenceBundle, EvidenceReference, PairedEvaluation,
    Provenance, Scope, SelectionPolicy, SplitManifest, WorkEpisode,
)
from grounded_reflection.workflow import (
    assess_candidate, context_artifact, digest, select_update, verify_references,
)


CONTEXT = {"role": "hr", "audience": "specialists", "project": "atlas"}


def make_bundle() -> EvidenceBundle:
    """Small self-contained synthetic fixture, independent of the showcase demo."""
    return EvidenceBundle.model_validate({
        "episodes": [{
            "episode_id": "dev-1", "split": "development", "context": CONTEXT,
            "task": "Draft a specialist recruiting message.",
            "evidence": [{
                "evidence_id": "feedback-1", "kind": "human_feedback",
                "text": "Lead with the scientific challenge for this audience.",
                "provenance": {
                    "origin": "synthetic", "source_id": "unit-test-fixture",
                    "recorded_at": "2026-09-01T10:00:00Z",
                },
            }],
        }],
        "hypotheses": [{
            "hypothesis_id": "h-1",
            "claim": "The specialist audience may prefer the scientific challenge first.",
            "scope": {"match": {k: [v] for k, v in CONTEXT.items()}},
            "support": [{
                "episode_id": "dev-1", "evidence_id": "feedback-1",
                "quote": "Lead with the scientific challenge",
            }],
            "origin": "curated_fixture",
        }],
        "candidates": [{
            "candidate_id": "candidate-1", "hypothesis_id": "h-1",
            "scope": {"match": {k: [v] for k, v in CONTEXT.items()}},
            "target": "context", "patch": "Introduce the scientific challenge first.",
            "expected_effect": {
                "metric": "professional_quality",
                "prediction": "Improve rubric-assessed audience fit.",
            },
        }],
    })


def make_splits() -> SplitManifest:
    return SplitManifest(development=["dev-1"], validation=["val-1", "val-2"],
                         final_test=["final-1"])


def make_records(origin: str = "fixture", candidate: CandidateUpdate | None = None) -> list[PairedEvaluation]:
    candidate = candidate or make_bundle().candidates[0]
    return [PairedEvaluation(
        case_id=case_id, split="validation", baseline_version="baseline-v1",
        candidate_id=candidate.candidate_id, candidate_digest=digest(candidate), context=CONTEXT,
        baseline_score=0.5, candidate_score=0.7,
        baseline_critical_errors=0, candidate_critical_errors=0,
        baseline_human_seconds=120, candidate_human_seconds=100,
        origin=origin, evaluator="synthetic-unit-test-only",
    ) for case_id in ("val-1", "val-2")]


class ContractTests(unittest.TestCase):
    def test_unknown_fields_are_rejected(self):
        raw = make_bundle().model_dump(mode="json")
        raw["silent_extra_data"] = "should not disappear"
        with self.assertRaises(ValidationError):
            EvidenceBundle.model_validate(raw)

    def test_provenance_requires_timezone(self):
        with self.assertRaises(ValidationError):
            Provenance(origin="synthetic", source_id="test",
                       recorded_at="2026-09-01T10:00:00")

    def test_whitespace_only_reference_is_rejected_and_verbatim_quote_preserved(self):
        for quote in ("", " ", "\n\t"):
            with self.subTest(quote=repr(quote)):
                with self.assertRaises(ValidationError):
                    EvidenceReference(episode_id="dev-1", evidence_id="feedback-1", quote=quote)
        reference = EvidenceReference(episode_id="dev-1", evidence_id="feedback-1",
                                      quote=" the scientific challenge ")
        self.assertEqual(reference.quote, " the scientific challenge ")

    def test_generated_evidence_requires_model_identifier(self):
        with self.assertRaises(ValidationError):
            Provenance(origin="model_generated", source_id="test",
                       recorded_at="2026-09-01T10:00:00Z")

    def test_duplicate_evidence_ids_are_rejected(self):
        raw = make_bundle().episodes[0].model_dump(mode="json")
        raw["evidence"].append(raw["evidence"][0].copy())
        with self.assertRaises(ValidationError):
            WorkEpisode.model_validate(raw)

    def test_unknown_candidate_hypothesis_is_rejected_at_parse_time(self):
        raw = make_bundle().model_dump(mode="json")
        raw["candidates"][0]["hypothesis_id"] = "unseen-hypothesis"
        with self.assertRaises(ValidationError):
            EvidenceBundle.model_validate(raw)

    def test_duplicate_candidate_ids_are_rejected(self):
        raw = make_bundle().model_dump(mode="json")
        raw["candidates"].append(raw["candidates"][0].copy())
        with self.assertRaises(ValidationError):
            EvidenceBundle.model_validate(raw)

    def test_split_overlap_and_duplicates_are_rejected(self):
        for updates in ({"validation": ["dev-1"]},
                        {"final_test": ["val-1"]},
                        {"development": ["dev-1", "dev-1"]}):
            with self.subTest(updates=updates):
                raw = make_splits().model_dump()
                raw.update(updates)
                with self.assertRaises(ValidationError):
                    SplitManifest.model_validate(raw)

    def test_ratings_must_be_finite_and_bounded(self):
        for field, value in (("candidate_score", float("nan")),
                             ("candidate_score", float("inf")),
                             ("candidate_score", 1.1),
                             ("baseline_score", -0.1),
                             ("candidate_human_seconds", -1),
                             ("baseline_human_seconds", float("inf"))):
            with self.subTest(field=field, value=value):
                raw = make_records()[0].model_dump()
                raw[field] = value
                with self.assertRaises(ValidationError):
                    PairedEvaluation.model_validate(raw)

    def test_critical_error_checks_cannot_be_silently_omitted(self):
        for field in ("baseline_critical_errors", "candidate_critical_errors"):
            with self.subTest(field=field):
                raw = make_records()[0].model_dump()
                del raw[field]
                with self.assertRaises(ValidationError):
                    PairedEvaluation.model_validate(raw)

    def test_ratings_must_identify_exact_candidate_content(self):
        raw = make_records()[0].model_dump()
        del raw["candidate_digest"]
        with self.assertRaises(ValidationError):
            PairedEvaluation.model_validate(raw)


class EvidenceAndScopeTests(unittest.TestCase):
    def setUp(self):
        self.bundle = make_bundle()
        self.candidate = self.bundle.candidates[0]
        self.hypothesis = self.bundle.hypotheses[0]

    def test_exact_reference_resolves_but_does_not_establish_effect(self):
        self.assertEqual(verify_references(self.hypothesis, self.bundle.episodes), [])
        assessment = assess_candidate(self.candidate, self.bundle)
        self.assertEqual(assessment.status, "eligible_for_validation")
        self.assertEqual(assessment.verified_reference_count, 1)

    def test_fabricated_quote_is_rejected(self):
        self.hypothesis.support[0].quote = "This fabricated sentence is absent."
        assessment = assess_candidate(self.candidate, self.bundle)
        self.assertEqual(assessment.status, "rejected")
        self.assertTrue(any("Quote not found" in reason for reason in assessment.reasons))

    def test_missing_episode_or_evidence_is_rejected(self):
        for field in ("episode_id", "evidence_id"):
            with self.subTest(field=field):
                bundle = make_bundle()
                setattr(bundle.hypotheses[0].support[0], field, "absent")
                self.assertEqual(assess_candidate(bundle.candidates[0], bundle).status,
                                 "rejected")

    def test_counterevidence_references_are_also_verified(self):
        self.hypothesis.counterevidence.append(EvidenceReference(
            episode_id="dev-1", evidence_id="feedback-1", quote="An invented counterexample"))
        self.assertEqual(assess_candidate(self.candidate, self.bundle).status, "rejected")

    def test_duplicate_episode_list_cannot_resolve_ambiguously(self):
        problems = verify_references(self.hypothesis,
                                     self.bundle.episodes + self.bundle.episodes)
        self.assertIn("Duplicate episode IDs", problems)

    def test_non_development_reference_is_rejected(self):
        for split in ("validation", "final_test"):
            with self.subTest(split=split):
                self.bundle.episodes[0].split = split
                self.assertEqual(assess_candidate(self.candidate, self.bundle).status,
                                 "rejected")

    def test_scope_cannot_drop_supporting_constraints(self):
        self.candidate.scope = Scope(match={"role": ["hr"]})
        self.assertEqual(assess_candidate(self.candidate, self.bundle).status, "rejected")

    def test_scope_cannot_add_unsupported_allowed_values(self):
        self.candidate.scope.match["audience"].append("apprentices")
        self.assertEqual(assess_candidate(self.candidate, self.bundle).status, "rejected")

    def test_narrower_scope_is_permitted(self):
        self.candidate.scope.match["channel"] = ["linkedin"]
        self.assertEqual(assess_candidate(self.candidate, self.bundle).status,
                         "eligible_for_validation")

    def test_missing_context_is_unknown_and_observed_conflict_is_mismatch(self):
        self.assertEqual(self.candidate.scope.applies_to({"role": "hr"}), "unknown")
        self.assertEqual(self.candidate.scope.applies_to({"role": "sales"}), "mismatch")
        self.assertEqual(self.candidate.scope.applies_to(CONTEXT), "match")

    def test_candidate_blocker_defers_while_general_research_question_does_not(self):
        self.hypothesis.unresolved_questions = ["Does this transfer to another organization?"]
        self.assertEqual(assess_candidate(self.candidate, self.bundle).status,
                         "eligible_for_validation")
        self.candidate.blocking_questions = ["Which contradictory source governs this task?"]
        self.assertEqual(assess_candidate(self.candidate, self.bundle).status,
                         "needs_clarification")


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.bundle = make_bundle()
        self.candidate = self.bundle.candidates[0]
        self.records = make_records()
        self.splits = make_splits()

    def select(self, **overrides):
        params = dict(candidate=self.candidate, bundle=self.bundle,
                      records=self.records, splits=self.splits,
                      baseline_version="baseline-v1")
        params.update(overrides)
        return select_update(**params)

    def assert_baseline_preserved(self, decision, status="rejected"):
        self.assertEqual(decision.status, status)
        self.assertEqual(decision.active_version, "baseline-v1")

    def test_no_or_insufficient_validation_defers(self):
        for records in ([], self.records[:1]):
            with self.subTest(count=len(records)):
                self.assert_baseline_preserved(self.select(records=records), "deferred")

    def test_tie_keeps_baseline(self):
        for record in self.records:
            record.candidate_score = record.baseline_score
        self.assert_baseline_preserved(self.select())

    def test_critical_error_rejects_despite_quality_gain(self):
        self.records[1].candidate_critical_errors = 1
        decision = self.select()
        self.assert_baseline_preserved(decision)
        self.assertGreater(decision.mean_quality_gain, 0)
        self.assertTrue(any("critical error" in reason for reason in decision.reasons))

    def test_one_case_regression_rejects_despite_mean_gain(self):
        self.records[0].candidate_score = 0.4
        self.records[1].candidate_score = 0.9
        decision = self.select()
        self.assert_baseline_preserved(decision)
        self.assertGreater(decision.mean_quality_gain, 0.05)

    def test_excess_human_effort_rejects(self):
        for record in self.records:
            record.candidate_human_seconds = 121
        self.assert_baseline_preserved(self.select())

    def test_explicit_effort_budget_controls_selection(self):
        for record in self.records:
            record.candidate_human_seconds = 121
        decision = self.select(policy=SelectionPolicy(max_mean_effort_increase=1))
        self.assertEqual(decision.status, "accepted")
        self.assertEqual(decision.policy.max_mean_effort_increase, 1)

    def test_minimum_gain_policy_is_applied(self):
        self.assert_baseline_preserved(self.select(policy=SelectionPolicy(min_mean_gain=0.3)))

    def test_blocked_candidate_remains_deferred_even_with_high_ratings(self):
        self.candidate.blocking_questions = ["Resolve contradictory role requirements."]
        self.assert_baseline_preserved(self.select(records=make_records(candidate=self.candidate)), "deferred")

    def test_invalid_evidence_cannot_be_rescued_by_high_ratings(self):
        self.bundle.hypotheses[0].support[0].quote = "An absent supporting quotation"
        self.assert_baseline_preserved(self.select())

    def test_all_inference_episodes_must_be_declared_development_cases(self):
        self.bundle.episodes[0].episode_id = "unregistered"
        with self.assertRaisesRegex(ValueError, "declared development"):
            self.select()

    def test_unreferenced_final_episode_still_cannot_enter_inference_bundle(self):
        leaked = self.bundle.episodes[0].model_copy(deep=True)
        leaked.episode_id = "final-1"
        leaked.split = "final_test"
        self.bundle.episodes.append(leaked)
        with self.assertRaisesRegex(ValueError, "declared development"):
            self.select()

    def test_final_test_record_is_refused_even_if_mislabeled_validation(self):
        for split in ("final_test", "validation"):
            with self.subTest(split=split):
                self.records[0].case_id = "final-1"
                self.records[0].split = split
                with self.assertRaisesRegex(ValueError, "declared validation"):
                    self.select()

    def test_wrong_split_is_refused_even_with_validation_case_id(self):
        self.records[0].split = "development"
        with self.assertRaisesRegex(ValueError, "declared validation"):
            self.select()

    def test_duplicate_validation_case_is_refused(self):
        self.records[1].case_id = self.records[0].case_id
        with self.assertRaisesRegex(ValueError, "Duplicate evaluation"):
            self.select()

    def test_ratings_must_match_candidate_and_baseline(self):
        for field in ("candidate_id", "baseline_version"):
            with self.subTest(field=field):
                records = make_records()
                setattr(records[0], field, "another-version")
                with self.assertRaisesRegex(ValueError, "candidate and baseline"):
                    self.select(records=records)

    def test_rated_metric_must_match_prediction(self):
        self.candidate.expected_effect.metric = "different_metric"
        with self.assertRaisesRegex(ValueError, "metric"):
            self.select(records=make_records(candidate=self.candidate))

    def test_old_ratings_cannot_accept_changed_patch_under_same_candidate_id(self):
        self.candidate.patch = "An untested replacement instruction."
        with self.assertRaisesRegex(ValueError, "candidate and baseline"):
            self.select()

    def test_old_ratings_cannot_accept_changed_scope_under_same_candidate_id(self):
        self.candidate.scope.match["channel"] = ["linkedin"]
        for record in self.records:
            record.context["channel"] = "linkedin"
        with self.assertRaisesRegex(ValueError, "candidate and baseline"):
            self.select()

    def test_missing_or_out_of_scope_validation_context_is_refused(self):
        for context in ({"role": "hr"}, {**CONTEXT, "project": "other-project"}):
            with self.subTest(context=context):
                self.records[0].context = context
                with self.assertRaisesRegex(ValueError, "outside scope"):
                    self.select()

    def test_baseline_version_required(self):
        with self.assertRaisesRegex(ValueError, "baseline_version"):
            self.select(baseline_version="")

    def test_accepted_branch_exports_versioned_context_with_provenance(self):
        # Synthetic records exercise a caller-supplied human_rating code path.
        records = make_records(origin="human_rating")
        decision = self.select(records=records)
        self.assertEqual(decision.status, "accepted")
        self.assertNotEqual(decision.active_version, "baseline-v1")
        artifact = context_artifact(self.candidate, decision)
        self.assertEqual(artifact["instruction"], self.candidate.patch)
        self.assertEqual(artifact["baseline_version"], "baseline-v1")
        self.assertEqual(artifact["decision"]["candidate_digest"], digest(self.candidate))
        self.assertEqual(artifact["decision"]["record_origins"], ["human_rating"])

    def test_fixture_ratings_can_exercise_policy_but_cannot_export_update(self):
        decision = self.select()
        self.assertEqual(decision.status, "accepted")
        with self.assertRaisesRegex(ValueError, "Fixture evaluations"):
            context_artifact(self.candidate, decision)

    def test_missing_rating_origins_cannot_export_update(self):
        decision = self.select(records=make_records(origin="human_rating"))
        decision.record_origins = []
        with self.assertRaises(ValueError):
            context_artifact(self.candidate, decision)

    def test_mixed_fixture_and_nonfixture_ratings_cannot_export(self):
        self.records[0].origin = "human_rating"
        decision = self.select()
        self.assertEqual(decision.record_origins, ["fixture", "human_rating"])
        with self.assertRaisesRegex(ValueError, "Fixture evaluations"):
            context_artifact(self.candidate, decision)

    def test_mutating_candidate_after_selection_blocks_export(self):
        decision = self.select(records=make_records(origin="human_rating"))
        self.candidate.patch = "A different update that was never rated."
        with self.assertRaisesRegex(ValueError, "matching accepted decision"):
            context_artifact(self.candidate, decision)

    def test_deferred_or_rejected_decision_cannot_export(self):
        deferred = self.select(records=[])
        with self.assertRaisesRegex(ValueError, "matching accepted decision"):
            context_artifact(self.candidate, deferred)
        for record in self.records:
            record.candidate_score = 0.1
        rejected = self.select()
        with self.assertRaisesRegex(ValueError, "matching accepted decision"):
            context_artifact(self.candidate, rejected)

    def test_same_inputs_produce_same_decision_and_changed_ratings_change_digest(self):
        first = self.select()
        self.assertEqual(first.model_dump(), self.select().model_dump())
        self.records[0].candidate_score = 0.8
        revised = self.select()
        self.assertEqual(first.candidate_digest, revised.candidate_digest)
        self.assertNotEqual(first.evaluation_digest, revised.evaluation_digest)

    def test_digest_is_insensitive_to_mapping_insertion_order(self):
        self.assertEqual(digest({"a": 1, "b": 2}), digest({"b": 2, "a": 1}))


if __name__ == "__main__":
    unittest.main()
