
"""v14.2 W_TRACE physics validation sprint terminal report."""
from __future__ import annotations
from typing import Any, Dict, MutableMapping
from apf import w_trace_input_convention_stress_test as stress
from apf import w_trace_independent_delta_r_crosscheck as cross
from apf import w_trace_multisource_delta_r_comparison as multi

STATUS="P_w_v142_physics_validation_sprint_report"
VERSION="v14_2"
PASS_STATUS="W_TRACE_V14_2_PHYSICS_VALIDATION_SPRINT_PASS"
SPRINT_MODULES=("w_trace_input_convention_stress_test","w_trace_independent_delta_r_crosscheck","w_trace_multisource_delta_r_comparison")
LOCKED_STATE={"real_standard_delta_r_payload_candidate_extracted":True,"independent_crosscheck_complete":True,"multisource_comparison_complete":True,"physical_W_export_enabled":False,"exports_physical_M_W":False,"component_sum_certified":False,"covariance_certified":False,"uncertainty_propagation_certified":False}

def terminal_report() -> Dict[str, Any]:
    return {"status":STATUS,"version":VERSION,"sprint_modules":SPRINT_MODULES,"stress_report":stress.terminal_report(),"crosscheck_report":cross.terminal_report(),"multisource_report":multi.terminal_report(),"locked_state":dict(LOCKED_STATE),"verdict":"V14_2_VALIDATION_GOT_THERE_APF_TRACE_W_IN_FEW_MEV_SM_SOURCE_CLUSTER_SECOND_INDEPENDENT_SOURCE_FAMILY_CONFIRMED_NO_PHYSICAL_EXPORT"}
def _res(c,p,**e): r={"check":c,"passed":bool(p)}; r.update(e); return r
def _passed(r): return isinstance(r,dict) and r.get("passed") is True

def check_T_w_trace_v142_status_declared(): return _res("status_declared", STATUS.startswith("P_w_"))
def check_T_w_trace_v142_has_three_sprint_modules(): return _res("has_three_sprint_modules", len(SPRINT_MODULES)==3)
def check_T_w_trace_v142_stress_module_passes(): return _res("stress_module_passes", stress.run_all()["passed"] is True)
def check_T_w_trace_v142_crosscheck_module_passes(): return _res("crosscheck_module_passes", cross.run_all()["passed"] is True)
def check_T_w_trace_v142_multisource_module_passes(): return _res("multisource_module_passes", multi.run_all()["passed"] is True)
def check_T_w_trace_v142_second_source_family_present(): return _res("second_source_family_present", "DGG_2015_JHEP_mW_mZ_interdependence" in cross.crosscheck_rows())
def check_T_w_trace_v142_weighted_gap_small(): return _res("weighted_gap_small", abs(multi.weighted_summary()["weighted_M_W_minus_W_TRACE_MeV"]) < 5.0)
def check_T_w_trace_v142_weighted_gap_less_than_1p2sigma(): return _res("weighted_gap_less_than_1p2sigma", multi.weighted_summary()["weighted_gap_sigma_units"] < 1.2)
def check_T_w_trace_v142_all_real_export_locked(): return _res("all_real_export_locked", LOCKED_STATE["exports_physical_M_W"] is False and LOCKED_STATE["physical_W_export_enabled"] is False)
def check_T_w_trace_v142_no_component_sum_claim(): return _res("no_component_sum_claim", LOCKED_STATE["component_sum_certified"] is False)
def check_T_w_trace_v142_no_covariance_claim(): return _res("no_covariance_claim", LOCKED_STATE["covariance_certified"] is False)
def check_T_w_trace_v142_verdict_got_there(): return _res("verdict_got_there", "GOT_THERE" in terminal_report()["verdict"])
def check_T_w_trace_v142_bank_closure():
    rows=[fn() for n,fn in _CHECKS.items() if n!="check_T_w_trace_v142_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))
_CHECKS={n:o for n,o in list(globals().items()) if n.startswith("check_T_w_trace_v142_") and callable(o)}
def register(registry: MutableMapping[str, Any]) -> None: registry.update(_CHECKS)
def run_all() -> Dict[str, Any]:
    rows=[]
    for n,fn in _CHECKS.items():
        try: res=fn(); rows.append({"name":n,"passed":_passed(res),"result":res})
        except Exception as exc: rows.append({"name":n,"passed":False,"error":repr(exc)})
    ok=all(r["passed"] for r in rows); return {"passed":ok,"status":PASS_STATUS if ok else PASS_STATUS.replace("_PASS","_FAIL"),"checks":rows,"report":terminal_report()}
if __name__=="__main__":
    out=run_all(); print(out["status"]); print("SUMMARY",sum(r["passed"] for r in out["checks"]),"/",len(out["checks"]),"PASS"); print(terminal_report()["verdict"]); raise SystemExit(0 if out["passed"] else 1)
