"""
APF Interface Repair Closure Simulator.

v24.3.12+ delta layer.

Purpose
-------
The repair planner turns failed movement-graph edges into ordered repair actions. This
module simulates safe ordinary-repair closure by producing candidate payload patches and
rerunning discovery/certification.

Important boundary:
    This simulator does not claim the physics repair has been executed.
    It answers: "If the named ordinary repair facts became true, would the gate close?"

It refuses to auto-patch:
    - provenance smuggling
    - substrate revision / structural blockers
    - mixed blocked cases with structural blockers

Top check:
    check_T_interface_repair_closure_simulator_P
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List

try:
    from apf.interface_structure_discovery_engine import discover_and_certify, discover_ledger
    from apf.interface_movement_graph_repair_planner import (
        discover_and_plan_repair,
        plan_graph_repair,
        GraphRepairClass,
        RepairActionType,
    )
    from apf.interface_structure_movement_graph import discover_movement_graph
except Exception as exc:  # pragma: no cover
    raise ImportError(f"interface_repair_closure_simulator requires repair planner stack: {exc}") from exc


class SimulationStatus(str, Enum):
    ALREADY_CLOSED = "ALREADY_CLOSED"
    SIMULATED_CLOSURE_REACHES_P = "SIMULATED_CLOSURE_REACHES_P"
    SIMULATED_PARTIAL_STILL_BLOCKED = "SIMULATED_PARTIAL_STILL_BLOCKED"
    REFUSE_PROVENANCE_AUTOPATCH = "REFUSE_PROVENANCE_AUTOPATCH"
    REFUSE_SUBSTRATE_AUTOPATCH = "REFUSE_SUBSTRATE_AUTOPATCH"
    UNSUPPORTED_ROUTE = "UNSUPPORTED_ROUTE"


@dataclass(frozen=True)
class PayloadPatch:
    field: str
    old_value: Any
    new_value: Any
    reason: str


@dataclass(frozen=True)
class ClosureSimulation:
    route: str
    original_payload: Mapping[str, Any]
    original_repair_class: GraphRepairClass
    simulation_status: SimulationStatus
    patches: Tuple[PayloadPatch, ...]
    patched_payload: Optional[Mapping[str, Any]]
    original_certificate: Mapping[str, Any]
    patched_certificate: Optional[Mapping[str, Any]]
    closure_claim: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "route": self.route,
            "original_payload": dict(self.original_payload),
            "original_repair_class": self.original_repair_class.value,
            "simulation_status": self.simulation_status.value,
            "patches": [asdict(p) for p in self.patches],
            "patched_payload": dict(self.patched_payload) if self.patched_payload is not None else None,
            "original_certificate": dict(self.original_certificate),
            "patched_certificate": dict(self.patched_certificate) if self.patched_certificate is not None else None,
            "closure_claim": self.closure_claim,
        }


def _set_patch(payload: Dict[str, Any], field: str, value: Any, reason: str, patches: List[PayloadPatch]) -> None:
    old = payload.get(field)
    if old != value:
        patches.append(PayloadPatch(field=field, old_value=old, new_value=value, reason=reason))
        payload[field] = value


def _capacity_min_factor(payload: Mapping[str, Any]) -> int:
    raw = int(payload.get("raw_capacity_load", 0))
    budget = int(payload.get("capacity_budget", 1))
    if budget <= 0:
        return 1
    return max(1, (raw + budget - 1) // budget)


def propose_ordinary_repair_patch(route: str, payload: Mapping[str, Any]) -> Tuple[PayloadPatch, ...]:
    """Return route-specific candidate patches for ordinary repair facts.

    These are not asserted as true physics; they are "what would need to be true" switches
    for closure simulation.
    """
    route_key = route.strip().lower().replace("-", "_")
    patched = dict(payload)
    patches: List[PayloadPatch] = []

    if route_key in {"ew", "ew_trace", "ew_trace_scheme"}:
        _set_patch(patched, "trace_sector_closed", True, "local APF_TRACE route must be closed", patches)
        _set_patch(patched, "source_to_scheme_registry_present", True, "target-scheme contract must be present", patches)
        _set_patch(patched, "evaluator_map_found", True, "physical scheme evaluator map must be declared", patches)
        _set_patch(patched, "codomain_transport_found", True, "codomain transport must be declared", patches)
        _set_patch(patched, "counterterm_finite_parts_declared", True, "counterterm finite parts must be declared", patches)
        _set_patch(patched, "external_constants_ledger_clean", True, "external constants ledger must be clean", patches)
        _set_patch(patched, "uncertainty_protocol_declared", True, "uncertainty/comparison protocol must be declared", patches)
        return tuple(patches)

    if route_key in {"dark", "dark_posterior"}:
        _set_patch(patched, "route_built", True, "dark route must be built", patches)
        _set_patch(patched, "run_completed", True, "dark run must complete", patches)
        _set_patch(patched, "chains_converged", True, "chains must converge", patches)
        _set_patch(patched, "posterior_closed", True, "posterior must close", patches)
        _set_patch(patched, "robustness_checks_passed", True, "robustness checks must pass", patches)
        _set_patch(patched, "data_ledger_clean", True, "data ledger must be clean", patches)
        _set_patch(patched, "evaluator_map_found", True, "empirical/posterior evaluator must be declared", patches)
        _set_patch(patched, "codomain_transport_found", True, "codomain transport must be declared", patches)
        return tuple(patches)

    if route_key in {"gauge", "gauge_fiber"}:
        _set_patch(patched, "local_fiber_action_defined", True, "fiber action must be defined", patches)
        _set_patch(patched, "group_law_verified", True, "group law must be verified", patches)
        _set_patch(patched, "representation_faithful", True, "representation faithfulness must be verified", patches)
        _set_patch(patched, "codomain_map_declared", True, "gauge codomain map must be declared", patches)
        _set_patch(patched, "overlap_cocycle_verified", True, "overlap/cocycle descent must be verified", patches)
        _set_patch(patched, "anomaly_check_passed", True, "anomaly/evaluator check must pass", patches)
        _set_patch(patched, "capacity_budget_verified", True, "capacity budget must be verified", patches)
        return tuple(patches)

    if route_key in {"horizon", "horizon_cost"}:
        _set_patch(patched, "horizon_partition_defined", True, "horizon partition must be defined", patches)
        _set_patch(patched, "area_cost_map_defined", True, "area cost map must be defined", patches)
        _set_patch(patched, "overlap_gluing_verified", True, "overlap/gluing must be verified", patches)
        _set_patch(patched, "capacity_bound_checked", True, "capacity bound must be checked", patches)
        _set_patch(patched, "entropy_ledger_clean", True, "entropy ledger must be clean", patches)
        _set_patch(patched, "codomain_transport_found", True, "codomain transport must be declared", patches)
        _set_patch(patched, "capacity_overspend_detected", False, "capacity overspend must be resolved", patches)
        return tuple(patches)

    if route_key in {"capacity", "coarse_grain"}:
        factor = _capacity_min_factor(payload)
        _set_patch(patched, "coarse_grain_factor", factor, "minimum coarse-grain factor required to fit capacity budget", patches)
        _set_patch(patched, "target_value_consumed", False, "capacity experiment must not consume target value", patches)
        return tuple(patches)

    if route_key in {"generic"}:
        _set_patch(patched, "local_solution_found", True, "local solution must be found", patches)
        _set_patch(patched, "acc_base_present", True, "ACC base must be present", patches)
        _set_patch(patched, "evaluator_map_found", True, "evaluator map must be present", patches)
        _set_patch(patched, "codomain_transport_found", True, "codomain transport must be present", patches)
        _set_patch(patched, "overlap_gluing_verified", True, "overlap gluing must be verified", patches)
        _set_patch(patched, "capacity_budget_verified", True, "capacity budget must be verified", patches)
        _set_patch(patched, "capacity_overspend_detected", False, "capacity overspend must be resolved", patches)
        _set_patch(patched, "empirical_or_posterior_closed", True, "posterior/empirical closure must hold", patches)
        return tuple(patches)

    return tuple(patches)


def apply_patches(payload: Mapping[str, Any], patches: Iterable[PayloadPatch]) -> Dict[str, Any]:
    out = dict(payload)
    for patch in patches:
        out[patch.field] = patch.new_value
    return out


def simulate_repair_closure(route: str, payload: Mapping[str, Any]) -> ClosureSimulation:
    original_report = discover_and_plan_repair(route, payload)
    original_graph = original_report["graph"]
    original_plan = original_report["repair_plan"]
    original_cert = original_graph["certificate"]
    original_class = GraphRepairClass(original_plan["repair_class"])

    if original_class == GraphRepairClass.EXACT:
        return ClosureSimulation(
            route=route,
            original_payload=dict(payload),
            original_repair_class=original_class,
            simulation_status=SimulationStatus.ALREADY_CLOSED,
            patches=tuple(),
            patched_payload=None,
            original_certificate=original_cert,
            patched_certificate=None,
            closure_claim="Already P: no simulated repair required.",
        )

    if original_class == GraphRepairClass.FAIL_CLOSED_PROVENANCE:
        return ClosureSimulation(
            route=route,
            original_payload=dict(payload),
            original_repair_class=original_class,
            simulation_status=SimulationStatus.REFUSE_PROVENANCE_AUTOPATCH,
            patches=tuple(),
            patched_payload=None,
            original_certificate=original_cert,
            patched_certificate=None,
            closure_claim="Refused: provenance smuggling cannot be auto-patched; rebuild from clean provenance.",
        )

    if original_class in {GraphRepairClass.SUBSTRATE_REVISION_REQUIRED, GraphRepairClass.MIXED_BLOCKED}:
        patches = propose_ordinary_repair_patch(route, payload)
        patched_payload = apply_patches(payload, patches)
        patched_cert = None
        try:
            patched_cert = discover_and_plan_repair(route, patched_payload)["graph"]["certificate"]
        except Exception:
            patched_cert = None
        return ClosureSimulation(
            route=route,
            original_payload=dict(payload),
            original_repair_class=original_class,
            simulation_status=SimulationStatus.REFUSE_SUBSTRATE_AUTOPATCH if patched_cert is None or not patched_cert.get("export_global_P") else SimulationStatus.SIMULATED_PARTIAL_STILL_BLOCKED,
            patches=patches,
            patched_payload=patched_payload,
            original_certificate=original_cert,
            patched_certificate=patched_cert,
            closure_claim="Refused/blocked: structural substrate requirements cannot be auto-patched by ordinary route fields.",
        )

    patches = propose_ordinary_repair_patch(route, payload)
    patched_payload = apply_patches(payload, patches)
    patched_report = discover_and_plan_repair(route, patched_payload)
    patched_cert = patched_report["graph"]["certificate"]

    status = SimulationStatus.SIMULATED_CLOSURE_REACHES_P if patched_cert.get("export_global_P") else SimulationStatus.SIMULATED_PARTIAL_STILL_BLOCKED
    claim = (
        "Simulated ordinary-repair facts close the gate to global P. This is a counterfactual closure test, not proof the repair was executed."
        if status == SimulationStatus.SIMULATED_CLOSURE_REACHES_P
        else "Simulated ordinary-repair facts do not close all obstructions; inspect patched certificate."
    )

    return ClosureSimulation(
        route=route,
        original_payload=dict(payload),
        original_repair_class=original_class,
        simulation_status=status,
        patches=patches,
        patched_payload=patched_payload,
        original_certificate=original_cert,
        patched_certificate=patched_cert,
        closure_claim=claim,
    )


def canonical_payloads_for_simulation() -> Dict[str, Tuple[str, Mapping[str, Any]]]:
    return {
        "ew_open": ("ew", {
            "name": "sim_EW_open",
            "trace_sector_closed": True,
            "source_to_scheme_registry_present": True,
            "evaluator_map_found": False,
            "codomain_transport_found": False,
            "counterterm_finite_parts_declared": False,
            "external_constants_ledger_clean": True,
            "uncertainty_protocol_declared": False,
            "target_value_consumed": False,
        }),
        "dark_open": ("dark", {
            "name": "sim_dark_open",
            "route_built": True,
            "run_completed": True,
            "chains_converged": False,
            "posterior_closed": False,
            "robustness_checks_passed": False,
            "data_ledger_clean": True,
            "evaluator_map_found": False,
            "codomain_transport_found": True,
            "target_value_consumed": False,
        }),
        "gauge_open": ("gauge", {
            "name": "sim_gauge_open",
            "local_fiber_action_defined": True,
            "group_law_verified": True,
            "representation_faithful": True,
            "codomain_map_declared": False,
            "overlap_cocycle_verified": True,
            "anomaly_check_passed": True,
            "capacity_budget_verified": True,
            "target_value_consumed": False,
        }),
        "horizon_open": ("horizon", {
            "name": "sim_horizon_open",
            "horizon_partition_defined": True,
            "area_cost_map_defined": True,
            "overlap_gluing_verified": False,
            "capacity_bound_checked": True,
            "entropy_ledger_clean": True,
            "codomain_transport_found": True,
            "target_value_consumed": False,
        }),
        "capacity_open": ("capacity", {
            "name": "sim_capacity_open",
            "raw_capacity_load": 100,
            "capacity_budget": 25,
            "coarse_grain_factor": 2,
        }),
        "provenance_smuggled": ("provenance", {
            "name": "sim_provenance_smuggled",
            "sector": "EW",
            "inputs_used": ["alpha_em", "M_W_physical"],
            "declared_targets": ["M_W_physical"],
            "fitted_outputs": ["posterior_M_W"],
            "posterior_outputs": ["fit_pull"],
            "allowed_exogenous_inputs": ["alpha_em"],
        }),
        "cstar": ("cstar", {
            "name": "sim_cstar",
        }),
        "ew_closed": ("ew", {
            "name": "sim_EW_closed",
            "trace_sector_closed": True,
            "source_to_scheme_registry_present": True,
            "evaluator_map_found": True,
            "codomain_transport_found": True,
            "counterterm_finite_parts_declared": True,
            "external_constants_ledger_clean": True,
            "uncertainty_protocol_declared": True,
            "target_value_consumed": False,
        }),
    }


def run_canonical_simulations() -> Dict[str, Dict[str, Any]]:
    return {
        name: simulate_repair_closure(route, payload).to_dict()
        for name, (route, payload) in canonical_payloads_for_simulation().items()
    }


def check_T_ordinary_repair_simulates_to_P_P() -> Dict[str, Any]:
    sims = run_canonical_simulations()
    ordinary = ["ew_open", "dark_open", "gauge_open", "horizon_open", "capacity_open"]
    tests = {
        f"{name}_reaches_P": sims[name]["simulation_status"] == "SIMULATED_CLOSURE_REACHES_P"
        and sims[name]["patched_certificate"]["export_global_P"] is True
        for name in ordinary
    }
    tests["all_have_patches"] = all(len(sims[name]["patches"]) > 0 for name in ordinary)
    return {
        "name": "check_T_ordinary_repair_simulates_to_P_P",
        "consistent": all(tests.values()),
        "status": "P_sim",
        "summary": "Ordinary repair cases have candidate payload patches that simulate closure to global P.",
        "data": {"tests": tests, "patch_counts": {name: len(sims[name]["patches"]) for name in ordinary}},
    }


def check_T_provenance_and_structural_refuse_autopatch_P() -> Dict[str, Any]:
    sims = run_canonical_simulations()
    tests = {
        "provenance_refused": sims["provenance_smuggled"]["simulation_status"] == "REFUSE_PROVENANCE_AUTOPATCH",
        "provenance_no_patched_payload": sims["provenance_smuggled"]["patched_payload"] is None,
        "cstar_refused": sims["cstar"]["simulation_status"] in {"REFUSE_SUBSTRATE_AUTOPATCH", "SIMULATED_PARTIAL_STILL_BLOCKED"},
        "cstar_not_global": sims["cstar"]["patched_certificate"] is None or sims["cstar"]["patched_certificate"]["export_global_P"] is False,
    }
    return {
        "name": "check_T_provenance_and_structural_refuse_autopatch_P",
        "consistent": all(tests.values()),
        "status": "P_sim",
        "summary": "Simulator refuses provenance and substrate/structural auto-patching.",
        "data": {"tests": tests},
        "dependencies": ["check_T_ordinary_repair_simulates_to_P_P"],
    }


def check_T_exact_case_no_patch_P() -> Dict[str, Any]:
    sims = run_canonical_simulations()
    tests = {
        "ew_closed_already_closed": sims["ew_closed"]["simulation_status"] == "ALREADY_CLOSED",
        "ew_closed_no_patches": sims["ew_closed"]["patches"] == [],
        "ew_closed_original_global": sims["ew_closed"]["original_certificate"]["export_global_P"] is True,
    }
    return {
        "name": "check_T_exact_case_no_patch_P",
        "consistent": all(tests.values()),
        "status": "P_sim",
        "summary": "Exact/closed cases produce no unnecessary repair patches.",
        "data": {"tests": tests},
        "dependencies": ["check_T_provenance_and_structural_refuse_autopatch_P"],
    }


def check_T_patch_semantics_are_counterfactual_P() -> Dict[str, Any]:
    sims = run_canonical_simulations()
    tests = {
        "ew_claim_mentions_counterfactual": "counterfactual" in sims["ew_open"]["closure_claim"].lower(),
        "provenance_claim_mentions_refused": "refused" in sims["provenance_smuggled"]["closure_claim"].lower(),
        "cstar_claim_mentions_structural": "structural" in sims["cstar"]["closure_claim"].lower(),
    }
    return {
        "name": "check_T_patch_semantics_are_counterfactual_P",
        "consistent": all(tests.values()),
        "status": "P_audit",
        "summary": "Closure simulation language preserves the no-smuggling boundary: patches are counterfactual checks, not executed physics.",
        "data": {"tests": tests},
        "dependencies": ["check_T_exact_case_no_patch_P"],
    }


def check_T_interface_repair_closure_simulator_P() -> Dict[str, Any]:
    subchecks = [
        check_T_ordinary_repair_simulates_to_P_P(),
        check_T_provenance_and_structural_refuse_autopatch_P(),
        check_T_exact_case_no_patch_P(),
        check_T_patch_semantics_are_counterfactual_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_interface_repair_closure_simulator_P",
        "consistent": ok,
        "status": "P_closure_sim" if ok else "FAIL",
        "summary": "Interface Repair Closure Simulator is P: ordinary repairs can be counterfactually patched and rerun, while provenance/structural blockers refuse auto-patching.",
        "data": {
            "core_claim": "The simulator answers whether named ordinary repair facts would close the gate, without claiming the repair has been executed.",
            "subchecks": [x["name"] for x in subchecks],
            "simulation_statuses": [x.value for x in SimulationStatus],
        },
        "dependencies": [x["name"] for x in subchecks],
    }


CHECKS = {
    "check_T_ordinary_repair_simulates_to_P_P": check_T_ordinary_repair_simulates_to_P_P,
    "check_T_provenance_and_structural_refuse_autopatch_P": check_T_provenance_and_structural_refuse_autopatch_P,
    "check_T_exact_case_no_patch_P": check_T_exact_case_no_patch_P,
    "check_T_patch_semantics_are_counterfactual_P": check_T_patch_semantics_are_counterfactual_P,
    "check_T_interface_repair_closure_simulator_P": check_T_interface_repair_closure_simulator_P,
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
            raise TypeError("Unsupported registry type for interface_repair_closure_simulator.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
