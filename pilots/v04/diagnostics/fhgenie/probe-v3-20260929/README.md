# FHGenie plain-output control probe

Prepared offline for a separate one-call approval. No v3 inference was requested.

The v2 final channel contained {"status{"status":"ok"}, which is invalid JSON.
It reported HTTP 200, the expected DeepSeek model, 24 prompt tokens and 34
completion tokens. The corrected strict parser rejected it appropriately.

vLLM PR #44993 describes a closely matching mechanism: under certain reasoning,
async scheduling and speculative decoding configurations, the grammar state
does not advance for the first answer tokens, so opening tokens are emitted
again. It reports a verification with DeepSeek V4 Flash DSpark. FHGenie's actual
configuration and patch status are unknown. This is a plausible explanation,
not a confirmed diagnosis.

This control removes only response_format from the request. Model, prompt,
reasoning_effort, sampling parameters, output limit and timeout remain unchanged.
The prompt still asks for precisely the same JSON. The strict local parser is
unchanged. There is no repair, prefix removal or answer substitution.

Success would demonstrate one valid answer without the explicitly requested
schema constraint and would be consistent with a problem in the constrained
output path. A single stochastic comparison cannot prove the precise cause or
establish reliable JSON generation for the research pilot. json_object is not
used as a fallback because it still requests constrained JSON generation.

The existing one-call approval gate, exclusive reservation, no retries or
redirects, 90-second timeout and requested 2,048-token output limit remain in
place. The final channel capture and credential protection are unchanged from
v2. No automatic study run or alternative request follows this probe.

23 offline fixtures and 14 strict-parser cases pass, including a check that
adding an unregistered response_format is rejected. PowerShell 7 is required.

Primary source

https://github.com/vllm-project/vllm/pull/44993
