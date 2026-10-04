# Pilot v0.3 first calibration

29 September 2026. Synthetic data only.

The first live calibration completed all 64 planned model calls. The registered gates failed, so the main comparison remains blocked. Output review identified problems in the measurement contract and one disputed inference target. The run provides a useful calibration record, but it does not yet support a comparison between grounded reflection and direct adaptation.

## Execution and review

The run used `gpt-6-sol` with medium reasoning through the existing ChatGPT-authenticated Codex transport. There were 16 preparation calls and 48 generation calls, with no failed or unfinished calls. All calls reported usage, totalling 745,349 input and output tokens. The cap was 64 logical calls and 2,000,000 reported tokens, audited between calls. This does not establish equal computation across conditions or a hard per-call token limit. The run used the existing account allowance and did not configure a paid API key or purchase credits.

Milad Morad confirmed the four conceptual inference rules before calibration. His response was “Alle vier sind plausibel”. That confirmation was an author-level conceptual check. Independent human review of generated records and model outputs remains pending. The post-run checks described here were assisted by coding agents and are not independent human validation.

This calibration used A, B and C only. Grounded reflection, D, was not run. No final-test histories or tasks were instantiated, and no F0 or main run was created. The calibration seed was 3307, with one repetition. The four designed pairs produced eight dependent histories and sixteen future tasks.

## Registered results

| Condition | Justified diagnostic updates | Compliant diagnostic outputs | Justified control updates | Compliant control outputs |
| --- | --- | --- | --- | --- |
| A, current task only | 8/8* | 3/8 | 8/8 | 8/8 |
| B, direct historical evidence | 7/8 | 6/8 | 8/8 | 8/8 |
| C, direct adaptation and review | 4/8 | 4/8 | 4/8 | 4/8 |

*A's update score is relative to its current-task information. It can correctly retain the baseline while failing a hidden work requirement. Its warrant score is therefore not directly comparable with B or C. World-field obligations are shared across conditions.*

C passed three of four change diagnostics but only one of four retention diagnostics. It failed the retention floor of 2/4 and the control floor of 7/8. The remaining registered gates passed. On the prespecified seven recoverable diagnostics, B produced six warranted, compliant outputs, compared with three world-compliant outputs for A.

Historical evidence helped on these particular diagnostic tasks. The experiment is too small and deliberately constructed to estimate an enterprise effect. The raw C scores should not be interpreted as evidence that adaptation is generally harmful. Several recorded failures arose from the issues below.

## Audit of the measurement

### Correct fields penalised by an update label

Four C outputs declared `apply` while their rules left the current baseline unchanged. Their fields matched the warranted outcome. Three of these were world-correct control outputs. The fourth was the ambiguous S02 diagnostic, where justified retention intentionally does not satisfy the hidden world policy.

The scorer made world compliance depend on the consistency of the declared decision. This conflated output-field correctness with update metadata. A separate read-only audit compared exact fields in completed, correctly identified outputs without employee questions. It preserved the original strings and did not change model answers, rules or calibration gates.

| Condition | Exact diagnostic fields | Exact control fields |
| --- | --- | --- |
| A | 3/8 | 8/8 |
| B | 6/8 | 8/8 |
| C | 4/8 | 7/8 |

These are post hoc diagnostic counts, not replacement primary scores. The original calibration still failed. The four label mismatches concern C tasks `122212938df73cc0`, `c1cc37bc9b619921`, `5b9ee762b5f29642` and `0545926cbae39b07`.

### S04 requires an additional generalisation assumption

Three equally authorised reviewers consistently request an annual total. C adopts that rule for those observed reviewers and preserves the broader workflow hypothesis as unresolved. The held-out task introduces a fourth reviewer. The public setup permits reviewer-specific conditions and instructs retention where no exception is supported, while the evaluator assumes a shared convention must transfer to the new reviewer.

C's caution is compatible with those public instructions. The broader convention is plausible, but its warranted transfer depends on an inductive assumption that was not stated clearly enough. S04 therefore cannot be treated as an unambiguous model failure. B also retained the baseline, although its output alone does not establish the same reasoning. No S04 score has been changed.

### S05 omits a required value convention from preparation

C correctly describes retaining checksum verification but encodes the marker as `"true"`. The evaluator expects `"required"`. Preparation receives only the description “Whether verification is required”, without the canonical value. The concrete baseline appears later during generation, after the rule has been committed.

Both S05 outputs have the correct endpoint and release. The marker mismatch accounts for their recorded field failures. This is predominantly an underspecified representation contract, rather than evidence that C inferred the wrong routing requirement. The audit does not silently normalise the two strings.

### S07 exposes a real translation error

C's first preparation correctly retains the configured table title. Its second preparation adds an `append_fact` rule while describing the intention as retaining an existing suffix. The title already contains the suffix. Execution follows the rule and produces `Response distribution / V92501 / V92501`.

The executable rule is wrong even though the stated contextual distinction is sensible. This case supports measuring requirement inference and rule construction separately. A future shared operator contract should make clear that append means literal concatenation to the complete baseline. The renderer should not silently repair such mistakes.

### S06 status coverage is sensitive to hypothesis decomposition

C marks the combined global routing candidate as rejected, while retaining a separate archive-route candidate as unresolved and identifying the missing archive evidence. Its active-route adaptation and boundary retention are correct. The registered target coverage of 1/2 therefore reflects, in part, how uncertainty is divided between candidates and what `reject` means. It does not demonstrate that C ignored all uncertainty or made a harmful global routing change.

## Implications for the next iteration

Before the remaining calibration round, make the measurement contract explicit and preserve these failures as development regressions.

1. Separate observed field correctness, execution consistency and the declared update label. Derive the actual update from rendered changes and retain label inconsistency as its own diagnostic. Any change to primary scoring needs a prospective protocol amendment.
2. Give all conditions the same canonical field values and exact operator semantics before preparation. Explain that confirming a baseline does not require a new change rule. Keep genuine duplicate-append failures visible.
3. Repair S04 at the level of admissible hypotheses and public assumptions. Either retain uncertainty for an unseen reviewer or explicitly define the bounded assumption under which shared practice supports transfer. Recheck the resulting diagnostic balance instead of preserving a disputed target merely to meet a gate.
4. Distinguish rejecting a proposed operational change from disproving a contextual explanation. Review set-level uncertainty coverage where a model decomposes a broad hypothesis into narrower ones.
5. Re-run offline regressions, record the revised review scope, and use a fresh calibration instance before considering the main comparison. Do not weaken C or inspect D to manufacture a gap. If the remaining round fails, retain that result and stop the planned main comparison.

No second live calibration was started. Measurement and rubric issues should be resolved before consuming that final round. The important outcome so far is a concrete account of where inference, executable representation and measurement diverge. There is no demonstrated benefit of grounded reflection, enterprise quality gain, ROI or recursive improvement yet.

## Reproducible record

- [Sealed original report](runs/calibration-r1-sol-medium-20260929/REPORT.md)
- [Registered results and all case scores](runs/calibration-r1-sol-medium-20260929/results.json)
- [Candidate scores](runs/calibration-r1-sol-medium-20260929/candidate_scores.json)
- [Read-only audit script](analysis/audit_calibration.py)
- [Post hoc field audit](analysis/calibration-r1-field-audit.json)
- [Blinded sample for future human checks](runs/calibration-r1-sol-medium-20260929/human_review/sample.json)

The audit verified all 907 files in the sealed artifact manifest. Analysis files live outside the sealed run. To reproduce the audit from the repository root without model calls, run `python -B pilots/v03/analysis/audit_calibration.py pilots/v03/runs/calibration-r1-sol-medium-20260929`. The script refuses an output path inside the sealed run and never overwrites an existing analysis file.
