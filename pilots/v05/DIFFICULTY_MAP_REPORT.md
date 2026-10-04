# Pilot v0.5 difficulty map: report on the main run

Status: **final, 4 October 2026; attribution review parts 1 and 2 by Milad Morad incorporated.** Every number is from the sealed main run
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
column follows the attribution review by Milad Morad (parts 1 and 2, 4 October 2026).

| | Comparison | Result | Holds formally? | Attribution |
| --- | --- | --- | --- | --- |
| E1 selection | K-L vs K-S | C 11 vs 12 | yes, by 1 | decided by C's missed transfer in `history-7b21f7009087`, which had complete evidence |
| E1 selection | U-L vs U-S | B 10 vs 12 | yes, by 2 | B's two failures had complete evidence; C failed technically in the same histories |
| E2 dimension uncertainty | U-S vs K-S | 12 vs 12 (hard 4 vs 4) | no | — |
| E2 dimension uncertainty | U-L vs K-L | 10 vs 11 (hard 2 vs 4) | yes, by 1 | B's failures are substantive and fit the E2 mechanism; the arm comparison stays open because C failed technically |
| E3 D accuracy | D minus better of B and C | K-S −5, K-L −4, U-S −3, U-L −4 | no, in all four settings | cause in proposing hypotheses; mixed, model and specification |
| E4 D cost | applies only where D is at least as accurate | D is less accurate everywhere | not applicable | — |

**Overall judgement.**

* **E1** is formally met in K and U but **not shown as a selection effect**: none of the
  decisive failures rests on missing evidence.
* **E2** is not met in U-S and formally met in U-L. Overall it is **partly consistent, not
  shown**.
* **E3** is not met.
* **E4** is not applicable.

Details:

* **E1 and E2 in U-L.** B's two U-L failures fall in exactly the two histories in which C's
  preparation failed technically (`Scope.match` format): the unidentifiable task in
  `history-dd4c7199f572` and the transfer task in `history-f09764e24578`.
  * In both, B had all 12 binding approvals in context, so neither is a selection error.
  * In the other two U-L histories, C solved all 6 diagnostics.
* **The stress design worked.** In U-S, B resisted the same traps (4 of 4 hard tasks).
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

## Attribution review part 2: the decisive B and C failures

Decision by Milad Morad, 4 October 2026. Case files:
`pilots/v05/review/attribution-20261004/CASES.md`, generated by
`pilots/v05/analysis/attribution_cases.py`. **In each of the three decisive failures the
binding evidence was completely in context.** The arms generalised wrongly. Their
decisions matched the nearest-neighbour heuristic at decision level; the declared reasons
differ.

| Case | Attribution | Label |
| --- | --- | --- |
| (a) C, `history-7b21f7009087`, transfer | substantive | missed transfer, class restriction not applied |
| (b1) B, `history-dd4c7199f572`, unidentifiable | substantive | unsupported change, rule over an irrelevant attribute |
| (b2) B, `history-f09764e24578`, transfer | substantive | missed change under omission, relevant attributes not recognised |
| C preparation failures in U-L | technical | `Scope.match` format |
| D registers | mixed, model and specification | see part 1 |

* **(a) C, transfer.**
  * Both neighbour cells of the transfer cell show the alternative four times each, and
    the diagonal shows the baseline four times. Under H14 the cell is identified.
  * C marked it unresolved throughout ("no binding approval there").
  * All binding approvals were present in the C1 chunks: the four chunks together saw all
    12. There was no selection error.
  * Generation received no instruction and kept the baseline.
* **(b1) B, unidentifiable.**
  * B declared `product_line=core`, in contradiction to the binding approval
    `record-e49afd3d3a66` in context (core, baseline).
  * 12 of 12 binding approvals were in context.
* **(b2) B, transfer.**
  * The relevant cell (`access=internal`, `collection=active`) is observed, with three
    approvals for the alternative.
  * The implication "`collection=active` → alternative" holds in every binding approval.
  * B declared no rule. 12 of 12 binding approvals were in context.

**Model or specification?** The check was whether the unclear class text could also have
affected B and C, that is, whether they too read a literal as a test of the second listed
value only.

* **The three cases.** Under that reading, no function of the class is consistent with
  the binding approvals in any of the three histories, so "keep" would be defensible.
* **The other transfer tasks.** In 6 of the 8 transfer tasks the reading
  likewise leaves no function.
  * B transferred correctly in 5 of them.
  * C transferred correctly in 4; of the other two, one is case (a) and 1
    is blocked.
  * So neither arm read the class systematically in this way.
* **Hence:** (a) and (b2) are substantive. A contribution of the class wording cannot be
  excluded but is unlikely. (b1) is substantive regardless of the reading, because the
  rule contradicts the evidence in context.

All 16 hard tasks under the second-value reading (in brackets: number of class functions
that fit the binding approvals under that reading), against the B and C results:

| Setting | Hard type | Direction | History | Required | Second-value reading | B | C |
| --- | --- | --- | --- | --- | --- | --- | --- |
| K-L | transfer | add | `history-e10528f0117b` | apply | apply (1) | correct | correct |
| K-L | transfer | omit | `history-7b21f7009087` | apply | no function fits (0) | correct | wrong |
| K-S | transfer | add | `history-548a79e9b9db` | apply | no function fits (0) | correct | correct |
| K-S | transfer | omit | `history-848082c39af3` | apply | no function fits (0) | correct | correct |
| U-L | transfer | add | `history-290afaaa1278` | apply | no function fits (0) | correct | correct |
| U-L | transfer | omit | `history-f09764e24578` | apply | no function fits (0) | wrong | blocked |
| U-S | transfer | add | `history-ab40cf721992` | apply | no function fits (0) | correct | correct |
| U-S | transfer | omit | `history-c3bafd0a1866` | apply | apply (2) | correct | correct |
| K-L | unidentifiable | add | `history-80aeea38c4d2` | keep | no function fits (0) | correct | correct |
| K-L | unidentifiable | omit | `history-b785c97276f8` | keep | no function fits (0) | correct | correct |
| K-S | unidentifiable | add | `history-35d5286e87c9` | keep | no function fits (0) | correct | correct |
| K-S | unidentifiable | omit | `history-c605640019bf` | keep | no function fits (0) | correct | correct |
| U-L | unidentifiable | add | `history-dd4c7199f572` | keep | no function fits (0) | wrong | blocked |
| U-L | unidentifiable | omit | `history-7eb081ccc622` | keep | no function fits (0) | correct | correct |
| U-S | unidentifiable | add | `history-f7d0ba014bba` | keep | no function fits (0) | correct | correct |
| U-S | unidentifiable | omit | `history-148cbff6972d` | keep | unresolved (2) | correct | correct |

## Interpretation limits

As registered:

* synthetic placeholder families and supplied approval semantics;
* the public H134 restriction, on which transfer depends;
* one model and one retrieval choice;
* D as one specific mechanism, not grounded reflection in general;
* 16 diagnostics per setting and arm;
* the public class text did not state that a literal may test either of the two values.
  D demonstrably misread it; for B and C its effect was at most limited, according to the
  data.

Hard tasks are constructed so that similarity and naive readings mislead. Their accuracy
is a stress test, not an estimate of natural error rates. The four expectations rest on
differences of one to five diagnostics.

## Implications (not tested)

1. Define the hypothesis space explicitly (a literal tests either of the two values; state
   the counts of 14 and 134), or let the harness enumerate it. The model then judges the
   evidence.
2. Give the round prompt a path for extending the register, and treat an empty register as
   a sign of an incomplete enumeration.
3. Carry the registration scope into adopted rules.
4. Study the omission asymmetry as a target in its own right.
