# Pilot v0.4 difficulty map

Status: complete registered run, 1 October 2026. Synthetic data only. Results describe
`deepseek-ai/DeepSeek-V4-Flash-0731` via FHGenie at reasoning `high` and are not
comparable with v0.3 (Amendment 4). Failure attribution was reviewed by Milad Morad. No
independent field validation, professional-quality or enterprise-utility claim is made.

The machine-generated report with every table is
[runs/live-fhgenie-high-20260930/REPORT.md](runs/live-fhgenie-high-20260930/REPORT.md).
This document interprets it and records the human attribution.

## Registration and execution

| Item | Record |
| --- | --- |
| Protocol | [pilot-v04-protocol.md](../../docs/pilot-v04-protocol.md) with amendments 1–3, the [surface repair](../../docs/pilot-v04-surface-repair.md), [Amendment 4](../../docs/pilot-v04-amendment-04.md) (model change) and [Amendment 5](../../docs/pilot-v04-amendment-05.md) (reasoning `high`, output limit 32,768, pinned PowerShell 7, tolerance of up to 19 isolated response failures) |
| Contract tests | Two development-data tests at `high`, 16/16 valid each ([16,384](diagnostics/fhgenie/contract-test-high-20260930/run/REPORT.md), [32,768](diagnostics/fhgenie/contract-test-high-32k-20260930/run/REPORT.md)). The second observed a 24,848-token output that the former limit would have truncated. |
| Material review | r2 materials approved by Milad Morad on 29 September 2026; carried forward by byte equality of all 14 files ([approvals](review/materials-amendment3-r2-amendment5-20260930-approvals.json)) |
| Live approval | Milad Morad, 30 September 2026, bound to configuration `23477ae8…678829` |
| Source binding | `1445c361ca7c3ec2f1048da47dc84432618545ab0fec94205e470205409badbb` |
| Configuration | [run-config.json](preflight/fhgenie-high-20260930/run-config.json); seeds 44361/44362/44363; temperature and top_p 1; timeout 420 s |
| Execution | 192/192 calls completed, 0 failed, 0 response failures, no retries or replacements; started 30 September 2026, 21:16 UTC |
| Run seal | `7afab956742071b0c5ddd8d696e854630a2a6f25945a32d34e6ece3dddbb8594` |

Earlier attempts remain preserved and are not part of these results: the stopped
gpt-6-sol attempt ([incident](runs/live-amendment3-r2-20260929-INCIDENT.md)), three
FHGenie toy probes and the two contract tests.

## Decisions and downstream outcomes

Registered metric: diagnostic decisions with warranted action, including the scope of declared rules, out of four per setting:

| Setting | Factor | C | B | C world fields | B world fields |
| --- | --- | ---: | ---: | ---: | ---: |
| S0 | base | 4/4 | 2/4 | 3/4 | 3/4 |
| S1 | raw artifacts | 3/4 | 3/4 | 4/4 | 3/4 |
| S2 | volume and noise | 4/4 | 2/4 | 3/4 | 2/4 |
| S3 | dependence | 4/4 | 4/4 | 3/4 | 3/4 |
| S4 | change over time | **2/4** | 3/4 | 1/4 | 3/4 |
| S5 | combined | 4/4 | 2/4 | 3/4 | 3/4 |
| **Total** | | **21/24** | **16/24** | 17/24 | 17/24 |

Controls: C 24/24, B 23/24 (one S3 unidentifiable control). A has current-task
information only. Its warrant score is not comparable; its world-field compliance is
6/24 on diagnostics and 24/24 on controls.

By task type, diagnostics:

| Task type | C | B |
| --- | ---: | ---: |
| Change with transfer | 5/6 | 1/6 |
| Change in an observed context | 5/6 | 3/6 |
| Resolved retention with transfer | 6/6 | 6/6 |
| Unidentifiable change | 5/6 | 6/6 |

**Correction (1 October 2026): B's lower score is not a decision deficit.** The
registered warranted-update metric, inherited from v0.3, also requires that every
*declared* `applied_rule` stays within warranted scope over all scope probes. In 7 of B's
8 diagnostic failures, B produced the correct output fields but declared a rule scoped
only to the two context attributes, without version or workflow. Such a rule is too broad
across versions and fails that check. C's executed rules come from its preparation with a
full scope. A post-hoc, descriptive comparison of the actual output fields (expected
baseline for `keep`, world fields for recoverable `apply`):

| Diagnostics, executed fields | C | B |
| --- | ---: | ---: |
| All | 21/24 | 23/24 |
| Change with transfer | 5/6 | 5/6 |
| Change in an observed context | 5/6 | 6/6 |
| Resolved retention with transfer | 6/6 | 6/6 |
| Unidentifiable change | 5/6 | 6/6 |

Controls on executed fields: C 24/24, B 23/24. B's only genuine diagnostic error is a
missed change (S2 Reporting, transfer); its control error applies an unsupported change
(S3 HR). The registered metric is not rescored; this table is an interpretive aid and was
not prespecified. It reverses the apparent B–C ordering: on the work actually produced,
B is at least as accurate as C. B's deficit lies in the scope of the rules it states,
which matters for reuse and traceability, not for the completed task.

C's three losses are described under failure causes. Unidentifiable cases can correctly
retain the baseline while failing world-field checks; world compliance there is not a
measure of warranted behaviour.

## Material relevance audit

Every present manipulated record type in every history met its gate: an action-flipping
record in unidentifiable histories and a contradiction-producing record elsewhere. The
full table is in the machine report. These are counterfactual checks of the material,
not measured model susceptibility.

## Surface audit

Unchanged from the reviewed r2 export
([surface audit](review/materials-amendment3-r2-amendment5-20260930/surface-audit.md)).
In the accepted-review population, development-selected family winners reach review
history-macro balanced accuracy of 0.463 to 0.544. 16 of 24 histories are undefined for
that metric. No tested selector is perfect on held-out hard negatives. The broad
work-record population reaches 0.816, which includes legitimate temporal information.
Untested shortcuts are not ruled out.

## Candidate errors

Confirmed candidate content errors (lower bounds, C1 / C2, pooled per setting):
S0 4/14 / 3/20, S1 2/12 / 1/15, S2 5/15 / 2/18, S3 3/22 / 0/25, S4 2/12 / 1/16,
S5 3/19 / 3/26. C2 generally reduces C1 errors. Candidate counts are model-controlled
and dependent and are not independent observations.

Transfer direction: in C2 there is one missed warranted transfer (S4 HR) and one
unsupported transfer (S1 Sales, unidentifiable). Observed-context contradictions occur
only in S4 (3/10 cells, C1 and C2). They are the inverted-polarity cases discussed below.
One simplest-pattern association occurs (S1 Sales). No wrong outcome matched the
registered majority or recency heuristics.

## Failure causes and headroom

Human attribution by Milad Morad, 1 October 2026
([record](review/attribution-live-fhgenie-high-20261001/responses.json), wording supplied
in [feedback](review/attribution-live-fhgenie-high-20261001/feedback-20261001.md) and
explicitly confirmed):

| Case | Expected | C did | Attribution | Tag |
| --- | --- | --- | --- | --- |
| S4 Sales, observed change (`task-f0ce9e3cd666`) | omit field | kept | unresolved | `baseline_polarity_inverted` |
| S4 HR, transfer change (`task-a920bd4a9f81`) | omit field | kept | unresolved | `baseline_polarity_inverted` |
| S1 Sales, unidentifiable (`task-e259eacd8c3d`) | keep baseline | omitted field | content | – |

In both S4 cases C read the current evidence and the compatible H14 functions in an
internally consistent frame but swapped the meaning of baseline and alternative. It
stated that the baseline already omitted the field and therefore encoded no omit rule.
Its compatible functions were exactly the complements of the oracle's. This is neither a
correctly formulated, wrongly encoded rule nor a demonstrated inference error from the
evidence. In S1 C treated a non-binding preference as support, enumerated two of four
compatible functions and extended the change to Mira/strategic. That its output matches
the hidden world does not make the decision warranted.

**Headroom is not met in any setting.** S1 has 3/4 correct. In S4 (2/4 correct) both
failures are unresolved, so the conservative content numerator is 0/2. The S4
classification is **provisional**: it would hold only if both cases were attributed to
content.

The following points must be read with the S4 result:

* In S4, the temporal break coincides with the omission direction. Both S4 change
  diagnostics have "omit" as the alternative, so the fixed allocation cannot separate
  the effect of the version break from the direction of the alternative.
* All three C failures occur in the 6 of 24 histories whose alternative is omission; C
  made no diagnostic error in the other 18. With four diagnostics per setting this is an
  observation, not an estimate.
* Both polarity inversions occur in histories with a version change in which the old
  version shows the field included and the current version mostly removes it. In S2 HR,
  with the same direction but no version change, C read the polarity correctly.
* The explanation that C inferred a changed baseline from the version change is
  **unverified**. Two cases cannot distinguish it from a plain misreading.

## Resource use

Reported input plus output tokens: 2,072,310 (no unknown usage). A 167,701; B 633,227;
C preparation 1,110,811 (C1 561,763, C2 549,048); C generation 160,571. Reasoning tokens
are not reported separately by the provider and are contained in output.

Conditional break-even with B, under the registered assumptions (stationary tasks,
reusable guidance, no maintenance): C's preparation costs 24,000 to 82,000 tokens per
history. C becomes cheaper than B from about the 3rd or 4th task for 60-record
histories and from about the 5th to 18th for six-record histories. These are
projections, not prices or observed savings. They hold only alongside the quality
results above.

## Limits

Synthetic placeholder families; the public H14 class excluding XOR and XNOR, on which
transfer depends; supplied approval semantics; four diagnostics per setting; rotating
family assignments; shared templates; one model with one reasoning level and no
sampling seed; AI-assisted analysis and a single author-level human attribution. The
surface audit does not exclude every shortcut. Nothing here supports conclusions about
unrestricted contextual learning or enterprise performance.

## Interpretation and next decision

Strong two-pass direct adaptation resolved 21 of 24 diagnostic cases with this Flash
model at high reasoning. None of the six evidence conditions produced a systematic C
failure. The tested conditions did not establish headroom. B, which reads the same
history only at generation time, produced the correct output in 23 of 24 diagnostics,
including 5 of 6 transfer changes. The registered metric ranks C above B only because of
the scope of B's declared rules. This run therefore provides **no evidence** that
explicit preparation improves decisions over direct use of the history. Its possible
advantage lies in reusable, correctly scoped guidance and lower per-task tokens. The
token break-even projections compare C with a B that is at least as accurate on the
executed output.

The protocol's options for v0.5 (hypothesis-guided witness search, a temporal evidence
registry) are not motivated by a clear inference failure here. The S4 observations point
first to a design repair: separate the direction of the alternative from the evidence
condition. **Noted for v0.5:** balance the direction of the alternative within every
setting, especially for the temporal break. The selection of any v0.5 mechanism is a
separate decision with its own protocol, frozen materials and fresh cases. It also
follows the [replacement-run rule](../../docs/pilot-replacement-run-rule.md) and
Amendment 4's fixed model.
