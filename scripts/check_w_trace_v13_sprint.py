#!/usr/bin/env python3
"""Combined targeted verifier for W_TRACE v13.0 terminal sprint."""
from __future__ import annotations
import importlib, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
MODULES = [
    'apf.w_trace_signature_verification_adapter',
    'apf.w_trace_signed_release_replay',
    'apf.w_trace_release_evidence_bundle',
    'apf.w_trace_terminal_state_report',
    'apf.w_trace_next_payload_requirements',
]

def main() -> int:
    total = passed = 0
    failures = []
    for modname in MODULES:
        mod = importlib.import_module(modname)
        result = mod.run_all()
        rows = result['checks']
        p = sum(1 for row in rows if row['passed'])
        total += len(rows); passed += p
        print(f"{modname}: {p}/{len(rows)} {'PASS' if result['passed'] else 'FAIL'}")
        if not result['passed']:
            failures.extend((modname, row) for row in rows if not row['passed'])
    print(f"SUMMARY {passed}/{total} PASS")
    status = 'W_TRACE_V13_TERMINAL_INFRASTRUCTURE_SPRINT_PASS' if passed == total else 'W_TRACE_V13_TERMINAL_INFRASTRUCTURE_SPRINT_FAIL'
    print(status)
    if failures:
        for modname, row in failures:
            print(modname, row)
    return 0 if passed == total else 1

if __name__ == '__main__':
    raise SystemExit(main())
