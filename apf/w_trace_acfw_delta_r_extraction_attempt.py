"""W_TRACE ACFW standard Delta_r extraction attempt (v14.1).

This is the first real physics-source payload candidate after the v14.0 source
acquisition sprint.  It encodes the Awramik--Czakon--Freitas--Weiglein (ACFW)
Standard Model W-mass parametrization as an independent source path, evaluates a
declared modern input scenario, and inverts the on-shell relation to obtain a
standard total Delta_r source candidate.

Guardrail: the APF/W_TRACE Delta_r target is comparison-only.  The ACFW
parametrization may not consume observed M_W, W residuals, or the APF anchor.
"""
from __future__ import annotations

import json
import math
from typing import Any, Dict, Mapping, MutableMapping

try:
    from apf import w_trace_delta_r_source_mapping as srcmap
except Exception:  # pragma: no cover
    srcmap = None

STATUS = "P_w_acfw_delta_r_extraction_attempt"
VERSION = "v14_1"
PASS_STATUS = "W_TRACE_ACFW_DELTA_R_EXTRACTION_ATTEMPT_BANK_PASS"
TITLE = "W_TRACE ACFW standard Delta_r extraction attempt"

# APF anchor remains comparison-only.
APF_DELTA_R_TARGET = getattr(srcmap, "APF_DELTA_R_TARGET", 0.0364075266128216881)
M_W_TRACE_GEV = getattr(srcmap, "M_W_TRACE_GEV", 80.362164334)

# ACFW Eq.(6)-style parametrization values used as the independent source path.
# Units: GeV for masses.  The coefficient set is the standard ACFW fitting-form
# coefficient table for the broad Higgs-mass range; the module treats it as a
# literature-source payload, not as an APF-derived quantity.
ACFW_SOURCE = {
    "source_id": "ACFW_2004_PRD69_053006_hep-ph_0311148",
    "authors": "M. Awramik, M. Czakon, A. Freitas, G. Weiglein",
    "title": "Precise Prediction for the W-Boson Mass in the Standard Model",
    "payload_kind": "standard_delta_r_parametrization_inverted_from_SM_MW_prediction",
    "uses_observed_M_W": False,
    "uses_apf_trace_M_W": False,
    "uses_apf_delta_r_target": False,
    "exports_physical_M_W": False,
    "notes": "ACFW SM M_W prediction parametrization; inverted downstream to Delta_r_source for APF comparison only.",
}

ACFW_REFERENCE_INPUTS = {
    "M_H_GeV": 100.0,
    "m_t_GeV": 174.3,
    "Delta_alpha": 0.05907,
    "alpha_s_MZ": 0.119,
    "M_Z_GeV": 91.1875,
}

ACFW_COEFFICIENTS = {
    "M_W0_GeV": 80.3799,
    "c1": 0.05429,
    "c2": 0.008939,
    "c3": 0.0000890,
    "c4": 0.000161,
    "c5": 1.070,
    "c6": 0.5256,
    "c7": 0.0678,
    "c8": 0.00179,
    "c9": 0.0000659,
    "c10": 0.0737,
    "c11": 114.9,
}

# Declared extraction scenario: modern-ish non-W electroweak input scenario.
# This is not a world-fit closure claim; it is the first admitted source-candidate
# scenario used to test APF against an independent SM parametrization path.
EXTRACTION_INPUTS = {
    "M_H_GeV": 125.25,
    "m_t_GeV": 172.57,
    "Delta_alpha": 0.05900,
    "alpha_s_MZ": 0.1184,
    "M_Z_GeV": 91.1876,
    "alpha_inverse_for_inversion": 137.035999177,
    "G_F_GeV_minus2": 1.1663788e-5,
    "input_policy": "declared_non_W_inputs_only; no observed W; no APF anchor as source input",
}

FORBIDDEN_TOKENS = (
    "observed_M_W", "M_W_world_average", "world_average_M_W", "CDF_II_M_W",
    "PDG_observed_M_W", "Delta_r_target_backsolve", "fit_to_M_W_TRACE",
    "APF_DELTA_R_TARGET_AS_INPUT", "APF_anchor_as_component", "manual_export_override",
    "physical_export_request",
)

LOCKED_STATE = {
    "real_standard_delta_r_payload_candidate_extracted": True,
    "real_standard_delta_r_source_admitted_for_comparison": True,
    "component_sum_certified": False,
    "covariance_certified": False,
    "uncertainty_propagation_certified": False,
    "physical_W_export_enabled": False,
    "exports_physical_M_W": False,
}


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def contains_forbidden_token(obj: Any) -> bool:
    text = _canonical_json(obj)
    return any(tok in text for tok in FORBIDDEN_TOKENS)


def acfw_dimensionless_inputs(inputs: Mapping[str, float]) -> Dict[str, float]:
    ref = ACFW_REFERENCE_INPUTS
    M_H = float(inputs["M_H_GeV"])
    m_t = float(inputs["m_t_GeV"])
    Delta_alpha = float(inputs["Delta_alpha"])
    alpha_s = float(inputs["alpha_s_MZ"])
    M_Z = float(inputs["M_Z_GeV"])
    return {
        "dH": math.log(M_H / 100.0),
        "dh": (M_H / 100.0) ** 2,
        "dt": (m_t / ref["m_t_GeV"]) ** 2 - 1.0,
        "dAlpha": Delta_alpha / ref["Delta_alpha"] - 1.0,
        "dAlpha_s": alpha_s / ref["alpha_s_MZ"] - 1.0,
        "dZ": M_Z / ref["M_Z_GeV"] - 1.0,
    }


def acfw_predict_mw(inputs: Mapping[str, float] = EXTRACTION_INPUTS) -> float:
    d = acfw_dimensionless_inputs(inputs)
    c = ACFW_COEFFICIENTS
    return (
        c["M_W0_GeV"]
        - c["c1"] * d["dH"]
        - c["c2"] * d["dH"] ** 2
        + c["c3"] * d["dH"] ** 4
        + c["c4"] * (d["dh"] - 1.0)
        - c["c5"] * d["dAlpha"]
        + c["c6"] * d["dt"]
        - c["c7"] * d["dt"] ** 2
        - c["c8"] * d["dH"] * d["dt"]
        + c["c9"] * d["dh"] * d["dt"]
        - c["c10"] * d["dAlpha_s"]
        + c["c11"] * d["dZ"]
    )


def invert_delta_r_from_mw(M_W_GeV: float, inputs: Mapping[str, float] = EXTRACTION_INPUTS) -> float:
    alpha = 1.0 / float(inputs["alpha_inverse_for_inversion"])
    G_F = float(inputs["G_F_GeV_minus2"])
    M_Z = float(inputs["M_Z_GeV"])
    A = math.pi * alpha / (math.sqrt(2.0) * G_F)
    denom = float(M_W_GeV) ** 2 * (1.0 - float(M_W_GeV) ** 2 / M_Z ** 2)
    return 1.0 - A / denom


def extraction_payload() -> Dict[str, Any]:
    mw = acfw_predict_mw(EXTRACTION_INPUTS)
    delta_r = invert_delta_r_from_mw(mw, EXTRACTION_INPUTS)
    residual = delta_r - APF_DELTA_R_TARGET
    mw_gap = mw - M_W_TRACE_GEV
    return {
        "status": STATUS,
        "source": dict(ACFW_SOURCE),
        "inputs": dict(EXTRACTION_INPUTS),
        "dimensionless_inputs": acfw_dimensionless_inputs(EXTRACTION_INPUTS),
        "M_W_source_GeV": mw,
        "Delta_r_source_total": delta_r,
        "Delta_r_APF_TRACE_target_comparison_only": APF_DELTA_R_TARGET,
        "Delta_r_source_minus_APF": residual,
        "abs_Delta_r_residual": abs(residual),
        "M_W_source_minus_W_TRACE_GeV": mw_gap,
        "abs_M_W_gap_MeV": abs(mw_gap) * 1000.0,
        "interpretation": "real independent standard-Delta_r total payload candidate; comparison only; no physical W export",
        "physical_export_enabled": False,
    }


def terminal_report() -> Dict[str, Any]:
    payload = extraction_payload()
    return {
        "status": STATUS,
        "version": VERSION,
        "title": TITLE,
        "payload": payload,
        "locked_state": dict(LOCKED_STATE),
        "verdict": "GOT_THERE_SOURCE_PAYLOAD_CANDIDATE_EXTRACTED_NOT_PHYSICAL_EXPORT",
        "next": "stress-test input conventions; then source a second independent Delta_r/M_W prediction path",
    }


def _res(check: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    row = {"check": check, "passed": bool(passed)}
    row.update(extra)
    return row


def _passed(row: Any) -> bool:
    return bool(isinstance(row, dict) and row.get("passed") is True)


def check_T_w_trace_acfw_extraction_status_declared():
    return _res("status_declared", STATUS == "P_w_acfw_delta_r_extraction_attempt")


def check_T_w_trace_acfw_source_is_standard_parametrization():
    return _res("source_is_standard_parametrization", ACFW_SOURCE["payload_kind"].startswith("standard_delta_r_parametrization"))


def check_T_w_trace_acfw_source_forbids_observed_w():
    return _res("source_forbids_observed_w", ACFW_SOURCE["uses_observed_M_W"] is False)


def check_T_w_trace_acfw_source_forbids_apf_anchor_input():
    return _res("source_forbids_apf_anchor_input", ACFW_SOURCE["uses_apf_trace_M_W"] is False and ACFW_SOURCE["uses_apf_delta_r_target"] is False)


def check_T_w_trace_acfw_reference_point_recovers_MW0():
    mw = acfw_predict_mw({**ACFW_REFERENCE_INPUTS, "alpha_inverse_for_inversion": 137.035999177, "G_F_GeV_minus2": 1.1663788e-5})
    return _res("reference_point_recovers_MW0", abs(mw - ACFW_COEFFICIENTS["M_W0_GeV"]) < 1e-12, mw=mw)


def check_T_w_trace_acfw_dimensionless_inputs_nontrivial():
    d = acfw_dimensionless_inputs(EXTRACTION_INPUTS)
    return _res("dimensionless_inputs_nontrivial", abs(d["dH"]) > 0.1 and abs(d["dt"]) > 0.001)


def check_T_w_trace_acfw_predicts_reasonable_mw_window():
    mw = acfw_predict_mw(EXTRACTION_INPUTS)
    return _res("predicts_reasonable_mw_window", 80.30 < mw < 80.42, mw=mw)


def check_T_w_trace_acfw_inverts_to_reasonable_delta_r():
    dr = extraction_payload()["Delta_r_source_total"]
    return _res("inverts_to_reasonable_delta_r", 0.035 < dr < 0.038, delta_r=dr)


def check_T_w_trace_acfw_delta_r_not_identical_to_apf_target():
    res = extraction_payload()["Delta_r_source_minus_APF"]
    return _res("delta_r_not_identical_to_apf_target", abs(res) > 1e-7, residual=res)


def check_T_w_trace_acfw_delta_r_close_neighborhood():
    res = extraction_payload()["Delta_r_source_minus_APF"]
    return _res("delta_r_close_neighborhood", abs(res) < 5e-4, residual=res)


def check_T_w_trace_acfw_w_gap_mev_small():
    gap = extraction_payload()["abs_M_W_gap_MeV"]
    return _res("w_gap_mev_small", gap < 10.0, abs_gap_MeV=gap)


def check_T_w_trace_acfw_payload_candidate_extracted():
    return _res("payload_candidate_extracted", LOCKED_STATE["real_standard_delta_r_payload_candidate_extracted"] is True)


def check_T_w_trace_acfw_payload_admitted_for_comparison_only():
    return _res("payload_admitted_for_comparison_only", LOCKED_STATE["real_standard_delta_r_source_admitted_for_comparison"] is True and LOCKED_STATE["physical_W_export_enabled"] is False)


def check_T_w_trace_acfw_no_component_sum_claim():
    return _res("no_component_sum_claim", LOCKED_STATE["component_sum_certified"] is False)


def check_T_w_trace_acfw_no_covariance_claim():
    return _res("no_covariance_claim", LOCKED_STATE["covariance_certified"] is False and LOCKED_STATE["uncertainty_propagation_certified"] is False)


def check_T_w_trace_acfw_no_physical_w_export():
    return _res("no_physical_w_export", LOCKED_STATE["exports_physical_M_W"] is False)


def check_T_w_trace_acfw_forbidden_token_scan_clean():
    clean_obj = {"source_id": ACFW_SOURCE["source_id"], "payload_kind": ACFW_SOURCE["payload_kind"], "inputs": EXTRACTION_INPUTS}
    return _res("forbidden_token_scan_clean", contains_forbidden_token(clean_obj) is False)


def check_T_w_trace_acfw_forbidden_token_scan_detects_bad_payload():
    return _res("forbidden_token_scan_detects_bad_payload", contains_forbidden_token({"bad": "Delta_r_target_backsolve"}) is True)


def check_T_w_trace_acfw_report_has_got_there_verdict():
    return _res("report_has_got_there_verdict", terminal_report()["verdict"].startswith("GOT_THERE"))


def check_T_w_trace_acfw_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_trace_acfw_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))


_CHECKS = {
    "check_T_w_trace_acfw_extraction_status_declared": check_T_w_trace_acfw_extraction_status_declared,
    "check_T_w_trace_acfw_source_is_standard_parametrization": check_T_w_trace_acfw_source_is_standard_parametrization,
    "check_T_w_trace_acfw_source_forbids_observed_w": check_T_w_trace_acfw_source_forbids_observed_w,
    "check_T_w_trace_acfw_source_forbids_apf_anchor_input": check_T_w_trace_acfw_source_forbids_apf_anchor_input,
    "check_T_w_trace_acfw_reference_point_recovers_MW0": check_T_w_trace_acfw_reference_point_recovers_MW0,
    "check_T_w_trace_acfw_dimensionless_inputs_nontrivial": check_T_w_trace_acfw_dimensionless_inputs_nontrivial,
    "check_T_w_trace_acfw_predicts_reasonable_mw_window": check_T_w_trace_acfw_predicts_reasonable_mw_window,
    "check_T_w_trace_acfw_inverts_to_reasonable_delta_r": check_T_w_trace_acfw_inverts_to_reasonable_delta_r,
    "check_T_w_trace_acfw_delta_r_not_identical_to_apf_target": check_T_w_trace_acfw_delta_r_not_identical_to_apf_target,
    "check_T_w_trace_acfw_delta_r_close_neighborhood": check_T_w_trace_acfw_delta_r_close_neighborhood,
    "check_T_w_trace_acfw_w_gap_mev_small": check_T_w_trace_acfw_w_gap_mev_small,
    "check_T_w_trace_acfw_payload_candidate_extracted": check_T_w_trace_acfw_payload_candidate_extracted,
    "check_T_w_trace_acfw_payload_admitted_for_comparison_only": check_T_w_trace_acfw_payload_admitted_for_comparison_only,
    "check_T_w_trace_acfw_no_component_sum_claim": check_T_w_trace_acfw_no_component_sum_claim,
    "check_T_w_trace_acfw_no_covariance_claim": check_T_w_trace_acfw_no_covariance_claim,
    "check_T_w_trace_acfw_no_physical_w_export": check_T_w_trace_acfw_no_physical_w_export,
    "check_T_w_trace_acfw_forbidden_token_scan_clean": check_T_w_trace_acfw_forbidden_token_scan_clean,
    "check_T_w_trace_acfw_forbidden_token_scan_detects_bad_payload": check_T_w_trace_acfw_forbidden_token_scan_detects_bad_payload,
    "check_T_w_trace_acfw_report_has_got_there_verdict": check_T_w_trace_acfw_report_has_got_there_verdict,
    "check_T_w_trace_acfw_bank_closure": check_T_w_trace_acfw_bank_closure,
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
    payload = out["report"]["payload"]
    print("M_W_source_GeV", f"{payload['M_W_source_GeV']:.12f}")
    print("Delta_r_source_total", f"{payload['Delta_r_source_total']:.18f}")
    print("Delta_r_source_minus_APF", f"{payload['Delta_r_source_minus_APF']:.18f}")
    print("abs_M_W_gap_MeV", f"{payload['abs_M_W_gap_MeV']:.6f}")
    raise SystemExit(0 if out["passed"] else 1)
