#!/usr/bin/env python3
"""Targeted verifier for the v9.2 W_TRACE Constants-Source Ledger Bank.

Passing means the allowed non-W EW input constants have source-tagged numerical
records.  It does not mean Delta_r, finite counterterms, covariance propagation,
uncertainty propagation, physical M_W, or physical scheme masses are closed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apf.w_trace_constants_source_ledger import run_all  # noqa: E402


def main() -> int:
    result = run_all()
    print(json.dumps(result, indent=2, sort_keys=False))
    ok = (
        result.get("passed") == result.get("total")
        and result.get("bank_registered") is True
        and result.get("route_status") == "P_w_constants_source_ledger"
        and result.get("route_id") == "w_trace_on_shell_route"
        and result.get("constants_source_ledger_filled") is True
        and result.get("numerical_EW_constants_filled") is True
        and result.get("delta_r_evaluated") is False
        and result.get("counterterm_finite_parts_evaluated") is False
        and result.get("correlation_propagation_evaluated") is False
        and result.get("uncertainty_protocol_evaluated") is False
        and result.get("physical_W_transport_closed") is False
        and result.get("exports_physical_M_W") is False
    )
    if ok:
        print("W_TRACE_CONSTANTS_SOURCE_LEDGER_BANK_PASS")
        return 0
    print("W_TRACE_CONSTANTS_SOURCE_LEDGER_BANK_FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
