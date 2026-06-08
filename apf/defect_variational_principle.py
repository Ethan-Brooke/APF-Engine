"""
APF Defect Variational Principle v1

Status: [P_architecture]

This module extends the Defect-Strata/Transition/Composition calculus
with a variational principle.

Core doctrine:
    APF processes select admissible continuations by minimizing weighted
    defect subject to finite capacity and irreversible-retention constraints.

This is architecture/math scaffolding only. It does not promote route-local
claims or assert a physical dynamics beyond existing certificates.
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
except Exception:  # pragma: no cover - standalone fallback
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


STATUS = "[P_architecture]"
MARKER = "DEFECT_VARIATIONAL_PRINCIPLE_PASS"
DEFECT_CHANNELS = ("preservation", "resolution", "route", "ledger", "smuggling")


class VariationalTarget(str, Enum):
    STABILIZATION = "stabilization"
    RECORD_FORMATION = "record_formation"
    ROUTE_REPAIR = "route_repair"
    RINGDOWN = "ringdown"
    HORIZON_RESOLUTION = "horizon_resolution"
    PERTURBATION_SUPPRESSION = "perturbation_suppression"
    GENERAL = "general"


@dataclass(frozen=True)
class DefectWeights:
    preservation: float = 1.0
    resolution: float = 1.0
    route: float = 1.0
    ledger: float = 1.0
    smuggling: float = 10.0

    def __post_init__(self) -> None:
        for name, value in self.as_dict().items():
            if value < 0:
                raise ValueError(f"Weight {name} must be nonnegative")

    def as_dict(self) -> dict[str, float]:
        return {
            "preservation": self.preservation,
            "resolution": self.resolution,
            "route": self.route,
            "ledger": self.ledger,
            "smuggling": self.smuggling,
        }


@dataclass(frozen=True)
class VariationalParameters:
    distance_weight: float = 1.0
    irreversible_weight: float = 1.0
    capacity_penalty_weight: float = 100.0
    defect_weights: DefectWeights = field(default_factory=DefectWeights)

    def __post_init__(self) -> None:
        for name in ("distance_weight", "irreversible_weight", "capacity_penalty_weight"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True)
class CandidateEvaluation:
    candidate: ContinuationCertificate
    objective_value: float
    defect_cost: float
    distance_cost: float
    irreversible_cost: float
    capacity_penalty: float
    target: VariationalTarget
    status: str = STATUS
    metadata: Mapping[str, Any] = field(default_factory=dict)


def weighted_defect_cost(defects: DefectVector, weights: DefectWeights = DefectWeights()) -> float:
    d = defects.as_dict()
    w = weights.as_dict()
    return sum(w[k] * d[k] for k in DEFECT_CHANNELS)


def capacity_violation(cert: ContinuationCertificate) -> float:
    if cert.capacity_cost is not None and cert.capacity_bound is not None:
        return max(0.0, float(cert.capacity_cost) - float(cert.capacity_bound))
    return 0.0 if cert.finite_continuability else 1.0


def apf_variational_objective(
    cert: ContinuationCertificate,
    *,
    distance_to_source: float = 0.0,
    irreversible_commitment: float = 0.0,
    params: VariationalParameters = VariationalParameters(),
    target: VariationalTarget = VariationalTarget.GENERAL,
) -> CandidateEvaluation:
    if distance_to_source < 0:
        raise ValueError("distance_to_source must be nonnegative")
    if irreversible_commitment < 0:
        raise ValueError("irreversible_commitment must be nonnegative")

    defect_cost = weighted_defect_cost(cert.defects(), params.defect_weights)
    distance_cost = params.distance_weight * distance_to_source
    irr_cost = params.irreversible_weight * irreversible_commitment
    cap_penalty = params.capacity_penalty_weight * capacity_violation(cert)
    objective = defect_cost + distance_cost + irr_cost + cap_penalty

    return CandidateEvaluation(
        candidate=cert,
        objective_value=objective,
        defect_cost=defect_cost,
        distance_cost=distance_cost,
        irreversible_cost=irr_cost,
        capacity_penalty=cap_penalty,
        target=target,
    )


def select_minimum(candidates: Sequence[CandidateEvaluation]) -> CandidateEvaluation:
    if not candidates:
        raise ValueError("At least one candidate evaluation is required")
    return min(candidates, key=lambda x: x.objective_value)


def evaluate_candidates(
    candidates: Sequence[ContinuationCertificate],
    *,
    distances: Optional[Mapping[str, float]] = None,
    irreversible_commitments: Optional[Mapping[str, float]] = None,
    params: VariationalParameters = VariationalParameters(),
    target: VariationalTarget = VariationalTarget.GENERAL,
) -> list[CandidateEvaluation]:
    distances = distances or {}
    irreversible_commitments = irreversible_commitments or {}
    return [
        apf_variational_objective(
            cert,
            distance_to_source=float(distances.get(cert.name, 0.0)),
            irreversible_commitment=float(irreversible_commitments.get(cert.name, 0.0)),
            params=params,
            target=target,
        )
        for cert in candidates
    ]


def variational_projection(
    candidates: Sequence[ContinuationCertificate],
    *,
    distances: Optional[Mapping[str, float]] = None,
    irreversible_commitments: Optional[Mapping[str, float]] = None,
    params: VariationalParameters = VariationalParameters(),
    target: VariationalTarget = VariationalTarget.GENERAL,
) -> CandidateEvaluation:
    return select_minimum(
        evaluate_candidates(
            candidates,
            distances=distances,
            irreversible_commitments=irreversible_commitments,
            params=params,
            target=target,
        )
    )


def target_weights(target: VariationalTarget) -> DefectWeights:
    if target == VariationalTarget.STABILIZATION:
        return DefectWeights(preservation=5.0, resolution=1.0, route=0.5, ledger=3.0, smuggling=10.0)
    if target == VariationalTarget.RECORD_FORMATION:
        return DefectWeights(preservation=3.0, resolution=5.0, route=0.5, ledger=3.0, smuggling=10.0)
    if target == VariationalTarget.ROUTE_REPAIR:
        return DefectWeights(preservation=2.0, resolution=3.0, route=5.0, ledger=4.0, smuggling=10.0)
    if target == VariationalTarget.RINGDOWN:
        return DefectWeights(preservation=6.0, resolution=1.0, route=0.0, ledger=4.0, smuggling=10.0)
    if target == VariationalTarget.HORIZON_RESOLUTION:
        return DefectWeights(preservation=2.0, resolution=6.0, route=0.0, ledger=4.0, smuggling=10.0)
    if target == VariationalTarget.PERTURBATION_SUPPRESSION:
        return DefectWeights(preservation=4.0, resolution=1.0, route=0.0, ledger=5.0, smuggling=10.0)
    return DefectWeights()


def params_for_target(
    target: VariationalTarget,
    *,
    distance_weight: float = 1.0,
    irreversible_weight: float = 1.0,
    capacity_penalty_weight: float = 100.0,
) -> VariationalParameters:
    return VariationalParameters(
        distance_weight=distance_weight,
        irreversible_weight=irreversible_weight,
        capacity_penalty_weight=capacity_penalty_weight,
        defect_weights=target_weights(target),
    )


def monotone_irreversible_retention(prior_commitment: float, later_commitment: float) -> bool:
    if prior_commitment < 0 or later_commitment < 0:
        raise ValueError("commitments must be nonnegative")
    return later_commitment >= prior_commitment


def collapse_projection_candidate(candidates: Sequence[ContinuationCertificate], *, distances=None, irreversible_commitments=None) -> CandidateEvaluation:
    return variational_projection(
        candidates,
        distances=distances,
        irreversible_commitments=irreversible_commitments,
        params=params_for_target(VariationalTarget.RECORD_FORMATION),
        target=VariationalTarget.RECORD_FORMATION,
    )


def ringdown_projection_candidate(candidates: Sequence[ContinuationCertificate], *, distances=None, irreversible_commitments=None) -> CandidateEvaluation:
    return variational_projection(
        candidates,
        distances=distances,
        irreversible_commitments=irreversible_commitments,
        params=params_for_target(VariationalTarget.RINGDOWN),
        target=VariationalTarget.RINGDOWN,
    )


def route_repair_projection_candidate(candidates: Sequence[ContinuationCertificate], *, distances=None, irreversible_commitments=None) -> CandidateEvaluation:
    return variational_projection(
        candidates,
        distances=distances,
        irreversible_commitments=irreversible_commitments,
        params=params_for_target(VariationalTarget.ROUTE_REPAIR),
        target=VariationalTarget.ROUTE_REPAIR,
    )


def variational_theorem_statement() -> str:
    return (
        "Defect Variational Principle: APF processes may be represented as "
        "constrained minimization of weighted defect plus distance, irreversible "
        "retention, and capacity-violation penalties over admissible continuations. "
        "This variational layer is architecture-level and does not promote "
        "route-local physical claims."
    )


def bank_marker() -> str:
    return MARKER
