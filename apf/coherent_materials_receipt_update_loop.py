"""CMAL receipt-update loop.

Architecture-only utility. This module does not register bank checks and does
not create a new APF engine. It is a Coherent Materials Audit Layer utility
under the Codomain Selection Engine.

The loop consumes a current material ledger, a current obligation packet, and
new receipt objects. It updates the ledger, reruns the CMAL discriminator, and
emits the next obligation packet while preserving explicit non-claims.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

from apf.coherent_materials_discriminator import classify_material_ledger
from apf.coherent_materials_obligation_packet_adapter import (
    compile_materials_obligation_packet_from_ledger,
    packet_to_dict,
)

NONCLAIM_LEDGER: Dict[str, int] = {
    "APF_Mat_sixth_engine": 0,
    "materials_discovery_OS_architecture": 0,
    "materials_public_ingestion_core_engine": 0,
    "Atlas_MATERIALS_axis": 0,
    "SC_numeric_Tc_prediction": 0,
    "SC_new_material_prediction": 0,
    "SC_highTc_solution": 0,
    "SC_ab_initio_chemistry": 0,
    "autonomous_lab_execution": 0,
    "Pearson_superconductivity_claim": 0,
    "room_temperature_superconductivity_claim": 0,
    "ambient_superconductivity_from_pressure_only": 0,
}

UPDATE_STATUSES = {
    "PROMOTE_CODOMAIN",
    "PROMOTE_PRESSURE_CONDITIONED_SC",
    "HOLD_PARTIAL",
    "DEMOTE_CLAIM",
    "QUARANTINE_CLAIM",
    "REQUEST_NEXT_RECEIPT",
    "ROUTE_TO_DIFFERENT_CODOMAIN",
    "UPDATE_PHASE_BOUNDARY_MAP",
}

SC_REQUIRED_RECEIPTS = {
    "R_SC_RESISTIVITY_ZERO_OR_DROP",
    "R_SC_MEISSNER_DIAMAGNETIC_RESPONSE",
    "R_SC_FIELD_SUPPRESSION_OR_CRITICAL_FIELD",
    "R_SC_REPRODUCIBILITY_SAMPLE_PROVENANCE",
    "R_SC_PHASE_BOUNDARY_CONTEXT",
}

QM_REQUIRED_RECEIPTS = {
    "R_QM_HOMOGENEOUS_LINEWIDTH",
    "R_QM_INHOMOGENEOUS_LINEWIDTH",
    "R_QM_SPIN_LIFETIME_OR_COHERENCE",
    "R_QM_SPECTRAL_HOLE_OR_PHOTON_ECHO",
    "R_QM_AFC_OR_STORAGE_RECEIPT",
    "R_QM_STABILITY_SYNTHESIS_PROVENANCE",
}

@dataclass(frozen=True)
class Receipt:
    receipt_id: str
    material_id: str
    sample_id: str
    target_codomain: str
    receipt_kind: str
    measurement_method: str
    control_vector: Mapping[str, Any] = field(default_factory=dict)
    measured_value: Any = None
    uncertainty: Any = None
    instrument_or_protocol: str = ""
    provenance: Mapping[str, Any] = field(default_factory=dict)
    replication_status: str = "single_run"
    contradicts_prior: bool = False
    updates_required_slots: Sequence[str] = field(default_factory=tuple)
    pass_fail: str = "pass"

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "Receipt":
        return cls(
            receipt_id=str(data.get("receipt_id", "UNKNOWN_RECEIPT")),
            material_id=str(data.get("material_id", data.get("ledger_id", "unknown_material"))),
            sample_id=str(data.get("sample_id", "unknown_sample")),
            target_codomain=str(data.get("target_codomain", "coherent_materials")),
            receipt_kind=str(data.get("receipt_kind", data.get("kind", "unknown"))),
            measurement_method=str(data.get("measurement_method", data.get("method", "unknown"))),
            control_vector=dict(data.get("control_vector", {})),
            measured_value=data.get("measured_value"),
            uncertainty=data.get("uncertainty"),
            instrument_or_protocol=str(data.get("instrument_or_protocol", "")),
            provenance=dict(data.get("provenance", {})),
            replication_status=str(data.get("replication_status", "single_run")),
            contradicts_prior=bool(data.get("contradicts_prior", False)),
            updates_required_slots=tuple(str(x) for x in data.get("updates_required_slots", ())),
            pass_fail=str(data.get("pass_fail", "pass")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "material_id": self.material_id,
            "sample_id": self.sample_id,
            "target_codomain": self.target_codomain,
            "receipt_kind": self.receipt_kind,
            "measurement_method": self.measurement_method,
            "control_vector": dict(self.control_vector),
            "measured_value": self.measured_value,
            "uncertainty": self.uncertainty,
            "instrument_or_protocol": self.instrument_or_protocol,
            "provenance": dict(self.provenance),
            "replication_status": self.replication_status,
            "contradicts_prior": self.contradicts_prior,
            "updates_required_slots": list(self.updates_required_slots),
            "pass_fail": self.pass_fail,
        }

@dataclass(frozen=True)
class ReceiptUpdateResult:
    ledger_id: str
    previous_classification: str
    updated_classification: str
    update_status: str
    promotion: bool
    demotion: bool
    quarantine: bool
    receipts_accepted: Tuple[str, ...]
    missing_evidence_required: Tuple[str, ...]
    updated_ledger: Mapping[str, Any]
    next_obligation_packet: Mapping[str, Any]
    preserved_nonclaims: Mapping[str, int]
    reasons: Tuple[str, ...]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ledger_id": self.ledger_id,
            "previous_classification": self.previous_classification,
            "updated_classification": self.updated_classification,
            "update_status": self.update_status,
            "promotion": self.promotion,
            "demotion": self.demotion,
            "quarantine": self.quarantine,
            "receipts_accepted": list(self.receipts_accepted),
            "missing_evidence_required": list(self.missing_evidence_required),
            "updated_ledger": dict(self.updated_ledger),
            "next_obligation_packet": dict(self.next_obligation_packet),
            "preserved_nonclaims": dict(self.preserved_nonclaims),
            "reasons": list(self.reasons),
        }


def _truthy_value(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in {"true", "pass", "present", "positive", "yes", "detected", "observed"}
    return bool(value)


def _float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _current_required(packet: Mapping[str, Any]) -> List[str]:
    return [str(x) for x in packet.get("evidence_required", [])]


def _accepts_required_slot(receipt: Receipt, required_slot: str) -> bool:
    if required_slot in receipt.updates_required_slots:
        return receipt.pass_fail.lower() == "pass"
    # Direct binding if receipt_kind and required slot use the registry IDs.
    return receipt.receipt_kind == required_slot and receipt.pass_fail.lower() == "pass"


def _apply_one_receipt(ledger: MutableMapping[str, Any], receipt: Receipt) -> None:
    evidence = ledger.setdefault("evidence", {})
    controls = ledger.setdefault("controls", {})
    provenance = ledger.setdefault("provenance", {})
    burdens = ledger.setdefault("burdens", {})
    receipts = ledger.setdefault("receipts", [])
    phase_map = ledger.setdefault("phase_boundary_map", {"receipts": []})
    receipts.append(receipt.to_dict())

    # Merge control vector values without erasing existing context.
    for key, value in receipt.control_vector.items():
        controls[key] = value

    if receipt.provenance:
        provenance["declared"] = bool(receipt.provenance.get("declared", True))
        provenance.setdefault("receipt_sources", []).append(dict(receipt.provenance))

    kind = receipt.receipt_kind
    if receipt.pass_fail.lower() != "pass":
        # Negative or failed receipts are evidence too: they block promotion and may increase burden.
        if kind in {"R_SC_MEISSNER_DIAMAGNETIC_RESPONSE", "meissner_response", "diamagnetic_response"}:
            evidence["meissner"] = False
            evidence["diamagnetic_response"] = False
        if kind in {"instability", "R_QM_STABILITY_SYNTHESIS_PROVENANCE"}:
            burdens["stability"] = max(_float(burdens.get("stability")), 1.0)
        return

    if kind in {"R_SC_RESISTIVITY_ZERO_OR_DROP", "resistance_trace", "zero_resistance"}:
        evidence["zero_resistance"] = True
        evidence["resistive_transition"] = True
        evidence["sigma_declared"] = True
    elif kind in {"normal_state_reference"}:
        evidence["normal_state_reference"] = True
    elif kind in {"R_SC_MEISSNER_DIAMAGNETIC_RESPONSE", "meissner_response", "diamagnetic_response"}:
        evidence["meissner"] = True
        evidence["diamagnetic_response"] = True
    elif kind in {"R_SC_FIELD_SUPPRESSION_OR_CRITICAL_FIELD", "field_suppression", "critical_field_response"}:
        evidence["field_suppression"] = True
        evidence["critical_field_response"] = True
    elif kind in {"R_SC_REPRODUCIBILITY_SAMPLE_PROVENANCE", "replication", "sample_provenance"}:
        evidence["reproducible"] = True
        provenance["declared"] = True
    elif kind in {"R_SC_PHASE_BOUNDARY_CONTEXT", "phase_coherence", "heat_capacity_or_phase_evidence"}:
        evidence["phase_coherence"] = True
        phase_map["receipts"].append(receipt.receipt_id)
    elif kind in {"R_QM_HOMOGENEOUS_LINEWIDTH", "homogeneous_linewidth"}:
        evidence["homogeneous_linewidth_kHz"] = _float(receipt.measured_value, evidence.get("homogeneous_linewidth_kHz", 0.0))
    elif kind in {"R_QM_INHOMOGENEOUS_LINEWIDTH", "inhomogeneous_linewidth"}:
        evidence["inhomogeneous_linewidth_GHz"] = _float(receipt.measured_value, evidence.get("inhomogeneous_linewidth_GHz", 0.0))
    elif kind in {"optical_lifetime"}:
        evidence["optical_lifetime_ms"] = _float(receipt.measured_value, evidence.get("optical_lifetime_ms", 0.0))
    elif kind in {"R_QM_SPIN_LIFETIME_OR_COHERENCE", "spin_lifetime"}:
        evidence["spin_lifetime_s"] = _float(receipt.measured_value, evidence.get("spin_lifetime_s", 0.0))
    elif kind in {"R_QM_SPECTRAL_HOLE_OR_PHOTON_ECHO", "spectral_hole_burning", "photon_echo"}:
        evidence["spectral_hole_burning"] = True
    elif kind in {"R_QM_AFC_OR_STORAGE_RECEIPT", "afc_storage", "afc_retrieval"}:
        evidence["afc_retrieval"] = True
        if receipt.measured_value is not None:
            evidence["afc_max_efficiency_percent"] = _float(receipt.measured_value, evidence.get("afc_max_efficiency_percent", 0.0))
    elif kind in {"R_QM_STABILITY_SYNTHESIS_PROVENANCE", "stability", "synthesis_provenance"}:
        evidence["environmentally_stable"] = True
        burdens["stability"] = min(_float(burdens.get("stability")), 0.2)
        provenance["declared"] = True
    elif kind in {"instability"}:
        evidence["environmentally_stable"] = False
        burdens["stability"] = max(_float(burdens.get("stability")), 1.0)
    elif kind in {"broadening", "inhomogeneity_burden"}:
        burdens["inhomogeneity"] = max(_float(burdens.get("inhomogeneity")), _float(receipt.measured_value, 1.4))
    elif kind in {"strain_sweep", "pressure_sweep", "oxygenation_sweep", "phase_boundary_sweep"}:
        phase_map["receipts"].append(receipt.receipt_id)
        phase_map.setdefault("control_axes_swept", []).append(kind)
    elif kind in {"high_pressure_sc_transport", "high_pressure_sc_field_response"}:
        evidence["zero_resistance"] = True
        evidence["resistive_transition"] = True
        evidence["field_suppression"] = True
        evidence["phase_coherence"] = True
        evidence["reproducible"] = True
        if kind == "high_pressure_sc_field_response":
            evidence["meissner"] = True
    # Unknown receipts are retained in the receipt ledger but do not promote.


def _coverage(required: Sequence[str], receipts: Sequence[Receipt]) -> Tuple[str, ...]:
    covered = set()
    for req in required:
        for receipt in receipts:
            if _accepts_required_slot(receipt, req):
                covered.add(req)
    return tuple(req for req in required if req not in covered)


def _status_after_update(previous: str, updated: str, ledger: Mapping[str, Any], receipts: Sequence[Receipt], missing: Sequence[str]) -> Tuple[str, List[str]]:
    reasons: List[str] = []
    if any(r.contradicts_prior for r in receipts):
        reasons.append("new_receipt_contradicts_prior_ledger")
        return "QUARANTINE_CLAIM", reasons
    if updated == "CLAIM_QUARANTINED":
        reasons.append("updated_discriminator_state_is_quarantine")
        return "QUARANTINE_CLAIM", reasons
    if any(r.receipt_kind in {"strain_sweep", "pressure_sweep", "oxygenation_sweep", "phase_boundary_sweep"} for r in receipts):
        reasons.append("phase-boundary receipts update map without formula-level material prediction")
        return "UPDATE_PHASE_BOUNDARY_MAP", reasons
    if updated == "DEFECT_OR_INHOMOGENEITY_OVERLOADED":
        reasons.append("new receipts keep or increase material burden")
        return "DEMOTE_CLAIM", reasons
    if missing:
        reasons.append("required_receipts_still_missing")
        if updated in {"MATERIAL_LEDGER_INSUFFICIENT", "RESISTIVE_ONLY_NO_MEISSNER", "COHERENT_SIGNATURE_PARTIAL"}:
            return "REQUEST_NEXT_RECEIPT", reasons
        return "HOLD_PARTIAL", reasons
    if updated == "SC_MATERIAL_ADMISSIBLE":
        pressure = _float((ledger.get("controls", {}) or {}).get("pressure_GPa", 0.0))
        if pressure and pressure > 1.0:
            reasons.append("SC evidence is pressure-conditioned; ambient usability not promoted")
            return "PROMOTE_PRESSURE_CONDITIONED_SC", reasons
        reasons.append("all SC material admissibility receipts complete")
        return "PROMOTE_CODOMAIN", reasons
    if updated == "COHERENT_BUT_NOT_SC":
        reasons.append("coherent-material receipts complete for non-SC codomain")
        return "PROMOTE_CODOMAIN", reasons
    if previous != updated:
        reasons.append("classification changed but not to full promotion")
        return "ROUTE_TO_DIFFERENT_CODOMAIN", reasons
    reasons.append("receipts accepted but claim state remains partial")
    return "HOLD_PARTIAL", reasons


def apply_receipt_update(
    ledger: Mapping[str, Any],
    obligation_packet: Mapping[str, Any],
    new_receipts: Iterable[Mapping[str, Any] | Receipt],
) -> ReceiptUpdateResult:
    """Apply receipts to a material ledger and emit an updated claim state.

    The operation is fail-closed. Full promotion only happens after the supplied
    receipt set covers the current obligation packet's evidence_required field
    and the updated discriminator classification is promotable.
    """
    ledger0 = deepcopy(dict(ledger))
    receipts = tuple(r if isinstance(r, Receipt) else Receipt.from_mapping(r) for r in new_receipts)
    previous = classify_material_ledger(ledger0).classification
    required = _current_required(obligation_packet)

    ledger1: Dict[str, Any] = deepcopy(ledger0)
    for receipt in receipts:
        _apply_one_receipt(ledger1, receipt)

    updated_result = classify_material_ledger(ledger1)
    missing = _coverage(required, receipts)

    status, reasons = _status_after_update(previous, updated_result.classification, ledger1, receipts, missing)
    # If receipts do not cover required slots, do not allow full promotion even if the ledger now looks complete.
    if missing and status in {"PROMOTE_CODOMAIN", "PROMOTE_PRESSURE_CONDITIONED_SC"}:
        status = "REQUEST_NEXT_RECEIPT"
        reasons.append("promotion_blocked_until_current_obligation_packet_is_receipt_complete")

    next_packet = packet_to_dict(compile_materials_obligation_packet_from_ledger(ledger1))

    promotion = status in {"PROMOTE_CODOMAIN", "PROMOTE_PRESSURE_CONDITIONED_SC"}
    demotion = status == "DEMOTE_CLAIM"
    quarantine = status == "QUARANTINE_CLAIM"
    return ReceiptUpdateResult(
        ledger_id=str(ledger1.get("ledger_id", "unknown_material_ledger")),
        previous_classification=previous,
        updated_classification=updated_result.classification,
        update_status=status,
        promotion=promotion,
        demotion=demotion,
        quarantine=quarantine,
        receipts_accepted=tuple(r.receipt_id for r in receipts if r.pass_fail.lower() == "pass"),
        missing_evidence_required=tuple(missing),
        updated_ledger=ledger1,
        next_obligation_packet=next_packet,
        preserved_nonclaims=dict(NONCLAIM_LEDGER),
        reasons=tuple(list(updated_result.reasons) + reasons),
    )


def receipt_update_roundtrip(ledger: Mapping[str, Any], receipts: Iterable[Mapping[str, Any] | Receipt]) -> Dict[str, Any]:
    """Compile the current obligation packet, apply receipts, and return a dict result."""
    packet = packet_to_dict(compile_materials_obligation_packet_from_ledger(ledger))
    return apply_receipt_update(ledger, packet, receipts).to_dict()
