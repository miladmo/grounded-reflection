# From infrastructure to a research method

The current code includes an initial experiment on synthetic work. It does not supply the empirical answer for professional use with employees.

## 1. Infer requirements from work evidence

Implement and compare inference backends that turn heterogeneous episodes into grounded requirement hypotheses. Evaluate whether they correctly link observations, distinguish corrections from preferences, identify counterexamples, represent missing information and limit applicability. Include ambiguous and contradictory evidence and current explicit task instructions. Use controlled cases with known provenance alongside independently assessed professional work.

A first Codex CLI backend now records configuration, prompts, usage and outputs, and a prompted reflection pilot uses it to infer hypotheses from historical episodes. Extend this into the general `ReflectionBackend` interface and compare inference methods under explicitly matched information and compute budgets. Exact reference resolution remains an infrastructure check; human assessment and task experiments address the validity of the interpretation.

## 2. Test whether interpretation helps adaptation

Connect the typed candidate to an existing agent runner and context optimizer. Compare a frozen baseline, direct retrieval of work evidence, direct adaptation and evidence-grounded reflection. Match the model, task materials and adaptation resources. Test whether the intermediate hypothesis improves new work beyond simply giving the agent more relevant context.

Use professional deliverables with independently specified quality rubrics and critical-error checks. Start with one workflow and expand only when task realism and reliable assessment have been established. HR recruiting, sales proposals and scientific decision memos are candidate task families; the current HR fixture is not evidence of readiness in all three domains.

## 3. Evaluate repeated improvement and its limits

Run bounded adaptation cycles using development and validation data while reserving final tasks and outcomes. Measure professional quality, critical errors, human revision effort, adaptation cost, out-of-scope regressions and stability across cycles. Predefine the resource budget and stopping rule to limit validation overfitting. Compare context adaptation with a bounded model-adaptation condition where feasible.

An especially relevant question is what happens as agents require less interaction: do remaining corrections and approvals provide enough information, and when does the system need a targeted request for expert input? Silence or lack of revision must not be automatically equated with success.

## Readiness record

| Component | Current status | Research still needed |
| --- | --- | --- |
| Evidence and hypothesis contracts | Implemented | Coverage of heterogeneous work and validity of representations |
| Reference and declared scope checks | Implemented | Semantic grounding, learned scope and calibrated uncertainty |
| HR example and pilot | Authored development fixture; six separately authored tasks with actual model outputs | Practitioner calibration, less explicit requirements and repetitions |
| Candidate selector and decision records | Implemented for supplied ratings | Calibrated evaluation and equal-budget comparisons |
| Automated reflection backend | Optional CLI backend and prompted pilot | General backend integration, comparative reliability and efficiency |
| Agent runner and adaptation loop | Single-cycle text-generation pilot | Tool-executing agents, optimizer integration and repeated cycles |
| Public benchmark and dataset | Planned | Task design, sampling, permission, splits and validation |
