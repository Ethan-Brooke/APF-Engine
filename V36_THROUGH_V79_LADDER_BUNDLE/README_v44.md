# APF v44 — Charged-Lepton QED Covariance and Running-Codomain Gate

Status stamp: `CHARGED_LEPTON_QED_COVARIANCE_RUNNING_CODOMAIN_PASS`.

Main theorem file:

- `paper/CHARGED_LEPTON_QED_COVARIANCE_AND_RUNNING_CODOMAIN_THEOREM_v44.tex`

Verifier:

```bash
python scripts/check_charged_lepton_qed_covariance_running_codomain_v44.py
```

Main result:

- `epsilon_QED_APF=1/5063`
- max v43 residual = `0.000741052916%`
- APF envelope = `0.019751135690%`
- max residual/envelope = `0.037519509161`

Claimed:

- charged leptons are `P_export_candidate^pole_v43 + P_covariance_admitted^APF_envelope / QED_running_open`.

Not claimed:

- final charged-lepton physical masses
- QED-running final masses
- zero residual
- target-fitted covariance

Next theorem: `APF_CHARGED_LEPTON_QED_RUNNING_TRANSPORT_THEOREM`.
