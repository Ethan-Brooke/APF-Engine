"""
APF Interface Kinematic Holonomy Diagnostics.

Purpose
-------
Detect curvature/path-memory in interface phase space:

    payload + closed transition loop
      -> forward path
      -> reverse/return path
      -> residual state/field defect
      -> holonomy certificate

Core idea
---------
A closed interface loop need not return to the same admissibility state when typed moves
consume, expose, or depend on finite interface capacity.

Boundary
--------
Holonomy diagnostics are structural/path-memory diagnostics. They do not supply evidence,
repair loops, or promote held physics claims.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List
import json

from apf.interface_kinematics_engine import (
    compute_kinematic_certificate,
    KinematicState,
    TransitionStatus,
)
from apf.interface_kinematics_order_defects import (
    classify_order_defect,
    canonical_move_order,
    evaluate_ordered_path,
)


class HolonomyStatus(str, Enum):
    FLAT_RETURN = "FLAT_RETURN"
    CURVED_RESIDUAL = "CURVED_RESIDUAL"
    LOOP_FORBIDDEN = "LOOP_FORBIDDEN"
    FAIL_CLOSED_PROVENANCE = "FAIL_CLOSED_PROVENANCE"
    STRUCTURAL_BLOCK = "STRUCTURAL_BLOCK"


class HolonomyDefect(str, Enum):
    NONE = "NONE"
    STATE_RESIDUAL = "STATE_RESIDUAL"
    BLOCKER_RESIDUAL = "BLOCKER_RESIDUAL"
    FIELD_MEMORY = "FIELD_MEMORY"
    ORDER_CURVATURE = "ORDER_CURVATURE"
    PROVENANCE_PROPAGATION = "PROVENANCE_PROPAGATION"
    STRUCTURAL_PROPAGATION = "STRUCTURAL_PROPAGATION"


@dataclass(frozen=True)
class HolonomyLoop:
    route: str
    payload: Mapping[str, Any]
    forward_order: Tuple[str, ...]
    return_order: Tuple[str, ...]
    loop_id: str = "loop"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "route": self.route,
            "payload": dict(self.payload),
            "forward_order": list(self.forward_order),
            "return_order": list(self.return_order),
            "loop_id": self.loop_id,
        }


@dataclass(frozen=True)
class HolonomyCertificate:
    loop_id: str
    route: str
    status: HolonomyStatus
    defect: HolonomyDefect
    forward_final_state: str
    return_final_state: str
    canonical_final_state: str
    forward_blocker: Optional[str]
    return_blocker: Optional[str]
    residual_fields: Tuple[str, ...]
    curvature_score: float
    summary: str
    boundary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "loop_id": self.loop_id,
            "route": self.route,
            "status": self.status.value,
            "defect": self.defect.value,
            "forward_final_state": self.forward_final_state,
            "return_final_state": self.return_final_state,
            "canonical_final_state": self.canonical_final_state,
            "forward_blocker": self.forward_blocker,
            "return_blocker": self.return_blocker,
            "residual_fields": list(self.residual_fields),
            "curvature_score": self.curvature_score,
            "summary": self.summary,
            "boundary": self.boundary,
        }


MEMORY_FIELDS = {
    "codomain_transport_found",
    "evaluator_map_found",
    "counterterm_finite_parts_declared",
    "uncertainty_protocol_declared",
    "overlap_cocycle_verified",
    "overlap_gluing_verified",
    "capacity_bound_checked",
    "entropy_ledger_clean",
    "data_ledger_clean",
    "external_constants_ledger_clean",
}


def _fields_touched_by_order(route: str, order: Iterable[str]) -> Tuple[str, ...]:
    from apf.interface_kinematics_engine import route_path
    mapping = {move: field for move, _, _, field in route_path(route if route in {"ew","dark","gauge","horizon","capacity","generic"} else "generic")}
    fields = []
    for move in order:
        field = mapping.get(move)
        if field and field in MEMORY_FIELDS:
            fields.append(field)
    return tuple(dict.fromkeys(fields))


def _blocked_field_from_order(route: str, payload: Mapping[str, Any], order: Iterable[str]) -> Optional[str]:
    from apf.interface_kinematics_engine import route_path
    mapping = {move: field for move, _, _, field in route_path(route if route in {"ew","dark","gauge","horizon","capacity","generic"} else "generic")}
    path = evaluate_ordered_path(route, payload, order)
    if path.first_blocked_move:
        return mapping.get(path.first_blocked_move)
    return None


def compute_holonomy(loop: HolonomyLoop) -> HolonomyCertificate:
    route = loop.route
    payload = loop.payload
    boundary = "Holonomy diagnostics detect structural path-memory only; they do not supply evidence or promote held claims."

    base_cert = compute_kinematic_certificate(route, payload)
    canonical_order = canonical_move_order(route)
    canonical = evaluate_ordered_path(route, payload, canonical_order)

    if base_cert.fail_closed:
        return HolonomyCertificate(loop.loop_id, route, HolonomyStatus.FAIL_CLOSED_PROVENANCE, HolonomyDefect.PROVENANCE_PROPAGATION, base_cert.current_state.value, base_cert.current_state.value, canonical.final_state.value, "reject_provenance", "reject_provenance", tuple(), 1.0, "Loop fail-closes because payload carries provenance failure.", boundary)

    if base_cert.structural_block:
        return HolonomyCertificate(loop.loop_id, route, HolonomyStatus.STRUCTURAL_BLOCK, HolonomyDefect.STRUCTURAL_PROPAGATION, base_cert.current_state.value, base_cert.current_state.value, canonical.final_state.value, "escalate_structural", "escalate_structural", tuple(), 1.0, "Loop structurally blocked by theorem/substrate requirement.", boundary)

    forward = evaluate_ordered_path(route, payload, loop.forward_order)
    ret = evaluate_ordered_path(route, payload, loop.return_order)

    forward_fields = set(_fields_touched_by_order(route, loop.forward_order))
    return_fields = set(_fields_touched_by_order(route, loop.return_order))
    residual_fields = tuple(sorted((forward_fields ^ return_fields) | {f for f in [_blocked_field_from_order(route, payload, loop.forward_order), _blocked_field_from_order(route, payload, loop.return_order)] if f}))

    if forward.first_blocked_move or ret.first_blocked_move:
        defect = HolonomyDefect.BLOCKER_RESIDUAL if forward.first_blocked_move != ret.first_blocked_move else HolonomyDefect.ORDER_CURVATURE
        score = 1.0 if forward.first_blocked_move != ret.first_blocked_move else 0.75
        return HolonomyCertificate(
            loop.loop_id,
            route,
            HolonomyStatus.LOOP_FORBIDDEN,
            defect,
            forward.final_state.value,
            ret.final_state.value,
            canonical.final_state.value,
            forward.first_blocked_move,
            ret.first_blocked_move,
            residual_fields,
            score,
            f"Loop forbidden: forward blocker={forward.first_blocked_move}, return blocker={ret.first_blocked_move}.",
            boundary,
        )

    if forward.final_state != ret.final_state:
        return HolonomyCertificate(
            loop.loop_id,
            route,
            HolonomyStatus.CURVED_RESIDUAL,
            HolonomyDefect.STATE_RESIDUAL,
            forward.final_state.value,
            ret.final_state.value,
            canonical.final_state.value,
            None,
            None,
            residual_fields,
            1.0,
            f"Closed loop has state residual: forward={forward.final_state.value}, return={ret.final_state.value}.",
            boundary,
        )

    if residual_fields:
        return HolonomyCertificate(
            loop.loop_id,
            route,
            HolonomyStatus.CURVED_RESIDUAL,
            HolonomyDefect.FIELD_MEMORY,
            forward.final_state.value,
            ret.final_state.value,
            canonical.final_state.value,
            None,
            None,
            residual_fields,
            min(1.0, 0.25 + 0.1 * len(residual_fields)),
            f"Loop returns to same state but carries field-memory residuals: {residual_fields}.",
            boundary,
        )

    return HolonomyCertificate(
        loop.loop_id,
        route,
        HolonomyStatus.FLAT_RETURN,
        HolonomyDefect.NONE,
        forward.final_state.value,
        ret.final_state.value,
        canonical.final_state.value,
        None,
        None,
        tuple(),
        0.0,
        "Loop is flat under this structural test: same state, no blocker, no residual field-memory.",
        boundary,
    )


def load_holonomy_loops(path: str) -> Tuple[HolonomyLoop, ...]:
    data = json.loads(open(path, "r", encoding="utf-8").read())
    rows = data.get("loops", data)
    out = []
    for idx, row in enumerate(rows):
        route = str(row.get("route", "generic"))
        out.append(HolonomyLoop(
            route=route,
            payload=row.get("payload", {}),
            forward_order=tuple(row.get("forward_order", canonical_move_order(route))),
            return_order=tuple(row.get("return_order", canonical_move_order(route))),
            loop_id=str(row.get("loop_id", f"loop_{idx:03d}")),
        ))
    return tuple(out)


def compute_holonomy_batch(loops: Iterable[HolonomyLoop]) -> Mapping[str, Any]:
    certs = tuple(compute_holonomy(loop) for loop in loops)
    status_counts: Dict[str, int] = {}
    defect_counts: Dict[str, int] = {}
    for cert in certs:
        status_counts[cert.status.value] = status_counts.get(cert.status.value, 0) + 1
        defect_counts[cert.defect.value] = defect_counts.get(cert.defect.value, 0) + 1
    return {
        "created_utc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "certificates": [c.to_dict() for c in certs],
        "status_counts": status_counts,
        "defect_counts": defect_counts,
        "max_curvature_score": max((c.curvature_score for c in certs), default=0.0),
        "boundary": "Batch holonomy diagnostics are structural/path-memory only; they do not promote held claims.",
    }


def check_T_holonomy_flat_canonical_P() -> Dict[str, Any]:
    payload = {
        "route_built": True, "run_completed": True, "chains_converged": True, "posterior_closed": True,
        "robustness_checks_passed": True, "codomain_transport_found": True, "evaluator_map_found": True,
        "data_ledger_clean": True, "target_value_consumed": False,
    }
    order = canonical_move_order("dark")
    cert = compute_holonomy(HolonomyLoop("dark", payload, order, order, "flat_dark"))
    tests = {
        "flat": cert.status == HolonomyStatus.FLAT_RETURN,
        "none": cert.defect == HolonomyDefect.NONE,
        "score_zero": cert.curvature_score == 0.0,
    }
    return {"name": "check_T_holonomy_flat_canonical_P", "consistent": all(tests.values()), "status": "P_holonomy" if all(tests.values()) else "FAIL", "summary": "Holonomy diagnostic recognizes flat canonical loop.", "data": {"tests": tests, "certificate": cert.to_dict()}}


def check_T_holonomy_order_curvature_P() -> Dict[str, Any]:
    payload = {
        "trace_sector_closed": True,
        "source_to_scheme_registry_present": True,
        "codomain_transport_found": True,
        "evaluator_map_found": True,
        "counterterm_finite_parts_declared": True,
        "external_constants_ledger_clean": True,
        "uncertainty_protocol_declared": True,
        "target_value_consumed": False,
    }
    canon = list(canonical_move_order("ew"))
    proposed = list(canon)
    proposed.insert(1, proposed.pop(proposed.index("instantiate_evaluator")))
    cert = compute_holonomy(HolonomyLoop("ew", payload, canon, proposed, "ew_order_loop"))
    tests = {
        "forbidden": cert.status == HolonomyStatus.LOOP_FORBIDDEN,
        "has_defect": cert.defect in {HolonomyDefect.BLOCKER_RESIDUAL, HolonomyDefect.ORDER_CURVATURE},
        "blocker": cert.return_blocker == "instantiate_evaluator",
    }
    return {"name": "check_T_holonomy_order_curvature_P", "consistent": all(tests.values()), "status": "P_holonomy" if all(tests.values()) else "FAIL", "summary": "Holonomy detects order curvature when return path violates prerequisites.", "data": {"tests": tests, "certificate": cert.to_dict()}, "dependencies": ["check_T_holonomy_flat_canonical_P"]}


def check_T_holonomy_field_memory_P() -> Dict[str, Any]:
    payload = {
        "local_fiber_action_defined": True,
        "group_law_verified": True,
        "representation_faithful": True,
        "codomain_map_declared": True,
        "overlap_cocycle_verified": True,
        "anomaly_check_passed": True,
        "target_value_consumed": False,
    }
    canon = canonical_move_order("gauge")
    # Partial same-state-ish loop: forward touches overlap/anomaly, return omits final anomaly export tail.
    fwd = canon
    ret = canon[:-2] + canon[-1:]
    cert = compute_holonomy(HolonomyLoop("gauge", payload, fwd, ret, "gauge_memory"))
    tests = {
        "curved_or_forbidden": cert.status in {HolonomyStatus.CURVED_RESIDUAL, HolonomyStatus.LOOP_FORBIDDEN},
        "nonzero": cert.curvature_score > 0,
        "residuals_or_state": cert.defect in {HolonomyDefect.FIELD_MEMORY, HolonomyDefect.STATE_RESIDUAL, HolonomyDefect.BLOCKER_RESIDUAL, HolonomyDefect.ORDER_CURVATURE},
    }
    return {"name": "check_T_holonomy_field_memory_P", "consistent": all(tests.values()), "status": "P_holonomy" if all(tests.values()) else "FAIL", "summary": "Holonomy detects residual memory/state defect for incomplete return path.", "data": {"tests": tests, "certificate": cert.to_dict()}, "dependencies": ["check_T_holonomy_order_curvature_P"]}


def check_T_holonomy_provenance_priority_P() -> Dict[str, Any]:
    cert = compute_holonomy(HolonomyLoop("ew", {"target_value_consumed": True}, canonical_move_order("ew"), canonical_move_order("ew"), "bad_loop"))
    tests = {
        "fail_closed": cert.status == HolonomyStatus.FAIL_CLOSED_PROVENANCE,
        "defect": cert.defect == HolonomyDefect.PROVENANCE_PROPAGATION,
        "score_one": cert.curvature_score == 1.0,
    }
    return {"name": "check_T_holonomy_provenance_priority_P", "consistent": all(tests.values()), "status": "P_holonomy" if all(tests.values()) else "FAIL", "summary": "Holonomy preserves provenance fail-closed priority.", "data": {"tests": tests, "certificate": cert.to_dict()}, "dependencies": ["check_T_holonomy_field_memory_P"]}


def check_T_interface_kinematic_holonomy_diagnostics_P() -> Dict[str, Any]:
    subchecks = [
        check_T_holonomy_flat_canonical_P(),
        check_T_holonomy_order_curvature_P(),
        check_T_holonomy_field_memory_P(),
        check_T_holonomy_provenance_priority_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {"name": "check_T_interface_kinematic_holonomy_diagnostics_P", "consistent": ok, "status": "P_holonomy" if ok else "FAIL", "summary": "Interface Kinematic Holonomy Diagnostics is P: closed interface loops are tested for flat return, residual memory, order curvature, and hard-stop propagation.", "data": {"core_claim": "Closed loops in interface phase space can accumulate structural defects under typed finite-capacity movement.", "subchecks": [x["name"] for x in subchecks]}, "dependencies": [x["name"] for x in subchecks]}


CHECKS = {
    "check_T_holonomy_flat_canonical_P": check_T_holonomy_flat_canonical_P,
    "check_T_holonomy_order_curvature_P": check_T_holonomy_order_curvature_P,
    "check_T_holonomy_field_memory_P": check_T_holonomy_field_memory_P,
    "check_T_holonomy_provenance_priority_P": check_T_holonomy_provenance_priority_P,
    "check_T_interface_kinematic_holonomy_diagnostics_P": check_T_interface_kinematic_holonomy_diagnostics_P,
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
            raise TypeError("Unsupported registry type for interface_kinematic_holonomy_diagnostics.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
