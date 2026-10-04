# S4 / retrieval

Material revision: v04-amendment-03. Synthetic development example.

Registered task type: **resolved_retention_transfer**. Intended diagnostic regime: **resolved_keep**.
Public records: 6. Control basis: resolved_keep.

## Review summary

Current compatible functions: **1**. Full cross-version policies: 7.

H14 identification is conditional on excluding XOR and XNOR. Retaining an unresolved
baseline does not establish that the baseline is the true requirement.

| Task | Public context | Previously observed | Warranted action | Retention basis |
| --- | --- | --- | --- | --- |
| diagnostic | task_family=document_retrieval, workflow=workflow-ba5baa940ec0, version=edition-144a2a828934, collection=archive, document_class=protocol | False | keep | resolved |
| control | task_family=document_retrieval, workflow=workflow-ba5baa940ec0, version=edition-144a2a828934, collection=active, document_class=protocol | True | keep | resolved |

Counterfactual qualification requires **contradiction** for every present type. All present types qualify: **True**.

One qualifying example per present type is shown below. The links lead to its
public evidence; all records and counts appear in the later audit and JSON sidecar.

| Type (record count) | Promoted record / source | Public target value | Exact promotion | Outcome / remaining policies |
| --- | --- | --- | --- | --- |
| old_approval (1) | [record-1a2bde59abdf](#record-1a2bde59abdf) | source_route = 'index-940ec0' | Add this publicly recovered field configuration as one binding current-version observation; preserve all genuine observations. Context: task_family=document_retrieval, workflow=workflow-ba5baa940ec0, version=edition-144a2a828934, collection=active, document_class=assay_report | contradiction / 0 |

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
  "workflow": "workflow-ba5baa940ec0"
}
```

This is a bounded synthetic workflow model. initial_configuration declares the field options, two context dimensions and the complete H14 hypothesis class. Each registered version has one class member. A field observation constrains the member indexed by its recorded version. Broader consequences follow from the declared class. Facts provide current artifact values. Other fields retain their configured baseline. Outside the declared task_family and workflow, or without a complete declared context, no update is authorised by this model. A register_version event supplies trusted workflow metadata with the authority roster and half-open validity interval. Binding field approval is an event of type review with decision accept, performed by a listed reviewer within that interval, with the field included in reviewed_fields. Its accepted artifact establishes the field configuration at the recorded context. This explicit approval convention is a supplied synthetic assumption. A forward has an origin_ref identifying the record whose content it reproduces. Raw artifacts expose named revisions and a selected artifact reference; interpreted records expose the selected fields directly. A rejection records a whole-artifact decision and its stated grounds. An artifact field whose review is not recorded has no approved assignment. The configured baseline is retained when the available evidence does not establish an update. Dates and version labels in new work identify the applicable registration.

## Public work records

### record-5d407371a897

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
  "version": "edition-6760601aaacc",
  "workflow": "workflow-ba5baa940ec0"
}
```

### record-1a2bde59abdf

2026-05-10T10:00:00Z | review | Elena

Context: task_family=document_retrieval, workflow=workflow-ba5baa940ec0, version=edition-6760601aaacc, collection=active, document_class=assay_report

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-5d407371a897
- comment: Approved.

```json
{
  "accepted_fields": {
    "checksum_check": "required",
    "release_id": "REL-97085",
    "source_route": "index-940ec0"
  },
  "authority_ref": "record-5d407371a897",
  "change_summary": {
    "after": "index-940ec0",
    "before": "index-ba5baa",
    "field": "source_route"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-97085",
  "event": "review",
  "facts": {
    "alternative_route": "index-ba5baa",
    "checksum": "sha256:e79c2cb91a52fec33af5e0b5121a4123",
    "configured_route": "index-940ec0",
    "date": "2026-05-10",
    "document_id": "DOC-97085",
    "release_id": "REL-97085"
  },
  "format": "interpreted",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-0b87d3565f74

2026-06-01T00:00:00Z | template | workflow-registry

Context: 


```json
{
  "authorised_reviewers": [
    "Daria",
    "Theo"
  ],
  "event": "register_version",
  "supersedes": "record-5d407371a897",
  "task_family": "document_retrieval",
  "valid_from": "2026-06-01T00:00:00Z",
  "valid_until": "2027-01-01T00:00:00Z",
  "version": "edition-144a2a828934",
  "workflow": "workflow-ba5baa940ec0"
}
```

### record-38d7449f0f05

2026-06-10T10:00:00Z | review | Daria

Context: task_family=document_retrieval, workflow=workflow-ba5baa940ec0, version=edition-144a2a828934, collection=active, document_class=assay_report

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-0b87d3565f74
- comment: Approved.

```json
{
  "accepted_fields": {
    "checksum_check": "required",
    "release_id": "REL-50020",
    "source_route": "index-ba5baa"
  },
  "authority_ref": "record-0b87d3565f74",
  "change_summary": {
    "after": "index-ba5baa",
    "before": "index-940ec0",
    "field": "source_route"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-50020",
  "event": "review",
  "facts": {
    "alternative_route": "index-ba5baa",
    "checksum": "sha256:314befc298f5c5261db83390d7f74d14",
    "configured_route": "index-940ec0",
    "date": "2026-06-10",
    "document_id": "DOC-50020",
    "release_id": "REL-50020"
  },
  "format": "interpreted",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-1a0edc5881b9

2026-06-11T10:00:00Z | review | Theo

Context: task_family=document_retrieval, workflow=workflow-ba5baa940ec0, version=edition-144a2a828934, collection=active, document_class=protocol

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-0b87d3565f74
- comment: Approved.

```json
{
  "accepted_fields": {
    "checksum_check": "required",
    "release_id": "REL-71538",
    "source_route": "index-940ec0"
  },
  "authority_ref": "record-0b87d3565f74",
  "change_summary": {
    "after": "index-940ec0",
    "before": "index-ba5baa",
    "field": "source_route"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-71538",
  "event": "review",
  "facts": {
    "alternative_route": "index-ba5baa",
    "checksum": "sha256:eff5e71ec5dd74c13fac9dcd847d2473",
    "configured_route": "index-940ec0",
    "date": "2026-06-11",
    "document_id": "DOC-71538",
    "release_id": "REL-71538"
  },
  "format": "interpreted",
  "reviewed_fields": [
    "source_route"
  ]
}
```

### record-256d5dac4317

2026-06-12T10:00:00Z | review | Daria

Context: task_family=document_retrieval, workflow=workflow-ba5baa940ec0, version=edition-144a2a828934, collection=archive, document_class=assay_report

- decision: accept
- reviewed_fields: ['source_route']
- authority_ref: record-0b87d3565f74
- comment: Approved.

```json
{
  "accepted_fields": {
    "checksum_check": "required",
    "release_id": "REL-32604",
    "source_route": "index-940ec0"
  },
  "authority_ref": "record-0b87d3565f74",
  "change_summary": {
    "after": "index-940ec0",
    "before": "index-ba5baa",
    "field": "source_route"
  },
  "comment": "Approved.",
  "decision": "accept",
  "document_id": "DOC-32604",
  "event": "review",
  "facts": {
    "alternative_route": "index-ba5baa",
    "checksum": "sha256:83af0b563d4d5c2de02d60c31d79fa79",
    "configured_route": "index-940ec0",
    "date": "2026-06-12",
    "document_id": "DOC-32604",
    "release_id": "REL-32604"
  },
  "format": "interpreted",
  "reviewed_fields": [
    "source_route"
  ]
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
| record-1a2bde59abdf | edition-6760601aaacc | task_family=document_retrieval, workflow=workflow-ba5baa940ec0, version=edition-6760601aaacc, collection=active, document_class=assay_report | 0 |
| record-38d7449f0f05 | edition-144a2a828934 | task_family=document_retrieval, workflow=workflow-ba5baa940ec0, version=edition-144a2a828934, collection=active, document_class=assay_report | 1 |
| record-1a0edc5881b9 | edition-144a2a828934 | task_family=document_retrieval, workflow=workflow-ba5baa940ec0, version=edition-144a2a828934, collection=active, document_class=protocol | 0 |
| record-256d5dac4317 | edition-144a2a828934 | task_family=document_retrieval, workflow=workflow-ba5baa940ec0, version=edition-144a2a828934, collection=archive, document_class=assay_report | 0 |

### Competing requirement explanations

Zero is the configured baseline; one is the alternative. Each row is a distinct
compatible function for this version. No preference for simplicity removes a row.
The private sampling plan and world policy do not filter these explanations.

Version edition-144a2a828934: 1 compatible functions.

| Function | collection=active, document_class=protocol | collection=active, document_class=assay_report | collection=archive, document_class=protocol | collection=archive, document_class=assay_report | Complexity |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | 1 | 0 | 0 | 2 |

Version edition-6760601aaacc: 7 compatible functions.

| Function | collection=active, document_class=protocol | collection=active, document_class=assay_report | collection=archive, document_class=protocol | collection=archive, document_class=assay_report | Complexity |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 0 | 0 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 | 1 | 2 |
| 3 | 0 | 0 | 1 | 0 | 2 |
| 4 | 0 | 0 | 1 | 1 | 1 |
| 5 | 1 | 0 | 0 | 0 | 2 |
| 6 | 1 | 0 | 1 | 0 | 1 |
| 7 | 1 | 0 | 1 | 1 | 2 |

### Diagnostic and control derivations

| Task | Context observed | Witnesses | Action | Retention basis |
| --- | --- | --- | --- | --- |
| diagnostic | False | none | keep | resolved |
| control | True | record-1a0edc5881b9 | keep | resolved |

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
      "document_class": "assay_report",
      "task_family": "document_retrieval",
      "version": "edition-144a2a828934",
      "workflow": "workflow-ba5baa940ec0"
    },
    {
      "collection": "active",
      "document_class": "protocol",
      "task_family": "document_retrieval",
      "version": "edition-144a2a828934",
      "workflow": "workflow-ba5baa940ec0"
    },
    {
      "collection": "archive",
      "document_class": "assay_report",
      "task_family": "document_retrieval",
      "version": "edition-144a2a828934",
      "workflow": "workflow-ba5baa940ec0"
    }
  ],
  "diagnostic_observed": false,
  "material_revision": "v04-amendment-03",
  "record_count": 6,
  "registered_versions": [
    "edition-6760601aaacc",
    "edition-144a2a828934"
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
| old_approval | 1 | 0 | 1 | 0 | 0 | 0 | 0 | record-1a2bde59abdf |

### Every promoted public record

| Record | Type | Origin | Public option | Remaining policies | Outcome | Qualifies | Diagnostic action | Control action |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| record-1a2bde59abdf | old_approval | record-1a2bde59abdf | 0 | 0 | contradiction | True | None | None |

### Exact promotions, contexts and public value provenance

The [complete JSON sidecar](S4-retrieval.json) preserves every intervention under `counterfactual.records`,
including selected field presence/value, effective current context, public origin,
precise promotion and remaining-policy count. No intervention alters the real history.

## Future tasks for this development example

### diagnostic

Public task

```json
{
  "task_id": "task-4bd6990ac302",
  "context": {
    "task_family": "document_retrieval",
    "workflow": "workflow-ba5baa940ec0",
    "version": "edition-144a2a828934",
    "collection": "archive",
    "document_class": "protocol"
  },
  "facts": {
    "document_id": "DOC-95422",
    "date": "2026-06-15",
    "configured_route": "index-940ec0",
    "alternative_route": "index-ba5baa",
    "release_id": "REL-95422",
    "checksum": "sha256:808c8703eb93e083f711fa12eb388722"
  },
  "baseline_fields": [
    {
      "name": "source_route",
      "value": "index-940ec0"
    },
    {
      "name": "release_id",
      "value": "REL-95422"
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
  "task_id": "task-4bd6990ac302",
  "history_id": "history-2cd307383a79",
  "probe": "diagnostic",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "source_route",
      "value": "index-940ec0"
    },
    {
      "name": "release_id",
      "value": "REL-95422"
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
  "task_id": "task-fb3d201488f4",
  "context": {
    "task_family": "document_retrieval",
    "workflow": "workflow-ba5baa940ec0",
    "version": "edition-144a2a828934",
    "collection": "active",
    "document_class": "protocol"
  },
  "facts": {
    "document_id": "DOC-53719",
    "date": "2026-06-15",
    "configured_route": "index-940ec0",
    "alternative_route": "index-ba5baa",
    "release_id": "REL-53719",
    "checksum": "sha256:f4d6681652fe896bef9a0dc531b6d1b6"
  },
  "baseline_fields": [
    {
      "name": "source_route",
      "value": "index-940ec0"
    },
    {
      "name": "release_id",
      "value": "REL-53719"
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
  "task_id": "task-fb3d201488f4",
  "history_id": "history-2cd307383a79",
  "probe": "control",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "source_route",
      "value": "index-940ec0"
    },
    {
      "name": "release_id",
      "value": "REL-53719"
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
