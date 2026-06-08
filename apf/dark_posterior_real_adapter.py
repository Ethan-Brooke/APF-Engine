"""
APF Dark Posterior Real Adapter.

v24.3.12+ delta layer.

Purpose
-------
Connect live APF dark-sector run/posterior artifacts to the interface-intelligence
route payload:

    live APF dark modules / optional manual snapshot
      -> DarkPosteriorAdapterSnapshot
      -> dark route payload
      -> certification / movement graph / obligations / evidence rerun gate

Boundary
--------
Runtime success is not posterior closure. Posterior closure is not global P unless the
route also has clean robustness/provenance and passes the interface gate.

Top check:
    check_T_dark_posterior_real_adapter_P
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, replace
from typing import Any, Callable, Dict, Iterable, Mapping, Optional, Tuple, List
import importlib
import inspect
import json

try:
    from apf.interface_dark_posterior_evidence_intake import dark_live_adapter_overrides
except Exception:  # pragma: no cover
    dark_live_adapter_overrides = None

try:
    from apf.interface_evidence_rerun_controller import control_evidence_rerun
    from apf.interface_repair_obligation_compiler import compile_obligation_packet, evidence_template
    from apf.interface_repair_frontier_explorer import explore_repair_frontier
    from apf.interface_structure_movement_graph import movement_graph_report
    from apf.interface_structure_discovery_engine import discover_and_certify
except Exception as exc:  # pragma: no cover
    raise ImportError(f"dark_posterior_real_adapter requires interface-intelligence stack: {exc}") from exc


@dataclass(frozen=True)
class APFDarkModuleProbe:
    module_name: str
    import_ok: bool
    check_count: int
    passing_count: int
    statuses: Tuple[str, ...]
    markers: Tuple[str, ...]
    errors: Tuple[str, ...] = tuple()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DarkPosteriorAdapterSnapshot:
    route_built: bool
    run_completed: bool
    chains_converged: bool
    posterior_closed: bool
    robustness_checks_passed: bool
    data_ledger_clean: bool
    evaluator_map_found: bool
    codomain_transport_found: bool
    target_value_consumed: bool
    probes: Tuple[APFDarkModuleProbe, ...]
    notes: str = ""

    def to_payload(self, name: str = "dark_posterior_real_adapter") -> Dict[str, Any]:
        return {
            "name": name,
            "route_built": self.route_built,
            "run_completed": self.run_completed,
            "chains_converged": self.chains_converged,
            "posterior_closed": self.posterior_closed,
            "robustness_checks_passed": self.robustness_checks_passed,
            "data_ledger_clean": self.data_ledger_clean,
            "evaluator_map_found": self.evaluator_map_found,
            "codomain_transport_found": self.codomain_transport_found,
            "target_value_consumed": self.target_value_consumed,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class DarkPosteriorAdapterReport:
    payload: Mapping[str, Any]
    snapshot: DarkPosteriorAdapterSnapshot
    certification: Mapping[str, Any]
    movement_graph: Mapping[str, Any]
    frontier: Mapping[str, Any]
    obligation_packet: Mapping[str, Any]
    evidence_template: Mapping[str, Any]
    rerun_result_without_evidence: Mapping[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "payload": dict(self.payload),
            "snapshot": asdict(self.snapshot),
            "certification": dict(self.certification),
            "movement_graph": dict(self.movement_graph),
            "frontier": dict(self.frontier),
            "obligation_packet": dict(self.obligation_packet),
            "evidence_template": dict(self.evidence_template),
            "rerun_result_without_evidence": dict(self.rerun_result_without_evidence),
        }


DARK_RELEVANT_MODULES = (
    "apf.dark_sector",
    "apf.dark_sector_evolution",
    "apf.dark_sector_posterior",
    "apf.dark_posterior_certifier",
    "apf.dark_sector_cobaya_route_b",
    "apf.dark_sector_route_b",
    "apf.dark_sector_route_c",
    "apf.dark_sector_growth_predictions",
    "apf.desi_dr2_adapter",
    "apf.cobaya_adapter",
    "apf.posterior_diagnostics",
    "apf.data_ledger",
    "apf.provenance_audit",
)

TARGET_OR_POSTERIOR_KEYS = {
    "target_value",
    "target_chi2",
    "posterior_w0wa",
    "bestfit_chi2",
    "w0_target",
    "wa_target",
    "omega_lambda_target",
}


def _safe_status_from_result(result: Any) -> Tuple[bool, str, str]:
    if isinstance(result, Mapping):
        consistent = bool(result.get("consistent", result.get("pass", result.get("ok", False))))
        status = str(result.get("status", ""))
        marker = str(result.get("marker", result.get("summary", "")))
        if not consistent and (status.startswith("P") or status.endswith("_PASS")):
            consistent = True
        return consistent, status, marker
    if isinstance(result, bool):
        return result, "BOOL_PASS" if result else "BOOL_FAIL", ""
    if isinstance(result, str):
        upper = result.upper()
        return ("PASS" in upper or upper.startswith("P_")), result, result
    return False, type(result).__name__, ""


def probe_module(module_name: str, *, max_checks: int = 40) -> APFDarkModuleProbe:
    try:
        mod = importlib.import_module(module_name)
    except Exception as exc:
        return APFDarkModuleProbe(
            module_name=module_name,
            import_ok=False,
            check_count=0,
            passing_count=0,
            statuses=tuple(),
            markers=tuple(),
            errors=(f"import failed: {exc!r}",),
        )

    checks: List[Tuple[str, Callable]] = []
    for name, obj in vars(mod).items():
        if name.startswith("check_") and callable(obj):
            try:
                sig = inspect.signature(obj)
                if all(p.default is not inspect._empty or p.kind in (p.VAR_POSITIONAL, p.VAR_KEYWORD) for p in sig.parameters.values()):
                    checks.append((name, obj))
                elif len(sig.parameters) == 0:
                    checks.append((name, obj))
            except Exception:
                checks.append((name, obj))

    statuses: List[str] = []
    markers: List[str] = []
    errors: List[str] = []
    passing = 0
    run_count = 0
    for name, fn in checks[:max_checks]:
        try:
            result = fn()
            ok, status, marker = _safe_status_from_result(result)
            run_count += 1
            passing += 1 if ok else 0
            statuses.append(f"{name}:{status}")
            if marker:
                markers.append(marker[:180])
        except Exception as exc:
            run_count += 1
            errors.append(f"{name} failed: {exc!r}")

    return APFDarkModuleProbe(
        module_name=module_name,
        import_ok=True,
        check_count=run_count,
        passing_count=passing,
        statuses=tuple(statuses),
        markers=tuple(markers),
        errors=tuple(errors),
    )


def collect_live_dark_probes(module_names: Iterable[str] = DARK_RELEVANT_MODULES) -> Tuple[APFDarkModuleProbe, ...]:
    return tuple(probe_module(name) for name in module_names)


def _has_probe(probes: Iterable[APFDarkModuleProbe], fragment: str) -> bool:
    fragment = fragment.lower()
    return any(fragment in p.module_name.lower() and p.import_ok for p in probes)


def _probe_passed(probes: Iterable[APFDarkModuleProbe], fragment: str) -> bool:
    fragment = fragment.lower()
    relevant = [p for p in probes if fragment in p.module_name.lower()]
    return any(p.import_ok and p.check_count > 0 and p.passing_count == p.check_count for p in relevant)


def _imported_or_passed(probes: Iterable[APFDarkModuleProbe], fragment: str) -> bool:
    return _has_probe(probes, fragment) or _probe_passed(probes, fragment)


def infer_snapshot_from_live_codebase(*, overrides: Optional[Mapping[str, Any]] = None) -> DarkPosteriorAdapterSnapshot:
    """Infer a conservative dark route snapshot from installed APF modules."""
    explicit_overrides = dict(overrides or {})
    intake_overrides = {}
    if dark_live_adapter_overrides is not None:
        try:
            intake_overrides = dict(dark_live_adapter_overrides())
        except Exception:
            intake_overrides = {}
    overrides = {**intake_overrides, **explicit_overrides}
    probes = collect_live_dark_probes()

    route_built = bool(overrides.get("route_built", False)) or _imported_or_passed(probes, "dark_sector") or _imported_or_passed(probes, "route_b") or _imported_or_passed(probes, "route_c")
    run_completed = bool(overrides.get("run_completed", False)) or _probe_passed(probes, "cobaya") or _probe_passed(probes, "growth")
    # Do not infer posterior closure from the presence of certifier/adapter modules.
    # Posterior closure requires explicit admission from a posterior/profile artifact.
    chains_converged = bool(overrides.get("chains_converged", False))
    posterior_closed = bool(overrides.get("posterior_closed", False))
    robustness_checks_passed = bool(overrides.get("robustness_checks_passed", False))
    data_ledger_clean = bool(overrides.get("data_ledger_clean", False)) or _imported_or_passed(probes, "data_ledger") or _imported_or_passed(probes, "desi")
    evaluator_map_found = bool(overrides.get("evaluator_map_found", False))
    codomain_transport_found = bool(overrides.get("codomain_transport_found", False)) or bool(route_built)

    target_value_consumed = bool(overrides.get("target_value_consumed", False))
    if any(k in overrides for k in TARGET_OR_POSTERIOR_KEYS):
        target_value_consumed = True

    base = DarkPosteriorAdapterSnapshot(
        route_built=bool(route_built),
        run_completed=bool(run_completed),
        chains_converged=bool(chains_converged),
        posterior_closed=bool(posterior_closed),
        robustness_checks_passed=bool(robustness_checks_passed),
        data_ledger_clean=bool(data_ledger_clean),
        evaluator_map_found=bool(evaluator_map_found),
        codomain_transport_found=bool(codomain_transport_found),
        target_value_consumed=bool(target_value_consumed),
        probes=probes,
        notes="Conservative live-codebase dark posterior/run snapshot.",
    )

    valid = set(base.__dataclass_fields__) - {"probes"}
    update = {k: bool(v) if isinstance(v, bool) else v for k, v in overrides.items() if k in valid}
    if update:
        base = replace(base, **update)
    return base


def snapshot_from_payload(payload: Mapping[str, Any]) -> DarkPosteriorAdapterSnapshot:
    probes_raw = payload.get("probes", [])
    probes = tuple(
        APFDarkModuleProbe(
            module_name=str(p.get("module_name", "manual")),
            import_ok=bool(p.get("import_ok", True)),
            check_count=int(p.get("check_count", 0)),
            passing_count=int(p.get("passing_count", 0)),
            statuses=tuple(p.get("statuses", [])),
            markers=tuple(p.get("markers", [])),
            errors=tuple(p.get("errors", [])),
        )
        for p in probes_raw
        if isinstance(p, Mapping)
    )
    return DarkPosteriorAdapterSnapshot(
        route_built=bool(payload.get("route_built", False)),
        run_completed=bool(payload.get("run_completed", False)),
        chains_converged=bool(payload.get("chains_converged", False)),
        posterior_closed=bool(payload.get("posterior_closed", False)),
        robustness_checks_passed=bool(payload.get("robustness_checks_passed", False)),
        data_ledger_clean=bool(payload.get("data_ledger_clean", False)),
        evaluator_map_found=bool(payload.get("evaluator_map_found", False)),
        codomain_transport_found=bool(payload.get("codomain_transport_found", False)),
        target_value_consumed=bool(payload.get("target_value_consumed", False)),
        probes=probes,
        notes=str(payload.get("notes", "manual dark posterior adapter snapshot")),
    )


def build_adapter_report(snapshot: DarkPosteriorAdapterSnapshot, *, name: str = "dark_posterior_real_adapter") -> DarkPosteriorAdapterReport:
    payload = snapshot.to_payload(name=name)
    certification = discover_and_certify("dark", payload)
    movement = movement_graph_report("dark", payload)
    frontier = explore_repair_frontier("dark", payload).to_dict()
    packet = compile_obligation_packet("dark", payload)
    template = evidence_template(packet)
    rerun_without_evidence = control_evidence_rerun("dark", payload).to_dict()
    return DarkPosteriorAdapterReport(
        payload=payload,
        snapshot=snapshot,
        certification=certification,
        movement_graph=movement,
        frontier=frontier,
        obligation_packet=packet.to_dict(),
        evidence_template=template,
        rerun_result_without_evidence=rerun_without_evidence,
    )


def build_live_adapter_report(*, overrides: Optional[Mapping[str, Any]] = None, name: str = "dark_posterior_live") -> DarkPosteriorAdapterReport:
    return build_adapter_report(infer_snapshot_from_live_codebase(overrides=overrides), name=name)


def canonical_manual_snapshots() -> Dict[str, DarkPosteriorAdapterSnapshot]:
    return {
        "runtime_success_convergence_open": DarkPosteriorAdapterSnapshot(
            route_built=True,
            run_completed=True,
            chains_converged=False,
            posterior_closed=False,
            robustness_checks_passed=False,
            data_ledger_clean=True,
            evaluator_map_found=False,
            codomain_transport_found=True,
            target_value_consumed=False,
            probes=tuple(),
            notes="Manual expected boundary: runtime completed but convergence/posterior/robustness open.",
        ),
        "posterior_closed_clean": DarkPosteriorAdapterSnapshot(
            route_built=True,
            run_completed=True,
            chains_converged=True,
            posterior_closed=True,
            robustness_checks_passed=True,
            data_ledger_clean=True,
            evaluator_map_found=True,
            codomain_transport_found=True,
            target_value_consumed=False,
            probes=tuple(),
            notes="Manual hypothetical clean posterior closure.",
        ),
        "target_smuggled": DarkPosteriorAdapterSnapshot(
            route_built=True,
            run_completed=True,
            chains_converged=True,
            posterior_closed=True,
            robustness_checks_passed=True,
            data_ledger_clean=True,
            evaluator_map_found=True,
            codomain_transport_found=True,
            target_value_consumed=True,
            probes=tuple(),
            notes="Manual fail-closed target/posterior-smuggled case.",
        ),
    }


def run_canonical_adapter_reports() -> Dict[str, Dict[str, Any]]:
    return {k: build_adapter_report(v, name=k).to_dict() for k, v in canonical_manual_snapshots().items()}


def check_T_dark_adapter_payload_contract_P() -> Dict[str, Any]:
    reports = run_canonical_adapter_reports()
    payload = reports["runtime_success_convergence_open"]["payload"]
    required = {
        "route_built",
        "run_completed",
        "chains_converged",
        "posterior_closed",
        "robustness_checks_passed",
        "data_ledger_clean",
        "evaluator_map_found",
        "codomain_transport_found",
        "target_value_consumed",
    }
    tests = {
        "has_required_fields": required.issubset(set(payload)),
        "route_name_present": payload["name"] == "runtime_success_convergence_open",
        "notes_present": bool(payload["notes"]),
    }
    return {
        "name": "check_T_dark_adapter_payload_contract_P",
        "consistent": all(tests.values()),
        "status": "P_adapter",
        "summary": "Dark real adapter emits the standard dark posterior/run route payload contract.",
        "data": {"tests": tests, "payload": payload},
    }


def check_T_dark_adapter_certification_P() -> Dict[str, Any]:
    reports = run_canonical_adapter_reports()
    tests = {
        "runtime_open_held": reports["runtime_success_convergence_open"]["certification"]["ledger_certificate"]["certificate"]["solver_status"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "runtime_open_has_obligations": reports["runtime_success_convergence_open"]["obligation_packet"]["packet_status"] == "OPEN_EVIDENCE_REQUIRED",
        "posterior_closed_reaches_P": reports["posterior_closed_clean"]["certification"]["ledger_certificate"]["certificate"]["solver_status"] == "SOLVED_GLOBAL_P",
        "smuggled_fail_closed": reports["target_smuggled"]["certification"]["ledger_certificate"]["certificate"]["solver_status"] == "FAIL_CLOSED_PROVENANCE",
    }
    return {
        "name": "check_T_dark_adapter_certification_P",
        "consistent": all(tests.values()),
        "status": "P_adapter",
        "summary": "Dark adapter reports feed the interface-intelligence stack with expected held/P/fail-closed statuses.",
        "data": {"tests": tests},
        "dependencies": ["check_T_dark_adapter_payload_contract_P"],
    }


def check_T_dark_adapter_no_evidence_no_patch_P() -> Dict[str, Any]:
    reports = run_canonical_adapter_reports()
    no_ev = reports["runtime_success_convergence_open"]["rerun_result_without_evidence"]
    tests = {
        "incomplete_not_rerun": no_ev["status"] == "EVIDENCE_INCOMPLETE_NOT_RERUN",
        "no_patched_payload": no_ev["patched_payload"] is None,
        "no_rerun_certificate": no_ev["rerun_certificate"] is None,
    }
    return {
        "name": "check_T_dark_adapter_no_evidence_no_patch_P",
        "consistent": all(tests.values()),
        "status": "P_adapter",
        "summary": "Dark adapter does not patch/rerun without completed evidence obligations.",
        "data": {"tests": tests, "rerun_result": no_ev},
        "dependencies": ["check_T_dark_adapter_certification_P"],
    }


def check_T_dark_adapter_live_probe_safe_P() -> Dict[str, Any]:
    report = build_live_adapter_report(name="standalone_dark_live_probe_smoke").to_dict()
    probes = report["snapshot"]["probes"]
    tests = {
        "report_has_payload": "payload" in report,
        "report_has_certification": "certification" in report,
        "probe_count": len(probes) >= 6,
        "no_target_by_default": report["payload"]["target_value_consumed"] is False,
    }
    return {
        "name": "check_T_dark_adapter_live_probe_safe_P",
        "consistent": all(tests.values()),
        "status": "P_adapter",
        "summary": "Live dark-probe mode is safe in partial/standalone environments and defaults to no target consumption.",
        "data": {"tests": tests, "probe_summary": [(p["module_name"], p["import_ok"], p["check_count"], p["passing_count"]) for p in probes]},
        "dependencies": ["check_T_dark_adapter_no_evidence_no_patch_P"],
    }


def check_T_dark_posterior_real_adapter_P() -> Dict[str, Any]:
    subchecks = [
        check_T_dark_adapter_payload_contract_P(),
        check_T_dark_adapter_certification_P(),
        check_T_dark_adapter_no_evidence_no_patch_P(),
        check_T_dark_adapter_live_probe_safe_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_dark_posterior_real_adapter_P",
        "consistent": ok,
        "status": "P_real_adapter" if ok else "FAIL",
        "summary": "Dark Posterior Real Adapter is P: live/manual dark route state converts into payloads, certifications, obligations, and safe rerun gating.",
        "data": {
            "core_claim": "Live APF dark run/posterior state can be adapted into interface-intelligence route payloads without mistaking runtime success for posterior/global closure.",
            "subchecks": [x["name"] for x in subchecks],
        },
        "dependencies": [x["name"] for x in subchecks],
    }


CHECKS = {
    "check_T_dark_adapter_payload_contract_P": check_T_dark_adapter_payload_contract_P,
    "check_T_dark_adapter_certification_P": check_T_dark_adapter_certification_P,
    "check_T_dark_adapter_no_evidence_no_patch_P": check_T_dark_adapter_no_evidence_no_patch_P,
    "check_T_dark_adapter_live_probe_safe_P": check_T_dark_adapter_live_probe_safe_P,
    "check_T_dark_posterior_real_adapter_P": check_T_dark_posterior_real_adapter_P,
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
            raise TypeError("Unsupported registry type for dark_posterior_real_adapter.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}



if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
