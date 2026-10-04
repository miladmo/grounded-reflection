# U-L reporting: transfer change

History `history-73cbefc42bdf`, 240 records. Synthetic review example; not a scored case.

## Public configuration

* Attributes (predicate tests the second listed value): `channel` portal / **email**; `department` operations / **finance**; `period` quarterly / **monthly**; `audience` internal / **external**; `language` english / **german**; `artifact` numeric_table / **chart**
* Candidate attributes (h134): `channel`, `department`, `period`, `audience`, `language`, `artifact`
* Target field `snapshot_label`: baseline does not include it; the alternative is `set_fact` with `snapshot_label`.

## Binding approvals (oracle input)

| Record | Reviewer | Context | Configuration |
| --- | --- | --- | --- |
| `record-680a40d507be` | Emil | channel=email, department=operations, period=monthly, audience=external, language=german, artifact=numeric_table | alternative |
| `record-455926529682` | Nora | channel=portal, department=operations, period=monthly, audience=external, language=german, artifact=numeric_table | alternative |
| `record-2ab9cafe5f24` | Nora | channel=portal, department=finance, period=quarterly, audience=internal, language=english, artifact=chart | baseline |
| `record-06914c8f6d52` | Emil | channel=portal, department=finance, period=quarterly, audience=internal, language=english, artifact=numeric_table | baseline |
| `record-7d316b55a514` | Nora | channel=portal, department=operations, period=quarterly, audience=internal, language=english, artifact=numeric_table | baseline |
| `record-46b42648c57b` | Emil | channel=email, department=operations, period=quarterly, audience=internal, language=english, artifact=numeric_table | alternative |
| `record-af2d216a9105` | Emil | channel=email, department=finance, period=monthly, audience=external, language=english, artifact=numeric_table | alternative |
| `record-26f99553d538` | Emil | channel=portal, department=finance, period=monthly, audience=external, language=english, artifact=chart | alternative |
| `record-f1a4fd2b28e3` | Nora | channel=portal, department=finance, period=monthly, audience=external, language=english, artifact=chart | alternative |
| `record-7afa0f05c88f` | Nora | channel=email, department=finance, period=monthly, audience=external, language=german, artifact=chart | alternative |
| `record-5bc62dda1da9` | Nora | channel=email, department=operations, period=monthly, audience=external, language=english, artifact=numeric_table | alternative |
| `record-437d5d21c9b0` | Emil | channel=portal, department=operations, period=quarterly, audience=internal, language=german, artifact=numeric_table | baseline |

## Non-binding records

accepted review without the target field: 49, personal preference: 49, rejected artifact: 49, review outside the roster: 49, technical failure log: 31.

## Oracle derivation

2 function(s) of the declared class fit every binding approval:

* channel=email OR period=monthly
* channel=email OR audience=external

## Future tasks and warranted actions

| Task type | Context | Status | Expected |
| --- | --- | --- | --- |
| observed_change | channel=email, department=operations, period=monthly, audience=external, language=german, artifact=numeric_table | apply | apply |
| observed_retention | channel=portal, department=operations, period=quarterly, audience=internal, language=german, artifact=numeric_table | keep | keep |
| transfer_change | channel=email, department=finance, period=quarterly, audience=internal, language=german, artifact=numeric_table | apply | apply |
| control | other workflow (control) | out_of_scope | keep |

## Evaluator-only construction note

Relevant attributes: `channel`, `period`; confusable attribute `audience` copies `period` in every binding approval.
The oracle above does not read this note.
