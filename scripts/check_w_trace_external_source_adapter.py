#!/usr/bin/env python3
"""Targeted verifier for APF v10.0 W_TRACE External Source Adapter Bank."""
from apf.w_trace_external_source_adapter import run_all

if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
