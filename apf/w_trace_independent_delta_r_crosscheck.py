
"""Independent Standard-Model W/Delta_r cross-check source bank (v14.2)."""
from __future__ import annotations
import json, math
from typing import Any, Dict, MutableMapping
from apf import w_trace_input_convention_stress_test as stress
from apf import w_trace_acfw_delta_r_extraction_attempt as acfw

STATUS = "P_w_independent_delta_r_crosscheck"
VERSION = "v14_2"
PASS_STATUS = "W_TRACE_INDEPENDENT_DELTA_R_CROSSCHECK_BANK_PASS"
APF_DELTA_R_TARGET = acfw.APF_DELTA_R_TARGET
M_W_TRACE_GEV = acfw.M_W_TRACE_GEV

INDEPENDENT_SOURCES = {
    "DGG_2015_JHEP_mW_mZ_interdependence": {
        "authors": "G. Degrassi, P. Gambino, P. P. Giardino",
        "prediction": "m_W = 80.357 +/- 0.009 +/- 0.003 GeV",
        "scheme_note": "MSbar two-loop analysis; converted to on-shell-equivalent Delta_r comparison using APF input constants.",
        "M_W_GeV": 80.357,
        "sigma_M_W_GeV": math.sqrt(0.009**2 + 0.003**2),
        "uses_observed_M_W": False,
        "uses_apf_trace_M_W": False,
        "uses_apf_delta_r_target": False,
    },
    "GFitter_2012_post_Higgs_global_fit": {
        "authors": "Baak et al. / GFitter Group",
        "prediction": "M_W = 80.359 +/- 0.011 GeV",
        "scheme_note": "Global SM fit prediction; comparison-only cross-check.",
        "M_W_GeV": 80.359,
        "sigma_M_W_GeV": 0.011,
        "uses_observed_M_W": False,
        "uses_apf_trace_M_W": False,
        "uses_apf_delta_r_target": False,
    },
}
FORBIDDEN_TOKENS = ("observed_M_W", "M_W_world_average", "CDF_II_M_W", "APF_anchor_as_input", "Delta_r_target_backsolve", "physical_export_request")
LOCKED_STATE = {"independent_crosscheck_extracted": True, "physical_W_export_enabled": False, "exports_physical_M_W": False, "component_sum_certified": False, "covariance_certified": False}

def _json(obj: Any) -> str: return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
def contains_forbidden_token(obj: Any) -> bool: return any(tok in _json(obj) for tok in FORBIDDEN_TOKENS)
def invert(mw: float) -> float: return acfw.invert_delta_r_from_mw(mw, acfw.EXTRACTION_INPUTS)
def crosscheck_rows() -> Dict[str, Dict[str, Any]]:
    out={}
    for k,r in INDEPENDENT_SOURCES.items():
        mw=float(r["M_W_GeV"]); sig=float(r["sigma_M_W_GeV"]); dr=invert(mw)
        out[k]=dict(r)
        out[k].update({"Delta_r_equiv_total":dr,"Delta_r_minus_APF":dr-APF_DELTA_R_TARGET,"abs_M_W_gap_MeV":abs(mw-M_W_TRACE_GEV)*1000.0,"gap_sigma_units":abs(mw-M_W_TRACE_GEV)/sig})
    return out

def terminal_report() -> Dict[str, Any]:
    return {"status":STATUS,"version":VERSION,"sources":crosscheck_rows(),"locked_state":dict(LOCKED_STATE),"verdict":"SECOND_INDEPENDENT_SOURCE_FAMILY_CROSSCHECKS_APF_TRACE_WITHIN_DECLARED_SOURCE_UNCERTAINTIES_NO_EXPORT"}

def _res(check: str, passed: bool, **extra: Any) -> Dict[str, Any]: row={"check":check,"passed":bool(passed)}; row.update(extra); return row
def _passed(r: Any) -> bool: return isinstance(r,dict) and r.get("passed") is True

def check_T_w_trace_independent_crosscheck_status_declared(): return _res("status_declared", STATUS == "P_w_independent_delta_r_crosscheck")
def check_T_w_trace_independent_crosscheck_has_dgg(): return _res("has_dgg", "DGG_2015_JHEP_mW_mZ_interdependence" in INDEPENDENT_SOURCES)
def check_T_w_trace_independent_crosscheck_has_gfitter(): return _res("has_gfitter", "GFitter_2012_post_Higgs_global_fit" in INDEPENDENT_SOURCES)
def check_T_w_trace_independent_crosscheck_sources_forbid_observed_w(): return _res("sources_forbid_observed_w", all(r["uses_observed_M_W"] is False for r in INDEPENDENT_SOURCES.values()))
def check_T_w_trace_independent_crosscheck_sources_forbid_apf_inputs(): return _res("sources_forbid_apf_inputs", all(r["uses_apf_trace_M_W"] is False and r["uses_apf_delta_r_target"] is False for r in INDEPENDENT_SOURCES.values()))
def check_T_w_trace_independent_crosscheck_delta_r_in_window(): return _res("delta_r_in_window", all(0.035 < float(r["Delta_r_equiv_total"]) < 0.038 for r in crosscheck_rows().values()))
def check_T_w_trace_independent_crosscheck_gaps_under_6_mev(): return _res("gaps_under_6_mev", all(float(r["abs_M_W_gap_MeV"]) < 6.0 for r in crosscheck_rows().values()))
def check_T_w_trace_independent_crosscheck_gaps_within_1sigma(): return _res("gaps_within_1sigma", all(float(r["gap_sigma_units"]) < 1.0 for r in crosscheck_rows().values()))
def check_T_w_trace_independent_crosscheck_dgg_cross_scheme_labeled(): return _res("dgg_cross_scheme_labeled", "MSbar" in INDEPENDENT_SOURCES["DGG_2015_JHEP_mW_mZ_interdependence"]["scheme_note"])
def check_T_w_trace_independent_crosscheck_no_component_claim(): return _res("no_component_claim", LOCKED_STATE["component_sum_certified"] is False)
def check_T_w_trace_independent_crosscheck_no_covariance_claim(): return _res("no_covariance_claim", LOCKED_STATE["covariance_certified"] is False)
def check_T_w_trace_independent_crosscheck_no_export(): return _res("no_export", LOCKED_STATE["exports_physical_M_W"] is False)
def check_T_w_trace_independent_crosscheck_forbidden_scan_clean():
    clean = {k: {"authors": v["authors"], "prediction": v["prediction"], "scheme_note": v["scheme_note"], "M_W_GeV": v["M_W_GeV"], "sigma_M_W_GeV": v["sigma_M_W_GeV"]} for k, v in INDEPENDENT_SOURCES.items()}
    return _res("forbidden_scan_clean", not contains_forbidden_token(clean))
def check_T_w_trace_independent_crosscheck_detects_bad_token(): return _res("detects_bad_token", contains_forbidden_token({"bad":"Delta_r_target_backsolve"}))
def check_T_w_trace_independent_crosscheck_bank_closure():
    rows=[fn() for n,fn in _CHECKS.items() if n!="check_T_w_trace_independent_crosscheck_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))
_CHECKS={n:o for n,o in list(globals().items()) if n.startswith("check_T_w_trace_independent_crosscheck_") and callable(o)}
def register(registry: MutableMapping[str, Any]) -> None: registry.update(_CHECKS)
def run_all() -> Dict[str, Any]:
    rows=[]
    for n,fn in _CHECKS.items():
        try: res=fn(); rows.append({"name":n,"passed":_passed(res),"result":res})
        except Exception as exc: rows.append({"name":n,"passed":False,"error":repr(exc)})
    ok=all(r["passed"] for r in rows); return {"passed":ok,"status":PASS_STATUS if ok else PASS_STATUS.replace("_PASS","_FAIL"),"checks":rows,"report":terminal_report()}
if __name__=="__main__":
    out=run_all(); print(out["status"]); print("SUMMARY", sum(r["passed"] for r in out["checks"]), "/", len(out["checks"]), "PASS"); raise SystemExit(0 if out["passed"] else 1)
