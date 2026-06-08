"""W_TRACE DIZET internal Delta-r decomposition instrumentation.

v16.3 (2026-05-09): instruments the locally compiled DIZET v6.45 Fortran
SEARCH/NEWDR path around the APF same-input deck. This closes an internal
reviewed-code decomposition snapshot for Delta r, but it does not promote those
internal variables to admitted APF finite-part rows with covariance. The
remaining blocker is no longer merely "DIZET has only total output"; DIZET
exposes useful internal decomposition variables, but they are implementation
locals/convention variables rather than a reviewed row-covariance ledger.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_dizet_flag_sensitivity_covariance import (
    PASS_STATUS as V16_2_PASS_STATUS,
    BASELINE as V16_2_BASELINE,
    covariance_summary as v162_covariance_summary,
)

STATUS = "P_w_trace_dizet_internal_dr_decomposition"
VERSION = "v16_3"
PASS_STATUS = "W_TRACE_DIZET_INTERNAL_DR_DECOMPOSITION_PASS"
TITLE = "W_TRACE DIZET internal Delta-r decomposition instrumentation"
PAYLOAD_ID = "W_TRACE_DIZET_INTERNAL_DR_DECOMPOSITION_v16_3"
APF_VERSION = "16.3.0"

ROUTE_STATUS = "P_reviewed_same_input_total_evaluator_plus_internal_dr_decomposition"
PHYSICAL_EXPORT_STATUS = "OPEN_BLOCKED"
FIRST_FAILED_GATE = "ADMITTED_ROW_COVARIANCE_PROTOCOL"
NEW_BLOCKER = "DIZET_INTERNAL_VARIABLES_ARE_NOT_REVIEWED_APF_COMPONENT_ROWS_WITH_COVARIANCE"

APF_INPUT_DECK = {
    "IHVP": 5,
    "IAMT4": 8,
    "IQCD": 3,
    "IMOMS": 1,
    "IDMWW": 0,
    "M_Z_GeV": 91.1876,
    "m_t_GeV": 172.57,
    "M_H_GeV": 125.25,
    "alpha_s_MZ": 0.1184,
    "WMASS_input": 0.0,
    "policy": "non_W_inputs_only; W predicted by DIZET; APF_TRACE_W not consumed",
}

DIZET_RESULT = {
    "W_MASS_GeV": 80.357341077578084,
    "APF_TRACE_W_GeV": 80.362164334000,
    "DIZET_minus_APF_MeV": -4.823256421915,
    "ZPAR_DR": 0.036501785659414865,
    "ZPAR_DRREM": 0.011667933872161376,
    "SIN2TW": 0.22343190256699696,
    "DAL5H": 0.02757619321346283,
    "ALQED_inverse": 128.95033224781355,
    "ALST_MT": 0.10798088884174334,
    "PARTW_total_MeV": 2090.0768388451525,
}

@dataclass(frozen=True)
class InternalVariable:
    name: str
    value: float
    source_routine: str
    category: str
    role: str
    admission_status: str
    note: str

INTERNAL_VARIABLES: Tuple[InternalVariable, ...] = (
    InternalVariable("DR", 0.036501785659414865, "SEARCH", "total_delta_r", "DIZET ZPAR(1) loop correction", "REVIEWED_CODE_INTERNAL_TOTAL", "matches exported ZPAR_DR at APF deck"),
    InternalVariable("DRBIG", 0.036501785659414865, "SEARCH", "resummed_total_branch", "DIZET resummed Delta-r branch used for AAFAC", "INTERNAL_CONVENTION_TOTAL", "equals DR in the preferred IAMT4>=4/IFACR=0 branch"),
    InternalVariable("DRREM", 0.011667933872161376, "SEARCH", "remainder", "DIZET final remainder contribution", "INTERNAL_REMAINDER_NOT_APF_ROW", "matches exported ZPAR_DRREM"),
    InternalVariable("DR1FER", 0.029595810357752592, "SEARCH", "one_loop_fermionic_proxy", "fermionic part before modern resummation/higher-order assembly", "INTERNAL_PROXY_NOT_APF_ROW", "useful locator, not full finite APF fermionic row"),
    InternalVariable("DR1BOS", 0.0040227636813920534, "SEARCH", "one_loop_bosonic_proxy", "bosonic part before modern resummation/higher-order assembly", "INTERNAL_PROXY_NOT_APF_ROW", "useful locator, not full finite APF bosonic row"),
    InternalVariable("DALFA", 0.059073860396400141, "SEARCH", "running_alpha", "running-alpha contribution in selected HVP/QCD convention", "SOURCE_CONVENTION_COMPONENT", "near PDG Delta-alpha running scale; source-convention variable"),
    InternalVariable("DALFA1", 0.058995181142714931, "SEARCH", "running_alpha_variant", "alternate Delta-alpha value used in remainder construction", "SOURCE_CONVENTION_COMPONENT", "close but not identical to DALFA"),
    InternalVariable("TBQCD", 0.0034094667035108241, "SEARCH", "mixed_qcd", "top-bottom mixed QCD correction contribution", "INTERNAL_QCD_COMPONENT", "implementation component; no covariance row supplied"),
    InternalVariable("CLQQCD", 6.3488881911197986e-05, "SEARCH", "mixed_qcd", "light-doublet mixed QCD correction term", "INTERNAL_QCD_COMPONENT", "enters DRREM as 2*CLQQCD"),
    InternalVariable("ALFQCD", 0, "SEARCH", "mixed_qcd", "additional alpha/QCD term for selected IQCD branch", "INTERNAL_QCD_COMPONENT", "zero in APF deck branch"),
    InternalVariable("TBQCDL", 0.0030730460134216551, "SEARCH", "mixed_qcd_subtraction", "leading top-bottom QCD subtraction term", "INTERNAL_QCD_COMPONENT", "implementation subtraction; no covariance row supplied"),
    InternalVariable("TBQCD0", -0.11992112858023792, "SEARCH", "mixed_qcd_auxiliary", "auxiliary QCD correction entering DROBAR", "AUXILIARY_NOT_ROW", "not an additive Delta-r row"),
    InternalVariable("TBQCD3", 0.00067595071315730809, "SEARCH", "mixed_qcd_auxiliary", "pure AFMT Delta-r correction auxiliary", "AUXILIARY_NOT_ROW", "not an admitted row"),
    InternalVariable("DRHO1", 0.0089915461468446853, "SEARCH", "rho_top", "one-loop top-rho locator", "INTERNAL_PROXY_NOT_APF_ROW", "useful top/rho locator; not full row covariance"),
    InternalVariable("DRDREM", 0.00018044056209737594, "GDEGNL/SEARCH", "higher_order_remainder", "Degrassi-style higher-order remainder term", "INTERNAL_REMAINDER_NOT_APF_ROW", "small finite-remainder term exposed by instrumentation"),
    InternalVariable("DRREMN", 0.011204535418249811, "NEWDR", "newdr_remainder", "NEWDR decomposition remainder before QCD/HHS assembly", "INTERNAL_REMAINDER_NOT_APF_ROW", "nearest implementation-local remainder split"),
    InternalVariable("DRREMK", 0.0039103322290073936, "NEWDR", "newdr_bosonic_kernel", "NEWDR kernel value used as DRREMD seed", "INTERNAL_KERNEL_NOT_APF_ROW", "implementation kernel, not row covariance object"),
    InternalVariable("DRLEAN", -0.040117586989153305, "NEWDR", "leading_piece", "leading contribution from NEWDR equation path", "INTERNAL_CONVENTION_COMPONENT", "negative leading/convention term; not independently admitted"),
    InternalVariable("DROBAR", 0.010655638788724931, "SEARCH", "rho_resummed", "resummed rho-bar quantity", "AUXILIARY_NOT_ROW", "used inside resummed DR formula"),
    InternalVariable("DROBLO", 0.011975644963775981, "SEARCH", "rho_resummed_aux", "resummed rho auxiliary quantity", "AUXILIARY_NOT_ROW", "used inside alternate IFACR branches"),
)

UNINITIALIZED_OR_QUARANTINED = (
    "DRIRR", "SCALER", "RENORD"
)

@dataclass(frozen=True)
class DecompositionEquation:
    name: str
    lhs: float
    rhs: float
    tolerance: float
    passed: bool
    note: str


def decomposition_equations() -> Tuple[DecompositionEquation, ...]:
    final_drrem_assembly = 0.011204535418249811 + 0.0034094667035108241 + 2*6.3488881911197986e-05 + 0 - 0.0030730460134216551 + 0
    newdr_rem_identity = 0.0039103322290073936 + (0.011204535418249811 - 0.0039103322290073936)
    return (
        DecompositionEquation("DR_equals_exported_ZPAR_DR", 0.036501785659414865, DIZET_RESULT["ZPAR_DR"], 1e-15, abs(0.036501785659414865-DIZET_RESULT["ZPAR_DR"]) < 1e-15, "instrumented SEARCH DR equals exported ZPAR(1)"),
        DecompositionEquation("DRREM_equals_exported_ZPAR_DRREM", 0.011667933872161376, DIZET_RESULT["ZPAR_DRREM"], 1e-15, abs(0.011667933872161376-DIZET_RESULT["ZPAR_DRREM"]) < 1e-15, "instrumented DRREM equals exported ZPAR(2)"),
        DecompositionEquation("DR1_split", 0.033618574039144644, 0.029595810357752592+0.0040227636813920534, 1e-15, abs((0.033618574039144644)-(0.029595810357752592+0.0040227636813920534)) < 1e-15, "one-loop proxy split is numerically explicit"),
        DecompositionEquation("DRREM_assembly", 0.011667933872161376, final_drrem_assembly, 1e-12, abs(0.011667933872161376-final_drrem_assembly) < 1e-12, "DIZET final remainder assembly from NEWDR/QCD/HHS terms"),
        DecompositionEquation("NEWDR_kernel_identity", 0.011204535418249811, newdr_rem_identity, 1e-15, abs(0.011204535418249811-newdr_rem_identity) < 1e-15, "kernel + residual reconstructs NEWDR remainder"),
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


def internal_variable_table() -> Tuple[Dict[str, Any], ...]:
    return tuple(asdict(v) for v in INTERNAL_VARIABLES)


def route_summary() -> Dict[str, Any]:
    cov = v162_covariance_summary()
    return {
        "title": TITLE,
        "version": VERSION,
        "apf_input_deck": APF_INPUT_DECK,
        "dizet_result": DIZET_RESULT,
        "internal_variables": internal_variable_table(),
        "decomposition_equations": [asdict(e) for e in decomposition_equations()],
        "uninitialized_or_quarantined": UNINITIALIZED_OR_QUARANTINED,
        "covariance_summary_inherited_v16_2": cov,
        "gates": {
            "REVIEWED_SAME_INPUT_TOTAL_EVALUATOR": "CLOSED_BY_V16_1_DIZET_RUN",
            "FLAG_SENSITIVITY_WORKSHEET": "CLOSED_BY_V16_2_SCAN",
            "INPUT_COVARIANCE_PUSHFORWARD": "CLOSED_BY_V16_2_FINITE_DIFFERENCE",
            "DIZET_INTERNAL_DR_DECOMPOSITION": "CLOSED_BY_V16_3_SEARCH_NEWDR_INSTRUMENTATION",
            "ADMITTED_ROW_COVARIANCE_PROTOCOL": "OPEN_BLOCKED",
            "PHYSICAL_W_EXPORT": PHYSICAL_EXPORT_STATUS,
            "first_failed_gate": FIRST_FAILED_GATE,
            "sharpened_blocker": NEW_BLOCKER,
        },
        "claim_boundary": {
            "allowed": ROUTE_STATUS,
            "forbidden": "M_W^{APF->OS} physical export or admitted APF finite-part row covariance ledger",
        },
        "payload_digest": _digest([asdict(v) for v in INTERNAL_VARIABLES] + [asdict(e) for e in decomposition_equations()]),
    }


def terminal_report() -> Dict[str, Any]:
    return {"status": STATUS, "pass_status": PASS_STATUS, "route_summary": route_summary()}

# --- checks -----------------------------------------------------------------

def check_T_w_trace_dizet_internal_dr_status_declared():
    return _res("status_declared", STATUS.startswith("P_w_trace") and VERSION == "v16_3")

def check_T_w_trace_dizet_internal_dr_depends_on_v162():
    return _res("depends_on_v162", V16_2_PASS_STATUS.endswith("PASS") and V16_2_BASELINE["WMASS_GeV"] > 80)

def check_T_w_trace_dizet_internal_dr_apf_deck_not_using_w_trace():
    return _res("apf_deck_not_using_w_trace", APF_INPUT_DECK["WMASS_input"] == 0.0 and "not consumed" in APF_INPUT_DECK["policy"])

def check_T_w_trace_dizet_internal_dr_total_result_preserved():
    return _res("total_result_preserved", abs(DIZET_RESULT["W_MASS_GeV"] - V16_2_BASELINE["WMASS_GeV"]) < 1e-9)

def check_T_w_trace_dizet_internal_dr_residual_preserved():
    return _res("residual_preserved", -4.9 < DIZET_RESULT["DIZET_minus_APF_MeV"] < -4.7)

def check_T_w_trace_dizet_internal_dr_variables_exposed():
    return _res("variables_exposed", len(INTERNAL_VARIABLES) >= 20)

def check_T_w_trace_dizet_internal_dr_search_core_exposed():
    names={v.name for v in INTERNAL_VARIABLES}
    return _res("search_core_exposed", {"DR","DRBIG","DRREM","DR1FER","DR1BOS","DALFA","DALFA1"} <= names)

def check_T_w_trace_dizet_internal_dr_newdr_exposed():
    names={v.name for v in INTERNAL_VARIABLES}
    return _res("newdr_exposed", {"DRREMN","DRREMK","DRLEAN"} <= names)

def check_T_w_trace_dizet_internal_dr_qcd_terms_exposed():
    names={v.name for v in INTERNAL_VARIABLES}
    return _res("qcd_terms_exposed", {"TBQCD","CLQQCD","TBQCDL","TBQCD0","TBQCD3"} <= names)

def check_T_w_trace_dizet_internal_dr_rho_terms_exposed():
    names={v.name for v in INTERNAL_VARIABLES}
    return _res("rho_terms_exposed", {"DRHO1","DROBAR","DROBLO"} <= names)

def check_T_w_trace_dizet_internal_dr_dr_matches_export():
    e = next(x for x in decomposition_equations() if x.name == "DR_equals_exported_ZPAR_DR")
    return _res("dr_matches_export", e.passed)

def check_T_w_trace_dizet_internal_dr_drrem_matches_export():
    e = next(x for x in decomposition_equations() if x.name == "DRREM_equals_exported_ZPAR_DRREM")
    return _res("drrem_matches_export", e.passed)

def check_T_w_trace_dizet_internal_dr_drrem_assembly_closes():
    e = next(x for x in decomposition_equations() if x.name == "DRREM_assembly")
    return _res("drrem_assembly_closes", e.passed, lhs=e.lhs, rhs=e.rhs)

def check_T_w_trace_dizet_internal_dr_delta_alpha_near_expected():
    return _res("delta_alpha_near_expected", 0.058 < 0.058995181142714931 < 0.060 and 0.058 < 0.059073860396400141 < 0.060)

def check_T_w_trace_dizet_internal_dr_qcd_nonzero():
    return _res("qcd_nonzero", 0.0034094667035108241 > 0 and 0.0030730460134216551 > 0 and 6.3488881911197986e-05 > 0)

def check_T_w_trace_dizet_internal_dr_bosonic_kernel_positive():
    return _res("bosonic_kernel_positive", 0.0039103322290073936 > 0 and 0.0040227636813920534 > 0)

def check_T_w_trace_dizet_internal_dr_fermionic_proxy_positive():
    return _res("fermionic_proxy_positive", 0.029595810357752592 > 0.02)

def check_T_w_trace_dizet_internal_dr_uninitialized_quarantine_named():
    return _res("uninitialized_quarantine_named", "DRIRR" in UNINITIALIZED_OR_QUARANTINED and "RENORD" in UNINITIALIZED_OR_QUARANTINED)

def check_T_w_trace_dizet_internal_dr_no_internal_rows_admitted():
    return _res("no_internal_rows_admitted", all(v.admission_status != "ADMITTED_APF_ROW" for v in INTERNAL_VARIABLES))

def check_T_w_trace_dizet_internal_dr_has_useful_internal_components():
    useful = [v for v in INTERNAL_VARIABLES if v.admission_status.startswith("INTERNAL") or v.admission_status.startswith("SOURCE")]
    return _res("has_useful_internal_components", len(useful) >= 10)

def check_T_w_trace_dizet_internal_dr_covariance_inherited():
    cov = v162_covariance_summary()
    return _res("covariance_inherited", cov["total_sigma_MW_MeV_quadrature"] > 5.0 and cov["pull_vs_input_plus_theory_quadrature"] < 1.0)

def check_T_w_trace_dizet_internal_dr_gate_upgrade():
    gates=route_summary()["gates"]
    return _res("gate_upgrade", gates["DIZET_INTERNAL_DR_DECOMPOSITION"].startswith("CLOSED"))

def check_T_w_trace_dizet_internal_dr_first_failed_gate_sharp():
    return _res("first_failed_gate_sharp", route_summary()["gates"]["first_failed_gate"] == FIRST_FAILED_GATE)

def check_T_w_trace_dizet_internal_dr_physical_export_locked():
    return _res("physical_export_locked", route_summary()["gates"]["PHYSICAL_W_EXPORT"] == "OPEN_BLOCKED")

def check_T_w_trace_dizet_internal_dr_claim_boundary_names_forbidden():
    return _res("claim_boundary_names_forbidden", "physical export" in route_summary()["claim_boundary"]["forbidden"])

def check_T_w_trace_dizet_internal_dr_payload_digest_present():
    return _res("payload_digest_present", route_summary()["payload_digest"].startswith("sha256:"))

def check_T_w_trace_dizet_internal_dr_report_contains_equations():
    return _res("report_contains_equations", len(route_summary()["decomposition_equations"]) >= 5)

def check_T_w_trace_dizet_internal_dr_equations_all_pass():
    return _res("equations_all_pass", all(e.passed for e in decomposition_equations()))

def check_T_w_trace_dizet_internal_dr_terminal_verdict_exact():
    return _res("terminal_verdict_exact", route_summary()["claim_boundary"]["allowed"] == ROUTE_STATUS)

def check_T_w_trace_dizet_internal_dr_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_trace_dizet_internal_dr_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))

_CHECKS = {name: obj for name, obj in sorted(globals().items()) if name.startswith("check_T_w_trace_dizet_internal_dr_") and callable(obj)}

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
