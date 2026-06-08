# W_TRACE Final Export Readiness Aggregator Bank v1.0

Status: `P_w_final_export_readiness_aggregator`.

This bank closes the readiness roll-up for the W_TRACE on-shell route.  It does
not export a physical W mass.  It collects the row-bundle admission state,
component-sum bridge, covariance bridge, uncertainty harness, counterterm
convention certificate, and physical export lock into one terminal readiness
predicate.

The shipped state is intentionally locked:

```text
real row bundle admitted: false
component sum certified: false
covariance certified: false
uncertainty propagation certified: false
physical W export enabled: false
```

The counterterm convention and target scheme contracts are banked as structural
prerequisites, but real finite-part rows and their numerical covariance remain
open.  The APF anchor \(\Delta r\) and W_TRACE mass are comparison anchors only;
they are not component inputs.
