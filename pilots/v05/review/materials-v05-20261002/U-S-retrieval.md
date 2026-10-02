# U-S retrieval: unidentifiable

History `history-54fba246d24d`, 24 records. Synthetic review example; not a scored case.

## Public configuration

* Attributes (predicate tests the second listed value): `access` partner / **internal**; `priority` routine / **urgent**; `document_class` assay_report / **protocol**; `collection` active / **archive**; `site` lab_a / **lab_b**; `file_format` xml / **pdf**
* Candidate attributes (h134): `access`, `priority`, `document_class`, `collection`, `site`, `file_format`
* Target field `checksum`: baseline does not include it; the alternative is `set_fact` with `checksum`.

## Binding approvals (oracle input)

| Record | Reviewer | Context | Configuration |
| --- | --- | --- | --- |
| `record-cd9fe93a5173` | Greta | access=internal, priority=routine, document_class=protocol, collection=active, site=lab_b, file_format=pdf | baseline |
| `record-3f7a1eb77b1c` | Leon | access=internal, priority=routine, document_class=protocol, collection=active, site=lab_a, file_format=xml | baseline |
| `record-f41a7510e350` | Leon | access=partner, priority=urgent, document_class=assay_report, collection=active, site=lab_a, file_format=pdf | baseline |
| `record-4db607caf0d9` | Greta | access=internal, priority=routine, document_class=protocol, collection=active, site=lab_a, file_format=pdf | baseline |
| `record-0d6c70009a10` | Greta | access=internal, priority=routine, document_class=protocol, collection=active, site=lab_b, file_format=pdf | baseline |
| `record-6e8401f132cc` | Greta | access=internal, priority=urgent, document_class=protocol, collection=active, site=lab_a, file_format=xml | baseline |
| `record-050967727dc0` | Leon | access=partner, priority=routine, document_class=assay_report, collection=archive, site=lab_a, file_format=pdf | alternative |
| `record-5931ed1dcd83` | Leon | access=internal, priority=urgent, document_class=protocol, collection=archive, site=lab_a, file_format=pdf | baseline |
| `record-8432b2d84ee7` | Leon | access=internal, priority=routine, document_class=protocol, collection=active, site=lab_a, file_format=xml | baseline |
| `record-ee194f668ebb` | Greta | access=partner, priority=urgent, document_class=assay_report, collection=active, site=lab_a, file_format=pdf | baseline |
| `record-5268c7c51195` | Greta | access=internal, priority=routine, document_class=protocol, collection=active, site=lab_b, file_format=xml | baseline |
| `record-cf3477ede979` | Leon | access=internal, priority=routine, document_class=protocol, collection=active, site=lab_a, file_format=pdf | baseline |

## Non-binding records

accepted review without the target field: 2, personal preference: 2, rejected artifact: 2, review outside the roster: 3, technical failure log: 2.

## Oracle derivation

5 function(s) of the declared class fit every binding approval:

* priority=routine AND document_class=assay_report
* document_class=assay_report AND collection=archive
* access=partner AND priority=routine
* priority=routine AND collection=archive
* access=partner AND collection=archive

## Future tasks and warranted actions

| Task type | Context | Status | Expected |
| --- | --- | --- | --- |
| observed_change | access=partner, priority=routine, document_class=assay_report, collection=archive, site=lab_a, file_format=pdf | apply | apply |
| observed_retention | access=internal, priority=routine, document_class=protocol, collection=active, site=lab_b, file_format=pdf | keep | keep |
| unidentifiable | access=partner, priority=urgent, document_class=protocol, collection=archive, site=lab_a, file_format=pdf | unresolved | keep |
| control | other workflow (control) | out_of_scope | keep |

## Evaluator-only construction note

Relevant attributes: `priority`, `document_class`; confusable attribute `access` copies `document_class` in every binding approval.
The oracle above does not read this note.
