"""
APF Interface Kinematics Engine.

Purpose
-------
Model how interface structure moves, before dynamics:

    route payload
      -> canonical kinematic state
      -> route transition path
      -> admissible/blocked moves
      -> first blocked transition
      -> nearest repair state
      -> path certificate

Boundary
--------
Kinematics describes allowed structural movement through interface gates. It does not
promote physics claims to P and does not supply missing evidence.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List
import json


class KinematicState(str, Enum):
    UNSEEN = "UNSEEN"
    LOCAL_OBJECT_PRESENT = "LOCAL_OBJECT_PRESENT"
    LOCAL_CLOSURE = "LOCAL_CLOSURE"
    SOURCE_TYPED = "SOURCE_TYPED"
    CODOMAIN_TYPED = "CODOMAIN_TYPED"
    TRANSPORT_DEFINED = "TRANSPORT_DEFINED"
    EVALUATOR_DEFINED = "EVALUATOR_DEFINED"
    COUNTERTERM_NORMALIZED = "COUNTERTERM_NORMALIZED"
    UNCERTAINTY_LEDGERED = "UNCERTAINTY_LEDGERED"
    RUN_COMPLETED = "RUN_COMPLETED"
    CHAINS_CONVERGED = "CHAINS_CONVERGED"
    POSTERIOR_CLOSED = "POSTERIOR_CLOSED"
    ROBUSTNESS_PASSED = "ROBUSTNESS_PASSED"
    GROUP_LAW_VERIFIED = "GROUP_LAW_VERIFIED"
    REPRESENTATION_FAITHFUL = "REPRESENTATION_FAITHFUL"
    OVERLAP_GLUED = "OVERLAP_GLUED"
    ANOMALY_CLEAN = "ANOMALY_CLEAN"
    AREA_COST_DEFINED = "AREA_COST_DEFINED"
    CAPACITY_BOUND_CHECKED = "CAPACITY_BOUND_CHECKED"
    ENTROPY_LEDGER_CLEAN = "ENTROPY_LEDGER_CLEAN"
    CAPACITY_BUDGET_VERIFIED = "CAPACITY_BUDGET_VERIFIED"
    COARSE_GRAINED_ADMISSIBLE = "COARSE_GRAINED_ADMISSIBLE"
    GLOBAL_EXPORTABLE = "GLOBAL_EXPORTABLE"
    FAIL_CLOSED_PROVENANCE = "FAIL_CLOSED_PROVENANCE"
    STRUCTURAL_BLOCK = "STRUCTURAL_BLOCK"


class TransitionStatus(str, Enum):
    ALLOWED = "ALLOWED"
    BLOCKED = "BLOCKED"
    FORBIDDEN = "FORBIDDEN"
    NOT_REACHED = "NOT_REACHED"


@dataclass(frozen=True)
class KinematicTransition:
    move: str
    from_state: KinematicState
    to_state: KinematicState
    required_field: Optional[str]
    status: TransitionStatus
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["from_state"] = self.from_state.value
        d["to_state"] = self.to_state.value
        d["status"] = self.status.value
        return d


@dataclass(frozen=True)
class KinematicCertificate:
    route: str
    current_state: KinematicState
    target_state: KinematicState
    path: Tuple[KinematicTransition, ...]
    first_blocked_move: Optional[str]
    first_blocked_state: Optional[KinematicState]
    nearest_repair_state: Optional[KinematicState]
    exportable: bool
    fail_closed: bool
    structural_block: bool
    boundary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "route": self.route,
            "current_state": self.current_state.value,
            "target_state": self.target_state.value,
            "path": [p.to_dict() for p in self.path],
            "first_blocked_move": self.first_blocked_move,
            "first_blocked_state": self.first_blocked_state.value if self.first_blocked_state else None,
            "nearest_repair_state": self.nearest_repair_state.value if self.nearest_repair_state else None,
            "exportable": self.exportable,
            "fail_closed": self.fail_closed,
            "structural_block": self.structural_block,
            "boundary": self.boundary,
        }


# Route path specification:
# (move_name, from_state, to_state, required_payload_field)
ROUTE_PATHS: Dict[str, Tuple[Tuple[str, KinematicState, KinematicState, Optional[str]], ...]] = {
    "ew": (
        ("observe_trace_object", KinematicState.UNSEEN, KinematicState.LOCAL_OBJECT_PRESENT, "trace_sector_closed"),
        ("close_local_trace", KinematicState.LOCAL_OBJECT_PRESENT, KinematicState.LOCAL_CLOSURE, "trace_sector_closed"),
        ("type_source_registry", KinematicState.LOCAL_CLOSURE, KinematicState.SOURCE_TYPED, "source_to_scheme_registry_present"),
        ("declare_codomain_transport", KinematicState.SOURCE_TYPED, KinematicState.CODOMAIN_TYPED, "codomain_transport_found"),
        ("define_transport", KinematicState.CODOMAIN_TYPED, KinematicState.TRANSPORT_DEFINED, "codomain_transport_found"),
        ("instantiate_evaluator", KinematicState.TRANSPORT_DEFINED, KinematicState.EVALUATOR_DEFINED, "evaluator_map_found"),
        ("normalize_counterterms", KinematicState.EVALUATOR_DEFINED, KinematicState.COUNTERTERM_NORMALIZED, "counterterm_finite_parts_declared"),
        ("attach_uncertainty_ledger", KinematicState.COUNTERTERM_NORMALIZED, KinematicState.UNCERTAINTY_LEDGERED, "uncertainty_protocol_declared"),
        ("export_physical_scheme", KinematicState.UNCERTAINTY_LEDGERED, KinematicState.GLOBAL_EXPORTABLE, "external_constants_ledger_clean"),
    ),
    "dark": (
        ("build_route", KinematicState.UNSEEN, KinematicState.LOCAL_OBJECT_PRESENT, "route_built"),
        ("complete_runtime", KinematicState.LOCAL_OBJECT_PRESENT, KinematicState.RUN_COMPLETED, "run_completed"),
        ("converge_chains", KinematicState.RUN_COMPLETED, KinematicState.CHAINS_CONVERGED, "chains_converged"),
        ("close_posterior", KinematicState.CHAINS_CONVERGED, KinematicState.POSTERIOR_CLOSED, "posterior_closed"),
        ("pass_robustness", KinematicState.POSTERIOR_CLOSED, KinematicState.ROBUSTNESS_PASSED, "robustness_checks_passed"),
        ("declare_dark_codomain", KinematicState.ROBUSTNESS_PASSED, KinematicState.CODOMAIN_TYPED, "codomain_transport_found"),
        ("instantiate_dark_evaluator", KinematicState.CODOMAIN_TYPED, KinematicState.EVALUATOR_DEFINED, "evaluator_map_found"),
        ("export_dark_posterior", KinematicState.EVALUATOR_DEFINED, KinematicState.GLOBAL_EXPORTABLE, "data_ledger_clean"),
    ),
    "gauge": (
        ("observe_local_fiber_action", KinematicState.UNSEEN, KinematicState.LOCAL_OBJECT_PRESENT, "local_fiber_action_defined"),
        ("verify_group_law", KinematicState.LOCAL_OBJECT_PRESENT, KinematicState.GROUP_LAW_VERIFIED, "group_law_verified"),
        ("verify_faithful_representation", KinematicState.GROUP_LAW_VERIFIED, KinematicState.REPRESENTATION_FAITHFUL, "representation_faithful"),
        ("declare_codomain_map", KinematicState.REPRESENTATION_FAITHFUL, KinematicState.CODOMAIN_TYPED, "codomain_map_declared"),
        ("verify_overlap_cocycle", KinematicState.CODOMAIN_TYPED, KinematicState.OVERLAP_GLUED, "overlap_cocycle_verified"),
        ("pass_anomaly_check", KinematicState.OVERLAP_GLUED, KinematicState.ANOMALY_CLEAN, "anomaly_check_passed"),
        ("export_gauge_route", KinematicState.ANOMALY_CLEAN, KinematicState.GLOBAL_EXPORTABLE, None),
    ),
    "horizon": (
        ("observe_horizon_partition", KinematicState.UNSEEN, KinematicState.LOCAL_OBJECT_PRESENT, "horizon_partition_defined"),
        ("define_area_cost_map", KinematicState.LOCAL_OBJECT_PRESENT, KinematicState.AREA_COST_DEFINED, "area_cost_map_defined"),
        ("verify_overlap_gluing", KinematicState.AREA_COST_DEFINED, KinematicState.OVERLAP_GLUED, "overlap_gluing_verified"),
        ("check_capacity_bound", KinematicState.OVERLAP_GLUED, KinematicState.CAPACITY_BOUND_CHECKED, "capacity_bound_checked"),
        ("clean_entropy_ledger", KinematicState.CAPACITY_BOUND_CHECKED, KinematicState.ENTROPY_LEDGER_CLEAN, "entropy_ledger_clean"),
        ("declare_horizon_codomain", KinematicState.ENTROPY_LEDGER_CLEAN, KinematicState.CODOMAIN_TYPED, "codomain_transport_found"),
        ("export_horizon_cost", KinematicState.CODOMAIN_TYPED, KinematicState.GLOBAL_EXPORTABLE, None),
    ),
    "capacity": (
        ("observe_capacity_load", KinematicState.UNSEEN, KinematicState.LOCAL_OBJECT_PRESENT, "raw_capacity_load"),
        ("verify_capacity_budget", KinematicState.LOCAL_OBJECT_PRESENT, KinematicState.CAPACITY_BUDGET_VERIFIED, "capacity_budget"),
        ("apply_coarse_graining", KinematicState.CAPACITY_BUDGET_VERIFIED, KinematicState.COARSE_GRAINED_ADMISSIBLE, "coarse_grain_factor"),
        ("export_capacity_state", KinematicState.COARSE_GRAINED_ADMISSIBLE, KinematicState.GLOBAL_EXPORTABLE, None),
    ),
    "generic": (
        ("observe_local_object", KinematicState.UNSEEN, KinematicState.LOCAL_OBJECT_PRESENT, "local_solution_found"),
        ("declare_codomain", KinematicState.LOCAL_OBJECT_PRESENT, KinematicState.CODOMAIN_TYPED, "codomain_transport_found"),
        ("instantiate_evaluator", KinematicState.CODOMAIN_TYPED, KinematicState.EVALUATOR_DEFINED, "evaluator_map_found"),
        ("verify_capacity_budget", KinematicState.EVALUATOR_DEFINED, KinematicState.CAPACITY_BUDGET_VERIFIED, "capacity_budget_verified"),
        ("export_generic", KinematicState.CAPACITY_BUDGET_VERIFIED, KinematicState.GLOBAL_EXPORTABLE, "empirical_or_posterior_closed"),
    ),
}


def _truthy(payload: Mapping[str, Any], field: Optional[str]) -> bool:
    if field is None:
        return True
    if field not in payload:
        return False
    value = payload[field]
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value > 0
    if isinstance(value, str):
        return value.strip().lower() not in {"", "false", "0", "none", "null", "no"}
    return bool(value)


def _capacity_overspend(payload: Mapping[str, Any]) -> bool:
    try:
        load = float(payload.get("raw_capacity_load", 0))
        budget = float(payload.get("capacity_budget", 0))
        cg = float(payload.get("coarse_grain_factor", 1))
        if cg <= 0:
            return True
        return load / cg > budget
    except Exception:
        return False


def route_path(route: str) -> Tuple[Tuple[str, KinematicState, KinematicState, Optional[str]], ...]:
    return ROUTE_PATHS.get(route, ROUTE_PATHS["generic"])


def provenance_fail_closed(payload: Mapping[str, Any]) -> bool:
    if bool(payload.get("target_value_consumed", False)):
        return True
    inputs = set(payload.get("inputs_used", []) or [])
    targets = set(payload.get("declared_targets", []) or [])
    allowed = set(payload.get("allowed_exogenous_inputs", []) or [])
    return bool((inputs & targets) - allowed)


def structural_blocked(route: str, payload: Mapping[str, Any]) -> bool:
    if route == "cstar":
        return True
    return bool(payload.get("structural_blocker", False) or payload.get("substrate_theorem_required", False))


def compute_kinematic_certificate(route: str, payload: Mapping[str, Any]) -> KinematicCertificate:
    route = route if route in ROUTE_PATHS else "generic"
    boundary = "Kinematics describes structural movement only; missing evidence is not supplied and held physics claims are not promoted."

    if provenance_fail_closed(payload):
        return KinematicCertificate(
            route=route,
            current_state=KinematicState.FAIL_CLOSED_PROVENANCE,
            target_state=KinematicState.GLOBAL_EXPORTABLE,
            path=tuple(),
            first_blocked_move="reject_provenance",
            first_blocked_state=KinematicState.FAIL_CLOSED_PROVENANCE,
            nearest_repair_state=None,
            exportable=False,
            fail_closed=True,
            structural_block=False,
            boundary=boundary,
        )

    if structural_blocked(route, payload):
        return KinematicCertificate(
            route=route,
            current_state=KinematicState.STRUCTURAL_BLOCK,
            target_state=KinematicState.GLOBAL_EXPORTABLE,
            path=tuple(),
            first_blocked_move="escalate_structural",
            first_blocked_state=KinematicState.STRUCTURAL_BLOCK,
            nearest_repair_state=None,
            exportable=False,
            fail_closed=False,
            structural_block=True,
            boundary=boundary,
        )

    path_entries = route_path(route)
    transitions: List[KinematicTransition] = []
    current = KinematicState.UNSEEN
    first_blocked: Optional[KinematicTransition] = None

    for move, from_state, to_state, field in path_entries:
        if first_blocked is not None:
            transitions.append(KinematicTransition(move, from_state, to_state, field, TransitionStatus.NOT_REACHED, "prior transition blocked"))
            continue

        if current != from_state:
            transitions.append(KinematicTransition(move, from_state, to_state, field, TransitionStatus.FORBIDDEN, f"state mismatch: current={current.value}, expected={from_state.value}"))
            first_blocked = transitions[-1]
            continue

        if route == "capacity" and move == "export_capacity_state" and _capacity_overspend(payload):
            tr = KinematicTransition(move, from_state, to_state, field, TransitionStatus.BLOCKED, "capacity overspend remains after coarse graining")
            transitions.append(tr)
            first_blocked = tr
            continue

        if _truthy(payload, field):
            tr = KinematicTransition(move, from_state, to_state, field, TransitionStatus.ALLOWED, "required field satisfied" if field else "no additional field required")
            transitions.append(tr)
            current = to_state
        else:
            tr = KinematicTransition(move, from_state, to_state, field, TransitionStatus.BLOCKED, f"missing or false required field: {field}")
            transitions.append(tr)
            first_blocked = tr

    exportable = current == KinematicState.GLOBAL_EXPORTABLE and first_blocked is None
    nearest = first_blocked.from_state if first_blocked else current
    return KinematicCertificate(
        route=route,
        current_state=current,
        target_state=KinematicState.GLOBAL_EXPORTABLE,
        path=tuple(transitions),
        first_blocked_move=first_blocked.move if first_blocked else None,
        first_blocked_state=first_blocked.from_state if first_blocked else None,
        nearest_repair_state=nearest if not exportable else None,
        exportable=exportable,
        fail_closed=False,
        structural_block=False,
        boundary=boundary,
    )


def next_required_field(cert: KinematicCertificate) -> Optional[str]:
    for tr in cert.path:
        if tr.status == TransitionStatus.BLOCKED:
            return tr.required_field
    return None


def summarize_kinematics(cert: KinematicCertificate) -> str:
    if cert.exportable:
        return f"{cert.route}: path reaches GLOBAL_EXPORTABLE."
    if cert.fail_closed:
        return f"{cert.route}: fail-closed provenance; clean rebuild required."
    if cert.structural_block:
        return f"{cert.route}: structural blocker; theorem/substrate repair required."
    field = next_required_field(cert)
    return f"{cert.route}: halted at {cert.current_state.value}; next blocked move={cert.first_blocked_move}; required_field={field}."


def check_T_kinematics_EW_path_P() -> Dict[str, Any]:
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
    cert = compute_kinematic_certificate("ew", payload)
    tests = {
        "not_exportable": cert.exportable is False,
        "halts_source_typed": cert.current_state == KinematicState.SOURCE_TYPED,
        "blocked_codomain": cert.first_blocked_move == "declare_codomain_transport",
        "required_codomain": next_required_field(cert) == "codomain_transport_found",
    }
    return {"name": "check_T_kinematics_EW_path_P", "consistent": all(tests.values()), "status": "P_kinematics" if all(tests.values()) else "FAIL", "summary": "EW kinematics halts at the first missing codomain transport move.", "data": {"tests": tests, "certificate": cert.to_dict()}}


def check_T_kinematics_dark_export_P() -> Dict[str, Any]:
    payload = {
        "route_built": True,
        "run_completed": True,
        "chains_converged": True,
        "posterior_closed": True,
        "robustness_checks_passed": True,
        "codomain_transport_found": True,
        "evaluator_map_found": True,
        "data_ledger_clean": True,
        "target_value_consumed": False,
    }
    cert = compute_kinematic_certificate("dark", payload)
    tests = {
        "exportable": cert.exportable is True,
        "global_state": cert.current_state == KinematicState.GLOBAL_EXPORTABLE,
        "no_blocked": cert.first_blocked_move is None,
    }
    return {"name": "check_T_kinematics_dark_export_P", "consistent": all(tests.values()), "status": "P_kinematics" if all(tests.values()) else "FAIL", "summary": "Dark route kinematics reaches GLOBAL_EXPORTABLE when every transition field is satisfied.", "data": {"tests": tests, "certificate": cert.to_dict()}, "dependencies": ["check_T_kinematics_EW_path_P"]}


def check_T_kinematics_provenance_fail_closed_P() -> Dict[str, Any]:
    payload = {"target_value_consumed": True, "trace_sector_closed": True}
    cert = compute_kinematic_certificate("ew", payload)
    tests = {
        "fail_closed": cert.fail_closed is True,
        "state_fail_closed": cert.current_state == KinematicState.FAIL_CLOSED_PROVENANCE,
        "not_exportable": cert.exportable is False,
        "no_repair_state": cert.nearest_repair_state is None,
    }
    return {"name": "check_T_kinematics_provenance_fail_closed_P", "consistent": all(tests.values()), "status": "P_kinematics" if all(tests.values()) else "FAIL", "summary": "Kinematics fail-closes provenance before ordinary transition repair.", "data": {"tests": tests, "certificate": cert.to_dict()}, "dependencies": ["check_T_kinematics_dark_export_P"]}


def check_T_kinematics_capacity_overspend_P() -> Dict[str, Any]:
    payload = {"raw_capacity_load": 100, "capacity_budget": 25, "coarse_grain_factor": 2, "target_value_consumed": False}
    cert = compute_kinematic_certificate("capacity", payload)
    tests = {
        "not_exportable": cert.exportable is False,
        "blocked_export": cert.first_blocked_move == "export_capacity_state",
        "reason_overspend": "overspend" in [tr.reason for tr in cert.path if tr.move == "export_capacity_state"][0],
    }
    return {"name": "check_T_kinematics_capacity_overspend_P", "consistent": all(tests.values()), "status": "P_kinematics" if all(tests.values()) else "FAIL", "summary": "Capacity kinematics detects overspend after coarse-graining.", "data": {"tests": tests, "certificate": cert.to_dict()}, "dependencies": ["check_T_kinematics_provenance_fail_closed_P"]}


def check_T_interface_kinematics_engine_P() -> Dict[str, Any]:
    subchecks = [
        check_T_kinematics_EW_path_P(),
        check_T_kinematics_dark_export_P(),
        check_T_kinematics_provenance_fail_closed_P(),
        check_T_kinematics_capacity_overspend_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {"name": "check_T_interface_kinematics_engine_P", "consistent": ok, "status": "P_kinematics" if ok else "FAIL", "summary": "Interface Kinematics Engine is P: route payloads produce states, transition paths, first blocked moves, and repair-state targets.", "data": {"core_claim": "The engine models structural movement through interface gates without supplying evidence or promoting held claims.", "subchecks": [x["name"] for x in subchecks]}, "dependencies": [x["name"] for x in subchecks]}


CHECKS = {
    "check_T_kinematics_EW_path_P": check_T_kinematics_EW_path_P,
    "check_T_kinematics_dark_export_P": check_T_kinematics_dark_export_P,
    "check_T_kinematics_provenance_fail_closed_P": check_T_kinematics_provenance_fail_closed_P,
    "check_T_kinematics_capacity_overspend_P": check_T_kinematics_capacity_overspend_P,
    "check_T_interface_kinematics_engine_P": check_T_interface_kinematics_engine_P,
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
            raise TypeError("Unsupported registry type for interface_kinematics_engine.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
