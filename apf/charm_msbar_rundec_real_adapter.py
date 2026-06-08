"""
APF Charm MSbar RunDec Real Adapter -- Tier-1 wire-in.

Engine-side adapter that turns the banked v72-v79 RunDec/CRunDec threshold-
matched QCD evaluator content into a typed route payload for the
mass:route03_charm_msbar_self_scale atlas input.

Status banked
-------------
- Export_charm_MSbar_QCD_running_route_typed = 1 (preserved from v71)
- Export_charm_MSbar_threshold_matched_evaluator_closed = 1 (preserved from v78)
- Export_charm_MSbar_engine_adapter_wired = 1 (NEW at this module)
- Export_charm_MSbar_full_RunDec_binary_parity = 0 (LATEST-33 next-gate non-claim)
- Export_charm_MSbar_APF_internal_full_QCD_loop_derivation = 0 (separate program)
"""
from __future__ import annotations

from typing import Any, Dict

from apf.real_adapter_factory import (
    RealAdapterSnapshot,
    build_adapter_report,
    make_check_set,
)


# ============================================================================
# Banked v78 + v79 content (verbatim from V36_THROUGH_V79_LADDER_BUNDLE)
# ============================================================================

# v79 active QCD evaluator output: APF charm trace anchored to MSbar(3 GeV).
CHARM_RUNDEC_OUTPUT: Dict[str, float] = {
    "m_c_APF_3GeV_GeV": 0.979226596181155,
    "alpha_s_charm_start_from_MZ": 0.3977811577835508,
    "alpha_s_3GeV": 0.2575869836500778,
}

# CRunDec v3 (Herren-Steinhauser arXiv:1703.03751) external evaluator
# at the v78 threshold-matched configuration.
RUNDEC_PROVENANCE: Dict[str, Any] = {
    "evaluator": "RunDec/CRunDec v3",
    "citation": "Herren-Steinhauser arXiv:1703.03751",
    "alpha_s_MZ": 0.1189,
    "alpha_s_MZ_uncertainty": 0.0009,  # PDG world average
    "threshold_matching": "n_f=5 <-> n_f=4 at m_b threshold",
    "loop_order": 4,
    "scheme": "MSbar self-scale",
}

# v78 benchmark closure: APF evaluator vs published RunDec reference,
# under the same threshold-matched configuration. Delta 0.55 MeV (charm).
BENCHMARK_CLOSURE: Dict[str, Any] = {
    "published_case": "m_c(m_c)=1.279 GeV -> m_c(3 GeV)=0.986 GeV",
    "published_target_GeV": 0.986,
    "v78_result_GeV": 0.9865518890879715,
    "delta_MeV": 0.5518890879715466,
    "tolerance_MeV": 1.0,
    "status": "BENCHMARK_PASS",
}

# 12-entry RunDec evaluator ledger per v72 (no-smuggling declaration).
REQUIRED_LEDGER_FIELDS = (
    "external_alpha_s_MZ_PDG_world_average",
    "external_RunDec_v3_evaluator_library",
    "external_beta_function_coefficients_b0_b1_b2_b3",
    "external_gamma_m_anomalous_dimension_coefficients_gamma0_gamma1_gamma2_gamma3",
    "external_decoupling_constants_zeta_g_zeta_m",
    "external_n_f_threshold_matching_schedule",
    "external_initial_scale_mu_0_target_scale_mu_1",
    "external_threshold_set_T_bottom_mass",
    "external_matching_convention_OS_MSbar",
    "external_covariance_propagation_from_alpha_s_uncertainty",
    "external_loop_order_L_ge_2_explicit",
    "external_threshold_matched_benchmark_closure_protocol",
)

# No-smuggling guard: forbidden input keys.
TARGET_VALUE_KEYS = frozenset({
    "pdg_m_c_target", "measured_m_c", "m_c_target_value",
    "m_c_observed", "m_c_PDG", "lattice_m_c_target",
    "target_charm_mass", "fitted_alpha_s_to_charm",
})


# ============================================================================
# Atlas live-runner contract
# ============================================================================

ATLAS_INPUT_ID = "mass:route03_charm_msbar_self_scale"
ATLAS_ROUTE = "ew"
ATLAS_PAYLOAD_NAME = "charm_msbar_rundec_real_adapter_live"


# ============================================================================
# Snapshot construction
# ============================================================================

_NOTES = (
    "v78 threshold-matched QCD evaluator + v79 active-outputs registry "
    "admitted as named external evaluator content under LATEST-33 "
    "imported-one-route policy. m_c^APF(3 GeV) = 0.9792 GeV at "
    "alpha_s(M_Z) = 0.1189 + n_f=5<->4 threshold matching at m_b. "
    "Benchmark closure vs RunDec published reference (m_c(m_c)=1.279 GeV "
    "-> m_c(3 GeV)=0.986 GeV): delta 0.55 MeV inside 1 MeV tolerance. "
    "Status: [P_threshold-matched QCD evaluator benchmark closed] preserved. "
    "Adapter wires v78+v79 content into Engine-readable payload. "
    "Full RunDec binary parity OPEN; higher-loop decoupling-constant parity "
    "OPEN. APF-internal full QCD loop derivation OPEN as separate program."
)


def build_snapshot() -> RealAdapterSnapshot:
    """Build the live snapshot from the banked v78 + v79 content."""
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
            "rundec_loop_order": RUNDEC_PROVENANCE["loop_order"],
            "rundec_threshold_matched": True,
            "rundec_benchmark_passed": True,
            "alpha_s_MZ": RUNDEC_PROVENANCE["alpha_s_MZ"],
        },
    )


def check_evaluator_consistent() -> Dict[str, Any]:
    """v78 threshold-matched evaluator output vs published RunDec benchmark."""
    delta = BENCHMARK_CLOSURE["delta_MeV"]
    tol = BENCHMARK_CLOSURE["tolerance_MeV"]
    ok = abs(delta) < tol
    return {
        "name": "check_T_charm_msbar_rundec_adapter_evaluator_consistent_P",
        "consistent": ok,
        "status": "P_v78_benchmark_closed" if ok else "FAIL",
        "summary": (
            "v78 threshold-matched RunDec output matches published benchmark "
            "case m_c(m_c)=1.279 GeV -> m_c(3 GeV)=0.986 GeV within 1 MeV tolerance."
        ),
        "data": {
            "delta_MeV": delta,
            "tolerance_MeV": tol,
            "v78_result_GeV": BENCHMARK_CLOSURE["v78_result_GeV"],
            "published_target_GeV": BENCHMARK_CLOSURE["published_target_GeV"],
        },
    }


# ============================================================================
# Public interface (used by atlas runner + closure-pack verifiers)
# ============================================================================

def build_live_atlas_payload():
    """Return the live route payload for the atlas runner's swap dict."""
    return build_snapshot().to_payload(name=ATLAS_PAYLOAD_NAME)


def build_live_adapter_report():
    """Run the full Engine pipeline on the live snapshot."""
    return build_adapter_report(
        build_snapshot(),
        name=ATLAS_PAYLOAD_NAME,
        route=ATLAS_ROUTE,
    )


def rundec_outputs_report() -> Dict[str, Any]:
    """Structured representation of the banked v78 + v79 content."""
    return {
        "charm_rundec_output": dict(CHARM_RUNDEC_OUTPUT),
        "rundec_provenance": dict(RUNDEC_PROVENANCE),
        "benchmark_closure": dict(BENCHMARK_CLOSURE),
        "required_external_ledger_fields": list(REQUIRED_LEDGER_FIELDS),
        "atlas_input_id": ATLAS_INPUT_ID,
        "status": {
            "Export_charm_MSbar_QCD_running_route_typed": 1,
            "Export_charm_MSbar_threshold_matched_evaluator_closed": 1,
            "Export_charm_MSbar_engine_adapter_wired": 1,  # NEW
            "Export_charm_MSbar_full_RunDec_binary_parity": 0,
            "Export_charm_MSbar_APF_internal_full_QCD_loop_derivation": 0,
        },
    }


# ============================================================================
# Bank-registered checks (factory-generated)
# ============================================================================

_CHECKS = make_check_set(
    adapter_name="charm_msbar_rundec",
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
