"""
APF Defect Falsifier Gate Logic v1

Status: [P_architecture]

This module extends the defect calculus with gate/falsifier logic.

Core doctrine:
    A persistent nonzero defect is not a nuisance; it is either:
        - an open gate,
        - a repair target,
        - a regime boundary,
        - a route-local obstruction,
        - or a falsifier if the claimed status requires that defect to vanish.

This is architecture/math scaffolding only. It does not promote route-local
claims or assert empirical falsification beyond declared thresholds.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Optional, Sequence

try:
    from apf.continuability_preservation_resolution import (
        APFClass,
        ContinuationCertificate,
        DefectVector,
        classify,
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


STATUS = "[P_architecture]"
MARKER = "DEFECT_FALSIFIER_GATE_LOGIC_PASS"
DEFECT_CHANNELS = ("preservation", "resolution", "route", "ledger", "smuggling")


class GateVerdict(str, Enum):
    PASS_ = "PASS"
    OPEN = "OPEN"
    REPAIR_TARGET = "REPAIR_TARGET"
    REGIME_BOUNDARY = "REGIME_BOUNDARY"
    ROUTE_OBSTRUCTION = "ROUTE_OBSTRUCTION"
    FALSIFIER = "FALSIFIER"


class ClaimStrength(str, Enum):
    ARCHITECTURE = "architecture"
    ADMISSIBLE = "admissible"
    PHYSICAL = "physical"
    OBSERVABLE = "observable"
    ROUTE_EXPORTED = "route_exported"


@dataclass(frozen=True)
class GateRequirement:
    """
    Required defect constraints for a claim.

    required_zero:
        Channels that must vanish for the claim.
    threshold:
        Channel-specific tolerated defect before failure.
    persistent_required:
        If True, a single nonzero event is open/repair; persistent nonzero is falsifier.
    """
    name: str
    claim_strength: ClaimStrength
    required_zero: tuple[str, ...]
    threshold: Mapping[str, float] = field(default_factory=dict)
    persistent_required: bool = True
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GateEvaluation:
    requirement: GateRequirement
    certificate: ContinuationCertificate
    verdict: GateVerdict
    active_defects: Mapping[str, float]
    status: str = STATUS
    metadata: Mapping[str, Any] = field(default_factory=dict)


def requirement_for_strength(strength: ClaimStrength) -> GateRequirement:
    if strength == ClaimStrength.ARCHITECTURE:
        return GateRequirement("architecture_guard", strength, required_zero=("smuggling",))
    if strength == ClaimStrength.ADMISSIBLE:
        return GateRequirement("admissible_guard", strength, required_zero=("ledger", "smuggling"))
    if strength == ClaimStrength.PHYSICAL:
        return GateRequirement("physical_guard", strength, required_zero=("preservation", "ledger", "smuggling"))
    if strength == ClaimStrength.OBSERVABLE:
        return GateRequirement("observable_guard", strength, required_zero=("preservation", "resolution", "ledger", "smuggling"))
    if strength == ClaimStrength.ROUTE_EXPORTED:
        return GateRequirement("route_export_guard", strength, required_zero=DEFECT_CHANNELS)
    raise ValueError(f"Unknown claim strength {strength}")


def active_required_defects(
    cert: ContinuationCertificate,
    req: GateRequirement,
) -> dict[str, float]:
    defects = cert.defects().as_dict()
    active = {}
    for ch in req.required_zero:
        if ch not in defects:
            raise KeyError(f"Unknown defect channel {ch!r}")
        tol = float(req.threshold.get(ch, 0.0))
        if defects[ch] > tol:
            active[ch] = defects[ch]
    return active


def evaluate_gate(
    cert: ContinuationCertificate,
    req: GateRequirement,
    *,
    persistent: bool = False,
    repair_available: bool = False,
    regime_boundary: bool = False,
    route_local: bool = False,
    metadata: Optional[Mapping[str, Any]] = None,
) -> GateEvaluation:
    active = active_required_defects(cert, req)

    if not active:
        verdict = GateVerdict.PASS_
    elif regime_boundary:
        verdict = GateVerdict.REGIME_BOUNDARY
    elif route_local and ("route" in active or req.claim_strength == ClaimStrength.ROUTE_EXPORTED):
        verdict = GateVerdict.ROUTE_OBSTRUCTION
    elif repair_available:
        verdict = GateVerdict.REPAIR_TARGET
    elif persistent and req.persistent_required:
        verdict = GateVerdict.FALSIFIER
    else:
        verdict = GateVerdict.OPEN

    return GateEvaluation(
        requirement=req,
        certificate=cert,
        verdict=verdict,
        active_defects=active,
        metadata=metadata or {},
    )


def evaluate_claim_strength(
    cert: ContinuationCertificate,
    strength: ClaimStrength,
    **kwargs: Any,
) -> GateEvaluation:
    return evaluate_gate(cert, requirement_for_strength(strength), **kwargs)


def is_falsified(ev: GateEvaluation) -> bool:
    return ev.verdict == GateVerdict.FALSIFIER


def is_open_gate(ev: GateEvaluation) -> bool:
    return ev.verdict in {GateVerdict.OPEN, GateVerdict.REPAIR_TARGET, GateVerdict.ROUTE_OBSTRUCTION, GateVerdict.REGIME_BOUNDARY}


def promotion_allowed(cert: ContinuationCertificate, target_strength: ClaimStrength) -> bool:
    """
    Promotion is allowed only if the target requirement passes.
    """
    return evaluate_claim_strength(cert, target_strength).verdict == GateVerdict.PASS_


def strongest_allowed_strength(cert: ContinuationCertificate) -> ClaimStrength:
    """
    Return strongest claim strength whose gate passes.
    """
    for strength in (
        ClaimStrength.ROUTE_EXPORTED,
        ClaimStrength.OBSERVABLE,
        ClaimStrength.PHYSICAL,
        ClaimStrength.ADMISSIBLE,
        ClaimStrength.ARCHITECTURE,
    ):
        if promotion_allowed(cert, strength):
            return strength
    return ClaimStrength.ARCHITECTURE


def persistent_defect_series(defect_values: Sequence[float], *, threshold: float = 0.0) -> bool:
    """
    Persistent defect: every observed value exceeds threshold.
    Empty sequences are not persistent.
    """
    if not defect_values:
        return False
    return all(v > threshold for v in defect_values)


def falsifier_from_series(
    cert: ContinuationCertificate,
    req: GateRequirement,
    defect_history: Mapping[str, Sequence[float]],
) -> GateEvaluation:
    """
    Escalate to falsifier when any required defect remains persistently nonzero.
    """
    persistent = False
    for ch in req.required_zero:
        if ch in defect_history:
            persistent = persistent or persistent_defect_series(
                defect_history[ch],
                threshold=float(req.threshold.get(ch, 0.0)),
            )
    return evaluate_gate(cert, req, persistent=persistent)


def prediction_gate(
    name: str,
    cert: ContinuationCertificate,
    *,
    claimed_strength: ClaimStrength,
    observed_defect_history: Optional[Mapping[str, Sequence[float]]] = None,
    repair_available: bool = False,
    route_local: bool = False,
) -> GateEvaluation:
    """
    Canonical prediction/falsifier gate.

    If observed defect history persists above threshold, a claimed required-zero
    channel becomes a falsifier.
    """
    req = requirement_for_strength(claimed_strength)
    req = GateRequirement(
        name=name,
        claim_strength=req.claim_strength,
        required_zero=req.required_zero,
        threshold=req.threshold,
        persistent_required=req.persistent_required,
        metadata=req.metadata,
    )
    if observed_defect_history is not None:
        return falsifier_from_series(cert, req, observed_defect_history)
    return evaluate_gate(cert, req, repair_available=repair_available, route_local=route_local)


def gate_logic_theorem_statement() -> str:
    return (
        "Defect Falsifier Gate Theorem: For any declared APF claim strength, "
        "the required zero-defect channels determine whether a certificate passes, "
        "remains open, becomes a repair target, identifies a regime boundary, "
        "or falsifies the claim when nonzero defect persists. This layer is "
        "architecture-level and does not promote route-local physical claims."
    )


def bank_marker() -> str:
    return MARKER
