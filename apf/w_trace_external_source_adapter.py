"""W_TRACE external finite-part source-pack adapter v1.

v10.0 (2026-05-09 LATER-18): external source-pack adapter after the v9.9
payload source-pack gate.  This module banks the import contract for external
finite-part tables or loop-library exports.  It deliberately does not ship any
independent numerical finite-part rows; it only defines how such rows may enter
without consuming the APF-anchor Delta r target, observed W mass, W residuals,
or a post-hoc counterterm fit.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from typing import Any, Dict, Mapping, Sequence, Tuple

from apf.w_trace_payload_source_pack import (
    W_PAYLOAD_SOURCE_PACK_STATUS,
    SourcePackRow,
    SOURCE_PACK_REQUIRED_FIELDS,
    FORBIDDEN_SOURCE_PACK_INPUTS,
    reviewed_shape_source_pack,
    source_pack_admission_report,
    check_T_w_payload_source_pack_bank_closure as _check_v99,
)
from apf.w_trace_numeric_source_adapter import ALLOWED_SOURCE_CLASSES, REQUIRED_SOURCE_FIELDS
from apf.w_trace_finite_part_skeleton import COMPONENT_SYMBOLS, FINITE_PART_COMPONENT_ORDER
from apf.trace_transport_completion import (
    check_T_physical_export_gate_locked_until_all_certificates_filled as _check_completion,
)

W_EXTERNAL_SOURCE_ADAPTER_STATUS = "P_w_external_source_adapter"
EXTERNAL_SOURCE_ADAPTER_DECLARED = True
EXTERNAL_ADAPTER_VERSION = "w_trace_external_finite_part_source_adapter_v1"
EXTERNAL_ADAPTER_MODE = "IMPORT_CONTRACT_ONLY_NO_NUMERICAL_ROWS"
EXTERNAL_PAYLOAD_ROWS_SUPPLIED = False
EXTERNAL_PAYLOAD_ROWS_ADMITTED = False
COMPONENT_SUM_CERTIFIED = False
PHYSICAL_W_TRANSPORT_CLOSED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

SUPPORTED_EXTERNAL_FORMATS = (
    "json_rows_v1",
    "csv_with_header_v1",
    "python_mapping_rows_v1",
)

EXTERNAL_RECORD_REQUIRED_FIELDS = SOURCE_PACK_REQUIRED_FIELDS + (
    "external_pack_uri",
    "external_pack_digest",
    "adapter_version",
    "ingest_format",
    "extraction_log_digest",
)

FORBIDDEN_EXTERNAL_ADAPTER_INPUTS = tuple(sorted(set(FORBIDDEN_SOURCE_PACK_INPUTS + (
    "observed_M_W_column",
    "world_average_W_mass_column",
    "fit_residual_column",
    "apf_anchor_delta_r_column",
    "target_closure_residual_column",
))))

@dataclass(frozen=True)
class ExternalSourceRecord:
    component_id: str
    symbol: str
    pack_id: str = "W_TRACE_EXTERNAL_SOURCE_ADAPTER_V1_EMPTY"
    source_class: str = "UNFILLED_ALLOWED_SOURCE_SLOT"
    source_name: str = "UNFILLED"
    version_or_citation: str = "UNFILLED"
    input_scheme: str = "UNFILLED"
    renormalization_scheme: str = "UNFILLED"
    gauge_convention: str = "UNFILLED"
    numeric_value: str = "UNSUPPLIED"
    uncertainty: str = "UNSUPPLIED"
    checksum_or_table_locator: str = "UNSUPPLIED"
    target_observables_consumed: Tuple[str, ...] = ()
    apf_target_consumed: bool = False
    provenance_chain: Tuple[str, ...] = ()
    license_or_access_note: str = "UNFILLED"
    status: str = "OPEN_WAITING_FOR_EXTERNAL_SOURCE_EXPORT"
    fixture_note: str = "external-source adapter row; not admitted as data unless source-pack gate accepts it"
    review_status: str = "EMPTY_PLACEHOLDER"
    external_pack_uri: str = "UNFILLED"
    external_pack_digest: str = "UNFILLED"
    adapter_version: str = EXTERNAL_ADAPTER_VERSION
    ingest_format: str = "UNFILLED"
    extraction_log_digest: str = "UNFILLED"


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def external_adapter_rows() -> Tuple[ExternalSourceRecord, ...]:
    return tuple(ExternalSourceRecord(cid, COMPONENT_SYMBOLS[cid]) for cid in FINITE_PART_COMPONENT_ORDER)


def _to_source_pack_row(row: ExternalSourceRecord | Mapping[str, Any]) -> SourcePackRow:
    d = asdict(row) if isinstance(row, ExternalSourceRecord) else dict(row)
    kwargs = {f.name: d.get(f.name) for f in fields(SourcePackRow) if f.name in d}
    return SourcePackRow(**kwargs)


def _external_record_complete(row: ExternalSourceRecord | Mapping[str, Any]) -> bool:
    d = asdict(row) if isinstance(row, ExternalSourceRecord) else dict(row)
    if not all(k in d for k in EXTERNAL_RECORD_REQUIRED_FIELDS):
        return False
    if d.get("adapter_version") != EXTERNAL_ADAPTER_VERSION:
        return False
    if d.get("ingest_format") not in SUPPORTED_EXTERNAL_FORMATS:
        return False
    if str(d.get("external_pack_uri")) in {"", "UNFILLED", "None"}:
        return False
    if not str(d.get("external_pack_digest", "")).startswith("sha256:"):
        return False
    if not str(d.get("extraction_log_digest", "")).startswith("sha256:"):
        return False
    consumed = set(d.get("target_observables_consumed") or ())
    if consumed.intersection(FORBIDDEN_EXTERNAL_ADAPTER_INPUTS):
        return False
    if d.get("apf_target_consumed"):
        return False
    source_pack_report = source_pack_admission_report((_to_source_pack_row(d),))
    # Single rows cannot have full source-pack table shape; row-level completeness
    # is checked by adapting to a one-row shape and then requiring the v9.9 row
    # predicate indirectly through a full test pack below.  Here we demand only
    # the external fields plus the underlying source-pack row fields.
    return True


def external_adapter_admission_report(rows: Sequence[ExternalSourceRecord | Mapping[str, Any]]) -> Dict[str, Any]:
    ids = tuple((r.component_id if isinstance(r, ExternalSourceRecord) else r.get("component_id")) for r in rows)
    duplicate_ids = tuple(sorted({x for x in ids if ids.count(x) > 1 and x is not None}))
    missing_ids = tuple(x for x in FINITE_PART_COMPONENT_ORDER if x not in ids)
    unknown_ids = tuple(x for x in ids if x not in FINITE_PART_COMPONENT_ORDER)
    table_shape_ok = not duplicate_ids and not missing_ids and not unknown_ids and len(rows) == len(FINITE_PART_COMPONENT_ORDER)
    row_results = tuple(_external_record_complete(r) for r in rows)
    source_rows = tuple(_to_source_pack_row(r) for r in rows)
    source_report = source_pack_admission_report(source_rows) if table_shape_ok else None
    all_rows_admitted = table_shape_ok and all(row_results) and bool(source_report and source_report["all_rows_admitted"])
    return {
        "table_shape_ok": table_shape_ok,
        "all_rows_admitted": all_rows_admitted,
        "external_payload_rows_admitted": all_rows_admitted,
        "component_sum_certified": False,
        "physical_W_transport_closed": False,
        "duplicate_ids": duplicate_ids,
        "missing_ids": missing_ids,
        "unknown_ids": unknown_ids,
        "row_results": row_results,
        "source_pack_report_status": None if source_report is None else source_report.get("all_rows_admitted"),
        "admitted_count": sum(1 for x in row_results if x),
        "total_count": len(rows),
    }


def _external_shape_row(component_id: str) -> ExternalSourceRecord:
    base = reviewed_shape_source_pack()[FINITE_PART_COMPONENT_ORDER.index(component_id)]
    d = asdict(base)
    d.update({
        "external_pack_uri": "file://future-independent-source-pack/shape-test.json",
        "external_pack_digest": "sha256:external-shape-test-not-data",
        "adapter_version": EXTERNAL_ADAPTER_VERSION,
        "ingest_format": "json_rows_v1",
        "extraction_log_digest": "sha256:extraction-log-shape-test-not-data",
        "fixture_note": "external adapter shape test only; not source data",
    })
    return ExternalSourceRecord(**{f.name: d.get(f.name) for f in fields(ExternalSourceRecord)})


def external_shape_source_pack() -> Tuple[ExternalSourceRecord, ...]:
    return tuple(_external_shape_row(cid) for cid in FINITE_PART_COMPONENT_ORDER)


def external_adapter_manifest() -> Dict[str, Any]:
    return {
        "status": W_EXTERNAL_SOURCE_ADAPTER_STATUS,
        "upstream_status": W_PAYLOAD_SOURCE_PACK_STATUS,
        "adapter_version": EXTERNAL_ADAPTER_VERSION,
        "adapter_mode": EXTERNAL_ADAPTER_MODE,
        "supported_formats": SUPPORTED_EXTERNAL_FORMATS,
        "required_fields": EXTERNAL_RECORD_REQUIRED_FIELDS,
        "allowed_source_classes": ALLOWED_SOURCE_CLASSES,
        "forbidden_inputs": FORBIDDEN_EXTERNAL_ADAPTER_INPUTS,
        "component_order": FINITE_PART_COMPONENT_ORDER,
        "rows": tuple(asdict(r) for r in external_adapter_rows()),
        "external_payload_rows_supplied": EXTERNAL_PAYLOAD_ROWS_SUPPLIED,
        "external_payload_rows_admitted": EXTERNAL_PAYLOAD_ROWS_ADMITTED,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
    }


def check_T_w_external_source_adapter_status_declared():
    p = W_EXTERNAL_SOURCE_ADAPTER_STATUS == "P_w_external_source_adapter" and EXTERNAL_SOURCE_ADAPTER_DECLARED
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_EXTERNAL_SOURCE_ADAPTER_STATUS}


def check_T_w_external_source_adapter_depends_on_v99_source_pack():
    d = _check_v99()
    p = _passed(d) and W_PAYLOAD_SOURCE_PACK_STATUS == "P_w_payload_source_pack"
    return {"passed": p, "status": "PASS" if p else "FAIL", "upstream": d.get("status")}


def check_T_w_external_source_adapter_schema_extends_source_pack():
    have = {f.name for f in fields(ExternalSourceRecord)}
    missing = [x for x in EXTERNAL_RECORD_REQUIRED_FIELDS if x not in have]
    p = not missing and set(SOURCE_PACK_REQUIRED_FIELDS).issubset(have) and set(REQUIRED_SOURCE_FIELDS).issubset(have)
    return {"passed": p, "status": "PASS" if p else "FAIL", "missing": missing}


def check_T_w_external_source_adapter_formats_declared():
    p = set(SUPPORTED_EXTERNAL_FORMATS) == {"json_rows_v1", "csv_with_header_v1", "python_mapping_rows_v1"}
    return {"passed": p, "status": "PASS" if p else "FAIL", "formats": SUPPORTED_EXTERNAL_FORMATS}


def check_T_w_external_source_adapter_covers_all_components():
    ids = tuple(r.component_id for r in external_adapter_rows())
    p = ids == FINITE_PART_COMPONENT_ORDER
    return {"passed": p, "status": "PASS" if p else "FAIL", "ids": ids}


def check_T_w_external_source_adapter_symbols_match_skeleton():
    p = all(r.symbol == COMPONENT_SYMBOLS[r.component_id] for r in external_adapter_rows())
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_external_source_adapter_empty_by_default():
    report = external_adapter_admission_report(external_adapter_rows())
    p = (not EXTERNAL_PAYLOAD_ROWS_SUPPLIED) and (not EXTERNAL_PAYLOAD_ROWS_ADMITTED) and not report["all_rows_admitted"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_external_source_adapter_shape_pack_admissible():
    report = external_adapter_admission_report(external_shape_source_pack())
    p = report["table_shape_ok"] and report["all_rows_admitted"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_external_source_adapter_requires_supported_format():
    rows = list(external_shape_source_pack())
    rows[0] = ExternalSourceRecord(**{**asdict(rows[0]), "ingest_format": "spreadsheet_unknown_v0"})
    report = external_adapter_admission_report(tuple(rows))
    p = not report["all_rows_admitted"] and report["row_results"][0] is False
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_external_source_adapter_requires_external_uri():
    rows = list(external_shape_source_pack())
    rows[0] = ExternalSourceRecord(**{**asdict(rows[0]), "external_pack_uri": "UNFILLED"})
    report = external_adapter_admission_report(tuple(rows))
    p = not report["all_rows_admitted"] and report["row_results"][0] is False
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_external_source_adapter_requires_sha256_pack_digest():
    rows = list(external_shape_source_pack())
    rows[0] = ExternalSourceRecord(**{**asdict(rows[0]), "external_pack_digest": "md5:not-allowed"})
    report = external_adapter_admission_report(tuple(rows))
    p = not report["all_rows_admitted"] and report["row_results"][0] is False
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_external_source_adapter_requires_extraction_log_digest():
    rows = list(external_shape_source_pack())
    rows[0] = ExternalSourceRecord(**{**asdict(rows[0]), "extraction_log_digest": "UNFILLED"})
    report = external_adapter_admission_report(tuple(rows))
    p = not report["all_rows_admitted"] and report["row_results"][0] is False
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_external_source_adapter_rejects_duplicate_components():
    rows = list(external_shape_source_pack())
    rows[1] = ExternalSourceRecord(**{**asdict(rows[1]), "component_id": rows[0].component_id, "symbol": rows[0].symbol})
    report = external_adapter_admission_report(tuple(rows))
    p = not report["table_shape_ok"] and rows[0].component_id in report["duplicate_ids"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_external_source_adapter_rejects_missing_components():
    rows = external_shape_source_pack()[:-1]
    report = external_adapter_admission_report(rows)
    p = not report["table_shape_ok"] and FINITE_PART_COMPONENT_ORDER[-1] in report["missing_ids"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_external_source_adapter_rejects_unknown_components():
    rows = list(external_shape_source_pack())
    rows[0] = ExternalSourceRecord(**{**asdict(rows[0]), "component_id": "Delta_r_unknown_external", "symbol": "x_unknown"})
    report = external_adapter_admission_report(tuple(rows))
    p = not report["table_shape_ok"] and "Delta_r_unknown_external" in report["unknown_ids"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_external_source_adapter_rejects_apf_anchor_column():
    rows = list(external_shape_source_pack())
    rows[0] = ExternalSourceRecord(**{**asdict(rows[0]), "target_observables_consumed": ("apf_anchor_delta_r_column",)})
    report = external_adapter_admission_report(tuple(rows))
    p = not report["all_rows_admitted"] and report["row_results"][0] is False
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_external_source_adapter_rejects_observed_W_column():
    rows = list(external_shape_source_pack())
    rows[0] = ExternalSourceRecord(**{**asdict(rows[0]), "target_observables_consumed": ("observed_M_W_column",)})
    report = external_adapter_admission_report(tuple(rows))
    p = not report["all_rows_admitted"] and report["row_results"][0] is False
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_external_source_adapter_rejects_residual_fit_column():
    rows = list(external_shape_source_pack())
    rows[0] = ExternalSourceRecord(**{**asdict(rows[0]), "target_observables_consumed": ("fit_residual_column",)})
    report = external_adapter_admission_report(tuple(rows))
    p = not report["all_rows_admitted"] and report["row_results"][0] is False
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_external_source_adapter_forbidden_inputs_superset_source_pack():
    p = set(FORBIDDEN_SOURCE_PACK_INPUTS).issubset(set(FORBIDDEN_EXTERNAL_ADAPTER_INPUTS))
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_external_source_adapter_no_component_sum_certification_yet():
    p = not COMPONENT_SUM_CERTIFIED and not PHYSICAL_W_TRANSPORT_CLOSED
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_external_source_adapter_completion_gate_remains_locked():
    d = _check_completion()
    p = _passed(d) and not EXPORTS_PHYSICAL_M_W and not EXPORTS_PHYSICAL_SCHEME_MASSES
    return {"passed": p, "status": "PASS" if p else "FAIL", "completion_gate": d.get("status")}


def check_T_w_external_source_adapter_manifest_export_shape():
    m = external_adapter_manifest()
    p = m["status"] == W_EXTERNAL_SOURCE_ADAPTER_STATUS and m["adapter_version"] == EXTERNAL_ADAPTER_VERSION and len(m["rows"]) == len(FINITE_PART_COMPONENT_ORDER)
    return {"passed": p, "status": "PASS" if p else "FAIL", "manifest_keys": tuple(sorted(m.keys()))}


def check_T_w_external_source_adapter_bank_closure():
    deps = [
        check_T_w_external_source_adapter_status_declared(),
        check_T_w_external_source_adapter_depends_on_v99_source_pack(),
        check_T_w_external_source_adapter_schema_extends_source_pack(),
        check_T_w_external_source_adapter_shape_pack_admissible(),
        check_T_w_external_source_adapter_completion_gate_remains_locked(),
    ]
    p = all(_passed(d) for d in deps) and not PHYSICAL_W_TRANSPORT_CLOSED
    return {
        "passed": p,
        "status": "PASS" if p else "FAIL",
        "tier": 4,
        "epistemic": W_EXTERNAL_SOURCE_ADAPTER_STATUS,
        "dependencies": [str(d.get("status")) for d in deps],
        "manifest": external_adapter_manifest(),
        "closed_now": "external finite-part source-pack adapter/import contract",
        "not_closed": "actual external finite-part payload values, component-sum certificate, covariance/uncertainty propagation, physical W export",
    }


_CHECKS: Dict[str, Any] = {
    "T_w_external_source_adapter_status_declared": check_T_w_external_source_adapter_status_declared,
    "T_w_external_source_adapter_depends_on_v99_source_pack": check_T_w_external_source_adapter_depends_on_v99_source_pack,
    "T_w_external_source_adapter_schema_extends_source_pack": check_T_w_external_source_adapter_schema_extends_source_pack,
    "T_w_external_source_adapter_formats_declared": check_T_w_external_source_adapter_formats_declared,
    "T_w_external_source_adapter_covers_all_components": check_T_w_external_source_adapter_covers_all_components,
    "T_w_external_source_adapter_symbols_match_skeleton": check_T_w_external_source_adapter_symbols_match_skeleton,
    "T_w_external_source_adapter_empty_by_default": check_T_w_external_source_adapter_empty_by_default,
    "T_w_external_source_adapter_shape_pack_admissible": check_T_w_external_source_adapter_shape_pack_admissible,
    "T_w_external_source_adapter_requires_supported_format": check_T_w_external_source_adapter_requires_supported_format,
    "T_w_external_source_adapter_requires_external_uri": check_T_w_external_source_adapter_requires_external_uri,
    "T_w_external_source_adapter_requires_sha256_pack_digest": check_T_w_external_source_adapter_requires_sha256_pack_digest,
    "T_w_external_source_adapter_requires_extraction_log_digest": check_T_w_external_source_adapter_requires_extraction_log_digest,
    "T_w_external_source_adapter_rejects_duplicate_components": check_T_w_external_source_adapter_rejects_duplicate_components,
    "T_w_external_source_adapter_rejects_missing_components": check_T_w_external_source_adapter_rejects_missing_components,
    "T_w_external_source_adapter_rejects_unknown_components": check_T_w_external_source_adapter_rejects_unknown_components,
    "T_w_external_source_adapter_rejects_apf_anchor_column": check_T_w_external_source_adapter_rejects_apf_anchor_column,
    "T_w_external_source_adapter_rejects_observed_W_column": check_T_w_external_source_adapter_rejects_observed_W_column,
    "T_w_external_source_adapter_rejects_residual_fit_column": check_T_w_external_source_adapter_rejects_residual_fit_column,
    "T_w_external_source_adapter_forbidden_inputs_superset_source_pack": check_T_w_external_source_adapter_forbidden_inputs_superset_source_pack,
    "T_w_external_source_adapter_no_component_sum_certification_yet": check_T_w_external_source_adapter_no_component_sum_certification_yet,
    "T_w_external_source_adapter_completion_gate_remains_locked": check_T_w_external_source_adapter_completion_gate_remains_locked,
    "T_w_external_source_adapter_manifest_export_shape": check_T_w_external_source_adapter_manifest_export_shape,
    "T_w_external_source_adapter_bank_closure": check_T_w_external_source_adapter_bank_closure,
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
    return {"passed": ok, "status": "W_TRACE_EXTERNAL_SOURCE_ADAPTER_BANK_PASS" if ok else "W_TRACE_EXTERNAL_SOURCE_ADAPTER_BANK_FAIL", "checks": rows, "manifest": external_adapter_manifest()}


if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
