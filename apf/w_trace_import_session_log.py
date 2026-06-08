"""W_TRACE reviewed payload import session log / audit-trail bank.

v11.9 (2026-05-09 LATER-54): session-level audit trail above the
v11.8 reviewed-source import handoff gate and v11.3 payload import CLI.
This module does not ship real finite-part rows and does not admit a
physical W export.  It banks the immutable audit-record schema for future
reviewed payload import sessions: handoff digest, payload digest, loader
status, admission state, component/covariance/export locks, and explicit
anti-smuggling tokens.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Dict, Mapping, Tuple
import hashlib
import json

from apf.w_trace_reviewed_source_import_handoff import (
    W_REVIEWED_SOURCE_IMPORT_HANDOFF_STATUS,
    REVIEWED_SOURCE_IMPORT_HANDOFF_VERSION,
    ReviewedSourceImportHandoff,
    promoted_reviewed_source_import_handoff,
    reviewed_source_import_handoff_report,
    check_T_w_reviewed_source_import_handoff_bank_closure as _check_v118,
)
from apf.w_trace_payload_import_cli import (
    W_PAYLOAD_IMPORT_CLI_STATUS,
    write_synthetic_json_fixture,
)
from apf.w_trace_final_export_readiness import readiness_report

W_IMPORT_SESSION_LOG_STATUS = "P_w_import_session_log"
IMPORT_SESSION_LOG_VERSION = "w_trace_import_session_log_v1"
IMPORT_SESSION_LOG_MODE = "REVIEWED_PAYLOAD_IMPORT_SESSION_AUDIT_TRAIL__NO_REAL_PAYLOAD_SHIPPED"

REAL_IMPORT_SESSION_SHIPPED = False
REAL_IMPORT_SESSION_VALIDATED = False
REAL_EXTERNAL_ROWS_IMPORTED = False
REAL_EXTERNAL_ROWS_ADMITTED = False
COMPONENT_SUM_CERTIFIED = False
COVARIANCE_CERTIFIED = False
UNCERTAINTY_PROPAGATION_CERTIFIED = False
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False

ROOT = Path(__file__).resolve().parent.parent
SESSION_LOG_DOC_PATH = ROOT / "W_TRACE_IMPORT_SESSION_LOG_BANK_v1_0.md"
SESSION_LOG_EXAMPLE_DIR = ROOT / "examples" / "w_trace_import_session_log"
SESSION_LOG_TEMPLATE_PATH = SESSION_LOG_EXAMPLE_DIR / "import_session_log_template.json"

SESSION_STATES: Tuple[str, ...] = (
    "NO_SESSION",
    "HANDOFF_NOT_VALIDATED",
    "AWAITING_PAYLOAD_FILE",
    "LOADER_DRYRUN_RECORDED",
    "REAL_PAYLOAD_RECORDED_NOT_ADMITTED",
    "BLOCKED_PHYSICAL_EXPORT_REQUEST",
)

REQUIRED_SESSION_RECORD_FIELDS: Tuple[str, ...] = (
    "session_id",
    "session_version",
    "session_state",
    "handoff_status",
    "handoff_version",
    "handoff_validated",
    "payload_path_supplied",
    "payload_digest",
    "payload_digest_algorithm",
    "loader_invoked",
    "loader_status",
    "loader_passed",
    "review_packet_digest",
    "source_candidate_digest",
    "extraction_log_digest",
    "real_payload_claimed",
    "real_external_rows_imported",
    "real_external_rows_admitted",
    "component_sum_certified",
    "covariance_certified",
    "uncertainty_propagation_certified",
    "physical_W_export_enabled",
    "exports_physical_M_W",
    "failure_reasons",
)

FORBIDDEN_AUDIT_TOKENS: Tuple[str, ...] = (
    "observed_M_W",
    "M_W_world_average",
    "world_average_W_mass",
    "fit_residual",
    "apf_anchor_delta_r",
    "APF_ANCHOR_DELTA_R_TARGET",
    "component_sum_residual_to_apf_target",
    "physical_export_request",
)

@dataclass(frozen=True)
class ImportSessionLogRequest:
    session_id: str = "UNSET"
    handoff: ReviewedSourceImportHandoff | None = None
    payload_path: str | None = None
    ingest_format: str | None = None
    review_packet_digest: str = "UNSET"
    source_candidate_digest: str = "UNSET"
    extraction_log_digest: str = "UNSET"
    real_payload_claimed: bool = False
    request_physical_export: bool = False


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def _res(name: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    return {"passed": bool(passed), "status": "PASS" if passed else "FAIL", "tier": 4, "epistemic": W_IMPORT_SESSION_LOG_STATUS, "check": name, **extra}


def _sha256_file(path: str | None) -> str:
    if not path:
        return "NO_PAYLOAD_FILE"
    p = Path(path)
    if not p.exists() or not p.is_file():
        return "PAYLOAD_FILE_MISSING"
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def default_import_session_log_request() -> ImportSessionLogRequest:
    return ImportSessionLogRequest(session_id="NO_SESSION", handoff=None)


def promoted_import_session_log_request() -> ImportSessionLogRequest:
    return ImportSessionLogRequest(
        session_id="reviewed-source-session-0001",
        handoff=promoted_reviewed_source_import_handoff(),
        payload_path=None,
        ingest_format=None,
        review_packet_digest="sha256:review-packet-digest-placeholder-64hex-required",
        source_candidate_digest="sha256:source-candidate-digest-placeholder-64hex-required",
        extraction_log_digest="sha256:extraction-log-digest-placeholder-64hex-required",
        real_payload_claimed=False,
        request_physical_export=False,
    )


def session_state(handoff_report: Mapping[str, Any], req: ImportSessionLogRequest) -> str:
    if req.request_physical_export:
        return "BLOCKED_PHYSICAL_EXPORT_REQUEST"
    if req.handoff is None:
        return "NO_SESSION"
    if not handoff_report.get("preflight_validated"):
        return "HANDOFF_NOT_VALIDATED"
    if req.payload_path is None:
        return "AWAITING_PAYLOAD_FILE"
    if req.real_payload_claimed:
        return "REAL_PAYLOAD_RECORDED_NOT_ADMITTED"
    return "LOADER_DRYRUN_RECORDED"


def _contains_forbidden_token(obj: Any) -> bool:
    """Search forbidden tokens in user/source-supplied values, not schema keys.

Field names such as request_physical_export are part of the guardrail
contract and must not themselves trip the observed-W/APF-anchor audit.
"""
    hits = []
    def walk(x: Any) -> None:
        if isinstance(x, str):
            hits.extend(tok for tok in FORBIDDEN_AUDIT_TOKENS if tok in x)
        elif isinstance(x, Mapping):
            for v in x.values():
                walk(v)
        elif isinstance(x, (list, tuple, set)):
            for v in x:
                walk(v)
        else:
            return
    walk(obj)
    return bool(hits)


def import_session_log_report(request: ImportSessionLogRequest | Mapping[str, Any] | None = None) -> Dict[str, Any]:
    if request is None:
        req = default_import_session_log_request()
    elif isinstance(request, ImportSessionLogRequest):
        req = request
    else:
        req = ImportSessionLogRequest(**dict(request))

    # Physical export is deliberately passed through to the handoff request so
    # the upstream handoff records the blocked state as well.
    h = req.handoff
    if h is not None and req.payload_path is not None:
        h = replace(h, payload_path=req.payload_path, ingest_format=req.ingest_format, request_real_data=req.real_payload_claimed, request_physical_export=req.request_physical_export)
    elif h is not None and req.request_physical_export:
        h = replace(h, request_physical_export=True)

    handoff_report = reviewed_source_import_handoff_report(h)
    lr = handoff_report.get("loader_report", {})
    ready = readiness_report(physical_export_requested=False)
    payload_digest = _sha256_file(req.payload_path)

    failures = []
    failures.extend(str(x) for x in handoff_report.get("failure_reasons", ()))
    if req.session_id in {"", "UNSET", "NO_SESSION"}:
        failures.append("SESSION_ID_NOT_PROMOTED")
    if req.payload_path is None:
        failures.append("NO_PAYLOAD_FILE_SUPPLIED")
    if payload_digest == "PAYLOAD_FILE_MISSING":
        failures.append("PAYLOAD_FILE_MISSING")
    if req.request_physical_export:
        failures.append("PHYSICAL_W_EXPORT_REQUEST_BLOCKED_BY_SESSION_LOG")
    if _contains_forbidden_token(asdict(req)):
        failures.append("FORBIDDEN_AUDIT_TOKEN_PRESENT")

    state = session_state(handoff_report, req)
    loader_passed = bool(lr.get("passed") is True or lr.get("status") == "PASS")

    return {
        "status": W_IMPORT_SESSION_LOG_STATUS,
        "version": IMPORT_SESSION_LOG_VERSION,
        "mode": IMPORT_SESSION_LOG_MODE,
        "session_states": SESSION_STATES,
        "session_id": req.session_id,
        "session_version": IMPORT_SESSION_LOG_VERSION,
        "session_state": state,
        "handoff_status": W_REVIEWED_SOURCE_IMPORT_HANDOFF_STATUS,
        "handoff_version": REVIEWED_SOURCE_IMPORT_HANDOFF_VERSION,
        "handoff_report": handoff_report,
        "handoff_validated": bool(handoff_report.get("preflight_validated")),
        "payload_path_supplied": req.payload_path is not None,
        "payload_digest": payload_digest,
        "payload_digest_algorithm": "sha256",
        "loader_invoked": bool(handoff_report.get("loader_invoked")),
        "loader_status": W_PAYLOAD_IMPORT_CLI_STATUS,
        "loader_report": lr,
        "loader_passed": loader_passed,
        "review_packet_digest": req.review_packet_digest,
        "source_candidate_digest": req.source_candidate_digest,
        "extraction_log_digest": req.extraction_log_digest,
        "real_payload_claimed": bool(req.real_payload_claimed),
        "real_import_session_shipped": REAL_IMPORT_SESSION_SHIPPED,
        "real_import_session_validated": REAL_IMPORT_SESSION_VALIDATED,
        "real_external_rows_imported": REAL_EXTERNAL_ROWS_IMPORTED,
        "real_external_rows_admitted": REAL_EXTERNAL_ROWS_ADMITTED,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "covariance_certified": COVARIANCE_CERTIFIED,
        "uncertainty_propagation_certified": UNCERTAINTY_PROPAGATION_CERTIFIED,
        "physical_W_export_enabled": PHYSICAL_W_EXPORT_ENABLED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "readiness_locked": not ready["physical_W_export_ready"] and not ready["physical_W_export_enabled"],
        "forbidden_audit_tokens": FORBIDDEN_AUDIT_TOKENS,
        "forbidden_token_present": _contains_forbidden_token(asdict(req)),
        "failure_reasons": tuple(dict.fromkeys(failures)),
        "session_log_doc_path": str(SESSION_LOG_DOC_PATH),
        "session_log_example_dir": str(SESSION_LOG_EXAMPLE_DIR),
        "session_log_template_path": str(SESSION_LOG_TEMPLATE_PATH),
    }


def write_session_log_template(path: str | Path = SESSION_LOG_TEMPLATE_PATH) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "template_only": True,
        "not_real_finite_part_evidence": True,
        "status": W_IMPORT_SESSION_LOG_STATUS,
        "version": IMPORT_SESSION_LOG_VERSION,
        "session_id": "REPLACE_WITH_REVIEWED_SOURCE_SESSION_ID",
        "review_packet_digest": "sha256:<completed-review-packet-digest>",
        "source_candidate_digest": "sha256:<source-candidate-digest>",
        "extraction_log_digest": "sha256:<extraction-log-digest>",
        "payload_digest_algorithm": "sha256",
        "real_payload_claimed": False,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
    }
    p.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return p


# Checks

def check_T_w_import_session_log_status_declared():
    r = import_session_log_report()
    return _res("status_declared", r["status"] == W_IMPORT_SESSION_LOG_STATUS and r["version"] == IMPORT_SESSION_LOG_VERSION, report=r)


def check_T_w_import_session_log_depends_on_v118_handoff():
    r = _check_v118()
    return _res("depends_on_v118_handoff", _passed(r), upstream=r)


def check_T_w_import_session_log_states_declared():
    ok = set(SESSION_STATES) >= {"NO_SESSION", "AWAITING_PAYLOAD_FILE", "LOADER_DRYRUN_RECORDED", "BLOCKED_PHYSICAL_EXPORT_REQUEST"}
    return _res("states_declared", ok, states=SESSION_STATES)


def check_T_w_import_session_log_record_schema_declared():
    r = import_session_log_report(promoted_import_session_log_request())
    missing = [f for f in REQUIRED_SESSION_RECORD_FIELDS if f not in r]
    return _res("record_schema_declared", not missing, missing=missing)


def check_T_w_import_session_log_default_no_session():
    r = import_session_log_report()
    ok = r["session_state"] == "NO_SESSION" and not r["handoff_validated"] and not r["loader_invoked"]
    return _res("default_no_session", ok, report=r)


def check_T_w_import_session_log_promoted_awaits_payload():
    r = import_session_log_report(promoted_import_session_log_request())
    ok = r["handoff_validated"] and r["session_state"] == "AWAITING_PAYLOAD_FILE" and not r["loader_invoked"]
    return _res("promoted_awaits_payload", ok, report=r)


def check_T_w_import_session_log_records_json_dryrun_digest():
    with TemporaryDirectory() as td:
        p = write_synthetic_json_fixture(Path(td) / "payload.json")
        req = replace(promoted_import_session_log_request(), payload_path=str(p), ingest_format="json_rows_v1")
        r = import_session_log_report(req)
    ok = r["session_state"] == "LOADER_DRYRUN_RECORDED" and r["payload_digest_algorithm"] == "sha256" and len(r["payload_digest"]) == 64
    return _res("records_json_dryrun_digest", ok, digest=r["payload_digest"], report_state=r["session_state"])


def check_T_w_import_session_log_loader_invoked_only_after_valid_handoff():
    with TemporaryDirectory() as td:
        p = write_synthetic_json_fixture(Path(td) / "payload.json")
        bad = ImportSessionLogRequest(session_id="bad", handoff=None, payload_path=str(p), ingest_format="json_rows_v1")
        rb = import_session_log_report(bad)
        good = replace(promoted_import_session_log_request(), payload_path=str(p), ingest_format="json_rows_v1")
        rg = import_session_log_report(good)
    ok = (not rb["loader_invoked"]) and rg["loader_invoked"]
    return _res("loader_invoked_only_after_valid_handoff", ok, bad=rb["session_state"], good=rg["session_state"])


def check_T_w_import_session_log_missing_payload_fails_closed():
    req = replace(promoted_import_session_log_request(), payload_path="/no/such/file.json", ingest_format="json_rows_v1")
    r = import_session_log_report(req)
    ok = "PAYLOAD_FILE_MISSING" in r["failure_reasons"] and not r["real_external_rows_admitted"] and not r["physical_W_export_enabled"]
    return _res("missing_payload_fails_closed", ok, report=r)


def check_T_w_import_session_log_real_flag_does_not_admit_rows():
    with TemporaryDirectory() as td:
        p = write_synthetic_json_fixture(Path(td) / "payload.json")
        req = replace(promoted_import_session_log_request(), payload_path=str(p), ingest_format="json_rows_v1", real_payload_claimed=True)
        r = import_session_log_report(req)
    ok = r["session_state"] == "REAL_PAYLOAD_RECORDED_NOT_ADMITTED" and not r["real_external_rows_admitted"]
    return _res("real_flag_does_not_admit_rows", ok, report=r)


def check_T_w_import_session_log_blocks_physical_export_request():
    r = import_session_log_report(replace(promoted_import_session_log_request(), request_physical_export=True))
    ok = r["session_state"] == "BLOCKED_PHYSICAL_EXPORT_REQUEST" and "PHYSICAL_W_EXPORT_REQUEST_BLOCKED_BY_SESSION_LOG" in r["failure_reasons"] and not r["exports_physical_M_W"]
    return _res("blocks_physical_export_request", ok, report=r)


def check_T_w_import_session_log_forbidden_tokens_declared():
    ok = "observed_M_W" in FORBIDDEN_AUDIT_TOKENS and "apf_anchor_delta_r" in FORBIDDEN_AUDIT_TOKENS
    return _res("forbidden_tokens_declared", ok, tokens=FORBIDDEN_AUDIT_TOKENS)


def check_T_w_import_session_log_rejects_forbidden_review_digest_token():
    req = replace(promoted_import_session_log_request(), review_packet_digest="sha256:observed_M_W")
    r = import_session_log_report(req)
    ok = r["forbidden_token_present"] and "FORBIDDEN_AUDIT_TOKEN_PRESENT" in r["failure_reasons"]
    return _res("rejects_forbidden_review_digest_token", ok, report=r)


def check_T_w_import_session_log_preserves_export_lock():
    r = import_session_log_report(promoted_import_session_log_request())
    ok = r["readiness_locked"] and not r["physical_W_export_enabled"] and not r["exports_physical_M_W"]
    return _res("preserves_export_lock", ok, report=r)


def check_T_w_import_session_log_no_rows_or_certificates_by_default():
    r = import_session_log_report(promoted_import_session_log_request())
    ok = not any(r[k] for k in ("real_external_rows_imported", "real_external_rows_admitted", "component_sum_certified", "covariance_certified", "uncertainty_propagation_certified"))
    return _res("no_rows_or_certificates_by_default", ok, report=r)


def check_T_w_import_session_log_payload_digest_changes_with_file():
    with TemporaryDirectory() as td:
        p1 = Path(td) / "a.json"; p1.write_text("{\"a\": 1}\n")
        p2 = Path(td) / "b.json"; p2.write_text("{\"a\": 2}\n")
        r1 = import_session_log_report(replace(promoted_import_session_log_request(), payload_path=str(p1), ingest_format="json_rows_v1"))
        r2 = import_session_log_report(replace(promoted_import_session_log_request(), payload_path=str(p2), ingest_format="json_rows_v1"))
    ok = len(r1["payload_digest"]) == 64 and len(r2["payload_digest"]) == 64 and r1["payload_digest"] != r2["payload_digest"]
    return _res("payload_digest_changes_with_file", ok, digest1=r1["payload_digest"], digest2=r2["payload_digest"])


def check_T_w_import_session_log_failure_reasons_deduplicated():
    r = import_session_log_report(default_import_session_log_request())
    ok = len(r["failure_reasons"]) == len(set(r["failure_reasons"]))
    return _res("failure_reasons_deduplicated", ok, reasons=r["failure_reasons"])


def check_T_w_import_session_log_json_serializable():
    text = json.dumps(import_session_log_report(promoted_import_session_log_request()), sort_keys=True, default=str)
    ok = W_IMPORT_SESSION_LOG_STATUS in text and "physical_W_export_enabled" in text
    return _res("json_serializable", ok, json_length=len(text))


def check_T_w_import_session_log_template_path_declared():
    ok = SESSION_LOG_TEMPLATE_PATH.name == "import_session_log_template.json" and "w_trace_import_session_log" in str(SESSION_LOG_TEMPLATE_PATH)
    return _res("template_path_declared", ok, path=str(SESSION_LOG_TEMPLATE_PATH))


def check_T_w_import_session_log_write_template():
    with TemporaryDirectory() as td:
        p = write_session_log_template(Path(td) / "template.json")
        data = json.loads(p.read_text())
    ok = data["template_only"] and data["physical_W_export_enabled"] is False and data["exports_physical_M_W"] is False
    return _res("write_template", ok, data=data)


def check_T_w_import_session_log_doc_exists():
    ok = SESSION_LOG_DOC_PATH.exists() and SESSION_LOG_DOC_PATH.is_file()
    return _res("doc_exists", ok, path=str(SESSION_LOG_DOC_PATH))


def check_T_w_import_session_log_doc_warns_locked():
    text = SESSION_LOG_DOC_PATH.read_text(encoding="utf-8") if SESSION_LOG_DOC_PATH.exists() else ""
    ok = "physical W export remains OPEN" in text and "No real finite-part rows are shipped" in text
    return _res("doc_warns_locked", ok)


def check_T_w_import_session_log_example_dir_exists():
    ok = SESSION_LOG_EXAMPLE_DIR.exists() and SESSION_LOG_EXAMPLE_DIR.is_dir()
    return _res("example_dir_exists", ok, path=str(SESSION_LOG_EXAMPLE_DIR))


def check_T_w_import_session_log_template_file_exists():
    ok = SESSION_LOG_TEMPLATE_PATH.exists() and SESSION_LOG_TEMPLATE_PATH.is_file()
    return _res("template_file_exists", ok, path=str(SESSION_LOG_TEMPLATE_PATH))


def check_T_w_import_session_log_template_not_real():
    data = json.loads(SESSION_LOG_TEMPLATE_PATH.read_text(encoding="utf-8")) if SESSION_LOG_TEMPLATE_PATH.exists() else {}
    ok = data.get("template_only") is True and data.get("not_real_finite_part_evidence") is True and data.get("exports_physical_M_W") is False
    return _res("template_not_real", ok, data=data)


def check_T_w_import_session_log_handoff_version_recorded():
    r = import_session_log_report(promoted_import_session_log_request())
    ok = r["handoff_version"] == REVIEWED_SOURCE_IMPORT_HANDOFF_VERSION and r["handoff_status"] == W_REVIEWED_SOURCE_IMPORT_HANDOFF_STATUS
    return _res("handoff_version_recorded", ok, report=r)


def check_T_w_import_session_log_loader_status_recorded():
    r = import_session_log_report(promoted_import_session_log_request())
    ok = r["loader_status"] == W_PAYLOAD_IMPORT_CLI_STATUS and "loader_report" in r
    return _res("loader_status_recorded", ok, report=r)


def check_T_w_import_session_log_digest_algorithm_fixed_sha256():
    r = import_session_log_report(promoted_import_session_log_request())
    ok = r["payload_digest_algorithm"] == "sha256"
    return _res("digest_algorithm_fixed_sha256", ok, algorithm=r["payload_digest_algorithm"])


def check_T_w_import_session_log_does_not_promote_dryrun_to_real():
    with TemporaryDirectory() as td:
        p = write_synthetic_json_fixture(Path(td) / "payload.json")
        r = import_session_log_report(replace(promoted_import_session_log_request(), payload_path=str(p), ingest_format="json_rows_v1"))
    ok = r["loader_invoked"] and not r["real_payload_claimed"] and not r["real_external_rows_imported"] and not r["real_external_rows_admitted"]
    return _res("does_not_promote_dryrun_to_real", ok, report=r)


def check_T_w_import_session_log_bank_closure():
    r = import_session_log_report(promoted_import_session_log_request())
    ok = (
        r["handoff_validated"]
        and r["session_state"] == "AWAITING_PAYLOAD_FILE"
        and not r["real_external_rows_imported"]
        and not r["real_external_rows_admitted"]
        and not r["component_sum_certified"]
        and not r["covariance_certified"]
        and not r["uncertainty_propagation_certified"]
        and not r["physical_W_export_enabled"]
        and not r["exports_physical_M_W"]
    )
    return _res("bank_closure", ok, total=len(CHECKS), report=r)


CHECKS: Dict[str, Any] = {
    "T_w_import_session_log_status_declared": check_T_w_import_session_log_status_declared,
    "T_w_import_session_log_depends_on_v118_handoff": check_T_w_import_session_log_depends_on_v118_handoff,
    "T_w_import_session_log_states_declared": check_T_w_import_session_log_states_declared,
    "T_w_import_session_log_record_schema_declared": check_T_w_import_session_log_record_schema_declared,
    "T_w_import_session_log_default_no_session": check_T_w_import_session_log_default_no_session,
    "T_w_import_session_log_promoted_awaits_payload": check_T_w_import_session_log_promoted_awaits_payload,
    "T_w_import_session_log_records_json_dryrun_digest": check_T_w_import_session_log_records_json_dryrun_digest,
    "T_w_import_session_log_loader_invoked_only_after_valid_handoff": check_T_w_import_session_log_loader_invoked_only_after_valid_handoff,
    "T_w_import_session_log_missing_payload_fails_closed": check_T_w_import_session_log_missing_payload_fails_closed,
    "T_w_import_session_log_real_flag_does_not_admit_rows": check_T_w_import_session_log_real_flag_does_not_admit_rows,
    "T_w_import_session_log_blocks_physical_export_request": check_T_w_import_session_log_blocks_physical_export_request,
    "T_w_import_session_log_forbidden_tokens_declared": check_T_w_import_session_log_forbidden_tokens_declared,
    "T_w_import_session_log_rejects_forbidden_review_digest_token": check_T_w_import_session_log_rejects_forbidden_review_digest_token,
    "T_w_import_session_log_preserves_export_lock": check_T_w_import_session_log_preserves_export_lock,
    "T_w_import_session_log_no_rows_or_certificates_by_default": check_T_w_import_session_log_no_rows_or_certificates_by_default,
    "T_w_import_session_log_payload_digest_changes_with_file": check_T_w_import_session_log_payload_digest_changes_with_file,
    "T_w_import_session_log_failure_reasons_deduplicated": check_T_w_import_session_log_failure_reasons_deduplicated,
    "T_w_import_session_log_json_serializable": check_T_w_import_session_log_json_serializable,
    "T_w_import_session_log_template_path_declared": check_T_w_import_session_log_template_path_declared,
    "T_w_import_session_log_write_template": check_T_w_import_session_log_write_template,
    "T_w_import_session_log_doc_exists": check_T_w_import_session_log_doc_exists,
    "T_w_import_session_log_doc_warns_locked": check_T_w_import_session_log_doc_warns_locked,
    "T_w_import_session_log_example_dir_exists": check_T_w_import_session_log_example_dir_exists,
    "T_w_import_session_log_template_file_exists": check_T_w_import_session_log_template_file_exists,
    "T_w_import_session_log_template_not_real": check_T_w_import_session_log_template_not_real,
    "T_w_import_session_log_handoff_version_recorded": check_T_w_import_session_log_handoff_version_recorded,
    "T_w_import_session_log_loader_status_recorded": check_T_w_import_session_log_loader_status_recorded,
    "T_w_import_session_log_digest_algorithm_fixed_sha256": check_T_w_import_session_log_digest_algorithm_fixed_sha256,
    "T_w_import_session_log_does_not_promote_dryrun_to_real": check_T_w_import_session_log_does_not_promote_dryrun_to_real,
    "T_w_import_session_log_bank_closure": check_T_w_import_session_log_bank_closure,
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
        "status": "W_TRACE_IMPORT_SESSION_LOG_BANK_PASS" if ok else "W_TRACE_IMPORT_SESSION_LOG_BANK_FAIL",
        "checks": rows,
        "report": import_session_log_report(),
    }
