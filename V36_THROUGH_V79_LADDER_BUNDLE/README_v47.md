# APF v47 — Charged-Lepton CODATA Ledger and LO QED Transport

Status stamp: `CHARGED_LEPTON_CODATA_LEDGER_AND_LO_QED_TRANSPORT_PASS`.

Main theorem file:

- `paper/CHARGED_LEPTON_CODATA_LEDGER_AND_LO_QED_TRANSPORT_THEOREM_v47.tex`

Verifier:

```bash
python scripts/check_charged_lepton_codata_ledger_lo_qed_transport_v47.py
```

Main results:

- CODATA 2022 ledger import: imports an external CODATA 2022/NIST constants ledger for alpha and charged-lepton diagnostic references.
- Re-audits the v43/v46 pole vector against CODATA 2022 values.
- The CODATA 2022 residuals remain inside the APF envelope `100/5063 = 0.019751135690302%`.
- Evaluates a declared leading-order frozen-alpha QED running witness:
  `(0.509818419640, 105.413387716567, 1772.798940124186) MeV`.

Claimed:

- `P_pole_completion^APF_envelope_CODATA2022_survives`
- `P_LO_QED_numeric_transport_witness`

Not claimed:

- final multi-loop QED-running masses
- final physical charged-lepton masses
- zero residual
- CODATA metrological-sigma agreement for every lepton
- target-selected alpha, scale, loop order, threshold convention, covariance, or free generation factors

Next theorem: `APF_CHARGED_LEPTON_FULL_QED_RUNNING_LEDGER_AND_COVARIANCE_EVALUATION`.
