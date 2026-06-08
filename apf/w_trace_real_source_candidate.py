"""W_TRACE real external finite-part source-pack candidate gate.

v10.2 (2026-05-09 LATER-20): first real-candidate layer after the v10.1
external ingestion dry-run.  This module defines the admission predicate for an
actual externally supplied W finite-part source pack.  It deliberately ships
with no real external rows: the bank closes the candidate-gate logic and the
failure/absence certificate, not a numerical Delta r component sum and not a
physical W export.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, Sequence, Tuple

from apf.w_trace_external_ingestion_dryrun import (
    W_EXTERNAL_INGESTION_DRYRUN_STATUS,
    PARSER_FORMATS_TESTED,
    parse_external_payload,
    synthetic_json_payload,
    check_T_w_external_ingestion_dryrun_bank_closure as _check_v101,
)
from apf.w_trace_external_source_adapter import (
    EXTERNAL_ADAPTER_VERSION,
    FORBIDDEN_EXTERNAL_ADAPTER_INPUTS,
    ExternalSourceRecord,
    external_adapter_admission_report,
)
from apf.w_trace_finite_part_skeleton import FINITE_PART_COMPONENT_ORDER, COMPONENT_SYMBOLS
from apf.w_trace_finite_part_ledger import apf_anchor_delta_r_target
from apf.trace_transport_completion import (
    check_T_physical_export_gate_locked_until_all_certificates_filled as _check_completion,
)

W_REAL_SOURCE_CANDIDATE_STATUS = "P_w_real_source_candidate_gate"
REAL_SOURCE_CANDIDATE_DECLARED = True
REAL_SOURCE_CANDIDATE_VERSION = "w_trace_real_external_source_candidate_v0"
REAL_SOURCE_CANDIDATE_MODE = "CANDIDATE_ADMISSION_GATE_NO_REAL_ROWS_SHIPPED"
REAL_EXTERNAL_CANDIDATE_ROWS_SUPPLIED = False
REAL_EXTERNAL_CANDIDATE_ROWS_ADMITTED = False
REAL_EXTERNAL_CANDIDATE_PACK_ID = "UNSUPPLIED_REAL_EXTERNAL_PACK"
REAL_EXTERNAL_CANDIDATE_DIGEST = "UNSUPPLIED"
REAL_EXTERNAL_CANDIDATE_URI = "UNSUPPLIED"
REAL_EXTERNAL_CANDIDATE_REVIEW_ATTESTATION = False
REAL_EXTERNAL_CANDIDATE_SYNTHETIC_FIXTURE = False
COMPONENT_SUM_CERTIFIED = False
COVARIANCE_PROTOCOL_SUPPLIED = False
UNCERTAINTY_PROTOCOL_SUPPLIED = False
PHYSICAL_W_TRANSPORT_CLOSED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

REQUIRED_CANDIDATE_METADATA_FIELDS = (
    "candidate_pack_id",
    "candidate_pack_uri",
    "candidate_pack_digest",
    "candidate_adapter_version",
    "candidate_ingest_format",
    "candidate_extraction_log_digest",
    "candidate_review_attestation",
    "candidate_synthetic_fixture",
)

FORBIDDEN_REAL_CANDIDATE_INPUTS = tuple(sorted(set(FORBIDDEN_EXTERNAL_ADAPTER_INPUTS + (
    "APF_ANCHOR_DELTA_R_TARGET",
    "apf_anchor_delta_r_target",
    "delta_r_target_residual",
    "component_sum_residual_to_apf_target",
    "physical_export_request",
))))

@dataclass(frozen=True)
class CandidatePackMetadata:
    candidate_pack_id: str = REAL_EXTERNAL_CANDIDATE_PACK_ID
    candidate_pack_uri: str = REAL_EXTERNAL_CANDIDATE_URI
    candidate_pack_digest: str = REAL_EXTERNAL_CANDIDATE_DIGEST
    candidate_adapter_version: str = EXTERNAL_ADAPTER_VERSION
    candidate_ingest_format: str = "UNSUPPLIED"
    candidate_extraction_log_digest: str = "UNSUPPLIED"
    candidate_review_attestation: bool = REAL_EXTERNAL_CANDIDATE_REVIEW_ATTESTATION
    candidate_synthetic_fixture: bool = REAL_EXTERNAL_CANDIDATE_SYNTHETIC_FIXTURE


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def empty_candidate_rows() -> Tuple[ExternalSourceRecord, ...]:
    return ()


def empty_candidate_metadata() -> CandidatePackMetadata:
    return CandidatePackMetadata()


def _metadata_complete(meta: CandidatePackMetadata | Mapping[str, Any]) -> bool:
    d = asdict(meta) if isinstance(meta, CandidatePackMetadata) else dict(meta)
    if not all(k in d for k in REQUIRED_CANDIDATE_METADATA_FIELDS):
        return False
    if d.get("candidate_adapter_version") != EXTERNAL_ADAPTER_VERSION:
        return False
    if d.get("candidate_ingest_format") not in PARSER_FORMATS_TESTED:
        return False
    if str(d.get("candidate_pack_id")) in {"", "UNSUPPLIED_REAL_EXTERNAL_PACK", "UNSUPPLIED", "None"}:
        return False
    if str(d.get("candidate_pack_uri")) in {"", "UNSUPPLIED", "None"}:
        return False
    if not str(d.get("candidate_pack_digest", "")).startswith("sha256:"):
        return False
    if not str(d.get("candidate_extraction_log_digest", "")).startswith("sha256:"):
        return False
    if d.get("candidate_review_attestation") is not True:
        return False
    if d.get("candidate_synthetic_fixture") is True:
        return False
    return True


def _row_consumes_forbidden(row: ExternalSourceRecord | Mapping[str, Any]) -> bool:
    d = asdict(row) if isinstance(row, ExternalSourceRecord) else dict(row)
    consumed = set(d.get("target_observables_consumed") or ())
    return bool(consumed.intersection(FORBIDDEN_REAL_CANDIDATE_INPUTS) or d.get("apf_target_consumed"))


def candidate_admission_report(rows: Sequence[ExternalSourceRecord | Mapping[str, Any]], meta: CandidatePackMetadata | Mapping[str, Any]) -> Dict[str, Any]:
    adapter_report = external_adapter_admission_report(rows)
    metadata_complete = _metadata_complete(meta)
    forbidden_rows = tuple((r.component_id if isinstance(r, ExternalSourceRecord) else r.get("component_id")) for r in rows if _row_consumes_forbidden(r))
    all_component_symbols_match = all(
        (r.symbol if isinstance(r, ExternalSourceRecord) else r.get("symbol")) == COMPONENT_SYMBOLS.get(r.component_id if isinstance(r, ExternalSourceRecord) else r.get("component_id"))
        for r in rows
    )
    all_rows_independent = adapter_report["all_rows_admitted"] and not forbidden_rows and all_component_symbols_match
    candidate_rows_supplied = len(rows) > 0
    candidate_rows_admitted = candidate_rows_supplied and metadata_complete and all_rows_independent
    failure_reasons = []
    if not candidate_rows_supplied:
        failure_reasons.append("NO_REAL_EXTERNAL_CANDIDATE_ROWS_SUPPLIED")
    if not metadata_complete:
        failure_reasons.append("CANDIDATE_METADATA_INCOMPLETE_OR_UNREVIEWED")
    if not adapter_report["all_rows_admitted"]:
        failure_reasons.append("ADAPTER_ADMISSION_FAILED")
    if forbidden_rows:
        failure_reasons.append("FORBIDDEN_TARGET_OR_APF_ANCHOR_CONSUMED")
    if not all_component_symbols_match:
        failure_reasons.append("COMPONENT_SYMBOL_MISMATCH")
    return {
        "status": W_REAL_SOURCE_CANDIDATE_STATUS,
        "candidate_rows_supplied": candidate_rows_supplied,
        "candidate_rows_admitted": candidate_rows_admitted,
        "metadata_complete": metadata_complete,
        "adapter_report": adapter_report,
        "forbidden_rows": forbidden_rows,
        "all_component_symbols_match": all_component_symbols_match,
        "failure_reasons": tuple(failure_reasons),
        "component_sum_certified": False,
        "physical_W_transport_closed": False,
        "exports_physical_M_W": False,
    }


def parse_candidate_payload(payload: Any, meta: CandidatePackMetadata | Mapping[str, Any]) -> Tuple[ExternalSourceRecord, ...]:
    d = asdict(meta) if isinstance(meta, CandidatePackMetadata) else dict(meta)
    fmt = d.get("candidate_ingest_format")
    return parse_external_payload(payload, fmt)


def real_candidate_manifest() -> Dict[str, Any]:
    report = candidate_admission_report(empty_candidate_rows(), empty_candidate_metadata())
    return {
        "status": W_REAL_SOURCE_CANDIDATE_STATUS,
        "upstream_status": W_EXTERNAL_INGESTION_DRYRUN_STATUS,
        "candidate_version": REAL_SOURCE_CANDIDATE_VERSION,
        "candidate_mode": REAL_SOURCE_CANDIDATE_MODE,
        "required_metadata_fields": REQUIRED_CANDIDATE_METADATA_FIELDS,
        "forbidden_inputs": FORBIDDEN_REAL_CANDIDATE_INPUTS,
        "component_order": FINITE_PART_COMPONENT_ORDER,
        "apf_anchor_delta_r_target_available_only_as_comparison": f"{apf_anchor_delta_r_target():.17E}",
        "real_external_candidate_rows_supplied": REAL_EXTERNAL_CANDIDATE_ROWS_SUPPLIED,
        "real_external_candidate_rows_admitted": REAL_EXTERNAL_CANDIDATE_ROWS_ADMITTED,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "covariance_protocol_supplied": COVARIANCE_PROTOCOL_SUPPLIED,
        "uncertainty_protocol_supplied": UNCERTAINTY_PROTOCOL_SUPPLIED,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "absence_certificate": report,
    }


def check_T_w_real_source_candidate_status_declared():
    p = W_REAL_SOURCE_CANDIDATE_STATUS == "P_w_real_source_candidate_gate" and REAL_SOURCE_CANDIDATE_DECLARED
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_REAL_SOURCE_CANDIDATE_STATUS}


def check_T_w_real_source_candidate_depends_on_v101_ingestion():
    d = _check_v101()
    p = _passed(d) and W_EXTERNAL_INGESTION_DRYRUN_STATUS == "P_w_external_ingestion_dryrun"
    return {"passed": p, "status": "PASS" if p else "FAIL", "upstream": d.get("status")}


def check_T_w_real_source_candidate_metadata_schema_declared():
    p = set(REQUIRED_CANDIDATE_METADATA_FIELDS) == set(asdict(CandidatePackMetadata()).keys())
    return {"passed": p, "status": "PASS" if p else "FAIL", "fields": REQUIRED_CANDIDATE_METADATA_FIELDS}


def check_T_w_real_source_candidate_supported_formats_inherited():
    p = set(PARSER_FORMATS_TESTED) == {"json_rows_v1", "csv_with_header_v1", "python_mapping_rows_v1"}
    return {"passed": p, "status": "PASS" if p else "FAIL", "formats": PARSER_FORMATS_TESTED}


def check_T_w_real_source_candidate_empty_by_default():
    report = candidate_admission_report(empty_candidate_rows(), empty_candidate_metadata())
    p = not report["candidate_rows_supplied"] and not report["candidate_rows_admitted"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_real_source_candidate_absence_certificate_names_missing_rows():
    report = candidate_admission_report(empty_candidate_rows(), empty_candidate_metadata())
    p = "NO_REAL_EXTERNAL_CANDIDATE_ROWS_SUPPLIED" in report["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "failure_reasons": report["failure_reasons"]}


def check_T_w_real_source_candidate_requires_metadata_digest():
    meta = CandidatePackMetadata(candidate_pack_id="pack", candidate_pack_uri="file://pack", candidate_ingest_format="json_rows_v1", candidate_review_attestation=True)
    p = not _metadata_complete(meta)
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_real_source_candidate_requires_extraction_log_digest():
    meta = CandidatePackMetadata(candidate_pack_id="pack", candidate_pack_uri="file://pack", candidate_pack_digest="sha256:abc", candidate_ingest_format="json_rows_v1", candidate_review_attestation=True)
    p = not _metadata_complete(meta)
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_real_source_candidate_requires_review_attestation():
    meta = CandidatePackMetadata(candidate_pack_id="pack", candidate_pack_uri="file://pack", candidate_pack_digest="sha256:abc", candidate_ingest_format="json_rows_v1", candidate_extraction_log_digest="sha256:def")
    p = not _metadata_complete(meta)
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_real_source_candidate_rejects_synthetic_fixture_metadata():
    meta = CandidatePackMetadata(candidate_pack_id="pack", candidate_pack_uri="file://pack", candidate_pack_digest="sha256:abc", candidate_ingest_format="json_rows_v1", candidate_extraction_log_digest="sha256:def", candidate_review_attestation=True, candidate_synthetic_fixture=True)
    p = not _metadata_complete(meta)
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_real_source_candidate_complete_metadata_predicate_positive():
    meta = CandidatePackMetadata(candidate_pack_id="pack", candidate_pack_uri="file://pack", candidate_pack_digest="sha256:abc", candidate_ingest_format="json_rows_v1", candidate_extraction_log_digest="sha256:def", candidate_review_attestation=True)
    p = _metadata_complete(meta)
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_real_source_candidate_parser_uses_metadata_format():
    meta = CandidatePackMetadata(candidate_pack_id="pack", candidate_pack_uri="file://pack", candidate_pack_digest="sha256:abc", candidate_ingest_format="json_rows_v1", candidate_extraction_log_digest="sha256:def", candidate_review_attestation=True)
    rows = parse_candidate_payload(synthetic_json_payload(), meta)
    p = len(rows) == len(FINITE_PART_COMPONENT_ORDER)
    return {"passed": p, "status": "PASS" if p else "FAIL", "row_count": len(rows)}


def check_T_w_real_source_candidate_rejects_bad_metadata_format():
    meta = CandidatePackMetadata(candidate_pack_id="pack", candidate_pack_uri="file://pack", candidate_pack_digest="sha256:abc", candidate_ingest_format="bad_format", candidate_extraction_log_digest="sha256:def", candidate_review_attestation=True)
    p = not _metadata_complete(meta)
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_real_source_candidate_forbidden_inputs_include_apf_target():
    p = "APF_ANCHOR_DELTA_R_TARGET" in FORBIDDEN_REAL_CANDIDATE_INPUTS and "apf_anchor_delta_r_column" in FORBIDDEN_REAL_CANDIDATE_INPUTS
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_real_source_candidate_forbidden_inputs_include_observed_W():
    p = "observed_M_W_column" in FORBIDDEN_REAL_CANDIDATE_INPUTS and "world_average_W_mass_column" in FORBIDDEN_REAL_CANDIDATE_INPUTS
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_real_source_candidate_forbidden_inputs_include_residual_fit():
    p = "fit_residual_column" in FORBIDDEN_REAL_CANDIDATE_INPUTS and "component_sum_residual_to_apf_target" in FORBIDDEN_REAL_CANDIDATE_INPUTS
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_real_source_candidate_rejects_apf_anchor_consuming_rows():
    rows = list(parse_external_payload(synthetic_json_payload(), "json_rows_v1"))
    bad = asdict(rows[0]); bad["apf_target_consumed"] = True
    rows[0] = ExternalSourceRecord(**bad)
    meta = CandidatePackMetadata(candidate_pack_id="pack", candidate_pack_uri="file://pack", candidate_pack_digest="sha256:abc", candidate_ingest_format="json_rows_v1", candidate_extraction_log_digest="sha256:def", candidate_review_attestation=True)
    report = candidate_admission_report(rows, meta)
    p = not report["candidate_rows_admitted"] and "FORBIDDEN_TARGET_OR_APF_ANCHOR_CONSUMED" in report["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_real_source_candidate_rejects_observed_W_consuming_rows():
    rows = list(parse_external_payload(synthetic_json_payload(), "json_rows_v1"))
    bad = asdict(rows[0]); bad["target_observables_consumed"] = ("observed_M_W_column",)
    rows[0] = ExternalSourceRecord(**bad)
    meta = CandidatePackMetadata(candidate_pack_id="pack", candidate_pack_uri="file://pack", candidate_pack_digest="sha256:abc", candidate_ingest_format="json_rows_v1", candidate_extraction_log_digest="sha256:def", candidate_review_attestation=True)
    report = candidate_admission_report(rows, meta)
    p = not report["candidate_rows_admitted"] and "FORBIDDEN_TARGET_OR_APF_ANCHOR_CONSUMED" in report["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_real_source_candidate_rejects_symbol_mismatch():
    rows = list(parse_external_payload(synthetic_json_payload(), "json_rows_v1"))
    bad = asdict(rows[0]); bad["symbol"] = "WRONG_SYMBOL"
    rows[0] = ExternalSourceRecord(**bad)
    meta = CandidatePackMetadata(candidate_pack_id="pack", candidate_pack_uri="file://pack", candidate_pack_digest="sha256:abc", candidate_ingest_format="json_rows_v1", candidate_extraction_log_digest="sha256:def", candidate_review_attestation=True)
    report = candidate_admission_report(rows, meta)
    p = not report["candidate_rows_admitted"] and "COMPONENT_SYMBOL_MISMATCH" in report["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_real_source_candidate_rejects_incomplete_table_shape():
    rows = parse_external_payload(synthetic_json_payload(), "json_rows_v1")[:-1]
    meta = CandidatePackMetadata(candidate_pack_id="pack", candidate_pack_uri="file://pack", candidate_pack_digest="sha256:abc", candidate_ingest_format="json_rows_v1", candidate_extraction_log_digest="sha256:def", candidate_review_attestation=True)
    report = candidate_admission_report(rows, meta)
    p = not report["candidate_rows_admitted"] and not report["adapter_report"]["table_shape_ok"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_real_source_candidate_does_not_certify_component_sum():
    p = not COMPONENT_SUM_CERTIFIED and not real_candidate_manifest()["component_sum_certified"]
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_real_source_candidate_does_not_supply_covariance_or_uncertainty():
    p = not COVARIANCE_PROTOCOL_SUPPLIED and not UNCERTAINTY_PROTOCOL_SUPPLIED
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_real_source_candidate_physical_export_remains_locked():
    d = _check_completion()
    p = _passed(d) and not PHYSICAL_W_TRANSPORT_CLOSED and not EXPORTS_PHYSICAL_M_W and not EXPORTS_PHYSICAL_SCHEME_MASSES
    return {"passed": p, "status": "PASS" if p else "FAIL", "completion_gate": d.get("status")}


def check_T_w_real_source_candidate_manifest_shape():
    m = real_candidate_manifest()
    p = m["status"] == W_REAL_SOURCE_CANDIDATE_STATUS and tuple(m["component_order"]) == FINITE_PART_COMPONENT_ORDER and m["absence_certificate"]["candidate_rows_admitted"] is False
    return {"passed": p, "status": "PASS" if p else "FAIL", "manifest": m}


def check_T_w_real_source_candidate_bank_closure():
    deps = [
        check_T_w_real_source_candidate_status_declared(),
        check_T_w_real_source_candidate_depends_on_v101_ingestion(),
        check_T_w_real_source_candidate_empty_by_default(),
        check_T_w_real_source_candidate_absence_certificate_names_missing_rows(),
        check_T_w_real_source_candidate_physical_export_remains_locked(),
    ]
    p = all(_passed(d) for d in deps) and not REAL_EXTERNAL_CANDIDATE_ROWS_ADMITTED and not COMPONENT_SUM_CERTIFIED and not PHYSICAL_W_TRANSPORT_CLOSED
    return {
        "passed": p,
        "status": "PASS" if p else "FAIL",
        "tier": 4,
        "epistemic": W_REAL_SOURCE_CANDIDATE_STATUS,
        "dependencies": [str(d.get("status")) for d in deps],
        "manifest": real_candidate_manifest(),
        "closed_now": "real external finite-part candidate-pack admission/failure gate and absence certificate",
        "not_closed": "actual real finite-part rows, component-sum certificate, covariance/uncertainty propagation, physical W export",
    }


_CHECKS: Dict[str, Any] = {
    "T_w_real_source_candidate_status_declared": check_T_w_real_source_candidate_status_declared,
    "T_w_real_source_candidate_depends_on_v101_ingestion": check_T_w_real_source_candidate_depends_on_v101_ingestion,
    "T_w_real_source_candidate_metadata_schema_declared": check_T_w_real_source_candidate_metadata_schema_declared,
    "T_w_real_source_candidate_supported_formats_inherited": check_T_w_real_source_candidate_supported_formats_inherited,
    "T_w_real_source_candidate_empty_by_default": check_T_w_real_source_candidate_empty_by_default,
    "T_w_real_source_candidate_absence_certificate_names_missing_rows": check_T_w_real_source_candidate_absence_certificate_names_missing_rows,
    "T_w_real_source_candidate_requires_metadata_digest": check_T_w_real_source_candidate_requires_metadata_digest,
    "T_w_real_source_candidate_requires_extraction_log_digest": check_T_w_real_source_candidate_requires_extraction_log_digest,
    "T_w_real_source_candidate_requires_review_attestation": check_T_w_real_source_candidate_requires_review_attestation,
    "T_w_real_source_candidate_rejects_synthetic_fixture_metadata": check_T_w_real_source_candidate_rejects_synthetic_fixture_metadata,
    "T_w_real_source_candidate_complete_metadata_predicate_positive": check_T_w_real_source_candidate_complete_metadata_predicate_positive,
    "T_w_real_source_candidate_parser_uses_metadata_format": check_T_w_real_source_candidate_parser_uses_metadata_format,
    "T_w_real_source_candidate_rejects_bad_metadata_format": check_T_w_real_source_candidate_rejects_bad_metadata_format,
    "T_w_real_source_candidate_forbidden_inputs_include_apf_target": check_T_w_real_source_candidate_forbidden_inputs_include_apf_target,
    "T_w_real_source_candidate_forbidden_inputs_include_observed_W": check_T_w_real_source_candidate_forbidden_inputs_include_observed_W,
    "T_w_real_source_candidate_forbidden_inputs_include_residual_fit": check_T_w_real_source_candidate_forbidden_inputs_include_residual_fit,
    "T_w_real_source_candidate_rejects_apf_anchor_consuming_rows": check_T_w_real_source_candidate_rejects_apf_anchor_consuming_rows,
    "T_w_real_source_candidate_rejects_observed_W_consuming_rows": check_T_w_real_source_candidate_rejects_observed_W_consuming_rows,
    "T_w_real_source_candidate_rejects_symbol_mismatch": check_T_w_real_source_candidate_rejects_symbol_mismatch,
    "T_w_real_source_candidate_rejects_incomplete_table_shape": check_T_w_real_source_candidate_rejects_incomplete_table_shape,
    "T_w_real_source_candidate_does_not_certify_component_sum": check_T_w_real_source_candidate_does_not_certify_component_sum,
    "T_w_real_source_candidate_does_not_supply_covariance_or_uncertainty": check_T_w_real_source_candidate_does_not_supply_covariance_or_uncertainty,
    "T_w_real_source_candidate_physical_export_remains_locked": check_T_w_real_source_candidate_physical_export_remains_locked,
    "T_w_real_source_candidate_manifest_shape": check_T_w_real_source_candidate_manifest_shape,
    "T_w_real_source_candidate_bank_closure": check_T_w_real_source_candidate_bank_closure,
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
    return {"passed": ok, "status": "W_TRACE_REAL_SOURCE_CANDIDATE_BANK_PASS" if ok else "W_TRACE_REAL_SOURCE_CANDIDATE_BANK_FAIL", "checks": rows, "manifest": real_candidate_manifest()}


if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
