# K-S hr: transfer change

History `history-849bc0a746a9`, 24 records. Synthetic review example; not a scored case.

## Public configuration

* Attributes (predicate tests the second listed value): `seniority` senior / **junior**; `channel` email / **portal**; `language` german / **english**; `location` onsite / **remote**; `recipient` external / **internal**; `contract` permanent / **temporary**
* Candidate attributes (h14-declared): `recipient`, `contract`
* Target field `booking_reference`: baseline includes it; the alternative is `omit`.

## Binding approvals (oracle input)

| Record | Reviewer | Context | Configuration |
| --- | --- | --- | --- |
| `record-77f8a788e197` | Jonas | seniority=junior, channel=email, language=english, location=remote, recipient=internal, contract=permanent | baseline |
| `record-2e4d7c589bf0` | Malte | seniority=junior, channel=portal, language=german, location=onsite, recipient=internal, contract=permanent | baseline |
| `record-f084dddd04ae` | Malte | seniority=senior, channel=portal, language=german, location=onsite, recipient=internal, contract=permanent | baseline |
| `record-bfef71c8c817` | Jonas | seniority=junior, channel=email, language=english, location=onsite, recipient=internal, contract=temporary | alternative |
| `record-c10448c1238d` | Malte | seniority=junior, channel=portal, language=german, location=remote, recipient=internal, contract=temporary | alternative |
| `record-e02f4f40870b` | Malte | seniority=junior, channel=email, language=english, location=onsite, recipient=internal, contract=temporary | alternative |
| `record-3f4936ee4304` | Malte | seniority=senior, channel=portal, language=german, location=onsite, recipient=external, contract=permanent | alternative |
| `record-7440f8240df9` | Jonas | seniority=junior, channel=email, language=german, location=onsite, recipient=internal, contract=temporary | alternative |
| `record-e5bce0899c7e` | Jonas | seniority=junior, channel=portal, language=german, location=onsite, recipient=external, contract=permanent | alternative |
| `record-bbeb82d2d6d6` | Jonas | seniority=junior, channel=email, language=english, location=remote, recipient=external, contract=permanent | alternative |
| `record-5b6d061b4a64` | Malte | seniority=senior, channel=email, language=english, location=onsite, recipient=external, contract=permanent | alternative |
| `record-6971fcc8e8f4` | Jonas | seniority=senior, channel=portal, language=english, location=remote, recipient=internal, contract=permanent | baseline |

## Non-binding records

accepted review without the target field: 2, personal preference: 2, rejected artifact: 2, review outside the roster: 3, technical failure log: 2.

## Oracle derivation

1 function(s) of the declared class fit every binding approval:

* recipient=external OR contract=temporary

## Future tasks and warranted actions

| Task type | Context | Status | Expected |
| --- | --- | --- | --- |
| observed_change | seniority=junior, channel=email, language=english, location=onsite, recipient=internal, contract=temporary | apply | apply |
| observed_retention | seniority=senior, channel=portal, language=german, location=onsite, recipient=internal, contract=permanent | keep | keep |
| transfer_change | seniority=junior, channel=email, language=german, location=onsite, recipient=external, contract=temporary | apply | apply |
| control | other workflow (control) | out_of_scope | keep |

## Evaluator-only construction note

Relevant attributes: `recipient`, `contract`.
The oracle above does not read this note.
