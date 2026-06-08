#!/usr/bin/env python3
from __future__ import annotations

import json
from apf.w_os_route_terminal_closure import run_all


def main() -> int:
    payload = run_all()
    print(json.dumps(payload, indent=2, default=str))
    if payload.get("passed") == payload.get("total"):
        print("W_OS_ROUTE_TERMINAL_CLOSURE_BANK_PASS")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
