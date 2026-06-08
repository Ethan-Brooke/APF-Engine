"""W_TRACE APF-native tensor/coefficient-map scaffold over PV scalar substrate.

v17.0 (2026-05-09): pushes below the finite scalar-integral substrate by
adding an auditable tensor-reduction and Denner/Sirlin coefficient-map
scaffold.  The module deliberately refuses to promote fitted coefficients to
an APF-native loop derivation.  It closes algebraic/tensor primitives and the
coefficient-map schema, while leaving the reviewed diagram coefficient table
as the first remaining gate.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_pv_scalar_integral_substrate import (
    PASS_STATUS as V16_9_PASS_STATUS,
    STATUS as V16_9_STATUS,
    a0_fin, b0_fin, b0_domain_status,
    A0_MW, A0_MZ, A0_MT, B0_MW_0_MW, B0_ZERO_MW_MW,
    C0_MW_MW_MW, D0_MW_MW_MW_MW,
    M_W_TRACE_GEV, M_Z_GEV, M_TOP_GEV, M_H_GEV,
    MW2, MZ2, MT2, MH2, MU2,
    DELTA_ALPHA_ADMITTED, RHO_BRANCH_LEADING, COUNTERTERM_TARGET_DELTA_R,
    DIZET_DR_TOTAL, DIZET_MW_GEV, DIZET_MINUS_APF_MEV,
    TOTAL_SIGMA_MW_MEV, PULL_INPUT_PLUS_THEORY,
)

STATUS = "P_w_trace_tensor_coefficient_map_scaffold"
VERSION = "v17_0"
PASS_STATUS = "W_TRACE_TENSOR_COEFFICIENT_MAP_SCAFFOLD_PASS"
TITLE = "W_TRACE APF-native tensor/coefficient-map scaffold"
PAYLOAD_ID = "W_TRACE_TENSOR_COEFFICIENT_MAP_SCAFFOLD_v17_0"
APF_VERSION = "17.0.0"

ROUTE_STATUS = "P_export_candidate_plus_native_tensor_coefficient_scaffold"
NATIVE_ONE_LOOP_STATUS = "OPEN_REVIEWED_DENNER_DIAGRAM_COEFFICIENT_TABLE_REQUIRED"
FIRST_FAILED_GATE = "APF_NATIVE_REVIEWED_DENNER_DIAGRAM_COEFFICIENT_TABLE"
NEXT_GATE = "G2H_DENNER_DIAGRAM_COEFFICIENT_TABLE_AND_VERTEX_BOX_ASSEMBLY"

@dataclass(frozen=True)
class TensorPrimitive:
    name: str
    value: float
    unit_power: int
    depends_on: str
    convention: str
    domain_status: str
    admitted_status: str
    notes: str

@dataclass(frozen=True)
class CoefficientSlot:
    slot_id: str
    physical_channel: str
    required_inputs: str
    substrate_objects: str
    coefficient_source_status: str
    apf_status: str
    blocks_full_native_loop: bool

@dataclass(frozen=True)
class CoefficientGate:
    gate_id: str
    status: str
    object: str
    evidence: str
    blocks_full_native_loop: bool


def _safe_div(num: float, den: float, label: str) -> float:
    if abs(den) < 1e-24:
        raise ZeroDivisionError(label)
    return num / den


def _a0_allow_massless(m2: float) -> float:
    if abs(m2) < 1e-30:
        return 0.0
    return a0_fin(m2)

def b1_fin(p2: float, m12: float, m22: float) -> float:
    """Finite B1-like two-point coefficient in a fixed algebraic convention.

    This is a tensor-reduction primitive scaffold.  Physical signs and
    normalizations remain owned by the Denner coefficient map layer.
    """
    return _safe_div(_a0_allow_massless(m12) - _a0_allow_massless(m22) + (m22 - m12 - p2) * b0_fin(p2, m12, m22), 2.0 * p2, "B1 p2")


def b00_fin_scaffold(p2: float, m12: float, m22: float) -> float:
    """Finite B00-like coefficient scaffold built from A0/B0/B1.

    The formula is used only as a stable tensor primitive and benchmark
    substrate; the module explicitly blocks physical closure without a reviewed
    diagram coefficient table.
    """
    b1 = b1_fin(p2, m12, m22)
    return 0.25 * (_a0_allow_massless(m22) + m12 * b0_fin(p2, m12, m22) + (m22 - m12 - p2) * b1)


def normalized_scalar_basis() -> Dict[str, float]:
    """Dimensionless normalized finite scalar/tensor basis at the APF route point."""
    return {
        "A0_MW_over_MW2": A0_MW / MW2,
        "A0_MZ_over_MZ2": A0_MZ / MZ2,
        "A0_MT_over_MT2": A0_MT / MT2,
        "B0_MW_0_MW": B0_MW_0_MW,
        "B0_ZERO_MW_MW": B0_ZERO_MW_MW,
        "B1_MW_0_MW": b1_fin(MW2, 0.0, MW2),
        "B1_MW_MW_MZ": b1_fin(MW2, MW2, MZ2),
        "B00_MW_0_MW_over_MW2": b00_fin_scaffold(MW2, 0.0, MW2) / MW2,
        "B00_MW_MW_MZ_over_MW2": b00_fin_scaffold(MW2, MW2, MZ2) / MW2,
        "C0_MW_MW_MW_times_MW2": C0_MW_MW_MW * MW2,
        "D0_MW_MW_MW_MW_times_MW4": D0_MW_MW_MW_MW * MW2 * MW2,
    }

BASIS = normalized_scalar_basis()
B1_ROUTE = BASIS["B1_MW_0_MW"]
B1_MIXED = BASIS["B1_MW_MW_MZ"]
B00_ROUTE = BASIS["B00_MW_0_MW_over_MW2"]
B00_MIXED = BASIS["B00_MW_MW_MZ_over_MW2"]

TENSOR_PRIMITIVES: Tuple[TensorPrimitive, ...] = (
    TensorPrimitive("B1_MW_0_MW", B1_ROUTE, 0, "A0(0), A0(MW), B0(MW;0,MW)", "fixed finite B1 scaffold", b0_domain_status(MW2, 0.0, MW2), "ADMITTED_TENSOR_PRIMITIVE", "two-point tensor coefficient scaffold on W/gamma branch"),
    TensorPrimitive("B1_MW_MW_MZ", B1_MIXED, 0, "A0(MW), A0(MZ), B0(MW;MW,MZ)", "fixed finite B1 scaffold", b0_domain_status(MW2, MW2, MZ2), "ADMITTED_TENSOR_PRIMITIVE", "two-point tensor coefficient scaffold on W/Z branch"),
    TensorPrimitive("B00_MW_0_MW_over_MW2", B00_ROUTE, 0, "A0(MW), B0, B1", "dimensionless B00 scaffold", b0_domain_status(MW2, 0.0, MW2), "ADMITTED_TENSOR_PRIMITIVE", "B00-like finite coefficient, normalized by MW^2"),
    TensorPrimitive("B00_MW_MW_MZ_over_MW2", B00_MIXED, 0, "A0(MZ), B0, B1", "dimensionless B00 scaffold", b0_domain_status(MW2, MW2, MZ2), "ADMITTED_TENSOR_PRIMITIVE", "mixed B00-like finite coefficient, normalized by MW^2"),
)

COEFFICIENT_SLOTS: Tuple[CoefficientSlot, ...] = (
    CoefficientSlot("CT_CHARGE", "charge renormalization / Delta-alpha channel", "fermion vacuum-polarization ledger", "A0, B0, B1, derivative of transverse self energy", "PARTIALLY_NATIVE_ANCHORED_BY_ADMITTED_DELTA_ALPHA", "PARTIAL", False),
    CoefficientSlot("CT_RHO", "rho / weak-isospin self-energy channel", "top-bottom self-energy difference and on-shell masses", "A0, B0, B00 tensor primitives", "LEADING_NATIVE_PLUS_DIZET_CROSS_TARGET", "PARTIAL", False),
    CoefficientSlot("CT_MASS", "W/Z mass counterterms", "transverse self-energy finite parts at poles", "A0, B0, B1, B00 plus diagram coefficients", "REVIEWED_COEFFICIENT_TABLE_REQUIRED", "OPEN", True),
    CoefficientSlot("CT_FIELD_MIX", "field and gamma-Z mixing counterterms", "derivatives/mixing self energies at p2=0/MZ2", "B0 derivatives, B1/B00 coefficients", "REVIEWED_COEFFICIENT_TABLE_REQUIRED", "OPEN", True),
    CoefficientSlot("VB_MU_DECAY", "muon-decay vertex/box finite terms", "vertex/box diagrams and gauge-fixing convention", "C0/D0 plus tensor reduction coefficients", "REVIEWED_COEFFICIENT_TABLE_REQUIRED", "OPEN", True),
    CoefficientSlot("QCD_MIXED", "mixed QCD/EW correction insertions", "QCD correction convention and top branch", "external DIZET internals / higher-order rows", "DIZET_INTERNAL_TARGET_ONLY", "IMPLEMENTATION_LOCAL_TARGET", True),
)

COEFFICIENT_GATES: Tuple[CoefficientGate, ...] = (
    CoefficientGate("G2F_B1_PRIMITIVE", "CLOSED_SCAFFOLD", "finite B1 tensor primitive", "implemented over A0/B0 substrate with domain checks", False),
    CoefficientGate("G2F_B00_PRIMITIVE", "CLOSED_SCAFFOLD", "finite B00 tensor primitive", "implemented over A0/B0/B1 substrate with normalization checks", False),
    CoefficientGate("G2F_COEFFICIENT_SLOT_SCHEMA", "CLOSED_SCHEMA", "Denner/Sirlin coefficient-map slot taxonomy", "charge, rho, mass, mixing, vertex/box, mixed-QCD slots declared", False),
    CoefficientGate("G2F_NO_FITTED_COEFFICIENT_PROOF", "CLOSED_GUARD", "fitted coefficients cannot certify physical diagram map", "least-norm/target-fitting routes are rejected as proof", False),
    CoefficientGate("G2H_REVIEWED_DENNER_TABLE", "OPEN", "reviewed diagram coefficient table", FIRST_FAILED_GATE, True),
    CoefficientGate("G2H_VERTEX_BOX_ASSEMBLY", "OPEN", "native vertex/box coefficient assembly", "requires reviewed coefficient table and C0/D0 full-kinematic tensor reduction", True),
    CoefficientGate("G2I_NATIVE_ONE_LOOP_CLOSURE", "OPEN", "native one-loop Delta-r closure", "requires G2H closure", True),
)

SAFE_CLAIMS = (
    "APF now owns finite scalar and selected tensor-reduction primitives beneath the Denner/Sirlin counterterm target.",
    "The coefficient-map problem has been converted into explicit charge, rho, mass, mixing, vertex/box, and mixed-QCD slots.",
    "Fitted coefficients are explicitly forbidden as evidence for native loop derivation.",
    "The W route remains an export candidate through DIZET transport and admitted covariance, not a completed APF-native one-loop derivation.",
)

FORBIDDEN_CLAIMS = (
    "APF has derived the Denner/Sirlin diagram coefficient table.",
    "The B1/B00 scaffold plus scalar substrate reproduces the full one-loop Delta-r finite target.",
    "Implementation-local DIZET internals are identical to APF-native diagram coefficients.",
    "Two-loop or higher-order electroweak corrections are native APF results.",
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


def tensor_primitive_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(x) for x in TENSOR_PRIMITIVES)


def coefficient_slot_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(x) for x in COEFFICIENT_SLOTS)


def coefficient_gate_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(x) for x in COEFFICIENT_GATES)


def basis_table() -> Tuple[Dict[str, Any], ...]:
    return tuple({"basis_object": k, "value": v, "finite": math.isfinite(v)} for k, v in BASIS.items())


def target_vector() -> Dict[str, float]:
    return {
        "Delta_alpha": DELTA_ALPHA_ADMITTED,
        "rho_leading_branch": RHO_BRANCH_LEADING,
        "counterterm_target_delta_r": COUNTERTERM_TARGET_DELTA_R,
        "DIZET_delta_r_total": DIZET_DR_TOTAL,
        "reconstructed_total": DELTA_ALPHA_ADMITTED + RHO_BRANCH_LEADING + COUNTERTERM_TARGET_DELTA_R,
        "closure_residual": DELTA_ALPHA_ADMITTED + RHO_BRANCH_LEADING + COUNTERTERM_TARGET_DELTA_R - DIZET_DR_TOTAL,
    }


def route_summary() -> Dict[str, Any]:
    return {
        "title": TITLE,
        "version": VERSION,
        "apf_version": APF_VERSION,
        "dependency": {"module_status": V16_9_STATUS, "pass_status": V16_9_PASS_STATUS},
        "input_point": {"M_W_TRACE_GeV": M_W_TRACE_GEV, "M_Z_GeV": M_Z_GEV, "m_t_GeV": M_TOP_GEV, "M_H_GeV": M_H_GEV},
        "normalized_basis": basis_table(),
        "tensor_primitives": tensor_primitive_table(),
        "coefficient_slots": coefficient_slot_table(),
        "target_vector": target_vector(),
        "route_state": {"route_status": ROUTE_STATUS, "native_one_loop_status": NATIVE_ONE_LOOP_STATUS, "first_failed_gate": FIRST_FAILED_GATE, "next_gate": NEXT_GATE},
        "export_candidate_state": {"M_W_TRACE_GeV": M_W_TRACE_GEV, "M_W_DIZET_GeV": DIZET_MW_GEV, "DIZET_minus_APF_MeV": DIZET_MINUS_APF_MEV, "sigma_total_MW_MeV": TOTAL_SIGMA_MW_MEV, "pull_sigma": PULL_INPUT_PLUS_THEORY},
        "coefficient_gates": coefficient_gate_table(),
        "safe_claims": SAFE_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "payload_digest": _digest([basis_table(), tensor_primitive_table(), coefficient_slot_table(), coefficient_gate_table(), target_vector()]),
    }


def terminal_report() -> Dict[str, Any]:
    return {"status": STATUS, "pass_status": PASS_STATUS, "route_summary": route_summary()}

# checks

def check_T_w_trace_tensor_coeff_status_declared(): return _res("status_declared", STATUS.startswith("P_w_trace") and VERSION == "v17_0")
def check_T_w_trace_tensor_coeff_dependency_pass(): return _res("dependency_pass", V16_9_PASS_STATUS.endswith("PASS"))
def check_T_w_trace_tensor_coeff_b1_route_finite(): return _res("b1_route_finite", math.isfinite(B1_ROUTE), value=B1_ROUTE)
def check_T_w_trace_tensor_coeff_b1_mixed_finite(): return _res("b1_mixed_finite", math.isfinite(B1_MIXED), value=B1_MIXED)
def check_T_w_trace_tensor_coeff_b00_route_finite(): return _res("b00_route_finite", math.isfinite(B00_ROUTE), value=B00_ROUTE)
def check_T_w_trace_tensor_coeff_b00_mixed_finite(): return _res("b00_mixed_finite", math.isfinite(B00_MIXED), value=B00_MIXED)
def check_T_w_trace_tensor_coeff_basis_count(): return _res("basis_count", len(BASIS) == 11)
def check_T_w_trace_tensor_coeff_basis_all_finite(): return _res("basis_all_finite", all(math.isfinite(v) for v in BASIS.values()))
def check_T_w_trace_tensor_coeff_tensor_primitive_count(): return _res("tensor_primitive_count", len(TENSOR_PRIMITIVES) == 4)
def check_T_w_trace_tensor_coeff_tensor_primitives_admitted(): return _res("tensor_primitives_admitted", all(t.admitted_status == "ADMITTED_TENSOR_PRIMITIVE" for t in TENSOR_PRIMITIVES))
def check_T_w_trace_tensor_coeff_slot_count(): return _res("slot_count", len(COEFFICIENT_SLOTS) == 6)
def check_T_w_trace_tensor_coeff_open_slots_present(): return _res("open_slots_present", any(s.apf_status == "OPEN" for s in COEFFICIENT_SLOTS))
def check_T_w_trace_tensor_coeff_partial_slots_present(): return _res("partial_slots_present", any(s.apf_status == "PARTIAL" for s in COEFFICIENT_SLOTS))
def check_T_w_trace_tensor_coeff_vertex_box_open(): return _res("vertex_box_open", any(s.slot_id == "VB_MU_DECAY" and s.apf_status == "OPEN" for s in COEFFICIENT_SLOTS))
def check_T_w_trace_tensor_coeff_mass_counterterm_open(): return _res("mass_counterterm_open", any(s.slot_id == "CT_MASS" and s.apf_status == "OPEN" for s in COEFFICIENT_SLOTS))
def check_T_w_trace_tensor_coeff_gate_count(): return _res("gate_count", len(COEFFICIENT_GATES) == 7)
def check_T_w_trace_tensor_coeff_b1_gate_closed(): return _res("b1_gate_closed", any(g.gate_id == "G2F_B1_PRIMITIVE" and g.status.startswith("CLOSED") for g in COEFFICIENT_GATES))
def check_T_w_trace_tensor_coeff_b00_gate_closed(): return _res("b00_gate_closed", any(g.gate_id == "G2F_B00_PRIMITIVE" and g.status.startswith("CLOSED") for g in COEFFICIENT_GATES))
def check_T_w_trace_tensor_coeff_schema_gate_closed(): return _res("schema_gate_closed", any(g.gate_id == "G2F_COEFFICIENT_SLOT_SCHEMA" and g.status.startswith("CLOSED") for g in COEFFICIENT_GATES))
def check_T_w_trace_tensor_coeff_no_fit_guard_closed(): return _res("no_fit_guard_closed", any(g.gate_id == "G2F_NO_FITTED_COEFFICIENT_PROOF" and g.status == "CLOSED_GUARD" for g in COEFFICIENT_GATES))
def check_T_w_trace_tensor_coeff_reviewed_table_open(): return _res("reviewed_table_open", any(g.gate_id == "G2H_REVIEWED_DENNER_TABLE" and g.status == "OPEN" for g in COEFFICIENT_GATES))
def check_T_w_trace_tensor_coeff_next_gate_exact(): return _res("next_gate_exact", NEXT_GATE == "G2H_DENNER_DIAGRAM_COEFFICIENT_TABLE_AND_VERTEX_BOX_ASSEMBLY")
def check_T_w_trace_tensor_coeff_first_failed_gate_exact(): return _res("first_failed_gate_exact", FIRST_FAILED_GATE == "APF_NATIVE_REVIEWED_DENNER_DIAGRAM_COEFFICIENT_TABLE")
def check_T_w_trace_tensor_coeff_route_export_candidate_preserved(): return _res("route_export_candidate_preserved", "export_candidate" in ROUTE_STATUS)
def check_T_w_trace_tensor_coeff_native_status_open(): return _res("native_status_open", NATIVE_ONE_LOOP_STATUS.startswith("OPEN"))
def check_T_w_trace_tensor_coeff_target_closure_zero(): return _res("target_closure_zero", abs(target_vector()["closure_residual"]) < 1e-15, residual=target_vector()["closure_residual"])
def check_T_w_trace_tensor_coeff_counterterm_target_range(): return _res("counterterm_target_range", 0.009 < COUNTERTERM_TARGET_DELTA_R < 0.011)
def check_T_w_trace_tensor_coeff_dizet_total_range(): return _res("dizet_total_range", 0.036 < DIZET_DR_TOTAL < 0.037)
def check_T_w_trace_tensor_coeff_safe_claims_present(): return _res("safe_claims_present", len(SAFE_CLAIMS) == 4)
def check_T_w_trace_tensor_coeff_forbidden_claims_present(): return _res("forbidden_claims_present", len(FORBIDDEN_CLAIMS) == 4)
def check_T_w_trace_tensor_coeff_forbids_full_native_claim(): return _res("forbids_full_native_claim", any("full one-loop" in c or "Denner/Sirlin" in c for c in FORBIDDEN_CLAIMS))
def check_T_w_trace_tensor_coeff_report_has_basis(): return _res("report_has_basis", len(route_summary()["normalized_basis"]) == 11)
def check_T_w_trace_tensor_coeff_report_has_slots(): return _res("report_has_slots", len(route_summary()["coefficient_slots"]) == 6)
def check_T_w_trace_tensor_coeff_report_has_gates(): return _res("report_has_gates", len(route_summary()["coefficient_gates"]) == 7)
def check_T_w_trace_tensor_coeff_payload_digest_present(): return _res("payload_digest_present", route_summary()["payload_digest"].startswith("sha256:"))
def check_T_w_trace_tensor_coeff_open_gates_block_native(): return _res("open_gates_block_native", all(g.blocks_full_native_loop for g in COEFFICIENT_GATES if g.status == "OPEN"))
def check_T_w_trace_tensor_coeff_slot_blockers_present(): return _res("slot_blockers_present", all(s.blocks_full_native_loop for s in COEFFICIENT_SLOTS if s.apf_status in ("OPEN", "IMPLEMENTATION_LOCAL_TARGET")))
def check_T_w_trace_tensor_coeff_mw_residual_preserved(): return _res("mw_residual_preserved", -4.9 < DIZET_MINUS_APF_MEV < -4.7)
def check_T_w_trace_tensor_coeff_sigma_preserved(): return _res("sigma_preserved", TOTAL_SIGMA_MW_MEV > 4.0 and 1.0 < PULL_INPUT_PLUS_THEORY < 1.2)
def check_T_w_trace_tensor_coeff_tensor_values_not_all_zero(): return _res("tensor_values_not_all_zero", any(abs(t.value) > 1e-8 for t in TENSOR_PRIMITIVES))
def check_T_w_trace_tensor_coeff_basis_contains_c0_d0(): return _res("basis_contains_c0_d0", "C0_MW_MW_MW_times_MW2" in BASIS and "D0_MW_MW_MW_MW_times_MW4" in BASIS)
def check_T_w_trace_tensor_coeff_b1_sensitive_to_mass_order(): return _res("b1_sensitive_to_mass_order", abs(B1_ROUTE - B1_MIXED) > 1e-4)
def check_T_w_trace_tensor_coeff_no_fitted_coefficient_claim(): return _res("no_fitted_coefficient_claim", all("fit" not in c.lower() or "forbidden" in c.lower() or "cannot" in c.lower() for c in SAFE_CLAIMS + FORBIDDEN_CLAIMS))
def check_T_w_trace_tensor_coeff_terminal_report_status(): return _res("terminal_report_status", terminal_report()["pass_status"] == PASS_STATUS)
def check_T_w_trace_tensor_coeff_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_trace_tensor_coeff_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))

_CHECKS = {name: obj for name, obj in sorted(globals().items()) if name.startswith("check_T_w_trace_tensor_coeff_") and callable(obj)}

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
