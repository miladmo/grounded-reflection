# v0.5 constructibility check (protocol step 2)

1 October 2026. Offline only: no model calls and no study material generated. Scripts:
[constructibility.py](constructibility.py) (unknown-6, randomised designs, 1,000 trials per
row) and [known2_exhaustive.py](known2_exhaustive.py) (known-2, every function and every
observed-cell set).

## unknown-6 (U-S and U-L): constructible

The H134 enumeration contains 134 distinct functions, as specified. With binding
approvals at random cells, where one non-relevant attribute copies a relevant one in
every approval, the share of designs that carry all four task types in one history is:

| Binding approvals | All four types | Unidentifiable via confusable attribute | Median compatible functions |
| ---: | ---: | ---: | ---: |
| 8 | 0.71 | 1.00 | 4 |
| 10 | 0.83 | 1.00 | 3 |
| 12 | 0.90 | 1.00 | 2 |
| 16 | 0.97 | 1.00 | 2 |

The proposed 12 approvals in a 24-record history are sufficient. Distractors are
non-binding and do not change the compatible set. A generator can choose a design
deterministically within the slot's seeded stream. This is construction, not a seed
redraw. With 12 approvals the remaining ambiguity is typically only the confusable pair.

## known-2 (K-S and K-L): all four types per history are impossible

Known-2 has four projected cells under H14. Exhaustive enumeration shows that one
history can carry at most **one** of the three hard types: transfer change, retention
with transfer, or unidentifiable. Each is available together with an observed change and
an observed retention:

| Jointly available in one history | Function/observation combinations |
| --- | ---: |
| observed change, observed retention, transfer change | 4 |
| observed change, observed retention, retention with transfer | 4 |
| observed change, observed retention, unidentifiable | 72 |

This follows from the four cells: identifying an unobserved cell needs three observed
cells, which leaves no further unobserved cell. v0.4 avoided the problem by giving each
history a single task type. The approved v0.5 design ("each history has one diagnostic
of each of the four types") therefore cannot be built for K-S and K-L.

## Proposed prespecified adjustment, for approval before any material is generated

Use the same task structure in **all four settings**, so that known-2 and unknown-6
remain comparable (E2):

* Each history has three diagnostics: observed change, observed retention, and **one
  hard task**. A fourth task is the control.
* The hard task rotates within each setting: **two histories with transfer change and
  two with unidentifiable**. Retention with transfer is dropped, because v0.4 found it
  easy for every arm (6/6). The direction of the alternative is balanced within each
  hard type (one add or set, one omit).
* Per setting and arm: 12 diagnostics (4 observed change, 4 observed retention, 2
  transfer change, 2 unidentifiable) and 4 controls. In total 48 diagnostics and 16
  controls per arm.
* Calibration (two histories per setting) gives 6 diagnostics per setting. The headroom
  criterion becomes **at most 4 of 6** correct for the better of B and C (67 %; the
  approved 6 of 8 is 75 %). E3 stays at "at least two more of 12".
* Amortisation is measured over the four tasks of a history. The generation reserve
  becomes four calls (227,072 tokens). Estimates drop slightly: about 6.9 M tokens and
  about 450 calls in the main run, about 2.0 M tokens and about 130 calls in
  calibration. The approved stops remain.

Alternatives that were rejected:

* *Keep four types per history only in unknown-6.* K and U would then differ in task
  mix, which confounds E2.
* *Six histories per setting, to restore 16 diagnostics.* This adds about 50 % cost and
  time and would endanger the schedule.
* *Three declared attributes in the known condition.* This changes the approved factor
  and adds its own relevance uncertainty.

With only two transfer and two unidentifiable diagnostics per setting, conclusions about
these hard types remain thin. The report must state this explicitly.
