# Ergebnis des Verbindungstests v2

29. September 2026. Der separat freigegebene Versuch wurde genau einmal ausgeführt.
Der Gateway meldet eine ausgehende Modellanfrage und HTTP 200. Er brach mit
streaming_response_required vor dem Lesen des Antwortinhalts ab. Das erwartete
JSON wurde nicht empfangen. Tokenverbrauch ist unbekannt, nicht null.

Die Anfrage enthielt Authentifizierungs- und Account-Header. Das beweist weder die
Annahme der Anmeldung noch eine ausgeführte Modellberechnung. Die Antwort hatte
keine brauchbare Content-Type-Angabe. Der damalige Beobachter fasst einen fehlenden
und einen explizit leeren Header als missing zusammen. Kein Proxy war in diesem
Ausführungskontext konfiguriert. Eine Proxyursache ist nicht belegt.

Dieser Versuch liefert kein Forschungsergebnis und wird nicht wiederholt. Die
vorherige README beschreibt den Plan vor Ausführung. Ein separater v3-Entwurf prüft
eine eng begrenzte Kompatibilität für tatsächlich fehlende MIME-Header. Seine
Vorbereitung und lokale Verifikation erteilen keine Freigabe für echte Aufrufe.
