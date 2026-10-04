# Live-Lauf v0.4 über FHGenie, Reasoning `high`

Vorbereitete Anfrage vom 30. September 2026. **Noch nicht freigegeben, nicht gestartet.**

## Umfang

Ein einmaliger Lauf mit 192 geplanten Aufrufen (48 C-Vorbereitungen, 144 Aufgaben in
A/B/C) auf ausschließlich synthetischen Daten der Revision `v04-amendment-03-r2`. Er
erstellt die Schwierigkeitskarte der direkten Anpassung. Er prüft keinen
Grounded-Reflection-Arm und belegt keinen Nutzen in Unternehmen. D bleibt ausgeschlossen.
Die Ergebnisse gelten nur für dieses Modell und sind nicht mit v0.3 vergleichbar
(Amendment 4).

## Konfiguration

| Einstellung | Wert |
| --- | --- |
| Modell | `deepseek-ai/DeepSeek-V4-Flash-0731` über FHGenie |
| Endpoint | `<FHGENIE_ENDPOINT>` |
| Reasoning | `high` |
| Output-Limit je Aufruf | 32.768 Tokens |
| Temperature / top_p | 1 / 1 |
| Timeout | 420 Sekunden je Aufruf |
| Final-Seeds Historien / Folgeaufgaben / Reihenfolge | 44361 / 44362 / 44363 |
| Geplante Aufrufe / Obergrenze | 192 / 200 Versuche |
| Token-Stopp | 6.000.000 gemeldete Tokens, zwischen Aufrufen geprüft |
| Tolerierte Antwortfehler | 19; der 20. beendet die weitere Planung |
| PowerShell 7 | fester Pfad, SHA-256 `362a356c…0ad139` |

Konfigurations-SHA-256: `23477ae8e2f511227f84cdcb1acb45f264b1d15ca704d8e628b0cdd145678829`
([run-config.json](run-config.json)).

## Regeln

* Kein Retry, kein Ersatzlauf, keine Wiederaufnahme, keine Käufe.
* Eine unbrauchbare Antwort nach einem sonst intakten Austausch zählt als technischer
  Fehler im Nenner. Abhängige C-Aufrufe sind dann blockiert. Beim 20. solchen Fehler
  endet der Lauf als unvollständig.
* Sofortiger Stopp bei unbekanntem Verbrauch, falscher Modellkennung, Tool-Aufruf,
  HTTP-, Timeout- oder Transportfehler, Quell- oder Siegelfehler und beim Token-Stopp.
* Vorbereitungen werden versiegelt, bevor die Folgeaufgaben entstehen. Die finalen
  Historien werden erst im Lauf erzeugt.

## Erwartung aus den Vertragstests

Beide Vertragstests auf Entwicklungsdaten mit Stufe `high` waren gültig (je 16/16).
Hochrechnung für 192 Aufrufe: etwa 2,46 Millionen Tokens; obere Laufzeitschätzung etwa
1,6 Stunden. Größter beobachteter Output: 24.848 Tokens. Das sind Schätzungen, keine
Zusagen.

## Nachweise

* Quellbindung `1445c361ca7c3ec2f1048da47dc84432618545ab0fec94205e470205409badbb`
* Review-Binding `review/materials-amendment3-r2-amendment5-20260930`, Siegel
  `f2a7b110f5afe7837ee3864c9d708842c2c7d9ec17c532da4984b6b4d3ee965c`. Alle 14 Material-
  und Auditdateien sind byte-gleich mit dem freigegebenen r2-Export. Die Materialfreigabe
  wurde übernommen; das ist keine neue menschliche Prüfung.
* 462 Offline-Tests und 39 HTTP-Treiberfälle bestanden. Der Mock-Lauf
  `runs/offline-amendment5-20260930` lief mit 192 Aufrufen ohne Fehler.
* Trockenprüfung der Live-Schranken nur im Speicher, ohne Reservierung.
* Details: [verification.json](verification.json).

## Einschränkungen

Die Backend- und Runner-Logik für FHGenie ist nur offline geprüft. Die Vertragstests
haben den gebundenen Transport direkt aufgerufen. Ob der Anbieter Reasoning-Stufe und
Output-Limit durchsetzt, ist nicht unabhängig bestätigt. Der letzte laufende Aufruf kann
den Token-Stopp überschreiten.

## Freigabe

Eine ausdrückliche Freigabe deckt genau diesen einmaligen Lauf mit der obigen
Konfiguration ab. Sie wird mit Wortlaut in
`review/materials-amendment3-r2-amendment5-20260930-approvals.json` eingetragen und vor
dem ersten Aufruf exklusiv reserviert.

Live-Freigabe: ausstehend.
