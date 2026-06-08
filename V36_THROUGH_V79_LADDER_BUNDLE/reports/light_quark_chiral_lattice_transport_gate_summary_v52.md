# Light-Quark Chiral/Lattice Transport Gate v52

`LIGHT_QUARK_CHIRAL_LATTICE_TRANSPORT_GATE_PASS`

v52 turns the old vague light-quark obstruction into a typed gate:

```text
(u,d,s): [P_light_transport_gate^chi-lat] / [T_u + L_chi-lat + Sigma_uds required]
```

## What is closed

- MSbar(2 GeV) light-quark codomain declared.
- Chiral/lattice transport schema typed.
- Source inventory audited.
- Identity transport knocked out.
- No-smuggling rules closed.

## Source inventory

Inherited down-family source components:

- `T_d = 0.003870916422334 GeV = 3.870916422334 MeV`
- `T_s = 0.087143281633652 GeV = 87.143281633652 MeV`

`T_u` is not banked in v52.

## Identity knockout diagnostic

- d identity residual: `-17.640076120553%`
- s identity residual: `-6.798629268821%`

This is assigned to missing chiral/lattice transport, not repaired by fitting a diagonal correction.

## Not claimed

No `u,d,s` export candidate, no physical-final light-quark masses, no zero residual, and no inverse target construction.

Next theorem: `APF_LIGHT_QUARK_UP_TRACE_SOURCE_AND_CHIRAL_LATTICE_EVALUATOR_LEDGER`.


## Audit vocabulary

- blocked: inverse target construction is blocked.
- not used: PDG values are not used to construct source or transport.
- not_claimed: export candidate and physical-final status are not_claimed.
- heavy-quark routes cannot substitute for low-energy transport.
