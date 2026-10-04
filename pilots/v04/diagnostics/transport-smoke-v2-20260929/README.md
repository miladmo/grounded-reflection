# Verbindungstest v2 zur separaten Freigabe

**Vorbereitet, kein echter Aufruf gestartet.**

Der erste Diagnoseversuch scheiterte lokal an einem Adapterfehler, bevor irgendeine
Anfrage zum Modelldienst gesendet wurde. Dieser Fehler ist behoben. 15 Offline-Tests
bestehen, einschließlich einer Prüfung mit der echten HTTPS-Klasse ohne Verbindung.
Eine zusätzliche lokale CLI-Probe mit aktivem Laufzeitattest lieferte die erwartete
Testantwort. Dabei wurde ausschließlich ein lokaler Simulator angesprochen.

Die Proxyvermutung bleibt unbestätigt. Der Adapter respektiert die Einstellungen
des tatsächlichen Ausführungskontexts, in dem beim ersten Diagnoseversuch kein
Proxy vorhanden war. Es werden keine Netzwerkeinstellungen geändert.

Zur Freigabe steht genau ein erneuter Verbindungstest mit gpt-6-sol, medium reasoning,
maximal 60 Sekunden und dem kurzen JSON-Testprompt aus plan.json. Keine Forschungsdaten,
keine Wiederholungen, keine Käufe und kein automatischer Studienstart. CLI-Kontext
verursacht zusätzliche Eingabetokens; eine genaue Tokenzahl ist vorher nicht bekannt.

Der Beobachter hält nur Kategorien und Wahrheitswerte zu MIME-Typ, Kompression,
HTTP-Version, Netzwerkroute und vorhandenen Authentifizierungsheadern fest. Er liest
keine Antwortinhalte und speichert keine Headerwerte, Zugangsdaten oder Cookies.
Die unveränderten Werkzeug- und Streaming-Prüfungen sowie die Sperre gegen einen
zweiten ausgehenden Modellrequest bleiben aktiv. Fehlerantworten werden nicht
blind als Modellantwort akzeptiert.

Die Freigabe in approval.json ist derzeit leer und an den Plan-Hash gebunden.
Die Ausführung reserviert sie einmalig. Eine Freigabe der Studie ist damit nicht verbunden.

Prüfen ohne Modellaufruf

```powershell
python -B run_smoke.py
```

Nur nach neuer ausdrücklicher Freigabe

```powershell
python -B run_smoke.py --execute-one-live-smoke
```
