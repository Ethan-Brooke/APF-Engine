"""Source authority grading for W_TRACE Standard-Model prediction sources (v14.4)."""
from __future__ import annotations
from typing import Any, Dict, MutableMapping
from apf import w_trace_correlated_uncertainty_model as corr
STATUS="P_w_source_authority_grading"; VERSION="v14_4"; PASS_STATUS="W_TRACE_SOURCE_AUTHORITY_GRADING_BANK_PASS"
LOCKED_STATE={"source_authority_grading_complete":True,"observed_measurements_are_sources":False,"physical_W_export_enabled":False,"exports_physical_M_W":False}
GRADE_ROWS={
"ACFW_precision_MW_parametrization":{"class":"primary_SM_prediction_parametrization","grade":"A","role":"prediction_source","payload_kind":"standard_delta_r_parametrization","admissible_for_comparison":True},
"DGG_2015_MSbar_cross_scheme_prediction":{"class":"peer_reviewed_cross_scheme_prediction","grade":"A-","role":"prediction_source","payload_kind":"standard_delta_r_total","admissible_for_comparison":True},
"GFitter_2012_post_Higgs_global_fit":{"class":"global_electroweak_fit_prediction","grade":"B+","role":"prediction_context","payload_kind":"standard_delta_r_total","admissible_for_comparison":True},
"CMS_global_EW_fit_context":{"class":"modern_global_fit_context","grade":"B+","role":"prediction_context","payload_kind":"standard_delta_r_total","admissible_for_comparison":True},
"CMS_2024_LHC_measurement":{"class":"observed_measurement","grade":"Q","role":"quarantined_context","payload_kind":"none","admissible_for_comparison":False},
"CDF_II_2022_measurement":{"class":"observed_measurement_outlier","grade":"Q","role":"quarantined_context","payload_kind":"none","admissible_for_comparison":False},
}
def authority_rows()->Dict[str,Dict[str,Any]]: return {k:dict(v) for k,v in GRADE_ROWS.items()}
def comparison_grade_rows()->Dict[str,Dict[str,Any]]: return {k:v for k,v in authority_rows().items() if v["admissible_for_comparison"]}
def terminal_report()->Dict[str,Any]: return {"status":STATUS,"version":VERSION,"rows":authority_rows(),"comparison_rows":comparison_grade_rows(),"locked_state":dict(LOCKED_STATE),"verdict":"PREDICTION_SOURCES_GRADED_AND_MEASUREMENTS_QUARANTINED_NO_EXPORT"}
def _res(c,p,**e): r={"check":c,"passed":bool(p)}; r.update(e); return r
def _passed(r): return isinstance(r,dict) and r.get("passed") is True
def check_T_w_trace_source_authority_status_declared(): return _res("status_declared", STATUS.startswith("P_w_"))
def check_T_w_trace_source_authority_has_prediction_sources(): return _res("has_prediction_sources", len(comparison_grade_rows())>=4)
def check_T_w_trace_source_authority_acfw_grade_A(): return _res("acfw_grade_A", authority_rows()["ACFW_precision_MW_parametrization"]["grade"]=="A")
def check_T_w_trace_source_authority_dgg_cross_scheme(): return _res("dgg_cross_scheme", "cross_scheme" in authority_rows()["DGG_2015_MSbar_cross_scheme_prediction"]["class"])
def check_T_w_trace_source_authority_gfitter_context_not_measurement(): return _res("gfitter_context_not_measurement", authority_rows()["GFitter_2012_post_Higgs_global_fit"]["role"]=="prediction_context")
def check_T_w_trace_source_authority_cms_global_fit_admissible(): return _res("cms_global_fit_admissible", authority_rows()["CMS_global_EW_fit_context"]["admissible_for_comparison"] is True)
def check_T_w_trace_source_authority_cms_measurement_quarantined(): return _res("cms_measurement_quarantined", authority_rows()["CMS_2024_LHC_measurement"]["admissible_for_comparison"] is False)
def check_T_w_trace_source_authority_cdf_measurement_quarantined(): return _res("cdf_measurement_quarantined", authority_rows()["CDF_II_2022_measurement"]["role"]=="quarantined_context")
def check_T_w_trace_source_authority_all_comparison_have_payload_kind(): return _res("comparison_have_payload_kind", all(v["payload_kind"].startswith("standard_delta_r") for v in comparison_grade_rows().values()))
def check_T_w_trace_source_authority_no_measurements_as_sources(): return _res("no_measurements_as_sources", LOCKED_STATE["observed_measurements_are_sources"] is False)
def check_T_w_trace_source_authority_matches_corr_points(): return _res("matches_corr_points", len(corr.source_points())==len(comparison_grade_rows()))
def check_T_w_trace_source_authority_no_export(): return _res("no_export", LOCKED_STATE["exports_physical_M_W"] is False)
def check_T_w_trace_source_authority_bank_closure():
    rows=[fn() for n,fn in _CHECKS.items() if n!="check_T_w_trace_source_authority_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))
_CHECKS={n:o for n,o in list(globals().items()) if n.startswith("check_T_w_trace_source_authority_") and callable(o)}
def register(registry:MutableMapping[str,Any])->None: registry.update(_CHECKS)
def run_all()->Dict[str,Any]:
    rows=[]
    for n,fn in _CHECKS.items():
        try: res=fn(); rows.append({"name":n,"passed":_passed(res),"result":res})
        except Exception as exc: rows.append({"name":n,"passed":False,"error":repr(exc)})
    ok=all(r["passed"] for r in rows); return {"passed":ok,"status":PASS_STATUS if ok else PASS_STATUS.replace("_PASS","_FAIL"),"checks":rows,"report":terminal_report()}
if __name__=="__main__":
    out=run_all(); print(out["status"]); print("SUMMARY",sum(r["passed"] for r in out["checks"]),"/",len(out["checks"]),"PASS"); print(terminal_report()["verdict"]); raise SystemExit(0 if out["passed"] else 1)
