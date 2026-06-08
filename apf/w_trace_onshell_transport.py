"""W_TRACE on-shell route contract bank.

v9.0 (2026-05-08 LATER-8): first concrete route-specific module after the
v8.9 transport completion gate.  The v8.9 gate answered the finish question:
physical scheme masses cannot yet be exported because the route maps, external
constants ledgers, counterterm finite parts, and uncertainty protocols are not
filled.  This module advances the safest next path without crossing that line.

Closed here:
    - Select the W_TRACE -> on-shell W comparison route as the first concrete
      transport route to develop.
    - Bank the W on-shell target-contract template.
    - Enumerate the required EW input-basis, finite radiative conversion, and
      uncertainty slots.
    - Prove the route consumes no target M_W observable and exports no physical
      M_W claim.

Not closed here:
    - No EW input constants are evaluated.
    - No radiative/finite-part conversion map is evaluated.
    - No uncertainty propagation is evaluated.
    - No physical W mass is exported.

Status discipline:
    - APF_TRACE/W_TRACE closure: [P_local] upstream.
    - Boundary/ledger/route/composition/completion gate: v8.5-v8.9 upstream.
    - This module: [P_w_trace_contract], a route-specific contract layer.
    - Physical W/on-shell transport: still open.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, fields
from typing import Any, Dict, Iterable, Mapping, Tuple

from apf.trace_sector_closure import check_T_W_trace_branch_local as _check_T_W_trace_branch_local
from apf.trace_transport_ledger import (
    EXTERNAL_CONSTANT_SLOTS,
    COUNTERTERM_SLOTS,
    check_T_transport_ledger_bank_closure as _check_T_transport_ledger_bank_closure,
)
from apf.trace_transport_routes import (
    check_T_transport_routes_bank_closure as _check_T_transport_routes_bank_closure,
)
from apf.trace_transport_composition import (
    check_T_trace_transport_composition_bank_closure as _check_T_trace_transport_composition_bank_closure,
)
from apf.trace_transport_completion import (
    ROUTE_COMPLETION_ORDER,
    check_T_trace_transport_completion_gate_bank_closure as _check_T_trace_transport_completion_gate_bank_closure,
    check_T_physical_export_gate_locked_until_all_certificates_filled as _check_T_physical_export_gate_locked_until_all_certificates_filled,
)


W_TRACE_CONTRACT_STATUS = "P_w_trace_contract"
W_ROUTE_ID = "w_trace_on_shell_route"
PHYSICAL_W_TRANSPORT_CLOSED = False
PHYSICAL_TRANSPORT_CLOSED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False
ROUTE_CONTRACT_LAYER_FILLED = True

W_TRACE_EXPECTED_GEV = 80.362164334

REQUIRED_W_CONTRACT_FIELDS: Tuple[str, ...] = (
    "route_id",
    "source_codomain",
    "target_scheme_name",
    "target_observable_family",
    "terminal_codomain",
    "reference_convention",
    "input_basis_family",
    "required_stage_ids",
    "required_external_slots",
    "required_counterterm_slots",
    "required_map_slots",
    "target_observables_consumed",
    "evaluated_input_constants",
    "evaluated_transport_maps",
    "uncertainty_protocol_evaluated",
    "exports_physical_M_W",
    "physical_W_transport_closed",
)

REQUIRED_W_STAGE_IDS: Tuple[str, ...] = (
    "w_input_basis_contract",
    "w_radiative_finite_conversion",
    "w_uncertainty_protocol",
)

W_EXTERNAL_SLOTS: Tuple[str, ...] = (
    "weak input convention for W/on-shell comparisons",
    "alpha_em(mu) or electroweak input basis for charged-lepton/EW transport",
    "uncertainties, correlations, and provenance tags",
)

W_COUNTERTERM_SLOTS: Tuple[str, ...] = (
    "scheme-specific finite-part convention slot",
    "EW/Yukawa running slot",
    "on-shell or pole-convention conversion slot",
)

W_MAP_SLOTS: Tuple[str, ...] = (
    "EW input-basis declaration map",
    "radiative correction / finite-part conversion map",
    "W uncertainty propagation and comparison protocol",
)

W_INPUT_BASIS_OPTIONS: Tuple[str, ...] = (
    "on-shell alpha/M_Z/G_F-style input basis",
    "MSbar electroweak input basis at declared reference scale",
    "hybrid input basis with explicit finite conversion contract",
)

FORBIDDEN_W_INPUTS: Tuple[str, ...] = (
    "observed physical M_W",
    "target W residual",
    "fit parameter chosen to minimize W-mass error",
    "identity map from W_TRACE to physical on-shell M_W",
)


@dataclass(frozen=True)
class WTraceOnShellContract:
    """Route-specific target contract for W_TRACE -> on-shell W comparison."""

    route_id: str
    source_codomain: str
    target_scheme_name: str
    target_observable_family: str
    terminal_codomain: str
    reference_convention: str
    input_basis_family: Tuple[str, ...]
    required_stage_ids: Tuple[str, ...]
    required_external_slots: Tuple[str, ...]
    required_counterterm_slots: Tuple[str, ...]
    required_map_slots: Tuple[str, ...]
    target_observables_consumed: bool = False
    evaluated_input_constants: Tuple[str, ...] = ()
    evaluated_transport_maps: Tuple[str, ...] = ()
    uncertainty_protocol_evaluated: bool = False
    exports_physical_M_W: bool = False
    physical_W_transport_closed: bool = False


@dataclass(frozen=True)
class WRouteSlot:
    """One declared-but-unfilled slot for the W on-shell route."""

    slot_id: str
    slot_kind: str
    role: str
    filled: bool = False
    consumes_target_observable: bool = False
    evaluates_numerical_transport: bool = False


def _passed(result: Mapping[str, Any]) -> bool:
    return bool(result.get("passed") is True or str(result.get("status", "")).upper() in {"PASS", "P"})


def _w_contract() -> WTraceOnShellContract:
    return WTraceOnShellContract(
        route_id=W_ROUTE_ID,
        source_codomain="W_TRACE immutable weak-branch codomain",
        target_scheme_name="on-shell W comparison contract",
        target_observable_family="W on-shell mass convention family",
        terminal_codomain="comparison-ready symbolic W on-shell-convention codomain",
        reference_convention="declared EW input basis plus finite on-shell conversion; values not filled in v9.0",
        input_basis_family=W_INPUT_BASIS_OPTIONS,
        required_stage_ids=REQUIRED_W_STAGE_IDS,
        required_external_slots=W_EXTERNAL_SLOTS,
        required_counterterm_slots=W_COUNTERTERM_SLOTS,
        required_map_slots=W_MAP_SLOTS,
        target_observables_consumed=False,
        evaluated_input_constants=(),
        evaluated_transport_maps=(),
        uncertainty_protocol_evaluated=False,
        exports_physical_M_W=False,
        physical_W_transport_closed=False,
    )


def _w_slots() -> Tuple[WRouteSlot, ...]:
    return (
        WRouteSlot(
            slot_id="w_weak_input_convention",
            slot_kind="external_constant_slot",
            role="choose and provenance-tag the EW input convention for on-shell W comparison",
        ),
        WRouteSlot(
            slot_id="w_alpha_or_ew_input_basis",
            slot_kind="external_constant_slot",
            role="declare alpha_em / EW input-basis data without importing target M_W",
        ),
        WRouteSlot(
            slot_id="w_uncertainty_correlation_provenance",
            slot_kind="external_constant_slot",
            role="carry uncertainties, correlations, scale choices, and source provenance",
        ),
        WRouteSlot(
            slot_id="w_scheme_finite_part_policy",
            slot_kind="counterterm_slot",
            role="fix scheme-specific finite-part convention before numerical comparison",
        ),
        WRouteSlot(
            slot_id="w_ew_yukawa_finite_conversion",
            slot_kind="counterterm_slot",
            role="evaluate EW/Yukawa/radiative finite conversion only after contract closure",
        ),
        WRouteSlot(
            slot_id="w_on_shell_conversion",
            slot_kind="counterterm_slot",
            role="convert symbolic W_TRACE branch to on-shell-convention codomain without identity mapping",
        ),
        WRouteSlot(
            slot_id="w_input_basis_map",
            slot_kind="transport_map_slot",
            role="map W_TRACE codomain into the declared EW input-basis codomain symbolically",
        ),
        WRouteSlot(
            slot_id="w_radiative_conversion_map",
            slot_kind="transport_map_slot",
            role="radiative correction / finite-part conversion map; explicitly unevaluated here",
        ),
        WRouteSlot(
            slot_id="w_uncertainty_protocol_map",
            slot_kind="uncertainty_protocol_slot",
            role="uncertainty propagation and comparison protocol; explicitly unevaluated here",
        ),
    )


def _completion_gate_locked_for_w() -> bool:
    result = _check_T_physical_export_gate_locked_until_all_certificates_filled()
    assert _passed(result)
    allowed = result.get("physical_export_allowed_by_route", {})
    return allowed.get(W_ROUTE_ID) is False


# ---------------------------------------------------------------------
# Bank-facing W route contract checks.
# ---------------------------------------------------------------------


def check_T_w_trace_contract_status_declared() -> Dict[str, Any]:
    """Declare v9.0 as W route contract closure, not W physical transport."""
    completion = _check_T_trace_transport_completion_gate_bank_closure()
    wtrace = _check_T_W_trace_branch_local()
    assert _passed(completion) and _passed(wtrace)
    assert completion.get("physical_transport_closed") is False
    assert wtrace.get("exports_physical_M_W") is False
    return {
        "name": "T_w_trace_contract_status_declared",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_TRACE_CONTRACT_STATUS,
        "dependencies": ["T_trace_transport_completion_gate_bank_closure", "T_W_trace_branch_local"],
        "closed_now": "W_TRACE on-shell route contract/template and slot inventory",
        "not_closed": "numerical W on-shell transport or physical M_W export",
        "route_contract_layer_filled": ROUTE_CONTRACT_LAYER_FILLED,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "key_result": "The next concrete route is W_TRACE -> on-shell contract closure; the export gate remains locked.",
    }


def check_T_w_trace_route_selected_from_completion_order() -> Dict[str, Any]:
    """W_TRACE is the first route recommended by the terminal completion gate."""
    assert ROUTE_COMPLETION_ORDER[0] == W_ROUTE_ID
    routes = _check_T_transport_routes_bank_closure()
    assert _passed(routes)
    route_ids = {row.get("route_id") for row in routes.get("route_table", ())}
    assert W_ROUTE_ID in route_ids
    return {
        "name": "T_w_trace_route_selected_from_completion_order",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_TRACE_CONTRACT_STATUS,
        "recommended_order": list(ROUTE_COMPLETION_ORDER),
        "selected_route_id": W_ROUTE_ID,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "key_result": "The W_TRACE route is selected because it is the least-burden terminal transport path.",
    }


def check_T_w_trace_contract_schema_complete() -> Dict[str, Any]:
    """The W route contract exposes all fields needed before terminal export."""
    actual = tuple(field.name for field in fields(WTraceOnShellContract))
    missing = set(REQUIRED_W_CONTRACT_FIELDS) - set(actual)
    extra = set(actual) - set(REQUIRED_W_CONTRACT_FIELDS)
    assert not missing, f"W contract missing fields: {sorted(missing)}"
    assert not extra, f"W contract has unexpected fields: {sorted(extra)}"
    return {
        "name": "T_w_trace_contract_schema_complete",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_TRACE_CONTRACT_STATUS,
        "contract_fields": list(actual),
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "key_result": "The W contract schema separates target declaration, evaluated maps, and physical export.",
    }


def check_T_w_trace_local_input_preserved() -> Dict[str, Any]:
    """The upstream W_TRACE value remains immutable and local, not physical."""
    wtrace = _check_T_W_trace_branch_local()
    assert _passed(wtrace)
    assert abs(float(wtrace["M_W_TRACE_GeV"]) - W_TRACE_EXPECTED_GEV) < 1e-12
    assert wtrace.get("exports_physical_M_W") is False
    return {
        "name": "T_w_trace_local_input_preserved",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_TRACE_CONTRACT_STATUS,
        "M_W_TRACE_GeV": float(wtrace["M_W_TRACE_GeV"]),
        "source_status": wtrace.get("epistemic"),
        "source_codomain": "W_TRACE immutable weak-branch codomain",
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "key_result": "v9.0 preserves M_W^TRACE as an upstream local trace value, not a physical on-shell mass.",
    }


def check_T_w_trace_on_shell_target_contract_declared() -> Dict[str, Any]:
    """Declare the W on-shell target contract while leaving values/maps empty."""
    contract = _w_contract()
    assert contract.route_id == W_ROUTE_ID
    assert "on-shell" in contract.target_scheme_name
    assert contract.target_observables_consumed is False
    assert contract.evaluated_input_constants == ()
    assert contract.evaluated_transport_maps == ()
    assert contract.physical_W_transport_closed is False
    return {
        "name": "T_w_trace_on_shell_target_contract_declared",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_TRACE_CONTRACT_STATUS,
        "contract": asdict(contract),
        "route_contract_layer_filled": ROUTE_CONTRACT_LAYER_FILLED,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "key_result": "The W on-shell target is declared as a contract, not as an evaluated physical prediction.",
    }


def check_T_w_trace_input_basis_slots_declared_unfilled() -> Dict[str, Any]:
    """EW input-basis alternatives are enumerated but no external values are filled."""
    contract = _w_contract()
    assert len(contract.input_basis_family) >= 3
    assert not contract.evaluated_input_constants
    slots = [slot for slot in _w_slots() if slot.slot_kind == "external_constant_slot"]
    assert slots
    assert all(slot.filled is False for slot in slots)
    assert all(slot.consumes_target_observable is False for slot in slots)
    return {
        "name": "T_w_trace_input_basis_slots_declared_unfilled",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_TRACE_CONTRACT_STATUS,
        "input_basis_options": list(contract.input_basis_family),
        "external_slots": [asdict(slot) for slot in slots],
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "key_result": "The W route can now name its input-basis choices without importing numerical EW constants or target M_W.",
    }


def check_T_w_trace_radiative_conversion_slots_declared_unevaluated() -> Dict[str, Any]:
    """Finite conversion/radiative map slots exist but are not evaluated."""
    slots = [slot for slot in _w_slots() if slot.slot_kind in {"counterterm_slot", "transport_map_slot"}]
    assert slots
    assert all(slot.evaluates_numerical_transport is False for slot in slots)
    assert all(slot.filled is False for slot in slots)
    contract = _w_contract()
    assert not contract.evaluated_transport_maps
    return {
        "name": "T_w_trace_radiative_conversion_slots_declared_unevaluated",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_TRACE_CONTRACT_STATUS,
        "map_slots": list(contract.required_map_slots),
        "counterterm_and_map_slots": [asdict(slot) for slot in slots],
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "key_result": "The W finite-conversion route is explicit but remains unevaluated.",
    }


def check_T_w_trace_external_slots_subset_of_transport_ledger() -> Dict[str, Any]:
    """Every W external slot is already authorized by the v8.6 ledger."""
    ledger = _check_T_transport_ledger_bank_closure()
    assert _passed(ledger)
    ledger_slots = set(EXTERNAL_CONSTANT_SLOTS)
    contract_slots = set(_w_contract().required_external_slots)
    missing = contract_slots - ledger_slots
    assert not missing, f"W external slots not in ledger: {sorted(missing)}"
    return {
        "name": "T_w_trace_external_slots_subset_of_transport_ledger",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_TRACE_CONTRACT_STATUS,
        "w_external_slots": sorted(contract_slots),
        "ledger_external_slots": list(EXTERNAL_CONSTANT_SLOTS),
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "key_result": "W route external constants are a subset of the existing transport ledger, not new hidden inputs.",
    }


def check_T_w_trace_counterterm_slots_subset_of_transport_ledger() -> Dict[str, Any]:
    """Every W counterterm/finite-part slot is already authorized by the ledger."""
    ledger = _check_T_transport_ledger_bank_closure()
    assert _passed(ledger)
    ledger_slots = set(COUNTERTERM_SLOTS)
    contract_slots = set(_w_contract().required_counterterm_slots)
    missing = contract_slots - ledger_slots
    assert not missing, f"W counterterm slots not in ledger: {sorted(missing)}"
    return {
        "name": "T_w_trace_counterterm_slots_subset_of_transport_ledger",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_TRACE_CONTRACT_STATUS,
        "w_counterterm_slots": sorted(contract_slots),
        "ledger_counterterm_slots": list(COUNTERTERM_SLOTS),
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "key_result": "W route finite-part/counterterm slots reuse the banked transport ledger.",
    }


def check_T_w_trace_no_target_MW_observable_consumed() -> Dict[str, Any]:
    """The W route contract forbids using observed M_W or residuals as inputs."""
    contract = _w_contract()
    slots = _w_slots()
    assert contract.target_observables_consumed is False
    assert all(slot.consumes_target_observable is False for slot in slots)
    forbidden = tuple(item for item in FORBIDDEN_W_INPUTS if "M_W" in item or "W" in item)
    assert forbidden
    return {
        "name": "T_w_trace_no_target_MW_observable_consumed",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_TRACE_CONTRACT_STATUS,
        "forbidden_inputs": list(FORBIDDEN_W_INPUTS),
        "target_observables_consumed": False,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "key_result": "Observed M_W and W residuals are explicitly forbidden as transport inputs.",
    }


def check_T_w_trace_uncertainty_protocol_declared_not_evaluated() -> Dict[str, Any]:
    """The comparison protocol exists as a required terminal slot only."""
    contract = _w_contract()
    uncertainty_slots = [slot for slot in _w_slots() if "uncertainty" in slot.slot_id or slot.slot_kind == "uncertainty_protocol_slot"]
    assert uncertainty_slots
    assert contract.uncertainty_protocol_evaluated is False
    assert all(slot.filled is False for slot in uncertainty_slots)
    return {
        "name": "T_w_trace_uncertainty_protocol_declared_not_evaluated",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_TRACE_CONTRACT_STATUS,
        "uncertainty_slots": [asdict(slot) for slot in uncertainty_slots],
        "uncertainty_protocol_evaluated": False,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "key_result": "The W route now has a required uncertainty protocol slot, but no comparison claim is made.",
    }


def check_T_w_trace_completion_gate_remains_locked() -> Dict[str, Any]:
    """Even after selecting the W contract, terminal physical export is blocked."""
    assert _completion_gate_locked_for_w() is True
    contract = _w_contract()
    terminal_requirements_unfilled = {
        "evaluated_input_constants": bool(contract.evaluated_input_constants),
        "evaluated_transport_maps": bool(contract.evaluated_transport_maps),
        "uncertainty_protocol_evaluated": contract.uncertainty_protocol_evaluated,
        "exports_physical_M_W": contract.exports_physical_M_W,
        "physical_W_transport_closed": contract.physical_W_transport_closed,
    }
    assert not any(terminal_requirements_unfilled.values())
    return {
        "name": "T_w_trace_completion_gate_remains_locked",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_TRACE_CONTRACT_STATUS,
        "route_id": W_ROUTE_ID,
        "physical_export_allowed": False,
        "terminal_requirements_unfilled": terminal_requirements_unfilled,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "key_result": "The v8.9 export gate remains locked for W_TRACE after v9.0 contract closure.",
    }


def check_T_w_trace_on_shell_contract_bank_closure() -> Dict[str, Any]:
    """Master v9.0 W route contract closure."""
    deps = [
        check_T_w_trace_contract_status_declared(),
        check_T_w_trace_route_selected_from_completion_order(),
        check_T_w_trace_contract_schema_complete(),
        check_T_w_trace_local_input_preserved(),
        check_T_w_trace_on_shell_target_contract_declared(),
        check_T_w_trace_input_basis_slots_declared_unfilled(),
        check_T_w_trace_radiative_conversion_slots_declared_unevaluated(),
        check_T_w_trace_external_slots_subset_of_transport_ledger(),
        check_T_w_trace_counterterm_slots_subset_of_transport_ledger(),
        check_T_w_trace_no_target_MW_observable_consumed(),
        check_T_w_trace_uncertainty_protocol_declared_not_evaluated(),
        check_T_w_trace_completion_gate_remains_locked(),
    ]
    assert all(_passed(dep) for dep in deps)
    composition = _check_T_trace_transport_composition_bank_closure()
    assert _passed(composition)
    stage_rows = [row for row in composition.get("composition_stage_table", ()) if row.get("route_id") == W_ROUTE_ID]
    assert tuple(row.get("stage_id") for row in stage_rows) == REQUIRED_W_STAGE_IDS
    return {
        "name": "T_w_trace_on_shell_contract_bank_closure",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_TRACE_CONTRACT_STATUS,
        "dependencies": [str(dep["name"]) for dep in deps] + ["T_trace_transport_composition_bank_closure"],
        "contract": asdict(_w_contract()),
        "slot_table": [asdict(slot) for slot in _w_slots()],
        "stage_ids": list(REQUIRED_W_STAGE_IDS),
        "closed_now": "W_TRACE route-specific on-shell contract and unfilled slot ledger",
        "not_closed": "evaluated W transport maps, external constants, counterterms, uncertainty propagation, physical M_W export",
        "route_contract_layer_filled": ROUTE_CONTRACT_LAYER_FILLED,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "key_result": "W_TRACE on-shell route contract is banked; terminal physical W transport remains open and gated.",
    }


_CHECKS = {
    "T_w_trace_contract_status_declared": check_T_w_trace_contract_status_declared,
    "T_w_trace_route_selected_from_completion_order": check_T_w_trace_route_selected_from_completion_order,
    "T_w_trace_contract_schema_complete": check_T_w_trace_contract_schema_complete,
    "T_w_trace_local_input_preserved": check_T_w_trace_local_input_preserved,
    "T_w_trace_on_shell_target_contract_declared": check_T_w_trace_on_shell_target_contract_declared,
    "T_w_trace_input_basis_slots_declared_unfilled": check_T_w_trace_input_basis_slots_declared_unfilled,
    "T_w_trace_radiative_conversion_slots_declared_unevaluated": check_T_w_trace_radiative_conversion_slots_declared_unevaluated,
    "T_w_trace_external_slots_subset_of_transport_ledger": check_T_w_trace_external_slots_subset_of_transport_ledger,
    "T_w_trace_counterterm_slots_subset_of_transport_ledger": check_T_w_trace_counterterm_slots_subset_of_transport_ledger,
    "T_w_trace_no_target_MW_observable_consumed": check_T_w_trace_no_target_MW_observable_consumed,
    "T_w_trace_uncertainty_protocol_declared_not_evaluated": check_T_w_trace_uncertainty_protocol_declared_not_evaluated,
    "T_w_trace_completion_gate_remains_locked": check_T_w_trace_completion_gate_remains_locked,
    "T_w_trace_on_shell_contract_bank_closure": check_T_w_trace_on_shell_contract_bank_closure,
}


def register(registry: Dict[str, Any]) -> None:
    """Register W_TRACE on-shell route contract checks into the global bank."""
    registry.update(_CHECKS)


def run_all() -> Dict[str, Any]:
    rows = []
    for name, fn in _CHECKS.items():
        try:
            result = fn()
            rows.append({"name": name, "passed": _passed(result), "result": result})
        except Exception as exc:
            rows.append({"name": name, "passed": False, "error": repr(exc)})
    ok = all(row["passed"] for row in rows)
    return {
        "passed": sum(1 for row in rows if row["passed"]),
        "total": len(rows),
        "status": "W_TRACE_ONSHELL_CONTRACT_BANK_PASS" if ok else "W_TRACE_ONSHELL_CONTRACT_BANK_FAIL",
        "bank_registered": True,
        "route_status": W_TRACE_CONTRACT_STATUS,
        "route_id": W_ROUTE_ID,
        "route_contract_layer_filled": ROUTE_CONTRACT_LAYER_FILLED,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "results": rows,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_all(), indent=2))
