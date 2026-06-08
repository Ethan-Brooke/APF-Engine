"""
APF Interface Solver Contracts.

Strict schemas and validation helpers for engineering integration.

This layer prevents external solver modules or another AI from sneaking expected labels
into the certification path. The only allowed route into certification is raw solver
metadata -> InterfaceSolverProblem -> solve_interface_descent.
"""

from __future__ import annotations

from dataclasses import asdict, fields
from typing import Any, Dict, Iterable, Mapping, Tuple

from apf.interface_solver_descent_bridge import InterfaceSolverProblem


FORBIDDEN_LABEL_FIELDS = {
    "expected_status",
    "expected_label",
    "expected_repair_class",
    "promotion_status",
    "solver_status",
    "export_global_P",
    "safe_claim",
    "obstruction",
    "repair_class",
}

REQUIRED_FIELDS = {f.name for f in fields(InterfaceSolverProblem)}

OPTIONAL_DEFAULTS = {
    "requires_substrate_polarity": False,
    "requires_substrate_reversal": False,
    "requires_complex_action": False,
    "requires_operator_norm": False,
    "route_notes": "",
}


def validate_problem_dict(raw: Mapping[str, Any], *, strict: bool = True) -> Dict[str, Any]:
    """Validate a raw dictionary intended to become an InterfaceSolverProblem.

    strict=True rejects unknown fields. Expected-label fields are always rejected.
    """
    keys = set(raw.keys())
    leaked = keys & FORBIDDEN_LABEL_FIELDS
    if leaked:
        raise ValueError(f"Expected-label/promotion fields are forbidden in solver input: {sorted(leaked)}")

    allowed = REQUIRED_FIELDS
    unknown = keys - allowed
    if strict and unknown:
        raise ValueError(f"Unknown fields for InterfaceSolverProblem: {sorted(unknown)}")

    values = dict(raw)
    for key, value in OPTIONAL_DEFAULTS.items():
        values.setdefault(key, value)

    missing = REQUIRED_FIELDS - set(values.keys())
    if missing:
        raise ValueError(f"Missing required InterfaceSolverProblem fields: {sorted(missing)}")

    return values


def problem_from_dict(raw: Mapping[str, Any], *, strict: bool = True) -> InterfaceSolverProblem:
    values = validate_problem_dict(raw, strict=strict)
    return InterfaceSolverProblem(**{k: values[k] for k in REQUIRED_FIELDS})


def problem_to_dict(problem: InterfaceSolverProblem) -> Dict[str, Any]:
    return asdict(problem)


def load_problem_list(payload: Any, *, strict: bool = True) -> Tuple[InterfaceSolverProblem, ...]:
    """Accept either {"problems": [...]} or a bare list of problem dictionaries."""
    if isinstance(payload, Mapping):
        items = payload.get("problems")
        if items is None:
            raise ValueError("Payload mapping must contain a 'problems' list.")
    elif isinstance(payload, list):
        items = payload
    else:
        raise ValueError("Payload must be a list or a mapping with 'problems'.")

    if not isinstance(items, list):
        raise ValueError("'problems' must be a list.")

    return tuple(problem_from_dict(item, strict=strict) for item in items)


def example_problem_dicts() -> Tuple[Dict[str, Any], ...]:
    return (
        {
            "name": "eng_clean_ACC",
            "sector": "ACC",
            "local_solution_found": True,
            "global_export_requested": True,
            "acc_base_present": True,
            "evaluator_map_found": True,
            "codomain_transport_found": True,
            "overlap_gluing_verified": True,
            "capacity_budget_verified": True,
            "capacity_overspend_detected": False,
            "empirical_or_posterior_closed": True,
            "target_value_used_as_input": False,
        },
        {
            "name": "eng_EW_trace_open_transport",
            "sector": "EW",
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
            "route_notes": "trace-sector closure exists; scheme transport open",
        },
    )
