# Fictional HR work-evidence example

**All work records, hypotheses and update patches in this offline example are authored synthetic fixtures.** Northstar Research and Atlas are fictional; `.example` addresses are placeholders. The labels `agent_output`, `human_feedback` and `human_revision` describe record types, without implying actual model runs or participant observations. Timestamps represent the fictional sequence of events. All four episodes belong to the development split.

The example tests evidence and adaptation contracts. For actual machine-generated hypotheses and outputs, see the separate [HR model pilot](../pilots/hr_v01/REPORT_en.md).

## The professional task

The recruiting lead needs a LinkedIn post for review: accurate role and employment details, a contribution explained for the intended audience, and the approved application route. Current facts and general brand guidance are supplied in the task materials.

| Episode | Audience and work | Evidence offered |
| --- | --- | --- |
| `hr-specialist-01` | Experienced computational biologist | Approved facts, team interview, generic draft, review requesting a concrete work-problem opening, and revision. |
| `hr-specialist-02` | Experienced research data engineer | A different role and location, engineering note, draft, similar review and revision. Employment facts differ from the first episode. |
| `hr-apprentice-03` | Research data apprentice | Programme facts, overly specialist draft, explicit objection and revised learning-and-support opening. |
| `hr-ambiguous-04` | Experienced research software engineer | Role facts, draft and unexplained shorter revision that drops employment information. Rationale and approval are missing. |

## Evidence and hypotheses

Each episode preserves its task, context, evidence records and provenance. References identify an episode, record and exact source quote. Missing feedback, approval and outcomes remain explicitly missing.

`h-specific` interprets two specialist reviews as a preference for opening with concrete work and contribution. The apprenticeship review challenges universal application of that preference while remaining compatible with the narrower specialist claim. Alternatives include a single reviewer's preference and a pattern specific to Atlas; these remain untested.

`h-ambiguous` records a possible preference for brevity. The shorter text is observable, but its rationale, approval and permission to remove employment details are unknown.

## Update candidates

| Candidate | Behaviour |
| --- | --- |
| `scoped-update` | Passes reference and scope checks. Its presentation strategy is eligible for validation; vacancy facts must still come from current approved sources. |
| `overbroad-update` | Retains only the HR restriction, removing audience, channel and project constraints. The scope guard rejects it. |
| `ambiguous-update` | Proposes omitting location and working arrangements. Its authored blocking question requires clarification before validation. |

Hypothesis-level `unresolved_questions` preserve broader uncertainty without automatically blocking an update. Transfer to another role can be evaluated; an unexplained deletion of important facts can instead block the proposed policy. The ambiguous candidate therefore carries a `blocking_questions` entry about the rationale and approval for removing employment details. This distinction is authored into the fixture. Expected effects remain untested predictions.

## Scope and use

Scopes specify HR, audience, channel and project. Both hypotheses and bounded candidates are restricted to Atlas; applicability elsewhere remains unestablished. Use these development records to test loading, reference resolution, missingness and candidate checks.

The fixtures contain no independently sampled observations, practitioner judgments or measured performance effects. Resolving a quote establishes traceability; assessing its relevance and a candidate's benefit requires separate evaluation. These public examples are not a held-out benchmark.
