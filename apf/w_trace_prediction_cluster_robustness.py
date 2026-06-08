"""Robustness diagnostics for W_TRACE Standard-Model prediction cluster (v14.4)."""
from __future__ import annotations
import itertools, math
from typing import Any, Dict, MutableMapping, List
from apf import w_trace_correlated_uncertainty_model as corr
from apf import w_trace_acfw_delta_r_extraction_attempt as acfw
STATUS="P_w_prediction_cluster_robustness"; VERSION="v14_4"; PASS_STATUS="W_TRACE_PREDICTION_CLUSTER_ROBUSTNESS_BANK_PASS"
APF_MW=acfw.M_W_TRACE_GEV; LOCKED_STATE={"cluster_robustness_complete":True,"physical_W_export_enabled":False,"exports_physical_M_W":False}
def points(): return corr.source_points()
def weighted(sub:Dict[str,Dict[str,float]], floor:float)->Dict[str,float]:
    weights={k:1.0/(math.sqrt(v["sigma_M_W_GeV"]**2+floor**2)**2) for k,v in sub.items()}; W=sum(weights.values())
    mw=sum(sub[k]["M_W_GeV"]*weights[k] for k in sub)/W; sig=math.sqrt(1.0/W + floor**2)
    return {"M_W_GeV":mw,"sigma_GeV":sig,"gap_MeV":(mw-APF_MW)*1000.0,"pull_sigma":abs(mw-APF_MW)/sig}
def floor_scan()->Dict[str,Dict[str,float]]: return {f"floor_{int(f*1000)}MeV":weighted(points(),f) for f in (0.0,0.002,0.004,0.006,0.008)}
def subset_scan()->Dict[str,Dict[str,float]]:
    pts=points(); out={}
    for r in range(2,len(pts)+1):
        for keys in itertools.combinations(pts.keys(),r): out["+".join(keys)]=weighted({k:pts[k] for k in keys},0.004)
    return out
def robustness_summary()->Dict[str,Any]:
    fs=floor_scan(); ss=subset_scan(); pulls=[v["pull_sigma"] for v in ss.values()] + [v["pull_sigma"] for v in fs.values()]
    gaps=[abs(v["gap_MeV"]) for v in ss.values()] + [abs(v["gap_MeV"]) for v in fs.values()]
    return {"floor_scan":fs,"subset_count":len(ss),"max_pull_sigma":max(pulls),"max_gap_MeV":max(gaps),"min_gap_MeV":min(gaps),"band":"GREEN" if max(pulls)<1.6 and max(gaps)<6.0 else "AMBER"}
def terminal_report()->Dict[str,Any]: return {"status":STATUS,"version":VERSION,"summary":robustness_summary(),"locked_state":dict(LOCKED_STATE),"verdict":"CLUSTER_ROBUST_TO_SOURCE_FLOORS_AND_SUBSETS_NO_EXPORT"}
def _res(c,p,**e): r={"check":c,"passed":bool(p)}; r.update(e); return r
def _passed(r): return isinstance(r,dict) and r.get("passed") is True
def check_T_w_trace_cluster_robust_status_declared(): return _res("status_declared", STATUS.startswith("P_w_"))
def check_T_w_trace_cluster_robust_four_points(): return _res("four_points", len(points())==4)
def check_T_w_trace_cluster_robust_floor_scan_has_five(): return _res("floor_scan_has_five", len(floor_scan())==5)
def check_T_w_trace_cluster_robust_subset_scan_nonempty(): return _res("subset_scan_nonempty", robustness_summary()["subset_count"]>=10)
def check_T_w_trace_cluster_robust_max_pull_under_1p6(): return _res("max_pull_under_1p6", robustness_summary()["max_pull_sigma"]<1.6, max_pull=robustness_summary()["max_pull_sigma"])
def check_T_w_trace_cluster_robust_max_gap_under_6MeV(): return _res("max_gap_under_6MeV", robustness_summary()["max_gap_MeV"]<6.0, max_gap=robustness_summary()["max_gap_MeV"])
def check_T_w_trace_cluster_robust_floor_zero_computed(): return _res("floor_zero_computed", "floor_0MeV" in floor_scan())
def check_T_w_trace_cluster_robust_floor_8_computed(): return _res("floor_8_computed", "floor_8MeV" in floor_scan())
def check_T_w_trace_cluster_robust_band_green(): return _res("band_green", robustness_summary()["band"]=="GREEN")
def check_T_w_trace_cluster_robust_apf_above_cluster(): return _res("apf_above_cluster", all(v["gap_MeV"]<0 for v in floor_scan().values()))
def check_T_w_trace_cluster_robust_no_export(): return _res("no_export", LOCKED_STATE["exports_physical_M_W"] is False)
def check_T_w_trace_cluster_robust_export_lock_preserved(): return _res("export_lock_preserved", LOCKED_STATE["physical_W_export_enabled"] is False)
def check_T_w_trace_cluster_robust_bank_closure():
    rows=[fn() for n,fn in _CHECKS.items() if n!="check_T_w_trace_cluster_robust_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))
_CHECKS={n:o for n,o in list(globals().items()) if n.startswith("check_T_w_trace_cluster_robust_") and callable(o)}
def register(registry:MutableMapping[str,Any])->None: registry.update(_CHECKS)
def run_all()->Dict[str,Any]:
    rows=[]
    for n,fn in _CHECKS.items():
        try: res=fn(); rows.append({"name":n,"passed":_passed(res),"result":res})
        except Exception as exc: rows.append({"name":n,"passed":False,"error":repr(exc)})
    ok=all(r["passed"] for r in rows); return {"passed":ok,"status":PASS_STATUS if ok else PASS_STATUS.replace("_PASS","_FAIL"),"checks":rows,"report":terminal_report()}
if __name__=="__main__":
    out=run_all(); print(out["status"]); print("SUMMARY",sum(r["passed"] for r in out["checks"]),"/",len(out["checks"]),"PASS"); print(robustness_summary()); raise SystemExit(0 if out["passed"] else 1)
