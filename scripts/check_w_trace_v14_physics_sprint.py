#!/usr/bin/env python3
"""Combined verifier for the v14.0 W_TRACE physics-source acquisition sprint."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from apf import w_trace_acfw_candidate_preflight as m1
from apf import w_trace_denner_sirlin_notation_map as m2
from apf import w_trace_standard_delta_r_payload_schema as m3
from apf import w_trace_delta_r_comparison_harness as m4
from apf import w_trace_physics_source_stop_condition as m5
from apf import w_trace_v14_physics_sprint_terminal_report as m6
MODULES = (m1, m2, m3, m4, m5, m6)
PASS_STATUS = "W_TRACE_V14_PHYSICS_SOURCE_ACQUISITION_SPRINT_PASS"

def main() -> int:
    total = passed = 0
    for mod in MODULES:
        report = mod.run_all()
        rows = report["checks"]
        p = sum(1 for r in rows if r["passed"])
        total += len(rows); passed += p
        print(f"{mod.__name__}: {p}/{len(rows)} PASS -- {report['status']}")
        for row in rows:
            if not row["passed"]:
                print(f"FAIL {row['name']}: {row.get('error') or row.get('result')}")
    print(f"SUMMARY {passed}/{total} PASS")
    print(PASS_STATUS if passed == total else PASS_STATUS.replace("_PASS", "_FAIL"))
    return 0 if passed == total else 1
if __name__ == "__main__":
    raise SystemExit(main())
