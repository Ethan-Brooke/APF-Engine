"""W_TRACE reviewed-pipeline release checklist / operator runbook bank.

v12.2 (2026-05-09 LATER-57): terminal operator-facing runbook above the
end-to-end reviewed import pipeline manifest. This module does not ship real
finite-part rows, admit payload rows, certify a component sum, certify
covariance, or unlock physical W export. It banks the release checklist and
operator runbook that tells a future operator exactly which artifacts must be
present before any reviewed W payload pipeline can move from locked to
releasable.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple
import json

from apf.w_trace_e2e_import_pipeline_manifest import (
    W_E2E_IMPORT_PIPELINE_MANIFEST_STATUS,
    E2E_IMPORT_PIPELINE_MANIFEST_VERSION,
    PIPELINE_STAGE_ORDER,
    REQUIRED_MANIFEST_FIELDS,
    FORBIDDEN_MANIFEST_TOKENS,
    e2e_import_pipeline_manifest_report,
    check_T_w_e2e_pipeline_manifest_bank_closure as _check_v121,
)
from apf.w_trace_final_export_readiness import readiness_report

W_RELEASE_RUNBOOK_STATUS = "P_w_release_runbook"
RELEASE_RUNBOOK_VERSION = "w_trace_release_runbook_v1"
RELEASE_RUNBOOK_MODE = "OPERATOR_RELEASE_CHECKLIST__NO_REAL_PAYLOAD_SHIPPED"

REAL_RELEASE_PACKET_SHIPPED = False
REAL_RELEASE_PACKET_VALIDATED = False
REAL_PAYLOAD_ROWS_ADMITTED = False
REAL_COMPONENT_SUM_CERTIFIED = False
REAL_COVARIANCE_CERTIFIED = False
REAL_UNCERTAINTY_CERTIFIED = False
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False

ROOT = Path(__file__).resolve().parent.parent
RUNBOOK_DOC_PATH = ROOT / "W_TRACE_RELEASE_RUNBOOK_BANK_v1_0.md"
RUNBOOK_EXAMPLE_DIR = ROOT / "examples" / "w_trace_release_runbook"
RUNBOOK_TEMPLATE_PATH = RUNBOOK_EXAMPLE_DIR / "release_runbook_template.json"
RUNBOOK_CHECKLIST_PATH = RUNBOOK_EXAMPLE_DIR / "release_checklist_template.md"

RUNBOOK_PHASES: Tuple[str, ...] = (
    "source_candidate_selected",
    "review_packet_completed",
    "review_packet_validated",
    "reviewed_source_handoff_completed",
    "payload_file_loaded",
    "import_session_logged",
    "import_session_replayed",
    "row_bundle_admitted",
    "component_sum_certified",
    "covariance_certified",
    "uncertainty_propagation_certified",
    "final_export_readiness_reviewed",
)

REQUIRED_ARTIFACTS: Tuple[str, ...] = (
    "completed_review_packet_json",
    "review_packet_digest",
    "source_candidate_digest",
    "payload_file_uri",
    "payload_sha256_digest",
    "extraction_log_digest",
    "import_session_log_json",
    "replay_report_json",
    "row_bundle_admission_report_json",
    "component_sum_certificate_json",
    "covariance_certificate_json",
    "uncertainty_propagation_certificate_json",
    "final_export_readiness_report_json",
)

RELEASE_PREDICATES: Tuple[str, ...] = (
    "validated_review_packet",
    "reviewed_source_handoff",
    "replayed_import_session",
    "admitted_real_rows",
    "certified_component_sum",
    "certified_covariance",
    "certified_uncertainty_propagation",
    "counterterm_convention_certified",
    "no_target_observable_consumption",
    "physical_export_lock_release_review",
)

OPERATOR_ACTIONS: Tuple[str, ...] = (
    "collect_artifacts",
    "compute_and_record_digests",
    "run_review_packet_validator",
    "run_reviewed_source_handoff",
    "run_payload_import_cli",
    "write_import_session_log",
    "replay_import_session",
    "run_row_bundle_admission",
    "run_component_sum_certificate",
    "run_covariance_certificate",
    "run_uncertainty_propagation",
    "run_final_export_readiness",
)

FORBIDDEN_RELEASE_TOKENS: Tuple[str, ...] = tuple(FORBIDDEN_MANIFEST_TOKENS) + (
    "observed_W_mass_input",
    "world_average_W_mass_input",
    "release_override",
    "manual_export_unlock",
)

@dataclass(frozen=True)
class ReleaseRunbookRequest:
    completed_review_packet_json: bool = False
    review_packet_digest: bool = False
    source_candidate_digest: bool = False
    payload_file_uri: bool = False
    payload_sha256_digest: bool = False
    extraction_log_digest: bool = False
    import_session_log_json: bool = False
    replay_report_json: bool = False
    row_bundle_admission_report_json: bool = False
    component_sum_certificate_json: bool = False
    covariance_certificate_json: bool = False
    uncertainty_propagation_certificate_json: bool = False
    final_export_readiness_report_json: bool = False
    no_target_observable_consumption: bool = False
    physical_export_lock_release_review: bool = False
    notes: str = ""


def default_release_runbook_request() -> ReleaseRunbookRequest:
    return ReleaseRunbookRequest()


def fully_documented_release_runbook_request() -> ReleaseRunbookRequest:
    return ReleaseRunbookRequest(
        completed_review_packet_json=True,
        review_packet_digest=True,
        source_candidate_digest=True,
        payload_file_uri=True,
        payload_sha256_digest=True,
        extraction_log_digest=True,
        import_session_log_json=True,
        replay_report_json=True,
        row_bundle_admission_report_json=True,
        component_sum_certificate_json=True,
        covariance_certificate_json=True,
        uncertainty_propagation_certificate_json=True,
        final_export_readiness_report_json=True,
        no_target_observable_consumption=True,
        physical_export_lock_release_review=True,
    )


def _contains_forbidden_token(text: str) -> bool:
    low = (text or "").lower()
    return any(tok.lower() in low for tok in FORBIDDEN_RELEASE_TOKENS)


def _artifact_dict(req: ReleaseRunbookRequest) -> Dict[str, bool]:
    d = asdict(req)
    return {k: bool(d.get(k, False)) for k in REQUIRED_ARTIFACTS}


def release_runbook_report(req: ReleaseRunbookRequest | None = None) -> Dict[str, Any]:
    req = req or default_release_runbook_request()
    d = asdict(req)
    artifacts = _artifact_dict(req)
    missing_artifacts = tuple(k for k, ok in artifacts.items() if not ok)
    failure_reasons = []
    if _contains_forbidden_token(req.notes):
        failure_reasons.append("FORBIDDEN_RELEASE_TOKEN_PRESENT")
    if d["payload_file_uri"] and not d["payload_sha256_digest"]:
        failure_reasons.append("PAYLOAD_FILE_WITHOUT_SHA256_DIGEST")
    if d["import_session_log_json"] and not d["replay_report_json"]:
        failure_reasons.append("IMPORT_LOG_WITHOUT_REPLAY_REPORT")
    if d["component_sum_certificate_json"] and not d["row_bundle_admission_report_json"]:
        failure_reasons.append("COMPONENT_SUM_WITHOUT_ROW_BUNDLE_ADMISSION_REPORT")
    if d["covariance_certificate_json"] and not d["row_bundle_admission_report_json"]:
        failure_reasons.append("COVARIANCE_WITHOUT_ROW_BUNDLE_ADMISSION_REPORT")
    if d["uncertainty_propagation_certificate_json"] and not (d["component_sum_certificate_json"] and d["covariance_certificate_json"]):
        failure_reasons.append("UNCERTAINTY_WITHOUT_SUM_AND_COVARIANCE_CERTIFICATES")
    release_documented = not missing_artifacts and d["no_target_observable_consumption"] and d["physical_export_lock_release_review"]
    pipeline = e2e_import_pipeline_manifest_report()
    readiness = readiness_report()
    physical_export_allowed = bool(release_documented and not failure_reasons and pipeline.get("pipeline_ready_for_physical_export", False) and not readiness.get("readiness_locked", True))
    report = {
        "release_runbook_status": W_RELEASE_RUNBOOK_STATUS,
        "release_runbook_version": RELEASE_RUNBOOK_VERSION,
        "release_runbook_mode": RELEASE_RUNBOOK_MODE,
        "upstream_pipeline_status": W_E2E_IMPORT_PIPELINE_MANIFEST_STATUS,
        "upstream_pipeline_version": E2E_IMPORT_PIPELINE_MANIFEST_VERSION,
        "runbook_phases": RUNBOOK_PHASES,
        "required_artifacts": REQUIRED_ARTIFACTS,
        "release_predicates": RELEASE_PREDICATES,
        "operator_actions": OPERATOR_ACTIONS,
        "artifact_state": artifacts,
        "missing_artifacts": missing_artifacts,
        **d,
        "release_packet_complete": bool(release_documented),
        "release_packet_validated": bool(release_documented and not failure_reasons),
        "real_payload_rows_admitted": REAL_PAYLOAD_ROWS_ADMITTED,
        "real_component_sum_certified": REAL_COMPONENT_SUM_CERTIFIED,
        "real_covariance_certified": REAL_COVARIANCE_CERTIFIED,
        "real_uncertainty_certified": REAL_UNCERTAINTY_CERTIFIED,
        "physical_W_export_enabled": PHYSICAL_W_EXPORT_ENABLED and physical_export_allowed,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W and physical_export_allowed,
        "physical_export_allowed_by_runbook": physical_export_allowed,
        "failure_reasons": tuple(dict.fromkeys(failure_reasons)),
        "locked_by_default": not physical_export_allowed,
        "terminal_state": "RUNBOOK_READY_BUT_PIPELINE_LOCKED" if release_documented and not failure_reasons else "RUNBOOK_INCOMPLETE_LOCKED",
    }
    return report


def write_release_runbook_template(path: str | Path = RUNBOOK_TEMPLATE_PATH) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = release_runbook_report()
    data.update({
        "template_only": True,
        "not_real_finite_part_evidence": True,
        "do_not_promote_to_real_release_packet": True,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
    })
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return path


def write_release_checklist_template(path: str | Path = RUNBOOK_CHECKLIST_PATH) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# W_TRACE Reviewed-Pipeline Release Checklist Template",
        "",
        "Template only. Not real finite-part evidence. Does not unlock physical W export.",
        "",
        "## Required artifacts",
    ]
    lines += [f"- [ ] `{item}`" for item in REQUIRED_ARTIFACTS]
    lines += ["", "## Operator actions"]
    lines += [f"- [ ] `{item}`" for item in OPERATOR_ACTIONS]
    lines += ["", "## Forbidden inputs", "Do not include observed M_W, W world average, residual-fit, APF-anchor as component input, or manual export override tokens."]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _res(name: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    return {"check": name, "passed": bool(passed), "epistemic": W_RELEASE_RUNBOOK_STATUS, **extra}


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed"))


def check_T_w_release_runbook_status_declared():
    return _res("status_declared", W_RELEASE_RUNBOOK_STATUS == "P_w_release_runbook")


def check_T_w_release_runbook_depends_on_e2e_manifest():
    upstream = _check_v121()
    ok = _passed(upstream) and W_E2E_IMPORT_PIPELINE_MANIFEST_STATUS == "P_w_e2e_import_pipeline_manifest"
    return _res("depends_on_e2e_manifest", ok, upstream=W_E2E_IMPORT_PIPELINE_MANIFEST_STATUS)


def check_T_w_release_runbook_phase_order_declared():
    ok = RUNBOOK_PHASES[0] == "source_candidate_selected" and RUNBOOK_PHASES[-1] == "final_export_readiness_reviewed" and len(RUNBOOK_PHASES) == 12
    return _res("phase_order_declared", ok, phases=RUNBOOK_PHASES)


def check_T_w_release_runbook_no_duplicate_phases():
    return _res("no_duplicate_phases", len(set(RUNBOOK_PHASES)) == len(RUNBOOK_PHASES))


def check_T_w_release_runbook_required_artifacts_declared():
    return _res("required_artifacts_declared", len(REQUIRED_ARTIFACTS) == 13 and "payload_sha256_digest" in REQUIRED_ARTIFACTS)


def check_T_w_release_runbook_required_artifacts_unique():
    return _res("required_artifacts_unique", len(set(REQUIRED_ARTIFACTS)) == len(REQUIRED_ARTIFACTS))


def check_T_w_release_runbook_operator_actions_declared():
    ok = "run_payload_import_cli" in OPERATOR_ACTIONS and "run_final_export_readiness" in OPERATOR_ACTIONS
    return _res("operator_actions_declared", ok, actions=OPERATOR_ACTIONS)


def check_T_w_release_runbook_release_predicates_declared():
    ok = set(RELEASE_PREDICATES) >= {"validated_review_packet", "admitted_real_rows", "certified_component_sum", "certified_covariance", "certified_uncertainty_propagation", "no_target_observable_consumption"}
    return _res("release_predicates_declared", ok, predicates=RELEASE_PREDICATES)


def check_T_w_release_runbook_default_locked_state():
    r = release_runbook_report()
    ok = r["locked_by_default"] is True and r["release_packet_complete"] is False and r["physical_W_export_enabled"] is False and r["exports_physical_M_W"] is False
    return _res("default_locked_state", ok, report=r)


def check_T_w_release_runbook_complete_packet_not_export_ready_without_pipeline():
    r = release_runbook_report(fully_documented_release_runbook_request())
    ok = r["release_packet_complete"] is True and r["release_packet_validated"] is True and r["physical_export_allowed_by_runbook"] is False
    return _res("complete_packet_not_export_ready_without_pipeline", ok, terminal=r["terminal_state"])


def check_T_w_release_runbook_missing_artifacts_reported():
    r = release_runbook_report()
    ok = len(r["missing_artifacts"]) == len(REQUIRED_ARTIFACTS)
    return _res("missing_artifacts_reported", ok, missing=r["missing_artifacts"])


def check_T_w_release_runbook_payload_digest_required():
    r = release_runbook_report(ReleaseRunbookRequest(payload_file_uri=True))
    ok = "PAYLOAD_FILE_WITHOUT_SHA256_DIGEST" in r["failure_reasons"]
    return _res("payload_digest_required", ok, failures=r["failure_reasons"])


def check_T_w_release_runbook_import_log_requires_replay():
    r = release_runbook_report(ReleaseRunbookRequest(import_session_log_json=True))
    ok = "IMPORT_LOG_WITHOUT_REPLAY_REPORT" in r["failure_reasons"]
    return _res("import_log_requires_replay", ok, failures=r["failure_reasons"])


def check_T_w_release_runbook_component_sum_requires_admission_report():
    r = release_runbook_report(ReleaseRunbookRequest(component_sum_certificate_json=True))
    ok = "COMPONENT_SUM_WITHOUT_ROW_BUNDLE_ADMISSION_REPORT" in r["failure_reasons"]
    return _res("component_sum_requires_admission_report", ok, failures=r["failure_reasons"])


def check_T_w_release_runbook_covariance_requires_admission_report():
    r = release_runbook_report(ReleaseRunbookRequest(covariance_certificate_json=True))
    ok = "COVARIANCE_WITHOUT_ROW_BUNDLE_ADMISSION_REPORT" in r["failure_reasons"]
    return _res("covariance_requires_admission_report", ok, failures=r["failure_reasons"])


def check_T_w_release_runbook_uncertainty_requires_sum_and_covariance():
    r = release_runbook_report(ReleaseRunbookRequest(uncertainty_propagation_certificate_json=True))
    ok = "UNCERTAINTY_WITHOUT_SUM_AND_COVARIANCE_CERTIFICATES" in r["failure_reasons"]
    return _res("uncertainty_requires_sum_and_covariance", ok, failures=r["failure_reasons"])


def check_T_w_release_runbook_forbidden_tokens_declared():
    ok = "observed_M_W" in FORBIDDEN_RELEASE_TOKENS and "manual_export_unlock" in FORBIDDEN_RELEASE_TOKENS
    return _res("forbidden_tokens_declared", ok, tokens=FORBIDDEN_RELEASE_TOKENS)


def check_T_w_release_runbook_rejects_observed_w_token():
    r = release_runbook_report(ReleaseRunbookRequest(notes="use observed_M_W as a check"))
    ok = "FORBIDDEN_RELEASE_TOKEN_PRESENT" in r["failure_reasons"]
    return _res("rejects_observed_w_token", ok, failures=r["failure_reasons"])


def check_T_w_release_runbook_rejects_manual_override_token():
    r = release_runbook_report(ReleaseRunbookRequest(notes="manual_export_unlock requested"))
    ok = "FORBIDDEN_RELEASE_TOKEN_PRESENT" in r["failure_reasons"]
    return _res("rejects_manual_override_token", ok, failures=r["failure_reasons"])


def check_T_w_release_runbook_no_physical_export_flags():
    r = release_runbook_report(fully_documented_release_runbook_request())
    ok = r["physical_W_export_enabled"] is False and r["exports_physical_M_W"] is False
    return _res("no_physical_export_flags", ok, export_enabled=r["physical_W_export_enabled"], exports=r["exports_physical_M_W"])


def check_T_w_release_runbook_json_serializable():
    try:
        json.dumps(release_runbook_report(), sort_keys=True)
        ok = True
    except TypeError:
        ok = False
    return _res("json_serializable", ok)


def check_T_w_release_runbook_template_path_declared():
    ok = RUNBOOK_TEMPLATE_PATH.name == "release_runbook_template.json" and RUNBOOK_CHECKLIST_PATH.name == "release_checklist_template.md"
    return _res("template_path_declared", ok, json_path=str(RUNBOOK_TEMPLATE_PATH), checklist_path=str(RUNBOOK_CHECKLIST_PATH))


def check_T_w_release_runbook_write_json_template():
    path = write_release_runbook_template()
    ok = path.exists() and json.loads(path.read_text(encoding="utf-8")).get("template_only") is True
    return _res("write_json_template", ok, path=str(path))


def check_T_w_release_runbook_write_checklist_template():
    path = write_release_checklist_template()
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    ok = "Template only" in text and "Required artifacts" in text and "Operator actions" in text
    return _res("write_checklist_template", ok, path=str(path))


def check_T_w_release_runbook_doc_exists():
    return _res("doc_exists", RUNBOOK_DOC_PATH.exists(), path=str(RUNBOOK_DOC_PATH))


def check_T_w_release_runbook_doc_warns_locked():
    text = RUNBOOK_DOC_PATH.read_text(encoding="utf-8") if RUNBOOK_DOC_PATH.exists() else ""
    ok = "physical W/on-shell export remains OPEN" in text and "operator runbook" in text and "template only" in text.lower()
    return _res("doc_warns_locked", ok, found=len(text))


def check_T_w_release_runbook_json_template_not_real():
    data = json.loads(RUNBOOK_TEMPLATE_PATH.read_text(encoding="utf-8")) if RUNBOOK_TEMPLATE_PATH.exists() else {}
    ok = data.get("template_only") is True and data.get("not_real_finite_part_evidence") is True and data.get("exports_physical_M_W") is False
    return _res("json_template_not_real", ok, data=data)


def check_T_w_release_runbook_checklist_template_not_real():
    text = RUNBOOK_CHECKLIST_PATH.read_text(encoding="utf-8") if RUNBOOK_CHECKLIST_PATH.exists() else ""
    ok = "Not real finite-part evidence" in text and "Does not unlock physical W export" in text
    return _res("checklist_template_not_real", ok)


def check_T_w_release_runbook_required_manifest_fields_referenced():
    ok = "physical_W_export_enabled" in REQUIRED_MANIFEST_FIELDS and "failure_reasons" in REQUIRED_MANIFEST_FIELDS
    return _res("required_manifest_fields_referenced", ok, manifest_fields=REQUIRED_MANIFEST_FIELDS)


def check_T_w_release_runbook_pipeline_stage_order_referenced():
    ok = PIPELINE_STAGE_ORDER[0] == "review_packet_preflight" and PIPELINE_STAGE_ORDER[-1] == "final_export_readiness"
    return _res("pipeline_stage_order_referenced", ok, pipeline_stage_order=PIPELINE_STAGE_ORDER)


def check_T_w_release_runbook_terminal_state_locked():
    r = release_runbook_report()
    ok = r["terminal_state"] == "RUNBOOK_INCOMPLETE_LOCKED" and r["locked_by_default"] is True
    return _res("terminal_state_locked", ok, terminal=r["terminal_state"])


def check_T_w_release_runbook_bank_closure():
    rows = [fn() for fn in CHECKS.values() if fn is not check_T_w_release_runbook_bank_closure]
    ok = all(_passed(r) for r in rows) and len(rows) == 31
    return _res("bank_closure", ok, checked=len(rows), failed=[r.get("check") for r in rows if not _passed(r)])


CHECKS = {
    "T_w_release_runbook_status_declared": check_T_w_release_runbook_status_declared,
    "T_w_release_runbook_depends_on_e2e_manifest": check_T_w_release_runbook_depends_on_e2e_manifest,
    "T_w_release_runbook_phase_order_declared": check_T_w_release_runbook_phase_order_declared,
    "T_w_release_runbook_no_duplicate_phases": check_T_w_release_runbook_no_duplicate_phases,
    "T_w_release_runbook_required_artifacts_declared": check_T_w_release_runbook_required_artifacts_declared,
    "T_w_release_runbook_required_artifacts_unique": check_T_w_release_runbook_required_artifacts_unique,
    "T_w_release_runbook_operator_actions_declared": check_T_w_release_runbook_operator_actions_declared,
    "T_w_release_runbook_release_predicates_declared": check_T_w_release_runbook_release_predicates_declared,
    "T_w_release_runbook_default_locked_state": check_T_w_release_runbook_default_locked_state,
    "T_w_release_runbook_complete_packet_not_export_ready_without_pipeline": check_T_w_release_runbook_complete_packet_not_export_ready_without_pipeline,
    "T_w_release_runbook_missing_artifacts_reported": check_T_w_release_runbook_missing_artifacts_reported,
    "T_w_release_runbook_payload_digest_required": check_T_w_release_runbook_payload_digest_required,
    "T_w_release_runbook_import_log_requires_replay": check_T_w_release_runbook_import_log_requires_replay,
    "T_w_release_runbook_component_sum_requires_admission_report": check_T_w_release_runbook_component_sum_requires_admission_report,
    "T_w_release_runbook_covariance_requires_admission_report": check_T_w_release_runbook_covariance_requires_admission_report,
    "T_w_release_runbook_uncertainty_requires_sum_and_covariance": check_T_w_release_runbook_uncertainty_requires_sum_and_covariance,
    "T_w_release_runbook_forbidden_tokens_declared": check_T_w_release_runbook_forbidden_tokens_declared,
    "T_w_release_runbook_rejects_observed_w_token": check_T_w_release_runbook_rejects_observed_w_token,
    "T_w_release_runbook_rejects_manual_override_token": check_T_w_release_runbook_rejects_manual_override_token,
    "T_w_release_runbook_no_physical_export_flags": check_T_w_release_runbook_no_physical_export_flags,
    "T_w_release_runbook_json_serializable": check_T_w_release_runbook_json_serializable,
    "T_w_release_runbook_template_path_declared": check_T_w_release_runbook_template_path_declared,
    "T_w_release_runbook_write_json_template": check_T_w_release_runbook_write_json_template,
    "T_w_release_runbook_write_checklist_template": check_T_w_release_runbook_write_checklist_template,
    "T_w_release_runbook_doc_exists": check_T_w_release_runbook_doc_exists,
    "T_w_release_runbook_doc_warns_locked": check_T_w_release_runbook_doc_warns_locked,
    "T_w_release_runbook_json_template_not_real": check_T_w_release_runbook_json_template_not_real,
    "T_w_release_runbook_checklist_template_not_real": check_T_w_release_runbook_checklist_template_not_real,
    "T_w_release_runbook_required_manifest_fields_referenced": check_T_w_release_runbook_required_manifest_fields_referenced,
    "T_w_release_runbook_pipeline_stage_order_referenced": check_T_w_release_runbook_pipeline_stage_order_referenced,
    "T_w_release_runbook_terminal_state_locked": check_T_w_release_runbook_terminal_state_locked,
    "T_w_release_runbook_bank_closure": check_T_w_release_runbook_bank_closure,
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
        "status": "W_TRACE_RELEASE_RUNBOOK_BANK_PASS" if ok else "W_TRACE_RELEASE_RUNBOOK_BANK_FAIL",
        "checks": rows,
        "report": release_runbook_report(),
    }
