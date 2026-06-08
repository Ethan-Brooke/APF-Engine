
"""APF Coherent Materials functional codomain registry.

Architecture-only utility. This module does not register a theorem and does not
create a new APF engine. It is a Tier-4 Coherent Materials Audit Layer adapter
under the Codomain Selection Engine.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterable, List, Mapping, Sequence


class CardStatus(str, Enum):
    ACTIVE_CARD = "ACTIVE_CARD"
    STUB_ONLY_NOT_EXPORTED = "STUB_ONLY_NOT_EXPORTED"


@dataclass(frozen=True)
class EvidenceReceipt:
    receipt_id: str
    description: str
    promotion_role: str = "required"


@dataclass(frozen=True)
class FunctionalCodomainCard:
    codomain_id: str
    label: str
    status: CardStatus
    target_functional_codomain: str
    fragmented_or_competing_codomain: Sequence[str]
    admissible_classifications: Sequence[str]
    required_ledger_slots: Sequence[str]
    core_evidence_receipts: Sequence[EvidenceReceipt]
    burden_channels: Sequence[str]
    intervention_bindings: Sequence[str]
    protocol_bindings: Sequence[str]
    nonclaim_guards: Sequence[str]
    source_case_binding: Mapping[str, str] = field(default_factory=dict)

    @property
    def receipt_ids(self) -> List[str]:
        return [receipt.receipt_id for receipt in self.core_evidence_receipts]

    def missing_receipts(self, supplied_receipts: Iterable[str]) -> List[str]:
        supplied = set(supplied_receipts)
        return [receipt_id for receipt_id in self.receipt_ids if receipt_id not in supplied]

    def receipt_status(self, supplied_receipts: Iterable[str]) -> str:
        missing = self.missing_receipts(supplied_receipts)
        if not missing:
            return "RECEIPT_COMPLETE"
        supplied = set(supplied_receipts)
        if supplied:
            return "RECEIPT_PARTIAL"
        return "RECEIPT_EMPTY"


def _receipt(data: Mapping[str, str]) -> EvidenceReceipt:
    return EvidenceReceipt(
        receipt_id=str(data["receipt_id"]),
        description=str(data["description"]),
        promotion_role=str(data.get("promotion_role", "required")),
    )


def _card(data: Mapping[str, object]) -> FunctionalCodomainCard:
    return FunctionalCodomainCard(
        codomain_id=str(data["codomain_id"]),
        label=str(data["label"]),
        status=CardStatus(str(data["status"])),
        target_functional_codomain=str(data["target_functional_codomain"]),
        fragmented_or_competing_codomain=tuple(str(x) for x in data.get("fragmented_or_competing_codomain", [])),
        admissible_classifications=tuple(str(x) for x in data.get("admissible_classifications", [])),
        required_ledger_slots=tuple(str(x) for x in data.get("required_ledger_slots", [])),
        core_evidence_receipts=tuple(_receipt(x) for x in data.get("core_evidence_receipts", [])),
        burden_channels=tuple(str(x) for x in data.get("burden_channels", [])),
        intervention_bindings=tuple(str(x) for x in data.get("intervention_bindings", [])),
        protocol_bindings=tuple(str(x) for x in data.get("protocol_bindings", [])),
        nonclaim_guards=tuple(str(x) for x in data.get("nonclaim_guards", [])),
        source_case_binding={str(k): str(v) for k, v in dict(data.get("source_case_binding", {})).items()},
    )


_REGISTRY_DATA: Dict[str, object] = {
    "architecture_posture": {
        "formal_layer": "Coherent Materials Audit Layer",
        "engine_placement": "Codomain Selection Engine specialization",
        "tier": "Tier 4 sector adapter / architecture-only utility",
        "is_sixth_engine": False,
        "is_materials_discovery_operating_system": False,
        "apf_mat": "strategic program label only",
    },
    "active_codomain_cards": [
        {
            "codomain_id": "SC_MATERIAL_ADMISSIBILITY",
            "label": "Superconductivity material admissibility",
            "status": "ACTIVE_CARD",
            "target_functional_codomain": "superconducting coherent phase",
            "fragmented_or_competing_codomain": ["normal transport", "phase fragmented", "vortex/mixed phase", "competing electronic order"],
            "admissible_classifications": ["SC_MATERIAL_ADMISSIBLE", "SC_SIGNATURE_PARTIAL", "RESISTIVE_ONLY_NO_MEISSNER", "COMPETING_CODOMAIN_DOMINANT", "MATERIAL_LEDGER_INSUFFICIENT", "CLAIM_QUARANTINED"],
            "required_ledger_slots": ["composition_stoichiometry", "crystal_structure_symmetry_dimensionality", "carrier_or_band_sector", "defect_disorder_impurity_oxygenation_strain", "control_vector_temperature_pressure_field_strain_doping_history", "competing_phase_registry", "measurement_provenance_uncertainty"],
            "core_evidence_receipts": [
                {"receipt_id": "R_SC_RESISTIVITY_ZERO_OR_DROP", "description": "transport transition with declared contacts/current/geometry and uncertainty", "promotion_role": "necessary_not_sufficient"},
                {"receipt_id": "R_SC_MEISSNER_DIAMAGNETIC_RESPONSE", "description": "diamagnetic or Meissner response with background subtraction/provenance", "promotion_role": "required_for_SC_admissible"},
                {"receipt_id": "R_SC_FIELD_SUPPRESSION_OR_CRITICAL_FIELD", "description": "field suppression, Hc1/Hc2, or equivalent field response", "promotion_role": "required_for_SC_admissible"},
                {"receipt_id": "R_SC_REPRODUCIBILITY_SAMPLE_PROVENANCE", "description": "sample provenance, synthesis route, replicate or independent run declaration", "promotion_role": "required_for_SC_admissible"},
                {"receipt_id": "R_SC_PHASE_BOUNDARY_CONTEXT", "description": "temperature/control/history location of transition and phase boundary context", "promotion_role": "required_for_material_phase_claims"},
            ],
            "burden_channels": ["thermal", "disorder", "competing_phase", "dimensionality_phase_stiffness", "synthesis_provenance", "history_hysteresis"],
            "intervention_bindings": ["MEASURE_MEISSNER_RESPONSE", "MAP_PHASE_BOUNDARY", "SWEEP_STRAIN", "SWEEP_PRESSURE", "SWEEP_OXYGENATION", "QUARANTINE_AND_REPRODUCE"],
            "protocol_bindings": ["SC_EVIDENCE_COMPLETION_PROTOCOL", "SC_PHASE_BOUNDARY_MAPPING_PROTOCOL", "CORRELATED_LAYER_PHASE_BOUNDARY_PROTOCOL", "HIGH_PRESSURE_BURDEN_SEPARATION_PROTOCOL", "CLAIM_QUARANTINE_REPLICATION_PROTOCOL"],
            "nonclaim_guards": ["numeric_tc_prediction", "room_temperature_superconductivity_claim", "new_material_prediction", "material_specific_phase_diagram", "ab_initio_chemistry", "resistive_only_promotion"],
        },
        {
            "codomain_id": "RARE_EARTH_QUANTUM_MEMORY",
            "label": "Rare-earth quantum-memory coherent material",
            "status": "ACTIVE_CARD",
            "target_functional_codomain": "optical/spin coherence material for quantum memory",
            "fragmented_or_competing_codomain": ["optically unresolved ensemble", "inhomogeneously broadened ensemble", "unstable/dephasing-dominated host"],
            "admissible_classifications": ["COHERENT_BUT_NOT_SC", "COHERENT_MATERIAL_ADMISSIBLE", "COHERENT_SIGNATURE_PARTIAL", "DEFECT_OR_INHOMOGENEITY_OVERLOADED", "MATERIAL_LEDGER_INSUFFICIENT", "CLAIM_QUARANTINED"],
            "required_ledger_slots": ["composition_stoichiometry", "crystal_structure_site_environment", "rare_earth_ion_identity_and_transition", "homogeneous_linewidth", "inhomogeneous_linewidth", "optical_lifetime", "spin_lifetime_or_spin_coherence_proxy", "spectral_hole_burning_or_photon_echo", "afc_or_memory_protocol_evidence", "stability_synthesis_provenance_uncertainty"],
            "core_evidence_receipts": [
                {"receipt_id": "R_QM_HOMOGENEOUS_LINEWIDTH", "description": "homogeneous linewidth or coherence proxy with method/provenance", "promotion_role": "required_for_QM_admissible_partial"},
                {"receipt_id": "R_QM_INHOMOGENEOUS_LINEWIDTH", "description": "inhomogeneous linewidth / spectral site distribution at cryogenic temperature", "promotion_role": "required_for_burden_typing"},
                {"receipt_id": "R_QM_SPIN_LIFETIME_OR_COHERENCE", "description": "spin lifetime or spin coherence proxy and uncertainty", "promotion_role": "required_for_memory_admissibility"},
                {"receipt_id": "R_QM_SPECTRAL_HOLE_OR_PHOTON_ECHO", "description": "spectral hole burning / photon echo / coherence measurement", "promotion_role": "required_for_coherence_claim"},
                {"receipt_id": "R_QM_AFC_OR_STORAGE_RECEIPT", "description": "AFC/storage efficiency, bandwidth, storage time, or explicit preliminary status", "promotion_role": "required_for_memory_protocol_claim"},
                {"receipt_id": "R_QM_STABILITY_SYNTHESIS_PROVENANCE", "description": "environmental stability, synthesis route, sample handling, provenance", "promotion_role": "required_for_material_route_claim"},
            ],
            "burden_channels": ["inhomogeneous_broadening", "homogeneous_dephasing", "spin_relaxation", "host_stability", "synthesis_defect", "local_environment_variation"],
            "intervention_bindings": ["OPTIMIZE_AFC_EFFICIENCY", "REDUCE_INHOMOGENEITY", "MAP_LINEWIDTH_VS_TEMPERATURE", "MEASURE_PHOTON_ECHO", "STABILIZE_HOST_CHEMISTRY"],
            "protocol_bindings": ["PEARSON_QM_AFC_OPTIMIZATION_PROTOCOL", "BURDEN_REDUCTION_PROTOCOL", "MATERIAL_LEDGER_COMPLETION_PROTOCOL"],
            "nonclaim_guards": ["superconductivity_claim", "numeric_tc_prediction", "room_temperature_superconductivity_claim", "universal_quantum_memory_solution", "device_level_network_demonstration"],
            "source_case_binding": {
                "material": "NaEu(IO3)4",
                "case_type": "Pearson thesis non-SC coherent-material case",
                "classification_binding": "COHERENT_BUT_NOT_SC",
                "subtype": "QUANTUM_MEMORY_MATERIAL_ADMISSIBLE_PARTIAL",
            },
        },
    ],
    "deferred_stub_codomain_cards": [
        {"codomain_id": "SOLID_ION_CONDUCTOR", "status": "STUB_ONLY_NOT_EXPORTED"},
        {"codomain_id": "THERMOELECTRIC", "status": "STUB_ONLY_NOT_EXPORTED"},
        {"codomain_id": "TOPOLOGICAL_MATERIAL", "status": "STUB_ONLY_NOT_EXPORTED"},
        {"codomain_id": "LOW_LOSS_OPTICAL_MATERIAL", "status": "STUB_ONLY_NOT_EXPORTED"},
        {"codomain_id": "MAGNETIC_ORDER_MATERIAL", "status": "STUB_ONLY_NOT_EXPORTED"},
    ],
}


def architecture_posture() -> Mapping[str, object]:
    return dict(_REGISTRY_DATA["architecture_posture"])


def active_cards() -> Dict[str, FunctionalCodomainCard]:
    return {card.codomain_id: card for card in map(_card, _REGISTRY_DATA["active_codomain_cards"])}


def stub_card_ids() -> List[str]:
    return [str(card["codomain_id"]) for card in _REGISTRY_DATA["deferred_stub_codomain_cards"]]


def get_card(codomain_id: str) -> FunctionalCodomainCard:
    cards = active_cards()
    if codomain_id not in cards:
        raise KeyError(f"No active functional codomain card: {codomain_id}")
    return cards[codomain_id]


def receipt_obligation_packet(codomain_id: str, supplied_receipts: Iterable[str]) -> Dict[str, object]:
    """Return a material-specific obligation packet fragment for a codomain card."""
    card = get_card(codomain_id)
    missing = card.missing_receipts(supplied_receipts)
    return {
        "target_engine": "Codomain Selection Engine",
        "target_unit_id": codomain_id,
        "obligation_kind": "MATERIAL_FUNCTIONAL_CODOMAIN_RECEIPTS",
        "current_status": card.receipt_status(supplied_receipts),
        "evidence_required": missing,
        "recommended_next_action": _recommended_action(card, missing),
        "nonclaim_guards": list(card.nonclaim_guards),
    }


def _recommended_action(card: FunctionalCodomainCard, missing_receipts: Sequence[str]) -> str:
    if not missing_receipts:
        return "RECLASSIFY_WITH_COMPLETE_RECEIPTS"
    first = missing_receipts[0]
    if first == "R_SC_MEISSNER_DIAMAGNETIC_RESPONSE":
        return "MEASURE_MEISSNER_RESPONSE"
    if first == "R_SC_FIELD_SUPPRESSION_OR_CRITICAL_FIELD":
        return "MEASURE_FIELD_SUPPRESSION_OR_CRITICAL_FIELD"
    if first == "R_QM_AFC_OR_STORAGE_RECEIPT":
        return "OPTIMIZE_AFC_EFFICIENCY"
    if first == "R_QM_SPECTRAL_HOLE_OR_PHOTON_ECHO":
        return "MEASURE_PHOTON_ECHO_OR_SPECTRAL_HOLE"
    if card.codomain_id == "RARE_EARTH_QUANTUM_MEMORY":
        return "COMPLETE_QM_COHERENCE_RECEIPTS"
    if card.codomain_id == "SC_MATERIAL_ADMISSIBILITY":
        return "COMPLETE_SC_RECEIPTS"
    return "COMPLETE_MATERIAL_RECEIPTS"


def validate_registry() -> List[str]:
    errors: List[str] = []
    posture = architecture_posture()
    if posture.get("is_sixth_engine") is not False:
        errors.append("architecture posture must not declare a sixth engine")
    if posture.get("engine_placement") != "Codomain Selection Engine specialization":
        errors.append("engine placement must be Codomain Selection specialization")
    cards = active_cards()
    for required in ("SC_MATERIAL_ADMISSIBILITY", "RARE_EARTH_QUANTUM_MEMORY"):
        if required not in cards:
            errors.append(f"missing active card {required}")
    for card in cards.values():
        if card.status != CardStatus.ACTIVE_CARD:
            errors.append(f"active registry returned non-active card {card.codomain_id}")
        if not card.required_ledger_slots:
            errors.append(f"{card.codomain_id} has no ledger slots")
        if not card.core_evidence_receipts:
            errors.append(f"{card.codomain_id} has no receipts")
        if not card.nonclaim_guards:
            errors.append(f"{card.codomain_id} has no nonclaim guards")
    return errors
