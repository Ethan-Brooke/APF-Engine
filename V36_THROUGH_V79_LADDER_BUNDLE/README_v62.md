# APF v62 — Top Codomain Diagnosis and MSR Repair

Stamp: `TOP_CODOMAIN_DIAGNOSIS_AND_MSR_REPAIR_PASS`

## Core diagnosis

v61 was not a coefficient bug. The sourced four-loop pole conversion is real, but it is the wrong codomain for auditing a direct/MC-style top mass.

The v61 pole branch remains knocked out:

- m_t^pole,4loop = `174.016604383647` GeV
- residual vs direct audit = `1.456604383647` GeV
- z = `4.698723818217`

## Repair witness

Keep the route in the short-distance MSR family and translate from R* to an EW-resolution reconstruction scale:

R_EW = M_W^TRACE/(2*pi) = `12.790035691319` GeV.

Using the v61 four-loop counterterm as a fixed-order scale-translation kernel:

m_t^MSR(R_EW) = `172.564754410708` GeV.

Residual vs audit-only direct mass 172.56 ± 0.31 GeV:

- residual = `0.004754410708` GeV = `4.754411` MeV
- z = `0.015336808734`

## Status

Closed:
- codomain diagnosis
- pole branch quarantine
- finite-resolution MSR witness evaluation

Conditional:
- R_EW theorem / MC calibration ledger still needed for finality

Not claimed:
- physical-final top mass
- exact pole mass
- MC equality
- target-fitted scale
- full R-evolution final
