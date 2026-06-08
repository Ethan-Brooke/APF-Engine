#!/usr/bin/env python3
"""Targeted verifier for the v9.5 W_TRACE finite-part evaluator gate bank.

Passing means the independent evaluator / component-sum certificate gate is
banked.  It does not mean the finite parts have been independently evaluated,
the component sum has been certified, or a physical W value has been exported.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apf.w_trace_finite_part_evaluator_gate import run_all  # noqa: E402


def main() -> int:
    result = run_all()
    print(json.dumps(result, indent=2, sort_keys=False))
    ok = (
        result.get("passed") == result.get("total")
        and result.get("bank_registered") is True
        and result.get("route_status") == "P_w_finite_part_evaluator_gate"
        and result.get("route_id") == "w_trace_on_shell_route"
        and result.get("upstream_status") == "P_w_finite_part_ledger"
        and result.get("independent_component_values_supplied") is False
        and result.get("independent_counterterm_supplied") is False
        and result.get("component_sum_certified") is False
        and result.get("covariance_protocol_supplied") is False
        and result.get("uncertainty_protocol_supplied") is False
        and result.get("physical_W_transport_closed") is False
        and result.get("exports_physical_M_W") is False
        and result.get("exports_physical_scheme_masses") is False
    )
    if ok:
        print("W_TRACE_FINITE_PART_EVALUATOR_GATE_BANK_PASS")
        return 0
    print("W_TRACE_FINITE_PART_EVALUATOR_GATE_BANK_FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
