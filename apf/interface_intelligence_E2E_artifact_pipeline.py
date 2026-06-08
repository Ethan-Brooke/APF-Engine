"""
APF Interface Intelligence E2E Artifact Pipeline.

Purpose
-------
One end-to-end engineering runner over real integration artifacts:

    artifact folder/files
      -> artifact-to-payload candidates
      -> payload batch certification
      -> atlas/batch reports
      -> reviewer markdown/JSON
      -> zipped E2E report bundle

Boundary
--------
This pipeline automates diagnostics and reporting. It does not validate artifact truth or
promote held physics claims to P.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List
import json
import zipfile
import datetime

from apf.artifact_to_route_payload_adapter import adapt_artifacts
from apf.payload_batch_certification_runner import load_payload_items_from_candidates, run_payload_batch, write_payload_batch_outputs
from apf.interface_intelligence_reviewer_reporter import write_reviewer_report


@dataclass(frozen=True)
class E2EArtifactPipelineReport:
    created_utc: str
    inputs: Tuple[str, ...]
    out_dir: str
    artifact_candidates_path: str
    payload_dir: str
    batch_out_dir: str
    reviewer_markdown_path: str
    reviewer_json_path: str
    zip_path: Optional[str]
    artifact_route_counts: Mapping[str, int]
    artifact_confidence_counts: Mapping[str, int]
    batch_status_counts: Mapping[str, int]
    batch_route_counts: Mapping[str, int]
    overall_pass: bool
    note: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "created_utc": self.created_utc,
            "inputs": list(self.inputs),
            "out_dir": self.out_dir,
            "artifact_candidates_path": self.artifact_candidates_path,
            "payload_dir": self.payload_dir,
            "batch_out_dir": self.batch_out_dir,
            "reviewer_markdown_path": self.reviewer_markdown_path,
            "reviewer_json_path": self.reviewer_json_path,
            "zip_path": self.zip_path,
            "artifact_route_counts": dict(self.artifact_route_counts),
            "artifact_confidence_counts": dict(self.artifact_confidence_counts),
            "batch_status_counts": dict(self.batch_status_counts),
            "batch_route_counts": dict(self.batch_route_counts),
            "overall_pass": self.overall_pass,
            "note": self.note,
        }


DEFAULT_EXTENSIONS = {".json", ".txt", ".log", ".out", ".stdout", ".stderr", ".md"}


def collect_artifact_files(paths: Iterable[str | Path], *, recursive: bool = True, extensions: Optional[Iterable[str]] = None) -> Tuple[Path, ...]:
    exts = {e.lower() if str(e).startswith(".") else "." + str(e).lower() for e in (extensions or DEFAULT_EXTENSIONS)}
    out: List[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_file() and p.suffix.lower() in exts:
            out.append(p)
        elif p.is_dir():
            iterator = p.rglob("*") if recursive else p.glob("*")
            for q in iterator:
                if q.is_file() and q.suffix.lower() in exts:
                    out.append(q)
    # deterministic, de-duplicated
    seen = set()
    result = []
    for p in sorted(out, key=lambda x: str(x)):
        rp = str(p.resolve())
        if rp not in seen:
            seen.add(rp)
            result.append(p)
    return tuple(result)


def _write_payload_files(candidates_report: Mapping[str, Any], payload_dir: Path) -> Tuple[str, ...]:
    payload_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for idx, cand in enumerate(candidates_report.get("candidates", [])):
        route = cand.get("route", "generic")
        name = cand.get("payload", {}).get("name", f"payload_{idx:03d}")
        safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in f"{idx:03d}_{route}_{name}")
        path = payload_dir / f"{safe}.payload.json"
        path.write_text(json.dumps(cand.get("payload", {}), indent=2, sort_keys=True), encoding="utf-8")
        written.append(str(path))
    return tuple(written)


def _zip_dir(out_dir: Path) -> str:
    zip_path = out_dir.parent / f"{out_dir.name}.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in out_dir.rglob("*"):
            z.write(p, p.relative_to(out_dir.parent))
    return str(zip_path)


def run_e2e_artifact_pipeline(
    inputs: Iterable[str | Path],
    out_dir: str | Path = "interface_intelligence_e2e_artifact_pipeline",
    *,
    recursive: bool = True,
    zip_outputs: bool = True,
) -> E2EArtifactPipelineReport:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    artifact_files = collect_artifact_files(inputs, recursive=recursive)
    if not artifact_files:
        # still emit structured empty report
        report = E2EArtifactPipelineReport(
            created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            inputs=tuple(str(p) for p in inputs),
            out_dir=str(out),
            artifact_candidates_path=str(out / "artifact_payload_candidates.json"),
            payload_dir=str(out / "payloads"),
            batch_out_dir=str(out / "payload_batch"),
            reviewer_markdown_path=str(out / "interface_reviewer_report.md"),
            reviewer_json_path=str(out / "interface_reviewer_report.json"),
            zip_path=None,
            artifact_route_counts={},
            artifact_confidence_counts={},
            batch_status_counts={},
            batch_route_counts={},
            overall_pass=False,
            note="No artifact files found; no claims promoted.",
        )
        (out / "e2e_artifact_pipeline_report.json").write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
        (out / "e2e_artifact_pipeline_summary.md").write_text(render_e2e_summary(report), encoding="utf-8")
        if zip_outputs:
            report = E2EArtifactPipelineReport(**{**report.to_dict(), "inputs": report.inputs, "zip_path": _zip_dir(out)})
        return report

    candidates = adapt_artifacts(artifact_files)
    candidates_path = out / "artifact_payload_candidates.json"
    candidates_path.write_text(json.dumps(candidates.to_dict(), indent=2, sort_keys=True), encoding="utf-8")

    payload_dir = out / "payloads"
    _write_payload_files(candidates.to_dict(), payload_dir)

    items = load_payload_items_from_candidates(candidates_path)
    batch = run_payload_batch(items, include_atlas=True)
    batch_out = out / "payload_batch"
    batch_info = write_payload_batch_outputs(batch, batch_out, zip_outputs=False)

    reviewer_md = out / "interface_reviewer_report.md"
    reviewer_json = out / "interface_reviewer_report.json"
    reviewer_inputs = [batch_out / "payload_batch_report.json"]
    if (batch_out / "payload_batch_atlas.json").exists():
        reviewer_inputs.append(batch_out / "payload_batch_atlas.json")
    write_reviewer_report(reviewer_inputs, reviewer_md, reviewer_json, title="APF Interface Intelligence E2E Artifact Pipeline Report")

    overall_pass = True  # pipeline ran; statuses may still be HELD/FAIL_CLOSED by design.
    report = E2EArtifactPipelineReport(
        created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        inputs=tuple(str(p) for p in artifact_files),
        out_dir=str(out),
        artifact_candidates_path=str(candidates_path),
        payload_dir=str(payload_dir),
        batch_out_dir=str(batch_out),
        reviewer_markdown_path=str(reviewer_md),
        reviewer_json_path=str(reviewer_json),
        zip_path=None,
        artifact_route_counts=candidates.route_counts,
        artifact_confidence_counts=candidates.confidence_counts,
        batch_status_counts=batch.status_counts,
        batch_route_counts=batch.route_counts,
        overall_pass=overall_pass,
        note="Pipeline pass means diagnostics completed; route statuses remain governed by certificates.",
    )
    (out / "e2e_artifact_pipeline_report.json").write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    (out / "e2e_artifact_pipeline_summary.md").write_text(render_e2e_summary(report), encoding="utf-8")
    if zip_outputs:
        zip_path = _zip_dir(out)
        report = E2EArtifactPipelineReport(**{**report.to_dict(), "inputs": report.inputs, "zip_path": zip_path})
        (out / "e2e_artifact_pipeline_report.json").write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
        (out / "e2e_artifact_pipeline_summary.md").write_text(render_e2e_summary(report), encoding="utf-8")
    return report


def render_e2e_summary(report: E2EArtifactPipelineReport) -> str:
    lines = [
        "# APF Interface Intelligence E2E Artifact Pipeline Summary",
        "",
        f"- Created UTC: `{report.created_utc}`",
        f"- Overall pipeline pass: `{report.overall_pass}`",
        f"- Input artifacts: `{len(report.inputs)}`",
        f"- Output directory: `{report.out_dir}`",
        f"- Zip: `{report.zip_path}`",
        "",
        "## Artifact route counts",
        "",
    ]
    for k, v in sorted(report.artifact_route_counts.items()):
        lines.append(f"- `{k}`: {v}")
    if not report.artifact_route_counts:
        lines.append("- none")
    lines += ["", "## Payload batch status counts", ""]
    for k, v in sorted(report.batch_status_counts.items()):
        lines.append(f"- **{k}**: {v}")
    if not report.batch_status_counts:
        lines.append("- none")
    lines += [
        "",
        "## Key outputs",
        "",
        f"- Candidates: `{report.artifact_candidates_path}`",
        f"- Payloads: `{report.payload_dir}`",
        f"- Batch reports: `{report.batch_out_dir}`",
        f"- Reviewer markdown: `{report.reviewer_markdown_path}`",
        f"- Reviewer JSON: `{report.reviewer_json_path}`",
        "",
        "## Boundary",
        "",
        "This pipeline automates diagnostics and reporting. It does not validate artifact truth or promote held physics claims to P.",
    ]
    return "\n".join(lines) + "\n"


def canonical_test_artifacts(tmp: Path) -> Tuple[Path, ...]:
    ew = tmp / "ew_trace_stdout.txt"
    ew.write_text("TRACE_SECTOR_BANK_INTEGRATION_PASS APF_TRACE local closure EW_SOURCE_TO_SCHEME_REGISTRY_REFRESH_PASS", encoding="utf-8")
    dark = tmp / "dark_runtime.json"
    dark.write_text(json.dumps({"payload": {"name": "dark_runtime", "route_built": True, "run_completed": True, "data_ledger_clean": True}}), encoding="utf-8")
    return ew, dark


def check_T_e2e_artifact_pipeline_collects_files_P() -> Dict[str, Any]:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        artifacts = canonical_test_artifacts(td)
        files = collect_artifact_files([td])
    tests = {
        "finds_two": len(files) == 2,
        "includes_json": any(p.suffix == ".json" for p in files),
        "includes_txt": any(p.suffix == ".txt" for p in files),
    }
    return {"name": "check_T_e2e_artifact_pipeline_collects_files_P", "consistent": all(tests.values()), "status": "P_e2e_pipeline" if all(tests.values()) else "FAIL", "summary": "E2E pipeline collects artifact files deterministically.", "data": {"tests": tests}}


def check_T_e2e_artifact_pipeline_runs_P() -> Dict[str, Any]:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        canonical_test_artifacts(td)
        report = run_e2e_artifact_pipeline([td], td / "out", zip_outputs=True)
        out = Path(report.out_dir)
        tests = {
            "overall_pass": report.overall_pass is True,
            "candidates_exists": Path(report.artifact_candidates_path).exists(),
            "batch_report_exists": (Path(report.batch_out_dir) / "payload_batch_report.json").exists(),
            "reviewer_md_exists": Path(report.reviewer_markdown_path).exists(),
            "zip_exists": Path(report.zip_path).exists(),
            "has_ew": report.artifact_route_counts.get("ew", 0) >= 1,
            "has_dark": report.artifact_route_counts.get("dark", 0) >= 1,
        }
    return {"name": "check_T_e2e_artifact_pipeline_runs_P", "consistent": all(tests.values()), "status": "P_e2e_pipeline" if all(tests.values()) else "FAIL", "summary": "E2E artifact pipeline produces candidates, batch certification, reviewer report, and zip.", "data": {"tests": tests}, "dependencies": ["check_T_e2e_artifact_pipeline_collects_files_P"]}


def check_T_e2e_artifact_pipeline_empty_safe_P() -> Dict[str, Any]:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        report = run_e2e_artifact_pipeline([td], td / "out", zip_outputs=False)
        tests = {
            "overall_false": report.overall_pass is False,
            "no_artifact_route_counts": report.artifact_route_counts == {},
            "summary_written": (Path(report.out_dir) / "e2e_artifact_pipeline_report.json").exists(),
            "note_boundary": "No artifact" in report.note,
        }
    return {"name": "check_T_e2e_artifact_pipeline_empty_safe_P", "consistent": all(tests.values()), "status": "P_e2e_pipeline" if all(tests.values()) else "FAIL", "summary": "E2E pipeline handles empty artifact folders without overclaiming.", "data": {"tests": tests}, "dependencies": ["check_T_e2e_artifact_pipeline_runs_P"]}


def check_T_interface_intelligence_E2E_artifact_pipeline_P() -> Dict[str, Any]:
    subchecks = [
        check_T_e2e_artifact_pipeline_collects_files_P(),
        check_T_e2e_artifact_pipeline_runs_P(),
        check_T_e2e_artifact_pipeline_empty_safe_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {"name": "check_T_interface_intelligence_E2E_artifact_pipeline_P", "consistent": ok, "status": "P_e2e_artifact_pipeline" if ok else "FAIL", "summary": "Interface Intelligence E2E Artifact Pipeline is P: artifact folders become payloads, batch certifications, reviewer reports, and zipped diagnostics.", "data": {"core_claim": "End-to-end artifact diagnostics can run without validating artifact truth or promoting held claims.", "subchecks": [x["name"] for x in subchecks]}, "dependencies": [x["name"] for x in subchecks]}


CHECKS = {
    "check_T_e2e_artifact_pipeline_collects_files_P": check_T_e2e_artifact_pipeline_collects_files_P,
    "check_T_e2e_artifact_pipeline_runs_P": check_T_e2e_artifact_pipeline_runs_P,
    "check_T_e2e_artifact_pipeline_empty_safe_P": check_T_e2e_artifact_pipeline_empty_safe_P,
    "check_T_interface_intelligence_E2E_artifact_pipeline_P": check_T_interface_intelligence_E2E_artifact_pipeline_P,
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
            raise TypeError("Unsupported registry type for interface_intelligence_E2E_artifact_pipeline.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
