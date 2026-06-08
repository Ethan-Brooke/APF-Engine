#!/usr/bin/env python3
"""Targeted verifier for the W_TRACE release runbook bank."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apf.w_trace_release_runbook import CHECKS, run_all  # noqa: E402


def main() -> int:
    result = run_all()
    rows = result["checks"]
    for row in rows:
        print(f"{row['name']}: {'PASS' if row['passed'] else 'FAIL'}")
    print(f"SUMMARY {sum(1 for r in rows if r['passed'])}/{len(rows)} PASS")
    print(result["status"])
    return 0 if result["passed"] and len(CHECKS) == 32 else 1


if __name__ == "__main__":
    raise SystemExit(main())
