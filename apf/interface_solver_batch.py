"""
APF Interface Solver Batch Certification.

Batch APIs for solver/CI integration.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Dict, Iterable, Mapping, Tuple, List, Any
from collections import Counter

from apf.interface_solver_descent_bridge import (
    InterfaceSolverProblem,
    InterfaceSolverCertificate,
    solve_interface_descent,
    certificate_data,
)


def certify_problem(problem: InterfaceSolverProblem) -> InterfaceSolverCertificate:
    return solve_interface_descent(problem)


def certify_batch(problems: Iterable[InterfaceSolverProblem]) -> Tuple[InterfaceSolverCertificate, ...]:
    return tuple(certify_problem(p) for p in problems)


def certificate_to_dict(cert: InterfaceSolverCertificate) -> Dict[str, Any]:
    return certificate_data(cert)


def certificates_to_jsonable(certs: Iterable[InterfaceSolverCertificate]) -> Dict[str, Any]:
    rows = [certificate_to_dict(c) for c in certs]
    return {
        "certificate_count": len(rows),
        "certificates": rows,
        "summary": summarize_certificates(rows),
    }


def summarize_certificates(rows: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    rows = list(rows)
    status_counts = Counter(row["solver_status"] for row in rows)
    promotion_counts = Counter(row["promotion_status"] for row in rows)
    repair_counts = Counter(row["repair_class"] for row in rows)
    global_exports = [row["problem_name"] for row in rows if row["export_global_P"]]
    held_or_failed = [row["problem_name"] for row in rows if not row["export_global_P"]]
    fail_closed = [row["problem_name"] for row in rows if row["solver_status"] == "FAIL_CLOSED_PROVENANCE"]
    return {
        "total": len(rows),
        "status_counts": dict(status_counts),
        "promotion_counts": dict(promotion_counts),
        "repair_counts": dict(repair_counts),
        "global_exports": global_exports,
        "held_or_failed": held_or_failed,
        "fail_closed": fail_closed,
    }


def certificates_to_csv_rows(certs: Iterable[InterfaceSolverCertificate]) -> Tuple[Tuple[str, ...], ...]:
    header = (
        "problem_name",
        "sector",
        "solver_status",
        "promotion_status",
        "repair_class",
        "obstruction",
        "export_global_P",
        "export_local_P",
        "safe_claim",
        "next_action",
        "route_notes",
    )
    rows: List[Tuple[str, ...]] = [header]
    for cert in certs:
        rows.append((
            cert.problem_name,
            cert.sector,
            cert.solver_status.value,
            cert.promotion_status.value,
            cert.repair_class.value,
            ";".join(cert.obstruction),
            str(cert.export_global_P),
            str(cert.export_local_P),
            cert.safe_claim,
            cert.next_action,
            cert.route_notes,
        ))
    return tuple(rows)
