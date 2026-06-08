# W_TRACE Counterterm Convention Certificate Bank v1.0

This bank adds the on-shell finite counterterm convention certificate for the W_TRACE -> on-shell route.

Closed in this layer:

- the required on-shell counterterm-convention schema;
- the mapping of the counterterm convention to the `Delta_r_ct_OS` component slot;
- mass, charge, mixing-angle, tadpole, gauge, finite-normalization, and no-smuggling clauses;
- explicit rejection of observed W mass, W world average, W residuals, APF-anchor Delta_r backsolves, post-hoc residual fits, tuned finite counterterms, and identity transport.

Not closed in this layer:

- numerical counterterm finite values;
- independent finite-part payload rows;
- component-sum certification;
- covariance and uncertainty propagation from admitted rows;
- physical W/on-shell export.

Master verifier:

```text
scripts/check_w_trace_counterterm_convention.py
W_TRACE_COUNTERTERM_CONVENTION_BANK_PASS
```
