#!/usr/bin/env python3
"""Targeted verifier for the W_TRACE admitted-row covariance bridge bank."""
from apf.w_trace_admitted_row_covariance_bridge import CHECKS


def _passed(r):
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def main() -> int:
    failures = []
    for name, fn in CHECKS.items():
        out = fn()
        ok = _passed(out)
        print(("PASS" if ok else "FAIL") + " " + name)
        if not ok:
            failures.append((name, out))
    print(f"SUMMARY {len(CHECKS)-len(failures)}/{len(CHECKS)} PASS")
    if failures:
        print("W_TRACE_ADMITTED_ROW_COVARIANCE_BRIDGE_BANK_FAIL")
        return 1
    print("W_TRACE_ADMITTED_ROW_COVARIANCE_BRIDGE_BANK_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
