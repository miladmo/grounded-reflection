# Fehlerzuordnung der C-Diagnosen S4 und S1

Lauf `runs/live-fhgenie-high-20260930` (Siegel `7afab956…dbb8594`), vorbereitet am
1. Oktober 2026. Die Einschätzungen unten sind **KI-gestützt** und keine menschliche
Validierung. Maßgeblich ist deine Entscheidung. Sie wird getrennt in
[responses.json](responses.json) festgehalten. Der versiegelte Lauf wird nicht verändert.

> **Nachtrag 1. Oktober 2026:** Die KI-gestützte Empfehlung „technical“ für die beiden
> S4-Fälle ist nach der [eingereichten Rückmeldung](feedback-20261001.md) überholt.
> Vertretbarer ist „unresolved“ mit dem Zusatzmerkmal `baseline_polarity_inverted`.
> **Tatsächliche Zuordnung durch Milad Morad (1. Oktober 2026):** S4 Sales unresolved,
> S4 HR unresolved (beide `baseline_polarity_inverted`), S1 Sales content. Siehe
> [responses.json](responses.json).

## Worum es geht

C hat 21 von 24 Diagnosen richtig. Die drei Fehler liegen in S1 (1) und S4 (2). Das
Headroom-Kriterium (höchstens 2/4 richtig **und** mindestens 60 % reine Inhaltsfehler)
kann nur in S4 greifen. Dort sind **beide** Fehler als Inhaltsfehler nötig. Wird einer
davon technisch oder gemischt eingeordnet, ist Headroom in S4 nicht erfüllt. Die
maschinelle Einordnung lautet vorläufig „content“, aber die bestätigte Untergrenze liegt
bei 0 %.

Die Taxonomie aus dem Protokoll:

| Kategorie | Bedeutung |
| --- | --- |
| Content | Schlussfehler aus der Evidenz, z. B. falscher Geltungsbereich, veraltete Evidenz, Ablenker übernommen, gerechtfertigte Änderung verpasst |
| Technical | ungültiges Feld oder Format, **korrekt formulierte Regel falsch kodiert**, korrekte Leitlinie nicht ausgeführt |
| Mixed | nachweisbarer Schlussfehler **und** technischer Defekt |
| Unresolved | Artefakte rechtfertigen keine Zuordnung |

Konventionen in allen Fällen: x prüft den zweiten Wert der ersten Kontextdimension, y den
der zweiten. 1 bedeutet Alternative, 0 Grundkonfiguration. Die Klasse H14 umfasst 14
Boolesche Funktionen ohne XOR und XNOR, je Version eine.

---

## Fall 1: S4 Sales, Änderung im beobachteten Kontext

`history-69cdd9239e11`, Aufgabe `task-f0ce9e3cd666`, Stand 15.06.2026.

**Konfiguration:** Die Grundkonfiguration **enthält** `annual_total`. Die Alternative
ist `omit`, also Weglassen. x = account_owner Sada, y = customer_segment strategic.

**Öffentliche Einträge**

| Zeit | Wer | Version | Kontext | Inhalt |
| --- | --- | --- | --- | --- |
| 01.01. | Registry | alt `4c4d…` | – | gültig bis 01.06., Prüfer Theo, Jonas |
| 22.05. | Theo | alt | Emil/standard | akzeptiert, `annual_total` **enthalten** |
| 01.06. | Registry | aktuell `18b3…` | – | ersetzt alte Version, gültig bis 01.01.2027, Prüfer Elena, Daria |
| 05.06. | Elena | aktuell | Sada/standard | akzeptiert, **enthalten** (= Grundkonfiguration) |
| 08.06. | Elena | aktuell | Emil/standard | akzeptiert, **entfernt** (9600 → leer) |
| 11.06. | Daria | aktuell | Emil/standard | akzeptiert, **entfernt** (3000 → leer) |

**Orakel:** f(Emil/std)=1, f(Sada/std)=0. Verträglich sind ¬x, ¬x∧¬y und ¬x∨y. Alle
drei verlangen im Diagnosekontext Emil/standard das Weglassen. **Erwartet: apply**
(`annual_total` weglassen).

**C1 und C2:** Die Evidenz wird korrekt gelesen. Die alte Version wird ausdrücklich
ignoriert, und beide Emil/standard-Freigaben werden als Weglassen erkannt. Dann steht in
beiden Vorbereitungen sinngemäß: *„Die Grundkonfiguration lässt annual_total bereits
weg; die Freigaben bei Emil/standard bestätigen das, daher ist dort keine Regel nötig.“*
Das ist falsch. Übernommen wird nur `set_fact annual_total` bei Sada/standard, was der
Grundkonfiguration entspricht und nichts bewirkt. Die von C genannten verträglichen
Funktionen (x, x∧¬y, x∨y) sind genau die Komplemente der Orakelfunktionen. Die
Schlussfolgerung ist also in sich stimmig, nur mit vertauschter 0/1-Bedeutung.

**Ausführung:** C erhält keine Anweisung und behält `annual_total` = 3000. **B** lässt
das Feld korrekt weg.

**KI-gestützte Einschätzung:** Die Anforderung (Weglassen bei Emil/standard) wurde
richtig erschlossen, aber wegen einer falschen Annahme über die Grundkonfiguration nicht
als Regel kodiert. Das entspricht am ehesten „korrekt formulierte Regel falsch kodiert“,
also **technical**. Vertretbar ist auch **mixed**, wenn man das Fehllesen der öffentlichen
Konfiguration als Interpretationsfehler wertet. **Content** im Sinn eines Schlussfehlers
aus der Evidenz stützen die Artefakte nicht. Die automatische Auswertung findet ebenfalls
0 Inhaltsfehler in der Vorbereitung.

---

## Fall 2: S4 HR, Änderung mit Transfer

`history-f22b09024bb8`, Aufgabe `task-a920bd4a9f81`.

**Konfiguration:** Die Grundkonfiguration **enthält** `booking_reference`, die
Alternative ist `omit`. x = recipient external, y = contract temporary.

**Öffentliche Einträge**

| Zeit | Wer | Version | Kontext | Inhalt |
| --- | --- | --- | --- | --- |
| 01.01. | Registry | alt `11fd…` | – | gültig bis 01.06., Prüfer Jonas, Anika |
| 11.05. | Jonas | alt | internal/permanent | akzeptiert, **enthalten** |
| 01.06. | Registry | aktuell `5e05…` | – | ersetzt alte Version, Prüfer Robin, Anika |
| 08.06. | Robin | aktuell | external/temporary | akzeptiert, **entfernt** |
| 09.06. | Anika | aktuell | internal/permanent | akzeptiert, **entfernt** |
| 14.06. | Robin | aktuell | internal/temporary | akzeptiert, **enthalten** |

**Orakel:** f(int/perm)=1, f(int/temp)=0, f(ext/temp)=1. Das bestimmt eindeutig x∨¬y.
Im **nicht beobachteten** Diagnosekontext external/permanent ergibt das 1.
**Erwartet: apply** (`booking_reference` weglassen).

**C1 und C2:** C leitet korrekt und eindeutig her: *„einschließen genau dann, wenn
internal und temporary; alle anderen Kombinationen weglassen, also auch
external/permanent“*. Damit ist auch der Transfer auf den unbeobachteten Kontext richtig.
Dann folgt: *„Die Grundkonfiguration wendet die Weglass-Option bereits an, daher braucht
nur die Einschlussbedingung eine Regel.“* Das ist falsch. Übernommen wird nur `set_fact`
bei internal/temporary.

**Ausführung:** C erhält keine Anweisung und behält `booking_reference`. **B** lässt das
Feld korrekt weg.

**KI-gestützte Einschätzung:** Das gleiche Muster wie in Fall 1. Die Transferinferenz
ist korrekt, die Kodierung scheitert an der falschen Annahme über die
Grundkonfiguration. Empfehlung: **technical**, vertretbar **mixed**, nicht **content**.

---

## Fall 3: S1 Sales, nicht identifizierbar

`history-d1b3a7f01f48`, Aufgabe `task-e259eacd8c3d`, Rohdarstellung (Entwurf und Ersatz).

**Konfiguration:** Die Grundkonfiguration **enthält** `annual_total`, die Alternative
ist `omit`. x = account_owner Sada, y = customer_segment strategic.

**Öffentliche Einträge (alle aktuelle Version, Prüfer Theo und Daria)**

| Zeit | Wer | Art | Kontext | Inhalt |
| --- | --- | --- | --- | --- |
| 25.05. | Theo | Review | Sada/strategic | akzeptierter Ersatz **mit** `annual_total` |
| 07.06. | Daria | Review | Mira/standard | akzeptierter Ersatz **ohne** `annual_total` (Entwurf hatte 11700) |
| 11.06. 09:08 | Theo | Review | Sada/strategic | erneut **mit** `annual_total` |
| 11.06. 13:15 | Daria | **Präferenz** | Mira/strategic | „I would prefer annual_total omitted“, keine Freigabe |
| 11.06. 17:40 | Laufzeit | Log | Mira/standard | 503, dann 200 (technisch) |

**Orakel:** f(Mira/std)=1, f(Sada/strat)=0. Verträglich sind ¬x, ¬y, ¬x∨¬y und ¬x∧¬y.
Im Diagnosekontext Mira/strategic liefern ¬x und ¬x∨¬y den Wert 1, ¬y und ¬x∧¬y den
Wert 0. Die Funktionen widersprechen sich, also ist der Fall nicht identifizierbar.
**Erwartet: keep** (Grundkonfiguration beibehalten, ohne sie als erwiesen zu behaupten).

**C1:** Die Grundkonfiguration wird korrekt gelesen. Begründung für die Übernahme:
*„Die akzeptierte Mira/standard-Freigabe **und die Mira/strategic-Präferenz**
rechtfertigen ein Weglassen für account_owner=Mira.“* Übernommen wird `omit` für alle
Mira-Kontexte.

**C2:** Dieselbe Regel. Begründung: nur ¬x und ¬x∨¬y seien verträglich. Das ist
unvollständig, denn ¬y und ¬x∧¬y fehlen.

**Ausführung:** C lässt `annual_total` weg. **B** behält es korrekt. Die tatsächliche
Welt ist ¬x, deshalb stimmt C zufällig mit der Welt überein, aber nicht mit der
gerechtfertigten Entscheidung.

**KI-gestützte Einschätzung:** C übernimmt einen unverbindlichen Ablenker (die
Präferenz), zählt die verträglichen Funktionen unvollständig auf und erweitert den
Geltungsbereich ungestützt auf Mira/strategic. Empfehlung: **content**. Kein technischer
Defekt erkennbar. Für Headroom ist der Fall ohne Folgen (S1: 3/4 richtig).

---

## Beobachtung über die Einzelfälle hinaus

Nur 6 der 24 Historien haben „weglassen“ als Alternative, das heißt, die
Grundkonfiguration enthält das Feld (Sales in S1 und S4; HR in S1, S2, S4 und S5).
**Alle drei C-Fehler liegen in diesen sechs Historien.** In den übrigen 18 Historien
macht C keinen Diagnosefehler.

| Historie mit Alternative „weglassen“ | Aufgabentyp | C richtig | Grundkonfiguration von C richtig gelesen |
| --- | --- | --- | --- |
| S1 HR | Beibehaltung mit Transfer | ja | ja |
| S1 Sales | nicht identifizierbar | nein (Fall 3) | ja |
| S2 HR | Änderung im beobachteten Kontext | ja | ja |
| S4 HR | Änderung mit Transfer | nein (Fall 2) | **nein** |
| S4 Sales | Änderung im beobachteten Kontext | nein (Fall 1) | **nein** |
| S5 HR | Beibehaltung mit Transfer | ja | ja |

Die Fehllesung tritt also in 2 von 6 dieser Historien auf, jeweils in S4. In S2 HR
wurde dieselbe Richtung korrekt gelesen und korrekt kodiert. Einen durchgängigen
Darstellungsfehler gibt es damit nicht. Die Häufung in der Weglass-Richtung (3 von 6
gegenüber 0 von 18) ist aber ein Befund, den der Bericht nennen sollte. Bei vier
Diagnosen je Setting ist das nur ein Hinweis, keine belastbare Schätzung.

In beiden S4-Fällen zeigt die alte Version das Feld **enthalten** und die aktuelle es
**entfernt**. Eine mögliche, **ungeprüfte** Erklärung: C deutet den Versionswechsel als
Wechsel der Grundkonfiguration. Das berührt die v0.5-Frage nach zeitlicher Provenienz,
wäre dann aber ein Darstellungs- und kein Evidenzfehler. Zwei Fälle belegen das nicht.

Für die Deutung heißt das: Die Karte vermischt in S4 die Wirkung des zeitlichen Bruchs
mit der Richtung der Alternative. Die feste Zuteilung trennt beides nicht, weil beide
S4-Änderungsfälle die Weglass-Richtung haben.

## Folgen je nach Entscheidung

| S4 Fall 1 | S4 Fall 2 | Headroom S4 |
| --- | --- | --- |
| content | content | erfüllt (2/4 richtig, 2/2 Inhaltsfehler) |
| content | technical/mixed/unresolved | nicht erfüllt |
| technical/mixed/unresolved | beliebig | nicht erfüllt |

Nach der KI-gestützten Einschätzung wäre Headroom **in keinem Setting** erfüllt. Die
Karte zeigt dann eine Deckengrenze der Inferenz bei DeepSeek-V4-Flash mit `high`. Die
beiden S4-Fehler wären als Kodierungsproblem zu berichten, das den Arm C trifft,
nicht B.

## Deine Entscheidung

Bitte je Fall eine Kategorie (content, technical, mixed, unresolved) und optional eine
Begründung. Ich trage deine tatsächliche Antwort in [responses.json](responses.json) ein
und aktualisiere danach den Abschlussbericht.
