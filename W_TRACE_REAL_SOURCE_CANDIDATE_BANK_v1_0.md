# W_TRACE Real External Source Candidate Bank v1.0

This bank layer defines the first real-candidate admission gate for W_TRACE finite-part external source packs.

It closes only the candidate-pack admission and absence/failure certificate. It does not ship real finite-part numerical rows, does not certify a component sum, does not propagate covariance or uncertainty, and does not export a physical W mass.

Closed status:

```text
[P_w_real_source_candidate_gate]
```

Master verifier:

```text
scripts/check_w_trace_real_source_candidate.py
W_TRACE_REAL_SOURCE_CANDIDATE_BANK_PASS
```

The shipped state is intentionally empty:

```text
real_external_candidate_rows_supplied = False
real_external_candidate_rows_admitted = False
component_sum_certified = False
physical_W_transport_closed = False
exports_physical_M_W = False
```

Forbidden candidate inputs include observed W mass columns, W world-average columns, fit residual columns, APF-anchor Delta-r target columns, and any component-sum residual chosen to close the APF target.
