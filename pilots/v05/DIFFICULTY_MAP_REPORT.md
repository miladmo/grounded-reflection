# Pilot v0.5 difficulty map: report on the main run

Status: **draft; attribution review part 1 incorporated, part 2 open.** Every number is from the sealed main run
`pilots/v05/runs/live-main-20261003` (seal
`dc4fc775af49df6c838c1cba29d730155319920298596791ecfffd08eb4ff4ab`), recomputed offline by
`pilots/v05/analysis/main_analysis.py`, which writes `pilots/v05/analysis/main-analysis.json`.
The analysis made no model calls. The results are descriptive: a synthetic stress test
with thin cells (two diagnostics per hard type, setting and arm), not a significance test.

## Run

* One model (DeepSeek-V4-Flash-0731 via FHGenie), reasoning high, a single run with no
  retries or replacement runs.
* 358 calls and 4,954,459 reported tokens, no unknown usage, no halt.
* Three isolated response failures were tolerated under the Amendment 5 rule:
  * Two C1 chunks returned `Scope.match` outside the agreed list format. C preparation was
    therefore unavailable for two U-L histories (`history-dd4c7199f572`,
    `history-f09764e24578`). Their 8 C tasks are counted as incorrect.
  * One B generation call failed in transport (K-L, observed change) and is counted as
    incorrect.
* Caveat on the environment: the main run and calibration ran under Python 3.12.14 with
  pydantic 2.13.5. The two D technical checks ran under 3.11.9 with pydantic 2.10.6.

## Primary outcome

Correct means the executed output fields equal the oracle's expected fields. Denominators
are fixed: blocked and failed calls count as incorrect.

| Arm | Observed change | Observed retention | Transfer | Unidentifiable | Control |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | 0/16 | 16/16 | 0/8 | 8/8 | 16/16 |
| B | 14/16 | 16/16 | 7/8 | 7/8 | 16/16 |
| C | 12/16 | 14/16 | 6/8 | 7/8 | 13/16 |
| D | 6/16 | 14/16 | 2/8 | 7/8 | 12/16 |

Diagnostics per setting (12 per arm: 8 observed and 4 hard), with controls separately:

| Setting | A | B | C | D | B observed / hard | C observed / hard | D observed / hard | Controls A, B, C, D |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| K-S | 6 | **12** | **12** | 7 | 8/8, 4/4 | 8/8, 4/4 | 5/8, 2/4 | 4, 4, 4, 2 |
| K-L | 6 | 10 | **11** | 7 | 6/8, 4/4 | 8/8, 3/4 | 5/8, 2/4 | 4, 4, 4, 3 |
| U-S | 6 | **12** | 10 | 9 | 8/8, 4/4 | 6/8, 4/4 | 6/8, 3/4 | 4, 4, 4, 3 |
| U-L | 6 | **10** | 6 | 6 | 8/8, 2/4 | 4/8, 2/4 | 4/8, 2/4 | 4, 4, 1, 4 |

**The keep floor.** An arm that never changes anything gets 6 of 12 diagnostics: the two
retentions plus, in the two histories with an unidentifiable hard task, the
unidentifiable task. A shows exactly this floor in every setting. D lies at or barely
above it: 7, 7, 9 and 6.

## Prespecified expectations

The better of B and C is taken over the 12 diagnostics of a setting. The attribution
column follows the attribution review by Milad Morad (part 1, 4 October 2026).

| | Comparison | Result | Holds? | Attribution |
| --- | --- | --- | --- | --- |
| E1 selection | K-L vs K-S | C 11 vs 12 | yes, by 1 | decided by C's missed transfer in `history-7b21f7009087`; under review (case file (a)) |
| E1 selection | U-L vs U-S | B 10 vs 12 | formally yes, by 2 | **not attributable in substance**: the comparison arm failed technically, and B failed with complete evidence |
| E2 dimension uncertainty | U-S vs K-S | 12 vs 12 (hard 4 vs 4) | no | — |
| E2 dimension uncertainty | U-L vs K-L | 10 vs 11 (hard 2 vs 4) | formally yes, by 1 | **not attributable in substance** for the same reason; the K-L side is C's missed transfer in `history-7b21f7009087` |
| E3 D accuracy | D minus better of B and C | K-S −5, K-L −4, U-S −3, U-L −4 | no, in all four settings | mixed, model and specification (see below) |
| E4 D cost | applies only where D is at least as accurate | D is less accurate everywhere | not applicable | — |

* **E1 and E2 in U-L.** B's two U-L failures fall in exactly the two histories in which C's
  preparation failed technically (`Scope.match` format): the unidentifiable task in
  `history-dd4c7199f572` and the transfer task in `history-f09764e24578`.
  * In both, B had all 12 binding approvals in context, so neither is a selection error.
  * In the other two U-L histories, C solved all 6 diagnostics.
  * Hence: formally met, but not attributable in substance (comparison arm technically
    failed; B's errors occurred with complete evidence).
* **E3 does not hold.** D is less accurate than the better of B and C in every setting,
  on both observed and hard diagnostics.
* For completeness, tokens per task over the four tasks of a history, including
  preparation:

  | Setting | A | B | C | D |
  | --- | ---: | ---: | ---: | ---: |
  | K-S | 3,320 | 13,990 | 16,710 | 16,442 |
  | K-L | 3,180 | 29,080 | 49,088 | 19,711 |
  | U-S | 3,057 | 16,437 | 16,262 | 25,181 |
  | U-L | 3,130 | 30,545 | 37,037 | 26,485 |

  D is cheaper than B and C in the large histories, but it is not accurate there.

## Why D falls short

**Attribution (Milad Morad, part 1): mixed, model and specification.** The shortfall lies
in proposing hypotheses, not in testing them. It goes back to a specification gap
recognised after the run. There is no repair and no follow-up run in v0.5. E3 remains
descriptively unmet.

* **Cause: D read a literal only as a test of the second listed value, never of the
  first.**
  * The public class text says "Each attribute defines a predicate testing its second
    listed value". It never states that a literal may also test the first value, which
    invites this misreading.
  * The round prompt offers no way to add hypotheses or to react to an empty register.
* **Literal values used.** 15 of 16 registers use only second-listed values; one uses both
  values of its two attributes.
* **Register size.**
  * In known-2, 7 of 8 registers hold exactly 6 functions: the negation-free subset of H14
    (2 constants, 2 literals, 1 conjunction, 1 disjunction).
  * In unknown-6, 6 of 8 hold exactly 38: 2 constants, 6 literals, 15 conjunctions and
    15 disjunctions.
  * Several D notes declare every hypothesis of the declared class refuted.
* **World function polarity against the register.** The type of the world function (which
  values its literals test) determines what appears:

  | World function uses | Histories | World function listed | Complement listed |
  | --- | ---: | ---: | ---: |
  | only second-listed values | 3 | 3 | 0 |
  | only first-listed values | 9 | 1 | 8 |
  | both (mixed) | 4 | 0 | 0 |

  * If the world function uses only first-listed values, its complement uses only
    second-listed values and therefore appears in the register. D then eliminates it
    correctly (8 histories).
  * With mixed polarity, neither appears (4 histories), and likewise in the one
    first-listed history whose register was truncated to 13 hypotheses.
  * This is **not** a baseline-polarity inversion as in v0.4.
* **Consequence.**
  * The register collapsed in 10 of 16 histories: every hypothesis was eliminated, D-final
    rejected every candidate, and generation kept the baseline. There D solved 15 of 30
    diagnostics and all 10 controls, which is exactly the keep pattern.
  * In 12 histories D listed none of the compatible functions.
* **Testing was sound.**
  * 825 of 938 records cited in the final registers are binding approvals.
  * D kept an incompatible function in only 2 histories and wrongly eliminated a
    compatible one in only 1.
  * Where D kept the world function (3 histories), it solved all 9 diagnostics.
* **Queries found the evidence.** In 11 of 16 histories D's queries returned all 12
  binding approvals, in the others at least 1. D stopped after 1 to 3 rounds, never after
  the maximum of 6.
* **D's control failures are a separate issue: scope.**
  * The register has no scope field, and D-final does not carry the registration scope
    (task family, workflow, version) into its rules. Only 1 of 9 rules D adopted names the
    workflow, against 20 of 22 for C.
  * Where D kept the world function, it therefore failed all 3 controls, and 4 of its 16
    controls in total.
* In line with the interpretation limits, D's shortfall cannot be attributed separately to
  the register or to the querying.

## B and C

* **Omission as a finding across pilots (small cells).** All five missed changes or
  transfers by B and C (B 2, C 3) fall in histories whose alternative is omission, as in
  v0.4. In histories with an added field, B and C solved every observed change and
  transfer that ran (11 of 12 each; the twelfth was a failed or blocked call).
* **Retrieval coverage of B in large histories.**
  * B's context contained 94.8 % of the binding approvals on average, and all of them in
    14 of 24 tasks.
  * B's missed observed change in K-L (`history-b785c97276f8`) had 9 of 12 in context.
  * Both U-L failures had 12 of 12.
* **Unidentifiable tasks.**
  * B decided "apply" once (U-L) and was otherwise correct with the "keep" label.
  * C reached "keep" in every completed case after its preparation had marked the context
    unresolved. Its one failure is a blocked task.
* **C controls.** C failed one completed control with an unsupported change (U-L); the
  other two C control failures are blocked tasks.

## Heuristic references on the main-run material (hard tasks)

| Hard type | Nearest neighbour | Always keep | Simplest compatible | Compatible majority | Misreadings (oracle reading) |
| --- | ---: | ---: | ---: | ---: | --- |
| Transfer (8) | 0/8 | 0/8 | 8/8 | 8/8 | 0/8 for every misreading |
| Unidentifiable (8) | 0/8 | 8/8 | 8/8 | 8/8 | 0/8, except `rejections_as_assent` 2/8 |

Nearest neighbour misleads on every hard task, as constructed. Always keep solves exactly
the unidentifiable tasks. Simplest compatible and compatible majority know the declared
class and the binding evidence, so they serve as references, not as shortcuts. Under
fallback (a), where undefined counts as keep, several misreadings solve the
unidentifiable tasks, which is the always-keep direction. This matches the r3 review
note.

## Open attribution cases (part 2)

Case files: `pilots/v05/review/attribution-20261004/CASES.md`, generated by
`pilots/v05/analysis/attribution_cases.py`.

1. **(a) C in `history-7b21f7009087`, transfer (decides E1 and E2 on the K-L side).** Did
   chunking lose evidence, or was it present?
2. **(b) B in `history-dd4c7199f572` (unidentifiable, "apply") and `history-f09764e24578`
   (transfer, "keep").** Outputs with declared rules and decision label.

## Interpretation limits

As registered:

* synthetic placeholder families and supplied approval semantics;
* the public H134 restriction, on which transfer depends;
* one model and one retrieval choice;
* D as one specific mechanism, not grounded reflection in general;
* 16 diagnostics per setting and arm.

Hard tasks are constructed so that similarity and naive readings mislead. Their accuracy
is a stress test, not an estimate of natural error rates. The four expectations rest on
differences of one to five diagnostics.
