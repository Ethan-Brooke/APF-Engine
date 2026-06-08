#!/usr/bin/env python3
"""Targeted verifier for the v9.0 W_TRACE On-Shell Contract Bank.

Passing means the W_TRACE -> on-shell route contract and slot inventory are
banked.  It does not mean numerical W transport or a physical M_W prediction is
closed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apf.w_trace_onshell_transport import run_all  # noqa: E402


def main() -> int:
    result = run_all()
    print(json.dumps(result, indent=2, sort_keys=False))
    ok = (
        result.get("passed") == result.get("total")
        and result.get("bank_registered") is True
        and result.get("route_status") == "P_w_trace_contract"
        and result.get("route_id") == "w_trace_on_shell_route"
        and result.get("route_contract_layer_filled") is True
        and result.get("physical_W_transport_closed") is False
        and result.get("exports_physical_M_W") is False
    )
    if ok:
        print("W_TRACE_ONSHELL_CONTRACT_BANK_PASS")
        return 0
    print("W_TRACE_ONSHELL_CONTRACT_BANK_FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
