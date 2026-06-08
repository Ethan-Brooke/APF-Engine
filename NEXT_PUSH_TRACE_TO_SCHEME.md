# Next Push: Trace-to-Scheme Transport

## Current position

Trace-sector closure is banked locally:

```text
APF_TRACE / W_TRACE : [P_local]
```

The trace-to-scheme layer is now bank-staged as a boundary contract:

```text
TRACE_TO_SCHEME_BOUNDARY_BANK_PASS
```

This does not export physical masses.

## What is open

The next theorem must construct a declared transport map:

```text
m_f^APF_TRACE -> m_f^S(mu)
```

where `S` is an explicit reporting scheme such as:

```text
MSbar(mu)
pole
on-shell
threshold/1S/PS/MSR
lattice reference scheme
Monte-Carlo event-generator mass convention
```

## Required theorem pieces

```text
1. scheme target contract S(mu)
2. EW/Yukawa running map
3. QED running map for charged leptons where applicable
4. QCD running and threshold matching for colored fermions
5. counterterm convention
6. external constants ledger with uncertainty/correlation tracking
7. no-inverse-fit proof
8. comparison protocol that never silently identifies APF_TRACE with physical masses
```

## Recommended next code module

```text
apf/trace_scheme_transport_maps.py
```

This should remain separate from `apf/trace_scheme_transport.py` until an actual map is available.

## First safe implementation target

Build a **scheme-contract object** and a **no-comparison-without-contract** verifier before adding numerical transport formulas.

```text
check_T_scheme_contract_validity
check_T_transport_map_domain_codomain
check_T_no_comparison_without_scheme_contract
check_T_external_constants_ledger_declared
```
