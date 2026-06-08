#!/usr/bin/env python3
"""Targeted verifier for APF v9.7 W_TRACE numeric-source adapter bank."""
from apf.w_trace_numeric_source_adapter import run_all

if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
