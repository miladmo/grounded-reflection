# Regel für Ersatzläufe nach technischem Abbruch

Grundsatz freigegeben von Milad Morad am 30. September 2026. Tatsächliche Antwort auf
den Vorschlag: „macht sinn oder, wenn ja mach es“.

**Gilt nur für künftige Läufe, ab v0.5.** Der laufende v0.4-Lauf
`pilots/v04/runs/live-fhgenie-high-20260930` bleibt an seine gebundenen Quellen und die
bisherige Protokollregel gebunden. Bei einem Abbruch dieses Laufs gilt nur die bisherige
Regel: Neustart oder Ersatz nur nach einer ausdrücklichen, neben den unvollständigen
Ergebnissen dokumentierten Entscheidung. Diese Datei gehört nicht zur v0.4-Quellbindung.
Sie wird in das v0.5-Protokoll übernommen und dort gebunden, bevor sie wirkt.

## Regel

Ein Ersatzlauf ist ohne erneute inhaltliche Abwägung zulässig, wenn **alle** folgenden
Bedingungen erfüllt sind.

1. Der Lauf stoppte, **bevor** eine einzige Modellantwort vertragsgültig abgeschlossen
   wurde. Es liegt also keine verwertbare Modellausgabe vor, weder Vorbereitung noch
   Aufgabe.
2. Die Ursache ist nachweislich technisch und unabhängig vom Modellinhalt, zum Beispiel
   Endpunkt nicht erreichbar, Authentifizierung, Schnittstellenformat, lokale Laufzeit,
   PowerShell oder Quellprüfung. Der Nachweis stammt aus den gespeicherten
   Transportmetadaten, nicht aus einer Vermutung.
3. Der Ersatzlauf verwendet unverändert dieselben Materialien, Seeds, Prompts, dasselbe
   Modell und dieselben Parameter. Nur die technische Ursache darf behoben werden. Diese
   Behebung wird offline getestet, dokumentiert und neu gebunden.
4. Der abgebrochene Lauf bleibt vollständig erhalten und wird im Bericht genannt.
5. Höchstens **ein** Ersatzlauf je Studie nach dieser Regel.
6. Der Ersatzlauf braucht trotzdem eine eigene ausdrückliche Live-Freigabe. Die Regel
   ersetzt nur die inhaltliche Begründung, nicht die Freigabe.

## Ausdrücklich ausgeschlossen

* Ersatz, sobald mindestens eine gültige Modellantwort vorliegt, gleich welchen Inhalts.
  Dann gilt der Lauf als inhaltlich begonnen und wird unvollständig berichtet.
* Ersatz wegen Antwortfehlern innerhalb der tolerierten Grenze, wegen schlechter oder
  unerwarteter Ergebnisse oder wegen Erreichen des Token-Stopps.
* Änderungen an Materialien, Prompts, Modell, Reasoning-Stufe, Limits oder Seeds im
  Ersatzlauf.

## Begründung

Der Ausfall vor der ersten gültigen Antwort enthält keine Information über die
untersuchte Frage. Ein Ersatz kann deshalb keine Auswahl nach Ergebnis bewirken. Die
Grenze „erste gültige Antwort“ ist objektiv prüfbar und nicht nachträglich verschiebbar.
Der v0.4-Vorfall vom 29. September 2026 (Abbruch beim ersten C1-Aufruf wegen der
Streaming-Schnittstelle) wäre unter diese Regel gefallen.
