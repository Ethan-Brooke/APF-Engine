# APF v41 charged-lepton trace-vector closure summary

Status: `CHARGED_LEPTON_TRACE_VECTOR_CLOSURE_PASS`.

v41 closes the v40 source gate by deriving the charged-lepton APF trace vector from the down-family APF_TRACE source:

```text
T_l = diag(1/3,3,1) T_d
T_d = (0.003870916422334, 0.087143281633652, 4.1774904559271) GeV
T_l = (0.001290305474111, 0.261429844900956, 4.1774904559271) GeV
```

The leading pole route is:

```text
Phi_l^pole,LO = (1/sqrt(6)) T_l
              = (0.526765004, 106.728287, 1705.453337) MeV
```

Diagnostic pole residuals, using external pole values only after the route is fixed:

```text
e:   +3.085340%
mu:  +1.012614%
tau: -4.022481%
```

Promotion:

```text
charged leptons: P_source_gate^T_l + P_codomain^pole_ready
              -> P_export_candidate^pole_LO
```

Not claimed: final physical charged-lepton masses, QED-running final export, zero residual, or fitted precision.

Next theorem: `APF_CHARGED_LEPTON_QED_RESIDUAL_TRANSPORT_THEOREM`.
