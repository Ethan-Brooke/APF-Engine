"""
APF Interface Intelligence CI Orchestrator.

v24.3.12+ delta layer.

Purpose
-------
Run the interface-intelligence stack as one release/CI target:

    module checks
      -> top P markers/statuses
      -> optional EW/dark live adapter reports
      -> interface atlas report
      -> release gate summary

Boundary
--------
The orchestrator only reports whether interface-intelligence software checks pass and what
route adapters report. It does not turn held/repair routes into physics P.

Top check:
    check_T_interface_intelligence_CI_orchestrator_P
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List
import importlib
import json
import traceback
from datetime import datetime, timezone


class CIStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    IMPORT_FAIL = "IMPORT_FAIL"
    CHECK_FAIL = "CHECK_FAIL"
    SKIPPED = "SKIPPED"


@dataclass(frozen=True)
class ModuleCIResult:
    module_name: str
    top_check: str
    expected_status: str
    import_ok: bool
    check_ok: bool
    actual_status: Optional[str]
    consistent: Optional[bool]
    error: Optional[str]
    summary: Optional[str]

    @property
    def ci_status(self) -> CIStatus:
        if not self.import_ok:
            return CIStatus.IMPORT_FAIL
        if not self.check_ok:
            return CIStatus.CHECK_FAIL
        if self.actual_status == self.expected_status and self.consistent is True:
            return CIStatus.PASS
        return CIStatus.FAIL

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["ci_status"] = self.ci_status.value
        return data


@dataclass(frozen=True)
class InterfaceIntelligenceCIReport:
    created_utc: str
    module_results: Tuple[ModuleCIResult, ...]
    atlas_report: Optional[Mapping[str, Any]]
    ew_adapter_report: Optional[Mapping[str, Any]]
    dark_adapter_report: Optional[Mapping[str, Any]]
    release_gate_pass: bool
    release_gate_reason: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "created_utc": self.created_utc,
            "module_results": [r.to_dict() for r in self.module_results],
            "atlas_report": dict(self.atlas_report) if self.atlas_report is not None else None,
            "ew_adapter_report": dict(self.ew_adapter_report) if self.ew_adapter_report is not None else None,
            "dark_adapter_report": dict(self.dark_adapter_report) if self.dark_adapter_report is not None else None,
            "release_gate_pass": self.release_gate_pass,
            "release_gate_reason": self.release_gate_reason,
            "summary_counts": summary_counts(self.module_results),
        }


MODULE_TARGETS: Tuple[Tuple[str, str, str], ...] = (
    ("apf.route_certification_starter_suite", "check_T_route_certification_starter_suite_P", "P_route_suite"),
    ("apf.route_certification_workbench", "check_T_route_workbench_payload_certification_P", "P_workbench"),
    ("apf.interface_structure_transport_ledger", "check_T_interface_structure_transport_ledger_P", "P_interface_ledger"),
    ("apf.interface_structure_discovery_engine", "check_T_interface_structure_discovery_engine_P", "P_discovery_engine"),
    ("apf.interface_structure_movement_graph", "check_T_interface_structure_movement_graph_P", "P_movement_graph"),
    ("apf.interface_movement_graph_repair_planner", "check_T_interface_movement_graph_repair_planner_P", "P_repair_planner"),
    ("apf.interface_repair_closure_simulator", "check_T_interface_repair_closure_simulator_P", "P_closure_sim"),
    ("apf.interface_repair_frontier_explorer", "check_T_interface_repair_frontier_explorer_P", "P_frontier_explorer"),
    ("apf.interface_repair_obligation_compiler", "check_T_interface_repair_obligation_compiler_P", "P_obligation_compiler"),
    ("apf.interface_evidence_rerun_controller", "check_T_interface_evidence_rerun_controller_P", "P_evidence_rerun"),
    ("apf.ew_trace_to_scheme_real_adapter", "check_T_EW_trace_to_scheme_real_adapter_P", "P_real_adapter"),
    ("apf.dark_posterior_real_adapter", "check_T_dark_posterior_real_adapter_P", "P_real_adapter"),
    ("apf.claim_to_interface_graph_compiler", "check_T_claim_to_interface_graph_compiler_P", "P_claim_compiler"),
    ("apf.interface_atlas", "check_T_interface_atlas_P", "P_interface_atlas"),
)


def run_module_top_check(module_name: str, top_check: str, expected_status: str) -> ModuleCIResult:
    try:
        mod = importlib.import_module(module_name)
    except Exception as exc:
        return ModuleCIResult(
            module_name=module_name,
            top_check=top_check,
            expected_status=expected_status,
            import_ok=False,
            check_ok=False,
            actual_status=None,
            consistent=None,
            error=f"import failed: {exc!r}",
            summary=None,
        )

    try:
        if not hasattr(mod, top_check):
            raise AttributeError(f"missing top check {top_check}")
        result = getattr(mod, top_check)()
        return ModuleCIResult(
            module_name=module_name,
            top_check=top_check,
            expected_status=expected_status,
            import_ok=True,
            check_ok=True,
            actual_status=str(result.get("status")),
            consistent=bool(result.get("consistent")),
            error=None,
            summary=str(result.get("summary")),
        )
    except Exception as exc:
        return ModuleCIResult(
            module_name=module_name,
            top_check=top_check,
            expected_status=expected_status,
            import_ok=True,
            check_ok=False,
            actual_status=None,
            consistent=None,
            error=f"check failed: {exc!r}\n{traceback.format_exc(limit=3)}",
            summary=None,
        )


def summary_counts(results: Iterable[ModuleCIResult]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for result in results:
        status = result.ci_status.value
        counts[status] = counts.get(status, 0) + 1
    return counts


def build_optional_atlas_report() -> Optional[Mapping[str, Any]]:
    try:
        atlas_mod = importlib.import_module("apf.interface_atlas")
        return atlas_mod.build_canonical_atlas().to_dict()
    except Exception as exc:
        return {"error": f"atlas report failed: {exc!r}"}


def build_optional_adapter_reports() -> Tuple[Optional[Mapping[str, Any]], Optional[Mapping[str, Any]]]:
    ew_report = None
    dark_report = None
    try:
        ew_mod = importlib.import_module("apf.ew_trace_to_scheme_real_adapter")
        ew_report = ew_mod.build_live_adapter_report(name="ci_EW_live_adapter").to_dict()
    except Exception as exc:
        ew_report = {"error": f"EW adapter report failed: {exc!r}"}

    try:
        dark_mod = importlib.import_module("apf.dark_posterior_real_adapter")
        dark_report = dark_mod.build_live_adapter_report(name="ci_dark_live_adapter").to_dict()
    except Exception as exc:
        dark_report = {"error": f"dark adapter report failed: {exc!r}"}

    return ew_report, dark_report


def run_interface_intelligence_CI(*, include_live_adapters: bool = True, include_atlas: bool = True) -> InterfaceIntelligenceCIReport:
    results = tuple(run_module_top_check(module, check, status) for module, check, status in MODULE_TARGETS)

    atlas = build_optional_atlas_report() if include_atlas else None
    ew_report = dark_report = None
    if include_live_adapters:
        ew_report, dark_report = build_optional_adapter_reports()

    all_pass = all(result.ci_status == CIStatus.PASS for result in results)
    atlas_ok = atlas is None or "error" not in atlas
    adapter_ok = (
        (ew_report is None or "error" not in ew_report)
        and (dark_report is None or "error" not in dark_report)
    )

    release_gate_pass = bool(all_pass and atlas_ok and adapter_ok)
    if release_gate_pass:
        reason = "All interface-intelligence top checks passed; optional reports generated."
    else:
        failed = [r.module_name for r in results if r.ci_status != CIStatus.PASS]
        reason = f"CI gate failed or optional report failed. failed_modules={failed}; atlas_ok={atlas_ok}; adapter_ok={adapter_ok}"

    return InterfaceIntelligenceCIReport(
        created_utc=datetime.now(timezone.utc).isoformat(),
        module_results=results,
        atlas_report=atlas,
        ew_adapter_report=ew_report,
        dark_adapter_report=dark_report,
        release_gate_pass=release_gate_pass,
        release_gate_reason=reason,
    )


def check_T_CI_module_target_coverage_P() -> Dict[str, Any]:
    modules = [x[0] for x in MODULE_TARGETS]
    tests = {
        "target_count_at_least_14": len(MODULE_TARGETS) >= 14,
        "has_ew_adapter": "apf.ew_trace_to_scheme_real_adapter" in modules,
        "has_dark_adapter": "apf.dark_posterior_real_adapter" in modules,
        "has_claim_compiler": "apf.claim_to_interface_graph_compiler" in modules,
        "has_atlas": "apf.interface_atlas" in modules,
    }
    return {
        "name": "check_T_CI_module_target_coverage_P",
        "consistent": all(tests.values()),
        "status": "P_CI" if all(tests.values()) else "FAIL",
        "summary": "CI orchestrator covers the full interface-intelligence stack through atlas and real adapters.",
        "data": {"tests": tests, "modules": modules},
    }


def check_T_CI_top_checks_pass_P() -> Dict[str, Any]:
    report = run_interface_intelligence_CI(include_live_adapters=False, include_atlas=False)
    counts = summary_counts(report.module_results)
    tests = {
        "all_targets_pass": all(r.ci_status == CIStatus.PASS for r in report.module_results),
        "no_import_fail": counts.get("IMPORT_FAIL", 0) == 0,
        "no_check_fail": counts.get("CHECK_FAIL", 0) == 0,
        "no_status_fail": counts.get("FAIL", 0) == 0,
    }
    return {
        "name": "check_T_CI_top_checks_pass_P",
        "consistent": all(tests.values()),
        "status": "P_CI" if all(tests.values()) else "FAIL",
        "summary": "CI orchestrator can run all top checks and confirm expected P statuses.",
        "data": {"tests": tests, "summary_counts": counts},
        "dependencies": ["check_T_CI_module_target_coverage_P"],
    }


def check_T_CI_report_generation_P() -> Dict[str, Any]:
    report = run_interface_intelligence_CI(include_live_adapters=True, include_atlas=True)
    data = report.to_dict()
    tests = {
        "has_module_results": len(data["module_results"]) >= 14,
        "has_atlas_report": data["atlas_report"] is not None,
        "has_ew_report": data["ew_adapter_report"] is not None,
        "has_dark_report": data["dark_adapter_report"] is not None,
        "summary_counts_present": "summary_counts" in data,
    }
    return {
        "name": "check_T_CI_report_generation_P",
        "consistent": all(tests.values()),
        "status": "P_CI" if all(tests.values()) else "FAIL",
        "summary": "CI orchestrator emits module, atlas, and live-adapter reports.",
        "data": {"tests": tests, "release_gate_pass": data["release_gate_pass"], "release_gate_reason": data["release_gate_reason"]},
        "dependencies": ["check_T_CI_top_checks_pass_P"],
    }


def check_T_interface_intelligence_CI_orchestrator_P() -> Dict[str, Any]:
    subchecks = [
        check_T_CI_module_target_coverage_P(),
        check_T_CI_top_checks_pass_P(),
        check_T_CI_report_generation_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_interface_intelligence_CI_orchestrator_P",
        "consistent": ok,
        "status": "P_CI_orchestrator" if ok else "FAIL",
        "summary": "Interface Intelligence CI Orchestrator is P: it runs the full stack, checks expected P statuses, and emits release reports.",
        "data": {
            "core_claim": "The full interface-intelligence stack can be executed as a single CI/release target without promoting route-level physics claims.",
            "subchecks": [x["name"] for x in subchecks],
            "target_count": len(MODULE_TARGETS),
        },
        "dependencies": [x["name"] for x in subchecks],
    }


CHECKS = {
    "check_T_CI_module_target_coverage_P": check_T_CI_module_target_coverage_P,
    "check_T_CI_top_checks_pass_P": check_T_CI_top_checks_pass_P,
    "check_T_CI_report_generation_P": check_T_CI_report_generation_P,
    "check_T_interface_intelligence_CI_orchestrator_P": check_T_interface_intelligence_CI_orchestrator_P,
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
            raise TypeError("Unsupported registry type for interface_intelligence_CI_orchestrator.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
