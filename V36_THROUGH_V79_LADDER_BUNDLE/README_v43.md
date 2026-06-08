# APF v43 — QED Scalar Normalization and Count-Source Witness

Adds a charged-lepton scalar normalization witness to the v42 residual-shape theorem.

Status: `CHARGED_LEPTON_QED_SCALAR_NORMALIZATION_COUNT_SOURCE_PASS`.

Main theorem file:

- `paper/CHARGED_LEPTON_QED_SCALAR_NORMALIZATION_AND_COUNT_SOURCE_v43.tex`

Run targeted verifier:

```bash
python scripts/check_charged_lepton_qed_scalar_normalization_v43.py
```

Inherited verifiers remain available:

```bash
python scripts/check_trace_to_scheme_export_v35.py
python scripts/check_top_msr_scale_selection_v37.py
python scripts/check_charged_lepton_residual_operator_v38.py
python scripts/check_charged_lepton_coefficient_closure_v39.py
python scripts/check_charged_lepton_trace_vector_source_gate_v40.py
python scripts/check_charged_lepton_trace_vector_closure_v41.py
python scripts/check_charged_lepton_qed_residual_witness_v42.py
```

Closed here:

- v42 generation-shape witness retained: `eta1=1/28`, `eta2=3/584`.
- v43 scalar count witness added: `eta0=1/5063`.
- Charged-lepton pole-codomain diagnostic residuals reduced below `1e-3%`.
- No-smuggling audit keeps inverse scalar coefficient diagnostic-only.

Not claimed: final charged-lepton physical masses, QED running finality, zero residual, or target-fitted scalar normalization.
