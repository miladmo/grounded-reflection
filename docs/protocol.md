# Executable protocol v0.1

## Data flow

`WorkEpisode` preserves the task, context, evidence records, provenance and explicitly missing information. A `Hypothesis` carries an interpretation, scope, supporting references, counterevidence, alternative explanations and unresolved questions. A `CandidateUpdate` is a specific context instruction with a predicted effect and optional blocking questions. A `PairedEvaluation` compares the baseline and that candidate on the same validation case.

Hypotheses and candidates are authored in the supplied example. Their semantic correctness is not scored by the current library. General unresolved research questions do not prevent validation. Candidate-specific `blocking_questions` defer selection; their classification is supplied by the author or future inference backend, not inferred by the present checks.

## Scope semantics

`scope.match` is a conjunction of constraints. For example, `role=["hr"]`, `audience=["experienced_specialists"]`, `channel=["linkedin"]` and `project=["atlas"]` must all match. Multiple values within one attribute are alternatives. A missing required context attribute returns `unknown`; a supplied incompatible value returns `mismatch`.

A candidate may narrow its hypothesis scope or add restrictions; it may not remove a restriction or add allowed values to it. These checks compare declarations. They do not infer the appropriate scope from evidence or verify that the natural-language instruction obeys its declared scope. Scope checks also do not establish validity over time or across related contexts.

## Evidence and splits

Evidence references contain an episode ID, record ID and exact nonblank quote. References are resolved against development episodes. Unknown IDs, missing quotes and non-development references fail. The method does not certify that a quote supports a claim. Repeated quotations do not constitute independent observations.

The split manifest requires globally unique, disjoint IDs. Every episode in a selection bundle must be declared as development; every paired evaluation must be declared as validation. An evaluation with a final-test ID is rejected even if its own split label says `validation`. Candidate ID, candidate digest, baseline version, metric and context must match the proposed comparison. Bind each rating to `digest(candidate)` from `grounded_reflection.workflow` when evaluating the candidate; changing the patch or its scope invalidates the earlier records.

These guards prevent straightforward mixing of declared records. They cannot detect relabelled duplicates, shared source documents, task-family overlap, temporal leakage or access to test outcomes elsewhere. A research experiment must group related data before splitting, restrict access to final cases, and retain final results outside the adaptation process. Public fixtures are not a secret held-out benchmark.

## Selection policy

The caller supplies paired ratings on a `professional_quality` scale normalised to [0, 1], explicit remaining critical-error counts and active human-revision time in seconds. Missing error counts are not assumed to be zero. Record the evaluator and origin (`human_rating`, `programmatic_check`, `model_judge` or `fixture`). The library does not collect, authenticate or calibrate these observations.

The default policy is a **demonstration setting**, not a research sample-size calculation: at least two validation cases, mean quality gain at least 0.05, no per-case quality regression, no remaining candidate critical errors and no increase in mean human effort. Supply a JSON `SelectionPolicy` with `--policy` to change the configurable thresholds. Define the scoring rubric, thresholds, power analysis and treatment of uncertainty before an actual experiment.

Insufficient observations or explicit blocking questions defer the candidate. Broken references or scope broadening reject it. If any acceptance condition fails, the baseline stays active. Passing produces a deterministic context version and an accepted policy decision. This is not a significance test or a claim of generalisation; repeated candidate search can overfit the validation set. Out-of-scope transfer and longitudinal stability need separate experiments.

## Outputs and trust boundaries

Each decision includes SHA-256 digests of the full evidence bundle, candidate and ordered evaluation records, plus the applied policy and baseline. A matching accepted candidate can be exported as `context.json`; records labelled `fixture` cannot produce an exportable update. Export never edits an agent or deploys code.

The checks trust the caller's input labels and ratings. They are not an authentication or adversarial-security boundary: a forged decision, falsely labelled rating or copied final case cannot be made trustworthy by a digest. Persist source records and decisions together for reproducibility. An integrating application must recheck applicability, instruction precedence and its own access controls. No raw-data anonymisation or secure data store is included.

## Versioning

Package version `0.1.0.dev1` and schema/protocol version `0.1` identify the current development snapshot. APIs may change. Version identifiers refer to the baseline label and candidate content; they do not hash model weights or establish a reproducible model runtime. The experimental CLI backend records requested model/settings and prompts, while server-side snapshots and sampling remain uncontrolled; a broader agent runner will also need adapter and environment versions.
