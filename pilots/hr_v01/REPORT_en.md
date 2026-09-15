# HR pilot v0.1 — observed model results

**All three conditions received 10/10 model ratings on all six tasks: a complete rating ceiling, with no observed advantage for structured reflection.** These exploratory results use synthetic tasks and actual model responses. No human evaluation or recursive improvement was measured.

Inputs were frozen at `2026-09-15T08:51:02.177941+00:00`. Requested model: `gpt-6-astra`; reasoning setting: `xhigh`. Six cases, three conditions, one generation per case/condition, two preparation calls, six blinded comparison calls and one inference audit. A separate transport smoke test is excluded.

## Descriptive comparison

The total is the sum of five ordinal 0–2 rubric judgments. Means describe this small run; no statistical significance or population effect is inferred.

| Condition | Mean model score / 10 | Cases with model-flagged critical errors | Posts within 110–150 words |
| --- | ---: | ---: | ---: |
| Direct evidence | 10.00 | 0/6 | 6/6 |
| Direct adaptation | 10.00 | 0/6 | 6/6 |
| Grounded reflection | 10.00 | 0/6 | 6/6 |

| Case | Type | Direct evidence | Direct adaptation | Grounded reflection | Reflection − evidence | Reflection − adaptation |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| eval-01 | transfer | 10 | 10 | 10 | +0 | +0 |
| eval-02 | transfer | 10 | 10 | 10 | +0 | +0 |
| eval-03 | transfer | 10 | 10 | 10 | +0 | +0 |
| eval-04 | boundary | 10 | 10 | 10 | +0 | +0 |
| eval-05 | boundary | 10 | 10 | 10 | +0 | +0 |
| eval-06 | explicit_override | 10 | 10 | 10 | +0 | +0 |

## Actual inference and protocol checks

The model generated 3 hypotheses and 3 candidate updates. Formal parsing status: `parsed`.

**H1:** For Atlas LinkedIn posts targeting experienced specialists, the reviews favor opening with the concrete work problem and applicant contribution while retaining meaningful technical terminology. This is a provisional editorial preference; recruiting effectiveness is unmeasured.

**H2:** The Atlas apprenticeship episode supports a provisional preference for introducing approved learning opportunities and support before explaining work plainly and clarifying experience requirements.

**H3:** For Atlas LinkedIn recruiting, current vacancy facts should govern employment details and application routes. The unexplained shortened post provides insufficient evidence for a standing word limit or permission to omit logistics.

| Candidate | Formal status | Resolved supporting/counterevidence references |
| --- | --- | ---: |
| C1 | eligible_for_validation | 3 |
| C2 | eligible_for_validation | 3 |
| C3 | eligible_for_validation | 4 |

These checks establish that quotes exist and declared scopes are contained. Semantic validity is separate. The same-model inference audit is available in `results.json`; it does not replace practitioner assessment.

The direct-adaptation response also identifies audience-specific openings, current-source precedence and the uncertainty of unexplained shortening. Consequently, successful inference alone does not establish that the structured method adds useful information.

The recorded reviews and missingness annotations explicitly indicate several relevant distinctions. This demonstrates synthesis of annotated work episodes, with limited evidence about discovering implicit requirements in raw logs. All three generated candidates have empty blocking-question lists: the model chose conservative guidance, and no clarification intervention was performed.

## Recorded resources

Direct adaptation and grounded reflection used the same model/settings and number of preparation/generation calls. The measured token consumption differs; this is not an exact compute-matched comparison.

| Condition | Generation + preparation calls | Reported input tokens | Reported output tokens | Sum of call durations (s) |
| --- | ---: | ---: | ---: | ---: |
| Direct evidence | 6 | 80642 | 7970 | 276.3 |
| Direct adaptation | 7 | 74862 | 9525 | 323.5 |
| Grounded reflection | 7 | 73514 | 12389 | 415.0 |

Across all 27 experimental calls, CLI-reported input tokens: 337263; output tokens: 46263; cached input tokens (reported separately): 0; reasoning output tokens (reported separately): 34074. Counts include the CLI's context overhead. Duration sums include concurrent calls and are not elapsed experiment time. No monetary cost is inferred.

| Preparation | Guidance words | Requested ≤350-word limit met |
| --- | ---: | --- |
| Direct adaptation | 311 | True |
| Grounded reflection | 180 | True |

## Interpretation and limits

This run demonstrates machine-generated structured hypotheses, executable reference/scope checks and a complete experimental path to new task outputs and blinded model assessment. It does not demonstrate employee-validated requirements, expert-level work quality, large-scale inference or repeated self-improvement.

Before execution, the protocol recorded that task briefs already expose much of the required information. The observed rating ceiling therefore leaves the value of learning implicit requirements unresolved. Six purposeful synthetic cases, one sample each, a coarse rubric and a judge from the same model family constrain interpretation. The structured condition combines prompting and deterministic scope filtering; no ablation isolates their contributions.

No human revision time was measured. No paired validation record was fabricated to satisfy the library's update-selection gate, and no update was exported or deployed. Next research steps require independently calibrated professional tasks, human judgments and comparisons with repetitions and explicitly matched resources.

## Inspect and reproduce

- [Frozen protocol](protocol.md) and [file hashes](frozen_manifest.json)
- [Task materials](tasks.json) and [rubric](rubric.json)
- [Complete preparations, outputs and anonymous judgments](observed_outputs.json)
- [All posts side by side](OUTPUTS.md)
- [Machine-readable analysis](results.json)
- [Runner](run_pilot.py) and [clean-replay preparation](prepare_replay.py)

To prepare a separate repeat without overwriting the observed run, invoke `python pilots/hr_v01/prepare_replay.py ../grounded-reflection-replay` from the repository. Follow the printed commands using your own authenticated Codex CLI. Preparing the copy makes no model calls; executing the stages makes 27 calls. Raw local run directories contain full runtime logs and are excluded from Git by default. Exact sampling and hidden server-side model version are not controlled.

Run `python pilots/hr_v01/export_report.py` to generate report views and an anonymous human-review sheet in `pilots/hr_v01/rendered/`. This uses the published responses and makes no model calls.
