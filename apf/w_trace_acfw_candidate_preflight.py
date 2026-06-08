"""W_TRACE ACFW precision-parametrization candidate preflight.

Part of the v14.0 W_TRACE physics-source acquisition sprint.
This module advances physics/content ingestion while preserving the locked rule:
standard electroweak Delta_r sources may be mapped and compared, but physical W
export remains closed until real reviewed payloads, component-sum/covariance, and
uncertainty certificates are supplied.
"""
from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Tuple

from apf import w_trace_delta_r_source_mapping as srcmap
from apf import w_trace_delta_r_source_candidate_registry as registry
from apf import w_trace_delta_r_source_extraction_protocol as protocol

STATUS = "P_w_acfw_candidate_preflight"
VERSION = "v14_0"
PASS_STATUS = "W_TRACE_ACFW_CANDIDATE_PREFLIGHT_BANK_PASS"
TITLE = "W_TRACE ACFW precision-parametrization candidate preflight"
APF_DELTA_R_TARGET = getattr(srcmap, "APF_DELTA_R_TARGET", 0.0364075266128216881)
M_W_TRACE_GEV = getattr(srcmap, "M_W_TRACE_GEV", 80.362164334)
FORBIDDEN_TOKENS = ("observed_M_W", "world_average_M_W", "M_W_world_average", "APF_DELTA_R_TARGET_AS_INPUT", "Delta_r_target_backsolve", "fit_to_M_W_TRACE", "tune_to_APF_anchor", "manual_export_override", "physical_export_request")
LOCKED_STATE = {"real_reviewed_delta_r_payload": False, "real_payload_rows_imported": False, "component_sum_certified": False, "covariance_certified": False, "uncertainty_propagation_certified": False, "physical_W_export_enabled": False, "exports_physical_M_W": False}


ACFW_CANDIDATE_ID = "ACFW_precision_MW_parametrization"
ACFW_PRELIGHT_RECORD = {
    "candidate_id": ACFW_CANDIDATE_ID,
    "payload_kind": "standard_delta_r_parametrization",
    "source_role": "precision_prediction_parametrization",
    "can_supply": ("M_W_SM_parametrization", "Delta_r_total_derived_by_forward_solve", "theory_uncertainty_MW"),
    "cannot_supply": ("APF_eight_slot_rows", "observed_W_mass_input", "APF_anchor_input"),
    "input_scheme_policy": ("alpha", "G_F", "M_Z", "M_H", "m_t", "Delta_alpha_had", "alpha_s"),
    "admission_state": "candidate_preflight_only",
}

def candidate_record() -> Dict[str, Any]:
    return dict(ACFW_PRELIGHT_RECORD)

def extraction_order() -> Tuple[str, ...]:
    return ("source_locator", "parametrization_formula", "input_domain", "input_constants", "forward_MW_output", "derive_Delta_r_total", "compare_to_APF_anchor")



def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def contains_forbidden_token(obj: Any) -> bool:
    text = _canonical_json(obj)
    return any(tok in text for tok in FORBIDDEN_TOKENS)

def _res(check: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    row = {"check": check, "passed": bool(passed)}
    row.update(extra)
    return row

def _passed(row: Any) -> bool:
    return bool(isinstance(row, dict) and row.get("passed") is True)

def terminal_report() -> Dict[str, Any]:
    return {
        "status": STATUS,
        "version": VERSION,
        "title": TITLE,
        "locked_state": dict(LOCKED_STATE),
        "apf_comparison_target": {"Delta_r_APF_TRACE_target": APF_DELTA_R_TARGET, "M_W_TRACE_GeV": M_W_TRACE_GEV, "role": "comparison_only"},
        "stop_rule": "No physical W export; no APF target or observed W may be consumed by a source payload.",
    }


def check_T_w_trace_acfw_candidate_preflight_status_declared():
    return _res("status_declared", STATUS == "P_w_acfw_candidate_preflight")


def check_T_w_trace_acfw_candidate_preflight_upstream_registry_present():
    return _res("upstream_registry_present", hasattr(registry, "source_to_payload_plan") and hasattr(srcmap, "ALLOWED_PAYLOAD_KINDS"))


def check_T_w_trace_acfw_candidate_preflight_candidate_id_known():
    return _res("candidate_id_known", registry.source_to_payload_plan(ACFW_CANDIDATE_ID).get("valid_candidate") is True)


def check_T_w_trace_acfw_candidate_preflight_payload_kind_standard():
    return _res("payload_kind_standard", ACFW_PRELIGHT_RECORD["payload_kind"] in getattr(srcmap, "ALLOWED_PAYLOAD_KINDS", ()))


def check_T_w_trace_acfw_candidate_preflight_candidate_not_admitted():
    return _res("candidate_not_admitted", ACFW_PRELIGHT_RECORD["admission_state"] == "candidate_preflight_only")


def check_T_w_trace_acfw_candidate_preflight_can_supply_forward_prediction():
    return _res("can_supply_forward_prediction", "M_W_SM_parametrization" in ACFW_PRELIGHT_RECORD["can_supply"])


def check_T_w_trace_acfw_candidate_preflight_derive_delta_r_after_forward_output():
    return _res("derive_delta_r_after_forward_output", extraction_order().index("derive_Delta_r_total") > extraction_order().index("forward_MW_output"))


def check_T_w_trace_acfw_candidate_preflight_comparison_last():
    return _res("comparison_last", extraction_order()[-1] == "compare_to_APF_anchor")


def check_T_w_trace_acfw_candidate_preflight_observed_w_forbidden():
    return _res("observed_w_forbidden", contains_forbidden_token({"x":"observed_M_W"}))


def check_T_w_trace_acfw_candidate_preflight_apf_anchor_forbidden():
    return _res("apf_anchor_forbidden", contains_forbidden_token({"x":"APF_DELTA_R_TARGET_AS_INPUT"}))


def check_T_w_trace_acfw_candidate_preflight_record_clean():
    return _res("record_clean", not contains_forbidden_token(ACFW_PRELIGHT_RECORD))


def check_T_w_trace_acfw_candidate_preflight_locked_no_export():
    return _res("locked_no_export", LOCKED_STATE["physical_W_export_enabled"] is False and LOCKED_STATE["exports_physical_M_W"] is False)


def check_T_w_trace_acfw_candidate_preflight_bank_closure():
    return _res("bank_closure", all([STATUS, PASS_STATUS, TITLE, ACFW_CANDIDATE_ID]))


_CHECKS = {
    "check_T_w_trace_acfw_candidate_preflight_status_declared": check_T_w_trace_acfw_candidate_preflight_status_declared,
    "check_T_w_trace_acfw_candidate_preflight_upstream_registry_present": check_T_w_trace_acfw_candidate_preflight_upstream_registry_present,
    "check_T_w_trace_acfw_candidate_preflight_candidate_id_known": check_T_w_trace_acfw_candidate_preflight_candidate_id_known,
    "check_T_w_trace_acfw_candidate_preflight_payload_kind_standard": check_T_w_trace_acfw_candidate_preflight_payload_kind_standard,
    "check_T_w_trace_acfw_candidate_preflight_candidate_not_admitted": check_T_w_trace_acfw_candidate_preflight_candidate_not_admitted,
    "check_T_w_trace_acfw_candidate_preflight_can_supply_forward_prediction": check_T_w_trace_acfw_candidate_preflight_can_supply_forward_prediction,
    "check_T_w_trace_acfw_candidate_preflight_derive_delta_r_after_forward_output": check_T_w_trace_acfw_candidate_preflight_derive_delta_r_after_forward_output,
    "check_T_w_trace_acfw_candidate_preflight_comparison_last": check_T_w_trace_acfw_candidate_preflight_comparison_last,
    "check_T_w_trace_acfw_candidate_preflight_observed_w_forbidden": check_T_w_trace_acfw_candidate_preflight_observed_w_forbidden,
    "check_T_w_trace_acfw_candidate_preflight_apf_anchor_forbidden": check_T_w_trace_acfw_candidate_preflight_apf_anchor_forbidden,
    "check_T_w_trace_acfw_candidate_preflight_record_clean": check_T_w_trace_acfw_candidate_preflight_record_clean,
    "check_T_w_trace_acfw_candidate_preflight_locked_no_export": check_T_w_trace_acfw_candidate_preflight_locked_no_export,
    "check_T_w_trace_acfw_candidate_preflight_bank_closure": check_T_w_trace_acfw_candidate_preflight_bank_closure,
}


def register(registry: MutableMapping[str, Any]) -> None:
    registry.update(_CHECKS)

def run_all() -> Dict[str, Any]:
    rows = []
    for name, fn in _CHECKS.items():
        try:
            result = fn()
            rows.append({"name": name, "passed": _passed(result), "result": result})
        except Exception as exc:  # pragma: no cover
            rows.append({"name": name, "passed": False, "error": repr(exc)})
    ok = all(row["passed"] for row in rows)
    return {"passed": ok, "status": PASS_STATUS if ok else PASS_STATUS.replace("_PASS", "_FAIL"), "checks": rows, "report": terminal_report()}

if __name__ == "__main__":
    out = run_all()
    print(out["status"])
    for row in out["checks"]:
        print(("PASS" if row["passed"] else "FAIL"), row["name"])
    raise SystemExit(0 if out["passed"] else 1)
