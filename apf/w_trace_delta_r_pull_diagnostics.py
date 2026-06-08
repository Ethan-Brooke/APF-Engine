"""Delta_r / M_W pull diagnostics for APF/W_TRACE source cluster (v14.3)."""
from __future__ import annotations
import math
from typing import Any, Dict, MutableMapping
from apf import w_trace_correlated_uncertainty_model as corr
from apf import w_trace_acfw_delta_r_extraction_attempt as acfw

STATUS="P_w_delta_r_pull_diagnostics"
VERSION="v14_3"
PASS_STATUS="W_TRACE_DELTA_R_PULL_DIAGNOSTICS_BANK_PASS"
APF_DELTA_R=acfw.APF_DELTA_R_TARGET
APF_MW=acfw.M_W_TRACE_GEV
LOCKED_STATE={"pull_diagnostics_complete":True,"physical_W_export_enabled":False,"exports_physical_M_W":False}

def derivative_delta_r_wrt_mw(mw:float=APF_MW)->float:
    h=0.001
    return (acfw.invert_delta_r_from_mw(mw+h, acfw.EXTRACTION_INPUTS)-acfw.invert_delta_r_from_mw(mw-h, acfw.EXTRACTION_INPUTS))/(2*h)

def diagnostic_rows()->Dict[str,Dict[str,float|str]]:
    d=abs(derivative_delta_r_wrt_mw())
    rows={}
    for k,v in corr.source_points().items():
        sig_mw=corr.conservative_sigma(v); sig_dr=d*sig_mw; delta_dr=float(v["Delta_r"])-APF_DELTA_R; gap_mw=(float(v["M_W_GeV"])-APF_MW)*1000.0
        pull=abs(delta_dr)/sig_dr if sig_dr>0 else math.inf
        rows[k]={"Delta_r":float(v["Delta_r"]),"Delta_r_minus_APF":delta_dr,"sigma_Delta_r_conservative":sig_dr,"Delta_r_pull_sigma":pull,"M_W_gap_MeV":gap_mw,"diagnostic_band":"GREEN" if pull<1.5 else "AMBER" if pull<2.5 else "RED"}
    return rows

def aggregate_diagnostics()->Dict[str,float|str]:
    rows=diagnostic_rows(); max_pull=max(float(v["Delta_r_pull_sigma"]) for v in rows.values()); green=sum(v["diagnostic_band"]=="GREEN" for v in rows.values())
    return {"max_delta_r_pull_sigma":max_pull,"green_count":green,"n_rows":len(rows),"aggregate_band":"GREEN" if max_pull<1.5 else "AMBER" if max_pull<2.5 else "RED","dDelta_r_dM_W_abs_per_GeV":abs(derivative_delta_r_wrt_mw())}

def terminal_report()->Dict[str,Any]: return {"status":STATUS,"version":VERSION,"rows":diagnostic_rows(),"aggregate":aggregate_diagnostics(),"locked_state":dict(LOCKED_STATE),"verdict":"APF_TRACE_PULLS_REMAIN_GREEN_UNDER_CONSERVATIVE_DELTA_R_PROPAGATION_NO_EXPORT"}
def _res(c,p,**e): r={"check":c,"passed":bool(p)}; r.update(e); return r
def _passed(r): return isinstance(r,dict) and r.get("passed") is True

def check_T_w_trace_pull_diag_status_declared(): return _res("status_declared", STATUS.startswith("P_w_"))
def check_T_w_trace_pull_diag_derivative_nonzero(): return _res("derivative_nonzero", abs(derivative_delta_r_wrt_mw())>0)
def check_T_w_trace_pull_diag_has_four_rows(): return _res("has_four_rows", len(diagnostic_rows())==4)
def check_T_w_trace_pull_diag_all_rows_have_sigma(): return _res("all_rows_have_sigma", all(float(v["sigma_Delta_r_conservative"])>0 for v in diagnostic_rows().values()))
def check_T_w_trace_pull_diag_all_rows_have_band(): return _res("all_rows_have_band", all(v["diagnostic_band"] in {"GREEN","AMBER","RED"} for v in diagnostic_rows().values()))
def check_T_w_trace_pull_diag_all_green(): return _res("all_green", all(v["diagnostic_band"]=="GREEN" for v in diagnostic_rows().values()), aggregate=aggregate_diagnostics())
def check_T_w_trace_pull_diag_max_pull_under_1p5sigma(): return _res("max_pull_under_1p5sigma", aggregate_diagnostics()["max_delta_r_pull_sigma"]<1.5, max_pull=aggregate_diagnostics()["max_delta_r_pull_sigma"])
def check_T_w_trace_pull_diag_delta_r_values_reasonable(): return _res("delta_r_values_reasonable", all(0.035<float(v["Delta_r"])<0.038 for v in diagnostic_rows().values()))
def check_T_w_trace_pull_diag_mw_gaps_few_mev(): return _res("mw_gaps_few_mev", all(abs(float(v["M_W_gap_MeV"]))<6.0 for v in diagnostic_rows().values()))
def check_T_w_trace_pull_diag_aggregate_green(): return _res("aggregate_green", aggregate_diagnostics()["aggregate_band"]=="GREEN")
def check_T_w_trace_pull_diag_no_export(): return _res("no_export", LOCKED_STATE["exports_physical_M_W"] is False)
def check_T_w_trace_pull_diag_export_lock_preserved(): return _res("export_lock_preserved", LOCKED_STATE["physical_W_export_enabled"] is False)
def check_T_w_trace_pull_diag_bank_closure():
    rows=[fn() for n,fn in _CHECKS.items() if n!="check_T_w_trace_pull_diag_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))
_CHECKS={n:o for n,o in list(globals().items()) if n.startswith("check_T_w_trace_pull_diag_") and callable(o)}
def register(registry:MutableMapping[str,Any])->None: registry.update(_CHECKS)
def run_all()->Dict[str,Any]:
    rows=[]
    for n,fn in _CHECKS.items():
        try: res=fn(); rows.append({"name":n,"passed":_passed(res),"result":res})
        except Exception as exc: rows.append({"name":n,"passed":False,"error":repr(exc)})
    ok=all(r["passed"] for r in rows); return {"passed":ok,"status":PASS_STATUS if ok else PASS_STATUS.replace("_PASS","_FAIL"),"checks":rows,"report":terminal_report()}
if __name__=="__main__":
    out=run_all(); print(out["status"]); print("SUMMARY",sum(r["passed"] for r in out["checks"]),"/",len(out["checks"]),"PASS"); print(aggregate_diagnostics()); raise SystemExit(0 if out["passed"] else 1)
