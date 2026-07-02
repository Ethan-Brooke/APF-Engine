"""
APF Interface Atlas — Live Adapter Runner.

Auto-discovers `*_real_adapter` modules in apf/, reads each module's atlas
declaration (ATLAS_INPUT_ID, ATLAS_ROUTE, ATLAS_PAYLOAD_NAME,
build_live_atlas_payload), and runs the v0.2 atlas with those CLAIM inputs
swapped for live ROUTE_PAYLOAD inputs. Produces:

- atlas-with-live-adapters JSON result
- per-route delta CSV vs the v0.2 baseline (which adapters lift to
  SOLVED_GLOBAL_P; which preserve OPEN_EVIDENCE_REQUIRED honestly)
- summary line printable for CI / signoff

Adapter contract
----------------
A module is recognized as a wire-in adapter if it lives at apf/*_real_adapter.py
OR apf/*_codomain_adapter.py (v24.3.32+) and exports all four of:

    ATLAS_INPUT_ID: str    # canonical v0.2 atlas input_id to swap (or new id for codomain axis)
    ATLAS_ROUTE: str       # "ew" / "dark" / etc., or "coherent_phase:<regime>" for codomain axis
    ATLAS_PAYLOAD_NAME: str # name to attach to the ROUTE_PAYLOAD swap
    build_live_atlas_payload() -> Dict[str, Any]

Optional v24.3.32+ attribute:

    ATLAS_AXIS: str        # "ROUTE" (default; route-axis adapter) or "CODOMAIN" (codomain-axis adapter)

Modules missing any of the four required attributes are skipped with a NOTE in
the result. ATLAS_AXIS defaults to "ROUTE" for backward compatibility with
v24.3.31-and-earlier adapters that don't declare it.

CLI
---
    python3 -m apf.interface_atlas_live_runner [--json-out PATH] [--csv-out PATH]

Returns nonzero exit if the atlas runner errors. Otherwise prints the
SOLVED_GLOBAL_P count + the wired-adapter table.
"""
from __future__ import annotations

import argparse
import csv
import importlib
import json
import pkgutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# v0.2 atlas runner lives outside apf/ as a script; we import its
# assemble_inputs() function via importlib for now. A future refactor could
# move assemble_inputs() into apf/ proper.
_V02_RUNNER_RELATIVE = (
    "DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/"
    "APF_INTERFACE_ATLAS_V02_FULL_REGISTRY_v1/scripts/run_interface_atlas_v02.py"
)


def _import_v02_runner(codebase_root: Path):
    """Return the v0.2 input-set provider.

    v24.3.307: the canonical source is the vendored in-repo module
    ``apf.interface_atlas_v02_inputs`` (the refactor this docstring block
    previously deferred), so the runner works from the git repo alone.
    The git-ignored Drive-side bundle script is retained as a fallback for
    archival installations that predate the vendoring.
    """
    try:
        from apf import interface_atlas_v02_inputs as mod
        return mod
    except ImportError:
        pass
    import importlib.util
    script_path = codebase_root / _V02_RUNNER_RELATIVE
    if not script_path.exists():
        raise FileNotFoundError(
            f"v0.2 atlas runner not found at {script_path}, and the vendored "
            f"apf.interface_atlas_v02_inputs module failed to import. "
            f"One of the two must be present."
        )
    spec = importlib.util.spec_from_file_location("_v02_runner_import", str(script_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _codebase_root_from_module() -> Path:
    """Locate the codebase root by walking up from apf/."""
    import apf
    apf_dir = Path(apf.__file__).parent
    return apf_dir.parent  # apf/ is one level under codebase root


def discover_adapters() -> Dict[str, Dict[str, Any]]:
    """Walk apf/ for `*_real_adapter` modules with the full atlas contract.

    Returns
    -------
    Mapping from module short-name to {input_id, route, payload_name,
    build_payload, module}. Modules missing any required attribute are
    skipped with a NOTE entry (key prefix "_skipped:").
    """
    import apf as apf_pkg
    discovered: Dict[str, Dict[str, Any]] = {}
    for finder, mod_short, _is_pkg in pkgutil.iter_modules(apf_pkg.__path__):
        if not mod_short.endswith(("_real_adapter", "_codomain_adapter")):
            continue
        full_name = f"apf.{mod_short}"
        try:
            mod = importlib.import_module(full_name)
        except Exception as exc:
            discovered[f"_skipped:{mod_short}"] = {
                "reason": f"import failed: {exc}",
                "module_name": full_name,
            }
            continue
        # Check the four required attributes
        required = ("ATLAS_INPUT_ID", "ATLAS_ROUTE",
                    "ATLAS_PAYLOAD_NAME", "build_live_atlas_payload")
        missing = [a for a in required if not hasattr(mod, a)]
        if missing:
            discovered[f"_skipped:{mod_short}"] = {
                "reason": f"missing atlas-contract attributes: {missing}",
                "module_name": full_name,
            }
            continue
        try:
            payload = mod.build_live_atlas_payload()
        except Exception as exc:
            discovered[f"_skipped:{mod_short}"] = {
                "reason": f"build_live_atlas_payload() raised: {exc}",
                "module_name": full_name,
            }
            continue
        # v24.3.32: capture optional ATLAS_AXIS (defaults to "ROUTE" for backward compat)
        atlas_axis = getattr(mod, "ATLAS_AXIS", "ROUTE")
        discovered[mod_short] = {
            "input_id": mod.ATLAS_INPUT_ID,
            "route": mod.ATLAS_ROUTE,
            "payload_name": mod.ATLAS_PAYLOAD_NAME,
            "payload": payload,
            "module_name": full_name,
            "axis": atlas_axis,
        }
    return discovered


def run_live_atlas(
    *,
    codebase_root: Optional[Path] = None,
    atlas_name: str = "interface_atlas_live",
) -> Dict[str, Any]:
    """Run the v0.2 atlas with live adapter swaps and return a structured result."""
    if codebase_root is None:
        codebase_root = _codebase_root_from_module()
    v02 = _import_v02_runner(codebase_root)
    # Late import keeps the apf.interface_atlas dependency optional for
    # callers that just want adapter-discovery without running the atlas.
    from apf.interface_atlas import AtlasInput, AtlasInputKind, build_interface_atlas

    adapters = discover_adapters()
    swaps = {
        info["input_id"]: info
        for key, info in adapters.items()
        if not key.startswith("_skipped:")
    }
    skipped = {
        key.removeprefix("_skipped:"): info
        for key, info in adapters.items()
        if key.startswith("_skipped:")
    }

    # v24.3.32: import AxisKind for codomain-axis adapter handling
    from apf.interface_atlas import AxisKind

    base_inputs = list(v02.assemble_inputs())

    # v24.3.320 (held-route repair): apply the v0.3 claim-refresh layer --
    # current-disposition texts/flags with banked-check provenance for the
    # six inputs whose frozen 2026-05-18 wording is stale. The vendored v0.2
    # module and canonical_atlas_inputs() are never mutated (archival; the
    # banked check_T_interface_atlas_* certify the canonical set as-is).
    claim_refreshes: List[Dict[str, Any]] = []
    try:
        from apf.interface_atlas_v03_claim_refresh import apply_refresh
        base_inputs, claim_refreshes = apply_refresh(base_inputs)
    except ImportError:
        pass  # pre-.320 checkout
    swapped_inputs: List[Any] = []
    actual_swaps: List[Dict[str, Any]] = []
    for inp in base_inputs:
        if inp.input_id in swaps:
            sw = swaps[inp.input_id]
            axis = AxisKind(sw.get("axis", "ROUTE"))
            kind = (
                AtlasInputKind.CODOMAIN_PAYLOAD
                if axis == AxisKind.CODOMAIN
                else AtlasInputKind.ROUTE_PAYLOAD
            )
            swapped_inputs.append(AtlasInput(
                input_id=f"payload:{sw['payload_name']}",
                kind=kind,
                route=sw["route"],
                claim_text=None,
                payload=sw["payload"],
                axis=axis,
            ))
            actual_swaps.append({
                "original_id": inp.input_id,
                "swapped_id": f"payload:{sw['payload_name']}",
                "route": sw["route"],
                "axis": axis.value,
            })
        else:
            swapped_inputs.append(inp)

    # v24.3.32: also append codomain-axis adapters whose input_id is NOT in the v0.2
    # base atlas (they don't replace existing inputs — they extend the atlas with a
    # new axis). This is the "Path 2 axis-typing" arrival point: codomain adapters
    # are first-class atlas citizens, not synthetic route-axis stand-ins.
    base_input_ids = {inp.input_id for inp in base_inputs}
    for key, info in adapters.items():
        if key.startswith("_skipped:"):
            continue
        if info["input_id"] in base_input_ids:
            continue  # already handled via swap above
        axis = AxisKind(info.get("axis", "ROUTE"))
        if axis != AxisKind.CODOMAIN:
            continue  # non-base route-axis adapter without a matching input_id; skip
        kind = AtlasInputKind.CODOMAIN_PAYLOAD
        new_input_id = info["input_id"]
        swapped_inputs.append(AtlasInput(
            input_id=new_input_id,
            kind=kind,
            route=info["route"],
            claim_text=None,
            payload=info["payload"],
            axis=axis,
        ))
        actual_swaps.append({
            "original_id": "(none; new codomain-axis input)",
            "swapped_id": new_input_id,
            "route": info["route"],
            "axis": axis.value,
        })

    # v24.3.308 (Full Bank Onboarding Wave 1c): append IE_DECLARATIONS inputs
    # discovered manifest-wide, so declaration verdicts appear in the live
    # atlas artifact rather than only inside the onboarding bank check.
    # Declarations never shadow existing atlas ids (registry-wide uniqueness
    # is certified by check_T_ie_onboarding_registry_coverage).
    declaration_rows: List[Dict[str, Any]] = []
    try:
        from apf.ie_onboarding_registry import (
            discover_ie_declarations, compile_declaration,
        )
        decls_by_module, _decl_skips = discover_ie_declarations()
        existing_ids = {inp.input_id for inp in swapped_inputs}
        for owner in sorted(decls_by_module):
            for d in decls_by_module[owner]:
                iid = d.get("input_id")
                if iid in existing_ids:
                    continue
                try:
                    swapped_inputs.append(compile_declaration(d))
                    existing_ids.add(iid)
                    declaration_rows.append({
                        "input_id": iid,
                        "owner_module": owner,
                        "axis": d.get("axis"),
                        "expect_export": d.get("expect_export"),
                    })
                except Exception as exc:  # noqa: BLE001 -- report, don't die
                    declaration_rows.append({
                        "input_id": iid,
                        "owner_module": owner,
                        "axis": d.get("axis"),
                        "compile_error": str(exc),
                    })
    except ImportError:
        pass  # registry not present (pre-.307 checkout); atlas runs without declarations

    atlas = build_interface_atlas(swapped_inputs, atlas_name=atlas_name)
    summaries = atlas.route_summaries

    # attach the delivered verdict to each declaration row
    by_id = {s.input_id: s for s in summaries}
    for row in declaration_rows:
        m = by_id.get(row["input_id"])
        if m is not None:
            row["solver_status"] = str(m.solver_status)
            row["export_global_P"] = bool(m.export_global_P)
            ee = row.get("expect_export")
            if ee is not None:
                row["verdict_matches_expectation"] = (bool(m.export_global_P) == ee)

    global_p_rows = [s for s in summaries if s.export_global_P]
    wired_rows = [s for s in summaries if any(s.input_id.endswith(sw["payload_name"]) for sw in swaps.values())]

    # Build per-adapter result table
    adapter_results: List[Dict[str, Any]] = []
    for sw_info in actual_swaps:
        match = next(
            (s for s in summaries if s.input_id == sw_info["swapped_id"]),
            None,
        )
        if match is None:
            adapter_results.append({
                "original_id": sw_info["original_id"],
                "swapped_id": sw_info["swapped_id"],
                "route": sw_info["route"],
                "axis": sw_info.get("axis", "ROUTE"),
                "solver_status": "NOT_FOUND_IN_SUMMARIES",
                "packet_status": None,
                "export_global_P": False,
            })
        else:
            adapter_results.append({
                "original_id": sw_info["original_id"],
                "swapped_id": sw_info["swapped_id"],
                "route": sw_info["route"],
                "axis": sw_info.get("axis", "ROUTE"),
                "solver_status": str(match.solver_status),
                "packet_status": str(match.packet_status),
                "export_global_P": bool(match.export_global_P),
            })

    return {
        "atlas_name": atlas_name,
        "total_inputs": len(summaries),
        "global_P_count": len(global_p_rows),
        "wired_adapter_count": len(adapter_results),
        "declaration_results": declaration_rows,  # v24.3.308 Wave 1c
        "claim_refreshes": claim_refreshes,  # v24.3.320 held-route repair
        "axis_summary": dict(atlas.axis_summary),  # v24.3.32 per-axis breakdown
        "adapters_discovered": [
            {
                "module": key,
                "input_id": info["input_id"],
                "route": info["route"],
                "payload_name": info["payload_name"],
                "axis": info.get("axis", "ROUTE"),
            }
            for key, info in adapters.items() if not key.startswith("_skipped:")
        ],
        "adapters_skipped": skipped,
        "adapter_results": adapter_results,
        "all_summaries": [
            {
                "input_id": s.input_id,
                "route": s.route,
                "axis": s.axis.value,
                "solver_status": str(s.solver_status),
                "packet_status": str(s.packet_status),
                "export_global_P": bool(s.export_global_P),
            }
            for s in summaries
        ],
    }


def write_csv_report(result: Dict[str, Any], csv_out: Path) -> None:
    """Write a per-adapter delta CSV alongside the JSON result."""
    with csv_out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "original_input_id", "swapped_input_id", "route", "axis",
            "solver_status", "packet_status", "export_global_P",
        ])
        for r in result["adapter_results"]:
            w.writerow([
                r["original_id"], r["swapped_id"], r["route"], r.get("axis", "ROUTE"),
                r["solver_status"], r["packet_status"], r["export_global_P"],
            ])


def print_summary(result: Dict[str, Any]) -> None:
    """Pretty-print the result to stdout — v24.3.32 includes per-axis breakdown."""
    total = result["total_inputs"]
    global_p = result["global_P_count"]
    wired = result["wired_adapter_count"]
    print(f"\nAtlas: {result['atlas_name']}")
    print(f"Total inputs:        {total}")
    print(f"Wired adapters:      {wired}")
    print(f"SOLVED_GLOBAL_P:     {global_p} of {total}")

    # v24.3.32: per-axis breakdown (primary reading per Reference doc Q2)
    axis_summary = result.get("axis_summary", {})
    axis_keys = [k for k in axis_summary if not k.startswith("_")]
    if axis_keys:
        print()
        print("Per-axis breakdown (primary):")
        for axis_key in sorted(axis_keys):
            data = axis_summary[axis_key]
            input_count = data.get("input_count", 0)
            gp = data.get("global_P_count", 0)
            print(f"  axis={axis_key:8}  inputs={input_count:3}  SOLVED_GLOBAL_P={gp:3} of {input_count}")
        if "_cross_axis_note" in axis_summary:
            print(f"  [advisory: top-level flat counts are cross-axis; per-axis above is primary]")

    print()
    print("Wired adapter readings:")
    print(f"  {'axis':9} {'route':28} {'original':45} {'->':4} {'swapped':45} {'solver':32} {'packet':32} {'P':5}")
    for r in result["adapter_results"]:
        mark = "GLOBAL_P" if r["export_global_P"] else "HELD"
        ax = r.get("axis", "ROUTE")
        print(f"  {ax:9} {r['route']:28} {r['original_id']:45} ->   {r['swapped_id']:45} {r['solver_status']:32} {r['packet_status'] or '-':32} {mark:5}")
    if result["adapters_skipped"]:
        print()
        print(f"Adapters skipped ({len(result['adapters_skipped'])}):")
        for name, info in result["adapters_skipped"].items():
            print(f"  {name}: {info['reason']}")


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    p.add_argument("--json-out", type=Path, help="Write structured result JSON to this path.")
    p.add_argument("--csv-out", type=Path, help="Write per-adapter delta CSV to this path.")
    p.add_argument("--quiet", action="store_true", help="Suppress stdout summary.")
    p.add_argument("--atlas-name", default="interface_atlas_live", help="Name for this atlas run.")
    args = p.parse_args(argv)

    result = run_live_atlas(atlas_name=args.atlas_name)

    if args.json_out:
        args.json_out.write_text(json.dumps(result, indent=2, sort_keys=True))
    if args.csv_out:
        write_csv_report(result, args.csv_out)
    if not args.quiet:
        print_summary(result)

    print(f"\nINTERFACE_ATLAS_LIVE_RUNNER_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
