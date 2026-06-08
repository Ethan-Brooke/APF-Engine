
"""Multi-source Delta_r comparison harness for APF/W_TRACE (v14.2)."""
from __future__ import annotations
import math
from typing import Any, Dict, MutableMapping
from apf import w_trace_input_convention_stress_test as stress
from apf import w_trace_acfw_delta_r_extraction_attempt as acfw

STATUS="P_w_multisource_delta_r_comparison"
VERSION="v14_2"
PASS_STATUS="W_TRACE_MULTISOURCE_DELTA_R_COMPARISON_BANK_PASS"
APF_MW=acfw.M_W_TRACE_GEV
APF_DELTA_R=acfw.APF_DELTA_R_TARGET
LOCKED_STATE={"multisource_comparison_complete":True,"physical_W_export_enabled":False,"exports_physical_M_W":False,"component_sum_certified":False,"covariance_certified":False}

def comparison_points() -> Dict[str, Dict[str, float]]:
    rows=stress.source_rows()
    return {k:{"M_W_GeV":float(v["M_W_GeV"]),"sigma_M_W_GeV":float(v["sigma_M_W_GeV"]),"Delta_r":float(v["Delta_r_equiv_total"]),"M_W_gap_MeV":float(v["M_W_minus_W_TRACE_MeV"]),"gap_sigma_units":float(v["gap_sigma_units"])} for k,v in rows.items()}

def weighted_summary() -> Dict[str, float]:
    pts=comparison_points(); weights={k:1.0/(v["sigma_M_W_GeV"]**2) for k,v in pts.items()}
    W=sum(weights.values())
    mw_mean=sum(pts[k]["M_W_GeV"]*weights[k] for k in pts)/W
    mw_sigma=math.sqrt(1.0/W)
    dr_mean=acfw.invert_delta_r_from_mw(mw_mean, acfw.EXTRACTION_INPUTS)
    return {"weighted_M_W_GeV":mw_mean,"weighted_sigma_GeV":mw_sigma,"weighted_M_W_minus_W_TRACE_MeV":(mw_mean-APF_MW)*1000.0,"weighted_gap_sigma_units":abs(mw_mean-APF_MW)/mw_sigma,"weighted_Delta_r_equiv":dr_mean,"weighted_Delta_r_minus_APF":dr_mean-APF_DELTA_R}

def envelope_summary() -> Dict[str, float]:
    pts=comparison_points(); mws=[v["M_W_GeV"] for v in pts.values()]
    return {"min_source_M_W_GeV":min(mws),"max_source_M_W_GeV":max(mws),"APF_M_W_TRACE_GeV":APF_MW,"APF_above_source_max_MeV":(APF_MW-max(mws))*1000.0,"source_spread_MeV":(max(mws)-min(mws))*1000.0}

def terminal_report() -> Dict[str, Any]: return {"status":STATUS,"version":VERSION,"points":comparison_points(),"weighted":weighted_summary(),"envelope":envelope_summary(),"locked_state":dict(LOCKED_STATE),"verdict":"APF_TRACE_W_IS_A_FEW_MEV_HIGH_RELATIVE_TO_INDEPENDENT_SM_PREDICTION_CLUSTER_BUT_WITHIN_DECLARED_SOURCE_THEORY_PARAMETRIC_SCALES_NO_EXPORT"}
def _res(c,p,**e): r={"check":c,"passed":bool(p)}; r.update(e); return r
def _passed(r): return isinstance(r,dict) and r.get("passed") is True

def check_T_w_trace_multisource_status_declared(): return _res("status_declared", STATUS.startswith("P_w_"))
def check_T_w_trace_multisource_has_three_points(): return _res("has_three_points", len(comparison_points())==3)
def check_T_w_trace_multisource_all_points_few_mev(): return _res("all_points_few_mev", all(abs(v["M_W_gap_MeV"])<6.0 for v in comparison_points().values()))
def check_T_w_trace_multisource_all_points_within_1p2sigma(): return _res("all_points_within_1p2sigma", all(v["gap_sigma_units"]<1.2 for v in comparison_points().values()))
def check_T_w_trace_multisource_weighted_mean_computed(): return _res("weighted_mean_computed", 80.35 < weighted_summary()["weighted_M_W_GeV"] < 80.37)
def check_T_w_trace_multisource_weighted_gap_small(): return _res("weighted_gap_small", abs(weighted_summary()["weighted_M_W_minus_W_TRACE_MeV"]) < 5.0)
def check_T_w_trace_multisource_weighted_gap_near_one_sigma(): return _res("weighted_gap_near_one_sigma", weighted_summary()["weighted_gap_sigma_units"] < 1.2, sigma=weighted_summary()["weighted_gap_sigma_units"])
def check_T_w_trace_multisource_delta_r_weighted_reasonable(): return _res("weighted_delta_r_reasonable", 0.035 < weighted_summary()["weighted_Delta_r_equiv"] < 0.038)
def check_T_w_trace_multisource_apf_above_source_cluster(): return _res("apf_above_source_cluster", envelope_summary()["APF_above_source_max_MeV"] > 0)
def check_T_w_trace_multisource_source_spread_small(): return _res("source_spread_small", envelope_summary()["source_spread_MeV"] < 3.0)
def check_T_w_trace_multisource_no_export(): return _res("no_export", LOCKED_STATE["exports_physical_M_W"] is False)
def check_T_w_trace_multisource_no_component_claim(): return _res("no_component_claim", LOCKED_STATE["component_sum_certified"] is False)
def check_T_w_trace_multisource_no_covariance_claim(): return _res("no_covariance_claim", LOCKED_STATE["covariance_certified"] is False)
def check_T_w_trace_multisource_verdict_is_not_export(): return _res("verdict_is_not_export", "NO_EXPORT" in terminal_report()["verdict"])
def check_T_w_trace_multisource_bank_closure():
    rows=[fn() for n,fn in _CHECKS.items() if n!="check_T_w_trace_multisource_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))
_CHECKS={n:o for n,o in list(globals().items()) if n.startswith("check_T_w_trace_multisource_") and callable(o)}
def register(registry: MutableMapping[str, Any]) -> None: registry.update(_CHECKS)
def run_all() -> Dict[str, Any]:
    rows=[]
    for n,fn in _CHECKS.items():
        try: res=fn(); rows.append({"name":n,"passed":_passed(res),"result":res})
        except Exception as exc: rows.append({"name":n,"passed":False,"error":repr(exc)})
    ok=all(r["passed"] for r in rows); return {"passed":ok,"status":PASS_STATUS if ok else PASS_STATUS.replace("_PASS","_FAIL"),"checks":rows,"report":terminal_report()}
if __name__=="__main__":
    out=run_all(); print(out["status"]); print("SUMMARY",sum(r["passed"] for r in out["checks"]),"/",len(out["checks"]),"PASS"); print(weighted_summary()); raise SystemExit(0 if out["passed"] else 1)
