# U-S retrieval: unidentifiable

History `history-56be5943974d`, 24 records. Synthetic review example; not a scored case.

## Public configuration

* Attributes (predicate tests the second listed value): `access` partner / **internal**; `priority` routine / **urgent**; `document_class` assay_report / **protocol**; `collection` active / **archive**; `site` lab_a / **lab_b**; `file_format` xml / **pdf**
* Candidate attributes (h134): `access`, `priority`, `document_class`, `collection`, `site`, `file_format`
* Target field `checksum`: baseline does not include it; the alternative is `set_fact` with `checksum`.

## Binding approvals (oracle input)

| Record | Reviewer | Context | Configuration |
| --- | --- | --- | --- |
| `record-5eafb4d3c5a7` | Emil | access=internal, priority=routine, document_class=protocol, collection=active, site=lab_a, file_format=xml | alternative |
| `record-c277037a9703` | Emil | access=partner, priority=urgent, document_class=assay_report, collection=active, site=lab_b, file_format=xml | alternative |
| `record-86ec9510aedd` | Emil | access=partner, priority=urgent, document_class=assay_report, collection=active, site=lab_a, file_format=pdf | alternative |
| `record-1879a60c28f5` | Paul | access=partner, priority=routine, document_class=assay_report, collection=archive, site=lab_a, file_format=pdf | alternative |
| `record-0d6c70009a10` | Paul | access=partner, priority=urgent, document_class=assay_report, collection=active, site=lab_a, file_format=xml | alternative |
| `record-69ffe3d914ba` | Paul | access=internal, priority=urgent, document_class=protocol, collection=archive, site=lab_a, file_format=xml | baseline |
| `record-1375f3e30526` | Paul | access=partner, priority=urgent, document_class=assay_report, collection=archive, site=lab_a, file_format=xml | alternative |
| `record-ba2398cf956a` | Paul | access=internal, priority=routine, document_class=protocol, collection=active, site=lab_a, file_format=pdf | alternative |
| `record-3f7a1eb77b1c` | Emil | access=partner, priority=routine, document_class=assay_report, collection=archive, site=lab_a, file_format=xml | alternative |
| `record-d1a9a4bdb984` | Paul | access=partner, priority=urgent, document_class=assay_report, collection=archive, site=lab_a, file_format=pdf | alternative |
| `record-cd2987ff415c` | Emil | access=internal, priority=routine, document_class=protocol, collection=archive, site=lab_b, file_format=xml | alternative |
| `record-8edb0ad0c997` | Emil | access=internal, priority=urgent, document_class=protocol, collection=active, site=lab_b, file_format=pdf | baseline |

## Non-binding records

accepted review without the target field: 2, personal preference: 2, rejected artifact: 2, review outside the roster: 3, technical failure log: 2.

## Oracle derivation

2 function(s) of the declared class fit every binding approval:

* priority=routine OR document_class=assay_report
* access=partner OR priority=routine

## Future tasks and warranted actions

| Task type | Context | Status | Expected |
| --- | --- | --- | --- |
| observed_change | access=internal, priority=routine, document_class=protocol, collection=active, site=lab_a, file_format=pdf | apply | apply |
| observed_retention | access=internal, priority=urgent, document_class=protocol, collection=active, site=lab_b, file_format=pdf | keep | keep |
| unidentifiable | access=partner, priority=urgent, document_class=protocol, collection=archive, site=lab_b, file_format=xml | unresolved | keep |
| control | other workflow (control) | out_of_scope | keep |

## Evaluator-only construction note

Relevant attributes: `priority`, `document_class`; confusable attribute `access` copies `document_class` in every binding approval.
The oracle above does not read this note.
