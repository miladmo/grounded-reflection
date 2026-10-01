"""Public model contracts and separate evaluator-only truth objects."""

from typing import Literal

from pydantic import Field, model_validator

from grounded_reflection.models import Contract, Scope, Text

Arm = Literal['A', 'B', 'C', 'D']


class OutputField(Contract):
    name: Text
    value: str


class Rule(Contract):
    field: Text
    operation: Literal['omit', 'set_literal', 'set_fact', 'append_fact']
    value: str = ''
    separator: str = ''
    scope: Scope

    @model_validator(mode='after')
    def valid_operation(self):
        if self.operation in ('set_fact', 'append_fact') and not self.value.strip():
            raise ValueError('fact operations require a fact key')
        if self.operation == 'omit' and (self.value or self.separator):
            raise ValueError('omit has neither a value nor a separator')
        if self.operation != 'append_fact' and self.separator:
            raise ValueError('only append_fact has a separator')
        return self


class Candidate(Contract):
    candidate_id: Text
    claim: Text
    status: Literal['adopt', 'reject', 'unresolved']
    rule: Rule
    evidence_ids: list[Text] = Field(default_factory=list)
    counterevidence_ids: list[Text] = Field(default_factory=list)
    alternatives: list[Text] = Field(default_factory=list)
    evidence_gap: str = ''


class Preparation(Contract):
    candidates: list[Candidate] = Field(default_factory=list)
    notes: str = ''

    @model_validator(mode='after')
    def unique_ids(self):
        ids = [candidate.candidate_id for candidate in self.candidates]
        if len(ids) != len(set(ids)):
            raise ValueError('duplicate candidate ID')
        return self


class ProvisionalCandidate(Candidate):
    """Uncommitted by procedure, not a verdict that the evidence is ambiguous."""

    status: Literal['unresolved'] = 'unresolved'


class ReflectionDraft(Contract):
    candidates: list[ProvisionalCandidate] = Field(default_factory=list)
    notes: str = ''

    @model_validator(mode='after')
    def unique_ids(self):
        ids = [candidate.candidate_id for candidate in self.candidates]
        if len(ids) != len(set(ids)):
            raise ValueError('duplicate candidate ID')
        return self


class Record(Contract):
    record_id: Text
    timestamp: Text
    kind: Literal['revision', 'review', 'tool', 'retrieval', 'template']
    actor: Text
    context: dict[Text, Text]
    observation: Text


class History(Contract):
    history_id: Text
    initial_configuration: Text
    assumptions: Text
    field_dictionary: dict[Text, Text]
    records: list[Record] = Field(min_length=1)

    @model_validator(mode='after')
    def unique_ids(self):
        ids = [record.record_id for record in self.records]
        if len(ids) != len(set(ids)):
            raise ValueError('duplicate record ID')
        return self


class Task(Contract):
    task_id: Text
    context: dict[Text, Text]
    facts: dict[Text, str]
    baseline_fields: list[OutputField]
    request: Text

    @model_validator(mode='after')
    def unique_fields(self):
        names = [field.name for field in self.baseline_fields]
        if len(names) != len(set(names)):
            raise ValueError('duplicate baseline field')
        return self


class WorkOutput(Contract):
    task_id: Text
    decision: Literal['apply', 'keep']
    applied_rules: list[Rule] = Field(default_factory=list)
    fields: list[OutputField] = Field(default_factory=list)
    completed: bool = True
    questions: list[Text] = Field(default_factory=list)

    @model_validator(mode='after')
    def unique_fields(self):
        names = [field.name for field in self.fields]
        if len(names) != len(set(names)):
            raise ValueError('duplicate output field')
        return self


class Policy(Contract):
    policy_id: Text
    rules: list[Rule] = Field(default_factory=list)


class CandidateTarget(Contract):
    target_id: Text
    status: Literal['adopt', 'reject', 'unresolved']
    rule: Rule


class HistoryTruth(Contract):
    """Never serialise this object into a model prompt."""

    history_id: Text
    scenario_id: Text
    pair_id: Text
    world_policy: Policy
    admissible_policies: list[Policy] = Field(min_length=1)
    candidate_targets: list[CandidateTarget]
    scope_probes: list[Task]


class TaskTruth(Contract):
    """Membership and obligations are evaluator-only, not agent instructions."""

    task_id: Text
    history_id: Text
    probe: Literal['diagnostic', 'control']
    expected_decision: Literal['apply', 'keep']
    recoverable: bool
    world_fields: list[OutputField]


class Dataset(Contract):
    split: Literal['development', 'final_test', 'test_fixture']
    seed: int
    histories: list[History]
    truths: list[HistoryTruth]
    tasks: list[Task] = Field(default_factory=list)
    task_truths: list[TaskTruth] = Field(default_factory=list)
    assignments: dict[str, str] = Field(default_factory=dict)


class BackendConfig(Contract):
    backend: Literal['mock', 'codex'] = 'mock'
    model: Text = 'offline-mock'
    reasoning_effort: Literal['low', 'medium', 'high'] = 'medium'
    timeout_seconds: int = Field(default=300, ge=1)
    max_calls: int = Field(default=288, ge=1)
    max_reported_tokens: int = Field(default=5000000, ge=1)


class RunConfig(Contract):
    protocol: Literal['pilot-v0.3'] = 'pilot-v0.3'
    phase: Literal['offline', 'calibration', 'main'] = 'offline'
    repetitions: int = Field(default=3, ge=1, le=3)
    seed: int = 3301
    order_seed: int = 3302
    backend: BackendConfig = Field(default_factory=BackendConfig)

    @model_validator(mode='after')
    def planned_repetitions(self):
        if self.phase == 'calibration' and self.repetitions != 1:
            raise ValueError('calibration uses exactly one repetition')
        if self.phase == 'main' and self.repetitions != 3:
            raise ValueError('main uses exactly three repetitions')
        if self.phase == 'offline' and self.backend.backend != 'mock':
            raise ValueError('offline phase requires the mock backend')
        if self.phase != 'offline' and self.backend.backend == 'mock':
            raise ValueError('mock runs cannot be scientific calibration or main runs')
        return self
