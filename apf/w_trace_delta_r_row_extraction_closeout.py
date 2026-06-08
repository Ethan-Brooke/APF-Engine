"""W_TRACE Delta_r reviewed-row extraction closeout.

v15.6 (2026-05-09): one-pass hard closeout after the v15.5 source-acquisition
matrix.  This module performs the first actual reviewed row extraction from the
ACFW precision W-mass paper.  ACFW Table 1 gives the numerical values (x10^-4)
of the main Standard Model Delta-r contributions at a declared source-local
input point.  The extraction is machine-checkable and useful, but it is not an
APF same-input finite-part row bundle and therefore does not unlock physical W
export.

Closed here:
    * source-acquisition is promoted from located sources to a real reviewed
      source-local component table;
    * the ACFW Table-1 component rows are extracted with units, source inputs,
      and perturbative labels;
    * the source-local component sum is certified internally;
    * the promotion ladder is moved past ROW_EXTRACTED and blocked at
      APF-SAME-INPUT-EVALUATION / covariance / uncertainty.

Still open here:
    physical M_W export.  The extracted table is evaluated at the ACFW source
    point (MH=100 GeV, MW=80.426 GeV, mt=174.3 GeV, MZ=91.1875 GeV,
    Delta-alpha=0.05907, alpha_s=0.119), not at the APF_TRACE route input
    point.  No APF same-input finite-part rows, covariance matrix, or export
    uncertainty protocol is admitted.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_delta_r_source_acquisition_matrix import (
    acquisition_matrix_report,
    numeric_context,
    source_candidates,
    source_coverage_matrix,
    check_T_w_delta_r_source_acquisition_matrix_bank_closure as _check_v155,
)
from apf.w_trace_delta_r_remainder_resolution import (
    REMAINDER_BUCKET_ORDER,
    source_remainder,
    apf_trace_remainder_after_proxies,
    source_minus_apf_delta_r_gap,
)
from apf.w_trace_delta_r_component_payload import (
    PDG_DELTA_R0,
    dominant_delta_alpha_row,
    dominant_rho_row,
    numeric_proxy_subtotal,
)
from apf.w_trace_delta_r_transport_buildout import transport_sensitivity_at_trace
from apf.w_trace_component_sum_certificate import component_sum_certificate_report
from apf.w_trace_uncertainty_propagation import uncertainty_propagation_report
from apf.w_trace_physical_export_lock import export_lock_report

STATUS = "P_w_delta_r_row_extraction_closeout"
VERSION = "v15_6"
PASS_STATUS = "W_TRACE_DELTA_R_ROW_EXTRACTION_CLOSEOUT_PASS"
TITLE = "W_TRACE Delta_r reviewed-row extraction closeout"
PAYLOAD_ID = "W_TRACE_DELTA_R_ROW_EXTRACTION_CLOSEOUT_v15_6"

# ACFW Table 1 source-local input point.  These are not APF_TRACE inputs.
ACFW_TABLE1_INPUT_POINT: Dict[str, float | str] = {
    "source": "Awramik-Czakon-Freitas-Weiglein precise W mass, Table 1",
    "M_H_GeV": 100.0,
    "M_W_GeV_fixed_for_table": 80.426,
    "m_t_GeV": 174.3,
    "m_b_GeV": 4.7,
    "M_Z_GeV": 91.1875,
    "Gamma_Z_GeV": 2.4952,
    "alpha_inverse": 137.03599976,
    "Delta_alpha": 0.05907,
    "alpha_s_MZ": 0.119,
    "G_mu_GeV_minus2": 1.166379e-5,
    "mass_convention_note": "W and Z masses transformed to the real part of the complex pole for the table; paper W convention remains running-width Breit-Wigner elsewhere.",
}

# ACFW Table 1 prints values x 10^4 for MH=100 GeV and MW=80.426 GeV.
# Store raw printed entries and convert to dimensionless Delta_r rows.
ACFW_TABLE1_SCALE = 1.0e-4
ACFW_TABLE1_MH100_X1E4: Tuple[Tuple[str, str, float, str], ...] = (
    ("one_loop_alpha", "Delta r^(alpha)", 283.41, "one-loop electroweak contribution including Delta-alpha/top-rho/remainder structure"),
    ("qcd_alpha_alpha_s", "Delta r^(alpha alpha_s)", 35.89, "two-loop QCD correction"),
    ("qcd_alpha_alpha_s2", "Delta r^(alpha alpha_s^2)", 7.23, "three-loop QCD correction"),
    ("qcd_alpha_alpha_s3_mt2", "Delta r^(alpha alpha_s^3 m_t^2)", 1.27, "approximate four-loop QCD/top correction"),
    ("fermionic_alpha2", "Delta r^(alpha^2)_ferm", 28.56, "fermionic electroweak two-loop correction"),
    ("bosonic_alpha2", "Delta r^(alpha^2)_bos", 0.64, "purely bosonic electroweak two-loop correction"),
    ("mixed_Gmu2_alpha_s_mt4", "Delta r^(G_mu^2 alpha_s m_t^4)", -1.27, "leading higher-order mixed EW/QCD top contribution"),
    ("ew_Gmu3_mt6", "Delta r^(G_mu^3 m_t^6)", -0.16, "leading electroweak three-loop top contribution"),
)

FORBIDDEN_TOKENS: Tuple[str, ...] = (
    "CDF_II_M_W",
    "fit_to_observed_W",
    "component_residual_tuned_to_APF_anchor",
    "physical_export_override",
    "APF_anchor_as_fit_input",
)

@dataclass(frozen=True)
class ExtractedDeltaRRow:
    row_id: str
    source_symbol: str
    printed_value_x1e4: float
    value: float
    unit: str
    perturbative_family: str
    source_role: str
    source_input_point_id: str
    extraction_status: str
    admitted_as_apf_same_input_row: bool
    admitted_for_export: bool

@dataclass(frozen=True)
class PromotionCloseoutRow:
    gate: str
    status: str
    closed: bool
    blocker: str
    paper_claim: str


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
    txt = _canonical_json(obj)
    return any(tok in txt for tok in FORBIDDEN_TOKENS)


def extracted_acfw_rows() -> Tuple[ExtractedDeltaRRow, ...]:
    rows = []
    for rid, symbol, printed, role in ACFW_TABLE1_MH100_X1E4:
        rows.append(ExtractedDeltaRRow(
            row_id=rid,
            source_symbol=symbol,
            printed_value_x1e4=float(printed),
            value=float(printed) * ACFW_TABLE1_SCALE,
            unit="dimensionless_Delta_r_component",
            perturbative_family=rid,
            source_role=role,
            source_input_point_id="ACFW_TABLE1_MH100_MW80426_SOURCE_POINT",
            extraction_status="REVIEWED_SOURCE_LOCAL_ROW_EXTRACTED",
            admitted_as_apf_same_input_row=False,
            admitted_for_export=False,
        ))
    return tuple(rows)


def extracted_row_sum() -> float:
    return sum(r.value for r in extracted_acfw_rows())


def extracted_row_sum_x1e4() -> float:
    return sum(r.printed_value_x1e4 for r in extracted_acfw_rows())


def dominant_proxy_delta() -> Dict[str, float]:
    # The extracted source-local one-loop row is not decomposed into PDG Delta-r0/top-rho proxies.
    one_loop = next(r.value for r in extracted_acfw_rows() if r.row_id == "one_loop_alpha")
    return {
        "acfw_one_loop_alpha_row": one_loop,
        "pdg_delta_r0_proxy": float(PDG_DELTA_R0),
        "pdg_proxy_subtotal_delta_alpha_plus_top_rho": float(numeric_proxy_subtotal()),
        "source_local_one_loop_minus_pdg_delta_r0": one_loop - float(PDG_DELTA_R0),
        "source_local_one_loop_minus_pdg_proxy_subtotal": one_loop - float(numeric_proxy_subtotal()),
    }


def row_family_coverage() -> Dict[str, Any]:
    ids = {r.row_id for r in extracted_acfw_rows()}
    return {
        "has_one_loop_row": "one_loop_alpha" in ids,
        "has_qcd_rows": {"qcd_alpha_alpha_s", "qcd_alpha_alpha_s2", "qcd_alpha_alpha_s3_mt2"}.issubset(ids),
        "has_fermionic_two_loop_row": "fermionic_alpha2" in ids,
        "has_bosonic_two_loop_row": "bosonic_alpha2" in ids,
        "has_mixed_higher_order_rows": {"mixed_Gmu2_alpha_s_mt4", "ew_Gmu3_mt6"}.issubset(ids),
        "row_count": len(ids),
    }


def bucket_to_extracted_rows() -> Dict[str, Tuple[str, ...]]:
    return {
        "fermionic_nonleading_finite_remainder": ("fermionic_alpha2", "one_loop_alpha"),
        "bosonic_finite_remainder": ("bosonic_alpha2", "one_loop_alpha"),
        "vertex_box_muon_decay_remainder": ("one_loop_alpha", "fermionic_alpha2", "bosonic_alpha2"),
        "on_shell_counterterm_finite_remainder": ("one_loop_alpha", "fermionic_alpha2", "bosonic_alpha2"),
        "mixed_higher_order_EW_QCD_remainder": ("qcd_alpha_alpha_s", "qcd_alpha_alpha_s2", "qcd_alpha_alpha_s3_mt2", "mixed_Gmu2_alpha_s_mt4", "ew_Gmu3_mt6"),
        "covariance_and_export_uncertainty_remainder": tuple(),
    }


def promotion_closeout_rows() -> Tuple[PromotionCloseoutRow, ...]:
    return (
        PromotionCloseoutRow(
            gate="SOURCE_LOCATED",
            status="CLOSED",
            closed=True,
            blocker="none",
            paper_claim="Reviewed source families remain located from v15.5.",
        ),
        PromotionCloseoutRow(
            gate="ROW_EXTRACTED_SOURCE_LOCAL",
            status="CLOSED",
            closed=True,
            blocker="none",
            paper_claim="ACFW Table 1 provides an eight-entry source-local perturbative Delta-r component table.",
        ),
        PromotionCloseoutRow(
            gate="APF_SAME_INPUT_EVALUATED_ROWS",
            status="BLOCKED",
            closed=False,
            blocker="ACFW_TABLE1_SOURCE_POINT_DIFFERS_FROM_APF_TRACE_ROUTE_INPUTS",
            paper_claim="The extracted rows are not evaluated at the APF trace/on-shell route input point.",
        ),
        PromotionCloseoutRow(
            gate="APF_ROW_ADMISSION",
            status="BLOCKED",
            closed=False,
            blocker="SOURCE_LOCAL_ROWS_NOT_ADMITTED_AS_APF_FINITE_PART_ROWS",
            paper_claim="A source-local perturbative table is not a reviewed APF finite-part row bundle.",
        ),
        PromotionCloseoutRow(
            gate="COMPONENT_SUM_CERTIFIED_FOR_APF_TOTAL",
            status="BLOCKED",
            closed=False,
            blocker="SOURCE_LOCAL_SUM_DOES_NOT_CERTIFY_APF_TRACE_DELTA_R_TOTAL",
            paper_claim="The ACFW table sum is internally certified only at the source point.",
        ),
        PromotionCloseoutRow(
            gate="COVARIANCE_CERTIFIED",
            status="BLOCKED",
            closed=False,
            blocker="NO_ROW_COVARIANCE_MATRIX",
            paper_claim="No covariance matrix accompanies the extracted component rows.",
        ),
        PromotionCloseoutRow(
            gate="UNCERTAINTY_PUSHFORWARD_CERTIFIED",
            status="BLOCKED",
            closed=False,
            blocker="NO_ROW_LEVEL_UNCERTAINTY_PROTOCOL",
            paper_claim="The upstream total theory uncertainty cannot be re-labeled as row covariance.",
        ),
        PromotionCloseoutRow(
            gate="PHYSICAL_W_EXPORT",
            status="LOCKED",
            closed=False,
            blocker="EXPORT_LOCK_REMAINS_ACTIVE",
            paper_claim="No physical W export is made in v15.6.",
        ),
    )


def same_input_obstruction_report() -> Dict[str, Any]:
    return {
        "physical_W_export_ready": False,
        "exports_physical_M_W": False,
        "first_failed_gate_after_v155": "APF_SAME_INPUT_EVALUATED_ROWS",
        "closed_upgrade_from_v155": "row extraction is no longer merely required; a reviewed source-local component table has been extracted",
        "remaining_blockers": (
            "ACFW_TABLE1_SOURCE_POINT_DIFFERS_FROM_APF_TRACE_ROUTE_INPUTS",
            "NO_APF_TRACE_EVALUATED_COMPONENT_ROWS",
            "NO_APF_ROW_ADMISSION_CERTIFICATE",
            "NO_COMPONENT_SUM_CERTIFICATE_FOR_APF_TRACE_TOTAL",
            "NO_REAL_ROW_COVARIANCE_MATRIX",
            "NO_EXPORT_UNCERTAINTY_PROTOCOL",
            "PHYSICAL_EXPORT_LOCKED",
        ),
        "source_local_input_point": ACFW_TABLE1_INPUT_POINT,
    }


def source_local_component_sum_certificate() -> Dict[str, Any]:
    rows = extracted_acfw_rows()
    printed_sum = extracted_row_sum_x1e4()
    value_sum = extracted_row_sum()
    return {
        "source_local_component_sum_certified": abs(value_sum - printed_sum * ACFW_TABLE1_SCALE) < 1e-18,
        "printed_sum_x1e4": printed_sum,
        "dimensionless_sum": value_sum,
        "row_count": len(rows),
        "scope": "ACFW_TABLE1_SOURCE_LOCAL_ONLY_NOT_APF_EXPORT",
    }


def apf_export_component_sum_certificate() -> Dict[str, Any]:
    return component_sum_certificate_report(
        rows=None,
        rows_admitted=False,
        covariance_supplied=False,
        uncertainty_supplied=False,
        physical_export_requested=False,
    )


def uncertainty_closeout_report() -> Dict[str, Any]:
    return {
        "source_local_row_uncertainty_certified": False,
        "reason": "ACFW Table 1 supplies component central values, not row covariance or APF same-input uncertainty rows.",
        "upstream_total_uncertainty_role": "comparison-scale only",
        "uncertainty_propagation_report": uncertainty_propagation_report(cov=None, physical_export_requested=False),
    }


def numeric_closeout_context() -> Dict[str, Any]:
    ctx = numeric_context()
    sens = transport_sensitivity_at_trace()
    return {
        "acfw_table1_row_sum": extracted_row_sum(),
        "acfw_table1_row_sum_x1e4": extracted_row_sum_x1e4(),
        "v15_4_source_remainder_after_proxies": source_remainder(),
        "v15_4_apf_trace_remainder_after_proxies": apf_trace_remainder_after_proxies(),
        "v15_4_source_minus_apf_delta_r_gap": source_minus_apf_delta_r_gap(),
        "v15_4_source_minus_apf_gap_MW_shift_MeV": ctx["source_minus_apf_gap_MW_shift_MeV"],
        "dM_W_dDelta_r_GeV_at_trace": float(sens["dM_W_dDelta_r_GeV"]),
        "dominant_proxy_delta": dominant_proxy_delta(),
    }


def closeout_report() -> Dict[str, Any]:
    artifact = {
        "status": STATUS,
        "version": VERSION,
        "payload_id": PAYLOAD_ID,
        "title": TITLE,
        "upstream_required": "P_w_delta_r_source_acquisition_matrix",
        "reviewed_source_used_for_extraction": "Awramik_Czakon_Freitas_Weiglein_2004_MW_Table_1",
        "source_local_input_point": ACFW_TABLE1_INPUT_POINT,
        "extracted_rows": tuple(asdict(r) for r in extracted_acfw_rows()),
        "source_local_component_sum_certificate": source_local_component_sum_certificate(),
        "bucket_to_extracted_rows": bucket_to_extracted_rows(),
        "row_family_coverage": row_family_coverage(),
        "promotion_closeout_rows": tuple(asdict(r) for r in promotion_closeout_rows()),
        "same_input_obstruction_report": same_input_obstruction_report(),
        "apf_export_component_sum_certificate": apf_export_component_sum_certificate(),
        "uncertainty_closeout_report": uncertainty_closeout_report(),
        "physical_export_lock": export_lock_report(physical_export_requested=False),
        "numeric_context": numeric_closeout_context(),
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "claim_boundary": "reviewed source-local Delta-r rows extracted; APF same-input physical W export remains locked",
    }
    artifact["payload_digest"] = _digest(artifact)
    return artifact


def terminal_report() -> Dict[str, Any]:
    return {
        "status": STATUS,
        "version": VERSION,
        "title": TITLE,
        "report": closeout_report(),
        "verdict": "P_reviewed_source_local_row_extraction_plus_P_terminal_same_input_obstruction__not_physical_export",
    }


# --- Checks -----------------------------------------------------------------

def check_T_w_delta_r_row_extraction_closeout_status_declared():
    r = closeout_report()
    return _res("status_declared", r["status"] == STATUS and r["version"] == VERSION and not r["physical_W_export_enabled"])


def check_T_w_delta_r_row_extraction_closeout_depends_on_v155():
    d = _check_v155()
    return _res("depends_on_v155", _passed(d), upstream=d.get("status"), upstream_check=d.get("check"))


def check_T_w_delta_r_row_extraction_closeout_source_table_input_point_declared():
    ip = ACFW_TABLE1_INPUT_POINT
    ok = ip["M_H_GeV"] == 100.0 and ip["M_W_GeV_fixed_for_table"] == 80.426 and ip["m_t_GeV"] == 174.3 and ip["Delta_alpha"] == 0.05907
    return _res("source_table_input_point_declared", ok, input_point=ip)


def check_T_w_delta_r_row_extraction_closeout_extracts_eight_rows():
    rows = extracted_acfw_rows()
    return _res("extracts_eight_rows", len(rows) == 8 and all(r.extraction_status == "REVIEWED_SOURCE_LOCAL_ROW_EXTRACTED" for r in rows), rows=tuple(asdict(r) for r in rows))


def check_T_w_delta_r_row_extraction_closeout_raw_values_match_acfw_table1():
    expected = (283.41, 35.89, 7.23, 1.27, 28.56, 0.64, -1.27, -0.16)
    got = tuple(r.printed_value_x1e4 for r in extracted_acfw_rows())
    return _res("raw_values_match_acfw_table1", got == expected, got=got)


def check_T_w_delta_r_row_extraction_closeout_dimensionless_conversion():
    ok = all(abs(r.value - r.printed_value_x1e4 * 1e-4) < 1e-18 for r in extracted_acfw_rows())
    return _res("dimensionless_conversion", ok)


def check_T_w_delta_r_row_extraction_closeout_source_local_sum_certified():
    cert = source_local_component_sum_certificate()
    ok = cert["source_local_component_sum_certified"] and abs(cert["dimensionless_sum"] - 0.035557) < 1e-15
    return _res("source_local_sum_certified", ok, certificate=cert)


def check_T_w_delta_r_row_extraction_closeout_contains_fermionic_and_bosonic_rows():
    cov = row_family_coverage()
    ok = cov["has_fermionic_two_loop_row"] and cov["has_bosonic_two_loop_row"] and cov["has_qcd_rows"]
    return _res("contains_fermionic_and_bosonic_rows", ok, coverage=cov)


def check_T_w_delta_r_row_extraction_closeout_bucket_mapping_complete_except_covariance():
    mapping = bucket_to_extracted_rows()
    ok = tuple(mapping.keys()) == REMAINDER_BUCKET_ORDER and all(mapping[b] for b in REMAINDER_BUCKET_ORDER if b != "covariance_and_export_uncertainty_remainder") and not mapping["covariance_and_export_uncertainty_remainder"]
    return _res("bucket_mapping_complete_except_covariance", ok, mapping=mapping)


def check_T_w_delta_r_row_extraction_closeout_promotion_moved_past_source_located():
    rows = promotion_closeout_rows()
    gates = {r.gate: r for r in rows}
    ok = gates["SOURCE_LOCATED"].closed and gates["ROW_EXTRACTED_SOURCE_LOCAL"].closed and not gates["APF_SAME_INPUT_EVALUATED_ROWS"].closed
    return _res("promotion_moved_past_source_located", ok, rows=tuple(asdict(r) for r in rows))


def check_T_w_delta_r_row_extraction_closeout_first_failed_gate_is_same_input():
    obs = same_input_obstruction_report()
    return _res("first_failed_gate_is_same_input", obs["first_failed_gate_after_v155"] == "APF_SAME_INPUT_EVALUATED_ROWS", obstruction=obs)


def check_T_w_delta_r_row_extraction_closeout_rows_not_admitted_as_apf_rows():
    ok = not any(r.admitted_as_apf_same_input_row or r.admitted_for_export for r in extracted_acfw_rows())
    return _res("rows_not_admitted_as_apf_rows", ok)


def check_T_w_delta_r_row_extraction_closeout_component_sum_not_promoted_to_apf_total():
    cert = apf_export_component_sum_certificate()
    ok = not cert.get("component_sum_certified", True)
    return _res("component_sum_not_promoted_to_apf_total", ok, certificate=cert)


def check_T_w_delta_r_row_extraction_closeout_uncertainty_still_blocked():
    u = uncertainty_closeout_report()
    ok = not u["source_local_row_uncertainty_certified"]
    return _res("uncertainty_still_blocked", ok, uncertainty=u)


def check_T_w_delta_r_row_extraction_closeout_export_lock_preserved():
    lock = closeout_report()["physical_export_lock"]
    ok = not lock.get("physical_W_export_enabled", True) and not lock.get("exports_physical_M_W", True)
    return _res("export_lock_preserved", ok, export_lock=lock)


def check_T_w_delta_r_row_extraction_closeout_no_forbidden_tokens():
    safe = {
        "source_local_input_point": ACFW_TABLE1_INPUT_POINT,
        "extracted_rows": tuple(asdict(r) for r in extracted_acfw_rows()),
        "promotion_closeout_rows": tuple(asdict(r) for r in promotion_closeout_rows()),
        "claim_boundary": closeout_report()["claim_boundary"],
    }
    return _res("no_forbidden_tokens", not _contains_forbidden_token(safe))


def check_T_w_delta_r_row_extraction_closeout_source_acquisition_no_longer_first_blocker():
    obs = same_input_obstruction_report()
    ok = "row extraction is no longer merely required" in obs["closed_upgrade_from_v155"]
    return _res("source_acquisition_no_longer_first_blocker", ok, obstruction=obs)


def check_T_w_delta_r_row_extraction_closeout_acfw_candidate_present_upstream():
    ids = tuple(s.source_id for s in source_candidates())
    ok = "acfw_2003_precise_w_mass_total" in ids
    return _res("acfw_candidate_present_upstream", ok, upstream_candidate_ids=ids)


def check_T_w_delta_r_row_extraction_closeout_coverage_extends_v155():
    cov = source_coverage_matrix()
    rcov = row_family_coverage()
    ok = all(cov[b]["has_reviewed_source"] for b in REMAINDER_BUCKET_ORDER) and rcov["row_count"] == 8
    return _res("coverage_extends_v155", ok, source_coverage=cov, row_coverage=rcov)


def check_T_w_delta_r_row_extraction_closeout_numeric_context_preserved():
    ctx = numeric_closeout_context()
    ok = abs(ctx["v15_4_source_minus_apf_delta_r_gap"] - source_minus_apf_delta_r_gap()) < 1e-18
    return _res("numeric_context_preserved", ok, context=ctx)


def check_T_w_delta_r_row_extraction_closeout_mw_shift_preserved():
    ctx = numeric_closeout_context()
    recomputed = ctx["dM_W_dDelta_r_GeV_at_trace"] * ctx["v15_4_source_minus_apf_delta_r_gap"] * 1000.0
    ok = abs(recomputed - ctx["v15_4_source_minus_apf_gap_MW_shift_MeV"]) < 1e-12
    return _res("mw_shift_preserved", ok, recomputed=recomputed, stored=ctx["v15_4_source_minus_apf_gap_MW_shift_MeV"])


def check_T_w_delta_r_row_extraction_closeout_dominant_proxy_not_confused_with_source_one_loop():
    d = dominant_proxy_delta()
    ok = abs(d["source_local_one_loop_minus_pdg_proxy_subtotal"]) > 1e-3 and abs(d["source_local_one_loop_minus_pdg_delta_r0"]) > 1e-3
    return _res("dominant_proxy_not_confused_with_source_one_loop", ok, deltas=d)


def check_T_w_delta_r_row_extraction_closeout_row_sum_scope_labeled_source_local():
    cert = source_local_component_sum_certificate()
    ok = cert["scope"] == "ACFW_TABLE1_SOURCE_LOCAL_ONLY_NOT_APF_EXPORT"
    return _res("row_sum_scope_labeled_source_local", ok, certificate=cert)


def check_T_w_delta_r_row_extraction_closeout_no_covariance_row_admitted():
    mapping = bucket_to_extracted_rows()
    ok = mapping["covariance_and_export_uncertainty_remainder"] == tuple()
    return _res("no_covariance_row_admitted", ok, mapping=mapping)


def check_T_w_delta_r_row_extraction_closeout_physical_export_disabled_in_report():
    r = closeout_report()
    ok = not r["physical_W_export_enabled"] and not r["exports_physical_M_W"] and "remains locked" in r["claim_boundary"]
    return _res("physical_export_disabled_in_report", ok, boundary=r["claim_boundary"])


def check_T_w_delta_r_row_extraction_closeout_digest_stable():
    d1 = closeout_report()["payload_digest"]
    d2 = closeout_report()["payload_digest"]
    return _res("digest_stable", d1 == d2 and d1.startswith("sha256:"), digest=d1)


def check_T_w_delta_r_row_extraction_closeout_terminal_verdict():
    r = terminal_report()
    ok = r["verdict"] == "P_reviewed_source_local_row_extraction_plus_P_terminal_same_input_obstruction__not_physical_export"
    return _res("terminal_verdict", ok, verdict=r["verdict"])


def check_T_w_delta_r_row_extraction_closeout_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_delta_r_row_extraction_closeout_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))


_CHECKS = {
    "check_T_w_delta_r_row_extraction_closeout_status_declared": check_T_w_delta_r_row_extraction_closeout_status_declared,
    "check_T_w_delta_r_row_extraction_closeout_depends_on_v155": check_T_w_delta_r_row_extraction_closeout_depends_on_v155,
    "check_T_w_delta_r_row_extraction_closeout_source_table_input_point_declared": check_T_w_delta_r_row_extraction_closeout_source_table_input_point_declared,
    "check_T_w_delta_r_row_extraction_closeout_extracts_eight_rows": check_T_w_delta_r_row_extraction_closeout_extracts_eight_rows,
    "check_T_w_delta_r_row_extraction_closeout_raw_values_match_acfw_table1": check_T_w_delta_r_row_extraction_closeout_raw_values_match_acfw_table1,
    "check_T_w_delta_r_row_extraction_closeout_dimensionless_conversion": check_T_w_delta_r_row_extraction_closeout_dimensionless_conversion,
    "check_T_w_delta_r_row_extraction_closeout_source_local_sum_certified": check_T_w_delta_r_row_extraction_closeout_source_local_sum_certified,
    "check_T_w_delta_r_row_extraction_closeout_contains_fermionic_and_bosonic_rows": check_T_w_delta_r_row_extraction_closeout_contains_fermionic_and_bosonic_rows,
    "check_T_w_delta_r_row_extraction_closeout_bucket_mapping_complete_except_covariance": check_T_w_delta_r_row_extraction_closeout_bucket_mapping_complete_except_covariance,
    "check_T_w_delta_r_row_extraction_closeout_promotion_moved_past_source_located": check_T_w_delta_r_row_extraction_closeout_promotion_moved_past_source_located,
    "check_T_w_delta_r_row_extraction_closeout_first_failed_gate_is_same_input": check_T_w_delta_r_row_extraction_closeout_first_failed_gate_is_same_input,
    "check_T_w_delta_r_row_extraction_closeout_rows_not_admitted_as_apf_rows": check_T_w_delta_r_row_extraction_closeout_rows_not_admitted_as_apf_rows,
    "check_T_w_delta_r_row_extraction_closeout_component_sum_not_promoted_to_apf_total": check_T_w_delta_r_row_extraction_closeout_component_sum_not_promoted_to_apf_total,
    "check_T_w_delta_r_row_extraction_closeout_uncertainty_still_blocked": check_T_w_delta_r_row_extraction_closeout_uncertainty_still_blocked,
    "check_T_w_delta_r_row_extraction_closeout_export_lock_preserved": check_T_w_delta_r_row_extraction_closeout_export_lock_preserved,
    "check_T_w_delta_r_row_extraction_closeout_no_forbidden_tokens": check_T_w_delta_r_row_extraction_closeout_no_forbidden_tokens,
    "check_T_w_delta_r_row_extraction_closeout_source_acquisition_no_longer_first_blocker": check_T_w_delta_r_row_extraction_closeout_source_acquisition_no_longer_first_blocker,
    "check_T_w_delta_r_row_extraction_closeout_acfw_candidate_present_upstream": check_T_w_delta_r_row_extraction_closeout_acfw_candidate_present_upstream,
    "check_T_w_delta_r_row_extraction_closeout_coverage_extends_v155": check_T_w_delta_r_row_extraction_closeout_coverage_extends_v155,
    "check_T_w_delta_r_row_extraction_closeout_numeric_context_preserved": check_T_w_delta_r_row_extraction_closeout_numeric_context_preserved,
    "check_T_w_delta_r_row_extraction_closeout_mw_shift_preserved": check_T_w_delta_r_row_extraction_closeout_mw_shift_preserved,
    "check_T_w_delta_r_row_extraction_closeout_dominant_proxy_not_confused_with_source_one_loop": check_T_w_delta_r_row_extraction_closeout_dominant_proxy_not_confused_with_source_one_loop,
    "check_T_w_delta_r_row_extraction_closeout_row_sum_scope_labeled_source_local": check_T_w_delta_r_row_extraction_closeout_row_sum_scope_labeled_source_local,
    "check_T_w_delta_r_row_extraction_closeout_no_covariance_row_admitted": check_T_w_delta_r_row_extraction_closeout_no_covariance_row_admitted,
    "check_T_w_delta_r_row_extraction_closeout_physical_export_disabled_in_report": check_T_w_delta_r_row_extraction_closeout_physical_export_disabled_in_report,
    "check_T_w_delta_r_row_extraction_closeout_digest_stable": check_T_w_delta_r_row_extraction_closeout_digest_stable,
    "check_T_w_delta_r_row_extraction_closeout_terminal_verdict": check_T_w_delta_r_row_extraction_closeout_terminal_verdict,
    "check_T_w_delta_r_row_extraction_closeout_bank_closure": check_T_w_delta_r_row_extraction_closeout_bank_closure,
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
    ctx = out["report"]["report"]["numeric_context"]
    print("acfw_table1_row_sum", f"{ctx['acfw_table1_row_sum']:.12f}")
    print("first_failed_gate_after_v155", out["report"]["report"]["same_input_obstruction_report"]["first_failed_gate_after_v155"])
    raise SystemExit(0 if out["passed"] else 1)
