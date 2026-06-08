"""Observed W-mass measurement quarantine/context layer for APF/W_TRACE (v14.3).

Observed measurements are useful context, but forbidden as inputs to the APF/W_TRACE
standard-Delta-r source comparison.  This module records CMS/CDF/context rows only
inside a quarantine namespace and proves they cannot feed source extraction or export.
"""
from __future__ import annotations
import json, math
from typing import Any, Dict, MutableMapping
from apf import w_trace_acfw_delta_r_extraction_attempt as acfw

STATUS="P_w_measurement_quarantine_context"
VERSION="v14_3"
PASS_STATUS="W_TRACE_MEASUREMENT_QUARANTINE_CONTEXT_BANK_PASS"
APF_MW=acfw.M_W_TRACE_GEV
MEASUREMENT_CONTEXT={
    "CMS_2024_LHC_measurement":{"kind":"observed_measurement_context_only","M_W_GeV":80.3602,"sigma_M_W_GeV":0.0099,"admissible_as_source_input":False},
    "CDF_II_2022_measurement":{"kind":"observed_measurement_context_only_outlier","M_W_GeV":80.4335,"sigma_M_W_GeV":0.0094,"admissible_as_source_input":False},
}
FORBIDDEN_INPUT_FIELDS=("admissible_as_source_input",)
LOCKED_STATE={"measurements_quarantined":True,"measurement_rows_feed_delta_r_source":False,"physical_W_export_enabled":False,"exports_physical_M_W":False}

def measurement_rows()->Dict[str,Dict[str,float|str|bool]]:
    out={}
    for k,v in MEASUREMENT_CONTEXT.items():
        mw=float(v["M_W_GeV"]); sig=float(v["sigma_M_W_GeV"]); gap=(mw-APF_MW)*1000.0
        row=dict(v); row.update({"M_W_minus_W_TRACE_MeV":gap,"abs_M_W_gap_MeV":abs(gap),"gap_sigma_units":abs(mw-APF_MW)/sig})
        out[k]=row
    return out

def context_summary()->Dict[str,Any]:
    rows=measurement_rows(); return {"n_measurements":len(rows),"cms_gap_MeV":rows["CMS_2024_LHC_measurement"]["M_W_minus_W_TRACE_MeV"],"cdf_gap_MeV":rows["CDF_II_2022_measurement"]["M_W_minus_W_TRACE_MeV"],"quarantine_verdict":"OBSERVED_MEASUREMENTS_CONTEXT_ONLY_NOT_SOURCE_INPUTS"}

def terminal_report()->Dict[str,Any]: return {"status":STATUS,"version":VERSION,"rows":measurement_rows(),"summary":context_summary(),"locked_state":dict(LOCKED_STATE)}
def _res(c,p,**e): r={"check":c,"passed":bool(p)}; r.update(e); return r
def _passed(r): return isinstance(r,dict) and r.get("passed") is True

def check_T_w_trace_measurement_quarantine_status_declared(): return _res("status_declared", STATUS.startswith("P_w_"))
def check_T_w_trace_measurement_quarantine_has_cms_context(): return _res("has_cms_context", "CMS_2024_LHC_measurement" in MEASUREMENT_CONTEXT)
def check_T_w_trace_measurement_quarantine_has_cdf_outlier_context(): return _res("has_cdf_outlier_context", "CDF_II_2022_measurement" in MEASUREMENT_CONTEXT)
def check_T_w_trace_measurement_quarantine_all_rows_context_only(): return _res("all_rows_context_only", all("context_only" in v["kind"] for v in MEASUREMENT_CONTEXT.values()))
def check_T_w_trace_measurement_quarantine_all_rows_not_admissible_as_source(): return _res("not_admissible_as_source", all(v["admissible_as_source_input"] is False for v in MEASUREMENT_CONTEXT.values()))
def check_T_w_trace_measurement_quarantine_cms_near_trace_context(): return _res("cms_near_trace_context", abs(measurement_rows()["CMS_2024_LHC_measurement"]["M_W_minus_W_TRACE_MeV"]) < 3.0)
def check_T_w_trace_measurement_quarantine_cdf_is_outlier_context(): return _res("cdf_outlier_context", measurement_rows()["CDF_II_2022_measurement"]["M_W_minus_W_TRACE_MeV"] > 50.0)
def check_T_w_trace_measurement_quarantine_no_delta_r_extraction_from_measurements(): return _res("no_delta_r_extraction", LOCKED_STATE["measurement_rows_feed_delta_r_source"] is False)
def check_T_w_trace_measurement_quarantine_no_export(): return _res("no_export", LOCKED_STATE["exports_physical_M_W"] is False)
def check_T_w_trace_measurement_quarantine_context_summary_present(): return _res("context_summary_present", context_summary()["n_measurements"]==2)
def check_T_w_trace_measurement_quarantine_cms_not_used_to_tune_apf(): return _res("cms_not_used_to_tune_apf", MEASUREMENT_CONTEXT["CMS_2024_LHC_measurement"]["admissible_as_source_input"] is False)
def check_T_w_trace_measurement_quarantine_cdf_not_used_to_tune_apf(): return _res("cdf_not_used_to_tune_apf", MEASUREMENT_CONTEXT["CDF_II_2022_measurement"]["admissible_as_source_input"] is False)
def check_T_w_trace_measurement_quarantine_bank_closure():
    rows=[fn() for n,fn in _CHECKS.items() if n!="check_T_w_trace_measurement_quarantine_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))
_CHECKS={n:o for n,o in list(globals().items()) if n.startswith("check_T_w_trace_measurement_quarantine_") and callable(o)}
def register(registry:MutableMapping[str,Any])->None: registry.update(_CHECKS)
def run_all()->Dict[str,Any]:
    rows=[]
    for n,fn in _CHECKS.items():
        try: res=fn(); rows.append({"name":n,"passed":_passed(res),"result":res})
        except Exception as exc: rows.append({"name":n,"passed":False,"error":repr(exc)})
    ok=all(r["passed"] for r in rows); return {"passed":ok,"status":PASS_STATUS if ok else PASS_STATUS.replace("_PASS","_FAIL"),"checks":rows,"report":terminal_report()}
if __name__=="__main__":
    out=run_all(); print(out["status"]); print("SUMMARY",sum(r["passed"] for r in out["checks"]),"/",len(out["checks"]),"PASS"); print(context_summary()); raise SystemExit(0 if out["passed"] else 1)
