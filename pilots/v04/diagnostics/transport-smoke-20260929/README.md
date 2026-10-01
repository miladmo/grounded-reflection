# Ein einzelner Verbindungstest

Stand 29. September 2026. Vorbereitet, **noch nicht zur Live-Ausführung freigegeben**.

Der erste Forschungsaufruf wurde bei HTTP 200 wegen eines unerwarteten Content-Type abgebrochen.
Der damalige Gateway speicherte den tatsächlichen Antworttyp nicht. Er verwendete zudem
`http.client.HTTPSConnection` direkt und berücksichtigte den in der Ausführungsumgebung
vorhandenen HTTP-Proxy nicht. Für chatgpt.com besteht keine NO_PROXY-Ausnahme. Ob diese
Abweichung den Fehler verursacht hat, ist noch nicht nachgewiesen.

Der vorbereitete Test nutzt die vorhandene Proxykonfiguration mit einem HTTPS-CONNECT-Tunnel.
Ziel, TLS-Prüfung, Ein-Aufruf-Sperre, Werkzeugverbote und Streaming-Prüfung bleiben erhalten.
Bei einem nicht unterstützten Proxy scheitert der Test ohne direkte Ausweichverbindung.
Es werden keine Proxy- oder Anmeldeeinstellungen geändert. Die Unterstützung alternativer
Provider mit vorhandener ChatGPT-Anmeldung ist in der [offiziellen OpenAI-Dokumentation](https://learn.chatgpt.com/docs/auth#alternative-model-providers) beschrieben.

Der Test verwendet gpt-6-sol mit medium reasoning und nur die Anweisung, ein JSON-Objekt
mit status gleich ok zurückzugeben. Kein Datensatz, keine Fallhistorie und keine
Evaluatordatei wird geladen. Es gibt höchstens einen ausgehenden Modellrequest,
60 Sekunden Timeout, keine Wiederholung und keinen automatischen Start der Studie.
Die CLI fügt eigenen Kontext hinzu, weshalb keine exakte Tokenprognose vorliegt.
Keine Käufe, Credit-Resets oder API-Schlüssel werden verwendet.

Erfasst werden nur Kategorien und Wahrheitswerte zu Antworttyp, Kompression,
HTTP-Version, Proxyroute und Vorhandensein von Authentifizierungsheadern. Keine
Headerwerte, Tokens oder Cookies werden gespeichert. Der Beobachter liest keine
Antwortinhalte. Der reguläre Transport bewahrt seine üblichen Testprompt- und
Antwortartefakte auf, falls überhaupt eine gültige Modellantwort zustande kommt.

11 gezielte Offline-Tests bestanden, ohne Sockets, CLI oder Modelle. Der eigentliche
Live-Verbindungstest bleibt separat gesperrt. Die ursprüngliche Studie, ihre
Quellbindung, der abgebrochene Lauf und seine Einmalfreigabe bleiben unangetastet.

Nur Plan und Hashes prüfen, ohne Netzwerkaufruf

```powershell
python -B run_smoke.py
```

Erst nach dokumentierter ausdrücklicher Zustimmung

```powershell
python -B run_smoke.py --execute-one-live-smoke
```

Die Freigabe muss an plan.json gebunden sein. Die Reservierung ist exklusiv und
lässt keine Wiederaufnahme zu. Ein positives Ergebnis bestätigt nur die technische
Verbindung; ein neuer Forschungslauf wird damit weder genehmigt noch gestartet.
