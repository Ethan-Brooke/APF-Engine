
"""W_TRACE input-convention stress test for the first real Delta_r payloads (v14.2).

This module stress-tests the v14.1 ACFW extraction against nearby independent
Standard Model W-mass prediction conventions.  It does not export a physical W
mass.  It converts source-predicted M_W values into an on-shell-equivalent total
Delta_r for comparison with the APF/W_TRACE anchor.
"""
from __future__ import annotations
import json, math
from typing import Any, Dict, Mapping, MutableMapping
from apf import w_trace_acfw_delta_r_extraction_attempt as acfw

STATUS = "P_w_input_convention_stress_test"
VERSION = "v14_2"
PASS_STATUS = "W_TRACE_INPUT_CONVENTION_STRESS_TEST_BANK_PASS"
APF_DELTA_R_TARGET = acfw.APF_DELTA_R_TARGET
M_W_TRACE_GEV = acfw.M_W_TRACE_GEV
BASE_INPUTS = dict(acfw.EXTRACTION_INPUTS)

SOURCE_POINTS = {
    "ACFW_v14_1": {
        "source_class": "on_shell_precision_parametrization",
        "M_W_GeV": acfw.extraction_payload()["M_W_source_GeV"],
        "sigma_M_W_GeV": 0.004,
        "source_note": "ACFW residual theory uncertainty scale for light Higgs region; comparison-only.",
    },
    "DGG_2015_MSbar_prediction": {
        "source_class": "MSbar_two_loop_cross_scheme_prediction",
        "M_W_GeV": 80.357,
        "sigma_M_W_GeV": math.sqrt(0.009**2 + 0.003**2),
        "source_note": "Degrassi-Gambino-Giardino prediction mW=80.357 +/-0.009 +/-0.003 GeV; cross-scheme equivalent Delta_r only.",
    },
    "GFitter_2012_global_fit_prediction": {
        "source_class": "global_SM_fit_prediction",
        "M_W_GeV": 80.359,
        "sigma_M_W_GeV": 0.011,
        "source_note": "GFitter post-Higgs global-fit SM prediction M_W=80.359 +/-0.011 GeV; comparison-only.",
    },
}

FORBIDDEN_TOKENS = (
    "observed_M_W", "M_W_world_average", "CDF_II_M_W", "fit_to_W_TRACE",
    "Delta_r_target_backsolve", "APF_anchor_as_input", "manual_export_override",
    "physical_export_request",
)
LOCKED_STATE = {
    "real_standard_delta_r_payload_candidates_stress_tested": True,
    "component_sum_certified": False,
    "covariance_certified": False,
    "uncertainty_propagation_certified": False,
    "physical_W_export_enabled": False,
    "exports_physical_M_W": False,
}

def _json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def contains_forbidden_token(obj: Any) -> bool:
    text = _json(obj)
    return any(tok in text for tok in FORBIDDEN_TOKENS)

def delta_r_from_mw(mw: float, inputs: Mapping[str, float] = BASE_INPUTS) -> float:
    return acfw.invert_delta_r_from_mw(mw, inputs)

def source_rows() -> Dict[str, Dict[str, float | str]]:
    out: Dict[str, Dict[str, float | str]] = {}
    for name, row in SOURCE_POINTS.items():
        mw = float(row["M_W_GeV"])
        sig = float(row["sigma_M_W_GeV"])
        dr = delta_r_from_mw(mw)
        gap_mev = (mw - M_W_TRACE_GEV) * 1000.0
        out[name] = dict(row)
        out[name].update({
            "Delta_r_equiv_total": dr,
            "Delta_r_minus_APF": dr - APF_DELTA_R_TARGET,
            "M_W_minus_W_TRACE_MeV": gap_mev,
            "abs_M_W_gap_MeV": abs(gap_mev),
            "gap_sigma_units": abs(mw - M_W_TRACE_GEV) / sig if sig > 0 else math.inf,
        })
    return out

def convention_sensitivity() -> Dict[str, float]:
    # Numerical derivatives around the APF/W_TRACE anchor; comparison only.
    base = delta_r_from_mw(M_W_TRACE_GEV)
    d_mw = (delta_r_from_mw(M_W_TRACE_GEV + 0.001) - delta_r_from_mw(M_W_TRACE_GEV - 0.001)) / 0.002
    hi = dict(BASE_INPUTS); lo = dict(BASE_INPUTS)
    hi["M_Z_GeV"] += 0.001; lo["M_Z_GeV"] -= 0.001
    d_mz = (delta_r_from_mw(M_W_TRACE_GEV, hi) - delta_r_from_mw(M_W_TRACE_GEV, lo)) / 0.002
    hi = dict(BASE_INPUTS); lo = dict(BASE_INPUTS)
    hi["alpha_inverse_for_inversion"] += 1e-6; lo["alpha_inverse_for_inversion"] -= 1e-6
    d_ainv = (delta_r_from_mw(M_W_TRACE_GEV, hi) - delta_r_from_mw(M_W_TRACE_GEV, lo)) / 2e-6
    return {"base_delta_r": base, "dDelta_r_dM_W_GeV": d_mw, "dDelta_r_dM_Z_GeV": d_mz, "dDelta_r_dalpha_inverse": d_ainv}

def terminal_report() -> Dict[str, Any]:
    rows = source_rows()
    return {"status": STATUS, "version": VERSION, "rows": rows, "sensitivity": convention_sensitivity(), "locked_state": dict(LOCKED_STATE), "verdict": "SOURCE_CONVENTIONS_STRESS_TESTED_APF_WITHIN_FEW_MEV_SM_SOURCE_ENVELOPE_NO_EXPORT"}

def _res(check: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    row = {"check": check, "passed": bool(passed)}; row.update(extra); return row

def _passed(row: Any) -> bool:
    return isinstance(row, dict) and row.get("passed") is True

def check_T_w_trace_input_convention_status_declared(): return _res("status_declared", STATUS.startswith("P_w_"))
def check_T_w_trace_input_convention_has_three_sources(): return _res("has_three_sources", len(SOURCE_POINTS) == 3)
def check_T_w_trace_input_convention_acfw_is_carried_forward(): return _res("acfw_carried_forward", "ACFW_v14_1" in SOURCE_POINTS)
def check_T_w_trace_input_convention_cross_scheme_is_labeled(): return _res("cross_scheme_labeled", SOURCE_POINTS["DGG_2015_MSbar_prediction"]["source_class"].startswith("MSbar"))
def check_T_w_trace_input_convention_global_fit_is_labeled(): return _res("global_fit_labeled", SOURCE_POINTS["GFitter_2012_global_fit_prediction"]["source_class"].startswith("global"))
def check_T_w_trace_input_convention_delta_r_all_reasonable():
    rows=source_rows(); return _res("delta_r_all_reasonable", all(0.035 < float(r["Delta_r_equiv_total"]) < 0.038 for r in rows.values()))
def check_T_w_trace_input_convention_gaps_few_mev():
    rows=source_rows(); return _res("gaps_few_mev", all(float(r["abs_M_W_gap_MeV"]) < 6.0 for r in rows.values()))
def check_T_w_trace_input_convention_gaps_within_declared_uncertainties():
    rows=source_rows(); return _res("gaps_within_declared_uncertainties", all(float(r["gap_sigma_units"]) < 1.2 for r in rows.values()), max_sigma=max(float(r["gap_sigma_units"]) for r in rows.values()))
def check_T_w_trace_input_convention_sensitivity_nonzero():
    s=convention_sensitivity(); return _res("sensitivity_nonzero", abs(s["dDelta_r_dM_W_GeV"]) > 0 and abs(s["dDelta_r_dM_Z_GeV"]) > 0)
def check_T_w_trace_input_convention_forbidden_scan_clean(): return _res("forbidden_scan_clean", not contains_forbidden_token({"sources": SOURCE_POINTS, "inputs": BASE_INPUTS}))
def check_T_w_trace_input_convention_detects_bad_token(): return _res("detects_bad_token", contains_forbidden_token({"bad":"observed_M_W"}))
def check_T_w_trace_input_convention_no_export(): return _res("no_export", LOCKED_STATE["exports_physical_M_W"] is False)
def check_T_w_trace_input_convention_bank_closure():
    rows=[fn() for n,fn in _CHECKS.items() if n!="check_T_w_trace_input_convention_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))

_CHECKS = {name: obj for name, obj in list(globals().items()) if name.startswith("check_T_w_trace_input_convention_") and callable(obj)}

def register(registry: MutableMapping[str, Any]) -> None: registry.update(_CHECKS)
def run_all() -> Dict[str, Any]:
    rows=[]
    for name,fn in _CHECKS.items():
        try: res=fn(); rows.append({"name":name,"passed":_passed(res),"result":res})
        except Exception as exc: rows.append({"name":name,"passed":False,"error":repr(exc)})
    ok=all(r["passed"] for r in rows)
    return {"passed":ok,"status":PASS_STATUS if ok else PASS_STATUS.replace("_PASS","_FAIL"),"checks":rows,"report":terminal_report()}
if __name__ == "__main__":
    out=run_all(); print(out["status"]); print("SUMMARY", sum(r["passed"] for r in out["checks"]), "/", len(out["checks"]), "PASS")
    for k,v in terminal_report()["rows"].items(): print(k, v["M_W_GeV"], v["Delta_r_equiv_total"], v["abs_M_W_gap_MeV"], v["gap_sigma_units"])
    raise SystemExit(0 if out["passed"] else 1)
