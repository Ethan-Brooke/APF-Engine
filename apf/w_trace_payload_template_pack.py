"""W_TRACE payload template pack / CLI examples bank.

v11.4 (2026-05-09 LATER-49): shipped JSON/CSV example template layer
above the v11.3 payload import CLI.  This module ships copy-editable
fixture files that exercise the loader path without admitting real finite-part
payloads.  Templates are shape-only examples: they are not reviewed external
data, not finite-part evidence, and cannot unlock physical W/on-shell export.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple

from apf.w_trace_external_ingestion_dryrun import parse_external_payload
from apf.w_trace_finite_part_skeleton import FINITE_PART_COMPONENT_ORDER
from apf.w_trace_payload_import_cli import (
    W_PAYLOAD_IMPORT_CLI_STATUS,
    loader_report,
    infer_ingest_format,
    check_T_w_payload_import_cli_bank_closure as _check_v113,
)
from apf.w_trace_external_ingestion_dryrun import (
    check_T_w_external_ingestion_dryrun_bank_closure as _check_v101,
)
from apf.w_trace_final_export_readiness import readiness_report

W_PAYLOAD_TEMPLATE_PACK_STATUS = "P_w_payload_template_pack"
PAYLOAD_TEMPLATE_PACK_VERSION = "w_trace_payload_template_pack_v1"
PAYLOAD_TEMPLATE_PACK_MODE = "SHAPE_ONLY_TEMPLATE_EXAMPLES__NO_REAL_PAYLOAD__EXPORT_LOCKED"

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "examples" / "w_trace_payload_templates"
JSON_TEMPLATE_NAME = "w_trace_payload_template_shape.json"
CSV_TEMPLATE_NAME = "w_trace_payload_template_shape.csv"
README_NAME = "README.md"

REAL_TEMPLATE_PAYLOAD_SHIPPED = False
REAL_TEMPLATE_PAYLOAD_ADMITTED = False
COMPONENT_SUM_CERTIFIED = False
COVARIANCE_CERTIFIED = False
UNCERTAINTY_PROPAGATION_CERTIFIED = False
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False

REQUIRED_TEMPLATE_FILES: Tuple[str, ...] = (JSON_TEMPLATE_NAME, CSV_TEMPLATE_NAME, README_NAME)
REQUIRED_TEMPLATE_WARNINGS: Tuple[str, ...] = (
    "shape-only",
    "not reviewed external finite-part data",
    "must not be used to unlock physical W/on-shell export",
    "observed `M_W`",
    "APF-anchor `Delta r` target",
)


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def _res(name: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    return {
        "passed": bool(passed),
        "status": "PASS" if passed else "FAIL",
        "tier": 4,
        "epistemic": W_PAYLOAD_TEMPLATE_PACK_STATUS,
        "check": name,
        **extra,
    }


def template_path(name: str) -> Path:
    return TEMPLATE_DIR / name


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def template_paths() -> Dict[str, str]:
    return {name: str(template_path(name)) for name in REQUIRED_TEMPLATE_FILES}


def template_digests() -> Dict[str, str]:
    out: Dict[str, str] = {}
    for name in REQUIRED_TEMPLATE_FILES:
        p = template_path(name)
        out[name] = sha256_file(p) if p.exists() else "MISSING"
    return out


def parse_json_template():
    return parse_external_payload(template_path(JSON_TEMPLATE_NAME).read_text(encoding="utf-8"), "json_rows_v1")


def parse_csv_template():
    return parse_external_payload(template_path(CSV_TEMPLATE_NAME).read_text(encoding="utf-8"), "csv_with_header_v1")


def template_report() -> Dict[str, Any]:
    json_rows = parse_json_template() if template_path(JSON_TEMPLATE_NAME).exists() else ()
    csv_rows = parse_csv_template() if template_path(CSV_TEMPLATE_NAME).exists() else ()
    json_loader = loader_report(template_path(JSON_TEMPLATE_NAME), "json_rows_v1") if template_path(JSON_TEMPLATE_NAME).exists() else None
    csv_loader = loader_report(template_path(CSV_TEMPLATE_NAME), "csv_with_header_v1") if template_path(CSV_TEMPLATE_NAME).exists() else None
    ready = readiness_report(physical_export_requested=False)
    return {
        "status": W_PAYLOAD_TEMPLATE_PACK_STATUS,
        "version": PAYLOAD_TEMPLATE_PACK_VERSION,
        "mode": PAYLOAD_TEMPLATE_PACK_MODE,
        "template_dir": str(TEMPLATE_DIR),
        "required_template_files": REQUIRED_TEMPLATE_FILES,
        "template_paths": template_paths(),
        "template_digests": template_digests(),
        "json_rows_loaded": len(json_rows),
        "csv_rows_loaded": len(csv_rows),
        "component_order": FINITE_PART_COMPONENT_ORDER,
        "json_component_order": tuple(getattr(r, "component_id", None) for r in json_rows),
        "csv_component_order": tuple(getattr(r, "component_id", None) for r in csv_rows),
        "json_loader_report": json_loader,
        "csv_loader_report": csv_loader,
        "readiness_report": ready,
        "real_template_payload_shipped": REAL_TEMPLATE_PAYLOAD_SHIPPED,
        "real_template_payload_admitted": REAL_TEMPLATE_PAYLOAD_ADMITTED,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "covariance_certified": COVARIANCE_CERTIFIED,
        "uncertainty_propagation_certified": UNCERTAINTY_PROPAGATION_CERTIFIED,
        "physical_W_export_enabled": PHYSICAL_W_EXPORT_ENABLED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
    }


def check_T_w_payload_template_pack_status_declared():
    r = template_report(); ok = r["status"] == W_PAYLOAD_TEMPLATE_PACK_STATUS and not r["physical_W_export_enabled"]
    return _res("status_declared", ok, report=r)


def check_T_w_payload_template_pack_depends_on_v113_loader():
    d = _check_v113(); return _res("depends_on_v113_loader", _passed(d), upstream=d.get("status"))


def check_T_w_payload_template_pack_depends_on_v101_parser():
    d = _check_v101(); return _res("depends_on_v101_parser", _passed(d), upstream=d.get("status"))


def check_T_w_payload_template_pack_directory_exists():
    return _res("template_dir_exists", TEMPLATE_DIR.exists() and TEMPLATE_DIR.is_dir(), path=str(TEMPLATE_DIR))


def check_T_w_payload_template_pack_required_files_exist():
    missing = tuple(name for name in REQUIRED_TEMPLATE_FILES if not template_path(name).exists())
    return _res("required_files_exist", not missing, missing=missing, paths=template_paths())


def check_T_w_payload_template_pack_json_template_parses():
    rows = parse_json_template(); ok = len(rows) == len(FINITE_PART_COMPONENT_ORDER)
    return _res("json_template_parses", ok, count=len(rows))


def check_T_w_payload_template_pack_csv_template_parses():
    rows = parse_csv_template(); ok = len(rows) == len(FINITE_PART_COMPONENT_ORDER)
    return _res("csv_template_parses", ok, count=len(rows))


def check_T_w_payload_template_pack_json_loader_path_works():
    r = loader_report(template_path(JSON_TEMPLATE_NAME), "json_rows_v1")
    ok = r["file_exists"] and r["rows_loaded"] == len(FINITE_PART_COMPONENT_ORDER)
    return _res("json_loader_path", ok, loader=r)


def check_T_w_payload_template_pack_csv_loader_path_works():
    r = loader_report(template_path(CSV_TEMPLATE_NAME), "csv_with_header_v1")
    ok = r["file_exists"] and r["rows_loaded"] == len(FINITE_PART_COMPONENT_ORDER)
    return _res("csv_loader_path", ok, loader=r)


def check_T_w_payload_template_pack_format_inference_for_templates():
    ok = infer_ingest_format(template_path(JSON_TEMPLATE_NAME)) == "json_rows_v1" and infer_ingest_format(template_path(CSV_TEMPLATE_NAME)) == "csv_with_header_v1"
    return _res("format_inference", ok)


def check_T_w_payload_template_pack_component_order_preserved_json():
    order = tuple(r.component_id for r in parse_json_template())
    return _res("json_component_order", order == FINITE_PART_COMPONENT_ORDER, order=order)


def check_T_w_payload_template_pack_component_order_preserved_csv():
    order = tuple(r.component_id for r in parse_csv_template())
    return _res("csv_component_order", order == FINITE_PART_COMPONENT_ORDER, order=order)


def check_T_w_payload_template_pack_json_shape_not_real_payload():
    r = loader_report(template_path(JSON_TEMPLATE_NAME), "json_rows_v1", review_attested=False, shipped_real_data=False)
    ok = (not r["real_payload_file_admitted"] and "SHAPE_OR_UNATTESTED_FILE_NOT_PROMOTED_TO_REAL_PAYLOAD" in r["failure_reasons"])
    return _res("json_shape_not_real", ok, loader=r)


def check_T_w_payload_template_pack_csv_shape_not_real_payload():
    r = loader_report(template_path(CSV_TEMPLATE_NAME), "csv_with_header_v1", review_attested=False, shipped_real_data=False)
    ok = (not r["real_payload_file_admitted"] and "SHAPE_OR_UNATTESTED_FILE_NOT_PROMOTED_TO_REAL_PAYLOAD" in r["failure_reasons"])
    return _res("csv_shape_not_real", ok, loader=r)


def check_T_w_payload_template_pack_review_attestation_still_no_export():
    r = loader_report(template_path(JSON_TEMPLATE_NAME), "json_rows_v1", review_attested=True, shipped_real_data=True)
    ok = r["rows_loaded"] == len(FINITE_PART_COMPONENT_ORDER) and not r["physical_W_export_enabled"] and not r["exports_physical_M_W"]
    return _res("attestation_still_no_export", ok, loader=r)


def check_T_w_payload_template_pack_readiness_remains_locked():
    r = template_report()["readiness_report"]
    ok = not r["physical_W_export_ready"] and not r["physical_W_export_enabled"] and not r["exports_physical_M_W"]
    return _res("readiness_locked", ok, readiness=r)


def check_T_w_payload_template_pack_no_forbidden_consumption_json():
    rows = parse_json_template()
    ok = all(not r.apf_target_consumed and not tuple(r.target_observables_consumed) for r in rows)
    return _res("json_no_forbidden_consumption", ok)


def check_T_w_payload_template_pack_no_forbidden_consumption_csv():
    rows = parse_csv_template()
    ok = all(not r.apf_target_consumed and not tuple(r.target_observables_consumed) for r in rows)
    return _res("csv_no_forbidden_consumption", ok)


def check_T_w_payload_template_pack_digests_declared():
    d = template_digests(); ok = all(v.startswith("sha256:") for v in d.values())
    return _res("digests_declared", ok, digests=d)


def check_T_w_payload_template_pack_json_csv_digests_distinct():
    d = template_digests(); ok = d[JSON_TEMPLATE_NAME] != d[CSV_TEMPLATE_NAME] and d[README_NAME].startswith("sha256:")
    return _res("digests_distinct", ok, digests=d)


def check_T_w_payload_template_pack_readme_warns_shape_only():
    text = template_path(README_NAME).read_text(encoding="utf-8")
    ok = all(s in text for s in REQUIRED_TEMPLATE_WARNINGS)
    return _res("readme_warnings", ok, warnings=REQUIRED_TEMPLATE_WARNINGS)


def check_T_w_payload_template_pack_manifest_has_absence_logic():
    r = template_report(); ok = not r["real_template_payload_shipped"] and not r["real_template_payload_admitted"] and not r["component_sum_certified"]
    return _res("manifest_absence_logic", ok, report=r)


def check_T_w_payload_template_pack_physical_export_request_still_blocked():
    r = loader_report(template_path(JSON_TEMPLATE_NAME), "json_rows_v1", review_attested=True, shipped_real_data=True, physical_export_requested=True)
    ok = "PHYSICAL_W_EXPORT_REQUEST_BLOCKED_BY_IMPORT_LOADER" in r["failure_reasons"] and not r["physical_W_export_enabled"]
    return _res("physical_export_request_blocked", ok, loader=r)


def check_T_w_payload_template_pack_templates_do_not_certify_sum():
    r = template_report(); ok = not r["component_sum_certified"] and not r["covariance_certified"] and not r["uncertainty_propagation_certified"]
    return _res("templates_do_not_certify_sum", ok, report=r)


def check_T_w_payload_template_pack_templates_do_not_export_physical_mw():
    r = template_report(); ok = not r["physical_W_export_enabled"] and not r["exports_physical_M_W"]
    return _res("templates_do_not_export_mw", ok, report=r)


def check_T_w_payload_template_pack_bank_closure():
    rows = [fn() for name, fn in CHECKS.items() if name != "T_w_payload_template_pack_bank_closure"]
    ok = all(_passed(r) for r in rows) and not template_report()["physical_W_export_enabled"]
    return _res("bank_closure", ok, passed_count=sum(_passed(r) for r in rows), total=len(rows))


CHECKS: Dict[str, Any] = {
    "T_w_payload_template_pack_status_declared": check_T_w_payload_template_pack_status_declared,
    "T_w_payload_template_pack_depends_on_v113_loader": check_T_w_payload_template_pack_depends_on_v113_loader,
    "T_w_payload_template_pack_depends_on_v101_parser": check_T_w_payload_template_pack_depends_on_v101_parser,
    "T_w_payload_template_pack_directory_exists": check_T_w_payload_template_pack_directory_exists,
    "T_w_payload_template_pack_required_files_exist": check_T_w_payload_template_pack_required_files_exist,
    "T_w_payload_template_pack_json_template_parses": check_T_w_payload_template_pack_json_template_parses,
    "T_w_payload_template_pack_csv_template_parses": check_T_w_payload_template_pack_csv_template_parses,
    "T_w_payload_template_pack_json_loader_path_works": check_T_w_payload_template_pack_json_loader_path_works,
    "T_w_payload_template_pack_csv_loader_path_works": check_T_w_payload_template_pack_csv_loader_path_works,
    "T_w_payload_template_pack_format_inference_for_templates": check_T_w_payload_template_pack_format_inference_for_templates,
    "T_w_payload_template_pack_component_order_preserved_json": check_T_w_payload_template_pack_component_order_preserved_json,
    "T_w_payload_template_pack_component_order_preserved_csv": check_T_w_payload_template_pack_component_order_preserved_csv,
    "T_w_payload_template_pack_json_shape_not_real_payload": check_T_w_payload_template_pack_json_shape_not_real_payload,
    "T_w_payload_template_pack_csv_shape_not_real_payload": check_T_w_payload_template_pack_csv_shape_not_real_payload,
    "T_w_payload_template_pack_review_attestation_still_no_export": check_T_w_payload_template_pack_review_attestation_still_no_export,
    "T_w_payload_template_pack_readiness_remains_locked": check_T_w_payload_template_pack_readiness_remains_locked,
    "T_w_payload_template_pack_no_forbidden_consumption_json": check_T_w_payload_template_pack_no_forbidden_consumption_json,
    "T_w_payload_template_pack_no_forbidden_consumption_csv": check_T_w_payload_template_pack_no_forbidden_consumption_csv,
    "T_w_payload_template_pack_digests_declared": check_T_w_payload_template_pack_digests_declared,
    "T_w_payload_template_pack_json_csv_digests_distinct": check_T_w_payload_template_pack_json_csv_digests_distinct,
    "T_w_payload_template_pack_readme_warns_shape_only": check_T_w_payload_template_pack_readme_warns_shape_only,
    "T_w_payload_template_pack_manifest_has_absence_logic": check_T_w_payload_template_pack_manifest_has_absence_logic,
    "T_w_payload_template_pack_physical_export_request_still_blocked": check_T_w_payload_template_pack_physical_export_request_still_blocked,
    "T_w_payload_template_pack_templates_do_not_certify_sum": check_T_w_payload_template_pack_templates_do_not_certify_sum,
    "T_w_payload_template_pack_templates_do_not_export_physical_mw": check_T_w_payload_template_pack_templates_do_not_export_physical_mw,
    "T_w_payload_template_pack_bank_closure": check_T_w_payload_template_pack_bank_closure,
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
        "status": "W_TRACE_PAYLOAD_TEMPLATE_PACK_BANK_PASS" if ok else "W_TRACE_PAYLOAD_TEMPLATE_PACK_BANK_FAIL",
        "checks": rows,
        "manifest": template_report(),
    }
