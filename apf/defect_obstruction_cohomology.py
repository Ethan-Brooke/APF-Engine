"""
APF Defect Obstruction Cohomology v1

Status: [P_architecture]

This module extends the defect calculus with a local-to-global obstruction layer.

Core doctrine:
    Local zero-defect certificates need not glue to a global zero-defect
    certificate. The obstruction to global gluing is represented by
    overlap defects and cycle defects on an interface cover.

This is architecture/math scaffolding only. It does not promote route-local
claims or assert a physical cohomology theory beyond existing certificates.
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
MARKER = "DEFECT_OBSTRUCTION_COHOMOLOGY_PASS"
DEFECT_CHANNELS = ("preservation", "resolution", "route", "ledger", "smuggling")


class ObstructionKind(str, Enum):
    NONE = "none"
    OVERLAP = "overlap"
    CYCLE = "cycle"
    GLOBAL_GLUE = "global_glue"
    CONTEXTUALITY = "contextuality"
    HORIZON = "horizon"
    ROUTE_INCOMPATIBILITY = "route_incompatibility"
    MIXED = "mixed"


@dataclass(frozen=True)
class InterfacePatch:
    """Local patch in an APF interface cover."""
    name: str
    certificate: ContinuationCertificate
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class OverlapDefect:
    """
    Defect on an overlap U_i cap U_j.

    The defect vector measures mismatch between locally valid certificates.
    """
    left: str
    right: str
    defects: DefectVector
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def is_zero(self, *, tol: float = 0.0) -> bool:
        return all(v <= tol for v in self.defects.as_dict().values())


@dataclass(frozen=True)
class CycleDefect:
    """
    Defect around a cycle of patches.

    Nonzero cycle defect witnesses local-to-global failure even if pairwise
    overlaps are locally acceptable.
    """
    cycle: tuple[str, ...]
    defects: DefectVector
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def is_zero(self, *, tol: float = 0.0) -> bool:
        return all(v <= tol for v in self.defects.as_dict().values())


@dataclass(frozen=True)
class ObstructionCertificate:
    patches: tuple[InterfacePatch, ...]
    overlaps: tuple[OverlapDefect, ...] = field(default_factory=tuple)
    cycles: tuple[CycleDefect, ...] = field(default_factory=tuple)
    kind: ObstructionKind = ObstructionKind.NONE
    status: str = STATUS
    metadata: Mapping[str, Any] = field(default_factory=dict)


def local_classes(cert: ObstructionCertificate, *, tol: float = 0.0) -> Mapping[str, APFClass]:
    return {p.name: classify(p.certificate, tol=tol) for p in cert.patches}


def all_local_at_least_physical(cert: ObstructionCertificate, *, tol: float = 0.0) -> bool:
    order = {
        APFClass.FORMAL: 0,
        APFClass.ADMISSIBLE: 1,
        APFClass.PHYSICAL: 2,
        APFClass.OBSERVABLE: 3,
        APFClass.EXPORTED: 4,
    }
    return all(order[classify(p.certificate, tol=tol)] >= order[APFClass.PHYSICAL] for p in cert.patches)


def overlap_obstruction(cert: ObstructionCertificate, *, tol: float = 0.0) -> bool:
    return any(not o.is_zero(tol=tol) for o in cert.overlaps)


def cycle_obstruction(cert: ObstructionCertificate, *, tol: float = 0.0) -> bool:
    return any(not c.is_zero(tol=tol) for c in cert.cycles)


def global_gluing_obstruction(cert: ObstructionCertificate, *, tol: float = 0.0) -> bool:
    """
    Global gluing obstruction exists if local patches are acceptable but
    overlap or cycle defects remain.
    """
    return all_local_at_least_physical(cert, tol=tol) and (
        overlap_obstruction(cert, tol=tol) or cycle_obstruction(cert, tol=tol)
    )


def infer_obstruction_kind(cert: ObstructionCertificate, *, tol: float = 0.0) -> ObstructionKind:
    has_overlap = overlap_obstruction(cert, tol=tol)
    has_cycle = cycle_obstruction(cert, tol=tol)

    if not has_overlap and not has_cycle:
        return ObstructionKind.NONE

    if has_overlap and has_cycle:
        return ObstructionKind.MIXED

    if has_cycle:
        # Resolution cycle defects are horizon-like/contextual depending channel.
        if any(c.defects.resolution > tol for c in cert.cycles):
            return ObstructionKind.CONTEXTUALITY
        return ObstructionKind.CYCLE

    if has_overlap:
        if any(o.defects.route > tol for o in cert.overlaps):
            return ObstructionKind.ROUTE_INCOMPATIBILITY
        if any(o.defects.resolution > tol for o in cert.overlaps):
            return ObstructionKind.HORIZON
        return ObstructionKind.OVERLAP

    return ObstructionKind.NONE


def obstruction_norm(cert: ObstructionCertificate) -> float:
    """Total L1 norm of all overlap and cycle defects."""
    total = 0.0
    for o in cert.overlaps:
        total += sum(o.defects.as_dict().values())
    for c in cert.cycles:
        total += sum(c.defects.as_dict().values())
    return total


def obstruction_vector_sum(cert: ObstructionCertificate) -> DefectVector:
    """Channelwise sum of obstruction defects."""
    sums = {k: 0.0 for k in DEFECT_CHANNELS}
    for o in cert.overlaps:
        for k, v in o.defects.as_dict().items():
            sums[k] += v
    for c in cert.cycles:
        for k, v in c.defects.as_dict().items():
            sums[k] += v
    return DefectVector(**sums)


def can_glue_global(cert: ObstructionCertificate, *, tol: float = 0.0) -> bool:
    """
    Global glue succeeds exactly when all overlap and cycle obstructions vanish.
    """
    return not overlap_obstruction(cert, tol=tol) and not cycle_obstruction(cert, tol=tol)


def contextuality_witness(cert: ObstructionCertificate, *, tol: float = 0.0) -> bool:
    """
    Contextuality as local zero-defect data with nonzero global/cycle defect.
    """
    return all_local_at_least_physical(cert, tol=tol) and cycle_obstruction(cert, tol=tol)


def horizon_witness(cert: ObstructionCertificate, *, tol: float = 0.0) -> bool:
    """
    Horizon-like witness: local internal physics exists but external overlap
    resolution defect blocks gluing to an external observer patch.
    """
    return all_local_at_least_physical(cert, tol=tol) and any(
        o.defects.resolution > tol for o in cert.overlaps
    )


def route_incompatibility_witness(cert: ObstructionCertificate, *, tol: float = 0.0) -> bool:
    """
    Route incompatibility: route/export defect appears on overlaps.
    """
    return any(o.defects.route > tol for o in cert.overlaps)


def repair_obstruction(
    cert: ObstructionCertificate,
    *,
    repair_fraction: float,
) -> ObstructionCertificate:
    """
    Toy repair map: scales all overlap/cycle defects by (1-repair_fraction).

    repair_fraction=1 closes all current obstruction defects.
    """
    if not (0.0 <= repair_fraction <= 1.0):
        raise ValueError("repair_fraction must be in [0, 1]")
    factor = 1.0 - repair_fraction

    def scale_defects(d: DefectVector) -> DefectVector:
        values = {k: v * factor for k, v in d.as_dict().items()}
        return DefectVector(**values)

    overlaps = tuple(
        OverlapDefect(o.left, o.right, scale_defects(o.defects), metadata=o.metadata)
        for o in cert.overlaps
    )
    cycles = tuple(
        CycleDefect(c.cycle, scale_defects(c.defects), metadata=c.metadata)
        for c in cert.cycles
    )
    repaired = ObstructionCertificate(
        patches=cert.patches,
        overlaps=overlaps,
        cycles=cycles,
        kind=cert.kind,
        metadata={**cert.metadata, "repair_fraction": repair_fraction},
    )
    return ObstructionCertificate(
        patches=repaired.patches,
        overlaps=repaired.overlaps,
        cycles=repaired.cycles,
        kind=infer_obstruction_kind(repaired),
        metadata=repaired.metadata,
    )


def obstruction_theorem_statement() -> str:
    return (
        "Defect Obstruction-Cohomology Theorem: Local zero-defect APF "
        "certificates need not glue globally. Overlap and cycle defects "
        "measure the obstruction to forming a global zero-defect certificate. "
        "Contextuality, horizon boundaries, and route incompatibility are "
        "typed instances of local-to-global defect obstruction. This layer "
        "is architecture-level and does not promote route-local physical claims."
    )


def bank_marker() -> str:
    return MARKER
