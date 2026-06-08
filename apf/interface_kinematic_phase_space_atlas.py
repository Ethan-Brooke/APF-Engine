"""
APF Interface Kinematic Phase-Space Atlas.

Purpose
-------
Map interface route payloads into kinematic phase space:

    route payloads
      -> kinematic coordinates
      -> distance-to-export
      -> repair-depth geometry
      -> bottleneck state histogram
      -> cross-route phase atlas

Boundary
--------
The phase-space atlas is descriptive and planning-oriented. It does not fabricate evidence,
solve physics routes, or promote held claims.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List
import json
import math
import datetime

from apf.interface_kinematics_engine import (
    KinematicState,
    TransitionStatus,
    compute_kinematic_certificate,
    route_path,
)
from apf.interface_kinematic_solver import (
    solve_kinematic_path,
    SolverStatus,
)


class PhaseRegion(str, Enum):
    ORIGIN = "ORIGIN"
    LOCAL = "LOCAL"
    TYPED = "TYPED"
    TRANSPORT = "TRANSPORT"
    EVALUATOR = "EVALUATOR"
    LEDGERED = "LEDGERED"
    EXPORT = "EXPORT"
    HARD_STOP = "HARD_STOP"


@dataclass(frozen=True)
class PhasePoint:
    item_id: str
    route: str
    current_state: KinematicState
    phase_region: PhaseRegion
    progress_fraction: float
    distance_to_export: int
    repair_depth: int
    first_blocked_move: Optional[str]
    first_required_field: Optional[str]
    exportable: bool
    hard_stop: bool
    solver_status: SolverStatus
    source: str = "manual"

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["current_state"] = self.current_state.value
        d["phase_region"] = self.phase_region.value
        d["solver_status"] = self.solver_status.value
        return d


@dataclass(frozen=True)
class PhaseSpaceAtlas:
    created_utc: str
    points: Tuple[PhasePoint, ...]
    route_counts: Mapping[str, int]
    region_counts: Mapping[str, int]
    solver_status_counts: Mapping[str, int]
    bottleneck_fields: Mapping[str, int]
    bottleneck_states: Mapping[str, int]
    mean_progress_fraction: float
    max_repair_depth: int
    nearest_exportable: Optional[str]
    farthest_from_export: Optional[str]
    summary: str
    boundary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "created_utc": self.created_utc,
            "points": [p.to_dict() for p in self.points],
            "route_counts": dict(self.route_counts),
            "region_counts": dict(self.region_counts),
            "solver_status_counts": dict(self.solver_status_counts),
            "bottleneck_fields": dict(self.bottleneck_fields),
            "bottleneck_states": dict(self.bottleneck_states),
            "mean_progress_fraction": self.mean_progress_fraction,
            "max_repair_depth": self.max_repair_depth,
            "nearest_exportable": self.nearest_exportable,
            "farthest_from_export": self.farthest_from_export,
            "summary": self.summary,
            "boundary": self.boundary,
        }


def phase_region_for_state(state: KinematicState) -> PhaseRegion:
    if state in {KinematicState.FAIL_CLOSED_PROVENANCE, KinematicState.STRUCTURAL_BLOCK}:
        return PhaseRegion.HARD_STOP
    if state == KinematicState.UNSEEN:
        return PhaseRegion.ORIGIN
    if state in {KinematicState.LOCAL_OBJECT_PRESENT, KinematicState.LOCAL_CLOSURE, KinematicState.RUN_COMPLETED, KinematicState.CHAINS_CONVERGED, KinematicState.POSTERIOR_CLOSED, KinematicState.ROBUSTNESS_PASSED}:
        return PhaseRegion.LOCAL
    if state in {KinematicState.SOURCE_TYPED, KinematicState.CODOMAIN_TYPED, KinematicState.GROUP_LAW_VERIFIED, KinematicState.REPRESENTATION_FAITHFUL, KinematicState.AREA_COST_DEFINED}:
        return PhaseRegion.TYPED
    if state in {KinematicState.TRANSPORT_DEFINED, KinematicState.OVERLAP_GLUED, KinematicState.CAPACITY_BOUND_CHECKED, KinematicState.CAPACITY_BUDGET_VERIFIED, KinematicState.COARSE_GRAINED_ADMISSIBLE}:
        return PhaseRegion.TRANSPORT
    if state == KinematicState.EVALUATOR_DEFINED:
        return PhaseRegion.EVALUATOR
    if state in {KinematicState.COUNTERTERM_NORMALIZED, KinematicState.UNCERTAINTY_LEDGERED, KinematicState.ENTROPY_LEDGER_CLEAN, KinematicState.ANOMALY_CLEAN}:
        return PhaseRegion.LEDGERED
    if state == KinematicState.GLOBAL_EXPORTABLE:
        return PhaseRegion.EXPORT
    return PhaseRegion.LOCAL


def _allowed_count(cert) -> int:
    return sum(1 for tr in cert.path if tr.status == TransitionStatus.ALLOWED)


def _path_len(route: str) -> int:
    return len(route_path(route if route in {"ew", "dark", "gauge", "horizon", "capacity", "generic"} else "generic"))


def phase_point(item_id: str, route: str, payload: Mapping[str, Any], *, source: str = "manual") -> PhasePoint:
    cert = compute_kinematic_certificate(route, payload)
    solve = solve_kinematic_path(route, payload)
    hard_stop = cert.fail_closed or cert.structural_block or solve.status in {SolverStatus.FAIL_CLOSED_PROVENANCE, SolverStatus.STRUCTURAL_BLOCK}
    total = max(_path_len(route), 1)
    allowed = _allowed_count(cert)
    if cert.exportable:
        progress = 1.0
        distance = 0
    elif hard_stop:
        progress = 0.0
        distance = -1
    else:
        progress = max(0.0, min(1.0, allowed / total))
        distance = max(total - allowed, 0)
    first_field = solve.first_next_field
    return PhasePoint(
        item_id=item_id,
        route=route,
        current_state=cert.current_state,
        phase_region=phase_region_for_state(cert.current_state),
        progress_fraction=round(progress, 6),
        distance_to_export=distance,
        repair_depth=solve.estimated_repair_depth,
        first_blocked_move=cert.first_blocked_move,
        first_required_field=first_field,
        exportable=cert.exportable,
        hard_stop=hard_stop,
        solver_status=solve.status,
        source=source,
    )


def build_phase_space_atlas(items: Iterable[Mapping[str, Any]]) -> PhaseSpaceAtlas:
    points: List[PhasePoint] = []
    for idx, row in enumerate(items):
        item_id = str(row.get("item_id", f"item_{idx:03d}"))
        route = str(row.get("route", "generic"))
        payload = row.get("payload", {})
        source = str(row.get("source", "manual"))
        points.append(phase_point(item_id, route, payload, source=source))

    route_counts: Dict[str, int] = {}
    region_counts: Dict[str, int] = {}
    status_counts: Dict[str, int] = {}
    fields: Dict[str, int] = {}
    states: Dict[str, int] = {}
    for p in points:
        route_counts[p.route] = route_counts.get(p.route, 0) + 1
        region_counts[p.phase_region.value] = region_counts.get(p.phase_region.value, 0) + 1
        status_counts[p.solver_status.value] = status_counts.get(p.solver_status.value, 0) + 1
        if p.first_required_field:
            fields[p.first_required_field] = fields.get(p.first_required_field, 0) + 1
        states[p.current_state.value] = states.get(p.current_state.value, 0) + 1

    mean_progress = round(sum(p.progress_fraction for p in points) / len(points), 6) if points else 0.0
    max_depth = max((p.repair_depth for p in points if p.repair_depth >= 0), default=0)

    repairable = [p for p in points if not p.hard_stop and not p.exportable and p.distance_to_export >= 0]
    nearest = min(repairable, key=lambda p: (p.distance_to_export, p.repair_depth, p.item_id)).item_id if repairable else None
    farthest_pool = [p for p in points if p.distance_to_export >= 0]
    farthest = max(farthest_pool, key=lambda p: (p.distance_to_export, p.repair_depth, p.item_id)).item_id if farthest_pool else None

    summary = f"{len(points)} point(s); mean_progress={mean_progress}; max_repair_depth={max_depth}; regions={dict(region_counts)}"
    boundary = "Phase-space atlas is descriptive/planning-only; it does not fabricate evidence or promote held claims."
    return PhaseSpaceAtlas(
        created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        points=tuple(points),
        route_counts=route_counts,
        region_counts=region_counts,
        solver_status_counts=status_counts,
        bottleneck_fields=fields,
        bottleneck_states=states,
        mean_progress_fraction=mean_progress,
        max_repair_depth=max_depth,
        nearest_exportable=nearest,
        farthest_from_export=farthest,
        summary=summary,
        boundary=boundary,
    )


def load_phase_items(path: str) -> Tuple[Mapping[str, Any], ...]:
    data = json.loads(open(path, "r", encoding="utf-8").read())
    if isinstance(data, dict) and "items" in data:
        return tuple(data["items"])
    if isinstance(data, dict) and "candidates" in data:
        return tuple({
            "item_id": c.get("item_id", f"candidate_{idx:03d}"),
            "route": c.get("route", "generic"),
            "payload": c.get("payload", {}),
            "source": c.get("artifact_path", "candidate"),
        } for idx, c in enumerate(data["candidates"]))
    if isinstance(data, list):
        return tuple(data)
    raise ValueError("Expected JSON object with items/candidates or a list of items.")


def render_phase_atlas_markdown(atlas: PhaseSpaceAtlas) -> str:
    lines = [
        "# APF Interface Kinematic Phase-Space Atlas",
        "",
        f"- Points: `{len(atlas.points)}`",
        f"- Mean progress: `{atlas.mean_progress_fraction}`",
        f"- Max repair depth: `{atlas.max_repair_depth}`",
        f"- Nearest repairable export: `{atlas.nearest_exportable}`",
        f"- Farthest from export: `{atlas.farthest_from_export}`",
        "",
        "## Region counts",
        "",
    ]
    for k, v in sorted(atlas.region_counts.items()):
        lines.append(f"- `{k}`: {v}")
    lines += ["", "## Bottleneck fields", ""]
    if atlas.bottleneck_fields:
        for k, v in sorted(atlas.bottleneck_fields.items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"- `{k}`: {v}")
    else:
        lines.append("- none")
    lines += [
        "",
        "## Points",
        "",
        "| Item | Route | State | Region | Progress | Distance | Repair depth | First field | Status |",
        "|---|---|---|---|---:|---:|---:|---|---|",
    ]
    for p in atlas.points:
        lines.append(f"| `{p.item_id}` | `{p.route}` | `{p.current_state.value}` | `{p.phase_region.value}` | {p.progress_fraction} | {p.distance_to_export} | {p.repair_depth} | `{p.first_required_field or '—'}` | `{p.solver_status.value}` |")
    lines += ["", "## Boundary", "", atlas.boundary]
    return "\n".join(lines) + "\n"


def check_T_phase_space_points_P() -> Dict[str, Any]:
    ew = {
        "trace_sector_closed": True,
        "source_to_scheme_registry_present": True,
        "codomain_transport_found": False,
        "evaluator_map_found": False,
        "counterterm_finite_parts_declared": False,
        "external_constants_ledger_clean": True,
        "uncertainty_protocol_declared": False,
        "target_value_consumed": False,
    }
    p = phase_point("ew_open", "ew", ew)
    tests = {
        "route": p.route == "ew",
        "typed_region": p.phase_region == PhaseRegion.TYPED,
        "first_field_codomain": p.first_required_field == "codomain_transport_found",
        "not_exportable": p.exportable is False,
    }
    return {"name": "check_T_phase_space_points_P", "consistent": all(tests.values()), "status": "P_phase_space_atlas" if all(tests.values()) else "FAIL", "summary": "Phase point maps EW open payload into typed region with codomain bottleneck.", "data": {"tests": tests, "point": p.to_dict()}}


def check_T_phase_space_atlas_counts_P() -> Dict[str, Any]:
    items = [
        {"item_id": "ew_open", "route": "ew", "payload": {"trace_sector_closed": True, "source_to_scheme_registry_present": True, "codomain_transport_found": False, "evaluator_map_found": False, "counterterm_finite_parts_declared": False, "external_constants_ledger_clean": True, "uncertainty_protocol_declared": False, "target_value_consumed": False}},
        {"item_id": "dark_closed", "route": "dark", "payload": {"route_built": True, "run_completed": True, "chains_converged": True, "posterior_closed": True, "robustness_checks_passed": True, "codomain_transport_found": True, "evaluator_map_found": True, "data_ledger_clean": True, "target_value_consumed": False}},
        {"item_id": "bad", "route": "ew", "payload": {"target_value_consumed": True}},
    ]
    atlas = build_phase_space_atlas(items)
    tests = {
        "three_points": len(atlas.points) == 3,
        "has_hard_stop": atlas.region_counts.get("HARD_STOP", 0) == 1,
        "has_export": atlas.region_counts.get("EXPORT", 0) == 1,
        "codomain_bottleneck": atlas.bottleneck_fields.get("codomain_transport_found", 0) == 1,
        "mean_progress_bounded": 0 <= atlas.mean_progress_fraction <= 1,
    }
    return {"name": "check_T_phase_space_atlas_counts_P", "consistent": all(tests.values()), "status": "P_phase_space_atlas" if all(tests.values()) else "FAIL", "summary": "Phase-space atlas aggregates route/region/status/bottleneck counts.", "data": {"tests": tests, "atlas": atlas.to_dict()}, "dependencies": ["check_T_phase_space_points_P"]}


def check_T_phase_space_markdown_P() -> Dict[str, Any]:
    items = [
        {"item_id": "ew_open", "route": "ew", "payload": {"trace_sector_closed": True, "source_to_scheme_registry_present": True, "codomain_transport_found": False}},
    ]
    atlas = build_phase_space_atlas(items)
    md = render_phase_atlas_markdown(atlas)
    tests = {
        "has_title": "# APF Interface Kinematic Phase-Space Atlas" in md,
        "has_points_table": "| Item | Route | State |" in md,
        "has_boundary": "does not fabricate evidence" in md,
        "has_bottleneck": "codomain_transport_found" in md,
    }
    return {"name": "check_T_phase_space_markdown_P", "consistent": all(tests.values()), "status": "P_phase_space_atlas" if all(tests.values()) else "FAIL", "summary": "Phase-space atlas renders reviewer/integrator markdown.", "data": {"tests": tests}, "dependencies": ["check_T_phase_space_atlas_counts_P"]}


def check_T_interface_kinematic_phase_space_atlas_P() -> Dict[str, Any]:
    subchecks = [
        check_T_phase_space_points_P(),
        check_T_phase_space_atlas_counts_P(),
        check_T_phase_space_markdown_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {"name": "check_T_interface_kinematic_phase_space_atlas_P", "consistent": ok, "status": "P_phase_space_atlas" if ok else "FAIL", "summary": "Interface Kinematic Phase-Space Atlas is P: route payloads map into state-space coordinates, bottlenecks, repair distances, and markdown summaries.", "data": {"core_claim": "The atlas makes kinematic state-space visible without fabricating evidence or promoting held claims.", "subchecks": [x["name"] for x in subchecks]}, "dependencies": [x["name"] for x in subchecks]}


CHECKS = {
    "check_T_phase_space_points_P": check_T_phase_space_points_P,
    "check_T_phase_space_atlas_counts_P": check_T_phase_space_atlas_counts_P,
    "check_T_phase_space_markdown_P": check_T_phase_space_markdown_P,
    "check_T_interface_kinematic_phase_space_atlas_P": check_T_interface_kinematic_phase_space_atlas_P,
}


def register(registry=None):
    if registry is None:
        return CHECKS
    if hasattr(registry, "update"):
        registry.update(CHECKS)
        return registry
    for name, fn in CHECKS.items():
        if hasattr(registry, "register"):
            registry.register(name, fn)
        elif hasattr(registry, "add"):
            registry.add(name, fn)
        else:
            raise TypeError("Unsupported registry type for interface_kinematic_phase_space_atlas.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
