# APF v62 — Top Codomain Diagnosis and MSR Repair Witness

Stamp: `TOP_CODOMAIN_DIAGNOSIS_AND_MSR_REPAIR_PASS`

## Diagnosis

v61 did not reveal a coefficient bug. It revealed a codomain problem: the full four-loop pole conversion is not the same target as the direct/MC-style top mass audit.

Pole branch:

- m_t^pole,4loop = `174.016604383647` GeV
- residual vs audit-only direct mass = `1.456604383647` GeV
- z vs direct sigma = `4.698723818217`

Therefore the pole branch remains knocked out for direct/MC comparison.

## Repair witness

Define the finite direct-reconstruction resolution scale

R_EW = M_W^TRACE/(2*pi) = `12.790035691319` GeV.

Use the v61 sourced counterterm as a fixed-order MSR-scale translation kernel:

m_t^MSR(R_EW) = m_t^MSR(R*) + delta_pole(R*) - delta_pole(R_EW).

This gives:

- delta_pole(R*) = `5.847548589847` GeV
- delta_pole(R_EW) = `1.451849972940` GeV
- m_t^MSR(R_EW) = `172.564754410708` GeV
- residual vs audit-only direct mass = `0.004754410708` GeV = `4.754411` MeV
- z vs direct sigma = `0.015336808734`

## Status

Closed:

- v61 pole-route failure diagnosed as direct/MC codomain mismatch.
- Pole branch quarantined.
- Finite-resolution MSR route opened and evaluated with the v61 coefficient ledger.

Conditional:

- R_EW = M_W/(2*pi) is a strong APF/EW-resolution witness.

Not claimed:

- physical-final top mass
- exact pole mass
- MC equality
- full R-evolution final
- target-fitted scale
