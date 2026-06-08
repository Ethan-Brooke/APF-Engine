"""W_TRACE Delta_r source-acquisition matrix.

v15.5 (2026-05-09): hard-push acquisition layer after v15.4 remainder
resolution.  This module does not promote the W route to physical export.  It
turns the named unresolved Delta-r remainder buckets into a reviewed-source
acquisition matrix: which electroweak references can support each bucket, which
objects remain missing, and which promotion predicates must be satisfied before
any finite-part component row can be admitted.

Closed here:
    * every v15.4 unresolved remainder bucket is mapped to at least one
      reviewed electroweak source family;
    * the distinction between source located, row extracted, row admitted, and
      physical export is made executable;
    * ACFW is quarantined as a precision total, not a component decomposition;
    * the export gate remains locked until numerical bucket rows, covariance,
      component-sum, and uncertainty propagation are supplied.

Still open here:
    numerical APF finite-part rows and physical W/on-shell export.  v15.5 is a
    source-acquisition closeout, not a finite-part payload closeout.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_delta_r_remainder_resolution import (
    BLOCKERS as V154_BLOCKERS,
    EXTERNAL_SOURCE_REQUIREMENTS,
    REMAINDER_BUCKET_ORDER,
    apf_trace_remainder_after_proxies,
    component_certificate_after_resolution,
    crosswalk_report,
    remainder_bucket_rows,
    remainder_resolution_report,
    source_minus_apf_delta_r_gap,
    source_remainder,
    check_T_w_delta_r_remainder_resolution_bank_closure as _check_v154,
)
from apf.w_trace_delta_r_component_payload import (
    PDG_DELTA_R0,
    PDG_DELTA_R0_SIGMA,
    PDG_RHO_T_NORMALIZATION,
    numeric_proxy_subtotal,
)
from apf.w_trace_delta_r_transport_buildout import transport_sensitivity_at_trace
from apf.w_trace_component_sum_certificate import component_sum_certificate_report
from apf.w_trace_uncertainty_propagation import uncertainty_propagation_report
from apf.w_trace_physical_export_lock import export_lock_report

STATUS = "P_w_delta_r_source_acquisition_matrix"
VERSION = "v15_5"
PASS_STATUS = "W_TRACE_DELTA_R_SOURCE_ACQUISITION_MATRIX_PASS"
TITLE = "W_TRACE Delta_r source-acquisition matrix"
PAYLOAD_ID = "W_TRACE_DELTA_R_SOURCE_ACQUISITION_MATRIX_v15_5"

ROW_STATES: Tuple[str, ...] = (
    "SOURCE_LOCATED",
    "ROW_EXTRACTED",
    "ROW_ADMITTED",
    "SUM_CERTIFIED",
    "COVARIANCE_CERTIFIED",
    "UNCERTAINTY_CERTIFIED",
    "EXPORT_ELIGIBLE",
)

PROMOTION_REQUIRED_STATES: Tuple[str, ...] = (
    "ROW_EXTRACTED",
    "ROW_ADMITTED",
    "SUM_CERTIFIED",
    "COVARIANCE_CERTIFIED",
    "UNCERTAINTY_CERTIFIED",
)

FORBIDDEN_SOURCE_ACQUISITION_TOKENS: Tuple[str, ...] = (
    "observed_M_W",
    "world_average_M_W",
    "CDF_II_M_W",
    "CMS_observed_M_W",
    "fit_to_observed_W",
    "component_residual_tuned_to_APF_anchor",
    "physical_export_override",
)

@dataclass(frozen=True)
class SourceCandidate:
    source_id: str
    citation_key: str
    source_family: str
    reviewed_status: str
    covers_buckets: Tuple[str, ...]
    component_granularity: str
    numerical_bucket_rows_available_here: bool
    covariance_available_here: bool
    uncertainty_protocol_available_here: bool
    allowed_role: str
    acquisition_status: str
    url_hint: str
    note: str

@dataclass(frozen=True)
class BucketAcquisitionRow:
    bucket_id: str
    required_components: Tuple[str, ...]
    source_candidates: Tuple[str, ...]
    source_located: bool
    row_extracted: bool
    row_admitted: bool
    component_sum_certified: bool
    covariance_certified: bool
    uncertainty_certified: bool
    export_eligible: bool
    blocker: str


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
    return any(tok in txt for tok in FORBIDDEN_SOURCE_ACQUISITION_TOKENS)


def source_candidates() -> Tuple[SourceCandidate, ...]:
    """Reviewed source map for the v15.4 remainder buckets.

    The entries are source-acquisition objects, not admitted APF component rows.
    """
    return (
        SourceCandidate(
            source_id="pdg_ew_review_delta_r_structure",
            citation_key="PDG_EW_Review_2024",
            source_family="review_structure_and_dominant_proxy_values",
            reviewed_status="REVIEWED_REFERENCE",
            covers_buckets=(
                "fermionic_nonleading_finite_remainder",
                "bosonic_finite_remainder",
                "mixed_higher_order_EW_QCD_remainder",
                "covariance_and_export_uncertainty_remainder",
            ),
            component_granularity="dominant_structure_plus_context_total",
            numerical_bucket_rows_available_here=False,
            covariance_available_here=False,
            uncertainty_protocol_available_here=False,
            allowed_role="source map and dominant-proxy scaffold only",
            acquisition_status="SOURCE_LOCATED_NOT_COMPONENT_TABLE",
            url_hint="https://pdg.lbl.gov/2024/reviews/rpp2024-rev-standard-model.pdf",
            note="Gives Delta-r structure and dominant Delta-alpha/top-rho proxy values; does not provide the APF eight-slot numerical finite-part table.",
        ),
        SourceCandidate(
            source_id="freitas_hollik_walter_weiglein_2000_complete_fermionic",
            citation_key="Freitas_Hollik_Walter_Weiglein_2000",
            source_family="complete_fermionic_two_loop_W_MZ_relation",
            reviewed_status="REVIEWED_CALCULATION_SOURCE",
            covers_buckets=(
                "fermionic_nonleading_finite_remainder",
                "vertex_box_muon_decay_remainder",
                "on_shell_counterterm_finite_remainder",
            ),
            component_granularity="full fermionic two-loop calculation / parametrization, not APF row table",
            numerical_bucket_rows_available_here=False,
            covariance_available_here=False,
            uncertainty_protocol_available_here=False,
            allowed_role="candidate extraction source for fermionic and muon-decay finite rows",
            acquisition_status="SOURCE_LOCATED_ROW_EXTRACTION_REQUIRED",
            url_hint="https://arxiv.org/abs/hep-ph/0007091",
            note="Source family for complete fermionic two-loop contributions; v15.5 has not extracted numerical APF-bucket rows from it.",
        ),
        SourceCandidate(
            source_id="freitas_heinemeyer_hollik_walter_weiglein_2001_delta_r_review",
            citation_key="Freitas_Heinemeyer_Hollik_Walter_Weiglein_2001",
            source_family="two_loop_delta_r_review_fermion_loops",
            reviewed_status="REVIEWED_REVIEW_SOURCE",
            covers_buckets=(
                "fermionic_nonleading_finite_remainder",
                "mixed_higher_order_EW_QCD_remainder",
                "vertex_box_muon_decay_remainder",
            ),
            component_granularity="review of exact Delta-r and W-mass prediction with fermion-loop corrections",
            numerical_bucket_rows_available_here=False,
            covariance_available_here=False,
            uncertainty_protocol_available_here=False,
            allowed_role="cross-reference and sign-convention audit source",
            acquisition_status="SOURCE_LOCATED_ROW_EXTRACTION_REQUIRED",
            url_hint="https://arxiv.org/abs/hep-ph/0101260",
            note="Useful for checking conventions and fermion-loop scope; not yet a row payload.",
        ),
        SourceCandidate(
            source_id="awramik_czakon_onishchenko_veretin_2002_bosonic_delta_r",
            citation_key="Awramik_Czakon_Onishchenko_Veretin_2002",
            source_family="bosonic_two_loop_delta_r",
            reviewed_status="REVIEWED_CALCULATION_SOURCE",
            covers_buckets=(
                "bosonic_finite_remainder",
                "vertex_box_muon_decay_remainder",
                "on_shell_counterterm_finite_remainder",
            ),
            component_granularity="two-loop bosonic Delta-r calculation with on-shell/MS convention checks",
            numerical_bucket_rows_available_here=False,
            covariance_available_here=False,
            uncertainty_protocol_available_here=False,
            allowed_role="candidate extraction source for bosonic and counterterm finite rows",
            acquisition_status="SOURCE_LOCATED_ROW_EXTRACTION_REQUIRED",
            url_hint="https://arxiv.org/abs/hep-ph/0209084",
            note="Source family for bosonic remainder and counterterm convention checks; v15.5 has not extracted machine-checkable numerical rows.",
        ),
        SourceCandidate(
            source_id="denner_2007_ew_renormalization_conventions",
            citation_key="Denner_2007_EW_Techniques",
            source_family="one_loop_electroweak_renormalization_and_counterterms",
            reviewed_status="TECHNICAL_REVIEW_SOURCE",
            covers_buckets=(
                "vertex_box_muon_decay_remainder",
                "on_shell_counterterm_finite_remainder",
            ),
            component_granularity="counterterm and amplitude-decomposition conventions",
            numerical_bucket_rows_available_here=False,
            covariance_available_here=False,
            uncertainty_protocol_available_here=False,
            allowed_role="notation and counterterm convention audit source",
            acquisition_status="SOURCE_LOCATED_CONVENTION_MAP_REQUIRED",
            url_hint="https://arxiv.org/abs/0709.1075",
            note="Convention support only; not a Delta-r numerical component source by itself.",
        ),
        SourceCandidate(
            source_id="acfw_2003_precise_w_mass_total",
            citation_key="Awramik_Czakon_Freitas_Weiglein_2004_MW",
            source_family="precision_total_SM_W_mass_parametrization",
            reviewed_status="REVIEWED_PRECISION_TOTAL_SOURCE",
            covers_buckets=(
                "fermionic_nonleading_finite_remainder",
                "bosonic_finite_remainder",
                "mixed_higher_order_EW_QCD_remainder",
                "covariance_and_export_uncertainty_remainder",
            ),
            component_granularity="combined complete two-loop plus known higher-order total",
            numerical_bucket_rows_available_here=False,
            covariance_available_here=False,
            uncertainty_protocol_available_here=True,
            allowed_role="total benchmark and theory-uncertainty scale only",
            acquisition_status="TOTAL_SOURCE_NOT_COMPONENT_DECOMPOSITION",
            url_hint="https://arxiv.org/abs/hep-ph/0311148",
            note="Precision total is already used upstream; it cannot be re-labeled as a finite-part bucket decomposition.",
        ),
        SourceCandidate(
            source_id="sirlin_marciano_radiative_correction_lineage",
            citation_key="Sirlin_2013_Radiative_Corrections_RMP",
            source_family="radiative_corrections_lineage_and_on_shell_context",
            reviewed_status="REVIEWED_CONTEXT_SOURCE",
            covers_buckets=(
                "vertex_box_muon_decay_remainder",
                "on_shell_counterterm_finite_remainder",
                "covariance_and_export_uncertainty_remainder",
            ),
            component_granularity="historical/on-shell context, not component table",
            numerical_bucket_rows_available_here=False,
            covariance_available_here=False,
            uncertainty_protocol_available_here=False,
            allowed_role="lineage and notation/context source only",
            acquisition_status="SOURCE_LOCATED_CONTEXT_ONLY",
            url_hint="https://arxiv.org/abs/1210.5296",
            note="Helpful for paper positioning and scheme discipline; not an APF row source.",
        ),
    )


def source_candidate_ids() -> Tuple[str, ...]:
    return tuple(s.source_id for s in source_candidates())


def candidates_for_bucket(bucket_id: str) -> Tuple[SourceCandidate, ...]:
    return tuple(s for s in source_candidates() if bucket_id in s.covers_buckets)


def bucket_acquisition_rows() -> Tuple[BucketAcquisitionRow, ...]:
    required = {b.bucket_id: b.required_components for b in remainder_bucket_rows()}
    rows = []
    for bid in REMAINDER_BUCKET_ORDER:
        cands = candidates_for_bucket(bid)
        row_extracted = any(c.numerical_bucket_rows_available_here for c in cands)
        covariance = any(c.covariance_available_here for c in cands)
        uncertainty = any(c.uncertainty_protocol_available_here for c in cands)
        # v15.5 never admits rows: source discovery is not row extraction.
        row_admitted = False
        sum_certified = False
        export_eligible = False
        blocker = "ROW_EXTRACTION_REQUIRED" if cands else "NO_REVIEWED_SOURCE_LOCATED"
        if row_extracted and not row_admitted:
            blocker = "ROW_ADMISSION_REQUIRED"
        if not covariance:
            blocker += "__COVARIANCE_REQUIRED"
        if not uncertainty:
            blocker += "__UNCERTAINTY_PROTOCOL_REQUIRED"
        rows.append(BucketAcquisitionRow(
            bucket_id=bid,
            required_components=tuple(required[bid]),
            source_candidates=tuple(c.source_id for c in cands),
            source_located=bool(cands),
            row_extracted=row_extracted,
            row_admitted=row_admitted,
            component_sum_certified=sum_certified,
            covariance_certified=covariance and row_admitted,
            uncertainty_certified=uncertainty and row_admitted,
            export_eligible=export_eligible,
            blocker=blocker,
        ))
    return tuple(rows)


def promotion_matrix() -> Tuple[Dict[str, Any], ...]:
    rows = []
    for r in bucket_acquisition_rows():
        states = {
            "SOURCE_LOCATED": r.source_located,
            "ROW_EXTRACTED": r.row_extracted,
            "ROW_ADMITTED": r.row_admitted,
            "SUM_CERTIFIED": r.component_sum_certified,
            "COVARIANCE_CERTIFIED": r.covariance_certified,
            "UNCERTAINTY_CERTIFIED": r.uncertainty_certified,
            "EXPORT_ELIGIBLE": r.export_eligible,
        }
        rows.append({
            "bucket_id": r.bucket_id,
            "states": states,
            "first_failed_required_state": next((s for s in PROMOTION_REQUIRED_STATES if not states[s]), None),
            "blocker": r.blocker,
        })
    return tuple(rows)


def source_coverage_matrix() -> Dict[str, Any]:
    by_bucket = {}
    for bid in REMAINDER_BUCKET_ORDER:
        cands = candidates_for_bucket(bid)
        by_bucket[bid] = {
            "candidate_count": len(cands),
            "source_ids": tuple(c.source_id for c in cands),
            "families": tuple(c.source_family for c in cands),
            "has_reviewed_source": bool(cands),
            "has_numerical_rows": any(c.numerical_bucket_rows_available_here for c in cands),
            "has_covariance": any(c.covariance_available_here for c in cands),
            "has_uncertainty_protocol": any(c.uncertainty_protocol_available_here for c in cands),
        }
    return by_bucket


def extraction_protocol() -> Tuple[Dict[str, Any], ...]:
    return (
        {"step": 1, "action": "extract source-local notation", "exit_condition": "component symbols and signs mapped to APF eight-slot names"},
        {"step": 2, "action": "extract or reproduce numerical finite-part rows", "exit_condition": "each required bucket has a numerical value and uncertainty, with units and input dependencies"},
        {"step": 3, "action": "certify no target observable as input", "exit_condition": "no observed W-mass or APF anchor used to fit any row"},
        {"step": 4, "action": "certify component sum", "exit_condition": "rows reproduce the declared Delta-r total within stated tolerance"},
        {"step": 5, "action": "certify covariance or independence", "exit_condition": "real covariance matrix or explicit independence proof supplied"},
        {"step": 6, "action": "push uncertainty through M_W solver", "exit_condition": "Delta-r covariance propagated to M_W uncertainty"},
        {"step": 7, "action": "release physical-export candidate", "exit_condition": "all promotion states true and export lock explicitly re-evaluated"},
    )


def numeric_context() -> Dict[str, Any]:
    cw = crosswalk_report()
    jac = float(transport_sensitivity_at_trace()["dM_W_dDelta_r_GeV"])
    return {
        "Delta_r0_proxy": PDG_DELTA_R0,
        "Delta_r0_proxy_sigma": PDG_DELTA_R0_SIGMA,
        "rho_t_normalization": PDG_RHO_T_NORMALIZATION,
        "numeric_proxy_subtotal": numeric_proxy_subtotal(),
        "source_remainder_after_proxies": source_remainder(),
        "apf_trace_remainder_after_proxies": apf_trace_remainder_after_proxies(),
        "source_minus_apf_delta_r_gap": source_minus_apf_delta_r_gap(),
        "source_minus_apf_gap_MW_shift_MeV": cw["source_minus_apf_gap_MW_shift_MeV"],
        "dM_W_dDelta_r_GeV": jac,
    }


def component_sum_status_after_acquisition_matrix() -> Dict[str, Any]:
    cert = component_sum_certificate_report(
        rows=None,
        rows_admitted=False,
        covariance_supplied=False,
        uncertainty_supplied=False,
        physical_export_requested=False,
    )
    return {
        "component_sum_certified": False,
        "reason": "source acquisition located reviewed families but did not extract/admit numerical APF finite-part rows",
        "certificate": cert,
    }


def uncertainty_status_after_acquisition_matrix() -> Dict[str, Any]:
    return {
        "certified_export_uncertainty": False,
        "reason": "no row covariance matrix and no bucket-level uncertainty protocol are admitted",
        "uncertainty_propagation_report": uncertainty_propagation_report(cov=None, physical_export_requested=False),
    }


def obstruction_report() -> Dict[str, Any]:
    blocked = tuple(r for r in bucket_acquisition_rows() if not r.export_eligible)
    return {
        "status": STATUS,
        "physical_W_export_ready": False,
        "exports_physical_M_W": False,
        "upstream_blockers": V154_BLOCKERS,
        "external_source_requirements": EXTERNAL_SOURCE_REQUIREMENTS,
        "bucket_blockers": tuple(asdict(r) for r in blocked),
        "sharp_obstruction": "reviewed source families are located, but no bucket has an admitted numerical row bundle with component-sum, covariance, and uncertainty certificates",
    }


def acquisition_matrix_report() -> Dict[str, Any]:
    artifact = {
        "status": STATUS,
        "version": VERSION,
        "payload_id": PAYLOAD_ID,
        "title": TITLE,
        "upstream_required": "P_w_delta_r_remainder_resolution",
        "source_candidates": tuple(asdict(s) for s in source_candidates()),
        "source_coverage_matrix": source_coverage_matrix(),
        "bucket_acquisition_rows": tuple(asdict(r) for r in bucket_acquisition_rows()),
        "promotion_matrix": promotion_matrix(),
        "extraction_protocol": extraction_protocol(),
        "numeric_context": numeric_context(),
        "component_sum_status": component_sum_status_after_acquisition_matrix(),
        "uncertainty_status": uncertainty_status_after_acquisition_matrix(),
        "physical_export_lock": export_lock_report(physical_export_requested=False),
        "obstruction_report": obstruction_report(),
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "claim_boundary": "reviewed-source acquisition matrix closed; numerical APF finite-part row payload remains open",
    }
    artifact["payload_digest"] = _digest(artifact)
    return artifact


def terminal_report() -> Dict[str, Any]:
    return {
        "status": STATUS,
        "version": VERSION,
        "title": TITLE,
        "report": acquisition_matrix_report(),
        "verdict": "P_source_acquisition_matrix_plus_P_sharp_row_extraction_obstruction__not_physical_export",
    }


# --- Checks -----------------------------------------------------------------

def check_T_w_delta_r_source_acquisition_matrix_status_declared():
    r = acquisition_matrix_report()
    return _res("status_declared", r["status"] == STATUS and r["version"] == VERSION and not r["physical_W_export_enabled"])


def check_T_w_delta_r_source_acquisition_matrix_depends_on_v154():
    d = _check_v154()
    return _res("depends_on_v154", _passed(d), upstream=d.get("status"), upstream_check=d.get("check"))


def check_T_w_delta_r_source_acquisition_matrix_candidate_ids_unique():
    ids = source_candidate_ids()
    return _res("candidate_ids_unique", len(ids) == len(set(ids)) and len(ids) == 7, candidate_ids=ids)


def check_T_w_delta_r_source_acquisition_matrix_candidates_have_citations():
    ok = all(s.citation_key and s.url_hint.startswith("https://") for s in source_candidates())
    return _res("candidates_have_citations", ok)


def check_T_w_delta_r_source_acquisition_matrix_candidate_roles_not_export():
    ok = all("export" not in s.allowed_role.lower() or "not" in s.allowed_role.lower() for s in source_candidates())
    return _res("candidate_roles_not_export", ok, roles=tuple(s.allowed_role for s in source_candidates()))


def check_T_w_delta_r_source_acquisition_matrix_bucket_coverage_complete():
    cov = source_coverage_matrix()
    ok = tuple(cov.keys()) == REMAINDER_BUCKET_ORDER and all(cov[b]["has_reviewed_source"] for b in REMAINDER_BUCKET_ORDER)
    return _res("bucket_coverage_complete", ok, coverage=cov)


def check_T_w_delta_r_source_acquisition_matrix_each_bucket_has_multiple_source_paths_where_possible():
    cov = source_coverage_matrix()
    ok = all(cov[b]["candidate_count"] >= 2 for b in REMAINDER_BUCKET_ORDER)
    return _res("each_bucket_has_multiple_source_paths_where_possible", ok, counts={b: cov[b]["candidate_count"] for b in REMAINDER_BUCKET_ORDER})


def check_T_w_delta_r_source_acquisition_matrix_fermionic_bucket_has_complete_fermionic_source():
    ids = set(source_coverage_matrix()["fermionic_nonleading_finite_remainder"]["source_ids"])
    return _res("fermionic_bucket_has_complete_fermionic_source", "freitas_hollik_walter_weiglein_2000_complete_fermionic" in ids)


def check_T_w_delta_r_source_acquisition_matrix_bosonic_bucket_has_bosonic_source():
    ids = set(source_coverage_matrix()["bosonic_finite_remainder"]["source_ids"])
    return _res("bosonic_bucket_has_bosonic_source", "awramik_czakon_onishchenko_veretin_2002_bosonic_delta_r" in ids)


def check_T_w_delta_r_source_acquisition_matrix_counterterm_bucket_has_convention_source():
    ids = set(source_coverage_matrix()["on_shell_counterterm_finite_remainder"]["source_ids"])
    return _res("counterterm_bucket_has_convention_source", "denner_2007_ew_renormalization_conventions" in ids)


def check_T_w_delta_r_source_acquisition_matrix_acfw_quarantined_as_total():
    acfw = [s for s in source_candidates() if s.source_id == "acfw_2003_precise_w_mass_total"][0]
    ok = acfw.component_granularity.startswith("combined") and not acfw.numerical_bucket_rows_available_here and acfw.acquisition_status == "TOTAL_SOURCE_NOT_COMPONENT_DECOMPOSITION"
    return _res("acfw_quarantined_as_total", ok, acfw=asdict(acfw))


def check_T_w_delta_r_source_acquisition_matrix_no_candidate_claims_numerical_bucket_rows():
    ok = not any(s.numerical_bucket_rows_available_here for s in source_candidates())
    return _res("no_candidate_claims_numerical_bucket_rows", ok)


def check_T_w_delta_r_source_acquisition_matrix_no_candidate_supplies_covariance_rows():
    ok = not any(s.covariance_available_here for s in source_candidates())
    return _res("no_candidate_supplies_covariance_rows", ok)


def check_T_w_delta_r_source_acquisition_matrix_uncertainty_protocol_total_only():
    cands = [s for s in source_candidates() if s.uncertainty_protocol_available_here]
    ok = len(cands) == 1 and cands[0].source_id == "acfw_2003_precise_w_mass_total"
    return _res("uncertainty_protocol_total_only", ok, candidates=tuple(s.source_id for s in cands))


def check_T_w_delta_r_source_acquisition_matrix_bucket_rows_shape():
    rows = bucket_acquisition_rows()
    return _res("bucket_rows_shape", tuple(r.bucket_id for r in rows) == REMAINDER_BUCKET_ORDER and len(rows) == 6)


def check_T_w_delta_r_source_acquisition_matrix_bucket_rows_source_located_not_extracted():
    rows = bucket_acquisition_rows()
    ok = all(r.source_located and not r.row_extracted and not r.row_admitted for r in rows)
    return _res("bucket_rows_source_located_not_extracted", ok, rows=tuple(asdict(r) for r in rows))


def check_T_w_delta_r_source_acquisition_matrix_promotion_matrix_all_blocked_at_extraction():
    pm = promotion_matrix()
    ok = all(r["first_failed_required_state"] == "ROW_EXTRACTED" for r in pm)
    return _res("promotion_matrix_all_blocked_at_extraction", ok, promotion_matrix=pm)


def check_T_w_delta_r_source_acquisition_matrix_row_state_ladder_declared():
    ok = ROW_STATES[0] == "SOURCE_LOCATED" and ROW_STATES[-1] == "EXPORT_ELIGIBLE" and "ROW_ADMITTED" in ROW_STATES
    return _res("row_state_ladder_declared", ok, row_states=ROW_STATES)


def check_T_w_delta_r_source_acquisition_matrix_extraction_protocol_ordered():
    p = extraction_protocol()
    ok = tuple(row["step"] for row in p) == tuple(range(1, 8)) and p[-1]["action"].startswith("release")
    return _res("extraction_protocol_ordered", ok, protocol=p)


def check_T_w_delta_r_source_acquisition_matrix_numeric_context_matches_v154():
    ctx = numeric_context()
    cw = crosswalk_report()
    ok = abs(ctx["source_remainder_after_proxies"] - cw["source_remainder_after_proxies"]) < 1e-18 and abs(ctx["source_minus_apf_delta_r_gap"] - cw["source_minus_apf_delta_r_gap"]) < 1e-18
    return _res("numeric_context_matches_v154", ok, context=ctx)


def check_T_w_delta_r_source_acquisition_matrix_gap_remains_localized():
    ctx = numeric_context()
    diff = ctx["source_remainder_after_proxies"] - ctx["apf_trace_remainder_after_proxies"]
    ok = abs(diff - ctx["source_minus_apf_delta_r_gap"]) < 1e-18
    return _res("gap_remains_localized", ok, remainder_gap=diff, total_gap=ctx["source_minus_apf_delta_r_gap"])


def check_T_w_delta_r_source_acquisition_matrix_mw_shift_unchanged():
    ctx = numeric_context()
    recomputed = float(transport_sensitivity_at_trace()["dM_W_dDelta_r_GeV"]) * ctx["source_minus_apf_delta_r_gap"] * 1000.0
    ok = abs(recomputed - ctx["source_minus_apf_gap_MW_shift_MeV"]) < 1e-12
    return _res("mw_shift_unchanged", ok, recomputed=recomputed, stored=ctx["source_minus_apf_gap_MW_shift_MeV"])


def check_T_w_delta_r_source_acquisition_matrix_component_sum_still_blocked():
    cert = component_sum_status_after_acquisition_matrix()["certificate"]
    ok = not cert["component_sum_certified"] and "NO_COMPONENT_ROWS_SUPPLIED" in cert["failure_reasons"]
    return _res("component_sum_still_blocked", ok, certificate=cert)


def check_T_w_delta_r_source_acquisition_matrix_uncertainty_still_blocked():
    u = uncertainty_status_after_acquisition_matrix()
    ok = not u["certified_export_uncertainty"]
    return _res("uncertainty_still_blocked", ok, uncertainty=u)


def check_T_w_delta_r_source_acquisition_matrix_export_lock_preserved():
    lock = acquisition_matrix_report()["physical_export_lock"]
    ok = not lock.get("physical_W_export_enabled", True) and not lock.get("exports_physical_M_W", True)
    return _res("export_lock_preserved", ok, export_lock=lock)


def check_T_w_delta_r_source_acquisition_matrix_no_forbidden_tokens():
    # Inspect the newly introduced source/acquisition payload only.  Upstream
    # export-lock reports intentionally carry forbidden-token policy lists, so
    # including those policy constants here would make the audit fail for the
    # wrong reason.
    safe = {
        "source_candidates": tuple(asdict(s) for s in source_candidates()),
        "bucket_acquisition_rows": tuple(asdict(r) for r in bucket_acquisition_rows()),
        "promotion_matrix": promotion_matrix(),
        "extraction_protocol": extraction_protocol(),
        "claim_boundary": acquisition_matrix_report()["claim_boundary"],
    }
    return _res("no_forbidden_tokens", not _contains_forbidden_token(safe))


def check_T_w_delta_r_source_acquisition_matrix_obstruction_is_sharper_than_v154():
    obs = obstruction_report()
    ok = "reviewed source families are located" in obs["sharp_obstruction"] and len(obs["bucket_blockers"]) == 6
    return _res("obstruction_is_sharper_than_v154", ok, obstruction=obs)


def check_T_w_delta_r_source_acquisition_matrix_claim_boundary_not_export():
    r = acquisition_matrix_report()
    ok = "remains open" in r["claim_boundary"] and not r["exports_physical_M_W"]
    return _res("claim_boundary_not_export", ok, boundary=r["claim_boundary"])


def check_T_w_delta_r_source_acquisition_matrix_digest_stable():
    d1 = acquisition_matrix_report()["payload_digest"]
    d2 = acquisition_matrix_report()["payload_digest"]
    return _res("digest_stable", d1 == d2 and d1.startswith("sha256:"), digest=d1)


def check_T_w_delta_r_source_acquisition_matrix_terminal_verdict():
    r = terminal_report()
    ok = r["verdict"] == "P_source_acquisition_matrix_plus_P_sharp_row_extraction_obstruction__not_physical_export"
    return _res("terminal_verdict", ok, verdict=r["verdict"])


def check_T_w_delta_r_source_acquisition_matrix_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_delta_r_source_acquisition_matrix_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))


_CHECKS = {
    "check_T_w_delta_r_source_acquisition_matrix_status_declared": check_T_w_delta_r_source_acquisition_matrix_status_declared,
    "check_T_w_delta_r_source_acquisition_matrix_depends_on_v154": check_T_w_delta_r_source_acquisition_matrix_depends_on_v154,
    "check_T_w_delta_r_source_acquisition_matrix_candidate_ids_unique": check_T_w_delta_r_source_acquisition_matrix_candidate_ids_unique,
    "check_T_w_delta_r_source_acquisition_matrix_candidates_have_citations": check_T_w_delta_r_source_acquisition_matrix_candidates_have_citations,
    "check_T_w_delta_r_source_acquisition_matrix_candidate_roles_not_export": check_T_w_delta_r_source_acquisition_matrix_candidate_roles_not_export,
    "check_T_w_delta_r_source_acquisition_matrix_bucket_coverage_complete": check_T_w_delta_r_source_acquisition_matrix_bucket_coverage_complete,
    "check_T_w_delta_r_source_acquisition_matrix_each_bucket_has_multiple_source_paths_where_possible": check_T_w_delta_r_source_acquisition_matrix_each_bucket_has_multiple_source_paths_where_possible,
    "check_T_w_delta_r_source_acquisition_matrix_fermionic_bucket_has_complete_fermionic_source": check_T_w_delta_r_source_acquisition_matrix_fermionic_bucket_has_complete_fermionic_source,
    "check_T_w_delta_r_source_acquisition_matrix_bosonic_bucket_has_bosonic_source": check_T_w_delta_r_source_acquisition_matrix_bosonic_bucket_has_bosonic_source,
    "check_T_w_delta_r_source_acquisition_matrix_counterterm_bucket_has_convention_source": check_T_w_delta_r_source_acquisition_matrix_counterterm_bucket_has_convention_source,
    "check_T_w_delta_r_source_acquisition_matrix_acfw_quarantined_as_total": check_T_w_delta_r_source_acquisition_matrix_acfw_quarantined_as_total,
    "check_T_w_delta_r_source_acquisition_matrix_no_candidate_claims_numerical_bucket_rows": check_T_w_delta_r_source_acquisition_matrix_no_candidate_claims_numerical_bucket_rows,
    "check_T_w_delta_r_source_acquisition_matrix_no_candidate_supplies_covariance_rows": check_T_w_delta_r_source_acquisition_matrix_no_candidate_supplies_covariance_rows,
    "check_T_w_delta_r_source_acquisition_matrix_uncertainty_protocol_total_only": check_T_w_delta_r_source_acquisition_matrix_uncertainty_protocol_total_only,
    "check_T_w_delta_r_source_acquisition_matrix_bucket_rows_shape": check_T_w_delta_r_source_acquisition_matrix_bucket_rows_shape,
    "check_T_w_delta_r_source_acquisition_matrix_bucket_rows_source_located_not_extracted": check_T_w_delta_r_source_acquisition_matrix_bucket_rows_source_located_not_extracted,
    "check_T_w_delta_r_source_acquisition_matrix_promotion_matrix_all_blocked_at_extraction": check_T_w_delta_r_source_acquisition_matrix_promotion_matrix_all_blocked_at_extraction,
    "check_T_w_delta_r_source_acquisition_matrix_row_state_ladder_declared": check_T_w_delta_r_source_acquisition_matrix_row_state_ladder_declared,
    "check_T_w_delta_r_source_acquisition_matrix_extraction_protocol_ordered": check_T_w_delta_r_source_acquisition_matrix_extraction_protocol_ordered,
    "check_T_w_delta_r_source_acquisition_matrix_numeric_context_matches_v154": check_T_w_delta_r_source_acquisition_matrix_numeric_context_matches_v154,
    "check_T_w_delta_r_source_acquisition_matrix_gap_remains_localized": check_T_w_delta_r_source_acquisition_matrix_gap_remains_localized,
    "check_T_w_delta_r_source_acquisition_matrix_mw_shift_unchanged": check_T_w_delta_r_source_acquisition_matrix_mw_shift_unchanged,
    "check_T_w_delta_r_source_acquisition_matrix_component_sum_still_blocked": check_T_w_delta_r_source_acquisition_matrix_component_sum_still_blocked,
    "check_T_w_delta_r_source_acquisition_matrix_uncertainty_still_blocked": check_T_w_delta_r_source_acquisition_matrix_uncertainty_still_blocked,
    "check_T_w_delta_r_source_acquisition_matrix_export_lock_preserved": check_T_w_delta_r_source_acquisition_matrix_export_lock_preserved,
    "check_T_w_delta_r_source_acquisition_matrix_no_forbidden_tokens": check_T_w_delta_r_source_acquisition_matrix_no_forbidden_tokens,
    "check_T_w_delta_r_source_acquisition_matrix_obstruction_is_sharper_than_v154": check_T_w_delta_r_source_acquisition_matrix_obstruction_is_sharper_than_v154,
    "check_T_w_delta_r_source_acquisition_matrix_claim_boundary_not_export": check_T_w_delta_r_source_acquisition_matrix_claim_boundary_not_export,
    "check_T_w_delta_r_source_acquisition_matrix_digest_stable": check_T_w_delta_r_source_acquisition_matrix_digest_stable,
    "check_T_w_delta_r_source_acquisition_matrix_terminal_verdict": check_T_w_delta_r_source_acquisition_matrix_terminal_verdict,
    "check_T_w_delta_r_source_acquisition_matrix_bank_closure": check_T_w_delta_r_source_acquisition_matrix_bank_closure,
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
    print("source_remainder_after_proxies", f"{ctx['source_remainder_after_proxies']:.12f}")
    print("apf_trace_remainder_after_proxies", f"{ctx['apf_trace_remainder_after_proxies']:.12f}")
    print("source_minus_apf_gap_MW_shift_MeV", f"{ctx['source_minus_apf_gap_MW_shift_MeV']:.6f}")
    raise SystemExit(0 if out["passed"] else 1)
