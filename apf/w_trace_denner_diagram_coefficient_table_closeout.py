"""W_TRACE Denner diagram coefficient-table closeout and import contract.

v18.0 (2026-05-09): pushes below the tensor/coefficient scaffold by
turning the vague "reviewed Denner coefficient table" obstruction into a
concrete, machine-checkable import contract.  The module also demonstrates that
numeric projection/fitting over the native scalar/tensor basis can reproduce the
counterterm target algebraically, but quarantines that result as non-physical
and non-evidentiary.  The remaining wall is therefore not algebraic capacity;
it is the reviewed diagram coefficient table and source-formula import.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_tensor_coefficient_map_scaffold import (
    PASS_STATUS as V17_PASS_STATUS,
    STATUS as V17_STATUS,
    BASIS,
    COEFFICIENT_SLOTS,
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

STATUS = "P_w_trace_denner_diagram_coefficient_table_closeout"
VERSION = "v18_0"
PASS_STATUS = "W_TRACE_DENNER_DIAGRAM_COEFFICIENT_TABLE_CLOSEOUT_PASS"
TITLE = "W_TRACE Denner diagram coefficient-table closeout/import contract"
PAYLOAD_ID = "W_TRACE_DENNER_DIAGRAM_COEFFICIENT_TABLE_CLOSEOUT_v18_0"
APF_VERSION = "18.0.0"

ROUTE_STATUS = "P_export_candidate_plus_denner_coefficient_import_contract"
NATIVE_ONE_LOOP_STATUS = "OPEN_SOURCE_FORMULAE_IMPORT_REQUIRED"
FIRST_FAILED_GATE = "APF_NATIVE_REVIEWED_DENNER_SOURCE_FORMULAE_NOT_IMPORTED"
NEXT_GATE = "G2J_REVIEWED_DENNER_SOURCE_FORMULA_IMPORT_AND_ASSEMBLY"

REQUIRED_SOURCE_FIELDS = (
    "source_id", "equation_or_table", "diagram_family", "renormalization_convention",
    "coefficient_expression", "pv_basis_terms", "sign_normalization",
    "gauge_parameter_status", "finite_part_status", "double_count_guard",
)

@dataclass(frozen=True)
class DiagramFamily:
    family_id: str
    physical_role: str
    required_pv_objects: str
    denner_sirlin_role: str
    import_status: str
    blocks_native_one_loop: bool

@dataclass(frozen=True)
class CoefficientImportRow:
    row_id: str
    target_slot: str
    diagram_family: str
    required_fields: Tuple[str, ...]
    admitted_basis_objects: Tuple[str, ...]
    source_formula_status: str
    apf_status: str
    blocks_native_one_loop: bool

@dataclass(frozen=True)
class ImportGate:
    gate_id: str
    status: str
    object: str
    evidence: str
    blocks_native_one_loop: bool

@dataclass(frozen=True)
class ProjectionRow:
    basis_object: str
    basis_value: float
    fitted_coefficient: float
    contribution: float
    admissibility_status: str

DIAGRAM_FAMILIES: Tuple[DiagramFamily, ...] = (
    DiagramFamily("SE_W_TRANSVERSE", "W transverse self-energy at p^2=M_W^2", "A0,B0,B1,B00", "mass counterterm delta M_W^2", "SOURCE_FORMULA_REQUIRED", True),
    DiagramFamily("SE_Z_TRANSVERSE", "Z transverse self-energy at p^2=M_Z^2", "A0,B0,B1,B00", "mass counterterm delta M_Z^2", "SOURCE_FORMULA_REQUIRED", True),
    DiagramFamily("SE_GAMMA_Z_MIX", "gamma-Z mixing and charge/mixing counterterms", "B0 derivatives,B1,B00", "field and charge renormalization", "SOURCE_FORMULA_REQUIRED", True),
    DiagramFamily("VAC_POL_FERMION", "running-alpha vacuum-polarization channel", "B0 derivatives, fermion threshold ledger", "Delta-alpha input/row", "PARTIALLY_ADMITTED_BY_DIZET_DELTA_ALPHA", False),
    DiagramFamily("VERTEX_MU_DECAY", "muon-decay vertex correction", "C0 plus tensor coefficients", "Sirlin/Denner vertex finite part", "SOURCE_FORMULA_REQUIRED", True),
    DiagramFamily("BOX_MU_DECAY", "muon-decay box correction", "D0 plus tensor coefficients", "Sirlin/Denner box finite part", "SOURCE_FORMULA_REQUIRED", True),
    DiagramFamily("TAD_GHOST_GAUGE", "tadpole, ghost, gauge-restoring counterterms", "A0,B0 plus convention terms", "gauge/counterterm closure", "SOURCE_FORMULA_REQUIRED", True),
    DiagramFamily("MIXED_QCD_EW", "mixed QCD/electroweak insertions", "external higher-order rows", "DIZET/ACFW higher-order branch", "IMPLEMENTATION_LOCAL_TARGET_ONLY", True),
)

COEFFICIENT_IMPORT_ROWS: Tuple[CoefficientImportRow, ...] = (
    CoefficientImportRow("R_CT_CHARGE_ALPHA", "CT_CHARGE", "VAC_POL_FERMION", REQUIRED_SOURCE_FIELDS, ("B0_MW_0_MW", "B1_MW_0_MW"), "PARTIAL_DIZET_ROW_PRESENT", "PARTIAL", False),
    CoefficientImportRow("R_CT_RHO_TB", "CT_RHO", "SE_W_TRANSVERSE+SE_Z_TRANSVERSE", REQUIRED_SOURCE_FIELDS, ("A0_MT_over_MT2", "B0_MW_0_MW", "B00_MW_MW_MZ_over_MW2"), "LEADING_NATIVE_PLUS_SOURCE_FORMULA_REQUIRED", "PARTIAL", False),
    CoefficientImportRow("R_CT_MASS_W", "CT_MASS", "SE_W_TRANSVERSE", REQUIRED_SOURCE_FIELDS, ("A0_MW_over_MW2", "B0_MW_0_MW", "B00_MW_0_MW_over_MW2"), "SOURCE_FORMULA_REQUIRED", "OPEN", True),
    CoefficientImportRow("R_CT_MASS_Z", "CT_MASS", "SE_Z_TRANSVERSE", REQUIRED_SOURCE_FIELDS, ("A0_MZ_over_MZ2", "B0_MW_MW_MZ", "B00_MW_MW_MZ_over_MW2"), "SOURCE_FORMULA_REQUIRED", "OPEN", True),
    CoefficientImportRow("R_FIELD_MIX_GZ", "CT_FIELD_MIX", "SE_GAMMA_Z_MIX", REQUIRED_SOURCE_FIELDS, ("B0_MW_0_MW", "B1_MW_0_MW", "B00_MW_0_MW_over_MW2"), "SOURCE_FORMULA_REQUIRED", "OPEN", True),
    CoefficientImportRow("R_VERTEX_MU_DECAY", "VB_MU_DECAY", "VERTEX_MU_DECAY", REQUIRED_SOURCE_FIELDS, ("C0_MW_MW_MW_times_MW2", "B0_MW_0_MW"), "SOURCE_FORMULA_REQUIRED", "OPEN", True),
    CoefficientImportRow("R_BOX_MU_DECAY", "VB_MU_DECAY", "BOX_MU_DECAY", REQUIRED_SOURCE_FIELDS, ("D0_MW_MW_MW_MW_times_MW4", "C0_MW_MW_MW_times_MW2"), "SOURCE_FORMULA_REQUIRED", "OPEN", True),
    CoefficientImportRow("R_TAD_GHOST_GAUGE", "CT_FIELD_MIX", "TAD_GHOST_GAUGE", REQUIRED_SOURCE_FIELDS, ("A0_MW_over_MW2", "A0_MZ_over_MZ2", "B0_ZERO_MW_MW"), "SOURCE_FORMULA_REQUIRED", "OPEN", True),
    CoefficientImportRow("R_MIXED_QCD_EW", "QCD_MIXED", "MIXED_QCD_EW", REQUIRED_SOURCE_FIELDS, tuple(), "DIZET_INTERNAL_TARGET_ONLY", "IMPLEMENTATION_LOCAL_TARGET", True),
)

IMPORT_GATES: Tuple[ImportGate, ...] = (
    ImportGate("G2H_DIAGRAM_FAMILY_ONTOLOGY", "CLOSED", "diagram-family ontology", "W/Z self-energies, gamma-Z mixing, Delta-alpha, vertex, box, tad/ghost/gauge, mixed-QCD families declared", False),
    ImportGate("G2H_IMPORT_ROW_SCHEMA", "CLOSED", "reviewed coefficient row schema", "all rows require source, equation/table, convention, coefficient expression, PV basis, signs, gauge status, finite status, double-count guard", False),
    ImportGate("G2H_SLOT_COVERAGE", "CLOSED", "coefficient slot coverage", "every v17 coefficient slot is mapped to at least one import row", False),
    ImportGate("G2H_TARGET_PROJECTION_QUARANTINE", "CLOSED_GUARD", "numeric target projection", "least-norm basis projection exactly reproduces target but is classified FIT_ONLY_NOT_PROOF", False),
    ImportGate("G2J_SOURCE_FORMULA_IMPORT", "OPEN", "reviewed Denner/Sirlin source formulae", FIRST_FAILED_GATE, True),
    ImportGate("G2J_SIGN_AND_GAUGE_AUDIT", "OPEN", "sign, normalization, gauge-convention audit", "requires imported formulae and benchmark comparison", True),
    ImportGate("G2J_VERTEX_BOX_FULL_KINEMATICS", "OPEN", "full-kinematic vertex/box tensor reduction", "requires source formulae and nonzero external-momentum C/D tensor coefficients", True),
    ImportGate("G2K_NATIVE_ONE_LOOP_DELTA_R", "OPEN", "APF-native one-loop Delta-r closure", "requires all G2J gates", True),
)

SAFE_CLAIMS = (
    "The reviewed Denner coefficient-table obstruction is now a concrete import contract, not an undefined blocker.",
    "Every coefficient slot has an assigned diagram family and required source fields.",
    "Numeric target projection over the APF-owned PV/tensor basis is possible but explicitly quarantined as non-proof.",
    "The W route remains an export candidate through DIZET transport and row covariance while APF-native one-loop derivation awaits reviewed source-formula import.",
)

FORBIDDEN_CLAIMS = (
    "The Denner/Sirlin coefficient formulae have been imported.",
    "The least-norm target projection is a physical diagram coefficient table.",
    "The APF-native full one-loop Delta-r evaluator is closed.",
    "Vertex and box full-kinematic tensor coefficients have been derived.",
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


def diagram_family_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(x) for x in DIAGRAM_FAMILIES)


def coefficient_import_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(x) for x in COEFFICIENT_IMPORT_ROWS)


def import_gate_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(x) for x in IMPORT_GATES)


def basis_vector() -> Tuple[Tuple[str, float], ...]:
    return tuple((k, float(v)) for k, v in sorted(BASIS.items()))


def least_norm_projection_rows() -> Tuple[ProjectionRow, ...]:
    # Algebraic demonstration only: for basis vector b, c = target*b/(b.b)
    # gives dot(c,b)=target.  This is explicitly not an admitted coefficient map.
    vec = basis_vector()
    norm2 = sum(v * v for _, v in vec)
    if norm2 <= 0:
        raise ValueError("empty basis norm")
    rows = []
    for name, value in vec:
        coeff = COUNTERTERM_TARGET_DELTA_R * value / norm2
        rows.append(ProjectionRow(name, value, coeff, coeff * value, "FIT_ONLY_NOT_PROOF"))
    return tuple(rows)


def projection_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(x) for x in least_norm_projection_rows())


def projection_sum() -> float:
    return sum(row.contribution for row in least_norm_projection_rows())


def slot_ids_from_v17() -> Tuple[str, ...]:
    return tuple(sorted(s.slot_id for s in COEFFICIENT_SLOTS))


def slots_covered_by_import_rows() -> Tuple[str, ...]:
    return tuple(sorted(set(r.target_slot for r in COEFFICIENT_IMPORT_ROWS)))


def open_import_rows() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(r) for r in COEFFICIENT_IMPORT_ROWS if r.blocks_native_one_loop)


def target_vector() -> Dict[str, float]:
    return {
        "Delta_alpha": DELTA_ALPHA_ADMITTED,
        "rho_leading_branch": RHO_BRANCH_LEADING,
        "counterterm_target_delta_r": COUNTERTERM_TARGET_DELTA_R,
        "DIZET_delta_r_total": DIZET_DR_TOTAL,
        "reconstructed_total": DELTA_ALPHA_ADMITTED + RHO_BRANCH_LEADING + COUNTERTERM_TARGET_DELTA_R,
        "closure_residual": DELTA_ALPHA_ADMITTED + RHO_BRANCH_LEADING + COUNTERTERM_TARGET_DELTA_R - DIZET_DR_TOTAL,
        "least_norm_projection_sum": projection_sum(),
        "least_norm_projection_residual": projection_sum() - COUNTERTERM_TARGET_DELTA_R,
    }


def route_summary() -> Dict[str, Any]:
    return {
        "title": TITLE,
        "version": VERSION,
        "apf_version": APF_VERSION,
        "dependency": {"module_status": V17_STATUS, "pass_status": V17_PASS_STATUS},
        "route_status": ROUTE_STATUS,
        "native_one_loop_status": NATIVE_ONE_LOOP_STATUS,
        "first_failed_gate": FIRST_FAILED_GATE,
        "next_gate": NEXT_GATE,
        "diagram_families": diagram_family_table(),
        "coefficient_import_rows": coefficient_import_table(),
        "import_gates": import_gate_table(),
        "target_vector": target_vector(),
        "projection_quarantine": projection_table(),
        "open_import_rows": open_import_rows(),
        "export_candidate_state": {"M_W_TRACE_GeV": M_W_TRACE_GEV, "M_W_DIZET_GeV": DIZET_MW_GEV, "DIZET_minus_APF_MeV": DIZET_MINUS_APF_MEV, "sigma_total_MW_MeV": TOTAL_SIGMA_MW_MEV, "pull_sigma": PULL_INPUT_PLUS_THEORY},
        "safe_claims": SAFE_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "payload_digest": _digest([diagram_family_table(), coefficient_import_table(), import_gate_table(), target_vector(), projection_table()]),
    }


def terminal_report() -> Dict[str, Any]:
    return {"status": STATUS, "pass_status": PASS_STATUS, "route_summary": route_summary()}

# checks

def check_T_w_trace_denner_coeff_status_declared(): return _res("status_declared", STATUS.startswith("P_w_trace") and VERSION == "v18_0")
def check_T_w_trace_denner_coeff_dependency_pass(): return _res("dependency_pass", V17_PASS_STATUS.endswith("PASS"))
def check_T_w_trace_denner_coeff_family_count(): return _res("family_count", len(DIAGRAM_FAMILIES) == 8)
def check_T_w_trace_denner_coeff_import_row_count(): return _res("import_row_count", len(COEFFICIENT_IMPORT_ROWS) == 9)
def check_T_w_trace_denner_coeff_gate_count(): return _res("gate_count", len(IMPORT_GATES) == 8)
def check_T_w_trace_denner_coeff_required_fields_count(): return _res("required_fields_count", len(REQUIRED_SOURCE_FIELDS) == 10)
def check_T_w_trace_denner_coeff_required_fields_unique(): return _res("required_fields_unique", len(set(REQUIRED_SOURCE_FIELDS)) == len(REQUIRED_SOURCE_FIELDS))
def check_T_w_trace_denner_coeff_all_rows_have_fields(): return _res("all_rows_have_fields", all(r.required_fields == REQUIRED_SOURCE_FIELDS for r in COEFFICIENT_IMPORT_ROWS))
def check_T_w_trace_denner_coeff_all_rows_have_slots(): return _res("all_rows_have_slots", all(r.target_slot for r in COEFFICIENT_IMPORT_ROWS))
def check_T_w_trace_denner_coeff_v17_slots_covered(): return _res("v17_slots_covered", set(slot_ids_from_v17()).issubset(set(slots_covered_by_import_rows())), v17_slots=slot_ids_from_v17(), covered=slots_covered_by_import_rows())
def check_T_w_trace_denner_coeff_mass_rows_open(): return _res("mass_rows_open", any(r.target_slot == "CT_MASS" and r.apf_status == "OPEN" for r in COEFFICIENT_IMPORT_ROWS))
def check_T_w_trace_denner_coeff_vertex_row_open(): return _res("vertex_row_open", any(r.row_id == "R_VERTEX_MU_DECAY" and r.apf_status == "OPEN" for r in COEFFICIENT_IMPORT_ROWS))
def check_T_w_trace_denner_coeff_box_row_open(): return _res("box_row_open", any(r.row_id == "R_BOX_MU_DECAY" and r.apf_status == "OPEN" for r in COEFFICIENT_IMPORT_ROWS))
def check_T_w_trace_denner_coeff_alpha_partial(): return _res("alpha_partial", any(r.row_id == "R_CT_CHARGE_ALPHA" and r.apf_status == "PARTIAL" for r in COEFFICIENT_IMPORT_ROWS))
def check_T_w_trace_denner_coeff_rho_partial(): return _res("rho_partial", any(r.row_id == "R_CT_RHO_TB" and r.apf_status == "PARTIAL" for r in COEFFICIENT_IMPORT_ROWS))
def check_T_w_trace_denner_coeff_qcd_quarantined(): return _res("qcd_quarantined", any(r.row_id == "R_MIXED_QCD_EW" and r.apf_status == "IMPLEMENTATION_LOCAL_TARGET" for r in COEFFICIENT_IMPORT_ROWS))
def check_T_w_trace_denner_coeff_open_rows_block_native(): return _res("open_rows_block_native", all(r.blocks_native_one_loop for r in COEFFICIENT_IMPORT_ROWS if r.apf_status in ("OPEN", "IMPLEMENTATION_LOCAL_TARGET")))
def check_T_w_trace_denner_coeff_closed_ontology_gate(): return _res("closed_ontology_gate", any(g.gate_id == "G2H_DIAGRAM_FAMILY_ONTOLOGY" and g.status == "CLOSED" for g in IMPORT_GATES))
def check_T_w_trace_denner_coeff_closed_schema_gate(): return _res("closed_schema_gate", any(g.gate_id == "G2H_IMPORT_ROW_SCHEMA" and g.status == "CLOSED" for g in IMPORT_GATES))
def check_T_w_trace_denner_coeff_closed_slot_coverage_gate(): return _res("closed_slot_coverage_gate", any(g.gate_id == "G2H_SLOT_COVERAGE" and g.status == "CLOSED" for g in IMPORT_GATES))
def check_T_w_trace_denner_coeff_projection_guard_closed(): return _res("projection_guard_closed", any(g.gate_id == "G2H_TARGET_PROJECTION_QUARANTINE" and g.status == "CLOSED_GUARD" for g in IMPORT_GATES))
def check_T_w_trace_denner_coeff_source_formula_gate_open(): return _res("source_formula_gate_open", any(g.gate_id == "G2J_SOURCE_FORMULA_IMPORT" and g.status == "OPEN" for g in IMPORT_GATES))
def check_T_w_trace_denner_coeff_sign_gauge_gate_open(): return _res("sign_gauge_gate_open", any(g.gate_id == "G2J_SIGN_AND_GAUGE_AUDIT" and g.status == "OPEN" for g in IMPORT_GATES))
def check_T_w_trace_denner_coeff_vertex_box_gate_open(): return _res("vertex_box_gate_open", any(g.gate_id == "G2J_VERTEX_BOX_FULL_KINEMATICS" and g.status == "OPEN" for g in IMPORT_GATES))
def check_T_w_trace_denner_coeff_native_closure_gate_open(): return _res("native_closure_gate_open", any(g.gate_id == "G2K_NATIVE_ONE_LOOP_DELTA_R" and g.status == "OPEN" for g in IMPORT_GATES))
def check_T_w_trace_denner_coeff_open_gates_block_native(): return _res("open_gates_block_native", all(g.blocks_native_one_loop for g in IMPORT_GATES if g.status == "OPEN"))
def check_T_w_trace_denner_coeff_first_failed_gate_exact(): return _res("first_failed_gate_exact", FIRST_FAILED_GATE == "APF_NATIVE_REVIEWED_DENNER_SOURCE_FORMULAE_NOT_IMPORTED")
def check_T_w_trace_denner_coeff_next_gate_exact(): return _res("next_gate_exact", NEXT_GATE == "G2J_REVIEWED_DENNER_SOURCE_FORMULA_IMPORT_AND_ASSEMBLY")
def check_T_w_trace_denner_coeff_route_export_candidate_preserved(): return _res("route_export_candidate_preserved", "export_candidate" in ROUTE_STATUS)
def check_T_w_trace_denner_coeff_native_status_open(): return _res("native_status_open", NATIVE_ONE_LOOP_STATUS.startswith("OPEN"))
def check_T_w_trace_denner_coeff_target_closure_zero(): return _res("target_closure_zero", abs(target_vector()["closure_residual"]) < 1e-15, residual=target_vector()["closure_residual"])
def check_T_w_trace_denner_coeff_projection_sum_exact(): return _res("projection_sum_exact", abs(target_vector()["least_norm_projection_residual"]) < 1e-15, residual=target_vector()["least_norm_projection_residual"])
def check_T_w_trace_denner_coeff_projection_rows_fit_only(): return _res("projection_rows_fit_only", all(r.admissibility_status == "FIT_ONLY_NOT_PROOF" for r in least_norm_projection_rows()))
def check_T_w_trace_denner_coeff_projection_rows_count(): return _res("projection_rows_count", len(least_norm_projection_rows()) == len(BASIS))
def check_T_w_trace_denner_coeff_projection_has_nonzero_coeffs(): return _res("projection_has_nonzero_coeffs", any(abs(r.fitted_coefficient) > 1e-12 for r in least_norm_projection_rows()))
def check_T_w_trace_denner_coeff_basis_not_empty(): return _res("basis_not_empty", len(BASIS) >= 10)
def check_T_w_trace_denner_coeff_counterterm_target_range(): return _res("counterterm_target_range", 0.009 < COUNTERTERM_TARGET_DELTA_R < 0.011)
def check_T_w_trace_denner_coeff_dizet_total_range(): return _res("dizet_total_range", 0.036 < DIZET_DR_TOTAL < 0.037)
def check_T_w_trace_denner_coeff_mw_residual_preserved(): return _res("mw_residual_preserved", -4.9 < DIZET_MINUS_APF_MEV < -4.7)
def check_T_w_trace_denner_coeff_sigma_preserved(): return _res("sigma_preserved", TOTAL_SIGMA_MW_MEV > 4.0 and 1.0 < PULL_INPUT_PLUS_THEORY < 1.2)
def check_T_w_trace_denner_coeff_safe_claims_present(): return _res("safe_claims_present", len(SAFE_CLAIMS) == 4)
def check_T_w_trace_denner_coeff_forbidden_claims_present(): return _res("forbidden_claims_present", len(FORBIDDEN_CLAIMS) == 4)
def check_T_w_trace_denner_coeff_forbids_projection_as_proof(): return _res("forbids_projection_as_proof", any("least-norm" in c and "physical" in c for c in FORBIDDEN_CLAIMS))
def check_T_w_trace_denner_coeff_forbids_native_closure_claim(): return _res("forbids_native_closure_claim", any("full one-loop" in c for c in FORBIDDEN_CLAIMS))
def check_T_w_trace_denner_coeff_report_has_families(): return _res("report_has_families", len(route_summary()["diagram_families"]) == 8)
def check_T_w_trace_denner_coeff_report_has_import_rows(): return _res("report_has_import_rows", len(route_summary()["coefficient_import_rows"]) == 9)
def check_T_w_trace_denner_coeff_report_has_projection(): return _res("report_has_projection", len(route_summary()["projection_quarantine"]) == len(BASIS))
def check_T_w_trace_denner_coeff_payload_digest_present(): return _res("payload_digest_present", route_summary()["payload_digest"].startswith("sha256:"))
def check_T_w_trace_denner_coeff_no_source_formula_imported(): return _res("no_source_formula_imported", all(r.source_formula_status != "SOURCE_FORMULA_IMPORTED" for r in COEFFICIENT_IMPORT_ROWS))
def check_T_w_trace_denner_coeff_terminal_report_status(): return _res("terminal_report_status", terminal_report()["pass_status"] == PASS_STATUS)
def check_T_w_trace_denner_coeff_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_trace_denner_coeff_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))

_CHECKS = {name: obj for name, obj in sorted(globals().items()) if name.startswith("check_T_w_trace_denner_coeff_") and callable(obj)}

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
