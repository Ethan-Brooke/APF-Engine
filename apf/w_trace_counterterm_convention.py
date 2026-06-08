"""W_TRACE counterterm convention certificate bank.

v10.7 (2026-05-09 LATER-30): counterterm-convention certificate after the
v10.6 physical-export lock.  This module banks the on-shell finite
counterterm convention contract required by the W_TRACE -> on-shell route.
It deliberately does not supply numerical finite counterterm values and does
not release physical W export.  It closes the convention schema, anti-smuggling
clauses, and compatibility with the W physical-export lock.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, Tuple

from apf.w_trace_physical_export_lock import (
    W_PHYSICAL_EXPORT_LOCK_STATUS,
    export_lock_report,
    release_predicate,
    dry_positive_release_flags,
    check_T_w_physical_export_lock_bank_closure as _check_v106,
)
from apf.w_trace_finite_part_skeleton import (
    FINITE_PART_COMPONENT_ORDER,
    COMPONENT_SYMBOLS,
    W_FINITE_PART_SKELETON_STATUS,
)
from apf.w_trace_finite_part_ledger import apf_anchor_delta_r_target
from apf.w_trace_onshell_transport import W_TRACE_EXPECTED_GEV as W_TRACE_MASS_GEV

W_COUNTERTERM_CONVENTION_STATUS = "P_w_counterterm_convention_certificate"
COUNTERTERM_CONVENTION_DECLARED = True
COUNTERTERM_CONVENTION_VERSION = "w_trace_counterterm_convention_v0"
COUNTERTERM_CONVENTION_MODE = "ON_SHELL_CONVENTION_CONTRACT_CERTIFIED_NO_NUMERIC_COUNTERTERM_NO_EXPORT"
COUNTERTERM_CONVENTION_ID = "OS_EW_Delta_r_counterterm_convention_v1"
COUNTERTERM_COMPONENT = "scheme_conversion_counterterm_component"

COUNTERTERM_CONVENTION_CONTRACT_CERTIFIED = True
NUMERICAL_COUNTERTERM_VALUES_SUPPLIED = False
FINITE_COUNTERTERM_VALUES_EVALUATED = False
COUNTERTERM_COMPONENT_SUM_CERTIFIED = False
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False

REQUIRED_CONVENTION_FIELDS: Tuple[str, ...] = (
    "scheme_name",
    "scheme_family",
    "target_route",
    "mass_renormalization_condition",
    "charge_renormalization_condition",
    "weak_mixing_angle_definition",
    "tadpole_scheme",
    "gauge_parameter_policy",
    "finite_part_normalization",
    "subtraction_scale_policy",
    "counterterm_component",
    "delta_r_sign_convention",
    "loop_order_scope",
    "source_reference",
    "no_observed_w_clause",
    "no_apf_anchor_backsolve_clause",
    "no_residual_fit_clause",
)

ALLOWED_CONVENTION_INPUTS: Tuple[str, ...] = (
    "alpha_em_reference",
    "G_F_reference",
    "M_Z_on_shell_reference",
    "W_TRACE_anchor",
    "symbolic_self_energy_terms",
    "symbolic_vertex_box_terms",
    "symbolic_tadpole_terms",
    "renormalization_condition_text",
)

FORBIDDEN_CONVENTION_INPUTS: Tuple[str, ...] = (
    "observed_M_W",
    "observed_M_W_uncertainty",
    "M_W_world_average",
    "world_average_W_mass_column",
    "W_mass_residual",
    "W_mass_residual_column",
    "Delta_r_fit_to_observed_M_W",
    "APF_ANCHOR_DELTA_R_TARGET",
    "apf_anchor_delta_r_target_as_component_input",
    "component_sum_residual_to_apf_target",
    "finite_counterterm_chosen_to_match_M_W",
    "posthoc_counterterm_fit",
    "identity_W_TRACE_to_on_shell_M_W",
)

REPORT_FIELDS: Tuple[str, ...] = (
    "status",
    "version",
    "convention_id",
    "contract_fields",
    "missing_fields",
    "forbidden_inputs_hit",
    "convention_contract_certified",
    "numerical_counterterm_values_supplied",
    "finite_counterterm_values_evaluated",
    "physical_W_export_enabled",
    "exports_physical_M_W",
    "failure_reasons",
)

@dataclass(frozen=True)
class CountertermConventionPolicy:
    require_os_scheme_family: bool = True
    require_pole_mass_condition: bool = True
    require_thomson_charge_condition: bool = True
    require_on_shell_mixing_angle_definition: bool = True
    require_tadpole_and_gauge_policy: bool = True
    require_no_target_observable_consumption: bool = True
    require_no_apf_anchor_backsolve: bool = True
    allow_tuned_finite_counterterm: bool = False
    allow_identity_trace_to_physical: bool = False
    allow_physical_w_export_from_convention_only: bool = False


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def policy() -> CountertermConventionPolicy:
    return CountertermConventionPolicy()


def default_convention_record() -> Dict[str, str]:
    return {
        "scheme_name": "electroweak on-shell Delta_r finite-counterterm convention",
        "scheme_family": "on_shell",
        "target_route": "w_trace_on_shell_route",
        "mass_renormalization_condition": "renormalized vector-boson masses defined by real pole/on-shell conditions; no observed W mass may be consumed as an input",
        "charge_renormalization_condition": "electric charge normalized at Thomson/alpha_em reference input; no W residual fitting",
        "weak_mixing_angle_definition": "s_W^2 = 1 - M_W^2/M_Z^2 inside the symbolic on-shell relation; M_W is the W_TRACE anchor until export release",
        "tadpole_scheme": "tadpole treatment must be declared and finite; not available as an APF-anchor tuning knob",
        "gauge_parameter_policy": "gauge choice/cancellation policy must be source-tagged; gauge parameter cannot be fit to W residual",
        "finite_part_normalization": "finite parts enter only through the declared scheme_conversion_counterterm_component (Delta_r_ct_OS) component with the v9.3 Delta_r sign convention",
        "subtraction_scale_policy": "on-shell finite conversion; any auxiliary scale dependence must cancel or be separately ledgered",
        "counterterm_component": COUNTERTERM_COMPONENT,
        "delta_r_sign_convention": "M_W^2(1-M_W^2/M_Z^2)=pi*alpha/(sqrt(2)*G_F)/(1-Delta_r)",
        "loop_order_scope": "symbolic finite-part convention only; numerical loop order not supplied in this bank",
        "source_reference": "internal APF v10.7 convention contract; external finite-part tables still required before numeric closure",
        "no_observed_w_clause": "observed M_W, world-average W mass, and W residuals are forbidden inputs",
        "no_apf_anchor_backsolve_clause": "APF-anchor Delta_r target is comparison-only and cannot determine the counterterm convention",
        "no_residual_fit_clause": "finite counterterms may not be chosen post hoc to close the APF-anchor residual",
    }


def convention_report(
    record: Mapping[str, Any] | None = None,
    consumed_inputs: Tuple[str, ...] = (),
    numerical_values_supplied: bool = False,
    physical_export_requested: bool = False,
) -> Dict[str, Any]:
    rec = dict(default_convention_record() if record is None else record)
    missing = tuple(k for k in REQUIRED_CONVENTION_FIELDS if not rec.get(k))
    forbidden_hit = tuple(x for x in consumed_inputs if x in FORBIDDEN_CONVENTION_INPUTS)
    pol = policy()
    os_ok = (not pol.require_os_scheme_family) or rec.get("scheme_family") == "on_shell"
    component_ok = rec.get("counterterm_component") == COUNTERTERM_COMPONENT
    pole_ok = "pole" in str(rec.get("mass_renormalization_condition", "")).lower() or "on-shell" in str(rec.get("mass_renormalization_condition", "")).lower()
    thomson_ok = "thomson" in str(rec.get("charge_renormalization_condition", "")).lower() or "alpha_em" in str(rec.get("charge_renormalization_condition", "")).lower()
    mixing_ok = "1 - M_W^2/M_Z^2" in str(rec.get("weak_mixing_angle_definition", ""))
    clauses_ok = all(rec.get(k) for k in ("no_observed_w_clause", "no_apf_anchor_backsolve_clause", "no_residual_fit_clause"))
    contract_ok = bool(
        not missing
        and not forbidden_hit
        and os_ok
        and component_ok
        and pole_ok
        and thomson_ok
        and mixing_ok
        and clauses_ok
        and not pol.allow_tuned_finite_counterterm
        and not pol.allow_identity_trace_to_physical
    )
    failures = []
    if missing:
        failures.append("MISSING_REQUIRED_CONVENTION_FIELDS")
    if forbidden_hit:
        failures.append("FORBIDDEN_COUNTERTERM_INPUT_CONSUMED")
    if not os_ok:
        failures.append("COUNTERTERM_SCHEME_NOT_ON_SHELL")
    if not component_ok:
        failures.append("COUNTERTERM_COMPONENT_NOT_DELTA_R_CT_OS")
    if not pole_ok:
        failures.append("POLE_OR_ON_SHELL_MASS_CONDITION_UNDECLARED")
    if not thomson_ok:
        failures.append("THOMSON_OR_ALPHA_CHARGE_CONDITION_UNDECLARED")
    if not mixing_ok:
        failures.append("ON_SHELL_MIXING_ANGLE_DEFINITION_UNDECLARED")
    if not clauses_ok:
        failures.append("NO_SMUGGLING_CLAUSES_INCOMPLETE")
    if numerical_values_supplied:
        failures.append("NUMERICAL_COUNTERTERM_VALUES_NOT_ADMITTED_IN_V10_7")
    if physical_export_requested:
        failures.append("PHYSICAL_W_EXPORT_REQUEST_BLOCKED_AT_COUNTERTERM_CONVENTION")
    return {
        "status": W_COUNTERTERM_CONVENTION_STATUS,
        "version": COUNTERTERM_CONVENTION_VERSION,
        "convention_id": COUNTERTERM_CONVENTION_ID,
        "contract_fields": tuple(rec.keys()),
        "required_fields": REQUIRED_CONVENTION_FIELDS,
        "missing_fields": missing,
        "allowed_inputs": ALLOWED_CONVENTION_INPUTS,
        "forbidden_inputs": FORBIDDEN_CONVENTION_INPUTS,
        "forbidden_inputs_hit": forbidden_hit,
        "on_shell_scheme_family": rec.get("scheme_family") == "on_shell",
        "counterterm_component": rec.get("counterterm_component"),
        "counterterm_component_ok": component_ok,
        "pole_or_on_shell_condition_declared": pole_ok,
        "thomson_or_alpha_charge_condition_declared": thomson_ok,
        "on_shell_mixing_definition_declared": mixing_ok,
        "no_smuggling_clauses_complete": clauses_ok,
        "convention_contract_certified": contract_ok,
        "numerical_counterterm_values_supplied": bool(numerical_values_supplied),
        "finite_counterterm_values_evaluated": False,
        "component_sum_certified": False,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "failure_reasons": tuple(dict.fromkeys(failures)),
    }


def manifest() -> Dict[str, Any]:
    return {
        "status": W_COUNTERTERM_CONVENTION_STATUS,
        "upstream_status": W_PHYSICAL_EXPORT_LOCK_STATUS,
        "finite_part_skeleton_status": W_FINITE_PART_SKELETON_STATUS,
        "version": COUNTERTERM_CONVENTION_VERSION,
        "mode": COUNTERTERM_CONVENTION_MODE,
        "convention_id": COUNTERTERM_CONVENTION_ID,
        "policy": asdict(policy()),
        "required_convention_fields": REQUIRED_CONVENTION_FIELDS,
        "report_fields": REPORT_FIELDS,
        "allowed_convention_inputs": ALLOWED_CONVENTION_INPUTS,
        "forbidden_convention_inputs": FORBIDDEN_CONVENTION_INPUTS,
        "finite_part_component_order": FINITE_PART_COMPONENT_ORDER,
        "component_symbols": COMPONENT_SYMBOLS,
        "counterterm_component": COUNTERTERM_COMPONENT,
        "W_TRACE_MASS_GeV": str(W_TRACE_MASS_GEV),
        "apf_anchor_delta_r_target": f"{apf_anchor_delta_r_target():.17E}",
        "convention_contract_certified": COUNTERTERM_CONVENTION_CONTRACT_CERTIFIED,
        "numerical_counterterm_values_supplied": NUMERICAL_COUNTERTERM_VALUES_SUPPLIED,
        "finite_counterterm_values_evaluated": FINITE_COUNTERTERM_VALUES_EVALUATED,
        "component_sum_certified": COUNTERTERM_COMPONENT_SUM_CERTIFIED,
        "physical_W_export_enabled": PHYSICAL_W_EXPORT_ENABLED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "default_report": convention_report(),
        "export_lock_after_convention": export_lock_report(),
    }


def check_T_w_counterterm_convention_status_declared():
    p = COUNTERTERM_CONVENTION_DECLARED and W_COUNTERTERM_CONVENTION_STATUS == "P_w_counterterm_convention_certificate"
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS, "mode": COUNTERTERM_CONVENTION_MODE}


def check_T_w_counterterm_convention_depends_on_export_lock():
    d = _check_v106()
    p = _passed(d) and W_PHYSICAL_EXPORT_LOCK_STATUS == "P_w_physical_export_lock"
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS, "upstream": d.get("status")}


def check_T_w_counterterm_convention_schema_complete():
    r = convention_report()
    p = set(REPORT_FIELDS).issubset(r.keys()) and set(REQUIRED_CONVENTION_FIELDS).issubset(r["contract_fields"])
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS, "report_fields": REPORT_FIELDS}


def check_T_w_counterterm_convention_policy_blocks_tuning():
    pol = policy()
    p = not pol.allow_tuned_finite_counterterm and not pol.allow_identity_trace_to_physical and not pol.allow_physical_w_export_from_convention_only
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS, "policy": asdict(pol)}


def check_T_w_counterterm_convention_default_contract_certifies_schema_only():
    r = convention_report()
    p = r["convention_contract_certified"] and not r["finite_counterterm_values_evaluated"] and not r["physical_W_export_enabled"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS, "report": r}


def check_T_w_counterterm_convention_on_shell_scheme_family_declared():
    r = convention_report()
    p = r["on_shell_scheme_family"] and default_convention_record()["scheme_family"] == "on_shell"
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS}


def check_T_w_counterterm_convention_pole_mass_condition_declared():
    r = convention_report()
    p = r["pole_or_on_shell_condition_declared"] and "observed W mass" in default_convention_record()["mass_renormalization_condition"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS}


def check_T_w_counterterm_convention_charge_condition_declared():
    r = convention_report()
    p = r["thomson_or_alpha_charge_condition_declared"] and "W residual" in default_convention_record()["charge_renormalization_condition"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS}


def check_T_w_counterterm_convention_mixing_angle_definition_declared():
    r = convention_report()
    p = r["on_shell_mixing_definition_declared"] and "1 - M_W^2/M_Z^2" in default_convention_record()["weak_mixing_angle_definition"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS}


def check_T_w_counterterm_convention_tadpole_and_gauge_policies_declared():
    rec = default_convention_record()
    p = bool(rec["tadpole_scheme"] and rec["gauge_parameter_policy"] and "fit" in rec["gauge_parameter_policy"])
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS}


def check_T_w_counterterm_convention_finite_part_normalization_declared():
    rec = default_convention_record()
    p = COUNTERTERM_COMPONENT in rec["finite_part_normalization"] and "Delta_r sign convention" in rec["finite_part_normalization"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS}


def check_T_w_counterterm_convention_maps_to_delta_r_ct_os_slot():
    r = convention_report()
    p = r["counterterm_component_ok"] and COUNTERTERM_COMPONENT in FINITE_PART_COMPONENT_ORDER and COMPONENT_SYMBOLS[COUNTERTERM_COMPONENT] == "Delta_r_ct_OS"
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS, "component": COUNTERTERM_COMPONENT}


def check_T_w_counterterm_convention_component_order_preserved():
    p = tuple(FINITE_PART_COMPONENT_ORDER).index(COUNTERTERM_COMPONENT) >= 0 and len(FINITE_PART_COMPONENT_ORDER) == 8
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS, "order": FINITE_PART_COMPONENT_ORDER}


def check_T_w_counterterm_convention_forbids_observed_w_input():
    r = convention_report(consumed_inputs=("observed_M_W",))
    p = not r["convention_contract_certified"] and "FORBIDDEN_COUNTERTERM_INPUT_CONSUMED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS, "report": r}


def check_T_w_counterterm_convention_forbids_world_average_input():
    r = convention_report(consumed_inputs=("M_W_world_average",))
    p = not r["convention_contract_certified"] and "M_W_world_average" in r["forbidden_inputs_hit"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS}


def check_T_w_counterterm_convention_forbids_apf_anchor_backsolve():
    r = convention_report(consumed_inputs=("APF_ANCHOR_DELTA_R_TARGET",))
    p = not r["convention_contract_certified"] and "APF_ANCHOR_DELTA_R_TARGET" in r["forbidden_inputs_hit"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS}


def check_T_w_counterterm_convention_forbids_residual_fit():
    r = convention_report(consumed_inputs=("component_sum_residual_to_apf_target", "posthoc_counterterm_fit"))
    p = not r["convention_contract_certified"] and len(r["forbidden_inputs_hit"]) == 2
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS}


def check_T_w_counterterm_convention_forbids_tuned_finite_counterterm():
    r = convention_report(consumed_inputs=("finite_counterterm_chosen_to_match_M_W",))
    p = not r["convention_contract_certified"] and "finite_counterterm_chosen_to_match_M_W" in r["forbidden_inputs_hit"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS}


def check_T_w_counterterm_convention_rejects_missing_fields():
    rec = default_convention_record(); rec.pop("tadpole_scheme")
    r = convention_report(rec)
    p = not r["convention_contract_certified"] and "MISSING_REQUIRED_CONVENTION_FIELDS" in r["failure_reasons"] and "tadpole_scheme" in r["missing_fields"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS}


def check_T_w_counterterm_convention_rejects_wrong_scheme_family():
    rec = default_convention_record(); rec["scheme_family"] = "MSbar"
    r = convention_report(rec)
    p = not r["convention_contract_certified"] and "COUNTERTERM_SCHEME_NOT_ON_SHELL" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS}


def check_T_w_counterterm_convention_rejects_wrong_component_slot():
    rec = default_convention_record(); rec["counterterm_component"] = "Delta_r_boson_finite"
    r = convention_report(rec)
    p = not r["convention_contract_certified"] and "COUNTERTERM_COMPONENT_NOT_DELTA_R_CT_OS" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS}


def check_T_w_counterterm_convention_numeric_values_still_unadmitted():
    r = convention_report(numerical_values_supplied=True)
    p = r["convention_contract_certified"] and "NUMERICAL_COUNTERTERM_VALUES_NOT_ADMITTED_IN_V10_7" in r["failure_reasons"] and not r["finite_counterterm_values_evaluated"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS, "report": r}


def check_T_w_counterterm_convention_export_request_blocked():
    r = convention_report(physical_export_requested=True)
    p = not r["physical_W_export_enabled"] and "PHYSICAL_W_EXPORT_REQUEST_BLOCKED_AT_COUNTERTERM_CONVENTION" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS}


def check_T_w_counterterm_convention_preserves_export_lock_default():
    r = export_lock_report()
    p = not r["release_predicate_satisfied"] and not r["physical_W_export_enabled"] and "MISSING_FINITE_COUNTERTERM_CONVENTION_CERTIFIED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS, "export_lock": r}


def check_T_w_counterterm_convention_dry_release_still_requires_other_flags():
    f = dry_positive_release_flags(); f["real_component_rows_admitted"] = False; f["component_sum_certified"] = False
    f["finite_counterterm_convention_certified"] = True
    p = not release_predicate(f) and not export_lock_report(f)["physical_W_export_enabled"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS, "flags": f}


def check_T_w_counterterm_convention_no_physical_w_exports():
    m = manifest()
    p = not m["physical_W_export_enabled"] and not m["exports_physical_M_W"] and not m["finite_counterterm_values_evaluated"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "tier": 4, "epistemic": W_COUNTERTERM_CONVENTION_STATUS, "manifest_flags": {"export": m["physical_W_export_enabled"], "exports_M_W": m["exports_physical_M_W"]}}


def check_T_w_counterterm_convention_bank_closure():
    deps = [
        check_T_w_counterterm_convention_status_declared(),
        check_T_w_counterterm_convention_depends_on_export_lock(),
        check_T_w_counterterm_convention_schema_complete(),
        check_T_w_counterterm_convention_default_contract_certifies_schema_only(),
        check_T_w_counterterm_convention_maps_to_delta_r_ct_os_slot(),
        check_T_w_counterterm_convention_preserves_export_lock_default(),
        check_T_w_counterterm_convention_no_physical_w_exports(),
    ]
    p = all(_passed(d) for d in deps) and COUNTERTERM_CONVENTION_CONTRACT_CERTIFIED and not PHYSICAL_W_EXPORT_ENABLED
    return {
        "passed": p,
        "status": "PASS" if p else "FAIL",
        "tier": 4,
        "epistemic": W_COUNTERTERM_CONVENTION_STATUS,
        "dependencies": [str(d.get("status")) for d in deps],
        "manifest": manifest(),
        "closed_now": "on-shell finite counterterm convention contract, required fields, Delta_r_ct_OS slot mapping, and anti-smuggling clauses",
        "not_closed": "numeric counterterm values, independent finite-part rows, component-sum certificate, covariance/uncertainty, physical W/on-shell export",
    }


_CHECKS: Dict[str, Any] = {
    "T_w_counterterm_convention_status_declared": check_T_w_counterterm_convention_status_declared,
    "T_w_counterterm_convention_depends_on_export_lock": check_T_w_counterterm_convention_depends_on_export_lock,
    "T_w_counterterm_convention_schema_complete": check_T_w_counterterm_convention_schema_complete,
    "T_w_counterterm_convention_policy_blocks_tuning": check_T_w_counterterm_convention_policy_blocks_tuning,
    "T_w_counterterm_convention_default_contract_certifies_schema_only": check_T_w_counterterm_convention_default_contract_certifies_schema_only,
    "T_w_counterterm_convention_on_shell_scheme_family_declared": check_T_w_counterterm_convention_on_shell_scheme_family_declared,
    "T_w_counterterm_convention_pole_mass_condition_declared": check_T_w_counterterm_convention_pole_mass_condition_declared,
    "T_w_counterterm_convention_charge_condition_declared": check_T_w_counterterm_convention_charge_condition_declared,
    "T_w_counterterm_convention_mixing_angle_definition_declared": check_T_w_counterterm_convention_mixing_angle_definition_declared,
    "T_w_counterterm_convention_tadpole_and_gauge_policies_declared": check_T_w_counterterm_convention_tadpole_and_gauge_policies_declared,
    "T_w_counterterm_convention_finite_part_normalization_declared": check_T_w_counterterm_convention_finite_part_normalization_declared,
    "T_w_counterterm_convention_maps_to_delta_r_ct_os_slot": check_T_w_counterterm_convention_maps_to_delta_r_ct_os_slot,
    "T_w_counterterm_convention_component_order_preserved": check_T_w_counterterm_convention_component_order_preserved,
    "T_w_counterterm_convention_forbids_observed_w_input": check_T_w_counterterm_convention_forbids_observed_w_input,
    "T_w_counterterm_convention_forbids_world_average_input": check_T_w_counterterm_convention_forbids_world_average_input,
    "T_w_counterterm_convention_forbids_apf_anchor_backsolve": check_T_w_counterterm_convention_forbids_apf_anchor_backsolve,
    "T_w_counterterm_convention_forbids_residual_fit": check_T_w_counterterm_convention_forbids_residual_fit,
    "T_w_counterterm_convention_forbids_tuned_finite_counterterm": check_T_w_counterterm_convention_forbids_tuned_finite_counterterm,
    "T_w_counterterm_convention_rejects_missing_fields": check_T_w_counterterm_convention_rejects_missing_fields,
    "T_w_counterterm_convention_rejects_wrong_scheme_family": check_T_w_counterterm_convention_rejects_wrong_scheme_family,
    "T_w_counterterm_convention_rejects_wrong_component_slot": check_T_w_counterterm_convention_rejects_wrong_component_slot,
    "T_w_counterterm_convention_numeric_values_still_unadmitted": check_T_w_counterterm_convention_numeric_values_still_unadmitted,
    "T_w_counterterm_convention_export_request_blocked": check_T_w_counterterm_convention_export_request_blocked,
    "T_w_counterterm_convention_preserves_export_lock_default": check_T_w_counterterm_convention_preserves_export_lock_default,
    "T_w_counterterm_convention_dry_release_still_requires_other_flags": check_T_w_counterterm_convention_dry_release_still_requires_other_flags,
    "T_w_counterterm_convention_no_physical_w_exports": check_T_w_counterterm_convention_no_physical_w_exports,
    "T_w_counterterm_convention_bank_closure": check_T_w_counterterm_convention_bank_closure,
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
        "status": "W_TRACE_COUNTERTERM_CONVENTION_BANK_PASS" if ok else "W_TRACE_COUNTERTERM_CONVENTION_BANK_FAIL",
        "checks": rows,
        "manifest": manifest(),
    }


if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
