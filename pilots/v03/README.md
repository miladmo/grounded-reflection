# Pilot v0.3

Eight synthetic histories test when work evidence warrants a contextual change.
The pilot separates candidate status, applied update decisions and actual-world task
compliance. Evaluated agents do not ask employees questions. Unresolved candidates stay
in the preparation record and never become operational prerequisites.

Implementation is isolated here so the v0.1 and v0.2 source manifests remain unchanged.
The existing `grounded_reflection` package supplies the strict Pydantic base, scope
contract and optional Codex transport. No API key is stored here.

## Current result

Both allowed live calibration rounds completed on 29 September 2026, with 128 calls
and no failed calls. After the prospective round-2 repairs, direct evidence use and
strong direct adaptation each made all eight warranted diagnostic decisions correctly.
Both achieved 7/8 world-correct diagnostic outputs, with the remaining case deliberately
unidentifiable from the available evidence, and passed all eight controls.

Direct adaptation reached the primary-score ceiling, so the prespecified headroom gate
failed. The planned main comparison is stopped. Grounded reflection (D) was not run.
These synthetic results support pipeline feasibility, not a reflection advantage or
enterprise effectiveness. See the [second calibration report](CALIBRATION_R2_REPORT.md)
and the preserved [first calibration report](CALIBRATION_REPORT.md).

## Offline check

From the repository root, using an environment with the project dependencies installed:

```powershell
python -B pilots/v03/run_pilot.py offline --out pilots/v03/runs/offline-check
$env:PYTHONPATH = 'src;pilots/v03'
python -B -m unittest discover -s tests -p 'test_pilot_v03_*.py'
```

The offline backend copies the configured baseline and infers nothing. It exercises
288 logical completions for three repetitions, including two preparation passes per
history and adaptation arm. These are local function calls, not provider calls.
Mock scores are engineering checks, never calibration or research findings.

`export-development --out PATH` writes public history/task examples and separate private
evaluator objects. `review-template --out PATH` creates a pending human rubric review.
The template must not be filled automatically as though a person reviewed it.

The [pre-calibration design review](../../docs/pilot-v03-design-review.md) explains the
matched Sales comparisons, unresolved routing alternatives and supplied scope assumptions.
C directly constructs and reviews guidance. D first produces an uncommitted hypothesis
draft, then audits it before adoption. Final C2/D2 preparations share one contract and
evaluator. D1 status labels are procedural and are not scored as final uncertainty judgments.

## Live stages

Milad Morad confirmed the four conceptual inference rules on 29 September 2026.
Independent review of generated records and human output assessment remain pending.
Live execution additionally needs
an explicit `--allow-live`. Calibration uses A/B/C, one repetition and at most two
registered rounds. Each round plans 64 calls. A failed attempt consumes its round.

Use `calibrate --config FILE --review FILE --round 1 --out PATH --allow-live` only after
review. A configuration uses `phase: calibration`, `repetitions: 1`, and backend values
`backend: codex`, `model: gpt-6-sol`, `reasoning_effort: medium`, `max_calls: 64` and an
explicit `max_reported_tokens`. Reviewers should fix the token budget before execution.
The transport audits reported tokens between calls but cannot cap tokens within a call.

After successful calibration, `freeze --config FILE --review FILE --calibration RUN_DIR
--out F0_FILE` seals sources, settings, review and calibration decisions. The main
configuration uses `phase: main`, three repetitions, a fresh seed and 288 calls.
`main --freeze F0_FILE --out PATH --allow-live` performs preparation without future tasks,
seals F1, then instantiates final tasks. Never reuse final outputs for tuning.

The generator and evaluator live in the same research repository but have different
data paths. Only explicit public payload builders pass data to a model. The optional
transport runs without tools in an empty model workspace. This is a programmatic
separation boundary, not protection against a researcher deliberately reading truth files.

See the [protocol](../../docs/pilot-v03-protocol.md), [scenario cards](SCENARIOS.md),
and [report template](REPORT_TEMPLATE.md). A small blinded review sample is exported
with a separate evaluator key. No LLM judge or holistic rating determines primary scores.
Field compliance in these small synthetic cases is not yet a measure of professional
quality. Results include call and reported-token accounting by arm and phase.
