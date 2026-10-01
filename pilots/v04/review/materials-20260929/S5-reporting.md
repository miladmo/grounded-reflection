# S5 / reporting

Synthetic development example. Not a live evaluation case.

Intended diagnostic regime: **change**.
Public records: 60. Admissible policies: 32.

## Public configuration

{"task_family":"report_artifact","workflow":"workflow-c9e87bd24be2","as_of":"2026-06-15T12:00:00Z","dimensions":{"artifact":["chart","numeric_table"],"audience":["internal","external"]},"field_option":{"field":"title","operation":"set_fact","value":"base_title","separator":""},"baseline_template":{"title":"{base_title} | {snapshot}","source_footnote":"{source_footnote}"},"fact_descriptions":{"base_title":"Current title without a snapshot suffix.","snapshot":"Current snapshot label.","source_footnote":"Current source note."}}

This is a bounded synthetic workflow model. initial_configuration declares the two available field configurations and two context dimensions. Within a registered version, the selected field configuration is fixed separately for each of the four complete context combinations. This is a supplied modelling restriction, not an inferred claim that other contextual variables never matter in real work. All assignments over those four combinations are possible before evidence. The two options do not imply that either is required. Facts provide current values, not requirement assignments. Other fields retain their configured baseline. Outside the declared task_family and workflow, or without a complete declared context, no update is authorised by this model. A register_version event records the authority roster and the half-open validity interval for that version. Registry records are trusted workflow metadata. An explicit acceptance by an authorised reviewer, within that interval, establishes the approved configuration of reviewed_fields for that exact context and version. Acceptance of an artifact does not approve an unlisted field. Silence is not acceptance. This explicit review convention is part of the synthetic model. A forward references another record; its destination context is not a new review. Comments, execution logs and registry events have their ordinary stated meanings. Their occurrence alone is not a review acceptance. Distinct version labels have separate assignments unless evidence links them. Do not assume an old configuration carries into a new version. The configured baseline is retained when available evidence does not establish an update. Dates and version labels in new work identify the applicable registration.

## Public work records

### record-8a692f4ab333

2026-01-01T00:00:00Z | template | workflow-registry

Context: 

```json
{"authorised_reviewers":["Elena","Anika"],"event":"register_version","supersedes":null,"task_family":"report_artifact","valid_from":"2026-01-01T00:00:00Z","valid_until":"2026-06-01T00:00:00Z","version":"edition-33e1ee13c64d","workflow":"workflow-c9e87bd24be2"}
```

### record-961b42cbae62

2026-05-10T10:00:00Z | review | Elena

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-33e1ee13c64d, artifact=chart, audience=external

```json
{"accepted_artifact":"replacement","artifacts":{"draft":{"fields":{"source_footnote":"Source: approved extract EX-42841.","title":"Quarterly allocation 42841"},"revision":"draft"},"replacement":{"fields":{"source_footnote":"Source: approved extract EX-42841.","title":"Quarterly allocation 42841 | SNAP-42841"},"revision":"reviewed"}},"authority_ref":"record-8a692f4ab333","comment":"This replacement is approved for the recorded work item.","decision":"accept","document_id":"DOC-42841","event":"review","facts":{"base_title":"Quarterly allocation 42841","date":"2026-05-10","document_id":"DOC-42841","snapshot":"SNAP-42841","source_footnote":"Source: approved extract EX-42841."},"format":"raw","reviewed_fields":["title"]}
```

### record-e93735564019

2026-06-01T00:00:00Z | template | workflow-registry

Context: 

```json
{"authorised_reviewers":["Theo","Robin"],"event":"register_version","supersedes":"record-8a692f4ab333","task_family":"report_artifact","valid_from":"2026-06-01T00:00:00Z","valid_until":"2027-01-01T00:00:00Z","version":"edition-e5198d7fe783","workflow":"workflow-c9e87bd24be2"}
```

### record-3eb5d8417d35

2026-06-10T10:00:00Z | review | Theo

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"accepted_artifact":"replacement","artifacts":{"draft":{"fields":{"source_footnote":"Source: approved extract EX-95967.","title":"Quarterly allocation 95967 | SNAP-95967"},"revision":"draft"},"replacement":{"fields":{"source_footnote":"Source: approved extract EX-95967.","title":"Quarterly allocation 95967"},"revision":"reviewed"}},"authority_ref":"record-e93735564019","comment":"This replacement is approved for the recorded work item.","decision":"accept","document_id":"DOC-95967","event":"review","facts":{"base_title":"Quarterly allocation 95967","date":"2026-06-10","document_id":"DOC-95967","snapshot":"SNAP-95967","source_footnote":"Source: approved extract EX-95967."},"format":"raw","reviewed_fields":["title"]}
```

### record-86f6f780f030

2026-06-11T10:00:00Z | review | Robin

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=internal

```json
{"accepted_artifact":"replacement","artifacts":{"draft":{"fields":{"source_footnote":"Source: approved extract EX-41024.","title":"Quarterly allocation 41024"},"revision":"draft"},"replacement":{"fields":{"source_footnote":"Source: approved extract EX-41024.","title":"Quarterly allocation 41024 | SNAP-41024"},"revision":"reviewed"}},"authority_ref":"record-e93735564019","comment":"This replacement is approved for the recorded work item.","decision":"accept","document_id":"DOC-41024","event":"review","facts":{"base_title":"Quarterly allocation 41024","date":"2026-06-11","document_id":"DOC-41024","snapshot":"SNAP-41024","source_footnote":"Source: approved extract EX-41024."},"format":"raw","reviewed_fields":["title"]}
```

### record-0248a90cbb29

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=report_artifact, workflow=other-workflow-312d40b2e6ac, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"accepted_fields":{"source_footnote":"Source: approved extract EX-36331.","title":"Quarterly allocation 36331"},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"base_title":"Quarterly allocation 36331","date":"2026-06-15","document_id":"DOC-36331","snapshot":"SNAP-36331","source_footnote":"Source: approved extract EX-36331."},"format":"interpreted","reviewed_fields":["title"]}
```

### record-05f2d1e1d644

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=report_artifact, workflow=other-workflow-f72549c6f972, version=edition-e5198d7fe783, artifact=numeric_table, audience=internal

```json
{"accepted_fields":{"source_footnote":"Source: approved extract EX-63997.","title":"Quarterly allocation 63997"},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"base_title":"Quarterly allocation 63997","date":"2026-06-15","document_id":"DOC-63997","snapshot":"SNAP-63997","source_footnote":"Source: approved extract EX-63997."},"format":"interpreted","reviewed_fields":["title"]}
```

### record-0f53c848bcea

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=internal

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-c27a5fdd8c34"}
```

### record-189e3739db86

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=internal

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-43ee6bdba2ae"}
```

### record-1aca743a05a6

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=report_artifact, workflow=other-workflow-564a6d701946, version=edition-e5198d7fe783, artifact=numeric_table, audience=internal

```json
{"accepted_fields":{"source_footnote":"Source: approved extract EX-19419.","title":"Quarterly allocation 19419"},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"base_title":"Quarterly allocation 19419","date":"2026-06-15","document_id":"DOC-19419","snapshot":"SNAP-19419","source_footnote":"Source: approved extract EX-19419."},"format":"interpreted","reviewed_fields":["title"]}
```

### record-200948748af4

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=internal

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-a57805d16ab0"}
```

### record-2cb34bca4608

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=internal

```json
{"document_id":"draft-3048921acd5f","event":"comment","message":"My draft view differs from the saved export. I will check my local settings."}
```

### record-2e3faf3119c2

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=report_artifact, workflow=other-workflow-b26ccc185e70, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"accepted_fields":{"source_footnote":"Source: approved extract EX-81154.","title":"Quarterly allocation 81154"},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"base_title":"Quarterly allocation 81154","date":"2026-06-15","document_id":"DOC-81154","snapshot":"SNAP-81154","source_footnote":"Source: approved extract EX-81154."},"format":"interpreted","reviewed_fields":["title"]}
```

### record-368939f80480

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=external

```json
{"document_id":"draft-0839cf78dafe","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-3800b4cdc5a5

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=external

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-157b096477e0"}
```

### record-3b400470383f

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"document_id":"draft-bbee0a231a33","event":"comment","message":"Personally I would prefer a shorter version; I have not reviewed this document."}
```

### record-3bbfbb5fee6d

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=report_artifact, workflow=other-workflow-f9669d77a5b0, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"accepted_fields":{"source_footnote":"Source: approved extract EX-96791.","title":"Quarterly allocation 96791"},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"base_title":"Quarterly allocation 96791","date":"2026-06-15","document_id":"DOC-96791","snapshot":"SNAP-96791","source_footnote":"Source: approved extract EX-96791."},"format":"interpreted","reviewed_fields":["title"]}
```

### record-4b1e00945a26

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=report_artifact, workflow=other-workflow-d4a32e6009f9, version=edition-e5198d7fe783, artifact=numeric_table, audience=internal

```json
{"accepted_fields":{"source_footnote":"Source: approved extract EX-12906.","title":"Quarterly allocation 12906"},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"base_title":"Quarterly allocation 12906","date":"2026-06-15","document_id":"DOC-12906","snapshot":"SNAP-12906","source_footnote":"Source: approved extract EX-12906."},"format":"interpreted","reviewed_fields":["title"]}
```

### record-5165f155af21

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=external

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-c6175932132d"}
```

### record-52690ec0edaf

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=external

```json
{"document_id":"draft-836e43f355b5","event":"comment","message":"Personally I would prefer a shorter version; I have not reviewed this document."}
```

### record-5385fd1b716d

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=internal

```json
{"document_id":"draft-131b76624cb4","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-55ecda34bdfe

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-a7bb21a0290d"}
```

### record-57b09983204c

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-5e4b280f1ee6"}
```

### record-615584cc038c

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"document_id":"draft-80cb9258c695","event":"comment","message":"My draft view differs from the saved export. I will check my local settings."}
```

### record-66c348ab57c2

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=internal

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-f5b83afad203"}
```

### record-6e3324c67d4e

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=internal

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-49ebcfcce5f5"}
```

### record-745f7c7d253f

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"document_id":"draft-c1523ce1158b","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-85cd45b98970

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=report_artifact, workflow=other-workflow-96fabc7b5be2, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"accepted_fields":{"source_footnote":"Source: approved extract EX-31619.","title":"Quarterly allocation 31619"},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"base_title":"Quarterly allocation 31619","date":"2026-06-15","document_id":"DOC-31619","snapshot":"SNAP-31619","source_footnote":"Source: approved extract EX-31619."},"format":"interpreted","reviewed_fields":["title"]}
```

### record-97324d6e97a7

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-44161434040a"}
```

### record-9b275214dc0a

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=report_artifact, workflow=other-workflow-d1270f1e956f, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"accepted_fields":{"source_footnote":"Source: approved extract EX-49951.","title":"Quarterly allocation 49951"},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"base_title":"Quarterly allocation 49951","date":"2026-06-15","document_id":"DOC-49951","snapshot":"SNAP-49951","source_footnote":"Source: approved extract EX-49951."},"format":"interpreted","reviewed_fields":["title"]}
```

### record-a1218adbda54

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=report_artifact, workflow=other-workflow-8582494c2f70, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"accepted_fields":{"source_footnote":"Source: approved extract EX-83193.","title":"Quarterly allocation 83193"},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"base_title":"Quarterly allocation 83193","date":"2026-06-15","document_id":"DOC-83193","snapshot":"SNAP-83193","source_footnote":"Source: approved extract EX-83193."},"format":"interpreted","reviewed_fields":["title"]}
```

### record-a8595655ad24

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-1efd16b6bbc4"}
```

### record-acebc1722c98

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-2f5c69868b46"}
```

### record-afd27e2ea4c9

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=external

```json
{"document_id":"draft-17edd64ce9eb","event":"comment","message":"Personally I would prefer a shorter version; I have not reviewed this document."}
```

### record-baccc59451d8

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=internal

```json
{"document_id":"draft-293c034400e5","event":"comment","message":"Personally I would prefer a shorter version; I have not reviewed this document."}
```

### record-bdc7b0cc91e1

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=external

```json
{"document_id":"draft-336f1df3eee4","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-be8ba02bff98

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=internal

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-ba4fa997c27a"}
```

### record-c0fe1f352acc

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"document_id":"draft-ae5ccb24d4ee","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-c14d6555b18d

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-8a744163ff92"}
```

### record-d54d06b54e3e

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=internal

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-a970f67caf1b"}
```

### record-d9e34f180c54

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=internal

```json
{"document_id":"draft-90b2dd588e6b","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-e22fa889e215

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=external

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-d74cc7d49196"}
```

### record-e354c0115d6d

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=internal

```json
{"document_id":"draft-e92cfff691ef","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-f1b3044187f4

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=report_artifact, workflow=other-workflow-5bcf06249b45, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"accepted_fields":{"source_footnote":"Source: approved extract EX-21765.","title":"Quarterly allocation 21765"},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"base_title":"Quarterly allocation 21765","date":"2026-06-15","document_id":"DOC-21765","snapshot":"SNAP-21765","source_footnote":"Source: approved extract EX-21765."},"format":"interpreted","reviewed_fields":["title"]}
```

### record-f2b769e29c0e

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=internal

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-8f2fa1075a90"}
```

### record-f5feb0e135a6

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=internal

```json
{"document_id":"draft-fb46991cf0b2","event":"comment","message":"Personally I would prefer a shorter version; I have not reviewed this document."}
```

### record-f78e9e219d3c

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=internal

```json
{"document_id":"draft-2ef689e6697a","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-ff586942ed18

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=internal

```json
{"document_id":"draft-4585702523ea","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-001f8d9e44c6

2026-06-14T11:00:00Z | revision | forwarding-service

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=internal

```json
{"event":"forward","message":"Forwarded review for reference. Please see the linked original artifact.","origin_ref":"record-961b42cbae62"}
```

### record-2de02e833aea

2026-06-14T11:00:00Z | revision | forwarding-service

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=internal

```json
{"event":"forward","message":"Forwarded review for reference. Please see the linked original artifact.","origin_ref":"record-3eb5d8417d35"}
```

### record-338aff24faa9

2026-06-14T11:00:00Z | revision | forwarding-service

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"event":"forward","message":"Forwarded review for reference. Please see the linked original artifact.","origin_ref":"record-961b42cbae62"}
```

### record-52bb0b2fcea7

2026-06-14T11:00:00Z | revision | forwarding-service

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"event":"forward","message":"Forwarded review for reference. Please see the linked original artifact.","origin_ref":"record-3eb5d8417d35"}
```

### record-7370871487cb

2026-06-14T11:00:00Z | revision | forwarding-service

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=internal

```json
{"event":"forward","message":"Forwarded review for reference. Please see the linked original artifact.","origin_ref":"record-961b42cbae62"}
```

### record-94cbdefc0d92

2026-06-14T11:00:00Z | revision | forwarding-service

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=internal

```json
{"event":"forward","message":"Forwarded review for reference. Please see the linked original artifact.","origin_ref":"record-961b42cbae62"}
```

### record-98ebe24b9c04

2026-06-14T11:00:00Z | revision | forwarding-service

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=external

```json
{"event":"forward","message":"Forwarded review for reference. Please see the linked original artifact.","origin_ref":"record-961b42cbae62"}
```

### record-a586337514f7

2026-06-14T11:00:00Z | revision | forwarding-service

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=internal

```json
{"event":"forward","message":"Forwarded review for reference. Please see the linked original artifact.","origin_ref":"record-961b42cbae62"}
```

### record-bfc269cec104

2026-06-14T11:00:00Z | revision | forwarding-service

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=internal

```json
{"event":"forward","message":"Forwarded review for reference. Please see the linked original artifact.","origin_ref":"record-961b42cbae62"}
```

### record-d2c540aa1a38

2026-06-14T11:00:00Z | revision | forwarding-service

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=internal

```json
{"event":"forward","message":"Forwarded review for reference. Please see the linked original artifact.","origin_ref":"record-961b42cbae62"}
```

### record-d6f70053352e

2026-06-14T11:00:00Z | revision | forwarding-service

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=chart, audience=internal

```json
{"event":"forward","message":"Forwarded review for reference. Please see the linked original artifact.","origin_ref":"record-961b42cbae62"}
```

### record-ee7fd73264aa

2026-06-14T11:00:00Z | revision | forwarding-service

Context: task_family=report_artifact, workflow=workflow-c9e87bd24be2, version=edition-e5198d7fe783, artifact=numeric_table, audience=external

```json
{"event":"forward","message":"Forwarded review for reference. Please see the linked original artifact.","origin_ref":"record-3eb5d8417d35"}
```

## Private evaluator view

The world policy is distinct from what the evidence identifies. The table shows
the complete registered contexts. Baseline and alternative describe field effects,
not whether a professional convention is desirable. Both means unresolved.
All policies, invalid-context probes and exact values remain in the accompanying JSON.

| Version and context | World | Admitted effects | Direct review witnesses |
| --- | --- | --- | --- |
| version=edition-33e1ee13c64d, artifact=chart, audience=internal | baseline | alternative, baseline | none |
| version=edition-33e1ee13c64d, artifact=chart, audience=external | baseline | baseline | record-961b42cbae62 |
| version=edition-33e1ee13c64d, artifact=numeric_table, audience=internal | alternative | alternative, baseline | none |
| version=edition-33e1ee13c64d, artifact=numeric_table, audience=external | alternative | alternative, baseline | none |
| version=edition-e5198d7fe783, artifact=chart, audience=internal | alternative | alternative, baseline | none |
| version=edition-e5198d7fe783, artifact=chart, audience=external | alternative | alternative | record-3eb5d8417d35 |
| version=edition-e5198d7fe783, artifact=numeric_table, audience=internal | baseline | baseline | record-86f6f780f030 |
| version=edition-e5198d7fe783, artifact=numeric_table, audience=external | alternative | alternative, baseline | none |

## Future tasks for this development example

### diagnostic

```json
{
  "task_id": "task-d038658ce573",
  "context": {
    "task_family": "report_artifact",
    "workflow": "workflow-c9e87bd24be2",
    "version": "edition-e5198d7fe783",
    "artifact": "chart",
    "audience": "external"
  },
  "facts": {
    "document_id": "DOC-98529",
    "date": "2026-06-15",
    "base_title": "Quarterly allocation 98529",
    "snapshot": "SNAP-98529",
    "source_footnote": "Source: approved extract EX-98529."
  },
  "baseline_fields": [
    {
      "name": "title",
      "value": "Quarterly allocation 98529 | SNAP-98529"
    },
    {
      "name": "source_footnote",
      "value": "Source: approved extract EX-98529."
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Expected obligations

```json
{
  "task_id": "task-d038658ce573",
  "history_id": "history-8eccf20d6cf1",
  "probe": "diagnostic",
  "expected_decision": "apply",
  "recoverable": true,
  "world_fields": [
    {
      "name": "title",
      "value": "Quarterly allocation 98529"
    },
    {
      "name": "source_footnote",
      "value": "Source: approved extract EX-98529."
    }
  ]
}
```

### control

```json
{
  "task_id": "task-40ebc361a4ae",
  "context": {
    "task_family": "report_artifact",
    "workflow": "workflow-c9e87bd24be2",
    "version": "edition-e5198d7fe783",
    "artifact": "numeric_table",
    "audience": "internal"
  },
  "facts": {
    "document_id": "DOC-91389",
    "date": "2026-06-15",
    "base_title": "Quarterly allocation 91389",
    "snapshot": "SNAP-91389",
    "source_footnote": "Source: approved extract EX-91389."
  },
  "baseline_fields": [
    {
      "name": "title",
      "value": "Quarterly allocation 91389 | SNAP-91389"
    },
    {
      "name": "source_footnote",
      "value": "Source: approved extract EX-91389."
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Expected obligations

```json
{
  "task_id": "task-40ebc361a4ae",
  "history_id": "history-8eccf20d6cf1",
  "probe": "control",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "title",
      "value": "Quarterly allocation 91389 | SNAP-91389"
    },
    {
      "name": "source_footnote",
      "value": "Source: approved extract EX-91389."
    }
  ]
}
```

## Human response

Pending. No approval is inferred from this export.
