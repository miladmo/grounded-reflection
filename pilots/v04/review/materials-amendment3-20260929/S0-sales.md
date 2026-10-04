# S0 / sales

Material revision: v04-amendment-03. Synthetic development example.

Registered task type: **observed_change**. Intended diagnostic regime: **change**.
Public records: 6. Control basis: resolved_keep.

## Review summary

Current compatible functions: **3**. Full cross-version policies: 3.

H14 identification is conditional on excluding XOR and XNOR. Retaining an unresolved
baseline does not establish that the baseline is the true requirement.

| Task | Public context | Previously observed | Warranted action | Retention basis |
| --- | --- | --- | --- | --- |
| diagnostic | task_family=sales_offer, workflow=workflow-bf7741f986ca, version=edition-a0a446a5fef5, account_owner=Alex, customer_segment=strategic | True | apply | not_retention |
| control | task_family=sales_offer, workflow=workflow-bf7741f986ca, version=edition-a0a446a5fef5, account_owner=Sada, customer_segment=strategic | True | keep | resolved |

Counterfactual qualification requires **contradiction** for every present type. All present types qualify: **True**.

One qualifying example per present type is shown below. The links lead to its
public evidence; all records and counts appear in the later audit and JSON sidecar.

| Type (record count) | Promoted record / source | Public target value | Exact promotion | Outcome / remaining policies |
| --- | --- | --- | --- | --- |
| target_field_preference (1) | [record-3650c6a39b6c](#record-3650c6a39b6c) | annual_total = absent | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=sales_offer, workflow=workflow-bf7741f986ca, version=edition-a0a446a5fef5, account_owner=Sada, customer_segment=strategic | contradiction / 0 |

An action flip requires a nonempty compatible set and a changed diagnostic or control
action. A contradiction has no compatible policy and supplies neither task action.

[Complete oracle derivation](#oracle-derivation-from-public-evidence) · [Every counterfactual record](#single-record-counterfactual-relevance)

## Public configuration and assumptions

```json
{
  "as_of": "2026-06-15T12:00:00Z",
  "baseline_template": {
    "annual_total": "{annual_total}",
    "contract_reference": "{contract_reference}",
    "offer_text": "{offer_text}"
  },
  "dimensions": {
    "account_owner": [
      "Alex",
      "Sada"
    ],
    "customer_segment": [
      "standard",
      "strategic"
    ]
  },
  "fact_descriptions": {
    "annual_total": "EUR, monthly_unit_price times seats times twelve.",
    "contract_reference": "Current offer reference.",
    "monthly_unit_price": "EUR per seat and month.",
    "offer_text": "Current offer text.",
    "seats": "Number of seats."
  },
  "field_option": {
    "field": "annual_total",
    "operation": "omit",
    "separator": "",
    "value": ""
  },
  "hypothesis_class": "h14",
  "hypothesis_definition": "Each of the two declared binary context dimensions defines a predicate testing its second listed value. Call these predicates x and y. In each registered version the target field configuration is one Boolean function from the following class: constant 0 or 1; x, not x, y, or not y; a conjunction of one literal from each dimension; or a disjunction of one literal from each dimension. Zero selects the configured baseline and one the available alternative. The fourteen distinct truth tables exclude only XOR and XNOR. Each version has its own class member, with no cross-version coupling. This restriction is a supplied synthetic assumption, not an established property of enterprise work.",
  "task_family": "sales_offer",
  "workflow": "workflow-bf7741f986ca"
}
```

This is a bounded synthetic workflow model. initial_configuration declares the field options, two context dimensions and the complete H14 hypothesis class. Each registered version has one class member. A field observation constrains the member indexed by its recorded version. Broader consequences follow from the declared class. Facts provide current artifact values. Other fields retain their configured baseline. Outside the declared task_family and workflow, or without a complete declared context, no update is authorised by this model. A register_version event supplies trusted workflow metadata with the authority roster and half-open validity interval. Binding field approval is an event of type review with decision accept, performed by a listed reviewer within that interval, with the field included in reviewed_fields. Its accepted artifact establishes the field configuration at the recorded context. This explicit approval convention is a supplied synthetic assumption. A forward has an origin_ref identifying the record whose content it reproduces. Raw artifacts expose named revisions and a selected artifact reference; interpreted records expose the selected fields directly. A rejection records a whole-artifact decision and its stated grounds. An artifact field whose review is not recorded has no approved assignment. The configured baseline is retained when the available evidence does not establish an update. Dates and version labels in new work identify the applicable registration.

## Public work records

### record-9a104312933b

2026-01-01T00:00:00Z | template | workflow-registry

Context: 


```json
{
  "authorised_reviewers": [
    "Elena",
    "Theo"
  ],
  "event": "register_version",
  "supersedes": null,
  "task_family": "sales_offer",
  "valid_from": "2026-01-01T00:00:00Z",
  "valid_until": "2027-01-01T00:00:00Z",
  "version": "edition-a0a446a5fef5",
  "workflow": "workflow-bf7741f986ca"
}
```

### record-8e42e136f9ba

2026-06-10T10:00:00Z | review | Elena

Context: task_family=sales_offer, workflow=workflow-bf7741f986ca, version=edition-a0a446a5fef5, account_owner=Sada, customer_segment=strategic

- decision: accept
- reviewed_fields: ['annual_total']
- authority_ref: record-9a104312933b
- comment: Approved.

```json
{
  "accepted_fields": {
    "annual_total": "6000",
    "contract_reference": "OFF-90332",
    "offer_text": "20 seats at EUR 25 per seat per month, billed annually."
  },
  "authority_ref": "record-9a104312933b",
  "change_summary": {
    "after": "6000",
    "before": null,
    "field": "annual_total"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-90332",
  "event": "review",
  "facts": {
    "annual_total": "6000",
    "contract_reference": "OFF-90332",
    "date": "2026-06-10",
    "document_id": "DOC-90332",
    "monthly_unit_price": "25",
    "offer_text": "20 seats at EUR 25 per seat per month, billed annually.",
    "seats": "20"
  },
  "format": "interpreted",
  "reviewed_fields": [
    "annual_total"
  ]
}
```

### record-f7dbd7423041

2026-06-11T10:00:00Z | review | Theo

Context: task_family=sales_offer, workflow=workflow-bf7741f986ca, version=edition-a0a446a5fef5, account_owner=Alex, customer_segment=strategic

- decision: accept
- reviewed_fields: ['annual_total']
- authority_ref: record-9a104312933b
- comment: Approved.

```json
{
  "accepted_fields": {
    "contract_reference": "OFF-68436",
    "offer_text": "5 seats at EUR 40 per seat per month, billed annually."
  },
  "authority_ref": "record-9a104312933b",
  "change_summary": {
    "after": null,
    "before": "2400",
    "field": "annual_total"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-68436",
  "event": "review",
  "facts": {
    "annual_total": "2400",
    "contract_reference": "OFF-68436",
    "date": "2026-06-11",
    "document_id": "DOC-68436",
    "monthly_unit_price": "40",
    "offer_text": "5 seats at EUR 40 per seat per month, billed annually.",
    "seats": "5"
  },
  "format": "interpreted",
  "reviewed_fields": [
    "annual_total"
  ]
}
```

### record-5672fd2c2cbd

2026-06-12T10:00:00Z | review | Elena

Context: task_family=sales_offer, workflow=workflow-bf7741f986ca, version=edition-a0a446a5fef5, account_owner=Alex, customer_segment=strategic

- decision: accept
- reviewed_fields: ['annual_total']
- authority_ref: record-9a104312933b
- comment: Approved.

```json
{
  "accepted_fields": {
    "contract_reference": "OFF-18783",
    "offer_text": "5 seats at EUR 25 per seat per month, billed annually."
  },
  "authority_ref": "record-9a104312933b",
  "change_summary": {
    "after": null,
    "before": "1500",
    "field": "annual_total"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-18783",
  "event": "review",
  "facts": {
    "annual_total": "1500",
    "contract_reference": "OFF-18783",
    "date": "2026-06-12",
    "document_id": "DOC-18783",
    "monthly_unit_price": "25",
    "offer_text": "5 seats at EUR 25 per seat per month, billed annually.",
    "seats": "5"
  },
  "format": "interpreted",
  "reviewed_fields": [
    "annual_total"
  ]
}
```

### record-6b60c73394aa

2026-06-14T08:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-bf7741f986ca, version=edition-a0a446a5fef5, account_owner=Alex, customer_segment=standard


```json
{
  "attempts": [
    {
      "attempt": 1,
      "http_status": 503
    },
    {
      "attempt": 2,
      "http_status": 200
    }
  ],
  "event": "execution",
  "log": "The request completed on retry.",
  "request_id": "request-005be67b545a"
}
```

### record-3650c6a39b6c

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=sales_offer, workflow=workflow-bf7741f986ca, version=edition-a0a446a5fef5, account_owner=Sada, customer_segment=strategic


```json
{
  "event": "preference",
  "facts": {
    "annual_total": "3000",
    "contract_reference": "OFF-56702",
    "date": "2026-06-14",
    "document_id": "DOC-56702",
    "monthly_unit_price": "25",
    "offer_text": "10 seats at EUR 25 per seat per month, billed annually.",
    "seats": "10"
  },
  "message": "My preference for this work item is that annual_total should be omitted.",
  "proposed_fields": {
    "contract_reference": "OFF-56702",
    "offer_text": "10 seats at EUR 25 per seat per month, billed annually."
  }
}
```

## Oracle derivation from public evidence

Recomputed solely from the public History by the independent oracle.

H14 excludes XOR and XNOR; transfer identification depends on this supplied restriction.

Distinct current-version functions: **3**. Full policies across all registered versions: **3**.

An approval constrains one cell in its registered version. The following are the
actual applied constraints, including independent repeats. Copies do not add a constraint.

| Public record | Version | Context | Field option |
| --- | --- | --- | --- |
| record-8e42e136f9ba | edition-a0a446a5fef5 | task_family=sales_offer, workflow=workflow-bf7741f986ca, version=edition-a0a446a5fef5, account_owner=Sada, customer_segment=strategic | 0 |
| record-f7dbd7423041 | edition-a0a446a5fef5 | task_family=sales_offer, workflow=workflow-bf7741f986ca, version=edition-a0a446a5fef5, account_owner=Alex, customer_segment=strategic | 1 |
| record-5672fd2c2cbd | edition-a0a446a5fef5 | task_family=sales_offer, workflow=workflow-bf7741f986ca, version=edition-a0a446a5fef5, account_owner=Alex, customer_segment=strategic | 1 |

### Competing requirement explanations

Zero is the configured baseline; one is the alternative. Each row is a distinct
compatible function for this version. No preference for simplicity removes a row.
The private sampling plan and world policy do not filter these explanations.

Version edition-a0a446a5fef5: 3 compatible functions.

| Function | account_owner=Alex, customer_segment=standard | account_owner=Alex, customer_segment=strategic | account_owner=Sada, customer_segment=standard | account_owner=Sada, customer_segment=strategic | Complexity |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | 1 | 0 | 0 | 2 |
| 2 | 1 | 1 | 0 | 0 | 1 |
| 3 | 1 | 1 | 1 | 0 | 2 |

### Diagnostic and control derivations

| Task | Context observed | Witnesses | Action | Retention basis |
| --- | --- | --- | --- | --- |
| diagnostic | True | record-f7dbd7423041, record-5672fd2c2cbd | apply | not_retention |
| control | True | record-8e42e136f9ba | keep | resolved |

## Private material audit

These design labels, counterfactuals and world requirements are evaluator material.
They are never preparation or generation inputs. The true world is distinct from
what the public evidence identifies. Exact world fields are shown with each task.

Registered record counts and construction audit:

```json
{
  "additional_noise_counts": {
    "target_field_preference": 1,
    "technical": 1
  },
  "admissible_count": 3,
  "control_basis": "resolved_keep",
  "current_admissible_count": 3,
  "current_witness_contexts": [
    {
      "account_owner": "Sada",
      "customer_segment": "strategic",
      "task_family": "sales_offer",
      "version": "edition-a0a446a5fef5",
      "workflow": "workflow-bf7741f986ca"
    },
    {
      "account_owner": "Alex",
      "customer_segment": "strategic",
      "task_family": "sales_offer",
      "version": "edition-a0a446a5fef5",
      "workflow": "workflow-bf7741f986ca"
    },
    {
      "account_owner": "Alex",
      "customer_segment": "strategic",
      "task_family": "sales_offer",
      "version": "edition-a0a446a5fef5",
      "workflow": "workflow-bf7741f986ca"
    }
  ],
  "diagnostic_observed": true,
  "material_revision": "v04-amendment-03",
  "record_count": 6,
  "registered_versions": [
    "edition-a0a446a5fef5"
  ],
  "rendering": "interpreted",
  "reversed_option": true,
  "task_type": "observed_change"
}
```

## Single-record counterfactual relevance

Evaluator audit only. Exactly one visible proposed configuration is promoted to a
binding current-version observation at its apparent context. Genuine observations
are retained. An empty compatible set is a contradiction, never an action flip.

Required qualifying outcome for each present type: **contradiction**. All present types qualify: **True**.

Absent types have no fabricated denominator. Technical recovery events are counted
separately in the material audit and are not approval-promotion interventions.

| Manipulated type | Records | Strict action flip | Contradiction | Unchanged | Narrower, same actions | Retention resolved | Unassessable | Qualifying records |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| target_field_preference | 1 | 0 | 1 | 0 | 0 | 0 | 0 | record-3650c6a39b6c |

### Every promoted public record

| Record | Type | Origin | Public option | Remaining policies | Outcome | Qualifies | Diagnostic action | Control action |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| record-3650c6a39b6c | target_field_preference | record-3650c6a39b6c | 1 | 0 | contradiction | True | None | None |

### Exact promotions, contexts and public value provenance

The [complete JSON sidecar](S0-sales.json) preserves every intervention under `counterfactual.records`,
including selected field presence/value, effective current context, public origin,
precise promotion and remaining-policy count. No intervention alters the real history.

## Future tasks for this development example

### diagnostic

Public task

```json
{
  "task_id": "task-11076b4a6e07",
  "context": {
    "task_family": "sales_offer",
    "workflow": "workflow-bf7741f986ca",
    "version": "edition-a0a446a5fef5",
    "account_owner": "Alex",
    "customer_segment": "strategic"
  },
  "facts": {
    "document_id": "DOC-41129",
    "date": "2026-06-15",
    "monthly_unit_price": "50",
    "seats": "10",
    "annual_total": "6000",
    "contract_reference": "OFF-41129",
    "offer_text": "10 seats at EUR 50 per seat per month, billed annually."
  },
  "baseline_fields": [
    {
      "name": "offer_text",
      "value": "10 seats at EUR 50 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-41129"
    },
    {
      "name": "annual_total",
      "value": "6000"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Private expected obligations and actual-world fields

```json
{
  "task_id": "task-11076b4a6e07",
  "history_id": "history-8fc9b7979fc2",
  "probe": "diagnostic",
  "expected_decision": "apply",
  "recoverable": true,
  "world_fields": [
    {
      "name": "offer_text",
      "value": "10 seats at EUR 50 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-41129"
    }
  ]
}
```

### control

Public task

```json
{
  "task_id": "task-2721e632c942",
  "context": {
    "task_family": "sales_offer",
    "workflow": "workflow-bf7741f986ca",
    "version": "edition-a0a446a5fef5",
    "account_owner": "Sada",
    "customer_segment": "strategic"
  },
  "facts": {
    "document_id": "DOC-33307",
    "date": "2026-06-15",
    "monthly_unit_price": "40",
    "seats": "10",
    "annual_total": "4800",
    "contract_reference": "OFF-33307",
    "offer_text": "10 seats at EUR 40 per seat per month, billed annually."
  },
  "baseline_fields": [
    {
      "name": "offer_text",
      "value": "10 seats at EUR 40 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-33307"
    },
    {
      "name": "annual_total",
      "value": "4800"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Private expected obligations and actual-world fields

```json
{
  "task_id": "task-2721e632c942",
  "history_id": "history-8fc9b7979fc2",
  "probe": "control",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "offer_text",
      "value": "10 seats at EUR 40 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-33307"
    },
    {
      "name": "annual_total",
      "value": "4800"
    }
  ]
}
```

## Human response

Pending. No approval is inferred from this export.
