"""
APF Interface Solver CI Policy.

Policy gates for engineering workflows.

Default behavior:
    * PASS if no fail-closed provenance and no unsupported failures.
    * STRICT_GLOBAL can require all requested exports to be global P.
    * WARN_HELD permits held-for-repair local results but marks them in the report.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Mapping, Tuple, Dict, Any, List

from apf.interface_solver_descent_bridge import InterfaceSolverCertificate


class CIPolicyMode(str, Enum):
    PERMISSIVE_RESEARCH = "PERMISSIVE_RESEARCH"
    BLOCK_FAIL_CLOSED = "BLOCK_FAIL_CLOSED"
    STRICT_GLOBAL_EXPORT = "STRICT_GLOBAL_EXPORT"


@dataclass(frozen=True)
class CIPolicyResult:
    mode: CIPolicyMode
    pass_gate: bool
    hard_failures: Tuple[str, ...]
    warnings: Tuple[str, ...]
    summary: str


def evaluate_ci_policy(
    certs: Iterable[InterfaceSolverCertificate],
    *,
    mode: CIPolicyMode = CIPolicyMode.BLOCK_FAIL_CLOSED,
) -> CIPolicyResult:
    certs = tuple(certs)
    hard: List[str] = []
    warnings: List[str] = []

    for cert in certs:
        if cert.solver_status.value in {"FAIL_CLOSED_PROVENANCE", "FAIL_UNSUPPORTED"}:
            hard.append(f"{cert.problem_name}: {cert.solver_status.value}")
        elif not cert.export_global_P:
            warnings.append(f"{cert.problem_name}: held/non-global ({cert.solver_status.value})")

    if mode == CIPolicyMode.PERMISSIVE_RESEARCH:
        pass_gate = len([h for h in hard if "FAIL_CLOSED_PROVENANCE" in h]) == 0
    elif mode == CIPolicyMode.BLOCK_FAIL_CLOSED:
        pass_gate = len(hard) == 0
    elif mode == CIPolicyMode.STRICT_GLOBAL_EXPORT:
        pass_gate = len(hard) == 0 and all(cert.export_global_P for cert in certs)
        if not pass_gate:
            for cert in certs:
                if not cert.export_global_P and f"{cert.problem_name}: not global export" not in warnings:
                    warnings.append(f"{cert.problem_name}: not global export")
    else:
        raise ValueError(f"Unknown CI policy mode: {mode}")

    if pass_gate:
        summary = f"CI policy {mode.value} PASS"
    else:
        summary = f"CI policy {mode.value} FAIL"

    return CIPolicyResult(
        mode=mode,
        pass_gate=pass_gate,
        hard_failures=tuple(hard),
        warnings=tuple(warnings),
        summary=summary,
    )


def policy_result_to_dict(result: CIPolicyResult) -> Dict[str, Any]:
    return {
        "mode": result.mode.value,
        "pass_gate": result.pass_gate,
        "hard_failures": list(result.hard_failures),
        "warnings": list(result.warnings),
        "summary": result.summary,
    }
