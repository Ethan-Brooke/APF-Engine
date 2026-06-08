# APF v45 — Charged-Lepton QED Running Transport Theorem

Status stamp: `CHARGED_LEPTON_QED_RUNNING_TRANSPORT_THEOREM_PASS`.

Main theorem file:

- `paper/CHARGED_LEPTON_QED_RUNNING_TRANSPORT_THEOREM_v45.tex`

Verifier:

```bash
python scripts/check_charged_lepton_qed_running_transport_v45.py
```

Main result:

- QED running route form closed symbolically: `U_QED^{S_pole_to_S_run}(L_QED; Phi_l_v43)`.
- Admitted source: APF v43 pole-codomain vector only.
- External constants/covariance ledger required before numerical running export.

Claimed:

- charged leptons are `P_running_route_form^QED + P_constants_ledger_required / numeric_QED_running_open`.

Not claimed:

- final QED-running charged-lepton masses
- final physical charged-lepton masses
- zero residual
- target-selected scale, loop order, threshold convention, or free generation factors

Next theorem: `APF_CHARGED_LEPTON_QED_CONSTANTS_LEDGER_AND_NUMERIC_RUNNING_THEOREM`.
