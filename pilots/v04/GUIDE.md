# Pilot v0.4 reader's guide

## 1. Summary

This pilot asks where a strong direct-adaptation procedure loses decisions justified by its evidence. It compares current-task-only generation, direct use of historical evidence, and two-pass preparation of reusable guidance across six synthetic settings. The registered metric gives preparation arm C 21/24 correct diagnostics and direct-use arm B 16/24. That metric also checks the scope of declared rules. An existing post hoc check of the fields actually produced gives B 23/24 and C 21/24. No setting establishes the registered difficulty threshold called *headroom*. The study therefore does not show that explicit preparation improves task decisions over direct use of evidence. See the [interpretive report](DIFFICULTY_MAP_REPORT.md) and [shared glossary](../../docs/glossary.md).

This guide is the new reading entry point. The [original README](README.md) is listed in a historical [copy-verification record](preflight/fhgenie-20260929/copy-verification.json), so it remains unchanged. Its dated preparation updates include pending steps that were later completed. Use the timeline below for the final execution status.

## 2. Why this pilot

In the preceding v0.3 calibration, B and C each passed 8/8 tasks. Short, already interpreted records and supplied assumptions about stable, independent evidence may have made inference too easy. These were possible explanations, not established causes. Version 0.4 varies presentation, volume, provenance and time validity to look for failures of C that concern inference rather than transport or formatting. It is a difficulty map, not a test of a new grounded-reflection treatment. Arm D is excluded. The [registered protocol](../../docs/pilot-v04-protocol.md#purpose) explains this transition.

## 3. Design at a glance

A *history* is a collection of synthetic work records. Each history supplies one new diagnostic task and one control task. A diagnostic tests an intended inference challenge. A control checks that an adaptation does not change another context without support.

| Arm | What the model receives | Procedure |
| --- | --- | --- |
| A | Current task, initial configuration and shared execution contract | Generate without historical evidence |
| B | A's inputs plus the complete corresponding history | Use historical evidence directly on each task |
| C | The same history during preparation, then the current task and retained applicable guidance | C1 constructs guidance, C2 reviews it, then generation applies the retained guidance |

C1 and C2 are two preparation calls, not separate experimental arms. The inherited prompts already ask for alternatives, counterevidence, provenance and scope. C is a strong direct-adaptation comparison. It is not called the grounded-reflection arm in this study. B and C have the same historical records, but their computation budgets are not equal. The [arm specification](../../docs/pilot-v04-protocol.md#arms-and-execution) fixes these procedures.

| Setting | Evidence presentation | Records per history | Main variation |
| --- | --- | ---: | --- |
| S0, base | Interpreted observations | 6 | Independent origins and stable validity |
| S1, raw | Before/after artifacts and logs | 6 | Reconstruct observations from artifacts |
| S2, volume and noise | Interpreted observations | 60 | More records, including misleading signals |
| S3, dependence | Interpreted observations | 6 | Copies and forwards |
| S4, change over time | Interpreted observations | 6 | Documented version break |
| S5, combined | Before/after artifacts and logs | 60 | Volume, copies and version break together |

There are four histories per setting, using human resources (HR), sales, retrieval and reporting placeholders. These are synthetic task families, not evidence about industry practice. Each setting contains the same four task types.

| Task type | What is tested | Warranted diagnostic action |
| --- | --- | --- |
| Change with transfer | Infer an alternative for a previously unobserved combination of context values | Change |
| Change in an observed context | Apply evidence to a new work item in a previously observed context | Change |
| Resolved retention with transfer | Infer that a previously unobserved combination should retain the baseline | Keep, with support for the baseline |
| Unidentifiable change | Competing explanations disagree at the diagnostic context | Keep, without claiming the baseline is established |

*Transfer* means applying a rule to an unobserved combination of the supplied context values. Twelve diagnostics require change, six support retention and six leave the change unidentified. Of the twelve changes, six test transfer and six test an observed context. Family assignments rotate, but transfer changes occur twice in HR and reporting and once in sales and retrieval. The [fixed allocation](../../docs/pilot-v04-amendment-03.md#identical-task-mix-in-every-setting) documents this imbalance.

The 24 histories yield 24 diagnostics and 24 controls per arm. That is 144 generation calls plus 48 C preparation calls, or 192 planned calls. C preparation is frozen before future task instances are generated. The [separation rules](../../docs/pilot-v04-protocol.md#separation-sealing-and-leakage-protection) prevent preparation from seeing those tasks. The author (Milad Morad) knows the construction templates, so this is not an unseen confirmatory benchmark. Employee clarification questions are not allowed. Keeping the baseline under unresolved evidence is the study's convention, not a general deployment policy.

### What the oracle knows

The *oracle* is the deterministic evaluator that establishes what the public evidence warrants. A change is *warranted* only when every compatible rule requires it at the task context. When compatible rules disagree, the study requires keeping the baseline without treating it as established truth. A *binding approval* must come from an authorised reviewer, cover the target field and fall within the relevant validity interval. A forward, preference or unreviewed field is not such an approval under this synthetic contract.

The oracle enumerates H14, a supplied class of fourteen Boolean functions over two declared binary context dimensions. It includes constants, single conditions, conjunctions and disjunctions. It excludes the two checkerboard patterns, exclusive OR (XOR) and its complement (XNOR). Those exclusions can make transfer identifiable. They are assumptions of the experiment, not findings about workplace requirements.

Three objects remain separate. The private *world function* specifies the constructed truth. The oracle derives compatible functions from public evidence without consulting that truth or the intended regime. Task obligations then distinguish the correct action under that evidence from the fields required by the hidden world. If compatible functions disagree, retaining the baseline may be warranted even when the hidden world requires a change. See the [oracle specification](../../docs/pilot-v04-amendment-03.md#a-genuinely-structured-hypothesis-class) and [implementation](reflectai_v04/oracle.py).

The [worked example](../v05/README.md#a-worked-example) follows one illustrative requirement from accepted reviews to a new task and its expected output field. It uses the same H14 transfer logic as this pilot.

### Metrics and the headroom decision

The registered primary metric is correct warranted diagnostic action, including the scope of every declared applied rule. *Scope probes* are evaluator contexts that check whether a rule extends beyond supported workflow, version or context boundaries. Correct fields on one task do not by themselves pass this metric. Controls, hidden-world field compliance, candidate errors, directional transfer errors and tokens are reported separately. There is no weighted overall score.

A later, explicitly **post hoc** analysis checks only the executed fields against the warranted action. It uses the expected baseline for keep decisions and world fields for recoverable changes. It does not replace the registered metric. The three measurements are therefore distinct: declared-rule warrant, hidden-world field compliance and post hoc executed-field correctness.

*Headroom* is the prespecified exploratory flag for a setting where C is sufficiently unsuccessful, predominantly for content reasons, to motivate a subsequent method study. It requires at most 70% correct diagnostics and at least 60% pure content errors among all diagnostic failures. With four diagnostics, the first condition means at most 2/4 correct. Mixed or unresolved failures stay in the denominator but do not count as confirmed content errors.

For example, S4 has 2/4 correct, meeting the accuracy condition. Its two failures were both classified unresolved, so the confirmed content fraction is 0/2, not the required two of two. Headroom is therefore not established. The classification remains provisional because both cases would need a content attribution for the flag to hold. S1 has a confirmed content error but 3/4 correct, so it fails the accuracy condition. Candidate errors do not enter this gate. These rules are fixed in the [protocol](../../docs/pilot-v04-protocol.md#c-error-taxonomy).

## 4. What happened

| Date in 2026 | Step | Outcome and evidence |
| --- | --- | --- |
| 29 September | Initial protocol and Amendment 3 | Authorisation for implementation; restricted hypothesis class and fixed transfer cases specified in [Amendment 3](../../docs/pilot-v04-amendment-03.md) |
| 29 September | Material review and surface repair | Earlier examples exposed timestamp/comment shortcuts. Revision r2 varied surfaces without changing approval semantics; [r2 approval](review/materials-amendment3-r2-20260929-approvals.json) followed |
| 29 September | Original gpt-6-sol attempt | The command-line interface (CLI) attempt stopped on its first C1 call because an upstream HTTP-200 response lacked the required streaming content type. No usable response; 191 remaining calls blocked; usage unknown. See the [incident](runs/live-amendment3-r2-20260929-INCIDENT.md) |
| 29 September | FHGenie connection probes | Three separately approved toy probes used 173 reported tokens in total. The third returned valid JSON. These tested connectivity, not research tasks. See the [probe history](diagnostics/fhgenie/README.md) |
| 30 September | Model change and contract tests | [Amendment 4](../../docs/pilot-v04-amendment-04.md) selected DeepSeek-V4-Flash-0731 via FHGenie. Two reasoning-high contract tests each returned 16/16 valid responses, first at [16,384 output tokens](diagnostics/fhgenie/contract-test-high-20260930/run/REPORT.md), then at [32,768](diagnostics/fhgenie/contract-test-high-32k-20260930/run/REPORT.md) |
| 30 September | Final configuration and approval | [Amendment 5](../../docs/pilot-v04-amendment-05.md) fixed high reasoning, the 32,768 output limit and tolerance of up to 19 isolated response failures. The [approval record](review/materials-amendment3-r2-amendment5-20260930-approvals.json) binds the final configuration |
| 30 September to 1 October | Registered research run | Started at 21:16 UTC on 30 September. Completed 192/192 calls with no failed calls, retries or replacements. See the [machine report](runs/live-fhgenie-high-20260930/REPORT.md) |
| 1 October | Failure review and interpretation | The author confirmed two unresolved polarity inversions and one content error. The report also recorded the executed-fields interpretation. See the [attribution record](review/attribution-live-fhgenie-high-20261001/responses.json) and [report](DIFFICULTY_MAP_REPORT.md) |

The final [live-run authorisation request](preflight/fhgenie-high-20260930/LIVE_FREIGABE.md) keeps its German filename. `LIVE_FREIGABE` means live-run authorisation. The recorded response “Live-Lauf freigegeben, ausführen.” means “Live run approved, execute.” Earlier consumed permissions did not authorise replacement runs.

The stopped attempt, toy probes and contract tests are excluded from the research results. The stopped attempt's automatic zero scores represent blocked planned rows, not observed model performance. The model change also prevents direct comparison with v0.3.

## 5. Results

The following tables are copied from the [interpretive report](DIFFICULTY_MAP_REPORT.md#decisions-and-downstream-outcomes). The [sealed machine report](runs/live-fhgenie-high-20260930/REPORT.md#outcomes) preserves the registered breakdowns.

| Setting | Factor | C | B | C world fields | B world fields |
| --- | --- | ---: | ---: | ---: | ---: |
| S0 | base | 4/4 | 2/4 | 3/4 | 3/4 |
| S1 | raw artifacts | 3/4 | 3/4 | 4/4 | 3/4 |
| S2 | volume and noise | 4/4 | 2/4 | 3/4 | 2/4 |
| S3 | dependence | 4/4 | 4/4 | 3/4 | 3/4 |
| S4 | change over time | **2/4** | 3/4 | 1/4 | 3/4 |
| S5 | combined | 4/4 | 2/4 | 3/4 | 3/4 |
| **Total** | | **21/24** | **16/24** | 17/24 | 17/24 |

C and B columns count registered warranted diagnostics, including declared scope. World-field columns check the hidden truth instead. Registered controls are C 24/24 and B 23/24. A's warrant score is not comparable because A has no history; its world-field compliance is 6/24 diagnostics and 24/24 controls.

| Task type | C | B |
| --- | ---: | ---: |
| Change with transfer | 5/6 | 1/6 |
| Change in an observed context | 5/6 | 3/6 |
| Resolved retention with transfer | 6/6 | 6/6 |
| Unidentifiable change | 5/6 | 6/6 |

These are the same registered diagnostics grouped by task type. They are not additional observations.

| Diagnostics, executed fields | C | B |
| --- | ---: | ---: |
| All | 21/24 | 23/24 |
| Change with transfer | 5/6 | 5/6 |
| Change in an observed context | 5/6 | 6/6 |
| Resolved retention with transfer | 6/6 | 6/6 |
| Unidentifiable change | 5/6 | 6/6 |

This is the existing **post hoc** comparison. Seven of B's eight registered failures had correct output fields but declared rules missing workflow/version restrictions. On the fields actually produced, B was at least as accurate as C in this run. Executed controls are C 24/24 and B 23/24. The primary scores remain unchanged.

The report's [candidate-error section](DIFFICULTY_MAP_REPORT.md#candidate-errors) gives confirmed lower bounds for C1 and C2. Candidate counts depend on what the model emits and are not independent observations. Its [resource section](DIFFICULTY_MAP_REPORT.md#resource-use) reports 2,072,310 input-plus-output tokens with no unknown usage in the completed run. Conditional token amortisation assumes reusable guidance and unchanged task composition; it is not observed monetary savings.

## 6. What the results mean

- **Registered.** C passes 21/24 diagnostic cases including declared scope, versus B's 16/24. C passes all 24 controls. The [registered outcomes](runs/live-fhgenie-high-20260930/REPORT.md#outcomes) describe this model on these materials.
- **Post hoc.** The executed-fields comparison gives B 23/24 and C 21/24. The [1 October correction](DIFFICULTY_MAP_REPORT.md#decisions-and-downstream-outcomes) explains why the primary difference is not evidence that C makes better task decisions.
- **Registered criterion, reviewed attribution.** No setting establishes headroom. S4 remains provisional because both failures are unresolved. The [human attribution](review/attribution-live-fhgenie-high-20261001/responses.json) must be read alongside the machine report's earlier provisional labels.
- **Interpretation.** S4's version break coincides with an omission alternative in both change diagnostics. The [failure analysis](DIFFICULTY_MAP_REPORT.md#failure-causes-and-headroom) cannot separate those factors. A changed-baseline explanation remains unverified.
- **Interpretation.** Correctly scoped reusable guidance and lower generation-token use may matter independently of immediate task accuracy. The [existing report](DIFFICULTY_MAP_REPORT.md#interpretation-and-next-decision) treats this as a possible benefit under reuse assumptions, not demonstrated enterprise value.

## 7. What the results do not show

This pilot does not establish unrestricted learning of tacit requirements, professional output quality, enterprise utility or a benefit of grounded reflection over direct use. The hypothesis class, approval semantics, context dimensions and field operations are supplied. Materials are synthetic placeholders, histories share templates and there are only four diagnostics per setting. One model and reasoning level were tested, without deterministic model sampling. The family rotation and omission-direction confound limit comparisons between settings.

The counterfactual material audit demonstrates that misleading records could cause a wrong action or inconsistency if counted as approvals. It does not show that the model actually counted them that way. The surface audit checks simple individual features and does not exclude every shortcut. Review included AI assistance and attribution by the author; it is not independent field validation. See the [limits](DIFFICULTY_MAP_REPORT.md#limits).

Open scientific questions remain unchanged. The two S4 polarity inversions do not distinguish inference failure from plain misreading. The apparent role of omission needs a design that varies direction independently of temporal change. Token break-even projections need stable future use and maintenance assumptions that two future tasks per history cannot establish. Any next study needs a fresh protocol and fresh cases.

## 8. Verify it yourself

The public repository contains the protocol, source code, reports and selected review records. The [publication sanitization record](PUBLICATION_SANITIZATION.md) documents later changes to published transport code and other bound files. Published copies therefore cannot reproduce every historical binding; exact verification requires the unmodified originals. The complete sealed run archive contains additional raw calls, task data, score files and manifests. A public checkout alone does not provide those archive-only files and cannot fully verify the live-run seal or replay its evaluation. No new inference or rescoring is needed to read this guide.

| Question | Public evidence | Complete-archive files, relative to `pilots/v04/` |
| --- | --- | --- |
| Registered task counts and scores | [Machine report](runs/live-fhgenie-high-20260930/REPORT.md) | `runs/live-fhgenie-high-20260930/scores.json`, `results.json` |
| Preparation-level errors | [Machine report](runs/live-fhgenie-high-20260930/REPORT.md), [interpretation](DIFFICULTY_MAP_REPORT.md#candidate-errors) | `runs/live-fhgenie-high-20260930/candidate-scores.json` |
| Call completion and token totals | [Machine report](runs/live-fhgenie-high-20260930/REPORT.md#conditional-token-amortisation) | `runs/live-fhgenie-high-20260930/calls.json`, `planned-calls.json` |
| Post hoc output interpretation | [Dated correction and table](DIFFICULTY_MAP_REPORT.md#decisions-and-downstream-outcomes) | Preserved generation outputs in `runs/live-fhgenie-high-20260930/generation/` |
| Final failure attribution | [Reviewer responses](review/attribution-live-fhgenie-high-20261001/responses.json) and [supplied feedback](review/attribution-live-fhgenie-high-20261001/feedback-20261001.md) | Kept outside the sealed run; does not rewrite automatic scores |
| Run integrity | Seal identity recorded in the [report](DIFFICULTY_MAP_REPORT.md#registration-and-execution) and [review](review/attribution-live-fhgenie-high-20261001/responses.json) | `runs/live-fhgenie-high-20260930/manifest.json`, plus `preparation/manifest.json` and `evaluator/manifest.json` |
| Frozen implementation | [Source-binding description](reflectai_v04/storage.py) | `runs/live-fhgenie-high-20260930/sources/`, including `binding.json` |

The scoring code is [evaluation.py](reflectai_v04/evaluation.py): `score_output` evaluates tasks, `score_preparation` evaluates candidates, `aggregate` assembles registered summaries and `amortisation` calculates conditional token projections. [oracle.py](reflectai_v04/oracle.py) derives compatible policies. [runner.py](reflectai_v04/runner.py) orchestrates those functions and [report.py](reflectai_v04/report.py) writes the machine report. These describe the computation route; there is no dedicated read-only replay command. Running the study runner would create a new run, not verify this one. Do not overwrite a recorded report or regenerate its scores.

From the repository root, with Python 3.11 or later and the project dependencies installed, run offline tests without API calls:

```powershell
$env:PYTHONPATH = 'src;pilots/v03;pilots/v04'
python -B -m unittest discover -s tests -p 'test_pilot_v04*.py' -v
```

With the **complete archive** present, the following reads and verifies the exact file sets and SHA-256 checksums. It does not change scores or make model calls.

```powershell
$env:PYTHONPATH = 'src;pilots/v03;pilots/v04'
python -B -c "from pathlib import Path; from reflectai_v04.storage import verify_seal; r=Path('pilots/v04/runs/live-fhgenie-high-20260930'); print({str(p): verify_seal(p, p/'manifest.json')['sha256'] for p in (r, r/'preparation', r/'evaluator')})"
```

The recorded run seal is `7afab956742071b0c5ddd8d696e854630a2a6f25945a32d34e6ece3dddbb8594`. Seal verification establishes consistency with the preserved record. It does not establish scientific validity or reproduce a stochastic model response. The run's automatic attribution remains sealed; the later human classification is separate and dated.

## 9. History

The complete [original README](README.md#status) remains the historical implementation log, unchanged in substance and bytes by this documentation revision. Its initial mock run, Amendment 3 verification, rejected material review, surface repair, CLI preflight, stopped attempt, FHGenie integration and subsequent approval preparations are preserved with their original links. Its [offline instructions](README.md#run-offline) create new mock or review artifacts, not a reproduction of the completed live responses.

Read historical phrases such as “Live approval is pending”, “It has not been run” and “No v0.4 model result” as statements from the preparation stage they describe. The completed research run and 1 October attribution in sections 4–6 above are the final status. The [protocol and approval record](../../docs/pilot-v04-protocol.md#approval-record), the [incident](runs/live-amendment3-r2-20260929-INCIDENT.md) and the [final interpretive report](DIFFICULTY_MAP_REPORT.md) retain their evidential roles. This guide changes presentation only.
