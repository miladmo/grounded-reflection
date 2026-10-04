# U-L reporting: transfer change

History `history-54bce27f3141`, 240 records. Synthetic review example; not a scored case.

## Public configuration

* Attributes (predicate tests the second listed value): `channel` portal / **email**; `department` operations / **finance**; `period` quarterly / **monthly**; `audience` internal / **external**; `language` english / **german**; `artifact` numeric_table / **chart**
* Candidate attributes (h134): `channel`, `department`, `period`, `audience`, `language`, `artifact`
* Target field `snapshot_label`: baseline does not include it; the alternative is `set_fact` with `snapshot_label`.

## Binding approvals (oracle input)

| Record | Reviewer | Context | Configuration |
| --- | --- | --- | --- |
| `record-46b42648c57b` | Lea | channel=email, department=finance, period=quarterly, audience=internal, language=german, artifact=chart | baseline |
| `record-455926529682` | Lea | channel=email, department=finance, period=monthly, audience=external, language=english, artifact=chart | alternative |
| `record-1e7f33ddc0dc` | Anika | channel=email, department=finance, period=quarterly, audience=internal, language=english, artifact=numeric_table | baseline |
| `record-ff0d9ee02cdb` | Lea | channel=portal, department=operations, period=monthly, audience=external, language=german, artifact=chart | alternative |
| `record-583b08fc7188` | Lea | channel=email, department=operations, period=monthly, audience=external, language=german, artifact=numeric_table | alternative |
| `record-680a40d507be` | Anika | channel=email, department=finance, period=quarterly, audience=internal, language=english, artifact=chart | baseline |
| `record-217b14aa4843` | Lea | channel=portal, department=finance, period=monthly, audience=external, language=english, artifact=numeric_table | alternative |
| `record-a8bc7013c4b5` | Anika | channel=portal, department=operations, period=quarterly, audience=internal, language=german, artifact=numeric_table | alternative |
| `record-06914c8f6d52` | Anika | channel=email, department=operations, period=monthly, audience=external, language=english, artifact=chart | alternative |
| `record-5bc62dda1da9` | Anika | channel=portal, department=operations, period=monthly, audience=external, language=german, artifact=numeric_table | alternative |
| `record-437d5d21c9b0` | Anika | channel=portal, department=operations, period=quarterly, audience=internal, language=german, artifact=chart | alternative |
| `record-7d316b55a514` | Lea | channel=email, department=operations, period=monthly, audience=external, language=english, artifact=numeric_table | alternative |

## Non-binding records

accepted review without the target field: 49, personal preference: 49, rejected artifact: 49, review outside the roster: 49, technical failure log: 31.

## Oracle derivation

4 function(s) of the declared class fit every binding approval:

* department=operations OR period=monthly
* channel=portal OR period=monthly
* department=operations OR audience=external
* channel=portal OR audience=external

## Future tasks and warranted actions

| Task type | Context | Status | Expected |
| --- | --- | --- | --- |
| observed_change | channel=portal, department=finance, period=monthly, audience=external, language=english, artifact=numeric_table | apply | apply |
| observed_retention | channel=email, department=finance, period=quarterly, audience=internal, language=german, artifact=chart | keep | keep |
| transfer_change | channel=portal, department=operations, period=quarterly, audience=external, language=german, artifact=chart | apply | apply |
| control | other workflow (control) | out_of_scope | keep |

## Evaluator-only construction note

Relevant attributes: `channel`, `period`; confusable attribute `audience` copies `period` in every binding approval.
The oracle above does not read this note.
