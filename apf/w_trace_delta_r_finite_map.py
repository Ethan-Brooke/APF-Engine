"""W_TRACE Delta_r / finite-correction symbolic-map bank.

v9.3 (2026-05-08 LATER-11): route-specific finite-correction interface after
v9.2 constants-source ledger.  This module banks the symbolic on-shell
Delta_r / finite-counterterm map needed to transport W_TRACE toward an
on-shell W comparison, without evaluating the finite map and without exporting
an observed or predicted physical W mass.

Closed here:
    - The W on-shell finite-correction map has a typed symbolic contract.
    - The allowed inputs are exactly the v9.2 non-W constants ledger plus the
      local W_TRACE anchor and declared finite-map slots.
    - Delta_r is decomposed into named unevaluated slots rather than a fitted
      residual.
    - Counterterm finite parts, correlations, and uncertainty propagation remain
      named blockers for physical export.

Not closed here:
    - Delta_r is not numerically evaluated.
    - The on-shell finite conversion is not solved for a physical M_W.
    - No physical W mass or physical scheme mass vector is exported.

Status discipline:
    - upstream W constants-source ledger: [P_w_constants_source_ledger]
    - this module: [P_w_delta_r_symbolic_map]
    - physical W/on-shell transport remains OPEN.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, fields
from typing import Any, Dict, Mapping, Tuple

from apf.w_trace_constants_source_ledger import (
    W_CONSTANTS_SOURCE_LEDGER_STATUS,
    CONSTANTS_SOURCE_LEDGER_FILLED,
    NUMERICAL_EW_CONSTANTS_FILLED,
    DELTA_R_EVALUATED as UPSTREAM_DELTA_R_EVALUATED,
    COUNTERTERM_FINITE_PARTS_EVALUATED as UPSTREAM_COUNTERTERM_FINITE_PARTS_EVALUATED,
    CORRELATION_PROPAGATION_EVALUATED as UPSTREAM_CORRELATION_PROPAGATION_EVALUATED,
    UNCERTAINTY_PROTOCOL_EVALUATED as UPSTREAM_UNCERTAINTY_PROTOCOL_EVALUATED,
    FORBIDDEN_CONSTANT_INPUTS,
    _ledger as _filled_constants_ledger,
    check_T_w_constants_source_ledger_bank_closure as _check_T_w_constants_source_ledger_bank_closure,
    check_T_w_constants_completion_gate_remains_locked as _check_T_w_constants_completion_gate_remains_locked,
)
from apf.w_trace_onshell_transport import W_ROUTE_ID, W_TRACE_EXPECTED_GEV
from apf.w_trace_input_basis_ledger import SELECTED_W_INPUT_BASIS
from apf.trace_transport_completion import (
    check_T_physical_export_gate_locked_until_all_certificates_filled as _check_T_physical_export_gate_locked_until_all_certificates_filled,
)

W_DELTA_R_SYMBOLIC_MAP_STATUS = "P_w_delta_r_symbolic_map"
DELTA_R_SYMBOLIC_MAP_DECLARED = True
DELTA_R_NUMERICALLY_EVALUATED = False
FINITE_COUNTERTERMS_EVALUATED = False
CORRELATION_PROPAGATION_EVALUATED = False
UNCERTAINTY_PROTOCOL_EVALUATED = False
PHYSICAL_W_TRANSPORT_CLOSED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

ON_SHELL_RELATION_TEMPLATE = (
    "M_W^2 * (1 - M_W^2/M_Z^2) = "
    "pi*alpha_em/(sqrt(2)*G_F) * 1/(1 - Delta_r_symbolic)"
)

DELTA_R_SLOT_IDS: Tuple[str, ...] = (
    "delta_alpha_running_slot",
    "delta_rho_or_oblique_slot",
    "vertex_box_finite_slot",
    "bosonic_loop_finite_slot",
    "fermionic_loop_finite_slot",
    "scheme_conversion_counterterm_slot",
)

REQUIRED_MAP_FIELDS: Tuple[str, ...] = (
    "route_id",
    "status",
    "input_basis",
    "allowed_numeric_inputs",
    "local_trace_anchor",
    "relation_template",
    "delta_r_slots",
    "counterterm_slots",
    "forbidden_inputs",
    "map_evaluated",
    "exports_physical_M_W",
    "physical_W_transport_closed",
)

FORBIDDEN_DELTA_R_INPUTS: Tuple[str, ...] = tuple(sorted(set(FORBIDDEN_CONSTANT_INPUTS + (
    "observed_M_W",
    "M_W_world_average",
    "W_mass_residual",
    "Delta_r_fit_to_observed_M_W",
    "finite_counterterm_chosen_to_match_M_W",
    "identity_W_TRACE_to_on_shell_M_W",
))))


@dataclass(frozen=True)
class WDeltaRFiniteMap:
    """Symbolic finite-correction map for the W_TRACE on-shell route."""

    route_id: str
    status: str
    input_basis: str
    allowed_numeric_inputs: Tuple[str, ...]
    local_trace_anchor: str
    relation_template: str
    delta_r_slots: Tuple[str, ...]
    counterterm_slots: Tuple[str, ...]
    forbidden_inputs: Tuple[str, ...]
    map_evaluated: bool = False
    delta_r_numerically_evaluated: bool = False
    finite_counterterms_evaluated: bool = False
    correlation_propagation_evaluated: bool = False
    uncertainty_protocol_evaluated: bool = False
    exports_physical_M_W: bool = False
    physical_W_transport_closed: bool = False


def _passed(result: Mapping[str, Any]) -> bool:
    return bool(result.get("passed") is True or str(result.get("status", "")).upper() in {"PASS", "P"})


def _constant_symbol_ids() -> Tuple[str, ...]:
    ledger = _filled_constants_ledger()
    return tuple(record.symbol_id for record in ledger.records)


def symbolic_delta_r_map() -> Dict[str, Any]:
    """Return the v9.3 symbolic finite-map contract as a serializable dict."""
    m = WDeltaRFiniteMap(
        route_id=W_ROUTE_ID,
        status=W_DELTA_R_SYMBOLIC_MAP_STATUS,
        input_basis=SELECTED_W_INPUT_BASIS,
        allowed_numeric_inputs=_constant_symbol_ids(),
        local_trace_anchor=f"M_W_TRACE_GeV={W_TRACE_EXPECTED_GEV}",
        relation_template=ON_SHELL_RELATION_TEMPLATE,
        delta_r_slots=DELTA_R_SLOT_IDS,
        counterterm_slots=("scheme_conversion_counterterm_slot", "finite_part_ledger_slot"),
        forbidden_inputs=FORBIDDEN_DELTA_R_INPUTS,
        map_evaluated=False,
        delta_r_numerically_evaluated=False,
        finite_counterterms_evaluated=False,
        correlation_propagation_evaluated=False,
        uncertainty_protocol_evaluated=False,
        exports_physical_M_W=False,
        physical_W_transport_closed=False,
    )
    return asdict(m)


def check_T_w_delta_r_symbolic_map_status_declared() -> Dict[str, Any]:
    return {
        "passed": W_DELTA_R_SYMBOLIC_MAP_STATUS == "P_w_delta_r_symbolic_map" and DELTA_R_SYMBOLIC_MAP_DECLARED,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_DELTA_R_SYMBOLIC_MAP_STATUS,
        "closed_now": "symbolic Delta_r / finite-correction map contract declared",
        "not_closed": "numeric Delta_r and physical W export",
    }


def check_T_w_delta_r_map_schema_complete() -> Dict[str, Any]:
    field_names = {f.name for f in fields(WDeltaRFiniteMap)}
    missing = [f for f in REQUIRED_MAP_FIELDS if f not in field_names]
    return {"passed": not missing, "status": "PASS" if not missing else "FAIL", "missing": missing, "schema": sorted(field_names)}


def check_T_w_delta_r_depends_on_v92_constants_ledger() -> Dict[str, Any]:
    dep = _check_T_w_constants_source_ledger_bank_closure()
    symbols = set(_constant_symbol_ids())
    required = {"alpha_em_reference", "G_F_reference", "M_Z_on_shell_reference"}
    passed = _passed(dep) and W_CONSTANTS_SOURCE_LEDGER_STATUS == "P_w_constants_source_ledger" and CONSTANTS_SOURCE_LEDGER_FILLED and NUMERICAL_EW_CONSTANTS_FILLED and required == symbols
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "upstream": dep.get("status"), "symbols": sorted(symbols)}


def check_T_w_delta_r_relation_template_on_shell_form() -> Dict[str, Any]:
    template = symbolic_delta_r_map()["relation_template"]
    tokens = ("M_W^2", "M_Z^2", "alpha_em", "G_F", "Delta_r_symbolic")
    passed = all(t in template for t in tokens) and "observed" not in template.lower()
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "relation_template": template}


def check_T_w_delta_r_slots_decomposed_not_fit_residual() -> Dict[str, Any]:
    slots = set(symbolic_delta_r_map()["delta_r_slots"])
    forbidden = {"Delta_r_fit_to_observed_M_W", "W_mass_residual"}
    passed = len(slots) >= 5 and not (slots & forbidden) and "delta_alpha_running_slot" in slots and "scheme_conversion_counterterm_slot" in slots
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "delta_r_slots": sorted(slots)}


def check_T_w_delta_r_counterterm_slots_required_unevaluated() -> Dict[str, Any]:
    m = symbolic_delta_r_map()
    slots = set(m["counterterm_slots"])
    passed = "finite_part_ledger_slot" in slots and "scheme_conversion_counterterm_slot" in slots and not m["finite_counterterms_evaluated"] and not FINITE_COUNTERTERMS_EVALUATED and not UPSTREAM_COUNTERTERM_FINITE_PARTS_EVALUATED
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "counterterm_slots": sorted(slots), "finite_counterterms_evaluated": False}


def check_T_w_delta_r_allowed_inputs_are_non_W_plus_trace_anchor() -> Dict[str, Any]:
    m = symbolic_delta_r_map()
    allowed = set(m["allowed_numeric_inputs"])
    forbidden_hits = allowed & set(FORBIDDEN_DELTA_R_INPUTS)
    passed = allowed == {"alpha_em_reference", "G_F_reference", "M_Z_on_shell_reference"} and not forbidden_hits and m["local_trace_anchor"].startswith("M_W_TRACE_GeV=")
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "allowed_numeric_inputs": sorted(allowed), "forbidden_hits": sorted(forbidden_hits), "local_trace_anchor": m["local_trace_anchor"]}


def check_T_w_delta_r_forbidden_target_observables_absent() -> Dict[str, Any]:
    m = symbolic_delta_r_map()
    serialized = repr((m["allowed_numeric_inputs"], m["relation_template"], m["delta_r_slots"], m["counterterm_slots"]))
    bad_terms = ("world_average", "CDF", "ATLAS", "CMS", "LEP_W", "observed_M_W", "W_mass_residual", "fit_to_observed")
    hits = [term for term in bad_terms if term in serialized]
    passed = not hits and "observed_M_W" in m["forbidden_inputs"] and "Delta_r_fit_to_observed_M_W" in m["forbidden_inputs"]
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "hits": hits, "forbidden_inputs_sample": m["forbidden_inputs"][:8]}


def check_T_w_delta_r_map_not_numerically_evaluated() -> Dict[str, Any]:
    m = symbolic_delta_r_map()
    passed = not m["map_evaluated"] and not m["delta_r_numerically_evaluated"] and not DELTA_R_NUMERICALLY_EVALUATED and not UPSTREAM_DELTA_R_EVALUATED
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "map_evaluated": m["map_evaluated"], "delta_r_numerically_evaluated": m["delta_r_numerically_evaluated"]}


def check_T_w_delta_r_preserves_W_TRACE_anchor_without_identity_export() -> Dict[str, Any]:
    m = symbolic_delta_r_map()
    passed = str(W_TRACE_EXPECTED_GEV) in m["local_trace_anchor"] and "identity_W_TRACE_to_on_shell_M_W" in m["forbidden_inputs"] and not m["exports_physical_M_W"]
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "local_trace_anchor": m["local_trace_anchor"], "identity_route_forbidden": "identity_W_TRACE_to_on_shell_M_W" in m["forbidden_inputs"]}


def check_T_w_delta_r_correlation_and_uncertainty_still_open() -> Dict[str, Any]:
    m = symbolic_delta_r_map()
    passed = not m["correlation_propagation_evaluated"] and not m["uncertainty_protocol_evaluated"] and not UPSTREAM_CORRELATION_PROPAGATION_EVALUATED and not UPSTREAM_UNCERTAINTY_PROTOCOL_EVALUATED
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "correlation_propagation_evaluated": False, "uncertainty_protocol_evaluated": False}


def check_T_w_delta_r_completion_gate_remains_locked() -> Dict[str, Any]:
    dep1 = _check_T_w_constants_completion_gate_remains_locked()
    dep2 = _check_T_physical_export_gate_locked_until_all_certificates_filled()
    m = symbolic_delta_r_map()
    passed = _passed(dep1) and _passed(dep2) and not m["physical_W_transport_closed"] and not m["exports_physical_M_W"]
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "dependencies": [dep1.get("status"), dep2.get("status")], "physical_W_transport_closed": False}


def check_T_w_delta_r_publication_claim_ladder() -> Dict[str, Any]:
    ladder = (
        ("W_TRACE local anchor", "P_local"),
        ("W route contract", "P_w_trace_contract"),
        ("W input-basis ledger", "P_w_input_basis_ledger"),
        ("W constants-source ledger", "P_w_constants_source_ledger"),
        ("W Delta_r symbolic map", W_DELTA_R_SYMBOLIC_MAP_STATUS),
        ("physical W/on-shell transport", "OPEN"),
    )
    passed = ladder[-1][1] == "OPEN" and ladder[-2][1] == W_DELTA_R_SYMBOLIC_MAP_STATUS
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "claim_ladder": ladder}


def check_T_w_delta_r_no_physical_scheme_mass_export() -> Dict[str, Any]:
    m = symbolic_delta_r_map()
    passed = not EXPORTS_PHYSICAL_SCHEME_MASSES and not EXPORTS_PHYSICAL_M_W and not PHYSICAL_W_TRANSPORT_CLOSED and not m["exports_physical_M_W"]
    return {"passed": passed, "status": "PASS" if passed else "FAIL", "exports_physical_scheme_masses": False, "exports_physical_M_W": False}


def check_T_w_delta_r_symbolic_map_bank_closure() -> Dict[str, Any]:
    deps = [
        check_T_w_delta_r_symbolic_map_status_declared(),
        check_T_w_delta_r_map_schema_complete(),
        check_T_w_delta_r_depends_on_v92_constants_ledger(),
        check_T_w_delta_r_relation_template_on_shell_form(),
        check_T_w_delta_r_slots_decomposed_not_fit_residual(),
        check_T_w_delta_r_counterterm_slots_required_unevaluated(),
        check_T_w_delta_r_allowed_inputs_are_non_W_plus_trace_anchor(),
        check_T_w_delta_r_forbidden_target_observables_absent(),
        check_T_w_delta_r_map_not_numerically_evaluated(),
        check_T_w_delta_r_preserves_W_TRACE_anchor_without_identity_export(),
        check_T_w_delta_r_correlation_and_uncertainty_still_open(),
        check_T_w_delta_r_completion_gate_remains_locked(),
        check_T_w_delta_r_publication_claim_ladder(),
        check_T_w_delta_r_no_physical_scheme_mass_export(),
    ]
    passed = all(_passed(dep) for dep in deps)
    return {
        "passed": passed,
        "status": "PASS" if passed else "FAIL",
        "tier": 4,
        "epistemic": W_DELTA_R_SYMBOLIC_MAP_STATUS,
        "dependencies": [str(dep.get("status")) for dep in deps],
        "map": symbolic_delta_r_map(),
        "closed_now": "symbolic W on-shell Delta_r / finite-correction map contract",
        "not_closed": "numeric Delta_r, finite counterterms, covariance/uncertainty propagation, physical W export",
        "delta_r_symbolic_map_declared": DELTA_R_SYMBOLIC_MAP_DECLARED,
        "delta_r_numerically_evaluated": DELTA_R_NUMERICALLY_EVALUATED,
        "finite_counterterms_evaluated": FINITE_COUNTERTERMS_EVALUATED,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "W Delta_r finite map is typed and symbolic; physical W transport remains open and gated.",
    }


_CHECKS = {
    "T_w_delta_r_symbolic_map_status_declared": check_T_w_delta_r_symbolic_map_status_declared,
    "T_w_delta_r_map_schema_complete": check_T_w_delta_r_map_schema_complete,
    "T_w_delta_r_depends_on_v92_constants_ledger": check_T_w_delta_r_depends_on_v92_constants_ledger,
    "T_w_delta_r_relation_template_on_shell_form": check_T_w_delta_r_relation_template_on_shell_form,
    "T_w_delta_r_slots_decomposed_not_fit_residual": check_T_w_delta_r_slots_decomposed_not_fit_residual,
    "T_w_delta_r_counterterm_slots_required_unevaluated": check_T_w_delta_r_counterterm_slots_required_unevaluated,
    "T_w_delta_r_allowed_inputs_are_non_W_plus_trace_anchor": check_T_w_delta_r_allowed_inputs_are_non_W_plus_trace_anchor,
    "T_w_delta_r_forbidden_target_observables_absent": check_T_w_delta_r_forbidden_target_observables_absent,
    "T_w_delta_r_map_not_numerically_evaluated": check_T_w_delta_r_map_not_numerically_evaluated,
    "T_w_delta_r_preserves_W_TRACE_anchor_without_identity_export": check_T_w_delta_r_preserves_W_TRACE_anchor_without_identity_export,
    "T_w_delta_r_correlation_and_uncertainty_still_open": check_T_w_delta_r_correlation_and_uncertainty_still_open,
    "T_w_delta_r_completion_gate_remains_locked": check_T_w_delta_r_completion_gate_remains_locked,
    "T_w_delta_r_publication_claim_ladder": check_T_w_delta_r_publication_claim_ladder,
    "T_w_delta_r_no_physical_scheme_mass_export": check_T_w_delta_r_no_physical_scheme_mass_export,
    "T_w_delta_r_symbolic_map_bank_closure": check_T_w_delta_r_symbolic_map_bank_closure,
}


def register(registry: Dict[str, Any]) -> None:
    """Register W_TRACE Delta_r symbolic-map checks into the global bank."""
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
        "status": "W_TRACE_DELTA_R_SYMBOLIC_MAP_BANK_PASS" if ok else "W_TRACE_DELTA_R_SYMBOLIC_MAP_BANK_FAIL",
        "bank_registered": True,
        "route_status": W_DELTA_R_SYMBOLIC_MAP_STATUS,
        "route_id": W_ROUTE_ID,
        "delta_r_symbolic_map_declared": DELTA_R_SYMBOLIC_MAP_DECLARED,
        "delta_r_numerically_evaluated": DELTA_R_NUMERICALLY_EVALUATED,
        "finite_counterterms_evaluated": FINITE_COUNTERTERMS_EVALUATED,
        "correlation_propagation_evaluated": CORRELATION_PROPAGATION_EVALUATED,
        "uncertainty_protocol_evaluated": UNCERTAINTY_PROTOCOL_EVALUATED,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "results": rows,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_all(), indent=2))
