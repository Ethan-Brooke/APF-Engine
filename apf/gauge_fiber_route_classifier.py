"""
Gauge-as-fiber-automorphism route classification.

Classifies whether a gauge route has enough fiber/codomain/descent data for promotion.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any

from apf.interface_solver_descent_bridge import InterfaceSolverProblem, InterfaceSolverCertificate, solve_interface_descent


@dataclass(frozen=True)
class GaugeFiberRouteInput:
    name: str
    local_fiber_action_defined: bool
    group_law_verified: bool
    representation_faithful: bool
    codomain_map_declared: bool
    overlap_cocycle_verified: bool
    anomaly_check_passed: bool
    capacity_budget_verified: bool
    target_value_consumed: bool
    notes: str = ""


def gauge_route_closed(x: GaugeFiberRouteInput) -> bool:
    return all([
        x.local_fiber_action_defined,
        x.group_law_verified,
        x.representation_faithful,
        x.codomain_map_declared,
        x.overlap_cocycle_verified,
        x.anomaly_check_passed,
        x.capacity_budget_verified,
        not x.target_value_consumed,
    ])


def to_interface_problem(x: GaugeFiberRouteInput) -> InterfaceSolverProblem:
    local = x.local_fiber_action_defined and x.group_law_verified and x.representation_faithful
    return InterfaceSolverProblem(
        name=x.name,
        sector="GAUGE",
        local_solution_found=local,
        global_export_requested=True,
        acc_base_present=True,
        evaluator_map_found=x.anomaly_check_passed,
        codomain_transport_found=x.codomain_map_declared,
        overlap_gluing_verified=x.overlap_cocycle_verified,
        capacity_budget_verified=x.capacity_budget_verified,
        capacity_overspend_detected=not x.capacity_budget_verified,
        empirical_or_posterior_closed=True,
        target_value_used_as_input=x.target_value_consumed,
        route_notes=x.notes or "gauge-as-fiber-automorphism route classification",
    )


def certify_gauge_fiber_route(x: GaugeFiberRouteInput) -> InterfaceSolverCertificate:
    return solve_interface_descent(to_interface_problem(x))


def canonical_cases() -> Dict[str, GaugeFiberRouteInput]:
    return {
        "codomain_open": GaugeFiberRouteInput(
            name="gauge_codomain_open",
            local_fiber_action_defined=True,
            group_law_verified=True,
            representation_faithful=True,
            codomain_map_declared=False,
            overlap_cocycle_verified=True,
            anomaly_check_passed=True,
            capacity_budget_verified=True,
            target_value_consumed=False,
            notes="local fiber automorphism route; codomain declaration open",
        ),
        "overlap_open": GaugeFiberRouteInput(
            name="gauge_overlap_open",
            local_fiber_action_defined=True,
            group_law_verified=True,
            representation_faithful=True,
            codomain_map_declared=True,
            overlap_cocycle_verified=False,
            anomaly_check_passed=True,
            capacity_budget_verified=True,
            target_value_consumed=False,
            notes="overlap/cocycle descent open",
        ),
        "closed_clean": GaugeFiberRouteInput(
            name="gauge_closed_clean",
            local_fiber_action_defined=True,
            group_law_verified=True,
            representation_faithful=True,
            codomain_map_declared=True,
            overlap_cocycle_verified=True,
            anomaly_check_passed=True,
            capacity_budget_verified=True,
            target_value_consumed=False,
            notes="clean hypothetical gauge descent closure",
        ),
    }


def run_cases() -> Dict[str, Dict[str, Any]]:
    out = {}
    for key, case in canonical_cases().items():
        cert = certify_gauge_fiber_route(case)
        out[key] = {
            "input": asdict(case),
            "gauge_route_closed": gauge_route_closed(case),
            "solver_status": cert.solver_status.value,
            "obstruction": cert.obstruction,
            "repair_class": cert.repair_class.value,
            "export_global_P": cert.export_global_P,
            "safe_claim": cert.safe_claim,
            "next_action": cert.next_action,
        }
    return out


def check_T_gauge_fiber_route_classifier_P() -> Dict[str, Any]:
    results = run_cases()
    tests = {
        "codomain_open_held": results["codomain_open"]["solver_status"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "codomain_obstruction": "CODOMAIN_MISMATCH" in results["codomain_open"]["obstruction"],
        "overlap_open_held": results["overlap_open"]["solver_status"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "overlap_obstruction": "OVERLAP_INCOHERENCE" in results["overlap_open"]["obstruction"],
        "closed_clean_exports": results["closed_clean"]["solver_status"] == "SOLVED_GLOBAL_P",
    }
    return {
        "name": "check_T_gauge_fiber_route_classifier_P",
        "consistent": all(tests.values()),
        "status": "P_route_cert" if all(tests.values()) else "FAIL",
        "summary": "Gauge fiber route classifier gates codomain/cocycle/descent closure.",
        "data": {"tests": tests, "results": results},
    }


CHECKS = {"check_T_gauge_fiber_route_classifier_P": check_T_gauge_fiber_route_classifier_P}


def register(registry=None):
    if registry is None:
        return CHECKS
    registry.update(CHECKS)
    return registry


def run_all() -> Dict[str, Any]:
    return {name: fn() for name, fn in CHECKS.items()}
