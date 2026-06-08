"""Trace transport completion-gate bank.

v8.9 (2026-05-08 LATER-7): terminal completion audit for the
APF_TRACE/W_TRACE -> physical scheme transport stack.

This module answers the operational question "can we finish it now?" in the
only bank-safe way: by stating and executing the physical-export gate.  The
v8.5-v8.8 stack has already banked the boundary, ledger, route classes, and
symbolic composition DAG.  What remains is not more naming; it is evaluated
transport data: selected target schemes, external constants/provenance,
QCD/QED/EW running and matching maps, finite counterterm conventions, and an
uncertainty/comparison protocol.

Status discipline:
    - APF_TRACE / W_TRACE closure: [P_local].
    - Trace-to-scheme boundary: [P_boundary].
    - Transport ledger: [P_ledger].
    - Route classification: [P_route].
    - Symbolic route composition: [P_composition].
    - This module: [P_completion_gate].
    - Physical scheme masses: still open; no physical mass vector is exported.

The main theorem is intentionally negative in the current code state:
from the banked v8.8 composition table alone, no route satisfies the terminal
export predicate.  Any physical-mass export before those certificates are
filled would be an identity-map or target-observable smuggle.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, fields
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

from apf.trace_transport_ledger import (
    EXTERNAL_CONSTANT_SLOTS,
    COUNTERTERM_SLOTS,
    OPEN_PROOF_OBLIGATIONS,
    check_T_transport_ledger_bank_closure as _check_T_transport_ledger_bank_closure,
)
from apf.trace_transport_routes import (
    check_T_transport_routes_bank_closure as _check_T_transport_routes_bank_closure,
)
from apf.trace_transport_composition import (
    check_T_trace_transport_composition_bank_closure as _check_T_trace_transport_composition_bank_closure,
)


COMPLETION_STATUS = "P_completion_gate"
PHYSICAL_TRANSPORT_CLOSED = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

FORBIDDEN_ROUTE_ID = "identity_trace_to_physical_route"
OPEN_ROUTE_IDS: Tuple[str, ...] = (
    "w_trace_on_shell_route",
    "charged_lepton_pole_or_running_route",
    "colored_msbar_running_route",
    "colored_pole_or_on_shell_route",
    "light_quark_low_energy_route",
)

ROUTE_COMPLETION_ORDER: Tuple[str, ...] = (
    "w_trace_on_shell_route",
    "charged_lepton_pole_or_running_route",
    "colored_msbar_running_route",
    "colored_pole_or_on_shell_route",
    "light_quark_low_energy_route",
)

MINIMAL_CLOSURE_REASONS: Mapping[str, str] = {
    "w_trace_on_shell_route": "fewest branch-specific slots; EW input-basis and finite on-shell conversion still required",
    "charged_lepton_pole_or_running_route": "no QCD threshold leg; QED/EW finite conversion and uncertainty protocol still required",
    "colored_msbar_running_route": "requires QCD running, thresholds, alpha_s/Lambda_QCD convention, and scale envelope",
    "colored_pole_or_on_shell_route": "extends colored short-distance route and adds pole/on-shell finite-part plus ambiguity ledger",
    "light_quark_low_energy_route": "hardest route: colored transport plus nonperturbative low-energy convention leg",
}

REQUIRED_COMPLETION_FIELDS: Tuple[str, ...] = (
    "route_id",
    "target_scheme_contract_filled",
    "terminal_codomain",
    "required_stage_ids",
    "required_external_slots",
    "required_counterterm_slots",
    "evaluated_transport_maps",
    "external_constants_ledger_filled",
    "counterterm_maps_evaluated",
    "uncertainty_protocol_evaluated",
    "target_observables_consumed",
    "exports_physical_scheme_masses",
    "physical_transport_closed",
)


@dataclass(frozen=True)
class TransportCompletionCertificate:
    """Terminal certificate required before a route may export physical masses."""

    route_id: str
    target_scheme_contract_filled: bool
    terminal_codomain: str
    required_stage_ids: Tuple[str, ...]
    required_external_slots: Tuple[str, ...]
    required_counterterm_slots: Tuple[str, ...]
    evaluated_transport_maps: Tuple[str, ...]
    external_constants_ledger_filled: bool
    counterterm_maps_evaluated: bool
    uncertainty_protocol_evaluated: bool
    target_observables_consumed: bool = False
    exports_physical_scheme_masses: bool = False
    physical_transport_closed: bool = False


def _passed(result: Mapping[str, Any]) -> bool:
    return bool(result.get("passed") is True or str(result.get("status", "")).upper() in {"PASS", "P"})


def _composition_rows() -> Tuple[Mapping[str, Any], ...]:
    result = _check_T_trace_transport_composition_bank_closure()
    assert _passed(result)
    assert result.get("physical_transport_closed") is False
    return tuple(result.get("composition_stage_table", ()))


def _route_rows() -> Tuple[Mapping[str, Any], ...]:
    result = _check_T_transport_routes_bank_closure()
    assert _passed(result)
    assert result.get("physical_transport_closed") is False
    return tuple(result.get("route_table", ()))


def _rows_for_route(route_id: str) -> Tuple[Mapping[str, Any], ...]:
    rows = [row for row in _composition_rows() if row.get("route_id") == route_id]
    return tuple(sorted(rows, key=lambda row: int(row.get("stage_order", 0))))


def _unique(items: Iterable[str]) -> Tuple[str, ...]:
    return tuple(sorted({str(item) for item in items if str(item)}))


def _completion_certificate(route_id: str) -> TransportCompletionCertificate:
    rows = _rows_for_route(route_id)
    stage_ids = tuple(str(row["stage_id"]) for row in rows)
    external_slots = _unique(
        slot
        for row in rows
        for slot in row.get("required_external_slots", ())
    )
    counterterm_slots = _unique(
        slot
        for row in rows
        for slot in row.get("required_counterterm_slots", ())
    )
    terminal = "NO_COMPOSITION_PLAN" if not rows else str(rows[-1].get("output_codomain"))
    return TransportCompletionCertificate(
        route_id=route_id,
        target_scheme_contract_filled=False,
        terminal_codomain=terminal,
        required_stage_ids=stage_ids,
        required_external_slots=external_slots,
        required_counterterm_slots=counterterm_slots,
        evaluated_transport_maps=(),
        external_constants_ledger_filled=False,
        counterterm_maps_evaluated=False,
        uncertainty_protocol_evaluated=False,
        target_observables_consumed=False,
        exports_physical_scheme_masses=False,
        physical_transport_closed=False,
    )


def _completion_certificates() -> Tuple[TransportCompletionCertificate, ...]:
    return tuple(_completion_certificate(route_id) for route_id in OPEN_ROUTE_IDS + (FORBIDDEN_ROUTE_ID,))


def _can_export_physical_masses(cert: TransportCompletionCertificate) -> bool:
    """Strict terminal export predicate for future transport theorems."""
    if cert.route_id == FORBIDDEN_ROUTE_ID:
        return False
    if cert.target_observables_consumed:
        return False
    if not cert.target_scheme_contract_filled:
        return False
    if not cert.required_stage_ids:
        return False
    if len(cert.evaluated_transport_maps) < len(cert.required_stage_ids):
        return False
    if cert.required_external_slots and not cert.external_constants_ledger_filled:
        return False
    if cert.required_counterterm_slots and not cert.counterterm_maps_evaluated:
        return False
    if not cert.uncertainty_protocol_evaluated:
        return False
    return True


# ---------------------------------------------------------------------
# Bank-facing completion-gate checks.
# ---------------------------------------------------------------------


def check_T_transport_completion_status_declared() -> Dict[str, Any]:
    """Declare that v8.9 is a terminal gate/obstruction bank, not mass closure."""
    comp = _check_T_trace_transport_composition_bank_closure()
    assert _passed(comp)
    assert comp.get("physical_transport_closed") is False
    return {
        "name": "T_transport_completion_status_declared",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": COMPLETION_STATUS,
        "dependencies": ["T_trace_transport_composition_bank_closure"],
        "closed_now": "terminal physical-export predicate and current obstruction certificate",
        "open_next": "fill one named route with evaluated transport maps, external ledger values, counterterms, and uncertainty propagation",
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "v8.9 answers the finish question: current bank state does not yet satisfy the physical-export gate.",
    }


def check_T_completion_certificate_schema_complete() -> Dict[str, Any]:
    """The terminal certificate has every field needed to police mass export."""
    actual = tuple(field.name for field in fields(TransportCompletionCertificate))
    missing = set(REQUIRED_COMPLETION_FIELDS) - set(actual)
    extra = set(actual) - set(REQUIRED_COMPLETION_FIELDS)
    assert not missing, f"completion certificate missing fields: {sorted(missing)}"
    assert not extra, f"completion certificate has unexpected fields: {sorted(extra)}"
    return {
        "name": "T_completion_certificate_schema_complete",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": COMPLETION_STATUS,
        "certificate_fields": list(actual),
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "The completion certificate distinguishes declared stages from evaluated physical transport.",
    }


def check_T_terminal_route_set_inherited_from_v88() -> Dict[str, Any]:
    """The completion gate covers every v8.8 route and preserves the forbidden identity route."""
    route_ids = {str(row.get("route_id")) for row in _route_rows()}
    stage_route_ids = {str(row.get("route_id")) for row in _composition_rows()}
    cert_ids = {cert.route_id for cert in _completion_certificates()}
    assert set(OPEN_ROUTE_IDS).issubset(route_ids)
    assert FORBIDDEN_ROUTE_ID in route_ids
    assert set(OPEN_ROUTE_IDS).issubset(stage_route_ids)
    assert FORBIDDEN_ROUTE_ID not in stage_route_ids
    assert cert_ids == set(OPEN_ROUTE_IDS + (FORBIDDEN_ROUTE_ID,))
    return {
        "name": "T_terminal_route_set_inherited_from_v88",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": COMPLETION_STATUS,
        "route_ids": sorted(route_ids),
        "composition_route_ids": sorted(stage_route_ids),
        "completion_certificate_route_ids": sorted(cert_ids),
        "forbidden_identity_has_stage_plan": False,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "The terminal gate covers all open v8.8 routes and keeps identity transport forbidden.",
    }


def check_T_evaluated_maps_required_for_completion() -> Dict[str, Any]:
    """Declared symbolic stages are not enough; evaluated maps are required."""
    certs = [cert for cert in _completion_certificates() if cert.route_id != FORBIDDEN_ROUTE_ID]
    assert all(cert.required_stage_ids for cert in certs)
    assert all(len(cert.evaluated_transport_maps) == 0 for cert in certs)
    assert all(not _can_export_physical_masses(cert) for cert in certs)
    return {
        "name": "T_evaluated_maps_required_for_completion",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": COMPLETION_STATUS,
        "stage_counts_by_route": {cert.route_id: len(cert.required_stage_ids) for cert in certs},
        "evaluated_transport_maps_by_route": {cert.route_id: list(cert.evaluated_transport_maps) for cert in certs},
        "physical_export_allowed_by_route": {cert.route_id: _can_export_physical_masses(cert) for cert in certs},
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "Symbolic route composition is not physical transport; each terminal stage needs an evaluated map.",
    }


def check_T_external_constants_ledger_unfilled_at_terminal_gate() -> Dict[str, Any]:
    """External constant slots are declared, but no terminal numerical ledger is filled."""
    certs = [cert for cert in _completion_certificates() if cert.route_id != FORBIDDEN_ROUTE_ID]
    required_union = _unique(slot for cert in certs for slot in cert.required_external_slots)
    declared = set(EXTERNAL_CONSTANT_SLOTS)
    unaccounted = set(required_union) - declared
    assert not unaccounted, f"external slots missing from v8.6 ledger: {sorted(unaccounted)}"
    assert required_union, "completion gate must see nonempty external slots"
    assert all(cert.external_constants_ledger_filled is False for cert in certs)
    return {
        "name": "T_external_constants_ledger_unfilled_at_terminal_gate",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": COMPLETION_STATUS,
        "declared_external_slots": list(EXTERNAL_CONSTANT_SLOTS),
        "terminal_required_external_slots": list(required_union),
        "filled_external_constant_ledgers": [],
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "External slots are ledgered but not numerically filled; terminal export remains blocked.",
    }


def check_T_counterterm_maps_unfilled_at_terminal_gate() -> Dict[str, Any]:
    """Counterterm/finite-part slots are declared, but no terminal maps are evaluated."""
    certs = [cert for cert in _completion_certificates() if cert.route_id != FORBIDDEN_ROUTE_ID]
    required_union = _unique(slot for cert in certs for slot in cert.required_counterterm_slots)
    declared = set(COUNTERTERM_SLOTS)
    unaccounted = set(required_union) - declared
    assert not unaccounted, f"counterterm slots missing from v8.6 ledger: {sorted(unaccounted)}"
    assert required_union, "completion gate must see nonempty counterterm slots"
    assert all(cert.counterterm_maps_evaluated is False for cert in certs)
    return {
        "name": "T_counterterm_maps_unfilled_at_terminal_gate",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": COMPLETION_STATUS,
        "declared_counterterm_slots": list(COUNTERTERM_SLOTS),
        "terminal_required_counterterm_slots": list(required_union),
        "evaluated_counterterm_maps": [],
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "Counterterm slots are named but unevaluated; terminal physical transport is not closed.",
    }


def check_T_uncertainty_protocol_required_before_physical_export() -> Dict[str, Any]:
    """No route may export until uncertainty propagation is evaluated."""
    certs = [cert for cert in _completion_certificates() if cert.route_id != FORBIDDEN_ROUTE_ID]
    assert all(cert.uncertainty_protocol_evaluated is False for cert in certs)
    assert all(not _can_export_physical_masses(cert) for cert in certs)
    return {
        "name": "T_uncertainty_protocol_required_before_physical_export",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": COMPLETION_STATUS,
        "uncertainty_protocol_evaluated_by_route": {cert.route_id: cert.uncertainty_protocol_evaluated for cert in certs},
        "open_requirement": "propagate external constants, correlations, truncation/order uncertainty, and scheme/scale variation before comparison",
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "A numerical map without an uncertainty protocol is still not a physical prediction claim.",
    }


def check_T_terminal_gate_forbids_target_observable_consumption() -> Dict[str, Any]:
    """Completion certificates and v8.8 stages cannot consume target observables."""
    rows = _composition_rows()
    certs = _completion_certificates()
    stage_consumers = [row for row in rows if bool(row.get("consumes_target_observables"))]
    cert_consumers = [cert.route_id for cert in certs if cert.target_observables_consumed]
    assert not stage_consumers
    assert not cert_consumers
    return {
        "name": "T_terminal_gate_forbids_target_observable_consumption",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": COMPLETION_STATUS + " | no-smuggling",
        "stage_consumers_of_target_observables": [],
        "certificate_consumers_of_target_observables": [],
        "forbidden_inputs": ["target physical mass vector", "post-hoc scalar fit", "identity APF_TRACE == physical mass assertion"],
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "The terminal gate preserves the no-target-observable/no-inverse-fit discipline.",
    }


def check_T_forbidden_identity_route_terminal_blocked() -> Dict[str, Any]:
    """The identity APF_TRACE -> physical route has no composition plan and cannot close."""
    cert = _completion_certificate(FORBIDDEN_ROUTE_ID)
    assert cert.required_stage_ids == ()
    assert cert.terminal_codomain == "NO_COMPOSITION_PLAN"
    assert _can_export_physical_masses(cert) is False
    return {
        "name": "T_forbidden_identity_route_terminal_blocked",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": COMPLETION_STATUS + " | no-smuggling",
        "route_id": FORBIDDEN_ROUTE_ID,
        "certificate": asdict(cert),
        "physical_export_allowed": False,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "The direct identity route remains forbidden at the terminal gate.",
    }


def check_T_minimal_closable_route_order_declared() -> Dict[str, Any]:
    """Rank the next route attempts by terminal burden without claiming closure."""
    certs = {cert.route_id: cert for cert in _completion_certificates()}
    assert tuple(ROUTE_COMPLETION_ORDER) == OPEN_ROUTE_IDS
    assert all(route in MINIMAL_CLOSURE_REASONS for route in ROUTE_COMPLETION_ORDER)
    burden = {
        route: {
            "stage_count": len(certs[route].required_stage_ids),
            "external_slot_count": len(certs[route].required_external_slots),
            "counterterm_slot_count": len(certs[route].required_counterterm_slots),
            "reason": MINIMAL_CLOSURE_REASONS[route],
        }
        for route in ROUTE_COMPLETION_ORDER
    }
    assert burden["w_trace_on_shell_route"]["stage_count"] <= burden["colored_msbar_running_route"]["stage_count"]
    assert burden["charged_lepton_pole_or_running_route"]["counterterm_slot_count"] <= burden["colored_msbar_running_route"]["counterterm_slot_count"]
    return {
        "name": "T_minimal_closable_route_order_declared",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": COMPLETION_STATUS,
        "recommended_next_order": list(ROUTE_COMPLETION_ORDER),
        "route_burden_summary": burden,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "The least-burden next closure attempts are W_TRACE and charged-lepton transport; colored/light-quark routes remain harder.",
    }


def check_T_physical_export_gate_locked_until_all_certificates_filled() -> Dict[str, Any]:
    """The terminal predicate blocks every current route certificate."""
    certs = _completion_certificates()
    allowed = {cert.route_id: _can_export_physical_masses(cert) for cert in certs}
    assert not any(allowed.values())
    return {
        "name": "T_physical_export_gate_locked_until_all_certificates_filled",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": COMPLETION_STATUS,
        "physical_export_allowed_by_route": allowed,
        "certificate_table": [asdict(cert) for cert in certs],
        "terminal_predicate": (
            "target scheme filled AND evaluated maps cover all stages AND external ledger filled "
            "AND counterterms evaluated AND uncertainty protocol evaluated AND no target-observable consumption"
        ),
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "The physical export gate is locked for every current route certificate.",
    }


def check_T_trace_transport_completion_gate_bank_closure() -> Dict[str, Any]:
    """Master v8.9 closure: the terminal gate is closed; physical masses are not."""
    ledger = _check_T_transport_ledger_bank_closure()
    routes = _check_T_transport_routes_bank_closure()
    composition = _check_T_trace_transport_composition_bank_closure()
    deps: List[Mapping[str, Any]] = [
        check_T_transport_completion_status_declared(),
        check_T_completion_certificate_schema_complete(),
        check_T_terminal_route_set_inherited_from_v88(),
        check_T_evaluated_maps_required_for_completion(),
        check_T_external_constants_ledger_unfilled_at_terminal_gate(),
        check_T_counterterm_maps_unfilled_at_terminal_gate(),
        check_T_uncertainty_protocol_required_before_physical_export(),
        check_T_terminal_gate_forbids_target_observable_consumption(),
        check_T_forbidden_identity_route_terminal_blocked(),
        check_T_minimal_closable_route_order_declared(),
        check_T_physical_export_gate_locked_until_all_certificates_filled(),
    ]
    assert _passed(ledger) and _passed(routes) and _passed(composition)
    assert all(_passed(dep) for dep in deps)
    return {
        "name": "T_trace_transport_completion_gate_bank_closure",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": COMPLETION_STATUS,
        "dependencies": [
            "T_transport_ledger_bank_closure",
            "T_transport_routes_bank_closure",
            "T_trace_transport_composition_bank_closure",
        ] + [str(dep["name"]) for dep in deps],
        "completion_certificate_table": [asdict(cert) for cert in _completion_certificates()],
        "open_proof_obligations": list(OPEN_PROOF_OBLIGATIONS),
        "closed_now": "terminal completion gate and current obstruction certificate",
        "not_closed": "physical scheme masses",
        "recommended_next_order": list(ROUTE_COMPLETION_ORDER),
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "Trace transport is fully staged to the terminal gate; the present codebase cannot honestly export physical scheme masses yet.",
    }


_CHECKS = {
    "T_transport_completion_status_declared": check_T_transport_completion_status_declared,
    "T_completion_certificate_schema_complete": check_T_completion_certificate_schema_complete,
    "T_terminal_route_set_inherited_from_v88": check_T_terminal_route_set_inherited_from_v88,
    "T_evaluated_maps_required_for_completion": check_T_evaluated_maps_required_for_completion,
    "T_external_constants_ledger_unfilled_at_terminal_gate": check_T_external_constants_ledger_unfilled_at_terminal_gate,
    "T_counterterm_maps_unfilled_at_terminal_gate": check_T_counterterm_maps_unfilled_at_terminal_gate,
    "T_uncertainty_protocol_required_before_physical_export": check_T_uncertainty_protocol_required_before_physical_export,
    "T_terminal_gate_forbids_target_observable_consumption": check_T_terminal_gate_forbids_target_observable_consumption,
    "T_forbidden_identity_route_terminal_blocked": check_T_forbidden_identity_route_terminal_blocked,
    "T_minimal_closable_route_order_declared": check_T_minimal_closable_route_order_declared,
    "T_physical_export_gate_locked_until_all_certificates_filled": check_T_physical_export_gate_locked_until_all_certificates_filled,
    "T_trace_transport_completion_gate_bank_closure": check_T_trace_transport_completion_gate_bank_closure,
}


def register(registry: Dict[str, Any]) -> None:
    """Register trace transport completion-gate checks into the global bank."""
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
        "status": "TRACE_TRANSPORT_COMPLETION_GATE_BANK_PASS" if ok else "TRACE_TRANSPORT_COMPLETION_GATE_BANK_FAIL",
        "bank_registered": True,
        "completion_status": COMPLETION_STATUS,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "results": rows,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_all(), indent=2))
