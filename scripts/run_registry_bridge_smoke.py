#!/usr/bin/env python3
"""Sprint A — Registry-bridge live integration smoke.

Exercises ``apf.interface_intelligence_registry_bridge`` against the live
v24.3.17 codebase end-to-end.

Round-trip:
  1. Probe all 15 interface-intelligence top checks via the bridge
     (confirms imports + function-presence).
  2. Build the full ``RegistryBridgeReport`` (confirms ready=True).
  3. Register all 15 into a scratch OrderedDict via the bridge.
  4. Run each registered check live; capture consistent/status/summary.
  5. Cross-check the bridge-emitted bank stub + verify_all snippet against
     a known good shape.
  6. Persist the full report to ``Evidence/registry_bridge_smoke_*.json``
     for the next session.

The smoke writes its results to ``__APF Library/Evidence/`` rather than
mutating ``bank.REGISTRY`` itself.  This is deliberate: the bridge is a
read-only wiring layer at the production level — it lets ``verify_all.py``
discover and register the interface-intelligence top checks, but it
should not silently mutate live bank state without an explicit bank-bump
step.  The smoke proves the bridge works; a follow-on integration would
wire the bridge into the real ``verify_all.MODULES`` ladder.
"""
from __future__ import annotations

import json
import sys
import time
from collections import OrderedDict
from pathlib import Path

CODEBASE = Path("/sessions/laughing-epic-brahmagupta/mnt/__APF Library/Codebase/APF_Codebase_v24.3")
EVIDENCE = Path("/sessions/laughing-epic-brahmagupta/mnt/__APF Library/Evidence")
sys.path.insert(0, str(CODEBASE))

from apf import bank  # noqa: E402
from apf.interface_intelligence_registry_bridge import (  # noqa: E402
    INTERFACE_INTELLIGENCE_TOP_CHECKS,
    build_registry_bridge_report,
    probe_all_top_checks,
    register_interface_intelligence_checks,
    run_registered_interface_intelligence_checks,
)


def _stage_probes() -> dict:
    """Stage 1 — probe each top check spec individually."""
    probes = probe_all_top_checks()
    ready_count = sum(1 for p in probes if p.status.value == "READY")
    return {
        "count_specs": len(INTERFACE_INTELLIGENCE_TOP_CHECKS),
        "count_probes": len(probes),
        "count_ready": ready_count,
        "all_ready": ready_count == len(INTERFACE_INTELLIGENCE_TOP_CHECKS),
        "probe_details": [p.to_dict() for p in probes],
    }


def _stage_report() -> dict:
    """Stage 2 — full RegistryBridgeReport via the bridge."""
    report = build_registry_bridge_report()
    return {
        "ready": report.ready,
        "registration_count": report.registration_count,
        "bank_stub_len": len(report.generated_bank_stub),
        "verify_all_snippet_len": len(report.generated_verify_all_snippet),
        "all_specs_match_probes": (
            len(report.specs) == len(report.probes) == 15
        ),
    }


def _stage_register_scratch() -> dict:
    """Stage 3 — register all 15 top checks into a scratch OrderedDict.

    Uses an OrderedDict (mirroring the shape of bank.REGISTRY) but does NOT
    write into the real production registry.  This proves the bridge's
    ``update()`` path works against the same shape that ``bank.REGISTRY``
    uses without mutating production state.
    """
    scratch: "OrderedDict[str, object]" = OrderedDict()
    register_interface_intelligence_checks(scratch)
    return {
        "registered_count": len(scratch),
        "expected_count": 15,
        "match": len(scratch) == 15,
        "registered_names": list(scratch.keys()),
    }


def _stage_run_live() -> dict:
    """Stage 4 — run each registered top check live in the v24.3.17 tree."""
    t0 = time.time()
    results = run_registered_interface_intelligence_checks()
    elapsed = time.time() - t0

    summary = {}
    failures = []
    for name, result in results.items():
        consistent = result.get("consistent") if isinstance(result, dict) else None
        status = result.get("status") if isinstance(result, dict) else None
        summary[name] = {"consistent": consistent, "status": status}
        if consistent is False or (isinstance(status, str) and status.startswith("FAIL")):
            failures.append(name)

    return {
        "live_count": len(results),
        "expected_count": 15,
        "match": len(results) == 15,
        "fail_count": len(failures),
        "fail_names": failures,
        "elapsed_seconds": round(elapsed, 3),
        "per_check": summary,
    }


def _stage_artifact_shape() -> dict:
    """Stage 5 — sanity check the bridge-emitted bank stub + verify_all snippet."""
    report = build_registry_bridge_report()
    stub = report.generated_bank_stub
    snippet = report.generated_verify_all_snippet
    return {
        "bank_stub_starts_with_docstring": stub.startswith('"""'),
        "bank_stub_mentions_register": "register_interface_intelligence_checks" in stub,
        "bank_stub_lists_15_specs": stub.count("apf.") >= 15,
        "snippet_mentions_expected_list": "INTERFACE_INTELLIGENCE_EXPECTED_CHECKS" in snippet,
        "snippet_mentions_assert": "assert_interface_intelligence_expected_checks_pass" in snippet,
        "snippet_lists_15_checks": snippet.count("check_T_") >= 15,
    }


def main() -> int:
    print("REGISTRY BRIDGE SMOKE v0.1")
    print(f"  apf bank EXPECTED_THEOREM_COUNT: {bank.EXPECTED_THEOREM_COUNT}")
    print(f"  apf top-check specs in bridge:   {len(INTERFACE_INTELLIGENCE_TOP_CHECKS)}")

    stages = OrderedDict()
    stages["stage_1_probes"] = _stage_probes()
    stages["stage_2_full_report"] = _stage_report()
    stages["stage_3_register_scratch"] = _stage_register_scratch()
    stages["stage_4_run_live"] = _stage_run_live()
    stages["stage_5_artifact_shape"] = _stage_artifact_shape()

    # Summary
    all_pass = (
        stages["stage_1_probes"]["all_ready"]
        and stages["stage_2_full_report"]["ready"]
        and stages["stage_3_register_scratch"]["match"]
        and stages["stage_4_run_live"]["fail_count"] == 0
        and all(stages["stage_5_artifact_shape"].values())
    )

    print()
    for stage_name, stage in stages.items():
        if "all_ready" in stage:
            ok = stage["all_ready"]
        elif "ready" in stage:
            ok = stage["ready"]
        elif "match" in stage:
            ok = stage["match"]
        elif "fail_count" in stage:
            ok = stage["fail_count"] == 0
        else:
            ok = all(v for v in stage.values() if isinstance(v, bool))
        print(f"  [{'PASS' if ok else 'FAIL'}] {stage_name}")
    print()

    # Persist artifact
    artifact = {
        "smoke_version": "v0.1",
        "codebase_version": "24.3.17",
        "bank_expected_count": bank.EXPECTED_THEOREM_COUNT,
        "all_pass": all_pass,
        "stages": stages,
    }
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
    artifact_path = EVIDENCE / f"registry_bridge_smoke_{ts}.json"
    artifact_path.write_text(json.dumps(artifact, indent=2, default=str), encoding="utf-8")
    print(f"  Artifact: {artifact_path}")
    print()
    print("=" * 60)
    print(f"REGISTRY_BRIDGE_LIVE_SMOKE_{'PASS' if all_pass else 'FAIL'}")
    print("=" * 60)
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
