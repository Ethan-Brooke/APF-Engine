"""W_TRACE reviewed-source import handoff gate bank.

v11.8 (2026-05-09 LATER-53): reviewed-source handoff layer above the
v11.7 completed source-review packet validator and the v11.3 payload import
CLI.  This module banks the permission boundary between a validated review
packet and the payload file loader.  It deliberately ships no real completed
packet and no real finite-part payload rows: the closure is the handoff
contract, validation precondition, blocked-template/default behavior, and
physical-export lock preservation.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from pathlib import Path
from tempfile import TemporaryDirectory
import json
from typing import Any, Dict, Mapping, Tuple

from apf.w_trace_review_packet_validator import (
    W_REVIEW_PACKET_VALIDATOR_STATUS,
    REVIEW_PACKET_VALIDATOR_VERSION,
    CompletedReviewPacketPreflight,
    default_completed_packet_preflight,
    promoted_completed_packet_preflight,
    validate_completed_review_packet_preflight,
    check_T_w_review_packet_validator_bank_closure as _check_v117,
)
from apf.w_trace_payload_import_cli import (
    W_PAYLOAD_IMPORT_CLI_STATUS,
    SUPPORTED_LOADER_FORMATS,
    loader_report,
    write_synthetic_json_fixture,
    write_synthetic_csv_fixture,
    check_T_w_payload_import_cli_bank_closure as _check_v113,
)
from apf.w_trace_final_export_readiness import readiness_report

W_REVIEWED_SOURCE_IMPORT_HANDOFF_STATUS = "P_w_reviewed_source_import_handoff"
REVIEWED_SOURCE_IMPORT_HANDOFF_VERSION = "w_trace_reviewed_source_import_handoff_v1"
REVIEWED_SOURCE_IMPORT_HANDOFF_MODE = "VALIDATED_REVIEW_PACKET_TO_IMPORT_LOADER_HANDOFF__NO_REAL_PAYLOAD_SHIPPED"

REAL_COMPLETED_REVIEW_PACKET_SHIPPED = False
REAL_COMPLETED_REVIEW_PACKET_VALIDATED = False
REAL_REVIEWED_SOURCE_HANDOFF_COMPLETED = False
REAL_EXTERNAL_ROWS_IMPORTED = False
REAL_EXTERNAL_ROWS_ADMITTED = False
COMPONENT_SUM_CERTIFIED = False
COVARIANCE_CERTIFIED = False
UNCERTAINTY_PROPAGATION_CERTIFIED = False
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False

ROOT = Path(__file__).resolve().parent.parent
HANDOFF_DOC_PATH = ROOT / "W_TRACE_REVIEWED_SOURCE_IMPORT_HANDOFF_BANK_v1_0.md"
HANDOFF_EXAMPLE_DIR = ROOT / "examples" / "w_trace_reviewed_source_import_handoff"
HANDOFF_TEMPLATE_PATH = HANDOFF_EXAMPLE_DIR / "reviewed_source_import_handoff_template.json"

HANDOFF_STATES: Tuple[str, ...] = (
    "NO_REVIEW_PACKET",
    "REVIEW_PACKET_REJECTED",
    "VALIDATED_AWAITING_PAYLOAD_FILE",
    "HANDOFF_TO_LOADER_DRYRUN",
    "HANDOFF_TO_LOADER_READY_FOR_REAL_FILE",
    "BLOCKED_PHYSICAL_EXPORT_REQUEST",
)

REQUIRED_HANDOFF_REPORT_FIELDS: Tuple[str, ...] = (
    "status",
    "version",
    "mode",
    "handoff_state",
    "preflight_validated",
    "payload_path_supplied",
    "loader_invoked",
    "loader_report",
    "review_attestation_passed_to_loader",
    "shipped_real_data_passed_to_loader",
    "real_reviewed_source_handoff_completed",
    "real_external_rows_imported",
    "real_external_rows_admitted",
    "component_sum_certified",
    "covariance_certified",
    "uncertainty_propagation_certified",
    "physical_W_export_enabled",
    "exports_physical_M_W",
    "failure_reasons",
)

@dataclass(frozen=True)
class ReviewedSourceImportHandoff:
    preflight: CompletedReviewPacketPreflight | None = None
    payload_path: str | None = None
    ingest_format: str | None = None
    request_real_data: bool = False
    request_physical_export: bool = False
    handoff_revision: str = "UNSET"


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def _res(name: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    return {
        "passed": bool(passed),
        "status": "PASS" if passed else "FAIL",
        "tier": 4,
        "epistemic": W_REVIEWED_SOURCE_IMPORT_HANDOFF_STATUS,
        "check": name,
        **extra,
    }


def default_reviewed_source_import_handoff() -> ReviewedSourceImportHandoff:
    return ReviewedSourceImportHandoff(preflight=None)


def promoted_reviewed_source_import_handoff() -> ReviewedSourceImportHandoff:
    return ReviewedSourceImportHandoff(
        preflight=promoted_completed_packet_preflight(),
        payload_path=None,
        request_real_data=False,
        request_physical_export=False,
        handoff_revision="handoff-revision-0001",
    )


def _validate_preflight(preflight: CompletedReviewPacketPreflight | Mapping[str, Any] | None) -> Dict[str, Any]:
    if preflight is None:
        return {
            "passed": False,
            "status": "FAIL",
            "decision": "NO_REVIEW_PACKET",
            "reasons": ("NO_REVIEW_PACKET",),
            "ready_for_import_attempt": False,
            "physical_export_enabled": False,
            "exports_physical_M_W": False,
        }
    return validate_completed_review_packet_preflight(preflight)


def handoff_state(preflight_validation: Mapping[str, Any], payload_path: str | None, physical_export_requested: bool) -> str:
    if physical_export_requested:
        return "BLOCKED_PHYSICAL_EXPORT_REQUEST"
    if not preflight_validation.get("passed"):
        return "NO_REVIEW_PACKET" if "NO_REVIEW_PACKET" in tuple(preflight_validation.get("reasons", ())) else "REVIEW_PACKET_REJECTED"
    if payload_path is None:
        return "VALIDATED_AWAITING_PAYLOAD_FILE"
    return "HANDOFF_TO_LOADER_DRYRUN"


def reviewed_source_import_handoff_report(
    handoff: ReviewedSourceImportHandoff | Mapping[str, Any] | None = None,
) -> Dict[str, Any]:
    if handoff is None:
        h = default_reviewed_source_import_handoff()
    elif isinstance(handoff, ReviewedSourceImportHandoff):
        h = handoff
    else:
        h = ReviewedSourceImportHandoff(**dict(handoff))

    validation = _validate_preflight(h.preflight)
    state = handoff_state(validation, h.payload_path, h.request_physical_export)
    failures = []
    if not validation.get("passed"):
        failures.extend(str(x) for x in validation.get("reasons", ("REVIEW_PACKET_NOT_VALIDATED",)))
    if h.payload_path is None:
        failures.append("NO_PAYLOAD_FILE_SUPPLIED")
    if h.request_physical_export:
        failures.append("PHYSICAL_W_EXPORT_REQUEST_BLOCKED_BY_HANDOFF")

    loader_invoked = bool(validation.get("passed") and h.payload_path is not None and not h.request_physical_export)
    if loader_invoked:
        lr = loader_report(
            h.payload_path,
            h.ingest_format,
            review_attested=True,
            shipped_real_data=bool(h.request_real_data),
            physical_export_requested=False,
        )
        failures.extend(str(x) for x in lr.get("failure_reasons", ()))
    else:
        lr = loader_report(None, None, review_attested=False, shipped_real_data=False, physical_export_requested=False)

    ready = readiness_report(physical_export_requested=False)
    return {
        "status": W_REVIEWED_SOURCE_IMPORT_HANDOFF_STATUS,
        "version": REVIEWED_SOURCE_IMPORT_HANDOFF_VERSION,
        "mode": REVIEWED_SOURCE_IMPORT_HANDOFF_MODE,
        "upstream_validator_status": W_REVIEW_PACKET_VALIDATOR_STATUS,
        "upstream_loader_status": W_PAYLOAD_IMPORT_CLI_STATUS,
        "handoff_states": HANDOFF_STATES,
        "handoff_state": state,
        "handoff_revision": h.handoff_revision,
        "preflight_validation": validation,
        "preflight_validated": bool(validation.get("passed")),
        "payload_path_supplied": h.payload_path is not None,
        "payload_ingest_format": h.ingest_format,
        "loader_invoked": loader_invoked,
        "loader_report": lr,
        "review_attestation_passed_to_loader": bool(loader_invoked),
        "shipped_real_data_passed_to_loader": bool(loader_invoked and h.request_real_data),
        "real_completed_review_packet_shipped": REAL_COMPLETED_REVIEW_PACKET_SHIPPED,
        "real_completed_review_packet_validated": REAL_COMPLETED_REVIEW_PACKET_VALIDATED,
        "real_reviewed_source_handoff_completed": REAL_REVIEWED_SOURCE_HANDOFF_COMPLETED,
        "real_external_rows_imported": REAL_EXTERNAL_ROWS_IMPORTED,
        "real_external_rows_admitted": REAL_EXTERNAL_ROWS_ADMITTED,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "covariance_certified": COVARIANCE_CERTIFIED,
        "uncertainty_propagation_certified": UNCERTAINTY_PROPAGATION_CERTIFIED,
        "physical_W_export_enabled": PHYSICAL_W_EXPORT_ENABLED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "readiness_locked": not ready["physical_W_export_ready"] and not ready["physical_W_export_enabled"],
        "failure_reasons": tuple(dict.fromkeys(failures)),
        "handoff_doc_path": str(HANDOFF_DOC_PATH),
        "handoff_example_dir": str(HANDOFF_EXAMPLE_DIR),
        "handoff_template_path": str(HANDOFF_TEMPLATE_PATH),
    }


def write_handoff_template(path: str | Path = HANDOFF_TEMPLATE_PATH) -> str:
    data = {
        "template_only": True,
        "version": REVIEWED_SOURCE_IMPORT_HANDOFF_VERSION,
        "handoff_revision": "UNSET",
        "preflight": "PASTE_VALIDATED_COMPLETED_REVIEW_PACKET_PREFLIGHT_HERE",
        "payload_path": "PATH_TO_REVIEWED_EXTERNAL_PAYLOAD_FILE",
        "ingest_format": "json_rows_v1",
        "request_real_data": False,
        "request_physical_export": False,
        "warning": "Template only: not a validated packet, not real finite-part evidence, and not a physical-W export request.",
    }
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return str(path)


# Checks

def check_T_w_reviewed_source_import_handoff_status_declared():
    r = reviewed_source_import_handoff_report()
    ok = r["status"] == W_REVIEWED_SOURCE_IMPORT_HANDOFF_STATUS and not r["physical_W_export_enabled"]
    return _res("status_declared", ok, report=r)


def check_T_w_reviewed_source_import_handoff_depends_on_v117_validator():
    d = _check_v117()
    return _res("depends_on_v117_validator", _passed(d), upstream=d)


def check_T_w_reviewed_source_import_handoff_depends_on_v113_loader():
    d = _check_v113()
    return _res("depends_on_v113_loader", _passed(d), upstream=d)


def check_T_w_reviewed_source_import_handoff_states_declared():
    needed = {"NO_REVIEW_PACKET", "REVIEW_PACKET_REJECTED", "VALIDATED_AWAITING_PAYLOAD_FILE", "HANDOFF_TO_LOADER_DRYRUN", "BLOCKED_PHYSICAL_EXPORT_REQUEST"}
    return _res("states_declared", needed.issubset(set(HANDOFF_STATES)), states=HANDOFF_STATES)


def check_T_w_reviewed_source_import_handoff_report_schema_declared():
    r = reviewed_source_import_handoff_report()
    ok = all(k in r for k in REQUIRED_HANDOFF_REPORT_FIELDS)
    return _res("report_schema_declared", ok, fields=REQUIRED_HANDOFF_REPORT_FIELDS)


def check_T_w_reviewed_source_import_handoff_default_no_packet_blocked():
    r = reviewed_source_import_handoff_report(default_reviewed_source_import_handoff())
    ok = r["handoff_state"] == "NO_REVIEW_PACKET" and not r["loader_invoked"] and "NO_REVIEW_PACKET" in r["failure_reasons"]
    return _res("default_no_packet_blocked", ok, report=r)


def check_T_w_reviewed_source_import_handoff_default_loader_not_invoked():
    r = reviewed_source_import_handoff_report()
    ok = not r["preflight_validated"] and not r["loader_invoked"] and not r["review_attestation_passed_to_loader"]
    return _res("default_loader_not_invoked", ok, report=r)


def check_T_w_reviewed_source_import_handoff_promoted_packet_validates():
    r = reviewed_source_import_handoff_report(promoted_reviewed_source_import_handoff())
    ok = r["preflight_validated"] and r["handoff_state"] == "VALIDATED_AWAITING_PAYLOAD_FILE"
    return _res("promoted_packet_validates", ok, report=r)


def check_T_w_reviewed_source_import_handoff_promoted_without_payload_no_import():
    r = reviewed_source_import_handoff_report(promoted_reviewed_source_import_handoff())
    ok = not r["loader_invoked"] and not r["real_external_rows_imported"] and "NO_PAYLOAD_FILE_SUPPLIED" in r["failure_reasons"]
    return _res("promoted_without_payload_no_import", ok, report=r)


def check_T_w_reviewed_source_import_handoff_rejects_template_preflight():
    h = ReviewedSourceImportHandoff(preflight=default_completed_packet_preflight(), payload_path="dummy.json")
    r = reviewed_source_import_handoff_report(h)
    ok = r["handoff_state"] == "REVIEW_PACKET_REJECTED" and not r["loader_invoked"]
    return _res("rejects_template_preflight", ok, report=r)


def check_T_w_reviewed_source_import_handoff_rejects_physical_export_request():
    h = replace(promoted_reviewed_source_import_handoff(), request_physical_export=True)
    r = reviewed_source_import_handoff_report(h)
    ok = r["handoff_state"] == "BLOCKED_PHYSICAL_EXPORT_REQUEST" and not r["loader_invoked"] and not r["physical_W_export_enabled"]
    return _res("rejects_physical_export_request", ok, report=r)


def check_T_w_reviewed_source_import_handoff_validated_json_fixture_invokes_loader():
    with TemporaryDirectory() as td:
        p = Path(td) / "shape.json"; write_synthetic_json_fixture(p)
        h = replace(promoted_reviewed_source_import_handoff(), payload_path=str(p), ingest_format="json_rows_v1")
        r = reviewed_source_import_handoff_report(h)
    ok = r["loader_invoked"] and r["loader_report"]["file_exists"] and r["loader_report"]["rows_loaded"] == 8
    return _res("validated_json_fixture_invokes_loader", ok, report=r)


def check_T_w_reviewed_source_import_handoff_validated_csv_fixture_invokes_loader():
    with TemporaryDirectory() as td:
        p = Path(td) / "shape.csv"; write_synthetic_csv_fixture(p)
        h = replace(promoted_reviewed_source_import_handoff(), payload_path=str(p), ingest_format="csv_with_header_v1")
        r = reviewed_source_import_handoff_report(h)
    ok = r["loader_invoked"] and r["loader_report"]["file_exists"] and r["loader_report"]["rows_loaded"] == 8
    return _res("validated_csv_fixture_invokes_loader", ok, report=r)


def check_T_w_reviewed_source_import_handoff_invalid_packet_blocks_existing_file():
    with TemporaryDirectory() as td:
        p = Path(td) / "shape.json"; write_synthetic_json_fixture(p)
        h = ReviewedSourceImportHandoff(preflight=default_completed_packet_preflight(), payload_path=str(p), ingest_format="json_rows_v1")
        r = reviewed_source_import_handoff_report(h)
    ok = not r["loader_invoked"] and r["loader_report"]["file_exists"] is False and r["loader_report"]["rows_loaded"] == 0
    return _res("invalid_packet_blocks_existing_file", ok, report=r)


def check_T_w_reviewed_source_import_handoff_review_attestation_only_after_validation():
    with TemporaryDirectory() as td:
        p = Path(td) / "shape.json"; write_synthetic_json_fixture(p)
        good = reviewed_source_import_handoff_report(replace(promoted_reviewed_source_import_handoff(), payload_path=str(p), ingest_format="json_rows_v1"))
        bad = reviewed_source_import_handoff_report(ReviewedSourceImportHandoff(preflight=default_completed_packet_preflight(), payload_path=str(p), ingest_format="json_rows_v1"))
    ok = good["review_attestation_passed_to_loader"] and not bad["review_attestation_passed_to_loader"]
    return _res("review_attestation_only_after_validation", ok, good=good, bad=bad)


def check_T_w_reviewed_source_import_handoff_shape_fixture_not_real_payload():
    with TemporaryDirectory() as td:
        p = Path(td) / "shape.json"; write_synthetic_json_fixture(p)
        h = replace(promoted_reviewed_source_import_handoff(), payload_path=str(p), ingest_format="json_rows_v1", request_real_data=False)
        r = reviewed_source_import_handoff_report(h)
    ok = r["loader_invoked"] and not r["shipped_real_data_passed_to_loader"] and not r["real_external_rows_imported"]
    return _res("shape_fixture_not_real_payload", ok, report=r)


def check_T_w_reviewed_source_import_handoff_real_flag_still_no_admission_without_bundle():
    with TemporaryDirectory() as td:
        p = Path(td) / "shape.json"; write_synthetic_json_fixture(p)
        h = replace(promoted_reviewed_source_import_handoff(), payload_path=str(p), ingest_format="json_rows_v1", request_real_data=True)
        r = reviewed_source_import_handoff_report(h)
    ok = r["shipped_real_data_passed_to_loader"] and not r["real_external_rows_admitted"] and not r["physical_W_export_enabled"]
    return _res("real_flag_still_no_admission_without_bundle", ok, report=r)


def check_T_w_reviewed_source_import_handoff_loader_failures_propagate():
    with TemporaryDirectory() as td:
        p = Path(td) / "bad.json"; p.write_text("not-json", encoding="utf-8")
        h = replace(promoted_reviewed_source_import_handoff(), payload_path=str(p), ingest_format="json_rows_v1")
        r = reviewed_source_import_handoff_report(h)
    ok = r["loader_invoked"] and "PAYLOAD_PARSE_ERROR" in r["failure_reasons"]
    return _res("loader_failures_propagate", ok, report=r)


def check_T_w_reviewed_source_import_handoff_missing_file_fails_closed():
    h = replace(promoted_reviewed_source_import_handoff(), payload_path="/tmp/definitely_missing_w_trace_payload.json", ingest_format="json_rows_v1")
    r = reviewed_source_import_handoff_report(h)
    ok = r["loader_invoked"] and "PAYLOAD_FILE_NOT_FOUND" in r["failure_reasons"] and not r["physical_W_export_enabled"]
    return _res("missing_file_fails_closed", ok, report=r)


def check_T_w_reviewed_source_import_handoff_supported_formats_inherited():
    ok = {"json_rows_v1", "csv_with_header_v1"}.issubset(set(SUPPORTED_LOADER_FORMATS))
    return _res("supported_formats_inherited", ok, formats=SUPPORTED_LOADER_FORMATS)


def check_T_w_reviewed_source_import_handoff_readiness_lock_preserved():
    r = reviewed_source_import_handoff_report(promoted_reviewed_source_import_handoff())
    ok = r["readiness_locked"] and not r["physical_W_export_enabled"] and not r["exports_physical_M_W"]
    return _res("readiness_lock_preserved", ok, report=r)


def check_T_w_reviewed_source_import_handoff_no_rows_or_certificates():
    r = reviewed_source_import_handoff_report()
    ok = not r["real_external_rows_admitted"] and not r["component_sum_certified"] and not r["covariance_certified"] and not r["uncertainty_propagation_certified"]
    return _res("no_rows_or_certificates", ok, report=r)


def check_T_w_reviewed_source_import_handoff_no_physical_W_export():
    r = reviewed_source_import_handoff_report(promoted_reviewed_source_import_handoff())
    ok = not r["physical_W_export_enabled"] and not r["exports_physical_M_W"]
    return _res("no_physical_W_export", ok, report=r)


def check_T_w_reviewed_source_import_handoff_template_path_declared():
    ok = str(HANDOFF_TEMPLATE_PATH).endswith("reviewed_source_import_handoff_template.json")
    return _res("template_path_declared", ok, path=str(HANDOFF_TEMPLATE_PATH))


def check_T_w_reviewed_source_import_handoff_write_template():
    with TemporaryDirectory() as td:
        p = Path(td) / "template.json"
        write_handoff_template(p)
        data = json.loads(p.read_text(encoding="utf-8"))
    ok = data["template_only"] is True and data["request_physical_export"] is False and REVIEWED_SOURCE_IMPORT_HANDOFF_VERSION in data["version"]
    return _res("write_template", ok, data=data)


def check_T_w_reviewed_source_import_handoff_doc_exists():
    return _res("doc_exists", HANDOFF_DOC_PATH.exists(), path=str(HANDOFF_DOC_PATH))


def check_T_w_reviewed_source_import_handoff_doc_warns_locked():
    text = HANDOFF_DOC_PATH.read_text(encoding="utf-8") if HANDOFF_DOC_PATH.exists() else ""
    needed = ("No real reviewed source is shipped", "validated review packet", "payload import CLI", "physical W export remains locked")
    ok = all(s in text for s in needed)
    return _res("doc_warns_locked", ok, needed=needed)


def check_T_w_reviewed_source_import_handoff_example_dir_exists():
    return _res("example_dir_exists", HANDOFF_EXAMPLE_DIR.exists(), path=str(HANDOFF_EXAMPLE_DIR))


def check_T_w_reviewed_source_import_handoff_template_file_exists():
    return _res("template_file_exists", HANDOFF_TEMPLATE_PATH.exists(), path=str(HANDOFF_TEMPLATE_PATH))


def check_T_w_reviewed_source_import_handoff_template_not_real():
    if not HANDOFF_TEMPLATE_PATH.exists():
        return _res("template_not_real", False, path=str(HANDOFF_TEMPLATE_PATH))
    data = json.loads(HANDOFF_TEMPLATE_PATH.read_text(encoding="utf-8"))
    ok = data.get("template_only") is True and data.get("request_real_data") is False and data.get("request_physical_export") is False
    return _res("template_not_real", ok, data=data)


def check_T_w_reviewed_source_import_handoff_serializes_report_json():
    text = json.dumps(reviewed_source_import_handoff_report(promoted_reviewed_source_import_handoff()), sort_keys=True, default=str)
    ok = REVIEWED_SOURCE_IMPORT_HANDOFF_VERSION in text and "VALIDATED_AWAITING_PAYLOAD_FILE" in text and "physical_W_export_enabled" in text
    return _res("serializes_report_json", ok, json_length=len(text))


def check_T_w_reviewed_source_import_handoff_bank_closure():
    # Keep closure lightweight: the targeted verifier exercises every row above.
    # This terminal theorem records the locked handoff invariant without
    # recursively re-running upstream closures and producing very large nested
    # diagnostic payloads.
    r = reviewed_source_import_handoff_report(promoted_reviewed_source_import_handoff())
    ok = (
        r["preflight_validated"]
        and r["handoff_state"] == "VALIDATED_AWAITING_PAYLOAD_FILE"
        and not r["loader_invoked"]
        and not r["real_external_rows_admitted"]
        and not r["component_sum_certified"]
        and not r["covariance_certified"]
        and not r["uncertainty_propagation_certified"]
        and not r["physical_W_export_enabled"]
        and not r["exports_physical_M_W"]
    )
    return _res("bank_closure", ok, total=len(CHECKS), report=r)


CHECKS: Dict[str, Any] = {
    "T_w_reviewed_source_import_handoff_status_declared": check_T_w_reviewed_source_import_handoff_status_declared,
    "T_w_reviewed_source_import_handoff_depends_on_v117_validator": check_T_w_reviewed_source_import_handoff_depends_on_v117_validator,
    "T_w_reviewed_source_import_handoff_depends_on_v113_loader": check_T_w_reviewed_source_import_handoff_depends_on_v113_loader,
    "T_w_reviewed_source_import_handoff_states_declared": check_T_w_reviewed_source_import_handoff_states_declared,
    "T_w_reviewed_source_import_handoff_report_schema_declared": check_T_w_reviewed_source_import_handoff_report_schema_declared,
    "T_w_reviewed_source_import_handoff_default_no_packet_blocked": check_T_w_reviewed_source_import_handoff_default_no_packet_blocked,
    "T_w_reviewed_source_import_handoff_default_loader_not_invoked": check_T_w_reviewed_source_import_handoff_default_loader_not_invoked,
    "T_w_reviewed_source_import_handoff_promoted_packet_validates": check_T_w_reviewed_source_import_handoff_promoted_packet_validates,
    "T_w_reviewed_source_import_handoff_promoted_without_payload_no_import": check_T_w_reviewed_source_import_handoff_promoted_without_payload_no_import,
    "T_w_reviewed_source_import_handoff_rejects_template_preflight": check_T_w_reviewed_source_import_handoff_rejects_template_preflight,
    "T_w_reviewed_source_import_handoff_rejects_physical_export_request": check_T_w_reviewed_source_import_handoff_rejects_physical_export_request,
    "T_w_reviewed_source_import_handoff_validated_json_fixture_invokes_loader": check_T_w_reviewed_source_import_handoff_validated_json_fixture_invokes_loader,
    "T_w_reviewed_source_import_handoff_validated_csv_fixture_invokes_loader": check_T_w_reviewed_source_import_handoff_validated_csv_fixture_invokes_loader,
    "T_w_reviewed_source_import_handoff_invalid_packet_blocks_existing_file": check_T_w_reviewed_source_import_handoff_invalid_packet_blocks_existing_file,
    "T_w_reviewed_source_import_handoff_review_attestation_only_after_validation": check_T_w_reviewed_source_import_handoff_review_attestation_only_after_validation,
    "T_w_reviewed_source_import_handoff_shape_fixture_not_real_payload": check_T_w_reviewed_source_import_handoff_shape_fixture_not_real_payload,
    "T_w_reviewed_source_import_handoff_real_flag_still_no_admission_without_bundle": check_T_w_reviewed_source_import_handoff_real_flag_still_no_admission_without_bundle,
    "T_w_reviewed_source_import_handoff_loader_failures_propagate": check_T_w_reviewed_source_import_handoff_loader_failures_propagate,
    "T_w_reviewed_source_import_handoff_missing_file_fails_closed": check_T_w_reviewed_source_import_handoff_missing_file_fails_closed,
    "T_w_reviewed_source_import_handoff_supported_formats_inherited": check_T_w_reviewed_source_import_handoff_supported_formats_inherited,
    "T_w_reviewed_source_import_handoff_readiness_lock_preserved": check_T_w_reviewed_source_import_handoff_readiness_lock_preserved,
    "T_w_reviewed_source_import_handoff_no_rows_or_certificates": check_T_w_reviewed_source_import_handoff_no_rows_or_certificates,
    "T_w_reviewed_source_import_handoff_no_physical_W_export": check_T_w_reviewed_source_import_handoff_no_physical_W_export,
    "T_w_reviewed_source_import_handoff_template_path_declared": check_T_w_reviewed_source_import_handoff_template_path_declared,
    "T_w_reviewed_source_import_handoff_write_template": check_T_w_reviewed_source_import_handoff_write_template,
    "T_w_reviewed_source_import_handoff_doc_exists": check_T_w_reviewed_source_import_handoff_doc_exists,
    "T_w_reviewed_source_import_handoff_doc_warns_locked": check_T_w_reviewed_source_import_handoff_doc_warns_locked,
    "T_w_reviewed_source_import_handoff_example_dir_exists": check_T_w_reviewed_source_import_handoff_example_dir_exists,
    "T_w_reviewed_source_import_handoff_template_file_exists": check_T_w_reviewed_source_import_handoff_template_file_exists,
    "T_w_reviewed_source_import_handoff_template_not_real": check_T_w_reviewed_source_import_handoff_template_not_real,
    "T_w_reviewed_source_import_handoff_serializes_report_json": check_T_w_reviewed_source_import_handoff_serializes_report_json,
    "T_w_reviewed_source_import_handoff_bank_closure": check_T_w_reviewed_source_import_handoff_bank_closure,
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
        "status": "W_TRACE_REVIEWED_SOURCE_IMPORT_HANDOFF_BANK_PASS" if ok else "W_TRACE_REVIEWED_SOURCE_IMPORT_HANDOFF_BANK_FAIL",
        "checks": rows,
        "report": reviewed_source_import_handoff_report(),
    }
