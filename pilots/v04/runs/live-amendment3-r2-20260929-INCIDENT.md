# Technisch abgebrochener Live-Versuch

29. September 2026. **Keine auswertbare Modellantwort und kein Forschungsergebnis.**

Milad Morad gab den einmaligen Lauf mit „ja freigegeben“ ausdrücklich frei. Die
Freigabe wurde an die geprüfte Konfiguration gebunden und vom Runner einmalig
reserviert. Der Lauf wurde gestartet und beim ersten C1-Aufruf automatisch beendet.
Es gab keine Wiederholung, keinen Ersatzlauf, keinen Kauf und keinen Credit-Reset.

## Beobachteter Fehler

Der Gateway leitete genau eine Anfrage an den festgelegten Dienst weiter. Dieser
antwortete mit HTTP 200. Der geprüfte Content-Type erfüllte jedoch nicht die
vorgesehene `text/event-stream`-Schnittstelle. Der Gateway verwarf die Antwort mit
`streaming_response_required`. Die CLI erhielt daraufhin einen lokalen Fehler.
Eine vollständige Modellantwort und Tokenangaben liegen nicht vor.

Der tatsächlich gelieferte Content-Type und der Antwortinhalt wurden von dieser
Transportversion nicht protokolliert. Deshalb ist die zugrunde liegende Ursache
noch offen. HTTP 200 belegt weder eine erfolgreiche Modellinferenz noch einen
kostenlosen Aufruf. Tokenverbrauch ist **unbekannt**, nicht null. Die Meldung
`reported_tokens: 0` bedeutet lediglich, dass kein Tokenverbrauch gemeldet wurde.

## Umfang und wissenschaftliche Interpretation

* Ein C1-Aufruf wurde versucht und ist technisch fehlgeschlagen.
* 47 weitere Vorbereitungen und alle 144 Generierungspositionen blieben blockiert.
* Es gibt keine erfolgreiche Modellantwort und keinen Vergleich zwischen A, B und C.
* Keine Aussage über Aufgabenschwierigkeit, Headroom oder Grounded Reflection ist möglich.

Der versiegelte automatische `REPORT.md` enthält sämtliche vorgesehenen
Tabellenpositionen. Seine `0/4`-Werte und `Headroom=False` beruhen auf blockierten
Sollpositionen. Sie sind keine beobachteten Modellleistungen. „Complete registered
design: True“ bezeichnet dort die vollständige Tabellenstruktur, nicht die
vollständige Ausführung. Für die Interpretation dieses Versuchs ist dieser
Incident-Bericht maßgeblich.

Die 157 Offline-Tests und die lokalen Simulatorprüfungen hatten bestanden. Sie
belegten die lokalen Transportregeln, konnten aber die Antwort des entfernten
Dienstes nicht prüfen. Die anschließende Live-Antwort offenbarte diese verbleibende
Integrationslücke. Der kontrollierte Stopp verhinderte weitere Versuche.

## Erhalt und nächster Schritt

Alle Laufdateien und die einmalige Autorisierungsreservierung bleiben unverändert.
Die vollständige Laufversiegelung wurde nach dem Abbruch erfolgreich geprüft.
Vor einem weiteren Forschungslauf muss die entfernte Antwortschnittstelle gezielt
diagnostiziert werden. Jeder weitere echte Modellaufruf oder Ersatzlauf braucht
neue ausdrückliche Freigabe. Die bestehende Freigabe wird nicht wiederverwendet.

Laufmanifest SHA-256

`c2254929afb0ca6634d633471a84eb794c08af934f809eed237034f0e15e3f5c`
