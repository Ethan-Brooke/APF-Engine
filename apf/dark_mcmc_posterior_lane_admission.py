"""Dark Route-C MCMC posterior lane admission contract.

This module is contract-side only. It defines the MCMC posterior evidence lane
that runs in parallel with the profile-likelihood lane under
APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1.

It does not run chains, read posterior samples, or promote posterior P. Real
posterior promotion requires a later result pack with complete runtime artifacts,
convergence diagnostics, and no-smuggling reports for the declared grid.

Top marker: DARK_MCMC_POSTERIOR_LANE_ADMISSION_PASS
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List

PACK_NAME = "APF_DARK_MCMC_POSTERIOR_LANE_ADMISSION_v1"
SHARED_CONTRACT_PACK = "APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1"
PARENT_MCMC_LAUNCH_PACK = "APF_DARK_SECTOR_ROUTE_C_MCMC_POSTERIOR_LAUNCH_v1"
PARENT_PROFILE_LANE_PACK = "APF_DARK_PROFILE_LIKELIHOOD_LANE_ADMISSION_v1"
MARKER = "DARK_MCMC_POSTERIOR_LANE_ADMISSION_PASS"

DATASETS = (
    "desi_cmb_native",
    "desi_cmb_pantheonplus",
    "desi_cmb_union3",
    "desi_cmb_desy5",
)
MODELS = ("APF2_fixed_w2", "free_w0wa", "LCDM")
SAMPLED_PARAMETER_SET = ("H0", "ombh2", "omch2", "logA", "ns")
NOT_SAMPLED_V1 = ("tau", "mnu", "nnu")
POSTERIOR_COORDINATES = {
    "APF2_fixed_w2": SAMPLED_PARAMETER_SET,
    "free_w0wa": SAMPLED_PARAMETER_SET + ("w0", "wa"),
    "LCDM": SAMPLED_PARAMETER_SET,
}
CHAINS_REQUIRED = 4
DIAGNOSTIC_THRESHOLDS = {
    "Rminus1_max": 0.01,
    "ESS_min": 200,
    "chains_min": CHAINS_REQUIRED,
    "acceptance_min": 0.05,
    "acceptance_max": 0.80,
}

PROMOTED_FLAGS = {
    "Export_dark_MCMC_posterior_lane_admission_contract": 1,
    "Export_dark_MCMC_result_format_locked": 1,
    "Export_dark_MCMC_launch_supersession_declared": 1,
    "Export_dark_MCMC_diagnostic_thresholds_locked": 1,
}

PRESERVED_NON_CLAIMS = {
    "Export_dark_profile_likelihood_P": 0,
    "Export_dark_RouteC_MCMC_posterior_P": 0,
    "Export_dark_MCMC_full_posterior_P": 0,
    "Export_dark_robust_empirical_P": 0,
    "Export_dark_MCMC_partial_chain_as_converged_posterior": 0,
    "Export_dark_profile_best_as_posterior_MAP": 0,
    "Export_dark_APF2_full_shape_likelihood_P": 0,
    "Export_collaboration_NERSC_reproduction": 0,
}

@dataclass(frozen=True)
class MCMCRunCell:
    cell_id: str
    dataset: str
    model: str
    sampled_parameter_set: List[str]
    posterior_coordinates: List[str]
    chains_required: int
    required_artifact_class: str
    result_status: str = "required_pending_result"


def mcmc_run_grid() -> List[MCMCRunCell]:
    """Return the 4x3 MCMC posterior run grid locked by the shared contract."""
    cells: List[MCMCRunCell] = []
    idx = 1
    for dataset in DATASETS:
        for model in MODELS:
            artifact = (
                "posterior_chain_bundle_with_fixed_structural_w2"
                if model == "APF2_fixed_w2"
                else "posterior_chain_bundle_comparator_model"
            )
            cells.append(MCMCRunCell(
                cell_id=f"M{idx:02d}",
                dataset=dataset,
                model=model,
                sampled_parameter_set=list(SAMPLED_PARAMETER_SET),
                posterior_coordinates=list(POSTERIOR_COORDINATES[model]),
                chains_required=CHAINS_REQUIRED,
                required_artifact_class=artifact,
            ))
            idx += 1
    return cells


def build_lane_contract() -> Dict[str, Any]:
    """Build the machine-readable MCMC lane-admission contract."""
    return {
        "pack": PACK_NAME,
        "pack_type": "mcmc_posterior_lane_admission_not_result_pack",
        "parent_shared_contract": SHARED_CONTRACT_PACK,
        "parent_mcmc_launch": {
            "pack": PARENT_MCMC_LAUNCH_PACK,
            "latest": "LATEST-82",
            "grade": "launch_infrastructure_schema_adjudicator_not_converged_posterior_result",
            "status": "subsumed_as_parent_evidence_not_promoted",
        },
        "parallel_profile_lane": {
            "pack": PARENT_PROFILE_LANE_PACK,
            "status": "parallel_lane_context_only_not_posterior_evidence",
        },
        "lane_policy": {
            "profile_and_mcmc_are_parallel": True,
            "profile_best_may_seed_mcmc_initialization_only": True,
            "profile_best_as_posterior_MAP_forbidden": True,
            "partial_chain_as_posterior_forbidden": True,
            "apf2_coefficients_refit_forbidden": True,
            "mcmc_lane_question": "posterior mass support under the shared five-parameter runtime contract",
        },
        "runtime_contract_v1": {
            "sampled_parameter_set": list(SAMPLED_PARAMETER_SET),
            "not_sampled_v1": list(NOT_SAMPLED_V1),
            "lockstep_rule": "If tau, mnu, or nnu are added by a custom theory wrapper in v2, both profile and MCMC lanes must adopt the change together.",
            "version_pins": {"Cobaya": "3.6.2", "CAMB": "1.6.6"},
            "apf2_injection_mechanism": "runtime monkeypatch of camb.CAMBparams.__init__ / camb.CAMBparams.set_classes",
            "forbidden_apf2_injection_mechanism": "use_tabulated_w extra_args pathway",
        },
        "diagnostic_thresholds": DIAGNOSTIC_THRESHOLDS,
        "posterior_coordinates_by_model": {k: list(v) for k, v in POSTERIOR_COORDINATES.items()},
        "grid": [asdict(c) for c in mcmc_run_grid()],
        "required_result_artifacts": [
            "mcmc_result.json",
            "chain files for 4 chains per cell",
            "convergence_diagnostics.json",
            "posterior_summary.csv or posterior_summary.json",
            "bestfit_or_MAP_table.csv",
            "likelihood_manifest.json",
            "dataset_manifest.json",
            "environment_manifest.json",
            "input_ledger.json",
            "no_smuggling_report.json",
        ],
        "promotion_rule": {
            "can_promote_MCMC_posterior_P": False,
            "why_false": "This admission pack defines the lane and templates only. A future result pack must carry complete runtime artifacts and diagnostics for the declared grid or an explicitly scoped subset.",
            "future_result_thresholds": {
                "diagnostics": DIAGNOSTIC_THRESHOLDS,
                "profile_delta_gate_reference": "APF2_chi2_minus_free_w0wa_chi2 <= 5.991 per declared dataset, when used for profile-delta adjudication",
                "no_smuggling": "APF2 coefficients frozen; posterior target not constructed from posterior/profile outputs; no target-data backfit of w2 coefficients",
            },
        },
        "latest82_caveat": {
            "profile_best_vs_marginal_MAP": "Profile-best and MCMC marginal MAP may differ at numerically similar chi2 minima; this is not a defect.",
            "desi_cmb_native_profile_best": {"w0": -0.778, "wa": -0.781},
            "desi_cmb_native_partial_mcmc_marginal_MAP": {"w0": -0.54, "wa": -1.38},
            "seed_policy": "Profile output may seed initial points only; it must not be admitted as posterior evidence.",
        },
        "exports_promoted": PROMOTED_FLAGS,
        "exports_preserved_non_claims": PRESERVED_NON_CLAIMS,
        "verifier_marker": MARKER,
    }


def validate_mcmc_result_stub(result: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a future MCMC result at the contract boundary."""
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
    if result.get("profile_best_used_as_posterior_MAP", False):
        failures.append("profile_best_as_posterior_MAP_forbidden")
    if result.get("partial_chain_promoted", False):
        failures.append("partial_chain_as_posterior_forbidden")
    if int(result.get("chains_completed", 0)) < CHAINS_REQUIRED:
        failures.append("insufficient_chains")
    rminus1 = result.get("Rminus1_max")
    if rminus1 is None or rminus1 > DIAGNOSTIC_THRESHOLDS["Rminus1_max"]:
        failures.append("Rminus1_threshold_not_met")
    ess = result.get("ESS_min")
    if ess is None or ess < DIAGNOSTIC_THRESHOLDS["ESS_min"]:
        failures.append("ESS_threshold_not_met")
    acc = result.get("acceptance_mean")
    if acc is None or not (DIAGNOSTIC_THRESHOLDS["acceptance_min"] <= acc <= DIAGNOSTIC_THRESHOLDS["acceptance_max"]):
        failures.append("acceptance_rate_threshold_not_met")
    status = "PASS" if not failures else "HELD"
    return {"status": status, "failures": failures}


def check_mcmc_lane_contract_identity() -> Dict[str, Any]:
    c = build_lane_contract()
    passed = c["pack"] == PACK_NAME and c["pack_type"] == "mcmc_posterior_lane_admission_not_result_pack"
    return {"name": "check_mcmc_lane_contract_identity", "passed": passed, "status": "P_contract"}


def check_mcmc_lane_grid_complete() -> Dict[str, Any]:
    grid = mcmc_run_grid()
    pairs = {(c.dataset, c.model) for c in grid}
    passed = len(grid) == 12 and pairs == {(d, m) for d in DATASETS for m in MODELS}
    return {"name": "check_mcmc_lane_grid_complete", "passed": passed, "status": "P_contract"}


def check_mcmc_lane_parameter_lockstep() -> Dict[str, Any]:
    grid = mcmc_run_grid()
    passed = all(tuple(c.sampled_parameter_set) == SAMPLED_PARAMETER_SET for c in grid)
    return {"name": "check_mcmc_lane_parameter_lockstep", "passed": passed, "status": "P_contract"}


def check_posterior_coordinates_by_model() -> Dict[str, Any]:
    grid = mcmc_run_grid()
    passed = True
    for c in grid:
        if c.model == "free_w0wa":
            passed = passed and tuple(c.posterior_coordinates) == SAMPLED_PARAMETER_SET + ("w0", "wa")
        else:
            passed = passed and tuple(c.posterior_coordinates) == SAMPLED_PARAMETER_SET
    return {"name": "check_posterior_coordinates_by_model", "passed": passed, "status": "P_contract"}


def check_mcmc_diagnostics_thresholds_declared() -> Dict[str, Any]:
    t = DIAGNOSTIC_THRESHOLDS
    passed = t["chains_min"] == 4 and t["Rminus1_max"] == 0.01 and t["ESS_min"] == 200 and t["acceptance_min"] < t["acceptance_max"]
    return {"name": "check_mcmc_diagnostics_thresholds_declared", "passed": passed, "status": "P_contract"}


def check_partial_chain_not_posterior_guard() -> Dict[str, Any]:
    c = build_lane_contract()
    passed = (
        c["lane_policy"]["partial_chain_as_posterior_forbidden"]
        and c["exports_preserved_non_claims"]["Export_dark_MCMC_partial_chain_as_converged_posterior"] == 0
        and c["exports_preserved_non_claims"]["Export_dark_RouteC_MCMC_posterior_P"] == 0
    )
    return {"name": "check_partial_chain_not_posterior_guard", "passed": passed, "status": "P_guard"}


def check_profile_best_not_posterior_MAP_guard() -> Dict[str, Any]:
    c = build_lane_contract()
    passed = (
        c["lane_policy"]["profile_best_may_seed_mcmc_initialization_only"]
        and c["lane_policy"]["profile_best_as_posterior_MAP_forbidden"]
        and c["exports_preserved_non_claims"]["Export_dark_profile_best_as_posterior_MAP"] == 0
    )
    return {"name": "check_profile_best_not_posterior_MAP_guard", "passed": passed, "status": "P_guard"}


def check_mcmc_result_stub_fails_closed_on_partial_chain() -> Dict[str, Any]:
    placeholder = {
        "contract_pack": SHARED_CONTRACT_PACK,
        "lane_admission_pack": PACK_NAME,
        "sampled_parameter_set": list(SAMPLED_PARAMETER_SET),
        "apf2_coefficients_frozen": True,
        "apf2_coefficients_refit": False,
        "profile_best_used_as_posterior_MAP": False,
        "partial_chain_promoted": True,
        "chains_completed": 1,
        "Rminus1_max": 0.5,
        "ESS_min": 20,
        "acceptance_mean": 0.2,
    }
    verdict = validate_mcmc_result_stub(placeholder)
    passed = verdict["status"] == "HELD" and "partial_chain_as_posterior_forbidden" in verdict["failures"] and "insufficient_chains" in verdict["failures"]
    return {"name": "check_mcmc_result_stub_fails_closed_on_partial_chain", "passed": passed, "status": "P_guard"}


def run_checks() -> List[Dict[str, Any]]:
    return [
        check_mcmc_lane_contract_identity(),
        check_mcmc_lane_grid_complete(),
        check_mcmc_lane_parameter_lockstep(),
        check_posterior_coordinates_by_model(),
        check_mcmc_diagnostics_thresholds_declared(),
        check_partial_chain_not_posterior_guard(),
        check_profile_best_not_posterior_MAP_guard(),
        check_mcmc_result_stub_fails_closed_on_partial_chain(),
    ]


def check_all() -> Dict[str, Any]:
    checks = run_checks()
    return {
        "marker": MARKER if all(c["passed"] for c in checks) else "DARK_MCMC_POSTERIOR_LANE_ADMISSION_FAIL",
        "passed": all(c["passed"] for c in checks),
        "checks": checks,
    }




def register(registry):
    """Register this module's 8 MCMC lane-admission checks with the bank."""
    for fn in (
        check_mcmc_lane_contract_identity,
        check_mcmc_lane_grid_complete,
        check_mcmc_lane_parameter_lockstep,
        check_posterior_coordinates_by_model,
        check_mcmc_diagnostics_thresholds_declared,
        check_partial_chain_not_posterior_guard,
        check_profile_best_not_posterior_MAP_guard,
        check_mcmc_result_stub_fails_closed_on_partial_chain,
    ):
        registry[fn.__name__] = fn

if __name__ == "__main__":
    result = check_all()
    print(result["marker"])
    for check in result["checks"]:
        print(f"{check['name']}: {'PASS' if check['passed'] else 'FAIL'}")
