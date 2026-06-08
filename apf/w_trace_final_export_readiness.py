"""W_TRACE final W-export readiness aggregator bank.

v11.2 (2026-05-09 LATER-37): final readiness aggregator for the W_TRACE
on-shell route.  This module collects the terminal states from the W-route
contract, row-bundle admission, component-sum bridge, covariance bridge,
uncertainty harness, counterterm convention certificate, and physical-export
lock.  It deliberately ships with no admitted real finite-part rows and no
physical W export.  The closure here is the readiness predicate and status
roll-up, not a numerical physical W prediction.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, Tuple

from apf.w_trace_physical_export_lock import (
    W_PHYSICAL_EXPORT_LOCK_STATUS,
    RELEASE_REQUIRED_FLAGS,
    FORBIDDEN_EXPORT_INPUTS,
    export_lock_report,
    release_predicate,
    dry_positive_release_flags,
    check_T_w_physical_export_lock_bank_closure as _check_v106,
)
from apf.w_trace_counterterm_convention import (
    W_COUNTERTERM_CONVENTION_STATUS,
    COUNTERTERM_CONVENTION_CONTRACT_CERTIFIED,
    check_T_w_counterterm_convention_bank_closure as _check_v107,
)
from apf.w_trace_real_row_bundle_admission import (
    W_REAL_ROW_BUNDLE_STATUS,
    check_T_w_real_row_bundle_bank_closure as _check_v109,
)
from apf.w_trace_row_bundle_to_component_sum import (
    W_ROW_BUNDLE_TO_COMPONENT_SUM_STATUS,
    bridge_report as row_bundle_sum_bridge_report,
    dry_target_sum_bundle_rows,
    check_T_w_row_bundle_sum_bridge_bank_closure as _check_v110,
)
from apf.w_trace_admitted_row_covariance_bridge import (
    W_ADMITTED_ROW_COVARIANCE_BRIDGE_STATUS,
    bridge_report as admitted_row_covariance_bridge_report,
    dry_covariance_rows,
)
from apf.w_trace_uncertainty_propagation import (
    W_UNCERTAINTY_PROPAGATION_STATUS,
    check_T_w_uncertainty_propagation_bank_closure as _check_v105,
)
from apf.w_trace_component_sum_certificate import W_COMPONENT_SUM_CERTIFICATE_STATUS
from apf.w_trace_onshell_transport import W_TRACE_EXPECTED_GEV as W_TRACE_MASS_GEV
from apf.w_trace_finite_part_ledger import apf_anchor_delta_r_target

W_FINAL_EXPORT_READINESS_STATUS = "P_w_final_export_readiness_aggregator"
FINAL_EXPORT_READINESS_VERSION = "w_trace_final_export_readiness_v0"
FINAL_EXPORT_READINESS_MODE = "AGGREGATOR_LOCKED_NO_REAL_ROWS_NO_NUMERIC_EXPORT"

REAL_ROW_BUNDLE_SUPPLIED = False
REAL_ROW_BUNDLE_ADMITTED = False
ROW_BUNDLE_COMPONENT_SUM_BRIDGED = False
ROW_BUNDLE_COVARIANCE_BRIDGED = False
NUMERICAL_COMPONENT_SUM_CERTIFIED = False
COVARIANCE_CERTIFIED = False
UNCERTAINTY_PROPAGATION_CERTIFIED = False
COUNTERTERM_CONVENTION_CERTIFIED = bool(COUNTERTERM_CONVENTION_CONTRACT_CERTIFIED)
TARGET_SCHEME_CONTRACT_CERTIFIED = True
NO_TARGET_OBSERVABLE_CONSUMPTION_CERTIFIED = True
PHYSICAL_W_EXPORT_READY = False
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

READINESS_REQUIRED_FLAGS: Tuple[str, ...] = RELEASE_REQUIRED_FLAGS
READINESS_REPORT_FIELDS: Tuple[str, ...] = (
    "status",
    "version",
    "mode",
    "readiness_flags",
    "readiness_predicate_satisfied",
    "release_predicate_satisfied",
    "physical_W_export_ready",
    "physical_W_export_enabled",
    "exports_physical_M_W",
    "failure_reasons",
)

FORBIDDEN_READINESS_INPUTS: Tuple[str, ...] = FORBIDDEN_EXPORT_INPUTS + (
    "physical_W_export_request",
    "readiness_override",
    "manual_export_enable",
    "force_unlock",
)

UPSTREAM_STATUSES: Tuple[str, ...] = (
    W_REAL_ROW_BUNDLE_STATUS,
    W_ROW_BUNDLE_TO_COMPONENT_SUM_STATUS,
    W_ADMITTED_ROW_COVARIANCE_BRIDGE_STATUS,
    W_COMPONENT_SUM_CERTIFICATE_STATUS,
    W_UNCERTAINTY_PROPAGATION_STATUS,
    W_COUNTERTERM_CONVENTION_STATUS,
    W_PHYSICAL_EXPORT_LOCK_STATUS,
)

@dataclass(frozen=True)
class FinalExportReadinessPolicy:
    require_all_release_flags: bool = True
    require_row_bundle_component_sum_bridge: bool = True
    require_row_bundle_covariance_bridge: bool = True
    require_counterterm_convention_certificate: bool = True
    require_export_lock_release_predicate: bool = True
    allow_empty_bundle_to_unlock: bool = False
    allow_dry_rows_to_unlock: bool = False
    allow_manual_override: bool = False
    allow_observed_w_input: bool = False
    allow_apf_anchor_as_component_input: bool = False
    allow_physical_export_by_aggregator: bool = False


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def policy() -> FinalExportReadinessPolicy:
    return FinalExportReadinessPolicy()


def default_readiness_flags() -> Dict[str, bool]:
    return {
        "real_component_rows_admitted": REAL_ROW_BUNDLE_ADMITTED,
        "component_sum_certified": NUMERICAL_COMPONENT_SUM_CERTIFIED,
        "covariance_certified": COVARIANCE_CERTIFIED,
        "uncertainty_propagation_certified": UNCERTAINTY_PROPAGATION_CERTIFIED,
        "finite_counterterm_convention_certified": COUNTERTERM_CONVENTION_CERTIFIED,
        "target_scheme_contract_certified": TARGET_SCHEME_CONTRACT_CERTIFIED,
        "no_target_observable_consumption_certified": NO_TARGET_OBSERVABLE_CONSUMPTION_CERTIFIED,
    }


def readiness_predicate(flags: Mapping[str, bool] | None = None, requested_inputs: Tuple[str, ...] = ()) -> bool:
    f = dict(default_readiness_flags() if flags is None else flags)
    forbidden = set(requested_inputs).intersection(FORBIDDEN_READINESS_INPUTS)
    pol = policy()
    return bool(
        pol.require_all_release_flags
        and all(bool(f.get(k)) for k in READINESS_REQUIRED_FLAGS)
        and not forbidden
        and release_predicate(f, tuple(requested_inputs))
        and not pol.allow_empty_bundle_to_unlock
        and not pol.allow_dry_rows_to_unlock
        and not pol.allow_manual_override
        and not pol.allow_observed_w_input
        and not pol.allow_apf_anchor_as_component_input
    )


def readiness_report(
    flags: Mapping[str, bool] | None = None,
    requested_inputs: Tuple[str, ...] = (),
    physical_export_requested: bool = False,
) -> Dict[str, Any]:
    f = dict(default_readiness_flags() if flags is None else flags)
    forbidden_hit = tuple(x for x in requested_inputs if x in FORBIDDEN_READINESS_INPUTS)
    release = export_lock_report(f, requested_inputs=tuple(requested_inputs), physical_export_requested=physical_export_requested)
    ready = readiness_predicate(f, tuple(requested_inputs))
    failures = []
    for k in READINESS_REQUIRED_FLAGS:
        if not bool(f.get(k)):
            failures.append("MISSING_" + k.upper())
    if forbidden_hit:
        failures.append("FORBIDDEN_READINESS_INPUT_CONSUMED")
    if physical_export_requested and not ready:
        failures.append("PHYSICAL_W_EXPORT_REQUEST_BLOCKED_BY_READINESS_AGGREGATOR")
    return {
        "status": W_FINAL_EXPORT_READINESS_STATUS,
        "version": FINAL_EXPORT_READINESS_VERSION,
        "mode": FINAL_EXPORT_READINESS_MODE,
        "upstream_statuses": UPSTREAM_STATUSES,
        "readiness_required_flags": READINESS_REQUIRED_FLAGS,
        "readiness_flags": {k: bool(f.get(k)) for k in READINESS_REQUIRED_FLAGS},
        "forbidden_readiness_inputs": FORBIDDEN_READINESS_INPUTS,
        "forbidden_inputs_hit": forbidden_hit,
        "readiness_predicate_satisfied": ready,
        "release_predicate_satisfied": bool(release.get("release_predicate_satisfied")),
        "physical_W_export_ready": ready,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "exports_physical_scheme_masses": False,
        "physical_export_requested": bool(physical_export_requested),
        "W_TRACE_MASS_GeV": str(W_TRACE_MASS_GEV),
        "apf_anchor_delta_r_target": f"{apf_anchor_delta_r_target():.17E}",
        "failure_reasons": tuple(dict.fromkeys(failures)),
        "export_lock_report": release,
    }


def dry_all_true_flags() -> Dict[str, bool]:
    return dry_positive_release_flags()


def current_route_state() -> Dict[str, bool]:
    r = readiness_report()
    return {
        "real_row_bundle_supplied": REAL_ROW_BUNDLE_SUPPLIED,
        "real_row_bundle_admitted": REAL_ROW_BUNDLE_ADMITTED,
        "row_bundle_component_sum_bridged": ROW_BUNDLE_COMPONENT_SUM_BRIDGED,
        "row_bundle_covariance_bridged": ROW_BUNDLE_COVARIANCE_BRIDGED,
        "numerical_component_sum_certified": NUMERICAL_COMPONENT_SUM_CERTIFIED,
        "covariance_certified": COVARIANCE_CERTIFIED,
        "uncertainty_propagation_certified": UNCERTAINTY_PROPAGATION_CERTIFIED,
        "counterterm_convention_certified": COUNTERTERM_CONVENTION_CERTIFIED,
        "target_scheme_contract_certified": TARGET_SCHEME_CONTRACT_CERTIFIED,
        "no_target_observable_consumption_certified": NO_TARGET_OBSERVABLE_CONSUMPTION_CERTIFIED,
        "physical_W_export_ready": bool(r["physical_W_export_ready"]),
        "physical_W_export_enabled": PHYSICAL_W_EXPORT_ENABLED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
    }


def manifest() -> Dict[str, Any]:
    return {
        "status": W_FINAL_EXPORT_READINESS_STATUS,
        "version": FINAL_EXPORT_READINESS_VERSION,
        "mode": FINAL_EXPORT_READINESS_MODE,
        "policy": asdict(policy()),
        "upstream_statuses": UPSTREAM_STATUSES,
        "readiness_required_flags": READINESS_REQUIRED_FLAGS,
        "readiness_report_fields": READINESS_REPORT_FIELDS,
        "forbidden_readiness_inputs": FORBIDDEN_READINESS_INPUTS,
        "current_route_state": current_route_state(),
        "default_readiness_flags": default_readiness_flags(),
        "absence_certificate": readiness_report(),
    }


def _res(name: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    return {"passed": bool(passed), "status": "PASS" if passed else "FAIL", "tier": 4, "epistemic": W_FINAL_EXPORT_READINESS_STATUS, "check": name, **extra}


def check_T_w_final_export_readiness_status_declared():
    m = manifest(); return _res("status_declared", m["status"] == W_FINAL_EXPORT_READINESS_STATUS and not m["current_route_state"]["physical_W_export_enabled"], manifest=m)


def check_T_w_final_export_readiness_depends_on_v106_export_lock():
    d = _check_v106(); return _res("depends_on_v106", _passed(d) and W_PHYSICAL_EXPORT_LOCK_STATUS == "P_w_physical_export_lock")


def check_T_w_final_export_readiness_depends_on_v107_counterterm_convention():
    d = _check_v107(); return _res("depends_on_v107", _passed(d) and COUNTERTERM_CONVENTION_CERTIFIED)


def check_T_w_final_export_readiness_depends_on_v109_bundle_admission():
    d = _check_v109(); return _res("depends_on_v109", _passed(d) and W_REAL_ROW_BUNDLE_STATUS == "P_w_real_row_bundle_admission")


def check_T_w_final_export_readiness_depends_on_v110_sum_bridge():
    d = _check_v110(); return _res("depends_on_v110", _passed(d) and W_ROW_BUNDLE_TO_COMPONENT_SUM_STATUS == "P_w_row_bundle_to_component_sum_bridge")


def check_T_w_final_export_readiness_depends_on_v111_covariance_bridge():
    r = admitted_row_covariance_bridge_report()
    ok = W_ADMITTED_ROW_COVARIANCE_BRIDGE_STATUS == "P_w_admitted_row_covariance_bridge" and r.get("status") == W_ADMITTED_ROW_COVARIANCE_BRIDGE_STATUS
    return _res("depends_on_v111", ok, upstream_status=r.get("status"))


def check_T_w_final_export_readiness_depends_on_v105_uncertainty_harness():
    d = _check_v105(); return _res("depends_on_v105", _passed(d) and W_UNCERTAINTY_PROPAGATION_STATUS == "P_w_uncertainty_propagation_harness")


def check_T_w_final_export_readiness_policy_blocks_manual_override():
    p = policy(); ok = not p.allow_manual_override and not p.allow_physical_export_by_aggregator and not p.allow_empty_bundle_to_unlock and not p.allow_dry_rows_to_unlock
    return _res("policy_blocks_override", ok, policy=asdict(p))


def check_T_w_final_export_readiness_report_schema_declared():
    r = readiness_report(); return _res("report_schema", set(READINESS_REPORT_FIELDS).issubset(r.keys()) and len(READINESS_REQUIRED_FLAGS) == 7, fields=READINESS_REPORT_FIELDS)


def check_T_w_final_export_readiness_default_locked():
    r = readiness_report(); ok = not r["readiness_predicate_satisfied"] and not r["physical_W_export_ready"] and "MISSING_REAL_COMPONENT_ROWS_ADMITTED" in r["failure_reasons"]
    return _res("default_locked", ok, report=r)


def check_T_w_final_export_readiness_counterterm_convention_contributes_true():
    f = default_readiness_flags(); return _res("counterterm_convention_true", f["finite_counterterm_convention_certified"] is True and COUNTERTERM_CONVENTION_CERTIFIED)


def check_T_w_final_export_readiness_real_rows_required():
    f = dry_all_true_flags(); f["real_component_rows_admitted"] = False; r = readiness_report(f)
    return _res("requires_real_rows", not r["readiness_predicate_satisfied"] and "MISSING_REAL_COMPONENT_ROWS_ADMITTED" in r["failure_reasons"])


def check_T_w_final_export_readiness_component_sum_required():
    f = dry_all_true_flags(); f["component_sum_certified"] = False; r = readiness_report(f)
    return _res("requires_component_sum", not r["readiness_predicate_satisfied"] and "MISSING_COMPONENT_SUM_CERTIFIED" in r["failure_reasons"])


def check_T_w_final_export_readiness_covariance_required():
    f = dry_all_true_flags(); f["covariance_certified"] = False; r = readiness_report(f)
    return _res("requires_covariance", not r["readiness_predicate_satisfied"] and "MISSING_COVARIANCE_CERTIFIED" in r["failure_reasons"])


def check_T_w_final_export_readiness_uncertainty_required():
    f = dry_all_true_flags(); f["uncertainty_propagation_certified"] = False; r = readiness_report(f)
    return _res("requires_uncertainty", not r["readiness_predicate_satisfied"] and "MISSING_UNCERTAINTY_PROPAGATION_CERTIFIED" in r["failure_reasons"])


def check_T_w_final_export_readiness_counterterm_required():
    f = dry_all_true_flags(); f["finite_counterterm_convention_certified"] = False; r = readiness_report(f)
    return _res("requires_counterterm", not r["readiness_predicate_satisfied"] and "MISSING_FINITE_COUNTERTERM_CONVENTION_CERTIFIED" in r["failure_reasons"])


def check_T_w_final_export_readiness_target_scheme_required():
    f = dry_all_true_flags(); f["target_scheme_contract_certified"] = False; r = readiness_report(f)
    return _res("requires_target_scheme", not r["readiness_predicate_satisfied"] and "MISSING_TARGET_SCHEME_CONTRACT_CERTIFIED" in r["failure_reasons"])


def check_T_w_final_export_readiness_no_target_observable_consumption_required():
    f = dry_all_true_flags(); f["no_target_observable_consumption_certified"] = False; r = readiness_report(f)
    return _res("requires_no_target_obs", not r["readiness_predicate_satisfied"] and "MISSING_NO_TARGET_OBSERVABLE_CONSUMPTION_CERTIFIED" in r["failure_reasons"])


def check_T_w_final_export_readiness_all_true_predicate_only_symbolic_ready():
    f = dry_all_true_flags(); r = readiness_report(f)
    ok = r["readiness_predicate_satisfied"] and r["release_predicate_satisfied"] and not r["physical_W_export_enabled"] and not r["exports_physical_M_W"]
    return _res("all_true_predicate_only", ok, report=r)


def check_T_w_final_export_readiness_forbids_observed_w_input():
    f = dry_all_true_flags(); r = readiness_report(f, requested_inputs=("observed_M_W",))
    return _res("forbids_observed_w", not r["readiness_predicate_satisfied"] and "FORBIDDEN_READINESS_INPUT_CONSUMED" in r["failure_reasons"], report=r)


def check_T_w_final_export_readiness_forbids_apf_anchor_as_input():
    f = dry_all_true_flags(); r = readiness_report(f, requested_inputs=("APF_ANCHOR_DELTA_R_TARGET_AS_INPUT",))
    return _res("forbids_apf_anchor_input", not r["readiness_predicate_satisfied"] and r["forbidden_inputs_hit"])


def check_T_w_final_export_readiness_forbids_residual_fit_input():
    f = dry_all_true_flags(); r = readiness_report(f, requested_inputs=("W_mass_residual",))
    return _res("forbids_residual_fit", not r["readiness_predicate_satisfied"] and r["forbidden_inputs_hit"])


def check_T_w_final_export_readiness_blocks_physical_export_request_when_locked():
    r = readiness_report(physical_export_requested=True)
    return _res("blocks_locked_export_request", not r["physical_W_export_enabled"] and "PHYSICAL_W_EXPORT_REQUEST_BLOCKED_BY_READINESS_AGGREGATOR" in r["failure_reasons"], report=r)


def check_T_w_final_export_readiness_manual_override_forbidden():
    f = dry_all_true_flags(); r = readiness_report(f, requested_inputs=("manual_export_enable",))
    return _res("manual_override_forbidden", not r["readiness_predicate_satisfied"] and "manual_export_enable" in r["forbidden_inputs_hit"])


def check_T_w_final_export_readiness_current_state_matches_locked_flags():
    s = current_route_state(); ok = (not s["real_row_bundle_admitted"] and not s["numerical_component_sum_certified"] and s["counterterm_convention_certified"] and not s["physical_W_export_enabled"])
    return _res("current_state_locked", ok, state=s)


def check_T_w_final_export_readiness_sum_bridge_empty_remains_uncertified():
    r = row_bundle_sum_bridge_report()
    ok = not r.get("component_sum_certified") and not r.get("physical_W_export_enabled")
    return _res("sum_bridge_empty_uncertified", ok, report=r)


def check_T_w_final_export_readiness_covariance_bridge_empty_remains_uncertified():
    r = admitted_row_covariance_bridge_report()
    ok = not r.get("covariance_certified") and not r.get("uncertainty_propagation_certified") and not r.get("physical_W_export_enabled")
    return _res("covariance_bridge_empty_uncertified", ok, report=r)


def check_T_w_final_export_readiness_dry_rows_do_not_set_current_flags():
    s1 = row_bundle_sum_bridge_report(dry_target_sum_bundle_rows())
    s2 = admitted_row_covariance_bridge_report(dry_covariance_rows(), component_sum_certified=True, covariance_supplied=True)
    current = current_route_state()
    ok = bool(s1.get("bundle_admitted")) and bool(s2.get("covariance_certified")) and not current["real_row_bundle_admitted"] and not current["physical_W_export_enabled"]
    return _res("dry_rows_do_not_set_current_flags", ok, dry_sum=s1, dry_cov=s2, current=current)


def check_T_w_final_export_readiness_physical_mass_exports_false():
    r = readiness_report(dry_all_true_flags())
    return _res("physical_mass_exports_false", not r["exports_physical_M_W"] and not r["exports_physical_scheme_masses"], report=r)


def check_T_w_final_export_readiness_manifest_has_anchor_and_trace_mass():
    m = manifest(); a = m["absence_certificate"]
    ok = "W_TRACE_MASS_GeV" in a and "apf_anchor_delta_r_target" in a and str(W_TRACE_MASS_GEV) == a["W_TRACE_MASS_GeV"]
    return _res("manifest_anchor_trace_mass", ok, manifest=m)


def check_T_w_final_export_readiness_forbidden_inputs_named():
    required = {"observed_M_W", "APF_ANCHOR_DELTA_R_TARGET_AS_INPUT", "manual_export_enable", "force_unlock"}
    return _res("forbidden_inputs_named", required.issubset(set(FORBIDDEN_READINESS_INPUTS)), forbidden=FORBIDDEN_READINESS_INPUTS)


def check_T_w_final_export_readiness_bank_closure():
    r = readiness_report()
    m = manifest()
    ok = (
        len(CHECKS) == 32
        and r["status"] == W_FINAL_EXPORT_READINESS_STATUS
        and not r["physical_W_export_enabled"]
        and not r["exports_physical_M_W"]
        and "MISSING_REAL_COMPONENT_ROWS_ADMITTED" in r["failure_reasons"]
        and m["current_route_state"]["counterterm_convention_certified"] is True
    )
    return _res("bank_closure", ok, checked=len(CHECKS), expected=32, report=r)



CHECKS: Dict[str, Any] = {
    "T_w_final_export_readiness_status_declared": check_T_w_final_export_readiness_status_declared,
    "T_w_final_export_readiness_depends_on_v106_export_lock": check_T_w_final_export_readiness_depends_on_v106_export_lock,
    "T_w_final_export_readiness_depends_on_v107_counterterm_convention": check_T_w_final_export_readiness_depends_on_v107_counterterm_convention,
    "T_w_final_export_readiness_depends_on_v109_bundle_admission": check_T_w_final_export_readiness_depends_on_v109_bundle_admission,
    "T_w_final_export_readiness_depends_on_v110_sum_bridge": check_T_w_final_export_readiness_depends_on_v110_sum_bridge,
    "T_w_final_export_readiness_depends_on_v111_covariance_bridge": check_T_w_final_export_readiness_depends_on_v111_covariance_bridge,
    "T_w_final_export_readiness_depends_on_v105_uncertainty_harness": check_T_w_final_export_readiness_depends_on_v105_uncertainty_harness,
    "T_w_final_export_readiness_policy_blocks_manual_override": check_T_w_final_export_readiness_policy_blocks_manual_override,
    "T_w_final_export_readiness_report_schema_declared": check_T_w_final_export_readiness_report_schema_declared,
    "T_w_final_export_readiness_default_locked": check_T_w_final_export_readiness_default_locked,
    "T_w_final_export_readiness_counterterm_convention_contributes_true": check_T_w_final_export_readiness_counterterm_convention_contributes_true,
    "T_w_final_export_readiness_real_rows_required": check_T_w_final_export_readiness_real_rows_required,
    "T_w_final_export_readiness_component_sum_required": check_T_w_final_export_readiness_component_sum_required,
    "T_w_final_export_readiness_covariance_required": check_T_w_final_export_readiness_covariance_required,
    "T_w_final_export_readiness_uncertainty_required": check_T_w_final_export_readiness_uncertainty_required,
    "T_w_final_export_readiness_counterterm_required": check_T_w_final_export_readiness_counterterm_required,
    "T_w_final_export_readiness_target_scheme_required": check_T_w_final_export_readiness_target_scheme_required,
    "T_w_final_export_readiness_no_target_observable_consumption_required": check_T_w_final_export_readiness_no_target_observable_consumption_required,
    "T_w_final_export_readiness_all_true_predicate_only_symbolic_ready": check_T_w_final_export_readiness_all_true_predicate_only_symbolic_ready,
    "T_w_final_export_readiness_forbids_observed_w_input": check_T_w_final_export_readiness_forbids_observed_w_input,
    "T_w_final_export_readiness_forbids_apf_anchor_as_input": check_T_w_final_export_readiness_forbids_apf_anchor_as_input,
    "T_w_final_export_readiness_forbids_residual_fit_input": check_T_w_final_export_readiness_forbids_residual_fit_input,
    "T_w_final_export_readiness_blocks_physical_export_request_when_locked": check_T_w_final_export_readiness_blocks_physical_export_request_when_locked,
    "T_w_final_export_readiness_manual_override_forbidden": check_T_w_final_export_readiness_manual_override_forbidden,
    "T_w_final_export_readiness_current_state_matches_locked_flags": check_T_w_final_export_readiness_current_state_matches_locked_flags,
    "T_w_final_export_readiness_sum_bridge_empty_remains_uncertified": check_T_w_final_export_readiness_sum_bridge_empty_remains_uncertified,
    "T_w_final_export_readiness_covariance_bridge_empty_remains_uncertified": check_T_w_final_export_readiness_covariance_bridge_empty_remains_uncertified,
    "T_w_final_export_readiness_dry_rows_do_not_set_current_flags": check_T_w_final_export_readiness_dry_rows_do_not_set_current_flags,
    "T_w_final_export_readiness_physical_mass_exports_false": check_T_w_final_export_readiness_physical_mass_exports_false,
    "T_w_final_export_readiness_manifest_has_anchor_and_trace_mass": check_T_w_final_export_readiness_manifest_has_anchor_and_trace_mass,
    "T_w_final_export_readiness_forbidden_inputs_named": check_T_w_final_export_readiness_forbidden_inputs_named,
    "T_w_final_export_readiness_bank_closure": check_T_w_final_export_readiness_bank_closure,
}

_CHECKS: Dict[str, Any] = CHECKS


def register(registry: Dict[str, Any]) -> None:
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
    return {
        "passed": ok,
        "status": "W_TRACE_FINAL_EXPORT_READINESS_BANK_PASS" if ok else "W_TRACE_FINAL_EXPORT_READINESS_BANK_FAIL",
        "checks": rows,
        "manifest": manifest(),
    }


if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
