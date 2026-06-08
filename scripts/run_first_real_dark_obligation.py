#!/usr/bin/env python3
"""Sprint C — First-real dark-sector posterior obligation packet.

Same pattern as Sprint B (EW) but for the dark sector.  Wires
``apf.dark_posterior_real_adapter`` to the live v24.3.17 codebase and
produces the framework's first real obligation packet against actual
dark-sector module state.

Output: a JSON artifact at ``Evidence/first_real_dark_obligation_*.json``
containing the full report.
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
from apf.dark_posterior_real_adapter import (  # noqa: E402
    DARK_RELEVANT_MODULES,
    build_live_adapter_report,
)


def main() -> int:
    print("FIRST-REAL DARK POSTERIOR OBLIGATION v0.1")
    print(f"  apf bank EXPECTED_THEOREM_COUNT: {bank.EXPECTED_THEOREM_COUNT}")
    print(f"  dark-relevant module probe targets: {len(DARK_RELEVANT_MODULES)}")
    print()

    t0 = time.time()
    report = build_live_adapter_report(name="DARK_first_real_obligation_v0.1")
    elapsed = time.time() - t0
    rep_dict = report.to_dict()
    print(f"  build_live_adapter_report ran in {elapsed:.2f}s")
    print()

    snapshot = rep_dict["snapshot"]
    cert = rep_dict["certification"]
    obligation = rep_dict["obligation_packet"]
    rerun = rep_dict["rerun_result_without_evidence"]

    # Snapshot
    print("  --- Snapshot (live-inferred) ---")
    for key, value in snapshot.items():
        if key == "probes":
            continue
        if isinstance(value, str) and len(value) > 60:
            value = value[:60] + "..."
        print(f"    {key:45s} {value}")
    print()

    # Live probe
    probes = snapshot.get("probes", [])
    imported_ok = sum(1 for p in probes if p.get("import_ok"))
    print(f"  --- Live dark-relevant probes ({len(probes)} total) ---")
    print(f"    imported_ok: {imported_ok} / {len(probes)}")
    for p in probes:
        ok = "OK" if p.get("import_ok") else "MISS"
        print(f"    [{ok:4s}] {p.get('module_name'):42s} {p.get('passing_count', 0):3d}/{p.get('check_count', 0):3d} pass")
    print()

    # Ledger certificate
    ledger_cert = cert.get("ledger_certificate", {})
    ledger = ledger_cert.get("ledger", {})
    print("  --- Ledger certificate ---")
    print(f"    sector:               {ledger.get('sector')}")
    print(f"    local_solution_found: {ledger.get('local_solution_found')}")
    ks = ledger.get("kind_status_summary", {})
    for kind, statuses in ks.items():
        print(f"    {kind:25s} {statuses}")
    miss_list = [item.get("kind") for item in ledger.get("missing_required", [])]
    print(f"    missing_required: {miss_list}")
    print()

    # Obligation packet
    print("  --- Obligation packet ---")
    print(f"    packet_status:          {obligation.get('packet_status')}")
    print(f"    frontier_status:        {obligation.get('frontier_status')}")
    print(f"    original_repair_class:  {obligation.get('original_repair_class')}")
    bundles = obligation.get("bundles", [])
    print(f"    repair_bundles:         {len(bundles)}")
    for b in bundles[:3]:
        n_slots = sum(len(o.get("evidence_slots", [])) for o in b.get("obligations", []))
        print(f"      - {b.get('bundle_id')} (minimal={b.get('minimal')}): {len(b.get('fields', []))} fields, {n_slots} evidence slots")
    print()

    # Rerun
    print("  --- Rerun (no evidence supplied) ---")
    print(f"    status: {rerun.get('status')}")
    ev = rerun.get("evidence_validation", {})
    print(f"    ready_to_rerun: {ev.get('ready_to_rerun')}")
    print(f"    missing_slots:  {len(ev.get('missing_slots', []))}")
    print()

    # Persist
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
    artifact = {
        "run_version": "v0.1",
        "codebase_version": "24.3.17",
        "bank_expected_count": bank.EXPECTED_THEOREM_COUNT,
        "wall_seconds": round(elapsed, 3),
        "report": rep_dict,
    }
    artifact_path = EVIDENCE / f"first_real_dark_obligation_{ts}.json"
    artifact_path.write_text(json.dumps(artifact, indent=2, default=str), encoding="utf-8")
    print(f"  Artifact: {artifact_path}")
    print()

    # Verdict
    cert_produced = bool(ledger)
    packet_produced = obligation.get("packet_status") in (
        "OPEN_EVIDENCE_REQUIRED",
        "CLOSED_GLOBAL_P",
        "BLOCKED_SUBSTRATE_REVISION_REQUIRED",
        "FAIL_CLOSED_PROVENANCE",
    )
    rerun_consistent = rerun.get("status") in (
        "EVIDENCE_INCOMPLETE_NOT_RERUN",
        "RERUN_GLOBAL_P",
        "RERUN_HELD",
        "RERUN_FAIL_CLOSED",
    )
    overall_pass = cert_produced and packet_produced and rerun_consistent

    print("=" * 60)
    verdict = "DARK_FIRST_REAL_OBLIGATION_PRODUCED_PASS" if overall_pass else "DARK_FIRST_REAL_OBLIGATION_PRODUCED_FAIL"
    print(verdict)
    print("=" * 60)
    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
