# Kontrolliert gestoppte Kalibrierung v0.5, Versuch 2, 2. Oktober 2026

**Keine Auswertung, kein Kalibrierungsergebnis.** Versuch 2 wurde von Milad Morad
freigegeben („ja, neuer Versuch freigegeben“) und lief als eigenständiger Prozess ab
20:25 UTC. Der Runner beendete den Lauf nach 18 Aufrufen selbst und versiegelte ihn.

## Verlauf

* 16 Aufrufe gültig, alle C-Vorbereitungen. Gemeldeter Verbrauch: 499.091 Tokens.
* Ein **Antwortfehler** (toleriert nach Amendment 5): Der C1-Abschnitt
  `history-467b1ac3560b-C1-01` lieferte `Scope.match` nicht im vereinbarten Listenformat.
  Damit war die C-Vorbereitung dieser Historie blockiert; der Lauf ging weiter.
* **Stopp:** Der C1-Abschnitt `history-ac653f6917a0-C1-00` überschritt das Zeitlimit von
  420 Sekunden. Ohne Antwort ist der Verbrauch unbekannt. Nach der Regel „unbekannter
  Verbrauch stoppt“ beendete der Runner den Lauf (`halt_reason: unknown_token_usage`).
  Der unbekannte Verbrauch beträgt höchstens etwa 57.000 Tokens.
* Es gab keine Generierung und keine Bewertung. Die Vorbereitungen wurden nicht
  angesehen. Kein Retry, kein Ersatzaufruf.

## Ursache

Der Durchsatz von FHGenie schwankte in beiden Versuchen stark, zwischen etwa 36 und 221
Output-Tokens je Sekunde. Bei dem von Amendment 5 festgelegten Output-Limit von 32.768
Tokens dauert ein vollständiger Aufruf bei langsamem Server über 420 Sekunden; bei
36 Tokens/s wären es etwa 15 Minuten. Zeitlimit und Output-Limit sind damit nicht
aufeinander abgestimmt. In den Vertragstests war der Server schneller (längster Aufruf
135 Sekunden), deshalb fiel das dort nicht auf.

## Stand beider Versuche

| Versuch | Gültige Aufrufe | Gemeldete Tokens | Unbekannt (höchstens) | Ergebnis |
| --- | ---: | ---: | ---: | --- |
| 1 | 13 | 391.653 | etwa 57.000 | durch die Sitzung abgebrochen |
| 2 | 16 | 499.091 | etwa 57.000 | Zeitlimit, kontrollierter Stopp |

Beide Lauf-Ordner sind versiegelt und bleiben unverändert erhalten.

Entscheidung von Milad Morad, 3. Oktober 2026: „A jetzt, und neue Live-Freigabe“. Das Zeitlimit wird als technische Korrektur auf 1.200 Sekunden angehoben; alle anderen Regeln bleiben. Versuch 3 läuft im Ordner `live-calibration-20261003-attempt3` als eigenständiger Prozess.
