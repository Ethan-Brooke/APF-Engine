#!/usr/bin/env python3
"""Sprint B — First-real EW trace-to-scheme obligation packet.

Wires ``apf.ew_trace_to_scheme_real_adapter`` to the live v24.3.17 codebase
and produces the framework's first real obligation packet against the actual
EW-route module state.

Pipeline (per the engine architecture):

    live APF EW modules
      -> EWTraceToSchemeAdapterSnapshot  (via build_live_adapter_report)
      -> route payload
      -> descent kernel certification
      -> movement graph + obstruction witnesses
      -> repair frontier
      -> obligation packet
      -> evidence rerun gate (without evidence -> HELD)
      -> safe claim language

The adapter's ``build_live_adapter_report()`` walks 13 EW-relevant module
names and constructs a conservative snapshot.  Of those 13 in the v24.3.17
codebase: 7 are present, 5 are missing (ew_trace_sector_closure,
ew_source_to_scheme_registry, source_to_scheme_registry,
external_constants_ledger, uncertainty_protocols).  The adapter handles
the missing modules by surfacing them as the obligation gap — exactly
what the engine is supposed to do.

Output: a JSON artifact at ``Evidence/first_real_ew_obligation_*.json``
containing the full report (payload + snapshot + certification +
movement_graph + frontier + obligation_packet + evidence_template +
rerun_result_without_evidence).
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
from apf.ew_trace_to_scheme_real_adapter import build_live_adapter_report  # noqa: E402


def main() -> int:
    print("FIRST-REAL EW TRACE-TO-SCHEME OBLIGATION v0.1")
    print(f"  apf bank EXPECTED_THEOREM_COUNT: {bank.EXPECTED_THEOREM_COUNT}")
    print()

    t0 = time.time()
    report = build_live_adapter_report(name="EW_first_real_obligation_v0.1")
    elapsed = time.time() - t0
    rep_dict = report.to_dict()
    print(f"  build_live_adapter_report ran in {elapsed:.2f}s")
    print()

    # Pull the headline fields
    snapshot = rep_dict["snapshot"]
    cert = rep_dict["certification"]
    obligation = rep_dict["obligation_packet"]
    rerun = rep_dict["rerun_result_without_evidence"]

    # Snapshot inferred from live codebase
    print("  --- Snapshot (live-inferred) ---")
    for key in (
        "trace_sector_closed",
        "source_to_scheme_registry_present",
        "evaluator_map_found",
        "codomain_transport_found",
        "counterterm_finite_parts_declared",
        "external_constants_ledger_clean",
        "uncertainty_protocol_declared",
        "target_value_consumed",
    ):
        print(f"    {key:45s} {snapshot.get(key)}")
    print()

    # Live probe summary
    probes = snapshot.get("probes", [])
    imported_ok = sum(1 for p in probes if p.get("import_ok"))
    print(f"  --- Live EW module probes ({len(probes)} total) ---")
    print(f"    imported_ok: {imported_ok} / {len(probes)}")
    for p in probes:
        ok = "OK" if p.get("import_ok") else "MISS"
        n_check = p.get("check_count", 0)
        n_pass = p.get("passing_count", 0)
        print(f"    [{ok:4s}] {p.get('module_name'):42s} {n_pass:3d}/{n_check:3d} pass")
    print()

    # Certification verdict — actual schema lives under certification.ledger_certificate
    print("  --- Certification ledger ---")
    ledger_cert = cert.get("ledger_certificate", {})
    ledger = ledger_cert.get("ledger", {})
    print(f"    sector:                 {ledger.get('sector')}")
    print(f"    local_solution_found:   {ledger.get('local_solution_found')}")
    kind_summary = ledger.get("kind_status_summary", {})
    moves_cleanly = sum(1 for kind, statuses in kind_summary.items() if "MOVES_CLEANLY" in statuses)
    missing = sum(1 for kind, statuses in kind_summary.items() if "MISSING" in statuses)
    print(f"    moves_cleanly_kinds:    {moves_cleanly}")
    print(f"    missing_kinds:          {missing}")
    miss_list = [item.get("kind") for item in ledger.get("missing_required", [])]
    print(f"    missing_required_kinds: {miss_list}")
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
        for fld in b.get("fields", []):
            print(f"          field: {fld}")
    print()

    # Rerun without evidence — should refuse to promote
    print("  --- Rerun (no evidence supplied) ---")
    print(f"    status:           {rerun.get('status')}")
    ev_val = rerun.get("evidence_validation", {})
    print(f"    ready_to_rerun:   {ev_val.get('ready_to_rerun')}")
    print(f"    missing_slots:    {len(ev_val.get('missing_slots', []))}")
    print(f"    supplied_slots:   {len(ev_val.get('supplied_slots', []))}")
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
    artifact_path = EVIDENCE / f"first_real_ew_obligation_{ts}.json"
    artifact_path.write_text(json.dumps(artifact, indent=2, default=str), encoding="utf-8")
    print(f"  Artifact: {artifact_path}")
    print()

    # Verdict — the engine produced a valid certification, obligation packet, and rerun result
    ledger_cert = cert.get("ledger_certificate", {})
    cert_produced = bool(ledger_cert.get("ledger"))
    packet_status = obligation.get("packet_status")
    packet_produced = packet_status in (
        "OPEN_EVIDENCE_REQUIRED",
        "CLOSED_GLOBAL_P",
        "BLOCKED_SUBSTRATE_REVISION_REQUIRED",
        "FAIL_CLOSED_PROVENANCE",
    )
    rerun_outcome = rerun.get("status")
    rerun_consistent = rerun_outcome in (
        "EVIDENCE_INCOMPLETE_NOT_RERUN",
        "RERUN_GLOBAL_P",
        "RERUN_HELD",
        "RERUN_FAIL_CLOSED",
    )

    overall_pass = cert_produced and packet_produced and rerun_consistent

    print("=" * 60)
    if overall_pass:
        verdict = "EW_FIRST_REAL_OBLIGATION_PRODUCED_PASS"
    else:
        verdict = "EW_FIRST_REAL_OBLIGATION_PRODUCED_FAIL"
    print(verdict)
    print("=" * 60)
    print()
    print("Note: this script PRODUCES the obligation packet against live state.")
    print("It does NOT promote any EW claim to global P; the descent kernel decides")
    print("that based on the obstruction object.  This run's verdict reflects what")
    print("the engine emitted, not a physics claim.")

    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
