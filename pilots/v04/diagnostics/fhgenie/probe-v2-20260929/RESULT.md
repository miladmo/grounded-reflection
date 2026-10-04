# FHGenie probe v2 result

The separately approved second probe ran once on 29 September 2026. No repeat
or research run followed. It returned HTTP 200 in 255 ms, the requested model
deepseek-ai/DeepSeek-V4-Flash-0731 and 24 prompt plus 34 completion tokens.
The two FHGenie inference probes together therefore reported 116 tokens.

The captured final channel is the exact 23-byte UTF-8 string

    {"status{"status":"ok"}

This is invalid JSON, not a valid escaped spelling. The v2 parser correctly
rejected it. The v1 final text is unknown, so its exact failure cannot be
reconstructed by comparison. Both records and consumed approvals are preserved.

The repeated opening is consistent with the failure mechanism described in
vLLM PR #44993, but no provider-side configuration or patch status was inspected.
A separate, unapproved v3 control removes only response_format while retaining
the same prompt and local validator. There is still no validated study backend
or scientific research result.

https://github.com/vllm-project/vllm/pull/44993
