# FHGenie connection and output-contract probe

Prepared for one separate live approval. This is not the research pilot and no
inference request has been made by this preparation.

An authenticated GET of the user-supplied FHGenie model inventory succeeded on
29 September 2026. It included DeepSeek V4 Flash 0731, MiniMax M2.5 and NVIDIA's
GLM 5.2 NVFP4. The sandboxed GET failed without an HTTP status; the separately
escalated GET succeeded. Neither was an inference request. The API key stays in
the existing Windows user-encrypted file outside the repository.

DeepSeek V4 Flash 0731 is the first candidate. Its official model card documents
the exact checkpoint and low, high and max reasoning settings. Its published
agent benchmarks do not establish performance on this study's task. No ranking
between available models has been measured here.

The one-call probe requests exactly {"status":"ok"}, a strict JSON schema,
low reasoning effort and at most 2,048 generated tokens. It uses a single POST
to the fixed FHGenie chat/completions route with a 90-second timeout. These
settings are capabilities to test, not capabilities established by the inventory.
There is no retry, redirect, alternative model or automatic research run. Only
the toy prompt and schema are transmitted. A correct response must finish normally,
contain the expected JSON without tool calls and include usable token counts.
One successful toy response does not prove general server-side schema enforcement
or establish the model's research performance. The requested token limit is not
an independently verified provider accounting or spending guarantee.

The helper requires PowerShell 7. The probe defaults to checking configuration and code hashes without reading the
key. -ExecuteOnce additionally requires matching approval and consumes an exclusive
reservation before making the request. Results contain sanitized diagnostic fields,
not credentials or raw reasoning. Transport and format failures are not scientific
errors. Unknown usage remains unknown.

If the probe succeeds, integrate a separate FHGenie backend, retaining the old
Codex transport and failed-run records. All live guards, source bindings and
run approvals must cover the new backend. Register actual model/settings and
document the changed request envelope. The former gpt-6-sol attempt is not a
scientific baseline. Byte-identical reviewed materials may retain their recorded
approval with a documented comparison, but the new run needs a separate approval.
No research sources, materials, seeds or original approvals are changed here.

Reference

https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731
