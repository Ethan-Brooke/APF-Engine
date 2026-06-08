"""W_TRACE real source candidate payload admission-attempt bank.

v10.3 (2026-05-09 LATER-23): first payload-admission attempt layer
above v10.2.  This module adds an explicit attempt-state machine for real
external W finite-part candidate packs.  The shipped state contains no real
external numerical rows; the bank closes the admission/failure certificate and
the shape-tested admission path, not numerical finite-part values and not a
physical W export.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, Sequence, Tuple

from apf.w_trace_external_ingestion_dryrun import synthetic_json_payload
from apf.w_trace_external_source_adapter import (
    ExternalSourceRecord,
    external_shape_source_pack,
    EXTERNAL_ADAPTER_VERSION,
)
from apf.w_trace_finite_part_skeleton import FINITE_PART_COMPONENT_ORDER, COMPONENT_SYMBOLS
from apf.w_trace_real_source_candidate import (
    W_REAL_SOURCE_CANDIDATE_STATUS,
    CandidatePackMetadata,
    REQUIRED_CANDIDATE_METADATA_FIELDS,
    FORBIDDEN_REAL_CANDIDATE_INPUTS,
    candidate_admission_report,
    empty_candidate_rows,
    empty_candidate_metadata,
    parse_candidate_payload,
    check_T_w_real_source_candidate_bank_closure as _check_v102,
)
from apf.trace_transport_completion import (
    check_T_physical_export_gate_locked_until_all_certificates_filled as _check_completion,
)

W_CANDIDATE_PAYLOAD_ATTEMPT_STATUS = "P_w_candidate_payload_attempt_gate"
CANDIDATE_PAYLOAD_ATTEMPT_DECLARED = True
CANDIDATE_PAYLOAD_ATTEMPT_VERSION = "w_trace_candidate_payload_attempt_v0"
CANDIDATE_PAYLOAD_ATTEMPT_MODE = "NO_REAL_EXTERNAL_ROWS_SHIPPED__FAIL_CLOSED"

REAL_PAYLOAD_ATTEMPT_ROWS_SUPPLIED = False
REAL_PAYLOAD_ATTEMPT_ROWS_ADMITTED = False
REAL_PAYLOAD_ATTEMPT_COMPONENT_SUM_CERTIFIED = False
REAL_PAYLOAD_ATTEMPT_COVARIANCE_SUPPLIED = False
REAL_PAYLOAD_ATTEMPT_UNCERTAINTY_SUPPLIED = False
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

ATTEMPT_REQUIRED_REPORT_FIELDS = (
    "status",
    "attempt_version",
    "attempt_kind",
    "rows_supplied",
    "rows_admitted",
    "metadata_complete",
    "candidate_report",
    "admission_certificate",
    "failure_reasons",
    "component_sum_certified",
    "physical_W_export_enabled",
)

ADMISSION_CERTIFICATE_FIELDS = (
    "table_shape_ok",
    "all_rows_admitted_by_candidate_gate",
    "all_component_symbols_match",
    "metadata_complete",
    "forbidden_inputs_absent",
    "review_attested",
    "not_synthetic_fixture",
    "component_sum_certified",
    "physical_W_export_enabled",
)

FORBIDDEN_ATTEMPT_COLUMNS = tuple(sorted(set(FORBIDDEN_REAL_CANDIDATE_INPUTS + (
    "observed_M_W_column",
    "world_average_W_mass_column",
    "W_mass_residual_column",
    "Delta_r_fit_to_observed_M_W_column",
    "APF_ANCHOR_DELTA_R_TARGET_COLUMN",
    "physical_W_export_column",
))))

@dataclass(frozen=True)
class PayloadAttempt:
    attempt_id: str = "UNSUPPLIED_REAL_PAYLOAD_ATTEMPT"
    attempt_kind: str = "real_external_candidate_pack"
    attempted_pack_id: str = "UNSUPPLIED_REAL_EXTERNAL_PACK"
    attempted_pack_digest: str = "UNSUPPLIED"
    adapter_version: str = EXTERNAL_ADAPTER_VERSION
    rows_are_shipped_real_data: bool = False
    rows_are_shape_fixture: bool = False
    physical_export_requested: bool = False


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def default_payload_attempt() -> PayloadAttempt:
    return PayloadAttempt()


def empty_payload_attempt_rows() -> Tuple[ExternalSourceRecord, ...]:
    return ()


def reviewed_shape_candidate_metadata() -> CandidatePackMetadata:
    """Complete metadata for shape tests only; not shipped as real data."""
    return CandidatePackMetadata(
        candidate_pack_id="SHAPE_TEST_REAL_CANDIDATE_CONTRACT_NOT_DATA",
        candidate_pack_uri="file://shape-test/w-trace-candidate-pack.json",
        candidate_pack_digest="sha256:shape-test-candidate-pack-not-data",
        candidate_adapter_version=EXTERNAL_ADAPTER_VERSION,
        candidate_ingest_format="json_rows_v1",
        candidate_extraction_log_digest="sha256:shape-test-extraction-log-not-data",
        candidate_review_attestation=True,
        candidate_synthetic_fixture=False,
    )


def shape_candidate_rows() -> Tuple[ExternalSourceRecord, ...]:
    """Return a complete adapter-admissible shape pack.

    Values are inherited from the v10.0/v10.1 shape path and remain fixture
    values, not admitted real external numerical finite-part payloads.
    """
    return external_shape_source_pack()


def _forbidden_inputs_absent(rows: Sequence[ExternalSourceRecord | Mapping[str, Any]]) -> bool:
    for r in rows:
        d = asdict(r) if isinstance(r, ExternalSourceRecord) else dict(r)
        consumed = set(d.get("target_observables_consumed") or ())
        if consumed.intersection(FORBIDDEN_ATTEMPT_COLUMNS):
            return False
        if d.get("apf_target_consumed"):
            return False
    return True


def _symbol_match(rows: Sequence[ExternalSourceRecord | Mapping[str, Any]]) -> bool:
    for r in rows:
        d = asdict(r) if isinstance(r, ExternalSourceRecord) else dict(r)
        cid = d.get("component_id")
        if cid not in COMPONENT_SYMBOLS or d.get("symbol") != COMPONENT_SYMBOLS[cid]:
            return False
    return True


def payload_attempt_report(
    rows: Sequence[ExternalSourceRecord | Mapping[str, Any]] | None = None,
    meta: CandidatePackMetadata | Mapping[str, Any] | None = None,
    attempt: PayloadAttempt | Mapping[str, Any] | None = None,
) -> Dict[str, Any]:
    rows = empty_payload_attempt_rows() if rows is None else tuple(rows)
    meta = empty_candidate_metadata() if meta is None else meta
    attempt_obj = default_payload_attempt() if attempt is None else attempt
    ad = asdict(attempt_obj) if isinstance(attempt_obj, PayloadAttempt) else dict(attempt_obj)
    candidate = candidate_admission_report(rows, meta)
    md = asdict(meta) if isinstance(meta, CandidatePackMetadata) else dict(meta)
    metadata_complete = bool(candidate.get("metadata_complete"))
    table_shape_ok = bool(candidate.get("adapter_report", {}).get("table_shape_ok"))
    candidate_admitted = bool(candidate.get("candidate_rows_admitted"))
    forbidden_absent = _forbidden_inputs_absent(rows)
    symbols_match = _symbol_match(rows) if rows else False
    physical_export_requested = bool(ad.get("physical_export_requested"))
    is_real_payload_claim = bool(ad.get("rows_are_shipped_real_data")) and not bool(ad.get("rows_are_shape_fixture"))
    rows_supplied = len(rows) > 0
    # The bank intentionally does not admit shipped real rows unless a later
    # module supplies a real reviewed payload and turns this gate into a source
    # table certificate.  Shape rows may demonstrate the path but cannot become
    # real payload admission in this v10.3 state.
    rows_admitted = bool(rows_supplied and candidate_admitted and is_real_payload_claim and not physical_export_requested)
    certificate = {
        "table_shape_ok": table_shape_ok,
        "all_rows_admitted_by_candidate_gate": candidate_admitted,
        "all_component_symbols_match": symbols_match,
        "metadata_complete": metadata_complete,
        "forbidden_inputs_absent": forbidden_absent,
        "review_attested": bool(md.get("candidate_review_attestation")),
        "not_synthetic_fixture": not bool(md.get("candidate_synthetic_fixture")),
        "component_sum_certified": False,
        "physical_W_export_enabled": False,
    }
    failure_reasons = list(candidate.get("failure_reasons", ()))
    if not rows_supplied:
        failure_reasons.append("NO_PAYLOAD_ATTEMPT_ROWS_SUPPLIED")
    if rows_supplied and not is_real_payload_claim:
        failure_reasons.append("ROWS_ARE_SHAPE_OR_NONREAL_FIXTURE_NOT_REAL_PAYLOAD")
    if physical_export_requested:
        failure_reasons.append("PHYSICAL_W_EXPORT_REQUEST_BLOCKED_AT_ATTEMPT_GATE")
    if not forbidden_absent:
        failure_reasons.append("FORBIDDEN_TARGET_OR_APF_INPUT_CONSUMED")
    return {
        "status": W_CANDIDATE_PAYLOAD_ATTEMPT_STATUS,
        "attempt_version": CANDIDATE_PAYLOAD_ATTEMPT_VERSION,
        "attempt_kind": ad.get("attempt_kind"),
        "rows_supplied": rows_supplied,
        "rows_admitted": rows_admitted,
        "metadata_complete": metadata_complete,
        "candidate_report": candidate,
        "admission_certificate": certificate,
        "failure_reasons": tuple(dict.fromkeys(failure_reasons)),
        "component_sum_certified": False,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "exports_physical_scheme_masses": False,
    }


def payload_attempt_manifest() -> Dict[str, Any]:
    r = payload_attempt_report()
    return {
        "status": W_CANDIDATE_PAYLOAD_ATTEMPT_STATUS,
        "upstream_status": W_REAL_SOURCE_CANDIDATE_STATUS,
        "attempt_version": CANDIDATE_PAYLOAD_ATTEMPT_VERSION,
        "attempt_mode": CANDIDATE_PAYLOAD_ATTEMPT_MODE,
        "required_report_fields": ATTEMPT_REQUIRED_REPORT_FIELDS,
        "admission_certificate_fields": ADMISSION_CERTIFICATE_FIELDS,
        "forbidden_attempt_columns": FORBIDDEN_ATTEMPT_COLUMNS,
        "component_order": FINITE_PART_COMPONENT_ORDER,
        "real_payload_attempt_rows_supplied": REAL_PAYLOAD_ATTEMPT_ROWS_SUPPLIED,
        "real_payload_attempt_rows_admitted": REAL_PAYLOAD_ATTEMPT_ROWS_ADMITTED,
        "component_sum_certified": REAL_PAYLOAD_ATTEMPT_COMPONENT_SUM_CERTIFIED,
        "covariance_supplied": REAL_PAYLOAD_ATTEMPT_COVARIANCE_SUPPLIED,
        "uncertainty_supplied": REAL_PAYLOAD_ATTEMPT_UNCERTAINTY_SUPPLIED,
        "physical_W_export_enabled": PHYSICAL_W_EXPORT_ENABLED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "absence_or_failure_certificate": r,
    }


# --- checks -----------------------------------------------------------------

def check_T_w_candidate_payload_attempt_status_declared():
    p = W_CANDIDATE_PAYLOAD_ATTEMPT_STATUS == "P_w_candidate_payload_attempt_gate" and CANDIDATE_PAYLOAD_ATTEMPT_DECLARED
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_CANDIDATE_PAYLOAD_ATTEMPT_STATUS}


def check_T_w_candidate_payload_attempt_depends_on_v102_candidate_gate():
    d = _check_v102()
    p = _passed(d) and W_REAL_SOURCE_CANDIDATE_STATUS == "P_w_real_source_candidate_gate"
    return {"passed": p, "status": "PASS" if p else "FAIL", "upstream": d.get("status")}


def check_T_w_candidate_payload_attempt_report_schema_declared():
    r = payload_attempt_report()
    p = set(ATTEMPT_REQUIRED_REPORT_FIELDS).issubset(r.keys())
    return {"passed": p, "status": "PASS" if p else "FAIL", "fields": ATTEMPT_REQUIRED_REPORT_FIELDS}


def check_T_w_candidate_payload_attempt_certificate_schema_declared():
    cert = payload_attempt_report()["admission_certificate"]
    p = set(ADMISSION_CERTIFICATE_FIELDS) == set(cert.keys())
    return {"passed": p, "status": "PASS" if p else "FAIL", "certificate": cert}


def check_T_w_candidate_payload_attempt_empty_by_default():
    r = payload_attempt_report()
    p = not r["rows_supplied"] and not r["rows_admitted"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_candidate_payload_attempt_absence_certificate_names_missing_rows():
    r = payload_attempt_report()
    p = "NO_PAYLOAD_ATTEMPT_ROWS_SUPPLIED" in r["failure_reasons"] and "NO_REAL_EXTERNAL_CANDIDATE_ROWS_SUPPLIED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "failure_reasons": r["failure_reasons"]}


def check_T_w_candidate_payload_attempt_shape_rows_cover_all_components():
    rows = shape_candidate_rows()
    p = tuple(r.component_id for r in rows) == FINITE_PART_COMPONENT_ORDER and len(rows) == 8
    return {"passed": p, "status": "PASS" if p else "FAIL", "component_ids": tuple(r.component_id for r in rows)}


def check_T_w_candidate_payload_attempt_shape_symbols_match():
    rows = shape_candidate_rows()
    p = _symbol_match(rows)
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_candidate_payload_attempt_candidate_gate_accepts_shape_path():
    r = candidate_admission_report(shape_candidate_rows(), reviewed_shape_candidate_metadata())
    p = r["adapter_report"]["table_shape_ok"] and r["candidate_rows_admitted"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "candidate_report": r}


def check_T_w_candidate_payload_attempt_does_not_promote_shape_to_real_payload():
    att = PayloadAttempt(rows_are_shipped_real_data=False, rows_are_shape_fixture=True)
    r = payload_attempt_report(shape_candidate_rows(), reviewed_shape_candidate_metadata(), att)
    p = r["candidate_report"]["candidate_rows_admitted"] and not r["rows_admitted"] and "ROWS_ARE_SHAPE_OR_NONREAL_FIXTURE_NOT_REAL_PAYLOAD" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_candidate_payload_attempt_requires_real_payload_flag_for_admission():
    att = PayloadAttempt(rows_are_shipped_real_data=True, rows_are_shape_fixture=False)
    r = payload_attempt_report(shape_candidate_rows(), reviewed_shape_candidate_metadata(), att)
    p = r["rows_admitted"] is True and r["component_sum_certified"] is False and r["physical_W_export_enabled"] is False
    # This is a dry admission-path test only: the shipped manifest constants remain false.
    return {"passed": p, "status": "PASS" if p else "FAIL", "dry_path_report": r}


def check_T_w_candidate_payload_attempt_manifest_remains_no_real_rows():
    m = payload_attempt_manifest()
    p = not m["real_payload_attempt_rows_supplied"] and not m["real_payload_attempt_rows_admitted"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "manifest": m}


def check_T_w_candidate_payload_attempt_rejects_physical_export_request():
    att = PayloadAttempt(rows_are_shipped_real_data=True, rows_are_shape_fixture=False, physical_export_requested=True)
    r = payload_attempt_report(shape_candidate_rows(), reviewed_shape_candidate_metadata(), att)
    p = not r["rows_admitted"] and "PHYSICAL_W_EXPORT_REQUEST_BLOCKED_AT_ATTEMPT_GATE" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_candidate_payload_attempt_forbidden_columns_include_observed_W():
    p = {"observed_M_W_column", "world_average_W_mass_column", "W_mass_residual_column"}.issubset(FORBIDDEN_ATTEMPT_COLUMNS)
    return {"passed": p, "status": "PASS" if p else "FAIL", "forbidden": FORBIDDEN_ATTEMPT_COLUMNS}


def check_T_w_candidate_payload_attempt_forbidden_columns_include_apf_anchor():
    p = "APF_ANCHOR_DELTA_R_TARGET_COLUMN" in FORBIDDEN_ATTEMPT_COLUMNS and "APF_ANCHOR_DELTA_R_TARGET" in FORBIDDEN_ATTEMPT_COLUMNS
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_candidate_payload_attempt_rejects_observed_W_consuming_row():
    rows = list(shape_candidate_rows())
    rows[0] = ExternalSourceRecord(**{**asdict(rows[0]), "target_observables_consumed": ("observed_M_W_column",)})
    att = PayloadAttempt(rows_are_shipped_real_data=True)
    r = payload_attempt_report(tuple(rows), reviewed_shape_candidate_metadata(), att)
    p = not r["rows_admitted"] and "FORBIDDEN_TARGET_OR_APF_INPUT_CONSUMED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_candidate_payload_attempt_rejects_apf_anchor_consuming_row():
    rows = list(shape_candidate_rows())
    rows[0] = ExternalSourceRecord(**{**asdict(rows[0]), "target_observables_consumed": ("APF_ANCHOR_DELTA_R_TARGET",), "apf_target_consumed": True})
    att = PayloadAttempt(rows_are_shipped_real_data=True)
    r = payload_attempt_report(tuple(rows), reviewed_shape_candidate_metadata(), att)
    p = not r["rows_admitted"] and "FORBIDDEN_TARGET_OR_APF_INPUT_CONSUMED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_candidate_payload_attempt_rejects_bad_metadata_digest():
    bad = CandidatePackMetadata(**{**asdict(reviewed_shape_candidate_metadata()), "candidate_pack_digest": "not-a-sha"})
    att = PayloadAttempt(rows_are_shipped_real_data=True)
    r = payload_attempt_report(shape_candidate_rows(), bad, att)
    p = not r["rows_admitted"] and not r["metadata_complete"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_candidate_payload_attempt_rejects_unreviewed_metadata():
    bad = CandidatePackMetadata(**{**asdict(reviewed_shape_candidate_metadata()), "candidate_review_attestation": False})
    att = PayloadAttempt(rows_are_shipped_real_data=True)
    r = payload_attempt_report(shape_candidate_rows(), bad, att)
    p = not r["rows_admitted"] and not r["metadata_complete"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_candidate_payload_attempt_rejects_synthetic_metadata():
    bad = CandidatePackMetadata(**{**asdict(reviewed_shape_candidate_metadata()), "candidate_synthetic_fixture": True})
    att = PayloadAttempt(rows_are_shipped_real_data=True)
    r = payload_attempt_report(shape_candidate_rows(), bad, att)
    p = not r["rows_admitted"] and not r["metadata_complete"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_candidate_payload_attempt_rejects_symbol_mismatch():
    rows = list(shape_candidate_rows())
    rows[0] = ExternalSourceRecord(**{**asdict(rows[0]), "symbol": "BAD_SYMBOL"})
    att = PayloadAttempt(rows_are_shipped_real_data=True)
    r = payload_attempt_report(tuple(rows), reviewed_shape_candidate_metadata(), att)
    p = not r["rows_admitted"] and r["admission_certificate"]["all_component_symbols_match"] is False
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_candidate_payload_attempt_rejects_missing_component():
    rows = shape_candidate_rows()[:-1]
    att = PayloadAttempt(rows_are_shipped_real_data=True)
    r = payload_attempt_report(rows, reviewed_shape_candidate_metadata(), att)
    p = not r["rows_admitted"] and r["admission_certificate"]["table_shape_ok"] is False
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_candidate_payload_attempt_parses_json_payload_through_metadata():
    parsed = parse_candidate_payload(synthetic_json_payload(), reviewed_shape_candidate_metadata())
    p = tuple(r.component_id for r in parsed) == FINITE_PART_COMPONENT_ORDER
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_candidate_payload_attempt_component_sum_not_certified_even_on_dry_path():
    att = PayloadAttempt(rows_are_shipped_real_data=True)
    r = payload_attempt_report(shape_candidate_rows(), reviewed_shape_candidate_metadata(), att)
    p = r["rows_admitted"] and r["component_sum_certified"] is False
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_candidate_payload_attempt_physical_export_remains_locked():
    d = _check_completion()
    m = payload_attempt_manifest()
    p = _passed(d) and not m["physical_W_export_enabled"] and not m["exports_physical_M_W"] and not m["real_payload_attempt_rows_admitted"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "completion_gate": d.get("status"), "manifest": m}


def check_T_w_candidate_payload_attempt_bank_closure():
    deps = [
        check_T_w_candidate_payload_attempt_status_declared(),
        check_T_w_candidate_payload_attempt_depends_on_v102_candidate_gate(),
        check_T_w_candidate_payload_attempt_empty_by_default(),
        check_T_w_candidate_payload_attempt_absence_certificate_names_missing_rows(),
        check_T_w_candidate_payload_attempt_does_not_promote_shape_to_real_payload(),
        check_T_w_candidate_payload_attempt_physical_export_remains_locked(),
    ]
    p = all(_passed(d) for d in deps) and not REAL_PAYLOAD_ATTEMPT_ROWS_ADMITTED and not REAL_PAYLOAD_ATTEMPT_COMPONENT_SUM_CERTIFIED and not PHYSICAL_W_EXPORT_ENABLED
    return {
        "passed": p,
        "status": "PASS" if p else "FAIL",
        "tier": 4,
        "epistemic": W_CANDIDATE_PAYLOAD_ATTEMPT_STATUS,
        "dependencies": [str(d.get("status")) for d in deps],
        "manifest": payload_attempt_manifest(),
        "closed_now": "real finite-part payload admission-attempt state machine, absence/failure certificate, and dry-path admission checks",
        "not_closed": "shipped real external rows, component-sum certificate, covariance/uncertainty propagation, physical W export",
    }


_CHECKS: Dict[str, Any] = {
    "T_w_candidate_payload_attempt_status_declared": check_T_w_candidate_payload_attempt_status_declared,
    "T_w_candidate_payload_attempt_depends_on_v102_candidate_gate": check_T_w_candidate_payload_attempt_depends_on_v102_candidate_gate,
    "T_w_candidate_payload_attempt_report_schema_declared": check_T_w_candidate_payload_attempt_report_schema_declared,
    "T_w_candidate_payload_attempt_certificate_schema_declared": check_T_w_candidate_payload_attempt_certificate_schema_declared,
    "T_w_candidate_payload_attempt_empty_by_default": check_T_w_candidate_payload_attempt_empty_by_default,
    "T_w_candidate_payload_attempt_absence_certificate_names_missing_rows": check_T_w_candidate_payload_attempt_absence_certificate_names_missing_rows,
    "T_w_candidate_payload_attempt_shape_rows_cover_all_components": check_T_w_candidate_payload_attempt_shape_rows_cover_all_components,
    "T_w_candidate_payload_attempt_shape_symbols_match": check_T_w_candidate_payload_attempt_shape_symbols_match,
    "T_w_candidate_payload_attempt_candidate_gate_accepts_shape_path": check_T_w_candidate_payload_attempt_candidate_gate_accepts_shape_path,
    "T_w_candidate_payload_attempt_does_not_promote_shape_to_real_payload": check_T_w_candidate_payload_attempt_does_not_promote_shape_to_real_payload,
    "T_w_candidate_payload_attempt_requires_real_payload_flag_for_admission": check_T_w_candidate_payload_attempt_requires_real_payload_flag_for_admission,
    "T_w_candidate_payload_attempt_manifest_remains_no_real_rows": check_T_w_candidate_payload_attempt_manifest_remains_no_real_rows,
    "T_w_candidate_payload_attempt_rejects_physical_export_request": check_T_w_candidate_payload_attempt_rejects_physical_export_request,
    "T_w_candidate_payload_attempt_forbidden_columns_include_observed_W": check_T_w_candidate_payload_attempt_forbidden_columns_include_observed_W,
    "T_w_candidate_payload_attempt_forbidden_columns_include_apf_anchor": check_T_w_candidate_payload_attempt_forbidden_columns_include_apf_anchor,
    "T_w_candidate_payload_attempt_rejects_observed_W_consuming_row": check_T_w_candidate_payload_attempt_rejects_observed_W_consuming_row,
    "T_w_candidate_payload_attempt_rejects_apf_anchor_consuming_row": check_T_w_candidate_payload_attempt_rejects_apf_anchor_consuming_row,
    "T_w_candidate_payload_attempt_rejects_bad_metadata_digest": check_T_w_candidate_payload_attempt_rejects_bad_metadata_digest,
    "T_w_candidate_payload_attempt_rejects_unreviewed_metadata": check_T_w_candidate_payload_attempt_rejects_unreviewed_metadata,
    "T_w_candidate_payload_attempt_rejects_synthetic_metadata": check_T_w_candidate_payload_attempt_rejects_synthetic_metadata,
    "T_w_candidate_payload_attempt_rejects_symbol_mismatch": check_T_w_candidate_payload_attempt_rejects_symbol_mismatch,
    "T_w_candidate_payload_attempt_rejects_missing_component": check_T_w_candidate_payload_attempt_rejects_missing_component,
    "T_w_candidate_payload_attempt_parses_json_payload_through_metadata": check_T_w_candidate_payload_attempt_parses_json_payload_through_metadata,
    "T_w_candidate_payload_attempt_component_sum_not_certified_even_on_dry_path": check_T_w_candidate_payload_attempt_component_sum_not_certified_even_on_dry_path,
    "T_w_candidate_payload_attempt_physical_export_remains_locked": check_T_w_candidate_payload_attempt_physical_export_remains_locked,
    "T_w_candidate_payload_attempt_bank_closure": check_T_w_candidate_payload_attempt_bank_closure,
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
        "status": "W_TRACE_CANDIDATE_PAYLOAD_ATTEMPT_BANK_PASS" if ok else "W_TRACE_CANDIDATE_PAYLOAD_ATTEMPT_BANK_FAIL",
        "checks": rows,
        "manifest": payload_attempt_manifest(),
    }


if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
