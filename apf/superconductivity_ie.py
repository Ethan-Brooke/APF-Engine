"""
APF superconductivity Interface Engine audit ladder.

Structural-only evaluator. It classifies toy interface networks into SC or fail-closed
states using the APF superconducting admissibility margin:

    S_SC = C(R_N) - C(R_SC) - Pi_defects

and phase-locking / coherence predicates.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from math import pi, isfinite
from typing import Dict, List, Tuple


def wrap_phase(delta: float) -> float:
    return (delta + pi) % (2.0 * pi) - pi


@dataclass(frozen=True)
class IEInterfaceState:
    node_id: str
    capacity_C: float
    phase_phi: float
    coherence_sigma: float
    defect_pressure_Pi: float = 0.0
    charge_q: float = 2.0

    def validate(self) -> None:
        if not self.node_id:
            raise ValueError("node_id required")
        if self.capacity_C < 0 or not isfinite(self.capacity_C):
            raise ValueError("capacity_C finite nonnegative required")
        if not (0.0 <= self.coherence_sigma <= 1.0):
            raise ValueError("coherence_sigma in [0,1] required")
        if self.defect_pressure_Pi < 0 or not isfinite(self.defect_pressure_Pi):
            raise ValueError("defect_pressure_Pi finite nonnegative required")


@dataclass(frozen=True)
class SCDefectAlgebra:
    thermal: float = 0.0
    gauge: float = 0.0
    disorder: float = 0.0
    competition: float = 0.0
    boundary: float = 0.0
    vortex: float = 0.0

    def total(self) -> float:
        vals = [self.thermal, self.gauge, self.disorder, self.competition, self.boundary, self.vortex]
        if any(v < 0 or not isfinite(v) for v in vals):
            raise ValueError("all defect terms finite nonnegative required")
        return sum(vals)


@dataclass(frozen=True)
class SCCostLedger:
    C_normal: float
    C_superconducting: float

    def validate(self) -> None:
        if self.C_normal < 0 or self.C_superconducting < 0:
            raise ValueError("costs nonnegative required")
        if not isfinite(self.C_normal) or not isfinite(self.C_superconducting):
            raise ValueError("costs finite required")


@dataclass(frozen=True)
class SCInterfaceNetwork:
    nodes: Dict[str, IEInterfaceState]
    edges: List[Tuple[str, str]]
    defects: SCDefectAlgebra = field(default_factory=SCDefectAlgebra)
    epsilon_phi: float = 0.25
    min_rho_coh: float = 0.5
    winding_sector_n: int = 0
    flux_sector_phi: float = 0.0

    def validate(self) -> None:
        if not self.nodes:
            raise ValueError("nodes required")
        for n in self.nodes.values():
            n.validate()
        for a, b in self.edges:
            if a not in self.nodes or b not in self.nodes:
                raise ValueError("edge references missing node")
        if self.epsilon_phi <= 0:
            raise ValueError("epsilon_phi positive required")
        if not (0.0 <= self.min_rho_coh <= 1.0):
            raise ValueError("min_rho_coh in [0,1] required")
        if int(self.winding_sector_n) != self.winding_sector_n:
            raise ValueError("winding sector integer required")

    def max_phase_gap(self) -> float:
        self.validate()
        if not self.edges:
            return 0.0
        return max(abs(wrap_phase(self.nodes[a].phase_phi - self.nodes[b].phase_phi)) for a, b in self.edges)

    def phase_locked_edges(self) -> bool:
        return self.max_phase_gap() <= self.epsilon_phi

    def coherent_density(self) -> float:
        self.validate()
        return sum(n.coherence_sigma for n in self.nodes.values()) / len(self.nodes)

    def local_defect_pressure(self) -> float:
        self.validate()
        return sum(n.defect_pressure_Pi for n in self.nodes.values())


@dataclass(frozen=True)
class SCEvaluation:
    admissibility_margin: float
    phase_locked: bool
    coherent_density: float
    max_phase_gap: float
    total_defect_pressure: float
    selected_codomain: str
    reason: str
    exports: Dict[str, int]


def classify_codomain(margin: float, phase_locked: bool, rho: float, min_rho: float) -> Tuple[str, str]:
    if margin <= 0:
        return "DEFECT_OVERLOADED", "S_SC <= 0; defect/cost penalties erase codomain-compression gain"
    if not phase_locked:
        return "PHASE_FRAGMENTED", "phase-locking condition fails on at least one coherent edge"
    if rho < min_rho:
        return "NORMAL_OR_COMPETING_CODOMAIN", "coherent density below threshold"
    return "SC_PHASE_CODOMAIN", "positive margin, phase locked, coherent density sufficient"


def evaluate_sc_codomain(network: SCInterfaceNetwork, costs: SCCostLedger) -> SCEvaluation:
    network.validate()
    costs.validate()
    total_defects = network.defects.total() + network.local_defect_pressure()
    margin = costs.C_normal - costs.C_superconducting - total_defects
    phase_locked = network.phase_locked_edges()
    rho = network.coherent_density()
    selected, reason = classify_codomain(margin, phase_locked, rho, network.min_rho_coh)

    return SCEvaluation(
        admissibility_margin=margin,
        phase_locked=phase_locked,
        coherent_density=rho,
        max_phase_gap=network.max_phase_gap(),
        total_defect_pressure=total_defects,
        selected_codomain=selected,
        reason=reason,
        exports={
            "SC_IE_audit_ladder": 1,
            "SC_selected_codomain_structural": int(selected == "SC_PHASE_CODOMAIN"),
            "SC_fail_closed_classification": int(selected != "SC_PHASE_CODOMAIN"),
            "SC_numeric_Tc": 0,
            "SC_material_prediction": 0,
            "SC_highTc_solved": 0,
        },
    )


def load_network_dict(data: dict) -> Tuple[SCInterfaceNetwork, SCCostLedger]:
    nodes = {item["node_id"]: IEInterfaceState(**item) for item in data["nodes"]}
    network = SCInterfaceNetwork(
        nodes=nodes,
        edges=[tuple(e) for e in data["edges"]],
        defects=SCDefectAlgebra(**data.get("defects", {})),
        epsilon_phi=data.get("epsilon_phi", 0.25),
        min_rho_coh=data.get("min_rho_coh", 0.5),
        winding_sector_n=data.get("winding_sector_n", 0),
        flux_sector_phi=data.get("flux_sector_phi", 0.0),
    )
    costs = SCCostLedger(**data["costs"])
    return network, costs
