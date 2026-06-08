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

PROTOCOLS = {
    "PHASE_BOUNDARY_SCOUT",
    "EVIDENCE_COMPLETION_SC",
    "COHERENCE_OPTIMIZATION_NONSC",
    "BURDEN_REDUCTION",
    "LEDGER_COMPLETION",
    "CLAIM_QUARANTINE",
    "BURDEN_SEPARATION_AND_STABILITY_SCOUT",
    "GENERIC_SIGNATURE_COMPLETION",
}

@dataclass(frozen=True)
class InterventionAction:
    name: str
    utility: float
    priority: float
    reason: str
    axes: List[str] = field(default_factory=list)
    required_evidence: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "utility": self.utility,
            "priority": self.priority,
            "reason": self.reason,
            "axes": list(self.axes),
            "required_evidence": list(self.required_evidence),
        }

@dataclass(frozen=True)
class InterventionResult:
    classification: str
    selected_protocol: str
    top_action: str
    actions: List[InterventionAction]
    phase_boundary_axes: List[str]
    promotion_allowed: bool
    exports: Dict[str, int]
    reasons: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "classification": self.classification,
            "selected_protocol": self.selected_protocol,
            "top_action": self.top_action,
            "actions": [a.as_dict() for a in self.actions],
            "phase_boundary_axes": list(self.phase_boundary_axes),
            "promotion_allowed": self.promotion_allowed,
            "exports": dict(self.exports),
            "reasons": list(self.reasons),
        }

def _exports_base() -> Dict[str, int]:
    return {
        "coherent_materials_intervention_selector": 1,
        "SC_materials_intervention_selector": 1,
        "phase_boundary_scout": 1,
        "fail_closed_intervention_ladder": 1,
        "Pearson_QM_nonSC_intervention": 0,
        "SC_phase_boundary_mapping_case": 0,
        "SC_numeric_Tc_prediction": 0,
        "SC_new_material_prediction": 0,
        "SC_highTc_solution": 0,
        "SC_ab_initio_chemistry": 0,
        "Pearson_superconductivity_claim": 0,
        "room_temperature_superconductivity_claim": 0,
    }

def _classification(ledger: Mapping[str, Any]) -> str:
    val = ledger.get("classification") or ledger.get("expected_classification")
    if val in CLASSIFICATIONS:
        return str(val)
    claim = ledger.get("claim", {}) or {}
    provenance = ledger.get("provenance", {}) or {}
    evidence = ledger.get("evidence", {}) or {}
    if claim.get("quarantine") or (claim.get("extraordinary") and not provenance.get("declared")):
        return "CLAIM_QUARANTINED"
    if not provenance.get("declared") or not evidence:
        return "MATERIAL_LEDGER_INSUFFICIENT"
    if evidence.get("zero_resistance") and not (evidence.get("meissner") or evidence.get("diamagnetic_response")):
        return "RESISTIVE_ONLY_NO_MEISSNER"
    return "COHERENT_SIGNATURE_PARTIAL"

def _action(name: str, utility: float, priority: float, reason: str, axes: Optional[List[str]] = None, required_evidence: Optional[List[str]] = None) -> InterventionAction:
    return InterventionAction(name=name, utility=round(float(utility), 6), priority=round(float(priority), 6), reason=reason, axes=list(axes or []), required_evidence=list(required_evidence or []))

def _top_burdens(ledger: Mapping[str, Any]) -> List[tuple[str, float]]:
    burdens = ledger.get("burdens", {}) or {}
    out = []
    for k, v in burdens.items():
        try:
            fv = float(v)
        except (TypeError, ValueError):
            continue
        if fv > 0:
            out.append((str(k), fv))
    out.sort(key=lambda kv: (-kv[1], kv[0]))
    return out

def _axis_utilities(ledger: Mapping[str, Any]) -> List[tuple[str, float]]:
    sens = ledger.get("control_sensitivities", {}) or {}
    out = []
    if not isinstance(sens, Mapping):
        return out
    for axis, spec in sens.items():
        if not isinstance(spec, Mapping):
            continue
        delta = float(spec.get("delta_margin", 0.0) or 0.0)
        cost = float(spec.get("cost", 0.0) or 0.0)
        risk = float(spec.get("risk", 0.0) or 0.0)
        provenance = float(spec.get("provenance_penalty", 0.0) or 0.0)
        utility = delta - cost - risk - provenance
        out.append((str(axis), utility))
    out.sort(key=lambda kv: (-kv[1], kv[0]))
    return out

def _is_high_pressure_case(ledger: Mapping[str, Any]) -> bool:
    controls = ledger.get("controls", {}) or {}
    burdens = ledger.get("burdens", {}) or {}
    try:
        pressure = float(controls.get("pressure_GPa", 0.0) or 0.0)
    except (TypeError, ValueError):
        pressure = 0.0
    try:
        pburden = float(burdens.get("pressure", 0.0) or 0.0)
    except (TypeError, ValueError):
        pburden = 0.0
    return pressure >= 20.0 or pburden >= 0.8

def select_interventions(ledger: Mapping[str, Any]) -> InterventionResult:
    classification = _classification(ledger)
    exports = _exports_base()
    reasons: List[str] = []
    actions: List[InterventionAction] = []
    axes = [axis for axis, utility in _axis_utilities(ledger) if utility > 0]
    protocol = "GENERIC_SIGNATURE_COMPLETION"
    promotion_allowed = False

    if classification == "CLAIM_QUARANTINED":
        protocol = "CLAIM_QUARANTINE"
        actions.append(_action(
            "QUARANTINE_AND_REPRODUCE", 2.0, 10.0,
            "extraordinary_or_flagged_claim_requires independent reproduction and provenance before interpretation",
            required_evidence=["independent_sample", "raw_data", "provenance", "Meissner_or_coherence_signature"],
        ))
        reasons.append("claim_quarantine_preempts_intervention_ranking")

    elif classification == "MATERIAL_LEDGER_INSUFFICIENT":
        protocol = "LEDGER_COMPLETION"
        actions.append(_action(
            "COMPLETE_MATERIAL_LEDGER", 1.8, 9.5,
            "required material/control/evidence/provenance slots are missing",
            required_evidence=["composition", "structure", "controls", "sample_history", "measurement_context", "covariance_or_uncertainty"],
        ))
        reasons.append("ledger_completion_precedes_phase_claims")

    elif classification == "RESISTIVE_ONLY_NO_MEISSNER":
        protocol = "EVIDENCE_COMPLETION_SC"
        actions.extend([
            _action("MEASURE_MEISSNER_RESPONSE", 1.5, 9.0, "resistive transition cannot establish superconductivity without diamagnetic/Meissner evidence", required_evidence=["Meissner", "diamagnetic_response"]),
            _action("MEASURE_FIELD_SUPPRESSION", 1.2, 8.7, "field suppression or critical-field response separates SC from artifacts/percolation", required_evidence=["critical_field_response", "field_suppression"]),
            _action("REPRODUCE_SAMPLE_SERIES", 1.0, 8.5, "claim must survive repeated sample/provenance checks", required_evidence=["sample_series", "raw_resistance_curves", "contact_geometry"]),
            _action("DECLARE_COVARIANCE_AND_PROVENANCE", 0.8, 8.0, "uncertainty and measurement provenance must be declared before promotion", required_evidence=["Sigma", "instrument_calibration", "sample_id"]),
        ])
        reasons.append("SC_evidence_completion_required")

    elif classification == "DEFECT_OR_INHOMOGENEITY_OVERLOADED":
        protocol = "BURDEN_REDUCTION"
        for burden, val in _top_burdens(ledger)[:4]:
            if burden == "inhomogeneity":
                name = "REDUCE_INHOMOGENEITY"
            elif burden == "synthesis":
                name = "STABILIZE_SYNTHESIS"
            elif burden == "stability":
                name = "IMPROVE_ENVIRONMENTAL_STABILITY"
            elif burden == "disorder":
                name = "REDUCE_DISORDER"
            elif burden == "ion_interaction":
                name = "DIAGNOSE_ION_INTERACTION_SPLITTING"
            else:
                name = f"REDUCE_{burden.upper()}_BURDEN"
            actions.append(_action(name, val, 7.0 + val, f"largest declared burden: {burden}={val}", required_evidence=["burden_remeasurement", "sample_comparison"]))
        reasons.append("largest_material_burdens_ranked_first")

    elif classification == "COMPETING_CODOMAIN_DOMINANT":
        protocol = "PHASE_BOUNDARY_SCOUT"
        exports["SC_phase_boundary_mapping_case"] = 1
        for axis, utility in _axis_utilities(ledger)[:4]:
            if utility > 0:
                actions.append(_action(f"SWEEP_{axis.upper()}", utility, 8.0 + utility, f"positive codomain-margin sensitivity along {axis}", axes=[axis], required_evidence=["codomain_signature", "history_state", "control_calibration"]))
        actions.append(_action("MAP_HYSTERESIS_AND_METASTABILITY", 0.6, 8.0, "competing codomain requires history/barrier map", axes=["history"], required_evidence=["up_sweep", "down_sweep", "dwell_time", "cooling_history"]))
        actions.append(_action("SUPPRESS_COMPETING_CODOMAIN", 0.5, 7.8, "selected codomain is not SC/coherent target", required_evidence=["AFM_CDW_stripe_or_pseudogap_signature", "SC_signature_package"] ))
        reasons.append("phase_boundary_scout_for_competing_codomain")

    elif classification == "SC_MATERIAL_ADMISSIBLE":
        if _is_high_pressure_case(ledger):
            protocol = "BURDEN_SEPARATION_AND_STABILITY_SCOUT"
            actions.append(_action("SEPARATE_HIGH_PRESSURE_SC_FROM_AMBIENT_USABILITY", 1.7, 9.2, "SC admissible under supplied controls does not imply ambient material solution", axes=["pressure"], required_evidence=["pressure_context", "decompression_history", "structural_stability"]))
            actions.append(_action("EVALUATE_QUENCH_OR_STABILIZATION_HISTORY", 1.0, 8.4, "history/stability gate required before ambient extrapolation", axes=["history", "pressure"], required_evidence=["post_quench_structure", "repeat_transport", "Meissner_after_history"] ))
        else:
            protocol = "PHASE_BOUNDARY_SCOUT"
            actions.append(_action("MAP_PHASE_BOUNDARY", 1.4, 8.8, "admissible SC ledger should map control limits without deriving Tc", axes=axes[:3] or ["temperature", "field"], required_evidence=["observed_transition_temperature", "critical_field_response", "Meissner", "sample_series"] ))
        exports["SC_phase_boundary_mapping_case"] = 1
        actions.append(_action("MEASURE_TC_AS_OBSERVED_LEDGER_VALUE", 0.9, 7.8, "Tc may be measured and recorded, not APF-predicted", axes=["temperature"], required_evidence=["observed_Tc", "uncertainty", "measurement_protocol"] ))
        actions.append(_action("MAP_CRITICAL_FIELDS_AND_FLUX_RESPONSE", 0.8, 7.7, "critical fields and flux response complete the SC material ledger", axes=["field"], required_evidence=["Hc1_or_Hc2", "field_suppression", "magnetization"] ))
        promotion_allowed = True
        reasons.append("SC_admissible_routes_to_mapping_not_prediction")

    elif classification == "COHERENT_BUT_NOT_SC":
        protocol = "COHERENCE_OPTIMIZATION_NONSC"
        coherence_type = ledger.get("coherence_type")
        if ledger.get("source_key") == "pearson_dissertation_2025" or coherence_type == "quantum_memory":
            exports["Pearson_QM_nonSC_intervention"] = 1 if ledger.get("source_key") == "pearson_dissertation_2025" else 0
            actions.extend([
                _action("OPTIMIZE_AFC_EFFICIENCY", 1.4, 8.8, "quantum-memory case should improve AFC retrieval before broader promotion", axes=["comb_spacing", "optical_depth", "burn_sequence"], required_evidence=["AFC_efficiency", "storage_time", "noise_floor"]),
                _action("REDUCE_INHOMOGENEOUS_BROADENING", 1.1, 8.2, "line narrowing improves optical resolvability and memory protocol margin", axes=["synthesis", "strain", "temperature"], required_evidence=["inhomogeneous_linewidth", "sample_series"]),
                _action("EXTEND_SPIN_STORAGE_TIME", 0.9, 8.0, "spin lifetime/coherence sets storage-time ceiling", axes=["magnetic_field", "temperature", "pulse_protocol"], required_evidence=["T1_spin", "T2_spin_or_echo", "hyperfine_resolution"]),
                _action("PRESERVE_NON_SC_CLASSIFICATION", 0.5, 7.5, "no superconductivity evidence is present in this ledger", required_evidence=["do_not_claim_SC"]),
            ])
            reasons.append("Pearson_style_quantum_memory_routes_to_nonSC_optimization")
        else:
            actions.append(_action("OPTIMIZE_COHERENCE_PROTOCOL", 1.0, 8.0, "coherent-but-not-SC case routes to regime-appropriate coherence optimization", required_evidence=["coherence_time", "protocol_efficiency", "noise_floor"]))
        promotion_allowed = True

    elif classification == "COHERENT_MATERIAL_ADMISSIBLE":
        protocol = "COHERENCE_OPTIMIZATION_NONSC"
        actions.append(_action("MAP_COHERENCE_PHASE_BOUNDARY", 1.1, 8.0, "generic coherent material should map controls and degradation thresholds", axes=axes[:3] or ["temperature", "field", "disorder"], required_evidence=["coherence_signature", "degradation_thresholds"]))
        promotion_allowed = True

    else:  # COHERENT_SIGNATURE_PARTIAL and any future known partial state
        protocol = "GENERIC_SIGNATURE_COMPLETION"
        actions.append(_action("COMPLETE_COHERENCE_SIGNATURES", 1.0, 8.0, "partial coherent-material signature requires missing protocol evidence", required_evidence=["coherence_signature", "reproducibility", "covariance", "control_sweep"]))
        for axis, utility in _axis_utilities(ledger)[:3]:
            if utility > 0:
                actions.append(_action(f"SCOUT_{axis.upper()}", utility, 7.0 + utility, f"positive partial-signature sensitivity along {axis}", axes=[axis], required_evidence=["control_calibration", "signature_response"]))
        reasons.append("partial_signature_completion")

    if not actions:
        actions.append(_action("COMPLETE_COHERENCE_SIGNATURES", 0.1, 1.0, "fallback action for undeclared partial state"))

    # For phase-boundary capable cases, append positive utility sweeps not already present.
    existing = {a.name for a in actions}
    if classification in {"SC_MATERIAL_ADMISSIBLE", "COMPETING_CODOMAIN_DOMINANT", "COHERENT_SIGNATURE_PARTIAL"}:
        for axis, utility in _axis_utilities(ledger)[:3]:
            name = f"SWEEP_{axis.upper()}"
            if utility > 0 and name not in existing:
                actions.append(_action(name, utility, 7.0 + utility, f"additional positive control-axis utility along {axis}", axes=[axis], required_evidence=["control_calibration", "codomain_signature"]))
                existing.add(name)

    actions.sort(key=lambda a: (-a.priority, -a.utility, a.name))
    phase_boundary_axes = axes[:4]
    top = actions[0].name
    return InterventionResult(
        classification=classification,
        selected_protocol=protocol,
        top_action=top,
        actions=actions,
        phase_boundary_axes=phase_boundary_axes,
        promotion_allowed=promotion_allowed,
        exports=exports,
        reasons=reasons,
    )
