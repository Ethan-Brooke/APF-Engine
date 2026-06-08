# W_TRACE Finite-Part Ledger Bank v1.0

Status: `[P_w_finite_part_ledger]`

This v9.4 module advances the W_TRACE on-shell route past the symbolic
`Delta_r` interface into an executable component ledger.  It closes the ledger
architecture for finite-part evaluation, computes the APF-anchor-implied
`Delta_r` target from W_TRACE plus the allowed non-W constants, and keeps all
physical export gates locked.

Closed here:

- finite-part component ledger schema;
- ordered component list for running, oblique, loop, vertex/box,
  counterterm, covariance, and uncertainty legs;
- APF-anchor Delta_r target computed from
  `alpha_em_reference`, `G_F_reference`, `M_Z_on_shell_reference`, and
  `M_W_TRACE_GeV = 80.362164334`;
- observed W mass, W world averages, W residuals, residual-fitted Delta_r,
  and target-tuned finite counterterms forbidden as inputs.

Not closed here:

- independent loop/counterterm finite-part evaluation;
- component-sum certificate against the APF-anchor Delta_r target;
- covariance and uncertainty propagation;
- physical on-shell W export;
- physical scheme mass vector export.

Master verifier:

```text
scripts/check_w_trace_finite_part_ledger.py
W_TRACE_FINITE_PART_LEDGER_BANK_PASS
```
