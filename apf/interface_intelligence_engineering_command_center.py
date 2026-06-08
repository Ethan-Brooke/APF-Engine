"""
APF Interface Intelligence Engineering Command Center.

Purpose
-------
One operational command center for an integrated interface-intelligence installation:

    optional live smoke
    optional E2E artifact pipeline
    optional payload batch
    optional reviewer reporter
    optional failure triage
      -> command center dashboard
      -> final zip bundle

Boundary
--------
This command center orchestrates diagnostics and reporting. It does not repair routes or
promote held physics claims.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List
import datetime
import json
import subprocess
import sys
import zipfile


class CommandStepStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIPPED = "SKIPPED"


@dataclass(frozen=True)
class CommandCenterStep:
    name: str
    command: Tuple[str, ...]
    exit_code: int
    status: CommandStepStatus
    stdout_path: str
    stderr_path: str
    note: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d


@dataclass(frozen=True)
class CommandCenterReport:
    created_utc: str
    root: str
    out_dir: str
    steps: Tuple[CommandCenterStep, ...]
    pass_count: int
    fail_count: int
    skipped_count: int
    overall_pass: bool
    key_outputs: Mapping[str, str]
    zip_path: Optional[str]
    recommended_next_action: str
    dashboard_markdown: str
    note: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "created_utc": self.created_utc,
            "root": self.root,
            "out_dir": self.out_dir,
            "steps": [s.to_dict() for s in self.steps],
            "pass_count": self.pass_count,
            "fail_count": self.fail_count,
            "skipped_count": self.skipped_count,
            "overall_pass": self.overall_pass,
            "key_outputs": dict(self.key_outputs),
            "zip_path": self.zip_path,
            "recommended_next_action": self.recommended_next_action,
            "dashboard_markdown": self.dashboard_markdown,
            "note": self.note,
        }


def _py() -> str:
    return sys.executable or "python"


def _run_step(name: str, cmd: List[str], *, cwd: Path, out_dir: Path, timeout_s: int, allow_nonzero: bool = False) -> CommandCenterStep:
    stdout = out_dir / f"{name}.stdout.txt"
    stderr = out_dir / f"{name}.stderr.txt"
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True, timeout=timeout_s)
        stdout.write_text(proc.stdout, encoding="utf-8", errors="replace")
        stderr.write_text(proc.stderr, encoding="utf-8", errors="replace")
        ok = proc.returncode == 0 or allow_nonzero
        return CommandCenterStep(name, tuple(cmd), proc.returncode, CommandStepStatus.PASS if ok else CommandStepStatus.FAIL, str(stdout), str(stderr), "ran" if ok else "nonzero exit")
    except subprocess.TimeoutExpired as exc:
        stdout.write_text(exc.stdout or "", encoding="utf-8", errors="replace")
        stderr.write_text((exc.stderr or "") + f"\nTIMEOUT after {timeout_s}s", encoding="utf-8", errors="replace")
        return CommandCenterStep(name, tuple(cmd), 124, CommandStepStatus.FAIL, str(stdout), str(stderr), "timeout")
    except Exception as exc:
        stdout.write_text("", encoding="utf-8")
        stderr.write_text(repr(exc), encoding="utf-8")
        return CommandCenterStep(name, tuple(cmd), 999, CommandStepStatus.FAIL, str(stdout), str(stderr), "exception")


def _script(root: Path, name: str) -> Optional[Path]:
    p = root / "scripts" / name
    return p if p.exists() else None


def _missing_step(name: str, script_name: str, out_dir: Path) -> CommandCenterStep:
    stdout = out_dir / f"{name}.stdout.txt"
    stderr = out_dir / f"{name}.stderr.txt"
    stdout.write_text("", encoding="utf-8")
    stderr.write_text(f"missing script: scripts/{script_name}", encoding="utf-8")
    return CommandCenterStep(name, (_py(), f"scripts/{script_name}"), 127, CommandStepStatus.FAIL, str(stdout), str(stderr), "missing script")


def _zip_dir(out_dir: Path) -> str:
    zip_path = out_dir.parent / f"{out_dir.name}.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in out_dir.rglob("*"):
            z.write(p, p.relative_to(out_dir.parent))
    return str(zip_path)


def _read_json(path: Path) -> Optional[Mapping[str, Any]]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def render_dashboard(report: CommandCenterReport) -> str:
    lines = [
        "# APF Interface Intelligence Engineering Command Center",
        "",
        f"- Created UTC: `{report.created_utc}`",
        f"- Root: `{report.root}`",
        f"- Output directory: `{report.out_dir}`",
        f"- Overall pass: `{report.overall_pass}`",
        f"- Pass/Fail/Skipped: `{report.pass_count}/{report.fail_count}/{report.skipped_count}`",
        f"- Zip: `{report.zip_path}`",
        "",
        "## Recommended next action",
        "",
        report.recommended_next_action,
        "",
        "## Steps",
        "",
        "| Step | Status | Exit | Note |",
        "|---|---:|---:|---|",
    ]
    for step in report.steps:
        lines.append(f"| `{step.name}` | `{step.status.value}` | `{step.exit_code}` | {step.note} |")
    lines += [
        "",
        "## Key outputs",
        "",
    ]
    for k, v in report.key_outputs.items():
        lines.append(f"- `{k}`: `{v}`")
    lines += [
        "",
        "## Boundary",
        "",
        "This command center orchestrates diagnostics and reporting only. Held routes remain held until route evidence and rerun gates close.",
    ]
    return "\n".join(lines) + "\n"


def _recommended_action(steps: Tuple[CommandCenterStep, ...], out_dir: Path) -> str:
    first_fail = next((s for s in steps if s.status == CommandStepStatus.FAIL), None)
    if first_fail:
        if "missing script" in first_fail.note:
            return f"Install the missing package layer for `{first_fail.name}`, then rerun the command center."
        return f"Inspect `{first_fail.stderr_path}` and rerun `{first_fail.name}` after fixing the error."
    triage_json = out_dir / "interface_intelligence_failure_triage.json"
    triage = _read_json(triage_json)
    if triage:
        return str(triage.get("recommended_next_action", "Review the triage report."))
    return "No command-center blockers detected. Review dashboard/reviewer reports and proceed to live bank/verify_all wiring."


def run_engineering_command_center(
    root: str | Path = ".",
    out_dir: str | Path = "interface_intelligence_command_center_reports",
    *,
    timeout_s: int = 240,
    zip_outputs: bool = True,
) -> CommandCenterReport:
    cwd = Path(root).resolve()
    out = Path(out_dir)
    if not out.is_absolute():
        out = cwd / out
    out.mkdir(parents=True, exist_ok=True)

    steps: List[CommandCenterStep] = []

    # 1. Targeted command-center verifier.
    verifier = _script(cwd, "check_interface_intelligence_engineering_command_center.py")
    if verifier:
        steps.append(_run_step("check_command_center", [_py(), str(verifier)], cwd=cwd, out_dir=out, timeout_s=timeout_s))
    else:
        # In an installed root this script may be absent before install; missing is reported.
        steps.append(_missing_step("check_command_center", "check_interface_intelligence_engineering_command_center.py", out))

    # 2. Live smoke.
    smoke = _script(cwd, "run_interface_intelligence_live_smoke.py")
    smoke_dir = out / "live_smoke"
    if smoke:
        steps.append(_run_step("live_smoke", [_py(), str(smoke), "--root", str(cwd), "--report-dir", str(smoke_dir), "--timeout-s", str(timeout_s)], cwd=cwd, out_dir=out, timeout_s=max(timeout_s, 300), allow_nonzero=True))
    else:
        steps.append(_missing_step("live_smoke", "run_interface_intelligence_live_smoke.py", out))

    # 3. E2E artifact pipeline over smoke dir and common report/log dirs.
    e2e = _script(cwd, "run_interface_intelligence_E2E_artifact_pipeline.py")
    e2e_dir = out / "e2e_artifact_pipeline"
    e2e_inputs = [str(smoke_dir)]
    for rel in ["logs", "reports", "interface_intelligence_live_smoke_reports"]:
        if (cwd / rel).exists():
            e2e_inputs.append(str(cwd / rel))
    if e2e:
        steps.append(_run_step("e2e_artifact_pipeline", [_py(), str(e2e), "--inputs", *e2e_inputs, "--out-dir", str(e2e_dir)], cwd=cwd, out_dir=out, timeout_s=max(timeout_s, 300), allow_nonzero=True))
    else:
        steps.append(_missing_step("e2e_artifact_pipeline", "run_interface_intelligence_E2E_artifact_pipeline.py", out))

    # 4. Failure triage.
    triage = _script(cwd, "build_interface_failure_triage.py")
    triage_md = out / "interface_intelligence_failure_triage.md"
    triage_json = out / "interface_intelligence_failure_triage.json"
    triage_inputs = [str(smoke_dir), str(e2e_dir)]
    if triage:
        steps.append(_run_step("failure_triage", [_py(), str(triage), "--inputs", *triage_inputs, "--out-md", str(triage_md), "--out-json", str(triage_json)], cwd=cwd, out_dir=out, timeout_s=timeout_s, allow_nonzero=True))
    else:
        steps.append(_missing_step("failure_triage", "build_interface_failure_triage.py", out))

    # 5. Reviewer report if E2E has reviewer or batch JSONs.
    reviewer = _script(cwd, "build_interface_reviewer_report.py")
    reviewer_md = out / "interface_intelligence_reviewer_report.md"
    reviewer_json = out / "interface_intelligence_reviewer_report.json"
    reviewer_inputs: List[str] = []
    for candidate in [
        e2e_dir / "interface_reviewer_report.json",
        e2e_dir / "payload_batch" / "payload_batch_report.json",
        e2e_dir / "payload_batch" / "payload_batch_atlas.json",
    ]:
        if candidate.exists():
            reviewer_inputs.append(str(candidate))
    if reviewer and reviewer_inputs:
        steps.append(_run_step("reviewer_report", [_py(), str(reviewer), "--inputs", *reviewer_inputs, "--out-md", str(reviewer_md), "--out-json", str(reviewer_json)], cwd=cwd, out_dir=out, timeout_s=timeout_s, allow_nonzero=False))
    elif reviewer:
        steps.append(CommandCenterStep("reviewer_report", tuple(), 0, CommandStepStatus.SKIPPED, "", "", "no reviewer inputs found"))
    else:
        steps.append(_missing_step("reviewer_report", "build_interface_reviewer_report.py", out))

    pass_count = sum(1 for s in steps if s.status == CommandStepStatus.PASS)
    fail_count = sum(1 for s in steps if s.status == CommandStepStatus.FAIL)
    skipped_count = sum(1 for s in steps if s.status == CommandStepStatus.SKIPPED)

    key_outputs = {
        "live_smoke_dir": str(smoke_dir),
        "e2e_artifact_pipeline_dir": str(e2e_dir),
        "failure_triage_md": str(triage_md),
        "failure_triage_json": str(triage_json),
        "reviewer_report_md": str(reviewer_md),
        "reviewer_report_json": str(reviewer_json),
    }
    overall = fail_count == 0
    # Build a temporary report without markdown first.
    temp = CommandCenterReport(
        created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        root=str(cwd),
        out_dir=str(out),
        steps=tuple(steps),
        pass_count=pass_count,
        fail_count=fail_count,
        skipped_count=skipped_count,
        overall_pass=overall,
        key_outputs=key_outputs,
        zip_path=None,
        recommended_next_action=_recommended_action(tuple(steps), out),
        dashboard_markdown="",
        note="Command center pass means orchestration completed; route-level claims remain governed by certificates.",
    )
    dashboard = render_dashboard(temp)
    zip_path = _zip_dir(out) if zip_outputs else None
    report = CommandCenterReport(**{**temp.to_dict(), "steps": temp.steps, "zip_path": zip_path, "dashboard_markdown": dashboard})
    (out / "engineering_command_center_report.json").write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    (out / "engineering_command_center_dashboard.md").write_text(report.dashboard_markdown, encoding="utf-8")
    if zip_outputs:
        # Re-zip now that final dashboard/report are present.
        zip_path = _zip_dir(out)
        report = CommandCenterReport(**{**report.to_dict(), "steps": report.steps, "zip_path": zip_path})
        (out / "engineering_command_center_report.json").write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
        (out / "engineering_command_center_dashboard.md").write_text(render_dashboard(report), encoding="utf-8")
    return report


def check_T_command_center_structure_P() -> Dict[str, Any]:
    tests = {
        "runner_callable": callable(run_engineering_command_center),
        "report_to_dict": hasattr(CommandCenterReport, "to_dict"),
        "step_to_dict": hasattr(CommandCenterStep, "to_dict"),
        "statuses": {x.value for x in CommandStepStatus} == {"PASS", "FAIL", "SKIPPED"},
    }
    return {
        "name": "check_T_command_center_structure_P",
        "consistent": all(tests.values()),
        "status": "P_command_center" if all(tests.values()) else "FAIL",
        "summary": "Engineering command center exposes runner and structured report objects.",
        "data": {"tests": tests},
    }


def check_T_command_center_dry_run_P() -> Dict[str, Any]:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / "scripts").mkdir()
        report = run_engineering_command_center(td, td / "out", timeout_s=1, zip_outputs=False)
    tests = {
        "structured_fail": report.overall_pass is False,
        "has_missing_scripts": report.fail_count >= 1,
        "dashboard_mentions_boundary": "Held routes remain held" in report.dashboard_markdown,
        "recommended_action_present": bool(report.recommended_next_action),
    }
    return {
        "name": "check_T_command_center_dry_run_P",
        "consistent": all(tests.values()),
        "status": "P_command_center" if all(tests.values()) else "FAIL",
        "summary": "Command center dry-run fails gracefully with missing-script diagnostics.",
        "data": {"tests": tests},
        "dependencies": ["check_T_command_center_structure_P"],
    }


def check_T_command_center_dashboard_P() -> Dict[str, Any]:
    step = CommandCenterStep("demo", ("python", "demo.py"), 0, CommandStepStatus.PASS, "out", "err", "ran")
    report = CommandCenterReport(
        created_utc="now",
        root=".",
        out_dir="reports",
        steps=(step,),
        pass_count=1,
        fail_count=0,
        skipped_count=0,
        overall_pass=True,
        key_outputs={"x": "y"},
        zip_path="reports.zip",
        recommended_next_action="Proceed.",
        dashboard_markdown="",
        note="note",
    )
    md = render_dashboard(report)
    tests = {
        "has_title": "# APF Interface Intelligence Engineering Command Center" in md,
        "has_steps": "| Step | Status | Exit | Note |" in md,
        "has_boundary": "Held routes remain held" in md,
        "has_recommended": "Recommended next action" in md,
    }
    return {
        "name": "check_T_command_center_dashboard_P",
        "consistent": all(tests.values()),
        "status": "P_command_center" if all(tests.values()) else "FAIL",
        "summary": "Command center renders an integrator dashboard with boundary language.",
        "data": {"tests": tests},
        "dependencies": ["check_T_command_center_dry_run_P"],
    }


def check_T_interface_intelligence_engineering_command_center_P() -> Dict[str, Any]:
    subchecks = [
        check_T_command_center_structure_P(),
        check_T_command_center_dry_run_P(),
        check_T_command_center_dashboard_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_interface_intelligence_engineering_command_center_P",
        "consistent": ok,
        "status": "P_command_center" if ok else "FAIL",
        "summary": "Interface Intelligence Engineering Command Center is P: live diagnostics can be orchestrated and dashboarded in one command.",
        "data": {
            "core_claim": "The command center gives integrators one operational entry point without promoting held route claims.",
            "subchecks": [x["name"] for x in subchecks],
        },
        "dependencies": [x["name"] for x in subchecks],
    }


CHECKS = {
    "check_T_command_center_structure_P": check_T_command_center_structure_P,
    "check_T_command_center_dry_run_P": check_T_command_center_dry_run_P,
    "check_T_command_center_dashboard_P": check_T_command_center_dashboard_P,
    "check_T_interface_intelligence_engineering_command_center_P": check_T_interface_intelligence_engineering_command_center_P,
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
            raise TypeError("Unsupported registry type for interface_intelligence_engineering_command_center.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
