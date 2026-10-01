# Verbindungstest v3 zur separaten Freigabe

Vorbereitet und offline geprüft. Kein echter Aufruf gestartet.

Der freigegebene v2-Test erreichte mit genau einer Anfrage HTTP 200, aber keine
brauchbare Content-Type-Angabe. Der Gateway stoppte vor dem Lesen des Inhalts.
Ob der Dienst einen gültigen Stream geliefert hatte, ist daher unbekannt.
Die damalige Beobachtung unterscheidet fehlende und leere Header nicht.

Diese Version prüft ausschließlich bei vollständig fehlendem Content-Type einen
begrenzten Antwortanfang. Ein durch den bestehenden Gateway validiertes Ereignis
muss innerhalb von 64 KiB und der Zeitgrenze auftreten. Vorgeholte Bytes werden
unverändert wiedergegeben. Explizite HTML-, JSON- und leere MIME-Angaben bleiben
abgewiesen. Ein gültiger Anfang allein zählt nicht als erfolgreicher Test.

23 Offline-Tests bestehen. Auch die installierte Codex-CLI erhielt von einem
lokalen Simulator ohne MIME-Header die vollständige erwartete Testantwort.
Dabei gab es keine externen Modellaufrufe. Der Arbeitsordner war anfangs leer,
keine Werkzeuge wurden angeboten und die privaten Testmarkierungen erschienen
nicht in der Anfrage. Dies ist keine Prüfung des echten Dienstes.

Zur Freigabe steht ein Verbindungstest mit gpt-6-sol und medium reasoning, höchstens
einer ausgehenden Modellanfrage und maximal 60 Sekunden. Keine Forschungsdaten,
Wiederholungen, Käufe oder automatischer Studienstart. Der vorhandene Transport
verwendet die ChatGPT-Anmeldung und keine API-Schlüssel. Verbrauchsdaten werden
festgehalten, sofern sie zurückkommen. Eine genaue Tokenzahl ist vorab unbekannt.

Forschungsquellen und bisherige Versuche bleiben unverändert. Der Beobachter
speichert nur Kategorien und Wahrheitswerte, keine Zugangsdaten oder Headerwerte.
Für die Kompatibilitätsprüfung wird der begrenzte Streamanfang im Speicher gelesen.
Zugelassene Streams durchlaufen weiterhin die üblichen Transportprüfungen und
Protokolle. Die Proxyvermutung ist weiterhin unbestätigt.

Die Freigabe in approval.json ist leer und an den Plan gebunden. Nur nach einer
neuen ausdrücklichen Freigabe darf --execute-one-live-smoke verwendet werden.
Ohne dieses Argument prüft run_smoke.py ausschließlich Plan und Laufzeitattest.
