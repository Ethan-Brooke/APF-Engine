
"""CMAL casebook utility.

Architecture-only utility. This module does not register bank checks and does
not create a new APF engine. It collects material case cards for the Coherent
Materials Audit Layer (CMAL), which remains a Codomain Selection specialization.

The casebook is intentionally not a public-ingestion bridge and not a material
prediction engine. It turns the existing CMAL discriminator / intervention /
protocol / receipt-update loop into one-page audit cards that preserve
non-claims.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

from apf.coherent_materials_discriminator import classify_material_ledger
from apf.coherent_materials_obligation_packet_adapter import compile_materials_obligation_packet_from_ledger, packet_to_dict

NONCLAIM_LEDGER: Dict[str, int] = {
    "APF_Mat_sixth_engine": 0,
    "materials_discovery_OS_architecture": 0,
    "Atlas_MATERIALS_axis": 0,
    "materials_public_ingestion_core_engine": 0,
    "autonomous_lab_execution": 0,
    "SC_numeric_Tc_prediction": 0,
    "SC_new_material_prediction": 0,
    "SC_material_specific_phase_diagram": 0,
    "SC_highTc_solution": 0,
    "SC_ab_initio_chemistry": 0,
    "Pearson_superconductivity_claim": 0,
    "room_temperature_superconductivity_claim": 0,
}

@dataclass(frozen=True)
class MaterialCaseCard:
    case_id: str
    title: str
    family: str
    target_codomain: str
    classification: str
    update_status: str
    protocol: str
    top_action: str
    dominant_burden: str
    active_lane: bool
    stub_only: bool
    source_basis: str
    receipt_slots: Tuple[str, ...]
    nonclaims: Tuple[str, ...]
    ledger: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "title": self.title,
            "family": self.family,
            "target_codomain": self.target_codomain,
            "classification": self.classification,
            "update_status": self.update_status,
            "protocol": self.protocol,
            "top_action": self.top_action,
            "dominant_burden": self.dominant_burden,
            "active_lane": self.active_lane,
            "stub_only": self.stub_only,
            "source_basis": self.source_basis,
            "receipt_slots": list(self.receipt_slots),
            "nonclaims": list(self.nonclaims),
            "ledger": deepcopy(dict(self.ledger)),
        }

_CASE_DATA: Tuple[Dict[str, Any], ...] = ({'case_id': 'SC_CONTROL_BULK_COMPLETE', 'title': 'Bulk superconductivity control — complete evidence package', 'family': 'superconductivity_control', 'target_codomain': 'SC_MATERIAL_ADMISSIBILITY', 'classification': 'SC_MATERIAL_ADMISSIBLE', 'update_status': 'PROMOTE_CODOMAIN', 'protocol': 'SC_PHASE_BOUNDARY_MAPPING_PROTOCOL', 'top_action': 'MAP_PHASE_BOUNDARY', 'dominant_burden': 'low_burden_control', 'active_lane': True, 'stub_only': False, 'source_basis': 'template_control_no_specific_material_claim', 'receipt_slots': ['R_SC_RESISTIVITY_ZERO_OR_DROP', 'R_SC_MEISSNER_DIAMAGNETIC_RESPONSE', 'R_SC_FIELD_SUPPRESSION_OR_CRITICAL_FIELD', 'R_SC_REPRODUCIBILITY_SAMPLE_PROVENANCE', 'R_SC_PHASE_BOUNDARY_CONTEXT'], 'nonclaims': ['numeric_Tc_prediction', 'new_material_prediction', 'material_specific_phase_diagram'], 'ledger': {'ledger_id': 'case_sc_control_bulk_complete', 'material': {'composition': 'known_bulk_SC_control_template', 'structure_known': True, 'family': 'superconductivity_control'}, 'coherence_type': 'superconductivity', 'codomain': {'dominant': 'R_SC'}, 'controls': {'temperature_K': 'below_transition', 'pressure_GPa': 0, 'field_T': 0, 'history': 'declared'}, 'evidence': {'zero_resistance': True, 'meissner': True, 'field_suppression': True, 'reproducible': True, 'phase_coherence': True, 'sigma_declared': True}, 'burdens': {'thermal': 0.05, 'disorder': 0.05, 'competition': 0.05, 'dimensionality': 0.05, 'synthesis': 0.05, 'history': 0.0}, 'scores': {'fragmented_or_normal_cost': 2.0, 'coherent_cost': 0.5}, 'provenance': {'declared': True, 'casebook_template': True}, 'claim': {'extraordinary': False, 'quarantine': False}}}, {'case_id': 'SC_RESISTIVE_ONLY_QUARANTINE', 'title': 'Resistive-only superconductivity claim — no Meissner receipt', 'family': 'superconductivity_claim_audit', 'target_codomain': 'SC_MATERIAL_ADMISSIBILITY', 'classification': 'RESISTIVE_ONLY_NO_MEISSNER', 'update_status': 'REQUEST_NEXT_RECEIPT', 'protocol': 'SC_EVIDENCE_COMPLETION_PROTOCOL', 'top_action': 'MEASURE_MEISSNER_RESPONSE', 'dominant_burden': 'missing_bulk_SC_receipts', 'active_lane': True, 'stub_only': False, 'source_basis': 'claim_hygiene_template', 'receipt_slots': ['R_SC_RESISTIVITY_ZERO_OR_DROP', 'R_SC_MEISSNER_DIAMAGNETIC_RESPONSE', 'R_SC_FIELD_SUPPRESSION_OR_CRITICAL_FIELD', 'R_SC_REPRODUCIBILITY_SAMPLE_PROVENANCE', 'R_SC_PHASE_BOUNDARY_CONTEXT'], 'nonclaims': ['SC_material_admissible', 'numeric_Tc_prediction', 'room_temperature_superconductivity_claim'], 'ledger': {'ledger_id': 'case_sc_resistive_only_quarantine', 'material': {'composition': 'unspecified_resistive_claim', 'structure_known': True, 'family': 'superconductivity_claim_audit'}, 'coherence_type': 'superconductivity', 'codomain': {'dominant': 'R_SC'}, 'controls': {'temperature_K': 'claimed_transition', 'pressure_GPa': 0, 'field_T': 0, 'history': 'declared'}, 'evidence': {'zero_resistance': True, 'resistive_transition': True, 'meissner': False, 'field_suppression': False, 'reproducible': False, 'phase_coherence': False}, 'burdens': {'thermal': 0.1, 'disorder': 0.2, 'competition': 0.1, 'dimensionality': 0.1, 'synthesis': 0.2, 'history': 0.2}, 'scores': {'fragmented_or_normal_cost': 1.2, 'coherent_cost': 0.8}, 'provenance': {'declared': True, 'casebook_template': True}, 'claim': {'extraordinary': False, 'quarantine': False}}}, {'case_id': 'PEARSON_NAEU_QM_POSITIVE', 'title': 'Pearson NaEu(IO3)4 — rare-earth quantum-memory coherent material', 'family': 'stoichiometric_rare_earth_quantum_memory', 'target_codomain': 'RARE_EARTH_QUANTUM_MEMORY', 'classification': 'COHERENT_BUT_NOT_SC', 'update_status': 'PROMOTE_CODOMAIN', 'protocol': 'PEARSON_QM_AFC_OPTIMIZATION_PROTOCOL', 'top_action': 'OPTIMIZE_AFC_EFFICIENCY', 'dominant_burden': 'inhomogeneous_broadening_vs_optical_depth_tradeoff', 'active_lane': True, 'stub_only': False, 'source_basis': 'Pearson dissertation 2025, NaEu(IO3)4 Chapter 7', 'receipt_slots': ['R_QM_HOMOGENEOUS_LINEWIDTH', 'R_QM_INHOMOGENEOUS_LINEWIDTH', 'R_QM_SPIN_LIFETIME_OR_COHERENCE', 'R_QM_SPECTRAL_HOLE_OR_PHOTON_ECHO', 'R_QM_AFC_OR_STORAGE_RECEIPT', 'R_QM_STABILITY_SYNTHESIS_PROVENANCE'], 'nonclaims': ['Pearson_superconductivity_claim', 'universal_quantum_memory_solution', 'device_level_network_demonstration'], 'ledger': {'ledger_id': 'case_pearson_naeu_io3_4_qm', 'source_key': 'pearson_dissertation_2025', 'material': {'composition': 'NaEu(IO3)4', 'structure_known': True, 'family': 'stoichiometric_rare_earth_quantum_memory', 'structure_note': '2D layered monoclinic Cc; Eu site C1'}, 'coherence_type': 'quantum_memory', 'codomain': {'dominant': 'R_memory_admissible'}, 'controls': {'temperature_K': 1.7, 'pressure_GPa': 0, 'field_T': 0, 'history': 'Pearson thesis Chapter 7'}, 'evidence': {'homogeneous_linewidth_kHz': 120, 'inhomogeneous_linewidth_GHz': 2.2, 'spin_lifetime_s': 2.0, 'spectral_hole_burning': True, 'photon_echo': True, 'afc_retrieval': True, 'afc_storage_ns': [300, 400, 500, 600, 700, 800], 'afc_max_efficiency_percent': 2.0, 'environmentally_stable': True, 'zero_resistance': False, 'meissner': False}, 'burdens': {'thermal': 0.05, 'disorder': 0.15, 'inhomogeneity': 0.45, 'synthesis': 0.15, 'stability': 0.05, 'history': 0.05}, 'scores': {'fragmented_or_normal_cost': 2.0, 'coherent_cost': 0.45}, 'provenance': {'declared': True, 'source': 'PEARSONJR-DISSERTATION-2025.pdf'}, 'claim': {'extraordinary': False, 'quarantine': False}}}, {'case_id': 'PEARSON_CAUTIONS_BURDEN', 'title': 'Pearson caution materials — EF/EF·FA, Eu(IO3)3, EuAl3(BO3)4 burden card', 'family': 'rare_earth_qm_caution_materials', 'target_codomain': 'RARE_EARTH_QUANTUM_MEMORY', 'classification': 'DEFECT_OR_INHOMOGENEITY_OVERLOADED', 'update_status': 'DEMOTE_CLAIM', 'protocol': 'BURDEN_REDUCTION_PROTOCOL', 'top_action': 'REDUCE_INHOMOGENEITY_OR_STABILITY_BURDEN', 'dominant_burden': 'stability_synthesis_inhomogeneity', 'active_lane': True, 'stub_only': False, 'source_basis': 'Pearson dissertation 2025 Chapters 6 and 8 caution/follow-up materials', 'receipt_slots': ['R_QM_HOMOGENEOUS_LINEWIDTH', 'R_QM_INHOMOGENEOUS_LINEWIDTH', 'R_QM_SPIN_LIFETIME_OR_COHERENCE', 'R_QM_SPECTRAL_HOLE_OR_PHOTON_ECHO', 'R_QM_AFC_OR_STORAGE_RECEIPT', 'R_QM_STABILITY_SYNTHESIS_PROVENANCE'], 'nonclaims': ['QM_material_admissible', 'Pearson_superconductivity_claim'], 'ledger': {'ledger_id': 'case_pearson_caution_materials_burden', 'source_key': 'pearson_dissertation_2025', 'material': {'composition': 'EF/EF.FA + Eu(IO3)3 + EuAl3(BO3)4 caution family', 'structure_known': True, 'family': 'rare_earth_qm_caution_materials'}, 'coherence_type': 'quantum_memory', 'codomain': {'dominant': 'R_memory_admissible'}, 'controls': {'temperature_K': 1.7, 'pressure_GPa': 0, 'field_T': 0, 'history': 'Pearson survey/follow-up'}, 'evidence': {'homogeneous_linewidth_kHz': 1000, 'inhomogeneous_linewidth_GHz': 8.0, 'spin_lifetime_s': 0.0, 'spectral_hole_burning': False, 'afc_retrieval': False, 'environmentally_stable': False, 'zero_resistance': False, 'meissner': False}, 'burdens': {'thermal': 0.1, 'disorder': 0.4, 'inhomogeneity': 0.8, 'ion_interaction': 0.5, 'synthesis': 0.7, 'stability': 0.8, 'history': 0.1}, 'scores': {'fragmented_or_normal_cost': 1.2, 'coherent_cost': 0.7}, 'provenance': {'declared': True, 'source': 'PEARSONJR-DISSERTATION-2025.pdf'}, 'claim': {'extraordinary': False, 'quarantine': False}}}, {'case_id': 'CORRELATED_LAYER_NICKELATE_TEMPLATE', 'title': 'Nickelate-style correlated layer — strain/pressure/oxygenation phase-boundary scout', 'family': 'correlated_layer_superconductivity_template', 'target_codomain': 'SC_MATERIAL_ADMISSIBILITY', 'classification': 'COHERENT_SIGNATURE_PARTIAL', 'update_status': 'UPDATE_PHASE_BOUNDARY_MAP', 'protocol': 'CORRELATED_LAYER_PHASE_BOUNDARY_PROTOCOL', 'top_action': 'SWEEP_STRAIN_PRESSURE_OXYGENATION_HISTORY', 'dominant_burden': 'SC_vs_AFM_CDW_stripe_pseudogap_competition', 'active_lane': True, 'stub_only': False, 'source_basis': 'generic correlated-layer template; no nickelate result claimed', 'receipt_slots': ['R_SC_RESISTIVITY_ZERO_OR_DROP', 'R_SC_MEISSNER_DIAMAGNETIC_RESPONSE', 'R_SC_FIELD_SUPPRESSION_OR_CRITICAL_FIELD', 'R_SC_REPRODUCIBILITY_SAMPLE_PROVENANCE', 'R_SC_PHASE_BOUNDARY_CONTEXT', 'R_PHASE_BOUNDARY_STRAIN_PRESSURE_OXYGENATION_SWEEP'], 'nonclaims': ['new_material_prediction', 'numeric_Tc_prediction', 'nickelate_specific_phase_diagram'], 'ledger': {'ledger_id': 'case_correlated_layer_nickelate_template', 'material': {'composition': 'generic_layered_nickelate_template', 'structure_known': True, 'family': 'correlated_layer_superconductivity_template'}, 'coherence_type': 'superconductivity', 'codomain': {'dominant': 'R_SC'}, 'controls': {'temperature_K': 20, 'pressure_GPa': 'sweep', 'field_T': 0, 'strain': 'sweep', 'oxygenation': 'sweep', 'history': 'declared'}, 'evidence': {'zero_resistance': True, 'meissner': False, 'field_suppression': False, 'reproducible': True, 'phase_coherence': False, 'phase_boundary_receipts': True}, 'burdens': {'thermal': 0.2, 'disorder': 0.1, 'competition': 1.0, 'dimensionality': 0.2, 'synthesis': 0.1, 'history': 0.0}, 'scores': {'fragmented_or_normal_cost': 1.8, 'coherent_cost': 0.7}, 'provenance': {'declared': True, 'casebook_template': True}, 'claim': {'extraordinary': False, 'quarantine': False}}}, {'case_id': 'HYDRIDE_PRESSURE_CONDITIONED', 'title': 'High-pressure hydride — pressure-conditioned SC, ambient usability not promoted', 'family': 'hydride_high_pressure_superconductivity_template', 'target_codomain': 'SC_MATERIAL_ADMISSIBILITY', 'classification': 'SC_MATERIAL_ADMISSIBLE', 'update_status': 'PROMOTE_PRESSURE_CONDITIONED_SC', 'protocol': 'HIGH_PRESSURE_BURDEN_SEPARATION_PROTOCOL', 'top_action': 'SEPARATE_HIGH_PRESSURE_SC_FROM_AMBIENT_USABILITY', 'dominant_burden': 'pressure_synthesis_stability', 'active_lane': True, 'stub_only': False, 'source_basis': 'generic high-pressure hydride template; no specific hydride result claimed', 'receipt_slots': ['R_SC_RESISTIVITY_ZERO_OR_DROP', 'R_SC_MEISSNER_DIAMAGNETIC_RESPONSE', 'R_SC_FIELD_SUPPRESSION_OR_CRITICAL_FIELD', 'R_SC_REPRODUCIBILITY_SAMPLE_PROVENANCE', 'R_SC_PHASE_BOUNDARY_CONTEXT', 'R_PRESSURE_CONDITION_DECLARED', 'R_AMBIENT_RELEASE_TEST'], 'nonclaims': ['ambient_superconductivity_from_pressure_only', 'room_temperature_superconductivity_claim', 'new_material_prediction'], 'ledger': {'ledger_id': 'case_hydride_pressure_conditioned', 'material': {'composition': 'generic_high_pressure_hydride_template', 'structure_known': True, 'family': 'hydride_high_pressure_superconductivity_template'}, 'coherence_type': 'superconductivity', 'codomain': {'dominant': 'R_SC'}, 'controls': {'temperature_K': 150, 'pressure_GPa': 150, 'field_T': 0, 'history': 'pressure-conditioned'}, 'evidence': {'zero_resistance': True, 'meissner': True, 'field_suppression': True, 'reproducible': True, 'phase_coherence': True, 'pressure_conditioned': True, 'ambient_retained': False}, 'burdens': {'thermal': 0.1, 'disorder': 0.05, 'competition': 0.05, 'dimensionality': 0.05, 'synthesis': 0.1, 'history': 0.05}, 'scores': {'fragmented_or_normal_cost': 2.4, 'coherent_cost': 0.6}, 'provenance': {'declared': True, 'casebook_template': True}, 'claim': {'extraordinary': False, 'quarantine': False}}}, {'case_id': 'CUPRATE_STRIPE_PSEUDOGAP_COMPETITION', 'title': 'Cuprate-style correlated layer — SC/stripe/CDW/pseudogap/vortex competition card', 'family': 'cuprate_correlated_layer_template', 'target_codomain': 'SC_MATERIAL_ADMISSIBILITY', 'classification': 'COMPETING_CODOMAIN_DOMINANT', 'update_status': 'UPDATE_PHASE_BOUNDARY_MAP', 'protocol': 'CORRELATED_LAYER_PHASE_BOUNDARY_PROTOCOL', 'top_action': 'MAP_DOPING_FIELD_STRAIN_VORTEX_REGIME', 'dominant_burden': 'stripe_CDW_pseudogap_vortex_competition', 'active_lane': True, 'stub_only': False, 'source_basis': 'generic cuprate/correlated-layer competition template; no material phase diagram claimed', 'receipt_slots': ['R_SC_RESISTIVITY_ZERO_OR_DROP', 'R_SC_MEISSNER_DIAMAGNETIC_RESPONSE', 'R_SC_FIELD_SUPPRESSION_OR_CRITICAL_FIELD', 'R_SC_REPRODUCIBILITY_SAMPLE_PROVENANCE', 'R_SC_PHASE_BOUNDARY_CONTEXT', 'R_COMPETING_ORDER_MAP', 'R_VORTEX_OR_FIELD_DEPENDENCE_MAP'], 'nonclaims': ['cuprate_mechanism_solution', 'numeric_Tc_prediction', 'material_specific_phase_diagram'], 'ledger': {'ledger_id': 'case_cuprate_stripe_pseudogap_competition', 'material': {'composition': 'generic_cuprate_template', 'structure_known': True, 'family': 'cuprate_correlated_layer_template'}, 'coherence_type': 'superconductivity', 'codomain': {'dominant': 'R_pseudogap'}, 'controls': {'temperature_K': 'sweep', 'pressure_GPa': 0, 'field_T': 'sweep', 'doping': 'sweep', 'history': 'declared'}, 'evidence': {'zero_resistance': False, 'meissner': False, 'field_suppression': False, 'reproducible': True, 'phase_coherence': False, 'competing_order_map': True}, 'burdens': {'thermal': 0.2, 'disorder': 0.15, 'competition': 1.4, 'dimensionality': 0.25, 'synthesis': 0.1, 'history': 0.1}, 'scores': {'fragmented_or_normal_cost': 1.5, 'coherent_cost': 1.0}, 'provenance': {'declared': True, 'casebook_template': True}, 'claim': {'extraordinary': False, 'quarantine': False}}}, {'case_id': 'TOPOLOGICAL_INTERFACE_STUB', 'title': 'Topological/interface material — future codomain stub, no active export', 'family': 'topological_interface_material_stub', 'target_codomain': 'TOPOLOGICAL_MATERIAL', 'classification': 'MATERIAL_LEDGER_INSUFFICIENT', 'update_status': 'REQUEST_NEXT_RECEIPT', 'protocol': 'FUTURE_CODOMAIN_STUB_PROTOCOL', 'top_action': 'DEFINE_RECEIPT_CARD_BEFORE_ADMISSION', 'dominant_burden': 'codomain_receipt_card_not_exported', 'active_lane': False, 'stub_only': True, 'source_basis': 'future-slot stub under functional codomain registry; not exported', 'receipt_slots': ['R_TOPOLOGICAL_BULK_INVARIANT', 'R_EDGE_STATE_OR_INTERFACE_SIGNATURE', 'R_TRIVIAL_PHASE_CONTROL'], 'nonclaims': ['topological_material_admissible', 'new_material_prediction'], 'ledger': {'ledger_id': 'case_topological_interface_stub', 'material': {'composition': 'generic_topological_interface_stub', 'structure_known': True, 'family': 'topological_interface_material_stub'}, 'coherence_type': 'topological', 'codomain': {'dominant': 'R_topological'}, 'controls': {'temperature_K': 'declared', 'pressure_GPa': 0, 'field_T': 'declared', 'history': 'stub'}, 'evidence': {}, 'burdens': {'thermal': 0.1, 'disorder': 0.2, 'competition': 0.2, 'synthesis': 0.2, 'history': 0.1}, 'scores': {'fragmented_or_normal_cost': 1.0, 'coherent_cost': 0.8}, 'provenance': {'declared': True, 'casebook_template': True}, 'claim': {'extraordinary': False, 'quarantine': False}}}, {'case_id': 'THERMOELECTRIC_STUB', 'title': 'Thermoelectric material — future functional codomain stub', 'family': 'thermoelectric_material_stub', 'target_codomain': 'THERMOELECTRIC_FUNCTIONAL_MATERIAL', 'classification': 'MATERIAL_LEDGER_INSUFFICIENT', 'update_status': 'REQUEST_NEXT_RECEIPT', 'protocol': 'FUTURE_CODOMAIN_STUB_PROTOCOL', 'top_action': 'DEFINE_ZT_THERMAL_ELECTRICAL_RECEIPT_CARD', 'dominant_burden': 'codomain_receipt_card_not_exported', 'active_lane': False, 'stub_only': True, 'source_basis': 'future-slot stub under functional codomain registry; not exported', 'receipt_slots': ['R_ZT_WITH_UNCERTAINTY', 'R_THERMAL_CONDUCTIVITY', 'R_SEEBECK_ELECTRICAL_CONDUCTIVITY', 'R_STABILITY_WINDOW'], 'nonclaims': ['thermoelectric_material_admissible', 'device_performance_prediction'], 'ledger': {'ledger_id': 'case_thermoelectric_stub', 'material': {'composition': 'generic_thermoelectric_stub', 'structure_known': True, 'family': 'thermoelectric_material_stub'}, 'coherence_type': 'thermoelectric_stub', 'codomain': {'dominant': 'R_functional_material'}, 'controls': {'temperature_K': 'declared', 'pressure_GPa': 0, 'field_T': 0, 'history': 'stub'}, 'evidence': {}, 'burdens': {'thermal': 0.2, 'disorder': 0.2, 'competition': 0.1, 'synthesis': 0.2, 'history': 0.1}, 'scores': {'fragmented_or_normal_cost': 1.0, 'coherent_cost': 0.9}, 'provenance': {'declared': True, 'casebook_template': True}, 'claim': {'extraordinary': False, 'quarantine': False}}}, {'case_id': 'ION_CONDUCTOR_STUB', 'title': 'Battery ion conductor — future functional codomain stub', 'family': 'ion_conductor_material_stub', 'target_codomain': 'BATTERY_ION_CONDUCTOR', 'classification': 'MATERIAL_LEDGER_INSUFFICIENT', 'update_status': 'REQUEST_NEXT_RECEIPT', 'protocol': 'FUTURE_CODOMAIN_STUB_PROTOCOL', 'top_action': 'DEFINE_IONIC_CONDUCTIVITY_STABILITY_RECEIPT_CARD', 'dominant_burden': 'codomain_receipt_card_not_exported', 'active_lane': False, 'stub_only': True, 'source_basis': 'future-slot stub under functional codomain registry; not exported', 'receipt_slots': ['R_IONIC_CONDUCTIVITY', 'R_ELECTRONIC_LEAKAGE', 'R_ELECTROCHEMICAL_STABILITY', 'R_SYNTHESIS_REPRODUCIBILITY'], 'nonclaims': ['battery_material_admissible', 'device_performance_prediction'], 'ledger': {'ledger_id': 'case_ion_conductor_stub', 'material': {'composition': 'generic_ion_conductor_stub', 'structure_known': True, 'family': 'ion_conductor_material_stub'}, 'coherence_type': 'ion_conductor_stub', 'codomain': {'dominant': 'R_functional_material'}, 'controls': {'temperature_K': 'declared', 'pressure_GPa': 0, 'field_T': 0, 'history': 'stub'}, 'evidence': {}, 'burdens': {'thermal': 0.2, 'disorder': 0.3, 'competition': 0.1, 'synthesis': 0.3, 'history': 0.1}, 'scores': {'fragmented_or_normal_cost': 1.0, 'coherent_cost': 0.9}, 'provenance': {'declared': True, 'casebook_template': True}, 'claim': {'extraordinary': False, 'quarantine': False}}})

def load_case_cards() -> Tuple[MaterialCaseCard, ...]:
    """Return the ten CMAL case cards in deterministic order."""
    cards: List[MaterialCaseCard] = []
    for raw in _CASE_DATA:
        cards.append(MaterialCaseCard(
            case_id=str(raw["case_id"]),
            title=str(raw["title"]),
            family=str(raw["family"]),
            target_codomain=str(raw["target_codomain"]),
            classification=str(raw["classification"]),
            update_status=str(raw["update_status"]),
            protocol=str(raw["protocol"]),
            top_action=str(raw["top_action"]),
            dominant_burden=str(raw["dominant_burden"]),
            active_lane=bool(raw["active_lane"]),
            stub_only=bool(raw["stub_only"]),
            source_basis=str(raw["source_basis"]),
            receipt_slots=tuple(str(x) for x in raw["receipt_slots"]),
            nonclaims=tuple(str(x) for x in raw["nonclaims"]),
            ledger=deepcopy(raw["ledger"]),
        ))
    return tuple(cards)

def summarize_casebook(cards: Sequence[MaterialCaseCard] | None = None) -> Dict[str, Any]:
    """Summarize the casebook without adding a bank theorem or new engine."""
    if cards is None:
        cards = load_case_cards()
    active = [c for c in cards if c.active_lane]
    stubs = [c for c in cards if c.stub_only]
    by_class: Dict[str, int] = {}
    for c in cards:
        by_class[c.classification] = by_class.get(c.classification, 0) + 1
    return {
        "case_count": len(cards),
        "active_lane_count": len(active),
        "stub_count": len(stubs),
        "active_targets": sorted(set(c.target_codomain for c in active)),
        "stub_targets": sorted(set(c.target_codomain for c in stubs)),
        "classification_counts": by_class,
        "nonclaims": dict(NONCLAIM_LEDGER),
        "architecture": {
            "CMAL_under_Codomain_Selection": 1,
            "APF_Mat_sixth_engine": 0,
            "materials_discovery_OS_architecture": 0,
            "Atlas_MATERIALS_axis": 0,
        },
    }

def run_casebook_roundtrip(cards: Sequence[MaterialCaseCard] | None = None) -> Dict[str, Dict[str, Any]]:
    """Run each non-stub case through CMAL classification and obligation compilation.

    Future codomain stubs are intentionally not pushed through the discriminator,
    because their receipt cards are not exported yet. They are returned as
    STUB_ONLY_NOT_EXPORTED entries.
    """
    if cards is None:
        cards = load_case_cards()
    results: Dict[str, Dict[str, Any]] = {}
    for card in cards:
        if card.stub_only:
            results[card.case_id] = {
                "case_id": card.case_id,
                "classification": card.classification,
                "expected_classification": card.classification,
                "update_status": card.update_status,
                "protocol": card.protocol,
                "top_action": card.top_action,
                "stub_only": True,
                "exports": {"future_codomain_stub_only_not_exported": 1},
                "nonclaims": dict(NONCLAIM_LEDGER),
            }
            continue
        disc = classify_material_ledger(card.ledger)
        packet = packet_to_dict(compile_materials_obligation_packet_from_ledger(card.ledger))
        results[card.case_id] = {
            "case_id": card.case_id,
            "classification": disc.classification,
            "expected_classification": card.classification,
            "subtype": disc.subtype,
            "selected_codomain": disc.selected_codomain,
            "protocol": card.protocol,
            "top_action": card.top_action,
            "dominant_burden": card.dominant_burden,
            "obligation_kind": packet.get("obligation_kind"),
            "evidence_required": packet.get("evidence_required", []),
            "recommended_next_action": packet.get("recommended_next_action"),
            "exports": dict(disc.exports),
            "nonclaims": dict(NONCLAIM_LEDGER),
            "reasons": list(disc.reasons),
            "stub_only": False,
        }
    return results

def casebook_exports() -> Dict[str, int]:
    """Exports promoted by the casebook pack."""
    return {
        "CMAL_casebook": 1,
        "CMAL_material_card_template": 1,
        "CMAL_casebook_roundtrip_summary": 1,
        "CMAL_two_active_hero_lanes": 1,
        "CMAL_future_codomain_stub_cards": 1,
        "CMAL_receipt_update_loop_preserved": 1,
        "APF_Mat_strategic_program_label": 1,
        "APF_Mat_sixth_engine": 0,
        "materials_discovery_OS_architecture": 0,
        "Atlas_MATERIALS_axis": 0,
    }
