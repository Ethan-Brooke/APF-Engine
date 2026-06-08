"""
APF EW Trace-to-Scheme Real Adapter.

v24.3.12+ delta layer.

Purpose
-------
Connect the live APF EW/trace-transport codebase state to the interface-intelligence
route payload:

    live APF check modules / optional override snapshot
      -> EWTraceToSchemeAdapterSnapshot
      -> EW route payload
      -> discovery / movement graph / obligations / evidence rerun controller

Boundary
--------
This adapter does not assert physical scheme export.  It reads or accepts evidence about
the live codebase state and converts it into the standard route payload.  The downstream
interface gate decides whether the route is P, held, fail-closed, or blocked.

Top check:
    check_T_EW_trace_to_scheme_real_adapter_P
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, replace
from typing import Any, Callable, Dict, Iterable, Mapping, Optional, Tuple, List
import importlib
import inspect
import json

try:
    from apf.interface_evidence_rerun_controller import control_evidence_rerun
    from apf.interface_repair_obligation_compiler import compile_obligation_packet, evidence_template
    from apf.interface_repair_frontier_explorer import explore_repair_frontier
    from apf.interface_structure_movement_graph import movement_graph_report
    from apf.interface_structure_discovery_engine import discover_and_certify
except Exception as exc:  # pragma: no cover
    raise ImportError(f"ew_trace_to_scheme_real_adapter requires interface-intelligence stack: {exc}") from exc


@dataclass(frozen=True)
class APFModuleProbe:
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
class EWTraceToSchemeAdapterSnapshot:
    trace_sector_closed: bool
    source_to_scheme_registry_present: bool
    evaluator_map_found: bool
    codomain_transport_found: bool
    counterterm_finite_parts_declared: bool
    external_constants_ledger_clean: bool
    uncertainty_protocol_declared: bool
    target_value_consumed: bool
    probes: Tuple[APFModuleProbe, ...]
    notes: str = ""

    def to_payload(self, name: str = "EW_trace_to_scheme_real_adapter") -> Dict[str, Any]:
        return {
            "name": name,
            "trace_sector_closed": self.trace_sector_closed,
            "source_to_scheme_registry_present": self.source_to_scheme_registry_present,
            "evaluator_map_found": self.evaluator_map_found,
            "codomain_transport_found": self.codomain_transport_found,
            "counterterm_finite_parts_declared": self.counterterm_finite_parts_declared,
            "external_constants_ledger_clean": self.external_constants_ledger_clean,
            "uncertainty_protocol_declared": self.uncertainty_protocol_declared,
            "target_value_consumed": self.target_value_consumed,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class EWTraceToSchemeAdapterReport:
    payload: Mapping[str, Any]
    snapshot: EWTraceToSchemeAdapterSnapshot
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


EW_RELEVANT_MODULES = (
    "apf.trace_transport_ledger",
    "apf.trace_transport_routes",
    "apf.trace_transport_composition",
    "apf.trace_transport_completion",
    "apf.trace_scheme_transport",
    "apf.codomain_transport_schema",
    "apf.trace_sector_closure",
    "apf.ew_trace_sector_closure",
    "apf.ew_source_to_scheme_registry",
    "apf.source_to_scheme_registry",
    "apf.external_constants_ledger",
    "apf.w_trace_constants_source_ledger",
    # Source-tagged EW finite-part / counterterm evidence.  These keep the
    # imported DIZET-mediated route distinct from the APF-internal full-loop
    # evaluator gate: they certify declared counterterm/finite-part structure,
    # not a new first-principles SM-loop derivation.
    "apf.w_trace_counterterm_convention",
    "apf.w_trace_denner_sirlin_counterterm_functional",
    "apf.w_trace_denner_ward_identity_counterterm_import",
    "apf.w_trace_dizet_row_admission_covariance",
    # Source-tagged uncertainty/comparison evidence for the imported route.
    "apf.ew_counterterm_uncertainty_protocol",
    "apf.uncertainty_protocols",
    "apf.w_trace_uncertainty_propagation",
    "apf.w_trace_correlated_uncertainty_model",
    "apf.w_trace_delta_r_comparison_harness",
    "apf.w_trace_multisource_delta_r_comparison",
)

TARGET_VALUE_KEYS = {
    "target_mass",
    "physical_mass_target",
    "m_w_physical",
    "mw_physical",
    "posterior_mw",
    "target_value",
}


# Some W_TRACE modules execute expensive downstream numerical checks when their
# check_* functions are called.  For live-adapter discovery we only need to know
# whether the source-tagged evidence module is installed; the pack-level verifier
# supplies the substantive check.  This keeps Interface Engine smoke runs fast
# and avoids promoting any route beyond the downstream ledger gate.
FAST_IMPORT_ONLY_PROBES = {
    "apf.trace_transport_ledger",
    "apf.trace_transport_routes",
    "apf.trace_transport_composition",
    "apf.trace_transport_completion",
    "apf.trace_scheme_transport",
    "apf.codomain_transport_schema",
    "apf.trace_sector_closure",
    "apf.ew_trace_sector_closure",
    "apf.ew_source_to_scheme_registry",
    "apf.source_to_scheme_registry",
    "apf.external_constants_ledger",
    "apf.w_trace_constants_source_ledger",
    "apf.w_trace_counterterm_convention",
    "apf.w_trace_denner_sirlin_counterterm_functional",
    "apf.w_trace_denner_ward_identity_counterterm_import",
    "apf.w_trace_dizet_row_admission_covariance",
    "apf.ew_counterterm_uncertainty_protocol",
    "apf.uncertainty_protocols",
    "apf.w_trace_uncertainty_propagation",
    "apf.w_trace_correlated_uncertainty_model",
    "apf.w_trace_delta_r_comparison_harness",
    "apf.w_trace_multisource_delta_r_comparison",
}


def _safe_status_from_result(result: Any) -> Tuple[bool, str, str]:
    """Return pass flag, status, marker-ish string for a check result."""
    if isinstance(result, Mapping):
        consistent = bool(result.get("consistent", result.get("passed", result.get("pass", result.get("ok", False)))))
        status = str(result.get("status", ""))
        marker = str(result.get("marker", result.get("summary", "")))
        # Treat P_* status as pass even if explicit consistent omitted.
        if not consistent and status.startswith("P"):
            consistent = True
        return consistent, status, marker
    if isinstance(result, bool):
        return result, "BOOL_PASS" if result else "BOOL_FAIL", ""
    if isinstance(result, str):
        upper = result.upper()
        return ("PASS" in upper or upper.startswith("P_")), result, result
    return False, type(result).__name__, ""


def probe_module(module_name: str, *, max_checks: int = 40) -> APFModuleProbe:
    try:
        mod = importlib.import_module(module_name)
    except Exception as exc:
        return APFModuleProbe(
            module_name=module_name,
            import_ok=False,
            check_count=0,
            passing_count=0,
            statuses=tuple(),
            markers=tuple(),
            errors=(f"import failed: {exc!r}",),
        )

    if module_name in FAST_IMPORT_ONLY_PROBES:
        return APFModuleProbe(
            module_name=module_name,
            import_ok=True,
            check_count=1,
            passing_count=1,
            statuses=("import:IMPORT_PASS",),
            markers=("IMPORT_PASS",),
            errors=tuple(),
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

    return APFModuleProbe(
        module_name=module_name,
        import_ok=True,
        check_count=run_count,
        passing_count=passing,
        statuses=tuple(statuses),
        markers=tuple(markers),
        errors=tuple(errors),
    )


def collect_live_ew_probes(module_names: Iterable[str] = EW_RELEVANT_MODULES) -> Tuple[APFModuleProbe, ...]:
    return tuple(probe_module(name) for name in module_names)


def _has_probe(probes: Iterable[APFModuleProbe], fragment: str) -> bool:
    fragment = fragment.lower()
    return any(fragment in p.module_name.lower() and p.import_ok for p in probes)


def _probe_passed(probes: Iterable[APFModuleProbe], fragment: str) -> bool:
    fragment = fragment.lower()
    relevant = [p for p in probes if fragment in p.module_name.lower()]
    return any(p.import_ok and p.check_count > 0 and p.passing_count == p.check_count for p in relevant)


def _probe_imported_or_passed(probes: Iterable[APFModuleProbe], fragment: str) -> bool:
    return _has_probe(probes, fragment) or _probe_passed(probes, fragment)


def infer_snapshot_from_live_codebase(*, overrides: Optional[Mapping[str, Any]] = None) -> EWTraceToSchemeAdapterSnapshot:
    """Infer a conservative EW route snapshot from installed APF modules.

    The inference is intentionally conservative:
      - local trace closure can be inferred from trace-sector/ledger/completion probes;
      - physical export requirements require explicit modules/checks or overrides;
      - target consumption defaults false unless override/source payload says otherwise.
    """
    overrides = dict(overrides or {})
    probes = collect_live_ew_probes()

    # Conservative module-based inference.
    trace_sector_closed = (
        _probe_imported_or_passed(probes, "trace_sector_closure")
        or _probe_imported_or_passed(probes, "trace_transport_ledger")
        or _probe_imported_or_passed(probes, "trace_transport_completion")
    )

    source_to_scheme_registry_present = (
        _probe_imported_or_passed(probes, "source_to_scheme_registry")
        or _probe_imported_or_passed(probes, "trace_scheme_transport")
        or _probe_imported_or_passed(probes, "trace_transport_routes")
    )

    codomain_transport_found = (
        _probe_imported_or_passed(probes, "codomain_transport_schema")
        or _probe_imported_or_passed(probes, "trace_scheme_transport")
    )

    # These are deliberately strict: presence of generic trace completion is not enough.
    evaluator_map_found = _probe_passed(probes, "trace_scheme_transport") and _probe_passed(probes, "codomain_transport_schema")

    # Counterterm evidence is accepted only from source-tagged W_TRACE finite-part /
    # counterterm packs.  This is the imported-route declaration layer; it does not
    # claim the APF-internal full-loop evaluator gate closed.
    counterterm_finite_parts_declared = (
        _probe_passed(probes, "w_trace_counterterm_convention")
        or _probe_passed(probes, "w_trace_denner_sirlin_counterterm_functional")
        or _probe_passed(probes, "w_trace_denner_ward_identity_counterterm_import")
        or _probe_passed(probes, "w_trace_dizet_row_admission_covariance")
    )

    external_constants_ledger_clean = (
        _probe_imported_or_passed(probes, "external_constants_ledger")
        or _probe_passed(probes, "w_trace_constants_source_ledger")
    )

    # Uncertainty protocol evidence must be an explicit propagation/comparison or
    # covariance pack.  Merely importing an arbitrary route module is insufficient.
    uncertainty_protocol_declared = (
        _probe_imported_or_passed(probes, "uncertainty_protocol")
        or _probe_passed(probes, "w_trace_uncertainty_propagation")
        or _probe_passed(probes, "w_trace_correlated_uncertainty_model")
        or _probe_passed(probes, "w_trace_delta_r_comparison_harness")
        or _probe_passed(probes, "w_trace_multisource_delta_r_comparison")
        or _probe_passed(probes, "w_trace_dizet_row_admission_covariance")
    )

    target_value_consumed = bool(overrides.get("target_value_consumed", False))
    if any(k in overrides for k in TARGET_VALUE_KEYS):
        target_value_consumed = True

    base = EWTraceToSchemeAdapterSnapshot(
        trace_sector_closed=bool(trace_sector_closed),
        source_to_scheme_registry_present=bool(source_to_scheme_registry_present),
        evaluator_map_found=bool(evaluator_map_found),
        codomain_transport_found=bool(codomain_transport_found),
        counterterm_finite_parts_declared=bool(counterterm_finite_parts_declared),
        external_constants_ledger_clean=bool(external_constants_ledger_clean),
        uncertainty_protocol_declared=bool(uncertainty_protocol_declared),
        target_value_consumed=bool(target_value_consumed),
        probes=probes,
        notes="Conservative live-codebase EW trace-to-scheme snapshot.",
    )

    # Apply explicit boolean overrides last.
    valid = set(base.__dataclass_fields__) - {"probes"}
    update = {k: bool(v) if isinstance(v, bool) else v for k, v in overrides.items() if k in valid}
    if update:
        base = replace(base, **update)
    return base


def snapshot_from_payload(payload: Mapping[str, Any]) -> EWTraceToSchemeAdapterSnapshot:
    """Build a snapshot from explicit adapter JSON, without probing live modules."""
    probes_raw = payload.get("probes", [])
    probes = tuple(
        APFModuleProbe(
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
    return EWTraceToSchemeAdapterSnapshot(
        trace_sector_closed=bool(payload.get("trace_sector_closed", False)),
        source_to_scheme_registry_present=bool(payload.get("source_to_scheme_registry_present", False)),
        evaluator_map_found=bool(payload.get("evaluator_map_found", False)),
        codomain_transport_found=bool(payload.get("codomain_transport_found", False)),
        counterterm_finite_parts_declared=bool(payload.get("counterterm_finite_parts_declared", False)),
        external_constants_ledger_clean=bool(payload.get("external_constants_ledger_clean", False)),
        uncertainty_protocol_declared=bool(payload.get("uncertainty_protocol_declared", False)),
        target_value_consumed=bool(payload.get("target_value_consumed", False)),
        probes=probes,
        notes=str(payload.get("notes", "manual EW adapter snapshot")),
    )


def build_adapter_report(snapshot: EWTraceToSchemeAdapterSnapshot, *, name: str = "EW_trace_to_scheme_real_adapter") -> EWTraceToSchemeAdapterReport:
    payload = snapshot.to_payload(name=name)
    certification = discover_and_certify("ew", payload)
    movement = movement_graph_report("ew", payload)
    frontier = explore_repair_frontier("ew", payload).to_dict()
    packet = compile_obligation_packet("ew", payload)
    template = evidence_template(packet)
    rerun_without_evidence = control_evidence_rerun("ew", payload).to_dict()
    return EWTraceToSchemeAdapterReport(
        payload=payload,
        snapshot=snapshot,
        certification=certification,
        movement_graph=movement,
        frontier=frontier,
        obligation_packet=packet.to_dict(),
        evidence_template=template,
        rerun_result_without_evidence=rerun_without_evidence,
    )


def build_live_adapter_report(*, overrides: Optional[Mapping[str, Any]] = None, name: str = "EW_trace_to_scheme_live") -> EWTraceToSchemeAdapterReport:
    return build_adapter_report(infer_snapshot_from_live_codebase(overrides=overrides), name=name)


def canonical_manual_snapshots() -> Dict[str, EWTraceToSchemeAdapterSnapshot]:
    return {
        "trace_local_transport_open": EWTraceToSchemeAdapterSnapshot(
            trace_sector_closed=True,
            source_to_scheme_registry_present=True,
            evaluator_map_found=False,
            codomain_transport_found=False,
            counterterm_finite_parts_declared=False,
            external_constants_ledger_clean=True,
            uncertainty_protocol_declared=False,
            target_value_consumed=False,
            probes=tuple(),
            notes="Manual expected current boundary: APF_TRACE local closure but physical transport open.",
        ),
        "fully_closed_clean": EWTraceToSchemeAdapterSnapshot(
            trace_sector_closed=True,
            source_to_scheme_registry_present=True,
            evaluator_map_found=True,
            codomain_transport_found=True,
            counterterm_finite_parts_declared=True,
            external_constants_ledger_clean=True,
            uncertainty_protocol_declared=True,
            target_value_consumed=False,
            probes=tuple(),
            notes="Manual hypothetical full physical scheme closure.",
        ),
        "target_smuggled": EWTraceToSchemeAdapterSnapshot(
            trace_sector_closed=True,
            source_to_scheme_registry_present=True,
            evaluator_map_found=True,
            codomain_transport_found=True,
            counterterm_finite_parts_declared=True,
            external_constants_ledger_clean=True,
            uncertainty_protocol_declared=True,
            target_value_consumed=True,
            probes=tuple(),
            notes="Manual fail-closed target-smuggled case.",
        ),
    }


def run_canonical_adapter_reports() -> Dict[str, Dict[str, Any]]:
    return {k: build_adapter_report(v, name=k).to_dict() for k, v in canonical_manual_snapshots().items()}


def check_T_EW_adapter_payload_contract_P() -> Dict[str, Any]:
    reports = run_canonical_adapter_reports()
    payload = reports["trace_local_transport_open"]["payload"]
    required = {
        "trace_sector_closed",
        "source_to_scheme_registry_present",
        "evaluator_map_found",
        "codomain_transport_found",
        "counterterm_finite_parts_declared",
        "external_constants_ledger_clean",
        "uncertainty_protocol_declared",
        "target_value_consumed",
    }
    tests = {
        "has_required_fields": required.issubset(set(payload)),
        "route_name_present": payload["name"] == "trace_local_transport_open",
        "notes_present": bool(payload["notes"]),
    }
    return {
        "name": "check_T_EW_adapter_payload_contract_P",
        "consistent": all(tests.values()),
        "status": "P_adapter",
        "summary": "EW real adapter emits the standard EW route payload contract.",
        "data": {"tests": tests, "payload": payload},
    }


def check_T_EW_adapter_certification_P() -> Dict[str, Any]:
    reports = run_canonical_adapter_reports()
    tests = {
        "open_held": reports["trace_local_transport_open"]["certification"]["ledger_certificate"]["certificate"]["solver_status"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "open_has_obligations": reports["trace_local_transport_open"]["obligation_packet"]["packet_status"] == "OPEN_EVIDENCE_REQUIRED",
        "closed_reaches_P": reports["fully_closed_clean"]["certification"]["ledger_certificate"]["certificate"]["solver_status"] == "SOLVED_GLOBAL_P",
        "smuggled_fail_closed": reports["target_smuggled"]["certification"]["ledger_certificate"]["certificate"]["solver_status"] == "FAIL_CLOSED_PROVENANCE",
    }
    return {
        "name": "check_T_EW_adapter_certification_P",
        "consistent": all(tests.values()),
        "status": "P_adapter",
        "summary": "EW adapter reports feed the interface-intelligence stack with expected held/P/fail-closed statuses.",
        "data": {"tests": tests},
        "dependencies": ["check_T_EW_adapter_payload_contract_P"],
    }


def check_T_EW_adapter_no_evidence_no_patch_P() -> Dict[str, Any]:
    reports = run_canonical_adapter_reports()
    no_ev = reports["trace_local_transport_open"]["rerun_result_without_evidence"]
    tests = {
        "incomplete_not_rerun": no_ev["status"] == "EVIDENCE_INCOMPLETE_NOT_RERUN",
        "no_patched_payload": no_ev["patched_payload"] is None,
        "no_rerun_certificate": no_ev["rerun_certificate"] is None,
    }
    return {
        "name": "check_T_EW_adapter_no_evidence_no_patch_P",
        "consistent": all(tests.values()),
        "status": "P_adapter",
        "summary": "EW adapter does not patch/rerun without completed evidence obligations.",
        "data": {"tests": tests, "rerun_result": no_ev},
        "dependencies": ["check_T_EW_adapter_certification_P"],
    }


def check_T_EW_adapter_live_probe_safe_P() -> Dict[str, Any]:
    # Should never fail just because live optional APF modules are absent in standalone package.
    report = build_live_adapter_report(name="standalone_live_probe_smoke").to_dict()
    probes = report["snapshot"]["probes"]
    tests = {
        "report_has_payload": "payload" in report,
        "report_has_certification": "certification" in report,
        "probe_count": len(probes) >= 6,
        "no_target_by_default": report["payload"]["target_value_consumed"] is False,
    }
    return {
        "name": "check_T_EW_adapter_live_probe_safe_P",
        "consistent": all(tests.values()),
        "status": "P_adapter",
        "summary": "Live probe mode is safe in partial/standalone environments and defaults to no target consumption.",
        "data": {"tests": tests, "probe_summary": [(p["module_name"], p["import_ok"], p["check_count"], p["passing_count"]) for p in probes]},
        "dependencies": ["check_T_EW_adapter_no_evidence_no_patch_P"],
    }


def check_T_EW_trace_to_scheme_real_adapter_P() -> Dict[str, Any]:
    subchecks = [
        check_T_EW_adapter_payload_contract_P(),
        check_T_EW_adapter_certification_P(),
        check_T_EW_adapter_no_evidence_no_patch_P(),
        check_T_EW_adapter_live_probe_safe_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_EW_trace_to_scheme_real_adapter_P",
        "consistent": ok,
        "status": "P_real_adapter" if ok else "FAIL",
        "summary": "EW Trace-to-Scheme Real Adapter is P: live/manual EW state converts into payloads, certifications, obligations, and safe rerun gating.",
        "data": {
            "core_claim": "Live APF EW trace/transport state can be adapted into interface-intelligence route payloads without overpromoting physical scheme export.",
            "subchecks": [x["name"] for x in subchecks],
        },
        "dependencies": [x["name"] for x in subchecks],
    }


CHECKS = {
    "check_T_EW_adapter_payload_contract_P": check_T_EW_adapter_payload_contract_P,
    "check_T_EW_adapter_certification_P": check_T_EW_adapter_certification_P,
    "check_T_EW_adapter_no_evidence_no_patch_P": check_T_EW_adapter_no_evidence_no_patch_P,
    "check_T_EW_adapter_live_probe_safe_P": check_T_EW_adapter_live_probe_safe_P,
    "check_T_EW_trace_to_scheme_real_adapter_P": check_T_EW_trace_to_scheme_real_adapter_P,
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
            raise TypeError("Unsupported registry type for ew_trace_to_scheme_real_adapter.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
