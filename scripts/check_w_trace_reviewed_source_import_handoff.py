#!/usr/bin/env python3
"""Targeted verifier for W_TRACE reviewed-source import handoff bank."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apf.w_trace_reviewed_source_import_handoff import CHECKS, _passed, run_all


def main() -> int:
    results = []
    for name, fn in CHECKS.items():
        try:
            r = fn()
            ok = _passed(r)
            results.append(ok)
            print(f"{name}: {'PASS' if ok else 'FAIL'}")
            if not ok:
                print(r)
        except Exception as exc:
            results.append(False)
            print(f"{name}: ERROR {exc!r}")
    ok = all(results)
    print(f"SUMMARY {sum(results)}/{len(results)} PASS")
    print("W_TRACE_REVIEWED_SOURCE_IMPORT_HANDOFF_BANK_PASS" if ok else "W_TRACE_REVIEWED_SOURCE_IMPORT_HANDOFF_BANK_FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
