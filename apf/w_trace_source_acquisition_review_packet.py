"""W_TRACE source-candidate acquisition worksheet / review-packet bank.

v11.6 (2026-05-09 LATER-51): review packet above the v11.5
source-candidate registry.  This module banks the concrete worksheet and
review artifact required before any external finite-part source candidate can
be promoted into the v11.3 import CLI / v10.x admission stack.  It deliberately
ships template-only review artifacts: no real source is acquired, no rows are
imported, no component-sum certificate is issued, and no physical W/on-shell
value is exported.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple

from apf.w_trace_source_candidate_registry import (
    W_SOURCE_CANDIDATE_REGISTRY_STATUS,
    ALLOWED_SOURCE_CANDIDATE_CLASSES,
    FORBIDDEN_ACQUISITION_INPUTS,
    REQUIRED_ACQUISITION_EVIDENCE_FIELDS,
    REQUIRED_PREIMPORT_STEPS,
    SourceCandidateEntry,
    candidate_complete_for_import,
    candidate_registry,
    check_T_w_source_candidate_registry_bank_closure as _check_v115,
    source_candidate_registry_report,
)
from apf.w_trace_finite_part_skeleton import FINITE_PART_COMPONENT_ORDER
from apf.w_trace_final_export_readiness import readiness_report

W_SOURCE_ACQUISITION_REVIEW_PACKET_STATUS = "P_w_source_acquisition_review_packet"
SOURCE_ACQUISITION_REVIEW_PACKET_VERSION = "w_trace_source_acquisition_review_packet_v1"
SOURCE_ACQUISITION_REVIEW_PACKET_MODE = "WORKSHEET_AND_REVIEW_PACKET__NO_REAL_SOURCE_ACQUIRED"

REAL_EXTERNAL_SOURCE_ACQUIRED = False
REAL_EXTERNAL_ROWS_IMPORTED = False
REAL_EXTERNAL_ROWS_ADMITTED = False
COMPONENT_SUM_CERTIFIED = False
COVARIANCE_CERTIFIED = False
UNCERTAINTY_PROPAGATION_CERTIFIED = False
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False

ROOT = Path(__file__).resolve().parent.parent
REVIEW_PACKET_DOC_PATH = ROOT / "W_TRACE_SOURCE_ACQUISITION_REVIEW_PACKET_BANK_v1_0.md"
TEMPLATE_DIR = ROOT / "examples" / "w_trace_source_acquisition_review_packet"
MARKDOWN_PACKET_TEMPLATE_PATH = TEMPLATE_DIR / "source_candidate_review_packet_template.md"
JSON_PACKET_TEMPLATE_PATH = TEMPLATE_DIR / "source_candidate_review_packet_template.json"

REVIEW_PACKET_SECTIONS: Tuple[str, ...] = (
    "candidate_identity",
    "source_class_and_locator",
    "component_coverage_map",
    "scheme_gauge_counterterm_alignment",
    "forbidden_input_audit",
    "extraction_and_digest_plan",
    "license_access_and_reproducibility",
    "review_attestation",
    "import_cli_preflight",
    "export_lock_confirmation",
)

REVIEW_DECISIONS: Tuple[str, ...] = (
    "TEMPLATE_ONLY_DO_NOT_IMPORT",
    "REJECT_SOURCE",
    "NEEDS_MORE_EVIDENCE",
    "APPROVE_FOR_IMPORT_ATTEMPT",
)

REQUIRED_REVIEW_PACKET_FIELDS: Tuple[str, ...] = (
    "packet_id",
    "candidate_entry",
    "reviewer_or_process",
    "review_decision",
    "review_notes_digest",
    "evidence_bundle_digest",
    "worksheet_sections_completed",
    "preimport_steps_attested",
    "forbidden_input_audit_passed",
    "template_only",
    "physical_export_requested",
)

@dataclass(frozen=True)
class SourceAcquisitionReviewPacket:
    packet_id: str
    candidate_entry: SourceCandidateEntry
    reviewer_or_process: str = "UNREVIEWED"
    review_decision: str = "TEMPLATE_ONLY_DO_NOT_IMPORT"
    review_notes_digest: str = "UNCOMPUTED"
    evidence_bundle_digest: str = "UNCOMPUTED"
    worksheet_sections_completed: Tuple[str, ...] = ()
    preimport_steps_attested: Tuple[str, ...] = ()
    forbidden_input_audit_passed: bool = False
    template_only: bool = True
    physical_export_requested: bool = False


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def _res(name: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    return {
        "passed": bool(passed),
        "status": "PASS" if passed else "FAIL",
        "tier": 4,
        "epistemic": W_SOURCE_ACQUISITION_REVIEW_PACKET_STATUS,
        "check": name,
        **extra,
    }


def default_review_packet() -> SourceAcquisitionReviewPacket:
    return SourceAcquisitionReviewPacket(
        packet_id="template_packet_no_real_source",
        candidate_entry=candidate_registry()[0],
        worksheet_sections_completed=(),
        preimport_steps_attested=(),
        template_only=True,
    )


def promoted_review_packet() -> SourceAcquisitionReviewPacket:
    entry = replace(
        candidate_registry()[0],
        public_or_archival_locator="doi_or_archive_locator_pending_real_value",
        version_or_revision_id="reviewed_revision_identifier_pending_real_value",
        license_or_access_note="access reviewed; redistribution constraints recorded",
        extraction_log_digest="sha256:" + "c" * 64,
        pack_digest_plan="sha256:" + "d" * 64,
        review_attestation_plan="REVIEWED_INDEPENDENT_SOURCE_READY_FOR_IMPORT",
        forbidden_input_audit_plan="PASSED_NO_FORBIDDEN_INPUTS",
        scheme_and_gauge_policy_note="on-shell-compatible scheme/gauge policy recorded",
        counterterm_convention_note="Delta_r_ct_OS convention mapped to v10.7 certificate",
        acquired=True,
        imported=False,
        admitted=False,
        synthetic_or_template_only=False,
        consumes_forbidden_input=False,
        exports_physical_mw=False,
    )
    return SourceAcquisitionReviewPacket(
        packet_id="reviewed_source_candidate_ready_for_import_attempt",
        candidate_entry=entry,
        reviewer_or_process="independent_review_process_recorded",
        review_decision="APPROVE_FOR_IMPORT_ATTEMPT",
        review_notes_digest="sha256:" + "e" * 64,
        evidence_bundle_digest="sha256:" + "f" * 64,
        worksheet_sections_completed=REVIEW_PACKET_SECTIONS,
        preimport_steps_attested=REQUIRED_PREIMPORT_STEPS,
        forbidden_input_audit_passed=True,
        template_only=False,
        physical_export_requested=False,
    )


def review_packet_complete_for_import_attempt(packet: SourceAcquisitionReviewPacket | Mapping[str, Any]) -> bool:
    if isinstance(packet, SourceAcquisitionReviewPacket):
        d = asdict(packet)
        entry = packet.candidate_entry
    else:
        d = dict(packet)
        entry_raw = d.get("candidate_entry", {})
        entry = SourceCandidateEntry(**entry_raw) if isinstance(entry_raw, dict) else entry_raw
    if not all(k in d for k in REQUIRED_REVIEW_PACKET_FIELDS):
        return False
    if d.get("review_decision") != "APPROVE_FOR_IMPORT_ATTEMPT":
        return False
    if d.get("template_only") or d.get("physical_export_requested"):
        return False
    if d.get("forbidden_input_audit_passed") is not True:
        return False
    if tuple(d.get("worksheet_sections_completed") or ()) != REVIEW_PACKET_SECTIONS:
        return False
    if tuple(d.get("preimport_steps_attested") or ()) != REQUIRED_PREIMPORT_STEPS:
        return False
    if not str(d.get("review_notes_digest", "")).startswith("sha256:"):
        return False
    if not str(d.get("evidence_bundle_digest", "")).startswith("sha256:"):
        return False
    return candidate_complete_for_import(entry)


def source_acquisition_review_packet_report() -> Dict[str, Any]:
    registry = source_candidate_registry_report()
    ready = readiness_report(physical_export_requested=False)
    default_packet = default_review_packet()
    return {
        "status": W_SOURCE_ACQUISITION_REVIEW_PACKET_STATUS,
        "version": SOURCE_ACQUISITION_REVIEW_PACKET_VERSION,
        "mode": SOURCE_ACQUISITION_REVIEW_PACKET_MODE,
        "upstream_registry_status": W_SOURCE_CANDIDATE_REGISTRY_STATUS,
        "registry_locked": not registry["physical_W_export_enabled"] and registry["complete_for_import_count"] == 0,
        "review_packet_sections": REVIEW_PACKET_SECTIONS,
        "review_decisions": REVIEW_DECISIONS,
        "required_review_packet_fields": REQUIRED_REVIEW_PACKET_FIELDS,
        "required_acquisition_evidence_fields": REQUIRED_ACQUISITION_EVIDENCE_FIELDS,
        "allowed_source_candidate_classes": ALLOWED_SOURCE_CANDIDATE_CLASSES,
        "required_preimport_steps": REQUIRED_PREIMPORT_STEPS,
        "forbidden_acquisition_inputs": FORBIDDEN_ACQUISITION_INPUTS,
        "component_order": FINITE_PART_COMPONENT_ORDER,
        "default_packet": asdict(default_packet),
        "default_packet_complete_for_import_attempt": review_packet_complete_for_import_attempt(default_packet),
        "promoted_packet_complete_for_import_attempt": review_packet_complete_for_import_attempt(promoted_review_packet()),
        "real_external_source_acquired": REAL_EXTERNAL_SOURCE_ACQUIRED,
        "real_external_rows_imported": REAL_EXTERNAL_ROWS_IMPORTED,
        "real_external_rows_admitted": REAL_EXTERNAL_ROWS_ADMITTED,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "covariance_certified": COVARIANCE_CERTIFIED,
        "uncertainty_propagation_certified": UNCERTAINTY_PROPAGATION_CERTIFIED,
        "physical_W_export_enabled": PHYSICAL_W_EXPORT_ENABLED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "readiness_locked": not ready["physical_W_export_ready"] and not ready["physical_W_export_enabled"],
        "review_packet_doc_path": str(REVIEW_PACKET_DOC_PATH),
        "markdown_packet_template_path": str(MARKDOWN_PACKET_TEMPLATE_PATH),
        "json_packet_template_path": str(JSON_PACKET_TEMPLATE_PATH),
    }


def _packet_with_forbidden_input(token: str) -> SourceAcquisitionReviewPacket:
    p = promoted_review_packet()
    entry = replace(
        p.candidate_entry,
        consumes_forbidden_input=True,
        forbidden_input_audit_plan=f"FAILED_USED_{token}",
    )
    return replace(p, candidate_entry=entry, forbidden_input_audit_passed=False)


def check_T_w_source_acquisition_review_packet_status_declared():
    r = source_acquisition_review_packet_report(); ok = r["status"] == W_SOURCE_ACQUISITION_REVIEW_PACKET_STATUS and not r["physical_W_export_enabled"]
    return _res("status_declared", ok, report=r)


def check_T_w_source_acquisition_review_packet_depends_on_v115_registry():
    d = _check_v115(); return _res("depends_on_v115_registry", _passed(d), upstream=d.get("status"))


def check_T_w_source_acquisition_review_packet_sections_declared():
    ok = len(REVIEW_PACKET_SECTIONS) == 10 and "forbidden_input_audit" in REVIEW_PACKET_SECTIONS and "export_lock_confirmation" in REVIEW_PACKET_SECTIONS
    return _res("sections_declared", ok, sections=REVIEW_PACKET_SECTIONS)


def check_T_w_source_acquisition_review_packet_decisions_declared():
    ok = set(REVIEW_DECISIONS) == {"TEMPLATE_ONLY_DO_NOT_IMPORT", "REJECT_SOURCE", "NEEDS_MORE_EVIDENCE", "APPROVE_FOR_IMPORT_ATTEMPT"}
    return _res("decisions_declared", ok, decisions=REVIEW_DECISIONS)


def check_T_w_source_acquisition_review_packet_required_fields_complete():
    needed = {"packet_id", "candidate_entry", "review_decision", "forbidden_input_audit_passed", "physical_export_requested"}
    ok = needed.issubset(set(REQUIRED_REVIEW_PACKET_FIELDS))
    return _res("required_fields_complete", ok, fields=REQUIRED_REVIEW_PACKET_FIELDS)


def check_T_w_source_acquisition_review_packet_carries_registry_evidence_fields():
    r = source_acquisition_review_packet_report(); ok = tuple(r["required_acquisition_evidence_fields"]) == REQUIRED_ACQUISITION_EVIDENCE_FIELDS
    return _res("carries_registry_evidence_fields", ok, report=r)


def check_T_w_source_acquisition_review_packet_carries_allowed_source_classes():
    r = source_acquisition_review_packet_report(); ok = tuple(r["allowed_source_candidate_classes"]) == ALLOWED_SOURCE_CANDIDATE_CLASSES
    return _res("carries_allowed_source_classes", ok, report=r)


def check_T_w_source_acquisition_review_packet_carries_forbidden_inputs():
    r = source_acquisition_review_packet_report(); ok = {"observed_M_W", "APF_ANCHOR_DELTA_R_TARGET", "physical_export_request"}.issubset(set(r["forbidden_acquisition_inputs"]))
    return _res("carries_forbidden_inputs", ok, report=r)


def check_T_w_source_acquisition_review_packet_carries_preimport_order():
    steps = source_acquisition_review_packet_report()["required_preimport_steps"]
    ok = steps.index("confirm_independent_of_observed_W_mass") < steps.index("run_v11_3_payload_import_cli") < steps.index("keep_export_lock_closed_until_final_readiness_passes")
    return _res("carries_preimport_order", ok, steps=steps)


def check_T_w_source_acquisition_review_packet_default_template_not_complete():
    p = default_review_packet(); return _res("default_template_not_complete", not review_packet_complete_for_import_attempt(p), packet=asdict(p))


def check_T_w_source_acquisition_review_packet_promoted_packet_complete():
    p = promoted_review_packet(); return _res("promoted_packet_complete", review_packet_complete_for_import_attempt(p), packet=asdict(p))


def check_T_w_source_acquisition_review_packet_rejects_observed_W_input():
    p = _packet_with_forbidden_input("observed_M_W"); return _res("rejects_observed_W_input", not review_packet_complete_for_import_attempt(p), packet=asdict(p))


def check_T_w_source_acquisition_review_packet_rejects_APF_anchor_input():
    p = _packet_with_forbidden_input("APF_ANCHOR_DELTA_R_TARGET"); return _res("rejects_APF_anchor_input", not review_packet_complete_for_import_attempt(p), packet=asdict(p))


def check_T_w_source_acquisition_review_packet_rejects_physical_export_request():
    p = replace(promoted_review_packet(), physical_export_requested=True); return _res("rejects_physical_export_request", not review_packet_complete_for_import_attempt(p), packet=asdict(p))


def check_T_w_source_acquisition_review_packet_rejects_missing_review_digest():
    p = replace(promoted_review_packet(), review_notes_digest="UNCOMPUTED"); return _res("rejects_missing_review_digest", not review_packet_complete_for_import_attempt(p), packet=asdict(p))


def check_T_w_source_acquisition_review_packet_rejects_missing_evidence_digest():
    p = replace(promoted_review_packet(), evidence_bundle_digest="UNCOMPUTED"); return _res("rejects_missing_evidence_digest", not review_packet_complete_for_import_attempt(p), packet=asdict(p))


def check_T_w_source_acquisition_review_packet_rejects_incomplete_sections():
    p = replace(promoted_review_packet(), worksheet_sections_completed=REVIEW_PACKET_SECTIONS[:-1]); return _res("rejects_incomplete_sections", not review_packet_complete_for_import_attempt(p), packet=asdict(p))


def check_T_w_source_acquisition_review_packet_rejects_incomplete_preimport_steps():
    p = replace(promoted_review_packet(), preimport_steps_attested=REQUIRED_PREIMPORT_STEPS[:-1]); return _res("rejects_incomplete_preimport_steps", not review_packet_complete_for_import_attempt(p), packet=asdict(p))


def check_T_w_source_acquisition_review_packet_rejects_wrong_decision():
    p = replace(promoted_review_packet(), review_decision="NEEDS_MORE_EVIDENCE"); return _res("rejects_wrong_decision", not review_packet_complete_for_import_attempt(p), packet=asdict(p))


def check_T_w_source_acquisition_review_packet_rejects_template_flag():
    p = replace(promoted_review_packet(), template_only=True); return _res("rejects_template_flag", not review_packet_complete_for_import_attempt(p), packet=asdict(p))


def check_T_w_source_acquisition_review_packet_report_locks_default_state():
    r = source_acquisition_review_packet_report(); ok = not r["real_external_source_acquired"] and not r["real_external_rows_imported"] and not r["physical_W_export_enabled"]
    return _res("report_locks_default_state", ok, report=r)


def check_T_w_source_acquisition_review_packet_readiness_locked():
    r = source_acquisition_review_packet_report(); ok = r["readiness_locked"] and not r["exports_physical_M_W"]
    return _res("readiness_locked", ok, report=r)


def check_T_w_source_acquisition_review_packet_no_component_sum_or_covariance():
    r = source_acquisition_review_packet_report(); ok = not r["component_sum_certified"] and not r["covariance_certified"] and not r["uncertainty_propagation_certified"]
    return _res("no_component_sum_or_covariance", ok, report=r)


def check_T_w_source_acquisition_review_packet_doc_exists():
    return _res("doc_exists", REVIEW_PACKET_DOC_PATH.exists(), path=str(REVIEW_PACKET_DOC_PATH))


def check_T_w_source_acquisition_review_packet_doc_warns_no_real_source():
    text = REVIEW_PACKET_DOC_PATH.read_text(encoding="utf-8") if REVIEW_PACKET_DOC_PATH.exists() else ""
    needed = ("No real external source is acquired", "observed M_W", "APF-anchor", "physical W export remains locked")
    ok = all(s in text for s in needed)
    return _res("doc_warns_no_real_source", ok, needed=needed)


def check_T_w_source_acquisition_review_packet_markdown_template_exists():
    return _res("markdown_template_exists", MARKDOWN_PACKET_TEMPLATE_PATH.exists(), path=str(MARKDOWN_PACKET_TEMPLATE_PATH))


def check_T_w_source_acquisition_review_packet_markdown_template_has_placeholders():
    text = MARKDOWN_PACKET_TEMPLATE_PATH.read_text(encoding="utf-8") if MARKDOWN_PACKET_TEMPLATE_PATH.exists() else ""
    needed = ("TEMPLATE_ONLY_DO_NOT_IMPORT", "sha256:<review_notes_digest>", "Forbidden-input audit")
    ok = all(s in text for s in needed)
    return _res("markdown_template_has_placeholders", ok, needed=needed)


def check_T_w_source_acquisition_review_packet_json_template_exists():
    return _res("json_template_exists", JSON_PACKET_TEMPLATE_PATH.exists(), path=str(JSON_PACKET_TEMPLATE_PATH))


def check_T_w_source_acquisition_review_packet_json_template_not_real_payload():
    text = JSON_PACKET_TEMPLATE_PATH.read_text(encoding="utf-8") if JSON_PACKET_TEMPLATE_PATH.exists() else ""
    ok = '"template_only": true' in text and '"physical_export_requested": false' in text and 'observed_M_W' not in text
    return _res("json_template_not_real_payload", ok, path=str(JSON_PACKET_TEMPLATE_PATH))


def check_T_w_source_acquisition_review_packet_bank_closure():
    rows = [fn() for name, fn in CHECKS.items() if name != "T_w_source_acquisition_review_packet_bank_closure"]
    r = source_acquisition_review_packet_report()
    ok = all(_passed(x) for x in rows) and not r["physical_W_export_enabled"] and not r["default_packet_complete_for_import_attempt"]
    return _res("bank_closure", ok, passed_count=sum(_passed(x) for x in rows), total=len(rows), report=r)


CHECKS: Dict[str, Any] = {
    "T_w_source_acquisition_review_packet_status_declared": check_T_w_source_acquisition_review_packet_status_declared,
    "T_w_source_acquisition_review_packet_depends_on_v115_registry": check_T_w_source_acquisition_review_packet_depends_on_v115_registry,
    "T_w_source_acquisition_review_packet_sections_declared": check_T_w_source_acquisition_review_packet_sections_declared,
    "T_w_source_acquisition_review_packet_decisions_declared": check_T_w_source_acquisition_review_packet_decisions_declared,
    "T_w_source_acquisition_review_packet_required_fields_complete": check_T_w_source_acquisition_review_packet_required_fields_complete,
    "T_w_source_acquisition_review_packet_carries_registry_evidence_fields": check_T_w_source_acquisition_review_packet_carries_registry_evidence_fields,
    "T_w_source_acquisition_review_packet_carries_allowed_source_classes": check_T_w_source_acquisition_review_packet_carries_allowed_source_classes,
    "T_w_source_acquisition_review_packet_carries_forbidden_inputs": check_T_w_source_acquisition_review_packet_carries_forbidden_inputs,
    "T_w_source_acquisition_review_packet_carries_preimport_order": check_T_w_source_acquisition_review_packet_carries_preimport_order,
    "T_w_source_acquisition_review_packet_default_template_not_complete": check_T_w_source_acquisition_review_packet_default_template_not_complete,
    "T_w_source_acquisition_review_packet_promoted_packet_complete": check_T_w_source_acquisition_review_packet_promoted_packet_complete,
    "T_w_source_acquisition_review_packet_rejects_observed_W_input": check_T_w_source_acquisition_review_packet_rejects_observed_W_input,
    "T_w_source_acquisition_review_packet_rejects_APF_anchor_input": check_T_w_source_acquisition_review_packet_rejects_APF_anchor_input,
    "T_w_source_acquisition_review_packet_rejects_physical_export_request": check_T_w_source_acquisition_review_packet_rejects_physical_export_request,
    "T_w_source_acquisition_review_packet_rejects_missing_review_digest": check_T_w_source_acquisition_review_packet_rejects_missing_review_digest,
    "T_w_source_acquisition_review_packet_rejects_missing_evidence_digest": check_T_w_source_acquisition_review_packet_rejects_missing_evidence_digest,
    "T_w_source_acquisition_review_packet_rejects_incomplete_sections": check_T_w_source_acquisition_review_packet_rejects_incomplete_sections,
    "T_w_source_acquisition_review_packet_rejects_incomplete_preimport_steps": check_T_w_source_acquisition_review_packet_rejects_incomplete_preimport_steps,
    "T_w_source_acquisition_review_packet_rejects_wrong_decision": check_T_w_source_acquisition_review_packet_rejects_wrong_decision,
    "T_w_source_acquisition_review_packet_rejects_template_flag": check_T_w_source_acquisition_review_packet_rejects_template_flag,
    "T_w_source_acquisition_review_packet_report_locks_default_state": check_T_w_source_acquisition_review_packet_report_locks_default_state,
    "T_w_source_acquisition_review_packet_readiness_locked": check_T_w_source_acquisition_review_packet_readiness_locked,
    "T_w_source_acquisition_review_packet_no_component_sum_or_covariance": check_T_w_source_acquisition_review_packet_no_component_sum_or_covariance,
    "T_w_source_acquisition_review_packet_doc_exists": check_T_w_source_acquisition_review_packet_doc_exists,
    "T_w_source_acquisition_review_packet_doc_warns_no_real_source": check_T_w_source_acquisition_review_packet_doc_warns_no_real_source,
    "T_w_source_acquisition_review_packet_markdown_template_exists": check_T_w_source_acquisition_review_packet_markdown_template_exists,
    "T_w_source_acquisition_review_packet_markdown_template_has_placeholders": check_T_w_source_acquisition_review_packet_markdown_template_has_placeholders,
    "T_w_source_acquisition_review_packet_json_template_exists": check_T_w_source_acquisition_review_packet_json_template_exists,
    "T_w_source_acquisition_review_packet_json_template_not_real_payload": check_T_w_source_acquisition_review_packet_json_template_not_real_payload,
    "T_w_source_acquisition_review_packet_bank_closure": check_T_w_source_acquisition_review_packet_bank_closure,
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
        "status": "W_TRACE_SOURCE_ACQUISITION_REVIEW_PACKET_BANK_PASS" if ok else "W_TRACE_SOURCE_ACQUISITION_REVIEW_PACKET_BANK_FAIL",
        "checks": rows,
        "manifest": source_acquisition_review_packet_report(),
    }
