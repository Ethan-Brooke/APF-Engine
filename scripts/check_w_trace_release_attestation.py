#!/usr/bin/env python3
"""Targeted verifier for W_TRACE release attestation / immutable manifest digest bank."""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from apf.w_trace_release_attestation import run_all

if __name__ == "__main__":
    result = run_all()
    rows = result["checks"]
    passed = sum(1 for r in rows if r["passed"])
    total = len(rows)
    for row in rows:
        status = "PASS" if row["passed"] else "FAIL"
        print(f"{status} {row['name']}")
        if not row["passed"]:
            print(row)
    print(f"SUMMARY {passed}/{total} PASS")
    print(result["status"])
    raise SystemExit(0 if result["passed"] else 1)
