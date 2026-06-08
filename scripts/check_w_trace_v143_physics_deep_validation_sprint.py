#!/usr/bin/env python3
"""Run the W_TRACE v14.3 deep physics validation sprint checks."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from apf import w_trace_cms_global_fit_context as cms
from apf import w_trace_measurement_quarantine_context as meas
from apf import w_trace_correlated_uncertainty_model as corr
from apf import w_trace_delta_r_pull_diagnostics as pulls
from apf import w_trace_v143_physics_deep_validation_report as report

MODULES=[cms,meas,corr,pulls,report]

def main()->int:
    total=0; passed=0
    for mod in MODULES:
        out=mod.run_all(); print(out["status"]); n=sum(1 for r in out["checks"] if r["passed"]); t=len(out["checks"]); passed+=n; total+=t; print(f"  {mod.__name__}: {n}/{t} PASS")
        if not out["passed"]: return 1
    print(f"SUMMARY {passed}/{total} PASS")
    print("W_TRACE_V14_3_PHYSICS_DEEP_VALIDATION_SPRINT_PASS")
    return 0
if __name__=="__main__": raise SystemExit(main())
