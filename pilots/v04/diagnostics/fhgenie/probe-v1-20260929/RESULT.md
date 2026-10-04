# FHGenie probe v1 result

The separately approved call ran once on 29 September 2026. No retry or study
run followed. HTTP 200 and the requested model identifier were returned in
484 ms. The service reported 24 prompt tokens and 34 completion tokens, 58 total.
Reported model was deepseek-ai/DeepSeek-V4-Flash-0731; reported server fingerprint
was vllm-0.25.1-dp4-ep-3e90b15f. These are observations, not independent deployment
attestations or confirmation that every requested setting was applied.

The response passed the one-choice, finish-reason, assistant-role and tool/refusal
checks and contained a separate reasoning field. Final content failed the regex
test. The original helper saved no final content or content-type metadata, so the
exact cause is unknown. The retained result cannot establish JSON invalidity.

An offline audit demonstrated that the regex rejects legitimate escaped property
names or values, while accepting some whitespace that strict JSON rejects. This
does not show that either occurred live. A separate v2 replaces the validator and
adds bounded final-channel capture while keeping the request byte-identical.

The original approval, reservation, source hashes and result remain untouched.
The live authorization was consumed. v2 is prepared without a new live approval.
The result establishes basic service reachability and reported model/token data,
not a validated pilot backend or any research finding.
