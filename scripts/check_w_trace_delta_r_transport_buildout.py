#!/usr/bin/env python3
"""Targeted verifier for W_TRACE Delta_r transport buildout."""
from apf.w_trace_delta_r_transport_buildout import run_all

if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
