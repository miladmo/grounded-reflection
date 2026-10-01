# S0 / hr

Synthetic development example. Not a live evaluation case.

Intended diagnostic regime: **change**.
Public records: 6. Admissible policies: 4.

## Public configuration

{"task_family":"personnel_document","workflow":"workflow-a7441d0180c8","as_of":"2026-06-15T12:00:00Z","dimensions":{"recipient":["internal","external"],"contract":["permanent","temporary"]},"field_option":{"field":"booking_reference","operation":"omit","value":"","separator":""},"baseline_template":{"message":"{message}","work_email":"{work_email}","booking_reference":"{booking_reference}"},"fact_descriptions":{"message":"Current personnel document text.","work_email":"Current contact email.","booking_reference":"Current booking reference."}}

This is a bounded synthetic workflow model. initial_configuration declares the two available field configurations and two context dimensions. Within a registered version, the selected field configuration is fixed separately for each of the four complete context combinations. This is a supplied modelling restriction, not an inferred claim that other contextual variables never matter in real work. All assignments over those four combinations are possible before evidence. The two options do not imply that either is required. Facts provide current values, not requirement assignments. Other fields retain their configured baseline. Outside the declared task_family and workflow, or without a complete declared context, no update is authorised by this model. A register_version event records the authority roster and the half-open validity interval for that version. Registry records are trusted workflow metadata. An explicit acceptance by an authorised reviewer, within that interval, establishes the approved configuration of reviewed_fields for that exact context and version. Acceptance of an artifact does not approve an unlisted field. Silence is not acceptance. This explicit review convention is part of the synthetic model. A forward references another record; its destination context is not a new review. Comments, execution logs and registry events have their ordinary stated meanings. Their occurrence alone is not a review acceptance. Distinct version labels have separate assignments unless evidence links them. Do not assume an old configuration carries into a new version. The configured baseline is retained when available evidence does not establish an update. Dates and version labels in new work identify the applicable registration.

## Public work records

### record-ee70a4226a86

2026-01-01T00:00:00Z | template | workflow-registry

Context: 

```json
{"authorised_reviewers":["Robin","Theo"],"event":"register_version","supersedes":null,"task_family":"personnel_document","valid_from":"2026-01-01T00:00:00Z","valid_until":"2027-01-01T00:00:00Z","version":"edition-9f2ec213e215","workflow":"workflow-a7441d0180c8"}
```

### record-cf0b5027b332

2026-06-10T10:00:00Z | review | Robin

Context: task_family=personnel_document, workflow=workflow-a7441d0180c8, version=edition-9f2ec213e215, recipient=external, contract=permanent

```json
{"accepted_fields":{"message":"Please prepare the appointment documents for case 40269.","work_email":"contact40269@example.test"},"authority_ref":"record-ee70a4226a86","change_summary":{"after":null,"before":"BK-40269","field":"booking_reference"},"comment":"This replacement is approved for the recorded work item.","decision":"accept","document_id":"DOC-40269","event":"review","facts":{"booking_reference":"BK-40269","date":"2026-06-10","document_id":"DOC-40269","message":"Please prepare the appointment documents for case 40269.","work_email":"contact40269@example.test"},"format":"interpreted","reviewed_fields":["booking_reference"]}
```

### record-f97a54f0d88c

2026-06-11T10:00:00Z | review | Theo

Context: task_family=personnel_document, workflow=workflow-a7441d0180c8, version=edition-9f2ec213e215, recipient=external, contract=temporary

```json
{"accepted_fields":{"booking_reference":"BK-28706","message":"Please prepare the appointment documents for case 28706.","work_email":"contact28706@example.test"},"authority_ref":"record-ee70a4226a86","change_summary":{"after":"BK-28706","before":null,"field":"booking_reference"},"comment":"This replacement is approved for the recorded work item.","decision":"accept","document_id":"DOC-28706","event":"review","facts":{"booking_reference":"BK-28706","date":"2026-06-11","document_id":"DOC-28706","message":"Please prepare the appointment documents for case 28706.","work_email":"contact28706@example.test"},"format":"interpreted","reviewed_fields":["booking_reference"]}
```

### record-06f17abd229a

2026-06-12T10:00:00Z | review | Robin

Context: task_family=personnel_document, workflow=workflow-a7441d0180c8, version=edition-9f2ec213e215, recipient=external, contract=permanent

```json
{"accepted_fields":{"message":"Please prepare the appointment documents for case 50575.","work_email":"contact50575@example.test"},"authority_ref":"record-ee70a4226a86","change_summary":{"after":null,"before":"BK-50575","field":"booking_reference"},"comment":"This replacement is approved for the recorded work item.","decision":"accept","document_id":"DOC-50575","event":"review","facts":{"booking_reference":"BK-50575","date":"2026-06-12","document_id":"DOC-50575","message":"Please prepare the appointment documents for case 50575.","work_email":"contact50575@example.test"},"format":"interpreted","reviewed_fields":["booking_reference"]}
```

### record-0960fb342997

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=personnel_document, workflow=workflow-a7441d0180c8, version=edition-9f2ec213e215, recipient=internal, contract=permanent

```json
{"document_id":"draft-2c59f07d0a65","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-a8c4e6ce214f

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=personnel_document, workflow=workflow-a7441d0180c8, version=edition-9f2ec213e215, recipient=internal, contract=permanent

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-58ca8db3f54c"}
```

## Private evaluator view

The world policy is distinct from what the evidence identifies. The table shows
the complete registered contexts. Baseline and alternative describe field effects,
not whether a professional convention is desirable. Both means unresolved.
All policies, invalid-context probes and exact values remain in the accompanying JSON.

| Version and context | World | Admitted effects | Direct review witnesses |
| --- | --- | --- | --- |
| version=edition-9f2ec213e215, recipient=internal, contract=permanent | baseline | alternative, baseline | none |
| version=edition-9f2ec213e215, recipient=internal, contract=temporary | alternative | alternative, baseline | none |
| version=edition-9f2ec213e215, recipient=external, contract=permanent | alternative | alternative | record-cf0b5027b332, record-06f17abd229a |
| version=edition-9f2ec213e215, recipient=external, contract=temporary | baseline | baseline | record-f97a54f0d88c |

## Future tasks for this development example

### diagnostic

```json
{
  "task_id": "task-136fa1b4bc22",
  "context": {
    "task_family": "personnel_document",
    "workflow": "workflow-a7441d0180c8",
    "version": "edition-9f2ec213e215",
    "recipient": "external",
    "contract": "permanent"
  },
  "facts": {
    "document_id": "DOC-27862",
    "date": "2026-06-15",
    "message": "Please prepare the appointment documents for case 27862.",
    "work_email": "contact27862@example.test",
    "booking_reference": "BK-27862"
  },
  "baseline_fields": [
    {
      "name": "message",
      "value": "Please prepare the appointment documents for case 27862."
    },
    {
      "name": "work_email",
      "value": "contact27862@example.test"
    },
    {
      "name": "booking_reference",
      "value": "BK-27862"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Expected obligations

```json
{
  "task_id": "task-136fa1b4bc22",
  "history_id": "history-e9d2cc6a8639",
  "probe": "diagnostic",
  "expected_decision": "apply",
  "recoverable": true,
  "world_fields": [
    {
      "name": "message",
      "value": "Please prepare the appointment documents for case 27862."
    },
    {
      "name": "work_email",
      "value": "contact27862@example.test"
    }
  ]
}
```

### control

```json
{
  "task_id": "task-3a5661780d92",
  "context": {
    "task_family": "personnel_document",
    "workflow": "workflow-a7441d0180c8",
    "version": "edition-9f2ec213e215",
    "recipient": "external",
    "contract": "temporary"
  },
  "facts": {
    "document_id": "DOC-58188",
    "date": "2026-06-15",
    "message": "Please prepare the appointment documents for case 58188.",
    "work_email": "contact58188@example.test",
    "booking_reference": "BK-58188"
  },
  "baseline_fields": [
    {
      "name": "message",
      "value": "Please prepare the appointment documents for case 58188."
    },
    {
      "name": "work_email",
      "value": "contact58188@example.test"
    },
    {
      "name": "booking_reference",
      "value": "BK-58188"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Expected obligations

```json
{
  "task_id": "task-3a5661780d92",
  "history_id": "history-e9d2cc6a8639",
  "probe": "control",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "message",
      "value": "Please prepare the appointment documents for case 58188."
    },
    {
      "name": "work_email",
      "value": "contact58188@example.test"
    },
    {
      "name": "booking_reference",
      "value": "BK-58188"
    }
  ]
}
```

## Human response

Pending. No approval is inferred from this export.
