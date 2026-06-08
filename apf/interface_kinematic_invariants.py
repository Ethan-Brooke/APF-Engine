"""
APF Interface Kinematic Invariants.

Purpose
-------
Extract and audit invariants of interface motion:

    route payload / kinematic certificate
      -> invariant signature
      -> monotone progress invariant
      -> hard-stop invariant
      -> capacity class invariant
      -> blocked-field invariant
      -> invariant violation certificate

Core idea
---------
Admissible interface motion is constrained not only by transition order but by invariants
that must be preserved or monotonically refined under repair.

Boundary
--------
Invariant diagnostics detect structural consistency of motion. They do not provide missing
evidence, repair proofs, or promote held physics claims.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List
import json
import datetime

from apf.interface_kinematics_engine import (
    compute_kinematic_certificate,
    KinematicState,
    TransitionStatus,
    provenance_fail_closed,
    structural_blocked,
)
from apf.interface_kinematic_solver import solve_kinematic_path, SolverStatus
from apf.interface_kinematic_phase_space_atlas import phase_point


class CapacityClass(str, Enum):
    UNKNOWN = "UNKNOWN"
    UNDER_BUDGET = "UNDER_BUDGET"
    SATURATED = "SATURATED"
    OVERSPENT = "OVERSPENT"


class InvariantStatus(str, Enum):
    PRESERVED = "PRESERVED"
    MONOTONE_REFINED = "MONOTONE_REFINED"
    VIOLATED = "VIOLATED"
    HARD_STOP = "HARD_STOP"


class InvariantViolationKind(str, Enum):
    NONE = "NONE"
    PROVENANCE_REVERSAL = "PROVENANCE_REVERSAL"
    STRUCTURAL_REVERSAL = "STRUCTURAL_REVERSAL"
    PROGRESS_REGRESSION = "PROGRESS_REGRESSION"
    CAPACITY_CLASS_WORSENED = "CAPACITY_CLASS_WORSENED"
    BLOCKED_FIELD_EXPANSION = "BLOCKED_FIELD_EXPANSION"
    EXPORT_WITH_UNRESOLVED_BLOCKERS = "EXPORT_WITH_UNRESOLVED_BLOCKERS"


@dataclass(frozen=True)
class InvariantSignature:
    route: str
    current_state: KinematicState
    phase_region: str
    progress_fraction: float
    distance_to_export: int
    repair_depth: int
    blocked_fields: Tuple[str, ...]
    capacity_class: CapacityClass
    provenance_clean: bool
    structural_clean: bool
    exportable: bool
    solver_status: SolverStatus

    def to_dict(self) -> Dict[str, Any]:
        return {
            "route": self.route,
            "current_state": self.current_state.value,
            "phase_region": self.phase_region,
            "progress_fraction": self.progress_fraction,
            "distance_to_export": self.distance_to_export,
            "repair_depth": self.repair_depth,
            "blocked_fields": list(self.blocked_fields),
            "capacity_class": self.capacity_class.value,
            "provenance_clean": self.provenance_clean,
            "structural_clean": self.structural_clean,
            "exportable": self.exportable,
            "solver_status": self.solver_status.value,
        }


@dataclass(frozen=True)
class InvariantAudit:
    route: str
    before: InvariantSignature
    after: InvariantSignature
    status: InvariantStatus
    violation: InvariantViolationKind
    changed_fields: Tuple[str, ...]
    summary: str
    boundary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "route": self.route,
            "before": self.before.to_dict(),
            "after": self.after.to_dict(),
            "status": self.status.value,
            "violation": self.violation.value,
            "changed_fields": list(self.changed_fields),
            "summary": self.summary,
            "boundary": self.boundary,
        }


def capacity_class(payload: Mapping[str, Any]) -> CapacityClass:
    if "raw_capacity_load" not in payload or "capacity_budget" not in payload:
        return CapacityClass.UNKNOWN
    try:
        load = float(payload.get("raw_capacity_load", 0))
        budget = float(payload.get("capacity_budget", 0))
        cg = float(payload.get("coarse_grain_factor", 1) or 1)
        if cg <= 0 or budget < 0:
            return CapacityClass.OVERSPENT
        effective = load / cg
        if effective > budget:
            return CapacityClass.OVERSPENT
        if budget == 0:
            return CapacityClass.SATURATED if effective == 0 else CapacityClass.OVERSPENT
        ratio = effective / budget
        if ratio >= 0.95:
            return CapacityClass.SATURATED
        return CapacityClass.UNDER_BUDGET
    except Exception:
        return CapacityClass.UNKNOWN


def blocked_fields_from_cert(cert) -> Tuple[str, ...]:
    fields = []
    for tr in cert.path:
        if tr.status in {TransitionStatus.BLOCKED, TransitionStatus.NOT_REACHED} and tr.required_field:
            fields.append(tr.required_field)
    return tuple(dict.fromkeys(fields))


def invariant_signature(route: str, payload: Mapping[str, Any]) -> InvariantSignature:
    cert = compute_kinematic_certificate(route, payload)
    solve = solve_kinematic_path(route, payload)
    point = phase_point("signature", route, payload)
    return InvariantSignature(
        route=route,
        current_state=cert.current_state,
        phase_region=point.phase_region.value,
        progress_fraction=point.progress_fraction,
        distance_to_export=point.distance_to_export,
        repair_depth=solve.estimated_repair_depth,
        blocked_fields=blocked_fields_from_cert(cert),
        capacity_class=capacity_class(payload),
        provenance_clean=not provenance_fail_closed(payload),
        structural_clean=not structural_blocked(route, payload),
        exportable=cert.exportable,
        solver_status=solve.status,
    )


CAPACITY_ORDER = {
    CapacityClass.UNKNOWN: 0,
    CapacityClass.UNDER_BUDGET: 1,
    CapacityClass.SATURATED: 2,
    CapacityClass.OVERSPENT: 3,
}


def changed_fields(before: Mapping[str, Any], after: Mapping[str, Any]) -> Tuple[str, ...]:
    keys = set(before) | set(after)
    return tuple(sorted(k for k in keys if before.get(k) != after.get(k)))


def audit_invariant_transition(route: str, before_payload: Mapping[str, Any], after_payload: Mapping[str, Any]) -> InvariantAudit:
    before = invariant_signature(route, before_payload)
    after = invariant_signature(route, after_payload)
    boundary = "Invariant audit is structural consistency checking only; it does not fabricate evidence or promote held claims."
    changes = changed_fields(before_payload, after_payload)

    if before.provenance_clean and not after.provenance_clean:
        return InvariantAudit(route, before, after, InvariantStatus.VIOLATED, InvariantViolationKind.PROVENANCE_REVERSAL, changes, "Transition introduces target/provenance contamination.", boundary)
    if before.structural_clean and not after.structural_clean:
        return InvariantAudit(route, before, after, InvariantStatus.VIOLATED, InvariantViolationKind.STRUCTURAL_REVERSAL, changes, "Transition introduces structural blocker.", boundary)
    if not before.provenance_clean or not before.structural_clean:
        return InvariantAudit(route, before, after, InvariantStatus.HARD_STOP, InvariantViolationKind.NONE, changes, "Before-state is already hard-stopped; ordinary invariant refinement is not applicable.", boundary)
    if CAPACITY_ORDER[after.capacity_class] > CAPACITY_ORDER[before.capacity_class] and before.capacity_class != CapacityClass.UNKNOWN:
        return InvariantAudit(route, before, after, InvariantStatus.VIOLATED, InvariantViolationKind.CAPACITY_CLASS_WORSENED, changes, "Transition worsens capacity class.", boundary)
    if after.progress_fraction + 1e-12 < before.progress_fraction:
        return InvariantAudit(route, before, after, InvariantStatus.VIOLATED, InvariantViolationKind.PROGRESS_REGRESSION, changes, "Transition regresses kinematic progress.", boundary)
    if set(after.blocked_fields) > set(before.blocked_fields) and before.blocked_fields:
        return InvariantAudit(route, before, after, InvariantStatus.VIOLATED, InvariantViolationKind.BLOCKED_FIELD_EXPANSION, changes, "Transition expands unresolved blocked-field set.", boundary)
    if after.exportable and after.blocked_fields:
        return InvariantAudit(route, before, after, InvariantStatus.VIOLATED, InvariantViolationKind.EXPORT_WITH_UNRESOLVED_BLOCKERS, changes, "Export state coexists with unresolved blockers.", boundary)

    if after.progress_fraction > before.progress_fraction or len(after.blocked_fields) < len(before.blocked_fields) or after.exportable:
        return InvariantAudit(route, before, after, InvariantStatus.MONOTONE_REFINED, InvariantViolationKind.NONE, changes, "Transition monotonically refines the kinematic signature.", boundary)

    return InvariantAudit(route, before, after, InvariantStatus.PRESERVED, InvariantViolationKind.NONE, changes, "Invariant signature preserved.", boundary)


def load_invariant_audit_cases(path: str) -> Tuple[Mapping[str, Any], ...]:
    data = json.loads(open(path, "r", encoding="utf-8").read())
    return tuple(data.get("cases", data))


def audit_invariant_batch(cases: Iterable[Mapping[str, Any]]) -> Mapping[str, Any]:
    audits = []
    for idx, case in enumerate(cases):
        route = str(case.get("route", "generic"))
        audits.append(audit_invariant_transition(route, case.get("before", {}), case.get("after", {})).to_dict() | {"case_id": case.get("case_id", f"case_{idx:03d}")})
    status_counts: Dict[str, int] = {}
    violation_counts: Dict[str, int] = {}
    for audit in audits:
        status_counts[audit["status"]] = status_counts.get(audit["status"], 0) + 1
        violation_counts[audit["violation"]] = violation_counts.get(audit["violation"], 0) + 1
    return {
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "audits": audits,
        "status_counts": status_counts,
        "violation_counts": violation_counts,
        "boundary": "Batch invariant audit is structural consistency checking only; it does not promote held claims.",
    }


def check_T_invariant_signature_EW_P() -> Dict[str, Any]:
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
    sig = invariant_signature("ew", payload)
    tests = {
        "route": sig.route == "ew",
        "blocked_codomain": "codomain_transport_found" in sig.blocked_fields,
        "clean": sig.provenance_clean and sig.structural_clean,
        "not_exportable": sig.exportable is False,
    }
    return {"name": "check_T_invariant_signature_EW_P", "consistent": all(tests.values()), "status": "P_invariants" if all(tests.values()) else "FAIL", "summary": "Invariant signature records EW blocked-field/progress state.", "data": {"tests": tests, "signature": sig.to_dict()}}


def check_T_invariant_monotone_repair_P() -> Dict[str, Any]:
    before = {
        "trace_sector_closed": True,
        "source_to_scheme_registry_present": True,
        "codomain_transport_found": False,
        "evaluator_map_found": False,
        "counterterm_finite_parts_declared": False,
        "external_constants_ledger_clean": True,
        "uncertainty_protocol_declared": False,
        "target_value_consumed": False,
    }
    after = dict(before)
    after["codomain_transport_found"] = True
    after["evaluator_map_found"] = True
    audit = audit_invariant_transition("ew", before, after)
    tests = {
        "monotone": audit.status == InvariantStatus.MONOTONE_REFINED,
        "no_violation": audit.violation == InvariantViolationKind.NONE,
        "changed": "codomain_transport_found" in audit.changed_fields,
    }
    return {"name": "check_T_invariant_monotone_repair_P", "consistent": all(tests.values()), "status": "P_invariants" if all(tests.values()) else "FAIL", "summary": "Invariant audit recognizes monotone evidence repair.", "data": {"tests": tests, "audit": audit.to_dict()}, "dependencies": ["check_T_invariant_signature_EW_P"]}


def check_T_invariant_provenance_violation_P() -> Dict[str, Any]:
    before = {"trace_sector_closed": True, "target_value_consumed": False}
    after = {"trace_sector_closed": True, "target_value_consumed": True}
    audit = audit_invariant_transition("ew", before, after)
    tests = {
        "violated": audit.status == InvariantStatus.VIOLATED,
        "provenance": audit.violation == InvariantViolationKind.PROVENANCE_REVERSAL,
        "boundary": "does not fabricate" in audit.boundary,
    }
    return {"name": "check_T_invariant_provenance_violation_P", "consistent": all(tests.values()), "status": "P_invariants" if all(tests.values()) else "FAIL", "summary": "Invariant audit catches provenance contamination as violation.", "data": {"tests": tests, "audit": audit.to_dict()}, "dependencies": ["check_T_invariant_monotone_repair_P"]}


def check_T_invariant_capacity_worsening_P() -> Dict[str, Any]:
    before = {"raw_capacity_load": 10, "capacity_budget": 20, "coarse_grain_factor": 1, "target_value_consumed": False}
    after = {"raw_capacity_load": 30, "capacity_budget": 20, "coarse_grain_factor": 1, "target_value_consumed": False}
    audit = audit_invariant_transition("capacity", before, after)
    tests = {
        "violated": audit.status == InvariantStatus.VIOLATED,
        "capacity": audit.violation == InvariantViolationKind.CAPACITY_CLASS_WORSENED,
        "after_overspent": audit.after.capacity_class == CapacityClass.OVERSPENT,
    }
    return {"name": "check_T_invariant_capacity_worsening_P", "consistent": all(tests.values()), "status": "P_invariants" if all(tests.values()) else "FAIL", "summary": "Invariant audit catches capacity-class worsening.", "data": {"tests": tests, "audit": audit.to_dict()}, "dependencies": ["check_T_invariant_provenance_violation_P"]}


def check_T_interface_kinematic_invariants_P() -> Dict[str, Any]:
    subchecks = [
        check_T_invariant_signature_EW_P(),
        check_T_invariant_monotone_repair_P(),
        check_T_invariant_provenance_violation_P(),
        check_T_invariant_capacity_worsening_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {"name": "check_T_interface_kinematic_invariants_P", "consistent": ok, "status": "P_invariants" if ok else "FAIL", "summary": "Interface Kinematic Invariants is P: payload transitions are audited for progress, capacity, provenance, blocked-field, and export invariants.", "data": {"core_claim": "Admissible interface motion is constrained by invariants that must be preserved or monotonically refined.", "subchecks": [x["name"] for x in subchecks]}, "dependencies": [x["name"] for x in subchecks]}


CHECKS = {
    "check_T_invariant_signature_EW_P": check_T_invariant_signature_EW_P,
    "check_T_invariant_monotone_repair_P": check_T_invariant_monotone_repair_P,
    "check_T_invariant_provenance_violation_P": check_T_invariant_provenance_violation_P,
    "check_T_invariant_capacity_worsening_P": check_T_invariant_capacity_worsening_P,
    "check_T_interface_kinematic_invariants_P": check_T_interface_kinematic_invariants_P,
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
            raise TypeError("Unsupported registry type for interface_kinematic_invariants.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
