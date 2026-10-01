# Synthetic pilot v0.2

This pilot asks whether grounded reflection recovers omitted contextual requirements and improves later outputs beyond direct adaptation of the same evidence. It compares four conditions across recruiting briefs, sales handovers and research notes.

| Condition | Historical evidence and preparation |
| --- | --- |
| A, no adaptation | Current task and initial instructions only |
| B, direct evidence | Full history supplied with each current task |
| C, direct adaptation | Two calls to develop and review reusable guidance |
| D, grounded reflection | Two calls to propose requirements, examine counterevidence and revise guidance |

C and D use the same histories, output representation and context rendering. D versus C is the primary comparison. See the [prespecified protocol](../../docs/pilot-v02-protocol.md), [data card](DATA_CARD.md) and [reporting template](RESULTS_TEMPLATE.md).

## First live findings

The completed September 2026 run found no advantage of grounded reflection over direct adaptation (19/24 versus 23/24 task attempts). Read the [findings and measurement audit](REPORT_en.md), [calibration report](CALIBRATION_REPORT.md) and [run notes](LIVE_RUN_NOTES.md) before interpreting raw metric differences. The first live evaluation exposed field-name and scope-encoding weaknesses; separate post hoc diagnostics preserve the original scores. No human evaluation has been performed.

## Run offline

Run these commands from the checkout root with Python 3.11+ and the existing project dependencies installed. The script imports the source checkout directly. No package installation, API key, model download, Codex CLI or login is needed for this run.

```bash
python pilots/v02/run_pilot.py calibrate --config pilots/v02/config.mock.json --run-dir pilots/v02/runs/mock-calibration
python pilots/v02/run_pilot.py prepare --config pilots/v02/config.mock.json --run-dir pilots/v02/runs/mock-main
python pilots/v02/run_pilot.py validate --run-dir pilots/v02/runs/mock-main
python pilots/v02/run_pilot.py freeze --run-dir pilots/v02/runs/mock-main
python pilots/v02/run_pilot.py final --run-dir pilots/v02/runs/mock-main
python pilots/v02/run_pilot.py report --run-dir pilots/v02/runs/mock-main
```

Calibration has its own run directory. Choose fresh directory names to repeat the sequence. Stages refuse to overwrite prior artifacts.

**The mock checks infrastructure only. It performs no requirement inference and cannot establish calibration or any research finding.** It copies public task facts into output fields, behaving identically across conditions. Mock outputs and reports are labelled `offline_mock`; token usage is unknown.

With two repetitions, preparation makes 24 backend calls, validation 48 and final generation 96, totalling 168 in the main run. Calibration makes 12 additional calls in its separate run. Offline calls do not contact a model. There are no judge calls, runner-level retries or output repairs. The underlying Codex CLI may reconnect internally, as documented in the live run notes.

## Inspect the records

- `calls/` preserves each request, schema, response when available, status, usage and timing. Failed calls remain in the ledger and evaluation denominators.
- `prepared/` records raw and retained requirements for both adaptive conditions.
- `freeze.json` binds source, prompts, configuration, development inputs and prepared artifacts. Concrete final tasks and their separate evaluator truth are generated only after freeze, under `heldout/`.
- `REPORT.md` and `results.json` report paired outcomes, requirement inference, scope, distractors, abstention and resource use. `human-review.json` is an unreviewed blinded sample; its mapping is separate.

Changed frozen inputs block final execution. Final results must not guide further tuning of this study. Further development requires a new labelled version with fresh held-out instances, preserving the original results. These are reproducibility controls, not a security boundary against someone deliberately opening evaluator files.

## Live model access

Agree the provider, explicit model, settings and budget before any live call. The current choices are the offline mock and the optional Codex CLI transport. Live use requires an installed, authenticated Codex CLI, an explicit model configuration and `--allow-live` on every inference stage. No credentials belong in repository files. Offline tests do not depend on CLI authentication.

A live final run also requires an eligible calibration run supplied to `freeze` through `--calibration-run`. The protocol permits at most two documented calibration rounds and specifies a 30–70% baseline compliance target. Inspect hidden and explicit requirements separately; mock scores cannot satisfy this requirement.

Call limits include failed attempts. The reported-token threshold is checked between calls. Codex cannot enforce a hard per-call token ceiling, so the threshold may be exceeded by a call already in progress. These runs are call-budget-controlled and token-audited, not strictly compute-matched. Cached input and reasoning output are recorded as subsets, without double counting. Missing usage and monetary costs remain unknown.

## Limits

This is a small, authored, structured synthetic rule problem. Deterministic compliance is not a measure of full professional quality. There is no real tool execution or completed human evaluation. Two repetitions do not constitute independent organisations, and within-family transfer does not establish enterprise generalisation. One preparation cycle per repetition does not demonstrate recursive improvement. The [v0.1 pilot](../hr_v01/REPORT_en.md) and its frozen results remain unchanged.
