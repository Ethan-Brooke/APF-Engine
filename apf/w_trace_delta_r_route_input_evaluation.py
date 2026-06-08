"""W_TRACE Delta_r APF-route-input evaluation and uncertainty propagation.

v15.7 (2026-05-09): evaluates the reviewed ACFW Table-1 Delta-r
component rows at the APF route input point using an explicit, auditable
transport model.  This is the first same-input numerical row-transfer layer:
it pushes the source-local ACFW row shape to (i) the ACFW standard-total value
computed on the APF route input ledger and (ii) the APF_TRACE Delta-r anchor,
and it propagates the quoted source-scale W-theory uncertainty through the
on-shell Delta-r -> M_W Jacobian.

Closed here:
    * route input point declared from the v15.2 on-shell ledger;
    * ACFW source-local row bundle transported to APF-route totals;
    * route-point component sums certified for the transport model;
    * rank-one correlated and diagonal reference covariance matrices built;
    * Delta-r and M_W uncertainty propagation computed numerically;
    * export-candidate status is blocked because the per-row transport map is
      a model transfer, not a reviewed source-evaluated same-input finite-part
      calculation.

Still open here:
    physical M_W export.  A reviewed component-level evaluator at the APF route
    input point, with source-provided row covariance/counterterm decomposition,
    is still required before the W route can be promoted beyond a model-limited
    same-input worksheet.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from decimal import Decimal, getcontext
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_delta_r_row_extraction_closeout import (
    extracted_acfw_rows,
    extracted_row_sum,
    source_local_component_sum_certificate,
    check_T_w_delta_r_row_extraction_closeout_bank_closure as _check_v156,
)
from apf.w_trace_delta_r_transport_buildout import (
    APF_DELTA_R_TARGET,
    M_W_TRACE_GEV,
    declared_on_shell_inputs,
    mw_from_delta_r,
    dMW_dDelta_r,
    source_vs_trace_transport_values,
    transport_sensitivity_at_trace,
)
from apf.w_trace_standard_delta_r_extraction_worksheet import SOURCE_THEORY_UNCERTAINTY_MEV
from apf.w_trace_component_sum_certificate import component_sum_certificate_report
from apf.w_trace_uncertainty_propagation import uncertainty_propagation_report, CovarianceMatrixRecord
from apf.w_trace_physical_export_lock import export_lock_report
from apf.w_trace_final_export_readiness import readiness_report

getcontext().prec = 50

STATUS = "P_w_delta_r_route_input_evaluation"
VERSION = "v15_7"
PASS_STATUS = "W_TRACE_DELTA_R_ROUTE_INPUT_EVALUATION_PASS"
TITLE = "W_TRACE Delta_r APF-route-input evaluation with covariance propagation"
PAYLOAD_ID = "W_TRACE_DELTA_R_ROUTE_INPUT_EVALUATION_v15_7"

ROW_ORDER: Tuple[str, ...] = tuple(r.row_id for r in extracted_acfw_rows())
ROW_SYMBOLS: Dict[str, str] = {r.row_id: r.source_symbol for r in extracted_acfw_rows()}
MODEL_STATUS = "MODEL_TRANSFERRED_TO_APF_ROUTE_INPUT_NOT_REVIEWED_ROW_EVALUATOR"

FORBIDDEN_TOKENS: Tuple[str, ...] = (
    "observed_M_W", "world_average_M_W", "CDF_II_M_W", "CMS_observed_M_W",
    "fit_to_observed_W", "row_residual_tuned_to_measurement", "manual_export_override",
    "physical_export_unlock", "component_rows_claimed_reviewed_same_input",
)

@dataclass(frozen=True)
class RouteInputPoint:
    point_id: str
    alpha_inverse: float
    G_F_GeV_minus2: float
    M_Z_GeV: float
    M_W_TRACE_GeV: float
    Delta_r_APF_TRACE: float
    Delta_r_source_total_at_route_inputs: float
    M_W_source_total_at_route_inputs_GeV: float
    role: str

@dataclass(frozen=True)
class TransferredRow:
    row_id: str
    source_symbol: str
    source_local_value: float
    source_local_weight: float
    transfer_target: str
    transfer_factor: float
    value_at_route_input: float
    covariance_sigma_delta_r: float
    covariance_sigma_MW_MeV: float
    transport_status: str
    reviewed_same_input_row: bool
    admitted_for_physical_export: bool

@dataclass(frozen=True)
class CovarianceSummary:
    target: str
    model: str
    sigma_delta_r: float
    sigma_MW_MeV: float
    rank: int
    source_uncertainty_MeV: float
    notes: str


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
    return any(tok in text for tok in FORBIDDEN_TOKENS)


def route_input_point() -> RouteInputPoint:
    inp = declared_on_shell_inputs()
    vals = source_vs_trace_transport_values()
    return RouteInputPoint(
        point_id="APF_TRACE_ON_SHELL_ROUTE_INPUT_POINT_v15_7",
        alpha_inverse=float(inp.alpha_inverse),
        G_F_GeV_minus2=float(inp.G_F_GeV_minus2),
        M_Z_GeV=float(inp.M_Z_GeV),
        M_W_TRACE_GeV=float(M_W_TRACE_GEV),
        Delta_r_APF_TRACE=float(APF_DELTA_R_TARGET),
        Delta_r_source_total_at_route_inputs=float(vals["Delta_r_source_total"]),
        M_W_source_total_at_route_inputs_GeV=float(vals["M_W_source_GeV"]),
        role="same declared non-W route inputs; APF trace anchor is a comparison target, not an observed-W source input",
    )


def source_local_sum() -> float:
    return float(extracted_row_sum())


def source_total_transfer_factor() -> float:
    return route_input_point().Delta_r_source_total_at_route_inputs / source_local_sum()


def apf_trace_transfer_factor() -> float:
    return route_input_point().Delta_r_APF_TRACE / source_local_sum()


def row_weights() -> Dict[str, float]:
    total = source_local_sum()
    return {r.row_id: float(r.value) / total for r in extracted_acfw_rows()}


def sigma_delta_r_source_scale() -> float:
    jac = abs(float(transport_sensitivity_at_trace()["dM_W_dDelta_r_GeV"]))
    return (float(SOURCE_THEORY_UNCERTAINTY_MEV) / 1000.0) / jac


def transferred_rows(target: str = "APF_TRACE_TARGET_TOTAL") -> Tuple[TransferredRow, ...]:
    if target == "APF_TRACE_TARGET_TOTAL":
        total = route_input_point().Delta_r_APF_TRACE
        factor = apf_trace_transfer_factor()
    elif target == "ACFW_SOURCE_TOTAL_AT_ROUTE_INPUTS":
        total = route_input_point().Delta_r_source_total_at_route_inputs
        factor = source_total_transfer_factor()
    else:
        raise ValueError("unknown transfer target")
    weights = row_weights()
    sigma_dr = sigma_delta_r_source_scale()
    jac_mev = abs(float(transport_sensitivity_at_trace()["dM_W_dDelta_r_GeV"])) * 1000.0
    rows = []
    for r in extracted_acfw_rows():
        w = weights[r.row_id]
        row_sigma_dr = abs(w) * sigma_dr
        rows.append(TransferredRow(
            row_id=r.row_id,
            source_symbol=r.source_symbol,
            source_local_value=float(r.value),
            source_local_weight=float(w),
            transfer_target=target,
            transfer_factor=float(factor),
            value_at_route_input=float(r.value) * float(factor),
            covariance_sigma_delta_r=float(row_sigma_dr),
            covariance_sigma_MW_MeV=float(row_sigma_dr * jac_mev),
            transport_status=MODEL_STATUS,
            reviewed_same_input_row=False,
            admitted_for_physical_export=False,
        ))
    # Guard against silent drift in total argument.
    assert abs(sum(x.value_at_route_input for x in rows) - total) < 1e-14
    return tuple(rows)


def transferred_sum(target: str = "APF_TRACE_TARGET_TOTAL") -> float:
    return sum(r.value_at_route_input for r in transferred_rows(target))


def rank_one_covariance_matrix(target: str = "APF_TRACE_TARGET_TOTAL") -> Tuple[Tuple[float, ...], ...]:
    sig = sigma_delta_r_source_scale()
    ws = [row_weights()[rid] for rid in ROW_ORDER]
    return tuple(tuple(float(ws[i] * ws[j] * sig * sig) for j in range(len(ws))) for i in range(len(ws)))


def diagonal_reference_covariance_matrix(target: str = "APF_TRACE_TARGET_TOTAL") -> Tuple[Tuple[float, ...], ...]:
    sig = sigma_delta_r_source_scale()
    ws = [abs(row_weights()[rid]) for rid in ROW_ORDER]
    return tuple(tuple(float((ws[i] * sig) ** 2) if i == j else 0.0 for j in range(len(ws))) for i in range(len(ws)))


def covariance_sigma_delta_r(matrix: Tuple[Tuple[float, ...], ...]) -> float:
    v = sum(sum(row) for row in matrix)
    if v < -1e-30:
        raise ValueError("negative total variance")
    return math.sqrt(max(0.0, v))


def covariance_summary(target: str = "APF_TRACE_TARGET_TOTAL", model: str = "rank_one_correlated_source_theory") -> CovarianceSummary:
    mat = rank_one_covariance_matrix(target) if model == "rank_one_correlated_source_theory" else diagonal_reference_covariance_matrix(target)
    sigma_dr = covariance_sigma_delta_r(mat)
    jac = abs(float(transport_sensitivity_at_trace()["dM_W_dDelta_r_GeV"]))
    return CovarianceSummary(
        target=target,
        model=model,
        sigma_delta_r=float(sigma_dr),
        sigma_MW_MeV=float(sigma_dr * jac * 1000.0),
        rank=1 if model == "rank_one_correlated_source_theory" else len(ROW_ORDER),
        source_uncertainty_MeV=float(SOURCE_THEORY_UNCERTAINTY_MEV),
        notes="rank-one model treats the ACFW theory scale as a coherent normalization uncertainty over the transported row shape; diagonal model is a reference only",
    )


def perturbative_covariance_record_for_harness(target: str = "APF_TRACE_TARGET_TOTAL") -> CovarianceMatrixRecord:
    # Deliberately not in APF finite-part component order, so the legacy APF
    # export harness must reject it.  This proves the row transfer is a
    # perturbative-family worksheet, not a certified APF export bundle.
    mat = rank_one_covariance_matrix(target)
    return CovarianceMatrixRecord(
        component_order=ROW_ORDER,
        matrix_kind="rank_one_correlated_acfw_row_shape_model_not_apf_component_order",
        entries=tuple(tuple(f"{x:.17E}" for x in row) for row in mat),
        units="dimensionless_delta_r_squared",
        provenance_digest=_digest({"target": target, "row_order": ROW_ORDER, "matrix": mat}),
        target_observables_consumed=(),
        apf_target_consumed=False,
    )


def model_component_sum_report(target: str = "APF_TRACE_TARGET_TOTAL") -> Dict[str, Any]:
    # The APF harness should not certify these rows because they are not in APF
    # finite-part component order and not admitted as reviewed APF rows.
    rows = tuple({
        "component_id": r.row_id,
        "symbol": r.source_symbol,
        "numeric_value": f"{r.value_at_route_input:.17E}",
        "uncertainty": f"{r.covariance_sigma_delta_r:.17E}",
        "target_observables_consumed": (),
        "apf_target_consumed": False,
    } for r in transferred_rows(target))
    return component_sum_certificate_report(rows=rows, rows_admitted=False, covariance_supplied=True, uncertainty_supplied=True, physical_export_requested=False)


def model_uncertainty_harness_report(target: str = "APF_TRACE_TARGET_TOTAL") -> Dict[str, Any]:
    cov = perturbative_covariance_record_for_harness(target)
    return uncertainty_propagation_report(cov=cov, covariance_supplied=True, rows_admitted=False, component_sum_certified=False, physical_export_requested=False)


def transport_error_budget() -> Dict[str, Any]:
    source_total = route_input_point().Delta_r_source_total_at_route_inputs
    apf_total = route_input_point().Delta_r_APF_TRACE
    gap = source_total - apf_total
    jac = float(transport_sensitivity_at_trace()["dM_W_dDelta_r_GeV"])
    sigma = covariance_summary("APF_TRACE_TARGET_TOTAL")
    return {
        "Delta_r_source_total_at_route_inputs": source_total,
        "Delta_r_APF_TRACE_target": apf_total,
        "Delta_r_source_minus_APF": gap,
        "M_W_gap_from_jacobian_MeV": gap * jac * 1000.0,
        "abs_M_W_gap_MeV": abs(gap * jac * 1000.0),
        "sigma_delta_r_rank_one": sigma.sigma_delta_r,
        "sigma_MW_MeV_rank_one": sigma.sigma_MW_MeV,
        "pull_source_minus_apf_in_sigma": abs(gap) / sigma.sigma_delta_r if sigma.sigma_delta_r else None,
    }


def export_boundary_report() -> Dict[str, Any]:
    return {
        "route_status": "P_model_limited_same_input_evaluation_plus_uncertainty_propagation",
        "physical_W_export_ready": False,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "first_failed_gate_after_v156": "REVIEWED_PER_ROW_SAME_INPUT_EVALUATOR",
        "closed_in_v157": (
            "APF-route-point transfer factors evaluated",
            "transported perturbative rows sum to APF trace target and ACFW route source total under declared model",
            "rank-one covariance and M_W uncertainty push-forward computed",
        ),
        "remaining_blockers": (
            "ROW_TRANSPORT_IS_SHAPE_MODEL_NOT_REVIEWED_COMPONENT_EVALUATOR",
            "PERTURBATIVE_ROW_ORDER_NOT_APF_FINITE_PART_COMPONENT_ORDER",
            "NO_SOURCE_PROVIDED_ROW_COVARIANCE_MATRIX_AT_APF_INPUTS",
            "NO_REVIEWED_COUNTERTERM_SPLIT_AT_APF_INPUTS",
            "NO_APF_EXPORT_COMPONENT_SUM_CERTIFICATE",
            "PHYSICAL_EXPORT_LOCKED",
        ),
    }


def route_input_evaluation_report() -> Dict[str, Any]:
    artifact = {
        "status": STATUS,
        "version": VERSION,
        "payload_id": PAYLOAD_ID,
        "title": TITLE,
        "upstream_required": "P_w_delta_r_row_extraction_closeout",
        "route_input_point": asdict(route_input_point()),
        "source_local_component_sum_certificate": source_local_component_sum_certificate(),
        "source_local_row_sum": source_local_sum(),
        "source_total_transfer_factor": source_total_transfer_factor(),
        "apf_trace_transfer_factor": apf_trace_transfer_factor(),
        "row_order": ROW_ORDER,
        "row_symbols": ROW_SYMBOLS,
        "row_weights": row_weights(),
        "transferred_rows_apf_trace_target": tuple(asdict(r) for r in transferred_rows("APF_TRACE_TARGET_TOTAL")),
        "transferred_rows_source_total": tuple(asdict(r) for r in transferred_rows("ACFW_SOURCE_TOTAL_AT_ROUTE_INPUTS")),
        "covariance_rank_one_apf_target": tuple(tuple(f"{x:.17E}" for x in row) for row in rank_one_covariance_matrix("APF_TRACE_TARGET_TOTAL")),
        "covariance_diagonal_reference_apf_target": tuple(tuple(f"{x:.17E}" for x in row) for row in diagonal_reference_covariance_matrix("APF_TRACE_TARGET_TOTAL")),
        "covariance_summary_rank_one": asdict(covariance_summary("APF_TRACE_TARGET_TOTAL", "rank_one_correlated_source_theory")),
        "covariance_summary_diagonal_reference": asdict(covariance_summary("APF_TRACE_TARGET_TOTAL", "diagonal_reference_independent_rows")),
        "transport_error_budget": transport_error_budget(),
        "component_sum_harness_report": model_component_sum_report("APF_TRACE_TARGET_TOTAL"),
        "uncertainty_harness_report": model_uncertainty_harness_report("APF_TRACE_TARGET_TOTAL"),
        "physical_export_lock": export_lock_report(physical_export_requested=False),
        "final_readiness": readiness_report(physical_export_requested=False),
        "export_boundary_report": export_boundary_report(),
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "claim_boundary": "same-input model transfer with covariance propagation; not a reviewed APF physical W export",
    }
    artifact["payload_digest"] = _digest(artifact)
    return artifact


def terminal_report() -> Dict[str, Any]:
    return {
        "status": STATUS,
        "version": VERSION,
        "title": TITLE,
        "report": route_input_evaluation_report(),
        "verdict": "P_model_limited_same_input_evaluation_with_covariance_propagation__not_physical_export",
    }

# --- Checks -----------------------------------------------------------------

def check_T_w_delta_r_route_input_evaluation_status_declared():
    r = route_input_evaluation_report()
    return _res("status_declared", r["status"] == STATUS and r["version"] == VERSION and not r["physical_W_export_enabled"])


def check_T_w_delta_r_route_input_evaluation_depends_on_v156():
    d = _check_v156()
    return _res("depends_on_v156", _passed(d), upstream=d.get("status"), upstream_check=d.get("check"))


def check_T_w_delta_r_route_input_evaluation_route_point_declared():
    p = route_input_point()
    ok = p.M_W_TRACE_GeV > 80 and p.M_Z_GeV > p.M_W_TRACE_GeV and p.Delta_r_APF_TRACE > 0
    return _res("route_point_declared", ok, route_input=asdict(p))


def check_T_w_delta_r_route_input_evaluation_source_local_sum_preserved():
    ok = abs(source_local_sum() - 0.035557) < 1e-15
    return _res("source_local_sum_preserved", ok, source_local_sum=source_local_sum())


def check_T_w_delta_r_route_input_evaluation_transfer_factors_positive():
    ok = source_total_transfer_factor() > 1.0 and apf_trace_transfer_factor() > 1.0
    return _res("transfer_factors_positive", ok, source_factor=source_total_transfer_factor(), apf_factor=apf_trace_transfer_factor())


def check_T_w_delta_r_route_input_evaluation_apf_rows_sum_to_apf_target():
    total = transferred_sum("APF_TRACE_TARGET_TOTAL")
    ok = abs(total - float(APF_DELTA_R_TARGET)) < 1e-14
    return _res("apf_rows_sum_to_apf_target", ok, total=total, target=float(APF_DELTA_R_TARGET))


def check_T_w_delta_r_route_input_evaluation_source_rows_sum_to_source_total():
    total = transferred_sum("ACFW_SOURCE_TOTAL_AT_ROUTE_INPUTS")
    target = route_input_point().Delta_r_source_total_at_route_inputs
    ok = abs(total - target) < 1e-14
    return _res("source_rows_sum_to_source_total", ok, total=total, target=target)


def check_T_w_delta_r_route_input_evaluation_eight_rows_transferred():
    rows = transferred_rows("APF_TRACE_TARGET_TOTAL")
    ok = len(rows) == 8 and tuple(r.row_id for r in rows) == ROW_ORDER
    return _res("eight_rows_transferred", ok, rows=tuple(asdict(r) for r in rows))


def check_T_w_delta_r_route_input_evaluation_reviewed_same_input_not_claimed():
    ok = not any(r.reviewed_same_input_row or r.admitted_for_physical_export for r in transferred_rows())
    return _res("reviewed_same_input_not_claimed", ok)


def check_T_w_delta_r_route_input_evaluation_weight_sum_unity():
    s = sum(row_weights().values())
    return _res("weight_sum_unity", abs(s - 1.0) < 1e-14, weight_sum=s)


def check_T_w_delta_r_route_input_evaluation_rank_one_covariance_shape():
    mat = rank_one_covariance_matrix()
    ok = len(mat) == 8 and all(len(row) == 8 for row in mat)
    return _res("rank_one_covariance_shape", ok)


def check_T_w_delta_r_route_input_evaluation_rank_one_covariance_symmetric():
    mat = rank_one_covariance_matrix()
    ok = all(abs(mat[i][j] - mat[j][i]) < 1e-30 for i in range(8) for j in range(8))
    return _res("rank_one_covariance_symmetric", ok)


def check_T_w_delta_r_route_input_evaluation_rank_one_sigma_matches_source_scale():
    sig = covariance_summary().sigma_MW_MeV
    ok = abs(sig - float(SOURCE_THEORY_UNCERTAINTY_MEV)) < 1e-12
    return _res("rank_one_sigma_matches_source_scale", ok, sigma_MW_MeV=sig)


def check_T_w_delta_r_route_input_evaluation_diagonal_reference_is_subconservative():
    rank = covariance_summary(model="rank_one_correlated_source_theory").sigma_delta_r
    diag = covariance_summary(model="diagonal_reference_independent_rows").sigma_delta_r
    ok = diag < rank and diag > 0
    return _res("diagonal_reference_is_subconservative", ok, rank_one_sigma=rank, diagonal_sigma=diag)


def check_T_w_delta_r_route_input_evaluation_uncertainty_pushforward_numeric():
    b = transport_error_budget()
    ok = b["sigma_MW_MeV_rank_one"] > 3.9 and b["sigma_MW_MeV_rank_one"] < 4.1
    return _res("uncertainty_pushforward_numeric", ok, budget=b)


def check_T_w_delta_r_route_input_evaluation_source_apf_pull_under_two_sigma():
    b = transport_error_budget()
    ok = b["pull_source_minus_apf_in_sigma"] is not None and b["pull_source_minus_apf_in_sigma"] < 1.0
    return _res("source_apf_pull_under_two_sigma", ok, budget=b)


def check_T_w_delta_r_route_input_evaluation_component_sum_harness_rejects_model_rows():
    r = model_component_sum_report()
    ok = not r.get("component_sum_certified", True) and "COMPONENT_TABLE_SHAPE_NOT_EXACT_ORDER" in r.get("failure_reasons", ())
    return _res("component_sum_harness_rejects_model_rows", ok, harness=r)


def check_T_w_delta_r_route_input_evaluation_uncertainty_harness_rejects_perturbative_order():
    r = model_uncertainty_harness_report()
    ok = not r.get("uncertainty_propagation_certified", True) and "COVARIANCE_SHAPE_NOT_EXACT_COMPONENT_ORDER" in r.get("failure_reasons", ())
    return _res("uncertainty_harness_rejects_perturbative_order", ok, harness=r)


def check_T_w_delta_r_route_input_evaluation_export_boundary_first_failed_gate():
    e = export_boundary_report()
    ok = e["first_failed_gate_after_v156"] == "REVIEWED_PER_ROW_SAME_INPUT_EVALUATOR"
    return _res("export_boundary_first_failed_gate", ok, boundary=e)


def check_T_w_delta_r_route_input_evaluation_export_lock_preserved():
    lock = route_input_evaluation_report()["physical_export_lock"]
    ok = not lock.get("physical_W_export_enabled", True) and not lock.get("exports_physical_M_W", True)
    return _res("export_lock_preserved", ok, export_lock=lock)


def check_T_w_delta_r_route_input_evaluation_final_readiness_blocked():
    ready = route_input_evaluation_report()["final_readiness"]
    ok = not ready.get("physical_W_export_ready", True) and not ready.get("exports_physical_M_W", True)
    return _res("final_readiness_blocked", ok, readiness=ready)


def check_T_w_delta_r_route_input_evaluation_no_forbidden_tokens():
    r = route_input_evaluation_report()
    safe = {"route_input_point": r["route_input_point"], "rows": r["transferred_rows_apf_trace_target"], "boundary": r["export_boundary_report"]}
    return _res("no_forbidden_tokens", not _contains_forbidden_token(safe))


def check_T_w_delta_r_route_input_evaluation_digest_present():
    d = route_input_evaluation_report()["payload_digest"]
    return _res("digest_present", isinstance(d, str) and d.startswith("sha256:") and len(d) == 71, digest=d)


def check_T_w_delta_r_route_input_evaluation_model_status_on_all_rows():
    ok = all(r.transport_status == MODEL_STATUS for r in transferred_rows())
    return _res("model_status_on_all_rows", ok)


def check_T_w_delta_r_route_input_evaluation_mw_from_apf_target_matches_trace():
    mw = mw_from_delta_r(APF_DELTA_R_TARGET)
    ok = abs(mw - M_W_TRACE_GEV) < 1e-10
    return _res("mw_from_apf_target_matches_trace", ok, mw=mw, trace=M_W_TRACE_GEV)


def check_T_w_delta_r_route_input_evaluation_source_total_mw_preserved():
    p = route_input_point()
    mw = mw_from_delta_r(p.Delta_r_source_total_at_route_inputs)
    ok = abs(mw - p.M_W_source_total_at_route_inputs_GeV) < 1e-12
    return _res("source_total_mw_preserved", ok, mw=mw)


def check_T_w_delta_r_route_input_evaluation_rank_one_covariance_digest_stable():
    cov = perturbative_covariance_record_for_harness()
    ok = cov.provenance_digest.startswith("sha256:") and cov.component_order == ROW_ORDER
    return _res("rank_one_covariance_digest_stable", ok, digest=cov.provenance_digest)


def check_T_w_delta_r_route_input_evaluation_same_input_closed_but_reviewed_open():
    e = export_boundary_report()
    ok = "transported perturbative rows sum" in e["closed_in_v157"][1] and "ROW_TRANSPORT_IS_SHAPE_MODEL_NOT_REVIEWED_COMPONENT_EVALUATOR" in e["remaining_blockers"]
    return _res("same_input_closed_but_reviewed_open", ok, boundary=e)


def check_T_w_delta_r_route_input_evaluation_terminal_verdict():
    v = terminal_report()["verdict"]
    ok = "not_physical_export" in v and "same_input_evaluation" in v
    return _res("terminal_verdict", ok, verdict=v)


def check_T_w_delta_r_route_input_evaluation_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_delta_r_route_input_evaluation_bank_closure"]
    ok = all(_passed(r) for r in rows)
    return _res("bank_closure", ok, passed_count=sum(_passed(r) for r in rows), total=len(rows))


_CHECKS: Dict[str, Any] = {
    "check_T_w_delta_r_route_input_evaluation_status_declared": check_T_w_delta_r_route_input_evaluation_status_declared,
    "check_T_w_delta_r_route_input_evaluation_depends_on_v156": check_T_w_delta_r_route_input_evaluation_depends_on_v156,
    "check_T_w_delta_r_route_input_evaluation_route_point_declared": check_T_w_delta_r_route_input_evaluation_route_point_declared,
    "check_T_w_delta_r_route_input_evaluation_source_local_sum_preserved": check_T_w_delta_r_route_input_evaluation_source_local_sum_preserved,
    "check_T_w_delta_r_route_input_evaluation_transfer_factors_positive": check_T_w_delta_r_route_input_evaluation_transfer_factors_positive,
    "check_T_w_delta_r_route_input_evaluation_apf_rows_sum_to_apf_target": check_T_w_delta_r_route_input_evaluation_apf_rows_sum_to_apf_target,
    "check_T_w_delta_r_route_input_evaluation_source_rows_sum_to_source_total": check_T_w_delta_r_route_input_evaluation_source_rows_sum_to_source_total,
    "check_T_w_delta_r_route_input_evaluation_eight_rows_transferred": check_T_w_delta_r_route_input_evaluation_eight_rows_transferred,
    "check_T_w_delta_r_route_input_evaluation_reviewed_same_input_not_claimed": check_T_w_delta_r_route_input_evaluation_reviewed_same_input_not_claimed,
    "check_T_w_delta_r_route_input_evaluation_weight_sum_unity": check_T_w_delta_r_route_input_evaluation_weight_sum_unity,
    "check_T_w_delta_r_route_input_evaluation_rank_one_covariance_shape": check_T_w_delta_r_route_input_evaluation_rank_one_covariance_shape,
    "check_T_w_delta_r_route_input_evaluation_rank_one_covariance_symmetric": check_T_w_delta_r_route_input_evaluation_rank_one_covariance_symmetric,
    "check_T_w_delta_r_route_input_evaluation_rank_one_sigma_matches_source_scale": check_T_w_delta_r_route_input_evaluation_rank_one_sigma_matches_source_scale,
    "check_T_w_delta_r_route_input_evaluation_diagonal_reference_is_subconservative": check_T_w_delta_r_route_input_evaluation_diagonal_reference_is_subconservative,
    "check_T_w_delta_r_route_input_evaluation_uncertainty_pushforward_numeric": check_T_w_delta_r_route_input_evaluation_uncertainty_pushforward_numeric,
    "check_T_w_delta_r_route_input_evaluation_source_apf_pull_under_two_sigma": check_T_w_delta_r_route_input_evaluation_source_apf_pull_under_two_sigma,
    "check_T_w_delta_r_route_input_evaluation_component_sum_harness_rejects_model_rows": check_T_w_delta_r_route_input_evaluation_component_sum_harness_rejects_model_rows,
    "check_T_w_delta_r_route_input_evaluation_uncertainty_harness_rejects_perturbative_order": check_T_w_delta_r_route_input_evaluation_uncertainty_harness_rejects_perturbative_order,
    "check_T_w_delta_r_route_input_evaluation_export_boundary_first_failed_gate": check_T_w_delta_r_route_input_evaluation_export_boundary_first_failed_gate,
    "check_T_w_delta_r_route_input_evaluation_export_lock_preserved": check_T_w_delta_r_route_input_evaluation_export_lock_preserved,
    "check_T_w_delta_r_route_input_evaluation_final_readiness_blocked": check_T_w_delta_r_route_input_evaluation_final_readiness_blocked,
    "check_T_w_delta_r_route_input_evaluation_no_forbidden_tokens": check_T_w_delta_r_route_input_evaluation_no_forbidden_tokens,
    "check_T_w_delta_r_route_input_evaluation_digest_present": check_T_w_delta_r_route_input_evaluation_digest_present,
    "check_T_w_delta_r_route_input_evaluation_model_status_on_all_rows": check_T_w_delta_r_route_input_evaluation_model_status_on_all_rows,
    "check_T_w_delta_r_route_input_evaluation_mw_from_apf_target_matches_trace": check_T_w_delta_r_route_input_evaluation_mw_from_apf_target_matches_trace,
    "check_T_w_delta_r_route_input_evaluation_source_total_mw_preserved": check_T_w_delta_r_route_input_evaluation_source_total_mw_preserved,
    "check_T_w_delta_r_route_input_evaluation_rank_one_covariance_digest_stable": check_T_w_delta_r_route_input_evaluation_rank_one_covariance_digest_stable,
    "check_T_w_delta_r_route_input_evaluation_same_input_closed_but_reviewed_open": check_T_w_delta_r_route_input_evaluation_same_input_closed_but_reviewed_open,
    "check_T_w_delta_r_route_input_evaluation_terminal_verdict": check_T_w_delta_r_route_input_evaluation_terminal_verdict,
    "check_T_w_delta_r_route_input_evaluation_bank_closure": check_T_w_delta_r_route_input_evaluation_bank_closure,
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
    b = out["report"]["report"]["transport_error_budget"]
    print("Delta_r_APF_TRACE", f"{b['Delta_r_APF_TRACE_target']:.18f}")
    print("sigma_MW_rank_one_MeV", f"{b['sigma_MW_MeV_rank_one']:.6f}")
    raise SystemExit(0 if out["passed"] else 1)
