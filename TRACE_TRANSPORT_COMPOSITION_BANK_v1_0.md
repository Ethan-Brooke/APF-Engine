# Trace Transport Composition Bank v1.0

Status: `P_composition`.

This bank layer comes after:

1. `P_local`: APF_TRACE / W_TRACE local trace-sector closure.
2. `P_boundary`: trace-to-scheme boundary discipline.
3. `P_ledger`: transport-ledger architecture.
4. `P_route`: route classification and prerequisites.

This layer banks ordered symbolic composition plans for each open route. It does **not** evaluate QCD, QED, EW, threshold, pole/on-shell, lattice, finite-part, or uncertainty maps. It does **not** export physical scheme masses.

Main verifier:

```bash
python scripts/check_trace_transport_composition.py
```

Expected result:

```text
TRACE_TRANSPORT_COMPOSITION_BANK_PASS
```

New module:

```text
apf/trace_transport_composition.py
```

New checks:

```text
check_T_transport_composition_status_declared
check_T_composition_stage_schema_complete
check_T_composition_graph_acyclic
check_T_open_routes_have_nonempty_stage_plans
check_T_colored_msbar_composition_ordered
check_T_charged_lepton_composition_ordered
check_T_w_trace_composition_ordered
check_T_colored_pole_composition_extends_msbar
check_T_light_quark_composition_requires_nonperturbative_leg
check_T_stage_inputs_exclude_target_observables
check_T_stage_outputs_are_intermediate_not_physical_claims
check_T_forbidden_identity_route_has_no_composition_plan
check_T_composition_external_slots_accounted_to_route
check_T_trace_transport_composition_bank_closure
```

Claim ladder after this push:

```text
APF_TRACE/W_TRACE local closure:        P_local
Trace-to-scheme boundary discipline:   P_boundary
Transport ledger architecture:         P_ledger
Route classification:                  P_route
Symbolic route composition:            P_composition
Physical scheme masses:                OPEN
```
