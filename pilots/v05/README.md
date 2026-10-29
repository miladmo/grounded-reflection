# Pilot v0.5: finding where direct evidence stops being enough

## Summary

Can direct use of work evidence still solve a task when the history is large and the relevant context attributes are unknown, and can a hypothesis register improve accuracy or cost? This pilot compares four methods across four synthetic settings with one model. Direct use (B) solved 44 of 48 diagnostic tasks, chunked preparation (C) 39, hypothesis register (D) 29, and no history (A) 24. D did not improve accuracy. Its main problems were an incomplete hypothesis register and loss of workflow scope. Post-run review identified specification ambiguity that may have contributed. These results diagnose one implementation under explicit synthetic rules. They do not establish that reflection in general is ineffective.

This guide explains the design, results and limitations. See [Methods](../../docs/methods.md#pilot-v05) for the shared experimental logic and [Reproducibility](../../docs/reproducibility.md) for verification. The [glossary](../../docs/glossary.md) defines study terms. Original protocols and execution records are indexed under [Provenance](../../docs/provenance.md#pilot-v05).

## Why this pilot

[Pilot v0.4](../v04/GUIDE.md) tested histories that fitted within one model call, with two known context dimensions and explicit approval rules. It did not establish the registered level of room for improvement by reflection. Its registered metric included declared-rule scope, so the score difference did not directly measure differences in executed task fields. A separate analysis of executed fields found B at 23 of 24 diagnoses and C at 21 of 24. Those figures were post hoc in v0.4.

Pilot v0.5 changes the challenge. It varies history size and whether the relevant attributes are named. It adds D, which proposes hypotheses and searches for evidence that distinguishes them. It also registers executed output fields as the primary outcome for every arm. This is a new design with fresh cases, not a rerun or a direct performance comparison with v0.4.

## Design at a glance

### Settings and evidence

Each history contains six attributes with two possible values each. A requirement may depend on at most two attributes.

| Setting | Relevant attributes | History size |
| --- | --- | ---: |
| K-S | Known: the two relevant attributes are named | Small: 24 records |
| K-L | Known: the two relevant attributes are named | Large: 240 records |
| U-S | Unknown: the relevant attributes must be found among six | Small: 24 records |
| U-L | Unknown: the relevant attributes must be found among six | Large: 240 records |

Every history has one workflow registration and 12 binding approvals. Small histories add 11 distractors, large histories 227. Increasing size adds surrounding material, not more binding evidence. The five distractor types are unauthorised revisions, rejected outputs, personal preferences, approvals that do not review the target field, and transient technical failures. Copies, forwarded approvals and version changes from v0.4 are not used here.

A **binding approval** is an accepted review by an authorised reviewer, within the registered validity period, that explicitly covers the target field. The model receives these conventions. It must apply all of them to decide which records constrain a requirement.

### Methods, called arms

| Arm | What it does |
| --- | --- |
| A, no history | Receives the future task, initial configuration and public task contract, but no historical evidence. |
| B, direct use | Retrieves historical records for the future task. Registrations come first, then accepted reviews that name the target field, then other records ranked by context match and recency. Retrieval does not decide whether a reviewer is authorised or an approval is valid. |
| C, chunked preparation | Reads the history in consecutive chunks and carries forward proposed guidance. C1 is the chunk-processing stage. C2 consolidates that guidance and cited records. Future tasks receive applicable guidance rather than the original history. |
| D, hypothesis register | Starts with an index of the history, proposes candidate functions in a hypothesis register, and requests records through structured queries. It updates the register through at most six rounds, with at most three queries per round. D-final turns the register into guidance for future tasks. |

All arms use `deepseek-ai/DeepSeek-V4-Flash-0731` through the institutional model gateway FHGenie with reasoning `high`. Each call permits 24,000 input tokens and at most 32,768 output tokens. C and D each have a 300,000-token preparation cap per history. Generation has a separate reservation so preparation cannot consume the budget for future tasks. These are common limits, not equal actual token use.

### Tasks and the oracle

There are four histories per setting, one each from synthetic human resources, sales, retrieval and reporting families. Every history has one observed change, one observed retention, one hard diagnostic, and one control outside the workflow. The four hard diagnostics per setting comprise two transfer changes and two unidentifiable cases. Adding or setting a field and omitting a field are balanced within each hard type.

An observed task uses a context covered by binding evidence. A transfer task asks for a change in a context not directly observed. An unidentifiable task has several explanations that fit the available evidence but disagree at the task context. The warranted action there is to keep the initial configuration. A control checks that a rule is not applied outside its workflow.

Each arm therefore faces **12 diagnostics and four controls per setting**, or **48 diagnostics and 16 controls overall**. Each hard type has only two cases per setting and arm.

The deterministic **oracle** computes which actions the public evidence warrants. It does not read the generator's intended answer. In known settings it considers **H14**, the 14 Boolean functions over two attributes except the two exclusive-or patterns. In unknown settings it considers **H134**, the 134 distinct functions over six attributes that depend on at most two attributes and use the same restricted forms. These forms include constants, individual value tests, and conjunctions or disjunctions of two tests. A test may refer to either value of an attribute.

The oracle retains every function consistent with the binding approvals. It authorises a change only when those functions agree at the task context. Their agreement, rather than a plausible guess, licenses transfer. If they disagree, the evidence is insufficient. The restriction to H14 or H134 is part of the experimental assumptions and supplies information needed for transfer.

### A worked example

This simplified illustration explains v0.4 and the known-attribute settings of v0.5. **It is not an observed pilot case or model output.** Repeated approvals and distractors are omitted.

Suppose an agent produces reports without a review-status footer. Authorised reviewers, within the current workflow and version, have explicitly accepted these outcomes for that field:

| Audience | Content | Accepted footer state |
| --- | --- | --- |
| Internal | Public | Absent |
| External | Public | Present |
| Internal | Sensitive | Present |

These observations suggest the requirement “include the footer for an external audience or sensitive content”. Checking all rules in the supplied H14 class leaves only this OR rule. The initial configuration alone would not establish any requirement.

A future report is both external and sensitive, a combination absent from the observations. Within the same workflow and version, the remaining rule requires the footer. This is **transfer**. The expected output field is therefore “present”; omitting it would fail the executed-field check.

The class restriction matters. XOR, meaning “external or sensitive, but not both”, also fits the three observations yet would omit the footer on the new report. H14 explicitly excludes XOR. Thus transfer follows from the evidence **and** a supplied assumption. These records do not justify applying the rule in another workflow. In v0.5's unknown-attribute settings, finding which attributes matter is an additional challenge.

### Measurement and decision rules

The **registered primary metric** compares the executed output fields with the oracle's expected fields, identically for all arms. Failed or blocked outputs remain incorrect in the fixed denominator. Controls are reported separately. Declared rules, decision labels, scope, evidence coverage, hypothesis-register behaviour and token use are secondary diagnostics. Error attribution was reviewed by the author (Milad Morad). Post-run explanations are labelled as such below.

The **calibration headroom criterion** asks whether direct methods are at ceiling before testing D. Calibration uses two histories per setting, with one transfer and one unidentifiable diagnostic, so its hard-task denominator is two rather than the main run's four. No headroom exists only if the better of B and C solves every hard calibration diagnostic in all four settings. For example, scores of 2/2, 2/2, 2/2 and 1/2 for the better direct arm leave headroom. This was the actual result. In U-L, B missed the unidentifiable case and C missed the transfer case, so each scored 1/2. Selecting the correct answer from either arm separately for each task would be a different rule. The one permitted difficulty amendment was not used.

This criterion differs from v0.4's threshold on C accuracy and the share of substantive errors. It also differs from the four **main-run expectations**, specified before the run:

- **E1, selection difficulty.** The better of B and C should score lower with large histories than with matching small histories.
- **E2, uncertainty about attributes.** The better of B and C should score lower when relevant attributes are unknown, especially on hard tasks.
- **E3, D accuracy.** D should solve at least two more diagnostics than the better direct arm in each setting.
- **E4, D cost.** Where D is at least as accurate, it should use at most 70 percent of the better direct arm's tokens.

These are descriptive expectations, not significance tests. Calibration headroom did not predict that D would succeed.

## Results

The following tables reproduce the primary-outcome tables in the [full report](DIFFICULTY_MAP_REPORT.md#primary-outcome). Technical failures remain in these fixed denominators; see [execution details](#what-happened).

| Arm | Observed change | Observed retention | Transfer | Unidentifiable | Control |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | 0/16 | 16/16 | 0/8 | 8/8 | 16/16 |
| B | 14/16 | 16/16 | 7/8 | 7/8 | 16/16 |
| C | 12/16 | 14/16 | 6/8 | 7/8 | 13/16 |
| D | 6/16 | 14/16 | 2/8 | 7/8 | 12/16 |

Read each cell as correct tasks divided by all planned tasks of that type. The first four columns sum to 24/48 for A, 44/48 for B, 39/48 for C and 29/48 for D. Controls do not enter those totals.

| Setting | A | B | C | D | B observed / hard | C observed / hard | D observed / hard | Controls A, B, C, D |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| K-S | 6 | **12** | **12** | 7 | 8/8, 4/4 | 8/8, 4/4 | 5/8, 2/4 | 4, 4, 4, 2 |
| K-L | 6 | 10 | **11** | 7 | 6/8, 4/4 | 8/8, 3/4 | 5/8, 2/4 | 4, 4, 4, 3 |
| U-S | 6 | **12** | 10 | 9 | 8/8, 4/4 | 6/8, 4/4 | 6/8, 3/4 | 4, 4, 4, 3 |
| U-L | 6 | **10** | 6 | 6 | 8/8, 2/4 | 4/8, 2/4 | 4/8, 2/4 | 4, 4, 1, 4 |

The A–D columns have denominator 12. Each control count has denominator four. Bold values mark the best direct score. The **keep floor** is 6/12, from four observed retentions and two unidentifiable tasks. A reaches it without learning a requirement.

### Reading corrections, 29 October 2026

Three clarifications preserve the original results while making the report readable:

1. The original keep-floor paragraph said “two retentions”. It should say **four**, plus two unidentifiable tasks.
2. “16 diagnostics per setting and arm” in the report's original limits should read **12 diagnostics plus four controls**. The same typo appears in the protected protocol's limits. The protocol is preserved, not rewritten.
3. The E2 row “U-L vs K-L” gives “hard 2 vs 4”. The archived analysis chooses the best overall score and the best hard score separately. In K-L, C has the best overall score, 11/12, with **3/4 hard**, while B has **4/4 hard** and 10/12 overall. A comparison following the same selected arm is therefore B in U-L at 10/12 with 2/4 hard versus C in K-L at 11/12 with 3/4 hard. The archived JSON explicitly names `arm: C` and `hard_arm: B`; its separate maxima are not new or corrected scores.

See the [report](DIFFICULTY_MAP_REPORT.md) for visible errata and the unchanged [machine analysis](analysis/main-analysis.json) for the original fields.

## What the results mean

- **Registered outcome.** D was less accurate than the better direct arm in every setting. E3 was not met. E1 was formally met, E2 was only partly consistent, and E4 was not applicable because D never reached equal accuracy. [Expectations and verdicts](DIFFICULTY_MAP_REPORT.md#prespecified-expectations).
- **Post hoc attribution.** All three B/C failures decisive for E1 and E2 had complete binding evidence in context. One C failure missed warranted transfer, one B failure adopted an unsupported rule, and another B failure missed an omission requirement. This does not demonstrate that retrieval or selection caused the accuracy differences. Technical C failures also weaken the U-L comparison. [Reviewed cases](review/attribution-20261004/CASES.md).
- **Post hoc attribution, mixed model and specification.** In 15 of 16 D registers, value tests covered only second-listed attribute values. For example, a register could consider “recipient is external” while omitting “recipient is internal”. This illustrates the missing alternative, not an additional observed case. The class wording may have contributed. The round prompt did not explicitly instruct D to add missing hypotheses or rebuild an exhausted register, although the response schema and runner allowed an updated hypothesis list. This identifies missing guidance, not a technical prohibition on additions. Ten registers eliminated every candidate and fell back to keeping the configuration. In the three histories where D retained the true function, it solved all nine diagnostics. [D analysis](DIFFICULTY_MAP_REPORT.md#why-d-falls-short).
- **Post hoc scope diagnosis.** Finding a rule did not ensure safe application. Only one of nine adopted D rules named its workflow, compared with 20 of 22 C rules. D failed four of 16 controls. The register and final guidance did not reliably preserve the registration's scope. [D analysis](DIFFICULTY_MAP_REPORT.md#why-d-falls-short).
- **Interpretation.** This implementation exposes a failure in proposing a complete hypothesis space and preserving scope, rather than a clean test of reflection against direct adaptation. D was cheaper in large histories but also less accurate. Its register and query mechanism cannot be assessed separately from this run. [Costs](DIFFICULTY_MAP_REPORT.md#prespecified-expectations), [limits](DIFFICULTY_MAP_REPORT.md#interpretation-limits).

## What the results do not show

This is a descriptive study with one model and two cases per hard type, setting and arm. Differences of a few tasks are not evidence of general superiority. Technical failures remain in the primary scores. The specification ambiguity prevents a clean attribution of D's result to reasoning ability alone.

The tasks use synthetic placeholder workflows, explicit approval conventions and a restricted rule class. Hard tasks were constructed so nearest-neighbour similarity gives the wrong answer. They are a stress test, not an estimate of how often such situations occur in professional work. The study does not demonstrate discovery of unrestricted implicit requirements, enterprise value, generalisation to other models, or the success or failure of Grounded Reflection as a broad approach.

Preparation was sealed before future tasks were generated. There is one disclosed earlier constructibility check: revision-r2 final-history seed 45061 was generated once in memory. The future-task and call-order seeds were not used, contents were not inspected or saved, and no generator change followed that check. See [separation and review](../../docs/methods.md#separation-and-review) and the original records indexed under [Provenance](../../docs/provenance.md#pilot-v05).

### Open questions

- Would a complete register that explicitly allows both attribute values, supports new hypotheses and preserves workflow scope improve D? That requires fresh material and a new protocol, not rescoring this run.
- Does the pattern of missed omission requirements persist beyond these small cells and this model? The [report](DIFFICULTY_MAP_REPORT.md#b-and-c) treats it as a limited observation.
- Full external reanalysis requires the preserved original run archive. Its permanent access location is not specified in the public repository. The archive name and hash are recorded in [publication sanitization](PUBLICATION_SANITIZATION.md#archive-of-originals).

## What happened

| Date in 2026 | Step | Outcome | Evidence |
| --- | --- | --- | --- |
| 1 October | Protocol and constructibility | Design and decision rules recorded before the evaluated runs. | [Methods](../../docs/methods.md#pilot-v05) |
| 2 October | Material reviews and revisions | First and second exports exposed shortcuts. Revision r3 repaired the materials before calibration. | [Material history](../../docs/provenance.md#pilot-v05) |
| 2 October | Calibration attempt 1 | Session time limit killed the background process after 13 valid calls. One further call had unknown usage. | [Incident](runs/live-calibration-20261002-INCIDENT.md) |
| 2 October | Calibration attempt 2 | 18 calls, including one format failure and one timeout. Unknown usage stopped the run before generation. | [Incident](runs/live-calibration-20261002-attempt2-INCIDENT.md) |
| 3 October | Technical correction | Call timeout increased from 420 to 1,200 seconds. | [Incident and correction](runs/live-calibration-20261002-attempt2-INCIDENT.md) |
| 3 October | Calibration attempt 3 | Completed 127 calls and 1,861,787 tokens. Headroom found by the registered rule. No difficulty amendment. | [Report](runs/live-calibration-20261003-attempt3/REPORT.md) |
| 3 October | First D technical check | Four calls. Found an incorrect `any` filter and missing budget for query-result wrappers. Both were contract defects. | [Incident](runs/live-dcheck-20261003-INCIDENT.md) |
| 3 October | Second D technical check | Six calls. Query execution and response format passed after those contract fixes. No scoring. | [Report](runs/live-dcheck-20261003-attempt2/REPORT.md) |
| 3 October | Freeze | D and study sources frozen before the main run. | [Source record](FROZEN-SOURCES.json) |
| 3–4 October | Main run | 358 calls, 4,954,459 tokens, no halt or unknown usage. Three isolated response failures retained. | [Machine report](runs/live-main-20261003/REPORT.md) |
| 4 October | Attribution and final report | Decisive errors reviewed. No repair or follow-up run. | [Cases](review/attribution-20261004/CASES.md), [full report](DIFFICULTY_MAP_REPORT.md) |

The two incomplete calibration attempts generated no future tasks or scores. Their preparation contents were not inspected. They are not additional performance results. The main run had no retries or replacement calls.

In the main run, two malformed C1 responses made C unavailable for two U-L histories. All eight planned C tasks in those histories count as incorrect, including six diagnostics and two controls. One B generation failed in transport and also counts as incorrect. These failures are not removed to improve the reported results.

## Verify it yourself

| Question | File to inspect |
| --- | --- |
| Counts by setting, arm and task type; main-run usage | [Machine report](runs/live-main-20261003/REPORT.md) |
| Diagnostic totals, selected arms, separate hard maxima, costs and D diagnostics | [Analysis JSON](analysis/main-analysis.json) |
| Definitions and prespecified criteria | [Methods](../../docs/methods.md#pilot-v05), [measurement](../../docs/methods.md#measurement) |
| Error explanations and the author's attribution | [Full report](DIFFICULTY_MAP_REPORT.md), [reviewed cases](review/attribution-20261004/CASES.md) |
| Main-run file hashes | [Run manifest](runs/live-main-20261003/manifest.json) |
| Frozen source and prompt hashes | [Source record](FROZEN-SOURCES.json), [prompt record](prompts/FROZEN.json) |
| What is public and what requires the original archive | [Verification boundary](../../docs/reproducibility.md#verification-boundary), [publication record](PUBLICATION_SANITIZATION.md) |

After following the [installation instructions](../../docs/reproducibility.md), run the offline pilot tests from the repository root:

```console
python -B -m unittest discover -s tests -p 'test_pilot_v05*.py' -v
```

The tests use mock responses and require no API key. They check materials, arms, budgets, failure handling, seals and the runner. Passing them verifies implementation behaviour, not the reported model performance. The main run and calibration used Python 3.12.14 with Pydantic 2.13.5. The D technical checks used Python 3.11.9 with Pydantic 2.10.6.

[main_analysis.py](analysis/main_analysis.py) is the offline recomputation script. It verifies the full run seal, then writes `analysis/main-analysis.json`. **Do not run it in the preserved results checkout merely to read the results.** It requires the complete original run data, which are not published, and it overwrites the existing analysis file. Reanalysis requires a separate working copy of the original archive to preserve the archived result.

The [seal verifier](reflectai_v05/storage.py) can check the complete original run directory, including its preparation and evaluator files. A public checkout contains selected reports and manifests, not raw prompts, responses and transport metadata. It can verify the hashes of available files but cannot reproduce a complete directory seal from missing files.

The [publication record](PUBLICATION_SANITIZATION.md#change-after-publication-windows-only-test-skipped-elsewhere) also documents a later Windows-only test skip. That changed a source-bound test file, so today's source tree does not exactly match `FROZEN-SOURCES.json`. The original test remains at tag `pilot-v05-results-20261004` and in the original archive. Do not treat the current source tree as an exact recreation of the frozen experiment. This guide and the report errata explain the archived study without changing its runs, prompts, analysis or registered metrics.
