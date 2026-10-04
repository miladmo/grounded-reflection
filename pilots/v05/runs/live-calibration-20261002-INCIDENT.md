# Abgebrochene Kalibrierung v0.5, 2. Oktober 2026

**Keine Auswertung, kein Kalibrierungsergebnis.** Die Kalibrierung wurde von Milad Morad
freigegeben („ja, kosten ok, live freigabe“) und um 19:40 UTC gestartet. Die Freigabe
wurde einmalig reserviert.

## Ursache

Der Lauf wurde als Hintergrundprozess der Arbeitssitzung von Claude Code gestartet.
Die Sitzung beendete den Prozess nach rund 27 Minuten wegen ihrer Zeitgrenze für
Hintergrundaufgaben. Weder der Runner noch FHGenie hatten einen Fehler gemeldet. Die
Ursache liegt also in der Startart, nicht im Studiencode, nicht im Modell und nicht in
den Daten. Das ist ein Fehler im Vorgehen: Ein Lauf von etwa 1,5 Stunden hätte nicht so
gestartet werden dürfen.

## Stand beim Abbruch

* 13 Aufrufe gültig abgeschlossen, alle C-Vorbereitungen (10 C1-Abschnitte, 3 C2).
  Gemeldeter Verbrauch: 391.653 Tokens.
* Ein 14. Aufruf (C1, Historie `history-1c5de8b77ead`) war unterwegs. Anfrage und
  Transportstart sind protokolliert, ein Ergebnis fehlt. Ob die Anfrage den Server
  erreichte, ist unbekannt. Ihr Verbrauch ist **unbekannt** und höchstens etwa
  57.000 Tokens.
* Die Vorbereitung war nicht abgeschlossen und nicht versiegelt. Es wurden keine
  Folgeaufgaben erzeugt, keine Generierung ausgeführt und nichts bewertet. Die
  Vorbereitungsinhalte wurden nicht angesehen.
* Kein Retry, kein Ersatzaufruf, keine Wiederaufnahme. Danach lief kein Prozess mehr.

Der Lauf-Ordner ist unverändert erhalten. Er ist als unvollständig markiert
(`INCOMPLETE.json`) und versiegelt (Manifest
`5d89570b793c2f3bf6ecca335c5aae242fc72f7f9f61347a1be1a85419a06c0e`).

## Einordnung und nächste Entscheidung

Die Freigabe ist verbraucht. Die Ersatzlauf-Regel deckt den Fall nicht ab, denn es
liegen bereits gültige Antworten vor. Ein neuer Kalibrierungsversuch braucht deshalb
eine ausdrückliche, hier dokumentierte Entscheidung und eine neue Freigabe. Der Zweck
der Regel, keine Auswahl nach Ergebnissen, ist nicht berührt: Es gibt keine Bewertung,
und die Vorbereitungen wurden nicht angesehen.

Ein neuer Versuch muss unabhängig von Sitzungsgrenzen laufen, als eigenständiger Prozess
mit Protokolldatei. Er darf erst nach Abschluss des Laufs ausgewertet werden.

Entscheidung von Milad Morad, 2. Oktober 2026: „ja, neuer Versuch freigegeben“. Neuer Versuch mit unveränderter Konfiguration und Quellbindung im Ordner `live-calibration-20261002-attempt2`, gestartet als eigenständiger Prozess mit Protokolldatei.
