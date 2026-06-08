"""
APF Interface Structure Movement Graph.

v24.3.12+ delta layer.

Purpose
-------
The discovery engine can infer a typed transport ledger from raw route payloads.
This module converts that ledger into an explicit source->target movement graph.

Pipeline:
    raw route payload
      -> discovered typed ledger
      -> movement graph
      -> obstruction witness paths
      -> promotion certificate

This is the closest software object so far to:
    "identify every piece of structure that moves at an interface."

Top check:
    check_T_interface_structure_movement_graph_P
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List, Set

try:
    from apf.interface_structure_transport_ledger import (
        StructureKind,
        StructureStatus,
        InterfaceStructureTransportLedger,
        InterfaceStructureItem,
        LedgerCertificate,
        certify_ledger,
    )
    from apf.interface_structure_discovery_engine import (
        discover_ledger,
        discover_and_certify,
        canonical_payloads,
    )
except Exception as exc:  # pragma: no cover
    raise ImportError(f"interface_structure_movement_graph requires discovery/ledger modules: {exc}") from exc


class NodeRole(str, Enum):
    SOURCE = "SOURCE"
    TARGET = "TARGET"
    BOTH = "BOTH"


@dataclass(frozen=True)
class MovementNode:
    node_id: str
    label: str
    role: NodeRole


@dataclass(frozen=True)
class MovementEdge:
    edge_id: str
    structure_name: str
    kind: StructureKind
    source: str
    target: str
    required: bool
    status: StructureStatus
    obstruction_hint: Tuple[str, ...]
    notes: str = ""

    @property
    def moves_cleanly(self) -> bool:
        return self.status in {StructureStatus.PRESENT_STABLE, StructureStatus.MOVES_CLEANLY}

    @property
    def is_failed_required(self) -> bool:
        return self.required and not self.moves_cleanly


@dataclass(frozen=True)
class InterfaceStructureMovementGraph:
    name: str
    sector: str
    nodes: Tuple[MovementNode, ...]
    edges: Tuple[MovementEdge, ...]
    ledger_certificate: Dict[str, Any]

    def edge_witnesses_for_obstruction(self, obstruction: str) -> Tuple[MovementEdge, ...]:
        return tuple(
            edge for edge in self.edges
            if obstruction in edge.obstruction_hint and edge.is_failed_required
        )

    def obstruction_witness_paths(self) -> Dict[str, Tuple[Tuple[str, str, str], ...]]:
        obstructions = tuple(self.ledger_certificate["certificate"]["obstruction"])
        out: Dict[str, Tuple[Tuple[str, str, str], ...]] = {}
        for obs in obstructions:
            witnesses = self.edge_witnesses_for_obstruction(obs)
            out[obs] = tuple((edge.source, edge.structure_name, edge.target) for edge in witnesses)
        return out

    def missing_or_blocked_edges(self) -> Tuple[MovementEdge, ...]:
        return tuple(edge for edge in self.edges if edge.is_failed_required)

    def kinds_present(self) -> Tuple[str, ...]:
        return tuple(sorted({edge.kind.value for edge in self.edges}))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "sector": self.sector,
            "nodes": [asdict(node) | {"role": node.role.value} for node in self.nodes],
            "edges": [
                {
                    "edge_id": edge.edge_id,
                    "structure_name": edge.structure_name,
                    "kind": edge.kind.value,
                    "source": edge.source,
                    "target": edge.target,
                    "required": edge.required,
                    "status": edge.status.value,
                    "obstruction_hint": edge.obstruction_hint,
                    "notes": edge.notes,
                }
                for edge in self.edges
            ],
            "kinds_present": self.kinds_present(),
            "missing_or_blocked_edges": [
                {
                    "edge_id": edge.edge_id,
                    "structure_name": edge.structure_name,
                    "kind": edge.kind.value,
                    "source": edge.source,
                    "target": edge.target,
                    "status": edge.status.value,
                    "obstruction_hint": edge.obstruction_hint,
                }
                for edge in self.missing_or_blocked_edges()
            ],
            "obstruction_witness_paths": self.obstruction_witness_paths(),
            "certificate": self.ledger_certificate["certificate"],
        }


def _node_id(label: str) -> str:
    return label.strip().lower().replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")


def movement_graph_from_ledger(ledger: InterfaceStructureTransportLedger) -> InterfaceStructureMovementGraph:
    cert = certify_ledger(ledger).to_dict()

    sources = {item.source for item in ledger.items}
    targets = {item.target for item in ledger.items}
    all_nodes = sorted(sources | targets)
    nodes = []
    for label in all_nodes:
        if label in sources and label in targets:
            role = NodeRole.BOTH
        elif label in sources:
            role = NodeRole.SOURCE
        else:
            role = NodeRole.TARGET
        nodes.append(MovementNode(node_id=_node_id(label), label=label, role=role))

    edges = []
    for i, item in enumerate(ledger.items):
        edge_id = f"{ledger.name}:{i}:{item.kind.value}"
        edges.append(
            MovementEdge(
                edge_id=edge_id,
                structure_name=item.name,
                kind=item.kind,
                source=item.source,
                target=item.target,
                required=item.required,
                status=item.status,
                obstruction_hint=item.obstruction_hint,
                notes=item.notes,
            )
        )

    return InterfaceStructureMovementGraph(
        name=ledger.name,
        sector=ledger.sector,
        nodes=tuple(nodes),
        edges=tuple(edges),
        ledger_certificate=cert,
    )


def discover_movement_graph(route: str, payload: Mapping[str, Any]) -> InterfaceStructureMovementGraph:
    return movement_graph_from_ledger(discover_ledger(route, payload))


def movement_graph_report(route: str, payload: Mapping[str, Any]) -> Dict[str, Any]:
    graph = discover_movement_graph(route, payload)
    data = graph.to_dict()
    data["all_obstructions_have_paths"] = all(
        bool(paths)
        for paths in data["obstruction_witness_paths"].values()
    )
    data["all_edges_typed"] = all(
        edge["kind"] and edge["source"] and edge["target"] and edge["status"]
        for edge in data["edges"]
    )
    return data


def canonical_graphs() -> Dict[str, InterfaceStructureMovementGraph]:
    out = {}
    for key, payload in canonical_payloads().items():
        raw = dict(payload)
        route = str(raw.pop("route"))
        out[key] = discover_movement_graph(route, raw)
    return out


def graph_kind_coverage(graphs: Mapping[str, InterfaceStructureMovementGraph]) -> Tuple[str, ...]:
    kinds: Set[str] = set()
    for graph in graphs.values():
        kinds.update(graph.kinds_present())
    return tuple(sorted(kinds))


def check_T_movement_graph_construction_P() -> Dict[str, Any]:
    graphs = canonical_graphs()
    tests = {
        "graph_count": len(graphs) >= 9,
        "all_have_nodes": all(len(g.nodes) > 0 for g in graphs.values()),
        "all_have_edges": all(len(g.edges) > 0 for g in graphs.values()),
        "all_edges_have_source_target": all(edge.source and edge.target for g in graphs.values() for edge in g.edges),
        "all_edges_have_kind_status": all(edge.kind and edge.status for g in graphs.values() for edge in g.edges),
    }
    return {
        "name": "check_T_movement_graph_construction_P",
        "consistent": all(tests.values()),
        "status": "P_graph" if all(tests.values()) else "FAIL",
        "summary": "Canonical route payloads construct explicit source-target movement graphs with typed edges.",
        "data": {"tests": tests, "graph_names": list(graphs.keys())},
    }


def check_T_movement_graph_kind_coverage_P() -> Dict[str, Any]:
    graphs = canonical_graphs()
    coverage = set(graph_kind_coverage(graphs))
    required = {
        "ACC_RECORD",
        "TRACE_INPUT",
        "SCHEME_CONTRACT",
        "CAPACITY_COST",
        "CODOMAIN_TRANSPORT",
        "EVALUATOR_MAP",
        "OVERLAP_GLUING",
        "PROVENANCE",
        "FIBER_ACTION",
        "SUBSTRATE_BOUNDARY",
        "EMPIRICAL_POSTERIOR",
        "EXTERNAL_CONSTANT",
        "COUNTERTERM",
        "UNCERTAINTY_PROTOCOL",
    }
    tests = {
        "all_required_kinds_covered": required.issubset(coverage),
        "coverage_count": len(coverage) >= len(required),
    }
    return {
        "name": "check_T_movement_graph_kind_coverage_P",
        "consistent": all(tests.values()),
        "status": "P_graph" if all(tests.values()) else "FAIL",
        "summary": "Movement graph coverage includes all currently typed interface-moving structure kinds.",
        "data": {"tests": tests, "coverage": sorted(coverage)},
        "dependencies": ["check_T_movement_graph_construction_P"],
    }


def check_T_obstruction_witness_paths_P() -> Dict[str, Any]:
    graphs = canonical_graphs()
    path_results = {}
    for name, graph in graphs.items():
        paths = graph.obstruction_witness_paths()
        if paths:
            path_results[name] = {obs: bool(path) for obs, path in paths.items()}
    tests = {
        "has_nonzero_graphs": len(path_results) >= 6,
        "all_nonzero_obstructions_have_paths": all(all(v.values()) for v in path_results.values()),
    }
    return {
        "name": "check_T_obstruction_witness_paths_P",
        "consistent": all(tests.values()),
        "status": "P_graph" if all(tests.values()) else "FAIL",
        "summary": "Every nonzero obstruction is witnessed by at least one source->structure->target path.",
        "data": {"tests": tests, "path_results": path_results},
        "dependencies": ["check_T_movement_graph_kind_coverage_P"],
    }


def check_T_zero_export_has_clean_graph_P() -> Dict[str, Any]:
    graphs = canonical_graphs()
    clean_graphs = {
        name: graph for name, graph in graphs.items()
        if graph.ledger_certificate["certificate"]["export_global_P"]
    }
    tests = {
        "has_clean_export": len(clean_graphs) >= 1,
        "clean_exports_have_no_failed_required_edges": all(len(g.missing_or_blocked_edges()) == 0 for g in clean_graphs.values()),
        "clean_exports_have_zero_obstruction": all(g.ledger_certificate["certificate"]["obstruction"] == tuple() for g in clean_graphs.values()),
    }
    return {
        "name": "check_T_zero_export_has_clean_graph_P",
        "consistent": all(tests.values()),
        "status": "P_graph" if all(tests.values()) else "FAIL",
        "summary": "Every global-export example has a clean movement graph: no failed required edges and zero obstruction.",
        "data": {"tests": tests, "clean_exports": list(clean_graphs.keys())},
        "dependencies": ["check_T_obstruction_witness_paths_P"],
    }


def check_T_interface_structure_movement_graph_P() -> Dict[str, Any]:
    subchecks = [
        check_T_movement_graph_construction_P(),
        check_T_movement_graph_kind_coverage_P(),
        check_T_obstruction_witness_paths_P(),
        check_T_zero_export_has_clean_graph_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_interface_structure_movement_graph_P",
        "consistent": ok,
        "status": "P_movement_graph" if ok else "FAIL",
        "summary": "Interface Structure Movement Graph is P: moving structures are explicit source-target edges and every obstruction has a witness path.",
        "data": {
            "core_claim": "Every interface-moving structure is represented as a typed source->target edge before obstruction certification.",
            "subchecks": [x["name"] for x in subchecks],
            "kind_coverage": graph_kind_coverage(canonical_graphs()),
        },
        "dependencies": [x["name"] for x in subchecks],
    }


CHECKS = {
    "check_T_movement_graph_construction_P": check_T_movement_graph_construction_P,
    "check_T_movement_graph_kind_coverage_P": check_T_movement_graph_kind_coverage_P,
    "check_T_obstruction_witness_paths_P": check_T_obstruction_witness_paths_P,
    "check_T_zero_export_has_clean_graph_P": check_T_zero_export_has_clean_graph_P,
    "check_T_interface_structure_movement_graph_P": check_T_interface_structure_movement_graph_P,
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
            raise TypeError("Unsupported registry type for interface_structure_movement_graph.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
