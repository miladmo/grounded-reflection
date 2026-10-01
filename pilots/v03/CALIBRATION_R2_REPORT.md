# Pilot v0.3 second calibration

29 September 2026. Synthetic data only. Design revision `v03-calibration-r2`.

The revised calibration completed all 64 planned calls. Direct historical evidence and direct adaptation both made all eight warranted diagnostic decisions correctly. Both also passed all eight controls. The planned main comparison is stopped because direct adaptation reached the ceiling of the primary measure, exceeding the prespecified calibration band of 4–7 correct decisions. Grounded reflection was not run.

## What changed before this run

The [prospective protocol amendment](../../docs/pilot-v03-protocol.md) separated output-field correctness from update labels and rule execution. All stages received the same explicit operator contract and canonical field values. Sales tasks now test a new case for an observed reviewer, while retaining uncertainty about unobserved reviewers. The first calibration and its source snapshot remain unchanged.

The full repository passed 264 unit tests. A complete offline mock run exercised 288 logical completions before live execution. Original conceptual human approval was carried forward with an explicit record of its limits. The amendment and automated verification are not represented as a new independent human review. Human output checks remain pending.

The model remained `gpt-6-sol` with medium reasoning. This run used seed 3317 and order seed 3318, one repetition, and the same 64-call cap. The fresh instance changed some counterbalanced policy directions as well as identifiers and values. In particular, HR initially omitted the reference and reporting initially omitted the title suffix, whereas both were present in round 1. Scores across the rounds therefore do not isolate the effect of the interface repairs.

## Results

| Condition | Warranted diagnostic decisions | World-correct diagnostic fields | World-correct control fields |
| --- | --- | --- | --- |
| A, current task only | Not comparable* | 3/8 | 8/8 |
| B, direct historical evidence | 8/8 | 7/8 | 8/8 |
| C, direct adaptation and review | 8/8 | 7/8 | 8/8 |

*A is evaluated against current-task information for warrant, while B and C are evaluated against the historical evidence. A's recorded warrant score is 8/8 because retaining the baseline is justified without that history. This is not evidence that it recovered the hidden requirements.*

B and C each made all four required changes and all four required retention decisions. Their control update scores were also 8/8. Across all 48 generated outputs, there were no declared-decision mismatches, execution inconsistencies or employee questions. Every output was marked completed and passed the strict output contract.

The one world-incorrect diagnostic in B and C was S02. Multiple hypotheses still fit the observations but disagree on the new context combination. Both procedures retained the baseline, which is justified under the evidence even though it misses the hidden world's booking-reference requirement. On the seven prespecified recoverable diagnostics, B and C each achieved 7/7, versus A's 3/7.

All registered gates passed except `C_diagnostic_between_4_and_7_of_8`. C scored 8/8. Both allowed calibration rounds are now consumed. No threshold was relaxed, no additional round was started, and no F0 or final-test experiment was created.

## What the preparation artifacts show

C's final preparations covered 12 of 15 author-defined candidate-status targets, including all seven required adopted rules, one of three rejection targets and four of five unresolved targets. Across 26 candidates there were seven adopted rules, with no unsupported adoption or untraceable candidate on the fixed checks. This secondary score is not equivalent to the primary task score. Its three misses require careful interpretation.

- In S01, C adopted the supported recipient rule and rejected a universal rule, but did not explicitly encode the evaluator's particular contract-trigger rival as rejected. This is a missing explanation in the requested representation, without an observed operational error.
- In S06, C adopted the active-collection route and kept the archive switch unresolved, including the missing archive test. The evaluator's single global-route target was not reproduced as one combined candidate. The uncertainty is nevertheless present for the archive boundary.
- In S07, C adopted a chart-only rule and explicitly rejected the corresponding table rule. The evaluator expected a combined chart-and-table generalisation to be rejected. The narrower rejection captures the consequential counterevidence but is not an exact match to that target.

The fixed coverage scores remain unchanged. They demonstrate dependence on candidate representation and cannot support the claim that C missed three work requirements. Future assessment of explanations should specify the alternative being tested and its observable implications before execution, rather than equating one preferred decomposition with understanding.

## Resource use

| Condition | Preparation calls | Generation calls | Reported input and output tokens |
| --- | --- | --- | --- |
| A | 0 | 16 | 180,103 |
| B | 0 | 16 | 197,778 |
| C | 16 | 16 | 396,240 |
| Total | 16 | 48 | 774,121 |

There were no failed, unfinished or unmetered calls. C's total comprises 215,687 preparation tokens and 180,553 generation tokens. It incurred more preparation work for the same observed task outcomes as B. Whether reusable guidance amortises that work over many subsequent tasks was not tested. These transport-reported counts do not establish equal computation or a monetary ROI. The run used the existing ChatGPT-authenticated Codex access, with no API key or credit purchase.

The two calibration rounds together used 128 calls and 1,519,470 reported tokens. This total excludes offline mocks and the surrounding development work.

## Scientific interpretation

The strongest supported finding is that, in these constructed scenarios, direct use of work evidence and a strong two-pass adaptation procedure both recover enough contextual guidance to make the tested warranted changes and avoid the tested unwarranted changes. A history-free baseline satisfies fewer hidden-world requirements.

This is a feasibility signal for deriving reusable guidance from work evidence. It provides no estimate of enterprise quality, human rework reduction or recursive improvement. It also provides no result for D, either positive or negative. A perfect primary score for C leaves no observed headroom for demonstrating an improvement on that measure with this sample. It does not prove that the procedures are equivalent or that reflection never helps.

The instrument has become more explicit about its contracts, but its current task distribution remains too easy for the planned method comparison. Its observations directly expose small rule changes within a supplied vocabulary and stability regime. Evaluation still covers four constructed contrasts, one model and one calibration repetition, with dependent cases and no independent human output assessment.

## Next research decision

Do not spend the planned 288-call main budget on this ceiling-limited comparison. A new protocol would be needed before further efficacy testing. It should investigate where evidence-grounded inference becomes difficult, while preserving a strong direct-adaptation baseline.

A useful next design would vary prespecified properties of the evidence, such as independent versus copied corrections, informative versus confounded context contrasts, and stable versus changing workflow authority. Both C and D must receive the same records and access budget. Some settings should warrant a narrow update, some a broader update, and some no identifiable update. Difficulty must come from the inference problem rather than obscure field strings or incomplete execution instructions.

Use multiple independently generated histories per setting and assess the resulting difficulty distribution, instead of adding one hand-picked case until C loses a point. Include bounded alternative explanations with explicit witness contexts, and evaluate both their evidential status and their downstream scope. Define the human review and held-out split before new live outputs. Retain the current ceiling result as part of the research record.

## Artifacts

- [Sealed round-2 report](runs/calibration-r2-sol-medium-20260929/REPORT.md)
- [Registered results](runs/calibration-r2-sol-medium-20260929/results.json)
- [Candidate scores](runs/calibration-r2-sol-medium-20260929/candidate_scores.json)
- [Blinded sample awaiting human assessment](runs/calibration-r2-sol-medium-20260929/human_review/sample.json)
- [Source amendment and verification record](analysis/round2-source-amendment.json)
- [First calibration and its interpretation](CALIBRATION_REPORT.md)

Both calibration runs remain sealed. Sealed source snapshots remain available for exact reproduction. A post-run relative-link correction to the scenario cards is recorded separately; experimental code, prompts and data were unchanged. No final-test data were used to develop or select these revisions.
