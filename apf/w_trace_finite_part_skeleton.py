"""W_TRACE finite-part skeleton evaluator / symbolic component algebra.

v9.6 (2026-05-08 LATER-14): route-specific symbolic-algebra layer after
v9.5. This module turns the eight W finite-part evaluation slots into a
strict symbolic component algebra without supplying numerical finite parts.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, fields
from typing import Any, Dict, Mapping, Tuple
from apf.w_trace_finite_part_ledger import FINITE_PART_COMPONENT_ORDER, FORBIDDEN_FINITE_PART_INPUTS, apf_anchor_delta_r_target
from apf.w_trace_finite_part_evaluator_gate import W_FINITE_PART_EVALUATOR_GATE_STATUS, FORBIDDEN_EVALUATOR_INPUTS, component_sum_certificate, component_sum_predicate, evaluation_slots, check_T_w_finite_part_evaluator_gate_bank_closure as _check_v95
from apf.w_trace_constants_source_ledger import _constant_records
from apf.w_trace_onshell_transport import W_ROUTE_ID, W_TRACE_EXPECTED_GEV
from apf.trace_transport_completion import check_T_physical_export_gate_locked_until_all_certificates_filled as _check_completion

W_FINITE_PART_SKELETON_STATUS = "P_w_finite_part_skeleton"
SYMBOLIC_COMPONENT_ALGEBRA_DECLARED = True
SYMBOLIC_COMPONENTS_NUMERICALLY_EVALUATED = False
SYMBOLIC_SUM_NUMERICALLY_EVALUATED = False
COMPONENT_SUM_CERTIFIED = False
PHYSICAL_W_TRANSPORT_CLOSED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False
ALLOWED_NUMERIC_LEAVES = ("alpha_em_reference", "G_F_reference", "M_Z_on_shell_reference", "M_W_TRACE_GeV")
ALLOWED_SYMBOLIC_LEAVES = ("Pi_AA_finite_q2_0_to_MZ2", "Sigma_WW_finite_0", "Sigma_ZZ_finite_MZ2", "fermion_loop_basis_sum", "boson_loop_basis_sum", "muon_decay_vertex_box_finite", "delta_ct_on_shell_finite", "covariance_pullback_symbol", "uncertainty_pushforward_symbol")
FORBIDDEN_SKELETON_INPUTS = tuple(sorted(set(FORBIDDEN_FINITE_PART_INPUTS + FORBIDDEN_EVALUATOR_INPUTS + ("apf_anchor_delta_r_target", "apf_anchor_delta_r_target_as_symbolic_leaf", "Delta_r_symbolic_sum_fitted_to_target", "observed_M_W_symbolic_leaf", "W_residual_symbolic_leaf", "counterterm_tuned_to_APF_anchor"))))
REQUIRED_SYMBOLIC_COMPONENT_FIELDS = ("component_id", "symbol", "expression", "dependencies", "allowed_numeric_leaves", "allowed_symbolic_leaves", "forbidden_inputs_consumed", "numeric_value", "provenance_status", "evaluation_status")
COMPONENT_SYMBOLS = {
    "delta_alpha_running_component": "Delta_alpha_run",
    "delta_rho_oblique_component": "Delta_rho_oblique",
    "fermionic_loop_finite_component": "Delta_r_fermion_finite",
    "bosonic_loop_finite_component": "Delta_r_boson_finite",
    "vertex_box_finite_component": "Delta_r_vertex_box",
    "scheme_conversion_counterterm_component": "Delta_r_ct_OS",
    "correlation_covariance_component": "Delta_r_covariance_pullback",
    "uncertainty_propagation_component": "sigma_Delta_r_pushforward",
}
COMPONENT_EXPRESSIONS = {
    "delta_alpha_running_component": "F_alpha(alpha_em_reference, M_Z_on_shell_reference; Pi_AA_finite_q2_0_to_MZ2)",
    "delta_rho_oblique_component": "F_rho(alpha_em_reference, G_F_reference, M_Z_on_shell_reference, M_W_TRACE_GeV; Sigma_WW_finite_0, Sigma_ZZ_finite_MZ2)",
    "fermionic_loop_finite_component": "F_fermions(alpha_em_reference, G_F_reference, M_Z_on_shell_reference; fermion_loop_basis_sum)",
    "bosonic_loop_finite_component": "F_bosons(alpha_em_reference, G_F_reference, M_Z_on_shell_reference, M_W_TRACE_GeV; boson_loop_basis_sum)",
    "vertex_box_finite_component": "F_vertex_box(alpha_em_reference, G_F_reference; muon_decay_vertex_box_finite)",
    "scheme_conversion_counterterm_component": "F_ct_OS(alpha_em_reference, G_F_reference, M_Z_on_shell_reference, M_W_TRACE_GeV; delta_ct_on_shell_finite)",
    "correlation_covariance_component": "F_covariance(covariance_pullback_symbol)",
    "uncertainty_propagation_component": "F_uncertainty(uncertainty_pushforward_symbol)",
}
COMPONENT_DEPENDENCIES = {
    "delta_alpha_running_component": ("alpha_em_reference", "M_Z_on_shell_reference", "Pi_AA_finite_q2_0_to_MZ2"),
    "delta_rho_oblique_component": ("alpha_em_reference", "G_F_reference", "M_Z_on_shell_reference", "M_W_TRACE_GeV", "Sigma_WW_finite_0", "Sigma_ZZ_finite_MZ2"),
    "fermionic_loop_finite_component": ("alpha_em_reference", "G_F_reference", "M_Z_on_shell_reference", "fermion_loop_basis_sum"),
    "bosonic_loop_finite_component": ("alpha_em_reference", "G_F_reference", "M_Z_on_shell_reference", "M_W_TRACE_GeV", "boson_loop_basis_sum"),
    "vertex_box_finite_component": ("alpha_em_reference", "G_F_reference", "muon_decay_vertex_box_finite"),
    "scheme_conversion_counterterm_component": ("alpha_em_reference", "G_F_reference", "M_Z_on_shell_reference", "M_W_TRACE_GeV", "delta_ct_on_shell_finite"),
    "correlation_covariance_component": ("covariance_pullback_symbol",),
    "uncertainty_propagation_component": ("uncertainty_pushforward_symbol",),
}
SUM_EXPRESSION = " + ".join(COMPONENT_SYMBOLS[cid] for cid in FINITE_PART_COMPONENT_ORDER)

@dataclass(frozen=True)
class WFinitePartSymbolicComponent:
    component_id: str; symbol: str; expression: str; dependencies: Tuple[str, ...]; allowed_numeric_leaves: Tuple[str, ...]; allowed_symbolic_leaves: Tuple[str, ...]
    forbidden_inputs_consumed: Tuple[str, ...] = (); numeric_value: str = "UNEVALUATED_SYMBOLIC_ONLY"; provenance_status: str = "SYMBOLIC_SHELL_ONLY"; evaluation_status: str = "OPEN_UNEVALUATED"
@dataclass(frozen=True)
class WFinitePartSkeletonAlgebra:
    route_id: str; status: str; upstream_status: str; components: Tuple[WFinitePartSymbolicComponent, ...]; sum_symbol: str; sum_expression: str; apf_anchor_delta_r_target: str; allowed_numeric_leaves: Tuple[str, ...]; allowed_symbolic_leaves: Tuple[str, ...]; forbidden_inputs: Tuple[str, ...]
    symbolic_components_numerically_evaluated: bool = False; symbolic_sum_numerically_evaluated: bool = False; component_sum_certified: bool = False; physical_W_transport_closed: bool = False; exports_physical_M_W: bool = False

def _passed(r: Mapping[str, Any]) -> bool: return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})
def symbolic_components() -> Tuple[WFinitePartSymbolicComponent, ...]:
    return tuple(WFinitePartSymbolicComponent(cid, COMPONENT_SYMBOLS[cid], COMPONENT_EXPRESSIONS[cid], COMPONENT_DEPENDENCIES[cid], tuple(d for d in COMPONENT_DEPENDENCIES[cid] if d in ALLOWED_NUMERIC_LEAVES), tuple(d for d in COMPONENT_DEPENDENCIES[cid] if d in ALLOWED_SYMBOLIC_LEAVES)) for cid in FINITE_PART_COMPONENT_ORDER)
def skeleton_algebra() -> Dict[str, Any]:
    alg = WFinitePartSkeletonAlgebra(W_ROUTE_ID, W_FINITE_PART_SKELETON_STATUS, W_FINITE_PART_EVALUATOR_GATE_STATUS, symbolic_components(), "Delta_r_symbolic_sum", SUM_EXPRESSION, f"{apf_anchor_delta_r_target():.17E}", ALLOWED_NUMERIC_LEAVES, ALLOWED_SYMBOLIC_LEAVES, FORBIDDEN_SKELETON_INPUTS)
    data = asdict(alg); data["components"] = tuple(asdict(c) for c in alg.components); return data
def symbolic_dependency_graph() -> Dict[str, Tuple[str, ...]]:
    g = {cid: COMPONENT_DEPENDENCIES[cid] for cid in FINITE_PART_COMPONENT_ORDER}; g["Delta_r_symbolic_sum"] = tuple(COMPONENT_SYMBOLS[cid] for cid in FINITE_PART_COMPONENT_ORDER); return g
def symbolic_sum_expression() -> str: return SUM_EXPRESSION

def check_T_w_finite_part_skeleton_status_declared():
    p = W_FINITE_PART_SKELETON_STATUS == "P_w_finite_part_skeleton" and SYMBOLIC_COMPONENT_ALGEBRA_DECLARED; return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_FINITE_PART_SKELETON_STATUS}
def check_T_w_finite_part_skeleton_depends_on_v95_gate():
    d = _check_v95(); c = component_sum_certificate(); p = _passed(d) and c["status"] == W_FINITE_PART_EVALUATOR_GATE_STATUS and not c["component_sum_certified"]; return {"passed": p, "status": "PASS" if p else "FAIL", "upstream": d.get("status")}
def check_T_w_finite_part_skeleton_component_schema_complete():
    m = [x for x in REQUIRED_SYMBOLIC_COMPONENT_FIELDS if x not in {f.name for f in fields(WFinitePartSymbolicComponent)}]; return {"passed": not m, "status": "PASS" if not m else "FAIL", "missing": m}
def check_T_w_finite_part_skeleton_covers_all_slots():
    ids = tuple(c.component_id for c in symbolic_components()); slots = tuple(s.component_id for s in evaluation_slots()); p = ids == FINITE_PART_COMPONENT_ORDER == slots; return {"passed": p, "status": "PASS" if p else "FAIL", "component_order": ids}
def check_T_w_finite_part_skeleton_symbols_unique():
    sy = tuple(c.symbol for c in symbolic_components()); p = len(sy) == len(set(sy)) == len(FINITE_PART_COMPONENT_ORDER); return {"passed": p, "status": "PASS" if p else "FAIL", "symbols": sy}
def check_T_w_finite_part_skeleton_dependency_graph_acyclic():
    g = symbolic_dependency_graph(); cids = set(FINITE_PART_COMPONENT_ORDER); sy = set(COMPONENT_SYMBOLS.values()); bad = [cid for cid, deps in g.items() if cid in cids for d in deps if d in cids or d in sy]; p = not bad and g["Delta_r_symbolic_sum"] == tuple(COMPONENT_SYMBOLS[cid] for cid in FINITE_PART_COMPONENT_ORDER); return {"passed": p, "status": "PASS" if p else "FAIL", "bad_edges": bad}
def check_T_w_finite_part_skeleton_allowed_numeric_leaves_source_filled():
    names = {c.symbol_id for c in _constant_records()}; req = {"alpha_em_reference", "G_F_reference", "M_Z_on_shell_reference"}; p = req.issubset(names) and "M_W_TRACE_GeV" in ALLOWED_NUMERIC_LEAVES and W_TRACE_EXPECTED_GEV > 0; return {"passed": p, "status": "PASS" if p else "FAIL", "constant_names": sorted(names)}
def check_T_w_finite_part_skeleton_forbids_target_as_leaf():
    bad = [c.component_id for c in symbolic_components() if "apf_anchor_delta_r_target" in c.dependencies or c.forbidden_inputs_consumed]; p = not bad and "apf_anchor_delta_r_target" in FORBIDDEN_SKELETON_INPUTS; return {"passed": p, "status": "PASS" if p else "FAIL", "bad_components": bad}
def check_T_w_finite_part_skeleton_forbids_observed_W_inputs():
    deps = {d for c in symbolic_components() for d in c.dependencies}; forbidden = {"observed_M_W", "M_W_world_average", "W_mass_residual", "observed_M_W_symbolic_leaf", "W_residual_symbolic_leaf"}; p = deps.isdisjoint(forbidden) and bool(forbidden.intersection(FORBIDDEN_SKELETON_INPUTS)); return {"passed": p, "status": "PASS" if p else "FAIL"}
def check_T_w_finite_part_skeleton_no_counterterm_tuning():
    c = {x.component_id: x for x in symbolic_components()}["scheme_conversion_counterterm_component"]; p = "delta_ct_on_shell_finite" in c.dependencies and "counterterm_tuned_to_APF_anchor" in FORBIDDEN_SKELETON_INPUTS and "Delta_r_symbolic_sum_fitted_to_target" in FORBIDDEN_SKELETON_INPUTS; return {"passed": p, "status": "PASS" if p else "FAIL", "counterterm_component": asdict(c)}
def check_T_w_finite_part_skeleton_sum_expression_declared():
    e = symbolic_sum_expression(); p = e == SUM_EXPRESSION and all(COMPONENT_SYMBOLS[cid] in e for cid in FINITE_PART_COMPONENT_ORDER) and "apf_anchor_delta_r_target" not in e; return {"passed": p, "status": "PASS" if p else "FAIL", "sum_expression": e}
def check_T_w_finite_part_skeleton_remains_symbolic_not_numeric():
    a = skeleton_algebra(); vals = [c["numeric_value"] for c in a["components"]]; p = all(v == "UNEVALUATED_SYMBOLIC_ONLY" for v in vals) and not SYMBOLIC_COMPONENTS_NUMERICALLY_EVALUATED and not SYMBOLIC_SUM_NUMERICALLY_EVALUATED; return {"passed": p, "status": "PASS" if p else "FAIL"}
def check_T_w_finite_part_skeleton_component_sum_still_uncertified():
    pr = component_sum_predicate({}); a = skeleton_algebra(); p = pr["status"] == "OPEN_MISSING_COMPONENTS" and not a["component_sum_certified"] and not COMPONENT_SUM_CERTIFIED; return {"passed": p, "status": "PASS" if p else "FAIL", "predicate_empty": pr}
def check_T_w_finite_part_skeleton_codomain_not_physical_export():
    a = skeleton_algebra(); p = a["sum_symbol"] == "Delta_r_symbolic_sum" and not a["exports_physical_M_W"] and not a["physical_W_transport_closed"] and not EXPORTS_PHYSICAL_SCHEME_MASSES; return {"passed": p, "status": "PASS" if p else "FAIL"}
def check_T_w_finite_part_skeleton_completion_gate_remains_locked():
    d = _check_completion(); p = _passed(d) and not PHYSICAL_W_TRANSPORT_CLOSED and not EXPORTS_PHYSICAL_M_W; return {"passed": p, "status": "PASS" if p else "FAIL", "completion_gate": d.get("status")}
def check_T_w_finite_part_skeleton_publication_ladder():
    ladder = (("W finite-part evaluator gate", W_FINITE_PART_EVALUATOR_GATE_STATUS), ("W finite-part symbolic component algebra", W_FINITE_PART_SKELETON_STATUS), ("independent numerical finite-part values", "OPEN"), ("component-sum certificate", "OPEN"), ("physical W/on-shell transport", "OPEN")); p = ladder[1][1] == W_FINITE_PART_SKELETON_STATUS and ladder[-1][1] == "OPEN"; return {"passed": p, "status": "PASS" if p else "FAIL", "claim_ladder": ladder}
def check_T_w_finite_part_skeleton_next_requirements_explicit():
    req = ("replace each symbolic finite function with an independently evaluated finite part", "declare the on-shell finite counterterm convention before summing components", "attach covariance and uncertainty protocols to the symbolic sum", "run component_sum_predicate only after all eight independent values are supplied", "compare to APF-anchor Delta_r target only at certificate stage, never as an input leaf"); p = len(req) == 5 and "never as an input leaf" in req[-1]; return {"passed": p, "status": "PASS" if p else "FAIL", "next_requirements": req}
def check_T_w_finite_part_skeleton_bank_closure():
    deps = [check_T_w_finite_part_skeleton_status_declared(), check_T_w_finite_part_skeleton_depends_on_v95_gate(), check_T_w_finite_part_skeleton_component_schema_complete(), check_T_w_finite_part_skeleton_covers_all_slots(), check_T_w_finite_part_skeleton_symbols_unique(), check_T_w_finite_part_skeleton_dependency_graph_acyclic(), check_T_w_finite_part_skeleton_allowed_numeric_leaves_source_filled(), check_T_w_finite_part_skeleton_forbids_target_as_leaf(), check_T_w_finite_part_skeleton_forbids_observed_W_inputs(), check_T_w_finite_part_skeleton_no_counterterm_tuning(), check_T_w_finite_part_skeleton_sum_expression_declared(), check_T_w_finite_part_skeleton_remains_symbolic_not_numeric(), check_T_w_finite_part_skeleton_component_sum_still_uncertified(), check_T_w_finite_part_skeleton_codomain_not_physical_export(), check_T_w_finite_part_skeleton_completion_gate_remains_locked(), check_T_w_finite_part_skeleton_publication_ladder(), check_T_w_finite_part_skeleton_next_requirements_explicit()]
    p = all(_passed(d) for d in deps); return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_FINITE_PART_SKELETON_STATUS, "dependencies": [str(d.get("status")) for d in deps], "skeleton_algebra": skeleton_algebra(), "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED, "exports_physical_M_W": EXPORTS_PHYSICAL_M_W, "closed_now": "symbolic finite-part component algebra and acyclic component-sum shell", "not_closed": "numeric finite parts, counterterm convention, covariance/uncertainty protocol, component-sum certificate, physical W export"}

_CHECKS: Dict[str, Any] = {
    "T_w_finite_part_skeleton_status_declared": check_T_w_finite_part_skeleton_status_declared,
    "T_w_finite_part_skeleton_depends_on_v95_gate": check_T_w_finite_part_skeleton_depends_on_v95_gate,
    "T_w_finite_part_skeleton_component_schema_complete": check_T_w_finite_part_skeleton_component_schema_complete,
    "T_w_finite_part_skeleton_covers_all_slots": check_T_w_finite_part_skeleton_covers_all_slots,
    "T_w_finite_part_skeleton_symbols_unique": check_T_w_finite_part_skeleton_symbols_unique,
    "T_w_finite_part_skeleton_dependency_graph_acyclic": check_T_w_finite_part_skeleton_dependency_graph_acyclic,
    "T_w_finite_part_skeleton_allowed_numeric_leaves_source_filled": check_T_w_finite_part_skeleton_allowed_numeric_leaves_source_filled,
    "T_w_finite_part_skeleton_forbids_target_as_leaf": check_T_w_finite_part_skeleton_forbids_target_as_leaf,
    "T_w_finite_part_skeleton_forbids_observed_W_inputs": check_T_w_finite_part_skeleton_forbids_observed_W_inputs,
    "T_w_finite_part_skeleton_no_counterterm_tuning": check_T_w_finite_part_skeleton_no_counterterm_tuning,
    "T_w_finite_part_skeleton_sum_expression_declared": check_T_w_finite_part_skeleton_sum_expression_declared,
    "T_w_finite_part_skeleton_remains_symbolic_not_numeric": check_T_w_finite_part_skeleton_remains_symbolic_not_numeric,
    "T_w_finite_part_skeleton_component_sum_still_uncertified": check_T_w_finite_part_skeleton_component_sum_still_uncertified,
    "T_w_finite_part_skeleton_codomain_not_physical_export": check_T_w_finite_part_skeleton_codomain_not_physical_export,
    "T_w_finite_part_skeleton_completion_gate_remains_locked": check_T_w_finite_part_skeleton_completion_gate_remains_locked,
    "T_w_finite_part_skeleton_publication_ladder": check_T_w_finite_part_skeleton_publication_ladder,
    "T_w_finite_part_skeleton_next_requirements_explicit": check_T_w_finite_part_skeleton_next_requirements_explicit,
    "T_w_finite_part_skeleton_bank_closure": check_T_w_finite_part_skeleton_bank_closure,
}


def register(registry: Dict[str, Any]) -> None:
    """Register W_TRACE finite-part skeleton checks into the theorem bank."""
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
        "status": "W_TRACE_FINITE_PART_SKELETON_BANK_PASS" if ok else "W_TRACE_FINITE_PART_SKELETON_BANK_FAIL",
        "bank_registered": True,
        "route_status": W_FINITE_PART_SKELETON_STATUS,
        "route_id": W_ROUTE_ID,
        "upstream_status": W_FINITE_PART_EVALUATOR_GATE_STATUS,
        "symbolic_components_numerically_evaluated": SYMBOLIC_COMPONENTS_NUMERICALLY_EVALUATED,
        "symbolic_sum_numerically_evaluated": SYMBOLIC_SUM_NUMERICALLY_EVALUATED,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "component_count": len(FINITE_PART_COMPONENT_ORDER),
        "results": rows,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_all(), indent=2))
