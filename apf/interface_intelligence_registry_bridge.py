
"""
APF Interface Intelligence Registry Bridge.

Bank/verify_all readiness layer for the interface-intelligence stack.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Callable, Dict, Iterable, Mapping, Optional, Tuple
import importlib


class RegistryBridgeStatus(str, Enum):
    READY = "READY"
    IMPORT_MISSING = "IMPORT_MISSING"
    CHECK_MISSING = "CHECK_MISSING"


@dataclass(frozen=True)
class TopCheckSpec:
    module_name: str
    function_name: str
    expected_status: str
    tier: str
    purpose: str

    @property
    def check_key(self) -> str:
        return f"{self.module_name}:{self.function_name}"

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["check_key"] = self.check_key
        return d


@dataclass(frozen=True)
class TopCheckProbe:
    spec: TopCheckSpec
    import_ok: bool
    function_present: bool
    status: RegistryBridgeStatus
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "spec": self.spec.to_dict(),
            "import_ok": self.import_ok,
            "function_present": self.function_present,
            "status": self.status.value,
            "error": self.error,
        }


@dataclass(frozen=True)
class RegistryBridgeReport:
    specs: Tuple[TopCheckSpec, ...]
    probes: Tuple[TopCheckProbe, ...]
    registration_count: int
    generated_bank_stub: str
    generated_verify_all_snippet: str
    ready: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "specs": [s.to_dict() for s in self.specs],
            "probes": [p.to_dict() for p in self.probes],
            "registration_count": self.registration_count,
            "generated_bank_stub": self.generated_bank_stub,
            "generated_verify_all_snippet": self.generated_verify_all_snippet,
            "ready": self.ready,
        }


INTERFACE_INTELLIGENCE_TOP_CHECKS: Tuple[TopCheckSpec, ...] = (
    TopCheckSpec("apf.route_certification_starter_suite", "check_T_route_certification_starter_suite_P", "P_route_suite", "interface", "Route-specific certifier suite."),
    TopCheckSpec("apf.route_certification_workbench", "check_T_route_workbench_payload_certification_P", "P_workbench", "interface", "Route payload workbench."),
    TopCheckSpec("apf.interface_structure_transport_ledger", "check_T_interface_structure_transport_ledger_P", "P_interface_ledger", "interface", "Typed interface-structure ledger."),
    TopCheckSpec("apf.interface_structure_discovery_engine", "check_T_interface_structure_discovery_engine_P", "P_discovery_engine", "interface", "Structure discovery engine."),
    TopCheckSpec("apf.interface_structure_movement_graph", "check_T_interface_structure_movement_graph_P", "P_movement_graph", "interface", "Movement graph and obstruction paths."),
    TopCheckSpec("apf.interface_movement_graph_repair_planner", "check_T_interface_movement_graph_repair_planner_P", "P_repair_planner", "interface", "Repair planner."),
    TopCheckSpec("apf.interface_repair_closure_simulator", "check_T_interface_repair_closure_simulator_P", "P_closure_sim", "interface", "Counterfactual closure simulator."),
    TopCheckSpec("apf.interface_repair_frontier_explorer", "check_T_interface_repair_frontier_explorer_P", "P_frontier_explorer", "interface", "Minimal repair frontier explorer."),
    TopCheckSpec("apf.interface_repair_obligation_compiler", "check_T_interface_repair_obligation_compiler_P", "P_obligation_compiler", "interface", "Evidence obligation compiler."),
    TopCheckSpec("apf.interface_evidence_rerun_controller", "check_T_interface_evidence_rerun_controller_P", "P_evidence_rerun", "interface", "Evidence rerun controller."),
    TopCheckSpec("apf.ew_trace_to_scheme_real_adapter", "check_T_EW_trace_to_scheme_real_adapter_P", "P_real_adapter", "adapter", "EW trace-to-scheme real adapter."),
    TopCheckSpec("apf.dark_posterior_real_adapter", "check_T_dark_posterior_real_adapter_P", "P_real_adapter", "adapter", "Dark posterior real adapter."),
    TopCheckSpec("apf.claim_to_interface_graph_compiler", "check_T_claim_to_interface_graph_compiler_P", "P_claim_compiler", "claim", "Claim-to-interface compiler."),
    TopCheckSpec("apf.interface_atlas", "check_T_interface_atlas_P", "P_interface_atlas", "atlas", "Interface atlas."),
    TopCheckSpec("apf.interface_intelligence_CI_orchestrator", "check_T_interface_intelligence_CI_orchestrator_P", "P_CI_orchestrator", "ci", "Full CI orchestrator."),
)


def probe_top_check(spec: TopCheckSpec) -> TopCheckProbe:
    try:
        module = importlib.import_module(spec.module_name)
    except Exception as exc:
        return TopCheckProbe(spec, False, False, RegistryBridgeStatus.IMPORT_MISSING, repr(exc))
    if not hasattr(module, spec.function_name):
        return TopCheckProbe(spec, True, False, RegistryBridgeStatus.CHECK_MISSING, f"missing {spec.function_name}")
    return TopCheckProbe(spec, True, True, RegistryBridgeStatus.READY, None)


def probe_all_top_checks() -> Tuple[TopCheckProbe, ...]:
    return tuple(probe_top_check(spec) for spec in INTERFACE_INTELLIGENCE_TOP_CHECKS)


def import_top_check(spec: TopCheckSpec) -> Callable[[], Mapping[str, Any]]:
    module = importlib.import_module(spec.module_name)
    return getattr(module, spec.function_name)


def top_check_callables() -> Dict[str, Callable[[], Mapping[str, Any]]]:
    return {spec.function_name: import_top_check(spec) for spec in INTERFACE_INTELLIGENCE_TOP_CHECKS}


def register_interface_intelligence_checks(registry: Any) -> Any:
    callables = top_check_callables()
    if hasattr(registry, "update"):
        registry.update(callables)
        return registry
    if hasattr(registry, "register"):
        for name, fn in callables.items():
            registry.register(name, fn)
        return registry
    if hasattr(registry, "add"):
        for name, fn in callables.items():
            registry.add(name, fn)
        return registry
    raise TypeError("Unsupported registry object: expected update(), register(), or add().")


def run_registered_interface_intelligence_checks() -> Dict[str, Mapping[str, Any]]:
    return {name: fn() for name, fn in top_check_callables().items()}


def generate_bank_stub() -> str:
    specs_literal = "\n".join(
        f"    ('{spec.module_name}', '{spec.function_name}'),"
        for spec in INTERFACE_INTELLIGENCE_TOP_CHECKS
    )
    return (
        '"""\\n'
        'Interface Intelligence bank registration stub.\\n'
        'Generated by apf.interface_intelligence_registry_bridge.\\n'
        '"""\\n\\n'
        'from importlib import import_module\\n\\n'
        'INTERFACE_INTELLIGENCE_TOP_CHECKS = (\\n'
        + specs_literal +
        '\\n)\\n\\n'
        'def register_interface_intelligence_checks(registry):\\n'
        '    for module_name, function_name in INTERFACE_INTELLIGENCE_TOP_CHECKS:\\n'
        '        module = import_module(module_name)\\n'
        '        fn = getattr(module, function_name)\\n'
        '        if hasattr(registry, "register"):\\n'
        '            registry.register(function_name, fn)\\n'
        '        elif hasattr(registry, "add"):\\n'
        '            registry.add(function_name, fn)\\n'
        '        elif hasattr(registry, "update"):\\n'
        '            registry.update({function_name: fn})\\n'
        '        else:\\n'
        '            raise TypeError("Unsupported registry object")\\n'
        '    return registry\\n'
    )


def generate_verify_all_snippet() -> str:
    names = "\n".join(f"        '{spec.function_name}'," for spec in INTERFACE_INTELLIGENCE_TOP_CHECKS)
    return (
        '# Interface Intelligence verify_all snippet\\n'
        '# Insert after APF bank registry is loaded.\\n\\n'
        'INTERFACE_INTELLIGENCE_EXPECTED_CHECKS = [\\n'
        + names +
        '\\n]\\n\\n'
        'def run_interface_intelligence_expected_checks(registry):\\n'
        '    results = {}\\n'
        '    for name in INTERFACE_INTELLIGENCE_EXPECTED_CHECKS:\\n'
        '        fn = registry[name] if isinstance(registry, dict) else getattr(registry, name)\\n'
        '        results[name] = fn()\\n'
        '    return results\\n\\n'
        'def assert_interface_intelligence_expected_checks_pass(registry):\\n'
        '    results = run_interface_intelligence_expected_checks(registry)\\n'
        '    failures = {\\n'
        '        name: result for name, result in results.items()\\n'
        '        if not result.get("consistent") or str(result.get("status", "")).startswith("FAIL")\\n'
        '    }\\n'
        '    if failures:\\n'
        '        raise AssertionError(f"Interface Intelligence checks failed: {list(failures)}")\\n'
        '    return results\\n'
    )


def build_registry_bridge_report() -> RegistryBridgeReport:
    probes = probe_all_top_checks()
    ready = all(p.status == RegistryBridgeStatus.READY for p in probes)
    return RegistryBridgeReport(
        specs=INTERFACE_INTELLIGENCE_TOP_CHECKS,
        probes=probes,
        registration_count=len(INTERFACE_INTELLIGENCE_TOP_CHECKS),
        generated_bank_stub=generate_bank_stub(),
        generated_verify_all_snippet=generate_verify_all_snippet(),
        ready=ready,
    )


class FakeRegisterRegistry:
    def __init__(self):
        self.items: Dict[str, Callable] = {}
    def register(self, name: str, fn: Callable) -> None:
        self.items[name] = fn


class FakeAddRegistry:
    def __init__(self):
        self.items: Dict[str, Callable] = {}
    def add(self, name: str, fn: Callable) -> None:
        self.items[name] = fn


def check_T_registry_bridge_manifest_complete_P() -> Dict[str, Any]:
    specs = INTERFACE_INTELLIGENCE_TOP_CHECKS
    names = [s.function_name for s in specs]
    tests = {
        "count_15": len(specs) == 15,
        "unique_names": len(names) == len(set(names)),
        "has_CI_orchestrator": "check_T_interface_intelligence_CI_orchestrator_P" in names,
        "has_atlas": "check_T_interface_atlas_P" in names,
        "has_real_adapters": "check_T_EW_trace_to_scheme_real_adapter_P" in names and "check_T_dark_posterior_real_adapter_P" in names,
    }
    return {
        "name": "check_T_registry_bridge_manifest_complete_P",
        "consistent": all(tests.values()),
        "status": "P_registry_bridge" if all(tests.values()) else "FAIL",
        "summary": "Registry bridge manifest covers all interface-intelligence top checks.",
        "data": {"tests": tests, "check_names": names},
    }


def check_T_registry_bridge_imports_ready_P() -> Dict[str, Any]:
    report = build_registry_bridge_report()
    tests = {
        "all_imports_ready": all(p.import_ok for p in report.probes),
        "all_functions_present": all(p.function_present for p in report.probes),
        "report_ready": report.ready is True,
        "registration_count_15": report.registration_count == 15,
    }
    return {
        "name": "check_T_registry_bridge_imports_ready_P",
        "consistent": all(tests.values()),
        "status": "P_registry_bridge" if all(tests.values()) else "FAIL",
        "summary": "Registry bridge can import every interface-intelligence top check.",
        "data": {"tests": tests, "probe_statuses": [p.to_dict() for p in report.probes]},
        "dependencies": ["check_T_registry_bridge_manifest_complete_P"],
    }


def check_T_registry_bridge_registers_dict_P() -> Dict[str, Any]:
    registry: Dict[str, Callable] = {}
    register_interface_intelligence_checks(registry)
    tests = {
        "registered_15": len(registry) == 15,
        "all_callable": all(callable(v) for v in registry.values()),
        "CI_registered": "check_T_interface_intelligence_CI_orchestrator_P" in registry,
    }
    return {
        "name": "check_T_registry_bridge_registers_dict_P",
        "consistent": all(tests.values()),
        "status": "P_registry_bridge" if all(tests.values()) else "FAIL",
        "summary": "Registry bridge registers checks into dict/update registries.",
        "data": {"tests": tests, "registered_names": sorted(registry)},
        "dependencies": ["check_T_registry_bridge_imports_ready_P"],
    }


def check_T_registry_bridge_registers_object_P() -> Dict[str, Any]:
    reg1 = FakeRegisterRegistry()
    reg2 = FakeAddRegistry()
    register_interface_intelligence_checks(reg1)
    register_interface_intelligence_checks(reg2)
    tests = {
        "register_method_15": len(reg1.items) == 15,
        "add_method_15": len(reg2.items) == 15,
        "all_callable_register": all(callable(v) for v in reg1.items.values()),
        "all_callable_add": all(callable(v) for v in reg2.items.values()),
    }
    return {
        "name": "check_T_registry_bridge_registers_object_P",
        "consistent": all(tests.values()),
        "status": "P_registry_bridge" if all(tests.values()) else "FAIL",
        "summary": "Registry bridge supports object registries exposing register() or add().",
        "data": {"tests": tests},
        "dependencies": ["check_T_registry_bridge_registers_dict_P"],
    }


def check_T_registry_bridge_generated_patches_P() -> Dict[str, Any]:
    report = build_registry_bridge_report()
    stub = report.generated_bank_stub
    snippet = report.generated_verify_all_snippet
    tests = {
        "stub_mentions_register": "register_interface_intelligence_checks" in stub,
        "stub_mentions_import_module": "import_module" in stub,
        "snippet_mentions_assert": "assert_interface_intelligence_expected_checks_pass" in snippet,
        "snippet_mentions_CI": "check_T_interface_intelligence_CI_orchestrator_P" in snippet,
        "all_check_names_in_stub": all(spec.function_name in stub for spec in INTERFACE_INTELLIGENCE_TOP_CHECKS),
    }
    return {
        "name": "check_T_registry_bridge_generated_patches_P",
        "consistent": all(tests.values()),
        "status": "P_registry_bridge" if all(tests.values()) else "FAIL",
        "summary": "Registry bridge generates bank-registration and verify_all integration snippets.",
        "data": {"tests": tests},
        "dependencies": ["check_T_registry_bridge_registers_object_P"],
    }


def check_T_interface_intelligence_registry_bridge_P() -> Dict[str, Any]:
    subchecks = [
        check_T_registry_bridge_manifest_complete_P(),
        check_T_registry_bridge_imports_ready_P(),
        check_T_registry_bridge_registers_dict_P(),
        check_T_registry_bridge_registers_object_P(),
        check_T_registry_bridge_generated_patches_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_interface_intelligence_registry_bridge_P",
        "consistent": ok,
        "status": "P_registry_bridge" if ok else "FAIL",
        "summary": "Interface Intelligence Registry Bridge is P: all top checks are manifest-defined, importable, registrable, and patch-emittable.",
        "data": {
            "core_claim": "The interface-intelligence stack is ready for live bank/verify_all registration without mutating the bank implicitly.",
            "subchecks": [x["name"] for x in subchecks],
            "registration_count": len(INTERFACE_INTELLIGENCE_TOP_CHECKS),
        },
        "dependencies": [x["name"] for x in subchecks],
    }


CHECKS = {
    "check_T_registry_bridge_manifest_complete_P": check_T_registry_bridge_manifest_complete_P,
    "check_T_registry_bridge_imports_ready_P": check_T_registry_bridge_imports_ready_P,
    "check_T_registry_bridge_registers_dict_P": check_T_registry_bridge_registers_dict_P,
    "check_T_registry_bridge_registers_object_P": check_T_registry_bridge_registers_object_P,
    "check_T_registry_bridge_generated_patches_P": check_T_registry_bridge_generated_patches_P,
    "check_T_interface_intelligence_registry_bridge_P": check_T_interface_intelligence_registry_bridge_P,
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
            raise TypeError("Unsupported registry type for interface_intelligence_registry_bridge.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
