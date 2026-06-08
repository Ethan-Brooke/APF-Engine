#!/usr/bin/env python3
"""Targeted TraceSector Bank Integration verifier.

Restores the sprint-level 11-check entry point for TraceSector Bank Integration
v1.0.  The 11 checks are intentionally split across upstream modules in the
bank: six were already bank-registered before v8.4 and five live in
apf.trace_sector_closure.  This script gives the release artifact a single
reproducible command without redefining any theorem names.

Usage:
    python scripts/check_trace_sector_integration.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Tuple

# Allow execution directly from a checkout/zip without installation.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apf.down_lepton_trace import (  # noqa: E402
    check_L_residual_down_normalizer_local,
    check_L_bottom_apf_trace,
    check_T_down_lepton_apf_trace_vector,
)
from apf.up_family_trace import check_T_up_family_apf_trace_vector  # noqa: E402
from apf.charged_trace_spectrum import (  # noqa: E402
    check_T_charged_fermion_apf_trace_spectrum,
    check_T_no_inverse_inputs_charged_trace,
)
from apf.trace_sector_closure import (  # noqa: E402
    check_T_W_trace_branch_local,
    check_T_neutrino_boundary_reconciled,
    check_T_qcd_transport_knockouts,
    check_T_ew_trace_sector_closure,
    check_T_apf_trace_sector_closure,
)

CHECKS: List[Tuple[str, Callable[[], Dict[str, Any]]]] = [
    ("check_L_residual_down_normalizer_local", check_L_residual_down_normalizer_local),
    ("check_L_bottom_apf_trace", check_L_bottom_apf_trace),
    ("check_T_down_lepton_apf_trace_vector", check_T_down_lepton_apf_trace_vector),
    ("check_T_up_family_apf_trace_vector", check_T_up_family_apf_trace_vector),
    ("check_T_charged_fermion_apf_trace_spectrum", check_T_charged_fermion_apf_trace_spectrum),
    ("check_T_no_inverse_inputs_charged_trace", check_T_no_inverse_inputs_charged_trace),
    ("check_T_W_trace_branch_local", check_T_W_trace_branch_local),
    ("check_T_neutrino_boundary_reconciled", check_T_neutrino_boundary_reconciled),
    ("check_T_qcd_transport_knockouts", check_T_qcd_transport_knockouts),
    ("check_T_ew_trace_sector_closure", check_T_ew_trace_sector_closure),
    ("check_T_apf_trace_sector_closure", check_T_apf_trace_sector_closure),
]


def passed(result: Dict[str, Any]) -> bool:
    return bool(result.get("passed") is True or str(result.get("status", "")).upper() in {"PASS", "P"})


def compact(result: Dict[str, Any]) -> Dict[str, Any]:
    keep = [
        "name", "passed", "status", "epistemic", "codomain", "scope",
        "exports_physical_scheme_masses", "exports_physical_masses",
        "physical_transport_status", "key_result", "summary",
    ]
    return {k: result[k] for k in keep if k in result}


def run_checks() -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    full: Dict[str, Dict[str, Any]] = {}
    for label, fn in CHECKS:
        try:
            result = fn()
            ok = passed(result)
            rows.append({"check": label, "passed": ok, **compact(result)})
            full[label] = result
        except Exception as exc:  # pragma: no cover - exercised by release script use
            rows.append({"check": label, "passed": False, "error": repr(exc)})
            full[label] = {"passed": False, "error": repr(exc)}
    total = len(rows)
    n_pass = sum(1 for row in rows if row["passed"])
    return {
        "name": "TRACE_SECTOR_BANK_INTEGRATION_PASS" if n_pass == total else "TRACE_SECTOR_BANK_INTEGRATION_FAIL",
        "passed": n_pass == total,
        "n_pass": n_pass,
        "total": total,
        "codomain": "APF_TRACE / W_TRACE only",
        "physical_scheme_transport": "open",
        "rows": rows,
        "full_results": full,
    }


def main() -> int:
    result = run_checks()
    print(json.dumps(result, indent=2, sort_keys=False))
    if result["passed"]:
        print("TRACE_SECTOR_BANK_INTEGRATION_PASS")
        return 0
    print("TRACE_SECTOR_BANK_INTEGRATION_FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
