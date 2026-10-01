"""Small pilot contracts. Public model inputs never contain evaluator truth."""

from typing import Literal

from pydantic import Field, model_validator

from ..models import Contract, Hypothesis, Scope, Text, WorkEpisode

Family = Literal['recruiting', 'sales', 'research']
Arm = Literal['no_adaptation', 'direct_evidence', 'direct_adaptation', 'grounded_reflection']
ARMS = ('no_adaptation', 'direct_evidence', 'direct_adaptation', 'grounded_reflection')
PilotSplit = Literal['calibration', 'validation', 'final_test']


class Rule(Contract):
    field: Text
    operator: Literal['equals', 'contains', 'excludes'] = 'equals'
    value: Text
    scope: Scope | None = None


class RequirementPrediction(Contract):
    rule: Rule
    decision: Literal['adopt', 'clarify', 'defer']
    missing_fields: list[Text] = Field(default_factory=list)
    hypothesis: Hypothesis | None = None


class Preparation(Contract):
    requirements: list[RequirementPrediction] = Field(default_factory=list)
    notes: str = ''


class OutputField(Contract):
    name: Text
    value: str


class WorkOutput(Contract):
    case_id: Text
    action: Literal['deliver', 'clarify', 'defer']
    missing_fields: list[Text] = Field(default_factory=list)
    fields: list[OutputField] = Field(default_factory=list)

    @model_validator(mode='after')
    def unique_fields(self):
        names = [f.name for f in self.fields]
        if len(names) != len(set(names)):
            raise ValueError('output field names must be unique')
        return self


class Task(Contract):
    case_id: Text
    family: Family
    split: PilotSplit
    context: dict[str, str]
    request: Text
    facts: dict[str, str]
    output_fields: list[Text]

    def public_payload(self) -> dict:
        return self.model_dump(exclude={'split'})


class TaskTruth(Contract):
    case_id: Text
    family: Family
    category: Literal['transfer', 'boundary', 'override', 'ambiguous']
    checks: list[Rule]
    check_kinds: list[Literal['hidden', 'explicit', 'generic']]
    allowed_actions: list[Literal['deliver', 'clarify', 'defer']]
    missing_fields: list[str] = Field(default_factory=list)
    unresolved_output_fields: list[str] = Field(default_factory=list)
    distractors: list[Rule] = Field(default_factory=list)

    @model_validator(mode='after')
    def parallel_checks(self):
        if len(self.checks) != len(self.check_kinds) or not self.checks:
            raise ValueError('nonempty checks require a matching kind for each rule')
        if not self.allowed_actions:
            raise ValueError('allowed_actions cannot be empty')
        return self


class FamilyTruth(Contract):
    family: Family
    recoverable: list[Rule]
    unidentifiable: list[Rule] = Field(default_factory=list)
    distractors: list[Rule] = Field(default_factory=list)
    supported_exceptions: list[Rule] = Field(default_factory=list)
    scope_probes: list[dict[str, str]]


class History(Contract):
    family: Family
    episodes: list[WorkEpisode]

    @model_validator(mode='after')
    def development_only(self):
        if not self.episodes or any(e.split != 'development' for e in self.episodes):
            raise ValueError('history must contain development episodes only')
        if len({e.episode_id for e in self.episodes}) != len(self.episodes):
            raise ValueError('duplicate history episode ID')
        return self


class BackendConfig(Contract):
    backend: Literal['mock', 'codex'] = 'mock'
    model: str = 'offline-mock'
    reasoning_effort: str = 'medium'
    timeout_seconds: int = Field(default=300, gt=0)
    max_calls: int = Field(default=220, ge=1)
    max_reported_tokens: int = Field(default=1000000, ge=1)

    @model_validator(mode='after')
    def explicit_live_model(self):
        if self.backend != 'mock' and (not self.model.strip() or self.model == 'offline-mock'):
            raise ValueError('a live backend requires an explicit model')
        return self


class RunConfig(Contract):
    protocol: Literal['pilot-v0.2'] = 'pilot-v0.2'
    backend: BackendConfig = Field(default_factory=BackendConfig)
    repetitions: int = Field(default=2, ge=1, le=5)
    order_seed: int = 20260928
    human_sample_seed: int = 43


class Usage(Contract):
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    cached_input_tokens: int | None = Field(default=None, ge=0)
    reasoning_output_tokens: int | None = Field(default=None, ge=0)


class CallRecord(Contract):
    call_id: Text
    arm: Arm
    phase: Literal['calibration', 'prepare', 'validation', 'final_test']
    family: Family
    repetition: int = Field(ge=0)
    status: Literal['completed', 'failed']
    origin: Literal['offline_mock', 'model_generated']
    usage: Usage = Field(default_factory=Usage)
    response: dict | None = None
    error: str | None = None
