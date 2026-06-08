#!/usr/bin/env python3
"""Sprint D — Interface atlas v0.1 over real APF sectors.

Feeds the real obligation packets produced by Sprints B (EW) and C (dark)
into the interface atlas, plus synthetic claim-text inputs for the gauge
and horizon sectors, and runs the atlas to identify cross-sector
obstruction families, shared repair dependencies, and bottleneck
structures.

The atlas v0.1 reading:
  - obstruction_counts: how often each obstruction channel fires across routes
  - failed_kind_counts: how often each structural kind is missing
  - critical_field_counts: which repair fields show up across sectors
  - global_bottlenecks: the highest-frequency obstructions across all routes
  - shared_repair_fields: repair fields that appear in multiple sectors

Output: a JSON artifact at ``Evidence/interface_atlas_v01_*.json``
plus a Markdown summary at ``Evidence/interface_atlas_v01_*.md``.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

CODEBASE = Path("/sessions/laughing-epic-brahmagupta/mnt/__APF Library/Codebase/APF_Codebase_v24.3")
EVIDENCE = Path("/sessions/laughing-epic-brahmagupta/mnt/__APF Library/Evidence")
sys.path.insert(0, str(CODEBASE))

from apf import bank  # noqa: E402
from apf.interface_atlas import AtlasInput, AtlasInputKind, build_interface_atlas  # noqa: E402
from apf.ew_trace_to_scheme_real_adapter import build_live_adapter_report as ew_live_report  # noqa: E402
from apf.dark_posterior_real_adapter import build_live_adapter_report as dark_live_report  # noqa: E402


def _build_live_inputs() -> list:
    """Construct AtlasInputs from live adapter snapshots + synthetic claims."""
    inputs = []

    # EW from live adapter snapshot
    ew_report = ew_live_report(name="atlas_input_ew_live")
    inputs.append(
        AtlasInput(
            input_id="ew_live",
            kind=AtlasInputKind.ROUTE_PAYLOAD,
            route="ew",
            claim_text=None,
            payload=dict(ew_report.payload),
        )
    )

    # Dark from live adapter snapshot
    dark_report = dark_live_report(name="atlas_input_dark_live")
    inputs.append(
        AtlasInput(
            input_id="dark_live",
            kind=AtlasInputKind.ROUTE_PAYLOAD,
            route="dark",
            claim_text=None,
            payload=dict(dark_report.payload),
        )
    )

    # Synthetic claim inputs for two additional sectors — exercises the claim
    # compiler path of the atlas (vs. the route-payload path used above).
    inputs.append(
        AtlasInput(
            input_id="gauge_claim",
            kind=AtlasInputKind.CLAIM,
            route="gauge",
            claim_text="The gauge group SU(3)_c x SU(2)_L x U(1)_Y is the unique structure that supports the four PLEC features at quantum-capable interfaces.",
            payload=None,
        )
    )
    inputs.append(
        AtlasInput(
            input_id="horizon_claim",
            kind=AtlasInputKind.CLAIM,
            route="horizon",
            claim_text="The horizon-area-as-fiber-cost reading recovers the Bekenstein bound from the substrate's V_global capacity ceiling.",
            payload=None,
        )
    )

    return inputs


def main() -> int:
    print("INTERFACE ATLAS v0.1 — over real APF sectors")
    print(f"  apf bank EXPECTED_THEOREM_COUNT: {bank.EXPECTED_THEOREM_COUNT}")
    print()

    t0 = time.time()
    inputs = _build_live_inputs()
    print(f"  Built {len(inputs)} atlas inputs")
    for inp in inputs:
        kind = inp.kind.value
        route = inp.route
        print(f"    - {inp.input_id:20s} kind={kind:14s} route={route}")
    print()

    atlas = build_interface_atlas(inputs, atlas_name="APF_interface_atlas_v0.1_real_sectors")
    elapsed = time.time() - t0
    print(f"  Atlas built in {elapsed:.2f}s")
    atlas_dict = atlas.to_dict()

    # Route-by-route summary
    print()
    print("  --- Route summaries ---")
    for rs in atlas.route_summaries:
        print(f"    [{rs.solver_status}] {rs.input_id:20s} route={rs.route:8s} export_global_P={rs.export_global_P}")
        if rs.obstruction:
            print(f"        obstruction: {rs.obstruction}")
        if rs.critical_fields:
            print(f"        critical_fields: {rs.critical_fields}")
    print()

    # Obstruction frequency
    print("  --- Obstruction frequency across all sectors ---")
    for chan, count in sorted(atlas.obstruction_counts.items(), key=lambda kv: -kv[1]):
        print(f"    {chan:35s} {count}")
    print()

    print("  --- Failed structural-kind frequency ---")
    for kind, count in sorted(atlas.failed_kind_counts.items(), key=lambda kv: -kv[1]):
        print(f"    {kind:35s} {count}")
    print()

    print("  --- Critical-repair-field frequency (top shared) ---")
    for fld, count in sorted(atlas.critical_field_counts.items(), key=lambda kv: -kv[1])[:10]:
        print(f"    {fld:45s} {count}")
    print()

    print("  --- Route-status distribution ---")
    for status, count in sorted(atlas.route_status_counts.items(), key=lambda kv: -kv[1]):
        print(f"    {status:40s} {count}")
    print()

    print("  --- Global bottlenecks (top obstructions across atlas) ---")
    for item in atlas.global_bottlenecks[:5]:
        print(f"    {item[0]:35s} {item[1]}")
    print()

    print("  --- Shared repair fields (appear in multiple sectors) ---")
    for item in atlas.shared_repair_fields[:5]:
        print(f"    {item[0]:45s} appears in {item[1]} routes")
    print()

    print(f"  --- Coverage ---")
    for k, v in atlas.coverage.items():
        print(f"    {k:35s} {v}")
    print()

    # Persist JSON artifact
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
    artifact_path = EVIDENCE / f"interface_atlas_v01_{ts}.json"
    artifact = {
        "atlas_version": "v0.1",
        "codebase_version": "24.3.17",
        "bank_expected_count": bank.EXPECTED_THEOREM_COUNT,
        "wall_seconds": round(elapsed, 3),
        "atlas": atlas_dict,
    }
    artifact_path.write_text(json.dumps(artifact, indent=2, default=str), encoding="utf-8")
    print(f"  JSON artifact: {artifact_path}")

    # Persist Markdown summary
    md_path = EVIDENCE / f"interface_atlas_v01_{ts}.md"
    md_lines = []
    md_lines.append(f"# Interface Atlas v0.1 — APF live sectors")
    md_lines.append(f"")
    md_lines.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    md_lines.append(f"Codebase: v24.3.17 (bank EXPECTED {bank.EXPECTED_THEOREM_COUNT})")
    md_lines.append(f"")
    md_lines.append(f"## Atlas inputs ({len(inputs)})")
    md_lines.append(f"")
    md_lines.append("| Input ID | Kind | Route |")
    md_lines.append("|---|---|---|")
    for inp in inputs:
        md_lines.append(f"| {inp.input_id} | {inp.kind.value} | {inp.route} |")
    md_lines.append("")
    md_lines.append("## Route summaries")
    md_lines.append("")
    md_lines.append("| Input | Route | Solver status | Export P | Obstruction | Critical fields |")
    md_lines.append("|---|---|---|---|---|---|")
    for rs in atlas.route_summaries:
        obs = ", ".join(rs.obstruction) if rs.obstruction else "—"
        crit = ", ".join(rs.critical_fields) if rs.critical_fields else "—"
        md_lines.append(f"| {rs.input_id} | {rs.route} | `{rs.solver_status}` | {rs.export_global_P} | {obs} | {crit} |")
    md_lines.append("")
    md_lines.append("## Global bottlenecks")
    md_lines.append("")
    md_lines.append("| Obstruction | Count |")
    md_lines.append("|---|---:|")
    for item in atlas.global_bottlenecks[:10]:
        md_lines.append(f"| `{item[0]}` | {item[1]} |")
    md_lines.append("")
    md_lines.append("## Shared repair fields")
    md_lines.append("")
    md_lines.append("| Field | Routes |")
    md_lines.append("|---|---:|")
    for item in atlas.shared_repair_fields[:10]:
        md_lines.append(f"| `{item[0]}` | {item[1]} |")
    md_lines.append("")
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"  Markdown summary: {md_path}")
    print()

    # Verdict
    overall = len(atlas.route_summaries) >= 4 and bool(atlas.obstruction_counts)
    print("=" * 60)
    verdict = "INTERFACE_ATLAS_V01_RUN_PASS" if overall else "INTERFACE_ATLAS_V01_RUN_FAIL"
    print(verdict)
    print("=" * 60)
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
