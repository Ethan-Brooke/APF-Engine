"""
APF Interface Solver Report Generation.
"""

from __future__ import annotations

from typing import Iterable, Mapping, Any, List
from datetime import datetime, timezone

from apf.interface_solver_descent_bridge import InterfaceSolverCertificate
from apf.interface_solver_batch import certificate_to_dict, certificates_to_jsonable
from apf.interface_solver_ci_policy import CIPolicyResult, policy_result_to_dict


def render_markdown_report(certs: Iterable[InterfaceSolverCertificate], policy: CIPolicyResult) -> str:
    certs = tuple(certs)
    summary = certificates_to_jsonable(certs)["summary"]
    lines: List[str] = []
    lines.append("# APF Interface Solver Certification Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now(timezone.utc).isoformat()}")
    lines.append("")
    lines.append(f"Policy: `{policy.mode.value}`")
    lines.append(f"Policy result: **{'PASS' if policy.pass_gate else 'FAIL'}**")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total certificates: {summary['total']}")
    lines.append(f"- Global exports: {len(summary['global_exports'])}")
    lines.append(f"- Held or failed: {len(summary['held_or_failed'])}")
    lines.append(f"- Fail-closed provenance: {len(summary['fail_closed'])}")
    lines.append("")
    if policy.hard_failures:
        lines.append("## Hard failures")
        lines.append("")
        for item in policy.hard_failures:
            lines.append(f"- {item}")
        lines.append("")
    if policy.warnings:
        lines.append("## Warnings")
        lines.append("")
        for item in policy.warnings:
            lines.append(f"- {item}")
        lines.append("")
    lines.append("## Certificates")
    lines.append("")
    lines.append("| Problem | Sector | Solver status | Obstruction | Export global P | Next action |")
    lines.append("|---|---|---|---|---:|---|")
    for cert in certs:
        obstruction = "; ".join(cert.obstruction) if cert.obstruction else "0"
        lines.append(
            f"| {cert.problem_name} | {cert.sector} | `{cert.solver_status.value}` | "
            f"{obstruction} | {cert.export_global_P} | {cert.next_action} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_json_report(certs: Iterable[InterfaceSolverCertificate], policy: CIPolicyResult) -> Mapping[str, Any]:
    return {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "policy": policy_result_to_dict(policy),
        **certificates_to_jsonable(certs),
    }
