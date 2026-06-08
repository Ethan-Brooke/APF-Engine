#!/usr/bin/env python3
"""Verifier for v14.1 W_TRACE ACFW Delta_r extraction attempt."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from apf import w_trace_acfw_delta_r_extraction_attempt as mod
PASS_STATUS = "W_TRACE_ACFW_DELTA_R_EXTRACTION_ATTEMPT_BANK_PASS"

def main() -> int:
    report = mod.run_all()
    rows = report["checks"]
    passed = sum(1 for r in rows if r["passed"])
    total = len(rows)
    for row in rows:
        if not row["passed"]:
            print(f"FAIL {row['name']}: {row.get('error') or row.get('result')}")
    payload = report["report"]["payload"]
    print(f"SUMMARY {passed}/{total} PASS")
    print(f"M_W_source_GeV={payload['M_W_source_GeV']:.12f}")
    print(f"Delta_r_source_total={payload['Delta_r_source_total']:.18f}")
    print(f"Delta_r_source_minus_APF={payload['Delta_r_source_minus_APF']:.18f}")
    print(f"abs_M_W_gap_MeV={payload['abs_M_W_gap_MeV']:.6f}")
    print(PASS_STATUS if report["passed"] else PASS_STATUS.replace("_PASS", "_FAIL"))
    return 0 if report["passed"] else 1
if __name__ == "__main__":
    raise SystemExit(main())
