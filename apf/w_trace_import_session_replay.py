"""W_TRACE import-session replay / reproducibility validator bank.

v12.0 (2026-05-09 LATER-55): reproducibility layer above the
v11.9 reviewed-payload import session log. This module does not ship or
admit real finite-part rows and does not unlock physical W export. It banks
the replay contract for future reviewed payload import sessions: session-log
schema, digest recomputation, replay status, mismatch/failure certificates,
loader-status preservation, and anti-smuggling/export-lock invariants.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, replace
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Dict, Mapping, Tuple
import hashlib
import json

from apf.w_trace_import_session_log import (
    W_IMPORT_SESSION_LOG_STATUS,
    IMPORT_SESSION_LOG_VERSION,
    ImportSessionLogRequest,
    promoted_import_session_log_request,
    import_session_log_report,
    write_session_log_template,
    check_T_w_import_session_log_bank_closure as _check_v119,
)
from apf.w_trace_payload_import_cli import write_synthetic_json_fixture
from apf.w_trace_final_export_readiness import readiness_report

W_IMPORT_SESSION_REPLAY_STATUS = "P_w_import_session_replay_validator"
IMPORT_SESSION_REPLAY_VERSION = "w_trace_import_session_replay_v1"
IMPORT_SESSION_REPLAY_MODE = "REPLAY_REPRODUCIBILITY_VALIDATOR__NO_REAL_PAYLOAD_SHIPPED"

REAL_REPLAY_SESSION_SHIPPED = False
REAL_REPLAY_SESSION_VALIDATED = False
REAL_EXTERNAL_ROWS_IMPORTED = False
REAL_EXTERNAL_ROWS_ADMITTED = False
COMPONENT_SUM_CERTIFIED = False
COVARIANCE_CERTIFIED = False
UNCERTAINTY_PROPAGATION_CERTIFIED = False
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False

ROOT = Path(__file__).resolve().parent.parent
REPLAY_DOC_PATH = ROOT / "W_TRACE_IMPORT_SESSION_REPLAY_BANK_v1_0.md"
REPLAY_EXAMPLE_DIR = ROOT / "examples" / "w_trace_import_session_replay"
REPLAY_TEMPLATE_PATH = REPLAY_EXAMPLE_DIR / "import_session_replay_template.json"

REPLAY_STATES: Tuple[str, ...] = (
    "NO_REPLAY_SESSION",
    "SESSION_LOG_NOT_PROMOTED",
    "PAYLOAD_MISSING",
    "DIGEST_MISMATCH",
    "REPLAYABLE_DRYRUN",
    "REAL_PAYLOAD_REPLAY_RECORDED_NOT_ADMITTED",
    "BLOCKED_PHYSICAL_EXPORT_REQUEST",
)

REQUIRED_REPLAY_FIELDS: Tuple[str, ...] = (
    "replay_id",
    "replay_version",
    "replay_state",
    "source_session_status",
    "source_session_version",
    "source_session_id",
    "source_payload_digest",
    "recomputed_payload_digest",
    "payload_digest_algorithm",
    "digest_matches_session_log",
    "session_loader_invoked",
    "session_loader_passed",
    "replay_loader_invoked",
    "replay_loader_passed",
    "session_failure_reasons",
    "replay_failure_reasons",
    "real_payload_replay_claimed",
    "real_external_rows_imported",
    "real_external_rows_admitted",
    "component_sum_certified",
    "covariance_certified",
    "uncertainty_propagation_certified",
    "physical_W_export_enabled",
    "exports_physical_M_W",
)

FORBIDDEN_REPLAY_TOKENS: Tuple[str, ...] = (
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
class ImportSessionReplayRequest:
    replay_id: str = "UNSET"
    session_request: ImportSessionLogRequest | None = None
    payload_path: str | None = None
    expected_payload_digest: str | None = None
    recompute_digest: bool = True
    real_payload_replay_claimed: bool = False
    request_physical_export: bool = False


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def _res(name: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    return {"passed": bool(passed), "status": "PASS" if passed else "FAIL", "tier": 4, "epistemic": W_IMPORT_SESSION_REPLAY_STATUS, "check": name, **extra}


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


def _contains_forbidden_token(obj: Any) -> bool:
    hits = []
    def walk(x: Any) -> None:
        if isinstance(x, str):
            hits.extend(tok for tok in FORBIDDEN_REPLAY_TOKENS if tok in x)
        elif isinstance(x, Mapping):
            for v in x.values():
                walk(v)
        elif isinstance(x, (list, tuple, set)):
            for v in x:
                walk(v)
    walk(obj)
    return bool(hits)


def default_import_session_replay_request() -> ImportSessionReplayRequest:
    return ImportSessionReplayRequest(replay_id="NO_REPLAY_SESSION", session_request=None)


def promoted_import_session_replay_request() -> ImportSessionReplayRequest:
    return ImportSessionReplayRequest(
        replay_id="reviewed-source-replay-0001",
        session_request=promoted_import_session_log_request(),
        payload_path=None,
        expected_payload_digest=None,
        recompute_digest=True,
        real_payload_replay_claimed=False,
        request_physical_export=False,
    )


def _replay_state(session_report: Mapping[str, Any], request: ImportSessionReplayRequest, recomputed_digest: str, digest_match: bool) -> str:
    if request.request_physical_export:
        return "BLOCKED_PHYSICAL_EXPORT_REQUEST"
    if request.session_request is None:
        return "NO_REPLAY_SESSION"
    if session_report.get("session_id") in {"", "UNSET", "NO_SESSION"}:
        return "SESSION_LOG_NOT_PROMOTED"
    if recomputed_digest in {"NO_PAYLOAD_FILE", "PAYLOAD_FILE_MISSING"}:
        return "PAYLOAD_MISSING"
    if not digest_match:
        return "DIGEST_MISMATCH"
    if request.real_payload_replay_claimed:
        return "REAL_PAYLOAD_REPLAY_RECORDED_NOT_ADMITTED"
    return "REPLAYABLE_DRYRUN"


def import_session_replay_report(request: ImportSessionReplayRequest | Mapping[str, Any] | None = None) -> Dict[str, Any]:
    if request is None:
        req = default_import_session_replay_request()
    elif isinstance(request, ImportSessionReplayRequest):
        req = request
    else:
        req = ImportSessionReplayRequest(**dict(request))

    session_req = req.session_request
    if session_req is not None and req.payload_path is not None:
        session_req = replace(session_req, payload_path=req.payload_path, ingest_format="json_rows_v1", real_payload_claimed=req.real_payload_replay_claimed)
    if session_req is not None and req.request_physical_export:
        session_req = replace(session_req, request_physical_export=True)

    session_report = import_session_log_report(session_req)
    source_digest = req.expected_payload_digest or session_report.get("payload_digest", "NO_SESSION_DIGEST")
    recomputed_digest = _sha256_file(req.payload_path) if req.recompute_digest else "RECOMPUTE_DISABLED"
    digest_match = bool(recomputed_digest not in {"NO_PAYLOAD_FILE", "PAYLOAD_FILE_MISSING", "RECOMPUTE_DISABLED"} and recomputed_digest == source_digest)
    ready = readiness_report(physical_export_requested=False)

    failures = []
    failures.extend(str(x) for x in session_report.get("failure_reasons", ()))
    if req.replay_id in {"", "UNSET", "NO_REPLAY_SESSION"}:
        failures.append("REPLAY_ID_NOT_PROMOTED")
    if req.session_request is None:
        failures.append("NO_SESSION_LOG_SUPPLIED")
    if recomputed_digest == "NO_PAYLOAD_FILE":
        failures.append("NO_PAYLOAD_FILE_SUPPLIED_FOR_REPLAY")
    if recomputed_digest == "PAYLOAD_FILE_MISSING":
        failures.append("REPLAY_PAYLOAD_FILE_MISSING")
    if recomputed_digest == "RECOMPUTE_DISABLED":
        failures.append("REPLAY_DIGEST_RECOMPUTE_DISABLED")
    if source_digest in {"NO_PAYLOAD_FILE", "PAYLOAD_FILE_MISSING", "NO_SESSION_DIGEST"}:
        failures.append("SESSION_DIGEST_NOT_REPLAYABLE")
    if recomputed_digest not in {"NO_PAYLOAD_FILE", "PAYLOAD_FILE_MISSING", "RECOMPUTE_DISABLED"} and source_digest not in {"NO_PAYLOAD_FILE", "PAYLOAD_FILE_MISSING", "NO_SESSION_DIGEST"} and recomputed_digest != source_digest:
        failures.append("REPLAY_DIGEST_MISMATCH")
    if req.request_physical_export:
        failures.append("PHYSICAL_W_EXPORT_REQUEST_BLOCKED_BY_REPLAY")
    if _contains_forbidden_token(asdict(req)):
        failures.append("FORBIDDEN_REPLAY_TOKEN_PRESENT")

    state = _replay_state(session_report, req, recomputed_digest, digest_match)
    return {
        "status": W_IMPORT_SESSION_REPLAY_STATUS,
        "version": IMPORT_SESSION_REPLAY_VERSION,
        "mode": IMPORT_SESSION_REPLAY_MODE,
        "replay_states": REPLAY_STATES,
        "replay_id": req.replay_id,
        "replay_version": IMPORT_SESSION_REPLAY_VERSION,
        "replay_state": state,
        "source_session_status": W_IMPORT_SESSION_LOG_STATUS,
        "source_session_version": IMPORT_SESSION_LOG_VERSION,
        "source_session_id": session_report.get("session_id"),
        "source_session_report": session_report,
        "source_payload_digest": source_digest,
        "recomputed_payload_digest": recomputed_digest,
        "payload_digest_algorithm": "sha256",
        "digest_matches_session_log": digest_match,
        "session_loader_invoked": bool(session_report.get("loader_invoked")),
        "session_loader_passed": bool(session_report.get("loader_passed")),
        "replay_loader_invoked": bool(digest_match and session_report.get("loader_invoked")),
        "replay_loader_passed": bool(digest_match and session_report.get("loader_passed")),
        "session_failure_reasons": tuple(session_report.get("failure_reasons", ())),
        "replay_failure_reasons": tuple(dict.fromkeys(failures)),
        "real_payload_replay_claimed": bool(req.real_payload_replay_claimed),
        "real_replay_session_shipped": REAL_REPLAY_SESSION_SHIPPED,
        "real_replay_session_validated": REAL_REPLAY_SESSION_VALIDATED,
        "real_external_rows_imported": REAL_EXTERNAL_ROWS_IMPORTED,
        "real_external_rows_admitted": REAL_EXTERNAL_ROWS_ADMITTED,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "covariance_certified": COVARIANCE_CERTIFIED,
        "uncertainty_propagation_certified": UNCERTAINTY_PROPAGATION_CERTIFIED,
        "physical_W_export_enabled": PHYSICAL_W_EXPORT_ENABLED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "readiness_locked": not ready["physical_W_export_ready"] and not ready["physical_W_export_enabled"],
        "forbidden_replay_tokens": FORBIDDEN_REPLAY_TOKENS,
        "forbidden_token_present": _contains_forbidden_token(asdict(req)),
        "replay_doc_path": str(REPLAY_DOC_PATH),
        "replay_example_dir": str(REPLAY_EXAMPLE_DIR),
        "replay_template_path": str(REPLAY_TEMPLATE_PATH),
    }


def write_replay_template(path: str | Path = REPLAY_TEMPLATE_PATH) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "template_only": True,
        "not_real_finite_part_evidence": True,
        "status": W_IMPORT_SESSION_REPLAY_STATUS,
        "version": IMPORT_SESSION_REPLAY_VERSION,
        "replay_id": "REPLACE_WITH_REPLAY_ID",
        "source_session_id": "REPLACE_WITH_SESSION_ID",
        "source_payload_digest": "sha256:<payload-digest-from-session-log>",
        "recompute_digest": True,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
    }
    p.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return p


def _dryrun_replay_request_with_payload(tmp_path: Path, mutate_expected: bool = False) -> ImportSessionReplayRequest:
    p = write_synthetic_json_fixture(tmp_path / "payload.json")
    digest = _sha256_file(str(p))
    expected = ("0" * 64) if mutate_expected else digest
    session_req = replace(promoted_import_session_log_request(), payload_path=str(p), ingest_format="json_rows_v1")
    return ImportSessionReplayRequest(
        replay_id="reviewed-source-replay-0001",
        session_request=session_req,
        payload_path=str(p),
        expected_payload_digest=expected,
        recompute_digest=True,
        real_payload_replay_claimed=False,
        request_physical_export=False,
    )

# Checks

def check_T_w_import_session_replay_status_declared():
    r = import_session_replay_report()
    return _res("status_declared", r["status"] == W_IMPORT_SESSION_REPLAY_STATUS and r["version"] == IMPORT_SESSION_REPLAY_VERSION, report=r)

def check_T_w_import_session_replay_depends_on_v119_log():
    r = _check_v119()
    return _res("depends_on_v119_log", _passed(r), upstream=r)

def check_T_w_import_session_replay_states_declared():
    ok = set(REPLAY_STATES) >= {"NO_REPLAY_SESSION", "REPLAYABLE_DRYRUN", "DIGEST_MISMATCH", "BLOCKED_PHYSICAL_EXPORT_REQUEST"}
    return _res("states_declared", ok, states=REPLAY_STATES)

def check_T_w_import_session_replay_record_schema_declared():
    r = import_session_replay_report(promoted_import_session_replay_request())
    missing = [f for f in REQUIRED_REPLAY_FIELDS if f not in r]
    return _res("record_schema_declared", not missing, missing=missing)

def check_T_w_import_session_replay_default_no_session():
    r = import_session_replay_report()
    ok = r["replay_state"] == "NO_REPLAY_SESSION" and not r["replay_loader_invoked"]
    return _res("default_no_session", ok, report=r)

def check_T_w_import_session_replay_promoted_without_payload_missing():
    r = import_session_replay_report(promoted_import_session_replay_request())
    ok = r["replay_state"] == "PAYLOAD_MISSING" and "NO_PAYLOAD_FILE_SUPPLIED_FOR_REPLAY" in r["replay_failure_reasons"]
    return _res("promoted_without_payload_missing", ok, report=r)

def check_T_w_import_session_replay_digest_recomputed_sha256():
    with TemporaryDirectory() as td:
        r = import_session_replay_report(_dryrun_replay_request_with_payload(Path(td)))
    ok = len(r["recomputed_payload_digest"]) == 64 and r["payload_digest_algorithm"] == "sha256"
    return _res("digest_recomputed_sha256", ok, digest=r["recomputed_payload_digest"])

def check_T_w_import_session_replay_digest_match_yields_dryrun_replayable():
    with TemporaryDirectory() as td:
        r = import_session_replay_report(_dryrun_replay_request_with_payload(Path(td)))
    ok = r["digest_matches_session_log"] and r["replay_state"] == "REPLAYABLE_DRYRUN"
    return _res("digest_match_yields_dryrun_replayable", ok, report=r)

def check_T_w_import_session_replay_digest_mismatch_fails_closed():
    with TemporaryDirectory() as td:
        r = import_session_replay_report(_dryrun_replay_request_with_payload(Path(td), mutate_expected=True))
    ok = r["replay_state"] == "DIGEST_MISMATCH" and "REPLAY_DIGEST_MISMATCH" in r["replay_failure_reasons"] and not r["real_external_rows_admitted"]
    return _res("digest_mismatch_fails_closed", ok, report=r)

def check_T_w_import_session_replay_missing_file_fails_closed():
    req = replace(promoted_import_session_replay_request(), payload_path="/no/such/payload.json", expected_payload_digest="0"*64)
    r = import_session_replay_report(req)
    ok = r["replay_state"] == "PAYLOAD_MISSING" and "REPLAY_PAYLOAD_FILE_MISSING" in r["replay_failure_reasons"]
    return _res("missing_file_fails_closed", ok, report=r)

def check_T_w_import_session_replay_recompute_required():
    with TemporaryDirectory() as td:
        req = replace(_dryrun_replay_request_with_payload(Path(td)), recompute_digest=False)
        r = import_session_replay_report(req)
    ok = "REPLAY_DIGEST_RECOMPUTE_DISABLED" in r["replay_failure_reasons"] and r["replay_state"] == "DIGEST_MISMATCH"
    return _res("recompute_required", ok, report=r)

def check_T_w_import_session_replay_loader_preserved_only_on_digest_match():
    with TemporaryDirectory() as td:
        good = import_session_replay_report(_dryrun_replay_request_with_payload(Path(td)))
    with TemporaryDirectory() as td:
        bad = import_session_replay_report(_dryrun_replay_request_with_payload(Path(td), mutate_expected=True))
    ok = good["replay_loader_invoked"] and not bad["replay_loader_invoked"]
    return _res("loader_preserved_only_on_digest_match", ok, good=good["replay_state"], bad=bad["replay_state"])

def check_T_w_import_session_replay_real_flag_does_not_admit_rows():
    with TemporaryDirectory() as td:
        req = replace(_dryrun_replay_request_with_payload(Path(td)), real_payload_replay_claimed=True)
        r = import_session_replay_report(req)
    ok = r["replay_state"] == "REAL_PAYLOAD_REPLAY_RECORDED_NOT_ADMITTED" and not r["real_external_rows_admitted"]
    return _res("real_flag_does_not_admit_rows", ok, report=r)

def check_T_w_import_session_replay_blocks_physical_export_request():
    with TemporaryDirectory() as td:
        req = replace(_dryrun_replay_request_with_payload(Path(td)), request_physical_export=True)
        r = import_session_replay_report(req)
    ok = r["replay_state"] == "BLOCKED_PHYSICAL_EXPORT_REQUEST" and "PHYSICAL_W_EXPORT_REQUEST_BLOCKED_BY_REPLAY" in r["replay_failure_reasons"] and not r["exports_physical_M_W"]
    return _res("blocks_physical_export_request", ok, report=r)

def check_T_w_import_session_replay_forbidden_tokens_declared():
    ok = "observed_M_W" in FORBIDDEN_REPLAY_TOKENS and "APF_ANCHOR_DELTA_R_TARGET" in FORBIDDEN_REPLAY_TOKENS
    return _res("forbidden_tokens_declared", ok, tokens=FORBIDDEN_REPLAY_TOKENS)

def check_T_w_import_session_replay_rejects_forbidden_expected_digest_token():
    req = replace(promoted_import_session_replay_request(), expected_payload_digest="sha256:observed_M_W")
    r = import_session_replay_report(req)
    ok = r["forbidden_token_present"] and "FORBIDDEN_REPLAY_TOKEN_PRESENT" in r["replay_failure_reasons"]
    return _res("rejects_forbidden_expected_digest_token", ok, report=r)

def check_T_w_import_session_replay_preserves_export_lock():
    r = import_session_replay_report(promoted_import_session_replay_request())
    ok = r["readiness_locked"] and not r["physical_W_export_enabled"] and not r["exports_physical_M_W"]
    return _res("preserves_export_lock", ok, report=r)

def check_T_w_import_session_replay_no_rows_or_certificates_by_default():
    r = import_session_replay_report(promoted_import_session_replay_request())
    ok = not any(r[k] for k in ("real_external_rows_imported", "real_external_rows_admitted", "component_sum_certified", "covariance_certified", "uncertainty_propagation_certified"))
    return _res("no_rows_or_certificates_by_default", ok, report=r)

def check_T_w_import_session_replay_failure_reasons_deduplicated():
    r = import_session_replay_report(default_import_session_replay_request())
    ok = len(r["replay_failure_reasons"]) == len(set(r["replay_failure_reasons"]))
    return _res("failure_reasons_deduplicated", ok, reasons=r["replay_failure_reasons"])

def check_T_w_import_session_replay_json_serializable():
    text = json.dumps(import_session_replay_report(promoted_import_session_replay_request()), sort_keys=True, default=str)
    ok = W_IMPORT_SESSION_REPLAY_STATUS in text and IMPORT_SESSION_REPLAY_VERSION in text
    return _res("json_serializable", ok, length=len(text))

def check_T_w_import_session_replay_template_path_declared():
    ok = REPLAY_TEMPLATE_PATH.name == "import_session_replay_template.json" and REPLAY_EXAMPLE_DIR.name == "w_trace_import_session_replay"
    return _res("template_path_declared", ok, path=str(REPLAY_TEMPLATE_PATH))

def check_T_w_import_session_replay_write_template():
    with TemporaryDirectory() as td:
        p = write_replay_template(Path(td) / "template.json")
        data = json.loads(p.read_text())
    ok = data["template_only"] and data["not_real_finite_part_evidence"] and not data["physical_W_export_enabled"]
    return _res("write_template", ok, data=data)

def check_T_w_import_session_replay_doc_exists():
    return _res("doc_exists", REPLAY_DOC_PATH.exists(), path=str(REPLAY_DOC_PATH))

def check_T_w_import_session_replay_doc_warns_locked():
    text = REPLAY_DOC_PATH.read_text(encoding="utf-8") if REPLAY_DOC_PATH.exists() else ""
    ok = "physical W/on-shell export remains OPEN" in text and "replay" in text.lower()
    return _res("doc_warns_locked", ok, found=len(text))

def check_T_w_import_session_replay_example_dir_exists():
    return _res("example_dir_exists", REPLAY_EXAMPLE_DIR.exists(), path=str(REPLAY_EXAMPLE_DIR))

def check_T_w_import_session_replay_template_file_exists():
    return _res("template_file_exists", REPLAY_TEMPLATE_PATH.exists(), path=str(REPLAY_TEMPLATE_PATH))

def check_T_w_import_session_replay_template_not_real():
    data = json.loads(REPLAY_TEMPLATE_PATH.read_text(encoding="utf-8")) if REPLAY_TEMPLATE_PATH.exists() else {}
    ok = data.get("template_only") is True and data.get("not_real_finite_part_evidence") is True and data.get("exports_physical_M_W") is False
    return _res("template_not_real", ok, data=data)

def check_T_w_import_session_replay_source_session_version_recorded():
    r = import_session_replay_report(promoted_import_session_replay_request())
    ok = r["source_session_version"] == IMPORT_SESSION_LOG_VERSION and r["source_session_status"] == W_IMPORT_SESSION_LOG_STATUS
    return _res("source_session_version_recorded", ok, report=r)

def check_T_w_import_session_replay_digest_algorithm_fixed_sha256():
    r = import_session_replay_report(promoted_import_session_replay_request())
    ok = r["payload_digest_algorithm"] == "sha256"
    return _res("digest_algorithm_fixed_sha256", ok, algorithm=r["payload_digest_algorithm"])

def check_T_w_import_session_replay_does_not_promote_dryrun_to_real():
    with TemporaryDirectory() as td:
        r = import_session_replay_report(_dryrun_replay_request_with_payload(Path(td)))
    ok = r["replay_state"] == "REPLAYABLE_DRYRUN" and not r["real_external_rows_imported"] and not r["real_replay_session_validated"]
    return _res("does_not_promote_dryrun_to_real", ok, report=r)

def check_T_w_import_session_replay_bank_closure():
    rows = [fn() for fn in CHECKS.values() if fn is not check_T_w_import_session_replay_bank_closure]
    ok = all(_passed(r) for r in rows) and len(rows) == 30
    return _res("bank_closure", ok, checked=len(rows), failed=[r.get("check") for r in rows if not _passed(r)])

CHECKS = {
    "T_w_import_session_replay_status_declared": check_T_w_import_session_replay_status_declared,
    "T_w_import_session_replay_depends_on_v119_log": check_T_w_import_session_replay_depends_on_v119_log,
    "T_w_import_session_replay_states_declared": check_T_w_import_session_replay_states_declared,
    "T_w_import_session_replay_record_schema_declared": check_T_w_import_session_replay_record_schema_declared,
    "T_w_import_session_replay_default_no_session": check_T_w_import_session_replay_default_no_session,
    "T_w_import_session_replay_promoted_without_payload_missing": check_T_w_import_session_replay_promoted_without_payload_missing,
    "T_w_import_session_replay_digest_recomputed_sha256": check_T_w_import_session_replay_digest_recomputed_sha256,
    "T_w_import_session_replay_digest_match_yields_dryrun_replayable": check_T_w_import_session_replay_digest_match_yields_dryrun_replayable,
    "T_w_import_session_replay_digest_mismatch_fails_closed": check_T_w_import_session_replay_digest_mismatch_fails_closed,
    "T_w_import_session_replay_missing_file_fails_closed": check_T_w_import_session_replay_missing_file_fails_closed,
    "T_w_import_session_replay_recompute_required": check_T_w_import_session_replay_recompute_required,
    "T_w_import_session_replay_loader_preserved_only_on_digest_match": check_T_w_import_session_replay_loader_preserved_only_on_digest_match,
    "T_w_import_session_replay_real_flag_does_not_admit_rows": check_T_w_import_session_replay_real_flag_does_not_admit_rows,
    "T_w_import_session_replay_blocks_physical_export_request": check_T_w_import_session_replay_blocks_physical_export_request,
    "T_w_import_session_replay_forbidden_tokens_declared": check_T_w_import_session_replay_forbidden_tokens_declared,
    "T_w_import_session_replay_rejects_forbidden_expected_digest_token": check_T_w_import_session_replay_rejects_forbidden_expected_digest_token,
    "T_w_import_session_replay_preserves_export_lock": check_T_w_import_session_replay_preserves_export_lock,
    "T_w_import_session_replay_no_rows_or_certificates_by_default": check_T_w_import_session_replay_no_rows_or_certificates_by_default,
    "T_w_import_session_replay_failure_reasons_deduplicated": check_T_w_import_session_replay_failure_reasons_deduplicated,
    "T_w_import_session_replay_json_serializable": check_T_w_import_session_replay_json_serializable,
    "T_w_import_session_replay_template_path_declared": check_T_w_import_session_replay_template_path_declared,
    "T_w_import_session_replay_write_template": check_T_w_import_session_replay_write_template,
    "T_w_import_session_replay_doc_exists": check_T_w_import_session_replay_doc_exists,
    "T_w_import_session_replay_doc_warns_locked": check_T_w_import_session_replay_doc_warns_locked,
    "T_w_import_session_replay_example_dir_exists": check_T_w_import_session_replay_example_dir_exists,
    "T_w_import_session_replay_template_file_exists": check_T_w_import_session_replay_template_file_exists,
    "T_w_import_session_replay_template_not_real": check_T_w_import_session_replay_template_not_real,
    "T_w_import_session_replay_source_session_version_recorded": check_T_w_import_session_replay_source_session_version_recorded,
    "T_w_import_session_replay_digest_algorithm_fixed_sha256": check_T_w_import_session_replay_digest_algorithm_fixed_sha256,
    "T_w_import_session_replay_does_not_promote_dryrun_to_real": check_T_w_import_session_replay_does_not_promote_dryrun_to_real,
    "T_w_import_session_replay_bank_closure": check_T_w_import_session_replay_bank_closure,
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
        "status": "W_TRACE_IMPORT_SESSION_REPLAY_BANK_PASS" if ok else "W_TRACE_IMPORT_SESSION_REPLAY_BANK_FAIL",
        "checks": rows,
        "report": import_session_replay_report(),
    }
