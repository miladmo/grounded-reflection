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

## Zweiter Check, 3. Oktober 2026

Entscheidung von Milad Morad: „ja ok, lass das so machen“. Den Lauf hat Milad Morad selbst
gestartet, im Ordner `live-dcheck-20261003-attempt2`, mit höchstens 16 Aufrufen und
446.174 Tokens. Der Lauf ist vollständig und versiegelt (Manifest
`80fee33a6f08461acfd5b1eaf78f2f8a13d14c5ef4243ebcb8c3a0e7276464b7`).

* 6 Aufrufe, 146.294 Tokens, kein unbekannter Verbrauch, kein Antwortfehler, kein
  Stopp. Alle Antworten waren gültiges JSON.
* Je Historie: D-Index, eine Runde, D-Final. Danach meldete D jeweils selbst
  `no_further_discrimination`.
* Die Abfragen lieferten jetzt Treffer:
  * erste Historie: 0, 4 und 1 Treffer;
  * zweite Historie: 23, 26 und 22 Treffer, davon 0, 5 und 22 aus Budgetgründen
    weggelassen.
* Die Rundenprompts blieben unter der Grenze je Aufruf. „any“ und leere Felder wurden
  nicht als Filter gewertet.
* D-Final zitierte je Historie 5 Datensätze.
* Inhaltlich nur beschreibend, nicht bewertet: In der zweiten Historie hat D alle
  38 Hypothesen verworfen. Das ist keine Frage von Format oder Vertrag. Nach dem Protokoll
  sind keine Strategieänderungen zulässig, daher bleibt das unverändert.

Damit sind die JSON-Gültigkeit und die Abfrageausführung von D geprüft. Als Nächstes
folgen das Einfrieren und der Hauptlauf mit eigener Freigabe.
