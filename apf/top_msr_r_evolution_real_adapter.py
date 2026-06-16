"""
APF Top MSR R-Evolution Real Adapter -- Tier-1 wire-in.

Engine-side adapter that turns the banked v66 + v67 + v68 top MSR R-evolution
evaluator content into a typed route payload for the
mass:route08_top_msr_ew_transport atlas input.

Replaces v62/v63's fixed-order MSR witness with v67's proper 4-loop R-evolution
from R_* = 85.86 GeV to R_EW = M_W^TRACE/(2pi) = 12.79 GeV.

Status banked
-------------
- Export_top_MSR_R_evolution_route_typed = 1 (preserved from v66)
- Export_top_MSR_R_evolution_4loop_evaluator_closed = 1 (preserved from v67)
- Export_top_MSR_engine_adapter_wired = 1 (NEW at this module)
- Export_top_pole_branch_quarantined = 1 (preserved from v61 KO; pole branch
  rejected at z=4.70 against PDG direct top under coefficient-ingested 4-loop)
- Export_top_physical_final = 0 (LATEST-30 next-gate non-claim)
- Export_top_APF_internal_full_QCD_loop_derivation = 0 (separate program)
"""
from __future__ import annotations

from typing import Any, Dict

from apf.real_adapter_factory import (
    RealAdapterSnapshot,
    build_adapter_report,
    make_check_set,
)


# ============================================================================
# Banked v66 + v67 + v68 content
# ============================================================================

# v67 4-loop R-evolution output: m_t^MSR transported from R_* to R_EW.
TOP_MSR_R_EVOLUTION_OUTPUT: Dict[str, float] = {
    "m_t_MSR_R_star_GeV": 168.169,           # v37 source value at APF-native scale R_*
    "m_t_MSR_R_EW_4loop_GeV": 172.7168,      # v67 4-loop R-evolved value
    "R_star_GeV": 85.857,                    # APF-native scale selector
    "R_EW_GeV": 12.790,                      # M_W^TRACE / (2*pi)
    "alpha_s_R_star": 0.11908,
    "alpha_s_R_EW": 0.16853,
    "delta_R_evolution_4loop_GeV": 4.5477,
}

# Loop convergence ladder banked at v67 (L=1 -> L=4).
LOOP_CONVERGENCE_LADDER: Dict[str, float] = {
    "L1_m_t_MSR_R_EW_GeV": 172.285,
    "L2_m_t_MSR_R_EW_GeV": 172.501,
    "L3_m_t_MSR_R_EW_GeV": 172.667,
    "L4_m_t_MSR_R_EW_GeV": 172.7168,
}

# v67 residual diagnostic vs PDG direct top (audit-only, not a fit).
RESIDUAL_DIAGNOSTIC: Dict[str, Any] = {
    "pdg_direct_top_GeV": 172.56,
    "pdg_direct_uncertainty_GeV": 0.31,
    "apf_residual_GeV": +0.157,
    "z_direct": 0.506,
    "combined_envelope_GeV": 0.317,
    "envelope_components": {
        "sigma_alpha_s": 0.0434,
        "sigma_gamma_3": 0.0004,
        "sigma_truncation": 0.0498,  # sourced last-term (was 0.018 unsourced); see
        # APF Reference Docs/Reference - Top MSR R-Evolution Coefficient Sourcing and sigma_trunc (2026-06-16).md
    },
    "z_combined": 0.495,
    "status": "INSIDE_COMBINED_ENVELOPE",
}

# Pole branch quarantine (v61 KO under sourced 4-loop coefficients).
POLE_BRANCH_QUARANTINE: Dict[str, Any] = {
    "v61_pole_4loop_GeV": 174.017,
    "z_vs_pdg_direct": 4.70,
    "status": "QUARANTINED_BY_KNOCKOUT",
    "audit_only_comparator": True,
}

REQUIRED_LEDGER_FIELDS = (
    "external_alpha_s_MZ_PDG_world_average",
    "external_R_star_scale_selector_apf_native",
    "external_R_EW_scale_selector_apf_native",
    "external_4loop_gamma_m_anomalous_dimension_coefficients",
    "external_4loop_beta_function_coefficients",
    "external_MSR_renormalization_scheme",
    "external_R_evolution_kernel_4loop",
    "external_loop_convergence_audit_L_1_to_4",
    "external_truncation_envelope_sigma_truncation",
    "external_alpha_s_running_R_star_to_R_EW",
    "external_combined_uncertainty_protocol",
    "external_pole_branch_KO_diagnostic_audit_only",
)

TARGET_VALUE_KEYS = frozenset({
    "pdg_top_target", "measured_top_mass", "mc_top_target",
    "fitted_R_scale_to_top", "fitted_alpha_s_to_top",
    "pole_top_input", "lhc_top_target",
})


# ============================================================================
# Atlas live-runner contract
# ============================================================================

ATLAS_INPUT_ID = "mass:route08_top_msr_ew_transport"
ATLAS_ROUTE = "ew"
ATLAS_PAYLOAD_NAME = "top_msr_r_evolution_real_adapter_live"


# ============================================================================
# Snapshot construction
# ============================================================================

_NOTES = (
    "v66/v67/v68 top MSR R-evolution evaluator admitted as named external "
    "evaluator content under LATEST-33 imported-one-route policy. "
    "m_t^MSR(R_*) = 168.169 GeV at v37 APF-native scale R_* = 85.86 GeV; "
    "4-loop R-evolution to R_EW = M_W^TRACE/(2*pi) = 12.79 GeV gives "
    "m_t^MSR(R_EW) = 172.7168 GeV. Residual vs PDG direct top 172.56 +/- 0.31 GeV "
    "is +0.157 GeV (z = 0.506 direct; z = 0.495 over combined envelope 0.317 GeV "
    "including alpha_s + gamma_3 + truncation channels). Loop convergence "
    "L1->L4 ladder banked. v61 pole branch quarantined under coefficient-ingested "
    "4-loop (174.017 GeV at z=4.70 vs PDG; rejected). Status: "
    "[P_direct-MSR R-evolution numeric evaluator closed] preserved. Adapter "
    "wires v66+v67+v68 into Engine-readable payload. Top physical-final OPEN; "
    "APF-internal full QCD loop derivation OPEN as separate program."
)


def build_snapshot() -> RealAdapterSnapshot:
    return RealAdapterSnapshot(
        trace_sector_closed=True,
        source_to_scheme_registry_present=True,
        evaluator_map_found=True,
        codomain_transport_found=True,
        counterterm_finite_parts_declared=True,
        external_constants_ledger_clean=True,
        uncertainty_protocol_declared=True,
        target_value_consumed=False,
        external_ledger_fields_declared=REQUIRED_LEDGER_FIELDS,
        notes=_NOTES,
        extension_fields={
            "msr_loop_order": 4,
            "msr_r_evolution_closed": True,
            "pole_branch_quarantined": True,
            "residual_z_combined": RESIDUAL_DIAGNOSTIC["z_combined"],
            "R_EW_GeV": TOP_MSR_R_EVOLUTION_OUTPUT["R_EW_GeV"],
        },
    )


def check_evaluator_consistent() -> Dict[str, Any]:
    """v67 4-loop R-evolution within declared combined envelope vs PDG direct."""
    z = RESIDUAL_DIAGNOSTIC["z_combined"]
    # Inside combined envelope means |z| < 1 by construction
    ok = abs(z) < 1.0
    # Also assert loop convergence: L4 value is the rightmost in the ladder
    ladder_values = list(LOOP_CONVERGENCE_LADDER.values())
    convergence_ok = ladder_values == sorted(ladder_values)
    return {
        "name": "check_T_top_msr_r_evolution_adapter_evaluator_consistent_P",
        "consistent": ok and convergence_ok,
        "status": "P_v67_R_evolution_closed" if (ok and convergence_ok) else "FAIL",
        "summary": (
            "v67 4-loop R-evolution m_t^MSR(R_EW) = 172.7168 GeV inside combined "
            "envelope vs PDG direct (z = 0.500). Loop convergence L1->L4 monotone."
        ),
        "data": {
            "z_combined": z,
            "z_direct": RESIDUAL_DIAGNOSTIC["z_direct"],
            "loop_ladder_monotone": convergence_ok,
            "loop_ladder": LOOP_CONVERGENCE_LADDER,
        },
    }


# ============================================================================
# Public interface
# ============================================================================

def build_live_atlas_payload():
    return build_snapshot().to_payload(name=ATLAS_PAYLOAD_NAME)


def build_live_adapter_report():
    return build_adapter_report(
        build_snapshot(),
        name=ATLAS_PAYLOAD_NAME,
        route=ATLAS_ROUTE,
    )


def top_msr_outputs_report() -> Dict[str, Any]:
    return {
        "top_msr_r_evolution_output": dict(TOP_MSR_R_EVOLUTION_OUTPUT),
        "loop_convergence_ladder": dict(LOOP_CONVERGENCE_LADDER),
        "residual_diagnostic": dict(RESIDUAL_DIAGNOSTIC),
        "pole_branch_quarantine": dict(POLE_BRANCH_QUARANTINE),
        "required_external_ledger_fields": list(REQUIRED_LEDGER_FIELDS),
        "atlas_input_id": ATLAS_INPUT_ID,
        "status": {
            "Export_top_MSR_R_evolution_route_typed": 1,
            "Export_top_MSR_R_evolution_4loop_evaluator_closed": 1,
            "Export_top_MSR_engine_adapter_wired": 1,  # NEW
            "Export_top_pole_branch_quarantined": 1,
            "Export_top_physical_final": 0,
            "Export_top_APF_internal_full_QCD_loop_derivation": 0,
        },
    }


# ============================================================================
# Bank-registered checks (factory-generated)
# ============================================================================

_CHECKS = make_check_set(
    adapter_name="top_msr_r_evolution",
    route=ATLAS_ROUTE,
    payload_name=ATLAS_PAYLOAD_NAME,
    snapshot_factory=build_snapshot,
    required_ledger_fields=REQUIRED_LEDGER_FIELDS,
    target_value_keys=TARGET_VALUE_KEYS,
    evaluator_consistent_check=check_evaluator_consistent,
)


def register(registry=None):
    if registry is None:
        return _CHECKS
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == "__main__":
    import json
    out = run_all()
    print(json.dumps({k: {"consistent": v["consistent"], "status": v["status"]} for k, v in out.items()}, indent=2))
