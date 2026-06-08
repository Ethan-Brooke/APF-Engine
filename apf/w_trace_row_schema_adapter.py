"""W_TRACE real finite-part row schema / counterterm-value adapter bank.

v10.8 (2026-05-09 LATER-31): row-level admission schema after the
v10.7 counterterm-convention certificate.  This module banks the exact
field contract for real finite-part rows, including the Delta_r_ct_OS
counterterm row, without shipping or admitting any real numerical finite-part
payload.  It preserves the physical-export lock and continues to forbid
observed-W, APF-anchor, residual-fit, and post-hoc counterterm inputs.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from math import isfinite
from typing import Any, Dict, Iterable, Mapping, Sequence, Tuple

from apf.w_trace_counterterm_convention import (
    W_COUNTERTERM_CONVENTION_STATUS,
    COUNTERTERM_CONVENTION_ID,
    COUNTERTERM_COMPONENT,
    FORBIDDEN_CONVENTION_INPUTS,
    convention_report,
    default_convention_record,
    check_T_w_counterterm_convention_bank_closure as _check_v107,
)
from apf.w_trace_finite_part_skeleton import (
    FINITE_PART_COMPONENT_ORDER,
    COMPONENT_SYMBOLS,
)
from apf.w_trace_physical_export_lock import export_lock_report, release_predicate

W_ROW_SCHEMA_STATUS = "P_w_row_schema_adapter"
ROW_SCHEMA_VERSION = "w_trace_row_schema_adapter_v0"
ROW_SCHEMA_MODE = "FINITE_PART_ROW_SCHEMA_AND_COUNTERTERM_VALUE_ADAPTER_NO_REAL_PAYLOAD_NO_EXPORT"

REAL_FINITE_PART_ROWS_SUPPLIED = False
REAL_FINITE_PART_ROWS_ADMITTED = False
COUNTERTERM_VALUE_ROW_ADMITTED = False
COMPONENT_SUM_CERTIFIED = False
COVARIANCE_CERTIFIED = False
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False

ALLOWED_ROW_SOURCE_CLASSES: Tuple[str, ...] = (
    "reviewed_loop_library_export",
    "audited_literature_table",
    "independent_symbolic_evaluator_export",
    "internal_shape_fixture_not_real_payload",
)

REQUIRED_ROW_FIELDS: Tuple[str, ...] = (
    "component_id",
    "component_symbol",
    "value",
    "uncertainty",
    "unit",
    "scheme_family",
    "convention_id",
    "counterterm_component",
    "loop_order_scope",
    "sign_convention",
    "source_class",
    "source_title",
    "source_pack_digest",
    "table_locator",
    "extraction_log_digest",
    "row_checksum",
    "provenance_chain",
    "review_status",
    "adapter_version",
    "consumed_inputs",
    "physical_export_request",
)

REPORT_FIELDS: Tuple[str, ...] = (
    "status",
    "version",
    "rows_supplied",
    "rows_admitted",
    "counterterm_value_row_admitted",
    "component_sum_certified",
    "physical_W_export_enabled",
    "exports_physical_M_W",
    "missing_components",
    "duplicate_components",
    "unknown_components",
    "forbidden_inputs_hit",
    "failure_reasons",
)

FORBIDDEN_ROW_INPUTS: Tuple[str, ...] = tuple(dict.fromkeys(FORBIDDEN_CONVENTION_INPUTS + (
    "observed_M_W_column",
    "world_average_W_mass_column",
    "fit_residual_column",
    "apf_anchor_delta_r_column",
    "APF_ANCHOR_DELTA_R_TARGET",
    "component_sum_residual_to_apf_target",
    "posthoc_counterterm_fit",
    "physical_export_request",
)))

@dataclass(frozen=True)
class RowSchemaPolicy:
    require_full_component_coverage: bool = True
    require_dimensionless_delta_r_rows: bool = True
    require_nonnegative_uncertainty: bool = True
    require_finite_numeric_values: bool = True
    require_counterterm_row_matches_v107_convention: bool = True
    require_independent_source_for_real_payload: bool = True
    allow_shape_fixtures_as_real_payload: bool = False
    allow_apf_anchor_consumption: bool = False
    allow_observed_w_consumption: bool = False
    allow_residual_fit_consumption: bool = False
    allow_physical_export_from_rows_only: bool = False


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def policy() -> RowSchemaPolicy:
    return RowSchemaPolicy()


def component_symbol(component_id: str) -> str:
    return str(COMPONENT_SYMBOLS[component_id])


def empty_state() -> Dict[str, bool]:
    return {
        "real_finite_part_rows_supplied": REAL_FINITE_PART_ROWS_SUPPLIED,
        "real_finite_part_rows_admitted": REAL_FINITE_PART_ROWS_ADMITTED,
        "counterterm_value_row_admitted": COUNTERTERM_VALUE_ROW_ADMITTED,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "covariance_certified": COVARIANCE_CERTIFIED,
        "physical_W_export_enabled": PHYSICAL_W_EXPORT_ENABLED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
    }


def make_shape_row(component_id: str, *, source_class: str = "internal_shape_fixture_not_real_payload", consumed_inputs: Tuple[str, ...] = ()) -> Dict[str, Any]:
    return {
        "component_id": component_id,
        "component_symbol": component_symbol(component_id),
        "value": 0.0,
        "uncertainty": 0.0,
        "unit": "dimensionless_Delta_r_component",
        "scheme_family": "on_shell",
        "convention_id": COUNTERTERM_CONVENTION_ID,
        "counterterm_component": COUNTERTERM_COMPONENT,
        "loop_order_scope": "schema_fixture_only_no_real_loop_order_claim",
        "sign_convention": "M_W^2(1-M_W^2/M_Z^2)=pi*alpha/(sqrt(2)*G_F)/(1-Delta_r)",
        "source_class": source_class,
        "source_title": "synthetic schema fixture row; not an external finite-part payload",
        "source_pack_digest": "sha256:fixture-digest-not-real-payload",
        "table_locator": "fixture://w_trace_row_schema_adapter/" + component_id,
        "extraction_log_digest": "sha256:fixture-extraction-log-not-real-payload",
        "row_checksum": "sha256:fixture-row-" + component_id,
        "provenance_chain": ("APF v10.8 schema fixture", "not a numerical finite-part source"),
        "review_status": "shape_fixture_not_reviewed_as_physics_payload",
        "adapter_version": ROW_SCHEMA_VERSION,
        "consumed_inputs": tuple(consumed_inputs),
        "physical_export_request": False,
    }


def shape_fixture_rows() -> Tuple[Dict[str, Any], ...]:
    return tuple(make_shape_row(c) for c in FINITE_PART_COMPONENT_ORDER)


def _is_number(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and isfinite(float(x))


def validate_rows(
    rows: Sequence[Mapping[str, Any]] | None = None,
    *,
    real_payload: bool = False,
    physical_export_requested: bool = False,
) -> Dict[str, Any]:
    supplied = rows is not None and len(rows) > 0
    row_list = [dict(r) for r in (rows or ())]
    pol = policy()
    failures = []
    missing_fields_by_row = []
    component_ids = []
    forbidden_hit = []
    bad_symbols = []
    bad_uncertainty = []
    bad_numeric = []
    bad_units = []
    bad_source_class = []
    bad_real_fixture = []
    bad_convention = []
    bad_counterterm = []
    bad_export_requests = []

    for i, row in enumerate(row_list):
        missing = tuple(k for k in REQUIRED_ROW_FIELDS if k not in row or row.get(k) in (None, ""))
        if missing:
            missing_fields_by_row.append((i, missing))
        cid = row.get("component_id")
        component_ids.append(cid)
        if cid in COMPONENT_SYMBOLS and row.get("component_symbol") != component_symbol(str(cid)):
            bad_symbols.append(str(cid))
        if pol.require_nonnegative_uncertainty and (not _is_number(row.get("uncertainty")) or float(row.get("uncertainty")) < 0.0):
            bad_uncertainty.append(str(cid))
        if pol.require_finite_numeric_values and not _is_number(row.get("value")):
            bad_numeric.append(str(cid))
        if pol.require_dimensionless_delta_r_rows and row.get("unit") != "dimensionless_Delta_r_component":
            bad_units.append(str(cid))
        if row.get("source_class") not in ALLOWED_ROW_SOURCE_CLASSES:
            bad_source_class.append(str(cid))
        if real_payload and row.get("source_class") == "internal_shape_fixture_not_real_payload":
            bad_real_fixture.append(str(cid))
        if row.get("scheme_family") != "on_shell" or row.get("convention_id") != COUNTERTERM_CONVENTION_ID:
            bad_convention.append(str(cid))
        if row.get("counterterm_component") != COUNTERTERM_COMPONENT:
            bad_counterterm.append(str(cid))
        if row.get("physical_export_request") or physical_export_requested:
            bad_export_requests.append(str(cid))
        for x in tuple(row.get("consumed_inputs", ())):
            if x in FORBIDDEN_ROW_INPUTS:
                forbidden_hit.append(x)

    known = set(FINITE_PART_COMPONENT_ORDER)
    ids = tuple(str(x) for x in component_ids if x is not None)
    unknown = tuple(x for x in ids if x not in known)
    missing_components = tuple(x for x in FINITE_PART_COMPONENT_ORDER if x not in ids)
    duplicate_components = tuple(x for x in dict.fromkeys(ids) if ids.count(x) > 1)
    counterterm_present = COUNTERTERM_COMPONENT in ids

    if not supplied:
        failures.append("NO_REAL_OR_FIXTURE_ROWS_SUPPLIED")
    if missing_fields_by_row:
        failures.append("ROW_MISSING_REQUIRED_FIELDS")
    if unknown:
        failures.append("UNKNOWN_COMPONENT_ROW")
    if duplicate_components:
        failures.append("DUPLICATE_COMPONENT_ROW")
    if pol.require_full_component_coverage and missing_components:
        failures.append("MISSING_COMPONENT_ROWS")
    if bad_symbols:
        failures.append("COMPONENT_SYMBOL_MISMATCH")
    if bad_uncertainty:
        failures.append("UNCERTAINTY_NOT_NONNEGATIVE_FINITE")
    if bad_numeric:
        failures.append("VALUE_NOT_FINITE_NUMERIC")
    if bad_units:
        failures.append("ROW_UNIT_NOT_DIMENSIONLESS_DELTA_R")
    if bad_source_class:
        failures.append("ROW_SOURCE_CLASS_NOT_ALLOWED")
    if bad_real_fixture:
        failures.append("SHAPE_FIXTURE_CANNOT_BE_REAL_PAYLOAD")
    if bad_convention:
        failures.append("ROW_CONVENTION_MISMATCH")
    if bad_counterterm:
        failures.append("ROW_COUNTERTERM_COMPONENT_MISMATCH")
    if forbidden_hit:
        failures.append("FORBIDDEN_ROW_INPUT_CONSUMED")
    if bad_export_requests:
        failures.append("PHYSICAL_EXPORT_REQUEST_BLOCKED_AT_ROW_SCHEMA")
    if physical_export_requested:
        failures.append("PHYSICAL_W_EXPORT_REQUEST_BLOCKED_AT_ROW_SCHEMA")

    schema_valid = bool(
        supplied and not missing_fields_by_row and not unknown and not duplicate_components
        and (not pol.require_full_component_coverage or not missing_components)
        and not bad_symbols and not bad_uncertainty and not bad_numeric and not bad_units
        and not bad_source_class and not bad_convention and not bad_counterterm and not forbidden_hit
        and not bad_export_requests
    )
    rows_admitted = bool(schema_valid and real_payload and not bad_real_fixture and not physical_export_requested)
    counterterm_admitted = bool(rows_admitted and counterterm_present)
    # This module never certifies the sum/export by itself.
    return {
        "status": W_ROW_SCHEMA_STATUS,
        "version": ROW_SCHEMA_VERSION,
        "rows_supplied": bool(supplied),
        "row_count": len(row_list),
        "real_payload_requested": bool(real_payload),
        "rows_schema_valid": schema_valid,
        "rows_admitted": rows_admitted,
        "counterterm_value_row_present": counterterm_present,
        "counterterm_value_row_admitted": counterterm_admitted,
        "component_sum_certified": False,
        "covariance_certified": False,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "component_order": FINITE_PART_COMPONENT_ORDER,
        "component_ids_seen": ids,
        "missing_components": missing_components,
        "duplicate_components": duplicate_components,
        "unknown_components": unknown,
        "missing_fields_by_row": tuple(missing_fields_by_row),
        "bad_symbols": tuple(bad_symbols),
        "bad_uncertainty": tuple(bad_uncertainty),
        "bad_numeric": tuple(bad_numeric),
        "bad_units": tuple(bad_units),
        "bad_source_class": tuple(bad_source_class),
        "bad_real_fixture": tuple(bad_real_fixture),
        "bad_convention": tuple(bad_convention),
        "bad_counterterm": tuple(bad_counterterm),
        "forbidden_inputs_hit": tuple(dict.fromkeys(forbidden_hit)),
        "failure_reasons": tuple(dict.fromkeys(failures)),
    }


def manifest() -> Dict[str, Any]:
    return {
        "status": W_ROW_SCHEMA_STATUS,
        "upstream_status": W_COUNTERTERM_CONVENTION_STATUS,
        "version": ROW_SCHEMA_VERSION,
        "mode": ROW_SCHEMA_MODE,
        "policy": asdict(policy()),
        "required_row_fields": REQUIRED_ROW_FIELDS,
        "report_fields": REPORT_FIELDS,
        "allowed_row_source_classes": ALLOWED_ROW_SOURCE_CLASSES,
        "forbidden_row_inputs": FORBIDDEN_ROW_INPUTS,
        "component_order": FINITE_PART_COMPONENT_ORDER,
        "component_symbols": COMPONENT_SYMBOLS,
        "counterterm_convention_id": COUNTERTERM_CONVENTION_ID,
        "counterterm_component": COUNTERTERM_COMPONENT,
        **empty_state(),
    }


def check_T_w_row_schema_status_declared():
    m = manifest()
    p = m["status"] == W_ROW_SCHEMA_STATUS and m["version"] == ROW_SCHEMA_VERSION and not m["physical_W_export_enabled"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_depends_on_counterterm_convention():
    d = _check_v107(); r = convention_report()
    p = _passed(d) and r["convention_contract_certified"] and manifest()["upstream_status"] == W_COUNTERTERM_CONVENTION_STATUS
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_required_fields_complete():
    p = set(REQUIRED_ROW_FIELDS).issuperset({"component_id", "value", "uncertainty", "convention_id", "consumed_inputs"}) and len(REQUIRED_ROW_FIELDS) == 21
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_report_fields_complete():
    r = validate_rows(shape_fixture_rows())
    p = all(k in r for k in REPORT_FIELDS)
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_component_order_matches_skeleton():
    r = validate_rows(shape_fixture_rows())
    p = r["component_ids_seen"] == FINITE_PART_COMPONENT_ORDER and r["component_order"] == FINITE_PART_COMPONENT_ORDER
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_component_symbols_match():
    rows = shape_fixture_rows(); r = validate_rows(rows)
    p = r["rows_schema_valid"] and not r["bad_symbols"] and all(row["component_symbol"] == component_symbol(row["component_id"]) for row in rows)
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_dimensionless_units_required():
    rows = list(shape_fixture_rows()); rows[0] = dict(rows[0]); rows[0]["unit"] = "GeV"
    r = validate_rows(rows)
    p = not r["rows_schema_valid"] and "ROW_UNIT_NOT_DIMENSIONLESS_DELTA_R" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_uncertainty_nonnegative():
    rows = list(shape_fixture_rows()); rows[0] = dict(rows[0]); rows[0]["uncertainty"] = -1e-6
    r = validate_rows(rows)
    p = not r["rows_schema_valid"] and "UNCERTAINTY_NOT_NONNEGATIVE_FINITE" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_values_finite_numeric():
    rows = list(shape_fixture_rows()); rows[0] = dict(rows[0]); rows[0]["value"] = float("nan")
    r = validate_rows(rows)
    p = not r["rows_schema_valid"] and "VALUE_NOT_FINITE_NUMERIC" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_default_empty_state_no_rows_admitted():
    r = validate_rows(None)
    p = not r["rows_admitted"] and "NO_REAL_OR_FIXTURE_ROWS_SUPPLIED" in r["failure_reasons"] and not manifest()["real_finite_part_rows_supplied"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_shape_rows_validate_schema_only():
    r = validate_rows(shape_fixture_rows(), real_payload=False)
    p = r["rows_schema_valid"] and not r["rows_admitted"] and not r["counterterm_value_row_admitted"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS, "report": r}


def check_T_w_row_schema_shape_rows_cannot_be_real_payload():
    r = validate_rows(shape_fixture_rows(), real_payload=True)
    p = r["rows_schema_valid"] and not r["rows_admitted"] and "SHAPE_FIXTURE_CANNOT_BE_REAL_PAYLOAD" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_rejects_missing_field():
    rows = list(shape_fixture_rows()); rows[0] = dict(rows[0]); rows[0].pop("row_checksum")
    r = validate_rows(rows)
    p = not r["rows_schema_valid"] and "ROW_MISSING_REQUIRED_FIELDS" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_rejects_missing_component():
    r = validate_rows(shape_fixture_rows()[:-1])
    p = not r["rows_schema_valid"] and "MISSING_COMPONENT_ROWS" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_rejects_duplicate_component():
    rows = list(shape_fixture_rows()); rows.append(dict(rows[0]))
    r = validate_rows(rows)
    p = not r["rows_schema_valid"] and "DUPLICATE_COMPONENT_ROW" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_rejects_unknown_component():
    rows = list(shape_fixture_rows()); bad = dict(rows[0]); bad["component_id"] = "Delta_r_magic_fit"; rows[0] = bad
    r = validate_rows(rows)
    p = not r["rows_schema_valid"] and "UNKNOWN_COMPONENT_ROW" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_rejects_wrong_symbol():
    rows = list(shape_fixture_rows()); rows[0] = dict(rows[0]); rows[0]["component_symbol"] = "wrong"
    r = validate_rows(rows)
    p = not r["rows_schema_valid"] and "COMPONENT_SYMBOL_MISMATCH" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_rejects_wrong_source_class():
    rows = list(shape_fixture_rows()); rows[0] = dict(rows[0]); rows[0]["source_class"] = "target_fit_spreadsheet"
    r = validate_rows(rows)
    p = not r["rows_schema_valid"] and "ROW_SOURCE_CLASS_NOT_ALLOWED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_rejects_wrong_convention_id():
    rows = list(shape_fixture_rows()); rows[0] = dict(rows[0]); rows[0]["convention_id"] = "floating_counterterm_convention"
    r = validate_rows(rows)
    p = not r["rows_schema_valid"] and "ROW_CONVENTION_MISMATCH" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_rejects_wrong_scheme_family():
    rows = list(shape_fixture_rows()); rows[0] = dict(rows[0]); rows[0]["scheme_family"] = "MSbar"
    r = validate_rows(rows)
    p = not r["rows_schema_valid"] and "ROW_CONVENTION_MISMATCH" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_rejects_wrong_counterterm_component():
    rows = list(shape_fixture_rows()); rows[0] = dict(rows[0]); rows[0]["counterterm_component"] = "posthoc_counterterm_fit"
    r = validate_rows(rows)
    p = not r["rows_schema_valid"] and "ROW_COUNTERTERM_COMPONENT_MISMATCH" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_counterterm_row_present_but_unadmitted():
    r = validate_rows(shape_fixture_rows())
    p = r["counterterm_value_row_present"] and not r["counterterm_value_row_admitted"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_forbids_observed_w_consumption():
    rows = list(shape_fixture_rows()); rows[0] = make_shape_row(rows[0]["component_id"], consumed_inputs=("observed_M_W",))
    r = validate_rows(rows)
    p = not r["rows_schema_valid"] and "FORBIDDEN_ROW_INPUT_CONSUMED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_forbids_apf_anchor_consumption():
    rows = list(shape_fixture_rows()); rows[0] = make_shape_row(rows[0]["component_id"], consumed_inputs=("APF_ANCHOR_DELTA_R_TARGET",))
    r = validate_rows(rows)
    p = not r["rows_schema_valid"] and "FORBIDDEN_ROW_INPUT_CONSUMED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_forbids_residual_fit_consumption():
    rows = list(shape_fixture_rows()); rows[0] = make_shape_row(rows[0]["component_id"], consumed_inputs=("component_sum_residual_to_apf_target",))
    r = validate_rows(rows)
    p = not r["rows_schema_valid"] and "FORBIDDEN_ROW_INPUT_CONSUMED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_physical_export_request_blocked():
    r = validate_rows(shape_fixture_rows(), physical_export_requested=True)
    p = not r["physical_W_export_enabled"] and "PHYSICAL_W_EXPORT_REQUEST_BLOCKED_AT_ROW_SCHEMA" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_preserves_export_lock():
    lock = export_lock_report()
    p = not lock["physical_W_export_enabled"] and not release_predicate({})
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS, "export_lock": lock}


def check_T_w_row_schema_no_component_sum_or_export():
    r = validate_rows(shape_fixture_rows())
    p = not r["component_sum_certified"] and not r["covariance_certified"] and not r["exports_physical_M_W"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_ROW_SCHEMA_STATUS}


def check_T_w_row_schema_bank_closure():
    deps = [
        check_T_w_row_schema_status_declared(),
        check_T_w_row_schema_depends_on_counterterm_convention(),
        check_T_w_row_schema_required_fields_complete(),
        check_T_w_row_schema_component_order_matches_skeleton(),
        check_T_w_row_schema_shape_rows_validate_schema_only(),
        check_T_w_row_schema_counterterm_row_present_but_unadmitted(),
        check_T_w_row_schema_preserves_export_lock(),
        check_T_w_row_schema_no_component_sum_or_export(),
    ]
    p = all(_passed(d) for d in deps) and not REAL_FINITE_PART_ROWS_ADMITTED and not PHYSICAL_W_EXPORT_ENABLED
    return {
        "passed": p,
        "status": "PASS" if p else "FAIL",
        "tier": 4,
        "epistemic": W_ROW_SCHEMA_STATUS,
        "dependencies": [str(d.get("status")) for d in deps],
        "manifest": manifest(),
        "closed_now": "finite-part row field schema, component-symbol alignment, Delta_r_ct_OS counterterm row adapter, and anti-smuggling row-level predicates",
        "not_closed": "real finite-part values, counterterm numerical value admission, component-sum certificate, covariance/uncertainty propagation, physical W export",
    }


_CHECKS: Dict[str, Any] = {
    "T_w_row_schema_status_declared": check_T_w_row_schema_status_declared,
    "T_w_row_schema_depends_on_counterterm_convention": check_T_w_row_schema_depends_on_counterterm_convention,
    "T_w_row_schema_required_fields_complete": check_T_w_row_schema_required_fields_complete,
    "T_w_row_schema_report_fields_complete": check_T_w_row_schema_report_fields_complete,
    "T_w_row_schema_component_order_matches_skeleton": check_T_w_row_schema_component_order_matches_skeleton,
    "T_w_row_schema_component_symbols_match": check_T_w_row_schema_component_symbols_match,
    "T_w_row_schema_dimensionless_units_required": check_T_w_row_schema_dimensionless_units_required,
    "T_w_row_schema_uncertainty_nonnegative": check_T_w_row_schema_uncertainty_nonnegative,
    "T_w_row_schema_values_finite_numeric": check_T_w_row_schema_values_finite_numeric,
    "T_w_row_schema_default_empty_state_no_rows_admitted": check_T_w_row_schema_default_empty_state_no_rows_admitted,
    "T_w_row_schema_shape_rows_validate_schema_only": check_T_w_row_schema_shape_rows_validate_schema_only,
    "T_w_row_schema_shape_rows_cannot_be_real_payload": check_T_w_row_schema_shape_rows_cannot_be_real_payload,
    "T_w_row_schema_rejects_missing_field": check_T_w_row_schema_rejects_missing_field,
    "T_w_row_schema_rejects_missing_component": check_T_w_row_schema_rejects_missing_component,
    "T_w_row_schema_rejects_duplicate_component": check_T_w_row_schema_rejects_duplicate_component,
    "T_w_row_schema_rejects_unknown_component": check_T_w_row_schema_rejects_unknown_component,
    "T_w_row_schema_rejects_wrong_symbol": check_T_w_row_schema_rejects_wrong_symbol,
    "T_w_row_schema_rejects_wrong_source_class": check_T_w_row_schema_rejects_wrong_source_class,
    "T_w_row_schema_rejects_wrong_convention_id": check_T_w_row_schema_rejects_wrong_convention_id,
    "T_w_row_schema_rejects_wrong_scheme_family": check_T_w_row_schema_rejects_wrong_scheme_family,
    "T_w_row_schema_rejects_wrong_counterterm_component": check_T_w_row_schema_rejects_wrong_counterterm_component,
    "T_w_row_schema_counterterm_row_present_but_unadmitted": check_T_w_row_schema_counterterm_row_present_but_unadmitted,
    "T_w_row_schema_forbids_observed_w_consumption": check_T_w_row_schema_forbids_observed_w_consumption,
    "T_w_row_schema_forbids_apf_anchor_consumption": check_T_w_row_schema_forbids_apf_anchor_consumption,
    "T_w_row_schema_forbids_residual_fit_consumption": check_T_w_row_schema_forbids_residual_fit_consumption,
    "T_w_row_schema_physical_export_request_blocked": check_T_w_row_schema_physical_export_request_blocked,
    "T_w_row_schema_preserves_export_lock": check_T_w_row_schema_preserves_export_lock,
    "T_w_row_schema_no_component_sum_or_export": check_T_w_row_schema_no_component_sum_or_export,
    "T_w_row_schema_bank_closure": check_T_w_row_schema_bank_closure,
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
    return {
        "passed": ok,
        "status": "W_TRACE_ROW_SCHEMA_ADAPTER_BANK_PASS" if ok else "W_TRACE_ROW_SCHEMA_ADAPTER_BANK_FAIL",
        "checks": rows,
        "manifest": manifest(),
    }


if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
