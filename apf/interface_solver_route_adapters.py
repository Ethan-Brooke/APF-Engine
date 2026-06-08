"""
APF Route Adapter Templates.

Adapters for turning solver-specific dictionaries into InterfaceSolverProblem objects.

Use these as templates for real route modules.
"""

from __future__ import annotations

from typing import Any, Dict, Mapping

from apf.interface_solver_contracts import problem_from_dict
from apf.interface_solver_descent_bridge import InterfaceSolverProblem


def from_generic_solver_result(result: Mapping[str, Any], *, strict: bool = True) -> InterfaceSolverProblem:
    """Adapt a generic solver result dict.

    Expected raw keys are InterfaceSolverProblem fields.
    Expected-label/promotion fields are rejected by problem_from_dict.
    """
    return problem_from_dict(result, strict=strict)


def ew_trace_to_scheme_problem(
    *,
    name: str,
    trace_local_closed: bool,
    evaluator_map_found: bool,
    codomain_transport_found: bool,
    notes: str = "",
) -> InterfaceSolverProblem:
    return InterfaceSolverProblem(
        name=name,
        sector="EW",
        local_solution_found=trace_local_closed,
        global_export_requested=True,
        acc_base_present=True,
        evaluator_map_found=evaluator_map_found,
        codomain_transport_found=codomain_transport_found,
        overlap_gluing_verified=True,
        capacity_budget_verified=True,
        capacity_overspend_detected=False,
        empirical_or_posterior_closed=True,
        target_value_used_as_input=False,
        route_notes=notes,
    )


def dark_empirical_problem(
    *,
    name: str,
    local_route_found: bool,
    posterior_closed: bool,
    evaluator_map_found: bool,
    notes: str = "",
) -> InterfaceSolverProblem:
    return InterfaceSolverProblem(
        name=name,
        sector="DARK",
        local_solution_found=local_route_found,
        global_export_requested=True,
        acc_base_present=True,
        evaluator_map_found=evaluator_map_found,
        codomain_transport_found=True,
        overlap_gluing_verified=True,
        capacity_budget_verified=True,
        capacity_overspend_detected=False,
        empirical_or_posterior_closed=posterior_closed,
        target_value_used_as_input=False,
        route_notes=notes,
    )
