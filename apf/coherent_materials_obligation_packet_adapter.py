from __future__ import annotations

from dataclasses import asdict
from typing import Any, Mapping

from apf.coherent_materials_protocol_compiler import ProtocolCard, compile_protocol
from apf.obligation_packet_meta_schema import (
    EngineSubtype,
    ObligationPacketMetaSchema,
    validate_meta_schema,
)


OBLIGATION_KIND_BY_PROTOCOL_ID = {
    "SC_PHASE_BOUNDARY_MAPPING_PROTOCOL": "materials_phase_boundary_mapping_receipts_required",
    "SC_EVIDENCE_COMPLETION_PROTOCOL": "materials_sc_evidence_completion_receipts_required",
    "PEARSON_QM_AFC_OPTIMIZATION_PROTOCOL": "materials_non_sc_quantum_memory_receipts_required",
    "BURDEN_REDUCTION_PROTOCOL": "materials_defect_inhomogeneity_burden_reduction_receipts_required",
    "CORRELATED_LAYER_PHASE_BOUNDARY_PROTOCOL": "materials_correlated_layer_phase_boundary_receipts_required",
    "HIGH_PRESSURE_BURDEN_SEPARATION_PROTOCOL": "materials_high_pressure_burden_separation_receipts_required",
    "MATERIAL_LEDGER_COMPLETION_PROTOCOL": "materials_ledger_completion_receipts_required",
    "CLAIM_QUARANTINE_REPLICATION_PROTOCOL": "materials_claim_quarantine_replication_receipts_required",
}

FUNCTIONAL_CODOMAIN_BY_PROTOCOL_ID = {
    "SC_PHASE_BOUNDARY_MAPPING_PROTOCOL": "superconductivity",
    "SC_EVIDENCE_COMPLETION_PROTOCOL": "superconductivity",
    "PEARSON_QM_AFC_OPTIMIZATION_PROTOCOL": "quantum_memory",
    "BURDEN_REDUCTION_PROTOCOL": "coherent_material_burden_reduction",
    "CORRELATED_LAYER_PHASE_BOUNDARY_PROTOCOL": "correlated_layer_superconductivity_competition",
    "HIGH_PRESSURE_BURDEN_SEPARATION_PROTOCOL": "pressure_conditioned_superconductivity",
    "MATERIAL_LEDGER_COMPLETION_PROTOCOL": "ledger_completion",
    "CLAIM_QUARANTINE_REPLICATION_PROTOCOL": "claim_quarantine",
}


def _protocol_to_dict(protocol: ProtocolCard | Mapping[str, Any]) -> dict[str, Any]:
    if isinstance(protocol, ProtocolCard):
        return protocol.to_dict()
    return dict(protocol)


def _status_for_protocol(protocol: Mapping[str, Any]) -> str:
    gate = str(protocol.get("classification_gate", "UNKNOWN"))
    pid = str(protocol.get("protocol_id", "UNKNOWN"))
    if pid == "CLAIM_QUARANTINE_REPLICATION_PROTOCOL":
        return "CLAIM_QUARANTINED_AWAITING_REPLICATION_RECEIPTS"
    if pid == "MATERIAL_LEDGER_COMPLETION_PROTOCOL":
        return "MATERIAL_LEDGER_INSUFFICIENT_AWAITING_COMPLETION_RECEIPTS"
    if pid == "SC_EVIDENCE_COMPLETION_PROTOCOL":
        return "RESISTIVE_ONLY_AWAITING_BULK_SC_RECEIPTS"
    if pid == "PEARSON_QM_AFC_OPTIMIZATION_PROTOCOL":
        return "NONSC_QM_COHERENCE_AWAITING_AFC_RECEIPTS"
    return f"{gate or 'MATERIAL'}_AWAITING_PROTOCOL_RECEIPTS"


def _non_claims_clean(non_claims: Mapping[str, Any]) -> bool:
    # In the v5 protocol compiler, all forbidden exports are explicitly 0.
    return all(int(v) == 0 for v in non_claims.values())


def compile_materials_obligation_packet(
    protocol: ProtocolCard | Mapping[str, Any],
    *,
    ledger_id: str = "unknown_material_ledger",
    material_family: str = "unknown",
    functional_codomain: str | None = None,
) -> ObligationPacketMetaSchema:
    """Compile a CMAL protocol card into the existing obligation packet meta-schema.

    This is the narrow architectural adapter requested by the CMAL Reference doc:
    it does not introduce a new receipt schema. It binds protocol receipts to
    ``obligation_packet_meta_schema.evidence_required`` and preserves the rest of
    the protocol card inside ``engine_subtype_data``.
    """
    p = _protocol_to_dict(protocol)
    pid = str(p.get("protocol_id", "UNKNOWN_PROTOCOL"))
    non_claims = dict(p.get("non_claims_preserved", {}))
    functional = functional_codomain or FUNCTIONAL_CODOMAIN_BY_PROTOCOL_ID.get(pid, "coherent_materials")
    evidence_required = tuple(str(x) for x in p.get("required_evidence_receipts", ()))

    subtype_data = {
        "adapter_schema": "APF_COHERENT_MATERIALS_OBLIGATION_PACKET_ADAPTER_v1",
        "receipt_binding": "obligation_packet_meta_schema.evidence_required",
        "receipts_are_new_schema": False,
        "ledger_id": ledger_id,
        "material_family": material_family,
        "functional_codomain": functional,
        "protocol_id": pid,
        "objective": p.get("objective", ""),
        "classification_gate": p.get("classification_gate", ""),
        "top_action": p.get("top_action", ""),
        "control_axes": tuple(p.get("control_axes", ())),
        "prerequisite_receipts": tuple(p.get("prerequisite_receipts", ())),
        "measurement_sequence": tuple(p.get("measurement_sequence", ())),
        "pass_condition": p.get("pass_condition", ""),
        "fail_condition": p.get("fail_condition", ""),
        "next_transition": p.get("next_transition", ""),
        "no_smuggling_guards": tuple(p.get("no_smuggling_guards", ())),
        "non_claims_preserved": non_claims,
        "review_placement": "Coherent Materials Audit Layer under Codomain Selection Engine",
    }

    return ObligationPacketMetaSchema(
        obligation_kind=OBLIGATION_KIND_BY_PROTOCOL_ID.get(pid, "materials_protocol_receipts_required"),
        target_engine="codomain_selection",
        target_unit_id=f"materials:{functional}:{ledger_id}",
        evidence_required=evidence_required,
        current_status=_status_for_protocol(p),
        recommended_next_action=str(p.get("top_action", "")),
        engine_subtype=EngineSubtype.CODOMAIN_SELECTION,
        engine_subtype_data=subtype_data,
        audit_first_non_claims_preserved=_non_claims_clean(non_claims),
    )


def compile_materials_obligation_packet_from_ledger(ledger: Mapping[str, Any]) -> ObligationPacketMetaSchema:
    """Compile a source demo/material ledger into a protocol card, then an obligation packet."""
    protocol = compile_protocol(ledger)
    ledger_id = str(ledger.get("ledger_id", ledger.get("material_id", "unknown_material_ledger")))
    material_family = str(ledger.get("material_family", ledger.get("family", "unknown")))
    return compile_materials_obligation_packet(
        protocol,
        ledger_id=ledger_id,
        material_family=material_family,
    )


def packet_to_dict(packet: ObligationPacketMetaSchema) -> dict[str, Any]:
    d = packet.to_dict()
    valid, errors = validate_meta_schema(d)
    d["meta_schema_valid"] = valid
    d["meta_schema_errors"] = errors
    return d


def compile_demo_packets(demo_ledgers: Mapping[str, Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    """Compile all demo ledgers to meta-schema packet dictionaries."""
    out: dict[str, dict[str, Any]] = {}
    for name, ledger in demo_ledgers.items():
        out[name] = packet_to_dict(compile_materials_obligation_packet_from_ledger(ledger))
    return out
