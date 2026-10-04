# FHGenie-Vertragstest, Stufe high

Nur technische Tauglichkeit. Modellentscheidungen wurden nicht bewertet.
Plan-SHA-256 `3ee95edd8d63481ed32eaebb5a16c186b377bd306429537515606866eea920b6`.

**Ergebnis: passed.** Bestanden. Die Stufe kann für den finalen Lauf festgelegt werden (separate Live-Freigabe nötig).

Gültig 16 von 16; ungültig einschließlich blockierter 0 (0.0%). Format 0, Output-Grenze 0, andere 0, blockiert 0, nicht versucht 0.

| Nr. | Aufruf | Typ | Ergebnis | Grund | finish | Input | Output | Reasoning | Sekunden |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 01-C1-C-H1 | C1_small | valid |  | stop | 4031 | 11256 |  | 66.565924 |
| 2 | 02-C1-C-H2 | C1_small | valid |  | stop | 4175 | 11829 |  | 72.554583 |
| 3 | 03-C1-C-H3 | C1_large | valid |  | stop | 20032 | 11551 |  | 66.083014 |
| 4 | 04-C1-C-H4 | C1_large | valid |  | stop | 21176 | 13603 |  | 77.636439 |
| 5 | 05-C2-C-H1 | C2_small | valid |  | stop | 5419 | 12621 |  | 91.2534 |
| 6 | 06-C2-C-H2 | C2_small | valid |  | stop | 5822 | 9650 |  | 48.968477 |
| 7 | 07-C2-C-H3 | C2_large | valid |  | stop | 20726 | 15552 |  | 89.896606 |
| 8 | 08-C2-C-H4 | C2_large | valid |  | stop | 22502 | 13316 |  | 62.853786 |
| 9 | 09-gen-C-H1 | C_gen | valid |  | stop | 2688 | 404 |  | 2.621087 |
| 10 | 10-gen-C-H2 | C_gen | valid |  | stop | 2606 | 835 |  | 7.706935 |
| 11 | 11-gen-C-H3 | C_gen | valid |  | stop | 2499 | 1370 |  | 11.302427 |
| 12 | 12-gen-C-H4 | C_gen | valid |  | stop | 2707 | 1030 |  | 5.856625 |
| 13 | 13-gen-B-H2 | B_small | valid |  | stop | 5123 | 1988 |  | 11.65259 |
| 14 | 14-gen-B-H4 | B_large | valid |  | stop | 22127 | 2541 |  | 14.809643 |
| 15 | 15-gen-A-H1 | A | valid |  | stop | 2589 | 484 |  | 3.434542 |
| 16 | 16-gen-A-H3 | A | valid |  | stop | 2494 | 621 |  | 6.118957 |

## Tokenhochrechnung für 192 Aufrufe

Kleinstes Verhältnis Zeichen je Token: 3.0974.
Eingabe: 1,461,271. Zusätze: {'C2_previous_preparation': 36159, 'C_generation_guidance': 2290}.
Ausgabe je Typ: {'A': 29808, 'B_large': 40656, 'B_small': 81312, 'C1_large': 108824, 'C1_small': 189264, 'C2_large': 124416, 'C2_small': 201936, 'C_gen': 65760} (Basis {'A': 'max_of_type', 'B_large': 'max_of_stage', 'B_small': 'max_of_stage', 'C1_large': 'max_of_type', 'C1_small': 'max_of_type', 'C2_large': 'max_of_type', 'C2_small': 'max_of_type', 'C_gen': 'max_of_type'}).
**Projektion: 2,341,696 Tokens** gegenüber Grenze 4,800,000: bestanden.
Obere Laufzeitschätzung: 1.5 Stunden.

Kein Retry, keine Reparatur, kein Ersatzaufruf. Verbrauch dieses Tests zählt nicht zum Budget des finalen Laufs.
