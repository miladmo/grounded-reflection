# Pilot v0.5 difficulty map: report on the main run

Status: **draft for the attribution review.** Every number is from the sealed main run
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

The better of B and C is taken over the 12 diagnostics of a setting.

| | Comparison | Result | Holds? |
| --- | --- | --- | --- |
| E1 selection | K-L vs K-S | 11 vs 12 | yes, by 1 |
| E1 selection | U-L vs U-S | 10 vs 12 | yes, by 2 |
| E2 dimension uncertainty | U-S vs K-S | 12 vs 12 (hard 4 vs 4) | no |
| E2 dimension uncertainty | U-L vs K-L | 10 vs 11 (hard 2 vs 4) | yes, by 1, on hard tasks |
| E3 D accuracy | D minus better of B and C | K-S −5, K-L −4, U-S −3, U-L −4 | no, in all four settings |
| E4 D cost | applies only where D is at least as accurate | D is less accurate everywhere | not applicable |

* **E1 and E2 hold only by one or two diagnostics.** In U-L, B's two failures fall in the
  same two histories in which C's preparation failed (unidentifiable in
  `history-dd4c7199f572`, transfer in `history-f09764e24578`). The U-L result therefore
  rests on two histories.
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

## Why D falls short (for attribution review)

D's register is evaluated against the oracle's compatible set. Each D hypothesis is
mapped to its truth table, with a literal true when the attribute has the stated value.

* **The register collapsed in 10 of 16 histories.** Every listed hypothesis was
  eliminated. D-final then rejected every candidate, so generation kept the baseline. In
  these histories D solved 15 of 30 diagnostics and all 10 controls, which is exactly the
  keep pattern.
* **The world function was missing from the register.** It was listed in only 4 of 16
  histories and kept in 3. In 12 histories D listed none of the compatible functions. Its
  eliminations were almost always consistent with the evidence: it kept an incompatible
  function in only 2 histories and wrongly eliminated a compatible one in only 1. **The
  failure lies in proposing hypotheses, not in testing them.**
* **The complement of the world function appears often.** In 8 histories D listed the
  function with the opposite polarity (the alternative where the world function selects
  the baseline) and then correctly eliminated it. In known-2, D listed only 6 of the 14
  functions of H14.
  * This pattern resembles the baseline-polarity inversion from v0.4. An attribution needs
    the review and is **unverified**. A plain incomplete enumeration would explain the
    data as well.
* **Where D kept the world function** (3 histories), it solved all 9 diagnostics but none
  of the 3 controls: the adopted rules reached beyond the declared workflow.
* **Queries found the evidence.** In 11 of 16 histories D's queries returned all 12
  binding approvals, in the others at least 1. D stopped after 1 to 3 rounds, never after
  the maximum of 6. Too little evidence is therefore not the cause.
* In line with the interpretation limits: D's shortfall cannot be attributed separately to
  the register or to the querying. The data point to the step where the register is
  first filled.

## B and C

* **Missed changes.** All five missed changes or transfers by B and C (B 2, C 3) fall in
  histories whose alternative is omission. In histories with an added field, B and C
  solved every observed change and transfer that ran (11 of 12 each; the twelfth was a
  failed or blocked call). This repeats the v0.4 observation that omission errs more
  often. The cells are small.
* **Retrieval coverage of B in large histories.** B's context contained 94.8 % of the
  binding approvals on average, and all of them in 14 of 24 tasks. One of B's two missed
  observed changes in K-L had 9 of 12 binding approvals in context.
* **Unidentifiable tasks.** B decided "apply" once (U-L) and was otherwise correct with
  the "keep" label. C reached "keep" in every completed case after its preparation had
  marked the context unresolved. Its one failure is a blocked task.
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

## Attribution candidates for review by Milad Morad

The failures that decide a hypothesis:

1. **E3:** D's register collapse and the missing world function, as above. Ten
   histories, list in `main-analysis.json` (`D`). Question: incomplete enumeration,
   polarity inversion, or both?
2. **E1 and E2 in U-L:** the two U-L histories with C preparation failures, in which B
   also failed (`history-dd4c7199f572` unidentifiable: B decided "apply";
   `history-f09764e24578` transfer: B decided "keep").
3. **E1 in K-L:** B's missed observed change in `history-b785c97276f8` (omission,
   9 of 12 binding approvals in context) and the failed B call in
   `history-80aeea38c4d2`.

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
