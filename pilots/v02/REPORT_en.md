# Synthetic pilot v0.2 findings

Conducted 28–29 September 2026. Synthetic data only. No human evaluation.

Grounded reflection did not outperform direct adaptation in this pilot. It passed 19 of 24 task attempts, compared with 23 of 24 for direct adaptation. Successful attempts include appropriate clarification as well as completed deliverables. Both recovered the defined requirements during preparation. The main observed difficulty was carrying uncertainty about rejected alternatives into later tasks as unnecessary clarification obligations. The live run also exposed two weaknesses in the evaluator, documented below without changing the frozen primary results.

## Design and completed run

The model was `gpt-6-sol` with `medium` reasoning, accessed through the ChatGPT-authenticated Codex CLI. There were three families, recruiting, sales and research, and two repetitions. C and D each used two preparation calls per family and repetition, from the same historical records. All arms used the same downstream model and output schema. A received no history. B received the history with each task. C prepared reusable guidance directly. D added structured hypotheses and a counterevidence review.

The completed run is `runs/sol-medium-main-r2-20260928`. It contains 24 preparation calls, 48 validation calls and 96 final calls, with no failed calls. The twelve final cases were generated only after source, prompts, configuration, histories and prepared artifacts were frozen. No validation scores or final outputs were used to tune or select an update. Final instances share the authored task grammar and occupations with development materials, so this tests within-family transfer.

The first main attempt stopped during preparation after a network interruption and timeout. Its 23 successful calls, one failed call and late excluded response remain intact in `runs/sol-medium-main-20260928`. The completed run regenerated all preparation. It did not replace an individual unfavourable answer. The repeat was documented before any downstream condition scores were inspected.

## Frozen primary results

| Condition | Successful task attempts | Check compliance | Hidden-requirement checks |
| --- | --- | --- | --- |
| A, no adaptation | 6/24 | 30/72, 41.7% | 0/18 |
| B, direct historical evidence | 21/24 | 72/72, 100% | 18/18 |
| C, direct adaptation | 23/24 | 72/72, 100% | 18/18 |
| D, grounded reflection | 19/24 | 60/72, 83.3% | 13/18 |

Task success includes six clarification cases per arm. Valid clarification cases have no predicate-compliance denominator, so perfect compliance does not imply perfect task success. Non-delivery on a task requiring delivery fails all its checks, including fields that may be partially correct.

The prespecified D minus C comparison is minus four successful attempts, or minus 16.7 percentage points. There was one paired win for D, five losses and eighteen ties. These are descriptive outcomes from twelve authored tasks, not 24 independent participants or evidence of statistical significance. In the first repetition, D achieved 12/12 and C 11/12. In the second, D achieved 7/12 and C 12/12. All five D losses occurred in the second repetition.

All arms passed the six boundary cases. No final distractor adoption was observed on the declared checks. This does not establish general robustness, particularly because non-delivery also avoids adopting a distractor.

## What went wrong for reflection

In the second repetition, D correctly retained the normal routing requirements for sales and research. It also stored rejected fallback proposals as deferred rule candidates with unresolved evidence requests. The shared context renderer translated these requests into clarification obligations for current tasks.

Three otherwise actionable tasks therefore asked for fallback approval or use evidence and left the route undetermined. Their emphasis, source identifier and summary were correct, but the completion rule marked all twelve associated checks as failed. The hidden-check score must not be interpreted as five missing or incorrectly inferred requirement bodies.

Two ambiguous tasks also received unnecessary fallback questions. One additionally filled a field that the oracle required to remain unresolved. D's single win arose when C filled that unresolved field and D did not. The output phrase was generic, so the evaluator label `unsafe_guess` denotes violation of this particular abstention rule, not an independently demonstrated dangerous action.

The preparation-to-execution interface is therefore a concrete development target. Uncertainty about whether an alternative should become a rule should not automatically become a blocking question for every task. This is a diagnosis of the implemented procedure, not proof that reflection itself is ineffective. The D-only reference filter removed no predictions in this run.

## Requirement inference and measurement audit

Both C and D recovered all 18 target rule bodies across families and repetitions. Each obtained 90/90 correct scope probes for those matched bodies, and scoped recall was 18/18. Those probes do not evaluate every additional proposed rule or every possible context.

Frozen precision was 18/32 for C and 18/31 for D. These denominators were inflated by a representation mismatch. The synthetic generator always makes `family` and `role` equal, but the structural exception check required an explicit `role` restriction. Models generally used `family`. Correctly scoped local observations were consequently counted as unsupported rules and, in some cases, as distractor adoptions.

A separate post hoc diagnostic adds the implied `role=family` restriction in memory. Both procedures then score 18/19 precision, with one remaining overbroad showcase rule each. Supported local observations number 13 for C and 12 for D. This sensitivity is specific to this dataset and cannot justify equating family and role in real organisations. The original predictions and primary scores are unchanged. The small raw precision difference does not support a benefit of reflection.

A second post hoc diagnostic normalises only `receiving_audience` and `receiving audience` to `audience`, ignoring letter case for that alias lookup. B then passes 24/24 instead of 21/24. A remains 6/24, C 23/24 and D 19/24. D still asks extra questions, so alias normalisation does not rescue its failures. This diagnosis exposes an overly literal field-name check. It is not a replacement primary analysis or a human judgement of answer quality.

Both diagnostics are preserved separately as `audit-label-sensitivity.json` and `audit-scope-sensitivity.json` in the completed run. No model was called for these analyses, and no frozen evaluation code was edited.

## Calibration and remaining ceiling

The first scientific calibration scored 7/48 checks. Before the second and final permitted calibration, three fully specified anchors replaced three withheld-knowledge cases, and summary containment became case-insensitive. The second round scored 28/48, or 58.3%, within the planned 30–70% band. Anchors scored 24/24, while transfer cases scored 4/24. See [the calibration report](CALIBRATION_REPORT.md).

The pooled score therefore reflects a mixture of easy explicit cases and unavailable-context cases. It does not establish intermediate difficulty of contextual learning. B and C still reached the predicate-compliance ceiling in the final test, and both C and D reached the target-body recall ceiling. The pilot distinguishes completion behaviour and reveals implementation problems, but does not yet provide a fully validated instrument for the proposed research question.

## Resources and reproducibility

The completed main run reports 2,044,468 input-plus-output tokens, including CLI overhead. Preparation used 206,868 tokens for C and 225,518 for D, about 9.0% more for D despite equal logical call counts. Preparation plus final generation used 450,389 tokens for C and 471,871 for D. These runs are call-budget-controlled and token-audited, not strictly compute-matched.

Across the completed main run, aborted main attempt, two scientific calibration rounds and two successful transport checks, known reported usage totals 2,753,006 tokens. Twelve earlier schema-rejected attempts have unavailable usage and are not counted as zero. The CLI can reconnect internally, so logical runner calls are not an exact count of network requests.

No API-key billing, credit purchase or reset-credit redemption was used. Calls consumed included ChatGPT/Codex capacity. Dollar or euro cost is not inferred from tokens. The complete offline suite passed all 153 tests, and the original v0.1 frozen files remain unchanged. Code tests do not by themselves validate the scientific scoring assumptions exposed by the live run.

Raw outputs, configs, hashes, seeds, model usage, case scores, a verified `source_snapshot` and the generated `REPORT.md` are retained in the local run folder. `human-review.json` contains twelve blinded review items with a separate key. None has yet received a human review. Raw runs are ignored by Git and nothing has been published during this work.

## Implication and next experiment

The evidence supports the usefulness of historical information for these synthetic tasks. It does not support an advantage of the implemented reflection procedure. The most actionable observation is the cost of turning uncertainty about rejected alternatives into unnecessary workflow interruption.

Before a new experiment, validate the field-name and scope representation rules independently of which method benefits. Separate rejected hypotheses from genuine missing prerequisites in the shared execution interface. Then register a new version with fresh cases, retain a strong direct-adaptation baseline, and add practitioner review. Do not tune or replace this completed run. The current evidence does not establish enterprise quality, ROI, generalisation to new work domains or recursive self-improvement.
