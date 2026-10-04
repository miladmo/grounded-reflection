"""Public v0.5 task semantics and private, separately serialised cases."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import model_validator

from grounded_reflection.models import Contract
from reflectai_v03.contracts import History, Task

Setting = Literal['K-S', 'K-L', 'U-S', 'U-L']
Family = Literal['hr', 'sales', 'retrieval', 'reporting']
HardType = Literal['transfer_change', 'unidentifiable']
TaskType = Literal['observed_change', 'observed_retention', 'transfer_change', 'unidentifiable', 'control']

CLASS_DEFINITIONS = {
    'h14-declared': (
        'Six binary context attributes are recorded for every work item. Only the two attributes '
        'listed in candidate_attributes can determine the target field configuration; the other '
        'attributes do not affect it. Each attribute defines a predicate testing its second listed '
        'value. The configuration is one Boolean function from the following class over the candidate '
        'attributes: constant 0 or 1; a single literal; a conjunction of one literal from each of two '
        'distinct candidate attributes; or a disjunction of one literal from each of two distinct '
        'candidate attributes. XOR and XNOR are excluded. Zero selects the configured baseline and one '
        'the available alternative. This restriction is a supplied synthetic assumption.'),
    'h134': (
        'Six binary context attributes are recorded for every work item. Which of them determine the '
        'target field configuration is not known; at most two do. Each attribute defines a predicate '
        'testing its second listed value. The configuration is one Boolean function from the following '
        'class over the attributes listed in candidate_attributes: constant 0 or 1; a single literal; a '
        'conjunction of one literal from each of two distinct attributes; or a disjunction of one literal '
        'from each of two distinct attributes. XOR and XNOR are excluded. Zero selects the configured '
        'baseline and one the available alternative. This restriction is a supplied synthetic assumption.'),
}


class FieldOption(Contract):
    field: str
    operation: Literal['omit', 'set_literal', 'set_fact', 'append_fact']
    value: str = ''
    separator: str = ''


class PublicFrame(Contract):
    """The declared modelling vocabulary; no requirement assignment."""

    task_family: str
    workflow: str
    version: str
    as_of: str
    attributes: dict[str, list[str]]
    candidate_attributes: list[str]
    field_option: FieldOption
    baseline_template: dict[str, str]
    fact_descriptions: dict[str, str]
    hypothesis_class: Literal['h14-declared', 'h134']
    hypothesis_definition: str

    @model_validator(mode='after')
    def declared_class(self):
        if len(self.attributes) != 6 or any(len(v) != 2 or len(set(v)) != 2 for v in self.attributes.values()):
            raise ValueError('v0.5 uses six binary context attributes')
        if {'task_family', 'workflow', 'version'} & set(self.attributes):
            raise ValueError('context attributes cannot replace scope boundaries')
        if not set(self.candidate_attributes) <= set(self.attributes):
            raise ValueError('candidate attributes must be declared attributes')
        expected = 2 if self.hypothesis_class == 'h14-declared' else 6
        if len(self.candidate_attributes) != expected or len(set(self.candidate_attributes)) != expected:
            raise ValueError('candidate attribute count does not match the declared class')
        if self.hypothesis_definition != CLASS_DEFINITIONS[self.hypothesis_class]:
            raise ValueError('the full public class definition must be present')
        return self

    @property
    def attribute_names(self) -> list[str]:
        return list(self.attributes)

    def cell_of(self, context: dict[str, str]) -> int:
        cell = 0
        for index, (name, values) in enumerate(self.attributes.items()):
            if context.get(name) not in values:
                raise KeyError(name)
            cell |= values.index(context[name]) << index
        return cell

    def context_of(self, cell: int) -> dict[str, str]:
        context = {'task_family': self.task_family, 'workflow': self.workflow, 'version': self.version}
        for index, (name, values) in enumerate(self.attributes.items()):
            context[name] = values[(cell >> index) & 1]
        return context

    def candidate_indices(self) -> list[int]:
        names = self.attribute_names
        return [names.index(name) for name in self.candidate_attributes]


class TaskTruth(Contract):
    task_id: str
    history_id: str
    task_type: TaskType
    cell: int | None
    expected_decision: Literal['apply', 'keep']
    oracle_status: Literal['apply', 'keep', 'unresolved', 'out_of_scope']
    expected_fields: dict[str, str]
    world_fields: dict[str, str]


class Case(Contract):
    """Evaluator material. Only history may enter a preparation payload."""

    case_id: str
    setting: Setting
    family: Family
    hard_type: HardType
    direction: Literal['omit', 'add']
    seed: int
    split: Literal['development', 'review', 'final_test', 'test_fixture']
    history: History
    world: dict[str, Any]
    task_cells: dict[str, int]
    oracle_audit: dict[str, Any]
    material_audit: dict[str, Any]


__all__ = ['CLASS_DEFINITIONS', 'Case', 'FieldOption', 'PublicFrame', 'Task', 'TaskTruth']
