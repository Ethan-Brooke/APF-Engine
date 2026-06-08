"""W_TRACE standard Delta_r payload schema.

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

STATUS = "P_w_standard_delta_r_payload_schema"
VERSION = "v14_0"
PASS_STATUS = "W_TRACE_STANDARD_DELTA_R_PAYLOAD_SCHEMA_BANK_PASS"
TITLE = "W_TRACE standard Delta_r payload schema"
APF_DELTA_R_TARGET = getattr(srcmap, "APF_DELTA_R_TARGET", 0.0364075266128216881)
M_W_TRACE_GEV = getattr(srcmap, "M_W_TRACE_GEV", 80.362164334)
FORBIDDEN_TOKENS = ("observed_M_W", "world_average_M_W", "M_W_world_average", "APF_DELTA_R_TARGET_AS_INPUT", "Delta_r_target_backsolve", "fit_to_M_W_TRACE", "tune_to_APF_anchor", "manual_export_override", "physical_export_request")
LOCKED_STATE = {"real_reviewed_delta_r_payload": False, "real_payload_rows_imported": False, "component_sum_certified": False, "covariance_certified": False, "uncertainty_propagation_certified": False, "physical_W_export_enabled": False, "exports_physical_M_W": False}


PAYLOAD_SCHEMA_VERSION = "standard_delta_r_payload_schema_v14_0"
PAYLOAD_KINDS = ("standard_delta_r_total", "standard_delta_r_decomposition", "standard_delta_r_parametrization")
COMMON_REQUIRED_FIELDS = ("payload_schema_version", "payload_kind", "source_candidate_id", "source_digest", "input_scheme", "provenance", "anti_smuggling_attestations", "physical_export_requested")
DECOMPOSITION_FIELDS = ("Delta_alpha", "Delta_rho", "Delta_r_rem", "sW2_policy", "cW2_policy")
TOTAL_FIELDS = ("Delta_r_total", "uncertainty", "derivation_note")
PARAM_FIELDS = ("formula_reference", "input_vector", "output_quantity", "forward_solve_policy")

def schema_for(kind: str) -> Dict[str, Any]:
    base = {"kind": kind, "required": list(COMMON_REQUIRED_FIELDS), "allowed_for_export": False}
    if kind == "standard_delta_r_decomposition":
        base["required"] += list(DECOMPOSITION_FIELDS)
    elif kind == "standard_delta_r_total":
        base["required"] += list(TOTAL_FIELDS)
    elif kind == "standard_delta_r_parametrization":
        base["required"] += list(PARAM_FIELDS)
    else:
        base["valid"] = False
        return base
    base["valid"] = True
    return base

def validate_minimal_payload(payload: Mapping[str, Any]) -> Dict[str, Any]:
    kind = payload.get("payload_kind")
    schema = schema_for(str(kind))
    missing = [k for k in schema.get("required", ()) if k not in payload]
    clean = not contains_forbidden_token(payload)
    no_export = payload.get("physical_export_requested") is False
    return {"valid": schema.get("valid") is True and not missing and clean and no_export, "missing": missing, "clean": clean, "no_export": no_export}



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


def check_T_w_trace_standard_delta_r_payload_schema_status_declared():
    return _res("status_declared", STATUS == "P_w_standard_delta_r_payload_schema")


def check_T_w_trace_standard_delta_r_payload_schema_payload_kinds_match_source_mapping():
    return _res("payload_kinds_match_source_mapping", set(PAYLOAD_KINDS) == set(getattr(srcmap, "ALLOWED_PAYLOAD_KINDS", PAYLOAD_KINDS)))


def check_T_w_trace_standard_delta_r_payload_schema_common_fields_include_attestations():
    return _res("common_fields_include_attestations", "anti_smuggling_attestations" in COMMON_REQUIRED_FIELDS)


def check_T_w_trace_standard_delta_r_payload_schema_total_schema_valid():
    return _res("total_schema_valid", schema_for("standard_delta_r_total")["valid"] is True)


def check_T_w_trace_standard_delta_r_payload_schema_decomposition_schema_valid():
    return _res("decomposition_schema_valid", schema_for("standard_delta_r_decomposition")["valid"] is True)


def check_T_w_trace_standard_delta_r_payload_schema_parametrization_schema_valid():
    return _res("parametrization_schema_valid", schema_for("standard_delta_r_parametrization")["valid"] is True)


def check_T_w_trace_standard_delta_r_payload_schema_unknown_schema_invalid():
    return _res("unknown_schema_invalid", schema_for("bogus").get("valid") is False)


def check_T_w_trace_standard_delta_r_payload_schema_decomposition_requires_three_terms():
    return _res("decomposition_requires_three_terms", all(x in schema_for("standard_delta_r_decomposition")["required"] for x in ("Delta_alpha", "Delta_rho", "Delta_r_rem")))


def check_T_w_trace_standard_delta_r_payload_schema_parametrization_requires_forward_policy():
    return _res("parametrization_requires_forward_policy", "forward_solve_policy" in schema_for("standard_delta_r_parametrization")["required"])


def check_T_w_trace_standard_delta_r_payload_schema_forbidden_rejected():
    return _res("forbidden_rejected", validate_minimal_payload({"payload_kind":"standard_delta_r_total", "observed_M_W":"bad", "physical_export_requested":False})["valid"] is False)


def check_T_w_trace_standard_delta_r_payload_schema_export_request_rejected():
    return _res("export_request_rejected", validate_minimal_payload({"payload_kind":"standard_delta_r_total", "physical_export_requested":True})["valid"] is False)


def check_T_w_trace_standard_delta_r_payload_schema_locked_no_export():
    return _res("locked_no_export", LOCKED_STATE["physical_W_export_enabled"] is False)


def check_T_w_trace_standard_delta_r_payload_schema_bank_closure():
    return _res("bank_closure", all([STATUS, PASS_STATUS, TITLE, PAYLOAD_SCHEMA_VERSION]))


_CHECKS = {
    "check_T_w_trace_standard_delta_r_payload_schema_status_declared": check_T_w_trace_standard_delta_r_payload_schema_status_declared,
    "check_T_w_trace_standard_delta_r_payload_schema_payload_kinds_match_source_mapping": check_T_w_trace_standard_delta_r_payload_schema_payload_kinds_match_source_mapping,
    "check_T_w_trace_standard_delta_r_payload_schema_common_fields_include_attestations": check_T_w_trace_standard_delta_r_payload_schema_common_fields_include_attestations,
    "check_T_w_trace_standard_delta_r_payload_schema_total_schema_valid": check_T_w_trace_standard_delta_r_payload_schema_total_schema_valid,
    "check_T_w_trace_standard_delta_r_payload_schema_decomposition_schema_valid": check_T_w_trace_standard_delta_r_payload_schema_decomposition_schema_valid,
    "check_T_w_trace_standard_delta_r_payload_schema_parametrization_schema_valid": check_T_w_trace_standard_delta_r_payload_schema_parametrization_schema_valid,
    "check_T_w_trace_standard_delta_r_payload_schema_unknown_schema_invalid": check_T_w_trace_standard_delta_r_payload_schema_unknown_schema_invalid,
    "check_T_w_trace_standard_delta_r_payload_schema_decomposition_requires_three_terms": check_T_w_trace_standard_delta_r_payload_schema_decomposition_requires_three_terms,
    "check_T_w_trace_standard_delta_r_payload_schema_parametrization_requires_forward_policy": check_T_w_trace_standard_delta_r_payload_schema_parametrization_requires_forward_policy,
    "check_T_w_trace_standard_delta_r_payload_schema_forbidden_rejected": check_T_w_trace_standard_delta_r_payload_schema_forbidden_rejected,
    "check_T_w_trace_standard_delta_r_payload_schema_export_request_rejected": check_T_w_trace_standard_delta_r_payload_schema_export_request_rejected,
    "check_T_w_trace_standard_delta_r_payload_schema_locked_no_export": check_T_w_trace_standard_delta_r_payload_schema_locked_no_export,
    "check_T_w_trace_standard_delta_r_payload_schema_bank_closure": check_T_w_trace_standard_delta_r_payload_schema_bank_closure,
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
