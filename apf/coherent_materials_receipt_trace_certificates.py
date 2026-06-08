"""CMAL receipt trace certificates (architecture-only).

Builds deterministic, source-bound certificates for CMAL receipt/update/triage
results. This module does not register bank checks, does not create a new APF
engine, and does not implement live ingestion. It attaches a reproducible audit
hash to the receipt-to-classification path so downstream reviewers can see which
receipts produced which claim state and which non-claims were preserved.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence
import hashlib
import json

NONCLAIM_GUARDS: dict[str, int] = {
    "APF_Mat_sixth_engine": 0,
    "materials_discovery_OS_architecture": 0,
    "materials_live_ingestion_connector": 0,
    "materials_public_ingestion_core_engine": 0,
    "autonomous_lab_execution": 0,
    "SC_numeric_Tc_prediction": 0,
    "SC_new_material_prediction": 0,
    "SC_highTc_solution": 0,
    "SC_ab_initio_chemistry": 0,
    "Pearson_superconductivity_claim": 0,
    "room_temperature_superconductivity_claim": 0,
    "ambient_superconductivity_from_pressure_only": 0,
}

@dataclass(frozen=True)
class ReceiptTraceCertificate:
    certificate_id: str
    case_id: str
    material_id: str
    target_codomain: str
    receipt_ids: tuple[str, ...]
    source_anchors: tuple[str, ...]
    validation_statuses: tuple[str, ...]
    validation_routes: tuple[str, ...]
    update_status: str
    updated_classification: str
    triage_bucket: str
    next_action: str
    obligation_packet_id: str
    promotion_state: str
    nonclaim_guards: Mapping[str, int]
    audit_hash: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "certificate_id": self.certificate_id,
            "case_id": self.case_id,
            "material_id": self.material_id,
            "target_codomain": self.target_codomain,
            "receipt_ids": list(self.receipt_ids),
            "source_anchors": list(self.source_anchors),
            "validation_statuses": list(self.validation_statuses),
            "validation_routes": list(self.validation_routes),
            "update_status": self.update_status,
            "updated_classification": self.updated_classification,
            "triage_bucket": self.triage_bucket,
            "next_action": self.next_action,
            "obligation_packet_id": self.obligation_packet_id,
            "promotion_state": self.promotion_state,
            "nonclaim_guards": dict(self.nonclaim_guards),
            "audit_hash": self.audit_hash,
        }


def _stable_hash(payload: Mapping[str, Any]) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _as_mapping(result: Any) -> Mapping[str, Any]:
    if hasattr(result, "to_dict"):
        return result.to_dict()
    if isinstance(result, Mapping):
        return result
    raise TypeError(f"unsupported result type: {type(result)!r}")


def _receipt_ids(case: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(str(r.get("receipt_id", "UNKNOWN_RECEIPT")) for r in case.get("receipts", ()))


def _material_id(case: Mapping[str, Any]) -> str:
    receipts = list(case.get("receipts", ()))
    if receipts:
        return str(receipts[0].get("material_id", case.get("ledger", {}).get("ledger_id", "unknown_material")))
    ledger = case.get("ledger", {})
    mat = ledger.get("material", {}) if isinstance(ledger, Mapping) else {}
    return str(mat.get("composition", ledger.get("ledger_id", "unknown_material")))


def _target_codomain(case: Mapping[str, Any]) -> str:
    receipts = list(case.get("receipts", ()))
    if receipts:
        targets = [str(r.get("target_codomain", "unknown")) for r in receipts]
        return "+".join(sorted(set(targets)))
    ledger = case.get("ledger", {})
    return str(ledger.get("target_codomain", ledger.get("coherence_type", "unknown")))


def _source_anchors(case: Mapping[str, Any]) -> tuple[str, ...]:
    anchors: list[str] = []
    for r in case.get("receipts", ()):
        prov = r.get("provenance", {}) if isinstance(r, Mapping) else {}
        if isinstance(prov, Mapping):
            anchor = prov.get("source_anchor") or prov.get("source") or prov.get("chain") or prov.get("source_url")
        else:
            anchor = str(prov)
        if anchor:
            anchors.append(str(anchor))
    return tuple(dict.fromkeys(anchors))


def _obligation_packet_id(packet: Mapping[str, Any]) -> str:
    for key in ("packet_id", "target_unit_id", "obligation_id"):
        if packet.get(key):
            return str(packet[key])
    if packet:
        return "packet:" + _stable_hash(packet)[:16]
    return "packet:none"


def _promotion_state(update_status: str, classification: str) -> str:
    if update_status in {"PROMOTE_CODOMAIN", "PROMOTE_PRESSURE_CONDITIONED_SC"}:
        return "PROMOTED_WITH_BOUNDARY"
    if update_status == "QUARANTINE_CLAIM" or classification == "CLAIM_QUARANTINED":
        return "QUARANTINED"
    if update_status == "ROUTE_TO_DIFFERENT_CODOMAIN":
        return "REROUTED"
    if update_status == "UPDATE_PHASE_BOUNDARY_MAP":
        return "UPDATED_MAP_NO_MATERIAL_PREDICTION"
    if update_status == "DEMOTE_CLAIM":
        return "DEMOTED"
    return "HELD_OR_PARTIAL"


def build_trace_certificate(case_id: str, case: Mapping[str, Any], result: Any) -> ReceiptTraceCertificate:
    rd = dict(_as_mapping(result))
    packet = dict(rd.get("obligation_packet", {}))
    update_status = str(rd.get("update_status", "UNKNOWN_UPDATE"))
    classification = str(rd.get("updated_classification", "UNKNOWN_CLASSIFICATION"))
    core_payload = {
        "case_id": case_id,
        "material_id": _material_id(case),
        "target_codomain": _target_codomain(case),
        "receipt_ids": list(_receipt_ids(case)),
        "source_anchors": list(_source_anchors(case)),
        "validation_statuses": list(rd.get("validation_statuses", ())),
        "validation_routes": list(rd.get("validation_routes", ())),
        "update_status": update_status,
        "updated_classification": classification,
        "triage_bucket": rd.get("triage_bucket"),
        "next_action": rd.get("next_action"),
        "obligation_packet_id": _obligation_packet_id(packet),
        "promotion_state": _promotion_state(update_status, classification),
        "nonclaim_guards": dict(NONCLAIM_GUARDS),
    }
    h = _stable_hash(core_payload)
    return ReceiptTraceCertificate(
        certificate_id="CMAL-TRACE-" + h[:16].upper(),
        case_id=case_id,
        material_id=str(core_payload["material_id"]),
        target_codomain=str(core_payload["target_codomain"]),
        receipt_ids=tuple(core_payload["receipt_ids"]),
        source_anchors=tuple(core_payload["source_anchors"]),
        validation_statuses=tuple(str(x) for x in core_payload["validation_statuses"]),
        validation_routes=tuple(str(x) for x in core_payload["validation_routes"]),
        update_status=update_status,
        updated_classification=classification,
        triage_bucket=str(core_payload["triage_bucket"]),
        next_action=str(core_payload["next_action"]),
        obligation_packet_id=str(core_payload["obligation_packet_id"]),
        promotion_state=str(core_payload["promotion_state"]),
        nonclaim_guards=dict(NONCLAIM_GUARDS),
        audit_hash=h,
    )


def certify_cases(cases: Mapping[str, Mapping[str, Any]]) -> list[ReceiptTraceCertificate]:
    from apf.coherent_materials_batch_triage_runner import run_case
    certs: list[ReceiptTraceCertificate] = []
    for case_id, case in cases.items():
        result = run_case(case_id, case)
        certs.append(build_trace_certificate(case_id, case, result))
    return certs


def certificates_to_report(certs: Sequence[ReceiptTraceCertificate]) -> dict[str, Any]:
    return {
        "schema": "CMAL_RECEIPT_TRACE_CERTIFICATE_REPORT_v1",
        "certificate_count": len(certs),
        "certificates": [c.to_dict() for c in certs],
        "preserved_nonclaims": dict(NONCLAIM_GUARDS),
    }


def write_certificate_report(path: str, certs: Sequence[ReceiptTraceCertificate]) -> str:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(certificates_to_report(certs), f, indent=2, ensure_ascii=False)
    return path
