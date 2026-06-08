"""W_TRACE v14 physics-source sprint terminal report.

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

STATUS = "P_w_v14_physics_sprint_terminal_report"
VERSION = "v14_0"
PASS_STATUS = "W_TRACE_V14_PHYSICS_SPRINT_TERMINAL_REPORT_BANK_PASS"
TITLE = "W_TRACE v14 physics-source sprint terminal report"
APF_DELTA_R_TARGET = getattr(srcmap, "APF_DELTA_R_TARGET", 0.0364075266128216881)
M_W_TRACE_GEV = getattr(srcmap, "M_W_TRACE_GEV", 80.362164334)
FORBIDDEN_TOKENS = ("observed_M_W", "world_average_M_W", "M_W_world_average", "APF_DELTA_R_TARGET_AS_INPUT", "Delta_r_target_backsolve", "fit_to_M_W_TRACE", "tune_to_APF_anchor", "manual_export_override", "physical_export_request")
LOCKED_STATE = {"real_reviewed_delta_r_payload": False, "real_payload_rows_imported": False, "component_sum_certified": False, "covariance_certified": False, "uncertainty_propagation_certified": False, "physical_W_export_enabled": False, "exports_physical_M_W": False}


SPRINT_MODULES = ("w_trace_acfw_candidate_preflight", "w_trace_denner_sirlin_notation_map", "w_trace_standard_delta_r_payload_schema", "w_trace_delta_r_comparison_harness", "w_trace_physics_source_stop_condition")
SPRINT_STATUS = "physics_source_acquisition_ready_no_more_scaffold"

def sprint_terminal_state() -> Dict[str, Any]:
    return {"sprint_modules": list(SPRINT_MODULES), "sprint_status": SPRINT_STATUS, "new_real_payloads_admitted": False, "physical_export": False, "next_required_artifact": "real reviewed standard Delta_r payload or completed source-extraction worksheet"}



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


def check_T_w_trace_v14_physics_sprint_terminal_report_status_declared():
    return _res("status_declared", STATUS == "P_w_v14_physics_sprint_terminal_report")


def check_T_w_trace_v14_physics_sprint_terminal_report_five_modules_listed():
    return _res("five_modules_listed", len(SPRINT_MODULES) == 5)


def check_T_w_trace_v14_physics_sprint_terminal_report_terminal_status_no_more_scaffold():
    return _res("terminal_status_no_more_scaffold", SPRINT_STATUS == "physics_source_acquisition_ready_no_more_scaffold")


def check_T_w_trace_v14_physics_sprint_terminal_report_no_payload_admitted():
    return _res("no_payload_admitted", sprint_terminal_state()["new_real_payloads_admitted"] is False)


def check_T_w_trace_v14_physics_sprint_terminal_report_no_export():
    return _res("no_export", sprint_terminal_state()["physical_export"] is False)


def check_T_w_trace_v14_physics_sprint_terminal_report_next_artifact_real_payload():
    return _res("next_artifact_real_payload", "real reviewed standard Delta_r payload" in sprint_terminal_state()["next_required_artifact"])


def check_T_w_trace_v14_physics_sprint_terminal_report_includes_acfw():
    return _res("includes_acfw", "w_trace_acfw_candidate_preflight" in SPRINT_MODULES)


def check_T_w_trace_v14_physics_sprint_terminal_report_includes_denner_sirlin():
    return _res("includes_denner_sirlin", "w_trace_denner_sirlin_notation_map" in SPRINT_MODULES)


def check_T_w_trace_v14_physics_sprint_terminal_report_includes_payload_schema():
    return _res("includes_payload_schema", "w_trace_standard_delta_r_payload_schema" in SPRINT_MODULES)


def check_T_w_trace_v14_physics_sprint_terminal_report_includes_comparison():
    return _res("includes_comparison", "w_trace_delta_r_comparison_harness" in SPRINT_MODULES)


def check_T_w_trace_v14_physics_sprint_terminal_report_includes_stop_condition():
    return _res("includes_stop_condition", "w_trace_physics_source_stop_condition" in SPRINT_MODULES)


def check_T_w_trace_v14_physics_sprint_terminal_report_locked_no_export():
    return _res("locked_no_export", LOCKED_STATE["exports_physical_M_W"] is False)


def check_T_w_trace_v14_physics_sprint_terminal_report_bank_closure():
    return _res("bank_closure", all([STATUS, PASS_STATUS, TITLE]))


_CHECKS = {
    "check_T_w_trace_v14_physics_sprint_terminal_report_status_declared": check_T_w_trace_v14_physics_sprint_terminal_report_status_declared,
    "check_T_w_trace_v14_physics_sprint_terminal_report_five_modules_listed": check_T_w_trace_v14_physics_sprint_terminal_report_five_modules_listed,
    "check_T_w_trace_v14_physics_sprint_terminal_report_terminal_status_no_more_scaffold": check_T_w_trace_v14_physics_sprint_terminal_report_terminal_status_no_more_scaffold,
    "check_T_w_trace_v14_physics_sprint_terminal_report_no_payload_admitted": check_T_w_trace_v14_physics_sprint_terminal_report_no_payload_admitted,
    "check_T_w_trace_v14_physics_sprint_terminal_report_no_export": check_T_w_trace_v14_physics_sprint_terminal_report_no_export,
    "check_T_w_trace_v14_physics_sprint_terminal_report_next_artifact_real_payload": check_T_w_trace_v14_physics_sprint_terminal_report_next_artifact_real_payload,
    "check_T_w_trace_v14_physics_sprint_terminal_report_includes_acfw": check_T_w_trace_v14_physics_sprint_terminal_report_includes_acfw,
    "check_T_w_trace_v14_physics_sprint_terminal_report_includes_denner_sirlin": check_T_w_trace_v14_physics_sprint_terminal_report_includes_denner_sirlin,
    "check_T_w_trace_v14_physics_sprint_terminal_report_includes_payload_schema": check_T_w_trace_v14_physics_sprint_terminal_report_includes_payload_schema,
    "check_T_w_trace_v14_physics_sprint_terminal_report_includes_comparison": check_T_w_trace_v14_physics_sprint_terminal_report_includes_comparison,
    "check_T_w_trace_v14_physics_sprint_terminal_report_includes_stop_condition": check_T_w_trace_v14_physics_sprint_terminal_report_includes_stop_condition,
    "check_T_w_trace_v14_physics_sprint_terminal_report_locked_no_export": check_T_w_trace_v14_physics_sprint_terminal_report_locked_no_export,
    "check_T_w_trace_v14_physics_sprint_terminal_report_bank_closure": check_T_w_trace_v14_physics_sprint_terminal_report_bank_closure,
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
