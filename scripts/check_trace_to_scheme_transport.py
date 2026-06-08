#!/usr/bin/env python3
"""Targeted verifier for the Trace-to-Scheme Transport boundary bank.

Passing means the trace-to-scheme problem is correctly staged at the bank level:
APF_TRACE/W_TRACE closure remains local, physical transport remains open, and
scheme/scale/running/threshold/counterterm/no-smuggling guardrails are explicit.
It does not mean physical scheme mass transport is closed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apf.trace_scheme_transport import run_all  # noqa: E402


def main() -> int:
    result = run_all()
    print(json.dumps(result, indent=2, sort_keys=False))
    ok = (
        result.get("passed") == result.get("total")
        and result.get("bank_registered") is True
        and result.get("physical_transport_closed") is False
    )
    print("TRACE_TO_SCHEME_BOUNDARY_BANK_PASS" if ok else "TRACE_TO_SCHEME_BOUNDARY_BANK_FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
