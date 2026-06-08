"""
APF Interface Evidence Rerun Controller.

v24.3.12+ delta layer.

Purpose
-------
The obligation compiler says what evidence must be supplied before rerun.
This controller closes the engineering loop:

    obligation packet
      -> evidence validation
      -> select satisfied minimal bundle
      -> patch route payload using only that bundle
      -> rerun discovery/certification
      -> compare before/after
      -> report whether the repaired route actually reaches P

Boundary
--------
Evidence completeness is not proof of truth.  It is permission to rerun.  Only the rerun
certificate decides whether the patched route reaches P.

Top check:
    check_T_interface_evidence_rerun_controller_P
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List
import json

try:
    from apf.interface_repair_obligation_compiler import (
        ObligationPacket,
        ObligationPacketStatus,
        EvidenceValidationResult,
        compile_obligation_packet,
        evidence_template,
        validate_evidence,
        canonical_payloads_for_simulation,
    )
    from apf.interface_movement_graph_repair_planner import discover_and_plan_repair
except Exception as exc:  # pragma: no cover
    raise ImportError(f"interface_evidence_rerun_controller requires obligation compiler stack: {exc}") from exc


class RerunControllerStatus(str, Enum):
    ALREADY_P_NO_RERUN = "ALREADY_P_NO_RERUN"
    EVIDENCE_INCOMPLETE_NOT_RERUN = "EVIDENCE_INCOMPLETE_NOT_RERUN"
    BLOCKED_PROVENANCE_NOT_RERUN = "BLOCKED_PROVENANCE_NOT_RERUN"
    BLOCKED_SUBSTRATE_NOT_RERUN = "BLOCKED_SUBSTRATE_NOT_RERUN"
    NO_CLOSING_FRONTIER_NOT_RERUN = "NO_CLOSING_FRONTIER_NOT_RERUN"
    RERUN_REACHES_P = "RERUN_REACHES_P"
    RERUN_STILL_BLOCKED = "RERUN_STILL_BLOCKED"


@dataclass(frozen=True)
class RerunPatch:
    field: str
    old_value: Any
    new_value: Any
    obligation_id: str
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RerunControllerResult:
    route: str
    status: RerunControllerStatus
    selected_bundle_id: Optional[str]
    original_payload: Mapping[str, Any]
    patched_payload: Optional[Mapping[str, Any]]
    patches: Tuple[RerunPatch, ...]
    evidence_validation: Mapping[str, Any]
    original_certificate: Mapping[str, Any]
    rerun_certificate: Optional[Mapping[str, Any]]
    before_after_summary: Mapping[str, Any]
    note: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "route": self.route,
            "status": self.status.value,
            "selected_bundle_id": self.selected_bundle_id,
            "original_payload": dict(self.original_payload),
            "patched_payload": dict(self.patched_payload) if self.patched_payload is not None else None,
            "patches": [p.to_dict() for p in self.patches],
            "evidence_validation": dict(self.evidence_validation),
            "original_certificate": dict(self.original_certificate),
            "rerun_certificate": dict(self.rerun_certificate) if self.rerun_certificate is not None else None,
            "before_after_summary": dict(self.before_after_summary),
            "note": self.note,
        }


def _certificate_for(route: str, payload: Mapping[str, Any]) -> Mapping[str, Any]:
    return discover_and_plan_repair(route, payload)["graph"]["certificate"]


def _summary(original: Mapping[str, Any], rerun: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    if rerun is None:
        return {
            "original_status": original.get("solver_status"),
            "rerun_status": None,
            "original_export_global_P": original.get("export_global_P"),
            "rerun_export_global_P": None,
            "original_obstruction": original.get("obstruction"),
            "rerun_obstruction": None,
            "closed": False,
        }
    return {
        "original_status": original.get("solver_status"),
        "rerun_status": rerun.get("solver_status"),
        "original_export_global_P": original.get("export_global_P"),
        "rerun_export_global_P": rerun.get("export_global_P"),
        "original_obstruction": original.get("obstruction"),
        "rerun_obstruction": rerun.get("obstruction"),
        "closed": bool(rerun.get("export_global_P")),
    }


def _packet_status_to_controller_status(packet_status: ObligationPacketStatus) -> RerunControllerStatus:
    if packet_status == ObligationPacketStatus.NOT_REQUIRED_ALREADY_P:
        return RerunControllerStatus.ALREADY_P_NO_RERUN
    if packet_status == ObligationPacketStatus.BLOCKED_PROVENANCE_REBUILD_REQUIRED:
        return RerunControllerStatus.BLOCKED_PROVENANCE_NOT_RERUN
    if packet_status == ObligationPacketStatus.BLOCKED_SUBSTRATE_THEOREM_REQUIRED:
        return RerunControllerStatus.BLOCKED_SUBSTRATE_NOT_RERUN
    if packet_status == ObligationPacketStatus.NO_CLOSING_FRONTIER:
        return RerunControllerStatus.NO_CLOSING_FRONTIER_NOT_RERUN
    return RerunControllerStatus.EVIDENCE_INCOMPLETE_NOT_RERUN


def _select_satisfied_bundle(packet: ObligationPacket, validation: EvidenceValidationResult) -> Optional[str]:
    if validation.satisfied_bundle_ids:
        return validation.satisfied_bundle_ids[0]
    return None


def _patches_for_bundle(packet: ObligationPacket, bundle_id: str, payload: Mapping[str, Any]) -> Tuple[RerunPatch, ...]:
    patches: List[RerunPatch] = []
    for bundle in packet.bundles:
        if bundle.bundle_id != bundle_id:
            continue
        for obligation in bundle.obligations:
            patches.append(
                RerunPatch(
                    field=obligation.field,
                    old_value=payload.get(obligation.field),
                    new_value=obligation.required_value,
                    obligation_id=obligation.obligation_id,
                    reason=obligation.reason,
                )
            )
    return tuple(patches)


def apply_rerun_patches(payload: Mapping[str, Any], patches: Iterable[RerunPatch]) -> Dict[str, Any]:
    patched = dict(payload)
    for patch in patches:
        patched[patch.field] = patch.new_value
    return patched


def control_evidence_rerun(route: str, payload: Mapping[str, Any], evidence_payload: Optional[Mapping[str, Any]] = None) -> RerunControllerResult:
    """Validate evidence, apply one satisfied minimal bundle, and rerun certification."""
    packet = compile_obligation_packet(route, payload)
    original_cert = dict(packet.original_certificate)

    if packet.packet_status == ObligationPacketStatus.NOT_REQUIRED_ALREADY_P:
        return RerunControllerResult(
            route=route,
            status=RerunControllerStatus.ALREADY_P_NO_RERUN,
            selected_bundle_id=None,
            original_payload=dict(payload),
            patched_payload=None,
            patches=tuple(),
            evidence_validation={
                "packet_status": packet.packet_status.value,
                "ready_to_rerun": True,
                "note": "Already P; no evidence or rerun required.",
            },
            original_certificate=original_cert,
            rerun_certificate=None,
            before_after_summary=_summary(original_cert, None),
            note="Already global P; controller did not rerun.",
        )

    if packet.packet_status in {
        ObligationPacketStatus.BLOCKED_PROVENANCE_REBUILD_REQUIRED,
        ObligationPacketStatus.BLOCKED_SUBSTRATE_THEOREM_REQUIRED,
        ObligationPacketStatus.NO_CLOSING_FRONTIER,
    }:
        return RerunControllerResult(
            route=route,
            status=_packet_status_to_controller_status(packet.packet_status),
            selected_bundle_id=None,
            original_payload=dict(payload),
            patched_payload=None,
            patches=tuple(),
            evidence_validation={
                "packet_status": packet.packet_status.value,
                "ready_to_rerun": False,
                "note": packet.blocked_reason or "Blocked packet cannot be rerun by evidence patch.",
            },
            original_certificate=original_cert,
            rerun_certificate=None,
            before_after_summary=_summary(original_cert, None),
            note="Blocked before evidence rerun; no payload patch applied.",
        )

    if evidence_payload is None:
        evidence_payload = evidence_template(packet)

    validation = validate_evidence(packet, evidence_payload)
    if not validation.ready_to_rerun:
        return RerunControllerResult(
            route=route,
            status=RerunControllerStatus.EVIDENCE_INCOMPLETE_NOT_RERUN,
            selected_bundle_id=None,
            original_payload=dict(payload),
            patched_payload=None,
            patches=tuple(),
            evidence_validation=validation.to_dict(),
            original_certificate=original_cert,
            rerun_certificate=None,
            before_after_summary=_summary(original_cert, None),
            note="Evidence incomplete; controller refused to patch/rerun.",
        )

    bundle_id = _select_satisfied_bundle(packet, validation)
    if bundle_id is None:
        return RerunControllerResult(
            route=route,
            status=RerunControllerStatus.EVIDENCE_INCOMPLETE_NOT_RERUN,
            selected_bundle_id=None,
            original_payload=dict(payload),
            patched_payload=None,
            patches=tuple(),
            evidence_validation=validation.to_dict(),
            original_certificate=original_cert,
            rerun_certificate=None,
            before_after_summary=_summary(original_cert, None),
            note="No satisfied minimal bundle found; controller refused to patch/rerun.",
        )

    patches = _patches_for_bundle(packet, bundle_id, payload)
    patched_payload = apply_rerun_patches(payload, patches)
    rerun_cert = dict(_certificate_for(route, patched_payload))
    status = RerunControllerStatus.RERUN_REACHES_P if rerun_cert.get("export_global_P") else RerunControllerStatus.RERUN_STILL_BLOCKED

    note = (
        "Evidence was complete for a minimal bundle; patched payload reran and reached global P."
        if status == RerunControllerStatus.RERUN_REACHES_P
        else "Evidence was complete for a minimal bundle, but rerun remains blocked; inspect rerun obstruction."
    )

    return RerunControllerResult(
        route=route,
        status=status,
        selected_bundle_id=bundle_id,
        original_payload=dict(payload),
        patched_payload=patched_payload,
        patches=patches,
        evidence_validation=validation.to_dict(),
        original_certificate=original_cert,
        rerun_certificate=rerun_cert,
        before_after_summary=_summary(original_cert, rerun_cert),
        note=note,
    )


def filled_evidence_for_first_bundle(route: str, payload: Mapping[str, Any]) -> Dict[str, Any]:
    packet = compile_obligation_packet(route, payload)
    template = evidence_template(packet)
    if not packet.bundles:
        return template
    bundle = packet.bundles[0]
    for obligation in bundle.obligations:
        for slot in obligation.evidence_slots:
            template["evidence"][bundle.bundle_id][obligation.obligation_id][slot.key] = f"evidence_for_{slot.key}"
    return template


def canonical_payloads_for_rerun() -> Dict[str, Tuple[str, Mapping[str, Any]]]:
    return canonical_payloads_for_simulation()


def run_canonical_reruns() -> Dict[str, Dict[str, Any]]:
    out = {}
    for name, (route, payload) in canonical_payloads_for_rerun().items():
        evidence = filled_evidence_for_first_bundle(route, payload)
        out[name] = control_evidence_rerun(route, payload, evidence).to_dict()
    return out


def check_T_evidence_complete_triggers_rerun_P() -> Dict[str, Any]:
    payloads = canonical_payloads_for_rerun()
    ordinary = ["ew_open", "dark_open", "gauge_open", "horizon_open", "capacity_open"]
    results = {}
    for name in ordinary:
        route, payload = payloads[name]
        evidence = filled_evidence_for_first_bundle(route, payload)
        results[name] = control_evidence_rerun(route, payload, evidence).to_dict()

    tests = {
        f"{name}_reaches_P": results[name]["status"] == "RERUN_REACHES_P"
        and results[name]["rerun_certificate"]["export_global_P"] is True
        for name in ordinary
    }
    tests["all_have_patches"] = all(len(results[name]["patches"]) > 0 for name in ordinary)
    tests["all_before_was_not_P"] = all(results[name]["original_certificate"]["export_global_P"] is False for name in ordinary)
    return {
        "name": "check_T_evidence_complete_triggers_rerun_P",
        "consistent": all(tests.values()),
        "status": "P_rerun",
        "summary": "Complete evidence for ordinary minimal bundles triggers payload patching and rerun to global P.",
        "data": {"tests": tests, "statuses": {k: v["status"] for k, v in results.items()}},
    }


def check_T_incomplete_evidence_blocks_rerun_P() -> Dict[str, Any]:
    route, payload = canonical_payloads_for_rerun()["ew_open"]
    # No explicit evidence => template with TODO values, so validation should fail.
    result = control_evidence_rerun(route, payload).to_dict()
    tests = {
        "status_incomplete": result["status"] == "EVIDENCE_INCOMPLETE_NOT_RERUN",
        "no_patched_payload": result["patched_payload"] is None,
        "no_rerun_certificate": result["rerun_certificate"] is None,
        "original_not_P": result["original_certificate"]["export_global_P"] is False,
    }
    return {
        "name": "check_T_incomplete_evidence_blocks_rerun_P",
        "consistent": all(tests.values()),
        "status": "P_rerun",
        "summary": "Incomplete evidence does not patch payload and does not rerun certification.",
        "data": {"tests": tests, "result": result},
        "dependencies": ["check_T_evidence_complete_triggers_rerun_P"],
    }


def check_T_blocked_cases_refuse_rerun_P() -> Dict[str, Any]:
    payloads = canonical_payloads_for_rerun()
    prov_route, prov_payload = payloads["provenance_smuggled"]
    cstar_route, cstar_payload = payloads["cstar"]
    prov = control_evidence_rerun(prov_route, prov_payload).to_dict()
    cstar = control_evidence_rerun(cstar_route, cstar_payload).to_dict()
    tests = {
        "provenance_refused": prov["status"] == "BLOCKED_PROVENANCE_NOT_RERUN",
        "cstar_refused": cstar["status"] == "BLOCKED_SUBSTRATE_NOT_RERUN",
        "provenance_no_patch": prov["patched_payload"] is None,
        "cstar_no_patch": cstar["patched_payload"] is None,
    }
    return {
        "name": "check_T_blocked_cases_refuse_rerun_P",
        "consistent": all(tests.values()),
        "status": "P_rerun",
        "summary": "Provenance and substrate-blocked cases refuse evidence patch/rerun.",
        "data": {"tests": tests, "statuses": {"provenance": prov["status"], "cstar": cstar["status"]}},
        "dependencies": ["check_T_incomplete_evidence_blocks_rerun_P"],
    }


def check_T_already_P_no_rerun_P() -> Dict[str, Any]:
    route, payload = canonical_payloads_for_rerun()["ew_closed"]
    result = control_evidence_rerun(route, payload).to_dict()
    tests = {
        "status_already_P": result["status"] == "ALREADY_P_NO_RERUN",
        "no_patch": result["patched_payload"] is None,
        "original_global_P": result["original_certificate"]["export_global_P"] is True,
        "no_rerun_cert": result["rerun_certificate"] is None,
    }
    return {
        "name": "check_T_already_P_no_rerun_P",
        "consistent": all(tests.values()),
        "status": "P_rerun",
        "summary": "Already-P cases do not generate unnecessary patches or reruns.",
        "data": {"tests": tests},
        "dependencies": ["check_T_blocked_cases_refuse_rerun_P"],
    }


def check_T_evidence_rerun_controller_boundary_P() -> Dict[str, Any]:
    route, payload = canonical_payloads_for_rerun()["ew_open"]
    evidence = filled_evidence_for_first_bundle(route, payload)
    result = control_evidence_rerun(route, payload, evidence).to_dict()
    tests = {
        "before_after_summary_present": "before_after_summary" in result,
        "original_not_exported": result["before_after_summary"]["original_export_global_P"] is False,
        "rerun_exported": result["before_after_summary"]["rerun_export_global_P"] is True,
        "note_mentions_reran": "reran" in result["note"].lower(),
    }
    return {
        "name": "check_T_evidence_rerun_controller_boundary_P",
        "consistent": all(tests.values()),
        "status": "P_audit",
        "summary": "Controller distinguishes evidence readiness from rerun certification and reports before/after status.",
        "data": {"tests": tests, "before_after_summary": result["before_after_summary"]},
        "dependencies": ["check_T_already_P_no_rerun_P"],
    }


def check_T_interface_evidence_rerun_controller_P() -> Dict[str, Any]:
    subchecks = [
        check_T_evidence_complete_triggers_rerun_P(),
        check_T_incomplete_evidence_blocks_rerun_P(),
        check_T_blocked_cases_refuse_rerun_P(),
        check_T_already_P_no_rerun_P(),
        check_T_evidence_rerun_controller_boundary_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_interface_evidence_rerun_controller_P",
        "consistent": ok,
        "status": "P_evidence_rerun" if ok else "FAIL",
        "summary": "Interface Evidence Rerun Controller is P: complete evidence patches one minimal bundle and reruns certification, while incomplete/blocked cases do not rerun.",
        "data": {
            "core_claim": "Evidence completion authorizes rerun; only rerun certification decides whether the repaired payload reaches P.",
            "subchecks": [x["name"] for x in subchecks],
            "controller_statuses": [x.value for x in RerunControllerStatus],
        },
        "dependencies": [x["name"] for x in subchecks],
    }


CHECKS = {
    "check_T_evidence_complete_triggers_rerun_P": check_T_evidence_complete_triggers_rerun_P,
    "check_T_incomplete_evidence_blocks_rerun_P": check_T_incomplete_evidence_blocks_rerun_P,
    "check_T_blocked_cases_refuse_rerun_P": check_T_blocked_cases_refuse_rerun_P,
    "check_T_already_P_no_rerun_P": check_T_already_P_no_rerun_P,
    "check_T_evidence_rerun_controller_boundary_P": check_T_evidence_rerun_controller_boundary_P,
    "check_T_interface_evidence_rerun_controller_P": check_T_interface_evidence_rerun_controller_P,
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
            raise TypeError("Unsupported registry type for interface_evidence_rerun_controller.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
