"""W_TRACE Delta_r transport buildout / route-to-export scaffold.

v15.2 (2026-05-09): hard-push buildout after the v15.1 standard-total
Delta_r worksheet.  This module wires the total-Delta_r payload into a real
transport workbench: on-shell inversion, analytic push-forward Jacobian,
source-theory uncertainty translation, component-row slot contract, covariance
contract, and final export blocker.

Closed here:
    * total Delta_r -> on-shell W calculator and inverse consistency;
    * analytic dM_W/dDelta_r sensitivity at the APF trace anchor;
    * source-scale Delta_r uncertainty equivalent from ACFW's quoted W-scale;
    * route buildout checklist down to the remaining real payload rows.

Still open here:
    physical M_W export, because no reviewed APF eight-slot finite-part row
    bundle, component-sum certificate, real covariance, or propagated export
    uncertainty is supplied.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Sequence, Tuple

from apf.w_trace_acfw_delta_r_extraction_attempt import (
    APF_DELTA_R_TARGET,
    EXTRACTION_INPUTS,
    M_W_TRACE_GEV,
    invert_delta_r_from_mw,
)
from apf.w_trace_standard_delta_r_extraction_worksheet import (
    SOURCE_THEORY_UNCERTAINTY_MEV,
    standard_total_payload,
    source_total_values,
    check_T_w_standard_delta_r_worksheet_bank_closure as _check_worksheet,
)
from apf.w_trace_finite_part_skeleton import FINITE_PART_COMPONENT_ORDER, COMPONENT_SYMBOLS
from apf.w_trace_component_sum_certificate import component_sum_certificate_report
from apf.w_trace_uncertainty_propagation import (
    uncertainty_propagation_report,
    diagonal_shape_covariance,
)
from apf.w_trace_final_export_readiness import readiness_report
from apf.w_trace_physical_export_lock import export_lock_report

STATUS = "P_w_delta_r_transport_buildout"
VERSION = "v15_2"
PASS_STATUS = "W_TRACE_DELTA_R_TRANSPORT_BUILDOUT_PASS"
TITLE = "W_TRACE Delta_r transport buildout"

PAYLOAD_ID = "W_TRACE_DELTA_R_TRANSPORT_BUILDOUT_v15_2"
ON_SHELL_RELATION_ID = "GF_alpha_MZ_MW_Delta_r_on_shell_relation"

# Do not infer real finite-part rows from a source total.  These labels are the
# APF row slots that the export route requires.  They are intentionally not
# populated with numerical values here.
REQUIRED_COMPONENT_SLOTS: Tuple[str, ...] = FINITE_PART_COMPONENT_ORDER

REMAINING_BLOCKERS: Tuple[str, ...] = (
    "NO_REVIEWED_APF_EIGHT_SLOT_FINITE_PART_ROWS",
    "NO_REAL_COMPONENT_SUM_CERTIFICATE",
    "NO_REAL_COVARIANCE_MATRIX",
    "NO_EXPORT_UNCERTAINTY_PROTOCOL_CERTIFICATE",
    "SOURCE_TOTAL_NOT_A_COMPONENT_DECOMPOSITION",
)

LOCKED_STATE: Dict[str, bool] = {
    "standard_total_delta_r_payload_present": True,
    "on_shell_delta_r_to_mw_calculator_present": True,
    "analytic_jacobian_present": True,
    "source_scale_uncertainty_translated": True,
    "component_slot_contract_present": True,
    "real_component_rows_admitted": False,
    "component_sum_certified": False,
    "covariance_certified": False,
    "export_uncertainty_certified": False,
    "physical_W_export_enabled": False,
    "exports_physical_M_W": False,
}

FORBIDDEN_BUILDOUT_TOKENS: Tuple[str, ...] = (
    "observed_M_W",
    "world_average_M_W",
    "CDF_II_M_W",
    "CMS_observed_M_W",
    "PDG_observed_M_W",
    "fit_to_observed_W",
    "fit_to_APF_anchor",
    "APF_DELTA_R_TARGET_AS_SOURCE_INPUT",
    "manual_export_override",
    "physical_export_request",
)


@dataclass(frozen=True)
class OnShellInputs:
    alpha_inverse: float
    G_F_GeV_minus2: float
    M_Z_GeV: float


@dataclass(frozen=True)
class TransportSensitivity:
    evaluation_point: str
    M_W_GeV: float
    Delta_r: float
    dM_W_dDelta_r_GeV: float
    dM_W_dDelta_r_MeV: float
    dDelta_r_dM_W_per_GeV: float
    source_theory_uncertainty_MeV: float
    source_theory_uncertainty_Delta_r_equiv: float


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(obj).encode("utf-8")).hexdigest()


def contains_forbidden_token(obj: Any) -> bool:
    text = _canonical_json(obj)
    return any(tok in text for tok in FORBIDDEN_BUILDOUT_TOKENS)


def declared_on_shell_inputs() -> OnShellInputs:
    return OnShellInputs(
        alpha_inverse=float(EXTRACTION_INPUTS["alpha_inverse_for_inversion"]),
        G_F_GeV_minus2=float(EXTRACTION_INPUTS["G_F_GeV_minus2"]),
        M_Z_GeV=float(EXTRACTION_INPUTS["M_Z_GeV"]),
    )


def _A(inputs: OnShellInputs) -> float:
    alpha = 1.0 / inputs.alpha_inverse
    return math.pi * alpha / (math.sqrt(2.0) * inputs.G_F_GeV_minus2)


def mw_from_delta_r(delta_r: float, inputs: OnShellInputs | None = None) -> float:
    """Solve the on-shell G_F relation for the physical high-mass W root.

    Let x=M_W^2 and z=M_Z^2.  The equation is
        x (1 - x/z) = A/(1-Delta_r).
    The W solution is the larger root x/z > 1/2.
    """
    inp = declared_on_shell_inputs() if inputs is None else inputs
    z = inp.M_Z_GeV ** 2
    rhs = _A(inp) / (1.0 - float(delta_r))
    disc = 1.0 - 4.0 * rhs / z
    if disc <= 0.0:
        raise ValueError("Delta_r outside real on-shell W-root domain")
    x = 0.5 * z * (1.0 + math.sqrt(disc))
    return math.sqrt(x)


def delta_r_from_mw(mw_gev: float, inputs: OnShellInputs | None = None) -> float:
    inp = declared_on_shell_inputs() if inputs is None else inputs
    return invert_delta_r_from_mw(float(mw_gev), {
        **EXTRACTION_INPUTS,
        "alpha_inverse_for_inversion": inp.alpha_inverse,
        "G_F_GeV_minus2": inp.G_F_GeV_minus2,
        "M_Z_GeV": inp.M_Z_GeV,
    })


def dMW_dDelta_r(delta_r: float, inputs: OnShellInputs | None = None) -> float:
    inp = declared_on_shell_inputs() if inputs is None else inputs
    mw = mw_from_delta_r(delta_r, inp)
    x = mw ** 2
    z = inp.M_Z_GeV ** 2
    numerator = x * (1.0 - x / z)
    denominator = (1.0 - float(delta_r)) * (1.0 - 2.0 * x / z)
    dx_dD = numerator / denominator
    return dx_dD / (2.0 * mw)


def transport_sensitivity_at_trace() -> Dict[str, Any]:
    jac = dMW_dDelta_r(APF_DELTA_R_TARGET)
    inv = 1.0 / jac
    sigma_dr = (SOURCE_THEORY_UNCERTAINTY_MEV / 1000.0) / abs(jac)
    s = TransportSensitivity(
        evaluation_point="APF_TRACE_Delta_r_anchor_comparison_only",
        M_W_GeV=mw_from_delta_r(APF_DELTA_R_TARGET),
        Delta_r=APF_DELTA_R_TARGET,
        dM_W_dDelta_r_GeV=jac,
        dM_W_dDelta_r_MeV=jac * 1000.0,
        dDelta_r_dM_W_per_GeV=inv,
        source_theory_uncertainty_MeV=SOURCE_THEORY_UNCERTAINTY_MEV,
        source_theory_uncertainty_Delta_r_equiv=sigma_dr,
    )
    return asdict(s)


def source_vs_trace_transport_values() -> Dict[str, Any]:
    vals = source_total_values()
    source_mw_recomputed = mw_from_delta_r(vals["Delta_r_source_total"])
    trace_mw_from_anchor = mw_from_delta_r(APF_DELTA_R_TARGET)
    source_delta_from_source_mw = delta_r_from_mw(vals["M_W_source_GeV"])
    return {
        **vals,
        "M_W_source_recomputed_from_Delta_r_GeV": source_mw_recomputed,
        "M_W_trace_recomputed_from_APF_Delta_r_GeV": trace_mw_from_anchor,
        "Delta_r_source_recomputed_from_source_MW": source_delta_from_source_mw,
        "source_roundtrip_MW_error_GeV": source_mw_recomputed - vals["M_W_source_GeV"],
        "trace_anchor_roundtrip_MW_error_GeV": trace_mw_from_anchor - M_W_TRACE_GEV,
    }


def component_slot_contract() -> Dict[str, Any]:
    return {
        "required_payload_kind": "APF_eight_slot_finite_part_component_row_bundle",
        "component_order": REQUIRED_COMPONENT_SLOTS,
        "component_symbols": {k: COMPONENT_SYMBOLS[k] for k in REQUIRED_COMPONENT_SLOTS},
        "numeric_rows_supplied_here": False,
        "allowed_role_of_standard_total_delta_r": "comparison_and_target_scale_context_only",
        "forbidden_promotion": "do_not_split_or_backfit_a_standard_total_into_component_rows_without_source_rows",
    }


def buildout_report() -> Dict[str, Any]:
    payload = standard_total_payload()
    values = source_vs_trace_transport_values()
    sensitivity = transport_sensitivity_at_trace()
    sum_absence = component_sum_certificate_report(
        rows=None,
        rows_admitted=False,
        covariance_supplied=False,
        uncertainty_supplied=False,
        physical_export_requested=False,
    )
    cov_shape = diagonal_shape_covariance("1e-10")
    cov_mechanics = uncertainty_propagation_report(
        cov_shape,
        covariance_supplied=True,
        rows_admitted=True,
        component_sum_certified=True,
        physical_export_requested=False,
    )
    cov_real_absence = uncertainty_propagation_report(
        None,
        covariance_supplied=False,
        rows_admitted=False,
        component_sum_certified=False,
        physical_export_requested=False,
    )
    readiness = readiness_report(physical_export_requested=False)
    export_lock = export_lock_report(physical_export_requested=False)
    artifact = {
        "status": STATUS,
        "version": VERSION,
        "payload_id": PAYLOAD_ID,
        "locked_state": dict(LOCKED_STATE),
        "source_total_payload_digest": payload["source_digest"],
        "on_shell_inputs": asdict(declared_on_shell_inputs()),
        "source_vs_trace_values": values,
        "sensitivity": sensitivity,
        "component_slot_contract": component_slot_contract(),
        "component_sum_absence_certificate": sum_absence,
        "covariance_mechanics_dryrun": cov_mechanics,
        "covariance_real_absence_certificate": cov_real_absence,
        "readiness_report": readiness,
        "physical_export_lock": export_lock,
        "remaining_blockers": REMAINING_BLOCKERS,
        "verdict": "TRANSPORT_WORKBENCH_BUILT_OUT__PHYSICAL_EXPORT_BLOCKED_UNTIL_REAL_COMPONENT_ROWS_AND_COVARIANCE",
    }
    artifact["buildout_digest"] = _digest(artifact)
    return artifact


def paper_table_rows() -> Tuple[Dict[str, Any], ...]:
    r = buildout_report()
    vals = r["source_vs_trace_values"]
    sens = r["sensitivity"]
    return (
        {"quantity": "Delta_r_source_total", "value": vals["Delta_r_source_total"], "status": "standard-source total; comparison payload"},
        {"quantity": "Delta_r_APF_TRACE", "value": APF_DELTA_R_TARGET, "status": "APF trace anchor; comparison target"},
        {"quantity": "Delta_r_source_minus_APF", "value": vals["Delta_r_source_minus_APF"], "status": "residual; not a fit"},
        {"quantity": "M_W(source Delta_r)", "value": vals["M_W_source_recomputed_from_Delta_r_GeV"], "status": "roundtrip calculator check"},
        {"quantity": "M_W(APF Delta_r)", "value": vals["M_W_trace_recomputed_from_APF_Delta_r_GeV"], "status": "trace-anchor roundtrip"},
        {"quantity": "dM_W/dDelta_r", "value": sens["dM_W_dDelta_r_GeV"], "status": "local sensitivity, GeV per unit Delta_r"},
        {"quantity": "sigma_Delta_r equiv. for 4 MeV", "value": sens["source_theory_uncertainty_Delta_r_equiv"], "status": "source-scale context only"},
    )


def terminal_report() -> Dict[str, Any]:
    return {
        "status": STATUS,
        "version": VERSION,
        "title": TITLE,
        "buildout": buildout_report(),
        "paper_table_rows": paper_table_rows(),
        "claim_boundary": "calculator and route workbench closed; physical W export remains open",
    }


def _res(check: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    row = {"check": check, "passed": bool(passed), "status": "PASS" if passed else "FAIL", "epistemic": STATUS}
    row.update(extra)
    return row


def _passed(row: Any) -> bool:
    return bool(isinstance(row, Mapping) and (row.get("passed") is True or row.get("status") in ("PASS", "P")))


def check_T_w_delta_r_transport_buildout_status_declared():
    r = terminal_report()
    return _res("status_declared", r["status"] == STATUS and r["buildout"]["locked_state"]["physical_W_export_enabled"] is False)


def check_T_w_delta_r_transport_buildout_depends_on_v151_worksheet():
    d = _check_worksheet()
    return _res("depends_on_v151_worksheet", _passed(d), upstream=d.get("status"), upstream_check=d.get("check"))


def check_T_w_delta_r_transport_buildout_on_shell_roundtrip_source():
    vals = source_vs_trace_transport_values()
    ok = abs(vals["source_roundtrip_MW_error_GeV"]) < 1e-11 and abs(vals["Delta_r_source_recomputed_from_source_MW"] - vals["Delta_r_source_total"]) < 1e-14
    return _res("on_shell_roundtrip_source", ok, values=vals)


def check_T_w_delta_r_transport_buildout_trace_anchor_roundtrip():
    vals = source_vs_trace_transport_values()
    ok = abs(vals["trace_anchor_roundtrip_MW_error_GeV"]) < 1e-9
    return _res("trace_anchor_roundtrip", ok, values=vals)


def check_T_w_delta_r_transport_buildout_jacobian_negative():
    sens = transport_sensitivity_at_trace()
    ok = sens["dM_W_dDelta_r_GeV"] < 0 and sens["dM_W_dDelta_r_MeV"] < -10000
    return _res("jacobian_negative", ok, sensitivity=sens)


def check_T_w_delta_r_transport_buildout_uncertainty_equivalent_positive():
    sens = transport_sensitivity_at_trace()
    ok = 0 < sens["source_theory_uncertainty_Delta_r_equiv"] < 1e-3
    return _res("uncertainty_equivalent_positive", ok, sensitivity=sens)


def check_T_w_delta_r_transport_buildout_source_residual_matches_linear_sensitivity():
    vals = source_vs_trace_transport_values()
    sens = transport_sensitivity_at_trace()
    linear_mw_gap_gev = sens["dM_W_dDelta_r_GeV"] * vals["Delta_r_source_minus_APF"]
    actual_mw_gap_gev = vals["M_W_source_GeV"] - M_W_TRACE_GEV
    ok = abs(linear_mw_gap_gev - actual_mw_gap_gev) < 2e-5
    return _res("source_residual_matches_linear_sensitivity", ok, linear_gap_GeV=linear_mw_gap_gev, actual_gap_GeV=actual_mw_gap_gev)


def check_T_w_delta_r_transport_buildout_component_contract_exact_order():
    c = component_slot_contract()
    ok = c["component_order"] == FINITE_PART_COMPONENT_ORDER and len(c["component_order"]) == 8 and c["numeric_rows_supplied_here"] is False
    return _res("component_contract_exact_order", ok, contract=c)


def check_T_w_delta_r_transport_buildout_does_not_promote_total_to_rows():
    c = component_slot_contract()
    payload = standard_total_payload()
    ok = payload["payload_kind"] == "standard_delta_r_total" and c["numeric_rows_supplied_here"] is False and "do_not_split" in c["forbidden_promotion"]
    return _res("does_not_promote_total_to_rows", ok, payload_kind=payload["payload_kind"], contract=c)


def check_T_w_delta_r_transport_buildout_component_sum_absence_locked():
    r = buildout_report()["component_sum_absence_certificate"]
    ok = not r["component_sum_certified"] and "NO_COMPONENT_ROWS_SUPPLIED" in r["failure_reasons"]
    return _res("component_sum_absence_locked", ok, component_sum=r)


def check_T_w_delta_r_transport_buildout_covariance_dryrun_mechanics_available():
    r = buildout_report()["covariance_mechanics_dryrun"]
    ok = r["uncertainty_propagation_certified"] and r["sigma_delta_r"] is not None and not r["physical_W_export_enabled"]
    return _res("covariance_dryrun_mechanics_available", ok, covariance_dryrun=r)


def check_T_w_delta_r_transport_buildout_real_covariance_absent():
    r = buildout_report()["covariance_real_absence_certificate"]
    ok = not r["uncertainty_propagation_certified"] and "NO_COVARIANCE_MATRIX_SUPPLIED" in r["failure_reasons"]
    return _res("real_covariance_absent", ok, covariance_absence=r)


def check_T_w_delta_r_transport_buildout_forbidden_tokens_absent_from_source_material():
    report = buildout_report()
    source_material = {
        "on_shell_inputs": report["on_shell_inputs"],
        "source_total_payload_digest": report["source_total_payload_digest"],
        "component_slot_contract": report["component_slot_contract"],
    }
    ok = not contains_forbidden_token(source_material)
    return _res("forbidden_tokens_absent_from_source_material", ok)


def check_T_w_delta_r_transport_buildout_export_lock_remains_closed():
    r = buildout_report()["physical_export_lock"]
    ok = not r.get("physical_W_export_enabled", True) and not r.get("exports_physical_M_W", True)
    return _res("export_lock_remains_closed", ok, physical_export_lock=r)


def check_T_w_delta_r_transport_buildout_readiness_remains_open():
    r = buildout_report()["readiness_report"]
    ok = not r["physical_W_export_ready"] and not r["exports_physical_M_W"]
    return _res("readiness_remains_open", ok, readiness=r)


def check_T_w_delta_r_transport_buildout_digest_stable():
    d1 = buildout_report()["buildout_digest"]
    d2 = buildout_report()["buildout_digest"]
    return _res("digest_stable", d1 == d2 and d1.startswith("sha256:"), digest=d1)


def check_T_w_delta_r_transport_buildout_table_has_seven_rows():
    rows = paper_table_rows()
    ok = len(rows) == 7 and rows[0]["quantity"] == "Delta_r_source_total"
    return _res("table_has_seven_rows", ok, rows=rows)


def check_T_w_delta_r_transport_buildout_blockers_are_terminal_and_named():
    r = buildout_report()
    ok = tuple(r["remaining_blockers"]) == REMAINING_BLOCKERS and "NO_REVIEWED_APF_EIGHT_SLOT_FINITE_PART_ROWS" in r["remaining_blockers"]
    return _res("blockers_are_terminal_and_named", ok, blockers=r["remaining_blockers"])


def check_T_w_delta_r_transport_buildout_no_physical_export_claim():
    r = terminal_report()
    ok = "physical W export remains open" in r["claim_boundary"] and r["buildout"]["locked_state"]["exports_physical_M_W"] is False
    return _res("no_physical_export_claim", ok, claim_boundary=r["claim_boundary"])


def check_T_w_delta_r_transport_buildout_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_delta_r_transport_buildout_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))


_CHECKS = {
    "check_T_w_delta_r_transport_buildout_status_declared": check_T_w_delta_r_transport_buildout_status_declared,
    "check_T_w_delta_r_transport_buildout_depends_on_v151_worksheet": check_T_w_delta_r_transport_buildout_depends_on_v151_worksheet,
    "check_T_w_delta_r_transport_buildout_on_shell_roundtrip_source": check_T_w_delta_r_transport_buildout_on_shell_roundtrip_source,
    "check_T_w_delta_r_transport_buildout_trace_anchor_roundtrip": check_T_w_delta_r_transport_buildout_trace_anchor_roundtrip,
    "check_T_w_delta_r_transport_buildout_jacobian_negative": check_T_w_delta_r_transport_buildout_jacobian_negative,
    "check_T_w_delta_r_transport_buildout_uncertainty_equivalent_positive": check_T_w_delta_r_transport_buildout_uncertainty_equivalent_positive,
    "check_T_w_delta_r_transport_buildout_source_residual_matches_linear_sensitivity": check_T_w_delta_r_transport_buildout_source_residual_matches_linear_sensitivity,
    "check_T_w_delta_r_transport_buildout_component_contract_exact_order": check_T_w_delta_r_transport_buildout_component_contract_exact_order,
    "check_T_w_delta_r_transport_buildout_does_not_promote_total_to_rows": check_T_w_delta_r_transport_buildout_does_not_promote_total_to_rows,
    "check_T_w_delta_r_transport_buildout_component_sum_absence_locked": check_T_w_delta_r_transport_buildout_component_sum_absence_locked,
    "check_T_w_delta_r_transport_buildout_covariance_dryrun_mechanics_available": check_T_w_delta_r_transport_buildout_covariance_dryrun_mechanics_available,
    "check_T_w_delta_r_transport_buildout_real_covariance_absent": check_T_w_delta_r_transport_buildout_real_covariance_absent,
    "check_T_w_delta_r_transport_buildout_forbidden_tokens_absent_from_source_material": check_T_w_delta_r_transport_buildout_forbidden_tokens_absent_from_source_material,
    "check_T_w_delta_r_transport_buildout_export_lock_remains_closed": check_T_w_delta_r_transport_buildout_export_lock_remains_closed,
    "check_T_w_delta_r_transport_buildout_readiness_remains_open": check_T_w_delta_r_transport_buildout_readiness_remains_open,
    "check_T_w_delta_r_transport_buildout_digest_stable": check_T_w_delta_r_transport_buildout_digest_stable,
    "check_T_w_delta_r_transport_buildout_table_has_seven_rows": check_T_w_delta_r_transport_buildout_table_has_seven_rows,
    "check_T_w_delta_r_transport_buildout_blockers_are_terminal_and_named": check_T_w_delta_r_transport_buildout_blockers_are_terminal_and_named,
    "check_T_w_delta_r_transport_buildout_no_physical_export_claim": check_T_w_delta_r_transport_buildout_no_physical_export_claim,
    "check_T_w_delta_r_transport_buildout_bank_closure": check_T_w_delta_r_transport_buildout_bank_closure,
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
    sens = out["report"]["buildout"]["sensitivity"]
    print("dM_W/dDelta_r_GeV", f"{sens['dM_W_dDelta_r_GeV']:.12f}")
    print("sigma_Delta_r_equiv_for_4MeV", f"{sens['source_theory_uncertainty_Delta_r_equiv']:.12e}")
    raise SystemExit(0 if out["passed"] else 1)
