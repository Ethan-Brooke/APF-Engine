"""
APF Defect Domain Applications v1

Status: [P_architecture]

This module provides guarded application templates for the integrated
defect-calculus stack.

Domains:
    - measurement / record formation
    - ringdown / stabilization
    - cosmology growth / perturbative suppression
    - horizon / external resolution boundary
    - contextuality / local-to-global mismatch
    - route transport / source-to-scheme export

Core doctrine:
    Domain applications instantiate the defect architecture. They do not
    promote any route-local physics claim or assert empirical detection.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Optional

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
    from apf.defect_observable_signatures import DomainKind, SignatureKind
except Exception:  # pragma: no cover
    class DomainKind(str, Enum):
        MEASUREMENT = "measurement"
        COSMOLOGY_GROWTH = "cosmology_growth"
        RINGDOWN = "ringdown"
        HORIZON = "horizon"
        ROUTE_TRANSPORT = "route_transport"
        CONTEXTUALITY = "contextuality"
        SCALE_FLOW = "scale_flow"
        GENERAL = "general"

    class SignatureKind(str, Enum):
        KNEE = "knee"
        SUPPRESSION = "suppression"
        HYSTERESIS = "hysteresis"
        BOUNDARY_RESIDUAL = "boundary_residual"
        ROUTE_RESIDUAL = "route_residual"
        LOCAL_GLOBAL_MISMATCH = "local_global_mismatch"
        SCALE_STATIONARITY = "scale_stationarity"
        NULL_SIGNATURE = "null_signature"


STATUS = "[P_architecture]"
MARKER = "DEFECT_DOMAIN_APPLICATIONS_PASS"


class DomainStatus(str, Enum):
    TEMPLATE_ONLY = "template_only"
    CANDIDATE_INSTANCE = "candidate_instance"
    OPEN_GATE = "open_gate"
    REPAIR_TARGET = "repair_target"
    ROUTE_LOCAL_ONLY = "route_local_only"
    EMPIRICAL_EXPORT_BLOCKED = "empirical_export_blocked"


@dataclass(frozen=True)
class DomainApplication:
    name: str
    domain: DomainKind
    required_defects: tuple[str, ...]
    predicted_signature: SignatureKind
    theorem_form: str
    status: DomainStatus = DomainStatus.TEMPLATE_ONLY
    guard: str = "architecture-only; no route-local promotion"
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DomainEvaluation:
    application: DomainApplication
    certificate: ContinuationCertificate
    active_defects: Mapping[str, float]
    applicable: bool
    status: str = STATUS
    metadata: Mapping[str, Any] = field(default_factory=dict)


def application_catalog() -> tuple[DomainApplication, ...]:
    return (
        DomainApplication(
            name="measurement_record_formation",
            domain=DomainKind.MEASUREMENT,
            required_defects=("resolution",),
            predicted_signature=SignatureKind.HYSTERESIS,
            theorem_form="P_Gamma -> O_Gamma as resolution-defect collapse with irreversible retention.",
        ),
        DomainApplication(
            name="ringdown_stabilization",
            domain=DomainKind.RINGDOWN,
            required_defects=("preservation", "ledger"),
            predicted_signature=SignatureKind.KNEE,
            theorem_form="A_Gamma/P_breakdown -> P_Gamma as preservation-defect relaxation.",
        ),
        DomainApplication(
            name="cosmology_growth_suppression",
            domain=DomainKind.COSMOLOGY_GROWTH,
            required_defects=("preservation", "ledger"),
            predicted_signature=SignatureKind.SUPPRESSION,
            theorem_form="Perturbative refinement load induces preservation/ledger defect and suppresses growth.",
        ),
        DomainApplication(
            name="horizon_external_resolution_boundary",
            domain=DomainKind.HORIZON,
            required_defects=("resolution",),
            predicted_signature=SignatureKind.BOUNDARY_RESIDUAL,
            theorem_form="Internal P_Gamma fails to glue to external O_Gamma due to persistent resolution defect.",
        ),
        DomainApplication(
            name="contextuality_local_global_mismatch",
            domain=DomainKind.CONTEXTUALITY,
            required_defects=("preservation", "resolution"),
            predicted_signature=SignatureKind.LOCAL_GLOBAL_MISMATCH,
            theorem_form="Local zero-defect patches fail global gluing through nonzero cycle defect.",
        ),
        DomainApplication(
            name="route_transport_export_gate",
            domain=DomainKind.ROUTE_TRANSPORT,
            required_defects=("route", "ledger", "smuggling"),
            predicted_signature=SignatureKind.ROUTE_RESIDUAL,
            theorem_form="O_Gamma -> E_Gamma,r only when route/export defect and hidden debt vanish.",
        ),
    )


def applications_for_domain(domain: DomainKind) -> tuple[DomainApplication, ...]:
    return tuple(app for app in application_catalog() if app.domain == domain)


def active_defects_for_application(cert: ContinuationCertificate, app: DomainApplication, *, threshold: float = 0.0) -> dict[str, float]:
    defects = cert.defects().as_dict()
    out = {}
    for ch in app.required_defects:
        if ch not in defects:
            raise KeyError(f"Unknown defect channel {ch!r}")
        if defects[ch] > threshold:
            out[ch] = defects[ch]
    return out


def evaluate_application(
    cert: ContinuationCertificate,
    app: DomainApplication,
    *,
    threshold: float = 0.0,
    metadata: Optional[Mapping[str, Any]] = None,
) -> DomainEvaluation:
    active = active_defects_for_application(cert, app, threshold=threshold)
    return DomainEvaluation(
        application=app,
        certificate=cert,
        active_defects=active,
        applicable=bool(active),
        metadata=metadata or {},
    )


def evaluate_domain(
    cert: ContinuationCertificate,
    domain: DomainKind,
    *,
    threshold: float = 0.0,
) -> tuple[DomainEvaluation, ...]:
    return tuple(evaluate_application(cert, app, threshold=threshold) for app in applications_for_domain(domain))


def active_domain_applications(
    cert: ContinuationCertificate,
    domain: DomainKind,
    *,
    threshold: float = 0.0,
) -> tuple[DomainEvaluation, ...]:
    return tuple(ev for ev in evaluate_domain(cert, domain, threshold=threshold) if ev.applicable)


def theorem_for_domain(domain: DomainKind) -> str:
    apps = applications_for_domain(domain)
    if not apps:
        return "No domain-specific theorem template registered."
    return " | ".join(app.theorem_form for app in apps)


def domain_status_guard(app: DomainApplication) -> bool:
    return app.status in {
        DomainStatus.TEMPLATE_ONLY,
        DomainStatus.CANDIDATE_INSTANCE,
        DomainStatus.OPEN_GATE,
        DomainStatus.REPAIR_TARGET,
        DomainStatus.ROUTE_LOCAL_ONLY,
        DomainStatus.EMPIRICAL_EXPORT_BLOCKED,
    } and "no route-local promotion" in app.guard


def measurement_application() -> DomainApplication:
    return applications_for_domain(DomainKind.MEASUREMENT)[0]


def ringdown_application() -> DomainApplication:
    return applications_for_domain(DomainKind.RINGDOWN)[0]


def cosmology_growth_application() -> DomainApplication:
    return applications_for_domain(DomainKind.COSMOLOGY_GROWTH)[0]


def horizon_application() -> DomainApplication:
    return applications_for_domain(DomainKind.HORIZON)[0]


def contextuality_application() -> DomainApplication:
    return applications_for_domain(DomainKind.CONTEXTUALITY)[0]


def route_transport_application() -> DomainApplication:
    return applications_for_domain(DomainKind.ROUTE_TRANSPORT)[0]


def domain_applications_theorem_statement() -> str:
    return (
        "Defect Domain-Applications Theorem: Measurement, ringdown, growth "
        "suppression, horizons, contextuality, and route transport are guarded "
        "domain instantiations of the same defect architecture. Each application "
        "identifies required defect channels and signature templates but remains "
        "architecture-level unless route-local and empirical gates close."
    )


def bank_marker() -> str:
    return MARKER
