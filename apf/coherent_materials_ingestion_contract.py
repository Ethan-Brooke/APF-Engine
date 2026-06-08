"""CMAL external ingestion contract.

Defines the JSON shape external tools must emit before CMAL can absorb material
receipts. This is a contract, not an ingestion implementation: no live API
calls, authentication, scraping, or autonomous lab execution.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Mapping, Sequence

SOURCE_TYPES = {
    "COMPUTED_STABILITY",
    "STRUCTURE_KNOWN",
    "SYNTHESIS_REPORTED",
    "PROPERTY_MEASURED",
    "FUNCTIONAL_CLAIMED",
    "REPRODUCED",
    "LITERATURE_EXTRACTED",
    "LAB_NOTEBOOK_EXTRACTED",
}
REQUIRED_FIELDS = (
    "receipt_id", "source_type", "source_name", "material_id", "sample_id",
    "target_codomain", "receipt_kind", "claim_text", "measurement_or_computation",
    "control_vector", "value", "uncertainty", "unit", "method", "provenance",
    "replication_status", "updates_required_slots", "non_claims",
)
FORBIDDEN_CORE_BEHAVIORS = {
    "live_api_fetch",
    "auth_handling",
    "database_scraping",
    "autonomous_lab_execution",
    "claim_promotion_without_receipts",
    "direct_numeric_Tc_prediction",
}

@dataclass(frozen=True)
class APFMaterialReceipt:
    receipt_id: str
    source_type: str
    source_name: str
    material_id: str
    sample_id: str | None
    target_codomain: str
    receipt_kind: str
    claim_text: str
    measurement_or_computation: Mapping[str, Any]
    control_vector: Mapping[str, Any]
    value: Any
    uncertainty: Any
    unit: str | None
    method: str
    provenance: Mapping[str, Any]
    replication_status: str
    updates_required_slots: Sequence[str]
    non_claims: Sequence[str]

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "APFMaterialReceipt":
        missing = [k for k in REQUIRED_FIELDS if k not in data]
        if missing:
            raise ValueError(f"receipt missing required fields: {missing}")
        st = str(data["source_type"])
        if st not in SOURCE_TYPES:
            raise ValueError(f"unknown source_type: {st}")
        prov = data.get("provenance") or {}
        if not isinstance(prov, Mapping) or not prov.get("declared"):
            raise ValueError("provenance.declared must be true")
        return cls(**{k: data[k] for k in REQUIRED_FIELDS})

    def as_obligation_evidence_item(self) -> Dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "target_codomain": self.target_codomain,
            "receipt_kind": self.receipt_kind,
            "material_id": self.material_id,
            "source_type": self.source_type,
            "updates_required_slots": list(self.updates_required_slots),
            "provenance_declared": bool(self.provenance.get("declared")),
            "replication_status": self.replication_status,
        }


def validate_contract(contract: Mapping[str, Any], examples: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    if not contract.get("contract_not_implementation"):
        raise AssertionError("ingestion contract must explicitly be non-implementation")
    exports = contract.get("exports", {})
    if exports.get("public_ingestion_core_engine") != 0:
        raise AssertionError("public ingestion core engine must remain false")
    if exports.get("APF_Mat_sixth_engine") != 0:
        raise AssertionError("APF-Mat sixth engine must remain false")
    if exports.get("materials_discovery_OS_architecture") != 0:
        raise AssertionError("Materials Discovery OS architecture must remain false")
    ex_receipts = [APFMaterialReceipt.from_mapping(e) for e in examples]
    if len(ex_receipts) < 4:
        raise AssertionError("expected at least four example receipts")
    source_types_seen = {r.source_type for r in ex_receipts}
    required_seen = {"COMPUTED_STABILITY", "STRUCTURE_KNOWN", "FUNCTIONAL_CLAIMED", "LITERATURE_EXTRACTED"}
    if not required_seen.issubset(source_types_seen):
        raise AssertionError(f"missing example source types: {required_seen - source_types_seen}")
    evidence_items = [r.as_obligation_evidence_item() for r in ex_receipts]
    return {
        "contract_valid": True,
        "example_count": len(ex_receipts),
        "source_types_seen": sorted(source_types_seen),
        "evidence_items": evidence_items,
        "export_CMAL_external_ingestion_contract": 1,
        "export_APF_ingestable_receipt_shape": 1,
        "export_public_ingestion_core_engine": 0,
        "export_live_api_connector": 0,
        "export_autonomous_lab_execution": 0,
        "export_materials_discovery_OS_architecture": 0,
        "export_APF_Mat_sixth_engine": 0,
    }
