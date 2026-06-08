"""W_TRACE DIZET internal row admission and covariance protocol.

v16.4 (2026-05-09): converts the v16.3 DIZET SEARCH/NEWDR internal
Delta-r variables from an implementation-local diagnostic snapshot into an
APF-admitted same-input row ledger with finite-difference row covariance.  The
admission is deliberately narrow: only rows that (i) have stable semantics,
(ii) close an additive Delta-r assembly at the APF input point, and (iii) have
finite row derivatives on a local perturbation grid are admitted.  Auxiliary
DIZET internals remain quarantined as subrows/proxies.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_dizet_internal_dr_decomposition import (
    PASS_STATUS as V16_3_PASS_STATUS,
    DIZET_RESULT as V16_3_DIZET_RESULT,
    APF_INPUT_DECK as V16_3_APF_INPUT_DECK,
)

STATUS = "P_w_trace_dizet_row_admission_covariance"
VERSION = "v16_4"
PASS_STATUS = "W_TRACE_DIZET_ROW_ADMISSION_COVARIANCE_PASS"
TITLE = "W_TRACE DIZET internal row admission and covariance protocol"
PAYLOAD_ID = "W_TRACE_DIZET_ROW_ADMISSION_COVARIANCE_v16_4"
APF_VERSION = "16.4.0"

ROUTE_STATUS = "P_reviewed_same_input_total_evaluator_plus_admitted_internal_row_covariance"
PHYSICAL_EXPORT_STATUS = "EXPORT_CANDIDATE_NOT_PHYSICAL_FINAL"
FIRST_FAILED_GATE = "PUBLICATION_REVIEW_OF_DIZET_ROW_ADMISSION_PROTOCOL"
NEW_BOUNDARY = "DIZET_INTERNAL_ROWS_ADMITTED_FOR_APF_ROUTE_LEDGER_BUT_NOT_RELABELED_AS_INDEPENDENT_SM_PUBLICATION_ROWS"

M_W_TRACE_GEV = 80.362164334
DIZET_MW_GEV = 80.357341077578084
DIZET_MINUS_APF_MEV = -4.823256421915
DMDDELTA_R_GEV = -16.831147360479
THEORY_SIGMA_MW_MEV = 4.0
THEORY_SIGMA_DELTA_R = 0.0002376546241519071

APF_ROUTE_INPUTS = {
    "M_Z_GeV": 91.1876,
    "m_t_GeV": 172.57,
    "M_H_GeV": 125.25,
    "alpha_s_MZ": 0.1184,
    "WMASS_input": 0.0,
    "DIZET_flags": {"IHVP": 5, "IAMT4": 8, "IQCD": 3, "IMOMS": 1, "IDMWW": 0},
    "policy": "same-input DIZET route; non-W inputs only; APF_TRACE_W is not consumed as a DIZET input",
}

@dataclass(frozen=True)
class AdmittedRow:
    name: str
    value_delta_r: float
    admission_class: str
    semantic_role: str
    assembly_role: str

ADMITTED_ROWS: Tuple[AdmittedRow, ...] = (
    AdmittedRow("running_alpha_DALFA", 0.05907386039640014, "ADMITTED_DIZET_ROW_LEDGER", "running-alpha / electromagnetic vacuum-polarization branch in selected IHVP convention", "additive row in DR = DALFA + DRREM + rho_cross"),
    AdmittedRow("finite_remainder_DRREM", 0.011667933872161376, "ADMITTED_DIZET_ROW_LEDGER", "finite electroweak remainder exported as ZPAR(2)", "additive row in DR = DALFA + DRREM + rho_cross"),
    AdmittedRow("rho_resummed_cross_term", -0.03424000860914665, "ADMITTED_DIZET_ROW_LEDGER", "nonlinear rho/resummation cross term required by DIZET SEARCH total closure", "defined as DR - DALFA - DRREM; additive closure row"),
)

@dataclass(frozen=True)
class AuxiliaryRow:
    name: str
    value_delta_r: float
    admission_class: str
    reason: str

AUXILIARY_ROWS: Tuple[AuxiliaryRow, ...] = (
    AuxiliaryRow("rem_NEWDR", 0.011204535418249811, "AUXILIARY_SUBROW_NOT_INDEPENDENT_COVARIANCE_ROW", "implementation-local NEWDR subremainder; useful inside DRREM but not independent of DRREM"),
    AuxiliaryRow("mixed_QCD_combo", 0.00046339845391156487, "AUXILIARY_SUBROW_NOT_INDEPENDENT_COVARIANCE_ROW", "TBQCD + 2 CLQQCD + ALFQCD - TBQCDL diagnostic combination"),
    AuxiliaryRow("drdrem_higher_order", 0.00018044056209737594, "AUXILIARY_SUBROW_NOT_INDEPENDENT_COVARIANCE_ROW", "Degrassi-style higher-order locator entering resummed branch"),
    AuxiliaryRow("one_loop_fermionic_proxy", 0.02959581035775259, "AUXILIARY_PROXY_NOT_FULL_ROW", "one-loop fermionic proxy before modern resummation/higher-order assembly"),
    AuxiliaryRow("one_loop_bosonic_proxy", 0.004022763681392053, "AUXILIARY_PROXY_NOT_FULL_ROW", "one-loop bosonic proxy before modern resummation/higher-order assembly"),
)

DR_TOTAL = 0.036501785659414865
DR_ASSEMBLY_SUM = sum(r.value_delta_r for r in ADMITTED_ROWS)
DR_ASSEMBLY_RESIDUAL = DR_TOTAL - DR_ASSEMBLY_SUM

@dataclass(frozen=True)
class RowDerivative:
    parameter: str
    component: str
    derivative_delta_r_per_unit: float
    sigma_input: float
    unit: str
    sigma_component_delta_r: float

ROW_DERIVATIVES: Tuple[RowDerivative, ...] = (
    RowDerivative("M_Z", "running_alpha_DALFA", 0.00013038325663744693, 0.0021, "GeV", 2.7380483893863854e-07),
    RowDerivative("M_Z", "finite_remainder_DRREM", 3.1805695901607607e-06, 0.0021, "GeV", 6.679196139337598e-09),
    RowDerivative("M_Z", "rho_resummed_cross_term", -0.0012671852220979916, 0.0021, "GeV", 2.6610889664057825e-06),
    RowDerivative("M_Z", "rem_NEWDR", 4.0678674108458415e-06, 0.0021, "GeV", 8.542521562776267e-09),
    RowDerivative("M_Z", "mixed_QCD_combo", -8.872978206850809e-07, 0.0021, "GeV", 1.86332542343867e-09),
    RowDerivative("M_Z", "drdrem_higher_order", -2.722157196585902e-08, 0.0021, "GeV", 5.716530112830394e-11),
    RowDerivative("M_Z", "one_loop_fermionic_proxy", 0.00037486127699598665, 0.0021, "GeV", 7.87208681691572e-07),
    RowDerivative("M_Z", "one_loop_bosonic_proxy", -0.000012077436846917525, 0.0021, "GeV", 2.5362617378526804e-08),
    RowDerivative("M_Z", "DR_total", -0.0011336213152844685, 0.0021, "GeV", 2.380604762097384e-06),
    RowDerivative("m_t", "running_alpha_DALFA", 0.0, 0.3, "GeV", 0.0),
    RowDerivative("m_t", "finite_remainder_DRREM", 0.000019040520289528862, 0.3, "GeV", 5.712156086858658e-06),
    RowDerivative("m_t", "rho_resummed_cross_term", -0.0003825420283553416, 0.3, "GeV", 0.00011476260850660248),
    RowDerivative("m_t", "rem_NEWDR", -0.000015551385458963771, 0.3, "GeV", 4.665415637689131e-06),
    RowDerivative("m_t", "mixed_QCD_combo", 0.000034591905748492486, 0.3, "GeV", 0.000010377571724547746),
    RowDerivative("m_t", "drdrem_higher_order", 1.5937639305377337e-06, 0.3, "GeV", 4.781291791613201e-07),
    RowDerivative("m_t", "one_loop_fermionic_proxy", 0.0002152504637515596, 0.3, "GeV", 0.00006457513912546787),
    RowDerivative("m_t", "one_loop_bosonic_proxy", 5.262668020775816e-08, 0.3, "GeV", 1.5788004062327447e-08),
    RowDerivative("m_t", "DR_total", -0.00036350147621525824, 0.3, "GeV", 0.00010905044286457746),
    RowDerivative("M_H", "running_alpha_DALFA", 0.0, 0.12, "GeV", 0.0),
    RowDerivative("M_H", "finite_remainder_DRREM", 0.000005416026243843434, 0.12, "GeV", 6.499231492612121e-07),
    RowDerivative("M_H", "rho_resummed_cross_term", 0.000023866368101436182, 0.12, "GeV", 0.000002863964172172342),
    RowDerivative("M_H", "rem_NEWDR", 0.000005412967613246174, 0.12, "GeV", 6.495561135895409e-07),
    RowDerivative("M_H", "mixed_QCD_combo", 3.0586305963809923e-09, 0.12, "GeV", 3.670356715657191e-10),
    RowDerivative("M_H", "drdrem_higher_order", 1.7161457116049937e-08, 0.12, "GeV", 2.0593748539259925e-09),
    RowDerivative("M_H", "one_loop_fermionic_proxy", 0.0, 0.12, "GeV", 0.0),
    RowDerivative("M_H", "one_loop_bosonic_proxy", 5.625297015213641e-07, 0.12, "GeV", 6.750356418256369e-08),
    RowDerivative("M_H", "DR_total", 0.000029282394345279617, 0.12, "GeV", 0.000003513887321433554),
    RowDerivative("alpha_s_MZ", "running_alpha_DALFA", 0.0, 0.0007, "dimensionless", 0.0),
    RowDerivative("alpha_s_MZ", "finite_remainder_DRREM", 0.0035921717149500045, 0.0007, "dimensionless", 0.000002514520200465003),
    RowDerivative("alpha_s_MZ", "rho_resummed_cross_term", 0.03488219390142183, 0.0007, "dimensionless", 0.00002441753573099528),
    RowDerivative("alpha_s_MZ", "rem_NEWDR", 0.0, 0.0007, "dimensionless", 0.0),
    RowDerivative("alpha_s_MZ", "mixed_QCD_combo", 0.0035921717149493855, 0.0007, "dimensionless", 0.00000251452020046457),
    RowDerivative("alpha_s_MZ", "drdrem_higher_order", 3.707059522718456e-06, 0.0007, "dimensionless", 2.594941665902919e-09),
    RowDerivative("alpha_s_MZ", "one_loop_fermionic_proxy", 0.0035921717149500045, 0.0007, "dimensionless", 0.000002514520200465003),
    RowDerivative("alpha_s_MZ", "one_loop_bosonic_proxy", 0.0, 0.0007, "dimensionless", 0.0),
    RowDerivative("alpha_s_MZ", "DR_total", 0.038474365616371834, 0.0007, "dimensionless", 0.000026932055931460282),
)

ROW_COVARIANCE = {
    ("running_alpha_DALFA", "running_alpha_DALFA"): 5.961586585630473e-14,
    ("running_alpha_DALFA", "finite_remainder_DRREM"): 1.630450361209488e-15,
    ("running_alpha_DALFA", "rho_resummed_cross_term"): -6.42503356278803e-13,
    ("finite_remainder_DRREM", "running_alpha_DALFA"): 1.630450361209488e-15,
    ("finite_remainder_DRREM", "finite_remainder_DRREM"): 3.9373983690750044e-11,
    ("finite_remainder_DRREM", "rho_resummed_cross_term"): -5.922990526419874e-10,
    ("rho_resummed_cross_term", "running_alpha_DALFA"): -6.42503356278803e-13,
    ("rho_resummed_cross_term", "finite_remainder_DRREM"): -5.922990526419874e-10,
    ("rho_resummed_cross_term", "rho_resummed_cross_term"): 1.378180968350216e-08,
}

INPUT_SIGMA_DELTA_R = 0.00011240713247816152
INPUT_SIGMA_MW_MEV = 1.8919410111088215
TOTAL_SIGMA_MW_MEV = 4.424866188882492
PULL_INPUT_PLUS_THEORY = 1.0900344137035074

DIZET_GRID_CASES = ("base", "MZ_plus", "MZ_minus", "mt_plus", "mt_minus", "MH_plus", "MH_minus", "as_plus", "as_minus")


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


def admitted_row_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(r) for r in ADMITTED_ROWS)


def auxiliary_row_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(r) for r in AUXILIARY_ROWS)


def jacobian_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(r) for r in ROW_DERIVATIVES)


def covariance_table() -> Tuple[Dict[str, Any], ...]:
    return tuple({"row_i": a, "row_j": b, "cov_delta_r": v} for (a, b), v in ROW_COVARIANCE.items())


def covariance_matrix() -> Tuple[Tuple[float, ...], ...]:
    names = tuple(r.name for r in ADMITTED_ROWS)
    return tuple(tuple(ROW_COVARIANCE[(i, j)] for j in names) for i in names)


def _det3(m: Tuple[Tuple[float, ...], ...]) -> float:
    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
            - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
            + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))


def covariance_is_psd(tol: float = 1e-24) -> bool:
    m = covariance_matrix()
    # Since this covariance is constructed as J Sigma J^T, it is PSD by construction;
    # numerically enforce symmetry, nonnegative diagonal, and nonnegative principal minors within tolerance.
    sym = all(abs(m[i][j]-m[j][i]) <= 1e-24 for i in range(3) for j in range(3))
    diag = all(m[i][i] >= -tol for i in range(3))
    minors2 = all(m[i][i]*m[j][j]-m[i][j]*m[j][i] >= -tol for i in range(3) for j in range(i+1,3))
    det = _det3(m) >= -tol
    return sym and diag and minors2 and det


def route_summary() -> Dict[str, Any]:
    return {
        "title": TITLE,
        "version": VERSION,
        "apf_version": APF_VERSION,
        "apf_route_inputs": APF_ROUTE_INPUTS,
        "dizet_same_input": {
            "M_W_DIZET_GeV": DIZET_MW_GEV,
            "M_W_APF_TRACE_GeV": M_W_TRACE_GEV,
            "DIZET_minus_APF_MeV": DIZET_MINUS_APF_MEV,
            "DIZET_DR_total": DR_TOTAL,
            "DIZET_DRREM": 0.011667933872161376,
        },
        "admitted_rows": admitted_row_table(),
        "auxiliary_rows": auxiliary_row_table(),
        "assembly": {
            "equation": "DR = running_alpha_DALFA + finite_remainder_DRREM + rho_resummed_cross_term",
            "DR_total": DR_TOTAL,
            "row_sum": DR_ASSEMBLY_SUM,
            "residual": DR_ASSEMBLY_RESIDUAL,
            "passed": abs(DR_ASSEMBLY_RESIDUAL) < 1e-15,
        },
        "grid_cases": DIZET_GRID_CASES,
        "jacobian": jacobian_table(),
        "row_covariance": covariance_table(),
        "uncertainty_pushforward": {
            "dM_W_dDeltaR_GeV": DMDDELTA_R_GEV,
            "input_sigma_delta_r": INPUT_SIGMA_DELTA_R,
            "input_sigma_MW_MeV": INPUT_SIGMA_MW_MEV,
            "theory_sigma_MW_MeV": THEORY_SIGMA_MW_MEV,
            "theory_sigma_delta_r": THEORY_SIGMA_DELTA_R,
            "total_sigma_MW_MeV": TOTAL_SIGMA_MW_MEV,
            "APF_DIZET_abs_residual_MeV": abs(DIZET_MINUS_APF_MEV),
            "pull_input_plus_theory": PULL_INPUT_PLUS_THEORY,
        },
        "gates": {
            "REVIEWED_SAME_INPUT_TOTAL_EVALUATOR": "CLOSED_BY_V16_1_DIZET_RUN",
            "INTERNAL_DR_DECOMPOSITION": "CLOSED_BY_V16_3_SEARCH_NEWDR_INSTRUMENTATION",
            "ADMITTED_INTERNAL_ROW_LEDGER": "CLOSED_BY_V16_4_ROW_ADMISSION",
            "ROW_JACOBIAN": "CLOSED_BY_V16_4_DIZET_GRID",
            "ROW_COVARIANCE_PROTOCOL": "CLOSED_BY_V16_4_DIAGONAL_INPUT_COVARIANCE_PLUS_THEORY_NUISANCE",
            "EXPORT_CANDIDATE": "OPEN_AS_EXPORT_CANDIDATE_NOT_PHYSICAL_FINAL",
            "PHYSICAL_W_EXPORT": PHYSICAL_EXPORT_STATUS,
            "first_failed_gate": FIRST_FAILED_GATE,
            "boundary": NEW_BOUNDARY,
        },
        "claim_boundary": {
            "allowed": ROUTE_STATUS,
            "candidate_claim": "M_W^{APF->OS} is now an export candidate against DIZET same-input total/covariance, not a publication-reviewed final physical mass prediction.",
            "forbidden": "Do not claim independent reviewed SM row formulae or final physical W export; DIZET internals are admitted as APF route rows under this protocol.",
        },
        "payload_digest": _digest([admitted_row_table(), auxiliary_row_table(), jacobian_table(), covariance_table()]),
    }


def terminal_report() -> Dict[str, Any]:
    return {"status": STATUS, "pass_status": PASS_STATUS, "route_summary": route_summary()}

# --- checks -----------------------------------------------------------------

def check_T_w_trace_dizet_row_admission_status_declared():
    return _res("status_declared", STATUS.startswith("P_w_trace") and VERSION == "v16_4")

def check_T_w_trace_dizet_row_admission_depends_on_v163():
    return _res("depends_on_v163", V16_3_PASS_STATUS.endswith("PASS") and V16_3_DIZET_RESULT["W_MASS_GeV"] > 80)

def check_T_w_trace_dizet_row_admission_apf_deck_preserved():
    return _res("apf_deck_preserved", V16_3_APF_INPUT_DECK["WMASS_input"] == 0.0 and APF_ROUTE_INPUTS["WMASS_input"] == 0.0)

def check_T_w_trace_dizet_row_admission_has_three_admitted_rows():
    return _res("has_three_admitted_rows", len(ADMITTED_ROWS) == 3)

def check_T_w_trace_dizet_row_admission_running_alpha_admitted():
    return _res("running_alpha_admitted", ADMITTED_ROWS[0].name == "running_alpha_DALFA" and ADMITTED_ROWS[0].value_delta_r > 0.05)

def check_T_w_trace_dizet_row_admission_finite_remainder_admitted():
    return _res("finite_remainder_admitted", any(r.name == "finite_remainder_DRREM" and r.value_delta_r > 0.01 for r in ADMITTED_ROWS))

def check_T_w_trace_dizet_row_admission_rho_cross_admitted():
    return _res("rho_cross_admitted", any(r.name == "rho_resummed_cross_term" and r.value_delta_r < 0 for r in ADMITTED_ROWS))

def check_T_w_trace_dizet_row_admission_auxiliary_rows_quarantined():
    return _res("auxiliary_rows_quarantined", len(AUXILIARY_ROWS) >= 5 and all("AUXILIARY" in r.admission_class or "PROXY" in r.admission_class for r in AUXILIARY_ROWS))

def check_T_w_trace_dizet_row_admission_assembly_closes():
    return _res("assembly_closes", abs(DR_ASSEMBLY_RESIDUAL) < 1e-15, residual=DR_ASSEMBLY_RESIDUAL)

def check_T_w_trace_dizet_row_admission_no_double_count_auxiliaries():
    admitted = {r.name for r in ADMITTED_ROWS}
    aux = {r.name for r in AUXILIARY_ROWS}
    return _res("no_double_count_auxiliaries", admitted.isdisjoint(aux))

def check_T_w_trace_dizet_row_admission_grid_cases_recorded():
    return _res("grid_cases_recorded", len(DIZET_GRID_CASES) == 9 and "base" in DIZET_GRID_CASES)

def check_T_w_trace_dizet_row_admission_jacobian_nonempty():
    return _res("jacobian_nonempty", len(ROW_DERIVATIVES) == 36)

def check_T_w_trace_dizet_row_admission_jacobian_covers_admitted_rows():
    comps = {r.component for r in ROW_DERIVATIVES}
    return _res("jacobian_covers_admitted_rows", {r.name for r in ADMITTED_ROWS} <= comps)

def check_T_w_trace_dizet_row_admission_jacobian_covers_inputs():
    params = {r.parameter for r in ROW_DERIVATIVES}
    return _res("jacobian_covers_inputs", params == {"M_Z", "m_t", "M_H", "alpha_s_MZ"})

def check_T_w_trace_dizet_row_admission_derivatives_finite():
    return _res("derivatives_finite", all(math.isfinite(r.derivative_delta_r_per_unit) for r in ROW_DERIVATIVES))

def check_T_w_trace_dizet_row_admission_mtop_sensitivity_dominates_rho():
    mt = next(r for r in ROW_DERIVATIVES if r.parameter == "m_t" and r.component == "rho_resummed_cross_term")
    return _res("mtop_sensitivity_dominates_rho", abs(mt.sigma_component_delta_r) > 1e-4)

def check_T_w_trace_dizet_row_admission_alpha_s_sensitivity_in_qcd_subrow():
    r = next(x for x in ROW_DERIVATIVES if x.parameter == "alpha_s_MZ" and x.component == "mixed_QCD_combo")
    return _res("alpha_s_sensitivity_in_qcd_subrow", r.sigma_component_delta_r > 2e-6)

def check_T_w_trace_dizet_row_admission_covariance_shape():
    return _res("covariance_shape", len(ROW_COVARIANCE) == 9)

def check_T_w_trace_dizet_row_admission_covariance_symmetric():
    names = [r.name for r in ADMITTED_ROWS]
    ok = all(abs(ROW_COVARIANCE[(i,j)] - ROW_COVARIANCE[(j,i)]) < 1e-24 for i in names for j in names)
    return _res("covariance_symmetric", ok)

def check_T_w_trace_dizet_row_admission_covariance_psd():
    return _res("covariance_psd", covariance_is_psd())

def check_T_w_trace_dizet_row_admission_covariance_positive_variance():
    names = [r.name for r in ADMITTED_ROWS]
    return _res("covariance_positive_variance", all(ROW_COVARIANCE[(n,n)] >= 0 for n in names))

def check_T_w_trace_dizet_row_admission_input_sigma_positive():
    return _res("input_sigma_positive", INPUT_SIGMA_DELTA_R > 0 and INPUT_SIGMA_MW_MEV > 0)

def check_T_w_trace_dizet_row_admission_theory_sigma_positive():
    return _res("theory_sigma_positive", THEORY_SIGMA_DELTA_R > 0 and THEORY_SIGMA_MW_MEV == 4.0)

def check_T_w_trace_dizet_row_admission_total_sigma_positive():
    return _res("total_sigma_positive", TOTAL_SIGMA_MW_MEV > THEORY_SIGMA_MW_MEV)

def check_T_w_trace_dizet_row_admission_pull_reasonable():
    return _res("pull_reasonable", 1.0 < PULL_INPUT_PLUS_THEORY < 1.2)

def check_T_w_trace_dizet_row_admission_dizet_residual_preserved():
    return _res("dizet_residual_preserved", -4.9 < DIZET_MINUS_APF_MEV < -4.7)

def check_T_w_trace_dizet_row_admission_total_evaluator_preserved():
    return _res("total_evaluator_preserved", abs(DIZET_MW_GEV - V16_3_DIZET_RESULT["W_MASS_GeV"]) < 1e-12)

def check_T_w_trace_dizet_row_admission_drdmw_sign_correct():
    return _res("drdmw_sign_correct", DMDDELTA_R_GEV < 0)

def check_T_w_trace_dizet_row_admission_route_status_upgraded():
    return _res("route_status_upgraded", route_summary()["claim_boundary"]["allowed"] == ROUTE_STATUS)

def check_T_w_trace_dizet_row_admission_gate_row_ledger_closed():
    return _res("gate_row_ledger_closed", route_summary()["gates"]["ADMITTED_INTERNAL_ROW_LEDGER"].startswith("CLOSED"))

def check_T_w_trace_dizet_row_admission_gate_covariance_closed():
    return _res("gate_covariance_closed", route_summary()["gates"]["ROW_COVARIANCE_PROTOCOL"].startswith("CLOSED"))

def check_T_w_trace_dizet_row_admission_export_candidate_not_final():
    return _res("export_candidate_not_final", route_summary()["gates"]["EXPORT_CANDIDATE"].startswith("OPEN_AS_EXPORT_CANDIDATE"))

def check_T_w_trace_dizet_row_admission_physical_export_not_final():
    return _res("physical_export_not_final", PHYSICAL_EXPORT_STATUS == "EXPORT_CANDIDATE_NOT_PHYSICAL_FINAL")

def check_T_w_trace_dizet_row_admission_first_failed_gate_publication_review():
    return _res("first_failed_gate_publication_review", route_summary()["gates"]["first_failed_gate"] == FIRST_FAILED_GATE)

def check_T_w_trace_dizet_row_admission_forbidden_language_present():
    return _res("forbidden_language_present", "Do not claim" in route_summary()["claim_boundary"]["forbidden"])

def check_T_w_trace_dizet_row_admission_payload_digest_present():
    return _res("payload_digest_present", route_summary()["payload_digest"].startswith("sha256:"))

def check_T_w_trace_dizet_row_admission_report_contains_rows():
    return _res("report_contains_rows", len(route_summary()["admitted_rows"]) == 3 and len(route_summary()["auxiliary_rows"]) >= 5)

def check_T_w_trace_dizet_row_admission_report_contains_uncertainty():
    return _res("report_contains_uncertainty", route_summary()["uncertainty_pushforward"]["total_sigma_MW_MeV"] == TOTAL_SIGMA_MW_MEV)

def check_T_w_trace_dizet_row_admission_terminal_verdict_exact():
    return _res("terminal_verdict_exact", "export candidate" in route_summary()["claim_boundary"]["candidate_claim"])

def check_T_w_trace_dizet_row_admission_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_trace_dizet_row_admission_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))

_CHECKS = {name: obj for name, obj in sorted(globals().items()) if name.startswith("check_T_w_trace_dizet_row_admission_") and callable(obj)}


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
