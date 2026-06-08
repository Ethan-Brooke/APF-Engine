#!/usr/bin/env python3
"""Targeted verifier for the v8.7 Trace Transport Routes Bank.

Passing means the trace-to-scheme problem has been split into named route
classes with explicit prerequisites and forbidden identity transport.  It does
not mean physical scheme mass transport is closed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apf.trace_transport_routes import run_all  # noqa: E402


def main() -> int:
    result = run_all()
    print(json.dumps(result, indent=2, sort_keys=False))
    ok = (
        result.get("passed") == result.get("total")
        and result.get("bank_registered") is True
        and result.get("route_status") == "P_route"
        and result.get("physical_transport_closed") is False
        and result.get("exports_physical_scheme_masses") is False
    )
    print("TRACE_TRANSPORT_ROUTES_BANK_PASS" if ok else "TRACE_TRANSPORT_ROUTES_BANK_FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
