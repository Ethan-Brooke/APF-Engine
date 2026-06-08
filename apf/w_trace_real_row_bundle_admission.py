"""W_TRACE real finite-part row-bundle admission report bank.

v10.9 (2026-05-09 LATER-33): bundle-level admission report after the
v10.8 row schema / counterterm-value adapter.  This module defines the
single gate that takes candidate real finite-part rows, runs them through the
row schema, and emits an explicit ADMITTED / REJECTED / EMPTY certificate.
The shipped bank state remains empty: no real finite-part rows are bundled,
no component sum is certified, and physical W export remains locked.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, Sequence, Tuple

from apf.w_trace_finite_part_skeleton import FINITE_PART_COMPONENT_ORDER
from apf.w_trace_row_schema_adapter import (
    W_ROW_SCHEMA_STATUS,
    ROW_SCHEMA_VERSION,
    REQUIRED_ROW_FIELDS,
    FORBIDDEN_ROW_INPUTS,
    ALLOWED_ROW_SOURCE_CLASSES,
    make_shape_row,
    shape_fixture_rows,
    validate_rows,
    check_T_w_row_schema_bank_closure as _check_v108,
)
from apf.w_trace_physical_export_lock import export_lock_report, release_predicate

W_REAL_ROW_BUNDLE_STATUS = "P_w_real_row_bundle_admission"
BUNDLE_ADMISSION_VERSION = "w_trace_real_row_bundle_admission_v0"
BUNDLE_ADMISSION_MODE = "EMPTY_BY_DEFAULT_REAL_ROW_BUNDLE_ADMISSION_REPORT_NO_EXPORT"

REAL_ROW_BUNDLE_SUPPLIED = False
REAL_ROW_BUNDLE_ADMITTED = False
REAL_ROW_BUNDLE_REJECTED = False
COMPONENT_SUM_CERTIFIED = False
COVARIANCE_CERTIFIED = False
UNCERTAINTY_PROPAGATION_CERTIFIED = False
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False

ADMISSION_STATES: Tuple[str, ...] = ("EMPTY", "REJECTED", "ADMITTED")
REQUIRED_BUNDLE_METADATA_FIELDS: Tuple[str, ...] = (
    "bundle_id",
    "bundle_version",
    "row_schema_version",
    "source_pack_digest",
    "source_pack_uri",
    "extraction_log_digest",
    "review_status",
    "license_or_access_note",
    "declared_component_order",
    "physical_export_request",
)
ALLOWED_REVIEW_STATUSES: Tuple[str, ...] = (
    "reviewed_external_payload",
    "audited_internal_reproduction",
    "candidate_under_review",
)
FORBIDDEN_BUNDLE_INPUTS: Tuple[str, ...] = tuple(dict.fromkeys(FORBIDDEN_ROW_INPUTS + (
    "observed_M_W_bundle_metadata",
    "world_average_W_mass_bundle_metadata",
    "apf_anchor_delta_r_bundle_metadata",
    "component_sum_residual_to_apf_target",
    "physical_export_request",
)))

@dataclass(frozen=True)
class BundleAdmissionPolicy:
    require_nonempty_real_rows_for_admission: bool = True
    require_v108_row_schema_pass: bool = True
    require_full_component_coverage: bool = True
    require_bundle_metadata: bool = True
    require_declared_order_matches_skeleton: bool = True
    allow_shape_fixtures_as_real_bundle: bool = False
    allow_component_sum_certification_here: bool = False
    allow_covariance_certification_here: bool = False
    allow_physical_export_here: bool = False
    allow_apf_anchor_consumption: bool = False
    allow_observed_w_consumption: bool = False


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def policy() -> BundleAdmissionPolicy:
    return BundleAdmissionPolicy()


def default_bundle_metadata(**overrides: Any) -> Dict[str, Any]:
    md: Dict[str, Any] = {
        "bundle_id": "EMPTY_W_TRACE_REAL_ROW_BUNDLE_v0",
        "bundle_version": BUNDLE_ADMISSION_VERSION,
        "row_schema_version": ROW_SCHEMA_VERSION,
        "source_pack_digest": "sha256:no-real-row-bundle-shipped",
        "source_pack_uri": "empty://w_trace_real_row_bundle_admission/no-real-rows-shipped",
        "extraction_log_digest": "sha256:no-extraction-log-no-real-rows-shipped",
        "review_status": "candidate_under_review",
        "license_or_access_note": "no external numerical finite-part rows shipped in this bank state",
        "declared_component_order": FINITE_PART_COMPONENT_ORDER,
        "physical_export_request": False,
        "consumed_inputs": (),
    }
    md.update(overrides)
    return md


def empty_bundle_report() -> Dict[str, Any]:
    return admit_bundle(rows=None, metadata=default_bundle_metadata())


def _metadata_failures(metadata: Mapping[str, Any] | None) -> Tuple[Tuple[str, ...], Tuple[str, ...]]:
    md = dict(metadata or {})
    missing = tuple(k for k in REQUIRED_BUNDLE_METADATA_FIELDS if k not in md or md.get(k) in (None, ""))
    forbidden = []
    for x in tuple(md.get("consumed_inputs", ())):
        if x in FORBIDDEN_BUNDLE_INPUTS:
            forbidden.append(x)
    for key in ("physical_export_request",):
        if md.get(key):
            forbidden.append(key)
    return missing, tuple(dict.fromkeys(forbidden))


def admit_bundle(
    rows: Sequence[Mapping[str, Any]] | None = None,
    *,
    metadata: Mapping[str, Any] | None = None,
    physical_export_requested: bool = False,
) -> Dict[str, Any]:
    pol = policy()
    supplied = rows is not None and len(rows) > 0
    md = dict(metadata or {})
    missing_metadata, forbidden_metadata = _metadata_failures(md)
    row_report = validate_rows(rows, real_payload=True, physical_export_requested=physical_export_requested)
    declared_order = tuple(md.get("declared_component_order", ()))
    bad_order = bool(declared_order and declared_order != FINITE_PART_COMPONENT_ORDER)
    bad_schema_version = bool(md.get("row_schema_version") not in (None, ROW_SCHEMA_VERSION))
    bad_review_status = bool(md.get("review_status") not in (None, *ALLOWED_REVIEW_STATUSES))
    fixture_rows = tuple(row_report.get("bad_real_fixture", ()))

    failures = []
    if not supplied:
        failures.append("EMPTY_BUNDLE_NO_REAL_ROWS_SUPPLIED")
    if missing_metadata:
        failures.append("BUNDLE_METADATA_MISSING_REQUIRED_FIELDS")
    if forbidden_metadata:
        failures.append("FORBIDDEN_BUNDLE_INPUT_CONSUMED")
    if bad_order:
        failures.append("DECLARED_COMPONENT_ORDER_MISMATCH")
    if bad_schema_version:
        failures.append("ROW_SCHEMA_VERSION_MISMATCH")
    if bad_review_status:
        failures.append("REVIEW_STATUS_NOT_ADMISSIBLE")
    if physical_export_requested:
        failures.append("PHYSICAL_EXPORT_REQUEST_BLOCKED_AT_BUNDLE_ADMISSION")
    if not row_report["rows_schema_valid"] and supplied:
        failures.append("ROW_SCHEMA_VALIDATION_FAILED")
    if fixture_rows:
        failures.append("SHAPE_FIXTURE_ROWS_NOT_REAL_BUNDLE")
    failures.extend(row_report.get("failure_reasons", ()))

    admitted = bool(
        supplied
        and row_report["rows_schema_valid"]
        and row_report["rows_admitted"]
        and not missing_metadata
        and not forbidden_metadata
        and not bad_order
        and not bad_schema_version
        and not bad_review_status
        and not physical_export_requested
    )
    state = "ADMITTED" if admitted else ("EMPTY" if not supplied else "REJECTED")
    return {
        "status": W_REAL_ROW_BUNDLE_STATUS,
        "version": BUNDLE_ADMISSION_VERSION,
        "mode": BUNDLE_ADMISSION_MODE,
        "admission_state": state,
        "bundle_supplied": bool(supplied),
        "bundle_admitted": admitted,
        "bundle_rejected": bool(supplied and not admitted),
        "row_count": int(row_report.get("row_count", 0)),
        "row_schema_status": W_ROW_SCHEMA_STATUS,
        "row_schema_version": ROW_SCHEMA_VERSION,
        "row_schema_valid": bool(row_report.get("rows_schema_valid")),
        "rows_admitted_by_schema": bool(row_report.get("rows_admitted")),
        "counterterm_value_row_admitted_by_schema": bool(row_report.get("counterterm_value_row_admitted")),
        "component_order": FINITE_PART_COMPONENT_ORDER,
        "declared_component_order": declared_order,
        "missing_metadata_fields": missing_metadata,
        "forbidden_bundle_inputs_hit": forbidden_metadata,
        "row_failure_reasons": tuple(row_report.get("failure_reasons", ())),
        "failure_reasons": tuple(dict.fromkeys(failures)),
        "component_sum_certified": False,
        "covariance_certified": False,
        "uncertainty_propagation_certified": False,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "row_report": row_report,
    }


def real_candidate_rows_from_shape_template() -> Tuple[Dict[str, Any], ...]:
    """Return correctly shaped non-fixture rows for dry admission logic tests.

    These are not shipped as an admitted payload by default; they merely test
    that the bundle gate can admit rows if a future source pack replaces the
    fixture provenance with reviewed independent provenance.
    """
    rows = []
    for r in shape_fixture_rows():
        x = dict(r)
        x.update({
            "source_class": "audited_literature_table",
            "source_title": "dry-run independent finite-part table placeholder; not shipped as default payload",
            "source_pack_digest": "sha256:dry-run-real-shaped-pack",
            "table_locator": "dryrun://independent-source-table/" + x["component_id"],
            "extraction_log_digest": "sha256:dry-run-extraction-log",
            "row_checksum": "sha256:dry-run-row-" + x["component_id"],
            "provenance_chain": ("dry-run reviewed source placeholder", "no APF target or observed W input"),
            "review_status": "candidate_under_review",
            "loop_order_scope": "dry_run_shape_only_no_numerical_physics_claim",
        })
        rows.append(x)
    return tuple(rows)


def manifest() -> Dict[str, Any]:
    return {
        "status": W_REAL_ROW_BUNDLE_STATUS,
        "version": BUNDLE_ADMISSION_VERSION,
        "mode": BUNDLE_ADMISSION_MODE,
        "upstream_row_schema_status": W_ROW_SCHEMA_STATUS,
        "upstream_row_schema_version": ROW_SCHEMA_VERSION,
        "policy": asdict(policy()),
        "admission_states": ADMISSION_STATES,
        "required_bundle_metadata_fields": REQUIRED_BUNDLE_METADATA_FIELDS,
        "allowed_review_statuses": ALLOWED_REVIEW_STATUSES,
        "allowed_row_source_classes": ALLOWED_ROW_SOURCE_CLASSES,
        "forbidden_bundle_inputs": FORBIDDEN_BUNDLE_INPUTS,
        "required_row_fields": REQUIRED_ROW_FIELDS,
        "component_order": FINITE_PART_COMPONENT_ORDER,
        "real_row_bundle_supplied": REAL_ROW_BUNDLE_SUPPLIED,
        "real_row_bundle_admitted": REAL_ROW_BUNDLE_ADMITTED,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "covariance_certified": COVARIANCE_CERTIFIED,
        "uncertainty_propagation_certified": UNCERTAINTY_PROPAGATION_CERTIFIED,
        "physical_W_export_enabled": PHYSICAL_W_EXPORT_ENABLED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
    }


def _res(name: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    return {"passed": bool(passed), "status": "PASS" if passed else "FAIL", "tier": 4, "epistemic": W_REAL_ROW_BUNDLE_STATUS, "check": name, **extra}


def check_T_w_real_row_bundle_status_declared():
    m = manifest(); return _res("status_declared", m["status"] == W_REAL_ROW_BUNDLE_STATUS and not m["physical_W_export_enabled"], manifest=m)

def check_T_w_real_row_bundle_depends_on_v108_schema():
    d = _check_v108(); m = manifest(); return _res("depends_on_v108", _passed(d) and m["upstream_row_schema_status"] == W_ROW_SCHEMA_STATUS)

def check_T_w_real_row_bundle_policy_blocks_export():
    p = policy(); return _res("policy_blocks_export", not p.allow_physical_export_here and not p.allow_component_sum_certification_here)

def check_T_w_real_row_bundle_metadata_fields_complete():
    req = set(REQUIRED_BUNDLE_METADATA_FIELDS); return _res("metadata_fields", {"bundle_id", "row_schema_version", "declared_component_order", "physical_export_request"}.issubset(req))

def check_T_w_real_row_bundle_default_empty_certificate():
    r = empty_bundle_report(); return _res("default_empty", r["admission_state"] == "EMPTY" and not r["bundle_admitted"] and "EMPTY_BUNDLE_NO_REAL_ROWS_SUPPLIED" in r["failure_reasons"], report=r)

def check_T_w_real_row_bundle_default_exports_locked():
    r = empty_bundle_report(); return _res("default_exports_locked", not r["physical_W_export_enabled"] and not r["exports_physical_M_W"])

def check_T_w_real_row_bundle_dry_rows_can_admit_when_not_shipped_default():
    r = admit_bundle(real_candidate_rows_from_shape_template(), metadata=default_bundle_metadata(bundle_id="dryrun", source_pack_digest="sha256:dryrun")); return _res("dry_rows_admit", r["admission_state"] == "ADMITTED" and r["bundle_admitted"] and not r["physical_W_export_enabled"], report=r)

def check_T_w_real_row_bundle_shape_fixture_rejected_as_real():
    r = admit_bundle(shape_fixture_rows(), metadata=default_bundle_metadata(bundle_id="fixture")); return _res("fixtures_rejected", r["admission_state"] == "REJECTED" and "SHAPE_FIXTURE_ROWS_NOT_REAL_BUNDLE" in r["failure_reasons"], report=r)

def check_T_w_real_row_bundle_rejects_missing_metadata():
    md = default_bundle_metadata(); md.pop("bundle_id"); r = admit_bundle(real_candidate_rows_from_shape_template(), metadata=md); return _res("missing_metadata", not r["bundle_admitted"] and "BUNDLE_METADATA_MISSING_REQUIRED_FIELDS" in r["failure_reasons"])

def check_T_w_real_row_bundle_rejects_wrong_order():
    md = default_bundle_metadata(declared_component_order=tuple(reversed(FINITE_PART_COMPONENT_ORDER))); r = admit_bundle(real_candidate_rows_from_shape_template(), metadata=md); return _res("wrong_order", not r["bundle_admitted"] and "DECLARED_COMPONENT_ORDER_MISMATCH" in r["failure_reasons"])

def check_T_w_real_row_bundle_rejects_schema_version_mismatch():
    md = default_bundle_metadata(row_schema_version="wrong_schema"); r = admit_bundle(real_candidate_rows_from_shape_template(), metadata=md); return _res("schema_mismatch", not r["bundle_admitted"] and "ROW_SCHEMA_VERSION_MISMATCH" in r["failure_reasons"])

def check_T_w_real_row_bundle_rejects_bad_review_status():
    md = default_bundle_metadata(review_status="unreviewed_target_fit"); r = admit_bundle(real_candidate_rows_from_shape_template(), metadata=md); return _res("bad_review", not r["bundle_admitted"] and "REVIEW_STATUS_NOT_ADMISSIBLE" in r["failure_reasons"])

def check_T_w_real_row_bundle_rejects_missing_component():
    rows = real_candidate_rows_from_shape_template()[:-1]; r = admit_bundle(rows, metadata=default_bundle_metadata(bundle_id="missing")); return _res("missing_component", not r["bundle_admitted"] and "ROW_SCHEMA_VALIDATION_FAILED" in r["failure_reasons"])

def check_T_w_real_row_bundle_rejects_duplicate_component():
    rows = real_candidate_rows_from_shape_template() + (real_candidate_rows_from_shape_template()[0],); r = admit_bundle(rows, metadata=default_bundle_metadata(bundle_id="dup")); return _res("duplicate_component", not r["bundle_admitted"] and "ROW_SCHEMA_VALIDATION_FAILED" in r["failure_reasons"])

def check_T_w_real_row_bundle_rejects_unknown_component():
    rows = list(real_candidate_rows_from_shape_template()); bad = dict(rows[0]); bad["component_id"] = "unknown_component"; rows[0] = bad; r = admit_bundle(rows, metadata=default_bundle_metadata(bundle_id="unknown")); return _res("unknown_component", not r["bundle_admitted"] and "ROW_SCHEMA_VALIDATION_FAILED" in r["failure_reasons"])

def check_T_w_real_row_bundle_forbids_observed_w_metadata():
    md = default_bundle_metadata(consumed_inputs=("observed_M_W_bundle_metadata",)); r = admit_bundle(real_candidate_rows_from_shape_template(), metadata=md); return _res("forbid_observed_w_md", not r["bundle_admitted"] and "FORBIDDEN_BUNDLE_INPUT_CONSUMED" in r["failure_reasons"])

def check_T_w_real_row_bundle_forbids_apf_anchor_metadata():
    md = default_bundle_metadata(consumed_inputs=("apf_anchor_delta_r_bundle_metadata",)); r = admit_bundle(real_candidate_rows_from_shape_template(), metadata=md); return _res("forbid_apf_anchor_md", not r["bundle_admitted"] and "FORBIDDEN_BUNDLE_INPUT_CONSUMED" in r["failure_reasons"])

def check_T_w_real_row_bundle_forbids_residual_fit_metadata():
    md = default_bundle_metadata(consumed_inputs=("component_sum_residual_to_apf_target",)); r = admit_bundle(real_candidate_rows_from_shape_template(), metadata=md); return _res("forbid_residual_md", not r["bundle_admitted"] and "FORBIDDEN_BUNDLE_INPUT_CONSUMED" in r["failure_reasons"])

def check_T_w_real_row_bundle_physical_export_request_blocked():
    md = default_bundle_metadata(physical_export_request=True); r = admit_bundle(real_candidate_rows_from_shape_template(), metadata=md, physical_export_requested=True); return _res("export_request_blocked", not r["bundle_admitted"] and "PHYSICAL_EXPORT_REQUEST_BLOCKED_AT_BUNDLE_ADMISSION" in r["failure_reasons"])

def check_T_w_real_row_bundle_does_not_certify_component_sum():
    r = admit_bundle(real_candidate_rows_from_shape_template(), metadata=default_bundle_metadata(bundle_id="dryrun")); return _res("no_component_sum", r["bundle_admitted"] and not r["component_sum_certified"])

def check_T_w_real_row_bundle_does_not_certify_covariance():
    r = admit_bundle(real_candidate_rows_from_shape_template(), metadata=default_bundle_metadata(bundle_id="dryrun")); return _res("no_covariance", r["bundle_admitted"] and not r["covariance_certified"] and not r["uncertainty_propagation_certified"])

def check_T_w_real_row_bundle_preserves_release_lock():
    lock = export_lock_report(); pred = release_predicate(); r = empty_bundle_report(); return _res("preserve_release_lock", not r["physical_W_export_enabled"] and not bool(pred) and not lock["physical_W_export_enabled"])

def check_T_w_real_row_bundle_admission_states_exhaustive():
    states = {empty_bundle_report()["admission_state"], admit_bundle(shape_fixture_rows(), metadata=default_bundle_metadata(bundle_id="fixture"))["admission_state"], admit_bundle(real_candidate_rows_from_shape_template(), metadata=default_bundle_metadata(bundle_id="dryrun"))["admission_state"]}; return _res("states", states == set(ADMISSION_STATES), states=tuple(sorted(states)))

def check_T_w_real_row_bundle_bank_closure():
    deps = [check_T_w_real_row_bundle_status_declared(), check_T_w_real_row_bundle_depends_on_v108_schema(), check_T_w_real_row_bundle_default_empty_certificate(), check_T_w_real_row_bundle_dry_rows_can_admit_when_not_shipped_default(), check_T_w_real_row_bundle_preserves_release_lock()]
    p = all(_passed(d) for d in deps) and not manifest()["real_row_bundle_admitted"] and not manifest()["physical_W_export_enabled"]
    return _res("bank_closure", p, dependencies=deps, closed_now="real row-bundle admission/absence/rejection report gate", not_closed="actual shipped real rows, component-sum certificate, covariance/uncertainty propagation, physical W export")

_CHECKS: Dict[str, Any] = {
    "T_w_real_row_bundle_status_declared": check_T_w_real_row_bundle_status_declared,
    "T_w_real_row_bundle_depends_on_v108_schema": check_T_w_real_row_bundle_depends_on_v108_schema,
    "T_w_real_row_bundle_policy_blocks_export": check_T_w_real_row_bundle_policy_blocks_export,
    "T_w_real_row_bundle_metadata_fields_complete": check_T_w_real_row_bundle_metadata_fields_complete,
    "T_w_real_row_bundle_default_empty_certificate": check_T_w_real_row_bundle_default_empty_certificate,
    "T_w_real_row_bundle_default_exports_locked": check_T_w_real_row_bundle_default_exports_locked,
    "T_w_real_row_bundle_dry_rows_can_admit_when_not_shipped_default": check_T_w_real_row_bundle_dry_rows_can_admit_when_not_shipped_default,
    "T_w_real_row_bundle_shape_fixture_rejected_as_real": check_T_w_real_row_bundle_shape_fixture_rejected_as_real,
    "T_w_real_row_bundle_rejects_missing_metadata": check_T_w_real_row_bundle_rejects_missing_metadata,
    "T_w_real_row_bundle_rejects_wrong_order": check_T_w_real_row_bundle_rejects_wrong_order,
    "T_w_real_row_bundle_rejects_schema_version_mismatch": check_T_w_real_row_bundle_rejects_schema_version_mismatch,
    "T_w_real_row_bundle_rejects_bad_review_status": check_T_w_real_row_bundle_rejects_bad_review_status,
    "T_w_real_row_bundle_rejects_missing_component": check_T_w_real_row_bundle_rejects_missing_component,
    "T_w_real_row_bundle_rejects_duplicate_component": check_T_w_real_row_bundle_rejects_duplicate_component,
    "T_w_real_row_bundle_rejects_unknown_component": check_T_w_real_row_bundle_rejects_unknown_component,
    "T_w_real_row_bundle_forbids_observed_w_metadata": check_T_w_real_row_bundle_forbids_observed_w_metadata,
    "T_w_real_row_bundle_forbids_apf_anchor_metadata": check_T_w_real_row_bundle_forbids_apf_anchor_metadata,
    "T_w_real_row_bundle_forbids_residual_fit_metadata": check_T_w_real_row_bundle_forbids_residual_fit_metadata,
    "T_w_real_row_bundle_physical_export_request_blocked": check_T_w_real_row_bundle_physical_export_request_blocked,
    "T_w_real_row_bundle_does_not_certify_component_sum": check_T_w_real_row_bundle_does_not_certify_component_sum,
    "T_w_real_row_bundle_does_not_certify_covariance": check_T_w_real_row_bundle_does_not_certify_covariance,
    "T_w_real_row_bundle_preserves_release_lock": check_T_w_real_row_bundle_preserves_release_lock,
    "T_w_real_row_bundle_admission_states_exhaustive": check_T_w_real_row_bundle_admission_states_exhaustive,
    "T_w_real_row_bundle_bank_closure": check_T_w_real_row_bundle_bank_closure,
}


def register(registry: Dict[str, Any]) -> None:
    registry.update(_CHECKS)


def run_all() -> Dict[str, Any]:
    rows = []
    for name, fn in _CHECKS.items():
        try:
            result = fn()
            rows.append({"name": name, "passed": _passed(result), "result": result})
        except Exception as exc:
            rows.append({"name": name, "passed": False, "error": repr(exc)})
    ok = all(row["passed"] for row in rows)
    return {"passed": ok, "status": "W_TRACE_REAL_ROW_BUNDLE_ADMISSION_BANK_PASS" if ok else "W_TRACE_REAL_ROW_BUNDLE_ADMISSION_BANK_FAIL", "checks": rows, "manifest": manifest()}


if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
