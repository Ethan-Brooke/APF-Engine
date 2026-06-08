"""Magnetism coherent-phase evaluator candidate.

Architecture-only intent: this module evaluates abstract interface-network ledgers.
It exports no numerical Curie temperature, material phase diagram, chemistry, or
experimental claim.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Mapping, Optional


REGIME = "magnetism"


class MagnetismVerdict(str, Enum):
    SELECT_MAGNETIC_STRUCTURAL = "SELECT_MAGNETIC_STRUCTURAL"
    FRAGMENTED_PARAMAGNET_WINS = "FRAGMENTED_PARAMAGNET_WINS"
    COHERENCE_INSUFFICIENT = "COHERENCE_INSUFFICIENT"
    THERMAL_DISORDER_OVERLOAD = "THERMAL_DISORDER_OVERLOAD"
    DOMAIN_DEFECT_OVERLOAD = "DOMAIN_DEFECT_OVERLOAD"
    FRUSTRATION_GLASS_LOCKED = "FRUSTRATION_GLASS_LOCKED"
    LOW_DIMENSION_FLUCTUATION_GUARD = "LOW_DIMENSION_FLUCTUATION_GUARD"
    METASTABLE_HISTORY_LOCKED = "METASTABLE_HISTORY_LOCKED"
    OPEN_EVIDENCE_REQUIRED = "OPEN_EVIDENCE_REQUIRED"
    REFUSE_NUMERIC_TC_EXPORT = "REFUSE_NUMERIC_TC_EXPORT"
    REFUSE_MATERIAL_SPECIFIC_MAGNET_CLAIM = "REFUSE_MATERIAL_SPECIFIC_MAGNET_CLAIM"
    REFUSE_WRONG_REGIME_CONTAMINATION = "REFUSE_WRONG_REGIME_CONTAMINATION"


class MagnetismUniversalityRoute(str, Enum):
    Z2_ISING = "Z2_ISING"
    O2_XY = "O2_XY"
    O3_HEISENBERG = "O3_HEISENBERG"
    BKT_MARGINAL = "BKT_MARGINAL"
    MEAN_FIELD_PARALLEL = "MEAN_FIELD_PARALLEL"
    DISORDER_RELEVANT_PARALLEL = "DISORDER_RELEVANT_PARALLEL"
    SPIN_GLASS_LOCKED = "SPIN_GLASS_LOCKED"
    NO_CLEAN_UNIVERSALITY_ROUTE = "NO_CLEAN_UNIVERSALITY_ROUTE"


COMMON_STATUS_MAP = {
    MagnetismVerdict.SELECT_MAGNETIC_STRUCTURAL: "COHERENT_CODOMAIN_SELECTED",
    MagnetismVerdict.FRAGMENTED_PARAMAGNET_WINS: "MARGIN_NONPOSITIVE",
    MagnetismVerdict.COHERENCE_INSUFFICIENT: "COHERENCE_INSUFFICIENT",
    MagnetismVerdict.THERMAL_DISORDER_OVERLOAD: "COHERENCE_INSUFFICIENT",
    MagnetismVerdict.DOMAIN_DEFECT_OVERLOAD: "COHERENCE_INSUFFICIENT",
    MagnetismVerdict.FRUSTRATION_GLASS_LOCKED: "COHERENCE_INSUFFICIENT",
    MagnetismVerdict.LOW_DIMENSION_FLUCTUATION_GUARD: "COHERENCE_INSUFFICIENT",
    MagnetismVerdict.METASTABLE_HISTORY_LOCKED: "METASTABLE_HISTORY_LOCKED",
    MagnetismVerdict.OPEN_EVIDENCE_REQUIRED: "OPEN_EVIDENCE_REQUIRED",
    MagnetismVerdict.REFUSE_NUMERIC_TC_EXPORT: "OPEN_EVIDENCE_REQUIRED",
    MagnetismVerdict.REFUSE_MATERIAL_SPECIFIC_MAGNET_CLAIM: "OPEN_EVIDENCE_REQUIRED",
    MagnetismVerdict.REFUSE_WRONG_REGIME_CONTAMINATION: "OPEN_EVIDENCE_REQUIRED",
}


@dataclass(frozen=True)
class MagnetismNetwork:
    cost_fragmented: float
    cost_coherent: float
    fragmented_pressure: float = 0.0

    thermal_pressure: float = 0.0
    domain_wall_pressure: float = 0.0
    frustration_pressure: float = 0.0
    disorder_pressure: float = 0.0
    anisotropy_pressure: float = 0.0
    dimensional_pressure: float = 0.0
    history_pressure: float = 0.0

    thermal_gate: float = 1.0
    domain_gate: float = 1.0
    frustration_gate: float = 1.0
    disorder_gate: float = 1.0
    dimensional_gate: float = 1.0
    history_gate: float = 1.0

    phase_lock: bool = True
    order_parameter_present: bool = True
    history_barrier_cleared: bool = True

    symmetry_class: str = "O3"
    dimension: float = 3.0
    locality_class: str = "short_range"
    dynamics_class: str = "model_A"
    anisotropy_class: str = "isotropic"
    disorder_strength: float = 0.0
    harris_disorder_flag: bool = False
    mean_field_escape_flag: bool = False
    spin_glass_candidate: bool = False
    bkt_allowed: bool = False
    low_dimensional_guard_required: bool = True

    numeric_export_attempt: bool = False
    material_specific_claim: bool = False
    target_value_consumed: bool = False
    wrong_regime_contamination: bool = False

    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def coherent_pressure(self) -> float:
        return (
            self.thermal_pressure
            + self.domain_wall_pressure
            + self.frustration_pressure
            + self.disorder_pressure
            + self.anisotropy_pressure
            + self.dimensional_pressure
            + self.history_pressure
        )

    @property
    def margin(self) -> float:
        return self.cost_fragmented + self.fragmented_pressure - self.cost_coherent - self.coherent_pressure


@dataclass(frozen=True)
class MagnetismEvaluationResult:
    regime: str
    margin: float
    verdict: MagnetismVerdict
    common_status: str
    universality_route: MagnetismUniversalityRoute
    critical_fields: Dict[str, Any]
    reason: str
    target_value_consumed: bool = False
    numeric_export: bool = False
    material_specific_export: bool = False

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


def load_magnetism_network(data: Mapping[str, Any]) -> MagnetismNetwork:
    required = ["cost_fragmented", "cost_coherent"]
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"magnetism network missing required keys: {missing}")

    return MagnetismNetwork(
        cost_fragmented=_float(data, "cost_fragmented"),
        cost_coherent=_float(data, "cost_coherent"),
        fragmented_pressure=_float(data, "fragmented_pressure"),
        thermal_pressure=_float(data, "thermal_pressure"),
        domain_wall_pressure=_float(data, "domain_wall_pressure"),
        frustration_pressure=_float(data, "frustration_pressure"),
        disorder_pressure=_float(data, "disorder_pressure"),
        anisotropy_pressure=_float(data, "anisotropy_pressure"),
        dimensional_pressure=_float(data, "dimensional_pressure"),
        history_pressure=_float(data, "history_pressure"),
        thermal_gate=_float(data, "thermal_gate", 1.0),
        domain_gate=_float(data, "domain_gate", 1.0),
        frustration_gate=_float(data, "frustration_gate", 1.0),
        disorder_gate=_float(data, "disorder_gate", 1.0),
        dimensional_gate=_float(data, "dimensional_gate", 1.0),
        history_gate=_float(data, "history_gate", 1.0),
        phase_lock=_bool(data.get("phase_lock", True), True),
        order_parameter_present=_bool(data.get("order_parameter_present", True), True),
        history_barrier_cleared=_bool(data.get("history_barrier_cleared", True), True),
        symmetry_class=str(data.get("symmetry_class", "O3")),
        dimension=_float(data, "dimension", 3.0),
        locality_class=str(data.get("locality_class", "short_range")),
        dynamics_class=str(data.get("dynamics_class", "model_A")),
        anisotropy_class=str(data.get("anisotropy_class", "isotropic")),
        disorder_strength=_float(data, "disorder_strength", 0.0),
        harris_disorder_flag=_bool(data.get("harris_disorder_flag", False)),
        mean_field_escape_flag=_bool(data.get("mean_field_escape_flag", False)),
        spin_glass_candidate=_bool(data.get("spin_glass_candidate", False)),
        bkt_allowed=_bool(data.get("bkt_allowed", False)),
        low_dimensional_guard_required=_bool(data.get("low_dimensional_guard_required", True), True),
        numeric_export_attempt=_bool(data.get("numeric_export_attempt", False)),
        material_specific_claim=_bool(data.get("material_specific_claim", False)),
        target_value_consumed=_bool(data.get("target_value_consumed", False)),
        wrong_regime_contamination=_bool(data.get("wrong_regime_contamination", False)),
        metadata=dict(data.get("metadata", {})),
    )


def route_magnetic_universality(network: MagnetismNetwork) -> MagnetismUniversalityRoute:
    sym = network.symmetry_class.strip().upper().replace("(", "").replace(")", "")
    locality = network.locality_class.strip().lower()

    if network.spin_glass_candidate or network.frustration_pressure > network.frustration_gate:
        return MagnetismUniversalityRoute.SPIN_GLASS_LOCKED
    if network.mean_field_escape_flag or locality in {"long_range", "global", "mean_field"}:
        return MagnetismUniversalityRoute.MEAN_FIELD_PARALLEL
    if network.harris_disorder_flag or network.disorder_strength > network.disorder_gate:
        return MagnetismUniversalityRoute.DISORDER_RELEVANT_PARALLEL
    if sym in {"Z2", "ISING", "DISCRETE_Z2"}:
        return MagnetismUniversalityRoute.Z2_ISING
    if sym in {"O2", "U1", "XY"}:
        if abs(network.dimension - 2.0) < 1e-9 and network.bkt_allowed:
            return MagnetismUniversalityRoute.BKT_MARGINAL
        return MagnetismUniversalityRoute.O2_XY
    if sym in {"O3", "HEISENBERG"}:
        return MagnetismUniversalityRoute.O3_HEISENBERG
    return MagnetismUniversalityRoute.NO_CLEAN_UNIVERSALITY_ROUTE


def _result(network: MagnetismNetwork, verdict: MagnetismVerdict, reason: str, extra: Optional[Dict[str, Any]] = None) -> MagnetismEvaluationResult:
    route = route_magnetic_universality(network)
    fields: Dict[str, Any] = {
        "cost_fragmented": network.cost_fragmented,
        "cost_coherent": network.cost_coherent,
        "fragmented_pressure": network.fragmented_pressure,
        "coherent_pressure": network.coherent_pressure,
        "thermal_pressure": network.thermal_pressure,
        "domain_wall_pressure": network.domain_wall_pressure,
        "frustration_pressure": network.frustration_pressure,
        "disorder_pressure": network.disorder_pressure,
        "anisotropy_pressure": network.anisotropy_pressure,
        "dimensional_pressure": network.dimensional_pressure,
        "history_pressure": network.history_pressure,
        "symmetry_class": network.symmetry_class,
        "dimension": network.dimension,
        "locality_class": network.locality_class,
        "dynamics_class": network.dynamics_class,
    }
    if extra:
        fields.update(extra)
    return MagnetismEvaluationResult(
        regime=REGIME,
        margin=network.margin,
        verdict=verdict,
        common_status=COMMON_STATUS_MAP[verdict],
        universality_route=route,
        critical_fields=fields,
        reason=reason,
        target_value_consumed=network.target_value_consumed,
        numeric_export=network.numeric_export_attempt,
        material_specific_export=network.material_specific_claim,
    )


def evaluate_magnetism_network(network: MagnetismNetwork) -> MagnetismEvaluationResult:
    # Hard refusals first: a favorable margin cannot outvote an inadmissible export.
    if network.numeric_export_attempt or network.target_value_consumed:
        return _result(network, MagnetismVerdict.REFUSE_NUMERIC_TC_EXPORT, "numeric Curie/Neel-temperature or target-value export attempt")
    if network.material_specific_claim:
        return _result(network, MagnetismVerdict.REFUSE_MATERIAL_SPECIFIC_MAGNET_CLAIM, "material-specific magnetism claim attempted")
    if network.wrong_regime_contamination:
        return _result(network, MagnetismVerdict.REFUSE_WRONG_REGIME_CONTAMINATION, "wrong-regime coherent machinery supplied to magnetism evaluator")

    # Evidence and audit gates.
    if not network.order_parameter_present or not network.phase_lock:
        return _result(network, MagnetismVerdict.COHERENCE_INSUFFICIENT, "spin-order evidence or phase/order lock insufficient")
    if not network.history_barrier_cleared or network.history_pressure > network.history_gate:
        return _result(network, MagnetismVerdict.METASTABLE_HISTORY_LOCKED, "history barrier not cleared")
    if network.thermal_pressure > network.thermal_gate:
        return _result(network, MagnetismVerdict.THERMAL_DISORDER_OVERLOAD, "thermal disorder pressure exceeds gate")
    if network.domain_wall_pressure > network.domain_gate:
        return _result(network, MagnetismVerdict.DOMAIN_DEFECT_OVERLOAD, "domain-wall pressure exceeds gate")
    if network.frustration_pressure > network.frustration_gate or network.spin_glass_candidate:
        return _result(network, MagnetismVerdict.FRUSTRATION_GLASS_LOCKED, "frustration/glass-locking pressure exceeds gate")

    continuous = network.symmetry_class.strip().upper() in {"O2", "U1", "XY", "O3", "HEISENBERG"}
    if network.low_dimensional_guard_required and continuous and network.dimension < 2.0:
        return _result(network, MagnetismVerdict.LOW_DIMENSION_FLUCTUATION_GUARD, "continuous symmetry below two dimensions trips fluctuation guard")
    if network.low_dimensional_guard_required and network.dimension == 2.0 and network.symmetry_class.strip().upper() in {"O3", "HEISENBERG"}:
        return _result(network, MagnetismVerdict.LOW_DIMENSION_FLUCTUATION_GUARD, "two-dimensional O(3) ledger requires explicit anisotropy or finite-size evidence")

    if network.margin <= 0:
        return _result(network, MagnetismVerdict.FRAGMENTED_PARAMAGNET_WINS, "magnetic coherent codomain margin is nonpositive")

    return _result(network, MagnetismVerdict.SELECT_MAGNETIC_STRUCTURAL, "magnetic coherent codomain selected structurally")


def evaluate_magnetism_state(data: Mapping[str, Any]) -> Dict[str, Any]:
    return evaluate_magnetism_network(load_magnetism_network(data)).as_dict()
