"""
APF Route Certification Integration Workbench.

Route-specific JSON adapter layer for engineering integration.

This module gives another AI or solver process a stable JSON-oriented API:

    route + JSON payload -> certificate report

Supported routes:
    ew
    dark
    gauge
    horizon
    capacity
    provenance
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Mapping

from apf.ew_trace_scheme_transport_certifier import EWTraceSchemeTransportInput, certify_ew_trace_scheme_transport
from apf.dark_posterior_certifier import DarkPosteriorRunInput, certify_dark_posterior_run
from apf.gauge_fiber_route_classifier import GaugeFiberRouteInput, certify_gauge_fiber_route
from apf.horizon_fiber_cost_classifier import HorizonFiberCostInput, certify_horizon_fiber_cost_route
from apf.capacity_coarse_grain_experiments import CapacityCoarseGrainExperiment, certify_capacity_experiment, effective_load, minimum_factor_to_fit, overspend_detected
from apf.anti_fitting_provenance_audit import ProvenanceAuditInput, audit_provenance, smuggled_symbols, target_value_consumed
from apf.interface_solver_descent_bridge import certificate_data


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
}


def normalize_route(route: str) -> str:
    key = route.strip().lower().replace("-", "_")
    if key not in ROUTE_ALIASES:
        raise ValueError(f"Unsupported route '{route}'. Supported: {sorted(set(ROUTE_ALIASES.values()))}")
    return ROUTE_ALIASES[key]


def _reject_expected_fields(payload: Mapping[str, Any]) -> None:
    forbidden = {
        "expected_status",
        "expected_label",
        "expected_repair_class",
        "solver_status",
        "promotion_status",
        "repair_class",
        "export_global_P",
        "obstruction",
        "safe_claim",
    }
    leaked = sorted(set(payload) & forbidden)
    if leaked:
        raise ValueError(f"Expected-label/promotion fields are forbidden in route payload: {leaked}")


def _tupleize(payload: Dict[str, Any], *fields: str) -> Dict[str, Any]:
    out = dict(payload)
    for field in fields:
        if field in out and isinstance(out[field], list):
            out[field] = tuple(out[field])
    return out


def certify_route_payload(route: str, payload: Mapping[str, Any]) -> Dict[str, Any]:
    """Certify one route payload and return a JSONable report."""
    route = normalize_route(route)
    _reject_expected_fields(payload)
    raw = dict(payload)

    if route == "ew":
        inp = EWTraceSchemeTransportInput(**raw)
        cert = certify_ew_trace_scheme_transport(inp)
        extras = {}
    elif route == "dark":
        inp = DarkPosteriorRunInput(**raw)
        cert = certify_dark_posterior_run(inp)
        extras = {}
    elif route == "gauge":
        inp = GaugeFiberRouteInput(**raw)
        cert = certify_gauge_fiber_route(inp)
        extras = {}
    elif route == "horizon":
        inp = HorizonFiberCostInput(**raw)
        cert = certify_horizon_fiber_cost_route(inp)
        extras = {}
    elif route == "capacity":
        inp = CapacityCoarseGrainExperiment(**raw)
        cert = certify_capacity_experiment(inp)
        extras = {
            "effective_load": effective_load(inp),
            "minimum_factor_to_fit": minimum_factor_to_fit(inp.raw_capacity_load, inp.capacity_budget),
            "overspend_detected": overspend_detected(inp),
        }
    elif route == "provenance":
        raw = _tupleize(raw, "inputs_used", "declared_targets", "fitted_outputs", "posterior_outputs", "allowed_exogenous_inputs")
        inp = ProvenanceAuditInput(**raw)
        cert = audit_provenance(inp)
        extras = {
            "smuggled_symbols": smuggled_symbols(inp),
            "target_value_consumed": target_value_consumed(inp),
        }
    else:  # pragma: no cover
        raise AssertionError(route)

    return {
        "route": route,
        "input": asdict(inp),
        "certificate": certificate_data(cert),
        "extras": extras,
    }


def certify_route_file(route: str, payload: Any) -> Dict[str, Any]:
    """Certify either a single payload dict or {"cases": [...]} / list of payload dicts."""
    if isinstance(payload, Mapping) and "cases" in payload:
        cases = payload["cases"]
    elif isinstance(payload, list):
        cases = payload
    else:
        cases = [payload]

    if not isinstance(cases, list):
        raise ValueError("Route payload must be a dict, a list, or {'cases': [...]}")

    reports = [certify_route_payload(route, case) for case in cases]
    status_counts: Dict[str, int] = {}
    for report in reports:
        status = report["certificate"]["solver_status"]
        status_counts[status] = status_counts.get(status, 0) + 1

    return {
        "route": normalize_route(route),
        "case_count": len(reports),
        "status_counts": status_counts,
        "global_exports": [
            r["certificate"]["problem_name"]
            for r in reports
            if r["certificate"]["export_global_P"]
        ],
        "held_or_failed": [
            r["certificate"]["problem_name"]
            for r in reports
            if not r["certificate"]["export_global_P"]
        ],
        "reports": reports,
    }


def check_T_route_workbench_payload_certification_P() -> Dict[str, Any]:
    cases = {
        "ew": {
            "name": "wb_EW_open",
            "trace_sector_closed": True,
            "source_to_scheme_registry_present": True,
            "evaluator_map_found": False,
            "codomain_transport_found": False,
            "counterterm_finite_parts_declared": False,
            "external_constants_ledger_clean": True,
            "uncertainty_protocol_declared": False,
            "target_value_consumed": False
        },
        "dark": {
            "name": "wb_dark_open",
            "route_built": True,
            "run_completed": True,
            "chains_converged": False,
            "posterior_closed": False,
            "robustness_checks_passed": False,
            "data_ledger_clean": True,
            "evaluator_map_found": False,
            "codomain_transport_found": True,
            "target_value_consumed": False
        },
        "gauge": {
            "name": "wb_gauge_codomain_open",
            "local_fiber_action_defined": True,
            "group_law_verified": True,
            "representation_faithful": True,
            "codomain_map_declared": False,
            "overlap_cocycle_verified": True,
            "anomaly_check_passed": True,
            "capacity_budget_verified": True,
            "target_value_consumed": False
        },
        "horizon": {
            "name": "wb_horizon_overlap_open",
            "horizon_partition_defined": True,
            "area_cost_map_defined": True,
            "overlap_gluing_verified": False,
            "capacity_bound_checked": True,
            "entropy_ledger_clean": True,
            "codomain_transport_found": True,
            "target_value_consumed": False
        },
        "capacity": {
            "name": "wb_capacity_overspend",
            "raw_capacity_load": 100,
            "capacity_budget": 25,
            "coarse_grain_factor": 2
        },
        "provenance": {
            "name": "wb_prov_target",
            "sector": "EW",
            "inputs_used": ["alpha_em", "M_W_physical"],
            "declared_targets": ["M_W_physical"],
            "fitted_outputs": ["posterior_M_W"],
            "posterior_outputs": ["fit_pull"],
            "allowed_exogenous_inputs": ["alpha_em"]
        }
    }
    results = {route: certify_route_payload(route, payload) for route, payload in cases.items()}
    tests = {
        "ew_held": results["ew"]["certificate"]["solver_status"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "dark_held": results["dark"]["certificate"]["solver_status"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "gauge_held": results["gauge"]["certificate"]["solver_status"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "horizon_held": results["horizon"]["certificate"]["solver_status"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "capacity_held": results["capacity"]["certificate"]["solver_status"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "provenance_fail_closed": results["provenance"]["certificate"]["solver_status"] == "FAIL_CLOSED_PROVENANCE",
        "capacity_extras_present": results["capacity"]["extras"]["effective_load"] == 50,
        "provenance_symbol_detected": "m_w_physical" in results["provenance"]["extras"]["smuggled_symbols"],
    }
    leakage_rejected = False
    try:
        bad = dict(cases["ew"])
        bad["expected_status"] = "SOLVED_GLOBAL_P"
        certify_route_payload("ew", bad)
    except ValueError:
        leakage_rejected = True
    tests["expected_label_rejected"] = leakage_rejected
    return {
        "name": "check_T_route_workbench_payload_certification_P",
        "consistent": all(tests.values()),
        "status": "P_workbench" if all(tests.values()) else "FAIL",
        "summary": "Route workbench certifies JSON payloads for all six starter routes and rejects expected-label leakage.",
        "data": {"tests": tests, "results": results},
    }


CHECKS = {"check_T_route_workbench_payload_certification_P": check_T_route_workbench_payload_certification_P}


def register(registry=None):
    if registry is None:
        return CHECKS
    registry.update(CHECKS)
    return registry


def run_all() -> Dict[str, Any]:
    return {name: fn() for name, fn in CHECKS.items()}
