# S5 / retrieval

Material revision: v04-amendment-03-r2. Synthetic development example.

[Frozen surface-selector audit](surface-audit.md) · [Complete audit JSON](surface-audit.json).
Its per-history results use this case’s history ID; selector choice used only separate development histories.

Registered task type: **transfer_change**. Intended diagnostic regime: **change**.
Public records: 60. Control basis: resolved_keep.

## Review summary

Current compatible functions: **1**. Full cross-version policies: 7.

H14 identification is conditional on excluding XOR and XNOR. Retaining an unresolved
baseline does not establish that the baseline is the true requirement.

| Task | Public context | Previously observed | Warranted action | Retention basis |
| --- | --- | --- | --- | --- |
| diagnostic | task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=assay_report | False | apply | not_retention |
| control | task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=protocol | True | keep | resolved |

Counterfactual qualification requires **contradiction** for every present type. All present types qualify: **True**.

One qualifying example per present type is shown below. The links lead to its
public evidence; all records and counts appear in the later audit and JSON sidecar.

| Type (record count) | Promoted record / source | Public target value | Exact promotion | Outcome / remaining policies |
| --- | --- | --- | --- | --- |
| approval_without_target (10) | [record-655fdac148de](#record-655fdac148de) | source_route = 'index-e07c29' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol | contradiction / 0 |
| forward (8) | [record-b6f43115ba0a](#record-b6f43115ba0a) / [record-7977928eea21](#record-7977928eea21) | source_route = 'index-e07c29' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol | contradiction / 0 |
| old_approval (1) | [record-ff8d3de131aa](#record-ff8d3de131aa) | source_route = 'index-e07c29' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol | contradiction / 0 |
| rejected_opposite_artifact (10) | [record-2527abbf4c9c](#record-2527abbf4c9c) | source_route = 'index-b6f72d' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=protocol | contradiction / 0 |
| target_field_preference (10) | [record-55d5909b7725](#record-55d5909b7725) | source_route = 'index-b6f72d' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=protocol | contradiction / 0 |
| unauthorised_revision (10) | [record-dbedb0c49248](#record-dbedb0c49248) | source_route = 'index-e07c29' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=assay_report | contradiction / 0 |

An action flip requires a nonempty compatible set and a changed diagnostic or control
action. A contradiction has no compatible policy and supplies neither task action.

[Complete oracle derivation](#oracle-derivation-from-public-evidence) · [Every counterfactual record](#single-record-counterfactual-relevance)

## Public configuration and assumptions

```json
{
  "as_of": "2026-06-15T12:00:00Z",
  "baseline_template": {
    "checksum_check": "required",
    "release_id": "{release_id}",
    "source_route": "{configured_route}"
  },
  "dimensions": {
    "collection": [
      "active",
      "archive"
    ],
    "document_class": [
      "protocol",
      "assay_report"
    ]
  },
  "fact_descriptions": {
    "alternative_route": "The other available endpoint.",
    "checksum_check": "The exact canonical marker required means verify the retrieved checksum.",
    "configured_route": "Endpoint selected by the initial configuration.",
    "release_id": "Requested release."
  },
  "field_option": {
    "field": "source_route",
    "operation": "set_fact",
    "separator": "",
    "value": "alternative_route"
  },
  "hypothesis_class": "h14",
  "hypothesis_definition": "Each of the two declared binary context dimensions defines a predicate testing its second listed value. Call these predicates x and y. In each registered version the target field configuration is one Boolean function from the following class: constant 0 or 1; x, not x, y, or not y; a conjunction of one literal from each dimension; or a disjunction of one literal from each dimension. Zero selects the configured baseline and one the available alternative. The fourteen distinct truth tables exclude only XOR and XNOR. Each version has its own class member, with no cross-version coupling. This restriction is a supplied synthetic assumption, not an established property of enterprise work.",
  "task_family": "document_retrieval",
  "workflow": "workflow-e07c29b6f72d"
}
```

This is a bounded synthetic workflow model. initial_configuration declares the field options, two context dimensions and the complete H14 hypothesis class. Each registered version has one class member. A field observation constrains the member indexed by its recorded version. Broader consequences follow from the declared class. Facts provide current artifact values. Other fields retain their configured baseline. Outside the declared task_family and workflow, or without a complete declared context, no update is authorised by this model. A register_version event supplies trusted workflow metadata with the authority roster and half-open validity interval. Binding field approval is an event of type review with decision accept, performed by a listed reviewer within that interval, with the field included in reviewed_fields. Its accepted artifact establishes the field configuration at the recorded context. This explicit approval convention is a supplied synthetic assumption. A forward has an origin_ref identifying the record whose content it reproduces. Raw artifacts expose named revisions and a selected artifact reference; interpreted records expose the selected fields directly. A rejection records a whole-artifact decision and its stated grounds. An artifact field whose review is not recorded has no approved assignment. The configured baseline is retained when the available evidence does not establish an update. Dates and version labels in new work identify the applicable registration.

## Public work records

### record-fb95d3b2a6ed

2026-06-02T14:34:19Z | tool | runtime

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol


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
  "request_id": "request-897bd915ef0a"
}
```

### record-2527abbf4c9c

2026-06-07T16:13:09Z | review | Anika

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=protocol

- decision: reject
- reviewed_fields: []
- authority_ref: record-8750d0bec6f4
- comment: Checked.

```json
{
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-24948",
        "source_route": "index-e07c29"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-24948",
        "source_route": "index-b6f72d"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Checked.",
  "decision": "reject",
  "document_id": "DOC-24948",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:299d35f1141e0ab1c441c36337e7a512",
    "configured_route": "index-e07c29",
    "date": "2026-06-07",
    "document_id": "DOC-24948",
    "release_id": "REL-24948"
  },
  "format": "raw",
  "rejected_artifact": "replacement",
  "rejection_reason": "Review stopped at the missing signature block. Target-field checks remain open.",
  "reviewed_fields": []
}
```

### record-55d5909b7725

2026-06-07T13:21:10Z | revision | Anika

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=protocol


```json
{
  "event": "preference",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:d14655884ba9c1853a39abbd2b053938",
    "configured_route": "index-e07c29",
    "date": "2026-06-07",
    "document_id": "DOC-73361",
    "release_id": "REL-73361"
  },
  "message": "My personal choice here would be source_route set to 'index-b6f72d'.",
  "proposed_fields": {
    "checksum_check": "required",
    "release_id": "REL-73361",
    "source_route": "index-b6f72d"
  }
}
```

### record-79e643f28bc5

2026-06-07T10:25:11Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-13435",
        "source_route": "index-e07c29"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-13435",
        "source_route": "index-b6f72d"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-13435",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:cb6bcf2fe013e36ad00b4254968a0cbb",
    "configured_route": "index-e07c29",
    "date": "2026-06-07",
    "document_id": "DOC-13435",
    "release_id": "REL-13435"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-fa378f935013

2026-06-02T12:26:17Z | revision | Anika

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=assay_report


```json
{
  "event": "preference",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:712695ebc38c2c4ec137e6ab101d8fae",
    "configured_route": "index-e07c29",
    "date": "2026-06-02",
    "document_id": "DOC-96159",
    "release_id": "REL-96159"
  },
  "message": "I would prefer source_route set to 'index-b6f72d' for this item.",
  "proposed_fields": {
    "checksum_check": "required",
    "release_id": "REL-96159",
    "source_route": "index-b6f72d"
  }
}
```

### record-31de4ada5aa6

2026-06-07T13:52:27Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=protocol

- decision: reject
- reviewed_fields: []
- authority_ref: record-8750d0bec6f4
- comment: Recorded.

```json
{
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-54019",
        "source_route": "index-b6f72d"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-54019",
        "source_route": "index-e07c29"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Recorded.",
  "decision": "reject",
  "document_id": "DOC-54019",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:50743a3234ac74406e47df142572dba2",
    "configured_route": "index-e07c29",
    "date": "2026-06-07",
    "document_id": "DOC-54019",
    "release_id": "REL-54019"
  },
  "format": "raw",
  "rejected_artifact": "replacement",
  "rejection_reason": "Review stopped at the missing signature block. Target-field checks remain open.",
  "reviewed_fields": []
}
```

### record-66caeb0db4f6

2026-06-10T13:40:59Z | review | Elena

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=assay_report

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Reviewed.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-78651",
        "source_route": "index-e07c29"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-78651",
        "source_route": "index-b6f72d"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Reviewed.",
  "decision": "accept",
  "document_id": "DOC-78651",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:ec37c2285491f147aec5d903f6a0f933",
    "configured_route": "index-e07c29",
    "date": "2026-06-10",
    "document_id": "DOC-78651",
    "release_id": "REL-78651"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-ee8f7b127597

2026-06-07T13:18:55Z | revision | Jonas

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=assay_report


```json
{
  "event": "preference",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:6d5f6dd951f5e5c97d603356a0c4e737",
    "configured_route": "index-e07c29",
    "date": "2026-06-07",
    "document_id": "DOC-46846",
    "release_id": "REL-46846"
  },
  "message": "My personal choice here would be source_route set to 'index-b6f72d'.",
  "proposed_fields": {
    "checksum_check": "required",
    "release_id": "REL-46846",
    "source_route": "index-b6f72d"
  }
}
```

### record-ff8d3de131aa

2026-05-12T17:37:50Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-174bdd4f41f8, collection=active, document_class=protocol

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-7ec6c6010e10
- accepted_artifact: replacement
- comment: Checked.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-69284",
        "source_route": "index-b6f72d"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-69284",
        "source_route": "index-e07c29"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7ec6c6010e10",
  "comment": "Checked.",
  "decision": "accept",
  "document_id": "DOC-69284",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:a01f0e9f7878696c73872c65b3fb5f29",
    "configured_route": "index-e07c29",
    "date": "2026-05-12",
    "document_id": "DOC-69284",
    "release_id": "REL-69284"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-0aad8f8989e2

2026-06-02T10:18:13Z | revision | forwarding-service

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=assay_report

- origin_ref: record-39b3ba320383

```json
{
  "event": "forward",
  "message": "Attached by reference from the earlier review.",
  "origin_ref": "record-39b3ba320383"
}
```

### record-5d0704f4066b

2026-06-07T11:28:29Z | tool | runtime

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol


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
  "request_id": "request-455597c49ef9"
}
```

### record-b6f43115ba0a

2026-06-10T16:07:18Z | revision | forwarding-service

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol

- origin_ref: record-7977928eea21

```json
{
  "event": "forward",
  "message": "Forwarded artifact for the next work item.",
  "origin_ref": "record-7977928eea21"
}
```

### record-7977928eea21

2026-06-10T13:32:27Z | review | Anika

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=protocol

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Reviewed.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-24208",
        "source_route": "index-b6f72d"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-24208",
        "source_route": "index-e07c29"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Reviewed.",
  "decision": "accept",
  "document_id": "DOC-24208",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:22f8560c088e1fc3885e9836301db44f",
    "configured_route": "index-e07c29",
    "date": "2026-06-10",
    "document_id": "DOC-24208",
    "release_id": "REL-24208"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-655fdac148de

2026-06-07T10:42:09Z | review | Anika

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-88940",
        "source_route": "index-b6f72d"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "delivery_timestamp": "2026-06-07T10:42:09Z",
        "release_id": "REL-88940",
        "source_route": "index-e07c29"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-88940",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:3b52602dfc660df3bc66bce9277b5a30",
    "configured_route": "index-e07c29",
    "date": "2026-06-07",
    "document_id": "DOC-88940",
    "release_id": "REL-88940"
  },
  "format": "raw",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-821523055e5a

2026-06-02T10:02:25Z | review | Anika

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=assay_report

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Review complete.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-74761",
        "source_route": "index-e07c29"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "delivery_timestamp": "2026-06-02T10:02:25Z",
        "release_id": "REL-74761",
        "source_route": "index-b6f72d"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Review complete.",
  "decision": "accept",
  "document_id": "DOC-74761",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:48f4b0e70c9c708d14072825ea9eea25",
    "configured_route": "index-e07c29",
    "date": "2026-06-02",
    "document_id": "DOC-74761",
    "release_id": "REL-74761"
  },
  "format": "raw",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-c74a514aab2d

2026-06-07T16:37:13Z | review | Anika

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=assay_report

- decision: reject
- reviewed_fields: []
- authority_ref: record-8750d0bec6f4
- comment: Checked.

```json
{
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-53524",
        "source_route": "index-e07c29"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-53524",
        "source_route": "index-b6f72d"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Checked.",
  "decision": "reject",
  "document_id": "DOC-53524",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:fb38d9241de00ba18a58247551e33ee0",
    "configured_route": "index-e07c29",
    "date": "2026-06-07",
    "document_id": "DOC-53524",
    "release_id": "REL-53524"
  },
  "format": "raw",
  "rejected_artifact": "replacement",
  "rejection_reason": "The signature block is missing. Field-level review was not completed.",
  "reviewed_fields": []
}
```

### record-ca939802ac74

2026-06-02T11:52:12Z | revision | forwarding-service

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=assay_report

- origin_ref: record-ff8d3de131aa

```json
{
  "event": "forward",
  "message": "Sharing the linked artifact with the working group.",
  "origin_ref": "record-ff8d3de131aa"
}
```

### record-78647d3a0d3d

2026-06-02T10:33:57Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=assay_report

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Reviewed.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-91383",
        "source_route": "index-e07c29"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "delivery_timestamp": "2026-06-02T10:33:57Z",
        "release_id": "REL-91383",
        "source_route": "index-b6f72d"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Reviewed.",
  "decision": "accept",
  "document_id": "DOC-91383",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:0ba5c525dc3d28be70e83494824e0b6c",
    "configured_route": "index-e07c29",
    "date": "2026-06-02",
    "document_id": "DOC-91383",
    "release_id": "REL-91383"
  },
  "format": "raw",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-92d70a65e9ac

2026-06-07T12:51:13Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=protocol

- decision: reject
- reviewed_fields: []
- authority_ref: record-8750d0bec6f4
- comment: Recorded.

```json
{
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-82702",
        "source_route": "index-e07c29"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-82702",
        "source_route": "index-b6f72d"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Recorded.",
  "decision": "reject",
  "document_id": "DOC-82702",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:c3fe3ae561b5cc95360042ddb7f67d0a",
    "configured_route": "index-e07c29",
    "date": "2026-06-07",
    "document_id": "DOC-82702",
    "release_id": "REL-82702"
  },
  "format": "raw",
  "rejected_artifact": "replacement",
  "rejection_reason": "Review stopped at the missing signature block. Target-field checks remain open.",
  "reviewed_fields": []
}
```

### record-4b4bc3378821

2026-06-10T13:35:31Z | revision | forwarding-service

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=assay_report

- origin_ref: record-7977928eea21

```json
{
  "event": "forward",
  "message": "Sharing the linked artifact with the working group.",
  "origin_ref": "record-7977928eea21"
}
```

### record-5f789d9a950c

2026-06-07T13:03:29Z | revision | Theo

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol


```json
{
  "event": "preference",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:9adc59045f050c906558d9fabc38117b",
    "configured_route": "index-e07c29",
    "date": "2026-06-07",
    "document_id": "DOC-55645",
    "release_id": "REL-55645"
  },
  "message": "I would prefer source_route set to 'index-b6f72d' for this item.",
  "proposed_fields": {
    "checksum_check": "required",
    "release_id": "REL-55645",
    "source_route": "index-b6f72d"
  }
}
```

### record-49930bfe7fea

2026-06-07T16:20:13Z | revision | forwarding-service

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=assay_report

- origin_ref: record-ff8d3de131aa

```json
{
  "event": "forward",
  "message": "Forwarded artifact for the next work item.",
  "origin_ref": "record-ff8d3de131aa"
}
```

### record-72408458abd5

2026-06-10T11:46:12Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=assay_report

- decision: reject
- reviewed_fields: []
- authority_ref: record-8750d0bec6f4
- comment: Completed.

```json
{
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-94884",
        "source_route": "index-b6f72d"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-94884",
        "source_route": "index-e07c29"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Completed.",
  "decision": "reject",
  "document_id": "DOC-94884",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:a52a718b0a1577d56b4d0aab93e3420b",
    "configured_route": "index-e07c29",
    "date": "2026-06-10",
    "document_id": "DOC-94884",
    "release_id": "REL-94884"
  },
  "format": "raw",
  "rejected_artifact": "replacement",
  "rejection_reason": "Missing signature block; the artifact was returned before field review.",
  "reviewed_fields": []
}
```

### record-e5676d86b1d0

2026-06-07T12:12:58Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=assay_report

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Recorded.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-56237",
        "source_route": "index-e07c29"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "delivery_timestamp": "2026-06-07T12:12:58Z",
        "release_id": "REL-56237",
        "source_route": "index-b6f72d"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Recorded.",
  "decision": "accept",
  "document_id": "DOC-56237",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:e132f33b33dc5c9da6901181d4f505f5",
    "configured_route": "index-e07c29",
    "date": "2026-06-07",
    "document_id": "DOC-56237",
    "release_id": "REL-56237"
  },
  "format": "raw",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-dbedb0c49248

2026-06-07T10:43:49Z | review | Robin

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=assay_report

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-53026",
        "source_route": "index-b6f72d"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-53026",
        "source_route": "index-e07c29"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-53026",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:44d9f2dffabaa3af4dff57fb4a59d67d",
    "configured_route": "index-e07c29",
    "date": "2026-06-07",
    "document_id": "DOC-53026",
    "release_id": "REL-53026"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-c996f905a544

2026-06-07T17:48:05Z | revision | Anika

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=protocol


```json
{
  "event": "preference",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:7e154d5f3376d9db0da98d8069856976",
    "configured_route": "index-e07c29",
    "date": "2026-06-07",
    "document_id": "DOC-36770",
    "release_id": "REL-36770"
  },
  "message": "My personal choice here would be source_route set to 'index-b6f72d'.",
  "proposed_fields": {
    "checksum_check": "required",
    "release_id": "REL-36770",
    "source_route": "index-b6f72d"
  }
}
```

### record-5801011c22d5

2026-06-10T14:34:40Z | revision | Elena

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol


```json
{
  "event": "preference",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:9a1b6fa33406d1f1c41aa78c005a4881",
    "configured_route": "index-e07c29",
    "date": "2026-06-10",
    "document_id": "DOC-96084",
    "release_id": "REL-96084"
  },
  "message": "For my version I would use source_route set to 'index-e07c29'.",
  "proposed_fields": {
    "checksum_check": "required",
    "release_id": "REL-96084",
    "source_route": "index-e07c29"
  }
}
```

### record-8750d0bec6f4

2026-06-01T00:00:00Z | template | workflow-registry

Context: 


```json
{
  "authorised_reviewers": [
    "Anika",
    "Theo"
  ],
  "event": "register_version",
  "supersedes": "record-7ec6c6010e10",
  "task_family": "document_retrieval",
  "valid_from": "2026-06-01T00:00:00Z",
  "valid_until": "2027-01-01T00:00:00Z",
  "version": "edition-59bd41831407",
  "workflow": "workflow-e07c29b6f72d"
}
```

### record-382ef09021bf

2026-06-10T13:35:16Z | revision | forwarding-service

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=protocol

- origin_ref: record-7977928eea21

```json
{
  "event": "forward",
  "message": "Sharing the linked artifact with the working group.",
  "origin_ref": "record-7977928eea21"
}
```

### record-afe55bdf02ad

2026-06-02T10:08:05Z | review | Daria

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Review complete.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-90251",
        "source_route": "index-b6f72d"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-90251",
        "source_route": "index-e07c29"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Review complete.",
  "decision": "accept",
  "document_id": "DOC-90251",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:348cd3d7ac160720e3eea819886a8127",
    "configured_route": "index-e07c29",
    "date": "2026-06-02",
    "document_id": "DOC-90251",
    "release_id": "REL-90251"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-34582169d183

2026-06-02T10:21:12Z | review | Elena

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=assay_report

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Review complete.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-74051",
        "source_route": "index-b6f72d"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-74051",
        "source_route": "index-e07c29"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Review complete.",
  "decision": "accept",
  "document_id": "DOC-74051",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:eb3fd9f2fc725c3c09d6fd2ecc3fa137",
    "configured_route": "index-e07c29",
    "date": "2026-06-02",
    "document_id": "DOC-74051",
    "release_id": "REL-74051"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-604c17aa28d8

2026-06-02T10:52:33Z | review | Anika

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=assay_report

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Review complete.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-13096",
        "source_route": "index-e07c29"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "delivery_timestamp": "2026-06-02T10:52:33Z",
        "release_id": "REL-13096",
        "source_route": "index-b6f72d"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Review complete.",
  "decision": "accept",
  "document_id": "DOC-13096",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:1c911ba6692fdebb4a626dae0e591420",
    "configured_route": "index-e07c29",
    "date": "2026-06-02",
    "document_id": "DOC-13096",
    "release_id": "REL-13096"
  },
  "format": "raw",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-904f74deb3c7

2026-06-07T16:18:27Z | revision | forwarding-service

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol

- origin_ref: record-ff8d3de131aa

```json
{
  "event": "forward",
  "message": "Sharing the linked artifact with the working group.",
  "origin_ref": "record-ff8d3de131aa"
}
```

### record-849c88bf5583

2026-06-02T08:46:20Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=assay_report

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Checked.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-14729",
        "source_route": "index-b6f72d"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "delivery_timestamp": "2026-06-02T08:46:20Z",
        "release_id": "REL-14729",
        "source_route": "index-e07c29"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Checked.",
  "decision": "accept",
  "document_id": "DOC-14729",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:de6bb14a253c839af2c13046b6bf63ce",
    "configured_route": "index-e07c29",
    "date": "2026-06-02",
    "document_id": "DOC-14729",
    "release_id": "REL-14729"
  },
  "format": "raw",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-7fa82b9fcde0

2026-06-10T13:00:24Z | review | Elena

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Reviewed.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-61059",
        "source_route": "index-b6f72d"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-61059",
        "source_route": "index-e07c29"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Reviewed.",
  "decision": "accept",
  "document_id": "DOC-61059",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:da6ef3ef6c443b3eb68f59d7e4e0ad9a",
    "configured_route": "index-e07c29",
    "date": "2026-06-10",
    "document_id": "DOC-61059",
    "release_id": "REL-61059"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-7f5b77a09f5e

2026-06-10T16:32:45Z | revision | Anika

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=assay_report


```json
{
  "event": "preference",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:294941a6da4b881bd6fd049b645b3a88",
    "configured_route": "index-e07c29",
    "date": "2026-06-10",
    "document_id": "DOC-84704",
    "release_id": "REL-84704"
  },
  "message": "For my version I would use source_route set to 'index-e07c29'.",
  "proposed_fields": {
    "checksum_check": "required",
    "release_id": "REL-84704",
    "source_route": "index-e07c29"
  }
}
```

### record-30c3dfbffa74

2026-06-02T10:13:11Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=assay_report

- decision: reject
- reviewed_fields: []
- authority_ref: record-8750d0bec6f4
- comment: Reviewed.

```json
{
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-38526",
        "source_route": "index-b6f72d"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-38526",
        "source_route": "index-e07c29"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Reviewed.",
  "decision": "reject",
  "document_id": "DOC-38526",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:59a3c3840bf0b6a496f0a9427650cba3",
    "configured_route": "index-e07c29",
    "date": "2026-06-02",
    "document_id": "DOC-38526",
    "release_id": "REL-38526"
  },
  "format": "raw",
  "rejected_artifact": "replacement",
  "rejection_reason": "The signature block is missing. Field-level review was not completed.",
  "reviewed_fields": []
}
```

### record-7ec6c6010e10

2026-01-01T00:00:00Z | template | workflow-registry

Context: 


```json
{
  "authorised_reviewers": [
    "Theo",
    "Daria"
  ],
  "event": "register_version",
  "supersedes": null,
  "task_family": "document_retrieval",
  "valid_from": "2026-01-01T00:00:00Z",
  "valid_until": "2026-06-01T00:00:00Z",
  "version": "edition-174bdd4f41f8",
  "workflow": "workflow-e07c29b6f72d"
}
```

### record-4e9574b3fb82

2026-06-02T13:31:07Z | tool | runtime

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=protocol


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
  "request_id": "request-3574289f86f1"
}
```

### record-88844f6014f0

2026-06-07T13:22:17Z | review | Anika

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=assay_report

- decision: reject
- reviewed_fields: []
- authority_ref: record-8750d0bec6f4
- comment: Review complete.

```json
{
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-31647",
        "source_route": "index-b6f72d"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-31647",
        "source_route": "index-e07c29"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Review complete.",
  "decision": "reject",
  "document_id": "DOC-31647",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:625e449b2ebe95f3d6521004a1017d4f",
    "configured_route": "index-e07c29",
    "date": "2026-06-07",
    "document_id": "DOC-31647",
    "release_id": "REL-31647"
  },
  "format": "raw",
  "rejected_artifact": "replacement",
  "rejection_reason": "Missing signature block; the artifact was returned before field review.",
  "reviewed_fields": []
}
```

### record-c53c5db78a50

2026-06-07T12:58:18Z | review | Anika

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol

- decision: reject
- reviewed_fields: []
- authority_ref: record-8750d0bec6f4
- comment: Reviewed.

```json
{
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-42045",
        "source_route": "index-b6f72d"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-42045",
        "source_route": "index-e07c29"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Reviewed.",
  "decision": "reject",
  "document_id": "DOC-42045",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:4a98469a2765e471cff2b46f47b30538",
    "configured_route": "index-e07c29",
    "date": "2026-06-07",
    "document_id": "DOC-42045",
    "release_id": "REL-42045"
  },
  "format": "raw",
  "rejected_artifact": "replacement",
  "rejection_reason": "Missing signature block; the artifact was returned before field review.",
  "reviewed_fields": []
}
```

### record-5ec72da8fccd

2026-06-07T15:26:39Z | review | Anika

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=protocol

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Reviewed.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-91883",
        "source_route": "index-e07c29"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "delivery_timestamp": "2026-06-07T15:26:39Z",
        "release_id": "REL-91883",
        "source_route": "index-b6f72d"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Reviewed.",
  "decision": "accept",
  "document_id": "DOC-91883",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:c50f6d741636ef3e52821ab74d69905b",
    "configured_route": "index-e07c29",
    "date": "2026-06-07",
    "document_id": "DOC-91883",
    "release_id": "REL-91883"
  },
  "format": "raw",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-9893c2d4cfbe

2026-06-07T09:15:01Z | review | Elena

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Completed.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-17170",
        "source_route": "index-e07c29"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-17170",
        "source_route": "index-b6f72d"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Completed.",
  "decision": "accept",
  "document_id": "DOC-17170",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:81788ff50e0557aa6a6e258993f886ec",
    "configured_route": "index-e07c29",
    "date": "2026-06-07",
    "document_id": "DOC-17170",
    "release_id": "REL-17170"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-0b81b8de0f7e

2026-06-10T17:17:20Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=protocol

- decision: reject
- reviewed_fields: []
- authority_ref: record-8750d0bec6f4
- comment: Recorded.

```json
{
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-78665",
        "source_route": "index-b6f72d"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-78665",
        "source_route": "index-e07c29"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Recorded.",
  "decision": "reject",
  "document_id": "DOC-78665",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:fc9f2919ece0b2550fc1cd591714ec5c",
    "configured_route": "index-e07c29",
    "date": "2026-06-10",
    "document_id": "DOC-78665",
    "release_id": "REL-78665"
  },
  "format": "raw",
  "rejected_artifact": "replacement",
  "rejection_reason": "Missing signature block; the artifact was returned before field review.",
  "reviewed_fields": []
}
```

### record-8f87ded1249f

2026-06-07T10:19:33Z | review | Anika

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-43398",
        "source_route": "index-b6f72d"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "delivery_timestamp": "2026-06-07T10:19:33Z",
        "release_id": "REL-43398",
        "source_route": "index-e07c29"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-43398",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:5224fa67684e37506e508842f30d876e",
    "configured_route": "index-e07c29",
    "date": "2026-06-07",
    "document_id": "DOC-43398",
    "release_id": "REL-43398"
  },
  "format": "raw",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-26b7e8637d8b

2026-06-10T10:59:01Z | tool | runtime

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol


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
  "request_id": "request-90425adcbb5d"
}
```

### record-f5174c3b1322

2026-06-10T13:07:09Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=assay_report

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Reviewed.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-86579",
        "source_route": "index-b6f72d"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "delivery_timestamp": "2026-06-10T13:07:09Z",
        "release_id": "REL-86579",
        "source_route": "index-e07c29"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Reviewed.",
  "decision": "accept",
  "document_id": "DOC-86579",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:b16fa988d82faff5df403edb6fb23a39",
    "configured_route": "index-e07c29",
    "date": "2026-06-10",
    "document_id": "DOC-86579",
    "release_id": "REL-86579"
  },
  "format": "raw",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-bb7c40de5c7e

2026-06-02T13:54:16Z | review | Jonas

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Completed.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-50426",
        "source_route": "index-b6f72d"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-50426",
        "source_route": "index-e07c29"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Completed.",
  "decision": "accept",
  "document_id": "DOC-50426",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:33ce3ddf3ef7c053e5c6aa6cf198fe4d",
    "configured_route": "index-e07c29",
    "date": "2026-06-02",
    "document_id": "DOC-50426",
    "release_id": "REL-50426"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-ae042fbfe4b5

2026-06-10T08:42:22Z | tool | runtime

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=assay_report


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
  "request_id": "request-772e1776c5d9"
}
```

### record-b58c2f60089e

2026-06-02T13:56:34Z | review | Anika

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=assay_report

- decision: reject
- reviewed_fields: []
- authority_ref: record-8750d0bec6f4
- comment: Checked.

```json
{
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-32019",
        "source_route": "index-e07c29"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-32019",
        "source_route": "index-b6f72d"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Checked.",
  "decision": "reject",
  "document_id": "DOC-32019",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:0ac068d52b054fa3109eb4426771ba35",
    "configured_route": "index-e07c29",
    "date": "2026-06-02",
    "document_id": "DOC-32019",
    "release_id": "REL-32019"
  },
  "format": "raw",
  "rejected_artifact": "replacement",
  "rejection_reason": "Missing signature block; the artifact was returned before field review.",
  "reviewed_fields": []
}
```

### record-77e9f027629a

2026-06-10T16:05:52Z | tool | runtime

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=assay_report


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
  "request_id": "request-1dd6c797fb28"
}
```

### record-dffd05b48108

2026-06-10T09:53:21Z | review | Elena

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=protocol

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Review complete.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-51517",
        "source_route": "index-b6f72d"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-51517",
        "source_route": "index-e07c29"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Review complete.",
  "decision": "accept",
  "document_id": "DOC-51517",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:252b21660955db8392785ad357b4b71c",
    "configured_route": "index-e07c29",
    "date": "2026-06-10",
    "document_id": "DOC-51517",
    "release_id": "REL-51517"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-83a5fb356519

2026-06-02T15:25:14Z | revision | forwarding-service

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol

- origin_ref: record-ff8d3de131aa

```json
{
  "event": "forward",
  "message": "Sharing the linked artifact with the working group.",
  "origin_ref": "record-ff8d3de131aa"
}
```

### record-a98ede9cf5c6

2026-06-10T13:42:11Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=assay_report

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Reviewed.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-74504",
        "source_route": "index-e07c29"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "delivery_timestamp": "2026-06-10T13:42:11Z",
        "release_id": "REL-74504",
        "source_route": "index-b6f72d"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Reviewed.",
  "decision": "accept",
  "document_id": "DOC-74504",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:f4da8beee8c7b69854458c2a036569f5",
    "configured_route": "index-e07c29",
    "date": "2026-06-10",
    "document_id": "DOC-74504",
    "release_id": "REL-74504"
  },
  "format": "raw",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-919f71c07d95

2026-06-02T12:09:51Z | review | Daria

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Recorded.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-77663",
        "source_route": "index-e07c29"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-77663",
        "source_route": "index-b6f72d"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Recorded.",
  "decision": "accept",
  "document_id": "DOC-77663",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:74943448a3da38d0bc4a39d1b8e178a5",
    "configured_route": "index-e07c29",
    "date": "2026-06-02",
    "document_id": "DOC-77663",
    "release_id": "REL-77663"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-2d96acb9573b

2026-06-07T10:05:50Z | review | Jonas

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-33176",
        "source_route": "index-b6f72d"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-33176",
        "source_route": "index-e07c29"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-33176",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:5fe5a69d15c374cf6df6194253ada217",
    "configured_route": "index-e07c29",
    "date": "2026-06-07",
    "document_id": "DOC-33176",
    "release_id": "REL-33176"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-2eb30caf990c

2026-06-02T16:48:03Z | revision | Daria

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=protocol


```json
{
  "event": "preference",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:85b1363238b2da51167ddac6d628be8f",
    "configured_route": "index-e07c29",
    "date": "2026-06-02",
    "document_id": "DOC-21187",
    "release_id": "REL-21187"
  },
  "message": "I would prefer source_route set to 'index-e07c29' for this item.",
  "proposed_fields": {
    "checksum_check": "required",
    "release_id": "REL-21187",
    "source_route": "index-e07c29"
  }
}
```

### record-d44c95952b18

2026-06-02T16:08:06Z | revision | Elena

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=protocol


```json
{
  "event": "preference",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:7351d4f83cc028ffdd175b2500c15e50",
    "configured_route": "index-e07c29",
    "date": "2026-06-02",
    "document_id": "DOC-57416",
    "release_id": "REL-57416"
  },
  "message": "My personal choice here would be source_route set to 'index-e07c29'.",
  "proposed_fields": {
    "checksum_check": "required",
    "release_id": "REL-57416",
    "source_route": "index-e07c29"
  }
}
```

### record-39b3ba320383

2026-06-02T10:15:27Z | review | Anika

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=assay_report

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-8750d0bec6f4
- accepted_artifact: replacement
- comment: Review complete.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-87235",
        "source_route": "index-e07c29"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-87235",
        "source_route": "index-b6f72d"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-8750d0bec6f4",
  "comment": "Review complete.",
  "decision": "accept",
  "document_id": "DOC-87235",
  "event": "review",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:a73af16e4dfa1ca39d24bbdc12e57d91",
    "configured_route": "index-e07c29",
    "date": "2026-06-02",
    "document_id": "DOC-87235",
    "release_id": "REL-87235"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-b8e08ebe7d68

2026-06-10T17:25:00Z | revision | Jonas

Context: task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=assay_report


```json
{
  "event": "preference",
  "facts": {
    "alternative_route": "index-b6f72d",
    "checksum": "sha256:ef065c01b28949b8458acf081061c701",
    "configured_route": "index-e07c29",
    "date": "2026-06-10",
    "document_id": "DOC-87958",
    "release_id": "REL-87958"
  },
  "message": "My personal choice here would be source_route set to 'index-e07c29'.",
  "proposed_fields": {
    "checksum_check": "required",
    "release_id": "REL-87958",
    "source_route": "index-e07c29"
  }
}
```

## Oracle derivation from public evidence

Recomputed solely from the public History by the independent oracle.

H14 excludes XOR and XNOR; transfer identification depends on this supplied restriction.

Distinct current-version functions: **1**. Full policies across all registered versions: **7**.

An approval constrains one cell in its registered version. The following are the
actual applied constraints, including independent repeats. Copies do not add a constraint.

| Public record | Version | Context | Field option |
| --- | --- | --- | --- |
| record-79e643f28bc5 | edition-59bd41831407 | task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=active, document_class=protocol | 1 |
| record-ff8d3de131aa | edition-174bdd4f41f8 | task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-174bdd4f41f8, collection=active, document_class=protocol | 0 |
| record-7977928eea21 | edition-59bd41831407 | task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=protocol | 0 |
| record-39b3ba320383 | edition-59bd41831407 | task_family=document_retrieval, workflow=workflow-e07c29b6f72d, version=edition-59bd41831407, collection=archive, document_class=assay_report | 1 |

### Competing requirement explanations

Zero is the configured baseline; one is the alternative. Each row is a distinct
compatible function for this version. No preference for simplicity removes a row.
The private sampling plan and world policy do not filter these explanations.

Version edition-174bdd4f41f8: 7 compatible functions.

| Function | collection=active, document_class=protocol | collection=active, document_class=assay_report | collection=archive, document_class=protocol | collection=archive, document_class=assay_report | Complexity |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | 0 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 | 1 | 2 |
| 3 | 0 | 0 | 1 | 0 | 2 |
| 4 | 0 | 0 | 1 | 1 | 1 |
| 5 | 0 | 1 | 0 | 0 | 2 |
| 6 | 0 | 1 | 0 | 1 | 1 |
| 7 | 0 | 1 | 1 | 1 | 2 |

Version edition-59bd41831407: 1 compatible functions.

| Function | collection=active, document_class=protocol | collection=active, document_class=assay_report | collection=archive, document_class=protocol | collection=archive, document_class=assay_report | Complexity |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 1 | 1 | 0 | 1 | 2 |

### Diagnostic and control derivations

| Task | Context observed | Witnesses | Action | Retention basis |
| --- | --- | --- | --- | --- |
| diagnostic | False | none | apply | not_retention |
| control | True | record-7977928eea21 | keep | resolved |

## Private material audit

These design labels, counterfactuals and world requirements are evaluator material.
They are never preparation or generation inputs. The true world is distinct from
what the public evidence identifies. Exact world fields are shown with each task.

Registered record counts and construction audit:

```json
{
  "additional_noise_counts": {
    "approval_without_target": 10,
    "forward_current": 4,
    "forward_old": 4,
    "rejected_opposite_artifact": 10,
    "target_field_preference": 10,
    "technical": 6,
    "unauthorised_revision": 10
  },
  "admissible_count": 7,
  "control_basis": "resolved_keep",
  "current_admissible_count": 1,
  "current_witness_contexts": [
    {
      "collection": "archive",
      "document_class": "protocol",
      "task_family": "document_retrieval",
      "version": "edition-59bd41831407",
      "workflow": "workflow-e07c29b6f72d"
    },
    {
      "collection": "active",
      "document_class": "protocol",
      "task_family": "document_retrieval",
      "version": "edition-59bd41831407",
      "workflow": "workflow-e07c29b6f72d"
    },
    {
      "collection": "archive",
      "document_class": "assay_report",
      "task_family": "document_retrieval",
      "version": "edition-59bd41831407",
      "workflow": "workflow-e07c29b6f72d"
    }
  ],
  "diagnostic_observed": false,
  "material_revision": "v04-amendment-03-r2",
  "record_count": 60,
  "registered_versions": [
    "edition-174bdd4f41f8",
    "edition-59bd41831407"
  ],
  "rendering": "raw",
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
| approval_without_target | 10 | 0 | 5 | 5 | 0 | 0 | 0 | record-655fdac148de, record-849c88bf5583, record-5ec72da8fccd, record-8f87ded1249f, record-f5174c3b1322 |
| forward | 8 | 0 | 6 | 2 | 0 | 0 | 0 | record-b6f43115ba0a, record-ca939802ac74, record-4b4bc3378821, record-49930bfe7fea, record-904f74deb3c7, record-83a5fb356519 |
| old_approval | 1 | 0 | 1 | 0 | 0 | 0 | 0 | record-ff8d3de131aa |
| rejected_opposite_artifact | 10 | 0 | 6 | 4 | 0 | 0 | 0 | record-2527abbf4c9c, record-92d70a65e9ac, record-72408458abd5, record-30c3dfbffa74, record-88844f6014f0, record-c53c5db78a50 |
| target_field_preference | 10 | 0 | 5 | 5 | 0 | 0 | 0 | record-55d5909b7725, record-c996f905a544, record-5801011c22d5, record-7f5b77a09f5e, record-b8e08ebe7d68 |
| unauthorised_revision | 10 | 0 | 6 | 4 | 0 | 0 | 0 | record-dbedb0c49248, record-afe55bdf02ad, record-34582169d183, record-7fa82b9fcde0, record-bb7c40de5c7e, record-2d96acb9573b |

### Every promoted public record

| Record | Type | Origin | Public option | Remaining policies | Outcome | Qualifies | Diagnostic action | Control action |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| record-2527abbf4c9c | rejected_opposite_artifact | record-2527abbf4c9c | 1 | 0 | contradiction | True | None | None |
| record-55d5909b7725 | target_field_preference | record-55d5909b7725 | 1 | 0 | contradiction | True | None | None |
| record-fa378f935013 | target_field_preference | record-fa378f935013 | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-31de4ada5aa6 | rejected_opposite_artifact | record-31de4ada5aa6 | 0 | 7 | unchanged_constraints | False | apply | keep |
| record-66caeb0db4f6 | unauthorised_revision | record-66caeb0db4f6 | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-ee8f7b127597 | target_field_preference | record-ee8f7b127597 | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-ff8d3de131aa | old_approval | record-ff8d3de131aa | 0 | 0 | contradiction | True | None | None |
| record-0aad8f8989e2 | forward | record-39b3ba320383 | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-b6f43115ba0a | forward | record-7977928eea21 | 0 | 0 | contradiction | True | None | None |
| record-655fdac148de | approval_without_target | record-655fdac148de | 0 | 0 | contradiction | True | None | None |
| record-821523055e5a | approval_without_target | record-821523055e5a | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-c74a514aab2d | rejected_opposite_artifact | record-c74a514aab2d | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-ca939802ac74 | forward | record-ff8d3de131aa | 0 | 0 | contradiction | True | None | None |
| record-78647d3a0d3d | approval_without_target | record-78647d3a0d3d | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-92d70a65e9ac | rejected_opposite_artifact | record-92d70a65e9ac | 1 | 0 | contradiction | True | None | None |
| record-4b4bc3378821 | forward | record-7977928eea21 | 0 | 0 | contradiction | True | None | None |
| record-5f789d9a950c | target_field_preference | record-5f789d9a950c | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-49930bfe7fea | forward | record-ff8d3de131aa | 0 | 0 | contradiction | True | None | None |
| record-72408458abd5 | rejected_opposite_artifact | record-72408458abd5 | 0 | 0 | contradiction | True | None | None |
| record-e5676d86b1d0 | approval_without_target | record-e5676d86b1d0 | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-dbedb0c49248 | unauthorised_revision | record-dbedb0c49248 | 0 | 0 | contradiction | True | None | None |
| record-c996f905a544 | target_field_preference | record-c996f905a544 | 1 | 0 | contradiction | True | None | None |
| record-5801011c22d5 | target_field_preference | record-5801011c22d5 | 0 | 0 | contradiction | True | None | None |
| record-382ef09021bf | forward | record-7977928eea21 | 0 | 7 | unchanged_constraints | False | apply | keep |
| record-afe55bdf02ad | unauthorised_revision | record-afe55bdf02ad | 0 | 0 | contradiction | True | None | None |
| record-34582169d183 | unauthorised_revision | record-34582169d183 | 0 | 0 | contradiction | True | None | None |
| record-604c17aa28d8 | approval_without_target | record-604c17aa28d8 | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-904f74deb3c7 | forward | record-ff8d3de131aa | 0 | 0 | contradiction | True | None | None |
| record-849c88bf5583 | approval_without_target | record-849c88bf5583 | 0 | 0 | contradiction | True | None | None |
| record-7fa82b9fcde0 | unauthorised_revision | record-7fa82b9fcde0 | 0 | 0 | contradiction | True | None | None |
| record-7f5b77a09f5e | target_field_preference | record-7f5b77a09f5e | 0 | 0 | contradiction | True | None | None |
| record-30c3dfbffa74 | rejected_opposite_artifact | record-30c3dfbffa74 | 0 | 0 | contradiction | True | None | None |
| record-88844f6014f0 | rejected_opposite_artifact | record-88844f6014f0 | 0 | 0 | contradiction | True | None | None |
| record-c53c5db78a50 | rejected_opposite_artifact | record-c53c5db78a50 | 0 | 0 | contradiction | True | None | None |
| record-5ec72da8fccd | approval_without_target | record-5ec72da8fccd | 1 | 0 | contradiction | True | None | None |
| record-9893c2d4cfbe | unauthorised_revision | record-9893c2d4cfbe | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-0b81b8de0f7e | rejected_opposite_artifact | record-0b81b8de0f7e | 0 | 7 | unchanged_constraints | False | apply | keep |
| record-8f87ded1249f | approval_without_target | record-8f87ded1249f | 0 | 0 | contradiction | True | None | None |
| record-f5174c3b1322 | approval_without_target | record-f5174c3b1322 | 0 | 0 | contradiction | True | None | None |
| record-bb7c40de5c7e | unauthorised_revision | record-bb7c40de5c7e | 0 | 0 | contradiction | True | None | None |
| record-b58c2f60089e | rejected_opposite_artifact | record-b58c2f60089e | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-dffd05b48108 | unauthorised_revision | record-dffd05b48108 | 0 | 7 | unchanged_constraints | False | apply | keep |
| record-83a5fb356519 | forward | record-ff8d3de131aa | 0 | 0 | contradiction | True | None | None |
| record-a98ede9cf5c6 | approval_without_target | record-a98ede9cf5c6 | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-919f71c07d95 | unauthorised_revision | record-919f71c07d95 | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-2d96acb9573b | unauthorised_revision | record-2d96acb9573b | 0 | 0 | contradiction | True | None | None |
| record-2eb30caf990c | target_field_preference | record-2eb30caf990c | 0 | 7 | unchanged_constraints | False | apply | keep |
| record-d44c95952b18 | target_field_preference | record-d44c95952b18 | 0 | 7 | unchanged_constraints | False | apply | keep |
| record-b8e08ebe7d68 | target_field_preference | record-b8e08ebe7d68 | 0 | 0 | contradiction | True | None | None |

### Exact promotions, contexts and public value provenance

The [complete JSON sidecar](S5-retrieval.json) preserves every intervention under `counterfactual.records`,
including selected field presence/value, effective current context, public origin,
precise promotion and remaining-policy count. No intervention alters the real history.

## Future tasks for this development example

### diagnostic

Public task

```json
{
  "task_id": "task-dcf74314234d",
  "context": {
    "task_family": "document_retrieval",
    "workflow": "workflow-e07c29b6f72d",
    "version": "edition-59bd41831407",
    "collection": "active",
    "document_class": "assay_report"
  },
  "facts": {
    "document_id": "DOC-96336",
    "date": "2026-06-15",
    "configured_route": "index-e07c29",
    "alternative_route": "index-b6f72d",
    "release_id": "REL-96336",
    "checksum": "sha256:8b8a139ae3bdf18f69de4a2c07167cbe"
  },
  "baseline_fields": [
    {
      "name": "source_route",
      "value": "index-e07c29"
    },
    {
      "name": "release_id",
      "value": "REL-96336"
    },
    {
      "name": "checksum_check",
      "value": "required"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Private expected obligations and actual-world fields

```json
{
  "task_id": "task-dcf74314234d",
  "history_id": "history-8b93ced45577",
  "probe": "diagnostic",
  "expected_decision": "apply",
  "recoverable": true,
  "world_fields": [
    {
      "name": "source_route",
      "value": "index-b6f72d"
    },
    {
      "name": "release_id",
      "value": "REL-96336"
    },
    {
      "name": "checksum_check",
      "value": "required"
    }
  ]
}
```

### control

Public task

```json
{
  "task_id": "task-9c00efbfb506",
  "context": {
    "task_family": "document_retrieval",
    "workflow": "workflow-e07c29b6f72d",
    "version": "edition-59bd41831407",
    "collection": "archive",
    "document_class": "protocol"
  },
  "facts": {
    "document_id": "DOC-84929",
    "date": "2026-06-15",
    "configured_route": "index-e07c29",
    "alternative_route": "index-b6f72d",
    "release_id": "REL-84929",
    "checksum": "sha256:fda078c6ddae91f150a87d6fc6d3e459"
  },
  "baseline_fields": [
    {
      "name": "source_route",
      "value": "index-e07c29"
    },
    {
      "name": "release_id",
      "value": "REL-84929"
    },
    {
      "name": "checksum_check",
      "value": "required"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Private expected obligations and actual-world fields

```json
{
  "task_id": "task-9c00efbfb506",
  "history_id": "history-8b93ced45577",
  "probe": "control",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "source_route",
      "value": "index-e07c29"
    },
    {
      "name": "release_id",
      "value": "REL-84929"
    },
    {
      "name": "checksum_check",
      "value": "required"
    }
  ]
}
```

## Human response

Pending. No approval is inferred from this export.
