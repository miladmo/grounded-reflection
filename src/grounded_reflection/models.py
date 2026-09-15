"""Typed contracts. Observations, hypotheses, updates and evaluations are distinct."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

Text = Annotated[str, StringConstraints(min_length=1, pattern=r"\S")]
Score = Annotated[float, Field(ge=0, le=1, allow_inf_nan=False)]
Nonnegative = Annotated[float, Field(ge=0, allow_inf_nan=False)]
Split = Literal["development", "validation", "final_test"]


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class Provenance(Contract):
    origin: Literal["synthetic", "human_observation", "model_generated"]
    source_id: Text
    recorded_at: datetime
    model: str | None = None

    @model_validator(mode="after")
    def check_origin(self):
        if self.recorded_at.tzinfo is None:
            raise ValueError("recorded_at must include a timezone")
        if self.origin == "model_generated" and not self.model:
            raise ValueError("model-generated evidence requires a model identifier")
        return self


class EvidenceItem(Contract):
    evidence_id: Text
    kind: Literal["source", "agent_output", "human_feedback", "human_revision", "tool_result"]
    text: Text
    provenance: Provenance


class WorkEpisode(Contract):
    episode_id: Text
    split: Split
    context: dict[Text, Text]
    task: Text
    evidence: list[EvidenceItem] = Field(min_length=1)
    missingness: list[Text] = Field(default_factory=list)

    @model_validator(mode="after")
    def unique_evidence(self):
        ids = [e.evidence_id for e in self.evidence]
        if len(set(ids)) != len(ids):
            raise ValueError("evidence IDs must be unique within an episode")
        return self


class EvidenceReference(Contract):
    episode_id: Text
    evidence_id: Text
    quote: Text


class Scope(Contract):
    """Explicit conjunction of allowed context values; omitted context is unknown."""

    match: dict[Text, list[Text]] = Field(min_length=1)

    @model_validator(mode="after")
    def nonempty_values(self):
        if any(not values or len(set(values)) != len(values) for values in self.match.values()):
            raise ValueError("scope values must be nonempty and unique")
        return self

    def applies_to(self, context: dict[str, str]) -> Literal["match", "mismatch", "unknown"]:
        if any(key in context and context[key] not in values for key, values in self.match.items()):
            return "mismatch"
        if any(key not in context for key in self.match):
            return "unknown"
        return "match"

    def is_within(self, outer: Scope) -> bool:
        return all(key in self.match and set(self.match[key]) <= set(values)
                   for key, values in outer.match.items())


class Hypothesis(Contract):
    hypothesis_id: Text
    claim: Text
    scope: Scope
    support: list[EvidenceReference] = Field(min_length=1)
    counterevidence: list[EvidenceReference] = Field(default_factory=list)
    alternatives: list[Text] = Field(default_factory=list)
    unresolved_questions: list[Text] = Field(default_factory=list)
    origin: Literal["curated_fixture", "human_authored", "model_generated"]


class ExpectedEffect(Contract):
    metric: Text
    prediction: Text


class CandidateUpdate(Contract):
    candidate_id: Text
    hypothesis_id: Text
    scope: Scope
    target: Literal["context"]
    patch: Text
    expected_effect: ExpectedEffect
    blocking_questions: list[Text] = Field(default_factory=list)


class EvidenceBundle(Contract):
    schema_version: Literal["0.1"] = "0.1"
    episodes: list[WorkEpisode] = Field(min_length=1)
    hypotheses: list[Hypothesis] = Field(min_length=1)
    candidates: list[CandidateUpdate] = Field(min_length=1)

    @model_validator(mode="after")
    def unique_ids(self):
        for field, key in [(self.episodes, "episode_id"), (self.hypotheses, "hypothesis_id"),
                           (self.candidates, "candidate_id")]:
            ids = [getattr(item, key) for item in field]
            if len(set(ids)) != len(ids):
                raise ValueError(f"duplicate {key}")
        known = {h.hypothesis_id for h in self.hypotheses}
        if any(c.hypothesis_id not in known for c in self.candidates):
            raise ValueError("candidate references an unknown hypothesis")
        return self


class SplitManifest(Contract):
    development: list[Text]
    validation: list[Text] = Field(min_length=1)
    final_test: list[Text]

    @model_validator(mode="after")
    def disjoint_splits(self):
        all_ids = self.development + self.validation + self.final_test
        if len(set(all_ids)) != len(all_ids):
            raise ValueError("case IDs must be unique across all splits")
        return self


class PairedEvaluation(Contract):
    case_id: Text
    split: Split
    baseline_version: Text
    candidate_id: Text
    candidate_digest: Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{64}$")]
    context: dict[Text, Text]
    metric: Literal["professional_quality"] = "professional_quality"
    baseline_score: Score
    candidate_score: Score
    baseline_critical_errors: Annotated[int, Field(ge=0)]
    candidate_critical_errors: Annotated[int, Field(ge=0)]
    baseline_human_seconds: Nonnegative
    candidate_human_seconds: Nonnegative
    origin: Literal["fixture", "human_rating", "programmatic_check", "model_judge"]
    evaluator: Text


class SelectionPolicy(Contract):
    min_cases: Annotated[int, Field(ge=1)] = 2
    min_mean_gain: Annotated[float, Field(gt=0, le=1, allow_inf_nan=False)] = 0.05
    max_mean_effort_increase: Nonnegative = 0


class CandidateAssessment(Contract):
    candidate_id: Text
    status: Literal["eligible_for_validation", "rejected", "needs_clarification"]
    reasons: list[str]
    verified_reference_count: int


class SelectionDecision(Contract):
    candidate_id: Text
    status: Literal["accepted", "rejected", "deferred"]
    active_version: Text
    baseline_version: Text
    reasons: list[str]
    case_count: int
    mean_quality_gain: float | None = None
    mean_human_seconds_change: float | None = None
    record_origins: list[str]
    evidence_digest: Text
    candidate_digest: Text
    evaluation_digest: Text
    policy: SelectionPolicy
    protocol_version: Literal["0.1"] = "0.1"
