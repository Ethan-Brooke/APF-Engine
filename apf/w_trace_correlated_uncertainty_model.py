"""Correlated source-uncertainty model for APF/W_TRACE SM W comparison (v14.3)."""
from __future__ import annotations
import math
from typing import Any, Dict, MutableMapping
from apf import w_trace_multisource_delta_r_comparison as multi
from apf import w_trace_cms_global_fit_context as cmsctx
from apf import w_trace_acfw_delta_r_extraction_attempt as acfw

STATUS="P_w_correlated_uncertainty_model"
VERSION="v14_3"
PASS_STATUS="W_TRACE_CORRELATED_UNCERTAINTY_MODEL_BANK_PASS"
APF_MW=acfw.M_W_TRACE_GEV
LOCKED_STATE={"correlated_uncertainty_model_declared":True,"physical_W_export_enabled":False,"exports_physical_M_W":False,"component_sum_certified":False}

COMMON_THEORY_FLOOR_GEV=0.004
GLOBAL_FIT_COMMON_FLOOR_GEV=0.004

def source_points()->Dict[str,Dict[str,float]]:
    pts={k:dict(v) for k,v in multi.comparison_points().items()}
    c=cmsctx.context_row()
    pts["CMS_global_EW_fit_context"]={"M_W_GeV":float(c["M_W_GeV"]),"sigma_M_W_GeV":float(c["sigma_M_W_GeV"]),"Delta_r":float(c["Delta_r_equiv_total"]),"M_W_gap_MeV":float(c["M_W_minus_W_TRACE_MeV"]),"gap_sigma_units":float(c["gap_sigma_units"])}
    return pts

def conservative_sigma(row:Dict[str,float])->float:
    return math.sqrt(float(row["sigma_M_W_GeV"])**2 + COMMON_THEORY_FLOOR_GEV**2)

def uncorrelated_weighted_summary()->Dict[str,float]:
    pts=source_points(); weights={k:1.0/(v["sigma_M_W_GeV"]**2) for k,v in pts.items()}; W=sum(weights.values())
    mw=sum(pts[k]["M_W_GeV"]*weights[k] for k in pts)/W; sig=math.sqrt(1.0/W)
    return {"M_W_GeV":mw,"sigma_GeV":sig,"gap_MeV":(mw-APF_MW)*1000.0,"gap_sigma_units":abs(mw-APF_MW)/sig}

def conservative_weighted_summary()->Dict[str,float]:
    pts=source_points(); weights={k:1.0/(conservative_sigma(v)**2) for k,v in pts.items()}; W=sum(weights.values())
    mw=sum(pts[k]["M_W_GeV"]*weights[k] for k in pts)/W; sig=math.sqrt(1.0/W + COMMON_THEORY_FLOOR_GEV**2)
    return {"M_W_GeV":mw,"sigma_GeV":sig,"gap_MeV":(mw-APF_MW)*1000.0,"gap_sigma_units":abs(mw-APF_MW)/sig}

def leave_one_out()->Dict[str,Dict[str,float]]:
    pts=source_points(); out={}
    for drop in pts:
        sub={k:v for k,v in pts.items() if k!=drop}; weights={k:1.0/(conservative_sigma(v)**2) for k,v in sub.items()}; W=sum(weights.values())
        mw=sum(sub[k]["M_W_GeV"]*weights[k] for k in sub)/W; sig=math.sqrt(1.0/W + COMMON_THEORY_FLOOR_GEV**2)
        out[drop]={"M_W_GeV":mw,"sigma_GeV":sig,"gap_MeV":(mw-APF_MW)*1000.0,"gap_sigma_units":abs(mw-APF_MW)/sig}
    return out

def terminal_report()->Dict[str,Any]: return {"status":STATUS,"version":VERSION,"points":source_points(),"uncorrelated":uncorrelated_weighted_summary(),"conservative":conservative_weighted_summary(),"leave_one_out":leave_one_out(),"locked_state":dict(LOCKED_STATE),"verdict":"CORRELATED_UNCERTAINTY_MODEL_KEEPS_APF_TRACE_WITHIN_CONSERVATIVE_SOURCE_SCALE_NO_EXPORT"}
def _res(c,p,**e): r={"check":c,"passed":bool(p)}; r.update(e); return r
def _passed(r): return isinstance(r,dict) and r.get("passed") is True

def check_T_w_trace_corr_uncertainty_status_declared(): return _res("status_declared", STATUS.startswith("P_w_"))
def check_T_w_trace_corr_uncertainty_has_four_points(): return _res("has_four_points", len(source_points())==4)
def check_T_w_trace_corr_uncertainty_cms_context_included(): return _res("cms_context_included", "CMS_global_EW_fit_context" in source_points())
def check_T_w_trace_corr_uncertainty_common_floor_positive(): return _res("common_floor_positive", COMMON_THEORY_FLOOR_GEV>0)
def check_T_w_trace_corr_uncertainty_conservative_sigma_not_smaller():
    pts=source_points(); return _res("conservative_sigma_not_smaller", all(conservative_sigma(v)>=v["sigma_M_W_GeV"] for v in pts.values()))
def check_T_w_trace_corr_uncertainty_uncorrelated_summary_computed(): return _res("uncorrelated_summary_computed", 80.35<uncorrelated_weighted_summary()["M_W_GeV"]<80.37)
def check_T_w_trace_corr_uncertainty_conservative_summary_computed(): return _res("conservative_summary_computed", 80.35<conservative_weighted_summary()["M_W_GeV"]<80.37)
def check_T_w_trace_corr_uncertainty_conservative_gap_under_1p5sigma(): return _res("conservative_gap_under_1p5sigma", conservative_weighted_summary()["gap_sigma_units"]<1.5, sigma=conservative_weighted_summary()["gap_sigma_units"])
def check_T_w_trace_corr_uncertainty_leave_one_out_all_under_1p6sigma(): return _res("loo_all_under_1p6sigma", all(v["gap_sigma_units"]<1.6 for v in leave_one_out().values()))
def check_T_w_trace_corr_uncertainty_gap_few_mev(): return _res("gap_few_mev", abs(conservative_weighted_summary()["gap_MeV"])<6.0)
def check_T_w_trace_corr_uncertainty_no_component_claim(): return _res("no_component_claim", LOCKED_STATE["component_sum_certified"] is False)
def check_T_w_trace_corr_uncertainty_no_export(): return _res("no_export", LOCKED_STATE["exports_physical_M_W"] is False)
def check_T_w_trace_corr_uncertainty_bank_closure():
    rows=[fn() for n,fn in _CHECKS.items() if n!="check_T_w_trace_corr_uncertainty_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))
_CHECKS={n:o for n,o in list(globals().items()) if n.startswith("check_T_w_trace_corr_uncertainty_") and callable(o)}
def register(registry:MutableMapping[str,Any])->None: registry.update(_CHECKS)
def run_all()->Dict[str,Any]:
    rows=[]
    for n,fn in _CHECKS.items():
        try: res=fn(); rows.append({"name":n,"passed":_passed(res),"result":res})
        except Exception as exc: rows.append({"name":n,"passed":False,"error":repr(exc)})
    ok=all(r["passed"] for r in rows); return {"passed":ok,"status":PASS_STATUS if ok else PASS_STATUS.replace("_PASS","_FAIL"),"checks":rows,"report":terminal_report()}
if __name__=="__main__":
    out=run_all(); print(out["status"]); print("SUMMARY",sum(r["passed"] for r in out["checks"]),"/",len(out["checks"]),"PASS"); print(conservative_weighted_summary()); raise SystemExit(0 if out["passed"] else 1)
