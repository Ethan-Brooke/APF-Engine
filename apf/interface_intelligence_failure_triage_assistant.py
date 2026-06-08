"""
APF Interface Intelligence Failure Triage Assistant.

Purpose
-------
Read interface-intelligence reports and emit integrator-facing triage:

    live smoke / CI / E2E / payload batch / reviewer JSON
      -> first failing layer
      -> likely cause class
      -> exact next command / action
      -> boundary-safe remediation language

Boundary
--------
Triage explains software/report/evidence next steps. It does not repair physics claims or
promote held routes to P.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List
import json
import re


class TriageSeverity(str, Enum):
    OK = "OK"
    INFO = "INFO"
    ACTION = "ACTION"
    BLOCKER = "BLOCKER"


class TriageCause(str, Enum):
    NONE = "NONE"
    MISSING_SCRIPT = "MISSING_SCRIPT"
    IMPORT_FAILURE = "IMPORT_FAILURE"
    CI_FAILURE = "CI_FAILURE"
    REGISTRY_FAILURE = "REGISTRY_FAILURE"
    ARTIFACT_COLLECTION_EMPTY = "ARTIFACT_COLLECTION_EMPTY"
    HELD_FOR_REPAIR = "HELD_FOR_REPAIR"
    PROVENANCE_FAIL_CLOSED = "PROVENANCE_FAIL_CLOSED"
    STRUCTURAL_BLOCK = "STRUCTURAL_BLOCK"
    UNSUPPORTED_ROUTE = "UNSUPPORTED_ROUTE"
    UNKNOWN_FAILURE = "UNKNOWN_FAILURE"


@dataclass(frozen=True)
class TriageFinding:
    item_id: str
    severity: TriageSeverity
    cause: TriageCause
    summary: str
    next_action: str
    command: Optional[str]
    source: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["severity"] = self.severity.value
        d["cause"] = self.cause.value
        return d


@dataclass(frozen=True)
class TriageReport:
    created_utc: str
    findings: Tuple[TriageFinding, ...]
    first_blocker: Optional[TriageFinding]
    recommended_next_action: str
    markdown: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "created_utc": self.created_utc,
            "findings": [f.to_dict() for f in self.findings],
            "first_blocker": self.first_blocker.to_dict() if self.first_blocker else None,
            "recommended_next_action": self.recommended_next_action,
            "markdown": self.markdown,
        }


def _load_json(path: str | Path) -> Optional[Mapping[str, Any]]:
    try:
        obj = json.loads(Path(path).read_text(encoding="utf-8", errors="replace"))
        return obj if isinstance(obj, Mapping) else None
    except Exception:
        return None


def _read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8", errors="replace")


def _finding(item_id: str, severity: TriageSeverity, cause: TriageCause, summary: str, next_action: str, command: Optional[str], source: str) -> TriageFinding:
    return TriageFinding(item_id, severity, cause, summary, next_action, command, source)


def triage_smoke_summary(path: str | Path, obj: Mapping[str, Any]) -> Tuple[TriageFinding, ...]:
    findings: List[TriageFinding] = []
    source = str(path)
    if obj.get("overall_pass") is True:
        findings.append(_finding("live_smoke", TriageSeverity.OK, TriageCause.NONE, "Live smoke harness passed.", "Proceed to E2E artifact pipeline or reviewer report.", r'python .\scripts\run_interface_intelligence_E2E_artifact_pipeline.py --inputs .\interface_intelligence_live_smoke_reports --out-dir .\interface_intelligence_E2E_artifact_pipeline_reports', source))
        return tuple(findings)

    for step in obj.get("steps", []):
        if step.get("status") == "FAIL":
            note = str(step.get("note", ""))
            stderr_path = step.get("stderr_path")
            text = ""
            if stderr_path and Path(stderr_path).exists():
                try:
                    text = _read_text(stderr_path)
                except Exception:
                    text = ""
            cause = TriageCause.UNKNOWN_FAILURE
            action = "Inspect the step stdout/stderr and rerun the failing command."
            cmd = " ".join(step.get("command", [])) if step.get("command") else None
            if "missing script" in note.lower() or "missing script" in text.lower():
                cause = TriageCause.MISSING_SCRIPT
                action = "Install the missing package layer or rerun the 100% handoff install order before repeating live smoke."
            elif "import" in text.lower() or "modulenotfounderror" in text.lower():
                cause = TriageCause.IMPORT_FAILURE
                action = "Install prerequisite modules in order, then rerun the failing targeted verifier."
            findings.append(_finding(step.get("name", "smoke_step"), TriageSeverity.BLOCKER, cause, f"Live smoke step failed: {step.get('name')}; note={note}", action, cmd, source))
            break
    if not findings:
        findings.append(_finding("live_smoke", TriageSeverity.BLOCKER, TriageCause.UNKNOWN_FAILURE, "Live smoke failed but no failing step was found.", "Open the smoke summary and inspect raw logs.", None, source))
    return tuple(findings)


def triage_ci_report(path: str | Path, obj: Mapping[str, Any]) -> Tuple[TriageFinding, ...]:
    source = str(path)
    if obj.get("release_gate_pass") is True:
        return (_finding("ci", TriageSeverity.OK, TriageCause.NONE, "Interface-intelligence CI release gate passed.", "Proceed to artifact payload adaptation or E2E pipeline.", r'python .\scripts\run_interface_intelligence_E2E_artifact_pipeline.py --inputs .\interface_intelligence_live_smoke_reports --out-dir .\interface_intelligence_E2E_artifact_pipeline_reports', source),)
    for row in obj.get("module_results", []):
        if row.get("ci_status") != "PASS":
            cause = TriageCause.CI_FAILURE
            err = str(row.get("error") or "")
            if "import" in err.lower():
                cause = TriageCause.IMPORT_FAILURE
            return (_finding(
                row.get("module_name", "ci_module"),
                TriageSeverity.BLOCKER,
                cause,
                f"CI module failed: {row.get('module_name')} status={row.get('ci_status')} error={err[:220]}",
                "Run that module's targeted verifier first; fix import/check status before full CI.",
                f"python .\\scripts\\check_{str(row.get('module_name','')).split('.')[-1]}.py",
                source,
            ),)
    return (_finding("ci", TriageSeverity.BLOCKER, TriageCause.CI_FAILURE, str(obj.get("release_gate_reason", "CI failed.")), "Inspect module_results in the CI report.", None, source),)


def triage_e2e_report(path: str | Path, obj: Mapping[str, Any]) -> Tuple[TriageFinding, ...]:
    source = str(path)
    if obj.get("overall_pass") is False:
        note = str(obj.get("note", ""))
        if "No artifact" in note:
            return (_finding("e2e_artifacts", TriageSeverity.ACTION, TriageCause.ARTIFACT_COLLECTION_EMPTY, "E2E pipeline found no artifacts to process.", "Point the pipeline at live smoke reports, logs, reports, or adapter output JSONs.", r'python .\scripts\run_interface_intelligence_E2E_artifact_pipeline.py --inputs .\interface_intelligence_live_smoke_reports .\logs .\reports --out-dir .\interface_intelligence_E2E_artifact_pipeline_reports', source),)
        return (_finding("e2e", TriageSeverity.BLOCKER, TriageCause.UNKNOWN_FAILURE, "E2E pipeline did not complete successfully.", "Inspect e2e_artifact_pipeline_summary.md and raw stderr logs.", None, source),)
    findings = [_finding("e2e", TriageSeverity.OK, TriageCause.NONE, "E2E artifact pipeline completed.", "Review batch status counts and reviewer report; held/provenance statuses are route findings, not pipeline failure.", None, source)]
    status_counts = obj.get("batch_status_counts", {})
    if status_counts.get("FAIL_CLOSED_PROVENANCE", 0):
        findings.append(_finding("provenance", TriageSeverity.BLOCKER, TriageCause.PROVENANCE_FAIL_CLOSED, f"{status_counts.get('FAIL_CLOSED_PROVENANCE')} payload(s) fail-closed on provenance.", "Rebuild affected routes from clean inputs; do not patch evidence onto target-smuggled payloads.", None, source))
    if status_counts.get("STRUCTURAL_BLOCK", 0):
        findings.append(_finding("structural", TriageSeverity.BLOCKER, TriageCause.STRUCTURAL_BLOCK, f"{status_counts.get('STRUCTURAL_BLOCK')} payload(s) have structural blockers.", "Route to theorem/substrate work; ordinary evidence patching is insufficient.", None, source))
    if status_counts.get("HELD_FOR_REPAIR", 0):
        findings.append(_finding("held", TriageSeverity.ACTION, TriageCause.HELD_FOR_REPAIR, f"{status_counts.get('HELD_FOR_REPAIR')} payload(s) are held for repair.", "Open the payload_batch evidence templates and fill required fields, then rerun batch certification.", r'python .\scripts\run_payload_batch_certification.py --candidates .\artifact_payload_candidates.json --out-dir .\payload_batch_certification_reports', source))
    return tuple(findings)


def triage_payload_batch(path: str | Path, obj: Mapping[str, Any]) -> Tuple[TriageFinding, ...]:
    source = str(path)
    status_counts = obj.get("status_counts", {})
    findings: List[TriageFinding] = []
    if status_counts.get("CERTIFIED_GLOBAL_P", 0):
        findings.append(_finding("payload_batch_P", TriageSeverity.OK, TriageCause.NONE, f"{status_counts.get('CERTIFIED_GLOBAL_P')} payload(s) certified global P.", "Bank only if artifact provenance is accepted by live APF rules.", None, source))
    if status_counts.get("HELD_FOR_REPAIR", 0):
        findings.append(_finding("payload_batch_held", TriageSeverity.ACTION, TriageCause.HELD_FOR_REPAIR, f"{status_counts.get('HELD_FOR_REPAIR')} payload(s) held for repair.", "Fill evidence templates in the batch output folder and rerun the evidence/rerun gate.", None, source))
    if status_counts.get("FAIL_CLOSED_PROVENANCE", 0):
        findings.append(_finding("payload_batch_provenance", TriageSeverity.BLOCKER, TriageCause.PROVENANCE_FAIL_CLOSED, f"{status_counts.get('FAIL_CLOSED_PROVENANCE')} payload(s) fail-closed provenance.", "Clean rebuild required; do not repair by evidence patch.", None, source))
    if status_counts.get("STRUCTURAL_BLOCK", 0):
        findings.append(_finding("payload_batch_structural", TriageSeverity.BLOCKER, TriageCause.STRUCTURAL_BLOCK, f"{status_counts.get('STRUCTURAL_BLOCK')} payload(s) structurally blocked.", "Escalate to theorem/substrate route.", None, source))
    if not findings:
        findings.append(_finding("payload_batch", TriageSeverity.INFO, TriageCause.UNKNOWN_FAILURE, "Payload batch report has no recognized status counts.", "Inspect payload_batch_report.json.", None, source))
    return tuple(findings)


def triage_reviewer_report(path: str | Path, obj: Mapping[str, Any]) -> Tuple[TriageFinding, ...]:
    source = str(path)
    findings: List[TriageFinding] = []
    for row in obj.get("findings", []):
        status = row.get("status")
        if status == "HELD_FOR_REPAIR":
            findings.append(_finding(row.get("item_id", "held"), TriageSeverity.ACTION, TriageCause.HELD_FOR_REPAIR, row.get("summary", "Held for repair."), row.get("safe_language", "Supply evidence and rerun."), None, source))
        elif status == "FAIL_CLOSED_PROVENANCE":
            findings.append(_finding(row.get("item_id", "provenance"), TriageSeverity.BLOCKER, TriageCause.PROVENANCE_FAIL_CLOSED, row.get("summary", "Fail-closed provenance."), row.get("safe_language", "Clean rebuild required."), None, source))
        elif status == "STRUCTURAL_BLOCK":
            findings.append(_finding(row.get("item_id", "structural"), TriageSeverity.BLOCKER, TriageCause.STRUCTURAL_BLOCK, row.get("summary", "Structural block."), row.get("safe_language", "Theorem-level repair required."), None, source))
    if not findings:
        findings.append(_finding("reviewer", TriageSeverity.OK, TriageCause.NONE, "Reviewer report contains no held/provenance/structural findings.", "Proceed or inspect report manually.", None, source))
    return tuple(findings)


def triage_json_report(path: str | Path) -> Tuple[TriageFinding, ...]:
    obj = _load_json(path)
    if obj is None:
        text = _read_text(path)
        if "ModuleNotFoundError" in text or "ImportError" in text:
            return (_finding(Path(path).stem, TriageSeverity.BLOCKER, TriageCause.IMPORT_FAILURE, "Text log contains import failure.", "Install missing prerequisite or rerun pack install order.", None, str(path)),)
        if "missing script" in text.lower():
            return (_finding(Path(path).stem, TriageSeverity.BLOCKER, TriageCause.MISSING_SCRIPT, "Text log reports missing script.", "Install missing package layer.", None, str(path)),)
        return tuple()
    keys = set(obj)
    p = str(path).lower()
    if {"overall_pass", "steps", "report_zip"}.issubset(keys):
        return triage_smoke_summary(path, obj)
    if {"module_results", "release_gate_pass"}.issubset(keys):
        return triage_ci_report(path, obj)
    if {"artifact_candidates_path", "batch_status_counts", "overall_pass"}.issubset(keys):
        return triage_e2e_report(path, obj)
    if {"results", "status_counts", "route_counts"}.issubset(keys):
        return triage_payload_batch(path, obj)
    if {"findings", "overall_summary", "markdown"}.issubset(keys):
        return triage_reviewer_report(path, obj)
    return tuple()


def triage_reports(paths: Iterable[str | Path]) -> TriageReport:
    import datetime
    findings: List[TriageFinding] = []
    for path in paths:
        p = Path(path)
        if p.is_dir():
            for q in sorted(p.rglob("*")):
                if q.is_file() and q.suffix.lower() in {".json", ".txt", ".log", ".stderr", ".stdout"}:
                    findings.extend(triage_json_report(q))
        elif p.is_file():
            findings.extend(triage_json_report(p))
    if not findings:
        findings.append(_finding("triage", TriageSeverity.INFO, TriageCause.UNKNOWN_FAILURE, "No recognizable reports found.", "Run live smoke or E2E artifact pipeline first.", r'.\RUN_INTERFACE_INTELLIGENCE_LIVE_SMOKE.ps1', "input"))

    severity_rank = {TriageSeverity.BLOCKER: 3, TriageSeverity.ACTION: 2, TriageSeverity.INFO: 1, TriageSeverity.OK: 0}
    first_blocker = next((f for f in findings if f.severity == TriageSeverity.BLOCKER), None)
    if first_blocker:
        next_action = first_blocker.next_action
    else:
        action = next((f for f in findings if f.severity == TriageSeverity.ACTION), None)
        next_action = action.next_action if action else "No blockers found; proceed with integration/review."
    md = render_triage_markdown(findings, next_action)
    return TriageReport(
        created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        findings=tuple(findings),
        first_blocker=first_blocker,
        recommended_next_action=next_action,
        markdown=md,
    )


def render_triage_markdown(findings: Iterable[TriageFinding], next_action: str) -> str:
    findings = tuple(findings)
    counts: Dict[str, int] = {}
    for f in findings:
        counts[f.severity.value] = counts.get(f.severity.value, 0) + 1
    lines = [
        "# APF Interface Intelligence Failure Triage",
        "",
        f"## Recommended next action",
        "",
        next_action,
        "",
        "## Severity counts",
        "",
    ]
    for sev in TriageSeverity:
        if counts.get(sev.value, 0):
            lines.append(f"- **{sev.value}**: {counts[sev.value]}")
    lines += [
        "",
        "## Findings",
        "",
        "| Item | Severity | Cause | Summary | Next action | Command | Source |",
        "|---|---|---|---|---|---|---|",
    ]
    for f in findings:
        cmd = "`" + f.command + "`" if f.command else "—"
        lines.append(f"| `{f.item_id}` | `{f.severity.value}` | `{f.cause.value}` | {f.summary} | {f.next_action} | {cmd} | `{f.source}` |")
    lines += [
        "",
        "## Boundary",
        "",
        "This triage report identifies software/evidence next steps. It does not repair physics claims or promote held routes to P.",
    ]
    return "\n".join(lines) + "\n"


def write_triage_report(paths: Iterable[str | Path], out_md: str | Path, out_json: Optional[str | Path] = None) -> TriageReport:
    report = triage_reports(paths)
    Path(out_md).write_text(report.markdown, encoding="utf-8")
    if out_json:
        Path(out_json).write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return report


def canonical_reports(tmp: Path) -> Tuple[Path, ...]:
    smoke = tmp / "smoke.json"
    smoke.write_text(json.dumps({"overall_pass": False, "report_zip": None, "steps": [
        {"name": "check_interface_atlas", "status": "FAIL", "note": "missing script", "command": ["python", "scripts/check_interface_atlas.py"], "stderr_path": str(tmp/"missing.stderr.txt")}
    ]}), encoding="utf-8")
    (tmp/"missing.stderr.txt").write_text("missing script: scripts/check_interface_atlas.py", encoding="utf-8")
    e2e = tmp / "e2e.json"
    e2e.write_text(json.dumps({"overall_pass": True, "artifact_candidates_path": "x", "batch_status_counts": {"HELD_FOR_REPAIR": 2, "FAIL_CLOSED_PROVENANCE": 1}, "batch_route_counts": {"ew": 2}}), encoding="utf-8")
    return smoke, e2e


def check_T_failure_triage_detects_smoke_blocker_P() -> Dict[str, Any]:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        paths = canonical_reports(Path(td))
        report = triage_reports([paths[0]])
    tests = {
        "has_blocker": report.first_blocker is not None,
        "cause_missing_script": report.first_blocker.cause == TriageCause.MISSING_SCRIPT,
        "action_install": "Install" in report.recommended_next_action,
    }
    return {"name": "check_T_failure_triage_detects_smoke_blocker_P", "consistent": all(tests.values()), "status": "P_failure_triage" if all(tests.values()) else "FAIL", "summary": "Failure triage detects first missing-script smoke blocker.", "data": {"tests": tests}}


def check_T_failure_triage_detects_route_actions_P() -> Dict[str, Any]:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        paths = canonical_reports(Path(td))
        report = triage_reports([paths[1]])
    causes = {f.cause for f in report.findings}
    tests = {
        "has_provenance_blocker": TriageCause.PROVENANCE_FAIL_CLOSED in causes,
        "has_held_action": TriageCause.HELD_FOR_REPAIR in causes,
        "first_blocker_provenance": report.first_blocker is not None and report.first_blocker.cause == TriageCause.PROVENANCE_FAIL_CLOSED,
    }
    return {"name": "check_T_failure_triage_detects_route_actions_P", "consistent": all(tests.values()), "status": "P_failure_triage" if all(tests.values()) else "FAIL", "summary": "Failure triage detects held repair and provenance fail-closed route actions.", "data": {"tests": tests}, "dependencies": ["check_T_failure_triage_detects_smoke_blocker_P"]}


def check_T_failure_triage_markdown_P() -> Dict[str, Any]:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        paths = canonical_reports(Path(td))
        report = triage_reports(paths)
    tests = {
        "has_title": "# APF Interface Intelligence Failure Triage" in report.markdown,
        "has_boundary": "does not repair physics claims" in report.markdown,
        "has_table": "| Item | Severity | Cause |" in report.markdown,
        "has_next_action": "Recommended next action" in report.markdown,
    }
    return {"name": "check_T_failure_triage_markdown_P", "consistent": all(tests.values()), "status": "P_failure_triage" if all(tests.values()) else "FAIL", "summary": "Failure triage emits markdown with next action and boundary language.", "data": {"tests": tests}, "dependencies": ["check_T_failure_triage_detects_route_actions_P"]}


def check_T_interface_intelligence_failure_triage_assistant_P() -> Dict[str, Any]:
    subchecks = [
        check_T_failure_triage_detects_smoke_blocker_P(),
        check_T_failure_triage_detects_route_actions_P(),
        check_T_failure_triage_markdown_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {"name": "check_T_interface_intelligence_failure_triage_assistant_P", "consistent": ok, "status": "P_failure_triage" if ok else "FAIL", "summary": "Interface Intelligence Failure Triage Assistant is P: reports become prioritized next actions without overclaiming.", "data": {"core_claim": "The assistant identifies first blockers and evidence actions from integration reports while preserving physics-claim boundaries.", "subchecks": [x["name"] for x in subchecks]}, "dependencies": [x["name"] for x in subchecks]}


CHECKS = {
    "check_T_failure_triage_detects_smoke_blocker_P": check_T_failure_triage_detects_smoke_blocker_P,
    "check_T_failure_triage_detects_route_actions_P": check_T_failure_triage_detects_route_actions_P,
    "check_T_failure_triage_markdown_P": check_T_failure_triage_markdown_P,
    "check_T_interface_intelligence_failure_triage_assistant_P": check_T_interface_intelligence_failure_triage_assistant_P,
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
            raise TypeError("Unsupported registry type for interface_intelligence_failure_triage_assistant.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
