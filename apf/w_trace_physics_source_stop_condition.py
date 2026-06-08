"""W_TRACE physics-source stop condition and no-more-scaffold gate.

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

STATUS = "P_w_physics_source_stop_condition"
VERSION = "v14_0"
PASS_STATUS = "W_TRACE_PHYSICS_SOURCE_STOP_CONDITION_BANK_PASS"
TITLE = "W_TRACE physics-source stop condition and no-more-scaffold gate"
APF_DELTA_R_TARGET = getattr(srcmap, "APF_DELTA_R_TARGET", 0.0364075266128216881)
M_W_TRACE_GEV = getattr(srcmap, "M_W_TRACE_GEV", 80.362164334)
FORBIDDEN_TOKENS = ("observed_M_W", "world_average_M_W", "M_W_world_average", "APF_DELTA_R_TARGET_AS_INPUT", "Delta_r_target_backsolve", "fit_to_M_W_TRACE", "tune_to_APF_anchor", "manual_export_override", "physical_export_request")
LOCKED_STATE = {"real_reviewed_delta_r_payload": False, "real_payload_rows_imported": False, "component_sum_certified": False, "covariance_certified": False, "uncertainty_propagation_certified": False, "physical_W_export_enabled": False, "exports_physical_M_W": False}


STOP_CONDITIONS = ("real_reviewed_standard_delta_r_payload_missing", "real_finite_part_rows_missing", "component_sum_certificate_missing", "covariance_certificate_missing", "uncertainty_certificate_missing")
ALLOWED_NEXT_ACTIONS = ("acquire_real_source", "complete_extraction_worksheet", "ingest_standard_delta_r_payload", "run_comparison_harness", "only_then_refine_to_apf_eight_slots")
FORBIDDEN_NEXT_ACTIONS = ("add_more_w_scaffolding_without_real_source", "fit_delta_r_to_apf_target", "consume_observed_w_mass", "enable_physical_export")

def stop_condition_report() -> Dict[str, Any]:
    return {"stop_conditions": list(STOP_CONDITIONS), "allowed_next_actions": list(ALLOWED_NEXT_ACTIONS), "forbidden_next_actions": list(FORBIDDEN_NEXT_ACTIONS), "scaffold_stop_active": True, "physical_export": False}

def action_allowed(action: str) -> bool:
    return action in ALLOWED_NEXT_ACTIONS and action not in FORBIDDEN_NEXT_ACTIONS



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


def check_T_w_trace_physics_source_stop_condition_status_declared():
    return _res("status_declared", STATUS == "P_w_physics_source_stop_condition")


def check_T_w_trace_physics_source_stop_condition_stop_active():
    return _res("stop_active", stop_condition_report()["scaffold_stop_active"] is True)


def check_T_w_trace_physics_source_stop_condition_requires_real_payload():
    return _res("requires_real_payload", "real_reviewed_standard_delta_r_payload_missing" in STOP_CONDITIONS)


def check_T_w_trace_physics_source_stop_condition_allows_source_acquisition():
    return _res("allows_source_acquisition", action_allowed("acquire_real_source"))


def check_T_w_trace_physics_source_stop_condition_allows_payload_ingestion():
    return _res("allows_payload_ingestion", action_allowed("ingest_standard_delta_r_payload"))


def check_T_w_trace_physics_source_stop_condition_forbids_more_scaffold():
    return _res("forbids_more_scaffold", action_allowed("add_more_w_scaffolding_without_real_source") is False)


def check_T_w_trace_physics_source_stop_condition_forbids_target_fit():
    return _res("forbids_target_fit", action_allowed("fit_delta_r_to_apf_target") is False)


def check_T_w_trace_physics_source_stop_condition_forbids_observed_w():
    return _res("forbids_observed_w", action_allowed("consume_observed_w_mass") is False)


def check_T_w_trace_physics_source_stop_condition_forbids_export():
    return _res("forbids_export", action_allowed("enable_physical_export") is False)


def check_T_w_trace_physics_source_stop_condition_report_clean():
    return _res("report_clean", not contains_forbidden_token(stop_condition_report()))


def check_T_w_trace_physics_source_stop_condition_locked_no_export():
    return _res("locked_no_export", LOCKED_STATE["physical_W_export_enabled"] is False)


def check_T_w_trace_physics_source_stop_condition_allowed_order_refines_last():
    return _res("allowed_order_refines_last", ALLOWED_NEXT_ACTIONS[-1] == "only_then_refine_to_apf_eight_slots")


def check_T_w_trace_physics_source_stop_condition_bank_closure():
    return _res("bank_closure", all([STATUS, PASS_STATUS, TITLE]))


_CHECKS = {
    "check_T_w_trace_physics_source_stop_condition_status_declared": check_T_w_trace_physics_source_stop_condition_status_declared,
    "check_T_w_trace_physics_source_stop_condition_stop_active": check_T_w_trace_physics_source_stop_condition_stop_active,
    "check_T_w_trace_physics_source_stop_condition_requires_real_payload": check_T_w_trace_physics_source_stop_condition_requires_real_payload,
    "check_T_w_trace_physics_source_stop_condition_allows_source_acquisition": check_T_w_trace_physics_source_stop_condition_allows_source_acquisition,
    "check_T_w_trace_physics_source_stop_condition_allows_payload_ingestion": check_T_w_trace_physics_source_stop_condition_allows_payload_ingestion,
    "check_T_w_trace_physics_source_stop_condition_forbids_more_scaffold": check_T_w_trace_physics_source_stop_condition_forbids_more_scaffold,
    "check_T_w_trace_physics_source_stop_condition_forbids_target_fit": check_T_w_trace_physics_source_stop_condition_forbids_target_fit,
    "check_T_w_trace_physics_source_stop_condition_forbids_observed_w": check_T_w_trace_physics_source_stop_condition_forbids_observed_w,
    "check_T_w_trace_physics_source_stop_condition_forbids_export": check_T_w_trace_physics_source_stop_condition_forbids_export,
    "check_T_w_trace_physics_source_stop_condition_report_clean": check_T_w_trace_physics_source_stop_condition_report_clean,
    "check_T_w_trace_physics_source_stop_condition_locked_no_export": check_T_w_trace_physics_source_stop_condition_locked_no_export,
    "check_T_w_trace_physics_source_stop_condition_allowed_order_refines_last": check_T_w_trace_physics_source_stop_condition_allowed_order_refines_last,
    "check_T_w_trace_physics_source_stop_condition_bank_closure": check_T_w_trace_physics_source_stop_condition_bank_closure,
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
