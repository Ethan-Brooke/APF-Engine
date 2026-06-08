"""
APF Interface Solver Descent Bridge.

This module is the integration layer that lets an interface solver call the
Representation Descent Kernel.

The interface solver should produce raw interface/sector metadata. This bridge then
certifies:

    * obstruction certificate
    * solver/export status
    * repair normal form
    * safe claim language
    * next action
    * fail-closed provenance behavior

Design principle:
    The bridge does not replace the interface solver.
    It wraps solver outputs with promotion/no-smuggling discipline.

Main export:
    solve_interface_descent(problem: InterfaceSolverProblem) -> InterfaceSolverCertificate

Top check:
    check_T_interface_solver_descent_bridge_P
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterable, Mapping, Optional, Tuple, List

try:
    from apf.descent_obstruction_calculus import Obstruction, ObstructionObject
    from apf.obstruction_repair_normal_form import RepairClass, canonical_plan, plan_data
    from apf.globalization_promotion_gate import PromotionStatus, decide_promotion
    from apf.representation_descent_application_harness import (
        SectorMetadata,
        obstruction_from_metadata,
        classify_sector,
        classification_data,
    )
except Exception as exc:  # pragma: no cover
    raise ImportError(f"interface_solver_descent_bridge dependencies missing: {exc}") from exc


def _ok(name: str, *, status: str, summary: str, data: Optional[Mapping] = None,
        dependencies: Optional[Iterable[str]] = None) -> Dict:
    return {
        "name": name,
        "consistent": True,
        "status": status,
        "summary": summary,
        "data": dict(data or {}),
        "dependencies": list(dependencies or []),
    }


def _fail(name: str, *, status: str, summary: str, data: Optional[Mapping] = None,
          dependencies: Optional[Iterable[str]] = None) -> Dict:
    return {
        "name": name,
        "consistent": False,
        "status": status,
        "summary": summary,
        "data": dict(data or {}),
        "dependencies": list(dependencies or []),
    }


class InterfaceSolverStatus(str, Enum):
    SOLVED_GLOBAL_P = "SOLVED_GLOBAL_P"
    SOLVED_LOCAL_HELD_FOR_REPAIR = "SOLVED_LOCAL_HELD_FOR_REPAIR"
    BLOCKED_SUBSTRATE_REVISION_REQUIRED = "BLOCKED_SUBSTRATE_REVISION_REQUIRED"
    FAIL_CLOSED_PROVENANCE = "FAIL_CLOSED_PROVENANCE"
    FAIL_UNSUPPORTED = "FAIL_UNSUPPORTED"
    # v24.3.41 — Mass-sector Step D audit Findings 2 + 3.
    # OBSTRUCTION_NAMED_CLOSURE: route closed by codomain knockout (e.g. heavy-quark
    # pole-mass routes 4/6/9). Codomain itself is rejected; route is closed-by-design,
    # NOT awaiting repair. Semantically distinct from SOLVED_LOCAL_HELD_FOR_REPAIR.
    OBSTRUCTION_NAMED_CLOSURE = "OBSTRUCTION_NAMED_CLOSURE"
    # INTERNAL_IDENTITY_GLOBAL_P: route IS the identity; source coincides with target
    # by construction (e.g. sin²θ_W = 3/13 + on-shell mass-ratio). Global-P semantics
    # via structural identity rather than evaluator transport.
    INTERNAL_IDENTITY_GLOBAL_P = "INTERNAL_IDENTITY_GLOBAL_P"


@dataclass(frozen=True)
class InterfaceSolverProblem:
    """Raw output object from an interface solver.

    No expected label/status fields are allowed. The solver may know whether it solved
    local equations/routes, but not whether global APF promotion is allowed.
    """
    name: str
    sector: str
    local_solution_found: bool
    global_export_requested: bool
    acc_base_present: bool
    evaluator_map_found: bool
    codomain_transport_found: bool
    overlap_gluing_verified: bool
    capacity_budget_verified: bool
    capacity_overspend_detected: bool
    empirical_or_posterior_closed: bool
    target_value_used_as_input: bool
    requires_substrate_polarity: bool = False
    requires_substrate_reversal: bool = False
    requires_complex_action: bool = False
    requires_operator_norm: bool = False
    route_notes: str = ""


@dataclass(frozen=True)
class InterfaceSolverCertificate:
    problem_name: str
    sector: str
    solver_status: InterfaceSolverStatus
    promotion_status: PromotionStatus
    repair_class: RepairClass
    obstruction: Tuple[str, ...]
    export_global_P: bool
    export_local_P: bool
    repair_plan: Mapping
    safe_claim: str
    next_action: str
    route_notes: str


def problem_to_sector_metadata(problem: InterfaceSolverProblem) -> SectorMetadata:
    """Translate raw interface-solver output into sector metadata for descent classification."""
    return SectorMetadata(
        name=problem.name,
        sector=problem.sector,
        local_claim_available=problem.local_solution_found,
        global_claim_requested=problem.global_export_requested,
        has_ACC_base=problem.acc_base_present,
        has_local_representation=problem.local_solution_found,
        has_evaluator_map=problem.evaluator_map_found,
        has_codomain_transport=problem.codomain_transport_found,
        has_overlap_gluing_proof=problem.overlap_gluing_verified,
        has_capacity_budget_proof=problem.capacity_budget_verified,
        capacity_overspend_detected=problem.capacity_overspend_detected,
        posterior_or_empirical_closed=problem.empirical_or_posterior_closed,
        target_value_consumed=problem.target_value_used_as_input,
        needs_substrate_polarity=problem.requires_substrate_polarity,
        needs_substrate_reversal=problem.requires_substrate_reversal,
        needs_complex_action=problem.requires_complex_action,
        needs_operator_norm=problem.requires_operator_norm,
        notes=problem.route_notes,
    )


def bridge_status_from_promotion(promotion: PromotionStatus, repair_class: RepairClass) -> InterfaceSolverStatus:
    if promotion == PromotionStatus.EXPORT_GLOBAL_P:
        return InterfaceSolverStatus.SOLVED_GLOBAL_P
    if promotion == PromotionStatus.HOLD_ORDINARY_REPAIR_REQUIRED:
        return InterfaceSolverStatus.SOLVED_LOCAL_HELD_FOR_REPAIR
    if promotion == PromotionStatus.HOLD_SUBSTRATE_REVISION_REQUIRED:
        return InterfaceSolverStatus.BLOCKED_SUBSTRATE_REVISION_REQUIRED
    if promotion == PromotionStatus.FAIL_CLOSED_PROVENANCE:
        return InterfaceSolverStatus.FAIL_CLOSED_PROVENANCE
    # v24.3.41 — new promotion statuses from Mass-sector Step D audit Findings 2 + 3:
    if promotion == PromotionStatus.OBSTRUCTION_NAMED_CLOSURE:
        return InterfaceSolverStatus.OBSTRUCTION_NAMED_CLOSURE
    if promotion == PromotionStatus.EXPORT_INTERNAL_IDENTITY_P:
        return InterfaceSolverStatus.INTERNAL_IDENTITY_GLOBAL_P
    return InterfaceSolverStatus.FAIL_UNSUPPORTED


def solve_interface_descent(problem: InterfaceSolverProblem) -> InterfaceSolverCertificate:
    """Bridge an interface solver output into the APF descent/promotion kernel."""
    meta = problem_to_sector_metadata(problem)
    classification = classify_sector(meta)
    status = bridge_status_from_promotion(classification.promotion_status, classification.repair_class)
    return InterfaceSolverCertificate(
        problem_name=problem.name,
        sector=problem.sector,
        solver_status=status,
        promotion_status=classification.promotion_status,
        repair_class=classification.repair_class,
        obstruction=classification.obstruction.names(),
        export_global_P=classification.export_global_P,
        export_local_P=classification.export_local_P,
        repair_plan=classification.repair_plan,
        safe_claim=classification.safe_claim,
        next_action=classification.next_action,
        route_notes=problem.route_notes,
    )


def certificate_data(cert: InterfaceSolverCertificate) -> Dict:
    return {
        "problem_name": cert.problem_name,
        "sector": cert.sector,
        "solver_status": cert.solver_status.value,
        "promotion_status": cert.promotion_status.value,
        "repair_class": cert.repair_class.value,
        "obstruction": cert.obstruction,
        "export_global_P": cert.export_global_P,
        "export_local_P": cert.export_local_P,
        "repair_plan": dict(cert.repair_plan),
        "safe_claim": cert.safe_claim,
        "next_action": cert.next_action,
        "route_notes": cert.route_notes,
    }


def canonical_solver_problems() -> Dict[str, InterfaceSolverProblem]:
    return {
        "clean_ACC_interface": InterfaceSolverProblem(
            name="clean_ACC_interface",
            sector="ACC",
            local_solution_found=True,
            global_export_requested=True,
            acc_base_present=True,
            evaluator_map_found=True,
            codomain_transport_found=True,
            overlap_gluing_verified=True,
            capacity_budget_verified=True,
            capacity_overspend_detected=False,
            empirical_or_posterior_closed=True,
            target_value_used_as_input=False,
            route_notes="clean interface solution",
        ),
        "EW_trace_route_open_transport": InterfaceSolverProblem(
            name="EW_trace_route_open_transport",
            sector="EW",
            local_solution_found=True,
            global_export_requested=True,
            acc_base_present=True,
            evaluator_map_found=False,
            codomain_transport_found=False,
            overlap_gluing_verified=True,
            capacity_budget_verified=True,
            capacity_overspend_detected=False,
            empirical_or_posterior_closed=True,
            target_value_used_as_input=False,
            route_notes="trace-sector closure; physical scheme transport open",
        ),
        "dark_posterior_open": InterfaceSolverProblem(
            name="dark_posterior_open",
            sector="DARK",
            local_solution_found=True,
            global_export_requested=True,
            acc_base_present=True,
            evaluator_map_found=False,
            codomain_transport_found=True,
            overlap_gluing_verified=True,
            capacity_budget_verified=True,
            capacity_overspend_detected=False,
            empirical_or_posterior_closed=False,
            target_value_used_as_input=False,
            route_notes="empirical posterior/convergence not closed",
        ),
        "gauge_codomain_open": InterfaceSolverProblem(
            name="gauge_codomain_open",
            sector="GAUGE",
            local_solution_found=True,
            global_export_requested=True,
            acc_base_present=True,
            evaluator_map_found=True,
            codomain_transport_found=False,
            overlap_gluing_verified=True,
            capacity_budget_verified=True,
            capacity_overspend_detected=False,
            empirical_or_posterior_closed=True,
            target_value_used_as_input=False,
            route_notes="fiber automorphism route; codomain descent open",
        ),
        "horizon_overlap_open": InterfaceSolverProblem(
            name="horizon_overlap_open",
            sector="HORIZON",
            local_solution_found=True,
            global_export_requested=True,
            acc_base_present=True,
            evaluator_map_found=True,
            codomain_transport_found=True,
            overlap_gluing_verified=False,
            capacity_budget_verified=True,
            capacity_overspend_detected=False,
            empirical_or_posterior_closed=True,
            target_value_used_as_input=False,
            route_notes="horizon/interface overlap proof open",
        ),
        "flat_Cstar_attempt": InterfaceSolverProblem(
            name="flat_Cstar_attempt",
            sector="CSTAR",
            local_solution_found=True,
            global_export_requested=True,
            acc_base_present=True,
            evaluator_map_found=True,
            codomain_transport_found=False,
            overlap_gluing_verified=True,
            capacity_budget_verified=True,
            capacity_overspend_detected=False,
            empirical_or_posterior_closed=True,
            target_value_used_as_input=False,
            requires_substrate_reversal=True,
            requires_complex_action=True,
            requires_operator_norm=True,
            route_notes="flat substrate C* attempt",
        ),
        "target_smuggled_route": InterfaceSolverProblem(
            name="target_smuggled_route",
            sector="PROVENANCE",
            local_solution_found=True,
            global_export_requested=True,
            acc_base_present=True,
            evaluator_map_found=True,
            codomain_transport_found=True,
            overlap_gluing_verified=True,
            capacity_budget_verified=True,
            capacity_overspend_detected=False,
            empirical_or_posterior_closed=True,
            target_value_used_as_input=True,
            route_notes="target value consumed as input",
        ),
        "capacity_overload_route": InterfaceSolverProblem(
            name="capacity_overload_route",
            sector="CAPACITY",
            local_solution_found=True,
            global_export_requested=True,
            acc_base_present=True,
            evaluator_map_found=True,
            codomain_transport_found=True,
            overlap_gluing_verified=True,
            capacity_budget_verified=False,
            capacity_overspend_detected=True,
            empirical_or_posterior_closed=True,
            target_value_used_as_input=False,
            route_notes="capacity overspend detected",
        ),
    }


def run_canonical_bridge() -> Dict[str, InterfaceSolverCertificate]:
    return {name: solve_interface_descent(problem) for name, problem in canonical_solver_problems().items()}


def check_T_interface_solver_problem_schema_no_expected_labels_P() -> Dict:
    fields = set(InterfaceSolverProblem.__dataclass_fields__.keys())
    forbidden = {"expected_status", "expected_label", "expected_repair_class", "promotion_status", "solver_status"}
    tests = {
        "no_expected_label_fields": fields.isdisjoint(forbidden),
        "has_solver_raw_fields": {
            "local_solution_found",
            "evaluator_map_found",
            "codomain_transport_found",
            "overlap_gluing_verified",
            "capacity_budget_verified",
            "target_value_used_as_input",
        }.issubset(fields),
    }
    if all(tests.values()):
        return _ok(
            "check_T_interface_solver_problem_schema_no_expected_labels_P",
            status="P_bridge",
            summary="Interface solver problem schema uses raw solver outputs only; no expected-label leakage.",
            data={"fields": sorted(fields), "tests": tests},
        )
    return _fail("check_T_interface_solver_problem_schema_no_expected_labels_P", status="FAIL", summary="Problem schema label leakage failed", data={"fields": sorted(fields), "tests": tests})


def check_T_problem_to_sector_metadata_translation_P() -> Dict:
    problems = canonical_solver_problems()
    translations = {name: problem_to_sector_metadata(problem) for name, problem in problems.items()}
    tests = {
        "same_count": len(translations) == len(problems),
        "EW_transport_maps_false": not translations["EW_trace_route_open_transport"].has_evaluator_map and not translations["EW_trace_route_open_transport"].has_codomain_transport,
        "dark_posterior_false": not translations["dark_posterior_open"].posterior_or_empirical_closed,
        "Cstar_structural_true": translations["flat_Cstar_attempt"].needs_substrate_reversal and translations["flat_Cstar_attempt"].needs_complex_action and translations["flat_Cstar_attempt"].needs_operator_norm,
        "provenance_true": translations["target_smuggled_route"].target_value_consumed,
    }
    if all(tests.values()):
        return _ok(
            "check_T_problem_to_sector_metadata_translation_P",
            status="P_bridge",
            summary="Interface solver outputs translate correctly into sector metadata.",
            data={"tests": tests},
            dependencies=["check_T_interface_solver_problem_schema_no_expected_labels_P"],
        )
    return _fail("check_T_problem_to_sector_metadata_translation_P", status="FAIL", summary="Problem-to-sector metadata translation failed", data=tests)


def check_T_bridge_certificates_status_P() -> Dict:
    certs = run_canonical_bridge()
    statuses = {name: cert.solver_status.value for name, cert in certs.items()}
    tests = {
        "clean_global_solved": statuses["clean_ACC_interface"] == "SOLVED_GLOBAL_P",
        "EW_held_repair": statuses["EW_trace_route_open_transport"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "dark_held_repair": statuses["dark_posterior_open"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "gauge_held_repair": statuses["gauge_codomain_open"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "horizon_held_repair": statuses["horizon_overlap_open"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "Cstar_blocked_revision": statuses["flat_Cstar_attempt"] == "BLOCKED_SUBSTRATE_REVISION_REQUIRED",
        "target_fail_closed": statuses["target_smuggled_route"] == "FAIL_CLOSED_PROVENANCE",
        "capacity_held_repair": statuses["capacity_overload_route"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
    }
    if all(tests.values()):
        return _ok(
            "check_T_bridge_certificates_status_P",
            status="P_bridge",
            summary="Interface solver bridge emits correct solver/promotion statuses for canonical problems.",
            data={"statuses": statuses, "tests": tests},
            dependencies=["check_T_problem_to_sector_metadata_translation_P"],
        )
    return _fail("check_T_bridge_certificates_status_P", status="FAIL", summary="Bridge certificate statuses failed", data={"statuses": statuses, "tests": tests})


def check_T_bridge_obstruction_certificates_P() -> Dict:
    certs = run_canonical_bridge()
    obs = {name: set(cert.obstruction) for name, cert in certs.items()}
    tests = {
        "clean_zero": len(obs["clean_ACC_interface"]) == 0,
        "EW_evaluator_codomain": obs["EW_trace_route_open_transport"] == {"EVALUATOR_MISSING", "CODOMAIN_MISMATCH"},
        "dark_evaluator": obs["dark_posterior_open"] == {"EVALUATOR_MISSING"},
        "gauge_codomain": obs["gauge_codomain_open"] == {"CODOMAIN_MISMATCH"},
        "horizon_overlap": obs["horizon_overlap_open"] == {"OVERLAP_INCOHERENCE"},
        "Cstar_structural": {"REVERSAL_MISSING", "COMPLEX_ACTION_MISSING", "NORM_MISSING", "CODOMAIN_MISMATCH"}.issubset(obs["flat_Cstar_attempt"]),
        "target_provenance": "PROVENANCE_SMUGGLE" in obs["target_smuggled_route"],
        "capacity_overspend": "CAPACITY_OVERSPEND" in obs["capacity_overload_route"],
    }
    if all(tests.values()):
        return _ok(
            "check_T_bridge_obstruction_certificates_P",
            status="P_bridge",
            summary="Interface solver bridge produces expected obstruction certificates from raw solver outputs.",
            data={"obstructions": {k: tuple(sorted(v)) for k, v in obs.items()}, "tests": tests},
            dependencies=["check_T_bridge_certificates_status_P"],
        )
    return _fail("check_T_bridge_obstruction_certificates_P", status="FAIL", summary="Bridge obstruction certificates failed", data={"obstructions": {k: tuple(sorted(v)) for k, v in obs.items()}, "tests": tests})


def check_T_bridge_no_overpromotion_P() -> Dict:
    certs = run_canonical_bridge()
    tests = {
        "global_export_iff_zero": all(cert.export_global_P == (len(cert.obstruction) == 0) for cert in certs.values()),
        "only_clean_exports": [name for name, cert in certs.items() if cert.export_global_P] == ["clean_ACC_interface"],
        "provenance_no_local_export": not certs["target_smuggled_route"].export_local_P and not certs["target_smuggled_route"].export_global_P,
        "Cstar_not_exported": not certs["flat_Cstar_attempt"].export_global_P,
    }
    if all(tests.values()):
        return _ok(
            "check_T_bridge_no_overpromotion_P",
            status="P_audit",
            summary="Interface solver bridge enforces no-overpromotion: global export iff zero obstruction.",
            data={"tests": tests},
            dependencies=["check_T_bridge_obstruction_certificates_P"],
        )
    return _fail("check_T_bridge_no_overpromotion_P", status="FAIL", summary="Bridge no-overpromotion failed", data=tests)


def check_T_bridge_repair_and_next_action_P() -> Dict:
    certs = run_canonical_bridge()
    data = {name: certificate_data(cert) for name, cert in certs.items()}
    tests = {
        "EW_rerun_transport": "transport" in certs["EW_trace_route_open_transport"].next_action.lower() and "rerun" in certs["EW_trace_route_open_transport"].next_action.lower(),
        "dark_continue_posterior": "posterior" in certs["dark_posterior_open"].next_action.lower() or "robustness" in certs["dark_posterior_open"].next_action.lower(),
        "Cstar_substrate_program": "substrate" in certs["flat_Cstar_attempt"].next_action.lower(),
        "provenance_rebuild": "rebuild" in certs["target_smuggled_route"].next_action.lower(),
        "capacity_has_repair_plan": certs["capacity_overload_route"].repair_class.value == "ORDINARY_REPAIRABLE",
    }
    if all(tests.values()):
        return _ok(
            "check_T_bridge_repair_and_next_action_P",
            status="P_bridge",
            summary="Interface solver bridge emits repair plans and next actions suitable for solver routing.",
            data={"certificates": data, "tests": tests},
            dependencies=["check_T_bridge_no_overpromotion_P"],
        )
    return _fail("check_T_bridge_repair_and_next_action_P", status="FAIL", summary="Bridge repair/next action failed", data={"certificates": data, "tests": tests})


def check_T_interface_solver_descent_bridge_P() -> Dict:
    subchecks = [
        check_T_interface_solver_problem_schema_no_expected_labels_P(),
        check_T_problem_to_sector_metadata_translation_P(),
        check_T_bridge_certificates_status_P(),
        check_T_bridge_obstruction_certificates_P(),
        check_T_bridge_no_overpromotion_P(),
        check_T_bridge_repair_and_next_action_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    if ok:
        return _ok(
            "check_T_interface_solver_descent_bridge_P",
            status="P_solver_bridge",
            summary="Interface Solver Descent Bridge is P: solver outputs are certified by obstruction, repair, and promotion gates.",
            data={
                "canonical_problem_count": len(canonical_solver_problems()),
                "global_exports": [name for name, cert in run_canonical_bridge().items() if cert.export_global_P],
                "held_or_blocked": [name for name, cert in run_canonical_bridge().items() if not cert.export_global_P],
                "subchecks": [x["name"] for x in subchecks],
            },
            dependencies=[x["name"] for x in subchecks],
        )
    return _fail(
        "check_T_interface_solver_descent_bridge_P",
        status="FAIL",
        summary="Interface Solver Descent Bridge failed.",
        data={"subchecks": subchecks},
    )


CHECKS = {
    "check_T_interface_solver_problem_schema_no_expected_labels_P": check_T_interface_solver_problem_schema_no_expected_labels_P,
    "check_T_problem_to_sector_metadata_translation_P": check_T_problem_to_sector_metadata_translation_P,
    "check_T_bridge_certificates_status_P": check_T_bridge_certificates_status_P,
    "check_T_bridge_obstruction_certificates_P": check_T_bridge_obstruction_certificates_P,
    "check_T_bridge_no_overpromotion_P": check_T_bridge_no_overpromotion_P,
    "check_T_bridge_repair_and_next_action_P": check_T_bridge_repair_and_next_action_P,
    "check_T_interface_solver_descent_bridge_P": check_T_interface_solver_descent_bridge_P,
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
            raise TypeError("Unsupported registry type for interface_solver_descent_bridge.register")
    return registry


def run_all() -> Dict[str, Dict]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
