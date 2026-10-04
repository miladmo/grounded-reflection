# Publication sanitization record, pilot v0.5

Prepared on 4 October 2026 before the first publication of branch `pilot-v05`. It applies
the decisions recorded for v0.2–v0.4 in `pilots/v04/PUBLICATION_SANITIZATION.md`.

**Unlike v0.4, no committed v0.5 file was changed after it was recorded.** v0.5 followed
the rules from the start:

* the endpoint is read from outside the repository;
* PowerShell paths use `%USERPROFILE%`;
* raw run folders are excluded from Git.

Every committed file therefore matches the version bound by its seal, approval or
manifest.

## Decisions applied

* **The industry partner is not named.**
* **Local user paths do not occur.** Run configurations name the pinned PowerShell 7 as
  `%USERPROFILE%/...`; the runner expands it at run time.
* **Raw model responses, transport metadata and full run folders are not published.** Of
  each run, only `REPORT.md`, `manifest.json` and, where relevant, `INCOMPLETE.json` and an
  incident report are committed. The manifests list the SHA-256 of every file in the full
  sealed folders.
* **The FHGenie endpoint address is not published.** The name FHGenie, the model and
  aggregated results are public. The transport reads the address from
  `REFLECTAI_FHGENIE_ENDPOINT` or `%LOCALAPPDATA%\reflectAI\fhgenie-endpoint.txt` and
  checks its pinned SHA-256 before any request.
* **No keys or tokens.** The FHGenie key is stored DPAPI-encrypted outside the repository
  and never enters run files.

## Checks performed

| Check | Scope | Result |
| --- | --- | --- |
| Endpoint address and host name | every blob and commit message in the push range `origin/pilot-v04..pilot-v05`, in the published `origin/pilot-v04`, `origin/main` and tag `pilot-v04-results-20261001`, and in all local tags | no hits |
| Endpoint host name | every file of the local `pilots/v05` tree, including the ignored full run folders (5,813 files) | no hits |
| Windows user path, partner name | v0.5 tree and all diffs of the push range | no hits |
| Keys and tokens | pattern search over the tree | only the known v0.4 test placeholders |
| Author identity | all commits of the push range | `Milad Morad <47043126+miladmo@users.noreply.github.com>` as author and committer |

**Identity rewrite.** Ten local commits originally carried an institutional address. Only
their author and committer were rewritten before the first push; every tree is
unchanged. See [COMMIT_MAP.md](COMMIT_MAP.md).

## Archive of originals

`grounded-reflection-v05-originals-20261004.zip`, SHA-256
`252cb74df08a90203d1fc9141ef6f0911f1e4ea107394bc14861a8a00061d06d`. It contains the
complete `pilots/v05` folder at report finalisation, including all ignored full run
folders with raw responses and transport metadata, and `docs/pilot-v05-protocol.md`. It is
stored outside this repository; its permanent location is chosen by Milad Morad.

Two further backups are kept outside the repository, as git bundles:

* `pilot-v05-before-identity-rewrite-20261004.bundle`: the branch before the identity
  rewrite;
* `pilot-v05-results-20261004.bundle`: the tags `pilot-v05-frozen-20261003` and
  `pilot-v05-results-20261004`; the latter points to the README correction commit
  `0386d21`. SHA-256 `5f423e990e31ec65b1378bde50f0c32ad5096f3f8c297e70418666d9103a6602`.
  This record was committed after the tagged commit, so the bundle does not contain it.

## Change after publication: Windows-only test skipped elsewhere

On 4 October 2026, after the first push, CI on Linux failed in one test,
`test_pinned_powershell_path_may_use_environment_variables`. The test relies on `%VAR%`
expansion, which `os.path.expandvars` performs only on Windows. All live runs were made on
Windows. Milad Morad decided to skip the test on other systems; the study code is
unchanged.

**Consequence.** `tests/test_pilot_v05_runner.py` is part of the v0.5 source binding, so
the committed sources no longer reproduce the frozen binding in `FROZEN-SOURCES.json`
(`9487e28b…`). The original test file is at tag `pilot-v05-results-20261004` and in the
archive of originals.

| File | Original SHA-256 | Committed SHA-256 |
| --- | --- | --- |
| `tests/test_pilot_v05_runner.py` | `4751137d0b02e9fb78edf48a22efed985cf643231a15b79da1199562152c49be` | `2c074b66be138dc75b1e5e53482d40338a7bb98e4672ec088147f209ffc11879` |
