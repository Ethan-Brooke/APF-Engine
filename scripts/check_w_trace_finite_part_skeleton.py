#!/usr/bin/env python3
from __future__ import annotations
import importlib, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
MODULE = "apf.w_trace_finite_part_skeleton"; EXPECTED = 18
def _passed(r): return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})
def main() -> int:
    mod = importlib.import_module(MODULE)
    checks = sorted([getattr(mod, n) for n in dir(mod) if n.startswith("check_T_w_finite_part_skeleton")], key=lambda f: f.__name__)
    failures=[]
    for ch in checks:
        r=ch(); st="PASS" if _passed(r) else "FAIL"; print(f"{st:4s} {ch.__name__}")
        if st != "PASS": failures.append((ch.__name__, r))
    print(f"\nW_TRACE finite-part skeleton checks: {len(checks)} / expected {EXPECTED}")
    if len(checks) != EXPECTED: print(f"FAIL expected {EXPECTED} checks, found {len(checks)}"); return 1
    if failures:
        for n,r in failures: print(f"FAIL_DETAIL {n}: {r}")
        return 1
    print("W_TRACE_FINITE_PART_SKELETON_BANK_PASS"); return 0
if __name__ == "__main__": sys.exit(main())
