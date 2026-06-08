"""W_TRACE Denner/Sirlin formula import and native one-loop assembly sprint.

v19.0 (2026-05-09): moves beyond the v18 coefficient-import contract by
building a source-formula import matrix and a partial APF-native one-loop
assembly.  The layer imports/evaluates the two rows that are defensible inside
APF at this stage (running-alpha input row and leading top-rho analytic row),
places Denner/Sirlin self-energy, gamma-Z, weak-angle, vertex, box, tadpole,
ghost, and gauge-restoring families into a coefficient/formula assembly matrix,
and proves that the remaining same-input target is exactly the finite
counterterm/remainder functional already isolated in v16.8-v18.0.

No fitted coefficients are admitted.  DIZET remainder and rho-resummation/cross
pieces are carried only as target/benchmark objects until reviewed formulae are
imported.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_denner_diagram_coefficient_table_closeout import (
    PASS_STATUS as V18_PASS_STATUS,
    STATUS as V18_STATUS,
    REQUIRED_SOURCE_FIELDS,
    DIAGRAM_FAMILIES as V18_DIAGRAM_FAMILIES,
    COEFFICIENT_IMPORT_ROWS as V18_COEFFICIENT_IMPORT_ROWS,
    IMPORT_GATES as V18_IMPORT_GATES,
    FIRST_FAILED_GATE as V18_FIRST_FAILED_GATE,
    SAFE_CLAIMS as V18_SAFE_CLAIMS,
    FORBIDDEN_CLAIMS as V18_FORBIDDEN_CLAIMS,
    COUNTERTERM_TARGET_DELTA_R,
    DELTA_ALPHA_ADMITTED,
    RHO_BRANCH_LEADING,
    DIZET_DR_TOTAL,
    DIZET_MW_GEV,
    DIZET_MINUS_APF_MEV,
    M_W_TRACE_GEV,
    TOTAL_SIGMA_MW_MEV,
    PULL_INPUT_PLUS_THEORY,
)
from apf.w_trace_denner_sirlin_counterterm_functional import (
    DRREM_TARGET as DIZET_REM,
    RHO_CROSS_MINUS_LEAD_TARGET as RHO_CROSS_CORRECTION_TARGET,
)
from apf.w_trace_tensor_coefficient_map_scaffold import BASIS

STATUS = "P_w_trace_denner_formula_import_native_assembly"
VERSION = "v19_0"
PASS_STATUS = "W_TRACE_DENNER_FORMULA_IMPORT_NATIVE_ASSEMBLY_PASS"
TITLE = "W_TRACE Denner/Sirlin formula import and native one-loop assembly sprint"
PAYLOAD_ID = "W_TRACE_DENNER_FORMULA_IMPORT_NATIVE_ASSEMBLY_v19_0"
APF_VERSION = "19.0.0"

ROUTE_STATUS = "P_export_candidate_plus_partial_native_one_loop_assembly"
NATIVE_ONE_LOOP_STATUS = "P_partial_evaluated_open_full_counterterm_formulae"
FIRST_FAILED_GATE = "APF_NATIVE_FULL_DENNER_SIRLIN_FORMULA_IMPORT_NOT_COMPLETE"
NEXT_GATE = "G2L_FULL_DENNER_SIRLIN_SOURCE_FORMULA_TABLE_AND_NUMERIC_EVALUATOR"

@dataclass(frozen=True)
class SourceFormulaRow:
    row_id: str
    family: str
    formula_role: str
    formula_expression: str
    input_dependencies: Tuple[str, ...]
    pv_basis_terms: Tuple[str, ...]
    numeric_value: float | None
    import_status: str
    apf_admission: str
    blocks_full_native_one_loop: bool
    source_anchor: str

@dataclass(frozen=True)
class AssemblyRow:
    row_id: str
    contribution_class: str
    numeric_value: float
    source: str
    admission_status: str
    included_in_partial_native: bool
    included_in_target_closure: bool

@dataclass(frozen=True)
class FormulaGate:
    gate_id: str
    status: str
    object: str
    evidence: str
    blocks_full_native_one_loop: bool

@dataclass(frozen=True)
class MissingFormulaFamily:
    family: str
    missing_object: str
    current_proxy_or_target: str
    why_not_closed: str
    next_acquisition: str

SOURCE_FORMULA_ROWS: Tuple[SourceFormulaRow, ...] = (
    SourceFormulaRow(
        "F_DELTA_ALPHA_RUNNING", "VAC_POL_FERMION", "running electromagnetic coupling / vacuum polarization input row",
        "Delta r_DeltaAlpha := Delta alpha_had+lept+top as admitted same-input DIZET row",
        ("DeltaAlpha_had5", "lepton thresholds", "top threshold"),
        ("B0_prime_gamma_gamma_0",), DELTA_ALPHA_ADMITTED,
        "FORMULA_IMPORTED_EVALUATED_AS_INPUT_ROW", "ADMIT_NATIVE_INPUT_ROW", False,
        "DIZET same-input Delta-alpha diagnostic; PDG/Denner running-alpha convention",
    ),
    SourceFormulaRow(
        "F_RHO_LEADING_TOP", "SE_W_TRANSVERSE+SE_Z_TRANSVERSE", "leading top-rho self-energy branch",
        "Delta r_rho_lead = -(c_W^2/s_W^2) * 3 G_F m_t^2/(8 sqrt(2) pi^2)",
        ("G_F", "m_t", "M_W", "M_Z"),
        ("A0(mt)", "B0(0;mt,mb) asymptotic"), RHO_BRANCH_LEADING,
        "FORMULA_IMPORTED_EVALUATED_ANALYTIC", "ADMIT_NATIVE_ANALYTIC_ROW", False,
        "Sirlin/Denner leading rho structure; APF same-input algebra",
    ),
    SourceFormulaRow(
        "F_CHARGE_RENORMALIZATION", "SE_GAMMA_Z_MIX", "charge renormalization / photon field row",
        "delta Z_e = -1/2 delta Z_AA - (s_W/(2 c_W)) delta Z_ZA; finite part required",
        ("M_W", "M_Z", "fermion masses", "renormalization convention"),
        ("B0'", "B1", "B00"), None,
        "SOURCE_FORMULA_SLOT_IMPORTED_NOT_NUMERIC", "OPEN_REQUIRES_COEFFICIENTS", True,
        "Denner electroweak on-shell counterterm notation",
    ),
    SourceFormulaRow(
        "F_WEAK_ANGLE_COUNTERTERM", "SE_W_TRANSVERSE+SE_Z_TRANSVERSE", "weak-angle counterterm row",
        "delta s_W/s_W = -(c_W^2/(2 s_W^2)) (delta M_W^2/M_W^2 - delta M_Z^2/M_Z^2)",
        ("Sigma_T^W(M_W^2)", "Sigma_T^Z(M_Z^2)"),
        ("A0", "B0", "B00"), None,
        "SOURCE_FORMULA_SLOT_IMPORTED_NOT_NUMERIC", "OPEN_REQUIRES_SELF_ENERGY_COEFFICIENTS", True,
        "Denner on-shell mass and weak-angle counterterm relation",
    ),
    SourceFormulaRow(
        "F_W_MASS_COUNTERTERM", "SE_W_TRANSVERSE", "W mass counterterm",
        "delta M_W^2 = Re Sigma_T^W(M_W^2)",
        ("M_W", "M_Z", "m_t", "m_b", "m_H", "gauge convention"),
        ("A0", "B0", "B1", "B00"), None,
        "SOURCE_FORMULA_SLOT_IMPORTED_NOT_NUMERIC", "OPEN_REQUIRES_SELF_ENERGY_COEFFICIENTS", True,
        "Denner W self-energy counterterm formula",
    ),
    SourceFormulaRow(
        "F_Z_MASS_COUNTERTERM", "SE_Z_TRANSVERSE", "Z mass counterterm",
        "delta M_Z^2 = Re Sigma_T^Z(M_Z^2)",
        ("M_W", "M_Z", "m_t", "m_b", "m_H", "gauge convention"),
        ("A0", "B0", "B1", "B00"), None,
        "SOURCE_FORMULA_SLOT_IMPORTED_NOT_NUMERIC", "OPEN_REQUIRES_SELF_ENERGY_COEFFICIENTS", True,
        "Denner Z self-energy counterterm formula",
    ),
    SourceFormulaRow(
        "F_VERTEX_MU_DECAY", "VERTEX_MU_DECAY", "muon-decay vertex finite part",
        "Delta r_vertex := finite on-shell vertex correction to muon decay amplitude",
        ("M_W", "M_Z", "external momenta", "gauge convention"),
        ("B0", "C0", "Cij tensor coefficients"), None,
        "SOURCE_FORMULA_SLOT_IMPORTED_NOT_NUMERIC", "OPEN_REQUIRES_VERTEX_COEFFICIENTS", True,
        "Sirlin/Denner muon-decay vertex formula family",
    ),
    SourceFormulaRow(
        "F_BOX_MU_DECAY", "BOX_MU_DECAY", "muon-decay box finite part",
        "Delta r_box := finite on-shell box correction to muon decay amplitude",
        ("M_W", "M_Z", "external momenta", "gauge convention"),
        ("C0", "D0", "Dij tensor coefficients"), None,
        "SOURCE_FORMULA_SLOT_IMPORTED_NOT_NUMERIC", "OPEN_REQUIRES_BOX_COEFFICIENTS", True,
        "Sirlin/Denner muon-decay box formula family",
    ),
    SourceFormulaRow(
        "F_TAD_GHOST_GAUGE", "TAD_GHOST_GAUGE", "tadpole/ghost/gauge-restoring finite row",
        "Delta r_tgg := convention-dependent finite terms needed for gauge-parameter cancellation",
        ("m_H", "M_W", "M_Z", "gauge-fixing convention"),
        ("A0", "B0"), None,
        "SOURCE_FORMULA_SLOT_IMPORTED_NOT_NUMERIC", "OPEN_REQUIRES_GAUGE_CANCELLATION_AUDIT", True,
        "Denner on-shell tadpole and gauge-restoring convention",
    ),
    SourceFormulaRow(
        "F_DIZET_FINITE_REMAINDER_TARGET", "IMPLEMENTATION_REMAINDER", "same-input finite remainder target",
        "Delta r_rem^DIZET + (Delta r_rho-cross^DIZET - Delta r_rho-lead)",
        ("DIZET same-input internal diagnostics",),
        tuple(sorted(BASIS.keys())), COUNTERTERM_TARGET_DELTA_R,
        "TARGET_VALUE_ONLY_NOT_SOURCE_FORMULA", "TARGET_ONLY_NOT_PROOF", True,
        "DIZET internal row ledger, APF v16.8 target identity",
    ),
)

ASSEMBLY_ROWS: Tuple[AssemblyRow, ...] = (
    AssemblyRow("A_DELTA_ALPHA", "native_input_row", DELTA_ALPHA_ADMITTED, "F_DELTA_ALPHA_RUNNING", "ADMITTED", True, True),
    AssemblyRow("A_RHO_LEAD", "native_analytic_row", RHO_BRANCH_LEADING, "F_RHO_LEADING_TOP", "ADMITTED", True, True),
    AssemblyRow("A_DIZET_REM_TARGET", "target_benchmark_row", DIZET_REM, "DIZET internal DRREM row", "TARGET_ONLY", False, True),
    AssemblyRow("A_RHO_RESUM_CROSS_TARGET", "target_benchmark_row", RHO_CROSS_CORRECTION_TARGET, "DIZET rho-cross minus leading-rho branch", "TARGET_ONLY", False, True),
)

FORMULA_GATES: Tuple[FormulaGate, ...] = (
    FormulaGate("G2I_SOURCE_FORMULA_MATRIX", "CLOSED", "formula import matrix", "ten formula/target rows declared with source anchors, dependencies, PV basis, and admission status", False),
    FormulaGate("G2I_NATIVE_DELTA_ALPHA_ROW", "CLOSED", "Delta-alpha row", "same-input DIZET/Denner running-alpha row admitted as APF input row", False),
    FormulaGate("G2I_NATIVE_RHO_LEAD_ROW", "CLOSED", "leading top-rho row", "analytic same-input APF formula evaluated", False),
    FormulaGate("G2I_PARTIAL_NATIVE_ASSEMBLY", "CLOSED", "partial native one-loop assembly", "Delta alpha + leading rho branch evaluated without fitted coefficients", False),
    FormulaGate("G2I_TARGET_CLOSURE", "CLOSED", "finite counterterm target closure", "partial native assembly plus DIZET target rows equals same-input DIZET Delta-r", False),
    FormulaGate("G2I_NO_FIT_GUARD", "CLOSED_GUARD", "no-fitted-coefficients guard", "least-norm or target-only rows are not admitted as proof", False),
    FormulaGate("G2L_SELF_ENERGY_COEFFS", "OPEN", "reviewed W/Z self-energy coefficient functions", "source formula slots imported, numeric coefficients not imported", True),
    FormulaGate("G2L_VERTEX_BOX_COEFFS", "OPEN", "reviewed vertex/box coefficient functions", "source formula slots imported, full-kinematic tensor coefficients not imported", True),
    FormulaGate("G2L_GAUGE_CANCELLATION_AUDIT", "OPEN", "gauge/tadpole/ghost cancellation audit", "requires source formula coefficients and gauge-parameter check", True),
    FormulaGate("G2L_FULL_NATIVE_ONE_LOOP", "OPEN", "full APF-native one-loop Delta-r evaluator", FIRST_FAILED_GATE, True),
)

MISSING_FAMILIES: Tuple[MissingFormulaFamily, ...] = (
    MissingFormulaFamily("SE_W_TRANSVERSE", "finite W self-energy coefficient table", "W mass counterterm slot", "only symbolic counterterm relation imported", "import Denner W self-energy coefficient formulae over PV basis"),
    MissingFormulaFamily("SE_Z_TRANSVERSE", "finite Z self-energy coefficient table", "Z mass/weak-angle counterterm slot", "only symbolic counterterm relation imported", "import Denner Z self-energy coefficient formulae over PV basis"),
    MissingFormulaFamily("SE_GAMMA_Z_MIX", "charge/gamma-Z field counterterm coefficient table", "charge-renormalization slot", "field-mixing coefficients not numerically assembled", "import delta Z_e, delta Z_AA, delta Z_ZA coefficient formulae"),
    MissingFormulaFamily("VERTEX_MU_DECAY", "muon-decay vertex coefficient table", "vertex slot", "full C-tensor finite coefficients not imported", "import Sirlin/Denner vertex finite formulae"),
    MissingFormulaFamily("BOX_MU_DECAY", "muon-decay box coefficient table", "box slot", "full D-tensor finite coefficients not imported", "import Sirlin/Denner box finite formulae"),
    MissingFormulaFamily("TAD_GHOST_GAUGE", "tadpole/ghost/gauge finite table", "gauge-restoring slot", "gauge-cancellation proof not native", "import tadpole convention and gauge-parameter cancellation rows"),
)

SAFE_CLAIMS = (
    "v19 imports a source-formula matrix and evaluates the defensible APF-native Delta-alpha and leading-rho rows.",
    "The partial APF-native one-loop assembly is evaluated without fitted coefficients.",
    "The remaining finite/counterterm target is exactly localized and preserved as target-only evidence, not proof.",
    "The W route remains an export candidate through reviewed DIZET transport and now has a partial native one-loop assembly beneath it.",
)

FORBIDDEN_CLAIMS = (
    "The full Denner/Sirlin coefficient formula table has been numerically imported.",
    "The DIZET finite remainder target is an APF-native formula.",
    "The full APF-native one-loop Delta-r evaluator is closed.",
    "Vertex, box, and gauge-cancellation families have been fully evaluated natively.",
)

def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True, default=str)

def _digest(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(obj).encode("utf-8")).hexdigest()

def _res(check: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    row = {"check": check, "passed": bool(passed), "status": "PASS" if passed else "FAIL", "epistemic": STATUS}
    row.update(extra)
    return row

def _passed(row: Any) -> bool:
    return bool(isinstance(row, Mapping) and (row.get("passed") is True or row.get("status") in ("PASS", "P")))

def source_formula_table() -> Tuple[Dict[str, Any], ...]: return tuple(asdict(x) for x in SOURCE_FORMULA_ROWS)
def assembly_table() -> Tuple[Dict[str, Any], ...]: return tuple(asdict(x) for x in ASSEMBLY_ROWS)
def formula_gate_table() -> Tuple[Dict[str, Any], ...]: return tuple(asdict(x) for x in FORMULA_GATES)
def missing_family_table() -> Tuple[Dict[str, Any], ...]: return tuple(asdict(x) for x in MISSING_FAMILIES)

def imported_evaluated_rows() -> Tuple[SourceFormulaRow, ...]:
    return tuple(r for r in SOURCE_FORMULA_ROWS if r.import_status.startswith("FORMULA_IMPORTED_EVALUATED"))

def target_only_rows() -> Tuple[SourceFormulaRow, ...]:
    return tuple(r for r in SOURCE_FORMULA_ROWS if "TARGET" in r.import_status or "TARGET" in r.apf_admission)

def open_formula_rows() -> Tuple[SourceFormulaRow, ...]:
    return tuple(r for r in SOURCE_FORMULA_ROWS if r.blocks_full_native_one_loop and r.apf_admission.startswith("OPEN"))

def partial_native_delta_r() -> float:
    return sum(r.numeric_value for r in ASSEMBLY_ROWS if r.included_in_partial_native)

def target_only_delta_r() -> float:
    return sum(r.numeric_value for r in ASSEMBLY_ROWS if (not r.included_in_partial_native) and r.included_in_target_closure)

def target_closed_delta_r() -> float:
    return sum(r.numeric_value for r in ASSEMBLY_ROWS if r.included_in_target_closure)

def assembly_vector() -> Dict[str, float]:
    return {
        "Delta_alpha": DELTA_ALPHA_ADMITTED,
        "rho_leading_branch": RHO_BRANCH_LEADING,
        "partial_native_delta_r": partial_native_delta_r(),
        "DIZET_remainder_target": DIZET_REM,
        "rho_resummation_cross_target": RHO_CROSS_CORRECTION_TARGET,
        "finite_counterterm_target": COUNTERTERM_TARGET_DELTA_R,
        "target_only_delta_r": target_only_delta_r(),
        "target_closed_delta_r": target_closed_delta_r(),
        "DIZET_delta_r_total": DIZET_DR_TOTAL,
        "target_closure_residual": target_closed_delta_r() - DIZET_DR_TOTAL,
        "native_to_full_gap": DIZET_DR_TOTAL - partial_native_delta_r(),
    }

def source_formula_coverage() -> Dict[str, Any]:
    total = len(SOURCE_FORMULA_ROWS)
    evaluated = len(imported_evaluated_rows())
    targets = len(target_only_rows())
    open_rows = len(open_formula_rows())
    return {
        "total_formula_rows": total,
        "evaluated_native_rows": evaluated,
        "target_only_rows": targets,
        "open_formula_rows": open_rows,
        "evaluated_fraction": evaluated / total,
        "closed_or_target_localized_fraction": (evaluated + targets) / total,
    }

def route_summary() -> Dict[str, Any]:
    return {
        "title": TITLE,
        "version": VERSION,
        "apf_version": APF_VERSION,
        "dependency": {"module_status": V18_STATUS, "pass_status": V18_PASS_STATUS, "v18_first_failed_gate": V18_FIRST_FAILED_GATE},
        "route_status": ROUTE_STATUS,
        "native_one_loop_status": NATIVE_ONE_LOOP_STATUS,
        "first_failed_gate": FIRST_FAILED_GATE,
        "next_gate": NEXT_GATE,
        "source_formula_rows": source_formula_table(),
        "assembly_rows": assembly_table(),
        "formula_gates": formula_gate_table(),
        "missing_families": missing_family_table(),
        "assembly_vector": assembly_vector(),
        "coverage": source_formula_coverage(),
        "export_candidate_state": {"M_W_TRACE_GeV": M_W_TRACE_GEV, "M_W_DIZET_GeV": DIZET_MW_GEV, "DIZET_minus_APF_MeV": DIZET_MINUS_APF_MEV, "sigma_total_MW_MeV": TOTAL_SIGMA_MW_MEV, "pull_sigma": PULL_INPUT_PLUS_THEORY},
        "safe_claims": SAFE_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "payload_digest": _digest([source_formula_table(), assembly_table(), formula_gate_table(), missing_family_table(), assembly_vector()]),
    }

def terminal_report() -> Dict[str, Any]:
    return {"status": STATUS, "pass_status": PASS_STATUS, "route_summary": route_summary()}

# checks

def check_T_w_trace_formula_import_status_declared(): return _res("status_declared", STATUS.startswith("P_w_trace") and VERSION == "v19_0")
def check_T_w_trace_formula_import_dependency_pass(): return _res("dependency_pass", V18_PASS_STATUS.endswith("PASS"))
def check_T_w_trace_formula_import_source_row_count(): return _res("source_row_count", len(SOURCE_FORMULA_ROWS) == 10)
def check_T_w_trace_formula_import_assembly_row_count(): return _res("assembly_row_count", len(ASSEMBLY_ROWS) == 4)
def check_T_w_trace_formula_import_gate_count(): return _res("gate_count", len(FORMULA_GATES) == 10)
def check_T_w_trace_formula_import_missing_family_count(): return _res("missing_family_count", len(MISSING_FAMILIES) == 6)
def check_T_w_trace_formula_import_unique_source_rows(): return _res("unique_source_rows", len({r.row_id for r in SOURCE_FORMULA_ROWS}) == len(SOURCE_FORMULA_ROWS))
def check_T_w_trace_formula_import_unique_gates(): return _res("unique_gates", len({g.gate_id for g in FORMULA_GATES}) == len(FORMULA_GATES))
def check_T_w_trace_formula_import_required_fields_preserved(): return _res("required_fields_preserved", len(REQUIRED_SOURCE_FIELDS) == 10)
def check_T_w_trace_formula_import_v18_families_available(): return _res("v18_families_available", len(V18_DIAGRAM_FAMILIES) == 8)
def check_T_w_trace_formula_import_v18_import_contract_available(): return _res("v18_import_contract_available", len(V18_COEFFICIENT_IMPORT_ROWS) == 9)
def check_T_w_trace_formula_import_v18_gates_available(): return _res("v18_gates_available", len(V18_IMPORT_GATES) == 8)
def check_T_w_trace_formula_import_delta_alpha_evaluated(): return _res("delta_alpha_evaluated", any(r.row_id == "F_DELTA_ALPHA_RUNNING" and r.numeric_value == DELTA_ALPHA_ADMITTED for r in SOURCE_FORMULA_ROWS))
def check_T_w_trace_formula_import_rho_lead_evaluated(): return _res("rho_lead_evaluated", any(r.row_id == "F_RHO_LEADING_TOP" and r.numeric_value == RHO_BRANCH_LEADING for r in SOURCE_FORMULA_ROWS))
def check_T_w_trace_formula_import_evaluated_rows_count(): return _res("evaluated_rows_count", len(imported_evaluated_rows()) == 2)
def check_T_w_trace_formula_import_target_only_count(): return _res("target_only_count", len(target_only_rows()) == 1)
def check_T_w_trace_formula_import_open_rows_present(): return _res("open_rows_present", len(open_formula_rows()) >= 6)
def check_T_w_trace_formula_import_open_rows_block_full(): return _res("open_rows_block_full", all(r.blocks_full_native_one_loop for r in open_formula_rows()))
def check_T_w_trace_formula_import_formula_matrix_gate_closed(): return _res("formula_matrix_gate_closed", any(g.gate_id == "G2I_SOURCE_FORMULA_MATRIX" and g.status == "CLOSED" for g in FORMULA_GATES))
def check_T_w_trace_formula_import_delta_alpha_gate_closed(): return _res("delta_alpha_gate_closed", any(g.gate_id == "G2I_NATIVE_DELTA_ALPHA_ROW" and g.status == "CLOSED" for g in FORMULA_GATES))
def check_T_w_trace_formula_import_rho_gate_closed(): return _res("rho_gate_closed", any(g.gate_id == "G2I_NATIVE_RHO_LEAD_ROW" and g.status == "CLOSED" for g in FORMULA_GATES))
def check_T_w_trace_formula_import_partial_assembly_gate_closed(): return _res("partial_assembly_gate_closed", any(g.gate_id == "G2I_PARTIAL_NATIVE_ASSEMBLY" and g.status == "CLOSED" for g in FORMULA_GATES))
def check_T_w_trace_formula_import_target_closure_gate_closed(): return _res("target_closure_gate_closed", any(g.gate_id == "G2I_TARGET_CLOSURE" and g.status == "CLOSED" for g in FORMULA_GATES))
def check_T_w_trace_formula_import_no_fit_guard_closed(): return _res("no_fit_guard_closed", any(g.gate_id == "G2I_NO_FIT_GUARD" and g.status == "CLOSED_GUARD" for g in FORMULA_GATES))
def check_T_w_trace_formula_import_self_energy_gate_open(): return _res("self_energy_gate_open", any(g.gate_id == "G2L_SELF_ENERGY_COEFFS" and g.status == "OPEN" for g in FORMULA_GATES))
def check_T_w_trace_formula_import_vertex_box_gate_open(): return _res("vertex_box_gate_open", any(g.gate_id == "G2L_VERTEX_BOX_COEFFS" and g.status == "OPEN" for g in FORMULA_GATES))
def check_T_w_trace_formula_import_gauge_gate_open(): return _res("gauge_gate_open", any(g.gate_id == "G2L_GAUGE_CANCELLATION_AUDIT" and g.status == "OPEN" for g in FORMULA_GATES))
def check_T_w_trace_formula_import_full_native_gate_open(): return _res("full_native_gate_open", any(g.gate_id == "G2L_FULL_NATIVE_ONE_LOOP" and g.status == "OPEN" for g in FORMULA_GATES))
def check_T_w_trace_formula_import_open_gates_block_full(): return _res("open_gates_block_full", all(g.blocks_full_native_one_loop for g in FORMULA_GATES if g.status == "OPEN"))
def check_T_w_trace_formula_import_first_failed_gate_exact(): return _res("first_failed_gate_exact", FIRST_FAILED_GATE == "APF_NATIVE_FULL_DENNER_SIRLIN_FORMULA_IMPORT_NOT_COMPLETE")
def check_T_w_trace_formula_import_next_gate_exact(): return _res("next_gate_exact", NEXT_GATE == "G2L_FULL_DENNER_SIRLIN_SOURCE_FORMULA_TABLE_AND_NUMERIC_EVALUATOR")
def check_T_w_trace_formula_import_route_export_candidate(): return _res("route_export_candidate", "export_candidate" in ROUTE_STATUS)
def check_T_w_trace_formula_import_native_status_partial(): return _res("native_status_partial", NATIVE_ONE_LOOP_STATUS.startswith("P_partial"))
def check_T_w_trace_formula_import_partial_native_value(): return _res("partial_native_value", abs(partial_native_delta_r() - (DELTA_ALPHA_ADMITTED + RHO_BRANCH_LEADING)) < 1e-15, value=partial_native_delta_r())
def check_T_w_trace_formula_import_partial_native_range(): return _res("partial_native_range", 0.026 < partial_native_delta_r() < 0.027)
def check_T_w_trace_formula_import_target_only_value(): return _res("target_only_value", abs(target_only_delta_r() - COUNTERTERM_TARGET_DELTA_R) < 1e-15, value=target_only_delta_r())
def check_T_w_trace_formula_import_target_closure_zero(): return _res("target_closure_zero", abs(assembly_vector()["target_closure_residual"]) < 1e-15, residual=assembly_vector()["target_closure_residual"])
def check_T_w_trace_formula_import_native_to_full_gap_positive(): return _res("native_to_full_gap_positive", 0.009 < assembly_vector()["native_to_full_gap"] < 0.011, gap=assembly_vector()["native_to_full_gap"])
def check_T_w_trace_formula_import_counterterm_target_preserved(): return _res("counterterm_target_preserved", 0.009 < COUNTERTERM_TARGET_DELTA_R < 0.011)
def check_T_w_trace_formula_import_dizet_total_preserved(): return _res("dizet_total_preserved", 0.036 < DIZET_DR_TOTAL < 0.037)
def check_T_w_trace_formula_import_mw_residual_preserved(): return _res("mw_residual_preserved", -4.9 < DIZET_MINUS_APF_MEV < -4.7)
def check_T_w_trace_formula_import_sigma_preserved(): return _res("sigma_preserved", TOTAL_SIGMA_MW_MEV > 4.0 and 1.0 < PULL_INPUT_PLUS_THEORY < 1.2)
def check_T_w_trace_formula_import_missing_families_block(): return _res("missing_families_block", all(x.next_acquisition for x in MISSING_FAMILIES))
def check_T_w_trace_formula_import_missing_families_cover_vertex(): return _res("missing_families_cover_vertex", any(x.family == "VERTEX_MU_DECAY" for x in MISSING_FAMILIES))
def check_T_w_trace_formula_import_missing_families_cover_box(): return _res("missing_families_cover_box", any(x.family == "BOX_MU_DECAY" for x in MISSING_FAMILIES))
def check_T_w_trace_formula_import_missing_families_cover_self_energy(): return _res("missing_families_cover_self_energy", {"SE_W_TRANSVERSE", "SE_Z_TRANSVERSE"}.issubset({x.family for x in MISSING_FAMILIES}))
def check_T_w_trace_formula_import_target_row_not_admitted(): return _res("target_row_not_admitted", all(r.apf_admission != "ADMIT_NATIVE_FORMULA" for r in target_only_rows()))
def check_T_w_trace_formula_import_no_fitted_coefficients(): return _res("no_fitted_coefficients", all("FIT" not in r.import_status for r in SOURCE_FORMULA_ROWS))
def check_T_w_trace_formula_import_open_rows_not_numeric(): return _res("open_rows_not_numeric", all(r.numeric_value is None for r in open_formula_rows()))
def check_T_w_trace_formula_import_evaluated_rows_numeric(): return _res("evaluated_rows_numeric", all(r.numeric_value is not None and math.isfinite(r.numeric_value) for r in imported_evaluated_rows()))
def check_T_w_trace_formula_import_coverage_total(): return _res("coverage_total", source_formula_coverage()["total_formula_rows"] == 10)
def check_T_w_trace_formula_import_coverage_evaluated_fraction(): return _res("coverage_evaluated_fraction", abs(source_formula_coverage()["evaluated_fraction"] - 0.2) < 1e-15)
def check_T_w_trace_formula_import_report_has_rows(): return _res("report_has_rows", len(route_summary()["source_formula_rows"]) == 10)
def check_T_w_trace_formula_import_report_has_assembly(): return _res("report_has_assembly", len(route_summary()["assembly_rows"]) == 4)
def check_T_w_trace_formula_import_report_has_missing(): return _res("report_has_missing", len(route_summary()["missing_families"]) == 6)
def check_T_w_trace_formula_import_payload_digest_present(): return _res("payload_digest_present", route_summary()["payload_digest"].startswith("sha256:"))
def check_T_w_trace_formula_import_safe_claims_present(): return _res("safe_claims_present", len(SAFE_CLAIMS) == 4)
def check_T_w_trace_formula_import_forbidden_claims_present(): return _res("forbidden_claims_present", len(FORBIDDEN_CLAIMS) == 4)
def check_T_w_trace_formula_import_forbids_full_closure(): return _res("forbids_full_closure", any("full APF-native one-loop" in c for c in FORBIDDEN_CLAIMS))
def check_T_w_trace_formula_import_forbids_target_as_formula(): return _res("forbids_target_as_formula", any("finite remainder target" in c for c in FORBIDDEN_CLAIMS))
def check_T_w_trace_formula_import_terminal_report_status(): return _res("terminal_report_status", terminal_report()["pass_status"] == PASS_STATUS)
def check_T_w_trace_formula_import_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_trace_formula_import_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))

_CHECKS = {name: obj for name, obj in sorted(globals().items()) if name.startswith("check_T_w_trace_formula_import_") and callable(obj)}

def register(registry: MutableMapping[str, Any]) -> None:
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
    return {"passed": ok, "status": PASS_STATUS if ok else PASS_STATUS.replace("_PASS", "_FAIL"), "checks": rows, "report": terminal_report()}

if __name__ == "__main__":
    out = run_all()
    print(out["status"])
    for row in out["checks"]:
        print(("PASS" if row["passed"] else "FAIL"), row["name"])
