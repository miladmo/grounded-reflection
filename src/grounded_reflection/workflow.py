"""Executable protocol checks, not a learned reflection or causal-inference method."""

from __future__ import annotations

import hashlib
import json
from statistics import mean
from typing import Protocol

from .models import (
    CandidateAssessment, CandidateUpdate, EvidenceBundle, Hypothesis, PairedEvaluation,
    SelectionDecision, SelectionPolicy, SplitManifest, WorkEpisode,
)


def digest(value) -> str:
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False, allow_nan=False).encode()).hexdigest()


class ReflectionBackend(Protocol):
    """An extension interface. No learned backend is bundled in v0.1."""

    def infer(self, episodes: list[WorkEpisode]) -> list[Hypothesis]: ...


def verify_references(hypothesis: Hypothesis, episodes: list[WorkEpisode]) -> list[str]:
    problems = []
    lookup = {ep.episode_id: ep for ep in episodes}
    if len(lookup) != len(episodes):
        return ["Duplicate episode IDs"]
    for reference in hypothesis.support + hypothesis.counterevidence:
        episode = lookup.get(reference.episode_id)
        if episode is None:
            problems.append(f"Unknown episode: {reference.episode_id}")
            continue
        if episode.split != "development":
            problems.append(f"Inference evidence must be development-only: {episode.episode_id}")
        item = next((e for e in episode.evidence if e.evidence_id == reference.evidence_id), None)
        if item is None:
            problems.append(f"Unknown evidence: {reference.episode_id}/{reference.evidence_id}")
        elif reference.quote not in item.text:
            problems.append(f"Quote not found: {reference.episode_id}/{reference.evidence_id}")
    return problems


def assess_candidate(candidate: CandidateUpdate, bundle: EvidenceBundle) -> CandidateAssessment:
    hypothesis = next((h for h in bundle.hypotheses if h.hypothesis_id == candidate.hypothesis_id), None)
    if hypothesis is None:
        return CandidateAssessment(candidate_id=candidate.candidate_id, status="rejected",
                                   reasons=["Unknown hypothesis"], verified_reference_count=0)
    problems = verify_references(hypothesis, bundle.episodes)
    if not candidate.scope.is_within(hypothesis.scope):
        problems.append("Candidate scope extends beyond its supporting hypothesis")
    count = len(hypothesis.support) + len(hypothesis.counterevidence)
    if problems:
        return CandidateAssessment(candidate_id=candidate.candidate_id, status="rejected",
                                   reasons=problems, verified_reference_count=0)
    if candidate.blocking_questions:
        return CandidateAssessment(candidate_id=candidate.candidate_id, status="needs_clarification",
                                   reasons=list(candidate.blocking_questions), verified_reference_count=count)
    return CandidateAssessment(
        candidate_id=candidate.candidate_id, status="eligible_for_validation",
        reasons=["References resolve and candidate scope is bounded; evidential validity still requires evaluation"],
        verified_reference_count=count,
    )


def select_update(candidate: CandidateUpdate, bundle: EvidenceBundle,
                  records: list[PairedEvaluation], splits: SplitManifest,
                  baseline_version: str, policy: SelectionPolicy | None = None) -> SelectionDecision:
    """Apply a declared policy to paired validation records; never read final results.

    Ratings come from the caller. These guards cannot establish their honesty,
    blinding, quality or the statistical generality of any apparent gain.
    """
    policy = policy or SelectionPolicy()
    if not baseline_version:
        raise ValueError("baseline_version is required")
    if any(ep.split != "development" or ep.episode_id not in splits.development
           for ep in bundle.episodes):
        raise ValueError("Evidence bundle must contain only declared development episodes")
    if len({r.case_id for r in records}) != len(records):
        raise ValueError("Duplicate evaluation cases")
    for record in records:
        if record.split != "validation" or record.case_id not in splits.validation:
            raise ValueError("Update selection accepts only declared validation cases")
        if (record.candidate_id != candidate.candidate_id or record.candidate_digest != digest(candidate)
                or record.baseline_version != baseline_version):
            raise ValueError("Evaluation does not match this candidate and baseline")
        if record.metric != candidate.expected_effect.metric:
            raise ValueError("Evaluation metric differs from predicted metric")
        if candidate.scope.applies_to(record.context) != "match":
            raise ValueError("Validation context is outside scope or missing required attributes")
    assessment = assess_candidate(candidate, bundle)
    common = dict(candidate_id=candidate.candidate_id, active_version=baseline_version,
                  baseline_version=baseline_version, case_count=len(records),
                  record_origins=sorted({r.origin for r in records}), policy=policy,
                  evidence_digest=digest(bundle), candidate_digest=digest(candidate),
                  evaluation_digest=digest([r.model_dump(mode="json") for r in records]))
    if assessment.status == "rejected":
        return SelectionDecision(status="rejected", reasons=assessment.reasons, **common)
    if assessment.status == "needs_clarification":
        return SelectionDecision(status="deferred", reasons=assessment.reasons, **common)
    if len(records) < policy.min_cases:
        return SelectionDecision(status="deferred", reasons=["Insufficient validation cases"], **common)
    gain = mean(r.candidate_score - r.baseline_score for r in records)
    effort = mean(r.candidate_human_seconds - r.baseline_human_seconds for r in records)
    reasons = []
    if any(r.candidate_critical_errors > 0 for r in records):
        reasons.append("Candidate retains a critical error in validation")
    if any(r.candidate_score < r.baseline_score for r in records):
        reasons.append("Candidate regresses on an observed validation case")
    if gain < policy.min_mean_gain:
        reasons.append("Mean quality gain is below the declared threshold")
    if effort > policy.max_mean_effort_increase:
        reasons.append("Human effort exceeds the declared budget")
    common.update(mean_quality_gain=gain, mean_human_seconds_change=effort)
    if reasons:
        return SelectionDecision(status="rejected", reasons=reasons, **common)
    common["active_version"] = "context-" + digest({"baseline": baseline_version,
                                                    "candidate": candidate.model_dump(mode="json")})[:16]
    return SelectionDecision(status="accepted", reasons=["Paired validation records satisfy the declared policy"], **common)


def context_artifact(candidate: CandidateUpdate, decision: SelectionDecision) -> dict:
    """Export a context instruction after a matching selection; never deploy it."""
    if decision.status != "accepted" or decision.candidate_digest != digest(candidate):
        raise ValueError("A matching accepted decision is required")
    if not decision.record_origins or "fixture" in decision.record_origins:
        raise ValueError("Fixture evaluations cannot produce an exportable update")
    return {"schema_version": "0.1", "version": decision.active_version,
            "baseline_version": decision.baseline_version, "scope": candidate.scope.model_dump(),
            "instruction": candidate.patch, "decision": decision.model_dump(mode="json")}
