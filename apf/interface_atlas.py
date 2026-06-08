"""
APF Interface Atlas.

v24.3.12+ delta layer; v24.3.32 engine-axis-typing refactor (Session 3 of
architecture-review sequencing plan per
``APF Reference Docs/Reference - APF Interface Engine Family Architecture (2026-05-19).md``).

Purpose
-------
Aggregate many interface-intelligence reports into a strategic atlas:

    many route payloads / claim texts / codomain regimes
      -> movement graphs (route axis) / codomain verdicts (codomain axis)
      -> obstruction distribution
      -> repeated failed structures
      -> critical repair fields
      -> route coverage
      -> bottleneck ranking

This is the layer that turns single-route/single-regime diagnosis into APF-wide
engineering strategy.

Engine-axis typing (v24.3.32)
-----------------------------
The atlas now spans two engine axes in the APF Interface Engine family:

* ``AxisKind.ROUTE`` -- Route Adjudication Engine inputs (single transport paths;
  unit = route; failure taxonomy = EVALUATOR_MISSING / CODOMAIN_MISMATCH /
  CAPACITY_OVERSPEND / OVERLAP_INCOHERENCE / etc). Default axis for backward
  compatibility with v24.3.31-and-earlier callers.
* ``AxisKind.CODOMAIN`` -- Codomain Selection Engine inputs (regime competitions;
  unit = codomain regime; failure taxonomy = MARGIN_NONPOSITIVE / PHASE_LOCK_FAILED /
  COHERENCE_INSUFFICIENT / METASTABLE_HISTORY_LOCKED / OPEN_EVIDENCE_REQUIRED).

Aggregation
-----------
Per-axis aggregation is primary. The atlas also exposes flat cross-axis counts
for backward compat and a cross-axis "global bottleneck" view, but the latter is
flagged advisory (apples-and-oranges across engines per Reference doc Q2).

Boundary
--------
The atlas does not prove any route or adjudicate any regime. It summarizes
already-produced interface reports and identifies repeated blockers and shared
repair dependencies.

Top check:
    check_T_interface_atlas_P
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from enum import Enum
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List, Set
from collections import Counter, defaultdict
import json

try:
    from apf.claim_to_interface_graph_compiler import audit_claim, canonical_claims
    from apf.interface_structure_movement_graph import movement_graph_report
    from apf.interface_repair_frontier_explorer import explore_repair_frontier
    from apf.interface_repair_obligation_compiler import compile_obligation_packet
except Exception as exc:  # pragma: no cover
    raise ImportError(f"interface_atlas requires claim/interface stack: {exc}") from exc


class AxisKind(str, Enum):
    """Engine-axis enum for the IE family (v24.3.32+)."""
    ROUTE = "ROUTE"          # Route Adjudication Engine (existing IE)
    CODOMAIN = "CODOMAIN"    # Codomain Selection Engine (new at v24.3.31)


class AtlasInputKind(str, Enum):
    CLAIM = "CLAIM"
    ROUTE_PAYLOAD = "ROUTE_PAYLOAD"
    CODOMAIN_PAYLOAD = "CODOMAIN_PAYLOAD"  # v24.3.32 new kind for codomain-axis inputs


@dataclass(frozen=True)
class AtlasInput:
    input_id: str
    kind: AtlasInputKind
    route: Optional[str]
    claim_text: Optional[str]
    payload: Optional[Mapping[str, Any]]
    axis: AxisKind = AxisKind.ROUTE  # v24.3.32; defaults preserve backward compat

    def to_dict(self) -> Dict[str, Any]:
        return {
            "input_id": self.input_id,
            "kind": self.kind.value,
            "route": self.route,
            "claim_text": self.claim_text,
            "payload": dict(self.payload) if self.payload is not None else None,
            "axis": self.axis.value,
        }


@dataclass(frozen=True)
class AtlasRouteSummary:
    input_id: str
    route: str
    solver_status: str
    export_global_P: bool
    obstruction: Tuple[str, ...]
    failed_edges: Tuple[str, ...]
    failed_kinds: Tuple[str, ...]
    critical_fields: Tuple[str, ...]
    packet_status: str
    axis: AxisKind = AxisKind.ROUTE  # v24.3.32; defaults preserve backward compat

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # asdict() on an Enum field gives the Enum instance; serialize cleanly
        if hasattr(self.axis, "value"):
            d["axis"] = self.axis.value
        return d


@dataclass(frozen=True)
class InterfaceAtlas:
    atlas_name: str
    inputs: Tuple[AtlasInput, ...]
    route_summaries: Tuple[AtlasRouteSummary, ...]
    obstruction_counts: Mapping[str, int]
    failed_kind_counts: Mapping[str, int]
    critical_field_counts: Mapping[str, int]
    route_status_counts: Mapping[str, int]
    global_bottlenecks: Tuple[Tuple[str, int], ...]
    shared_repair_fields: Tuple[Tuple[str, int], ...]
    coverage: Mapping[str, Any]
    axis_summary: Mapping[str, Any] = field(default_factory=dict)  # v24.3.32 per-axis breakdown

    def to_dict(self) -> Dict[str, Any]:
        return {
            "atlas_name": self.atlas_name,
            "inputs": [x.to_dict() for x in self.inputs],
            "route_summaries": [x.to_dict() for x in self.route_summaries],
            "obstruction_counts": dict(self.obstruction_counts),
            "failed_kind_counts": dict(self.failed_kind_counts),
            "critical_field_counts": dict(self.critical_field_counts),
            "route_status_counts": dict(self.route_status_counts),
            "global_bottlenecks": list(self.global_bottlenecks),
            "shared_repair_fields": list(self.shared_repair_fields),
            "coverage": dict(self.coverage),
            "axis_summary": dict(self.axis_summary),
        }


def _cert_from_claim_report(report: Mapping[str, Any]) -> Mapping[str, Any]:
    return report["certification"]["ledger_certificate"]["certificate"]


def _compile_claim_input(inp: AtlasInput) -> Tuple[str, Mapping[str, Any], Mapping[str, Any], Mapping[str, Any]]:
    report = audit_claim(inp.claim_text or "")
    route = report.compilation.route.value
    report_dict = report.to_dict()
    graph = report_dict["movement_graph"]
    frontier = report_dict["frontier"]
    packet = report_dict["obligation_packet"]
    cert = _cert_from_claim_report(report_dict)
    return route, cert, graph, frontier | {"packet_status": packet["packet_status"]}


def _compile_payload_input(inp: AtlasInput) -> Tuple[str, Mapping[str, Any], Mapping[str, Any], Mapping[str, Any]]:
    if inp.route is None or inp.payload is None:
        raise ValueError("ROUTE_PAYLOAD atlas input requires route and payload")
    route = inp.route
    payload = inp.payload
    # v24.3.42 — Mass-sector engine closure: closure_kind fast-path.
    # Adapters that declare payload["closure_kind"] in {"obstruction_named",
    # "internal_identity"} short-circuit the standard ledger/movement-graph
    # pipeline. The new statuses OBSTRUCTION_NAMED_CLOSURE +
    # INTERNAL_IDENTITY_GLOBAL_P (added at v24.3.41 Fix B) are produced
    # directly with appropriate obstruction names + packet status.
    closure_kind = payload.get("closure_kind")
    if closure_kind in ("obstruction_named", "internal_identity"):
        return _compile_closure_kind_input(route, payload, closure_kind)
    graph = movement_graph_report(route, payload)
    frontier = explore_repair_frontier(route, payload).to_dict()
    packet = compile_obligation_packet(route, payload).to_dict()
    cert = graph["certificate"]
    return route, cert, graph, frontier | {"packet_status": packet["packet_status"]}


def _compile_closure_kind_input(route: str, payload: Mapping[str, Any], closure_kind: str) -> Tuple[str, Mapping[str, Any], Mapping[str, Any], Mapping[str, Any]]:
    """v24.3.42 — short-circuit closure-by-design payloads to the new statuses.

    For obstruction_named: produces OBSTRUCTION_NAMED_CLOSURE solver_status
    with NON_REPAIRABLE_BY_DESIGN repair class. The route is structurally closed;
    the codomain itself is rejected; not awaiting repair.

    For internal_identity: produces INTERNAL_IDENTITY_GLOBAL_P solver_status
    with EXACT repair class. Source IS the codomain by construction; global P
    by structural identity, not by evaluator transport.
    """
    name = str(payload.get("name", "closure_kind_input"))
    if closure_kind == "obstruction_named":
        obstruction_class = str(payload.get("obstruction_class", "OBSTRUCTION_NAMED_BY_DESIGN"))
        knockout_summary = str(payload.get("knockout_summary", "Codomain knockout — route closed by structural obstruction"))
        cert = {
            "name": name,
            "solver_status": "OBSTRUCTION_NAMED_CLOSURE",
            "promotion_status": "OBSTRUCTION_NAMED_CLOSURE",
            "repair_class": "NON_REPAIRABLE_BY_DESIGN",
            "obstruction": [obstruction_class],
            "export_global_P": False,
            "export_local_P": False,
            "safe_claim": knockout_summary,
            "next_action": "No action — codomain rejected by structural obstruction.",
            "route_notes": "closure-by-design obstruction route",
            "target_value_consumed": bool(payload.get("target_value_consumed", False)),
            "closure_kind": "obstruction_named",
        }
        packet_status = "OBSTRUCTION_NAMED_NO_OBLIGATIONS"
    else:  # internal_identity
        identity_summary = str(payload.get("identity_summary", "Source coincides with codomain by construction — internal identity"))
        cert = {
            "name": name,
            "solver_status": "INTERNAL_IDENTITY_GLOBAL_P",
            "promotion_status": "EXPORT_INTERNAL_IDENTITY_P",
            "repair_class": "EXACT",
            "obstruction": [],
            "export_global_P": True,
            "export_local_P": True,
            "safe_claim": identity_summary,
            "next_action": "Export as global P via structural identity (no evaluator transport required).",
            "route_notes": "internal-identity route",
            "target_value_consumed": False,
            "closure_kind": "internal_identity",
        }
        packet_status = "NOT_REQUIRED_ALREADY_P"
    graph = {
        "name": name,
        "certificate": cert,
        "edges": [],
        "missing_or_blocked_edges": [],
        "obstruction_witness_paths": {},
        "all_obstructions_have_paths": True,
        "all_edges_typed": True,
        "closure_kind": closure_kind,
    }
    frontier = {
        "critical_fields": list(cert["obstruction"]),
        "packet_status": packet_status,
    }
    return route, cert, graph, frontier


def _compile_codomain_input(
    inp: AtlasInput,
) -> Tuple[str, Mapping[str, Any], Mapping[str, Any], Mapping[str, Any]]:
    """v24.3.32: compile a Codomain Selection Engine input through the engine entry point.

    Reads ``inp.payload["regime"]`` + ``inp.payload["network_state"]`` and dispatches
    to ``adjudicate_codomain_competition``. Reshapes the verdict into the shared
    (route, cert, graph, frontier) tuple shape so the downstream
    summarize_input + build_interface_atlas machinery works uniformly.

    Codomain inputs do not have movement-graph edges; ``graph`` is populated with an
    empty ``missing_or_blocked_edges`` list. The verdict's ``critical_fields`` populate
    ``cert["obstruction"]`` and ``frontier["critical_fields"]``. The verdict status
    enum value goes into ``cert["solver_status"]`` and the obligation packet's
    ``current_status`` populates ``frontier["packet_status"]``.
    """
    if inp.payload is None:
        raise ValueError("CODOMAIN_PAYLOAD atlas input requires payload")
    # Late import to avoid circular dependency at module-load time
    from apf.codomain_selection_engine import (
        adjudicate_codomain_competition,
        CodomainSelectionStatus,
    )
    payload = dict(inp.payload)
    regime = payload.get("regime") or payload.get("adapter_regime") or "UNKNOWN"
    network_state = payload.get("network_state") or payload.get("source_network")
    verdict = adjudicate_codomain_competition(regime, network_state)
    verdict_dict = verdict.to_dict()
    route = inp.route or f"coherent_phase:{regime.lower()}"
    cert = {
        "solver_status": verdict_dict["status"],
        "export_global_P": (
            verdict_dict["status"] == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED.value
        ),
        "obstruction": list(verdict_dict["critical_fields"]),
    }
    graph = {
        "certificate": cert,
        "missing_or_blocked_edges": [],  # codomain selection has no transport edges
        "axis": "CODOMAIN",
        "engine": "codomain_selection",
        "regime": regime,
        "verdict": verdict_dict,
    }
    frontier = {
        "critical_fields": list(verdict_dict["critical_fields"]),
        "packet_status": verdict_dict["obligation_packet"].get("current_status", "UNKNOWN"),
    }
    return route, cert, graph, frontier


def summarize_input(inp: AtlasInput) -> AtlasRouteSummary:
    """v24.3.32: axis-aware dispatch.

    Codomain-axis inputs go through ``_compile_codomain_input``; route-axis inputs
    continue to use ``_compile_claim_input`` (CLAIM kind) or ``_compile_payload_input``
    (ROUTE_PAYLOAD kind), preserving v24.3.31-and-earlier behavior.
    """
    if inp.axis == AxisKind.CODOMAIN:
        route, cert, graph, frontier = _compile_codomain_input(inp)
    elif inp.kind == AtlasInputKind.CLAIM:
        route, cert, graph, frontier = _compile_claim_input(inp)
    else:
        route, cert, graph, frontier = _compile_payload_input(inp)

    failed_edges = tuple(edge["structure_name"] for edge in graph.get("missing_or_blocked_edges", []))
    failed_kinds = tuple(sorted({edge["kind"] for edge in graph.get("missing_or_blocked_edges", [])}))
    critical_fields = tuple(frontier.get("critical_fields", ()))
    packet_status = str(frontier.get("packet_status", "UNKNOWN"))

    return AtlasRouteSummary(
        input_id=inp.input_id,
        route=route,
        solver_status=str(cert.get("solver_status")),
        export_global_P=bool(cert.get("export_global_P")),
        obstruction=tuple(cert.get("obstruction", ())),
        failed_edges=failed_edges,
        failed_kinds=failed_kinds,
        critical_fields=critical_fields,
        packet_status=packet_status,
        axis=inp.axis,
    )


def _compute_axis_summary(
    summaries: Tuple[AtlasRouteSummary, ...],
) -> Dict[str, Any]:
    """v24.3.32: per-axis breakdown of obstructions / failed-kinds / critical-fields / status counts.

    Returns a dict keyed by axis value with per-axis counts. The primary surface for
    cross-engine reading per the Reference doc Q2 starting position (single atlas with
    engine-axis typing; per-axis aggregation primary; cross-axis flat counts secondary).
    """
    axis_keys = sorted({s.axis.value for s in summaries})
    summary: Dict[str, Any] = {}
    for axis in axis_keys:
        axis_summaries = [s for s in summaries if s.axis.value == axis]
        obstruction_counts: Counter = Counter()
        failed_kind_counts: Counter = Counter()
        critical_field_counts: Counter = Counter()
        status_counts: Counter = Counter()
        for s in axis_summaries:
            status_counts[s.solver_status] += 1
            obstruction_counts.update(s.obstruction)
            failed_kind_counts.update(s.failed_kinds)
            critical_field_counts.update(s.critical_fields)
        global_p = sum(1 for s in axis_summaries if s.export_global_P)
        summary[axis] = {
            "input_count": len(axis_summaries),
            "global_P_count": global_p,
            "non_global_count": len(axis_summaries) - global_p,
            "obstruction_counts": dict(obstruction_counts),
            "failed_kind_counts": dict(failed_kind_counts),
            "critical_field_counts": dict(critical_field_counts),
            "status_counts": dict(status_counts),
            "input_ids": [s.input_id for s in axis_summaries],
        }
    summary["_cross_axis_note"] = (
        "Per-axis counts above are primary. The top-level flat counts on "
        "InterfaceAtlas aggregate across axes and should be read as advisory only "
        "(per Reference - APF Interface Engine Family Architecture, Q2: apples-and-"
        "oranges risk when an EVALUATOR_MISSING route-axis obstruction is summed with "
        "a MARGIN_NONPOSITIVE codomain-axis failure)."
    )
    return summary


def build_interface_atlas(inputs: Iterable[AtlasInput], *, atlas_name: str = "APF_interface_atlas") -> InterfaceAtlas:
    inputs = tuple(inputs)
    summaries = tuple(summarize_input(inp) for inp in inputs)

    obstruction_counts = Counter()
    failed_kind_counts = Counter()
    critical_field_counts = Counter()
    status_counts = Counter()

    for summary in summaries:
        status_counts[summary.solver_status] += 1
        obstruction_counts.update(summary.obstruction)
        failed_kind_counts.update(summary.failed_kinds)
        critical_field_counts.update(summary.critical_fields)

    # Combine obstruction and failed-kind counts for a simple bottleneck ranking.
    bottleneck_counter = Counter()
    bottleneck_counter.update(obstruction_counts)
    for kind, count in failed_kind_counts.items():
        bottleneck_counter[f"KIND:{kind}"] += count
    global_bottlenecks = tuple(bottleneck_counter.most_common())

    shared_repair_fields = tuple((field, count) for field, count in critical_field_counts.most_common() if count >= 1)

    route_counts = Counter(summary.route for summary in summaries)
    coverage = {
        "input_count": len(inputs),
        "route_count": len(route_counts),
        "routes": dict(route_counts),
        "global_P_count": sum(1 for s in summaries if s.export_global_P),
        "non_global_count": sum(1 for s in summaries if not s.export_global_P),
        "obstructed_count": sum(1 for s in summaries if s.obstruction),
        "axis_counts": dict(Counter(s.axis.value for s in summaries)),
    }

    axis_summary = _compute_axis_summary(summaries)

    return InterfaceAtlas(
        atlas_name=atlas_name,
        inputs=inputs,
        route_summaries=summaries,
        obstruction_counts=dict(obstruction_counts),
        failed_kind_counts=dict(failed_kind_counts),
        critical_field_counts=dict(critical_field_counts),
        route_status_counts=dict(status_counts),
        global_bottlenecks=global_bottlenecks,
        shared_repair_fields=shared_repair_fields,
        coverage=coverage,
        axis_summary=axis_summary,
    )


def canonical_atlas_inputs() -> Tuple[AtlasInput, ...]:
    claim_inputs = tuple(
        AtlasInput(
            input_id=f"claim:{name}",
            kind=AtlasInputKind.CLAIM,
            route=None,
            claim_text=text,
            payload=None,
        )
        for name, text in canonical_claims().items()
    )

    route_inputs = (
        AtlasInput(
            input_id="payload:ew_transport_open",
            kind=AtlasInputKind.ROUTE_PAYLOAD,
            route="ew",
            claim_text=None,
            payload={
                "name": "atlas_EW_open",
                "trace_sector_closed": True,
                "source_to_scheme_registry_present": True,
                "evaluator_map_found": False,
                "codomain_transport_found": False,
                "counterterm_finite_parts_declared": False,
                "external_constants_ledger_clean": True,
                "uncertainty_protocol_declared": False,
                "target_value_consumed": False,
            },
        ),
        AtlasInput(
            input_id="payload:dark_runtime_open",
            kind=AtlasInputKind.ROUTE_PAYLOAD,
            route="dark",
            claim_text=None,
            payload={
                "name": "atlas_dark_runtime_open",
                "route_built": True,
                "run_completed": True,
                "chains_converged": False,
                "posterior_closed": False,
                "robustness_checks_passed": False,
                "data_ledger_clean": True,
                "evaluator_map_found": False,
                "codomain_transport_found": True,
                "target_value_consumed": False,
            },
        ),
        AtlasInput(
            input_id="payload:capacity_overspend",
            kind=AtlasInputKind.ROUTE_PAYLOAD,
            route="capacity",
            claim_text=None,
            payload={
                "name": "atlas_capacity_overspend",
                "raw_capacity_load": 100,
                "capacity_budget": 25,
                "coarse_grain_factor": 2,
            },
        ),
    )
    return claim_inputs + route_inputs


def build_canonical_atlas() -> InterfaceAtlas:
    return build_interface_atlas(canonical_atlas_inputs(), atlas_name="APF_canonical_interface_atlas")


def check_T_interface_atlas_construction_P() -> Dict[str, Any]:
    atlas = build_canonical_atlas()
    tests = {
        "has_inputs": atlas.coverage["input_count"] >= 10,
        "has_route_summaries": len(atlas.route_summaries) == atlas.coverage["input_count"],
        "covers_many_routes": atlas.coverage["route_count"] >= 7,
        "has_obstructions": atlas.coverage["obstructed_count"] >= 6,
    }
    return {
        "name": "check_T_interface_atlas_construction_P",
        "consistent": all(tests.values()),
        "status": "P_atlas" if all(tests.values()) else "FAIL",
        "summary": "Interface atlas constructs route summaries across canonical claims and payloads.",
        "data": {"tests": tests, "coverage": atlas.coverage},
    }


def check_T_interface_atlas_bottlenecks_P() -> Dict[str, Any]:
    atlas = build_canonical_atlas()
    obstructions = atlas.obstruction_counts
    failed_kinds = atlas.failed_kind_counts
    tests = {
        "evaluator_missing_present": obstructions.get("EVALUATOR_MISSING", 0) >= 1,
        "codomain_mismatch_present": obstructions.get("CODOMAIN_MISMATCH", 0) >= 1,
        "provenance_smuggle_present": obstructions.get("PROVENANCE_SMUGGLE", 0) >= 1,
        "failed_kinds_present": len(failed_kinds) >= 3,
        "bottlenecks_ranked": len(atlas.global_bottlenecks) >= 3,
    }
    return {
        "name": "check_T_interface_atlas_bottlenecks_P",
        "consistent": all(tests.values()),
        "status": "P_atlas" if all(tests.values()) else "FAIL",
        "summary": "Interface atlas ranks repeated obstructions and failed structure kinds.",
        "data": {"tests": tests, "obstruction_counts": obstructions, "failed_kind_counts": failed_kinds, "global_bottlenecks": atlas.global_bottlenecks[:10]},
        "dependencies": ["check_T_interface_atlas_construction_P"],
    }


def check_T_interface_atlas_shared_repairs_P() -> Dict[str, Any]:
    atlas = build_canonical_atlas()
    fields = dict(atlas.critical_field_counts)
    tests = {
        "has_critical_fields": len(fields) >= 3,
        "has_transport_or_evaluator_field": any(k in fields for k in ("codomain_transport_found", "evaluator_map_found", "codomain_map_declared", "posterior_closed")),
        "shared_repair_list_present": len(atlas.shared_repair_fields) >= 3,
    }
    return {
        "name": "check_T_interface_atlas_shared_repairs_P",
        "consistent": all(tests.values()),
        "status": "P_atlas" if all(tests.values()) else "FAIL",
        "summary": "Interface atlas identifies shared critical repair fields across route frontiers.",
        "data": {"tests": tests, "critical_field_counts": fields, "shared_repair_fields": atlas.shared_repair_fields[:20]},
        "dependencies": ["check_T_interface_atlas_bottlenecks_P"],
    }


def check_T_interface_atlas_strategy_report_P() -> Dict[str, Any]:
    atlas = build_canonical_atlas()
    atlas_dict = atlas.to_dict()
    tests = {
        "dict_has_coverage": "coverage" in atlas_dict,
        "dict_has_route_summaries": len(atlas_dict["route_summaries"]) == atlas.coverage["input_count"],
        "dict_has_bottlenecks": len(atlas_dict["global_bottlenecks"]) > 0,
        "dict_has_shared_repairs": len(atlas_dict["shared_repair_fields"]) > 0,
    }
    return {
        "name": "check_T_interface_atlas_strategy_report_P",
        "consistent": all(tests.values()),
        "status": "P_atlas" if all(tests.values()) else "FAIL",
        "summary": "Interface atlas emits a JSON strategy report suitable for integration dashboards.",
        "data": {"tests": tests, "atlas_preview": {"coverage": atlas_dict["coverage"], "top_bottlenecks": atlas_dict["global_bottlenecks"][:5]}},
        "dependencies": ["check_T_interface_atlas_shared_repairs_P"],
    }


def check_T_interface_atlas_axis_typing_P() -> Dict[str, Any]:
    """v24.3.32: verify engine-axis typing — atlas reads ROUTE + CODOMAIN axes uniformly.

    Constructs a mixed-axis input set (canonical route-axis inputs + a synthetic
    codomain-axis SC input) and verifies: per-axis summary exists; codomain axis
    summary present with correct verdict status; ROUTE axis summary present and
    non-empty; advisory cross-axis note present in axis_summary.
    """
    # Late import to avoid hard dep on codomain engine at module load
    try:
        from apf.codomain_selection_engine import CodomainSelectionStatus
    except ImportError as exc:
        return {
            "name": "check_T_interface_atlas_axis_typing_P",
            "consistent": False,
            "status": "FAIL",
            "summary": f"codomain_selection_engine import failed: {exc}",
            "data": {},
        }

    # Build a minimal codomain-axis input using the SC adapter's positive fixture
    sc_positive_payload = {
        "regime": "SUPERCONDUCTIVITY",
        "network_state": {
            "epsilon_phi": 0.2,
            "min_rho_coh": 0.5,
            "winding_sector_n": 1,
            "flux_sector_phi": 1.0,
            "nodes": [
                {"node_id": "a", "capacity_C": 10.0, "phase_phi": 0.00,
                 "coherence_sigma": 0.95, "defect_pressure_Pi": 0.05, "charge_q": 2.0},
                {"node_id": "b", "capacity_C": 10.0, "phase_phi": 0.04,
                 "coherence_sigma": 0.95, "defect_pressure_Pi": 0.05, "charge_q": 2.0},
                {"node_id": "c", "capacity_C": 10.0, "phase_phi": 0.08,
                 "coherence_sigma": 0.95, "defect_pressure_Pi": 0.05, "charge_q": 2.0},
                {"node_id": "d", "capacity_C": 10.0, "phase_phi": 0.03,
                 "coherence_sigma": 0.95, "defect_pressure_Pi": 0.05, "charge_q": 2.0},
            ],
            "edges": [["a", "b"], ["b", "c"], ["c", "d"], ["d", "a"]],
            "defects": {"thermal": 0.15, "gauge": 0.1, "disorder": 0.1,
                        "competition": 0.05, "boundary": 0.05, "vortex": 0.05},
            "costs": {"C_normal": 12.0, "C_superconducting": 5.0},
        },
    }
    sc_input = AtlasInput(
        input_id="codomain:superconductivity_positive",
        kind=AtlasInputKind.CODOMAIN_PAYLOAD,
        route="coherent_phase:superconductivity",
        claim_text=None,
        payload=sc_positive_payload,
        axis=AxisKind.CODOMAIN,
    )
    mixed_inputs = canonical_atlas_inputs() + (sc_input,)
    atlas = build_interface_atlas(mixed_inputs, atlas_name="APF_axis_typing_test_atlas")

    # Verify axis_summary structure
    summary = atlas.axis_summary
    route_summary = summary.get("ROUTE", {})
    codomain_summary = summary.get("CODOMAIN", {})
    cross_note = summary.get("_cross_axis_note", "")

    # Find the SC codomain row in route_summaries
    sc_row = next((s for s in atlas.route_summaries if s.input_id == "codomain:superconductivity_positive"), None)

    tests = {
        "axis_summary_present": "ROUTE" in summary and "CODOMAIN" in summary,
        "route_axis_nonempty": route_summary.get("input_count", 0) >= 10,
        "codomain_axis_present": codomain_summary.get("input_count", 0) == 1,
        "codomain_axis_global_P": codomain_summary.get("global_P_count", 0) == 1,
        "cross_axis_advisory_note": "apples-and-oranges" in cross_note,
        "sc_row_axis_codomain": sc_row is not None and sc_row.axis == AxisKind.CODOMAIN,
        "sc_row_solver_status_coherent": sc_row is not None and sc_row.solver_status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED.value,
        "sc_row_export_global_P": sc_row is not None and sc_row.export_global_P is True,
        "coverage_axis_counts_present": "axis_counts" in atlas.coverage,
        "coverage_axis_counts_codomain_one": atlas.coverage.get("axis_counts", {}).get("CODOMAIN") == 1,
    }
    consistent = all(tests.values())
    return {
        "name": "check_T_interface_atlas_axis_typing_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_atlas_axis_typing" if consistent else "FAIL",
        "epistemic": "P_atlas_axis_typing",
        "summary": (
            "Atlas engine-axis typing operational: mixed-axis input set produces per-axis "
            "summary with ROUTE + CODOMAIN axes; SC codomain row classified as "
            "COHERENT_CODOMAIN_SELECTED with export_global_P; cross-axis advisory note "
            "present (Reference doc Q2 starting position)."
        ),
        "dependencies": [
            "check_T_interface_atlas_construction_P",
            "apf.codomain_selection_engine",
        ],
        "data": {
            "tests": tests,
            "route_axis_input_count": route_summary.get("input_count"),
            "codomain_axis_input_count": codomain_summary.get("input_count"),
            "axis_counts": atlas.coverage.get("axis_counts"),
        },
    }


def check_T_interface_atlas_P() -> Dict[str, Any]:
    subchecks = [
        check_T_interface_atlas_construction_P(),
        check_T_interface_atlas_bottlenecks_P(),
        check_T_interface_atlas_shared_repairs_P(),
        check_T_interface_atlas_strategy_report_P(),
        check_T_interface_atlas_axis_typing_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_interface_atlas_P",
        "consistent": ok,
        "status": "P_interface_atlas" if ok else "FAIL",
        "summary": "Interface Atlas is P: many route/claim/codomain graphs aggregate into APF-wide bottleneck and repair-strategy reports across engine axes.",
        "data": {
            "core_claim": "The atlas turns single-route/single-regime interface audits into APF-wide obstruction, failed-structure, and repair-dependency maps across engine axes.",
            "subchecks": [x["name"] for x in subchecks],
        },
        "dependencies": [x["name"] for x in subchecks],
    }


CHECKS = {
    "check_T_interface_atlas_construction_P": check_T_interface_atlas_construction_P,
    "check_T_interface_atlas_bottlenecks_P": check_T_interface_atlas_bottlenecks_P,
    "check_T_interface_atlas_shared_repairs_P": check_T_interface_atlas_shared_repairs_P,
    "check_T_interface_atlas_strategy_report_P": check_T_interface_atlas_strategy_report_P,
    "check_T_interface_atlas_axis_typing_P": check_T_interface_atlas_axis_typing_P,
    "check_T_interface_atlas_P": check_T_interface_atlas_P,
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
            raise TypeError("Unsupported registry type for interface_atlas.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
