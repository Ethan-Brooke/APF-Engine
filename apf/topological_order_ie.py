"""Topological-order coherent-phase evaluator candidate.

Architecture-only intent: this module evaluates abstract interface-network ledgers.
It exports no numerical gap, material phase diagram, anyon experiment, quantum
computer design, topological-code threshold, or hardware diagnostic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Mapping


REGIME = "topological_order"


class TopologicalOrderVerdict(str, Enum):
    SELECT_TOPOLOGICAL_ORDER_STRUCTURAL = "SELECT_TOPOLOGICAL_ORDER_STRUCTURAL"
    LOCAL_MICROSCOPIC_RECORDS_WIN = "LOCAL_MICROSCOPIC_RECORDS_WIN"
    GLOBAL_SECTOR_LEDGER_MISSING = "GLOBAL_SECTOR_LEDGER_MISSING"
    LOCAL_INDISTINGUISHABILITY_FAILED = "LOCAL_INDISTINGUISHABILITY_FAILED"
    GAP_INSUFFICIENT = "GAP_INSUFFICIENT"
    ANYON_DEFECT_OVERLOAD = "ANYON_DEFECT_OVERLOAD"
    BOUNDARY_DEFECT_OVERLOAD = "BOUNDARY_DEFECT_OVERLOAD"
    DISORDER_OVERLOAD = "DISORDER_OVERLOAD"
    LOCAL_ORDER_CONTAMINATION_REFUSED = "LOCAL_ORDER_CONTAMINATION_REFUSED"
    TOPOLOGICAL_DEGENERACY_INSUFFICIENT = "TOPOLOGICAL_DEGENERACY_INSUFFICIENT"
    BRAID_WINDING_LEDGER_MISSING = "BRAID_WINDING_LEDGER_MISSING"
    FINITE_SIZE_ROUNDED_HOLD = "FINITE_SIZE_ROUNDED_HOLD"
    METASTABLE_HISTORY_LOCKED = "METASTABLE_HISTORY_LOCKED"
    OPEN_EVIDENCE_REQUIRED = "OPEN_EVIDENCE_REQUIRED"
    REFUSE_NUMERIC_GAP_EXPORT = "REFUSE_NUMERIC_GAP_EXPORT"
    REFUSE_MATERIAL_SPECIFIC_TOPOLOGICAL_PHASE_CLAIM = "REFUSE_MATERIAL_SPECIFIC_TOPOLOGICAL_PHASE_CLAIM"
    REFUSE_WRONG_REGIME_CONTAMINATION = "REFUSE_WRONG_REGIME_CONTAMINATION"


class TopologicalOrderRoute(str, Enum):
    Z2_TOPOLOGICAL_SECTOR_ORDER = "Z2_TOPOLOGICAL_SECTOR_ORDER"
    CHERN_OR_FQH_BRAID_ORDER = "CHERN_OR_FQH_BRAID_ORDER"
    SPT_BOUNDARY_GUARDED = "SPT_BOUNDARY_GUARDED"
    TOPOLOGICAL_QUANTUM_CRITICAL_CANDIDATE = "TOPOLOGICAL_QUANTUM_CRITICAL_CANDIDATE"
    DISORDER_LOCALIZATION_PARALLEL = "DISORDER_LOCALIZATION_PARALLEL"
    FINITE_SIZE_TOPOLOGICAL_MEMORY_HOLD = "FINITE_SIZE_TOPOLOGICAL_MEMORY_HOLD"
    NO_CLEAN_UNIVERSALITY_ROUTE = "NO_CLEAN_UNIVERSALITY_ROUTE"


COMMON_STATUS_MAP = {
    TopologicalOrderVerdict.SELECT_TOPOLOGICAL_ORDER_STRUCTURAL: "COHERENT_CODOMAIN_SELECTED",
    TopologicalOrderVerdict.LOCAL_MICROSCOPIC_RECORDS_WIN: "MARGIN_NONPOSITIVE",
    TopologicalOrderVerdict.GLOBAL_SECTOR_LEDGER_MISSING: "OPEN_EVIDENCE_REQUIRED",
    TopologicalOrderVerdict.LOCAL_INDISTINGUISHABILITY_FAILED: "COHERENCE_INSUFFICIENT",
    TopologicalOrderVerdict.GAP_INSUFFICIENT: "COHERENCE_INSUFFICIENT",
    TopologicalOrderVerdict.ANYON_DEFECT_OVERLOAD: "COHERENCE_INSUFFICIENT",
    TopologicalOrderVerdict.BOUNDARY_DEFECT_OVERLOAD: "COHERENCE_INSUFFICIENT",
    TopologicalOrderVerdict.DISORDER_OVERLOAD: "COHERENCE_INSUFFICIENT",
    TopologicalOrderVerdict.LOCAL_ORDER_CONTAMINATION_REFUSED: "OPEN_EVIDENCE_REQUIRED",
    TopologicalOrderVerdict.TOPOLOGICAL_DEGENERACY_INSUFFICIENT: "COHERENCE_INSUFFICIENT",
    TopologicalOrderVerdict.BRAID_WINDING_LEDGER_MISSING: "OPEN_EVIDENCE_REQUIRED",
    TopologicalOrderVerdict.FINITE_SIZE_ROUNDED_HOLD: "OPEN_EVIDENCE_REQUIRED",
    TopologicalOrderVerdict.METASTABLE_HISTORY_LOCKED: "METASTABLE_HISTORY_LOCKED",
    TopologicalOrderVerdict.OPEN_EVIDENCE_REQUIRED: "OPEN_EVIDENCE_REQUIRED",
    TopologicalOrderVerdict.REFUSE_NUMERIC_GAP_EXPORT: "OPEN_EVIDENCE_REQUIRED",
    TopologicalOrderVerdict.REFUSE_MATERIAL_SPECIFIC_TOPOLOGICAL_PHASE_CLAIM: "OPEN_EVIDENCE_REQUIRED",
    TopologicalOrderVerdict.REFUSE_WRONG_REGIME_CONTAMINATION: "OPEN_EVIDENCE_REQUIRED",
}


@dataclass(frozen=True)
class TopologicalOrderNetwork:
    cost_fragmented: float
    cost_coherent: float
    fragmented_pressure: float = 0.0

    thermal_pressure: float = 0.0
    gap_pressure: float = 0.0
    anyon_defect_pressure: float = 0.0
    boundary_pressure: float = 0.0
    disorder_pressure: float = 0.0
    local_order_pressure: float = 0.0
    degeneracy_pressure: float = 0.0
    braid_winding_pressure: float = 0.0
    finite_size_pressure: float = 0.0
    history_pressure: float = 0.0

    thermal_gate: float = 1.0
    gap_gate: float = 1.0
    anyon_defect_gate: float = 1.0
    boundary_gate: float = 1.0
    disorder_gate: float = 1.0
    local_order_gate: float = 1.0
    degeneracy_gate: float = 1.0
    braid_winding_gate: float = 1.0
    finite_size_gate: float = 1.0
    history_gate: float = 1.0

    global_sector_declared: bool = True
    winding_or_braid_ledger_declared: bool = True
    local_indistinguishability_declared: bool = True
    local_indistinguishability_passed: bool = True
    topological_gap_declared: bool = True
    topological_degeneracy_declared: bool = True
    anyon_or_defect_sector_declared: bool = True
    boundary_condition_declared: bool = True
    history_barrier_cleared: bool = True
    finite_size_rounded_allowed: bool = False

    dimension: float = 2.0
    locality_class: str = "local"
    symmetry_class: str = "topological_sector"
    topology_class: str = "Z2_gauge"
    dynamics_class: str = "gapped_topological"
    disorder_strength: float = 0.0
    harris_disorder_flag: bool = False
    finite_size_flag: bool = False
    topological_quantum_critical_flag: bool = False
    chern_or_fqh_flag: bool = False
    spt_boundary_flag: bool = False

    numeric_export_attempt: bool = False
    material_specific_claim: bool = False
    hardware_or_code_threshold_claim: bool = False
    target_value_consumed: bool = False
    ordinary_symmetry_breaking_relabel: bool = False
    local_order_contamination: bool = False
    superconducting_flux_relabel: bool = False
    quantum_hall_numeric_relabel: bool = False
    mere_band_topology_claim: bool = False

    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def coherent_pressure(self) -> float:
        return (
            self.thermal_pressure
            + self.gap_pressure
            + self.anyon_defect_pressure
            + self.boundary_pressure
            + self.disorder_pressure
            + self.local_order_pressure
            + self.degeneracy_pressure
            + self.braid_winding_pressure
            + self.finite_size_pressure
            + self.history_pressure
        )

    @property
    def margin(self) -> float:
        return self.cost_fragmented + self.fragmented_pressure - self.cost_coherent - self.coherent_pressure


@dataclass(frozen=True)
class TopologicalOrderEvaluationResult:
    regime: str
    margin: float
    verdict: TopologicalOrderVerdict
    common_status: str
    transition_route: TopologicalOrderRoute
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


def load_topological_order_network(payload: Mapping[str, Any]) -> TopologicalOrderNetwork:
    required = ["cost_fragmented", "cost_coherent"]
    missing = [k for k in required if k not in payload]
    if missing:
        raise ValueError(f"missing required topological-order fields: {missing}")
    return TopologicalOrderNetwork(
        cost_fragmented=_as_float(payload.get("cost_fragmented")),
        cost_coherent=_as_float(payload.get("cost_coherent")),
        fragmented_pressure=_as_float(payload.get("fragmented_pressure")),
        thermal_pressure=_as_float(payload.get("thermal_pressure")),
        gap_pressure=_as_float(payload.get("gap_pressure")),
        anyon_defect_pressure=_as_float(payload.get("anyon_defect_pressure")),
        boundary_pressure=_as_float(payload.get("boundary_pressure")),
        disorder_pressure=_as_float(payload.get("disorder_pressure")),
        local_order_pressure=_as_float(payload.get("local_order_pressure")),
        degeneracy_pressure=_as_float(payload.get("degeneracy_pressure")),
        braid_winding_pressure=_as_float(payload.get("braid_winding_pressure")),
        finite_size_pressure=_as_float(payload.get("finite_size_pressure")),
        history_pressure=_as_float(payload.get("history_pressure")),
        thermal_gate=_as_float(payload.get("thermal_gate"), 1.0),
        gap_gate=_as_float(payload.get("gap_gate"), 1.0),
        anyon_defect_gate=_as_float(payload.get("anyon_defect_gate"), 1.0),
        boundary_gate=_as_float(payload.get("boundary_gate"), 1.0),
        disorder_gate=_as_float(payload.get("disorder_gate"), 1.0),
        local_order_gate=_as_float(payload.get("local_order_gate"), 1.0),
        degeneracy_gate=_as_float(payload.get("degeneracy_gate"), 1.0),
        braid_winding_gate=_as_float(payload.get("braid_winding_gate"), 1.0),
        finite_size_gate=_as_float(payload.get("finite_size_gate"), 1.0),
        history_gate=_as_float(payload.get("history_gate"), 1.0),
        global_sector_declared=_as_bool(payload.get("global_sector_declared"), True),
        winding_or_braid_ledger_declared=_as_bool(payload.get("winding_or_braid_ledger_declared"), True),
        local_indistinguishability_declared=_as_bool(payload.get("local_indistinguishability_declared"), True),
        local_indistinguishability_passed=_as_bool(payload.get("local_indistinguishability_passed"), True),
        topological_gap_declared=_as_bool(payload.get("topological_gap_declared"), True),
        topological_degeneracy_declared=_as_bool(payload.get("topological_degeneracy_declared"), True),
        anyon_or_defect_sector_declared=_as_bool(payload.get("anyon_or_defect_sector_declared"), True),
        boundary_condition_declared=_as_bool(payload.get("boundary_condition_declared"), True),
        history_barrier_cleared=_as_bool(payload.get("history_barrier_cleared"), True),
        finite_size_rounded_allowed=_as_bool(payload.get("finite_size_rounded_allowed"), False),
        dimension=_as_float(payload.get("dimension"), 2.0),
        locality_class=str(payload.get("locality_class", "local")),
        symmetry_class=str(payload.get("symmetry_class", "topological_sector")),
        topology_class=str(payload.get("topology_class", "Z2_gauge")),
        dynamics_class=str(payload.get("dynamics_class", "gapped_topological")),
        disorder_strength=_as_float(payload.get("disorder_strength"), 0.0),
        harris_disorder_flag=_as_bool(payload.get("harris_disorder_flag"), False),
        finite_size_flag=_as_bool(payload.get("finite_size_flag"), False),
        topological_quantum_critical_flag=_as_bool(payload.get("topological_quantum_critical_flag"), False),
        chern_or_fqh_flag=_as_bool(payload.get("chern_or_fqh_flag"), False),
        spt_boundary_flag=_as_bool(payload.get("spt_boundary_flag"), False),
        numeric_export_attempt=_as_bool(payload.get("numeric_export_attempt"), False),
        material_specific_claim=_as_bool(payload.get("material_specific_claim"), False),
        hardware_or_code_threshold_claim=_as_bool(payload.get("hardware_or_code_threshold_claim"), False),
        target_value_consumed=_as_bool(payload.get("target_value_consumed"), False),
        ordinary_symmetry_breaking_relabel=_as_bool(payload.get("ordinary_symmetry_breaking_relabel"), False),
        local_order_contamination=_as_bool(payload.get("local_order_contamination"), False),
        superconducting_flux_relabel=_as_bool(payload.get("superconducting_flux_relabel"), False),
        quantum_hall_numeric_relabel=_as_bool(payload.get("quantum_hall_numeric_relabel"), False),
        mere_band_topology_claim=_as_bool(payload.get("mere_band_topology_claim"), False),
        metadata=dict(payload.get("metadata", {})),
    )


def route_transition(network: TopologicalOrderNetwork) -> TopologicalOrderRoute:
    if network.finite_size_flag or (network.finite_size_pressure > network.finite_size_gate and network.finite_size_rounded_allowed):
        return TopologicalOrderRoute.FINITE_SIZE_TOPOLOGICAL_MEMORY_HOLD
    if network.harris_disorder_flag or network.disorder_strength >= 0.5:
        return TopologicalOrderRoute.DISORDER_LOCALIZATION_PARALLEL
    if network.topological_quantum_critical_flag or network.dynamics_class in {"topological_quantum_critical", "deconfined_critical"}:
        return TopologicalOrderRoute.TOPOLOGICAL_QUANTUM_CRITICAL_CANDIDATE
    if network.spt_boundary_flag or network.topology_class.upper() in {"SPT", "SYMMETRY_PROTECTED", "SPT_BOUNDARY"}:
        return TopologicalOrderRoute.SPT_BOUNDARY_GUARDED
    if network.chern_or_fqh_flag or network.topology_class.upper() in {"CHERN", "FQH", "FRACTIONAL_QUANTUM_HALL", "CHERN_BRAID"}:
        return TopologicalOrderRoute.CHERN_OR_FQH_BRAID_ORDER
    if network.topology_class.upper() in {"Z2", "Z2_GAUGE", "TORIC", "TORIC_CODE", "ANYONIC", "WINDING_BRAID"}:
        return TopologicalOrderRoute.Z2_TOPOLOGICAL_SECTOR_ORDER
    return TopologicalOrderRoute.NO_CLEAN_UNIVERSALITY_ROUTE


def evaluate_topological_order(network: TopologicalOrderNetwork) -> TopologicalOrderEvaluationResult:
    route = route_transition(network)
    wrong_regime = (
        network.ordinary_symmetry_breaking_relabel
        or network.superconducting_flux_relabel
        or network.quantum_hall_numeric_relabel
        or network.mere_band_topology_claim
    )
    gates = {
        "margin_positive": network.margin > 0,
        "global_sector_declared": network.global_sector_declared,
        "winding_or_braid_ledger_declared": network.winding_or_braid_ledger_declared,
        "local_indistinguishability_declared": network.local_indistinguishability_declared,
        "local_indistinguishability_passed": network.local_indistinguishability_passed,
        "topological_gap_declared": network.topological_gap_declared,
        "topological_degeneracy_declared": network.topological_degeneracy_declared,
        "anyon_or_defect_sector_declared": network.anyon_or_defect_sector_declared,
        "boundary_condition_declared": network.boundary_condition_declared,
        "thermal_within_gate": network.thermal_pressure <= network.thermal_gate,
        "gap_within_gate": network.gap_pressure <= network.gap_gate,
        "anyon_defect_within_gate": network.anyon_defect_pressure <= network.anyon_defect_gate,
        "boundary_within_gate": network.boundary_pressure <= network.boundary_gate,
        "disorder_within_gate": network.disorder_pressure <= network.disorder_gate,
        "local_order_within_gate": network.local_order_pressure <= network.local_order_gate,
        "degeneracy_within_gate": network.degeneracy_pressure <= network.degeneracy_gate,
        "braid_winding_within_gate": network.braid_winding_pressure <= network.braid_winding_gate,
        "finite_size_within_gate_or_declared_rounding": (network.finite_size_pressure <= network.finite_size_gate) or network.finite_size_rounded_allowed,
        "history_barrier_cleared": network.history_barrier_cleared and network.history_pressure <= network.history_gate,
        "no_numeric_export_attempt": not network.numeric_export_attempt,
        "no_material_specific_claim": not network.material_specific_claim,
        "no_hardware_or_code_threshold_claim": not network.hardware_or_code_threshold_claim,
        "no_target_value_consumed": not network.target_value_consumed,
        "no_wrong_regime_contamination": not wrong_regime,
    }
    critical_fields: Dict[str, Any] = {
        "margin": network.margin,
        "coherent_pressure": network.coherent_pressure,
        "fragmented_pressure": network.fragmented_pressure,
        "dimension": network.dimension,
        "locality_class": network.locality_class,
        "symmetry_class": network.symmetry_class,
        "topology_class": network.topology_class,
        "dynamics_class": network.dynamics_class,
        "transition_route": route.value,
    }

    if network.numeric_export_attempt or network.target_value_consumed:
        verdict = TopologicalOrderVerdict.REFUSE_NUMERIC_GAP_EXPORT
        reason = "numeric topological gap / threshold export attempted or target value consumed"
    elif network.material_specific_claim or network.hardware_or_code_threshold_claim:
        verdict = TopologicalOrderVerdict.REFUSE_MATERIAL_SPECIFIC_TOPOLOGICAL_PHASE_CLAIM
        reason = "material-, device-, hardware-, or code-threshold-specific claim attempted"
    elif wrong_regime:
        verdict = TopologicalOrderVerdict.REFUSE_WRONG_REGIME_CONTAMINATION
        reason = "ordinary symmetry breaking, superconducting flux, quantum-Hall numeric target, or band-topology relabel detected"
    elif network.local_order_contamination or network.local_order_pressure > network.local_order_gate:
        verdict = TopologicalOrderVerdict.LOCAL_ORDER_CONTAMINATION_REFUSED
        reason = "ordinary local-order explanation contaminates topological-order claim"
    elif not network.global_sector_declared:
        verdict = TopologicalOrderVerdict.GLOBAL_SECTOR_LEDGER_MISSING
        reason = "global sector ledger missing"
    elif not network.winding_or_braid_ledger_declared:
        verdict = TopologicalOrderVerdict.BRAID_WINDING_LEDGER_MISSING
        reason = "winding/braid ledger missing"
    elif not network.local_indistinguishability_declared or not network.local_indistinguishability_passed:
        verdict = TopologicalOrderVerdict.LOCAL_INDISTINGUISHABILITY_FAILED
        reason = "local indistinguishability gate failed or was not declared"
    elif not network.topological_gap_declared or network.gap_pressure > network.gap_gate:
        verdict = TopologicalOrderVerdict.GAP_INSUFFICIENT
        reason = "topological gap not declared or gap pressure exceeds gate"
    elif not network.topological_degeneracy_declared or network.degeneracy_pressure > network.degeneracy_gate:
        verdict = TopologicalOrderVerdict.TOPOLOGICAL_DEGENERACY_INSUFFICIENT
        reason = "topological degeneracy evidence insufficient"
    elif not network.anyon_or_defect_sector_declared or network.anyon_defect_pressure > network.anyon_defect_gate:
        verdict = TopologicalOrderVerdict.ANYON_DEFECT_OVERLOAD
        reason = "anyon/defect sector missing or overloaded"
    elif not network.boundary_condition_declared or network.boundary_pressure > network.boundary_gate:
        verdict = TopologicalOrderVerdict.BOUNDARY_DEFECT_OVERLOAD
        reason = "boundary condition missing or boundary pressure exceeds gate"
    elif network.disorder_pressure > network.disorder_gate:
        verdict = TopologicalOrderVerdict.DISORDER_OVERLOAD
        reason = "disorder pressure exceeds gate"
    elif network.margin <= 0:
        verdict = TopologicalOrderVerdict.LOCAL_MICROSCOPIC_RECORDS_WIN
        reason = "fragmented local microscopic records remain cheaper"
    elif network.finite_size_pressure > network.finite_size_gate and network.finite_size_rounded_allowed:
        verdict = TopologicalOrderVerdict.FINITE_SIZE_ROUNDED_HOLD
        reason = "finite-size topological-memory hold declared rather than promotion"
    elif network.finite_size_pressure > network.finite_size_gate:
        verdict = TopologicalOrderVerdict.OPEN_EVIDENCE_REQUIRED
        reason = "finite-size pressure exceeds gate without declared rounding"
    elif not gates["history_barrier_cleared"]:
        verdict = TopologicalOrderVerdict.METASTABLE_HISTORY_LOCKED
        reason = "instantaneous margin positive but topological-sector history barrier is locked"
    else:
        verdict = TopologicalOrderVerdict.SELECT_TOPOLOGICAL_ORDER_STRUCTURAL
        reason = "global sector / winding / braid codomain selected structurally"

    return TopologicalOrderEvaluationResult(
        regime=REGIME,
        margin=network.margin,
        verdict=verdict,
        common_status=COMMON_STATUS_MAP[verdict],
        transition_route=route,
        gates=gates,
        critical_fields=critical_fields,
        reason=reason,
        export_global_P=verdict == TopologicalOrderVerdict.SELECT_TOPOLOGICAL_ORDER_STRUCTURAL,
        target_value_consumed=network.target_value_consumed,
    )


def evaluate_topological_order_payload(payload: Mapping[str, Any]) -> Dict[str, Any]:
    return evaluate_topological_order(load_topological_order_network(payload)).to_dict()
