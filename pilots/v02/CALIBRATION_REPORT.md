# Synthetic pilot v0.2 calibration

28 September 2026. Both scientific calibration rounds used `gpt-6-sol` with `medium` reasoning through the authenticated Codex CLI. Each round evaluated the no-adaptation condition on six synthetic cases across recruiting, sales and research, with two repetitions. Neither round compared adaptation methods.

The second round reached the protocol's pooled 30–70% compliance band. This resulted from a revised mixture of explicit instruction-following anchors and cases requiring unavailable workflow knowledge. It does not demonstrate model improvement or intermediate difficulty in learning hidden requirements.

| Scientific round | Passing checks | Complete tasks | Actions | Reported input + output tokens |
| --- | --- | --- | --- | --- |
| 1 | 7/48, 14.58% | 0/12 | 6 clarify, 6 partial deliver | 123,784 |
| 2 | 28/48, 58.33% | 6/12 | 4 clarify, 8 deliver | 122,427 |

Both rounds produced twelve valid responses, without failed scientific calls. The twelve repeated outputs are not twelve independent organisations or tasks.

## Amendment and interpretation

Round 1 used only transfer cases whose correct emphasis and route were absent from current task inputs. The baseline had no history containing these conventions. None of the 24 hidden-requirement checks passed. Requests for unavailable information were scored as incomplete tasks, but can be reasonable given the baseline's information access. The result therefore does not establish poor instruction-following ability.

The documented round 2 amendment replaced one calibration case per family with a fully specified boundary anchor. It also made containment checks for natural-language summaries insensitive to letter case. Exact structured requirement checks remained unchanged. Model settings, prompts, histories, validation cases and the final-case generator were retained.

| Round 2 case category | Passing checks | Complete tasks | Actions |
| --- | --- | --- | --- |
| Explicit anchors | 24/24 | 6/6 | 6 deliver |
| Withheld-knowledge transfer | 4/24 | 0/6 | 4 clarify, 2 partial deliver |

All twelve hidden-requirement checks in round 2 failed. The pooled score combines perfect anchor compliance with low transfer compliance. The change between rounds is confounded by task composition and summary scoring and cannot be attributed to an improved model. A later advantage from providing history would establish an information benefit; the separate grounded-reflection versus direct-adaptation comparison is needed to assess the added value of the method.

## Provenance and resources

The local records are `runs/sol-medium-calibration-r1b-20260928` and `runs/sol-medium-calibration-r2-20260928`. Their `setup.json` files record configuration and source hashes. Round 1's original materials and scoring implementation remain in its `source_snapshot`, alongside its unchanged responses and results.

The two scientific rounds used 24 calls and 246,211 reported input-plus-output tokens, including CLI overhead. They used included subscription capacity without API-key billing, credit purchases or reset-credit redemption. No monetary amount is inferred from token counts. Limits were call-budget-controlled and token-audited, not strict per-request compute caps.

Twelve earlier schema-rejected transport attempts and two subsequent checks without study tasks are preserved separately and excluded from scientific outcomes. The rejections produced no valid answers; unavailable usage is not treated as zero.

These results concern a small authored decision task with deterministic checks. There was no human evaluation, measurement of professional work quality or recursive improvement. Main-study outputs and final cases were not examined for this report.
