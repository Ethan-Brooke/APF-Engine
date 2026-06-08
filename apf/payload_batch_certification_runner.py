"""
APF Payload Batch Certification Runner.

Purpose
-------
Run interface-intelligence certification over many route payloads.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List
import json
import zipfile
import datetime

from apf.interface_structure_discovery_engine import discover_and_certify
from apf.interface_structure_movement_graph import movement_graph_report
from apf.interface_repair_frontier_explorer import explore_repair_frontier
from apf.interface_repair_obligation_compiler import compile_obligation_packet, evidence_template
from apf.interface_evidence_rerun_controller import control_evidence_rerun
from apf.interface_atlas import AtlasInput, AtlasInputKind, build_interface_atlas


class BatchItemStatus(str, Enum):
    CERTIFIED_GLOBAL_P = "CERTIFIED_GLOBAL_P"
    HELD_FOR_REPAIR = "HELD_FOR_REPAIR"
    FAIL_CLOSED_PROVENANCE = "FAIL_CLOSED_PROVENANCE"
    STRUCTURAL_BLOCK = "STRUCTURAL_BLOCK"
    UNSUPPORTED_OR_FAILED = "UNSUPPORTED_OR_FAILED"


@dataclass(frozen=True)
class PayloadBatchItem:
    item_id: str
    route: str
    payload: Mapping[str, Any]
    source: str = "manual"

    def to_dict(self) -> Dict[str, Any]:
        return {"item_id": self.item_id, "route": self.route, "payload": dict(self.payload), "source": self.source}


@dataclass(frozen=True)
class PayloadBatchResult:
    item: PayloadBatchItem
    status: BatchItemStatus
    certification: Mapping[str, Any]
    movement_graph: Mapping[str, Any]
    frontier: Mapping[str, Any]
    obligation_packet: Mapping[str, Any]
    evidence_template: Mapping[str, Any]
    rerun_without_evidence: Mapping[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "item": self.item.to_dict(),
            "status": self.status.value,
            "certification": dict(self.certification),
            "movement_graph": dict(self.movement_graph),
            "frontier": dict(self.frontier),
            "obligation_packet": dict(self.obligation_packet),
            "evidence_template": dict(self.evidence_template),
            "rerun_without_evidence": dict(self.rerun_without_evidence),
        }


@dataclass(frozen=True)
class PayloadBatchReport:
    created_utc: str
    results: Tuple[PayloadBatchResult, ...]
    status_counts: Mapping[str, int]
    route_counts: Mapping[str, int]
    atlas: Optional[Mapping[str, Any]]
    note: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "created_utc": self.created_utc,
            "results": [r.to_dict() for r in self.results],
            "status_counts": dict(self.status_counts),
            "route_counts": dict(self.route_counts),
            "atlas": dict(self.atlas) if self.atlas is not None else None,
            "note": self.note,
        }


def _cert(report: Mapping[str, Any]) -> Mapping[str, Any]:
    return report.get("ledger_certificate", {}).get("certificate", report.get("certificate", {}))


def classify_batch_status(cert: Mapping[str, Any], packet: Mapping[str, Any], frontier: Mapping[str, Any]) -> BatchItemStatus:
    solver = str(cert.get("solver_status", ""))
    obstruction = tuple(cert.get("obstruction", ()))
    packet_status = str(packet.get("packet_status", ""))
    frontier_status = str(frontier.get("frontier_status", ""))
    if cert.get("export_global_P") is True or solver == "SOLVED_GLOBAL_P":
        return BatchItemStatus.CERTIFIED_GLOBAL_P
    if solver == "FAIL_CLOSED_PROVENANCE" or "PROVENANCE_SMUGGLE" in obstruction or packet_status == "BLOCKED_PROVENANCE_REBUILD_REQUIRED":
        return BatchItemStatus.FAIL_CLOSED_PROVENANCE
    if packet_status == "BLOCKED_SUBSTRATE_THEOREM_REQUIRED" or frontier_status == "REFUSE_SUBSTRATE_FRONTIER" or "STRUCTURAL_BLOCKER" in obstruction:
        return BatchItemStatus.STRUCTURAL_BLOCK
    if solver == "SOLVED_LOCAL_HELD_FOR_REPAIR" or packet_status == "OPEN_EVIDENCE_REQUIRED":
        return BatchItemStatus.HELD_FOR_REPAIR
    return BatchItemStatus.UNSUPPORTED_OR_FAILED


def certify_payload_item(item: PayloadBatchItem) -> PayloadBatchResult:
    certification = discover_and_certify(item.route, item.payload)
    movement = movement_graph_report(item.route, item.payload)
    frontier = explore_repair_frontier(item.route, item.payload).to_dict()
    packet_obj = compile_obligation_packet(item.route, item.payload)
    packet = packet_obj.to_dict()
    template = evidence_template(packet_obj)
    rerun = control_evidence_rerun(item.route, item.payload).to_dict()
    cert = _cert(certification)
    status = classify_batch_status(cert, packet, frontier)
    return PayloadBatchResult(item, status, certification, movement, frontier, packet, template, rerun)


def load_payload_items_from_candidates(path: str | Path) -> Tuple[PayloadBatchItem, ...]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    candidates = data.get("candidates", data)
    items: List[PayloadBatchItem] = []
    for idx, cand in enumerate(candidates):
        route = cand.get("route", "generic")
        payload = cand.get("payload", {})
        source = cand.get("artifact_path", cand.get("source", "candidate"))
        item_id = cand.get("item_id", f"candidate_{idx:03d}_{route}_{payload.get('name', 'payload')}")
        items.append(PayloadBatchItem(item_id=item_id, route=route, payload=payload, source=source))
    return tuple(items)


def load_payload_items_from_payload_files(paths: Iterable[str | Path], *, route: Optional[str] = None) -> Tuple[PayloadBatchItem, ...]:
    items: List[PayloadBatchItem] = []
    for idx, path in enumerate(paths):
        p = Path(path)
        payload = json.loads(p.read_text(encoding="utf-8"))
        inferred_route = route
        if inferred_route is None:
            name = str(payload.get("name", p.stem)).lower()
            if "ew" in name or "trace" in name:
                inferred_route = "ew"
            elif "dark" in name or "posterior" in name:
                inferred_route = "dark"
            elif "capacity" in name:
                inferred_route = "capacity"
            elif "prov" in name:
                inferred_route = "provenance"
            else:
                inferred_route = str(payload.get("route", "generic"))
        items.append(PayloadBatchItem(item_id=f"payload_{idx:03d}_{p.stem}", route=inferred_route, payload=payload, source=str(p)))
    return tuple(items)


def build_atlas_from_results(results: Iterable[PayloadBatchResult]) -> Mapping[str, Any]:
    inputs = [AtlasInput(input_id=r.item.item_id, kind=AtlasInputKind.ROUTE_PAYLOAD, route=r.item.route, claim_text=None, payload=r.item.payload) for r in results]
    return build_interface_atlas(inputs, atlas_name="payload_batch_interface_atlas").to_dict()


def run_payload_batch(items: Iterable[PayloadBatchItem], *, include_atlas: bool = True) -> PayloadBatchReport:
    results = tuple(certify_payload_item(item) for item in items)
    status_counts: Dict[str, int] = {}
    route_counts: Dict[str, int] = {}
    for result in results:
        status_counts[result.status.value] = status_counts.get(result.status.value, 0) + 1
        route_counts[result.item.route] = route_counts.get(result.item.route, 0) + 1
    atlas = build_atlas_from_results(results) if include_atlas and results else None
    return PayloadBatchReport(datetime.datetime.now(datetime.timezone.utc).isoformat(), results, status_counts, route_counts, atlas, "Batch certification runs interface gates over payload candidates; it does not independently validate artifact truth.")


def render_batch_summary(report: PayloadBatchReport) -> str:
    lines = ["# APF Payload Batch Certification Summary", "", "## Counts", ""]
    for key, val in sorted(report.status_counts.items()):
        lines.append(f"- **{key}**: {val}")
    lines += ["", "## Routes", ""]
    for key, val in sorted(report.route_counts.items()):
        lines.append(f"- `{key}`: {val}")
    lines += ["", "## Items", "", "| Item | Route | Status | Source |", "|---|---|---|---|"]
    for result in report.results:
        lines.append(f"| `{result.item.item_id}` | `{result.item.route}` | `{result.status.value}` | `{result.item.source}` |")
    lines += ["", "## Boundary", "", "This batch certifies payload candidates through the interface gates. It does not independently validate artifact truth."]
    return "\n".join(lines) + "\n"


def write_payload_batch_outputs(report: PayloadBatchReport, out_dir: str | Path, *, zip_outputs: bool = True) -> Mapping[str, Any]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "payload_batch_report.json").write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    if report.atlas is not None:
        (out / "payload_batch_atlas.json").write_text(json.dumps(report.atlas, indent=2, sort_keys=True), encoding="utf-8")
    for result in report.results:
        safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in result.item.item_id)
        (out / f"{safe}.certification.json").write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
        (out / f"{safe}.evidence_template.json").write_text(json.dumps(result.evidence_template, indent=2, sort_keys=True), encoding="utf-8")
    (out / "payload_batch_summary.md").write_text(render_batch_summary(report), encoding="utf-8")
    zip_path = None
    if zip_outputs:
        zip_path = out.parent / f"{out.name}.zip"
        if zip_path.exists():
            zip_path.unlink()
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for p in out.rglob("*"):
                z.write(p, p.relative_to(out.parent))
    return {"out_dir": str(out), "zip_path": str(zip_path) if zip_path else None, "count": len(report.results)}


def canonical_items() -> Tuple[PayloadBatchItem, ...]:
    return (
        PayloadBatchItem("ew_open", "ew", {"name": "ew_open", "trace_sector_closed": True, "source_to_scheme_registry_present": True, "evaluator_map_found": False, "codomain_transport_found": False, "counterterm_finite_parts_declared": False, "external_constants_ledger_clean": True, "uncertainty_protocol_declared": False, "target_value_consumed": False}, "canonical"),
        PayloadBatchItem("dark_clean", "dark", {"name": "dark_clean", "route_built": True, "run_completed": True, "chains_converged": True, "posterior_closed": True, "robustness_checks_passed": True, "data_ledger_clean": True, "evaluator_map_found": True, "codomain_transport_found": True, "target_value_consumed": False}, "canonical"),
        PayloadBatchItem("prov_fail", "provenance", {"name": "prov_fail", "sector": "PROVENANCE", "inputs_used": ["declared_input", "target_value"], "declared_targets": ["target_value"], "fitted_outputs": ["fitted_output"], "posterior_outputs": ["posterior_output"], "allowed_exogenous_inputs": ["declared_input"]}, "canonical"),
    )


def check_T_payload_batch_runner_certifies_items_P() -> Dict[str, Any]:
    report = run_payload_batch(canonical_items(), include_atlas=True)
    tests = {"three_results": len(report.results) == 3, "has_held": report.status_counts.get("HELD_FOR_REPAIR", 0) == 1, "has_banked": report.status_counts.get("CERTIFIED_GLOBAL_P", 0) == 1, "has_provenance_fail": report.status_counts.get("FAIL_CLOSED_PROVENANCE", 0) == 1, "atlas_present": report.atlas is not None}
    return {"name": "check_T_payload_batch_runner_certifies_items_P", "consistent": all(tests.values()), "status": "P_payload_batch" if all(tests.values()) else "FAIL", "summary": "Payload batch runner certifies canonical held/P/provenance cases.", "data": {"tests": tests, "status_counts": report.status_counts}}


def check_T_payload_batch_runner_loads_candidates_P() -> Dict[str, Any]:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "candidates.json"
        p.write_text(json.dumps({"candidates": [{"route": "ew", "payload": {"name": "ew_candidate", "trace_sector_closed": True}, "artifact_path": "ew.txt"}, {"route": "dark", "payload": {"name": "dark_candidate", "route_built": True}, "artifact_path": "dark.txt"}]}), encoding="utf-8")
        items = load_payload_items_from_candidates(p)
    tests = {"two_items": len(items) == 2, "routes": {i.route for i in items} == {"ew", "dark"}, "sources_preserved": items[0].source == "ew.txt"}
    return {"name": "check_T_payload_batch_runner_loads_candidates_P", "consistent": all(tests.values()), "status": "P_payload_batch" if all(tests.values()) else "FAIL", "summary": "Payload batch runner loads artifact adapter candidate reports.", "data": {"tests": tests}, "dependencies": ["check_T_payload_batch_runner_certifies_items_P"]}


def check_T_payload_batch_runner_writes_outputs_P() -> Dict[str, Any]:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        report = run_payload_batch(canonical_items(), include_atlas=True)
        info = write_payload_batch_outputs(report, td / "out", zip_outputs=True)
        out = Path(info["out_dir"])
        tests = {"report_exists": (out / "payload_batch_report.json").exists(), "summary_exists": (out / "payload_batch_summary.md").exists(), "atlas_exists": (out / "payload_batch_atlas.json").exists(), "zip_exists": Path(info["zip_path"]).exists()}
    return {"name": "check_T_payload_batch_runner_writes_outputs_P", "consistent": all(tests.values()), "status": "P_payload_batch" if all(tests.values()) else "FAIL", "summary": "Payload batch runner writes report/atlas/templates and zips outputs.", "data": {"tests": tests}, "dependencies": ["check_T_payload_batch_runner_loads_candidates_P"]}


def check_T_payload_batch_certification_runner_P() -> Dict[str, Any]:
    subchecks = [check_T_payload_batch_runner_certifies_items_P(), check_T_payload_batch_runner_loads_candidates_P(), check_T_payload_batch_runner_writes_outputs_P()]
    ok = all(x["consistent"] for x in subchecks)
    return {"name": "check_T_payload_batch_certification_runner_P", "consistent": ok, "status": "P_payload_batch_runner" if ok else "FAIL", "summary": "Payload Batch Certification Runner is P: payload candidates batch-run through interface gates with atlas/report outputs.", "data": {"core_claim": "Many payload candidates can be certified, summarized, and zipped in one batch without overclaiming artifact truth.", "subchecks": [x["name"] for x in subchecks]}, "dependencies": [x["name"] for x in subchecks]}


CHECKS = {
    "check_T_payload_batch_runner_certifies_items_P": check_T_payload_batch_runner_certifies_items_P,
    "check_T_payload_batch_runner_loads_candidates_P": check_T_payload_batch_runner_loads_candidates_P,
    "check_T_payload_batch_runner_writes_outputs_P": check_T_payload_batch_runner_writes_outputs_P,
    "check_T_payload_batch_certification_runner_P": check_T_payload_batch_certification_runner_P,
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
            raise TypeError("Unsupported registry type for payload_batch_certification_runner.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
