# W_TRACE Import Session Replay Bank v1.0

Status: `[P_w_import_session_replay_validator]`.

This bank adds the replay and reproducibility validator above the v11.9 reviewed payload import session log. It does not ship real finite-part rows, does not admit real rows, and does not export a physical W/on-shell value.

## What is banked

- replay record schema
- replay states: `NO_REPLAY_SESSION`, `SESSION_LOG_NOT_PROMOTED`, `PAYLOAD_MISSING`, `DIGEST_MISMATCH`, `REPLAYABLE_DRYRUN`, `REAL_PAYLOAD_REPLAY_RECORDED_NOT_ADMITTED`, `BLOCKED_PHYSICAL_EXPORT_REQUEST`
- payload SHA-256 recomputation against the session-log digest
- digest-mismatch failure certificate
- missing-payload failure certificate
- physical-export request rejection
- anti-smuggling token scan
- preservation of the W_TRACE final export lock

## Boundary

The APF/W trace route remains locked:

```text
real_replay_session_shipped = False
real_replay_session_validated = False
real_external_rows_imported = False
real_external_rows_admitted = False
component_sum_certified = False
covariance_certified = False
uncertainty_propagation_certified = False
physical_W_export_enabled = False
exports_physical_M_W = False
```

physical W/on-shell export remains OPEN.
