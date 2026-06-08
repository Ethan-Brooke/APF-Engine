"""W_TRACE release packet validator / operator checklist preflight bank.

v12.3 (2026-05-09 LATER-58): completed release-packet validator above the
v12.2 operator runbook. This module validates a filled release packet before
any W_TRACE reviewed import pipeline can be treated as release-ready. It rejects
template/default packets, missing digests, incomplete checklist attestations,
forbidden W-target tokens, and any attempted physical export override. It does
not ship real finite-part rows, certify sums/covariance, or unlock physical W
export.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple
import json
import re

from apf.w_trace_release_runbook import (
    W_RELEASE_RUNBOOK_STATUS,
    RELEASE_RUNBOOK_VERSION,
    REQUIRED_ARTIFACTS,
    RELEASE_PREDICATES,
    OPERATOR_ACTIONS,
    FORBIDDEN_RELEASE_TOKENS,
    ReleaseRunbookRequest,
    release_runbook_report,
    fully_documented_release_runbook_request,
    check_T_w_release_runbook_bank_closure as _check_v122,
)

W_RELEASE_PACKET_VALIDATOR_STATUS = "P_w_release_packet_validator"
RELEASE_PACKET_VALIDATOR_VERSION = "w_trace_release_packet_validator_v1"
RELEASE_PACKET_VALIDATOR_MODE = "COMPLETED_RELEASE_PACKET_PREFLIGHT__NO_REAL_PAYLOAD_SHIPPED"

REAL_COMPLETED_RELEASE_PACKET_SHIPPED = False
REAL_COMPLETED_RELEASE_PACKET_VALIDATED = False
REAL_PAYLOAD_ROWS_ADMITTED = False
REAL_COMPONENT_SUM_CERTIFIED = False
REAL_COVARIANCE_CERTIFIED = False
REAL_UNCERTAINTY_CERTIFIED = False
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False

ROOT = Path(__file__).resolve().parent.parent
DOC_PATH = ROOT / "W_TRACE_RELEASE_PACKET_VALIDATOR_BANK_v1_0.md"
EXAMPLE_DIR = ROOT / "examples" / "w_trace_release_packet_validator"
TEMPLATE_PATH = EXAMPLE_DIR / "release_packet_preflight_template.json"

REQUIRED_PACKET_FIELDS: Tuple[str, ...] = (
    "packet_id",
    "packet_version",
    "operator_id",
    "reviewer_ids",
    "runbook_version",
    "artifact_state",
    "artifact_digests",
    "predicate_attestations",
    "operator_action_attestations",
    "forbidden_input_audit",
    "export_lock_acknowledgement",
    "release_decision",
    "notes",
)

VALID_RELEASE_DECISIONS: Tuple[str, ...] = (
    "BLOCKED_INCOMPLETE",
    "READY_FOR_EXTERNAL_ROWS_REVIEW",
    "READY_FOR_FINAL_EXPORT_REVIEW",
)

DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")

@dataclass(frozen=True)
class ReleasePacket:
    packet_id: str = "TEMPLATE_RELEASE_PACKET_DO_NOT_USE"
    packet_version: str = RELEASE_PACKET_VALIDATOR_VERSION
    operator_id: str = "TEMPLATE_OPERATOR"
    reviewer_ids: Tuple[str, ...] = ()
    runbook_version: str = RELEASE_RUNBOOK_VERSION
    artifact_state: Mapping[str, bool] | None = None
    artifact_digests: Mapping[str, str] | None = None
    predicate_attestations: Mapping[str, bool] | None = None
    operator_action_attestations: Mapping[str, bool] | None = None
    forbidden_input_audit: bool = False
    export_lock_acknowledgement: bool = False
    release_decision: str = "BLOCKED_INCOMPLETE"
    notes: str = "template only; not real finite-part evidence"


def default_release_packet() -> ReleasePacket:
    return ReleasePacket()


def completed_shape_release_packet() -> ReleasePacket:
    return ReleasePacket(
        packet_id="RELEASE_PACKET_SHAPE_EXAMPLE_0001",
        operator_id="operator_example",
        reviewer_ids=("reviewer_a", "reviewer_b"),
        artifact_state={k: True for k in REQUIRED_ARTIFACTS},
        artifact_digests={k: "sha256:" + ("a" * 64) for k in REQUIRED_ARTIFACTS},
        predicate_attestations={k: True for k in RELEASE_PREDICATES},
        operator_action_attestations={k: True for k in OPERATOR_ACTIONS},
        forbidden_input_audit=True,
        export_lock_acknowledgement=True,
        release_decision="READY_FOR_FINAL_EXPORT_REVIEW",
        notes="shape example only; no real rows shipped",
    )


def _as_dict(packet: ReleasePacket) -> Dict[str, Any]:
    d = asdict(packet)
    d["artifact_state"] = dict(packet.artifact_state or {})
    d["artifact_digests"] = dict(packet.artifact_digests or {})
    d["predicate_attestations"] = dict(packet.predicate_attestations or {})
    d["operator_action_attestations"] = dict(packet.operator_action_attestations or {})
    d["reviewer_ids"] = tuple(packet.reviewer_ids or ())
    return d


def _contains_forbidden_token(text: str) -> bool:
    low = (text or "").lower()
    return any(tok.lower() in low for tok in FORBIDDEN_RELEASE_TOKENS)


def _looks_template(packet: ReleasePacket) -> bool:
    d = _as_dict(packet)
    blob = json.dumps(d, sort_keys=True).lower()
    return "template" in blob or "do_not_use" in blob or "do not use" in blob


def _all_required_true(state: Mapping[str, bool], required: Tuple[str, ...]) -> bool:
    return all(bool(state.get(k, False)) for k in required)


def _all_required_digests(digests: Mapping[str, str]) -> bool:
    return all(isinstance(digests.get(k), str) and bool(DIGEST_RE.match(digests[k])) for k in REQUIRED_ARTIFACTS)


def _to_runbook_request(packet: ReleasePacket) -> ReleaseRunbookRequest:
    state = dict(packet.artifact_state or {})
    return ReleaseRunbookRequest(
        completed_review_packet_json=bool(state.get("completed_review_packet_json", False)),
        review_packet_digest=bool(state.get("review_packet_digest", False)),
        source_candidate_digest=bool(state.get("source_candidate_digest", False)),
        payload_file_uri=bool(state.get("payload_file_uri", False)),
        payload_sha256_digest=bool(state.get("payload_sha256_digest", False)),
        extraction_log_digest=bool(state.get("extraction_log_digest", False)),
        import_session_log_json=bool(state.get("import_session_log_json", False)),
        replay_report_json=bool(state.get("replay_report_json", False)),
        row_bundle_admission_report_json=bool(state.get("row_bundle_admission_report_json", False)),
        component_sum_certificate_json=bool(state.get("component_sum_certificate_json", False)),
        covariance_certificate_json=bool(state.get("covariance_certificate_json", False)),
        uncertainty_propagation_certificate_json=bool(state.get("uncertainty_propagation_certificate_json", False)),
        final_export_readiness_report_json=bool(state.get("final_export_readiness_report_json", False)),
        no_target_observable_consumption=bool((packet.predicate_attestations or {}).get("no_target_observable_consumption", False)),
        physical_export_lock_release_review=bool((packet.predicate_attestations or {}).get("physical_export_lock_release_review", False)),
        notes=packet.notes,
    )


def validate_release_packet(packet: ReleasePacket | None = None) -> Dict[str, Any]:
    packet = packet or default_release_packet()
    d = _as_dict(packet)
    artifacts = dict(packet.artifact_state or {})
    digests = dict(packet.artifact_digests or {})
    predicates = dict(packet.predicate_attestations or {})
    actions = dict(packet.operator_action_attestations or {})
    failure_reasons = []

    missing_packet_fields = tuple(k for k in REQUIRED_PACKET_FIELDS if k not in d)
    missing_artifacts = tuple(k for k in REQUIRED_ARTIFACTS if not artifacts.get(k, False))
    missing_digests = tuple(k for k in REQUIRED_ARTIFACTS if not digests.get(k))
    bad_digests = tuple(k for k, v in digests.items() if k in REQUIRED_ARTIFACTS and not (isinstance(v, str) and DIGEST_RE.match(v)))
    missing_predicates = tuple(k for k in RELEASE_PREDICATES if not predicates.get(k, False))
    missing_actions = tuple(k for k in OPERATOR_ACTIONS if not actions.get(k, False))

    if _looks_template(packet):
        failure_reasons.append("TEMPLATE_OR_DEFAULT_PACKET_REJECTED")
    if packet.runbook_version != RELEASE_RUNBOOK_VERSION:
        failure_reasons.append("RUNBOOK_VERSION_MISMATCH")
    if packet.release_decision not in VALID_RELEASE_DECISIONS:
        failure_reasons.append("INVALID_RELEASE_DECISION")
    if not packet.reviewer_ids or len(set(packet.reviewer_ids)) < 2:
        failure_reasons.append("INSUFFICIENT_INDEPENDENT_REVIEWERS")
    if missing_artifacts:
        failure_reasons.append("MISSING_REQUIRED_ARTIFACTS")
    if missing_digests:
        failure_reasons.append("MISSING_REQUIRED_DIGESTS")
    if bad_digests:
        failure_reasons.append("BAD_DIGEST_FORMAT")
    if missing_predicates:
        failure_reasons.append("MISSING_RELEASE_PREDICATE_ATTESTATIONS")
    if missing_actions:
        failure_reasons.append("MISSING_OPERATOR_ACTION_ATTESTATIONS")
    if not packet.forbidden_input_audit:
        failure_reasons.append("FORBIDDEN_INPUT_AUDIT_NOT_ATTESTED")
    if not packet.export_lock_acknowledgement:
        failure_reasons.append("EXPORT_LOCK_ACKNOWLEDGEMENT_MISSING")
    if _contains_forbidden_token(packet.notes):
        failure_reasons.append("FORBIDDEN_RELEASE_TOKEN_PRESENT")

    runbook = release_runbook_report(_to_runbook_request(packet))
    if runbook.get("failure_reasons"):
        failure_reasons.append("RUNBOOK_DEPENDENCY_FAILURE")

    packet_shape_complete = not missing_packet_fields and not missing_artifacts and not missing_digests and not bad_digests and not missing_predicates and not missing_actions
    packet_validated = bool(packet_shape_complete and not failure_reasons)
    physical_export_allowed = False  # This validator is preflight only; final export lock remains authoritative.
    return {
        "release_packet_validator_status": W_RELEASE_PACKET_VALIDATOR_STATUS,
        "release_packet_validator_version": RELEASE_PACKET_VALIDATOR_VERSION,
        "release_packet_validator_mode": RELEASE_PACKET_VALIDATOR_MODE,
        "upstream_runbook_status": W_RELEASE_RUNBOOK_STATUS,
        "upstream_runbook_version": RELEASE_RUNBOOK_VERSION,
        "required_packet_fields": REQUIRED_PACKET_FIELDS,
        "required_artifacts": REQUIRED_ARTIFACTS,
        "release_predicates": RELEASE_PREDICATES,
        "operator_actions": OPERATOR_ACTIONS,
        "packet_id": packet.packet_id,
        "packet_version": packet.packet_version,
        "release_decision": packet.release_decision,
        "artifact_state": artifacts,
        "artifact_digests": digests,
        "predicate_attestations": predicates,
        "operator_action_attestations": actions,
        "missing_packet_fields": missing_packet_fields,
        "missing_artifacts": missing_artifacts,
        "missing_digests": missing_digests,
        "bad_digests": bad_digests,
        "missing_predicates": missing_predicates,
        "missing_actions": missing_actions,
        "forbidden_input_audit": packet.forbidden_input_audit,
        "export_lock_acknowledgement": packet.export_lock_acknowledgement,
        "runbook_dependency_report": runbook,
        "release_packet_shape_complete": packet_shape_complete,
        "release_packet_validated": packet_validated,
        "real_completed_release_packet_shipped": REAL_COMPLETED_RELEASE_PACKET_SHIPPED,
        "real_completed_release_packet_validated": REAL_COMPLETED_RELEASE_PACKET_VALIDATED and packet_validated,
        "real_payload_rows_admitted": REAL_PAYLOAD_ROWS_ADMITTED,
        "real_component_sum_certified": REAL_COMPONENT_SUM_CERTIFIED,
        "real_covariance_certified": REAL_COVARIANCE_CERTIFIED,
        "real_uncertainty_certified": REAL_UNCERTAINTY_CERTIFIED,
        "physical_W_export_enabled": PHYSICAL_W_EXPORT_ENABLED and physical_export_allowed,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W and physical_export_allowed,
        "physical_export_allowed_by_validator": physical_export_allowed,
        "failure_reasons": tuple(dict.fromkeys(failure_reasons)),
        "locked_by_default": True,
        "terminal_state": "RELEASE_PACKET_PREFLIGHT_VALID_BUT_EXPORT_LOCKED" if packet_validated else "RELEASE_PACKET_PREFLIGHT_BLOCKED",
    }


def write_release_packet_template(path: str | Path = TEMPLATE_PATH) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    packet = default_release_packet()
    report = validate_release_packet(packet)
    report.update({
        "template_only": True,
        "not_real_finite_part_evidence": True,
        "do_not_promote_to_real_release_packet": True,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
    })
    path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return path


def _res(name: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    return {"check": name, "passed": bool(passed), "epistemic": W_RELEASE_PACKET_VALIDATOR_STATUS, **extra}


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed"))


def check_T_w_release_packet_validator_status_declared():
    return _res("status_declared", W_RELEASE_PACKET_VALIDATOR_STATUS == "P_w_release_packet_validator")


def check_T_w_release_packet_validator_depends_on_runbook():
    upstream = _check_v122()
    ok = _passed(upstream) and W_RELEASE_RUNBOOK_STATUS == "P_w_release_runbook"
    return _res("depends_on_runbook", ok, upstream=W_RELEASE_RUNBOOK_STATUS)


def check_T_w_release_packet_validator_required_fields_declared():
    ok = len(REQUIRED_PACKET_FIELDS) == 13 and "artifact_digests" in REQUIRED_PACKET_FIELDS and "export_lock_acknowledgement" in REQUIRED_PACKET_FIELDS
    return _res("required_fields_declared", ok, fields=REQUIRED_PACKET_FIELDS)


def check_T_w_release_packet_validator_required_fields_unique():
    return _res("required_fields_unique", len(set(REQUIRED_PACKET_FIELDS)) == len(REQUIRED_PACKET_FIELDS))


def check_T_w_release_packet_validator_valid_decisions_declared():
    ok = "READY_FOR_FINAL_EXPORT_REVIEW" in VALID_RELEASE_DECISIONS and "BLOCKED_INCOMPLETE" in VALID_RELEASE_DECISIONS
    return _res("valid_decisions_declared", ok, decisions=VALID_RELEASE_DECISIONS)


def check_T_w_release_packet_validator_default_rejected():
    r = validate_release_packet()
    ok = r["release_packet_validated"] is False and "TEMPLATE_OR_DEFAULT_PACKET_REJECTED" in r["failure_reasons"] and r["physical_W_export_enabled"] is False
    return _res("default_rejected", ok, report=r)


def check_T_w_release_packet_validator_completed_shape_still_export_locked():
    r = validate_release_packet(completed_shape_release_packet())
    ok = r["release_packet_shape_complete"] is True and r["physical_W_export_enabled"] is False and r["exports_physical_M_W"] is False
    return _res("completed_shape_still_export_locked", ok, terminal=r["terminal_state"], failures=r["failure_reasons"])


def check_T_w_release_packet_validator_requires_two_reviewers():
    p = completed_shape_release_packet().__class__(**{**_as_dict(completed_shape_release_packet()), "reviewer_ids": ("one",)})
    r = validate_release_packet(p)
    ok = "INSUFFICIENT_INDEPENDENT_REVIEWERS" in r["failure_reasons"]
    return _res("requires_two_reviewers", ok, failures=r["failure_reasons"])


def check_T_w_release_packet_validator_rejects_template_token():
    r = validate_release_packet(ReleasePacket(notes="template only"))
    ok = "TEMPLATE_OR_DEFAULT_PACKET_REJECTED" in r["failure_reasons"]
    return _res("rejects_template_token", ok, failures=r["failure_reasons"])


def check_T_w_release_packet_validator_runbook_version_required():
    p = completed_shape_release_packet().__class__(**{**_as_dict(completed_shape_release_packet()), "runbook_version": "wrong"})
    r = validate_release_packet(p)
    ok = "RUNBOOK_VERSION_MISMATCH" in r["failure_reasons"]
    return _res("runbook_version_required", ok, failures=r["failure_reasons"])


def check_T_w_release_packet_validator_rejects_bad_decision():
    p = completed_shape_release_packet().__class__(**{**_as_dict(completed_shape_release_packet()), "release_decision": "UNLOCK_NOW"})
    r = validate_release_packet(p)
    ok = "INVALID_RELEASE_DECISION" in r["failure_reasons"]
    return _res("rejects_bad_decision", ok, failures=r["failure_reasons"])


def check_T_w_release_packet_validator_reports_missing_artifacts():
    r = validate_release_packet(default_release_packet())
    ok = "MISSING_REQUIRED_ARTIFACTS" in r["failure_reasons"] and len(r["missing_artifacts"]) == len(REQUIRED_ARTIFACTS)
    return _res("reports_missing_artifacts", ok, missing=r["missing_artifacts"])


def check_T_w_release_packet_validator_reports_missing_digests():
    r = validate_release_packet(default_release_packet())
    ok = "MISSING_REQUIRED_DIGESTS" in r["failure_reasons"] and len(r["missing_digests"]) == len(REQUIRED_ARTIFACTS)
    return _res("reports_missing_digests", ok, missing=r["missing_digests"])


def check_T_w_release_packet_validator_bad_digest_rejected():
    p = completed_shape_release_packet().__class__(**{**_as_dict(completed_shape_release_packet()), "artifact_digests": {k: "bad" for k in REQUIRED_ARTIFACTS}})
    r = validate_release_packet(p)
    ok = "BAD_DIGEST_FORMAT" in r["failure_reasons"] and len(r["bad_digests"]) == len(REQUIRED_ARTIFACTS)
    return _res("bad_digest_rejected", ok, bad=r["bad_digests"])


def check_T_w_release_packet_validator_sha256_digest_accepted_shape():
    p = completed_shape_release_packet()
    r = validate_release_packet(p)
    ok = not r["bad_digests"]
    return _res("sha256_digest_accepted_shape", ok)


def check_T_w_release_packet_validator_predicates_required():
    p = completed_shape_release_packet().__class__(**{**_as_dict(completed_shape_release_packet()), "predicate_attestations": {}})
    r = validate_release_packet(p)
    ok = "MISSING_RELEASE_PREDICATE_ATTESTATIONS" in r["failure_reasons"]
    return _res("predicates_required", ok, missing=r["missing_predicates"])


def check_T_w_release_packet_validator_actions_required():
    p = completed_shape_release_packet().__class__(**{**_as_dict(completed_shape_release_packet()), "operator_action_attestations": {}})
    r = validate_release_packet(p)
    ok = "MISSING_OPERATOR_ACTION_ATTESTATIONS" in r["failure_reasons"]
    return _res("actions_required", ok, missing=r["missing_actions"])


def check_T_w_release_packet_validator_forbidden_audit_required():
    p = completed_shape_release_packet().__class__(**{**_as_dict(completed_shape_release_packet()), "forbidden_input_audit": False})
    r = validate_release_packet(p)
    ok = "FORBIDDEN_INPUT_AUDIT_NOT_ATTESTED" in r["failure_reasons"]
    return _res("forbidden_audit_required", ok, failures=r["failure_reasons"])


def check_T_w_release_packet_validator_export_lock_ack_required():
    p = completed_shape_release_packet().__class__(**{**_as_dict(completed_shape_release_packet()), "export_lock_acknowledgement": False})
    r = validate_release_packet(p)
    ok = "EXPORT_LOCK_ACKNOWLEDGEMENT_MISSING" in r["failure_reasons"]
    return _res("export_lock_ack_required", ok, failures=r["failure_reasons"])


def check_T_w_release_packet_validator_observed_w_token_rejected():
    p = completed_shape_release_packet().__class__(**{**_as_dict(completed_shape_release_packet()), "notes": "observed_M_W used"})
    r = validate_release_packet(p)
    ok = "FORBIDDEN_RELEASE_TOKEN_PRESENT" in r["failure_reasons"]
    return _res("observed_w_token_rejected", ok, failures=r["failure_reasons"])


def check_T_w_release_packet_validator_manual_unlock_rejected():
    p = completed_shape_release_packet().__class__(**{**_as_dict(completed_shape_release_packet()), "notes": "manual_export_unlock"})
    r = validate_release_packet(p)
    ok = "FORBIDDEN_RELEASE_TOKEN_PRESENT" in r["failure_reasons"]
    return _res("manual_unlock_rejected", ok, failures=r["failure_reasons"])


def check_T_w_release_packet_validator_runbook_dependency_invoked():
    r = validate_release_packet(completed_shape_release_packet())
    ok = r["runbook_dependency_report"]["release_runbook_status"] == W_RELEASE_RUNBOOK_STATUS
    return _res("runbook_dependency_invoked", ok)


def check_T_w_release_packet_validator_no_physical_export_flags():
    r = validate_release_packet(completed_shape_release_packet())
    ok = r["physical_W_export_enabled"] is False and r["exports_physical_M_W"] is False and r["physical_export_allowed_by_validator"] is False
    return _res("no_physical_export_flags", ok)


def check_T_w_release_packet_validator_real_state_false():
    r = validate_release_packet(completed_shape_release_packet())
    ok = r["real_completed_release_packet_shipped"] is False and r["real_payload_rows_admitted"] is False and r["real_component_sum_certified"] is False
    return _res("real_state_false", ok)


def check_T_w_release_packet_validator_json_serializable():
    try:
        json.dumps(validate_release_packet(), sort_keys=True)
        ok = True
    except TypeError:
        ok = False
    return _res("json_serializable", ok)


def check_T_w_release_packet_validator_template_path_declared():
    ok = TEMPLATE_PATH.name == "release_packet_preflight_template.json"
    return _res("template_path_declared", ok, path=str(TEMPLATE_PATH))


def check_T_w_release_packet_validator_write_template():
    path = write_release_packet_template()
    data = json.loads(path.read_text(encoding="utf-8"))
    ok = path.exists() and data.get("template_only") is True and data.get("not_real_finite_part_evidence") is True
    return _res("write_template", ok, path=str(path))


def check_T_w_release_packet_validator_template_not_real():
    data = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8")) if TEMPLATE_PATH.exists() else {}
    ok = data.get("template_only") is True and data.get("exports_physical_M_W") is False
    return _res("template_not_real", ok)


def check_T_w_release_packet_validator_doc_exists():
    return _res("doc_exists", DOC_PATH.exists(), path=str(DOC_PATH))


def check_T_w_release_packet_validator_doc_warns_locked():
    text = DOC_PATH.read_text(encoding="utf-8") if DOC_PATH.exists() else ""
    ok = "physical W/on-shell export remains OPEN" in text and "template/default packets" in text.lower() and "release packet validator" in text
    return _res("doc_warns_locked", ok, found=len(text))


def check_T_w_release_packet_validator_release_predicates_match_runbook():
    ok = "physical_export_lock_release_review" in RELEASE_PREDICATES and "no_target_observable_consumption" in RELEASE_PREDICATES
    return _res("release_predicates_match_runbook", ok, predicates=RELEASE_PREDICATES)


def check_T_w_release_packet_validator_operator_actions_match_runbook():
    ok = "run_final_export_readiness" in OPERATOR_ACTIONS and "run_payload_import_cli" in OPERATOR_ACTIONS
    return _res("operator_actions_match_runbook", ok, actions=OPERATOR_ACTIONS)


def check_T_w_release_packet_validator_terminal_state_blocked_default():
    r = validate_release_packet()
    ok = r["terminal_state"] == "RELEASE_PACKET_PREFLIGHT_BLOCKED" and r["locked_by_default"] is True
    return _res("terminal_state_blocked_default", ok, terminal=r["terminal_state"])


def check_T_w_release_packet_validator_terminal_state_valid_shape_locked():
    r = validate_release_packet(completed_shape_release_packet())
    ok = r["locked_by_default"] is True and r["physical_W_export_enabled"] is False
    return _res("terminal_state_valid_shape_locked", ok, terminal=r["terminal_state"])


def check_T_w_release_packet_validator_bank_closure():
    rows = [fn() for fn in CHECKS.values() if fn is not check_T_w_release_packet_validator_bank_closure]
    ok = all(_passed(r) for r in rows) and len(rows) == 34
    return _res("bank_closure", ok, checked=len(rows), failed=[r.get("check") for r in rows if not _passed(r)])


CHECKS = {
    "T_w_release_packet_validator_status_declared": check_T_w_release_packet_validator_status_declared,
    "T_w_release_packet_validator_depends_on_runbook": check_T_w_release_packet_validator_depends_on_runbook,
    "T_w_release_packet_validator_required_fields_declared": check_T_w_release_packet_validator_required_fields_declared,
    "T_w_release_packet_validator_required_fields_unique": check_T_w_release_packet_validator_required_fields_unique,
    "T_w_release_packet_validator_valid_decisions_declared": check_T_w_release_packet_validator_valid_decisions_declared,
    "T_w_release_packet_validator_default_rejected": check_T_w_release_packet_validator_default_rejected,
    "T_w_release_packet_validator_completed_shape_still_export_locked": check_T_w_release_packet_validator_completed_shape_still_export_locked,
    "T_w_release_packet_validator_requires_two_reviewers": check_T_w_release_packet_validator_requires_two_reviewers,
    "T_w_release_packet_validator_rejects_template_token": check_T_w_release_packet_validator_rejects_template_token,
    "T_w_release_packet_validator_runbook_version_required": check_T_w_release_packet_validator_runbook_version_required,
    "T_w_release_packet_validator_rejects_bad_decision": check_T_w_release_packet_validator_rejects_bad_decision,
    "T_w_release_packet_validator_reports_missing_artifacts": check_T_w_release_packet_validator_reports_missing_artifacts,
    "T_w_release_packet_validator_reports_missing_digests": check_T_w_release_packet_validator_reports_missing_digests,
    "T_w_release_packet_validator_bad_digest_rejected": check_T_w_release_packet_validator_bad_digest_rejected,
    "T_w_release_packet_validator_sha256_digest_accepted_shape": check_T_w_release_packet_validator_sha256_digest_accepted_shape,
    "T_w_release_packet_validator_predicates_required": check_T_w_release_packet_validator_predicates_required,
    "T_w_release_packet_validator_actions_required": check_T_w_release_packet_validator_actions_required,
    "T_w_release_packet_validator_forbidden_audit_required": check_T_w_release_packet_validator_forbidden_audit_required,
    "T_w_release_packet_validator_export_lock_ack_required": check_T_w_release_packet_validator_export_lock_ack_required,
    "T_w_release_packet_validator_observed_w_token_rejected": check_T_w_release_packet_validator_observed_w_token_rejected,
    "T_w_release_packet_validator_manual_unlock_rejected": check_T_w_release_packet_validator_manual_unlock_rejected,
    "T_w_release_packet_validator_runbook_dependency_invoked": check_T_w_release_packet_validator_runbook_dependency_invoked,
    "T_w_release_packet_validator_no_physical_export_flags": check_T_w_release_packet_validator_no_physical_export_flags,
    "T_w_release_packet_validator_real_state_false": check_T_w_release_packet_validator_real_state_false,
    "T_w_release_packet_validator_json_serializable": check_T_w_release_packet_validator_json_serializable,
    "T_w_release_packet_validator_template_path_declared": check_T_w_release_packet_validator_template_path_declared,
    "T_w_release_packet_validator_write_template": check_T_w_release_packet_validator_write_template,
    "T_w_release_packet_validator_template_not_real": check_T_w_release_packet_validator_template_not_real,
    "T_w_release_packet_validator_doc_exists": check_T_w_release_packet_validator_doc_exists,
    "T_w_release_packet_validator_doc_warns_locked": check_T_w_release_packet_validator_doc_warns_locked,
    "T_w_release_packet_validator_release_predicates_match_runbook": check_T_w_release_packet_validator_release_predicates_match_runbook,
    "T_w_release_packet_validator_operator_actions_match_runbook": check_T_w_release_packet_validator_operator_actions_match_runbook,
    "T_w_release_packet_validator_terminal_state_blocked_default": check_T_w_release_packet_validator_terminal_state_blocked_default,
    "T_w_release_packet_validator_terminal_state_valid_shape_locked": check_T_w_release_packet_validator_terminal_state_valid_shape_locked,
    "T_w_release_packet_validator_bank_closure": check_T_w_release_packet_validator_bank_closure,
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
        "status": "W_TRACE_RELEASE_PACKET_VALIDATOR_BANK_PASS" if ok else "W_TRACE_RELEASE_PACKET_VALIDATOR_BANK_FAIL",
        "checks": rows,
        "report": validate_release_packet(),
    }
