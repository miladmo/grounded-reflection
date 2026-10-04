# S3 / hr

Material revision: v04-amendment-03-r2. Synthetic development example.

[Frozen surface-selector audit](surface-audit.md) · [Complete audit JSON](surface-audit.json).
Its per-history results use this case’s history ID; selector choice used only separate development histories.

Registered task type: **unidentifiable**. Intended diagnostic regime: **unidentifiable**.
Public records: 6. Control basis: unidentifiable_baseline_world.

## Review summary

Current compatible functions: **4**. Full cross-version policies: 4.

H14 identification is conditional on excluding XOR and XNOR. Retaining an unresolved
baseline does not establish that the baseline is the true requirement.

| Task | Public context | Previously observed | Warranted action | Retention basis |
| --- | --- | --- | --- | --- |
| diagnostic | task_family=personnel_document, workflow=workflow-7e0284a9f5cd, version=edition-00e5eb7c0872, recipient=internal, contract=permanent | False | keep | unresolved |
| control | task_family=personnel_document, workflow=workflow-7e0284a9f5cd, version=edition-00e5eb7c0872, recipient=external, contract=temporary | False | keep | unresolved |

Counterfactual qualification requires **action_flip** for every present type. All present types qualify: **True**.

One qualifying example per present type is shown below. The links lead to its
public evidence; all records and counts appear in the later audit and JSON sidecar.

| Type (record count) | Promoted record / source | Public target value | Exact promotion | Outcome / remaining policies |
| --- | --- | --- | --- | --- |
| forward (2) | [record-5e5bc7a546c1](#record-5e5bc7a546c1) / [record-ed88d1449d9f](#record-ed88d1449d9f) | booking_reference = 'BK-55604' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=personnel_document, workflow=workflow-7e0284a9f5cd, version=edition-00e5eb7c0872, recipient=external, contract=temporary | action_flip / 2 |

An action flip requires a nonempty compatible set and a changed diagnostic or control
action. A contradiction has no compatible policy and supplies neither task action.

[Complete oracle derivation](#oracle-derivation-from-public-evidence) · [Every counterfactual record](#single-record-counterfactual-relevance)

## Public configuration and assumptions

```json
{
  "as_of": "2026-06-15T12:00:00Z",
  "baseline_template": {
    "message": "{message}",
    "work_email": "{work_email}"
  },
  "dimensions": {
    "contract": [
      "permanent",
      "temporary"
    ],
    "recipient": [
      "internal",
      "external"
    ]
  },
  "fact_descriptions": {
    "booking_reference": "Current booking reference.",
    "message": "Current personnel document text.",
    "work_email": "Current contact email."
  },
  "field_option": {
    "field": "booking_reference",
    "operation": "set_fact",
    "separator": "",
    "value": "booking_reference"
  },
  "hypothesis_class": "h14",
  "hypothesis_definition": "Each of the two declared binary context dimensions defines a predicate testing its second listed value. Call these predicates x and y. In each registered version the target field configuration is one Boolean function from the following class: constant 0 or 1; x, not x, y, or not y; a conjunction of one literal from each dimension; or a disjunction of one literal from each dimension. Zero selects the configured baseline and one the available alternative. The fourteen distinct truth tables exclude only XOR and XNOR. Each version has its own class member, with no cross-version coupling. This restriction is a supplied synthetic assumption, not an established property of enterprise work.",
  "task_family": "personnel_document",
  "workflow": "workflow-7e0284a9f5cd"
}
```

This is a bounded synthetic workflow model. initial_configuration declares the field options, two context dimensions and the complete H14 hypothesis class. Each registered version has one class member. A field observation constrains the member indexed by its recorded version. Broader consequences follow from the declared class. Facts provide current artifact values. Other fields retain their configured baseline. Outside the declared task_family and workflow, or without a complete declared context, no update is authorised by this model. A register_version event supplies trusted workflow metadata with the authority roster and half-open validity interval. Binding field approval is an event of type review with decision accept, performed by a listed reviewer within that interval, with the field included in reviewed_fields. Its accepted artifact establishes the field configuration at the recorded context. This explicit approval convention is a supplied synthetic assumption. A forward has an origin_ref identifying the record whose content it reproduces. Raw artifacts expose named revisions and a selected artifact reference; interpreted records expose the selected fields directly. A rejection records a whole-artifact decision and its stated grounds. An artifact field whose review is not recorded has no approved assignment. The configured baseline is retained when the available evidence does not establish an update. Dates and version labels in new work identify the applicable registration.

## Public work records

### record-ed88d1449d9f

2026-05-19T16:37:12Z | review | Jonas

Context: task_family=personnel_document, workflow=workflow-7e0284a9f5cd, version=edition-00e5eb7c0872, recipient=external, contract=permanent

- decision: accept
- reviewed_fields: ['booking_reference']
- authority_ref: record-15ef3cc618a1
- comment: Checked.

```json
{
  "accepted_fields": {
    "booking_reference": "BK-55604",
    "message": "Please prepare the appointment documents for case 55604.",
    "work_email": "contact55604@example.test"
  },
  "authority_ref": "record-15ef3cc618a1",
  "change_summary": {
    "after": "BK-55604",
    "before": null,
    "field": "booking_reference"
  },
  "comment": "Checked.",
  "decision": "accept",
  "document_id": "DOC-55604",
  "event": "review",
  "facts": {
    "booking_reference": "BK-55604",
    "date": "2026-05-19",
    "document_id": "DOC-55604",
    "message": "Please prepare the appointment documents for case 55604.",
    "work_email": "contact55604@example.test"
  },
  "format": "interpreted",
  "reviewed_fields": [
    "booking_reference"
  ]
}
```

### record-1be8539b89c8

2026-06-13T15:17:39Z | review | Robin

Context: task_family=personnel_document, workflow=workflow-7e0284a9f5cd, version=edition-00e5eb7c0872, recipient=internal, contract=temporary

- decision: accept
- reviewed_fields: ['booking_reference']
- authority_ref: record-15ef3cc618a1
- comment: Approved.

```json
{
  "accepted_fields": {
    "message": "Please prepare the appointment documents for case 36881.",
    "work_email": "contact36881@example.test"
  },
  "authority_ref": "record-15ef3cc618a1",
  "change_summary": {
    "after": null,
    "before": "BK-36881",
    "field": "booking_reference"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-36881",
  "event": "review",
  "facts": {
    "booking_reference": "BK-36881",
    "date": "2026-06-13",
    "document_id": "DOC-36881",
    "message": "Please prepare the appointment documents for case 36881.",
    "work_email": "contact36881@example.test"
  },
  "format": "interpreted",
  "reviewed_fields": [
    "booking_reference"
  ]
}
```

### record-5e5bc7a546c1

2026-06-02T08:22:40Z | revision | forwarding-service

Context: task_family=personnel_document, workflow=workflow-7e0284a9f5cd, version=edition-00e5eb7c0872, recipient=external, contract=temporary

- origin_ref: record-ed88d1449d9f

```json
{
  "event": "forward",
  "message": "Sharing the linked artifact with the working group.",
  "origin_ref": "record-ed88d1449d9f"
}
```

### record-15ef3cc618a1

2026-01-01T00:00:00Z | template | workflow-registry

Context: 


```json
{
  "authorised_reviewers": [
    "Robin",
    "Jonas"
  ],
  "event": "register_version",
  "supersedes": null,
  "task_family": "personnel_document",
  "valid_from": "2026-01-01T00:00:00Z",
  "valid_until": "2027-01-01T00:00:00Z",
  "version": "edition-00e5eb7c0872",
  "workflow": "workflow-7e0284a9f5cd"
}
```

### record-b6d7c2702512

2026-06-02T12:44:09Z | review | Robin

Context: task_family=personnel_document, workflow=workflow-7e0284a9f5cd, version=edition-00e5eb7c0872, recipient=internal, contract=temporary

- decision: accept
- reviewed_fields: ['booking_reference']
- authority_ref: record-15ef3cc618a1
- comment: Recorded.

```json
{
  "accepted_fields": {
    "message": "Please prepare the appointment documents for case 35164.",
    "work_email": "contact35164@example.test"
  },
  "authority_ref": "record-15ef3cc618a1",
  "change_summary": {
    "after": null,
    "before": "BK-35164",
    "field": "booking_reference"
  },
  "comment": "Recorded.",
  "decision": "accept",
  "document_id": "DOC-35164",
  "event": "review",
  "facts": {
    "booking_reference": "BK-35164",
    "date": "2026-06-02",
    "document_id": "DOC-35164",
    "message": "Please prepare the appointment documents for case 35164.",
    "work_email": "contact35164@example.test"
  },
  "format": "interpreted",
  "reviewed_fields": [
    "booking_reference"
  ]
}
```

### record-8e79f0d57861

2026-06-13T09:09:01Z | revision | forwarding-service

Context: task_family=personnel_document, workflow=workflow-7e0284a9f5cd, version=edition-00e5eb7c0872, recipient=internal, contract=permanent

- origin_ref: record-ed88d1449d9f

```json
{
  "event": "forward",
  "message": "Sharing the linked artifact with the working group.",
  "origin_ref": "record-ed88d1449d9f"
}
```

## Oracle derivation from public evidence

Recomputed solely from the public History by the independent oracle.

H14 excludes XOR and XNOR; transfer identification depends on this supplied restriction.

Distinct current-version functions: **4**. Full policies across all registered versions: **4**.

An approval constrains one cell in its registered version. The following are the
actual applied constraints, including independent repeats. Copies do not add a constraint.

| Public record | Version | Context | Field option |
| --- | --- | --- | --- |
| record-ed88d1449d9f | edition-00e5eb7c0872 | task_family=personnel_document, workflow=workflow-7e0284a9f5cd, version=edition-00e5eb7c0872, recipient=external, contract=permanent | 1 |
| record-1be8539b89c8 | edition-00e5eb7c0872 | task_family=personnel_document, workflow=workflow-7e0284a9f5cd, version=edition-00e5eb7c0872, recipient=internal, contract=temporary | 0 |
| record-b6d7c2702512 | edition-00e5eb7c0872 | task_family=personnel_document, workflow=workflow-7e0284a9f5cd, version=edition-00e5eb7c0872, recipient=internal, contract=temporary | 0 |

### Competing requirement explanations

Zero is the configured baseline; one is the alternative. Each row is a distinct
compatible function for this version. No preference for simplicity removes a row.
The private sampling plan and world policy do not filter these explanations.

Version edition-00e5eb7c0872: 4 compatible functions.

| Function | recipient=internal, contract=permanent | recipient=internal, contract=temporary | recipient=external, contract=permanent | recipient=external, contract=temporary | Complexity |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | 0 | 1 | 0 | 2 |
| 2 | 0 | 0 | 1 | 1 | 1 |
| 3 | 1 | 0 | 1 | 0 | 1 |
| 4 | 1 | 0 | 1 | 1 | 2 |

### Diagnostic and control derivations

| Task | Context observed | Witnesses | Action | Retention basis |
| --- | --- | --- | --- | --- |
| diagnostic | False | none | keep | unresolved |
| control | False | none | keep | unresolved |

## Private material audit

These design labels, counterfactuals and world requirements are evaluator material.
They are never preparation or generation inputs. The true world is distinct from
what the public evidence identifies. Exact world fields are shown with each task.

Registered record counts and construction audit:

```json
{
  "additional_noise_counts": {
    "forward_current": 2
  },
  "admissible_count": 4,
  "control_basis": "unidentifiable_baseline_world",
  "current_admissible_count": 4,
  "current_witness_contexts": [
    {
      "contract": "temporary",
      "recipient": "internal",
      "task_family": "personnel_document",
      "version": "edition-00e5eb7c0872",
      "workflow": "workflow-7e0284a9f5cd"
    },
    {
      "contract": "permanent",
      "recipient": "external",
      "task_family": "personnel_document",
      "version": "edition-00e5eb7c0872",
      "workflow": "workflow-7e0284a9f5cd"
    },
    {
      "contract": "temporary",
      "recipient": "internal",
      "task_family": "personnel_document",
      "version": "edition-00e5eb7c0872",
      "workflow": "workflow-7e0284a9f5cd"
    }
  ],
  "diagnostic_observed": false,
  "material_revision": "v04-amendment-03-r2",
  "record_count": 6,
  "registered_versions": [
    "edition-00e5eb7c0872"
  ],
  "rendering": "interpreted",
  "reversed_option": false,
  "task_type": "unidentifiable"
}
```

## Single-record counterfactual relevance

Evaluator audit only. Exactly one visible proposed configuration is promoted to a
binding current-version observation at its apparent context. Genuine observations
are retained. An empty compatible set is a contradiction, never an action flip.

Required qualifying outcome for each present type: **action_flip**. All present types qualify: **True**.

Absent types have no fabricated denominator. Technical recovery events are counted
separately in the material audit and are not approval-promotion interventions.

| Manipulated type | Records | Strict action flip | Contradiction | Unchanged | Narrower, same actions | Retention resolved | Unassessable | Qualifying records |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| forward | 2 | 2 | 0 | 0 | 0 | 0 | 0 | record-5e5bc7a546c1, record-8e79f0d57861 |

### Every promoted public record

| Record | Type | Origin | Public option | Remaining policies | Outcome | Qualifies | Diagnostic action | Control action |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| record-5e5bc7a546c1 | forward | record-ed88d1449d9f | 1 | 2 | action_flip | True | keep | apply |
| record-8e79f0d57861 | forward | record-ed88d1449d9f | 1 | 2 | action_flip | True | apply | keep |

### Exact promotions, contexts and public value provenance

The [complete JSON sidecar](S3-hr.json) preserves every intervention under `counterfactual.records`,
including selected field presence/value, effective current context, public origin,
precise promotion and remaining-policy count. No intervention alters the real history.

## Future tasks for this development example

### diagnostic

Public task

```json
{
  "task_id": "task-cb0f54d54662",
  "context": {
    "task_family": "personnel_document",
    "workflow": "workflow-7e0284a9f5cd",
    "version": "edition-00e5eb7c0872",
    "recipient": "internal",
    "contract": "permanent"
  },
  "facts": {
    "document_id": "DOC-38525",
    "date": "2026-06-15",
    "message": "Please prepare the appointment documents for case 38525.",
    "work_email": "contact38525@example.test",
    "booking_reference": "BK-38525"
  },
  "baseline_fields": [
    {
      "name": "message",
      "value": "Please prepare the appointment documents for case 38525."
    },
    {
      "name": "work_email",
      "value": "contact38525@example.test"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Private expected obligations and actual-world fields

```json
{
  "task_id": "task-cb0f54d54662",
  "history_id": "history-b25c68bba955",
  "probe": "diagnostic",
  "expected_decision": "keep",
  "recoverable": false,
  "world_fields": [
    {
      "name": "message",
      "value": "Please prepare the appointment documents for case 38525."
    },
    {
      "name": "work_email",
      "value": "contact38525@example.test"
    },
    {
      "name": "booking_reference",
      "value": "BK-38525"
    }
  ]
}
```

### control

Public task

```json
{
  "task_id": "task-71682033d71f",
  "context": {
    "task_family": "personnel_document",
    "workflow": "workflow-7e0284a9f5cd",
    "version": "edition-00e5eb7c0872",
    "recipient": "external",
    "contract": "temporary"
  },
  "facts": {
    "document_id": "DOC-87928",
    "date": "2026-06-15",
    "message": "Please prepare the appointment documents for case 87928.",
    "work_email": "contact87928@example.test",
    "booking_reference": "BK-87928"
  },
  "baseline_fields": [
    {
      "name": "message",
      "value": "Please prepare the appointment documents for case 87928."
    },
    {
      "name": "work_email",
      "value": "contact87928@example.test"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Private expected obligations and actual-world fields

```json
{
  "task_id": "task-71682033d71f",
  "history_id": "history-b25c68bba955",
  "probe": "control",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "message",
      "value": "Please prepare the appointment documents for case 87928."
    },
    {
      "name": "work_email",
      "value": "contact87928@example.test"
    }
  ]
}
```

## Human response

Pending. No approval is inferred from this export.
