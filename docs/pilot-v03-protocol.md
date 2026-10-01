# Pilot v0.3 protocol

29 September 2026. The initial design preceded implementation. The amendment below follows the first live calibration and precedes the second. Before the first calibration, Milad Morad confirmed the four conceptual inference rules as plausible under the stated synthetic assumptions. This is an author-level rubric check, not independent validation of every generated record or human evaluation of model outputs. The scientific freezes remain pending. The accompanying [eight scenario cards](../pilots/v03/SCENARIOS.md) are development examples with evaluator answers, not the final dataset.

## Amendment before calibration round 2

Round 1 completed 64 calls and failed its registered gates. Its complete sources, prompts, responses and scores remain sealed in `pilots/v03/runs/calibration-r1-sol-medium-20260929`. The [calibration report](../pilots/v03/CALIBRATION_REPORT.md) records the subsequent audit. None of the revisions below changes those original scores or retrospectively authorises a main run. D has not been inspected or run during calibration.

The second and final calibration round uses seed 3317, order seed 3318, the same model and reasoning settings, 64 calls and a 2,000,000 reported-token ceiling audited between calls. The original gate thresholds and case counts remain unchanged. All changes described here apply prospectively and symmetrically to the conditions.

The primary update measure follows the actual effect of executable rules and rendered fields. A mismatching declared `apply` or `keep` label is retained as a separate diagnostic. It cannot by itself erase a justified actual update or a correct completed output. Missing responses, incorrect task identity, employee questions and incomplete deliverables still fail. Execution consistency, supported scope and agreement with adopted preparation remain necessary for update credit. World-field compliance requires the correct fields in a completed output for the right task without employee questions, independently of rule and decision-label metadata. Strict output validity remains separately visible.

All stages receive the same versioned operator contract. Rules act on the complete configured baseline. `append_fact` performs literal concatenation and never deduplicates an existing suffix. A rule that leaves the baseline unchanged may be recorded with `keep`. Public field definitions include canonical value conventions needed before preparation, including the `checksum_check` marker. No evaluator policy or task answer is provided.

The Sales contrast now tests a new case for an already observed reviewer in both pair members. The conflicting-history member supports retention for that reviewer. The consistent-history member supports a change for the observed reviewers. For the latter, both a shared workflow convention and an observed-reviewer convention remain admissible. A completely new reviewer is therefore an unresolved scope boundary, not a compulsory generalisation target. Private probes include all observed reviewers and a new reviewer. The hidden world may have a broader convention than the evidence warrants. This narrows the inference claim while preserving four change diagnostics and four retention diagnostics.

Candidate statuses describe evidential support for a contextual hypothesis. Rejection means contradiction, not simply withholding operational permission. Partial support and unresolved remainder can be represented separately. Secondary candidate-coverage scores remain dependent on the bounded hypothesis representation and must be inspected alongside the complete candidate set. They do not establish that an omitted broad candidate means the model ignored every corresponding uncertainty.

The original conceptual human review is carried forward transparently. The same four principles apply, and the Sales change removes an unsupported extrapolation. Milad's instruction to continue authorises implementation and execution, but it is not recorded as a new independent review of revised records. The new source binding documents the amendment and its automated checks separately from his original confirmation. No human output assessment is assumed. If round 2 fails, the planned main comparison stops, with both rounds retained.

## Scientific question

When does situated work evidence justify learning a previously unstated requirement, and when does that learning improve an agent's next decision?

The primary comparison remains grounded reflection (D) versus strong direct adaptation (C). C constructs candidate guidance and then reviews it. D first produces an uncommitted hypothesis draft, then audits the draft before any adoption decision. The directional hypothesis is that this staged procedure makes more justified update decisions without missing warranted changes. C may also reason about alternatives and counterevidence. Equal or worse D performance is a valid result. This comparison concerns complete procedures, not reflection versus an inability to reflect, an isolated cognitive mechanism or recursive improvement. Employee questions and human answers are outside the experiment.

The [v0.2 result](../pilots/v02/REPORT_en.md) motivates this design. Both procedures recovered the target rules, but D sometimes turned uncertainty about rejected alternatives into current-task blockers. Field-label and scope-representation errors also distorted measurement. Correcting those errors is engineering work, not new evidence of a reflection benefit. Preserve v0.1 and v0.2, including their original scores and source snapshots.

## Repair before experiment

Use one public field dictionary and one execution interface across conditions. Test equivalent field representations, scope containment, unsupported generalisation and leakage of unresolved candidates into instructions. Task family and work role must be distinct concepts, with some fixtures where they differ. Do not infer that they are universally interchangeable from v0.2.

Separate candidate status (`adopt`, `reject`, `unresolved`) from the applied update decision (`apply`, `keep`). An unresolved candidate remains labelled as unresolved, with its alternatives and evidence gap. A rejected candidate cannot become an instruction. C and D use the same rule renderer and validation, and all arms expose the same applied-decision fields. Evidence-reference checks are symmetric and establish traceability only. An employee question is a protocol deviation, never a successful outcome.

The two preparation calls may examine and search the same fixed historical pool for support and counterevidence. No arm receives extra records, invented answers or human feedback during the run. If the pool cannot resolve a candidate, record which observations would discriminate the alternatives and retain the applicable configuration. Searching additional future records is a later extension, not a capability evaluated here. Evidence gaps are research outputs, not runtime questions or blocking instructions.

Verify repairs offline on v0.2-derived regression fixtures, including correct retention under uncertainty and correct application of supported changes. These are development cases. Do not report improvement on them as fresh efficacy evidence.

## Materials and units

Use four paired scenario structures spanning HR, sales and research. Each pair contains two contrasting histories, giving eight history variants. Each variant has two future tasks: one separating rival explanations and one stability or boundary control. Current task inputs are held equal within a pair where specified. Histories include corrections, revisions, accepted/rejected artifacts, retrieval and execution records. Everything is synthetic.

The pairs test identifiable versus confounded requirements, a person's preference versus a scoped work requirement, a transient technical incident versus a persistent routing change, and narrow versus broader scope supported by counterevidence. Acceptance alone is not treated as a universal rule. Historical provenance, independence, authority and current validity matter within the stated synthetic operating assumptions.

Use three end-to-end repetitions. Each independently prepares C/D and generates one answer per future task and arm. This is not three generations for each of three preparations. The eight variants, sixteen tasks and repetitions are dependent observations organised into four designed contrasts, not a population sample of organisations.

## Truth, warrant and update decisions

Keep three evaluator objects separate from model inputs.

1. The actual policy of the synthetic world.
2. The candidate policies admissible under the available evidence and explicit current instructions.
3. The observable obligations for the current output or action.

Admissibility is relative to a prespecified, bounded hypothesis class. It is not proof that every real-world explanation has been excluded. Models receive generic field and rule vocabulary, not the author-labelled hypotheses or answers. A uses current-task information only. B/C/D are assessed against the same allowed history pool, even if preparation discarded useful information.

Apply a contextual change only within the scope warranted by the evidence. If multiple admissible policies disagree for a context, make no unsupported update there, preserve the alternatives and execute the configured baseline for the synthetic task. Partial rules in the region where those policies agree may still be retained. Do not confuse this experimental retention default with proof that the baseline satisfies a hidden policy or with permission to deploy an uncertain output in real work.

A correct decision to keep the configuration can coexist with failed actual-world compliance. A coincidentally correct output after an unsupported update does not earn warrant credit. These are different outcomes, not alternative ways to earn one task-success point. No evaluated agent asks employees questions, receives answers or pauses the task to acquire human input.

## Conditions

| Arm | Access and processing |
| --- | --- |
| A | Current task and initial configuration, without history |
| B | Same current task plus the full corresponding history |
| C | Direct candidate guidance with adopt/reject/unresolved decisions, followed by strong review against the same history |
| D | An explicitly uncommitted hypothesis draft, followed by a counterevidence audit that determines status and scope |

C may reason about alternatives, authority, conflicts and scope, including reviewing records for additional evidence. D receives no additional records, evaluator access or execution safeguard. Report raw and retained candidates. B/C/D have equal access to evidence, not necessarily identical prompt lengths. Initial configuration and generation settings are shared. B may use evidence for the current task but has no persistent preparation artifact.

D's first response has a separate `ReflectionDraft` contract. Its candidate status must remain `unresolved` until the second pass. This means procedurally uncommitted, not epistemically unidentifiable. Do not score D's first-pass statuses against final adoption targets. Compare C2 and D2 using the identical final `Preparation` contract and evaluator. Preserve drafts as process artifacts. C's ability to investigate evidence is unchanged.

## Measurement

The primary measure is D minus C in justified update decisions on the eight diagnostic future probes, four requiring change and four requiring retention. A decision passes when it applies the warranted change at the supported scope or retains the applicable configuration where no update is justified. Derive the decision from the actual applied rule and rendered output. The model's claimed `apply`/`keep` label is a separate consistency diagnostic. Report both diagnostic subgroups separately. The eight stability/boundary controls remain a separate outcome and are not pooled into primary accuracy, where easy retention could conceal missed changes.

Candidate measures use fixed evaluator targets and distinguish unsupported adoption, missed warranted rules, scope errors, rejection and preserved uncertainty. A missing candidate is not automatically a correct rejection. S03 can require learning Mira's local exception while retaining the baseline for the observed reviewer Leon; S07 requires a chart rule while leaving the table unchanged. Score raw and retained candidates, including partial rules supported across admissible explanations. Scope checks apply the deterministic rubric to these existing artifacts, without additional model calls or execution tasks. Evidence-gap descriptions are diagnostic, not a new free-text primary metric.

Report completed structured outputs, compliance with the synthetic world's field rules and partial field correctness separately from update correctness. These deterministic measures do not establish professional quality. A failed deliverable may contain correct fields. Unsupported lucky successes, unintended interventions, logical calls, failures and reported usage also remain visible. Do not combine these into an arbitrarily weighted score or treat a justified non-update as a completed professional task. A's warrant score uses current-task information only, so only its downstream field compliance is directly comparable with that of history-informed arms.

The legacy JSON field `unsupported_lucky_success` means world compliance without verified update credit. It also includes execution or rule-metadata failures. Inspect execution consistency and the recorded errors before attributing such a case to unsupported learning or chance.

Average the three repetitions within each history variant, keeping diagnostic and control outcomes separate. Report all eight variant summaries, all four paired evidence contrasts and every repetition. Use descriptive differences, not significance claims. Improved update decisions must be interpreted alongside downstream utility and missed opportunities to improve.

## Review and calibration

Before live calibration, audit all eight development cards for rival explanations, justified scope, supported partial rules and informative evidence gaps. Record the human check of the author-defined warrant and task rubric. On 29 September 2026, Milad Morad judged all four presented inference rules plausible under their synthetic assumptions. His response was "Alle vier sind plausibel". This conceptual check is separate from employee questioning by the evaluated agent and from independent human output assessment, which remains pending.

Calibrate on separate development instances with A/B/C only, one repetition per round. Preserve eight diagnostic probes, four requiring a supported update and four requiring retention, plus eight controls. Proposed gates are B at least 6/8 correct diagnostic update decisions and C 4–7/8, with C at least 2/4 in each diagnostic subgroup. B and C each need at least 7/8 correct control decisions. These subgroup floors reject an always-keep strategy. Show output completion and actual-world compliance beside decision scores.

Seven diagnostic cases permit an evidence-grounded, world-compliant deliverable. On that fixed subset, B must achieve at least 6/7 warranted, world-compliant deliverables. Separately, its actual-world-compliant outputs must exceed A's by at least two, regardless of whether A's correct outputs were warranted or lucky. Comparing A's warranted outputs would make this utility gate redundant because A cannot warrant a hidden-rule change from current information alone. S02's unresolved diagnostic is outside this recoverability gate but remains in every overall result and failure denominator. Its correct retention decision can still produce a world-incorrect output. Report denominators and outcomes by evidence regime; do not recreate a target band by mixing perfect anchors with unanswerable tasks.

These thresholds are pragmatic headroom checks, not measurement validation. They deliberately select diagnostic difficulty and limit representativeness. Allow at most two documented rounds, without weakening C or inspecting D to select materials. If gates fail, retain the result and stop the planned main comparison. A final ceiling remains possible and must be reported. The scenarios test inference within supplied context vocabularies and stability assumptions, not open discovery of every latent feature of real enterprise work. The [pre-calibration design review](pilot-v03-design-review.md) records these limits and the repairs made before any live v0.3 output.

## Separation and execution budget

Use two freezes. First freeze the protocol, reviewed rubric, generators, counterbalancing, prompts, code, model settings and calibration decisions. Then instantiate fresh final histories with counterbalanced policy triggers and values, not merely renamed documents. Prepare C/D without future tasks. Freeze those histories and all preparations before generating or revealing the future tasks. Only designated cases test an unobserved context combination; others test new instances in known contexts. Author answers, pair labels, difficulty labels and synthetic policy identifiers never enter model payloads.

Pair members may intentionally share a current task. Leakage checks must distinguish this registered contrast from accidental reuse across development and final splits, using history-plus-task identity. Log seeds, source hashes, model identifiers, order, prompts, responses and usage. Preserve all failures and prohibit selective retries, repairs or replacement of unfavourable outputs. Every planned task attempt remains in the denominator; missing or invalid responses fail update and downstream success rather than being counted as justified retention. Incomplete preparation blocks generation. Report a stopped run as incomplete rather than as a fair comparative result.

Retain the v0.2 model and settings for comparability: `gpt-6-sol`, medium reasoning. Main preparation requires 96 logical calls and generation 192, totalling 288. Each calibration round adds 64, so two rounds plus main require at most 416. Token limits and the selected transport configuration must be fixed before execution. This document starts no model calls or purchases. A transport without strict per-call token limits is call-budget-controlled and token-audited, not compute-matched; internal network reconnects must be reported separately.

## Readiness and reporting

The first live calibration is complete and failed its registered gates. The revised implementation must pass offline checks before the remaining calibration round. The code resides in `pilots/v03/reflectai_v03` so the historical `src` manifests remain unchanged. Run registries permit at most two calibration rounds, require every recorded round at F0 and prevent reuse of the final experiment. Sources and raw artifacts are snapshotted and sealed. Offline copies of F1 exercise sequencing but do not constitute a scientific freeze. Export a blinded sample for later human checking and a separate key. Report synthetic scope, selection through calibration, limited hypothesis classes, single-model dependence, no real tool execution and no evidence of enterprise ROI or recursive self-improvement.
