# Administrative publisher

This separate operations component appends exact independently reviewed governance text to an existing private mission description. It does not authorize scientific staging, proof submission, foundation promotion, graph completion, changed inputs, or public release. The four accepted candidate04 scientific files are unchanged.

## Interface

```python
from apf.administrative_publisher import (
    GuardedAdministrativePublisher, validate_administrative_request,
    administrative_baseline_digest,
)

publisher = GuardedAdministrativePublisher(
    independently_provisioned_authorization_pin, actual_publisher_id,
    checked_live_baseline_transport, clock=aware_utc_clock,
)
publisher.mutate(
    action="administrative_update", method="PATCH",
    path="/missions/<exact canonical lowercase UUID>",
    payload=exact_reviewed_payload_bytes, content_type="application/json",
)
```

The constructor and mutate signature match the existing scientific wrapper. Each call revalidates all pinned bytes, exact review, identifiers, scope, privacy baseline and expiry. The immutable payload is passed once to the callback. Callback failures propagate without automatic retry. The optional clock must return an aware datetime and is checked again before entering the callback.

`validate_administrative_request(authorization_pin, publisher_id=..., action=..., method=..., path=..., payload=..., content_type=..., now=...)` performs the same checks and returns `AdministrativeDecision(mission_id, expires_at, required_baseline_sha256)`. Its three scientific credit/completion flags are always false. It raises the existing `GateRejected` with a stable rejection code.

## Required live adapter integration

The gate itself has no network access. The actual mutation callback must obtain a fresh authenticated mission read immediately before PATCH. Extract the response's real mission UUID, exact description, and explicit private status. Do not fill missing fields from the expected values. Compute `administrative_baseline_digest(mission_id, description, private)` and compare it to the validated decision's `required_baseline_sha256`; abort on mismatch, non-private state, omitted fields, read error or uncertain identity. The helper accepts only `private is True` and canonical UUID text.

That digest is SHA256 of UTF-8 canonical JSON with sorted keys and compact separators:
`{"description": "<exact prior text>", "mission_id": "<actual UUID>", "private": true}`.

After the read, recheck release expiry immediately before transport, because the read may take time. Send the exact immutable method/path/payload/content type received from the guard. Do not reserialize, merge other fields, resolve a different mission, add a retry, or bypass the guard. A synthetic callback test demonstrates this pattern; it does not verify the real publisher's adapter. Reviewer acceptance of that actual adapter is a separate integration step.

Where the service supports a verified conditional update such as an entity-tag precondition, the adapter should use it to close concurrent changes between read and write. Without a service-side condition, a remaining read/write race exists; local checking does not create a distributed lock. Reusing the same release after successful append fails the live baseline check because the description has changed. The local guard alone is not an anti-replay mechanism.

## Records and trust

Every structured record is a strict JSON object with exactly one key, `administrative_gate`. Inside it, integer `schema_version: 1` and a `kind` identify the record. Unknown fields are rejected. Pins contain exactly an absolute `path` and lowercase SHA256 `sha256`. Duplicate JSON keys and non-finite numbers fail closed. Pinned files use the accepted evidence gate's 64 MiB read bound.

The authorization hash must come from an independently trusted owner/configuration, not from the candidate, publisher-generated acceptance or an automatically refreshed digest. Pin current canonical mission contract and basis paths so a changed file invalidates the release. The validator verifies bytes and declarations; it cannot decide whether these are the current authoritative documents or whether a replacement anchor is legitimate.

- **authorization:** `mission_id`, `author_id`, `reviewer_id`, `publisher_id`, pins `mission_contract`, `basis`, `baseline`, `appendix`, `payload`, `review`, `release`; `authorized_at`, `expires_at`, `required_baseline_sha256`.
- **baseline:** `mission_id`, `description`, explicit `private: true`, `observed_at`.
- **appendix:** plain UTF-8 bytes, starting with two newlines and containing nonempty prose.
- **payload:** exact outgoing UTF-8 JSON bytes with only `description`, equal as a string to baseline description plus appendix. No additional keys, deletion or replacement of prior text.
- **review:** `author_id`, `reviewer_id`, `publisher_id`, `mission_id`, same five pins `mission_contract`, `basis`, `baseline`, `appendix`, `payload`, `required_baseline_sha256`, `request`, `verdict: "accepted"`, `governance_only: true`, `prior_description_preserved: true`, `scientific_claims_added: false`, `reviewed_at`.
- **release:** `publisher_id`, `mission_id`, same `review` pin, `request`, `required_baseline_sha256`, `valid_from`, `expires_at`.

The review pin set is exactly the five named pins. Each `request` is exactly `{action, method, path, content_type, body_sha256}`. Action is `administrative_update`, method `PATCH`, route the exact approved mission UUID, content type exactly `application/json`. Content-type parameters, alternative JSON media types, query strings, encoded paths, other verbs and arbitrary endpoints are rejected. Outgoing serialization may vary only if those exact bytes are independently reviewed and pinned.

Chronology must satisfy baseline observed <= review completed <= authorized <= release starts <= current time < release expires <= authorization expires. Authorization duration is positive and at most 3600 seconds; use the tighter assigned work envelope when provisioning it. No allowance is created or renewed by these files.

The reviewer must differ from the author and match the independently named reviewer. IDs in a JSON file are not authentication. The reviewer accepts the exact appendix and outgoing bytes as governance-only. A preserved text prefix cannot guarantee unchanged rendered meaning: appended Markdown/HTML or misleading prose could reinterpret it. Human semantic and rendering review must assess that before acceptance. The guard neither reads papers nor invents consultations, premises, scientific proof acceptance or foundation credit.

## Verification and limits

Run `py -3 -B -m unittest discover -s tests -p test_administrative_publisher.py -v` from the checkout. Tests cover actual callback entry, altered current mission/basis and all evidence pins, different payloads, unreviewed claims, modified prior scientific text, public/implicit privacy, unrelated routes and media, wrong publisher, self-review, stale/future evidence, expiry, no retry, repeated validation and simulated live-baseline mismatch.

The module imports integrity helpers from the exact accepted `apf/evidence_gate.py`. Deploy it together with that accepted dependency. Direct HTTP, dishonest callbacks, altered code or caller-controlled anchors bypass this local guard. No actual HTTP, real identity authentication, installed publisher integration, second-box execution or platform-wide enforcement is established by the unit tests.
