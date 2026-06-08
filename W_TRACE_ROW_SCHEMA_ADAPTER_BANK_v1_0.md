# W_TRACE Row Schema Adapter Bank v1.0

Status: `P_w_row_schema_adapter`

This bank layer closes the row-level schema for admitting independently sourced W_TRACE finite-part component values, including the `Delta_r_ct_OS` counterterm row governed by the v10.7 on-shell counterterm-convention certificate.

It deliberately does **not** admit real finite-part numerical rows, certify the component sum, propagate covariance, or release physical W export.

## Closed here

- Required row-field contract for all eight finite-part components.
- Component-order and component-symbol preservation against the v9.6 skeleton.
- Dimensionless `Delta r` component units.
- Nonnegative finite uncertainties.
- Finite numeric value shape.
- On-shell convention identity and `Delta_r_ct_OS` counterterm adapter.
- Row-level anti-smuggling predicates for observed W inputs, APF-anchor backsolve, residual-fit columns, post-hoc counterterm fits, and physical-export requests.

## Still open

- Real finite-part numerical values.
- Counterterm numerical value admission.
- Component-sum certificate.
- Covariance and uncertainty propagation from real rows.
- Physical W/on-shell export.

Master result: `W_TRACE_ROW_SCHEMA_ADAPTER_BANK_PASS`.
