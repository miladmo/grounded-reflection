# S2 / sales

Synthetic development example. Not a live evaluation case.

Intended diagnostic regime: **resolved_keep**.
Public records: 60. Admissible policies: 4.

## Public configuration

{"task_family":"sales_offer","workflow":"workflow-77da9260c28a","as_of":"2026-06-15T12:00:00Z","dimensions":{"reviewer":["Emil","Nora"],"customer_segment":["standard","strategic"]},"field_option":{"field":"annual_total","operation":"omit","value":"","separator":""},"baseline_template":{"offer_text":"{offer_text}","contract_reference":"{contract_reference}","annual_total":"{annual_total}"},"fact_descriptions":{"offer_text":"Current offer text.","contract_reference":"Current offer reference.","monthly_unit_price":"EUR per seat and month.","seats":"Number of seats.","annual_total":"EUR, monthly_unit_price times seats times twelve."}}

This is a bounded synthetic workflow model. initial_configuration declares the two available field configurations and two context dimensions. Within a registered version, the selected field configuration is fixed separately for each of the four complete context combinations. This is a supplied modelling restriction, not an inferred claim that other contextual variables never matter in real work. All assignments over those four combinations are possible before evidence. The two options do not imply that either is required. Facts provide current values, not requirement assignments. Other fields retain their configured baseline. Outside the declared task_family and workflow, or without a complete declared context, no update is authorised by this model. A register_version event records the authority roster and the half-open validity interval for that version. Registry records are trusted workflow metadata. An explicit acceptance by an authorised reviewer, within that interval, establishes the approved configuration of reviewed_fields for that exact context and version. Acceptance of an artifact does not approve an unlisted field. Silence is not acceptance. This explicit review convention is part of the synthetic model. A forward references another record; its destination context is not a new review. Comments, execution logs and registry events have their ordinary stated meanings. Their occurrence alone is not a review acceptance. Distinct version labels have separate assignments unless evidence links them. Do not assume an old configuration carries into a new version. The configured baseline is retained when available evidence does not establish an update. Dates and version labels in new work identify the applicable registration.

## Public work records

### record-1dbbf91bafe4

2026-01-01T00:00:00Z | template | workflow-registry

Context: 

```json
{"authorised_reviewers":["Theo","Anika"],"event":"register_version","supersedes":null,"task_family":"sales_offer","valid_from":"2026-01-01T00:00:00Z","valid_until":"2027-01-01T00:00:00Z","version":"edition-b6a204a69019","workflow":"workflow-77da9260c28a"}
```

### record-3673101a7b64

2026-06-10T10:00:00Z | review | Theo

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=strategic

```json
{"accepted_fields":{"contract_reference":"OFF-65442","offer_text":"20 seats at EUR 25 per seat per month, billed annually."},"authority_ref":"record-1dbbf91bafe4","change_summary":{"after":null,"before":"6000","field":"annual_total"},"comment":"This replacement is approved for the recorded work item.","decision":"accept","document_id":"DOC-65442","event":"review","facts":{"annual_total":"6000","contract_reference":"OFF-65442","date":"2026-06-10","document_id":"DOC-65442","monthly_unit_price":"25","offer_text":"20 seats at EUR 25 per seat per month, billed annually.","seats":"20"},"format":"interpreted","reviewed_fields":["annual_total"]}
```

### record-3e16bb4da3c0

2026-06-11T10:00:00Z | review | Anika

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=standard

```json
{"accepted_fields":{"annual_total":"15600","contract_reference":"OFF-43374","offer_text":"20 seats at EUR 65 per seat per month, billed annually."},"authority_ref":"record-1dbbf91bafe4","change_summary":{"after":"15600","before":null,"field":"annual_total"},"comment":"This replacement is approved for the recorded work item.","decision":"accept","document_id":"DOC-43374","event":"review","facts":{"annual_total":"15600","contract_reference":"OFF-43374","date":"2026-06-11","document_id":"DOC-43374","monthly_unit_price":"65","offer_text":"20 seats at EUR 65 per seat per month, billed annually.","seats":"20"},"format":"interpreted","reviewed_fields":["annual_total"]}
```

### record-1e45235d9bc8

2026-06-12T10:00:00Z | review | Theo

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=strategic

```json
{"accepted_fields":{"contract_reference":"OFF-98757","offer_text":"15 seats at EUR 40 per seat per month, billed annually."},"authority_ref":"record-1dbbf91bafe4","change_summary":{"after":null,"before":"7200","field":"annual_total"},"comment":"This replacement is approved for the recorded work item.","decision":"accept","document_id":"DOC-98757","event":"review","facts":{"annual_total":"7200","contract_reference":"OFF-98757","date":"2026-06-12","document_id":"DOC-98757","monthly_unit_price":"40","offer_text":"15 seats at EUR 40 per seat per month, billed annually.","seats":"15"},"format":"interpreted","reviewed_fields":["annual_total"]}
```

### record-01a67b4bd5d6

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Nora, customer_segment=standard

```json
{"document_id":"draft-1dba7c512268","event":"comment","message":"My draft view differs from the saved export. I will check my local settings."}
```

### record-030ae00d58d1

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=standard

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-2ba6dfa8d1f8"}
```

### record-042725078ad3

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Nora, customer_segment=standard

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-8b74642a4aea"}
```

### record-08a7d228e7ac

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=sales_offer, workflow=other-workflow-34f814dad9b1, version=edition-b6a204a69019, reviewer=Nora, customer_segment=standard

```json
{"accepted_fields":{"contract_reference":"OFF-98893","offer_text":"5 seats at EUR 50 per seat per month, billed annually."},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"annual_total":"3000","contract_reference":"OFF-98893","date":"2026-06-15","document_id":"DOC-98893","monthly_unit_price":"50","offer_text":"5 seats at EUR 50 per seat per month, billed annually.","seats":"5"},"format":"interpreted","reviewed_fields":["annual_total"]}
```

### record-101b06344ab4

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Nora, customer_segment=strategic

```json
{"document_id":"draft-52cf958d1c4e","event":"comment","message":"My draft view differs from the saved export. I will check my local settings."}
```

### record-13ce1d783067

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Nora, customer_segment=standard

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-f61af88341cb"}
```

### record-1802476d43ad

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=sales_offer, workflow=other-workflow-4919af0cbc2c, version=edition-b6a204a69019, reviewer=Emil, customer_segment=standard

```json
{"accepted_fields":{"contract_reference":"OFF-52162","offer_text":"20 seats at EUR 25 per seat per month, billed annually."},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"annual_total":"6000","contract_reference":"OFF-52162","date":"2026-06-15","document_id":"DOC-52162","monthly_unit_price":"25","offer_text":"20 seats at EUR 25 per seat per month, billed annually.","seats":"20"},"format":"interpreted","reviewed_fields":["annual_total"]}
```

### record-1897c5c943a7

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=strategic

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-3e7cd0f8ce9b"}
```

### record-192b65229c79

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=standard

```json
{"document_id":"draft-f4f44253c966","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-1c664f6e68c9

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=sales_offer, workflow=other-workflow-2acfbba6eb4a, version=edition-b6a204a69019, reviewer=Nora, customer_segment=standard

```json
{"accepted_fields":{"contract_reference":"OFF-23031","offer_text":"10 seats at EUR 40 per seat per month, billed annually."},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"annual_total":"4800","contract_reference":"OFF-23031","date":"2026-06-15","document_id":"DOC-23031","monthly_unit_price":"40","offer_text":"10 seats at EUR 40 per seat per month, billed annually.","seats":"10"},"format":"interpreted","reviewed_fields":["annual_total"]}
```

### record-1d3de78aa75a

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Nora, customer_segment=standard

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-152948b6dc07"}
```

### record-1e41634b0345

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=strategic

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-4607b5000506"}
```

### record-1fcb598788ef

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Nora, customer_segment=standard

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-52ff741d4825"}
```

### record-203cfa2d03ad

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=strategic

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-8cd70eca57ec"}
```

### record-2ad9eb59ad03

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=strategic

```json
{"document_id":"draft-03fc78df668a","event":"comment","message":"Personally I would prefer a shorter version; I have not reviewed this document."}
```

### record-316409d4d29d

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=sales_offer, workflow=other-workflow-9ab0919e22d2, version=edition-b6a204a69019, reviewer=Emil, customer_segment=standard

```json
{"accepted_fields":{"contract_reference":"OFF-97304","offer_text":"5 seats at EUR 65 per seat per month, billed annually."},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"annual_total":"3900","contract_reference":"OFF-97304","date":"2026-06-15","document_id":"DOC-97304","monthly_unit_price":"65","offer_text":"5 seats at EUR 65 per seat per month, billed annually.","seats":"5"},"format":"interpreted","reviewed_fields":["annual_total"]}
```

### record-320ec6f0da9a

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=strategic

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-fa8eb0066af1"}
```

### record-3aec3bccfdea

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=strategic

```json
{"document_id":"draft-e4b2641593c6","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-3d800b8e5a88

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Nora, customer_segment=strategic

```json
{"document_id":"draft-d6d62920c01f","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-3e6faea51f20

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Nora, customer_segment=standard

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-7773be3c23cd"}
```

### record-40dc6f7cdce7

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=strategic

```json
{"document_id":"draft-b626a9fc69dc","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-44a527c35b7c

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=sales_offer, workflow=other-workflow-5eeb23615587, version=edition-b6a204a69019, reviewer=Emil, customer_segment=standard

```json
{"accepted_fields":{"contract_reference":"OFF-32720","offer_text":"5 seats at EUR 50 per seat per month, billed annually."},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"annual_total":"3000","contract_reference":"OFF-32720","date":"2026-06-15","document_id":"DOC-32720","monthly_unit_price":"50","offer_text":"5 seats at EUR 50 per seat per month, billed annually.","seats":"5"},"format":"interpreted","reviewed_fields":["annual_total"]}
```

### record-4abdd18a8f52

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=standard

```json
{"document_id":"draft-1ad8fe289626","event":"comment","message":"Personally I would prefer a shorter version; I have not reviewed this document."}
```

### record-4de87c9d8c0a

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Nora, customer_segment=standard

```json
{"document_id":"draft-f3517b3eabed","event":"comment","message":"Personally I would prefer a shorter version; I have not reviewed this document."}
```

### record-52c56cafa5b8

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=strategic

```json
{"document_id":"draft-dea766a68318","event":"comment","message":"My draft view differs from the saved export. I will check my local settings."}
```

### record-56ec89b2a795

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=sales_offer, workflow=other-workflow-7cf9872dd934, version=edition-b6a204a69019, reviewer=Nora, customer_segment=strategic

```json
{"accepted_fields":{"contract_reference":"OFF-27827","offer_text":"15 seats at EUR 25 per seat per month, billed annually."},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"annual_total":"4500","contract_reference":"OFF-27827","date":"2026-06-15","document_id":"DOC-27827","monthly_unit_price":"25","offer_text":"15 seats at EUR 25 per seat per month, billed annually.","seats":"15"},"format":"interpreted","reviewed_fields":["annual_total"]}
```

### record-58be12d953c5

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=sales_offer, workflow=other-workflow-842ab348b5bf, version=edition-b6a204a69019, reviewer=Nora, customer_segment=strategic

```json
{"accepted_fields":{"contract_reference":"OFF-42024","offer_text":"20 seats at EUR 40 per seat per month, billed annually."},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"annual_total":"9600","contract_reference":"OFF-42024","date":"2026-06-15","document_id":"DOC-42024","monthly_unit_price":"40","offer_text":"20 seats at EUR 40 per seat per month, billed annually.","seats":"20"},"format":"interpreted","reviewed_fields":["annual_total"]}
```

### record-5b7b3352f701

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=strategic

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-60637ae092ba"}
```

### record-5d083b08166f

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Nora, customer_segment=standard

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-01578aa7d38a"}
```

### record-60d53821d0e7

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=standard

```json
{"document_id":"draft-b9052ab9b005","event":"comment","message":"Personally I would prefer a shorter version; I have not reviewed this document."}
```

### record-614f16370198

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=sales_offer, workflow=other-workflow-f231c2a679ca, version=edition-b6a204a69019, reviewer=Nora, customer_segment=standard

```json
{"accepted_fields":{"contract_reference":"OFF-56455","offer_text":"15 seats at EUR 50 per seat per month, billed annually."},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"annual_total":"9000","contract_reference":"OFF-56455","date":"2026-06-15","document_id":"DOC-56455","monthly_unit_price":"50","offer_text":"15 seats at EUR 50 per seat per month, billed annually.","seats":"15"},"format":"interpreted","reviewed_fields":["annual_total"]}
```

### record-6e0933a7815b

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Nora, customer_segment=strategic

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-e1547fcdd1c8"}
```

### record-723e07430d76

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=standard

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-5b1bd4892b1e"}
```

### record-96941109521d

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=strategic

```json
{"document_id":"draft-9f3ce4d98ce1","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-9a40c4c2e729

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=sales_offer, workflow=other-workflow-a302c80195c0, version=edition-b6a204a69019, reviewer=Emil, customer_segment=standard

```json
{"accepted_fields":{"contract_reference":"OFF-17904","offer_text":"10 seats at EUR 50 per seat per month, billed annually."},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"annual_total":"6000","contract_reference":"OFF-17904","date":"2026-06-15","document_id":"DOC-17904","monthly_unit_price":"50","offer_text":"10 seats at EUR 50 per seat per month, billed annually.","seats":"10"},"format":"interpreted","reviewed_fields":["annual_total"]}
```

### record-9b968d9e8383

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=strategic

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-44254b6d9d3d"}
```

### record-9edf62313def

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=standard

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-9ce30b8f1f8c"}
```

### record-a69f7e8e5609

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Nora, customer_segment=strategic

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-c75ca701d74e"}
```

### record-b7ddc4163501

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Nora, customer_segment=standard

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-8ac4c930767a"}
```

### record-b8aa308fc887

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=sales_offer, workflow=other-workflow-b19c8d387f1b, version=edition-b6a204a69019, reviewer=Nora, customer_segment=standard

```json
{"accepted_fields":{"contract_reference":"OFF-34316","offer_text":"15 seats at EUR 50 per seat per month, billed annually."},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"annual_total":"9000","contract_reference":"OFF-34316","date":"2026-06-15","document_id":"DOC-34316","monthly_unit_price":"50","offer_text":"15 seats at EUR 50 per seat per month, billed annually.","seats":"15"},"format":"interpreted","reviewed_fields":["annual_total"]}
```

### record-c462bb70f073

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Nora, customer_segment=strategic

```json
{"document_id":"draft-323abcdb9d14","event":"comment","message":"Personally I would prefer a shorter version; I have not reviewed this document."}
```

### record-c6ea135f557c

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Nora, customer_segment=strategic

```json
{"document_id":"draft-7f9e02ced378","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-c8b0d0a748bc

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=sales_offer, workflow=other-workflow-98e9a081d3ab, version=edition-b6a204a69019, reviewer=Emil, customer_segment=standard

```json
{"accepted_fields":{"contract_reference":"OFF-15128","offer_text":"15 seats at EUR 65 per seat per month, billed annually."},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"annual_total":"11700","contract_reference":"OFF-15128","date":"2026-06-15","document_id":"DOC-15128","monthly_unit_price":"65","offer_text":"15 seats at EUR 65 per seat per month, billed annually.","seats":"15"},"format":"interpreted","reviewed_fields":["annual_total"]}
```

### record-cbdce4949cac

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=standard

```json
{"document_id":"draft-0057c942e2ff","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-ce2c3e35719a

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=sales_offer, workflow=other-workflow-238f84eeae9b, version=edition-b6a204a69019, reviewer=Emil, customer_segment=strategic

```json
{"accepted_fields":{"contract_reference":"OFF-75971","offer_text":"10 seats at EUR 50 per seat per month, billed annually."},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"annual_total":"6000","contract_reference":"OFF-75971","date":"2026-06-15","document_id":"DOC-75971","monthly_unit_price":"50","offer_text":"10 seats at EUR 50 per seat per month, billed annually.","seats":"10"},"format":"interpreted","reviewed_fields":["annual_total"]}
```

### record-ce422083f9f1

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=standard

```json
{"document_id":"draft-31b2f63cb9c0","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-ce4caed5b2d2

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Nora, customer_segment=strategic

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-94096bd4c442"}
```

### record-d6b7826abcb1

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Nora, customer_segment=strategic

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-780ac63b5510"}
```

### record-ec13e79511f5

2026-06-14T09:00:00Z | tool | runtime

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Nora, customer_segment=strategic

```json
{"attempts":[{"attempt":1,"http_status":503},{"attempt":2,"http_status":200}],"event":"execution","log":"The same request completed on retry; no review was recorded.","request_id":"request-55b5de4ee94f"}
```

### record-ec52e8114537

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=standard

```json
{"document_id":"draft-dc61272f3ad7","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-f1cb8a4f34de

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=sales_offer, workflow=other-workflow-c163f863d4e0, version=edition-b6a204a69019, reviewer=Nora, customer_segment=strategic

```json
{"accepted_fields":{"contract_reference":"OFF-57613","offer_text":"15 seats at EUR 25 per seat per month, billed annually."},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"annual_total":"4500","contract_reference":"OFF-57613","date":"2026-06-15","document_id":"DOC-57613","monthly_unit_price":"25","offer_text":"15 seats at EUR 25 per seat per month, billed annually.","seats":"15"},"format":"interpreted","reviewed_fields":["annual_total"]}
```

### record-f875124cb1d0

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=strategic

```json
{"document_id":"draft-4831d7e4142c","event":"comment","message":"My draft view differs from the saved export. I will check my local settings."}
```

### record-fa5e8d289668

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=strategic

```json
{"document_id":"draft-5eab84979c9b","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-fa60b5c45241

2026-06-14T09:00:00Z | review | external-workflow-reviewer

Context: task_family=sales_offer, workflow=other-workflow-5eb1a2872755, version=edition-b6a204a69019, reviewer=Emil, customer_segment=standard

```json
{"accepted_fields":{"contract_reference":"OFF-69095","offer_text":"10 seats at EUR 65 per seat per month, billed annually."},"authority_ref":"separate-workflow-registry-not-exported","comment":"Approved in this separate workflow.","decision":"accept","event":"review","facts":{"annual_total":"7800","contract_reference":"OFF-69095","date":"2026-06-15","document_id":"DOC-69095","monthly_unit_price":"65","offer_text":"10 seats at EUR 65 per seat per month, billed annually.","seats":"10"},"format":"interpreted","reviewed_fields":["annual_total"]}
```

### record-ff019668f23a

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=standard

```json
{"document_id":"draft-ae8e79f1c1e4","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

### record-ffec8462391d

2026-06-14T09:00:00Z | revision | draft-author

Context: task_family=sales_offer, workflow=workflow-77da9260c28a, version=edition-b6a204a69019, reviewer=Emil, customer_segment=standard

```json
{"document_id":"draft-04a5c02d40ac","event":"comment","message":"Could we try the other format in the next design workshop?"}
```

## Private evaluator view

The world policy is distinct from what the evidence identifies. The table shows
the complete registered contexts. Baseline and alternative describe field effects,
not whether a professional convention is desirable. Both means unresolved.
All policies, invalid-context probes and exact values remain in the accompanying JSON.

| Version and context | World | Admitted effects | Direct review witnesses |
| --- | --- | --- | --- |
| version=edition-b6a204a69019, reviewer=Emil, customer_segment=standard | baseline | baseline | record-3e16bb4da3c0 |
| version=edition-b6a204a69019, reviewer=Emil, customer_segment=strategic | alternative | alternative | record-3673101a7b64, record-1e45235d9bc8 |
| version=edition-b6a204a69019, reviewer=Nora, customer_segment=standard | baseline | alternative, baseline | none |
| version=edition-b6a204a69019, reviewer=Nora, customer_segment=strategic | alternative | alternative, baseline | none |

## Future tasks for this development example

### diagnostic

```json
{
  "task_id": "task-3141355b0d05",
  "context": {
    "task_family": "sales_offer",
    "workflow": "workflow-77da9260c28a",
    "version": "edition-b6a204a69019",
    "reviewer": "Emil",
    "customer_segment": "standard"
  },
  "facts": {
    "document_id": "DOC-41179",
    "date": "2026-06-15",
    "monthly_unit_price": "40",
    "seats": "15",
    "annual_total": "7200",
    "contract_reference": "OFF-41179",
    "offer_text": "15 seats at EUR 40 per seat per month, billed annually."
  },
  "baseline_fields": [
    {
      "name": "offer_text",
      "value": "15 seats at EUR 40 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-41179"
    },
    {
      "name": "annual_total",
      "value": "7200"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Expected obligations

```json
{
  "task_id": "task-3141355b0d05",
  "history_id": "history-f513da5f2d2d",
  "probe": "diagnostic",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "offer_text",
      "value": "15 seats at EUR 40 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-41179"
    },
    {
      "name": "annual_total",
      "value": "7200"
    }
  ]
}
```

### control

```json
{
  "task_id": "task-8bedfd127e30",
  "context": {
    "task_family": "sales_offer",
    "workflow": "workflow-77da9260c28a",
    "version": "edition-b6a204a69019",
    "reviewer": "Nora",
    "customer_segment": "standard"
  },
  "facts": {
    "document_id": "DOC-38716",
    "date": "2026-06-15",
    "monthly_unit_price": "40",
    "seats": "15",
    "annual_total": "7200",
    "contract_reference": "OFF-38716",
    "offer_text": "15 seats at EUR 40 per seat per month, billed annually."
  },
  "baseline_fields": [
    {
      "name": "offer_text",
      "value": "15 seats at EUR 40 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-38716"
    },
    {
      "name": "annual_total",
      "value": "7200"
    }
  ],
  "request": "Complete the current work item using the supplied facts and field dictionary. Use only contextually supported adjustments. Retain all unaffected fields."
}
```

Expected obligations

```json
{
  "task_id": "task-8bedfd127e30",
  "history_id": "history-f513da5f2d2d",
  "probe": "control",
  "expected_decision": "keep",
  "recoverable": true,
  "world_fields": [
    {
      "name": "offer_text",
      "value": "15 seats at EUR 40 per seat per month, billed annually."
    },
    {
      "name": "contract_reference",
      "value": "OFF-38716"
    },
    {
      "name": "annual_total",
      "value": "7200"
    }
  ]
}
```

## Human response

Pending. No approval is inferred from this export.
