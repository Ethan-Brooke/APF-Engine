"""CMS/global-fit W prediction context for APF/W_TRACE (v14.3).

This module adds the modern CMS-era electroweak-fit context as a comparison
source class.  It is *not* an observed-W input.  It records the SM/global-fit
prediction quoted in the CMS public result context as a standard-MW prediction
context and converts it to an on-shell-equivalent total Delta_r for comparison
with the APF/W_TRACE anchor.
"""
from __future__ import annotations
import json, math
from typing import Any, Dict, MutableMapping
from apf import w_trace_acfw_delta_r_extraction_attempt as acfw

STATUS="P_w_cms_global_fit_context"
VERSION="v14_3"
PASS_STATUS="W_TRACE_CMS_GLOBAL_FIT_CONTEXT_BANK_PASS"
APF_MW=acfw.M_W_TRACE_GEV
APF_DELTA_R=acfw.APF_DELTA_R_TARGET
INPUTS=dict(acfw.EXTRACTION_INPUTS)

CMS_GLOBAL_FIT_CONTEXT={
    "source_id":"CMS_SMP_23_002_public_context_global_EW_fit_prediction",
    "source_kind":"standard_model_global_fit_prediction_context_not_observed_W",
    "M_W_GeV":80.357,
    "sigma_M_W_GeV":0.006,
    "published_context":"CMS 2024/2026 public result context quotes global electroweak-fit SM prediction scale 80.357 +/- 0.006 GeV.",
    "consumes_observed_W_mass":False,
    "consumes_cms_measured_W_mass":False,
    "consumes_APF_TRACE_W_mass":False,
    "uses_APF_delta_r_target":False,
    "exports_physical_M_W":False,
}
FORBIDDEN=("observed_M_W","CMS_measured_M_W_as_input","M_W_world_average","CDF_II_M_W","APF_anchor_as_input","Delta_r_target_backsolve","physical_export_request")
LOCKED_STATE={"cms_global_fit_context_added":True,"cms_measurement_used_as_source_input":False,"physical_W_export_enabled":False,"exports_physical_M_W":False}

def _json(o:Any)->str: return json.dumps(o,sort_keys=True,separators=(",",":"),ensure_ascii=True)
def contains_forbidden_token(o:Any)->bool: return any(t in _json(o) for t in FORBIDDEN)
def delta_r_equiv()->float: return acfw.invert_delta_r_from_mw(float(CMS_GLOBAL_FIT_CONTEXT["M_W_GeV"]), INPUTS)
def context_row()->Dict[str,Any]:
    mw=float(CMS_GLOBAL_FIT_CONTEXT["M_W_GeV"]); sig=float(CMS_GLOBAL_FIT_CONTEXT["sigma_M_W_GeV"]); dr=delta_r_equiv(); gap=(mw-APF_MW)*1000.0
    row=dict(CMS_GLOBAL_FIT_CONTEXT); row.update({"Delta_r_equiv_total":dr,"Delta_r_minus_APF":dr-APF_DELTA_R,"M_W_minus_W_TRACE_MeV":gap,"abs_M_W_gap_MeV":abs(gap),"gap_sigma_units":abs(mw-APF_MW)/sig})
    return row

def terminal_report()->Dict[str,Any]: return {"status":STATUS,"version":VERSION,"context_row":context_row(),"locked_state":dict(LOCKED_STATE),"verdict":"CMS_GLOBAL_FIT_CONTEXT_ADDED_AS_PREDICTION_CONTEXT_ONLY_NO_OBSERVED_W_INPUT_NO_EXPORT"}
def _res(c,p,**e): r={"check":c,"passed":bool(p)}; r.update(e); return r
def _passed(r): return isinstance(r,dict) and r.get("passed") is True

def check_T_w_trace_cms_context_status_declared(): return _res("status_declared", STATUS.startswith("P_w_"))
def check_T_w_trace_cms_context_kind_is_prediction_not_measurement(): return _res("kind_prediction_not_measurement", "prediction" in CMS_GLOBAL_FIT_CONTEXT["source_kind"] and "not_observed" in CMS_GLOBAL_FIT_CONTEXT["source_kind"])
def check_T_w_trace_cms_context_mw_value_reasonable(): return _res("mw_value_reasonable", 80.34 < CMS_GLOBAL_FIT_CONTEXT["M_W_GeV"] < 80.38)
def check_T_w_trace_cms_context_sigma_value_reasonable(): return _res("sigma_value_reasonable", 0.003 <= CMS_GLOBAL_FIT_CONTEXT["sigma_M_W_GeV"] <= 0.012)
def check_T_w_trace_cms_context_delta_r_inverted(): return _res("delta_r_inverted", 0.035 < delta_r_equiv() < 0.038, delta_r=delta_r_equiv())
def check_T_w_trace_cms_context_gap_few_mev(): return _res("gap_few_mev", context_row()["abs_M_W_gap_MeV"] < 6.0, gap=context_row()["abs_M_W_gap_MeV"])
def check_T_w_trace_cms_context_gap_within_prediction_uncertainty(): return _res("gap_within_prediction_uncertainty", context_row()["gap_sigma_units"] < 1.0, sigma=context_row()["gap_sigma_units"])
def check_T_w_trace_cms_context_declares_no_cms_measurement_input(): return _res("no_cms_measurement_input", CMS_GLOBAL_FIT_CONTEXT["consumes_cms_measured_W_mass"] is False)
def check_T_w_trace_cms_context_declares_no_apf_input(): return _res("no_apf_input", CMS_GLOBAL_FIT_CONTEXT["consumes_APF_TRACE_W_mass"] is False and CMS_GLOBAL_FIT_CONTEXT["uses_APF_delta_r_target"] is False)
def check_T_w_trace_cms_context_forbidden_scan_clean(): return _res("forbidden_scan_clean", not contains_forbidden_token({"context":CMS_GLOBAL_FIT_CONTEXT,"inputs":INPUTS}))
def check_T_w_trace_cms_context_detects_bad_token(): return _res("detects_bad_token", contains_forbidden_token({"bad":"observed_M_W"}))
def check_T_w_trace_cms_context_no_export(): return _res("no_export", LOCKED_STATE["exports_physical_M_W"] is False)
def check_T_w_trace_cms_context_bank_closure():
    rows=[fn() for n,fn in _CHECKS.items() if n!="check_T_w_trace_cms_context_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))
_CHECKS={n:o for n,o in list(globals().items()) if n.startswith("check_T_w_trace_cms_context_") and callable(o)}
def register(registry:MutableMapping[str,Any])->None: registry.update(_CHECKS)
def run_all()->Dict[str,Any]:
    rows=[]
    for n,fn in _CHECKS.items():
        try: res=fn(); rows.append({"name":n,"passed":_passed(res),"result":res})
        except Exception as exc: rows.append({"name":n,"passed":False,"error":repr(exc)})
    ok=all(r["passed"] for r in rows); return {"passed":ok,"status":PASS_STATUS if ok else PASS_STATUS.replace("_PASS","_FAIL"),"checks":rows,"report":terminal_report()}
if __name__=="__main__":
    out=run_all(); print(out["status"]); print("SUMMARY",sum(r["passed"] for r in out["checks"]),"/",len(out["checks"]),"PASS"); print(context_row()); raise SystemExit(0 if out["passed"] else 1)
