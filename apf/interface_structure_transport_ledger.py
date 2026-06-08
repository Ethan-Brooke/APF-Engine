"""
APF Interface Structure Transport Ledger.

v24.3.12 delta layer.

Purpose
-------
Generalize the trace-specific transport ledger into a typed ledger for every structure
that moves at an APF interface.

This module does not replace existing v24.3.12 modules:
    - trace_transport_ledger.py
    - trace_transport_routes.py
    - trace_transport_composition.py
    - trace_transport_completion.py
    - codomain_transport_schema.py
    - subspace_functors.py
    - interface_solver_descent_bridge.py

It sits above them as an inventory/typing layer:

    interface/solver metadata
      -> typed moving-structure ledger
      -> InterfaceSolverProblem
      -> InterfaceSolverCertificate

Core result:
    Every certifiable interface solver result can be decomposed into typed moving structures
    before obstruction/promotion certification.

Top check:
    check_T_interface_structure_transport_ledger_P
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, Iterable, Mapping, Optional, Tuple, List, Any

try:
    from apf.interface_solver_descent_bridge import (
        InterfaceSolverProblem,
        InterfaceSolverCertificate,
        solve_interface_descent,
        certificate_data,
    )
except Exception as exc:  # pragma: no cover
    raise ImportError(f"interface_structure_transport_ledger requires v24.3.12 descent bridge: {exc}") from exc


class StructureKind(str, Enum):
    ACC_RECORD = "ACC_RECORD"
    TRACE_INPUT = "TRACE_INPUT"
    SCHEME_CONTRACT = "SCHEME_CONTRACT"
    CAPACITY_COST = "CAPACITY_COST"
    CODOMAIN_TRANSPORT = "CODOMAIN_TRANSPORT"
    EVALUATOR_MAP = "EVALUATOR_MAP"
    OVERLAP_GLUING = "OVERLAP_GLUING"
    PROVENANCE = "PROVENANCE"
    FIBER_ACTION = "FIBER_ACTION"
    SUBSTRATE_BOUNDARY = "SUBSTRATE_BOUNDARY"
    EMPIRICAL_POSTERIOR = "EMPIRICAL_POSTERIOR"
    EXTERNAL_CONSTANT = "EXTERNAL_CONSTANT"
    COUNTERTERM = "COUNTERTERM"
    UNCERTAINTY_PROTOCOL = "UNCERTAINTY_PROTOCOL"


class StructureStatus(str, Enum):
    PRESENT_STABLE = "PRESENT_STABLE"
    MOVES_CLEANLY = "MOVES_CLEANLY"
    MISSING = "MISSING"
    BLOCKED_STRUCTURAL = "BLOCKED_STRUCTURAL"
    FAIL_CLOSED_PROVENANCE = "FAIL_CLOSED_PROVENANCE"


@dataclass(frozen=True)
class InterfaceStructureItem:
    name: str
    kind: StructureKind
    source: str
    target: str
    required: bool
    status: StructureStatus
    obstruction_hint: Tuple[str, ...] = tuple()
    notes: str = ""

    @property
    def present(self) -> bool:
        return self.status in {StructureStatus.PRESENT_STABLE, StructureStatus.MOVES_CLEANLY}

    @property
    def missing(self) -> bool:
        return self.required and self.status == StructureStatus.MISSING

    @property
    def blocked(self) -> bool:
        return self.required and self.status == StructureStatus.BLOCKED_STRUCTURAL

    @property
    def provenance_fail(self) -> bool:
        return self.status == StructureStatus.FAIL_CLOSED_PROVENANCE


@dataclass(frozen=True)
class InterfaceStructureTransportLedger:
    name: str
    sector: str
    items: Tuple[InterfaceStructureItem, ...]
    global_export_requested: bool = True
    local_solution_found: bool = True
    notes: str = ""

    def by_kind(self, kind: StructureKind) -> Tuple[InterfaceStructureItem, ...]:
        return tuple(item for item in self.items if item.kind == kind)

    def missing_required(self) -> Tuple[InterfaceStructureItem, ...]:
        return tuple(item for item in self.items if item.missing)

    def blocked_required(self) -> Tuple[InterfaceStructureItem, ...]:
        return tuple(item for item in self.items if item.blocked)

    def provenance_failures(self) -> Tuple[InterfaceStructureItem, ...]:
        return tuple(item for item in self.items if item.provenance_fail)

    def kind_status_summary(self) -> Dict[str, Dict[str, int]]:
        out: Dict[str, Dict[str, int]] = {}
        for item in self.items:
            bucket = out.setdefault(item.kind.value, {})
            bucket[item.status.value] = bucket.get(item.status.value, 0) + 1
        return out


def _required_kind_present(ledger: InterfaceStructureTransportLedger, kind: StructureKind) -> bool:
    items = ledger.by_kind(kind)
    required = tuple(item for item in items if item.required)
    if not required:
        return True
    return all(item.present for item in required)


def _required_kind_clean_or_absent(ledger: InterfaceStructureTransportLedger, kind: StructureKind) -> bool:
    return _required_kind_present(ledger, kind)


def ledger_to_interface_problem(ledger: InterfaceStructureTransportLedger) -> InterfaceSolverProblem:
    """Translate typed moving-structure inventory into the v24.3.12 solver certification contract."""
    has_acc = _required_kind_clean_or_absent(ledger, StructureKind.ACC_RECORD)

    evaluator_ok = all([
        _required_kind_clean_or_absent(ledger, StructureKind.EVALUATOR_MAP),
        _required_kind_clean_or_absent(ledger, StructureKind.SCHEME_CONTRACT),
        _required_kind_clean_or_absent(ledger, StructureKind.EXTERNAL_CONSTANT),
        _required_kind_clean_or_absent(ledger, StructureKind.COUNTERTERM),
        _required_kind_clean_or_absent(ledger, StructureKind.UNCERTAINTY_PROTOCOL),
    ])

    codomain_ok = _required_kind_clean_or_absent(ledger, StructureKind.CODOMAIN_TRANSPORT)
    overlap_ok = _required_kind_clean_or_absent(ledger, StructureKind.OVERLAP_GLUING)
    capacity_ok = _required_kind_clean_or_absent(ledger, StructureKind.CAPACITY_COST)
    empirical_ok = _required_kind_clean_or_absent(ledger, StructureKind.EMPIRICAL_POSTERIOR)

    target_smuggled = bool(ledger.provenance_failures())

    requires_polarity = any(
        item.required and item.blocked and "POLARITY_MISSING" in item.obstruction_hint
        for item in ledger.items
    )
    requires_reversal = any(
        item.required and item.blocked and "REVERSAL_MISSING" in item.obstruction_hint
        for item in ledger.items
    )
    requires_complex = any(
        item.required and item.blocked and "COMPLEX_ACTION_MISSING" in item.obstruction_hint
        for item in ledger.items
    )
    requires_norm = any(
        item.required and item.blocked and "NORM_MISSING" in item.obstruction_hint
        for item in ledger.items
    )

    return InterfaceSolverProblem(
        name=ledger.name,
        sector=ledger.sector,
        local_solution_found=ledger.local_solution_found,
        global_export_requested=ledger.global_export_requested,
        acc_base_present=has_acc,
        evaluator_map_found=evaluator_ok,
        codomain_transport_found=codomain_ok,
        overlap_gluing_verified=overlap_ok,
        capacity_budget_verified=capacity_ok,
        capacity_overspend_detected=not capacity_ok,
        empirical_or_posterior_closed=empirical_ok,
        target_value_used_as_input=target_smuggled,
        requires_substrate_polarity=requires_polarity,
        requires_substrate_reversal=requires_reversal,
        requires_complex_action=requires_complex,
        requires_operator_norm=requires_norm,
        route_notes=ledger.notes,
    )


@dataclass(frozen=True)
class LedgerCertificate:
    ledger: InterfaceStructureTransportLedger
    solver_certificate: InterfaceSolverCertificate

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ledger": {
                "name": self.ledger.name,
                "sector": self.ledger.sector,
                "global_export_requested": self.ledger.global_export_requested,
                "local_solution_found": self.ledger.local_solution_found,
                "kind_status_summary": self.ledger.kind_status_summary(),
                "missing_required": [asdict(item) for item in self.ledger.missing_required()],
                "blocked_required": [asdict(item) for item in self.ledger.blocked_required()],
                "provenance_failures": [asdict(item) for item in self.ledger.provenance_failures()],
                "items": [asdict(item) for item in self.ledger.items],
                "notes": self.ledger.notes,
            },
            "certificate": certificate_data(self.solver_certificate),
        }


def certify_ledger(ledger: InterfaceStructureTransportLedger) -> LedgerCertificate:
    return LedgerCertificate(
        ledger=ledger,
        solver_certificate=solve_interface_descent(ledger_to_interface_problem(ledger)),
    )


def item(
    name: str,
    kind: StructureKind,
    source: str,
    target: str,
    required: bool,
    ok: bool,
    *,
    obstruction_hint: Iterable[str] = tuple(),
    notes: str = "",
    status_if_missing: StructureStatus = StructureStatus.MISSING,
) -> InterfaceStructureItem:
    return InterfaceStructureItem(
        name=name,
        kind=kind,
        source=source,
        target=target,
        required=required,
        status=StructureStatus.MOVES_CLEANLY if ok else status_if_missing,
        obstruction_hint=tuple(obstruction_hint),
        notes=notes,
    )


def ew_trace_scheme_ledger(
    *,
    name: str,
    trace_sector_closed: bool,
    source_to_scheme_registry_present: bool,
    evaluator_map_found: bool,
    codomain_transport_found: bool,
    counterterm_finite_parts_declared: bool,
    external_constants_ledger_clean: bool,
    uncertainty_protocol_declared: bool,
    target_value_consumed: bool,
) -> InterfaceStructureTransportLedger:
    items = (
        item("ACC base record", StructureKind.ACC_RECORD, "APF interface", "APF interface", True, True),
        item("immutable APF_TRACE input", StructureKind.TRACE_INPUT, "APF_TRACE", "transport ledger", True, trace_sector_closed),
        item("target-scheme contract", StructureKind.SCHEME_CONTRACT, "APF_TRACE", "physical scheme S(mu)", True, source_to_scheme_registry_present, obstruction_hint=("EVALUATOR_MISSING",)),
        item("codomain transport", StructureKind.CODOMAIN_TRANSPORT, "APF_TRACE", "physical scheme S(mu)", True, codomain_transport_found, obstruction_hint=("CODOMAIN_MISMATCH",)),
        item("scheme evaluator map", StructureKind.EVALUATOR_MAP, "trace route", "physical export evaluator", True, evaluator_map_found, obstruction_hint=("EVALUATOR_MISSING",)),
        item("external constants ledger", StructureKind.EXTERNAL_CONSTANT, "external constants", "transport evaluator", True, external_constants_ledger_clean, obstruction_hint=("EVALUATOR_MISSING",)),
        item("counterterm finite parts", StructureKind.COUNTERTERM, "counterterm slots", "scheme evaluator", True, counterterm_finite_parts_declared, obstruction_hint=("EVALUATOR_MISSING",)),
        item("uncertainty/comparison protocol", StructureKind.UNCERTAINTY_PROTOCOL, "transport output", "comparison claim", True, uncertainty_protocol_declared, obstruction_hint=("EVALUATOR_MISSING",)),
        InterfaceStructureItem(
            "no target physical mass as inverse input",
            StructureKind.PROVENANCE,
            "physical target",
            "transport input",
            True,
            StructureStatus.FAIL_CLOSED_PROVENANCE if target_value_consumed else StructureStatus.PRESENT_STABLE,
            ("PROVENANCE_SMUGGLE",),
            "Fail closed if target physical mass is used as an inverse input.",
        ),
    )
    return InterfaceStructureTransportLedger(
        name=name,
        sector="EW",
        items=items,
        local_solution_found=trace_sector_closed,
        notes="EW trace-to-scheme structure transport ledger; generalizes trace_transport_ledger.py architecture.",
    )


def dark_posterior_ledger(
    *,
    name: str,
    route_built: bool,
    run_completed: bool,
    posterior_closed: bool,
    robustness_checks_passed: bool,
    target_value_consumed: bool,
) -> InterfaceStructureTransportLedger:
    local = route_built and run_completed
    items = (
        item("ACC base record", StructureKind.ACC_RECORD, "APF interface", "APF interface", True, True),
        item("dark empirical evaluator", StructureKind.EVALUATOR_MAP, "dark route", "posterior evaluator", True, posterior_closed and robustness_checks_passed, obstruction_hint=("EVALUATOR_MISSING",)),
        item("posterior/robustness closure", StructureKind.EMPIRICAL_POSTERIOR, "run output", "empirical claim", True, posterior_closed and robustness_checks_passed, obstruction_hint=("EVALUATOR_MISSING",)),
        item("codomain transport", StructureKind.CODOMAIN_TRANSPORT, "model output", "empirical claim", True, True),
        InterfaceStructureItem("no posterior output as input", StructureKind.PROVENANCE, "posterior", "route input", True, StructureStatus.FAIL_CLOSED_PROVENANCE if target_value_consumed else StructureStatus.PRESENT_STABLE, ("PROVENANCE_SMUGGLE",)),
    )
    return InterfaceStructureTransportLedger(name=name, sector="DARK", items=items, local_solution_found=local, notes="Dark-sector posterior structure ledger.")


def gauge_fiber_ledger(
    *,
    name: str,
    local_fiber_action_defined: bool,
    codomain_map_declared: bool,
    overlap_cocycle_verified: bool,
    anomaly_check_passed: bool,
    target_value_consumed: bool = False,
) -> InterfaceStructureTransportLedger:
    items = (
        item("ACC base record", StructureKind.ACC_RECORD, "APF interface", "APF interface", True, True),
        item("fiber action", StructureKind.FIBER_ACTION, "fiber", "fiber automorphism", True, local_fiber_action_defined, obstruction_hint=("EVALUATOR_MISSING",)),
        item("gauge codomain map", StructureKind.CODOMAIN_TRANSPORT, "fiber action", "gauge codomain", True, codomain_map_declared, obstruction_hint=("CODOMAIN_MISMATCH",)),
        item("overlap cocycle", StructureKind.OVERLAP_GLUING, "local patches", "global gauge object", True, overlap_cocycle_verified, obstruction_hint=("OVERLAP_INCOHERENCE",)),
        item("anomaly/evaluator check", StructureKind.EVALUATOR_MAP, "gauge route", "export evaluator", True, anomaly_check_passed, obstruction_hint=("EVALUATOR_MISSING",)),
        InterfaceStructureItem("no target gauge structure as input", StructureKind.PROVENANCE, "target", "input", True, StructureStatus.FAIL_CLOSED_PROVENANCE if target_value_consumed else StructureStatus.PRESENT_STABLE, ("PROVENANCE_SMUGGLE",)),
    )
    return InterfaceStructureTransportLedger(name=name, sector="GAUGE", items=items, local_solution_found=local_fiber_action_defined, notes="Gauge-as-fiber-automorphism structure ledger.")


def horizon_fiber_cost_ledger(
    *,
    name: str,
    horizon_partition_defined: bool,
    area_cost_map_defined: bool,
    overlap_gluing_verified: bool,
    capacity_bound_checked: bool,
    target_value_consumed: bool = False,
) -> InterfaceStructureTransportLedger:
    local = horizon_partition_defined and area_cost_map_defined
    items = (
        item("ACC base record", StructureKind.ACC_RECORD, "APF interface", "APF interface", True, True),
        item("horizon area cost map", StructureKind.CAPACITY_COST, "horizon partition", "capacity ledger", True, capacity_bound_checked, obstruction_hint=("CAPACITY_OVERSPEND",)),
        item("area-cost evaluator", StructureKind.EVALUATOR_MAP, "horizon map", "export evaluator", True, area_cost_map_defined, obstruction_hint=("EVALUATOR_MISSING",)),
        item("horizon overlap gluing", StructureKind.OVERLAP_GLUING, "horizon patches", "global horizon object", True, overlap_gluing_verified, obstruction_hint=("OVERLAP_INCOHERENCE",)),
        item("codomain transport", StructureKind.CODOMAIN_TRANSPORT, "area/cost ledger", "horizon claim", True, True),
        InterfaceStructureItem("no target horizon output as input", StructureKind.PROVENANCE, "target", "input", True, StructureStatus.FAIL_CLOSED_PROVENANCE if target_value_consumed else StructureStatus.PRESENT_STABLE, ("PROVENANCE_SMUGGLE",)),
    )
    return InterfaceStructureTransportLedger(name=name, sector="HORIZON", items=items, local_solution_found=local, notes="Horizon-area-as-fiber-cost structure ledger.")


def substrate_cstar_attempt_ledger(name: str = "flat_Cstar_substrate_attempt") -> InterfaceStructureTransportLedger:
    items = (
        item("ACC base record", StructureKind.ACC_RECORD, "APF interface", "APF interface", True, True),
        item("complex scalar action at substrate", StructureKind.SUBSTRATE_BOUNDARY, "substrate", "C* carrier", True, False, obstruction_hint=("COMPLEX_ACTION_MISSING",), status_if_missing=StructureStatus.BLOCKED_STRUCTURAL),
        item("cost-preserving reversal at substrate", StructureKind.SUBSTRATE_BOUNDARY, "substrate", "C* involution", True, False, obstruction_hint=("REVERSAL_MISSING",), status_if_missing=StructureStatus.BLOCKED_STRUCTURAL),
        item("operator/C*-norm at substrate", StructureKind.SUBSTRATE_BOUNDARY, "substrate", "C* norm", True, False, obstruction_hint=("NORM_MISSING",), status_if_missing=StructureStatus.BLOCKED_STRUCTURAL),
        item("C* codomain declaration", StructureKind.CODOMAIN_TRANSPORT, "substrate", "C* codomain", True, False, obstruction_hint=("CODOMAIN_MISMATCH",)),
    )
    return InterfaceStructureTransportLedger(name=name, sector="CSTAR", items=items, local_solution_found=True, notes="Flat substrate-global C* attempt structure ledger.")


def canonical_ledgers() -> Dict[str, InterfaceStructureTransportLedger]:
    return {
        "EW_open": ew_trace_scheme_ledger(
            name="ledger_EW_open_transport",
            trace_sector_closed=True,
            source_to_scheme_registry_present=True,
            evaluator_map_found=False,
            codomain_transport_found=False,
            counterterm_finite_parts_declared=False,
            external_constants_ledger_clean=True,
            uncertainty_protocol_declared=False,
            target_value_consumed=False,
        ),
        "EW_closed": ew_trace_scheme_ledger(
            name="ledger_EW_closed_clean",
            trace_sector_closed=True,
            source_to_scheme_registry_present=True,
            evaluator_map_found=True,
            codomain_transport_found=True,
            counterterm_finite_parts_declared=True,
            external_constants_ledger_clean=True,
            uncertainty_protocol_declared=True,
            target_value_consumed=False,
        ),
        "EW_smuggled": ew_trace_scheme_ledger(
            name="ledger_EW_smuggled",
            trace_sector_closed=True,
            source_to_scheme_registry_present=True,
            evaluator_map_found=True,
            codomain_transport_found=True,
            counterterm_finite_parts_declared=True,
            external_constants_ledger_clean=True,
            uncertainty_protocol_declared=True,
            target_value_consumed=True,
        ),
        "dark_open": dark_posterior_ledger(
            name="ledger_dark_open",
            route_built=True,
            run_completed=True,
            posterior_closed=False,
            robustness_checks_passed=False,
            target_value_consumed=False,
        ),
        "gauge_codomain_open": gauge_fiber_ledger(
            name="ledger_gauge_codomain_open",
            local_fiber_action_defined=True,
            codomain_map_declared=False,
            overlap_cocycle_verified=True,
            anomaly_check_passed=True,
        ),
        "horizon_overlap_open": horizon_fiber_cost_ledger(
            name="ledger_horizon_overlap_open",
            horizon_partition_defined=True,
            area_cost_map_defined=True,
            overlap_gluing_verified=False,
            capacity_bound_checked=True,
        ),
        "flat_Cstar": substrate_cstar_attempt_ledger(),
    }


def run_canonical_ledgers() -> Dict[str, Dict[str, Any]]:
    return {name: certify_ledger(ledger).to_dict() for name, ledger in canonical_ledgers().items()}


def check_T_structure_kind_inventory_P() -> Dict[str, Any]:
    kinds = {kind.value for kind in StructureKind}
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
        "all_required_kinds_present": required.issubset(kinds),
        "kind_count_at_least_14": len(kinds) >= 14,
    }
    return {
        "name": "check_T_structure_kind_inventory_P",
        "consistent": all(tests.values()),
        "status": "P_ledger" if all(tests.values()) else "FAIL",
        "summary": "Interface structure kind inventory covers trace, scheme, capacity, codomain, evaluator, gluing, provenance, fiber, substrate, empirical, constants, counterterms, and uncertainty protocol.",
        "data": {"tests": tests, "kinds": sorted(kinds)},
    }


def check_T_trace_transport_ledger_generalization_P() -> Dict[str, Any]:
    ledger = canonical_ledgers()["EW_open"]
    kinds = {item.kind.value for item in ledger.items}
    result = certify_ledger(ledger).to_dict()
    tests = {
        "has_trace_input": "TRACE_INPUT" in kinds,
        "has_scheme_contract": "SCHEME_CONTRACT" in kinds,
        "has_external_constant": "EXTERNAL_CONSTANT" in kinds,
        "has_counterterm": "COUNTERTERM" in kinds,
        "has_uncertainty_protocol": "UNCERTAINTY_PROTOCOL" in kinds,
        "has_no_smuggling_provenance": "PROVENANCE" in kinds,
        "held_for_repair": result["certificate"]["solver_status"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "not_global_export": result["certificate"]["export_global_P"] is False,
    }
    return {
        "name": "check_T_trace_transport_ledger_generalization_P",
        "consistent": all(tests.values()),
        "status": "P_ledger" if all(tests.values()) else "FAIL",
        "summary": "EW trace transport ledger architecture is represented as an instance of the general interface structure ledger.",
        "data": {"tests": tests, "ledger_summary": result["ledger"]["kind_status_summary"], "certificate": result["certificate"]},
        "dependencies": ["check_T_structure_kind_inventory_P"],
    }


def check_T_ledger_to_solver_certificate_P() -> Dict[str, Any]:
    results = run_canonical_ledgers()
    tests = {
        "EW_open_held": results["EW_open"]["certificate"]["solver_status"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "EW_open_has_evaluator": "EVALUATOR_MISSING" in results["EW_open"]["certificate"]["obstruction"],
        "EW_open_has_codomain": "CODOMAIN_MISMATCH" in results["EW_open"]["certificate"]["obstruction"],
        "EW_closed_exports": results["EW_closed"]["certificate"]["solver_status"] == "SOLVED_GLOBAL_P",
        "EW_smuggled_fails_closed": results["EW_smuggled"]["certificate"]["solver_status"] == "FAIL_CLOSED_PROVENANCE",
        "dark_open_held": results["dark_open"]["certificate"]["solver_status"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "gauge_open_held": results["gauge_codomain_open"]["certificate"]["solver_status"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "horizon_open_held": results["horizon_overlap_open"]["certificate"]["solver_status"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "Cstar_revision_blocked": results["flat_Cstar"]["certificate"]["solver_status"] == "BLOCKED_SUBSTRATE_REVISION_REQUIRED",
    }
    return {
        "name": "check_T_ledger_to_solver_certificate_P",
        "consistent": all(tests.values()),
        "status": "P_ledger" if all(tests.values()) else "FAIL",
        "summary": "Typed structure ledgers translate into v24.3.12 interface-solver certificates with expected statuses.",
        "data": {"tests": tests, "results": results},
        "dependencies": ["check_T_trace_transport_ledger_generalization_P"],
    }


def check_T_every_certificate_has_pre_obstruction_inventory_P() -> Dict[str, Any]:
    results = run_canonical_ledgers()
    tests = {
        name: (
            len(result["ledger"]["items"]) > 0
            and "kind_status_summary" in result["ledger"]
            and "certificate" in result
            and "solver_status" in result["certificate"]
        )
        for name, result in results.items()
    }
    return {
        "name": "check_T_every_certificate_has_pre_obstruction_inventory_P",
        "consistent": all(tests.values()),
        "status": "P_ledger" if all(tests.values()) else "FAIL",
        "summary": "Every canonical solver certificate is preceded by a typed inventory of moving structures.",
        "data": {"tests": tests},
        "dependencies": ["check_T_ledger_to_solver_certificate_P"],
    }


def check_T_interface_structure_transport_ledger_P() -> Dict[str, Any]:
    subchecks = [
        check_T_structure_kind_inventory_P(),
        check_T_trace_transport_ledger_generalization_P(),
        check_T_ledger_to_solver_certificate_P(),
        check_T_every_certificate_has_pre_obstruction_inventory_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_interface_structure_transport_ledger_P",
        "consistent": ok,
        "status": "P_interface_ledger" if ok else "FAIL",
        "summary": "Interface Structure Transport Ledger is P: it inventories moving structures before obstruction/promotion certification and generalizes the trace transport ledger architecture.",
        "data": {
            "core_claim": "Every certifiable interface solver output decomposes into typed moving structures before obstruction certification.",
            "subchecks": [x["name"] for x in subchecks],
            "structure_kinds": [kind.value for kind in StructureKind],
        },
        "dependencies": [x["name"] for x in subchecks],
    }


CHECKS = {
    "check_T_structure_kind_inventory_P": check_T_structure_kind_inventory_P,
    "check_T_trace_transport_ledger_generalization_P": check_T_trace_transport_ledger_generalization_P,
    "check_T_ledger_to_solver_certificate_P": check_T_ledger_to_solver_certificate_P,
    "check_T_every_certificate_has_pre_obstruction_inventory_P": check_T_every_certificate_has_pre_obstruction_inventory_P,
    "check_T_interface_structure_transport_ledger_P": check_T_interface_structure_transport_ledger_P,
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
            raise TypeError("Unsupported registry type for interface_structure_transport_ledger.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
