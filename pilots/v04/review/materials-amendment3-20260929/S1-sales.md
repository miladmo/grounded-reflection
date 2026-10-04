# S1 / sales

Material revision: v04-amendment-03. Synthetic development example.

Registered task type: **unidentifiable**. Intended diagnostic regime: **unidentifiable**.
Public records: 6. Control basis: unidentifiable_baseline_world.

## Review summary

Current compatible functions: **4**. Full cross-version policies: 4.

H14 identification is conditional on excluding XOR and XNOR. Retaining an unresolved
baseline does not establish that the baseline is the true requirement.

| Task | Public context | Previously observed | Warranted action | Retention basis |
| --- | --- | --- | --- | --- |
| diagnostic | task_family=sales_offer, workflow=workflow-d99c667f7f5c, version=edition-cc2ea8106d6a, account_owner=Alex, customer_segment=strategic | False | keep | unresolved |
| control | task_family=sales_offer, workflow=workflow-d99c667f7f5c, version=edition-cc2ea8106d6a, account_owner=Sada, customer_segment=standard | False | keep | unresolved |

Counterfactual qualification requires **action_flip** for every present type. All present types qualify: **True**.

One qualifying example per present type is shown below. The links lead to its
public evidence; all records and counts appear in the later audit and JSON sidecar.

| Type (record count) | Promoted record / source | Public target value | Exact promotion | Outcome / remaining policies |
| --- | --- | --- | --- | --- |
| target_field_preference (1) | [record-96b5f728fbd8](#record-96b5f728fbd8) | annual_total = '9600' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=sales_offer, workflow=workflow-d99c667f7f5c, version=edition-cc2ea8106d6a, account_owner=Alex, customer_segment=strategic | action_flip / 2 |

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
      "Sada",
      "Alex"
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
  "workflow": "workflow-d99c667f7f5c"
}
```

This is a bounded synthetic workflow model. initial_configuration declares the field options, two context dimensions and the complete H14 hypothesis class. Each registered version has one class member. A field observation constrains the member indexed by its recorded version. Broader consequences follow from the declared class. Facts provide current artifact values. Other fields retain their configured baseline. Outside the declared task_family and workflow, or without a complete declared context, no update is authorised by this model. A register_version event supplies trusted workflow metadata with the authority roster and half-open validity interval. Binding field approval is an event of type review with decision accept, performed by a listed reviewer within that interval, with the field included in reviewed_fields. Its accepted artifact establishes the field configuration at the recorded context. This explicit approval convention is a supplied synthetic assumption. A forward has an origin_ref identifying the record whose content it reproduces. Raw artifacts expose named revisions and a selected artifact reference; interpreted records expose the selected fields directly. A rejection records a whole-artifact decision and its stated grounds. An artifact field whose review is not recorded has no approved assignment. The configured baseline is retained when the available evidence does not establish an update. Dates and version labels in new work identify the applicable registration.

## Public work records

### record-3d92ccfd6f36

2026-01-01T00:00:00Z | template | workflow-registry

Context: 


```json
{
  "authorised_reviewers": [
    "Robin",
    "Anika"
  ],
  "event": "register_version",
  "supersedes": null,
  "task_family": "sales_offer",
  "valid_from": "2026-01-01T00:00:00Z",
  "valid_until": "2027-01-01T00:00:00Z",
  "version": "edition-cc2ea8106d6a",
  "workflow": "workflow-d99c667f7f5c"
}
```

### record-071e20552a66

2026-06-10T10:00:00Z | review | Robin

Context: task_family=sales_offer, workflow=workflow-d99c667f7f5c, version=edition-cc2ea8106d6a, account_owner=Alex, customer_segment=standard

- decision: accept
- reviewed_fields: ['annual_total']
- authority_ref: record-3d92ccfd6f36
- accepted_artifact: replacement
- comment: Approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "annual_total": "7800",
        "contract_reference": "OFF-86696",
        "offer_text": "10 seats at EUR 65 per seat per month, billed annually."
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "contract_reference": "OFF-86696",
        "offer_text": "10 seats at EUR 65 per seat per month, billed annually."
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-3d92ccfd6f36",
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-86696",
  "event": "review",
  "facts": {
    "annual_total": "7800",
    "contract_reference": "OFF-86696",
    "date": "2026-06-10",
    "document_id": "DOC-86696",
    "monthly_unit_price": "65",
    "offer_text": "10 seats at EUR 65 per seat per month, billed annually.",
    "seats": "10"
  },
  "format": "raw",
  "reviewed_fields": [
    "annual_total"
  ]
}
```

### record-40ac9bb968a7

2026-06-11T10:00:00Z | review | Anika

Context: task_family=sales_offer, workflow=workflow-d99c667f7f5c, version=edition-cc2ea8106d6a, account_owner=Sada, customer_segment=strategic

- decision: accept
- reviewed_fields: ['annual_total']
- authority_ref: record-3d92ccfd6f36
- accepted_artifact: replacement
- comment: Approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "contract_reference": "OFF-25771",
        "offer_text": "15 seats at EUR 50 per seat per month, billed annually."
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "annual_total": "9000",
        "contract_reference": "OFF-25771",
        "offer_text": "15 seats at EUR 50 per seat per month, billed annually."
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-3d92ccfd6f36",
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-25771",
  "event": "review",
  "facts": {
    "annual_total": "9000",
    "contract_reference": "OFF-25771",
    "date": "2026-06-11",
    "document_id": "DOC-25771",
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

### record-2a2f38a7a419

2026-06-12T10:00:00Z | review | Robin

Context: task_family=sales_offer, workflow=workflow-d99c667f7f5c, version=edition-cc2ea8106d6a, account_owner=Alex, customer_segment=standard

- decision: accept
- reviewed_fields: ['annual_total']
- authority_ref: record-3d92ccfd6f36
- accepted_artifact: replacement
- comment: Approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "annual_total": "12000",
        "contract_reference": "OFF-81798",
        "offer_text": "20 seats at EUR 50 per seat per month, billed annually."
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "contract_reference": "OFF-81798",
        "offer_text": "20 seats at EUR 50 per seat per month, billed annually."
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-3d92ccfd6f36",
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-81798",
  "event": "review",
  "facts": {
    "annual_total": "12000",
    "contract_reference": "OFF-81798",
    "date": "2026-06-12",
    "document_id": "DOC-81798",
    "monthly_unit_price": "50",
    "offer_text": "20 seats at EUR 50 per seat per month, billed annually.",
    "seats": "20"
  },
  "format": "raw",
  "reviewed_fields": [
    "annual_total"
  ]
}
```

### record-39806d4e588b

2026-06-14T08:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-d99c667f7f5c, version=edition-cc2ea8106d6a, account_owner=Sada, customer_segment=standard


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
  "request_id": "request-4e532ce8bfc5"
}
```

### record-96b5f728fbd8

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=sales_offer, workflow=workflow-d99c667f7f5c, version=edition-cc2ea8106d6a, account_owner=Alex, customer_segment=strategic


```json
{
  "event": "preference",
  "facts": {
    "annual_total": "9600",
    "contract_reference": "OFF-33256",
    "date": "2026-06-14",
    "document_id": "DOC-33256",
    "monthly_unit_price": "40",
    "offer_text": "20 seats at EUR 40 per seat per month, billed annually.",
    "seats": "20"
  },
  "message": "My preference for this work item is that annual_total should be '9600'.",
  "proposed_fields": {
    "annual_total": "9600",
    "contract_reference": "OFF-33256",
    "offer_text": "20 seats at EUR 40 per seat per month, billed annually."
  }
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
| record-071e20552a66 | edition-cc2ea8106d6a | task_family=sales_offer, workflow=workflow-d99c667f7f5c, version=edition-cc2ea8106d6a, account_owner=Alex, customer_segment=standard | 0 |
| record-40ac9bb968a7 | edition-cc2ea8106d6a | task_family=sales_offer, workflow=workflow-d99c667f7f5c, version=edition-cc2ea8106d6a, account_owner=Sada, customer_segment=strategic | 1 |
| record-2a2f38a7a419 | edition-cc2ea8106d6a | task_family=sales_offer, workflow=workflow-d99c667f7f5c, version=edition-cc2ea8106d6a, account_owner=Alex, customer_segment=standard | 0 |

### Competing requirement explanations

Zero is the configured baseline; one is the alternative. Each row is a distinct
compatible function for this version. No preference for simplicity removes a row.
The private sampling plan and world policy do not filter these explanations.

Version edition-cc2ea8106d6a: 4 compatible functions.

| Function | account_owner=Sada, customer_segment=standard | account_owner=Sada, customer_segment=strategic | account_owner=Alex, customer_segment=standard | account_owner=Alex, customer_segment=strategic | Complexity |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | 1 | 0 | 0 | 2 |
| 2 | 0 | 1 | 0 | 1 | 1 |
| 3 | 1 | 1 | 0 | 0 | 1 |
| 4 | 1 | 1 | 0 | 1 | 2 |

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
      "account_owner": "Alex",
      "customer_segment": "standard",
      "task_family": "sales_offer",
      "version": "edition-cc2ea8106d6a",
      "workflow": "workflow-d99c667f7f5c"
    },
    {
      "account_owner": "Sada",
      "customer_segment": "strategic",
      "task_family": "sales_offer",
      "version": "edition-cc2ea8106d6a",
      "workflow": "workflow-d99c667f7f5c"
    },
    {
      "account_owner": "Alex",
      "customer_segment": "standard",
      "task_family": "sales_offer",
      "version": "edition-cc2ea8106d6a",
      "workflow": "workflow-d99c667f7f5c"
    }
  ],
  "diagnostic_observed": false,
  "material_revision": "v04-amendment-03",
  "record_count": 6,
  "registered_versions": [
    "edition-cc2ea8106d6a"
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
| target_field_preference | 1 | 1 | 0 | 0 | 0 | 0 | 0 | record-96b5f728fbd8 |

### Every promoted public record

| Record | Type | Origin | Public option | Remaining policies | Outcome | Qualifies | Diagnostic action | Control action |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| record-96b5f728fbd8 | target_field_preference | record-96b5f728fbd8 | 1 | 2 | action_flip | True | apply | keep |

### Exact promotions, contexts and public value provenance

The [complete JSON sidecar](S1-sales.json) preserves every intervention under `counterfactual.records`,
including selected field presence/value, effective current context, public origin,
precise promotion and remaining-policy count. No intervention alters the real history.

## Future tasks for this development example

### diagnostic

Public task

```json
{
  "task_id": "task-106faf2706d1",
  "context": {
    "task_family": "sales_offer",
    "workflow": "workflow-d99c667f7f5c",
    "version": "edition-cc2ea8106d6a",
    "account_owner": "Alex",
    "customer_segment": "strategic"
  },
  "facts": {
    "document_id": "DOC-14105",
    "date": "2026-06-15",
    "monthly_unit_price": "50",
    "seats": "15",
    "annual_total": "9000",
    "contract_reference": "OFF-14105",
    "offer_text": "15 seats at EUR 50 per seat per month, billed annually."
  },
  "baseline_fields": [
    {
      "name": "offer_text",
      "value": "15 seats at EUR 50 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-14105"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Private expected obligations and actual-world fields

```json
{
  "task_id": "task-106faf2706d1",
  "history_id": "history-df3e3de1a862",
  "probe": "diagnostic",
  "expected_decision": "keep",
  "recoverable": false,
  "world_fields": [
    {
      "name": "offer_text",
      "value": "15 seats at EUR 50 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-14105"
    },
    {
      "name": "annual_total",
      "value": "9000"
    }
  ]
}
```

### control

Public task

```json
{
  "task_id": "task-8fc22ff5fca7",
  "context": {
    "task_family": "sales_offer",
    "workflow": "workflow-d99c667f7f5c",
    "version": "edition-cc2ea8106d6a",
    "account_owner": "Sada",
    "customer_segment": "standard"
  },
  "facts": {
    "document_id": "DOC-12929",
    "date": "2026-06-15",
    "monthly_unit_price": "25",
    "seats": "20",
    "annual_total": "6000",
    "contract_reference": "OFF-12929",
    "offer_text": "20 seats at EUR 25 per seat per month, billed annually."
  },
  "baseline_fields": [
    {
      "name": "offer_text",
      "value": "20 seats at EUR 25 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-12929"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Private expected obligations and actual-world fields

```json
{
  "task_id": "task-8fc22ff5fca7",
  "history_id": "history-df3e3de1a862",
  "probe": "control",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "offer_text",
      "value": "20 seats at EUR 25 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-12929"
    }
  ]
}
```

## Human response

Pending. No approval is inferred from this export.
