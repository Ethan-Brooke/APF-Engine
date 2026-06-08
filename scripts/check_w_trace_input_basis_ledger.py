#!/usr/bin/env python3
"""Targeted verifier for the v9.1 W_TRACE Input-Basis Ledger Bank.

Passing means the W_TRACE -> on-shell input-basis ledger is selected and
provenance/no-smuggling gated.  It does not mean numerical EW constants,
Delta_r, uncertainty propagation, or a physical M_W prediction are closed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apf.w_trace_input_basis_ledger import run_all  # noqa: E402


def main() -> int:
    result = run_all()
    print(json.dumps(result, indent=2, sort_keys=False))
    ok = (
        result.get("passed") == result.get("total")
        and result.get("bank_registered") is True
        and result.get("route_status") == "P_w_input_basis_ledger"
        and result.get("route_id") == "w_trace_on_shell_route"
        and result.get("selected_basis") == "on-shell alpha/M_Z/G_F-style input basis"
        and result.get("input_basis_ledger_filled") is True
        and result.get("numerical_EW_constants_filled") is False
        and result.get("delta_r_evaluated") is False
        and result.get("physical_W_transport_closed") is False
        and result.get("exports_physical_M_W") is False
    )
    if ok:
        print("W_TRACE_INPUT_BASIS_LEDGER_BANK_PASS")
        return 0
    print("W_TRACE_INPUT_BASIS_LEDGER_BANK_FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
