# v44 charged-lepton QED covariance and running-codomain gate

Status: `CHARGED_LEPTON_QED_COVARIANCE_RUNNING_CODOMAIN_PASS`.

v44 closes the covariance-admission gate for the charged-lepton pole/reference codomain. The APF envelope is

`epsilon_QED_APF = 1/5063`, so the percent envelope is `0.019751135690%`.

The v43 diagnostic residuals were:

- e: `+0.000721290823%`
- mu: `-0.000124471588%`
- tau: `-0.000741052916%`

The largest residual is `0.000741052916%`, only `0.037519509161` of the APF envelope. All three components are inside the predeclared APF covariance envelope.

Promotion:

`charged leptons: P_export_candidate^pole_v43 + P_covariance_admitted^APF_envelope / QED_running_open`.

This does **not** claim final physical charged-lepton masses, QED-running masses, zero residual, or a target-fitted covariance. The running codomain is typed but still needs `U_QED`, alpha/threshold/loop-order conventions, and numeric covariance.

Next theorem: `APF_CHARGED_LEPTON_QED_RUNNING_TRANSPORT_THEOREM`.
