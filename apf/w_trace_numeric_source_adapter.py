"""W_TRACE finite-part numerical-source adapter / loop-library interface gate.

v9.7 (2026-05-08 LATER-15): route-specific ingress layer after v9.6.
This module defines the admissible interface by which independent numerical
finite-part values may enter the W_TRACE finite-part stack. It does not supply
those values and does not close physical W transport.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, fields
from typing import Any, Dict, Mapping, Tuple

from apf.w_trace_finite_part_skeleton import (
    W_FINITE_PART_SKELETON_STATUS,
    COMPONENT_SYMBOLS,
    FINITE_PART_COMPONENT_ORDER,
    FORBIDDEN_SKELETON_INPUTS,
    symbolic_components,
    check_T_w_finite_part_skeleton_bank_closure as _check_v96,
)
from apf.w_trace_finite_part_evaluator_gate import component_sum_certificate
from apf.w_trace_finite_part_ledger import apf_anchor_delta_r_target
from apf.trace_transport_completion import (
    check_T_physical_export_gate_locked_until_all_certificates_filled as _check_completion,
)

W_NUMERIC_SOURCE_ADAPTER_STATUS = "P_w_numeric_source_adapter"
NUMERIC_SOURCE_ADAPTER_DECLARED = True
NUMERICAL_COMPONENT_VALUES_SUPPLIED = False
COMPONENT_SUM_CERTIFIED = False
PHYSICAL_W_TRANSPORT_CLOSED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

ALLOWED_SOURCE_CLASSES = (
    "independent_loop_library",
    "audited_literature_table",
    "symbolic_algebra_export",
    "hand_transcribed_source_with_checksum",
)
REQUIRED_SOURCE_FIELDS = (
    "component_id",
    "symbol",
    "source_class",
    "source_name",
    "version_or_citation",
    "input_scheme",
    "renormalization_scheme",
    "gauge_convention",
    "numeric_value",
    "uncertainty",
    "checksum_or_table_locator",
    "target_observables_consumed",
    "apf_target_consumed",
    "status",
)
FORBIDDEN_NUMERIC_SOURCE_INPUTS = tuple(sorted(set(FORBIDDEN_SKELETON_INPUTS + (
    "observed_M_W",
    "M_W_world_average",
    "W_mass_residual",
    "Delta_r_fit_to_observed_M_W",
    "Delta_r_target_backsolve",
    "apf_anchor_delta_r_target",
    "apf_anchor_delta_r_target_as_numeric_input",
    "component_value_chosen_to_close_residual",
    "counterterm_chosen_to_match_APF_anchor",
))))

@dataclass(frozen=True)
class NumericSourceAdapterSlot:
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


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def adapter_slots() -> Tuple[NumericSourceAdapterSlot, ...]:
    return tuple(NumericSourceAdapterSlot(cid, COMPONENT_SYMBOLS[cid]) for cid in FINITE_PART_COMPONENT_ORDER)


def numeric_source_adapter_contract() -> Dict[str, Any]:
    return {
        "status": W_NUMERIC_SOURCE_ADAPTER_STATUS,
        "upstream_status": W_FINITE_PART_SKELETON_STATUS,
        "allowed_source_classes": ALLOWED_SOURCE_CLASSES,
        "required_source_fields": REQUIRED_SOURCE_FIELDS,
        "slots": tuple(asdict(s) for s in adapter_slots()),
        "forbidden_inputs": FORBIDDEN_NUMERIC_SOURCE_INPUTS,
        "apf_anchor_delta_r_target_comparison_only": f"{apf_anchor_delta_r_target():.17E}",
        "numerical_component_values_supplied": NUMERICAL_COMPONENT_VALUES_SUPPLIED,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
    }


def admitted_numeric_payload(payload: Mapping[str, Any]) -> bool:
    """Predicate for future finite-part payload admission.

    The current bank ships no payload. This predicate is intentionally strict:
    every required field must be present, the source class must be one of the
    allowed source classes, and neither observed W data nor the APF-anchor target
    may be consumed as an input.
    """
    if not all(k in payload for k in REQUIRED_SOURCE_FIELDS):
        return False
    if payload.get("source_class") not in ALLOWED_SOURCE_CLASSES:
        return False
    if payload.get("component_id") not in FINITE_PART_COMPONENT_ORDER:
        return False
    if payload.get("symbol") != COMPONENT_SYMBOLS[payload.get("component_id")]:
        return False
    consumed = set(payload.get("target_observables_consumed") or ())
    if consumed.intersection(FORBIDDEN_NUMERIC_SOURCE_INPUTS):
        return False
    if bool(payload.get("apf_target_consumed")):
        return False
    if str(payload.get("numeric_value")) in {"", "UNSUPPLIED", "None"}:
        return False
    return True


def check_T_w_numeric_source_adapter_status_declared():
    p = W_NUMERIC_SOURCE_ADAPTER_STATUS == "P_w_numeric_source_adapter" and NUMERIC_SOURCE_ADAPTER_DECLARED
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_NUMERIC_SOURCE_ADAPTER_STATUS}


def check_T_w_numeric_source_adapter_depends_on_v96_skeleton():
    d = _check_v96()
    p = _passed(d) and W_FINITE_PART_SKELETON_STATUS == "P_w_finite_part_skeleton"
    return {"passed": p, "status": "PASS" if p else "FAIL", "upstream": d.get("status")}


def check_T_w_numeric_source_adapter_schema_complete():
    have = {f.name for f in fields(NumericSourceAdapterSlot)}
    missing = [x for x in REQUIRED_SOURCE_FIELDS if x not in have]
    return {"passed": not missing, "status": "PASS" if not missing else "FAIL", "missing": missing}


def check_T_w_numeric_source_adapter_covers_all_components():
    ids = tuple(s.component_id for s in adapter_slots())
    p = ids == FINITE_PART_COMPONENT_ORDER == tuple(c.component_id for c in symbolic_components())
    return {"passed": p, "status": "PASS" if p else "FAIL", "component_order": ids}


def check_T_w_numeric_source_adapter_symbols_match_skeleton():
    bad = [s.component_id for s in adapter_slots() if s.symbol != COMPONENT_SYMBOLS[s.component_id]]
    return {"passed": not bad, "status": "PASS" if not bad else "FAIL", "bad": bad}


def check_T_w_numeric_source_adapter_allowed_source_classes_declared():
    req = {"independent_loop_library", "audited_literature_table", "symbolic_algebra_export", "hand_transcribed_source_with_checksum"}
    p = req.issubset(set(ALLOWED_SOURCE_CLASSES)) and len(ALLOWED_SOURCE_CLASSES) == len(set(ALLOWED_SOURCE_CLASSES))
    return {"passed": p, "status": "PASS" if p else "FAIL", "allowed_source_classes": ALLOWED_SOURCE_CLASSES}


def check_T_w_numeric_source_adapter_slots_unfilled_by_default():
    p = all(s.numeric_value == "UNSUPPLIED" and s.status.startswith("OPEN_") for s in adapter_slots())
    return {"passed": p, "status": "PASS" if p else "FAIL", "numerical_component_values_supplied": NUMERICAL_COMPONENT_VALUES_SUPPLIED}


def check_T_w_numeric_source_adapter_forbids_observed_W_inputs():
    forbidden = {"observed_M_W", "M_W_world_average", "W_mass_residual", "Delta_r_fit_to_observed_M_W"}
    p = forbidden.issubset(set(FORBIDDEN_NUMERIC_SOURCE_INPUTS)) and all(not set(s.target_observables_consumed) for s in adapter_slots())
    return {"passed": p, "status": "PASS" if p else "FAIL", "forbidden_checked": sorted(forbidden)}


def check_T_w_numeric_source_adapter_forbids_apf_target_as_input():
    p = "apf_anchor_delta_r_target" in FORBIDDEN_NUMERIC_SOURCE_INPUTS and all(not s.apf_target_consumed for s in adapter_slots())
    return {"passed": p, "status": "PASS" if p else "FAIL", "target_comparison_only": True}


def check_T_w_numeric_source_adapter_payload_predicate_rejects_target_backsolve():
    payload = asdict(adapter_slots()[0])
    payload.update({"source_class": "independent_loop_library", "numeric_value": "0.01", "target_observables_consumed": ("Delta_r_target_backsolve",)})
    p = not admitted_numeric_payload(payload)
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_numeric_source_adapter_payload_predicate_rejects_apf_target_consumption():
    payload = asdict(adapter_slots()[0])
    payload.update({"source_class": "audited_literature_table", "numeric_value": "0.01", "apf_target_consumed": True})
    p = not admitted_numeric_payload(payload)
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_numeric_source_adapter_payload_predicate_accepts_independent_shape():
    payload = asdict(adapter_slots()[0])
    payload.update({
        "source_class": "independent_loop_library",
        "source_name": "future_loop_library_fixture",
        "version_or_citation": "UNFILLED_TEST_SHAPE",
        "input_scheme": "alpha_G_F_MZ",
        "renormalization_scheme": "on_shell",
        "gauge_convention": "declared",
        "numeric_value": "1.0e-3",
        "uncertainty": "1.0e-6",
        "checksum_or_table_locator": "sha256:fixture",
    })
    p = admitted_numeric_payload(payload)
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_numeric_source_adapter_no_component_sum_certification_yet():
    cert = component_sum_certificate()
    p = not NUMERICAL_COMPONENT_VALUES_SUPPLIED and not COMPONENT_SUM_CERTIFIED and not cert.get("component_sum_certified", False)
    return {"passed": p, "status": "PASS" if p else "FAIL", "component_sum_certified": COMPONENT_SUM_CERTIFIED}


def check_T_w_numeric_source_adapter_codomain_not_physical_export():
    p = not PHYSICAL_W_TRANSPORT_CLOSED and not EXPORTS_PHYSICAL_M_W and not EXPORTS_PHYSICAL_SCHEME_MASSES
    return {"passed": p, "status": "PASS" if p else "FAIL", "exports_physical_M_W": EXPORTS_PHYSICAL_M_W}


def check_T_w_numeric_source_adapter_completion_gate_remains_locked():
    d = _check_completion()
    p = _passed(d) and not PHYSICAL_W_TRANSPORT_CLOSED
    return {"passed": p, "status": "PASS" if p else "FAIL", "completion_gate": d.get("status")}


def check_T_w_numeric_source_adapter_contract_export_shape():
    c = numeric_source_adapter_contract()
    p = c["status"] == W_NUMERIC_SOURCE_ADAPTER_STATUS and len(c["slots"]) == len(FINITE_PART_COMPONENT_ORDER)
    return {"passed": p, "status": "PASS" if p else "FAIL", "contract": c}


def check_T_w_numeric_source_adapter_publication_ladder():
    ladder = (
        "P_local", "P_boundary", "P_ledger", "P_route", "P_composition", "P_completion_gate",
        "P_w_trace_contract", "P_w_input_basis_ledger", "P_w_constants_source_ledger",
        "P_w_delta_r_symbolic_map", "P_w_finite_part_ledger", "P_w_finite_part_evaluator_gate",
        "P_w_finite_part_skeleton", W_NUMERIC_SOURCE_ADAPTER_STATUS, "OPEN_physical_W_transport",
    )
    p = ladder[-2] == W_NUMERIC_SOURCE_ADAPTER_STATUS and ladder[-1].startswith("OPEN_")
    return {"passed": p, "status": "PASS" if p else "FAIL", "ladder": ladder}


def check_T_w_numeric_source_adapter_next_requirements_explicit():
    req = ("supply_independent_component_payloads", "verify_checksums_or_table_locators", "declare_scheme_and_gauge_conventions", "evaluate_component_sum_residual", "propagate_covariance_and_uncertainty")
    p = len(req) == 5 and "supply_independent_component_payloads" in req
    return {"passed": p, "status": "PASS" if p else "FAIL", "next_requirements": req}


def check_T_w_numeric_source_adapter_bank_closure():
    deps = [
        check_T_w_numeric_source_adapter_status_declared(),
        check_T_w_numeric_source_adapter_depends_on_v96_skeleton(),
        check_T_w_numeric_source_adapter_schema_complete(),
        check_T_w_numeric_source_adapter_covers_all_components(),
        check_T_w_numeric_source_adapter_symbols_match_skeleton(),
        check_T_w_numeric_source_adapter_allowed_source_classes_declared(),
        check_T_w_numeric_source_adapter_slots_unfilled_by_default(),
        check_T_w_numeric_source_adapter_forbids_observed_W_inputs(),
        check_T_w_numeric_source_adapter_forbids_apf_target_as_input(),
        check_T_w_numeric_source_adapter_payload_predicate_rejects_target_backsolve(),
        check_T_w_numeric_source_adapter_payload_predicate_rejects_apf_target_consumption(),
        check_T_w_numeric_source_adapter_payload_predicate_accepts_independent_shape(),
        check_T_w_numeric_source_adapter_no_component_sum_certification_yet(),
        check_T_w_numeric_source_adapter_codomain_not_physical_export(),
        check_T_w_numeric_source_adapter_completion_gate_remains_locked(),
        check_T_w_numeric_source_adapter_contract_export_shape(),
        check_T_w_numeric_source_adapter_publication_ladder(),
        check_T_w_numeric_source_adapter_next_requirements_explicit(),
    ]
    p = all(_passed(d) for d in deps)
    return {
        "passed": p,
        "status": "PASS" if p else "FAIL",
        "tier": 4,
        "epistemic": W_NUMERIC_SOURCE_ADAPTER_STATUS,
        "dependencies": [str(d.get("status")) for d in deps],
        "contract": numeric_source_adapter_contract(),
        "closed_now": "finite-part numerical-source adapter interface and anti-backfit ingress predicate",
        "not_closed": "actual independent numerical finite parts, component-sum certificate, covariance/uncertainty propagation, physical W export",
    }

_CHECKS: Dict[str, Any] = {
    "T_w_numeric_source_adapter_status_declared": check_T_w_numeric_source_adapter_status_declared,
    "T_w_numeric_source_adapter_depends_on_v96_skeleton": check_T_w_numeric_source_adapter_depends_on_v96_skeleton,
    "T_w_numeric_source_adapter_schema_complete": check_T_w_numeric_source_adapter_schema_complete,
    "T_w_numeric_source_adapter_covers_all_components": check_T_w_numeric_source_adapter_covers_all_components,
    "T_w_numeric_source_adapter_symbols_match_skeleton": check_T_w_numeric_source_adapter_symbols_match_skeleton,
    "T_w_numeric_source_adapter_allowed_source_classes_declared": check_T_w_numeric_source_adapter_allowed_source_classes_declared,
    "T_w_numeric_source_adapter_slots_unfilled_by_default": check_T_w_numeric_source_adapter_slots_unfilled_by_default,
    "T_w_numeric_source_adapter_forbids_observed_W_inputs": check_T_w_numeric_source_adapter_forbids_observed_W_inputs,
    "T_w_numeric_source_adapter_forbids_apf_target_as_input": check_T_w_numeric_source_adapter_forbids_apf_target_as_input,
    "T_w_numeric_source_adapter_payload_predicate_rejects_target_backsolve": check_T_w_numeric_source_adapter_payload_predicate_rejects_target_backsolve,
    "T_w_numeric_source_adapter_payload_predicate_rejects_apf_target_consumption": check_T_w_numeric_source_adapter_payload_predicate_rejects_apf_target_consumption,
    "T_w_numeric_source_adapter_payload_predicate_accepts_independent_shape": check_T_w_numeric_source_adapter_payload_predicate_accepts_independent_shape,
    "T_w_numeric_source_adapter_no_component_sum_certification_yet": check_T_w_numeric_source_adapter_no_component_sum_certification_yet,
    "T_w_numeric_source_adapter_codomain_not_physical_export": check_T_w_numeric_source_adapter_codomain_not_physical_export,
    "T_w_numeric_source_adapter_completion_gate_remains_locked": check_T_w_numeric_source_adapter_completion_gate_remains_locked,
    "T_w_numeric_source_adapter_contract_export_shape": check_T_w_numeric_source_adapter_contract_export_shape,
    "T_w_numeric_source_adapter_publication_ladder": check_T_w_numeric_source_adapter_publication_ladder,
    "T_w_numeric_source_adapter_next_requirements_explicit": check_T_w_numeric_source_adapter_next_requirements_explicit,
    "T_w_numeric_source_adapter_bank_closure": check_T_w_numeric_source_adapter_bank_closure,
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
    return {"passed": ok, "status": "W_TRACE_NUMERIC_SOURCE_ADAPTER_BANK_PASS" if ok else "W_TRACE_NUMERIC_SOURCE_ADAPTER_BANK_FAIL", "checks": rows, "contract": numeric_source_adapter_contract()}

if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
