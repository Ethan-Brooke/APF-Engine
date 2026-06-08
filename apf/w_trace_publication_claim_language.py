"""Publication-safe claim language for W_TRACE physics validation result (v14.4)."""
from __future__ import annotations
from typing import Any, Dict, MutableMapping
from apf import w_trace_residual_interpretation as resid
STATUS="P_w_publication_claim_language"; VERSION="v14_4"; PASS_STATUS="W_TRACE_PUBLICATION_CLAIM_LANGUAGE_BANK_PASS"
LOCKED_STATE={"claim_language_banked":True,"physical_W_export_enabled":False,"exports_physical_M_W":False}
ALLOWED_CLAIMS=[
"APF/W_TRACE produces a local trace-sector W anchor.",
"Independent SM prediction sources map to total Delta_r values within a few MeV of the W_TRACE anchor.",
"Under conservative source-scale pulls, the comparison is GREEN.",
"Observed W measurements are quarantined as context and are not source inputs.",
]
FORBIDDEN_CLAIMS=["APF predicts the physical W mass", "APF closes on-shell W transport", "observed W mass was used", "Delta_r components are independently certified"]
def claim_packet()->Dict[str,Any]: return {"status":STATUS,"version":VERSION,"allowed_claims":list(ALLOWED_CLAIMS),"forbidden_claims":list(FORBIDDEN_CLAIMS),"preferred_sentence":resid.paper_safe_sentence(),"locked_state":dict(LOCKED_STATE),"claim_level":"validation_comparison_not_export"}
def is_safe_claim(text:str)->bool:
    low=text.lower(); return not any(tok.lower() in low for tok in ["predicts the physical w", "closes on-shell", "observed w mass was used", "components are independently certified"])
def _res(c,p,**e): r={"check":c,"passed":bool(p)}; r.update(e); return r
def _passed(r): return isinstance(r,dict) and r.get("passed") is True
def check_T_w_trace_claim_language_status_declared(): return _res("status_declared", STATUS.startswith("P_w_"))
def check_T_w_trace_claim_language_allowed_nonempty(): return _res("allowed_nonempty", len(ALLOWED_CLAIMS)>=4)
def check_T_w_trace_claim_language_forbidden_nonempty(): return _res("forbidden_nonempty", len(FORBIDDEN_CLAIMS)>=4)
def check_T_w_trace_claim_language_preferred_sentence_safe(): return _res("preferred_sentence_safe", is_safe_claim(claim_packet()["preferred_sentence"]))
def check_T_w_trace_claim_language_mentions_validation_not_export(): return _res("mentions_validation_not_export", claim_packet()["claim_level"]=="validation_comparison_not_export")
def check_T_w_trace_claim_language_forbids_physical_prediction(): return _res("forbids_physical_prediction", any("physical W mass" in x for x in FORBIDDEN_CLAIMS))
def check_T_w_trace_claim_language_forbids_observed_input(): return _res("forbids_observed_input", any("observed" in x for x in FORBIDDEN_CLAIMS))
def check_T_w_trace_claim_language_all_allowed_safe(): return _res("all_allowed_safe", all(is_safe_claim(x) for x in ALLOWED_CLAIMS))
def check_T_w_trace_claim_language_preferred_mentions_green_or_few_mev(): return _res("preferred_mentions_mev", "MeV" in claim_packet()["preferred_sentence"])
def check_T_w_trace_claim_language_no_component_certification_claim(): return _res("no_component_certification_claim", any("components" in x for x in FORBIDDEN_CLAIMS))
def check_T_w_trace_claim_language_no_export(): return _res("no_export", LOCKED_STATE["exports_physical_M_W"] is False)
def check_T_w_trace_claim_language_export_lock_preserved(): return _res("export_lock_preserved", LOCKED_STATE["physical_W_export_enabled"] is False)
def check_T_w_trace_claim_language_bank_closure():
    rows=[fn() for n,fn in _CHECKS.items() if n!="check_T_w_trace_claim_language_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))
_CHECKS={n:o for n,o in list(globals().items()) if n.startswith("check_T_w_trace_claim_language_") and callable(o)}
def register(registry:MutableMapping[str,Any])->None: registry.update(_CHECKS)
def run_all()->Dict[str,Any]:
    rows=[]
    for n,fn in _CHECKS.items():
        try: res=fn(); rows.append({"name":n,"passed":_passed(res),"result":res})
        except Exception as exc: rows.append({"name":n,"passed":False,"error":repr(exc)})
    ok=all(r["passed"] for r in rows); return {"passed":ok,"status":PASS_STATUS if ok else PASS_STATUS.replace("_PASS","_FAIL"),"checks":rows,"report":claim_packet()}
if __name__=="__main__":
    out=run_all(); print(out["status"]); print("SUMMARY",sum(r["passed"] for r in out["checks"]),"/",len(out["checks"]),"PASS"); print(claim_packet()["preferred_sentence"]); raise SystemExit(0 if out["passed"] else 1)
