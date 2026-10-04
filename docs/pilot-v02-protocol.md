# Synthetic pilot v0.2 protocol

Written 28 September 2026, before implementation or v0.2 model outcomes.

## Question and hypotheses

Can structured, grounded reflection recover omitted contextual requirements from work evidence, and improve subsequent outputs beyond direct use or direct adaptation of the same evidence? This is a measurement and feasibility pilot. It does not establish enterprise effectiveness or recursive self improvement.

The primary comparison is grounded reflection versus direct adaptation. We hypothesise better precision of retained requirements and less adoption of distractors, without losing recoverable requirements or increasing unnecessary deferral. Direct adaptation may perform equally well or better. A null result remains informative. Comparisons with an unchanged agent assess the combined value of evidence and processing, not reflection alone.

## Materials and sample

All names, documents, feedback, and execution records are synthetic. No proprietary or industry-partner data are used. Three task families cover recruiting briefs, sales handovers, and research notes. Each family has requirements absent from the initial agent configuration and historical evidence containing accepted and rejected outputs, corrections and execution records. Evidence includes individual preferences, conflicting feedback, context boundaries and transient technical failures. Model payloads omit author labels such as gold requirement, distractor and expected decision.

Development histories support some requirements, leave others unresolved, and do not license arbitrary generalisation. The oracle distinguishes an actual synthetic world rule from whether available evidence justifies learning it. Unidentifiable rules are not counted as missed recoverable requirements. Current explicit task instructions take precedence over historical patterns.

The initial design uses six calibration tasks, six validation tasks and twelve final tasks across three families. Final tasks cover in-scope transfer, out-of-scope boundaries, explicit overrides and insufficient context. Two repetitions independently prepare guidance and generate outputs. Repetitions are not independent organisations. Histories necessarily share some requirements with future tasks; case instances, source identifiers and documents are separate. This is within-family transfer, not proof of generalisation to unseen occupations.

## Conditions and information access

All arms share the generation model, configuration, public output schema, current task and baseline instructions. Every request starts without previous model-session state. A has no historical evidence by design. B, C and D receive the same full historical pool for the relevant family, without oracle information.

* A, no adaptation, uses the initial configuration and current task.
* B, direct evidence, receives the historical pool with every current task, without a persistent patch.
* C, direct adaptation, uses two preparation calls to develop and review reusable guidance by any appropriate method. It is a strong baseline and is not prohibited from noticing conflicts or scope.
* D, grounded reflection, uses two preparation calls. The first proposes requirements with references, alternatives and scope. The second searches the same pool for counterevidence and revises or withdraws requirements. It receives no extra evidence or oracle access.

C and D emit the same compact structured rule representation, including a decision to adopt, clarify or defer. A common renderer converts applicable rules into context instructions and unresolved fields into clarification cues. Free-text notes are recorded but never used as instructions. D additionally supplies grounded hypotheses using the existing evidence contracts. Both use the same downstream applicability handling. D's reference checks establish traceability, not semantic truth. Record raw predictions as well as retained instructions, so filtering cannot conceal inference errors. This comparison evaluates the full prompted procedure, not an isolated internal reasoning mechanism.

## Budgets and model access

Preparation budgets are equal for C and D. Generation ceilings and settings are equal for all arms. A and B do not consume artificial preparation calls merely to equalise counts. Preparation cost is amortised over the same fixed number of future cases and reported separately. Input, output, reasoning and cached tokens are recorded when available, without double counting. Missing usage or unavailable costs stay unknown. Failed calls count towards the budget. There are no silent retries, output repair, selective resampling or free clarification calls.

The runner enforces call limits and stops further calls after a reported token limit is exceeded or the backend records a failed call. A stopped downstream stage retains every planned case in its report, counting missing outputs as failed attempts. There is no post-hoc completion of selected cases. An incomplete preparation cannot advance to validation. A backend without a provider-enforced per-call token ceiling cannot guarantee a strict token cap. Such runs must be labelled call-budget-controlled and token-audited, not compute-matched. Backend capabilities and model budget must be agreed with the user before any live call. Real backends require explicit opt-in and an explicit model. Credentials are never included in configuration, prompts or source code.

## Measurement

Primary outputs are structured work decisions and small deliverables. Rules consist of typed observable predicates, values and contextual scope. Models see generic schema vocabulary, not the list of correct rules, hidden rule IDs or permissible gold values. Evaluators match canonical predicates and values, not exact free-text explanations.

Preparation-level precision and recall compare C and D's adopted rules with the recoverable gold set. Duplicate predictions do not inflate recall. Supported local exceptions, such as a change confined to a specific commission or a correctly scoped other-workflow rule, are counted separately and excluded from the primary precision denominator and recall target. An overbroad rule with the same body remains an error even if a second, properly scoped rule is also present. Unsupported adoption, including adoption of unidentifiable rules, counts against precision. Abstention and empty predictions have explicit denominators and are not treated as perfect precision. Scope is evaluated separately on in-scope, out-of-scope and unknown-context probes, recording overgeneralisation and excessive restriction. Report all predicted rules before traceability or applicability filtering as well as retained rules afterwards.

Downstream deterministic checks evaluate requirement compliance for all four arms on the same tasks. Report per-rule binary results, per-task proportions and all-requirements-passed counts. Report checks for hidden requirements separately from explicit task requirements and generic structure. This prevents easy checks from hiding failure to learn missing context. Out-of-scope cases measure regression and distractor adoption. Invalid or missing model outputs remain failed attempts in the denominator.

Clarification and deferral are assessed through the requested action and the relevant missing context field. Both missed necessary clarification and unnecessary abstention are errors. The first pilot does not answer clarification requests or grant extra evidence; it measures the decision to ask or defer and reports task completion separately. Unresolved cases do not require guessing the hidden world rule to pass. This limits conclusions about interactive information acquisition.

Deterministic checks are primary. No LLM judge is needed for the default experiment. An optional later semantic assessment would require a separately configured different-family judge, anonymous pairwise outputs, balanced order and a prespecified rubric. It cannot replace failed primary checks. Export a stratified, blinded sample for later human review with a separate mapping. Do not claim human validation before reviews exist.

## Calibration and stopping rule

Before the main run, run A on the calibration set with the selected live model. Target approximately 30 to 70 percent downstream compliance, reporting hidden-rule, explicit-rule and family-level results separately. The target is a ceiling/floor diagnostic, not evidence of real-world realism. Offline mock scores cannot certify calibration.

Allow at most two documented calibration rounds for this pilot version. Changes may adjust evidence ambiguity, context distinctions or task difficulty, but cannot select tasks because D beats C. Preserve every round and its inputs. Freeze one version before final evaluation. If the band is not reached, report the failure to calibrate; do not silently continue labelling the pilot calibrated. Validation data may be used for development checks before freeze. They never substitute for final data.

## Test separation and freeze

Development and calibration/validation data are available during implementation. Concrete final tasks and their oracle records are generated only after code, protocol, prompts, model configuration and prepared C/D artifacts have been frozen. Use a separate final seed that is not available to preparation. Retain it for audit only after freeze. Test generation is scripted without displaying tasks to the developer before the final run.

Preparation loaders accept histories only. Generation loaders accept task inputs and approved context artifacts, never oracle files. Evaluation loads gold records in a separate stage after outputs exist. No function loads every split into a shared prompt. Freeze manifests bind code, configuration, histories, development tasks, prompts and prepared artifacts. A changed dependency blocks final execution. IDs and content fingerprints guard against duplicated or relabelled cases. Tests use sentinel values to detect leakage into preparation and generation payloads.

These are workflow and access-path controls, not a security boundary against a machine owner deliberately reading files. Public synthetic fixtures are not permanently secret. Final outcomes never feed update selection. After viewing final outcomes, further tuning requires a new labelled study version and fresh held-out instances. Never replace the original result.

## Analysis and reporting

Report case-level paired outcomes for all four arms, with D minus C as the primary contrast. Separate preparation variability, downstream compliance, scope errors, distractor adoption, appropriate abstention, failed calls and actual costs. Do not treat checks or repeated generations as independent participants. Use descriptive results rather than significance claims from this small purposive sample. Do not select a winning repetition.

Report mock origin in the setup, every model-call record and prepared artifact, the review sample and results report. Stage summaries inherit their origin from the run setup. Mock data exercise infrastructure and are not experimental evidence. Report limitations including synthetic author-designed rules, restricted predicates, small sample, shared model family for generation, model nondeterminism, no human evaluation, no real tool execution and only one prepared adaptation per repetition. The pilot does not yet establish repeated recursive improvement.

## Reproducibility and protected history

Version prompt files and configuration; preserve seeds, code hashes, installed Python and Pydantic versions, requested and returned model identifiers where available, request/response records, status, usage and timings. Use fixed seeds for generation, ordering and blinding; do not claim deterministic model sampling when a backend cannot provide it. Refuse to overwrite existing experiment stages. Offline tests must not access a live backend.

Keep pilots/hr_v01 and its results untouched. Its frozen manifest also covers models.py, workflow.py, codex_backend.py and the original HR evidence file. v0.2 therefore adds modules and imports the existing contracts without changing those frozen files. This protocol is frozen with each run; amendments must be documented before the corresponding outcomes are observed.

## Transport amendment, 28 September 2026

The initial live attempt was rejected with HTTP 400 before producing any model answers. A v0.2 adapter now derives a strict transport schema, explicitly requires every property and encodes scope mappings as attribute/value lists. It decodes those lists back into the existing Pydantic contracts without changing their meaning. Raw wire responses remain available alongside canonical responses. A failed call now stops the stage immediately to avoid repeating an invalid setup. These changes are technical corrections made before any valid v0.2 model outputs. Earlier attempts and their source snapshot remain preserved. See pilots/v02/LIVE_RUN_NOTES.md.

## Calibration amendment before round 2, 28 September 2026

The first completed scientific calibration produced 7 passing checks out of 48 (14.58%). All 12 responses were structurally valid. Six asked for unavailable decision criteria; six delivered partial records, and none recovered the hidden conventions. This is below the target band. It also exposes two measurement issues. The original calibration included only tasks requiring private knowledge unavailable to A, and literal case-sensitive matching penalised harmless capitalisation in summaries.

Before the second and last permitted calibration round, the calibration composition is fixed to one fully specified current-instruction anchor and one withheld-requirement transfer case in each family. Histories, validation tasks, final-task layout, model settings and experimental conditions remain unchanged. Three successful anchors plus appropriate abstention on three transfer cases would yield about 50% pooled check compliance by construction. The 30–70% band therefore checks mixed task execution, not intermediate difficulty of hidden-requirement learning. Anchor and transfer outcomes are reported separately. Failure to reach the band again stops the planned main run.

Only generic summary containment ignores letter case through casefolding. Identifiers, structured decision values, other predicates and requirement inference retain exact matching. This applies uniformly to every condition and phase from round 2 onwards. Round 1 records and scores remain unchanged in their archived version. No C/D comparison or final outcome has been observed when choosing these changes.

The label unnecessary_abstention counts asking or deferring despite complete task metadata. For A, private conventions are absent from its evidence, so such a request may nevertheless be epistemically justified. Interpret this as incomplete workflow execution, not as an unconditional judgement about whether asking was reasonable.
