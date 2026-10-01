# FHGenie transport revision

Implementation preparation, 29 September 2026. This document does not authorize
model calls or a new research run. The user's existing one-call diagnostic
approvals were consumed by those calls.

## Reason for the revision

The original gpt-6-sol research attempt stopped before obtaining a usable model
response. Its records and source snapshot remain preserved. The user subsequently
requested an API connection and supplied a local FHGenie on-premises credential.
An authenticated model inventory identified DeepSeek V4 Flash 0731 as available.

Three separately approved technical probes used only the toy instruction to
return {"status":"ok"}. The first two schema-constrained calls each reported
58 tokens. The second retained final channel was {"status{"status":"ok"}, which
is invalid JSON. The third removed only response_format, passed the same strict
local validator and reported 57 tokens. The three FHGenie probes reported 173
tokens in total. Prior Codex attempts with unknown usage are not included.

The third call returned the expected model identifier and the reported server
fingerprint vllm-0.25.1-dp4-ep-3e90b15f. These observations do not independently
attest deployment weights, backend patches or parameter enforcement.

[vLLM PR #44993](https://github.com/vllm-project/vllm/pull/44993) describes duplicate
opening tokens when constrained generation crosses a reasoning boundary under
particular speculative-decoding and scheduling configurations. That mechanism is
consistent with the observed failure, but FHGenie's configuration was not inspected.
One successful unconstrained toy answer does not establish robust schema adherence
or performance on the pilot. No research task has been run through FHGenie.

## Proposed registered configuration

| Parameter | Value |
| --- | --- |
| Backend | fhgenie |
| Endpoint | <FHGENIE_ENDPOINT> |
| Requested model | deepseek-ai/DeepSeek-V4-Flash-0731 |
| Requested reasoning effort | low |
| Temperature / top_p | 1 / 1 |
| Requested per-call output limit | 16,384 tokens |
| Timeout | 420 seconds per call |
| Planned requests / attempt cap | 192 / 200 |
| Reported-token stop | 6,000,000, checked between calls |
| Proposed final history / future / order seeds | 44361 / 44362 / 44363 |

No final histories or future tasks are generated during this integration work.
Development tests use the existing development seeds. The new final seeds are
prospective choices, not selected from observed performance. The higher output
limit accommodates the actual contracts and reasoning, rather than the tiny
connection-test answer. Model sampling is not deterministic. The provider's
handling of the requested token limit must not be presented as an independently
verified hard spending limit.

The credentials, account balance and organizational allocation are not part of
the scientific configuration. No purchase or claim of zero cost follows from
having a working key. Calls record reported usage; missing usage stops a live run.

## Public request and response boundary

The Python transport passes a JSON request to a fixed PowerShell 7 HTTP driver.
The driver makes one POST using the existing Windows user-encrypted key, with
normal TLS validation, redirects disabled and no retries. The model has no tool,
file, browser or shell interface. The child process starts in an empty temporary
working directory. That directory is not claimed as operating-system read
isolation; only the supplied public messages are sent over the API.

The frozen study prompt remains the user message. A system message supplies the
strict response schema and requests one JSON object. The API request omits
response_format and does not include previous conversations or runtime context.
This explicit schema message replaces the former Codex request envelope and is
a documented transport change, not scientific equivalence with the old model.

The local JSON decoder and existing contract validation remain authoritative.
There is no Markdown stripping, prefix repair, answer substitution or retry for
an invalid response. Unknown usage, model-identity mismatches, tool calls and
systemic transport failures stop the run. Final-channel content is preserved for
technical diagnosis. Separate reasoning text and credentials are not logged.
Field-level or scope errors in a valid response remain governed by the original
evaluation and conservative error-attribution rules.

## Research design and approvals

The r2 materials, public conventions, oracle, prompts, A/B/C arms, 192-call
schedule and evaluation are unchanged. This is still a difficulty map, not a
test of an implemented grounded-reflection arm. Results would describe this
DeepSeek deployment and these settings. They cannot stand in for gpt-6-sol
results or establish cross-model generality.

All live guards cover both API and Codex backends, including review/source
bindings, final-seed separation, exclusive approval reservation and budget stops.
The new transport, HTTP driver, tests and this document belong to the source
binding. The previous consumed approval cannot authorize the new configuration.

Before a live run, export a new review binding and compare the six existing
example pairs and two surface-audit files byte-for-byte. An exact comparison can
carry forward the actual r2 material approval with its provenance; it is not a
new human validation. Final-run approval remains empty until the user approves
the concrete configuration. Complex-contract live checks, if needed, also require
their own explicit authorization and must use development or toy material only.
