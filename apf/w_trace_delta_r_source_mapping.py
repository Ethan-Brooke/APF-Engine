"""W_TRACE standard electroweak Delta_r source mapping.

Physics pivot module for v13.1.  This module changes the W_TRACE import
strategy from APF-slot-first payload hunting to standard electroweak
Delta_r-source acquisition first.  It admits either a total independent
Delta_r payload or the standard decomposition

    Delta_r = Delta_alpha - (c_W^2/s_W^2) Delta_rho + Delta_r_rem,

with APF's anchor Delta_r used only as a downstream comparison target.
No observed W mass, W residual, APF-anchor backsolve, or physical export is
permitted at this layer.
"""
from __future__ import annotations

import json
import math
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Tuple

STATUS = "P_w_delta_r_source_mapping"
VERSION = "w_trace_delta_r_source_mapping_v1"
PASS_STATUS = "W_TRACE_DELTA_R_SOURCE_MAPPING_BANK_PASS"
TITLE = "W_TRACE standard electroweak Delta_r source mapping"

M_W_TRACE_GEV = 80.362164334
APF_DELTA_R_TARGET = 3.64075266128216881e-2

STANDARD_DECOMPOSITION = ("Delta_alpha", "Delta_rho", "Delta_r_rem")
STANDARD_TOTAL = ("Delta_r_total",)
APF_LEGACY_COMPONENTS = (
    "Delta_alpha_run",
    "Delta_rho_oblique",
    "Delta_r_fermion_finite",
    "Delta_r_boson_finite",
    "Delta_r_vertex_box",
    "Delta_r_ct_OS",
    "Delta_r_covariance_pullback",
    "sigma_Delta_r_pushforward",
)

ALLOWED_PAYLOAD_KINDS = (
    "standard_delta_r_total",
    "standard_delta_r_decomposition",
    "standard_delta_r_parametrization",
)

CANDIDATE_SOURCE_CLASSES = {
    "precision_sm_mw_parametrization": {
        "kind": "standard_delta_r_parametrization",
        "examples": ("Awramik-Czakon-Freitas-Weiglein style W-mass/Delta-r source",),
        "may_output": ("Delta_r_total", "M_W_prediction_auxiliary"),
        "requires_no_observed_w_input": True,
    },
    "onshell_renormalization_review_or_table": {
        "kind": "standard_delta_r_decomposition",
        "examples": ("Denner-style on-shell renormalization/counterterm source",),
        "may_output": STANDARD_DECOMPOSITION,
        "requires_no_observed_w_input": True,
    },
    "direct_delta_r_table": {
        "kind": "standard_delta_r_total",
        "examples": ("reviewed table of independently evaluated Delta_r",),
        "may_output": STANDARD_TOTAL,
        "requires_no_observed_w_input": True,
    },
}

INPUT_SCHEME = {
    "alpha_em_reference": "allowed_non_W_input",
    "G_F_reference": "allowed_non_W_input",
    "M_Z_on_shell_reference": "allowed_non_W_input",
}

FORBIDDEN_TOKENS = (
    "observed_M_W_column",
    "M_W_world_average",
    "world_average_W_mass",
    "fit_residual",
    "W_mass_residual",
    "apf_anchor_delta_r_column",
    "APF_ANCHOR_DELTA_R_TARGET",
    "Delta_r_target_backsolve",
    "backsolve",
    "posthoc_counterterm_fit",
    "identity_W_TRACE_to_on_shell_M_W",
    "manual_unlock",
    "force_export",
    "physical_M_W_override",
)

LOCKED_EXPORT_STATE = {
    "standard_delta_r_source_mapping_banked": True,
    "real_standard_delta_r_source_admitted": False,
    "apf_legacy_eight_slot_decomposition_required_first": False,
    "apf_anchor_is_comparison_only": True,
    "physical_W_export_enabled": False,
    "exports_physical_M_W": False,
}


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _contains_forbidden_token(obj: Any) -> bool:
    text = _canonical_json(obj)
    return any(tok in text for tok in FORBIDDEN_TOKENS)


def _is_number(x: Any) -> bool:
    return isinstance(x, (int, float)) and math.isfinite(float(x))


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
        "strategy_shift": "standard_electroweak_delta_r_first_apf_slot_refinement_second",
        "standard_decomposition": {
            "formula": "Delta_r = Delta_alpha - (cW2/sW2)*Delta_rho + Delta_r_rem",
            "components": list(STANDARD_DECOMPOSITION),
            "allowed_total_payload": list(STANDARD_TOTAL),
        },
        "input_scheme": dict(INPUT_SCHEME),
        "candidate_source_classes": CANDIDATE_SOURCE_CLASSES,
        "apf_comparison_target": {
            "M_W_TRACE_GeV": M_W_TRACE_GEV,
            "Delta_r_APF_TRACE_target": APF_DELTA_R_TARGET,
            "use": "downstream_comparison_only_not_component_input",
        },
        "legacy_apf_components": list(APF_LEGACY_COMPONENTS),
        "locked_export_state": dict(LOCKED_EXPORT_STATE),
        "stop_rule": "Do not require the eight APF finite-part rows before admitting a standard independent Delta_r source; decompose later only if the source supports it.",
    }


def standard_delta_r_from_decomposition(delta_alpha: float, delta_rho: float, delta_r_rem: float, cW2_over_sW2: float) -> float:
    """Compute the standard on-shell decomposition value.

    This helper is algebra only.  It does not certify a source and does not use
    APF's comparison target or observed W data.
    """
    if not all(_is_number(x) for x in (delta_alpha, delta_rho, delta_r_rem, cW2_over_sW2)):
        raise ValueError("all decomposition arguments must be finite numeric values")
    if cW2_over_sW2 <= 0:
        raise ValueError("cW2_over_sW2 must be positive")
    return float(delta_alpha) - float(cW2_over_sW2) * float(delta_rho) + float(delta_r_rem)


def map_standard_payload(payload: Mapping[str, Any]) -> Dict[str, Any]:
    """Validate/map a standard Delta_r source payload.

    Accepted forms:
      - {'payload_kind': 'standard_delta_r_total', 'Delta_r_total': <num>, ...}
      - {'payload_kind': 'standard_delta_r_decomposition', 'Delta_alpha': <num>,
         'Delta_rho': <num>, 'Delta_r_rem': <num>, 'cW2_over_sW2': <num>, ...}
      - {'payload_kind': 'standard_delta_r_parametrization', 'parametrization_id': str,
         'outputs_independent_delta_r_total': bool, ...}
    """
    errors: List[str] = []
    if _contains_forbidden_token(payload):
        errors.append("forbidden_token_detected")
    if payload.get("uses_observed_M_W") is True:
        errors.append("observed_W_input_forbidden")
    if payload.get("uses_APF_anchor_delta_r") is True:
        errors.append("apf_anchor_input_forbidden")
    if payload.get("physical_export_requested") is True:
        errors.append("physical_export_request_forbidden")

    kind = payload.get("payload_kind")
    if kind not in ALLOWED_PAYLOAD_KINDS:
        errors.append("unknown_payload_kind")

    mapped: Dict[str, Any] = {
        "status": STATUS,
        "version": VERSION,
        "payload_kind": kind,
        "accepted_shape": False,
        "mapped_delta_r_total": None,
        "mapped_standard_components": {},
        "comparison_target_available_downstream": APF_DELTA_R_TARGET,
        "apf_anchor_is_input": False,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "errors": errors,
    }

    if kind == "standard_delta_r_total":
        if not _is_number(payload.get("Delta_r_total")):
            errors.append("Delta_r_total_required")
        else:
            mapped["mapped_delta_r_total"] = float(payload["Delta_r_total"])
            mapped["accepted_shape"] = True

    elif kind == "standard_delta_r_decomposition":
        missing = [k for k in (*STANDARD_DECOMPOSITION, "cW2_over_sW2") if k not in payload]
        bad_numeric = [k for k in (*STANDARD_DECOMPOSITION, "cW2_over_sW2") if k in payload and not _is_number(payload[k])]
        if missing:
            errors.append("missing_standard_decomposition_fields:" + ",".join(missing))
        if bad_numeric:
            errors.append("non_numeric_standard_decomposition_fields:" + ",".join(bad_numeric))
        if not missing and not bad_numeric:
            try:
                total = standard_delta_r_from_decomposition(
                    float(payload["Delta_alpha"]),
                    float(payload["Delta_rho"]),
                    float(payload["Delta_r_rem"]),
                    float(payload["cW2_over_sW2"]),
                )
                mapped["mapped_delta_r_total"] = total
                mapped["mapped_standard_components"] = {k: float(payload[k]) for k in STANDARD_DECOMPOSITION}
                mapped["accepted_shape"] = True
            except ValueError as exc:
                errors.append(str(exc))

    elif kind == "standard_delta_r_parametrization":
        if not isinstance(payload.get("parametrization_id"), str) or not payload.get("parametrization_id"):
            errors.append("parametrization_id_required")
        if payload.get("outputs_independent_delta_r_total") is not True:
            errors.append("independent_delta_r_output_attestation_required")
        if not any(e.startswith("parametrization") or e.startswith("independent") for e in errors):
            mapped["accepted_shape"] = True
            mapped["mapped_delta_r_total"] = "deferred_to_parametrization_evaluator"

    mapped["valid"] = bool(mapped["accepted_shape"] and not errors)
    return mapped


def compare_to_apf_target(mapped_payload: Mapping[str, Any]) -> Dict[str, Any]:
    """Downstream comparison helper; never part of source admission."""
    val = mapped_payload.get("mapped_delta_r_total")
    if not _is_number(val):
        return {
            "comparison_available": False,
            "reason": "no_numeric_independent_delta_r_total",
            "physical_W_export_enabled": False,
            "exports_physical_M_W": False,
        }
    residual = float(val) - APF_DELTA_R_TARGET
    return {
        "comparison_available": True,
        "delta_r_source": float(val),
        "delta_r_apf_trace_target": APF_DELTA_R_TARGET,
        "source_minus_apf_target": residual,
        "apf_anchor_role": "comparison_only",
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
    }


def check_T_w_trace_delta_r_source_mapping_status_declared():
    return _res("status_declared", STATUS == "P_w_delta_r_source_mapping" and VERSION == "w_trace_delta_r_source_mapping_v1")


def check_T_w_trace_delta_r_source_mapping_strategy_shift_declared():
    r = terminal_report()
    return _res("strategy_shift_declared", "standard_electroweak_delta_r_first" in r["strategy_shift"])


def check_T_w_trace_delta_r_source_mapping_standard_decomposition_declared():
    r = terminal_report()["standard_decomposition"]
    return _res("standard_decomposition_declared", tuple(r["components"]) == STANDARD_DECOMPOSITION and "Delta_alpha" in r["formula"])


def check_T_w_trace_delta_r_source_mapping_total_payload_allowed():
    r = map_standard_payload({"payload_kind": "standard_delta_r_total", "Delta_r_total": 0.036, "uses_observed_M_W": False})
    return _res("total_payload_allowed", r["valid"] and r["mapped_delta_r_total"] == 0.036)


def check_T_w_trace_delta_r_source_mapping_decomposition_payload_allowed():
    r = map_standard_payload({"payload_kind": "standard_delta_r_decomposition", "Delta_alpha": 0.059, "Delta_rho": 0.009, "Delta_r_rem": 0.008, "cW2_over_sW2": 3.3})
    expected = 0.059 - 3.3 * 0.009 + 0.008
    return _res("decomposition_payload_allowed", r["valid"] and abs(r["mapped_delta_r_total"] - expected) < 1e-15)


def check_T_w_trace_delta_r_source_mapping_parametrization_payload_allowed():
    r = map_standard_payload({"payload_kind": "standard_delta_r_parametrization", "parametrization_id": "reviewed_mw_delta_r_param_v1", "outputs_independent_delta_r_total": True})
    return _res("parametrization_payload_allowed", r["valid"] and r["mapped_delta_r_total"] == "deferred_to_parametrization_evaluator")


def check_T_w_trace_delta_r_source_mapping_legacy_eight_slot_not_required_first():
    r = terminal_report()
    return _res("legacy_eight_slot_not_required_first", r["locked_export_state"]["apf_legacy_eight_slot_decomposition_required_first"] is False)


def check_T_w_trace_delta_r_source_mapping_apf_anchor_comparison_only():
    r = map_standard_payload({"payload_kind": "standard_delta_r_total", "Delta_r_total": 0.036})
    c = compare_to_apf_target(r)
    return _res("apf_anchor_comparison_only", r["apf_anchor_is_input"] is False and c["apf_anchor_role"] == "comparison_only")


def check_T_w_trace_delta_r_source_mapping_observed_w_forbidden():
    r = map_standard_payload({"payload_kind": "standard_delta_r_total", "Delta_r_total": 0.036, "uses_observed_M_W": True})
    return _res("observed_w_forbidden", not r["valid"] and "observed_W_input_forbidden" in r["errors"])


def check_T_w_trace_delta_r_source_mapping_apf_anchor_input_forbidden():
    r = map_standard_payload({"payload_kind": "standard_delta_r_total", "Delta_r_total": 0.036, "uses_APF_anchor_delta_r": True})
    return _res("apf_anchor_input_forbidden", not r["valid"] and "apf_anchor_input_forbidden" in r["errors"])


def check_T_w_trace_delta_r_source_mapping_forbidden_token_scan():
    r = map_standard_payload({"payload_kind": "standard_delta_r_total", "Delta_r_total": 0.036, "note": "Delta_r_target_backsolve"})
    return _res("forbidden_token_scan", not r["valid"] and "forbidden_token_detected" in r["errors"])


def check_T_w_trace_delta_r_source_mapping_physical_export_locked():
    r = terminal_report()["locked_export_state"]
    return _res("physical_export_locked", r["physical_W_export_enabled"] is False and r["exports_physical_M_W"] is False)


def check_T_w_trace_delta_r_source_mapping_candidate_source_classes_declared():
    return _res("candidate_source_classes_declared", set(CANDIDATE_SOURCE_CLASSES) == {"precision_sm_mw_parametrization", "onshell_renormalization_review_or_table", "direct_delta_r_table"})


def check_T_w_trace_delta_r_source_mapping_input_scheme_preserved():
    return _res("input_scheme_preserved", set(INPUT_SCHEME) == {"alpha_em_reference", "G_F_reference", "M_Z_on_shell_reference"})


def check_T_w_trace_delta_r_source_mapping_missing_component_rejected():
    r = map_standard_payload({"payload_kind": "standard_delta_r_decomposition", "Delta_alpha": 0.059, "Delta_rho": 0.009, "cW2_over_sW2": 3.3})
    return _res("missing_component_rejected", not r["valid"] and any(e.startswith("missing_standard_decomposition_fields") for e in r["errors"]))


def check_T_w_trace_delta_r_source_mapping_bad_ratio_rejected():
    r = map_standard_payload({"payload_kind": "standard_delta_r_decomposition", "Delta_alpha": 0.059, "Delta_rho": 0.009, "Delta_r_rem": 0.008, "cW2_over_sW2": -1.0})
    return _res("bad_ratio_rejected", not r["valid"] and any("positive" in e for e in r["errors"]))


def check_T_w_trace_delta_r_source_mapping_comparison_no_export():
    r = map_standard_payload({"payload_kind": "standard_delta_r_total", "Delta_r_total": 0.036})
    c = compare_to_apf_target(r)
    return _res("comparison_no_export", c["comparison_available"] is True and c["physical_W_export_enabled"] is False and c["exports_physical_M_W"] is False)


def check_T_w_trace_delta_r_source_mapping_serializable():
    json.dumps(terminal_report(), sort_keys=True)
    r = map_standard_payload({"payload_kind": "standard_delta_r_total", "Delta_r_total": 0.036})
    json.dumps(r, sort_keys=True)
    return _res("serializable", True)


CHECKS = {
    "T_w_trace_delta_r_source_mapping_status_declared": check_T_w_trace_delta_r_source_mapping_status_declared,
    "T_w_trace_delta_r_source_mapping_strategy_shift_declared": check_T_w_trace_delta_r_source_mapping_strategy_shift_declared,
    "T_w_trace_delta_r_source_mapping_standard_decomposition_declared": check_T_w_trace_delta_r_source_mapping_standard_decomposition_declared,
    "T_w_trace_delta_r_source_mapping_total_payload_allowed": check_T_w_trace_delta_r_source_mapping_total_payload_allowed,
    "T_w_trace_delta_r_source_mapping_decomposition_payload_allowed": check_T_w_trace_delta_r_source_mapping_decomposition_payload_allowed,
    "T_w_trace_delta_r_source_mapping_parametrization_payload_allowed": check_T_w_trace_delta_r_source_mapping_parametrization_payload_allowed,
    "T_w_trace_delta_r_source_mapping_legacy_eight_slot_not_required_first": check_T_w_trace_delta_r_source_mapping_legacy_eight_slot_not_required_first,
    "T_w_trace_delta_r_source_mapping_apf_anchor_comparison_only": check_T_w_trace_delta_r_source_mapping_apf_anchor_comparison_only,
    "T_w_trace_delta_r_source_mapping_observed_w_forbidden": check_T_w_trace_delta_r_source_mapping_observed_w_forbidden,
    "T_w_trace_delta_r_source_mapping_apf_anchor_input_forbidden": check_T_w_trace_delta_r_source_mapping_apf_anchor_input_forbidden,
    "T_w_trace_delta_r_source_mapping_forbidden_token_scan": check_T_w_trace_delta_r_source_mapping_forbidden_token_scan,
    "T_w_trace_delta_r_source_mapping_physical_export_locked": check_T_w_trace_delta_r_source_mapping_physical_export_locked,
    "T_w_trace_delta_r_source_mapping_candidate_source_classes_declared": check_T_w_trace_delta_r_source_mapping_candidate_source_classes_declared,
    "T_w_trace_delta_r_source_mapping_input_scheme_preserved": check_T_w_trace_delta_r_source_mapping_input_scheme_preserved,
    "T_w_trace_delta_r_source_mapping_missing_component_rejected": check_T_w_trace_delta_r_source_mapping_missing_component_rejected,
    "T_w_trace_delta_r_source_mapping_bad_ratio_rejected": check_T_w_trace_delta_r_source_mapping_bad_ratio_rejected,
    "T_w_trace_delta_r_source_mapping_comparison_no_export": check_T_w_trace_delta_r_source_mapping_comparison_no_export,
    "T_w_trace_delta_r_source_mapping_serializable": check_T_w_trace_delta_r_source_mapping_serializable,
}
_CHECKS = CHECKS


def check_T_w_trace_delta_r_source_mapping_bank_closure():
    rows = [fn() for name, fn in CHECKS.items() if not name.endswith("_bank_closure")]
    ok = all(_passed(r) for r in rows) and len(rows) == 18
    return _res("bank_closure", ok, checked=len(rows), failed=[r.get("check") for r in rows if not _passed(r)])


CHECKS["T_w_trace_delta_r_source_mapping_bank_closure"] = check_T_w_trace_delta_r_source_mapping_bank_closure
_CHECKS = CHECKS


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
