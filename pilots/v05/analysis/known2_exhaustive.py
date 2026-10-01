"""Exhaustive check: which diagnostic task types can one known-2 history carry?

Known-2 has four projected cells (two declared binary attributes) and the H14 class.
For every true function and every set of observed cells, list the task types that are
simultaneously available. Observed counts do not matter; only the observed cell set.
"""

import itertools

CELLS = range(4)  # bit 0: first declared attribute, bit 1: second


def table(pred):
    return sum(1 << c for c in CELLS if pred(c))


def lit(a, p):
    return table(lambda c: ((c >> a) & 1) == p)


H14 = {0, 15}
for a in (0, 1):
    for p in (0, 1):
        H14.add(lit(a, p))
for pa, pb in itertools.product((0, 1), repeat=2):
    H14.add(lit(0, pa) & lit(1, pb))
    H14.add(lit(0, pa) | lit(1, pb))
assert len(H14) == 14

combos = {}
for f in sorted(H14):
    for r in range(1, 5):
        for observed in itertools.combinations(CELLS, r):
            mask = sum(1 << c for c in observed)
            compatible = [g for g in H14 if (g ^ f) & mask == 0]
            kinds = set()
            for c in CELLS:
                values = {(g >> c) & 1 for g in compatible}
                seen = c in observed
                if len(values) == 2:
                    kinds.add('unidentifiable')
                elif values == {1}:
                    kinds.add('observed_change' if seen else 'transfer_change')
                else:
                    kinds.add('observed_retention' if seen else 'retention_transfer')
            combos.setdefault(frozenset(kinds), []).append((f, observed))

hard = {'transfer_change', 'retention_transfer', 'unidentifiable'}
print('Jointly available type sets (with an observed change):')
for kinds, examples in sorted(combos.items(), key=lambda kv: (-len(kv[0]), sorted(kv[0]))):
    if 'observed_change' in kinds:
        print(f'  {sorted(kinds)}  examples={len(examples)}  hard types={len(kinds & hard)}')
best = max(len(k & hard) for k in combos)
print('Maximum number of distinct hard types (transfer, retention transfer, unidentifiable) in one history:', best)
