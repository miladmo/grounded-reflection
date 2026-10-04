"""Offline constructibility check for pilot v0.5 (protocol step 2).

No model calls and no study material. Enumerates the public rule classes over six
binary attributes and asks, for a given number of binding approvals, how often one
history supports all four diagnostic task types at once:

* observed change: an observed cell where every compatible function gives 1;
* transfer change: an unobserved cell where every compatible function gives 1;
* resolved retention: a cell where every compatible function gives 0
  (reported separately for unobserved cells);
* unidentifiable: an unobserved cell where compatible functions disagree. In
  unknown-6 it must arise from a confusable attribute, i.e. the cell separates the
  relevant attribute from an attribute that covaries with it in every approval.

Usage: python constructibility.py [trials]
"""

import itertools
import json
import random
import sys

N_ATTR = 6
CELLS = list(range(1 << N_ATTR))
FULL = (1 << len(CELLS)) - 1


def bit(cell, attr):
    return (cell >> attr) & 1


def table(predicate):
    value = 0
    for cell in CELLS:
        if predicate(cell):
            value |= 1 << cell
    return value


def literal(attr, positive):
    return table(lambda c: bit(c, attr) == (1 if positive else 0))


def rule_class(attrs):
    """Constants, literals and two-literal AND/OR over the given attributes (no XOR)."""
    tables = {0: ('const', 0), FULL: ('const', 1)}
    for a in attrs:
        for p in (True, False):
            tables.setdefault(literal(a, p), ('lit', a, p))
    for a, b in itertools.combinations(attrs, 2):
        for pa, pb in itertools.product((True, False), repeat=2):
            la, lb = literal(a, pa), literal(b, pb)
            tables.setdefault(la & lb, ('and', a, pa, b, pb))
            tables.setdefault(la | lb, ('or', a, pa, b, pb))
    return tables


H134 = rule_class(range(N_ATTR))
H14 = rule_class((0, 1))
assert len(H134) == 134 and len(H14) == 14, (len(H134), len(H14))


def classify(true_fn, observed, klass):
    mask = 0
    for cell in observed:
        mask |= 1 << cell
    compatible = [g for g in klass if (g ^ true_fn) & mask == 0]
    kinds = {}
    for cell in CELLS:
        values = {(g >> cell) & 1 for g in compatible}
        seen = bool((mask >> cell) & 1)
        kinds[cell] = (seen, 'mixed' if len(values) == 2 else values.pop())
    return compatible, kinds


def trial(rng, n_approvals, condition):
    # True function: two relevant attributes, AND or OR with random polarities.
    if condition == 'known-2':
        relevant = (0, 1)
        klass = H14
    else:
        relevant = tuple(sorted(rng.sample(range(N_ATTR), 2)))
        klass = H134
    a, b = relevant
    pa, pb = rng.random() < 0.5, rng.random() < 0.5
    la, lb = literal(a, pa), literal(b, pb)
    true_fn = (la & lb) if rng.random() < 0.5 else (la | lb)
    confusable = None
    if condition == 'unknown-6':
        confusable = rng.choice([x for x in range(N_ATTR) if x not in relevant])
        anchor = rng.choice(relevant)
    observed = []
    for _ in range(n_approvals):
        cell = rng.randrange(len(CELLS))
        if confusable is not None:  # the confusable attribute copies the anchor in every approval
            cell = (cell & ~(1 << confusable)) | (bit(cell, anchor) << confusable)
        observed.append(cell)
    compatible, kinds = classify(true_fn, observed, klass)
    unseen = [c for c, (s, v) in kinds.items() if not s]
    found = {
        'observed_change': any(s and v == 1 for s, v in kinds.values()),
        'transfer_change': any(kinds[c][1] == 1 for c in unseen),
        'retention_unobserved': any(kinds[c][1] == 0 for c in unseen),
        'retention_any': any(v == 0 for s, v in kinds.values()),
    }
    mixed = [c for c in unseen if kinds[c][1] == 'mixed']
    if confusable is None:
        found['unidentifiable'] = bool(mixed)
    else:
        found['unidentifiable'] = any(bit(c, confusable) != bit(c, anchor) for c in mixed)
    found['all_four'] = all(found[k] for k in ('observed_change', 'transfer_change',
                                               'retention_unobserved', 'unidentifiable'))
    found['all_four_retention_any'] = all(found[k] for k in ('observed_change', 'transfer_change',
                                                             'retention_any', 'unidentifiable'))
    return found, len(compatible)


def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    rng = random.Random(45000)
    report = {}
    # known-2 has only four projected cells; see known2_exhaustive.py. Counting the
    # 64 raw cells here would treat irrelevant-attribute variants as unobserved.
    for condition in ('unknown-6',):
        for n in (6, 8, 10, 12, 16, 20):
            counts, sizes = {}, []
            for _ in range(trials):
                found, size = trial(rng, n, condition)
                sizes.append(size)
                for k, v in found.items():
                    counts[k] = counts.get(k, 0) + v
            report[f'{condition} approvals={n}'] = {
                **{k: round(v / trials, 3) for k, v in counts.items()},
                'median_compatible': sorted(sizes)[len(sizes) // 2]}
    print(json.dumps(report, indent=1))


if __name__ == '__main__':
    main()
