# S1 / sales

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
| diagnostic | task_family=sales_offer, workflow=workflow-09625e499abc, version=edition-7815519526e8, account_owner=Leon, customer_segment=strategic | False | keep | unresolved |
| control | task_family=sales_offer, workflow=workflow-09625e499abc, version=edition-7815519526e8, account_owner=Sada, customer_segment=standard | False | keep | unresolved |

Counterfactual qualification requires **action_flip** for every present type. All present types qualify: **True**.

One qualifying example per present type is shown below. The links lead to its
public evidence; all records and counts appear in the later audit and JSON sidecar.

| Type (record count) | Promoted record / source | Public target value | Exact promotion | Outcome / remaining policies |
| --- | --- | --- | --- | --- |
| target_field_preference (1) | [record-6f418baccd85](#record-6f418baccd85) | annual_total = '6000' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=sales_offer, workflow=workflow-09625e499abc, version=edition-7815519526e8, account_owner=Leon, customer_segment=strategic | action_flip / 2 |

An action flip requires a nonempty compatible set and a changed diagnostic or control
action. A contradiction has no compatible policy and supplies neither task action.

[Complete oracle derivation](#oracle-derivation-from-public-evidence) · [Every counterfactual record](#single-record-counterfactual-relevance)

## Public configuration and assumptions

```json
{
  "as_of": "2026-06-15T12:00:00Z",
  "baseline_template": {
    "contract_reference": "{contract_reference}",
    "offer_text": "{offer_text}"
  },
  "dimensions": {
    "account_owner": [
      "Leon",
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
    "operation": "set_fact",
    "separator": "",
    "value": "annual_total"
  },
  "hypothesis_class": "h14",
  "hypothesis_definition": "Each of the two declared binary context dimensions defines a predicate testing its second listed value. Call these predicates x and y. In each registered version the target field configuration is one Boolean function from the following class: constant 0 or 1; x, not x, y, or not y; a conjunction of one literal from each dimension; or a disjunction of one literal from each dimension. Zero selects the configured baseline and one the available alternative. The fourteen distinct truth tables exclude only XOR and XNOR. Each version has its own class member, with no cross-version coupling. This restriction is a supplied synthetic assumption, not an established property of enterprise work.",
  "task_family": "sales_offer",
  "workflow": "workflow-09625e499abc"
}
```

This is a bounded synthetic workflow model. initial_configuration declares the field options, two context dimensions and the complete H14 hypothesis class. Each registered version has one class member. A field observation constrains the member indexed by its recorded version. Broader consequences follow from the declared class. Facts provide current artifact values. Other fields retain their configured baseline. Outside the declared task_family and workflow, or without a complete declared context, no update is authorised by this model. A register_version event supplies trusted workflow metadata with the authority roster and half-open validity interval. Binding field approval is an event of type review with decision accept, performed by a listed reviewer within that interval, with the field included in reviewed_fields. Its accepted artifact establishes the field configuration at the recorded context. This explicit approval convention is a supplied synthetic assumption. A forward has an origin_ref identifying the record whose content it reproduces. Raw artifacts expose named revisions and a selected artifact reference; interpreted records expose the selected fields directly. A rejection records a whole-artifact decision and its stated grounds. An artifact field whose review is not recorded has no approved assignment. The configured baseline is retained when the available evidence does not establish an update. Dates and version labels in new work identify the applicable registration.

## Public work records

### record-9010b1034fc7

2026-05-31T15:39:48Z | review | Anika

Context: task_family=sales_offer, workflow=workflow-09625e499abc, version=edition-7815519526e8, account_owner=Sada, customer_segment=strategic

- decision: accept
- reviewed_fields: ['annual_total']
- authority_ref: record-dab7efffdfcd
- accepted_artifact: replacement
- comment: Approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "annual_total": "9000",
        "contract_reference": "OFF-86636",
        "offer_text": "15 seats at EUR 50 per seat per month, billed annually."
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "contract_reference": "OFF-86636",
        "offer_text": "15 seats at EUR 50 per seat per month, billed annually."
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-dab7efffdfcd",
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-86636",
  "event": "review",
  "facts": {
    "annual_total": "9000",
    "contract_reference": "OFF-86636",
    "date": "2026-05-31",
    "document_id": "DOC-86636",
    "monthly_unit_price": "50",
    "offer_text": "15 seats at EUR 50 per seat per month, billed annually.",
    "seats": "15"
  },
  "format": "raw",
  "reviewed_fields": [
    "annual_total"
  ]
}
```

### record-c0c3ff0dfe8a

2026-06-07T17:20:44Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-09625e499abc, version=edition-7815519526e8, account_owner=Leon, customer_segment=standard


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
  "request_id": "request-8b7f8298f09b"
}
```

### record-240500dffd85

2026-05-29T10:27:47Z | review | Theo

Context: task_family=sales_offer, workflow=workflow-09625e499abc, version=edition-7815519526e8, account_owner=Leon, customer_segment=standard

- decision: accept
- reviewed_fields: ['annual_total']
- authority_ref: record-dab7efffdfcd
- accepted_artifact: replacement
- comment: Review complete.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "contract_reference": "OFF-35309",
        "offer_text": "5 seats at EUR 40 per seat per month, billed annually."
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "annual_total": "2400",
        "contract_reference": "OFF-35309",
        "offer_text": "5 seats at EUR 40 per seat per month, billed annually."
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-dab7efffdfcd",
  "comment": "Review complete.",
  "decision": "accept",
  "document_id": "DOC-35309",
  "event": "review",
  "facts": {
    "annual_total": "2400",
    "contract_reference": "OFF-35309",
    "date": "2026-05-29",
    "document_id": "DOC-35309",
    "monthly_unit_price": "40",
    "offer_text": "5 seats at EUR 40 per seat per month, billed annually.",
    "seats": "5"
  },
  "format": "raw",
  "reviewed_fields": [
    "annual_total"
  ]
}
```

### record-dab7efffdfcd

2026-01-01T00:00:00Z | template | workflow-registry

Context: 


```json
{
  "authorised_reviewers": [
    "Anika",
    "Theo"
  ],
  "event": "register_version",
  "supersedes": null,
  "task_family": "sales_offer",
  "valid_from": "2026-01-01T00:00:00Z",
  "valid_until": "2027-01-01T00:00:00Z",
  "version": "edition-7815519526e8",
  "workflow": "workflow-09625e499abc"
}
```

### record-6f418baccd85

2026-06-07T15:24:04Z | revision | Anika

Context: task_family=sales_offer, workflow=workflow-09625e499abc, version=edition-7815519526e8, account_owner=Leon, customer_segment=strategic


```json
{
  "event": "preference",
  "facts": {
    "annual_total": "6000",
    "contract_reference": "OFF-90013",
    "date": "2026-06-07",
    "document_id": "DOC-90013",
    "monthly_unit_price": "50",
    "offer_text": "10 seats at EUR 50 per seat per month, billed annually.",
    "seats": "10"
  },
  "message": "I would prefer annual_total set to '6000' for this item.",
  "proposed_fields": {
    "annual_total": "6000",
    "contract_reference": "OFF-90013",
    "offer_text": "10 seats at EUR 50 per seat per month, billed annually."
  }
}
```

### record-bc88934a58ae

2026-06-07T17:38:47Z | review | Anika

Context: task_family=sales_offer, workflow=workflow-09625e499abc, version=edition-7815519526e8, account_owner=Sada, customer_segment=strategic

- decision: accept
- reviewed_fields: ['annual_total']
- authority_ref: record-dab7efffdfcd
- accepted_artifact: replacement
- comment: Completed.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "annual_total": "9600",
        "contract_reference": "OFF-38222",
        "offer_text": "20 seats at EUR 40 per seat per month, billed annually."
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "contract_reference": "OFF-38222",
        "offer_text": "20 seats at EUR 40 per seat per month, billed annually."
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-dab7efffdfcd",
  "comment": "Completed.",
  "decision": "accept",
  "document_id": "DOC-38222",
  "event": "review",
  "facts": {
    "annual_total": "9600",
    "contract_reference": "OFF-38222",
    "date": "2026-06-07",
    "document_id": "DOC-38222",
    "monthly_unit_price": "40",
    "offer_text": "20 seats at EUR 40 per seat per month, billed annually.",
    "seats": "20"
  },
  "format": "raw",
  "reviewed_fields": [
    "annual_total"
  ]
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
| record-9010b1034fc7 | edition-7815519526e8 | task_family=sales_offer, workflow=workflow-09625e499abc, version=edition-7815519526e8, account_owner=Sada, customer_segment=strategic | 0 |
| record-240500dffd85 | edition-7815519526e8 | task_family=sales_offer, workflow=workflow-09625e499abc, version=edition-7815519526e8, account_owner=Leon, customer_segment=standard | 1 |
| record-bc88934a58ae | edition-7815519526e8 | task_family=sales_offer, workflow=workflow-09625e499abc, version=edition-7815519526e8, account_owner=Sada, customer_segment=strategic | 0 |

### Competing requirement explanations

Zero is the configured baseline; one is the alternative. Each row is a distinct
compatible function for this version. No preference for simplicity removes a row.
The private sampling plan and world policy do not filter these explanations.

Version edition-7815519526e8: 4 compatible functions.

| Function | account_owner=Leon, customer_segment=standard | account_owner=Leon, customer_segment=strategic | account_owner=Sada, customer_segment=standard | account_owner=Sada, customer_segment=strategic | Complexity |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 1 | 0 | 0 | 0 | 2 |
| 2 | 1 | 0 | 1 | 0 | 1 |
| 3 | 1 | 1 | 0 | 0 | 1 |
| 4 | 1 | 1 | 1 | 0 | 2 |

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
    "target_field_preference": 1,
    "technical": 1
  },
  "admissible_count": 4,
  "control_basis": "unidentifiable_baseline_world",
  "current_admissible_count": 4,
  "current_witness_contexts": [
    {
      "account_owner": "Sada",
      "customer_segment": "strategic",
      "task_family": "sales_offer",
      "version": "edition-7815519526e8",
      "workflow": "workflow-09625e499abc"
    },
    {
      "account_owner": "Leon",
      "customer_segment": "standard",
      "task_family": "sales_offer",
      "version": "edition-7815519526e8",
      "workflow": "workflow-09625e499abc"
    },
    {
      "account_owner": "Sada",
      "customer_segment": "strategic",
      "task_family": "sales_offer",
      "version": "edition-7815519526e8",
      "workflow": "workflow-09625e499abc"
    }
  ],
  "diagnostic_observed": false,
  "material_revision": "v04-amendment-03-r2",
  "record_count": 6,
  "registered_versions": [
    "edition-7815519526e8"
  ],
  "rendering": "raw",
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
| target_field_preference | 1 | 1 | 0 | 0 | 0 | 0 | 0 | record-6f418baccd85 |

### Every promoted public record

| Record | Type | Origin | Public option | Remaining policies | Outcome | Qualifies | Diagnostic action | Control action |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| record-6f418baccd85 | target_field_preference | record-6f418baccd85 | 1 | 2 | action_flip | True | apply | keep |

### Exact promotions, contexts and public value provenance

The [complete JSON sidecar](S1-sales.json) preserves every intervention under `counterfactual.records`,
including selected field presence/value, effective current context, public origin,
precise promotion and remaining-policy count. No intervention alters the real history.

## Future tasks for this development example

### diagnostic

Public task

```json
{
  "task_id": "task-792932c6a78e",
  "context": {
    "task_family": "sales_offer",
    "workflow": "workflow-09625e499abc",
    "version": "edition-7815519526e8",
    "account_owner": "Leon",
    "customer_segment": "strategic"
  },
  "facts": {
    "document_id": "DOC-38125",
    "date": "2026-06-15",
    "monthly_unit_price": "65",
    "seats": "5",
    "annual_total": "3900",
    "contract_reference": "OFF-38125",
    "offer_text": "5 seats at EUR 65 per seat per month, billed annually."
  },
  "baseline_fields": [
    {
      "name": "offer_text",
      "value": "5 seats at EUR 65 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-38125"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Private expected obligations and actual-world fields

```json
{
  "task_id": "task-792932c6a78e",
  "history_id": "history-b9e284e0f723",
  "probe": "diagnostic",
  "expected_decision": "keep",
  "recoverable": false,
  "world_fields": [
    {
      "name": "offer_text",
      "value": "5 seats at EUR 65 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-38125"
    },
    {
      "name": "annual_total",
      "value": "3900"
    }
  ]
}
```

### control

Public task

```json
{
  "task_id": "task-230a06fb0bcb",
  "context": {
    "task_family": "sales_offer",
    "workflow": "workflow-09625e499abc",
    "version": "edition-7815519526e8",
    "account_owner": "Sada",
    "customer_segment": "standard"
  },
  "facts": {
    "document_id": "DOC-29190",
    "date": "2026-06-15",
    "monthly_unit_price": "65",
    "seats": "10",
    "annual_total": "7800",
    "contract_reference": "OFF-29190",
    "offer_text": "10 seats at EUR 65 per seat per month, billed annually."
  },
  "baseline_fields": [
    {
      "name": "offer_text",
      "value": "10 seats at EUR 65 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-29190"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Private expected obligations and actual-world fields

```json
{
  "task_id": "task-230a06fb0bcb",
  "history_id": "history-b9e284e0f723",
  "probe": "control",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "offer_text",
      "value": "10 seats at EUR 65 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-29190"
    }
  ]
}
```

## Human response

Pending. No approval is inferred from this export.
