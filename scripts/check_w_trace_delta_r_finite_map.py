#!/usr/bin/env python3
"""Targeted verifier for the v9.3 W_TRACE Delta_r symbolic-map bank.

Passing means the W on-shell finite-correction / Delta_r map is typed and
banked symbolically.  It does not mean Delta_r, counterterms, uncertainty
propagation, physical M_W, or physical scheme masses are numerically closed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apf.w_trace_delta_r_finite_map import run_all  # noqa: E402


def main() -> int:
    result = run_all()
    print(json.dumps(result, indent=2, sort_keys=False))
    ok = (
        result.get("passed") == result.get("total")
        and result.get("bank_registered") is True
        and result.get("route_status") == "P_w_delta_r_symbolic_map"
        and result.get("route_id") == "w_trace_on_shell_route"
        and result.get("delta_r_symbolic_map_declared") is True
        and result.get("delta_r_numerically_evaluated") is False
        and result.get("finite_counterterms_evaluated") is False
        and result.get("physical_W_transport_closed") is False
        and result.get("exports_physical_M_W") is False
        and result.get("exports_physical_scheme_masses") is False
    )
    if ok:
        print("W_TRACE_DELTA_R_SYMBOLIC_MAP_BANK_PASS")
        return 0
    print("W_TRACE_DELTA_R_SYMBOLIC_MAP_BANK_FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
