#!/usr/bin/env python3
"""Targeted verifier for the v8.6 Trace Transport Ledger Bank.

Passing means the architecture for future trace-to-scheme transport is banked:
trace inputs are immutable, target schemes require explicit contracts, external
constants/counterterms/uncertainties are ledger slots, and target physical
masses are barred as inverse inputs.  It does not mean physical scheme mass
transport is closed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apf.trace_transport_ledger import run_all  # noqa: E402


def main() -> int:
    result = run_all()
    print(json.dumps(result, indent=2, sort_keys=False))
    ok = (
        result.get("passed") == result.get("total")
        and result.get("bank_registered") is True
        and result.get("physical_transport_closed") is False
        and result.get("exports_physical_scheme_masses") is False
    )
    print("TRACE_TRANSPORT_LEDGER_BANK_PASS" if ok else "TRACE_TRANSPORT_LEDGER_BANK_FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
