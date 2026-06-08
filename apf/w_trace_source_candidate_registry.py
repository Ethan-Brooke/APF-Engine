"""W_TRACE external-source acquisition checklist / source-candidate registry bank.

v11.5 (2026-05-09 LATER-50): source-acquisition registry above the
v11.4 payload template pack.  This module banks the checklist for finding and
qualifying an external finite-part source pack before it can be imported by the
v11.3 CLI / v10.x admission stack.  It deliberately ships with candidate
entries only: no external finite-part rows are admitted, no component-sum
certificate is issued, and no physical W/on-shell value is exported.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence, Tuple

from apf.w_trace_payload_template_pack import (
    W_PAYLOAD_TEMPLATE_PACK_STATUS,
    PAYLOAD_TEMPLATE_PACK_MODE,
    template_report,
    check_T_w_payload_template_pack_bank_closure as _check_v114,
)
from apf.w_trace_payload_import_cli import W_PAYLOAD_IMPORT_CLI_STATUS
from apf.w_trace_external_source_adapter import EXTERNAL_ADAPTER_VERSION
from apf.w_trace_real_source_candidate import REQUIRED_CANDIDATE_METADATA_FIELDS
from apf.w_trace_finite_part_skeleton import FINITE_PART_COMPONENT_ORDER
from apf.w_trace_final_export_readiness import readiness_report

W_SOURCE_CANDIDATE_REGISTRY_STATUS = "P_w_source_candidate_registry"
SOURCE_CANDIDATE_REGISTRY_VERSION = "w_trace_source_candidate_registry_v1"
SOURCE_CANDIDATE_REGISTRY_MODE = "ACQUISITION_CHECKLIST_AND_CANDIDATE_REGISTRY__NO_REAL_ROWS_ADMITTED"

REAL_EXTERNAL_SOURCE_ACQUIRED = False
REAL_EXTERNAL_ROWS_IMPORTED = False
REAL_EXTERNAL_ROWS_ADMITTED = False
COMPONENT_SUM_CERTIFIED = False
COVARIANCE_CERTIFIED = False
UNCERTAINTY_PROPAGATION_CERTIFIED = False
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False

REGISTRY_DOC_PATH = Path(__file__).resolve().parent.parent / "W_TRACE_SOURCE_CANDIDATE_REGISTRY_BANK_v1_0.md"

ALLOWED_SOURCE_CANDIDATE_CLASSES: Tuple[str, ...] = (
    "reviewed_literature_finite_part_table",
    "audited_loop_library_export",
    "independent_reimplementation_table",
    "collaboration_or_review_auxiliary_table",
)

REQUIRED_ACQUISITION_EVIDENCE_FIELDS: Tuple[str, ...] = (
    "source_candidate_id",
    "source_candidate_class",
    "intended_component_coverage",
    "public_or_archival_locator",
    "version_or_revision_id",
    "license_or_access_note",
    "extraction_method",
    "extraction_log_digest",
    "pack_digest_plan",
    "review_attestation_plan",
    "forbidden_input_audit_plan",
    "scheme_and_gauge_policy_note",
    "counterterm_convention_note",
)

REQUIRED_PREIMPORT_STEPS: Tuple[str, ...] = (
    "identify_candidate_source",
    "confirm_independent_of_observed_W_mass",
    "confirm_independent_of_APF_anchor_delta_r_target",
    "map_components_to_eight_slot_skeleton",
    "record_scheme_and_gauge_policy",
    "record_counterterm_convention_alignment",
    "extract_rows_into_v11_4_template_shape",
    "compute_payload_digest",
    "compute_extraction_log_digest",
    "run_v11_3_payload_import_cli",
    "run_v10_x_admission_stack",
    "keep_export_lock_closed_until_final_readiness_passes",
)

FORBIDDEN_ACQUISITION_INPUTS: Tuple[str, ...] = (
    "observed_M_W",
    "M_W_world_average",
    "world_average_W_mass",
    "W_mass_residual",
    "fit_residual_column",
    "APF_ANCHOR_DELTA_R_TARGET",
    "apf_anchor_delta_r_target",
    "component_sum_residual_to_apf_target",
    "posthoc_counterterm_fit",
    "physical_export_request",
)

@dataclass(frozen=True)
class SourceCandidateEntry:
    source_candidate_id: str
    source_candidate_class: str
    intended_component_coverage: Tuple[str, ...]
    public_or_archival_locator: str = "UNACQUIRED"
    version_or_revision_id: str = "UNACQUIRED"
    license_or_access_note: str = "UNACQUIRED"
    extraction_method: str = "UNSPECIFIED"
    extraction_log_digest: str = "UNCOMPUTED"
    pack_digest_plan: str = "UNCOMPUTED"
    review_attestation_plan: str = "PENDING"
    forbidden_input_audit_plan: str = "REQUIRED_BEFORE_IMPORT"
    scheme_and_gauge_policy_note: str = "REQUIRED_BEFORE_IMPORT"
    counterterm_convention_note: str = "REQUIRED_BEFORE_IMPORT"
    acquired: bool = False
    imported: bool = False
    admitted: bool = False
    synthetic_or_template_only: bool = False
    consumes_forbidden_input: bool = False
    exports_physical_mw: bool = False


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def _res(name: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    return {
        "passed": bool(passed),
        "status": "PASS" if passed else "FAIL",
        "tier": 4,
        "epistemic": W_SOURCE_CANDIDATE_REGISTRY_STATUS,
        "check": name,
        **extra,
    }


def candidate_registry() -> Tuple[SourceCandidateEntry, ...]:
    return (
        SourceCandidateEntry(
            source_candidate_id="reviewed_finite_part_table_candidate",
            source_candidate_class="reviewed_literature_finite_part_table",
            intended_component_coverage=FINITE_PART_COMPONENT_ORDER,
            extraction_method="manual_or_scripted_table_extraction_after_review",
        ),
        SourceCandidateEntry(
            source_candidate_id="audited_loop_library_export_candidate",
            source_candidate_class="audited_loop_library_export",
            intended_component_coverage=FINITE_PART_COMPONENT_ORDER,
            extraction_method="machine_export_with_reproducible_configuration_log",
        ),
        SourceCandidateEntry(
            source_candidate_id="independent_reimplementation_candidate",
            source_candidate_class="independent_reimplementation_table",
            intended_component_coverage=FINITE_PART_COMPONENT_ORDER,
            extraction_method="independent_code_generation_with_diffable_output_table",
        ),
        SourceCandidateEntry(
            source_candidate_id="review_auxiliary_table_candidate",
            source_candidate_class="collaboration_or_review_auxiliary_table",
            intended_component_coverage=FINITE_PART_COMPONENT_ORDER,
            extraction_method="archival_auxiliary_material_extraction_with_digest",
        ),
    )


def candidate_complete_for_import(entry: SourceCandidateEntry | Mapping[str, Any]) -> bool:
    d = asdict(entry) if isinstance(entry, SourceCandidateEntry) else dict(entry)
    if not all(k in d for k in REQUIRED_ACQUISITION_EVIDENCE_FIELDS):
        return False
    if d.get("source_candidate_class") not in ALLOWED_SOURCE_CANDIDATE_CLASSES:
        return False
    if tuple(d.get("intended_component_coverage") or ()) != FINITE_PART_COMPONENT_ORDER:
        return False
    if d.get("synthetic_or_template_only"):
        return False
    if d.get("consumes_forbidden_input") or d.get("exports_physical_mw"):
        return False
    required_nonplaceholder = (
        "public_or_archival_locator",
        "version_or_revision_id",
        "license_or_access_note",
        "extraction_method",
        "scheme_and_gauge_policy_note",
        "counterterm_convention_note",
    )
    for key in required_nonplaceholder:
        if str(d.get(key)) in {"", "UNACQUIRED", "UNSPECIFIED", "REQUIRED_BEFORE_IMPORT", "None"}:
            return False
    if not str(d.get("extraction_log_digest", "")).startswith("sha256:"):
        return False
    if not str(d.get("pack_digest_plan", "")).startswith("sha256:"):
        return False
    if d.get("review_attestation_plan") != "REVIEWED_INDEPENDENT_SOURCE_READY_FOR_IMPORT":
        return False
    if d.get("forbidden_input_audit_plan") != "PASSED_NO_FORBIDDEN_INPUTS":
        return False
    if d.get("acquired") is not True or d.get("imported") is not False or d.get("admitted") is not False:
        return False
    return True


def source_candidate_registry_report() -> Dict[str, Any]:
    tmpl = template_report()
    ready = readiness_report(physical_export_requested=False)
    candidates = candidate_registry()
    return {
        "status": W_SOURCE_CANDIDATE_REGISTRY_STATUS,
        "version": SOURCE_CANDIDATE_REGISTRY_VERSION,
        "mode": SOURCE_CANDIDATE_REGISTRY_MODE,
        "upstream_template_status": W_PAYLOAD_TEMPLATE_PACK_STATUS,
        "upstream_template_mode": PAYLOAD_TEMPLATE_PACK_MODE,
        "upstream_cli_status": W_PAYLOAD_IMPORT_CLI_STATUS,
        "external_adapter_version": EXTERNAL_ADAPTER_VERSION,
        "required_candidate_metadata_fields": REQUIRED_CANDIDATE_METADATA_FIELDS,
        "allowed_source_candidate_classes": ALLOWED_SOURCE_CANDIDATE_CLASSES,
        "required_acquisition_evidence_fields": REQUIRED_ACQUISITION_EVIDENCE_FIELDS,
        "required_preimport_steps": REQUIRED_PREIMPORT_STEPS,
        "forbidden_acquisition_inputs": FORBIDDEN_ACQUISITION_INPUTS,
        "component_order": FINITE_PART_COMPONENT_ORDER,
        "candidate_count": len(candidates),
        "candidate_registry": tuple(asdict(c) for c in candidates),
        "complete_for_import_count": sum(candidate_complete_for_import(c) for c in candidates),
        "real_external_source_acquired": REAL_EXTERNAL_SOURCE_ACQUIRED,
        "real_external_rows_imported": REAL_EXTERNAL_ROWS_IMPORTED,
        "real_external_rows_admitted": REAL_EXTERNAL_ROWS_ADMITTED,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "covariance_certified": COVARIANCE_CERTIFIED,
        "uncertainty_propagation_certified": UNCERTAINTY_PROPAGATION_CERTIFIED,
        "physical_W_export_enabled": PHYSICAL_W_EXPORT_ENABLED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "template_report_locked": not tmpl["physical_W_export_enabled"] and not tmpl["exports_physical_M_W"],
        "readiness_locked": not ready["physical_W_export_ready"] and not ready["physical_W_export_enabled"],
        "registry_doc_path": str(REGISTRY_DOC_PATH),
    }


def _promoted_candidate() -> SourceCandidateEntry:
    return replace(
        candidate_registry()[0],
        public_or_archival_locator="doi_or_archive_locator_pending_real_value",
        version_or_revision_id="reviewed_revision_identifier_pending_real_value",
        license_or_access_note="access reviewed; redistribution constraints recorded",
        extraction_log_digest="sha256:" + "a" * 64,
        pack_digest_plan="sha256:" + "b" * 64,
        review_attestation_plan="REVIEWED_INDEPENDENT_SOURCE_READY_FOR_IMPORT",
        forbidden_input_audit_plan="PASSED_NO_FORBIDDEN_INPUTS",
        scheme_and_gauge_policy_note="on-shell-compatible scheme/gauge policy recorded",
        counterterm_convention_note="Delta_r_ct_OS convention mapped to v10.7 certificate",
        acquired=True,
        imported=False,
        admitted=False,
    )


def _forbidden_candidate() -> SourceCandidateEntry:
    return replace(
        _promoted_candidate(),
        consumes_forbidden_input=True,
        forbidden_input_audit_plan="FAILED_USED_OBSERVED_W_OR_APF_TARGET",
    )


def _template_candidate() -> SourceCandidateEntry:
    return replace(
        _promoted_candidate(),
        source_candidate_id="template_shape_candidate_not_real_source",
        synthetic_or_template_only=True,
    )


def check_T_w_source_candidate_registry_status_declared():
    r = source_candidate_registry_report(); ok = r["status"] == W_SOURCE_CANDIDATE_REGISTRY_STATUS and not r["physical_W_export_enabled"]
    return _res("status_declared", ok, report=r)


def check_T_w_source_candidate_registry_depends_on_v114_template_pack():
    d = _check_v114(); return _res("depends_on_v114_template_pack", _passed(d), upstream=d.get("status"))


def check_T_w_source_candidate_registry_allowed_classes_declared():
    ok = len(ALLOWED_SOURCE_CANDIDATE_CLASSES) == 4 and all(isinstance(x, str) and x for x in ALLOWED_SOURCE_CANDIDATE_CLASSES)
    return _res("allowed_classes_declared", ok, classes=ALLOWED_SOURCE_CANDIDATE_CLASSES)


def check_T_w_source_candidate_registry_required_evidence_complete():
    needed = {"source_candidate_id", "source_candidate_class", "public_or_archival_locator", "extraction_log_digest", "pack_digest_plan", "forbidden_input_audit_plan"}
    ok = needed.issubset(set(REQUIRED_ACQUISITION_EVIDENCE_FIELDS))
    return _res("required_evidence_complete", ok, required=REQUIRED_ACQUISITION_EVIDENCE_FIELDS)


def check_T_w_source_candidate_registry_preimport_steps_ordered():
    steps = REQUIRED_PREIMPORT_STEPS
    ok = steps.index("confirm_independent_of_observed_W_mass") < steps.index("run_v11_3_payload_import_cli") < steps.index("keep_export_lock_closed_until_final_readiness_passes")
    return _res("preimport_steps_ordered", ok, steps=steps)


def check_T_w_source_candidate_registry_forbidden_inputs_declared():
    ok = {"observed_M_W", "APF_ANCHOR_DELTA_R_TARGET", "component_sum_residual_to_apf_target"}.issubset(set(FORBIDDEN_ACQUISITION_INPUTS))
    return _res("forbidden_inputs_declared", ok, forbidden=FORBIDDEN_ACQUISITION_INPUTS)


def check_T_w_source_candidate_registry_has_candidates():
    c = candidate_registry(); ok = len(c) == len(ALLOWED_SOURCE_CANDIDATE_CLASSES)
    return _res("has_candidates", ok, count=len(c))


def check_T_w_source_candidate_registry_candidate_classes_allowed():
    bad = tuple(c.source_candidate_class for c in candidate_registry() if c.source_candidate_class not in ALLOWED_SOURCE_CANDIDATE_CLASSES)
    return _res("candidate_classes_allowed", not bad, bad=bad)


def check_T_w_source_candidate_registry_candidates_cover_all_components():
    bad = tuple(c.source_candidate_id for c in candidate_registry() if tuple(c.intended_component_coverage) != FINITE_PART_COMPONENT_ORDER)
    return _res("candidates_cover_components", not bad, bad=bad)


def check_T_w_source_candidate_registry_candidates_not_acquired_by_default():
    ok = all(not c.acquired and not c.imported and not c.admitted for c in candidate_registry())
    return _res("candidates_not_acquired_default", ok)


def check_T_w_source_candidate_registry_no_default_complete_imports():
    r = source_candidate_registry_report(); ok = r["complete_for_import_count"] == 0 and not r["real_external_rows_imported"]
    return _res("no_default_complete_imports", ok, report=r)


def check_T_w_source_candidate_registry_candidate_completion_predicate_accepts_promoted_independent_source():
    c = _promoted_candidate(); return _res("completion_accepts_promoted", candidate_complete_for_import(c), candidate=asdict(c))


def check_T_w_source_candidate_registry_completion_rejects_unacquired_default():
    ok = all(not candidate_complete_for_import(c) for c in candidate_registry())
    return _res("completion_rejects_unacquired", ok)


def check_T_w_source_candidate_registry_completion_rejects_forbidden_input():
    c = _forbidden_candidate(); return _res("completion_rejects_forbidden", not candidate_complete_for_import(c), candidate=asdict(c))


def check_T_w_source_candidate_registry_completion_rejects_template_shape_source():
    c = _template_candidate(); return _res("completion_rejects_template", not candidate_complete_for_import(c), candidate=asdict(c))


def check_T_w_source_candidate_registry_completion_rejects_missing_digest():
    c = replace(_promoted_candidate(), extraction_log_digest="UNCOMPUTED")
    return _res("completion_rejects_missing_digest", not candidate_complete_for_import(c), candidate=asdict(c))


def check_T_w_source_candidate_registry_completion_rejects_wrong_review_status():
    c = replace(_promoted_candidate(), review_attestation_plan="PENDING")
    return _res("completion_rejects_wrong_review", not candidate_complete_for_import(c), candidate=asdict(c))


def check_T_w_source_candidate_registry_completion_rejects_partial_coverage():
    c = replace(_promoted_candidate(), intended_component_coverage=FINITE_PART_COMPONENT_ORDER[:-1])
    return _res("completion_rejects_partial_coverage", not candidate_complete_for_import(c), candidate=asdict(c))


def check_T_w_source_candidate_registry_report_exposes_adapter_fields():
    r = source_candidate_registry_report(); ok = tuple(r["required_candidate_metadata_fields"]) == REQUIRED_CANDIDATE_METADATA_FIELDS and r["external_adapter_version"] == EXTERNAL_ADAPTER_VERSION
    return _res("report_exposes_adapter_fields", ok, report=r)


def check_T_w_source_candidate_registry_template_pack_locked():
    r = source_candidate_registry_report(); ok = r["template_report_locked"] and r["upstream_template_status"] == W_PAYLOAD_TEMPLATE_PACK_STATUS
    return _res("template_pack_locked", ok, report=r)


def check_T_w_source_candidate_registry_readiness_locked():
    r = source_candidate_registry_report(); ok = r["readiness_locked"] and not r["physical_W_export_enabled"] and not r["exports_physical_M_W"]
    return _res("readiness_locked", ok, report=r)


def check_T_w_source_candidate_registry_no_component_sum_certified():
    r = source_candidate_registry_report(); ok = not r["component_sum_certified"] and not r["covariance_certified"] and not r["uncertainty_propagation_certified"]
    return _res("no_component_sum_certified", ok, report=r)


def check_T_w_source_candidate_registry_no_physical_export():
    r = source_candidate_registry_report(); ok = not r["physical_W_export_enabled"] and not r["exports_physical_M_W"]
    return _res("no_physical_export", ok, report=r)


def check_T_w_source_candidate_registry_doc_exists():
    return _res("doc_exists", REGISTRY_DOC_PATH.exists(), path=str(REGISTRY_DOC_PATH))


def check_T_w_source_candidate_registry_doc_warns_no_real_rows():
    text = REGISTRY_DOC_PATH.read_text(encoding="utf-8") if REGISTRY_DOC_PATH.exists() else ""
    needed = ("No real finite-part rows are admitted", "observed M_W", "APF-anchor", "physical W export remains locked")
    ok = all(s in text for s in needed)
    return _res("doc_warns_no_real_rows", ok, needed=needed)


def check_T_w_source_candidate_registry_source_classes_unique():
    classes = tuple(c.source_candidate_class for c in candidate_registry())
    ok = len(classes) == len(set(classes))
    return _res("source_classes_unique", ok, classes=classes)


def check_T_w_source_candidate_registry_candidate_ids_unique():
    ids = tuple(c.source_candidate_id for c in candidate_registry())
    ok = len(ids) == len(set(ids))
    return _res("candidate_ids_unique", ok, ids=ids)


def check_T_w_source_candidate_registry_bank_closure():
    rows = [fn() for name, fn in CHECKS.items() if name != "T_w_source_candidate_registry_bank_closure"]
    r = source_candidate_registry_report()
    ok = all(_passed(x) for x in rows) and not r["physical_W_export_enabled"] and r["complete_for_import_count"] == 0
    return _res("bank_closure", ok, passed_count=sum(_passed(x) for x in rows), total=len(rows), report=r)


CHECKS: Dict[str, Any] = {
    "T_w_source_candidate_registry_status_declared": check_T_w_source_candidate_registry_status_declared,
    "T_w_source_candidate_registry_depends_on_v114_template_pack": check_T_w_source_candidate_registry_depends_on_v114_template_pack,
    "T_w_source_candidate_registry_allowed_classes_declared": check_T_w_source_candidate_registry_allowed_classes_declared,
    "T_w_source_candidate_registry_required_evidence_complete": check_T_w_source_candidate_registry_required_evidence_complete,
    "T_w_source_candidate_registry_preimport_steps_ordered": check_T_w_source_candidate_registry_preimport_steps_ordered,
    "T_w_source_candidate_registry_forbidden_inputs_declared": check_T_w_source_candidate_registry_forbidden_inputs_declared,
    "T_w_source_candidate_registry_has_candidates": check_T_w_source_candidate_registry_has_candidates,
    "T_w_source_candidate_registry_candidate_classes_allowed": check_T_w_source_candidate_registry_candidate_classes_allowed,
    "T_w_source_candidate_registry_candidates_cover_all_components": check_T_w_source_candidate_registry_candidates_cover_all_components,
    "T_w_source_candidate_registry_candidates_not_acquired_by_default": check_T_w_source_candidate_registry_candidates_not_acquired_by_default,
    "T_w_source_candidate_registry_no_default_complete_imports": check_T_w_source_candidate_registry_no_default_complete_imports,
    "T_w_source_candidate_registry_candidate_completion_predicate_accepts_promoted_independent_source": check_T_w_source_candidate_registry_candidate_completion_predicate_accepts_promoted_independent_source,
    "T_w_source_candidate_registry_completion_rejects_unacquired_default": check_T_w_source_candidate_registry_completion_rejects_unacquired_default,
    "T_w_source_candidate_registry_completion_rejects_forbidden_input": check_T_w_source_candidate_registry_completion_rejects_forbidden_input,
    "T_w_source_candidate_registry_completion_rejects_template_shape_source": check_T_w_source_candidate_registry_completion_rejects_template_shape_source,
    "T_w_source_candidate_registry_completion_rejects_missing_digest": check_T_w_source_candidate_registry_completion_rejects_missing_digest,
    "T_w_source_candidate_registry_completion_rejects_wrong_review_status": check_T_w_source_candidate_registry_completion_rejects_wrong_review_status,
    "T_w_source_candidate_registry_completion_rejects_partial_coverage": check_T_w_source_candidate_registry_completion_rejects_partial_coverage,
    "T_w_source_candidate_registry_report_exposes_adapter_fields": check_T_w_source_candidate_registry_report_exposes_adapter_fields,
    "T_w_source_candidate_registry_template_pack_locked": check_T_w_source_candidate_registry_template_pack_locked,
    "T_w_source_candidate_registry_readiness_locked": check_T_w_source_candidate_registry_readiness_locked,
    "T_w_source_candidate_registry_no_component_sum_certified": check_T_w_source_candidate_registry_no_component_sum_certified,
    "T_w_source_candidate_registry_no_physical_export": check_T_w_source_candidate_registry_no_physical_export,
    "T_w_source_candidate_registry_doc_exists": check_T_w_source_candidate_registry_doc_exists,
    "T_w_source_candidate_registry_doc_warns_no_real_rows": check_T_w_source_candidate_registry_doc_warns_no_real_rows,
    "T_w_source_candidate_registry_source_classes_unique": check_T_w_source_candidate_registry_source_classes_unique,
    "T_w_source_candidate_registry_candidate_ids_unique": check_T_w_source_candidate_registry_candidate_ids_unique,
    "T_w_source_candidate_registry_bank_closure": check_T_w_source_candidate_registry_bank_closure,
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
        "status": "W_TRACE_SOURCE_CANDIDATE_REGISTRY_BANK_PASS" if ok else "W_TRACE_SOURCE_CANDIDATE_REGISTRY_BANK_FAIL",
        "checks": rows,
        "manifest": source_candidate_registry_report(),
    }
