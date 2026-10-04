# S4 / retrieval

Material revision: v04-amendment-03-r2. Synthetic development example.

[Frozen surface-selector audit](surface-audit.md) · [Complete audit JSON](surface-audit.json).
Its per-history results use this case’s history ID; selector choice used only separate development histories.

Registered task type: **resolved_retention_transfer**. Intended diagnostic regime: **resolved_keep**.
Public records: 6. Control basis: resolved_keep.

## Review summary

Current compatible functions: **1**. Full cross-version policies: 7.

H14 identification is conditional on excluding XOR and XNOR. Retaining an unresolved
baseline does not establish that the baseline is the true requirement.

| Task | Public context | Previously observed | Warranted action | Retention basis |
| --- | --- | --- | --- | --- |
| diagnostic | task_family=document_retrieval, workflow=workflow-891f5dfcb0f4, version=edition-63094e2a57bb, collection=archive, document_class=assay_report | False | keep | resolved |
| control | task_family=document_retrieval, workflow=workflow-891f5dfcb0f4, version=edition-63094e2a57bb, collection=archive, document_class=protocol | True | keep | resolved |

Counterfactual qualification requires **contradiction** for every present type. All present types qualify: **True**.

One qualifying example per present type is shown below. The links lead to its
public evidence; all records and counts appear in the later audit and JSON sidecar.

| Type (record count) | Promoted record / source | Public target value | Exact promotion | Outcome / remaining policies |
| --- | --- | --- | --- | --- |
| old_approval (1) | [record-c98c5f595368](#record-c98c5f595368) | source_route = 'index-fcb0f4' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=document_retrieval, workflow=workflow-891f5dfcb0f4, version=edition-63094e2a57bb, collection=archive, document_class=assay_report | contradiction / 0 |

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
  "workflow": "workflow-891f5dfcb0f4"
}
```

This is a bounded synthetic workflow model. initial_configuration declares the field options, two context dimensions and the complete H14 hypothesis class. Each registered version has one class member. A field observation constrains the member indexed by its recorded version. Broader consequences follow from the declared class. Facts provide current artifact values. Other fields retain their configured baseline. Outside the declared task_family and workflow, or without a complete declared context, no update is authorised by this model. A register_version event supplies trusted workflow metadata with the authority roster and half-open validity interval. Binding field approval is an event of type review with decision accept, performed by a listed reviewer within that interval, with the field included in reviewed_fields. Its accepted artifact establishes the field configuration at the recorded context. This explicit approval convention is a supplied synthetic assumption. A forward has an origin_ref identifying the record whose content it reproduces. Raw artifacts expose named revisions and a selected artifact reference; interpreted records expose the selected fields directly. A rejection records a whole-artifact decision and its stated grounds. An artifact field whose review is not recorded has no approved assignment. The configured baseline is retained when the available evidence does not establish an update. Dates and version labels in new work identify the applicable registration.

## Public work records

### record-bef7444d2efe

2026-06-05T10:51:20Z | review | Elena

Context: task_family=document_retrieval, workflow=workflow-891f5dfcb0f4, version=edition-63094e2a57bb, collection=archive, document_class=protocol

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-0289b140f7f7
- comment: Completed.

```json
{
  "accepted_fields": {
    "checksum_check": "required",
    "release_id": "REL-67407",
    "source_route": "index-891f5d"
  },
  "authority_ref": "record-0289b140f7f7",
  "change_summary": {
    "after": "index-891f5d",
    "before": "index-fcb0f4",
    "field": "source_route"
  },
  "comment": "Completed.",
  "decision": "accept",
  "document_id": "DOC-67407",
  "event": "review",
  "facts": {
    "alternative_route": "index-fcb0f4",
    "checksum": "sha256:54e9beb9db6196b41a8ab57fc7ec05cd",
    "configured_route": "index-891f5d",
    "date": "2026-06-05",
    "document_id": "DOC-67407",
    "release_id": "REL-67407"
  },
  "format": "interpreted",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-3fe900f8a425

2026-06-10T14:28:27Z | review | Robin

Context: task_family=document_retrieval, workflow=workflow-891f5dfcb0f4, version=edition-63094e2a57bb, collection=active, document_class=assay_report

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-0289b140f7f7
- comment: Approved.

```json
{
  "accepted_fields": {
    "checksum_check": "required",
    "release_id": "REL-40810",
    "source_route": "index-891f5d"
  },
  "authority_ref": "record-0289b140f7f7",
  "change_summary": {
    "after": "index-891f5d",
    "before": "index-fcb0f4",
    "field": "source_route"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-40810",
  "event": "review",
  "facts": {
    "alternative_route": "index-fcb0f4",
    "checksum": "sha256:c78ad11c79b1955d1974410cae6cf7f4",
    "configured_route": "index-891f5d",
    "date": "2026-06-10",
    "document_id": "DOC-40810",
    "release_id": "REL-40810"
  },
  "format": "interpreted",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-cccde5fd4d91

2026-06-03T15:24:01Z | review | Robin

Context: task_family=document_retrieval, workflow=workflow-891f5dfcb0f4, version=edition-63094e2a57bb, collection=active, document_class=protocol

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-0289b140f7f7
- comment: Reviewed.

```json
{
  "accepted_fields": {
    "checksum_check": "required",
    "release_id": "REL-95843",
    "source_route": "index-fcb0f4"
  },
  "authority_ref": "record-0289b140f7f7",
  "change_summary": {
    "after": "index-fcb0f4",
    "before": "index-891f5d",
    "field": "source_route"
  },
  "comment": "Reviewed.",
  "decision": "accept",
  "document_id": "DOC-95843",
  "event": "review",
  "facts": {
    "alternative_route": "index-fcb0f4",
    "checksum": "sha256:a1461e78ef5a3c75309e8762644dce0e",
    "configured_route": "index-891f5d",
    "date": "2026-06-03",
    "document_id": "DOC-95843",
    "release_id": "REL-95843"
  },
  "format": "interpreted",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-c98c5f595368

2026-05-24T08:46:18Z | review | Robin

Context: task_family=document_retrieval, workflow=workflow-891f5dfcb0f4, version=edition-ba9a27ca804a, collection=archive, document_class=assay_report

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-61cb6ba05acc
- comment: Reviewed.

```json
{
  "accepted_fields": {
    "checksum_check": "required",
    "release_id": "REL-33803",
    "source_route": "index-fcb0f4"
  },
  "authority_ref": "record-61cb6ba05acc",
  "change_summary": {
    "after": "index-fcb0f4",
    "before": "index-891f5d",
    "field": "source_route"
  },
  "comment": "Reviewed.",
  "decision": "accept",
  "document_id": "DOC-33803",
  "event": "review",
  "facts": {
    "alternative_route": "index-fcb0f4",
    "checksum": "sha256:4f0f5a4b13974748d21b2f05d178207c",
    "configured_route": "index-891f5d",
    "date": "2026-05-24",
    "document_id": "DOC-33803",
    "release_id": "REL-33803"
  },
  "format": "interpreted",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-61cb6ba05acc

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
  "task_family": "document_retrieval",
  "valid_from": "2026-01-01T00:00:00Z",
  "valid_until": "2026-06-01T00:00:00Z",
  "version": "edition-ba9a27ca804a",
  "workflow": "workflow-891f5dfcb0f4"
}
```

### record-0289b140f7f7

2026-06-01T00:00:00Z | template | workflow-registry

Context: 


```json
{
  "authorised_reviewers": [
    "Robin",
    "Elena"
  ],
  "event": "register_version",
  "supersedes": "record-61cb6ba05acc",
  "task_family": "document_retrieval",
  "valid_from": "2026-06-01T00:00:00Z",
  "valid_until": "2027-01-01T00:00:00Z",
  "version": "edition-63094e2a57bb",
  "workflow": "workflow-891f5dfcb0f4"
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
| record-bef7444d2efe | edition-63094e2a57bb | task_family=document_retrieval, workflow=workflow-891f5dfcb0f4, version=edition-63094e2a57bb, collection=archive, document_class=protocol | 0 |
| record-3fe900f8a425 | edition-63094e2a57bb | task_family=document_retrieval, workflow=workflow-891f5dfcb0f4, version=edition-63094e2a57bb, collection=active, document_class=assay_report | 0 |
| record-cccde5fd4d91 | edition-63094e2a57bb | task_family=document_retrieval, workflow=workflow-891f5dfcb0f4, version=edition-63094e2a57bb, collection=active, document_class=protocol | 1 |
| record-c98c5f595368 | edition-ba9a27ca804a | task_family=document_retrieval, workflow=workflow-891f5dfcb0f4, version=edition-ba9a27ca804a, collection=archive, document_class=assay_report | 1 |

### Competing requirement explanations

Zero is the configured baseline; one is the alternative. Each row is a distinct
compatible function for this version. No preference for simplicity removes a row.
The private sampling plan and world policy do not filter these explanations.

Version edition-63094e2a57bb: 1 compatible functions.

| Function | collection=active, document_class=protocol | collection=active, document_class=assay_report | collection=archive, document_class=protocol | collection=archive, document_class=assay_report | Complexity |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 1 | 0 | 0 | 0 | 2 |

Version edition-ba9a27ca804a: 7 compatible functions.

| Function | collection=active, document_class=protocol | collection=active, document_class=assay_report | collection=archive, document_class=protocol | collection=archive, document_class=assay_report | Complexity |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | 0 | 0 | 1 | 2 |
| 2 | 0 | 0 | 1 | 1 | 1 |
| 3 | 0 | 1 | 0 | 1 | 1 |
| 4 | 0 | 1 | 1 | 1 | 2 |
| 5 | 1 | 0 | 1 | 1 | 2 |
| 6 | 1 | 1 | 0 | 1 | 2 |
| 7 | 1 | 1 | 1 | 1 | 0 |

### Diagnostic and control derivations

| Task | Context observed | Witnesses | Action | Retention basis |
| --- | --- | --- | --- | --- |
| diagnostic | False | none | keep | resolved |
| control | True | record-bef7444d2efe | keep | resolved |

## Private material audit

These design labels, counterfactuals and world requirements are evaluator material.
They are never preparation or generation inputs. The true world is distinct from
what the public evidence identifies. Exact world fields are shown with each task.

Registered record counts and construction audit:

```json
{
  "additional_noise_counts": {},
  "admissible_count": 7,
  "control_basis": "resolved_keep",
  "current_admissible_count": 1,
  "current_witness_contexts": [
    {
      "collection": "active",
      "document_class": "protocol",
      "task_family": "document_retrieval",
      "version": "edition-63094e2a57bb",
      "workflow": "workflow-891f5dfcb0f4"
    },
    {
      "collection": "archive",
      "document_class": "protocol",
      "task_family": "document_retrieval",
      "version": "edition-63094e2a57bb",
      "workflow": "workflow-891f5dfcb0f4"
    },
    {
      "collection": "active",
      "document_class": "assay_report",
      "task_family": "document_retrieval",
      "version": "edition-63094e2a57bb",
      "workflow": "workflow-891f5dfcb0f4"
    }
  ],
  "diagnostic_observed": false,
  "material_revision": "v04-amendment-03-r2",
  "record_count": 6,
  "registered_versions": [
    "edition-ba9a27ca804a",
    "edition-63094e2a57bb"
  ],
  "rendering": "interpreted",
  "reversed_option": true,
  "task_type": "resolved_retention_transfer"
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
| old_approval | 1 | 0 | 1 | 0 | 0 | 0 | 0 | record-c98c5f595368 |

### Every promoted public record

| Record | Type | Origin | Public option | Remaining policies | Outcome | Qualifies | Diagnostic action | Control action |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| record-c98c5f595368 | old_approval | record-c98c5f595368 | 1 | 0 | contradiction | True | None | None |

### Exact promotions, contexts and public value provenance

The [complete JSON sidecar](S4-retrieval.json) preserves every intervention under `counterfactual.records`,
including selected field presence/value, effective current context, public origin,
precise promotion and remaining-policy count. No intervention alters the real history.

## Future tasks for this development example

### diagnostic

Public task

```json
{
  "task_id": "task-10dd81571202",
  "context": {
    "task_family": "document_retrieval",
    "workflow": "workflow-891f5dfcb0f4",
    "version": "edition-63094e2a57bb",
    "collection": "archive",
    "document_class": "assay_report"
  },
  "facts": {
    "document_id": "DOC-21057",
    "date": "2026-06-15",
    "configured_route": "index-891f5d",
    "alternative_route": "index-fcb0f4",
    "release_id": "REL-21057",
    "checksum": "sha256:f7bf98840af9a88b922660c0f8939c42"
  },
  "baseline_fields": [
    {
      "name": "source_route",
      "value": "index-891f5d"
    },
    {
      "name": "release_id",
      "value": "REL-21057"
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
  "task_id": "task-10dd81571202",
  "history_id": "history-7b76660c7faa",
  "probe": "diagnostic",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "source_route",
      "value": "index-891f5d"
    },
    {
      "name": "release_id",
      "value": "REL-21057"
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
  "task_id": "task-b96913b3b884",
  "context": {
    "task_family": "document_retrieval",
    "workflow": "workflow-891f5dfcb0f4",
    "version": "edition-63094e2a57bb",
    "collection": "archive",
    "document_class": "protocol"
  },
  "facts": {
    "document_id": "DOC-90991",
    "date": "2026-06-15",
    "configured_route": "index-891f5d",
    "alternative_route": "index-fcb0f4",
    "release_id": "REL-90991",
    "checksum": "sha256:dc325b30090eb2bf3c037675bbcdd685"
  },
  "baseline_fields": [
    {
      "name": "source_route",
      "value": "index-891f5d"
    },
    {
      "name": "release_id",
      "value": "REL-90991"
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
  "task_id": "task-b96913b3b884",
  "history_id": "history-7b76660c7faa",
  "probe": "control",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "source_route",
      "value": "index-891f5d"
    },
    {
      "name": "release_id",
      "value": "REL-90991"
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
