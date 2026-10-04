# FHGenie probe v2

Prepared offline for one separate approval. No v2 inference has been requested.

The first approved probe reached the requested model with HTTP 200. It reported
24 prompt tokens and 34 completion tokens, but the final content failed the
literal regex validator. Its final text was not retained. The cause of that
particular failure therefore cannot be reconstructed.

The regex has independently demonstrated defects. It rejects schema-equivalent
JSON escapes and accepts some whitespace that JSON disallows. This version uses
System.Text.Json to parse the entire final content. It requires an object with
exactly one property, decoded name status, string value ok. It rejects duplicate
properties, comments, trailing commas and appended content. No stripping of
Markdown, explanations or other output repair is performed.

Only diagnostic handling changes. request.json is byte-identical to v1. The
model, prompt, schema, reasoning setting, requested token limit and timeout stay
unchanged. This does not retroactively turn v1 into a successful contract test.

The final message.content channel is retained locally only when it is a string
of at most 16,384 UTF-8 bytes. Larger strings are not truncated or saved. The
limit applies to the content, not the JSON artifact wrapper. The separate
reasoning_content field is never persisted. A gateway could put reasoning into
the final channel itself, so this is a channel distinction, not a guarantee
about its contents. Credential echoes are checked both before and after JSON
decoding. The report contains finite failure categories and capture status,
not raw provider or parser errors. This remains a synthetic connection test.

23 offline fixtures and 14 parser cases pass. No real key is read by those tests.
PowerShell 7 is required. Default execution checks hashes and request format only.
-ExecuteOnce requires a new matching approval and makes at most one POST, without
retry, redirect, fallback or a study launch. One success would establish only
this toy response, not general schema enforcement or scientific performance.
