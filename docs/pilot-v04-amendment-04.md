# Pilot v0.4, Amendment 4: Modellwechsel

Freigegeben von Milad Morad am 30. September 2026. Die Freigabe autorisiert keinen
Modellaufruf, weder den Vertragstest noch den finalen Lauf. Materialien, Prompts und
Seeds bleiben unverändert.

## Änderung

Das Protokoll legt fest: „All arms use `gpt-6-sol` with medium reasoning through the
existing transport.“ Dieser Satz wird ersetzt durch:

> Alle Arme (A, B, C) nutzen `deepseek-ai/DeepSeek-V4-Flash-0731` über den
> FHGenie-On-Prem-Endpunkt `<FHGENIE_ENDPOINT>` mit
> der im Vertragstest festgelegten Reasoning-Stufe. Temperature und top_p sind 1,
> das Output-Limit beträgt 16.384 Tokens je Aufruf, der Timeout 420 Sekunden.

Alle übrigen Festlegungen bleiben unverändert: r2-Materialien, öffentliche
Konventionen, H14-Hypothesenklasse, Orakel, Prompts, A/B/C-Arme, 192 geplante
Aufrufe, Grenze von 200 Versuchen, Token-Stopp bei 6.000.000 gemeldeten Tokens,
Final-Seeds 44361/44362/44363, Auswertung, Fehlertaxonomie und Headroom-Kriterium.
D bleibt ausgeschlossen.

## Begründung

1. Der einmal freigegebene gpt-6-sol-Lauf brach beim ersten C1-Aufruf technisch ab
   (siehe `pilots/v04/runs/live-amendment3-r2-20260929-INCIDENT.md`). Die Freigabe ist
   verbraucht. Die Ursache der Streaming-Abweichung ist nicht geklärt, und der
   Codex-Transport hängt von einer ChatGPT-Anmeldung und einer bestimmten CLI-Version ab.
2. FHGenie ist ein institutionell bereitgestellter On-Prem-Zugang mit direkter
   API-Schnittstelle. Der Transport sendet nur die expliziten Nachrichten, ohne Tools,
   Dateien oder Sitzungskontext. Die Datengrenze ist damit einfacher prüfbar als beim
   CLI-Transport.
3. Drei einzeln freigegebene Verbindungsproben (insgesamt 173 gemeldete Tokens)
   bestätigten Erreichbarkeit, Modellkennung und Tokenmeldung. Die dritte Probe ohne
   serverseitiges `response_format` lieferte gültiges JSON. Das belegt noch keine
   zuverlässige Einhaltung der größeren Studienverträge; dazu dient der separate
   Vertragstest.
4. Die Wahl beruht auf Verfügbarkeit und Transporttauglichkeit, nicht auf gemessener
   Leistung in dieser Aufgabe. Eine Rangfolge der verfügbaren FHGenie-Modelle wurde
   nicht erhoben. Der Wechsel ist keine Reaktion auf Ergebnisse, denn es liegen keine
   Modellergebnisse für v0.4 vor.

## Reasoning-Stufen

Laut offizieller Modellkarte, wie in `pilots/v04/diagnostics/fhgenie/probe-v1-20260929/README.md`
dokumentiert, unterstützt DeepSeek V4 Flash 0731 die Stufen **low**, **high** und **max**.
Eine Stufe `medium` gibt es nicht. Eine direkte Entsprechung zur gpt-6-sol-Stufe
`medium` besteht daher nicht und wird nicht behauptet.

Ob FHGenie den Parameter `reasoning_effort` tatsächlich anwendet, ist nicht unabhängig
bestätigt. Beobachtet wurde nur, dass bei `low` ein separater Reasoning-Kanal vorhanden
war. Der Vertragstest protokolliert deshalb je Stufe die gemeldeten Reasoning-Tokens,
soweit der Server sie meldet.

Festlegung: Der Vertragstest beginnt auf Stufe **`high`**. Das hat Milad Morad bei der
Freigabe festgelegt, abweichend vom Entwurf, der mit `low` beginnen wollte. Die
Festlegung erfolgte vor jedem Modellaufruf auf Studienmaterial und ohne Kenntnis von
Ergebnissen. `low` wird nicht getestet. Eine Eskalation ist nur noch auf `max` möglich
und folgt ausschließlich der vorab festgelegten Entscheidungsregel des Vertragstests.
Die bestandene Stufe wird vor dem finalen Lauf in `run-config.json` eingetragen und
danach nicht mehr geändert.

Umsetzung am 30. September 2026: Transport (`reflectai_v04/fhgenie_transport.py`) und
HTTP-Treiber (`transport/fhgenie-request.ps1`) akzeptieren jetzt genau die dokumentierten
Stufen `low`, `high` und `max`. Jede andere Angabe wird weiterhin vor Schlüsselzugriff
und HTTP abgelehnt. `reflectai_v04/config.py` erlaubt für FHGenie weiterhin nur `low`.
Das wird erst nach dem Vertragstest auf die bestandene Stufe gesetzt, zusammen mit neuer
Quellbindung, neuem Review-Export und neuer Verifikation.

## Folgen für die Interpretation

1. **Kein Vergleich mit v0.3.** Die Deckeneffekte aus v0.3 Kalibrierungsrunde 2 wurden
   mit gpt-6-sol (medium) beobachtet. Sie sind keine Ausgangslage für v0.4-Ergebnisse
   mit DeepSeek. Unterschiede zwischen v0.3 und v0.4 dürfen weder den neuen Materialien
   noch dem Modell zugeschrieben werden, da beides gleichzeitig wechselt. Der Bericht
   stellt keine Tabelle oder Aussage auf, die v0.3- und v0.4-Werte nebeneinander als
   Veränderung deutet.
2. **Die Schwierigkeitskarte gilt nur für dieses Modell.** Sie beschreibt
   DeepSeek-V4-Flash-0731 in der gemeldeten FHGenie-Bereitstellung
   (Server-Fingerprint, soweit gemeldet), mit der festgelegten Reasoning-Stufe, diesen
   Prompts und diesem Transport. Sie ist keine Aussage über gpt-6-sol, andere Modelle
   oder Modelle allgemein. Der Server-Fingerprint wird je Aufruf protokolliert; ein
   Wechsel während des Laufs wird berichtet.
3. **Fehler können Modellkapazität widerspiegeln.** Ein Flash-Modell kann an der
   Aufgabenlänge, am Vertragsformat oder an der Inferenz scheitern, wo ein stärkeres
   Modell nicht scheitern würde. Ein bestandenes Headroom-Kriterium zeigt dann
   möglicherweise eine Kapazitätsgrenze dieses Modells und nicht eine
   modellübergreifende Schwierigkeit der Evidenzbedingungen. Der Bericht nennt diese
   Alternative ausdrücklich bei jedem Befund zu Headroom und Fehlerursachen.
   Technische Fehler (Format, Abbruch an der Output-Grenze, Timeout) bleiben nach der
   bestehenden Taxonomie getrennt und zählen nicht als Inhaltsfehler.
4. **Keine Kostenaussage.** Ein funktionierender Schlüssel belegt nicht, dass die
   Nutzung kostenlos ist. Tokenprojektionen bleiben Token, keine Preise.
5. **Transportänderung.** Das Antwortschema steht in einer Systemnachricht statt im
   früheren Codex-Anfragerahmen. Das ist dokumentiert und keine wissenschaftliche
   Gleichwertigkeit mit dem alten Transport.

## Festlegung für v0.5

Eine etwaige v0.5-Studie nutzt dasselbe Modell `deepseek-ai/DeepSeek-V4-Flash-0731`
über FHGenie mit derselben Reasoning-Stufe, denselben Sampling-Parametern und demselben
Output-Limit wie der finale v0.4-Lauf. Damit bleibt der Vergleich zwischen der
v0.4-Karte und einem in v0.5 geprüften Mechanismus nicht durch einen Modellwechsel
verzerrt.

Ist das Modell für v0.5 nicht mehr verfügbar oder meldet der Server eine andere
Modellkennung, wird v0.5 nicht stillschweigend mit einem anderen Modell ausgeführt.
Ein Wechsel braucht dann ein eigenes Amendment, das die fehlende Vergleichbarkeit
mit v0.4 benennt. Ein geänderter Server-Fingerprint bei gleicher Modellkennung wird
berichtet und als Einschränkung der Vergleichbarkeit dokumentiert.

## Was unverändert bleibt

Keine Wiederholungen, keine Ersatzläufe, keine Wiederaufnahme, keine Käufe. Frühere
Läufe, Freigaben, Materialien und Quellsnapshots bleiben unverändert. Die verbrauchten
Freigaben (gpt-6-sol-Lauf, drei FHGenie-Proben) gelten nicht für diese Konfiguration.

Bei Freigabe dieses Amendments wird es neben dem Protokoll abgelegt und in die
Quellbindung aufgenommen. Der Statusabschnitt des Protokolls erhält einen Verweis.
Diese Änderungen ändern den Quellhash; vor dem finalen Lauf sind deshalb neue
Offline-Tests und eine neue Verifikation nötig.

## Reihenfolge der Freigaben

1. Freigabe dieses Amendments (Modellwechsel und Interpretation).
2. Freigabe des Vertragstests (`pilot-v04-fhgenie-contract-test.md`) und seiner
   Umsetzung als eigener Diagnose-Harness.
3. Ausführung des Vertragstests, nur nach ausdrücklicher Freigabe.
4. Separate Live-Freigabe des finalen Laufs mit der dann festgelegten Reasoning-Stufe
   und neuer Quellbindung.

## Freigabevermerk

Amendment 4: freigegeben.

Reviewer: Milad Morad
Datum: 30. September 2026
Tatsächliche Antwort: „Amendment 4 freigegeben, Harness für den Vertragstest umsetzen,
aber reasoning auf stufe high setzen“

Ausführung des Vertragstests: ausstehend. Live-Freigabe des finalen Laufs: ausstehend.
