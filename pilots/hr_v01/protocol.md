# HR model pilot v0.1 — protocol before outcomes

This exploratory pilot tests whether a language model can generate traceable, scoped requirement hypotheses from work episodes and whether using its proposed context updates changes performance on new recruiting tasks. It is a first implementation probe; it is not a powered experiment or a validated benchmark.

## Materials and independence

The four development episodes are wholly fictional library fixtures. Only their `episodes` field is passed to preparation or direct-evidence conditions. The curated hypotheses, candidate patches and assessment outcomes in the library example are excluded from every experimental prompt. The model receives no application narrative or proposed answer.

Six new tasks and a rubric are authored by a separate assistant with no conversation history and instructed not to inspect the training fixture, prototype or later model outputs. Tasks cover specialist-role transfer, different audiences/projects and a current-instruction override. They remain synthetic, not independent human observations. Hashes of tasks, rubric, runner, model backend, protocol and supporting library code are frozen before preparation. The task designer receives category requirements; this is purposeful stress-case design rather than random sampling.

## Conditions

1. **Direct evidence:** the generation model receives the current task and the complete historical episodes, with no preparatory call.
2. **Direct adaptation:** one preparation call sees only historical episodes and may use any approach to produce up to 350 words of reusable guidance. The generation model receives that guidance and the current task.
3. **Grounded reflection:** one preparation call sees the same historical episodes and produces up to three typed hypotheses and candidates, including source references, alternatives, scope and blocking questions. Candidate patches combined are requested to stay within 350 words. Formal checks reject invalid references or excessive scope; only eligible, context-matching patches are supplied to generation.

The structured condition tests the combined effect of a structured prompt, representation and deterministic applicability checks. It does not isolate a learned scope algorithm from the surrounding pipeline. A fourth raw-reflection or scope-ablation condition is outside this initial run.

Direct adaptation and reflection use the same requested model, reasoning setting and number of preparation/generation calls. They are **not guaranteed token- or compute-matched**: structured output contains additional fields and all usage is reported. Direct evidence has a longer generation context and no preparation call. The 350-word guidance limit is requested, checked descriptively and never enforced by silently truncating a response. No exact monetary cost is inferred from subscription usage.

## Execution

Use the user's configured `gpt-6-astra` model and `xhigh` reasoning setting via the authenticated Codex CLI. The smoke test only checks transport and structured JSON. Each experimental call starts a fresh ephemeral session with an empty working directory; project instructions, memories, external tools and plugins are disabled for isolation. The CLI retains its own system instructions, so this is a Codex-mediated pilot, not a bare-model API experiment. Tool-use events invalidate a run. Managed security policies are not bypassed.

Record input prompts, schemas, raw JSONL events, final responses, requested configuration, CLI return code, timestamps, duration and available token counts. Exact server-side model snapshot, sampling seed and hidden computation may be unavailable. No answer repair, prompt tuning or selective resampling after observing experimental results. A transport failure is preserved and may require a separately labelled rerun; it is not replaced silently.

Generation order is shuffled with seed 20260915; at most two calls run concurrently. Every condition produces one answer per case. No evaluation task, rubric or judge output is shown in preparation. Evaluation results are not used to choose a candidate or continue an adaptation loop.

## Assessment

Five prewritten criteria use ordinal 0/1/2 anchors: factual fidelity, task completeness, audience fit, work specificity and instruction/context fit. A fresh model call assesses each case's three outputs under anonymous, randomly assigned labels. It sees current task materials, rubric and historical evidence but not preparation responses, condition identities or the research proposal. Position is shuffled once; position sensitivity is not estimated. Critical errors are listed separately. Code reports whitespace-delimited post word counts and adherence to the requested range independently of the judge.

An additional fresh model call audits the generated hypotheses for source relevance, justified scope and uncertainty handling. Both assessments use the same model family as generation and may share biases. They are model judgments, not human or domain-expert ratings. No human revision time is collected or substituted with zero.

Report every case, failures, critical errors, criterion scores, descriptive paired differences, inference audit and actual usage. A null result or a weaker structured condition is a valid outcome. No inferential significance tests are planned for six purposefully selected cases with one generation each. The library's production-selection/export function is not invoked: experimental context injection does not certify a deployable update.

## Interpretation

The pilot can demonstrate actual machine-generated hypotheses, feasibility of the data flow and concrete failure modes. It cannot establish professional validity with employees, robust superiority, high-scale operation, or recursive improvement. A later study needs practitioner calibration, further cases and repetitions, equal-budget comparisons and independent final evaluation. The proposed research remains open regardless of which condition scores highest here.

The new task briefs already explain source precedence, desired substance and explicit overrides; their rubrics accept multiple suitable openings. This makes them useful tests of execution, instruction precedence and unintended harm, but weak tests of recovering genuinely latent organisational requirements. A ceiling or null result would not adjudicate the central research hypothesis. This limitation is recorded before any experimental outputs are observed.

Execution references: [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode) and [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).
