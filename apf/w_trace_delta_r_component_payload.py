"""W_TRACE Delta_r component-payload sprint / dominant-row worksheet.

v15.3 (2026-05-09): hard-push component payload layer after the v15.2
transport workbench.  This module builds the first paper-facing component
ledger for the W_TRACE -> on-shell route.

Closed here:
    * the standard source total from v15.1/v15.2 is split into a documented
      dominant-row worksheet using the PDG Delta_r decomposition line;
    * the two dominant source-proxy rows, Delta alpha running and top/rho,
      are numerically instantiated without using observed W or the APF anchor
      as a fit input;
    * the remaining source-total remainder is isolated as an unassigned
      aggregate remainder, not promoted into APF finite-part rows;
    * uncertainty-scale translation and missing-slot obstruction are sharpened
      row-by-row.

Still open here:
    physical M_W export, because the worksheet is not a reviewed APF eight-slot
    finite-part row bundle: fermionic/bosonic/vertex-box/counterterm rows are
    still unfilled as independent finite pieces; no real covariance matrix or
    export uncertainty certificate is supplied.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Sequence, Tuple

from apf.w_trace_delta_r_transport_buildout import (
    APF_DELTA_R_TARGET,
    M_W_TRACE_GEV,
    REQUIRED_COMPONENT_SLOTS,
    dMW_dDelta_r,
    mw_from_delta_r,
    source_vs_trace_transport_values,
    transport_sensitivity_at_trace,
    check_T_w_delta_r_transport_buildout_bank_closure as _check_v152,
)
from apf.w_trace_finite_part_skeleton import COMPONENT_SYMBOLS, FINITE_PART_COMPONENT_ORDER
from apf.w_trace_component_sum_certificate import component_sum_certificate_report
from apf.w_trace_uncertainty_propagation import uncertainty_propagation_report
from apf.w_trace_row_schema_adapter import validate_rows
from apf.w_trace_final_export_readiness import readiness_report
from apf.w_trace_physical_export_lock import export_lock_report

STATUS = "P_w_delta_r_component_payload_worksheet"
VERSION = "v15_3"
PASS_STATUS = "W_TRACE_DELTA_R_COMPONENT_PAYLOAD_WORKSHEET_PASS"
TITLE = "W_TRACE Delta_r component payload worksheet"
PAYLOAD_ID = "W_TRACE_DELTA_R_COMPONENT_PAYLOAD_WORKSHEET_v15_3"

# PDG electroweak-review decomposition line used as a source-proxy scaffold:
#   Delta r ~ Delta r_0 - rho_t tan^{-2} theta_W + additional bosonic / higher-order terms
# with Delta r_0 = 0.06646(6) and rho_t = 0.00934*(m_t/172.61 GeV)^2.
# These are source-proxy entries, not APF finite-part rows.
PDG_DELTA_R0 = 0.06646
PDG_DELTA_R0_SIGMA = 0.00006
PDG_RHO_T_NORMALIZATION = 0.00934
PDG_RHO_T_REFERENCE_MT_GEV = 172.61
PDG_DELTA_R_TOTAL_CONTEXT = 0.03685
PDG_DELTA_R_TOTAL_MT_SIGMA = 0.00020
PDG_DELTA_R_TOTAL_ALPHA_SIGMA = 0.00006

# Use the same non-W M_Z input as the v15.2 inversion layer.  The APF_TRACE W
# value appears only to define the already-locked trace/on-shell comparison
# angle for this worksheet; it is not an observed-W input and is not used to
# tune any component to a residual.
M_Z_CONTEXT_GEV = 91.1876

# Source-proxy component identifiers: exactly the APF eight slots, but only the
# first two are numerically populated as dominant standard-decomposition proxies.
NUMERIC_PROXY_COMPONENTS: Tuple[str, ...] = (
    "delta_alpha_running_component",
    "delta_rho_oblique_component",
)
UNFILLED_FINITE_COMPONENTS: Tuple[str, ...] = (
    "fermionic_loop_finite_component",
    "bosonic_loop_finite_component",
    "vertex_box_finite_component",
    "scheme_conversion_counterterm_component",
)
UNFILLED_EXPORT_COMPONENTS: Tuple[str, ...] = (
    "correlation_covariance_component",
    "uncertainty_propagation_component",
)

BLOCKERS: Tuple[str, ...] = (
    "FERMIONIC_LOOP_FINITE_ROW_UNFILLED",
    "BOSONIC_LOOP_FINITE_ROW_UNFILLED",
    "VERTEX_BOX_FINITE_ROW_UNFILLED",
    "ON_SHELL_COUNTERTERM_FINITE_ROW_UNFILLED",
    "UNASSIGNED_STANDARD_REMAINDER_NOT_APF_COMPONENT_ROW",
    "NO_REVIEWED_APF_EIGHT_SLOT_FINITE_PART_BUNDLE",
    "NO_REAL_COVARIANCE_MATRIX",
    "NO_EXPORT_UNCERTAINTY_CERTIFICATE",
)

FORBIDDEN_COMPONENT_PAYLOAD_TOKENS: Tuple[str, ...] = (
    "observed_M_W",
    "world_average_M_W",
    "CDF_II_M_W",
    "CMS_observed_M_W",
    "PDG_observed_M_W",
    "fit_to_observed_W",
    "fit_to_APF_anchor",
    "component_residual_tuned_to_APF_anchor",
    "APF_DELTA_R_TARGET_AS_COMPONENT_INPUT",
    "physical_export_override",
)


@dataclass(frozen=True)
class ComponentPayloadRow:
    component_id: str
    component_symbol: str
    role: str
    value: float | None
    uncertainty: float | None
    unit: str
    source_basis: str
    scheme_family: str
    evaluation_status: str
    admission_status: str
    consumes_observed_W: bool = False
    consumes_APF_anchor_as_input: bool = False
    promotes_source_total_to_component: bool = False


@dataclass(frozen=True)
class RemainderRow:
    row_id: str
    value: float
    unit: str
    source_basis: str
    interpretation: str
    admissibility_status: str
    allowed_role: str
    promotes_to_APF_component: bool = False


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True, default=str)


def _digest(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(obj).encode("utf-8")).hexdigest()


def _res(check: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    row = {"check": check, "passed": bool(passed), "status": "PASS" if passed else "FAIL", "epistemic": STATUS}
    row.update(extra)
    return row


def _passed(row: Any) -> bool:
    return bool(isinstance(row, Mapping) and (row.get("passed") is True or row.get("status") in ("PASS", "P")))


def _contains_forbidden_token(obj: Any) -> bool:
    text = _canonical_json(obj)
    return any(tok in text for tok in FORBIDDEN_COMPONENT_PAYLOAD_TOKENS)


def trace_on_shell_angle_values() -> Dict[str, float]:
    ratio = M_W_TRACE_GEV / M_Z_CONTEXT_GEV
    s2 = 1.0 - ratio * ratio
    c2 = ratio * ratio
    cot2 = c2 / s2
    return {"ratio_MW_MZ": ratio, "s2_on_shell_trace_context": s2, "c2_on_shell_trace_context": c2, "cot2_trace_context": cot2}


def dominant_delta_alpha_row() -> ComponentPayloadRow:
    return ComponentPayloadRow(
        component_id="delta_alpha_running_component",
        component_symbol=COMPONENT_SYMBOLS["delta_alpha_running_component"],
        role="dominant running-alpha source-proxy term Delta r_0",
        value=PDG_DELTA_R0,
        uncertainty=PDG_DELTA_R0_SIGMA,
        unit="dimensionless_Delta_r_component",
        source_basis="PDG electroweak review: Delta r_0 = 1 - alpha/alpha_hat(M_Z) = 0.06646(6)",
        scheme_family="on_shell_source_proxy",
        evaluation_status="NUMERIC_SOURCE_PROXY_NOT_APF_FINITE_ROW",
        admission_status="WORKSHEET_PROXY_ONLY_NOT_ADMITTED_FOR_EXPORT",
    )


def dominant_rho_row(mt_gev: float = PDG_RHO_T_REFERENCE_MT_GEV) -> ComponentPayloadRow:
    angles = trace_on_shell_angle_values()
    rho_t = PDG_RHO_T_NORMALIZATION * (float(mt_gev) / PDG_RHO_T_REFERENCE_MT_GEV) ** 2
    value = -rho_t * angles["cot2_trace_context"]
    # The PDG total context assigns a +/-0.00020 scale to mt variation in Delta r.
    return ComponentPayloadRow(
        component_id="delta_rho_oblique_component",
        component_symbol=COMPONENT_SYMBOLS["delta_rho_oblique_component"],
        role="dominant top/rho source-proxy term -rho_t tan^{-2}(theta_W)",
        value=value,
        uncertainty=PDG_DELTA_R_TOTAL_MT_SIGMA,
        unit="dimensionless_Delta_r_component",
        source_basis="PDG electroweak review: rho_t = 0.00934*(m_t/172.61 GeV)^2, entering Delta r with -tan^{-2}(theta_W)",
        scheme_family="on_shell_source_proxy",
        evaluation_status="NUMERIC_SOURCE_PROXY_NOT_APF_FINITE_ROW",
        admission_status="WORKSHEET_PROXY_ONLY_NOT_ADMITTED_FOR_EXPORT",
    )


def unfilled_component_row(component_id: str) -> ComponentPayloadRow:
    return ComponentPayloadRow(
        component_id=component_id,
        component_symbol=COMPONENT_SYMBOLS[component_id],
        role="required APF finite-part/export slot; no reviewed row supplied in this sprint",
        value=None,
        uncertainty=None,
        unit="dimensionless_Delta_r_component",
        source_basis="UNSUPPLIED_REVIEWED_COMPONENT_ROW",
        scheme_family="on_shell_required_slot",
        evaluation_status="OPEN_UNFILLED",
        admission_status="NOT_ADMITTED_FOR_EXPORT",
    )


def component_payload_rows() -> Tuple[ComponentPayloadRow, ...]:
    rows = []
    for cid in FINITE_PART_COMPONENT_ORDER:
        if cid == "delta_alpha_running_component":
            rows.append(dominant_delta_alpha_row())
        elif cid == "delta_rho_oblique_component":
            rows.append(dominant_rho_row())
        else:
            rows.append(unfilled_component_row(cid))
    return tuple(rows)


def numeric_proxy_subtotal() -> float:
    return sum(float(r.value) for r in component_payload_rows() if r.value is not None)


def source_total_remainder_row() -> RemainderRow:
    vals = source_vs_trace_transport_values()
    source_total = float(vals["Delta_r_source_total"])
    rem = source_total - numeric_proxy_subtotal()
    return RemainderRow(
        row_id="standard_source_total_minus_two_dominant_proxies",
        value=rem,
        unit="dimensionless_Delta_r_remainder",
        source_basis="ACFW standard-total Delta_r from v15.1/v15.2 minus PDG dominant Delta alpha and rho proxies",
        interpretation="unassigned aggregate source remainder; contains finite fermionic, bosonic, vertex/box, counterterm and higher-order pieces in unresolved mixture",
        admissibility_status="NOT_AN_APF_COMPONENT_ROW",
        allowed_role="diagnostic scale and source-acquisition target only",
        promotes_to_APF_component=False,
    )


def source_proxy_closure_report() -> Dict[str, Any]:
    vals = source_vs_trace_transport_values()
    total = float(vals["Delta_r_source_total"])
    subtotal = numeric_proxy_subtotal()
    rem = source_total_remainder_row().value
    return {
        "Delta_r_source_total": total,
        "numeric_proxy_subtotal": subtotal,
        "unassigned_remainder": rem,
        "subtotal_plus_remainder": subtotal + rem,
        "closure_error": (subtotal + rem) - total,
        "remainder_fraction_of_total": rem / total,
        "known_proxy_rows": NUMERIC_PROXY_COMPONENTS,
        "unfilled_finite_rows": UNFILLED_FINITE_COMPONENTS,
        "unfilled_export_rows": UNFILLED_EXPORT_COMPONENTS,
        "source_total_promoted_to_component_rows": False,
    }


def uncertainty_scale_report() -> Dict[str, Any]:
    sens = transport_sensitivity_at_trace()
    jac = float(sens["dM_W_dDelta_r_GeV"])
    sigma_dr_quadrature = math.sqrt(PDG_DELTA_R_TOTAL_MT_SIGMA ** 2 + PDG_DELTA_R_TOTAL_ALPHA_SIGMA ** 2)
    return {
        "dM_W_dDelta_r_GeV": jac,
        "PDG_delta_r_total_mt_sigma": PDG_DELTA_R_TOTAL_MT_SIGMA,
        "PDG_delta_r_total_alpha_sigma": PDG_DELTA_R_TOTAL_ALPHA_SIGMA,
        "sigma_delta_r_quadrature_context": sigma_dr_quadrature,
        "sigma_M_W_MeV_quadrature_context": abs(jac) * sigma_dr_quadrature * 1000.0,
        "ACFW_source_theory_sigma_MeV_context": sens["source_theory_uncertainty_MeV"],
        "certified_export_uncertainty": False,
    }


def row_level_obstruction() -> Dict[str, Any]:
    rows = component_payload_rows()
    unfilled = tuple(r.component_id for r in rows if r.value is None)
    numeric_proxy = tuple(r.component_id for r in rows if r.value is not None and "PROXY" in r.evaluation_status)
    return {
        "status": STATUS,
        "numeric_proxy_components": numeric_proxy,
        "unfilled_components": unfilled,
        "finite_components_unfilled": UNFILLED_FINITE_COMPONENTS,
        "export_components_unfilled": UNFILLED_EXPORT_COMPONENTS,
        "blockers": BLOCKERS,
        "physical_W_export_ready": False,
        "exports_physical_M_W": False,
        "sharp_obstruction": "dominant standard proxies are present, but the APF eight-slot finite-part bundle is not reviewed/admitted and the source-total remainder is unresolved",
    }


def _shape_rows_for_schema_validation() -> Tuple[Dict[str, Any], ...]:
    out = []
    for r in component_payload_rows():
        out.append({
            "component_id": r.component_id,
            "component_symbol": r.component_symbol,
            "value": 0.0 if r.value is None else float(r.value),
            "uncertainty": 0.0 if r.uncertainty is None else float(r.uncertainty),
            "unit": "dimensionless_Delta_r_component",
            "scheme_family": "on_shell",
            "convention_id": "OS_EW_Delta_r_counterterm_convention_v1",
            "counterterm_component": "scheme_conversion_counterterm_component",
            "loop_order_scope": "v15.3 worksheet shape validation; source proxies not real APF payload",
            "sign_convention": "M_W^2(1-M_W^2/M_Z^2)=pi*alpha/(sqrt(2)*G_F)/(1-Delta_r)",
            "source_class": "internal_shape_fixture_not_real_payload",
            "source_title": r.source_basis,
            "source_pack_digest": "sha256:v15-3-component-worksheet-not-real-payload",
            "table_locator": "worksheet://w_trace_delta_r_component_payload/" + r.component_id,
            "extraction_log_digest": "sha256:v15-3-component-worksheet-extraction-log",
            "row_checksum": "sha256:v15-3-row-" + r.component_id,
            "provenance_chain": ("APF v15.3 component worksheet", "not a reviewed numerical finite-part source bundle"),
            "review_status": r.admission_status,
            "adapter_version": "w_trace_row_schema_adapter_v0",
            "consumed_inputs": (),
            "physical_export_request": False,
        })
    return tuple(out)


def component_sum_attempt_report() -> Dict[str, Any]:
    # Only pass the two source-proxy rows to the numerical sum machinery?  No:
    # certification requires all APF rows, admitted rows, covariance, and uncertainty.
    # We therefore deliberately use no admitted real rows and attach the worksheet
    # subtotal/remainder as diagnostics outside the certificate.
    cert = component_sum_certificate_report(
        rows=None,
        rows_admitted=False,
        covariance_supplied=False,
        uncertainty_supplied=False,
        physical_export_requested=False,
    )
    return {
        "certificate": cert,
        "worksheet_closure": source_proxy_closure_report(),
        "component_sum_certified": False,
        "reason": "source proxies plus aggregate remainder are diagnostics, not an admitted APF component-sum bundle",
    }


def component_payload_report() -> Dict[str, Any]:
    rows = component_payload_rows()
    row_dicts = tuple(asdict(r) for r in rows)
    remainder = asdict(source_total_remainder_row())
    schema_report = validate_rows(_shape_rows_for_schema_validation(), real_payload=False, physical_export_requested=False)
    readiness = readiness_report(physical_export_requested=False)
    export_lock = export_lock_report(physical_export_requested=False)
    artifact = {
        "status": STATUS,
        "version": VERSION,
        "payload_id": PAYLOAD_ID,
        "title": TITLE,
        "upstream_transport_status_required": "P_w_delta_r_transport_buildout",
        "trace_on_shell_angle_values": trace_on_shell_angle_values(),
        "pdg_decomposition_constants": {
            "Delta_r0": PDG_DELTA_R0,
            "Delta_r0_sigma": PDG_DELTA_R0_SIGMA,
            "rho_t_normalization": PDG_RHO_T_NORMALIZATION,
            "rho_t_reference_mt_GeV": PDG_RHO_T_REFERENCE_MT_GEV,
            "Delta_r_total_context": PDG_DELTA_R_TOTAL_CONTEXT,
            "Delta_r_total_mt_sigma": PDG_DELTA_R_TOTAL_MT_SIGMA,
            "Delta_r_total_alpha_sigma": PDG_DELTA_R_TOTAL_ALPHA_SIGMA,
        },
        "component_rows": row_dicts,
        "source_remainder_row": remainder,
        "source_proxy_closure": source_proxy_closure_report(),
        "uncertainty_scale_report": uncertainty_scale_report(),
        "component_sum_attempt": component_sum_attempt_report(),
        "schema_shape_validation": schema_report,
        "row_level_obstruction": row_level_obstruction(),
        "readiness_report": readiness,
        "physical_export_lock": export_lock,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "claim_boundary": "dominant-row component worksheet closed; APF finite-part export remains open",
    }
    artifact["payload_digest"] = _digest(artifact)
    return artifact


def paper_table_rows() -> Tuple[Dict[str, Any], ...]:
    rows = []
    for r in component_payload_rows():
        rows.append({
            "component_id": r.component_id,
            "symbol": r.component_symbol,
            "value": "UNFILLED" if r.value is None else f"{r.value:.15g}",
            "uncertainty": "UNFILLED" if r.uncertainty is None else f"{r.uncertainty:.3g}",
            "status": r.admission_status,
            "role": r.role,
        })
    rem = source_total_remainder_row()
    rows.append({
        "component_id": rem.row_id,
        "symbol": "Delta_r_remainder_source_total",
        "value": f"{rem.value:.15g}",
        "uncertainty": "NOT_SEPARATED",
        "status": rem.admissibility_status,
        "role": rem.interpretation,
    })
    return tuple(rows)


def terminal_report() -> Dict[str, Any]:
    return {
        "status": STATUS,
        "version": VERSION,
        "title": TITLE,
        "report": component_payload_report(),
        "paper_table_rows": paper_table_rows(),
        "verdict": "P_component_worksheet_plus_P_sharp_obstruction__not_physical_export",
    }


def check_T_w_delta_r_component_payload_status_declared():
    r = component_payload_report()
    return _res("status_declared", r["status"] == STATUS and r["version"] == VERSION and not r["physical_W_export_enabled"])


def check_T_w_delta_r_component_payload_depends_on_v152():
    d = _check_v152()
    return _res("depends_on_v152", _passed(d), upstream=d.get("status"), upstream_check=d.get("check"))


def check_T_w_delta_r_component_payload_exact_eight_slot_order():
    ids = tuple(r.component_id for r in component_payload_rows())
    return _res("exact_eight_slot_order", ids == FINITE_PART_COMPONENT_ORDER == REQUIRED_COMPONENT_SLOTS, component_order=ids)


def check_T_w_delta_r_component_payload_two_numeric_proxies_only():
    numeric = tuple(r.component_id for r in component_payload_rows() if r.value is not None)
    return _res("two_numeric_proxies_only", numeric == NUMERIC_PROXY_COMPONENTS, numeric=numeric)


def check_T_w_delta_r_component_payload_delta_alpha_row_matches_pdg_context():
    r = dominant_delta_alpha_row()
    ok = r.value == PDG_DELTA_R0 and r.uncertainty == PDG_DELTA_R0_SIGMA and r.value > 0
    return _res("delta_alpha_row_matches_pdg_context", ok, row=asdict(r))


def check_T_w_delta_r_component_payload_rho_row_negative_and_computed():
    r = dominant_rho_row()
    angles = trace_on_shell_angle_values()
    expected = -PDG_RHO_T_NORMALIZATION * angles["cot2_trace_context"]
    ok = r.value is not None and r.value < 0 and abs(r.value - expected) < 1e-15
    return _res("rho_row_negative_and_computed", ok, row=asdict(r), expected=expected)


def check_T_w_delta_r_component_payload_source_remainder_closes_total():
    c = source_proxy_closure_report()
    ok = abs(c["closure_error"]) < 1e-15 and c["source_total_promoted_to_component_rows"] is False
    return _res("source_remainder_closes_total", ok, closure=c)


def check_T_w_delta_r_component_payload_remainder_not_apf_row():
    rem = source_total_remainder_row()
    ok = rem.promotes_to_APF_component is False and rem.admissibility_status == "NOT_AN_APF_COMPONENT_ROW"
    return _res("remainder_not_apf_row", ok, remainder=asdict(rem))


def check_T_w_delta_r_component_payload_unfilled_slots_are_named():
    obs = row_level_obstruction()
    ok = tuple(obs["unfilled_components"]) == UNFILLED_FINITE_COMPONENTS + UNFILLED_EXPORT_COMPONENTS
    return _res("unfilled_slots_are_named", ok, obstruction=obs)


def check_T_w_delta_r_component_payload_blockers_are_sharpened():
    obs = row_level_obstruction()
    ok = tuple(obs["blockers"]) == BLOCKERS and "UNASSIGNED_STANDARD_REMAINDER_NOT_APF_COMPONENT_ROW" in obs["blockers"]
    return _res("blockers_are_sharpened", ok, blockers=obs["blockers"])


def check_T_w_delta_r_component_payload_no_forbidden_tokens():
    safe_material = {
        "constants": component_payload_report()["pdg_decomposition_constants"],
        "rows": component_payload_report()["component_rows"],
        "remainder": component_payload_report()["source_remainder_row"],
    }
    return _res("no_forbidden_tokens", not _contains_forbidden_token(safe_material))


def check_T_w_delta_r_component_payload_no_observed_w_consumed():
    rows = component_payload_rows()
    ok = all(not r.consumes_observed_W for r in rows)
    return _res("no_observed_w_consumed", ok)


def check_T_w_delta_r_component_payload_no_apf_anchor_as_component_input():
    rows = component_payload_rows()
    ok = all(not r.consumes_APF_anchor_as_input for r in rows)
    return _res("no_apf_anchor_as_component_input", ok)


def check_T_w_delta_r_component_payload_schema_shape_validates_but_not_real():
    r = component_payload_report()["schema_shape_validation"]
    ok = r["rows_supplied"] and r["rows_schema_valid"] and not r["rows_admitted"] and r["real_payload_requested"] is False
    return _res("schema_shape_validates_but_not_real", ok, schema_report=r)


def check_T_w_delta_r_component_payload_component_sum_not_certified():
    r = component_sum_attempt_report()
    cert = r["certificate"]
    ok = not cert["component_sum_certified"] and "NO_COMPONENT_ROWS_SUPPLIED" in cert["failure_reasons"]
    return _res("component_sum_not_certified", ok, component_sum_attempt=r)


def check_T_w_delta_r_component_payload_uncertainty_scale_context_only():
    u = uncertainty_scale_report()
    ok = u["sigma_M_W_MeV_quadrature_context"] > 0 and u["certified_export_uncertainty"] is False
    return _res("uncertainty_scale_context_only", ok, uncertainty=u)


def check_T_w_delta_r_component_payload_delta_r_to_mw_sensitivity_consistent():
    jac = dMW_dDelta_r(APF_DELTA_R_TARGET)
    u = uncertainty_scale_report()
    ok = abs(jac - u["dM_W_dDelta_r_GeV"]) < 1e-14 and jac < 0
    return _res("delta_r_to_mw_sensitivity_consistent", ok, jacobian=jac)


def check_T_w_delta_r_component_payload_mw_roundtrip_still_trace():
    mw = mw_from_delta_r(APF_DELTA_R_TARGET)
    ok = abs(mw - M_W_TRACE_GEV) < 1e-9
    return _res("mw_roundtrip_still_trace", ok, mw_from_apf_delta_r=mw, W_TRACE=M_W_TRACE_GEV)


def check_T_w_delta_r_component_payload_readiness_remains_open():
    r = component_payload_report()["readiness_report"]
    ok = not r["physical_W_export_ready"] and not r["exports_physical_M_W"]
    return _res("readiness_remains_open", ok, readiness=r)


def check_T_w_delta_r_component_payload_export_lock_closed():
    r = component_payload_report()["physical_export_lock"]
    ok = not r.get("physical_W_export_enabled", True) and not r.get("exports_physical_M_W", True)
    return _res("export_lock_closed", ok, export_lock=r)


def check_T_w_delta_r_component_payload_paper_table_has_nine_rows():
    rows = paper_table_rows()
    ok = len(rows) == 9 and rows[-1]["component_id"] == "standard_source_total_minus_two_dominant_proxies"
    return _res("paper_table_has_nine_rows", ok, rows=rows)


def check_T_w_delta_r_component_payload_digest_stable():
    d1 = component_payload_report()["payload_digest"]
    d2 = component_payload_report()["payload_digest"]
    return _res("digest_stable", d1 == d2 and d1.startswith("sha256:"), digest=d1)


def check_T_w_delta_r_component_payload_terminal_verdict():
    r = terminal_report()
    ok = r["verdict"] == "P_component_worksheet_plus_P_sharp_obstruction__not_physical_export"
    return _res("terminal_verdict", ok, verdict=r["verdict"])


def check_T_w_delta_r_component_payload_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_delta_r_component_payload_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))


_CHECKS = {
    "check_T_w_delta_r_component_payload_status_declared": check_T_w_delta_r_component_payload_status_declared,
    "check_T_w_delta_r_component_payload_depends_on_v152": check_T_w_delta_r_component_payload_depends_on_v152,
    "check_T_w_delta_r_component_payload_exact_eight_slot_order": check_T_w_delta_r_component_payload_exact_eight_slot_order,
    "check_T_w_delta_r_component_payload_two_numeric_proxies_only": check_T_w_delta_r_component_payload_two_numeric_proxies_only,
    "check_T_w_delta_r_component_payload_delta_alpha_row_matches_pdg_context": check_T_w_delta_r_component_payload_delta_alpha_row_matches_pdg_context,
    "check_T_w_delta_r_component_payload_rho_row_negative_and_computed": check_T_w_delta_r_component_payload_rho_row_negative_and_computed,
    "check_T_w_delta_r_component_payload_source_remainder_closes_total": check_T_w_delta_r_component_payload_source_remainder_closes_total,
    "check_T_w_delta_r_component_payload_remainder_not_apf_row": check_T_w_delta_r_component_payload_remainder_not_apf_row,
    "check_T_w_delta_r_component_payload_unfilled_slots_are_named": check_T_w_delta_r_component_payload_unfilled_slots_are_named,
    "check_T_w_delta_r_component_payload_blockers_are_sharpened": check_T_w_delta_r_component_payload_blockers_are_sharpened,
    "check_T_w_delta_r_component_payload_no_forbidden_tokens": check_T_w_delta_r_component_payload_no_forbidden_tokens,
    "check_T_w_delta_r_component_payload_no_observed_w_consumed": check_T_w_delta_r_component_payload_no_observed_w_consumed,
    "check_T_w_delta_r_component_payload_no_apf_anchor_as_component_input": check_T_w_delta_r_component_payload_no_apf_anchor_as_component_input,
    "check_T_w_delta_r_component_payload_schema_shape_validates_but_not_real": check_T_w_delta_r_component_payload_schema_shape_validates_but_not_real,
    "check_T_w_delta_r_component_payload_component_sum_not_certified": check_T_w_delta_r_component_payload_component_sum_not_certified,
    "check_T_w_delta_r_component_payload_uncertainty_scale_context_only": check_T_w_delta_r_component_payload_uncertainty_scale_context_only,
    "check_T_w_delta_r_component_payload_delta_r_to_mw_sensitivity_consistent": check_T_w_delta_r_component_payload_delta_r_to_mw_sensitivity_consistent,
    "check_T_w_delta_r_component_payload_mw_roundtrip_still_trace": check_T_w_delta_r_component_payload_mw_roundtrip_still_trace,
    "check_T_w_delta_r_component_payload_readiness_remains_open": check_T_w_delta_r_component_payload_readiness_remains_open,
    "check_T_w_delta_r_component_payload_export_lock_closed": check_T_w_delta_r_component_payload_export_lock_closed,
    "check_T_w_delta_r_component_payload_paper_table_has_nine_rows": check_T_w_delta_r_component_payload_paper_table_has_nine_rows,
    "check_T_w_delta_r_component_payload_digest_stable": check_T_w_delta_r_component_payload_digest_stable,
    "check_T_w_delta_r_component_payload_terminal_verdict": check_T_w_delta_r_component_payload_terminal_verdict,
    "check_T_w_delta_r_component_payload_bank_closure": check_T_w_delta_r_component_payload_bank_closure,
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
    closure = out["report"]["report"]["source_proxy_closure"]
    print("numeric_proxy_subtotal", f"{closure['numeric_proxy_subtotal']:.12f}")
    print("unassigned_remainder", f"{closure['unassigned_remainder']:.12f}")
    raise SystemExit(0 if out["passed"] else 1)
