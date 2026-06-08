#!/usr/bin/env python3
"""Verifier for v14.2 W_TRACE physics validation sprint."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from apf import w_trace_input_convention_stress_test as stress
from apf import w_trace_independent_delta_r_crosscheck as cross
from apf import w_trace_multisource_delta_r_comparison as multi
from apf import w_trace_v142_physics_validation_sprint_report as terminal
PASS_STATUS="W_TRACE_V14_2_PHYSICS_VALIDATION_SPRINT_PASS"
MODULES=(stress,cross,multi,terminal)
def main() -> int:
    total=passed=0
    for mod in MODULES:
        rep=mod.run_all(); rows=rep["checks"]; p=sum(1 for r in rows if r["passed"]); t=len(rows); total+=t; passed+=p
        print(f"{mod.__name__.split('.')[-1]}: {p}/{t} PASS")
        for r in rows:
            if not r["passed"]: print(f"  FAIL {r['name']}: {r.get('error') or r.get('result')}")
    print(f"SUMMARY {passed}/{total} PASS")
    print("weighted", multi.weighted_summary())
    print(PASS_STATUS if passed==total else PASS_STATUS.replace("_PASS","_FAIL"))
    return 0 if passed==total else 1
if __name__=="__main__": raise SystemExit(main())
