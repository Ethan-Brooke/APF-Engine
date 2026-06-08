# APF v39 — Charged-Lepton Coefficient Closure Theorem

Status: `CHARGED_LEPTON_COEFFICIENT_CLOSURE_PASS`.

Builds on:
- v35 Trace-to-Scheme Export Theorem
- v36 APF derivation of G1--G6
- v37 Top MSR scale-selection theorem
- v38 Charged-lepton residual operator-form theorem

New closure:

```text
R_l(alpha,beta)=exp(alpha H1 + beta H2)
alpha = 0.5 log(N_c)
beta  = -0.5 log(N_c)
N_c = 3
R_l = diag(1/3, 3, 1)
```

Promotion:

```text
charged leptons: P_route^operator_form -> P_route^coefficient_closed
```

Not claimed: charged-lepton physical export, final electron/muon/tau masses, or target-mass fitting.

Next theorem: `APF_CHARGED_LEPTON_TRACE_VECTOR_AND_QED_SCHEME_EXPORT_THEOREM`.
