# Grounded Reflection

A Python research library for turning feedback, revisions and work records into scoped requirement hypotheses and candidate context updates for agents.

```text
Work evidence → Requirement hypothesis → Context update → Paired evaluation
                sources, scope,          predicted        keep baseline,
                alternatives             effect           defer or accept
```

**Early development — `0.1.0.dev1`.** The library implements data models, evidence and scope checks, and a selector for supplied evaluation records. An optional model backend supports a first experiment; repeated autonomous adaptation remains research work.

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

## Research and development

The research question is when an explicit, evidence-grounded interpretation of work requirements helps agents adapt beyond retrieval or direct adaptation. Next steps are less explicit and conflicting evidence, practitioner-calibrated tasks, repeated trials and bounded adaptation cycles. See the [roadmap](docs/research-roadmap.md) and [HR data card](docs/hr-example.md).

Run the tests with `python -m unittest discover -s tests -v`. Contributions should include reproducible examples and tests for changes to protocol behaviour. Use synthetic data in public examples.

Milad Morad. Developed with AI coding assistance. Code and fictional fixtures: [MIT License](LICENSE). Citation metadata: [CITATION.cff](CITATION.cff).
