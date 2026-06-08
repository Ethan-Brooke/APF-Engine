"""
Horizon-area-as-fiber-cost route classification.

Classifies horizon/interface cost routes for overlap, capacity, and provenance closure.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any

from apf.interface_solver_descent_bridge import InterfaceSolverProblem, InterfaceSolverCertificate, solve_interface_descent


@dataclass(frozen=True)
class HorizonFiberCostInput:
    name: str
    horizon_partition_defined: bool
    area_cost_map_defined: bool
    overlap_gluing_verified: bool
    capacity_bound_checked: bool
    entropy_ledger_clean: bool
    codomain_transport_found: bool
    target_value_consumed: bool
    capacity_overspend_detected: bool = False
    notes: str = ""


def horizon_route_closed(x: HorizonFiberCostInput) -> bool:
    return all([
        x.horizon_partition_defined,
        x.area_cost_map_defined,
        x.overlap_gluing_verified,
        x.capacity_bound_checked,
        x.entropy_ledger_clean,
        x.codomain_transport_found,
        not x.target_value_consumed,
        not x.capacity_overspend_detected,
    ])


def to_interface_problem(x: HorizonFiberCostInput) -> InterfaceSolverProblem:
    local = x.horizon_partition_defined and x.area_cost_map_defined and x.entropy_ledger_clean
    return InterfaceSolverProblem(
        name=x.name,
        sector="HORIZON",
        local_solution_found=local,
        global_export_requested=True,
        acc_base_present=True,
        evaluator_map_found=x.area_cost_map_defined and x.entropy_ledger_clean,
        codomain_transport_found=x.codomain_transport_found,
        overlap_gluing_verified=x.overlap_gluing_verified,
        capacity_budget_verified=x.capacity_bound_checked,
        capacity_overspend_detected=x.capacity_overspend_detected,
        empirical_or_posterior_closed=True,
        target_value_used_as_input=x.target_value_consumed,
        route_notes=x.notes or "horizon-area-as-fiber-cost route classification",
    )


def certify_horizon_fiber_cost_route(x: HorizonFiberCostInput) -> InterfaceSolverCertificate:
    return solve_interface_descent(to_interface_problem(x))


def canonical_cases() -> Dict[str, HorizonFiberCostInput]:
    return {
        "overlap_open": HorizonFiberCostInput(
            name="horizon_overlap_open",
            horizon_partition_defined=True,
            area_cost_map_defined=True,
            overlap_gluing_verified=False,
            capacity_bound_checked=True,
            entropy_ledger_clean=True,
            codomain_transport_found=True,
            target_value_consumed=False,
            notes="horizon/interface overlap gluing open",
        ),
        "capacity_open": HorizonFiberCostInput(
            name="horizon_capacity_open",
            horizon_partition_defined=True,
            area_cost_map_defined=True,
            overlap_gluing_verified=True,
            capacity_bound_checked=False,
            entropy_ledger_clean=True,
            codomain_transport_found=True,
            target_value_consumed=False,
            capacity_overspend_detected=True,
            notes="capacity bound open / overspend detected",
        ),
        "closed_clean": HorizonFiberCostInput(
            name="horizon_closed_clean",
            horizon_partition_defined=True,
            area_cost_map_defined=True,
            overlap_gluing_verified=True,
            capacity_bound_checked=True,
            entropy_ledger_clean=True,
            codomain_transport_found=True,
            target_value_consumed=False,
            notes="clean hypothetical horizon route closure",
        ),
    }


def run_cases() -> Dict[str, Dict[str, Any]]:
    out = {}
    for key, case in canonical_cases().items():
        cert = certify_horizon_fiber_cost_route(case)
        out[key] = {
            "input": asdict(case),
            "horizon_route_closed": horizon_route_closed(case),
            "solver_status": cert.solver_status.value,
            "obstruction": cert.obstruction,
            "repair_class": cert.repair_class.value,
            "export_global_P": cert.export_global_P,
            "safe_claim": cert.safe_claim,
            "next_action": cert.next_action,
        }
    return out


def check_T_horizon_fiber_cost_classifier_P() -> Dict[str, Any]:
    results = run_cases()
    tests = {
        "overlap_open_held": results["overlap_open"]["solver_status"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "overlap_obstruction": "OVERLAP_INCOHERENCE" in results["overlap_open"]["obstruction"],
        "capacity_open_held": results["capacity_open"]["solver_status"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "capacity_obstruction": "CAPACITY_OVERSPEND" in results["capacity_open"]["obstruction"],
        "closed_clean_exports": results["closed_clean"]["solver_status"] == "SOLVED_GLOBAL_P",
    }
    return {
        "name": "check_T_horizon_fiber_cost_classifier_P",
        "consistent": all(tests.values()),
        "status": "P_route_cert" if all(tests.values()) else "FAIL",
        "summary": "Horizon fiber-cost classifier gates overlap and capacity closure.",
        "data": {"tests": tests, "results": results},
    }


CHECKS = {"check_T_horizon_fiber_cost_classifier_P": check_T_horizon_fiber_cost_classifier_P}


def register(registry=None):
    if registry is None:
        return CHECKS
    registry.update(CHECKS)
    return registry


def run_all() -> Dict[str, Any]:
    return {name: fn() for name, fn in CHECKS.items()}
