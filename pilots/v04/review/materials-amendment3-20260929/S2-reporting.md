# S2 / reporting

Material revision: v04-amendment-03. Synthetic development example.

Registered task type: **transfer_change**. Intended diagnostic regime: **change**.
Public records: 60. Control basis: resolved_keep.

## Review summary

Current compatible functions: **1**. Full cross-version policies: 1.

H14 identification is conditional on excluding XOR and XNOR. Retaining an unresolved
baseline does not establish that the baseline is the true requirement.

| Task | Public context | Previously observed | Warranted action | Retention basis |
| --- | --- | --- | --- | --- |
| diagnostic | task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=internal | False | apply | not_retention |
| control | task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=external | True | keep | resolved |

Counterfactual qualification requires **contradiction** for every present type. All present types qualify: **True**.

One qualifying example per present type is shown below. The links lead to its
public evidence; all records and counts appear in the later audit and JSON sidecar.

| Type (record count) | Promoted record / source | Public target value | Exact promotion | Outcome / remaining policies |
| --- | --- | --- | --- | --- |
| approval_without_target (12) | [record-0b9a5f018b90](#record-0b9a5f018b90) | title = 'Quarterly allocation 23654' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal | contradiction / 0 |
| rejected_opposite_artifact (12) | [record-1459dea8b485](#record-1459dea8b485) | title = 'Quarterly allocation 52063 \| SNAP-52063' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=external | contradiction / 0 |
| target_field_preference (12) | [record-09dadce5dc37](#record-09dadce5dc37) | title = 'Quarterly allocation 37670' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=internal | contradiction / 0 |
| unauthorised_revision (12) | [record-6f89029be48d](#record-6f89029be48d) | title = 'Quarterly allocation 41608' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=external | contradiction / 0 |

An action flip requires a nonempty compatible set and a changed diagnostic or control
action. A contradiction has no compatible policy and supplies neither task action.

[Complete oracle derivation](#oracle-derivation-from-public-evidence) · [Every counterfactual record](#single-record-counterfactual-relevance)

## Public configuration and assumptions

```json
{
  "as_of": "2026-06-15T12:00:00Z",
  "baseline_template": {
    "source_footnote": "{source_footnote}",
    "title": "{base_title}"
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
    "operation": "append_fact",
    "separator": " | ",
    "value": "snapshot"
  },
  "hypothesis_class": "h14",
  "hypothesis_definition": "Each of the two declared binary context dimensions defines a predicate testing its second listed value. Call these predicates x and y. In each registered version the target field configuration is one Boolean function from the following class: constant 0 or 1; x, not x, y, or not y; a conjunction of one literal from each dimension; or a disjunction of one literal from each dimension. Zero selects the configured baseline and one the available alternative. The fourteen distinct truth tables exclude only XOR and XNOR. Each version has its own class member, with no cross-version coupling. This restriction is a supplied synthetic assumption, not an established property of enterprise work.",
  "task_family": "report_artifact",
  "workflow": "workflow-aac8277e4921"
}
```

This is a bounded synthetic workflow model. initial_configuration declares the field options, two context dimensions and the complete H14 hypothesis class. Each registered version has one class member. A field observation constrains the member indexed by its recorded version. Broader consequences follow from the declared class. Facts provide current artifact values. Other fields retain their configured baseline. Outside the declared task_family and workflow, or without a complete declared context, no update is authorised by this model. A register_version event supplies trusted workflow metadata with the authority roster and half-open validity interval. Binding field approval is an event of type review with decision accept, performed by a listed reviewer within that interval, with the field included in reviewed_fields. Its accepted artifact establishes the field configuration at the recorded context. This explicit approval convention is a supplied synthetic assumption. A forward has an origin_ref identifying the record whose content it reproduces. Raw artifacts expose named revisions and a selected artifact reference; interpreted records expose the selected fields directly. A rejection records a whole-artifact decision and its stated grounds. An artifact field whose review is not recorded has no approved assignment. The configured baseline is retained when the available evidence does not establish an update. Dates and version labels in new work identify the applicable registration.

## Public work records

### record-48b0e35e5e93

2026-01-01T00:00:00Z | template | workflow-registry

Context: 


```json
{
  "authorised_reviewers": [
    "Daria",
    "Theo"
  ],
  "event": "register_version",
  "supersedes": null,
  "task_family": "report_artifact",
  "valid_from": "2026-01-01T00:00:00Z",
  "valid_until": "2027-01-01T00:00:00Z",
  "version": "edition-54581174746e",
  "workflow": "workflow-aac8277e4921"
}
```

### record-9242604ce001

2026-06-10T10:00:00Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=external

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-48b0e35e5e93
- comment: Approved.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-36597.",
    "title": "Quarterly allocation 36597"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 36597",
    "before": "Quarterly allocation 36597 | SNAP-36597",
    "field": "title"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-36597",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 36597",
    "date": "2026-06-10",
    "document_id": "DOC-36597",
    "snapshot": "SNAP-36597",
    "source_footnote": "Source: approved extract EX-36597."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-6d0d7889dcb0

2026-06-11T10:00:00Z | review | Theo

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=external

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-48b0e35e5e93
- comment: Approved.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-95626.",
    "title": "Quarterly allocation 95626 | SNAP-95626"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 95626 | SNAP-95626",
    "before": "Quarterly allocation 95626",
    "field": "title"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-95626",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 95626",
    "date": "2026-06-11",
    "document_id": "DOC-95626",
    "snapshot": "SNAP-95626",
    "source_footnote": "Source: approved extract EX-95626."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-4175f9730330

2026-06-12T10:00:00Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-48b0e35e5e93
- comment: Approved.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-74359.",
    "title": "Quarterly allocation 74359 | SNAP-74359"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 74359 | SNAP-74359",
    "before": "Quarterly allocation 74359",
    "field": "title"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-74359",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 74359",
    "date": "2026-06-12",
    "document_id": "DOC-74359",
    "snapshot": "SNAP-74359",
    "source_footnote": "Source: approved extract EX-74359."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-895e86de4e4d

2026-06-14T08:00:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=external


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
  "request_id": "request-7a1d94bc9a15"
}
```

### record-d6c215555881

2026-06-14T08:01:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=external


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
  "request_id": "request-61c069288a42"
}
```

### record-0ea93c09c934

2026-06-14T08:02:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal


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
  "request_id": "request-758d58b36e65"
}
```

### record-5676c943be38

2026-06-14T08:03:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal


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
  "request_id": "request-697c6e2c5b4c"
}
```

### record-9730cfa832fc

2026-06-14T08:04:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal


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
  "request_id": "request-6db5e3f13aee"
}
```

### record-0f788fd2b1f1

2026-06-14T08:05:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=external


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
  "request_id": "request-c42133cf1989"
}
```

### record-7b2ac35e6028

2026-06-14T08:06:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=external


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
  "request_id": "request-9e209ae9d0b9"
}
```

### record-fe55100eda23

2026-06-14T08:07:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal


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
  "request_id": "request-bbefcb6094fe"
}
```

### record-09dadce5dc37

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=internal


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 37670",
    "date": "2026-06-14",
    "document_id": "DOC-37670",
    "snapshot": "SNAP-37670",
    "source_footnote": "Source: approved extract EX-37670."
  },
  "message": "My preference for this work item is that title should be 'Quarterly allocation 37670'.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-37670.",
    "title": "Quarterly allocation 37670"
  }
}
```

### record-0b356356def7

2026-06-14T09:00:00Z | review | Theo

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=internal

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-48b0e35e5e93
- comment: Delivery timestamp approved.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-06-14T08:00:00Z",
    "source_footnote": "Source: approved extract EX-31176.",
    "title": "Quarterly allocation 31176 | SNAP-31176"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 31176 | SNAP-31176",
    "before": "Quarterly allocation 31176",
    "field": "title"
  },
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-31176",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 31176",
    "date": "2026-06-14",
    "document_id": "DOC-31176",
    "snapshot": "SNAP-31176",
    "source_footnote": "Source: approved extract EX-31176."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-0b9a5f018b90

2026-06-14T09:00:00Z | review | Theo

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-48b0e35e5e93
- comment: Delivery timestamp approved.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-06-14T08:00:00Z",
    "source_footnote": "Source: approved extract EX-23654.",
    "title": "Quarterly allocation 23654"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 23654",
    "before": "Quarterly allocation 23654 | SNAP-23654",
    "field": "title"
  },
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-23654",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 23654",
    "date": "2026-06-14",
    "document_id": "DOC-23654",
    "snapshot": "SNAP-23654",
    "source_footnote": "Source: approved extract EX-23654."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-1459dea8b485

2026-06-14T09:00:00Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=external

- decision: reject
- reviewed_fields: []
- authority_ref: record-48b0e35e5e93
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 52063 | SNAP-52063",
    "before": "Quarterly allocation 52063",
    "field": "title"
  },
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-52063",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 52063",
    "date": "2026-06-14",
    "document_id": "DOC-52063",
    "snapshot": "SNAP-52063",
    "source_footnote": "Source: approved extract EX-52063."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-52063.",
    "title": "Quarterly allocation 52063 | SNAP-52063"
  },
  "reviewed_fields": []
}
```

### record-183f49895968

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=external


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 34658",
    "date": "2026-06-14",
    "document_id": "DOC-34658",
    "snapshot": "SNAP-34658",
    "source_footnote": "Source: approved extract EX-34658."
  },
  "message": "My preference for this work item is that title should be 'Quarterly allocation 34658 | SNAP-34658'.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-34658.",
    "title": "Quarterly allocation 34658 | SNAP-34658"
  }
}
```

### record-185f33c091f1

2026-06-14T09:00:00Z | review | Theo

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal

- decision: reject
- reviewed_fields: []
- authority_ref: record-48b0e35e5e93
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 86482 | SNAP-86482",
    "before": "Quarterly allocation 86482",
    "field": "title"
  },
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-86482",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 86482",
    "date": "2026-06-14",
    "document_id": "DOC-86482",
    "snapshot": "SNAP-86482",
    "source_footnote": "Source: approved extract EX-86482."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-86482.",
    "title": "Quarterly allocation 86482 | SNAP-86482"
  },
  "reviewed_fields": []
}
```

### record-198aa7e7d880

2026-06-14T09:00:00Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=external

- decision: reject
- reviewed_fields: []
- authority_ref: record-48b0e35e5e93
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 95564",
    "before": "Quarterly allocation 95564 | SNAP-95564",
    "field": "title"
  },
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-95564",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 95564",
    "date": "2026-06-14",
    "document_id": "DOC-95564",
    "snapshot": "SNAP-95564",
    "source_footnote": "Source: approved extract EX-95564."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-95564.",
    "title": "Quarterly allocation 95564"
  },
  "reviewed_fields": []
}
```

### record-1bd04faf814c

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 44573",
    "date": "2026-06-14",
    "document_id": "DOC-44573",
    "snapshot": "SNAP-44573",
    "source_footnote": "Source: approved extract EX-44573."
  },
  "message": "My preference for this work item is that title should be 'Quarterly allocation 44573 | SNAP-44573'.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-44573.",
    "title": "Quarterly allocation 44573 | SNAP-44573"
  }
}
```

### record-23d55fec2d6f

2026-06-14T09:00:00Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=internal

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-48b0e35e5e93
- comment: Delivery timestamp approved.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-06-14T08:00:00Z",
    "source_footnote": "Source: approved extract EX-54243.",
    "title": "Quarterly allocation 54243 | SNAP-54243"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 54243 | SNAP-54243",
    "before": "Quarterly allocation 54243",
    "field": "title"
  },
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-54243",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 54243",
    "date": "2026-06-14",
    "document_id": "DOC-54243",
    "snapshot": "SNAP-54243",
    "source_footnote": "Source: approved extract EX-54243."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-28aa165e1825

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=external


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 65455",
    "date": "2026-06-14",
    "document_id": "DOC-65455",
    "snapshot": "SNAP-65455",
    "source_footnote": "Source: approved extract EX-65455."
  },
  "message": "My preference for this work item is that title should be 'Quarterly allocation 65455 | SNAP-65455'.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-65455.",
    "title": "Quarterly allocation 65455 | SNAP-65455"
  }
}
```

### record-2dcda272d52f

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 64498",
    "date": "2026-06-14",
    "document_id": "DOC-64498",
    "snapshot": "SNAP-64498",
    "source_footnote": "Source: approved extract EX-64498."
  },
  "message": "My preference for this work item is that title should be 'Quarterly allocation 64498'.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-64498.",
    "title": "Quarterly allocation 64498"
  }
}
```

### record-387715763c3b

2026-06-14T09:00:00Z | review | Theo

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=internal

- decision: reject
- reviewed_fields: []
- authority_ref: record-48b0e35e5e93
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 19418 | SNAP-19418",
    "before": "Quarterly allocation 19418",
    "field": "title"
  },
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-19418",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 19418",
    "date": "2026-06-14",
    "document_id": "DOC-19418",
    "snapshot": "SNAP-19418",
    "source_footnote": "Source: approved extract EX-19418."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-19418.",
    "title": "Quarterly allocation 19418 | SNAP-19418"
  },
  "reviewed_fields": []
}
```

### record-45705df6944d

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-48b0e35e5e93
- comment: Updated the proposed export.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-15807.",
    "title": "Quarterly allocation 15807 | SNAP-15807"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 15807 | SNAP-15807",
    "before": "Quarterly allocation 15807",
    "field": "title"
  },
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-15807",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 15807",
    "date": "2026-06-14",
    "document_id": "DOC-15807",
    "snapshot": "SNAP-15807",
    "source_footnote": "Source: approved extract EX-15807."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-48030188ed80

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 29173",
    "date": "2026-06-14",
    "document_id": "DOC-29173",
    "snapshot": "SNAP-29173",
    "source_footnote": "Source: approved extract EX-29173."
  },
  "message": "My preference for this work item is that title should be 'Quarterly allocation 29173'.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-29173.",
    "title": "Quarterly allocation 29173"
  }
}
```

### record-4a83f32d69d8

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=external

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-48b0e35e5e93
- comment: Updated the proposed export.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-75869.",
    "title": "Quarterly allocation 75869 | SNAP-75869"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 75869 | SNAP-75869",
    "before": "Quarterly allocation 75869",
    "field": "title"
  },
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-75869",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 75869",
    "date": "2026-06-14",
    "document_id": "DOC-75869",
    "snapshot": "SNAP-75869",
    "source_footnote": "Source: approved extract EX-75869."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-4bbc0eb0bed9

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-48b0e35e5e93
- comment: Updated the proposed export.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-86739.",
    "title": "Quarterly allocation 86739 | SNAP-86739"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 86739 | SNAP-86739",
    "before": "Quarterly allocation 86739",
    "field": "title"
  },
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-86739",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 86739",
    "date": "2026-06-14",
    "document_id": "DOC-86739",
    "snapshot": "SNAP-86739",
    "source_footnote": "Source: approved extract EX-86739."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-597d4fb1a9ef

2026-06-14T09:00:00Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=external

- decision: reject
- reviewed_fields: []
- authority_ref: record-48b0e35e5e93
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 36236",
    "before": "Quarterly allocation 36236 | SNAP-36236",
    "field": "title"
  },
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-36236",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 36236",
    "date": "2026-06-14",
    "document_id": "DOC-36236",
    "snapshot": "SNAP-36236",
    "source_footnote": "Source: approved extract EX-36236."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-36236.",
    "title": "Quarterly allocation 36236"
  },
  "reviewed_fields": []
}
```

### record-5a91ed37c72b

2026-06-14T09:00:00Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=external

- decision: reject
- reviewed_fields: []
- authority_ref: record-48b0e35e5e93
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 64768 | SNAP-64768",
    "before": "Quarterly allocation 64768",
    "field": "title"
  },
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-64768",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 64768",
    "date": "2026-06-14",
    "document_id": "DOC-64768",
    "snapshot": "SNAP-64768",
    "source_footnote": "Source: approved extract EX-64768."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-64768.",
    "title": "Quarterly allocation 64768 | SNAP-64768"
  },
  "reviewed_fields": []
}
```

### record-5b9ecede47c6

2026-06-14T09:00:00Z | review | Theo

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal

- decision: reject
- reviewed_fields: []
- authority_ref: record-48b0e35e5e93
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 76294 | SNAP-76294",
    "before": "Quarterly allocation 76294",
    "field": "title"
  },
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-76294",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 76294",
    "date": "2026-06-14",
    "document_id": "DOC-76294",
    "snapshot": "SNAP-76294",
    "source_footnote": "Source: approved extract EX-76294."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-76294.",
    "title": "Quarterly allocation 76294 | SNAP-76294"
  },
  "reviewed_fields": []
}
```

### record-5cb1f69e1316

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=external

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-48b0e35e5e93
- comment: Updated the proposed export.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-89199.",
    "title": "Quarterly allocation 89199 | SNAP-89199"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 89199 | SNAP-89199",
    "before": "Quarterly allocation 89199",
    "field": "title"
  },
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-89199",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 89199",
    "date": "2026-06-14",
    "document_id": "DOC-89199",
    "snapshot": "SNAP-89199",
    "source_footnote": "Source: approved extract EX-89199."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-626b29752f35

2026-06-14T09:00:00Z | review | Theo

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=external

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-48b0e35e5e93
- comment: Delivery timestamp approved.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-06-14T08:00:00Z",
    "source_footnote": "Source: approved extract EX-55176.",
    "title": "Quarterly allocation 55176"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 55176",
    "before": "Quarterly allocation 55176 | SNAP-55176",
    "field": "title"
  },
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-55176",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 55176",
    "date": "2026-06-14",
    "document_id": "DOC-55176",
    "snapshot": "SNAP-55176",
    "source_footnote": "Source: approved extract EX-55176."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-6be871b6a7ff

2026-06-14T09:00:00Z | review | Theo

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=external

- decision: reject
- reviewed_fields: []
- authority_ref: record-48b0e35e5e93
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 69246",
    "before": "Quarterly allocation 69246 | SNAP-69246",
    "field": "title"
  },
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-69246",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 69246",
    "date": "2026-06-14",
    "document_id": "DOC-69246",
    "snapshot": "SNAP-69246",
    "source_footnote": "Source: approved extract EX-69246."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-69246.",
    "title": "Quarterly allocation 69246"
  },
  "reviewed_fields": []
}
```

### record-6f89029be48d

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=external

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-48b0e35e5e93
- comment: Updated the proposed export.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-41608.",
    "title": "Quarterly allocation 41608"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 41608",
    "before": "Quarterly allocation 41608 | SNAP-41608",
    "field": "title"
  },
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-41608",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 41608",
    "date": "2026-06-14",
    "document_id": "DOC-41608",
    "snapshot": "SNAP-41608",
    "source_footnote": "Source: approved extract EX-41608."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-8f8d06503a4e

2026-06-14T09:00:00Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal

- decision: reject
- reviewed_fields: []
- authority_ref: record-48b0e35e5e93
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 95178",
    "before": "Quarterly allocation 95178 | SNAP-95178",
    "field": "title"
  },
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-95178",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 95178",
    "date": "2026-06-14",
    "document_id": "DOC-95178",
    "snapshot": "SNAP-95178",
    "source_footnote": "Source: approved extract EX-95178."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-95178.",
    "title": "Quarterly allocation 95178"
  },
  "reviewed_fields": []
}
```

### record-924d3967d941

2026-06-14T09:00:00Z | review | Theo

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=external

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-48b0e35e5e93
- comment: Delivery timestamp approved.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-06-14T08:00:00Z",
    "source_footnote": "Source: approved extract EX-82681.",
    "title": "Quarterly allocation 82681"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 82681",
    "before": "Quarterly allocation 82681 | SNAP-82681",
    "field": "title"
  },
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-82681",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 82681",
    "date": "2026-06-14",
    "document_id": "DOC-82681",
    "snapshot": "SNAP-82681",
    "source_footnote": "Source: approved extract EX-82681."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-96832f9f78bd

2026-06-14T09:00:00Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=internal

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-48b0e35e5e93
- comment: Delivery timestamp approved.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-06-14T08:00:00Z",
    "source_footnote": "Source: approved extract EX-37142.",
    "title": "Quarterly allocation 37142"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 37142",
    "before": "Quarterly allocation 37142 | SNAP-37142",
    "field": "title"
  },
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-37142",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 37142",
    "date": "2026-06-14",
    "document_id": "DOC-37142",
    "snapshot": "SNAP-37142",
    "source_footnote": "Source: approved extract EX-37142."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-9bbde8c7e837

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-48b0e35e5e93
- comment: Updated the proposed export.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-83652.",
    "title": "Quarterly allocation 83652 | SNAP-83652"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 83652 | SNAP-83652",
    "before": "Quarterly allocation 83652",
    "field": "title"
  },
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-83652",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 83652",
    "date": "2026-06-14",
    "document_id": "DOC-83652",
    "snapshot": "SNAP-83652",
    "source_footnote": "Source: approved extract EX-83652."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-acb0f3435588

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-48b0e35e5e93
- comment: Updated the proposed export.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-71941.",
    "title": "Quarterly allocation 71941 | SNAP-71941"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 71941 | SNAP-71941",
    "before": "Quarterly allocation 71941",
    "field": "title"
  },
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-71941",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 71941",
    "date": "2026-06-14",
    "document_id": "DOC-71941",
    "snapshot": "SNAP-71941",
    "source_footnote": "Source: approved extract EX-71941."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-ad2fcd2f8810

2026-06-14T09:00:00Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal

- decision: reject
- reviewed_fields: []
- authority_ref: record-48b0e35e5e93
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 26668",
    "before": "Quarterly allocation 26668 | SNAP-26668",
    "field": "title"
  },
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-26668",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 26668",
    "date": "2026-06-14",
    "document_id": "DOC-26668",
    "snapshot": "SNAP-26668",
    "source_footnote": "Source: approved extract EX-26668."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-26668.",
    "title": "Quarterly allocation 26668"
  },
  "reviewed_fields": []
}
```

### record-ae776e17f4ec

2026-06-14T09:00:00Z | review | Theo

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=external

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-48b0e35e5e93
- comment: Delivery timestamp approved.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-06-14T08:00:00Z",
    "source_footnote": "Source: approved extract EX-11099.",
    "title": "Quarterly allocation 11099 | SNAP-11099"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 11099 | SNAP-11099",
    "before": "Quarterly allocation 11099",
    "field": "title"
  },
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-11099",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 11099",
    "date": "2026-06-14",
    "document_id": "DOC-11099",
    "snapshot": "SNAP-11099",
    "source_footnote": "Source: approved extract EX-11099."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-b4aa76ee799b

2026-06-14T09:00:00Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=external

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-48b0e35e5e93
- comment: Delivery timestamp approved.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-06-14T08:00:00Z",
    "source_footnote": "Source: approved extract EX-44843.",
    "title": "Quarterly allocation 44843 | SNAP-44843"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 44843 | SNAP-44843",
    "before": "Quarterly allocation 44843",
    "field": "title"
  },
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-44843",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 44843",
    "date": "2026-06-14",
    "document_id": "DOC-44843",
    "snapshot": "SNAP-44843",
    "source_footnote": "Source: approved extract EX-44843."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-bcba8b9e7759

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-48b0e35e5e93
- comment: Updated the proposed export.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-58695.",
    "title": "Quarterly allocation 58695"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 58695",
    "before": "Quarterly allocation 58695 | SNAP-58695",
    "field": "title"
  },
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-58695",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 58695",
    "date": "2026-06-14",
    "document_id": "DOC-58695",
    "snapshot": "SNAP-58695",
    "source_footnote": "Source: approved extract EX-58695."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-bd2d292b7b1c

2026-06-14T09:00:00Z | review | Theo

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=external

- decision: reject
- reviewed_fields: []
- authority_ref: record-48b0e35e5e93
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 24602 | SNAP-24602",
    "before": "Quarterly allocation 24602",
    "field": "title"
  },
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-24602",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 24602",
    "date": "2026-06-14",
    "document_id": "DOC-24602",
    "snapshot": "SNAP-24602",
    "source_footnote": "Source: approved extract EX-24602."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-24602.",
    "title": "Quarterly allocation 24602 | SNAP-24602"
  },
  "reviewed_fields": []
}
```

### record-c4bac97e4eb3

2026-06-14T09:00:00Z | review | Theo

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=external

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-48b0e35e5e93
- comment: Delivery timestamp approved.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-06-14T08:00:00Z",
    "source_footnote": "Source: approved extract EX-49387.",
    "title": "Quarterly allocation 49387"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 49387",
    "before": "Quarterly allocation 49387 | SNAP-49387",
    "field": "title"
  },
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-49387",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 49387",
    "date": "2026-06-14",
    "document_id": "DOC-49387",
    "snapshot": "SNAP-49387",
    "source_footnote": "Source: approved extract EX-49387."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-c4f68d10211d

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=external


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 68323",
    "date": "2026-06-14",
    "document_id": "DOC-68323",
    "snapshot": "SNAP-68323",
    "source_footnote": "Source: approved extract EX-68323."
  },
  "message": "My preference for this work item is that title should be 'Quarterly allocation 68323'.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-68323.",
    "title": "Quarterly allocation 68323"
  }
}
```

### record-d5d39a1d0c82

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 29514",
    "date": "2026-06-14",
    "document_id": "DOC-29514",
    "snapshot": "SNAP-29514",
    "source_footnote": "Source: approved extract EX-29514."
  },
  "message": "My preference for this work item is that title should be 'Quarterly allocation 29514 | SNAP-29514'.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-29514.",
    "title": "Quarterly allocation 29514 | SNAP-29514"
  }
}
```

### record-d82dd258623d

2026-06-14T09:00:00Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-48b0e35e5e93
- comment: Delivery timestamp approved.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-06-14T08:00:00Z",
    "source_footnote": "Source: approved extract EX-74240.",
    "title": "Quarterly allocation 74240 | SNAP-74240"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 74240 | SNAP-74240",
    "before": "Quarterly allocation 74240",
    "field": "title"
  },
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-74240",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 74240",
    "date": "2026-06-14",
    "document_id": "DOC-74240",
    "snapshot": "SNAP-74240",
    "source_footnote": "Source: approved extract EX-74240."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-dd85b3b8b42e

2026-06-14T09:00:00Z | review | Theo

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal

- decision: reject
- reviewed_fields: []
- authority_ref: record-48b0e35e5e93
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 12354 | SNAP-12354",
    "before": "Quarterly allocation 12354",
    "field": "title"
  },
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-12354",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 12354",
    "date": "2026-06-14",
    "document_id": "DOC-12354",
    "snapshot": "SNAP-12354",
    "source_footnote": "Source: approved extract EX-12354."
  },
  "format": "interpreted",
  "rejected_fields": {
    "source_footnote": "Source: approved extract EX-12354.",
    "title": "Quarterly allocation 12354 | SNAP-12354"
  },
  "reviewed_fields": []
}
```

### record-de0743454f80

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=external


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 31886",
    "date": "2026-06-14",
    "document_id": "DOC-31886",
    "snapshot": "SNAP-31886",
    "source_footnote": "Source: approved extract EX-31886."
  },
  "message": "My preference for this work item is that title should be 'Quarterly allocation 31886'.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-31886.",
    "title": "Quarterly allocation 31886"
  }
}
```

### record-df1e4e428275

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 42112",
    "date": "2026-06-14",
    "document_id": "DOC-42112",
    "snapshot": "SNAP-42112",
    "source_footnote": "Source: approved extract EX-42112."
  },
  "message": "My preference for this work item is that title should be 'Quarterly allocation 42112 | SNAP-42112'.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-42112.",
    "title": "Quarterly allocation 42112 | SNAP-42112"
  }
}
```

### record-df6eca99ebee

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=external

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-48b0e35e5e93
- comment: Updated the proposed export.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-37162.",
    "title": "Quarterly allocation 37162"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 37162",
    "before": "Quarterly allocation 37162 | SNAP-37162",
    "field": "title"
  },
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-37162",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 37162",
    "date": "2026-06-14",
    "document_id": "DOC-37162",
    "snapshot": "SNAP-37162",
    "source_footnote": "Source: approved extract EX-37162."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-e4d0c6535827

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-48b0e35e5e93
- comment: Updated the proposed export.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-43501.",
    "title": "Quarterly allocation 43501"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 43501",
    "before": "Quarterly allocation 43501 | SNAP-43501",
    "field": "title"
  },
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-43501",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 43501",
    "date": "2026-06-14",
    "document_id": "DOC-43501",
    "snapshot": "SNAP-43501",
    "source_footnote": "Source: approved extract EX-43501."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-e6da9c5ffcc3

2026-06-14T09:00:00Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=external

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-48b0e35e5e93
- comment: Delivery timestamp approved.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-06-14T08:00:00Z",
    "source_footnote": "Source: approved extract EX-54082.",
    "title": "Quarterly allocation 54082"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 54082",
    "before": "Quarterly allocation 54082 | SNAP-54082",
    "field": "title"
  },
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-54082",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 54082",
    "date": "2026-06-14",
    "document_id": "DOC-54082",
    "snapshot": "SNAP-54082",
    "source_footnote": "Source: approved extract EX-54082."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-e8d593b4c3cb

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=external

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-48b0e35e5e93
- comment: Updated the proposed export.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-89245.",
    "title": "Quarterly allocation 89245"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 89245",
    "before": "Quarterly allocation 89245 | SNAP-89245",
    "field": "title"
  },
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-89245",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 89245",
    "date": "2026-06-14",
    "document_id": "DOC-89245",
    "snapshot": "SNAP-89245",
    "source_footnote": "Source: approved extract EX-89245."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-efe0bc45aa55

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=internal


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 86279",
    "date": "2026-06-14",
    "document_id": "DOC-86279",
    "snapshot": "SNAP-86279",
    "source_footnote": "Source: approved extract EX-86279."
  },
  "message": "My preference for this work item is that title should be 'Quarterly allocation 86279 | SNAP-86279'.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-86279.",
    "title": "Quarterly allocation 86279 | SNAP-86279"
  }
}
```

### record-f25d3a64db6b

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=external

- decision: accept
- reviewed_fields: ['title']
- authority_ref: record-48b0e35e5e93
- comment: Updated the proposed export.

```json
{
  "accepted_fields": {
    "source_footnote": "Source: approved extract EX-14686.",
    "title": "Quarterly allocation 14686 | SNAP-14686"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 14686 | SNAP-14686",
    "before": "Quarterly allocation 14686",
    "field": "title"
  },
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-14686",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 14686",
    "date": "2026-06-14",
    "document_id": "DOC-14686",
    "snapshot": "SNAP-14686",
    "source_footnote": "Source: approved extract EX-14686."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "title"
  ]
}
```

### record-fa48ce8311f5

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=internal


```json
{
  "event": "preference",
  "facts": {
    "base_title": "Quarterly allocation 70679",
    "date": "2026-06-14",
    "document_id": "DOC-70679",
    "snapshot": "SNAP-70679",
    "source_footnote": "Source: approved extract EX-70679."
  },
  "message": "My preference for this work item is that title should be 'Quarterly allocation 70679 | SNAP-70679'.",
  "proposed_fields": {
    "source_footnote": "Source: approved extract EX-70679.",
    "title": "Quarterly allocation 70679 | SNAP-70679"
  }
}
```

### record-ffa304e07288

2026-06-14T09:00:00Z | review | Daria

Context: task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-48b0e35e5e93
- comment: Delivery timestamp approved.

```json
{
  "accepted_fields": {
    "delivery_timestamp": "2026-06-14T08:00:00Z",
    "source_footnote": "Source: approved extract EX-89018.",
    "title": "Quarterly allocation 89018 | SNAP-89018"
  },
  "authority_ref": "record-48b0e35e5e93",
  "change_summary": {
    "after": "Quarterly allocation 89018 | SNAP-89018",
    "before": "Quarterly allocation 89018",
    "field": "title"
  },
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-89018",
  "event": "review",
  "facts": {
    "base_title": "Quarterly allocation 89018",
    "date": "2026-06-14",
    "document_id": "DOC-89018",
    "snapshot": "SNAP-89018",
    "source_footnote": "Source: approved extract EX-89018."
  },
  "format": "interpreted",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
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
| record-9242604ce001 | edition-54581174746e | task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=external | 0 |
| record-6d0d7889dcb0 | edition-54581174746e | task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=numeric_table, audience=external | 1 |
| record-4175f9730330 | edition-54581174746e | task_family=report_artifact, workflow=workflow-aac8277e4921, version=edition-54581174746e, artifact=chart, audience=internal | 1 |

### Competing requirement explanations

Zero is the configured baseline; one is the alternative. Each row is a distinct
compatible function for this version. No preference for simplicity removes a row.
The private sampling plan and world policy do not filter these explanations.

Version edition-54581174746e: 1 compatible functions.

| Function | artifact=chart, audience=internal | artifact=chart, audience=external | artifact=numeric_table, audience=internal | artifact=numeric_table, audience=external | Complexity |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 1 | 0 | 1 | 1 | 2 |

### Diagnostic and control derivations

| Task | Context observed | Witnesses | Action | Retention basis |
| --- | --- | --- | --- | --- |
| diagnostic | False | none | apply | not_retention |
| control | True | record-9242604ce001 | keep | resolved |

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
      "audience": "external",
      "task_family": "report_artifact",
      "version": "edition-54581174746e",
      "workflow": "workflow-aac8277e4921"
    },
    {
      "artifact": "numeric_table",
      "audience": "external",
      "task_family": "report_artifact",
      "version": "edition-54581174746e",
      "workflow": "workflow-aac8277e4921"
    },
    {
      "artifact": "chart",
      "audience": "internal",
      "task_family": "report_artifact",
      "version": "edition-54581174746e",
      "workflow": "workflow-aac8277e4921"
    }
  ],
  "diagnostic_observed": false,
  "material_revision": "v04-amendment-03",
  "record_count": 60,
  "registered_versions": [
    "edition-54581174746e"
  ],
  "rendering": "interpreted",
  "reversed_option": false,
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
| approval_without_target | 12 | 0 | 5 | 7 | 0 | 0 | 0 | record-0b9a5f018b90, record-96832f9f78bd, record-ae776e17f4ec, record-b4aa76ee799b, record-e6da9c5ffcc3 |
| rejected_opposite_artifact | 12 | 0 | 7 | 5 | 0 | 0 | 0 | record-1459dea8b485, record-198aa7e7d880, record-597d4fb1a9ef, record-5a91ed37c72b, record-6be871b6a7ff, record-8f8d06503a4e, record-ad2fcd2f8810 |
| target_field_preference | 12 | 0 | 6 | 6 | 0 | 0 | 0 | record-09dadce5dc37, record-183f49895968, record-28aa165e1825, record-2dcda272d52f, record-48030188ed80, record-c4f68d10211d |
| unauthorised_revision | 12 | 0 | 6 | 6 | 0 | 0 | 0 | record-6f89029be48d, record-bcba8b9e7759, record-df6eca99ebee, record-e4d0c6535827, record-e8d593b4c3cb, record-f25d3a64db6b |

### Every promoted public record

| Record | Type | Origin | Public option | Remaining policies | Outcome | Qualifies | Diagnostic action | Control action |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| record-09dadce5dc37 | target_field_preference | record-09dadce5dc37 | 0 | 0 | contradiction | True | None | None |
| record-0b356356def7 | approval_without_target | record-0b356356def7 | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-0b9a5f018b90 | approval_without_target | record-0b9a5f018b90 | 0 | 0 | contradiction | True | None | None |
| record-1459dea8b485 | rejected_opposite_artifact | record-1459dea8b485 | 1 | 0 | contradiction | True | None | None |
| record-183f49895968 | target_field_preference | record-183f49895968 | 1 | 0 | contradiction | True | None | None |
| record-185f33c091f1 | rejected_opposite_artifact | record-185f33c091f1 | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-198aa7e7d880 | rejected_opposite_artifact | record-198aa7e7d880 | 0 | 0 | contradiction | True | None | None |
| record-1bd04faf814c | target_field_preference | record-1bd04faf814c | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-23d55fec2d6f | approval_without_target | record-23d55fec2d6f | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-28aa165e1825 | target_field_preference | record-28aa165e1825 | 1 | 0 | contradiction | True | None | None |
| record-2dcda272d52f | target_field_preference | record-2dcda272d52f | 0 | 0 | contradiction | True | None | None |
| record-387715763c3b | rejected_opposite_artifact | record-387715763c3b | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-45705df6944d | unauthorised_revision | record-45705df6944d | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-48030188ed80 | target_field_preference | record-48030188ed80 | 0 | 0 | contradiction | True | None | None |
| record-4a83f32d69d8 | unauthorised_revision | record-4a83f32d69d8 | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-4bbc0eb0bed9 | unauthorised_revision | record-4bbc0eb0bed9 | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-597d4fb1a9ef | rejected_opposite_artifact | record-597d4fb1a9ef | 0 | 0 | contradiction | True | None | None |
| record-5a91ed37c72b | rejected_opposite_artifact | record-5a91ed37c72b | 1 | 0 | contradiction | True | None | None |
| record-5b9ecede47c6 | rejected_opposite_artifact | record-5b9ecede47c6 | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-5cb1f69e1316 | unauthorised_revision | record-5cb1f69e1316 | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-626b29752f35 | approval_without_target | record-626b29752f35 | 0 | 1 | unchanged_constraints | False | apply | keep |
| record-6be871b6a7ff | rejected_opposite_artifact | record-6be871b6a7ff | 0 | 0 | contradiction | True | None | None |
| record-6f89029be48d | unauthorised_revision | record-6f89029be48d | 0 | 0 | contradiction | True | None | None |
| record-8f8d06503a4e | rejected_opposite_artifact | record-8f8d06503a4e | 0 | 0 | contradiction | True | None | None |
| record-924d3967d941 | approval_without_target | record-924d3967d941 | 0 | 1 | unchanged_constraints | False | apply | keep |
| record-96832f9f78bd | approval_without_target | record-96832f9f78bd | 0 | 0 | contradiction | True | None | None |
| record-9bbde8c7e837 | unauthorised_revision | record-9bbde8c7e837 | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-acb0f3435588 | unauthorised_revision | record-acb0f3435588 | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-ad2fcd2f8810 | rejected_opposite_artifact | record-ad2fcd2f8810 | 0 | 0 | contradiction | True | None | None |
| record-ae776e17f4ec | approval_without_target | record-ae776e17f4ec | 1 | 0 | contradiction | True | None | None |
| record-b4aa76ee799b | approval_without_target | record-b4aa76ee799b | 1 | 0 | contradiction | True | None | None |
| record-bcba8b9e7759 | unauthorised_revision | record-bcba8b9e7759 | 0 | 0 | contradiction | True | None | None |
| record-bd2d292b7b1c | rejected_opposite_artifact | record-bd2d292b7b1c | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-c4bac97e4eb3 | approval_without_target | record-c4bac97e4eb3 | 0 | 1 | unchanged_constraints | False | apply | keep |
| record-c4f68d10211d | target_field_preference | record-c4f68d10211d | 0 | 0 | contradiction | True | None | None |
| record-d5d39a1d0c82 | target_field_preference | record-d5d39a1d0c82 | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-d82dd258623d | approval_without_target | record-d82dd258623d | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-dd85b3b8b42e | rejected_opposite_artifact | record-dd85b3b8b42e | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-de0743454f80 | target_field_preference | record-de0743454f80 | 0 | 1 | unchanged_constraints | False | apply | keep |
| record-df1e4e428275 | target_field_preference | record-df1e4e428275 | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-df6eca99ebee | unauthorised_revision | record-df6eca99ebee | 0 | 0 | contradiction | True | None | None |
| record-e4d0c6535827 | unauthorised_revision | record-e4d0c6535827 | 0 | 0 | contradiction | True | None | None |
| record-e6da9c5ffcc3 | approval_without_target | record-e6da9c5ffcc3 | 0 | 0 | contradiction | True | None | None |
| record-e8d593b4c3cb | unauthorised_revision | record-e8d593b4c3cb | 0 | 0 | contradiction | True | None | None |
| record-efe0bc45aa55 | target_field_preference | record-efe0bc45aa55 | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-f25d3a64db6b | unauthorised_revision | record-f25d3a64db6b | 1 | 0 | contradiction | True | None | None |
| record-fa48ce8311f5 | target_field_preference | record-fa48ce8311f5 | 1 | 1 | unchanged_constraints | False | apply | keep |
| record-ffa304e07288 | approval_without_target | record-ffa304e07288 | 1 | 1 | unchanged_constraints | False | apply | keep |

### Exact promotions, contexts and public value provenance

The [complete JSON sidecar](S2-reporting.json) preserves every intervention under `counterfactual.records`,
including selected field presence/value, effective current context, public origin,
precise promotion and remaining-policy count. No intervention alters the real history.

## Future tasks for this development example

### diagnostic

Public task

```json
{
  "task_id": "task-3feed7ec8ea4",
  "context": {
    "task_family": "report_artifact",
    "workflow": "workflow-aac8277e4921",
    "version": "edition-54581174746e",
    "artifact": "numeric_table",
    "audience": "internal"
  },
  "facts": {
    "document_id": "DOC-39339",
    "date": "2026-06-15",
    "base_title": "Quarterly allocation 39339",
    "snapshot": "SNAP-39339",
    "source_footnote": "Source: approved extract EX-39339."
  },
  "baseline_fields": [
    {
      "name": "title",
      "value": "Quarterly allocation 39339"
    },
    {
      "name": "source_footnote",
      "value": "Source: approved extract EX-39339."
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Private expected obligations and actual-world fields

```json
{
  "task_id": "task-3feed7ec8ea4",
  "history_id": "history-2f61d9ac5236",
  "probe": "diagnostic",
  "expected_decision": "apply",
  "recoverable": true,
  "world_fields": [
    {
      "name": "title",
      "value": "Quarterly allocation 39339 | SNAP-39339"
    },
    {
      "name": "source_footnote",
      "value": "Source: approved extract EX-39339."
    }
  ]
}
```

### control

Public task

```json
{
  "task_id": "task-9965158902b8",
  "context": {
    "task_family": "report_artifact",
    "workflow": "workflow-aac8277e4921",
    "version": "edition-54581174746e",
    "artifact": "chart",
    "audience": "external"
  },
  "facts": {
    "document_id": "DOC-74821",
    "date": "2026-06-15",
    "base_title": "Quarterly allocation 74821",
    "snapshot": "SNAP-74821",
    "source_footnote": "Source: approved extract EX-74821."
  },
  "baseline_fields": [
    {
      "name": "title",
      "value": "Quarterly allocation 74821"
    },
    {
      "name": "source_footnote",
      "value": "Source: approved extract EX-74821."
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Private expected obligations and actual-world fields

```json
{
  "task_id": "task-9965158902b8",
  "history_id": "history-2f61d9ac5236",
  "probe": "control",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "title",
      "value": "Quarterly allocation 74821"
    },
    {
      "name": "source_footnote",
      "value": "Source: approved extract EX-74821."
    }
  ]
}
```

## Human response

Pending. No approval is inferred from this export.
