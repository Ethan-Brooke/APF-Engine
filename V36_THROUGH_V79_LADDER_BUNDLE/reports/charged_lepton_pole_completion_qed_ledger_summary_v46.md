# v46 charged-lepton pole completion and QED ledger theorem

Status: `CHARGED_LEPTON_POLE_COMPLETION_AND_QED_LEDGER_THEOREM_PASS`.

v46 closes the charged-lepton APF pole-codomain route as an envelope-admitted completion theorem.  The source vector, residual operator, count coefficients, scalar count normalization, covariance envelope, and QED route boundary are all now typed and banked.

Pole-codomain vector:

`(0.511002635789, 105.658243985342, 1776.916832008411) MeV`.

Diagnostic residuals versus supplied pole references:

`(+0.000721290823%, -0.000124471588%, -0.000741052916%)`.

APF QED covariance envelope:

`epsilon_QED_APF = 1/5063`, i.e. `0.019751135690302%`.

Maximum residual/envelope:

`0.037519509162 < 1`.

Promotion:

`charged leptons: P_pole_completion^APF_envelope + P_QED_route_typed / numeric_running_ledger_external`.

Completion means: no APF-side source/operator/coefficient/scalar/covariance gate remains open for the pole-codomain branch.

Completion does not mean: exact equality to pole masses, final QED-running masses, final physical masses, or a target-selected QED cleanup.

Next theorem, only if desired: `APF_CHARGED_LEPTON_EXTERNAL_QED_LEDGER_IMPORT_AND_NUMERIC_RUNNING_EVALUATION`.
