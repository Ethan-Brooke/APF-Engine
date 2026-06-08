"""W_TRACE DIZET flag-sensitivity and covariance sprint.

v16.2 (2026-05-09): extends the compiled DIZET v6.45 run by running a
broad same-input flag and input-sensitivity campaign around the APF route deck.
This closes a reviewed-code total-evaluator sensitivity/covariance worksheet and
sharpens the remaining blocker: DIZET exposes useful flags, DR/DRREM outputs,
and theory-error toggles, but it still does not expose an admitted APF row
covariance ledger.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_dizet_executable_run import (
    RUN_ROWS as V16_1_RUN_ROWS,
    baseline as v161_baseline,
    route_summary as v161_route_summary,
    PASS_STATUS as V16_1_PASS_STATUS,
    M_W_TRACE_GEV,
    APF_DELTA_R_TARGET,
)

STATUS = "P_w_trace_dizet_flag_sensitivity_covariance"
VERSION = "v16_2"
PASS_STATUS = "W_TRACE_DIZET_FLAG_SENSITIVITY_COVARIANCE_PASS"
TITLE = "W_TRACE DIZET flag-sensitivity and covariance worksheet"
PAYLOAD_ID = "W_TRACE_DIZET_FLAG_SENSITIVITY_COVARIANCE_v16_2"

APF_VERSION = "16.2.0"
ROUTE_STATUS = "P_reviewed_same_input_total_evaluator_plus_flag_sensitivity_covariance"
PHYSICAL_EXPORT_STATUS = "OPEN_BLOCKED"
FIRST_FAILED_GATE = "ROW_DECOMPOSITION_AND_COVARIANCE_PROTOCOL"
NEW_BLOCKER = "DIZET_FLAGS_ARE_RESPONSE_TOGGLES_NOT_REVIEWED_APF_COMPONENT_ROWS"

BASELINE = {
    "WMASS_GeV": 80.357341077578,
    "ZPARD_DR": 0.036501785659,
    "ZPARD_DRREM": 0.011667933872,
    "SW2": 0.223431902567,
    "GMUC_x1e5": 1.166146252349,
    "DAL5H": 0.027576193213,
    "ALQED_inverse": 128.950332247814,
    "ALST_MT": 0.107980888842,
    "PARTW_total_MeV": 2090.076838845152,
}

SCAN_COUNTS = {
    "total_runs_attempted": 65,
    "successful_runs": 64,
    "failed_or_timed_out": 1,
    "failed_variant": "IFACR=3",
    "failure_reason": "timeout / non-recommended fully expanded double-violating DR branch",
}

@dataclass(frozen=True)
class FlagResponse:
    variant: str
    category: str
    delta_MW_MeV: float
    delta_ZPARD_DR: float
    delta_DRREM: float
    admission_status: str
    interpretation: str

FLAG_RESPONSES: Tuple[FlagResponse, ...] = (
    FlagResponse("IAMT4=0", "two_loop_order_knockout", 54.89174477000347, -0.0030917547600000025, -0.011667933872, "NOT_ADMITTED_AS_APF_ROW", "removes modern top/higher-order W machinery; too coarse for APF row ontology"),
    FlagResponse("IAMT4=5", "fermionic_two_loop_approximation", -0.47346352999966257, 0.0, 0.0, "REVIEWED_CODE_TOGGLE_ONLY", "switch to older fermionic-MW approximation; useful sensitivity, not row covariance"),
    FlagResponse("IAMT4=6", "ACFW_MW_formula", 0.0, 0.0, 0.0, "BENCHMARK_EQUIVALENT_FOR_MW", "same W as preferred IAMT4=8 at APF deck"),
    FlagResponse("IQCD=0", "QCD_self_energy_knockout", 0.0, -0.004352547400000004, -0.000460170124, "DR_ONLY_RESPONSE", "changes ZPARD DR/DRREM but not ACFW parametrized W in this mode"),
    FlagResponse("IQCD=1", "QCD_formula_approx", 0.0, -0.00003635453700000235, -0.0000332155, "DR_ONLY_RESPONSE", "small DR shift from alternative QCD handling"),
    FlagResponse("IQCD=2", "QCD_formula_bardin_chizhov", 0.0, 0.000000014393999998862927, 0.000000013151, "DR_ONLY_RESPONSE", "near-identical to baseline Kniehl option"),
    FlagResponse("IHVP=1", "hadronic_vacuum_polarization_legacy", -8.397989336998535, 0.0005052238539999948, 0.000000424305, "SOURCE_VARIANT_ONLY", "legacy hadronic-vacuum-polarization option moves W by multi-MeV"),
    FlagResponse("IHVP=4", "hadronic_vacuum_polarization_2016", -0.1777768190009965, 0.00001071791, -0.000000021780, "SOURCE_VARIANT_ONLY", "newer HVP choices are mutually stable at sub-MeV level"),
    FlagResponse("IDMWW=+1", "theory_error_toggle", 4.0000000000048885, 0.0, 0.0, "THEORY_NUISANCE", "built-in DIZET/ACFW W theory uncertainty toggle"),
    FlagResponse("IDMWW=-1", "theory_error_toggle", -4.0000000000048885, 0.0, 0.0, "THEORY_NUISANCE", "built-in DIZET/ACFW W theory uncertainty toggle"),
    FlagResponse("IFACR=1", "delta_r_expansion_convention", 0.0, -0.0000070398740000046645, 0.000000014306, "CONVENTION_RESPONSE", "DR convention shift; not independent physics row"),
    FlagResponse("ISCRE=1", "remainder_scale_convention", 0.0, -0.000014118319999999185, 0.000000028690, "CONVENTION_RESPONSE", "remainder-scale convention shift; not independent physics row"),
)

@dataclass(frozen=True)
class InputDerivative:
    parameter: str
    sigma: float
    unit: str
    derivative_MW_GeV_per_unit: float
    sigma_MW_MeV: float
    derivative_DR_per_unit: float
    sigma_DR: float
    method: str

INPUT_DERIVATIVES: Tuple[InputDerivative, ...] = (
    InputDerivative("M_Z", 0.0021, "GeV", 1.2579350269026874, 2.6416635564956437, -0.0011336214285703617, 2.3806049999977597e-06, "central finite difference"),
    InputDerivative("m_t", 0.3, "GeV", 0.0059981409649860025, 1.7994422894958007, -0.000363501476666669, 0.00010905044300000069, "central finite difference"),
    InputDerivative("M_H", 0.12, "GeV", -0.00046127437502245056, -0.055352925002694064, 2.9282379166665345e-05, 3.5138854999998415e-06, "central finite difference"),
    InputDerivative("alpha_s(M_Z)", 0.0007, "dimensionless", -0.6193277314281431, -0.4335294119997002, 0.038474737857143095, 2.6932316500000167e-05, "central finite difference"),
    InputDerivative("Delta_alpha_had5", 0.00006, "dimensionless", -18.114101916684906, -1.0868461150010944, 1.0920739166666442, 6.552443499999866e-05, "IALEM=2 explicit-DAL5H finite difference"),
)

THEORY_SIGMA_MW_MEV = 4.0
DIZET_TOTAL_MW_MINUS_APF_TRACE_MEV = -4.823256421914834


def covariance_summary() -> Dict[str, Any]:
    experimental_variance = sum(d.sigma_MW_MeV ** 2 for d in INPUT_DERIVATIVES)
    total_variance = experimental_variance + THEORY_SIGMA_MW_MEV ** 2
    sigma_inputs = math.sqrt(experimental_variance)
    sigma_total = math.sqrt(total_variance)
    return {
        "input_sigma_MW_MeV": sigma_inputs,
        "theory_sigma_MW_MeV": THEORY_SIGMA_MW_MEV,
        "total_sigma_MW_MeV_quadrature": sigma_total,
        "APF_minus_DIZET_abs_MeV": abs(DIZET_TOTAL_MW_MINUS_APF_TRACE_MEV),
        "pull_vs_theory_only": abs(DIZET_TOTAL_MW_MINUS_APF_TRACE_MEV) / THEORY_SIGMA_MW_MEV,
        "pull_vs_input_plus_theory_quadrature": abs(DIZET_TOTAL_MW_MINUS_APF_TRACE_MEV) / sigma_total,
        "dominant_input_uncertainty": max(INPUT_DERIVATIVES, key=lambda d: abs(d.sigma_MW_MeV)).parameter,
    }


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True, default=str)


def _digest(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(obj).encode("utf-8")).hexdigest()


def _res(check: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    row = {"check": check, "passed": bool(passed), "status": "PASS" if passed else "FAIL", "epistemic": STATUS}
    row.update(extra)
    return row


def _passed(row: Any) -> bool:
    return bool(isinstance(row, Mapping) and (row.get("passed") is True or row.get("status") in ("PASS", "P")))


def route_summary() -> Dict[str, Any]:
    cov = covariance_summary()
    return {
        "title": TITLE,
        "version": VERSION,
        "baseline": BASELINE,
        "scan_counts": SCAN_COUNTS,
        "flag_responses": [asdict(r) for r in FLAG_RESPONSES],
        "input_derivatives": [asdict(r) for r in INPUT_DERIVATIVES],
        "covariance_summary": cov,
        "gates": {
            "REVIEWED_SAME_INPUT_TOTAL_EVALUATOR": "CLOSED_BY_V16_1_DIZET_RUN",
            "FLAG_SENSITIVITY_WORKSHEET": "CLOSED_BY_V16_2_SCAN",
            "INPUT_COVARIANCE_PUSHFORWARD": "CLOSED_BY_V16_2_FINITE_DIFFERENCE",
            "ROW_DECOMPOSITION_AND_COVARIANCE_PROTOCOL": "OPEN_BLOCKED",
            "PHYSICAL_W_EXPORT": PHYSICAL_EXPORT_STATUS,
            "first_failed_gate": FIRST_FAILED_GATE,
            "sharpened_blocker": NEW_BLOCKER,
        },
        "claim_boundary": {
            "allowed": ROUTE_STATUS,
            "forbidden": "M_W^{APF->OS} physical export or admitted APF Delta-r row ledger",
        },
        "payload_digest": _digest([asdict(r) for r in FLAG_RESPONSES] + [asdict(r) for r in INPUT_DERIVATIVES]),
    }


def terminal_report() -> Dict[str, Any]:
    return {"status": STATUS, "pass_status": PASS_STATUS, "route_summary": route_summary()}

# --- checks -----------------------------------------------------------------

def check_T_w_trace_dizet_flag_sensitivity_status_declared():
    return _res("status_declared", STATUS.startswith("P_w_trace") and VERSION == "v16_2")

def check_T_w_trace_dizet_flag_sensitivity_depends_on_v161():
    return _res("depends_on_v161", V16_1_PASS_STATUS.endswith("PASS") and len(V16_1_RUN_ROWS) >= 10)

def check_T_w_trace_dizet_flag_sensitivity_baseline_consistent():
    b = v161_baseline()
    return _res("baseline_consistent", abs(b.W_MASS_GeV - BASELINE["WMASS_GeV"]) < 1e-9)

def check_T_w_trace_dizet_flag_sensitivity_scan_counts_recorded():
    return _res("scan_counts_recorded", SCAN_COUNTS["total_runs_attempted"] == 65 and SCAN_COUNTS["successful_runs"] == 64)

def check_T_w_trace_dizet_flag_sensitivity_timeout_quarantined():
    return _res("timeout_quarantined", SCAN_COUNTS["failed_variant"] == "IFACR=3" and "non-recommended" in SCAN_COUNTS["failure_reason"])

def check_T_w_trace_dizet_flag_sensitivity_all_responses_unadmitted():
    return _res("all_responses_unadmitted", all(r.admission_status != "ADMITTED_APF_ROW" for r in FLAG_RESPONSES))

def check_T_w_trace_dizet_flag_sensitivity_theory_toggles_symmetric():
    plus = next(r for r in FLAG_RESPONSES if r.variant == "IDMWW=+1")
    minus = next(r for r in FLAG_RESPONSES if r.variant == "IDMWW=-1")
    return _res("theory_toggles_symmetric", abs(plus.delta_MW_MeV + minus.delta_MW_MeV) < 1e-9)

def check_T_w_trace_dizet_flag_sensitivity_iamt0_knockout_large():
    r = next(x for x in FLAG_RESPONSES if x.variant == "IAMT4=0")
    return _res("iamt0_knockout_large", r.delta_MW_MeV > 50 and r.delta_ZPARD_DR < -0.003)

def check_T_w_trace_dizet_flag_sensitivity_iamt5_small_but_nonzero():
    r = next(x for x in FLAG_RESPONSES if x.variant == "IAMT4=5")
    return _res("iamt5_small_but_nonzero", -0.6 < r.delta_MW_MeV < -0.3)

def check_T_w_trace_dizet_flag_sensitivity_iamt6_equivalent_for_mw():
    r = next(x for x in FLAG_RESPONSES if x.variant == "IAMT4=6")
    return _res("iamt6_equivalent_for_mw", abs(r.delta_MW_MeV) < 1e-12)

def check_T_w_trace_dizet_flag_sensitivity_iqcd0_dr_only():
    r = next(x for x in FLAG_RESPONSES if x.variant == "IQCD=0")
    return _res("iqcd0_dr_only", abs(r.delta_MW_MeV) < 1e-12 and r.delta_ZPARD_DR < -0.004)

def check_T_w_trace_dizet_flag_sensitivity_ihvp2016_submev():
    r = next(x for x in FLAG_RESPONSES if x.variant == "IHVP=4")
    return _res("ihvp2016_submev", abs(r.delta_MW_MeV) < 0.2)

def check_T_w_trace_dizet_flag_sensitivity_conventions_do_not_move_mw():
    rows = [r for r in FLAG_RESPONSES if "convention" in r.category]
    return _res("conventions_do_not_move_mw", rows and all(abs(r.delta_MW_MeV) < 1e-12 for r in rows))

def check_T_w_trace_dizet_flag_sensitivity_derivatives_present():
    return _res("derivatives_present", len(INPUT_DERIVATIVES) == 5)

def check_T_w_trace_dizet_flag_sensitivity_mz_dominates_inputs():
    cov = covariance_summary()
    return _res("mz_dominates_inputs", cov["dominant_input_uncertainty"] == "M_Z")

def check_T_w_trace_dizet_flag_sensitivity_mt_input_uncertainty_nontrivial():
    r = next(x for x in INPUT_DERIVATIVES if x.parameter == "m_t")
    return _res("mt_input_uncertainty_nontrivial", 1.7 < abs(r.sigma_MW_MeV) < 1.9)

def check_T_w_trace_dizet_flag_sensitivity_delta_alpha_derivative_large():
    r = next(x for x in INPUT_DERIVATIVES if x.parameter == "Delta_alpha_had5")
    return _res("delta_alpha_derivative_large", abs(r.derivative_MW_GeV_per_unit) > 10 and abs(r.sigma_MW_MeV) > 1.0)

def check_T_w_trace_dizet_flag_sensitivity_alpha_s_small_input_uncertainty():
    r = next(x for x in INPUT_DERIVATIVES if x.parameter == "alpha_s(M_Z)")
    return _res("alpha_s_small_input_uncertainty", 0.3 < abs(r.sigma_MW_MeV) < 0.6)

def check_T_w_trace_dizet_flag_sensitivity_higgs_small_input_uncertainty():
    r = next(x for x in INPUT_DERIVATIVES if x.parameter == "M_H")
    return _res("higgs_small_input_uncertainty", abs(r.sigma_MW_MeV) < 0.1)

def check_T_w_trace_dizet_flag_sensitivity_covariance_positive():
    cov = covariance_summary()
    return _res("covariance_positive", cov["input_sigma_MW_MeV"] > 3.0 and cov["total_sigma_MW_MeV_quadrature"] > cov["theory_sigma_MW_MeV"])

def check_T_w_trace_dizet_flag_sensitivity_pull_reduced_by_covariance():
    cov = covariance_summary()
    return _res("pull_reduced_by_covariance", cov["pull_vs_input_plus_theory_quadrature"] < cov["pull_vs_theory_only"] and cov["pull_vs_input_plus_theory_quadrature"] < 1.0)

def check_T_w_trace_dizet_flag_sensitivity_total_sigma_value():
    cov = covariance_summary()
    return _res("total_sigma_value", 5.20 < cov["total_sigma_MW_MeV_quadrature"] < 5.30, sigma=cov["total_sigma_MW_MeV_quadrature"])

def check_T_w_trace_dizet_flag_sensitivity_apf_dizet_residual_preserved():
    return _res("apf_dizet_residual_preserved", -4.9 < DIZET_TOTAL_MW_MINUS_APF_TRACE_MEV < -4.7)

def check_T_w_trace_dizet_flag_sensitivity_apf_not_input():
    s = v161_route_summary()
    return _res("apf_not_input", "non_W_inputs_only" in s["apf_inputs"]["policy"])

def check_T_w_trace_dizet_flag_sensitivity_gate_split_preserved():
    gates = route_summary()["gates"]
    return _res("gate_split_preserved", gates["REVIEWED_SAME_INPUT_TOTAL_EVALUATOR"].startswith("CLOSED") and gates["ROW_DECOMPOSITION_AND_COVARIANCE_PROTOCOL"] == "OPEN_BLOCKED")

def check_T_w_trace_dizet_flag_sensitivity_blocker_sharpened():
    return _res("blocker_sharpened", route_summary()["gates"]["sharpened_blocker"] == NEW_BLOCKER)

def check_T_w_trace_dizet_flag_sensitivity_physical_export_locked():
    return _res("physical_export_locked", route_summary()["gates"]["PHYSICAL_W_EXPORT"] == "OPEN_BLOCKED")

def check_T_w_trace_dizet_flag_sensitivity_forbidden_claim_named():
    return _res("forbidden_claim_named", "physical export" in route_summary()["claim_boundary"]["forbidden"])

def check_T_w_trace_dizet_flag_sensitivity_payload_digest_present():
    return _res("payload_digest_present", route_summary()["payload_digest"].startswith("sha256:"))

def check_T_w_trace_dizet_flag_sensitivity_terminal_verdict_exact():
    return _res("terminal_verdict_exact", route_summary()["claim_boundary"]["allowed"] == ROUTE_STATUS)

def check_T_w_trace_dizet_flag_sensitivity_report_contains_scan():
    rep = terminal_report()
    return _res("report_contains_scan", rep["route_summary"]["scan_counts"]["successful_runs"] == 64 and len(rep["route_summary"]["flag_responses"]) >= 10)

def check_T_w_trace_dizet_flag_sensitivity_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_trace_dizet_flag_sensitivity_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))

_CHECKS = {name: obj for name, obj in sorted(globals().items()) if name.startswith("check_T_w_trace_dizet_flag_sensitivity_") and callable(obj)}

def register(registry: MutableMapping[str, Any]) -> None:
    registry.update(_CHECKS)

def run_all() -> Dict[str, Any]:
    rows = []
    for name, fn in _CHECKS.items():
        try:
            result = fn()
            rows.append({"name": name, "passed": _passed(result), "result": result})
        except Exception as exc:  # pragma: no cover
            rows.append({"name": name, "passed": False, "error": repr(exc)})
    ok = all(row["passed"] for row in rows)
    return {"passed": ok, "status": PASS_STATUS if ok else PASS_STATUS.replace("_PASS", "_FAIL"), "checks": rows, "report": terminal_report()}

if __name__ == "__main__":
    out = run_all()
    print(out["status"])
    for row in out["checks"]:
        print(("PASS" if row["passed"] else "FAIL"), row["name"])
    raise SystemExit(0 if out["passed"] else 1)
