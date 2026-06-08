"""W_TRACE Denner/Sirlin standard Delta_r notation map.

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

STATUS = "P_w_denner_sirlin_notation_map"
VERSION = "v14_0"
PASS_STATUS = "W_TRACE_DENNER_SIRLIN_NOTATION_MAP_BANK_PASS"
TITLE = "W_TRACE Denner/Sirlin standard Delta_r notation map"
APF_DELTA_R_TARGET = getattr(srcmap, "APF_DELTA_R_TARGET", 0.0364075266128216881)
M_W_TRACE_GEV = getattr(srcmap, "M_W_TRACE_GEV", 80.362164334)
FORBIDDEN_TOKENS = ("observed_M_W", "world_average_M_W", "M_W_world_average", "APF_DELTA_R_TARGET_AS_INPUT", "Delta_r_target_backsolve", "fit_to_M_W_TRACE", "tune_to_APF_anchor", "manual_export_override", "physical_export_request")
LOCKED_STATE = {"real_reviewed_delta_r_payload": False, "real_payload_rows_imported": False, "component_sum_certified": False, "covariance_certified": False, "uncertainty_propagation_certified": False, "physical_W_export_enabled": False, "exports_physical_M_W": False}


STANDARD_SYMBOLS = {"Delta_r": "Delta_r", "Delta_alpha": "Delta_alpha", "Delta_rho": "Delta_rho", "Delta_r_rem": "Delta_r_rem", "Delta_r_ct_OS": "Delta_r_ct_OS"}
DENNER_MAP = {"source_family": "Denner_on_shell_renormalization_structure", "supports": ("counterterm_structure_reference", "standard_delta_r_decomposition"), "maps": dict(STANDARD_SYMBOLS), "role": "on_shell_counterterm_and_notation_structure"}
SIRLIN_MAP = {"source_family": "Sirlin_Delta_r_lineage", "supports": ("definition_lineage_reference", "standard_delta_r_total"), "maps": {"Delta_r": "Delta_r", "on_shell_relation": "Sirlin_Delta_r_definition"}, "role": "definition_lineage"}

def combined_notation_map() -> Dict[str, Any]:
    return {"standard_symbols": dict(STANDARD_SYMBOLS), "denner": dict(DENNER_MAP), "sirlin": dict(SIRLIN_MAP), "physical_export": False}

def maps_to_standard(symbol: str) -> bool:
    return symbol in STANDARD_SYMBOLS.values()



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


def check_T_w_trace_denner_sirlin_notation_map_status_declared():
    return _res("status_declared", STATUS == "P_w_denner_sirlin_notation_map")


def check_T_w_trace_denner_sirlin_notation_map_standard_symbols_complete():
    return _res("standard_symbols_complete", set(STANDARD_SYMBOLS) == {"Delta_r", "Delta_alpha", "Delta_rho", "Delta_r_rem", "Delta_r_ct_OS"})


def check_T_w_trace_denner_sirlin_notation_map_denner_supports_counterterm():
    return _res("denner_supports_counterterm", "counterterm_structure_reference" in DENNER_MAP["supports"])


def check_T_w_trace_denner_sirlin_notation_map_denner_supports_decomposition():
    return _res("denner_supports_decomposition", "standard_delta_r_decomposition" in DENNER_MAP["supports"])


def check_T_w_trace_denner_sirlin_notation_map_sirlin_supports_lineage():
    return _res("sirlin_supports_lineage", "definition_lineage_reference" in SIRLIN_MAP["supports"])


def check_T_w_trace_denner_sirlin_notation_map_sirlin_delta_r_present():
    return _res("sirlin_delta_r_present", SIRLIN_MAP["maps"].get("Delta_r") == "Delta_r")


def check_T_w_trace_denner_sirlin_notation_map_delta_r_maps_standard():
    return _res("delta_r_maps_standard", maps_to_standard("Delta_r"))


def check_T_w_trace_denner_sirlin_notation_map_ct_maps_standard():
    return _res("ct_maps_standard", maps_to_standard("Delta_r_ct_OS"))


def check_T_w_trace_denner_sirlin_notation_map_combined_clean():
    return _res("combined_clean", not contains_forbidden_token(combined_notation_map()))


def check_T_w_trace_denner_sirlin_notation_map_no_physical_export():
    return _res("no_physical_export", combined_notation_map()["physical_export"] is False)


def check_T_w_trace_denner_sirlin_notation_map_upstream_candidate_registry_loaded():
    return _res("upstream_candidate_registry_loaded", hasattr(registry, "source_to_payload_plan"))


def check_T_w_trace_denner_sirlin_notation_map_locked_no_export():
    return _res("locked_no_export", LOCKED_STATE["physical_W_export_enabled"] is False)


def check_T_w_trace_denner_sirlin_notation_map_bank_closure():
    return _res("bank_closure", all([STATUS, PASS_STATUS, TITLE]))


_CHECKS = {
    "check_T_w_trace_denner_sirlin_notation_map_status_declared": check_T_w_trace_denner_sirlin_notation_map_status_declared,
    "check_T_w_trace_denner_sirlin_notation_map_standard_symbols_complete": check_T_w_trace_denner_sirlin_notation_map_standard_symbols_complete,
    "check_T_w_trace_denner_sirlin_notation_map_denner_supports_counterterm": check_T_w_trace_denner_sirlin_notation_map_denner_supports_counterterm,
    "check_T_w_trace_denner_sirlin_notation_map_denner_supports_decomposition": check_T_w_trace_denner_sirlin_notation_map_denner_supports_decomposition,
    "check_T_w_trace_denner_sirlin_notation_map_sirlin_supports_lineage": check_T_w_trace_denner_sirlin_notation_map_sirlin_supports_lineage,
    "check_T_w_trace_denner_sirlin_notation_map_sirlin_delta_r_present": check_T_w_trace_denner_sirlin_notation_map_sirlin_delta_r_present,
    "check_T_w_trace_denner_sirlin_notation_map_delta_r_maps_standard": check_T_w_trace_denner_sirlin_notation_map_delta_r_maps_standard,
    "check_T_w_trace_denner_sirlin_notation_map_ct_maps_standard": check_T_w_trace_denner_sirlin_notation_map_ct_maps_standard,
    "check_T_w_trace_denner_sirlin_notation_map_combined_clean": check_T_w_trace_denner_sirlin_notation_map_combined_clean,
    "check_T_w_trace_denner_sirlin_notation_map_no_physical_export": check_T_w_trace_denner_sirlin_notation_map_no_physical_export,
    "check_T_w_trace_denner_sirlin_notation_map_upstream_candidate_registry_loaded": check_T_w_trace_denner_sirlin_notation_map_upstream_candidate_registry_loaded,
    "check_T_w_trace_denner_sirlin_notation_map_locked_no_export": check_T_w_trace_denner_sirlin_notation_map_locked_no_export,
    "check_T_w_trace_denner_sirlin_notation_map_bank_closure": check_T_w_trace_denner_sirlin_notation_map_bank_closure,
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
