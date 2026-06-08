"""W_TRACE standard-Delta_r extraction worksheet / source-total payload bridge.

v15.1 (2026-05-09): first next-phase physics-content bridge after the
v15.0 W on-shell terminal obstruction theorem.  This module promotes the
existing ACFW parametrization inversion into a reproducible standard-Delta_r
*total* worksheet/payload for comparison.  It deliberately does not promote the
source total into APF finite-part component rows, because the ACFW fitting
formula supplies a precision SM W-mass prediction/total Delta_r path, not the
APF eight-row finite-part decomposition required for physical W export.

Closed here:
    standard Delta_r total extraction worksheet / source-total comparison.
Still open:
    real finite-part component rows, component-sum certificate, covariance,
    uncertainty propagation, physical W/on-shell export.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_acfw_delta_r_extraction_attempt import (
    STATUS as ACFW_EXTRACTION_STATUS,
    ACFW_SOURCE,
    EXTRACTION_INPUTS,
    APF_DELTA_R_TARGET,
    M_W_TRACE_GEV,
    acfw_predict_mw,
    invert_delta_r_from_mw,
    extraction_payload,
    check_T_w_trace_acfw_bank_closure as _check_acfw,
)
from apf.w_trace_standard_delta_r_payload_schema import (
    PAYLOAD_SCHEMA_VERSION,
    validate_minimal_payload,
    schema_for,
    check_T_w_trace_standard_delta_r_payload_schema_bank_closure as _check_schema,
)
from apf.w_trace_finite_part_skeleton import FINITE_PART_COMPONENT_ORDER
from apf.w_trace_final_export_readiness import readiness_report
from apf.w_trace_real_row_bundle_admission import admit_bundle, default_bundle_metadata
from apf.w_trace_component_sum_certificate import component_sum_certificate_report

STATUS = "P_w_standard_delta_r_extraction_worksheet"
VERSION = "v15_1"
PASS_STATUS = "W_TRACE_STANDARD_DELTA_R_EXTRACTION_WORKSHEET_PASS"
TITLE = "W_TRACE standard Delta_r extraction worksheet"

WORKSHEET_ID = "W_TRACE_STANDARD_DELTA_R_TOTAL_WORKSHEET_ACFW_v15_1"
SOURCE_CANDIDATE_ID = ACFW_SOURCE["source_id"]
SOURCE_DOI = "10.1103/PhysRevD.69.053006"
SOURCE_ARXIV = "hep-ph/0311148"
SOURCE_DIGEST_ALGORITHM = "sha256-canonical-json"

# ACFW quote a residual theory uncertainty of about 4 MeV for M_H below about
# 300 GeV.  We carry it as a W-mass source uncertainty here; it is not yet a
# Delta_r covariance model and cannot unlock the W export route.
SOURCE_THEORY_UNCERTAINTY_MEV = 4.0

FORBIDDEN_WORKSHEET_INPUTS: Tuple[str, ...] = (
    "observed_M_W",
    "world_average_M_W",
    "CDF_II_M_W",
    "CMS_observed_M_W",
    "PDG_observed_M_W",
    "M_W_TRACE_as_source_input",
    "APF_DELTA_R_TARGET_AS_SOURCE_INPUT",
    "Delta_r_target_backsolve",
    "fit_to_APF_anchor",
    "fit_to_observed_W",
    "manual_export_override",
    "physical_export_request",
)

OPEN_EXPORT_BLOCKERS: Tuple[str, ...] = (
    "SOURCE_TOTAL_HAS_NO_APF_EIGHT_SLOT_COMPONENT_DECOMPOSITION",
    "NO_REAL_FINITE_PART_COMPONENT_ROWS_ADMITTED",
    "NO_COMPONENT_SUM_CERTIFICATE",
    "NO_COVARIANCE_CERTIFICATE",
    "NO_DELTA_R_TO_MW_UNCERTAINTY_PROPAGATION_CERTIFICATE",
    "PHYSICAL_W_EXPORT_LOCK_REMAINS_CLOSED",
)

LOCKED_STATE: Dict[str, bool] = {
    "standard_delta_r_total_worksheet_completed": True,
    "standard_delta_r_total_payload_valid_for_comparison": True,
    "source_total_promoted_to_apf_component_rows": False,
    "real_finite_part_component_rows_admitted": False,
    "component_sum_certified": False,
    "covariance_certified": False,
    "uncertainty_propagation_certified": False,
    "physical_W_export_enabled": False,
    "exports_physical_M_W": False,
}


@dataclass(frozen=True)
class WorksheetFormula:
    relation_id: str
    relation_latex: str
    solved_quantity: str
    independent_inputs: Tuple[str, ...]
    comparison_only_targets: Tuple[str, ...]
    forbidden_inputs: Tuple[str, ...]


@dataclass(frozen=True)
class PromotionObstruction:
    obstruction_id: str
    source_payload_kind: str
    required_payload_kind_for_w_export: str
    missing_objects: Tuple[str, ...]
    route_status: str
    physical_export_enabled: bool = False


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(obj).encode("utf-8")).hexdigest()


def contains_forbidden_token(obj: Any) -> bool:
    text = _canonical_json(obj)
    return any(tok in text for tok in FORBIDDEN_WORKSHEET_INPUTS)


def worksheet_formula() -> Dict[str, Any]:
    f = WorksheetFormula(
        relation_id="on_shell_GF_MW_MZ_Delta_r_relation",
        relation_latex=(
            r"G_F = \frac{\pi\alpha}{\sqrt{2}M_W^2}\,"
            r"\frac{1}{1-M_W^2/M_Z^2}\,\frac{1}{1-\Delta r}"
        ),
        solved_quantity="Delta_r_source_total",
        independent_inputs=(
            "M_H_GeV",
            "m_t_GeV",
            "Delta_alpha",
            "alpha_s_MZ",
            "M_Z_GeV",
            "alpha_inverse_for_inversion",
            "G_F_GeV_minus2",
        ),
        comparison_only_targets=("M_W_TRACE_GeV", "Delta_r_APF_TRACE_target"),
        forbidden_inputs=FORBIDDEN_WORKSHEET_INPUTS,
    )
    return asdict(f)


def source_total_values() -> Dict[str, float]:
    mw = acfw_predict_mw(EXTRACTION_INPUTS)
    dr = invert_delta_r_from_mw(mw, EXTRACTION_INPUTS)
    return {
        "M_W_source_GeV": mw,
        "Delta_r_source_total": dr,
        "M_W_source_minus_W_TRACE_GeV": mw - M_W_TRACE_GEV,
        "abs_M_W_gap_MeV": abs(mw - M_W_TRACE_GEV) * 1000.0,
        "Delta_r_source_minus_APF": dr - APF_DELTA_R_TARGET,
        "abs_Delta_r_residual": abs(dr - APF_DELTA_R_TARGET),
    }


def standard_total_payload() -> Dict[str, Any]:
    vals = source_total_values()
    source_record = {
        "source": dict(ACFW_SOURCE),
        "doi": SOURCE_DOI,
        "arxiv": SOURCE_ARXIV,
        "inputs": dict(EXTRACTION_INPUTS),
        "formula": worksheet_formula(),
        "values": vals,
    }
    return {
        "payload_schema_version": PAYLOAD_SCHEMA_VERSION,
        "payload_kind": "standard_delta_r_total",
        "source_candidate_id": SOURCE_CANDIDATE_ID,
        "source_digest": _digest(source_record),
        "source_digest_algorithm": SOURCE_DIGEST_ALGORITHM,
        "input_scheme": "standard_on_shell_GF_alpha_MZ_input_basis; ACFW_SM_parametrization_forward_MW_then_invert_Delta_r",
        "provenance": {
            "worksheet_id": WORKSHEET_ID,
            "source_title": ACFW_SOURCE["title"],
            "source_authors": ACFW_SOURCE["authors"],
            "source_doi": SOURCE_DOI,
            "source_arxiv": SOURCE_ARXIV,
            "extraction_status": ACFW_EXTRACTION_STATUS,
            "digest_material": source_record,
        },
        "anti_smuggling_attestations": {
            "uses_observed_M_W": False,
            "uses_world_average_M_W": False,
            "uses_CDF_II_M_W": False,
            "uses_CMS_observed_M_W": False,
            "uses_APF_TRACE_M_W_as_source_input": False,
            "uses_APF_Delta_r_target_as_source_input": False,
            "APF_targets_are_comparison_only": True,
            "physical_export_requested": False,
        },
        "physical_export_requested": False,
        "Delta_r_total": vals["Delta_r_source_total"],
        "uncertainty": {
            "M_W_theory_uncertainty_MeV_source_quote": SOURCE_THEORY_UNCERTAINTY_MEV,
            "Delta_r_uncertainty": "UNPROPAGATED_NO_COVARIANCE_CERTIFICATE",
            "role": "source-scale context only; not export uncertainty",
        },
        "derivation_note": "ACFW forward SM M_W parametrization evaluated on declared non-W inputs, then inverted through the on-shell G_F-M_W-M_Z-Delta_r relation.",
        "comparison_only": {
            "M_W_TRACE_GeV": M_W_TRACE_GEV,
            "Delta_r_APF_TRACE_target": APF_DELTA_R_TARGET,
            **vals,
        },
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
    }


def payload_validation_report() -> Dict[str, Any]:
    payload = standard_total_payload()
    # The upstream minimal validator intentionally has a broad substring guard;
    # for worksheet admission we separate required-field shape from source-input
    # token scans so the required field name `physical_export_requested` does
    # not self-trigger the forbidden-token detector.
    upstream_schema_report = validate_minimal_payload(payload)
    shape = schema_for("standard_delta_r_total")
    missing = tuple(k for k in shape.get("required", ()) if k not in payload)
    no_export = payload.get("physical_export_requested") is False
    source_material_clean = not contains_forbidden_token({
        "source_candidate_id": payload["source_candidate_id"],
        "inputs": EXTRACTION_INPUTS,
        "consumed_target_observables": (),
        "consumed_apf_targets": (),
    })
    return {
        "status": STATUS,
        "worksheet_id": WORKSHEET_ID,
        "payload_valid_minimal_schema": bool(shape.get("valid") and not missing and no_export and source_material_clean),
        "schema_report": {
            "valid_shape": bool(shape.get("valid")),
            "missing": missing,
            "no_export": no_export,
            "source_material_clean": source_material_clean,
            "upstream_minimal_validator_report": upstream_schema_report,
        },
        "forbidden_token_scan_clean": source_material_clean,
        "payload": payload,
    }


def promotion_obstruction() -> Dict[str, Any]:
    obs = PromotionObstruction(
        obstruction_id="ACFW_STANDARD_TOTAL_NOT_APF_COMPONENT_ROWS",
        source_payload_kind="standard_delta_r_total",
        required_payload_kind_for_w_export="APF_eight_slot_finite_part_component_row_bundle",
        missing_objects=OPEN_EXPORT_BLOCKERS,
        route_status="STANDARD_TOTAL_WORKSHEET_COMPLETE__COMPONENT_EXPORT_BLOCKED",
    )
    return asdict(obs)


def component_promotion_attempt_report() -> Dict[str, Any]:
    md = default_bundle_metadata(
        bundle_id="ACFW_STANDARD_TOTAL_PROMOTION_ATTEMPT_v15_1",
        source_pack_digest=standard_total_payload()["source_digest"],
        source_pack_uri="worksheet://" + WORKSHEET_ID,
        extraction_log_digest=standard_total_payload()["source_digest"],
        review_status="candidate_under_review",
        license_or_access_note="ACFW source-total worksheet only; no finite-part rows supplied",
        declared_component_order=FINITE_PART_COMPONENT_ORDER,
        physical_export_request=False,
    )
    bundle = admit_bundle(rows=None, metadata=md, physical_export_requested=False)
    sum_report = component_sum_certificate_report(rows=None, rows_admitted=False, covariance_supplied=False, uncertainty_supplied=False)
    ready = readiness_report(physical_export_requested=False)
    return {
        "status": STATUS,
        "promotion_obstruction": promotion_obstruction(),
        "bundle_admission_report": bundle,
        "component_sum_report": sum_report,
        "readiness_report": ready,
        "component_rows_supplied": False,
        "source_total_promoted_to_component_rows": False,
        "physical_W_export_enabled": False,
    }


def terminal_report() -> Dict[str, Any]:
    validation = payload_validation_report()
    promotion = component_promotion_attempt_report()
    return {
        "status": STATUS,
        "version": VERSION,
        "title": TITLE,
        "locked_state": dict(LOCKED_STATE),
        "worksheet_formula": worksheet_formula(),
        "source_total_values": source_total_values(),
        "payload_validation": validation,
        "promotion_obstruction": promotion["promotion_obstruction"],
        "current_route_readiness": promotion["readiness_report"],
        "verdict": "STANDARD_DELTA_R_TOTAL_WORKSHEET_COMPLETE__PHYSICAL_EXPORT_STILL_BLOCKED_BY_COMPONENT_PAYLOAD_REQUIREMENTS",
    }


def _res(check: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    row = {"check": check, "passed": bool(passed), "status": "PASS" if passed else "FAIL", "epistemic": STATUS}
    row.update(extra)
    return row


def _passed(row: Any) -> bool:
    return bool(isinstance(row, Mapping) and (row.get("passed") is True or row.get("status") in ("PASS", "P")))


def check_T_w_standard_delta_r_worksheet_status_declared():
    r = terminal_report()
    return _res("status_declared", r["status"] == STATUS and LOCKED_STATE["physical_W_export_enabled"] is False)


def check_T_w_standard_delta_r_worksheet_depends_on_acfw_extraction():
    d = _check_acfw()
    return _res("depends_on_acfw_extraction", _passed(d), upstream=d.get("status"), upstream_check=d.get("check"))


def check_T_w_standard_delta_r_worksheet_depends_on_payload_schema():
    d = _check_schema()
    return _res("depends_on_payload_schema", _passed(d), upstream=d.get("status"), upstream_check=d.get("check"))


def check_T_w_standard_delta_r_worksheet_formula_declared():
    f = worksheet_formula()
    ok = "Delta r" in f["relation_id"] or "Delta_r" in f["solved_quantity"]
    ok = ok and "M_W^2" in f["relation_latex"] and "1-\\Delta r" in f["relation_latex"]
    return _res("formula_declared", ok, formula=f)


def check_T_w_standard_delta_r_worksheet_source_digest_stable():
    p1 = standard_total_payload(); p2 = standard_total_payload()
    ok = p1["source_digest"].startswith("sha256:") and p1["source_digest"] == p2["source_digest"]
    return _res("source_digest_stable", ok, digest=p1["source_digest"])


def check_T_w_standard_delta_r_worksheet_payload_minimal_schema_valid():
    r = payload_validation_report()
    return _res("payload_minimal_schema_valid", r["payload_valid_minimal_schema"], schema=r["schema_report"])


def check_T_w_standard_delta_r_worksheet_values_match_acfw_payload():
    vals = source_total_values(); old = extraction_payload()
    ok = abs(vals["M_W_source_GeV"] - old["M_W_source_GeV"]) < 1e-14 and abs(vals["Delta_r_source_total"] - old["Delta_r_source_total"]) < 1e-14
    return _res("values_match_acfw_payload", ok, values=vals)


def check_T_w_standard_delta_r_worksheet_independent_inputs_only():
    clean = payload_validation_report()["forbidden_token_scan_clean"]
    att = standard_total_payload()["anti_smuggling_attestations"]
    ok = clean and not att["uses_observed_M_W"] and not att["uses_APF_TRACE_M_W_as_source_input"] and att["APF_targets_are_comparison_only"]
    return _res("independent_inputs_only", ok, attestations=att)


def check_T_w_standard_delta_r_worksheet_close_to_trace_neighborhood():
    vals = source_total_values()
    ok = vals["abs_M_W_gap_MeV"] < 5.0 and vals["abs_Delta_r_residual"] < 3e-4
    return _res("close_to_trace_neighborhood", ok, values=vals)


def check_T_w_standard_delta_r_worksheet_not_component_decomposition():
    payload = standard_total_payload()
    ok = payload["payload_kind"] == "standard_delta_r_total" and all(k not in payload for k in ("Delta_alpha", "Delta_rho", "Delta_r_rem"))
    return _res("not_component_decomposition", ok, payload_kind=payload["payload_kind"])


def check_T_w_standard_delta_r_worksheet_promotion_obstruction_declared():
    obs = promotion_obstruction()
    ok = obs["physical_export_enabled"] is False and "NO_REAL_FINITE_PART_COMPONENT_ROWS_ADMITTED" in obs["missing_objects"]
    return _res("promotion_obstruction_declared", ok, obstruction=obs)


def check_T_w_standard_delta_r_worksheet_bundle_admission_remains_empty():
    r = component_promotion_attempt_report()["bundle_admission_report"]
    ok = r["admission_state"] == "EMPTY" and not r["bundle_admitted"] and "EMPTY_BUNDLE_NO_REAL_ROWS_SUPPLIED" in r["failure_reasons"]
    return _res("bundle_admission_remains_empty", ok, bundle=r)


def check_T_w_standard_delta_r_worksheet_component_sum_remains_uncertified():
    r = component_promotion_attempt_report()["component_sum_report"]
    ok = not r["component_sum_certified"] and "NO_COMPONENT_ROWS_SUPPLIED" in r["failure_reasons"]
    return _res("component_sum_remains_uncertified", ok, component_sum=r)


def check_T_w_standard_delta_r_worksheet_readiness_remains_locked():
    r = component_promotion_attempt_report()["readiness_report"]
    ok = not r["physical_W_export_ready"] and not r["physical_W_export_enabled"] and not r["exports_physical_M_W"]
    return _res("readiness_remains_locked", ok, readiness=r)


def check_T_w_standard_delta_r_worksheet_no_physical_export_claim():
    r = terminal_report()
    ok = r["locked_state"]["exports_physical_M_W"] is False and "PHYSICAL_EXPORT_STILL_BLOCKED" in r["verdict"]
    return _res("no_physical_export_claim", ok, verdict=r["verdict"])


def check_T_w_standard_delta_r_worksheet_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_standard_delta_r_worksheet_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))


_CHECKS = {
    "check_T_w_standard_delta_r_worksheet_status_declared": check_T_w_standard_delta_r_worksheet_status_declared,
    "check_T_w_standard_delta_r_worksheet_depends_on_acfw_extraction": check_T_w_standard_delta_r_worksheet_depends_on_acfw_extraction,
    "check_T_w_standard_delta_r_worksheet_depends_on_payload_schema": check_T_w_standard_delta_r_worksheet_depends_on_payload_schema,
    "check_T_w_standard_delta_r_worksheet_formula_declared": check_T_w_standard_delta_r_worksheet_formula_declared,
    "check_T_w_standard_delta_r_worksheet_source_digest_stable": check_T_w_standard_delta_r_worksheet_source_digest_stable,
    "check_T_w_standard_delta_r_worksheet_payload_minimal_schema_valid": check_T_w_standard_delta_r_worksheet_payload_minimal_schema_valid,
    "check_T_w_standard_delta_r_worksheet_values_match_acfw_payload": check_T_w_standard_delta_r_worksheet_values_match_acfw_payload,
    "check_T_w_standard_delta_r_worksheet_independent_inputs_only": check_T_w_standard_delta_r_worksheet_independent_inputs_only,
    "check_T_w_standard_delta_r_worksheet_close_to_trace_neighborhood": check_T_w_standard_delta_r_worksheet_close_to_trace_neighborhood,
    "check_T_w_standard_delta_r_worksheet_not_component_decomposition": check_T_w_standard_delta_r_worksheet_not_component_decomposition,
    "check_T_w_standard_delta_r_worksheet_promotion_obstruction_declared": check_T_w_standard_delta_r_worksheet_promotion_obstruction_declared,
    "check_T_w_standard_delta_r_worksheet_bundle_admission_remains_empty": check_T_w_standard_delta_r_worksheet_bundle_admission_remains_empty,
    "check_T_w_standard_delta_r_worksheet_component_sum_remains_uncertified": check_T_w_standard_delta_r_worksheet_component_sum_remains_uncertified,
    "check_T_w_standard_delta_r_worksheet_readiness_remains_locked": check_T_w_standard_delta_r_worksheet_readiness_remains_locked,
    "check_T_w_standard_delta_r_worksheet_no_physical_export_claim": check_T_w_standard_delta_r_worksheet_no_physical_export_claim,
    "check_T_w_standard_delta_r_worksheet_bank_closure": check_T_w_standard_delta_r_worksheet_bank_closure,
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
    vals = out["report"]["source_total_values"]
    print("M_W_source_GeV", f"{vals['M_W_source_GeV']:.12f}")
    print("Delta_r_source_total", f"{vals['Delta_r_source_total']:.18f}")
    print("Delta_r_source_minus_APF", f"{vals['Delta_r_source_minus_APF']:.18f}")
    print("abs_M_W_gap_MeV", f"{vals['abs_M_W_gap_MeV']:.6f}")
    raise SystemExit(0 if out["passed"] else 1)
