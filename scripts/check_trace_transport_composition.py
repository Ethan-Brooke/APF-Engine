#!/usr/bin/env python3
"""Targeted verifier for the v8.8 Trace Transport Composition Bank.

Passing means every open trace-to-scheme route has an ordered symbolic
composition plan and the forbidden identity route remains non-composable.  It
does not mean physical scheme mass transport is closed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apf.trace_transport_composition import run_all  # noqa: E402


def main() -> int:
    result = run_all()
    print(json.dumps(result, indent=2, sort_keys=False))
    ok = (
        result.get("passed") == result.get("total")
        and result.get("bank_registered") is True
        and result.get("composition_status") == "P_composition"
        and result.get("physical_transport_closed") is False
        and result.get("exports_physical_scheme_masses") is False
    )
    print("TRACE_TRANSPORT_COMPOSITION_BANK_PASS" if ok else "TRACE_TRANSPORT_COMPOSITION_BANK_FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
