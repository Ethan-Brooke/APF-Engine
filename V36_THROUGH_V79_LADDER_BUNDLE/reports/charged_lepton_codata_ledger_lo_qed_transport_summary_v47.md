# v47 Charged-Lepton CODATA Ledger and LO QED Transport Summary

Status: `CHARGED_LEPTON_CODATA_LEDGER_AND_LO_QED_TRANSPORT_PASS`

## CODATA 2022 ledger import

- alpha^-1 = 137.035999177000 +/- 0.000000021000
- alpha = 0.007297352564331424
- CODATA charged-lepton references (MeV): [0.51099895069, 105.6583755, 1776.86]
- CODATA uncertainties (MeV): [1.6e-10, 2.3e-06, 0.12]

## Re-audit of v43/v46 pole vector

Phi_l^v43 = [0.5110026357885311, 105.658243985342, 1776.9168320084111] MeV

Relative residuals against CODATA 2022:

- e: 0.000721155792%
- mu: -0.000124471588%
- tau: 0.003198451674%

APF envelope: 100/5063 = 0.019751135690302%

Max residual/envelope = 0.161937608245 < 1.

Conclusion: charged-lepton pole completion survives official CODATA 2022 ledger import.

Important honesty boundary: this is APF-envelope admission, not CODATA metrological-sigma agreement for every lepton.

## LO QED numeric transport witness

Formula:

mbar_i^LO(mu_i=m_i) = Phi_i^v43/(1+alpha/pi)

Factor: 0.997682563522362

LO running witness (MeV):

- e: 0.509818419640
- mu: 105.413387716567
- tau: 1772.798940124186

Claimed: `P_LO_QED_numeric_transport_witness`.

Not claimed: final QED-running masses, final physical masses, zero residual, or target-fitted QED cleanup.

Next theorem: `APF_CHARGED_LEPTON_FULL_QED_RUNNING_LEDGER_AND_COVARIANCE_EVALUATION`.
