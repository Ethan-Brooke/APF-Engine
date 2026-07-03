#!/usr/bin/env python3
"""Generate the IE Onboarding Dashboard data payload (Full Bank Onboarding, Phase 4).

Runs the coverage map (apf.ie_onboarding_registry.coverage_map) + the live atlas
(apf.interface_atlas_live_runner.run_live_atlas) and writes ONE JSON payload for
the Cowork dashboard artifact. Architecture-only tooling: no bank checks, no
physics; the payload is a snapshot of instrument outputs.

Usage (from repo root):
    python3 scripts/gen_ie_onboarding_dashboard_data.py [--out PATH]

Refresh pattern (signoff or on demand): re-run this script, splice the fresh
JSON into the artifact HTML (single DASHBOARD_DATA constant), update the
artifact via update_artifact. Same mount-independent pattern as the
apf-top-of-mind sync (wiki/Log.md 2026-06-21 LATER-5).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone


def build_payload() -> dict:
    from apf import _module_manifest as manifest
    from apf.ie_onboarding_registry import coverage_map, ONBOARDED_MODULE_FLOOR
    from apf.interface_atlas_live_runner import run_live_atlas

    cov = coverage_map()
    atlas = run_live_atlas(atlas_name="ie_onboarding_dashboard_snapshot")

    # slim the atlas rows to what the dashboard renders
    rows = []
    for s in atlas.get("all_summaries", []):
        get = s.get if isinstance(s, dict) else lambda k, d=None: getattr(s, k, d)
        rows.append({
            "input_id": get("input_id"),
            "route": get("route"),
            "axis": get("axis", "ROUTE"),
            "solver_status": str(get("solver_status")),
            "export_global_P": bool(get("export_global_P")),
        })

    import apf
    version = None
    try:
        import re
        setup_src = open("setup.py", encoding="utf-8").read()
        m = re.search(r"version='([^']+)'", setup_src)
        version = m.group(1) if m else None
    except Exception:
        pass

    return {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "codebase_version": version,
        "expected_registry_size": manifest.EXPECTED_REGISTRY_SIZE,
        "floor": ONBOARDED_MODULE_FLOOR,
        "coverage_summary": cov["summary"],
        "coverage_rows": cov["rows"],
        "atlas": {
            "total_inputs": atlas.get("total_inputs"),
            "global_P_count": atlas.get("global_P_count"),
            "wired_adapter_count": atlas.get("wired_adapter_count"),
            "declaration_results": atlas.get("declaration_results", []),
            "rows": rows,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="ie_onboarding_dashboard_data.json")
    ap.add_argument("--with-crystal", action="store_true",
                    help="append the crystal spine grade census + strengthening "
                         "ledger (CORE view; ~20 s extra: registry load + "
                         "build_crystal + betweenness). The disposition map is "
                         "curated in apf/crystal_ledger_dispositions.py.")
    args = ap.parse_args()
    payload = build_payload()
    if args.with_crystal:
        from apf.crystal_ledger import crystal_dashboard_section
        payload["crystal"] = crystal_dashboard_section()
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=1, default=str)
    s = payload["coverage_summary"]
    print("wrote %s  (coverage %d/%d direct %d, target %d/%d; atlas %d inputs)" % (
        args.out, s["modules_onboarded"], s["modules_total"],
        s["modules_onboarded_direct"], s["target_surface_onboarded"],
        s["target_surface_total"], payload["atlas"]["total_inputs"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
