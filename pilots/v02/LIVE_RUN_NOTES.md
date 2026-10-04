# First live pilot

Model selection and operating budget were delegated by Milad Morad on 28 September 2026. The selected model is `gpt-6-sol` with `medium` reasoning, used consistently across phases and conditions. There are two repetitions, a 300 second timeout, and no application-level automatic retries. The underlying CLI may reconnect internally; see the interruption note below. No model is selected for producing a favourable contrast.

The CLI is authenticated through ChatGPT. This run uses included subscription usage, with no purchase of credits, API-key billing or redemption of reset credits. Subscription capacity is shared with other work. An exhausted allowance stops work; it does not authorise paid fallback. This is an operating choice, not a conversion of tokens into monetary cost.

One complete calibration round uses 12 calls. The main run is limited to 168 calls and 3,000,000 reported input-plus-output tokens. A separate calibration configuration limits that stage to 12 calls and 250,000 reported tokens. Token totals include CLI overhead. Thresholds stop subsequent calls, but are not hard per-request limits. At most two scientific calibration rounds are allowed by the protocol.

## Transport rejection before calibration

The initial attempt `sol-medium-calibration-r1-20260928` received twelve HTTP 400 schema rejections before any valid model output. Pydantic defaults had left fields optional in the transport JSON schema. The strict interface requires every property to be listed as required. The local contracts also represent scope using a mapping; the strict interface needs an explicit attribute/value list.

All rejected attempts, unknown usage, and the source snapshot are retained in the ignored run directory. They are not treated as model answers, evidence of task difficulty or a completed scientific calibration round. A lossless transport conversion is tested separately. The work tasks, evaluation rules and prompts are unchanged by that correction. A new run name is used after the fix; previous files are never replaced.

## Interpretation of calibration

The baseline has no history from which to recover the private workflow conventions. A low score caused by correctly requesting unavailable knowledge must be distinguished from invalid output or inability to follow visible instructions. The 30–70% band is checked before the main run. We will not change the model or ask it to guess merely to hit that band. Any change to the calibration design must be documented before the next outcomes and must preserve the earlier result.

Two independent transport checks subsequently succeeded, using no study tasks. The first completed scientific round, `sol-medium-calibration-r1b-20260928`, produced 12 valid model responses and 7/48 passing checks (14.58%). Six responses clarified and six delivered partial records. Reported usage was 123,784 input-plus-output tokens. The source, tasks and original scores are archived with that round.

The second-round amendment is specified in the protocol. It balances fully specified anchors and withheld-knowledge cases, and makes only natural-summary containment insensitive to letter case. The new mixture assesses visible task execution and missing knowledge separately. Meeting its pooled band cannot establish that hidden requirements are moderately difficult or that reflection adds value. The main D/C contrast remains unobserved at this point.

## References

- [Codex models](https://learn.chatgpt.com/docs/models)
- [Codex pricing and included usage](https://learn.chatgpt.com/docs/pricing)
- [Structured output requirements](https://developers.openai.com/api/docs/guides/structured-outputs)

## Main-run transport interruption

The first main attempt, `sol-medium-main-20260928`, stopped during the 24th preparation call. Its sales direct-adaptation review exceeded the 300-second transport deadline after a WebSocket interruption, DNS errors and CLI reconnect attempts. The record remains failed even though late output was preserved by the CLI. No validation or final tasks were run, no condition scores were inspected, and the failed preparation is not replaced selectively. Twenty-three calls completed and one failed; all 24 records report 442,721 input-plus-output tokens in total.

The CLI's own logs reveal internal network retries. The runner performs no automatic re-invocation, but the capability label `automatic_retries=false` must be interpreted at that layer only. Reported model-call counts are logical runner calls, not a proven count of underlying network requests. This qualification applies to all Codex runs.

After DNS resolution recovered, a full new main attempt was designated `sol-medium-main-r2-20260928`, with the same model, settings, prompts, evidence, tasks, code and 168-call budget. All preparation is regenerated. The successful second calibration is reused. This technical repeat is chosen before any main condition scores or final cases are observed. The original attempt remains intact. No credit purchase or paid API fallback is authorised. If this full repeat also stops, report the available calibration and failure rather than repeatedly launching new complete runs.
