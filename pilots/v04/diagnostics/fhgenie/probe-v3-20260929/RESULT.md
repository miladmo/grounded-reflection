# FHGenie connection probe v3

The separately approved request completed successfully on 29 September 2026.
One POST returned HTTP 200 and the final content `{"status":"ok"}` passed the
unchanged strict local validator. No research task was included.

The response identified `deepseek-ai/DeepSeek-V4-Flash-0731`, reported 24 input
tokens and 33 output tokens, and returned the server fingerprint
`vllm-0.25.1-dp4-ep-3e90b15f`. Elapsed request time was 1,223 ms. Separate
reasoning content was present but was not retained.

The only request change from probe v2 was removing `response_format`.
The v2 final content was invalid JSON. This successful control supports
investigating constrained generation as the source of that failure. It does
not establish the cause or reliable adherence to complex response contracts.

The three approved FHGenie probes together reported 173 tokens. Earlier Codex
attempts with unknown usage are excluded. All three probe approvals are consumed.
There were no retries, replacement requests, purchases or research model results.
