#!/usr/bin/env python3
"""Targeted verifier for APF v10.1 W_TRACE External Ingestion Dry-Run Bank."""
from apf.w_trace_external_ingestion_dryrun import run_all

if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
