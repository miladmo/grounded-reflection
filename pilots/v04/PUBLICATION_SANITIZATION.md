# Publication sanitization record

Prepared on 1 October 2026 before publication of pilots v0.2–v0.4, following decisions by Milad Morad. All changes are **retrospective**: they were made after the files were recorded, sealed, approved or executed. Changed files therefore do not reproduce the hashes in the seals, approvals or plans that bind them. The unmodified originals, including all full run folders and the exact code of every run, are in the archive below. Only the originals verify those bindings.

Archive: `grounded-reflection-originals-20261001.zip`, SHA-256 `822eb28069c67c2675133649edb6ef28f2d2fd9db6733489149b99b239cd6f2c`. It is stored outside this repository; its permanent location is chosen by Milad Morad.

## Decisions

* The industry partner is not named.
* Local user paths are replaced by `%USERPROFILE%`.
* Raw model responses, sealed source snapshots and CLI logs are not published.
* The FHGenie endpoint address is not published. The name FHGenie, the model and aggregated results may be public.

## Endpoint handling after the run

The transport no longer contains the address. It reads it from the environment variable `REFLECTAI_FHGENIE_ENDPOINT` or from `%LOCALAPPDATA%\reflectAI\fhgenie-endpoint.txt`, outside the repository. Before credential access or any request, both the Python transport and the PowerShell driver compare its SHA-256 with the pinned value `36247a636ec109c62faa6d828357e6027571e8f56e1c6890e8e0d169acc730db` and stop on a mismatch. This keeps the protection against redirection. It does not make the address secret: a guessed address can be checked against the published hash. Documents and records use the placeholder `<FHGENIE_ENDPOINT>`.

**The committed transport code was changed after the registered run.** The exact code of the contract tests and of the run `live-fhgenie-high-20260930` is in the archive (run folder `sources/` snapshot and the original files). Offline tests use the fixture address `https://fhgenie.invalid/v1/chat/completions`. The historical probe scripts and the `fhgenie.ps1` model-list helper now contain placeholders and are kept as records; they are not runnable as committed.

Further consequences: `preflight/fhgenie-high-20260930/run-config.json` no longer matches the live approval's configuration hash `23477ae8…678829`; both contract-test `plan.json` files no longer match their approved plan hashes; and the protocol was edited after the run to add approval records, so the committed sources differ from the run binding `1445c361…`.

## Modified files

71 committed files differ from their archived originals. Full hashes are in [publication-sanitization.json](publication-sanitization.json).

| File | Change | Original SHA-256 | Committed SHA-256 |
| --- | --- | --- | --- |
| `docs/pilot-v02-protocol.md` | industry partner name -> generic wording | `3e25574af8703daf…` | `5f64b73cf90cd135…` |
| `docs/pilot-v04-amendment-04.md` | endpoint address -> placeholder | `60d9f1a649e5d735…` | `bee0a12d32e70198…` |
| `docs/pilot-v04-fhgenie-transport.md` | endpoint address -> placeholder | `c6cf72d40732b641…` | `49766b6f98fa5510…` |
| `docs/pilot-v04-protocol.md` | industry partner name -> generic wording | `b617e48ef51bcda0…` | `0e25e6629e8f187c…` |
| `pilots/v02/DATA_CARD.md` | industry partner name -> generic wording | `95f8be08531c9397…` | `8be53a7262dd6512…` |
| `pilots/v04/.authorizations/7d34df38a9d28d2a97344c701c535c6e24eca468c66f9b983479d1d617f43550.json` | local user path -> %USERPROFILE% | `65bb256a37c73423…` | `ec28fdfa4402862d…` |
| `pilots/v04/.authorizations/cc618ad05f5a63333332c091ea8b3d4a5631530af98b4ece5ecf51ff836b793a.json` | local user path -> %USERPROFILE% | `be9938580fbc78dd…` | `3414f7992fe2029d…` |
| `pilots/v04/diagnostics/fhgenie/README.md` | endpoint address -> placeholder | `56aafee76049c37b…` | `175e1941c206314e…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/plan.json` | endpoint address -> placeholder; local user path -> %USERPROFILE% | `3ee95edd8d63481e…` | `7f81b96ac1980c64…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/run/calls/01-C1-C-H1/metadata.json` | endpoint address -> placeholder | `16bdc5826b171e3d…` | `eacb54a2a527468c…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/run/calls/02-C1-C-H2/metadata.json` | endpoint address -> placeholder | `78c95b35771b57fe…` | `c197f9afe6a1b5f2…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/run/calls/03-C1-C-H3/metadata.json` | endpoint address -> placeholder | `3b3edbeff2c08b13…` | `b62af6d1ca1fc117…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/run/calls/04-C1-C-H4/metadata.json` | endpoint address -> placeholder | `fae16568fb2758a9…` | `973389df693683f3…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/run/calls/05-C2-C-H1/metadata.json` | endpoint address -> placeholder | `33a9c62e8e5c097f…` | `edbb6c545999b4ce…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/run/calls/06-C2-C-H2/metadata.json` | endpoint address -> placeholder | `18063cc418c840e6…` | `5b88db643caf6674…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/run/calls/07-C2-C-H3/metadata.json` | endpoint address -> placeholder | `b6d88e84e2127151…` | `8c4ec1ebd470fd51…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/run/calls/08-C2-C-H4/metadata.json` | endpoint address -> placeholder | `e3002cef858393aa…` | `017d7d38128e3b87…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/run/calls/09-gen-C-H1/metadata.json` | endpoint address -> placeholder | `c2d9643823c4c713…` | `f6368a36efb90212…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/run/calls/10-gen-C-H2/metadata.json` | endpoint address -> placeholder | `7ff1d47d346bb1f8…` | `b9626d022119bc88…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/run/calls/11-gen-C-H3/metadata.json` | endpoint address -> placeholder | `586e1d8d48e11136…` | `b6e08fb900cbe9f6…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/run/calls/12-gen-C-H4/metadata.json` | endpoint address -> placeholder | `04d24e90cd92d79b…` | `a0b7719f86eed138…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/run/calls/13-gen-B-H2/metadata.json` | endpoint address -> placeholder | `bdb5ba178d1f1e0e…` | `0ee89bcb6fd63490…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/run/calls/14-gen-B-H4/metadata.json` | endpoint address -> placeholder | `0bb7b0717e7ad654…` | `ca2d92f93787b7cd…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/run/calls/15-gen-A-H1/metadata.json` | endpoint address -> placeholder | `7f6baa50284fbaab…` | `e58ce58b605b836d…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/run/calls/16-gen-A-H3/metadata.json` | endpoint address -> placeholder | `a4a0a0d08d9d9ad8…` | `053b0a833974a025…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/test_contract_test.py` | transport code/tests changed after the run: endpoint read locally and verified by SHA-256 | `613001b34b237bff…` | `00ea7b6983091fac…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/plan.json` | endpoint address -> placeholder; local user path -> %USERPROFILE% | `c0fd147d987f5e31…` | `ab65a6c6b4b15bf4…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/run/calls/01-C1-C-H1/metadata.json` | endpoint address -> placeholder | `a4de4eabcb996028…` | `4ebdfce0c839f988…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/run/calls/02-C1-C-H2/metadata.json` | endpoint address -> placeholder | `b5ab0e4ec2bcc8f7…` | `097c0716fe390e53…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/run/calls/03-C1-C-H3/metadata.json` | endpoint address -> placeholder | `7c70932fd063f21c…` | `6f609ecbeff31cd9…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/run/calls/04-C1-C-H4/metadata.json` | endpoint address -> placeholder | `a9a733a149e8e8ca…` | `d0e025399229df07…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/run/calls/05-C2-C-H1/metadata.json` | endpoint address -> placeholder | `ba1d911dd917d935…` | `838412b7e3f9e34f…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/run/calls/06-C2-C-H2/metadata.json` | endpoint address -> placeholder | `5c091b6ac6d0e64d…` | `a4069e844c71e97e…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/run/calls/07-C2-C-H3/metadata.json` | endpoint address -> placeholder | `0da449af65cb90d6…` | `24d2ca3188dd9af8…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/run/calls/08-C2-C-H4/metadata.json` | endpoint address -> placeholder | `7a446e9a50fdfd54…` | `6af7e20c778e3551…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/run/calls/09-gen-C-H1/metadata.json` | endpoint address -> placeholder | `fa2d69d2af1916ba…` | `e5157623bfe32ab5…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/run/calls/10-gen-C-H2/metadata.json` | endpoint address -> placeholder | `bad53808604d71a6…` | `97d3843aa7ff3783…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/run/calls/11-gen-C-H3/metadata.json` | endpoint address -> placeholder | `80889e1cf7f4ec88…` | `580ac97feaeadf43…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/run/calls/12-gen-C-H4/metadata.json` | endpoint address -> placeholder | `81502f203af8bf06…` | `f135c170ef7e3fa5…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/run/calls/13-gen-B-H2/metadata.json` | endpoint address -> placeholder | `185c9e3a6e439b41…` | `b6db34b42f5d5f14…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/run/calls/14-gen-B-H4/metadata.json` | endpoint address -> placeholder | `4dc7844bef66036a…` | `7a6868ca00d437ec…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/run/calls/15-gen-A-H1/metadata.json` | endpoint address -> placeholder | `492949aef669498b…` | `7165fdf9c7aea7d7…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/run/calls/16-gen-A-H3/metadata.json` | endpoint address -> placeholder | `b1ef9e778b9a353c…` | `b88c4e0293d0527f…` |
| `pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/test_contract_test.py` | transport code/tests changed after the run: endpoint read locally and verified by SHA-256 | `6e4abf4942fbf259…` | `8554b87bbfa7d545…` |
| `pilots/v04/diagnostics/fhgenie/fhgenie.ps1` | endpoint address -> placeholder | `ce88f8baa8d3f9c0…` | `5f7440b992d5ed81…` |
| `pilots/v04/diagnostics/fhgenie/probe-v1-20260929/plan.json` | endpoint address -> placeholder | `36b4df7f563f9aaf…` | `099b194108c201d7…` |
| `pilots/v04/diagnostics/fhgenie/probe-v1-20260929/probe.ps1` | endpoint address -> placeholder | `9042d3f2c14e621b…` | `6541110990f97f54…` |
| `pilots/v04/diagnostics/fhgenie/probe-v1-20260929/test_probe.ps1` | endpoint address -> placeholder | `8ff3e9a022001a46…` | `338dd247028266d5…` |
| `pilots/v04/diagnostics/fhgenie/probe-v2-20260929/plan.json` | endpoint address -> placeholder | `1eebe9265fb3f9a1…` | `b7900de453806479…` |
| `pilots/v04/diagnostics/fhgenie/probe-v2-20260929/probe.ps1` | endpoint address -> placeholder | `86371eb4efe5598f…` | `17023c1a3b19b68f…` |
| `pilots/v04/diagnostics/fhgenie/probe-v2-20260929/test_probe.ps1` | endpoint address -> placeholder | `dd66f4a8a9a88110…` | `9bcf0f143805fc37…` |
| `pilots/v04/diagnostics/fhgenie/probe-v3-20260929/plan.json` | endpoint address -> placeholder | `80394dfa9a9d583f…` | `0206620522b3ce46…` |
| `pilots/v04/diagnostics/fhgenie/probe-v3-20260929/probe.ps1` | endpoint address -> placeholder | `96db898efce1125d…` | `a9232460619c0524…` |
| `pilots/v04/diagnostics/fhgenie/probe-v3-20260929/test_probe.ps1` | endpoint address -> placeholder | `66e7438cde506351…` | `7b1f485fc3e8e8ac…` |
| `pilots/v04/diagnostics/fhgenie/test_fhgenie.ps1` | endpoint address -> placeholder | `fe05f0a125c20806…` | `ad0b9818662f0691…` |
| `pilots/v04/diagnostics/transport-smoke-20260929/attempt/summary.json` | local user path -> %USERPROFILE% | `c1f1d5ec9d180619…` | `1856d0bb87d10da1…` |
| `pilots/v04/diagnostics/transport-smoke-v2-20260929/attempt/summary.json` | local user path -> %USERPROFILE% | `b07faba9ac880570…` | `72ffd4fda337aec6…` |
| `pilots/v04/diagnostics/transport-smoke-v3-20260929/capture_local.py` | local user path -> %USERPROFILE% | `86c5719165380975…` | `329aa623aea91917…` |
| `pilots/v04/preflight/fhgenie-20260929/LIVE_FREIGABE.md` | endpoint address -> placeholder | `70ad8897fbfd65a8…` | `e585b54b8cab487e…` |
| `pilots/v04/preflight/fhgenie-20260929/copy-verification.json` | local user path -> %USERPROFILE% | `509bbc535a02e375…` | `36c04d0a44a2b4e8…` |
| `pilots/v04/preflight/fhgenie-20260929/run-config.json` | endpoint address -> placeholder | `54a65d9ec390e2d1…` | `ad78c4c6e57583bc…` |
| `pilots/v04/preflight/fhgenie-high-20260930/LIVE_FREIGABE.md` | endpoint address -> placeholder | `6d14266991c24596…` | `bb1cd6084b066ca1…` |
| `pilots/v04/preflight/fhgenie-high-20260930/run-config.json` | endpoint address -> placeholder; local user path -> %USERPROFILE% | `d0da743cb0c49fcd…` | `378b349d6d1a1028…` |
| `pilots/v04/preflight/fhgenie-high-20260930/verification.json` | endpoint address -> placeholder; local user path -> %USERPROFILE% | `8e760984aaef5e35…` | `5b89802a62027c17…` |
| `pilots/v04/preflight/live-20260929/verification.json` | local user path -> %USERPROFILE% | `b63013de237d64c1…` | `811ffb1cf1135563…` |
| `pilots/v04/reflectai_v04/config.py` | transport code/tests changed after the run: endpoint read locally and verified by SHA-256; endpoint address -> placeholder | `a2b63261bd81c171…` | `db45bfbc01e7a73b…` |
| `pilots/v04/reflectai_v04/fhgenie_transport.py` | transport code/tests changed after the run: endpoint read locally and verified by SHA-256; endpoint address -> placeholder | `38f275261ee4d487…` | `593c5102a87ff810…` |
| `pilots/v04/transport/fhgenie-request.ps1` | transport code/tests changed after the run: endpoint read locally and verified by SHA-256 | `bb79246517ba609b…` | `36e06b3ed2460d69…` |
| `pilots/v04/transport/runtime-attestation.json` | local user path -> %USERPROFILE% | `510412e3102687ef…` | `f5d0f9ccaebcf9eb…` |
| `pilots/v04/transport/test_fhgenie_request.ps1` | transport code/tests changed after the run: endpoint read locally and verified by SHA-256 | `0d4a3532c8aee918…` | `7245addc6f5e64f2…` |
| `tests/test_pilot_v04_fhgenie_transport.py` | transport code/tests changed after the run: endpoint read locally and verified by SHA-256 | `ca884a98e024641b…` | `b3150a2cab7a659c…` |

## Excluded from the repository

| Pattern | Files | Reason |
| --- | ---: | --- |
| `pilots/v04/review/*/sources/**` | 301 | sealed source snapshots with unsanitized copies; sanitizing them would break their seals |
| `pilots/v04/diagnostics/fhgenie/contract-test-*/run/calls/*/final.txt` | 32 | raw model responses |
| `pilots/v04/diagnostics/fhgenie/contract-test-*/run/calls/*/final.json` | 32 | raw model responses |
| `pilots/v04/diagnostics/fhgenie/probe-*/final-content.json` | 2 | raw model responses (toy probes) |
| `pilots/v04/diagnostics/transport-smoke-20260929/attempt/transport/*` | 5 | Codex CLI logs and metadata with local paths |
| `pilots/v04/diagnostics/transport-smoke-v2-20260929/attempt/transport/*` | 5 | Codex CLI logs and metadata with local paths |
| `pilots/v04/preflight/fhgenie-20260929/offline-tests-*-failed.txt` | 2 | failed sandbox test logs with local paths |
| `pilots/*/runs/` (existing rule) | all | full run folders; only each v0.4 run's `REPORT.md` and `manifest.json` and the incident report are committed |

Every excluded file and its SHA-256 is listed in the JSON record. Review-export manifests list their `sources/` files, which are available only in the archive. The frozen v0.3 calibration reports (`pilots/v03/CALIBRATION_REPORT.md`, `pilots/v03/CALIBRATION_R2_REPORT.md`) link to their run folders, which resolve only in the archive. These reports are left unchanged.

## Unchanged

Credentials were never in the repository: the FHGenie key is DPAPI-encrypted in the user profile outside it. `.gitignore` additionally excludes key-like files. `.gitattributes` keeps pilot material byte-exact so that unchanged files verify against their recorded hashes from a clone.
