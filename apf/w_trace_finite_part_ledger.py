"""W_TRACE finite-part / Delta_r component-evaluation gate bank.

v9.4 (2026-05-08 LATER-12): route-specific finite-part ledger after the
v9.3 symbolic Delta_r map.  This module pushes the W_TRACE route one layer
harder without smuggling the observed W mass.  It decomposes the symbolic
Delta_r map into a component ledger, computes only the APF-anchor-implied
Delta_r target from W_TRACE plus the v9.2 non-W constants, and blocks physical
export until independent finite parts, counterterms, correlations, and
uncertainty propagation are evaluated.

Closed here:
    - The Delta_r finite-part component ledger is typed and complete.
    - The APF/W_TRACE anchor-implied Delta_r target is reproducibly computed
      from allowed non-W constants and M_W_TRACE, not from observed M_W.
    - Required loop/counterterm/correlation/uncertainty components are named,
      ordered, and kept unevaluated unless independently certified.
    - Target-observable residual fitting remains forbidden.

Not closed here:
    - The independent Standard-Model-like finite-part calculation is not done.
    - Counterterm finite parts are not evaluated.
    - The component sum is not certified equal to the APF anchor target.
    - No physical W mass or physical scheme mass vector is exported.

Status discipline:
    - upstream symbolic map: [P_w_delta_r_symbolic_map]
    - this module: [P_w_finite_part_ledger]
    - physical W/on-shell transport remains OPEN.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, fields
from decimal import Decimal, getcontext
from typing import Any, Dict, Mapping, Tuple

from apf.w_trace_constants_source_ledger import (
    ALPHA_INV_VALUE,
    G_F_VALUE,
    M_Z_VALUE_GEV,
    FORBIDDEN_CONSTANT_INPUTS,
    _ledger as _constants_ledger,
    check_T_w_constants_source_ledger_bank_closure as _check_T_w_constants_source_ledger_bank_closure,
)
from apf.w_trace_delta_r_finite_map import (
    W_DELTA_R_SYMBOLIC_MAP_STATUS,
    DELTA_R_SLOT_IDS,
    FORBIDDEN_DELTA_R_INPUTS,
    symbolic_delta_r_map,
    check_T_w_delta_r_symbolic_map_bank_closure as _check_T_w_delta_r_symbolic_map_bank_closure,
    check_T_w_delta_r_completion_gate_remains_locked as _check_T_w_delta_r_completion_gate_remains_locked,
)
from apf.w_trace_onshell_transport import W_ROUTE_ID, W_TRACE_EXPECTED_GEV
from apf.trace_transport_completion import (
    check_T_physical_export_gate_locked_until_all_certificates_filled as _check_T_physical_export_gate_locked_until_all_certificates_filled,
)

getcontext().prec = 50

W_FINITE_PART_LEDGER_STATUS = "P_w_finite_part_ledger"
FINITE_PART_LEDGER_DECLARED = True
APF_ANCHOR_DELTA_R_TARGET_COMPUTED = True
INDEPENDENT_FINITE_PARTS_EVALUATED = False
COUNTERTERM_FINITE_PARTS_EVALUATED = False
COMPONENT_SUM_CERTIFIED = False
CORRELATION_PROPAGATION_EVALUATED = False
UNCERTAINTY_PROTOCOL_EVALUATED = False
PHYSICAL_W_TRANSPORT_CLOSED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

REQUIRED_COMPONENT_FIELDS: Tuple[str, ...] = (
    "component_id",
    "component_kind",
    "role",
    "dependencies",
    "evaluation_status",
    "numeric_value",
    "uncertainty_value",
    "consumes_observed_M_W",
    "consumes_target_residual",
    "is_required_for_physical_export",
)

FINITE_PART_COMPONENT_ORDER: Tuple[str, ...] = (
    "delta_alpha_running_component",
    "delta_rho_oblique_component",
    "fermionic_loop_finite_component",
    "bosonic_loop_finite_component",
    "vertex_box_finite_component",
    "scheme_conversion_counterterm_component",
    "correlation_covariance_component",
    "uncertainty_propagation_component",
)

FORBIDDEN_FINITE_PART_INPUTS: Tuple[str, ...] = tuple(sorted(set(
    FORBIDDEN_CONSTANT_INPUTS + FORBIDDEN_DELTA_R_INPUTS + (
        "observed_M_W",
        "M_W_world_average",
        "target_W_mass_residual",
        "Delta_r_backsolved_from_observed_M_W",
        "counterterm_tuned_to_W_world_average",
        "finite_part_fitted_to_W_residual",
    )
)))

@dataclass(frozen=True)
class WFinitePartComponent:
    """One component required by the W Delta_r finite-part ledger."""

    component_id: str
    component_kind: str
    role: str
    dependencies: Tuple[str, ...]
    evaluation_status: str
    numeric_value: str = "UNEVALUATED"
    uncertainty_value: str = "UNEVALUATED"
    consumes_observed_M_W: bool = False
    consumes_target_residual: bool = False
    is_required_for_physical_export: bool = True

@dataclass(frozen=True)
class WFinitePartLedger:
    """Finite-part ledger for the W_TRACE Delta_r route."""

    route_id: str
    status: str
    upstream_symbolic_status: str
    allowed_numeric_inputs: Tuple[str, ...]
    local_trace_anchor: str
    apf_anchor_delta_r_target: str
    apf_anchor_delta_r_target_formula: str
    components: Tuple[WFinitePartComponent, ...]
    forbidden_inputs: Tuple[str, ...]
    independent_finite_parts_evaluated: bool = False
    counterterm_finite_parts_evaluated: bool = False
    component_sum_certified: bool = False
    correlation_propagation_evaluated: bool = False
    uncertainty_protocol_evaluated: bool = False
    exports_physical_M_W: bool = False
    physical_W_transport_closed: bool = False


def _passed(result: Mapping[str, Any]) -> bool:
    return bool(result.get("passed") is True or str(result.get("status", "")).upper() in {"PASS", "P"})


def _constant_symbol_ids() -> Tuple[str, ...]:
    return tuple(record.symbol_id for record in _constants_ledger().records)


def _decimal_pi() -> Decimal:
    # More precision than the input constants require; kept local to avoid an
    # external numerical dependency in the bank theorem.
    return Decimal("3.1415926535897932384626433832795028841971693993751")


def _decimal_sqrt2() -> Decimal:
    return Decimal(2).sqrt()


def apf_anchor_delta_r_target() -> Decimal:
    """Delta_r implied by the APF/W_TRACE anchor and allowed non-W inputs.

    This is *not* a fit to observed M_W.  It is the finite-correction target
    that an independent component calculation would have to reproduce before
    W_TRACE could be transported to an on-shell physical comparison.
    """
    alpha = Decimal(1) / ALPHA_INV_VALUE
    gf = G_F_VALUE
    mz = M_Z_VALUE_GEV
    mw = Decimal(str(W_TRACE_EXPECTED_GEV))
    lhs = (mw * mw) * (Decimal(1) - (mw * mw) / (mz * mz))
    rhs_prefactor = _decimal_pi() * alpha / (_decimal_sqrt2() * gf)
    return Decimal(1) - rhs_prefactor / lhs


def finite_part_components() -> Tuple[WFinitePartComponent, ...]:
    base = ("alpha_em_reference", "G_F_reference", "M_Z_on_shell_reference", "M_W_TRACE_anchor")
    return (
        WFinitePartComponent("delta_alpha_running_component", "running", "independent alpha(0)->EW-scale running contribution", ("alpha_em_reference",), "DECLARED_UNEVALUATED"),
        WFinitePartComponent("delta_rho_oblique_component", "oblique", "rho/T-like oblique finite contribution", base, "DECLARED_UNEVALUATED"),
        WFinitePartComponent("fermionic_loop_finite_component", "loop", "finite fermionic loop contribution", base, "DECLARED_UNEVALUATED"),
        WFinitePartComponent("bosonic_loop_finite_component", "loop", "finite bosonic loop contribution", base, "DECLARED_UNEVALUATED"),
        WFinitePartComponent("vertex_box_finite_component", "vertex_box", "muon-decay vertex/box finite contribution", ("alpha_em_reference", "G_F_reference", "M_Z_on_shell_reference"), "DECLARED_UNEVALUATED"),
        WFinitePartComponent("scheme_conversion_counterterm_component", "counterterm", "finite on-shell conversion/counterterm convention", base, "DECLARED_UNEVALUATED"),
        WFinitePartComponent("correlation_covariance_component", "covariance", "correlation propagation among sourced constants and finite parts", base, "DECLARED_UNEVALUATED"),
        WFinitePartComponent("uncertainty_propagation_component", "uncertainty", "uncertainty propagation protocol for route export", base, "DECLARED_UNEVALUATED"),
    )


def finite_part_ledger() -> Dict[str, Any]:
    target = apf_anchor_delta_r_target()
    ledger = WFinitePartLedger(
        route_id=W_ROUTE_ID,
        status=W_FINITE_PART_LEDGER_STATUS,
        upstream_symbolic_status=W_DELTA_R_SYMBOLIC_MAP_STATUS,
        allowed_numeric_inputs=_constant_symbol_ids(),
        local_trace_anchor=f"M_W_TRACE_GeV={W_TRACE_EXPECTED_GEV}",
        apf_anchor_delta_r_target=f"{target:.17E}",
        apf_anchor_delta_r_target_formula=(
            "1 - [pi*alpha_em/(sqrt(2)*G_F)] / "
            "[M_W_TRACE^2*(1-M_W_TRACE^2/M_Z^2)]"
        ),
        components=finite_part_components(),
        forbidden_inputs=FORBIDDEN_FINITE_PART_INPUTS,
        independent_finite_parts_evaluated=False,
        counterterm_finite_parts_evaluated=False,
        component_sum_certified=False,
        correlation_propagation_evaluated=False,
        uncertainty_protocol_evaluated=False,
        exports_physical_M_W=False,
        physical_W_transport_closed=False,
    )
    data = asdict(ledger)
    data["components"] = tuple(asdict(c) for c in ledger.components)
    return data


def check_T_w_finite_part_ledger_status_declared() -> Dict[str, Any]:
    passed = W_FINITE_PART_LEDGER_STATUS == "P_w_finite_part_ledger" and FINITE_PART_LEDGER_DECLARED
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "tier": 4, "epistemic": W_FINITE_PART_LEDGER_STATUS, "closed_now": "finite-part component ledger declared", "not_closed": "independent finite-part evaluation and physical W export"}


def check_T_w_finite_part_depends_on_v93_symbolic_map() -> Dict[str, Any]:
    dep = _check_T_w_delta_r_symbolic_map_bank_closure()
    m = symbolic_delta_r_map()
    passed = _passed(dep) and m["status"] == W_DELTA_R_SYMBOLIC_MAP_STATUS and set(DELTA_R_SLOT_IDS) <= set(m["delta_r_slots"])
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "upstream": dep.get("status"), "upstream_status": m["status"]}


def check_T_w_finite_part_component_schema_complete() -> Dict[str, Any]:
    names = {f.name for f in fields(WFinitePartComponent)}
    missing = [x for x in REQUIRED_COMPONENT_FIELDS if x not in names]
    return {"passed": not missing, "status": "PASS" if not missing else "FAIL", "missing": missing, "schema": sorted(names)}


def check_T_w_finite_part_required_components_enumerated() -> Dict[str, Any]:
    ids = tuple(c.component_id for c in finite_part_components())
    passed = ids == FINITE_PART_COMPONENT_ORDER and len(ids) == 8
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "component_order": ids}


def check_T_w_finite_part_anchor_delta_r_target_computed_from_trace_not_observed() -> Dict[str, Any]:
    d = finite_part_ledger()
    target = Decimal(d["apf_anchor_delta_r_target"])
    passed = (Decimal("0.03") < target < Decimal("0.05") and "M_W_TRACE" in d["apf_anchor_delta_r_target_formula"] and "observed" not in d["apf_anchor_delta_r_target_formula"].lower())
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "apf_anchor_delta_r_target": d["apf_anchor_delta_r_target"], "formula": d["apf_anchor_delta_r_target_formula"]}


def check_T_w_finite_part_allowed_inputs_are_v92_plus_trace_anchor() -> Dict[str, Any]:
    d = finite_part_ledger()
    allowed = set(d["allowed_numeric_inputs"])
    required = {"alpha_em_reference", "G_F_reference", "M_Z_on_shell_reference"}
    component_deps = set().union(*(set(c.dependencies) for c in finite_part_components()))
    passed = allowed == required and "M_W_TRACE_anchor" in component_deps and not (allowed & set(FORBIDDEN_FINITE_PART_INPUTS))
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "allowed_numeric_inputs": sorted(allowed), "component_deps": sorted(component_deps)}


def check_T_w_finite_part_no_observed_W_or_residual_inputs() -> Dict[str, Any]:
    d = finite_part_ledger()
    serialized = repr(d)
    bad_terms = ("M_W_world_average", "observed_W_mass", "CDF_M_W", "ATLAS_M_W", "CMS_M_W", "LEP_W", "target_W_mass_residual", "backsolved_from_observed")
    hits = [b for b in bad_terms if b in serialized and b not in repr(d["forbidden_inputs"])]
    component_flags = [(c.component_id, c.consumes_observed_M_W, c.consumes_target_residual) for c in finite_part_components()]
    passed = not hits and all((not a and not b) for _, a, b in component_flags) and "observed_M_W" in d["forbidden_inputs"]
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "hits": hits, "component_flags": component_flags}


def check_T_w_finite_part_components_declared_unevaluated() -> Dict[str, Any]:
    comps = finite_part_components()
    passed = all(c.evaluation_status == "DECLARED_UNEVALUATED" and c.numeric_value == "UNEVALUATED" for c in comps) and not INDEPENDENT_FINITE_PARTS_EVALUATED
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "statuses": {c.component_id: c.evaluation_status for c in comps}, "independent_finite_parts_evaluated": INDEPENDENT_FINITE_PARTS_EVALUATED}


def check_T_w_finite_part_counterterm_component_required_not_filled() -> Dict[str, Any]:
    comps = {c.component_id: c for c in finite_part_components()}
    c = comps.get("scheme_conversion_counterterm_component")
    passed = c is not None and c.component_kind == "counterterm" and c.evaluation_status == "DECLARED_UNEVALUATED" and not COUNTERTERM_FINITE_PARTS_EVALUATED
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "counterterm_component": asdict(c) if c else None}


def check_T_w_finite_part_component_sum_not_certified_yet() -> Dict[str, Any]:
    d = finite_part_ledger()
    passed = not d["component_sum_certified"] and not COMPONENT_SUM_CERTIFIED and d["apf_anchor_delta_r_target"] != "UNEVALUATED"
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "component_sum_certified": False, "apf_anchor_delta_r_target": d["apf_anchor_delta_r_target"]}


def check_T_w_finite_part_covariance_and_uncertainty_gate_open() -> Dict[str, Any]:
    d = finite_part_ledger()
    ids = {c["component_id"] for c in d["components"]}
    passed = "correlation_covariance_component" in ids and "uncertainty_propagation_component" in ids and not d["correlation_propagation_evaluated"] and not d["uncertainty_protocol_evaluated"]
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "correlation_propagation_evaluated": False, "uncertainty_protocol_evaluated": False}


def check_T_w_finite_part_completion_gate_remains_locked() -> Dict[str, Any]:
    dep1 = _check_T_w_delta_r_completion_gate_remains_locked()
    dep2 = _check_T_physical_export_gate_locked_until_all_certificates_filled()
    d = finite_part_ledger()
    passed = _passed(dep1) and _passed(dep2) and not d["physical_W_transport_closed"] and not d["exports_physical_M_W"]
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "dependencies": [dep1.get("status"), dep2.get("status")], "physical_W_transport_closed": False}


def check_T_w_finite_part_publication_claim_ladder() -> Dict[str, Any]:
    ladder = (
        ("W_TRACE local anchor", "P_local"),
        ("W route contract", "P_w_trace_contract"),
        ("W constants-source ledger", "P_w_constants_source_ledger"),
        ("W Delta_r symbolic map", "P_w_delta_r_symbolic_map"),
        ("W finite-part component ledger", W_FINITE_PART_LEDGER_STATUS),
        ("independent finite-part evaluation", "OPEN"),
        ("physical W/on-shell transport", "OPEN"),
    )
    passed = ladder[-1][1] == "OPEN" and ladder[-3][1] == W_FINITE_PART_LEDGER_STATUS
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "claim_ladder": ladder}


def check_T_w_finite_part_no_physical_W_export() -> Dict[str, Any]:
    d = finite_part_ledger()
    passed = not EXPORTS_PHYSICAL_M_W and not EXPORTS_PHYSICAL_SCHEME_MASSES and not d["exports_physical_M_W"] and not d["physical_W_transport_closed"]
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "exports_physical_M_W": False, "exports_physical_scheme_masses": False}


def check_T_w_finite_part_constants_ledger_still_source_tagged() -> Dict[str, Any]:
    dep = _check_T_w_constants_source_ledger_bank_closure()
    ledger = _constants_ledger()
    records = ledger.records
    passed = _passed(dep) and all(r.provenance_status == "source_tagged_numeric_value_filled" for r in records) and all(not r.consumes_observed_M_W for r in records)
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "upstream": dep.get("status"), "records": [r.symbol_id for r in records]}


def check_T_w_finite_part_next_completion_requirements_explicit() -> Dict[str, Any]:
    requirements = (
        "evaluate delta_alpha_running_component independently",
        "evaluate oblique/fermionic/bosonic/vertex-box finite components",
        "evaluate scheme_conversion_counterterm_component",
        "certify component sum against APF anchor Delta_r target without observed M_W",
        "propagate source correlations and uncertainties",
    )
    passed = len(requirements) == 5 and all("observed M_W" not in r or "without observed M_W" in r for r in requirements)
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "next_requirements": requirements}


def check_T_w_finite_part_ledger_bank_closure() -> Dict[str, Any]:
    deps = [
        check_T_w_finite_part_ledger_status_declared(),
        check_T_w_finite_part_depends_on_v93_symbolic_map(),
        check_T_w_finite_part_component_schema_complete(),
        check_T_w_finite_part_required_components_enumerated(),
        check_T_w_finite_part_anchor_delta_r_target_computed_from_trace_not_observed(),
        check_T_w_finite_part_allowed_inputs_are_v92_plus_trace_anchor(),
        check_T_w_finite_part_no_observed_W_or_residual_inputs(),
        check_T_w_finite_part_components_declared_unevaluated(),
        check_T_w_finite_part_counterterm_component_required_not_filled(),
        check_T_w_finite_part_component_sum_not_certified_yet(),
        check_T_w_finite_part_covariance_and_uncertainty_gate_open(),
        check_T_w_finite_part_completion_gate_remains_locked(),
        check_T_w_finite_part_publication_claim_ladder(),
        check_T_w_finite_part_no_physical_W_export(),
        check_T_w_finite_part_constants_ledger_still_source_tagged(),
        check_T_w_finite_part_next_completion_requirements_explicit(),
    ]
    passed = all(_passed(d) for d in deps)
    return {
        "passed": passed,
        "status": "PASS" if passed else "FAIL",
        "tier": 4,
        "epistemic": W_FINITE_PART_LEDGER_STATUS,
        "dependencies": [str(d.get("status")) for d in deps],
        "ledger": finite_part_ledger(),
        "closed_now": "W Delta_r finite-part component ledger plus APF-anchor Delta_r target",
        "not_closed": "independent finite-part evaluation, counterterm finite parts, component-sum certificate, uncertainty/correlation propagation, physical W export",
        "apf_anchor_delta_r_target_computed": APF_ANCHOR_DELTA_R_TARGET_COMPUTED,
        "independent_finite_parts_evaluated": INDEPENDENT_FINITE_PARTS_EVALUATED,
        "counterterm_finite_parts_evaluated": COUNTERTERM_FINITE_PARTS_EVALUATED,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "W finite-part ledger is ready for independent component evaluation; physical W transport remains open and gated.",
    }

_CHECKS = {
    "T_w_finite_part_ledger_status_declared": check_T_w_finite_part_ledger_status_declared,
    "T_w_finite_part_depends_on_v93_symbolic_map": check_T_w_finite_part_depends_on_v93_symbolic_map,
    "T_w_finite_part_component_schema_complete": check_T_w_finite_part_component_schema_complete,
    "T_w_finite_part_required_components_enumerated": check_T_w_finite_part_required_components_enumerated,
    "T_w_finite_part_anchor_delta_r_target_computed_from_trace_not_observed": check_T_w_finite_part_anchor_delta_r_target_computed_from_trace_not_observed,
    "T_w_finite_part_allowed_inputs_are_v92_plus_trace_anchor": check_T_w_finite_part_allowed_inputs_are_v92_plus_trace_anchor,
    "T_w_finite_part_no_observed_W_or_residual_inputs": check_T_w_finite_part_no_observed_W_or_residual_inputs,
    "T_w_finite_part_components_declared_unevaluated": check_T_w_finite_part_components_declared_unevaluated,
    "T_w_finite_part_counterterm_component_required_not_filled": check_T_w_finite_part_counterterm_component_required_not_filled,
    "T_w_finite_part_component_sum_not_certified_yet": check_T_w_finite_part_component_sum_not_certified_yet,
    "T_w_finite_part_covariance_and_uncertainty_gate_open": check_T_w_finite_part_covariance_and_uncertainty_gate_open,
    "T_w_finite_part_completion_gate_remains_locked": check_T_w_finite_part_completion_gate_remains_locked,
    "T_w_finite_part_publication_claim_ladder": check_T_w_finite_part_publication_claim_ladder,
    "T_w_finite_part_no_physical_W_export": check_T_w_finite_part_no_physical_W_export,
    "T_w_finite_part_constants_ledger_still_source_tagged": check_T_w_finite_part_constants_ledger_still_source_tagged,
    "T_w_finite_part_next_completion_requirements_explicit": check_T_w_finite_part_next_completion_requirements_explicit,
    "T_w_finite_part_ledger_bank_closure": check_T_w_finite_part_ledger_bank_closure,
}


def register(registry: Dict[str, Any]) -> None:
    """Register W_TRACE finite-part ledger checks into the global bank."""
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
        "status": "W_TRACE_FINITE_PART_LEDGER_BANK_PASS" if ok else "W_TRACE_FINITE_PART_LEDGER_BANK_FAIL",
        "bank_registered": True,
        "route_status": W_FINITE_PART_LEDGER_STATUS,
        "route_id": W_ROUTE_ID,
        "apf_anchor_delta_r_target_computed": APF_ANCHOR_DELTA_R_TARGET_COMPUTED,
        "apf_anchor_delta_r_target": f"{apf_anchor_delta_r_target():.17E}",
        "independent_finite_parts_evaluated": INDEPENDENT_FINITE_PARTS_EVALUATED,
        "counterterm_finite_parts_evaluated": COUNTERTERM_FINITE_PARTS_EVALUATED,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "correlation_propagation_evaluated": CORRELATION_PROPAGATION_EVALUATED,
        "uncertainty_protocol_evaluated": UNCERTAINTY_PROTOCOL_EVALUATED,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "component_count": len(FINITE_PART_COMPONENT_ORDER),
        "results": rows,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_all(), indent=2))
