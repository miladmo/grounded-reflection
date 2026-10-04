# S5 / retrieval

Material revision: v04-amendment-03. Synthetic development example.

Registered task type: **transfer_change**. Intended diagnostic regime: **change**.
Public records: 60. Control basis: resolved_keep.

## Review summary

Current compatible functions: **1**. Full cross-version policies: 7.

H14 identification is conditional on excluding XOR and XNOR. Retaining an unresolved
baseline does not establish that the baseline is the true requirement.

| Task | Public context | Previously observed | Warranted action | Retention basis |
| --- | --- | --- | --- | --- |
| diagnostic | task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=assay_report | False | apply | not_retention |
| control | task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=protocol | True | keep | resolved |

Counterfactual qualification requires **contradiction** for every present type. All present types qualify: **True**.

One qualifying example per present type is shown below. The links lead to its
public evidence; all records and counts appear in the later audit and JSON sidecar.

| Type (record count) | Promoted record / source | Public target value | Exact promotion | Outcome / remaining policies |
| --- | --- | --- | --- | --- |
| approval_without_target (10) | [record-471d0905dd28](#record-471d0905dd28) | source_route = 'index-ff280e' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=assay_report | contradiction / 0 |
| forward (8) | [record-46c478584a37](#record-46c478584a37) / [record-fdf86322160f](#record-fdf86322160f) | source_route = 'index-ff280e' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol | contradiction / 0 |
| old_approval (1) | [record-fdf86322160f](#record-fdf86322160f) | source_route = 'index-ff280e' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol | contradiction / 0 |
| rejected_opposite_artifact (10) | [record-45e2b15510c4](#record-45e2b15510c4) | source_route = 'index-ff280e' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol | contradiction / 0 |
| target_field_preference (10) | [record-54a85dd1314b](#record-54a85dd1314b) | source_route = 'index-ff280e' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=assay_report | contradiction / 0 |
| unauthorised_revision (10) | [record-2e670c7b559c](#record-2e670c7b559c) | source_route = 'index-a2fbe9' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=protocol | contradiction / 0 |

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
  "workflow": "workflow-ff280ea2fbe9"
}
```

This is a bounded synthetic workflow model. initial_configuration declares the field options, two context dimensions and the complete H14 hypothesis class. Each registered version has one class member. A field observation constrains the member indexed by its recorded version. Broader consequences follow from the declared class. Facts provide current artifact values. Other fields retain their configured baseline. Outside the declared task_family and workflow, or without a complete declared context, no update is authorised by this model. A register_version event supplies trusted workflow metadata with the authority roster and half-open validity interval. Binding field approval is an event of type review with decision accept, performed by a listed reviewer within that interval, with the field included in reviewed_fields. Its accepted artifact establishes the field configuration at the recorded context. This explicit approval convention is a supplied synthetic assumption. A forward has an origin_ref identifying the record whose content it reproduces. Raw artifacts expose named revisions and a selected artifact reference; interpreted records expose the selected fields directly. A rejection records a whole-artifact decision and its stated grounds. An artifact field whose review is not recorded has no approved assignment. The configured baseline is retained when the available evidence does not establish an update. Dates and version labels in new work identify the applicable registration.

## Public work records

### record-f9da8799e038

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
  "task_family": "document_retrieval",
  "valid_from": "2026-01-01T00:00:00Z",
  "valid_until": "2026-06-01T00:00:00Z",
  "version": "edition-de7fcc0e8a7b",
  "workflow": "workflow-ff280ea2fbe9"
}
```

### record-fdf86322160f

2026-05-10T10:00:00Z | review | Elena

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-de7fcc0e8a7b, collection=active, document_class=protocol

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-f9da8799e038
- accepted_artifact: replacement
- comment: Approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-90259",
        "source_route": "index-a2fbe9"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-90259",
        "source_route": "index-ff280e"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-f9da8799e038",
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-90259",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:2f43b817e9574cf69c76f5f6646be82d",
    "configured_route": "index-ff280e",
    "date": "2026-05-10",
    "document_id": "DOC-90259",
    "release_id": "REL-90259"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-7f4d5b2ba261

2026-06-01T00:00:00Z | template | workflow-registry

Context: 


```json
{
  "authorised_reviewers": [
    "Theo",
    "Robin"
  ],
  "event": "register_version",
  "supersedes": "record-f9da8799e038",
  "task_family": "document_retrieval",
  "valid_from": "2026-06-01T00:00:00Z",
  "valid_until": "2027-01-01T00:00:00Z",
  "version": "edition-c2b92d1fed69",
  "workflow": "workflow-ff280ea2fbe9"
}
```

### record-d22b5218f597

2026-06-10T10:00:00Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=protocol

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-84044",
        "source_route": "index-a2fbe9"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-84044",
        "source_route": "index-ff280e"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-84044",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:9f655870122374275591699786a56a0b",
    "configured_route": "index-ff280e",
    "date": "2026-06-10",
    "document_id": "DOC-84044",
    "release_id": "REL-84044"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-81f1bfa5d45e

2026-06-11T10:00:00Z | review | Robin

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-16838",
        "source_route": "index-ff280e"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-16838",
        "source_route": "index-a2fbe9"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-16838",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:3663f4c9249d3034ac6b6dee420f6688",
    "configured_route": "index-ff280e",
    "date": "2026-06-11",
    "document_id": "DOC-16838",
    "release_id": "REL-16838"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-224ad4b44c96

2026-06-12T10:00:00Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=assay_report

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-45155",
        "source_route": "index-ff280e"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-45155",
        "source_route": "index-a2fbe9"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-45155",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:ceeed919c88d8d9e5e854be79ba5a00f",
    "configured_route": "index-ff280e",
    "date": "2026-06-12",
    "document_id": "DOC-45155",
    "release_id": "REL-45155"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-8dcd23da0b11

2026-06-14T08:00:00Z | tool | runtime

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=assay_report


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
  "request_id": "request-05e6f4a2b8b4"
}
```

### record-e512ee6b4600

2026-06-14T08:01:00Z | tool | runtime

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol


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
  "request_id": "request-fcffd1932397"
}
```

### record-44fd07ab1666

2026-06-14T08:02:00Z | tool | runtime

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=protocol


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
  "request_id": "request-72fda7697628"
}
```

### record-6c5c513995a3

2026-06-14T08:03:00Z | tool | runtime

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=protocol


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
  "request_id": "request-df6351336462"
}
```

### record-b01efe4fec7e

2026-06-14T08:04:00Z | tool | runtime

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=assay_report


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
  "request_id": "request-01af00a4c55c"
}
```

### record-ede5181940d8

2026-06-14T08:05:00Z | tool | runtime

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol


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
  "request_id": "request-67cb2a2aebc1"
}
```

### record-13e1a2e6294b

2026-06-14T09:00:00Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Delivery timestamp approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-97498",
        "source_route": "index-ff280e"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "delivery_timestamp": "2026-06-14T08:00:00Z",
        "release_id": "REL-97498",
        "source_route": "index-a2fbe9"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-97498",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:d616ac0560988246040aa3acfbc40e31",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-97498",
    "release_id": "REL-97498"
  },
  "format": "raw",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-182c814827e2

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=assay_report


```json
{
  "event": "preference",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:cb8c3d1011fd9435a622ae068c5197d7",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-95640",
    "release_id": "REL-95640"
  },
  "message": "My preference for this work item is that source_route should be 'index-a2fbe9'.",
  "proposed_fields": {
    "checksum_check": "required",
    "release_id": "REL-95640",
    "source_route": "index-a2fbe9"
  }
}
```

### record-1b8caa2517aa

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=assay_report

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Updated the proposed export.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-81383",
        "source_route": "index-ff280e"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-81383",
        "source_route": "index-a2fbe9"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-81383",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:ab52693bc3aa41ec4775c1660af4628b",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-81383",
    "release_id": "REL-81383"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-2a088c7e0181

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=protocol


```json
{
  "event": "preference",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:b3efc03078df72e5c3e3e370d69aad0f",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-54355",
    "release_id": "REL-54355"
  },
  "message": "My preference for this work item is that source_route should be 'index-ff280e'.",
  "proposed_fields": {
    "checksum_check": "required",
    "release_id": "REL-54355",
    "source_route": "index-ff280e"
  }
}
```

### record-2e670c7b559c

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=protocol

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Updated the proposed export.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-80347",
        "source_route": "index-ff280e"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-80347",
        "source_route": "index-a2fbe9"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-80347",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:c2c0d39592a9271e3b5010eeea4d5816",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-80347",
    "release_id": "REL-80347"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-372fdb213dec

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Updated the proposed export.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-12496",
        "source_route": "index-a2fbe9"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-12496",
        "source_route": "index-ff280e"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-12496",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:654cbf422e19bfa7073e0b542d0dd3ed",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-12496",
    "release_id": "REL-12496"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-45e2b15510c4

2026-06-14T09:00:00Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol

- decision: reject
- reviewed_fields: []
- authority_ref: record-7f4d5b2ba261
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-51704",
        "source_route": "index-a2fbe9"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-51704",
        "source_route": "index-ff280e"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-51704",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:56a407adf855da5238e62918900f21d6",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-51704",
    "release_id": "REL-51704"
  },
  "format": "raw",
  "rejected_artifact": "replacement",
  "reviewed_fields": []
}
```

### record-471d0905dd28

2026-06-14T09:00:00Z | review | Robin

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=assay_report

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Delivery timestamp approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-81191",
        "source_route": "index-a2fbe9"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "delivery_timestamp": "2026-06-14T08:00:00Z",
        "release_id": "REL-81191",
        "source_route": "index-ff280e"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-81191",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:7277341108cd1a022acbf4ebf28600bb",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-81191",
    "release_id": "REL-81191"
  },
  "format": "raw",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-52de3cf98f9e

2026-06-14T09:00:00Z | review | Robin

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=protocol

- decision: reject
- reviewed_fields: []
- authority_ref: record-7f4d5b2ba261
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-61411",
        "source_route": "index-a2fbe9"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-61411",
        "source_route": "index-ff280e"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-61411",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:2f06cb1e7a5983af78413f1701f5745e",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-61411",
    "release_id": "REL-61411"
  },
  "format": "raw",
  "rejected_artifact": "replacement",
  "reviewed_fields": []
}
```

### record-54a85dd1314b

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=assay_report


```json
{
  "event": "preference",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:d2a61bc5052fa0f7a163da072b6ac8ff",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-25662",
    "release_id": "REL-25662"
  },
  "message": "My preference for this work item is that source_route should be 'index-ff280e'.",
  "proposed_fields": {
    "checksum_check": "required",
    "release_id": "REL-25662",
    "source_route": "index-ff280e"
  }
}
```

### record-5659217b378f

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=assay_report


```json
{
  "event": "preference",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:0155373903a58204826f6f6c9da63221",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-96427",
    "release_id": "REL-96427"
  },
  "message": "My preference for this work item is that source_route should be 'index-a2fbe9'.",
  "proposed_fields": {
    "checksum_check": "required",
    "release_id": "REL-96427",
    "source_route": "index-a2fbe9"
  }
}
```

### record-56d7fa47b746

2026-06-14T09:00:00Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol

- decision: reject
- reviewed_fields: []
- authority_ref: record-7f4d5b2ba261
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-48983",
        "source_route": "index-ff280e"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-48983",
        "source_route": "index-a2fbe9"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-48983",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:4bb36afa7e9abdf620fe9648ff6ec5b7",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-48983",
    "release_id": "REL-48983"
  },
  "format": "raw",
  "rejected_artifact": "replacement",
  "reviewed_fields": []
}
```

### record-5c1062bf007d

2026-06-14T09:00:00Z | review | Robin

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=assay_report

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Delivery timestamp approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-71584",
        "source_route": "index-a2fbe9"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "delivery_timestamp": "2026-06-14T08:00:00Z",
        "release_id": "REL-71584",
        "source_route": "index-ff280e"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-71584",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:95c266a3a34821688a5f612aa603c7e4",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-71584",
    "release_id": "REL-71584"
  },
  "format": "raw",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-5cb90703eaf1

2026-06-14T09:00:00Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Delivery timestamp approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-45252",
        "source_route": "index-ff280e"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "delivery_timestamp": "2026-06-14T08:00:00Z",
        "release_id": "REL-45252",
        "source_route": "index-a2fbe9"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-45252",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:dd91c4cc6d6b6607197f088e9679d5d5",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-45252",
    "release_id": "REL-45252"
  },
  "format": "raw",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-5f94e1773a60

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=assay_report

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Updated the proposed export.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-67460",
        "source_route": "index-ff280e"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-67460",
        "source_route": "index-a2fbe9"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-67460",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:2ea83847103f2fa6bb7557e835d39f91",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-67460",
    "release_id": "REL-67460"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-607c9e454fe8

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=assay_report


```json
{
  "event": "preference",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:97962a12ff52ce5d2d45f9332e5d421d",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-15903",
    "release_id": "REL-15903"
  },
  "message": "My preference for this work item is that source_route should be 'index-ff280e'.",
  "proposed_fields": {
    "checksum_check": "required",
    "release_id": "REL-15903",
    "source_route": "index-ff280e"
  }
}
```

### record-62cfecdd4613

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol


```json
{
  "event": "preference",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:4dac41a7f3d05225d8c73f78174dedd6",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-48399",
    "release_id": "REL-48399"
  },
  "message": "My preference for this work item is that source_route should be 'index-a2fbe9'.",
  "proposed_fields": {
    "checksum_check": "required",
    "release_id": "REL-48399",
    "source_route": "index-a2fbe9"
  }
}
```

### record-69bad3c7744f

2026-06-14T09:00:00Z | review | Robin

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=protocol

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Delivery timestamp approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-80535",
        "source_route": "index-a2fbe9"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "delivery_timestamp": "2026-06-14T08:00:00Z",
        "release_id": "REL-80535",
        "source_route": "index-ff280e"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-80535",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:b1a825014945901c84793195141951de",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-80535",
    "release_id": "REL-80535"
  },
  "format": "raw",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-7295fa8b1182

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=protocol


```json
{
  "event": "preference",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:e4db4338ddfd2464a298d6997717b308",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-96930",
    "release_id": "REL-96930"
  },
  "message": "My preference for this work item is that source_route should be 'index-a2fbe9'.",
  "proposed_fields": {
    "checksum_check": "required",
    "release_id": "REL-96930",
    "source_route": "index-a2fbe9"
  }
}
```

### record-82d8f6f2e022

2026-06-14T09:00:00Z | review | Robin

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=protocol

- decision: reject
- reviewed_fields: []
- authority_ref: record-7f4d5b2ba261
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-58963",
        "source_route": "index-ff280e"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-58963",
        "source_route": "index-a2fbe9"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-58963",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:bcdf26742a11afdaa5ada01c3829f5ed",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-58963",
    "release_id": "REL-58963"
  },
  "format": "raw",
  "rejected_artifact": "replacement",
  "reviewed_fields": []
}
```

### record-83f80afe05db

2026-06-14T09:00:00Z | review | Robin

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=assay_report

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Delivery timestamp approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-94599",
        "source_route": "index-ff280e"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "delivery_timestamp": "2026-06-14T08:00:00Z",
        "release_id": "REL-94599",
        "source_route": "index-a2fbe9"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-94599",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:4eab3a0683db79c14b548039b1af2a21",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-94599",
    "release_id": "REL-94599"
  },
  "format": "raw",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-8ad95fea1ef6

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=assay_report


```json
{
  "event": "preference",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:dd63ec4747ebbbb324e4caaa366acf3a",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-49767",
    "release_id": "REL-49767"
  },
  "message": "My preference for this work item is that source_route should be 'index-a2fbe9'.",
  "proposed_fields": {
    "checksum_check": "required",
    "release_id": "REL-49767",
    "source_route": "index-a2fbe9"
  }
}
```

### record-8ce9f927687c

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=assay_report

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Updated the proposed export.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-39437",
        "source_route": "index-a2fbe9"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-39437",
        "source_route": "index-ff280e"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-39437",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:072c88cbe74f511bcceae8b7532e2564",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-39437",
    "release_id": "REL-39437"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-9a87a2c6ba69

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol


```json
{
  "event": "preference",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:9fcc7a985d0809d2642454007323151e",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-19763",
    "release_id": "REL-19763"
  },
  "message": "My preference for this work item is that source_route should be 'index-ff280e'.",
  "proposed_fields": {
    "checksum_check": "required",
    "release_id": "REL-19763",
    "source_route": "index-ff280e"
  }
}
```

### record-9c66a589d409

2026-06-14T09:00:00Z | revision | work-item-author

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=assay_report


```json
{
  "event": "preference",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:53efed5a68d509601e171cb33d7ca93f",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-61271",
    "release_id": "REL-61271"
  },
  "message": "My preference for this work item is that source_route should be 'index-ff280e'.",
  "proposed_fields": {
    "checksum_check": "required",
    "release_id": "REL-61271",
    "source_route": "index-ff280e"
  }
}
```

### record-9f774abc0b1d

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=assay_report

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Updated the proposed export.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-89802",
        "source_route": "index-a2fbe9"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-89802",
        "source_route": "index-ff280e"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-89802",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:ca431f6b3000e6e6843c9a29b8542bc9",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-89802",
    "release_id": "REL-89802"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-a33bb373c43f

2026-06-14T09:00:00Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=assay_report

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Delivery timestamp approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-21622",
        "source_route": "index-a2fbe9"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "delivery_timestamp": "2026-06-14T08:00:00Z",
        "release_id": "REL-21622",
        "source_route": "index-ff280e"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-21622",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:74ba45ed81a5c8be9d685a3672aafa9f",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-21622",
    "release_id": "REL-21622"
  },
  "format": "raw",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-b94ee59d03d2

2026-06-14T09:00:00Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=assay_report

- decision: reject
- reviewed_fields: []
- authority_ref: record-7f4d5b2ba261
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-71623",
        "source_route": "index-a2fbe9"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-71623",
        "source_route": "index-ff280e"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-71623",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:dd81249ce6b0fb98489c278c93ab1fc5",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-71623",
    "release_id": "REL-71623"
  },
  "format": "raw",
  "rejected_artifact": "replacement",
  "reviewed_fields": []
}
```

### record-be9f65676802

2026-06-14T09:00:00Z | review | Robin

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol

- decision: reject
- reviewed_fields: []
- authority_ref: record-7f4d5b2ba261
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-26652",
        "source_route": "index-a2fbe9"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-26652",
        "source_route": "index-ff280e"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-26652",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:61ca7ad91d57aa1433fbdb8b3bfaa798",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-26652",
    "release_id": "REL-26652"
  },
  "format": "raw",
  "rejected_artifact": "replacement",
  "reviewed_fields": []
}
```

### record-bf5821ae3b97

2026-06-14T09:00:00Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol

- decision: reject
- reviewed_fields: []
- authority_ref: record-7f4d5b2ba261
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-71964",
        "source_route": "index-ff280e"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-71964",
        "source_route": "index-a2fbe9"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-71964",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:12a9573a51f3d4775b942ab7cf8fd512",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-71964",
    "release_id": "REL-71964"
  },
  "format": "raw",
  "rejected_artifact": "replacement",
  "reviewed_fields": []
}
```

### record-c9407bfb56aa

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=protocol

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Updated the proposed export.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-23280",
        "source_route": "index-ff280e"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-23280",
        "source_route": "index-a2fbe9"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-23280",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:77325f73d8b73e2ea0637c1fe25678bd",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-23280",
    "release_id": "REL-23280"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-d647987fc5d1

2026-06-14T09:00:00Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=assay_report

- decision: reject
- reviewed_fields: []
- authority_ref: record-7f4d5b2ba261
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-24635",
        "source_route": "index-ff280e"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-24635",
        "source_route": "index-a2fbe9"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-24635",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:6cad527cc208b78297f73ed31ac5e8cc",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-24635",
    "release_id": "REL-24635"
  },
  "format": "raw",
  "rejected_artifact": "replacement",
  "reviewed_fields": []
}
```

### record-da8481497f73

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Updated the proposed export.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-24735",
        "source_route": "index-a2fbe9"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-24735",
        "source_route": "index-ff280e"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-24735",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:930f525b90f3faed735ba1c1907f0c1a",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-24735",
    "release_id": "REL-24735"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-de492c370f7d

2026-06-14T09:00:00Z | review | Robin

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=assay_report

- decision: reject
- reviewed_fields: []
- authority_ref: record-7f4d5b2ba261
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-24853",
        "source_route": "index-ff280e"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-24853",
        "source_route": "index-a2fbe9"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-24853",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:8446cf39c5c7c90a2eb51c3f0b62d318",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-24853",
    "release_id": "REL-24853"
  },
  "format": "raw",
  "rejected_artifact": "replacement",
  "reviewed_fields": []
}
```

### record-e0edee364361

2026-06-14T09:00:00Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=assay_report

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Delivery timestamp approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-96236",
        "source_route": "index-a2fbe9"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "delivery_timestamp": "2026-06-14T08:00:00Z",
        "release_id": "REL-96236",
        "source_route": "index-ff280e"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-96236",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:3e6f3636018540446f8b8044437308b5",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-96236",
    "release_id": "REL-96236"
  },
  "format": "raw",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-e295cc222665

2026-06-14T09:00:00Z | review | Robin

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=assay_report

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Delivery timestamp approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-56364",
        "source_route": "index-a2fbe9"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "delivery_timestamp": "2026-06-14T08:00:00Z",
        "release_id": "REL-56364",
        "source_route": "index-ff280e"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-56364",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:7b36168192af5283fd982550da676dd9",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-56364",
    "release_id": "REL-56364"
  },
  "format": "raw",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-eb2e99a511fb

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=assay_report

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Updated the proposed export.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-42475",
        "source_route": "index-ff280e"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-42475",
        "source_route": "index-a2fbe9"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-42475",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:d144cde3400ce9da55d25ac92c01123d",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-42475",
    "release_id": "REL-42475"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-ef3196012861

2026-06-14T09:00:00Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol

- decision: accept
- reviewed_fields: ['delivery_timestamp']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Delivery timestamp approved.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-95049",
        "source_route": "index-a2fbe9"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "delivery_timestamp": "2026-06-14T08:00:00Z",
        "release_id": "REL-95049",
        "source_route": "index-ff280e"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Delivery timestamp approved.",
  "decision": "accept",
  "document_id": "DOC-95049",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:eabbc8461266ef536c7d55c0cf0c2fbd",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-95049",
    "release_id": "REL-95049"
  },
  "format": "raw",
  "reviewed_fields": [
    "delivery_timestamp"
  ]
}
```

### record-fec0126b8e51

2026-06-14T09:00:00Z | review | Robin

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=assay_report

- decision: reject
- reviewed_fields: []
- authority_ref: record-7f4d5b2ba261
- comment: Rejected because the signature block is missing. Field-level review was not completed.

```json
{
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-95491",
        "source_route": "index-ff280e"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-95491",
        "source_route": "index-a2fbe9"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Rejected because the signature block is missing. Field-level review was not completed.",
  "decision": "reject",
  "document_id": "DOC-95491",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:5621a8cd204132c242dd1253ea29c9db",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-95491",
    "release_id": "REL-95491"
  },
  "format": "raw",
  "rejected_artifact": "replacement",
  "reviewed_fields": []
}
```

### record-fee87ba5b8a2

2026-06-14T09:00:00Z | revision | document-editor

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=assay_report

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-7f4d5b2ba261
- accepted_artifact: replacement
- comment: Updated the proposed export.

```json
{
  "accepted_artifact": "replacement",
  "artifacts": {
    "draft": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-16541",
        "source_route": "index-a2fbe9"
      },
      "revision": "draft"
    },
    "replacement": {
      "fields": {
        "checksum_check": "required",
        "release_id": "REL-16541",
        "source_route": "index-ff280e"
      },
      "revision": "reviewed"
    }
  },
  "authority_ref": "record-7f4d5b2ba261",
  "comment": "Updated the proposed export.",
  "decision": "accept",
  "document_id": "DOC-16541",
  "event": "review",
  "facts": {
    "alternative_route": "index-a2fbe9",
    "checksum": "sha256:11bc6bd1d3c8f92dadad9c7bdc59f647",
    "configured_route": "index-ff280e",
    "date": "2026-06-14",
    "document_id": "DOC-16541",
    "release_id": "REL-16541"
  },
  "format": "raw",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-46c478584a37

2026-06-14T11:00:00Z | revision | forwarding-service

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol

- origin_ref: record-fdf86322160f

```json
{
  "event": "forward",
  "message": "Forwarded artifact for the next work item.",
  "origin_ref": "record-fdf86322160f"
}
```

### record-89bdb57ebfb1

2026-06-14T11:01:00Z | revision | forwarding-service

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol

- origin_ref: record-fdf86322160f

```json
{
  "event": "forward",
  "message": "Forwarded artifact for the next work item.",
  "origin_ref": "record-fdf86322160f"
}
```

### record-faeac1254957

2026-06-14T11:02:00Z | revision | forwarding-service

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol

- origin_ref: record-fdf86322160f

```json
{
  "event": "forward",
  "message": "Forwarded artifact for the next work item.",
  "origin_ref": "record-fdf86322160f"
}
```

### record-a2e1f05d3788

2026-06-14T11:03:00Z | revision | forwarding-service

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol

- origin_ref: record-fdf86322160f

```json
{
  "event": "forward",
  "message": "Forwarded artifact for the next work item.",
  "origin_ref": "record-fdf86322160f"
}
```

### record-7ae4e7bf0a82

2026-06-14T11:04:00Z | revision | forwarding-service

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol

- origin_ref: record-d22b5218f597

```json
{
  "event": "forward",
  "message": "Forwarded artifact for the next work item.",
  "origin_ref": "record-d22b5218f597"
}
```

### record-44f4243ac8f2

2026-06-14T11:05:00Z | revision | forwarding-service

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol

- origin_ref: record-d22b5218f597

```json
{
  "event": "forward",
  "message": "Forwarded artifact for the next work item.",
  "origin_ref": "record-d22b5218f597"
}
```

### record-2153099b3f5c

2026-06-14T11:06:00Z | revision | forwarding-service

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=protocol

- origin_ref: record-d22b5218f597

```json
{
  "event": "forward",
  "message": "Forwarded artifact for the next work item.",
  "origin_ref": "record-d22b5218f597"
}
```

### record-ed4131e304da

2026-06-14T11:07:00Z | revision | forwarding-service

Context: task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=assay_report

- origin_ref: record-81f1bfa5d45e

```json
{
  "event": "forward",
  "message": "Forwarded artifact for the next work item.",
  "origin_ref": "record-81f1bfa5d45e"
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
| record-fdf86322160f | edition-de7fcc0e8a7b | task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-de7fcc0e8a7b, collection=active, document_class=protocol | 0 |
| record-d22b5218f597 | edition-c2b92d1fed69 | task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=protocol | 0 |
| record-81f1bfa5d45e | edition-c2b92d1fed69 | task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=active, document_class=protocol | 1 |
| record-224ad4b44c96 | edition-c2b92d1fed69 | task_family=document_retrieval, workflow=workflow-ff280ea2fbe9, version=edition-c2b92d1fed69, collection=archive, document_class=assay_report | 1 |

### Competing requirement explanations

Zero is the configured baseline; one is the alternative. Each row is a distinct
compatible function for this version. No preference for simplicity removes a row.
The private sampling plan and world policy do not filter these explanations.

Version edition-c2b92d1fed69: 1 compatible functions.

| Function | collection=active, document_class=protocol | collection=active, document_class=assay_report | collection=archive, document_class=protocol | collection=archive, document_class=assay_report | Complexity |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 1 | 1 | 0 | 1 | 2 |

Version edition-de7fcc0e8a7b: 7 compatible functions.

| Function | collection=active, document_class=protocol | collection=active, document_class=assay_report | collection=archive, document_class=protocol | collection=archive, document_class=assay_report | Complexity |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | 0 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 | 1 | 2 |
| 3 | 0 | 0 | 1 | 0 | 2 |
| 4 | 0 | 0 | 1 | 1 | 1 |
| 5 | 0 | 1 | 0 | 0 | 2 |
| 6 | 0 | 1 | 0 | 1 | 1 |
| 7 | 0 | 1 | 1 | 1 | 2 |

### Diagnostic and control derivations

| Task | Context observed | Witnesses | Action | Retention basis |
| --- | --- | --- | --- | --- |
| diagnostic | False | none | apply | not_retention |
| control | True | record-d22b5218f597 | keep | resolved |

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
      "version": "edition-c2b92d1fed69",
      "workflow": "workflow-ff280ea2fbe9"
    },
    {
      "collection": "active",
      "document_class": "protocol",
      "task_family": "document_retrieval",
      "version": "edition-c2b92d1fed69",
      "workflow": "workflow-ff280ea2fbe9"
    },
    {
      "collection": "archive",
      "document_class": "assay_report",
      "task_family": "document_retrieval",
      "version": "edition-c2b92d1fed69",
      "workflow": "workflow-ff280ea2fbe9"
    }
  ],
  "diagnostic_observed": false,
  "material_revision": "v04-amendment-03",
  "record_count": 60,
  "registered_versions": [
    "edition-de7fcc0e8a7b",
    "edition-c2b92d1fed69"
  ],
  "rendering": "raw",
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
| approval_without_target | 10 | 0 | 6 | 4 | 0 | 0 | 0 | record-471d0905dd28, record-5c1062bf007d, record-a33bb373c43f, record-e0edee364361, record-e295cc222665, record-ef3196012861 |
| forward | 8 | 0 | 6 | 2 | 0 | 0 | 0 | record-46c478584a37, record-89bdb57ebfb1, record-faeac1254957, record-a2e1f05d3788, record-7ae4e7bf0a82, record-44f4243ac8f2 |
| old_approval | 1 | 0 | 1 | 0 | 0 | 0 | 0 | record-fdf86322160f |
| rejected_opposite_artifact | 10 | 0 | 4 | 6 | 0 | 0 | 0 | record-45e2b15510c4, record-82d8f6f2e022, record-b94ee59d03d2, record-be9f65676802 |
| target_field_preference | 10 | 0 | 5 | 5 | 0 | 0 | 0 | record-54a85dd1314b, record-607c9e454fe8, record-7295fa8b1182, record-9a87a2c6ba69, record-9c66a589d409 |
| unauthorised_revision | 10 | 0 | 7 | 3 | 0 | 0 | 0 | record-2e670c7b559c, record-372fdb213dec, record-8ce9f927687c, record-9f774abc0b1d, record-c9407bfb56aa, record-da8481497f73, record-fee87ba5b8a2 |

### Every promoted public record

| Record | Type | Origin | Public option | Remaining policies | Outcome | Qualifies | Diagnostic action | Control action |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| record-fdf86322160f | old_approval | record-fdf86322160f | 0 | 0 | contradiction | True | None | None |
| record-13e1a2e6294b | approval_without_target | record-13e1a2e6294b | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-182c814827e2 | target_field_preference | record-182c814827e2 | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-1b8caa2517aa | unauthorised_revision | record-1b8caa2517aa | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-2a088c7e0181 | target_field_preference | record-2a088c7e0181 | 0 | 7 | unchanged_constraints | False | apply | keep |
| record-2e670c7b559c | unauthorised_revision | record-2e670c7b559c | 1 | 0 | contradiction | True | None | None |
| record-372fdb213dec | unauthorised_revision | record-372fdb213dec | 0 | 0 | contradiction | True | None | None |
| record-45e2b15510c4 | rejected_opposite_artifact | record-45e2b15510c4 | 0 | 0 | contradiction | True | None | None |
| record-471d0905dd28 | approval_without_target | record-471d0905dd28 | 0 | 0 | contradiction | True | None | None |
| record-52de3cf98f9e | rejected_opposite_artifact | record-52de3cf98f9e | 0 | 7 | unchanged_constraints | False | apply | keep |
| record-54a85dd1314b | target_field_preference | record-54a85dd1314b | 0 | 0 | contradiction | True | None | None |
| record-5659217b378f | target_field_preference | record-5659217b378f | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-56d7fa47b746 | rejected_opposite_artifact | record-56d7fa47b746 | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-5c1062bf007d | approval_without_target | record-5c1062bf007d | 0 | 0 | contradiction | True | None | None |
| record-5cb90703eaf1 | approval_without_target | record-5cb90703eaf1 | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-5f94e1773a60 | unauthorised_revision | record-5f94e1773a60 | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-607c9e454fe8 | target_field_preference | record-607c9e454fe8 | 0 | 0 | contradiction | True | None | None |
| record-62cfecdd4613 | target_field_preference | record-62cfecdd4613 | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-69bad3c7744f | approval_without_target | record-69bad3c7744f | 0 | 7 | unchanged_constraints | False | apply | keep |
| record-7295fa8b1182 | target_field_preference | record-7295fa8b1182 | 1 | 0 | contradiction | True | None | None |
| record-82d8f6f2e022 | rejected_opposite_artifact | record-82d8f6f2e022 | 1 | 0 | contradiction | True | None | None |
| record-83f80afe05db | approval_without_target | record-83f80afe05db | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-8ad95fea1ef6 | target_field_preference | record-8ad95fea1ef6 | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-8ce9f927687c | unauthorised_revision | record-8ce9f927687c | 0 | 0 | contradiction | True | None | None |
| record-9a87a2c6ba69 | target_field_preference | record-9a87a2c6ba69 | 0 | 0 | contradiction | True | None | None |
| record-9c66a589d409 | target_field_preference | record-9c66a589d409 | 0 | 0 | contradiction | True | None | None |
| record-9f774abc0b1d | unauthorised_revision | record-9f774abc0b1d | 0 | 0 | contradiction | True | None | None |
| record-a33bb373c43f | approval_without_target | record-a33bb373c43f | 0 | 0 | contradiction | True | None | None |
| record-b94ee59d03d2 | rejected_opposite_artifact | record-b94ee59d03d2 | 0 | 0 | contradiction | True | None | None |
| record-be9f65676802 | rejected_opposite_artifact | record-be9f65676802 | 0 | 0 | contradiction | True | None | None |
| record-bf5821ae3b97 | rejected_opposite_artifact | record-bf5821ae3b97 | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-c9407bfb56aa | unauthorised_revision | record-c9407bfb56aa | 1 | 0 | contradiction | True | None | None |
| record-d647987fc5d1 | rejected_opposite_artifact | record-d647987fc5d1 | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-da8481497f73 | unauthorised_revision | record-da8481497f73 | 0 | 0 | contradiction | True | None | None |
| record-de492c370f7d | rejected_opposite_artifact | record-de492c370f7d | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-e0edee364361 | approval_without_target | record-e0edee364361 | 0 | 0 | contradiction | True | None | None |
| record-e295cc222665 | approval_without_target | record-e295cc222665 | 0 | 0 | contradiction | True | None | None |
| record-eb2e99a511fb | unauthorised_revision | record-eb2e99a511fb | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-ef3196012861 | approval_without_target | record-ef3196012861 | 0 | 0 | contradiction | True | None | None |
| record-fec0126b8e51 | rejected_opposite_artifact | record-fec0126b8e51 | 1 | 7 | unchanged_constraints | False | apply | keep |
| record-fee87ba5b8a2 | unauthorised_revision | record-fee87ba5b8a2 | 0 | 0 | contradiction | True | None | None |
| record-46c478584a37 | forward | record-fdf86322160f | 0 | 0 | contradiction | True | None | None |
| record-89bdb57ebfb1 | forward | record-fdf86322160f | 0 | 0 | contradiction | True | None | None |
| record-faeac1254957 | forward | record-fdf86322160f | 0 | 0 | contradiction | True | None | None |
| record-a2e1f05d3788 | forward | record-fdf86322160f | 0 | 0 | contradiction | True | None | None |
| record-7ae4e7bf0a82 | forward | record-d22b5218f597 | 0 | 0 | contradiction | True | None | None |
| record-44f4243ac8f2 | forward | record-d22b5218f597 | 0 | 0 | contradiction | True | None | None |
| record-2153099b3f5c | forward | record-d22b5218f597 | 0 | 7 | unchanged_constraints | False | apply | keep |
| record-ed4131e304da | forward | record-81f1bfa5d45e | 1 | 7 | unchanged_constraints | False | apply | keep |

### Exact promotions, contexts and public value provenance

The [complete JSON sidecar](S5-retrieval.json) preserves every intervention under `counterfactual.records`,
including selected field presence/value, effective current context, public origin,
precise promotion and remaining-policy count. No intervention alters the real history.

## Future tasks for this development example

### diagnostic

Public task

```json
{
  "task_id": "task-75f644cea7dd",
  "context": {
    "task_family": "document_retrieval",
    "workflow": "workflow-ff280ea2fbe9",
    "version": "edition-c2b92d1fed69",
    "collection": "active",
    "document_class": "assay_report"
  },
  "facts": {
    "document_id": "DOC-67900",
    "date": "2026-06-15",
    "configured_route": "index-ff280e",
    "alternative_route": "index-a2fbe9",
    "release_id": "REL-67900",
    "checksum": "sha256:92c206f3d4d58c804b275d643a35a37f"
  },
  "baseline_fields": [
    {
      "name": "source_route",
      "value": "index-ff280e"
    },
    {
      "name": "release_id",
      "value": "REL-67900"
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
  "task_id": "task-75f644cea7dd",
  "history_id": "history-70c8ae5e7fe9",
  "probe": "diagnostic",
  "expected_decision": "apply",
  "recoverable": true,
  "world_fields": [
    {
      "name": "source_route",
      "value": "index-a2fbe9"
    },
    {
      "name": "release_id",
      "value": "REL-67900"
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
  "task_id": "task-8ba87cb6364f",
  "context": {
    "task_family": "document_retrieval",
    "workflow": "workflow-ff280ea2fbe9",
    "version": "edition-c2b92d1fed69",
    "collection": "archive",
    "document_class": "protocol"
  },
  "facts": {
    "document_id": "DOC-24516",
    "date": "2026-06-15",
    "configured_route": "index-ff280e",
    "alternative_route": "index-a2fbe9",
    "release_id": "REL-24516",
    "checksum": "sha256:52bbbc8f039d0e16d3fb28c067e03747"
  },
  "baseline_fields": [
    {
      "name": "source_route",
      "value": "index-ff280e"
    },
    {
      "name": "release_id",
      "value": "REL-24516"
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
  "task_id": "task-8ba87cb6364f",
  "history_id": "history-70c8ae5e7fe9",
  "probe": "control",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "source_route",
      "value": "index-ff280e"
    },
    {
      "name": "release_id",
      "value": "REL-24516"
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
