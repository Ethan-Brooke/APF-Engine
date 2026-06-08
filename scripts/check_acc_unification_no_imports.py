#!/usr/bin/env python3
"""Targeted verifier for ACC unification fully-P no-import closure."""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    mod = importlib.import_module("apf.acc_unification_no_imports")
except Exception as exc:
    print("ACC_UNIFICATION_NO_IMPORTS_IMPORT_FAIL")
    print(repr(exc))
    raise SystemExit(2)

results = mod.run_all()
print(json.dumps(results, indent=2, sort_keys=True))

top = results.get("check_T_ACC_unification_fully_P_no_external_imports", {})
no_imports = results.get("check_T_no_external_physical_imports_P", {})
boundary = results.get("check_T_no_bare_record_overclaim_P", {})
ok = all(x.get("consistent") for x in results.values())

if (
    ok
    and top.get("status") == "P_cat_fully_closed_no_imports"
    and top.get("data", {}).get("external_physical_imports") is False
    and no_imports.get("status") == "P_audit"
    and boundary.get("data", {}).get("bare_record_only_collapse_claimed") is False
):
    print("ACC_UNIFICATION_FULLY_P_NO_EXTERNAL_IMPORTS_PASS")
    raise SystemExit(0)

print("ACC_UNIFICATION_FULLY_P_NO_EXTERNAL_IMPORTS_FAIL")
raise SystemExit(1)
