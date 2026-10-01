# Pilot v0.4, Amendment 5: Fehlertoleranz, PowerShell und Reasoning `high`

Freigegeben von Milad Morad am 30. September 2026 mit Option B2. Die Freigabe
autorisiert keinen Modellaufruf; der neue Vertragstest und der finale Lauf brauchen
jeweils eine eigene ausdrückliche Freigabe. Materialien, Prompts, Seeds, Orakel und Auswertung bleiben
unverändert. D bleibt ausgeschlossen.

Anlass ist der bestandene Vertragstest auf Stufe `high`
(`pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/run/REPORT.md`) und die
Rückmeldung von Milad Morad vom 30. September 2026: Fehler zulassen, aber mit Grenze;
`high` festschreiben, weil hohes Reasoning für den Piloten wichtig ist; PowerShell-Pfad
klären.

## A. Einzelne Antwortfehler zulassen, mit Grenze

**Heute:** Der Backend beendet den ganzen Lauf, sobald eine einzige Antwort ungültiges
JSON enthält, an der Output-Grenze abbricht, verweigert wird oder keinen Inhalt hat. Diese
Fälle erscheinen als Audit-Fehler des Transports. Vertragsfehler bei gültigem JSON beenden
den Lauf dagegen nicht. Das Protokoll sieht vor, dass unabhängige Aufrufe nach einem
isolierten Antwortfehler weiterlaufen.

**Vorschlag:**

1. **Antwortfehler** beenden den Lauf nicht mehr. Dazu zählen ungültiges JSON,
   `finish_reason ≠ stop` (etwa ein Abbruch an der Output-Grenze), Verweigerung, fehlender
   Inhalt, falsche Rolle oder Choice-Anzahl und Vertragsverletzung.
   Voraussetzung ist, dass die Antwort mit HTTP 200, korrekter Modellkennung und
   bekanntem Verbrauch zurückkommt. Der Aufruf wird als fehlgeschlagen gespeichert,
   sein finaler Kanal bleibt erhalten, und nichts wird repariert.
2. Abhängige Aufrufe bleiben wie bisher blockiert: Ein fehlgeschlagenes C1 blockiert C2
   und beide C-Aufgaben dieser Historie, ein fehlgeschlagenes C2 die C-Aufgaben. Alle
   Positionen bleiben in ihren Nennern und zählen als nicht korrekt. In der Taxonomie
   sind sie **technische** Fehler, keine Inhaltsfehler.
3. **Grenze:** Höchstens 19 Antwortfehler im Lauf (unter 10 Prozent von 192, dieselbe
   Schwelle wie im Vertragstest). Beim 20. Antwortfehler werden keine weiteren Aufrufe
   geplant. Der Lauf endet dann als unvollständig, ohne Wiederaufnahme oder Ersatz.
   Blockierte Folgeaufrufe zählen nicht zur Grenze, werden aber getrennt berichtet.
4. **Weiterhin sofortiger Stopp** bei unbekanntem oder ungültigem Verbrauch, falscher
   Modellkennung, Tool-Aufruf, HTTP-, Timeout- oder Transportfehler, Quell-, Siegel- oder
   Integritätsfehler und beim Token-Stopp von 6.000.000.

**Folgen für die Auswertung:** Technische Fehler senken die Trefferquote, zählen aber
nicht als Inhaltsfehler im Headroom-Kriterium. Viele technische Fehler machen das
Headroom-Kriterium deshalb schwerer erreichbar und die Karte weniger aussagekräftig. Der
Bericht weist Antwortfehler je Arm, Aufruftyp und Setting aus.

**Umsetzung:** Anpassung in `backend.py` (Klassifikation von Antwort- und
Systemfehlern) und `runner.py` (Zählung und Grenze). Offline-Tests mit Fehlerinjektion:
Weiterlauf nach einem Fehler, Blockierung, Stopp beim 20. Fehler, Stopp bei unbekanntem
Verbrauch, Nenner.

## B. Output-Limit bei Stufe `high`

Im Vertragstest brauchten die Vorbereitungsaufrufe C1 und C2 9.650 bis 15.552 von 16.384
Output-Tokens, einschließlich Reasoning. Im finalen Lauf gibt es 48 solcher Aufrufe. Ein
Abbruch an der Grenze ist deshalb plausibel. Jeder Abbruch bei C1 oder C2 blockiert beide
C-Aufgaben der Historie, benachteiligt also gezielt den untersuchten Arm C.

* **B1, Limit 16.384 beibehalten.** Kein neuer Test nötig. Abbrüche werden Antwortfehler
  nach A und zählen zur Grenze.
* **B2, Limit auf 32.768 erhöhen (empfohlen).** Die Hochrechnung ändert sich nicht, weil
  sie auf gemessenem Verbrauch beruht: 2,34 Millionen bei 4,8 Millionen Grenze. Die
  theoretische Obergrenze steigt, bleibt aber durch den Token-Stopp von 6.000.000
  abgesichert. Nach der Regel des Vertragstests verlangt eine Änderung des Output-Limits
  einen neuen Vertragstest: dieselben 16 Aufrufe auf Entwicklungsdaten, etwa 0,26 Millionen
  Tokens, mit eigener Freigabe. Ob FHGenie 32.768 akzeptiert, ist ungeprüft; der Test würde
  es zeigen.

Die Stufe `high` bleibt in beiden Optionen unverändert.

**Gewählt: B2.** Laut Milad Morad setzt FHGenie selbst keine Token-Grenzen. Der
Token-Stopp von 6.000.000 bleibt trotzdem als Protokollgrenze des Laufs bestehen; er ist
eine Grenze der Studie, keine Anbietergrenze. Das Output-Limit von 32.768 wird als
Anfrageparameter gesendet. Ob FHGenie es anwendet, zeigt der neue Vertragstest.

## C. PowerShell 7 für den finalen Lauf

**Heute:** Der Backend übergibt kein PowerShell-Programm. Der Transport sucht `pwsh` im
PATH, wo es auf diesem Rechner nicht liegt. Der finale Lauf würde beim ersten Aufruf mit
`powershell_7_unavailable` stoppen.

Das Hilfsskript `diagnostics/fhgenie/fhgenie.ps1` läuft in Windows PowerShell 5.1, aber
nur zum Speichern des Schlüssels und zum Abrufen der Modellliste. Der Anfrage-Treiber
braucht PowerShell 7 (`-MaximumRetryCount`, `System.Text.Json`). Der per DPAPI
gespeicherte Schlüssel ist unter beiden Versionen für dasselbe Windows-Konto lesbar. Das
zeigt der erfolgreiche Vertragstest.

**Vorschlag:** Die Laufkonfiguration erhält den festen Pfad zu dem PowerShell-7-Programm,
das im Vertragstest verwendet wurde
(`%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe`),
und dessen SHA-256. Der Runner prüft den Hash vor der Reservierung der Freigabe, der
Backend übergibt den Pfad an den Transport. Ein anderes Programm ergibt einen anderen
Konfigurations-Hash und braucht eine neue Freigabe.

Verworfene Alternativen:
* Den Treiber nach Windows PowerShell 5.1 portieren: größere, ungetestete Änderung.
* PowerShell 7 systemweit installieren: Systemänderung, die zudem nicht an die geprüfte
  Version gebunden wäre.

## D. Reasoning `high` festschreiben

* `config.py`: Für FHGenie ist nur `high` zulässig, mit dem Output-Limit aus B.
  `transport` und Treiber akzeptieren weiterhin die drei dokumentierten Stufen. Die
  Konfiguration legt die Stufe verbindlich fest.
* Neue Laufkonfiguration unter `pilots/v04/preflight/fhgenie-high-<datum>/run-config.json`
  mit `high`, Output-Limit, PowerShell-Pfad und -Hash sowie den Final-Seeds
  44361/44362/44363.
* Danach wie beim letzten Transportwechsel: volle Offline-Testsuite, kompletter Mock-Lauf
  mit 192 Aufrufen, neuer Review-Export mit Byte-Vergleich der 14 Material- und
  Auditdateien (Übernahme der Materialfreigabe nur bei Gleichheit), neue
  `verification.json` und neue `LIVE_FREIGABE.md`.

## Reihenfolge

1. Freigabe dieses Amendments einschließlich der Wahl B1 oder B2.
2. Umsetzung von A, C und D in einem Durchgang, nur offline. Die bestehenden Läufe,
   Vertragstestergebnisse und Freigaben bleiben unverändert.
3. Nur bei B2: neuer Vertragstest mit 32.768 Tokens, nach eigener ausdrücklicher Freigabe.
4. Quellbindung, Review-Export, Verifikation und Live-Anfrage.
5. Separate ausdrückliche Live-Freigabe des finalen Laufs.

## Umsetzung (30. September 2026, offline)

* `config.py`: FHGenie verlangt Reasoning `high`, ein Output-Limit bis 32.768, einen
  PowerShell-7-Pfad mit SHA-256 und höchstens 19 tolerierte Antwortfehler.
* `backend.py`: Antwortfehler nach vollständigem Austausch (HTTP 200, ein Request,
  korrektes Modell, bekannter Verbrauch, kein Tool) erhalten `failure_class = response`
  und beenden den Lauf nicht. Der 20. setzt `response_failure_limit`. Alles andere bleibt
  systemisch. Der PowerShell-Pfad wird an den Transport übergeben.
* `runner.py`: prüft den PowerShell-Hash vor der Reservierung und meldet ungültige
  C2-Belegverweise als Antwortfehler.
* Tests für Weiterlauf, Grenze, Belegverweise, systemische Fälle und PowerShell-Hash.

## Freigabevermerk

Amendment 5: freigegeben, Option B2.

Reviewer: Milad Morad
Datum: 30. September 2026
Tatsächliche Antwort: „Amendment 5 freigegeben, B2 mit neuem Vertragstest. folge B2, wobei
es über fhgenie keine token limits gibt.“

Neuer Vertragstest mit 32.768: ausgeführt am 30. September 2026, bestanden (16/16
gültig, Projektion 2.459.918 Tokens). Das Output-Limit 32.768 ist damit festgelegt.
Live-Freigabe: ausstehend.
