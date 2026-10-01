# S2 / reporting

Material revision: v04-amendment-03-r2. Synthetic development example.

[Frozen surface-selector audit](surface-audit.md) · [Complete audit JSON](surface-audit.json).
Its per-history results use this case’s history ID; selector choice used only separate development histories.

Registered task type: **transfer_change**. Intended diagnostic regime: **change**.
Public records: 60. Control basis: resolved_keep.

## Review summary

Current compatible functions: **1**. Full cross-version policies: 1.

H14 identification is conditional on excluding XOR and XNOR. Retaining an unresolved
baseline does not establish that the baseline is the true requirement.

| Task | Public context | Previously observed | Warranted action | Retention basis |
| --- | --- | --- | --- | --- |
| diagnostic | task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=external | False | apply | not_retention |
| control | task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal | True | keep | resolved |

Counterfactual qualification requires **contradiction** for every present type. All present types qualify: **True**.

One qualifying example per present type is shown below. The links lead to its
public evidence; all records and counts appear in the later audit and JSON sidecar.

| Type (record count) | Promoted record / source | Public target value | Exact promotion | Outcome / remaining policies |
| --- | --- | --- | --- | --- |
| approval_without_target (12) | [record-51d930d16c3a](#record-51d930d16c3a) | title = 'Quarterly allocation 51871 \| SNAP-51871' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=internal | contradiction / 0 |
| rejected_opposite_artifact (12) | [record-4ee7b6e8f98f](#record-4ee7b6e8f98f) | title = 'Quarterly allocation 75713' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal | contradiction / 0 |
| target_field_preference (12) | [record-35188f97aa23](#record-35188f97aa23) | title = 'Quarterly allocation 39885' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal | contradiction / 0 |
| unauthorised_revision (12) | [record-86f2948918a3](#record-86f2948918a3) | title = 'Quarterly allocation 58007 \| SNAP-58007' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=external | contradiction / 0 |

An action flip requires a nonempty compatible set and a changed diagnostic or control
action. A contradiction has no compatible policy and supplies neither task action.

[Complete oracle derivation](#oracle-derivation-from-public-evidence) · [Every counterfactual record](#single-record-counterfactual-relevance)

## Public configuration and assumptions

```json
{
  "as_of": "2026-06-15T12:00:00Z",
  "baseline_template": {
    "source_footnote": "{source_footnote}",
    "title": "{base_title} | {snapshot}"
  },
  "dimensions": {
    "artifact": [
      "chart",
      "numeric_table"
    ],
    "audience": [
      "internal",
      "external"
    ]
  },
  "fact_descriptions": {
    "base_title": "Current title without a snapshot suffix.",
    "snapshot": "Current snapshot label.",
    "source_footnote": "Current source note."
  },
  "field_option": {
    "field": "title",
    "operation": "set_fact",
    "separator": "",
    "value": "base_title"
  },
  "hypothesis_class": "h14",
  "hypothesis_definition": "Each of the two declared binary context dimensions defines a predicate testing its second listed value. Call these predicates x and y. In each registered version the target field configuration is one Boolean function from the following class: constant 0 or 1; x, not x, y, or not y; a conjunction of one literal from each dimension; or a disjunction of one literal from each dimension. Zero selects the configured baseline and one the available alternative. The fourteen distinct truth tables exclude only XOR and XNOR. Each version has its own class member, with no cross-version coupling. This restriction is a supplied synthetic assumption, not an established property of enterprise work.",
  "task_family": "report_artifact",
  "workflow": "workflow-f978d20c60f7"
}
```

This is a bounded synthetic workflow model. initial_configuration declares the field options, two context dimensions and the complete H14 hypothesis class. Each registered version has one class member. A field observation constrains the member indexed by its recorded version. Broader consequences follow from the declared class. Facts provide current artifact values. Other fields retain their configured baseline. Outside the declared task_family and workflow, or without a complete declared context, no update is authorised by this model. A register_version event supplies trusted workflow metadata with the authority roster and half-open validity interval. Binding field approval is an event of type review with decision accept, performed by a listed reviewer within that interval, with the field included in reviewed_fields. Its accepted artifact establishes the field configuration at the recorded context. This explicit approval convention is a supplied synthetic assumption. A forward has an origin_ref identifying the record whose content it reproduces. Raw artifacts expose named revisions and a selected artifact reference; interpreted records expose the selected fields directly. A rejection records a whole-artifact decision and its stated grounds. An artifact field whose review is not recorded has no approved assignment. The configured baseline is retained when the available evidence does not establish an update. Dates and version labels in new work identify the applicable registration.

## Public work records

### record-db32dbbdfec6

2026-06-12T15:43:06Z | revision | Daria

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 68775",
    "date": "2026-06-12",
    "document_id": "DOC-68775",
    "snapshot": "SNAP-68775",
    "source_footnote": "Source: approved extract EX-68775."
  },
  "message": "My personal choice here would be title set to 'Quarterly allocation 68775 | SNAP-68775'.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-68775.",
    "title": "Quarterly allocation 68775 | SNAP-68775"
  }
}
```

### record-bcc9228c3dff

2026-05-23T17:10:02Z | review | Jonas

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=external

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-edf9c8f6ec8a
- comment: Checked.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-97631.",
    "title": "Quarterly allocation 97631"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 97631",
    "before": "Quarterly allocation 97631 | SNAP-97631",
    "field": "title"
  },
  "comment": "Checked.",
  "decision": "accept",
  "document_id": "DOC-97631",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 97631",
    "date": "2026-05-23",
    "document_id": "DOC-97631",
    "snapshot": "SNAP-97631",
    "source_footnote": "Source: approved extract EX-97631."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-874524c1f2a1

2026-06-12T14:13:32Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=internal

- decision: reject
- reviewed_fields: []
- authority_ref: record-edf9c8f6ec8a
- comment: Checked.

```json
{
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 54196",
    "before": "Quarterly allocation 54196 | SNAP-54196",
    "field": "title"
  },
  "comment": "Checked.",
  "decision": "reject",
  "document_id": "DOC-54196",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 54196",
    "date": "2026-06-12",
    "document_id": "DOC-54196",
    "snapshot": "SNAP-54196",
    "source_footnote": "Source: approved extract EX-54196."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-54196.",
    "title": "Quarterly allocation 54196"
  },
  "rejection_reason": "Missing signature block; the artifact was returned before field review.",
  "reviewed_fields": []
}
```

### record-785ee2a0047e

2026-06-12T12:16:10Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=external


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
  "request_id": "request-8c5380180f79"
}
```

### record-51d930d16c3a

2026-05-23T10:44:33Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=internal

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-edf9c8f6ec8a
- comment: Review complete.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-05-23T10:44:33Z",
    "source_footnote": "Source: approved extract EX-51871.",
    "title": "Quarterly allocation 51871 | SNAP-51871"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 51871 | SNAP-51871",
    "before": "Quarterly allocation 51871",
    "field": "title"
  },
  "comment": "Review complete.",
  "decision": "accept",
  "document_id": "DOC-51871",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 51871",
    "date": "2026-05-23",
    "document_id": "DOC-51871",
    "snapshot": "SNAP-51871",
    "source_footnote": "Source: approved extract EX-51871."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-1eef212119ba

2026-06-12T12:07:17Z | review | Robin

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal

- decision: reject
- reviewed_fields: []
- authority_ref: record-edf9c8f6ec8a
- comment: Recorded.

```json
{
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 62114 | SNAP-62114",
    "before": "Quarterly allocation 62114",
    "field": "title"
  },
  "comment": "Recorded.",
  "decision": "reject",
  "document_id": "DOC-62114",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 62114",
    "date": "2026-06-12",
    "document_id": "DOC-62114",
    "snapshot": "SNAP-62114",
    "source_footnote": "Source: approved extract EX-62114."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-62114.",
    "title": "Quarterly allocation 62114 | SNAP-62114"
  },
  "rejection_reason": "Review stopped at the missing signature block. Target-field checks remain open.",
  "reviewed_fields": []
}
```

### record-35188f97aa23

2026-05-31T11:39:26Z | revision | Elena

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 39885",
    "date": "2026-05-31",
    "document_id": "DOC-39885",
    "snapshot": "SNAP-39885",
    "source_footnote": "Source: approved extract EX-39885."
  },
  "message": "My personal choice here would be title set to 'Quarterly allocation 39885'.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-39885.",
    "title": "Quarterly allocation 39885"
  }
}
```

### record-f2e50ae9c6f3

2026-05-31T15:49:30Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=internal


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
  "request_id": "request-dea7244c545c"
}
```

### record-ead2e643f1ab

2026-05-31T13:15:03Z | revision | Anika

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 10061",
    "date": "2026-05-31",
    "document_id": "DOC-10061",
    "snapshot": "SNAP-10061",
    "source_footnote": "Source: approved extract EX-10061."
  },
  "message": "For my version I would use title set to 'Quarterly allocation 10061'.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-10061.",
    "title": "Quarterly allocation 10061"
  }
}
```

### record-955f6b117be9

2026-05-31T16:05:09Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=external


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
  "request_id": "request-4c6129c46240"
}
```

### record-4ee7b6e8f98f

2026-05-23T17:53:23Z | review | Robin

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal

- decision: reject
- reviewed_fields: []
- authority_ref: record-edf9c8f6ec8a
- comment: Recorded.

```json
{
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 75713",
    "before": "Quarterly allocation 75713 | SNAP-75713",
    "field": "title"
  },
  "comment": "Recorded.",
  "decision": "reject",
  "document_id": "DOC-75713",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 75713",
    "date": "2026-05-23",
    "document_id": "DOC-75713",
    "snapshot": "SNAP-75713",
    "source_footnote": "Source: approved extract EX-75713."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-75713.",
    "title": "Quarterly allocation 75713"
  },
  "rejection_reason": "The signature block is missing. Field-level review was not completed.",
  "reviewed_fields": []
}
```

### record-07f58aee9c3c

2026-06-12T16:17:23Z | revision | Jonas

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=external


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 53048",
    "date": "2026-06-12",
    "document_id": "DOC-53048",
    "snapshot": "SNAP-53048",
    "source_footnote": "Source: approved extract EX-53048."
  },
  "message": "I would prefer title set to 'Quarterly allocation 53048 | SNAP-53048' for this item.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-53048.",
    "title": "Quarterly allocation 53048 | SNAP-53048"
  }
}
```

### record-dff5d3984839

2026-06-12T12:43:22Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=external


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
  "request_id": "request-787d46354488"
}
```

### record-b8f32e66e6bc

2026-05-23T14:03:30Z | review | Elena

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=external

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-edf9c8f6ec8a
- comment: Reviewed.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-27799.",
    "title": "Quarterly allocation 27799"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 27799",
    "before": "Quarterly allocation 27799 | SNAP-27799",
    "field": "title"
  },
  "comment": "Reviewed.",
  "decision": "accept",
  "document_id": "DOC-27799",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 27799",
    "date": "2026-05-23",
    "document_id": "DOC-27799",
    "snapshot": "SNAP-27799",
    "source_footnote": "Source: approved extract EX-27799."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-77315f1936f1

2026-06-12T17:09:51Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal


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
  "request_id": "request-790780fe24a3"
}
```

### record-c967b4143393

2026-06-12T14:27:27Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=external

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-edf9c8f6ec8a
- comment: Review complete.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-06-12T14:27:27Z",
    "source_footnote": "Source: approved extract EX-11266.",
    "title": "Quarterly allocation 11266"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 11266",
    "before": "Quarterly allocation 11266 | SNAP-11266",
    "field": "title"
  },
  "comment": "Review complete.",
  "decision": "accept",
  "document_id": "DOC-11266",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 11266",
    "date": "2026-06-12",
    "document_id": "DOC-11266",
    "snapshot": "SNAP-11266",
    "source_footnote": "Source: approved extract EX-11266."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-a05edcbf8ccf

2026-05-23T15:08:02Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=internal

- decision: reject
- reviewed_fields: []
- authority_ref: record-edf9c8f6ec8a
- comment: Checked.

```json
{
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 89693 | SNAP-89693",
    "before": "Quarterly allocation 89693",
    "field": "title"
  },
  "comment": "Checked.",
  "decision": "reject",
  "document_id": "DOC-89693",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 89693",
    "date": "2026-05-23",
    "document_id": "DOC-89693",
    "snapshot": "SNAP-89693",
    "source_footnote": "Source: approved extract EX-89693."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-89693.",
    "title": "Quarterly allocation 89693 | SNAP-89693"
  },
  "rejection_reason": "Review stopped at the missing signature block. Target-field checks remain open.",
  "reviewed_fields": []
}
```

### record-7a78bbaf249a

2026-06-12T16:41:44Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=external

- decision: reject
- reviewed_fields: []
- authority_ref: record-edf9c8f6ec8a
- comment: Completed.

```json
{
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 29638",
    "before": "Quarterly allocation 29638 | SNAP-29638",
    "field": "title"
  },
  "comment": "Completed.",
  "decision": "reject",
  "document_id": "DOC-29638",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 29638",
    "date": "2026-06-12",
    "document_id": "DOC-29638",
    "snapshot": "SNAP-29638",
    "source_footnote": "Source: approved extract EX-29638."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-29638.",
    "title": "Quarterly allocation 29638"
  },
  "rejection_reason": "Missing signature block; the artifact was returned before field review.",
  "reviewed_fields": []
}
```

### record-86f2948918a3

2026-05-23T10:35:17Z | review | Elena

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=external

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-edf9c8f6ec8a
- comment: Approved.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-58007.",
    "title": "Quarterly allocation 58007 | SNAP-58007"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 58007 | SNAP-58007",
    "before": "Quarterly allocation 58007",
    "field": "title"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-58007",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 58007",
    "date": "2026-05-23",
    "document_id": "DOC-58007",
    "snapshot": "SNAP-58007",
    "source_footnote": "Source: approved extract EX-58007."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-c5523c0b9399

2026-05-31T15:54:49Z | review | Robin

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-edf9c8f6ec8a
- comment: Review complete.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-86085.",
    "title": "Quarterly allocation 86085 | SNAP-86085"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 86085 | SNAP-86085",
    "before": "Quarterly allocation 86085",
    "field": "title"
  },
  "comment": "Review complete.",
  "decision": "accept",
  "document_id": "DOC-86085",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 86085",
    "date": "2026-05-31",
    "document_id": "DOC-86085",
    "snapshot": "SNAP-86085",
    "source_footnote": "Source: approved extract EX-86085."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-5719fe10a847

2026-05-23T14:49:18Z | review | Elena

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=external

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-edf9c8f6ec8a
- comment: Reviewed.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-38384.",
    "title": "Quarterly allocation 38384 | SNAP-38384"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 38384 | SNAP-38384",
    "before": "Quarterly allocation 38384",
    "field": "title"
  },
  "comment": "Reviewed.",
  "decision": "accept",
  "document_id": "DOC-38384",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 38384",
    "date": "2026-05-23",
    "document_id": "DOC-38384",
    "snapshot": "SNAP-38384",
    "source_footnote": "Source: approved extract EX-38384."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-26079bc4a4d5

2026-05-31T17:08:56Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=internal


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
  "log": "Retry completed successfully.",
  "request_id": "request-6b47883c9651"
}
```

### record-837fb0516311

2026-06-12T11:20:18Z | review | Elena

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=internal

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-edf9c8f6ec8a
- comment: Approved.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-20275.",
    "title": "Quarterly allocation 20275 | SNAP-20275"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 20275 | SNAP-20275",
    "before": "Quarterly allocation 20275",
    "field": "title"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-20275",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 20275",
    "date": "2026-06-12",
    "document_id": "DOC-20275",
    "snapshot": "SNAP-20275",
    "source_footnote": "Source: approved extract EX-20275."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-69097a1fefd4

2026-05-23T14:46:21Z | review | Robin

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=external

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-edf9c8f6ec8a
- comment: Approved.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-05-23T14:46:21Z",
    "source_footnote": "Source: approved extract EX-41428.",
    "title": "Quarterly allocation 41428"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 41428",
    "before": "Quarterly allocation 41428 | SNAP-41428",
    "field": "title"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-41428",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 41428",
    "date": "2026-05-23",
    "document_id": "DOC-41428",
    "snapshot": "SNAP-41428",
    "source_footnote": "Source: approved extract EX-41428."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-b3a0982e618e

2026-06-12T09:41:23Z | review | Jonas

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=external

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-edf9c8f6ec8a
- comment: Checked.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-29174.",
    "title": "Quarterly allocation 29174"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 29174",
    "before": "Quarterly allocation 29174 | SNAP-29174",
    "field": "title"
  },
  "comment": "Checked.",
  "decision": "accept",
  "document_id": "DOC-29174",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 29174",
    "date": "2026-06-12",
    "document_id": "DOC-29174",
    "snapshot": "SNAP-29174",
    "source_footnote": "Source: approved extract EX-29174."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-faccea4248ef

2026-05-31T17:33:59Z | revision | Elena

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=external


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 66588",
    "date": "2026-05-31",
    "document_id": "DOC-66588",
    "snapshot": "SNAP-66588",
    "source_footnote": "Source: approved extract EX-66588."
  },
  "message": "I would prefer title set to 'Quarterly allocation 66588' for this item.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-66588.",
    "title": "Quarterly allocation 66588"
  }
}
```

### record-8b8d9e86fdcb

2026-05-31T15:04:50Z | review | Robin

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=external

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-edf9c8f6ec8a
- comment: Review complete.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-05-31T15:04:50Z",
    "source_footnote": "Source: approved extract EX-69829.",
    "title": "Quarterly allocation 69829 | SNAP-69829"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 69829 | SNAP-69829",
    "before": "Quarterly allocation 69829",
    "field": "title"
  },
  "comment": "Review complete.",
  "decision": "accept",
  "document_id": "DOC-69829",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 69829",
    "date": "2026-05-31",
    "document_id": "DOC-69829",
    "snapshot": "SNAP-69829",
    "source_footnote": "Source: approved extract EX-69829."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-325491c706a4

2026-05-31T10:53:51Z | revision | Theo

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=external


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 68643",
    "date": "2026-05-31",
    "document_id": "DOC-68643",
    "snapshot": "SNAP-68643",
    "source_footnote": "Source: approved extract EX-68643."
  },
  "message": "My personal choice here would be title set to 'Quarterly allocation 68643 | SNAP-68643'.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-68643.",
    "title": "Quarterly allocation 68643 | SNAP-68643"
  }
}
```

### record-509aba153258

2026-06-12T15:53:18Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal


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
  "request_id": "request-362665f843e4"
}
```

### record-412b8e005a18

2026-05-31T16:00:07Z | revision | Robin

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=external


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 80767",
    "date": "2026-05-31",
    "document_id": "DOC-80767",
    "snapshot": "SNAP-80767",
    "source_footnote": "Source: approved extract EX-80767."
  },
  "message": "I would prefer title set to 'Quarterly allocation 80767' for this item.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-80767.",
    "title": "Quarterly allocation 80767"
  }
}
```

### record-123a93d85b3a

2026-06-12T10:21:33Z | review | Robin

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal

- decision: reject
- reviewed_fields: []
- authority_ref: record-edf9c8f6ec8a
- comment: Review complete.

```json
{
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 32421",
    "before": "Quarterly allocation 32421 | SNAP-32421",
    "field": "title"
  },
  "comment": "Review complete.",
  "decision": "reject",
  "document_id": "DOC-32421",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 32421",
    "date": "2026-06-12",
    "document_id": "DOC-32421",
    "snapshot": "SNAP-32421",
    "source_footnote": "Source: approved extract EX-32421."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-32421.",
    "title": "Quarterly allocation 32421"
  },
  "rejection_reason": "Review stopped at the missing signature block. Target-field checks remain open.",
  "reviewed_fields": []
}
```

### record-ce75754ce6cb

2026-05-23T14:00:42Z | review | Robin

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=external

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-edf9c8f6ec8a
- comment: Reviewed.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-05-23T14:00:42Z",
    "source_footnote": "Source: approved extract EX-42516.",
    "title": "Quarterly allocation 42516 | SNAP-42516"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 42516 | SNAP-42516",
    "before": "Quarterly allocation 42516",
    "field": "title"
  },
  "comment": "Reviewed.",
  "decision": "accept",
  "document_id": "DOC-42516",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 42516",
    "date": "2026-05-23",
    "document_id": "DOC-42516",
    "snapshot": "SNAP-42516",
    "source_footnote": "Source: approved extract EX-42516."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-f59ed0eac296

2026-06-12T11:37:12Z | review | Robin

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=internal

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-edf9c8f6ec8a
- comment: Approved.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-56153.",
    "title": "Quarterly allocation 56153"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 56153",
    "before": "Quarterly allocation 56153 | SNAP-56153",
    "field": "title"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-56153",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 56153",
    "date": "2026-06-12",
    "document_id": "DOC-56153",
    "snapshot": "SNAP-56153",
    "source_footnote": "Source: approved extract EX-56153."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-6c82139e65d5

2026-05-31T13:28:54Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=external

- decision: reject
- reviewed_fields: []
- authority_ref: record-edf9c8f6ec8a
- comment: Review complete.

```json
{
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 23641",
    "before": "Quarterly allocation 23641 | SNAP-23641",
    "field": "title"
  },
  "comment": "Review complete.",
  "decision": "reject",
  "document_id": "DOC-23641",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 23641",
    "date": "2026-05-31",
    "document_id": "DOC-23641",
    "snapshot": "SNAP-23641",
    "source_footnote": "Source: approved extract EX-23641."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-23641.",
    "title": "Quarterly allocation 23641"
  },
  "rejection_reason": "Review stopped at the missing signature block. Target-field checks remain open.",
  "reviewed_fields": []
}
```

### record-3bc718860c73

2026-06-12T11:34:05Z | review | Robin

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-edf9c8f6ec8a
- comment: Approved.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-06-12T11:34:05Z",
    "source_footnote": "Source: approved extract EX-33068.",
    "title": "Quarterly allocation 33068"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 33068",
    "before": "Quarterly allocation 33068 | SNAP-33068",
    "field": "title"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-33068",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 33068",
    "date": "2026-06-12",
    "document_id": "DOC-33068",
    "snapshot": "SNAP-33068",
    "source_footnote": "Source: approved extract EX-33068."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-694b03611256

2026-05-23T14:48:28Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=internal

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-edf9c8f6ec8a
- comment: Reviewed.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-05-23T14:48:28Z",
    "source_footnote": "Source: approved extract EX-74174.",
    "title": "Quarterly allocation 74174 | SNAP-74174"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 74174 | SNAP-74174",
    "before": "Quarterly allocation 74174",
    "field": "title"
  },
  "comment": "Reviewed.",
  "decision": "accept",
  "document_id": "DOC-74174",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 74174",
    "date": "2026-05-23",
    "document_id": "DOC-74174",
    "snapshot": "SNAP-74174",
    "source_footnote": "Source: approved extract EX-74174."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-51379a55fe7b

2026-06-12T15:37:17Z | revision | Elena

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 52019",
    "date": "2026-06-12",
    "document_id": "DOC-52019",
    "snapshot": "SNAP-52019",
    "source_footnote": "Source: approved extract EX-52019."
  },
  "message": "For my version I would use title set to 'Quarterly allocation 52019 | SNAP-52019'.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-52019.",
    "title": "Quarterly allocation 52019 | SNAP-52019"
  }
}
```

### record-bf7d9be02e76

2026-05-31T09:01:41Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-edf9c8f6ec8a
- comment: Approved.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-05-31T09:01:41Z",
    "source_footnote": "Source: approved extract EX-37424.",
    "title": "Quarterly allocation 37424 | SNAP-37424"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 37424 | SNAP-37424",
    "before": "Quarterly allocation 37424",
    "field": "title"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-37424",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 37424",
    "date": "2026-05-31",
    "document_id": "DOC-37424",
    "snapshot": "SNAP-37424",
    "source_footnote": "Source: approved extract EX-37424."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-a59387bb2f56

2026-05-31T15:55:50Z | review | Jonas

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-edf9c8f6ec8a
- comment: Review complete.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-59477.",
    "title": "Quarterly allocation 59477 | SNAP-59477"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 59477 | SNAP-59477",
    "before": "Quarterly allocation 59477",
    "field": "title"
  },
  "comment": "Review complete.",
  "decision": "accept",
  "document_id": "DOC-59477",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 59477",
    "date": "2026-05-31",
    "document_id": "DOC-59477",
    "snapshot": "SNAP-59477",
    "source_footnote": "Source: approved extract EX-59477."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-80af99033879

2026-05-23T11:57:50Z | revision | Robin

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=external


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 29601",
    "date": "2026-05-23",
    "document_id": "DOC-29601",
    "snapshot": "SNAP-29601",
    "source_footnote": "Source: approved extract EX-29601."
  },
  "message": "For my version I would use title set to 'Quarterly allocation 29601 | SNAP-29601'.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-29601.",
    "title": "Quarterly allocation 29601 | SNAP-29601"
  }
}
```

### record-b73b74fad664

2026-05-23T14:59:31Z | revision | Robin

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 48329",
    "date": "2026-05-23",
    "document_id": "DOC-48329",
    "snapshot": "SNAP-48329",
    "source_footnote": "Source: approved extract EX-48329."
  },
  "message": "I would prefer title set to 'Quarterly allocation 48329' for this item.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-48329.",
    "title": "Quarterly allocation 48329"
  }
}
```

### record-3082091c7641

2026-05-31T10:38:19Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=external

- decision: reject
- reviewed_fields: []
- authority_ref: record-edf9c8f6ec8a
- comment: Review complete.

```json
{
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 84833 | SNAP-84833",
    "before": "Quarterly allocation 84833",
    "field": "title"
  },
  "comment": "Review complete.",
  "decision": "reject",
  "document_id": "DOC-84833",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 84833",
    "date": "2026-05-31",
    "document_id": "DOC-84833",
    "snapshot": "SNAP-84833",
    "source_footnote": "Source: approved extract EX-84833."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-84833.",
    "title": "Quarterly allocation 84833 | SNAP-84833"
  },
  "rejection_reason": "The signature block is missing. Field-level review was not completed.",
  "reviewed_fields": []
}
```

### record-2f47a8fbb5c5

2026-05-23T10:59:39Z | review | Theo

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-edf9c8f6ec8a
- comment: Review complete.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-93015.",
    "title": "Quarterly allocation 93015 | SNAP-93015"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 93015 | SNAP-93015",
    "before": "Quarterly allocation 93015",
    "field": "title"
  },
  "comment": "Review complete.",
  "decision": "accept",
  "document_id": "DOC-93015",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 93015",
    "date": "2026-05-23",
    "document_id": "DOC-93015",
    "snapshot": "SNAP-93015",
    "source_footnote": "Source: approved extract EX-93015."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-603ed31407f7

2026-06-12T08:22:05Z | review | Anika

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=external

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-edf9c8f6ec8a
- comment: Reviewed.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-24845.",
    "title": "Quarterly allocation 24845 | SNAP-24845"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 24845 | SNAP-24845",
    "before": "Quarterly allocation 24845",
    "field": "title"
  },
  "comment": "Reviewed.",
  "decision": "accept",
  "document_id": "DOC-24845",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 24845",
    "date": "2026-06-12",
    "document_id": "DOC-24845",
    "snapshot": "SNAP-24845",
    "source_footnote": "Source: approved extract EX-24845."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-623129cfc74d

2026-06-12T11:43:35Z | review | Elena

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=internal

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-edf9c8f6ec8a
- comment: Approved.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-46346.",
    "title": "Quarterly allocation 46346"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 46346",
    "before": "Quarterly allocation 46346 | SNAP-46346",
    "field": "title"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-46346",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 46346",
    "date": "2026-06-12",
    "document_id": "DOC-46346",
    "snapshot": "SNAP-46346",
    "source_footnote": "Source: approved extract EX-46346."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-533710671044

2026-06-12T08:35:53Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=external


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
  "log": "Retry completed successfully.",
  "request_id": "request-85e3cff67c3c"
}
```

### record-c330f8d90d55

2026-06-12T11:52:47Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=external

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-edf9c8f6ec8a
- comment: Approved.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-06-12T11:52:47Z",
    "source_footnote": "Source: approved extract EX-43222.",
    "title": "Quarterly allocation 43222"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 43222",
    "before": "Quarterly allocation 43222 | SNAP-43222",
    "field": "title"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-43222",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 43222",
    "date": "2026-06-12",
    "document_id": "DOC-43222",
    "snapshot": "SNAP-43222",
    "source_footnote": "Source: approved extract EX-43222."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-37dabbefcd0b

2026-05-31T15:55:20Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-edf9c8f6ec8a
- comment: Review complete.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-05-31T15:55:20Z",
    "source_footnote": "Source: approved extract EX-62667.",
    "title": "Quarterly allocation 62667"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 62667",
    "before": "Quarterly allocation 62667 | SNAP-62667",
    "field": "title"
  },
  "comment": "Review complete.",
  "decision": "accept",
  "document_id": "DOC-62667",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 62667",
    "date": "2026-05-31",
    "document_id": "DOC-62667",
    "snapshot": "SNAP-62667",
    "source_footnote": "Source: approved extract EX-62667."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-6a1b2664e5b9

2026-05-31T16:28:33Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=external

- decision: reject
- reviewed_fields: []
- authority_ref: record-edf9c8f6ec8a
- comment: Review complete.

```json
{
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 49359",
    "before": "Quarterly allocation 49359 | SNAP-49359",
    "field": "title"
  },
  "comment": "Review complete.",
  "decision": "reject",
  "document_id": "DOC-49359",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 49359",
    "date": "2026-05-31",
    "document_id": "DOC-49359",
    "snapshot": "SNAP-49359",
    "source_footnote": "Source: approved extract EX-49359."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-49359.",
    "title": "Quarterly allocation 49359"
  },
  "rejection_reason": "Review stopped at the missing signature block. Target-field checks remain open.",
  "reviewed_fields": []
}
```

### record-3d0e769ddbd3

2026-05-31T15:23:38Z | review | Jonas

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=external

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-edf9c8f6ec8a
- comment: Review complete.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-66499.",
    "title": "Quarterly allocation 66499"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 66499",
    "before": "Quarterly allocation 66499 | SNAP-66499",
    "field": "title"
  },
  "comment": "Review complete.",
  "decision": "accept",
  "document_id": "DOC-66499",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 66499",
    "date": "2026-05-31",
    "document_id": "DOC-66499",
    "snapshot": "SNAP-66499",
    "source_footnote": "Source: approved extract EX-66499."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-beefd5f66c9a

2026-05-23T17:06:00Z | review | Robin

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=external

- decision: reject
- reviewed_fields: []
- authority_ref: record-edf9c8f6ec8a
- comment: Reviewed.

```json
{
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 63627 | SNAP-63627",
    "before": "Quarterly allocation 63627",
    "field": "title"
  },
  "comment": "Reviewed.",
  "decision": "reject",
  "document_id": "DOC-63627",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 63627",
    "date": "2026-05-23",
    "document_id": "DOC-63627",
    "snapshot": "SNAP-63627",
    "source_footnote": "Source: approved extract EX-63627."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-63627.",
    "title": "Quarterly allocation 63627 | SNAP-63627"
  },
  "rejection_reason": "Missing signature block; the artifact was returned before field review.",
  "reviewed_fields": []
}
```

### record-ece5ee6f0778

2026-05-23T11:45:58Z | review | Robin

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=internal

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-edf9c8f6ec8a
- comment: Reviewed.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-05-23T11:45:58Z",
    "source_footnote": "Source: approved extract EX-12850.",
    "title": "Quarterly allocation 12850 | SNAP-12850"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 12850 | SNAP-12850",
    "before": "Quarterly allocation 12850",
    "field": "title"
  },
  "comment": "Reviewed.",
  "decision": "accept",
  "document_id": "DOC-12850",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 12850",
    "date": "2026-05-23",
    "document_id": "DOC-12850",
    "snapshot": "SNAP-12850",
    "source_footnote": "Source: approved extract EX-12850."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-edf9c8f6ec8a

2026-01-01T00:00:00Z | template | workflow-registry

Context: 


```json
{
  "authorised_reviewers": [
    "Robin",
    "Daria"
  ],
  "event": "register_version",
  "supersedes": null,
  "task_family": "report_artifact",
  "valid_from": "2026-01-01T00:00:00Z",
  "valid_until": "2027-01-01T00:00:00Z",
  "version": "edition-6c192159bf30",
  "workflow": "workflow-f978d20c60f7"
}
```

### record-d9f3cbd0155c

2026-05-31T16:44:38Z | review | Robin

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=external

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-edf9c8f6ec8a
- comment: Review complete.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-05-31T16:44:38Z",
    "source_footnote": "Source: approved extract EX-42564.",
    "title": "Quarterly allocation 42564"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 42564",
    "before": "Quarterly allocation 42564 | SNAP-42564",
    "field": "title"
  },
  "comment": "Review complete.",
  "decision": "accept",
  "document_id": "DOC-42564",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 42564",
    "date": "2026-05-31",
    "document_id": "DOC-42564",
    "snapshot": "SNAP-42564",
    "source_footnote": "Source: approved extract EX-42564."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-0e4b962f7040

2026-05-23T17:52:07Z | review | Robin

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=internal

- decision: reject
- reviewed_fields: []
- authority_ref: record-edf9c8f6ec8a
- comment: Checked.

```json
{
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 96293 | SNAP-96293",
    "before": "Quarterly allocation 96293",
    "field": "title"
  },
  "comment": "Checked.",
  "decision": "reject",
  "document_id": "DOC-96293",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 96293",
    "date": "2026-05-23",
    "document_id": "DOC-96293",
    "snapshot": "SNAP-96293",
    "source_footnote": "Source: approved extract EX-96293."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-96293.",
    "title": "Quarterly allocation 96293 | SNAP-96293"
  },
  "rejection_reason": "Missing signature block; the artifact was returned before field review.",
  "reviewed_fields": []
}
```

### record-887c32cf23cc

2026-05-31T10:19:01Z | revision | Elena

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 25933",
    "date": "2026-05-31",
    "document_id": "DOC-25933",
    "snapshot": "SNAP-25933",
    "source_footnote": "Source: approved extract EX-25933."
  },
  "message": "For my version I would use title set to 'Quarterly allocation 25933'.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-25933.",
    "title": "Quarterly allocation 25933"
  }
}
```

### record-5f6f0cf22bb1

2026-05-23T14:05:28Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=external

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-edf9c8f6ec8a
- comment: Reviewed.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-92524.",
    "title": "Quarterly allocation 92524"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 92524",
    "before": "Quarterly allocation 92524 | SNAP-92524",
    "field": "title"
  },
  "comment": "Reviewed.",
  "decision": "accept",
  "document_id": "DOC-92524",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 92524",
    "date": "2026-05-23",
    "document_id": "DOC-92524",
    "snapshot": "SNAP-92524",
    "source_footnote": "Source: approved extract EX-92524."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-094913dcf75e

2026-06-12T10:31:53Z | review | Theo

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=internal

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-edf9c8f6ec8a
- comment: Approved.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-42657.",
    "title": "Quarterly allocation 42657 | SNAP-42657"
  },
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 42657 | SNAP-42657",
    "before": "Quarterly allocation 42657",
    "field": "title"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-42657",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 42657",
    "date": "2026-06-12",
    "document_id": "DOC-42657",
    "snapshot": "SNAP-42657",
    "source_footnote": "Source: approved extract EX-42657."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-bdd8ece9528e

2026-05-31T14:59:27Z | revision | Jonas

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=external


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 62750",
    "date": "2026-05-31",
    "document_id": "DOC-62750",
    "snapshot": "SNAP-62750",
    "source_footnote": "Source: approved extract EX-62750."
  },
  "message": "I would prefer title set to 'Quarterly allocation 62750' for this item.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-62750.",
    "title": "Quarterly allocation 62750"
  }
}
```

### record-63117ba33fff

2026-06-12T12:17:59Z | review | Robin

Context: task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=external

- decision: reject
- reviewed_fields: []
- authority_ref: record-edf9c8f6ec8a
- comment: Checked.

```json
{
  "authority_ref": "record-edf9c8f6ec8a",
  "change_summary": {
    "after": "Quarterly allocation 38725 | SNAP-38725",
    "before": "Quarterly allocation 38725",
    "field": "title"
  },
  "comment": "Checked.",
  "decision": "reject",
  "document_id": "DOC-38725",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 38725",
    "date": "2026-06-12",
    "document_id": "DOC-38725",
    "snapshot": "SNAP-38725",
    "source_footnote": "Source: approved extract EX-38725."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-38725.",
    "title": "Quarterly allocation 38725 | SNAP-38725"
  },
  "rejection_reason": "The signature block is missing. Field-level review was not completed.",
  "reviewed_fields": []
}
```

## Oracle derivation from public evidence

Recomputed solely from the public History by the independent oracle.

H14 excludes XOR and XNOR; transfer identification depends on this supplied restriction.

Distinct current-version functions: **1**. Full policies across all registered versions: **1**.

An approval constrains one cell in its registered version. The following are the
actual applied constraints, including independent repeats. Copies do not add a constraint.

| Public record | Version | Context | Field option |
| --- | --- | --- | --- |
| record-c5523c0b9399 | edition-6c192159bf30 | task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=internal | 0 |
| record-f59ed0eac296 | edition-6c192159bf30 | task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=numeric_table, audience=internal | 1 |
| record-5f6f0cf22bb1 | edition-6c192159bf30 | task_family=report_artifact, workflow=workflow-f978d20c60f7, version=edition-6c192159bf30, artifact=chart, audience=external | 1 |

### Competing requirement explanations

Zero is the configured baseline; one is the alternative. Each row is a distinct
compatible function for this version. No preference for simplicity removes a row.
The private sampling plan and world policy do not filter these explanations.

Version edition-6c192159bf30: 1 compatible functions.

| Function | artifact=chart, audience=internal | artifact=chart, audience=external | artifact=numeric_table, audience=internal | artifact=numeric_table, audience=external | Complexity |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | 1 | 1 | 1 | 2 |

### Diagnostic and control derivations

| Task | Context observed | Witnesses | Action | Retention basis |
| --- | --- | --- | --- | --- |
| diagnostic | False | none | apply | not_retention |
| control | True | record-c5523c0b9399 | keep | resolved |

## Private material audit

These design labels, counterfactuals and world requirements are evaluator material.
They are never preparation or generation inputs. The true world is distinct from
what the public evidence identifies. Exact world fields are shown with each task.

Registered record counts and construction audit:

```json
{
  "additional_noise_counts": {
    "approval_without_target": 12,
    "rejected_opposite_artifact": 12,
    "target_field_preference": 12,
    "technical": 8,
    "unauthorised_revision": 12
  },
  "admissible_count": 1,
  "control_basis": "resolved_keep",
  "current_admissible_count": 1,
  "current_witness_contexts": [
    {
      "artifact": "chart",
      "audience": "internal",
      "task_family": "report_artifact",
      "version": "edition-6c192159bf30",
      "workflow": "workflow-f978d20c60f7"
    },
    {
      "artifact": "chart",
      "audience": "external",
      "task_family": "report_artifact",
      "version": "edition-6c192159bf30",
      "workflow": "workflow-f978d20c60f7"
    },
    {
      "artifact": "numeric_table",
      "audience": "internal",
      "task_family": "report_artifact",
      "version": "edition-6c192159bf30",
      "workflow": "workflow-f978d20c60f7"
    }
  ],
  "diagnostic_observed": false,
  "material_revision": "v04-amendment-03-r2",
  "record_count": 60,
  "registered_versions": [
    "edition-6c192159bf30"
  ],
  "rendering": "interpreted",
  "reversed_option": true,
  "task_type": "transfer_change"
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
| approval_without_target | 12 | 0 | 7 | 5 | 0 | 0 | 0 | record-51d930d16c3a, record-8b8d9e86fdcb, record-ce75754ce6cb, record-3bc718860c73, record-694b03611256, record-37dabbefcd0b, record-ece5ee6f0778 |
| rejected_opposite_artifact | 12 | 0 | 7 | 5 | 0 | 0 | 0 | record-4ee7b6e8f98f, record-a05edcbf8ccf, record-123a93d85b3a, record-3082091c7641, record-beefd5f66c9a, record-0e4b962f7040, record-63117ba33fff |
| target_field_preference | 12 | 0 | 7 | 5 | 0 | 0 | 0 | record-35188f97aa23, record-ead2e643f1ab, record-07f58aee9c3c, record-325491c706a4, record-80af99033879, record-b73b74fad664, record-887c32cf23cc |
| unauthorised_revision | 12 | 0 | 5 | 7 | 0 | 0 | 0 | record-86f2948918a3, record-5719fe10a847, record-837fb0516311, record-603ed31407f7, record-094913dcf75e |

### Every promoted public record

| Record | Type | Origin | Public option | Remaining policies | Outcome | Qualifies | Diagnostic action | Control action |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| record-db32dbbdfec6 | target_field_preference | record-db32dbbdfec6 | 0 | 1 | unchanged_constraints | False | apply | keep |
| record-bcc9228c3dff | unauthorised_revision | record-bcc9228c3dff | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-874524c1f2a1 | rejected_opposite_artifact | record-874524c1f2a1 | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-51d930d16c3a | approval_without_target | record-51d930d16c3a | 0 | 0 | contradiction | True | None | None |
| record-1eef212119ba | rejected_opposite_artifact | record-1eef212119ba | 0 | 1 | unchanged_constraints | False | apply | keep |
| record-35188f97aa23 | target_field_preference | record-35188f97aa23 | 1 | 0 | contradiction | True | None | None |
| record-ead2e643f1ab | target_field_preference | record-ead2e643f1ab | 1 | 0 | contradiction | True | None | None |
| record-4ee7b6e8f98f | rejected_opposite_artifact | record-4ee7b6e8f98f | 1 | 0 | contradiction | True | None | None |
| record-07f58aee9c3c | target_field_preference | record-07f58aee9c3c | 0 | 0 | contradiction | True | None | None |
| record-b8f32e66e6bc | unauthorised_revision | record-b8f32e66e6bc | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-c967b4143393 | approval_without_target | record-c967b4143393 | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-a05edcbf8ccf | rejected_opposite_artifact | record-a05edcbf8ccf | 0 | 0 | contradiction | True | None | None |
| record-7a78bbaf249a | rejected_opposite_artifact | record-7a78bbaf249a | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-86f2948918a3 | unauthorised_revision | record-86f2948918a3 | 0 | 0 | contradiction | True | None | None |
| record-5719fe10a847 | unauthorised_revision | record-5719fe10a847 | 0 | 0 | contradiction | True | None | None |
| record-837fb0516311 | unauthorised_revision | record-837fb0516311 | 0 | 0 | contradiction | True | None | None |
| record-69097a1fefd4 | approval_without_target | record-69097a1fefd4 | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-b3a0982e618e | unauthorised_revision | record-b3a0982e618e | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-faccea4248ef | target_field_preference | record-faccea4248ef | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-8b8d9e86fdcb | approval_without_target | record-8b8d9e86fdcb | 0 | 0 | contradiction | True | None | None |
| record-325491c706a4 | target_field_preference | record-325491c706a4 | 0 | 0 | contradiction | True | None | None |
| record-412b8e005a18 | target_field_preference | record-412b8e005a18 | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-123a93d85b3a | rejected_opposite_artifact | record-123a93d85b3a | 1 | 0 | contradiction | True | None | None |
| record-ce75754ce6cb | approval_without_target | record-ce75754ce6cb | 0 | 0 | contradiction | True | None | None |
| record-6c82139e65d5 | rejected_opposite_artifact | record-6c82139e65d5 | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-3bc718860c73 | approval_without_target | record-3bc718860c73 | 1 | 0 | contradiction | True | None | None |
| record-694b03611256 | approval_without_target | record-694b03611256 | 0 | 0 | contradiction | True | None | None |
| record-51379a55fe7b | target_field_preference | record-51379a55fe7b | 0 | 1 | unchanged_constraints | False | apply | keep |
| record-bf7d9be02e76 | approval_without_target | record-bf7d9be02e76 | 0 | 1 | unchanged_constraints | False | apply | keep |
| record-a59387bb2f56 | unauthorised_revision | record-a59387bb2f56 | 0 | 1 | unchanged_constraints | False | apply | keep |
| record-80af99033879 | target_field_preference | record-80af99033879 | 0 | 0 | contradiction | True | None | None |
| record-b73b74fad664 | target_field_preference | record-b73b74fad664 | 1 | 0 | contradiction | True | None | None |
| record-3082091c7641 | rejected_opposite_artifact | record-3082091c7641 | 0 | 0 | contradiction | True | None | None |
| record-2f47a8fbb5c5 | unauthorised_revision | record-2f47a8fbb5c5 | 0 | 1 | unchanged_constraints | False | apply | keep |
| record-603ed31407f7 | unauthorised_revision | record-603ed31407f7 | 0 | 0 | contradiction | True | None | None |
| record-623129cfc74d | unauthorised_revision | record-623129cfc74d | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-c330f8d90d55 | approval_without_target | record-c330f8d90d55 | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-37dabbefcd0b | approval_without_target | record-37dabbefcd0b | 1 | 0 | contradiction | True | None | None |
| record-6a1b2664e5b9 | rejected_opposite_artifact | record-6a1b2664e5b9 | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-3d0e769ddbd3 | unauthorised_revision | record-3d0e769ddbd3 | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-beefd5f66c9a | rejected_opposite_artifact | record-beefd5f66c9a | 0 | 0 | contradiction | True | None | None |
| record-ece5ee6f0778 | approval_without_target | record-ece5ee6f0778 | 0 | 0 | contradiction | True | None | None |
| record-d9f3cbd0155c | approval_without_target | record-d9f3cbd0155c | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-0e4b962f7040 | rejected_opposite_artifact | record-0e4b962f7040 | 0 | 0 | contradiction | True | None | None |
| record-887c32cf23cc | target_field_preference | record-887c32cf23cc | 1 | 0 | contradiction | True | None | None |
| record-094913dcf75e | unauthorised_revision | record-094913dcf75e | 0 | 0 | contradiction | True | None | None |
| record-bdd8ece9528e | target_field_preference | record-bdd8ece9528e | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-63117ba33fff | rejected_opposite_artifact | record-63117ba33fff | 0 | 0 | contradiction | True | None | None |

### Exact promotions, contexts and public value provenance

The [complete JSON sidecar](S2-reporting.json) preserves every intervention under `counterfactual.records`,
including selected field presence/value, effective current context, public origin,
precise promotion and remaining-policy count. No intervention alters the real history.

## Future tasks for this development example

### diagnostic

Public task

```json
{
  "task_id": "task-cd264539067c",
  "context": {
    "task_family": "report_artifact",
    "workflow": "workflow-f978d20c60f7",
    "version": "edition-6c192159bf30",
    "artifact": "numeric_table",
    "audience": "external"
  },
  "facts": {
    "document_id": "DOC-99748",
    "date": "2026-06-15",
    "base_title": "Quarterly allocation 99748",
    "snapshot": "SNAP-99748",
    "source_footnote": "Source: approved extract EX-99748."
  },
  "baseline_fields": [
    {
      "name": "title",
      "value": "Quarterly allocation 99748 | SNAP-99748"
    },
    {
      "name": "source_footnote",
      "value": "Source: approved extract EX-99748."
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Private expected obligations and actual-world fields

```json
{
  "task_id": "task-cd264539067c",
  "history_id": "history-d74e248c70fc",
  "probe": "diagnostic",
  "expected_decision": "apply",
  "recoverable": true,
  "world_fields": [
    {
      "name": "title",
      "value": "Quarterly allocation 99748"
    },
    {
      "name": "source_footnote",
      "value": "Source: approved extract EX-99748."
    }
  ]
}
```

### control

Public task

```json
{
  "task_id": "task-9213ccd1cbb1",
  "context": {
    "task_family": "report_artifact",
    "workflow": "workflow-f978d20c60f7",
    "version": "edition-6c192159bf30",
    "artifact": "chart",
    "audience": "internal"
  },
  "facts": {
    "document_id": "DOC-60251",
    "date": "2026-06-15",
    "base_title": "Quarterly allocation 60251",
    "snapshot": "SNAP-60251",
    "source_footnote": "Source: approved extract EX-60251."
  },
  "baseline_fields": [
    {
      "name": "title",
      "value": "Quarterly allocation 60251 | SNAP-60251"
    },
    {
      "name": "source_footnote",
      "value": "Source: approved extract EX-60251."
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Private expected obligations and actual-world fields

```json
{
  "task_id": "task-9213ccd1cbb1",
  "history_id": "history-d74e248c70fc",
  "probe": "control",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "title",
      "value": "Quarterly allocation 60251 | SNAP-60251"
    },
    {
      "name": "source_footnote",
      "value": "Source: approved extract EX-60251."
    }
  ]
}
```

## Human response

Pending. No approval is inferred from this export.
