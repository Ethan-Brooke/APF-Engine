#!/usr/bin/env python3
"""Targeted verifier for the v8.9 Trace Transport Completion Gate Bank.

Passing means the terminal physical-export predicate is banked and the current
codebase is certified *not* to export physical scheme masses until the required
transport maps, external ledgers, counterterms, and uncertainty protocol are
filled.  It does not mean physical scheme mass transport is closed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apf.trace_transport_completion import run_all  # noqa: E402


def main() -> int:
    result = run_all()
    print(json.dumps(result, indent=2, sort_keys=False))
    ok = (
        result.get("passed") == result.get("total")
        and result.get("bank_registered") is True
        and result.get("completion_status") == "P_completion_gate"
        and result.get("physical_transport_closed") is False
        and result.get("exports_physical_scheme_masses") is False
    )
    if ok:
        print("TRACE_TRANSPORT_COMPLETION_GATE_BANK_PASS")
        return 0
    print("TRACE_TRANSPORT_COMPLETION_GATE_BANK_FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
