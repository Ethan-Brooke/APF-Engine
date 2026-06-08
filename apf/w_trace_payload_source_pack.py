"""W_TRACE independent finite-part payload source pack v0.

v9.9 (2026-05-09 LATER-17): source-pack manifest after the v9.8
payload fixture.  This module banks the admissible source-pack container and
admission report for future independently sourced W finite-part payload rows.
It deliberately ships with an empty source pack: no numerical finite-part values
are supplied, no component-sum certificate is issued, and no physical W value is
exported.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, fields, replace
from typing import Any, Dict, Mapping, Sequence, Tuple

from apf.w_trace_payload_fixture import (
    W_PAYLOAD_FIXTURE_STATUS,
    PayloadFixtureRow,
    PAYLOAD_TABLE_VERSION,
    payload_admission_report,
    payload_fixture_rows,
    synthetic_independent_payload_table,
    check_T_w_payload_fixture_bank_closure as _check_v98,
)
from apf.w_trace_numeric_source_adapter import (
    ALLOWED_SOURCE_CLASSES,
    FORBIDDEN_NUMERIC_SOURCE_INPUTS,
    REQUIRED_SOURCE_FIELDS,
    admitted_numeric_payload,
)
from apf.w_trace_finite_part_skeleton import (
    COMPONENT_SYMBOLS,
    FINITE_PART_COMPONENT_ORDER,
)
from apf.trace_transport_completion import (
    check_T_physical_export_gate_locked_until_all_certificates_filled as _check_completion,
)

W_PAYLOAD_SOURCE_PACK_STATUS = "P_w_payload_source_pack"
SOURCE_PACK_DECLARED = True
SOURCE_PACK_VERSION = "w_trace_independent_payload_source_pack_v0"
SOURCE_PACK_MODE = "EMPTY_AUDITABLE_CONTAINER"
NUMERICAL_COMPONENT_VALUES_SUPPLIED = False
INDEPENDENT_SOURCE_PACK_ROWS_SUPPLIED = False
COMPONENT_SUM_CERTIFIED = False
COVARIANCE_PROTOCOL_SUPPLIED = False
UNCERTAINTY_PROTOCOL_SUPPLIED = False
PHYSICAL_W_TRANSPORT_CLOSED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

SOURCE_PACK_REQUIRED_FIELDS = REQUIRED_SOURCE_FIELDS + (
    "pack_id",
    "provenance_chain",
    "license_or_access_note",
    "review_status",
)

ALLOWED_PACK_REVIEW_STATUSES = (
    "EMPTY_PLACEHOLDER",
    "INDEPENDENT_SOURCE_PENDING_REVIEW",
    "INDEPENDENT_SOURCE_REVIEWED_NOT_SUMMED",
)

FORBIDDEN_SOURCE_PACK_INPUTS = tuple(sorted(set(FORBIDDEN_NUMERIC_SOURCE_INPUTS + (
    "apf_anchor_delta_r_target_as_pack_value",
    "component_pack_chosen_to_close_delta_r_residual",
    "posthoc_payload_pack_fit",
))))

@dataclass(frozen=True)
class SourcePackRow:
    component_id: str
    symbol: str
    pack_id: str = "W_TRACE_PAYLOAD_SOURCE_PACK_V0_EMPTY"
    source_class: str = "UNFILLED_ALLOWED_SOURCE_SLOT"
    source_name: str = "UNFILLED"
    version_or_citation: str = "UNFILLED"
    input_scheme: str = "UNFILLED"
    renormalization_scheme: str = "UNFILLED"
    gauge_convention: str = "UNFILLED"
    numeric_value: str = "UNSUPPLIED"
    uncertainty: str = "UNSUPPLIED"
    checksum_or_table_locator: str = "UNSUPPLIED"
    target_observables_consumed: Tuple[str, ...] = ()
    apf_target_consumed: bool = False
    provenance_chain: Tuple[str, ...] = ()
    license_or_access_note: str = "UNFILLED"
    status: str = "OPEN_WAITING_FOR_INDEPENDENT_NUMERICAL_SOURCE"
    fixture_note: str = "source-pack row; not an admitted finite-part value unless reviewed and independently sourced"
    review_status: str = "EMPTY_PLACEHOLDER"


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def source_pack_rows() -> Tuple[SourcePackRow, ...]:
    return tuple(SourcePackRow(cid, COMPONENT_SYMBOLS[cid]) for cid in FINITE_PART_COMPONENT_ORDER)


def _row_to_adapter_payload(row: SourcePackRow | Mapping[str, Any]) -> Dict[str, Any]:
    d = asdict(row) if isinstance(row, SourcePackRow) else dict(row)
    return {k: d.get(k) for k in REQUIRED_SOURCE_FIELDS}


def _source_pack_row_complete(row: SourcePackRow | Mapping[str, Any]) -> bool:
    d = asdict(row) if isinstance(row, SourcePackRow) else dict(row)
    if not all(k in d for k in SOURCE_PACK_REQUIRED_FIELDS):
        return False
    if d.get("review_status") not in ALLOWED_PACK_REVIEW_STATUSES:
        return False
    if d.get("review_status") != "INDEPENDENT_SOURCE_REVIEWED_NOT_SUMMED":
        return False
    if not d.get("provenance_chain"):
        return False
    if str(d.get("license_or_access_note")) in {"", "UNFILLED", "None"}:
        return False
    consumed = set(d.get("target_observables_consumed") or ())
    if consumed.intersection(FORBIDDEN_SOURCE_PACK_INPUTS):
        return False
    return admitted_numeric_payload(_row_to_adapter_payload(d))


def source_pack_admission_report(rows: Sequence[SourcePackRow | Mapping[str, Any]]) -> Dict[str, Any]:
    ids = tuple((r.component_id if isinstance(r, SourcePackRow) else r.get("component_id")) for r in rows)
    duplicate_ids = tuple(sorted({x for x in ids if ids.count(x) > 1 and x is not None}))
    missing_ids = tuple(x for x in FINITE_PART_COMPONENT_ORDER if x not in ids)
    unknown_ids = tuple(x for x in ids if x not in FINITE_PART_COMPONENT_ORDER)
    table_shape_ok = not duplicate_ids and not missing_ids and not unknown_ids and len(rows) == len(FINITE_PART_COMPONENT_ORDER)
    row_results = tuple(_source_pack_row_complete(r) for r in rows)
    fixture_report = payload_admission_report(tuple(_source_pack_to_fixture_row(r) for r in rows)) if table_shape_ok else None
    all_rows_admitted = table_shape_ok and all(row_results) and bool(fixture_report and fixture_report["all_rows_admitted"])
    return {
        "table_shape_ok": table_shape_ok,
        "all_rows_admitted": all_rows_admitted,
        "component_sum_certified": False,
        "physical_W_transport_closed": False,
        "duplicate_ids": duplicate_ids,
        "missing_ids": missing_ids,
        "unknown_ids": unknown_ids,
        "row_results": row_results,
        "admitted_count": sum(1 for x in row_results if x),
        "total_count": len(rows),
        "fixture_report_status": None if fixture_report is None else fixture_report.get("all_rows_admitted"),
    }


def _source_pack_to_fixture_row(row: SourcePackRow | Mapping[str, Any]) -> PayloadFixtureRow:
    d = asdict(row) if isinstance(row, SourcePackRow) else dict(row)
    kwargs = {f.name: d.get(f.name) for f in fields(PayloadFixtureRow) if f.name in d}
    return PayloadFixtureRow(**kwargs)


def source_pack_manifest() -> Dict[str, Any]:
    return {
        "status": W_PAYLOAD_SOURCE_PACK_STATUS,
        "upstream_status": W_PAYLOAD_FIXTURE_STATUS,
        "source_pack_version": SOURCE_PACK_VERSION,
        "source_pack_mode": SOURCE_PACK_MODE,
        "payload_table_version": PAYLOAD_TABLE_VERSION,
        "required_fields": SOURCE_PACK_REQUIRED_FIELDS,
        "allowed_source_classes": ALLOWED_SOURCE_CLASSES,
        "allowed_review_statuses": ALLOWED_PACK_REVIEW_STATUSES,
        "forbidden_inputs": FORBIDDEN_SOURCE_PACK_INPUTS,
        "component_order": FINITE_PART_COMPONENT_ORDER,
        "rows": tuple(asdict(r) for r in source_pack_rows()),
        "independent_source_pack_rows_supplied": INDEPENDENT_SOURCE_PACK_ROWS_SUPPLIED,
        "numerical_component_values_supplied": NUMERICAL_COMPONENT_VALUES_SUPPLIED,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
    }


def _reviewed_shape_row(component_id: str) -> SourcePackRow:
    return SourcePackRow(
        component_id=component_id,
        symbol=COMPONENT_SYMBOLS[component_id],
        pack_id="W_TRACE_TEST_SHAPE_PACK_NOT_DATA",
        source_class="audited_literature_table",
        source_name="future_independent_source_pack_shape_test",
        version_or_citation="UNFILLED_TEST_SHAPE_NOT_A_VALUE",
        input_scheme="alpha_G_F_MZ",
        renormalization_scheme="on_shell",
        gauge_convention="declared_test_gauge",
        numeric_value="1.0e-3",
        uncertainty="1.0e-6",
        checksum_or_table_locator="sha256:source-pack-shape-test-not-a-source",
        provenance_chain=("source_document", "component_extraction", "checksum"),
        license_or_access_note="shape-test placeholder; not a source payload",
        status="SHAPE_TEST_ONLY_NOT_ADMITTED_TO_BANK_AS_DATA",
        review_status="INDEPENDENT_SOURCE_REVIEWED_NOT_SUMMED",
    )


def reviewed_shape_source_pack() -> Tuple[SourcePackRow, ...]:
    return tuple(_reviewed_shape_row(cid) for cid in FINITE_PART_COMPONENT_ORDER)


def check_T_w_payload_source_pack_status_declared():
    p = W_PAYLOAD_SOURCE_PACK_STATUS == "P_w_payload_source_pack" and SOURCE_PACK_DECLARED
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_PAYLOAD_SOURCE_PACK_STATUS}


def check_T_w_payload_source_pack_depends_on_v98_fixture():
    d = _check_v98()
    p = _passed(d) and W_PAYLOAD_FIXTURE_STATUS == "P_w_payload_fixture"
    return {"passed": p, "status": "PASS" if p else "FAIL", "upstream": d.get("status")}


def check_T_w_payload_source_pack_schema_extends_fixture_and_adapter():
    have = {f.name for f in fields(SourcePackRow)}
    missing = [x for x in SOURCE_PACK_REQUIRED_FIELDS if x not in have]
    fixture = {f.name for f in fields(PayloadFixtureRow)}
    p = not missing and fixture.issubset(have) and set(REQUIRED_SOURCE_FIELDS).issubset(have)
    return {"passed": p, "status": "PASS" if p else "FAIL", "missing": missing}


def check_T_w_payload_source_pack_covers_all_components():
    ids = tuple(r.component_id for r in source_pack_rows())
    p = ids == FINITE_PART_COMPONENT_ORDER
    return {"passed": p, "status": "PASS" if p else "FAIL", "component_order": ids}


def check_T_w_payload_source_pack_symbols_match_skeleton():
    bad = [r.component_id for r in source_pack_rows() if r.symbol != COMPONENT_SYMBOLS[r.component_id]]
    return {"passed": not bad, "status": "PASS" if not bad else "FAIL", "bad": bad}


def check_T_w_payload_source_pack_empty_by_default():
    rows = source_pack_rows()
    p = all(r.numeric_value == "UNSUPPLIED" and r.review_status == "EMPTY_PLACEHOLDER" for r in rows)
    return {"passed": p, "status": "PASS" if p else "FAIL", "independent_source_pack_rows_supplied": INDEPENDENT_SOURCE_PACK_ROWS_SUPPLIED}


def check_T_w_payload_source_pack_empty_rows_rejected():
    report = source_pack_admission_report(source_pack_rows())
    p = report["table_shape_ok"] and not report["all_rows_admitted"] and report["admitted_count"] == 0
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_payload_source_pack_reviewed_shape_rows_admissible():
    report = source_pack_admission_report(reviewed_shape_source_pack())
    p = report["table_shape_ok"] and report["all_rows_admitted"] and report["admitted_count"] == len(FINITE_PART_COMPONENT_ORDER)
    return {"passed": p, "status": "PASS" if p else "FAIL", "shape_only": True, "report": report}


def check_T_w_payload_source_pack_requires_provenance_chain():
    row = replace(_reviewed_shape_row(FINITE_PART_COMPONENT_ORDER[0]), provenance_chain=())
    p = not _source_pack_row_complete(row)
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_payload_source_pack_requires_license_or_access_note():
    row = replace(_reviewed_shape_row(FINITE_PART_COMPONENT_ORDER[0]), license_or_access_note="UNFILLED")
    p = not _source_pack_row_complete(row)
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_payload_source_pack_rejects_unreviewed_numeric_rows():
    row = replace(_reviewed_shape_row(FINITE_PART_COMPONENT_ORDER[0]), review_status="INDEPENDENT_SOURCE_PENDING_REVIEW")
    p = not _source_pack_row_complete(row)
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_payload_source_pack_rejects_duplicate_components():
    rows = list(reviewed_shape_source_pack())
    rows[-1] = replace(rows[-1], component_id=rows[0].component_id, symbol=rows[0].symbol)
    report = source_pack_admission_report(tuple(rows))
    p = not report["table_shape_ok"] and rows[0].component_id in report["duplicate_ids"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_payload_source_pack_rejects_missing_components():
    report = source_pack_admission_report(reviewed_shape_source_pack()[:-1])
    p = not report["table_shape_ok"] and len(report["missing_ids"]) == 1
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_payload_source_pack_rejects_unknown_components():
    rows = list(reviewed_shape_source_pack())
    rows[-1] = replace(rows[-1], component_id="Delta_r_fake_source_pack_component", symbol="Delta_r_fake")
    report = source_pack_admission_report(tuple(rows))
    p = not report["table_shape_ok"] and "Delta_r_fake_source_pack_component" in report["unknown_ids"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_payload_source_pack_rejects_apf_anchor_consumption():
    row = replace(_reviewed_shape_row(FINITE_PART_COMPONENT_ORDER[0]), apf_target_consumed=True)
    p = not _source_pack_row_complete(row)
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_payload_source_pack_rejects_observed_W_consumption():
    row = replace(_reviewed_shape_row(FINITE_PART_COMPONENT_ORDER[0]), target_observables_consumed=("observed_M_W",))
    p = not _source_pack_row_complete(row)
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_payload_source_pack_rejects_delta_r_residual_fit():
    row = replace(_reviewed_shape_row(FINITE_PART_COMPONENT_ORDER[0]), target_observables_consumed=("component_pack_chosen_to_close_delta_r_residual",))
    p = not _source_pack_row_complete(row)
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_payload_source_pack_forbidden_inputs_superset_adapter():
    p = set(FORBIDDEN_NUMERIC_SOURCE_INPUTS).issubset(set(FORBIDDEN_SOURCE_PACK_INPUTS))
    return {"passed": p, "status": "PASS" if p else "FAIL", "forbidden_count": len(FORBIDDEN_SOURCE_PACK_INPUTS)}


def check_T_w_payload_source_pack_no_component_sum_certification_yet():
    p = not NUMERICAL_COMPONENT_VALUES_SUPPLIED and not COMPONENT_SUM_CERTIFIED and not PHYSICAL_W_TRANSPORT_CLOSED
    return {"passed": p, "status": "PASS" if p else "FAIL", "component_sum_certified": COMPONENT_SUM_CERTIFIED}


def check_T_w_payload_source_pack_codomain_not_physical_export():
    p = not PHYSICAL_W_TRANSPORT_CLOSED and not EXPORTS_PHYSICAL_M_W and not EXPORTS_PHYSICAL_SCHEME_MASSES
    return {"passed": p, "status": "PASS" if p else "FAIL", "exports_physical_M_W": EXPORTS_PHYSICAL_M_W}


def check_T_w_payload_source_pack_completion_gate_remains_locked():
    d = _check_completion()
    p = _passed(d) and not PHYSICAL_W_TRANSPORT_CLOSED
    return {"passed": p, "status": "PASS" if p else "FAIL", "completion_gate": d.get("status")}


def check_T_w_payload_source_pack_manifest_export_shape():
    m = source_pack_manifest()
    p = m["status"] == W_PAYLOAD_SOURCE_PACK_STATUS and len(m["rows"]) == len(FINITE_PART_COMPONENT_ORDER)
    return {"passed": p, "status": "PASS" if p else "FAIL", "manifest": m}


def check_T_w_payload_source_pack_bank_closure():
    deps = [
        check_T_w_payload_source_pack_status_declared(),
        check_T_w_payload_source_pack_depends_on_v98_fixture(),
        check_T_w_payload_source_pack_schema_extends_fixture_and_adapter(),
        check_T_w_payload_source_pack_covers_all_components(),
        check_T_w_payload_source_pack_symbols_match_skeleton(),
        check_T_w_payload_source_pack_empty_by_default(),
        check_T_w_payload_source_pack_empty_rows_rejected(),
        check_T_w_payload_source_pack_reviewed_shape_rows_admissible(),
        check_T_w_payload_source_pack_requires_provenance_chain(),
        check_T_w_payload_source_pack_requires_license_or_access_note(),
        check_T_w_payload_source_pack_rejects_unreviewed_numeric_rows(),
        check_T_w_payload_source_pack_rejects_duplicate_components(),
        check_T_w_payload_source_pack_rejects_missing_components(),
        check_T_w_payload_source_pack_rejects_unknown_components(),
        check_T_w_payload_source_pack_rejects_apf_anchor_consumption(),
        check_T_w_payload_source_pack_rejects_observed_W_consumption(),
        check_T_w_payload_source_pack_rejects_delta_r_residual_fit(),
        check_T_w_payload_source_pack_forbidden_inputs_superset_adapter(),
        check_T_w_payload_source_pack_no_component_sum_certification_yet(),
        check_T_w_payload_source_pack_codomain_not_physical_export(),
        check_T_w_payload_source_pack_completion_gate_remains_locked(),
        check_T_w_payload_source_pack_manifest_export_shape(),
    ]
    p = all(_passed(d) for d in deps)
    return {
        "passed": p,
        "status": "PASS" if p else "FAIL",
        "tier": 4,
        "epistemic": W_PAYLOAD_SOURCE_PACK_STATUS,
        "dependencies": [str(d.get("status")) for d in deps],
        "manifest": source_pack_manifest(),
        "closed_now": "independent finite-part payload source-pack manifest and admission gate",
        "not_closed": "actual independent finite-part numerical rows, component-sum certificate, covariance/uncertainty propagation, physical W export",
    }

_CHECKS: Dict[str, Any] = {
    "T_w_payload_source_pack_status_declared": check_T_w_payload_source_pack_status_declared,
    "T_w_payload_source_pack_depends_on_v98_fixture": check_T_w_payload_source_pack_depends_on_v98_fixture,
    "T_w_payload_source_pack_schema_extends_fixture_and_adapter": check_T_w_payload_source_pack_schema_extends_fixture_and_adapter,
    "T_w_payload_source_pack_covers_all_components": check_T_w_payload_source_pack_covers_all_components,
    "T_w_payload_source_pack_symbols_match_skeleton": check_T_w_payload_source_pack_symbols_match_skeleton,
    "T_w_payload_source_pack_empty_by_default": check_T_w_payload_source_pack_empty_by_default,
    "T_w_payload_source_pack_empty_rows_rejected": check_T_w_payload_source_pack_empty_rows_rejected,
    "T_w_payload_source_pack_reviewed_shape_rows_admissible": check_T_w_payload_source_pack_reviewed_shape_rows_admissible,
    "T_w_payload_source_pack_requires_provenance_chain": check_T_w_payload_source_pack_requires_provenance_chain,
    "T_w_payload_source_pack_requires_license_or_access_note": check_T_w_payload_source_pack_requires_license_or_access_note,
    "T_w_payload_source_pack_rejects_unreviewed_numeric_rows": check_T_w_payload_source_pack_rejects_unreviewed_numeric_rows,
    "T_w_payload_source_pack_rejects_duplicate_components": check_T_w_payload_source_pack_rejects_duplicate_components,
    "T_w_payload_source_pack_rejects_missing_components": check_T_w_payload_source_pack_rejects_missing_components,
    "T_w_payload_source_pack_rejects_unknown_components": check_T_w_payload_source_pack_rejects_unknown_components,
    "T_w_payload_source_pack_rejects_apf_anchor_consumption": check_T_w_payload_source_pack_rejects_apf_anchor_consumption,
    "T_w_payload_source_pack_rejects_observed_W_consumption": check_T_w_payload_source_pack_rejects_observed_W_consumption,
    "T_w_payload_source_pack_rejects_delta_r_residual_fit": check_T_w_payload_source_pack_rejects_delta_r_residual_fit,
    "T_w_payload_source_pack_forbidden_inputs_superset_adapter": check_T_w_payload_source_pack_forbidden_inputs_superset_adapter,
    "T_w_payload_source_pack_no_component_sum_certification_yet": check_T_w_payload_source_pack_no_component_sum_certification_yet,
    "T_w_payload_source_pack_codomain_not_physical_export": check_T_w_payload_source_pack_codomain_not_physical_export,
    "T_w_payload_source_pack_completion_gate_remains_locked": check_T_w_payload_source_pack_completion_gate_remains_locked,
    "T_w_payload_source_pack_manifest_export_shape": check_T_w_payload_source_pack_manifest_export_shape,
    "T_w_payload_source_pack_bank_closure": check_T_w_payload_source_pack_bank_closure,
}


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
    return {"passed": ok, "status": "W_TRACE_PAYLOAD_SOURCE_PACK_BANK_PASS" if ok else "W_TRACE_PAYLOAD_SOURCE_PACK_BANK_FAIL", "checks": rows, "manifest": source_pack_manifest()}


if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
