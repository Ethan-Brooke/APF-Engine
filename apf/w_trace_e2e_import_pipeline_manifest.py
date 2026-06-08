"""W_TRACE end-to-end reviewed import pipeline manifest bank.

v12.1 (2026-05-09 LATER-56): roll-up manifest above the reviewed
source-packet, handoff, import-session log, replay, row-admission,
component-sum, covariance/uncertainty, and export-readiness gates. This
module does not ship, admit, or certify real finite-part rows and does not
unlock physical W export. It banks the ordered end-to-end pipeline contract
and proves that every real-payload route remains fail-closed until the prior
review/replay/admission/certification predicates are true together.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, replace
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple
import json

from apf.w_trace_review_packet_validator import (
    W_REVIEW_PACKET_VALIDATOR_STATUS,
    REVIEW_PACKET_VALIDATOR_VERSION,
    check_T_w_review_packet_validator_bank_closure as _check_v117,
)
from apf.w_trace_reviewed_source_import_handoff import (
    W_REVIEWED_SOURCE_IMPORT_HANDOFF_STATUS,
    REVIEWED_SOURCE_IMPORT_HANDOFF_VERSION,
    check_T_w_reviewed_source_import_handoff_bank_closure as _check_v118,
)
from apf.w_trace_import_session_log import (
    W_IMPORT_SESSION_LOG_STATUS,
    IMPORT_SESSION_LOG_VERSION,
    check_T_w_import_session_log_bank_closure as _check_v119,
)
from apf.w_trace_import_session_replay import (
    W_IMPORT_SESSION_REPLAY_STATUS,
    IMPORT_SESSION_REPLAY_VERSION,
    check_T_w_import_session_replay_bank_closure as _check_v120,
)
from apf.w_trace_payload_import_cli import (
    W_PAYLOAD_IMPORT_CLI_STATUS,
    PAYLOAD_IMPORT_CLI_VERSION,
    check_T_w_payload_import_cli_bank_closure as _check_v113,
)
from apf.w_trace_real_row_bundle_admission import (
    W_REAL_ROW_BUNDLE_STATUS,
    BUNDLE_ADMISSION_VERSION,
    check_T_w_real_row_bundle_bank_closure as _check_v109,
)
from apf.w_trace_row_bundle_to_component_sum import (
    W_ROW_BUNDLE_TO_COMPONENT_SUM_STATUS,
    ROW_BUNDLE_TO_COMPONENT_SUM_VERSION,
    check_T_w_row_bundle_sum_bridge_bank_closure as _check_v110,
)
from apf.w_trace_admitted_row_covariance_bridge import (
    W_ADMITTED_ROW_COVARIANCE_BRIDGE_STATUS,
    ADMITTED_ROW_COVARIANCE_BRIDGE_VERSION,
    check_T_w_admitted_row_covariance_bridge_bank_closure as _check_v111,
)
from apf.w_trace_component_sum_certificate import (
    W_COMPONENT_SUM_CERTIFICATE_STATUS,
    COMPONENT_SUM_CERTIFICATE_VERSION,
    check_T_w_component_sum_certificate_bank_closure as _check_v104,
)
from apf.w_trace_uncertainty_propagation import (
    W_UNCERTAINTY_PROPAGATION_STATUS,
    UNCERTAINTY_PROPAGATION_VERSION,
    check_T_w_uncertainty_propagation_bank_closure as _check_v105,
)
from apf.w_trace_physical_export_lock import (
    W_PHYSICAL_EXPORT_LOCK_STATUS,
    PHYSICAL_EXPORT_LOCK_VERSION,
    check_T_w_physical_export_lock_bank_closure as _check_v106,
)
from apf.w_trace_final_export_readiness import (
    W_FINAL_EXPORT_READINESS_STATUS,
    FINAL_EXPORT_READINESS_VERSION,
    readiness_report,
    check_T_w_final_export_readiness_bank_closure as _check_v112,
)

W_E2E_IMPORT_PIPELINE_MANIFEST_STATUS = "P_w_e2e_import_pipeline_manifest"
E2E_IMPORT_PIPELINE_MANIFEST_VERSION = "w_trace_e2e_import_pipeline_manifest_v1"
E2E_IMPORT_PIPELINE_MODE = "END_TO_END_REVIEWED_IMPORT_PIPELINE_MANIFEST__NO_REAL_PAYLOAD_SHIPPED"

REAL_COMPLETED_REVIEW_PACKET_SHIPPED = False
REAL_COMPLETED_REVIEW_PACKET_VALIDATED = False
REAL_REVIEWED_SOURCE_HANDOFF_COMPLETED = False
REAL_IMPORT_SESSION_REPLAY_VALIDATED = False
REAL_EXTERNAL_ROWS_IMPORTED = False
REAL_EXTERNAL_ROWS_ADMITTED = False
ROW_BUNDLE_COMPONENT_SUM_BRIDGED = False
ROW_BUNDLE_COVARIANCE_BRIDGED = False
NUMERICAL_COMPONENT_SUM_CERTIFIED = False
COVARIANCE_CERTIFIED = False
UNCERTAINTY_PROPAGATION_CERTIFIED = False
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_DOC_PATH = ROOT / "W_TRACE_E2E_IMPORT_PIPELINE_MANIFEST_BANK_v1_0.md"
MANIFEST_EXAMPLE_DIR = ROOT / "examples" / "w_trace_e2e_import_pipeline_manifest"
MANIFEST_TEMPLATE_PATH = MANIFEST_EXAMPLE_DIR / "e2e_import_pipeline_manifest_template.json"

PIPELINE_STAGE_ORDER: Tuple[str, ...] = (
    "review_packet_preflight",
    "reviewed_source_handoff",
    "payload_import_cli",
    "import_session_log",
    "import_session_replay",
    "real_row_bundle_admission",
    "row_bundle_to_component_sum_bridge",
    "admitted_row_covariance_bridge",
    "component_sum_certificate",
    "uncertainty_propagation",
    "physical_export_lock",
    "final_export_readiness",
)

STAGE_STATUS_VERSION: Dict[str, Tuple[str, str]] = {
    "review_packet_preflight": (W_REVIEW_PACKET_VALIDATOR_STATUS, REVIEW_PACKET_VALIDATOR_VERSION),
    "reviewed_source_handoff": (W_REVIEWED_SOURCE_IMPORT_HANDOFF_STATUS, REVIEWED_SOURCE_IMPORT_HANDOFF_VERSION),
    "payload_import_cli": (W_PAYLOAD_IMPORT_CLI_STATUS, PAYLOAD_IMPORT_CLI_VERSION),
    "import_session_log": (W_IMPORT_SESSION_LOG_STATUS, IMPORT_SESSION_LOG_VERSION),
    "import_session_replay": (W_IMPORT_SESSION_REPLAY_STATUS, IMPORT_SESSION_REPLAY_VERSION),
    "real_row_bundle_admission": (W_REAL_ROW_BUNDLE_STATUS, BUNDLE_ADMISSION_VERSION),
    "row_bundle_to_component_sum_bridge": (W_ROW_BUNDLE_TO_COMPONENT_SUM_STATUS, ROW_BUNDLE_TO_COMPONENT_SUM_VERSION),
    "admitted_row_covariance_bridge": (W_ADMITTED_ROW_COVARIANCE_BRIDGE_STATUS, ADMITTED_ROW_COVARIANCE_BRIDGE_VERSION),
    "component_sum_certificate": (W_COMPONENT_SUM_CERTIFICATE_STATUS, COMPONENT_SUM_CERTIFICATE_VERSION),
    "uncertainty_propagation": (W_UNCERTAINTY_PROPAGATION_STATUS, UNCERTAINTY_PROPAGATION_VERSION),
    "physical_export_lock": (W_PHYSICAL_EXPORT_LOCK_STATUS, PHYSICAL_EXPORT_LOCK_VERSION),
    "final_export_readiness": (W_FINAL_EXPORT_READINESS_STATUS, FINAL_EXPORT_READINESS_VERSION),
}

PIPELINE_EDGES: Tuple[Tuple[str, str], ...] = tuple(zip(PIPELINE_STAGE_ORDER, PIPELINE_STAGE_ORDER[1:]))

REQUIRED_MANIFEST_FIELDS: Tuple[str, ...] = (
    "pipeline_manifest_status",
    "pipeline_manifest_version",
    "pipeline_mode",
    "stage_order",
    "stage_statuses",
    "stage_versions",
    "pipeline_edges",
    "review_packet_validated",
    "reviewed_source_handoff_completed",
    "payload_import_cli_reachable",
    "import_session_logged",
    "import_session_replay_validated",
    "real_external_rows_imported",
    "real_external_rows_admitted",
    "row_bundle_component_sum_bridged",
    "row_bundle_covariance_bridged",
    "numerical_component_sum_certified",
    "covariance_certified",
    "uncertainty_propagation_certified",
    "physical_W_export_enabled",
    "exports_physical_M_W",
    "pipeline_ready_for_real_payload",
    "pipeline_ready_for_physical_export",
    "failure_reasons",
    "readiness_locked",
    "terminal_state",
)

FORBIDDEN_MANIFEST_TOKENS: Tuple[str, ...] = (
    "observed_M_W",
    "M_W_world_average",
    "W_mass_residual",
    "Delta_r_fit_to_observed_M_W",
    "APF_ANCHOR_DELTA_R_TARGET",
    "component_sum_residual_to_apf_target",
    "physical_export_request",
)

TERMINAL_STATES: Tuple[str, ...] = (
    "NO_REAL_PAYLOAD_PIPELINE_LOCKED",
    "REVIEWED_IMPORT_READY_BUT_NO_ROWS",
    "ROWS_ADMITTED_AWAITING_CERTIFICATES",
    "EXPORT_READY",
    "BLOCKED_FORBIDDEN_TOKEN",
)

@dataclass(frozen=True)
class E2EImportPipelineManifestRequest:
    review_packet_validated: bool = False
    reviewed_source_handoff_completed: bool = False
    payload_import_cli_reachable: bool = True
    import_session_logged: bool = False
    import_session_replay_validated: bool = False
    real_external_rows_imported: bool = False
    real_external_rows_admitted: bool = False
    row_bundle_component_sum_bridged: bool = False
    row_bundle_covariance_bridged: bool = False
    numerical_component_sum_certified: bool = False
    covariance_certified: bool = False
    uncertainty_propagation_certified: bool = False
    physical_W_export_enabled: bool = False
    exports_physical_M_W: bool = False
    notes: str = ""


def default_e2e_import_pipeline_manifest_request() -> E2EImportPipelineManifestRequest:
    return E2EImportPipelineManifestRequest()


def reviewed_no_rows_manifest_request() -> E2EImportPipelineManifestRequest:
    return E2EImportPipelineManifestRequest(
        review_packet_validated=True,
        reviewed_source_handoff_completed=True,
        payload_import_cli_reachable=True,
        import_session_logged=True,
        import_session_replay_validated=True,
    )


def _stage_statuses() -> Dict[str, str]:
    return {stage: STAGE_STATUS_VERSION[stage][0] for stage in PIPELINE_STAGE_ORDER}


def _stage_versions() -> Dict[str, str]:
    return {stage: STAGE_STATUS_VERSION[stage][1] for stage in PIPELINE_STAGE_ORDER}


def _contains_forbidden_token(text: str) -> bool:
    low = (text or "").lower()
    return any(tok.lower() in low for tok in FORBIDDEN_MANIFEST_TOKENS)


def e2e_import_pipeline_manifest_report(req: E2EImportPipelineManifestRequest | None = None) -> Dict[str, Any]:
    req = req or default_e2e_import_pipeline_manifest_request()
    d = asdict(req)
    failure_reasons = []
    if _contains_forbidden_token(req.notes):
        failure_reasons.append("FORBIDDEN_MANIFEST_TOKEN_PRESENT")
    if d["reviewed_source_handoff_completed"] and not d["review_packet_validated"]:
        failure_reasons.append("HANDOFF_WITHOUT_VALIDATED_REVIEW_PACKET")
    if d["import_session_logged"] and not d["reviewed_source_handoff_completed"]:
        failure_reasons.append("IMPORT_LOG_WITHOUT_REVIEWED_HANDOFF")
    if d["import_session_replay_validated"] and not d["import_session_logged"]:
        failure_reasons.append("REPLAY_WITHOUT_IMPORT_LOG")
    if d["real_external_rows_imported"] and not d["import_session_replay_validated"]:
        failure_reasons.append("ROWS_IMPORTED_WITHOUT_REPLAY_VALIDATION")
    if d["real_external_rows_admitted"] and not d["real_external_rows_imported"]:
        failure_reasons.append("ROWS_ADMITTED_WITHOUT_IMPORT")
    if d["row_bundle_component_sum_bridged"] and not d["real_external_rows_admitted"]:
        failure_reasons.append("SUM_BRIDGE_WITHOUT_ADMITTED_ROWS")
    if d["row_bundle_covariance_bridged"] and not d["real_external_rows_admitted"]:
        failure_reasons.append("COVARIANCE_BRIDGE_WITHOUT_ADMITTED_ROWS")
    if d["numerical_component_sum_certified"] and not d["row_bundle_component_sum_bridged"]:
        failure_reasons.append("COMPONENT_SUM_WITHOUT_BRIDGE")
    if d["covariance_certified"] and not d["row_bundle_covariance_bridged"]:
        failure_reasons.append("COVARIANCE_WITHOUT_BRIDGE")
    if d["uncertainty_propagation_certified"] and not (d["numerical_component_sum_certified"] and d["covariance_certified"]):
        failure_reasons.append("UNCERTAINTY_WITHOUT_SUM_AND_COVARIANCE")
    release_ready = all(d[k] for k in (
        "review_packet_validated",
        "reviewed_source_handoff_completed",
        "import_session_logged",
        "import_session_replay_validated",
        "real_external_rows_imported",
        "real_external_rows_admitted",
        "row_bundle_component_sum_bridged",
        "row_bundle_covariance_bridged",
        "numerical_component_sum_certified",
        "covariance_certified",
        "uncertainty_propagation_certified",
    ))
    if d["physical_W_export_enabled"] and not release_ready:
        failure_reasons.append("PHYSICAL_EXPORT_ENABLED_WITHOUT_ALL_RELEASE_PREDICATES")
    if d["exports_physical_M_W"] and not d["physical_W_export_enabled"]:
        failure_reasons.append("PHYSICAL_M_W_EXPORT_WITHOUT_EXPORT_ENABLE")
    if "FORBIDDEN_MANIFEST_TOKEN_PRESENT" in failure_reasons:
        terminal_state = "BLOCKED_FORBIDDEN_TOKEN"
    elif release_ready and d["physical_W_export_enabled"] and d["exports_physical_M_W"]:
        terminal_state = "EXPORT_READY"
    elif d["real_external_rows_admitted"]:
        terminal_state = "ROWS_ADMITTED_AWAITING_CERTIFICATES"
    elif d["review_packet_validated"] and d["import_session_replay_validated"]:
        terminal_state = "REVIEWED_IMPORT_READY_BUT_NO_ROWS"
    else:
        terminal_state = "NO_REAL_PAYLOAD_PIPELINE_LOCKED"
    readiness = readiness_report()
    report = {
        "pipeline_manifest_status": W_E2E_IMPORT_PIPELINE_MANIFEST_STATUS,
        "pipeline_manifest_version": E2E_IMPORT_PIPELINE_MANIFEST_VERSION,
        "pipeline_mode": E2E_IMPORT_PIPELINE_MODE,
        "stage_order": PIPELINE_STAGE_ORDER,
        "stage_statuses": _stage_statuses(),
        "stage_versions": _stage_versions(),
        "pipeline_edges": PIPELINE_EDGES,
        **d,
        "pipeline_ready_for_real_payload": d["review_packet_validated"] and d["reviewed_source_handoff_completed"] and d["import_session_replay_validated"] and not failure_reasons,
        "pipeline_ready_for_physical_export": release_ready and d["physical_W_export_enabled"] and d["exports_physical_M_W"] and not failure_reasons,
        "failure_reasons": tuple(dict.fromkeys(failure_reasons)),
        "readiness_locked": bool(readiness.get("readiness_locked", True)) and not d["physical_W_export_enabled"],
        "terminal_state": terminal_state,
    }
    return report


def write_e2e_manifest_template(path: str | Path = MANIFEST_TEMPLATE_PATH) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = e2e_import_pipeline_manifest_report()
    data.update({
        "template_only": True,
        "not_real_finite_part_evidence": True,
        "do_not_promote_to_real_payload": True,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
    })
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return path


def _res(check: str, passed: bool, **kw: Any) -> Dict[str, Any]:
    return {"check": check, "passed": bool(passed), "epistemic": W_E2E_IMPORT_PIPELINE_MANIFEST_STATUS, **kw}


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed"))


def check_T_w_e2e_pipeline_manifest_status_declared():
    return _res("status_declared", W_E2E_IMPORT_PIPELINE_MANIFEST_STATUS == "P_w_e2e_import_pipeline_manifest")

def check_T_w_e2e_pipeline_manifest_depends_on_v117_to_v120():
    ok = (
        W_REVIEW_PACKET_VALIDATOR_STATUS == "P_w_review_packet_validator"
        and W_REVIEWED_SOURCE_IMPORT_HANDOFF_STATUS == "P_w_reviewed_source_import_handoff"
        and W_IMPORT_SESSION_LOG_STATUS == "P_w_import_session_log"
        and W_IMPORT_SESSION_REPLAY_STATUS == "P_w_import_session_replay_validator"
    )
    return _res("depends_on_v117_to_v120", ok, upstream=(W_REVIEW_PACKET_VALIDATOR_STATUS, W_REVIEWED_SOURCE_IMPORT_HANDOFF_STATUS, W_IMPORT_SESSION_LOG_STATUS, W_IMPORT_SESSION_REPLAY_STATUS))

def check_T_w_e2e_pipeline_manifest_depends_on_export_stack():
    upstream = (W_REAL_ROW_BUNDLE_STATUS, W_ROW_BUNDLE_TO_COMPONENT_SUM_STATUS, W_ADMITTED_ROW_COVARIANCE_BRIDGE_STATUS, W_COMPONENT_SUM_CERTIFICATE_STATUS, W_UNCERTAINTY_PROPAGATION_STATUS, W_PHYSICAL_EXPORT_LOCK_STATUS, W_FINAL_EXPORT_READINESS_STATUS, W_PAYLOAD_IMPORT_CLI_STATUS)
    ok = all(s.startswith("P_w_") for s in upstream)
    return _res("depends_on_export_stack", ok, upstream=upstream)

def check_T_w_e2e_pipeline_manifest_stage_order_declared():
    ok = PIPELINE_STAGE_ORDER[0] == "review_packet_preflight" and PIPELINE_STAGE_ORDER[-1] == "final_export_readiness" and len(PIPELINE_STAGE_ORDER) == 12
    return _res("stage_order_declared", ok, stage_order=PIPELINE_STAGE_ORDER)

def check_T_w_e2e_pipeline_manifest_no_duplicate_stages():
    return _res("no_duplicate_stages", len(set(PIPELINE_STAGE_ORDER)) == len(PIPELINE_STAGE_ORDER))

def check_T_w_e2e_pipeline_manifest_edges_are_adjacent_and_acyclic():
    ok = len(PIPELINE_EDGES) == len(PIPELINE_STAGE_ORDER)-1 and all(a != b for a,b in PIPELINE_EDGES)
    return _res("edges_are_adjacent_and_acyclic", ok, edges=PIPELINE_EDGES)

def check_T_w_e2e_pipeline_manifest_status_versions_complete():
    ok = set(STAGE_STATUS_VERSION) == set(PIPELINE_STAGE_ORDER) and all(v[0].startswith("P_w_") for v in STAGE_STATUS_VERSION.values())
    return _res("status_versions_complete", ok, stages=STAGE_STATUS_VERSION)

def check_T_w_e2e_pipeline_manifest_required_fields_declared():
    r = e2e_import_pipeline_manifest_report()
    ok = all(k in r for k in REQUIRED_MANIFEST_FIELDS)
    return _res("required_fields_declared", ok, missing=[k for k in REQUIRED_MANIFEST_FIELDS if k not in r])

def check_T_w_e2e_pipeline_manifest_default_locked_state():
    r = e2e_import_pipeline_manifest_report()
    ok = r["terminal_state"] == "NO_REAL_PAYLOAD_PIPELINE_LOCKED" and not r["physical_W_export_enabled"] and not r["exports_physical_M_W"]
    return _res("default_locked_state", ok, report=r)

def check_T_w_e2e_pipeline_manifest_review_before_handoff():
    r = e2e_import_pipeline_manifest_report(E2EImportPipelineManifestRequest(reviewed_source_handoff_completed=True))
    ok = "HANDOFF_WITHOUT_VALIDATED_REVIEW_PACKET" in r["failure_reasons"]
    return _res("review_before_handoff", ok, report=r)

def check_T_w_e2e_pipeline_manifest_handoff_before_import_log():
    r = e2e_import_pipeline_manifest_report(E2EImportPipelineManifestRequest(import_session_logged=True))
    ok = "IMPORT_LOG_WITHOUT_REVIEWED_HANDOFF" in r["failure_reasons"]
    return _res("handoff_before_import_log", ok, report=r)

def check_T_w_e2e_pipeline_manifest_import_log_before_replay():
    r = e2e_import_pipeline_manifest_report(E2EImportPipelineManifestRequest(import_session_replay_validated=True))
    ok = "REPLAY_WITHOUT_IMPORT_LOG" in r["failure_reasons"]
    return _res("import_log_before_replay", ok, report=r)

def check_T_w_e2e_pipeline_manifest_replay_before_rows_imported():
    r = e2e_import_pipeline_manifest_report(E2EImportPipelineManifestRequest(real_external_rows_imported=True))
    ok = "ROWS_IMPORTED_WITHOUT_REPLAY_VALIDATION" in r["failure_reasons"]
    return _res("replay_before_rows_imported", ok, report=r)

def check_T_w_e2e_pipeline_manifest_import_before_rows_admitted():
    r = e2e_import_pipeline_manifest_report(E2EImportPipelineManifestRequest(real_external_rows_admitted=True))
    ok = "ROWS_ADMITTED_WITHOUT_IMPORT" in r["failure_reasons"]
    return _res("import_before_rows_admitted", ok, report=r)

def check_T_w_e2e_pipeline_manifest_sum_bridge_requires_admitted_rows():
    r = e2e_import_pipeline_manifest_report(E2EImportPipelineManifestRequest(row_bundle_component_sum_bridged=True))
    ok = "SUM_BRIDGE_WITHOUT_ADMITTED_ROWS" in r["failure_reasons"]
    return _res("sum_bridge_requires_admitted_rows", ok, report=r)

def check_T_w_e2e_pipeline_manifest_covariance_bridge_requires_admitted_rows():
    r = e2e_import_pipeline_manifest_report(E2EImportPipelineManifestRequest(row_bundle_covariance_bridged=True))
    ok = "COVARIANCE_BRIDGE_WITHOUT_ADMITTED_ROWS" in r["failure_reasons"]
    return _res("covariance_bridge_requires_admitted_rows", ok, report=r)

def check_T_w_e2e_pipeline_manifest_component_sum_requires_bridge():
    r = e2e_import_pipeline_manifest_report(E2EImportPipelineManifestRequest(numerical_component_sum_certified=True))
    ok = "COMPONENT_SUM_WITHOUT_BRIDGE" in r["failure_reasons"]
    return _res("component_sum_requires_bridge", ok, report=r)

def check_T_w_e2e_pipeline_manifest_covariance_requires_bridge():
    r = e2e_import_pipeline_manifest_report(E2EImportPipelineManifestRequest(covariance_certified=True))
    ok = "COVARIANCE_WITHOUT_BRIDGE" in r["failure_reasons"]
    return _res("covariance_requires_bridge", ok, report=r)

def check_T_w_e2e_pipeline_manifest_uncertainty_requires_sum_and_covariance():
    r = e2e_import_pipeline_manifest_report(E2EImportPipelineManifestRequest(uncertainty_propagation_certified=True))
    ok = "UNCERTAINTY_WITHOUT_SUM_AND_COVARIANCE" in r["failure_reasons"]
    return _res("uncertainty_requires_sum_and_covariance", ok, report=r)

def check_T_w_e2e_pipeline_manifest_export_requires_all_release_predicates():
    r = e2e_import_pipeline_manifest_report(E2EImportPipelineManifestRequest(physical_W_export_enabled=True))
    ok = "PHYSICAL_EXPORT_ENABLED_WITHOUT_ALL_RELEASE_PREDICATES" in r["failure_reasons"] and not r["pipeline_ready_for_physical_export"]
    return _res("export_requires_all_release_predicates", ok, report=r)

def check_T_w_e2e_pipeline_manifest_physical_mw_requires_export_enable():
    r = e2e_import_pipeline_manifest_report(E2EImportPipelineManifestRequest(exports_physical_M_W=True))
    ok = "PHYSICAL_M_W_EXPORT_WITHOUT_EXPORT_ENABLE" in r["failure_reasons"]
    return _res("physical_mw_requires_export_enable", ok, report=r)

def check_T_w_e2e_pipeline_manifest_reviewed_no_rows_is_not_export_ready():
    r = e2e_import_pipeline_manifest_report(reviewed_no_rows_manifest_request())
    ok = r["terminal_state"] == "REVIEWED_IMPORT_READY_BUT_NO_ROWS" and r["pipeline_ready_for_real_payload"] and not r["pipeline_ready_for_physical_export"]
    return _res("reviewed_no_rows_is_not_export_ready", ok, report=r)

def check_T_w_e2e_pipeline_manifest_forbidden_tokens_declared():
    ok = "observed_M_W" in FORBIDDEN_MANIFEST_TOKENS and "APF_ANCHOR_DELTA_R_TARGET" in FORBIDDEN_MANIFEST_TOKENS
    return _res("forbidden_tokens_declared", ok, tokens=FORBIDDEN_MANIFEST_TOKENS)

def check_T_w_e2e_pipeline_manifest_rejects_forbidden_tokens():
    r = e2e_import_pipeline_manifest_report(E2EImportPipelineManifestRequest(notes="contains observed_M_W"))
    ok = r["terminal_state"] == "BLOCKED_FORBIDDEN_TOKEN" and "FORBIDDEN_MANIFEST_TOKEN_PRESENT" in r["failure_reasons"]
    return _res("rejects_forbidden_tokens", ok, report=r)

def check_T_w_e2e_pipeline_manifest_failure_reasons_deduplicated():
    r = e2e_import_pipeline_manifest_report(E2EImportPipelineManifestRequest(real_external_rows_admitted=True, physical_W_export_enabled=True, exports_physical_M_W=True))
    ok = len(r["failure_reasons"]) == len(set(r["failure_reasons"]))
    return _res("failure_reasons_deduplicated", ok, reasons=r["failure_reasons"])

def check_T_w_e2e_pipeline_manifest_json_serializable():
    text = json.dumps(e2e_import_pipeline_manifest_report(), sort_keys=True, default=str)
    ok = W_E2E_IMPORT_PIPELINE_MANIFEST_STATUS in text and E2E_IMPORT_PIPELINE_MANIFEST_VERSION in text
    return _res("json_serializable", ok, length=len(text))

def check_T_w_e2e_pipeline_manifest_template_path_declared():
    ok = MANIFEST_TEMPLATE_PATH.name == "e2e_import_pipeline_manifest_template.json" and MANIFEST_EXAMPLE_DIR.name == "w_trace_e2e_import_pipeline_manifest"
    return _res("template_path_declared", ok, path=str(MANIFEST_TEMPLATE_PATH))

def check_T_w_e2e_pipeline_manifest_write_template():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = write_e2e_manifest_template(Path(td) / "template.json")
        data = json.loads(p.read_text())
    ok = data["template_only"] and data["not_real_finite_part_evidence"] and not data["exports_physical_M_W"]
    return _res("write_template", ok, data=data)

def check_T_w_e2e_pipeline_manifest_doc_exists():
    return _res("doc_exists", MANIFEST_DOC_PATH.exists(), path=str(MANIFEST_DOC_PATH))

def check_T_w_e2e_pipeline_manifest_doc_warns_locked():
    text = MANIFEST_DOC_PATH.read_text(encoding="utf-8") if MANIFEST_DOC_PATH.exists() else ""
    ok = "physical W/on-shell export remains OPEN" in text and "review packet" in text and "replay" in text
    return _res("doc_warns_locked", ok, found=len(text))

def check_T_w_e2e_pipeline_manifest_example_template_exists():
    return _res("example_template_exists", MANIFEST_TEMPLATE_PATH.exists(), path=str(MANIFEST_TEMPLATE_PATH))

def check_T_w_e2e_pipeline_manifest_template_not_real():
    data = json.loads(MANIFEST_TEMPLATE_PATH.read_text(encoding="utf-8")) if MANIFEST_TEMPLATE_PATH.exists() else {}
    ok = data.get("template_only") is True and data.get("not_real_finite_part_evidence") is True and data.get("exports_physical_M_W") is False
    return _res("template_not_real", ok, data=data)


def check_T_w_e2e_pipeline_manifest_terminal_states_declared():
    ok = set(TERMINAL_STATES) == {"NO_REAL_PAYLOAD_PIPELINE_LOCKED", "REVIEWED_IMPORT_READY_BUT_NO_ROWS", "ROWS_ADMITTED_AWAITING_CERTIFICATES", "EXPORT_READY", "BLOCKED_FORBIDDEN_TOKEN"}
    return _res("terminal_states_declared", ok, states=TERMINAL_STATES)

def check_T_w_e2e_pipeline_manifest_bank_closure():
    rows = [fn() for fn in CHECKS.values() if fn is not check_T_w_e2e_pipeline_manifest_bank_closure]
    ok = all(_passed(r) for r in rows) and len(rows) == 33
    return _res("bank_closure", ok, checked=len(rows), failed=[r.get("check") for r in rows if not _passed(r)])

CHECKS = {
    "T_w_e2e_pipeline_manifest_status_declared": check_T_w_e2e_pipeline_manifest_status_declared,
    "T_w_e2e_pipeline_manifest_depends_on_v117_to_v120": check_T_w_e2e_pipeline_manifest_depends_on_v117_to_v120,
    "T_w_e2e_pipeline_manifest_depends_on_export_stack": check_T_w_e2e_pipeline_manifest_depends_on_export_stack,
    "T_w_e2e_pipeline_manifest_stage_order_declared": check_T_w_e2e_pipeline_manifest_stage_order_declared,
    "T_w_e2e_pipeline_manifest_no_duplicate_stages": check_T_w_e2e_pipeline_manifest_no_duplicate_stages,
    "T_w_e2e_pipeline_manifest_edges_are_adjacent_and_acyclic": check_T_w_e2e_pipeline_manifest_edges_are_adjacent_and_acyclic,
    "T_w_e2e_pipeline_manifest_status_versions_complete": check_T_w_e2e_pipeline_manifest_status_versions_complete,
    "T_w_e2e_pipeline_manifest_required_fields_declared": check_T_w_e2e_pipeline_manifest_required_fields_declared,
    "T_w_e2e_pipeline_manifest_default_locked_state": check_T_w_e2e_pipeline_manifest_default_locked_state,
    "T_w_e2e_pipeline_manifest_review_before_handoff": check_T_w_e2e_pipeline_manifest_review_before_handoff,
    "T_w_e2e_pipeline_manifest_handoff_before_import_log": check_T_w_e2e_pipeline_manifest_handoff_before_import_log,
    "T_w_e2e_pipeline_manifest_import_log_before_replay": check_T_w_e2e_pipeline_manifest_import_log_before_replay,
    "T_w_e2e_pipeline_manifest_replay_before_rows_imported": check_T_w_e2e_pipeline_manifest_replay_before_rows_imported,
    "T_w_e2e_pipeline_manifest_import_before_rows_admitted": check_T_w_e2e_pipeline_manifest_import_before_rows_admitted,
    "T_w_e2e_pipeline_manifest_sum_bridge_requires_admitted_rows": check_T_w_e2e_pipeline_manifest_sum_bridge_requires_admitted_rows,
    "T_w_e2e_pipeline_manifest_covariance_bridge_requires_admitted_rows": check_T_w_e2e_pipeline_manifest_covariance_bridge_requires_admitted_rows,
    "T_w_e2e_pipeline_manifest_component_sum_requires_bridge": check_T_w_e2e_pipeline_manifest_component_sum_requires_bridge,
    "T_w_e2e_pipeline_manifest_covariance_requires_bridge": check_T_w_e2e_pipeline_manifest_covariance_requires_bridge,
    "T_w_e2e_pipeline_manifest_uncertainty_requires_sum_and_covariance": check_T_w_e2e_pipeline_manifest_uncertainty_requires_sum_and_covariance,
    "T_w_e2e_pipeline_manifest_export_requires_all_release_predicates": check_T_w_e2e_pipeline_manifest_export_requires_all_release_predicates,
    "T_w_e2e_pipeline_manifest_physical_mw_requires_export_enable": check_T_w_e2e_pipeline_manifest_physical_mw_requires_export_enable,
    "T_w_e2e_pipeline_manifest_reviewed_no_rows_is_not_export_ready": check_T_w_e2e_pipeline_manifest_reviewed_no_rows_is_not_export_ready,
    "T_w_e2e_pipeline_manifest_forbidden_tokens_declared": check_T_w_e2e_pipeline_manifest_forbidden_tokens_declared,
    "T_w_e2e_pipeline_manifest_rejects_forbidden_tokens": check_T_w_e2e_pipeline_manifest_rejects_forbidden_tokens,
    "T_w_e2e_pipeline_manifest_failure_reasons_deduplicated": check_T_w_e2e_pipeline_manifest_failure_reasons_deduplicated,
    "T_w_e2e_pipeline_manifest_json_serializable": check_T_w_e2e_pipeline_manifest_json_serializable,
    "T_w_e2e_pipeline_manifest_template_path_declared": check_T_w_e2e_pipeline_manifest_template_path_declared,
    "T_w_e2e_pipeline_manifest_write_template": check_T_w_e2e_pipeline_manifest_write_template,
    "T_w_e2e_pipeline_manifest_doc_exists": check_T_w_e2e_pipeline_manifest_doc_exists,
    "T_w_e2e_pipeline_manifest_doc_warns_locked": check_T_w_e2e_pipeline_manifest_doc_warns_locked,
    "T_w_e2e_pipeline_manifest_example_template_exists": check_T_w_e2e_pipeline_manifest_example_template_exists,
    "T_w_e2e_pipeline_manifest_template_not_real": check_T_w_e2e_pipeline_manifest_template_not_real,
    "T_w_e2e_pipeline_manifest_terminal_states_declared": check_T_w_e2e_pipeline_manifest_terminal_states_declared,
    "T_w_e2e_pipeline_manifest_bank_closure": check_T_w_e2e_pipeline_manifest_bank_closure,
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
        "status": "W_TRACE_E2E_IMPORT_PIPELINE_MANIFEST_BANK_PASS" if ok else "W_TRACE_E2E_IMPORT_PIPELINE_MANIFEST_BANK_FAIL",
        "checks": rows,
        "report": e2e_import_pipeline_manifest_report(),
    }
