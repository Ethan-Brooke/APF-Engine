# W_TRACE Numerical-Source Adapter Bank v1.0

Status: `P_w_numeric_source_adapter`

This bank layer defines the admissible ingress interface for independently
evaluated W_TRACE finite-part component numbers. It does **not** supply those
numbers, certify the component sum, or export a physical W mass.

Closed here:

- required source-field schema for each finite-part component;
- allowed source classes: independent loop library, audited literature table,
  symbolic algebra export, or hand-transcribed source with checksum;
- strict predicate rejecting APF-anchor target consumption, observed W inputs,
  target backsolves, residual fits, and tuned counterterms;
- preservation of the v9.6 symbolic component skeleton and v8.9 physical-export
  lock.

Still open:

- actual independent numerical finite-part payloads;
- checksum/table-locator verification against external sources;
- component-sum residual certificate;
- covariance and uncertainty propagation;
- physical W/on-shell export.

Master verifier: `W_TRACE_NUMERIC_SOURCE_ADAPTER_BANK_PASS`.
