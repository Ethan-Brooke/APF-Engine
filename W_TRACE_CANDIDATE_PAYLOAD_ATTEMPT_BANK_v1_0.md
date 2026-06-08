# W_TRACE Candidate Payload Admission-Attempt Bank v1.0

Codebase layer: v10.3.

This bank adds the first explicit admission-attempt state machine above the
v10.2 real-source candidate gate.  It does not ship real external numerical
finite-part rows.  It closes the admission/failure certificate, the dry-path
admission logic, and the physical-export lock.

Closed status:

```text
[P_w_candidate_payload_attempt_gate]
```

Still open:

```text
actual shipped real external finite-part rows
component-sum certificate
covariance / uncertainty propagation
physical W/on-shell export
```

The APF-anchor Delta r target and observed physical W measurements remain
forbidden as source inputs.
