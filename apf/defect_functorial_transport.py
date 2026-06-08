"""
APF Defect Functorial Transport v1

Status: [P_architecture]

This module extends the defect/global-descent calculus with guarded transport maps.

Core doctrine:
    APF transport is admissible only when it is defect-nonincreasing or
    defect-preserving in the relevant channels, respects typed codomains,
    and does not introduce hidden route/evaluator/smuggling debt.

This is architecture/math scaffolding only. It does not promote route-local
claims or assert physical export beyond existing certificates.
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
MARKER = "DEFECT_FUNCTORIAL_TRANSPORT_PASS"
DEFECT_CHANNELS = ("preservation", "resolution", "route", "ledger", "smuggling")


class TransportKind(str, Enum):
    IDENTITY = "identity"
    PRESERVATION = "preservation"
    RESOLUTION = "resolution"
    ROUTE = "route"
    SCALE = "scale"
    PATCH_GLUE = "patch_glue"
    QUOTIENT = "quotient"
    REPAIR = "repair"


@dataclass(frozen=True)
class TransportMap:
    """
    Typed APF transport map between certificates.

    allowed_increase:
        Per-channel tolerance for defect increase. Defaults to strict
        nonincrease in all architecture channels.
    codomain:
        Optional target codomain label.
    """
    name: str
    source_class: APFClass
    target_class: APFClass
    kind: TransportKind
    codomain: Optional[str] = None
    allowed_increase: Mapping[str, float] = field(default_factory=dict)
    requires_route_closed: bool = False
    requires_resolved_codomain: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TransportCertificate:
    transport: TransportMap
    source: ContinuationCertificate
    target: ContinuationCertificate
    source_class: APFClass
    target_class: APFClass
    defect_delta: Mapping[str, float]
    admissible: bool
    status: str = STATUS
    metadata: Mapping[str, Any] = field(default_factory=dict)


def defect_delta(source: ContinuationCertificate, target: ContinuationCertificate) -> dict[str, float]:
    """
    Delta(target)-Delta(source). Positive means transport introduced defect.
    """
    s = source.defects().as_dict()
    t = target.defects().as_dict()
    return {k: t[k] - s[k] for k in DEFECT_CHANNELS}


def transport_defect_nonincreasing(
    source: ContinuationCertificate,
    target: ContinuationCertificate,
    *,
    allowed_increase: Optional[Mapping[str, float]] = None,
) -> bool:
    allowed_increase = allowed_increase or {}
    dd = defect_delta(source, target)
    for channel, inc in dd.items():
        allowed = float(allowed_increase.get(channel, 0.0))
        if inc > allowed:
            return False
    return True


def typed_codomain_guard(tmap: TransportMap, target: ContinuationCertificate) -> bool:
    """
    If transport names a codomain, target must resolve codomain.
    """
    if tmap.codomain is None:
        return True
    return bool(target.resolved_codomain)


def route_guard(tmap: TransportMap, target: ContinuationCertificate) -> bool:
    if tmap.requires_route_closed and not target.route_closed:
        return False
    if tmap.requires_resolved_codomain and not target.resolved_codomain:
        return False
    return True


def smuggling_guard(source: ContinuationCertificate, target: ContinuationCertificate) -> bool:
    if "smuggling" in source.obstruction_channels:
        return False
    if "smuggling" in target.obstruction_channels:
        return False
    # Route closure without resolved codomain is a hidden promotion.
    if target.route_closed and not target.resolved_codomain:
        return False
    return True


def certify_transport(
    tmap: TransportMap,
    source: ContinuationCertificate,
    target: ContinuationCertificate,
    *,
    tol: float = 0.0,
    metadata: Optional[Mapping[str, Any]] = None,
) -> TransportCertificate:
    sc = classify(source, tol=tol)
    tc = classify(target, tol=tol)
    dd = defect_delta(source, target)

    class_ok = sc == tmap.source_class and tc == tmap.target_class
    defect_ok = transport_defect_nonincreasing(
        source,
        target,
        allowed_increase=tmap.allowed_increase,
    )
    codomain_ok = typed_codomain_guard(tmap, target)
    route_ok = route_guard(tmap, target)
    smuggle_ok = smuggling_guard(source, target)

    return TransportCertificate(
        transport=tmap,
        source=source,
        target=target,
        source_class=sc,
        target_class=tc,
        defect_delta=dd,
        admissible=class_ok and defect_ok and codomain_ok and route_ok and smuggle_ok,
        metadata=metadata or {},
    )


def identity_transport_for(cert: ContinuationCertificate, *, tol: float = 0.0) -> TransportMap:
    cls = classify(cert, tol=tol)
    return TransportMap(
        name=f"id_{cert.name}",
        source_class=cls,
        target_class=cls,
        kind=TransportKind.IDENTITY,
    )


def identity_transport_admissible(cert: ContinuationCertificate, *, tol: float = 0.0) -> bool:
    tmap = identity_transport_for(cert, tol=tol)
    return certify_transport(tmap, cert, cert, tol=tol).admissible


def compose_transport_maps(first: TransportMap, second: TransportMap, *, name: Optional[str] = None) -> TransportMap:
    """
    Compose transport maps if target/source classes match.

        first:  A -> B
        second: B -> C
        result: A -> C

    Allowed increases add channelwise.
    """
    if first.target_class != second.source_class:
        raise ValueError("Transport maps do not compose: class mismatch")

    allowed = {}
    for ch in DEFECT_CHANNELS:
        allowed[ch] = float(first.allowed_increase.get(ch, 0.0)) + float(second.allowed_increase.get(ch, 0.0))

    return TransportMap(
        name=name or f"{second.name}_after_{first.name}",
        source_class=first.source_class,
        target_class=second.target_class,
        kind=second.kind if first.kind == TransportKind.IDENTITY else first.kind,
        codomain=second.codomain or first.codomain,
        allowed_increase=allowed,
        requires_route_closed=first.requires_route_closed or second.requires_route_closed,
        requires_resolved_codomain=first.requires_resolved_codomain or second.requires_resolved_codomain,
        metadata={"composed_from": (first.name, second.name)},
    )


def functoriality_witness(
    first: TransportMap,
    second: TransportMap,
    x: ContinuationCertificate,
    y: ContinuationCertificate,
    z: ContinuationCertificate,
    *,
    tol: float = 0.0,
) -> bool:
    """
    Witness functorial compatibility:
        admissible(f) and admissible(g) imply admissible(g∘f)
    for the supplied certificates.
    """
    c1 = certify_transport(first, x, y, tol=tol)
    c2 = certify_transport(second, y, z, tol=tol)
    if not (c1.admissible and c2.admissible):
        return False
    composed = compose_transport_maps(first, second)
    c3 = certify_transport(composed, x, z, tol=tol)
    return c3.admissible


def trace_to_scheme_transport_template() -> TransportMap:
    """
    Architecture template for trace-to-scheme export.

    O_Gamma -> E_Gamma_r, route must close and codomain must be resolved.
    """
    return TransportMap(
        name="trace_to_scheme_transport_template",
        source_class=APFClass.OBSERVABLE,
        target_class=APFClass.EXPORTED,
        kind=TransportKind.ROUTE,
        codomain="scheme_codomain",
        requires_route_closed=True,
        requires_resolved_codomain=True,
    )


def source_to_resolution_transport_template() -> TransportMap:
    """
    Architecture template for source-to-record resolution.

    P_Gamma -> O_Gamma, resolution codomain must appear.
    """
    return TransportMap(
        name="source_to_resolution_transport_template",
        source_class=APFClass.PHYSICAL,
        target_class=APFClass.OBSERVABLE,
        kind=TransportKind.RESOLUTION,
        codomain="resolved_record",
        requires_resolved_codomain=True,
    )


def stabilization_transport_template() -> TransportMap:
    """
    Architecture template for A_Gamma -> P_Gamma stabilization.
    """
    return TransportMap(
        name="stabilization_transport_template",
        source_class=APFClass.ADMISSIBLE,
        target_class=APFClass.PHYSICAL,
        kind=TransportKind.PRESERVATION,
    )


def repair_transport_template(source_class: APFClass, target_class: APFClass) -> TransportMap:
    """
    Generic repair map: allows no defect increase and moves to target class.
    """
    return TransportMap(
        name=f"repair_{source_class.value}_to_{target_class.value}",
        source_class=source_class,
        target_class=target_class,
        kind=TransportKind.REPAIR,
    )


def transport_theorem_statement() -> str:
    return (
        "Defect Functorial Transport Theorem: APF transport maps are admissible "
        "only when they preserve typed classes, respect codomains, introduce no "
        "hidden smuggling debt, and are defect-nonincreasing up to explicit "
        "route-local tolerances. Composable admissible transports yield admissible "
        "composite transport. This layer is architecture-level and does not promote "
        "route-local physical claims."
    )


def bank_marker() -> str:
    return MARKER
