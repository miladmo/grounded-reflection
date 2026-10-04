# S4 / retrieval

Synthetic development example. Not a live evaluation case.

Intended diagnostic regime: **resolved_keep**.
Public records: 6. Admissible policies: 32.

## Public configuration

{"task_family":"document_retrieval","workflow":"workflow-0f3589fcd2d1","as_of":"2026-06-15T12:00:00Z","dimensions":{"collection":["active","archive"],"document_class":["protocol","assay_report"]},"field_option":{"field":"source_route","operation":"set_fact","value":"alternative_route","separator":""},"baseline_template":{"source_route":"{configured_route}","release_id":"{release_id}","checksum_check":"required"},"fact_descriptions":{"configured_route":"Endpoint selected by the initial configuration.","alternative_route":"The other available endpoint.","release_id":"Requested release.","checksum_check":"The exact canonical marker required means verify the retrieved checksum."}}

This is a bounded synthetic workflow model. initial_configuration declares the two available field configurations and two context dimensions. Within a registered version, the selected field configuration is fixed separately for each of the four complete context combinations. This is a supplied modelling restriction, not an inferred claim that other contextual variables never matter in real work. All assignments over those four combinations are possible before evidence. The two options do not imply that either is required. Facts provide current values, not requirement assignments. Other fields retain their configured baseline. Outside the declared task_family and workflow, or without a complete declared context, no update is authorised by this model. A register_version event records the authority roster and the half-open validity interval for that version. Registry records are trusted workflow metadata. An explicit acceptance by an authorised reviewer, within that interval, establishes the approved configuration of reviewed_fields for that exact context and version. Acceptance of an artifact does not approve an unlisted field. Silence is not acceptance. This explicit review convention is part of the synthetic model. A forward references another record; its destination context is not a new review. Comments, execution logs and registry events have their ordinary stated meanings. Their occurrence alone is not a review acceptance. Distinct version labels have separate assignments unless evidence links them. Do not assume an old configuration carries into a new version. The configured baseline is retained when available evidence does not establish an update. Dates and version labels in new work identify the applicable registration.

## Public work records

### record-b0b8089e2074

2026-01-01T00:00:00Z | template | workflow-registry

Context: 

```json
{"authorised_reviewers":["Jonas","Robin"],"event":"register_version","supersedes":null,"task_family":"document_retrieval","valid_from":"2026-01-01T00:00:00Z","valid_until":"2026-06-01T00:00:00Z","version":"edition-b1f9d24ccdc8","workflow":"workflow-0f3589fcd2d1"}
```

### record-07814b6662ed

2026-05-10T10:00:00Z | review | Jonas

Context: task_family=document_retrieval, workflow=workflow-0f3589fcd2d1, version=edition-b1f9d24ccdc8, collection=archive, document_class=protocol

```json
{"accepted_fields":{"checksum_check":"required","release_id":"REL-31803","source_route":"index-0f3589"},"authority_ref":"record-b0b8089e2074","change_summary":{"after":"index-0f3589","before":"index-fcd2d1","field":"source_route"},"comment":"This replacement is approved for the recorded work item.","decision":"accept","document_id":"DOC-31803","event":"review","facts":{"alternative_route":"index-0f3589","checksum":"sha256:87da1605c29fe6f7d69b3e18f8606691","configured_route":"index-fcd2d1","date":"2026-05-10","document_id":"DOC-31803","release_id":"REL-31803"},"format":"interpreted","reviewed_fields":["source_route"]}
```

### record-c4cb4f18ac6b

2026-06-01T00:00:00Z | template | workflow-registry

Context: 

```json
{"authorised_reviewers":["Jonas","Elena"],"event":"register_version","supersedes":"record-b0b8089e2074","task_family":"document_retrieval","valid_from":"2026-06-01T00:00:00Z","valid_until":"2027-01-01T00:00:00Z","version":"edition-58cc8921cd84","workflow":"workflow-0f3589fcd2d1"}
```

### record-b213a40b6943

2026-06-10T10:00:00Z | review | Jonas

Context: task_family=document_retrieval, workflow=workflow-0f3589fcd2d1, version=edition-58cc8921cd84, collection=archive, document_class=assay_report

```json
{"accepted_fields":{"checksum_check":"required","release_id":"REL-75727","source_route":"index-0f3589"},"authority_ref":"record-c4cb4f18ac6b","change_summary":{"after":"index-0f3589","before":"index-fcd2d1","field":"source_route"},"comment":"This replacement is approved for the recorded work item.","decision":"accept","document_id":"DOC-75727","event":"review","facts":{"alternative_route":"index-0f3589","checksum":"sha256:3a0abf9ceea06a960b7899b5455d47b3","configured_route":"index-fcd2d1","date":"2026-06-10","document_id":"DOC-75727","release_id":"REL-75727"},"format":"interpreted","reviewed_fields":["source_route"]}
```

### record-459d6bc560b3

2026-06-11T10:00:00Z | review | Elena

Context: task_family=document_retrieval, workflow=workflow-0f3589fcd2d1, version=edition-58cc8921cd84, collection=archive, document_class=protocol

```json
{"accepted_fields":{"checksum_check":"required","release_id":"REL-67504","source_route":"index-fcd2d1"},"authority_ref":"record-c4cb4f18ac6b","change_summary":{"after":"index-fcd2d1","before":"index-0f3589","field":"source_route"},"comment":"This replacement is approved for the recorded work item.","decision":"accept","document_id":"DOC-67504","event":"review","facts":{"alternative_route":"index-0f3589","checksum":"sha256:fdefc516240b8b2bbb44caa56427b812","configured_route":"index-fcd2d1","date":"2026-06-11","document_id":"DOC-67504","release_id":"REL-67504"},"format":"interpreted","reviewed_fields":["source_route"]}
```

### record-a5a045c14e70

2026-06-12T10:00:00Z | review | Jonas

Context: task_family=document_retrieval, workflow=workflow-0f3589fcd2d1, version=edition-58cc8921cd84, collection=archive, document_class=assay_report

```json
{"accepted_fields":{"checksum_check":"required","release_id":"REL-88343","source_route":"index-0f3589"},"authority_ref":"record-c4cb4f18ac6b","change_summary":{"after":"index-0f3589","before":"index-fcd2d1","field":"source_route"},"comment":"This replacement is approved for the recorded work item.","decision":"accept","document_id":"DOC-88343","event":"review","facts":{"alternative_route":"index-0f3589","checksum":"sha256:d9ff42861e89e1ec40877107f88b9ddf","configured_route":"index-fcd2d1","date":"2026-06-12","document_id":"DOC-88343","release_id":"REL-88343"},"format":"interpreted","reviewed_fields":["source_route"]}
```

## Private evaluator view

The world policy is distinct from what the evidence identifies. The table shows
the complete registered contexts. Baseline and alternative describe field effects,
not whether a professional convention is desirable. Both means unresolved.
All policies, invalid-context probes and exact values remain in the accompanying JSON.

| Version and context | World | Admitted effects | Direct review witnesses |
| --- | --- | --- | --- |
| version=edition-b1f9d24ccdc8, collection=active, document_class=protocol | baseline | alternative, baseline | none |
| version=edition-b1f9d24ccdc8, collection=active, document_class=assay_report | baseline | alternative, baseline | none |
| version=edition-b1f9d24ccdc8, collection=archive, document_class=protocol | alternative | alternative | record-07814b6662ed |
| version=edition-b1f9d24ccdc8, collection=archive, document_class=assay_report | alternative | alternative, baseline | none |
| version=edition-58cc8921cd84, collection=active, document_class=protocol | baseline | alternative, baseline | none |
| version=edition-58cc8921cd84, collection=active, document_class=assay_report | alternative | alternative, baseline | none |
| version=edition-58cc8921cd84, collection=archive, document_class=protocol | baseline | baseline | record-459d6bc560b3 |
| version=edition-58cc8921cd84, collection=archive, document_class=assay_report | alternative | alternative | record-b213a40b6943, record-a5a045c14e70 |

## Future tasks for this development example

### diagnostic

```json
{
  "task_id": "task-121116fd4c17",
  "context": {
    "task_family": "document_retrieval",
    "workflow": "workflow-0f3589fcd2d1",
    "version": "edition-58cc8921cd84",
    "collection": "archive",
    "document_class": "protocol"
  },
  "facts": {
    "document_id": "DOC-68882",
    "date": "2026-06-15",
    "configured_route": "index-fcd2d1",
    "alternative_route": "index-0f3589",
    "release_id": "REL-68882",
    "checksum": "sha256:5032ca9371b4371f2d7fca7f6ca766cd"
  },
  "baseline_fields": [
    {
      "name": "source_route",
      "value": "index-fcd2d1"
    },
    {
      "name": "release_id",
      "value": "REL-68882"
    },
    {
      "name": "checksum_check",
      "value": "required"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Expected obligations

```json
{
  "task_id": "task-121116fd4c17",
  "history_id": "history-a3c58177d846",
  "probe": "diagnostic",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "source_route",
      "value": "index-fcd2d1"
    },
    {
      "name": "release_id",
      "value": "REL-68882"
    },
    {
      "name": "checksum_check",
      "value": "required"
    }
  ]
}
```

### control

```json
{
  "task_id": "task-f8e4917b664f",
  "context": {
    "task_family": "document_retrieval",
    "workflow": "workflow-0f3589fcd2d1",
    "version": "edition-58cc8921cd84",
    "collection": "active",
    "document_class": "protocol"
  },
  "facts": {
    "document_id": "DOC-26088",
    "date": "2026-06-15",
    "configured_route": "index-fcd2d1",
    "alternative_route": "index-0f3589",
    "release_id": "REL-26088",
    "checksum": "sha256:6bcc75f8a96d946e55e086130d5198eb"
  },
  "baseline_fields": [
    {
      "name": "source_route",
      "value": "index-fcd2d1"
    },
    {
      "name": "release_id",
      "value": "REL-26088"
    },
    {
      "name": "checksum_check",
      "value": "required"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Expected obligations

```json
{
  "task_id": "task-f8e4917b664f",
  "history_id": "history-a3c58177d846",
  "probe": "control",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "source_route",
      "value": "index-fcd2d1"
    },
    {
      "name": "release_id",
      "value": "REL-26088"
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
