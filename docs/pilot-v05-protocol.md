# Pilot v0.5 protocol

Approved on 1 October 2026 with four changes, which are incorporated below; the
approval record is at the end. **No model call is authorised by this approval.**
Calibration, the D technical check and the main run each need their own live approval.
Synthetic data only.

## Starting point from v0.4

With explicit approval semantics, two known context dimensions and histories that fit
into one call, direct use of the history (B) reached 23/24 correct diagnostics on the
executed output fields and two-pass preparation (C) 21/24. No setting showed headroom.
Preparation offered a token advantage for large histories but no accuracy advantage.
The registered v0.4 metric penalised B for the scope of its declared rules even where
its fields were correct (see `pilots/v04/DIFFICULTY_MAP_REPORT.md`). All three C
failures fell in histories whose alternative was omission. That direction was not
balanced within settings.

## Research question

Does direct use of evidence remain sufficient when

1. the history exceeds the input budget of a single call, so evidence must be selected
   or condensed, and
2. it is publicly unknown which of several context attributes determine a requirement?

Where it does not, does a hypothesis-guided procedure (D) improve accuracy or cost
relative to strong direct procedures?

The study remains a synthetic, descriptive map. It does not test professional quality,
enterprise utility or unrestricted requirement discovery.

## Rule class

Each work item carries six binary context attributes `a1`–`a6`. Each attribute has two
named values; the predicate tests the second listed value. A requirement is a Boolean
function of **at most two** attributes with the H14 forms: constant 0 or 1; a single
literal; a conjunction of one literal from each of two distinct attributes; or a
disjunction of one literal from each of two distinct attributes. XOR and XNOR are
excluded. Over six attributes this is the class **H134**: 2 constants, 12 literals and
120 two-attribute conjunctions and disjunctions, all with distinct truth tables over the
64 cells.

The class is described publicly in every payload. Which attributes are relevant is not
disclosed. In the *known-2* condition the public class is restricted to two declared
attributes, which gives H14 as in v0.4. The other four attributes stay visible but are
declared irrelevant. Records have the same format in both conditions. Only the declared
hypothesis class differs.

A case is unidentifiable when compatible functions disagree on the evaluated cell. In
*unknown-6*, this arises prospectively through **confusable attributes**: two attributes
covary across all binding approvals, so rules over either one fit the evidence, but they
differ in the evaluated task.

## Evidence semantics

The explicit v0.4 approval convention is unchanged. A version registration lists the
authorised reviewers and the validity interval. A binding approval is an accepted review
by a listed reviewer within that interval, with the target field in `reviewed_fields`.
The v0.4 distractor types are kept with fixed quotas per history: unauthorised revision,
rejected artifact, personal preference, approval without the target field and transient
technical failure. Copies, forwards and version breaks are **not** used, because v0.4
did not show them to be difficult and they would confound the two new factors. Implicit
evidence is deferred to a later iteration.

## Settings and tasks

A 2 × 2 design. Each setting has four histories, one per placeholder family (HR, sales,
retrieval, reporting).

Proposed record quotas, to be checked before any material is generated:

| History size | Registration | Binding approvals | Distractors (five v0.4 types) |
| --- | ---: | ---: | ---: |
| 24 records | 1 | 12 | 11 (at least two per type) |
| 240 records | 1 | 12 | 227 (fixed per-type quotas, as in v0.4 S2) |

The number of binding approvals is equal across sizes, so size changes only the amount
of surrounding material.

| Setting | History size | Candidate attributes |
| --- | --- | --- |
| K-S | 24 records (about 8,000 tokens, within one call) | known-2 |
| K-L | 240 records (about 77,000 tokens, about 3.2 × the call budget) | known-2 |
| U-S | 24 records | unknown-6 |
| U-L | 240 records | unknown-6 |

Every history has **four future tasks**, generated only after all preparations are
sealed. The structure is the same in all four settings (adjustment after the
constructibility check, `pilots/v05/analysis/CONSTRUCTIBILITY.md`):

* three diagnostics: a change in an observed context, a retention in an observed
  context, and **one hard task**;
* one control outside the declared workflow, where no update is authorised.

The hard task is a **change with transfer** to an unobserved cell in two histories per
setting and an **unidentifiable** case in the other two. Retention with transfer is not
used. In known-2 a history can carry only one hard type, and v0.4 found that type easy
for every arm. The direction of the alternative (add or set versus omit) is **balanced
within each hard type in every setting**: one history of each direction. Family
assignment rotates across settings. The generator selects true functions from the
public class subject to these slot constraints. The oracle checks every task type
independently from public evidence only. A history that cannot be constructed stops
generation; seeds are not redrawn.

The main run has 16 histories per arm, with 48 diagnostics (16 observed change, 16
observed retention, 8 transfer change, 8 unidentifiable) and 16 controls. With two
diagnostics per hard type, setting and arm, conclusions about the hard types remain
thin. The report must state this.

## Arms

All arms use the same model and the same per-call input budget of **24,000 tokens**
(prompt, schema and payload, counted with the v0.4 contract-test character-per-token
ratio of 3.10). Every task is generated by one call with the same generation contract.

**Budget per history and arm.** The four generation calls are **reserved in advance**
outside the cap, up to four times the maximum generation input of 24,000 tokens plus the
32,768-token output limit (227,072 tokens). The cap of **300,000 reported tokens applies
to preparation only** (C1/C2 and D's index, query and final calls). *Correction confirmed
on 1 October 2026: the first wording deducted the reserve from the 300,000 cap, which
would leave almost nothing for preparation, while large-history preparation needs about
220,000 to 240,000.* Before each further preparation round, C and D check whether the remaining preparation budget can still cover one more round and the
final call, each assumed at its maximum (input budget plus output limit). If not, they
proceed directly to their final call. **No arm loses a task to the cap.** Early
completion is reported. A and B have no preparation.

**A, no history.** The current task, configuration, public contract and class
description.

**B, direct use with retrieval.** As A plus the most relevant records, selected
deterministically from public fields only. B is meant to be a strong baseline, so
retrieval prefilters the way any reasonable system would:

1. All registrations.
2. All accepted reviews that list the target field in `reviewed_fields`.
3. The remaining records, ranked by the number of context attributes they share with the
   task and then by recency.

Records are added in this order until the budget is full. For 24-record histories this
is the whole history, as in v0.4. Retrieval does not read outcomes, truth or authority
validity; whether a review is binding remains for the model to judge. Retrieval coverage
of the records needed for identification is reported.

**C, chunked preparation.** The history is split into consecutive chunks that fit the
budget together with the running guidance. Each chunk call (C1) receives the previous
guidance and the next chunk and returns updated guidance in the v0.4 `Preparation`
contract. A final consolidation call (C2) receives the guidance together with the
records it cites, up to the budget, and returns the retained guidance. Small histories
need one C1 call and one C2 call, as in v0.4. Large histories need about five C1 calls
and one C2 call. Generation receives only the applicable retained guidance.

**D, grounded reflection with a hypothesis register and record queries.** Fixed now,
before any v0.5 data are generated:

1. *Index call.* D receives the public contract, the class description, the
   registrations and a deterministic index of the history: the number of records per
   event type and decision, and for every attribute the counts of approvals per value.
   It receives no record contents beyond the registrations. It returns a **hypothesis
   register**: candidate functions from the declared class with status `open`,
   `eliminated` or `supported`, their evidence references, and a list of queries.
2. *Query rounds.* At most **six** rounds, each with at most **three** queries. A query
   is a JSON filter over public record fields: attribute values, event type, decision,
   reviewer and reviewed field, combined conjunctively. The harness executes it
   deterministically and returns matching records ordered by timestamp, truncated to
   the budget. The truncation is reported to D. Each round call receives the register
   and the results and returns an updated register and the next queries. D should ask
   for records that distinguish open hypotheses, for example cells where confusable
   attributes differ. The model has no tool interface; the harness alone executes
   queries.
3. *Stopping.* D stops when it returns no queries, when the register states that no
   further query can discriminate, or after six rounds.
4. *Final call.* D converts the register into guidance in the v0.4 `Preparation`
   contract. Adopted rules must be entailed by all open or supported hypotheses on the
   affected cells. Disagreement becomes `unresolved`. Generation is identical to C's.

D sees no future task. Its queries and results are logged and sealed with the
preparation. D's mechanism above is fixed by this protocol. D's prompts are written
after the material review. D sees no v0.5 data until the headroom decision and the
single possible amendment are settled. After the D technical check, only format and
contract changes are permitted, never strategy changes. Every change is documented.

## Measurement

**Primary outcome:** the decision implied by the **executed output fields**, compared
with the oracle's warranted action. It is the same for all arms. A diagnostic is
correct if the fields equal the consensus fields for `apply`, or the baseline for
`keep` and for unidentifiable cases. Missing or invalid outputs fail. Declared rules,
decision labels and rule scope are **secondary** and never enter the primary outcome.
This removes the v0.4 measurement asymmetry.

Report the primary outcome per setting, arm and task type, with fixed denominators. Hard
diagnostics (transfer, unidentifiable) are always reported separately from observed
diagnostics.

Secondary outcomes:

* Tokens per task and **measured** amortisation over the four tasks of each history,
  including preparation, query rounds and generation. There is no extrapolation beyond
  observed tasks.
* Error types as in v0.4: unsupported or missed change, unsupported or missed transfer,
  adoption of distractors, and the **baseline-polarity inversion** tag introduced after
  v0.4.
* For D: queries issued, discriminating records found, register accuracy against the
  oracle's compatible set, and rounds used.
* For B in large histories: whether the retrieved set contained the records needed to
  identify the function (retrieval coverage).

Failure attribution follows the v0.4 taxonomy and conservative rules. Attribution is
reviewed by Milad Morad for failures that decide a hypothesis below.

## Prespecified expectations and decision rules

These are descriptive expectations, not significance tests. There are 12 diagnostics
per setting and arm, four of them hard.

* **E1 Selection:** In K-L and U-L, the better of B and C is less accurate than in the
  matching small setting.
* **E2 Dimension uncertainty:** In U-S and U-L, the better of B and C is less accurate
  than in the matching known-2 setting, mainly on transfer and unidentifiable tasks.
* **E3 D accuracy:** D is correct in at least **two more** diagnostics than the better of
  B and C. E3 is evaluated descriptively in **every** setting, with hard and observed
  diagnostics reported separately.
* **E4 D cost:** Where D is at least as accurate as the better of B and C, D uses at most
  **70 %** of that arm's tokens per task over the four tasks of a history.

**Calibration headroom criterion,** fixed on 1 October 2026 after the constructibility
check. The calibration is meant to detect a ceiling across the board before the costly
main run. **There is no headroom only if the better of B and C correctly solves every
hard calibration diagnostic (transfer and unidentifiable) in all four settings.** Only
then may the single permitted amendment be used, for example to increase history size or
attribute confusability before the main run. It must be decided before D sees any v0.5
data. In every other case the main run follows, and E3 is evaluated descriptively in all
settings. The criterion replaces the earlier "at most 6 of 8" (later "at most 4 of 6").
With only two hard diagnostics per setting, such a count would show headroom almost
never, and the easy observed diagnostics would dilute the signal.

## Changes from the first material review (material revision r2)

The first material review (2 October 2026, supplied as a pasted review text) did not
approve the materials. It reproduced the binding sets, compatible sets and all 16
expected actions with an independent H134 oracle, found no surface separation between
binding and similar reviews, and showed that every hard task was solvable by simple
shortcuts. The generator was changed constructively within each slot's seeded stream,
without redrawing seeds:

1. **Similarity placement.** Nearest-neighbour heuristic: the configuration of the
   binding approval(s) with minimal Hamming distance over all six attributes, majority on
   ties, "keep" on a tied vote. For every hard task it must give the action that is not
   warranted. For transfer the nearest approvals lie in the diagonal cell of the relevant
   pair; for unidentifiable tasks they show the alternative.
2. **Unidentifiable probes.** At least half of the compatible functions change at the
   probe. In unknown-6 the probe breaks the covariance so that every function over the
   confusable attribute changes.
3. **Reviewers.** When both configurations occur, each listed reviewer approves each
   configuration at least once. Each configuration then occurs at least twice.
4. **Distractors in the exact hard-task context.** Non-binding accepted reviews and
   preferences there show the configuration that is not warranted; a rejected version
   there carries the warranted one. Neither of the misreadings "all accepted reviews
   bind", "rejection inverted" or "preference followed" reaches the warranted action.
5. **Names.** Person names and attribute values come from disjoint pools.
6. **Approvals without the target field** list an existing other field of the artifact.

Generation stops if any of these conditions fails. A **heuristic audit** without model
calls (`pilots/v05/analysis/heuristic_audit.py`) reports, per setting and hard type, how
often the nearest-neighbour heuristic, the majority of compatible functions, the simplest
compatible function, always-keep and the three misreadings give the warranted action. It
also reports reviewer × configuration counts and name collisions. These reference lines
also appear in the final report.

### Changes from the second material review (material revision r3)

The second review (2 October 2026, supplied as a pasted review text) confirmed r2 with an
independent oracle but did not yet approve it. Three corrections:

1. **Rejected versions carry no information.** The r2 rule that a rejected version in the
   exact hard-task context carries the warranted configuration created a new shortcut:
   reading a rejection on unrelated grounds as tacit assent to the field reached the
   warranted action. Now no rejected version sits in the exact hard-task context.
   Elsewhere, rejected versions are balanced between world and counter configuration
   within the relevant cell of the probe and within the rest. In small histories the two
   rejections carry one configuration each and lie outside the relevant cell. Every
   rejected version is **strictly farther from the hard task (Hamming distance) than the
   nearest binding approval**. Otherwise a rejection would decide the nearest neighbour,
   and either inverting it or reading it as assent would reach the warranted action.
2. **Distractors outside the exact context carry no information.** Non-binding accepted
   reviews, preferences and rejections of each type are balanced between world and
   counter configuration, separately in the relevant cell of the probe and in the rest
   (deviation at most one per history). Ties are broken at random, so single records in
   small histories do not systematically agree with the world.
3. **The audit reports "undefined" separately.** Each misreading ("all accepted reviews
   bind", "rejection inverted", "rejection as tacit assent", "preference followed") is
   reported in three readings:
   * the oracle reading, in which a contradiction is "undefined" and not a success;
   * fallback (a), in which a contradiction means "keep";
   * fallback (b), the majority of the misread evidence in the exact context, otherwise
     the nearest neighbour over binding plus misread evidence.

   Condition: under (b) no misreading reaches the warranted action. Under (a),
   unidentifiable tasks are structurally always right, like always-keep. The audit also
   reports distractor agreement with the world per type, size and location (exact,
   relevant cell, rest). It covers all 32 histories of the review and development seeds.

The search for a distractor layout satisfying these conditions runs within the slot's
seeded stream. If none is found, generation stops.

On 2 October 2026, while checking r2, the final-test histories were generated once in
memory to confirm that the main run would not stop at construction. Only the history
seed 45061 was used. The future-task seed 45062 and the order seed 45063 were not used,
so no final future task or call order was generated. The material was neither saved nor
inspected, and no generator change followed from it. Later
constructibility checks use only development and review seeds.

Confirmed: D's index counts "approvals per value" over the same records as B's prefilter,
namely accepted reviews that list the target field in `reviewed_fields`, without any roster
or validity check.

## Procedure

1. **Protocol approval.**
2. **Constructibility check first** (done on 1 October 2026): unknown-6 is
   constructible with the quotas above; known-2 cannot carry more than one hard type per
   history, which led to the uniform task structure above.
3. **Implementation and offline verification:** generator and H134 oracle, retrieval,
   chunked C, the D harness and query executor, budget reservation, field-based scoring,
   mock runs and tests.
4. **One material review** with four examples, one per setting, from a separate review
   seed namespace.
5. **Calibration** with A, B and C only on development seeds: two histories per setting,
   eight histories, 32 tasks per arm. Apply the headroom criterion and decide on the
   single possible amendment. D has not yet seen v0.5 data at this point.
6. **D technical check.** Up to 20 D calls on two development histories, for JSON
   validity and query execution only, with no scoring. The FHGenie contract tests did not
   cover D's register and query contract. Afterwards only documented format and contract
   changes are permitted.
7. **Freeze D** and all sources, then **the main run** on fresh final seeds. One run, no
   retries or replacement runs, sealed outputs. The replacement-run rule
   (`docs/pilot-replacement-run-rule.md`) applies.
8. **Attribution review and report.**

At most one amendment is permitted.

## Model and budgets

`deepseek-ai/DeepSeek-V4-Flash-0731` via FHGenie, reasoning `high`, output limit 32,768,
temperature and top_p 1, as fixed for v0.5 by Amendment 4, with a per-call timeout of 1,200 s (technical correction below). The endpoint
is configured locally and verified by hash. It is never written to the repository.

Estimates from v0.4 usage. Preparation calls averaged about 13,000 output tokens, B
generation about 2,800 and other generations about 900. Records average about 320
tokens.

| Arm | Per small history | Per large history | Calls per small / large history |
| --- | ---: | ---: | --- |
| Arm | Per small history | Per large history | Calls per small / large history |
| --- | ---: | ---: | --- |
| A | about 14,000 | about 14,000 | 4 / 4 |
| B | about 56,000 | about 108,000 | 4 / 4 |
| C | about 64,000 | about 236,000 | 6 / 10 |
| D | about 116,000 | about 256,000 | up to 12 / 12 |

| Phase | Calls (estimate) | Tokens (estimate) | Hard call cap | Token stop |
| --- | ---: | ---: | ---: | ---: |
| D technical check | ≤ 20 | ≤ 0.4 M | 20 | 0.5 M |
| Calibration (A, B, C; 8 histories) | about 130 | 2.0 M | 170 | 3.0 M |
| Main run (A–D; 16 histories) | about 450 | 6.9 M | 560 | 10.0 M |

Token stops are checked between calls, as in v0.4; the final in-flight call can cross
them. Up to 10 % isolated response failures per phase are tolerated under the Amendment 5
rule; the next one stops scheduling. Estimated sequential runtime: calibration about
1.5 hours, main run about 5.5 hours, based on v0.4 call durations.

## Calibration attempts and technical correction of the timeout

Calibration attempt 1 (2 October 2026) was killed after 13 valid calls by the time limit of
the working session that had launched it as a background process. Attempt 2, started as an
independent process, was stopped by the runner after 18 calls, when a C1 call exceeded the
420 s timeout and its usage became unknown. Neither attempt reached generation or scoring,
and no preparation content was inspected. Both run folders are sealed and kept, with
incident reports. Each new attempt was explicitly decided and approved by Milad Morad.

FHGenie throughput varied between about 36 and 221 output tokens per second. A full
32,768-token output can therefore take far longer than 420 s. As a **technical
correction** (3 October 2026, decided by Milad Morad: "A jetzt, und neue Live-Freigabe"),
the per-call timeout is 1,200 s for all v0.5 phases, which covers a full output at about
28 tokens per second. All other rules are unchanged, including "unknown usage stops".
This correction is not the single amendment reserved for the headroom decision. Live
phases run as independent processes, not as background tasks of a working session.

Calibration attempt 3 (3 October 2026, folder
`pilots/v05/runs/live-calibration-20261003-attempt3`) completed: 127 calls, 1,861,787
reported tokens, no unknown usage, no response failures, no halt; seal
`0b2acde6ce83ef00fb598646cecea5866e6b2a8686b0fe24014b71d83546a7b1`. Every C preparation
stayed within its cap. Headroom decision by the registered rule: the better of B and C
solved both hard calibration diagnostics in K-L, K-S and U-S, but only 1 of 2 in U-L
(B failed the unidentifiable task, C the transfer task). Hence **headroom exists**, and the
reserved single amendment is not used. The margin is one task in one setting, and the
calibration results are descriptive only. The next step is the D technical check, which
needs its own live approval.

D technical check (3 October 2026, approved by Milad Morad, folder
`pilots/v05/runs/live-dcheck-20261003`, seal `9d822acc…c7263`): 4 calls, 53,826 tokens,
all responses valid JSON. It found two contract defects in the query code, not in the
model. First, `actor` and `reviewed_field` treated "any" as a literal value, although
the prompt says "any" does not filter, so all queries of one history matched nothing.
Second, query results did not budget their per-result wrappers, so a round prompt
exceeded the call limit by 37 characters and the runner stopped before the call. Both
are fixed as permitted contract changes, with regression tests. Prompts and strategy are
unchanged. See `pilots/v05/runs/live-dcheck-20261003-INCIDENT.md`. A second check (at
most the remaining 16 of the 20 D calls) needs its own approval.

## Seeds

Development and calibration 45021/45022/45023, review 45031/45032, final 45061/45062/45063.
These are prospective choices and are not selected by performance.

## Separation, sealing and integrity

Unchanged from v0.4. The oracle reads public evidence only. Payload allowlists and
leakage tests apply. Preparations, including D's queries and results, are sealed before
future tasks are generated. Raw responses, prompts, usage and errors are preserved. There
are no selective retries, repairs, substituted histories or purchases. D's harness is
the only component that executes queries. It has no write access to evaluator material.

## Proposed schedule

Realistic for results by about 20 October 2026 if each approval takes at most one day.

| Date | Step |
| --- | --- |
| 1–2 Oct | Protocol review and approval |
| 3–7 Oct | Implementation and offline verification. This is the critical path: H134 generator and oracle, chunked C, D harness |
| 8 Oct | Material review of four examples; D prompts frozen |
| 9 Oct | Calibration with A, B and C (about 1.5 hours of calls) |
| 10 Oct | Headroom decision and amendment only if needed; then the D technical check |
| 12–13 Oct | Main run (about 5.5 hours of calls) |
| 14–17 Oct | Scoring, attribution review, report |
| 18–20 Oct | Buffer |

Main risks: the D harness and chunked C take longer than planned, or calibration shows
no headroom and the amendment is needed. Each costs about two days, still within the
buffer once. If both occur, results move to about 23 October.

## Interpretation limits

Synthetic placeholder families; the public H134 restriction, on which transfer depends;
supplied approval semantics; 16 diagnostics per setting and arm; one model; deterministic
retrieval as one choice of strong direct baseline; and D as one specific mechanism, not
grounded reflection in general. **Hard tasks are deliberately constructed so that
similarity and naive readings mislead.** Their accuracy is a stress test, not an estimate
of natural error rates. Success on unidentifiable tasks is broken down secondarily by the
declared decision label of each generation call, for all four arms. For C and D it is
also broken down by whether their preparation marked the context unresolved, because
confusion followed by fallback to the baseline also yields the correct fields.
**Under H14 an identified transfer always equals the
shared value of the two neighbour cells in the relevant pair**, so in known-2 a transfer
is solvable within the pair by neighbourhood. The r2 similarity placement prevents this
only over all six attributes, not within the pair. **An advantage of D cannot be attributed separately to
the hypothesis register or to targeted querying.** Separating them would need another
arm, such as targeted queries without a register. Conclusions about D are worded
accordingly.

## Approval record

Protocol approval: Milad Morad, 1 October 2026, with four changes (strong B retrieval,
reserved generation budget, D technical check after the headroom decision, early
constructibility check for U-S) and the added interpretation limit. The headroom
criterion, E1–E4 and the budget limits are approved. The wording was supplied in a
pasted text and explicitly confirmed by Milad Morad, including the budget correction
(preparation cap of 300,000 tokens, generation reserved outside the cap). Actual
response: "ja, mit Budget-Korrektur freigegeben".

Adjustment after the constructibility check: Milad Morad, 1 October 2026. It
introduces the uniform task structure (three diagnostics with one hard task, plus one
control), two transfer and two unidentifiable histories per setting, balanced direction
within each hard type, no retention with transfer, and a generation reserve for four
calls. It replaces the headroom criterion with "no headroom only if the better of B and C
solves every hard calibration diagnostic in all four settings", with E3 evaluated
descriptively in all settings. The wording was supplied in a pasted text and endorsed by
Milad Morad with "push +".

Total planned FHGenie use is at most about 13.5 million tokens across all phases,
counted at the stops (expected about 9.3 million). The cost question is to be settled before the live approvals.
Material review: first export not approved (2 October 2026; review text supplied by Milad
Morad, recorded as feedback). Revision r2 not yet approved (second review, same day,
recorded as feedback). Material review: r3 approved by Milad Morad, 2 October 2026
(export `pilots/v05/review/materials-v05-r3-20261002`, seal
`2d5c5b8068d3bafa40494b43038f516d20c2fdbd729ed27cb64b1b844fd531b0`). The wording was supplied in a
pasted review text and confirmed by Milad Morad ("ja", 2 October 2026).

Note from the r3 review on oracle readings of misreadings: for transfer tasks the
binding approvals already identify the action. Additional misread evidence can only
shrink the compatible set, so it yields the same action or a contradiction, never the
other one. An oracle-reading hit there (for example `inverted_rejections` in U-S
transfer, 1 of 4) is therefore not a shortcut. For unidentifiable tasks a hit means the
misreading resolves towards the baseline or stays open, the direction of always-keep,
which the breakdown by declared decision label covers.
Calibration and main-run live approvals: pending, each separately.
