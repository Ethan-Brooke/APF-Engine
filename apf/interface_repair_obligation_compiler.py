"""
APF Interface Repair Obligation Compiler.

v24.3.12+ delta layer.

Purpose
-------
The repair frontier explorer identifies minimal counterfactual repair bundles.
This module compiles those bundles into concrete evidence obligations:

    repair frontier
      -> minimal repair bundle(s)
      -> evidence slots
      -> acceptance criteria
      -> evidence template
      -> ready-to-rerun predicate

Boundary
--------
This module does not assert the evidence is true. It defines what evidence must be supplied
before rerunning the certification gate.

Top check:
    check_T_interface_repair_obligation_compiler_P
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List, Set

try:
    from apf.interface_repair_frontier_explorer import (
        RepairFrontier,
        RepairBundle,
        FrontierStatus,
        explore_repair_frontier,
        canonical_frontiers,
        canonical_payloads_for_simulation,
    )
except Exception as exc:  # pragma: no cover
    raise ImportError(f"interface_repair_obligation_compiler requires frontier explorer stack: {exc}") from exc


class ObligationPacketStatus(str, Enum):
    NOT_REQUIRED_ALREADY_P = "NOT_REQUIRED_ALREADY_P"
    OPEN_EVIDENCE_REQUIRED = "OPEN_EVIDENCE_REQUIRED"
    READY_TO_RERUN = "READY_TO_RERUN"
    BLOCKED_PROVENANCE_REBUILD_REQUIRED = "BLOCKED_PROVENANCE_REBUILD_REQUIRED"
    BLOCKED_SUBSTRATE_THEOREM_REQUIRED = "BLOCKED_SUBSTRATE_THEOREM_REQUIRED"
    NO_CLOSING_FRONTIER = "NO_CLOSING_FRONTIER"


@dataclass(frozen=True)
class EvidenceSlot:
    slot_id: str
    key: str
    description: str
    required: bool
    acceptance_criteria: str
    example_value: Any = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepairObligation:
    obligation_id: str
    bundle_id: str
    field: str
    old_value: Any
    required_value: Any
    reason: str
    evidence_slots: Tuple[EvidenceSlot, ...]
    rerun_hint: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "obligation_id": self.obligation_id,
            "bundle_id": self.bundle_id,
            "field": self.field,
            "old_value": self.old_value,
            "required_value": self.required_value,
            "reason": self.reason,
            "evidence_slots": [slot.to_dict() for slot in self.evidence_slots],
            "rerun_hint": self.rerun_hint,
        }


@dataclass(frozen=True)
class ObligationBundle:
    bundle_id: str
    fields: Tuple[str, ...]
    obligations: Tuple[RepairObligation, ...]
    minimal: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bundle_id": self.bundle_id,
            "fields": self.fields,
            "minimal": self.minimal,
            "obligations": [obl.to_dict() for obl in self.obligations],
        }


@dataclass(frozen=True)
class ObligationPacket:
    route: str
    packet_status: ObligationPacketStatus
    frontier_status: FrontierStatus
    original_repair_class: str
    bundles: Tuple[ObligationBundle, ...]
    critical_fields: Tuple[str, ...]
    optional_fields: Tuple[str, ...]
    blocked_reason: Optional[str]
    ready_to_rerun: bool
    rerun_command_hint: str
    original_certificate: Mapping[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "route": self.route,
            "packet_status": self.packet_status.value,
            "frontier_status": self.frontier_status.value,
            "original_repair_class": self.original_repair_class,
            "bundles": [bundle.to_dict() for bundle in self.bundles],
            "critical_fields": self.critical_fields,
            "optional_fields": self.optional_fields,
            "blocked_reason": self.blocked_reason,
            "ready_to_rerun": self.ready_to_rerun,
            "rerun_command_hint": self.rerun_command_hint,
            "original_certificate": dict(self.original_certificate),
        }


@dataclass(frozen=True)
class EvidenceValidationResult:
    packet_status: ObligationPacketStatus
    ready_to_rerun: bool
    satisfied_bundle_ids: Tuple[str, ...]
    missing_slots: Tuple[str, ...]
    supplied_slots: Tuple[str, ...]
    rerun_command_hint: str
    note: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _slot(slot_id: str, key: str, description: str, criteria: str, example: Any = "TODO") -> EvidenceSlot:
    return EvidenceSlot(
        slot_id=slot_id,
        key=key,
        description=description,
        required=True,
        acceptance_criteria=criteria,
        example_value=example,
    )


def evidence_slots_for_field(field: str, bundle_id: str) -> Tuple[EvidenceSlot, ...]:
    """Compile field-level repair facts into evidence slots."""
    prefix = f"{bundle_id}:{field}"

    if field in {"source_to_scheme_registry_present"}:
        return (
            _slot(prefix+":source_scheme", "source_scheme", "Name the source scheme/domain.", "Must name the APF source domain, e.g. APF_TRACE."),
            _slot(prefix+":target_scheme", "target_scheme", "Name the target physical scheme.", "Must name the target scheme and scale/convention."),
            _slot(prefix+":registry_entry", "registry_entry", "Provide registry entry or theorem ID.", "Must identify a banked source-to-scheme registry entry."),
        )

    if field in {"evaluator_map_found"}:
        return (
            _slot(prefix+":evaluator_definition", "evaluator_definition", "Define the evaluator map.", "Must specify domain, codomain, inputs, outputs, and invariants."),
            _slot(prefix+":evaluator_verifier", "evaluator_verifier", "Verifier/check that evaluates the map.", "Must provide script/check name or theorem certificate."),
        )

    if field in {"codomain_transport_found", "codomain_map_declared"}:
        return (
            _slot(prefix+":source_codomain", "source_codomain", "Source codomain.", "Must name the source codomain."),
            _slot(prefix+":target_codomain", "target_codomain", "Target codomain.", "Must name the target codomain."),
            _slot(prefix+":transport_map", "transport_map", "Transport map.", "Must identify an explicit transport map or theorem."),
            _slot(prefix+":preserved_invariants", "preserved_invariants", "Invariants preserved by transport.", "Must list invariants and how they are checked."),
        )

    if field in {"counterterm_finite_parts_declared"}:
        return (
            _slot(prefix+":counterterm_scheme", "counterterm_scheme", "Counterterm/finite-part scheme.", "Must define finite part convention and dependency ledger."),
            _slot(prefix+":counterterm_verifier", "counterterm_verifier", "Counterterm verifier.", "Must provide verifier or theorem checking finite-part slots."),
        )

    if field in {"external_constants_ledger_clean", "data_ledger_clean"}:
        return (
            _slot(prefix+":ledger_source", "ledger_source", "External/data ledger source.", "Must name source and provenance."),
            _slot(prefix+":ledger_no_targets", "ledger_no_targets", "No target leakage statement.", "Must certify no target/posterior/fitted output appears as input."),
        )

    if field in {"uncertainty_protocol_declared"}:
        return (
            _slot(prefix+":uncertainty_model", "uncertainty_model", "Uncertainty protocol.", "Must specify uncertainty propagation/comparison protocol."),
            _slot(prefix+":comparison_rule", "comparison_rule", "Comparison rule.", "Must state how prediction vs target is compared without inverse fitting."),
        )

    if field in {"chains_converged"}:
        return (
            _slot(prefix+":convergence_diagnostics", "convergence_diagnostics", "Convergence diagnostics.", "Must provide R-hat/ESS/trace or equivalent convergence evidence."),
        )

    if field in {"posterior_closed"}:
        return (
            _slot(prefix+":posterior_summary", "posterior_summary", "Posterior closure summary.", "Must provide posterior artifacts and closure criterion."),
            _slot(prefix+":posterior_repro_command", "posterior_repro_command", "Reproducible posterior command.", "Must include command/config hash/path."),
        )

    if field in {"robustness_checks_passed"}:
        return (
            _slot(prefix+":robustness_matrix", "robustness_matrix", "Robustness checks.", "Must list perturbations/knockouts and pass status."),
        )

    if field in {"overlap_cocycle_verified", "overlap_gluing_verified"}:
        return (
            _slot(prefix+":overlap_cover", "overlap_cover", "Overlap/cover specification.", "Must identify local patches/sections."),
            _slot(prefix+":gluing_proof", "gluing_proof", "Gluing/cocycle proof.", "Must provide proof or finite checker showing consistency."),
        )

    if field in {"capacity_bound_checked", "capacity_overspend_detected", "coarse_grain_factor"}:
        return (
            _slot(prefix+":capacity_budget", "capacity_budget", "Capacity budget.", "Must state budget and normalization."),
            _slot(prefix+":effective_load", "effective_load", "Effective load after repair/coarse-graining.", "Must show load <= budget."),
            _slot(prefix+":capacity_verifier", "capacity_verifier", "Capacity verifier.", "Must provide script/theorem checking no overspend."),
        )

    if field in {"local_fiber_action_defined", "group_law_verified", "representation_faithful", "anomaly_check_passed"}:
        return (
            _slot(prefix+":fiber_action_definition", "fiber_action_definition", "Fiber action definition.", "Must define action and domain."),
            _slot(prefix+":fiber_consistency_check", "fiber_consistency_check", "Fiber consistency verifier.", "Must check group law/faithfulness/anomaly as applicable."),
        )

    if field in {"horizon_partition_defined", "area_cost_map_defined", "entropy_ledger_clean"}:
        return (
            _slot(prefix+":horizon_partition", "horizon_partition", "Horizon/interface partition.", "Must define partition and interface domains."),
            _slot(prefix+":area_cost_map", "area_cost_map", "Area-cost map.", "Must define cost map and entropy ledger."),
        )

    if field in {"trace_sector_closed", "route_built", "run_completed", "local_solution_found", "acc_base_present", "empirical_or_posterior_closed"}:
        return (
            _slot(prefix+":closure_certificate", "closure_certificate", f"Closure certificate for {field}.", "Must provide verifier marker or theorem certificate."),
        )

    return (
        _slot(prefix+":evidence", "evidence", f"Evidence for repair field {field}.", "Must provide enough evidence to justify setting this field to the required value."),
    )


def obligation_for_patch(bundle_id: str, patch: Any) -> RepairObligation:
    # Patch comes from PayloadPatch dataclass in frontier explorer dependency.
    field = patch.field
    return RepairObligation(
        obligation_id=f"{bundle_id}:{field}",
        bundle_id=bundle_id,
        field=field,
        old_value=patch.old_value,
        required_value=patch.new_value,
        reason=patch.reason,
        evidence_slots=evidence_slots_for_field(field, bundle_id),
        rerun_hint="After supplying evidence, update the route payload, rerun discovery/certification, and require zero obstruction.",
    )


def compile_obligation_packet(route: str, payload: Mapping[str, Any]) -> ObligationPacket:
    frontier = explore_repair_frontier(route, payload)
    status = frontier.frontier_status

    if status == FrontierStatus.ALREADY_CLOSED:
        packet_status = ObligationPacketStatus.NOT_REQUIRED_ALREADY_P
        bundles: Tuple[ObligationBundle, ...] = tuple()
        blocked_reason = None
        ready = True
    elif status == FrontierStatus.REFUSE_PROVENANCE_FRONTIER:
        packet_status = ObligationPacketStatus.BLOCKED_PROVENANCE_REBUILD_REQUIRED
        bundles = tuple()
        blocked_reason = frontier.blocked_reason
        ready = False
    elif status == FrontierStatus.REFUSE_SUBSTRATE_FRONTIER:
        packet_status = ObligationPacketStatus.BLOCKED_SUBSTRATE_THEOREM_REQUIRED
        bundles = tuple()
        blocked_reason = frontier.blocked_reason
        ready = False
    elif status == FrontierStatus.NO_CLOSING_FRONTIER:
        packet_status = ObligationPacketStatus.NO_CLOSING_FRONTIER
        bundles = tuple()
        blocked_reason = frontier.blocked_reason
        ready = False
    else:
        packet_status = ObligationPacketStatus.OPEN_EVIDENCE_REQUIRED
        compiled = []
        for bundle in frontier.minimal_bundles:
            obligations = tuple(obligation_for_patch(bundle.bundle_id, patch) for patch in bundle.patches)
            compiled.append(
                ObligationBundle(
                    bundle_id=bundle.bundle_id,
                    fields=bundle.fields,
                    obligations=obligations,
                    minimal=True,
                )
            )
        bundles = tuple(compiled)
        blocked_reason = None
        ready = False

    return ObligationPacket(
        route=route,
        packet_status=packet_status,
        frontier_status=status,
        original_repair_class=frontier.original_repair_class.value,
        bundles=bundles,
        critical_fields=frontier.critical_fields,
        optional_fields=frontier.optional_fields,
        blocked_reason=blocked_reason,
        ready_to_rerun=ready,
        rerun_command_hint=f"After evidence is supplied, rerun the route certification for route={route}.",
        original_certificate=frontier.original_certificate,
    )


def evidence_template(packet: ObligationPacket) -> Dict[str, Any]:
    out = {
        "route": packet.route,
        "packet_status": packet.packet_status.value,
        "evidence": {},
    }
    for bundle in packet.bundles:
        out["evidence"][bundle.bundle_id] = {}
        for obligation in bundle.obligations:
            out["evidence"][bundle.bundle_id][obligation.obligation_id] = {
                slot.key: slot.example_value for slot in obligation.evidence_slots
            }
    return out


def validate_evidence(packet: ObligationPacket, evidence_payload: Mapping[str, Any]) -> EvidenceValidationResult:
    if packet.packet_status == ObligationPacketStatus.NOT_REQUIRED_ALREADY_P:
        return EvidenceValidationResult(
            packet_status=packet.packet_status,
            ready_to_rerun=True,
            satisfied_bundle_ids=tuple(),
            missing_slots=tuple(),
            supplied_slots=tuple(),
            rerun_command_hint=packet.rerun_command_hint,
            note="Already global P; no evidence required.",
        )

    if packet.packet_status in {
        ObligationPacketStatus.BLOCKED_PROVENANCE_REBUILD_REQUIRED,
        ObligationPacketStatus.BLOCKED_SUBSTRATE_THEOREM_REQUIRED,
        ObligationPacketStatus.NO_CLOSING_FRONTIER,
    }:
        return EvidenceValidationResult(
            packet_status=packet.packet_status,
            ready_to_rerun=False,
            satisfied_bundle_ids=tuple(),
            missing_slots=tuple(),
            supplied_slots=tuple(),
            rerun_command_hint=packet.rerun_command_hint,
            note=packet.blocked_reason or "Blocked packet cannot be evidence-validated into rerun readiness.",
        )

    evidence = evidence_payload.get("evidence", evidence_payload)
    missing: List[str] = []
    supplied: List[str] = []
    satisfied_bundles: List[str] = []

    for bundle in packet.bundles:
        bundle_evidence = evidence.get(bundle.bundle_id, {})
        bundle_missing: List[str] = []
        for obligation in bundle.obligations:
            obligation_evidence = bundle_evidence.get(obligation.obligation_id, {})
            for slot in obligation.evidence_slots:
                slot_key = f"{bundle.bundle_id}:{obligation.obligation_id}:{slot.key}"
                value = obligation_evidence.get(slot.key)
                if value in (None, "", [], {}, "TODO"):
                    bundle_missing.append(slot_key)
                else:
                    supplied.append(slot_key)
        if not bundle_missing:
            satisfied_bundles.append(bundle.bundle_id)
        else:
            missing.extend(bundle_missing)

    ready = bool(satisfied_bundles)
    status = ObligationPacketStatus.READY_TO_RERUN if ready else ObligationPacketStatus.OPEN_EVIDENCE_REQUIRED
    note = (
        f"At least one minimal bundle has complete evidence: {satisfied_bundles}."
        if ready
        else "No minimal bundle has complete evidence yet."
    )
    return EvidenceValidationResult(
        packet_status=status,
        ready_to_rerun=ready,
        satisfied_bundle_ids=tuple(satisfied_bundles),
        missing_slots=tuple(missing),
        supplied_slots=tuple(supplied),
        rerun_command_hint=packet.rerun_command_hint,
        note=note,
    )


def canonical_packets() -> Dict[str, ObligationPacket]:
    return {
        name: compile_obligation_packet(route, payload)
        for name, (route, payload) in canonical_payloads_for_simulation().items()
    }


def check_T_obligation_packet_compilation_P() -> Dict[str, Any]:
    packets = canonical_packets()
    tests = {
        "ew_open_requires_evidence": packets["ew_open"].packet_status == ObligationPacketStatus.OPEN_EVIDENCE_REQUIRED,
        "ew_open_has_bundles": len(packets["ew_open"].bundles) >= 1,
        "ew_open_has_slots": sum(len(o.evidence_slots) for b in packets["ew_open"].bundles for o in b.obligations) >= 4,
        "dark_open_requires_evidence": packets["dark_open"].packet_status == ObligationPacketStatus.OPEN_EVIDENCE_REQUIRED,
        "capacity_open_requires_evidence": packets["capacity_open"].packet_status == ObligationPacketStatus.OPEN_EVIDENCE_REQUIRED,
        "ew_closed_not_required": packets["ew_closed"].packet_status == ObligationPacketStatus.NOT_REQUIRED_ALREADY_P,
    }
    return {
        "name": "check_T_obligation_packet_compilation_P",
        "consistent": all(tests.values()),
        "status": "P_obligation" if all(tests.values()) else "FAIL",
        "summary": "Minimal repair frontiers compile into evidence obligation packets.",
        "data": {"tests": tests, "bundle_counts": {k: len(v.bundles) for k, v in packets.items()}},
    }


def check_T_obligation_blocked_cases_P() -> Dict[str, Any]:
    packets = canonical_packets()
    tests = {
        "provenance_blocked": packets["provenance_smuggled"].packet_status == ObligationPacketStatus.BLOCKED_PROVENANCE_REBUILD_REQUIRED,
        "cstar_blocked": packets["cstar"].packet_status == ObligationPacketStatus.BLOCKED_SUBSTRATE_THEOREM_REQUIRED,
        "provenance_no_bundles": len(packets["provenance_smuggled"].bundles) == 0,
        "cstar_no_bundles": len(packets["cstar"].bundles) == 0,
    }
    return {
        "name": "check_T_obligation_blocked_cases_P",
        "consistent": all(tests.values()),
        "status": "P_obligation" if all(tests.values()) else "FAIL",
        "summary": "Obligation compiler refuses evidence packets for provenance and substrate-blocked cases.",
        "data": {"tests": tests},
        "dependencies": ["check_T_obligation_packet_compilation_P"],
    }


def check_T_evidence_template_and_validation_P() -> Dict[str, Any]:
    packets = canonical_packets()
    packet = packets["ew_open"]
    template = evidence_template(packet)
    empty_validation = validate_evidence(packet, template)

    # Fill one minimal bundle completely.
    filled = json_like_copy(template)
    first_bundle_id = packet.bundles[0].bundle_id
    for obligation in packet.bundles[0].obligations:
        for slot in obligation.evidence_slots:
            filled["evidence"][first_bundle_id][obligation.obligation_id][slot.key] = f"evidence_for_{slot.key}"
    filled_validation = validate_evidence(packet, filled)

    tests = {
        "template_has_evidence": "evidence" in template,
        "empty_template_not_ready": empty_validation.ready_to_rerun is False,
        "filled_template_ready": filled_validation.ready_to_rerun is True,
        "filled_has_satisfied_bundle": first_bundle_id in filled_validation.satisfied_bundle_ids,
    }
    return {
        "name": "check_T_evidence_template_and_validation_P",
        "consistent": all(tests.values()),
        "status": "P_obligation" if all(tests.values()) else "FAIL",
        "summary": "Evidence templates validate to ready-to-rerun only after at least one minimal bundle is fully supplied.",
        "data": {"tests": tests, "first_bundle_id": first_bundle_id},
        "dependencies": ["check_T_obligation_blocked_cases_P"],
    }


def json_like_copy(x: Mapping[str, Any]) -> Dict[str, Any]:
    import json
    return json.loads(json.dumps(x))


def check_T_ready_to_rerun_is_not_truth_assertion_P() -> Dict[str, Any]:
    packets = canonical_packets()
    packet = packets["ew_open"]
    template = evidence_template(packet)
    first_bundle_id = packet.bundles[0].bundle_id
    for obligation in packet.bundles[0].obligations:
        for slot in obligation.evidence_slots:
            template["evidence"][first_bundle_id][obligation.obligation_id][slot.key] = f"evidence_for_{slot.key}"
    validation = validate_evidence(packet, template)
    tests = {
        "ready_to_rerun_true": validation.ready_to_rerun is True,
        "note_mentions_bundle": "minimal bundle" in validation.note.lower(),
        "rerun_hint_present": "rerun" in validation.rerun_command_hint.lower(),
        "packet_still_original_not_export": packet.original_certificate["export_global_P"] is False,
    }
    return {
        "name": "check_T_ready_to_rerun_is_not_truth_assertion_P",
        "consistent": all(tests.values()),
        "status": "P_audit" if all(tests.values()) else "FAIL",
        "summary": "Ready-to-rerun means evidence obligations are filled; it does not assert the original route is already P.",
        "data": {"tests": tests, "validation": validation.to_dict()},
        "dependencies": ["check_T_evidence_template_and_validation_P"],
    }


def check_T_interface_repair_obligation_compiler_P() -> Dict[str, Any]:
    subchecks = [
        check_T_obligation_packet_compilation_P(),
        check_T_obligation_blocked_cases_P(),
        check_T_evidence_template_and_validation_P(),
        check_T_ready_to_rerun_is_not_truth_assertion_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_interface_repair_obligation_compiler_P",
        "consistent": ok,
        "status": "P_obligation_compiler" if ok else "FAIL",
        "summary": "Interface Repair Obligation Compiler is P: minimal repair bundles become auditable evidence obligations and ready-to-rerun packets.",
        "data": {
            "core_claim": "Minimal repair bundles compile into evidence obligations; completion means ready-to-rerun, not proof of truth.",
            "subchecks": [x["name"] for x in subchecks],
            "packet_statuses": [x.value for x in ObligationPacketStatus],
        },
        "dependencies": [x["name"] for x in subchecks],
    }


CHECKS = {
    "check_T_obligation_packet_compilation_P": check_T_obligation_packet_compilation_P,
    "check_T_obligation_blocked_cases_P": check_T_obligation_blocked_cases_P,
    "check_T_evidence_template_and_validation_P": check_T_evidence_template_and_validation_P,
    "check_T_ready_to_rerun_is_not_truth_assertion_P": check_T_ready_to_rerun_is_not_truth_assertion_P,
    "check_T_interface_repair_obligation_compiler_P": check_T_interface_repair_obligation_compiler_P,
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
            raise TypeError("Unsupported registry type for interface_repair_obligation_compiler.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
