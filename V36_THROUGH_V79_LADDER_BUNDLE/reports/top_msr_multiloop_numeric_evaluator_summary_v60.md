# APF v60 — Top MSR Multiloop Numeric Evaluator Implementation

Stamp: `TOP_MSR_MULTILOOP_NUMERIC_EVALUATOR_IMPLEMENTATION_PASS`

Closed status:

`P_LO_numeric_evaluator_closed_fail_closed_multiloop_boundary`

The package implements a runnable evaluator with a fail-closed coefficient protocol. It reproduces the v58 LO pole witness:

- m_t^MSR(R*) = 168.169055793800 GeV
- R* = 85.857222698385 GeV
- alpha_s(R*) one-loop = 0.119032308653252
- Delta m_LO = 4.337410801564 GeV
- m_t^pole,LO witness = 172.506466595364 GeV
- residual vs audit-only PDG direct top average = -0.053533404636 GeV

It refuses L>=2 unless explicit sourced coefficients are supplied. This closes the evaluator implementation boundary, not the full physical-final top mass.
