# FHGenie-Vertragstest, Stufe `high`

Vorbereitet am 30. September 2026. **Nicht ausgeführt, keine Freigabe zur Ausführung.**
Plan und Regeln: [`docs/pilot-v04-fhgenie-contract-test.md`](../../../../../docs/pilot-v04-fhgenie-contract-test.md).
Grundlage: [Amendment 4](../../../../../docs/pilot-v04-amendment-04.md).

16 Aufrufe auf Entwicklungsmaterial (Seeds 44321/44322/44323) mit
`deepseek-ai/DeepSeek-V4-Flash-0731`, Reasoning `high`, Output-Limit 16.384, Timeout
420 s, Token-Stopp 600.000. Gemessen werden nur technische Größen. Kein Evaluator,
keine Scores, kein Retry, keine Reparatur, kein Ersatzaufruf.

Plan-SHA-256: `3ee95edd8d63481ed32eaebb5a16c186b377bd306429537515606866eea920b6`

## Dateien

* `contract_test.py`: Harness mit den Befehlen `plan`, `verify` und `execute --once`
* `test_contract_test.py`: 18 Offline-Tests mit gefälschtem Transport
* `plan.json`: fester Plan mit Material-, Prompt-, Quell- und Laufzeit-Hashes
* `offline-verification.json`: Nachweis der Offline-Prüfung

`approval.json`, `attempt.json` und `run/` entstehen erst nach einer tatsächlichen
Freigabe.

## Befehle

Aus dem Repository-Wurzelverzeichnis mit der gebundenen Laufzeit (Python 3.12.14,
pydantic 2.13.5) und PowerShell 7:

```powershell
$py = "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$pw = "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe"
$env:PYTHONPATH = 'src;pilots/v03;pilots/v04'
& $py -B -m unittest discover -s pilots/v04/diagnostics/fhgenie/contract-test-high-20260930 -p "test_*.py"
& $py -B pilots/v04/diagnostics/fhgenie/contract-test-high-20260930/contract_test.py verify --pwsh $pw
```

`verify` berechnet den Plan neu und vergleicht ihn Byte für Byte, ohne Modellaufruf.
Jede Änderung an Quellen der v0.4-Bindung, am Harness, am Transport, am Treiber, an
der Laufzeit oder am Material führt zu einer Abweichung. Dann ist ein neuer Plan und
eine neue Freigabe nötig.

## Freigabe und Ausführung

`execute --once` startet nur, wenn `approval.json` genau diese Felder mit passenden
Werten enthält: `approved: true`, `reviewer: "Milad Morad"`, `date`, die tatsächliche
Antwort in `response`, `reasoning_effort: "high"`, `planned_calls: 16` und den obigen
`plan_sha256`. Vor dem ersten Aufruf wird `attempt.json` exklusiv angelegt. Eine
Freigabe kann dadurch nur einmal verwendet werden, auch nach einem Abbruch.

Der Transport liest den FHGenie-Schlüssel erst beim echten Aufruf aus der
DPAPI-verschlüsselten Datei. Die Offline-Tests berühren weder Schlüssel noch Netzwerk.
