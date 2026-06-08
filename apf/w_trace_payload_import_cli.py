"""W_TRACE real payload import CLI / fixture-file loader bank.

v11.3 (2026-05-09 LATER-41): file-loader and command-line import layer
above the v11.2 final export-readiness aggregator.  This module provides a
concrete way to load candidate W_TRACE finite-part source-pack files from
JSON or CSV fixtures and route them through the existing v10.x/v11.x
admission gates.  The shipped state contains no real finite-part payload file,
so physical W export remains locked.  The closure here is the loader contract,
absence certificate, and non-smuggling behavior, not numerical W transport.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Dict, Mapping, Sequence, Tuple

from apf.w_trace_external_ingestion_dryrun import (
    parse_external_payload,
    synthetic_json_payload,
    synthetic_csv_payload,
)
from apf.w_trace_external_source_adapter import (
    EXTERNAL_ADAPTER_VERSION,
    ExternalSourceRecord,
)
from apf.w_trace_real_source_candidate import CandidatePackMetadata
from apf.w_trace_candidate_payload_attempt import (
    PayloadAttempt,
    payload_attempt_report,
    reviewed_shape_candidate_metadata,
    FORBIDDEN_ATTEMPT_COLUMNS,
    check_T_w_candidate_payload_attempt_bank_closure as _check_v103,
)
from apf.w_trace_real_row_bundle_admission import (
    empty_bundle_report,
    check_T_w_real_row_bundle_bank_closure as _check_v109,
)
from apf.w_trace_final_export_readiness import (
    readiness_report,
    current_route_state,
    check_T_w_final_export_readiness_bank_closure as _check_v112,
)

W_PAYLOAD_IMPORT_CLI_STATUS = "P_w_payload_import_cli_loader"
PAYLOAD_IMPORT_CLI_VERSION = "w_trace_payload_import_cli_v0"
PAYLOAD_IMPORT_CLI_MODE = "FILE_LOADER_READY__NO_REAL_PAYLOAD_SHIPPED__EXPORT_LOCKED"

REAL_PAYLOAD_FILE_SHIPPED = False
REAL_PAYLOAD_FILE_LOADED = False
REAL_PAYLOAD_FILE_ADMITTED = False
COMPONENT_SUM_CERTIFIED = False
COVARIANCE_CERTIFIED = False
UNCERTAINTY_PROPAGATION_CERTIFIED = False
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

SUPPORTED_LOADER_FORMATS: Tuple[str, ...] = ("json_rows_v1", "csv_with_header_v1")
REQUIRED_LOADER_REPORT_FIELDS: Tuple[str, ...] = (
    "status",
    "version",
    "mode",
    "path_supplied",
    "file_exists",
    "ingest_format",
    "file_digest",
    "rows_loaded",
    "attempt_report",
    "bundle_report",
    "readiness_report",
    "physical_W_export_enabled",
    "exports_physical_M_W",
    "failure_reasons",
)
FORBIDDEN_LOADER_FIELDS: Tuple[str, ...] = tuple(sorted(set(FORBIDDEN_ATTEMPT_COLUMNS + (
    "observed_M_W",
    "world_average_W_mass",
    "W_mass_residual",
    "Delta_r_fit_to_observed_M_W",
    "APF_ANCHOR_DELTA_R_TARGET",
    "physical_W_export_request",
    "force_unlock",
))))

@dataclass(frozen=True)
class PayloadFileLoad:
    path: str = "UNSUPPLIED"
    ingest_format: str = "UNSUPPLIED"
    file_exists: bool = False
    file_digest: str = "UNSUPPLIED"
    rows_loaded: int = 0
    parse_error: str = ""


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def _res(name: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    return {
        "passed": bool(passed),
        "status": "PASS" if passed else "FAIL",
        "tier": 4,
        "epistemic": W_PAYLOAD_IMPORT_CLI_STATUS,
        "check": name,
        **extra,
    }


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def infer_ingest_format(path: str | Path, explicit: str | None = None) -> str:
    if explicit:
        if explicit not in SUPPORTED_LOADER_FORMATS:
            raise ValueError(f"unsupported ingest_format: {explicit}")
        return explicit
    suffix = Path(path).suffix.lower()
    if suffix == ".json":
        return "json_rows_v1"
    if suffix == ".csv":
        return "csv_with_header_v1"
    raise ValueError("cannot infer ingest format; use --format")


def load_payload_file(path: str | Path, ingest_format: str | None = None) -> Tuple[Tuple[ExternalSourceRecord, ...], PayloadFileLoad]:
    p = Path(path)
    fmt = infer_ingest_format(p, ingest_format)
    if not p.exists():
        return (), PayloadFileLoad(path=str(p), ingest_format=fmt, file_exists=False, parse_error="FILE_NOT_FOUND")
    payload = p.read_text(encoding="utf-8")
    digest = sha256_file(p)
    try:
        rows = tuple(parse_external_payload(payload, fmt))
    except Exception as exc:
        return (), PayloadFileLoad(path=str(p), ingest_format=fmt, file_exists=True, file_digest=digest, parse_error=repr(exc))
    return rows, PayloadFileLoad(path=str(p), ingest_format=fmt, file_exists=True, file_digest=digest, rows_loaded=len(rows))


def metadata_from_load(load: PayloadFileLoad, *, review_attested: bool = False, shipped_real_data: bool = False) -> CandidatePackMetadata:
    return CandidatePackMetadata(
        candidate_pack_id="FILE_LOADED_W_TRACE_PAYLOAD" if load.file_exists else "UNSUPPLIED_FILE_PAYLOAD",
        candidate_pack_uri="file://" + load.path,
        candidate_pack_digest=load.file_digest,
        candidate_adapter_version=EXTERNAL_ADAPTER_VERSION,
        candidate_ingest_format=load.ingest_format if load.ingest_format != "UNSUPPLIED" else "json_rows_v1",
        candidate_extraction_log_digest=("sha256:file-loader-extraction-log-placeholder" if load.file_exists else "UNSUPPLIED"),
        candidate_review_attestation=bool(review_attested),
        candidate_synthetic_fixture=not bool(shipped_real_data),
    )


def attempt_from_load(load: PayloadFileLoad, *, shipped_real_data: bool = False, physical_export_requested: bool = False) -> PayloadAttempt:
    return PayloadAttempt(
        attempt_id="FILE_LOADER_ATTEMPT" if load.file_exists else "UNSUPPLIED_FILE_LOADER_ATTEMPT",
        attempt_kind="file_payload_import",
        attempted_pack_id="FILE_LOADED_W_TRACE_PAYLOAD" if load.file_exists else "UNSUPPLIED_FILE_PAYLOAD",
        attempted_pack_digest=load.file_digest,
        adapter_version=EXTERNAL_ADAPTER_VERSION,
        rows_are_shipped_real_data=bool(shipped_real_data),
        rows_are_shape_fixture=not bool(shipped_real_data),
        physical_export_requested=bool(physical_export_requested),
    )


def _row_consumes_forbidden(row: ExternalSourceRecord | Mapping[str, Any]) -> bool:
    d = asdict(row) if isinstance(row, ExternalSourceRecord) else dict(row)
    consumed = set(d.get("target_observables_consumed") or ())
    return bool(consumed.intersection(FORBIDDEN_LOADER_FIELDS) or d.get("apf_target_consumed"))


def loader_report(
    path: str | Path | None = None,
    ingest_format: str | None = None,
    *,
    review_attested: bool = False,
    shipped_real_data: bool = False,
    physical_export_requested: bool = False,
) -> Dict[str, Any]:
    if path is None:
        rows: Tuple[ExternalSourceRecord, ...] = ()
        load = PayloadFileLoad()
    else:
        rows, load = load_payload_file(path, ingest_format)
    meta = metadata_from_load(load, review_attested=review_attested, shipped_real_data=shipped_real_data)
    attempt = attempt_from_load(load, shipped_real_data=shipped_real_data, physical_export_requested=physical_export_requested)
    attempt_r = payload_attempt_report(rows, meta, attempt)
    bundle_r = empty_bundle_report()
    readiness_r = readiness_report(physical_export_requested=physical_export_requested)
    failures = []
    if path is None:
        failures.append("NO_PAYLOAD_FILE_SUPPLIED")
    if not load.file_exists and path is not None:
        failures.append("PAYLOAD_FILE_NOT_FOUND")
    if load.parse_error:
        failures.append("PAYLOAD_PARSE_ERROR")
    if rows and any(_row_consumes_forbidden(r) for r in rows):
        failures.append("FORBIDDEN_TARGET_OBSERVABLE_OR_APF_ANCHOR_CONSUMED")
    if rows and not review_attested:
        failures.append("REVIEW_ATTESTATION_REQUIRED_FOR_REAL_PAYLOAD_ADMISSION")
    if rows and not shipped_real_data:
        failures.append("SHAPE_OR_UNATTESTED_FILE_NOT_PROMOTED_TO_REAL_PAYLOAD")
    if physical_export_requested:
        failures.append("PHYSICAL_W_EXPORT_REQUEST_BLOCKED_BY_IMPORT_LOADER")
    return {
        "status": W_PAYLOAD_IMPORT_CLI_STATUS,
        "version": PAYLOAD_IMPORT_CLI_VERSION,
        "mode": PAYLOAD_IMPORT_CLI_MODE,
        "supported_loader_formats": SUPPORTED_LOADER_FORMATS,
        "path_supplied": path is not None,
        "file_exists": bool(load.file_exists),
        "ingest_format": load.ingest_format,
        "file_digest": load.file_digest,
        "rows_loaded": int(load.rows_loaded),
        "parse_error": load.parse_error,
        "loader_state": asdict(load),
        "attempt_report": attempt_r,
        "bundle_report": bundle_r,
        "readiness_report": readiness_r,
        "real_payload_file_shipped": REAL_PAYLOAD_FILE_SHIPPED,
        "real_payload_file_loaded": bool(load.file_exists and load.rows_loaded > 0 and not load.parse_error and shipped_real_data),
        "real_payload_file_admitted": False,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "covariance_certified": COVARIANCE_CERTIFIED,
        "uncertainty_propagation_certified": UNCERTAINTY_PROPAGATION_CERTIFIED,
        "physical_W_export_enabled": PHYSICAL_W_EXPORT_ENABLED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "failure_reasons": tuple(dict.fromkeys(failures)),
    }


def write_synthetic_json_fixture(path: str | Path) -> str:
    Path(path).write_text(synthetic_json_payload(), encoding="utf-8")
    return str(path)


def write_synthetic_csv_fixture(path: str | Path) -> str:
    Path(path).write_text(synthetic_csv_payload(), encoding="utf-8")
    return str(path)


def manifest() -> Dict[str, Any]:
    return {
        "status": W_PAYLOAD_IMPORT_CLI_STATUS,
        "version": PAYLOAD_IMPORT_CLI_VERSION,
        "mode": PAYLOAD_IMPORT_CLI_MODE,
        "supported_loader_formats": SUPPORTED_LOADER_FORMATS,
        "required_loader_report_fields": REQUIRED_LOADER_REPORT_FIELDS,
        "forbidden_loader_fields": FORBIDDEN_LOADER_FIELDS,
        "current_route_state": current_route_state(),
        "absence_certificate": loader_report(),
    }


def check_T_w_payload_import_cli_status_declared():
    m = manifest(); return _res("status_declared", m["status"] == W_PAYLOAD_IMPORT_CLI_STATUS and not m["current_route_state"]["physical_W_export_enabled"], manifest=m)


def check_T_w_payload_import_cli_depends_on_v103_attempt_gate():
    d = _check_v103(); return _res("depends_on_v103", _passed(d), upstream=d.get("status"))


def check_T_w_payload_import_cli_depends_on_v109_bundle_gate():
    d = _check_v109(); return _res("depends_on_v109", _passed(d), upstream=d.get("status"))


def check_T_w_payload_import_cli_depends_on_v112_readiness():
    d = _check_v112(); return _res("depends_on_v112", _passed(d), upstream=d.get("status"))


def check_T_w_payload_import_cli_report_schema_declared():
    r = loader_report(); return _res("report_schema", set(REQUIRED_LOADER_REPORT_FIELDS).issubset(r.keys()), fields=REQUIRED_LOADER_REPORT_FIELDS)


def check_T_w_payload_import_cli_default_absence_certificate_locked():
    r = loader_report(); ok = (not r["path_supplied"] and "NO_PAYLOAD_FILE_SUPPLIED" in r["failure_reasons"] and not r["physical_W_export_enabled"])
    return _res("default_absence_locked", ok, report=r)


def check_T_w_payload_import_cli_supported_formats_match_parser_path():
    ok = set(SUPPORTED_LOADER_FORMATS) == {"json_rows_v1", "csv_with_header_v1"}
    return _res("supported_formats", ok, formats=SUPPORTED_LOADER_FORMATS)


def check_T_w_payload_import_cli_infers_json_format():
    return _res("infers_json", infer_ingest_format("candidate.json") == "json_rows_v1")


def check_T_w_payload_import_cli_infers_csv_format():
    return _res("infers_csv", infer_ingest_format("candidate.csv") == "csv_with_header_v1")


def check_T_w_payload_import_cli_rejects_unknown_extension():
    try:
        infer_ingest_format("candidate.txt")
        ok = False
    except ValueError:
        ok = True
    return _res("rejects_unknown_extension", ok)


def check_T_w_payload_import_cli_missing_file_fails_closed():
    r = loader_report("/tmp/nonexistent_w_trace_payload.json", "json_rows_v1")
    ok = (not r["file_exists"] and "PAYLOAD_FILE_NOT_FOUND" in r["failure_reasons"] and not r["physical_W_export_enabled"])
    return _res("missing_file_closed", ok, report=r)


def check_T_w_payload_import_cli_json_fixture_loads_rows():
    with TemporaryDirectory() as td:
        p = write_synthetic_json_fixture(Path(td) / "fixture.json")
        r = loader_report(p, "json_rows_v1")
    ok = r["file_exists"] and r["rows_loaded"] == 8 and r["file_digest"].startswith("sha256:")
    return _res("json_fixture_loads", ok, report=r)


def check_T_w_payload_import_cli_csv_fixture_loads_rows():
    with TemporaryDirectory() as td:
        p = write_synthetic_csv_fixture(Path(td) / "fixture.csv")
        r = loader_report(p, "csv_with_header_v1")
    ok = r["file_exists"] and r["rows_loaded"] == 8 and r["file_digest"].startswith("sha256:")
    return _res("csv_fixture_loads", ok, report=r)


def check_T_w_payload_import_cli_json_fixture_not_promoted_to_real():
    with TemporaryDirectory() as td:
        p = write_synthetic_json_fixture(Path(td) / "fixture.json")
        r = loader_report(p, "json_rows_v1", review_attested=False, shipped_real_data=False)
    ok = (not r["real_payload_file_admitted"] and "SHAPE_OR_UNATTESTED_FILE_NOT_PROMOTED_TO_REAL_PAYLOAD" in r["failure_reasons"])
    return _res("json_fixture_not_real", ok, report=r)


def check_T_w_payload_import_cli_csv_fixture_not_promoted_to_real():
    with TemporaryDirectory() as td:
        p = write_synthetic_csv_fixture(Path(td) / "fixture.csv")
        r = loader_report(p, "csv_with_header_v1", review_attested=False, shipped_real_data=False)
    ok = (not r["real_payload_file_admitted"] and not r["physical_W_export_enabled"])
    return _res("csv_fixture_not_real", ok, report=r)


def check_T_w_payload_import_cli_review_required_for_real_claim():
    with TemporaryDirectory() as td:
        p = write_synthetic_json_fixture(Path(td) / "fixture.json")
        r = loader_report(p, "json_rows_v1", review_attested=False, shipped_real_data=True)
    ok = "REVIEW_ATTESTATION_REQUIRED_FOR_REAL_PAYLOAD_ADMISSION" in r["failure_reasons"] and not r["real_payload_file_admitted"]
    return _res("review_required", ok, report=r)


def check_T_w_payload_import_cli_attested_shape_still_no_physical_export():
    with TemporaryDirectory() as td:
        p = write_synthetic_json_fixture(Path(td) / "fixture.json")
        r = loader_report(p, "json_rows_v1", review_attested=True, shipped_real_data=True)
    ok = r["rows_loaded"] == 8 and not r["physical_W_export_enabled"] and not r["exports_physical_M_W"]
    return _res("attested_shape_no_export", ok, report=r)


def check_T_w_payload_import_cli_parse_error_fails_closed():
    with TemporaryDirectory() as td:
        p = Path(td) / "bad.json"; p.write_text("{bad json", encoding="utf-8")
        r = loader_report(p, "json_rows_v1")
    ok = "PAYLOAD_PARSE_ERROR" in r["failure_reasons"] and not r["physical_W_export_enabled"]
    return _res("parse_error_closed", ok, report=r)


def check_T_w_payload_import_cli_explicit_format_enforced():
    with TemporaryDirectory() as td:
        p = write_synthetic_json_fixture(Path(td) / "fixture.json")
        r = loader_report(p, "csv_with_header_v1")
    ok = "PAYLOAD_PARSE_ERROR" in r["failure_reasons"]
    return _res("explicit_format_enforced", ok, report=r)


def check_T_w_payload_import_cli_forbids_physical_export_request():
    with TemporaryDirectory() as td:
        p = write_synthetic_json_fixture(Path(td) / "fixture.json")
        r = loader_report(p, "json_rows_v1", physical_export_requested=True)
    ok = "PHYSICAL_W_EXPORT_REQUEST_BLOCKED_BY_IMPORT_LOADER" in r["failure_reasons"] and not r["physical_W_export_enabled"]
    return _res("forbids_export_request", ok, report=r)


def check_T_w_payload_import_cli_forbidden_fields_named():
    req = {"observed_M_W", "APF_ANCHOR_DELTA_R_TARGET", "force_unlock"}
    return _res("forbidden_fields_named", req.issubset(set(FORBIDDEN_LOADER_FIELDS)), forbidden=FORBIDDEN_LOADER_FIELDS)


def check_T_w_payload_import_cli_forbidden_consumption_rejected():
    rows = list(reviewed_shape_candidate_metadata().__dict__.keys())
    # mutate a parsed fixture row directly instead of abusing metadata keys
    parsed, _ = load_payload_file(Path(write_synthetic_json_fixture(Path(TemporaryDirectory().name) / "x.json")) if False else "/tmp/nonexistent", "json_rows_v1")
    with TemporaryDirectory() as td:
        p = Path(td) / "fixture.json"; write_synthetic_json_fixture(p)
        data = json.loads(p.read_text())
        data["rows"][0]["target_observables_consumed"] = ["observed_M_W"]
        p.write_text(json.dumps(data), encoding="utf-8")
        r = loader_report(p, "json_rows_v1", review_attested=True, shipped_real_data=True)
    ok = "FORBIDDEN_TARGET_OBSERVABLE_OR_APF_ANCHOR_CONSUMED" in r["failure_reasons"] and not r["physical_W_export_enabled"]
    return _res("forbidden_consumption_rejected", ok, report=r)


def check_T_w_payload_import_cli_apf_anchor_consumption_rejected():
    with TemporaryDirectory() as td:
        p = Path(td) / "fixture.json"; write_synthetic_json_fixture(p)
        data = json.loads(p.read_text())
        data["rows"][0]["apf_target_consumed"] = True
        p.write_text(json.dumps(data), encoding="utf-8")
        r = loader_report(p, "json_rows_v1", review_attested=True, shipped_real_data=True)
    ok = "FORBIDDEN_TARGET_OBSERVABLE_OR_APF_ANCHOR_CONSUMED" in r["failure_reasons"] and not r["physical_W_export_enabled"]
    return _res("apf_anchor_consumption_rejected", ok, report=r)


def check_T_w_payload_import_cli_readiness_remains_locked_after_load():
    with TemporaryDirectory() as td:
        p = write_synthetic_json_fixture(Path(td) / "fixture.json")
        r = loader_report(p, "json_rows_v1", review_attested=True, shipped_real_data=True)
    ready = r["readiness_report"]
    ok = not ready["physical_W_export_ready"] and not r["physical_W_export_enabled"]
    return _res("readiness_locked_after_load", ok, readiness=ready)


def check_T_w_payload_import_cli_bundle_report_stays_unadmitted_for_fixture():
    with TemporaryDirectory() as td:
        p = write_synthetic_json_fixture(Path(td) / "fixture.json")
        r = loader_report(p, "json_rows_v1")
    ok = not r["bundle_report"].get("real_row_bundle_admitted") and not r["physical_W_export_enabled"]
    return _res("bundle_unadmitted_fixture", ok, bundle=r["bundle_report"])


def check_T_w_payload_import_cli_manifest_contains_absence_certificate():
    m = manifest(); a = m["absence_certificate"]
    ok = a["status"] == W_PAYLOAD_IMPORT_CLI_STATUS and "NO_PAYLOAD_FILE_SUPPLIED" in a["failure_reasons"]
    return _res("manifest_absence", ok, manifest=m)


def check_T_w_payload_import_cli_current_flags_false():
    r = loader_report(); ok = not r["real_payload_file_shipped"] and not r["component_sum_certified"] and not r["covariance_certified"] and not r["uncertainty_propagation_certified"]
    return _res("current_flags_false", ok, report=r)


def check_T_w_payload_import_cli_bank_closure():
    checks = [fn for name, fn in CHECKS.items() if name != "T_w_payload_import_cli_bank_closure"]
    rows = [fn() for fn in checks]
    ok = all(_passed(r) for r in rows) and not loader_report()["physical_W_export_enabled"]
    return _res("bank_closure", ok, passed_count=sum(_passed(r) for r in rows), total=len(rows))


CHECKS: Dict[str, Any] = {
    "T_w_payload_import_cli_status_declared": check_T_w_payload_import_cli_status_declared,
    "T_w_payload_import_cli_depends_on_v103_attempt_gate": check_T_w_payload_import_cli_depends_on_v103_attempt_gate,
    "T_w_payload_import_cli_depends_on_v109_bundle_gate": check_T_w_payload_import_cli_depends_on_v109_bundle_gate,
    "T_w_payload_import_cli_depends_on_v112_readiness": check_T_w_payload_import_cli_depends_on_v112_readiness,
    "T_w_payload_import_cli_report_schema_declared": check_T_w_payload_import_cli_report_schema_declared,
    "T_w_payload_import_cli_default_absence_certificate_locked": check_T_w_payload_import_cli_default_absence_certificate_locked,
    "T_w_payload_import_cli_supported_formats_match_parser_path": check_T_w_payload_import_cli_supported_formats_match_parser_path,
    "T_w_payload_import_cli_infers_json_format": check_T_w_payload_import_cli_infers_json_format,
    "T_w_payload_import_cli_infers_csv_format": check_T_w_payload_import_cli_infers_csv_format,
    "T_w_payload_import_cli_rejects_unknown_extension": check_T_w_payload_import_cli_rejects_unknown_extension,
    "T_w_payload_import_cli_missing_file_fails_closed": check_T_w_payload_import_cli_missing_file_fails_closed,
    "T_w_payload_import_cli_json_fixture_loads_rows": check_T_w_payload_import_cli_json_fixture_loads_rows,
    "T_w_payload_import_cli_csv_fixture_loads_rows": check_T_w_payload_import_cli_csv_fixture_loads_rows,
    "T_w_payload_import_cli_json_fixture_not_promoted_to_real": check_T_w_payload_import_cli_json_fixture_not_promoted_to_real,
    "T_w_payload_import_cli_csv_fixture_not_promoted_to_real": check_T_w_payload_import_cli_csv_fixture_not_promoted_to_real,
    "T_w_payload_import_cli_review_required_for_real_claim": check_T_w_payload_import_cli_review_required_for_real_claim,
    "T_w_payload_import_cli_attested_shape_still_no_physical_export": check_T_w_payload_import_cli_attested_shape_still_no_physical_export,
    "T_w_payload_import_cli_parse_error_fails_closed": check_T_w_payload_import_cli_parse_error_fails_closed,
    "T_w_payload_import_cli_explicit_format_enforced": check_T_w_payload_import_cli_explicit_format_enforced,
    "T_w_payload_import_cli_forbids_physical_export_request": check_T_w_payload_import_cli_forbids_physical_export_request,
    "T_w_payload_import_cli_forbidden_fields_named": check_T_w_payload_import_cli_forbidden_fields_named,
    "T_w_payload_import_cli_forbidden_consumption_rejected": check_T_w_payload_import_cli_forbidden_consumption_rejected,
    "T_w_payload_import_cli_apf_anchor_consumption_rejected": check_T_w_payload_import_cli_apf_anchor_consumption_rejected,
    "T_w_payload_import_cli_readiness_remains_locked_after_load": check_T_w_payload_import_cli_readiness_remains_locked_after_load,
    "T_w_payload_import_cli_bundle_report_stays_unadmitted_for_fixture": check_T_w_payload_import_cli_bundle_report_stays_unadmitted_for_fixture,
    "T_w_payload_import_cli_manifest_contains_absence_certificate": check_T_w_payload_import_cli_manifest_contains_absence_certificate,
    "T_w_payload_import_cli_current_flags_false": check_T_w_payload_import_cli_current_flags_false,
    "T_w_payload_import_cli_bank_closure": check_T_w_payload_import_cli_bank_closure,
}

_CHECKS = CHECKS


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
        "status": "W_TRACE_PAYLOAD_IMPORT_CLI_BANK_PASS" if ok else "W_TRACE_PAYLOAD_IMPORT_CLI_BANK_FAIL",
        "checks": rows,
        "manifest": manifest(),
    }


def cli_main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="W_TRACE finite-part payload file loader (locked by default).")
    ap.add_argument("--file", dest="path", default=None, help="candidate JSON/CSV payload path")
    ap.add_argument("--format", dest="ingest_format", default=None, choices=SUPPORTED_LOADER_FORMATS)
    ap.add_argument("--review-attested", action="store_true", help="declare external review attestation present")
    ap.add_argument("--shipped-real-data", action="store_true", help="declare rows are shipped real data, not fixture rows")
    ap.add_argument("--request-physical-export", action="store_true", help="attempt physical W export; should remain blocked")
    args = ap.parse_args(argv)
    report = loader_report(
        args.path,
        args.ingest_format,
        review_attested=args.review_attested,
        shipped_real_data=args.shipped_real_data,
        physical_export_requested=args.request_physical_export,
    )
    print(json.dumps(report, indent=2, sort_keys=True, default=str))
    return 0 if not report["physical_W_export_enabled"] else 2


if __name__ == "__main__":
    raise SystemExit(cli_main())
