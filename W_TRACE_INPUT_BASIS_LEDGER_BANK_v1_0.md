# W_TRACE Input-Basis Ledger Bank v1.0

Status: `[P_w_input_basis_ledger]`

This bank layer selects the W_TRACE -> on-shell input-basis ledger after the
v9.0 W_TRACE on-shell contract bank.

Closed here:

- selected input-basis family: `on-shell alpha/M_Z/G_F-style input basis`;
- symbolic allowed inputs: `alpha_em_reference`, `G_F_reference`,
  `M_Z_on_shell_reference`;
- unevaluated finite electroweak radiative slot: `Delta_r_finite_EW_correction_slot`;
- provenance, uncertainty, and correlation metadata requirements;
- symbolic terminal relation template;
- explicit exclusion of observed physical `M_W`, W residuals, residual-fitted
  knobs, and identity transport.

Not closed here:

- no numerical EW constants are filled;
- no finite radiative correction / `Delta_r` is evaluated;
- no uncertainty propagation is evaluated;
- no physical W mass is exported.

Master verifier:

```bash
python scripts/check_w_trace_input_basis_ledger.py
```

Expected result:

```text
W_TRACE_INPUT_BASIS_LEDGER_BANK_PASS
```
