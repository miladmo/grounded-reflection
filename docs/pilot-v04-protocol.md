# Pilot v0.4 protocol

Approved for implementation with amendments 1 and 2, 29 September 2026. Synthetic data only. Human approval of the six review examples and a separate live-run approval remain pending. Neither is implied by implementation approval.

Amendment 3 was approved for implementation on 29 September 2026, including its two supplements and the user's explicit clarification separating counterfactual action flips from contradictions. [The approved amendment](pilot-v04-amendment-03.md) defines the revised hypothesis class, task subtypes, record quotas, counterfactual audits and transfer measurements. It takes precedence over the initial material specification below. The original review set and offline run remain preserved. Revised material review and live approval are pending.

The 29 September material review withheld approval and requested [revision 2 of the presentation and error audit](pilot-v04-surface-repair.md). That repair is authorised for implementation. It adds overlapping random timestamps, shared varied comments, shuffled record order, a held-out surface-heuristic audit and a secondary apparent-conflict subtype. The supplied independent reconstruction is AI-assisted review, not human validation. Material approval and live approval remain pending.

[Amendment 4](pilot-v04-amendment-04.md) was approved on 30 September 2026. It replaces `gpt-6-sol` with medium reasoning by `deepseek-ai/DeepSeek-V4-Flash-0731` via FHGenie, at the reasoning level fixed by the [contract test](pilot-v04-fhgenie-contract-test.md) (starting at `high`). It takes precedence over the model statement under Arms and execution. Results are not comparable with v0.3 and describe this model only. The contract test and the final run each require separate explicit approval.

[Amendment 5](pilot-v04-amendment-05.md) was approved on 30 September 2026. It fixes reasoning `high`, raises the per-call output limit to 32,768 tokens (subject to a new contract test), pins the PowerShell 7 executable by hash and lets isolated response failures stay in their denominators without stopping the run. The 20th such failure stops further scheduling. This implements the rule under Live budget and stopping that unaffected calls may continue after an isolated response failure.

## Purpose

Map the evidence conditions under which strong direct adaptation loses warranted decisions, and distinguish failures of inference from failures of representation or execution. This is a difficulty study, not a test of a grounded-reflection method.

In [v0.3 calibration round 2](../pilots/v03/CALIBRATION_R2_REPORT.md), B and C made all eight warranted diagnostic decisions correctly. Their histories were short, observations were already interpreted, and public assumptions supplied independence and stability. These are plausible explanations for the ceiling, not established causes. v0.4 examines them prospectively. C may again succeed on every setting.

D is excluded. Do not run, inspect or modify its prompts, implementation or outputs for this study. A possible v0.5 mechanism will be selected only after the difficulty map, then frozen and assessed on fresh data.

## Questions and expectations

1. Does C retain warranted changes and warranted retention decisions when the same kinds of requirements must be inferred from less explicit evidence?
2. Where C fails, is the error in interpreting evidence, encoding guidance or executing that guidance?
3. How much reusable preparation does C require, and under what assumptions could its reported token use become lower than B's over future tasks?

Raw artifacts, distracting records, dependent corrections and changes in authority may expose weaknesses in C. No setting is required to produce a failure. The study will not weaken C, search seeds for poor performance or add cases after seeing scores.

## Materials and sampling

Generate 24 separately seeded histories, four per setting. Every history has one diagnostic future task and one control task. Use one execution per arm and task. Multiple histories are generated before any live output is seen, rather than hand-edited until a target score appears.

Start with four clearly labelled placeholder families, one represented in each setting.

| Placeholder family | Candidate requirement types | Candidate misleading evidence |
| --- | --- | --- |
| HR documents | Recipient-specific reference or document format | Contract and recipient confounding, personal edits |
| Sales review | Reviewer or workflow-specific amount presentation | Forwarded corrections, a single person's preference |
| Research retrieval | Collection and version-specific route or verification rule | Temporary failure, an obsolete route |
| Reporting | Artifact-specific label or schema | Cosmetic changes, evidence from another artifact type |

These are synthetic design devices, not descriptions of an industry partner's practice or established field requirements. Requirement types, scope dimensions, distractor types and their frequencies are configurable. A later field-research list may replace the placeholders only before the materials freeze and live approval. Record the actual changes and re-review affected materials.

Use a fixed, prospective case allocation. Three diagnostic regimes are distinguished.

* Warranted change. All admissible policies agree on a change for the diagnostic context.
* Resolved retention. All admissible policies agree with the configured baseline in that context.
* Unidentifiable change. Admissible policies disagree about a possible change. The experimental action is to retain the baseline without claiming that it is the true requirement.

The last two regimes both require retention, but must not be pooled without showing their separate counts. Unidentifiable cases may intentionally fail hidden-world field checks despite a warranted decision.

| Setting | Explicitness | Record count | Provenance | Validity | Change / resolved retention / unidentifiable |
| --- | --- | --- | --- | --- | --- |
| S0 base | Interpreted observations | About 6 | Independent origins | Stable | 2 / 1 / 1 |
| S1 raw | Before/after artifacts and logs | About 6 | Independent origins | Stable | 2 / 1 / 1 |
| S2 volume and noise | Interpreted observations | About 60 | Independent origins | Stable | 2 / 1 / 1 |
| S3 dependence | Interpreted observations | About 6 | Copies and forwards present | Stable | 2 / 1 / 1 |
| S4 change over time | Interpreted observations | About 6 | Independent origins | Documented break | 2 / 1 / 1 |
| S5 combined | Before/after artifacts and logs | About 60 | Copies and forwards present | Documented break | 2 / 1 / 1 |

Amendment 1 fixes the same regime mix in every setting so that differing change/retention frequencies do not dominate a four-case comparison with S0. This gives twelve warranted changes, six resolved retentions and six unidentifiable changes overall. Use the following private allocation, where C means warranted change, R resolved retention and U unidentifiable change.

| Setting | HR | Sales | Retrieval | Reporting |
| --- | --- | --- | --- | --- |
| S0 | C | C | R | U |
| S1 | R | U | C | C |
| S2 | C | R | U | C |
| S3 | U | C | C | R |
| S4 | C | C | R | U |
| S5 | R | U | C | C |

Every family contributes three warranted changes. HR and retrieval each contribute two resolved retentions and one unidentifiable change; sales and reporting each contribute one resolved retention and two unidentifiable changes. This remaining family imbalance is reported explicitly. Exact balance of six retention cases across four families is impossible at this size.

Counterbalance change directions and values independently of setting names. Exact record counts and seeds are frozen before live execution. This allocation is evaluator material and does not enter model payloads.

Histories use separate seeds, but share templates, a model and an oracle. The two future tasks from one history share preparation. These are not independent samples of enterprise work. Regime frequencies are held constant, but family-to-regime assignments rotate and there are only four diagnostics per setting. Results form a descriptive map, not a causal estimate of individual factor effects. Volume and noise are a bundled intervention. The combined setting cannot identify individual interactions.

Each control probes a prespecified boundary outside the diagnostic adjustment, where retention is warranted. A control must remain informative when the diagnostic itself requires retention, for example by testing another plausible but unsupported extension. Report controls separately from diagnostics.

## Evidence generation

The generator creates a latent world, an event stream and public work records. Raw records contain drafts, changed fields, review comments, acceptance or rejection events, execution outcomes and provenance or version events. Interpreted records are a different rendering of the relevant events. The raw rendering must not label the inferred requirement or its evidential status.

Personal preferences, unrelated edits and temporary failures are generated prospectively. The small and large histories retain a documented core of potentially informative events. Additional records must not accidentally introduce a decisive witness unless that is part of the registered scenario. Report distractor counts and core-evidence coverage in the private material audit.

Copied records retain visible origin references. Forwarding a correction into another context does not establish that it was independently reviewed there. Copying alone does not add information to the warrant oracle. Where independent contexts distinguish rival policies, the dependence manipulation changes that witness coverage visibly. Do not invent an undisclosed minimum-vote rule to make duplication count as an error.

Temporal settings contain visible dates, authority changes or template-version events. Supersession applies to the documented scope and time, not automatically to every older record. Future tasks expose their current date and relevant version. Continued validity must follow from public intervals or version semantics, not from a hidden assumption that past authority persists. If the evidence does not establish it, validity remains unresolved. Stable settings need not announce that stability is guaranteed. Model-facing assumptions explain record and operator semantics but do not declare records independent, authority stable, roles irrelevant or distractors harmless.

Canonical field names, allowed values and rule operations stay explicit in all arms. Difficulty must not come from arbitrary strings, inaccessible metadata or missing execution instructions.

## Three truth objects and an independent warrant oracle

Maintain three private evaluator objects for each history.

1. The actual synthetic world policy, including its temporal scope.
2. The policies admissible under the public evidence and the registered hypothesis class.
3. The obligations of each future task, including the warranted action and actual-world field values.

The warrant oracle independently enumerates and filters a bounded policy class. Its evidence input is exclusively the public evidence projection, with public current-task metadata when deriving task obligations. Structural facts such as origin references, artifact differences, review authority and validity intervals must be present in those public records. Any derived feature must be deterministically reconstructible from them. The private latent event stream is not a second oracle input. The oracle must not read the true policy identifier, intended decision label, setting label, or private convenience flags such as `is_stale`, `is_independent` or `supports_requirement`.

The model need not receive evaluator policy IDs or the oracle's candidate list. However, the oracle must not exclude an alternative using a substantive assumption that is absent from the public task semantics. Unknown authority, validity or origin remains unknown. Silence and mere absence of an edit are not proof of approval. Any synthetic completeness convention for an explicit review must be stated publicly and reviewed before the run.

Generator intention and oracle result are checked against each other. Intended labels do not drive the oracle. An empty admissible set, an unjustified label or a true policy incompatible with the constructed evidence is a material-generation failure. Stop and repair it before live execution. Preserve failed generation records. Do not quietly redraw seeds to achieve a preferred difficulty.

The oracle is ground truth within a finite synthetic model, not proof that every real-world explanation has been excluded. Independently authored small fixtures and human review are required because agreement between a generator and its own tests can conceal a shared error.

## Arms and execution

| Arm | Available information and processing |
| --- | --- |
| A | Current task, initial configuration and shared execution contract |
| B | The same inputs plus the full corresponding history at generation |
| C | Two preparation calls over that same history, followed by generation using the retained applicable guidance |

Keep C's strong direct construction and review procedure from v0.3 round 2. It may examine alternative explanations, counterevidence, provenance and scope. Freeze its two-pass instructions before live execution. Changes required for the new record representation are documented; do not remove its existing capabilities.

C's preparation sees no future task, future answer or evaluator truth. Generation receives the same configured baseline as A and B and only the applicable retained guidance. Rejected and unresolved candidates do not become executable instructions. Preserve both preparation responses for analysis.

All arms use `gpt-6-sol` with medium reasoning through the existing transport. Use identical generation contracts and canonical operation semantics. B and C have access to the same history, but the procedures deliberately have different call and token costs. Do not describe this as equal computation.

No arm asks employees questions, acquires new human answers or blocks a task for clarification. Uncertainty remains in the preparation record. For these synthetic tasks, retaining the configured baseline is the registered default where an update is not warranted. This is not a deployment policy for uncertain professional work.

## Measurement

The primary outcome is C's warranted diagnostic decision rate per setting, always out of four planned diagnostic attempts. Show all individual cases and all three regimes. Report B beside C as a history-informed reference and A's world-field compliance as a history-free reference. A's information-relative warrant score is not directly comparable with B or C and must not be presented as recovery of hidden requirements.

Reuse v0.3's separation of actual field values, executed rule effects and declared decision labels. A correct decision requires a completed deliverable for the correct task, no employee question, execution consistency and an action within warranted scope. Missing or invalid outputs fail. A contradictory `apply` or `keep` label remains a separate diagnostic rather than erasing an otherwise correct actual effect.

Retention earns decision credit only where the oracle establishes resolved retention or unresolved disagreement requiring the registered default. An always-keep policy fails warranted-change cases. Correct behavior alone does not show that the model understood its justification. Report retention basis separately using C's candidates, notes, evidence references and preserved uncertainty. Empty preparation or a lucky unchanged answer must not be described as successful requirement inference.

Assess candidates at the level of their observable policy consequences and scope, not exact candidate wording or a preferred decomposition. Separate contradictory explanations from unresolved explanations. A narrow supported rule plus an explicit unresolved remainder can represent the same knowledge as another decomposition. Merely naming a record establishes traceability, not semantic grounding.

Report actual-world field compliance independently of warranted action, both per required field and per complete task. Keep control regressions, task completion, unsupported changes, missed warranted changes, scope errors, evidence traceability and declared-label inconsistencies visible. Do not create a weighted aggregate score.

### Secondary candidate-level content errors

Amendment 2 adds the proportion of C preparation candidates with at least one content error per setting. Assess unsupported adoption, scope errors, spurious evidence and obsolete evidence by observable policy consequences over the registered scope probes and by public evidence provenance. Count a candidate only once in the numerator even if it has multiple error tags. A candidate may be erroneous even when the final diagnostic decision is correct.

Report C1 and C2 separately, with C2 as the final-preparation summary. Never pool the same candidate across both stages as independent evidence. Show error count, candidate count, unassessable count and preparation completeness, alongside each history's rate and the mean of defined history rates. Candidate counts are model-controlled and candidates are dependent. A missing preparation is not an error-free candidate set, and an empty candidate set has an undefined rate rather than zero. Preserve technical or unassessable cases separately and do not silently classify them as content errors. Deterministically confirmed errors form a lower bound where semantic attribution remains pending.

Rejected or unresolved hypotheses are not mistakes merely because they would be unsafe to adopt. Their stated evidential status must be checked against admissible policy consequences. Narrow valid decompositions must not be penalised for omitting an author's preferred wording. This secondary outcome is excluded from the headroom criterion.

### C error taxonomy

Audit every failed C diagnostic and every failed control. Assign one primary cause per case, with optional secondary tags. Use the two preparation artifacts and final execution to locate the failure.

| Primary cause | Definition and examples |
| --- | --- |
| Content | An inferential error is supported by the artifacts, such as overbroad or too narrow scope, treating copied evidence as independent support, using obsolete evidence, adopting a distractor or missing a warranted change |
| Technical | An invalid field or format, a correct stated rule encoded with the wrong operator, transport failure, or failure to execute otherwise correct guidance |
| Mixed | Both an independently observable inference error and a technical defect contribute |
| Unresolved | Available artifacts do not justify an attribution |

A well-formed rule with the wrong evidential scope is a content error. A format failure without interpretable reasoning is not evidence of a content error. Do not silently repair outputs to obtain a category. Deterministic checks identify mechanical defects; semantic attribution may require human review. Preserve raw observations, provisional labels, actual reviewer responses and any disagreements separately. AI-assisted attribution is not independent human validation.

The prespecified headroom criterion is C diagnostic accuracy at most 70 percent and at least 60 percent of its diagnostic failures classified as content errors. Controls do not enter this gate. Mixed and unresolved cases stay in the error denominator and do not count as content in the conservative numerator. Show mixed-inclusive sensitivity separately.

With four diagnostics, at most 70 percent means at most 2/4 correct. Two errors require two content errors, three require at least two, and four require at least three. Unknown or disputed attribution makes the headroom classification provisional unless the criterion holds under every admissible attribution. This is an exploratory flag, not a validated difficulty threshold or significance test. It must not be relaxed after results are known.

## Token accounting and conditional amortisation

Log reported input, output, cached and reasoning-token fields where available for every actual call. Total reported tokens are input plus output. Cached and reasoning fields may be subsets and must not be added a second time. Missing usage is unknown, never zero.

For each history, let P be C's two preparation calls' total tokens, b the mean B generation tokens and c the mean C generation tokens across its diagnostic and control. The conditional projection is B(N) = N*b and C(N) = P + N*c. If b > c, the first integer N for which C is strictly lower is floor(P / (b - c)) + 1. Otherwise there is no finite token break-even under these assumptions.

Show diagnostic-only, control-only and the registered 50:50 mix as scenarios. No additional live tasks are needed. Scenarios are not confidence intervals. If metering is incomplete, do not manufacture a point estimate. Report failures and quality beside resource use; lower token use at worse outcomes is not equivalent efficiency.

This extrapolation assumes unchanged future task composition, reusable guidance, no new preparation and no growing-history or maintenance costs. Two future tasks per history cannot validate those assumptions. Report token amortisation, not monetary ROI, latency savings or enterprise rollout acceleration. A monetary estimate would additionally require an explicit pricing model and a justified treatment of caching.

## Separation, sealing and leakage protection

Development and human-review examples use a separate seed namespace from the 24 live histories. Export one development history with truth per setting for Milad's review. Those six examples are not scored live cases.

Before the live run, freeze this protocol, the actual human-review record, allocation manifest, generator, oracle, evaluator, prompts, model settings, seed registry and call schedule. Hash and snapshot all required sources. Then generate fresh live histories without using their outcomes to tune anything. Seal histories and all C preparations before generating or releasing future tasks. Preparations cannot inspect future task files or truth objects.

Use a model-input allowlist and leakage tests. Exclude evaluator objects, scenario labels, intended regimes, difficulty labels and hidden policy IDs from every payload. Verify that the live transport exposes neither evaluator files nor future tasks through auxiliary tools or its working directory. A prompt instruction alone is not sufficient isolation. Halt if the transport cannot enforce or audit the required boundary.

The shared authoring templates are known during development, but final instances and outcomes are not. This is an exploratory mapping set, not an untouched confirmatory benchmark. Any v0.5 mechanism informed by it needs fresh evaluation data.

Preserve each raw response, exact prompt, source binding, seed, execution order, usage report and error. No selective retries, automatic answer repairs, substituted histories or favourable-output selection. Every planned task remains in its denominator, including tasks blocked by failed preparation. A run stopped early is reported as incomplete.

## Offline checks and human review

Before requesting live approval, complete the following without model calls.

* Unit tests for seeded generation, regime allocation, world-policy consistency and oracle-derived labels.
* Independently authored fixtures for warranted change, resolved retention and ambiguity, including counterexamples to tempting generalisations.
* Metamorphic checks for copies, irrelevant additions, consistent identifier renaming, alternate raw/interpreted rendering and visible validity changes. Copies must not create independent support. Removing a decisive witness must not make the admissible set narrower.
* Tests for rendering, field compliance, scope boundaries, no-op decisions, unresolved candidates, retained-baseline claims, taxonomy accounting and amortisation arithmetic.
* Leakage and isolation tests, future-task ordering tests, sealed-source checks, denominator preservation and budget-stop tests. The v0.4 runner must reject D.
* A full 192-call offline mock schedule and failure-injection runs. Mock outputs use public inputs only; do not feed the oracle's answer to the mock and call that model success.
* Six readable human-review examples, one per setting, showing public records, competing explanations, oracle reasoning and both future-task obligations. Record Milad's actual response and required revisions. Prior v0.3 approval does not approve these new materials.

Human review at this stage is an author-level check of synthetic assumptions, not independent field validation. Export blinded live-output samples and a separate key for later spot checks, and flag any review that is still pending.

## Live budget and stopping

The planned schedule contains 48 C preparation calls and 144 generation calls, totalling 192. The hard call cap is 200. The unused eight slots are not permission for replacement attempts, extra cases or retries.

Stop scheduling calls once reported input-plus-output tokens reach 6,000,000, checking between calls. This is an audited stop threshold, not a strict per-call cap. The final in-flight call can cross it. Log that limitation and any transport-level reconnects separately from logical completions.

A failed C preparation blocks its dependent calls without removing their task attempts from the analysis. Unaffected planned calls may continue after an isolated response failure. Stop the whole run for uncertain usage accounting, integrity failure, systemic transport failure or the budget threshold. Do not restart or replace an interrupted live run without an explicit decision recorded alongside its incomplete results.

The named backend and limits are planning parameters, not live authorisation. Ask Milad after offline verification and human material review, before the first live call. No purchase, paid API migration or extra budget is authorised here.

## Implementation plan and preservation

Work on branch `pilot-v04`. Preserve all existing worktree changes. v0.1 to v0.3 remain unchanged, including protocols, prompts, scores, sealed snapshots and original reports.

Implement the isolated package under `pilots/v04/reflectai_v04`. Reuse compatible v0.3 A/B/C contracts, rendering and evaluation semantics through narrow, version-bound dependencies. Do not reuse its four-arm orchestration or change its historical source files. v0.4 needs its own configuration, generator, oracle, A/B/C-only runner and reporting layer. Avoid opening D-specific files while resolving dependencies.

Review implementation in four steps after protocol approval.

1. Generator, separated truth objects, warrant oracle and small hand-checked fixtures.
2. A/B/C execution adapter, deterministic evaluation, error-audit records and token accounting.
3. Leakage and sealing safeguards, unit tests, offline mock run and six human-review exports.
4. After the separate live approval, the one registered difficulty run, sealed outputs and report.

The final report at `pilots/v04/DIFFICULTY_MAP_REPORT.md` will show all settings and cases, failures, regime-specific decisions, world compliance, control regressions, error attribution and its review status, token projections and limitations. It will not claim professional quality, enterprise ROI, recursive self-improvement or a benefit of D.

## Decision after the map

If errors mainly concern finding discriminating witnesses among conflicting records, v0.5 may investigate hypothesis-guided search with a query budget. If they mainly concern provenance, version boundaries and persistent use of obsolete evidence, a temporal evidence registry may be the better candidate. Both are prospective hypotheses, not mechanisms implemented or selected in v0.4.

If failures are mainly technical, repair the interface in a separately documented iteration before interpreting them as an inference opportunity. If C remains at ceiling, report that the tested conditions did not establish headroom. Do not force a recommendation for D. Any selected v0.5 design needs its own protocol, frozen mechanism and fresh cases.

## Approval record

Protocol approval: Milad Morad, 29 September 2026, with amendments 1 and 2.

Amendment 3 implementation approval: Milad Morad, 29 September 2026, with supplements 1 and 2 and explicit counterfactual clarification. Actual response: "Ja, getrennt prüfen und so implementieren."

Amendment 4 approval (model change to DeepSeek-V4-Flash-0731 via FHGenie): Milad Morad, 30 September 2026. Actual response: "Amendment 4 freigegeben, Harness für den Vertragstest umsetzen, aber reasoning auf stufe high setzen"

Amendment 5 approval (error tolerance with limit, pinned PowerShell 7, reasoning high, output limit 32,768): Milad Morad, 30 September 2026. Actual response: "Amendment 5 freigegeben, B2 mit neuem Vertragstest. folge B2, wobei es über fhgenie keine token limits gibt."

New material review: pending.

Live-run approval: Milad Morad, 30 September 2026, for configuration `23477ae8e2f511227f84cdcb1acb45f264b1d15ca704d8e628b0cdd145678829` (DeepSeek-V4-Flash-0731, reasoning high). Actual response: "Live-Lauf freigegeben, ausführen." The run completed all 192 calls (seal `7afab956742071b0c5ddd8d696e854630a2a6f25945a32d34e6ece3dddbb8594`). Earlier consumed approvals for the gpt-6-sol attempt and the FHGenie probes remain recorded separately.

C failure attribution: Milad Morad, 1 October 2026. Two S4 failures unresolved (`baseline_polarity_inverted`), one S1 failure content. Headroom is not met in any setting, provisional in S4. See [DIFFICULTY_MAP_REPORT.md](../pilots/v04/DIFFICULTY_MAP_REPORT.md).

AI-assisted planning and internal review do not fill any of these fields.
