"""
APF Defect-Strata Calculus v1

Status: [P_architecture]

This module formalizes the APF object ladder

    A_Gamma ⊇ P_Gamma ⊇ O_Gamma ⊇ E_{Gamma,r}

as zero-defect strata over finite continuability.

It is architecture/math scaffolding only. It does not promote any
route-specific physics claim beyond its route-local certificates.

Core interpretation:
    - admissible: finite continuation exists
    - physical: preservation defect vanishes
    - observable: resolution defect vanishes
    - exported: route/export defect vanishes for route r
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Mapping, Optional, Sequence


STATUS = "[P_architecture]"
MARKER = "DEFECT_STRATA_CALCULUS_PASS"


class APFClass(str, Enum):
    """Typed APF class ladder."""
    FORMAL = "formal"
    ADMISSIBLE = "A_Gamma"
    PHYSICAL = "P_Gamma"
    OBSERVABLE = "O_Gamma"
    EXPORTED = "E_Gamma_r"


@dataclass(frozen=True)
class DefectVector:
    """
    Nonnegative defect coordinates.

    preservation:
        Vanishes iff admissible continuation preserves identity/stability.
    resolution:
        Vanishes iff physical structure resolves to a record/codomain.
    route:
        Vanishes iff route-local export gates close.
    ledger:
        Vanishes iff no hidden capacity debt remains.
    smuggling:
        Vanishes iff no hidden codomain/transport/evaluator substitution occurs.
    """
    preservation: float = 0.0
    resolution: float = 0.0
    route: float = 0.0
    ledger: float = 0.0
    smuggling: float = 0.0

    def __post_init__(self) -> None:
        for name, value in self.as_dict().items():
            if value < 0:
                raise ValueError(f"Defect {name} must be nonnegative, got {value!r}")

    def as_dict(self) -> dict[str, float]:
        return {
            "preservation": self.preservation,
            "resolution": self.resolution,
            "route": self.route,
            "ledger": self.ledger,
            "smuggling": self.smuggling,
        }

    def architecture_zero(self, tol: float = 0.0) -> bool:
        """All architecture-level defects vanish."""
        return (
            self.preservation <= tol
            and self.resolution <= tol
            and self.ledger <= tol
            and self.smuggling <= tol
        )

    def route_zero(self, tol: float = 0.0) -> bool:
        """All defects, including route/export, vanish."""
        return self.architecture_zero(tol=tol) and self.route <= tol


@dataclass(frozen=True)
class ContinuationCertificate:
    """
    Certificate for a candidate APF object X.

    This intentionally mirrors the CPR theorem shape:

        finite continuability
        preservation stability
        ledger coherence
        resolved codomain
        route closure

    `route_closed` is optional because route export is strictly below
    observable/resolved status.
    """
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

    def capacity_admissible(self) -> bool:
        """True unless explicit cost/bound are supplied and cost exceeds bound."""
        if self.capacity_cost is None or self.capacity_bound is None:
            return self.finite_continuability
        return self.finite_continuability and self.capacity_cost <= self.capacity_bound

    def defects(self) -> DefectVector:
        """
        Convert certificate failures into canonical defects.

        Values are structural indicators, not empirical residuals.
        """
        preservation = 0.0 if self.preservation_stability else 1.0
        resolution = 0.0 if self.resolved_codomain else 1.0
        route = 0.0 if self.route_closed else 1.0
        ledger = 0.0 if self.ledger_coherence and self.capacity_admissible() else 1.0
        smuggling = 0.0 if "smuggling" not in self.obstruction_channels else 1.0
        return DefectVector(
            preservation=preservation,
            resolution=resolution,
            route=route,
            ledger=ledger,
            smuggling=smuggling,
        )


def classify(cert: ContinuationCertificate, *, tol: float = 0.0) -> APFClass:
    """
    Classify a candidate object into the APF ladder.

        A_Gamma: finite continuability + capacity admissibility
        P_Gamma: A_Gamma + preservation defect zero
        O_Gamma: P_Gamma + resolution defect zero
        E_Gamma_r: O_Gamma + route defect zero

    Strictly architecture-safe: E_Gamma_r means route-closed according
    to this certificate, not global physical truth.
    """
    if not cert.capacity_admissible():
        return APFClass.FORMAL

    defects = cert.defects()

    if defects.preservation > tol or defects.ledger > tol or defects.smuggling > tol:
        return APFClass.ADMISSIBLE

    if defects.resolution > tol:
        return APFClass.PHYSICAL

    if defects.route > tol:
        return APFClass.OBSERVABLE

    return APFClass.EXPORTED


def is_admissible(cert: ContinuationCertificate) -> bool:
    return classify(cert) in {
        APFClass.ADMISSIBLE,
        APFClass.PHYSICAL,
        APFClass.OBSERVABLE,
        APFClass.EXPORTED,
    }


def is_physical(cert: ContinuationCertificate) -> bool:
    return classify(cert) in {
        APFClass.PHYSICAL,
        APFClass.OBSERVABLE,
        APFClass.EXPORTED,
    }


def is_observable(cert: ContinuationCertificate) -> bool:
    return classify(cert) in {
        APFClass.OBSERVABLE,
        APFClass.EXPORTED,
    }


def is_route_exported(cert: ContinuationCertificate) -> bool:
    return classify(cert) == APFClass.EXPORTED


def no_smuggling_guard(cert: ContinuationCertificate) -> bool:
    """
    No hidden route/codomain/evaluator substitution.

    Fails if certificate explicitly names smuggling or if route closure is
    claimed without resolved codomain.
    """
    if "smuggling" in cert.obstruction_channels:
        return False
    if cert.route_closed and not cert.resolved_codomain:
        return False
    return True


def class_transition(
    before: ContinuationCertificate,
    after: ContinuationCertificate,
) -> tuple[APFClass, APFClass]:
    """Return the APF class transition generated by an update/correction/flow."""
    return classify(before), classify(after)


def defect_reduction(
    before: ContinuationCertificate,
    after: ContinuationCertificate,
) -> dict[str, float]:
    """
    Positive value means a defect decreased.

    Useful for modeling measurement, decoherence, route repair, or
    interface-engine evidence reruns.
    """
    b = before.defects().as_dict()
    a = after.defects().as_dict()
    return {k: b[k] - a[k] for k in b}


def resolved_projection_candidate(
    cert: ContinuationCertificate,
    *,
    distance_to_record: float,
    irreversible_cost: float = 0.0,
    lam: float = 1.0,
    eta: float = 1.0,
) -> float:
    """
    Toy objective for observable projection:

        distance_to_record + lambda * Delta_O + eta * L_irr

    This is not a physical fit; it is a canonical objective-shape helper
    for comparing candidate projections.
    """
    if distance_to_record < 0 or irreversible_cost < 0:
        raise ValueError("distance_to_record and irreversible_cost must be nonnegative")
    return distance_to_record + lam * cert.defects().resolution + eta * irreversible_cost


def growth_suppression_factor(delta_preservation: float) -> float:
    """
    Minimal APF-compatible suppression ansatz:

        f(Delta_P) = 1 / (1 + Delta_P)

    GR recovery occurs at Delta_P = 0.
    """
    if delta_preservation < 0:
        raise ValueError("delta_preservation must be nonnegative")
    return 1.0 / (1.0 + delta_preservation)


def theorem_statement() -> str:
    return (
        "Defect-Strata Theorem: In a finite closed-world APF regime, "
        "the classes A_Gamma, P_Gamma, O_Gamma, and E_{Gamma,r} are "
        "zero-defect strata of finite continuability. Preservation, "
        "resolution, ledger, smuggling, and route defects determine "
        "membership and obstruction. This architecture does not promote "
        "route-local physical claims."
    )


def bank_marker() -> str:
    return MARKER
