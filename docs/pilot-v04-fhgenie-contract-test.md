# Pilot v0.4: FHGenie-Vertragstest auf Entwicklungsdaten

Plan und Umsetzung freigegeben von Milad Morad am 30. September 2026, mit der Vorgabe
Reasoning-Stufe `high` (siehe Amendment 4). **Nicht ausgeführt.** Jeder Modellaufruf
braucht eine gesonderte ausdrückliche Freigabe, die an den exakten Plan-Hash gebunden ist.
Das gilt getrennt für jede Reasoning-Stufe.

Harness: `pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/`.

## Zweck und Grenze

Der Test prüft allein, ob DeepSeek-V4-Flash-0731 über FHGenie technisch mit den
tatsächlichen Studienverträgen umgehen kann.

* JSON-Gültigkeit und Vertragsgültigkeit (lokaler strikter Parser und unveränderte
  Pydantic-Verträge; bei C2 zusätzlich gültige Belegverweise wie im Runner)
* Abschluss mit `finish_reason = stop`, also kein Abbruch an der Output-Grenze
* gemeldeter Tokenverbrauch je Aufruf (Input, Output, Reasoning, soweit gemeldet)
* Laufzeit je Aufruf gegenüber dem Timeout von 420 Sekunden
* Modellkennung und Server-Fingerprint

Die Ergebnisse dienen **nicht** der Anpassung von Materialien, Prompts, Schwierigkeit,
Fallauswahl, Seeds oder Auswertung. Inhaltliche Entscheidungen werden nicht bewertet:
Der Harness wendet keinen Evaluator an und berechnet keine Scores, Headroom-Werte oder
Fehlerattributionen. Rohantworten werden nur zur technischen Diagnose aufbewahrt. Die
finalen Seeds 44361, 44362 und 44363 werden nicht benutzt, und es werden keine finalen
Historien oder Folgeaufgaben erzeugt.

## Material

Entwicklungs-Namespace der Revision `v04-amendment-03-r2` mit den bestehenden Seeds
44321 (Historien), 44322 (Folgeaufgaben) und 44323 (Reihenfolge). Die Historien sind
dieselben wie im Offline-Lauf `runs/offline-fhgenie-integration-20260929`. Alle acht
Prompts, die nicht von früheren Modellantworten abhängen, sind nachweislich byte-gleich
mit den dortigen Prompts.

| Kürzel | Slot | Historie | Aufgabentyp |
| --- | --- | --- | --- |
| H1 | S0 Sales | 6 Einträge, interpretiert | Änderung im beobachteten Kontext |
| H2 | S1 Sales | 6 Einträge, roh | nicht identifizierbar |
| H3 | S2 Reporting | 60 Einträge, interpretiert | Änderung mit Transfer |
| H4 | S5 Retrieval | 60 Einträge, roh, kombiniert | Änderung mit Transfer |

## Aufrufplan (16 Aufrufe)

| Nr. | Aufruf | Historien | Anzahl |
| --- | --- | --- | --- |
| 1–4 | C1-Vorbereitung | H1, H2, H3, H4 | 4 |
| 5–8 | C2-Vorbereitung | H1, H2, H3, H4 | 4 |
| 9–12 | C-Generierung, Diagnoseaufgabe | H1, H2, H3, H4 | 4 |
| 13–14 | B-Generierung, Diagnoseaufgabe | H2, H4 | 2 |
| 15–16 | A-Generierung, Diagnoseaufgabe | H1, H3 | 2 |

B läuft auf H4, weil B-Aufrufe über große Historien die längsten Eingaben der Studie
haben (hier 69.905 Zeichen). Die Reihenfolge ist fest.

Ist ein C1 ungültig, sind das zugehörige C2 und die C-Generierung blockiert. Ist ein C2
ungültig oder sind seine Leitlinien nicht ausführbar, ist die C-Generierung blockiert.
Blockierte Aufrufe werden nicht ersetzt und zählen konservativ als nicht bestanden.

## Laufregeln

* Dieselben Transportregeln wie im finalen Lauf: gebundener Transport und Treiber, ein
  POST je Aufruf, keine Weiterleitung, kein Retry, keine Reparatur, kein
  `response_format`, Reasoning `high`, Output-Limit 16.384, Temperature/top_p 1,
  Timeout 420 s.
* Sofortiger Stopp des gesamten Tests bei unbekanntem oder ungültigem Verbrauch,
  falscher Modellkennung, Tool-Aufruf, Integritätsfehler oder Transportfehler. Ein
  Timeout oder HTTP-Fehler liefert keine Tokenangabe und stoppt deshalb ebenfalls.
  Das entspricht der bestehenden Regel „unbekannter Verbrauch stoppt“.
* Eigener Token-Stopp für den Test: 600.000 gemeldete Tokens, zwischen Aufrufen
  geprüft. Obere Abschätzung für 16 Aufrufe: etwa 0,6 Millionen Tokens, realistisch
  deutlich weniger. Diese Tokens zählen nicht zum 6.000.000-Budget des finalen Laufs,
  werden aber berichtet.
* Keine Wiederholung einzelner Aufrufe. Ein Test je Stufe. Die Freigabe wird vor dem
  ersten Aufruf exklusiv reserviert und kann nicht erneut verwendet werden.

## Vorab festgelegte Entscheidungsregel

Als ungültig zählt eine Antwort bei ungültigem JSON, Vertragsverletzung,
`finish_reason ≠ stop`, Verweigerung oder fehlendem Inhalt. Blockierte Aufrufe zählen
ebenfalls als ungültig. Nenner sind immer die 16 geplanten Aufrufe.

1. **Bestanden:** höchstens 1 von 16 ungültig (≤ 6,25 Prozent, also nicht über
   10 Prozent) **und** kein Stopp **und** die Tokenhochrechnung (unten) besteht **und**
   kein Aufruf über 336 Sekunden (80 Prozent des Timeouts). `high` wird dann für den
   finalen Lauf festgelegt.
2. **Ungültigkeit über 10 Prozent** (2 oder mehr von 16):
   * Eskalation auf `max` nach neuer Freigabe mit demselben Plan, nur wenn alle drei
     Bedingungen gelten: Formatfehler (JSON oder Vertrag) sind häufiger als alle anderen
     direkten Fehler zusammen, die Tokenhochrechnung besteht und kein Aufruf dauert über
     336 Sekunden.
   * Sonst Stopp ohne Eskalation. Das gilt vor allem, wenn Abbrüche an der Output-Grenze
     überwiegen, denn eine höhere Stufe lässt mehr Output und längere Laufzeit erwarten.
   * Scheitert auch `max`, wird gestoppt. Das Modell gilt dann über diesen Transport als
     technisch ungeeignet für die Studienverträge.
3. **Tokenhochrechnung nicht bestanden** oder **ein Aufruf über 336 Sekunden:** keine
   Eskalation, Stopp und Bericht.

Nach einem Stopp folgt keine automatische Reparatur. Änderungen am Output-Limit, an
Prompts, am Antwortschema, an `response_format` oder ein anderes Modell wären eine neue,
dokumentierte Iteration mit eigenem Amendment, eigener Freigabe und neuem Vertragstest.
Die Regel wird nach Kenntnis der Ergebnisse nicht gelockert.

Einschränkung: 16 Aufrufe können eine Ungültigkeitsrate im finalen Lauf nicht
belegen. Auch bei 0 von 16 ist eine wahre Rate um 17 Prozent mit dem Ergebnis
vereinbar (einseitige obere 95-Prozent-Grenze nach Clopper-Pearson). Der Test schließt
nur grobe Untauglichkeit aus. Ungültige Antworten im finalen Lauf bleiben nach der
bestehenden Taxonomie technische Fehler in ihren Nennern.

## Tokenhochrechnung für 192 Aufrufe

### Ausgangslage ohne Modellaufrufe

Die Eingaben aller 192 Aufrufe auf dem Entwicklungsmaterial (Studienprompt plus
Systemnachricht mit Schema, mit leerer Vorbereitung) umfassen **4.526.103 Zeichen**.
Der Harness berechnet diese Basis selbst und legt sie im Plan ab.

| Aufruftyp | Anzahl im Plan | mittlere Eingabe (Zeichen) |
| --- | --- | --- |
| A | 48 | ca. 12.200 |
| B, kleine Historien (S0, S1, S3, S4) | 32 | ca. 20.500 |
| B, große Historien (S2, S5) | 16 | ca. 70.000 |
| C-Generierung | 48 | ca. 12.200 plus übernommene Leitlinien |
| C1, klein / groß | 16 / 8 | ca. 16.400 / 65.900 |
| C2, klein / groß | 16 / 8 | ca. 16.300 / 65.800 plus C1-Antwort |

Das Zeichen-Token-Verhältnis des DeepSeek-Tokenizers ist nicht gemessen. Bei 2,5 bis
4 Zeichen je Token ergeben sich etwa **1,1 bis 1,8 Millionen Eingabetokens**. Die
Ausgabe einschließlich Reasoning ist durch das Output-Limit begrenzt, sofern FHGenie es
durchsetzt: 192 × 16.384 = **3,15 Millionen**. Die zusätzlichen Eingaben aus
C1-Antworten und Leitlinien betragen höchstens 72 × 16.384 = 1,18 Millionen. Die
theoretische Obergrenze liegt damit bei etwa **6,1 Millionen**, knapp über dem Stopp.

Mit `high` sind mehr Reasoning-Tokens je Aufruf zu erwarten als mit `low`. Der
Abstand zur Obergrenze ist damit kleiner, und Abbrüche an der Output-Grenze werden
wahrscheinlicher. Das Risiko ist kein Mehrverbrauch über den Stopp hinaus (höchstens
ein laufender Aufruf), sondern ein unvollständiger finaler Lauf.

### Rechenregel mit den Messwerten

1. **Eingabe:** Aus den gemeldeten `input_tokens` und den bekannten Eingabelängen wird
   je Aufruf das Verhältnis Zeichen je Token bestimmt. Maßgeblich ist das kleinste
   beobachtete Verhältnis. Damit werden die 4.526.103 Basiszeichen umgerechnet.
2. **Ausgabe:** Für jeden Aufruftyp (A, B klein, B groß, C1 klein, C1 groß, C2 klein,
   C2 groß, C-Generierung) wird der größte gemessene `output_tokens`-Wert mit der
   Anzahl im Plan multipliziert. Hat ein Typ weniger als zwei Messwerte (B klein,
   B groß oder durch Blockierung), gilt der größte Wert seiner Stufe: aller
   Generierungen bzw. aller Vorbereitungen. Ohne Messwert gilt das Limit von 16.384.
3. **Zusatzeingaben:** Die mittlere gemessene Mehrlänge der C2-Prompts (vorherige
   Vorbereitung) wird für 24 C2-Aufrufe addiert, die der C-Generierungen (Leitlinien)
   für 48 Aufrufe, jeweils mit dem Verhältnis aus Schritt 1. Ohne Messwert gilt das
   Limit je Aufruf.
4. **Projektion** = Summe aus 1 bis 3.

Kriterium: Die Projektion muss **höchstens 4.800.000** Tokens betragen (80 Prozent
von 6.000.000). Zwischen 4.800.000 und 6.000.000 gilt das Kriterium als nicht
bestanden; Milad entscheidet dann ausdrücklich über das weitere Vorgehen. Eine
Budgeterhöhung oder Kürzung des Plans ist damit nicht vorab genehmigt. Über 6.000.000
wird mit dieser Konfiguration kein finaler Lauf gestartet.

Laufzeit: Die Summe aus der größten gemessenen Laufzeit je Aufruftyp mal Anzahl wird
als obere Schätzung der Gesamtdauer berichtet. Ohne Messwert gelten 420 Sekunden.

## Ablage und Bericht

Alles liegt im Harness-Verzeichnis: `plan.json`, später `approval.json` (nur nach
tatsächlicher Freigabe), die Reservierung `attempt.json` sowie `run/` mit je Aufruf
der credential-freien Anfrage, dem finalen Antwortkanal, den Transportmetadaten und
einem Ergebnisdatensatz, dazu `results.json` und `REPORT.md`. Der Test schreibt nicht in
`runs/`, `review/`, `preflight/` oder bestehende Diagnoseverzeichnisse.

Der Bericht enthält je Aufruf: Typ, Ergebnis mit Grund, `finish_reason`, Input-,
Output- und Reasoning-Tokens, Laufzeit und Fingerprint; dazu die Hochrechnung mit allen
Zwischenwerten und das Ergebnis der Entscheidungsregel. Er enthält keine inhaltlichen
Bewertungen.

## Umsetzung

* Der Harness `contract_test.py` ruft den gebundenen FHGenie-Transport direkt auf und
  nicht den Studien-Backend. Der Backend würde schon eine einzelne Antwort mit
  ungültigem JSON oder einen Abbruch an der Output-Grenze als Integritätsfehler
  behandeln und den Lauf beenden. Der Vertragstest muss solche Antworten aber zählen,
  solange Verbrauch und Integrität bekannt sind.
* `plan` erzeugt den Plan offline. `verify` berechnet ihn neu und vergleicht Byte für
  Byte. `execute --once` rechnet den Plan erneut nach und verlangt eine passende
  Freigabe sowie eine unbenutzte Reservierung, bevor ein Aufruf erfolgt.
* Der Plan bindet die Quellbindung von v0.4, den Harness, Transport und Treiber, die
  Python-/pydantic-Version und das PowerShell-7-Programm per Hash. Weicht etwas ab,
  erfolgt kein Aufruf.
* 18 Offline-Tests mit gefälschtem Transport prüfen: Seeds und Reihenfolge, die
  192er-Basis, Gleichheit der Zeichenzählung mit dem echten Transport, Freigabe- und
  Reservierungsschranke, Blockierung, alle Stoppbedingungen, die Rechenregel und die
  Entscheidungsregel. Weder Schlüssel noch Netzwerk werden benutzt.

## Offene Punkte für den finalen Lauf (nicht Teil dieses Tests)

* Der Studien-Backend beendet den gesamten Lauf bereits bei einer einzelnen Antwort mit
  ungültigem JSON oder einem Abbruch an der Output-Grenze, weil beides als Audit-Fehler
  des Transports erscheint. Vertragsfehler bei gültigem JSON beenden den Lauf nicht. Das
  Protokoll sieht dagegen vor, dass unabhängige Aufrufe nach einem isolierten
  Antwortfehler weiterlaufen. Das muss vor dem finalen Lauf entschieden werden.
* Der Backend übergibt dem Transport kein PowerShell-Programm. Der Transport sucht dann
  `pwsh` im PATH, wo es auf diesem Rechner nicht liegt. Ohne Anpassung würde der finale
  Lauf beim ersten Aufruf mit `powershell_7_unavailable` stoppen.

## Vertragstest 2: Output-Limit 32.768 (Amendment 5, Option B2)

Die Erhöhung des Output-Limits verlangt nach der obigen Regel einen neuen Test.
Harness: `pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/`.

* Gleiches Material, gleiche 16 Aufrufe und Reihenfolge, Stufe `high`, gleiche
  Entscheidungsregel und gleiche Hochrechnung. Einziger Unterschied: das Output-Limit
  von 32.768 Tokens. Ohne Messwert setzt die Hochrechnung dieses Limit ein.
* Die Freigabe muss zusätzlich `max_output_tokens: 32768` enthalten. Eine Freigabe für
  Test 1 gilt nicht für Test 2.
* Der Token-Stopp des Tests bleibt bei 600.000. Mit dem höheren Limit liegt die
  theoretische Obergrenze bei etwa 0,75 Millionen, Test 1 verbrauchte 255.367 Tokens.
  Wird der Stopp erreicht, ist der Test unvollständig und nicht bestanden.
* Test 1 bleibt als abgeschlossener Befund unverändert. Die Offene-Punkte-Liste oben
  ist durch Amendment 5 umgesetzt: Antwortfehler mit Grenze und fester PowerShell-Pfad.

## Freigabevermerk

Vertragstest-Plan mit Stufe `high`: freigegeben, Milad Morad, 30. September 2026.
Umsetzung des Harness: freigegeben, Milad Morad, 30. September 2026.
Ausführung Stufe `high`: freigegeben, Milad Morad, 30. September 2026. Tatsächliche
Antwort: „Vertragstest auf Stufe high freigegeben, ausführen“. Einmal ausgeführt,
Ergebnis **bestanden** (16/16 gültig, Projektion 2.341.696 Tokens, 255.367 Tokens
verbraucht). Bericht: `pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/run/REPORT.md`.
Ausführung Stufe `max`: nicht erforderlich.
Vertragstest 2 (Output-Limit 32.768): Plan und Umsetzung freigegeben mit Amendment 5,
Milad Morad, 30. September 2026. Ausführung freigegeben, tatsächliche Antwort:
„Vertragstest 2 freigegeben, ausführen und danach vorbereiten“. Einmal ausgeführt,
Ergebnis **bestanden** (16/16 gültig, Projektion 2.459.918 Tokens, 258.451 Tokens
verbraucht). Der größte Output betrug 24.848 Tokens (C2, S2 Reporting) und hätte das
frühere Limit von 16.384 überschritten. Bericht:
`pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/run/REPORT.md`.
