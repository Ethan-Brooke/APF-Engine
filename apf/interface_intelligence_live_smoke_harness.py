"""
APF Interface Intelligence Live Smoke Harness.

Purpose
-------
One live integration smoke target for an installed interface-intelligence stack.

The full smoke run is intentionally meant for the live APF codebase after integration.
The verifier for this package checks harness structure and graceful failure behavior only.

Boundary: integration diagnostic only; does not promote physics claims.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, List
import datetime
import json
import subprocess
import sys
import zipfile


class SmokeStepStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIPPED = "SKIPPED"


@dataclass(frozen=True)
class SmokeStep:
    name: str
    command: Tuple[str, ...]
    exit_code: int
    status: SmokeStepStatus
    stdout_path: str
    stderr_path: str
    output_path: Optional[str]
    note: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d


@dataclass(frozen=True)
class SmokeSummary:
    created_utc: str
    root: str
    report_dir: str
    steps: Tuple[SmokeStep, ...]
    pass_count: int
    fail_count: int
    skipped_count: int
    overall_pass: bool
    report_zip: Optional[str]
    note: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "created_utc": self.created_utc,
            "root": self.root,
            "report_dir": self.report_dir,
            "steps": [s.to_dict() for s in self.steps],
            "pass_count": self.pass_count,
            "fail_count": self.fail_count,
            "skipped_count": self.skipped_count,
            "overall_pass": self.overall_pass,
            "report_zip": self.report_zip,
            "note": self.note,
        }


DEFAULT_STEPS: Tuple[Tuple[str, Tuple[str, ...], Optional[str]], ...] = (
    ("check_interface_intelligence_CI_orchestrator", ("scripts/check_interface_intelligence_CI_orchestrator.py",), None),
    ("check_interface_intelligence_registry_bridge", ("scripts/check_interface_intelligence_registry_bridge.py",), None),
    ("run_interface_intelligence_CI", ("scripts/run_interface_intelligence_CI.py", "--out", "interface_intelligence_CI_report.json"), "interface_intelligence_CI_report.json"),
    ("run_ew_trace_to_scheme_adapter", ("scripts/run_ew_trace_to_scheme_adapter.py", "--out", "ew_live_adapter_report.json"), "ew_live_adapter_report.json"),
    ("run_dark_posterior_adapter", ("scripts/run_dark_posterior_adapter.py", "--out", "dark_live_adapter_report.json"), "dark_live_adapter_report.json"),
    ("build_interface_atlas", ("scripts/build_interface_atlas.py", "--out", "interface_atlas_report.json"), "interface_atlas_report.json"),
    ("emit_registry_bridge", ("scripts/emit_interface_intelligence_registry_bridge.py", "--out-dir", "registry_bridge_out"), "registry_bridge_out"),
    ("compile_EW_claim_smoke", ("scripts/compile_claim_to_interface_graph.py", "--claim", "EW APF_TRACE physical scheme masses are exported to global P.", "--out", "ew_claim_audit_report.json"), "ew_claim_audit_report.json"),
)


def _py() -> str:
    return sys.executable or "python"


def _run_step(name: str, relcmd: Tuple[str, ...], output_rel: Optional[str], *, cwd: Path, report_dir: Path, timeout_s: int) -> SmokeStep:
    script = cwd / relcmd[0]
    stdout_path = report_dir / f"{name}.stdout.txt"
    stderr_path = report_dir / f"{name}.stderr.txt"
    output_path = report_dir / output_rel if output_rel else None

    if not script.exists():
        stdout_path.write_text("", encoding="utf-8")
        stderr_path.write_text(f"missing script: {script}", encoding="utf-8")
        return SmokeStep(name, tuple([_py(), str(script), *relcmd[1:]]), 127, SmokeStepStatus.FAIL, str(stdout_path), str(stderr_path), str(output_path) if output_path else None, "missing script")

    cmd = [_py(), str(script)]
    for arg in relcmd[1:]:
        if arg.endswith(".json") or arg.endswith("_out") or arg.endswith("_report.json"):
            cmd.append(str(report_dir / arg))
        else:
            cmd.append(arg)
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True, timeout=timeout_s)
        stdout_path.write_text(proc.stdout, encoding="utf-8", errors="replace")
        stderr_path.write_text(proc.stderr, encoding="utf-8", errors="replace")
        return SmokeStep(name, tuple(cmd), proc.returncode, SmokeStepStatus.PASS if proc.returncode == 0 else SmokeStepStatus.FAIL, str(stdout_path), str(stderr_path), str(output_path) if output_path else None, "ran")
    except subprocess.TimeoutExpired as exc:
        stdout_path.write_text(exc.stdout or "", encoding="utf-8", errors="replace")
        stderr_path.write_text((exc.stderr or "") + f"\nTIMEOUT after {timeout_s}s", encoding="utf-8", errors="replace")
        return SmokeStep(name, tuple(cmd), 124, SmokeStepStatus.FAIL, str(stdout_path), str(stderr_path), str(output_path) if output_path else None, "timeout")
    except Exception as exc:
        stdout_path.write_text("", encoding="utf-8")
        stderr_path.write_text(repr(exc), encoding="utf-8")
        return SmokeStep(name, tuple(cmd), 999, SmokeStepStatus.FAIL, str(stdout_path), str(stderr_path), str(output_path) if output_path else None, "exception")


def render_text_summary(summary: SmokeSummary) -> str:
    lines = [
        "APF Interface Intelligence Live Smoke Summary",
        "=" * 52,
        f"Created UTC: {summary.created_utc}",
        f"Root: {summary.root}",
        f"Report dir: {summary.report_dir}",
        f"Overall pass: {summary.overall_pass}",
        f"Pass/Fail/Skipped: {summary.pass_count}/{summary.fail_count}/{summary.skipped_count}",
        f"Report zip: {summary.report_zip}",
        "",
        "Steps:",
    ]
    for step in summary.steps:
        lines.append(f"- {step.name}: {step.status.value} exit={step.exit_code} note={step.note}")
        if step.output_path:
            lines.append(f"  output: {step.output_path}")
    lines += [
        "",
        "Boundary:",
        "This smoke harness validates software integration and report generation only.",
        "It does not promote held route-level physics claims to P.",
    ]
    return "\n".join(lines) + "\n"


def run_live_smoke_harness(root: str | Path = ".", report_dir: str | Path = "interface_intelligence_live_smoke_reports", *, zip_reports: bool = True, timeout_s: int = 180) -> SmokeSummary:
    cwd = Path(root).resolve()
    out = Path(report_dir)
    if not out.is_absolute():
        out = cwd / out
    out.mkdir(parents=True, exist_ok=True)

    steps = tuple(_run_step(name, relcmd, output_rel, cwd=cwd, report_dir=out, timeout_s=timeout_s) for name, relcmd, output_rel in DEFAULT_STEPS)

    pass_count = sum(1 for s in steps if s.status == SmokeStepStatus.PASS)
    fail_count = sum(1 for s in steps if s.status == SmokeStepStatus.FAIL)
    skipped_count = sum(1 for s in steps if s.status == SmokeStepStatus.SKIPPED)
    overall = fail_count == 0

    summary = SmokeSummary(
        created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        root=str(cwd),
        report_dir=str(out),
        steps=steps,
        pass_count=pass_count,
        fail_count=fail_count,
        skipped_count=skipped_count,
        overall_pass=overall,
        report_zip=None,
        note="Live smoke harness is diagnostic/integration-only; route-level physics claims remain governed by route certificates.",
    )

    (out / "interface_intelligence_live_smoke_summary.json").write_text(json.dumps(summary.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    (out / "interface_intelligence_live_smoke_summary.txt").write_text(render_text_summary(summary), encoding="utf-8")

    report_zip = None
    if zip_reports:
        zip_path = out.parent / f"{out.name}.zip"
        if zip_path.exists():
            zip_path.unlink()
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for p in out.rglob("*"):
                z.write(p, p.relative_to(out.parent))
        report_zip = str(zip_path)
        summary = SmokeSummary(**{**summary.to_dict(), "steps": steps, "report_zip": report_zip})
        (out / "interface_intelligence_live_smoke_summary.json").write_text(json.dumps(summary.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
        (out / "interface_intelligence_live_smoke_summary.txt").write_text(render_text_summary(summary), encoding="utf-8")

    return summary


def check_T_live_smoke_harness_structure_P() -> Dict[str, Any]:
    tests = {
        "has_default_steps": len(DEFAULT_STEPS) >= 8,
        "runner_callable": callable(run_live_smoke_harness),
        "summary_to_dict": hasattr(SmokeSummary, "to_dict"),
        "step_to_dict": hasattr(SmokeStep, "to_dict"),
    }
    return {
        "name": "check_T_live_smoke_harness_structure_P",
        "consistent": all(tests.values()),
        "status": "P_live_smoke" if all(tests.values()) else "FAIL",
        "summary": "Live smoke harness exposes required steps and structured summary objects.",
        "data": {"tests": tests},
    }


def check_T_live_smoke_harness_dry_run_P() -> Dict[str, Any]:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / "scripts").mkdir()
        summary = run_live_smoke_harness(td, td / "out", zip_reports=False, timeout_s=1)
    tests = {
        "graceful_failures": summary.fail_count >= 1,
        "overall_false": summary.overall_pass is False,
        "summary_created": isinstance(summary, SmokeSummary),
        "step_count": len(summary.steps) == len(DEFAULT_STEPS),
    }
    return {
        "name": "check_T_live_smoke_harness_dry_run_P",
        "consistent": all(tests.values()),
        "status": "P_live_smoke" if all(tests.values()) else "FAIL",
        "summary": "Dry-run in empty root fails gracefully with structured missing-script diagnostics.",
        "data": {"tests": tests},
        "dependencies": ["check_T_live_smoke_harness_structure_P"],
    }


def check_T_live_smoke_harness_text_summary_P() -> Dict[str, Any]:
    step = SmokeStep("demo", ("python", "x.py"), 0, SmokeStepStatus.PASS, "stdout", "stderr", "out.json", "demo")
    summary = SmokeSummary("now", ".", "reports", (step,), 1, 0, 0, True, "reports.zip", "note")
    text = render_text_summary(summary)
    tests = {
        "mentions_overall": "Overall pass: True" in text,
        "mentions_boundary": "does not promote" in text,
        "mentions_step": "- demo: PASS" in text,
    }
    return {
        "name": "check_T_live_smoke_harness_text_summary_P",
        "consistent": all(tests.values()),
        "status": "P_live_smoke" if all(tests.values()) else "FAIL",
        "summary": "Live smoke harness emits human-readable summary with boundary language.",
        "data": {"tests": tests},
        "dependencies": ["check_T_live_smoke_harness_dry_run_P"],
    }


def check_T_interface_intelligence_live_smoke_harness_P() -> Dict[str, Any]:
    subchecks = [
        check_T_live_smoke_harness_structure_P(),
        check_T_live_smoke_harness_dry_run_P(),
        check_T_live_smoke_harness_text_summary_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_interface_intelligence_live_smoke_harness_P",
        "consistent": ok,
        "status": "P_live_smoke_harness" if ok else "FAIL",
        "summary": "Interface Intelligence Live Smoke Harness is P: one diagnostic target for installed-stack reporting.",
        "data": {
            "core_claim": "The harness gives the integrator one diagnostic target for the installed interface-intelligence stack.",
            "subchecks": [x["name"] for x in subchecks],
        },
        "dependencies": [x["name"] for x in subchecks],
    }


CHECKS = {
    "check_T_live_smoke_harness_structure_P": check_T_live_smoke_harness_structure_P,
    "check_T_live_smoke_harness_dry_run_P": check_T_live_smoke_harness_dry_run_P,
    "check_T_live_smoke_harness_text_summary_P": check_T_live_smoke_harness_text_summary_P,
    "check_T_interface_intelligence_live_smoke_harness_P": check_T_interface_intelligence_live_smoke_harness_P,
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
            raise TypeError("Unsupported registry type for interface_intelligence_live_smoke_harness.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
