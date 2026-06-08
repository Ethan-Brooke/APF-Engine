"""Dark Route-C profile-likelihood lane admission contract.

This module is intentionally contract-side only. It defines the profile-likelihood
lane that will run in parallel with the MCMC lane under
APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1.

It does not evaluate a Cobaya likelihood and does not promote profile-likelihood P.
Real result promotion requires a later result pack carrying runtime artifacts.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List

PACK_NAME = "APF_DARK_PROFILE_LIKELIHOOD_LANE_ADMISSION_v1"
SHARED_CONTRACT_PACK = "APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1"
PARENT_PROFILE_PROBE_PACK = "APF_DARK_SECTOR_ROUTE_C_PROFILE_PROBE_ALL_DATASETS_v1"
PARENT_MCMC_LAUNCH_PACK = "APF_DARK_SECTOR_ROUTE_C_MCMC_POSTERIOR_LAUNCH_v1"
MARKER = "DARK_PROFILE_LIKELIHOOD_LANE_ADMISSION_PASS"

DATASETS = (
    "desi_cmb_native",
    "desi_cmb_pantheonplus",
    "desi_cmb_union3",
    "desi_cmb_desy5",
)
MODELS = ("APF2_fixed_w2", "free_w0wa", "LCDM")
SAMPLED_PARAMETER_SET = ("H0", "ombh2", "omch2", "logA", "ns")
NOT_SAMPLED_V1 = ("tau", "mnu", "nnu")
OUTER_PROFILE_COORDINATES = ("w0", "wa")

PROMOTED_FLAGS = {
    "Export_dark_profile_likelihood_lane_admission_contract": 1,
    "Export_dark_profile_likelihood_full_scan_format_locked": 1,
    "Export_dark_profile_likelihood_probe_supersession_declared": 1,
}

PRESERVED_NON_CLAIMS = {
    "Export_dark_profile_likelihood_P": 0,
    "Export_dark_RouteC_MCMC_posterior_P": 0,
    "Export_dark_MCMC_full_posterior_P": 0,
    "Export_dark_robust_empirical_P": 0,
    "Export_dark_profile_probe_as_full_scan_P": 0,
    "Export_dark_profile_best_as_posterior_MAP": 0,
    "Export_dark_APF2_full_shape_likelihood_P": 0,
    "Export_collaboration_NERSC_reproduction": 0,
}

@dataclass(frozen=True)
class ProfileRunCell:
    cell_id: str
    dataset: str
    model: str
    sampled_parameter_set: List[str]
    outer_profile_coordinates: List[str]
    required_artifact_class: str
    result_status: str = "required_pending_result"


def profile_run_grid() -> List[ProfileRunCell]:
    """Return the 4x3 profile-likelihood run grid locked by the shared contract."""
    cells: List[ProfileRunCell] = []
    idx = 1
    for dataset in DATASETS:
        for model in MODELS:
            outer = list(OUTER_PROFILE_COORDINATES) if model == "free_w0wa" else []
            artifact = (
                "continuous_or_adaptive_w0wa_profile_surface"
                if model == "free_w0wa"
                else "fixed_model_profiled_nuisance_minimum"
            )
            cells.append(ProfileRunCell(
                cell_id=f"P{idx:02d}",
                dataset=dataset,
                model=model,
                sampled_parameter_set=list(SAMPLED_PARAMETER_SET),
                outer_profile_coordinates=outer,
                required_artifact_class=artifact,
            ))
            idx += 1
    return cells


def build_lane_contract() -> Dict[str, Any]:
    """Build the machine-readable lane-admission contract."""
    return {
        "pack": PACK_NAME,
        "pack_type": "profile_likelihood_lane_admission_not_result_pack",
        "parent_shared_contract": SHARED_CONTRACT_PACK,
        "parent_profile_probe": {
            "pack": PARENT_PROFILE_PROBE_PACK,
            "grade": "probe_grade_discrete_3x3_grid_candidate_not_full_scan",
            "status": "subsumed_as_parent_evidence_not_promoted",
        },
        "parent_mcmc_launch": {
            "pack": PARENT_MCMC_LAUNCH_PACK,
            "grade": "launch_infrastructure_not_posterior_result",
            "status": "parallel_lane_context_only",
        },
        "lane_policy": {
            "profile_and_mcmc_are_parallel": True,
            "profile_best_may_seed_mcmc_initialization_only": True,
            "profile_best_as_posterior_evidence_forbidden": True,
            "profile_probe_as_full_scan_forbidden": True,
            "apf2_coefficients_refit_forbidden": True,
            "profile_lane_question": "point-likelihood support after profiling the shared five-parameter nuisance set",
        },
        "runtime_contract_v1": {
            "sampled_parameter_set": list(SAMPLED_PARAMETER_SET),
            "not_sampled_v1": list(NOT_SAMPLED_V1),
            "outer_profile_coordinates_for_free_w0wa": list(OUTER_PROFILE_COORDINATES),
            "version_pins": {"Cobaya": "3.6.2", "CAMB": "1.6.6"},
            "apf2_injection_mechanism": "runtime monkeypatch of camb.CAMBparams.__init__ / camb.CAMBparams.set_classes",
            "forbidden_apf2_injection_mechanism": "use_tabulated_w extra_args pathway",
        },
        "grid": [asdict(c) for c in profile_run_grid()],
        "required_result_artifacts": [
            "profile_result.json",
            "profile_surface.csv or profile_trace.csv",
            "bestfit_table.csv",
            "likelihood_manifest.json",
            "dataset_manifest.json",
            "environment_manifest.json",
            "input_ledger.json",
            "no_smuggling_report.json",
        ],
        "promotion_rule": {
            "can_promote_profile_likelihood_P": False,
            "why_false": "This admission pack defines the lane and templates only. A future result pack must carry complete runtime artifacts for every required cell or an explicit scoped subset.",
            "future_result_threshold": "APF2_chi2_minus_profile_best <= 5.991 per declared dataset under the 2-dof 95% gate, with all no-smuggling and shared-contract checks passing.",
        },
        "exports_promoted": PROMOTED_FLAGS,
        "exports_preserved_non_claims": PRESERVED_NON_CLAIMS,
        "verifier_marker": MARKER,
    }


def validate_profile_result_stub(result: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a future profile result at the contract boundary."""
    failures: List[str] = []
    if result.get("contract_pack") != SHARED_CONTRACT_PACK:
        failures.append("contract_pack_mismatch")
    if result.get("lane_admission_pack") != PACK_NAME:
        failures.append("lane_admission_pack_mismatch")
    if result.get("sampled_parameter_set") != list(SAMPLED_PARAMETER_SET):
        failures.append("sampled_parameter_set_mismatch")
    if not result.get("apf2_coefficients_frozen", False):
        failures.append("apf2_coefficients_not_frozen")
    if result.get("apf2_coefficients_refit", False):
        failures.append("apf2_coefficients_refit_forbidden")
    if result.get("profile_probe_used_as_full_scan", False):
        failures.append("profile_probe_used_as_full_scan_forbidden")
    status = "PASS" if not failures else "HELD"
    return {"status": status, "failures": failures}


def check_profile_likelihood_lane_contract_identity() -> Dict[str, Any]:
    c = build_lane_contract()
    passed = c["pack"] == PACK_NAME and c["pack_type"] == "profile_likelihood_lane_admission_not_result_pack"
    return {"name": "check_profile_likelihood_lane_contract_identity", "passed": passed, "status": "P_contract"}


def check_profile_likelihood_lane_grid_complete() -> Dict[str, Any]:
    grid = profile_run_grid()
    pairs = {(c.dataset, c.model) for c in grid}
    passed = len(grid) == 12 and pairs == {(d, m) for d in DATASETS for m in MODELS}
    return {"name": "check_profile_likelihood_lane_grid_complete", "passed": passed, "status": "P_contract"}


def check_profile_likelihood_lane_parameter_lockstep() -> Dict[str, Any]:
    grid = profile_run_grid()
    passed = all(tuple(c.sampled_parameter_set) == SAMPLED_PARAMETER_SET for c in grid)
    return {"name": "check_profile_likelihood_lane_parameter_lockstep", "passed": passed, "status": "P_contract"}


def check_profile_probe_not_full_scan_guard() -> Dict[str, Any]:
    c = build_lane_contract()
    passed = (
        c["parent_profile_probe"]["grade"] == "probe_grade_discrete_3x3_grid_candidate_not_full_scan"
        and c["exports_preserved_non_claims"]["Export_dark_profile_probe_as_full_scan_P"] == 0
        and c["exports_preserved_non_claims"]["Export_dark_profile_likelihood_P"] == 0
    )
    return {"name": "check_profile_probe_not_full_scan_guard", "passed": passed, "status": "P_guard"}


def check_profile_best_not_posterior_guard() -> Dict[str, Any]:
    c = build_lane_contract()
    passed = (
        c["lane_policy"]["profile_best_may_seed_mcmc_initialization_only"]
        and c["lane_policy"]["profile_best_as_posterior_evidence_forbidden"]
        and c["exports_preserved_non_claims"]["Export_dark_profile_best_as_posterior_MAP"] == 0
    )
    return {"name": "check_profile_best_not_posterior_guard", "passed": passed, "status": "P_guard"}


def check_profile_result_stub_fails_closed_on_placeholder() -> Dict[str, Any]:
    placeholder = {
        "contract_pack": SHARED_CONTRACT_PACK,
        "lane_admission_pack": PACK_NAME,
        "sampled_parameter_set": list(SAMPLED_PARAMETER_SET),
        "apf2_coefficients_frozen": True,
        "apf2_coefficients_refit": False,
        "profile_probe_used_as_full_scan": True,
    }
    verdict = validate_profile_result_stub(placeholder)
    passed = verdict["status"] == "HELD" and "profile_probe_used_as_full_scan_forbidden" in verdict["failures"]
    return {"name": "check_profile_result_stub_fails_closed_on_placeholder", "passed": passed, "status": "P_guard"}


def run_checks() -> List[Dict[str, Any]]:
    return [
        check_profile_likelihood_lane_contract_identity(),
        check_profile_likelihood_lane_grid_complete(),
        check_profile_likelihood_lane_parameter_lockstep(),
        check_profile_probe_not_full_scan_guard(),
        check_profile_best_not_posterior_guard(),
        check_profile_result_stub_fails_closed_on_placeholder(),
    ]


def check_all() -> Dict[str, Any]:
    checks = run_checks()
    return {
        "marker": MARKER if all(c["passed"] for c in checks) else "DARK_PROFILE_LIKELIHOOD_LANE_ADMISSION_FAIL",
        "passed": all(c["passed"] for c in checks),
        "checks": checks,
    }



def register(registry):
    """Register this module's 6 lane-admission checks with the bank."""
    registry[check_profile_likelihood_lane_contract_identity.__name__] = (
        check_profile_likelihood_lane_contract_identity
    )
    registry[check_profile_likelihood_lane_grid_complete.__name__] = (
        check_profile_likelihood_lane_grid_complete
    )
    registry[check_profile_likelihood_lane_parameter_lockstep.__name__] = (
        check_profile_likelihood_lane_parameter_lockstep
    )
    registry[check_profile_probe_not_full_scan_guard.__name__] = (
        check_profile_probe_not_full_scan_guard
    )
    registry[check_profile_best_not_posterior_guard.__name__] = (
        check_profile_best_not_posterior_guard
    )
    registry[check_profile_result_stub_fails_closed_on_placeholder.__name__] = (
        check_profile_result_stub_fails_closed_on_placeholder
    )

if __name__ == "__main__":
    result = check_all()
    for c in result["checks"]:
        print(f"{c['name']}: {'PASS' if c['passed'] else 'FAIL'}")
    print(result["marker"])
