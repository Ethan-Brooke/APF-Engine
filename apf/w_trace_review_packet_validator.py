"""W_TRACE completed source-review packet validator / import preflight bank.

v11.7 (2026-05-09 LATER-52): validator layer above the v11.6
source-acquisition review packet.  This module banks the completed-packet
preflight contract used before any reviewed external finite-part source packet
may be handed to the v11.3 payload import CLI.  It deliberately ships no real
completed packet and imports no rows: default/template packets fail closed,
physical W export remains locked, and only a synthetic promoted packet witness
is used to prove the validator logic.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from pathlib import Path
import json
from typing import Any, Dict, Mapping, Tuple

from apf.w_trace_source_acquisition_review_packet import (
    W_SOURCE_ACQUISITION_REVIEW_PACKET_STATUS,
    REVIEW_PACKET_SECTIONS,
    REVIEW_DECISIONS,
    REQUIRED_REVIEW_PACKET_FIELDS,
    SourceAcquisitionReviewPacket,
    default_review_packet,
    promoted_review_packet,
    review_packet_complete_for_import_attempt,
    check_T_w_source_acquisition_review_packet_bank_closure as _check_v116,
)
from apf.w_trace_source_candidate_registry import (
    FORBIDDEN_ACQUISITION_INPUTS,
    REQUIRED_PREIMPORT_STEPS,
    SourceCandidateEntry,
    candidate_complete_for_import,
)
from apf.w_trace_final_export_readiness import readiness_report

W_REVIEW_PACKET_VALIDATOR_STATUS = "P_w_review_packet_validator"
REVIEW_PACKET_VALIDATOR_VERSION = "w_trace_review_packet_validator_v1"
REVIEW_PACKET_VALIDATOR_MODE = "COMPLETED_PACKET_PREFLIGHT__NO_REAL_PACKET_SHIPPED"

REAL_COMPLETED_REVIEW_PACKET_SHIPPED = False
REAL_COMPLETED_REVIEW_PACKET_VALIDATED = False
REAL_EXTERNAL_SOURCE_ACQUIRED = False
REAL_EXTERNAL_ROWS_IMPORTED = False
REAL_EXTERNAL_ROWS_ADMITTED = False
COMPONENT_SUM_CERTIFIED = False
COVARIANCE_CERTIFIED = False
UNCERTAINTY_PROPAGATION_CERTIFIED = False
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False

ROOT = Path(__file__).resolve().parent.parent
VALIDATOR_DOC_PATH = ROOT / "W_TRACE_REVIEW_PACKET_VALIDATOR_BANK_v1_0.md"
VALIDATOR_TEMPLATE_DIR = ROOT / "examples" / "w_trace_review_packet_validator"
VALIDATOR_PACKET_TEMPLATE_PATH = VALIDATOR_TEMPLATE_DIR / "completed_packet_preflight_template.json"

PREFLIGHT_DECISIONS: Tuple[str, ...] = (
    "NO_PACKET_SUPPLIED",
    "REJECT_TEMPLATE_OR_INCOMPLETE_PACKET",
    "REJECT_FORBIDDEN_INPUT_CONSUMPTION",
    "READY_FOR_IMPORT_ATTEMPT",
)

VALIDATOR_REQUIRED_FIELDS: Tuple[str, ...] = REQUIRED_REVIEW_PACKET_FIELDS + (
    "validator_version",
    "preflight_timestamp_or_revision",
    "packet_digest",
)

@dataclass(frozen=True)
class CompletedReviewPacketPreflight:
    packet: SourceAcquisitionReviewPacket
    validator_version: str = REVIEW_PACKET_VALIDATOR_VERSION
    preflight_timestamp_or_revision: str = "UNSET"
    packet_digest: str = "UNCOMPUTED"
    preflight_decision: str = "NO_PACKET_SUPPLIED"
    ready_for_import_attempt: bool = False
    physical_export_requested: bool = False


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def _res(name: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    return {
        "passed": bool(passed),
        "status": "PASS" if passed else "FAIL",
        "tier": 4,
        "epistemic": W_REVIEW_PACKET_VALIDATOR_STATUS,
        "check": name,
        **extra,
    }


def _entry_from_raw(raw: Any) -> SourceCandidateEntry | Any:
    if isinstance(raw, SourceCandidateEntry):
        return raw
    if isinstance(raw, Mapping):
        d = dict(raw)
        if "intended_component_coverage" in d:
            d["intended_component_coverage"] = tuple(d["intended_component_coverage"])
        return SourceCandidateEntry(**d)
    return raw


def _packet_from_raw(raw: SourceAcquisitionReviewPacket | Mapping[str, Any]) -> SourceAcquisitionReviewPacket:
    if isinstance(raw, SourceAcquisitionReviewPacket):
        return raw
    d = dict(raw)
    entry = _entry_from_raw(d.get("candidate_entry", {}))
    return SourceAcquisitionReviewPacket(
        packet_id=d.get("packet_id", ""),
        candidate_entry=entry,
        reviewer_or_process=d.get("reviewer_or_process", "UNREVIEWED"),
        review_decision=d.get("review_decision", "TEMPLATE_ONLY_DO_NOT_IMPORT"),
        review_notes_digest=d.get("review_notes_digest", "UNCOMPUTED"),
        evidence_bundle_digest=d.get("evidence_bundle_digest", "UNCOMPUTED"),
        worksheet_sections_completed=tuple(d.get("worksheet_sections_completed") or ()),
        preimport_steps_attested=tuple(d.get("preimport_steps_attested") or ()),
        forbidden_input_audit_passed=bool(d.get("forbidden_input_audit_passed")),
        template_only=bool(d.get("template_only", True)),
        physical_export_requested=bool(d.get("physical_export_requested")),
    )


def _has_forbidden_text(obj: Any) -> bool:
    """Detect target-observable/backsolve tokens in free-text packet fields.

    The packet schema legitimately carries *names* of forbidden-input audit
    predicates and pre-import steps such as "confirm_independent_of_observed_W_mass".
    Those policy labels must not themselves trip the validator.  This scanner is
    therefore applied to free-text provenance/review fields only.
    """
    if isinstance(obj, SourceAcquisitionReviewPacket):
        d = asdict(obj)
    elif isinstance(obj, Mapping):
        d = dict(obj)
    else:
        d = {"value": obj}
    candidate = d.get("candidate_entry", {}) or {}
    if isinstance(candidate, SourceCandidateEntry):
        candidate = asdict(candidate)
    fields = (
        d.get("packet_id", ""),
        d.get("reviewer_or_process", ""),
        d.get("review_notes_digest", ""),
        d.get("evidence_bundle_digest", ""),
        candidate.get("source_candidate_id", "") if isinstance(candidate, Mapping) else "",
        candidate.get("public_or_archival_locator", "") if isinstance(candidate, Mapping) else "",
        candidate.get("version_or_revision_id", "") if isinstance(candidate, Mapping) else "",
        candidate.get("license_or_access_note", "") if isinstance(candidate, Mapping) else "",
        candidate.get("extraction_method", "") if isinstance(candidate, Mapping) else "",
        candidate.get("scheme_and_gauge_policy_note", "") if isinstance(candidate, Mapping) else "",
        candidate.get("counterterm_convention_note", "") if isinstance(candidate, Mapping) else "",
    )
    text = "\n".join(str(x) for x in fields)
    for token in FORBIDDEN_ACQUISITION_INPUTS:
        if token in text:
            return True
    aliases = ("observed_W", "world_average_W", "APF-anchor", "Delta_r_target_backsolve")
    return any(alias in text for alias in aliases)


def packet_digest_ok(digest: str) -> bool:
    if not isinstance(digest, str) or not digest.startswith("sha256:"):
        return False
    suffix = digest.split(":", 1)[1]
    return len(suffix) == 64 and all(ch in "0123456789abcdef" for ch in suffix.lower())


def default_completed_packet_preflight() -> CompletedReviewPacketPreflight:
    return CompletedReviewPacketPreflight(packet=default_review_packet())


def promoted_completed_packet_preflight() -> CompletedReviewPacketPreflight:
    return CompletedReviewPacketPreflight(
        packet=promoted_review_packet(),
        preflight_timestamp_or_revision="review-revision-0001",
        packet_digest="sha256:" + "1" * 64,
        preflight_decision="READY_FOR_IMPORT_ATTEMPT",
        ready_for_import_attempt=True,
        physical_export_requested=False,
    )


def validate_completed_review_packet_preflight(
    preflight: CompletedReviewPacketPreflight | Mapping[str, Any]
) -> Dict[str, Any]:
    if isinstance(preflight, CompletedReviewPacketPreflight):
        packet = preflight.packet
        d = asdict(preflight)
    else:
        d = dict(preflight)
        packet = _packet_from_raw(d.get("packet", d))
    packet_dict = asdict(packet)
    reasons = []
    if d.get("validator_version") != REVIEW_PACKET_VALIDATOR_VERSION:
        reasons.append("wrong_validator_version")
    if d.get("preflight_decision") != "READY_FOR_IMPORT_ATTEMPT":
        reasons.append("not_ready_decision")
    if d.get("ready_for_import_attempt") is not True:
        reasons.append("ready_flag_false")
    if d.get("physical_export_requested") or packet.physical_export_requested:
        reasons.append("physical_export_requested")
    if packet.template_only:
        reasons.append("template_only_packet")
    if str(packet.reviewer_or_process) in {"", "UNREVIEWED", "None"}:
        reasons.append("missing_reviewer_or_process")
    if str(d.get("preflight_timestamp_or_revision", "")) in {"", "UNSET", "None"}:
        reasons.append("missing_preflight_revision")
    if not packet_digest_ok(str(d.get("packet_digest", ""))):
        reasons.append("bad_packet_digest")
    if not review_packet_complete_for_import_attempt(packet):
        reasons.append("v11_6_packet_not_complete")
    if not candidate_complete_for_import(packet.candidate_entry):
        reasons.append("candidate_not_complete")
    if _has_forbidden_text(packet):
        reasons.append("forbidden_input_token_present")
    ok = not reasons
    return {
        "passed": ok,
        "status": "PASS" if ok else "FAIL",
        "decision": "READY_FOR_IMPORT_ATTEMPT" if ok else "REJECT_TEMPLATE_OR_INCOMPLETE_PACKET",
        "reasons": tuple(reasons),
        "packet_id": packet.packet_id,
        "validator_version": d.get("validator_version"),
        "ready_for_import_attempt": bool(ok),
        "physical_export_enabled": False,
        "exports_physical_M_W": False,
    }


def review_packet_validator_report() -> Dict[str, Any]:
    ready = readiness_report(physical_export_requested=False)
    default_pf = default_completed_packet_preflight()
    promoted_pf = promoted_completed_packet_preflight()
    return {
        "status": W_REVIEW_PACKET_VALIDATOR_STATUS,
        "version": REVIEW_PACKET_VALIDATOR_VERSION,
        "mode": REVIEW_PACKET_VALIDATOR_MODE,
        "upstream_review_packet_status": W_SOURCE_ACQUISITION_REVIEW_PACKET_STATUS,
        "preflight_decisions": PREFLIGHT_DECISIONS,
        "validator_required_fields": VALIDATOR_REQUIRED_FIELDS,
        "review_packet_required_fields": REQUIRED_REVIEW_PACKET_FIELDS,
        "review_packet_sections": REVIEW_PACKET_SECTIONS,
        "review_decisions": REVIEW_DECISIONS,
        "required_preimport_steps": REQUIRED_PREIMPORT_STEPS,
        "forbidden_acquisition_inputs": FORBIDDEN_ACQUISITION_INPUTS,
        "default_preflight": asdict(default_pf),
        "default_preflight_validated": validate_completed_review_packet_preflight(default_pf)["passed"],
        "promoted_preflight_validated": validate_completed_review_packet_preflight(promoted_pf)["passed"],
        "real_completed_review_packet_shipped": REAL_COMPLETED_REVIEW_PACKET_SHIPPED,
        "real_completed_review_packet_validated": REAL_COMPLETED_REVIEW_PACKET_VALIDATED,
        "real_external_source_acquired": REAL_EXTERNAL_SOURCE_ACQUIRED,
        "real_external_rows_imported": REAL_EXTERNAL_ROWS_IMPORTED,
        "real_external_rows_admitted": REAL_EXTERNAL_ROWS_ADMITTED,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "covariance_certified": COVARIANCE_CERTIFIED,
        "uncertainty_propagation_certified": UNCERTAINTY_PROPAGATION_CERTIFIED,
        "physical_W_export_enabled": PHYSICAL_W_EXPORT_ENABLED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "readiness_locked": not ready["physical_W_export_ready"] and not ready["physical_W_export_enabled"],
        "validator_doc_path": str(VALIDATOR_DOC_PATH),
        "validator_template_dir": str(VALIDATOR_TEMPLATE_DIR),
        "validator_packet_template_path": str(VALIDATOR_PACKET_TEMPLATE_PATH),
    }


def check_T_w_review_packet_validator_status_declared():
    r = review_packet_validator_report(); ok = r["status"] == W_REVIEW_PACKET_VALIDATOR_STATUS and not r["physical_W_export_enabled"]
    return _res("status_declared", ok, report=r)


def check_T_w_review_packet_validator_depends_on_v116_review_packet():
    d = _check_v116(); return _res("depends_on_v116_review_packet", _passed(d), upstream=d.get("status"))


def check_T_w_review_packet_validator_preflight_decisions_declared():
    ok = set(PREFLIGHT_DECISIONS) == {"NO_PACKET_SUPPLIED", "REJECT_TEMPLATE_OR_INCOMPLETE_PACKET", "REJECT_FORBIDDEN_INPUT_CONSUMPTION", "READY_FOR_IMPORT_ATTEMPT"}
    return _res("preflight_decisions_declared", ok, decisions=PREFLIGHT_DECISIONS)


def check_T_w_review_packet_validator_required_fields_extend_packet():
    ok = set(REQUIRED_REVIEW_PACKET_FIELDS).issubset(set(VALIDATOR_REQUIRED_FIELDS)) and {"validator_version", "packet_digest"}.issubset(set(VALIDATOR_REQUIRED_FIELDS))
    return _res("required_fields_extend_packet", ok, fields=VALIDATOR_REQUIRED_FIELDS)


def check_T_w_review_packet_validator_default_packet_rejected():
    pf = default_completed_packet_preflight(); v = validate_completed_review_packet_preflight(pf)
    return _res("default_packet_rejected", not v["passed"], validation=v)


def check_T_w_review_packet_validator_promoted_packet_validates():
    pf = promoted_completed_packet_preflight(); v = validate_completed_review_packet_preflight(pf)
    return _res("promoted_packet_validates", v["passed"], validation=v)


def check_T_w_review_packet_validator_rejects_template_packet():
    pf = replace(promoted_completed_packet_preflight(), packet=replace(promoted_review_packet(), template_only=True))
    v = validate_completed_review_packet_preflight(pf)
    return _res("rejects_template_packet", not v["passed"] and "template_only_packet" in v["reasons"], validation=v)


def check_T_w_review_packet_validator_rejects_physical_export_request():
    p = replace(promoted_review_packet(), physical_export_requested=True)
    pf = replace(promoted_completed_packet_preflight(), packet=p, physical_export_requested=True)
    v = validate_completed_review_packet_preflight(pf)
    return _res("rejects_physical_export_request", not v["passed"] and "physical_export_requested" in v["reasons"], validation=v)


def check_T_w_review_packet_validator_rejects_missing_reviewer():
    p = replace(promoted_review_packet(), reviewer_or_process="UNREVIEWED")
    pf = replace(promoted_completed_packet_preflight(), packet=p)
    v = validate_completed_review_packet_preflight(pf)
    return _res("rejects_missing_reviewer", not v["passed"], validation=v)


def check_T_w_review_packet_validator_rejects_wrong_decision():
    p = replace(promoted_review_packet(), review_decision="NEEDS_MORE_EVIDENCE")
    pf = replace(promoted_completed_packet_preflight(), packet=p)
    v = validate_completed_review_packet_preflight(pf)
    return _res("rejects_wrong_decision", not v["passed"], validation=v)


def check_T_w_review_packet_validator_rejects_missing_section():
    p = replace(promoted_review_packet(), worksheet_sections_completed=REVIEW_PACKET_SECTIONS[:-1])
    pf = replace(promoted_completed_packet_preflight(), packet=p)
    v = validate_completed_review_packet_preflight(pf)
    return _res("rejects_missing_section", not v["passed"], validation=v)


def check_T_w_review_packet_validator_rejects_wrong_section_order():
    sections = tuple(reversed(REVIEW_PACKET_SECTIONS))
    p = replace(promoted_review_packet(), worksheet_sections_completed=sections)
    pf = replace(promoted_completed_packet_preflight(), packet=p)
    v = validate_completed_review_packet_preflight(pf)
    return _res("rejects_wrong_section_order", not v["passed"], validation=v)


def check_T_w_review_packet_validator_rejects_missing_preimport_step():
    p = replace(promoted_review_packet(), preimport_steps_attested=REQUIRED_PREIMPORT_STEPS[:-1])
    pf = replace(promoted_completed_packet_preflight(), packet=p)
    v = validate_completed_review_packet_preflight(pf)
    return _res("rejects_missing_preimport_step", not v["passed"], validation=v)


def check_T_w_review_packet_validator_rejects_missing_review_digest():
    p = replace(promoted_review_packet(), review_notes_digest="UNCOMPUTED")
    pf = replace(promoted_completed_packet_preflight(), packet=p)
    v = validate_completed_review_packet_preflight(pf)
    return _res("rejects_missing_review_digest", not v["passed"], validation=v)


def check_T_w_review_packet_validator_rejects_bad_packet_digest():
    pf = replace(promoted_completed_packet_preflight(), packet_digest="sha256:not64hex")
    v = validate_completed_review_packet_preflight(pf)
    return _res("rejects_bad_packet_digest", not v["passed"] and "bad_packet_digest" in v["reasons"], validation=v)


def check_T_w_review_packet_validator_rejects_missing_evidence_digest():
    p = replace(promoted_review_packet(), evidence_bundle_digest="UNCOMPUTED")
    pf = replace(promoted_completed_packet_preflight(), packet=p)
    v = validate_completed_review_packet_preflight(pf)
    return _res("rejects_missing_evidence_digest", not v["passed"], validation=v)


def check_T_w_review_packet_validator_rejects_candidate_template_only():
    p = promoted_review_packet()
    e = replace(p.candidate_entry, synthetic_or_template_only=True)
    pf = replace(promoted_completed_packet_preflight(), packet=replace(p, candidate_entry=e))
    v = validate_completed_review_packet_preflight(pf)
    return _res("rejects_candidate_template_only", not v["passed"], validation=v)


def check_T_w_review_packet_validator_rejects_candidate_forbidden_input():
    p = promoted_review_packet()
    e = replace(p.candidate_entry, consumes_forbidden_input=True, forbidden_input_audit_plan="FAILED_USED_OBSERVED_W")
    pf = replace(promoted_completed_packet_preflight(), packet=replace(p, candidate_entry=e, forbidden_input_audit_passed=False))
    v = validate_completed_review_packet_preflight(pf)
    return _res("rejects_candidate_forbidden_input", not v["passed"], validation=v)


def check_T_w_review_packet_validator_rejects_observed_W_token():
    p = replace(promoted_review_packet(), review_notes_digest="sha256:" + "2" * 64, reviewer_or_process="reviewed observed_M_W source")
    pf = replace(promoted_completed_packet_preflight(), packet=p)
    v = validate_completed_review_packet_preflight(pf)
    return _res("rejects_observed_W_token", not v["passed"] and "forbidden_input_token_present" in v["reasons"], validation=v)


def check_T_w_review_packet_validator_rejects_APF_anchor_token():
    p = replace(promoted_review_packet(), reviewer_or_process="reviewed APF_ANCHOR_DELTA_R_TARGET table")
    pf = replace(promoted_completed_packet_preflight(), packet=p)
    v = validate_completed_review_packet_preflight(pf)
    return _res("rejects_APF_anchor_token", not v["passed"] and "forbidden_input_token_present" in v["reasons"], validation=v)


def check_T_w_review_packet_validator_rejects_incomplete_candidate():
    p = promoted_review_packet()
    e = replace(p.candidate_entry, public_or_archival_locator="UNACQUIRED")
    pf = replace(promoted_completed_packet_preflight(), packet=replace(p, candidate_entry=e))
    v = validate_completed_review_packet_preflight(pf)
    return _res("rejects_incomplete_candidate", not v["passed"], validation=v)


def check_T_w_review_packet_validator_report_locks_default_state():
    r = review_packet_validator_report(); ok = not r["real_completed_review_packet_shipped"] and not r["real_external_rows_imported"] and not r["physical_W_export_enabled"]
    return _res("report_locks_default_state", ok, report=r)


def check_T_w_review_packet_validator_promoted_ready_without_import_or_export():
    r = review_packet_validator_report(); ok = r["promoted_preflight_validated"] and not r["real_external_rows_imported"] and not r["exports_physical_M_W"]
    return _res("promoted_ready_without_import_or_export", ok, report=r)


def check_T_w_review_packet_validator_readiness_lock_unchanged():
    r = review_packet_validator_report(); ok = r["readiness_locked"] and not r["physical_W_export_enabled"]
    return _res("readiness_lock_unchanged", ok, report=r)


def check_T_w_review_packet_validator_no_rows_or_certificates():
    r = review_packet_validator_report(); ok = not r["real_external_rows_admitted"] and not r["component_sum_certified"] and not r["covariance_certified"] and not r["uncertainty_propagation_certified"]
    return _res("no_rows_or_certificates", ok, report=r)


def check_T_w_review_packet_validator_schema_serializes_json():
    text = json.dumps(asdict(promoted_completed_packet_preflight()), sort_keys=True, default=str)
    ok = "READY_FOR_IMPORT_ATTEMPT" in text and REVIEW_PACKET_VALIDATOR_VERSION in text and "physical_export_requested" in text
    return _res("schema_serializes_json", ok, json_length=len(text))


def check_T_w_review_packet_validator_doc_exists():
    return _res("doc_exists", VALIDATOR_DOC_PATH.exists(), path=str(VALIDATOR_DOC_PATH))


def check_T_w_review_packet_validator_doc_warns_locked():
    text = VALIDATOR_DOC_PATH.read_text(encoding="utf-8") if VALIDATOR_DOC_PATH.exists() else ""
    needed = ("No real completed packet is shipped", "observed M_W", "APF-anchor", "physical W export remains locked")
    ok = all(s in text for s in needed)
    return _res("doc_warns_locked", ok, needed=needed)


def check_T_w_review_packet_validator_template_dir_exists():
    return _res("template_dir_exists", VALIDATOR_TEMPLATE_DIR.exists(), path=str(VALIDATOR_TEMPLATE_DIR))


def check_T_w_review_packet_validator_json_template_exists():
    return _res("json_template_exists", VALIDATOR_PACKET_TEMPLATE_PATH.exists(), path=str(VALIDATOR_PACKET_TEMPLATE_PATH))


def check_T_w_review_packet_validator_json_template_not_importable():
    if not VALIDATOR_PACKET_TEMPLATE_PATH.exists():
        return _res("json_template_not_importable", False, path=str(VALIDATOR_PACKET_TEMPLATE_PATH))
    data = json.loads(VALIDATOR_PACKET_TEMPLATE_PATH.read_text(encoding="utf-8"))
    v = validate_completed_review_packet_preflight(data)
    ok = not v["passed"] and data.get("packet", {}).get("template_only") is True
    return _res("json_template_not_importable", ok, validation=v)


def check_T_w_review_packet_validator_bank_closure():
    rows = [fn() for name, fn in CHECKS.items() if name != "T_w_review_packet_validator_bank_closure"]
    r = review_packet_validator_report()
    ok = all(_passed(x) for x in rows) and not r["default_preflight_validated"] and r["promoted_preflight_validated"] and not r["physical_W_export_enabled"]
    return _res("bank_closure", ok, passed_count=sum(_passed(x) for x in rows), total=len(rows), report=r)


CHECKS: Dict[str, Any] = {
    "T_w_review_packet_validator_status_declared": check_T_w_review_packet_validator_status_declared,
    "T_w_review_packet_validator_depends_on_v116_review_packet": check_T_w_review_packet_validator_depends_on_v116_review_packet,
    "T_w_review_packet_validator_preflight_decisions_declared": check_T_w_review_packet_validator_preflight_decisions_declared,
    "T_w_review_packet_validator_required_fields_extend_packet": check_T_w_review_packet_validator_required_fields_extend_packet,
    "T_w_review_packet_validator_default_packet_rejected": check_T_w_review_packet_validator_default_packet_rejected,
    "T_w_review_packet_validator_promoted_packet_validates": check_T_w_review_packet_validator_promoted_packet_validates,
    "T_w_review_packet_validator_rejects_template_packet": check_T_w_review_packet_validator_rejects_template_packet,
    "T_w_review_packet_validator_rejects_physical_export_request": check_T_w_review_packet_validator_rejects_physical_export_request,
    "T_w_review_packet_validator_rejects_missing_reviewer": check_T_w_review_packet_validator_rejects_missing_reviewer,
    "T_w_review_packet_validator_rejects_wrong_decision": check_T_w_review_packet_validator_rejects_wrong_decision,
    "T_w_review_packet_validator_rejects_missing_section": check_T_w_review_packet_validator_rejects_missing_section,
    "T_w_review_packet_validator_rejects_wrong_section_order": check_T_w_review_packet_validator_rejects_wrong_section_order,
    "T_w_review_packet_validator_rejects_missing_preimport_step": check_T_w_review_packet_validator_rejects_missing_preimport_step,
    "T_w_review_packet_validator_rejects_missing_review_digest": check_T_w_review_packet_validator_rejects_missing_review_digest,
    "T_w_review_packet_validator_rejects_bad_packet_digest": check_T_w_review_packet_validator_rejects_bad_packet_digest,
    "T_w_review_packet_validator_rejects_missing_evidence_digest": check_T_w_review_packet_validator_rejects_missing_evidence_digest,
    "T_w_review_packet_validator_rejects_candidate_template_only": check_T_w_review_packet_validator_rejects_candidate_template_only,
    "T_w_review_packet_validator_rejects_candidate_forbidden_input": check_T_w_review_packet_validator_rejects_candidate_forbidden_input,
    "T_w_review_packet_validator_rejects_observed_W_token": check_T_w_review_packet_validator_rejects_observed_W_token,
    "T_w_review_packet_validator_rejects_APF_anchor_token": check_T_w_review_packet_validator_rejects_APF_anchor_token,
    "T_w_review_packet_validator_rejects_incomplete_candidate": check_T_w_review_packet_validator_rejects_incomplete_candidate,
    "T_w_review_packet_validator_report_locks_default_state": check_T_w_review_packet_validator_report_locks_default_state,
    "T_w_review_packet_validator_promoted_ready_without_import_or_export": check_T_w_review_packet_validator_promoted_ready_without_import_or_export,
    "T_w_review_packet_validator_readiness_lock_unchanged": check_T_w_review_packet_validator_readiness_lock_unchanged,
    "T_w_review_packet_validator_no_rows_or_certificates": check_T_w_review_packet_validator_no_rows_or_certificates,
    "T_w_review_packet_validator_schema_serializes_json": check_T_w_review_packet_validator_schema_serializes_json,
    "T_w_review_packet_validator_doc_exists": check_T_w_review_packet_validator_doc_exists,
    "T_w_review_packet_validator_doc_warns_locked": check_T_w_review_packet_validator_doc_warns_locked,
    "T_w_review_packet_validator_template_dir_exists": check_T_w_review_packet_validator_template_dir_exists,
    "T_w_review_packet_validator_json_template_exists": check_T_w_review_packet_validator_json_template_exists,
    "T_w_review_packet_validator_json_template_not_importable": check_T_w_review_packet_validator_json_template_not_importable,
    "T_w_review_packet_validator_bank_closure": check_T_w_review_packet_validator_bank_closure,
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
        "status": "W_TRACE_REVIEW_PACKET_VALIDATOR_BANK_PASS" if ok else "W_TRACE_REVIEW_PACKET_VALIDATOR_BANK_FAIL",
        "checks": rows,
        "manifest": review_packet_validator_report(),
    }
