#!/usr/bin/env python3
"""Targeted verifier for W_TRACE v14 physics-source sprint terminal report."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from apf import w_trace_v14_physics_sprint_terminal_report as mod

def main() -> int:
    report = mod.run_all()
    rows = report["checks"]
    passed = sum(1 for r in rows if r["passed"])
    total = len(rows)
    for row in rows:
        status = "PASS" if row["passed"] else "FAIL"
        print(f"{status:4} {row['name']}")
        if not row["passed"]:
            print(f"      {row.get('error') or row.get('result')}")
    print(f"SUMMARY {passed}/{total} PASS")
    print(report["status"])
    return 0 if report["passed"] and report["status"] == mod.PASS_STATUS else 1

if __name__ == "__main__":
    raise SystemExit(main())
