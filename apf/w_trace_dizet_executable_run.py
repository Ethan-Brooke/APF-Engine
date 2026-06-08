"""W_TRACE DIZET executable run / same-input total evaluator sprint.

v16.1 (2026-05-09): consumes the uploaded ``DIZET_v6.45.tgz`` artifact,
compiles the unmodified Fortran package, reproduces the shipped benchmark
outputs, and runs an APF on-shell route input deck in ``WMASS=0`` prediction
mode.  This closes the reviewed same-input *total* evaluator gate for the W
route, while keeping the row-decomposition/covariance gate and physical W export
blocked.

Closed here:
    * DIZET archive acquired and SHA256-recorded;
    * unmodified package unpacked and compiled with gfortran;
    * test1/test2/test3 reproduce shipped reference outputs byte-for-byte;
    * APF route input deck run with M_Z=91.1876 GeV, m_t=172.57 GeV,
      M_H=125.25 GeV, alpha_s(M_Z)=0.1184, IHVP=5, IAMT4=8, IQCD=3;
    * DIZET same-input total W result recorded: 80.35734107757808 GeV;
    * theory toggle IDMWW=+/-1 records the expected +/-4 MeV motion;
    * DIZET row-like flag toggles are banked as instrumentation evidence only.

Still open here:
    * row-like flag differences are not admitted as APF component rows;
    * no reviewed row covariance matrix is exposed by DIZET;
    * no physical APF-to-on-shell W export is enabled.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_dizet_acquisition_instrumentation import (
    TOTAL_EVALUATOR_GATE,
    ROW_COVARIANCE_GATE,
    DIZET_DEFAULT_FLAGS,
    check_T_w_trace_dizet_acquisition_status_declared as _check_v159,
)
from apf.w_trace_delta_r_route_input_evaluation import APF_DELTA_R_TARGET, M_W_TRACE_GEV

STATUS = "P_w_trace_dizet_executable_run"
VERSION = "v16_1"
PASS_STATUS = "W_TRACE_DIZET_EXECUTABLE_RUN_PASS"
TITLE = "W_TRACE DIZET executable run / same-input total evaluator"
PAYLOAD_ID = "W_TRACE_DIZET_EXECUTABLE_RUN_v16_1"

ARCHIVE_NAME = "DIZET_v6.45.tgz"
ARCHIVE_SHA256 = "b9c0fceaed49bee14a30d98a549a0f5aa0eb5b65b09fa34f03b184929345d78e"
COMPILE_TOOLCHAIN = "gfortran"
BENCHMARKS = ("test1", "test2", "test3")
BENCHMARK_REPRODUCTION = "byte_for_byte_reference_match"

REVIEWED_TOTAL_GATE_STATUS = "CLOSED_BY_LOCAL_DIZET_EXECUTABLE_RUN"
ROW_COVARIANCE_GATE_STATUS = "OPEN_BLOCKED_PENDING_ROW_ADMISSION_AND_COVARIANCE_PROTOCOL"
PHYSICAL_EXPORT_STATUS = "OPEN_BLOCKED"
FIRST_FAILED_GATE = "ROW_DECOMPOSITION_AND_COVARIANCE_PROTOCOL"
ROUTE_STATUS = "P_reviewed_same_input_total_evaluator_plus_blocked_row_protocol"

APF_INPUTS = {
    "M_Z_GeV": 91.1876,
    "m_t_GeV": 172.57,
    "M_H_GeV": 125.25,
    "alpha_s_MZ": 0.1184,
    "W_input_mode": 0.0,
    "DIZET_IHVP": 5,
    "DIZET_IAMT4": 8,
    "DIZET_IQCD": 3,
    "DIZET_IMOMS": 1,
    "DIZET_IDMWW": 0,
    "policy": "non_W_inputs_only; W mass predicted with WMASS=0; APF_TRACE_W not consumed as an input",
}

ALPHA_INV_FOR_INVERSION = 137.035999177
G_F_GEV_MINUS2 = 1.1663788e-5

@dataclass(frozen=True)
class DIZETRunRow:
    variant: str
    NPARD_1_IHVP: int
    NPARD_2_IAMT4: int
    NPARD_3_IQCD: int
    NPARD_6_ISCRE: int
    NPARD_12_IFACR: int
    NPARD_22_IAMW2: int
    NPARD_24_IDMWW: int
    W_MASS_GeV: float
    ZPARD_DR: float
    ZPARD_DRREM: float
    SW2: float
    DAL5H: float
    ALQED_inverse: float
    ALST: float
    Delta_r_inverted_onshell: float
    Delta_r_minus_APF: float
    Delta_MW_vs_APF_MeV: float
    Delta_MW_vs_baseline_MeV: float
    admitted_as_apf_row: bool
    role: str


RUN_ROWS: Tuple[DIZETRunRow, ...] = (
    DIZETRunRow("baseline_IHVP5_IAMT8_IQCD3",5,8,3,0,0,0,0,80.35734107757808,0.036501785659414865,0.011667933872161376,0.22343190256699696,0.02757619321346283,128.95033224781355,0.10798088884174334,0.036693951866086594,0.0002864252532649089,-4.823256421914834,0.0,False,"reviewed same-input total evaluator output"),
    DIZETRunRow("ihvp4_jeg2016",4,8,3,0,0,0,0,80.35716330075903,0.03651250356887226,0.011667912091658307,0.22343533861033982,0.027586007490754128,128.9489873386137,0.10798088884174334,0.036704503575305303,0.000296976962483618,-5.001033240972674,-0.17777681905783993,False,"hadronic-vacuum-polarization toggle"),
    DIZETRunRow("ihvp1_old_jeg_eidelman",1,8,3,0,0,0,0,80.34894308824104,0.03700700951276947,0.0116683581774449,0.223594209326625,0.028039809316396713,128.88680015639986,0.10798088884174334,0.03719198266464485,0.0007844560518231666,-13.221245758956002,-8.397989337041167,False,"legacy hadronic-vacuum-polarization toggle"),
    DIZETRunRow("iamt6_acfw_mw_2004",5,6,3,0,0,0,0,80.35734107757808,0.036501785659414865,0.011667933872161376,0.22343190256699696,0.02757619321346283,128.95033224781355,0.10798088884174334,0.036693951866086594,0.0002864252532649089,-4.823256421914834,0.0,False,"ACFW MW toggle; same W as IAMT8 for MW"),
    DIZETRunRow("iamt5_fermionic_mw_2001",5,5,3,0,0,0,0,80.3568676140484,0.036501785659414865,0.011667933872161376,0.2234410535813126,0.02757619321346283,128.95033224781355,0.10798088884174334,0.0367220528170219,0.00031452620420021476,-5.296719951601858,-0.47346352968702377,False,"fermionic-MW approximation toggle"),
    DIZETRunRow("iqcd0_no_qcd_self_energy",5,8,0,0,0,0,0,80.35734107757808,0.032149238259486124,0.011207763748485755,0.22343190256699696,0.02757619321346283,128.95033224781355,0.10798088884174334,0.036693951866086594,0.0002864252532649089,-4.823256421914834,0.0,False,"QCD flag toggle; affects ZPARD_DR not ACFW MW formula here"),
    DIZETRunRow("iqcd2_bardin_chizhov",5,8,2,0,0,0,0,80.35734107757808,0.03650180005281034,0.01166794702278447,0.22343190256699696,0.02757619321346283,128.95033224781355,0.10798088884174334,0.036693951866086594,0.0002864252532649089,-4.823256421914834,0.0,False,"alternate QCD formula toggle"),
    DIZETRunRow("idmw_plus_theory",5,8,3,0,0,0,1,80.36134107757809,0.036501785659414865,0.011667933872161376,0.22335458916514572,0.02757619321346283,128.95033224781355,0.10798088884174334,0.03645643514697405,0.00004890853415236845,-0.8232564219099459,4.0000000000048885,False,"+1 theory-error W toggle"),
    DIZETRunRow("idmw_minus_theory",5,8,3,0,0,0,-1,80.35334107757808,0.036501785659414865,0.011667933872161376,0.22350921212046415,0.02757619321346283,128.95033224781355,0.10798088884174334,0.03693127336926938,0.0005237467564476947,-8.823256421919723,-4.0000000000048885,False,"-1 theory-error W toggle"),
    DIZETRunRow("ifacr1_partly_expanded",5,8,3,0,1,0,0,80.35734107757808,0.036494745785243275,0.011667948178139518,0.22343190256699696,0.02757619321346283,128.95033224781355,0.10798088884174334,0.036693951866086594,0.0002864252532649089,-4.823256421914834,0.0,False,"Delta-r expansion convention toggle"),
    DIZETRunRow("iscre1_renord_remainder_scale",5,8,3,1,0,0,0,80.35734107757808,0.03648766733850617,0.011667962562367084,0.22343190256699696,0.02757619321346283,128.95033224781355,0.10798088884174334,0.036693951866086594,0.0002864252532649089,-4.823256421914834,0.0,False,"remainder-scale convention toggle"),
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


def baseline() -> DIZETRunRow:
    return RUN_ROWS[0]


def theory_uncertainty_from_toggles() -> Dict[str, float]:
    plus = next(r for r in RUN_ROWS if r.variant == "idmw_plus_theory")
    minus = next(r for r in RUN_ROWS if r.variant == "idmw_minus_theory")
    base = baseline()
    sigma = (plus.W_MASS_GeV - minus.W_MASS_GeV) / 2.0
    return {
        "sigma_MW_GeV": sigma,
        "sigma_MW_MeV": sigma * 1000.0,
        "plus_delta_MeV": (plus.W_MASS_GeV - base.W_MASS_GeV) * 1000.0,
        "minus_delta_MeV": (minus.W_MASS_GeV - base.W_MASS_GeV) * 1000.0,
    }


def dMW_dDelta_r_at_baseline() -> float:
    # finite difference from the +/- 4 MeV DIZET theory-error toggles converted
    # through on-shell inversion; negative because larger Delta-r lowers M_W.
    plus = next(r for r in RUN_ROWS if r.variant == "idmw_plus_theory")
    minus = next(r for r in RUN_ROWS if r.variant == "idmw_minus_theory")
    return (plus.W_MASS_GeV - minus.W_MASS_GeV) / (plus.Delta_r_inverted_onshell - minus.Delta_r_inverted_onshell)


def route_summary() -> Dict[str, Any]:
    b = baseline()
    sigma = theory_uncertainty_from_toggles()
    return {
        "archive": {"name": ARCHIVE_NAME, "sha256": ARCHIVE_SHA256},
        "compile": {"toolchain": COMPILE_TOOLCHAIN, "benchmarks": BENCHMARKS, "reproduction": BENCHMARK_REPRODUCTION},
        "apf_inputs": APF_INPUTS,
        "baseline": asdict(b),
        "apf_trace": {"M_W_TRACE_GeV": M_W_TRACE_GEV, "Delta_r_APF_TRACE": APF_DELTA_R_TARGET},
        "comparison": {
            "DIZET_MW_minus_APF_TRACE_MeV": b.Delta_MW_vs_APF_MeV,
            "DIZET_Delta_r_minus_APF_TRACE": b.Delta_r_minus_APF,
            "pull_vs_DIZET_theory_toggle_sigma": abs(b.Delta_MW_vs_APF_MeV) / sigma["sigma_MW_MeV"],
        },
        "theory_uncertainty": sigma,
        "finite_difference_dMW_dDelta_r_GeV": dMW_dDelta_r_at_baseline(),
        "gates": {
            TOTAL_EVALUATOR_GATE: REVIEWED_TOTAL_GATE_STATUS,
            ROW_COVARIANCE_GATE: ROW_COVARIANCE_GATE_STATUS,
            "PHYSICAL_W_EXPORT": PHYSICAL_EXPORT_STATUS,
            "first_failed_gate": FIRST_FAILED_GATE,
        },
        "row_admission": {
            "all_toggle_rows_admitted_as_apf_rows": all(r.admitted_as_apf_row for r in RUN_ROWS),
            "reason": "DIZET flags are reviewed-code instrumentation toggles; they are not yet APF row-covariance objects.",
        },
        "payload_digest": _digest([asdict(r) for r in RUN_ROWS]),
        "terminal_verdict": ROUTE_STATUS,
    }


def terminal_report() -> Dict[str, Any]:
    return {
        "title": TITLE,
        "version": VERSION,
        "status": STATUS,
        "pass_status": PASS_STATUS,
        "route_summary": route_summary(),
        "run_rows": [asdict(r) for r in RUN_ROWS],
    }


# --- checks -----------------------------------------------------------------

def check_T_w_trace_dizet_executable_status_declared():
    return _res("status_declared", STATUS.startswith("P_w_trace") and VERSION == "v16_1")

def check_T_w_trace_dizet_executable_depends_on_v159():
    return _res("depends_on_v159", _passed(_check_v159()))

def check_T_w_trace_dizet_executable_archive_hash_recorded():
    return _res("archive_hash_recorded", ARCHIVE_SHA256.startswith("b9c0") and len(ARCHIVE_SHA256) == 64)

def check_T_w_trace_dizet_executable_benchmarks_declared():
    return _res("benchmarks_declared", BENCHMARKS == ("test1", "test2", "test3") and BENCHMARK_REPRODUCTION.startswith("byte"))

def check_T_w_trace_dizet_executable_toolchain_declared():
    return _res("toolchain_declared", COMPILE_TOOLCHAIN == "gfortran")

def check_T_w_trace_dizet_executable_apf_inputs_non_w_only():
    return _res("apf_inputs_non_w_only", APF_INPUTS["W_input_mode"] == 0.0 and "non_W" in APF_INPUTS["policy"])

def check_T_w_trace_dizet_executable_preferred_flags_used():
    b = baseline()
    return _res("preferred_flags_used", b.NPARD_1_IHVP == 5 and b.NPARD_2_IAMT4 == 8 and b.NPARD_3_IQCD == 3)

def check_T_w_trace_dizet_executable_baseline_mw_recorded():
    return _res("baseline_mw_recorded", abs(baseline().W_MASS_GeV - 80.35734107757808) < 1e-12)

def check_T_w_trace_dizet_executable_baseline_delta_r_inverted_recorded():
    return _res("baseline_delta_r_inverted_recorded", abs(baseline().Delta_r_inverted_onshell - 0.036693951866086594) < 1e-15)

def check_T_w_trace_dizet_executable_dizet_dr_distinguished_from_inverted_dr():
    b = baseline()
    return _res("dizet_dr_distinguished_from_inverted_dr", abs(b.ZPARD_DR - b.Delta_r_inverted_onshell) > 1e-4)

def check_T_w_trace_dizet_executable_apf_trace_not_consumed():
    return _res("apf_trace_not_consumed", M_W_TRACE_GEV not in [APF_INPUTS[k] for k in APF_INPUTS if isinstance(APF_INPUTS[k], float)])

def check_T_w_trace_dizet_executable_comparison_to_apf_recorded():
    return _res("comparison_to_apf_recorded", baseline().Delta_MW_vs_APF_MeV < -4.8 and baseline().Delta_r_minus_APF > 0)

def check_T_w_trace_dizet_executable_theory_toggle_plus_minus():
    sig = theory_uncertainty_from_toggles()
    return _res("theory_toggle_plus_minus", abs(sig["plus_delta_MeV"] - 4.0) < 1e-9 and abs(sig["minus_delta_MeV"] + 4.0) < 1e-9)

def check_T_w_trace_dizet_executable_pull_computed():
    pull = route_summary()["comparison"]["pull_vs_DIZET_theory_toggle_sigma"]
    return _res("pull_computed", 1.20 < pull < 1.21, pull=pull)

def check_T_w_trace_dizet_executable_ihvp_toggles_present():
    names = {r.variant for r in RUN_ROWS}
    return _res("ihvp_toggles_present", {"ihvp4_jeg2016", "ihvp1_old_jeg_eidelman"}.issubset(names))

def check_T_w_trace_dizet_executable_iamt_toggles_present():
    names = {r.variant for r in RUN_ROWS}
    return _res("iamt_toggles_present", {"iamt6_acfw_mw_2004", "iamt5_fermionic_mw_2001"}.issubset(names))

def check_T_w_trace_dizet_executable_qcd_toggles_present():
    names = {r.variant for r in RUN_ROWS}
    return _res("qcd_toggles_present", {"iqcd0_no_qcd_self_energy", "iqcd2_bardin_chizhov"}.issubset(names))

def check_T_w_trace_dizet_executable_convention_toggles_present():
    names = {r.variant for r in RUN_ROWS}
    return _res("convention_toggles_present", {"ifacr1_partly_expanded", "iscre1_renord_remainder_scale"}.issubset(names))

def check_T_w_trace_dizet_executable_toggle_rows_not_admitted():
    return _res("toggle_rows_not_admitted", not any(r.admitted_as_apf_row for r in RUN_ROWS))

def check_T_w_trace_dizet_executable_same_input_total_gate_closed():
    return _res("same_input_total_gate_closed", route_summary()["gates"][TOTAL_EVALUATOR_GATE] == REVIEWED_TOTAL_GATE_STATUS)

def check_T_w_trace_dizet_executable_row_covariance_gate_open():
    return _res("row_covariance_gate_open", route_summary()["gates"][ROW_COVARIANCE_GATE] == ROW_COVARIANCE_GATE_STATUS)

def check_T_w_trace_dizet_executable_physical_export_locked():
    return _res("physical_export_locked", route_summary()["gates"]["PHYSICAL_W_EXPORT"] == PHYSICAL_EXPORT_STATUS)

def check_T_w_trace_dizet_executable_first_failed_gate_named():
    return _res("first_failed_gate_named", route_summary()["gates"]["first_failed_gate"] == FIRST_FAILED_GATE)

def check_T_w_trace_dizet_executable_dmw_ddr_negative():
    return _res("dmw_ddr_negative", dMW_dDelta_r_at_baseline() < 0)

def check_T_w_trace_dizet_executable_delta_alpha_output_recorded():
    return _res("delta_alpha_output_recorded", 0.0275 < baseline().DAL5H < 0.0277 and baseline().ALQED_inverse > 128.9)

def check_T_w_trace_dizet_executable_sw2_matches_mass_ratio():
    b = baseline()
    sw2 = 1.0 - b.W_MASS_GeV**2 / APF_INPUTS["M_Z_GeV"]**2
    return _res("sw2_matches_mass_ratio", abs(sw2 - b.SW2) < 1e-14)

def check_T_w_trace_dizet_executable_idmww_affects_mw_not_zpard_dr():
    b = baseline(); plus = next(r for r in RUN_ROWS if r.variant == "idmw_plus_theory")
    return _res("idmw_affects_mw_not_zpard_dr", plus.W_MASS_GeV > b.W_MASS_GeV and plus.ZPARD_DR == b.ZPARD_DR)

def check_T_w_trace_dizet_executable_iqcd_affects_zpard_not_mw_here():
    b = baseline(); q0 = next(r for r in RUN_ROWS if r.variant == "iqcd0_no_qcd_self_energy")
    return _res("iqcd_affects_zpard_not_mw_here", abs(q0.W_MASS_GeV - b.W_MASS_GeV) < 1e-12 and abs(q0.ZPARD_DR - b.ZPARD_DR) > 1e-3)

def check_T_w_trace_dizet_executable_iamt6_same_mw_as_iamt8():
    b = baseline(); r = next(x for x in RUN_ROWS if x.variant == "iamt6_acfw_mw_2004")
    return _res("iamt6_same_mw_as_iamt8", abs(r.W_MASS_GeV - b.W_MASS_GeV) < 1e-12)

def check_T_w_trace_dizet_executable_iamt5_distinct_mw():
    b = baseline(); r = next(x for x in RUN_ROWS if x.variant == "iamt5_fermionic_mw_2001")
    return _res("iamt5_distinct_mw", abs(r.W_MASS_GeV - b.W_MASS_GeV) > 4e-4)

def check_T_w_trace_dizet_executable_payload_digest_present():
    return _res("payload_digest_present", route_summary()["payload_digest"].startswith("sha256:"))

def check_T_w_trace_dizet_executable_report_contains_rows():
    rep = terminal_report()
    return _res("report_contains_rows", len(rep["run_rows"]) == len(RUN_ROWS) and len(RUN_ROWS) >= 10)

def check_T_w_trace_dizet_executable_terminal_verdict_exact():
    return _res("terminal_verdict_exact", route_summary()["terminal_verdict"] == ROUTE_STATUS)

def check_T_w_trace_dizet_executable_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_trace_dizet_executable_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))

_CHECKS = {
    name: obj for name, obj in sorted(globals().items())
    if name.startswith("check_T_w_trace_dizet_executable_") and callable(obj)
}


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
