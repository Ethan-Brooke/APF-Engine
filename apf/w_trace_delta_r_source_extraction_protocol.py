"""W_TRACE standard Delta_r source-extraction protocol / candidate worksheet.

Physics-source acquisition module for v13.3.  v13.1 admitted the standard
Delta_r source shapes, and v13.2 named concrete literature/source candidates.
This module converts the candidate registry into an executable extraction
protocol: every candidate must pass a completed worksheet before it can become
a reviewed payload candidate.

The protocol is intentionally pre-admission.  It records source identity,
notation, input scheme, extracted quantities, provenance/digests, and explicit
anti-smuggling attestations.  It does not admit numerical Delta_r rows, does not
certify a component sum, and does not unlock physical W export.
"""
from __future__ import annotations

import copy
import json
import re
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Tuple

from apf import w_trace_delta_r_source_candidate_registry as candidates
from apf import w_trace_delta_r_source_mapping as srcmap

STATUS = "P_w_delta_r_source_extraction_protocol"
VERSION = "w_trace_delta_r_source_extraction_protocol_v1"
PASS_STATUS = "W_TRACE_DELTA_R_SOURCE_EXTRACTION_PROTOCOL_BANK_PASS"
TITLE = "W_TRACE standard Delta_r source-extraction protocol / candidate worksheet"

UPSTREAM_CANDIDATE_STATUS = candidates.STATUS
UPSTREAM_MAPPING_STATUS = srcmap.STATUS
STANDARD_PAYLOAD_KINDS = tuple(srcmap.ALLOWED_PAYLOAD_KINDS)
APF_DELTA_R_TARGET = srcmap.APF_DELTA_R_TARGET
M_W_TRACE_GEV = srcmap.M_W_TRACE_GEV

WORKSHEET_STATES = (
    "template_only",
    "draft_unreviewed",
    "review_ready",
    "reviewed_pre_admission",
    "rejected",
)

EXTRACTION_PAYLOAD_KINDS = STANDARD_PAYLOAD_KINDS + (
    "constants_reference",
    "counterterm_structure_reference",
    "definition_lineage_reference",
)

WORKSHEET_REQUIRED_FIELDS = (
    "worksheet_version",
    "candidate_id",
    "candidate_role",
    "source_locator",
    "source_version_or_date",
    "source_digest",
    "extraction_owner",
    "reviewer",
    "extraction_state",
    "payload_kind",
    "input_scheme",
    "notation_mapping",
    "extracted_quantities",
    "uncertainty_fields",
    "provenance_notes_digest",
    "observed_w_exclusion_attested",
    "apf_anchor_exclusion_attested",
    "target_fit_exclusion_attested",
    "physical_export_requested",
)

NOTATION_MAPPING_REQUIRED_KEYS = (
    "source_delta_r_symbol",
    "source_delta_alpha_symbol",
    "source_delta_rho_symbol",
    "source_remainder_symbol",
    "source_counterterm_symbol",
    "notes",
)

INPUT_SCHEME_REQUIRED_KEYS = (
    "alpha_reference",
    "G_F_reference",
    "M_Z_reference",
    "M_H_reference_policy",
    "m_t_reference_policy",
    "renormalization_scheme",
)

FORBIDDEN_TOKENS = tuple(candidates.FORBIDDEN_TOKENS) + (
    "observed_M_W",
    "world_average_M_W",
    "M_W_world_average",
    "APF_DELTA_R_TARGET_AS_INPUT",
    "Delta_r_target_backsolve",
    "fit_to_M_W_TRACE",
    "tune_to_APF_anchor",
    "manual_export_override",
)

TEMPLATE_TOKENS = (
    "TODO",
    "TBD",
    "FILL_ME",
    "template_only",
    "example_only",
    "not_a_real_source",
)

LOCKED_STATE = {
    "source_extraction_protocol_banked": True,
    "real_completed_extraction_worksheet_shipped": False,
    "real_delta_r_source_admitted": False,
    "real_delta_r_payload_rows_imported": False,
    "component_sum_certified": False,
    "covariance_certified": False,
    "uncertainty_propagation_certified": False,
    "physical_W_export_enabled": False,
    "exports_physical_M_W": False,
}


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _contains_token(obj: Any, tokens: Iterable[str]) -> bool:
    text = _canonical_json(obj)
    return any(tok in text for tok in tokens)


def _contains_forbidden_token(obj: Any) -> bool:
    return _contains_token(obj, FORBIDDEN_TOKENS)


def _contains_template_token(obj: Any) -> bool:
    return _contains_token(obj, TEMPLATE_TOKENS)


def _res(check: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    row = {"check": check, "passed": bool(passed)}
    row.update(extra)
    return row


def _passed(row: Any) -> bool:
    return bool(isinstance(row, dict) and row.get("passed") is True)


def terminal_report() -> Dict[str, Any]:
    return {
        "status": STATUS,
        "version": VERSION,
        "title": TITLE,
        "upstream_candidate_status": UPSTREAM_CANDIDATE_STATUS,
        "upstream_mapping_status": UPSTREAM_MAPPING_STATUS,
        "worksheet_states": list(WORKSHEET_STATES),
        "required_fields": list(WORKSHEET_REQUIRED_FIELDS),
        "notation_mapping_required_keys": list(NOTATION_MAPPING_REQUIRED_KEYS),
        "input_scheme_required_keys": list(INPUT_SCHEME_REQUIRED_KEYS),
        "payload_kinds": list(EXTRACTION_PAYLOAD_KINDS),
        "candidate_order": list(candidates.build_acquisition_priority()),
        "apf_comparison_target": {
            "Delta_r_APF_TRACE_target": APF_DELTA_R_TARGET,
            "M_W_TRACE_GeV": M_W_TRACE_GEV,
            "role": "comparison_only_after_independent_source_admission",
        },
        "locked_state": dict(LOCKED_STATE),
        "stop_rule": "A literature/source candidate may not become an admitted Delta_r payload until a non-template worksheet passes this protocol and the downstream admission gates remain export-locked.",
    }


def worksheet_payload_kind_for_candidate(candidate_id: str) -> str:
    plan = candidates.source_to_payload_plan(candidate_id)
    if not plan.get("valid_candidate"):
        return "unknown_candidate"
    role = plan["role"]
    supported = tuple(plan.get("payload_kinds_supported", ()))
    if "standard_delta_r_parametrization" in supported:
        return "standard_delta_r_parametrization"
    if "standard_delta_r_decomposition" in supported:
        return "standard_delta_r_decomposition"
    if role == "input_constant_source":
        return "constants_reference"
    if role == "counterterm_scheme_structure":
        return "counterterm_structure_reference"
    if role == "definition_lineage":
        return "definition_lineage_reference"
    return "standard_delta_r_total"


def build_extraction_worksheet(candidate_id: str) -> Dict[str, Any]:
    plan = candidates.source_to_payload_plan(candidate_id)
    role = plan.get("role", "unknown")
    return {
        "worksheet_version": VERSION,
        "candidate_id": candidate_id,
        "candidate_role": role,
        "source_locator": "TODO: canonical DOI/arXiv/PDG/NIST/URL locator",
        "source_version_or_date": "TODO: source version/date",
        "source_digest": "TODO: sha256 digest of source or extracted table",
        "extraction_owner": "TODO: extractor identity",
        "reviewer": "TODO: independent reviewer identity",
        "extraction_state": "template_only",
        "payload_kind": worksheet_payload_kind_for_candidate(candidate_id),
        "input_scheme": {
            "alpha_reference": "TODO",
            "G_F_reference": "TODO",
            "M_Z_reference": "TODO",
            "M_H_reference_policy": "TODO",
            "m_t_reference_policy": "TODO",
            "renormalization_scheme": "on_shell_or_declared_source_scheme",
        },
        "notation_mapping": {
            "source_delta_r_symbol": "TODO",
            "source_delta_alpha_symbol": "TODO or not_applicable",
            "source_delta_rho_symbol": "TODO or not_applicable",
            "source_remainder_symbol": "TODO or not_applicable",
            "source_counterterm_symbol": "TODO or not_applicable",
            "notes": "TODO: map source notation to standard APF Delta_r source schema",
        },
        "extracted_quantities": [],
        "uncertainty_fields": [],
        "provenance_notes_digest": "TODO: sha256 digest of extraction notes",
        "observed_w_exclusion_attested": False,
        "apf_anchor_exclusion_attested": False,
        "target_fit_exclusion_attested": False,
        "physical_export_requested": False,
    }


def build_completed_synthetic_worksheet(candidate_id: str) -> Dict[str, Any]:
    """Build a syntactically complete non-real worksheet for verifier dry-paths.

    It is marked reviewed_pre_admission and contains no numerical source rows.
    This is used only to prove the worksheet validator admits shape-complete
    non-template metadata while still refusing physical export.
    """
    plan = candidates.source_to_payload_plan(candidate_id)
    if not plan.get("valid_candidate"):
        raise KeyError(candidate_id)
    w = build_extraction_worksheet(candidate_id)
    w.update({
        "source_locator": f"synthetic://reviewed-source/{candidate_id}",
        "source_version_or_date": "2026-05-09-synthetic-preflight",
        "source_digest": "sha256:" + "a" * 64,
        "extraction_owner": "apf-source-extraction-preflight",
        "reviewer": "apf-independent-review-preflight",
        "extraction_state": "reviewed_pre_admission",
        "provenance_notes_digest": "sha256:" + "b" * 64,
        "observed_w_exclusion_attested": True,
        "apf_anchor_exclusion_attested": True,
        "target_fit_exclusion_attested": True,
        "physical_export_requested": False,
    })
    w["input_scheme"] = {
        "alpha_reference": "declared_external_reference_no_observed_W",
        "G_F_reference": "declared_external_reference_no_observed_W",
        "M_Z_reference": "declared_external_reference_no_observed_W",
        "M_H_reference_policy": "source_declared_or_not_applicable",
        "m_t_reference_policy": "source_declared_or_not_applicable",
        "renormalization_scheme": "on_shell_or_declared_source_scheme",
    }
    w["notation_mapping"] = {
        "source_delta_r_symbol": "Delta_r",
        "source_delta_alpha_symbol": "Delta_alpha_or_not_applicable",
        "source_delta_rho_symbol": "Delta_rho_or_not_applicable",
        "source_remainder_symbol": "Delta_r_rem_or_not_applicable",
        "source_counterterm_symbol": "Delta_r_ct_OS_or_not_applicable",
        "notes": "synthetic preflight mapping; no APF target or observed W consumed",
    }
    if w["payload_kind"] in STANDARD_PAYLOAD_KINDS:
        w["extracted_quantities"] = ["Delta_r_source_shape_no_numeric_payload"]
        w["uncertainty_fields"] = ["source_uncertainty_shape_no_numeric_payload"]
    else:
        w["extracted_quantities"] = ["reference_or_structure_shape_no_numeric_payload"]
        w["uncertainty_fields"] = ["not_applicable_or_source_declared"]
    return w


def validate_extraction_worksheet(worksheet: Mapping[str, Any]) -> Dict[str, Any]:
    errors: List[str] = []
    for field in WORKSHEET_REQUIRED_FIELDS:
        if field not in worksheet:
            errors.append(f"missing_field:{field}")
    cid = worksheet.get("candidate_id")
    plan = candidates.source_to_payload_plan(str(cid)) if cid is not None else {"valid_candidate": False, "errors": ["missing_candidate_id"]}
    if not plan.get("valid_candidate"):
        errors.append("unknown_candidate_id")
    if worksheet.get("candidate_role") != plan.get("role") and plan.get("valid_candidate"):
        errors.append("candidate_role_mismatch")
    if worksheet.get("worksheet_version") != VERSION:
        errors.append("worksheet_version_mismatch")
    if worksheet.get("extraction_state") not in WORKSHEET_STATES:
        errors.append("unknown_extraction_state")
    if worksheet.get("payload_kind") not in EXTRACTION_PAYLOAD_KINDS:
        errors.append("unknown_payload_kind")
    if worksheet.get("extraction_state") == "template_only":
        errors.append("template_state_not_admissible")
    if _contains_template_token(worksheet):
        errors.append("template_token_detected")
    if _contains_forbidden_token(worksheet):
        errors.append("forbidden_token_detected")
    for key in INPUT_SCHEME_REQUIRED_KEYS:
        if key not in worksheet.get("input_scheme", {}):
            errors.append(f"missing_input_scheme_key:{key}")
    for key in NOTATION_MAPPING_REQUIRED_KEYS:
        if key not in worksheet.get("notation_mapping", {}):
            errors.append(f"missing_notation_mapping_key:{key}")
    if not worksheet.get("extracted_quantities"):
        errors.append("missing_extracted_quantities")
    if not worksheet.get("uncertainty_fields"):
        errors.append("missing_uncertainty_fields")
    for attest in ("observed_w_exclusion_attested", "apf_anchor_exclusion_attested", "target_fit_exclusion_attested"):
        if worksheet.get(attest) is not True:
            errors.append(f"missing_attestation:{attest}")
    if worksheet.get("physical_export_requested") is not False:
        errors.append("physical_export_request_forbidden")
    for digest_field in ("source_digest", "provenance_notes_digest"):
        digest = str(worksheet.get(digest_field, ""))
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
            errors.append(f"bad_digest:{digest_field}")
    return {
        "valid": not errors,
        "errors": errors,
        "candidate_id": cid,
        "payload_kind": worksheet.get("payload_kind"),
        "real_payload_admitted": False,
        "component_sum_certified": False,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
    }


def extraction_plan_for_candidate(candidate_id: str) -> Dict[str, Any]:
    plan = candidates.source_to_payload_plan(candidate_id)
    if not plan.get("valid_candidate"):
        return {"valid": False, "candidate_id": candidate_id, "errors": plan.get("errors", ["unknown_candidate_id"]), "physical_W_export_enabled": False}
    return {
        "valid": True,
        "candidate_id": candidate_id,
        "candidate_role": plan["role"],
        "tier": plan["tier"],
        "payload_kind": worksheet_payload_kind_for_candidate(candidate_id),
        "steps": [
            "locate_canonical_source",
            "record_source_version_and_digest",
            "map_source_notation_to_standard_delta_r_schema",
            "record_input_scheme_and_reference_constants",
            "extract_declared_quantities_without_observed_W_or_APF_anchor",
            "record_uncertainty_fields_or_source_absence",
            "independent_review_and_forbidden_input_audit",
            "handoff_to_payload_admission_gates_without_export_unlock",
        ],
        "real_payload_admitted": False,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
    }


# Checks

def check_T_w_trace_delta_r_source_extraction_protocol_status_declared():
    return _res("status_declared", STATUS == "P_w_delta_r_source_extraction_protocol" and VERSION.endswith("_v1"))


def check_T_w_trace_delta_r_source_extraction_protocol_upstream_imports():
    return _res("upstream_imports", candidates.STATUS == "P_w_delta_r_source_candidate_registry" and srcmap.STATUS == "P_w_delta_r_source_mapping")


def check_T_w_trace_delta_r_source_extraction_protocol_payload_kinds_extend_standard():
    return _res("payload_kinds_extend_standard", set(STANDARD_PAYLOAD_KINDS).issubset(EXTRACTION_PAYLOAD_KINDS) and "constants_reference" in EXTRACTION_PAYLOAD_KINDS)


def check_T_w_trace_delta_r_source_extraction_protocol_required_fields_declared():
    return _res("required_fields_declared", len(WORKSHEET_REQUIRED_FIELDS) >= 18 and "observed_w_exclusion_attested" in WORKSHEET_REQUIRED_FIELDS)


def check_T_w_trace_delta_r_source_extraction_protocol_template_built_for_all_candidates():
    reg = candidates.registry()
    ok = all(build_extraction_worksheet(cid)["candidate_id"] == cid for cid in reg)
    return _res("template_built_for_all_candidates", ok, count=len(reg))


def check_T_w_trace_delta_r_source_extraction_protocol_template_rejected():
    w = build_extraction_worksheet("ACFW_precision_MW_parametrization")
    v = validate_extraction_worksheet(w)
    return _res("template_rejected", not v["valid"] and "template_state_not_admissible" in v["errors"] and "template_token_detected" in v["errors"])


def check_T_w_trace_delta_r_source_extraction_protocol_completed_synthetic_accepted_pre_admission():
    w = build_completed_synthetic_worksheet("ACFW_precision_MW_parametrization")
    v = validate_extraction_worksheet(w)
    return _res("completed_synthetic_accepted_pre_admission", v["valid"] and v["real_payload_admitted"] is False and v["physical_W_export_enabled"] is False)


def check_T_w_trace_delta_r_source_extraction_protocol_unknown_candidate_rejected():
    w = build_completed_synthetic_worksheet("ACFW_precision_MW_parametrization")
    w["candidate_id"] = "not_a_source"
    v = validate_extraction_worksheet(w)
    return _res("unknown_candidate_rejected", not v["valid"] and "unknown_candidate_id" in v["errors"])


def check_T_w_trace_delta_r_source_extraction_protocol_candidate_role_mismatch_rejected():
    w = build_completed_synthetic_worksheet("ACFW_precision_MW_parametrization")
    w["candidate_role"] = "input_constant_source"
    v = validate_extraction_worksheet(w)
    return _res("candidate_role_mismatch_rejected", not v["valid"] and "candidate_role_mismatch" in v["errors"])


def check_T_w_trace_delta_r_source_extraction_protocol_forbidden_token_rejected():
    w = build_completed_synthetic_worksheet("ACFW_precision_MW_parametrization")
    w["notation_mapping"]["notes"] = "observed_M_W used here"
    v = validate_extraction_worksheet(w)
    return _res("forbidden_token_rejected", not v["valid"] and "forbidden_token_detected" in v["errors"])


def check_T_w_trace_delta_r_source_extraction_protocol_attestations_required():
    w = build_completed_synthetic_worksheet("ACFW_precision_MW_parametrization")
    w["apf_anchor_exclusion_attested"] = False
    v = validate_extraction_worksheet(w)
    return _res("attestations_required", not v["valid"] and "missing_attestation:apf_anchor_exclusion_attested" in v["errors"])


def check_T_w_trace_delta_r_source_extraction_protocol_physical_export_request_rejected():
    w = build_completed_synthetic_worksheet("ACFW_precision_MW_parametrization")
    w["physical_export_requested"] = True
    v = validate_extraction_worksheet(w)
    return _res("physical_export_request_rejected", not v["valid"] and "physical_export_request_forbidden" in v["errors"])


def check_T_w_trace_delta_r_source_extraction_protocol_bad_digest_rejected():
    w = build_completed_synthetic_worksheet("ACFW_precision_MW_parametrization")
    w["source_digest"] = "not-a-digest"
    v = validate_extraction_worksheet(w)
    return _res("bad_digest_rejected", not v["valid"] and "bad_digest:source_digest" in v["errors"])


def check_T_w_trace_delta_r_source_extraction_protocol_input_scheme_keys_required():
    w = build_completed_synthetic_worksheet("ACFW_precision_MW_parametrization")
    del w["input_scheme"]["M_Z_reference"]
    v = validate_extraction_worksheet(w)
    return _res("input_scheme_keys_required", not v["valid"] and "missing_input_scheme_key:M_Z_reference" in v["errors"])


def check_T_w_trace_delta_r_source_extraction_protocol_notation_keys_required():
    w = build_completed_synthetic_worksheet("ACFW_precision_MW_parametrization")
    del w["notation_mapping"]["source_delta_r_symbol"]
    v = validate_extraction_worksheet(w)
    return _res("notation_keys_required", not v["valid"] and "missing_notation_mapping_key:source_delta_r_symbol" in v["errors"])


def check_T_w_trace_delta_r_source_extraction_protocol_acfw_gets_parametrization_kind():
    return _res("acfw_gets_parametrization_kind", worksheet_payload_kind_for_candidate("ACFW_precision_MW_parametrization") == "standard_delta_r_parametrization")


def check_T_w_trace_delta_r_source_extraction_protocol_denner_gets_decomposition_kind():
    return _res("denner_gets_decomposition_kind", worksheet_payload_kind_for_candidate("Denner_on_shell_renormalization_structure") == "standard_delta_r_decomposition")


def check_T_w_trace_delta_r_source_extraction_protocol_constants_get_reference_kind():
    return _res("constants_get_reference_kind", worksheet_payload_kind_for_candidate("NIST_CODATA_alpha_reference") == "constants_reference")


def check_T_w_trace_delta_r_source_extraction_protocol_extraction_plan_steps_ordered():
    p = extraction_plan_for_candidate("ACFW_precision_MW_parametrization")
    return _res("extraction_plan_steps_ordered", p["valid"] and p["steps"][0] == "locate_canonical_source" and p["steps"][-1].endswith("without_export_unlock"))


def check_T_w_trace_delta_r_source_extraction_protocol_unknown_plan_rejected():
    p = extraction_plan_for_candidate("missing")
    return _res("unknown_plan_rejected", not p["valid"] and p["physical_W_export_enabled"] is False)


def check_T_w_trace_delta_r_source_extraction_protocol_apf_anchor_comparison_only():
    r = terminal_report()["apf_comparison_target"]
    return _res("apf_anchor_comparison_only", r["Delta_r_APF_TRACE_target"] == APF_DELTA_R_TARGET and "comparison_only" in r["role"])


def check_T_w_trace_delta_r_source_extraction_protocol_locked_state_no_export():
    s = terminal_report()["locked_state"]
    return _res("locked_state_no_export", s["physical_W_export_enabled"] is False and s["exports_physical_M_W"] is False and s["real_delta_r_source_admitted"] is False)


def check_T_w_trace_delta_r_source_extraction_protocol_serializable():
    json.dumps(terminal_report(), sort_keys=True)
    json.dumps(build_extraction_worksheet("ACFW_precision_MW_parametrization"), sort_keys=True)
    json.dumps(validate_extraction_worksheet(build_completed_synthetic_worksheet("ACFW_precision_MW_parametrization")), sort_keys=True)
    return _res("serializable", True)


def check_T_w_trace_delta_r_source_extraction_protocol_priority_order_preserved():
    order = candidates.build_acquisition_priority()
    plans = [extraction_plan_for_candidate(cid) for cid in order]
    return _res("priority_order_preserved", plans[0]["candidate_id"] == "ACFW_precision_MW_parametrization" and all(p["valid"] for p in plans))


def check_T_w_trace_delta_r_source_extraction_protocol_bank_closure():
    checks = [fn for name, fn in CHECKS.items() if name != "T_w_trace_delta_r_source_extraction_protocol_bank_closure"]
    rows = [fn() for fn in checks]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))


CHECKS = {
    "T_w_trace_delta_r_source_extraction_protocol_status_declared": check_T_w_trace_delta_r_source_extraction_protocol_status_declared,
    "T_w_trace_delta_r_source_extraction_protocol_upstream_imports": check_T_w_trace_delta_r_source_extraction_protocol_upstream_imports,
    "T_w_trace_delta_r_source_extraction_protocol_payload_kinds_extend_standard": check_T_w_trace_delta_r_source_extraction_protocol_payload_kinds_extend_standard,
    "T_w_trace_delta_r_source_extraction_protocol_required_fields_declared": check_T_w_trace_delta_r_source_extraction_protocol_required_fields_declared,
    "T_w_trace_delta_r_source_extraction_protocol_template_built_for_all_candidates": check_T_w_trace_delta_r_source_extraction_protocol_template_built_for_all_candidates,
    "T_w_trace_delta_r_source_extraction_protocol_template_rejected": check_T_w_trace_delta_r_source_extraction_protocol_template_rejected,
    "T_w_trace_delta_r_source_extraction_protocol_completed_synthetic_accepted_pre_admission": check_T_w_trace_delta_r_source_extraction_protocol_completed_synthetic_accepted_pre_admission,
    "T_w_trace_delta_r_source_extraction_protocol_unknown_candidate_rejected": check_T_w_trace_delta_r_source_extraction_protocol_unknown_candidate_rejected,
    "T_w_trace_delta_r_source_extraction_protocol_candidate_role_mismatch_rejected": check_T_w_trace_delta_r_source_extraction_protocol_candidate_role_mismatch_rejected,
    "T_w_trace_delta_r_source_extraction_protocol_forbidden_token_rejected": check_T_w_trace_delta_r_source_extraction_protocol_forbidden_token_rejected,
    "T_w_trace_delta_r_source_extraction_protocol_attestations_required": check_T_w_trace_delta_r_source_extraction_protocol_attestations_required,
    "T_w_trace_delta_r_source_extraction_protocol_physical_export_request_rejected": check_T_w_trace_delta_r_source_extraction_protocol_physical_export_request_rejected,
    "T_w_trace_delta_r_source_extraction_protocol_bad_digest_rejected": check_T_w_trace_delta_r_source_extraction_protocol_bad_digest_rejected,
    "T_w_trace_delta_r_source_extraction_protocol_input_scheme_keys_required": check_T_w_trace_delta_r_source_extraction_protocol_input_scheme_keys_required,
    "T_w_trace_delta_r_source_extraction_protocol_notation_keys_required": check_T_w_trace_delta_r_source_extraction_protocol_notation_keys_required,
    "T_w_trace_delta_r_source_extraction_protocol_acfw_gets_parametrization_kind": check_T_w_trace_delta_r_source_extraction_protocol_acfw_gets_parametrization_kind,
    "T_w_trace_delta_r_source_extraction_protocol_denner_gets_decomposition_kind": check_T_w_trace_delta_r_source_extraction_protocol_denner_gets_decomposition_kind,
    "T_w_trace_delta_r_source_extraction_protocol_constants_get_reference_kind": check_T_w_trace_delta_r_source_extraction_protocol_constants_get_reference_kind,
    "T_w_trace_delta_r_source_extraction_protocol_extraction_plan_steps_ordered": check_T_w_trace_delta_r_source_extraction_protocol_extraction_plan_steps_ordered,
    "T_w_trace_delta_r_source_extraction_protocol_unknown_plan_rejected": check_T_w_trace_delta_r_source_extraction_protocol_unknown_plan_rejected,
    "T_w_trace_delta_r_source_extraction_protocol_apf_anchor_comparison_only": check_T_w_trace_delta_r_source_extraction_protocol_apf_anchor_comparison_only,
    "T_w_trace_delta_r_source_extraction_protocol_locked_state_no_export": check_T_w_trace_delta_r_source_extraction_protocol_locked_state_no_export,
    "T_w_trace_delta_r_source_extraction_protocol_serializable": check_T_w_trace_delta_r_source_extraction_protocol_serializable,
    "T_w_trace_delta_r_source_extraction_protocol_priority_order_preserved": check_T_w_trace_delta_r_source_extraction_protocol_priority_order_preserved,
}
CHECKS["T_w_trace_delta_r_source_extraction_protocol_bank_closure"] = check_T_w_trace_delta_r_source_extraction_protocol_bank_closure
_CHECKS = CHECKS


def register(registry: MutableMapping[str, Any]) -> None:
    registry.update(_CHECKS)


def run_all() -> Dict[str, Any]:
    rows = []
    for name, fn in _CHECKS.items():
        try:
            result = fn()
            rows.append({"name": name, "passed": _passed(result), "result": result})
        except Exception as exc:  # pragma: no cover
            rows.append({"name": name, "passed": False, "error": repr(exc)})
    ok = all(row["passed"] for row in rows)
    return {"passed": ok, "status": PASS_STATUS if ok else PASS_STATUS.replace("_PASS", "_FAIL"), "checks": rows, "report": terminal_report()}
