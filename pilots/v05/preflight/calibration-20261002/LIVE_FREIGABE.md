# Live-Freigabe: Kalibrierung Pilot v0.5

Vorbereitet am 2. Oktober 2026. **Noch nicht freigegeben, nicht gestartet.** Die Freigabe
folgt nach der Kostenklärung mit FHGenie.

## Umfang

Kalibrierung nach Protokoll, Schritt 5: Arme **A, B und C** auf den Entwicklungsseeds,
8 Historien (je Einstellung eine Transfer- und eine nicht identifizierbare Historie,
Richtungen abwechselnd), je Historie 4 Aufgaben, also 32 Aufgaben je Arm. Arm D läuft
nicht mit und sieht keine v0.5-Daten. Anschließend wird das vorab festgelegte
Headroom-Kriterium angewandt: Kein Headroom liegt nur vor, wenn der bessere von B und C
in allen vier Einstellungen alle schwierigen Kalibrierungsdiagnosen löst. Nur dann ist
das einzige Amendment möglich.

## Konfiguration

| Einstellung | Wert |
| --- | --- |
| Modell | `deepseek-ai/DeepSeek-V4-Flash-0731` über FHGenie (Amendment 4) |
| Endpoint | lokal konfiguriert, per SHA-256 geprüft, nicht im Repository |
| Reasoning | `high` |
| Output-Limit je Aufruf | 32.768 Tokens |
| Eingabebudget je Aufruf | 24.000 Tokens |
| Vorbereitungsdeckel | 300.000 Tokens je Historie und Arm, Generierung außerhalb reserviert |
| Temperature / top_p | 1 / 1 |
| Timeout | 420 Sekunden je Aufruf |
| Seeds Historien / Folgeaufgaben / Reihenfolge | 45021 / 45022 / 45023 (Entwicklung) |
| Harte Obergrenze | 170 Aufrufe |
| Token-Stopp | 3.000.000 gemeldete Tokens, zwischen Aufrufen geprüft |
| Tolerierte Antwortfehler | 17; der 18. beendet die weitere Planung |
| PowerShell 7 | `%USERPROFILE%\…\pwsh.exe`, SHA-256 `362a356c…0ad139` |

Konfigurations-SHA-256: `692239b0c229c1a82b87439c59f65e290166e284aa560cfebd975a714faa533b`
([run-config.json](run-config.json)).

Quellbindung: `f94329843eeff3318c9a8d85a4b805867c1bef7c8e487dd36a5a831af82b3f50`.

## Erwartung

Etwa 130 Aufrufe (Mock: 124; echte C-Abschnitte können einige mehr ergeben), etwa
2,0 Millionen Tokens, etwa 1,5 Stunden Laufzeit. Das sind Schätzungen aus v0.4, keine
Zusagen.

## Regeln

* Kein Retry, kein Ersatzlauf, keine Wiederaufnahme, keine Käufe.
* Vorbereitungen werden versiegelt, bevor die Folgeaufgaben entstehen.
* Einzelne unbrauchbare Antworten nach intaktem Austausch zählen als technischer Fehler
  im Nenner. Abhängige C-Aufgaben sind dann blockiert. Sofortiger Stopp bei
  unbekanntem Verbrauch, falscher Modellkennung, Tool-Aufruf, HTTP-, Timeout- oder
  Transportfehler und beim Token-Stopp.
* Primärergebnis: die Entscheidung aus den erzeugten Feldern, für alle Arme gleich.
* Die Ersatzlauf-Regel (`docs/pilot-replacement-run-rule.md`) gilt: Ein Ersatzlauf ist
  nur zulässig, wenn der Lauf vor der ersten gültigen Antwort aus nachweislich
  technischen Gründen stoppt, und braucht eine eigene Freigabe.

## Nachweise

* Materialprüfung r3 freigegeben (`review/materials-v05-r3-20261002`).
* D-Prompts eingefroren (`prompts/FROZEN.json`).
* 503 Offline-Tests und 44 HTTP-Treiberfälle bestanden.
* Mock-Kalibrierung vollständig mit 124 Aufrufen
  (`runs/offline-calibration-20261002`, nicht im Repository).
* Details: [verification.json](verification.json).

## Freigabe

Eine ausdrückliche Freigabe deckt genau diesen einmaligen Kalibrierungslauf mit der
obigen Konfiguration und Quellbindung ab. Sie wird als `approval.json` mit Phase,
Konfigurations- und Quell-Hash sowie deinem Wortlaut angelegt und vor dem ersten Aufruf
exklusiv reserviert.

Live-Freigabe: ausstehend.
