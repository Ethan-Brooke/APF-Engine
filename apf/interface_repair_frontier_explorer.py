"""
APF Interface Repair Frontier Explorer.

v24.3.12+ delta layer.

Purpose
-------
The closure simulator applies all ordinary repair facts and asks whether the gate would
close.  This module explores the repair frontier:

    * Which subsets of repair patches are sufficient?
    * Which repair bundles are minimal?
    * Which repair fields are critical, appearing in every closing bundle?
    * Which routes are not frontier-searchable because they are provenance/structural blocked?

Boundary:
    This is still counterfactual. A closing frontier bundle says:
        "if these repair facts became true, the gate would close."
    It does not claim those facts have been physically/theoretically executed.

Top check:
    check_T_interface_repair_frontier_explorer_P
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List, Set
import itertools

try:
    from apf.interface_repair_closure_simulator import (
        PayloadPatch,
        SimulationStatus,
        simulate_repair_closure,
        propose_ordinary_repair_patch,
        apply_patches,
        canonical_payloads_for_simulation,
    )
    from apf.interface_movement_graph_repair_planner import (
        GraphRepairClass,
        discover_and_plan_repair,
    )
except Exception as exc:  # pragma: no cover
    raise ImportError(f"interface_repair_frontier_explorer requires closure simulator stack: {exc}") from exc


class FrontierStatus(str, Enum):
    ALREADY_CLOSED = "ALREADY_CLOSED"
    FRONTIER_FOUND = "FRONTIER_FOUND"
    NO_CLOSING_FRONTIER = "NO_CLOSING_FRONTIER"
    REFUSE_PROVENANCE_FRONTIER = "REFUSE_PROVENANCE_FRONTIER"
    REFUSE_SUBSTRATE_FRONTIER = "REFUSE_SUBSTRATE_FRONTIER"


@dataclass(frozen=True)
class RepairBundle:
    bundle_id: str
    fields: Tuple[str, ...]
    patch_count: int
    patches: Tuple[PayloadPatch, ...]
    patched_certificate: Mapping[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bundle_id": self.bundle_id,
            "fields": self.fields,
            "patch_count": self.patch_count,
            "patches": [asdict(p) for p in self.patches],
            "patched_certificate": dict(self.patched_certificate),
        }


@dataclass(frozen=True)
class RepairFrontier:
    route: str
    original_repair_class: GraphRepairClass
    frontier_status: FrontierStatus
    candidate_patch_count: int
    minimal_bundles: Tuple[RepairBundle, ...]
    critical_fields: Tuple[str, ...]
    optional_fields: Tuple[str, ...]
    blocked_reason: Optional[str]
    original_certificate: Mapping[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "route": self.route,
            "original_repair_class": self.original_repair_class.value,
            "frontier_status": self.frontier_status.value,
            "candidate_patch_count": self.candidate_patch_count,
            "minimal_bundles": [b.to_dict() for b in self.minimal_bundles],
            "critical_fields": self.critical_fields,
            "optional_fields": self.optional_fields,
            "blocked_reason": self.blocked_reason,
            "original_certificate": dict(self.original_certificate),
        }


def _certificate_for(route: str, payload: Mapping[str, Any]) -> Mapping[str, Any]:
    return discover_and_plan_repair(route, payload)["graph"]["certificate"]


def _repair_class_for(route: str, payload: Mapping[str, Any]) -> GraphRepairClass:
    return GraphRepairClass(discover_and_plan_repair(route, payload)["repair_plan"]["repair_class"])


def _closing(route: str, payload: Mapping[str, Any]) -> Tuple[bool, Mapping[str, Any]]:
    cert = _certificate_for(route, payload)
    return bool(cert.get("export_global_P")), cert


def _dedupe_patches(patches: Iterable[PayloadPatch]) -> Tuple[PayloadPatch, ...]:
    by_field: Dict[str, PayloadPatch] = {}
    for p in patches:
        by_field[p.field] = p
    return tuple(by_field[k] for k in sorted(by_field))


def explore_repair_frontier(route: str, payload: Mapping[str, Any], *, max_patch_count: int = 12) -> RepairFrontier:
    original_report = discover_and_plan_repair(route, payload)
    original_cert = original_report["graph"]["certificate"]
    original_class = GraphRepairClass(original_report["repair_plan"]["repair_class"])

    if original_class == GraphRepairClass.EXACT:
        return RepairFrontier(
            route=route,
            original_repair_class=original_class,
            frontier_status=FrontierStatus.ALREADY_CLOSED,
            candidate_patch_count=0,
            minimal_bundles=tuple(),
            critical_fields=tuple(),
            optional_fields=tuple(),
            blocked_reason=None,
            original_certificate=original_cert,
        )

    if original_class == GraphRepairClass.FAIL_CLOSED_PROVENANCE:
        return RepairFrontier(
            route=route,
            original_repair_class=original_class,
            frontier_status=FrontierStatus.REFUSE_PROVENANCE_FRONTIER,
            candidate_patch_count=0,
            minimal_bundles=tuple(),
            critical_fields=tuple(),
            optional_fields=tuple(),
            blocked_reason="Provenance smuggling cannot be explored by auto-patching; rebuild from clean provenance.",
            original_certificate=original_cert,
        )

    if original_class in {GraphRepairClass.SUBSTRATE_REVISION_REQUIRED, GraphRepairClass.MIXED_BLOCKED}:
        return RepairFrontier(
            route=route,
            original_repair_class=original_class,
            frontier_status=FrontierStatus.REFUSE_SUBSTRATE_FRONTIER,
            candidate_patch_count=0,
            minimal_bundles=tuple(),
            critical_fields=tuple(),
            optional_fields=tuple(),
            blocked_reason="Structural/substrate blockers cannot be explored by ordinary patch frontier.",
            original_certificate=original_cert,
        )

    patches = _dedupe_patches(propose_ordinary_repair_patch(route, payload))
    if len(patches) > max_patch_count:
        # Avoid exponential explosion; use all-patch closure as a bounded fallback.
        sim = simulate_repair_closure(route, payload)
        if sim.simulation_status == SimulationStatus.SIMULATED_CLOSURE_REACHES_P:
            bundle = RepairBundle(
                bundle_id="bounded_all_patches",
                fields=tuple(p.field for p in patches),
                patch_count=len(patches),
                patches=patches,
                patched_certificate=sim.patched_certificate or {},
            )
            return RepairFrontier(
                route=route,
                original_repair_class=original_class,
                frontier_status=FrontierStatus.FRONTIER_FOUND,
                candidate_patch_count=len(patches),
                minimal_bundles=(bundle,),
                critical_fields=bundle.fields,
                optional_fields=tuple(),
                blocked_reason="Frontier search bounded; all-patches closure bundle returned.",
                original_certificate=original_cert,
            )

    closing_bundles: List[RepairBundle] = []
    found_size: Optional[int] = None
    for r in range(1, len(patches) + 1):
        if found_size is not None and r > found_size:
            break
        for combo in itertools.combinations(patches, r):
            patched = apply_patches(payload, combo)
            ok, cert = _closing(route, patched)
            if ok:
                fields = tuple(sorted(p.field for p in combo))
                closing_bundles.append(
                    RepairBundle(
                        bundle_id=f"bundle_{len(closing_bundles):03d}",
                        fields=fields,
                        patch_count=len(combo),
                        patches=tuple(combo),
                        patched_certificate=cert,
                    )
                )
                found_size = r
        if found_size is not None:
            break

    if not closing_bundles:
        return RepairFrontier(
            route=route,
            original_repair_class=original_class,
            frontier_status=FrontierStatus.NO_CLOSING_FRONTIER,
            candidate_patch_count=len(patches),
            minimal_bundles=tuple(),
            critical_fields=tuple(),
            optional_fields=tuple(sorted(p.field for p in patches)),
            blocked_reason="No subset of candidate ordinary patches closed the gate.",
            original_certificate=original_cert,
        )

    field_sets = [set(b.fields) for b in closing_bundles]
    critical = tuple(sorted(set.intersection(*field_sets))) if field_sets else tuple()
    all_closing_fields = set.union(*field_sets) if field_sets else set()
    optional = tuple(sorted(all_closing_fields - set(critical)))

    return RepairFrontier(
        route=route,
        original_repair_class=original_class,
        frontier_status=FrontierStatus.FRONTIER_FOUND,
        candidate_patch_count=len(patches),
        minimal_bundles=tuple(closing_bundles),
        critical_fields=critical,
        optional_fields=optional,
        blocked_reason=None,
        original_certificate=original_cert,
    )


def canonical_frontiers() -> Dict[str, RepairFrontier]:
    return {
        name: explore_repair_frontier(route, payload)
        for name, (route, payload) in canonical_payloads_for_simulation().items()
    }


def check_T_frontier_finds_minimal_ordinary_bundles_P() -> Dict[str, Any]:
    frontiers = canonical_frontiers()
    ordinary = ["ew_open", "dark_open", "gauge_open", "horizon_open", "capacity_open"]
    tests = {
        f"{name}_frontier_found": frontiers[name].frontier_status == FrontierStatus.FRONTIER_FOUND
        and len(frontiers[name].minimal_bundles) >= 1
        for name in ordinary
    }
    tests["capacity_minimal_factor_field"] = frontiers["capacity_open"].minimal_bundles[0].fields == ("coarse_grain_factor",)
    tests["ew_minimal_nonempty"] = frontiers["ew_open"].minimal_bundles[0].patch_count >= 1
    return {
        "name": "check_T_frontier_finds_minimal_ordinary_bundles_P",
        "consistent": all(tests.values()),
        "status": "P_frontier" if all(tests.values()) else "FAIL",
        "summary": "Frontier explorer finds minimal closing bundles for ordinary repair cases.",
        "data": {
            "tests": tests,
            "bundle_counts": {name: len(frontiers[name].minimal_bundles) for name in ordinary},
            "critical_fields": {name: frontiers[name].critical_fields for name in ordinary},
        },
    }


def check_T_frontier_refuses_blocked_cases_P() -> Dict[str, Any]:
    frontiers = canonical_frontiers()
    tests = {
        "provenance_refused": frontiers["provenance_smuggled"].frontier_status == FrontierStatus.REFUSE_PROVENANCE_FRONTIER,
        "cstar_refused": frontiers["cstar"].frontier_status == FrontierStatus.REFUSE_SUBSTRATE_FRONTIER,
        "provenance_no_bundles": len(frontiers["provenance_smuggled"].minimal_bundles) == 0,
        "cstar_no_bundles": len(frontiers["cstar"].minimal_bundles) == 0,
    }
    return {
        "name": "check_T_frontier_refuses_blocked_cases_P",
        "consistent": all(tests.values()),
        "status": "P_frontier" if all(tests.values()) else "FAIL",
        "summary": "Frontier explorer refuses provenance and substrate/structural auto-frontiers.",
        "data": {"tests": tests},
        "dependencies": ["check_T_frontier_finds_minimal_ordinary_bundles_P"],
    }


def check_T_frontier_exact_cases_no_bundle_P() -> Dict[str, Any]:
    frontiers = canonical_frontiers()
    tests = {
        "ew_closed_already": frontiers["ew_closed"].frontier_status == FrontierStatus.ALREADY_CLOSED,
        "ew_closed_no_bundles": len(frontiers["ew_closed"].minimal_bundles) == 0,
        "ew_closed_original_global": frontiers["ew_closed"].original_certificate["export_global_P"] is True,
    }
    return {
        "name": "check_T_frontier_exact_cases_no_bundle_P",
        "consistent": all(tests.values()),
        "status": "P_frontier" if all(tests.values()) else "FAIL",
        "summary": "Already closed cases have no artificial repair frontier.",
        "data": {"tests": tests},
        "dependencies": ["check_T_frontier_refuses_blocked_cases_P"],
    }


def check_T_frontier_critical_fields_are_in_every_bundle_P() -> Dict[str, Any]:
    frontiers = canonical_frontiers()
    tests = {}
    for name, frontier in frontiers.items():
        if frontier.minimal_bundles:
            critical = set(frontier.critical_fields)
            tests[f"{name}_critical_in_all"] = all(critical.issubset(set(b.fields)) for b in frontier.minimal_bundles)
    tests["has_bundle_cases"] = len(tests) >= 5
    return {
        "name": "check_T_frontier_critical_fields_are_in_every_bundle_P",
        "consistent": all(tests.values()),
        "status": "P_frontier" if all(tests.values()) else "FAIL",
        "summary": "Critical fields are exactly fields common to every minimal closing bundle.",
        "data": {"tests": tests},
        "dependencies": ["check_T_frontier_exact_cases_no_bundle_P"],
    }


def check_T_interface_repair_frontier_explorer_P() -> Dict[str, Any]:
    subchecks = [
        check_T_frontier_finds_minimal_ordinary_bundles_P(),
        check_T_frontier_refuses_blocked_cases_P(),
        check_T_frontier_exact_cases_no_bundle_P(),
        check_T_frontier_critical_fields_are_in_every_bundle_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_interface_repair_frontier_explorer_P",
        "consistent": ok,
        "status": "P_frontier_explorer" if ok else "FAIL",
        "summary": "Interface Repair Frontier Explorer is P: it finds minimal ordinary repair bundles, critical fields, and refuses blocked/provenance frontiers.",
        "data": {
            "core_claim": "The explorer identifies minimal counterfactual repair bundles sufficient to close a route, without claiming execution.",
            "subchecks": [x["name"] for x in subchecks],
            "frontier_statuses": [x.value for x in FrontierStatus],
        },
        "dependencies": [x["name"] for x in subchecks],
    }


CHECKS = {
    "check_T_frontier_finds_minimal_ordinary_bundles_P": check_T_frontier_finds_minimal_ordinary_bundles_P,
    "check_T_frontier_refuses_blocked_cases_P": check_T_frontier_refuses_blocked_cases_P,
    "check_T_frontier_exact_cases_no_bundle_P": check_T_frontier_exact_cases_no_bundle_P,
    "check_T_frontier_critical_fields_are_in_every_bundle_P": check_T_frontier_critical_fields_are_in_every_bundle_P,
    "check_T_interface_repair_frontier_explorer_P": check_T_interface_repair_frontier_explorer_P,
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
            raise TypeError("Unsupported registry type for interface_repair_frontier_explorer.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
