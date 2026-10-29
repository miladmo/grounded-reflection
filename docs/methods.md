# Methods

This page explains the existing designs of pilots v0.4 and v0.5. It is a public reading guide, not a new protocol or preregistration. Here, *registered* means specified internally before the relevant evaluation. Original protocols, amendments and subsequent qualifications remain in the [provenance index](provenance.md).

## Evidence and warrant

The research question is whether work evidence supports a previously unspecified requirement, and where that requirement applies. The pilots reduce this to synthetic field operations in fictional workflows. They supply the evidence conventions, context attributes and permitted rule forms. They do not yet test discovery of unrestricted tacit requirements in real organisations.

A history includes useful reviews and misleading records. A **binding approval** is an accepted review from an authorised person, within the registration's validity interval, that covers the target field. A preference, rejected revision or review of another field does not establish the requirement. These are experimental evidence semantics, distinct from permissions to execute research code.

The deterministic warrant oracle filters the public records and retains every permitted rule consistent with them. A change is warranted only when all compatible rules require it at the task context. If they disagree, the agent must retain the initial configuration. This does not prove that the baseline is true. The generator's hidden *world function* is used separately to measure world compliance, not to tell the oracle what to infer.

H14 contains all Boolean rules over two binary attributes except XOR and its complement, XNOR. Excluding these two patterns is a supplied assumption that makes some unseen combinations identifiable. H134 extends those restricted forms to six binary attributes, using at most two per rule. It contains two constants, twelve tests of individual attribute values, and 120 conjunctions or disjunctions. A value test can concern either value of an attribute. The [worked example](../pilots/v05/README.md#a-worked-example) shows why these assumptions matter.

## Pilot v0.4

Twenty-four histories cross six evidence settings with four diagnostic types. Settings vary raw versus interpreted records, volume and noise, dependence, and a documented version break. Every setting contains two warranted changes, one resolved retention and one unidentifiable change. Task families rotate imperfectly. Each history yields one diagnostic and one control, giving 24 of each per arm.

| Arm | Procedure |
| --- | --- |
| A | Current task, initial configuration and public contract, without history. |
| B | The complete history is supplied for each task. |
| C | C1 constructs reusable guidance, C2 reviews it, and future tasks receive applicable guidance. |

C's prompts already request counterevidence, alternatives and scope. There is no additional reflection arm D. Sharing evidence does not give B and C equal computational cost. The purpose is to locate inference difficulty for a subsequent study. See the [design and setting tables](../pilots/v04/GUIDE.md#3-design-at-a-glance).

Material checks distinguish action changes from contradictions. Counting a nonbinding record as valid must be capable of changing the expected action in ambiguous histories, or creating a contradiction in already decided histories. Additional evidence cannot reverse an already unanimous rule set without making it inconsistent. Surface audits test whether simple timestamps, comments or positions separate binding reviews. They cannot exclude every possible shortcut.

## Pilot v0.5

Sixteen histories cross two history sizes with known or unknown relevant attributes. Small histories contain 24 records and large histories 240, but both contain twelve binding approvals. In known settings the relevant pair is disclosed and the class is H14. In unknown settings the pair is hidden among six visible attributes and the class is H134.

| Arm | Procedure |
| --- | --- |
| A | Generate without history. |
| B | Retrieve records deterministically for each task, prioritising registration and accepted reviews of the target field, then context and recency. Selection does not validate authority or time validity. |
| C | Process consecutive chunks into running guidance, then consolidate it before future tasks. |
| D | Propose a hypothesis register, query records for up to six rounds, and derive guidance from the resulting register. |

Each history yields an observed change, an observed retention, a hard diagnostic and an out-of-workflow control. The hard diagnostics comprise two transferred changes and two unidentifiable cases per setting. Overall there are 48 diagnostics and sixteen controls per arm. These are stress cases where simple similarity can mislead.

All arms use the same model and per-call limits. C and D share a preparation cap, with generation budget reserved separately. Actual token use differs. The D schema and runner allow an updated hypothesis list, but the prompt does not explicitly instruct the model to add missing rules or rebuild an exhausted register. The incomplete enumeration observed after the run therefore has mixed model and specification explanations. See the [procedure and limitations](../pilots/v05/README.md).

## Measurement

| Measure | v0.4 | v0.5 |
| --- | --- | --- |
| Primary | Warranted diagnostic action, including declared-rule scope. A's history-warrant score is not comparable. | Executed fields against the oracle, identically for all arms. Failed or blocked outputs remain incorrect. |
| Scope and controls | Scope enters the primary metric. Controls are separate. | Declared scope is secondary. Controls are separate. |
| Additional analyses | Hidden-world compliance, candidate errors, transfer-error direction, tokens and a labelled post hoc fields-only comparison. | Evidence coverage, register behaviour, error attribution and tokens. |

The **v0.4 headroom criterion** requires C to pass at most 70 percent of diagnostics and at least 60 percent of all its failures to have confirmed content causes. Mixed and unresolved failures stay in the denominator but not the numerator. Candidate-level errors are secondary and do not enter the gate. Four diagnostics per setting make this exploratory. [Results](../pilots/v04/GUIDE.md#5-results) report the primary and post hoc comparisons separately.

The **v0.5 calibration gate** checks whether the better whole direct arm, B or C, solves every hard calibration task in every setting. It does not choose the correct arm separately for each task. Calibration has two hard cases per setting. The main run then tests descriptive expectations about history size, unknown attributes, D's accuracy and its conditional token cost. The [decision rules](../pilots/v05/README.md#measurement-and-decision-rules) and [results](../pilots/v05/README.md#results) preserve the original denominators and later reading corrections.

Neither pilot supplies a significance test or an estimate of enterprise return. Conditional token amortisation assumes reuse of unchanged guidance. It does not measure saved employee time or financial value.

## Separation and review

Preparation is frozen before future task instances are generated. The author knows the synthetic construction templates, so these are not unseen confirmatory benchmarks. v0.5 also discloses a one-time, in-memory revision-r2 constructibility check using final-history seed 45061. Its contents were not inspected or saved, future-task and call-order seeds were not used, and no generator change followed that check.

Material reviews included AI-assisted checks. Decisive failure attribution was reviewed by the author, not an independent evaluator. These checks are distinct from independent human evaluation or field validation. Technical tests and incomplete runs are excluded from performance results, except isolated failures within the completed main run, which remain in its fixed denominators.

The [reproducibility guide](reproducibility.md) distinguishes public checks from reanalysis requiring the original archives. The [glossary](glossary.md) provides definitions; [provenance](provenance.md) retains the detailed historical record.
