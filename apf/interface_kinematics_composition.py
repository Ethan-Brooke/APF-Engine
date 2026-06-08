"""
APF Interface Kinematics Composition.

Purpose
-------
Test whether multiple interface kinematic paths compose:

    route payloads
      -> individual kinematic certificates
      -> shared-interface load
      -> conflicting required moves
      -> provenance/structural fail-closed propagation
      -> composition certificate

Core principle
--------------
Individual admissibility does not imply admissible composition under finite interface capacity.

Boundary
--------
Composition kinematics detects non-closure and shared-capacity defects. It does not repair
them or promote held physics claims.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List, Set
import json

from apf.interface_kinematics_engine import (
    compute_kinematic_certificate,
    KinematicCertificate,
    KinematicState,
    TransitionStatus,
)


class CompositionStatus(str, Enum):
    COMPOSES = "COMPOSES"
    HELD_NONCLOSURE = "HELD_NONCLOSURE"
    FAIL_CLOSED_PROVENANCE = "FAIL_CLOSED_PROVENANCE"
    STRUCTURAL_BLOCK = "STRUCTURAL_BLOCK"
    CAPACITY_OVERSPEND = "CAPACITY_OVERSPEND"


class CompositionDefect(str, Enum):
    NONE = "NONE"
    INDIVIDUAL_BLOCKED = "INDIVIDUAL_BLOCKED"
    SHARED_FIELD_CONFLICT = "SHARED_FIELD_CONFLICT"
    SHARED_CAPACITY_OVERSPEND = "SHARED_CAPACITY_OVERSPEND"
    PROVENANCE_PROPAGATION = "PROVENANCE_PROPAGATION"
    STRUCTURAL_PROPAGATION = "STRUCTURAL_PROPAGATION"
    ORDER_DEPENDENCE = "ORDER_DEPENDENCE"


@dataclass(frozen=True)
class CompositionInput:
    item_id: str
    route: str
    payload: Mapping[str, Any]
    interface_domain: str = "default"
    capacity_load: float = 1.0
    capacity_budget: float = 10.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item_id": self.item_id,
            "route": self.route,
            "payload": dict(self.payload),
            "interface_domain": self.interface_domain,
            "capacity_load": self.capacity_load,
            "capacity_budget": self.capacity_budget,
        }


@dataclass(frozen=True)
class CompositionCertificate:
    status: CompositionStatus
    defect: CompositionDefect
    inputs: Tuple[CompositionInput, ...]
    individual_certificates: Tuple[Mapping[str, Any], ...]
    shared_required_fields: Tuple[str, ...]
    conflicting_fields: Tuple[str, ...]
    total_capacity_load: float
    capacity_budget: float
    first_blocker: Optional[str]
    composition_order: Tuple[str, ...]
    summary: str
    boundary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status.value,
            "defect": self.defect.value,
            "inputs": [i.to_dict() for i in self.inputs],
            "individual_certificates": [dict(c) for c in self.individual_certificates],
            "shared_required_fields": list(self.shared_required_fields),
            "conflicting_fields": list(self.conflicting_fields),
            "total_capacity_load": self.total_capacity_load,
            "capacity_budget": self.capacity_budget,
            "first_blocker": self.first_blocker,
            "composition_order": list(self.composition_order),
            "summary": self.summary,
            "boundary": self.boundary,
        }


# Fields that consume shared interface resources when unresolved or simultaneously demanded.
SHARED_INTERFACE_FIELDS = {
    "codomain_transport_found",
    "evaluator_map_found",
    "counterterm_finite_parts_declared",
    "uncertainty_protocol_declared",
    "overlap_cocycle_verified",
    "overlap_gluing_verified",
    "capacity_bound_checked",
    "data_ledger_clean",
    "external_constants_ledger_clean",
}


def required_blocked_fields(cert: KinematicCertificate) -> Tuple[str, ...]:
    fields = []
    for tr in cert.path:
        if tr.status == TransitionStatus.BLOCKED and tr.required_field:
            fields.append(tr.required_field)
    return tuple(fields)


def traversed_states(cert: KinematicCertificate) -> Tuple[str, ...]:
    states = []
    for tr in cert.path:
        if tr.status == TransitionStatus.ALLOWED:
            states.append(tr.to_state.value)
        elif tr.status == TransitionStatus.BLOCKED:
            states.append(tr.from_state.value)
            break
    if not states:
        states.append(cert.current_state.value)
    return tuple(states)


def _capacity_budget(inputs: Tuple[CompositionInput, ...]) -> float:
    if not inputs:
        return 0.0
    budgets = [i.capacity_budget for i in inputs if i.capacity_budget is not None]
    return min(budgets) if budgets else 0.0


def _composition_order(inputs: Tuple[CompositionInput, ...]) -> Tuple[str, ...]:
    # Canonical deterministic order: fail-closed first, then most advanced path, then item id.
    scored = []
    for item in inputs:
        cert = compute_kinematic_certificate(item.route, item.payload)
        score = 100 if cert.fail_closed else 90 if cert.structural_block else len([tr for tr in cert.path if tr.status == TransitionStatus.ALLOWED])
        scored.append((-score, item.item_id))
    return tuple(item_id for _, item_id in sorted(scored))


def compose_kinematics(items: Iterable[CompositionInput]) -> CompositionCertificate:
    inputs = tuple(items)
    boundary = "Composition kinematics tests non-closure under finite interface capacity; it does not repair routes or promote held claims."

    certs: List[KinematicCertificate] = [compute_kinematic_certificate(i.route, i.payload) for i in inputs]
    cert_dicts = tuple(c.to_dict() for c in certs)
    order = _composition_order(inputs)

    if any(c.fail_closed for c in certs):
        blocker = next(inputs[idx].item_id for idx, c in enumerate(certs) if c.fail_closed)
        return CompositionCertificate(
            status=CompositionStatus.FAIL_CLOSED_PROVENANCE,
            defect=CompositionDefect.PROVENANCE_PROPAGATION,
            inputs=inputs,
            individual_certificates=cert_dicts,
            shared_required_fields=tuple(),
            conflicting_fields=tuple(),
            total_capacity_load=sum(i.capacity_load for i in inputs),
            capacity_budget=_capacity_budget(inputs),
            first_blocker=blocker,
            composition_order=order,
            summary=f"Composition fail-closes because {blocker} carries provenance failure.",
            boundary=boundary,
        )

    if any(c.structural_block for c in certs):
        blocker = next(inputs[idx].item_id for idx, c in enumerate(certs) if c.structural_block)
        return CompositionCertificate(
            status=CompositionStatus.STRUCTURAL_BLOCK,
            defect=CompositionDefect.STRUCTURAL_PROPAGATION,
            inputs=inputs,
            individual_certificates=cert_dicts,
            shared_required_fields=tuple(),
            conflicting_fields=tuple(),
            total_capacity_load=sum(i.capacity_load for i in inputs),
            capacity_budget=_capacity_budget(inputs),
            first_blocker=blocker,
            composition_order=order,
            summary=f"Composition structurally blocked because {blocker} requires theorem/substrate repair.",
            boundary=boundary,
        )

    total_load = sum(float(i.capacity_load) for i in inputs)
    budget = _capacity_budget(inputs)
    if budget >= 0 and total_load > budget:
        return CompositionCertificate(
            status=CompositionStatus.CAPACITY_OVERSPEND,
            defect=CompositionDefect.SHARED_CAPACITY_OVERSPEND,
            inputs=inputs,
            individual_certificates=cert_dicts,
            shared_required_fields=tuple(),
            conflicting_fields=tuple(),
            total_capacity_load=total_load,
            capacity_budget=budget,
            first_blocker="shared_capacity",
            composition_order=order,
            summary=f"Composition overspends shared interface capacity: load={total_load} > budget={budget}.",
            boundary=boundary,
        )

    blocked_fields: List[str] = []
    for cert in certs:
        blocked_fields.extend(required_blocked_fields(cert))
    shared_required = tuple(sorted({f for f in blocked_fields if f in SHARED_INTERFACE_FIELDS}))

    # Conflict if two or more routes demand the same unresolved shared field in the same domain.
    counts: Dict[Tuple[str, str], int] = {}
    for item, cert in zip(inputs, certs):
        for field in required_blocked_fields(cert):
            if field in SHARED_INTERFACE_FIELDS:
                key = (item.interface_domain, field)
                counts[key] = counts.get(key, 0) + 1
    conflicts = tuple(sorted({field for (_, field), count in counts.items() if count > 1}))

    if conflicts:
        return CompositionCertificate(
            status=CompositionStatus.HELD_NONCLOSURE,
            defect=CompositionDefect.SHARED_FIELD_CONFLICT,
            inputs=inputs,
            individual_certificates=cert_dicts,
            shared_required_fields=shared_required,
            conflicting_fields=conflicts,
            total_capacity_load=total_load,
            capacity_budget=budget,
            first_blocker=conflicts[0],
            composition_order=order,
            summary=f"Composition held: multiple paths require unresolved shared interface fields {conflicts}.",
            boundary=boundary,
        )

    # Individual blocked paths compose only as a held bundle, not as export.
    if any(not c.exportable for c in certs):
        blocker = next(inputs[idx].item_id for idx, c in enumerate(certs) if not c.exportable)
        return CompositionCertificate(
            status=CompositionStatus.HELD_NONCLOSURE,
            defect=CompositionDefect.INDIVIDUAL_BLOCKED,
            inputs=inputs,
            individual_certificates=cert_dicts,
            shared_required_fields=shared_required,
            conflicting_fields=tuple(),
            total_capacity_load=total_load,
            capacity_budget=budget,
            first_blocker=blocker,
            composition_order=order,
            summary=f"Composition held because {blocker} has an individually blocked kinematic path.",
            boundary=boundary,
        )

    return CompositionCertificate(
        status=CompositionStatus.COMPOSES,
        defect=CompositionDefect.NONE,
        inputs=inputs,
        individual_certificates=cert_dicts,
        shared_required_fields=tuple(),
        conflicting_fields=tuple(),
        total_capacity_load=total_load,
        capacity_budget=budget,
        first_blocker=None,
        composition_order=order,
        summary="All individual paths export and shared interface capacity is not overspent.",
        boundary=boundary,
    )


def load_composition_inputs(path: str) -> Tuple[CompositionInput, ...]:
    data = json.loads(open(path, "r", encoding="utf-8").read())
    rows = data.get("inputs", data)
    out = []
    for idx, row in enumerate(rows):
        out.append(CompositionInput(
            item_id=str(row.get("item_id", f"item_{idx:03d}")),
            route=str(row.get("route", "generic")),
            payload=row.get("payload", {}),
            interface_domain=str(row.get("interface_domain", "default")),
            capacity_load=float(row.get("capacity_load", 1.0)),
            capacity_budget=float(row.get("capacity_budget", 10.0)),
        ))
    return tuple(out)


def check_T_composition_two_exportable_paths_P() -> Dict[str, Any]:
    dark_payload = {
        "route_built": True, "run_completed": True, "chains_converged": True, "posterior_closed": True,
        "robustness_checks_passed": True, "codomain_transport_found": True, "evaluator_map_found": True,
        "data_ledger_clean": True, "target_value_consumed": False,
    }
    items = (
        CompositionInput("dark1", "dark", dark_payload, capacity_load=1, capacity_budget=5),
        CompositionInput("dark2", "dark", dark_payload, capacity_load=1, capacity_budget=5),
    )
    cert = compose_kinematics(items)
    tests = {
        "composes": cert.status == CompositionStatus.COMPOSES,
        "no_defect": cert.defect == CompositionDefect.NONE,
        "no_blocker": cert.first_blocker is None,
    }
    return {"name": "check_T_composition_two_exportable_paths_P", "consistent": all(tests.values()), "status": "P_composition_kinematics" if all(tests.values()) else "FAIL", "summary": "Composition succeeds for exportable paths within capacity.", "data": {"tests": tests, "certificate": cert.to_dict()}}


def check_T_composition_shared_field_nonclosure_P() -> Dict[str, Any]:
    ew_payload = {
        "trace_sector_closed": True,
        "source_to_scheme_registry_present": True,
        "codomain_transport_found": False,
        "evaluator_map_found": False,
        "counterterm_finite_parts_declared": False,
        "external_constants_ledger_clean": True,
        "uncertainty_protocol_declared": False,
        "target_value_consumed": False,
    }
    items = (
        CompositionInput("ew_a", "ew", ew_payload, interface_domain="EW_IFACE", capacity_load=1, capacity_budget=5),
        CompositionInput("ew_b", "ew", ew_payload, interface_domain="EW_IFACE", capacity_load=1, capacity_budget=5),
    )
    cert = compose_kinematics(items)
    tests = {
        "held": cert.status == CompositionStatus.HELD_NONCLOSURE,
        "shared_conflict": cert.defect == CompositionDefect.SHARED_FIELD_CONFLICT,
        "codomain_conflict": "codomain_transport_found" in cert.conflicting_fields,
    }
    return {"name": "check_T_composition_shared_field_nonclosure_P", "consistent": all(tests.values()), "status": "P_composition_kinematics" if all(tests.values()) else "FAIL", "summary": "Composition detects non-closure from unresolved shared interface fields.", "data": {"tests": tests, "certificate": cert.to_dict()}, "dependencies": ["check_T_composition_two_exportable_paths_P"]}


def check_T_composition_capacity_overspend_P() -> Dict[str, Any]:
    dark_payload = {
        "route_built": True, "run_completed": True, "chains_converged": True, "posterior_closed": True,
        "robustness_checks_passed": True, "codomain_transport_found": True, "evaluator_map_found": True,
        "data_ledger_clean": True, "target_value_consumed": False,
    }
    items = (
        CompositionInput("dark_heavy_a", "dark", dark_payload, capacity_load=4, capacity_budget=6),
        CompositionInput("dark_heavy_b", "dark", dark_payload, capacity_load=4, capacity_budget=6),
    )
    cert = compose_kinematics(items)
    tests = {
        "overspend": cert.status == CompositionStatus.CAPACITY_OVERSPEND,
        "defect": cert.defect == CompositionDefect.SHARED_CAPACITY_OVERSPEND,
        "load_gt_budget": cert.total_capacity_load > cert.capacity_budget,
    }
    return {"name": "check_T_composition_capacity_overspend_P", "consistent": all(tests.values()), "status": "P_composition_kinematics" if all(tests.values()) else "FAIL", "summary": "Composition detects shared capacity overspend even when individual routes export.", "data": {"tests": tests, "certificate": cert.to_dict()}, "dependencies": ["check_T_composition_shared_field_nonclosure_P"]}


def check_T_composition_provenance_propagation_P() -> Dict[str, Any]:
    items = (
        CompositionInput("bad", "ew", {"trace_sector_closed": True, "target_value_consumed": True}),
        CompositionInput("good", "dark", {"route_built": True, "run_completed": True}),
    )
    cert = compose_kinematics(items)
    tests = {
        "fail_closed": cert.status == CompositionStatus.FAIL_CLOSED_PROVENANCE,
        "defect": cert.defect == CompositionDefect.PROVENANCE_PROPAGATION,
        "blocker_bad": cert.first_blocker == "bad",
    }
    return {"name": "check_T_composition_provenance_propagation_P", "consistent": all(tests.values()), "status": "P_composition_kinematics" if all(tests.values()) else "FAIL", "summary": "Composition propagates provenance fail-closed status.", "data": {"tests": tests, "certificate": cert.to_dict()}, "dependencies": ["check_T_composition_capacity_overspend_P"]}


def check_T_interface_kinematics_composition_P() -> Dict[str, Any]:
    subchecks = [
        check_T_composition_two_exportable_paths_P(),
        check_T_composition_shared_field_nonclosure_P(),
        check_T_composition_capacity_overspend_P(),
        check_T_composition_provenance_propagation_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {"name": "check_T_interface_kinematics_composition_P", "consistent": ok, "status": "P_composition_kinematics" if ok else "FAIL", "summary": "Interface Kinematics Composition is P: individual path certificates are checked for non-closure, shared field conflicts, capacity overspend, and fail-closed propagation.", "data": {"core_claim": "Individually admissible interface motions need not compose under finite interface capacity.", "subchecks": [x["name"] for x in subchecks]}, "dependencies": [x["name"] for x in subchecks]}


CHECKS = {
    "check_T_composition_two_exportable_paths_P": check_T_composition_two_exportable_paths_P,
    "check_T_composition_shared_field_nonclosure_P": check_T_composition_shared_field_nonclosure_P,
    "check_T_composition_capacity_overspend_P": check_T_composition_capacity_overspend_P,
    "check_T_composition_provenance_propagation_P": check_T_composition_provenance_propagation_P,
    "check_T_interface_kinematics_composition_P": check_T_interface_kinematics_composition_P,
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
            raise TypeError("Unsupported registry type for interface_kinematics_composition.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
