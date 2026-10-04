# Diagnoseversuch v1 lokal abgebrochen

Der gesondert freigegebene Verbindungstest wurde einmal gestartet. Der Fehler trat
vor dem Verbindungsaufbau zum entfernten Dienst auf. Gateway-Metadaten zeigen null
ausgehende Modellanfragen. Es gab keine Wiederholung.

Ursache war ein Implementierungsfehler im Diagnoseadapter. Das globale Ersetzen
von http.client.HTTPSConnection kollidierte mit einem internen super-Aufruf der
Standardbibliothek. Der Fehler wurde anschließend durch reine Konstruktion des
Objekts ohne Netzwerkzugriff reproduziert. Die Korrektur in Diagnoseversion v2
ersetzt nur den Verweis im Gateway und lässt die Standardbibliothek unverändert.

Die vermutete Proxyursache ist nicht bestätigt. Proxyvariablen waren im zuvor
untersuchten eingeschränkten Tool-Kontext vorhanden, im tatsächlichen freigegebenen
Ausführungskontext dagegen nicht. Aus dieser Kontextdifferenz lässt sich die
ursprüngliche HTTP-200-Antwort nicht erklären.

Die ursprüngliche Freigabe, Reservierung und Fehlerdateien bleiben erhalten.
Version v2 ist lokal getestet, aber noch nicht für einen echten Aufruf freigegeben.
