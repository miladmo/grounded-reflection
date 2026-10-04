# Separate Live-Freigabe für Pilot v0.4

Stand 29. September 2026. **Noch nicht freigegeben. Kein echter Modellaufruf gestartet.**

Die Materialfreigabe durch Milad Morad ist dokumentiert. S1 und S5 wurden zusätzlich
anhand der öffentlichen Konventionen KI-gestützt geprüft. Diese Zusatzprüfung ist
keine unabhängige menschliche Validierung. Die sechs Fälle und der Oberflächentest
bleiben in allen 14 Materialdateien byte-identisch. Der neue Export bindet allein
die überarbeitete Transportimplementierung und ihre Tests.

## Zur Freigabe vorgelegter Lauf

| Einstellung | Festgelegter Wert |
| --- | --- |
| Modell | `gpt-6-sol` |
| Reasoning | `medium` |
| Transport | Installierte Codex CLI `0.155.0-alpha.16.4`, ChatGPT-Anmeldung, gesperrter lokaler Gateway zum festen ChatGPT-Codex-Endpunkt |
| Geplante Aufrufe | 192, davon 48 Vorbereitungen und 144 Aufgabenausführungen in A/B/C |
| Absolute Aufrufgrenze | 200 Versuche. Höchstens eine ausgehende Modellanfrage je Versuch |
| Token-Stopp | 6.000.000 gemeldete Eingabe- plus Ausgabetokens, zwischen Aufrufen geprüft |
| Timeout | 420 Sekunden je Aufruf |
| Seeds | Historien 44341, zukünftige Aufgaben 44342, Reihenfolge 44343 |
| Wiederholungen | Keine Retries, Ersatzläufe oder Wiederaufnahme |
| Käufe | Keine Käufe, Credit-Resets oder API-Key-Fallbacks |

Die freien acht Plätze sind keine Erlaubnis für zusätzliche Versuche. Der feste
Plan bleibt bei 192. Ein Integritätsfehler oder unbekannter Tokenverbrauch stoppt
den Lauf. Die letzte laufende Antwort kann die Tokengrenze überschreiten. Es
handelt sich daher nicht um eine exakt garantierte harte Tokenobergrenze.

## Tatsächlich durchgeführte Isolationsprüfung

Die finale CLI lief lokal gegen einen Antwortsimulator. Die produktive
Transportimplementierung und ihre Hashprüfung waren aktiv. Nur die ausgehende
HTTPS-Verbindung wurde durch eine lokale Fixture ersetzt und die Anmeldung für
diese Fixture deaktiviert. Ein kontrolliertes temporäres Verzeichnis außerhalb
des Repositorys ermöglichte echte Prüfdateien im übergeordneten Verzeichnis und
daneben. Keine Anfrage wurde an einen Inferenzdienst weitergeleitet.

* Alle drei erfassten Anfragen enthielten keine Werkzeuge, auch nicht in verschachtelten Tool-Definitionen.
* Keine Prüfzeichen aus Evaluatordateien, zukünftigen Aufgaben oder der übergeordneten `AGENTS.md` waren in der Modelleingabe enthalten.
* Die normale Fixture-Antwort wurde verarbeitet. Ein HTTP-503-Fehler führte zu keinem Retry.
* Eine injizierte Werkzeugantwort wurde abgefangen, bevor die CLI sie ausführen konnte. Alle drei Proben erzeugten jeweils genau eine lokale ausgehende Anfrage.
* 157 Offline-Tests bestanden. Zusätzlich sperrt der Gateway jeden zweiten Request vor der Weiterleitung.

Der Nachweis beruht auf fehlenden Modellwerkzeugen und geprüften Anfragen. Er
behauptet keine Betriebssystem-Sperre für beliebige Dateizugriffe. Eine andere
CLI-Version, geänderter Code oder Modellkatalog besteht die Hashprüfung nicht.
Die Annahme durch den entfernten Dienst bleibt bis zur Live-Freigabe ungeprüft.

Die finalen Testaufgaben wurden nicht erzeugt oder angesehen. Ihre Instanziierung
erfolgt erst nach dem im Protokoll vorgesehenen Einfrieren der Vorbereitungen.
Die Daten sind vollständig synthetisch. Frühere Pilotdateien bleiben erhalten.

## Prüfnachweise

Die [Konfiguration](run-config.json), der [Prüfbericht](verification.json) und das
[Testprotokoll](offline-tests.txt) sind gespeichert. Die Materialien und die
separate Freigabe stehen unter
`pilots/v04/review/materials-amendment3-r2-live-ready-20260929` und der zugehörigen
`-approvals.json`. Deren Live-Feld bleibt leer, bis die ausdrückliche Antwort vorliegt.

* Quellbindung `8dab3506c3c26b0c5eaeb3318104e2eec15efe8b5de1755ea42bcc9e75b47fd4`
* Materialbindung `fad6299fffe016c28c954ba0f34f6989f95c64c3953282071017fe2cccd1d31a`
* Konfiguration `e265476641d895eaea855b70844ee5d8228eb9e3383ea298207e11c76250d0cb`

**Freigabefrage**

Gibst du genau diesen einmaligen Live-Lauf mit diesen Grenzen und dem beschriebenen
Token-Stopp frei? Die Freigabe gilt nicht für Nachläufe, zusätzliche Studienarme
oder Käufe.
