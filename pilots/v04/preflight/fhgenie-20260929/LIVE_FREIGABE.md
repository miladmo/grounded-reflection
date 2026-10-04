# Neuer v0.4-Lauf über FHGenie

Vorbereitete Anfrage. Noch nicht freigegeben oder gestartet.

## Umfang

Ein vollständiger Lauf mit 192 geplanten Aufrufen auf ausschließlich synthetischen
Daten. Untersucht werden die bestehenden Bedingungen A, B und C. Der Lauf erstellt
eine Schwierigkeitskarte der direkten Anpassung. Er prüft noch keinen zusätzlichen
Grounded-Reflection-Arm und belegt keinen Nutzen in Unternehmen.

Die r2-Fallkonstruktion, öffentlichen Konventionen, Bewertungsregeln und bisherigen
Studienprompts bleiben gleich. Der Modellwechsel wird ausdrücklich dokumentiert.
Frühere fehlgeschlagene Versuche bleiben erhalten und werden nicht überschrieben.

## Modell und Grenzen

| Einstellung | Vorgeschlagener Wert |
| --- | --- |
| Modell | deepseek-ai/DeepSeek-V4-Flash-0731 |
| Zugang | FHGenie On-Prem, vorhandener lokal verschlüsselter Schlüssel |
| Endpoint | <FHGENIE_ENDPOINT> |
| Reasoning | low |
| Temperature / top_p | 1 / 1 |
| Output-Limit je Aufruf | 16.384 Tokens einschließlich der vom Anbieter so gezählten Ausgabe |
| Geplante Aufrufe | 192 |
| Obergrenze | 200 Versuche, keine zusätzlichen Aufrufe vorgesehen |
| Token-Stopp | 6.000.000 gemeldete Tokens, geprüft zwischen Aufrufen |
| Timeout | 420 Sekunden je Aufruf |
| Final-Seeds für Historien / Folgeaufgaben / Reihenfolge | 44361 / 44362 / 44363 |

Kein Retry, kein Ersatzlauf und keine Wiederaufnahme nach einem Abbruch.
Keine Käufe, keine Guthaben-Resets und kein Wechsel auf einen anderen Anbieter.
Bei unbekanntem Verbrauch oder einem Integritätsfehler stoppt der Lauf.
Der Token-Stopp ist keine exakt durchgesetzte Abrechnungsgrenze. Ein bereits
laufender Aufruf kann ihn überschreiten. Ein funktionierender Schlüssel bestätigt
nicht, dass die Nutzung für das Institut kostenlos ist.

## Transport und Datentrennung

Der Python-Transport übergibt genau zwei Nachrichten an einen lokalen PowerShell-7-
HTTP-Treiber. Die Systemnachricht enthält das Antwortschema. Die Nutzernachricht
enthält den unveränderten öffentlichen Studienprompt. Serverseitiges
`response_format` bleibt nach dem erfolgreichen Verbindungstest ausgeschaltet.
Die lokale JSON-Prüfung und die Pydantic-Verträge bleiben verbindlich. Fehlerhafte
Antworten werden nicht repariert.

Der Modellaufruf bietet keine Tools, Dateien, Shell, Browser oder Gesprächssitzung
an. Der lokale Unterprozess startet in einem leeren temporären Arbeitsverzeichnis
außerhalb des Repositories. Dies ist keine Betriebssystem-Sandbox. Die maßgebliche
Grenze ist die tatsächlich gesendete HTTP-Nachricht. Offline-Tests prüfen sowohl
die Python-Übergabe als auch den beim HTTP-Treiber abgefangenen Body und kontrollieren
auf mitgeschickte private Testmarkierungen.

Vorbereitungen erhalten nur öffentliche Historien. Folgeaufgaben werden erst nach
dem Versiegeln der Vorbereitungen erzeugt. Die neuen Final-Seeds werden in dieser
Vorbereitung nicht benutzt. Der Verbindungstest enthielt nur die Aufgabe, ein
kleines JSON-Objekt zurückzugeben. Er enthält keine Forschungsaufgabe und bestätigt
noch keine zuverlässigen Antworten auf die größeren Studienverträge.

Der Treiber sendet höchstens einen POST und folgt keinen Weiterleitungen. Schlüssel,
HTTP-Header und separate Reasoning-Inhalte werden nicht gespeichert. Die finale
Antwort, Modellkennung und gemeldete Nutzung werden protokolliert.

## Nachweise und Freigabestatus

`verification.json` dokumentiert die abgeschlossenen Offline-Prüfungen, Quellcode-
Hashes und den Vergleich der Materialien. Der neue Review-Export übernimmt eine
bestehende Materialfreigabe nur bei Bytegleichheit aller 14 Fall- und Auditdateien.
Das ist keine zusätzliche menschliche Validierung.

Die Live-Freigabe bleibt leer. Die früheren Freigaben für den Codex-Versuch und die
drei FHGenie-Verbindungstests sind verbraucht und gelten nicht für diese Konfiguration.
Eine neue ausdrückliche Freigabe würde genau diesen einmaligen Lauf abdecken.
