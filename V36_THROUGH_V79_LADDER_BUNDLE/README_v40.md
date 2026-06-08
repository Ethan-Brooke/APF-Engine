# APF v40 — Charged-Lepton Trace-Vector Source Gate

This package extends v39. It banks the charged-lepton trace-vector source gate and QED codomain declaration.

Run:

```bash
python scripts/check_trace_to_scheme_export_v35.py
python scripts/check_top_msr_scale_selection_v37.py
python scripts/check_charged_lepton_residual_operator_v38.py
python scripts/check_charged_lepton_coefficient_closure_v39.py
python scripts/check_charged_lepton_trace_vector_source_gate_v40.py
```

Expected new stamp:

```text
CHARGED_LEPTON_TRACE_VECTOR_SOURCE_GATE_PASS
```

Important: v40 does **not** claim charged-lepton physical export. It declares the pole codomain and proves the source-gate obstruction: the numeric APF trace vector `T_l` must be supplied by an APF-native trace theorem or by closing `Omega_l`, not by inverting the physical charged-lepton masses.
