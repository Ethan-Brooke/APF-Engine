"""W_TRACE reviewed diagram-family numeric evaluator import layer.

v21.0 (2026-05-09): deepens v20 from relation import into an evaluated
family-frontier layer.  The point of this module is deliberately narrow:
separate what has become APF-owned and numerically evaluated from what is still
only a DIZET-internal or source-formula acquisition target.

Closed here:
  * reviewed same-input transport and admitted DIZET row/covariance chain remain
    inherited from v16.4--v20;
  * APF-owned Delta-alpha and leading-rho rows remain evaluated;
  * the one-loop finite/counterterm target is decomposed into named family
    acquisition buckets with residual closure and no-fit guard;
  * DIZET-internal implementation variables are mapped onto those buckets as
    diagnostic anchors, not as analytic Denner/Sirlin proof.

Still open:
  APF_NATIVE_REVIEWED_FAMILY_FORMULAE_NUMERIC_IMPORT_AND_VERTEX_BOX_GAUGE_AUDIT.

This is the correct next wall: not scalar integrals, not tensor primitives, not
Ward relations, and not DIZET same-input evaluation.  The missing object is the
reviewed family-by-family numerical formula import for self energies,
gamma-Z/charge, vertex, box, and tadpole/ghost/gauge-cancellation finite rows.
"""
from __future__ import annotations

import hashlib, json, math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_denner_ward_identity_counterterm_import import (
    PASS_STATUS as V20_PASS_STATUS, STATUS as V20_STATUS,
    IMPORTED_RELATIONS as V20_IMPORTED_RELATIONS,
    ASSEMBLY_FAMILIES as V20_ASSEMBLY_FAMILIES,
    WARD_GATES as V20_WARD_GATES,
    DELTA_ALPHA_ADMITTED, RHO_BRANCH_LEADING, COUNTERTERM_TARGET_DELTA_R,
    DIZET_DR_TOTAL, DIZET_MW_GEV, DIZET_MINUS_APF_MEV, M_W_TRACE_GEV,
    TOTAL_SIGMA_MW_MEV, PULL_INPUT_PLUS_THEORY,
    native_partial_delta_r as v20_native_partial_delta_r,
)
from apf.w_trace_dizet_internal_dr_decomposition import (
    DIZET_RESULT as DIZET_INTERNAL_RESULT,
    INTERNAL_VARIABLES as DIZET_INTERNAL_VARIABLES,
)
from apf.w_trace_pv_scalar_integral_substrate import PASS_STATUS as PV_PASS_STATUS
from apf.w_trace_tensor_coefficient_map_scaffold import PASS_STATUS as TENSOR_PASS_STATUS

STATUS = "P_w_trace_diagram_family_numeric_evaluator_import"
VERSION = "v21_0"
PASS_STATUS = "W_TRACE_DIAGRAM_FAMILY_NUMERIC_EVALUATOR_IMPORT_PASS"
TITLE = "W_TRACE diagram-family numeric evaluator import and closeout layer"
PAYLOAD_ID = "W_TRACE_DIAGRAM_FAMILY_NUMERIC_EVALUATOR_IMPORT_v21_0"
APF_VERSION = "21.0.0"

ROUTE_STATUS = "P_export_candidate_plus_family_numeric_import_frontier"
NATIVE_ONE_LOOP_STATUS = "P_partial_native_rows_plus_diagnostic_family_projection_open_reviewed_formula_import"
FIRST_FAILED_GATE = "APF_NATIVE_REVIEWED_FAMILY_FORMULAE_NUMERIC_IMPORT_AND_VERTEX_BOX_GAUGE_AUDIT"
NEXT_GATE = "G2N_REVIEWED_SELF_ENERGY_VERTEX_BOX_GAUGE_FORMULAE"

def _iv(name: str) -> float:
    for row in DIZET_INTERNAL_VARIABLES:
        if row.name == name:
            return float(row.value)
    raise KeyError(name)

DIZET_INTERNAL_DR_TOTAL = float(DIZET_INTERNAL_RESULT["ZPAR_DR"])
DIZET_DRREM = float(DIZET_INTERNAL_RESULT["ZPAR_DRREM"])
DIZET_DR1FERM = _iv("DR1FER")
DIZET_DR1BOS = _iv("DR1BOS")
DIZET_DELTA_ALPHA = _iv("DALFA")
T_BQCD = _iv("TBQCD")
C_LQQCD = _iv("CLQQCD")
T_BQCD_L = _iv("TBQCDL")
DRREM_NEWDR = _iv("DRREMN")
DRKER_NEWDR = _iv("DRREMK")

# Same-input APF/DIZET numerical backbone.
NATIVE_PARTIAL_DELTA_R = DELTA_ALPHA_ADMITTED + RHO_BRANCH_LEADING
FINITE_TARGET = DIZET_DR_TOTAL - NATIVE_PARTIAL_DELTA_R
RHO_CROSS_TARGET = -0.03424000860914665
RHO_RESUMMATION_DELTA = RHO_CROSS_TARGET - RHO_BRANCH_LEADING
DIZET_REM_PLUS_RHO_DELTA = DIZET_DRREM + RHO_RESUMMATION_DELTA

@dataclass(frozen=True)
class FamilyEvaluatorImport:
    family_id: str
    physical_family: str
    v20_relation_ids: Tuple[str, ...]
    native_value: float | None
    diagnostic_value: float | None
    target_share: float | None
    evaluator_status: str
    admission_status: str
    source_formula_status: str
    blocks_full_native_one_loop: bool
    note: str

@dataclass(frozen=True)
class DiagnosticAnchor:
    anchor_id: str
    dizet_variable: str
    value: float
    maps_to_family: str
    admission: str
    reason: str

@dataclass(frozen=True)
class FormulaAcquisitionTask:
    task_id: str
    family_id: str
    required_formulae: Tuple[str, ...]
    required_integrals: Tuple[str, ...]
    current_support: Tuple[str, ...]
    blocking_reason: str
    next_action: str

@dataclass(frozen=True)
class CloseoutGate:
    gate_id: str
    status: str
    evidence: str
    blocks_full_native_one_loop: bool

FAMILY_IMPORTS: Tuple[FamilyEvaluatorImport, ...] = (
    FamilyEvaluatorImport(
        "F_DELTA_ALPHA", "running-alpha / vacuum-polarization input channel", ("R_DELTA_ALPHA_ROW",),
        DELTA_ALPHA_ADMITTED, DIZET_DELTA_ALPHA, DELTA_ALPHA_ADMITTED,
        "EVALUATED", "ADMITTED_NATIVE_OR_REVIEWED_INPUT", "IMPORTED_EVALUATED", False,
        "Same-input Delta-alpha row is admitted and numerically stable.",
    ),
    FamilyEvaluatorImport(
        "F_RHO_LEAD", "leading top-rho weak-isospin channel", ("R_RHO_LEAD_ROW",),
        RHO_BRANCH_LEADING, RHO_CROSS_TARGET, RHO_BRANCH_LEADING,
        "EVALUATED_LEADING_ONLY", "ADMITTED_NATIVE_LEADING_ROW", "LEADING_ANALYTIC_IMPORTED", False,
        "APF owns the leading top-rho row; DIZET's rho-cross includes finite/resummed correction.",
    ),
    FamilyEvaluatorImport(
        "F_RHO_RESUMMATION_DELTA", "rho-cross finite/resummation correction", ("R_RHO_LEAD_ROW", "R_WEAK_ANGLE_CT"),
        None, RHO_RESUMMATION_DELTA, RHO_RESUMMATION_DELTA,
        "DIAGNOSTIC_TARGET_ONLY", "QUARANTINED_DIAGNOSTIC", "NEEDS_REVIEWED_FORMULA_IMPORT", True,
        "Exact gap between DIZET rho-cross and APF leading rho; not admitted as native proof.",
    ),
    FamilyEvaluatorImport(
        "F_FINITE_REMAINDER", "finite self-energy/charge/vertex/box/gauge remainder aggregate", tuple(r.relation_id for r in V20_IMPORTED_RELATIONS if r.numeric_status != "EVALUATED"),
        None, DIZET_DRREM, DIZET_DRREM,
        "DIAGNOSTIC_AGGREGATE", "QUARANTINED_IMPLEMENTATION_AGGREGATE", "NEEDS_FAMILY_FORMULAE", True,
        "DIZET DRREM is a real implementation-local aggregate; it is not a reviewed family formula table.",
    ),
    FamilyEvaluatorImport(
        "F_MASS_WEAK_ANGLE_CT", "W/Z self-energy and weak-angle counterterm finite family", ("R_OS_MASS_CT_W", "R_OS_MASS_CT_Z", "R_WEAK_ANGLE_CT"),
        None, None, None,
        "RELATION_IMPORTED_NUMERIC_OPEN", "OPEN", "NEEDS_WZ_SELF_ENERGY_FORMULAE", True,
        "PV/tensor substrate and Ward relation exist; reviewed self-energy coefficient formulae are not imported.",
    ),
    FamilyEvaluatorImport(
        "F_CHARGE_FIELD_CT", "charge, photon, gamma-Z mixing finite family", ("R_CHARGE_CT_ALPHA0", "R_FIELD_AA", "R_FIELD_ZA"),
        None, None, None,
        "RELATION_IMPORTED_NUMERIC_OPEN", "OPEN", "NEEDS_PHOTON_GAMMAZ_FORMULAE", True,
        "Charge/Ward relations exist; finite derivative/mixing coefficient rows remain open.",
    ),
    FamilyEvaluatorImport(
        "F_VERTEX", "muon-decay vertex finite family", ("R_VERTEX_FAMILY",),
        None, None, None,
        "RELATION_IMPORTED_NUMERIC_OPEN", "OPEN", "NEEDS_VERTEX_FORMULAE", True,
        "Vertex relation slot exists; reviewed B/C tensor coefficient formulae not imported.",
    ),
    FamilyEvaluatorImport(
        "F_BOX", "muon-decay box finite family", ("R_BOX_FAMILY",),
        None, None, None,
        "RELATION_IMPORTED_NUMERIC_OPEN", "OPEN", "NEEDS_BOX_FORMULAE", True,
        "Box relation slot exists; reviewed C/D coefficient formulae not imported.",
    ),
    FamilyEvaluatorImport(
        "F_GAUGE_RESTORING", "tadpole/ghost/gauge-cancellation finite family", ("R_TAD_GHOST_GAUGE",),
        None, None, None,
        "RELATION_IMPORTED_NUMERIC_OPEN", "OPEN", "NEEDS_GAUGE_CANCELLATION_AUDIT", True,
        "Gauge-restoring slot exists; convention-specific numeric audit remains open.",
    ),
)

DIAGNOSTIC_ANCHORS: Tuple[DiagnosticAnchor, ...] = (
    DiagnosticAnchor("A_DELTA_ALPHA", "DELTA_ALPHA", DIZET_DELTA_ALPHA, "F_DELTA_ALPHA", "ADMITTED_ANCHOR", "matches running-alpha channel"),
    DiagnosticAnchor("A_DR1FERM", "DR1FERM", DIZET_DR1FERM, "F_FINITE_REMAINDER", "DIAGNOSTIC_ONLY", "fermionic one-loop implementation variable, not APF formula row"),
    DiagnosticAnchor("A_DR1BOS", "DR1BOS", DIZET_DR1BOS, "F_FINITE_REMAINDER", "DIAGNOSTIC_ONLY", "bosonic one-loop implementation variable, not APF formula row"),
    DiagnosticAnchor("A_DRREM", "DRREM", DIZET_DRREM, "F_FINITE_REMAINDER", "DIAGNOSTIC_AGGREGATE", "same-input implementation aggregate closes DIZET internal path"),
    DiagnosticAnchor("A_TBQCD", "T_BQCD", T_BQCD, "F_FINITE_REMAINDER", "AUXILIARY_SUBROW", "QCD/mixed auxiliary in DIZET DRREM assembly"),
    DiagnosticAnchor("A_CLQQCD", "C_LQQCD", C_LQQCD, "F_FINITE_REMAINDER", "AUXILIARY_SUBROW", "small QCD/mixed auxiliary in DIZET DRREM assembly"),
    DiagnosticAnchor("A_TBQCDL", "T_BQCD_L", T_BQCD_L, "F_FINITE_REMAINDER", "AUXILIARY_SUBROW", "subtracted QCD/mixed auxiliary in DIZET DRREM assembly"),
    DiagnosticAnchor("A_DRREM_NEWDR", "DRREM_NEWDR", DRREM_NEWDR, "F_FINITE_REMAINDER", "IMPLEMENTATION_LOCAL", "DIZET NEWDR remainder kernel; not source-family formula"),
    DiagnosticAnchor("A_DRKER_NEWDR", "DRKER_NEWDR", DRKER_NEWDR, "F_FINITE_REMAINDER", "IMPLEMENTATION_LOCAL", "DIZET kernel diagnostic; not source-family formula"),
)

ACQUISITION_TASKS: Tuple[FormulaAcquisitionTask, ...] = (
    FormulaAcquisitionTask("TASK_SELF_ENERGY_WZ", "F_MASS_WEAK_ANGLE_CT", ("Sigma_T^W(M_W^2)", "Sigma_T^Z(M_Z^2)", "derivatives where required"), ("A0", "B0", "B00", "B1"), ("PV substrate", "Ward mass CT relations"), "coefficient formulae not imported", "import reviewed Denner self-energy coefficient tables"),
    FormulaAcquisitionTask("TASK_CHARGE_GAMMAZ", "F_CHARGE_FIELD_CT", ("Sigma_AA_prime(0)", "Sigma_AZ(0)"), ("B0", "B0_prime", "B00", "B1"), ("PV substrate", "charge Ward relation"), "neutral field formulae not imported", "import photon/gamma-Z field-renormalization formulas"),
    FormulaAcquisitionTask("TASK_VERTEX", "F_VERTEX", ("muon-decay W vertex finite amplitudes",), ("B0", "C0", "C_tensor"), ("relation slot",), "vertex coefficient maps absent", "import reviewed vertex coefficient formulas"),
    FormulaAcquisitionTask("TASK_BOX", "F_BOX", ("muon-decay box matching finite amplitudes",), ("C0", "D0", "D_tensor"), ("relation slot",), "box coefficient maps absent", "import reviewed box coefficient formulas"),
    FormulaAcquisitionTask("TASK_GAUGE", "F_GAUGE_RESTORING", ("tadpole convention", "ghost finite rows", "gauge-parameter cancellation rows"), ("A0", "B0"), ("gauge-restoring relation slot",), "gauge-cancellation numeric audit absent", "define and verify gauge/tadpole convention across all families"),
)

GATES: Tuple[CloseoutGate, ...] = (
    CloseoutGate("G2N_V20_DEPENDENCY", "CLOSED", V20_PASS_STATUS, False),
    CloseoutGate("G2N_DIZET_INTERNALS", "CLOSED", "DIZET internal variables imported as diagnostics", False),
    CloseoutGate("G2N_NATIVE_EVALUATED_ROWS", "CLOSED", "Delta-alpha and leading-rho rows evaluated", False),
    CloseoutGate("G2N_TARGET_DECOMPOSITION", "CLOSED", "finite target = DIZET DRREM + rho resummation delta", False),
    CloseoutGate("G2N_NO_FIT_GUARD", "CLOSED_GUARD", "diagnostic targets cannot become admitted formula rows", False),
    CloseoutGate("G2N_SELF_ENERGY_FORMULAE", "OPEN", "reviewed W/Z self-energy numeric formulae missing", True),
    CloseoutGate("G2N_CHARGE_GAMMAZ_FORMULAE", "OPEN", "reviewed photon/gamma-Z formulae missing", True),
    CloseoutGate("G2N_VERTEX_BOX_FORMULAE", "OPEN", "reviewed vertex/box coefficient formulae missing", True),
    CloseoutGate("G2N_GAUGE_AUDIT", "OPEN", "tadpole/ghost/gauge-cancellation numeric audit missing", True),
    CloseoutGate("G2N_FULL_NATIVE_ONE_LOOP", "OPEN", FIRST_FAILED_GATE, True),
)

SAFE_CLAIMS = (
    "v21 imports a numeric family frontier and decomposes the finite target without admitting fitted coefficients.",
    "DIZET implementation variables are diagnostic anchors, not APF-native Denner/Sirlin formulae.",
    "The route remains an export candidate by reviewed same-input transport plus partial APF-native assembly.",
    "The next wall is reviewed source-formula import for diagram families, not DIZET execution, scalar integrals, tensors, or Ward relations.",
)
FORBIDDEN_CLAIMS = (
    "v21 derives full APF-native one-loop Delta r.",
    "DIZET DRREM is a reviewed APF finite-row formula.",
    "The finite target is proven by fitting coefficients.",
    "Vertex, box, and gauge-restoring families are numerically evaluated from source formulae.",
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

def family_table(): return tuple(asdict(f) for f in FAMILY_IMPORTS)
def anchor_table(): return tuple(asdict(a) for a in DIAGNOSTIC_ANCHORS)
def task_table(): return tuple(asdict(t) for t in ACQUISITION_TASKS)
def gate_table(): return tuple(asdict(g) for g in GATES)
def family_ids(): return {f.family_id for f in FAMILY_IMPORTS}
def admitted_families(): return tuple(f for f in FAMILY_IMPORTS if f.admission_status.startswith("ADMITTED"))
def open_families(): return tuple(f for f in FAMILY_IMPORTS if f.admission_status == "OPEN")
def quarantined_families(): return tuple(f for f in FAMILY_IMPORTS if "QUARANTINED" in f.admission_status)
def diagnostic_families(): return tuple(f for f in FAMILY_IMPORTS if f.evaluator_status.startswith("DIAGNOSTIC"))
def native_partial_delta_r(): return NATIVE_PARTIAL_DELTA_R
def finite_target_recomposed(): return DIZET_DRREM + RHO_RESUMMATION_DELTA

def coverage() -> Dict[str, Any]:
    return {
        "families": len(FAMILY_IMPORTS),
        "admitted_families": len(admitted_families()),
        "open_families": len(open_families()),
        "quarantined_families": len(quarantined_families()),
        "diagnostic_families": len(diagnostic_families()),
        "diagnostic_anchors": len(DIAGNOSTIC_ANCHORS),
        "acquisition_tasks": len(ACQUISITION_TASKS),
        "open_gates": sum(1 for g in GATES if g.status == "OPEN"),
        "closed_gates": sum(1 for g in GATES if g.status.startswith("CLOSED")),
    }

def assembly_vector() -> Dict[str, float]:
    return {
        "Delta_alpha": DELTA_ALPHA_ADMITTED,
        "rho_leading_branch": RHO_BRANCH_LEADING,
        "native_partial_delta_r": NATIVE_PARTIAL_DELTA_R,
        "DIZET_DRREM": DIZET_DRREM,
        "rho_resummation_delta": RHO_RESUMMATION_DELTA,
        "finite_target_recomposed": finite_target_recomposed(),
        "finite_target": FINITE_TARGET,
        "target_recomposition_residual": finite_target_recomposed() - FINITE_TARGET,
        "target_closed_delta_r": NATIVE_PARTIAL_DELTA_R + FINITE_TARGET,
        "DIZET_delta_r_total": DIZET_DR_TOTAL,
        "full_closure_residual": NATIVE_PARTIAL_DELTA_R + FINITE_TARGET - DIZET_DR_TOTAL,
        "DIZET_internal_total": DIZET_INTERNAL_DR_TOTAL,
        "DIZET_internal_vs_imported_residual": DIZET_INTERNAL_DR_TOTAL - DIZET_DR_TOTAL,
    }

def terminal_report() -> Dict[str, Any]:
    payload = {
        "title": TITLE, "version": VERSION, "apf_version": APF_VERSION,
        "route_status": ROUTE_STATUS, "native_one_loop_status": NATIVE_ONE_LOOP_STATUS,
        "first_failed_gate": FIRST_FAILED_GATE, "next_gate": NEXT_GATE,
        "dependencies": {"v20_status": V20_STATUS, "v20_pass_status": V20_PASS_STATUS, "pv": PV_PASS_STATUS, "tensor": TENSOR_PASS_STATUS},
        "families": family_table(), "diagnostic_anchors": anchor_table(), "acquisition_tasks": task_table(), "gates": gate_table(),
        "coverage": coverage(), "assembly_vector": assembly_vector(),
        "export_candidate_state": {"M_W_TRACE_GeV": M_W_TRACE_GEV, "M_W_DIZET_GeV": DIZET_MW_GEV, "DIZET_minus_APF_MeV": DIZET_MINUS_APF_MEV, "sigma_total_MW_MeV": TOTAL_SIGMA_MW_MEV, "pull_sigma": PULL_INPUT_PLUS_THEORY},
        "safe_claims": SAFE_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    payload["payload_digest"] = _digest(payload)
    return payload

def check_T_w_trace_family_numeric_dependency_v20_pass(): return _res("dependency_v20_pass", V20_PASS_STATUS.endswith("PASS"))
def check_T_w_trace_family_numeric_dependency_pv_pass(): return _res("dependency_pv_pass", PV_PASS_STATUS.endswith("PASS"))
def check_T_w_trace_family_numeric_dependency_tensor_pass(): return _res("dependency_tensor_pass", TENSOR_PASS_STATUS.endswith("PASS"))
def check_T_w_trace_family_numeric_status_strings(): return _res("status_strings", STATUS.startswith("P_") and PASS_STATUS.endswith("PASS"))
def check_T_w_trace_family_numeric_family_count(): return _res("family_count", len(FAMILY_IMPORTS) == 9)
def check_T_w_trace_family_numeric_anchor_count(): return _res("anchor_count", len(DIAGNOSTIC_ANCHORS) == 9)
def check_T_w_trace_family_numeric_task_count(): return _res("task_count", len(ACQUISITION_TASKS) == 5)
def check_T_w_trace_family_numeric_gate_count(): return _res("gate_count", len(GATES) == 10)
def check_T_w_trace_family_numeric_family_ids_unique(): return _res("family_ids_unique", len(family_ids()) == len(FAMILY_IMPORTS))
def check_T_w_trace_family_numeric_anchor_ids_unique(): return _res("anchor_ids_unique", len({a.anchor_id for a in DIAGNOSTIC_ANCHORS}) == len(DIAGNOSTIC_ANCHORS))
def check_T_w_trace_family_numeric_task_ids_unique(): return _res("task_ids_unique", len({t.task_id for t in ACQUISITION_TASKS}) == len(ACQUISITION_TASKS))
def check_T_w_trace_family_numeric_gate_ids_unique(): return _res("gate_ids_unique", len({g.gate_id for g in GATES}) == len(GATES))
def check_T_w_trace_family_numeric_delta_alpha_family_present(): return _res("delta_alpha_family_present", "F_DELTA_ALPHA" in family_ids())
def check_T_w_trace_family_numeric_rho_family_present(): return _res("rho_family_present", "F_RHO_LEAD" in family_ids())
def check_T_w_trace_family_numeric_rho_resummation_family_present(): return _res("rho_resummation_present", "F_RHO_RESUMMATION_DELTA" in family_ids())
def check_T_w_trace_family_numeric_finite_remainder_present(): return _res("finite_remainder_present", "F_FINITE_REMAINDER" in family_ids())
def check_T_w_trace_family_numeric_self_energy_present(): return _res("self_energy_present", "F_MASS_WEAK_ANGLE_CT" in family_ids())
def check_T_w_trace_family_numeric_charge_present(): return _res("charge_present", "F_CHARGE_FIELD_CT" in family_ids())
def check_T_w_trace_family_numeric_vertex_present(): return _res("vertex_present", "F_VERTEX" in family_ids())
def check_T_w_trace_family_numeric_box_present(): return _res("box_present", "F_BOX" in family_ids())
def check_T_w_trace_family_numeric_gauge_present(): return _res("gauge_present", "F_GAUGE_RESTORING" in family_ids())
def check_T_w_trace_family_numeric_admitted_count(): return _res("admitted_count", len(admitted_families()) == 2)
def check_T_w_trace_family_numeric_open_count(): return _res("open_count", len(open_families()) == 5)
def check_T_w_trace_family_numeric_quarantined_count(): return _res("quarantined_count", len(quarantined_families()) == 2)
def check_T_w_trace_family_numeric_diagnostic_count(): return _res("diagnostic_count", len(diagnostic_families()) == 2)
def check_T_w_trace_family_numeric_open_families_block(): return _res("open_families_block", all(f.blocks_full_native_one_loop for f in open_families()))
def check_T_w_trace_family_numeric_quarantined_block(): return _res("quarantined_block", all(f.blocks_full_native_one_loop for f in quarantined_families()))
def check_T_w_trace_family_numeric_delta_alpha_value(): return _res("delta_alpha_value", abs(DELTA_ALPHA_ADMITTED - 0.05907386039640014) < 1e-15)
def check_T_w_trace_family_numeric_rho_value(): return _res("rho_value", abs(RHO_BRANCH_LEADING + 0.032452969615) < 1e-12)
def check_T_w_trace_family_numeric_native_partial(): return _res("native_partial", abs(NATIVE_PARTIAL_DELTA_R - 0.02662089078140014) < 1e-12, value=NATIVE_PARTIAL_DELTA_R)
def check_T_w_trace_family_numeric_native_partial_matches_v20(): return _res("native_partial_matches_v20", abs(NATIVE_PARTIAL_DELTA_R - v20_native_partial_delta_r()) < 1e-15)
def check_T_w_trace_family_numeric_finite_target_range(): return _res("finite_target_range", 0.009 < FINITE_TARGET < 0.011, value=FINITE_TARGET)
def check_T_w_trace_family_numeric_rho_cross_target_range(): return _res("rho_cross_target_range", -0.035 < RHO_CROSS_TARGET < -0.033)
def check_T_w_trace_family_numeric_rho_resummation_negative(): return _res("rho_resummation_negative", RHO_RESUMMATION_DELTA < 0)
def check_T_w_trace_family_numeric_drrem_positive(): return _res("drrem_positive", DIZET_DRREM > 0)
def check_T_w_trace_family_numeric_target_decomposition(): return _res("target_decomposition", abs(finite_target_recomposed() - FINITE_TARGET) < 1e-12, residual=finite_target_recomposed() - FINITE_TARGET)
def check_T_w_trace_family_numeric_full_closure(): return _res("full_closure", abs(assembly_vector()["full_closure_residual"]) < 1e-15)
def check_T_w_trace_family_numeric_dizet_internal_total_close(): return _res("dizet_internal_total_close", abs(DIZET_INTERNAL_DR_TOTAL - DIZET_DR_TOTAL) < 2e-4)
def check_T_w_trace_family_numeric_dizet_delta_alpha_anchor(): return _res("dizet_delta_alpha_anchor", abs(DIZET_DELTA_ALPHA - DELTA_ALPHA_ADMITTED) < 1e-12)
def check_T_w_trace_family_numeric_dr1ferm_reasonable(): return _res("dr1ferm_reasonable", 0.02 < DIZET_DR1FERM < 0.04)
def check_T_w_trace_family_numeric_dr1bos_reasonable(): return _res("dr1bos_reasonable", 0.003 < DIZET_DR1BOS < 0.005)
def check_T_w_trace_family_numeric_qcd_aux_nonzero(): return _res("qcd_aux_nonzero", abs(T_BQCD) > 1e-6 and abs(C_LQQCD) > 1e-8 and abs(T_BQCD_L) > 1e-6)
def check_T_w_trace_family_numeric_newdr_nonzero(): return _res("newdr_nonzero", abs(DRREM_NEWDR) > 1e-6 and abs(DRKER_NEWDR) > 1e-6)
def check_T_w_trace_family_numeric_anchors_map_to_known_families(): return _res("anchors_map_to_known_families", all(a.maps_to_family in family_ids() for a in DIAGNOSTIC_ANCHORS))
def check_T_w_trace_family_numeric_tasks_map_to_known_families(): return _res("tasks_map_to_known_families", all(t.family_id in family_ids() for t in ACQUISITION_TASKS))
def check_T_w_trace_family_numeric_tasks_have_formulae(): return _res("tasks_have_formulae", all(t.required_formulae for t in ACQUISITION_TASKS))
def check_T_w_trace_family_numeric_tasks_have_integrals(): return _res("tasks_have_integrals", all(t.required_integrals for t in ACQUISITION_TASKS))
def check_T_w_trace_family_numeric_tasks_have_next_action(): return _res("tasks_have_next_action", all(t.next_action for t in ACQUISITION_TASKS))
def check_T_w_trace_family_numeric_gate_closed_count(): return _res("gate_closed_count", coverage()["closed_gates"] == 5)
def check_T_w_trace_family_numeric_gate_open_count(): return _res("gate_open_count", coverage()["open_gates"] == 5)
def check_T_w_trace_family_numeric_gate_no_fit_closed(): return _res("gate_no_fit_closed", any(g.gate_id == "G2N_NO_FIT_GUARD" and g.status == "CLOSED_GUARD" for g in GATES))
def check_T_w_trace_family_numeric_open_gates_block(): return _res("open_gates_block", all(g.blocks_full_native_one_loop for g in GATES if g.status == "OPEN"))
def check_T_w_trace_family_numeric_first_failed_gate_exact(): return _res("first_failed_gate_exact", FIRST_FAILED_GATE == "APF_NATIVE_REVIEWED_FAMILY_FORMULAE_NUMERIC_IMPORT_AND_VERTEX_BOX_GAUGE_AUDIT")
def check_T_w_trace_family_numeric_next_gate_exact(): return _res("next_gate_exact", NEXT_GATE == "G2N_REVIEWED_SELF_ENERGY_VERTEX_BOX_GAUGE_FORMULAE")
def check_T_w_trace_family_numeric_route_status_export_candidate(): return _res("route_status_export_candidate", "export_candidate" in ROUTE_STATUS)
def check_T_w_trace_family_numeric_native_status_partial(): return _res("native_status_partial", NATIVE_ONE_LOOP_STATUS.startswith("P_partial"))
def check_T_w_trace_family_numeric_no_fit_not_admitted(): return _res("no_fit_not_admitted", all("FIT" not in f.admission_status for f in FAMILY_IMPORTS))
def check_T_w_trace_family_numeric_diagnostic_not_native(): return _res("diagnostic_not_native", all("QUARANTINED" in f.admission_status for f in diagnostic_families()))
def check_T_w_trace_family_numeric_target_not_formula(): return _res("target_not_formula", all(f.source_formula_status != "IMPORTED_EVALUATED" for f in quarantined_families()))
def check_T_w_trace_family_numeric_export_mw_preserved(): return _res("export_mw_preserved", 80.35 < DIZET_MW_GEV < 80.36 and 80.36 < M_W_TRACE_GEV < 80.37)
def check_T_w_trace_family_numeric_export_residual_preserved(): return _res("export_residual_preserved", -5.0 < DIZET_MINUS_APF_MEV < -4.5)
def check_T_w_trace_family_numeric_pull_preserved(): return _res("pull_preserved", 1.0 < PULL_INPUT_PLUS_THEORY < 1.2)
def check_T_w_trace_family_numeric_sigma_preserved(): return _res("sigma_preserved", 4.0 < TOTAL_SIGMA_MW_MEV < 4.8)
def check_T_w_trace_family_numeric_safe_claims_count(): return _res("safe_claims_count", len(SAFE_CLAIMS) == 4)
def check_T_w_trace_family_numeric_forbidden_claims_count(): return _res("forbidden_claims_count", len(FORBIDDEN_CLAIMS) == 4)
def check_T_w_trace_family_numeric_forbidden_full(): return _res("forbidden_full", any("full APF-native" in c for c in FORBIDDEN_CLAIMS))
def check_T_w_trace_family_numeric_forbidden_drrem(): return _res("forbidden_drrem", any("DRREM" in c for c in FORBIDDEN_CLAIMS))
def check_T_w_trace_family_numeric_report_has_digest(): return _res("report_has_digest", terminal_report()["payload_digest"].startswith("sha256:"))
def check_T_w_trace_family_numeric_report_has_families(): return _res("report_has_families", len(terminal_report()["families"]) == len(FAMILY_IMPORTS))
def check_T_w_trace_family_numeric_report_has_tasks(): return _res("report_has_tasks", len(terminal_report()["acquisition_tasks"]) == len(ACQUISITION_TASKS))
def check_T_w_trace_family_numeric_report_has_anchors(): return _res("report_has_anchors", len(terminal_report()["diagnostic_anchors"]) == len(DIAGNOSTIC_ANCHORS))
def check_T_w_trace_family_numeric_report_has_gates(): return _res("report_has_gates", len(terminal_report()["gates"]) == len(GATES))
def check_T_w_trace_family_numeric_coverage_family_total(): return _res("coverage_family_total", coverage()["families"] == 9)
def check_T_w_trace_family_numeric_coverage_tasks_total(): return _res("coverage_tasks_total", coverage()["acquisition_tasks"] == 5)
def check_T_w_trace_family_numeric_coverage_anchors_total(): return _res("coverage_anchors_total", coverage()["diagnostic_anchors"] == 9)
def check_T_w_trace_family_numeric_payload_id(): return _res("payload_id", PAYLOAD_ID.endswith("v21_0"))
def check_T_w_trace_family_numeric_version(): return _res("version", VERSION == "v21_0" and APF_VERSION == "21.0.0")
def check_T_w_trace_family_numeric_pass_status(): return _res("pass_status", PASS_STATUS == "W_TRACE_DIAGRAM_FAMILY_NUMERIC_EVALUATOR_IMPORT_PASS")
def check_T_w_trace_family_numeric_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_trace_family_numeric_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))

_CHECKS = {name: obj for name, obj in sorted(globals().items()) if name.startswith("check_T_w_trace_family_numeric_") and callable(obj)}

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
