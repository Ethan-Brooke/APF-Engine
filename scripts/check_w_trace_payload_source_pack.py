#!/usr/bin/env python3
"""Targeted verifier for APF v9.9 W_TRACE Payload Source Pack Bank."""
from apf.w_trace_payload_source_pack import run_all

if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
