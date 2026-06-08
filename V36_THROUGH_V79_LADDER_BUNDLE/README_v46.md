# APF v46 — Charged-Lepton Pole Completion and QED Ledger Theorem

Status stamp: `CHARGED_LEPTON_POLE_COMPLETION_AND_QED_LEDGER_THEOREM_PASS`.

Main theorem file:

- `paper/CHARGED_LEPTON_POLE_COMPLETION_AND_QED_LEDGER_THEOREM_v46.tex`

Verifier:

```bash
python scripts/check_charged_lepton_pole_completion_qed_ledger_v46.py
```

Main result:

- Charged leptons are complete at the APF pole-codomain/envelope level.
- The pole vector is `(0.511002635789, 105.658243985342, 1776.916832008411) MeV`.
- The max residual is inside the predeclared APF QED envelope `epsilon_QED_APF=1/5063`.
- The QED running route remains typed, but numerical running requires an external constants/covariance ledger.

Claimed:

- `charged leptons: P_pole_completion^APF_envelope + P_QED_route_typed / numeric_running_ledger_external`.

Not claimed:

- final QED-running charged-lepton masses
- final physical charged-lepton masses
- exact equality / zero residual
- target-selected scale, loop order, threshold convention, covariance, or free generation factors

Next theorem: `APF_CHARGED_LEPTON_EXTERNAL_QED_LEDGER_IMPORT_AND_NUMERIC_RUNNING_EVALUATION`.
