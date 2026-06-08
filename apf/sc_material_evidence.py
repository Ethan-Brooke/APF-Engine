"""APF superconductivity material evidence audit ladder.

Fail-closed classifier. It does not determine whether a real material is a
superconductor; it determines whether the declared evidence is admissible for
SC material-branch promotion.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List

CLASSIFICATIONS = (
    "SC_MATERIAL_ADMISSIBLE",
    "SC_SIGNATURE_PARTIAL",
    "RESISTIVE_ONLY_NO_MEISSNER",
    "COMPETING_PHASE_DOMINANT",
    "MATERIAL_LEDGER_INSUFFICIENT",
    "CLAIM_QUARANTINED",
)

FORBIDDEN_FLAGS = (
    "target_Tc_fit",
    "post_hoc_threshold",
    "sample_unidentified",
    "no_provenance",
    "known_label_used_as_input",
    "retracted_or_contradicted_source_unresolved",
)

@dataclass(frozen=True)
class SCEvidenceRecord:
    ledger_complete: bool
    resistive_transition: bool
    zero_resistance_claim: bool
    meissner_or_diamagnetic: bool
    field_suppression_or_critical_field: bool
    reproducible_across_samples_or_runs: bool
    sample_provenance_declared: bool
    uncertainty_or_covariance_declared: bool
    competing_phase_dominant: bool = False
    forbidden_flags_present: List[str] = field(default_factory=list)

    def forbidden(self) -> bool:
        return any(flag in FORBIDDEN_FLAGS for flag in self.forbidden_flags_present)

@dataclass(frozen=True)
class SCEvidenceAuditResult:
    classification: str
    promotion_allowed: bool
    missing_evidence: List[str]
    exports: Dict[str, int]


def classify_sc_evidence(record: SCEvidenceRecord) -> SCEvidenceAuditResult:
    missing: List[str] = []

    if record.forbidden():
        cls = "CLAIM_QUARANTINED"
        return _result(cls, missing)

    if not record.ledger_complete:
        cls = "MATERIAL_LEDGER_INSUFFICIENT"
        return _result(cls, ["ledger_complete"])

    if record.competing_phase_dominant:
        cls = "COMPETING_PHASE_DOMINANT"
        return _result(cls, ["competing_phase_resolution"])

    # Resistive-only pattern is explicitly quarantined at lower ladder level.
    if (record.resistive_transition or record.zero_resistance_claim) and not record.meissner_or_diamagnetic:
        cls = "RESISTIVE_ONLY_NO_MEISSNER"
        return _result(cls, ["meissner_or_diamagnetic"])

    required = {
        "resistive_transition_or_zero_resistance": record.resistive_transition or record.zero_resistance_claim,
        "meissner_or_diamagnetic": record.meissner_or_diamagnetic,
        "field_suppression_or_critical_field": record.field_suppression_or_critical_field,
        "reproducible_across_samples_or_runs": record.reproducible_across_samples_or_runs,
        "sample_provenance_declared": record.sample_provenance_declared,
        "uncertainty_or_covariance_declared": record.uncertainty_or_covariance_declared,
    }
    missing = [name for name, ok in required.items() if not ok]

    cls = "SC_MATERIAL_ADMISSIBLE" if not missing else "SC_SIGNATURE_PARTIAL"
    return _result(cls, missing)


def _result(classification: str, missing: List[str]) -> SCEvidenceAuditResult:
    if classification not in CLASSIFICATIONS:
        raise ValueError(f"unknown classification: {classification}")
    promotion = classification == "SC_MATERIAL_ADMISSIBLE"
    return SCEvidenceAuditResult(
        classification=classification,
        promotion_allowed=promotion,
        missing_evidence=missing,
        exports={
            "SC_material_evidence_audit_ladder": 1,
            "SC_material_admissible": int(promotion),
            "SC_resistive_only_full_promotion": 0,
            "SC_material_prediction": 0,
            "SC_numeric_Tc": 0,
        },
    )


def load_evidence_dict(data: dict) -> SCEvidenceRecord:
    return SCEvidenceRecord(**data)
