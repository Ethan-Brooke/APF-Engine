# APF v41 — Charged-Lepton Trace-Vector Closure

This package extends v40. It closes the charged-lepton APF trace-vector source gate by deriving

```text
T_l = diag(1/3,3,1) T_d
```

from the APF down-family trace source. It then supplies the leading pole route

```text
Phi_l^pole,LO = (1/sqrt(6)) T_l
```

Status stamp:

```text
CHARGED_LEPTON_TRACE_VECTOR_CLOSURE_PASS
```

Important: v41 claims only `P_export_candidate^pole_LO`. It does **not** claim final physical charged-lepton masses, QED-running export, zero residuals, or fitted precision. The external pole comparison is diagnostic only and is performed after the APF source and route are fixed.

Run:

```bash
python scripts/check_trace_to_scheme_export_v35.py
python scripts/check_top_msr_scale_selection_v37.py
python scripts/check_charged_lepton_residual_operator_v38.py
python scripts/check_charged_lepton_coefficient_closure_v39.py
python scripts/check_charged_lepton_trace_vector_source_gate_v40.py
python scripts/check_charged_lepton_trace_vector_closure_v41.py
```
