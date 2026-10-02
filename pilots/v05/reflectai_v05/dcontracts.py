"""Response contracts for arm D (hypothesis register and record queries).

All mappings are lists of name/value pairs, so the strict wire schema stays closed.
A hypothesis states its function structurally (form and literals) so the register
can be compared with the oracle's compatible set after the run.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from grounded_reflection.models import Contract, Text

MAX_QUERIES_PER_ROUND = 3
MAX_ROUNDS = 6


class LiteralSpec(Contract):
    attribute: Text
    value: Text            # the predicate is true when attribute equals this value


class Hypothesis(Contract):
    hypothesis_id: Text
    form: Literal['always_baseline', 'always_alternative', 'literal', 'and', 'or']
    literals: list[LiteralSpec] = Field(default_factory=list, max_length=2)
    status: Literal['open', 'eliminated', 'supported']
    evidence_ids: list[Text] = Field(default_factory=list)
    counterevidence_ids: list[Text] = Field(default_factory=list)
    note: str = ''


class AttributeValue(Contract):
    attribute: Text
    value: Text


class RecordQuery(Contract):
    query_id: Text
    attributes: list[AttributeValue] = Field(default_factory=list)
    event: Literal['any', 'register_version', 'review', 'preference', 'execution'] = 'any'
    decision: Literal['any', 'accept', 'reject'] = 'any'
    actor: str = ''
    reviewed_field: str = ''
    purpose: str = ''


class Register(Contract):
    hypotheses: list[Hypothesis] = Field(default_factory=list)
    queries: list[RecordQuery] = Field(default_factory=list, max_length=MAX_QUERIES_PER_ROUND)
    no_further_discrimination: bool = False
    notes: str = ''
