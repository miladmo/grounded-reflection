# Grounded Reflection

A Python research library for turning feedback, revisions and work records into scoped requirement hypotheses and candidate context updates for agents.

```text
Work evidence → Requirement hypothesis → Context update → Paired evaluation
                sources, scope,          predicted        keep baseline,
                alternatives             effect           defer or accept
```

**Early development — `0.1.0.dev1`.** The library implements data models, evidence and scope checks, and a selector for supplied evaluation records. An optional model backend supports a first experiment; repeated autonomous adaptation remains research work.

## Latest result: synthetic pilot v0.5

**Question.** Is direct use of organisational evidence still enough when a history does not fit into one model call, and when it is publicly unknown which attributes of a work item determine a requirement? An oracle computes the warranted action from the public evidence, so every answer can be scored.

**Four arms**, all using one model (DeepSeek-V4-Flash via FHGenie):

* A: no history;
* B: direct use with deterministic retrieval;
* C: chunked preparation;
* D: a hypothesis register with targeted record queries.

**Results** (correct diagnostics out of 48):

| Arm | Correct |
| --- | ---: |
| B, direct use | **44** |
| C, chunked preparation | 39 |
| D, hypothesis register | 29 |
| Never change anything (keep floor) | 24 |

* **The decisive errors happened with complete evidence.** The binding evidence was fully in context, but the arms generalised wrongly. B stated a rule over an irrelevant attribute or missed the relevant ones. C did not apply the rule class to an unobserved combination. In each case the decision matched a pure similarity heuristic.
* **D's shortfall lies in setting up the hypothesis space, not in testing.** D considered only one of the two values per attribute. It therefore proposed only 6 of 14 or 38 of 134 possible rules, which an unclear sentence in our class description invited. Where the correct rule was in its register, D solved every diagnostic.
* **Removing a field is missed more often than adding one.** All five missed changes by B and C concern omission, as in v0.4.

**Limits.** Synthetic data, one model, thin cells (two diagnostics per hard type, setting and arm). The hard tasks are a stress test built so that similarity misleads, not an estimate of natural error rates. The protocol was approved before any data, the runs are sealed, and changes and incidents are documented.

See the [v0.5 report](pilots/v05/DIFFICULTY_MAP_REPORT.md) and [protocol](docs/pilot-v05-protocol.md).

## A recorded example

The model pilot produced hypothesis `H1` and candidate update `C1` from fictional HR work records:

| Step | Example |
| --- | --- |
| Work evidence | Two specialist reviews ask for a concrete work-problem opening. An apprenticeship review instead asks for learning opportunities and support. |
| Provisional hypothesis | Experienced specialists may prefer a problem-and-contribution opening in Atlas LinkedIn recruiting posts. |
| Scoped update | Use that opening for this audience and campaign; current approved facts and explicit task instructions take precedence. |
| Boundary | The apprenticeship review challenges applying the same opening to every audience. Recruiting effectiveness remains unmeasured. |

This summarises actual model-generated hypotheses and updates from synthetic records. The [recorded preparation](pilots/hr_v01/observed_outputs.json) preserves exact source quotes, alternative explanations and untested predictions.

**Pilot finding:** all three conditions received 10/10 model ratings on all six synthetic tasks. This complete rating ceiling provides no observed advantage for structured reflection. There has been no human evaluation. See the [results and limitations](pilots/hr_v01/REPORT_en.md).

## Quick start

Requires Python 3.11+. Install from a checkout; the package is not on PyPI.

```bash
python -m pip install .
grounded-reflection demo --output demo-output
```

The offline demo uses four fictional HR episodes and three authored candidate updates. It makes no model calls and requires no API key.

| Candidate | Result | Reason |
| --- | --- | --- |
| `scoped-update` | `eligible_for_validation` | References resolve and the declared scope is preserved. |
| `overbroad-update` | `rejected` | The update broadens its supporting hypothesis. |
| `ambiguous-update` | `needs_clarification` | A missing rationale blocks the proposed change. |

Final selection is deferred because no validation ratings are supplied. The baseline is retained and no update is exported.

## Library

- **Evidence models:** Pydantic contracts for work episodes, hypotheses, updates, paired evaluations and decisions. Evidence records carry provenance; hypotheses retain references, counterevidence and alternative explanations.
- **Reference and scope checks:** resolve exact source quotes, reject scope broadening and report missing context. These checks validate declarations, not semantic support for a claim.
- **Update selection:** compare supplied ratings with a fixed baseline, require a declared quality gain and human-effort budget, and reject observed regressions or remaining critical errors. Decisions bind to candidate content through digests.
- **Model backend:** an experimental Codex CLI adapter records prompts, responses, usage and tool-use checks. The pilot uses it to generate hypotheses and context patches.

```bash
grounded-reflection schema --output exported-schemas
grounded-reflection validate path/to/evidence.json
grounded-reflection select --help
```

Output commands refuse to overwrite existing files. The selector can export an accepted context artifact; deployment belongs to the consuming application. The library trusts supplied labels and ratings and includes no anonymisation or secure data storage. See the [protocol](docs/protocol.md) for policy defaults, split checks and limits.

## Model pilot

The pilot compares direct use of historical evidence, direct adaptation and structured reflection on six independently authored synthetic recruiting tasks. Unlike the offline demo, its hypotheses and texts are actual model outputs. It uses one generation per case and condition, with a separate, blinded judge call from the same model family.

- [Protocol and frozen inputs](pilots/hr_v01/protocol.md)
- [Results and resource use](pilots/hr_v01/REPORT_en.md)
- [All 18 outputs](pilots/hr_v01/OUTPUTS.md)
- [Preparations, outputs and judgments as JSON](pilots/hr_v01/observed_outputs.json)

The report explains how to repeat the experiment with an authenticated Codex CLI. A repeat makes 27 model calls and uses the caller's model access. Raw runtime logs are excluded from Git.

## Synthetic pilot v0.2

The [v0.2 pilot](pilots/v02/README.md) adds four comparison conditions, conflicting evidence and scoped requirements across three synthetic task families. It separates preparation, validation, source freeze and final evaluation, with deterministic checks and recorded budgets. A complete offline mock run requires no model access. Mock outputs test infrastructure and are not calibration or research results. The v0.1 findings above remain unchanged.

## Research and development

The research question is when an explicit, evidence-grounded interpretation of work requirements helps agents adapt beyond retrieval or direct adaptation. Next steps are less explicit and conflicting evidence, practitioner-calibrated tasks, repeated trials and bounded adaptation cycles. See the [roadmap](docs/research-roadmap.md) and [HR data card](docs/hr-example.md).

Run the tests with `python -m unittest discover -s tests -v`. Contributions should include reproducible examples and tests for changes to protocol behaviour. Use synthetic data in public examples.

Milad Morad. Developed with AI coding assistance. Code and fictional fixtures: [MIT License](LICENSE). Citation metadata: [CITATION.cff](CITATION.cff).
