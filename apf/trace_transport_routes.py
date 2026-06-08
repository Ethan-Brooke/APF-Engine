"""Trace-to-scheme route-classification bank.

v8.7 (2026-05-08 LATER-5): executable route map for the transport phase
following the v8.6 transport-ledger bank.  This module still does not compute
QCD, QED, EW, threshold, pole, on-shell, lattice, or finite-part maps.  It
banks a finite set of admissible and forbidden *route classes* so the next
push can target one route at a time without smuggling a physical-mass claim.

Status discipline:
    - APF_TRACE / W_TRACE closure: closed upstream at [P_local].
    - Trace-to-scheme boundary discipline: closed upstream at [P_boundary].
    - Transport ledger architecture: closed upstream at [P_ledger].
    - This module: [P_route], route/prerequisite classification only.
    - Physical scheme masses: still open; no physical mass vector is exported.

The route classifier gives the next theorem program a reproducible map:
colored-quark routes require QCD running + threshold matching + a scheme
contract; charged-lepton routes require QED/EW running/conversion; W_TRACE
routes require an EW input convention and radiative/on-shell contract; direct
identity routes are forbidden.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, Mapping, Tuple

from apf.trace_transport_ledger import (
    COLORED_BRANCH,
    LEPTON_BRANCH,
    WEAK_BRANCH,
    EXTERNAL_CONSTANT_SLOTS,
    COUNTERTERM_SLOTS,
    check_T_transport_ledger_bank_closure as _check_T_transport_ledger_bank_closure,
    check_T_target_observables_not_transport_inputs as _check_T_target_observables_not_transport_inputs,
    check_T_trace_values_remain_immutable_inputs as _check_T_trace_values_remain_immutable_inputs,
)


ROUTE_STATUS = "P_route"
PHYSICAL_TRANSPORT_CLOSED = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

ROUTE_FIELDS: Tuple[str, ...] = (
    "route_id",
    "domain_branch",
    "target_scheme_family",
    "required_maps",
    "required_external_slots",
    "required_counterterm_slots",
    "allowed_status",
    "blocked_reason",
    "may_consume_target_masses",
    "exports_physical_masses",
)

REQUIRED_ROUTE_IDS: Tuple[str, ...] = (
    "colored_msbar_running_route",
    "colored_pole_or_on_shell_route",
    "light_quark_low_energy_route",
    "charged_lepton_pole_or_running_route",
    "w_trace_on_shell_route",
    "identity_trace_to_physical_route",
)

FORBIDDEN_ROUTE_IDS: Tuple[str, ...] = (
    "identity_trace_to_physical_route",
)

OPEN_ROUTE_IDS: Tuple[str, ...] = tuple(r for r in REQUIRED_ROUTE_IDS if r not in FORBIDDEN_ROUTE_IDS)

NEXT_ROUTE_ORDER: Tuple[str, ...] = (
    "colored_msbar_running_route",
    "charged_lepton_pole_or_running_route",
    "w_trace_on_shell_route",
    "colored_pole_or_on_shell_route",
    "light_quark_low_energy_route",
)


@dataclass(frozen=True)
class TransportRoute:
    """One declared route class from APF_TRACE/W_TRACE to a reporting convention."""

    route_id: str
    domain_branch: Tuple[str, ...]
    target_scheme_family: str
    required_maps: Tuple[str, ...]
    required_external_slots: Tuple[str, ...]
    required_counterterm_slots: Tuple[str, ...]
    allowed_status: str
    blocked_reason: str = ""
    may_consume_target_masses: bool = False
    exports_physical_masses: bool = False


def _passed(result: Mapping[str, Any]) -> bool:
    return bool(result.get("passed") is True or str(result.get("status", "")).upper() in {"PASS", "P"})


def _route_table() -> Tuple[TransportRoute, ...]:
    return (
        TransportRoute(
            route_id="colored_msbar_running_route",
            domain_branch=COLORED_BRANCH,
            target_scheme_family="short-distance colored-fermion mass scheme, e.g. MSbar m_q^S(mu)",
            required_maps=(
                "QCD anomalous-dimension running map",
                "quark-threshold matching map",
                "EW/Yukawa finite correction policy when target precision requires it",
                "scale-variation and uncertainty propagation map",
            ),
            required_external_slots=(
                "alpha_s(mu) and/or Lambda_QCD convention for colored transport",
                "quark-threshold matching conventions and threshold order",
                "renormalization scales and scale-variation envelope",
                "uncertainties, correlations, and provenance tags",
            ),
            required_counterterm_slots=(
                "QCD running anomalous-dimension/counterterm slot",
                "QCD threshold matching slot",
                "scheme-specific finite-part convention slot",
            ),
            allowed_status="open_admissible_route",
        ),
        TransportRoute(
            route_id="colored_pole_or_on_shell_route",
            domain_branch=COLORED_BRANCH,
            target_scheme_family="pole/on-shell colored mass convention, only after short-distance transport",
            required_maps=(
                "short-distance colored transport route",
                "pole/on-shell conversion finite-part map",
                "renormalon/scheme-ambiguity warning ledger for quarks",
                "comparison metric fixed before target residuals are read",
            ),
            required_external_slots=(
                "alpha_s(mu) and/or Lambda_QCD convention for colored transport",
                "renormalization scales and scale-variation envelope",
                "uncertainties, correlations, and provenance tags",
            ),
            required_counterterm_slots=(
                "QCD running anomalous-dimension/counterterm slot",
                "QCD threshold matching slot",
                "on-shell or pole-convention conversion slot",
            ),
            allowed_status="open_admissible_route_after_msbar_leg",
        ),
        TransportRoute(
            route_id="light_quark_low_energy_route",
            domain_branch=("m_u", "m_d", "m_s"),
            target_scheme_family="low-energy or lattice/hadronic convention for light quarks",
            required_maps=(
                "nonperturbative convention declaration",
                "matching from trace codomain into selected low-energy convention",
                "external-constant and correlation ledger",
                "no direct identity comparison to quoted light-quark values",
            ),
            required_external_slots=(
                "alpha_s(mu) and/or Lambda_QCD convention for colored transport",
                "quark-threshold matching conventions and threshold order",
                "uncertainties, correlations, and provenance tags",
            ),
            required_counterterm_slots=(
                "QCD threshold matching slot",
                "scheme-specific finite-part convention slot",
            ),
            allowed_status="open_admissible_route_nonperturbative_contract_required",
        ),
        TransportRoute(
            route_id="charged_lepton_pole_or_running_route",
            domain_branch=LEPTON_BRANCH,
            target_scheme_family="charged-lepton pole, on-shell, or running mass convention",
            required_maps=(
                "QED running/conversion map",
                "EW/Yukawa finite correction policy when target precision requires it",
                "scheme-specific finite-part convention",
                "uncertainty propagation map",
            ),
            required_external_slots=(
                "alpha_em(mu) or electroweak input basis for charged-lepton/EW transport",
                "renormalization scales and scale-variation envelope",
                "uncertainties, correlations, and provenance tags",
            ),
            required_counterterm_slots=(
                "QED charged-lepton running slot",
                "EW/Yukawa running slot",
                "scheme-specific finite-part convention slot",
            ),
            allowed_status="open_admissible_route",
        ),
        TransportRoute(
            route_id="w_trace_on_shell_route",
            domain_branch=WEAK_BRANCH,
            target_scheme_family="W on-shell / EW input-basis convention",
            required_maps=(
                "EW input-basis declaration",
                "radiative correction / finite-part conversion map",
                "on-shell convention contract",
                "uncertainty propagation and comparison protocol",
            ),
            required_external_slots=(
                "weak input convention for W/on-shell comparisons",
                "alpha_em(mu) or electroweak input basis for charged-lepton/EW transport",
                "uncertainties, correlations, and provenance tags",
            ),
            required_counterterm_slots=(
                "EW/Yukawa running slot",
                "on-shell or pole-convention conversion slot",
                "scheme-specific finite-part convention slot",
            ),
            allowed_status="open_admissible_route",
        ),
        TransportRoute(
            route_id="identity_trace_to_physical_route",
            domain_branch=COLORED_BRANCH + LEPTON_BRANCH + WEAK_BRANCH,
            target_scheme_family="forbidden direct physical reporting codomain",
            required_maps=(),
            required_external_slots=(),
            required_counterterm_slots=(),
            allowed_status="forbidden_route",
            blocked_reason="APF_TRACE/W_TRACE and physical reporting schemes are distinct codomains; identity transport would smuggle the open theorem.",
            may_consume_target_masses=True,
            exports_physical_masses=True,
        ),
    )


def _route_by_id(route_id: str) -> TransportRoute:
    for route in _route_table():
        if route.route_id == route_id:
            return route
    raise KeyError(route_id)


def _all_slots(routes: Iterable[TransportRoute], attr: str) -> Tuple[str, ...]:
    values = sorted({slot for route in routes for slot in getattr(route, attr)})
    return tuple(values)


# ---------------------------------------------------------------------
# Bank-facing route-classification checks.
# ---------------------------------------------------------------------


def check_T_transport_route_status_declared() -> Dict[str, Any]:
    """Declare that v8.7 is route classification, not physical transport."""
    ledger = _check_T_transport_ledger_bank_closure()
    assert _passed(ledger)
    assert ledger.get("physical_transport_closed") is False
    return {
        "name": "T_transport_route_status_declared",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": ROUTE_STATUS,
        "dependencies": ["T_transport_ledger_bank_closure"],
        "closed_now": "route classification and prerequisite routing",
        "open_next": "actual route-map derivations/evaluations",
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "v8.7 banks the transport route map while preserving the open physical-transport boundary.",
    }


def check_T_transport_route_schema_complete() -> Dict[str, Any]:
    """Every route exposes the fields needed for a no-smuggling audit."""
    routes = _route_table()
    missing_by_route = {}
    for route in routes:
        payload = asdict(route)
        missing = [field for field in ROUTE_FIELDS if field not in payload]
        if missing:
            missing_by_route[route.route_id] = missing
    assert not missing_by_route
    return {
        "name": "T_transport_route_schema_complete",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_route | no-smuggling",
        "required_fields": list(ROUTE_FIELDS),
        "route_count": len(routes),
        "routes": [asdict(route) for route in routes],
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "Each route has explicit branch, target-family, prerequisite-map, external-slot, counterterm, and export flags.",
    }


def check_T_required_route_families_enumerated() -> Dict[str, Any]:
    """Enumerate the minimal route families needed for the next transport phase."""
    route_ids = tuple(route.route_id for route in _route_table())
    assert route_ids == REQUIRED_ROUTE_IDS
    assert set(FORBIDDEN_ROUTE_IDS).issubset(set(route_ids))
    return {
        "name": "T_required_route_families_enumerated",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_route",
        "route_ids": list(route_ids),
        "open_route_ids": list(OPEN_ROUTE_IDS),
        "forbidden_route_ids": list(FORBIDDEN_ROUTE_IDS),
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "The route space is finite and named before physical comparisons are attempted.",
    }


def check_T_colored_msbar_route_prerequisites_declared() -> Dict[str, Any]:
    """Colored short-distance route requires QCD running and thresholds."""
    route = _route_by_id("colored_msbar_running_route")
    assert set(route.domain_branch) == set(COLORED_BRANCH)
    assert "QCD anomalous-dimension running map" in route.required_maps
    assert "quark-threshold matching map" in route.required_maps
    assert route.allowed_status == "open_admissible_route"
    assert route.may_consume_target_masses is False
    return {
        "name": "T_colored_msbar_route_prerequisites_declared",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_route | colored-branch",
        "route": asdict(route),
        "computed_here": False,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "The colored MSbar-like route is admissible only as an open QCD running/matching theorem, not by identity.",
    }


def check_T_colored_pole_route_requires_short_distance_leg() -> Dict[str, Any]:
    """Pole/on-shell colored routes depend on the short-distance route first."""
    route = _route_by_id("colored_pole_or_on_shell_route")
    assert "short-distance colored transport route" in route.required_maps
    assert "on-shell or pole-convention conversion slot" in route.required_counterterm_slots
    assert route.allowed_status.endswith("after_msbar_leg")
    return {
        "name": "T_colored_pole_route_requires_short_distance_leg",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_route | colored-branch",
        "route": asdict(route),
        "direct_trace_to_pole_allowed": False,
        "computed_here": False,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "Colored pole/on-shell comparison is staged after a short-distance transport leg and a conversion contract.",
    }


def check_T_light_quark_route_nonperturbative_contract_required() -> Dict[str, Any]:
    """Light-quark low-energy routes require an explicit nonperturbative contract."""
    route = _route_by_id("light_quark_low_energy_route")
    assert set(route.domain_branch) == {"m_u", "m_d", "m_s"}
    assert "nonperturbative convention declaration" in route.required_maps
    assert "no direct identity comparison to quoted light-quark values" in route.required_maps
    return {
        "name": "T_light_quark_route_nonperturbative_contract_required",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_route | nonperturbative-boundary",
        "route": asdict(route),
        "direct_quote_comparison_allowed": False,
        "computed_here": False,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "Light-quark values cannot be read as APF_TRACE identities; a low-energy/nonperturbative convention must be declared first.",
    }


def check_T_charged_lepton_route_prerequisites_declared() -> Dict[str, Any]:
    """Charged-lepton routes require QED/EW conversion, not hidden fitting."""
    route = _route_by_id("charged_lepton_pole_or_running_route")
    assert set(route.domain_branch) == set(LEPTON_BRANCH)
    assert "QED running/conversion map" in route.required_maps
    assert "QED charged-lepton running slot" in route.required_counterterm_slots
    assert route.may_consume_target_masses is False
    return {
        "name": "T_charged_lepton_route_prerequisites_declared",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_route | lepton-branch",
        "route": asdict(route),
        "computed_here": False,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "Charged-lepton physical comparison is routed through QED/EW conversion and a finite-part convention.",
    }


def check_T_w_trace_route_prerequisites_declared() -> Dict[str, Any]:
    """W_TRACE routes require an EW input basis and radiative/on-shell contract."""
    route = _route_by_id("w_trace_on_shell_route")
    assert set(route.domain_branch) == set(WEAK_BRANCH)
    assert "EW input-basis declaration" in route.required_maps
    assert "weak input convention for W/on-shell comparisons" in route.required_external_slots
    assert route.exports_physical_masses is False
    return {
        "name": "T_w_trace_route_prerequisites_declared",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_route | W_TRACE-boundary",
        "route": asdict(route),
        "computed_here": False,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "W_TRACE comparison must pass through an EW input/on-shell convention rather than direct physical identification.",
    }


def check_T_identity_route_forbidden() -> Dict[str, Any]:
    """Forbid the one route that would collapse trace and physical codomains."""
    route = _route_by_id("identity_trace_to_physical_route")
    prior = _check_T_target_observables_not_transport_inputs()
    assert _passed(prior)
    assert route.allowed_status == "forbidden_route"
    assert route.blocked_reason
    assert route.may_consume_target_masses is True
    assert route.exports_physical_masses is True
    return {
        "name": "T_identity_route_forbidden",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_route | no-smuggling",
        "route": asdict(route),
        "forbidden_by": ["T_target_observables_not_transport_inputs", "trace/physical codomain separation"],
        "allowed": False,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "The identity map from APF_TRACE/W_TRACE to physical reporting values remains explicitly forbidden.",
    }


def check_T_route_external_slots_subset_of_ledger() -> Dict[str, Any]:
    """Route external slots must be inherited from the v8.6 ledger slots."""
    open_routes = tuple(route for route in _route_table() if route.route_id in OPEN_ROUTE_IDS)
    used_slots = set(_all_slots(open_routes, "required_external_slots"))
    assert used_slots.issubset(set(EXTERNAL_CONSTANT_SLOTS))
    return {
        "name": "T_route_external_slots_subset_of_ledger",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_route | ledger-compatibility",
        "used_external_slots": sorted(used_slots),
        "ledger_external_slots": list(EXTERNAL_CONSTANT_SLOTS),
        "new_hidden_external_slots": [],
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "The route classifier adds no new hidden constants beyond the banked transport ledger slots.",
    }


def check_T_route_counterterm_slots_subset_of_ledger() -> Dict[str, Any]:
    """Route counterterm slots must be inherited from the v8.6 ledger slots."""
    open_routes = tuple(route for route in _route_table() if route.route_id in OPEN_ROUTE_IDS)
    used_slots = set(_all_slots(open_routes, "required_counterterm_slots"))
    assert used_slots.issubset(set(COUNTERTERM_SLOTS))
    return {
        "name": "T_route_counterterm_slots_subset_of_ledger",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_route | ledger-compatibility",
        "used_counterterm_slots": sorted(used_slots),
        "ledger_counterterm_slots": list(COUNTERTERM_SLOTS),
        "counterterms_evaluated_here": False,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "The route classifier declares counterterm obligations but evaluates none of them.",
    }


def check_T_route_priority_order_declared() -> Dict[str, Any]:
    """Declare the recommended order for attacking the open transport theorem."""
    assert set(NEXT_ROUTE_ORDER) == set(OPEN_ROUTE_IDS)
    assert NEXT_ROUTE_ORDER[0] == "colored_msbar_running_route"
    return {
        "name": "T_route_priority_order_declared",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_route | workplan",
        "next_route_order": list(NEXT_ROUTE_ORDER),
        "rationale": {
            "colored_msbar_running_route": "canonical short-distance colored route; prerequisite for colored pole/on-shell claims",
            "charged_lepton_pole_or_running_route": "cleaner QED/EW branch with no QCD threshold stack",
            "w_trace_on_shell_route": "separate EW input-basis route for the W_TRACE branch",
            "colored_pole_or_on_shell_route": "allowed only after short-distance colored transport is fixed",
            "light_quark_low_energy_route": "requires the strongest nonperturbative convention discipline",
        },
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "The next push should attack named route maps, not the whole physical spectrum at once.",
    }


def check_T_transport_routes_bank_closure() -> Dict[str, Any]:
    """Master v8.7 closure: route classification only, no physical transport."""
    deps = [
        check_T_transport_route_status_declared(),
        check_T_transport_route_schema_complete(),
        check_T_required_route_families_enumerated(),
        check_T_colored_msbar_route_prerequisites_declared(),
        check_T_colored_pole_route_requires_short_distance_leg(),
        check_T_light_quark_route_nonperturbative_contract_required(),
        check_T_charged_lepton_route_prerequisites_declared(),
        check_T_w_trace_route_prerequisites_declared(),
        check_T_identity_route_forbidden(),
        check_T_route_external_slots_subset_of_ledger(),
        check_T_route_counterterm_slots_subset_of_ledger(),
        check_T_route_priority_order_declared(),
    ]
    immutable = _check_T_trace_values_remain_immutable_inputs()
    assert all(_passed(dep) for dep in deps)
    assert _passed(immutable)
    return {
        "name": "T_transport_routes_bank_closure",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": ROUTE_STATUS,
        "dependencies": [dep["name"] for dep in deps] + ["T_trace_values_remain_immutable_inputs"],
        "route_table": [asdict(route) for route in _route_table()],
        "next_route_order": list(NEXT_ROUTE_ORDER),
        "closed_now": "route classification and prerequisite routing",
        "open_next": "derive/evaluate one named route map under the v8.6 ledger",
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "The trace-to-scheme transport problem is now route-classified; all physical scheme masses remain open until a named route is derived and evaluated.",
    }


_CHECKS = {
    "T_transport_route_status_declared": check_T_transport_route_status_declared,
    "T_transport_route_schema_complete": check_T_transport_route_schema_complete,
    "T_required_route_families_enumerated": check_T_required_route_families_enumerated,
    "T_colored_msbar_route_prerequisites_declared": check_T_colored_msbar_route_prerequisites_declared,
    "T_colored_pole_route_requires_short_distance_leg": check_T_colored_pole_route_requires_short_distance_leg,
    "T_light_quark_route_nonperturbative_contract_required": check_T_light_quark_route_nonperturbative_contract_required,
    "T_charged_lepton_route_prerequisites_declared": check_T_charged_lepton_route_prerequisites_declared,
    "T_w_trace_route_prerequisites_declared": check_T_w_trace_route_prerequisites_declared,
    "T_identity_route_forbidden": check_T_identity_route_forbidden,
    "T_route_external_slots_subset_of_ledger": check_T_route_external_slots_subset_of_ledger,
    "T_route_counterterm_slots_subset_of_ledger": check_T_route_counterterm_slots_subset_of_ledger,
    "T_route_priority_order_declared": check_T_route_priority_order_declared,
    "T_transport_routes_bank_closure": check_T_transport_routes_bank_closure,
}


def register(registry: Dict[str, Any]) -> None:
    """Register trace-to-scheme route-classification checks into the global bank."""
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
        "status": "TRACE_TRANSPORT_ROUTES_BANK_PASS" if ok else "TRACE_TRANSPORT_ROUTES_BANK_FAIL",
        "bank_registered": True,
        "route_status": ROUTE_STATUS,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "results": rows,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_all(), indent=2))
