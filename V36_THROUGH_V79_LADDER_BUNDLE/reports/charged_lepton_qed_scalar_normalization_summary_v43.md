# v43 charged-lepton QED scalar normalization and count-source witness

Status: `CHARGED_LEPTON_QED_SCALAR_NORMALIZATION_COUNT_SOURCE_PASS`.

v43 adds the scalar APF-count witness

`eta0 = 1/5063`, with `5063 = K_SM*(K_SM+K_c+K_b+N_gen) = 61*(61+16+3+3)`.

Together with v42's generation-shape witness,

`Z_l^v43 = exp((1/5063) I + (1/28) H1 + (3/584) H2)`.

Predicted scalar-normalized vector:

- e: `0.511002635789` MeV
- mu: `105.658243985342` MeV
- tau: `1776.916832008411` MeV

Diagnostic residuals versus supplied pole references:

- e: `+0.000721291%`
- mu: `-0.000124472%`
- tau: `-0.000741053%`

The max absolute residual drops from v42's `0.020490092%` to `0.000741053%`, a factor `27.65` improvement.

This does **not** claim final physical charged-lepton masses, QED running closure, zero residual, or a target-fitted scalar. The inverse scalar coefficient is quarantined as diagnostic-only.

Next theorem: `APF_CHARGED_LEPTON_QED_COVARIANCE_AND_RUNNING_CODOMAIN_THEOREM`.
