"""W_TRACE independent Delta_r comparison harness.

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

STATUS = "P_w_delta_r_comparison_harness"
VERSION = "v14_0"
PASS_STATUS = "W_TRACE_DELTA_R_COMPARISON_HARNESS_BANK_PASS"
TITLE = "W_TRACE independent Delta_r comparison harness"
APF_DELTA_R_TARGET = getattr(srcmap, "APF_DELTA_R_TARGET", 0.0364075266128216881)
M_W_TRACE_GEV = getattr(srcmap, "M_W_TRACE_GEV", 80.362164334)
FORBIDDEN_TOKENS = ("observed_M_W", "world_average_M_W", "M_W_world_average", "APF_DELTA_R_TARGET_AS_INPUT", "Delta_r_target_backsolve", "fit_to_M_W_TRACE", "tune_to_APF_anchor", "manual_export_override", "physical_export_request")
LOCKED_STATE = {"real_reviewed_delta_r_payload": False, "real_payload_rows_imported": False, "component_sum_certified": False, "covariance_certified": False, "uncertainty_propagation_certified": False, "physical_W_export_enabled": False, "exports_physical_M_W": False}


COMPARISON_SCHEMA = {"source_delta_r": "independent_source_output", "apf_delta_r_target": "comparison_only", "residual": "source_minus_apf", "tolerance": "declared_before_comparison", "verdict": "descriptive_not_export"}

def compute_residual(source_delta_r: float, tolerance: float) -> Dict[str, Any]:
    residual = float(source_delta_r) - float(APF_DELTA_R_TARGET)
    return {"source_delta_r": float(source_delta_r), "apf_delta_r_target": APF_DELTA_R_TARGET, "residual": residual, "abs_residual": abs(residual), "within_tolerance": abs(residual) <= float(tolerance), "physical_export": False}

def comparison_allowed(payload: Mapping[str, Any]) -> bool:
    return bool(payload.get("independent_source_admitted") is True and payload.get("uses_apf_target_as_input") is False and payload.get("uses_observed_w_as_input") is False and payload.get("physical_export_requested") is False)



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


def check_T_w_trace_delta_r_comparison_harness_status_declared():
    return _res("status_declared", STATUS == "P_w_delta_r_comparison_harness")


def check_T_w_trace_delta_r_comparison_harness_schema_comparison_only():
    return _res("schema_comparison_only", COMPARISON_SCHEMA["apf_delta_r_target"] == "comparison_only")


def check_T_w_trace_delta_r_comparison_harness_residual_zero_for_target():
    return _res("residual_zero_for_target", compute_residual(APF_DELTA_R_TARGET, 0.0)["residual"] == 0.0)


def check_T_w_trace_delta_r_comparison_harness_residual_nonexport():
    return _res("residual_nonexport", compute_residual(APF_DELTA_R_TARGET, 1.0)["physical_export"] is False)


def check_T_w_trace_delta_r_comparison_harness_comparison_requires_admitted_source():
    return _res("comparison_requires_admitted_source", comparison_allowed({"independent_source_admitted":False,"uses_apf_target_as_input":False,"uses_observed_w_as_input":False,"physical_export_requested":False}) is False)


def check_T_w_trace_delta_r_comparison_harness_comparison_blocks_apf_input():
    return _res("comparison_blocks_apf_input", comparison_allowed({"independent_source_admitted":True,"uses_apf_target_as_input":True,"uses_observed_w_as_input":False,"physical_export_requested":False}) is False)


def check_T_w_trace_delta_r_comparison_harness_comparison_blocks_observed_w():
    return _res("comparison_blocks_observed_w", comparison_allowed({"independent_source_admitted":True,"uses_apf_target_as_input":False,"uses_observed_w_as_input":True,"physical_export_requested":False}) is False)


def check_T_w_trace_delta_r_comparison_harness_comparison_blocks_export():
    return _res("comparison_blocks_export", comparison_allowed({"independent_source_admitted":True,"uses_apf_target_as_input":False,"uses_observed_w_as_input":False,"physical_export_requested":True}) is False)


def check_T_w_trace_delta_r_comparison_harness_comparison_allows_clean_admitted():
    return _res("comparison_allows_clean_admitted", comparison_allowed({"independent_source_admitted":True,"uses_apf_target_as_input":False,"uses_observed_w_as_input":False,"physical_export_requested":False}) is True)


def check_T_w_trace_delta_r_comparison_harness_forbidden_token_detected():
    return _res("forbidden_token_detected", contains_forbidden_token({"x":"Delta_r_target_backsolve"}))


def check_T_w_trace_delta_r_comparison_harness_locked_no_export():
    return _res("locked_no_export", LOCKED_STATE["physical_W_export_enabled"] is False and LOCKED_STATE["exports_physical_M_W"] is False)


def check_T_w_trace_delta_r_comparison_harness_target_preserved():
    return _res("target_preserved", 0.03 < APF_DELTA_R_TARGET < 0.04)


def check_T_w_trace_delta_r_comparison_harness_bank_closure():
    return _res("bank_closure", all([STATUS, PASS_STATUS, TITLE]))


_CHECKS = {
    "check_T_w_trace_delta_r_comparison_harness_status_declared": check_T_w_trace_delta_r_comparison_harness_status_declared,
    "check_T_w_trace_delta_r_comparison_harness_schema_comparison_only": check_T_w_trace_delta_r_comparison_harness_schema_comparison_only,
    "check_T_w_trace_delta_r_comparison_harness_residual_zero_for_target": check_T_w_trace_delta_r_comparison_harness_residual_zero_for_target,
    "check_T_w_trace_delta_r_comparison_harness_residual_nonexport": check_T_w_trace_delta_r_comparison_harness_residual_nonexport,
    "check_T_w_trace_delta_r_comparison_harness_comparison_requires_admitted_source": check_T_w_trace_delta_r_comparison_harness_comparison_requires_admitted_source,
    "check_T_w_trace_delta_r_comparison_harness_comparison_blocks_apf_input": check_T_w_trace_delta_r_comparison_harness_comparison_blocks_apf_input,
    "check_T_w_trace_delta_r_comparison_harness_comparison_blocks_observed_w": check_T_w_trace_delta_r_comparison_harness_comparison_blocks_observed_w,
    "check_T_w_trace_delta_r_comparison_harness_comparison_blocks_export": check_T_w_trace_delta_r_comparison_harness_comparison_blocks_export,
    "check_T_w_trace_delta_r_comparison_harness_comparison_allows_clean_admitted": check_T_w_trace_delta_r_comparison_harness_comparison_allows_clean_admitted,
    "check_T_w_trace_delta_r_comparison_harness_forbidden_token_detected": check_T_w_trace_delta_r_comparison_harness_forbidden_token_detected,
    "check_T_w_trace_delta_r_comparison_harness_locked_no_export": check_T_w_trace_delta_r_comparison_harness_locked_no_export,
    "check_T_w_trace_delta_r_comparison_harness_target_preserved": check_T_w_trace_delta_r_comparison_harness_target_preserved,
    "check_T_w_trace_delta_r_comparison_harness_bank_closure": check_T_w_trace_delta_r_comparison_harness_bank_closure,
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
