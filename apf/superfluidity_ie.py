"""
APF superfluidity Interface Engine runtime scaffold.

Structural-only evaluator. This module does not predict material-specific
lambda temperatures, critical velocities, helium phase diagrams, ultracold-gas
phase diagrams, or experimental results.

It checks whether an abstract neutral-flow interface ledger satisfies the APF
superfluid codomain criterion:

    S_SF = C(R_viscous) - C(R_SF) - Pi_SF > 0

plus neutral phase-lock and circulation-quantization gates.

Provenance: installed at v24.3.62 from sibling pack
``APF_SUPERFLUIDITY_CODOMAIN_ADAPTER_INTEGRATION_v3`` (upstream
``APF_SUPERFLUIDITY_IE_RUNTIME_SCAFFOLD_v2``), audited 2026-05-24. Parallels
``apf.superconductivity_ie`` as the neutral (gauge/winding/flux-free) sibling
evaluator. This is a runtime evaluator, not a bank module: it has no
``check_*`` functions and is not in the bank manifest. The Codomain Selection
Engine dispatches it via ``_adjudicate_superfluidity``; the bank-registered
checks live in ``apf.superfluidity_codomain_adapter``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import isfinite, pi
from typing import Dict, List, Tuple


def wrap_phase(delta: float) -> float:
    """Wrap a phase difference to [-pi, pi]."""
    return (delta + pi) % (2.0 * pi) - pi


class SFVerdict(str, Enum):
    SF_PHASE_CODOMAIN = "SF_PHASE_CODOMAIN"
    VISCOUS_FRAGMENTED_CODOMAIN = "VISCOUS_FRAGMENTED_CODOMAIN"
    PHASE_LOCK_FAILED = "PHASE_LOCK_FAILED"
    CIRCULATION_QUANTIZATION_FAILED = "CIRCULATION_QUANTIZATION_FAILED"
    VORTEX_OVERLOADED = "VORTEX_OVERLOADED"
    NORMAL_FRACTION_OVERLOADED = "NORMAL_FRACTION_OVERLOADED"
    CHARGED_GAUGE_CONTAMINATION = "CHARGED_GAUGE_CONTAMINATION"


@dataclass(frozen=True)
class SFInterfaceState:
    node_id: str
    capacity_C: float
    phase_phi: float
    phase_stiffness_sigma: float
    normal_fraction_eta: float
    local_defect_pressure_Pi: float = 0.0

    def validate(self) -> None:
        if not self.node_id:
            raise ValueError("node_id required")
        if self.capacity_C < 0 or not isfinite(self.capacity_C):
            raise ValueError("capacity_C must be finite and nonnegative")
        if not (0.0 <= self.phase_stiffness_sigma <= 1.0):
            raise ValueError("phase_stiffness_sigma must lie in [0,1]")
        if not (0.0 <= self.normal_fraction_eta <= 1.0):
            raise ValueError("normal_fraction_eta must lie in [0,1]")
        if self.local_defect_pressure_Pi < 0 or not isfinite(self.local_defect_pressure_Pi):
            raise ValueError("local_defect_pressure_Pi must be finite and nonnegative")


@dataclass(frozen=True)
class SFDefectPressure:
    thermal: float = 0.0
    vortex: float = 0.0
    boundary: float = 0.0
    normal_fraction: float = 0.0
    disorder: float = 0.0
    drive: float = 0.0

    def terms(self) -> Dict[str, float]:
        return {
            "thermal": self.thermal,
            "vortex": self.vortex,
            "boundary": self.boundary,
            "normal_fraction": self.normal_fraction,
            "disorder": self.disorder,
            "drive": self.drive,
        }

    def total(self) -> float:
        terms = self.terms()
        if any(x < 0 or not isfinite(x) for x in terms.values()):
            raise ValueError("defect terms must be finite and nonnegative")
        return sum(terms.values())


@dataclass(frozen=True)
class SFInterfaceNetwork:
    nodes: Dict[str, SFInterfaceState]
    edges: List[Tuple[str, str]]
    defects: SFDefectPressure = field(default_factory=SFDefectPressure)
    epsilon_phi: float = 0.20
    circulation_ratio: float = 1.0
    circulation_tolerance: float = 0.05
    vortex_overload_threshold: float = 1.0
    normal_fraction_threshold: float = 0.55
    charged_gauge_flux_required: bool = False

    def validate(self) -> None:
        if not self.nodes:
            raise ValueError("network must contain nodes")
        for node in self.nodes.values():
            node.validate()
        for a, b in self.edges:
            if a not in self.nodes or b not in self.nodes:
                raise ValueError(f"edge ({a},{b}) references missing node")
        if self.epsilon_phi <= 0 or not isfinite(self.epsilon_phi):
            raise ValueError("epsilon_phi must be positive finite")
        if self.circulation_tolerance < 0 or not isfinite(self.circulation_tolerance):
            raise ValueError("circulation_tolerance must be finite and nonnegative")
        if self.vortex_overload_threshold <= 0 or not isfinite(self.vortex_overload_threshold):
            raise ValueError("vortex_overload_threshold must be positive finite")
        if not (0.0 < self.normal_fraction_threshold <= 1.0):
            raise ValueError("normal_fraction_threshold must lie in (0,1]")

    def phase_locked_edges(self) -> bool:
        self.validate()
        for a, b in self.edges:
            da = wrap_phase(self.nodes[a].phase_phi - self.nodes[b].phase_phi)
            if abs(da) > self.epsilon_phi:
                return False
        return True

    def coherent_density(self) -> float:
        self.validate()
        return sum(n.phase_stiffness_sigma for n in self.nodes.values()) / len(self.nodes)

    def average_normal_fraction(self) -> float:
        self.validate()
        return sum(n.normal_fraction_eta for n in self.nodes.values()) / len(self.nodes)

    def local_defect_pressure(self) -> float:
        self.validate()
        return sum(n.local_defect_pressure_Pi for n in self.nodes.values())

    def circulation_quantized(self) -> bool:
        self.validate()
        nearest = round(self.circulation_ratio)
        return abs(self.circulation_ratio - nearest) <= self.circulation_tolerance


@dataclass(frozen=True)
class SFCostLedger:
    C_viscous: float
    C_superfluid: float

    def validate(self) -> None:
        if self.C_viscous < 0 or self.C_superfluid < 0:
            raise ValueError("costs must be nonnegative")
        if not isfinite(self.C_viscous) or not isfinite(self.C_superfluid):
            raise ValueError("costs must be finite")


@dataclass(frozen=True)
class SFEvaluation:
    admissibility_margin: float
    defect_pressure_total: float
    phase_locked: bool
    circulation_quantized: bool
    coherent_density: float
    average_normal_fraction: float
    selected_codomain: str
    verdict: SFVerdict
    exports: Dict[str, int]
    details: Dict[str, float]


def evaluate_sf_codomain(network: SFInterfaceNetwork, costs: SFCostLedger) -> SFEvaluation:
    """
    Structural superfluidity evaluator.

    The neutral superfluid codomain is selected iff:
      1. S_SF > 0,
      2. phase locking holds on coherent edges,
      3. circulation is integer-quantized in neutral circulation units,
      4. vortex pressure is not overloaded,
      5. normal-fraction load is below threshold,
      6. no charged-gauge/flux machinery is required.
    """
    network.validate()
    costs.validate()

    pi_defects = network.defects.total() + network.local_defect_pressure()
    margin = costs.C_viscous - costs.C_superfluid - pi_defects
    phase_locked = network.phase_locked_edges()
    quantized = network.circulation_quantized()
    rho = network.coherent_density()
    eta_n = network.average_normal_fraction()

    if network.charged_gauge_flux_required:
        verdict = SFVerdict.CHARGED_GAUGE_CONTAMINATION
    elif not phase_locked:
        verdict = SFVerdict.PHASE_LOCK_FAILED
    elif not quantized:
        verdict = SFVerdict.CIRCULATION_QUANTIZATION_FAILED
    elif network.defects.vortex >= network.vortex_overload_threshold:
        verdict = SFVerdict.VORTEX_OVERLOADED
    elif eta_n >= network.normal_fraction_threshold:
        verdict = SFVerdict.NORMAL_FRACTION_OVERLOADED
    elif margin > 0 and rho > 0:
        verdict = SFVerdict.SF_PHASE_CODOMAIN
    else:
        verdict = SFVerdict.VISCOUS_FRAGMENTED_CODOMAIN

    selected = (
        "NEUTRAL_SUPERFLUID_PHASE_CODOMAIN"
        if verdict == SFVerdict.SF_PHASE_CODOMAIN
        else "VISCOUS_OR_FRAGMENTED_MOMENTUM_CODOMAIN"
    )

    exports = {
        "SF_interface_runtime_scaffold": 1,
        "SF_admissibility_margin_evaluated_structural": 1,
        "SF_neutral_phase_codomain_selected_structural": int(verdict == SFVerdict.SF_PHASE_CODOMAIN),
        "SF_numeric_T_lambda": 0,
        "SF_numeric_critical_velocity": 0,
        "SF_helium_phase_diagram": 0,
        "SF_ultracold_gas_phase_diagram": 0,
        "SF_material_prediction": 0,
        "SF_ab_initio_chemistry": 0,
    }

    return SFEvaluation(
        admissibility_margin=margin,
        defect_pressure_total=pi_defects,
        phase_locked=phase_locked,
        circulation_quantized=quantized,
        coherent_density=rho,
        average_normal_fraction=eta_n,
        selected_codomain=selected,
        verdict=verdict,
        exports=exports,
        details={
            "Pi_defects": pi_defects,
            "C_viscous": costs.C_viscous,
            "C_superfluid": costs.C_superfluid,
            "circulation_ratio": network.circulation_ratio,
            "normal_fraction_eta_avg": eta_n,
            **network.defects.terms(),
        },
    )


def load_runtime_dict(data: dict) -> Tuple[SFInterfaceNetwork, SFCostLedger]:
    nodes = {item["node_id"]: SFInterfaceState(**item) for item in data["nodes"]}
    defects = SFDefectPressure(**data.get("defects", {}))
    network = SFInterfaceNetwork(
        nodes=nodes,
        edges=[tuple(e) for e in data["edges"]],
        defects=defects,
        epsilon_phi=data.get("epsilon_phi", 0.20),
        circulation_ratio=data.get("circulation_ratio", 1.0),
        circulation_tolerance=data.get("circulation_tolerance", 0.05),
        vortex_overload_threshold=data.get("vortex_overload_threshold", 1.0),
        normal_fraction_threshold=data.get("normal_fraction_threshold", 0.55),
        charged_gauge_flux_required=data.get("charged_gauge_flux_required", False),
    )
    costs = SFCostLedger(**data["costs"])
    return network, costs


# ---------------------------------------------------------------------------
# v4 audit-ladder layer (v24.3.63)
# ---------------------------------------------------------------------------
#
# Richer verdict lattice than the v2/v3 network evaluator above. Consumes the
# flat SF audit-state schema (coherence_score / thermal_pressure / vortex_* /
# boundary_pressure / metastable_history_locked / numeric_export_attempt /
# margin_to_fragmented / ...) and reproduces APF_SUPERFLUIDITY_IE_AUDIT_LADDER_v4
# SF-G0..SF-G7 exactly: hard refusals (numeric export, charged gauge) and the
# metastability / thermal / vortex / coherence gates all fire before the
# margin + total-score tie-break. The network evaluator stays the coarser
# runtime path; this is the post-integration audit fence.


class SFAuditVerdict(str, Enum):
    SELECT_SUPERFLUID_STRUCTURAL = "SELECT_SUPERFLUID_STRUCTURAL"
    HOLD_EVIDENCE_REQUIRED = "HOLD_EVIDENCE_REQUIRED"
    FRAGMENTED_WINS = "FRAGMENTED_WINS"
    COHERENCE_INSUFFICIENT = "COHERENCE_INSUFFICIENT"
    THERMAL_PRESSURE_OVERLOAD = "THERMAL_PRESSURE_OVERLOAD"
    VORTEX_DEFECT_OVERLOAD = "VORTEX_DEFECT_OVERLOAD"
    METASTABLE_HISTORY_LOCKED = "METASTABLE_HISTORY_LOCKED"
    REFUSE_CHARGED_GAUGE_CONTAMINATION = "REFUSE_CHARGED_GAUGE_CONTAMINATION"
    REFUSE_NUMERIC_EXPORT = "REFUSE_NUMERIC_EXPORT"


SF_AUDIT_THRESHOLDS = {
    "coherence_min": 0.70,
    "thermal_pressure_max": 0.70,
    "normal_fraction_max": 0.50,
    "vortex_pressure_max": 0.70,
    "vortex_defect_density_max": 0.50,
    "boundary_pressure_max": 0.70,
}

SF_FORBIDDEN_NUMERIC_EXPORTS = frozenset({
    "SF_numeric_T_lambda",
    "SF_numeric_critical_velocity",
    "SF_helium_phase_diagram",
    "SF_ultracold_gas_phase_diagram",
    "SF_material_prediction",
    "SF_ab_initio_chemistry",
    "SF_experimental_result",
    "SF_physical_final",
})

SF_FORBIDDEN_SC_MARKERS = frozenset({
    "charged_condensate",
    "electromagnetic_flux_quantization",
    "Cooper_pair",
    "Meissner_sector",
    "SC_winding_sector",
    "superconductivity_flux",
    "superconductivity_gauge",
})


def _sf_requested_numeric_export(state: dict) -> bool:
    if state.get("numeric_export_attempt"):
        return True
    requested = state.get("requested_exports", {}) or {}
    return any(requested.get(k, 0) not in (0, False, None) for k in SF_FORBIDDEN_NUMERIC_EXPORTS)


def _sf_has_gauge_contamination(state: dict) -> bool:
    if state.get("charged_gauge_contamination"):
        return True
    markers = set(state.get("forbidden_sc_markers", []) or [])
    return bool(markers & SF_FORBIDDEN_SC_MARKERS)


def is_sf_audit_state(data: dict) -> bool:
    """True if a dict is a flat v4 audit-state rather than a v2/v3 network ledger."""
    if "nodes" in data or "costs" in data:
        return False
    return any(k in data for k in (
        "coherence_score", "margin_to_fragmented", "thermal_pressure",
        "metastable_history_locked", "numeric_export_attempt",
    ))


def evaluate_sf_audit_state(state: dict) -> "SFAuditVerdict":
    """v4 audit-ladder evaluator.

    Reproduces APF_SUPERFLUIDITY_IE_AUDIT_LADDER_v4 SF-G0..SF-G7 promotion rule
    exactly. SELECT_SUPERFLUID_STRUCTURAL iff every gate passes and the
    fragmented-vs-coherent margin is strictly positive. Numeric-export and
    charged-gauge violations hard-refuse before margin evaluation.
    """
    t = SF_AUDIT_THRESHOLDS
    if state.get("regime_id") != "superfluidity":
        return SFAuditVerdict.HOLD_EVIDENCE_REQUIRED
    if state.get("target_engine") != "CODOMAIN_SELECTION" or state.get("atlas_axis") != "CODOMAIN":
        return SFAuditVerdict.HOLD_EVIDENCE_REQUIRED
    if _sf_requested_numeric_export(state):
        return SFAuditVerdict.REFUSE_NUMERIC_EXPORT
    if _sf_has_gauge_contamination(state):
        return SFAuditVerdict.REFUSE_CHARGED_GAUGE_CONTAMINATION
    if state.get("metastable_history_locked") or state.get("boundary_pressure", 0.0) >= t["boundary_pressure_max"]:
        return SFAuditVerdict.METASTABLE_HISTORY_LOCKED
    if state.get("thermal_pressure", 0.0) >= t["thermal_pressure_max"] or state.get("normal_fraction", 0.0) >= t["normal_fraction_max"]:
        return SFAuditVerdict.THERMAL_PRESSURE_OVERLOAD
    if state.get("vortex_pressure", 0.0) >= t["vortex_pressure_max"] or state.get("vortex_defect_density", 0.0) >= t["vortex_defect_density_max"]:
        return SFAuditVerdict.VORTEX_DEFECT_OVERLOAD
    if not state.get("phase_lock") or state.get("coherence_score", 0.0) < t["coherence_min"]:
        return SFAuditVerdict.COHERENCE_INSUFFICIENT
    if state.get("margin_to_fragmented", 0.0) <= 0.0:
        return SFAuditVerdict.FRAGMENTED_WINS
    if state.get("fragmented_total_score", 0.0) <= state.get("superfluid_total_score", 0.0):
        return SFAuditVerdict.FRAGMENTED_WINS
    return SFAuditVerdict.SELECT_SUPERFLUID_STRUCTURAL
