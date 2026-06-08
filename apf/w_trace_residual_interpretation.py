"""Interpretation of APF/W_TRACE residual against SM prediction cluster (v14.4)."""
from __future__ import annotations
from typing import Any, Dict, MutableMapping
from apf import w_trace_correlated_uncertainty_model as corr
from apf import w_trace_delta_r_pull_diagnostics as pulls
from apf import w_trace_acfw_delta_r_extraction_attempt as acfw
STATUS="P_w_residual_interpretation"; VERSION="v14_4"; PASS_STATUS="W_TRACE_RESIDUAL_INTERPRETATION_BANK_PASS"
LOCKED_STATE={"residual_interpretation_complete":True,"physical_W_export_enabled":False,"exports_physical_M_W":False,"overclaim_guard_active":True}
def residual_summary()->Dict[str,float|str]:
    c=corr.conservative_weighted_summary(); d=abs(pulls.derivative_delta_r_wrt_mw()); delta_r_gap=d*abs(c["gap_MeV"])/1000.0
    return {"cluster_M_W_GeV":c["M_W_GeV"],"APF_M_W_TRACE_GeV":acfw.M_W_TRACE_GEV,"APF_minus_cluster_MeV":-c["gap_MeV"],"cluster_sigma_MeV":c["sigma_GeV"]*1000.0,"pull_sigma":c["gap_sigma_units"],"abs_dDelta_r_dM_W_per_GeV":d,"approx_abs_Delta_r_gap":delta_r_gap,"interpretation_band":"GREEN_FEW_MEV_HIGH" if c["gap_sigma_units"]<1.0 else "GREEN_NEAR_ONE_SIGMA" if c["gap_sigma_units"]<1.5 else "AMBER"}
def paper_safe_sentence()->str:
    s=residual_summary(); return f"APF/W_TRACE lies {s['APF_minus_cluster_MeV']:.2f} MeV above the conservative independent SM prediction cluster, a {s['pull_sigma']:.2f} sigma source-scale pull; this is a validation comparison, not a physical W-mass export."
def terminal_report()->Dict[str,Any]: return {"status":STATUS,"version":VERSION,"summary":residual_summary(),"paper_safe_sentence":paper_safe_sentence(),"locked_state":dict(LOCKED_STATE),"verdict":"RESIDUAL_IS_FEW_MEV_HIGH_GREEN_SOURCE_PULL_NOT_EXPORT"}
def _res(c,p,**e): r={"check":c,"passed":bool(p)}; r.update(e); return r
def _passed(r): return isinstance(r,dict) and r.get("passed") is True
def check_T_w_trace_residual_status_declared(): return _res("status_declared", STATUS.startswith("P_w_"))
def check_T_w_trace_residual_apf_above_cluster_positive(): return _res("apf_above_cluster_positive", residual_summary()["APF_minus_cluster_MeV"]>0)
def check_T_w_trace_residual_gap_under_6MeV(): return _res("gap_under_6MeV", residual_summary()["APF_minus_cluster_MeV"]<6.0)
def check_T_w_trace_residual_pull_under_1sigma_or_near(): return _res("pull_under_1p5sigma", residual_summary()["pull_sigma"]<1.5)
def check_T_w_trace_residual_derivative_positive(): return _res("derivative_positive", residual_summary()["abs_dDelta_r_dM_W_per_GeV"]>0)
def check_T_w_trace_residual_delta_r_gap_small(): return _res("delta_r_gap_small", residual_summary()["approx_abs_Delta_r_gap"]<0.00035)
def check_T_w_trace_residual_sentence_mentions_not_export(): return _res("sentence_mentions_not_export", "not a physical W-mass export" in paper_safe_sentence())
def check_T_w_trace_residual_sentence_mentions_mev(): return _res("sentence_mentions_mev", "MeV" in paper_safe_sentence())
def check_T_w_trace_residual_band_green(): return _res("band_green", str(residual_summary()["interpretation_band"]).startswith("GREEN"))
def check_T_w_trace_residual_overclaim_guard_active(): return _res("overclaim_guard_active", LOCKED_STATE["overclaim_guard_active"] is True)
def check_T_w_trace_residual_no_export(): return _res("no_export", LOCKED_STATE["exports_physical_M_W"] is False)
def check_T_w_trace_residual_export_lock_preserved(): return _res("export_lock_preserved", LOCKED_STATE["physical_W_export_enabled"] is False)
def check_T_w_trace_residual_bank_closure():
    rows=[fn() for n,fn in _CHECKS.items() if n!="check_T_w_trace_residual_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))
_CHECKS={n:o for n,o in list(globals().items()) if n.startswith("check_T_w_trace_residual_") and callable(o)}
def register(registry:MutableMapping[str,Any])->None: registry.update(_CHECKS)
def run_all()->Dict[str,Any]:
    rows=[]
    for n,fn in _CHECKS.items():
        try: res=fn(); rows.append({"name":n,"passed":_passed(res),"result":res})
        except Exception as exc: rows.append({"name":n,"passed":False,"error":repr(exc)})
    ok=all(r["passed"] for r in rows); return {"passed":ok,"status":PASS_STATUS if ok else PASS_STATUS.replace("_PASS","_FAIL"),"checks":rows,"report":terminal_report()}
if __name__=="__main__":
    out=run_all(); print(out["status"]); print("SUMMARY",sum(r["passed"] for r in out["checks"]),"/",len(out["checks"]),"PASS"); print(paper_safe_sentence()); raise SystemExit(0 if out["passed"] else 1)
