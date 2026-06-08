#!/usr/bin/env python3
"""Targeted verifier for bottom MSbar transport route v23.0."""
from apf.bottom_msbar_transport import run_all

if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL"), row["name"])
    raise SystemExit(0 if result["passed"] else 1)
