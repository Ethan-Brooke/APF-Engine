# W_TRACE Payload Fixture Bank v1.0

Status: `[P_w_payload_fixture]`

This bank adds the concrete payload-table harness for independent W_TRACE finite-part component values after the v9.7 numerical-source adapter. It does not ship independent numerical finite parts and does not close physical W/on-shell transport.

Closed now:

- component-aligned fixture rows for all eight W finite-part slots,
- table admission report discipline,
- duplicate/missing/unknown component rejection,
- anti-backsolve, anti-APF-target, and anti-observed-W guards,
- explicit declaration that the fixture is an empty admission harness.

Still open:

- actual independently sourced finite-part numerical payloads,
- component-sum certificate against the APF-anchor Delta_r comparison target,
- covariance and uncertainty propagation,
- physical W/on-shell export.

Master verifier:

```text
scripts/check_w_trace_payload_fixture.py
W_TRACE_PAYLOAD_FIXTURE_BANK_PASS
```
