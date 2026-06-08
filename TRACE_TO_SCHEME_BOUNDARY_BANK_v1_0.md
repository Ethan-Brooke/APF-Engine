# Trace-to-Scheme Transport Boundary Bank v1.0

## Status

```text
TRACE_TO_SCHEME_BOUNDARY_BANK_PASS
```

This bundle promotes the trace-to-scheme layer from a pre-bank scaffold to a bank-registered boundary package.

It does **not** close physical mass transport.

Closed upstream:

```text
APF_TRACE / W_TRACE local trace-sector closure
```

Bank-staged here:

```text
APF_TRACE / W_TRACE -> physical reporting scheme S(mu)
```

Open after this bundle:

```text
Trace-to-Scheme Transport Theorem
```

## New module

```text
apf/trace_scheme_transport.py
```

## Targeted verifier

```text
scripts/check_trace_to_scheme_transport.py
```

Expected targeted output:

```text
TRACE_TO_SCHEME_BOUNDARY_BANK_PASS
```

## New bank checks

```text
check_T_trace_scheme_boundary_declared
check_T_trace_codomain_immutability
check_T_trace_to_scheme_inputs_separated
check_T_scheme_target_contract_declared
check_T_colored_qcd_transport_branch_separated
check_T_lepton_ew_qed_transport_branch_separated
check_T_identity_map_to_physical_scheme_forbidden
check_T_external_constants_ledger_required
check_T_no_physical_mass_inverse_fit
check_T_trace_to_scheme_boundary_bank_closure
```

## Boundary protected

The module forbids:

```text
APF_TRACE == physical reporting mass identity
post-hoc scalar fitted to physical mass vector
PDG/MSbar/pole/lattice/MC masses as inverse normalization inputs
silent scheme comparison without declared S(mu)
```

The module requires future transport to declare:

```text
target scheme S
reference scale mu or scheme convention
EW/Yukawa running map
QED running map where applicable
QCD running and threshold matching for colored fermions
counterterm convention
external constants ledger with uncertainties
uncertainty propagation and comparison protocol
```

## Correct claim language

```text
(m_f)^APF_TRACE : [P_local]
Trace-to-scheme boundary discipline : [P_boundary]
(m_f)^physical : open transport theorem
```
