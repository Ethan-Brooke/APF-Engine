"""
APF Defect Transition Dynamics v1

Status: [P_architecture]

This module extends the Defect-Strata Calculus with transition laws.

Core doctrine:
    Physical events are defect-class transitions.

A transition occurs when a candidate structure changes APF class because
one or more defect coordinates vanish, become nonzero, or cross a boundary.

This is architecture/math scaffolding only. It does not promote route-local
claims or assert a physical dynamics beyond existing certificates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, Any, Optional

try:
    from apf.continuability_preservation_resolution import (
        APFClass,
        ContinuationCertificate,
        DefectVector,
        classify,
        defect_reduction,
    )
except Exception:  # pragma: no cover
    class APFClass(str, Enum):
        FORMAL = "formal"
        ADMISSIBLE = "A_Gamma"
        PHYSICAL = "P_Gamma"
        OBSERVABLE = "O_Gamma"
        EXPORTED = "E_Gamma_r"

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

    def classify(cert: ContinuationCertificate, *, tol: float = 0.0) -> APFClass:
        if not cert.finite_continuability:
            return APFClass.FORMAL
        d = cert.defects()
        if d.preservation > tol or d.ledger > tol or d.smuggling > tol:
            return APFClass.ADMISSIBLE
        if d.resolution > tol:
            return APFClass.PHYSICAL
        if d.route > tol:
            return APFClass.OBSERVABLE
        return APFClass.EXPORTED

    def defect_reduction(before: ContinuationCertificate, after: ContinuationCertificate) -> dict[str, float]:
        b = before.defects().as_dict()
        a = after.defects().as_dict()
        return {k: b[k] - a[k] for k in b}


STATUS = "[P_architecture]"
MARKER = "DEFECT_TRANSITION_DYNAMICS_PASS"


class TransitionKind(str, Enum):
    NO_CHANGE = "no_change"
    STABILIZATION = "A_to_P"
    RECORD_FORMATION = "P_to_O"
    ROUTE_EXPORT = "O_to_E"
    PRESERVATION_BREAKDOWN = "P_to_A"
    RESOLUTION_LOSS = "O_to_P"
    ROUTE_DECERTIFICATION = "E_to_O"
    FORMALIZATION = "formal_to_A"
    CAPACITY_FAILURE = "A_to_formal"
    MIXED = "mixed_transition"


CLASS_ORDER = {
    APFClass.FORMAL: 0,
    APFClass.ADMISSIBLE: 1,
    APFClass.PHYSICAL: 2,
    APFClass.OBSERVABLE: 3,
    APFClass.EXPORTED: 4,
}


@dataclass(frozen=True)
class DefectVelocity:
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
class TransitionCertificate:
    before: ContinuationCertificate
    after: ContinuationCertificate
    before_class: APFClass
    after_class: APFClass
    kind: TransitionKind
    defect_delta: Mapping[str, float]
    status: str = STATUS
    metadata: Mapping[str, Any] = field(default_factory=dict)


def defect_velocity(before: ContinuationCertificate, after: ContinuationCertificate, *, dt: float = 1.0) -> DefectVelocity:
    if dt <= 0:
        raise ValueError("dt must be positive")
    b = before.defects().as_dict()
    a = after.defects().as_dict()
    return DefectVelocity(**{k: (a[k] - b[k]) / dt for k in b})


def transition_kind(before_class: APFClass, after_class: APFClass) -> TransitionKind:
    if before_class == after_class:
        return TransitionKind.NO_CHANGE
    pair = (before_class, after_class)
    if pair == (APFClass.ADMISSIBLE, APFClass.PHYSICAL):
        return TransitionKind.STABILIZATION
    if pair == (APFClass.PHYSICAL, APFClass.OBSERVABLE):
        return TransitionKind.RECORD_FORMATION
    if pair == (APFClass.OBSERVABLE, APFClass.EXPORTED):
        return TransitionKind.ROUTE_EXPORT
    if pair == (APFClass.PHYSICAL, APFClass.ADMISSIBLE):
        return TransitionKind.PRESERVATION_BREAKDOWN
    if pair == (APFClass.OBSERVABLE, APFClass.PHYSICAL):
        return TransitionKind.RESOLUTION_LOSS
    if pair == (APFClass.EXPORTED, APFClass.OBSERVABLE):
        return TransitionKind.ROUTE_DECERTIFICATION
    if pair == (APFClass.FORMAL, APFClass.ADMISSIBLE):
        return TransitionKind.FORMALIZATION
    if pair == (APFClass.ADMISSIBLE, APFClass.FORMAL):
        return TransitionKind.CAPACITY_FAILURE
    return TransitionKind.MIXED


def certify_transition(before: ContinuationCertificate, after: ContinuationCertificate, *, tol: float = 0.0, metadata: Optional[Mapping[str, Any]] = None) -> TransitionCertificate:
    bc = classify(before, tol=tol)
    ac = classify(after, tol=tol)
    return TransitionCertificate(
        before=before,
        after=after,
        before_class=bc,
        after_class=ac,
        kind=transition_kind(bc, ac),
        defect_delta=defect_reduction(before, after),
        metadata=metadata or {},
    )


def is_upward_transition(t: TransitionCertificate) -> bool:
    return CLASS_ORDER[t.after_class] > CLASS_ORDER[t.before_class]


def is_downward_transition(t: TransitionCertificate) -> bool:
    return CLASS_ORDER[t.after_class] < CLASS_ORDER[t.before_class]


def transition_boundary_hit(cert: ContinuationCertificate, velocity: DefectVelocity, *, defect: str, tol: float = 0.0) -> bool:
    defects = cert.defects().as_dict()
    velocities = velocity.as_dict()
    if defect not in defects:
        raise KeyError(f"Unknown defect coordinate {defect!r}")
    return abs(defects[defect]) <= tol and abs(velocities[defect]) > tol


def measurement_transition(before: ContinuationCertificate, after: ContinuationCertificate) -> bool:
    t = certify_transition(before, after)
    return t.kind == TransitionKind.RECORD_FORMATION and t.defect_delta["resolution"] > 0


def ringdown_transition(before: ContinuationCertificate, after: ContinuationCertificate) -> bool:
    t = certify_transition(before, after)
    return t.defect_delta["preservation"] > 0 and CLASS_ORDER[t.after_class] >= CLASS_ORDER[APFClass.PHYSICAL]


def route_repair_transition(before: ContinuationCertificate, after: ContinuationCertificate) -> bool:
    t = certify_transition(before, after)
    return t.kind == TransitionKind.ROUTE_EXPORT and t.defect_delta["route"] > 0


def horizon_condition_external(*, internally_physical: bool, external_resolution_defect: float, drive_to_zero_available: bool) -> bool:
    if external_resolution_defect < 0:
        raise ValueError("external_resolution_defect must be nonnegative")
    return internally_physical and external_resolution_defect > 0 and not drive_to_zero_available


def event_theorem_statement() -> str:
    return (
        "Defect Transition Theorem: Physical events in APF are class transitions "
        "between zero-defect strata of finite continuability. Measurement, route "
        "export, ringdown, horizon formation, and obstruction repair are typed "
        "instances of defect coordinates vanishing, becoming nonzero, or crossing "
        "a boundary. This theorem is architecture-level and does not promote "
        "route-local physical claims."
    )


def bank_marker() -> str:
    return MARKER
