"""
APF Interface Structure Discovery Engine.

v24.3.12+ delta layer.

Purpose
-------
The Interface Structure Transport Ledger can represent the structures that move at an
interface.  This module is the next layer: it discovers/infers that typed ledger from raw
route payloads and checks that every downstream obstruction has a structure-level witness.

Architecture:
    raw route payload
      -> discover_ledger(route, payload)
      -> typed moving-structure inventory
      -> certify_ledger(...)
      -> obstruction/promotion certificate
      -> witness map: obstruction -> moving structure(s)

Top check:
    check_T_interface_structure_discovery_engine_P

Important:
    This engine still does not compute physics routes. It identifies and certifies the
    interface-moving structures exposed by a route or solver payload.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Iterable, Mapping, Tuple, List, Optional

try:
    from apf.interface_structure_transport_ledger import (
        StructureKind,
        StructureStatus,
        InterfaceStructureItem,
        InterfaceStructureTransportLedger,
        LedgerCertificate,
        certify_ledger,
        item,
        ew_trace_scheme_ledger,
        dark_posterior_ledger,
        gauge_fiber_ledger,
        horizon_fiber_cost_ledger,
        substrate_cstar_attempt_ledger,
    )
except Exception as exc:  # pragma: no cover
    raise ImportError(f"interface_structure_discovery_engine requires interface_structure_transport_ledger: {exc}") from exc


FORBIDDEN_EXPECTED_FIELDS = {
    "expected_status",
    "expected_label",
    "expected_repair_class",
    "solver_status",
    "promotion_status",
    "repair_class",
    "export_global_P",
    "obstruction",
    "safe_claim",
    "certificate",
}


ROUTE_ALIASES = {
    "ew": "ew",
    "ew_trace": "ew",
    "ew_trace_scheme": "ew",
    "dark": "dark",
    "dark_posterior": "dark",
    "gauge": "gauge",
    "gauge_fiber": "gauge",
    "horizon": "horizon",
    "horizon_cost": "horizon",
    "capacity": "capacity",
    "coarse_grain": "capacity",
    "provenance": "provenance",
    "anti_fitting": "provenance",
    "cstar": "cstar",
    "flat_cstar": "cstar",
    "generic": "generic",
    # v24.3.41 — Step D audit Finding 1 closer:
    # The 3 new claim-compiler routes (STRUCTURAL_KERNEL / MULTI_ROUTE_AUDIT /
    # CATEGORICAL_UNIFICATION) are claim-classification routes, not new physical
    # sector routes. They alias to existing downstream routes:
    # - STRUCTURAL_KERNEL → cstar (substrate-C* / kernel-master is the closest
    #   existing sector for RDFI master-theorem-style claims)
    # - MULTI_ROUTE_AUDIT → generic (no single sector owns multi-route
    #   adjudication claims)
    # - CATEGORICAL_UNIFICATION → gauge (the categorical fibration shape and
    #   ACC-unification content closest matches gauge_fiber downstream)
    "structural_kernel": "cstar",
    "multi_route_audit": "generic",
    "categorical_unification": "gauge",
}


def normalize_route(route: str) -> str:
    key = route.strip().lower().replace("-", "_")
    if key not in ROUTE_ALIASES:
        raise ValueError(f"Unsupported route '{route}'. Supported: {sorted(set(ROUTE_ALIASES.values()))}")
    return ROUTE_ALIASES[key]


def reject_expected_fields(payload: Mapping[str, Any]) -> None:
    leaked = sorted(set(payload.keys()) & FORBIDDEN_EXPECTED_FIELDS)
    if leaked:
        raise ValueError(f"Expected-label/certificate fields are forbidden in discovery payload: {leaked}")


def _truth(payload: Mapping[str, Any], key: str, default: bool = False) -> bool:
    return bool(payload.get(key, default))


def capacity_ledger_from_payload(payload: Mapping[str, Any]) -> InterfaceStructureTransportLedger:
    name = str(payload.get("name", "capacity_discovery"))
    raw = int(payload.get("raw_capacity_load", 0))
    budget = int(payload.get("capacity_budget", 1))
    factor = int(payload.get("coarse_grain_factor", 1))
    if factor <= 0:
        raise ValueError("coarse_grain_factor must be positive")
    effective = (raw + factor - 1) // factor
    fits = effective <= budget
    target_value_consumed = _truth(payload, "target_value_consumed", False)

    items = (
        item("ACC base record", StructureKind.ACC_RECORD, "APF interface", "APF interface", True, True),
        item(
            "capacity load after coarse-graining",
            StructureKind.CAPACITY_COST,
            "raw interface load",
            "capacity budget",
            True,
            fits,
            obstruction_hint=("CAPACITY_OVERSPEND",),
            notes=f"raw={raw}; budget={budget}; factor={factor}; effective={effective}",
        ),
        item("capacity codomain declaration", StructureKind.CODOMAIN_TRANSPORT, "load ledger", "capacity claim", True, True),
        item("capacity evaluator", StructureKind.EVALUATOR_MAP, "coarse-grain experiment", "capacity claim", True, True),
        InterfaceStructureItem(
            "no capacity target used as input",
            StructureKind.PROVENANCE,
            "target",
            "capacity experiment input",
            True,
            StructureStatus.FAIL_CLOSED_PROVENANCE if target_value_consumed else StructureStatus.PRESENT_STABLE,
            ("PROVENANCE_SMUGGLE",),
        ),
    )
    return InterfaceStructureTransportLedger(
        name=name,
        sector="CAPACITY",
        items=items,
        local_solution_found=True,
        notes=f"capacity discovery: effective_load={effective}; minimum_factor_to_fit={(raw + budget - 1) // budget if budget > 0 else None}",
    )


def provenance_ledger_from_payload(payload: Mapping[str, Any]) -> InterfaceStructureTransportLedger:
    name = str(payload.get("name", "provenance_discovery"))
    sector = str(payload.get("sector", "PROVENANCE"))
    inputs = {str(x).strip().lower().replace(" ", "_") for x in payload.get("inputs_used", [])}
    forbidden = {
        str(x).strip().lower().replace(" ", "_")
        for x in (
            list(payload.get("declared_targets", []))
            + list(payload.get("fitted_outputs", []))
            + list(payload.get("posterior_outputs", []))
        )
    }
    allowed = {str(x).strip().lower().replace(" ", "_") for x in payload.get("allowed_exogenous_inputs", [])}
    smuggled = tuple(sorted((inputs & forbidden) - allowed))
    ok = not smuggled

    items = (
        item("ACC base record", StructureKind.ACC_RECORD, "APF interface", "APF interface", True, True),
        item("provenance evaluator", StructureKind.EVALUATOR_MAP, "input ledger", "claim", True, True),
        item("provenance codomain", StructureKind.CODOMAIN_TRANSPORT, "input ledger", "claim", True, True),
        InterfaceStructureItem(
            "no target/posterior/fitted output consumed",
            StructureKind.PROVENANCE,
            "targets/posteriors/fitted outputs",
            "route inputs",
            True,
            StructureStatus.FAIL_CLOSED_PROVENANCE if not ok else StructureStatus.PRESENT_STABLE,
            ("PROVENANCE_SMUGGLE",),
            f"smuggled={smuggled}",
        ),
    )
    return InterfaceStructureTransportLedger(
        name=name,
        sector=sector,
        items=items,
        local_solution_found=True,
        notes=f"provenance discovery: smuggled={smuggled}",
    )


def generic_ledger_from_payload(payload: Mapping[str, Any]) -> InterfaceStructureTransportLedger:
    """Discover a minimal generic ledger from InterfaceSolverProblem-like raw fields."""
    name = str(payload.get("name", "generic_discovery"))
    sector = str(payload.get("sector", "GENERIC"))
    target_value_consumed = _truth(payload, "target_value_used_as_input", _truth(payload, "target_value_consumed", False))
    items = (
        item("ACC base record", StructureKind.ACC_RECORD, "APF interface", "APF interface", True, _truth(payload, "acc_base_present", True), obstruction_hint=("CODOMAIN_MISMATCH",)),
        item("generic evaluator map", StructureKind.EVALUATOR_MAP, "solver route", "claim", True, _truth(payload, "evaluator_map_found", False), obstruction_hint=("EVALUATOR_MISSING",)),
        item("generic codomain transport", StructureKind.CODOMAIN_TRANSPORT, "source codomain", "target codomain", True, _truth(payload, "codomain_transport_found", False), obstruction_hint=("CODOMAIN_MISMATCH",)),
        item("generic overlap gluing", StructureKind.OVERLAP_GLUING, "local patches", "global object", True, _truth(payload, "overlap_gluing_verified", True), obstruction_hint=("OVERLAP_INCOHERENCE",)),
        item("generic capacity budget", StructureKind.CAPACITY_COST, "load", "budget", True, _truth(payload, "capacity_budget_verified", True) and not _truth(payload, "capacity_overspend_detected", False), obstruction_hint=("CAPACITY_OVERSPEND",)),
        item("generic empirical/posterior closure", StructureKind.EMPIRICAL_POSTERIOR, "run output", "claim", True, _truth(payload, "empirical_or_posterior_closed", True), obstruction_hint=("EVALUATOR_MISSING",)),
        InterfaceStructureItem(
            "generic no target as input",
            StructureKind.PROVENANCE,
            "target",
            "input",
            True,
            StructureStatus.FAIL_CLOSED_PROVENANCE if target_value_consumed else StructureStatus.PRESENT_STABLE,
            ("PROVENANCE_SMUGGLE",),
        ),
    )
    return InterfaceStructureTransportLedger(
        name=name,
        sector=sector,
        items=items,
        local_solution_found=_truth(payload, "local_solution_found", True),
        global_export_requested=_truth(payload, "global_export_requested", True),
        notes=str(payload.get("notes", "generic discovery ledger")),
    )


def discover_ledger(route: str, payload: Mapping[str, Any]) -> InterfaceStructureTransportLedger:
    """Infer a typed interface-structure ledger from a route-specific raw payload."""
    reject_expected_fields(payload)
    route = normalize_route(route)

    if route == "ew":
        return ew_trace_scheme_ledger(
            name=str(payload.get("name", "EW_discovery")),
            trace_sector_closed=_truth(payload, "trace_sector_closed", False),
            source_to_scheme_registry_present=_truth(payload, "source_to_scheme_registry_present", False),
            evaluator_map_found=_truth(payload, "evaluator_map_found", False),
            codomain_transport_found=_truth(payload, "codomain_transport_found", False),
            counterterm_finite_parts_declared=_truth(payload, "counterterm_finite_parts_declared", False),
            external_constants_ledger_clean=_truth(payload, "external_constants_ledger_clean", False),
            uncertainty_protocol_declared=_truth(payload, "uncertainty_protocol_declared", False),
            target_value_consumed=_truth(payload, "target_value_consumed", False),
        )

    if route == "dark":
        return dark_posterior_ledger(
            name=str(payload.get("name", "dark_discovery")),
            route_built=_truth(payload, "route_built", False),
            run_completed=_truth(payload, "run_completed", False),
            posterior_closed=_truth(payload, "posterior_closed", False),
            robustness_checks_passed=_truth(payload, "robustness_checks_passed", False),
            target_value_consumed=_truth(payload, "target_value_consumed", False),
        )

    if route == "gauge":
        return gauge_fiber_ledger(
            name=str(payload.get("name", "gauge_discovery")),
            local_fiber_action_defined=_truth(payload, "local_fiber_action_defined", False),
            codomain_map_declared=_truth(payload, "codomain_map_declared", False),
            overlap_cocycle_verified=_truth(payload, "overlap_cocycle_verified", False),
            anomaly_check_passed=_truth(payload, "anomaly_check_passed", False),
            target_value_consumed=_truth(payload, "target_value_consumed", False),
        )

    if route == "horizon":
        return horizon_fiber_cost_ledger(
            name=str(payload.get("name", "horizon_discovery")),
            horizon_partition_defined=_truth(payload, "horizon_partition_defined", False),
            area_cost_map_defined=_truth(payload, "area_cost_map_defined", False),
            overlap_gluing_verified=_truth(payload, "overlap_gluing_verified", False),
            capacity_bound_checked=_truth(payload, "capacity_bound_checked", False),
            target_value_consumed=_truth(payload, "target_value_consumed", False),
        )

    if route == "capacity":
        return capacity_ledger_from_payload(payload)

    if route == "provenance":
        return provenance_ledger_from_payload(payload)

    if route == "cstar":
        return substrate_cstar_attempt_ledger(name=str(payload.get("name", "flat_Cstar_discovery")))

    if route == "generic":
        return generic_ledger_from_payload(payload)

    raise AssertionError(route)  # pragma: no cover


def obstruction_witness_map(cert: LedgerCertificate) -> Dict[str, Tuple[str, ...]]:
    """Map each obstruction in the certificate to ledger item names that predicted it."""
    obstructions = tuple(cert.solver_certificate.obstruction)
    witnesses: Dict[str, List[str]] = {obs: [] for obs in obstructions}
    for obs in obstructions:
        for item_ in cert.ledger.items:
            if obs in item_.obstruction_hint:
                if item_.missing or item_.blocked or item_.provenance_fail:
                    witnesses[obs].append(item_.name)
    return {obs: tuple(names) for obs, names in witnesses.items()}


def discover_and_certify(route: str, payload: Mapping[str, Any]) -> Dict[str, Any]:
    ledger = discover_ledger(route, payload)
    cert = certify_ledger(ledger)
    witness_map = obstruction_witness_map(cert)
    return {
        "route": normalize_route(route),
        "ledger_certificate": cert.to_dict(),
        "obstruction_witness_map": witness_map,
        "all_obstructions_have_witnesses": all(witness_map.get(obs) for obs in cert.solver_certificate.obstruction),
    }


def canonical_payloads() -> Dict[str, Mapping[str, Any]]:
    return {
        "ew_open": {
            "route": "ew",
            "name": "discovery_EW_open",
            "trace_sector_closed": True,
            "source_to_scheme_registry_present": True,
            "evaluator_map_found": False,
            "codomain_transport_found": False,
            "counterterm_finite_parts_declared": False,
            "external_constants_ledger_clean": True,
            "uncertainty_protocol_declared": False,
            "target_value_consumed": False,
        },
        "ew_closed": {
            "route": "ew",
            "name": "discovery_EW_closed",
            "trace_sector_closed": True,
            "source_to_scheme_registry_present": True,
            "evaluator_map_found": True,
            "codomain_transport_found": True,
            "counterterm_finite_parts_declared": True,
            "external_constants_ledger_clean": True,
            "uncertainty_protocol_declared": True,
            "target_value_consumed": False,
        },
        "dark_open": {
            "route": "dark",
            "name": "discovery_dark_open",
            "route_built": True,
            "run_completed": True,
            "posterior_closed": False,
            "robustness_checks_passed": False,
            "target_value_consumed": False,
        },
        "gauge_codomain_open": {
            "route": "gauge",
            "name": "discovery_gauge_codomain_open",
            "local_fiber_action_defined": True,
            "codomain_map_declared": False,
            "overlap_cocycle_verified": True,
            "anomaly_check_passed": True,
        },
        "horizon_overlap_open": {
            "route": "horizon",
            "name": "discovery_horizon_overlap_open",
            "horizon_partition_defined": True,
            "area_cost_map_defined": True,
            "overlap_gluing_verified": False,
            "capacity_bound_checked": True,
        },
        "capacity_overspend": {
            "route": "capacity",
            "name": "discovery_capacity_overspend",
            "raw_capacity_load": 100,
            "capacity_budget": 25,
            "coarse_grain_factor": 2,
        },
        "provenance_smuggled": {
            "route": "provenance",
            "name": "discovery_provenance_smuggled",
            "sector": "EW",
            "inputs_used": ["alpha_em", "M_W_physical"],
            "declared_targets": ["M_W_physical"],
            "fitted_outputs": ["posterior_M_W"],
            "posterior_outputs": ["fit_pull"],
            "allowed_exogenous_inputs": ["alpha_em"],
        },
        "cstar": {
            "route": "cstar",
            "name": "discovery_flat_Cstar",
        },
        "generic_evaluator_codomain_open": {
            "route": "generic",
            "name": "discovery_generic_open",
            "sector": "GENERIC",
            "local_solution_found": True,
            "global_export_requested": True,
            "acc_base_present": True,
            "evaluator_map_found": False,
            "codomain_transport_found": False,
            "overlap_gluing_verified": True,
            "capacity_budget_verified": True,
            "capacity_overspend_detected": False,
            "empirical_or_posterior_closed": True,
            "target_value_used_as_input": False,
        },
    }


def run_canonical_discovery() -> Dict[str, Dict[str, Any]]:
    out = {}
    for key, payload in canonical_payloads().items():
        route = str(payload["route"])
        raw = dict(payload)
        raw.pop("route")
        out[key] = discover_and_certify(route, raw)
    return out


def check_T_discovery_payload_to_ledger_P() -> Dict[str, Any]:
    results = run_canonical_discovery()
    tests = {
        "all_payloads_return_ledgers": all("ledger_certificate" in r for r in results.values()),
        "all_have_items": all(len(r["ledger_certificate"]["ledger"]["items"]) > 0 for r in results.values()),
        "route_count": len(results) >= 9,
    }
    return {
        "name": "check_T_discovery_payload_to_ledger_P",
        "consistent": all(tests.values()),
        "status": "P_discovery" if all(tests.values()) else "FAIL",
        "summary": "Raw route payloads discover typed interface-structure ledgers.",
        "data": {"tests": tests, "routes": list(results.keys())},
    }


def check_T_obstruction_structure_witnesses_P() -> Dict[str, Any]:
    results = run_canonical_discovery()
    tests = {
        key: report["all_obstructions_have_witnesses"]
        for key, report in results.items()
        if report["ledger_certificate"]["certificate"]["obstruction"]
    }
    tests["has_nonzero_cases"] = len(tests) >= 6
    return {
        "name": "check_T_obstruction_structure_witnesses_P",
        "consistent": all(tests.values()),
        "status": "P_discovery" if all(tests.values()) else "FAIL",
        "summary": "Every nonzero obstruction has at least one moving-structure witness in the discovered ledger.",
        "data": {"tests": tests},
        "dependencies": ["check_T_discovery_payload_to_ledger_P"],
    }


def check_T_zero_obstruction_inventory_clean_P() -> Dict[str, Any]:
    results = run_canonical_discovery()
    clean = results["ew_closed"]
    ledger = clean["ledger_certificate"]["ledger"]
    cert = clean["ledger_certificate"]["certificate"]
    tests = {
        "ew_closed_zero_obstruction": cert["obstruction"] == tuple(),
        "ew_closed_exports": cert["solver_status"] == "SOLVED_GLOBAL_P",
        "ew_closed_no_missing_required": ledger["missing_required"] == [],
        "ew_closed_no_blocked_required": ledger["blocked_required"] == [],
        "ew_closed_no_provenance_failures": ledger["provenance_failures"] == [],
    }
    return {
        "name": "check_T_zero_obstruction_inventory_clean_P",
        "consistent": all(tests.values()),
        "status": "P_discovery" if all(tests.values()) else "FAIL",
        "summary": "A zero-obstruction export case has no missing, blocked, or provenance-failed required structures.",
        "data": {"tests": tests, "clean_certificate": cert},
        "dependencies": ["check_T_obstruction_structure_witnesses_P"],
    }


def check_T_expected_label_leakage_rejected_P() -> Dict[str, Any]:
    raw = dict(canonical_payloads()["ew_open"])
    route = raw.pop("route")
    raw["expected_status"] = "SOLVED_GLOBAL_P"
    rejected = False
    try:
        discover_and_certify(route, raw)
    except ValueError:
        rejected = True
    tests = {"expected_label_rejected": rejected}
    return {
        "name": "check_T_expected_label_leakage_rejected_P",
        "consistent": all(tests.values()),
        "status": "P_audit" if all(tests.values()) else "FAIL",
        "summary": "Discovery engine rejects expected-label/certificate leakage in payloads.",
        "data": {"tests": tests},
        "dependencies": ["check_T_zero_obstruction_inventory_clean_P"],
    }


def check_T_interface_structure_discovery_engine_P() -> Dict[str, Any]:
    subchecks = [
        check_T_discovery_payload_to_ledger_P(),
        check_T_obstruction_structure_witnesses_P(),
        check_T_zero_obstruction_inventory_clean_P(),
        check_T_expected_label_leakage_rejected_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_interface_structure_discovery_engine_P",
        "consistent": ok,
        "status": "P_discovery_engine" if ok else "FAIL",
        "summary": "Interface Structure Discovery Engine is P: raw route payloads discover typed moving-structure ledgers, certify them, and witness every obstruction.",
        "data": {
            "core_pipeline": "raw route payload -> typed ledger -> certificate -> obstruction witness map",
            "subchecks": [x["name"] for x in subchecks],
            "supported_routes": sorted(set(ROUTE_ALIASES.values())),
        },
        "dependencies": [x["name"] for x in subchecks],
    }


CHECKS = {
    "check_T_discovery_payload_to_ledger_P": check_T_discovery_payload_to_ledger_P,
    "check_T_obstruction_structure_witnesses_P": check_T_obstruction_structure_witnesses_P,
    "check_T_zero_obstruction_inventory_clean_P": check_T_zero_obstruction_inventory_clean_P,
    "check_T_expected_label_leakage_rejected_P": check_T_expected_label_leakage_rejected_P,
    "check_T_interface_structure_discovery_engine_P": check_T_interface_structure_discovery_engine_P,
}


def register(registry=None):
    if registry is None:
        return CHECKS
    if hasattr(registry, "update"):
        registry.update(CHECKS)
        return registry
    for name, fn in CHECKS.items():
        if hasattr(registry, "register"):
            registry.register(name, fn)
        elif hasattr(registry, "add"):
            registry.add(name, fn)
        else:
            raise TypeError("Unsupported registry type for interface_structure_discovery_engine.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
