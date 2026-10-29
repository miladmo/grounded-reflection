# Reproducibility

The public checkout supports offline tests, inspection of the study code and checks of published summaries. It does **not** contain the complete raw model runs needed for independent reanalysis. The distinction is part of the reported limitations.

## Install and test offline

From the repository root, with Python 3.11 or later:

```console
python -m pip install .
python -B -m unittest discover -s tests -v
grounded-reflection demo --output demo-output
```

Tests and the demo need no API key and make no live model calls. Use a new demo output directory, since output commands refuse to overwrite existing files. The demo uses authored candidates. Passing the tests establishes implementation behaviour, not reproduction of stochastic model outputs or confirmation of research conclusions.

For focused pilot tests in PowerShell, with the dependencies installed but without installing the package:

```powershell
$env:PYTHONPATH = 'src;pilots/v03;pilots/v04'
python -B -m unittest discover -s tests -p 'test_pilot_v04*.py' -v
python -B -m unittest discover -s tests -p 'test_pilot_v05*.py' -v
```

The v0.5 calibration and main run used Python 3.12.14 with Pydantic 2.13.5. Its D technical checks used Python 3.11.9 with Pydantic 2.10.6. See the study records for the corresponding model configuration.

## Inspect the published results

| Evidence | v0.4 | v0.5 |
| --- | --- | --- |
| Design and interpretation | [Guide](../pilots/v04/GUIDE.md) | [Study](../pilots/v05/README.md) |
| Counts and usage | [Machine report](../pilots/v04/runs/live-fhgenie-high-20260930/REPORT.md) | [Machine report](../pilots/v05/runs/live-main-20261003/REPORT.md) |
| Detailed analysis | [Report, including post hoc fields](../pilots/v04/DIFFICULTY_MAP_REPORT.md) | [Report](../pilots/v05/DIFFICULTY_MAP_REPORT.md) and [analysis JSON](../pilots/v05/analysis/main-analysis.json) |
| Author's failure attribution | [Responses](../pilots/v04/review/attribution-live-fhgenie-high-20261001/responses.json) | [Cases](../pilots/v05/review/attribution-20261004/CASES.md) |
| File identity | [Run manifest](../pilots/v04/runs/live-fhgenie-high-20260930/manifest.json) | [Run manifest](../pilots/v05/runs/live-main-20261003/manifest.json), [source binding](../pilots/v05/FROZEN-SOURCES.json) and [prompt hashes](../pilots/v05/prompts/FROZEN.json) |

These summaries retain failed outputs and fixed denominators. Later interpretations do not replace the recorded scores. The [provenance index](provenance.md) provides the original protocols, incidents and publication records.

## Verification boundary

A manifest records file hashes. A matching hash establishes file identity, not scientific validity. Public reports and manifests can be inspected, and available files can be compared with their recorded hashes. Missing raw responses, preparation files and evaluator files prevent verification of a complete run seal from the public checkout.

For v0.4, publication sanitization changed 71 committed files after recording. The [publication record](../pilots/v04/PUBLICATION_SANITIZATION.md) explains which historical bindings require originals. It records the archive name and hash. For v0.5, the [publication record](../pilots/v05/PUBLICATION_SANITIZATION.md) documents the raw-data exclusions and a later Windows-only test skip that changes the frozen source binding. The original test remains at tag `pilot-v05-results-20261004` and in the original archive. Neither archive has a permanent public access location specified here.

With the **complete v0.4 original archive** present, this PowerShell command checks the run, preparation and evaluator file sets without changing scores or calling a model:

```powershell
$env:PYTHONPATH = 'src;pilots/v03;pilots/v04'
python -B -c "from pathlib import Path; from reflectai_v04.storage import verify_seal; r=Path('pilots/v04/runs/live-fhgenie-high-20260930'); print({str(p): verify_seal(p, p/'manifest.json')['sha256'] for p in (r, r/'preparation', r/'evaluator')})"
```

The recorded run seal is `7afab956742071b0c5ddd8d696e854630a2a6f25945a32d34e6ece3dddbb8594`. The [oracle](../pilots/v04/reflectai_v04/oracle.py) and [evaluation code](../pilots/v04/reflectai_v04/evaluation.py) expose the scoring route, but v0.4 has no dedicated read-only evaluation replay command. Running its study runner would create a new run rather than verify the recorded one.

For v0.5, [main_analysis.py](../pilots/v05/analysis/main_analysis.py) verifies the full seal and recomputes analysis from the original data. It **overwrites** `analysis/main-analysis.json`. Do not run it merely to inspect results in the preserved checkout. Reanalysis requires a separate working copy of the complete original archive. The [seal verifier](../pilots/v05/reflectai_v05/storage.py) likewise requires the complete file set.

No new model run, rescoring or change to archived evidence is part of the public documentation revision. A new experiment would require fresh material, a specified protocol and separately configured model access.
