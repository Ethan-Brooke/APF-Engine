# W_TRACE Delta_r Source Mapping Bank v13.1

Status: `P_w_delta_r_source_mapping`.

This is the first post-infrastructure physics-pivot bank.  It changes the W_TRACE payload strategy from APF eight-slot acquisition first to standard electroweak Delta_r source acquisition first.

## Standard source schema

The bank accepts either:

1. `standard_delta_r_total`, a reviewed independent value of total `Delta_r`;
2. `standard_delta_r_decomposition`, using
   `Delta_r = Delta_alpha - (cW2/sW2) Delta_rho + Delta_r_rem`; or
3. `standard_delta_r_parametrization`, a reviewed parametrization/evaluator that can output independent total `Delta_r` under the declared input scheme.

## APF comparison role

The APF anchor

```text
Delta_r_APF_TRACE_target = 0.0364075266128216881
M_W_TRACE_GeV            = 80.362164334
```

is comparison-only.  It is not a component value, not a backsolve target, and not an import input.

## Strategy shift

The eight legacy APF finite-part slots remain available for later refinement, but they are no longer a prerequisite for admitting a standard independent Delta_r source.  We ingest standard electroweak Delta_r first, then decompose into APF slots only when a source supports that decomposition.

## Still locked

Physical W export remains disabled.  Real reviewed external finite-part/source payloads, component-sum certification, covariance/uncertainty propagation, and physical W export remain open.
