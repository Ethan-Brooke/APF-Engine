"""Synchronization coherent-phase evaluator candidate.

Architecture-only intent: this module evaluates abstract interface-network ledgers.
It exports no numerical threshold, critical coupling, oscillator-network design,
material/device prediction, biological claim, or experimental result.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Mapping, Optional


REGIME = "synchronization"


class SynchronizationVerdict(str, Enum):
    SELECT_SYNCHRONIZED_STRUCTURAL = "SELECT_SYNCHRONIZED_STRUCTURAL"
    INDEPENDENT_OSCILLATOR_PHASES_WIN = "INDEPENDENT_OSCILLATOR_PHASES_WIN"
    PHASE_LOCK_FAILED = "PHASE_LOCK_FAILED"
    COUPLING_INSUFFICIENT = "COUPLING_INSUFFICIENT"
    DETUNING_SPREAD_OVERLOAD = "DETUNING_SPREAD_OVERLOAD"
    NOISE_OVERLOAD = "NOISE_OVERLOAD"
    NETWORK_FRUSTRATION_LOCKED = "NETWORK_FRUSTRATION_LOCKED"
    DRIVE_DISORDER_OVERLOAD = "DRIVE_DISORDER_OVERLOAD"
    TOPOLOGY_BOUNDARY_OVERLOAD = "TOPOLOGY_BOUNDARY_OVERLOAD"
    FINITE_SIZE_ROUNDED_HOLD = "FINITE_SIZE_ROUNDED_HOLD"
    METASTABLE_HISTORY_LOCKED = "METASTABLE_HISTORY_LOCKED"
    OPEN_EVIDENCE_REQUIRED = "OPEN_EVIDENCE_REQUIRED"
    REFUSE_NUMERIC_THRESHOLD_EXPORT = "REFUSE_NUMERIC_THRESHOLD_EXPORT"
    REFUSE_DEVICE_SPECIFIC_SYNC_CLAIM = "REFUSE_DEVICE_SPECIFIC_SYNC_CLAIM"
    REFUSE_WRONG_REGIME_CONTAMINATION = "REFUSE_WRONG_REGIME_CONTAMINATION"


class SynchronizationRoute(str, Enum):
    KURAMOTO_MEAN_FIELD_LOCKING = "KURAMOTO_MEAN_FIELD_LOCKING"
    LOCAL_XY_PHASE_LOCKING = "LOCAL_XY_PHASE_LOCKING"
    BKT_MARGINAL_2D = "BKT_MARGINAL_2D"
    DISORDER_RELEVANT_PARALLEL = "DISORDER_RELEVANT_PARALLEL"
    FRUSTRATED_NETWORK_GLASS_LOCKED = "FRUSTRATED_NETWORK_GLASS_LOCKED"
    NOISE_BROADENED_PARALLEL = "NOISE_BROADENED_PARALLEL"
    NO_CLEAN_UNIVERSALITY_ROUTE = "NO_CLEAN_UNIVERSALITY_ROUTE"


COMMON_STATUS_MAP = {
    SynchronizationVerdict.SELECT_SYNCHRONIZED_STRUCTURAL: "COHERENT_CODOMAIN_SELECTED",
    SynchronizationVerdict.INDEPENDENT_OSCILLATOR_PHASES_WIN: "MARGIN_NONPOSITIVE",
    SynchronizationVerdict.PHASE_LOCK_FAILED: "PHASE_LOCK_FAILED",
    SynchronizationVerdict.COUPLING_INSUFFICIENT: "COHERENCE_INSUFFICIENT",
    SynchronizationVerdict.DETUNING_SPREAD_OVERLOAD: "COHERENCE_INSUFFICIENT",
    SynchronizationVerdict.NOISE_OVERLOAD: "COHERENCE_INSUFFICIENT",
    SynchronizationVerdict.NETWORK_FRUSTRATION_LOCKED: "COHERENCE_INSUFFICIENT",
    SynchronizationVerdict.DRIVE_DISORDER_OVERLOAD: "COHERENCE_INSUFFICIENT",
    SynchronizationVerdict.TOPOLOGY_BOUNDARY_OVERLOAD: "COHERENCE_INSUFFICIENT",
    SynchronizationVerdict.FINITE_SIZE_ROUNDED_HOLD: "OPEN_EVIDENCE_REQUIRED",
    SynchronizationVerdict.METASTABLE_HISTORY_LOCKED: "METASTABLE_HISTORY_LOCKED",
    SynchronizationVerdict.OPEN_EVIDENCE_REQUIRED: "OPEN_EVIDENCE_REQUIRED",
    SynchronizationVerdict.REFUSE_NUMERIC_THRESHOLD_EXPORT: "OPEN_EVIDENCE_REQUIRED",
    SynchronizationVerdict.REFUSE_DEVICE_SPECIFIC_SYNC_CLAIM: "OPEN_EVIDENCE_REQUIRED",
    SynchronizationVerdict.REFUSE_WRONG_REGIME_CONTAMINATION: "OPEN_EVIDENCE_REQUIRED",
}


@dataclass(frozen=True)
class SynchronizationNetwork:
    cost_fragmented: float
    cost_coherent: float
    fragmented_pressure: float = 0.0

    detuning_pressure: float = 0.0
    coupling_deficit_pressure: float = 0.0
    noise_pressure: float = 0.0
    frustration_pressure: float = 0.0
    drive_disorder_pressure: float = 0.0
    topology_boundary_pressure: float = 0.0
    finite_size_pressure: float = 0.0
    history_pressure: float = 0.0

    detuning_gate: float = 1.0
    coupling_gate: float = 1.0
    noise_gate: float = 1.0
    frustration_gate: float = 1.0
    drive_disorder_gate: float = 1.0
    topology_boundary_gate: float = 1.0
    finite_size_gate: float = 1.0
    history_gate: float = 1.0

    phase_locked: bool = True
    coupling_declared: bool = True
    oscillator_network_declared: bool = True
    order_parameter_declared: bool = True
    history_barrier_cleared: bool = True
    finite_size_rounded_allowed: bool = False

    dimension: float = 3.0
    locality_class: str = "local_network"
    dynamics_class: str = "phase_oscillator"
    topology_class: str = "generic_connected_graph"
    symmetry_class: str = "U1_phase"
    disorder_strength: float = 0.0
    harris_disorder_flag: bool = False
    mean_field_escape_flag: bool = False
    finite_size_flag: bool = False
    frustrated_network_flag: bool = False
    noise_broadened_flag: bool = False
    bkt_candidate_flag: bool = False

    numeric_export_attempt: bool = False
    device_specific_claim: bool = False
    biological_or_neural_claim: bool = False
    target_value_consumed: bool = False
    wrong_regime_contamination: bool = False
    laser_relabel_contamination: bool = False
    bec_relabel_contamination: bool = False
    superconducting_gauge_contamination: bool = False

    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def coherent_pressure(self) -> float:
        return (
            self.detuning_pressure
            + self.coupling_deficit_pressure
            + self.noise_pressure
            + self.frustration_pressure
            + self.drive_disorder_pressure
            + self.topology_boundary_pressure
            + self.finite_size_pressure
            + self.history_pressure
        )

    @property
    def margin(self) -> float:
        return self.cost_fragmented + self.fragmented_pressure - self.cost_coherent - self.coherent_pressure


@dataclass(frozen=True)
class SynchronizationEvaluationResult:
    regime: str
    margin: float
    verdict: SynchronizationVerdict
    common_status: str
    transition_route: SynchronizationRoute
    gates: Dict[str, bool]
    critical_fields: Dict[str, Any]
    reason: str
    export_global_P: bool
    target_value_consumed: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "regime": self.regime,
            "margin": self.margin,
            "verdict": self.verdict.value,
            "common_status": self.common_status,
            "transition_route": self.transition_route.value,
            "gates": dict(self.gates),
            "critical_fields": dict(self.critical_fields),
            "reason": self.reason,
            "export_global_P": self.export_global_P,
            "target_value_consumed": self.target_value_consumed,
        }


def _as_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    return bool(value)


def _as_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"expected float-compatible value, got {value!r}") from exc


def load_synchronization_network(payload: Mapping[str, Any]) -> SynchronizationNetwork:
    """Load a plain dict into the typed synchronization network object."""
    required = ["cost_fragmented", "cost_coherent"]
    missing = [k for k in required if k not in payload]
    if missing:
        raise ValueError(f"missing required synchronization fields: {missing}")
    return SynchronizationNetwork(
        cost_fragmented=_as_float(payload.get("cost_fragmented")),
        cost_coherent=_as_float(payload.get("cost_coherent")),
        fragmented_pressure=_as_float(payload.get("fragmented_pressure")),
        detuning_pressure=_as_float(payload.get("detuning_pressure")),
        coupling_deficit_pressure=_as_float(payload.get("coupling_deficit_pressure")),
        noise_pressure=_as_float(payload.get("noise_pressure")),
        frustration_pressure=_as_float(payload.get("frustration_pressure")),
        drive_disorder_pressure=_as_float(payload.get("drive_disorder_pressure")),
        topology_boundary_pressure=_as_float(payload.get("topology_boundary_pressure")),
        finite_size_pressure=_as_float(payload.get("finite_size_pressure")),
        history_pressure=_as_float(payload.get("history_pressure")),
        detuning_gate=_as_float(payload.get("detuning_gate"), 1.0),
        coupling_gate=_as_float(payload.get("coupling_gate"), 1.0),
        noise_gate=_as_float(payload.get("noise_gate"), 1.0),
        frustration_gate=_as_float(payload.get("frustration_gate"), 1.0),
        drive_disorder_gate=_as_float(payload.get("drive_disorder_gate"), 1.0),
        topology_boundary_gate=_as_float(payload.get("topology_boundary_gate"), 1.0),
        finite_size_gate=_as_float(payload.get("finite_size_gate"), 1.0),
        history_gate=_as_float(payload.get("history_gate"), 1.0),
        phase_locked=_as_bool(payload.get("phase_locked"), True),
        coupling_declared=_as_bool(payload.get("coupling_declared"), True),
        oscillator_network_declared=_as_bool(payload.get("oscillator_network_declared"), True),
        order_parameter_declared=_as_bool(payload.get("order_parameter_declared"), True),
        history_barrier_cleared=_as_bool(payload.get("history_barrier_cleared"), True),
        finite_size_rounded_allowed=_as_bool(payload.get("finite_size_rounded_allowed"), False),
        dimension=_as_float(payload.get("dimension"), 3.0),
        locality_class=str(payload.get("locality_class", "local_network")),
        dynamics_class=str(payload.get("dynamics_class", "phase_oscillator")),
        topology_class=str(payload.get("topology_class", "generic_connected_graph")),
        symmetry_class=str(payload.get("symmetry_class", "U1_phase")),
        disorder_strength=_as_float(payload.get("disorder_strength"), 0.0),
        harris_disorder_flag=_as_bool(payload.get("harris_disorder_flag"), False),
        mean_field_escape_flag=_as_bool(payload.get("mean_field_escape_flag"), False),
        finite_size_flag=_as_bool(payload.get("finite_size_flag"), False),
        frustrated_network_flag=_as_bool(payload.get("frustrated_network_flag"), False),
        noise_broadened_flag=_as_bool(payload.get("noise_broadened_flag"), False),
        bkt_candidate_flag=_as_bool(payload.get("bkt_candidate_flag"), False),
        numeric_export_attempt=_as_bool(payload.get("numeric_export_attempt"), False),
        device_specific_claim=_as_bool(payload.get("device_specific_claim"), False),
        biological_or_neural_claim=_as_bool(payload.get("biological_or_neural_claim"), False),
        target_value_consumed=_as_bool(payload.get("target_value_consumed"), False),
        wrong_regime_contamination=_as_bool(payload.get("wrong_regime_contamination"), False),
        laser_relabel_contamination=_as_bool(payload.get("laser_relabel_contamination"), False),
        bec_relabel_contamination=_as_bool(payload.get("bec_relabel_contamination"), False),
        superconducting_gauge_contamination=_as_bool(payload.get("superconducting_gauge_contamination"), False),
        metadata=dict(payload.get("metadata", {})),
    )


def route_transition(network: SynchronizationNetwork) -> SynchronizationRoute:
    """Paper-11-style transition routing for synchronization claims."""
    if network.frustrated_network_flag or network.frustration_pressure > network.frustration_gate:
        return SynchronizationRoute.FRUSTRATED_NETWORK_GLASS_LOCKED
    if network.harris_disorder_flag or network.disorder_strength >= 0.5:
        return SynchronizationRoute.DISORDER_RELEVANT_PARALLEL
    if network.bkt_candidate_flag or (network.dimension <= 2.05 and network.symmetry_class.upper() in {"U1", "U1_PHASE", "O2", "O2_XY"}):
        return SynchronizationRoute.BKT_MARGINAL_2D
    if network.mean_field_escape_flag or network.locality_class in {"global", "all_to_all", "mean_field"}:
        return SynchronizationRoute.KURAMOTO_MEAN_FIELD_LOCKING
    if network.noise_broadened_flag or network.noise_pressure > 0.75 * max(network.noise_gate, 1e-12):
        return SynchronizationRoute.NOISE_BROADENED_PARALLEL
    if network.symmetry_class.upper() in {"U1", "U1_PHASE", "O2", "O2_XY"} and network.locality_class in {"local", "local_network", "short_range"}:
        return SynchronizationRoute.LOCAL_XY_PHASE_LOCKING
    return SynchronizationRoute.NO_CLEAN_UNIVERSALITY_ROUTE


def evaluate_synchronization(network: SynchronizationNetwork) -> SynchronizationEvaluationResult:
    """Evaluate a synchronization codomain-selection ledger."""
    route = route_transition(network)
    gates = {
        "margin_positive": network.margin > 0,
        "oscillator_network_declared": network.oscillator_network_declared,
        "coupling_declared": network.coupling_declared,
        "order_parameter_declared": network.order_parameter_declared,
        "phase_locked": network.phase_locked,
        "detuning_within_gate": network.detuning_pressure <= network.detuning_gate,
        "coupling_deficit_within_gate": network.coupling_deficit_pressure <= network.coupling_gate,
        "noise_within_gate": network.noise_pressure <= network.noise_gate,
        "frustration_within_gate": network.frustration_pressure <= network.frustration_gate,
        "drive_disorder_within_gate": network.drive_disorder_pressure <= network.drive_disorder_gate,
        "topology_boundary_within_gate": network.topology_boundary_pressure <= network.topology_boundary_gate,
        "finite_size_within_gate_or_declared_rounding": (network.finite_size_pressure <= network.finite_size_gate) or network.finite_size_rounded_allowed,
        "history_barrier_cleared": network.history_barrier_cleared and network.history_pressure <= network.history_gate,
        "no_numeric_export_attempt": not network.numeric_export_attempt,
        "no_device_specific_claim": not network.device_specific_claim,
        "no_biological_or_neural_claim": not network.biological_or_neural_claim,
        "no_target_value_consumed": not network.target_value_consumed,
        "no_wrong_regime_contamination": not (
            network.wrong_regime_contamination
            or network.laser_relabel_contamination
            or network.bec_relabel_contamination
            or network.superconducting_gauge_contamination
        ),
    }

    critical_fields: Dict[str, Any] = {
        "margin": network.margin,
        "coherent_pressure": network.coherent_pressure,
        "fragmented_pressure": network.fragmented_pressure,
        "dimension": network.dimension,
        "locality_class": network.locality_class,
        "dynamics_class": network.dynamics_class,
        "topology_class": network.topology_class,
        "symmetry_class": network.symmetry_class,
        "transition_route": route.value,
    }

    if network.numeric_export_attempt:
        verdict = SynchronizationVerdict.REFUSE_NUMERIC_THRESHOLD_EXPORT
        reason = "numeric synchronization threshold / critical-coupling export attempted"
    elif network.device_specific_claim or network.biological_or_neural_claim:
        verdict = SynchronizationVerdict.REFUSE_DEVICE_SPECIFIC_SYNC_CLAIM
        reason = "device-, organism-, or application-specific synchronization claim attempted"
    elif network.target_value_consumed:
        verdict = SynchronizationVerdict.REFUSE_NUMERIC_THRESHOLD_EXPORT
        reason = "target value consumed by evaluator"
    elif not gates["no_wrong_regime_contamination"]:
        verdict = SynchronizationVerdict.REFUSE_WRONG_REGIME_CONTAMINATION
        reason = "claim relabels another coherent regime as synchronization"
    elif not network.oscillator_network_declared or not network.order_parameter_declared:
        verdict = SynchronizationVerdict.OPEN_EVIDENCE_REQUIRED
        reason = "oscillator network or phase/order parameter not declared"
    elif not network.coupling_declared:
        verdict = SynchronizationVerdict.OPEN_EVIDENCE_REQUIRED
        reason = "coupling ledger is missing"
    elif network.margin <= 0:
        verdict = SynchronizationVerdict.INDEPENDENT_OSCILLATOR_PHASES_WIN
        reason = "fragmented independent-phase codomain remains cheaper"
    elif not network.phase_locked:
        verdict = SynchronizationVerdict.PHASE_LOCK_FAILED
        reason = "phase-lock predicate failed despite positive margin"
    elif network.coupling_deficit_pressure > network.coupling_gate:
        verdict = SynchronizationVerdict.COUPLING_INSUFFICIENT
        reason = "coupling-deficit pressure exceeds gate"
    elif network.detuning_pressure > network.detuning_gate:
        verdict = SynchronizationVerdict.DETUNING_SPREAD_OVERLOAD
        reason = "detuning spread exceeds gate"
    elif network.noise_pressure > network.noise_gate:
        verdict = SynchronizationVerdict.NOISE_OVERLOAD
        reason = "noise pressure exceeds gate"
    elif network.frustration_pressure > network.frustration_gate:
        verdict = SynchronizationVerdict.NETWORK_FRUSTRATION_LOCKED
        reason = "network frustration prevents clean phase-lock codomain selection"
    elif network.drive_disorder_pressure > network.drive_disorder_gate:
        verdict = SynchronizationVerdict.DRIVE_DISORDER_OVERLOAD
        reason = "drive disorder exceeds gate"
    elif network.topology_boundary_pressure > network.topology_boundary_gate:
        verdict = SynchronizationVerdict.TOPOLOGY_BOUNDARY_OVERLOAD
        reason = "network boundary/topology pressure exceeds gate"
    elif network.finite_size_pressure > network.finite_size_gate and network.finite_size_rounded_allowed:
        verdict = SynchronizationVerdict.FINITE_SIZE_ROUNDED_HOLD
        reason = "finite-size rounding declared; structural hold rather than promotion"
    elif network.finite_size_pressure > network.finite_size_gate:
        verdict = SynchronizationVerdict.TOPOLOGY_BOUNDARY_OVERLOAD
        reason = "finite-size pressure exceeds gate without rounding declaration"
    elif not gates["history_barrier_cleared"]:
        verdict = SynchronizationVerdict.METASTABLE_HISTORY_LOCKED
        reason = "instantaneous margin positive but history/realignment barrier is locked"
    else:
        verdict = SynchronizationVerdict.SELECT_SYNCHRONIZED_STRUCTURAL
        reason = "phase-locked oscillator codomain selected structurally"

    return SynchronizationEvaluationResult(
        regime=REGIME,
        margin=network.margin,
        verdict=verdict,
        common_status=COMMON_STATUS_MAP[verdict],
        transition_route=route,
        gates=gates,
        critical_fields=critical_fields,
        reason=reason,
        export_global_P=verdict == SynchronizationVerdict.SELECT_SYNCHRONIZED_STRUCTURAL,
        target_value_consumed=network.target_value_consumed,
    )


def evaluate_synchronization_payload(payload: Mapping[str, Any]) -> Dict[str, Any]:
    """Plain-dict entry point expected by a registry dispatcher."""
    return evaluate_synchronization(load_synchronization_network(payload)).to_dict()
