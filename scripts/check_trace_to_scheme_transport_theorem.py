#!/usr/bin/env python3
from __future__ import annotations

import json

from apf.trace_to_scheme_transport_theorem import (
    check_T_transport_theorem_upstream_banks_closed,
    check_T_admissible_transport_definition_complete,
    check_T_transport_export_iff_certificate_complete,
    check_T_route_specific_theorem_clauses_enumerated,
    check_T_w_trace_on_shell_route_theorem_obligations,
    check_T_bottom_msbar_route_theorem_obligations,
    check_T_no_inverse_fit_transport_theorem,
    check_T_residuals_are_transport_observables_not_contradictions,
    check_T_trace_to_scheme_transport_theorem_bank_closure,
)

CHECKS = [
    check_T_transport_theorem_upstream_banks_closed,
    check_T_admissible_transport_definition_complete,
    check_T_transport_export_iff_certificate_complete,
    check_T_route_specific_theorem_clauses_enumerated,
    check_T_w_trace_on_shell_route_theorem_obligations,
    check_T_bottom_msbar_route_theorem_obligations,
    check_T_no_inverse_fit_transport_theorem,
    check_T_residuals_are_transport_observables_not_contradictions,
    check_T_trace_to_scheme_transport_theorem_bank_closure,
]


def main() -> int:
    results = []
    for check in CHECKS:
        try:
            result = check()
            passed = bool(result.get("passed") is True)
        except Exception as exc:  # pragma: no cover - diagnostic script
            result = {"name": check.__name__, "passed": False, "error": repr(exc)}
            passed = False
        results.append({"name": result.get("name", check.__name__), "passed": passed, "result": result})
    passed_count = sum(1 for r in results if r["passed"])
    payload = {
        "passed": passed_count,
        "total": len(results),
        "status": "TRACE_TO_SCHEME_TRANSPORT_THEOREM_BANK_PASS" if passed_count == len(results) else "TRACE_TO_SCHEME_TRANSPORT_THEOREM_BANK_FAIL",
        "bank_registered": passed_count == len(results),
        "transport_theorem_status": "P_transport_theorem",
        "physical_transport_closed": False,
        "exports_physical_scheme_masses": False,
        "results": results,
    }
    print(json.dumps(payload, indent=2))
    if passed_count == len(results):
        print("TRACE_TO_SCHEME_TRANSPORT_THEOREM_BANK_PASS")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
