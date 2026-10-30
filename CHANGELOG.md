# Changelog

This record separates study history from software and documentation changes. Pilot numbers identify study stages, not software releases; the package version is `0.1.0.dev1`.

Research dates below are the event dates stated in the linked reports and protocols. Where studies entered Git later, the recording date is explicit. Software and documentation dates are Git commit or merge dates. Commit links identify the recorded changes; the three existing pilot tags identify research checkpoints. The reports retain the detailed findings and interpretation limits.

## Research record

### 2026-10-29 — Report errata and clarifications

- Added dated clarifications to the [v0.4 report](pilots/v04/DIFFICULTY_MAP_REPORT.md) about the stopped transport attempt and to the [v0.5 report](pilots/v05/DIFFICULTY_MAP_REPORT.md) about the keep floor, E2 arm comparison and diagnostic denominator. The sealed runs, analysis and scores were unchanged. [Commit `3bb3a6a`](https://github.com/miladmo/grounded-reflection/commit/3bb3a6a23ba1f325b99152a5580b8d87f30c0b91).
- Added the dated D failure-attribution clarification already recorded in the [v0.5 report](pilots/v05/DIFFICULTY_MAP_REPORT.md#why-d-falls-short). [Commit `b9edaea`](https://github.com/miladmo/grounded-reflection/commit/b9edaeacf3cd931e7b25b2e3a04d588f6dcb9901).

### 2026-10-03–04 — Pilot v0.5 main run and results

- Completed the main run on 3–4 October and finalized the [report](pilots/v05/DIFFICULTY_MAP_REPORT.md) on 4 October with both attribution-review parts incorporated. The run recorded 358 calls and three isolated response failures; failed and blocked tasks remain in their denominators. [Completion `4899cd5`](https://github.com/miladmo/grounded-reflection/commit/4899cd5892dd8c8061254cdc1fc2dfe42f16a023); [final report `747ef56`](https://github.com/miladmo/grounded-reflection/commit/747ef563228831f9d17183a46bfe83ed9cfd2768).
- Recorded the results checkpoint [`pilot-v05-results-20261004`](https://github.com/miladmo/grounded-reflection/tree/pilot-v05-results-20261004) at [commit `0386d21`](https://github.com/miladmo/grounded-reflection/commit/0386d21437a940cce7d02f87d1bf0a321415d7bb), following the README summary correction. Recorded the results-bundle SHA-256 in [commit `8654666`](https://github.com/miladmo/grounded-reflection/commit/865466650e43869b969971aeff02592ac624198e).

### 2026-10-01–03 — Pilot v0.5 preparation and freeze

- Approved the [v0.5 protocol](docs/pilot-v05-protocol.md) on 1 October, including the constructibility adjustment and calibration headroom criterion. [Commit `59bdd60`](https://github.com/miladmo/grounded-reflection/commit/59bdd60d36b43e93a6471a9e67d05ba77e6bbd1c).
- Revised materials after two reviews on 2 October, then recorded r3 approval and froze prompts. [r2 `cd9c975`](https://github.com/miladmo/grounded-reflection/commit/cd9c9751e81a6f038826d5b80a245286a910e70f); [r3 `757b87b`](https://github.com/miladmo/grounded-reflection/commit/757b87b01e846ebbd443af16c0b09c3b9a616731); [approval and prompt freeze `86c1e26`](https://github.com/miladmo/grounded-reflection/commit/86c1e26563cc69d2048030066035f48bda806fb8).
- Preserved two stopped calibration attempts and recorded the timeout correction on 3 October. The third calibration completed with headroom, so the reserved scientific amendment was unused. [Technical correction `7129302`](https://github.com/miladmo/grounded-reflection/commit/7129302f0b9d8d6efc39b7118844e7c49e2cf79e); [completed calibration `cc7d094`](https://github.com/miladmo/grounded-reflection/commit/cc7d09451d093c7f0046c4c9a2a264dcf4ae3605).
- Completed the second D technical check and froze D and all sources before the main run. [Check `ab01ec3`](https://github.com/miladmo/grounded-reflection/commit/ab01ec37cdebf08bb47727ef31b40f10601a0e08); checkpoint [`pilot-v05-frozen-20261003`](https://github.com/miladmo/grounded-reflection/tree/pilot-v05-frozen-20261003) at [commit `ecb4673`](https://github.com/miladmo/grounded-reflection/commit/ecb4673289357bbcaa6932baf9f5c7a6fd37139e).

### 2026-09-29–10-01 — Pilot v0.4 amendments and results

- Approved protocol amendments 1–3 and the material surface repair on 29 September. These recorded the fixed task mix, candidate-error measurement, H14 hypothesis class, transfer cases and material audits. Approved [Amendment 4](docs/pilot-v04-amendment-04.md), changing the model and transport, and [Amendment 5](docs/pilot-v04-amendment-05.md), specifying reasoning, output limit, PowerShell binding and isolated-response-failure handling, on 30 September. Recorded in Git on 1 October in [commit `8cb4ab7`](https://github.com/miladmo/grounded-reflection/commit/8cb4ab7563913909c0e4511364f0675dffd5af10); see the [protocol](docs/pilot-v04-protocol.md).
- Started the registered run on 30 September and recorded completion and attribution on 1 October. The [report](pilots/v04/DIFFICULTY_MAP_REPORT.md) separates registered scores from its dated, post hoc executed-fields correction; the registered metric was not rescored. Checkpoint [`pilot-v04-results-20261001`](https://github.com/miladmo/grounded-reflection/tree/pilot-v04-results-20261001) points to [commit `8cb4ab7`](https://github.com/miladmo/grounded-reflection/commit/8cb4ab7563913909c0e4511364f0675dffd5af10). Its annotation records publication sanitization and distinguishes the committed state from the archived run's bound source snapshot.

### 2026-09-29 — Pilot v0.3 calibration

- Completed two calibration rounds, with a prospective measurement-contract amendment before round 2. The [second-round report](pilots/v03/CALIBRATION_R2_REPORT.md) records the ceiling and stopped main comparison; grounded reflection was not run. The calibration records and implementation entered Git on 1 October in [commit `d25fd78`](https://github.com/miladmo/grounded-reflection/commit/d25fd78dc9f1fca5ad78f6989b6fd01445d3f6f8).

### 2026-09-28–29 — Pilot v0.2 results

- Conducted calibration on 28 September, including the documented round-2 material/scoring amendment, and the main study on 28–29 September. The [report](pilots/v02/REPORT_en.md) records 19/24 successful task attempts for grounded reflection and 23/24 for direct adaptation, retaining the frozen primary results alongside measurement limitations. Recorded in Git on 1 October in [commit `11c7172`](https://github.com/miladmo/grounded-reflection/commit/11c71721a2349ef1ab109d5cc28de8847670b7c2).

### 2026-09-15 — HR pilot v0.1

- Recorded the synthetic HR pilot, its frozen inputs and observed outputs. The [report](pilots/hr_v01/REPORT_en.md) documents a complete model-rating ceiling across all three conditions, with no observed method advantage. [Commit `c34a959`](https://github.com/miladmo/grounded-reflection/commit/c34a959d9e065c312697c01710d9cf4f2f7659b4).

## Software and documentation

### 2026-10-29

- [PR #5](https://github.com/miladmo/grounded-reflection/pull/5) aligned arm names, added the current v0.4 reading entry and restored original source documents beside public explanations. [Merge `94b248c`](https://github.com/miladmo/grounded-reflection/commit/94b248c787a93788a54908000590f29ed0381291).
- [PR #4](https://github.com/miladmo/grounded-reflection/pull/4) separated public methods and verification guidance from study provenance, foregrounded findings and explained the difficulty criterion. [Merge `ee6e880`](https://github.com/miladmo/grounded-reflection/commit/ee6e8804cfaa72834c0c29c95eeef0aa979ef5a9).
- [PR #3](https://github.com/miladmo/grounded-reflection/pull/3) added the shared glossary and pilot reader guides, separated registered and post hoc findings, and incorporated the dated report clarifications listed above. [Merge `5be3877`](https://github.com/miladmo/grounded-reflection/commit/5be3877de73b54a7069623df8a2810f3eaee4e5e).

### 2026-10-04

- [PR #2](https://github.com/miladmo/grounded-reflection/pull/2) removed duplicated README material and updated outdated pilot wording. [Merge `4510ff3`](https://github.com/miladmo/grounded-reflection/commit/4510ff326dd29d9d8ee4666a085371746e2e71dc).
- [PR #1](https://github.com/miladmo/grounded-reflection/pull/1) added the pilot overview, study/software version distinction, research next steps, gateway description and citation repository URL. It also skipped the Windows-specific PowerShell path test on other systems and recorded that deviation from the frozen source binding. [Merge `413bec4`](https://github.com/miladmo/grounded-reflection/commit/413bec4b768356b8439df6d7062322eacf0824bb).

### 2026-10-02–03

- Added v0.5 arms, runner and material-review export on 2 October. [Commit `7325df5`](https://github.com/miladmo/grounded-reflection/commit/7325df50c42b4fd09a1c2703342dc46eb66d39c8).
- Fixed two D query-contract defects found by the first technical check on 3 October: `any` filtering and wrapper-aware result budgeting. Prompts and strategy were unchanged. [Commit `1b49052`](https://github.com/miladmo/grounded-reflection/commit/1b4905271dcfdee93583253a63e4ac361797a047).

### 2026-09-15

- Introduced the research prototype and development library with evidence contracts, reference/scope checks, selection workflow, offline demo, CLI and tests. [Introduction `a2deb28`](https://github.com/miladmo/grounded-reflection/commit/a2deb283eddfa5ac15b4ccc71bcc3275e6005697); [library `c34a959`](https://github.com/miladmo/grounded-reflection/commit/c34a959d9e065c312697c01710d9cf4f2f7659b4). Added a recorded evidence-to-update README example in [commit `8a3225e`](https://github.com/miladmo/grounded-reflection/commit/8a3225e26cdbaea19f9e520de3d7e4d17e3f21cc).
