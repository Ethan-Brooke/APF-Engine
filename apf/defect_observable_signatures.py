"""
APF Defect Observable Signatures v1

Status: [P_architecture]

This module extends the defect/gate calculus with observable-signature templates.

Core doctrine:
    Defect class transitions should leave typed signature families:
        - knees / sharp transitions
        - suppression envelopes
        - hysteresis / retention memory
        - boundary residuals
        - route-obstruction residuals
        - local-to-global mismatch patterns

This is architecture/math scaffolding only. It does not assert empirical
detection or promote physical export beyond route-local certificates.
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
    from apf.defect_transition_dynamics import TransitionKind
except Exception:  # pragma: no cover
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

try:
    from apf.defect_falsifier_gate_logic import ClaimStrength
except Exception:  # pragma: no cover
    class ClaimStrength(str, Enum):
        ARCHITECTURE = "architecture"
        ADMISSIBLE = "admissible"
        PHYSICAL = "physical"
        OBSERVABLE = "observable"
        ROUTE_EXPORTED = "route_exported"


STATUS = "[P_architecture]"
MARKER = "DEFECT_OBSERVABLE_SIGNATURES_PASS"


class SignatureKind(str, Enum):
    KNEE = "knee"
    SUPPRESSION = "suppression"
    HYSTERESIS = "hysteresis"
    BOUNDARY_RESIDUAL = "boundary_residual"
    ROUTE_RESIDUAL = "route_residual"
    LOCAL_GLOBAL_MISMATCH = "local_global_mismatch"
    SCALE_STATIONARITY = "scale_stationarity"
    NULL_SIGNATURE = "null_signature"


class DomainKind(str, Enum):
    MEASUREMENT = "measurement"
    COSMOLOGY_GROWTH = "cosmology_growth"
    RINGDOWN = "ringdown"
    HORIZON = "horizon"
    ROUTE_TRANSPORT = "route_transport"
    CONTEXTUALITY = "contextuality"
    SCALE_FLOW = "scale_flow"
    GENERAL = "general"


@dataclass(frozen=True)
class SignatureTemplate:
    name: str
    kind: SignatureKind
    domain: DomainKind
    required_defects: tuple[str, ...]
    claim_strength: ClaimStrength
    description: str
    falsifier_condition: str
    status: str = STATUS
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SignaturePrediction:
    template: SignatureTemplate
    active: bool
    score: float
    active_defects: Mapping[str, float]
    status: str = STATUS
    metadata: Mapping[str, Any] = field(default_factory=dict)


def defect_activity(defects: DefectVector, channels: Sequence[str], *, threshold: float = 0.0) -> dict[str, float]:
    table = defects.as_dict()
    out = {}
    for ch in channels:
        if ch not in table:
            raise KeyError(f"Unknown defect channel {ch!r}")
        if table[ch] > threshold:
            out[ch] = table[ch]
    return out


def signature_score(defects: DefectVector, channels: Sequence[str], *, threshold: float = 0.0) -> float:
    return sum(defect_activity(defects, channels, threshold=threshold).values())


def evaluate_signature(
    cert: ContinuationCertificate,
    template: SignatureTemplate,
    *,
    threshold: float = 0.0,
    metadata: Optional[Mapping[str, Any]] = None,
) -> SignaturePrediction:
    active = defect_activity(cert.defects(), template.required_defects, threshold=threshold)
    return SignaturePrediction(
        template=template,
        active=bool(active),
        score=sum(active.values()),
        active_defects=active,
        metadata=metadata or {},
    )


def template_catalog() -> tuple[SignatureTemplate, ...]:
    return (
        SignatureTemplate(
            name="preservation_knee",
            kind=SignatureKind.KNEE,
            domain=DomainKind.RINGDOWN,
            required_defects=("preservation", "ledger"),
            claim_strength=ClaimStrength.PHYSICAL,
            description="Sharp transition where preservation defect approaches zero or reappears.",
            falsifier_condition="Claimed preservation transition absent under certified boundary conditions.",
        ),
        SignatureTemplate(
            name="growth_suppression_envelope",
            kind=SignatureKind.SUPPRESSION,
            domain=DomainKind.COSMOLOGY_GROWTH,
            required_defects=("preservation", "ledger"),
            claim_strength=ClaimStrength.PHYSICAL,
            description="Suppression envelope driven by preservation/ledger defect near refinement load.",
            falsifier_condition="No suppression where persistent preservation/ledger defect is predicted.",
        ),
        SignatureTemplate(
            name="record_hysteresis",
            kind=SignatureKind.HYSTERESIS,
            domain=DomainKind.MEASUREMENT,
            required_defects=("resolution",),
            claim_strength=ClaimStrength.OBSERVABLE,
            description="History-dependent record formation caused by irreversible retention.",
            falsifier_condition="No retention asymmetry where resolution transition requires record locking.",
        ),
        SignatureTemplate(
            name="external_horizon_residual",
            kind=SignatureKind.BOUNDARY_RESIDUAL,
            domain=DomainKind.HORIZON,
            required_defects=("resolution",),
            claim_strength=ClaimStrength.OBSERVABLE,
            description="Observer-relative boundary residual from nonzero external resolution defect.",
            falsifier_condition="External resolution closes across claimed horizon boundary.",
        ),
        SignatureTemplate(
            name="route_transport_residual",
            kind=SignatureKind.ROUTE_RESIDUAL,
            domain=DomainKind.ROUTE_TRANSPORT,
            required_defects=("route", "ledger", "smuggling"),
            claim_strength=ClaimStrength.ROUTE_EXPORTED,
            description="Route-local residual from unclosed codomain/transport/evaluator gate.",
            falsifier_condition="Claimed exported route leaves persistent route/ledger/smuggling defect.",
        ),
        SignatureTemplate(
            name="contextuality_local_global_mismatch",
            kind=SignatureKind.LOCAL_GLOBAL_MISMATCH,
            domain=DomainKind.CONTEXTUALITY,
            required_defects=("preservation", "resolution"),
            claim_strength=ClaimStrength.PHYSICAL,
            description="Local zero-defect patches fail to glue globally.",
            falsifier_condition="Global section exists where APF predicts persistent gluing obstruction.",
        ),
        SignatureTemplate(
            name="scale_stationarity_signature",
            kind=SignatureKind.SCALE_STATIONARITY,
            domain=DomainKind.SCALE_FLOW,
            required_defects=("preservation", "route", "ledger"),
            claim_strength=ClaimStrength.OBSERVABLE,
            description="Preferred scale appears as stationary/minimal weighted defect.",
            falsifier_condition="No stable scale exists under certified route scale-flow assumptions.",
        ),
    )


def templates_for_domain(domain: DomainKind) -> tuple[SignatureTemplate, ...]:
    return tuple(t for t in template_catalog() if t.domain == domain)


def evaluate_catalog(
    cert: ContinuationCertificate,
    *,
    domain: DomainKind = DomainKind.GENERAL,
    threshold: float = 0.0,
) -> tuple[SignaturePrediction, ...]:
    templates = template_catalog() if domain == DomainKind.GENERAL else templates_for_domain(domain)
    return tuple(evaluate_signature(cert, t, threshold=threshold) for t in templates)


def active_predictions(
    cert: ContinuationCertificate,
    *,
    domain: DomainKind = DomainKind.GENERAL,
    threshold: float = 0.0,
) -> tuple[SignaturePrediction, ...]:
    return tuple(p for p in evaluate_catalog(cert, domain=domain, threshold=threshold) if p.active)


def null_prediction(
    name: str,
    domain: DomainKind,
    *,
    claim_strength: ClaimStrength = ClaimStrength.ARCHITECTURE,
) -> SignatureTemplate:
    return SignatureTemplate(
        name=name,
        kind=SignatureKind.NULL_SIGNATURE,
        domain=domain,
        required_defects=(),
        claim_strength=claim_strength,
        description="No defect signature predicted at architecture level.",
        falsifier_condition="Nonzero persistent defect appears where null signature was required.",
    )


def knee_indicator(values: Sequence[float], *, sharpness_threshold: float) -> bool:
    """
    Minimal discrete knee detector:
    second finite difference exceeds threshold in magnitude.
    """
    if len(values) < 3:
        return False
    if sharpness_threshold < 0:
        raise ValueError("sharpness_threshold must be nonnegative")
    for i in range(1, len(values) - 1):
        second = values[i + 1] - 2 * values[i] + values[i - 1]
        if abs(second) > sharpness_threshold:
            return True
    return False


def suppression_ratio(reference: float, observed: float) -> float:
    """
    reference-to-observed suppression ratio.
    1 means no suppression; below 1 means observed below reference.
    """
    if reference == 0:
        raise ValueError("reference must be nonzero")
    return observed / reference


def is_suppressed(reference: float, observed: float, *, tolerance: float = 0.0) -> bool:
    return suppression_ratio(reference, observed) < 1.0 - tolerance


def hysteresis_indicator(forward_values: Sequence[float], reverse_values: Sequence[float], *, tolerance: float = 0.0) -> bool:
    if len(forward_values) != len(reverse_values):
        raise ValueError("forward and reverse sequences must have same length")
    return any(abs(f - r) > tolerance for f, r in zip(forward_values, reverse_values))


def observable_signature_theorem_statement() -> str:
    return (
        "Defect Observable-Signature Theorem: Defect class transitions generate "
        "typed observable-signature families such as knees, suppression envelopes, "
        "hysteresis, boundary residuals, route residuals, and local-to-global "
        "mismatch patterns. These are search templates, not empirical detections. "
        "This layer is architecture-level and does not promote route-local claims."
    )


def bank_marker() -> str:
    return MARKER
