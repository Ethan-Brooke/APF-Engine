# APF v38 Charged-Lepton Generation Residual Operator Theorem

Status: `CHARGED_LEPTON_RESIDUAL_OPERATOR_FORM_PASS`.

This package does **not** claim charged-lepton physical export. It closes the operator-form part of the charged-lepton obstruction: scalar normalization by `1/sqrt(6)` cannot carry generation-dependent residuals, so the route requires a generation-typed residual operator. APF's ordered three-rung generation ladder forces the minimal positive form

`R_l(alpha,beta) = exp(alpha H1 + beta H2)`,

with `H1 = diag(-1,0,1)` and `H2 = diag(1,-2,1)`.

Remaining gate: derive `alpha` and `beta` from APF generation-interface data without using electron, muon, or tau target masses.
