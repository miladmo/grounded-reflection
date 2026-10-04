# S3 / hr

Material revision: v04-amendment-03. Synthetic development example.

Registered task type: **unidentifiable**. Intended diagnostic regime: **unidentifiable**.
Public records: 6. Control basis: unidentifiable_baseline_world.

## Review summary

Current compatible functions: **4**. Full cross-version policies: 4.

H14 identification is conditional on excluding XOR and XNOR. Retaining an unresolved
baseline does not establish that the baseline is the true requirement.

| Task | Public context | Previously observed | Warranted action | Retention basis |
| --- | --- | --- | --- | --- |
| diagnostic | task_family=personnel_document, workflow=workflow-0d35569dce41, version=edition-45f532dcd9f6, recipient=external, contract=permanent | False | keep | unresolved |
| control | task_family=personnel_document, workflow=workflow-0d35569dce41, version=edition-45f532dcd9f6, recipient=internal, contract=temporary | False | keep | unresolved |

Counterfactual qualification requires **action_flip** for every present type. All present types qualify: **True**.

One qualifying example per present type is shown below. The links lead to its
public evidence; all records and counts appear in the later audit and JSON sidecar.

| Type (record count) | Promoted record / source | Public target value | Exact promotion | Outcome / remaining policies |
| --- | --- | --- | --- | --- |
| forward (2) | [record-350aa96091e7](#record-350aa96091e7) / [record-f9e5ab019e35](#record-f9e5ab019e35) | booking_reference = 'BK-74389' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=personnel_document, workflow=workflow-0d35569dce41, version=edition-45f532dcd9f6, recipient=internal, contract=temporary | action_flip / 2 |

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
  "workflow": "workflow-0d35569dce41"
}
```

This is a bounded synthetic workflow model. initial_configuration declares the field options, two context dimensions and the complete H14 hypothesis class. Each registered version has one class member. A field observation constrains the member indexed by its recorded version. Broader consequences follow from the declared class. Facts provide current artifact values. Other fields retain their configured baseline. Outside the declared task_family and workflow, or without a complete declared context, no update is authorised by this model. A register_version event supplies trusted workflow metadata with the authority roster and half-open validity interval. Binding field approval is an event of type review with decision accept, performed by a listed reviewer within that interval, with the field included in reviewed_fields. Its accepted artifact establishes the field configuration at the recorded context. This explicit approval convention is a supplied synthetic assumption. A forward has an origin_ref identifying the record whose content it reproduces. Raw artifacts expose named revisions and a selected artifact reference; interpreted records expose the selected fields directly. A rejection records a whole-artifact decision and its stated grounds. An artifact field whose review is not recorded has no approved assignment. The configured baseline is retained when the available evidence does not establish an update. Dates and version labels in new work identify the applicable registration.

## Public work records

### record-9356e08a272b

2026-01-01T00:00:00Z | template | workflow-registry

Context: 


```json
{
  "authorised_reviewers": [
    "Theo",
    "Robin"
  ],
  "event": "register_version",
  "supersedes": null,
  "task_family": "personnel_document",
  "valid_from": "2026-01-01T00:00:00Z",
  "valid_until": "2027-01-01T00:00:00Z",
  "version": "edition-45f532dcd9f6",
  "workflow": "workflow-0d35569dce41"
}
```

### record-8340b7954c02

2026-06-10T10:00:00Z | review | Theo

Context: task_family=personnel_document, workflow=workflow-0d35569dce41, version=edition-45f532dcd9f6, recipient=internal, contract=permanent

- decision: accept
- reviewed_fields: ['booking_reference']
- authority_ref: record-9356e08a272b
- comment: Approved.

```json
{
  "accepted_fields": {
    "message": "Please prepare the appointment documents for case 88362.",
    "work_email": "contact88362@example.test"
  },
  "authority_ref": "record-9356e08a272b",
  "change_summary": {
    "after": null,
    "before": "BK-88362",
    "field": "booking_reference"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-88362",
  "event": "review",
  "facts": {
    "booking_reference": "BK-88362",
    "date": "2026-06-10",
    "document_id": "DOC-88362",
    "message": "Please prepare the appointment documents for case 88362.",
    "work_email": "contact88362@example.test"
  },
  "format": "interpreted",
  "reviewed_fields": [
    "booking_reference"
  ]
}
```

### record-f9e5ab019e35

2026-06-11T10:00:00Z | review | Robin

Context: task_family=personnel_document, workflow=workflow-0d35569dce41, version=edition-45f532dcd9f6, recipient=external, contract=temporary

- decision: accept
- reviewed_fields: ['booking_reference']
- authority_ref: record-9356e08a272b
- comment: Approved.

```json
{
  "accepted_fields": {
    "booking_reference": "BK-74389",
    "message": "Please prepare the appointment documents for case 74389.",
    "work_email": "contact74389@example.test"
  },
  "authority_ref": "record-9356e08a272b",
  "change_summary": {
    "after": "BK-74389",
    "before": null,
    "field": "booking_reference"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-74389",
  "event": "review",
  "facts": {
    "booking_reference": "BK-74389",
    "date": "2026-06-11",
    "document_id": "DOC-74389",
    "message": "Please prepare the appointment documents for case 74389.",
    "work_email": "contact74389@example.test"
  },
  "format": "interpreted",
  "reviewed_fields": [
    "booking_reference"
  ]
}
```

### record-2dbb9570989c

2026-06-12T10:00:00Z | review | Theo

Context: task_family=personnel_document, workflow=workflow-0d35569dce41, version=edition-45f532dcd9f6, recipient=internal, contract=permanent

- decision: accept
- reviewed_fields: ['booking_reference']
- authority_ref: record-9356e08a272b
- comment: Approved.

```json
{
  "accepted_fields": {
    "message": "Please prepare the appointment documents for case 17635.",
    "work_email": "contact17635@example.test"
  },
  "authority_ref": "record-9356e08a272b",
  "change_summary": {
    "after": null,
    "before": "BK-17635",
    "field": "booking_reference"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-17635",
  "event": "review",
  "facts": {
    "booking_reference": "BK-17635",
    "date": "2026-06-12",
    "document_id": "DOC-17635",
    "message": "Please prepare the appointment documents for case 17635.",
    "work_email": "contact17635@example.test"
  },
  "format": "interpreted",
  "reviewed_fields": [
    "booking_reference"
  ]
}
```

### record-350aa96091e7

2026-06-14T11:00:00Z | revision | forwarding-service

Context: task_family=personnel_document, workflow=workflow-0d35569dce41, version=edition-45f532dcd9f6, recipient=internal, contract=temporary

- origin_ref: record-f9e5ab019e35

```json
{
  "event": "forward",
  "message": "Forwarded artifact for the next work item.",
  "origin_ref": "record-f9e5ab019e35"
}
```

### record-4bf8b5c02bd2

2026-06-14T11:01:00Z | revision | forwarding-service

Context: task_family=personnel_document, workflow=workflow-0d35569dce41, version=edition-45f532dcd9f6, recipient=external, contract=permanent

- origin_ref: record-f9e5ab019e35

```json
{
  "event": "forward",
  "message": "Forwarded artifact for the next work item.",
  "origin_ref": "record-f9e5ab019e35"
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
| record-8340b7954c02 | edition-45f532dcd9f6 | task_family=personnel_document, workflow=workflow-0d35569dce41, version=edition-45f532dcd9f6, recipient=internal, contract=permanent | 0 |
| record-f9e5ab019e35 | edition-45f532dcd9f6 | task_family=personnel_document, workflow=workflow-0d35569dce41, version=edition-45f532dcd9f6, recipient=external, contract=temporary | 1 |
| record-2dbb9570989c | edition-45f532dcd9f6 | task_family=personnel_document, workflow=workflow-0d35569dce41, version=edition-45f532dcd9f6, recipient=internal, contract=permanent | 0 |

### Competing requirement explanations

Zero is the configured baseline; one is the alternative. Each row is a distinct
compatible function for this version. No preference for simplicity removes a row.
The private sampling plan and world policy do not filter these explanations.

Version edition-45f532dcd9f6: 4 compatible functions.

| Function | recipient=internal, contract=permanent | recipient=internal, contract=temporary | recipient=external, contract=permanent | recipient=external, contract=temporary | Complexity |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | 0 | 0 | 1 | 2 |
| 2 | 0 | 0 | 1 | 1 | 1 |
| 3 | 0 | 1 | 0 | 1 | 1 |
| 4 | 0 | 1 | 1 | 1 | 2 |

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
      "contract": "permanent",
      "recipient": "internal",
      "task_family": "personnel_document",
      "version": "edition-45f532dcd9f6",
      "workflow": "workflow-0d35569dce41"
    },
    {
      "contract": "temporary",
      "recipient": "external",
      "task_family": "personnel_document",
      "version": "edition-45f532dcd9f6",
      "workflow": "workflow-0d35569dce41"
    },
    {
      "contract": "permanent",
      "recipient": "internal",
      "task_family": "personnel_document",
      "version": "edition-45f532dcd9f6",
      "workflow": "workflow-0d35569dce41"
    }
  ],
  "diagnostic_observed": false,
  "material_revision": "v04-amendment-03",
  "record_count": 6,
  "registered_versions": [
    "edition-45f532dcd9f6"
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
| forward | 2 | 2 | 0 | 0 | 0 | 0 | 0 | record-350aa96091e7, record-4bf8b5c02bd2 |

### Every promoted public record

| Record | Type | Origin | Public option | Remaining policies | Outcome | Qualifies | Diagnostic action | Control action |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| record-350aa96091e7 | forward | record-f9e5ab019e35 | 1 | 2 | action_flip | True | keep | apply |
| record-4bf8b5c02bd2 | forward | record-f9e5ab019e35 | 1 | 2 | action_flip | True | apply | keep |

### Exact promotions, contexts and public value provenance

The [complete JSON sidecar](S3-hr.json) preserves every intervention under `counterfactual.records`,
including selected field presence/value, effective current context, public origin,
precise promotion and remaining-policy count. No intervention alters the real history.

## Future tasks for this development example

### diagnostic

Public task

```json
{
  "task_id": "task-0ef2c071e236",
  "context": {
    "task_family": "personnel_document",
    "workflow": "workflow-0d35569dce41",
    "version": "edition-45f532dcd9f6",
    "recipient": "external",
    "contract": "permanent"
  },
  "facts": {
    "document_id": "DOC-22974",
    "date": "2026-06-15",
    "message": "Please prepare the appointment documents for case 22974.",
    "work_email": "contact22974@example.test",
    "booking_reference": "BK-22974"
  },
  "baseline_fields": [
    {
      "name": "message",
      "value": "Please prepare the appointment documents for case 22974."
    },
    {
      "name": "work_email",
      "value": "contact22974@example.test"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Private expected obligations and actual-world fields

```json
{
  "task_id": "task-0ef2c071e236",
  "history_id": "history-9ff6c57e650c",
  "probe": "diagnostic",
  "expected_decision": "keep",
  "recoverable": false,
  "world_fields": [
    {
      "name": "message",
      "value": "Please prepare the appointment documents for case 22974."
    },
    {
      "name": "work_email",
      "value": "contact22974@example.test"
    },
    {
      "name": "booking_reference",
      "value": "BK-22974"
    }
  ]
}
```

### control

Public task

```json
{
  "task_id": "task-205f4f95bdec",
  "context": {
    "task_family": "personnel_document",
    "workflow": "workflow-0d35569dce41",
    "version": "edition-45f532dcd9f6",
    "recipient": "internal",
    "contract": "temporary"
  },
  "facts": {
    "document_id": "DOC-72796",
    "date": "2026-06-15",
    "message": "Please prepare the appointment documents for case 72796.",
    "work_email": "contact72796@example.test",
    "booking_reference": "BK-72796"
  },
  "baseline_fields": [
    {
      "name": "message",
      "value": "Please prepare the appointment documents for case 72796."
    },
    {
      "name": "work_email",
      "value": "contact72796@example.test"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Private expected obligations and actual-world fields

```json
{
  "task_id": "task-205f4f95bdec",
  "history_id": "history-9ff6c57e650c",
  "probe": "control",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "message",
      "value": "Please prepare the appointment documents for case 72796."
    },
    {
      "name": "work_email",
      "value": "contact72796@example.test"
    }
  ]
}
```

## Human response

Pending. No approval is inferred from this export.
