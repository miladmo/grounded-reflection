"""Public finite task semantics and private, separately serialised cases."""

from typing import Any, Literal

from pydantic import Field, model_validator

from grounded_reflection.models import Contract
from reflectai_v03.contracts import History, HistoryTruth, Policy

Setting = Literal['S0', 'S1', 'S2', 'S3', 'S4', 'S5']
Family = Literal['hr', 'sales', 'retrieval', 'reporting']
Regime = Literal['change', 'resolved_keep', 'unidentifiable']
H14_DEFINITION = (
    'Each of the two declared binary context dimensions defines a predicate testing its second '
    'listed value. Call these predicates x and y. In each registered version the target field '
    'configuration is one Boolean function from the following class: constant 0 or 1; x, not x, '
    'y, or not y; a conjunction of one literal from each dimension; or a disjunction of one '
    'literal from each dimension. Zero selects the configured baseline and one the available '
    'alternative. The fourteen distinct truth tables exclude only XOR and XNOR. Each version '
    'has its own class member, with no cross-version coupling. This restriction is a supplied '
    'synthetic assumption, not an established property of enterprise work.'
)


class FieldOption(Contract):
    field: str
    operation: Literal['omit', 'set_literal', 'set_fact', 'append_fact']
    value: str = ''
    separator: str = ''


class PublicFrame(Contract):
    """The declared modelling vocabulary, not a requirement assignment."""

    task_family: str
    workflow: str
    as_of: str
    dimensions: dict[str, list[str]]
    field_option: FieldOption
    baseline_template: dict[str, str]
    fact_descriptions: dict[str, str]
    hypothesis_class: Literal['h14'] = 'h14'
    hypothesis_definition: Literal[H14_DEFINITION] = H14_DEFINITION

    @model_validator(mode='after')
    def bounded_dimensions(self):
        if len(self.dimensions) != 2 or any(len(set(v)) != 2 or len(v) != 2
                                           for v in self.dimensions.values()):
            raise ValueError('the registered finite class has two binary context dimensions')
        reserved = {'task_family', 'workflow', 'version'}
        if reserved.intersection(self.dimensions):
            raise ValueError('context dimensions cannot replace scope boundaries')
        return self


class FamilyConfig(Contract):
    """Optional replacements of the placeholder vocabulary, frozen before a run."""

    task_family: str | None = None
    dimensions: dict[str, list[str]] | None = None
    field: str | None = None
    field_option: FieldOption | None = None
    baseline_template: dict[str, str] | None = None
    fact_descriptions: dict[str, str] | None = None


class GeneratorConfig(Contract):
    families: dict[Family, FamilyConfig] = Field(default_factory=dict)


class OracleResult(Contract):
    policies: list[Policy]
    evidence_audit: dict[str, dict[str, Any]]
    constraints: list[dict[str, Any]]
    versions: dict[str, dict[str, Any]]
    current_version: str


class Case(Contract):
    """Evaluator material. Only history may enter a preparation payload."""

    case_id: str
    setting: Setting
    family: Family
    regime: Regime
    seed: int
    split: Literal['development', 'review', 'final_test', 'test_fixture']
    history: History
    truth: HistoryTruth
    diagnostic_context: dict[str, str]
    control_context: dict[str, str]
    oracle_audit: dict[str, dict[str, Any]]
    material_audit: dict[str, Any]
