# FHGenie-Vertragstest 2: Stufe `high`, Output-Limit 32.768

Vorbereitet am 30. September 2026 nach Amendment 5 (Option B2). **Nicht ausgeführt.**
Regeln: [`docs/pilot-v04-fhgenie-contract-test.md`](../../../../../docs/pilot-v04-fhgenie-contract-test.md),
Abschnitt „Vertragstest 2“. Vorgänger: [`contract-test-high-20260930`](../contract-test-high-20260930/README.md)
(bestanden bei 16.384).

Einziger Unterschied zu Test 1 ist das Output-Limit von 32.768. Material, Reihenfolge,
Stufe, Entscheidungsregel und Hochrechnung sind gleich. Token-Stopp des Tests: 600.000.

Plan-SHA-256: `c0fd147d987f5e3115a087c7b55c76e97e7d5a13296a535df857433a03d08abe`

## Befehle

```powershell
$py = "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$pw = "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe"
$env:PYTHONPATH = 'src;pilots/v03;pilots/v04'
& $py -B -m unittest discover -s pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930 -p "test_*.py"
& $py -B pilots/v04/diagnostics/fhgenie/contract-test-high-32k-20260930/contract_test.py verify --pwsh $pw
```

`execute --once` verlangt eine `approval.json` mit `approved: true`,
`reviewer: "Milad Morad"`, `date`, der tatsächlichen Antwort in `response`,
`reasoning_effort: "high"`, `max_output_tokens: 32768`, `planned_calls: 16` und dem obigen
`plan_sha256`. Die Freigabe wird vor dem ersten Aufruf exklusiv in `attempt.json`
reserviert und kann nur einmal verwendet werden.
