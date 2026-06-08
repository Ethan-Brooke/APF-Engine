# W_TRACE Delta_r Symbolic Map Bank v1.0

Status: `[P_w_delta_r_symbolic_map]`.

This bank layer defines the symbolic finite-correction interface for the
`W_TRACE -> on-shell` route.  It is intentionally not a numerical evaluation of
`Delta_r` and not a physical W-mass export.

Closed here:

- selected route: `w_trace_on_shell_route`;
- preserved local input: `M_W_TRACE_GeV = 80.362164334`;
- allowed non-W numerical inputs inherited from v9.2:
  `alpha_em_reference`, `G_F_reference`, and `M_Z_on_shell_reference`;
- symbolic on-shell relation template:

```text
M_W^2 * (1 - M_W^2/M_Z^2)
  = pi*alpha_em/(sqrt(2)*G_F) * 1/(1 - Delta_r_symbolic)
```

- decomposed unevaluated `Delta_r` slots:
  `delta_alpha_running_slot`, `delta_rho_or_oblique_slot`,
  `vertex_box_finite_slot`, `bosonic_loop_finite_slot`,
  `fermionic_loop_finite_slot`, and `scheme_conversion_counterterm_slot`;
- forbidden inputs: observed physical `M_W`, W residuals, residual-fitted
  `Delta_r`, finite counterterms chosen to match observed `M_W`, and identity
  `W_TRACE -> physical M_W` transport.

Still open:

- numerical `Delta_r`;
- finite counterterm values;
- covariance/correlation propagation;
- uncertainty propagation;
- physical W/on-shell transport;
- physical scheme masses.

Targeted verifier:

```bash
python scripts/check_w_trace_delta_r_finite_map.py
```

Expected terminal string:

```text
W_TRACE_DELTA_R_SYMBOLIC_MAP_BANK_PASS
```
