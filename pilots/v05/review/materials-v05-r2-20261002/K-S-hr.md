# K-S hr: transfer change

History `history-96cce3be9d8f`, 24 records. Synthetic review example; not a scored case.

## Public configuration

* Attributes (predicate tests the second listed value): `seniority` senior / **junior**; `channel` email / **portal**; `language` german / **english**; `location` onsite / **remote**; `recipient` external / **internal**; `contract` permanent / **temporary**
* Candidate attributes (h14-declared): `recipient`, `contract`
* Target field `booking_reference`: baseline includes it; the alternative is `omit`.

## Binding approvals (oracle input)

| Record | Reviewer | Context | Configuration |
| --- | --- | --- | --- |
| `record-3f4936ee4304` | Theo | seniority=junior, channel=email, language=english, location=onsite, recipient=external, contract=permanent | alternative |
| `record-e089231b2de4` | Emil | seniority=junior, channel=portal, language=german, location=onsite, recipient=internal, contract=permanent | baseline |
| `record-d5ebc69fb127` | Emil | seniority=junior, channel=email, language=english, location=remote, recipient=internal, contract=permanent | baseline |
| `record-e02f4f40870b` | Theo | seniority=senior, channel=email, language=english, location=onsite, recipient=external, contract=permanent | alternative |
| `record-fdf581a575bc` | Theo | seniority=junior, channel=portal, language=german, location=onsite, recipient=internal, contract=permanent | baseline |
| `record-021772848f85` | Emil | seniority=senior, channel=portal, language=english, location=remote, recipient=internal, contract=temporary | alternative |
| `record-df31412c119d` | Emil | seniority=senior, channel=portal, language=english, location=remote, recipient=external, contract=permanent | alternative |
| `record-77f8a788e197` | Emil | seniority=senior, channel=email, language=english, location=remote, recipient=internal, contract=temporary | alternative |
| `record-3074c3545ef3` | Theo | seniority=senior, channel=email, language=german, location=onsite, recipient=internal, contract=temporary | alternative |
| `record-f70bf3eeb16f` | Theo | seniority=junior, channel=email, language=english, location=remote, recipient=external, contract=permanent | alternative |
| `record-47c53e756005` | Emil | seniority=junior, channel=email, language=english, location=onsite, recipient=internal, contract=temporary | alternative |
| `record-bfef71c8c817` | Theo | seniority=junior, channel=portal, language=german, location=remote, recipient=internal, contract=permanent | baseline |

## Non-binding records

accepted review without the target field: 2, personal preference: 2, rejected artifact: 2, review outside the roster: 3, technical failure log: 2.

## Oracle derivation

1 function(s) of the declared class fit every binding approval:

* recipient=external OR contract=temporary

## Future tasks and warranted actions

| Task type | Context | Status | Expected |
| --- | --- | --- | --- |
| observed_change | seniority=senior, channel=portal, language=english, location=remote, recipient=external, contract=permanent | apply | apply |
| observed_retention | seniority=junior, channel=portal, language=german, location=onsite, recipient=internal, contract=permanent | keep | keep |
| transfer_change | seniority=junior, channel=portal, language=german, location=onsite, recipient=external, contract=temporary | apply | apply |
| control | other workflow (control) | out_of_scope | keep |

## Evaluator-only construction note

Relevant attributes: `recipient`, `contract`.
The oracle above does not read this note.
