"""
APF Defect Global Descent Kernel v1

Status: [P_architecture]

This module extends obstruction cohomology into a global descent/kernel layer.

Core doctrine:
    Global APF physics is the zero-obstruction descent kernel over an
    interface cover. Local certificates define a global object exactly when
    overlap and cycle obstructions vanish and the resulting global certificate
    remains finite, preservation-stable, ledger-coherent, and resolvable.

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

try:
    from apf.defect_obstruction_cohomology import (
        InterfacePatch,
        ObstructionCertificate,
        can_glue_global,
        obstruction_norm,
        obstruction_vector_sum,
    )
except Exception:  # pragma: no cover
    @dataclass(frozen=True)
    class InterfacePatch:
        name: str
        certificate: ContinuationCertificate
        metadata: Mapping[str, Any] = field(default_factory=dict)

    @dataclass(frozen=True)
    class ObstructionCertificate:
        patches: tuple[InterfacePatch, ...]
        overlaps: tuple[Any, ...] = field(default_factory=tuple)
        cycles: tuple[Any, ...] = field(default_factory=tuple)
        kind: Any = None
        status: str = "[P_architecture]"
        metadata: Mapping[str, Any] = field(default_factory=dict)

    def can_glue_global(cert: ObstructionCertificate, *, tol: float = 0.0) -> bool:
        return not cert.overlaps and not cert.cycles

    def obstruction_norm(cert: ObstructionCertificate) -> float:
        return 0.0 if can_glue_global(cert) else 1.0

    def obstruction_vector_sum(cert: ObstructionCertificate) -> DefectVector:
        return DefectVector()


STATUS = "[P_architecture]"
MARKER = "DEFECT_GLOBAL_DESCENT_KERNEL_PASS"


class DescentStatus(str, Enum):
    NO_LOCAL_DATA = "no_local_data"
    LOCAL_ONLY = "local_only"
    OBSTRUCTED = "obstructed"
    GLOBAL_ADMISSIBLE = "global_admissible"
    GLOBAL_PHYSICAL = "global_physical"
    GLOBAL_OBSERVABLE = "global_observable"
    GLOBAL_EXPORTED_ROUTE = "global_exported_route"


@dataclass(frozen=True)
class GlobalDescentCertificate:
    """
    Certificate that local interface patches descend to a global APF object.

    `global_certificate` is constructed/declared only when gluing succeeds.
    """
    obstruction_certificate: ObstructionCertificate
    global_certificate: Optional[ContinuationCertificate]
    descent_status: DescentStatus
    obstruction_norm_value: float
    status: str = STATUS
    metadata: Mapping[str, Any] = field(default_factory=dict)


def _all_patch_field(patches: Sequence[InterfacePatch], field_name: str) -> bool:
    return all(bool(getattr(p.certificate, field_name)) for p in patches)


def _all_patch_routes_closed(patches: Sequence[InterfacePatch]) -> bool:
    return all(bool(p.certificate.route_closed) for p in patches)


def _merged_capacity_cost(patches: Sequence[InterfacePatch]) -> Optional[float]:
    costs = [p.certificate.capacity_cost for p in patches]
    if any(c is None for c in costs):
        return None
    return sum(float(c) for c in costs if c is not None)


def _merged_capacity_bound(patches: Sequence[InterfacePatch]) -> Optional[float]:
    bounds = [p.certificate.capacity_bound for p in patches]
    if any(b is None for b in bounds):
        return None
    return sum(float(b) for b in bounds if b is not None)


def build_global_certificate(
    oc: ObstructionCertificate,
    *,
    name: str = "global_descent_object",
    route: Optional[str] = None,
    tol: float = 0.0,
) -> Optional[ContinuationCertificate]:
    """
    Build global certificate if and only if local data glue globally.

    The global certificate inherits truth only when all patches satisfy that
    predicate and obstruction vanishes.
    """
    if not oc.patches:
        return None
    if not can_glue_global(oc, tol=tol):
        return None

    patches = oc.patches
    obstruction_channels = tuple(
        sorted({ch for p in patches for ch in p.certificate.obstruction_channels})
    )

    return ContinuationCertificate(
        name=name,
        finite_continuability=_all_patch_field(patches, "finite_continuability"),
        preservation_stability=_all_patch_field(patches, "preservation_stability"),
        ledger_coherence=_all_patch_field(patches, "ledger_coherence"),
        resolved_codomain=_all_patch_field(patches, "resolved_codomain"),
        route_closed=_all_patch_routes_closed(patches),
        route=route,
        capacity_cost=_merged_capacity_cost(patches),
        capacity_bound=_merged_capacity_bound(patches),
        obstruction_channels=obstruction_channels,
        metadata={
            "patches": tuple(p.name for p in patches),
            "descent": "zero_obstruction_global_glue",
        },
    )


def descent_status_from_global(
    oc: ObstructionCertificate,
    global_cert: Optional[ContinuationCertificate],
    *,
    tol: float = 0.0,
) -> DescentStatus:
    if not oc.patches:
        return DescentStatus.NO_LOCAL_DATA
    if global_cert is None:
        return DescentStatus.OBSTRUCTED if obstruction_norm(oc) > tol else DescentStatus.LOCAL_ONLY

    cls = classify(global_cert, tol=tol)
    if cls == APFClass.ADMISSIBLE:
        return DescentStatus.GLOBAL_ADMISSIBLE
    if cls == APFClass.PHYSICAL:
        return DescentStatus.GLOBAL_PHYSICAL
    if cls == APFClass.OBSERVABLE:
        return DescentStatus.GLOBAL_OBSERVABLE
    if cls == APFClass.EXPORTED:
        return DescentStatus.GLOBAL_EXPORTED_ROUTE
    return DescentStatus.LOCAL_ONLY


def certify_global_descent(
    oc: ObstructionCertificate,
    *,
    name: str = "global_descent_object",
    route: Optional[str] = None,
    tol: float = 0.0,
    metadata: Optional[Mapping[str, Any]] = None,
) -> GlobalDescentCertificate:
    global_cert = build_global_certificate(oc, name=name, route=route, tol=tol)
    return GlobalDescentCertificate(
        obstruction_certificate=oc,
        global_certificate=global_cert,
        descent_status=descent_status_from_global(oc, global_cert, tol=tol),
        obstruction_norm_value=obstruction_norm(oc),
        metadata=metadata or {},
    )


def in_global_kernel(cert: GlobalDescentCertificate, *, tol: float = 0.0) -> bool:
    """
    True iff global object exists and obstruction norm vanishes.
    """
    return cert.global_certificate is not None and cert.obstruction_norm_value <= tol


def global_physics_kernel(cert: GlobalDescentCertificate, *, tol: float = 0.0) -> bool:
    """
    Global physics kernel:
    zero obstruction plus at least physical global APF class.
    """
    if not in_global_kernel(cert, tol=tol):
        return False
    assert cert.global_certificate is not None
    cls = classify(cert.global_certificate, tol=tol)
    return cls in {APFClass.PHYSICAL, APFClass.OBSERVABLE, APFClass.EXPORTED}


def global_observable_kernel(cert: GlobalDescentCertificate, *, tol: float = 0.0) -> bool:
    if not in_global_kernel(cert, tol=tol):
        return False
    assert cert.global_certificate is not None
    return classify(cert.global_certificate, tol=tol) in {APFClass.OBSERVABLE, APFClass.EXPORTED}


def global_export_kernel(cert: GlobalDescentCertificate, *, tol: float = 0.0) -> bool:
    if not in_global_kernel(cert, tol=tol):
        return False
    assert cert.global_certificate is not None
    return classify(cert.global_certificate, tol=tol) == APFClass.EXPORTED


def representation_descent_exactness(
    cert: GlobalDescentCertificate,
    *,
    tol: float = 0.0,
) -> bool:
    """
    Exactness form:
        global physics = ker(obstruction)
    at architecture level, with physical global certificate.
    """
    return in_global_kernel(cert, tol=tol) == global_physics_kernel(cert, tol=tol)


def obstruction_image_nonzero(cert: GlobalDescentCertificate, *, tol: float = 0.0) -> bool:
    """
    im(obstruction) nonzero: local data exist but do not descend.
    """
    return bool(cert.obstruction_certificate.patches) and cert.obstruction_norm_value > tol


def quotient_by_obstruction(
    cert: GlobalDescentCertificate,
    *,
    tol: float = 0.0,
) -> str:
    """
    Architecture-level quotient label.
    """
    if in_global_kernel(cert, tol=tol):
        return "zero_obstruction_kernel"
    if obstruction_image_nonzero(cert, tol=tol):
        vec = obstruction_vector_sum(cert.obstruction_certificate)
        active = tuple(k for k, v in vec.as_dict().items() if v > tol)
        return "quotient_required:" + ",".join(active)
    return "no_global_data"


def descent_theorem_statement() -> str:
    return (
        "Global Descent Kernel Theorem: Local APF certificates define a global "
        "physical object exactly when their overlap and cycle obstruction defects "
        "vanish and the resulting global certificate is finite, preservation-stable, "
        "ledger-coherent, and resolvable at the appropriate class. In this sense "
        "global APF physics is the zero-obstruction descent kernel. This layer is "
        "architecture-level and does not promote route-local physical claims."
    )


def bank_marker() -> str:
    return MARKER
