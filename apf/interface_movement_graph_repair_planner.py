"""
APF Interface Movement Graph Repair Planner.

v24.3.12+ delta layer.

Purpose
-------
The movement graph identifies every moving structure as a source->target edge and maps
obstructions to failed/witness edges.  This module converts that graph into a concrete
repair plan:

    movement graph
      -> failed required edges
      -> obstruction witness paths
      -> ordered repair actions
      -> closure predicate / next P condition

Top check:
    check_T_interface_movement_graph_repair_planner_P

Important:
    This planner does not repair physics by assertion. It states the concrete edge-level
    actions that must be executed and rerun before promotion.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List, Set

try:
    from apf.interface_structure_movement_graph import (
        MovementEdge,
        InterfaceStructureMovementGraph,
        discover_movement_graph,
        movement_graph_report,
        canonical_graphs,
    )
except Exception as exc:  # pragma: no cover
    raise ImportError(f"interface_movement_graph_repair_planner requires movement graph module: {exc}") from exc


class GraphRepairClass(str, Enum):
    EXACT = "EXACT"
    ORDINARY_REPAIR_REQUIRED = "ORDINARY_REPAIR_REQUIRED"
    SUBSTRATE_REVISION_REQUIRED = "SUBSTRATE_REVISION_REQUIRED"
    FAIL_CLOSED_PROVENANCE = "FAIL_CLOSED_PROVENANCE"
    MIXED_BLOCKED = "MIXED_BLOCKED"


class RepairActionType(str, Enum):
    DECLARE_EVALUATOR = "DECLARE_EVALUATOR"
    DECLARE_CODOMAIN_TRANSPORT = "DECLARE_CODOMAIN_TRANSPORT"
    PROVE_OVERLAP_GLUING = "PROVE_OVERLAP_GLUING"
    REPAIR_CAPACITY_BUDGET = "REPAIR_CAPACITY_BUDGET"
    REBUILD_CLEAN_PROVENANCE = "REBUILD_CLEAN_PROVENANCE"
    OPEN_SUBSTRATE_REVISION_PROGRAM = "OPEN_SUBSTRATE_REVISION_PROGRAM"
    DECLARE_SCHEME_CONTRACT = "DECLARE_SCHEME_CONTRACT"
    DECLARE_EXTERNAL_CONSTANT_LEDGER = "DECLARE_EXTERNAL_CONSTANT_LEDGER"
    DECLARE_COUNTERTERM_SLOT = "DECLARE_COUNTERTERM_SLOT"
    DECLARE_UNCERTAINTY_PROTOCOL = "DECLARE_UNCERTAINTY_PROTOCOL"
    COMPLETE_EMPIRICAL_POSTERIOR = "COMPLETE_EMPIRICAL_POSTERIOR"
    COMPLETE_FIBER_ACTION = "COMPLETE_FIBER_ACTION"


@dataclass(frozen=True)
class GraphRepairAction:
    action_id: str
    action_type: RepairActionType
    obstruction: str
    edge_id: str
    structure_name: str
    structure_kind: str
    source: str
    target: str
    priority: int
    description: str


@dataclass(frozen=True)
class GraphRepairPlan:
    graph_name: str
    sector: str
    repair_class: GraphRepairClass
    already_global_P: bool
    actions: Tuple[GraphRepairAction, ...]
    fail_closed_reason: Optional[str]
    substrate_revision_reason: Optional[str]
    rerun_required: bool
    p_closure_condition: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "graph_name": self.graph_name,
            "sector": self.sector,
            "repair_class": self.repair_class.value,
            "already_global_P": self.already_global_P,
            "actions": [asdict(a) | {"action_type": a.action_type.value} for a in self.actions],
            "fail_closed_reason": self.fail_closed_reason,
            "substrate_revision_reason": self.substrate_revision_reason,
            "rerun_required": self.rerun_required,
            "p_closure_condition": self.p_closure_condition,
        }


STRUCTURAL_OBSTRUCTIONS = {
    "POLARITY_MISSING",
    "REVERSAL_MISSING",
    "COMPLEX_ACTION_MISSING",
    "NORM_MISSING",
}
ORDINARY_OBSTRUCTIONS = {
    "EVALUATOR_MISSING",
    "CODOMAIN_MISMATCH",
    "CAPACITY_OVERSPEND",
    "OVERLAP_INCOHERENCE",
}
PROVENANCE_OBSTRUCTIONS = {"PROVENANCE_SMUGGLE"}


def _action_type_for(edge: MovementEdge, obstruction: str) -> RepairActionType:
    if obstruction == "PROVENANCE_SMUGGLE":
        return RepairActionType.REBUILD_CLEAN_PROVENANCE
    if obstruction in STRUCTURAL_OBSTRUCTIONS:
        return RepairActionType.OPEN_SUBSTRATE_REVISION_PROGRAM
    if obstruction == "CODOMAIN_MISMATCH":
        return RepairActionType.DECLARE_CODOMAIN_TRANSPORT
    if obstruction == "CAPACITY_OVERSPEND":
        return RepairActionType.REPAIR_CAPACITY_BUDGET
    if obstruction == "OVERLAP_INCOHERENCE":
        return RepairActionType.PROVE_OVERLAP_GLUING
    if obstruction == "EVALUATOR_MISSING":
        kind = edge.kind.value
        if kind == "SCHEME_CONTRACT":
            return RepairActionType.DECLARE_SCHEME_CONTRACT
        if kind == "EXTERNAL_CONSTANT":
            return RepairActionType.DECLARE_EXTERNAL_CONSTANT_LEDGER
        if kind == "COUNTERTERM":
            return RepairActionType.DECLARE_COUNTERTERM_SLOT
        if kind == "UNCERTAINTY_PROTOCOL":
            return RepairActionType.DECLARE_UNCERTAINTY_PROTOCOL
        if kind == "EMPIRICAL_POSTERIOR":
            return RepairActionType.COMPLETE_EMPIRICAL_POSTERIOR
        if kind == "FIBER_ACTION":
            return RepairActionType.COMPLETE_FIBER_ACTION
        return RepairActionType.DECLARE_EVALUATOR
    return RepairActionType.DECLARE_EVALUATOR


def _priority_for(action_type: RepairActionType) -> int:
    order = {
        RepairActionType.REBUILD_CLEAN_PROVENANCE: 0,
        RepairActionType.OPEN_SUBSTRATE_REVISION_PROGRAM: 1,
        RepairActionType.DECLARE_SCHEME_CONTRACT: 10,
        RepairActionType.DECLARE_EXTERNAL_CONSTANT_LEDGER: 11,
        RepairActionType.DECLARE_COUNTERTERM_SLOT: 12,
        RepairActionType.DECLARE_UNCERTAINTY_PROTOCOL: 13,
        RepairActionType.DECLARE_CODOMAIN_TRANSPORT: 20,
        RepairActionType.DECLARE_EVALUATOR: 30,
        RepairActionType.COMPLETE_EMPIRICAL_POSTERIOR: 31,
        RepairActionType.COMPLETE_FIBER_ACTION: 32,
        RepairActionType.PROVE_OVERLAP_GLUING: 40,
        RepairActionType.REPAIR_CAPACITY_BUDGET: 50,
    }
    return order[action_type]


def _description(action_type: RepairActionType, edge: MovementEdge, obstruction: str) -> str:
    if action_type == RepairActionType.REBUILD_CLEAN_PROVENANCE:
        return f"Rebuild route so '{edge.structure_name}' does not consume target/posterior/fitted output as input."
    if action_type == RepairActionType.OPEN_SUBSTRATE_REVISION_PROGRAM:
        return f"Do not promote under current primitives; open substrate-revision program for '{edge.structure_name}' ({obstruction})."
    if action_type == RepairActionType.DECLARE_CODOMAIN_TRANSPORT:
        return f"Declare and verify codomain transport for '{edge.structure_name}' from {edge.source} to {edge.target}."
    if action_type == RepairActionType.REPAIR_CAPACITY_BUDGET:
        return f"Repair capacity budget for '{edge.structure_name}' by reducing load, increasing budget, or applying admissible coarse-graining, then rerun."
    if action_type == RepairActionType.PROVE_OVERLAP_GLUING:
        return f"Prove overlap/gluing/coherence for '{edge.structure_name}' across {edge.source} -> {edge.target}."
    if action_type == RepairActionType.DECLARE_SCHEME_CONTRACT:
        return f"Declare target-scheme contract for '{edge.structure_name}'."
    if action_type == RepairActionType.DECLARE_EXTERNAL_CONSTANT_LEDGER:
        return f"Declare clean external-constant ledger for '{edge.structure_name}'."
    if action_type == RepairActionType.DECLARE_COUNTERTERM_SLOT:
        return f"Declare finite counterterm/renormalization slot for '{edge.structure_name}'."
    if action_type == RepairActionType.DECLARE_UNCERTAINTY_PROTOCOL:
        return f"Declare uncertainty/comparison protocol for '{edge.structure_name}'."
    if action_type == RepairActionType.COMPLETE_EMPIRICAL_POSTERIOR:
        return f"Complete posterior/convergence/robustness closure for '{edge.structure_name}'."
    if action_type == RepairActionType.COMPLETE_FIBER_ACTION:
        return f"Complete fiber-action/evaluator proof for '{edge.structure_name}'."
    return f"Declare and verify evaluator map for '{edge.structure_name}' from {edge.source} to {edge.target}."


def repair_actions_for_graph(graph: InterfaceStructureMovementGraph) -> Tuple[GraphRepairAction, ...]:
    actions: List[GraphRepairAction] = []
    seen = set()
    witness_paths = graph.obstruction_witness_paths()
    for obstruction, _paths in witness_paths.items():
        witnesses = graph.edge_witnesses_for_obstruction(obstruction)
        for edge in witnesses:
            action_type = _action_type_for(edge, obstruction)
            key = (obstruction, edge.edge_id, action_type.value)
            if key in seen:
                continue
            seen.add(key)
            actions.append(
                GraphRepairAction(
                    action_id=f"{graph.name}:{len(actions):03d}:{action_type.value}",
                    action_type=action_type,
                    obstruction=obstruction,
                    edge_id=edge.edge_id,
                    structure_name=edge.structure_name,
                    structure_kind=edge.kind.value,
                    source=edge.source,
                    target=edge.target,
                    priority=_priority_for(action_type),
                    description=_description(action_type, edge, obstruction),
                )
            )
    return tuple(sorted(actions, key=lambda a: (a.priority, a.obstruction, a.structure_name)))


def classify_repair(actions: Tuple[GraphRepairAction, ...], already_global_P: bool) -> GraphRepairClass:
    if already_global_P and not actions:
        return GraphRepairClass.EXACT
    obstructions = {a.obstruction for a in actions}
    if obstructions & PROVENANCE_OBSTRUCTIONS:
        return GraphRepairClass.FAIL_CLOSED_PROVENANCE
    if obstructions and obstructions <= STRUCTURAL_OBSTRUCTIONS:
        return GraphRepairClass.SUBSTRATE_REVISION_REQUIRED
    if obstructions & STRUCTURAL_OBSTRUCTIONS:
        return GraphRepairClass.MIXED_BLOCKED
    if actions:
        return GraphRepairClass.ORDINARY_REPAIR_REQUIRED
    return GraphRepairClass.EXACT


def plan_graph_repair(graph: InterfaceStructureMovementGraph) -> GraphRepairPlan:
    already_global = bool(graph.ledger_certificate["certificate"]["export_global_P"])
    actions = repair_actions_for_graph(graph)
    repair_class = classify_repair(actions, already_global)
    fail_closed_reason = None
    substrate_revision_reason = None

    if repair_class == GraphRepairClass.FAIL_CLOSED_PROVENANCE:
        fail_closed_reason = "Provenance smuggling is present; rebuild from clean provenance before any promotion."
    if repair_class in {GraphRepairClass.SUBSTRATE_REVISION_REQUIRED, GraphRepairClass.MIXED_BLOCKED}:
        substrate_revision_reason = "At least one required edge depends on substrate primitives not available in current APF layer."

    if repair_class == GraphRepairClass.EXACT:
        closure = "Already P: graph has zero obstruction and no failed required edges."
    elif repair_class == GraphRepairClass.FAIL_CLOSED_PROVENANCE:
        closure = "Rebuild from clean provenance, regenerate graph, and rerun; do not repair by algebraic patch."
    elif repair_class == GraphRepairClass.SUBSTRATE_REVISION_REQUIRED:
        closure = "Open/complete a substrate revision theorem program, regenerate graph, and rerun."
    elif repair_class == GraphRepairClass.MIXED_BLOCKED:
        closure = "Resolve provenance/structural blockers first, then execute remaining ordinary repairs and rerun."
    else:
        closure = "Execute all ordered repair actions, regenerate the movement graph, and rerun until obstruction is zero."

    return GraphRepairPlan(
        graph_name=graph.name,
        sector=graph.sector,
        repair_class=repair_class,
        already_global_P=already_global,
        actions=actions,
        fail_closed_reason=fail_closed_reason,
        substrate_revision_reason=substrate_revision_reason,
        rerun_required=repair_class != GraphRepairClass.EXACT,
        p_closure_condition=closure,
    )


def discover_and_plan_repair(route: str, payload: Mapping[str, Any]) -> Dict[str, Any]:
    graph = discover_movement_graph(route, payload)
    plan = plan_graph_repair(graph)
    return {
        "graph": graph.to_dict(),
        "repair_plan": plan.to_dict(),
    }


def canonical_repair_plans() -> Dict[str, GraphRepairPlan]:
    return {name: plan_graph_repair(graph) for name, graph in canonical_graphs().items()}


def check_T_graph_repair_actions_from_witnesses_P() -> Dict[str, Any]:
    graphs = canonical_graphs()
    plans = {name: plan_graph_repair(graph) for name, graph in graphs.items()}
    tests = {
        "EW_open_has_actions": len(plans["ew_open"].actions) >= 4,
        "EW_open_has_codomain_action": any(a.action_type == RepairActionType.DECLARE_CODOMAIN_TRANSPORT for a in plans["ew_open"].actions),
        "EW_open_has_scheme_or_evaluator_action": any(a.action_type in {RepairActionType.DECLARE_SCHEME_CONTRACT, RepairActionType.DECLARE_EVALUATOR, RepairActionType.DECLARE_COUNTERTERM_SLOT, RepairActionType.DECLARE_UNCERTAINTY_PROTOCOL} for a in plans["ew_open"].actions),
        "dark_open_has_posterior_action": any(a.action_type == RepairActionType.COMPLETE_EMPIRICAL_POSTERIOR for a in plans["dark_open"].actions),
        "gauge_open_has_codomain_action": any(a.action_type == RepairActionType.DECLARE_CODOMAIN_TRANSPORT for a in plans["gauge_codomain_open"].actions),
        "horizon_open_has_gluing_action": any(a.action_type == RepairActionType.PROVE_OVERLAP_GLUING for a in plans["horizon_overlap_open"].actions),
    }
    return {
        "name": "check_T_graph_repair_actions_from_witnesses_P",
        "consistent": all(tests.values()),
        "status": "P_repair_graph" if all(tests.values()) else "FAIL",
        "summary": "Repair planner converts obstruction witness edges into concrete route-specific actions.",
        "data": {"tests": tests, "action_counts": {k: len(v.actions) for k, v in plans.items()}},
    }


def check_T_graph_repair_classification_P() -> Dict[str, Any]:
    plans = canonical_repair_plans()
    tests = {
        "EW_open_ordinary": plans["ew_open"].repair_class == GraphRepairClass.ORDINARY_REPAIR_REQUIRED,
        "EW_closed_exact": plans["ew_closed"].repair_class == GraphRepairClass.EXACT,
        "provenance_smuggled_fail_closed": plans["provenance_smuggled"].repair_class == GraphRepairClass.FAIL_CLOSED_PROVENANCE,
        "dark_open_ordinary": plans["dark_open"].repair_class == GraphRepairClass.ORDINARY_REPAIR_REQUIRED,
        "flat_Cstar_mixed_blocked": plans["cstar"].repair_class == GraphRepairClass.MIXED_BLOCKED,
        "generic_open_ordinary": plans["generic_evaluator_codomain_open"].repair_class == GraphRepairClass.ORDINARY_REPAIR_REQUIRED,
    }
    return {
        "name": "check_T_graph_repair_classification_P",
        "consistent": all(tests.values()),
        "status": "P_repair_graph" if all(tests.values()) else "FAIL",
        "summary": "Repair planner classifies exact, ordinary repair, substrate revision, and fail-closed provenance cases.",
        "data": {"tests": tests, "classes": {k: v.repair_class.value for k, v in plans.items()}},
        "dependencies": ["check_T_graph_repair_actions_from_witnesses_P"],
    }


def check_T_graph_repair_ordering_P() -> Dict[str, Any]:
    plans = canonical_repair_plans()
    tests = {}
    for name, plan in plans.items():
        priorities = [a.priority for a in plan.actions]
        tests[f"{name}_priority_sorted"] = priorities == sorted(priorities)
    tests["EW_open_ordered_before_rerun"] = plans["ew_open"].rerun_required is True
    tests["EW_closed_no_rerun"] = plans["ew_closed"].rerun_required is False
    return {
        "name": "check_T_graph_repair_ordering_P",
        "consistent": all(tests.values()),
        "status": "P_repair_graph" if all(tests.values()) else "FAIL",
        "summary": "Repair actions are priority ordered and exact cases do not require rerun.",
        "data": {"tests": tests},
        "dependencies": ["check_T_graph_repair_classification_P"],
    }


def check_T_graph_repair_closure_predicates_P() -> Dict[str, Any]:
    plans = canonical_repair_plans()
    tests = {
        "exact_mentions_already_P": "Already P" in plans["ew_closed"].p_closure_condition,
        "ordinary_mentions_rerun": "rerun" in plans["ew_open"].p_closure_condition.lower(),
        "provenance_mentions_clean": "clean provenance" in plans["provenance_smuggled"].p_closure_condition.lower(),
        "substrate_mentions_structural": "structural" in plans["cstar"].p_closure_condition.lower(),
    }
    return {
        "name": "check_T_graph_repair_closure_predicates_P",
        "consistent": all(tests.values()),
        "status": "P_repair_graph" if all(tests.values()) else "FAIL",
        "summary": "Repair plans produce explicit P-closure conditions.",
        "data": {"tests": tests, "closure_conditions": {k: v.p_closure_condition for k, v in plans.items()}},
        "dependencies": ["check_T_graph_repair_ordering_P"],
    }


def check_T_interface_movement_graph_repair_planner_P() -> Dict[str, Any]:
    subchecks = [
        check_T_graph_repair_actions_from_witnesses_P(),
        check_T_graph_repair_classification_P(),
        check_T_graph_repair_ordering_P(),
        check_T_graph_repair_closure_predicates_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_interface_movement_graph_repair_planner_P",
        "consistent": ok,
        "status": "P_repair_planner" if ok else "FAIL",
        "summary": "Interface Movement Graph Repair Planner is P: failed movement edges become ordered repair actions with closure predicates.",
        "data": {
            "core_claim": "Each nonzero movement-graph obstruction yields concrete edge-level repair actions or a fail-closed/substrate-revision certificate.",
            "subchecks": [x["name"] for x in subchecks],
            "repair_classes": [x.value for x in GraphRepairClass],
        },
        "dependencies": [x["name"] for x in subchecks],
    }


CHECKS = {
    "check_T_graph_repair_actions_from_witnesses_P": check_T_graph_repair_actions_from_witnesses_P,
    "check_T_graph_repair_classification_P": check_T_graph_repair_classification_P,
    "check_T_graph_repair_ordering_P": check_T_graph_repair_ordering_P,
    "check_T_graph_repair_closure_predicates_P": check_T_graph_repair_closure_predicates_P,
    "check_T_interface_movement_graph_repair_planner_P": check_T_interface_movement_graph_repair_planner_P,
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
            raise TypeError("Unsupported registry type for interface_movement_graph_repair_planner.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
