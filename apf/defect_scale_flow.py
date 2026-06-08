"""
APF Defect Scale Flow v1

Status: [P_architecture]

This module extends the defect calculus with scale/refinement flow.

Core doctrine:
    Scale selection and coarse-graining are defect-flow problems.
    A physically preferred scale is a stable or stationary point of the
    relevant defect functional under admissible refinement/coarse-graining.

This is architecture/math scaffolding only. It does not promote route-local
claims or assert a physical RG dynamics beyond existing certificates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Optional, Sequence

try:
    from apf.continuability_preservation_resolution import (
        ContinuationCertificate,
        DefectVector,
    )
except Exception:  # pragma: no cover
    @dataclass(frozen=True)
    class DefectVector:
        preservation: float = 0.0
        resolution: float = 0.0
        route: float = 0.0
        ledger: float = 0.0
        smuggling: float = 0.0
        def as_dict(self) -> dict[str, float]:
            return {
                "preservation": self.preservation,
                "resolution": self.resolution,
                "route": self.route,
                "ledger": self.ledger,
                "smuggling": self.smuggling,
            }

    @dataclass(frozen=True)
    class ContinuationCertificate:
        name: str
        finite_continuability: bool
        preservation_stability: bool
        ledger_coherence: bool
        resolved_codomain: bool
        route_closed: bool = False
        route: Optional[str] = None
        capacity_cost: Optional[float] = None
        capacity_bound: Optional[float] = None
        obstruction_channels: tuple[str, ...] = field(default_factory=tuple)
        metadata: Mapping[str, Any] = field(default_factory=dict)
        def defects(self) -> DefectVector:
            return DefectVector(
                preservation=0.0 if self.preservation_stability else 1.0,
                resolution=0.0 if self.resolved_codomain else 1.0,
                route=0.0 if self.route_closed else 1.0,
                ledger=0.0 if self.ledger_coherence else 1.0,
                smuggling=1.0 if "smuggling" in self.obstruction_channels else 0.0,
            )

try:
    from apf.defect_variational_principle import (
        DefectWeights,
        weighted_defect_cost,
    )
except Exception:  # pragma: no cover
    @dataclass(frozen=True)
    class DefectWeights:
        preservation: float = 1.0
        resolution: float = 1.0
        route: float = 1.0
        ledger: float = 1.0
        smuggling: float = 10.0
        def as_dict(self) -> dict[str, float]:
            return {
                "preservation": self.preservation,
                "resolution": self.resolution,
                "route": self.route,
                "ledger": self.ledger,
                "smuggling": self.smuggling,
            }

    def weighted_defect_cost(defects: DefectVector, weights: DefectWeights = DefectWeights()) -> float:
        d = defects.as_dict()
        w = weights.as_dict()
        return sum(w[k] * d[k] for k in d)


STATUS = "[P_architecture]"
MARKER = "DEFECT_SCALE_FLOW_PASS"


class ScaleFlowKind(str, Enum):
    REFINEMENT = "refinement"
    COARSE_GRAINING = "coarse_graining"
    ROUTE_TRANSPORT = "route_transport"
    RENORMALIZATION = "renormalization"
    OBSERVER_RESOLUTION = "observer_resolution"


@dataclass(frozen=True)
class ScalePoint:
    """
    A candidate object at a scale.

    scale may be physical scale, route scale, resolution depth, or refinement index.
    """
    scale: float
    certificate: ContinuationCertificate
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.scale <= 0:
            raise ValueError("scale must be positive")


@dataclass(frozen=True)
class ScaleFlowCertificate:
    """
    Defect-flow certificate over an ordered sequence of scale points.
    """
    points: tuple[ScalePoint, ...]
    kind: ScaleFlowKind
    weights: DefectWeights = field(default_factory=DefectWeights)
    status: str = STATUS
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if len(self.points) < 2:
            raise ValueError("ScaleFlowCertificate requires at least two scale points")


def defect_cost_at(point: ScalePoint, weights: DefectWeights = DefectWeights()) -> float:
    return weighted_defect_cost(point.certificate.defects(), weights)


def ordered_points(flow: ScaleFlowCertificate) -> tuple[ScalePoint, ...]:
    """Return points sorted by scale."""
    return tuple(sorted(flow.points, key=lambda p: p.scale))


def finite_difference(values: Sequence[float], xs: Sequence[float]) -> list[float]:
    """
    First finite differences dy/dx between adjacent points.
    """
    if len(values) != len(xs):
        raise ValueError("values and xs must have same length")
    if len(values) < 2:
        raise ValueError("need at least two points")
    out = []
    for i in range(len(values) - 1):
        dx = xs[i + 1] - xs[i]
        if dx == 0:
            raise ValueError("duplicate scale values")
        out.append((values[i + 1] - values[i]) / dx)
    return out


def defect_cost_profile(flow: ScaleFlowCertificate) -> list[tuple[float, float]]:
    pts = ordered_points(flow)
    return [(p.scale, defect_cost_at(p, flow.weights)) for p in pts]


def defect_beta_profile(flow: ScaleFlowCertificate) -> list[tuple[float, float]]:
    """
    Architecture-level beta profile:
        beta_Delta = d(weighted_defect)/d(log scale)
    """
    pts = ordered_points(flow)
    scales = [p.scale for p in pts]
    # avoid importing math for simplicity? use natural log.
    import math
    logs = [math.log(s) for s in scales]
    costs = [defect_cost_at(p, flow.weights) for p in pts]
    betas = finite_difference(costs, logs)
    midpoints = [(scales[i] * scales[i + 1]) ** 0.5 for i in range(len(betas))]
    return list(zip(midpoints, betas))


def stable_scale_candidates(flow: ScaleFlowCertificate) -> list[ScalePoint]:
    """
    Interior local minima of weighted defect cost.
    """
    pts = ordered_points(flow)
    costs = [defect_cost_at(p, flow.weights) for p in pts]
    out = []
    for i in range(1, len(pts) - 1):
        if costs[i] <= costs[i - 1] and costs[i] <= costs[i + 1]:
            out.append(pts[i])
    return out


def preferred_scale(flow: ScaleFlowCertificate) -> ScalePoint:
    """
    Scale point with globally minimal weighted defect.
    """
    pts = ordered_points(flow)
    return min(pts, key=lambda p: defect_cost_at(p, flow.weights))


def is_defect_monotone_decreasing(flow: ScaleFlowCertificate) -> bool:
    profile = defect_cost_profile(flow)
    costs = [c for _, c in profile]
    return all(costs[i + 1] <= costs[i] for i in range(len(costs) - 1))


def is_defect_monotone_increasing(flow: ScaleFlowCertificate) -> bool:
    profile = defect_cost_profile(flow)
    costs = [c for _, c in profile]
    return all(costs[i + 1] >= costs[i] for i in range(len(costs) - 1))


def scale_stationarity_witness(
    flow: ScaleFlowCertificate,
    *,
    tolerance: float = 1e-12,
) -> list[float]:
    """
    Return scales where adjacent beta estimates change sign or approach zero.
    """
    beta = defect_beta_profile(flow)
    witnesses = []
    for scale, value in beta:
        if abs(value) <= tolerance:
            witnesses.append(scale)
    for i in range(len(beta) - 1):
        s0, b0 = beta[i]
        s1, b1 = beta[i + 1]
        if b0 == 0 or b1 == 0:
            continue
        if (b0 < 0 < b1) or (b0 > 0 > b1):
            witnesses.append((s0 * s1) ** 0.5)
    return witnesses


def refinement_instability(flow: ScaleFlowCertificate) -> bool:
    """
    Refinement instability: defect cost increases monotonically under increasing scale index.
    Interpreted as refinement adding unresolved burden rather than resolving it.
    """
    return flow.kind == ScaleFlowKind.REFINEMENT and is_defect_monotone_increasing(flow)


def coarse_graining_resolution(flow: ScaleFlowCertificate) -> bool:
    """
    Coarse-graining resolution: defect cost decreases monotonically under coarse-graining.
    """
    return flow.kind == ScaleFlowKind.COARSE_GRAINING and is_defect_monotone_decreasing(flow)


def route_scale_selection(flow: ScaleFlowCertificate) -> ScalePoint:
    """
    Route-scale selector: choose the scale minimizing route-sensitive defect.
    """
    return preferred_scale(flow)


def gr_recovery_at_scale(point: ScalePoint, *, tolerance: float = 0.0) -> bool:
    """
    GR-like recovery in perturbative applications:
    preservation and ledger defects vanish at scale.
    """
    d = point.certificate.defects()
    return d.preservation <= tolerance and d.ledger <= tolerance


def suppression_from_scale_defect(point: ScalePoint, weights: DefectWeights = DefectWeights()) -> float:
    """
    Minimal scale-flow suppression ansatz:
        f = 1 / (1 + weighted_defect)
    """
    cost = defect_cost_at(point, weights)
    return 1.0 / (1.0 + cost)


def scale_flow_theorem_statement() -> str:
    return (
        "Defect Scale-Flow Theorem: APF scale selection, coarse-graining, "
        "renormalization, and observer-resolution effects may be represented "
        "as flows of weighted defect over admissible scale points. Preferred "
        "scales are stable or minimal defect strata. This theorem is "
        "architecture-level and does not promote route-local physical claims."
    )


def bank_marker() -> str:
    return MARKER
