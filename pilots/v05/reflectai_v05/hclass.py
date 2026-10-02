"""Public rule classes over binary context attributes.

A cell is an integer whose bit i is 1 when attribute i takes its second listed
value. A requirement is a truth table over all cells (bit c set means the
alternative applies in cell c). The classes contain constants, single literals and
two-literal conjunctions and disjunctions over the declared candidate attributes;
XOR and XNOR are excluded. Over six candidates this is H134; over two it is H14.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass


@dataclass(frozen=True)
class Function:
    table: int
    form: str              # 'const', 'lit', 'and', 'or'
    literals: tuple        # ((attribute index, positive), ...)

    @property
    def complexity(self) -> int:
        return len(self.literals)

    @property
    def attributes(self) -> tuple:
        return tuple(sorted({attr for attr, _ in self.literals}))


def n_cells(n_attributes: int) -> int:
    return 1 << n_attributes


def bit(cell: int, attribute: int) -> int:
    return (cell >> attribute) & 1


def _table(n_attributes: int, predicate) -> int:
    return sum(1 << cell for cell in range(n_cells(n_attributes)) if predicate(cell))


def literal_table(n_attributes: int, attribute: int, positive: bool) -> int:
    want = 1 if positive else 0
    return _table(n_attributes, lambda cell: bit(cell, attribute) == want)


def rule_class(n_attributes: int, candidates) -> tuple[Function, ...]:
    """Distinct functions of at most two candidate attributes; first form wins on ties."""
    candidates = tuple(candidates)
    if len(set(candidates)) != len(candidates) or any(not 0 <= a < n_attributes for a in candidates):
        raise ValueError('candidate attributes must be distinct valid indices')
    full = (1 << n_cells(n_attributes)) - 1
    found: dict[int, Function] = {}

    def add(function: Function):
        found.setdefault(function.table, function)

    add(Function(0, 'const', ()))
    add(Function(full, 'const', ()))
    for attribute in candidates:
        for positive in (True, False):
            add(Function(literal_table(n_attributes, attribute, positive), 'lit', ((attribute, positive),)))
    for a, b in itertools.combinations(candidates, 2):
        for pa, pb in itertools.product((True, False), repeat=2):
            la, lb = literal_table(n_attributes, a, pa), literal_table(n_attributes, b, pb)
            add(Function(la & lb, 'and', ((a, pa), (b, pb))))
            add(Function(la | lb, 'or', ((a, pa), (b, pb))))
    return tuple(found[key] for key in sorted(found))


def value(function_or_table, cell: int) -> int:
    table = function_or_table.table if isinstance(function_or_table, Function) else function_or_table
    return (table >> cell) & 1


def compatible(klass, observations: dict[int, int]) -> list[Function]:
    """Functions agreeing with every observed cell -> bit."""
    return [f for f in klass if all(value(f, cell) == b for cell, b in observations.items())]


def status_at(functions, cell: int) -> str:
    values = {value(f, cell) for f in functions}
    if not values:
        raise ValueError('empty compatible set')
    if len(values) == 2:
        return 'unresolved'
    return 'apply' if values.pop() == 1 else 'keep'


def describe(function: Function, names, values=None) -> str:
    """Readable form; with values (per-attribute value pairs) the literal shows the real value."""
    if function.form == 'const':
        return 'always alternative' if function.table else 'always baseline'
    parts = [f"{names[a]}={values[a][1 if p else 0] if values else ('second' if p else 'first')}"
             for a, p in function.literals]
    if function.form == 'lit':
        return parts[0]
    return f" {function.form.upper()} ".join(parts)
