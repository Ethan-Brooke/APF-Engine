"""Bose--Einstein condensation coherent-phase evaluator candidate.

Architecture-only intent: this module evaluates abstract interface-network
ledgers for a BEC codomain-selection regime. It exports no numerical critical
temperature, trap phase diagram, atom-species claim, material prediction, or
experimental result.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Mapping, Optional


REGIME = "bose_einstein_condensation"


class BECVerdict(str, Enum):
    SELECT_BEC_STRUCTURAL = "SELECT_BEC_STRUCTURAL"
    THERMAL_GAS_WINS = "THERMAL_GAS_WINS"
    MACROSCOPIC_OCCUPATION_INSUFFICIENT = "MACROSCOPIC_OCCUPATION_INSUFFICIENT"
    PHASE_COHERENCE_INSUFFICIENT = "PHASE_COHERENCE_INSUFFICIENT"
    SINGLE_MODE_DOMINANCE_INSUFFICIENT = "SINGLE_MODE_DOMINANCE_INSUFFICIENT"
    THERMAL_DEPLETION_OVERLOAD = "THERMAL_DEPLETION_OVERLOAD"
    FRAGMENTED_CONDENSATE_REFUSAL = "FRAGMENTED_CONDENSATE_REFUSAL"
    INTERACTION_INSTABILITY_OVERLOAD = "INTERACTION_INSTABILITY_OVERLOAD"
    TRAP_BOUNDARY_OVERLOAD = "TRAP_BOUNDARY_OVERLOAD"
    LOW_DIMENSION_FLUCTUATION_GUARD = "LOW_DIMENSION_FLUCTUATION_GUARD"
    FINITE_SIZE_ROUNDED_HOLD = "FINITE_SIZE_ROUNDED_HOLD"
    METASTABLE_HISTORY_LOCKED = "METASTABLE_HISTORY_LOCKED"
    OPEN_EVIDENCE_REQUIRED = "OPEN_EVIDENCE_REQUIRED"
    REFUSE_NUMERIC_TC_EXPORT = "REFUSE_NUMERIC_TC_EXPORT"
    REFUSE_TRAP_SPECIFIC_PHASE_DIAGRAM = "REFUSE_TRAP_SPECIFIC_PHASE_DIAGRAM"
    REFUSE_MATERIAL_SPECIFIC_BEC_CLAIM = "REFUSE_MATERIAL_SPECIFIC_BEC_CLAIM"
    REFUSE_WRONG_REGIME_CONTAMINATION = "REFUSE_WRONG_REGIME_CONTAMINATION"


class BECUniversalityRoute(str, Enum):
    O2_3D_XY = "O2_3D_XY"
    BKT_MARGINAL_2D = "BKT_MARGINAL_2D"
    MEAN_FIELD_GAUSSIAN_OR_TRAP = "MEAN_FIELD_GAUSSIAN_OR_TRAP"
    DISORDER_RELEVANT_PARALLEL = "DISORDER_RELEVANT_PARALLEL"
    FINITE_SIZE_ROUNDED = "FINITE_SIZE_ROUNDED"
    FRAGMENTED_CONDENSATE_LOCKED = "FRAGMENTED_CONDENSATE_LOCKED"
    NO_CLEAN_UNIVERSALITY_ROUTE = "NO_CLEAN_UNIVERSALITY_ROUTE"


COMMON_STATUS_MAP = {
    BECVerdict.SELECT_BEC_STRUCTURAL: "COHERENT_CODOMAIN_SELECTED",
    BECVerdict.THERMAL_GAS_WINS: "MARGIN_NONPOSITIVE",
    BECVerdict.MACROSCOPIC_OCCUPATION_INSUFFICIENT: "COHERENCE_INSUFFICIENT",
    BECVerdict.PHASE_COHERENCE_INSUFFICIENT: "PHASE_LOCK_FAILED",
    BECVerdict.SINGLE_MODE_DOMINANCE_INSUFFICIENT: "COHERENCE_INSUFFICIENT",
    BECVerdict.THERMAL_DEPLETION_OVERLOAD: "COHERENCE_INSUFFICIENT",
    BECVerdict.FRAGMENTED_CONDENSATE_REFUSAL: "COHERENCE_INSUFFICIENT",
    BECVerdict.INTERACTION_INSTABILITY_OVERLOAD: "COHERENCE_INSUFFICIENT",
    BECVerdict.TRAP_BOUNDARY_OVERLOAD: "COHERENCE_INSUFFICIENT",
    BECVerdict.LOW_DIMENSION_FLUCTUATION_GUARD: "COHERENCE_INSUFFICIENT",
    BECVerdict.FINITE_SIZE_ROUNDED_HOLD: "OPEN_EVIDENCE_REQUIRED",
    BECVerdict.METASTABLE_HISTORY_LOCKED: "METASTABLE_HISTORY_LOCKED",
    BECVerdict.OPEN_EVIDENCE_REQUIRED: "OPEN_EVIDENCE_REQUIRED",
    BECVerdict.REFUSE_NUMERIC_TC_EXPORT: "OPEN_EVIDENCE_REQUIRED",
    BECVerdict.REFUSE_TRAP_SPECIFIC_PHASE_DIAGRAM: "OPEN_EVIDENCE_REQUIRED",
    BECVerdict.REFUSE_MATERIAL_SPECIFIC_BEC_CLAIM: "OPEN_EVIDENCE_REQUIRED",
    BECVerdict.REFUSE_WRONG_REGIME_CONTAMINATION: "OPEN_EVIDENCE_REQUIRED",
}


@dataclass(frozen=True)
class BECNetwork:
    cost_fragmented: float
    cost_coherent: float
    fragmented_pressure: float = 0.0

    thermal_depletion_pressure: float = 0.0
    interaction_pressure: float = 0.0
    fragmentation_pressure: float = 0.0
    trap_boundary_pressure: float = 0.0
    phase_fluctuation_pressure: float = 0.0
    finite_size_pressure: float = 0.0
    dimensional_pressure: float = 0.0
    history_pressure: float = 0.0

    thermal_depletion_gate: float = 1.0
    interaction_gate: float = 1.0
    fragmentation_gate: float = 1.0
    trap_boundary_gate: float = 1.0
    phase_fluctuation_gate: float = 1.0
    finite_size_gate: float = 1.0
    dimensional_gate: float = 1.0
    history_gate: float = 1.0

    macroscopic_occupation: bool = True
    phase_lock: bool = True
    single_mode_dominance: bool = True
    condensate_fraction_evidence: bool = True
    history_barrier_cleared: bool = True

    symmetry_class: str = "O2"
    dimension: float = 3.0
    locality_class: str = "short_range"
    dynamics_class: str = "model_F"
    interaction_class: str = "weak_repulsive"
    trap_class: str = "bulk_or_thermodynamic"
    disorder_strength: float = 0.0
    harris_disorder_flag: bool = False
    mean_field_escape_flag: bool = False
    bkt_allowed: bool = False
    finite_size_rounding: bool = False
    fragmented_condensate_candidate: bool = False
    low_dimensional_guard_required: bool = True

    numeric_export_attempt: bool = False
    trap_specific_phase_diagram_attempt: bool = False
    material_specific_claim: bool = False
    target_value_consumed: bool = False
    wrong_regime_contamination: bool = False

    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def coherent_pressure(self) -> float:
        return (
            self.thermal_depletion_pressure
            + self.interaction_pressure
            + self.fragmentation_pressure
            + self.trap_boundary_pressure
            + self.phase_fluctuation_pressure
            + self.finite_size_pressure
            + self.dimensional_pressure
            + self.history_pressure
        )

    @property
    def margin(self) -> float:
        return self.cost_fragmented + self.fragmented_pressure - self.cost_coherent - self.coherent_pressure


@dataclass(frozen=True)
class BECEvaluationResult:
    regime: str
    margin: float
    verdict: BECVerdict
    common_status: str
    universality_route: BECUniversalityRoute
    critical_fields: Dict[str, Any]
    reason: str
    target_value_consumed: bool = False
    numeric_export: bool = False
    material_specific_export: bool = False
    trap_specific_export: bool = False

    def as_dict(self) -> Dict[str, Any]:
        return {
            "regime": self.regime,
            "margin": self.margin,
            "verdict": self.verdict.value,
            "common_status": self.common_status,
            "universality_route": self.universality_route.value,
            "critical_fields": dict(self.critical_fields),
            "reason": self.reason,
            "target_value_consumed": self.target_value_consumed,
            "numeric_export": self.numeric_export,
            "material_specific_export": self.material_specific_export,
            "trap_specific_export": self.trap_specific_export,
        }


def _bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return bool(value)


def _float(data: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    value = data.get(key, default)
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{key} must be numeric, got {value!r}") from exc


def load_bec_network(data: Mapping[str, Any]) -> BECNetwork:
    required = ["cost_fragmented", "cost_coherent"]
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"BEC network missing required keys: {missing}")

    return BECNetwork(
        cost_fragmented=_float(data, "cost_fragmented"),
        cost_coherent=_float(data, "cost_coherent"),
        fragmented_pressure=_float(data, "fragmented_pressure"),
        thermal_depletion_pressure=_float(data, "thermal_depletion_pressure"),
        interaction_pressure=_float(data, "interaction_pressure"),
        fragmentation_pressure=_float(data, "fragmentation_pressure"),
        trap_boundary_pressure=_float(data, "trap_boundary_pressure"),
        phase_fluctuation_pressure=_float(data, "phase_fluctuation_pressure"),
        finite_size_pressure=_float(data, "finite_size_pressure"),
        dimensional_pressure=_float(data, "dimensional_pressure"),
        history_pressure=_float(data, "history_pressure"),
        thermal_depletion_gate=_float(data, "thermal_depletion_gate", 1.0),
        interaction_gate=_float(data, "interaction_gate", 1.0),
        fragmentation_gate=_float(data, "fragmentation_gate", 1.0),
        trap_boundary_gate=_float(data, "trap_boundary_gate", 1.0),
        phase_fluctuation_gate=_float(data, "phase_fluctuation_gate", 1.0),
        finite_size_gate=_float(data, "finite_size_gate", 1.0),
        dimensional_gate=_float(data, "dimensional_gate", 1.0),
        history_gate=_float(data, "history_gate", 1.0),
        macroscopic_occupation=_bool(data.get("macroscopic_occupation", True), True),
        phase_lock=_bool(data.get("phase_lock", True), True),
        single_mode_dominance=_bool(data.get("single_mode_dominance", True), True),
        condensate_fraction_evidence=_bool(data.get("condensate_fraction_evidence", True), True),
        history_barrier_cleared=_bool(data.get("history_barrier_cleared", True), True),
        symmetry_class=str(data.get("symmetry_class", "O2")),
        dimension=_float(data, "dimension", 3.0),
        locality_class=str(data.get("locality_class", "short_range")),
        dynamics_class=str(data.get("dynamics_class", "model_F")),
        interaction_class=str(data.get("interaction_class", "weak_repulsive")),
        trap_class=str(data.get("trap_class", "bulk_or_thermodynamic")),
        disorder_strength=_float(data, "disorder_strength", 0.0),
        harris_disorder_flag=_bool(data.get("harris_disorder_flag", False)),
        mean_field_escape_flag=_bool(data.get("mean_field_escape_flag", False)),
        bkt_allowed=_bool(data.get("bkt_allowed", False)),
        finite_size_rounding=_bool(data.get("finite_size_rounding", False)),
        fragmented_condensate_candidate=_bool(data.get("fragmented_condensate_candidate", False)),
        low_dimensional_guard_required=_bool(data.get("low_dimensional_guard_required", True), True),
        numeric_export_attempt=_bool(data.get("numeric_export_attempt", False)),
        trap_specific_phase_diagram_attempt=_bool(data.get("trap_specific_phase_diagram_attempt", False)),
        material_specific_claim=_bool(data.get("material_specific_claim", False)),
        target_value_consumed=_bool(data.get("target_value_consumed", False)),
        wrong_regime_contamination=_bool(data.get("wrong_regime_contamination", False)),
        metadata=dict(data.get("metadata", {})),
    )


def route_bec_universality(network: BECNetwork) -> BECUniversalityRoute:
    sym = network.symmetry_class.strip().upper().replace("(", "").replace(")", "")
    locality = network.locality_class.strip().lower()
    interaction = network.interaction_class.strip().lower()
    trap = network.trap_class.strip().lower()

    if network.fragmented_condensate_candidate or network.fragmentation_pressure > network.fragmentation_gate:
        return BECUniversalityRoute.FRAGMENTED_CONDENSATE_LOCKED
    if network.finite_size_rounding or network.finite_size_pressure > network.finite_size_gate:
        return BECUniversalityRoute.FINITE_SIZE_ROUNDED
    if network.mean_field_escape_flag or locality in {"long_range", "global", "mean_field"} or "mean" in trap or interaction in {"ideal", "gaussian", "weak_ideal"}:
        return BECUniversalityRoute.MEAN_FIELD_GAUSSIAN_OR_TRAP
    if network.harris_disorder_flag or network.disorder_strength > 0.0:
        return BECUniversalityRoute.DISORDER_RELEVANT_PARALLEL
    if sym in {"O2", "U1", "U(1)", "XY", "BEC"}:
        if abs(network.dimension - 2.0) < 1e-9 and network.bkt_allowed:
            return BECUniversalityRoute.BKT_MARGINAL_2D
        if network.dimension >= 2.5:
            return BECUniversalityRoute.O2_3D_XY
    return BECUniversalityRoute.NO_CLEAN_UNIVERSALITY_ROUTE


def _result(network: BECNetwork, verdict: BECVerdict, reason: str, extra: Optional[Dict[str, Any]] = None) -> BECEvaluationResult:
    route = route_bec_universality(network)
    critical = {
        "cost_fragmented": network.cost_fragmented,
        "cost_coherent": network.cost_coherent,
        "fragmented_pressure": network.fragmented_pressure,
        "coherent_pressure": network.coherent_pressure,
        "thermal_depletion_pressure": network.thermal_depletion_pressure,
        "interaction_pressure": network.interaction_pressure,
        "fragmentation_pressure": network.fragmentation_pressure,
        "trap_boundary_pressure": network.trap_boundary_pressure,
        "phase_fluctuation_pressure": network.phase_fluctuation_pressure,
        "finite_size_pressure": network.finite_size_pressure,
        "dimensional_pressure": network.dimensional_pressure,
        "history_pressure": network.history_pressure,
        "symmetry_class": network.symmetry_class,
        "dimension": network.dimension,
        "locality_class": network.locality_class,
        "dynamics_class": network.dynamics_class,
        "interaction_class": network.interaction_class,
        "trap_class": network.trap_class,
    }
    if extra:
        critical.update(extra)
    return BECEvaluationResult(
        regime=REGIME,
        margin=network.margin,
        verdict=verdict,
        common_status=COMMON_STATUS_MAP[verdict],
        universality_route=route,
        critical_fields=critical,
        reason=reason,
        target_value_consumed=network.target_value_consumed,
        numeric_export=network.numeric_export_attempt,
        material_specific_export=network.material_specific_claim,
        trap_specific_export=network.trap_specific_phase_diagram_attempt,
    )


def evaluate_bec(network: BECNetwork) -> BECEvaluationResult:
    if network.wrong_regime_contamination:
        return _result(network, BECVerdict.REFUSE_WRONG_REGIME_CONTAMINATION, "wrong regime contamination: charged gauge, laser gain, or superfluid-only circulation machinery was supplied to the BEC evaluator")
    if network.numeric_export_attempt or network.target_value_consumed:
        return _result(network, BECVerdict.REFUSE_NUMERIC_TC_EXPORT, "numeric critical-temperature or target-value export attempt refused before margin evaluation")
    if network.trap_specific_phase_diagram_attempt:
        return _result(network, BECVerdict.REFUSE_TRAP_SPECIFIC_PHASE_DIAGRAM, "trap-specific phase-diagram export attempt refused")
    if network.material_specific_claim:
        return _result(network, BECVerdict.REFUSE_MATERIAL_SPECIFIC_BEC_CLAIM, "material- or atom-species-specific BEC claim refused")

    if not network.condensate_fraction_evidence:
        return _result(network, BECVerdict.OPEN_EVIDENCE_REQUIRED, "condensate-fraction evidence channel missing")
    if not network.macroscopic_occupation:
        return _result(network, BECVerdict.MACROSCOPIC_OCCUPATION_INSUFFICIENT, "no macroscopic single-mode occupation ledger")
    if not network.phase_lock:
        return _result(network, BECVerdict.PHASE_COHERENCE_INSUFFICIENT, "phase-coherence predicate failed")
    if not network.single_mode_dominance:
        return _result(network, BECVerdict.SINGLE_MODE_DOMINANCE_INSUFFICIENT, "single-mode dominance predicate failed")

    if network.thermal_depletion_pressure > network.thermal_depletion_gate:
        return _result(network, BECVerdict.THERMAL_DEPLETION_OVERLOAD, "thermal depletion pressure exceeds gate")
    if network.fragmented_condensate_candidate or network.fragmentation_pressure > network.fragmentation_gate:
        return _result(network, BECVerdict.FRAGMENTED_CONDENSATE_REFUSAL, "fragmented condensate ledger prevents one-codomain BEC promotion")
    if network.interaction_pressure > network.interaction_gate:
        return _result(network, BECVerdict.INTERACTION_INSTABILITY_OVERLOAD, "interaction pressure exceeds stability gate")
    if network.trap_boundary_pressure > network.trap_boundary_gate:
        return _result(network, BECVerdict.TRAP_BOUNDARY_OVERLOAD, "trap or boundary pressure exceeds gate")
    if network.phase_fluctuation_pressure > network.phase_fluctuation_gate:
        return _result(network, BECVerdict.PHASE_COHERENCE_INSUFFICIENT, "phase-fluctuation pressure exceeds gate")
    if network.low_dimensional_guard_required and network.dimension < 2.5 and not network.bkt_allowed:
        return _result(network, BECVerdict.LOW_DIMENSION_FLUCTUATION_GUARD, "low-dimensional fluctuation guard blocks ordinary BEC promotion")
    if network.dimensional_pressure > network.dimensional_gate:
        return _result(network, BECVerdict.LOW_DIMENSION_FLUCTUATION_GUARD, "dimensional fluctuation pressure exceeds gate")
    if network.finite_size_rounding or network.finite_size_pressure > network.finite_size_gate:
        return _result(network, BECVerdict.FINITE_SIZE_ROUNDED_HOLD, "finite-size rounding prevents sharp structural promotion")
    if not network.history_barrier_cleared or network.history_pressure > network.history_gate:
        return _result(network, BECVerdict.METASTABLE_HISTORY_LOCKED, "history barrier prevents codomain transition")
    if network.margin <= 0:
        return _result(network, BECVerdict.THERMAL_GAS_WINS, "fragmented occupation codomain remains cheaper after pressure")

    return _result(network, BECVerdict.SELECT_BEC_STRUCTURAL, "single-mode occupation plus phase codomain is admissibility-preferred and all audit gates pass")


def evaluate_bec_state(data: Mapping[str, Any]) -> Dict[str, Any]:
    return evaluate_bec(load_bec_network(data)).as_dict()
