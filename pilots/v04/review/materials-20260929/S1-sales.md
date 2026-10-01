# S1 / sales

Synthetic development example. Not a live evaluation case.

Intended diagnostic regime: **unidentifiable**.
Public records: 6. Admissible policies: 4.

## Public configuration

{"task_family":"sales_offer","workflow":"workflow-715db261d8fb","as_of":"2026-06-15T12:00:00Z","dimensions":{"reviewer":["Sada","Nora"],"customer_segment":["standard","strategic"]},"field_option":{"field":"annual_total","operation":"set_fact","value":"annual_total","separator":""},"baseline_template":{"offer_text":"{offer_text}","contract_reference":"{contract_reference}"},"fact_descriptions":{"offer_text":"Current offer text.","contract_reference":"Current offer reference.","monthly_unit_price":"EUR per seat and month.","seats":"Number of seats.","annual_total":"EUR, monthly_unit_price times seats times twelve."}}

This is a bounded synthetic workflow model. initial_configuration declares the two available field configurations and two context dimensions. Within a registered version, the selected field configuration is fixed separately for each of the four complete context combinations. This is a supplied modelling restriction, not an inferred claim that other contextual variables never matter in real work. All assignments over those four combinations are possible before evidence. The two options do not imply that either is required. Facts provide current values, not requirement assignments. Other fields retain their configured baseline. Outside the declared task_family and workflow, or without a complete declared context, no update is authorised by this model. A register_version event records the authority roster and the half-open validity interval for that version. Registry records are trusted workflow metadata. An explicit acceptance by an authorised reviewer, within that interval, establishes the approved configuration of reviewed_fields for that exact context and version. Acceptance of an artifact does not approve an unlisted field. Silence is not acceptance. This explicit review convention is part of the synthetic model. A forward references another record; its destination context is not a new review. Comments, execution logs and registry events have their ordinary stated meanings. Their occurrence alone is not a review acceptance. Distinct version labels have separate assignments unless evidence links them. Do not assume an old configuration carries into a new version. The configured baseline is retained when available evidence does not establish an update. Dates and version labels in new work identify the applicable registration.

## Public work records

### record-41768b02dbb6

2026-01-01T00:00:00Z | template | workflow-registry

Context: 

```json
{"authorised_reviewers":["Theo","Jonas"],"event":"register_version","supersedes":null,"task_family":"sales_offer","valid_from":"2026-01-01T00:00:00Z","valid_until":"2027-01-01T00:00:00Z","version":"edition-a1bc340e23c5","workflow":"workflow-715db261d8fb"}
```

### record-b69b3a5c31ef

2026-06-10T10:00:00Z | review | Theo

Context: task_family=sales_offer, workflow=workflow-715db261d8fb, version=edition-a1bc340e23c5, reviewer=Nora, customer_segment=standard

```json
{"accepted_artifact":"replacement","artifacts":{"draft":{"fields":{"contract_reference":"OFF-77260","offer_text":"20 seats at EUR 40 per seat per month, billed annually."},"revision":"draft"},"replacement":{"fields":{"annual_total":"9600","contract_reference":"OFF-77260","offer_text":"20 seats at EUR 40 per seat per month, billed annually."},"revision":"reviewed"}},"authority_ref":"record-41768b02dbb6","comment":"This replacement is approved for the recorded work item.","decision":"accept","document_id":"DOC-77260","event":"review","facts":{"annual_total":"9600","contract_reference":"OFF-77260","date":"2026-06-10","document_id":"DOC-77260","monthly_unit_price":"40","offer_text":"20 seats at EUR 40 per seat per month, billed annually.","seats":"20"},"format":"raw","reviewed_fields":["annual_total"]}
```

### record-59323a5a8ca3

2026-06-11T10:00:00Z | review | Jonas

Context: task_family=sales_offer, workflow=workflow-715db261d8fb, version=edition-a1bc340e23c5, reviewer=Sada, customer_segment=strategic

```json
{"accepted_artifact":"replacement","artifacts":{"draft":{"fields":{"annual_total":"9000","contract_reference":"OFF-99186","offer_text":"15 seats at EUR 50 per seat per month, billed annually."},"revision":"draft"},"replacement":{"fields":{"contract_reference":"OFF-99186","offer_text":"15 seats at EUR 50 per seat per month, billed annually."},"revision":"reviewed"}},"authority_ref":"record-41768b02dbb6","comment":"This replacement is approved for the recorded work item.","decision":"accept","document_id":"DOC-99186","event":"review","facts":{"annual_total":"9000","contract_reference":"OFF-99186","date":"2026-06-11","document_id":"DOC-99186","monthly_unit_price":"50","offer_text":"15 seats at EUR 50 per seat per month, billed annually.","seats":"15"},"format":"raw","reviewed_fields":["annual_total"]}
```

### record-c2cbc03603ac

2026-06-12T10:00:00Z | review | Theo

Context: task_family=sales_offer, workflow=workflow-715db261d8fb, version=edition-a1bc340e23c5, reviewer=Nora, customer_segment=standard

```json
{"accepted_artifact":"replacement","artifacts":{"draft":{"fields":{"contract_reference":"OFF-73539","offer_text":"10 seats at EUR 65 per seat per month, billed annually."},"revision":"draft"},"replacement":{"fields":{"annual_total":"7800","contract_reference":"OFF-73539","offer_text":"10 seats at EUR 65 per seat per month, billed annually."},"revision":"reviewed"}},"authority_ref":"record-41768b02dbb6","comment":"This replacement is approved for the recorded work item.","decision":"accept","document_id":"DOC-73539","event":"review","facts":{"annual_total":"7800","contract_reference":"OFF-73539","date":"2026-06-12","document_id":"DOC-73539","monthly_unit_price":"65","offer_text":"10 seats at EUR 65 per seat per month, billed annually.","seats":"10"},"format":"raw","reviewed_fields":["annual_total"]}
```

### record-1b6488d1b78b

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-715db261d8fb, version=edition-a1bc340e23c5, reviewer=Sada, customer_segment=standard

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-bcd637e8caab"}
```

### record-a6e90c1e89b6

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-715db261d8fb, version=edition-a1bc340e23c5, reviewer=Sada, customer_segment=strategic

```json
{"document_id":"draft-8a07be367f92","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

## Private evaluator view

The world policy is distinct from what the evidence identifies. The table shows
the complete registered contexts. Baseline and alternative describe field effects,
not whether a professional convention is desirable. Both means unresolved.
All policies, invalid-context probes and exact values remain in the accompanying JSON.

| Version and context | World | Admitted effects | Direct review witnesses |
| --- | --- | --- | --- |
| version=edition-a1bc340e23c5, reviewer=Sada, customer_segment=standard | baseline | alternative, baseline | none |
| version=edition-a1bc340e23c5, reviewer=Sada, customer_segment=strategic | baseline | baseline | record-59323a5a8ca3 |
| version=edition-a1bc340e23c5, reviewer=Nora, customer_segment=standard | alternative | alternative | record-b69b3a5c31ef, record-c2cbc03603ac |
| version=edition-a1bc340e23c5, reviewer=Nora, customer_segment=strategic | alternative | alternative, baseline | none |

## Future tasks for this development example

### diagnostic

```json
{
  "task_id": "task-3a13d185a5af",
  "context": {
    "task_family": "sales_offer",
    "workflow": "workflow-715db261d8fb",
    "version": "edition-a1bc340e23c5",
    "reviewer": "Nora",
    "customer_segment": "strategic"
  },
  "facts": {
    "document_id": "DOC-56063",
    "date": "2026-06-15",
    "monthly_unit_price": "50",
    "seats": "20",
    "annual_total": "12000",
    "contract_reference": "OFF-56063",
    "offer_text": "20 seats at EUR 50 per seat per month, billed annually."
  },
  "baseline_fields": [
    {
      "name": "offer_text",
      "value": "20 seats at EUR 50 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-56063"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Expected obligations

```json
{
  "task_id": "task-3a13d185a5af",
  "history_id": "history-1138113f5c8a",
  "probe": "diagnostic",
  "expected_decision": "keep",
  "recoverable": false,
  "world_fields": [
    {
      "name": "offer_text",
      "value": "20 seats at EUR 50 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-56063"
    },
    {
      "name": "annual_total",
      "value": "12000"
    }
  ]
}
```

### control

```json
{
  "task_id": "task-a0224f10d5cf",
  "context": {
    "task_family": "sales_offer",
    "workflow": "workflow-715db261d8fb",
    "version": "edition-a1bc340e23c5",
    "reviewer": "Sada",
    "customer_segment": "strategic"
  },
  "facts": {
    "document_id": "DOC-33585",
    "date": "2026-06-15",
    "monthly_unit_price": "50",
    "seats": "15",
    "annual_total": "9000",
    "contract_reference": "OFF-33585",
    "offer_text": "15 seats at EUR 50 per seat per month, billed annually."
  },
  "baseline_fields": [
    {
      "name": "offer_text",
      "value": "15 seats at EUR 50 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-33585"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Expected obligations

```json
{
  "task_id": "task-a0224f10d5cf",
  "history_id": "history-1138113f5c8a",
  "probe": "control",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "offer_text",
      "value": "15 seats at EUR 50 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-33585"
    }
  ]
}
```

## Human response

Pending. No approval is inferred from this export.
