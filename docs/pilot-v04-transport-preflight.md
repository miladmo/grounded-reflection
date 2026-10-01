# Pilot v0.4 transport preflight

29 September 2026. This implementation addendum changes only the inference
transport. Material revision `v04-amendment-03-r2`, prompts, cases, oracle,
analysis, and the registered A/B/C design remain unchanged. Material approval
and permission to make model calls are separate. Live permission is pending.

## Why the transport changed

An empty working directory and a read-only sandbox are insufficient evidence
of isolation. The installed CLI can normally read outside its current directory.
Its model metadata also enables capabilities beyond the feature flags used by
the earlier transport. Inspection of the actual request, including nested
`additional_tools`, found tools that had not been intended for this experiment.
No research inference was made during this inspection.

The v0.4-specific transport uses a fresh empty temporary working directory outside
the repository. It disables project document loading, user configuration, tools,
agents, external services, and model metadata that offers additional tools. The
restricted catalog retains the installed model's remaining metadata and base
instructions. Standard CLI instructions and installed skill descriptions may
still appear. They do not contain experiment evidence or evaluator information.

A local gateway allows at most one upstream Responses request per scheduled
completion. It rejects requests advertising tools and stops response events that
attempt tool use before forwarding them to the CLI. A second request is rejected
locally. This matters because a deliberately injected, unadvertised tool response
caused the CLI to attempt another request even with all tools disabled.

The gateway forwards only to the fixed ChatGPT Codex Responses endpoint. It does
not follow redirects or retry. The CLI's request and stream retry limits are also
zero. Authentication stays with the installed CLI, with ChatGPT sign-in required.
API-key and alternative endpoint environment variables are removed from the child
process. Credentials are never written to experiment records. No purchase or
credit-reset operation is available in this transport.

## Offline test and its limits

The preflight runs the installed CLI against a local response fixture. There is
no model behind this fixture, no request forwarding to an inference service, and
no research result. The fixture captures the actual model-visible request. It
checks both top-level tools and nested additional tools. Synthetic private-file
markers identify accidental inclusion of evaluator files, future tasks, or
ancestor project documents. Success, server errors, duplicate requests and
prohibited tool responses are tested separately.

Local routing and authentication differ from a live request by necessity. The
diagnostic replaces the gateway's outbound connection with a loopback fixture
and disables authentication to that fixture. It preserves the CLI executable,
model, reasoning, restricted catalog, workspace setup, tool restrictions and
retry settings. The production authentication and remote endpoint cannot be
tested without making a live request and are not claimed to have been tested.

This is a capability and request-content boundary, not a claim of operating
system read denial. Its validity depends on the pinned CLI binary and settings.
The runtime attestation binds the executable, transport, gateway, catalog and
exact fixed arguments. A changed binding fails before inference. The run's
source snapshot also includes the catalog and attestation. Results of the actual
preflight are recorded separately from this specification.

## Run limits and failures

The plan has 192 completions, consisting of 48 C preparations and 144 task
generations. The outer attempt limit is 200, but unused capacity does not permit
retries or replacements. Each scheduled completion permits at most one upstream
request. A failed completion remains recorded. Integrity failures or unknown
token usage stop the study. There is no resumption or replacement authorization.

The token stop is 6,000,000 reported input plus output tokens, checked between
calls. The final in-flight response can cross that threshold. This is explicitly
not a guaranteed hard token cap. The per-call timeout is 420 seconds. The model
is `gpt-6-sol` with `medium` reasoning. The CLI does not expose a model sampling
seed, so dataset and order seeds do not guarantee identical model responses.

No live task is generated for transport testing. A fresh seed configuration is
prepared without executing it. The six reviewed examples are re-exported only
to bind the changed transport source. Exact equality of all material files is
checked before carrying forward the author's material approval. The original
review, source snapshot, and offline results remain preserved. New live approval
must identify the new source and configuration.
