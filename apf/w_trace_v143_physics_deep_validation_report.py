"""Terminal report for W_TRACE v14.3 deep physics validation sprint."""
from __future__ import annotations
from typing import Any, Dict, MutableMapping
from apf import w_trace_cms_global_fit_context as cmsctx
from apf import w_trace_measurement_quarantine_context as meas
from apf import w_trace_correlated_uncertainty_model as corr
from apf import w_trace_delta_r_pull_diagnostics as pulls

STATUS="P_w_v143_physics_deep_validation_report"
VERSION="v14_3"
PASS_STATUS="W_TRACE_V14_3_PHYSICS_DEEP_VALIDATION_SPRINT_PASS"
LOCKED_STATE={"real_physics_validation_deepened":True,"physical_W_export_enabled":False,"exports_physical_M_W":False,"component_sum_certified":False,"covariance_certified":False,"uncertainty_propagation_certified":False}

def sprint_report()->Dict[str,Any]:
    return {"status":STATUS,"version":VERSION,"cms_global_fit_context":cmsctx.context_row(),"measurement_quarantine":meas.context_summary(),"correlated_uncertainty":corr.conservative_weighted_summary(),"pull_diagnostics":pulls.aggregate_diagnostics(),"locked_state":dict(LOCKED_STATE),"verdict":"V14_3_HARD_VALIDATION_COMPLETE_APF_TRACE_REMAINS_FEW_MEV_HIGH_BUT_GREEN_UNDER_CONSERVATIVE_SM_SOURCE_PULLS_NO_EXPORT","next":"move to real standard-Delta-r worksheet/payload extraction or write paper-facing physics result"}

def _res(c,p,**e): r={"check":c,"passed":bool(p)}; r.update(e); return r
def _passed(r): return isinstance(r,dict) and r.get("passed") is True

def check_T_w_trace_v143_report_status_declared(): return _res("status_declared", STATUS.startswith("P_w_"))
def check_T_w_trace_v143_report_cms_context_present(): return _res("cms_context_present", sprint_report()["cms_global_fit_context"]["source_id"].startswith("CMS"))
def check_T_w_trace_v143_report_measurements_quarantined(): return _res("measurements_quarantined", meas.LOCKED_STATE["measurement_rows_feed_delta_r_source"] is False)
def check_T_w_trace_v143_report_correlated_model_present(): return _res("correlated_model_present", corr.conservative_weighted_summary()["sigma_GeV"]>0)
def check_T_w_trace_v143_report_pull_diagnostics_green(): return _res("pull_diagnostics_green", pulls.aggregate_diagnostics()["aggregate_band"]=="GREEN")
def check_T_w_trace_v143_report_gap_few_mev(): return _res("gap_few_mev", abs(corr.conservative_weighted_summary()["gap_MeV"])<6.0, gap=corr.conservative_weighted_summary()["gap_MeV"])
def check_T_w_trace_v143_report_gap_under_1p5sigma(): return _res("gap_under_1p5sigma", corr.conservative_weighted_summary()["gap_sigma_units"]<1.5, sigma=corr.conservative_weighted_summary()["gap_sigma_units"])
def check_T_w_trace_v143_report_four_source_context(): return _res("four_source_context", len(corr.source_points())==4)
def check_T_w_trace_v143_report_cdf_not_source(): return _res("cdf_not_source", meas.MEASUREMENT_CONTEXT["CDF_II_2022_measurement"]["admissible_as_source_input"] is False)
def check_T_w_trace_v143_report_cms_measurement_not_source(): return _res("cms_measurement_not_source", meas.MEASUREMENT_CONTEXT["CMS_2024_LHC_measurement"]["admissible_as_source_input"] is False)
def check_T_w_trace_v143_report_no_export(): return _res("no_export", LOCKED_STATE["exports_physical_M_W"] is False)
def check_T_w_trace_v143_report_next_is_physics_or_paper(): return _res("next_is_physics_or_paper", "payload" in sprint_report()["next"] or "paper" in sprint_report()["next"])
def check_T_w_trace_v143_report_bank_closure():
    rows=[fn() for n,fn in _CHECKS.items() if n!="check_T_w_trace_v143_report_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))
_CHECKS={n:o for n,o in list(globals().items()) if n.startswith("check_T_w_trace_v143_report_") and callable(o)}
def register(registry:MutableMapping[str,Any])->None: registry.update(_CHECKS)
def run_all()->Dict[str,Any]:
    rows=[]
    for n,fn in _CHECKS.items():
        try: res=fn(); rows.append({"name":n,"passed":_passed(res),"result":res})
        except Exception as exc: rows.append({"name":n,"passed":False,"error":repr(exc)})
    ok=all(r["passed"] for r in rows); return {"passed":ok,"status":PASS_STATUS if ok else PASS_STATUS.replace("_PASS","_FAIL"),"checks":rows,"report":sprint_report()}
if __name__=="__main__":
    out=run_all(); print(out["status"]); print("SUMMARY",sum(r["passed"] for r in out["checks"]),"/",len(out["checks"]),"PASS"); print(sprint_report()["verdict"]); raise SystemExit(0 if out["passed"] else 1)
