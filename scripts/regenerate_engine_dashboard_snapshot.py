#!/usr/bin/env python3
"""Regenerate the engine-state snapshot for the apf-61-to-102-bridge dashboard.

Runs the live atlas, maps each adapter to the lattice channels it structurally
touches via a CURATED registry (the v2 successor to the keyword-based mapping
that shipped in v24.3.46), validates every channel ID against the canonical
61-channel registry, and patches the ATLAS_SNAPSHOT constant inside the bridge
artifact's index.html via tmp+rename per Working Rule 9.

Run from anywhere under the codebase tree; resolves apf import via sys.path
walk-up.

Usage:
    python3 scripts/regenerate_engine_dashboard_snapshot.py [--no-patch]

--no-patch  emit the snapshot JSON to stdout without modifying the artifact.
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
import tempfile
import os
from pathlib import Path


# Resolve apf import
_here = Path(__file__).resolve()
for _ in range(6):
    if (_here.parent / "apf" / "bank.py").is_file():
        sys.path.insert(0, str(_here.parent))
        break
    _here = _here.parent


# Canonical 61-channel registry. Exact IDs as defined in the bridge artifact
# (vacuum 42 + baryonic 3 + dark 16).
CANONICAL_CHANNELS_61: tuple[str, ...] = (
    # vacuum (42): 8 gluons + 3 EW bosons + photon + 27 color-internal + 3 Goldstones
    "g1", "g2", "g3", "g4", "g5", "g6", "g7", "g8",
    "W⁺", "W⁻", "Z⁰", "γ",
    "Q₁r", "Q₁g", "Q₁b", "uᶜ₁r", "uᶜ₁g", "uᶜ₁b", "dᶜ₁r", "dᶜ₁g", "dᶜ₁b",
    "Q₂r", "Q₂g", "Q₂b", "cᶜ₂r", "cᶜ₂g", "cᶜ₂b", "sᶜ₂r", "sᶜ₂g", "sᶜ₂b",
    "Q₃r", "Q₃g", "Q₃b", "tᶜ₃r", "tᶜ₃g", "tᶜ₃b", "bᶜ₃r", "bᶜ₃g", "bᶜ₃b",
    "G⁺", "G⁻", "G⁰",
    # baryonic (3): topological color charges
    "r", "g", "b",
    # dark (16): 3 neutrinos + 3 charged leptons + 3 charged-lepton conjugates +
    #            3 quark-doublets dark partner + 3 up-singlet dark partner + Higgs
    "νₑ", "e", "νₘ", "μ", "ντ", "τ",
    "eᶜ", "μᶜ", "τᶜ",
    "Q₁ⁿ", "Q₂ⁿ", "Q₃ⁿ",
    "uᶜ₁ⁿ", "cᶜ₂ⁿ", "tᶜ₃ⁿ",
    "H⁰",
)
assert len(CANONICAL_CHANNELS_61) == 61
CANONICAL_SET = frozenset(CANONICAL_CHANNELS_61)


# Convenience subsets
ALL_VACUUM = CANONICAL_CHANNELS_61[:42]
ALL_BARYONIC = CANONICAL_CHANNELS_61[42:45]
ALL_DARK = CANONICAL_CHANNELS_61[45:]
ALL_61 = CANONICAL_CHANNELS_61

GLUONS_8 = tuple(CANONICAL_CHANNELS_61[:8])
EW_BOSONS = ("W⁺", "W⁻", "Z⁰", "γ")
GOLDSTONES = ("G⁺", "G⁻", "G⁰")
COLOR_TRIPLE = ("r", "g", "b")
NEUTRINOS = ("νₑ", "νₘ", "ντ")
CHARGED_LEPTONS = ("e", "μ", "τ")
CHARGED_LEPTON_CONJ = ("eᶜ", "μᶜ", "τᶜ")

CHARM_3COL = ("cᶜ₂r", "cᶜ₂g", "cᶜ₂b")
BOTTOM_3COL = ("bᶜ₃r", "bᶜ₃g", "bᶜ₃b")
TOP_3COL = ("tᶜ₃r", "tᶜ₃g", "tᶜ₃b")
LIGHT_QUARKS_9COL = (
    "Q₁r", "Q₁g", "Q₁b", "uᶜ₁r", "uᶜ₁g", "uᶜ₁b", "dᶜ₁r", "dᶜ₁g", "dᶜ₁b",
)


# Curated authoritative channel-touch map. Each atlas_input_id maps to the
# lattice channels it structurally touches (as opposed to the v1 keyword-based
# heuristic). The mapping is interpretive — built from a reading of each
# adapter's payload + the underlying physical claim it adjudicates — and is
# tightened over time as adapter authors gain clearer structural intuition for
# their own routes.
#
# Convention: channels are listed at the granularity the route actually
# distinguishes. Mass routes for a specific quark generation list that
# generation's 3-color triple. Identity routes list the structural EW-gauge
# channels that compose the identity. Substrate-level routes (cosmogenesis /
# evaporation / gravity) list ALL_61 because the substrate is universal.
# Arch / meta routes list () because they don't bind to any lattice channel.

ATLAS_CHANNEL_TOUCH_MAP: dict[str, tuple[str, ...]] = {
    # --- Mass sector — 14 routes ---
    "mass:route01_charged_lepton_pole": ("e",),
    "mass:route02_charged_lepton_qed_running": CHARGED_LEPTONS + ("γ",),
    "mass:route03_charm_msbar_self_scale": CHARM_3COL,
    "mass:route04_charm_pole": CHARM_3COL,  # obstruction-named on charm pole codomain
    "mass:route05_bottom_msbar_self_scale": BOTTOM_3COL,
    "mass:route06_bottom_pole": BOTTOM_3COL,  # obstruction-named on bottom pole
    "mass:route07_top_external_msr": TOP_3COL,
    "mass:route08_top_msr_ew_transport": TOP_3COL + EW_BOSONS,  # EW-transport ladder couples top to M_W
    "mass:route09_top_pole_mc": TOP_3COL,  # obstruction-named on top pole/MC
    "mass:route10_light_quark_flag_external_kernel": LIGHT_QUARKS_9COL + GLUONS_8 + COLOR_TRIPLE,  # FLAG external kernel + QCD context
    "mass:route11_mw_on_shell_dizet": ("W⁺", "W⁻", "Z⁰", "γ", "G⁺", "G⁻"),
    "mass:route12_sin2_theta_w_source_identity": EW_BOSONS,  # sin²θ_W = 3/13 source identity
    "mass:route13_sin2_theta_eff_bsy_four_channel": EW_BOSONS + GOLDSTONES,  # four-channel effective angle
    "mass:route14_sin2_theta_w_mass_ratio_identity": ("W⁺", "W⁻", "Z⁰"),  # 1 - M_W²/M_Z²

    # --- Dark sector — 4 routes ---
    # APF2 w2(a) background response — vacuum/cold-sector coupling per LATEST-62
    "dark:route_w2_a_background": GOLDSTONES + tuple(ALL_DARK),
    # Empirical cross-SN audit — same structural footprint
    "dark:route_cross_sn_profile_probe": GOLDSTONES + tuple(ALL_DARK),
    # Particle ID obstruction — names which dark channels CAN'T be promoted to particle DM
    "dark:route_dark_particle_id": tuple(ALL_DARK),
    # Modified gravity Bianchi no-go — geometric/topological
    "dark:route_modified_gravity": COLOR_TRIPLE,

    # --- Gravity (3) — route_class=horizon, all INTERNAL_IDENTITY_GLOBAL_P ---
    # GR-limit theorem couples to the full substrate
    "gravity:route_gr_limit_full_close": ALL_61,
    "gravity:route_bianchi_rigidity": ALL_61,
    "gravity:route_ringdown_capacity_schema": ALL_61,

    # --- Cosmogenesis / evaporation — substrate-level transitions ---
    "cosmogenesis:route_t1_t4_quartet": ALL_61,  # void → middle transition
    "evaporation:route_e1_e4_quartet": ALL_61,   # saturation → middle (inverse)

    # --- Neutrino ---
    "neutrino:route_mbb_reconciliation": NEUTRINOS,

    # --- Architecture / meta — no lattice-channel binding ---
    "arch:route_rdfi_global_descent_kernel": (),
    "arch:route_defect_calculus_architecture": (),
    "arch:route_interface_engine_operational": (),

    # --- CODOMAIN axis ---
    # Superconductivity codomain — gauge-coherence over U(1)_em with electrons
    "coherent_phase:superconductivity": ("γ", "G⁰") + CHARGED_LEPTONS + CHARGED_LEPTON_CONJ,
}


def validate_touch_map() -> list[str]:
    """Return a list of problems with the touch map. Empty list = clean."""
    problems = []
    for adapter_id, channels in ATLAS_CHANNEL_TOUCH_MAP.items():
        for ch in channels:
            if ch not in CANONICAL_SET:
                problems.append(f"adapter {adapter_id!r}: channel {ch!r} not in canonical 61")
    return problems


def run() -> dict:
    """Build the snapshot dict from the live atlas + curated touch map."""
    problems = validate_touch_map()
    if problems:
        print("VALIDATION FAILED:")
        for p in problems:
            print("  " + p)
        sys.exit(2)

    # Fresh import to pick up any in-session edits
    for k in list(sys.modules):
        if k.startswith("apf"):
            del sys.modules[k]
    from apf import bank, _module_manifest as mm, __version__  # noqa: PLC0415
    from apf import interface_atlas_live_runner as runner  # noqa: PLC0415

    bank._load()
    result = runner.run_live_atlas()

    # Check for adapters present in atlas but missing from touch map. Resolve
    # CODOMAIN-axis placeholder original_ids ("(none; new codomain-axis input)")
    # to their route field so the SC codomain adapter doesn't false-positive.
    def resolve_id(a):
        rid = a["original_id"]
        return a["route"] if rid.startswith("(") and a["route"] in ATLAS_CHANNEL_TOUCH_MAP else rid

    seen_in_atlas = {resolve_id(a) for a in result["adapter_results"]}
    missing_from_map = seen_in_atlas - set(ATLAS_CHANNEL_TOUCH_MAP)
    extra_in_map = set(ATLAS_CHANNEL_TOUCH_MAP) - seen_in_atlas

    if missing_from_map:
        print("WARNING: atlas has these adapters but touch map doesn't:")
        for x in sorted(missing_from_map):
            print("  " + x)
    if extra_in_map:
        print("WARNING: touch map has these adapters but atlas doesn't:")
        for x in sorted(extra_in_map):
            print("  " + x)

    # Build per-adapter records. For CODOMAIN-axis inputs whose original_id is
    # the live-runner placeholder "(none; new codomain-axis input)", the real
    # identifier lives in the route field — fall back to it for the touch-map
    # lookup so the SC codomain adapter resolves correctly.
    adapters = []
    matched_via_route = 0
    for a in result["adapter_results"]:
        rid = a["original_id"]
        route = a["route"]
        channels = list(ATLAS_CHANNEL_TOUCH_MAP.get(rid, ()))
        # Codomain-axis placeholder fallback
        if not channels and rid.startswith("(") and route in ATLAS_CHANNEL_TOUCH_MAP:
            channels = list(ATLAS_CHANNEL_TOUCH_MAP[route])
            rid_display = route
            matched_via_route += 1
        else:
            rid_display = rid
        adapters.append({
            "id": rid_display,
            "route": route,
            "axis": a["axis"],
            "status": a["solver_status"],
            "packet_status": a["packet_status"],
            "global_P": a["export_global_P"],
            "channels": channels,
        })
    if matched_via_route:
        print(f"INFO: matched {matched_via_route} CODOMAIN-axis adapter(s) via route fallback")

    return {
        "apf_version": __version__,
        "snapshot_utc": datetime.datetime.utcnow().isoformat() + "Z",
        "bank_expected": bank.EXPECTED_THEOREM_COUNT,
        "bank_registry": len(bank.REGISTRY),
        "bank_registry_modules": len(mm.BANK_REGISTRY_MODULES),
        "arch_only_modules": len(mm.ARCHITECTURE_ONLY_MODULES),
        "channel_registry_size": len(CANONICAL_CHANNELS_61),
        "touch_map_coverage": f"{len(seen_in_atlas - missing_from_map)}/{len(seen_in_atlas)}",
        "atlas": {
            "total_inputs": result["total_inputs"],
            "wired_adapter_count": result["wired_adapter_count"],
            "global_P_count": result["global_P_count"],
            "adapters": adapters,
            "axis_summary": {
                axis: {
                    "input_count": result["axis_summary"][axis]["input_count"],
                    "global_P_count": result["axis_summary"][axis]["global_P_count"],
                    "status_counts": result["axis_summary"][axis]["status_counts"],
                    "obstruction_counts": result["axis_summary"][axis].get("obstruction_counts", {}),
                    "failed_kind_counts": result["axis_summary"][axis].get("failed_kind_counts", {}),
                }
                for axis in ("ROUTE", "CODOMAIN")
                if axis in result["axis_summary"]
            },
        },
        "cmal": {
            "pipeline_state": "INTERNAL_RELEASE_CANDIDATE_WITH_GUARDS",
            "rc_id": "CMAL-RC-2026-05-19-v1",
            "allowed_channels": ["INTERNAL_BANK_REVIEW", "GUARDED_PARTNER_PILOT_PACKET"],
            "blocked_channels": [
                "PUBLIC_UNREVIEWED_RELEASE",
                "LIVE_EXTERNAL_CONNECTORS",
                "AUTONOMOUS_LAB_EXECUTION",
                "MATERIAL_PREDICTION_CLAIMS",
                "ROOM_TEMPERATURE_SC_CLAIMS",
            ],
            "module_count": sum(1 for m in mm.ARCHITECTURE_ONLY_MODULES if "coherent_materials_" in m),
            "pipeline_layers": [
                {"name": "Front gate + triage", "modules": ["receipt_contract_validator", "candidate_triage_kernel"]},
                {"name": "Batch composition", "modules": ["batch_triage_runner", "golden_receipt_benchmark", "manual_external_dry_run", "manual_dry_run_pilot", "receipt_trace_certificates"]},
                {"name": "Red team", "modules": ["adversarial_receipt_stress_suite", "claim_fence_certifier", "provenance_conflict_auditor"]},
                {"name": "RC + pilot pipeline", "modules": ["pilot_telemetry_schema", "acceptance_test_harness", "release_candidate_certifier", "pilot_readiness_gate", "partner_pilot_kit", "partner_feedback_intake", "pilot_outcome_review_board", "release_governance_gate", "portfolio_planner"]},
                {"name": "Baseline (pre-RC)", "modules": ["casebook", "discriminator", "functional_codomain_registry", "ingestion_contract", "intervention_selector", "obligation_packet_adapter", "protocol_compiler", "receipt_update_loop", "sc_material_evidence", "sc_material_ledger", "correlated_layer_competition"]},
            ],
        },
    }


def patch_artifact(snapshot: dict, artifact_path: Path) -> None:
    """Replace the ATLAS_SNAPSHOT constant in the bridge artifact's index.html."""
    content = artifact_path.read_text(encoding="utf-8")
    start_marker = "const ATLAS_SNAPSHOT = "
    end_marker = ";\n\n// ========== DATA =========="
    s = content.find(start_marker)
    e = content.find(end_marker, s)
    if s == -1 or e == -1:
        raise RuntimeError("could not locate ATLAS_SNAPSHOT block in artifact")
    new_constant = start_marker + json.dumps(snapshot, ensure_ascii=False) + ";"
    new_content = content[:s] + new_constant + "\n\n// ========== DATA ==========" + content[e + len(end_marker):]

    fd, tmp = tempfile.mkstemp(dir=artifact_path.parent, prefix=".bridge_snap_", suffix=".html.tmp")
    os.close(fd)
    Path(tmp).write_text(new_content, encoding="utf-8")
    Path(tmp).replace(artifact_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-patch", action="store_true",
                        help="emit JSON to stdout only; don't modify the artifact")
    parser.add_argument("--artifact-path",
                        default="/sessions/cool-great-meitner/mnt/Artifacts/apf-61-to-102-bridge/index.html",
                        help="path to the bridge artifact's index.html")
    args = parser.parse_args()

    snapshot = run()

    if args.no_patch:
        print(json.dumps(snapshot, indent=2, ensure_ascii=False))
        return

    artifact_path = Path(args.artifact_path)
    if not artifact_path.is_file():
        print(f"artifact not found at {artifact_path}; emitting JSON to stdout instead")
        print(json.dumps(snapshot, indent=2, ensure_ascii=False))
        return

    patch_artifact(snapshot, artifact_path)
    print(f"Patched {artifact_path}")
    print(f"  apf_version: {snapshot['apf_version']}")
    print(f"  snapshot_utc: {snapshot['snapshot_utc']}")
    print(f"  atlas wired: {snapshot['atlas']['wired_adapter_count']}, global_P: {snapshot['atlas']['global_P_count']}")
    print(f"  touch_map_coverage: {snapshot['touch_map_coverage']}")


if __name__ == "__main__":
    main()
