"""
Anti-fitting / provenance-smuggling audits.

Detects target-consuming or post-hoc derivations before promotion.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any, Tuple, Iterable, Set

from apf.interface_solver_descent_bridge import InterfaceSolverProblem, InterfaceSolverCertificate, solve_interface_descent


def _norm(x: str) -> str:
    return x.strip().lower().replace(" ", "_")


@dataclass(frozen=True)
class ProvenanceAuditInput:
    name: str
    sector: str
    inputs_used: Tuple[str, ...]
    declared_targets: Tuple[str, ...]
    fitted_outputs: Tuple[str, ...]
    posterior_outputs: Tuple[str, ...]
    allowed_exogenous_inputs: Tuple[str, ...]
    local_solution_found: bool = True
    evaluator_map_found: bool = True
    codomain_transport_found: bool = True
    overlap_gluing_verified: bool = True
    capacity_budget_verified: bool = True
    notes: str = ""


def smuggled_symbols(x: ProvenanceAuditInput) -> Tuple[str, ...]:
    inputs = {_norm(v) for v in x.inputs_used}
    forbidden = {_norm(v) for v in x.declared_targets + x.fitted_outputs + x.posterior_outputs}
    allowed = {_norm(v) for v in x.allowed_exogenous_inputs}
    bad = sorted((inputs & forbidden) - allowed)
    return tuple(bad)


def target_value_consumed(x: ProvenanceAuditInput) -> bool:
    return len(smuggled_symbols(x)) > 0


def to_interface_problem(x: ProvenanceAuditInput) -> InterfaceSolverProblem:
    return InterfaceSolverProblem(
        name=x.name,
        sector=x.sector,
        local_solution_found=x.local_solution_found,
        global_export_requested=True,
        acc_base_present=True,
        evaluator_map_found=x.evaluator_map_found,
        codomain_transport_found=x.codomain_transport_found,
        overlap_gluing_verified=x.overlap_gluing_verified,
        capacity_budget_verified=x.capacity_budget_verified,
        capacity_overspend_detected=not x.capacity_budget_verified,
        empirical_or_posterior_closed=True,
        target_value_used_as_input=target_value_consumed(x),
        route_notes=x.notes or f"smuggled_symbols={smuggled_symbols(x)}",
    )


def audit_provenance(x: ProvenanceAuditInput) -> InterfaceSolverCertificate:
    return solve_interface_descent(to_interface_problem(x))


def canonical_cases() -> Dict[str, ProvenanceAuditInput]:
    return {
        "clean_external_inputs": ProvenanceAuditInput(
            name="prov_clean_external_inputs",
            sector="EW",
            inputs_used=("alpha_em", "G_F", "source_trace_constants"),
            declared_targets=("M_W_physical",),
            fitted_outputs=("posterior_M_W",),
            posterior_outputs=("fit_pull",),
            allowed_exogenous_inputs=("alpha_em", "G_F"),
            notes="clean external constants and source trace constants",
        ),
        "target_consumed": ProvenanceAuditInput(
            name="prov_target_consumed",
            sector="EW",
            inputs_used=("alpha_em", "M_W_physical", "source_trace_constants"),
            declared_targets=("M_W_physical",),
            fitted_outputs=("posterior_M_W",),
            posterior_outputs=("fit_pull",),
            allowed_exogenous_inputs=("alpha_em",),
            notes="target used as input",
        ),
        "posterior_consumed": ProvenanceAuditInput(
            name="prov_posterior_consumed",
            sector="DARK",
            inputs_used=("DESI_DR2", "posterior_w0wa", "Planck_constants"),
            declared_targets=("w0", "wa"),
            fitted_outputs=("posterior_w0wa",),
            posterior_outputs=("bestfit_chi2",),
            allowed_exogenous_inputs=("DESI_DR2", "Planck_constants"),
            notes="posterior output used as input",
        ),
    }


def run_cases() -> Dict[str, Dict[str, Any]]:
    out = {}
    for key, case in canonical_cases().items():
        cert = audit_provenance(case)
        out[key] = {
            "input": asdict(case),
            "smuggled_symbols": smuggled_symbols(case),
            "target_value_consumed": target_value_consumed(case),
            "solver_status": cert.solver_status.value,
            "obstruction": cert.obstruction,
            "repair_class": cert.repair_class.value,
            "export_global_P": cert.export_global_P,
            "safe_claim": cert.safe_claim,
            "next_action": cert.next_action,
        }
    return out


def check_T_anti_fitting_provenance_audit_P() -> Dict[str, Any]:
    results = run_cases()
    tests = {
        "clean_exports": results["clean_external_inputs"]["solver_status"] == "SOLVED_GLOBAL_P",
        "clean_no_smuggled": results["clean_external_inputs"]["smuggled_symbols"] == tuple(),
        "target_fails_closed": results["target_consumed"]["solver_status"] == "FAIL_CLOSED_PROVENANCE",
        "target_symbol_detected": "m_w_physical" in results["target_consumed"]["smuggled_symbols"],
        "posterior_fails_closed": results["posterior_consumed"]["solver_status"] == "FAIL_CLOSED_PROVENANCE",
        "posterior_symbol_detected": "posterior_w0wa" in results["posterior_consumed"]["smuggled_symbols"],
    }
    return {
        "name": "check_T_anti_fitting_provenance_audit_P",
        "consistent": all(tests.values()),
        "status": "P_route_cert" if all(tests.values()) else "FAIL",
        "summary": "Anti-fitting provenance audit detects target/posterior smuggling and fail-closes.",
        "data": {"tests": tests, "results": results},
    }


CHECKS = {"check_T_anti_fitting_provenance_audit_P": check_T_anti_fitting_provenance_audit_P}


def register(registry=None):
    if registry is None:
        return CHECKS
    registry.update(CHECKS)
    return registry


def run_all() -> Dict[str, Any]:
    return {name: fn() for name, fn in CHECKS.items()}
