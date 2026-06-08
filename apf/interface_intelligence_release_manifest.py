"""
APF Interface Intelligence Release Manifest.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any, Dict
import csv, io, json, datetime

LAYERS = [
    [
        1,
        "APF_ROUTE_CERTIFICATION_STARTER_SUITE_v1.zip",
        "ROUTE_CERTIFICATION_STARTER_SUITE_P_PASS",
        "check_T_route_certification_starter_suite_P",
        "APPLY_ROUTE_CERTIFICATION_STARTER_SUITE.ps1",
        "foundation",
        "Route-specific starter certification."
    ],
    [
        2,
        "APF_ROUTE_CERTIFICATION_INTEGRATION_WORKBENCH_v1.zip",
        "ROUTE_CERTIFICATION_INTEGRATION_WORKBENCH_P_PASS",
        "check_T_route_workbench_payload_certification_P",
        "APPLY_ROUTE_CERTIFICATION_INTEGRATION_WORKBENCH.ps1",
        "foundation",
        "Payload/CLI certification workbench."
    ],
    [
        3,
        "APF_INTERFACE_STRUCTURE_TRANSPORT_LEDGER_v1.zip",
        "INTERFACE_STRUCTURE_TRANSPORT_LEDGER_P_PASS",
        "check_T_interface_structure_transport_ledger_P",
        "APPLY_INTERFACE_STRUCTURE_TRANSPORT_LEDGER.ps1",
        "interface",
        "Typed interface-structure ledger."
    ],
    [
        4,
        "APF_INTERFACE_STRUCTURE_DISCOVERY_ENGINE_v1.zip",
        "INTERFACE_STRUCTURE_DISCOVERY_ENGINE_P_PASS",
        "check_T_interface_structure_discovery_engine_P",
        "APPLY_INTERFACE_STRUCTURE_DISCOVERY_ENGINE.ps1",
        "interface",
        "Structure discovery engine."
    ],
    [
        5,
        "APF_INTERFACE_STRUCTURE_MOVEMENT_GRAPH_v1.zip",
        "INTERFACE_STRUCTURE_MOVEMENT_GRAPH_P_PASS",
        "check_T_interface_structure_movement_graph_P",
        "APPLY_INTERFACE_STRUCTURE_MOVEMENT_GRAPH.ps1",
        "interface",
        "Movement graph/obstruction path."
    ],
    [
        6,
        "APF_INTERFACE_MOVEMENT_GRAPH_REPAIR_PLANNER_v1.zip",
        "INTERFACE_MOVEMENT_GRAPH_REPAIR_PLANNER_P_PASS",
        "check_T_interface_movement_graph_repair_planner_P",
        "APPLY_INTERFACE_MOVEMENT_GRAPH_REPAIR_PLANNER.ps1",
        "repair",
        "Repair planner."
    ],
    [
        7,
        "APF_INTERFACE_REPAIR_CLOSURE_SIMULATOR_v1.zip",
        "INTERFACE_REPAIR_CLOSURE_SIMULATOR_P_PASS",
        "check_T_interface_repair_closure_simulator_P",
        "APPLY_INTERFACE_REPAIR_CLOSURE_SIMULATOR.ps1",
        "repair",
        "Counterfactual closure simulator."
    ],
    [
        8,
        "APF_INTERFACE_REPAIR_FRONTIER_EXPLORER_v1.zip",
        "INTERFACE_REPAIR_FRONTIER_EXPLORER_P_PASS",
        "check_T_interface_repair_frontier_explorer_P",
        "APPLY_INTERFACE_REPAIR_FRONTIER_EXPLORER.ps1",
        "repair",
        "Minimal repair frontier explorer."
    ],
    [
        9,
        "APF_INTERFACE_REPAIR_OBLIGATION_COMPILER_v1.zip",
        "INTERFACE_REPAIR_OBLIGATION_COMPILER_P_PASS",
        "check_T_interface_repair_obligation_compiler_P",
        "APPLY_INTERFACE_REPAIR_OBLIGATION_COMPILER.ps1",
        "evidence",
        "Evidence obligation compiler."
    ],
    [
        10,
        "APF_INTERFACE_EVIDENCE_RERUN_CONTROLLER_v1.zip",
        "INTERFACE_EVIDENCE_RERUN_CONTROLLER_P_PASS",
        "check_T_interface_evidence_rerun_controller_P",
        "APPLY_INTERFACE_EVIDENCE_RERUN_CONTROLLER.ps1",
        "evidence",
        "Evidence rerun controller."
    ],
    [
        11,
        "APF_EW_TRACE_TO_SCHEME_REAL_ADAPTER_v1.zip",
        "EW_TRACE_TO_SCHEME_REAL_ADAPTER_P_PASS",
        "check_T_EW_trace_to_scheme_real_adapter_P",
        "APPLY_EW_TRACE_TO_SCHEME_REAL_ADAPTER.ps1",
        "real_adapters",
        "EW real adapter."
    ],
    [
        12,
        "APF_DARK_POSTERIOR_REAL_ADAPTER_v1.zip",
        "DARK_POSTERIOR_REAL_ADAPTER_P_PASS",
        "check_T_dark_posterior_real_adapter_P",
        "APPLY_DARK_POSTERIOR_REAL_ADAPTER.ps1",
        "real_adapters",
        "Dark posterior/run real adapter."
    ],
    [
        13,
        "APF_CLAIM_TO_INTERFACE_GRAPH_COMPILER_v1.zip",
        "CLAIM_TO_INTERFACE_GRAPH_COMPILER_P_PASS",
        "check_T_claim_to_interface_graph_compiler_P",
        "APPLY_CLAIM_TO_INTERFACE_GRAPH_COMPILER.ps1",
        "reporting",
        "Claim-to-interface graph compiler."
    ],
    [
        14,
        "APF_INTERFACE_ATLAS_v1.zip",
        "INTERFACE_ATLAS_P_PASS",
        "check_T_interface_atlas_P",
        "APPLY_INTERFACE_ATLAS.ps1",
        "reporting",
        "Interface atlas."
    ],
    [
        15,
        "APF_INTERFACE_INTELLIGENCE_CI_ORCHESTRATOR_v1.zip",
        "INTERFACE_INTELLIGENCE_CI_ORCHESTRATOR_P_PASS",
        "check_T_interface_intelligence_CI_orchestrator_P",
        "APPLY_INTERFACE_INTELLIGENCE_CI_ORCHESTRATOR.ps1",
        "ci",
        "Full CI orchestrator."
    ],
    [
        16,
        "APF_INTERFACE_INTELLIGENCE_REGISTRY_BRIDGE_v1.zip",
        "INTERFACE_INTELLIGENCE_REGISTRY_BRIDGE_P_PASS",
        "check_T_interface_intelligence_registry_bridge_P",
        "APPLY_INTERFACE_INTELLIGENCE_REGISTRY_BRIDGE.ps1",
        "ci",
        "Bank/verify_all registry bridge."
    ],
    [
        17,
        "APF_INTERFACE_INTELLIGENCE_LIVE_SMOKE_HARNESS_v1.zip",
        "INTERFACE_INTELLIGENCE_LIVE_SMOKE_HARNESS_P_PASS",
        "check_T_interface_intelligence_live_smoke_harness_P",
        "RUN_INTERFACE_INTELLIGENCE_LIVE_SMOKE.ps1",
        "operations",
        "Live integration smoke harness."
    ],
    [
        18,
        "APF_INTERFACE_INTELLIGENCE_REVIEWER_REPORTER_v1.zip",
        "INTERFACE_INTELLIGENCE_REVIEWER_REPORTER_P_PASS",
        "check_T_interface_intelligence_reviewer_reporter_P",
        "APPLY_INTERFACE_INTELLIGENCE_REVIEWER_REPORTER.ps1",
        "operations",
        "Reviewer-safe reporter."
    ],
    [
        19,
        "APF_ARTIFACT_TO_ROUTE_PAYLOAD_ADAPTER_v1.zip",
        "ARTIFACT_TO_ROUTE_PAYLOAD_ADAPTER_P_PASS",
        "check_T_artifact_to_route_payload_adapter_P",
        "APPLY_ARTIFACT_TO_ROUTE_PAYLOAD_ADAPTER.ps1",
        "operations",
        "Artifact-to-payload adapter."
    ],
    [
        20,
        "APF_PAYLOAD_BATCH_CERTIFICATION_RUNNER_v1.zip",
        "PAYLOAD_BATCH_CERTIFICATION_RUNNER_P_PASS",
        "check_T_payload_batch_certification_runner_P",
        "APPLY_PAYLOAD_BATCH_CERTIFICATION_RUNNER.ps1",
        "operations",
        "Payload batch certification runner."
    ],
    [
        21,
        "APF_INTERFACE_INTELLIGENCE_E2E_ARTIFACT_PIPELINE_v1.zip",
        "INTERFACE_INTELLIGENCE_E2E_ARTIFACT_PIPELINE_P_PASS",
        "check_T_interface_intelligence_E2E_artifact_pipeline_P",
        "RUN_INTERFACE_INTELLIGENCE_E2E_ARTIFACT_PIPELINE.ps1",
        "operations",
        "E2E artifact diagnostics pipeline."
    ],
    [
        22,
        "APF_INTERFACE_INTELLIGENCE_FAILURE_TRIAGE_ASSISTANT_v1.zip",
        "INTERFACE_INTELLIGENCE_FAILURE_TRIAGE_ASSISTANT_P_PASS",
        "check_T_interface_intelligence_failure_triage_assistant_P",
        "APPLY_INTERFACE_INTELLIGENCE_FAILURE_TRIAGE_ASSISTANT.ps1",
        "operations",
        "Failure triage assistant."
    ],
    [
        23,
        "APF_INTERFACE_INTELLIGENCE_ENGINEERING_COMMAND_CENTER_v1.zip",
        "INTERFACE_INTELLIGENCE_ENGINEERING_COMMAND_CENTER_P_PASS",
        "check_T_interface_intelligence_engineering_command_center_P",
        "RUN_INTERFACE_INTELLIGENCE_ENGINEERING_COMMAND_CENTER.ps1",
        "operations",
        "One-button engineering command center."
    ]
]
ACCEPTANCE = [
    "All listed targeted markers pass after install.",
    "Engineering command center emits engineering_command_center_dashboard.md.",
    "Engineering command center emits interface_intelligence_command_center_reports.zip.",
    "Registry bridge emits register_interface_intelligence_checks.py and verify_all_interface_intelligence_snippet.py.",
    "Live APF bank/verify_all explicitly registers top checks before claims are called banked.",
    "Held, provenance-blocked, and structural-blocked route claims are not promoted by software pass alone."
]

def _layer_dict(t):
    return {"order": t[0], "pack": t[1], "top_marker": t[2], "top_check": t[3], "install_script": t[4], "phase": t[5], "purpose": t[6]}

def build_release_manifest():
    layer_dicts = [_layer_dict(t) for t in LAYERS]
    md = render_markdown()
    return {
        "release_name": "APF_INTERFACE_INTELLIGENCE_ENGINEERING_RELEASE_v1",
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "layers": layer_dicts,
        "command_center_pack": "APF_INTERFACE_INTELLIGENCE_ENGINEERING_COMMAND_CENTER_v1.zip",
        "command_center_script": "RUN_INTERFACE_INTELLIGENCE_ENGINEERING_COMMAND_CENTER.ps1",
        "boundary": "Software package readiness and integration procedure only; live APF bank integration requires install + verify_all pass.",
        "acceptance_criteria": ACCEPTANCE,
        "install_order_csv": render_install_order_csv(),
        "markdown": md,
    }

def render_install_order_csv():
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["order", "pack", "top_marker", "top_check", "install_script", "phase", "purpose"])
    for t in LAYERS:
        w.writerow(list(t))
    return buf.getvalue()

def render_markdown():
    lines = [
        "# APF Interface Intelligence Engineering Release Manifest v1",
        "",
        "## Boundary",
        "",
        "This release records software package readiness and integration procedure. It does not claim live APF bank integration until installed and `verify_all.py` passes.",
        "",
        "## One-button entry point",
        "",
        "```powershell",
        ".\\RUN_INTERFACE_INTELLIGENCE_ENGINEERING_COMMAND_CENTER.ps1",
        "```",
        "",
        "## Install order",
        "",
        "| Order | Phase | Pack | Marker | Purpose |",
        "|---:|---|---|---|---|",
    ]
    for t in LAYERS:
        lines.append(f"| {t[0]} | `{t[5]}` | `{t[1]}` | `{t[2]}` | {t[6]} |")
    lines += ["", "## Acceptance criteria", ""]
    for item in ACCEPTANCE:
        lines.append(f"- {item}")
    lines += [
        "",
        "## Integrator workflow",
        "",
        "1. Install packs in order.",
        "2. Confirm each targeted marker.",
        "3. Run the engineering command center.",
        "4. Inspect dashboard and failure triage.",
        "5. Wire registry bridge into live bank/`verify_all.py`.",
        "6. Run live full verifier.",
        "7. Only then mark the software stack as live-banked.",
        "",
        "## Physics-claim boundary",
        "",
        "A software P marker means the tool works. It does not mean a held physics route is promoted. Route promotion still requires clean evidence, rerun, and live bank acceptance.",
    ]
    return "\n".join(lines) + "\n"

def write_release_manifest(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    manifest = build_release_manifest()
    (out / "interface_intelligence_release_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    (out / "interface_intelligence_release_manifest.md").write_text(manifest["markdown"], encoding="utf-8")
    (out / "interface_intelligence_install_order.csv").write_text(manifest["install_order_csv"], encoding="utf-8")
    (out / "interface_intelligence_top_checks.txt").write_text("\n".join(t[3] for t in LAYERS) + "\n", encoding="utf-8")
    return {"json": str(out / "interface_intelligence_release_manifest.json"), "markdown": str(out / "interface_intelligence_release_manifest.md"), "csv": str(out / "interface_intelligence_install_order.csv"), "top_checks": str(out / "interface_intelligence_top_checks.txt")}

def check_T_release_manifest_layer_count_P():
    m = build_release_manifest()
    tests = {
        "count_23": len(m["layers"]) == 23,
        "orders_unique": len({l["order"] for l in m["layers"]}) == len(m["layers"]),
        "has_command_center": any(l["pack"] == m["command_center_pack"] for l in m["layers"]),
        "has_registry_bridge": any("REGISTRY_BRIDGE" in l["pack"] for l in m["layers"]),
        "has_e2e_pipeline": any("E2E_ARTIFACT_PIPELINE" in l["pack"] for l in m["layers"]),
    }
    return {"name": "check_T_release_manifest_layer_count_P", "consistent": all(tests.values()), "status": "P_release_manifest" if all(tests.values()) else "FAIL", "summary": "Release manifest covers all engineering layers through command center.", "data": {"tests": tests}}

def check_T_release_manifest_boundary_P():
    m = build_release_manifest()
    tests = {
        "boundary_mentions_verify_all": "verify_all" in m["boundary"],
        "markdown_mentions_no_promotion": "does not mean a held physics route is promoted" in m["markdown"],
        "acceptance_mentions_no_promote": any("not promoted" in x for x in m["acceptance_criteria"]),
        "command_center_entry": "RUN_INTERFACE_INTELLIGENCE_ENGINEERING_COMMAND_CENTER.ps1" in m["markdown"],
    }
    return {"name": "check_T_release_manifest_boundary_P", "consistent": all(tests.values()), "status": "P_release_manifest" if all(tests.values()) else "FAIL", "summary": "Release manifest preserves live-bank and physics-claim boundaries.", "data": {"tests": tests}, "dependencies": ["check_T_release_manifest_layer_count_P"]}

def check_T_release_manifest_writes_files_P():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        files = write_release_manifest(td)
        tests = {
            "json_exists": Path(files["json"]).exists(),
            "md_exists": Path(files["markdown"]).exists(),
            "csv_exists": Path(files["csv"]).exists(),
            "top_checks_exists": Path(files["top_checks"]).exists(),
            "csv_has_command_center": "APF_INTERFACE_INTELLIGENCE_ENGINEERING_COMMAND_CENTER_v1.zip" in Path(files["csv"]).read_text(encoding="utf-8"),
        }
    return {"name": "check_T_release_manifest_writes_files_P", "consistent": all(tests.values()), "status": "P_release_manifest" if all(tests.values()) else "FAIL", "summary": "Release manifest writes JSON/Markdown/CSV/top-check artifacts.", "data": {"tests": tests}, "dependencies": ["check_T_release_manifest_boundary_P"]}

def check_T_interface_intelligence_release_manifest_P():
    subchecks = [check_T_release_manifest_layer_count_P(), check_T_release_manifest_boundary_P(), check_T_release_manifest_writes_files_P()]
    ok = all(x["consistent"] for x in subchecks)
    return {"name": "check_T_interface_intelligence_release_manifest_P", "consistent": ok, "status": "P_release_manifest" if ok else "FAIL", "summary": "Interface Intelligence Release Manifest is P: install order, markers, top checks, and boundaries are auditable.", "data": {"core_claim": "The full engineering stack has a machine-readable release manifest and handoff checklist.", "subchecks": [x["name"] for x in subchecks]}, "dependencies": [x["name"] for x in subchecks]}

CHECKS = {
    "check_T_release_manifest_layer_count_P": check_T_release_manifest_layer_count_P,
    "check_T_release_manifest_boundary_P": check_T_release_manifest_boundary_P,
    "check_T_release_manifest_writes_files_P": check_T_release_manifest_writes_files_P,
    "check_T_interface_intelligence_release_manifest_P": check_T_interface_intelligence_release_manifest_P,
}

def register(registry=None):
    if registry is None:
        return CHECKS
    if hasattr(registry, "update"):
        registry.update(CHECKS)
        return registry
    for name, fn in CHECKS.items():
        if hasattr(registry, "register"):
            registry.register(name, fn)
        elif hasattr(registry, "add"):
            registry.add(name, fn)
        else:
            raise TypeError("Unsupported registry type")
    return registry

def run_all():
    return {name: fn() for name, fn in CHECKS.items()}

if __name__ == "__main__":
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
