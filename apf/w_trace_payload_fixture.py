"""W_TRACE finite-part payload fixture / independent source table v0.

v9.8 (2026-05-09 LATER-16): payload-table harness after v9.7.
This module banks the concrete fixture/table structure into which independent
finite-part component payloads may be admitted.  It deliberately ships with no
numerical finite-part values and therefore does not close Delta_r, physical W
transport, or physical scheme masses.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, fields, replace
from typing import Any, Dict, Iterable, Mapping, Sequence, Tuple

from apf.w_trace_numeric_source_adapter import (
    W_NUMERIC_SOURCE_ADAPTER_STATUS,
    REQUIRED_SOURCE_FIELDS,
    FORBIDDEN_NUMERIC_SOURCE_INPUTS,
    admitted_numeric_payload,
    adapter_slots,
    numeric_source_adapter_contract,
    check_T_w_numeric_source_adapter_bank_closure as _check_v97,
)
from apf.w_trace_finite_part_skeleton import (
    COMPONENT_SYMBOLS,
    FINITE_PART_COMPONENT_ORDER,
)
from apf.trace_transport_completion import (
    check_T_physical_export_gate_locked_until_all_certificates_filled as _check_completion,
)

W_PAYLOAD_FIXTURE_STATUS = "P_w_payload_fixture"
PAYLOAD_FIXTURE_DECLARED = True
NUMERICAL_COMPONENT_VALUES_SUPPLIED = False
COMPONENT_SUM_CERTIFIED = False
COVARIANCE_PROTOCOL_SUPPLIED = False
UNCERTAINTY_PROTOCOL_SUPPLIED = False
PHYSICAL_W_TRANSPORT_CLOSED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

PAYLOAD_TABLE_VERSION = "w_trace_finite_part_payload_fixture_v0"
PAYLOAD_TABLE_MODE = "EMPTY_ADMISSION_HARNESS"
PAYLOAD_TABLE_SHA_POLICY = "sha256_or_stable_table_locator_required_before_admission"

@dataclass(frozen=True)
class PayloadFixtureRow:
    component_id: str
    symbol: str
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
    status: str = "OPEN_WAITING_FOR_INDEPENDENT_NUMERICAL_SOURCE"
    fixture_note: str = "schema-only row; not an admitted finite-part value"


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def payload_fixture_rows() -> Tuple[PayloadFixtureRow, ...]:
    return tuple(PayloadFixtureRow(cid, COMPONENT_SYMBOLS[cid]) for cid in FINITE_PART_COMPONENT_ORDER)


def payload_fixture_manifest() -> Dict[str, Any]:
    return {
        "status": W_PAYLOAD_FIXTURE_STATUS,
        "upstream_status": W_NUMERIC_SOURCE_ADAPTER_STATUS,
        "table_version": PAYLOAD_TABLE_VERSION,
        "table_mode": PAYLOAD_TABLE_MODE,
        "sha_policy": PAYLOAD_TABLE_SHA_POLICY,
        "required_source_fields": REQUIRED_SOURCE_FIELDS,
        "component_order": FINITE_PART_COMPONENT_ORDER,
        "rows": tuple(asdict(r) for r in payload_fixture_rows()),
        "numerical_component_values_supplied": NUMERICAL_COMPONENT_VALUES_SUPPLIED,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
    }


def _row_to_payload(row: PayloadFixtureRow | Mapping[str, Any]) -> Dict[str, Any]:
    if isinstance(row, PayloadFixtureRow):
        d = asdict(row)
    else:
        d = dict(row)
    # The v9.7 adapter requires exactly the source fields; fixture-only fields
    # are metadata and are not part of payload admission.
    return {k: d.get(k) for k in REQUIRED_SOURCE_FIELDS}


def payload_admission_report(rows: Sequence[PayloadFixtureRow | Mapping[str, Any]]) -> Dict[str, Any]:
    payloads = tuple(_row_to_payload(r) for r in rows)
    ids = tuple(p.get("component_id") for p in payloads)
    duplicate_ids = tuple(sorted({x for x in ids if ids.count(x) > 1 and x is not None}))
    missing_ids = tuple(x for x in FINITE_PART_COMPONENT_ORDER if x not in ids)
    unknown_ids = tuple(x for x in ids if x not in FINITE_PART_COMPONENT_ORDER)
    row_results = tuple(admitted_numeric_payload(p) for p in payloads)
    table_shape_ok = not duplicate_ids and not missing_ids and not unknown_ids and len(payloads) == len(FINITE_PART_COMPONENT_ORDER)
    all_rows_admitted = all(row_results) and table_shape_ok
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
        "total_count": len(payloads),
    }


def _synthetic_independent_row(component_id: str) -> PayloadFixtureRow:
    """Shape-only row for predicate tests; not shipped as a value table."""
    return PayloadFixtureRow(
        component_id=component_id,
        symbol=COMPONENT_SYMBOLS[component_id],
        source_class="independent_loop_library",
        source_name="future_independent_loop_payload_fixture",
        version_or_citation="UNFILLED_TEST_SHAPE_NOT_A_VALUE",
        input_scheme="alpha_G_F_MZ",
        renormalization_scheme="on_shell",
        gauge_convention="declared_test_gauge",
        numeric_value="1.0e-3",
        uncertainty="1.0e-6",
        checksum_or_table_locator="sha256:shape-test-not-a-source",
        status="SHAPE_TEST_ONLY_NOT_ADMITTED_TO_BANK_AS_DATA",
        fixture_note="positive-shape predicate test only; not a finite-part claim",
    )


def synthetic_independent_payload_table() -> Tuple[PayloadFixtureRow, ...]:
    return tuple(_synthetic_independent_row(cid) for cid in FINITE_PART_COMPONENT_ORDER)


def check_T_w_payload_fixture_status_declared():
    p = W_PAYLOAD_FIXTURE_STATUS == "P_w_payload_fixture" and PAYLOAD_FIXTURE_DECLARED
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_PAYLOAD_FIXTURE_STATUS}


def check_T_w_payload_fixture_depends_on_v97_adapter():
    d = _check_v97()
    p = _passed(d) and W_NUMERIC_SOURCE_ADAPTER_STATUS == "P_w_numeric_source_adapter"
    return {"passed": p, "status": "PASS" if p else "FAIL", "upstream": d.get("status")}


def check_T_w_payload_fixture_manifest_schema_complete():
    have = {f.name for f in fields(PayloadFixtureRow)}
    missing = [x for x in REQUIRED_SOURCE_FIELDS if x not in have]
    p = not missing and "fixture_note" in have
    return {"passed": p, "status": "PASS" if p else "FAIL", "missing": missing}


def check_T_w_payload_fixture_covers_all_components():
    ids = tuple(r.component_id for r in payload_fixture_rows())
    p = ids == FINITE_PART_COMPONENT_ORDER
    return {"passed": p, "status": "PASS" if p else "FAIL", "component_order": ids}


def check_T_w_payload_fixture_symbols_match_skeleton():
    bad = [r.component_id for r in payload_fixture_rows() if r.symbol != COMPONENT_SYMBOLS[r.component_id]]
    return {"passed": not bad, "status": "PASS" if not bad else "FAIL", "bad": bad}


def check_T_w_payload_fixture_rows_unfilled_by_default():
    rows = payload_fixture_rows()
    p = all(r.numeric_value == "UNSUPPLIED" and r.uncertainty == "UNSUPPLIED" and r.status.startswith("OPEN_") for r in rows)
    return {"passed": p, "status": "PASS" if p else "FAIL", "numerical_component_values_supplied": NUMERICAL_COMPONENT_VALUES_SUPPLIED}


def check_T_w_payload_fixture_empty_table_rejected_by_admission():
    report = payload_admission_report(payload_fixture_rows())
    p = report["table_shape_ok"] and not report["all_rows_admitted"] and report["admitted_count"] == 0
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_payload_fixture_positive_shape_table_admissible():
    report = payload_admission_report(synthetic_independent_payload_table())
    p = report["table_shape_ok"] and report["all_rows_admitted"] and report["admitted_count"] == len(FINITE_PART_COMPONENT_ORDER)
    return {"passed": p, "status": "PASS" if p else "FAIL", "shape_only": True, "report": report}


def check_T_w_payload_fixture_requires_full_component_coverage():
    partial = synthetic_independent_payload_table()[:-1]
    report = payload_admission_report(partial)
    p = not report["table_shape_ok"] and len(report["missing_ids"]) == 1
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_payload_fixture_rejects_duplicate_components():
    rows = list(synthetic_independent_payload_table())
    rows[-1] = replace(rows[-1], component_id=rows[0].component_id, symbol=rows[0].symbol)
    report = payload_admission_report(tuple(rows))
    p = not report["table_shape_ok"] and rows[0].component_id in report["duplicate_ids"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_payload_fixture_rejects_unknown_components():
    rows = list(synthetic_independent_payload_table())
    rows[-1] = replace(rows[-1], component_id="Delta_r_fake_component", symbol="Delta_r_fake")
    report = payload_admission_report(tuple(rows))
    p = not report["table_shape_ok"] and "Delta_r_fake_component" in report["unknown_ids"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": report}


def check_T_w_payload_fixture_rejects_target_backsolve_rows():
    row = replace(_synthetic_independent_row(FINITE_PART_COMPONENT_ORDER[0]), target_observables_consumed=("Delta_r_target_backsolve",))
    p = not admitted_numeric_payload(_row_to_payload(row))
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_payload_fixture_rejects_apf_anchor_consumption_rows():
    row = replace(_synthetic_independent_row(FINITE_PART_COMPONENT_ORDER[0]), apf_target_consumed=True)
    p = not admitted_numeric_payload(_row_to_payload(row))
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_payload_fixture_rejects_observed_W_consumption_rows():
    row = replace(_synthetic_independent_row(FINITE_PART_COMPONENT_ORDER[0]), target_observables_consumed=("observed_M_W",))
    p = not admitted_numeric_payload(_row_to_payload(row)) and "observed_M_W" in FORBIDDEN_NUMERIC_SOURCE_INPUTS
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_payload_fixture_checksum_locator_required():
    row = replace(_synthetic_independent_row(FINITE_PART_COMPONENT_ORDER[0]), checksum_or_table_locator="UNSUPPLIED")
    # v9.8 declares the policy.  Admission remains governed by v9.7; future
    # payload-loader admissibility may tighten the row-level predicate further.
    p = PAYLOAD_TABLE_SHA_POLICY.startswith("sha256") and _row_to_payload(row)["checksum_or_table_locator"] == "UNSUPPLIED"
    return {"passed": p, "status": "PASS" if p else "FAIL", "policy": PAYLOAD_TABLE_SHA_POLICY}


def check_T_w_payload_fixture_numeric_parse_policy_declared():
    allowed = ("decimal_string", "scientific_notation_string", "rational_string_future")
    p = "decimal_string" in allowed and "scientific_notation_string" in allowed
    return {"passed": p, "status": "PASS" if p else "FAIL", "allowed_numeric_encodings": allowed}


def check_T_w_payload_fixture_no_component_sum_certification_yet():
    report = payload_admission_report(payload_fixture_rows())
    p = not COMPONENT_SUM_CERTIFIED and not report["component_sum_certified"] and not NUMERICAL_COMPONENT_VALUES_SUPPLIED
    return {"passed": p, "status": "PASS" if p else "FAIL", "component_sum_certified": COMPONENT_SUM_CERTIFIED}


def check_T_w_payload_fixture_codomain_not_physical_export():
    p = not PHYSICAL_W_TRANSPORT_CLOSED and not EXPORTS_PHYSICAL_M_W and not EXPORTS_PHYSICAL_SCHEME_MASSES
    return {"passed": p, "status": "PASS" if p else "FAIL", "exports_physical_M_W": EXPORTS_PHYSICAL_M_W}


def check_T_w_payload_fixture_completion_gate_remains_locked():
    d = _check_completion()
    p = _passed(d) and not PHYSICAL_W_TRANSPORT_CLOSED
    return {"passed": p, "status": "PASS" if p else "FAIL", "completion_gate": d.get("status")}


def check_T_w_payload_fixture_bank_closure():
    deps = [
        check_T_w_payload_fixture_status_declared(),
        check_T_w_payload_fixture_depends_on_v97_adapter(),
        check_T_w_payload_fixture_manifest_schema_complete(),
        check_T_w_payload_fixture_covers_all_components(),
        check_T_w_payload_fixture_symbols_match_skeleton(),
        check_T_w_payload_fixture_rows_unfilled_by_default(),
        check_T_w_payload_fixture_empty_table_rejected_by_admission(),
        check_T_w_payload_fixture_positive_shape_table_admissible(),
        check_T_w_payload_fixture_requires_full_component_coverage(),
        check_T_w_payload_fixture_rejects_duplicate_components(),
        check_T_w_payload_fixture_rejects_unknown_components(),
        check_T_w_payload_fixture_rejects_target_backsolve_rows(),
        check_T_w_payload_fixture_rejects_apf_anchor_consumption_rows(),
        check_T_w_payload_fixture_rejects_observed_W_consumption_rows(),
        check_T_w_payload_fixture_checksum_locator_required(),
        check_T_w_payload_fixture_numeric_parse_policy_declared(),
        check_T_w_payload_fixture_no_component_sum_certification_yet(),
        check_T_w_payload_fixture_codomain_not_physical_export(),
        check_T_w_payload_fixture_completion_gate_remains_locked(),
    ]
    p = all(_passed(d) for d in deps)
    return {
        "passed": p,
        "status": "PASS" if p else "FAIL",
        "tier": 4,
        "epistemic": W_PAYLOAD_FIXTURE_STATUS,
        "dependencies": [str(d.get("status")) for d in deps],
        "manifest": payload_fixture_manifest(),
        "closed_now": "finite-part payload fixture/table harness and admission-report discipline",
        "not_closed": "actual independent numerical finite-part payloads, component-sum certificate, covariance/uncertainty propagation, physical W export",
    }

_CHECKS: Dict[str, Any] = {
    "T_w_payload_fixture_status_declared": check_T_w_payload_fixture_status_declared,
    "T_w_payload_fixture_depends_on_v97_adapter": check_T_w_payload_fixture_depends_on_v97_adapter,
    "T_w_payload_fixture_manifest_schema_complete": check_T_w_payload_fixture_manifest_schema_complete,
    "T_w_payload_fixture_covers_all_components": check_T_w_payload_fixture_covers_all_components,
    "T_w_payload_fixture_symbols_match_skeleton": check_T_w_payload_fixture_symbols_match_skeleton,
    "T_w_payload_fixture_rows_unfilled_by_default": check_T_w_payload_fixture_rows_unfilled_by_default,
    "T_w_payload_fixture_empty_table_rejected_by_admission": check_T_w_payload_fixture_empty_table_rejected_by_admission,
    "T_w_payload_fixture_positive_shape_table_admissible": check_T_w_payload_fixture_positive_shape_table_admissible,
    "T_w_payload_fixture_requires_full_component_coverage": check_T_w_payload_fixture_requires_full_component_coverage,
    "T_w_payload_fixture_rejects_duplicate_components": check_T_w_payload_fixture_rejects_duplicate_components,
    "T_w_payload_fixture_rejects_unknown_components": check_T_w_payload_fixture_rejects_unknown_components,
    "T_w_payload_fixture_rejects_target_backsolve_rows": check_T_w_payload_fixture_rejects_target_backsolve_rows,
    "T_w_payload_fixture_rejects_apf_anchor_consumption_rows": check_T_w_payload_fixture_rejects_apf_anchor_consumption_rows,
    "T_w_payload_fixture_rejects_observed_W_consumption_rows": check_T_w_payload_fixture_rejects_observed_W_consumption_rows,
    "T_w_payload_fixture_checksum_locator_required": check_T_w_payload_fixture_checksum_locator_required,
    "T_w_payload_fixture_numeric_parse_policy_declared": check_T_w_payload_fixture_numeric_parse_policy_declared,
    "T_w_payload_fixture_no_component_sum_certification_yet": check_T_w_payload_fixture_no_component_sum_certification_yet,
    "T_w_payload_fixture_codomain_not_physical_export": check_T_w_payload_fixture_codomain_not_physical_export,
    "T_w_payload_fixture_completion_gate_remains_locked": check_T_w_payload_fixture_completion_gate_remains_locked,
    "T_w_payload_fixture_bank_closure": check_T_w_payload_fixture_bank_closure,
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
    return {"passed": ok, "status": "W_TRACE_PAYLOAD_FIXTURE_BANK_PASS" if ok else "W_TRACE_PAYLOAD_FIXTURE_BANK_FAIL", "checks": rows, "manifest": payload_fixture_manifest()}

if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
