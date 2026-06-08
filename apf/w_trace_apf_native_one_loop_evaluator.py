"""W_TRACE APF-native one-loop Delta-r evaluator scaffold.

v16.6 (2026-05-09): begins the APF-owned electroweak loop stack after the
v16.4/v16.5 DIZET transport closeout.  This module does not claim a full SM
loop derivation.  It closes the first native layer that can be closed honestly:

  * on-shell weak-angle algebra at the APF W route point;
  * the leading one-loop top/rho branch from the standard quadratic-top
    counterterm structure;
  * the running-alpha channel as an admitted external vacuum-polarization input;
  * an explicit finite-remainder theorem saying what is still missing before
    APF-native one-loop Delta-r closure.

The result is deliberately a scaffold-plus-obstruction: APF now owns the
leading analytic one-loop skeleton, while DIZET remains the reviewed same-input
transport reference for the full row ledger and covariance.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_full_loop_derivation_closeout import (
    PASS_STATUS as V16_5_PASS_STATUS,
    route_summary as v16_5_route_summary,
    EXPORT_CANDIDATE_STATUS as V16_5_EXPORT_CANDIDATE_STATUS,
)
from apf.w_trace_dizet_row_admission_covariance import (
    DR_TOTAL as DIZET_DR_TOTAL,
    DIZET_MW_GEV,
    M_W_TRACE_GEV,
    DIZET_MINUS_APF_MEV,
    TOTAL_SIGMA_MW_MEV,
    PULL_INPUT_PLUS_THEORY,
    DMDDELTA_R_GEV,
    ADMITTED_ROWS,
    INPUT_SIGMA_MW_MEV,
    THEORY_SIGMA_MW_MEV,
)

STATUS = "P_w_trace_apf_native_one_loop_evaluator_scaffold"
VERSION = "v16_6"
PASS_STATUS = "W_TRACE_APF_NATIVE_ONE_LOOP_EVALUATOR_SCAFFOLD_PASS"
TITLE = "W_TRACE APF-native one-loop Delta-r evaluator scaffold"
PAYLOAD_ID = "W_TRACE_APF_NATIVE_ONE_LOOP_EVALUATOR_SCAFFOLD_v16_6"
APF_VERSION = "16.6.0"

# Same-input APF/DIZET route point.
M_Z_GEV = 91.1876
M_TOP_GEV = 172.57
M_H_GEV = 125.25
ALPHA_S_MZ = 0.1184
G_F_GEV_MINUS2 = 1.1663787e-5

# DIZET-admitted running-alpha row from v16.4.  It is a reviewed-code input row,
# not an APF derivation of hadronic vacuum polarization.
DELTA_ALPHA_ADMITTED = 0.05907386039640014
DIZET_FINITE_REMAINDER = 0.011667933872161376
DIZET_RHO_CROSS = -0.03424000860914665

# APF on-shell algebra at the APF trace anchor.
S2_APF_TRACE = 1.0 - (M_W_TRACE_GEV / M_Z_GEV) ** 2
C2_APF_TRACE = 1.0 - S2_APF_TRACE
C2_OVER_S2_APF_TRACE = C2_APF_TRACE / S2_APF_TRACE

# Leading one-loop top/rho branch.
DELTA_RHO_TOP_LEADING = 3.0 * G_F_GEV_MINUS2 * M_TOP_GEV ** 2 / (8.0 * math.sqrt(2.0) * math.pi ** 2)
RHO_BRANCH_LEADING = -C2_OVER_S2_APF_TRACE * DELTA_RHO_TOP_LEADING

# APF-owned one-loop skeleton using admitted Delta-alpha as external row.
DELTA_R_ONE_LOOP_SKELETON = DELTA_ALPHA_ADMITTED + RHO_BRANCH_LEADING
SKELETON_TO_DIZET_RESIDUAL = DIZET_DR_TOTAL - DELTA_R_ONE_LOOP_SKELETON
SKELETON_TO_DIZET_MW_SHIFT_MEV = (DELTA_R_ONE_LOOP_SKELETON - DIZET_DR_TOTAL) * DMDDELTA_R_GEV * 1000.0

# Split the residual against the DIZET admitted rows.
RHO_RESUMMATION_GAP = DIZET_RHO_CROSS - RHO_BRANCH_LEADING
FINITE_REMAINDER_GAP = DIZET_FINITE_REMAINDER
RESIDUAL_RECOMPOSED = FINITE_REMAINDER_GAP + RHO_RESUMMATION_GAP
RESIDUAL_RECOMPOSITION_ERROR = SKELETON_TO_DIZET_RESIDUAL - RESIDUAL_RECOMPOSED

ROUTE_STATUS = "P_native_one_loop_skeleton_plus_reviewed_transport_export_candidate"
NATIVE_ONE_LOOP_STATUS = "P_scaffold_not_full_one_loop_delta_r"
FIRST_FAILED_GATE = "APF_NATIVE_FINITE_REMAINDER_AND_COUNTERTERM_EVALUATOR"
NEXT_GATE = "G2B_NATIVE_ONE_LOOP_FINITE_REMAINDER"
FULL_LOOP_STATUS = "OPEN_BEYOND_ONE_LOOP_SCAFFOLD"

@dataclass(frozen=True)
class NativeRow:
    row_id: str
    symbol: str
    value_delta_r: float
    source: str
    apf_owned: bool
    status: str
    interpretation: str

NATIVE_ROWS: Tuple[NativeRow, ...] = (
    NativeRow(
        "R1_DALPHA",
        "Delta alpha",
        DELTA_ALPHA_ADMITTED,
        "DIZET admitted same-input vacuum-polarization row",
        False,
        "ADMITTED_EXTERNAL_INPUT_ROW",
        "running-alpha / vacuum-polarization branch; APF transports but does not derive hadronic VP here",
    ),
    NativeRow(
        "R2_RHOTOP",
        "-(c^2/s^2) Delta rho_t",
        RHO_BRANCH_LEADING,
        "APF-owned on-shell algebra + leading top-rho formula",
        True,
        "APF_NATIVE_ANALYTIC_ROW",
        "leading quadratic-top weak-isospin/rho correction at APF route point",
    ),
    NativeRow(
        "R3_FINITE_RESIDUAL_REQUIRED",
        "Delta r finite remainder required",
        SKELETON_TO_DIZET_RESIDUAL,
        "difference between DIZET same-input total and APF one-loop skeleton",
        False,
        "OPEN_NATIVE_COUNTERTERM_ROW_REQUIRED",
        "bosonic/vertex/box/counterterm/resummation finite remainder required for full one-loop/transport closure",
    ),
)

@dataclass(frozen=True)
class NativeFormula:
    formula_id: str
    expression: str
    closed: bool
    blocker: str

FORMULAE: Tuple[NativeFormula, ...] = (
    NativeFormula("F1_S2", "s_W^2 = 1 - M_W^2/M_Z^2", True, ""),
    NativeFormula("F2_RHO", "Delta rho_t = 3 G_F m_t^2/(8 sqrt(2) pi^2)", True, ""),
    NativeFormula("F3_ONE_LOOP_SKELETON", "Delta r_skel = Delta alpha - (c_W^2/s_W^2) Delta rho_t", True, ""),
    NativeFormula("F4_FINITE_REMAINDER", "Delta r_full = Delta r_skel + Delta r_finite", False, FIRST_FAILED_GATE),
    NativeFormula("F5_TWO_LOOP", "Delta r_full += Delta r_ferm^2 + Delta r_bos^2 + mixed QCD/EW", False, "APF_NATIVE_TWO_LOOP_MASTER_INTEGRAL_EVALUATOR"),
)

@dataclass(frozen=True)
class GapRow:
    gap_id: str
    value_delta_r: float
    value_MW_shift_MeV: float
    interpretation: str

GAP_ROWS: Tuple[GapRow, ...] = (
    GapRow("skeleton_to_DIZET_total", SKELETON_TO_DIZET_RESIDUAL, -SKELETON_TO_DIZET_MW_SHIFT_MEV, "full finite correction missing from analytic Delta-alpha/top-rho scaffold"),
    GapRow("DIZET_finite_remainder_DRREM", FINITE_REMAINDER_GAP, -FINITE_REMAINDER_GAP * DMDDELTA_R_GEV * 1000.0, "DIZET admitted finite-remainder channel"),
    GapRow("rho_resummation_gap", RHO_RESUMMATION_GAP, -RHO_RESUMMATION_GAP * DMDDELTA_R_GEV * 1000.0, "gap between leading top-rho formula and DIZET rho/cross branch"),
)

SAFE_CLAIMS = (
    "APF owns the on-shell algebra and leading top-rho analytic row at the same APF route point.",
    "The running-alpha row is admitted as reviewed-code/external vacuum-polarization input, not derived from APF here.",
    "The APF-native one-loop skeleton does not close the full DIZET Delta-r; the missing finite row is explicitly quantified.",
    "W remains an export candidate by reviewed same-input DIZET transport plus admitted row covariance.",
)

FORBIDDEN_CLAIMS = (
    "APF has derived the full one-loop electroweak Delta-r finite part.",
    "APF has derived the two-loop/higher-order electroweak stack.",
    "The one-loop skeleton alone is the physical on-shell W prediction.",
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


def native_row_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(x) for x in NATIVE_ROWS)


def formula_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(x) for x in FORMULAE)


def gap_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(x) for x in GAP_ROWS)


def route_summary() -> Dict[str, Any]:
    return {
        "title": TITLE,
        "version": VERSION,
        "apf_version": APF_VERSION,
        "dependency": V16_5_PASS_STATUS,
        "same_input_point": {
            "M_Z_GeV": M_Z_GEV,
            "m_t_GeV": M_TOP_GEV,
            "M_H_GeV": M_H_GEV,
            "alpha_s_MZ": ALPHA_S_MZ,
            "M_W_APF_TRACE_GeV": M_W_TRACE_GEV,
            "M_W_DIZET_GeV": DIZET_MW_GEV,
            "DIZET_minus_APF_MeV": DIZET_MINUS_APF_MEV,
            "sigma_input_plus_theory_MeV": TOTAL_SIGMA_MW_MEV,
            "pull_sigma": PULL_INPUT_PLUS_THEORY,
        },
        "on_shell_algebra": {
            "s2_APF_TRACE": S2_APF_TRACE,
            "c2_APF_TRACE": C2_APF_TRACE,
            "c2_over_s2": C2_OVER_S2_APF_TRACE,
        },
        "native_one_loop_skeleton": {
            "Delta_alpha_admitted": DELTA_ALPHA_ADMITTED,
            "Delta_rho_top_leading": DELTA_RHO_TOP_LEADING,
            "rho_branch_leading": RHO_BRANCH_LEADING,
            "Delta_r_skeleton": DELTA_R_ONE_LOOP_SKELETON,
            "DIZET_Delta_r_total": DIZET_DR_TOTAL,
            "skeleton_to_DIZET_residual": SKELETON_TO_DIZET_RESIDUAL,
            "skeleton_to_DIZET_MW_shift_MeV": SKELETON_TO_DIZET_MW_SHIFT_MEV,
        },
        "residual_split": {
            "finite_remainder_DRREM": FINITE_REMAINDER_GAP,
            "rho_resummation_gap": RHO_RESUMMATION_GAP,
            "recomposed_residual": RESIDUAL_RECOMPOSED,
            "recomposition_error": RESIDUAL_RECOMPOSITION_ERROR,
        },
        "native_rows": native_row_table(),
        "formulae": formula_table(),
        "gap_rows": gap_table(),
        "status": {
            "route_status": ROUTE_STATUS,
            "native_one_loop_status": NATIVE_ONE_LOOP_STATUS,
            "full_loop_status": FULL_LOOP_STATUS,
            "first_failed_gate": FIRST_FAILED_GATE,
            "next_gate": NEXT_GATE,
        },
        "safe_claims": SAFE_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "payload_digest": _digest([native_row_table(), formula_table(), gap_table(), SAFE_CLAIMS, FORBIDDEN_CLAIMS]),
    }


def terminal_report() -> Dict[str, Any]:
    return {"status": STATUS, "pass_status": PASS_STATUS, "route_summary": route_summary()}

# checks ---------------------------------------------------------------------

def check_T_w_trace_native_one_loop_status_declared():
    return _res("status_declared", STATUS.startswith("P_w_trace") and VERSION == "v16_6")


def check_T_w_trace_native_one_loop_depends_on_v165():
    return _res("depends_on_v165", V16_5_PASS_STATUS.endswith("PASS"))


def check_T_w_trace_native_one_loop_v165_export_candidate_preserved():
    return _res("v165_export_candidate_preserved", v16_5_route_summary()["route_status"] == V16_5_EXPORT_CANDIDATE_STATUS)


def check_T_w_trace_native_one_loop_inputs_declared():
    return _res("inputs_declared", M_Z_GEV > 91 and M_TOP_GEV > 170 and G_F_GEV_MINUS2 > 0)


def check_T_w_trace_native_one_loop_s2_physical():
    return _res("s2_physical", 0.22 < S2_APF_TRACE < 0.23 and 0.77 < C2_APF_TRACE < 0.78)


def check_T_w_trace_native_one_loop_c2_over_s2_physical():
    return _res("c2_over_s2_physical", 3.4 < C2_OVER_S2_APF_TRACE < 3.6)


def check_T_w_trace_native_one_loop_delta_rho_formula_positive():
    return _res("delta_rho_formula_positive", 0.009 < DELTA_RHO_TOP_LEADING < 0.010)


def check_T_w_trace_native_one_loop_rho_branch_negative():
    return _res("rho_branch_negative", RHO_BRANCH_LEADING < 0)


def check_T_w_trace_native_one_loop_delta_alpha_admitted_positive():
    return _res("delta_alpha_admitted_positive", 0.058 < DELTA_ALPHA_ADMITTED < 0.060)


def check_T_w_trace_native_one_loop_skeleton_value_range():
    return _res("skeleton_value_range", 0.026 < DELTA_R_ONE_LOOP_SKELETON < 0.027)


def check_T_w_trace_native_one_loop_dizet_total_range():
    return _res("dizet_total_range", 0.036 < DIZET_DR_TOTAL < 0.037)


def check_T_w_trace_native_one_loop_residual_positive():
    return _res("residual_positive", 0.009 < SKELETON_TO_DIZET_RESIDUAL < 0.011)


def check_T_w_trace_native_one_loop_residual_split_closes():
    return _res("residual_split_closes", abs(RESIDUAL_RECOMPOSITION_ERROR) < 1e-15)


def check_T_w_trace_native_one_loop_finite_remainder_nonzero():
    return _res("finite_remainder_nonzero", FINITE_REMAINDER_GAP > 0.011)


def check_T_w_trace_native_one_loop_rho_resummation_gap_nonzero():
    return _res("rho_resummation_gap_nonzero", RHO_RESUMMATION_GAP < -0.001)


def check_T_w_trace_native_one_loop_gap_rows_three():
    return _res("gap_rows_three", len(GAP_ROWS) == 3)


def check_T_w_trace_native_one_loop_native_rows_three():
    return _res("native_rows_three", len(NATIVE_ROWS) == 3)


def check_T_w_trace_native_one_loop_has_apf_owned_row():
    return _res("has_apf_owned_row", any(r.apf_owned for r in NATIVE_ROWS))


def check_T_w_trace_native_one_loop_delta_alpha_not_apf_owned():
    return _res("delta_alpha_not_apf_owned", next(r for r in NATIVE_ROWS if r.row_id == "R1_DALPHA").apf_owned is False)


def check_T_w_trace_native_one_loop_open_finite_row_marked():
    return _res("open_finite_row_marked", next(r for r in NATIVE_ROWS if r.row_id == "R3_FINITE_RESIDUAL_REQUIRED").status.startswith("OPEN"))


def check_T_w_trace_native_one_loop_formulae_five():
    return _res("formulae_five", len(FORMULAE) == 5)


def check_T_w_trace_native_one_loop_formulae_include_closed_and_open():
    return _res("formulae_include_closed_and_open", any(f.closed for f in FORMULAE) and any(not f.closed for f in FORMULAE))


def check_T_w_trace_native_one_loop_first_failed_gate_exact():
    return _res("first_failed_gate_exact", route_summary()["status"]["first_failed_gate"] == FIRST_FAILED_GATE)


def check_T_w_trace_native_one_loop_next_gate_exact():
    return _res("next_gate_exact", route_summary()["status"]["next_gate"] == NEXT_GATE)


def check_T_w_trace_native_one_loop_forbidden_claims_present():
    return _res("forbidden_claims_present", len(FORBIDDEN_CLAIMS) == 3)


def check_T_w_trace_native_one_loop_safe_claims_present():
    return _res("safe_claims_present", len(SAFE_CLAIMS) == 4)


def check_T_w_trace_native_one_loop_no_full_loop_claim():
    return _res("no_full_loop_claim", "OPEN" in FULL_LOOP_STATUS and "not_full" in NATIVE_ONE_LOOP_STATUS)


def check_T_w_trace_native_one_loop_transport_status_preserved():
    return _res("transport_status_preserved", "export_candidate" in ROUTE_STATUS)


def check_T_w_trace_native_one_loop_mw_state_preserved():
    return _res("mw_state_preserved", 80.35 < DIZET_MW_GEV < 80.37 and 80.36 < M_W_TRACE_GEV < 80.37)


def check_T_w_trace_native_one_loop_pull_state_preserved():
    return _res("pull_state_preserved", 1.0 < PULL_INPUT_PLUS_THEORY < 1.2)


def check_T_w_trace_native_one_loop_gap_mw_scale_large():
    return _res("gap_mw_scale_large", abs(SKELETON_TO_DIZET_MW_SHIFT_MEV) > 100)


def check_T_w_trace_native_one_loop_gap_explains_need_for_finite_part():
    return _res("gap_explains_need_for_finite_part", abs(SKELETON_TO_DIZET_RESIDUAL) > 0.25 * abs(DIZET_DR_TOTAL))


def check_T_w_trace_native_one_loop_report_contains_rows():
    return _res("report_contains_rows", len(route_summary()["native_rows"]) == 3)


def check_T_w_trace_native_one_loop_report_contains_gap_rows():
    return _res("report_contains_gap_rows", len(route_summary()["gap_rows"]) == 3)


def check_T_w_trace_native_one_loop_payload_digest_present():
    return _res("payload_digest_present", route_summary()["payload_digest"].startswith("sha256:"))


def check_T_w_trace_native_one_loop_admitted_dizet_rows_available():
    return _res("admitted_dizet_rows_available", len(ADMITTED_ROWS) == 3)


def check_T_w_trace_native_one_loop_dmd_delta_r_nonzero():
    return _res("dmd_delta_r_nonzero", DMDDELTA_R_GEV < -10)


def check_T_w_trace_native_one_loop_input_sigma_preserved():
    return _res("input_sigma_preserved", INPUT_SIGMA_MW_MEV > 0 and THEORY_SIGMA_MW_MEV == 4.0)


def check_T_w_trace_native_one_loop_formal_boundary_correct():
    return _res("formal_boundary_correct", NATIVE_ONE_LOOP_STATUS == "P_scaffold_not_full_one_loop_delta_r")


def check_T_w_trace_native_one_loop_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_trace_native_one_loop_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))

_CHECKS = {name: obj for name, obj in sorted(globals().items()) if name.startswith("check_T_w_trace_native_one_loop_") and callable(obj)}


def register(registry: MutableMapping[str, Any]) -> None:
    registry.update(_CHECKS)


def run_all() -> Dict[str, Any]:
    rows = []
    for name, fn in _CHECKS.items():
        try:
            result = fn()
            rows.append({"name": name, "passed": _passed(result), "result": result})
        except Exception as exc:  # pragma: no cover
            rows.append({"name": name, "passed": False, "error": repr(exc)})
    ok = all(row["passed"] for row in rows)
    return {"passed": ok, "status": PASS_STATUS if ok else PASS_STATUS.replace("_PASS", "_FAIL"), "checks": rows, "report": terminal_report()}

if __name__ == "__main__":
    out = run_all()
    print(out["status"])
    for row in out["checks"]:
        print(("PASS" if row["passed"] else "FAIL"), row["name"])
    raise SystemExit(0 if out["passed"] else 1)
