from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional

CLASSIFICATIONS = {
    "SC_MATERIAL_ADMISSIBLE",
    "COHERENT_BUT_NOT_SC",
    "COHERENT_MATERIAL_ADMISSIBLE",
    "COHERENT_SIGNATURE_PARTIAL",
    "RESISTIVE_ONLY_NO_MEISSNER",
    "DEFECT_OR_INHOMOGENEITY_OVERLOADED",
    "COMPETING_CODOMAIN_DOMINANT",
    "MATERIAL_LEDGER_INSUFFICIENT",
    "CLAIM_QUARANTINED",
}

COHERENCE_TYPES = {
    "superconductivity",
    "quantum_memory",
    "superfluidity",
    "magnetism",
    "BEC",
    "laser",
    "synchronization",
    "topological",
}

@dataclass(frozen=True)
class DiscriminatorResult:
    classification: str
    subtype: str
    selected_codomain: str
    margin: Optional[float]
    exports: Dict[str, int]
    reasons: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "classification": self.classification,
            "subtype": self.subtype,
            "selected_codomain": self.selected_codomain,
            "margin": self.margin,
            "exports": dict(self.exports),
            "reasons": list(self.reasons),
        }

def _truthy(d: Mapping[str, Any], key: str) -> bool:
    return bool(d.get(key, False))

def _num(d: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    value = d.get(key, default)
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

def _margin(ledger: Mapping[str, Any]) -> Optional[float]:
    scores = ledger.get("scores", {}) or {}
    burdens = ledger.get("burdens", {}) or {}
    if not isinstance(scores, Mapping) or not isinstance(burdens, Mapping):
        return None
    fragmented = scores.get("fragmented_or_normal_cost")
    coherent = scores.get("coherent_cost")
    if fragmented is None or coherent is None:
        return None
    return float(fragmented) - float(coherent) - sum(float(x) for x in burdens.values())

def _ledger_complete_enough(ledger: Mapping[str, Any]) -> bool:
    required = ["ledger_id", "material", "coherence_type", "controls", "provenance", "evidence", "burdens"]
    for key in required:
        if key not in ledger:
            return False
    material = ledger.get("material") or {}
    provenance = ledger.get("provenance") or {}
    evidence = ledger.get("evidence") or {}
    return bool(material.get("composition") and material.get("structure_known") is not None and provenance.get("declared") and evidence)

def _exports_base() -> Dict[str, int]:
    return {
        "coherent_materials_discriminator": 1,
        "SC_materials_discriminator": 1,
        "fail_closed_material_claim_ladder": 1,
        "Pearson_quantum_memory_nonSC_case": 0,
        "SC_material_admissible": 0,
        "coherent_material_admissible": 0,
        "SC_numeric_Tc": 0,
        "SC_highTc_solution": 0,
        "SC_ab_initio_chemistry": 0,
        "Pearson_superconductivity_claim": 0,
        "room_temperature_superconductivity_claim": 0,
    }

def classify_material_ledger(ledger: Mapping[str, Any]) -> DiscriminatorResult:
    """Classify a material ledger fail-closed.

    The function does not predict Tc and does not infer superconductivity from formula or family.
    It only evaluates the supplied evidence and provenance ledger.
    """
    reasons: List[str] = []
    exports = _exports_base()
    margin = _margin(ledger)
    claim = ledger.get("claim", {}) or {}
    evidence = ledger.get("evidence", {}) or {}
    burdens = ledger.get("burdens", {}) or {}
    codomain = ledger.get("codomain", {}) or {}
    coherence_type = ledger.get("coherence_type")

    extraordinary = bool(claim.get("extraordinary", False))
    missing_provenance = not bool((ledger.get("provenance", {}) or {}).get("declared", False))
    if claim.get("quarantine", False) or (extraordinary and missing_provenance):
        reasons.append("extraordinary_or_flagged_claim_without_required_provenance")
        return DiscriminatorResult(
            "CLAIM_QUARANTINED",
            "fail_closed_claim_hygiene",
            "R_quarantine",
            margin,
            exports,
            reasons,
        )

    if not _ledger_complete_enough(ledger):
        reasons.append("required_material_or_evidence_ledger_slots_missing")
        return DiscriminatorResult(
            "MATERIAL_LEDGER_INSUFFICIENT",
            "ledger_incomplete",
            "R_ledger_insufficient",
            margin,
            exports,
            reasons,
        )

    if coherence_type not in COHERENCE_TYPES:
        reasons.append("unknown_or_undeclared_coherence_type")
        return DiscriminatorResult(
            "MATERIAL_LEDGER_INSUFFICIENT",
            "unknown_coherence_type",
            "R_ledger_insufficient",
            margin,
            exports,
            reasons,
        )

    dominant = codomain.get("dominant")
    if dominant and dominant not in {"R_SC", "R_memory_admissible", "R_coherent", "R_topological"}:
        reasons.append(f"competing_codomain_selected:{dominant}")
        return DiscriminatorResult(
            "COMPETING_CODOMAIN_DOMINANT",
            str(dominant),
            str(dominant),
            margin,
            exports,
            reasons,
        )

    # High burden fail-closed, with an explicit exception for useful inhomogeneous bandwidth in AFC-like ledgers.
    total_burden = sum(float(v) for v in burdens.values())
    inhom = float(burdens.get("inhomogeneity", 0.0))
    disorder = float(burdens.get("disorder", 0.0))
    synthesis = float(burdens.get("synthesis", 0.0))
    stability = float(burdens.get("stability", 0.0))
    ion_interaction = float(burdens.get("ion_interaction", 0.0))
    afc_resource = bool(evidence.get("afc_retrieval", False)) and coherence_type == "quantum_memory"
    if (disorder + synthesis + stability + ion_interaction) >= 1.7 or (inhom >= 1.2 and not afc_resource):
        reasons.append("defect_inhomogeneity_stability_or_synthesis_burden_over_threshold")
        return DiscriminatorResult(
            "DEFECT_OR_INHOMOGENEITY_OVERLOADED",
            "material_burden_overloaded",
            "R_fragmented_or_unresolved",
            margin,
            exports,
            reasons,
        )

    if coherence_type == "superconductivity":
        zero_r = _truthy(evidence, "zero_resistance") or _truthy(evidence, "resistive_transition")
        meissner = _truthy(evidence, "meissner") or _truthy(evidence, "diamagnetic_response")
        field_supp = _truthy(evidence, "field_suppression") or _truthy(evidence, "critical_field_response")
        repro = _truthy(evidence, "reproducible")
        phase = _truthy(evidence, "phase_coherence") or _truthy(evidence, "heat_capacity_or_phase_evidence")
        if zero_r and not meissner:
            reasons.append("resistive_transition_without_meissner_or_diamagnetic_evidence")
            return DiscriminatorResult(
                "RESISTIVE_ONLY_NO_MEISSNER",
                "SC_signature_partial_resistive_only",
                "R_resistive_only",
                margin,
                exports,
                reasons,
            )
        if zero_r and meissner and field_supp and repro and phase and (margin is None or margin > 0):
            exports["SC_material_admissible"] = 1
            reasons.append("SC_evidence_package_complete")
            return DiscriminatorResult(
                "SC_MATERIAL_ADMISSIBLE",
                "SC_evidence_package_complete_no_Tc_prediction",
                "R_SC",
                margin,
                exports,
                reasons,
            )
        reasons.append("SC_evidence_package_partial")
        return DiscriminatorResult(
            "COHERENT_SIGNATURE_PARTIAL",
            "SC_signature_partial",
            "R_SC_candidate_partial",
            margin,
            exports,
            reasons,
        )

    if coherence_type == "quantum_memory":
        h_khz = _num(evidence, "homogeneous_linewidth_kHz", default=1e9)
        inh_ghz = _num(evidence, "inhomogeneous_linewidth_GHz", default=1e9)
        spin_s = _num(evidence, "spin_lifetime_s", default=0.0)
        spectral_holes = _truthy(evidence, "spectral_hole_burning")
        afc = _truthy(evidence, "afc_retrieval")
        stable = _truthy(evidence, "environmentally_stable")
        no_sc = not (_truthy(evidence, "zero_resistance") or _truthy(evidence, "meissner"))
        strong_qm = h_khz <= 200.0 and inh_ghz <= 3.0 and spin_s >= 1.0 and spectral_holes and afc and stable
        if strong_qm and no_sc and (margin is None or margin > 0):
            exports["Pearson_quantum_memory_nonSC_case"] = 1 if ledger.get("source_key") == "pearson_dissertation_2025" else 0
            exports["coherent_material_admissible"] = 1
            reasons.append("quantum_memory_coherence_evidence_present_no_SC_evidence")
            return DiscriminatorResult(
                "COHERENT_BUT_NOT_SC",
                "QUANTUM_MEMORY_MATERIAL_ADMISSIBLE_PARTIAL",
                "R_memory_admissible",
                margin,
                exports,
                reasons,
            )
        if h_khz < 1000.0 or spectral_holes or afc:
            reasons.append("quantum_memory_signature_partial")
            return DiscriminatorResult(
                "COHERENT_SIGNATURE_PARTIAL",
                "quantum_memory_signature_partial",
                "R_memory_candidate_partial",
                margin,
                exports,
                reasons,
            )
        reasons.append("quantum_memory_coherence_evidence_insufficient")
        return DiscriminatorResult(
            "DEFECT_OR_INHOMOGENEITY_OVERLOADED" if total_burden > 1.5 else "COHERENT_SIGNATURE_PARTIAL",
            "quantum_memory_burden_or_signature_insufficient",
            "R_fragmented_or_unresolved",
            margin,
            exports,
            reasons,
        )

    # Other coherent regimes: generic positive-margin path.
    if margin is not None and margin > 0 and evidence.get("coherence_signature", False):
        exports["coherent_material_admissible"] = 1
        reasons.append("generic_coherent_regime_positive_margin_and_signature")
        return DiscriminatorResult(
            "COHERENT_MATERIAL_ADMISSIBLE",
            f"{coherence_type}_coherent_regime",
            "R_coherent",
            margin,
            exports,
            reasons,
        )

    reasons.append("generic_coherent_regime_signature_partial")
    return DiscriminatorResult(
        "COHERENT_SIGNATURE_PARTIAL",
        f"{coherence_type}_signature_partial",
        "R_coherent_candidate_partial",
        margin,
        exports,
        reasons,
    )
