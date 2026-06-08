"""
APF Interface Kinematic Solver.

Purpose
-------
Compute the nearest admissible repair path from current interface motion to target export:

    route payload
      -> kinematic certificate
      -> missing transition fields
      -> repair moves
      -> minimal repair plan
      -> solvability class

Boundary
--------
The solver identifies what must change in the payload/evidence state. It does not fabricate
evidence, bypass provenance fail-closed states, or promote held physics claims.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List
import json

from apf.interface_kinematics_engine import (
    compute_kinematic_certificate,
    KinematicCertificate,
    KinematicState,
    TransitionStatus,
    next_required_field,
    summarize_kinematics,
)


class SolverStatus(str, Enum):
    ALREADY_EXPORTABLE = "ALREADY_EXPORTABLE"
    REPAIRABLE = "REPAIRABLE"
    FAIL_CLOSED_PROVENANCE = "FAIL_CLOSED_PROVENANCE"
    STRUCTURAL_BLOCK = "STRUCTURAL_BLOCK"
    UNSOLVABLE_BY_EVIDENCE_PATCH = "UNSOLVABLE_BY_EVIDENCE_PATCH"


class RepairPriority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    NORMAL = "NORMAL"
    LOW = "LOW"


@dataclass(frozen=True)
class RepairMove:
    order: int
    move: str
    required_field: str
    target_state: KinematicState
    priority: RepairPriority
    rationale: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["target_state"] = self.target_state.value
        d["priority"] = self.priority.value
        return d


@dataclass(frozen=True)
class KinematicSolveReport:
    route: str
    status: SolverStatus
    current_state: KinematicState
    target_state: KinematicState
    repair_moves: Tuple[RepairMove, ...]
    minimal_required_fields: Tuple[str, ...]
    first_next_field: Optional[str]
    estimated_repair_depth: int
    certificate: Mapping[str, Any]
    summary: str
    boundary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "route": self.route,
            "status": self.status.value,
            "current_state": self.current_state.value,
            "target_state": self.target_state.value,
            "repair_moves": [m.to_dict() for m in self.repair_moves],
            "minimal_required_fields": list(self.minimal_required_fields),
            "first_next_field": self.first_next_field,
            "estimated_repair_depth": self.estimated_repair_depth,
            "certificate": dict(self.certificate),
            "summary": self.summary,
            "boundary": self.boundary,
        }


CRITICAL_FIELDS = {
    "target_value_consumed",
    "codomain_transport_found",
    "evaluator_map_found",
    "data_ledger_clean",
    "external_constants_ledger_clean",
    "capacity_budget",
    "coarse_grain_factor",
}
HIGH_FIELDS = {
    "counterterm_finite_parts_declared",
    "uncertainty_protocol_declared",
    "posterior_closed",
    "chains_converged",
    "overlap_cocycle_verified",
    "overlap_gluing_verified",
    "capacity_bound_checked",
}


def _priority(field: str) -> RepairPriority:
    if field in CRITICAL_FIELDS:
        return RepairPriority.CRITICAL
    if field in HIGH_FIELDS:
        return RepairPriority.HIGH
    return RepairPriority.NORMAL


def repair_moves_from_certificate(cert: KinematicCertificate) -> Tuple[RepairMove, ...]:
    moves: List[RepairMove] = []
    order = 1
    for tr in cert.path:
        if tr.status == TransitionStatus.BLOCKED and tr.required_field:
            moves.append(RepairMove(
                order=order,
                move=tr.move,
                required_field=tr.required_field,
                target_state=tr.to_state,
                priority=_priority(tr.required_field),
                rationale=tr.reason,
            ))
            order += 1
        elif tr.status == TransitionStatus.NOT_REACHED and tr.required_field:
            moves.append(RepairMove(
                order=order,
                move=tr.move,
                required_field=tr.required_field,
                target_state=tr.to_state,
                priority=_priority(tr.required_field),
                rationale="not reached because an earlier move is blocked",
            ))
            order += 1
    return tuple(moves)


def solve_kinematic_path(route: str, payload: Mapping[str, Any]) -> KinematicSolveReport:
    cert = compute_kinematic_certificate(route, payload)
    boundary = "Kinematic solver identifies required evidence/state repairs only; it does not fabricate evidence or promote held claims."

    if cert.fail_closed:
        return KinematicSolveReport(
            route=route,
            status=SolverStatus.FAIL_CLOSED_PROVENANCE,
            current_state=cert.current_state,
            target_state=cert.target_state,
            repair_moves=tuple(),
            minimal_required_fields=tuple(),
            first_next_field=None,
            estimated_repair_depth=-1,
            certificate=cert.to_dict(),
            summary=f"{route}: provenance fail-closed; clean rebuild required, not evidence patch.",
            boundary=boundary,
        )

    if cert.structural_block:
        return KinematicSolveReport(
            route=route,
            status=SolverStatus.STRUCTURAL_BLOCK,
            current_state=cert.current_state,
            target_state=cert.target_state,
            repair_moves=tuple(),
            minimal_required_fields=tuple(),
            first_next_field=None,
            estimated_repair_depth=-1,
            certificate=cert.to_dict(),
            summary=f"{route}: structural block; theorem/substrate repair required.",
            boundary=boundary,
        )

    if cert.exportable:
        return KinematicSolveReport(
            route=route,
            status=SolverStatus.ALREADY_EXPORTABLE,
            current_state=cert.current_state,
            target_state=cert.target_state,
            repair_moves=tuple(),
            minimal_required_fields=tuple(),
            first_next_field=None,
            estimated_repair_depth=0,
            certificate=cert.to_dict(),
            summary=f"{route}: already reaches GLOBAL_EXPORTABLE.",
            boundary=boundary,
        )

    moves = repair_moves_from_certificate(cert)
    fields = tuple(dict.fromkeys(m.required_field for m in moves))
    status = SolverStatus.REPAIRABLE if moves else SolverStatus.UNSOLVABLE_BY_EVIDENCE_PATCH
    return KinematicSolveReport(
        route=route,
        status=status,
        current_state=cert.current_state,
        target_state=cert.target_state,
        repair_moves=moves,
        minimal_required_fields=fields,
        first_next_field=fields[0] if fields else None,
        estimated_repair_depth=len(fields) if fields else -1,
        certificate=cert.to_dict(),
        summary=f"{route}: repairable path requires {len(fields)} field(s): {', '.join(fields) if fields else 'none'}.",
        boundary=boundary,
    )


def apply_hypothetical_repairs(payload: Mapping[str, Any], fields: Iterable[str]) -> Dict[str, Any]:
    patched = dict(payload)
    for field in fields:
        if field in {"raw_capacity_load"}:
            continue
        if field == "coarse_grain_factor":
            patched[field] = max(float(patched.get(field, 1) or 1), 10.0)
        elif field == "capacity_budget":
            patched[field] = max(float(patched.get(field, 0) or 0), float(patched.get("raw_capacity_load", 1) or 1))
        else:
            patched[field] = True
    return patched


def solve_with_hypothetical_patch(route: str, payload: Mapping[str, Any]) -> Mapping[str, Any]:
    initial = solve_kinematic_path(route, payload)
    patched_payload = apply_hypothetical_repairs(payload, initial.minimal_required_fields)
    after = solve_kinematic_path(route, patched_payload)
    return {
        "initial": initial.to_dict(),
        "patched_payload": patched_payload,
        "after_patch": after.to_dict(),
        "patch_closes": after.status == SolverStatus.ALREADY_EXPORTABLE,
        "boundary": "Hypothetical patch toggles fields for planning only; it is not evidence.",
    }


def check_T_kinematic_solver_EW_repair_path_P() -> Dict[str, Any]:
    payload = {
        "trace_sector_closed": True,
        "source_to_scheme_registry_present": True,
        "codomain_transport_found": False,
        "evaluator_map_found": False,
        "counterterm_finite_parts_declared": False,
        "external_constants_ledger_clean": True,
        "uncertainty_protocol_declared": False,
        "target_value_consumed": False,
    }
    report = solve_kinematic_path("ew", payload)
    tests = {
        "repairable": report.status == SolverStatus.REPAIRABLE,
        "first_codomain": report.first_next_field == "codomain_transport_found",
        "has_evaluator": "evaluator_map_found" in report.minimal_required_fields,
        "depth_positive": report.estimated_repair_depth > 0,
    }
    return {"name": "check_T_kinematic_solver_EW_repair_path_P", "consistent": all(tests.values()), "status": "P_kinematic_solver" if all(tests.values()) else "FAIL", "summary": "Kinematic solver derives ordered EW repair fields.", "data": {"tests": tests, "report": report.to_dict()}}


def check_T_kinematic_solver_dark_exportable_P() -> Dict[str, Any]:
    payload = {
        "route_built": True, "run_completed": True, "chains_converged": True, "posterior_closed": True,
        "robustness_checks_passed": True, "codomain_transport_found": True, "evaluator_map_found": True,
        "data_ledger_clean": True, "target_value_consumed": False,
    }
    report = solve_kinematic_path("dark", payload)
    tests = {
        "already": report.status == SolverStatus.ALREADY_EXPORTABLE,
        "depth_zero": report.estimated_repair_depth == 0,
        "no_fields": report.minimal_required_fields == tuple(),
    }
    return {"name": "check_T_kinematic_solver_dark_exportable_P", "consistent": all(tests.values()), "status": "P_kinematic_solver" if all(tests.values()) else "FAIL", "summary": "Kinematic solver recognizes already exportable dark route.", "data": {"tests": tests, "report": report.to_dict()}, "dependencies": ["check_T_kinematic_solver_EW_repair_path_P"]}


def check_T_kinematic_solver_fail_closed_P() -> Dict[str, Any]:
    report = solve_kinematic_path("ew", {"trace_sector_closed": True, "target_value_consumed": True})
    tests = {
        "fail_closed": report.status == SolverStatus.FAIL_CLOSED_PROVENANCE,
        "negative_depth": report.estimated_repair_depth == -1,
        "no_repair_moves": report.repair_moves == tuple(),
    }
    return {"name": "check_T_kinematic_solver_fail_closed_P", "consistent": all(tests.values()), "status": "P_kinematic_solver" if all(tests.values()) else "FAIL", "summary": "Kinematic solver refuses evidence patching for provenance fail-closed states.", "data": {"tests": tests, "report": report.to_dict()}, "dependencies": ["check_T_kinematic_solver_dark_exportable_P"]}


def check_T_kinematic_solver_hypothetical_patch_P() -> Dict[str, Any]:
    payload = {
        "trace_sector_closed": True,
        "source_to_scheme_registry_present": True,
        "codomain_transport_found": False,
        "evaluator_map_found": False,
        "counterterm_finite_parts_declared": False,
        "external_constants_ledger_clean": True,
        "uncertainty_protocol_declared": False,
        "target_value_consumed": False,
    }
    plan = solve_with_hypothetical_patch("ew", payload)
    tests = {
        "patch_closes": plan["patch_closes"] is True,
        "boundary_not_evidence": "not evidence" in plan["boundary"],
        "initial_repairable": plan["initial"]["status"] == "REPAIRABLE",
        "after_exportable": plan["after_patch"]["status"] == "ALREADY_EXPORTABLE",
    }
    return {"name": "check_T_kinematic_solver_hypothetical_patch_P", "consistent": all(tests.values()), "status": "P_kinematic_solver" if all(tests.values()) else "FAIL", "summary": "Kinematic solver can test hypothetical repair closure without treating patch as evidence.", "data": {"tests": tests, "plan": plan}, "dependencies": ["check_T_kinematic_solver_fail_closed_P"]}


def check_T_interface_kinematic_solver_P() -> Dict[str, Any]:
    subchecks = [
        check_T_kinematic_solver_EW_repair_path_P(),
        check_T_kinematic_solver_dark_exportable_P(),
        check_T_kinematic_solver_fail_closed_P(),
        check_T_kinematic_solver_hypothetical_patch_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {"name": "check_T_interface_kinematic_solver_P", "consistent": ok, "status": "P_kinematic_solver" if ok else "FAIL", "summary": "Interface Kinematic Solver is P: it computes minimal repair fields, closure depth, and hard-stop classes.", "data": {"core_claim": "The solver computes what must change for admissible motion without fabricating evidence or promoting held claims.", "subchecks": [x["name"] for x in subchecks]}, "dependencies": [x["name"] for x in subchecks]}


CHECKS = {
    "check_T_kinematic_solver_EW_repair_path_P": check_T_kinematic_solver_EW_repair_path_P,
    "check_T_kinematic_solver_dark_exportable_P": check_T_kinematic_solver_dark_exportable_P,
    "check_T_kinematic_solver_fail_closed_P": check_T_kinematic_solver_fail_closed_P,
    "check_T_kinematic_solver_hypothetical_patch_P": check_T_kinematic_solver_hypothetical_patch_P,
    "check_T_interface_kinematic_solver_P": check_T_interface_kinematic_solver_P,
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
            raise TypeError("Unsupported registry type for interface_kinematic_solver.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
