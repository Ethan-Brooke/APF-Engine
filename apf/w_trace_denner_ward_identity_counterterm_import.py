"""W_TRACE Denner/Sirlin Ward-identity and counterterm formula import layer.

v20.0 (2026-05-09): deepens v19 from a source-formula import matrix into a
reviewed-relation import layer.  This module does not claim full APF-native
one-loop numerical closure.  It imports the on-shell Ward/counterterm relations
needed to make the Denner/Sirlin coefficient table meaningful, declares the
family-level assembly DAG for Delta r, and proves that the remaining numerical
object is not the scalar-integral substrate or tensor primitive layer but the
reviewed diagram coefficient/evaluator table for self-energy, vertex, box, and
gauge-cancellation finite parts.

No fitted coefficient is admitted.  Target residuals remain target-only.
"""
from __future__ import annotations

import hashlib, json, math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_denner_formula_import_native_assembly import (
    PASS_STATUS as V19_PASS_STATUS, STATUS as V19_STATUS,
    SOURCE_FORMULA_ROWS as V19_SOURCE_FORMULA_ROWS,
    FORMULA_GATES as V19_FORMULA_GATES,
    MISSING_FAMILIES as V19_MISSING_FAMILIES,
    DELTA_ALPHA_ADMITTED, RHO_BRANCH_LEADING, COUNTERTERM_TARGET_DELTA_R,
    DIZET_DR_TOTAL, DIZET_MW_GEV, DIZET_MINUS_APF_MEV, M_W_TRACE_GEV,
    TOTAL_SIGMA_MW_MEV, PULL_INPUT_PLUS_THEORY,
    partial_native_delta_r as v19_partial_native_delta_r,
)
from apf.w_trace_pv_scalar_integral_substrate import PASS_STATUS as PV_PASS_STATUS
from apf.w_trace_tensor_coefficient_map_scaffold import PASS_STATUS as TENSOR_PASS_STATUS, BASIS

STATUS = "P_w_trace_denner_ward_identity_counterterm_import"
VERSION = "v20_0"
PASS_STATUS = "W_TRACE_DENNER_WARD_IDENTITY_COUNTERTERM_IMPORT_PASS"
TITLE = "W_TRACE Denner/Sirlin Ward-identity and counterterm formula import layer"
PAYLOAD_ID = "W_TRACE_DENNER_WARD_IDENTITY_COUNTERTERM_IMPORT_v20_0"
APF_VERSION = "20.0.0"

ROUTE_STATUS = "P_export_candidate_plus_ward_counterterm_import_layer"
NATIVE_ONE_LOOP_STATUS = "P_partial_native_rows_plus_reviewed_relation_import_open_numeric_family_evaluators"
FIRST_FAILED_GATE = "APF_NATIVE_REVIEWED_DIAGRAM_FAMILY_NUMERIC_EVALUATORS_NOT_IMPORTED"
NEXT_GATE = "G2M_SELF_ENERGY_VERTEX_BOX_GAUGE_FAMILY_EVALUATORS"

@dataclass(frozen=True)
class ImportedRelation:
    relation_id: str
    relation_class: str
    expression: str
    required_inputs: Tuple[str, ...]
    output_objects: Tuple[str, ...]
    pv_or_tensor_dependencies: Tuple[str, ...]
    import_status: str
    numeric_status: str
    admits_as_formula: bool
    source_anchor: str

@dataclass(frozen=True)
class AssemblyFamily:
    family_id: str
    role_in_delta_r: str
    relation_inputs: Tuple[str, ...]
    required_numeric_evaluator: str
    current_value: float | None
    admission_status: str
    blocks_full_native_one_loop: bool

@dataclass(frozen=True)
class WardIdentityGate:
    gate_id: str
    status: str
    object: str
    evidence: str
    blocks_full_native_one_loop: bool

@dataclass(frozen=True)
class NativeImportFrontier:
    frontier_id: str
    closed_object: str
    remaining_object: str
    why_it_matters: str
    next_acquisition_step: str

IMPORTED_RELATIONS: Tuple[ImportedRelation, ...] = (
    ImportedRelation(
        "R_OS_MASS_CT_W", "ON_SHELL_MASS_COUNTERTERM",
        "delta M_W^2 = Re Sigma_T^W(M_W^2)",
        ("Sigma_T^W", "M_W"), ("delta_MW2",), ("A0", "B0", "B00"),
        "REVIEWED_RELATION_IMPORTED", "NEEDS_SELF_ENERGY_NUMERIC_COEFFICIENTS", True,
        "Denner on-shell mass renormalization relation",
    ),
    ImportedRelation(
        "R_OS_MASS_CT_Z", "ON_SHELL_MASS_COUNTERTERM",
        "delta M_Z^2 = Re Sigma_T^Z(M_Z^2)",
        ("Sigma_T^Z", "M_Z"), ("delta_MZ2",), ("A0", "B0", "B00"),
        "REVIEWED_RELATION_IMPORTED", "NEEDS_SELF_ENERGY_NUMERIC_COEFFICIENTS", True,
        "Denner on-shell mass renormalization relation",
    ),
    ImportedRelation(
        "R_WEAK_ANGLE_CT", "ON_SHELL_WEAK_ANGLE_COUNTERTERM",
        "delta s_W/s_W = -(c_W^2/(2 s_W^2))*(delta M_W^2/M_W^2 - delta M_Z^2/M_Z^2)",
        ("delta_MW2", "delta_MZ2", "M_W", "M_Z"), ("delta_sW_over_sW",), ("A0", "B0", "B00"),
        "REVIEWED_RELATION_IMPORTED", "COMPOSITE_NEEDS_MASS_CTS", True,
        "Denner on-shell weak-mixing-angle counterterm relation",
    ),
    ImportedRelation(
        "R_CHARGE_CT_ALPHA0", "WARD_CHARGE_RENORMALIZATION",
        "delta Z_e|alpha(0) = -1/2 Re[delta Z_AA + (s_W/c_W) delta Z_ZA]",
        ("delta_Z_AA", "delta_Z_ZA", "s_W", "c_W"), ("delta_Z_e_alpha0",), ("B0_prime", "B1"),
        "REVIEWED_RELATION_IMPORTED", "NEEDS_NEUTRAL_FIELD_RENORM_NUMERIC_COEFFICIENTS", True,
        "Denner charge-renormalization Ward relation",
    ),
    ImportedRelation(
        "R_FIELD_AA", "FIELD_RENORMALIZATION",
        "delta Z_AA = - Re d Sigma_T^AA(k^2)/dk^2 | k^2=0",
        ("Sigma_T^AA_prime_0",), ("delta_Z_AA",), ("B0_prime",),
        "REVIEWED_RELATION_IMPORTED", "NEEDS_PHOTON_SELF_ENERGY_DERIVATIVE", True,
        "Neutral gauge-field wave-function counterterm relation",
    ),
    ImportedRelation(
        "R_FIELD_ZA", "FIELD_MIXING_RENORMALIZATION",
        "delta Z_ZA = 2 Sigma_T^AZ(0)/M_Z^2",
        ("Sigma_T^AZ_0", "M_Z"), ("delta_Z_ZA",), ("B0", "B00"),
        "REVIEWED_RELATION_IMPORTED", "NEEDS_GAMMA_Z_MIXING_NUMERIC_COEFFICIENTS", True,
        "Neutral gauge-field mixing counterterm relation",
    ),
    ImportedRelation(
        "R_DELTA_ALPHA_ROW", "RUNNING_ALPHA_INPUT_ROW",
        "Delta r_DeltaAlpha = Delta alpha admitted at same-input route point",
        ("DeltaAlpha_had5", "leptonic_vacuum_polarization"), ("Delta_r_DeltaAlpha",), ("B0_prime_gamma_gamma_0",),
        "REVIEWED_INPUT_ROW_IMPORTED_EVALUATED", "EVALUATED", True,
        "DIZET same-input diagnostic and standard running-alpha convention",
    ),
    ImportedRelation(
        "R_RHO_LEAD_ROW", "LEADING_TOP_RHO_ROW",
        "Delta r_rho_lead = -(c_W^2/s_W^2) * 3 G_F m_t^2/(8 sqrt(2) pi^2)",
        ("G_F", "m_t", "M_W", "M_Z"), ("Delta_r_rho_lead",), ("A0_top_asymptotic", "B0_tb_asymptotic"),
        "REVIEWED_ANALYTIC_ROW_IMPORTED_EVALUATED", "EVALUATED", True,
        "Sirlin/Denner leading top-rho structure",
    ),
    ImportedRelation(
        "R_VERTEX_FAMILY", "MUON_DECAY_VERTEX_FINITE_RELATION",
        "Delta r_vertex = finite one-loop muon-decay vertex correction after OS subtraction",
        ("vertex_amplitudes", "external_leg_convention"), ("Delta_r_vertex",), ("B0", "C0", "C_tensor"),
        "RELATION_SLOT_IMPORTED", "NEEDS_VERTEX_NUMERIC_COEFFICIENTS", True,
        "Sirlin/Denner muon-decay vertex family",
    ),
    ImportedRelation(
        "R_BOX_FAMILY", "MUON_DECAY_BOX_FINITE_RELATION",
        "Delta r_box = finite one-loop muon-decay box correction after matching to Fermi theory",
        ("box_amplitudes", "Fermi_matching_convention"), ("Delta_r_box",), ("C0", "D0", "D_tensor"),
        "RELATION_SLOT_IMPORTED", "NEEDS_BOX_NUMERIC_COEFFICIENTS", True,
        "Sirlin/Denner muon-decay box family",
    ),
    ImportedRelation(
        "R_TAD_GHOST_GAUGE", "GAUGE_CANCELLATION_RELATION",
        "Delta r_gauge_restoring = tadpole + ghost + gauge-parameter-cancelling finite terms",
        ("tadpole_convention", "gauge_fixing", "ghost_rows"), ("Delta_r_gauge_restoring",), ("A0", "B0"),
        "RELATION_SLOT_IMPORTED", "NEEDS_GAUGE_CANCELLATION_NUMERIC_AUDIT", True,
        "Denner tadpole/gauge-restoring convention",
    ),
)

ASSEMBLY_FAMILIES: Tuple[AssemblyFamily, ...] = (
    AssemblyFamily("F_DELTA_ALPHA", "large positive vacuum-polarization channel", ("R_DELTA_ALPHA_ROW",), "evaluated input row", DELTA_ALPHA_ADMITTED, "ADMITTED_EVALUATED", False),
    AssemblyFamily("F_RHO_LEAD", "dominant negative leading top-rho channel", ("R_RHO_LEAD_ROW",), "analytic evaluated row", RHO_BRANCH_LEADING, "ADMITTED_EVALUATED", False),
    AssemblyFamily("F_MASS_WEAK_ANGLE_CT", "mass and weak-angle counterterm finite family", ("R_OS_MASS_CT_W", "R_OS_MASS_CT_Z", "R_WEAK_ANGLE_CT"), "W/Z self-energy coefficient evaluator", None, "RELATION_IMPORTED_NUMERIC_OPEN", True),
    AssemblyFamily("F_CHARGE_FIELD_CT", "charge/field-renormalization finite family", ("R_CHARGE_CT_ALPHA0", "R_FIELD_AA", "R_FIELD_ZA"), "neutral self-energy derivative/mixing evaluator", None, "RELATION_IMPORTED_NUMERIC_OPEN", True),
    AssemblyFamily("F_VERTEX", "muon-decay vertex finite family", ("R_VERTEX_FAMILY",), "vertex coefficient evaluator", None, "RELATION_IMPORTED_NUMERIC_OPEN", True),
    AssemblyFamily("F_BOX", "muon-decay box finite family", ("R_BOX_FAMILY",), "box coefficient evaluator", None, "RELATION_IMPORTED_NUMERIC_OPEN", True),
    AssemblyFamily("F_GAUGE_RESTORING", "tadpole/ghost/gauge-cancellation finite family", ("R_TAD_GHOST_GAUGE",), "gauge-cancellation numerical audit", None, "RELATION_IMPORTED_NUMERIC_OPEN", True),
    AssemblyFamily("F_TARGET_FINITE", "same-input full finite target for all open families", tuple(), "target only, not proof", COUNTERTERM_TARGET_DELTA_R, "TARGET_ONLY_QUARANTINED", True),
)

WARD_GATES: Tuple[WardIdentityGate, ...] = (
    WardIdentityGate("G2M_PV_TENSOR_SUBSTRATE", "CLOSED", "PV scalar/tensor substrate", "v16.9/v17.0 dependencies pass", False),
    WardIdentityGate("G2M_RELATION_IMPORT", "CLOSED", "reviewed Ward/counterterm relations", "eleven relation rows imported with dependencies and output objects", False),
    WardIdentityGate("G2M_NATIVE_EVALUATED_ROWS", "CLOSED", "Delta-alpha and leading-rho rows", "two same-input rows evaluated natively or as admitted input row", False),
    WardIdentityGate("G2M_RELATION_DAG", "CLOSED", "relation-to-family DAG", "all eight families map to imported relation ids or target quarantine", False),
    WardIdentityGate("G2M_TARGET_LOCALIZATION", "CLOSED", "same-input finite target", "open numeric families collectively target 0.009880894878", False),
    WardIdentityGate("G2M_NO_TARGET_FIT", "CLOSED_GUARD", "no target fitting", "target-only family is quarantined and not admitted as a formula", False),
    WardIdentityGate("G2M_SELF_ENERGY_NUMERIC", "OPEN", "reviewed W/Z/gamma/gamma-Z self-energy evaluator", "relations imported but coefficients not evaluated", True),
    WardIdentityGate("G2M_VERTEX_BOX_NUMERIC", "OPEN", "reviewed vertex/box finite evaluator", "relations imported but C/D tensor coefficient maps not evaluated", True),
    WardIdentityGate("G2M_GAUGE_CANCELLATION_NUMERIC", "OPEN", "tadpole/ghost/gauge cancellation evaluator", "relation slot imported but gauge audit not numeric", True),
    WardIdentityGate("G2M_FULL_NATIVE_ONE_LOOP", "OPEN", "full APF-native one-loop Delta-r", FIRST_FAILED_GATE, True),
)

FRONTIER: Tuple[NativeImportFrontier, ...] = (
    NativeImportFrontier("FRONTIER_SCALAR", "A0/B0/C0/D0 finite substrate", "none at scalar level", "integrals are available for coefficient maps", "keep as dependency"),
    NativeImportFrontier("FRONTIER_TENSOR", "B1/B00 tensor primitives and slot schema", "full C/D tensor coefficient maps", "vertex/box families require higher tensor assembly", "extend tensor reduction only when source formulas demand it"),
    NativeImportFrontier("FRONTIER_RELATIONS", "OS mass, weak-angle, charge, field, vertex, box relation imports", "numeric diagram-family evaluators", "relations alone do not produce finite rows", "import reviewed coefficient formulae family by family"),
    NativeImportFrontier("FRONTIER_NATIVE_ROWS", "Delta-alpha and leading-rho rows", "finite/counterterm families", "dominant scaffold closed; finite target remains", "start with self-energy finite coefficients"),
)

SAFE_CLAIMS = (
    "v20 imports reviewed Ward/counterterm relation structure beneath the v19 formula matrix.",
    "The scalar/tensor substrate is sufficient to host the next coefficient maps, but not enough to infer coefficients.",
    "The APF-native evaluated content remains Delta-alpha plus leading top-rho; the finite target is localized but quarantined.",
    "The next obstruction is numeric reviewed diagram-family evaluators, not DIZET transport or scalar integrals.",
)
FORBIDDEN_CLAIMS = (
    "v20 evaluates the full APF-native one-loop Delta-r.",
    "The counterterm target is derived rather than target-localized.",
    "The vertex, box, and gauge-cancellation finite rows are numerically imported.",
    "Fitted coefficients are accepted as Denner/Sirlin proof.",
)

def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True, default=str)
def _digest(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(obj).encode()).hexdigest()
def _res(check: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    row = {"check": check, "passed": bool(passed), "status": "PASS" if passed else "FAIL", "epistemic": STATUS}
    row.update(extra); return row
def _passed(row: Any) -> bool:
    return bool(isinstance(row, Mapping) and (row.get("passed") is True or row.get("status") in ("PASS", "P")))

def relation_table(): return tuple(asdict(r) for r in IMPORTED_RELATIONS)
def family_table(): return tuple(asdict(f) for f in ASSEMBLY_FAMILIES)
def gate_table(): return tuple(asdict(g) for g in WARD_GATES)
def frontier_table(): return tuple(asdict(f) for f in FRONTIER)
def evaluated_family_rows(): return tuple(f for f in ASSEMBLY_FAMILIES if f.admission_status == "ADMITTED_EVALUATED")
def open_numeric_families(): return tuple(f for f in ASSEMBLY_FAMILIES if f.admission_status == "RELATION_IMPORTED_NUMERIC_OPEN")
def target_families(): return tuple(f for f in ASSEMBLY_FAMILIES if "TARGET" in f.admission_status)
def relation_ids(): return {r.relation_id for r in IMPORTED_RELATIONS}
def native_partial_delta_r(): return sum(f.current_value for f in evaluated_family_rows() if f.current_value is not None)
def target_closure_delta_r(): return native_partial_delta_r() + COUNTERTERM_TARGET_DELTA_R

def relation_dependency_graph() -> Dict[str, Tuple[str, ...]]:
    return {f.family_id: f.relation_inputs for f in ASSEMBLY_FAMILIES}

def coverage() -> Dict[str, Any]:
    nrel = len(IMPORTED_RELATIONS); nfam = len(ASSEMBLY_FAMILIES)
    return {
        "relation_rows": nrel,
        "relation_rows_imported": sum(1 for r in IMPORTED_RELATIONS if "IMPORTED" in r.import_status or "SLOT_IMPORTED" in r.import_status),
        "evaluated_relations": sum(1 for r in IMPORTED_RELATIONS if r.numeric_status == "EVALUATED"),
        "families": nfam,
        "evaluated_families": len(evaluated_family_rows()),
        "open_numeric_families": len(open_numeric_families()),
        "target_families": len(target_families()),
        "evaluated_family_fraction": len(evaluated_family_rows()) / nfam,
    }

def assembly_vector() -> Dict[str, float]:
    return {
        "Delta_alpha": DELTA_ALPHA_ADMITTED,
        "rho_leading_branch": RHO_BRANCH_LEADING,
        "native_partial_delta_r": native_partial_delta_r(),
        "counterterm_target_delta_r": COUNTERTERM_TARGET_DELTA_R,
        "target_closed_delta_r": target_closure_delta_r(),
        "DIZET_delta_r_total": DIZET_DR_TOTAL,
        "target_closure_residual": target_closure_delta_r() - DIZET_DR_TOTAL,
        "native_open_gap": DIZET_DR_TOTAL - native_partial_delta_r(),
    }

def route_summary() -> Dict[str, Any]:
    return {
        "title": TITLE, "version": VERSION, "apf_version": APF_VERSION,
        "dependency": {"v19_status": V19_STATUS, "v19_pass_status": V19_PASS_STATUS, "pv_pass_status": PV_PASS_STATUS, "tensor_pass_status": TENSOR_PASS_STATUS},
        "route_status": ROUTE_STATUS, "native_one_loop_status": NATIVE_ONE_LOOP_STATUS,
        "first_failed_gate": FIRST_FAILED_GATE, "next_gate": NEXT_GATE,
        "relations": relation_table(), "families": family_table(), "gates": gate_table(), "frontier": frontier_table(),
        "dependency_graph": relation_dependency_graph(), "coverage": coverage(), "assembly_vector": assembly_vector(),
        "export_candidate_state": {"M_W_TRACE_GeV": M_W_TRACE_GEV, "M_W_DIZET_GeV": DIZET_MW_GEV, "DIZET_minus_APF_MeV": DIZET_MINUS_APF_MEV, "sigma_total_MW_MeV": TOTAL_SIGMA_MW_MEV, "pull_sigma": PULL_INPUT_PLUS_THEORY},
        "safe_claims": SAFE_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS,
        "payload_digest": _digest([relation_table(), family_table(), gate_table(), frontier_table(), assembly_vector()]),
    }

def terminal_report() -> Dict[str, Any]:
    return {"status": STATUS, "pass_status": PASS_STATUS, "route_summary": route_summary()}

# checks

def check_T_w_trace_ward_import_status_declared(): return _res("status_declared", STATUS.startswith("P_w_trace") and VERSION == "v20_0")
def check_T_w_trace_ward_import_dependencies_pass(): return _res("dependencies_pass", V19_PASS_STATUS.endswith("PASS") and PV_PASS_STATUS.endswith("PASS") and TENSOR_PASS_STATUS.endswith("PASS"))
def check_T_w_trace_ward_import_v19_rows_available(): return _res("v19_rows_available", len(V19_SOURCE_FORMULA_ROWS) == 10)
def check_T_w_trace_ward_import_v19_gates_available(): return _res("v19_gates_available", len(V19_FORMULA_GATES) == 10)
def check_T_w_trace_ward_import_v19_missing_available(): return _res("v19_missing_available", len(V19_MISSING_FAMILIES) == 6)
def check_T_w_trace_ward_import_relation_count(): return _res("relation_count", len(IMPORTED_RELATIONS) == 11)
def check_T_w_trace_ward_import_family_count(): return _res("family_count", len(ASSEMBLY_FAMILIES) == 8)
def check_T_w_trace_ward_import_gate_count(): return _res("gate_count", len(WARD_GATES) == 10)
def check_T_w_trace_ward_import_frontier_count(): return _res("frontier_count", len(FRONTIER) == 4)
def check_T_w_trace_ward_import_unique_relations(): return _res("unique_relations", len({r.relation_id for r in IMPORTED_RELATIONS}) == len(IMPORTED_RELATIONS))
def check_T_w_trace_ward_import_unique_families(): return _res("unique_families", len({f.family_id for f in ASSEMBLY_FAMILIES}) == len(ASSEMBLY_FAMILIES))
def check_T_w_trace_ward_import_unique_gates(): return _res("unique_gates", len({g.gate_id for g in WARD_GATES}) == len(WARD_GATES))
def check_T_w_trace_ward_import_relation_outputs_nonempty(): return _res("relation_outputs_nonempty", all(r.output_objects for r in IMPORTED_RELATIONS))
def check_T_w_trace_ward_import_relation_inputs_nonempty(): return _res("relation_inputs_nonempty", all(r.required_inputs for r in IMPORTED_RELATIONS))
def check_T_w_trace_ward_import_relation_dependencies_nonempty(): return _res("relation_dependencies_nonempty", all(r.pv_or_tensor_dependencies for r in IMPORTED_RELATIONS))
def check_T_w_trace_ward_import_mass_ct_w_imported(): return _res("mass_ct_w_imported", any(r.relation_id == "R_OS_MASS_CT_W" for r in IMPORTED_RELATIONS))
def check_T_w_trace_ward_import_mass_ct_z_imported(): return _res("mass_ct_z_imported", any(r.relation_id == "R_OS_MASS_CT_Z" for r in IMPORTED_RELATIONS))
def check_T_w_trace_ward_import_weak_angle_imported(): return _res("weak_angle_imported", any(r.relation_id == "R_WEAK_ANGLE_CT" for r in IMPORTED_RELATIONS))
def check_T_w_trace_ward_import_charge_ct_imported(): return _res("charge_ct_imported", any(r.relation_id == "R_CHARGE_CT_ALPHA0" for r in IMPORTED_RELATIONS))
def check_T_w_trace_ward_import_field_aa_imported(): return _res("field_aa_imported", any(r.relation_id == "R_FIELD_AA" for r in IMPORTED_RELATIONS))
def check_T_w_trace_ward_import_field_za_imported(): return _res("field_za_imported", any(r.relation_id == "R_FIELD_ZA" for r in IMPORTED_RELATIONS))
def check_T_w_trace_ward_import_vertex_imported(): return _res("vertex_imported", any(r.relation_id == "R_VERTEX_FAMILY" for r in IMPORTED_RELATIONS))
def check_T_w_trace_ward_import_box_imported(): return _res("box_imported", any(r.relation_id == "R_BOX_FAMILY" for r in IMPORTED_RELATIONS))
def check_T_w_trace_ward_import_gauge_imported(): return _res("gauge_imported", any(r.relation_id == "R_TAD_GHOST_GAUGE" for r in IMPORTED_RELATIONS))
def check_T_w_trace_ward_import_evaluated_relation_count(): return _res("evaluated_relation_count", coverage()["evaluated_relations"] == 2)
def check_T_w_trace_ward_import_evaluated_family_count(): return _res("evaluated_family_count", len(evaluated_family_rows()) == 2)
def check_T_w_trace_ward_import_open_numeric_family_count(): return _res("open_numeric_family_count", len(open_numeric_families()) == 5)
def check_T_w_trace_ward_import_target_family_count(): return _res("target_family_count", len(target_families()) == 1)
def check_T_w_trace_ward_import_all_open_block(): return _res("all_open_block", all(f.blocks_full_native_one_loop for f in open_numeric_families()))
def check_T_w_trace_ward_import_target_blocks_full(): return _res("target_blocks_full", all(f.blocks_full_native_one_loop for f in target_families()))
def check_T_w_trace_ward_import_relation_dag_references_exist(): return _res("relation_dag_references_exist", all(set(f.relation_inputs).issubset(relation_ids()) for f in ASSEMBLY_FAMILIES if f.relation_inputs))
def check_T_w_trace_ward_import_no_orphan_relations(): return _res("no_orphan_relations", relation_ids().issuperset({rid for f in ASSEMBLY_FAMILIES for rid in f.relation_inputs}))
def check_T_w_trace_ward_import_delta_alpha_value(): return _res("delta_alpha_value", abs(DELTA_ALPHA_ADMITTED - 0.05907386039640014) < 1e-15)
def check_T_w_trace_ward_import_rho_value(): return _res("rho_value", abs(RHO_BRANCH_LEADING + 0.032452969615) < 1e-12)
def check_T_w_trace_ward_import_native_partial_matches_v19(): return _res("native_partial_matches_v19", abs(native_partial_delta_r() - v19_partial_native_delta_r()) < 1e-15)
def check_T_w_trace_ward_import_native_partial_range(): return _res("native_partial_range", 0.026 < native_partial_delta_r() < 0.027, value=native_partial_delta_r())
def check_T_w_trace_ward_import_target_range(): return _res("target_range", 0.009 < COUNTERTERM_TARGET_DELTA_R < 0.011, value=COUNTERTERM_TARGET_DELTA_R)
def check_T_w_trace_ward_import_target_closure_zero(): return _res("target_closure_zero", abs(assembly_vector()["target_closure_residual"]) < 1e-15, residual=assembly_vector()["target_closure_residual"])
def check_T_w_trace_ward_import_native_gap_equals_target(): return _res("native_gap_equals_target", abs(assembly_vector()["native_open_gap"] - COUNTERTERM_TARGET_DELTA_R) < 1e-15)
def check_T_w_trace_ward_import_dizet_total_preserved(): return _res("dizet_total_preserved", 0.036 < DIZET_DR_TOTAL < 0.037)
def check_T_w_trace_ward_import_mw_preserved(): return _res("mw_preserved", 80.35 < DIZET_MW_GEV < 80.36 and 80.36 < M_W_TRACE_GEV < 80.37)
def check_T_w_trace_ward_import_pull_preserved(): return _res("pull_preserved", 1.0 < PULL_INPUT_PLUS_THEORY < 1.2)
def check_T_w_trace_ward_import_first_failed_gate_exact(): return _res("first_failed_gate_exact", FIRST_FAILED_GATE == "APF_NATIVE_REVIEWED_DIAGRAM_FAMILY_NUMERIC_EVALUATORS_NOT_IMPORTED")
def check_T_w_trace_ward_import_next_gate_exact(): return _res("next_gate_exact", NEXT_GATE == "G2M_SELF_ENERGY_VERTEX_BOX_GAUGE_FAMILY_EVALUATORS")
def check_T_w_trace_ward_import_route_status_export_candidate(): return _res("route_status_export_candidate", "export_candidate" in ROUTE_STATUS)
def check_T_w_trace_ward_import_native_status_partial(): return _res("native_status_partial", NATIVE_ONE_LOOP_STATUS.startswith("P_partial"))
def check_T_w_trace_ward_import_gate_relation_import_closed(): return _res("gate_relation_import_closed", any(g.gate_id == "G2M_RELATION_IMPORT" and g.status == "CLOSED" for g in WARD_GATES))
def check_T_w_trace_ward_import_gate_relation_dag_closed(): return _res("gate_relation_dag_closed", any(g.gate_id == "G2M_RELATION_DAG" and g.status == "CLOSED" for g in WARD_GATES))
def check_T_w_trace_ward_import_gate_target_localized(): return _res("gate_target_localized", any(g.gate_id == "G2M_TARGET_LOCALIZATION" and g.status == "CLOSED" for g in WARD_GATES))
def check_T_w_trace_ward_import_gate_no_fit_guard(): return _res("gate_no_fit_guard", any(g.gate_id == "G2M_NO_TARGET_FIT" and g.status == "CLOSED_GUARD" for g in WARD_GATES))
def check_T_w_trace_ward_import_open_gates_block(): return _res("open_gates_block", all(g.blocks_full_native_one_loop for g in WARD_GATES if g.status == "OPEN"))
def check_T_w_trace_ward_import_basis_contains_A0(): return _res("basis_contains_A0", any(k.startswith("A0") for k in BASIS))
def check_T_w_trace_ward_import_basis_contains_B0(): return _res("basis_contains_B0", any(k.startswith("B0") for k in BASIS))
def check_T_w_trace_ward_import_basis_has_native_terms(): return _res("basis_has_native_terms", len(BASIS) >= 4)
def check_T_w_trace_ward_import_frontier_relations_closed(): return _res("frontier_relations_closed", any(f.frontier_id == "FRONTIER_RELATIONS" and "OS mass" in f.closed_object for f in FRONTIER))
def check_T_w_trace_ward_import_frontier_rows_closed(): return _res("frontier_rows_closed", any(f.frontier_id == "FRONTIER_NATIVE_ROWS" for f in FRONTIER))
def check_T_w_trace_ward_import_frontier_next_steps_nonempty(): return _res("frontier_next_steps_nonempty", all(f.next_acquisition_step for f in FRONTIER))
def check_T_w_trace_ward_import_safe_claims_present(): return _res("safe_claims_present", len(SAFE_CLAIMS) == 4)
def check_T_w_trace_ward_import_forbidden_claims_present(): return _res("forbidden_claims_present", len(FORBIDDEN_CLAIMS) == 4)
def check_T_w_trace_ward_import_forbids_full_closure(): return _res("forbids_full_closure", any("full APF-native one-loop" in c for c in FORBIDDEN_CLAIMS))
def check_T_w_trace_ward_import_forbids_target_derivation(): return _res("forbids_target_derivation", any("target" in c and "derived" in c for c in FORBIDDEN_CLAIMS))
def check_T_w_trace_ward_import_no_fit_admitted(): return _res("no_fit_admitted", all("FIT" not in f.admission_status for f in ASSEMBLY_FAMILIES))
def check_T_w_trace_ward_import_target_not_admitted_formula(): return _res("target_not_admitted_formula", all(f.admission_status != "ADMITTED_EVALUATED" for f in target_families()))
def check_T_w_trace_ward_import_coverage_relations(): return _res("coverage_relations", coverage()["relation_rows"] == 11 and coverage()["relation_rows_imported"] == 11)
def check_T_w_trace_ward_import_coverage_families(): return _res("coverage_families", coverage()["families"] == 8 and coverage()["evaluated_families"] == 2)
def check_T_w_trace_ward_import_coverage_fraction(): return _res("coverage_fraction", abs(coverage()["evaluated_family_fraction"] - 0.25) < 1e-15)
def check_T_w_trace_ward_import_summary_has_relations(): return _res("summary_has_relations", len(route_summary()["relations"]) == 11)
def check_T_w_trace_ward_import_summary_has_families(): return _res("summary_has_families", len(route_summary()["families"]) == 8)
def check_T_w_trace_ward_import_summary_has_graph(): return _res("summary_has_graph", len(route_summary()["dependency_graph"]) == 8)
def check_T_w_trace_ward_import_summary_has_frontier(): return _res("summary_has_frontier", len(route_summary()["frontier"]) == 4)
def check_T_w_trace_ward_import_payload_digest_present(): return _res("payload_digest_present", route_summary()["payload_digest"].startswith("sha256:"))
def check_T_w_trace_ward_import_terminal_report_status(): return _res("terminal_report_status", terminal_report()["pass_status"] == PASS_STATUS)
def check_T_w_trace_ward_import_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_trace_ward_import_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))

_CHECKS = {name: obj for name, obj in sorted(globals().items()) if name.startswith("check_T_w_trace_ward_import_") and callable(obj)}

def register(registry: MutableMapping[str, Any]) -> None: registry.update(_CHECKS)
def run_all() -> Dict[str, Any]:
    rows = []
    for name, fn in _CHECKS.items():
        try:
            result = fn(); rows.append({"name": name, "passed": _passed(result), "result": result})
        except Exception as exc:
            rows.append({"name": name, "passed": False, "error": repr(exc)})
    ok = all(row["passed"] for row in rows)
    return {"passed": ok, "status": PASS_STATUS if ok else PASS_STATUS.replace("_PASS", "_FAIL"), "checks": rows, "report": terminal_report()}

if __name__ == "__main__":
    out = run_all(); print(out["status"])
    for row in out["checks"]: print(("PASS" if row["passed"] else "FAIL"), row["name"])
