"""W_TRACE APF-native finite-remainder evaluator target and closure map.

v16.7 (2026-05-09): pushes beyond the leading one-loop skeleton.  The
module does not pretend to derive the complete Denner/DIZET finite one-loop
counterterm stack.  It closes the next useful layer: an APF-owned target
functional for the missing finite remainder, an admitted DIZET same-input
finite-remainder realization, a row-wise covariance bridge, and a precise
native-derivation blocker.

Conceptually:

    Delta r_DIZET = Delta alpha + rho_cross + DRREM
    Delta r_skel  = Delta alpha + rho_top_leading

so the finite/native gap is

    Delta r_req = Delta r_DIZET - Delta r_skel
                = DRREM + (rho_cross - rho_top_leading).

This is now an exact audited same-input target for the APF-native finite
counterterm theorem.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_apf_native_one_loop_evaluator import (
    PASS_STATUS as V16_6_PASS_STATUS,
    M_Z_GEV, M_TOP_GEV, M_H_GEV, ALPHA_S_MZ, G_F_GEV_MINUS2,
    S2_APF_TRACE, C2_APF_TRACE, C2_OVER_S2_APF_TRACE,
    DELTA_ALPHA_ADMITTED, DELTA_RHO_TOP_LEADING, RHO_BRANCH_LEADING,
    DELTA_R_ONE_LOOP_SKELETON, DIZET_DR_TOTAL, DIZET_FINITE_REMAINDER,
    DIZET_RHO_CROSS, SKELETON_TO_DIZET_RESIDUAL,
    RHO_RESUMMATION_GAP, RESIDUAL_RECOMPOSED, RESIDUAL_RECOMPOSITION_ERROR,
    DMDDELTA_R_GEV, DIZET_MW_GEV, M_W_TRACE_GEV, DIZET_MINUS_APF_MEV,
    TOTAL_SIGMA_MW_MEV, PULL_INPUT_PLUS_THEORY,
)
from apf.w_trace_dizet_row_admission_covariance import (
    PASS_STATUS as V16_4_PASS_STATUS,
    ADMITTED_ROWS as V16_4_ADMITTED_ROWS,
    ROW_COVARIANCE as V16_4_ROW_COVARIANCE,
    INPUT_SIGMA_DELTA_R as V16_4_INPUT_SIGMA_DELTA_R,
    INPUT_SIGMA_MW_MEV as V16_4_INPUT_SIGMA_MW_MEV,
    THEORY_SIGMA_MW_MEV as V16_4_THEORY_SIGMA_MW_MEV,
)

STATUS = "P_w_trace_native_finite_remainder_evaluator_target"
VERSION = "v16_7"
PASS_STATUS = "W_TRACE_NATIVE_FINITE_REMAINDER_EVALUATOR_TARGET_PASS"
TITLE = "W_TRACE APF-native finite-remainder evaluator target and closure map"
PAYLOAD_ID = "W_TRACE_NATIVE_FINITE_REMAINDER_EVALUATOR_TARGET_v16_7"
APF_VERSION = "16.7.0"

ROUTE_STATUS = "P_export_candidate_plus_native_finite_remainder_target"
NATIVE_FINITE_STATUS = "P_target_functional_and_reviewed_code_realization_not_APF_native_derivation"
FULL_NATIVE_ONE_LOOP_STATUS = "OPEN_COUNTERTERM_FUNCTIONS_NOT_YET_DERIVED"
FIRST_FAILED_GATE = "APF_NATIVE_DENNER_COUNTERTERM_FUNCTIONAL_EVALUATOR"
NEXT_GATE = "G2C_NATIVE_COUNTERTERM_MASTER_FUNCTIONS"

# Exact same-input finite target from v16.6/v16.4.
FINITE_TARGET_DELTA_R = SKELETON_TO_DIZET_RESIDUAL
FINITE_TARGET_MW_MEV = -FINITE_TARGET_DELTA_R * DMDDELTA_R_GEV * 1000.0
FINITE_TARGET_RECOMPOSED = DIZET_FINITE_REMAINDER + RHO_RESUMMATION_GAP
FINITE_TARGET_ERROR = FINITE_TARGET_DELTA_R - FINITE_TARGET_RECOMPOSED

# Admitted target pieces.
DRREM_MW_MEV = -DIZET_FINITE_REMAINDER * DMDDELTA_R_GEV * 1000.0
RHO_RESUM_GAP_MW_MEV = -RHO_RESUMMATION_GAP * DMDDELTA_R_GEV * 1000.0

# A useful dimensionless compactness diagnostic: how much of total Delta r is
# already captured by the leading skeleton.
SKELETON_FRACTION_OF_TOTAL = DELTA_R_ONE_LOOP_SKELETON / DIZET_DR_TOTAL
FINITE_FRACTION_OF_TOTAL = FINITE_TARGET_DELTA_R / DIZET_DR_TOTAL

@dataclass(frozen=True)
class FinitePiece:
    piece_id: str
    symbol: str
    value_delta_r: float
    value_mw_mev: float
    admission: str
    apf_native_status: str
    interpretation: str

FINITE_PIECES: Tuple[FinitePiece, ...] = (
    FinitePiece(
        "F1_DRREM",
        "Delta r_rem^DIZET",
        DIZET_FINITE_REMAINDER,
        DRREM_MW_MEV,
        "ADMITTED_SAME_INPUT_DIZET_ROW",
        "TARGET_REALIZATION_NOT_DERIVED",
        "finite electroweak remainder channel admitted by v16.4 row ledger",
    ),
    FinitePiece(
        "F2_RHO_RESUMMATION_GAP",
        "Delta r_rho^DIZET - Delta r_rho^lead",
        RHO_RESUMMATION_GAP,
        RHO_RESUM_GAP_MW_MEV,
        "ADMITTED_DIFFERENCE_ROW",
        "TARGET_REALIZATION_NOT_DERIVED",
        "resummation/cross gap between leading APF rho row and DIZET rho-cross row",
    ),
    FinitePiece(
        "F3_TOTAL_NATIVE_TARGET",
        "Delta r_finite,target",
        FINITE_TARGET_DELTA_R,
        FINITE_TARGET_MW_MEV,
        "EXACT_SAME_INPUT_TARGET_FUNCTIONAL",
        "NATIVE_FUNCTIONAL_OPEN",
        "the exact finite/counterterm target that APF-native one-loop closure must reproduce",
    ),
)

@dataclass(frozen=True)
class CountertermGate:
    gate_id: str
    status: str
    required_object: str
    current_evidence: str
    closes_physical_export: bool

COUNTERTERM_GATES: Tuple[CountertermGate, ...] = (
    CountertermGate("G2A_ONSHELL_ALGEBRA", "CLOSED", "s_W^2, c_W^2/s_W^2 at APF route point", "v16.6 analytic on-shell algebra", False),
    CountertermGate("G2B_LEADING_RHO", "CLOSED", "leading top-rho analytic row", "v16.6 Delta rho_t formula", False),
    CountertermGate("G2C_FINITE_TARGET", "CLOSED", "exact finite target value at same input", "v16.7 target functional from DIZET-total minus APF skeleton", False),
    CountertermGate("G2D_NATIVE_COUNTERTERMS", "OPEN", "Denner/Sirlin one-loop self-energy vertex box counterterm functions", "not implemented in APF-owned formula evaluator", False),
    CountertermGate("G2E_NATIVE_ONE_LOOP_CLOSURE", "OPEN", "APF-native evaluator reproduces finite target within tolerance", FIRST_FAILED_GATE, True),
)

SAFE_CLAIMS = (
    "The APF-native leading skeleton plus admitted same-input DIZET finite target exactly defines the one-loop finite/counterterm target.",
    "The missing native finite piece is not an unstructured residual; it splits into DIZET DRREM and the rho-resummation/cross gap.",
    "W remains an export candidate through reviewed same-input DIZET transport and admitted row covariance.",
    "Full APF-native one-loop closure requires an APF-owned Denner/Sirlin counterterm functional evaluator.",
)

FORBIDDEN_CLAIMS = (
    "APF has derived the Denner/Sirlin one-loop finite counterterms.",
    "APF has derived the full two-loop electroweak stack.",
    "The finite target is a new independent APF loop calculation.",
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


def finite_piece_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(x) for x in FINITE_PIECES)


def counterterm_gate_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(x) for x in COUNTERTERM_GATES)


def route_summary() -> Dict[str, Any]:
    return {
        "title": TITLE,
        "version": VERSION,
        "apf_version": APF_VERSION,
        "dependencies": [V16_4_PASS_STATUS, V16_6_PASS_STATUS],
        "input_point": {
            "M_Z_GeV": M_Z_GEV,
            "m_t_GeV": M_TOP_GEV,
            "M_H_GeV": M_H_GEV,
            "alpha_s_MZ": ALPHA_S_MZ,
            "G_F_GeV_minus2": G_F_GEV_MINUS2,
        },
        "same_input_values": {
            "Delta_alpha": DELTA_ALPHA_ADMITTED,
            "Delta_rho_top_leading": DELTA_RHO_TOP_LEADING,
            "rho_branch_leading": RHO_BRANCH_LEADING,
            "Delta_r_one_loop_skeleton": DELTA_R_ONE_LOOP_SKELETON,
            "Delta_r_DIZET_total": DIZET_DR_TOTAL,
            "finite_target_delta_r": FINITE_TARGET_DELTA_R,
            "finite_target_MW_MeV": FINITE_TARGET_MW_MEV,
            "DIZET_DRREM": DIZET_FINITE_REMAINDER,
            "rho_resummation_gap": RHO_RESUMMATION_GAP,
            "finite_target_recomposed": FINITE_TARGET_RECOMPOSED,
            "finite_target_error": FINITE_TARGET_ERROR,
            "skeleton_fraction_of_total": SKELETON_FRACTION_OF_TOTAL,
            "finite_fraction_of_total": FINITE_FRACTION_OF_TOTAL,
        },
        "w_export_candidate_state": {
            "M_W_TRACE_GeV": M_W_TRACE_GEV,
            "M_W_DIZET_GeV": DIZET_MW_GEV,
            "DIZET_minus_APF_MeV": DIZET_MINUS_APF_MEV,
            "sigma_input_MW_MeV": V16_4_INPUT_SIGMA_MW_MEV,
            "sigma_theory_MW_MeV": V16_4_THEORY_SIGMA_MW_MEV,
            "sigma_total_MW_MeV": TOTAL_SIGMA_MW_MEV,
            "pull_sigma": PULL_INPUT_PLUS_THEORY,
        },
        "finite_pieces": finite_piece_table(),
        "counterterm_gates": counterterm_gate_table(),
        "status": {
            "route_status": ROUTE_STATUS,
            "native_finite_status": NATIVE_FINITE_STATUS,
            "full_native_one_loop_status": FULL_NATIVE_ONE_LOOP_STATUS,
            "first_failed_gate": FIRST_FAILED_GATE,
            "next_gate": NEXT_GATE,
        },
        "safe_claims": SAFE_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "payload_digest": _digest([finite_piece_table(), counterterm_gate_table(), SAFE_CLAIMS, FORBIDDEN_CLAIMS]),
    }


def terminal_report() -> Dict[str, Any]:
    return {"status": STATUS, "pass_status": PASS_STATUS, "route_summary": route_summary()}

# checks

def check_T_w_trace_native_finite_status_declared():
    return _res("status_declared", STATUS.startswith("P_w_trace") and VERSION == "v16_7")

def check_T_w_trace_native_finite_dependencies_pass():
    return _res("dependencies_pass", V16_4_PASS_STATUS.endswith("PASS") and V16_6_PASS_STATUS.endswith("PASS"))

def check_T_w_trace_native_finite_input_physical():
    return _res("input_physical", 91 < M_Z_GEV < 92 and 170 < M_TOP_GEV < 175 and 120 < M_H_GEV < 130)

def check_T_w_trace_native_finite_skeleton_below_total():
    return _res("skeleton_below_total", 0 < DELTA_R_ONE_LOOP_SKELETON < DIZET_DR_TOTAL)

def check_T_w_trace_native_finite_target_positive():
    return _res("finite_target_positive", 0.009 < FINITE_TARGET_DELTA_R < 0.011)

def check_T_w_trace_native_finite_target_recomposes():
    return _res("finite_target_recomposes", abs(FINITE_TARGET_ERROR) < 1e-15)

def check_T_w_trace_native_finite_piece_count():
    return _res("finite_piece_count", len(FINITE_PIECES) == 3)

def check_T_w_trace_native_finite_has_drrem_piece():
    return _res("has_drrem_piece", any(p.piece_id == "F1_DRREM" for p in FINITE_PIECES))

def check_T_w_trace_native_finite_has_rho_gap_piece():
    return _res("has_rho_gap_piece", any(p.piece_id == "F2_RHO_RESUMMATION_GAP" for p in FINITE_PIECES))

def check_T_w_trace_native_finite_has_total_target_piece():
    return _res("has_total_target_piece", any(p.piece_id == "F3_TOTAL_NATIVE_TARGET" for p in FINITE_PIECES))

def check_T_w_trace_native_finite_drrem_positive():
    return _res("drrem_positive", DIZET_FINITE_REMAINDER > 0)

def check_T_w_trace_native_finite_rho_gap_negative():
    return _res("rho_gap_negative", RHO_RESUMMATION_GAP < 0)

def check_T_w_trace_native_finite_mw_scale_large():
    return _res("mw_scale_large", 150 < FINITE_TARGET_MW_MEV < 180)

def check_T_w_trace_native_finite_skeleton_fraction_reasonable():
    return _res("skeleton_fraction_reasonable", 0.70 < SKELETON_FRACTION_OF_TOTAL < 0.75)

def check_T_w_trace_native_finite_fraction_reasonable():
    return _res("finite_fraction_reasonable", 0.25 < FINITE_FRACTION_OF_TOTAL < 0.30)

def check_T_w_trace_native_finite_gates_count():
    return _res("gates_count", len(COUNTERTERM_GATES) == 5)

def check_T_w_trace_native_finite_open_gate_present():
    return _res("open_gate_present", any(g.status == "OPEN" for g in COUNTERTERM_GATES))

def check_T_w_trace_native_finite_closed_target_gate_present():
    return _res("closed_target_gate_present", any(g.gate_id == "G2C_FINITE_TARGET" and g.status == "CLOSED" for g in COUNTERTERM_GATES))

def check_T_w_trace_native_finite_first_failed_gate_exact():
    return _res("first_failed_gate_exact", FIRST_FAILED_GATE == "APF_NATIVE_DENNER_COUNTERTERM_FUNCTIONAL_EVALUATOR")

def check_T_w_trace_native_finite_no_physical_final_claim():
    return _res("no_physical_final_claim", "not" in NATIVE_FINITE_STATUS.lower() and "OPEN" in FULL_NATIVE_ONE_LOOP_STATUS)

def check_T_w_trace_native_finite_export_candidate_preserved():
    return _res("export_candidate_preserved", "export_candidate" in ROUTE_STATUS)

def check_T_w_trace_native_finite_row_covariance_available():
    return _res("row_covariance_available", len(V16_4_ROW_COVARIANCE) >= 9 and V16_4_INPUT_SIGMA_DELTA_R > 0)

def check_T_w_trace_native_finite_mw_pull_preserved():
    return _res("mw_pull_preserved", 1.0 < PULL_INPUT_PLUS_THEORY < 1.2)

def check_T_w_trace_native_finite_safe_claims_present():
    return _res("safe_claims_present", len(SAFE_CLAIMS) == 4)

def check_T_w_trace_native_finite_forbidden_claims_present():
    return _res("forbidden_claims_present", len(FORBIDDEN_CLAIMS) == 3)

def check_T_w_trace_native_finite_denner_gate_blocks_native_loop():
    return _res("denner_gate_blocks_native_loop", route_summary()["status"]["first_failed_gate"] == FIRST_FAILED_GATE)

def check_T_w_trace_native_finite_report_contains_pieces():
    return _res("report_contains_pieces", len(route_summary()["finite_pieces"]) == 3)

def check_T_w_trace_native_finite_report_contains_gates():
    return _res("report_contains_gates", len(route_summary()["counterterm_gates"]) == 5)

def check_T_w_trace_native_finite_payload_digest_present():
    return _res("payload_digest_present", route_summary()["payload_digest"].startswith("sha256:"))

def check_T_w_trace_native_finite_no_double_count_identity():
    lhs = DELTA_ALPHA_ADMITTED + RHO_BRANCH_LEADING + FINITE_TARGET_DELTA_R
    return _res("no_double_count_identity", abs(lhs - DIZET_DR_TOTAL) < 1e-15)

def check_T_w_trace_native_finite_target_pieces_sum_to_total_target():
    lhs = DIZET_FINITE_REMAINDER + RHO_RESUMMATION_GAP
    return _res("target_pieces_sum_to_total_target", abs(lhs - FINITE_TARGET_DELTA_R) < 1e-15)

def check_T_w_trace_native_finite_mw_conversion_sign():
    return _res("mw_conversion_sign", DMDDELTA_R_GEV < 0 and FINITE_TARGET_MW_MEV > 0)

def check_T_w_trace_native_finite_admitted_rows_available():
    return _res("admitted_rows_available", len(V16_4_ADMITTED_ROWS) == 3)

def check_T_w_trace_native_finite_open_closure_requires_counterterms():
    return _res("open_closure_requires_counterterms", any("COUNTERTERM" in g.required_object.upper() for g in COUNTERTERM_GATES if g.status == "OPEN"))

def check_T_w_trace_native_finite_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_trace_native_finite_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))

_CHECKS = {name: obj for name, obj in sorted(globals().items()) if name.startswith("check_T_w_trace_native_finite_") and callable(obj)}


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
    raise SystemExit(0 if out["passed"] else 1)
