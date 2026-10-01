# Pilot v0.4

Synthetic difficulty mapping for evidence-based adaptation. This pilot asks where a strong two-pass direct adaptation procedure loses warranted decisions. It does not evaluate a grounded-reflection arm.

The [protocol](../../docs/pilot-v04-protocol.md) and [amendment 3](../../docs/pilot-v04-amendment-03.md) were approved for implementation by Milad Morad on 29 September 2026. Each setting contains one warranted transfer change, one change in an observed context, one resolved retention with transfer and one unidentifiable change. Candidate-level errors and directional scope measures are reported separately for C1 and C2, outside the headroom criterion.

## Status

**Result (1 October 2026):** The registered run completed 192/192 calls with DeepSeek-V4-Flash-0731 at reasoning `high`. Under the registered metric C made 21/24 warranted diagnostic decisions and B 16/24; on the executed output fields B was correct in 23/24 and C in 21/24, because B's misses are mainly over-broad declared rules. Headroom is not met in any setting; it is provisional in S4 because of the attribution. See the [difficulty map report](DIFFICULTY_MAP_REPORT.md) and the [human attribution](review/attribution-live-fhgenie-high-20261001/README.md).

[Amendment 5](../../docs/pilot-v04-amendment-05.md) (30 September 2026) fixes reasoning `high`, an output limit of 32,768, a hash-pinned PowerShell 7 and tolerance of up to 19 isolated response failures. Both contract tests at `high` passed with 16/16 valid responses; the second, at 32,768, observed a maximum output of 24,848 tokens. The [live request](preflight/fhgenie-high-20260930/LIVE_FREIGABE.md) is prepared with a new review binding, 462 offline tests and a complete [mock run](runs/offline-amendment5-20260930/REPORT.md). Live approval is pending.

[Amendment 4](../../docs/pilot-v04-amendment-04.md) was approved on 30 September 2026: all arms move to `deepseek-ai/DeepSeek-V4-Flash-0731` via FHGenie. Results will not be comparable with v0.3 and describe this model only. The [contract test](../../docs/pilot-v04-fhgenie-contract-test.md) at reasoning level `high` is implemented in [`diagnostics/fhgenie/contract-test-high-20260930`](diagnostics/fhgenie/contract-test-high-20260930/README.md) and verified offline. It has not been run and requires its own explicit approval. The transport now accepts the documented levels `low`, `high` and `max`. The source binding changed, so the final run needs a new review binding, verification and live approval.

The [FHGenie revision](../../docs/pilot-v04-fhgenie-transport.md) adds a direct API backend for `deepseek-ai/DeepSeek-V4-Flash-0731`. The third separately approved connection probe returned valid JSON after removing server-side `response_format`. It reported 57 tokens. All three FHGenie probes together reported 173 tokens and used only a toy request. This is a working connection, not a research result or a guarantee that complex contracts will succeed. A new research run requires approval of the new model and configuration. The previous consumed approvals remain closed.

The integration passed **191 Python tests and 31 offline HTTP-driver cases**. Its [full offline run](runs/offline-fhgenie-integration-20260929/REPORT.md) completed 192 mock calls without failures and preserved 144 task rows and 48 preparation rows. The [new review binding](review/materials-amendment3-r2-fhgenie-20260929/README.md) preserves all 14 example and surface-audit files byte-for-byte, carrying forward the actual material approval with its provenance. The [verification record](preflight/fhgenie-20260929/verification.json) and [separate live request](preflight/fhgenie-20260929/LIVE_FREIGABE.md) document the API boundary and proposed configuration. Live approval remains pending. No final-test tasks were generated during this integration.

Milad Morad approved revision-r2 materials and the one-time live run on 29 September 2026. The [live attempt stopped on its first C1 call](runs/live-amendment3-r2-20260929-INCIDENT.md) because the upstream HTTP-200 response did not provide the required streaming content type. No usable model response was obtained. The other 191 scheduled calls were blocked. No retry or replacement was made. Token consumption is unknown. No v0.4 model result, improvement claim or enterprise ROI is available.

The linked incident is the authoritative interpretation of this attempt. The sealed automatic report's zero scores and Headroom=False reflect blocked planned rows, not observed model performance. Any further model attempt requires fresh authorization.

The initial implementation passed 73 unit tests and completed the [original 192-call offline run](runs/offline-20260929/REPORT.md). These results describe the original materials and remain preserved. They do not validate the revised materials.

Amendment 3 verification completed on 29 September 2026. All 109 unit tests passed. The [revised offline run](runs/offline-amendment3-20260929/REPORT.md) completed all 192 mock calls without failures and preserved 144 task rows and 48 preparation rows. All 24 histories passed the counterfactual relevance gates. Source bindings and the run, preparation, evaluator and review seals verified successfully. These are implementation checks, not model findings.

The [amendment-3 examples](review/materials-amendment3-20260929/README.md) were not approved. The [supplied review](review/feedback-surface-20260929.json) reported agreement with their decisions through an independent AI-assisted reconstruction, but found timestamp and comment shortcuts. This is AI-assisted review, not human validation. The earlier examples, run and source snapshots remain preserved.

The [surface repair protocol](../../docs/pilot-v04-surface-repair.md) specifies revision `v04-amendment-03-r2`. It varies presentation while preserving approval semantics, overlaps genuine and nonbinding review comments, randomises valid timestamps and input order, and audits simple surface selectors on separate development and review histories. Material approval is recorded for this revision. Live approval remains separate and pending.

Revision 2 passed all **137 v0.4 unit tests** on 29 September 2026. Its [complete offline run](runs/offline-amendment3-r2-20260929/REPORT.md) completed 192 mock calls without failures, with 144 task rows, 48 preparation rows and all 24 counterfactual material gates passing. Source snapshots and stage seals verified. The [verification record](review/surface-repair-verification-20260929.json) records the unchanged hashes of 1,723 protected prior files in aggregate and the new artifact bindings. These checks do not establish model performance.

The [same six cases are exported for renewed review](review/materials-amendment3-r2-20260929/README.md), especially [S1 sales](review/materials-amendment3-r2-20260929/S1-sales.md) and [S5 retrieval](review/materials-amendment3-r2-20260929/S5-retrieval.md). The [surface audit](review/materials-amendment3-r2-20260929/surface-audit.md) fits selectors on 24 development histories and evaluates them on 24 separate review histories. In the current accepted-review population, development-selected family winners attain review history-macro balanced accuracy from 0.463 to 0.544. Eight histories contain both classes; 16 remain undefined for that metric. The overall development winner attains 0.463. No tested selector is perfect on the held-out hard negatives. The broad work-record population retains a higher diagnostic value of 0.816 for its development-selected winner. This includes legitimate differences between review and other records and is not presented as chance-level performance. The audit does not rule out every possible shortcut.

The [original approval record](review/materials-amendment3-r2-20260929-approvals.json) records material approval and distinguishes supplementary AI-assisted checking from human validation.

The [live request](preflight/live-20260929/LIVE_FREIGABE.md) documents the final v04-specific transport and the request subsequently approved for the one-time attempt. All **157 offline tests passed**. The installed CLI was inspected through the complete attested transport with local response fixtures, without real inference. Normal output passed, a 503 was not retried, and an injected tool response was blocked before execution. No private canaries or offered tools appeared in the requests. A one-request gateway enforces the upstream call boundary.

The [live-ready review binding](review/materials-amendment3-r2-live-ready-20260929/README.md) preserves all 14 material files byte-for-byte. Its adjacent approval carries forward the original material response with an explicit equality record, and records the subsequently granted live permission. That permission was reserved by the stopped run and cannot be reused. The [verification](preflight/live-20260929/verification.json) records the final attested repetitions, source hashes and limitations. This is a transport verification, not a model result.

The [historical wording check](review/legacy-wording-check-20260929.json) used the frozen original oracle and all six original review histories. Removing the two factor-specific instructional fragments left the complete oracle results and future-task actions unchanged. Because the oracle does not parse this prose, this establishes operational invariance only.

## Run offline

From the repository root, using Python 3.11 or later and the project's installed dependencies:

```powershell
python -B pilots/v04/run.py offline --output pilots/v04/runs/offline-amendment3-r2-check
python -B pilots/v04/run.py review --output pilots/v04/review/materials-amendment3-r2
$env:PYTHONPATH = 'src;pilots/v03;pilots/v04'
python -B -m unittest discover -s tests -p 'test_pilot_v04*.py' -v
```

Existing output directories are never overwritten. The mock follows the public execution contract and performs no inference. Its scores test the pipeline, not model capability. Mock token use is unknown rather than a fabricated zero.

Seeds control material generation and call order. The CLI transport does not expose a model sampling seed, so a live response is not guaranteed to reproduce exactly. Record and inspect the preserved raw completions and reported usage. Token limits are checked between calls and may be crossed by the final in-flight completion.

The FHGenie backend likewise makes no claim of deterministic sampling. It uses a fixed HTTP endpoint and a local DPAPI-encrypted key. Its model receives only the explicit messages and response schema. Separate provider reasoning text is not retained. Strict local parsing and the existing Pydantic contracts validate the final answer without repairing it or making a replacement request.

The revision-2 offline defaults are 44321 for histories, 44322 for future instances and 44323 for call order. Review materials use a distinct development namespace and seeds 44331/44332. The generator also uses a revision-specific namespace. Any live configuration must be separately frozen and approved with fresh final-test material.

The review command exports six development cases with public records and separate evaluator truth. An adjacent approvals file starts with both approvals pending. Record actual human responses only after review. A live configuration and separate explicit authorisation are required before the live runner can call the model. Existing v0.1–v0.3 files are read-only dependencies and remain unchanged.

## Structure

* `reflectai_v04/data.py` generates seeded placeholder histories and future tasks.
* `reflectai_v04/presentation.py` varies public record presentation without changing the compatible policies.
* `reflectai_v04/surface_audit.py` tests prespecified surface-only selectors on disjoint development and review histories.
* `reflectai_v04/oracle.py` derives admissible policies exclusively from public evidence.
* `reflectai_v04/counterfactual.py` checks each manipulated record for an action flip or contradiction under an explicit false-approval intervention.
* `reflectai_v04/evaluation.py` separates warranted actions, field outcomes, candidate errors and attribution uncertainty.
* `reflectai_v04/runner.py` freezes preparations before instantiating future tasks and preserves missing attempts.
* `reflectai_v04/backend.py` logs every attempted completion and enforces call and token stops without retries.
* `reflectai_v04/storage.py` binds shared dependencies and immutable source and preparation snapshots.
* `prompts/` contains the versioned strong C prompts and shared generation contract.

The C1, C2 and generation instructions are inherited unchanged from v0.3 round 2. The shared contract omits the sentence about a provisional reflection-draft type, which is not part of this study. No weaker C procedure is introduced.

## Interpretation

The oracle evaluates fourteen Boolean functions over two declared binary context dimensions. Constants, single literals, conjunctions and disjunctions are possible. XOR and XNOR are excluded publicly. Transfer to an unseen context can therefore be warranted, but only under that supplied restriction. Raw artifact settings require reconstruction of observations while the field operations remain supplied. This does not yet test unrestricted discovery of new concepts or requirements.

Counterfactual relevance is audited without model calls. Each manipulated type present must include an action-flipping record in an unidentifiable history or a contradiction-producing record in a decided history. An inconsistent evidence set is never counted as a changed decision. These checks show conflict or decision relevance, not actual model errors.

Unsupported transfer and missed warranted transfer are separate secondary measures. An adoption matching a simplest compatible function can be flagged when it extends beyond the warranted scope. This is an observed pattern, not proof that the model used simplicity as a decision strategy. Tied simplest functions remain distinct possibilities.

Decided cases also have a secondary marker for wrong adaptations consistent with majority or latest-record resolution of an apparent contradiction. It requires conflicting visible configurations in the same context and an unambiguous heuristic prediction. Matching that prediction does not establish the model's reasoning. The marker can overlap scope errors and does not change the headroom criterion.

Four diagnostics per setting provide little resolution. The 70 percent headroom threshold means at most two correct decisions out of four. Candidate errors may expose weaknesses before they affect those task outcomes, but model-selected candidate counts are not independent sample sizes. Error attribution can remain provisional pending human review.

A single control per history cannot reveal every possible scope error. It stays within the same workflow and checks a different context. Additional private scope probes evaluate candidate consequences at the other registered boundaries. Some controls require retention because the evidence remains unresolved, even though their constructed world uses the baseline.

Amortisation is a conditional token projection from two future tasks per history. It is not a price estimate or evidence of recurring savings. The data are synthetic placeholders, the model is single-family, and histories share templates. A later method selected using this map needs a new protocol and fresh evaluation cases.
