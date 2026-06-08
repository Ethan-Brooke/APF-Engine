#!/usr/bin/env python3
"""Targeted verifier for W_TRACE final export readiness aggregator."""
from apf.w_trace_final_export_readiness import run_all

if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
