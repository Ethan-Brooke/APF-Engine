"""W_TRACE component-sum certificate harness bank.

v10.4 (2026-05-09 LATER-24): certificate harness after the v10.3
candidate-payload attempt gate.  This module defines the exact summation,
tolerance, covariance, and APF-anchor comparison contract for W finite-part
payload rows.  It deliberately ships with no admitted real external rows; the
bank closes the certificate *harness*, not a numerical Delta_r component-sum
certificate and not a physical W/on-shell export.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation, getcontext
from typing import Any, Dict, Mapping, Sequence, Tuple

from apf.w_trace_candidate_payload_attempt import (
    W_CANDIDATE_PAYLOAD_ATTEMPT_STATUS,
    PayloadAttempt,
    payload_attempt_report,
    shape_candidate_rows,
    reviewed_shape_candidate_metadata,
    check_T_w_candidate_payload_attempt_bank_closure as _check_v103,
)
from apf.w_trace_finite_part_ledger import apf_anchor_delta_r_target
from apf.w_trace_finite_part_skeleton import FINITE_PART_COMPONENT_ORDER, COMPONENT_SYMBOLS
from apf.w_trace_external_source_adapter import ExternalSourceRecord
from apf.trace_transport_completion import (
    check_T_physical_export_gate_locked_until_all_certificates_filled as _check_completion,
)

getcontext().prec = 50

W_COMPONENT_SUM_CERTIFICATE_STATUS = "P_w_component_sum_certificate_harness"
COMPONENT_SUM_CERTIFICATE_DECLARED = True
COMPONENT_SUM_CERTIFICATE_VERSION = "w_trace_component_sum_certificate_harness_v0"
COMPONENT_SUM_CERTIFICATE_MODE = "HARNESS_ONLY_NO_REAL_ROWS_NO_PHYSICAL_EXPORT"

REAL_COMPONENT_ROWS_ADMITTED = False
COMPONENT_SUM_NUMERICALLY_CERTIFIED = False
COVARIANCE_MATRIX_SUPPLIED = False
UNCERTAINTY_PROPAGATION_CERTIFIED = False
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

CERTIFICATE_REQUIRED_FIELDS: Tuple[str, ...] = (
    "status",
    "certificate_version",
    "rows_admitted",
    "table_shape_ok",
    "component_sum",
    "apf_anchor_delta_r_target",
    "absolute_residual",
    "tolerance",
    "within_tolerance",
    "covariance_supplied",
    "uncertainty_supplied",
    "component_sum_certified",
    "physical_W_export_enabled",
    "failure_reasons",
)

SUMMAND_REQUIRED_FIELDS: Tuple[str, ...] = (
    "component_id",
    "symbol",
    "numeric_value",
    "uncertainty",
    "target_observables_consumed",
    "apf_target_consumed",
)

FORBIDDEN_SUM_CERTIFICATE_INPUTS: Tuple[str, ...] = (
    "observed_M_W",
    "observed_M_W_column",
    "world_average_W_mass_column",
    "W_mass_residual",
    "W_mass_residual_column",
    "Delta_r_fit_to_observed_M_W",
    "Delta_r_fit_to_observed_M_W_column",
    "APF_ANCHOR_DELTA_R_TARGET",
    "APF_ANCHOR_DELTA_R_TARGET_COLUMN",
    "component_sum_residual_to_apf_target",
    "target_closure_residual_column",
    "physical_W_export_request",
)

DEFAULT_ABSOLUTE_TOLERANCE = Decimal("1e-12")

@dataclass(frozen=True)
class SumCertificatePolicy:
    tolerance_kind: str = "absolute_decimal"
    absolute_tolerance: str = "1e-12"
    require_covariance_for_physical_export: bool = True
    require_uncertainty_for_physical_export: bool = True
    allow_apf_anchor_as_comparison_target_only: bool = True
    allow_apf_anchor_as_component_input: bool = False
    allow_observed_w_as_input: bool = False
    allow_physical_export_from_harness: bool = False


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def certificate_policy() -> SumCertificatePolicy:
    return SumCertificatePolicy()


def _row_dict(row: ExternalSourceRecord | Mapping[str, Any]) -> Dict[str, Any]:
    return asdict(row) if isinstance(row, ExternalSourceRecord) else dict(row)


def _decimal_value(x: Any) -> Decimal | None:
    try:
        s = str(x)
        if s.upper() in {"UNSUPPLIED", "UNEVALUATED", "UNFILLED", "NONE", ""}:
            return None
        return Decimal(s)
    except (InvalidOperation, ValueError):
        return None


def _table_shape_ok(rows: Sequence[ExternalSourceRecord | Mapping[str, Any]]) -> bool:
    ids = tuple(_row_dict(r).get("component_id") for r in rows)
    return tuple(ids) == FINITE_PART_COMPONENT_ORDER and len(ids) == len(FINITE_PART_COMPONENT_ORDER)


def _symbols_match(rows: Sequence[ExternalSourceRecord | Mapping[str, Any]]) -> bool:
    for r in rows:
        d = _row_dict(r)
        cid = d.get("component_id")
        if cid not in COMPONENT_SYMBOLS or d.get("symbol") != COMPONENT_SYMBOLS[cid]:
            return False
    return True


def _forbidden_inputs_absent(rows: Sequence[ExternalSourceRecord | Mapping[str, Any]]) -> bool:
    forbidden = set(FORBIDDEN_SUM_CERTIFICATE_INPUTS)
    for r in rows:
        d = _row_dict(r)
        consumed = set(d.get("target_observables_consumed") or ())
        if consumed.intersection(forbidden):
            return False
        if bool(d.get("apf_target_consumed")):
            return False
    return True


def component_sum(rows: Sequence[ExternalSourceRecord | Mapping[str, Any]]) -> Decimal | None:
    vals = []
    for r in rows:
        v = _decimal_value(_row_dict(r).get("numeric_value"))
        if v is None:
            return None
        vals.append(v)
    return sum(vals, Decimal("0"))


def component_sum_certificate_report(
    rows: Sequence[ExternalSourceRecord | Mapping[str, Any]] | None = None,
    rows_admitted: bool = False,
    covariance_supplied: bool = False,
    uncertainty_supplied: bool = False,
    tolerance: Decimal = DEFAULT_ABSOLUTE_TOLERANCE,
    physical_export_requested: bool = False,
) -> Dict[str, Any]:
    rows = tuple() if rows is None else tuple(rows)
    table_ok = _table_shape_ok(rows)
    symbols_ok = _symbols_match(rows) if rows else False
    forbidden_absent = _forbidden_inputs_absent(rows)
    total = component_sum(rows) if rows else None
    target = apf_anchor_delta_r_target()
    residual = None if total is None else abs(total - target)
    within = False if residual is None else residual <= tolerance
    # Harness only: even a dry-path numeric shape may prove the comparison
    # mechanics, but no shipped physical closure is allowed without real rows,
    # covariance, uncertainty, and later export gates.
    certified = bool(rows_admitted and table_ok and symbols_ok and forbidden_absent and total is not None and within and covariance_supplied and uncertainty_supplied)
    physical_export_enabled = False
    failures = []
    if not rows:
        failures.append("NO_COMPONENT_ROWS_SUPPLIED")
    if not rows_admitted:
        failures.append("NO_ADMITTED_REAL_COMPONENT_ROWS")
    if rows and not table_ok:
        failures.append("COMPONENT_TABLE_SHAPE_NOT_EXACT_ORDER")
    if rows and not symbols_ok:
        failures.append("COMPONENT_SYMBOL_MISMATCH")
    if rows and not forbidden_absent:
        failures.append("FORBIDDEN_TARGET_OR_APF_INPUT_CONSUMED")
    if total is None:
        failures.append("COMPONENT_SUM_UNEVALUATED")
    if total is not None and not within:
        failures.append("COMPONENT_SUM_OUTSIDE_TOLERANCE")
    if not covariance_supplied:
        failures.append("COVARIANCE_PROTOCOL_UNSUPPLIED")
    if not uncertainty_supplied:
        failures.append("UNCERTAINTY_PROTOCOL_UNSUPPLIED")
    if physical_export_requested:
        failures.append("PHYSICAL_W_EXPORT_REQUEST_BLOCKED_AT_CERTIFICATE_HARNESS")
    return {
        "status": W_COMPONENT_SUM_CERTIFICATE_STATUS,
        "certificate_version": COMPONENT_SUM_CERTIFICATE_VERSION,
        "rows_admitted": bool(rows_admitted),
        "table_shape_ok": table_ok,
        "symbols_match": symbols_ok,
        "forbidden_inputs_absent": forbidden_absent,
        "component_sum": None if total is None else f"{total:.17E}",
        "apf_anchor_delta_r_target": f"{target:.17E}",
        "absolute_residual": None if residual is None else f"{residual:.17E}",
        "tolerance": f"{tolerance:.1E}",
        "within_tolerance": within,
        "covariance_supplied": bool(covariance_supplied),
        "uncertainty_supplied": bool(uncertainty_supplied),
        "component_sum_certified": certified,
        "physical_W_export_enabled": physical_export_enabled,
        "exports_physical_M_W": False,
        "exports_physical_scheme_masses": False,
        "failure_reasons": tuple(dict.fromkeys(failures)),
    }


def manifest() -> Dict[str, Any]:
    return {
        "status": W_COMPONENT_SUM_CERTIFICATE_STATUS,
        "upstream_status": W_CANDIDATE_PAYLOAD_ATTEMPT_STATUS,
        "certificate_version": COMPONENT_SUM_CERTIFICATE_VERSION,
        "certificate_mode": COMPONENT_SUM_CERTIFICATE_MODE,
        "required_certificate_fields": CERTIFICATE_REQUIRED_FIELDS,
        "summand_required_fields": SUMMAND_REQUIRED_FIELDS,
        "forbidden_sum_certificate_inputs": FORBIDDEN_SUM_CERTIFICATE_INPUTS,
        "component_order": FINITE_PART_COMPONENT_ORDER,
        "policy": asdict(certificate_policy()),
        "real_component_rows_admitted": REAL_COMPONENT_ROWS_ADMITTED,
        "component_sum_certified": COMPONENT_SUM_NUMERICALLY_CERTIFIED,
        "covariance_matrix_supplied": COVARIANCE_MATRIX_SUPPLIED,
        "uncertainty_propagation_certified": UNCERTAINTY_PROPAGATION_CERTIFIED,
        "physical_W_export_enabled": PHYSICAL_W_EXPORT_ENABLED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "absence_certificate": component_sum_certificate_report(),
    }


def _dry_rows_shifted_to_target() -> Tuple[ExternalSourceRecord, ...]:
    """Dry-path rows summing exactly to the APF anchor; not shipped data."""
    rows = list(shape_candidate_rows())
    target = apf_anchor_delta_r_target()
    per = target / Decimal(len(rows))
    out = []
    for r in rows:
        d = asdict(r)
        d["numeric_value"] = f"{per:.30E}"
        d["uncertainty"] = "1.0e-18"
        d["fixture_note"] = "dry-path sum mechanics only; not external finite-part data"
        out.append(ExternalSourceRecord(**d))
    return tuple(out)


# --- checks -----------------------------------------------------------------

def check_T_w_component_sum_certificate_status_declared():
    p = W_COMPONENT_SUM_CERTIFICATE_STATUS == "P_w_component_sum_certificate_harness" and COMPONENT_SUM_CERTIFICATE_DECLARED
    return {"passed": p, "status": "PASS" if p else "FAIL", "epistemic": W_COMPONENT_SUM_CERTIFICATE_STATUS}


def check_T_w_component_sum_certificate_depends_on_v103_attempt_gate():
    d = _check_v103()
    p = _passed(d) and W_CANDIDATE_PAYLOAD_ATTEMPT_STATUS == "P_w_candidate_payload_attempt_gate"
    return {"passed": p, "status": "PASS" if p else "FAIL", "upstream": d.get("status")}


def check_T_w_component_sum_certificate_schema_declared():
    r = component_sum_certificate_report()
    p = set(CERTIFICATE_REQUIRED_FIELDS).issubset(r.keys())
    return {"passed": p, "status": "PASS" if p else "FAIL", "fields": CERTIFICATE_REQUIRED_FIELDS}


def check_T_w_component_sum_certificate_policy_blocks_export():
    pol = certificate_policy()
    p = not pol.allow_physical_export_from_harness and pol.require_covariance_for_physical_export and pol.require_uncertainty_for_physical_export
    return {"passed": p, "status": "PASS" if p else "FAIL", "policy": asdict(pol)}


def check_T_w_component_sum_certificate_empty_by_default():
    r = component_sum_certificate_report()
    p = not r["rows_admitted"] and not r["component_sum_certified"] and "NO_COMPONENT_ROWS_SUPPLIED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_component_sum_certificate_target_available_from_trace_anchor():
    t = apf_anchor_delta_r_target()
    p = Decimal("0.03") < t < Decimal("0.05")
    return {"passed": p, "status": "PASS" if p else "FAIL", "target": f"{t:.17E}"}


def check_T_w_component_sum_certificate_shape_rows_exact_order():
    rows = shape_candidate_rows()
    p = _table_shape_ok(rows)
    return {"passed": p, "status": "PASS" if p else "FAIL", "ids": tuple(r.component_id for r in rows)}


def check_T_w_component_sum_certificate_symbols_match():
    p = _symbols_match(shape_candidate_rows())
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_component_sum_certificate_computes_decimal_sum():
    total = component_sum(shape_candidate_rows())
    p = total is not None and total > Decimal("0")
    return {"passed": p, "status": "PASS" if p else "FAIL", "sum": None if total is None else f"{total:.17E}"}


def check_T_w_component_sum_certificate_dry_path_within_tolerance():
    rows = _dry_rows_shifted_to_target()
    r = component_sum_certificate_report(rows, rows_admitted=True, covariance_supplied=True, uncertainty_supplied=True)
    p = r["within_tolerance"] and r["component_sum_certified"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "dry_path_report": r}


def check_T_w_component_sum_certificate_no_covariance_no_certification():
    rows = _dry_rows_shifted_to_target()
    r = component_sum_certificate_report(rows, rows_admitted=True, covariance_supplied=False, uncertainty_supplied=True)
    p = not r["component_sum_certified"] and "COVARIANCE_PROTOCOL_UNSUPPLIED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_component_sum_certificate_no_uncertainty_no_certification():
    rows = _dry_rows_shifted_to_target()
    r = component_sum_certificate_report(rows, rows_admitted=True, covariance_supplied=True, uncertainty_supplied=False)
    p = not r["component_sum_certified"] and "UNCERTAINTY_PROTOCOL_UNSUPPLIED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_component_sum_certificate_not_admitted_no_certification():
    rows = _dry_rows_shifted_to_target()
    r = component_sum_certificate_report(rows, rows_admitted=False, covariance_supplied=True, uncertainty_supplied=True)
    p = not r["component_sum_certified"] and "NO_ADMITTED_REAL_COMPONENT_ROWS" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_component_sum_certificate_rejects_missing_component():
    rows = shape_candidate_rows()[:-1]
    r = component_sum_certificate_report(rows, rows_admitted=True)
    p = not r["table_shape_ok"] and "COMPONENT_TABLE_SHAPE_NOT_EXACT_ORDER" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_component_sum_certificate_rejects_symbol_mismatch():
    rows = list(shape_candidate_rows())
    d = asdict(rows[0]); d["symbol"] = "BAD_SYMBOL"
    rows[0] = ExternalSourceRecord(**d)
    r = component_sum_certificate_report(tuple(rows), rows_admitted=True)
    p = not r["symbols_match"] and "COMPONENT_SYMBOL_MISMATCH" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_component_sum_certificate_rejects_apf_anchor_consumption():
    rows = list(shape_candidate_rows())
    d = asdict(rows[0]); d["target_observables_consumed"] = ("APF_ANCHOR_DELTA_R_TARGET",); d["apf_target_consumed"] = True
    rows[0] = ExternalSourceRecord(**d)
    r = component_sum_certificate_report(tuple(rows), rows_admitted=True)
    p = not r["forbidden_inputs_absent"] and "FORBIDDEN_TARGET_OR_APF_INPUT_CONSUMED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_component_sum_certificate_rejects_observed_w_consumption():
    rows = list(shape_candidate_rows())
    d = asdict(rows[0]); d["target_observables_consumed"] = ("observed_M_W_column",)
    rows[0] = ExternalSourceRecord(**d)
    r = component_sum_certificate_report(tuple(rows), rows_admitted=True)
    p = not r["forbidden_inputs_absent"] and "FORBIDDEN_TARGET_OR_APF_INPUT_CONSUMED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_component_sum_certificate_rejects_physical_export_request():
    rows = _dry_rows_shifted_to_target()
    r = component_sum_certificate_report(rows, rows_admitted=True, covariance_supplied=True, uncertainty_supplied=True, physical_export_requested=True)
    p = not r["physical_W_export_enabled"] and "PHYSICAL_W_EXPORT_REQUEST_BLOCKED_AT_CERTIFICATE_HARNESS" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_component_sum_certificate_manifest_remains_open():
    m = manifest()
    p = not m["real_component_rows_admitted"] and not m["component_sum_certified"] and not m["physical_W_export_enabled"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "manifest": m}


def check_T_w_component_sum_certificate_attempt_gate_shape_path_not_real():
    att = PayloadAttempt(rows_are_shipped_real_data=False, rows_are_shape_fixture=True)
    r = payload_attempt_report(shape_candidate_rows(), reviewed_shape_candidate_metadata(), att)
    p = r["candidate_report"]["candidate_rows_admitted"] and not r["rows_admitted"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "attempt_report": r}


def check_T_w_component_sum_certificate_forbidden_inputs_named():
    needed = {"observed_M_W_column", "APF_ANCHOR_DELTA_R_TARGET", "component_sum_residual_to_apf_target"}
    p = needed.issubset(FORBIDDEN_SUM_CERTIFICATE_INPUTS)
    return {"passed": p, "status": "PASS" if p else "FAIL", "forbidden": FORBIDDEN_SUM_CERTIFICATE_INPUTS}


def check_T_w_component_sum_certificate_no_physical_mass_exports():
    d = _check_completion()
    m = manifest()
    p = _passed(d) and not m["exports_physical_M_W"] and not m["physical_W_export_enabled"] and not EXPORTS_PHYSICAL_SCHEME_MASSES
    return {"passed": p, "status": "PASS" if p else "FAIL", "completion_gate": d.get("status"), "manifest": m}


def check_T_w_component_sum_certificate_bank_closure():
    deps = [
        check_T_w_component_sum_certificate_status_declared(),
        check_T_w_component_sum_certificate_depends_on_v103_attempt_gate(),
        check_T_w_component_sum_certificate_schema_declared(),
        check_T_w_component_sum_certificate_empty_by_default(),
        check_T_w_component_sum_certificate_manifest_remains_open(),
        check_T_w_component_sum_certificate_no_physical_mass_exports(),
    ]
    p = all(_passed(d) for d in deps) and not COMPONENT_SUM_NUMERICALLY_CERTIFIED and not PHYSICAL_W_EXPORT_ENABLED
    return {
        "passed": p,
        "status": "PASS" if p else "FAIL",
        "tier": 4,
        "epistemic": W_COMPONENT_SUM_CERTIFICATE_STATUS,
        "dependencies": [str(d.get("status")) for d in deps],
        "manifest": manifest(),
        "closed_now": "component-sum certificate schema, decimal summation/tolerance contract, covariance/uncertainty prerequisites, and anti-smuggling guards",
        "not_closed": "admitted real finite-part rows, certified component-sum, covariance/uncertainty propagation, physical W export",
    }


_CHECKS: Dict[str, Any] = {
    "T_w_component_sum_certificate_status_declared": check_T_w_component_sum_certificate_status_declared,
    "T_w_component_sum_certificate_depends_on_v103_attempt_gate": check_T_w_component_sum_certificate_depends_on_v103_attempt_gate,
    "T_w_component_sum_certificate_schema_declared": check_T_w_component_sum_certificate_schema_declared,
    "T_w_component_sum_certificate_policy_blocks_export": check_T_w_component_sum_certificate_policy_blocks_export,
    "T_w_component_sum_certificate_empty_by_default": check_T_w_component_sum_certificate_empty_by_default,
    "T_w_component_sum_certificate_target_available_from_trace_anchor": check_T_w_component_sum_certificate_target_available_from_trace_anchor,
    "T_w_component_sum_certificate_shape_rows_exact_order": check_T_w_component_sum_certificate_shape_rows_exact_order,
    "T_w_component_sum_certificate_symbols_match": check_T_w_component_sum_certificate_symbols_match,
    "T_w_component_sum_certificate_computes_decimal_sum": check_T_w_component_sum_certificate_computes_decimal_sum,
    "T_w_component_sum_certificate_dry_path_within_tolerance": check_T_w_component_sum_certificate_dry_path_within_tolerance,
    "T_w_component_sum_certificate_no_covariance_no_certification": check_T_w_component_sum_certificate_no_covariance_no_certification,
    "T_w_component_sum_certificate_no_uncertainty_no_certification": check_T_w_component_sum_certificate_no_uncertainty_no_certification,
    "T_w_component_sum_certificate_not_admitted_no_certification": check_T_w_component_sum_certificate_not_admitted_no_certification,
    "T_w_component_sum_certificate_rejects_missing_component": check_T_w_component_sum_certificate_rejects_missing_component,
    "T_w_component_sum_certificate_rejects_symbol_mismatch": check_T_w_component_sum_certificate_rejects_symbol_mismatch,
    "T_w_component_sum_certificate_rejects_apf_anchor_consumption": check_T_w_component_sum_certificate_rejects_apf_anchor_consumption,
    "T_w_component_sum_certificate_rejects_observed_w_consumption": check_T_w_component_sum_certificate_rejects_observed_w_consumption,
    "T_w_component_sum_certificate_rejects_physical_export_request": check_T_w_component_sum_certificate_rejects_physical_export_request,
    "T_w_component_sum_certificate_manifest_remains_open": check_T_w_component_sum_certificate_manifest_remains_open,
    "T_w_component_sum_certificate_attempt_gate_shape_path_not_real": check_T_w_component_sum_certificate_attempt_gate_shape_path_not_real,
    "T_w_component_sum_certificate_forbidden_inputs_named": check_T_w_component_sum_certificate_forbidden_inputs_named,
    "T_w_component_sum_certificate_no_physical_mass_exports": check_T_w_component_sum_certificate_no_physical_mass_exports,
    "T_w_component_sum_certificate_bank_closure": check_T_w_component_sum_certificate_bank_closure,
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
        "status": "W_TRACE_COMPONENT_SUM_CERTIFICATE_BANK_PASS" if ok else "W_TRACE_COMPONENT_SUM_CERTIFICATE_BANK_FAIL",
        "checks": rows,
        "manifest": manifest(),
    }


if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
