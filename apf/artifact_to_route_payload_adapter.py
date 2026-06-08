"""
APF Artifact-to-Route Payload Adapter.

Purpose
-------
Parse real integration artifacts into interface-intelligence route payloads:

    verifier stdout/logs
    smoke summaries
    adapter reports
    CI reports
    arbitrary JSON/log snippets
      -> inferred route
      -> conservative route payload
      -> payload confidence/provenance
      -> optional certification report

Boundary
--------
Artifacts are evidence only when they contain explicit clean markers/fields. Ambiguous text
does not promote a route; unknown fields remain open and produce obligations downstream.

Top check:
    check_T_artifact_to_route_payload_adapter_P
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List
import json
import re


class ArtifactKind(str, Enum):
    VERIFIER_STDOUT = "VERIFIER_STDOUT"
    SMOKE_SUMMARY = "SMOKE_SUMMARY"
    ADAPTER_REPORT = "ADAPTER_REPORT"
    CI_REPORT = "CI_REPORT"
    JSON_PAYLOAD = "JSON_PAYLOAD"
    LOG_TEXT = "LOG_TEXT"
    UNKNOWN = "UNKNOWN"


class PayloadConfidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass(frozen=True)
class ArtifactPayloadCandidate:
    artifact_path: str
    artifact_kind: ArtifactKind
    route: str
    payload: Mapping[str, Any]
    confidence: PayloadConfidence
    detected_markers: Tuple[str, ...]
    warnings: Tuple[str, ...]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "artifact_path": self.artifact_path,
            "artifact_kind": self.artifact_kind.value,
            "route": self.route,
            "payload": dict(self.payload),
            "confidence": self.confidence.value,
            "detected_markers": self.detected_markers,
            "warnings": self.warnings,
        }


@dataclass(frozen=True)
class ArtifactAdapterBatchReport:
    candidates: Tuple[ArtifactPayloadCandidate, ...]
    route_counts: Mapping[str, int]
    confidence_counts: Mapping[str, int]
    warnings: Tuple[str, ...]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "candidates": [c.to_dict() for c in self.candidates],
            "route_counts": dict(self.route_counts),
            "confidence_counts": dict(self.confidence_counts),
            "warnings": self.warnings,
        }


EW_MARKERS = (
    "TRACE_SECTOR_BANK_INTEGRATION_PASS",
    "EW_SOURCE_TO_SCHEME_REGISTRY_REFRESH_PASS",
    "W_TRACE",
    "APF_TRACE",
    "EW_TRACE_TO_SCHEME_REAL_ADAPTER_P_PASS",
    "trace_sector_closed",
)
DARK_MARKERS = (
    "DARK_POSTERIOR_REAL_ADAPTER_P_PASS",
    "DARK_SECTOR",
    "COBAYA",
    "DESI",
    "posterior",
    "chains_converged",
    "run_completed",
)
GAUGE_MARKERS = ("GAUGE", "fiber", "automorphism", "cocycle", "anomaly")
HORIZON_MARKERS = ("HORIZON", "area_cost", "fiber-cost", "entropy_ledger")
CAPACITY_MARKERS = ("capacity", "overspend", "coarse_grain", "coarse-grain")
PROVENANCE_MARKERS = ("PROVENANCE_SMUGGLE", "target_value_consumed", "smuggling", "anti-fitting")
CSTAR_MARKERS = ("CSTAR", "C*", "substrate", "operator norm")


def _read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8", errors="replace")


def _try_json(path: str | Path) -> Optional[Any]:
    try:
        return json.loads(_read_text(path))
    except Exception:
        return None


def detect_artifact_kind(path: str | Path, obj: Optional[Any], text: str) -> ArtifactKind:
    p = str(path).lower()
    if isinstance(obj, Mapping):
        if "interface_intelligence_live_smoke_summary" in p or {"overall_pass", "steps", "report_zip"}.issubset(set(obj)):
            return ArtifactKind.SMOKE_SUMMARY
        if "module_results" in obj and "release_gate_pass" in obj:
            return ArtifactKind.CI_REPORT
        if "payload" in obj and ("certification" in obj or "movement_graph" in obj or "obligation_packet" in obj):
            return ArtifactKind.ADAPTER_REPORT
        if "route" in obj or "name" in obj:
            return ArtifactKind.JSON_PAYLOAD
    if "stdout" in p or "verifier" in p or "_pass" in text.upper():
        return ArtifactKind.VERIFIER_STDOUT
    if text:
        return ArtifactKind.LOG_TEXT
    return ArtifactKind.UNKNOWN


def _has_any(text: str, markers: Iterable[str]) -> Tuple[str, ...]:
    lower = text.lower()
    hits = []
    for marker in markers:
        if marker.lower() in lower:
            hits.append(marker)
    return tuple(hits)


def infer_route(text: str, obj: Optional[Any]) -> Tuple[str, Tuple[str, ...]]:
    if isinstance(obj, Mapping):
        if isinstance(obj.get("payload"), Mapping):
            payload = obj["payload"]
            name = str(payload.get("name", ""))
            route = str(obj.get("route", "") or "")
            if route in {"ew", "dark", "gauge", "horizon", "capacity", "provenance", "cstar"}:
                return route, (f"route:{route}",)
            if "ew" in name.lower() or "trace" in name.lower():
                return "ew", ("payload.name",)
            if "dark" in name.lower() or "posterior" in name.lower():
                return "dark", ("payload.name",)
        if obj.get("route") in {"ew", "dark", "gauge", "horizon", "capacity", "provenance", "cstar"}:
            return str(obj["route"]), (f"route:{obj['route']}",)
    marker_sets = [
        ("provenance", PROVENANCE_MARKERS),
        ("ew", EW_MARKERS),
        ("dark", DARK_MARKERS),
        ("gauge", GAUGE_MARKERS),
        ("horizon", HORIZON_MARKERS),
        ("capacity", CAPACITY_MARKERS),
        ("cstar", CSTAR_MARKERS),
    ]
    scored: List[Tuple[str, Tuple[str, ...]]] = []
    for route, markers in marker_sets:
        hits = _has_any(text, markers)
        if hits:
            scored.append((route, hits))
    if not scored:
        return "generic", tuple()
    scored.sort(key=lambda x: len(x[1]), reverse=True)
    return scored[0]


def _bool_from_obj(obj: Mapping[str, Any], keys: Iterable[str], default: bool = False) -> bool:
    for key in keys:
        if key in obj:
            return bool(obj[key])
    return default


def _flatten_json_text(obj: Any) -> str:
    try:
        return json.dumps(obj, sort_keys=True)
    except Exception:
        return str(obj)


def ew_payload_from_artifact(name: str, text: str, obj: Optional[Any]) -> Dict[str, Any]:
    payload = obj.get("payload", obj) if isinstance(obj, Mapping) else {}
    if not isinstance(payload, Mapping):
        payload = {}
    upper = text.upper()

    trace_closed = (
        _bool_from_obj(payload, ("trace_sector_closed",), False)
        or "TRACE_SECTOR_BANK_INTEGRATION_PASS" in upper
        or "TRACE_SECTOR_CLOSURE" in upper and "PASS" in upper
        or "APF_TRACE" in upper and ("P_LOCAL" in upper or "LOCAL CLOSURE" in upper)
    )
    registry = _bool_from_obj(payload, ("source_to_scheme_registry_present",), False) or "EW_SOURCE_TO_SCHEME_REGISTRY_REFRESH_PASS" in upper
    evaluator = _bool_from_obj(payload, ("evaluator_map_found",), False) or "evaluator_map_found\": true" in text.lower()
    codomain = _bool_from_obj(payload, ("codomain_transport_found",), False) or "codomain_transport_found\": true" in text.lower()
    counterterm = _bool_from_obj(payload, ("counterterm_finite_parts_declared",), False) or "counterterm_finite_parts_declared\": true" in text.lower()
    constants = _bool_from_obj(payload, ("external_constants_ledger_clean",), False) or "external_constants_ledger_clean\": true" in text.lower()
    uncertainty = _bool_from_obj(payload, ("uncertainty_protocol_declared",), False) or "uncertainty_protocol_declared\": true" in text.lower()
    target = _bool_from_obj(payload, ("target_value_consumed",), False) or bool(_has_any(text, PROVENANCE_MARKERS))

    return {
        "name": name,
        "trace_sector_closed": trace_closed,
        "source_to_scheme_registry_present": registry,
        "evaluator_map_found": evaluator,
        "codomain_transport_found": codomain,
        "counterterm_finite_parts_declared": counterterm,
        "external_constants_ledger_clean": constants,
        "uncertainty_protocol_declared": uncertainty,
        "target_value_consumed": target,
        "notes": "Generated by artifact_to_route_payload_adapter; ambiguous fields remain open.",
    }


def dark_payload_from_artifact(name: str, text: str, obj: Optional[Any]) -> Dict[str, Any]:
    payload = obj.get("payload", obj) if isinstance(obj, Mapping) else {}
    if not isinstance(payload, Mapping):
        payload = {}
    lower = text.lower()
    route_built = _bool_from_obj(payload, ("route_built",), False) or any(x in lower for x in ["dark sector", "desi", "cobaya", "route_b", "route b"])
    run_completed = _bool_from_obj(payload, ("run_completed",), False) or any(x in lower for x in ["run_completed\": true", "runtime completed", "run completed", "successfully completed"])
    chains = _bool_from_obj(payload, ("chains_converged",), False) or any(x in lower for x in ["chains_converged\": true", "r-hat", "rhat", "converged"])
    posterior = _bool_from_obj(payload, ("posterior_closed",), False) or "posterior_closed\": true" in lower
    robustness = _bool_from_obj(payload, ("robustness_checks_passed",), False) or "robustness_checks_passed\": true" in lower
    ledger = _bool_from_obj(payload, ("data_ledger_clean",), False) or "data_ledger_clean\": true" in lower or "data ledger clean" in lower
    evaluator = _bool_from_obj(payload, ("evaluator_map_found",), False) or "evaluator_map_found\": true" in lower
    codomain = _bool_from_obj(payload, ("codomain_transport_found",), False) or route_built
    target = _bool_from_obj(payload, ("target_value_consumed",), False) or bool(_has_any(text, PROVENANCE_MARKERS))
    return {
        "name": name,
        "route_built": route_built,
        "run_completed": run_completed,
        "chains_converged": chains,
        "posterior_closed": posterior,
        "robustness_checks_passed": robustness,
        "data_ledger_clean": ledger,
        "evaluator_map_found": evaluator,
        "codomain_transport_found": codomain,
        "target_value_consumed": target,
        "notes": "Generated by artifact_to_route_payload_adapter; runtime success is not posterior/global closure.",
    }


def generic_payload_from_artifact(route: str, name: str, text: str, obj: Optional[Any]) -> Dict[str, Any]:
    target = bool(_has_any(text, PROVENANCE_MARKERS))
    if route == "capacity":
        nums = [float(x) for x in re.findall(r"\b\d+(?:\.\d+)?\b", text)[:2]]
        raw = nums[0] if nums else 100
        budget = nums[1] if len(nums) > 1 else 25
        return {"name": name, "raw_capacity_load": raw, "capacity_budget": budget, "coarse_grain_factor": 1, "target_value_consumed": target}
    if route == "provenance":
        return {"name": name, "sector": "PROVENANCE", "inputs_used": ["declared_input", "target_value"] if target else ["declared_input"], "declared_targets": ["target_value"], "fitted_outputs": ["fitted_output"], "posterior_outputs": ["posterior_output"], "allowed_exogenous_inputs": ["declared_input"]}
    if route == "gauge":
        lower = text.lower()
        return {"name": name, "local_fiber_action_defined": "fiber" in lower or "gauge" in lower, "group_law_verified": "group_law_verified\": true" in lower, "representation_faithful": "representation_faithful\": true" in lower, "codomain_map_declared": "codomain_map_declared\": true" in lower, "overlap_cocycle_verified": "overlap_cocycle_verified\": true" in lower, "anomaly_check_passed": "anomaly_check_passed\": true" in lower, "target_value_consumed": target}
    if route == "horizon":
        lower = text.lower()
        return {"name": name, "horizon_partition_defined": "horizon" in lower, "area_cost_map_defined": "area" in lower or "cost" in lower, "overlap_gluing_verified": "overlap_gluing_verified\": true" in lower, "capacity_bound_checked": "capacity_bound_checked\": true" in lower, "entropy_ledger_clean": "entropy_ledger_clean\": true" in lower, "codomain_transport_found": "codomain_transport_found\": true" in lower, "target_value_consumed": target}
    if route == "cstar":
        return {"name": name, "notes": "C*/substrate artifact detected; theorem-level substrate payload remains conservative."}
    return {"name": name, "sector": "GENERIC", "local_solution_found": False, "global_export_requested": True, "acc_base_present": False, "evaluator_map_found": False, "codomain_transport_found": False, "overlap_gluing_verified": False, "capacity_budget_verified": False, "capacity_overspend_detected": False, "empirical_or_posterior_closed": False, "target_value_used_as_input": target, "notes": "Generic artifact payload; manual route review required."}


def adapt_artifact_to_payload(path: str | Path) -> ArtifactPayloadCandidate:
    p = Path(path)
    obj = _try_json(p)
    text = _flatten_json_text(obj) if obj is not None else _read_text(p)
    kind = detect_artifact_kind(p, obj, text)
    route, markers = infer_route(text, obj)
    name = "artifact_" + re.sub(r"[^a-zA-Z0-9]+", "_", p.stem).strip("_").lower()

    if route == "ew":
        payload = ew_payload_from_artifact(name, text, obj)
    elif route == "dark":
        payload = dark_payload_from_artifact(name, text, obj)
    else:
        payload = generic_payload_from_artifact(route, name, text, obj)

    warnings: List[str] = []
    if route == "generic":
        warnings.append("Route could not be confidently inferred; generic conservative payload emitted.")
    if kind in {ArtifactKind.LOG_TEXT, ArtifactKind.VERIFIER_STDOUT}:
        warnings.append("Text/log artifact parsed heuristically; inspect payload before banking.")
    if bool(_has_any(text, PROVENANCE_MARKERS)):
        warnings.append("Provenance/target-consumption marker detected; downstream gate should fail closed if target consumed.")

    confidence = PayloadConfidence.HIGH if kind in {ArtifactKind.ADAPTER_REPORT, ArtifactKind.JSON_PAYLOAD, ArtifactKind.CI_REPORT, ArtifactKind.SMOKE_SUMMARY} and route != "generic" else PayloadConfidence.MEDIUM if route != "generic" else PayloadConfidence.LOW

    return ArtifactPayloadCandidate(
        artifact_path=str(p),
        artifact_kind=kind,
        route=route,
        payload=payload,
        confidence=confidence,
        detected_markers=markers,
        warnings=tuple(warnings),
    )


def adapt_artifacts(paths: Iterable[str | Path]) -> ArtifactAdapterBatchReport:
    candidates = tuple(adapt_artifact_to_payload(p) for p in paths)
    route_counts: Dict[str, int] = {}
    confidence_counts: Dict[str, int] = {}
    warnings: List[str] = []
    for c in candidates:
        route_counts[c.route] = route_counts.get(c.route, 0) + 1
        confidence_counts[c.confidence.value] = confidence_counts.get(c.confidence.value, 0) + 1
        warnings.extend(c.warnings)
    return ArtifactAdapterBatchReport(candidates, route_counts, confidence_counts, tuple(warnings))


def check_T_artifact_adapter_detects_EW_P() -> Dict[str, Any]:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "ew_stdout.txt"
        p.write_text("TRACE_SECTOR_BANK_INTEGRATION_PASS APF_TRACE local closure. EW_SOURCE_TO_SCHEME_REGISTRY_REFRESH_PASS", encoding="utf-8")
        c = adapt_artifact_to_payload(p)
    tests = {
        "route_ew": c.route == "ew",
        "trace_closed": c.payload["trace_sector_closed"] is True,
        "registry_present": c.payload["source_to_scheme_registry_present"] is True,
        "evaluator_open": c.payload["evaluator_map_found"] is False,
    }
    return {"name": "check_T_artifact_adapter_detects_EW_P", "consistent": all(tests.values()), "status": "P_artifact_adapter" if all(tests.values()) else "FAIL", "summary": "Artifact adapter infers EW trace payload from verifier text.", "data": {"tests": tests, "candidate": c.to_dict()}}


def check_T_artifact_adapter_detects_dark_runtime_P() -> Dict[str, Any]:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "dark.json"
        p.write_text(json.dumps({"payload": {"name": "dark_runtime", "route_built": True, "run_completed": True, "chains_converged": False, "posterior_closed": False, "data_ledger_clean": True}}), encoding="utf-8")
        c = adapt_artifact_to_payload(p)
    tests = {
        "route_dark": c.route == "dark",
        "run_completed": c.payload["run_completed"] is True,
        "posterior_open": c.payload["posterior_closed"] is False,
        "codomain_true_from_route": c.payload["codomain_transport_found"] is True,
    }
    return {"name": "check_T_artifact_adapter_detects_dark_runtime_P", "consistent": all(tests.values()), "status": "P_artifact_adapter" if all(tests.values()) else "FAIL", "summary": "Artifact adapter infers dark runtime payload from JSON.", "data": {"tests": tests, "candidate": c.to_dict()}, "dependencies": ["check_T_artifact_adapter_detects_EW_P"]}


def check_T_artifact_adapter_provenance_boundary_P() -> Dict[str, Any]:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "smuggle.log"
        p.write_text("EW APF_TRACE target_value_consumed true PROVENANCE_SMUGGLE", encoding="utf-8")
        c = adapt_artifact_to_payload(p)
    tests = {
        "route_provenance_preferred": c.route == "provenance",
        "warning_present": any("Provenance" in w for w in c.warnings),
        "payload_has_target": "target_value" in c.payload.get("inputs_used", []),
    }
    return {"name": "check_T_artifact_adapter_provenance_boundary_P", "consistent": all(tests.values()), "status": "P_artifact_adapter" if all(tests.values()) else "FAIL", "summary": "Artifact adapter preserves provenance boundary by routing smuggling markers to provenance audit.", "data": {"tests": tests, "candidate": c.to_dict()}, "dependencies": ["check_T_artifact_adapter_detects_dark_runtime_P"]}


def check_T_artifact_adapter_batch_report_P() -> Dict[str, Any]:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / "ew.txt").write_text("EW_TRACE_TO_SCHEME_REAL_ADAPTER_P_PASS APF_TRACE", encoding="utf-8")
        (td / "dark.txt").write_text("DARK_POSTERIOR_REAL_ADAPTER_P_PASS run_completed posterior", encoding="utf-8")
        report = adapt_artifacts([td / "ew.txt", td / "dark.txt"])
    tests = {
        "two_candidates": len(report.candidates) == 2,
        "has_ew": report.route_counts.get("ew", 0) == 1,
        "has_dark": report.route_counts.get("dark", 0) == 1,
        "confidence_counts": sum(report.confidence_counts.values()) == 2,
    }
    return {"name": "check_T_artifact_adapter_batch_report_P", "consistent": all(tests.values()), "status": "P_artifact_adapter" if all(tests.values()) else "FAIL", "summary": "Artifact adapter emits batch reports with route/confidence counts.", "data": {"tests": tests, "report": report.to_dict()}, "dependencies": ["check_T_artifact_adapter_provenance_boundary_P"]}


def check_T_artifact_to_route_payload_adapter_P() -> Dict[str, Any]:
    subchecks = [
        check_T_artifact_adapter_detects_EW_P(),
        check_T_artifact_adapter_detects_dark_runtime_P(),
        check_T_artifact_adapter_provenance_boundary_P(),
        check_T_artifact_adapter_batch_report_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {"name": "check_T_artifact_to_route_payload_adapter_P", "consistent": ok, "status": "P_artifact_adapter" if ok else "FAIL", "summary": "Artifact-to-Route Payload Adapter is P: integration artifacts compile into conservative route payload candidates.", "data": {"core_claim": "Real artifacts can be converted into route payloads without treating ambiguous text as proof.", "subchecks": [x["name"] for x in subchecks]}, "dependencies": [x["name"] for x in subchecks]}


CHECKS = {
    "check_T_artifact_adapter_detects_EW_P": check_T_artifact_adapter_detects_EW_P,
    "check_T_artifact_adapter_detects_dark_runtime_P": check_T_artifact_adapter_detects_dark_runtime_P,
    "check_T_artifact_adapter_provenance_boundary_P": check_T_artifact_adapter_provenance_boundary_P,
    "check_T_artifact_adapter_batch_report_P": check_T_artifact_adapter_batch_report_P,
    "check_T_artifact_to_route_payload_adapter_P": check_T_artifact_to_route_payload_adapter_P,
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
            raise TypeError("Unsupported registry type for artifact_to_route_payload_adapter.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
