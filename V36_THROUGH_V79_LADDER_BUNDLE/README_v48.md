# APF v48 — Charged-Lepton Full QED Running Ledger and Covariance Evaluation

Status stamp: `CHARGED_LEPTON_FULL_QED_RUNNING_LEDGER_AND_COVARIANCE_EVALUATION_PASS`.

Main theorem file:

- `paper/CHARGED_LEPTON_FULL_QED_RUNNING_LEDGER_AND_COVARIANCE_EVALUATION_v48.tex`

Verifier:

```bash
python scripts/check_charged_lepton_full_qed_running_ledger_covariance_v48.py
```

Main results:

- Keeps the official CODATA 2022 ledger imported in v47.
- Promotes QED from an LO numeric witness to a typed full-running ledger.
- Evaluates the perturbative truncation scale `100*(alpha/pi)^2 = 0.000539549026324%`.
- Combines the APF envelope and declared QED truncation scale into `0.019758503845396%`.
- Confirms all CODATA-ledger residuals remain inside that non-fit covariance envelope.

Claimed:

- `P_QED_truncation_covariance_admitted`
- `P_full_QED_running_ledger_typed`

Not claimed:

- final multi-loop QED-running masses
- final physical charged-lepton masses
- zero residual
- CODATA metrological-sigma agreement for every lepton
- target-selected alpha, scale, loop order, threshold convention, covariance, or free generation factors

Next theorem: `APF_CHARGED_LEPTON_FULL_QED_NUMERIC_RUNNING_WITH_DECLARED_EXTERNAL_COEFFICIENT_LEDGER`.
