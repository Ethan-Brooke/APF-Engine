"""W_TRACE physical export lock / release predicate bank.

v10.6 (2026-05-09 LATER-28): terminal W-route export lock after the
v10.5 uncertainty-propagation harness.  This module defines the exact release
predicate for exporting a physical on-shell W value from the W_TRACE route.  It
ships locked: no real component rows, component-sum certificate, covariance,
uncertainty, finite counterterm convention, or physical-export request is
admitted.  The module closes only the release logic and anti-smuggling guard.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, Tuple

from apf.w_trace_uncertainty_propagation import (
    W_UNCERTAINTY_PROPAGATION_STATUS,
    manifest as uncertainty_manifest,
    uncertainty_propagation_report,
    diagonal_shape_covariance,
    check_T_w_uncertainty_propagation_bank_closure as _check_v105,
)
from apf.w_trace_component_sum_certificate import W_COMPONENT_SUM_CERTIFICATE_STATUS
from apf.w_trace_finite_part_ledger import apf_anchor_delta_r_target
from apf.w_trace_onshell_transport import W_TRACE_EXPECTED_GEV as W_TRACE_MASS_GEV
from apf.trace_transport_completion import (
    check_T_physical_export_gate_locked_until_all_certificates_filled as _check_completion,
)

W_PHYSICAL_EXPORT_LOCK_STATUS = "P_w_physical_export_lock"
PHYSICAL_EXPORT_LOCK_DECLARED = True
PHYSICAL_EXPORT_LOCK_VERSION = "w_trace_physical_export_lock_v0"
PHYSICAL_EXPORT_LOCK_MODE = "LOCKED_NO_REAL_ROWS_NO_COMPONENT_SUM_NO_COVARIANCE_NO_PHYSICAL_EXPORT"

REAL_COMPONENT_ROWS_ADMITTED = False
COMPONENT_SUM_CERTIFIED = False
COVARIANCE_CERTIFIED = False
UNCERTAINTY_PROPAGATION_CERTIFIED = False
FINITE_COUNTERTERM_CONVENTION_CERTIFIED = False
TARGET_SCHEME_CONTRACT_CERTIFIED = True
NO_TARGET_OBSERVABLE_CONSUMPTION_CERTIFIED = True
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

RELEASE_REQUIRED_FLAGS: Tuple[str, ...] = (
    "real_component_rows_admitted",
    "component_sum_certified",
    "covariance_certified",
    "uncertainty_propagation_certified",
    "finite_counterterm_convention_certified",
    "target_scheme_contract_certified",
    "no_target_observable_consumption_certified",
)

EXPORT_REPORT_FIELDS: Tuple[str, ...] = (
    "status",
    "version",
    "release_required_flags",
    "release_flags",
    "release_predicate_satisfied",
    "physical_W_export_enabled",
    "exports_physical_M_W",
    "exports_physical_scheme_masses",
    "failure_reasons",
)

FORBIDDEN_EXPORT_INPUTS: Tuple[str, ...] = (
    "observed_M_W",
    "observed_M_W_uncertainty",
    "M_W_world_average",
    "world_average_W_mass_column",
    "W_mass_residual",
    "W_mass_residual_column",
    "Delta_r_fit_to_observed_M_W",
    "APF_ANCHOR_DELTA_R_TARGET_AS_INPUT",
    "component_sum_residual_to_apf_target_as_input",
    "identity_W_TRACE_to_on_shell_M_W",
)

@dataclass(frozen=True)
class WPhysicalExportPolicy:
    require_all_release_flags: bool = True
    require_no_target_observable_consumption: bool = True
    require_counterterm_convention: bool = True
    require_uncertainty_propagation: bool = True
    allow_identity_trace_to_physical_export: bool = False
    allow_apf_anchor_as_component_input: bool = False
    allow_observed_w_input: bool = False
    allow_partial_release: bool = False


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def policy() -> WPhysicalExportPolicy:
    return WPhysicalExportPolicy()


def default_release_flags() -> Dict[str, bool]:
    return {
        "real_component_rows_admitted": REAL_COMPONENT_ROWS_ADMITTED,
        "component_sum_certified": COMPONENT_SUM_CERTIFIED,
        "covariance_certified": COVARIANCE_CERTIFIED,
        "uncertainty_propagation_certified": UNCERTAINTY_PROPAGATION_CERTIFIED,
        "finite_counterterm_convention_certified": FINITE_COUNTERTERM_CONVENTION_CERTIFIED,
        "target_scheme_contract_certified": TARGET_SCHEME_CONTRACT_CERTIFIED,
        "no_target_observable_consumption_certified": NO_TARGET_OBSERVABLE_CONSUMPTION_CERTIFIED,
    }


def release_predicate(flags: Mapping[str, bool] | None = None, requested_inputs: Tuple[str, ...] = ()) -> bool:
    f = dict(default_release_flags() if flags is None else flags)
    required_ok = all(bool(f.get(k)) for k in RELEASE_REQUIRED_FLAGS)
    forbidden_absent = not set(requested_inputs).intersection(FORBIDDEN_EXPORT_INPUTS)
    pol = policy()
    return bool(
        pol.require_all_release_flags
        and required_ok
        and forbidden_absent
        and not pol.allow_identity_trace_to_physical_export
        and not pol.allow_observed_w_input
        and not pol.allow_apf_anchor_as_component_input
    )


def export_lock_report(
    flags: Mapping[str, bool] | None = None,
    requested_inputs: Tuple[str, ...] = (),
    physical_export_requested: bool = False,
) -> Dict[str, Any]:
    f = dict(default_release_flags() if flags is None else flags)
    forbidden_hit = tuple(x for x in requested_inputs if x in FORBIDDEN_EXPORT_INPUTS)
    release_ok = release_predicate(f, requested_inputs)
    failures = []
    for k in RELEASE_REQUIRED_FLAGS:
        if not bool(f.get(k)):
            failures.append("MISSING_" + k.upper())
    if forbidden_hit:
        failures.append("FORBIDDEN_EXPORT_INPUT_CONSUMED")
    if physical_export_requested and not release_ok:
        failures.append("PHYSICAL_W_EXPORT_REQUEST_BLOCKED_BY_RELEASE_PREDICATE")
    return {
        "status": W_PHYSICAL_EXPORT_LOCK_STATUS,
        "version": PHYSICAL_EXPORT_LOCK_VERSION,
        "release_required_flags": RELEASE_REQUIRED_FLAGS,
        "release_flags": {k: bool(f.get(k)) for k in RELEASE_REQUIRED_FLAGS},
        "forbidden_export_inputs": FORBIDDEN_EXPORT_INPUTS,
        "forbidden_inputs_hit": forbidden_hit,
        "release_predicate_satisfied": release_ok,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "exports_physical_scheme_masses": False,
        "physical_export_requested": bool(physical_export_requested),
        "failure_reasons": tuple(dict.fromkeys(failures)),
    }


def dry_positive_release_flags() -> Dict[str, bool]:
    return {k: True for k in RELEASE_REQUIRED_FLAGS}


def manifest() -> Dict[str, Any]:
    return {
        "status": W_PHYSICAL_EXPORT_LOCK_STATUS,
        "upstream_status": W_UNCERTAINTY_PROPAGATION_STATUS,
        "component_sum_status": W_COMPONENT_SUM_CERTIFICATE_STATUS,
        "version": PHYSICAL_EXPORT_LOCK_VERSION,
        "mode": PHYSICAL_EXPORT_LOCK_MODE,
        "policy": asdict(policy()),
        "release_required_flags": RELEASE_REQUIRED_FLAGS,
        "export_report_fields": EXPORT_REPORT_FIELDS,
        "forbidden_export_inputs": FORBIDDEN_EXPORT_INPUTS,
        "W_TRACE_MASS_GeV": str(W_TRACE_MASS_GEV),
        "apf_anchor_delta_r_target": f"{apf_anchor_delta_r_target():.17E}",
        "default_release_flags": default_release_flags(),
        "physical_W_export_enabled": PHYSICAL_W_EXPORT_ENABLED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "absence_certificate": export_lock_report(),
    }


def check_T_w_physical_export_lock_status_declared():
    p = PHYSICAL_EXPORT_LOCK_DECLARED and W_PHYSICAL_EXPORT_LOCK_STATUS == "P_w_physical_export_lock"
    return {"passed": p, "status": "PASS" if p else "FAIL", "mode": PHYSICAL_EXPORT_LOCK_MODE}


def check_T_w_physical_export_lock_depends_on_uncertainty_harness():
    d = _check_v105()
    p = _passed(d) and W_UNCERTAINTY_PROPAGATION_STATUS == "P_w_uncertainty_propagation_harness"
    return {"passed": p, "status": "PASS" if p else "FAIL", "upstream": d.get("status")}


def check_T_w_physical_export_lock_schema_declared():
    r = export_lock_report()
    p = set(EXPORT_REPORT_FIELDS).issubset(r.keys()) and len(RELEASE_REQUIRED_FLAGS) == 7
    return {"passed": p, "status": "PASS" if p else "FAIL", "fields": EXPORT_REPORT_FIELDS}


def check_T_w_physical_export_lock_policy_blocks_smuggling():
    pol = policy()
    p = (not pol.allow_identity_trace_to_physical_export and not pol.allow_observed_w_input and not pol.allow_apf_anchor_as_component_input and not pol.allow_partial_release)
    return {"passed": p, "status": "PASS" if p else "FAIL", "policy": asdict(pol)}


def check_T_w_physical_export_lock_default_locked():
    r = export_lock_report()
    p = not r["release_predicate_satisfied"] and not r["physical_W_export_enabled"] and "MISSING_REAL_COMPONENT_ROWS_ADMITTED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_physical_export_lock_requires_real_rows():
    f = dry_positive_release_flags(); f["real_component_rows_admitted"] = False
    r = export_lock_report(f)
    p = not r["release_predicate_satisfied"] and "MISSING_REAL_COMPONENT_ROWS_ADMITTED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_physical_export_lock_requires_component_sum():
    f = dry_positive_release_flags(); f["component_sum_certified"] = False
    r = export_lock_report(f)
    p = not r["release_predicate_satisfied"] and "MISSING_COMPONENT_SUM_CERTIFIED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_physical_export_lock_requires_covariance():
    f = dry_positive_release_flags(); f["covariance_certified"] = False
    r = export_lock_report(f)
    p = not r["release_predicate_satisfied"] and "MISSING_COVARIANCE_CERTIFIED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_physical_export_lock_requires_uncertainty():
    f = dry_positive_release_flags(); f["uncertainty_propagation_certified"] = False
    r = export_lock_report(f)
    p = not r["release_predicate_satisfied"] and "MISSING_UNCERTAINTY_PROPAGATION_CERTIFIED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_physical_export_lock_requires_counterterm_convention():
    f = dry_positive_release_flags(); f["finite_counterterm_convention_certified"] = False
    r = export_lock_report(f)
    p = not r["release_predicate_satisfied"] and "MISSING_FINITE_COUNTERTERM_CONVENTION_CERTIFIED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_physical_export_lock_requires_target_scheme_contract():
    f = dry_positive_release_flags(); f["target_scheme_contract_certified"] = False
    r = export_lock_report(f)
    p = not r["release_predicate_satisfied"] and "MISSING_TARGET_SCHEME_CONTRACT_CERTIFIED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_physical_export_lock_requires_no_target_observable_consumption():
    f = dry_positive_release_flags(); f["no_target_observable_consumption_certified"] = False
    r = export_lock_report(f)
    p = not r["release_predicate_satisfied"] and "MISSING_NO_TARGET_OBSERVABLE_CONSUMPTION_CERTIFIED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_physical_export_lock_dry_positive_predicate_true_but_no_export():
    r = export_lock_report(dry_positive_release_flags())
    p = r["release_predicate_satisfied"] and not r["physical_W_export_enabled"] and not r["exports_physical_M_W"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "dry_report": r}


def check_T_w_physical_export_lock_rejects_observed_w_input():
    r = export_lock_report(dry_positive_release_flags(), ("observed_M_W",))
    p = not r["release_predicate_satisfied"] and "FORBIDDEN_EXPORT_INPUT_CONSUMED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_physical_export_lock_rejects_world_average_input():
    r = export_lock_report(dry_positive_release_flags(), ("M_W_world_average",))
    p = not r["release_predicate_satisfied"] and "M_W_world_average" in r["forbidden_inputs_hit"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_physical_export_lock_rejects_apf_anchor_as_input():
    r = export_lock_report(dry_positive_release_flags(), ("APF_ANCHOR_DELTA_R_TARGET_AS_INPUT",))
    p = not r["release_predicate_satisfied"] and "APF_ANCHOR_DELTA_R_TARGET_AS_INPUT" in r["forbidden_inputs_hit"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_physical_export_lock_rejects_residual_fit_input():
    r = export_lock_report(dry_positive_release_flags(), ("component_sum_residual_to_apf_target_as_input",))
    p = not r["release_predicate_satisfied"] and "component_sum_residual_to_apf_target_as_input" in r["forbidden_inputs_hit"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_physical_export_lock_rejects_identity_transport():
    r = export_lock_report(dry_positive_release_flags(), ("identity_W_TRACE_to_on_shell_M_W",))
    p = not r["release_predicate_satisfied"] and "identity_W_TRACE_to_on_shell_M_W" in r["forbidden_inputs_hit"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_physical_export_lock_rejects_export_request_when_locked():
    r = export_lock_report(physical_export_requested=True)
    p = not r["physical_W_export_enabled"] and "PHYSICAL_W_EXPORT_REQUEST_BLOCKED_BY_RELEASE_PREDICATE" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_physical_export_lock_preserves_W_TRACE_as_anchor_not_export():
    m = manifest()
    p = m["W_TRACE_MASS_GeV"] == str(W_TRACE_MASS_GEV) and not m["exports_physical_M_W"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "W_TRACE_MASS_GeV": m["W_TRACE_MASS_GeV"]}


def check_T_w_physical_export_lock_preserves_apf_delta_r_as_comparison_only():
    m = manifest()
    p = m["apf_anchor_delta_r_target"].startswith("3.640752661") and not policy().allow_apf_anchor_as_component_input
    return {"passed": p, "status": "PASS" if p else "FAIL", "apf_anchor_delta_r_target": m["apf_anchor_delta_r_target"]}


def check_T_w_physical_export_lock_uncertainty_absence_blocks_release():
    u = uncertainty_manifest()
    p = not u["uncertainty_propagation_certified"] and not release_predicate()
    return {"passed": p, "status": "PASS" if p else "FAIL", "uncertainty_manifest_open": not u["uncertainty_propagation_certified"]}


def check_T_w_physical_export_lock_completion_gate_still_locked():
    d = _check_completion()
    m = manifest()
    p = _passed(d) and not m["physical_W_export_enabled"] and not m["exports_physical_scheme_masses"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "completion_gate": d.get("status"), "manifest": m}


def check_T_w_physical_export_lock_no_physical_mass_exports():
    r = export_lock_report(dry_positive_release_flags())
    p = not r["exports_physical_M_W"] and not r["exports_physical_scheme_masses"] and not EXPORTS_PHYSICAL_SCHEME_MASSES
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_physical_export_lock_bank_closure():
    deps = [
        check_T_w_physical_export_lock_status_declared(),
        check_T_w_physical_export_lock_depends_on_uncertainty_harness(),
        check_T_w_physical_export_lock_schema_declared(),
        check_T_w_physical_export_lock_default_locked(),
        check_T_w_physical_export_lock_completion_gate_still_locked(),
        check_T_w_physical_export_lock_no_physical_mass_exports(),
    ]
    p = all(_passed(d) for d in deps) and not PHYSICAL_W_EXPORT_ENABLED and not EXPORTS_PHYSICAL_M_W
    return {
        "passed": p,
        "status": "PASS" if p else "FAIL",
        "tier": 4,
        "epistemic": W_PHYSICAL_EXPORT_LOCK_STATUS,
        "dependencies": [str(d.get("status")) for d in deps],
        "manifest": manifest(),
        "closed_now": "physical W export release predicate, required release flags, and anti-smuggling export lock",
        "not_closed": "real component rows, certified component sum, certified covariance/uncertainty, counterterm convention, numeric physical W/on-shell export",
    }


_CHECKS: Dict[str, Any] = {
    "T_w_physical_export_lock_status_declared": check_T_w_physical_export_lock_status_declared,
    "T_w_physical_export_lock_depends_on_uncertainty_harness": check_T_w_physical_export_lock_depends_on_uncertainty_harness,
    "T_w_physical_export_lock_schema_declared": check_T_w_physical_export_lock_schema_declared,
    "T_w_physical_export_lock_policy_blocks_smuggling": check_T_w_physical_export_lock_policy_blocks_smuggling,
    "T_w_physical_export_lock_default_locked": check_T_w_physical_export_lock_default_locked,
    "T_w_physical_export_lock_requires_real_rows": check_T_w_physical_export_lock_requires_real_rows,
    "T_w_physical_export_lock_requires_component_sum": check_T_w_physical_export_lock_requires_component_sum,
    "T_w_physical_export_lock_requires_covariance": check_T_w_physical_export_lock_requires_covariance,
    "T_w_physical_export_lock_requires_uncertainty": check_T_w_physical_export_lock_requires_uncertainty,
    "T_w_physical_export_lock_requires_counterterm_convention": check_T_w_physical_export_lock_requires_counterterm_convention,
    "T_w_physical_export_lock_requires_target_scheme_contract": check_T_w_physical_export_lock_requires_target_scheme_contract,
    "T_w_physical_export_lock_requires_no_target_observable_consumption": check_T_w_physical_export_lock_requires_no_target_observable_consumption,
    "T_w_physical_export_lock_dry_positive_predicate_true_but_no_export": check_T_w_physical_export_lock_dry_positive_predicate_true_but_no_export,
    "T_w_physical_export_lock_rejects_observed_w_input": check_T_w_physical_export_lock_rejects_observed_w_input,
    "T_w_physical_export_lock_rejects_world_average_input": check_T_w_physical_export_lock_rejects_world_average_input,
    "T_w_physical_export_lock_rejects_apf_anchor_as_input": check_T_w_physical_export_lock_rejects_apf_anchor_as_input,
    "T_w_physical_export_lock_rejects_residual_fit_input": check_T_w_physical_export_lock_rejects_residual_fit_input,
    "T_w_physical_export_lock_rejects_identity_transport": check_T_w_physical_export_lock_rejects_identity_transport,
    "T_w_physical_export_lock_rejects_export_request_when_locked": check_T_w_physical_export_lock_rejects_export_request_when_locked,
    "T_w_physical_export_lock_preserves_W_TRACE_as_anchor_not_export": check_T_w_physical_export_lock_preserves_W_TRACE_as_anchor_not_export,
    "T_w_physical_export_lock_preserves_apf_delta_r_as_comparison_only": check_T_w_physical_export_lock_preserves_apf_delta_r_as_comparison_only,
    "T_w_physical_export_lock_uncertainty_absence_blocks_release": check_T_w_physical_export_lock_uncertainty_absence_blocks_release,
    "T_w_physical_export_lock_completion_gate_still_locked": check_T_w_physical_export_lock_completion_gate_still_locked,
    "T_w_physical_export_lock_no_physical_mass_exports": check_T_w_physical_export_lock_no_physical_mass_exports,
    "T_w_physical_export_lock_bank_closure": check_T_w_physical_export_lock_bank_closure,
}


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
        "status": "W_TRACE_PHYSICAL_EXPORT_LOCK_BANK_PASS" if ok else "W_TRACE_PHYSICAL_EXPORT_LOCK_BANK_FAIL",
        "checks": rows,
        "manifest": manifest(),
    }


if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
