# K-L sales: unidentifiable

History `history-002c0c904864`, 240 records. Synthetic review example; not a scored case.

## Public configuration

* Attributes (predicate tests the second listed value): `product_line` premium / **core**; `account_owner` Sada / **Mira**; `region` south / **north**; `contract_term` one_year / **multi_year**; `deal_source` direct / **partner**; `customer_segment` standard / **strategic**
* Candidate attributes (h14-declared): `region`, `deal_source`
* Target field `annual_total`: baseline includes it; the alternative is `omit`.

## Binding approvals (oracle input)

| Record | Reviewer | Context | Configuration |
| --- | --- | --- | --- |
| `record-a6aa982d3f39` | Anika | product_line=premium, account_owner=Mira, region=north, contract_term=one_year, deal_source=partner, customer_segment=standard | alternative |
| `record-20425e614298` | Leon | product_line=premium, account_owner=Sada, region=south, contract_term=multi_year, deal_source=direct, customer_segment=strategic | baseline |
| `record-55f30904d817` | Leon | product_line=core, account_owner=Sada, region=south, contract_term=multi_year, deal_source=direct, customer_segment=standard | baseline |
| `record-655c59c1a0b2` | Anika | product_line=premium, account_owner=Mira, region=north, contract_term=one_year, deal_source=partner, customer_segment=strategic | alternative |
| `record-5464796d1c34` | Anika | product_line=premium, account_owner=Mira, region=north, contract_term=one_year, deal_source=partner, customer_segment=strategic | alternative |
| `record-4d90c75b16d9` | Leon | product_line=core, account_owner=Sada, region=north, contract_term=multi_year, deal_source=partner, customer_segment=standard | alternative |
| `record-77e65451afd3` | Anika | product_line=core, account_owner=Mira, region=south, contract_term=one_year, deal_source=direct, customer_segment=standard | baseline |
| `record-3196cf47c781` | Anika | product_line=premium, account_owner=Sada, region=south, contract_term=one_year, deal_source=direct, customer_segment=standard | baseline |
| `record-3b03eaf4e76d` | Leon | product_line=premium, account_owner=Sada, region=north, contract_term=one_year, deal_source=partner, customer_segment=strategic | alternative |
| `record-99038b46f0ae` | Anika | product_line=premium, account_owner=Mira, region=south, contract_term=one_year, deal_source=direct, customer_segment=standard | baseline |
| `record-3e1c93474384` | Leon | product_line=premium, account_owner=Mira, region=south, contract_term=multi_year, deal_source=direct, customer_segment=standard | baseline |
| `record-c945d368d499` | Leon | product_line=premium, account_owner=Sada, region=north, contract_term=multi_year, deal_source=partner, customer_segment=strategic | alternative |

## Non-binding records

accepted review without the target field: 49, personal preference: 49, rejected artifact: 49, review outside the roster: 49, technical failure log: 31.

## Oracle derivation

4 function(s) of the declared class fit every binding approval:

* region=north AND deal_source=partner
* region=north
* deal_source=partner
* region=north OR deal_source=partner

## Future tasks and warranted actions

| Task type | Context | Status | Expected |
| --- | --- | --- | --- |
| observed_change | product_line=premium, account_owner=Mira, region=north, contract_term=one_year, deal_source=partner, customer_segment=strategic | apply | apply |
| observed_retention | product_line=premium, account_owner=Mira, region=south, contract_term=one_year, deal_source=direct, customer_segment=standard | keep | keep |
| unidentifiable | product_line=premium, account_owner=Mira, region=north, contract_term=one_year, deal_source=direct, customer_segment=strategic | unresolved | keep |
| control | other workflow (control) | out_of_scope | keep |

## Evaluator-only construction note

Relevant attributes: `region`, `deal_source`.
The oracle above does not read this note.
