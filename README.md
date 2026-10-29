# Grounded Reflection

**When does evidence from an agent's use justify learning a new work requirement?**

This research project studies how agents can infer requirements omitted from their initial configuration, test competing explanations and limit an adaptation to the contexts supported by evidence. It combines a Python library with five synthetic pilot studies.

```text
Work evidence → Requirement hypothesis → Scoped update → Evaluation on new tasks
```

**Early development, package version `0.1.0.dev1`.** The pilots have not established a benefit of grounded reflection over strong direct methods. They identify measurement ceilings, scope errors and incomplete hypothesis enumeration. Repeated autonomous improvement and enterprise value remain research questions.

Start with the [methods](docs/methods.md), the [v0.4 guide](pilots/v04/GUIDE.md) or the [v0.5 study](pilots/v05/README.md). [Reproducibility](docs/reproducibility.md) explains what can be checked from this checkout. The [glossary](docs/glossary.md) defines study terms, and [provenance](docs/provenance.md) indexes the historical records.

## Pilot studies

Pilot numbers identify study stages, not software releases. All use synthetic data.

| Pilot | Question | Main finding | Study |
| --- | --- | --- | --- |
| v0.1 | Does structured reflection improve recruiting posts? | All three conditions received 10/10 model ratings on six tasks. This ceiling, without human evaluation, could not distinguish them. | [Report](pilots/hr_v01/REPORT_en.md) |
| v0.2 | Can reflection recover omitted requirements from conflicting evidence? | Reflection passed 19/24 task attempts, direct adaptation 23/24 and direct evidence 21/24. Rejected alternatives became unnecessary clarifications. | [Report](pilots/v02/REPORT_en.md) |
| v0.3 | Can warranted adaptation be measured separately from hidden-world accuracy? | Direct evidence and adaptation each passed 8/8 calibration tasks. The ceiling stopped the main comparison before reflection was run. | [Calibration](pilots/v03/CALIBRATION_R2_REPORT.md) |
| v0.4 | Which evidence difficulties challenge direct methods? | Preparation scored 21/24 and direct use 16/24 on the registered metric including declared scope. The post hoc fields-only scores were 21/24 and 23/24. No setting established headroom. | [Guide and results](pilots/v04/GUIDE.md) |
| v0.5 | Does a hypothesis register help with large histories and unknown relevant attributes? | Direct retrieval scored 44/48, chunked preparation 39/48 and the register procedure 29/48. Never changing the configuration scored 24/48. | [Study and results](pilots/v05/README.md) |

## Latest result: synthetic pilot v0.5

Four procedures use the same model, DeepSeek-V4-Flash via FHGenie, with different preparation and retrieval procedures. A deterministic oracle scores output fields against what the public evidence warrants. Actual computation differs between arms.

The hypothesis-register procedure was less accurate than direct retrieval in every setting. In 15 of 16 histories it considered only one of the two values per attribute. Ambiguous specification wording may have contributed. It also lost workflow scope. These findings prevent a clean attribution to the effectiveness of reflection itself.

The three direct-method errors decisive for the main difficulty comparisons occurred with complete binding evidence in context. They do not demonstrate a retrieval failure. All five missed changes by the direct methods concerned omission, a small-sample observation that needs further study.

The design and decision rules were recorded before the evaluated runs. Technical failures remain in the scores. This is a descriptive stress test with one model and two cases per hard task type, setting and arm. See the [results, incidents and limitations](pilots/v05/README.md).

## Reading the v0.4 result

Seven of direct use's eight registered failures had correct output fields but declared rules with excessive scope. Its post hoc fields-only score of 23/24 exceeds preparation's 21/24. The registered comparison therefore does not establish better task decisions through preparation. No setting met both headroom conditions. S4 remains provisional because its two failure causes are unresolved. The [guide](pilots/v04/GUIDE.md) keeps these measurements separate.

## A recorded example

In the first pilot, two specialist reviews requested a concrete work-problem opening for recruiting posts. An apprenticeship review instead requested learning opportunities and support. The model proposed a problem-and-contribution opening scoped to experienced specialists in one campaign, retaining the contrasting review as counterevidence to wider use.

This example comes from [recorded model outputs on fictional records](pilots/hr_v01/observed_outputs.json). Recruiting effectiveness was not measured. A separate [worked illustration](pilots/v05/README.md#a-worked-example) explains the deterministic inference used in the later pilots.

## Quick start

Requires Python 3.11+. Install from a checkout; the package is not on PyPI.

```bash
python -m pip install .
grounded-reflection demo --output demo-output
```

The offline demo uses four fictional HR episodes and three authored candidates. It requires no API key. It accepts one candidate for validation, rejects an overbroad candidate and flags a candidate with a missing rationale. Final selection stays deferred because validation ratings are absent. No update is exported.

## Library

- Pydantic contracts represent evidence, hypotheses, scoped updates and paired evaluations.
- Reference and scope checks validate source quotes and declared boundaries. They do not establish semantic support for a claim.
- A selector evaluates supplied ratings, required gains, human-effort limits and regressions. It can export an accepted context artifact; it does not deploy changes.
- Experimental model backends log calls and usage for the pilots. The offline library does not require them.

The library trusts supplied labels and ratings and provides no anonymisation or secure data storage. See the [executable library protocol](docs/protocol.md) for its boundaries and demonstration thresholds.

## Pilot v0.1 in detail

The first pilot uses one generation per task and condition, with a separate blinded judge call from the same model family. Its [protocol](pilots/hr_v01/protocol.md), [report](pilots/hr_v01/REPORT_en.md), [18 outputs](pilots/hr_v01/OUTPUTS.md) and [preparations and judgments](pilots/hr_v01/observed_outputs.json) remain available. The rating ceiling supports no conclusion about superiority.

## Research and development

The next study would need a complete hypothesis space, explicit guidance for revising an exhausted register and reliable preservation of workflow scope. Whether these changes improve new tasks must be tested on fresh material. The asymmetry between adding and removing fields also remains open.

See the [roadmap](docs/research-roadmap.md), [HR data card](docs/hr-example.md) and [offline verification instructions](docs/reproducibility.md). Contributions should use synthetic examples and include tests for changes to protocol behaviour.

Milad Morad. Developed with AI coding assistance. Code and fictional fixtures are released under the [MIT License](LICENSE). Cite the software version using [CITATION.cff](CITATION.cff).
