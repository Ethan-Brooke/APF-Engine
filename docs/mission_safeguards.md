# Prospective private-publisher evidence gate

This is an operations boundary, not a mathematical theorem or automatic source-fidelity certificate. The maintained implementation is `apf/evidence_gate.py`; `apf/private_publisher.py` checks it immediately before its mutation callback. Existing research modules, historical acceptances and frozen publisher runners are not edited. The independent review and actual future publisher integration remain separate acceptance steps.

## Run and integrate

Run `py -3 -B -m unittest discover -s tests -p test_evidence_gate.py -v` from this worktree. All fixtures are synthetic; callbacks collect arguments or raise simulated transport errors. No credentials or network access are used.

A future mutable publisher must construct the exact JSON or multipart payload bytes first, then invoke the wrapper for **every** content-changing call, including uploads and mission-description updates:

```python
from apf.evidence_gate import canonical_bytes
from apf.private_publisher import GuardedPrivatePublisher

publisher = GuardedPrivatePublisher(
    authorization_pin={"path": ABSOLUTE_FROZEN_AUTHORIZATION_PATH,
                       "sha256": INDEPENDENTLY_TRUSTED_AUTHORIZATION_SHA256},
    publisher_id=ASSIGNED_PUBLISHER_ID,
    mutation_callback=existing_bytes_transport,
)
result = publisher.mutate(
    action="private_stage", method="PATCH", path=EXACT_REVIEWED_PATH,
    payload=EXACT_REVIEWED_BYTES, content_type="application/json",
)
```

The transport receives `(method, path, immutable_bytes, content_type)`. It owns credentials and sends those exact bytes. A callback that ignores or changes its arguments is outside this guarantee. Build multipart boundaries before freezing the independently accepted request hash; the wrapper handles those as exact bytes, without reserialization. Read-only queries and token refresh may remain outside the content-mutation wrapper. This module makes no HTTP requests itself.

The frozen `physical_interface_20260912/delivery_runner.py` is reference evidence only. A future reviewed successor must route both its `call` mutation branch and its separate multipart `/verify` branch through this entry point. Merely calling `validate_request` once at startup leaves later changes unguarded. The wrapper revalidates pins/time on every mutation and checks expiry again before callback entry. It does not retry after an uncertain callback failure. Existing read-only reconciliation and publisher journaling remain necessary.

## Schema proposal for existing records

Use `evidence_gate` with integer `schema_version: 1` in prospective frozen assignment, selection acceptance, proof/source acceptance, package manifest, release and source-consultation records. Do not rewrite old records to imply earlier compliance. `SCHEMA_PROPOSAL.json` and the runnable `synthetic_example` enumerate exact implemented fields. Each pin is exactly `{path: absolute filesystem path, sha256: lowercase SHA256 of exact file bytes}`; strict JSON rejects duplicate keys. Unknown schema versions and missing required values fail closed. Native API responses are retained verbatim and are not wrapped or reserialized before hashing.

An immutable **authorization snapshot** in the existing release evidence area anchors mission/basis files, frozen assignment, selection, review and release, approved-input source pins, named author-independent reviewer IDs, publisher ID, allowed action and commissioned conclusion. Its SHA256 must come from an independent trusted policy configuration/channel, never from candidate data. It is not another progress tracker. Reviewer-name matching is not identity authentication.

Do not pin the entire mutable live `ACTIVE_WORK_ORDER.json`. Status or budget changes must not alter the frozen commissioned assignment. `mission_scope_sha256` and `basis_scope_sha256` are independently authorized content identities, distinct from current administrative document hashes. Updating authorized administrative mission references requires a new trusted authorization snapshot with the same frozen consumed-content/review pins where meaning is unchanged; it does not revoke the historical proof. The code does not infer that a document change was merely administrative. New or weakened input meaning requires explicit user authority and affected source/proof review, not a convenient recomputed hash.

The trusted authorization also names `manager_id`. The frozen assignment includes `manager_id`, `manager_consultation`, and `assigned_at`. The manager record must be saved before assignment; assignment must precede selection evaluation. Manager, author, selection reviewer and proof reviewer consultations all cover the consumed source pins. Nonempty `work_type` and `intended_addition` are required in the assignment and must match explicitly in both selection and proof review.

Selection and proof review bind the exact assignment and conclusion; the final review also binds the package, all declared premise IDs, proof-evidence pins, exact accepted outgoing requests, permitted claim and four evidence axes. `accepted_requests` is mandatory: an operations release cannot replace a payload after independent review merely by hashing its replacement. Consultations include personally attributed actual paper/code pins, read-completion time and saved-record time preceding the corresponding evaluation or construction. The code verifies these declared records and file integrity, not whether a person actually read them.

The package declares all consumed source pins, file pins, conclusion and premise nodes. Each node has `id`, `kind`, `suppliers`, `evidence`; approved inputs carry `input_id`, original definitions/math apparatus carry an independently reviewed disposition, and conditional physical assumptions carry an explicit unresolved disposition. Derived leaves require an explicit independently reviewed no-physical-premises disposition. Ordinary mathematics does not need fabricated physical input IDs. Missing suppliers, cycles, changed inputs, unused disconnected premise entries and assumed outputs are refused. Semantic completeness of the declared inventory remains independently reviewed.

Actions are separate:

* `private_stage`: exact independently reviewed conditional material may be staged privately, with no foundation, graph-completion or full-mission credit. `proof_verdict: not_applicable` is allowed only at this stage for independently reviewed non-proof material.
* `foundation_promote`: accepted proof evidence, declared recursive physical-premise closure, machine-checking evidence and completed scoped objective are required.
* `native_graph_complete`: those promotion checks plus current independently reviewed raw native graph and separately evidenced native default-UI coverage. It means completion at the exact commissioned graph scope, not a general-purpose milestone display label.
* `full_mission_complete`: all preceding checks plus a frozen `full_mission` assignment matching the independently authorized full-mission conclusion. A first segment is refused.

Native graph requirements use actual node IDs and typed edges, including native sketch intermediates. The gate checks root, freshness, endpoint provenance fields, statuses, every reviewed reachable node/edge, no additional unreviewed reachable dependency, no cycle/truncation, and declared premise coverage. Deep API reachability alone is insufficient: an independently reviewed default-UI record with pinned capture and exact visible IDs/edges is also required. Captures/normalized visibility declarations are evidence for human review; this module does not inspect pixels or authenticate that a response originated at the platform.

## Tested boundary and explicit bypasses

The tested guarantee is that an invalid prospective request cannot enter this wrapper's callback. It is not a platform permission lock. Direct HTTP clients, a legacy runner, arbitrary direct tools, altered wrapper code, a caller-controlled trust anchor, a dishonest callback or omitted/false semantic attestations are outside that guarantee. Hash checks do not prove physics, enforce reviewer identity, deploy to the second box, or make all writers use this entry point. Files can change after validation; the exact outgoing bytes remain immutable, while external concurrent writers and transport behavior require operational control. No process-wide write lock or one-shot/anti-replay ledger is implemented. Repeated valid invocations remain possible; the wrapper never automatically retries them.

Keep implementation, independent acceptance, integration into the selected publisher, observed use and second-box deployment as distinct status fields. This candidate is locally tested and ready for independent review; it has not been installed into the old runner or used for a live write.

## Independent review corrections in candidate03

R1: enforce selection decision <= construction <= package freeze <= final review decision <= release start <= current time, and proof evaluation cannot begin before construction. R2: graph and default-UI observations cannot postdate the pinned independent review decision; a later observation needs a new reviewed release. R3: the supported mutation route grammar is `/[A-Za-z0-9_-]+(?:/[A-Za-z0-9_-]+)*`. Query strings, fragments, escapes, dot segments, duplicate slashes, backslashes and control characters are denied before route/privacy policy or callback. This deliberately restrictive adapter supports the relevant plain native API mutation endpoints; new route syntax requires explicit implementation/review, never silent normalization.

For native completion, stage first, collect actual graph/default-UI observations, then obtain a later independent final release-review decision covering those observations. Reuse earlier unchanged proof/source acceptance by exact preserved references in the existing review evidence; do not edit that earlier acceptance or backdate new observations. The new pinned final review reaffirms the unchanged proof/source scope and explicitly reviews the new graph facts. The gate requires its decision timestamp to cover all attached observations. Merely changing a timestamp without that review is not authorization.

Mutation media types are restricted to application/json, plus exact reviewed multipart/form-data bytes only at /verify. Alternate +json, opaque text, and multipart registration are rejected before the callback; they cannot bypass endpoint privacy inspection.
