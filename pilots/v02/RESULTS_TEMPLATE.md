# Pilot v0.2 results

Status: not run with a live model. Do not replace this statement with mock scores.

## Run record

Record protocol and code hashes, data version, model/backend, settings, dates,
repetitions, final-case count and freeze manifest. Specify whether usage limits
were provider enforced or audited after calls. Link complete failure logs.

## Calibration

Report each calibration round, rationale for changes and no-adaptation results.
Show hidden, explicit and generic checks separately, with family-level counts.
Did baseline compliance fall in the prespecified 30–70% band? Were all changes
completed before freeze? A mock run does not answer either research question.

## Primary comparison

Compare grounded reflection against direct adaptation on all prespecified cases.
Report raw and retained requirement precision/recall, scope recovery, excessive
restriction, harmful generalisation and distractor adoption. Use explicit
denominators; no predictions means undefined precision, not perfect precision.

## Downstream behaviour

For all four conditions, show per-case/per-repetition requirement checks, task
success, required and unnecessary abstention, invalid outputs and boundary-case
regressions. Distinguish appropriate deferral from successful delivery. Include
the full paired D–C table even if it shows no benefit or worse performance.

## Resource use

Separate preparation, validation and final generation. Report attempts, failures,
input/output tokens and available cache/reasoning subsets without double counting.
Amortise preparation across the actual number of future tasks. Record unknown
usage, cost and human effort as unavailable. Never infer money from subscription
usage or human time from a model judgement.

## Human spot checks

State how the blinded sample was selected, who reviewed it and which disagreements
were found. Until reviews exist, write "No human evaluation has been performed."
Any later judge must come from a different model family and use blinded pairwise
comparisons; document its separate protocol and budget before running it.

## What this pilot can and cannot show

This is a small, synthetic, author-designed test of scoped rule recovery and
decision compliance. The predicate vocabulary limits what is measurable. A
calibrated baseline does not establish realism or measurement validity. Results
within these task families do not establish enterprise readiness, employee
benefit, high-scale operation, causal effects in organisations or recursive
self improvement. State null results, failure modes and residual ceiling/floor
effects plainly. Final outcomes must not be reused for tuning this run.
