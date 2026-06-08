from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


NON_CLAIMS = {
    "Export_protocol_execution": 0,
    "Export_experimental_result": 0,
    "Export_SC_numeric_Tc_prediction": 0,
    "Export_SC_material_specific_phase_diagram": 0,
    "Export_SC_new_material_prediction": 0,
    "Export_SC_highTc_solution": 0,
    "Export_SC_ab_initio_chemistry": 0,
    "Export_Pearson_superconductivity_claim": 0,
    "Export_room_temperature_superconductivity_claim": 0,
}


@dataclass(frozen=True)
class ProtocolCard:
    protocol_id: str
    objective: str
    classification_gate: str
    top_action: str
    control_axes: tuple[str, ...]
    prerequisite_receipts: tuple[str, ...]
    measurement_sequence: tuple[str, ...]
    required_evidence_receipts: tuple[str, ...]
    pass_condition: str
    fail_condition: str
    next_transition: str
    no_smuggling_guards: tuple[str, ...]
    non_claims_preserved: Mapping[str, int] = field(default_factory=lambda: dict(NON_CLAIMS))

    def to_dict(self) -> dict[str, Any]:
        return {
            "protocol_id": self.protocol_id,
            "objective": self.objective,
            "classification_gate": self.classification_gate,
            "top_action": self.top_action,
            "control_axes": list(self.control_axes),
            "prerequisite_receipts": list(self.prerequisite_receipts),
            "measurement_sequence": list(self.measurement_sequence),
            "required_evidence_receipts": list(self.required_evidence_receipts),
            "pass_condition": self.pass_condition,
            "fail_condition": self.fail_condition,
            "next_transition": self.next_transition,
            "no_smuggling_guards": list(self.no_smuggling_guards),
            "non_claims_preserved": dict(self.non_claims_preserved),
        }


def _get(ledger: Mapping[str, Any], *keys: str, default: Any = None) -> Any:
    cur: Any = ledger
    for key in keys:
        if not isinstance(cur, Mapping) or key not in cur:
            return default
        cur = cur[key]
    return cur


def _classification(ledger: Mapping[str, Any]) -> str:
    return str(_get(ledger, "classification", default=_get(ledger, "discriminator", "classification", default="")))


def _top_action(ledger: Mapping[str, Any]) -> str:
    return str(_get(ledger, "top_action", default=_get(ledger, "intervention", "top_action", default="")))


def _family(ledger: Mapping[str, Any]) -> str:
    return str(_get(ledger, "material_family", default=_get(ledger, "family", default=""))).lower()


def _subtype(ledger: Mapping[str, Any]) -> str:
    return str(_get(ledger, "subtype", default=_get(ledger, "coherence_subtype", default=""))).lower()


def _axes(ledger: Mapping[str, Any], fallback: tuple[str, ...]) -> tuple[str, ...]:
    axes = _get(ledger, "control_axes", default=None)
    if axes is None:
        axes = _get(ledger, "controls", "axes", default=None)
    if axes:
        return tuple(str(a) for a in axes)
    return fallback


def compile_protocol(ledger: Mapping[str, Any]) -> ProtocolCard:
    classification = _classification(ledger)
    action = _top_action(ledger)
    family = _family(ledger)
    subtype = _subtype(ledger)

    if classification == "CLAIM_QUARANTINED" or action == "QUARANTINE_AND_REPRODUCE":
        return ProtocolCard(
            protocol_id="CLAIM_QUARANTINE_REPLICATION_PROTOCOL",
            objective="Prevent phase promotion until provenance, calibration, and independent replication receipts exist.",
            classification_gate=classification,
            top_action=action or "QUARANTINE_AND_REPRODUCE",
            control_axes=_axes(ledger, ("sample_batch", "laboratory", "instrument", "temperature", "field")),
            prerequisite_receipts=("claim_text", "raw_trace_pointer", "sample_chain_of_custody"),
            measurement_sequence=(
                "Freeze claim language and prohibit phase labels during quarantine.",
                "Archive raw electrical, magnetic, thermal, structural, and calibration data.",
                "Run blind or independent replication on at least one new sample batch.",
                "Compare negative controls and instrument artifacts before any codomain interpretation.",
            ),
            required_evidence_receipts=(
                "raw_data_archive",
                "instrument_calibration",
                "sample_chain_of_custody",
                "blind_or_independent_replication",
                "negative_control_outcome",
                "pre_registered_pass_fail_rule",
            ),
            pass_condition="Only after independent replication plus SC bulk receipts may the ledger be re-entered as SC_SIGNATURE_PARTIAL or SC_MATERIAL_ADMISSIBLE.",
            fail_condition="If replication, calibration, or chain-of-custody fails, remain CLAIM_QUARANTINED.",
            next_transition="QUARANTINE_TO_EVIDENCE_LEDGER_REENTRY",
            no_smuggling_guards=(
                "No room-temperature superconductivity export is allowed from quarantine.",
                "No formula-only inference is allowed.",
                "No unpublished target curve may tune the protocol.",
            ),
        )

    if classification == "MATERIAL_LEDGER_INSUFFICIENT" or action == "COMPLETE_MATERIAL_LEDGER":
        return ProtocolCard(
            protocol_id="MATERIAL_LEDGER_COMPLETION_PROTOCOL",
            objective="Complete the material ledger before coherent-phase or superconductivity interpretation.",
            classification_gate=classification,
            top_action=action or "COMPLETE_MATERIAL_LEDGER",
            control_axes=_axes(ledger, ("composition", "structure", "carrier_or_emitter_sector", "defects", "controls", "provenance")),
            prerequisite_receipts=("declared_missing_slots",),
            measurement_sequence=(
                "Declare composition, stoichiometry, synthesis route, sample history, and batch identifiers.",
                "Attach crystal/structural characterization and dimensionality/symmetry evidence.",
                "Attach carrier-sector or emitter-sector evidence appropriate to the intended coherence type.",
                "Attach defect/disorder/provenance and control-vector uncertainty ledgers.",
            ),
            required_evidence_receipts=(
                "composition_and_stoichiometry",
                "crystal_structure_or_phase_purity",
                "carrier_or_emitter_sector",
                "defect_disorder_ledger",
                "control_vector_ledger",
                "sample_provenance_and_uncertainty",
            ),
            pass_condition="If all required ledger slots are supplied, rerun the discriminator; no direct phase promotion occurs inside this protocol.",
            fail_condition="If any required slot remains absent, remain MATERIAL_LEDGER_INSUFFICIENT.",
            next_transition="LEDGER_COMPLETION_TO_DISCRIMINATOR_REENTRY",
            no_smuggling_guards=(
                "No formula-only SC inference.",
                "No inferred Meissner or coherence signature from composition alone.",
                "No missing covariance/provenance suppression.",
            ),
        )

    if classification == "RESISTIVE_ONLY_NO_MEISSNER" or action == "MEASURE_MEISSNER_RESPONSE":
        return ProtocolCard(
            protocol_id="SC_EVIDENCE_COMPLETION_PROTOCOL",
            objective="Convert a resistive-only superconductivity claim into a bulk-evidence ledger or fail it closed.",
            classification_gate=classification,
            top_action=action or "MEASURE_MEISSNER_RESPONSE",
            control_axes=_axes(ledger, ("temperature", "magnetic_field", "current", "sample_batch", "contact_geometry")),
            prerequisite_receipts=("resistance_trace", "contact_geometry", "sample_identity"),
            measurement_sequence=(
                "Repeat resistivity with current/contact-geometry checks and normal-state reference.",
                "Measure bulk diamagnetic shielding or Meissner response on the same sample/batch.",
                "Measure field suppression, critical-field response, or transition broadening under applied field.",
                "Replicate across samples and attach raw traces plus uncertainty/provenance ledger.",
            ),
            required_evidence_receipts=(
                "zero_resistance_trace_with_contacts_and_geometry",
                "bulk_diamagnetic_or_Meissner_response",
                "field_suppression_or_critical_field_response",
                "reproducible_transition_across_samples",
                "normal_state_reference",
                "sample_provenance_and_uncertainty_ledger",
            ),
            pass_condition="Only after zero resistance, bulk Meissner/diamagnetic response, field suppression, reproducibility, and provenance receipts can the ledger re-enter as SC_MATERIAL_ADMISSIBLE.",
            fail_condition="If bulk magnetic/field/provenance receipts fail, remain RESISTIVE_ONLY_NO_MEISSNER or CLAIM_QUARANTINED depending on severity.",
            next_transition="RESISTIVE_ONLY_TO_SC_AUDIT_REENTRY",
            no_smuggling_guards=(
                "A resistivity drop alone cannot promote SC.",
                "Transport artifacts cannot substitute for bulk magnetic evidence.",
                "Numeric Tc export remains forbidden.",
            ),
        )

    if action == "SEPARATE_HIGH_PRESSURE_SC_FROM_AMBIENT_USABILITY" or "hydride" in family:
        return ProtocolCard(
            protocol_id="HIGH_PRESSURE_BURDEN_SEPARATION_PROTOCOL",
            objective="Separate pressure-confined superconductivity evidence from ambient-material usability claims.",
            classification_gate=classification,
            top_action=action or "SEPARATE_HIGH_PRESSURE_SC_FROM_AMBIENT_USABILITY",
            control_axes=_axes(ledger, ("pressure", "temperature", "magnetic_field", "decompression_history", "sample_phase")),
            prerequisite_receipts=("pressure_cell_calibration", "structural_phase_pointer", "transport_or_magnetic_trace"),
            measurement_sequence=(
                "Calibrate pressure and temperature in situ and declare pressure medium/cell artifacts.",
                "Track structure/phase identity under pressure, during sweep, and after decompression.",
                "Pair transport evidence with magnetic/field-response evidence where experimentally possible.",
                "Run decompression/hysteresis checks to test whether any coherent signature survives ambient return.",
            ),
            required_evidence_receipts=(
                "pressure_calibration_trace",
                "in_situ_structural_phase_identity",
                "transport_and_field_response_under_pressure",
                "decompression_history_ledger",
                "ambient_return_measurement",
                "artifact_and_pressure_cell_control",
            ),
            pass_condition="May support pressure-confined SC admissibility only under declared controls; ambient usability requires separate ambient-return receipts.",
            fail_condition="If pressure or phase identity receipts fail, route to BURDEN_REDUCTION or CLAIM_QUARANTINED; do not infer ambient SC.",
            next_transition="HIGH_PRESSURE_SC_TO_CONTROL_CONDITIONED_LEDGER",
            no_smuggling_guards=(
                "High-pressure evidence is not ambient-pressure evidence.",
                "Decompression history cannot be omitted.",
                "Room-temperature or ambient usability claims require independent receipts.",
            ),
        )

    if classification == "COHERENT_BUT_NOT_SC" or "quantum_memory" in subtype or action == "OPTIMIZE_AFC_EFFICIENCY":
        return ProtocolCard(
            protocol_id="PEARSON_QM_AFC_OPTIMIZATION_PROTOCOL",
            objective="Optimize a non-SC rare-earth quantum-memory coherent-material ledger.",
            classification_gate=classification,
            top_action=action or "OPTIMIZE_AFC_EFFICIENCY",
            control_axes=_axes(ledger, ("temperature", "optical_frequency", "burn_power", "comb_spacing", "storage_time", "sample_orientation")),
            prerequisite_receipts=("5D0_to_7F0_transition", "inhomogeneous_linewidth", "homogeneous_linewidth_or_photon_echo"),
            measurement_sequence=(
                "Map photoluminescence/PLE center frequency, optical lifetime, and inhomogeneous linewidth.",
                "Measure spectral-hole and photon-echo/coherence behavior with declared pulse sequence.",
                "Sweep AFC comb spacing, finesse, burn power, and storage-time targets.",
                "Attach stability and synthesis-provenance receipts before device-readiness promotion.",
            ),
            required_evidence_receipts=(
                "inhomogeneous_linewidth",
                "homogeneous_linewidth_or_T2opt",
                "optical_lifetime",
                "spin_lifetime",
                "spectral_hole_or_photon_echo_trace",
                "AFC_efficiency_bandwidth_storage_time",
                "environmental_stability",
                "synthesis_and_sample_provenance",
            ),
            pass_condition="May promote as quantum-memory coherent-material evidence when AFC/coherence/stability receipts improve under declared controls; superconductivity remains unclaimed.",
            fail_condition="If linewidth, spin lifetime, AFC, or stability receipts degrade or remain absent, route to burden reduction or partial-coherence status.",
            next_transition="NONSC_QM_OPTIMIZATION_TO_COHERENT_MATERIAL_REENTRY",
            no_smuggling_guards=(
                "Do not convert rare-earth quantum-memory coherence into superconductivity.",
                "Do not infer device readiness without AFC and stability receipts.",
                "Do not suppress inhomogeneous broadening or synthesis burdens.",
            ),
        )

    if classification == "DEFECT_OR_INHOMOGENEITY_OVERLOADED" or action in {"REDUCE_INHOMOGENEITY", "REDUCE_DEFECT_BURDEN"}:
        return ProtocolCard(
            protocol_id="BURDEN_REDUCTION_PROTOCOL",
            objective="Reduce declared defect, inhomogeneity, stability, or synthesis burdens before reclassification.",
            classification_gate=classification,
            top_action=action or "REDUCE_INHOMOGENEITY",
            control_axes=_axes(ledger, ("synthesis_route", "anneal_or_growth_rate", "environment", "temperature", "sample_batch")),
            prerequisite_receipts=("burden_registry", "baseline_spectrum_or_transport", "synthesis_route"),
            measurement_sequence=(
                "Identify dominant burden: defects, inhomogeneity, instability, impurity phase, or local-environment spread.",
                "Run controlled synthesis/growth/stability variants with one burden axis changed at a time.",
                "Measure before/after structural purity and coherence or transport signatures.",
                "Rerun discriminator only after the burden ledger is quantitatively updated.",
            ),
            required_evidence_receipts=(
                "baseline_burden_measurement",
                "modified_synthesis_or_stability_protocol",
                "before_after_structure_or_phase_purity",
                "before_after_coherence_or_transport_signature",
                "environmental_stability_receipt",
                "updated_defect_or_inhomogeneity_ledger",
            ),
            pass_condition="If burden penalties decrease and coherence/SC evidence improves, re-enter the discriminator; no direct phase promotion occurs.",
            fail_condition="If burdens persist or worsen, remain DEFECT_OR_INHOMOGENEITY_OVERLOADED.",
            next_transition="BURDEN_REDUCTION_TO_DISCRIMINATOR_REENTRY",
            no_smuggling_guards=(
                "No handwaving away defects or instability.",
                "No after-only measurement without baseline.",
                "No phase promotion from synthesis intent alone.",
            ),
        )

    if classification == "COMPETING_CODOMAIN_DOMINANT" or action == "SWEEP_STRAIN" or "nickelate" in family or "correlated" in family:
        return ProtocolCard(
            protocol_id="CORRELATED_LAYER_PHASE_BOUNDARY_PROTOCOL",
            objective="Map competing codomain boundaries in a correlated-layer material without formula-level SC claims.",
            classification_gate=classification,
            top_action=action or "SWEEP_STRAIN",
            control_axes=_axes(ledger, ("strain", "oxygenation", "pressure", "temperature", "magnetic_field", "history")),
            prerequisite_receipts=("structure_and_dimensionality", "normal_state_transport", "competing_order_indicator"),
            measurement_sequence=(
                "Declare strain/pressure/oxygenation/history axes and sample-preparation route.",
                "Sweep one control axis at a time while tracking transport, magnetic response, and structural state.",
                "Measure competing-order indicators such as AFM/CDW/stripe/pseudogap proxies where available.",
                "Attach hysteresis and sample-history receipts before selecting SC, vortex, or competing codomain.",
            ),
            required_evidence_receipts=(
                "strain_pressure_oxygenation_history_ledger",
                "normal_state_transport_reference",
                "bulk_SC_evidence_if_claimed",
                "competing_order_probe",
                "hysteresis_or_metastability_trace",
                "structure_phase_identity_under_control",
            ),
            pass_condition="Codomain may change only at receipt-backed phase boundaries; SC admissibility requires the SC bulk receipt subset.",
            fail_condition="If competing-order evidence dominates or bulk SC receipts are absent, remain COMPETING_CODOMAIN_DOMINANT or PHASE_FRAGMENTED.",
            next_transition="CORRELATED_LAYER_BOUNDARY_TO_SELECTOR_REENTRY",
            no_smuggling_guards=(
                "No formula-level nickelate or cuprate SC claim.",
                "No hidden oxygenation/strain/history axis.",
                "No resistive-only promotion in a competing-order regime.",
            ),
        )

    if classification == "SC_MATERIAL_ADMISSIBLE" or action == "MAP_PHASE_BOUNDARY":
        return ProtocolCard(
            protocol_id="SC_PHASE_BOUNDARY_MAPPING_PROTOCOL",
            objective="Map the control-conditioned superconducting codomain without claiming a numeric-Tc prediction or complete phase diagram.",
            classification_gate=classification,
            top_action=action or "MAP_PHASE_BOUNDARY",
            control_axes=_axes(ledger, ("temperature", "magnetic_field", "current", "pressure_or_strain_or_doping", "sample_history")),
            prerequisite_receipts=("bulk_SC_evidence", "provenance_ledger", "normal_state_reference"),
            measurement_sequence=(
                "Repeat SC evidence across declared control axes and sample batches.",
                "Measure field/current suppression and critical response envelopes.",
                "Track vortex/mixed-phase, hysteresis, and sample-history effects.",
                "Emit a bounded phase-boundary scout ledger, not a final material phase diagram.",
            ),
            required_evidence_receipts=(
                "zero_resistance_trace_with_contacts_and_geometry",
                "bulk_diamagnetic_or_Meissner_response",
                "critical_field_or_field_suppression_envelope",
                "critical_current_or_current_response",
                "sample_batch_reproducibility",
                "vortex_or_hysteresis_boundary_if_present",
                "control_axis_uncertainty_ledger",
            ),
            pass_condition="May retain SC_MATERIAL_ADMISSIBLE over the measured control region; extrapolation outside receipts is forbidden.",
            fail_condition="If SC receipts vanish or competing/vortex codomain dominates, demote to competing or fragmented codomain.",
            next_transition="SC_ADMISSIBLE_TO_BOUNDARY_SCOUT_LEDGER",
            no_smuggling_guards=(
                "No numeric Tc prediction; only measured transition receipts.",
                "No complete phase diagram claim from a scout grid.",
                "No extrapolation beyond declared controls.",
            ),
        )

    return ProtocolCard(
        protocol_id="GENERIC_COHERENT_MATERIAL_PROTOCOL",
        objective="Collect coherence-specific receipts for a declared non-SC or SC-adjacent material ledger.",
        classification_gate=classification,
        top_action=action or "COLLECT_COHERENCE_RECEIPTS",
        control_axes=_axes(ledger, ("temperature", "field", "history", "sample_batch")),
        prerequisite_receipts=("declared_coherence_type", "baseline_material_ledger"),
        measurement_sequence=(
            "Declare the target coherence codomain and burden model.",
            "Collect baseline coherence signatures under declared controls.",
            "Collect burden and provenance receipts.",
            "Rerun discriminator after receipt attachment.",
        ),
        required_evidence_receipts=(
            "coherence_signature",
            "control_vector_ledger",
            "burden_ledger",
            "sample_provenance_and_uncertainty",
        ),
        pass_condition="Re-enter discriminator after receipts; no direct promotion from generic protocol.",
        fail_condition="Remain partial or insufficient if receipts are absent.",
        next_transition="GENERIC_PROTOCOL_TO_DISCRIMINATOR_REENTRY",
        no_smuggling_guards=("No inferred coherence from material name.", "No untyped codomain promotion."),
    )
