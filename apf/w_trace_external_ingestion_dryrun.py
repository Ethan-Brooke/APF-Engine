"""W_TRACE external payload ingestion dry-run / parser fixtures.

v10.1 (2026-05-09 LATER-19): parser-fixture layer after the v10.0
external source adapter.  This module exercises JSON/CSV/Python-mapping
payload shapes using synthetic, non-physical shape rows.  It deliberately
admits no real finite-part numerical source rows and exports no physical W
value.  Its role is to prove that future external source packs can be parsed
into the v10.0 adapter contract without weakening the anti-backsolve,
anti-APF-target, anti-observed-W, and physical-export locks.
"""
from __future__ import annotations

import csv
import io
import json
from dataclasses import asdict, fields
from typing import Any, Dict, Iterable, Mapping, Sequence, Tuple

from apf.w_trace_external_source_adapter import (
    EXTERNAL_ADAPTER_VERSION,
    W_EXTERNAL_SOURCE_ADAPTER_STATUS,
    FORBIDDEN_EXTERNAL_ADAPTER_INPUTS,
    SUPPORTED_EXTERNAL_FORMATS,
    ExternalSourceRecord,
    external_adapter_admission_report,
    external_shape_source_pack,
    check_T_w_external_source_adapter_bank_closure as _check_v100,
)
from apf.w_trace_finite_part_skeleton import FINITE_PART_COMPONENT_ORDER, COMPONENT_SYMBOLS
from apf.trace_transport_completion import (
    check_T_physical_export_gate_locked_until_all_certificates_filled as _check_completion,
)

W_EXTERNAL_INGESTION_DRYRUN_STATUS = "P_w_external_ingestion_dryrun"
INGESTION_DRYRUN_DECLARED = True
INGESTION_DRYRUN_VERSION = "w_trace_external_payload_ingestion_dryrun_v1"
INGESTION_MODE = "SYNTHETIC_PARSER_FIXTURES_NO_REAL_NUMERICAL_ROWS"
SYNTHETIC_FIXTURES_ONLY = True
REAL_EXTERNAL_PAYLOAD_ROWS_SUPPLIED = False
REAL_EXTERNAL_PAYLOAD_ROWS_ADMITTED = False
COMPONENT_SUM_CERTIFIED = False
PHYSICAL_W_TRANSPORT_CLOSED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

TUPLE_FIELDS = ("target_observables_consumed", "provenance_chain")
RECORD_FIELDS = tuple(f.name for f in fields(ExternalSourceRecord))
PARSER_FORMATS_TESTED = ("json_rows_v1", "csv_with_header_v1", "python_mapping_rows_v1")


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def _coerce_tuple(value: Any) -> Tuple[Any, ...]:
    if value in (None, "", "()", "[]"):
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    if isinstance(value, str):
        s = value.strip()
        if s.startswith("[") or s.startswith("("):
            try:
                parsed = json.loads(s.replace("(", "[").replace(")", "]"))
                return tuple(parsed)
            except Exception:
                return (value,)
        return (value,)
    return tuple(value) if isinstance(value, Iterable) and not isinstance(value, (bytes, bytearray, str)) else (value,)


def _normalize_row(row: Mapping[str, Any], ingest_format: str | None = None) -> ExternalSourceRecord:
    d = {k: row.get(k) for k in RECORD_FIELDS if k in row}
    for field in TUPLE_FIELDS:
        if field in d:
            d[field] = _coerce_tuple(d[field])
    if "apf_target_consumed" in d and isinstance(d["apf_target_consumed"], str):
        d["apf_target_consumed"] = d["apf_target_consumed"].strip().lower() == "true"
    if ingest_format is not None:
        d["ingest_format"] = ingest_format
    return ExternalSourceRecord(**d)


def synthetic_shape_rows(ingest_format: str = "json_rows_v1") -> Tuple[ExternalSourceRecord, ...]:
    return tuple(_normalize_row(asdict(r), ingest_format) for r in external_shape_source_pack())


def synthetic_json_payload() -> str:
    rows = [asdict(r) for r in synthetic_shape_rows("json_rows_v1")]
    return json.dumps({"adapter_version": EXTERNAL_ADAPTER_VERSION, "rows": rows}, sort_keys=True)


def parse_json_rows_v1(payload: str) -> Tuple[ExternalSourceRecord, ...]:
    data = json.loads(payload)
    if data.get("adapter_version") != EXTERNAL_ADAPTER_VERSION:
        raise ValueError("adapter_version mismatch")
    rows = data.get("rows")
    if not isinstance(rows, list):
        raise ValueError("rows must be a list")
    return tuple(_normalize_row(row, "json_rows_v1") for row in rows)


def synthetic_csv_payload() -> str:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=RECORD_FIELDS)
    writer.writeheader()
    for r in synthetic_shape_rows("csv_with_header_v1"):
        row = asdict(r)
        for field in TUPLE_FIELDS:
            row[field] = json.dumps(list(row[field]))
        writer.writerow(row)
    return output.getvalue()


def parse_csv_with_header_v1(payload: str) -> Tuple[ExternalSourceRecord, ...]:
    reader = csv.DictReader(io.StringIO(payload))
    if tuple(reader.fieldnames or ()) != RECORD_FIELDS:
        raise ValueError("CSV header does not match ExternalSourceRecord schema")
    return tuple(_normalize_row(row, "csv_with_header_v1") for row in reader)


def synthetic_python_mapping_payload() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(r) for r in synthetic_shape_rows("python_mapping_rows_v1"))


def parse_python_mapping_rows_v1(payload: Sequence[Mapping[str, Any]]) -> Tuple[ExternalSourceRecord, ...]:
    return tuple(_normalize_row(row, "python_mapping_rows_v1") for row in payload)


def parse_external_payload(payload: Any, ingest_format: str) -> Tuple[ExternalSourceRecord, ...]:
    if ingest_format == "json_rows_v1":
        return parse_json_rows_v1(payload)
    if ingest_format == "csv_with_header_v1":
        return parse_csv_with_header_v1(payload)
    if ingest_format == "python_mapping_rows_v1":
        return parse_python_mapping_rows_v1(payload)
    raise ValueError(f"unsupported ingest_format: {ingest_format}")


def ingestion_dryrun_report() -> Dict[str, Any]:
    parsed = {
        "json_rows_v1": parse_external_payload(synthetic_json_payload(), "json_rows_v1"),
        "csv_with_header_v1": parse_external_payload(synthetic_csv_payload(), "csv_with_header_v1"),
        "python_mapping_rows_v1": parse_external_payload(synthetic_python_mapping_payload(), "python_mapping_rows_v1"),
    }
    admissions = {fmt: external_adapter_admission_report(rows) for fmt, rows in parsed.items()}
    return {
        "status": W_EXTERNAL_INGESTION_DRYRUN_STATUS,
        "upstream_status": W_EXTERNAL_SOURCE_ADAPTER_STATUS,
        "ingestion_version": INGESTION_DRYRUN_VERSION,
        "ingestion_mode": INGESTION_MODE,
        "synthetic_fixtures_only": SYNTHETIC_FIXTURES_ONLY,
        "parser_formats_tested": PARSER_FORMATS_TESTED,
        "component_order": FINITE_PART_COMPONENT_ORDER,
        "admissions": admissions,
        "real_external_payload_rows_supplied": REAL_EXTERNAL_PAYLOAD_ROWS_SUPPLIED,
        "real_external_payload_rows_admitted": REAL_EXTERNAL_PAYLOAD_ROWS_ADMITTED,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
    }


def _all_admitted(report: Mapping[str, Any]) -> bool:
    return all(v["table_shape_ok"] and v["all_rows_admitted"] for v in report["admissions"].values())


def check_T_w_external_ingestion_dryrun_status_declared():
    p = W_EXTERNAL_INGESTION_DRYRUN_STATUS == "P_w_external_ingestion_dryrun" and INGESTION_DRYRUN_DECLARED
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_EXTERNAL_INGESTION_DRYRUN_STATUS}


def check_T_w_external_ingestion_dryrun_depends_on_v100_adapter():
    d = _check_v100()
    p = _passed(d) and W_EXTERNAL_SOURCE_ADAPTER_STATUS == "P_w_external_source_adapter"
    return {"passed": p, "status": "PASS" if p else "FAIL", "upstream": d.get("status")}


def check_T_w_external_ingestion_dryrun_formats_match_adapter():
    p = set(PARSER_FORMATS_TESTED) == set(SUPPORTED_EXTERNAL_FORMATS)
    return {"passed": p, "status": "PASS" if p else "FAIL", "formats": PARSER_FORMATS_TESTED}


def check_T_w_external_ingestion_dryrun_record_schema_preserved():
    rows = synthetic_shape_rows()
    p = all(set(asdict(r).keys()) == set(RECORD_FIELDS) for r in rows) and len(RECORD_FIELDS) == len(set(RECORD_FIELDS))
    return {"passed": p, "status": "PASS" if p else "FAIL", "field_count": len(RECORD_FIELDS)}


def check_T_w_external_ingestion_json_parser_roundtrip():
    rows = parse_json_rows_v1(synthetic_json_payload())
    report = external_adapter_admission_report(rows)
    p = len(rows) == len(FINITE_PART_COMPONENT_ORDER) and report["all_rows_admitted"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_external_ingestion_csv_parser_roundtrip():
    rows = parse_csv_with_header_v1(synthetic_csv_payload())
    report = external_adapter_admission_report(rows)
    p = len(rows) == len(FINITE_PART_COMPONENT_ORDER) and report["all_rows_admitted"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_external_ingestion_mapping_parser_roundtrip():
    rows = parse_python_mapping_rows_v1(synthetic_python_mapping_payload())
    report = external_adapter_admission_report(rows)
    p = len(rows) == len(FINITE_PART_COMPONENT_ORDER) and report["all_rows_admitted"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_external_ingestion_parser_outputs_external_records():
    rows = parse_external_payload(synthetic_json_payload(), "json_rows_v1")
    p = all(isinstance(r, ExternalSourceRecord) for r in rows)
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_external_ingestion_component_order_preserved_all_formats():
    report = ingestion_dryrun_report()
    p = all(tuple(r.component_id for r in parse_external_payload(
        synthetic_json_payload() if fmt == "json_rows_v1" else synthetic_csv_payload() if fmt == "csv_with_header_v1" else synthetic_python_mapping_payload(), fmt
    )) == FINITE_PART_COMPONENT_ORDER for fmt in PARSER_FORMATS_TESTED)
    return {"passed": p, "status": "PASS" if p else "FAIL", "component_order": report["component_order"]}


def check_T_w_external_ingestion_symbols_preserved_all_formats():
    parsed = [
        parse_external_payload(synthetic_json_payload(), "json_rows_v1"),
        parse_external_payload(synthetic_csv_payload(), "csv_with_header_v1"),
        parse_external_payload(synthetic_python_mapping_payload(), "python_mapping_rows_v1"),
    ]
    p = all(all(r.symbol == COMPONENT_SYMBOLS[r.component_id] for r in rows) for rows in parsed)
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_external_ingestion_rejects_unknown_format():
    try:
        parse_external_payload("{}", "xlsx_unknown_v0")
    except ValueError:
        return {"passed": True, "status": "PASS"}
    return {"passed": False, "status": "FAIL"}


def check_T_w_external_ingestion_rejects_bad_json_version():
    payload = json.dumps({"adapter_version": "wrong", "rows": []})
    try:
        parse_json_rows_v1(payload)
    except ValueError:
        return {"passed": True, "status": "PASS"}
    return {"passed": False, "status": "FAIL"}


def check_T_w_external_ingestion_rejects_bad_csv_header():
    bad = "component_id,symbol\nDelta_alpha_run,da\n"
    try:
        parse_csv_with_header_v1(bad)
    except ValueError:
        return {"passed": True, "status": "PASS"}
    return {"passed": False, "status": "FAIL"}


def check_T_w_external_ingestion_rejects_missing_component_after_parse():
    rows = list(synthetic_python_mapping_payload())[:-1]
    parsed = parse_python_mapping_rows_v1(rows)
    report = external_adapter_admission_report(parsed)
    p = not report["table_shape_ok"] and FINITE_PART_COMPONENT_ORDER[-1] in report["missing_ids"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_external_ingestion_rejects_duplicate_component_after_parse():
    rows = list(synthetic_python_mapping_payload())
    rows[1] = {**rows[1], "component_id": rows[0]["component_id"], "symbol": rows[0]["symbol"]}
    report = external_adapter_admission_report(parse_python_mapping_rows_v1(rows))
    p = not report["table_shape_ok"] and rows[0]["component_id"] in report["duplicate_ids"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_external_ingestion_rejects_apf_anchor_column_after_parse():
    rows = list(synthetic_python_mapping_payload())
    rows[0] = {**rows[0], "target_observables_consumed": ("apf_anchor_delta_r_column",)}
    report = external_adapter_admission_report(parse_python_mapping_rows_v1(rows))
    p = not report["all_rows_admitted"] and report["row_results"][0] is False
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_external_ingestion_rejects_observed_W_column_after_parse():
    rows = list(synthetic_python_mapping_payload())
    rows[0] = {**rows[0], "target_observables_consumed": ("observed_M_W_column",)}
    report = external_adapter_admission_report(parse_python_mapping_rows_v1(rows))
    p = not report["all_rows_admitted"] and report["row_results"][0] is False
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_external_ingestion_rejects_fit_residual_column_after_parse():
    rows = list(synthetic_python_mapping_payload())
    rows[0] = {**rows[0], "target_observables_consumed": ("fit_residual_column",)}
    report = external_adapter_admission_report(parse_python_mapping_rows_v1(rows))
    p = not report["all_rows_admitted"] and report["row_results"][0] is False
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_external_ingestion_forbidden_inputs_reused_from_adapter():
    p = {"observed_M_W_column", "apf_anchor_delta_r_column", "fit_residual_column"}.issubset(set(FORBIDDEN_EXTERNAL_ADAPTER_INPUTS))
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_external_ingestion_synthetic_only_flag_blocks_real_rows():
    p = SYNTHETIC_FIXTURES_ONLY and not REAL_EXTERNAL_PAYLOAD_ROWS_SUPPLIED and not REAL_EXTERNAL_PAYLOAD_ROWS_ADMITTED
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_external_ingestion_no_component_sum_certified():
    p = not COMPONENT_SUM_CERTIFIED and not PHYSICAL_W_TRANSPORT_CLOSED
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_external_ingestion_completion_gate_remains_locked():
    d = _check_completion()
    p = _passed(d) and not EXPORTS_PHYSICAL_M_W and not EXPORTS_PHYSICAL_SCHEME_MASSES
    return {"passed": p, "status": "PASS" if p else "FAIL", "completion_gate": d.get("status")}


def check_T_w_external_ingestion_dryrun_report_shape():
    report = ingestion_dryrun_report()
    p = report["status"] == W_EXTERNAL_INGESTION_DRYRUN_STATUS and set(report["admissions"].keys()) == set(PARSER_FORMATS_TESTED)
    return {"passed": p, "status": "PASS" if p else "FAIL", "report_keys": tuple(sorted(report.keys()))}


def check_T_w_external_ingestion_all_synthetic_formats_admit_shape_rows():
    report = ingestion_dryrun_report()
    p = _all_admitted(report)
    return {"passed": p, "status": "PASS" if p else "FAIL", "admissions": report["admissions"]}


def check_T_w_external_ingestion_dryrun_bank_closure():
    deps = [
        check_T_w_external_ingestion_dryrun_status_declared(),
        check_T_w_external_ingestion_dryrun_depends_on_v100_adapter(),
        check_T_w_external_ingestion_dryrun_formats_match_adapter(),
        check_T_w_external_ingestion_all_synthetic_formats_admit_shape_rows(),
        check_T_w_external_ingestion_completion_gate_remains_locked(),
    ]
    p = all(_passed(d) for d in deps) and not REAL_EXTERNAL_PAYLOAD_ROWS_ADMITTED and not PHYSICAL_W_TRANSPORT_CLOSED
    return {
        "passed": p,
        "status": "PASS" if p else "FAIL",
        "tier": 4,
        "epistemic": W_EXTERNAL_INGESTION_DRYRUN_STATUS,
        "dependencies": [str(d.get("status")) for d in deps],
        "manifest": ingestion_dryrun_report(),
        "closed_now": "external payload parser fixtures/dry-run ingestion for JSON/CSV/Python mappings",
        "not_closed": "real external finite-part payload rows, component-sum certificate, covariance/uncertainty propagation, physical W export",
    }


_CHECKS: Dict[str, Any] = {
    "T_w_external_ingestion_dryrun_status_declared": check_T_w_external_ingestion_dryrun_status_declared,
    "T_w_external_ingestion_dryrun_depends_on_v100_adapter": check_T_w_external_ingestion_dryrun_depends_on_v100_adapter,
    "T_w_external_ingestion_dryrun_formats_match_adapter": check_T_w_external_ingestion_dryrun_formats_match_adapter,
    "T_w_external_ingestion_dryrun_record_schema_preserved": check_T_w_external_ingestion_dryrun_record_schema_preserved,
    "T_w_external_ingestion_json_parser_roundtrip": check_T_w_external_ingestion_json_parser_roundtrip,
    "T_w_external_ingestion_csv_parser_roundtrip": check_T_w_external_ingestion_csv_parser_roundtrip,
    "T_w_external_ingestion_mapping_parser_roundtrip": check_T_w_external_ingestion_mapping_parser_roundtrip,
    "T_w_external_ingestion_parser_outputs_external_records": check_T_w_external_ingestion_parser_outputs_external_records,
    "T_w_external_ingestion_component_order_preserved_all_formats": check_T_w_external_ingestion_component_order_preserved_all_formats,
    "T_w_external_ingestion_symbols_preserved_all_formats": check_T_w_external_ingestion_symbols_preserved_all_formats,
    "T_w_external_ingestion_rejects_unknown_format": check_T_w_external_ingestion_rejects_unknown_format,
    "T_w_external_ingestion_rejects_bad_json_version": check_T_w_external_ingestion_rejects_bad_json_version,
    "T_w_external_ingestion_rejects_bad_csv_header": check_T_w_external_ingestion_rejects_bad_csv_header,
    "T_w_external_ingestion_rejects_missing_component_after_parse": check_T_w_external_ingestion_rejects_missing_component_after_parse,
    "T_w_external_ingestion_rejects_duplicate_component_after_parse": check_T_w_external_ingestion_rejects_duplicate_component_after_parse,
    "T_w_external_ingestion_rejects_apf_anchor_column_after_parse": check_T_w_external_ingestion_rejects_apf_anchor_column_after_parse,
    "T_w_external_ingestion_rejects_observed_W_column_after_parse": check_T_w_external_ingestion_rejects_observed_W_column_after_parse,
    "T_w_external_ingestion_rejects_fit_residual_column_after_parse": check_T_w_external_ingestion_rejects_fit_residual_column_after_parse,
    "T_w_external_ingestion_forbidden_inputs_reused_from_adapter": check_T_w_external_ingestion_forbidden_inputs_reused_from_adapter,
    "T_w_external_ingestion_synthetic_only_flag_blocks_real_rows": check_T_w_external_ingestion_synthetic_only_flag_blocks_real_rows,
    "T_w_external_ingestion_no_component_sum_certified": check_T_w_external_ingestion_no_component_sum_certified,
    "T_w_external_ingestion_completion_gate_remains_locked": check_T_w_external_ingestion_completion_gate_remains_locked,
    "T_w_external_ingestion_dryrun_report_shape": check_T_w_external_ingestion_dryrun_report_shape,
    "T_w_external_ingestion_all_synthetic_formats_admit_shape_rows": check_T_w_external_ingestion_all_synthetic_formats_admit_shape_rows,
    "T_w_external_ingestion_dryrun_bank_closure": check_T_w_external_ingestion_dryrun_bank_closure,
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
    return {"passed": ok, "status": "W_TRACE_EXTERNAL_INGESTION_DRYRUN_BANK_PASS" if ok else "W_TRACE_EXTERNAL_INGESTION_DRYRUN_BANK_FAIL", "checks": rows, "manifest": ingestion_dryrun_report()}


if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
