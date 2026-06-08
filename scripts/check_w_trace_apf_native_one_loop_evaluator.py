#!/usr/bin/env python3
"""Targeted verifier for W_TRACE APF-native one-loop evaluator scaffold v16.6."""
from apf.w_trace_apf_native_one_loop_evaluator import run_all

if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
