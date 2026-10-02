"""Evaluator-side reference heuristics for hard tasks (material review r2).

None of these functions is available to any arm. They define what a shallow
procedure would answer, so the generator can require that the warranted action is
not reachable by such a shortcut, and the report can show the reference lines.

Decisions are 'apply', 'keep' or 'undefined' (contradictory reading).
"""

from __future__ import annotations

import json
from collections import Counter

from reflectai_v03.contracts import History

from . import hclass
from .oracle import configuration_bit, infer, read_frame


def _decision(functions, cell) -> str:
    if not functions:
        return 'undefined'
    return 'apply' if hclass.status_at(functions, cell) == 'apply' else 'keep'


def nearest_neighbour(observations: list[tuple[int, int]], cell: int) -> str:
    """Configuration of the binding approval(s) with minimal Hamming distance over all
    attributes; majority on ties, 'keep' on a tied vote."""
    if not observations:
        return 'keep'
    distance = lambda other: bin(other ^ cell).count('1')
    best = min(distance(c) for c, _ in observations)
    votes = Counter(bit for c, bit in observations if distance(c) == best)
    if votes[1] > votes[0]:
        return 'apply'
    return 'keep'


def compatible_majority(functions, cell) -> str:
    share = sum(hclass.value(f, cell) for f in functions) / len(functions)
    return 'apply' if share > 0.5 else 'keep'


def simplest_compatible(functions, cell) -> str:
    minimum = min(f.complexity for f in functions)
    simplest = [f for f in functions if f.complexity == minimum]
    return _decision(simplest, cell)


def _observations_with(history: History, extra) -> dict | None:
    """Binding observations plus extra (cell, bit) pairs; None if contradictory."""
    oracle = infer(history)
    observed = dict(oracle.observations)
    for cell, bit in extra:
        if observed.get(cell, bit) != bit:
            return None
        observed[cell] = bit
    return observed


def misreading_records(history: History) -> dict[str, list[tuple[int, int]]]:
    """Public records a misreading would wrongly promote, as (cell, bit) pairs."""
    frame = read_frame(history)
    binding = set(infer(history).binding_records)
    readings = {'all_accepted_reviews': [], 'inverted_rejections': [], 'followed_preferences': []}
    for record in history.records:
        if record.record_id in binding:
            continue
        event = json.loads(record.observation)
        try:
            cell = frame.cell_of(record.context)
        except KeyError:
            continue
        try:
            if event.get('event') == 'review' and event.get('decision') == 'accept':
                readings['all_accepted_reviews'].append((cell, configuration_bit(frame, event['accepted_fields'],
                                                                                  event['facts'])))
            elif event.get('event') == 'review' and event.get('decision') == 'reject':
                bit = configuration_bit(frame, event['rejected_fields'], event['facts'])
                readings['inverted_rejections'].append((cell, 1 - bit))
            elif event.get('event') == 'preference':
                readings['followed_preferences'].append((cell, configuration_bit(frame, event['proposed_fields'],
                                                                                 event['facts'])))
        except (KeyError, ValueError):
            continue
    return readings


def misreading_decisions(history: History, cell: int) -> dict[str, str]:
    frame = read_frame(history)
    klass = hclass.rule_class(len(frame.attributes), frame.candidate_indices())
    result = {}
    for name, extra in misreading_records(history).items():
        observed = _observations_with(history, extra)
        result[name] = 'undefined' if observed is None else _decision(hclass.compatible(klass, observed), cell)
    return result


def all_references(history: History, cell: int) -> dict[str, str]:
    oracle = infer(history)
    observations = [(c, b) for c, b in _binding_pairs(history)]
    return {'nearest_neighbour': nearest_neighbour(observations, cell),
            'compatible_majority': compatible_majority(oracle.compatible, cell),
            'simplest_compatible': simplest_compatible(oracle.compatible, cell),
            'always_keep': 'keep', **misreading_decisions(history, cell)}


def _binding_pairs(history: History) -> list[tuple[int, int]]:
    """Every binding approval as (cell, bit), repetitions included."""
    frame = read_frame(history)
    records = {r.record_id: r for r in history.records}
    pairs = []
    for record_id in infer(history).binding_records:
        record = records[record_id]
        event = json.loads(record.observation)
        pairs.append((frame.cell_of(record.context), configuration_bit(frame, event['accepted_fields'], event['facts'])))
    return pairs
