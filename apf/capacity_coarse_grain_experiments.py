"""
Capacity overspend / coarse-graining experiments.

Provides engineering helpers for testing whether a coarse-graining factor relieves
capacity overspend enough for promotion.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from math import ceil
from typing import Dict, Any, Optional

from apf.interface_solver_descent_bridge import InterfaceSolverProblem, InterfaceSolverCertificate, solve_interface_descent


@dataclass(frozen=True)
class CapacityCoarseGrainExperiment:
    name: str
    raw_capacity_load: int
    capacity_budget: int
    coarse_grain_factor: int
    evaluator_map_found: bool = True
    codomain_transport_found: bool = True
    overlap_gluing_verified: bool = True
    target_value_consumed: bool = False
    notes: str = ""


def effective_load(x: CapacityCoarseGrainExperiment) -> int:
    if x.coarse_grain_factor <= 0:
        raise ValueError("coarse_grain_factor must be positive")
    return ceil(x.raw_capacity_load / x.coarse_grain_factor)


def overspend_detected(x: CapacityCoarseGrainExperiment) -> bool:
    return effective_load(x) > x.capacity_budget


def minimum_factor_to_fit(raw_capacity_load: int, capacity_budget: int) -> int:
    if capacity_budget <= 0:
        raise ValueError("capacity_budget must be positive")
    return max(1, ceil(raw_capacity_load / capacity_budget))


def to_interface_problem(x: CapacityCoarseGrainExperiment) -> InterfaceSolverProblem:
    return InterfaceSolverProblem(
        name=x.name,
        sector="CAPACITY",
        local_solution_found=True,
        global_export_requested=True,
        acc_base_present=True,
        evaluator_map_found=x.evaluator_map_found,
        codomain_transport_found=x.codomain_transport_found,
        overlap_gluing_verified=x.overlap_gluing_verified,
        capacity_budget_verified=not overspend_detected(x),
        capacity_overspend_detected=overspend_detected(x),
        empirical_or_posterior_closed=True,
        target_value_used_as_input=x.target_value_consumed,
        route_notes=x.notes or f"effective_load={effective_load(x)} budget={x.capacity_budget}",
    )


def certify_capacity_experiment(x: CapacityCoarseGrainExperiment) -> InterfaceSolverCertificate:
    return solve_interface_descent(to_interface_problem(x))


def recommend_next_factor(x: CapacityCoarseGrainExperiment) -> int:
    return minimum_factor_to_fit(x.raw_capacity_load, x.capacity_budget)


def canonical_cases() -> Dict[str, CapacityCoarseGrainExperiment]:
    return {
        "overspend_before_grain": CapacityCoarseGrainExperiment(
            name="capacity_overspend_before_grain",
            raw_capacity_load=100,
            capacity_budget=25,
            coarse_grain_factor=2,
            notes="still overspent",
        ),
        "fits_after_grain": CapacityCoarseGrainExperiment(
            name="capacity_fits_after_grain",
            raw_capacity_load=100,
            capacity_budget=25,
            coarse_grain_factor=4,
            notes="fits exactly after coarse-graining",
        ),
        "target_smuggled": CapacityCoarseGrainExperiment(
            name="capacity_target_smuggled",
            raw_capacity_load=100,
            capacity_budget=25,
            coarse_grain_factor=4,
            target_value_consumed=True,
            notes="fits capacity but fails provenance",
        ),
    }


def run_cases() -> Dict[str, Dict[str, Any]]:
    out = {}
    for key, case in canonical_cases().items():
        cert = certify_capacity_experiment(case)
        out[key] = {
            "input": asdict(case),
            "effective_load": effective_load(case),
            "minimum_factor_to_fit": recommend_next_factor(case),
            "overspend_detected": overspend_detected(case),
            "solver_status": cert.solver_status.value,
            "obstruction": cert.obstruction,
            "repair_class": cert.repair_class.value,
            "export_global_P": cert.export_global_P,
            "safe_claim": cert.safe_claim,
            "next_action": cert.next_action,
        }
    return out


def check_T_capacity_coarse_grain_experiments_P() -> Dict[str, Any]:
    results = run_cases()
    tests = {
        "overspend_held": results["overspend_before_grain"]["solver_status"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "overspend_has_capacity": "CAPACITY_OVERSPEND" in results["overspend_before_grain"]["obstruction"],
        "fits_exports": results["fits_after_grain"]["solver_status"] == "SOLVED_GLOBAL_P",
        "minimum_factor_correct": results["fits_after_grain"]["minimum_factor_to_fit"] == 4,
        "target_smuggled_fails_closed": results["target_smuggled"]["solver_status"] == "FAIL_CLOSED_PROVENANCE",
    }
    return {
        "name": "check_T_capacity_coarse_grain_experiments_P",
        "consistent": all(tests.values()),
        "status": "P_route_cert" if all(tests.values()) else "FAIL",
        "summary": "Capacity/coarse-graining experiments certify overspend relief and provenance boundaries.",
        "data": {"tests": tests, "results": results},
    }


CHECKS = {"check_T_capacity_coarse_grain_experiments_P": check_T_capacity_coarse_grain_experiments_P}


def register(registry=None):
    if registry is None:
        return CHECKS
    registry.update(CHECKS)
    return registry


def run_all() -> Dict[str, Any]:
    return {name: fn() for name, fn in CHECKS.items()}
