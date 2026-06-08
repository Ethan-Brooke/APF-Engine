"""
APF Interface Kinematics Order Defects.

Purpose
-------
Detect noncommuting / path-dependent transition order defects:

    route payload + proposed move orders
      -> canonical path certificate
      -> alternative order certificate
      -> commutation table
      -> first order defect
      -> admissible normal form hint

Core principle
--------------
Interface moves are typed and capacity-bearing. Reordering them is not free.

Boundary
--------
Order-defect kinematics detects path dependence. It does not repair missing evidence,
supply omitted maps, or promote held route claims.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List
import json

from apf.interface_kinematics_engine import (
    KinematicState,
    TransitionStatus,
    KinematicTransition,
    compute_kinematic_certificate,
    route_path,
    provenance_fail_closed,
    structural_blocked,
    _truthy,
    _capacity_overspend,
)


class OrderDefectStatus(str, Enum):
    ORDER_ADMISSIBLE = "ORDER_ADMISSIBLE"
    ORDER_DEPENDENT = "ORDER_DEPENDENT"
    ORDER_FORBIDDEN = "ORDER_FORBIDDEN"
    FAIL_CLOSED_PROVENANCE = "FAIL_CLOSED_PROVENANCE"
    STRUCTURAL_BLOCK = "STRUCTURAL_BLOCK"


class OrderDefectKind(str, Enum):
    NONE = "NONE"
    PREREQUISITE_VIOLATION = "PREREQUISITE_VIOLATION"
    DIFFERENT_FINAL_STATE = "DIFFERENT_FINAL_STATE"
    DIFFERENT_BLOCKER = "DIFFERENT_BLOCKER"
    CAPACITY_ORDER_DEFECT = "CAPACITY_ORDER_DEFECT"
    TYPE_ORDER_DEFECT = "TYPE_ORDER_DEFECT"
    PROVENANCE_PROPAGATION = "PROVENANCE_PROPAGATION"
    STRUCTURAL_PROPAGATION = "STRUCTURAL_PROPAGATION"


@dataclass(frozen=True)
class OrderedPathCertificate:
    route: str
    move_order: Tuple[str, ...]
    final_state: KinematicState
    transitions: Tuple[KinematicTransition, ...]
    first_blocked_move: Optional[str]
    exportable: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "route": self.route,
            "move_order": list(self.move_order),
            "final_state": self.final_state.value,
            "transitions": [t.to_dict() for t in self.transitions],
            "first_blocked_move": self.first_blocked_move,
            "exportable": self.exportable,
        }


@dataclass(frozen=True)
class OrderDefectCertificate:
    route: str
    status: OrderDefectStatus
    defect: OrderDefectKind
    canonical: OrderedPathCertificate
    proposed: OrderedPathCertificate
    first_defect_move: Optional[str]
    normal_form_order: Tuple[str, ...]
    summary: str
    boundary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "route": self.route,
            "status": self.status.value,
            "defect": self.defect.value,
            "canonical": self.canonical.to_dict(),
            "proposed": self.proposed.to_dict(),
            "first_defect_move": self.first_defect_move,
            "normal_form_order": list(self.normal_form_order),
            "summary": self.summary,
            "boundary": self.boundary,
        }


def canonical_move_order(route: str) -> Tuple[str, ...]:
    return tuple(row[0] for row in route_path(route if route in {"ew", "dark", "gauge", "horizon", "capacity", "generic"} else "generic"))


def _path_by_move(route: str) -> Dict[str, Tuple[str, KinematicState, KinematicState, Optional[str]]]:
    return {row[0]: row for row in route_path(route if route in {"ew", "dark", "gauge", "horizon", "capacity", "generic"} else "generic")}


def evaluate_ordered_path(route: str, payload: Mapping[str, Any], move_order: Iterable[str]) -> OrderedPathCertificate:
    route = route if route in {"ew", "dark", "gauge", "horizon", "capacity", "generic"} else "generic"
    moves = tuple(move_order)
    by_move = _path_by_move(route)
    current = KinematicState.UNSEEN
    transitions: List[KinematicTransition] = []
    first_blocked: Optional[str] = None

    for move in moves:
        if move not in by_move:
            tr = KinematicTransition(move, current, current, None, TransitionStatus.FORBIDDEN, "unknown move for route")
            transitions.append(tr)
            first_blocked = first_blocked or move
            break

        _, from_state, to_state, field = by_move[move]
        if current != from_state:
            tr = KinematicTransition(move, from_state, to_state, field, TransitionStatus.FORBIDDEN, f"prerequisite state violation: current={current.value}, expected={from_state.value}")
            transitions.append(tr)
            first_blocked = first_blocked or move
            break

        if route == "capacity" and move == "export_capacity_state" and _capacity_overspend(payload):
            tr = KinematicTransition(move, from_state, to_state, field, TransitionStatus.BLOCKED, "capacity overspend remains after coarse graining")
            transitions.append(tr)
            first_blocked = first_blocked or move
            break

        if _truthy(payload, field):
            transitions.append(KinematicTransition(move, from_state, to_state, field, TransitionStatus.ALLOWED, "required field satisfied" if field else "no additional field required"))
            current = to_state
        else:
            transitions.append(KinematicTransition(move, from_state, to_state, field, TransitionStatus.BLOCKED, f"missing or false required field: {field}"))
            first_blocked = first_blocked or move
            break

    # Any canonical moves omitted by proposed order are not reached; order may still be partial.
    exportable = current == KinematicState.GLOBAL_EXPORTABLE and first_blocked is None and set(moves) == set(canonical_move_order(route))
    return OrderedPathCertificate(route, moves, current, tuple(transitions), first_blocked, exportable)


def classify_order_defect(route: str, payload: Mapping[str, Any], proposed_order: Iterable[str]) -> OrderDefectCertificate:
    route = route if route in {"ew", "dark", "gauge", "horizon", "capacity", "generic"} else "generic"
    boundary = "Order-defect kinematics detects path dependence only; it does not repair evidence or promote held route claims."

    canonical_order = canonical_move_order(route)
    canonical = evaluate_ordered_path(route, payload, canonical_order)
    proposed = evaluate_ordered_path(route, payload, proposed_order)

    if provenance_fail_closed(payload):
        return OrderDefectCertificate(route, OrderDefectStatus.FAIL_CLOSED_PROVENANCE, OrderDefectKind.PROVENANCE_PROPAGATION, canonical, proposed, "reject_provenance", canonical_order, "Order test fail-closes because payload carries provenance failure.", boundary)

    if structural_blocked(route, payload):
        return OrderDefectCertificate(route, OrderDefectStatus.STRUCTURAL_BLOCK, OrderDefectKind.STRUCTURAL_PROPAGATION, canonical, proposed, "escalate_structural", canonical_order, "Order test structurally blocked by theorem/substrate requirement.", boundary)

    if tuple(proposed_order) == canonical_order:
        return OrderDefectCertificate(route, OrderDefectStatus.ORDER_ADMISSIBLE, OrderDefectKind.NONE, canonical, proposed, None, canonical_order, "Proposed order is canonical normal form.", boundary)

    if proposed.first_blocked_move:
        # Diagnose type/prereq order defects from transition reason.
        reason = next((t.reason for t in proposed.transitions if t.move == proposed.first_blocked_move), "")
        if "prerequisite" in reason:
            kind = OrderDefectKind.PREREQUISITE_VIOLATION
        elif "capacity" in reason:
            kind = OrderDefectKind.CAPACITY_ORDER_DEFECT
        else:
            kind = OrderDefectKind.TYPE_ORDER_DEFECT
        return OrderDefectCertificate(route, OrderDefectStatus.ORDER_FORBIDDEN, kind, canonical, proposed, proposed.first_blocked_move, canonical_order, f"Proposed order is forbidden at {proposed.first_blocked_move}: {reason}", boundary)

    if proposed.final_state != canonical.final_state:
        return OrderDefectCertificate(route, OrderDefectStatus.ORDER_DEPENDENT, OrderDefectKind.DIFFERENT_FINAL_STATE, canonical, proposed, None, canonical_order, f"Proposed order reaches {proposed.final_state.value}; canonical reaches {canonical.final_state.value}.", boundary)

    if proposed.first_blocked_move != canonical.first_blocked_move:
        return OrderDefectCertificate(route, OrderDefectStatus.ORDER_DEPENDENT, OrderDefectKind.DIFFERENT_BLOCKER, canonical, proposed, proposed.first_blocked_move, canonical_order, "Proposed order changes first blocked move.", boundary)

    # Same endpoint/blocker but noncanonical order: admissible only if it included all moves and exported.
    if proposed.exportable and canonical.exportable:
        return OrderDefectCertificate(route, OrderDefectStatus.ORDER_ADMISSIBLE, OrderDefectKind.NONE, canonical, proposed, None, canonical_order, "Proposed order reaches same export state.", boundary)

    return OrderDefectCertificate(route, OrderDefectStatus.ORDER_DEPENDENT, OrderDefectKind.DIFFERENT_FINAL_STATE, canonical, proposed, None, canonical_order, "Proposed order is noncanonical and does not prove order invariance.", boundary)


def adjacent_commutation_table(route: str, payload: Mapping[str, Any]) -> Tuple[Mapping[str, Any], ...]:
    order = list(canonical_move_order(route))
    rows: List[Mapping[str, Any]] = []
    canonical = evaluate_ordered_path(route, payload, order)
    for i in range(len(order) - 1):
        swapped = list(order)
        swapped[i], swapped[i+1] = swapped[i+1], swapped[i]
        cert = classify_order_defect(route, payload, swapped)
        rows.append({
            "swap": [order[i], order[i+1]],
            "status": cert.status.value,
            "defect": cert.defect.value,
            "first_defect_move": cert.first_defect_move,
            "commutes": cert.status == OrderDefectStatus.ORDER_ADMISSIBLE and cert.proposed.final_state == canonical.final_state,
        })
    return tuple(rows)


def check_T_order_defects_canonical_P() -> Dict[str, Any]:
    payload = {
        "route_built": True, "run_completed": True, "chains_converged": True, "posterior_closed": True,
        "robustness_checks_passed": True, "codomain_transport_found": True, "evaluator_map_found": True,
        "data_ledger_clean": True, "target_value_consumed": False,
    }
    cert = classify_order_defect("dark", payload, canonical_move_order("dark"))
    tests = {
        "admissible": cert.status == OrderDefectStatus.ORDER_ADMISSIBLE,
        "no_defect": cert.defect == OrderDefectKind.NONE,
        "canonical_exportable": cert.canonical.exportable is True,
    }
    return {"name": "check_T_order_defects_canonical_P", "consistent": all(tests.values()), "status": "P_order_defects" if all(tests.values()) else "FAIL", "summary": "Canonical route order is admissible when transition fields are satisfied.", "data": {"tests": tests, "certificate": cert.to_dict()}}


def check_T_order_defects_prerequisite_violation_P() -> Dict[str, Any]:
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
    proposed = list(canonical_move_order("ew"))
    # Try evaluator before transport/codomain.
    i = proposed.index("instantiate_evaluator")
    proposed.pop(i)
    proposed.insert(1, "instantiate_evaluator")
    cert = classify_order_defect("ew", payload, proposed)
    tests = {
        "forbidden": cert.status == OrderDefectStatus.ORDER_FORBIDDEN,
        "prereq": cert.defect == OrderDefectKind.PREREQUISITE_VIOLATION,
        "blocked_evaluator": cert.first_defect_move == "instantiate_evaluator",
    }
    return {"name": "check_T_order_defects_prerequisite_violation_P", "consistent": all(tests.values()), "status": "P_order_defects" if all(tests.values()) else "FAIL", "summary": "Order defects catch evaluator-before-transport prerequisite violation.", "data": {"tests": tests, "certificate": cert.to_dict()}, "dependencies": ["check_T_order_defects_canonical_P"]}


def check_T_order_defects_adjacent_table_P() -> Dict[str, Any]:
    payload = {
        "local_fiber_action_defined": True,
        "group_law_verified": True,
        "representation_faithful": True,
        "codomain_map_declared": True,
        "overlap_cocycle_verified": True,
        "anomaly_check_passed": True,
        "target_value_consumed": False,
    }
    table = adjacent_commutation_table("gauge", payload)
    tests = {
        "rows_present": len(table) == len(canonical_move_order("gauge")) - 1,
        "has_forbidden": any(row["status"] == "ORDER_FORBIDDEN" for row in table),
        "has_prereq": any(row["defect"] == "PREREQUISITE_VIOLATION" for row in table),
    }
    return {"name": "check_T_order_defects_adjacent_table_P", "consistent": all(tests.values()), "status": "P_order_defects" if all(tests.values()) else "FAIL", "summary": "Order-defect engine emits adjacent commutation diagnostics.", "data": {"tests": tests, "table": table}, "dependencies": ["check_T_order_defects_prerequisite_violation_P"]}


def check_T_order_defects_provenance_boundary_P() -> Dict[str, Any]:
    payload = {"target_value_consumed": True, "trace_sector_closed": True}
    cert = classify_order_defect("ew", payload, reversed(canonical_move_order("ew")))
    tests = {
        "fail_closed": cert.status == OrderDefectStatus.FAIL_CLOSED_PROVENANCE,
        "provenance_kind": cert.defect == OrderDefectKind.PROVENANCE_PROPAGATION,
        "boundary": "does not repair" in cert.boundary,
    }
    return {"name": "check_T_order_defects_provenance_boundary_P", "consistent": all(tests.values()), "status": "P_order_defects" if all(tests.values()) else "FAIL", "summary": "Order-defect engine preserves provenance fail-closed priority.", "data": {"tests": tests, "certificate": cert.to_dict()}, "dependencies": ["check_T_order_defects_adjacent_table_P"]}


def check_T_interface_kinematics_order_defects_P() -> Dict[str, Any]:
    subchecks = [
        check_T_order_defects_canonical_P(),
        check_T_order_defects_prerequisite_violation_P(),
        check_T_order_defects_adjacent_table_P(),
        check_T_order_defects_provenance_boundary_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {"name": "check_T_interface_kinematics_order_defects_P", "consistent": ok, "status": "P_order_defects" if ok else "FAIL", "summary": "Interface Kinematics Order Defects is P: transition orders are checked for prerequisite, path-dependence, commutation, and provenance-priority defects.", "data": {"core_claim": "Interface moves are typed and capacity-bearing; reordering them is not free.", "subchecks": [x["name"] for x in subchecks]}, "dependencies": [x["name"] for x in subchecks]}


CHECKS = {
    "check_T_order_defects_canonical_P": check_T_order_defects_canonical_P,
    "check_T_order_defects_prerequisite_violation_P": check_T_order_defects_prerequisite_violation_P,
    "check_T_order_defects_adjacent_table_P": check_T_order_defects_adjacent_table_P,
    "check_T_order_defects_provenance_boundary_P": check_T_order_defects_provenance_boundary_P,
    "check_T_interface_kinematics_order_defects_P": check_T_interface_kinematics_order_defects_P,
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
            raise TypeError("Unsupported registry type for interface_kinematics_order_defects.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
