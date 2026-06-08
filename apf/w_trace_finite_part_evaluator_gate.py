"""W_TRACE independent finite-part evaluator / component-sum certificate gate.

v9.5 (2026-05-08 LATER-13): route-specific evaluator gate after the
v9.4 finite-part ledger.  This module is the hard stop between an APF-anchor
Delta_r target and any honest W on-shell export.  It defines the independent
component-evaluation certificate that would be required to close the W route,
and proves that the current codebase does not yet possess that certificate.

Closed here:
    - The evaluator/certificate schema is typed and banked.
    - Every v9.4 finite-part component is assigned an independent source
      requirement and a no-fit/no-target-input rule.
    - The component-sum predicate is explicit: only independently supplied
      component values may be summed and compared to the APF-anchor Delta_r.
    - The obstruction certificate is executable: no supplied finite parts,
      no counterterm finite part, no covariance/uncertainty protocol, therefore
      no physical W export.

Not closed here:
    - No loop/counterterm finite part is numerically evaluated.
    - No component sum is certified against the APF anchor.
    - No physical W mass or physical scheme mass vector is exported.

Status discipline:
    - upstream finite-part ledger: [P_w_finite_part_ledger]
    - this module: [P_w_finite_part_evaluator_gate]
    - physical W/on-shell transport remains OPEN.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, fields
from decimal import Decimal
from typing import Any, Dict, Mapping, Tuple

from apf.w_trace_finite_part_ledger import (
    W_FINITE_PART_LEDGER_STATUS,
    FINITE_PART_COMPONENT_ORDER,
    FORBIDDEN_FINITE_PART_INPUTS,
    apf_anchor_delta_r_target,
    finite_part_components,
    finite_part_ledger,
    check_T_w_finite_part_ledger_bank_closure as _check_T_w_finite_part_ledger_bank_closure,
)
from apf.w_trace_onshell_transport import W_ROUTE_ID
from apf.trace_transport_completion import (
    check_T_physical_export_gate_locked_until_all_certificates_filled as _check_T_physical_export_gate_locked_until_all_certificates_filled,
)

W_FINITE_PART_EVALUATOR_GATE_STATUS = "P_w_finite_part_evaluator_gate"
EVALUATOR_GATE_DECLARED = True
INDEPENDENT_COMPONENT_VALUES_SUPPLIED = False
INDEPENDENT_COUNTERTERM_SUPPLIED = False
COMPONENT_SUM_CERTIFIED = False
COVARIANCE_PROTOCOL_SUPPLIED = False
UNCERTAINTY_PROTOCOL_SUPPLIED = False
PHYSICAL_W_TRANSPORT_CLOSED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

COMPONENT_SUM_TOLERANCE = Decimal("1e-12")

REQUIRED_EVALUATION_SLOT_FIELDS: Tuple[str, ...] = (
    "component_id",
    "independent_source_requirement",
    "allowed_dependencies",
    "supplied_value",
    "supplied_uncertainty",
    "provenance_status",
    "consumes_apf_anchor_delta_r_target",
    "consumes_observed_M_W",
    "fit_status",
    "certification_status",
)

FORBIDDEN_EVALUATOR_INPUTS: Tuple[str, ...] = tuple(sorted(set(
    FORBIDDEN_FINITE_PART_INPUTS + (
        "apf_anchor_delta_r_target_as_component_input",
        "Delta_r_target_backsolve",
        "component_residual_fit",
        "posthoc_counterterm_fit",
        "observed_W_mass_residual",
    )
)))

SOURCE_REQUIREMENTS: Dict[str, str] = {
    "delta_alpha_running_component": "independent alpha-running finite-part calculation with provenance",
    "delta_rho_oblique_component": "independent oblique/rho finite-part calculation with declared mass/input basis",
    "fermionic_loop_finite_component": "independent fermionic loop finite-part calculation",
    "bosonic_loop_finite_component": "independent bosonic loop finite-part calculation",
    "vertex_box_finite_component": "independent muon-decay vertex/box finite-part calculation",
    "scheme_conversion_counterterm_component": "declared on-shell finite counterterm convention, not tuned to W residual",
    "correlation_covariance_component": "source covariance matrix and propagation map",
    "uncertainty_propagation_component": "declared uncertainty propagation protocol",
}


@dataclass(frozen=True)
class WFinitePartEvaluationSlot:
    """One independent-evaluation slot for a v9.4 finite-part component."""

    component_id: str
    independent_source_requirement: str
    allowed_dependencies: Tuple[str, ...]
    supplied_value: str = "NOT_SUPPLIED"
    supplied_uncertainty: str = "NOT_SUPPLIED"
    provenance_status: str = "REQUIRED_NOT_SUPPLIED"
    consumes_apf_anchor_delta_r_target: bool = False
    consumes_observed_M_W: bool = False
    fit_status: str = "NO_FIT_ALLOWED"
    certification_status: str = "OPEN_UNCERTIFIED"


@dataclass(frozen=True)
class WFinitePartComponentSumCertificate:
    """Certificate shape for comparing independent components to the APF target."""

    route_id: str
    status: str
    upstream_status: str
    apf_anchor_delta_r_target: str
    tolerance: str
    evaluation_slots: Tuple[WFinitePartEvaluationSlot, ...]
    forbidden_inputs: Tuple[str, ...]
    independent_component_values_supplied: bool = False
    independent_counterterm_supplied: bool = False
    covariance_protocol_supplied: bool = False
    uncertainty_protocol_supplied: bool = False
    component_sum_certified: bool = False
    physical_W_transport_closed: bool = False
    exports_physical_M_W: bool = False


def _passed(result: Mapping[str, Any]) -> bool:
    return bool(result.get("passed") is True or str(result.get("status", "")).upper() in {"PASS", "P"})


def evaluation_slots() -> Tuple[WFinitePartEvaluationSlot, ...]:
    comps = {c.component_id: c for c in finite_part_components()}
    slots = []
    for cid in FINITE_PART_COMPONENT_ORDER:
        c = comps[cid]
        deps = tuple(d for d in c.dependencies if d != "apf_anchor_delta_r_target")
        slots.append(WFinitePartEvaluationSlot(
            component_id=cid,
            independent_source_requirement=SOURCE_REQUIREMENTS[cid],
            allowed_dependencies=deps,
        ))
    return tuple(slots)


def component_sum_certificate() -> Dict[str, Any]:
    cert = WFinitePartComponentSumCertificate(
        route_id=W_ROUTE_ID,
        status=W_FINITE_PART_EVALUATOR_GATE_STATUS,
        upstream_status=W_FINITE_PART_LEDGER_STATUS,
        apf_anchor_delta_r_target=f"{apf_anchor_delta_r_target():.17E}",
        tolerance=f"{COMPONENT_SUM_TOLERANCE:.1E}",
        evaluation_slots=evaluation_slots(),
        forbidden_inputs=FORBIDDEN_EVALUATOR_INPUTS,
        independent_component_values_supplied=False,
        independent_counterterm_supplied=False,
        covariance_protocol_supplied=False,
        uncertainty_protocol_supplied=False,
        component_sum_certified=False,
        physical_W_transport_closed=False,
        exports_physical_M_W=False,
    )
    data = asdict(cert)
    data["evaluation_slots"] = tuple(asdict(s) for s in cert.evaluation_slots)
    return data


def component_sum_predicate(values: Mapping[str, Decimal], tolerance: Decimal = COMPONENT_SUM_TOLERANCE) -> Dict[str, Any]:
    """Pure predicate for a future independently supplied component sum.

    The APF target may be used only as the comparison target after independent
    components are supplied; it is never an allowed component input.
    """
    required = set(FINITE_PART_COMPONENT_ORDER)
    supplied = set(values)
    missing = sorted(required - supplied)
    extra = sorted(supplied - required)
    if missing or extra:
        return {"passed": False, "status": "OPEN_MISSING_COMPONENTS", "missing": missing, "extra": extra}
    total = sum(values[cid] for cid in FINITE_PART_COMPONENT_ORDER)
    target = apf_anchor_delta_r_target()
    residual = abs(total - target)
    passed = residual <= tolerance
    return {
        "passed": passed,
        "status": "CERTIFIED" if passed else "RESIDUAL_EXCEEDS_TOLERANCE",
        "component_sum": f"{total:.17E}",
        "apf_anchor_delta_r_target": f"{target:.17E}",
        "absolute_residual": f"{residual:.17E}",
        "tolerance": f"{tolerance:.1E}",
    }


def check_T_w_finite_part_evaluator_gate_status_declared() -> Dict[str, Any]:
    passed = W_FINITE_PART_EVALUATOR_GATE_STATUS == "P_w_finite_part_evaluator_gate" and EVALUATOR_GATE_DECLARED
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "tier": 4, "epistemic": W_FINITE_PART_EVALUATOR_GATE_STATUS, "closed_now": "independent evaluator gate declared", "not_closed": "independent component evaluation and physical W export"}


def check_T_w_finite_part_evaluator_depends_on_v94_ledger() -> Dict[str, Any]:
    dep = _check_T_w_finite_part_ledger_bank_closure()
    ledger = finite_part_ledger()
    passed = _passed(dep) and ledger["status"] == W_FINITE_PART_LEDGER_STATUS and ledger["apf_anchor_delta_r_target"] != "UNEVALUATED"
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "upstream": dep.get("status"), "upstream_status": ledger["status"], "target": ledger["apf_anchor_delta_r_target"]}


def check_T_w_finite_part_evaluator_slot_schema_complete() -> Dict[str, Any]:
    names = {f.name for f in fields(WFinitePartEvaluationSlot)}
    missing = [x for x in REQUIRED_EVALUATION_SLOT_FIELDS if x not in names]
    return {"passed": not missing, "status": "PASS" if not missing else "FAIL", "missing": missing, "schema": sorted(names)}


def check_T_w_finite_part_evaluator_slots_cover_v94_components() -> Dict[str, Any]:
    ids = tuple(s.component_id for s in evaluation_slots())
    passed = ids == FINITE_PART_COMPONENT_ORDER and len(ids) == len(finite_part_components())
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "slot_order": ids}


def check_T_w_finite_part_evaluator_source_requirements_declared() -> Dict[str, Any]:
    slots = evaluation_slots()
    missing = [s.component_id for s in slots if not s.independent_source_requirement or "independent" not in s.independent_source_requirement.lower() and s.component_id not in {"scheme_conversion_counterterm_component", "correlation_covariance_component", "uncertainty_propagation_component"}]
    passed = not missing and set(SOURCE_REQUIREMENTS) == set(FINITE_PART_COMPONENT_ORDER)
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "missing_or_weak": missing, "source_requirements": SOURCE_REQUIREMENTS}


def check_T_w_finite_part_evaluator_values_not_supplied_yet() -> Dict[str, Any]:
    slots = evaluation_slots()
    passed = all(s.supplied_value == "NOT_SUPPLIED" and s.provenance_status == "REQUIRED_NOT_SUPPLIED" for s in slots) and not INDEPENDENT_COMPONENT_VALUES_SUPPLIED
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "supplied_values": {s.component_id: s.supplied_value for s in slots}, "independent_component_values_supplied": False}


def check_T_w_finite_part_evaluator_target_not_component_input() -> Dict[str, Any]:
    slots = evaluation_slots()
    bad = [s.component_id for s in slots if s.consumes_apf_anchor_delta_r_target or "apf_anchor_delta_r_target" in s.allowed_dependencies]
    passed = not bad and "apf_anchor_delta_r_target_as_component_input" in FORBIDDEN_EVALUATOR_INPUTS
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "bad_slots": bad}


def check_T_w_finite_part_evaluator_observed_W_forbidden() -> Dict[str, Any]:
    slots = evaluation_slots()
    bad = [s.component_id for s in slots if s.consumes_observed_M_W]
    forbidden_hits = [x for x in FORBIDDEN_EVALUATOR_INPUTS if "observed" in x or "W_world" in x or "residual" in x]
    passed = not bad and "observed_M_W" in FORBIDDEN_EVALUATOR_INPUTS and forbidden_hits
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "bad_slots": bad, "forbidden_W_like_inputs": forbidden_hits}


def check_T_w_finite_part_evaluator_no_fit_or_backsolve_allowed() -> Dict[str, Any]:
    slots = evaluation_slots()
    bad = [s.component_id for s in slots if s.fit_status != "NO_FIT_ALLOWED"]
    passed = not bad and "Delta_r_target_backsolve" in FORBIDDEN_EVALUATOR_INPUTS and "component_residual_fit" in FORBIDDEN_EVALUATOR_INPUTS
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "bad_slots": bad}


def check_T_w_finite_part_component_sum_predicate_declared() -> Dict[str, Any]:
    pred = component_sum_predicate({})
    passed = pred["status"] == "OPEN_MISSING_COMPONENTS" and len(pred["missing"]) == len(FINITE_PART_COMPONENT_ORDER)
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "predicate_on_empty_values": pred}


def check_T_w_finite_part_component_sum_not_certified_without_values() -> Dict[str, Any]:
    cert = component_sum_certificate()
    passed = not cert["component_sum_certified"] and not COMPONENT_SUM_CERTIFIED and not cert["independent_component_values_supplied"]
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "component_sum_certified": False, "independent_component_values_supplied": False}


def check_T_w_finite_part_counterterm_evaluator_slot_required_open() -> Dict[str, Any]:
    slots = {s.component_id: s for s in evaluation_slots()}
    slot = slots.get("scheme_conversion_counterterm_component")
    passed = slot is not None and "counterterm" in slot.independent_source_requirement.lower() and slot.supplied_value == "NOT_SUPPLIED" and not INDEPENDENT_COUNTERTERM_SUPPLIED
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "counterterm_slot": asdict(slot) if slot else None}


def check_T_w_finite_part_covariance_uncertainty_still_block_export() -> Dict[str, Any]:
    slots = {s.component_id: s for s in evaluation_slots()}
    passed = (
        "correlation_covariance_component" in slots
        and "uncertainty_propagation_component" in slots
        and not COVARIANCE_PROTOCOL_SUPPLIED
        and not UNCERTAINTY_PROTOCOL_SUPPLIED
        and not PHYSICAL_W_TRANSPORT_CLOSED
    )
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "covariance_protocol_supplied": False, "uncertainty_protocol_supplied": False}


def check_T_w_finite_part_evaluator_completion_gate_remains_locked() -> Dict[str, Any]:
    dep = _check_T_physical_export_gate_locked_until_all_certificates_filled()
    cert = component_sum_certificate()
    passed = _passed(dep) and not cert["physical_W_transport_closed"] and not cert["exports_physical_M_W"] and not PHYSICAL_W_TRANSPORT_CLOSED
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "dependency": dep.get("status"), "physical_W_transport_closed": False}


def check_T_w_finite_part_evaluator_publication_ladder() -> Dict[str, Any]:
    ladder = (
        ("W finite-part component ledger", W_FINITE_PART_LEDGER_STATUS),
        ("W independent finite-part evaluator gate", W_FINITE_PART_EVALUATOR_GATE_STATUS),
        ("independent component values", "OPEN"),
        ("component-sum certificate", "OPEN"),
        ("physical W/on-shell transport", "OPEN"),
    )
    passed = ladder[1][1] == W_FINITE_PART_EVALUATOR_GATE_STATUS and ladder[-1][1] == "OPEN"
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "claim_ladder": ladder}


def check_T_w_finite_part_evaluator_no_physical_export() -> Dict[str, Any]:
    cert = component_sum_certificate()
    passed = not EXPORTS_PHYSICAL_M_W and not EXPORTS_PHYSICAL_SCHEME_MASSES and not cert["exports_physical_M_W"] and not cert["physical_W_transport_closed"]
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "exports_physical_M_W": False, "exports_physical_scheme_masses": False}


def check_T_w_finite_part_evaluator_next_requirements_explicit() -> Dict[str, Any]:
    requirements = (
        "supply independent numeric values for all eight finite-part slots",
        "supply a finite on-shell counterterm convention not tuned to W residual",
        "run the component-sum predicate against the APF-anchor Delta_r target",
        "supply covariance and uncertainty propagation protocols",
        "keep observed physical M_W outside every input ledger until comparison stage",
    )
    passed = len(requirements) == 5 and "observed physical M_W" in requirements[-1]
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "next_requirements": requirements}


def check_T_w_finite_part_evaluator_gate_bank_closure() -> Dict[str, Any]:
    deps = [
        check_T_w_finite_part_evaluator_gate_status_declared(),
        check_T_w_finite_part_evaluator_depends_on_v94_ledger(),
        check_T_w_finite_part_evaluator_slot_schema_complete(),
        check_T_w_finite_part_evaluator_slots_cover_v94_components(),
        check_T_w_finite_part_evaluator_source_requirements_declared(),
        check_T_w_finite_part_evaluator_values_not_supplied_yet(),
        check_T_w_finite_part_evaluator_target_not_component_input(),
        check_T_w_finite_part_evaluator_observed_W_forbidden(),
        check_T_w_finite_part_evaluator_no_fit_or_backsolve_allowed(),
        check_T_w_finite_part_component_sum_predicate_declared(),
        check_T_w_finite_part_component_sum_not_certified_without_values(),
        check_T_w_finite_part_counterterm_evaluator_slot_required_open(),
        check_T_w_finite_part_covariance_uncertainty_still_block_export(),
        check_T_w_finite_part_evaluator_completion_gate_remains_locked(),
        check_T_w_finite_part_evaluator_publication_ladder(),
        check_T_w_finite_part_evaluator_no_physical_export(),
        check_T_w_finite_part_evaluator_next_requirements_explicit(),
    ]
    passed = all(_passed(d) for d in deps)
    return {
        "passed": passed,
        "status": "PASS" if passed else "FAIL",
        "tier": 4,
        "epistemic": W_FINITE_PART_EVALUATOR_GATE_STATUS,
        "dependencies": [str(d.get("status")) for d in deps],
        "certificate": component_sum_certificate(),
        "closed_now": "independent finite-part evaluator gate and component-sum certificate predicate",
        "not_closed": "numeric component values, counterterm finite part, component-sum certificate, covariance/uncertainty propagation, physical W export",
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
    }


_CHECKS = {
    "T_w_finite_part_evaluator_gate_status_declared": check_T_w_finite_part_evaluator_gate_status_declared,
    "T_w_finite_part_evaluator_depends_on_v94_ledger": check_T_w_finite_part_evaluator_depends_on_v94_ledger,
    "T_w_finite_part_evaluator_slot_schema_complete": check_T_w_finite_part_evaluator_slot_schema_complete,
    "T_w_finite_part_evaluator_slots_cover_v94_components": check_T_w_finite_part_evaluator_slots_cover_v94_components,
    "T_w_finite_part_evaluator_source_requirements_declared": check_T_w_finite_part_evaluator_source_requirements_declared,
    "T_w_finite_part_evaluator_values_not_supplied_yet": check_T_w_finite_part_evaluator_values_not_supplied_yet,
    "T_w_finite_part_evaluator_target_not_component_input": check_T_w_finite_part_evaluator_target_not_component_input,
    "T_w_finite_part_evaluator_observed_W_forbidden": check_T_w_finite_part_evaluator_observed_W_forbidden,
    "T_w_finite_part_evaluator_no_fit_or_backsolve_allowed": check_T_w_finite_part_evaluator_no_fit_or_backsolve_allowed,
    "T_w_finite_part_component_sum_predicate_declared": check_T_w_finite_part_component_sum_predicate_declared,
    "T_w_finite_part_component_sum_not_certified_without_values": check_T_w_finite_part_component_sum_not_certified_without_values,
    "T_w_finite_part_counterterm_evaluator_slot_required_open": check_T_w_finite_part_counterterm_evaluator_slot_required_open,
    "T_w_finite_part_covariance_uncertainty_still_block_export": check_T_w_finite_part_covariance_uncertainty_still_block_export,
    "T_w_finite_part_evaluator_completion_gate_remains_locked": check_T_w_finite_part_evaluator_completion_gate_remains_locked,
    "T_w_finite_part_evaluator_publication_ladder": check_T_w_finite_part_evaluator_publication_ladder,
    "T_w_finite_part_evaluator_no_physical_export": check_T_w_finite_part_evaluator_no_physical_export,
    "T_w_finite_part_evaluator_next_requirements_explicit": check_T_w_finite_part_evaluator_next_requirements_explicit,
    "T_w_finite_part_evaluator_gate_bank_closure": check_T_w_finite_part_evaluator_gate_bank_closure,
}


def register(registry: Dict[str, Any]) -> None:
    """Register W_TRACE finite-part evaluator gate checks into the bank."""
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
        "passed": sum(1 for row in rows if row["passed"]),
        "total": len(rows),
        "status": "W_TRACE_FINITE_PART_EVALUATOR_GATE_BANK_PASS" if ok else "W_TRACE_FINITE_PART_EVALUATOR_GATE_BANK_FAIL",
        "bank_registered": True,
        "route_status": W_FINITE_PART_EVALUATOR_GATE_STATUS,
        "route_id": W_ROUTE_ID,
        "upstream_status": W_FINITE_PART_LEDGER_STATUS,
        "apf_anchor_delta_r_target": f"{apf_anchor_delta_r_target():.17E}",
        "independent_component_values_supplied": INDEPENDENT_COMPONENT_VALUES_SUPPLIED,
        "independent_counterterm_supplied": INDEPENDENT_COUNTERTERM_SUPPLIED,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "covariance_protocol_supplied": COVARIANCE_PROTOCOL_SUPPLIED,
        "uncertainty_protocol_supplied": UNCERTAINTY_PROTOCOL_SUPPLIED,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "slot_count": len(FINITE_PART_COMPONENT_ORDER),
        "results": rows,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_all(), indent=2))
