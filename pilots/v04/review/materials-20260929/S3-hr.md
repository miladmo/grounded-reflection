# S3 / hr

Synthetic development example. Not a live evaluation case.

Intended diagnostic regime: **unidentifiable**.
Public records: 6. Admissible policies: 4.

## Public configuration

{"task_family":"personnel_document","workflow":"workflow-c2427dc47447","as_of":"2026-06-15T12:00:00Z","dimensions":{"recipient":["internal","external"],"contract":["permanent","temporary"]},"field_option":{"field":"booking_reference","operation":"omit","value":"","separator":""},"baseline_template":{"message":"{message}","work_email":"{work_email}","booking_reference":"{booking_reference}"},"fact_descriptions":{"message":"Current personnel document text.","work_email":"Current contact email.","booking_reference":"Current booking reference."}}

This is a bounded synthetic workflow model. initial_configuration declares the two available field configurations and two context dimensions. Within a registered version, the selected field configuration is fixed separately for each of the four complete context combinations. This is a supplied modelling restriction, not an inferred claim that other contextual variables never matter in real work. All assignments over those four combinations are possible before evidence. The two options do not imply that either is required. Facts provide current values, not requirement assignments. Other fields retain their configured baseline. Outside the declared task_family and workflow, or without a complete declared context, no update is authorised by this model. A register_version event records the authority roster and the half-open validity interval for that version. Registry records are trusted workflow metadata. An explicit acceptance by an authorised reviewer, within that interval, establishes the approved configuration of reviewed_fields for that exact context and version. Acceptance of an artifact does not approve an unlisted field. Silence is not acceptance. This explicit review convention is part of the synthetic model. A forward references another record; its destination context is not a new review. Comments, execution logs and registry events have their ordinary stated meanings. Their occurrence alone is not a review acceptance. Distinct version labels have separate assignments unless evidence links them. Do not assume an old configuration carries into a new version. The configured baseline is retained when available evidence does not establish an update. Dates and version labels in new work identify the applicable registration.

## Public work records

### record-155ad88e962b

2026-01-01T00:00:00Z | template | workflow-registry

Context: 

```json
{"authorised_reviewers":["Anika","Elena"],"event":"register_version","supersedes":null,"task_family":"personnel_document","valid_from":"2026-01-01T00:00:00Z","valid_until":"2027-01-01T00:00:00Z","version":"edition-fe9597b2b588","workflow":"workflow-c2427dc47447"}
```

### record-65d35cc1a335

2026-06-10T10:00:00Z | review | Anika

Context: task_family=personnel_document, workflow=workflow-c2427dc47447, version=edition-fe9597b2b588, recipient=external, contract=permanent

```json
{"accepted_fields":{"message":"Please prepare the appointment documents for case 90045.","work_email":"contact90045@example.test"},"authority_ref":"record-155ad88e962b","change_summary":{"after":null,"before":"BK-90045","field":"booking_reference"},"comment":"This replacement is approved for the recorded work item.","decision":"accept","document_id":"DOC-90045","event":"review","facts":{"booking_reference":"BK-90045","date":"2026-06-10","document_id":"DOC-90045","message":"Please prepare the appointment documents for case 90045.","work_email":"contact90045@example.test"},"format":"interpreted","reviewed_fields":["booking_reference"]}
```

### record-162edd5df90f

2026-06-11T10:00:00Z | review | Elena

Context: task_family=personnel_document, workflow=workflow-c2427dc47447, version=edition-fe9597b2b588, recipient=external, contract=temporary

```json
{"accepted_fields":{"booking_reference":"BK-44094","message":"Please prepare the appointment documents for case 44094.","work_email":"contact44094@example.test"},"authority_ref":"record-155ad88e962b","change_summary":{"after":"BK-44094","before":null,"field":"booking_reference"},"comment":"This replacement is approved for the recorded work item.","decision":"accept","document_id":"DOC-44094","event":"review","facts":{"booking_reference":"BK-44094","date":"2026-06-11","document_id":"DOC-44094","message":"Please prepare the appointment documents for case 44094.","work_email":"contact44094@example.test"},"format":"interpreted","reviewed_fields":["booking_reference"]}
```

### record-c872429ea7c8

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=personnel_document, workflow=workflow-c2427dc47447, version=edition-fe9597b2b588, recipient=external, contract=temporary

```json
{"document_id":"draft-ee02034b7204","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-2e3f27e3149f

2026-06-14T11:00:00Z | revision | forwarding-service

Context: task_family=personnel_document, workflow=workflow-c2427dc47447, version=edition-fe9597b2b588, recipient=internal, contract=temporary

```json
{"event":"forward","message":"Forwarded review for reference. Please see the linked original artifact.","origin_ref":"record-6021875a04bc"}
```

### record-6021875a04bc

2026-06-14T11:00:00Z | revision | forwarding-service

Context: task_family=personnel_document, workflow=workflow-c2427dc47447, version=edition-fe9597b2b588, recipient=internal, contract=permanent

```json
{"event":"forward","message":"Forwarded review for reference. Please see the linked original artifact.","origin_ref":"record-65d35cc1a335"}
```

## Private evaluator view

The world policy is distinct from what the evidence identifies. The table shows
the complete registered contexts. Baseline and alternative describe field effects,
not whether a professional convention is desirable. Both means unresolved.
All policies, invalid-context probes and exact values remain in the accompanying JSON.

| Version and context | World | Admitted effects | Direct review witnesses |
| --- | --- | --- | --- |
| version=edition-fe9597b2b588, recipient=internal, contract=permanent | alternative | alternative, baseline | none |
| version=edition-fe9597b2b588, recipient=internal, contract=temporary | baseline | alternative, baseline | none |
| version=edition-fe9597b2b588, recipient=external, contract=permanent | alternative | alternative | record-65d35cc1a335 |
| version=edition-fe9597b2b588, recipient=external, contract=temporary | baseline | baseline | record-162edd5df90f |

## Future tasks for this development example

### diagnostic

```json
{
  "task_id": "task-e0ac7a3832c6",
  "context": {
    "task_family": "personnel_document",
    "workflow": "workflow-c2427dc47447",
    "version": "edition-fe9597b2b588",
    "recipient": "internal",
    "contract": "permanent"
  },
  "facts": {
    "document_id": "DOC-32280",
    "date": "2026-06-15",
    "message": "Please prepare the appointment documents for case 32280.",
    "work_email": "contact32280@example.test",
    "booking_reference": "BK-32280"
  },
  "baseline_fields": [
    {
      "name": "message",
      "value": "Please prepare the appointment documents for case 32280."
    },
    {
      "name": "work_email",
      "value": "contact32280@example.test"
    },
    {
      "name": "booking_reference",
      "value": "BK-32280"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Expected obligations

```json
{
  "task_id": "task-e0ac7a3832c6",
  "history_id": "history-8cb578381ebd",
  "probe": "diagnostic",
  "expected_decision": "keep",
  "recoverable": false,
  "world_fields": [
    {
      "name": "message",
      "value": "Please prepare the appointment documents for case 32280."
    },
    {
      "name": "work_email",
      "value": "contact32280@example.test"
    }
  ]
}
```

### control

```json
{
  "task_id": "task-1e3e6deff94d",
  "context": {
    "task_family": "personnel_document",
    "workflow": "workflow-c2427dc47447",
    "version": "edition-fe9597b2b588",
    "recipient": "external",
    "contract": "temporary"
  },
  "facts": {
    "document_id": "DOC-64445",
    "date": "2026-06-15",
    "message": "Please prepare the appointment documents for case 64445.",
    "work_email": "contact64445@example.test",
    "booking_reference": "BK-64445"
  },
  "baseline_fields": [
    {
      "name": "message",
      "value": "Please prepare the appointment documents for case 64445."
    },
    {
      "name": "work_email",
      "value": "contact64445@example.test"
    },
    {
      "name": "booking_reference",
      "value": "BK-64445"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Expected obligations

```json
{
  "task_id": "task-1e3e6deff94d",
  "history_id": "history-8cb578381ebd",
  "probe": "control",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "message",
      "value": "Please prepare the appointment documents for case 64445."
    },
    {
      "name": "work_email",
      "value": "contact64445@example.test"
    },
    {
      "name": "booking_reference",
      "value": "BK-64445"
    }
  ]
}
```

## Human response

Pending. No approval is inferred from this export.
