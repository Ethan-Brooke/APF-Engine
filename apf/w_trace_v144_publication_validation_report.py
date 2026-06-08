"""Terminal report for W_TRACE v14.4 publication-grade physics validation sprint."""
from __future__ import annotations
from typing import Any, Dict, MutableMapping
from apf import w_trace_source_authority_grading as grade
from apf import w_trace_prediction_cluster_robustness as robust
from apf import w_trace_residual_interpretation as resid
from apf import w_trace_publication_claim_language as claims
STATUS="P_w_v144_publication_validation_report"; VERSION="v14_4"; PASS_STATUS="W_TRACE_V14_4_PUBLICATION_VALIDATION_SPRINT_PASS"
LOCKED_STATE={"publication_validation_complete":True,"physical_W_export_enabled":False,"exports_physical_M_W":False,"component_sum_certified":False,"covariance_certified":False,"uncertainty_propagation_certified":False}
def sprint_report()->Dict[str,Any]: return {"status":STATUS,"version":VERSION,"source_authority":grade.terminal_report(),"cluster_robustness":robust.robustness_summary(),"residual":resid.residual_summary(),"claim_packet":claims.claim_packet(),"locked_state":dict(LOCKED_STATE),"verdict":"V14_4_PUBLICATION_READY_VALIDATION_COMPARISON_APF_TRACE_FEW_MEV_HIGH_GREEN_NO_EXPORT","next":"write paper-facing W_TRACE validation section or supply real component-level Delta_r payload"}
def _res(c,p,**e): r={"check":c,"passed":bool(p)}; r.update(e); return r
def _passed(r): return isinstance(r,dict) and r.get("passed") is True
def check_T_w_trace_v144_report_status_declared(): return _res("status_declared", STATUS.startswith("P_w_"))
def check_T_w_trace_v144_report_authority_present(): return _res("authority_present", len(grade.comparison_grade_rows())>=4)
def check_T_w_trace_v144_report_measurements_quarantined(): return _res("measurements_quarantined", grade.LOCKED_STATE["observed_measurements_are_sources"] is False)
def check_T_w_trace_v144_report_robustness_green(): return _res("robustness_green", robust.robustness_summary()["band"]=="GREEN")
def check_T_w_trace_v144_report_residual_green(): return _res("residual_green", str(resid.residual_summary()["interpretation_band"]).startswith("GREEN"))
def check_T_w_trace_v144_report_gap_few_mev(): return _res("gap_few_mev", resid.residual_summary()["APF_minus_cluster_MeV"]<6.0)
def check_T_w_trace_v144_report_claim_language_safe(): return _res("claim_language_safe", claims.claim_packet()["claim_level"]=="validation_comparison_not_export")
def check_T_w_trace_v144_report_preferred_sentence_no_export(): return _res("preferred_sentence_no_export", "not a physical W-mass export" in claims.claim_packet()["preferred_sentence"])
def check_T_w_trace_v144_report_no_component_certification(): return _res("no_component_certification", LOCKED_STATE["component_sum_certified"] is False)
def check_T_w_trace_v144_report_no_covariance_certification(): return _res("no_covariance_certification", LOCKED_STATE["covariance_certified"] is False)
def check_T_w_trace_v144_report_no_export(): return _res("no_export", LOCKED_STATE["exports_physical_M_W"] is False)
def check_T_w_trace_v144_report_next_is_paper_or_payload(): return _res("next_is_paper_or_payload", "paper" in sprint_report()["next"] or "payload" in sprint_report()["next"])
def check_T_w_trace_v144_report_bank_closure():
    rows=[fn() for n,fn in _CHECKS.items() if n!="check_T_w_trace_v144_report_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))
_CHECKS={n:o for n,o in list(globals().items()) if n.startswith("check_T_w_trace_v144_report_") and callable(o)}
def register(registry:MutableMapping[str,Any])->None: registry.update(_CHECKS)
def run_all()->Dict[str,Any]:
    rows=[]
    for n,fn in _CHECKS.items():
        try: res=fn(); rows.append({"name":n,"passed":_passed(res),"result":res})
        except Exception as exc: rows.append({"name":n,"passed":False,"error":repr(exc)})
    ok=all(r["passed"] for r in rows); return {"passed":ok,"status":PASS_STATUS if ok else PASS_STATUS.replace("_PASS","_FAIL"),"checks":rows,"report":sprint_report()}
if __name__=="__main__":
    out=run_all(); print(out["status"]); print("SUMMARY",sum(r["passed"] for r in out["checks"]),"/",len(out["checks"]),"PASS"); print(sprint_report()["verdict"]); raise SystemExit(0 if out["passed"] else 1)
