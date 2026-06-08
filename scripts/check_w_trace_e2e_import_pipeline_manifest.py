#!/usr/bin/env python3
"""Targeted verifier for W_TRACE E2E import pipeline manifest bank (v12.1)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apf.w_trace_e2e_import_pipeline_manifest import run_all  # noqa: E402


def main() -> int:
    result = run_all()
    rows = result["checks"]
    passed = sum(1 for r in rows if r["passed"])
    total = len(rows)
    for row in rows:
        print(f"{row['name']}: {'PASS' if row['passed'] else 'FAIL'}")
        if not row["passed"]:
            print(row)
    print(f"SUMMARY {passed}/{total} PASS")
    print(result["status"])
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
