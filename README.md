# Grounded Reflection

A Python research library for turning feedback, revisions and work records into scoped requirement hypotheses and candidate context updates for agents.

```text
Work evidence → Requirement hypothesis → Context update → Paired evaluation
                sources, scope,          predicted        keep baseline,
                alternatives             effect           defer or accept
```

**Early development — `0.1.0.dev1`.** The library implements data models, evidence and scope checks, and a selector for supplied evaluation records. An optional model backend supports a first experiment; repeated autonomous adaptation remains research work.

## Pilot studies

Pilot numbers are study stages. The package version is `0.1.0.dev1`.

| Pilot | Question | Core result | Protocol and report |
| --- | --- | --- | --- |
| v0.1 | Does structured reflection improve recruiting posts over direct use and direct adaptation? | All three conditions received 10/10 model ratings on six tasks: a rating ceiling, with no observed advantage for reflection. | [protocol](pilots/hr_v01/protocol.md), [report](pilots/hr_v01/REPORT_en.md) |
| v0.2 | Does grounded reflection recover omitted requirements better than direct adaptation, across three task families with conflicting evidence? | Reflection passed 19 of 24 task attempts, against 23 for direct adaptation and 21 for direct evidence. It carried rejected alternatives forward as unnecessary clarifications. | [protocol](docs/pilot-v02-protocol.md), [report](pilots/v02/REPORT_en.md) |
| v0.3 | When does work evidence warrant a change, with candidate status, update decision and world compliance scored separately? | Direct evidence and direct adaptation made all 8 warranted decisions in calibration. The ceiling stopped the main comparison, so reflection was not run. | [protocol](docs/pilot-v03-protocol.md), [report](pilots/v03/CALIBRATION_R2_REPORT.md) |
| v0.4 | Which evidence difficulties (raw artifacts, volume and noise, dependence, change over time) break direct use or preparation? | With explicit approval semantics and histories that fit into one call, direct use reached 23 of 24 executed-field diagnostics and two-pass preparation 21. No setting showed headroom. | [protocol](docs/pilot-v04-protocol.md), [report](pilots/v04/DIFFICULTY_MAP_REPORT.md) |
| v0.5 | Is direct use still enough when histories exceed one call and the relevant attributes are unknown, and does a hypothesis register help? | Direct use 44 of 48, chunked preparation 39, hypothesis register 29, never-change floor 24. The register failed at setting up the hypothesis space, not at testing. | [protocol](docs/pilot-v05-protocol.md), [report](pilots/v05/DIFFICULTY_MAP_REPORT.md) |

All pilots use synthetic data; each report states its registration, deviations and limits.

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
* **D's shortfall lies in setting up the hypothesis space, not in testing.** In 15 of 16 histories D considered only one of the two values per attribute, so most registers held only 6 of 14 or 38 of 134 possible rules; an unclear sentence in our class description invited this reading. Where D kept the correct rule (3 histories), it solved every diagnostic.
* **Removing a field is missed more often than adding one.** All five missed changes by B and C concern omission, as in v0.4.
* **Prespecified expectations.**
  * Larger histories did lower the best direct arm slightly, but this is not shown as a selection effect: no decisive error rested on missing evidence.
  * The effect of unknown attributes is partly consistent but not shown.
  * D did not beat the direct arms in any setting.

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
- **Model backends:** an experimental Codex CLI adapter records prompts, responses, usage and tool-use checks; pilots v0.1–v0.3 use it. Pilots v0.4 and v0.5 use an HTTP transport for FHGenie, an institutional LLM gateway. The transport reads the gateway address from local configuration outside the repository and checks a pinned SHA-256 before any request; the address is not published.

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

The research question is when an explicit, evidence-grounded interpretation of work requirements helps agents adapt beyond retrieval or direct adaptation. The v0.5 report names four next steps, none of them tested yet:

1. Define the hypothesis space explicitly (a literal tests either of the two values of an attribute; the declared classes hold 14 and 134 rules), or let the harness enumerate it. The model then judges the evidence.
2. Give the query rounds a path for extending the register, and treat an empty register as a sign of an incomplete enumeration.
3. Carry the registration scope into adopted rules.
4. Study the asymmetry between removing and adding a field as a target in its own right.

See also the [roadmap](docs/research-roadmap.md) and [HR data card](docs/hr-example.md).

Run the tests with `python -m unittest discover -s tests -v`. Contributions should include reproducible examples and tests for changes to protocol behaviour. Use synthetic data in public examples.

Milad Morad. Developed with AI coding assistance. Code and fictional fixtures: [MIT License](LICENSE). Citation metadata: [CITATION.cff](CITATION.cff).
