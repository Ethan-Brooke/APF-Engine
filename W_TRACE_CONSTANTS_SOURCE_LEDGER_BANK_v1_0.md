# W_TRACE Constants-Source Ledger Bank v1.0

Status: `P_w_constants_source_ledger`.

This bank layer fills the allowed non-W electroweak numerical input ledger for
the W_TRACE -> on-shell route selected in v9.0 and symbolically gated in v9.1.

Closed here:

- source-tagged numerical record for `alpha_em_reference` using the NIST/CODATA
  2022 inverse fine-structure constant;
- source-tagged numerical record for `G_F_reference` using the PDG 2024
  electroweak review Fermi-constant convention;
- source-tagged numerical record for `M_Z_on_shell_reference` using the PDG 2024
  Z-boson listing / LEP Z convention;
- unit, uncertainty, source URL, convention, and W-exclusion fields for each
  record;
- explicit exclusion of observed `M_W`, W residuals, residual-fitted `Delta_r`,
  and identity transport.

Still open:

- `Delta_r` / finite electroweak correction;
- counterterm finite parts;
- covariance/correlation propagation;
- uncertainty propagation;
- physical W export;
- physical scheme masses.

Passing command:

```bash
python scripts/check_w_trace_constants_source_ledger.py
```

Expected sentinel:

```text
W_TRACE_CONSTANTS_SOURCE_LEDGER_BANK_PASS
```
