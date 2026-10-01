# S0 / sales

Material revision: v04-amendment-03-r2. Synthetic development example.

[Frozen surface-selector audit](surface-audit.md) · [Complete audit JSON](surface-audit.json).
Its per-history results use this case’s history ID; selector choice used only separate development histories.

Registered task type: **observed_change**. Intended diagnostic regime: **change**.
Public records: 6. Control basis: resolved_keep.

## Review summary

Current compatible functions: **3**. Full cross-version policies: 3.

H14 identification is conditional on excluding XOR and XNOR. Retaining an unresolved
baseline does not establish that the baseline is the true requirement.

| Task | Public context | Previously observed | Warranted action | Retention basis |
| --- | --- | --- | --- | --- |
| diagnostic | task_family=sales_offer, workflow=workflow-13e78ea66a96, version=edition-b47d936dcd38, account_owner=Sada, customer_segment=strategic | True | apply | not_retention |
| control | task_family=sales_offer, workflow=workflow-13e78ea66a96, version=edition-b47d936dcd38, account_owner=Sada, customer_segment=standard | True | keep | resolved |

Counterfactual qualification requires **contradiction** for every present type. All present types qualify: **True**.

One qualifying example per present type is shown below. The links lead to its
public evidence; all records and counts appear in the later audit and JSON sidecar.

| Type (record count) | Promoted record / source | Public target value | Exact promotion | Outcome / remaining policies |
| --- | --- | --- | --- | --- |
| target_field_preference (1) | [record-829be85abd49](#record-829be85abd49) | annual_total = '9600' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=sales_offer, workflow=workflow-13e78ea66a96, version=edition-b47d936dcd38, account_owner=Sada, customer_segment=strategic | contradiction / 0 |

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
      "Sada",
      "Leon"
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
  "workflow": "workflow-13e78ea66a96"
}
```

This is a bounded synthetic workflow model. initial_configuration declares the field options, two context dimensions and the complete H14 hypothesis class. Each registered version has one class member. A field observation constrains the member indexed by its recorded version. Broader consequences follow from the declared class. Facts provide current artifact values. Other fields retain their configured baseline. Outside the declared task_family and workflow, or without a complete declared context, no update is authorised by this model. A register_version event supplies trusted workflow metadata with the authority roster and half-open validity interval. Binding field approval is an event of type review with decision accept, performed by a listed reviewer within that interval, with the field included in reviewed_fields. Its accepted artifact establishes the field configuration at the recorded context. This explicit approval convention is a supplied synthetic assumption. A forward has an origin_ref identifying the record whose content it reproduces. Raw artifacts expose named revisions and a selected artifact reference; interpreted records expose the selected fields directly. A rejection records a whole-artifact decision and its stated grounds. An artifact field whose review is not recorded has no approved assignment. The configured baseline is retained when the available evidence does not establish an update. Dates and version labels in new work identify the applicable registration.

## Public work records

### record-875b46b4817e

2026-05-31T16:57:39Z | review | Robin

Context: task_family=sales_offer, workflow=workflow-13e78ea66a96, version=edition-b47d936dcd38, account_owner=Sada, customer_segment=strategic

- decision: accept
- reviewed_fields: ['annual_total']
- authority_ref: record-b15333e312f5
- comment: Checked.

```json
{
  "accepted_fields": {
    "contract_reference": "OFF-14525",
    "offer_text": "5 seats at EUR 25 per seat per month, billed annually."
  },
  "authority_ref": "record-b15333e312f5",
  "change_summary": {
    "after": null,
    "before": "1500",
    "field": "annual_total"
  },
  "comment": "Checked.",
  "decision": "accept",
  "document_id": "DOC-14525",
  "event": "review",
  "facts": {
    "annual_total": "1500",
    "contract_reference": "OFF-14525",
    "date": "2026-05-31",
    "document_id": "DOC-14525",
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

### record-829be85abd49

2026-05-18T08:11:03Z | revision | Jonas

Context: task_family=sales_offer, workflow=workflow-13e78ea66a96, version=edition-b47d936dcd38, account_owner=Sada, customer_segment=strategic


```json
{
  "event": "preference",
  "facts": {
    "annual_total": "9600",
    "contract_reference": "OFF-15350",
    "date": "2026-05-18",
    "document_id": "DOC-15350",
    "monthly_unit_price": "40",
    "offer_text": "20 seats at EUR 40 per seat per month, billed annually.",
    "seats": "20"
  },
  "message": "I would prefer annual_total set to '9600' for this item.",
  "proposed_fields": {
    "annual_total": "9600",
    "contract_reference": "OFF-15350",
    "offer_text": "20 seats at EUR 40 per seat per month, billed annually."
  }
}
```

### record-b08f2a04b62e

2026-05-18T15:45:29Z | review | Theo

Context: task_family=sales_offer, workflow=workflow-13e78ea66a96, version=edition-b47d936dcd38, account_owner=Sada, customer_segment=strategic

- decision: accept
- reviewed_fields: ['annual_total']
- authority_ref: record-b15333e312f5
- comment: Review complete.

```json
{
  "accepted_fields": {
    "contract_reference": "OFF-90580",
    "offer_text": "5 seats at EUR 25 per seat per month, billed annually."
  },
  "authority_ref": "record-b15333e312f5",
  "change_summary": {
    "after": null,
    "before": "1500",
    "field": "annual_total"
  },
  "comment": "Review complete.",
  "decision": "accept",
  "document_id": "DOC-90580",
  "event": "review",
  "facts": {
    "annual_total": "1500",
    "contract_reference": "OFF-90580",
    "date": "2026-05-18",
    "document_id": "DOC-90580",
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

### record-b15333e312f5

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
  "task_family": "sales_offer",
  "valid_from": "2026-01-01T00:00:00Z",
  "valid_until": "2027-01-01T00:00:00Z",
  "version": "edition-b47d936dcd38",
  "workflow": "workflow-13e78ea66a96"
}
```

### record-87a2457cd883

2026-06-10T10:53:10Z | review | Theo

Context: task_family=sales_offer, workflow=workflow-13e78ea66a96, version=edition-b47d936dcd38, account_owner=Sada, customer_segment=standard

- decision: accept
- reviewed_fields: ['annual_total']
- authority_ref: record-b15333e312f5
- comment: Approved.

```json
{
  "accepted_fields": {
    "annual_total": "6000",
    "contract_reference": "OFF-85155",
    "offer_text": "20 seats at EUR 25 per seat per month, billed annually."
  },
  "authority_ref": "record-b15333e312f5",
  "change_summary": {
    "after": "6000",
    "before": null,
    "field": "annual_total"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-85155",
  "event": "review",
  "facts": {
    "annual_total": "6000",
    "contract_reference": "OFF-85155",
    "date": "2026-06-10",
    "document_id": "DOC-85155",
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

### record-2cd339b6af54

2026-05-31T15:59:27Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-13e78ea66a96, version=edition-b47d936dcd38, account_owner=Sada, customer_segment=strategic


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
  "log": "The first attempt failed; the next attempt completed.",
  "request_id": "request-d8f20c0a34ed"
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
| record-875b46b4817e | edition-b47d936dcd38 | task_family=sales_offer, workflow=workflow-13e78ea66a96, version=edition-b47d936dcd38, account_owner=Sada, customer_segment=strategic | 1 |
| record-b08f2a04b62e | edition-b47d936dcd38 | task_family=sales_offer, workflow=workflow-13e78ea66a96, version=edition-b47d936dcd38, account_owner=Sada, customer_segment=strategic | 1 |
| record-87a2457cd883 | edition-b47d936dcd38 | task_family=sales_offer, workflow=workflow-13e78ea66a96, version=edition-b47d936dcd38, account_owner=Sada, customer_segment=standard | 0 |

### Competing requirement explanations

Zero is the configured baseline; one is the alternative. Each row is a distinct
compatible function for this version. No preference for simplicity removes a row.
The private sampling plan and world policy do not filter these explanations.

Version edition-b47d936dcd38: 3 compatible functions.

| Function | account_owner=Sada, customer_segment=standard | account_owner=Sada, customer_segment=strategic | account_owner=Leon, customer_segment=standard | account_owner=Leon, customer_segment=strategic | Complexity |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | 1 | 0 | 0 | 2 |
| 2 | 0 | 1 | 0 | 1 | 1 |
| 3 | 0 | 1 | 1 | 1 | 2 |

### Diagnostic and control derivations

| Task | Context observed | Witnesses | Action | Retention basis |
| --- | --- | --- | --- | --- |
| diagnostic | True | record-875b46b4817e, record-b08f2a04b62e | apply | not_retention |
| control | True | record-87a2457cd883 | keep | resolved |

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
      "customer_segment": "standard",
      "task_family": "sales_offer",
      "version": "edition-b47d936dcd38",
      "workflow": "workflow-13e78ea66a96"
    },
    {
      "account_owner": "Sada",
      "customer_segment": "strategic",
      "task_family": "sales_offer",
      "version": "edition-b47d936dcd38",
      "workflow": "workflow-13e78ea66a96"
    },
    {
      "account_owner": "Sada",
      "customer_segment": "strategic",
      "task_family": "sales_offer",
      "version": "edition-b47d936dcd38",
      "workflow": "workflow-13e78ea66a96"
    }
  ],
  "diagnostic_observed": true,
  "material_revision": "v04-amendment-03-r2",
  "record_count": 6,
  "registered_versions": [
    "edition-b47d936dcd38"
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
| target_field_preference | 1 | 0 | 1 | 0 | 0 | 0 | 0 | record-829be85abd49 |

### Every promoted public record

| Record | Type | Origin | Public option | Remaining policies | Outcome | Qualifies | Diagnostic action | Control action |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| record-829be85abd49 | target_field_preference | record-829be85abd49 | 0 | 0 | contradiction | True | None | None |

### Exact promotions, contexts and public value provenance

The [complete JSON sidecar](S0-sales.json) preserves every intervention under `counterfactual.records`,
including selected field presence/value, effective current context, public origin,
precise promotion and remaining-policy count. No intervention alters the real history.

## Future tasks for this development example

### diagnostic

Public task

```json
{
  "task_id": "task-0dccb5cd3ff4",
  "context": {
    "task_family": "sales_offer",
    "workflow": "workflow-13e78ea66a96",
    "version": "edition-b47d936dcd38",
    "account_owner": "Sada",
    "customer_segment": "strategic"
  },
  "facts": {
    "document_id": "DOC-48541",
    "date": "2026-06-15",
    "monthly_unit_price": "50",
    "seats": "15",
    "annual_total": "9000",
    "contract_reference": "OFF-48541",
    "offer_text": "15 seats at EUR 50 per seat per month, billed annually."
  },
  "baseline_fields": [
    {
      "name": "offer_text",
      "value": "15 seats at EUR 50 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-48541"
    },
    {
      "name": "annual_total",
      "value": "9000"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Private expected obligations and actual-world fields

```json
{
  "task_id": "task-0dccb5cd3ff4",
  "history_id": "history-dd60612b6ea2",
  "probe": "diagnostic",
  "expected_decision": "apply",
  "recoverable": true,
  "world_fields": [
    {
      "name": "offer_text",
      "value": "15 seats at EUR 50 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-48541"
    }
  ]
}
```

### control

Public task

```json
{
  "task_id": "task-6e1f4cccf5c4",
  "context": {
    "task_family": "sales_offer",
    "workflow": "workflow-13e78ea66a96",
    "version": "edition-b47d936dcd38",
    "account_owner": "Sada",
    "customer_segment": "standard"
  },
  "facts": {
    "document_id": "DOC-74952",
    "date": "2026-06-15",
    "monthly_unit_price": "65",
    "seats": "20",
    "annual_total": "15600",
    "contract_reference": "OFF-74952",
    "offer_text": "20 seats at EUR 65 per seat per month, billed annually."
  },
  "baseline_fields": [
    {
      "name": "offer_text",
      "value": "20 seats at EUR 65 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-74952"
    },
    {
      "name": "annual_total",
      "value": "15600"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Private expected obligations and actual-world fields

```json
{
  "task_id": "task-6e1f4cccf5c4",
  "history_id": "history-dd60612b6ea2",
  "probe": "control",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "offer_text",
      "value": "20 seats at EUR 65 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-74952"
    },
    {
      "name": "annual_total",
      "value": "15600"
    }
  ]
}
```

## Human response

Pending. No approval is inferred from this export.
