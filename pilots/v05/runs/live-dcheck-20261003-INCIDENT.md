# D-Technikcheck v0.5, 3. Oktober 2026: zwei Vertragsfehler gefunden

Freigabe durch Milad Morad („ja freibabe für die nächsetn schritte“). Den Lauf hat
Milad Morad selbst als eigenständigen Prozess gestartet. Der Runner hat ihn nach
4 Aufrufen selbst beendet und versiegelt (Manifest
`9d822accfa0d0c0615e937e089ab7c9ef8ab82baa6988e35d3f364aeb7d7c263`).

## Verlauf

* 4 Aufrufe, 53.826 gemeldete Tokens, kein unbekannter Verbrauch, kein Antwortfehler.
  Alle vier Antworten waren gültiges JSON nach dem Vertrag.
* Historie `history-ac653f6917a0`: D-Index, eine Runde, D-Final, alle abgeschlossen.
  Alle drei Abfragen lieferten jedoch **0 Treffer**, und D-Final zitierte 0 Datensätze.
* Historie `history-d1f86f08d7a3`: Der D-Index wurde abgeschlossen. Danach überschritt der
  Prompt für Runde 1 die Grenze je Aufruf um 37 Zeichen. Die Prüfung im Code griff vor
  dem Aufruf, es wurde also kein Aufruf verschwendet. Der Runner stoppte
  (`halt_reason: BudgetExceeded: D round prompt exceeds the call budget`).
* Es gab keine Generierung und keine Bewertung.

## Ursachen (beide im Code, nicht im Modell)

1. **Platzhalter.** Der D-Prompt sagt, dass leere Felder und „any“ nicht filtern. Der Code
   behandelte bei `actor` und `reviewed_field` aber nur leere Felder so. D schrieb
   `actor: "any"` und suchte damit nach einer Person namens „any“. Dadurch blieben alle
   Abfragen der ersten Historie ohne Treffer.
2. **Budget der Abfrageergebnisse.** Die Ergebnisse durften den Platz bis zur Grenze mit
   Datensätzen füllen. Der Code rechnete die Hülle jedes Ergebnisses (Wiederholung der
   Abfrage, Zähler, Trennzeichen) nicht mit ein. Bei 61 Treffern waren das 1.665 Zeichen,
   mehr als die Sicherheitsreserve von 1.500.

## Korrektur (Format und Vertrag, nach Protokoll zulässig)

* `dquery.matches`: Bei `actor` und `reviewed_field` filtern jetzt weder leere Felder
  noch „any“, so wie es der Prompt zusagt.
* `dquery.execute`: Die Hüllen aller Ergebnisse werden reserviert, bevor Datensätze
  hinzukommen.
* Prompts, Strategie, Grenzen und Ablauf bleiben unverändert.
* Zwei Regressionstests sind neu. Ohne die Korrektur schlagen beide fehl.
* Mit den gespeicherten D-Index-Antworten offline nachgerechnet: Die erste Historie
  findet jetzt 15, 2 und 3 Treffer statt 0. Der Rundenprompt der zweiten Historie liegt
  2.118 Zeichen unter der Grenze.

## Bewertung

Der Technikcheck hat seinen Zweck erfüllt. Die Abfrageausführung mit echten Treffern und
eine Runde nach Abfrage mit Ergebnissen sind aber noch nicht live geprüft. Für einen
zweiten Check braucht es eine eigene, hier dokumentierte Entscheidung und eine neue
Freigabe. Vorschlag: höchstens die verbleibenden 16 der 20 vorgesehenen D-Aufrufe.
