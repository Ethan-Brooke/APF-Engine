"""
Dark-sector run/posterior certification.

Certifies whether a dark-sector run has enough empirical/posterior closure to be promoted.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any

from apf.interface_solver_descent_bridge import InterfaceSolverProblem, InterfaceSolverCertificate, solve_interface_descent


@dataclass(frozen=True)
class DarkPosteriorRunInput:
    name: str
    route_built: bool
    run_completed: bool
    chains_converged: bool
    posterior_closed: bool
    robustness_checks_passed: bool
    data_ledger_clean: bool
    evaluator_map_found: bool
    codomain_transport_found: bool
    target_value_consumed: bool
    capacity_budget_verified: bool = True
    capacity_overspend_detected: bool = False
    notes: str = ""


def posterior_certified(x: DarkPosteriorRunInput) -> bool:
    return all([
        x.route_built,
        x.run_completed,
        x.chains_converged,
        x.posterior_closed,
        x.robustness_checks_passed,
        x.data_ledger_clean,
        x.evaluator_map_found,
        x.codomain_transport_found,
        not x.target_value_consumed,
        x.capacity_budget_verified,
        not x.capacity_overspend_detected,
    ])


def to_interface_problem(x: DarkPosteriorRunInput) -> InterfaceSolverProblem:
    empirical_closed = (
        x.chains_converged
        and x.posterior_closed
        and x.robustness_checks_passed
        and x.data_ledger_clean
    )
    evaluator_closed = x.evaluator_map_found and empirical_closed
    return InterfaceSolverProblem(
        name=x.name,
        sector="DARK",
        local_solution_found=x.route_built and x.run_completed,
        global_export_requested=True,
        acc_base_present=True,
        evaluator_map_found=evaluator_closed,
        codomain_transport_found=x.codomain_transport_found,
        overlap_gluing_verified=True,
        capacity_budget_verified=x.capacity_budget_verified,
        capacity_overspend_detected=x.capacity_overspend_detected,
        empirical_or_posterior_closed=empirical_closed,
        target_value_used_as_input=x.target_value_consumed,
        route_notes=x.notes or "dark-sector posterior certification",
    )


def certify_dark_posterior_run(x: DarkPosteriorRunInput) -> InterfaceSolverCertificate:
    return solve_interface_descent(to_interface_problem(x))


def canonical_cases() -> Dict[str, DarkPosteriorRunInput]:
    return {
        "runtime_success_convergence_open": DarkPosteriorRunInput(
            name="dark_runtime_success_convergence_open",
            route_built=True,
            run_completed=True,
            chains_converged=False,
            posterior_closed=False,
            robustness_checks_passed=False,
            data_ledger_clean=True,
            evaluator_map_found=False,
            codomain_transport_found=True,
            target_value_consumed=False,
            notes="Runtime success but posterior/convergence/robustness open.",
        ),
        "posterior_closed_clean": DarkPosteriorRunInput(
            name="dark_posterior_closed_clean",
            route_built=True,
            run_completed=True,
            chains_converged=True,
            posterior_closed=True,
            robustness_checks_passed=True,
            data_ledger_clean=True,
            evaluator_map_found=True,
            codomain_transport_found=True,
            target_value_consumed=False,
            notes="Clean hypothetical posterior closure.",
        ),
        "target_smuggled": DarkPosteriorRunInput(
            name="dark_target_smuggled",
            route_built=True,
            run_completed=True,
            chains_converged=True,
            posterior_closed=True,
            robustness_checks_passed=True,
            data_ledger_clean=True,
            evaluator_map_found=True,
            codomain_transport_found=True,
            target_value_consumed=True,
            notes="Bad route: posterior/target consumed as input.",
        ),
    }


def run_cases() -> Dict[str, Dict[str, Any]]:
    out = {}
    for key, case in canonical_cases().items():
        cert = certify_dark_posterior_run(case)
        out[key] = {
            "input": asdict(case),
            "posterior_certified": posterior_certified(case),
            "solver_status": cert.solver_status.value,
            "promotion_status": cert.promotion_status.value,
            "repair_class": cert.repair_class.value,
            "obstruction": cert.obstruction,
            "export_global_P": cert.export_global_P,
            "safe_claim": cert.safe_claim,
            "next_action": cert.next_action,
        }
    return out


def check_T_dark_posterior_certifier_P() -> Dict[str, Any]:
    results = run_cases()
    tests = {
        "open_runtime_held": results["runtime_success_convergence_open"]["solver_status"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "open_runtime_has_evaluator": "EVALUATOR_MISSING" in results["runtime_success_convergence_open"]["obstruction"],
        "closed_clean_exports": results["posterior_closed_clean"]["solver_status"] == "SOLVED_GLOBAL_P",
        "target_smuggled_fails_closed": results["target_smuggled"]["solver_status"] == "FAIL_CLOSED_PROVENANCE",
    }
    return {
        "name": "check_T_dark_posterior_certifier_P",
        "consistent": all(tests.values()),
        "status": "P_route_cert" if all(tests.values()) else "FAIL",
        "summary": "Dark-sector posterior certifier separates runtime success from posterior/global P closure.",
        "data": {"tests": tests, "results": results},
    }


CHECKS = {"check_T_dark_posterior_certifier_P": check_T_dark_posterior_certifier_P}


def register(registry=None):
    if registry is None:
        return CHECKS
    registry.update(CHECKS)
    return registry


def run_all() -> Dict[str, Any]:
    return {name: fn() for name, fn in CHECKS.items()}
