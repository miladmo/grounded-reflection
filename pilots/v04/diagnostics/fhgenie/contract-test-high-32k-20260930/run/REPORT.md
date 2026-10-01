# FHGenie-Vertragstest 2, Stufe high, Output-Limit 32,768

Nur technische Tauglichkeit. Modellentscheidungen wurden nicht bewertet.
Plan-SHA-256 `c0fd147d987f5e3115a087c7b55c76e97e7d5a13296a535df857433a03d08abe`.

**Ergebnis: passed.** Bestanden. Die Stufe kann für den finalen Lauf festgelegt werden (separate Live-Freigabe nötig).

Gültig 16 von 16; ungültig einschließlich blockierter 0 (0.0%). Format 0, Output-Grenze 0, andere 0, blockiert 0, nicht versucht 0.

| Nr. | Aufruf | Typ | Ergebnis | Grund | finish | Input | Output | Reasoning | Sekunden |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 01-C1-C-H1 | C1_small | valid |  | stop | 4031 | 7122 |  | 42.185278 |
| 2 | 02-C1-C-H2 | C1_small | valid |  | stop | 4175 | 12928 |  | 80.998372 |
| 3 | 03-C1-C-H3 | C1_large | valid |  | stop | 20032 | 11866 |  | 78.049056 |
| 4 | 04-C1-C-H4 | C1_large | valid |  | stop | 21176 | 9082 |  | 69.004315 |
| 5 | 05-C2-C-H1 | C2_small | valid |  | stop | 4582 | 10815 |  | 87.559792 |
| 6 | 06-C2-C-H2 | C2_small | valid |  | stop | 5537 | 12978 |  | 84.216539 |
| 7 | 07-C2-C-H3 | C2_large | valid |  | stop | 21008 | 24848 |  | 135.545409 |
| 8 | 08-C2-C-H4 | C2_large | valid |  | stop | 21808 | 14033 |  | 91.111607 |
| 9 | 09-gen-C-H1 | C_gen | valid |  | stop | 2692 | 725 |  | 5.491164 |
| 10 | 10-gen-C-H2 | C_gen | valid |  | stop | 2606 | 633 |  | 4.311561 |
| 11 | 11-gen-C-H3 | C_gen | valid |  | stop | 2499 | 569 |  | 4.043457 |
| 12 | 12-gen-C-H4 | C_gen | valid |  | stop | 2707 | 669 |  | 4.156427 |
| 13 | 13-gen-B-H2 | B_small | valid |  | stop | 5123 | 1854 |  | 15.765885 |
| 14 | 14-gen-B-H4 | B_large | valid |  | stop | 22127 | 4115 |  | 19.423853 |
| 15 | 15-gen-A-H1 | A | valid |  | stop | 2589 | 406 |  | 3.324763 |
| 16 | 16-gen-A-H3 | A | valid |  | stop | 2494 | 622 |  | 4.453381 |

## Tokenhochrechnung für 192 Aufrufe

Kleinstes Verhältnis Zeichen je Token: 3.0974.
Eingabe: 1,461,271. Zusätze: {'C2_previous_preparation': 25942, 'C_generation_guidance': 2321}.
Ausgabe je Typ: {'A': 29856, 'B_large': 65840, 'B_small': 131680, 'C1_large': 94928, 'C1_small': 206848, 'C2_large': 198784, 'C2_small': 207648, 'C_gen': 34800} (Basis {'A': 'max_of_type', 'B_large': 'max_of_stage', 'B_small': 'max_of_stage', 'C1_large': 'max_of_type', 'C1_small': 'max_of_type', 'C2_large': 'max_of_type', 'C2_small': 'max_of_type', 'C_gen': 'max_of_type'}).
**Projektion: 2,459,918 Tokens** gegenüber Grenze 4,800,000: bestanden.
Obere Laufzeitschätzung: 1.6 Stunden.

Kein Retry, keine Reparatur, kein Ersatzaufruf. Verbrauch dieses Tests zählt nicht zum Budget des finalen Laufs.
