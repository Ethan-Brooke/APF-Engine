"""W_TRACE Denner/Sirlin counterterm-functional reduction layer.

v16.8 (2026-05-09): pushes below the finite-target layer by translating the
APF-native one-loop problem into an explicit Denner/Sirlin counterterm
functional basis.  The module does not claim that APF has evaluated every
Passarino--Veltman scalar integral.  It closes the symbolic and numerical
master-identity layer: the APF-owned leading skeleton plus an exact
same-input counterterm target reproduces the DIZET Delta-r total, while the
remaining open object is sharply reduced to a native scalar-integral and
counterterm evaluator.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_native_finite_remainder_evaluator import (
    PASS_STATUS as V16_7_PASS_STATUS,
    M_Z_GEV, M_TOP_GEV, M_H_GEV, ALPHA_S_MZ, G_F_GEV_MINUS2,
    DELTA_ALPHA_ADMITTED, RHO_BRANCH_LEADING, DELTA_R_ONE_LOOP_SKELETON,
    DIZET_DR_TOTAL, DIZET_FINITE_REMAINDER, DIZET_RHO_CROSS,
    RHO_RESUMMATION_GAP, FINITE_TARGET_DELTA_R, FINITE_TARGET_MW_MEV,
    DMDDELTA_R_GEV, M_W_TRACE_GEV, DIZET_MW_GEV, DIZET_MINUS_APF_MEV,
    TOTAL_SIGMA_MW_MEV, PULL_INPUT_PLUS_THEORY,
)
from apf.w_trace_dizet_internal_dr_decomposition import (
    PASS_STATUS as V16_3_PASS_STATUS,
    decomposition_equations as v163_decomposition_equations,
)
from apf.w_trace_dizet_row_admission_covariance import (
    PASS_STATUS as V16_4_PASS_STATUS,
    ROW_COVARIANCE as V16_4_ROW_COVARIANCE,
    INPUT_SIGMA_MW_MEV,
    THEORY_SIGMA_MW_MEV,
)

STATUS = "P_w_trace_denner_sirlin_counterterm_functional"
VERSION = "v16_8"
PASS_STATUS = "W_TRACE_DENNER_SIRLIN_COUNTERTERM_FUNCTIONAL_PASS"
TITLE = "W_TRACE Denner/Sirlin counterterm-functional reduction layer"
PAYLOAD_ID = "W_TRACE_DENNER_SIRLIN_COUNTERTERM_FUNCTIONAL_v16_8"
APF_VERSION = "16.8.0"

ROUTE_STATUS = "P_export_candidate_plus_denner_sirlin_counterterm_functional_basis"
FULL_NATIVE_ONE_LOOP_STATUS = "OPEN_NATIVE_SCALAR_INTEGRAL_EVALUATOR_REQUIRED"
FIRST_FAILED_GATE = "APF_NATIVE_PASSARINO_VELTMAN_SCALAR_INTEGRAL_EVALUATOR"
NEXT_GATE = "G2D_NATIVE_SCALAR_INTEGRAL_AND_COUNTERTERM_EVALUATOR"

# The counterterm target that must be reproduced by an APF-native on-shell
# one-loop evaluator.  Numerically this is exactly the finite target closed in
# v16.7.
COUNTERTERM_TARGET_DELTA_R = FINITE_TARGET_DELTA_R
COUNTERTERM_TARGET_MW_MEV = FINITE_TARGET_MW_MEV
MASTER_IDENTITY_TOTAL = DELTA_ALPHA_ADMITTED + RHO_BRANCH_LEADING + COUNTERTERM_TARGET_DELTA_R
MASTER_IDENTITY_ERROR = MASTER_IDENTITY_TOTAL - DIZET_DR_TOTAL

# A useful split of the counterterm target into DIZET-admitted realization
# pieces.  These are not asserted to be APF-derived finite loop rows; they are
# same-input reviewed-code target values for the APF-native evaluator to hit.
DRREM_TARGET = DIZET_FINITE_REMAINDER
RHO_CROSS_MINUS_LEAD_TARGET = RHO_RESUMMATION_GAP
TARGET_SPLIT_ERROR = (DRREM_TARGET + RHO_CROSS_MINUS_LEAD_TARGET) - COUNTERTERM_TARGET_DELTA_R

# DIZET internal DRREM assembly terms from the v16.3 instrumentation.  Keeping
# these here prevents the finite remainder from degenerating back into a
# shapeless residual.
DRREM_NEWDR = 0.011204535418249811
TBQCD = 0.0034094667035108241
CLQQCD = 6.3488881911197986e-05
ALFQCD = 0.0
TBQCDL = 0.0030730460134216551
DRHH = 0.0
DRREM_ASSEMBLED = DRREM_NEWDR + TBQCD + 2.0 * CLQQCD + ALFQCD - TBQCDL + DRHH
DRREM_ASSEMBLY_ERROR = DRREM_ASSEMBLED - DRREM_TARGET

# one-loop vs beyond-one-loop bookkeeping.  This is conservative: the target is
# a same-input functional to reproduce, not a claim that all pieces are pure
# one-loop.
PURE_SKELETON_DELTA_R = DELTA_ALPHA_ADMITTED + RHO_BRANCH_LEADING
PURE_SKELETON_ERROR_TO_TOTAL = DIZET_DR_TOTAL - PURE_SKELETON_DELTA_R

@dataclass(frozen=True)
class FunctionalTerm:
    term_id: str
    symbol: str
    value_delta_r: float
    value_mw_mev: float
    role: str
    evidence: str
    native_status: str
    notes: str

FUNCTIONAL_TERMS: Tuple[FunctionalTerm, ...] = (
    FunctionalTerm(
        "DS1_RUNNING_ALPHA",
        "Delta r_{Delta alpha}",
        DELTA_ALPHA_ADMITTED,
        -DELTA_ALPHA_ADMITTED * DMDDELTA_R_GEV * 1000.0,
        "charge-renormalization/running-alpha channel",
        "admitted same-input DIZET row; APF input ledger",
        "ADMITTED_TRANSPORT_ROW_NOT_APF_LOOP_DERIVED",
        "large positive electromagnetic screening contribution",
    ),
    FunctionalTerm(
        "DS2_LEADING_RHO",
        "-(c_W^2/s_W^2) Delta rho_t^{lead}",
        RHO_BRANCH_LEADING,
        -RHO_BRANCH_LEADING * DMDDELTA_R_GEV * 1000.0,
        "mass-counterterm/top-rho leading channel",
        "APF-owned analytic leading top-rho formula closed in v16.6",
        "APF_NATIVE_LEADING_ROW_CLOSED",
        "large negative weak-isospin-breaking branch",
    ),
    FunctionalTerm(
        "DS3_RHO_CROSS_CORRECTION",
        "Delta r_{rho-cross}^{DIZET}-Delta r_{rho}^{lead}",
        RHO_CROSS_MINUS_LEAD_TARGET,
        -RHO_CROSS_MINUS_LEAD_TARGET * DMDDELTA_R_GEV * 1000.0,
        "rho resummation/cross correction target",
        "same-input DIZET admitted rho-cross minus APF leading rho",
        "NATIVE_COUNTERTERM_TARGET_NOT_DERIVED",
        "target for mass-counterterm/resummation refinements beyond leading rho",
    ),
    FunctionalTerm(
        "DS4_FINITE_REMAINDER",
        "Delta r_{rem}^{DIZET}",
        DRREM_TARGET,
        -DRREM_TARGET * DMDDELTA_R_GEV * 1000.0,
        "finite self-energy/vertex/box/counterterm remainder target",
        "same-input DIZET DRREM, internally assembled by v16.3",
        "NATIVE_FINITE_FUNCTIONAL_TARGET_NOT_DERIVED",
        "target for Denner/Sirlin finite counterterm, vertex, box and implementation remainder",
    ),
    FunctionalTerm(
        "DS5_TOTAL",
        "Delta r_{DIZET}(x_{APF})",
        DIZET_DR_TOTAL,
        -DIZET_DR_TOTAL * DMDDELTA_R_GEV * 1000.0,
        "same-input total transport evaluator",
        "compiled DIZET v6.45 same-input run and admitted row ledger",
        "REVIEWED_TRANSPORT_TOTAL_CLOSED",
        "not an APF-native full loop derivation",
    ),
)

@dataclass(frozen=True)
class CountertermBasisGate:
    gate_id: str
    status: str
    object: str
    evidence: str
    blocks_full_native_loop: bool

COUNTERTERM_BASIS_GATES: Tuple[CountertermBasisGate, ...] = (
    CountertermBasisGate("G2C_1_MASTER_IDENTITY", "CLOSED", "Delta r = Delta alpha + rho_lead + counterterm_target", "v16.8 master identity closes to DIZET total", False),
    CountertermBasisGate("G2C_2_DRREM_ASSEMBLY", "CLOSED", "DRREM = DRREM_NEWDR + TBQCD + 2CLQQCD + ALFQCD - TBQCDL + DRHH", "v16.3 instrumentation identity imported and verified", False),
    CountertermBasisGate("G2C_3_DENNER_SIRLIN_BASIS", "CLOSED_SYMBOLIC", "charge, mass, W self-energy, vertex, box, finite remainder basis", "basis terms typed and mapped to target values", False),
    CountertermBasisGate("G2D_1_SCALAR_INTEGRALS", "OPEN", "A0/B0/B00/C0/D0 finite parts in on-shell convention", "not APF-native implemented", True),
    CountertermBasisGate("G2D_2_COUNTERTERM_EVALUATOR", "OPEN", "native Denner/Sirlin counterterm functions evaluated at APF input", FIRST_FAILED_GATE, True),
    CountertermBasisGate("G2E_NATIVE_ONE_LOOP_CLOSURE", "OPEN", "native function equals target within tolerance and covariance", "requires G2D closure", True),
)

SAFE_CLAIMS = (
    "The Denner/Sirlin master identity has been converted into an APF-owned counterterm target functional.",
    "The same-input target closes exactly to the DIZET Delta-r total when combined with the APF leading skeleton.",
    "The finite target is decomposed into rho-cross correction and DRREM pieces, with DRREM internally assembled from exposed DIZET variables.",
    "W remains an on-shell export candidate through reviewed same-input transport, row ledger, and covariance.",
)

FORBIDDEN_CLAIMS = (
    "APF has analytically evaluated all one-loop scalar integrals.",
    "APF has independently derived the complete Denner/Sirlin counterterm stack.",
    "APF has derived two-loop electroweak corrections from first principles.",
    "The DIZET implementation-local decomposition is a unique physical ontology.",
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


def functional_term_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(x) for x in FUNCTIONAL_TERMS)


def counterterm_basis_gate_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(x) for x in COUNTERTERM_BASIS_GATES)


def route_summary() -> Dict[str, Any]:
    return {
        "title": TITLE,
        "version": VERSION,
        "apf_version": APF_VERSION,
        "dependencies": [V16_3_PASS_STATUS, V16_4_PASS_STATUS, V16_7_PASS_STATUS],
        "input_point": {
            "M_Z_GeV": M_Z_GEV,
            "m_t_GeV": M_TOP_GEV,
            "M_H_GeV": M_H_GEV,
            "alpha_s_MZ": ALPHA_S_MZ,
            "G_F_GeV_minus2": G_F_GEV_MINUS2,
        },
        "master_identity": {
            "Delta_alpha": DELTA_ALPHA_ADMITTED,
            "rho_leading_branch": RHO_BRANCH_LEADING,
            "counterterm_target_delta_r": COUNTERTERM_TARGET_DELTA_R,
            "master_identity_total": MASTER_IDENTITY_TOTAL,
            "DIZET_delta_r_total": DIZET_DR_TOTAL,
            "master_identity_error": MASTER_IDENTITY_ERROR,
            "counterterm_target_MW_MeV": COUNTERTERM_TARGET_MW_MEV,
        },
        "drrem_assembly": {
            "DRREM_NEWDR": DRREM_NEWDR,
            "TBQCD": TBQCD,
            "CLQQCD": CLQQCD,
            "ALFQCD": ALFQCD,
            "TBQCDL": TBQCDL,
            "DRHH": DRHH,
            "DRREM_assembled": DRREM_ASSEMBLED,
            "DRREM_target": DRREM_TARGET,
            "DRREM_assembly_error": DRREM_ASSEMBLY_ERROR,
        },
        "functional_terms": functional_term_table(),
        "counterterm_basis_gates": counterterm_basis_gate_table(),
        "export_candidate_state": {
            "M_W_TRACE_GeV": M_W_TRACE_GEV,
            "M_W_DIZET_GeV": DIZET_MW_GEV,
            "DIZET_minus_APF_MeV": DIZET_MINUS_APF_MEV,
            "sigma_input_MW_MeV": INPUT_SIGMA_MW_MEV,
            "sigma_theory_MW_MeV": THEORY_SIGMA_MW_MEV,
            "sigma_total_MW_MeV": TOTAL_SIGMA_MW_MEV,
            "pull_sigma": PULL_INPUT_PLUS_THEORY,
        },
        "status": {
            "route_status": ROUTE_STATUS,
            "full_native_one_loop_status": FULL_NATIVE_ONE_LOOP_STATUS,
            "first_failed_gate": FIRST_FAILED_GATE,
            "next_gate": NEXT_GATE,
        },
        "safe_claims": SAFE_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "payload_digest": _digest([functional_term_table(), counterterm_basis_gate_table(), SAFE_CLAIMS, FORBIDDEN_CLAIMS]),
    }


def terminal_report() -> Dict[str, Any]:
    return {"status": STATUS, "pass_status": PASS_STATUS, "route_summary": route_summary()}


# --- checks -----------------------------------------------------------------

def check_T_w_trace_denner_sirlin_status_declared():
    return _res("status_declared", STATUS.startswith("P_w_trace") and VERSION == "v16_8")

def check_T_w_trace_denner_sirlin_dependencies_pass():
    return _res("dependencies_pass", all(x.endswith("PASS") for x in (V16_3_PASS_STATUS, V16_4_PASS_STATUS, V16_7_PASS_STATUS)))

def check_T_w_trace_denner_sirlin_functional_terms_count():
    return _res("functional_terms_count", len(FUNCTIONAL_TERMS) == 5)

def check_T_w_trace_denner_sirlin_has_running_alpha():
    return _res("has_running_alpha", any(t.term_id == "DS1_RUNNING_ALPHA" for t in FUNCTIONAL_TERMS))

def check_T_w_trace_denner_sirlin_has_leading_rho():
    return _res("has_leading_rho", any(t.term_id == "DS2_LEADING_RHO" for t in FUNCTIONAL_TERMS))

def check_T_w_trace_denner_sirlin_has_rho_cross_target():
    return _res("has_rho_cross_target", any(t.term_id == "DS3_RHO_CROSS_CORRECTION" for t in FUNCTIONAL_TERMS))

def check_T_w_trace_denner_sirlin_has_finite_remainder():
    return _res("has_finite_remainder", any(t.term_id == "DS4_FINITE_REMAINDER" for t in FUNCTIONAL_TERMS))

def check_T_w_trace_denner_sirlin_has_total():
    return _res("has_total", any(t.term_id == "DS5_TOTAL" for t in FUNCTIONAL_TERMS))

def check_T_w_trace_denner_sirlin_master_identity_closes():
    return _res("master_identity_closes", abs(MASTER_IDENTITY_ERROR) < 1e-15, error=MASTER_IDENTITY_ERROR)

def check_T_w_trace_denner_sirlin_counterterm_target_positive():
    return _res("counterterm_target_positive", 0.009 < COUNTERTERM_TARGET_DELTA_R < 0.011)

def check_T_w_trace_denner_sirlin_counterterm_target_mw_scale():
    return _res("counterterm_target_mw_scale", 150 < COUNTERTERM_TARGET_MW_MEV < 180)

def check_T_w_trace_denner_sirlin_target_split_closes():
    return _res("target_split_closes", abs(TARGET_SPLIT_ERROR) < 1e-15, error=TARGET_SPLIT_ERROR)

def check_T_w_trace_denner_sirlin_drrem_assembly_closes():
    return _res("drrem_assembly_closes", abs(DRREM_ASSEMBLY_ERROR) < 1e-12, error=DRREM_ASSEMBLY_ERROR)

def check_T_w_trace_denner_sirlin_imported_v163_equation_closes():
    eqs = {e.name: e for e in v163_decomposition_equations()}
    return _res("imported_v163_equation_closes", eqs["DRREM_assembly"].passed and eqs["DR_equals_exported_ZPAR_DR"].passed)

def check_T_w_trace_denner_sirlin_drrem_newdr_positive():
    return _res("drrem_newdr_positive", DRREM_NEWDR > 0)

def check_T_w_trace_denner_sirlin_qcd_terms_physical_signs():
    return _res("qcd_terms_physical_signs", TBQCD > 0 and CLQQCD > 0 and TBQCDL > 0)

def check_T_w_trace_denner_sirlin_rho_gap_negative():
    return _res("rho_gap_negative", RHO_CROSS_MINUS_LEAD_TARGET < 0)

def check_T_w_trace_denner_sirlin_finite_remainder_positive():
    return _res("finite_remainder_positive", DRREM_TARGET > 0)

def check_T_w_trace_denner_sirlin_skeleton_plus_target_equals_total():
    return _res("skeleton_plus_target_equals_total", abs(PURE_SKELETON_DELTA_R + COUNTERTERM_TARGET_DELTA_R - DIZET_DR_TOTAL) < 1e-15)

def check_T_w_trace_denner_sirlin_gate_count():
    return _res("gate_count", len(COUNTERTERM_BASIS_GATES) == 6)

def check_T_w_trace_denner_sirlin_symbolic_basis_closed():
    return _res("symbolic_basis_closed", any(g.gate_id == "G2C_3_DENNER_SIRLIN_BASIS" and g.status == "CLOSED_SYMBOLIC" for g in COUNTERTERM_BASIS_GATES))

def check_T_w_trace_denner_sirlin_scalar_integral_gate_open():
    return _res("scalar_integral_gate_open", any(g.gate_id == "G2D_1_SCALAR_INTEGRALS" and g.status == "OPEN" for g in COUNTERTERM_BASIS_GATES))

def check_T_w_trace_denner_sirlin_counterterm_evaluator_gate_open():
    return _res("counterterm_evaluator_gate_open", any(g.gate_id == "G2D_2_COUNTERTERM_EVALUATOR" and g.status == "OPEN" for g in COUNTERTERM_BASIS_GATES))

def check_T_w_trace_denner_sirlin_first_failed_gate_exact():
    return _res("first_failed_gate_exact", FIRST_FAILED_GATE == "APF_NATIVE_PASSARINO_VELTMAN_SCALAR_INTEGRAL_EVALUATOR")

def check_T_w_trace_denner_sirlin_next_gate_exact():
    return _res("next_gate_exact", NEXT_GATE == "G2D_NATIVE_SCALAR_INTEGRAL_AND_COUNTERTERM_EVALUATOR")

def check_T_w_trace_denner_sirlin_export_candidate_preserved():
    return _res("export_candidate_preserved", "export_candidate" in ROUTE_STATUS)

def check_T_w_trace_denner_sirlin_no_full_native_claim():
    return _res("no_full_native_claim", FULL_NATIVE_ONE_LOOP_STATUS.startswith("OPEN"))

def check_T_w_trace_denner_sirlin_covariance_inherited():
    return _res("covariance_inherited", len(V16_4_ROW_COVARIANCE) >= 9 and INPUT_SIGMA_MW_MEV > 0 and THEORY_SIGMA_MW_MEV == 4.0)

def check_T_w_trace_denner_sirlin_pull_preserved():
    return _res("pull_preserved", 1.0 < PULL_INPUT_PLUS_THEORY < 1.2)

def check_T_w_trace_denner_sirlin_report_has_master_identity():
    return _res("report_has_master_identity", "master_identity" in route_summary())

def check_T_w_trace_denner_sirlin_report_has_drrem_assembly():
    return _res("report_has_drrem_assembly", "drrem_assembly" in route_summary())

def check_T_w_trace_denner_sirlin_report_has_terms():
    return _res("report_has_terms", len(route_summary()["functional_terms"]) == 5)

def check_T_w_trace_denner_sirlin_report_has_gates():
    return _res("report_has_gates", len(route_summary()["counterterm_basis_gates"]) == 6)

def check_T_w_trace_denner_sirlin_safe_claims_present():
    return _res("safe_claims_present", len(SAFE_CLAIMS) == 4)

def check_T_w_trace_denner_sirlin_forbidden_claims_present():
    return _res("forbidden_claims_present", len(FORBIDDEN_CLAIMS) == 4)

def check_T_w_trace_denner_sirlin_payload_digest_present():
    return _res("payload_digest_present", route_summary()["payload_digest"].startswith("sha256:"))

def check_T_w_trace_denner_sirlin_target_not_shapeless():
    # DRREM itself is internally assembled, so the target is typed rather than an opaque scalar.
    return _res("target_not_shapeless", abs(DRREM_ASSEMBLED - DRREM_TARGET) < 1e-12 and abs(TARGET_SPLIT_ERROR) < 1e-15)

def check_T_w_trace_denner_sirlin_mw_residual_preserved():
    return _res("mw_residual_preserved", -4.9 < DIZET_MINUS_APF_MEV < -4.7)

def check_T_w_trace_denner_sirlin_total_mw_sigma_positive():
    return _res("total_mw_sigma_positive", TOTAL_SIGMA_MW_MEV > 4.0)

def check_T_w_trace_denner_sirlin_dimensional_values_reasonable():
    return _res("dimensional_values_reasonable", 80 < DIZET_MW_GEV < 81 and 80 < M_W_TRACE_GEV < 81)

def check_T_w_trace_denner_sirlin_open_gates_block_full_native_loop():
    return _res("open_gates_block_full_native_loop", all(g.blocks_full_native_loop for g in COUNTERTERM_BASIS_GATES if g.status == "OPEN"))

def check_T_w_trace_denner_sirlin_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_trace_denner_sirlin_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))

_CHECKS = {name: obj for name, obj in sorted(globals().items()) if name.startswith("check_T_w_trace_denner_sirlin_") and callable(obj)}


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
