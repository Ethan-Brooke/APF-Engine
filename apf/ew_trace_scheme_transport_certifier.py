"""
EW Trace-to-Scheme Transport Certification.

Certifies whether a locally closed EW/APF_TRACE route can honestly be promoted to
physical scheme export.

This module does not compute masses. It certifies the transport gate:
    APF_TRACE -> physical scheme masses

Expected high-value use:
    prevent APF_TRACE local closure from being mislabeled as physical scheme P.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Mapping, Any, Iterable, Optional

from apf.interface_solver_descent_bridge import InterfaceSolverProblem, InterfaceSolverCertificate, solve_interface_descent


@dataclass(frozen=True)
class EWTraceSchemeTransportInput:
    name: str
    trace_sector_closed: bool
    source_to_scheme_registry_present: bool
    evaluator_map_found: bool
    codomain_transport_found: bool
    counterterm_finite_parts_declared: bool
    external_constants_ledger_clean: bool
    uncertainty_protocol_declared: bool
    target_value_consumed: bool
    overlap_gluing_verified: bool = True
    capacity_budget_verified: bool = True
    capacity_overspend_detected: bool = False
    notes: str = ""


def ew_transport_ready(x: EWTraceSchemeTransportInput) -> bool:
    return all([
        x.trace_sector_closed,
        x.source_to_scheme_registry_present,
        x.evaluator_map_found,
        x.codomain_transport_found,
        x.counterterm_finite_parts_declared,
        x.external_constants_ledger_clean,
        x.uncertainty_protocol_declared,
        not x.target_value_consumed,
        x.overlap_gluing_verified,
        x.capacity_budget_verified,
        not x.capacity_overspend_detected,
    ])


def to_interface_problem(x: EWTraceSchemeTransportInput) -> InterfaceSolverProblem:
    # Missing registry/counterterms/constants/uncertainty are represented as evaluator
    # non-closure because the physical export evaluator is not fully declared.
    evaluator_closed = (
        x.evaluator_map_found
        and x.source_to_scheme_registry_present
        and x.counterterm_finite_parts_declared
        and x.external_constants_ledger_clean
        and x.uncertainty_protocol_declared
    )
    return InterfaceSolverProblem(
        name=x.name,
        sector="EW",
        local_solution_found=x.trace_sector_closed,
        global_export_requested=True,
        acc_base_present=True,
        evaluator_map_found=evaluator_closed,
        codomain_transport_found=x.codomain_transport_found,
        overlap_gluing_verified=x.overlap_gluing_verified,
        capacity_budget_verified=x.capacity_budget_verified,
        capacity_overspend_detected=x.capacity_overspend_detected,
        empirical_or_posterior_closed=True,
        target_value_used_as_input=x.target_value_consumed,
        route_notes=x.notes or "EW trace-to-scheme transport certification",
    )


def certify_ew_trace_scheme_transport(x: EWTraceSchemeTransportInput) -> InterfaceSolverCertificate:
    return solve_interface_descent(to_interface_problem(x))


def canonical_cases() -> Dict[str, EWTraceSchemeTransportInput]:
    return {
        "trace_closed_transport_open": EWTraceSchemeTransportInput(
            name="EW_trace_closed_transport_open",
            trace_sector_closed=True,
            source_to_scheme_registry_present=True,
            evaluator_map_found=False,
            codomain_transport_found=False,
            counterterm_finite_parts_declared=False,
            external_constants_ledger_clean=True,
            uncertainty_protocol_declared=False,
            target_value_consumed=False,
            notes="APF_TRACE local closure; physical scheme transport not closed.",
        ),
        "transport_closed_clean": EWTraceSchemeTransportInput(
            name="EW_transport_closed_clean",
            trace_sector_closed=True,
            source_to_scheme_registry_present=True,
            evaluator_map_found=True,
            codomain_transport_found=True,
            counterterm_finite_parts_declared=True,
            external_constants_ledger_clean=True,
            uncertainty_protocol_declared=True,
            target_value_consumed=False,
            notes="Clean hypothetical full transport closure.",
        ),
        "target_smuggled": EWTraceSchemeTransportInput(
            name="EW_target_smuggled",
            trace_sector_closed=True,
            source_to_scheme_registry_present=True,
            evaluator_map_found=True,
            codomain_transport_found=True,
            counterterm_finite_parts_declared=True,
            external_constants_ledger_clean=True,
            uncertainty_protocol_declared=True,
            target_value_consumed=True,
            notes="Bad route: target value used as input.",
        ),
    }


def run_cases() -> Dict[str, Dict[str, Any]]:
    out = {}
    for key, case in canonical_cases().items():
        cert = certify_ew_trace_scheme_transport(case)
        out[key] = {
            "input": asdict(case),
            "transport_ready": ew_transport_ready(case),
            "solver_status": cert.solver_status.value,
            "promotion_status": cert.promotion_status.value,
            "repair_class": cert.repair_class.value,
            "obstruction": cert.obstruction,
            "export_global_P": cert.export_global_P,
            "safe_claim": cert.safe_claim,
            "next_action": cert.next_action,
        }
    return out


def check_T_EW_trace_scheme_transport_certifier_P() -> Dict[str, Any]:
    results = run_cases()
    tests = {
        "open_transport_held": results["trace_closed_transport_open"]["solver_status"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "open_transport_has_evaluator": "EVALUATOR_MISSING" in results["trace_closed_transport_open"]["obstruction"],
        "open_transport_has_codomain": "CODOMAIN_MISMATCH" in results["trace_closed_transport_open"]["obstruction"],
        "closed_clean_exports": results["transport_closed_clean"]["solver_status"] == "SOLVED_GLOBAL_P",
        "target_smuggled_fails_closed": results["target_smuggled"]["solver_status"] == "FAIL_CLOSED_PROVENANCE",
    }
    return {
        "name": "check_T_EW_trace_scheme_transport_certifier_P",
        "consistent": all(tests.values()),
        "status": "P_route_cert" if all(tests.values()) else "FAIL",
        "summary": "EW trace-to-scheme transport certifier gates APF_TRACE local closure vs physical scheme export.",
        "data": {"tests": tests, "results": results},
    }


CHECKS = {"check_T_EW_trace_scheme_transport_certifier_P": check_T_EW_trace_scheme_transport_certifier_P}


def register(registry=None):
    if registry is None:
        return CHECKS
    registry.update(CHECKS)
    return registry


def run_all() -> Dict[str, Any]:
    return {name: fn() for name, fn in CHECKS.items()}
