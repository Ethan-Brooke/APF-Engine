"""
APF Interface Intelligence Post-Install Acceptance Auditor.

Purpose
-------
Audit a live integration after install:

    release manifest
    command-center dashboard/report
    CI report
    registry bridge output
    failure triage
    verify_all log
      -> ACCEPTED / HELD / BLOCKED
      -> missing acceptance criteria
      -> exact next action

Boundary
--------
This auditor accepts or holds software integration only. It does not promote physics route
claims merely because the software stack is installed.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List
import json
import re
import datetime


class AcceptanceStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    HELD = "HELD"
    BLOCKED = "BLOCKED"


class AcceptanceCriterionStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    MISSING = "MISSING"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True)
class AcceptanceCriterion:
    criterion_id: str
    status: AcceptanceCriterionStatus
    summary: str
    evidence: Optional[str]
    next_action: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d


@dataclass(frozen=True)
class AcceptanceAuditReport:
    created_utc: str
    root: str
    status: AcceptanceStatus
    criteria: Tuple[AcceptanceCriterion, ...]
    missing_markers: Tuple[str, ...]
    failed_markers: Tuple[str, ...]
    recommended_next_action: str
    markdown: str
    boundary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "created_utc": self.created_utc,
            "root": self.root,
            "status": self.status.value,
            "criteria": [c.to_dict() for c in self.criteria],
            "missing_markers": list(self.missing_markers),
            "failed_markers": list(self.failed_markers),
            "recommended_next_action": self.recommended_next_action,
            "markdown": self.markdown,
            "boundary": self.boundary,
        }


DEFAULT_EXPECTED_MARKERS: Tuple[str, ...] = (
    "ROUTE_CERTIFICATION_STARTER_SUITE_P_PASS",
    "ROUTE_CERTIFICATION_INTEGRATION_WORKBENCH_P_PASS",
    "INTERFACE_STRUCTURE_TRANSPORT_LEDGER_P_PASS",
    "INTERFACE_STRUCTURE_DISCOVERY_ENGINE_P_PASS",
    "INTERFACE_STRUCTURE_MOVEMENT_GRAPH_P_PASS",
    "INTERFACE_MOVEMENT_GRAPH_REPAIR_PLANNER_P_PASS",
    "INTERFACE_REPAIR_CLOSURE_SIMULATOR_P_PASS",
    "INTERFACE_REPAIR_FRONTIER_EXPLORER_P_PASS",
    "INTERFACE_REPAIR_OBLIGATION_COMPILER_P_PASS",
    "INTERFACE_EVIDENCE_RERUN_CONTROLLER_P_PASS",
    "EW_TRACE_TO_SCHEME_REAL_ADAPTER_P_PASS",
    "DARK_POSTERIOR_REAL_ADAPTER_P_PASS",
    "CLAIM_TO_INTERFACE_GRAPH_COMPILER_P_PASS",
    "INTERFACE_ATLAS_P_PASS",
    "INTERFACE_INTELLIGENCE_CI_ORCHESTRATOR_P_PASS",
    "INTERFACE_INTELLIGENCE_REGISTRY_BRIDGE_P_PASS",
    "INTERFACE_INTELLIGENCE_LIVE_SMOKE_HARNESS_P_PASS",
    "INTERFACE_INTELLIGENCE_REVIEWER_REPORTER_P_PASS",
    "ARTIFACT_TO_ROUTE_PAYLOAD_ADAPTER_P_PASS",
    "PAYLOAD_BATCH_CERTIFICATION_RUNNER_P_PASS",
    "INTERFACE_INTELLIGENCE_E2E_ARTIFACT_PIPELINE_P_PASS",
    "INTERFACE_INTELLIGENCE_FAILURE_TRIAGE_ASSISTANT_P_PASS",
    "INTERFACE_INTELLIGENCE_ENGINEERING_COMMAND_CENTER_P_PASS",
    "INTERFACE_INTELLIGENCE_RELEASE_MANIFEST_P_PASS",
)


def _safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def _safe_json(path: Path) -> Optional[Mapping[str, object]]:
    try:
        obj = json.loads(_safe_read(path))
        return obj if isinstance(obj, Mapping) else None
    except Exception:
        return None


def collect_text_corpus(root: str | Path) -> str:
    root = Path(root)
    parts: List[str] = []
    for pattern in ("*.txt", "*.log", "*.json", "*.md", "*.out", "*.stderr", "*.stdout"):
        for p in root.rglob(pattern):
            if p.is_file() and p.stat().st_size < 5_000_000:
                parts.append(f"\n--- {p} ---\n")
                parts.append(_safe_read(p))
    return "\n".join(parts)


def expected_markers_from_manifest(root: str | Path) -> Tuple[str, ...]:
    root = Path(root)
    for p in root.rglob("interface_intelligence_release_manifest.json"):
        obj = _safe_json(p)
        if obj and isinstance(obj.get("layers"), list):
            markers = []
            for layer in obj["layers"]:
                if isinstance(layer, Mapping) and layer.get("top_marker"):
                    markers.append(str(layer["top_marker"]))
            if markers:
                return tuple(markers)
    return DEFAULT_EXPECTED_MARKERS


def audit_markers(root: str | Path, expected_markers: Optional[Iterable[str]] = None) -> Tuple[AcceptanceCriterion, Tuple[str, ...], Tuple[str, ...]]:
    corpus = collect_text_corpus(root)
    markers = tuple(expected_markers or expected_markers_from_manifest(root))
    missing = tuple(m for m in markers if m not in corpus)
    failed = tuple(m.replace("_P_PASS", "_P_FAIL") for m in markers if m.replace("_P_PASS", "_P_FAIL") in corpus)
    if not missing and not failed:
        status = AcceptanceCriterionStatus.PASS
        summary = f"All {len(markers)} expected markers found; no matching FAIL markers found."
        action = None
    elif failed:
        status = AcceptanceCriterionStatus.FAIL
        summary = f"{len(failed)} fail marker(s) found."
        action = "Inspect targeted verifier logs for the failed markers before rerunning command center."
    else:
        status = AcceptanceCriterionStatus.MISSING
        summary = f"{len(missing)} expected marker(s) missing."
        action = "Run/install missing layers in release-manifest order, then rerun acceptance audit."
    criterion = AcceptanceCriterion("targeted_markers", status, summary, "text corpus under root", action)
    return criterion, missing, failed


def audit_command_center(root: str | Path) -> AcceptanceCriterion:
    root = Path(root)
    candidates = list(root.rglob("engineering_command_center_report.json"))
    if not candidates:
        return AcceptanceCriterion("command_center_report", AcceptanceCriterionStatus.MISSING, "No engineering_command_center_report.json found.", None, "Run RUN_INTERFACE_INTELLIGENCE_ENGINEERING_COMMAND_CENTER.ps1.")
    latest = max(candidates, key=lambda p: p.stat().st_mtime)
    obj = _safe_json(latest)
    if obj and obj.get("overall_pass") is True:
        return AcceptanceCriterion("command_center_report", AcceptanceCriterionStatus.PASS, "Engineering command center reports overall_pass=true.", str(latest), None)
    return AcceptanceCriterion("command_center_report", AcceptanceCriterionStatus.FAIL, "Engineering command center report exists but did not pass.", str(latest), "Open engineering_command_center_dashboard.md and failure triage; fix first blocker.")


def audit_registry_bridge(root: str | Path) -> AcceptanceCriterion:
    root = Path(root)
    names = {"register_interface_intelligence_checks.py", "verify_all_interface_intelligence_snippet.py", "interface_intelligence_top_checks.json"}
    found = {p.name for p in root.rglob("*") if p.name in names}
    if found == names:
        return AcceptanceCriterion("registry_bridge_outputs", AcceptanceCriterionStatus.PASS, "Registry bridge output files found.", ", ".join(sorted(found)), None)
    missing = names - found
    return AcceptanceCriterion("registry_bridge_outputs", AcceptanceCriterionStatus.MISSING, f"Missing registry bridge outputs: {sorted(missing)}", ", ".join(sorted(found)) if found else None, "Run emit_interface_intelligence_registry_bridge.py and wire generated stub into live bank/verify_all.")


def audit_verify_all(root: str | Path) -> AcceptanceCriterion:
    corpus = collect_text_corpus(root).lower()
    verify_lines = [line for line in corpus.splitlines() if "verify_all" in line or "verify all" in line]
    if not verify_lines:
        return AcceptanceCriterion("verify_all", AcceptanceCriterionStatus.MISSING, "No verify_all pass evidence found.", None, "Run live verify_all.py after registry wiring.")
    joined = "\n".join(verify_lines)
    if re.search(r"\b(fail|failed|failure|error)\b", joined):
        return AcceptanceCriterion("verify_all", AcceptanceCriterionStatus.FAIL, "verify_all-like log mentions failure.", "text corpus under root", "Fix verify_all failure before accepting live bank integration.")
    if re.search(r"\b(pass|passed|success|ok)\b", joined):
        return AcceptanceCriterion("verify_all", AcceptanceCriterionStatus.PASS, "verify_all-like pass evidence found.", "text corpus under root", None)
    return AcceptanceCriterion("verify_all", AcceptanceCriterionStatus.MISSING, "verify_all mentioned but no explicit pass evidence found.", "text corpus under root", "Run live verify_all.py and capture pass output.")


def audit_triage(root: str | Path) -> AcceptanceCriterion:
    root = Path(root)
    candidates = list(root.rglob("interface_intelligence_failure_triage.json"))
    if not candidates:
        return AcceptanceCriterion("failure_triage", AcceptanceCriterionStatus.MISSING, "No failure triage JSON found.", None, "Run build_interface_failure_triage.py or engineering command center.")
    latest = max(candidates, key=lambda p: p.stat().st_mtime)
    obj = _safe_json(latest)
    if obj and obj.get("first_blocker"):
        cause = obj["first_blocker"].get("cause", "UNKNOWN") if isinstance(obj["first_blocker"], Mapping) else "UNKNOWN"
        return AcceptanceCriterion("failure_triage", AcceptanceCriterionStatus.FAIL, f"Failure triage reports first blocker: {cause}.", str(latest), str(obj.get("recommended_next_action", "Fix first blocker.")))
    return AcceptanceCriterion("failure_triage", AcceptanceCriterionStatus.PASS, "Failure triage reports no first blocker.", str(latest), None)


def determine_status(criteria: Iterable[AcceptanceCriterion]) -> AcceptanceStatus:
    statuses = {c.status for c in criteria}
    if AcceptanceCriterionStatus.FAIL in statuses:
        return AcceptanceStatus.BLOCKED
    if AcceptanceCriterionStatus.MISSING in statuses:
        return AcceptanceStatus.HELD
    return AcceptanceStatus.ACCEPTED


def recommended_action(status: AcceptanceStatus, criteria: Iterable[AcceptanceCriterion]) -> str:
    for c in criteria:
        if c.status in {AcceptanceCriterionStatus.FAIL, AcceptanceCriterionStatus.MISSING} and c.next_action:
            return c.next_action
    if status == AcceptanceStatus.ACCEPTED:
        return "Software integration acceptance criteria passed. Proceed to live bank documentation while preserving route-claim boundaries."
    return "Inspect failed/missing criteria and rerun acceptance audit."


def render_acceptance_markdown(report: AcceptanceAuditReport) -> str:
    lines = [
        "# APF Interface Intelligence Post-Install Acceptance Audit",
        "",
        f"- Status: **{report.status.value}**",
        f"- Root: `{report.root}`",
        f"- Created UTC: `{report.created_utc}`",
        "",
        "## Recommended next action",
        "",
        report.recommended_next_action,
        "",
        "## Criteria",
        "",
        "| Criterion | Status | Summary | Evidence | Next action |",
        "|---|---|---|---|---|",
    ]
    for c in report.criteria:
        lines.append(f"| `{c.criterion_id}` | `{c.status.value}` | {c.summary} | `{c.evidence or '—'}` | {c.next_action or '—'} |")
    lines += [
        "",
        "## Missing markers",
        "",
    ]
    if report.missing_markers:
        lines.extend(f"- `{m}`" for m in report.missing_markers)
    else:
        lines.append("- none")
    lines += [
        "",
        "## Failed markers",
        "",
    ]
    if report.failed_markers:
        lines.extend(f"- `{m}`" for m in report.failed_markers)
    else:
        lines.append("- none")
    lines += [
        "",
        "## Boundary",
        "",
        report.boundary,
    ]
    return "\n".join(lines) + "\n"


def run_acceptance_audit(root: str | Path) -> AcceptanceAuditReport:
    root = Path(root).resolve()
    marker_criterion, missing, failed = audit_markers(root)
    criteria = (
        marker_criterion,
        audit_command_center(root),
        audit_registry_bridge(root),
        audit_triage(root),
        audit_verify_all(root),
    )
    status = determine_status(criteria)
    boundary = "This accepts or holds software integration only; it does not promote held physics route claims to P."
    temp = AcceptanceAuditReport(
        created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        root=str(root),
        status=status,
        criteria=criteria,
        missing_markers=missing,
        failed_markers=failed,
        recommended_next_action=recommended_action(status, criteria),
        markdown="",
        boundary=boundary,
    )
    return AcceptanceAuditReport(**{**temp.to_dict(), "criteria": criteria, "missing_markers": missing, "failed_markers": failed, "markdown": render_acceptance_markdown(temp)})


def write_acceptance_audit(root: str | Path, out_md: str | Path, out_json: Optional[str | Path] = None) -> AcceptanceAuditReport:
    report = run_acceptance_audit(root)
    Path(out_md).write_text(report.markdown, encoding="utf-8")
    if out_json:
        Path(out_json).write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return report


def check_T_acceptance_auditor_holds_missing_P() -> Dict[str, object]:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        report = run_acceptance_audit(td)
    tests = {
        "held_or_blocked": report.status in {AcceptanceStatus.HELD, AcceptanceStatus.BLOCKED},
        "has_missing": any(c.status == AcceptanceCriterionStatus.MISSING for c in report.criteria),
        "boundary": "does not promote" in report.boundary,
    }
    return {"name": "check_T_acceptance_auditor_holds_missing_P", "consistent": all(tests.values()), "status": "P_acceptance_auditor" if all(tests.values()) else "FAIL", "summary": "Acceptance auditor holds empty/missing integrations.", "data": {"tests": tests}}


def check_T_acceptance_auditor_accepts_complete_P() -> Dict[str, object]:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        # Emit marker corpus.
        (td / "markers.txt").write_text("\n".join(DEFAULT_EXPECTED_MARKERS) + "\nverify_all passed\n", encoding="utf-8")
        (td / "engineering_command_center_report.json").write_text(json.dumps({"overall_pass": True}), encoding="utf-8")
        rb = td / "registry_bridge_out"
        rb.mkdir()
        for name in ["register_interface_intelligence_checks.py", "verify_all_interface_intelligence_snippet.py", "interface_intelligence_top_checks.json"]:
            (rb / name).write_text("x", encoding="utf-8")
        (td / "interface_intelligence_failure_triage.json").write_text(json.dumps({"first_blocker": None, "recommended_next_action": "Proceed."}), encoding="utf-8")
        report = run_acceptance_audit(td)
    tests = {
        "accepted": report.status == AcceptanceStatus.ACCEPTED,
        "no_missing_markers": report.missing_markers == tuple(),
        "criteria_pass": all(c.status == AcceptanceCriterionStatus.PASS for c in report.criteria),
    }
    return {"name": "check_T_acceptance_auditor_accepts_complete_P", "consistent": all(tests.values()), "status": "P_acceptance_auditor" if all(tests.values()) else "FAIL", "summary": "Acceptance auditor accepts a complete synthetic integration.", "data": {"tests": tests}, "dependencies": ["check_T_acceptance_auditor_holds_missing_P"]}


def check_T_acceptance_auditor_blocks_failures_P() -> Dict[str, object]:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / "markers.txt").write_text("INTERFACE_ATLAS_P_FAIL\n", encoding="utf-8")
        (td / "engineering_command_center_report.json").write_text(json.dumps({"overall_pass": False}), encoding="utf-8")
        report = run_acceptance_audit(td)
    tests = {
        "blocked": report.status == AcceptanceStatus.BLOCKED,
        "has_fail_marker": any("P_FAIL" in x for x in report.failed_markers),
        "next_action": bool(report.recommended_next_action),
    }
    return {"name": "check_T_acceptance_auditor_blocks_failures_P", "consistent": all(tests.values()), "status": "P_acceptance_auditor" if all(tests.values()) else "FAIL", "summary": "Acceptance auditor blocks explicit failure evidence.", "data": {"tests": tests}, "dependencies": ["check_T_acceptance_auditor_accepts_complete_P"]}


def check_T_interface_intelligence_post_install_acceptance_auditor_P() -> Dict[str, object]:
    subchecks = [
        check_T_acceptance_auditor_holds_missing_P(),
        check_T_acceptance_auditor_accepts_complete_P(),
        check_T_acceptance_auditor_blocks_failures_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {"name": "check_T_interface_intelligence_post_install_acceptance_auditor_P", "consistent": ok, "status": "P_acceptance_auditor" if ok else "FAIL", "summary": "Post-Install Acceptance Auditor is P: live integration is accepted, held, or blocked by explicit evidence criteria.", "data": {"core_claim": "Software acceptance is audited separately from physics route promotion.", "subchecks": [x["name"] for x in subchecks]}, "dependencies": [x["name"] for x in subchecks]}


CHECKS = {
    "check_T_acceptance_auditor_holds_missing_P": check_T_acceptance_auditor_holds_missing_P,
    "check_T_acceptance_auditor_accepts_complete_P": check_T_acceptance_auditor_accepts_complete_P,
    "check_T_acceptance_auditor_blocks_failures_P": check_T_acceptance_auditor_blocks_failures_P,
    "check_T_interface_intelligence_post_install_acceptance_auditor_P": check_T_interface_intelligence_post_install_acceptance_auditor_P,
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
            raise TypeError("Unsupported registry type for interface_intelligence_post_install_acceptance_auditor.register")
    return registry


def run_all() -> Dict[str, Dict[str, object]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
