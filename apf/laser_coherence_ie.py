"""
Laser coherence evaluator for APF coherent-phase Codomain Selection.

This module is a structural classifier over abstract interface-network ledgers.  It
exports no numeric threshold, no material-specific laser claim, no cavity design,
and no experimental result.  The evaluator is intentionally small enough to be
read and audited by the integrator before bank-side landing.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Mapping, Optional

REGIME = "laser_coherence"


class LaserVerdict(str, Enum):
    SELECT_LASER_STRUCTURAL = "SELECT_LASER_STRUCTURAL"
    FRAGMENTED_SPONTANEOUS_EMISSION_WINS = "FRAGMENTED_SPONTANEOUS_EMISSION_WINS"
    GAIN_INSUFFICIENT = "GAIN_INSUFFICIENT"
    PHASE_LOCK_FAILED = "PHASE_LOCK_FAILED"
    COHERENCE_INSUFFICIENT = "COHERENCE_INSUFFICIENT"
    LOSS_PRESSURE_OVERLOAD = "LOSS_PRESSURE_OVERLOAD"
    NOISE_PRESSURE_OVERLOAD = "NOISE_PRESSURE_OVERLOAD"
    MODE_COMPETITION_LOCKED = "MODE_COMPETITION_LOCKED"
    SATURATION_DEPLETION_OVERLOAD = "SATURATION_DEPLETION_OVERLOAD"
    METASTABLE_HISTORY_LOCKED = "METASTABLE_HISTORY_LOCKED"
    OPEN_EVIDENCE_REQUIRED = "OPEN_EVIDENCE_REQUIRED"
    REFUSE_NUMERIC_EXPORT = "REFUSE_NUMERIC_EXPORT"
    REFUSE_MATERIAL_SPECIFIC_CAVITY_CLAIM = "REFUSE_MATERIAL_SPECIFIC_CAVITY_CLAIM"
    REFUSE_BEC_OR_SUPERCONDUCTIVITY_RELABEL = "REFUSE_BEC_OR_SUPERCONDUCTIVITY_RELABEL"


class LaserUniversalityRoute(str, Enum):
    O2_PHASE_LOCKED_DRIVEN_DISSIPATIVE = "O2_PHASE_LOCKED_DRIVEN_DISSIPATIVE"
    MEAN_FIELD_DRIVEN_DISSIPATIVE = "MEAN_FIELD_DRIVEN_DISSIPATIVE"
    DIRECTED_PERCOLATION_ABSORBING_STATE = "DIRECTED_PERCOLATION_ABSORBING_STATE"
    KPZ_SCOPE_REQUIRES_BOUNDEDNESS_AUDIT = "KPZ_SCOPE_REQUIRES_BOUNDEDNESS_AUDIT"
    DISORDER_RELEVANT_PARALLEL = "DISORDER_RELEVANT_PARALLEL"
    MODE_COMPETITION_LOCKED = "MODE_COMPETITION_LOCKED"
    FINITE_SIZE_ROUNDED = "FINITE_SIZE_ROUNDED"
    NO_CLEAN_UNIVERSALITY_ROUTE = "NO_CLEAN_UNIVERSALITY_ROUTE"


@dataclass(frozen=True)
class LaserNetwork:
    # Codomain scores.  Lower score wins.  Margin is fragmented_score - coherent_score.
    independent_emission_cost: float
    phase_locked_mode_cost: float
    independent_emission_pressure: float = 0.0
    loss_pressure: float = 0.0
    spontaneous_noise_pressure: float = 0.0
    pump_noise_pressure: float = 0.0
    mode_competition_pressure: float = 0.0
    linewidth_phase_diffusion_pressure: float = 0.0
    saturation_depletion_pressure: float = 0.0
    cavity_boundary_pressure: float = 0.0
    disorder_pressure: float = 0.0
    history_pressure: float = 0.0

    # Audit gates.  The evaluator is structural: these are dimensionless ledger fields.
    gain_margin: float = 0.0
    gain_margin_floor: float = 0.0
    phase_lock_residual: float = 0.0
    phase_lock_tolerance: float = 0.05
    coherent_mode_fraction: float = 1.0
    coherent_mode_floor: float = 0.5
    loss_pressure_gate: float = 1.0
    noise_pressure_gate: float = 1.0
    mode_competition_gate: float = 1.0
    saturation_gate: float = 1.0
    output_mode_declared: bool = True
    pump_ledger_declared: bool = True
    cavity_or_feedback_ledger_declared: bool = True
    boundedness_audit_passed: bool = True
    history_barrier_cleared: bool = True

    # Paper 11 routing fields.
    dimension: int = 3
    symmetry_class: str = "U1_phase"
    dynamics_class: str = "driven_dissipative"
    locality_class: str = "local"
    mean_field_parallel: bool = False
    absorbing_state_flag: bool = False
    disorder_relevant_flag: bool = False
    finite_size_rounded: bool = False

    # Hard refusals.
    numeric_threshold_export_attempted: bool = False
    material_or_cavity_specific_claim: bool = False
    bec_or_superconductivity_relabel: bool = False


def _num(state: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    value = state.get(key, default)
    if value is None:
        return default
    return float(value)


def _bool(state: Mapping[str, Any], key: str, default: bool = False) -> bool:
    value = state.get(key, default)
    if isinstance(value, str):
        return value.lower() in {"1", "true", "yes", "y"}
    return bool(value)


def load_laser_network(state: Mapping[str, Any]) -> LaserNetwork:
    """Load a plain dict into the typed laser network ledger."""
    return LaserNetwork(
        independent_emission_cost=_num(state, "independent_emission_cost"),
        phase_locked_mode_cost=_num(state, "phase_locked_mode_cost"),
        independent_emission_pressure=_num(state, "independent_emission_pressure"),
        loss_pressure=_num(state, "loss_pressure"),
        spontaneous_noise_pressure=_num(state, "spontaneous_noise_pressure"),
        pump_noise_pressure=_num(state, "pump_noise_pressure"),
        mode_competition_pressure=_num(state, "mode_competition_pressure"),
        linewidth_phase_diffusion_pressure=_num(state, "linewidth_phase_diffusion_pressure"),
        saturation_depletion_pressure=_num(state, "saturation_depletion_pressure"),
        cavity_boundary_pressure=_num(state, "cavity_boundary_pressure"),
        disorder_pressure=_num(state, "disorder_pressure"),
        history_pressure=_num(state, "history_pressure"),
        gain_margin=_num(state, "gain_margin"),
        gain_margin_floor=_num(state, "gain_margin_floor"),
        phase_lock_residual=_num(state, "phase_lock_residual"),
        phase_lock_tolerance=_num(state, "phase_lock_tolerance", 0.05),
        coherent_mode_fraction=_num(state, "coherent_mode_fraction", 1.0),
        coherent_mode_floor=_num(state, "coherent_mode_floor", 0.5),
        loss_pressure_gate=_num(state, "loss_pressure_gate", 1.0),
        noise_pressure_gate=_num(state, "noise_pressure_gate", 1.0),
        mode_competition_gate=_num(state, "mode_competition_gate", 1.0),
        saturation_gate=_num(state, "saturation_gate", 1.0),
        output_mode_declared=_bool(state, "output_mode_declared", True),
        pump_ledger_declared=_bool(state, "pump_ledger_declared", True),
        cavity_or_feedback_ledger_declared=_bool(state, "cavity_or_feedback_ledger_declared", True),
        boundedness_audit_passed=_bool(state, "boundedness_audit_passed", True),
        history_barrier_cleared=_bool(state, "history_barrier_cleared", True),
        dimension=int(state.get("dimension", 3)),
        symmetry_class=str(state.get("symmetry_class", "U1_phase")),
        dynamics_class=str(state.get("dynamics_class", "driven_dissipative")),
        locality_class=str(state.get("locality_class", "local")),
        mean_field_parallel=_bool(state, "mean_field_parallel", False),
        absorbing_state_flag=_bool(state, "absorbing_state_flag", False),
        disorder_relevant_flag=_bool(state, "disorder_relevant_flag", False),
        finite_size_rounded=_bool(state, "finite_size_rounded", False),
        numeric_threshold_export_attempted=_bool(state, "numeric_threshold_export_attempted", False),
        material_or_cavity_specific_claim=_bool(state, "material_or_cavity_specific_claim", False),
        bec_or_superconductivity_relabel=_bool(state, "bec_or_superconductivity_relabel", False),
    )


@dataclass(frozen=True)
class LaserEvaluation:
    regime: str
    fragmented_score: float
    coherent_score: float
    admissibility_margin: float
    defect_pressure: float
    verdict: LaserVerdict
    universality_route: LaserUniversalityRoute
    reason: str
    critical_fields: Dict[str, Any]
    export_global_P: bool
    target_value_consumed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["verdict"] = self.verdict.value
        d["universality_route"] = self.universality_route.value
        return d


def _route_universality(n: LaserNetwork) -> LaserUniversalityRoute:
    """Paper 11 routing layer for the laser transition."""
    if not n.boundedness_audit_passed:
        return LaserUniversalityRoute.KPZ_SCOPE_REQUIRES_BOUNDEDNESS_AUDIT
    if n.mode_competition_pressure > n.mode_competition_gate:
        return LaserUniversalityRoute.MODE_COMPETITION_LOCKED
    if n.absorbing_state_flag:
        return LaserUniversalityRoute.DIRECTED_PERCOLATION_ABSORBING_STATE
    if n.finite_size_rounded:
        return LaserUniversalityRoute.FINITE_SIZE_ROUNDED
    if n.disorder_relevant_flag:
        return LaserUniversalityRoute.DISORDER_RELEVANT_PARALLEL
    if n.mean_field_parallel or n.locality_class in {"global", "long_range", "cavity_all_to_all"}:
        return LaserUniversalityRoute.MEAN_FIELD_DRIVEN_DISSIPATIVE
    if n.symmetry_class in {"U1_phase", "O2_phase", "phase"} and n.dynamics_class == "driven_dissipative":
        return LaserUniversalityRoute.O2_PHASE_LOCKED_DRIVEN_DISSIPATIVE
    return LaserUniversalityRoute.NO_CLEAN_UNIVERSALITY_ROUTE


def evaluate_laser_codomain(network: LaserNetwork) -> LaserEvaluation:
    """Evaluate whether the laser coherent codomain is structurally selected."""
    defect_pressure = (
        network.loss_pressure
        + network.spontaneous_noise_pressure
        + network.pump_noise_pressure
        + network.mode_competition_pressure
        + network.linewidth_phase_diffusion_pressure
        + network.saturation_depletion_pressure
        + network.cavity_boundary_pressure
        + network.disorder_pressure
        + network.history_pressure
    )
    fragmented_score = network.independent_emission_cost + network.independent_emission_pressure
    coherent_score = network.phase_locked_mode_cost + defect_pressure
    margin = fragmented_score - coherent_score
    route = _route_universality(network)

    crit = {
        "gain_margin": network.gain_margin,
        "gain_margin_floor": network.gain_margin_floor,
        "phase_lock_residual": network.phase_lock_residual,
        "phase_lock_tolerance": network.phase_lock_tolerance,
        "coherent_mode_fraction": network.coherent_mode_fraction,
        "coherent_mode_floor": network.coherent_mode_floor,
        "defect_pressure": defect_pressure,
        "boundedness_audit_passed": network.boundedness_audit_passed,
        "history_barrier_cleared": network.history_barrier_cleared,
        "universality_route": route.value,
    }

    def out(verdict: LaserVerdict, reason: str, export: bool = False) -> LaserEvaluation:
        return LaserEvaluation(
            regime=REGIME,
            fragmented_score=fragmented_score,
            coherent_score=coherent_score,
            admissibility_margin=margin,
            defect_pressure=defect_pressure,
            verdict=verdict,
            universality_route=route,
            reason=reason,
            critical_fields=crit,
            export_global_P=export,
            target_value_consumed=False,
        )

    # Hard refusals come before the margin, matching the coherent-phase audit ladder.
    if network.numeric_threshold_export_attempted:
        return out(LaserVerdict.REFUSE_NUMERIC_EXPORT, "numeric threshold / linewidth / pump export attempted")
    if network.material_or_cavity_specific_claim:
        return out(LaserVerdict.REFUSE_MATERIAL_SPECIFIC_CAVITY_CLAIM, "material- or cavity-specific laser claim attempted")
    if network.bec_or_superconductivity_relabel:
        return out(LaserVerdict.REFUSE_BEC_OR_SUPERCONDUCTIVITY_RELABEL, "laser claim relabels BEC or superconductivity machinery")

    if not (network.output_mode_declared and network.pump_ledger_declared and network.cavity_or_feedback_ledger_declared):
        return out(LaserVerdict.OPEN_EVIDENCE_REQUIRED, "required output-mode/pump/cavity ledger is missing")
    if network.gain_margin <= network.gain_margin_floor:
        return out(LaserVerdict.GAIN_INSUFFICIENT, "gain margin does not clear the structural floor")
    if network.phase_lock_residual > network.phase_lock_tolerance:
        return out(LaserVerdict.PHASE_LOCK_FAILED, "phase-lock residual exceeds tolerance")
    if network.coherent_mode_fraction < network.coherent_mode_floor:
        return out(LaserVerdict.COHERENCE_INSUFFICIENT, "coherent photon-mode fraction below floor")
    if network.loss_pressure > network.loss_pressure_gate:
        return out(LaserVerdict.LOSS_PRESSURE_OVERLOAD, "loss pressure exceeds gate")
    if network.spontaneous_noise_pressure + network.pump_noise_pressure + network.linewidth_phase_diffusion_pressure > network.noise_pressure_gate:
        return out(LaserVerdict.NOISE_PRESSURE_OVERLOAD, "noise / phase-diffusion pressure exceeds gate")
    if network.mode_competition_pressure > network.mode_competition_gate:
        return out(LaserVerdict.MODE_COMPETITION_LOCKED, "mode competition prevents clean single-mode codomain selection")
    if network.saturation_depletion_pressure > network.saturation_gate:
        return out(LaserVerdict.SATURATION_DEPLETION_OVERLOAD, "gain saturation or depletion pressure exceeds gate")
    if margin <= 0:
        return out(LaserVerdict.FRAGMENTED_SPONTANEOUS_EMISSION_WINS, "fragmented emission codomain is not undercut")
    if not network.history_barrier_cleared:
        return out(LaserVerdict.METASTABLE_HISTORY_LOCKED, "instantaneous margin positive but history barrier not cleared")

    return out(LaserVerdict.SELECT_LASER_STRUCTURAL, "phase-locked photon-mode codomain selected", export=True)


def evaluate_from_dict(state: Mapping[str, Any]) -> Dict[str, Any]:
    return evaluate_laser_codomain(load_laser_network(state)).to_dict()
