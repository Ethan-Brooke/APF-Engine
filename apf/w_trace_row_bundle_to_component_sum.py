"""W_TRACE row-bundle-to-component-sum bridge bank.

v11.0 (2026-05-09 LATER-37): bridge layer after the v10.9 real
row-bundle admission report and the v10.4 component-sum certificate harness.
This module wires admitted row bundles into the Delta_r component-sum
certificate pathway.  It closes the structural bridge only: the shipped bank
state remains empty, no real rows are supplied, no numerical component-sum
certificate is claimed, and physical W export remains locked.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal
from typing import Any, Dict, Mapping, Sequence, Tuple

from apf.w_trace_finite_part_skeleton import FINITE_PART_COMPONENT_ORDER, COMPONENT_SYMBOLS
from apf.w_trace_finite_part_ledger import apf_anchor_delta_r_target
from apf.w_trace_real_row_bundle_admission import (
    W_REAL_ROW_BUNDLE_STATUS,
    BUNDLE_ADMISSION_VERSION,
    admit_bundle,
    default_bundle_metadata,
    empty_bundle_report,
    real_candidate_rows_from_shape_template,
    check_T_w_real_row_bundle_bank_closure as _check_v109,
)
from apf.w_trace_component_sum_certificate import (
    W_COMPONENT_SUM_CERTIFICATE_STATUS,
    COMPONENT_SUM_CERTIFICATE_VERSION,
    DEFAULT_ABSOLUTE_TOLERANCE,
    FORBIDDEN_SUM_CERTIFICATE_INPUTS,
    component_sum_certificate_report,
    check_T_w_component_sum_certificate_bank_closure as _check_v104,
)
from apf.w_trace_physical_export_lock import export_lock_report, release_predicate

W_ROW_BUNDLE_TO_COMPONENT_SUM_STATUS = "P_w_row_bundle_to_component_sum_bridge"
ROW_BUNDLE_TO_COMPONENT_SUM_VERSION = "w_trace_row_bundle_to_component_sum_bridge_v0"
ROW_BUNDLE_TO_COMPONENT_SUM_MODE = "BRIDGE_ONLY_EMPTY_DEFAULT_NO_REAL_ROWS_NO_EXPORT"

REAL_ROW_BUNDLE_SUPPLIED = False
REAL_ROW_BUNDLE_ADMITTED = False
ROW_BUNDLE_COMPONENT_SUM_BRIDGED = False
NUMERICAL_COMPONENT_SUM_CERTIFIED = False
COVARIANCE_CERTIFIED = False
UNCERTAINTY_PROPAGATION_CERTIFIED = False
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False

BRIDGE_REQUIRED_FIELDS: Tuple[str, ...] = (
    "status",
    "version",
    "mode",
    "bundle_admission_state",
    "bundle_admitted",
    "summand_rows_constructed",
    "sum_certificate_invoked",
    "component_sum_certified",
    "physical_W_export_enabled",
    "failure_reasons",
)

FORBIDDEN_BRIDGE_INPUTS: Tuple[str, ...] = tuple(dict.fromkeys(FORBIDDEN_SUM_CERTIFICATE_INPUTS + (
    "observed_M_W_bundle_bridge",
    "world_average_W_mass_bundle_bridge",
    "APF_ANCHOR_DELTA_R_TARGET_AS_ROW_VALUE",
    "component_sum_residual_to_apf_target",
    "posthoc_bridge_residual_fit",
    "physical_W_export_request",
)))

@dataclass(frozen=True)
class BridgePolicy:
    require_admitted_bundle_before_sum_certificate: bool = True
    require_exact_component_order: bool = True
    require_symbol_translation: bool = True
    require_no_forbidden_bridge_inputs: bool = True
    allow_empty_bundle_to_certify_sum: bool = False
    allow_rejected_bundle_to_certify_sum: bool = False
    allow_bridge_to_edit_row_values: bool = False
    allow_apf_anchor_as_row_input: bool = False
    allow_observed_w_as_input: bool = False
    allow_physical_export_from_bridge: bool = False


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def policy() -> BridgePolicy:
    return BridgePolicy()


def row_to_summand(row: Mapping[str, Any]) -> Dict[str, Any]:
    """Translate one v10.8/v10.9 row into a v10.4 summand mapping."""
    cid = str(row.get("component_id"))
    return {
        "component_id": cid,
        "symbol": str(row.get("component_symbol", COMPONENT_SYMBOLS.get(cid, ""))),
        "numeric_value": str(row.get("value")),
        "uncertainty": str(row.get("uncertainty")),
        "target_observables_consumed": tuple(row.get("consumed_inputs", ())),
        "apf_target_consumed": bool(row.get("apf_target_consumed", False)),
        "source_class": row.get("source_class"),
        "source_pack_digest": row.get("source_pack_digest"),
        "row_checksum": row.get("row_checksum"),
    }


def rows_to_summands(rows: Sequence[Mapping[str, Any]]) -> Tuple[Dict[str, Any], ...]:
    return tuple(row_to_summand(r) for r in rows)


def dry_target_sum_bundle_rows() -> Tuple[Dict[str, Any], ...]:
    """Dry-path rows whose values sum to the APF anchor.

    These rows are not shipped as real data and are used only to prove the
    bridge mechanics.  They do not appear in the default bank state.
    """
    target = apf_anchor_delta_r_target()
    per = float(target / Decimal(len(FINITE_PART_COMPONENT_ORDER)))
    rows = []
    for r in real_candidate_rows_from_shape_template():
        x = dict(r)
        x["value"] = per
        x["uncertainty"] = 1.0e-18
        x["source_title"] = "dry-path bridge mechanics table; not shipped as physical payload"
        x["provenance_chain"] = tuple(x.get("provenance_chain", ())) + ("dry bridge mechanics only",)
        rows.append(x)
    return tuple(rows)


def bridge_report(
    rows: Sequence[Mapping[str, Any]] | None = None,
    *,
    metadata: Mapping[str, Any] | None = None,
    covariance_supplied: bool = False,
    uncertainty_supplied: bool = False,
    tolerance: Decimal = DEFAULT_ABSOLUTE_TOLERANCE,
    physical_export_requested: bool = False,
) -> Dict[str, Any]:
    md = default_bundle_metadata() if metadata is None else dict(metadata)
    bundle = admit_bundle(rows, metadata=md, physical_export_requested=physical_export_requested)
    supplied_rows = tuple(rows or ())
    failures = []
    bridge_forbidden = []
    for row in supplied_rows:
        for x in tuple(row.get("consumed_inputs", ())):
            if x in FORBIDDEN_BRIDGE_INPUTS:
                bridge_forbidden.append(x)
        if row.get("physical_export_request"):
            bridge_forbidden.append("physical_W_export_request")
    if physical_export_requested:
        bridge_forbidden.append("physical_W_export_request")
    if bridge_forbidden:
        failures.append("FORBIDDEN_BRIDGE_INPUT_CONSUMED")

    if not bundle["bundle_admitted"]:
        failures.append("NO_ADMITTED_BUNDLE_AVAILABLE_FOR_COMPONENT_SUM")
        summands: Tuple[Dict[str, Any], ...] = tuple()
        cert = component_sum_certificate_report(
            summands,
            rows_admitted=False,
            covariance_supplied=covariance_supplied,
            uncertainty_supplied=uncertainty_supplied,
            tolerance=tolerance,
            physical_export_requested=physical_export_requested,
        )
        invoked = False
    else:
        summands = rows_to_summands(supplied_rows)
        order_ok = tuple(s["component_id"] for s in summands) == FINITE_PART_COMPONENT_ORDER
        if not order_ok:
            failures.append("SUMMAND_COMPONENT_ORDER_MISMATCH")
        cert = component_sum_certificate_report(
            summands,
            rows_admitted=bool(order_ok and not bridge_forbidden),
            covariance_supplied=covariance_supplied,
            uncertainty_supplied=uncertainty_supplied,
            tolerance=tolerance,
            physical_export_requested=physical_export_requested,
        )
        invoked = True
        failures.extend(tuple(cert.get("failure_reasons", ())))

    if physical_export_requested:
        failures.append("PHYSICAL_EXPORT_REQUEST_BLOCKED_AT_ROW_BUNDLE_SUM_BRIDGE")

    certified = bool(cert.get("component_sum_certified") and bundle.get("bundle_admitted") and not bridge_forbidden)
    return {
        "status": W_ROW_BUNDLE_TO_COMPONENT_SUM_STATUS,
        "version": ROW_BUNDLE_TO_COMPONENT_SUM_VERSION,
        "mode": ROW_BUNDLE_TO_COMPONENT_SUM_MODE,
        "upstream_bundle_status": W_REAL_ROW_BUNDLE_STATUS,
        "upstream_bundle_version": BUNDLE_ADMISSION_VERSION,
        "upstream_sum_certificate_status": W_COMPONENT_SUM_CERTIFICATE_STATUS,
        "upstream_sum_certificate_version": COMPONENT_SUM_CERTIFICATE_VERSION,
        "bundle_admission_state": bundle.get("admission_state"),
        "bundle_supplied": bool(bundle.get("bundle_supplied")),
        "bundle_admitted": bool(bundle.get("bundle_admitted")),
        "row_count": int(bundle.get("row_count", 0)),
        "summand_rows_constructed": bool(bundle.get("bundle_admitted") and supplied_rows),
        "summand_row_count": len(summands),
        "sum_certificate_invoked": bool(invoked),
        "component_sum_certified": certified,
        "covariance_certified": bool(covariance_supplied and certified),
        "uncertainty_propagation_certified": bool(uncertainty_supplied and certified),
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "forbidden_bridge_inputs_hit": tuple(dict.fromkeys(bridge_forbidden)),
        "failure_reasons": tuple(dict.fromkeys(failures)),
        "bundle_report": bundle,
        "component_sum_report": cert,
    }


def manifest() -> Dict[str, Any]:
    return {
        "status": W_ROW_BUNDLE_TO_COMPONENT_SUM_STATUS,
        "version": ROW_BUNDLE_TO_COMPONENT_SUM_VERSION,
        "mode": ROW_BUNDLE_TO_COMPONENT_SUM_MODE,
        "policy": asdict(policy()),
        "required_fields": BRIDGE_REQUIRED_FIELDS,
        "forbidden_bridge_inputs": FORBIDDEN_BRIDGE_INPUTS,
        "component_order": FINITE_PART_COMPONENT_ORDER,
        "real_row_bundle_supplied": REAL_ROW_BUNDLE_SUPPLIED,
        "real_row_bundle_admitted": REAL_ROW_BUNDLE_ADMITTED,
        "row_bundle_component_sum_bridged": ROW_BUNDLE_COMPONENT_SUM_BRIDGED,
        "numerical_component_sum_certified": NUMERICAL_COMPONENT_SUM_CERTIFIED,
        "covariance_certified": COVARIANCE_CERTIFIED,
        "uncertainty_propagation_certified": UNCERTAINTY_PROPAGATION_CERTIFIED,
        "physical_W_export_enabled": PHYSICAL_W_EXPORT_ENABLED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "default_report": bridge_report(),
    }


def _res(name: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    return {"passed": bool(passed), "status": "PASS" if passed else "FAIL", "tier": 4, "epistemic": W_ROW_BUNDLE_TO_COMPONENT_SUM_STATUS, "check": name, **extra}


def check_T_w_row_bundle_sum_bridge_status_declared():
    m = manifest(); return _res("status_declared", m["status"] == W_ROW_BUNDLE_TO_COMPONENT_SUM_STATUS and not m["physical_W_export_enabled"], manifest=m)


def check_T_w_row_bundle_sum_bridge_depends_on_v109_bundle_gate():
    d = _check_v109(); return _res("depends_on_v109", _passed(d) and W_REAL_ROW_BUNDLE_STATUS == "P_w_real_row_bundle_admission")


def check_T_w_row_bundle_sum_bridge_depends_on_v104_sum_harness():
    d = _check_v104(); return _res("depends_on_v104", _passed(d) and W_COMPONENT_SUM_CERTIFICATE_STATUS == "P_w_component_sum_certificate_harness")


def check_T_w_row_bundle_sum_bridge_policy_blocks_export():
    p = policy(); return _res("policy_blocks_export", not p.allow_physical_export_from_bridge and not p.allow_empty_bundle_to_certify_sum and not p.allow_rejected_bundle_to_certify_sum, policy=asdict(p))


def check_T_w_row_bundle_sum_bridge_required_fields_declared():
    r = bridge_report(); return _res("required_fields", set(BRIDGE_REQUIRED_FIELDS).issubset(r.keys()), fields=BRIDGE_REQUIRED_FIELDS)


def check_T_w_row_bundle_sum_bridge_default_empty_no_invocation():
    r = bridge_report(); return _res("default_empty", r["bundle_admission_state"] == "EMPTY" and not r["sum_certificate_invoked"] and not r["component_sum_certified"], report=r)


def check_T_w_row_bundle_sum_bridge_default_export_locked():
    r = bridge_report(); return _res("default_export_locked", not r["physical_W_export_enabled"] and not r["exports_physical_M_W"])


def check_T_w_row_bundle_sum_bridge_empty_bundle_cannot_certify():
    r = bridge_report(); return _res("empty_cannot_certify", not r["bundle_admitted"] and not r["component_sum_certified"] and "NO_ADMITTED_BUNDLE_AVAILABLE_FOR_COMPONENT_SUM" in r["failure_reasons"])


def check_T_w_row_bundle_sum_bridge_rejected_bundle_cannot_certify():
    rows = real_candidate_rows_from_shape_template()[:-1]
    r = bridge_report(rows, metadata=default_bundle_metadata(bundle_id="rejected_missing_component"), covariance_supplied=True, uncertainty_supplied=True)
    return _res("rejected_cannot_certify", r["bundle_admission_state"] == "REJECTED" and not r["component_sum_certified"])


def check_T_w_row_bundle_sum_bridge_admitted_bundle_constructs_summands():
    rows = real_candidate_rows_from_shape_template()
    r = bridge_report(rows, metadata=default_bundle_metadata(bundle_id="admitted_zero_rows"))
    return _res("admitted_constructs_summands", r["bundle_admitted"] and r["summand_rows_constructed"] and r["summand_row_count"] == len(FINITE_PART_COMPONENT_ORDER), report=r)


def check_T_w_row_bundle_sum_bridge_summand_translation_preserves_order():
    rows = real_candidate_rows_from_shape_template()
    summands = rows_to_summands(rows)
    p = tuple(s["component_id"] for s in summands) == FINITE_PART_COMPONENT_ORDER
    return _res("order_preserved", p, summands=summands)


def check_T_w_row_bundle_sum_bridge_summand_translation_preserves_symbols():
    rows = real_candidate_rows_from_shape_template()
    summands = rows_to_summands(rows)
    p = all(s["symbol"] == COMPONENT_SYMBOLS[s["component_id"]] for s in summands)
    return _res("symbols_preserved", p)


def check_T_w_row_bundle_sum_bridge_zero_rows_do_not_certify_sum():
    rows = real_candidate_rows_from_shape_template()
    r = bridge_report(rows, metadata=default_bundle_metadata(bundle_id="zero_rows"), covariance_supplied=True, uncertainty_supplied=True)
    return _res("zero_rows_no_cert", r["bundle_admitted"] and not r["component_sum_certified"], report=r)


def check_T_w_row_bundle_sum_bridge_dry_target_rows_can_certify_mechanics():
    rows = dry_target_sum_bundle_rows()
    r = bridge_report(rows, metadata=default_bundle_metadata(bundle_id="dry_target_sum"), covariance_supplied=True, uncertainty_supplied=True, tolerance=Decimal("1e-9"))
    return _res("dry_target_mechanics", r["bundle_admitted"] and r["component_sum_report"]["component_sum_certified"] and r["component_sum_certified"], report=r)


def check_T_w_row_bundle_sum_bridge_dry_target_rows_do_not_unlock_export():
    rows = dry_target_sum_bundle_rows()
    r = bridge_report(rows, metadata=default_bundle_metadata(bundle_id="dry_target_sum"), covariance_supplied=True, uncertainty_supplied=True, tolerance=Decimal("1e-9"))
    return _res("dry_no_export", r["component_sum_certified"] and not r["physical_W_export_enabled"] and not r["exports_physical_M_W"])


def check_T_w_row_bundle_sum_bridge_requires_covariance_for_certification():
    rows = dry_target_sum_bundle_rows()
    r = bridge_report(rows, metadata=default_bundle_metadata(bundle_id="dry_no_cov"), covariance_supplied=False, uncertainty_supplied=True, tolerance=Decimal("1e-9"))
    return _res("requires_covariance", not r["component_sum_certified"] and "COVARIANCE_PROTOCOL_UNSUPPLIED" in r["failure_reasons"])


def check_T_w_row_bundle_sum_bridge_requires_uncertainty_for_certification():
    rows = dry_target_sum_bundle_rows()
    r = bridge_report(rows, metadata=default_bundle_metadata(bundle_id="dry_no_unc"), covariance_supplied=True, uncertainty_supplied=False, tolerance=Decimal("1e-9"))
    return _res("requires_uncertainty", not r["component_sum_certified"] and "UNCERTAINTY_PROTOCOL_UNSUPPLIED" in r["failure_reasons"])


def check_T_w_row_bundle_sum_bridge_rejects_order_mismatch():
    rows = tuple(reversed(real_candidate_rows_from_shape_template()))
    r = bridge_report(rows, metadata=default_bundle_metadata(bundle_id="bad_order", declared_component_order=tuple(reversed(FINITE_PART_COMPONENT_ORDER))))
    return _res("rejects_order_mismatch", not r["component_sum_certified"] and r["bundle_admission_state"] == "REJECTED")


def check_T_w_row_bundle_sum_bridge_forbids_observed_w_consumption():
    rows = list(real_candidate_rows_from_shape_template()); rows[0] = dict(rows[0]); rows[0]["consumed_inputs"] = ("observed_M_W_column",)
    r = bridge_report(rows, metadata=default_bundle_metadata(bundle_id="obs_w"))
    return _res("forbid_observed_w", not r["component_sum_certified"] and "FORBIDDEN_BRIDGE_INPUT_CONSUMED" in r["failure_reasons"])


def check_T_w_row_bundle_sum_bridge_forbids_apf_anchor_consumption():
    rows = list(real_candidate_rows_from_shape_template()); rows[0] = dict(rows[0]); rows[0]["consumed_inputs"] = ("APF_ANCHOR_DELTA_R_TARGET",)
    r = bridge_report(rows, metadata=default_bundle_metadata(bundle_id="apf_anchor"))
    return _res("forbid_apf_anchor", not r["component_sum_certified"] and "FORBIDDEN_BRIDGE_INPUT_CONSUMED" in r["failure_reasons"])


def check_T_w_row_bundle_sum_bridge_forbids_residual_fit_consumption():
    rows = list(real_candidate_rows_from_shape_template()); rows[0] = dict(rows[0]); rows[0]["consumed_inputs"] = ("component_sum_residual_to_apf_target",)
    r = bridge_report(rows, metadata=default_bundle_metadata(bundle_id="residual_fit"))
    return _res("forbid_residual_fit", not r["component_sum_certified"] and "FORBIDDEN_BRIDGE_INPUT_CONSUMED" in r["failure_reasons"])


def check_T_w_row_bundle_sum_bridge_blocks_physical_export_request():
    rows = dry_target_sum_bundle_rows()
    r = bridge_report(rows, metadata=default_bundle_metadata(bundle_id="export_block", physical_export_request=True), covariance_supplied=True, uncertainty_supplied=True, tolerance=Decimal("1e-9"), physical_export_requested=True)
    return _res("blocks_export_request", not r["physical_W_export_enabled"] and "PHYSICAL_EXPORT_REQUEST_BLOCKED_AT_ROW_BUNDLE_SUM_BRIDGE" in r["failure_reasons"])


def check_T_w_row_bundle_sum_bridge_manifest_remains_open():
    m = manifest(); p = not m["real_row_bundle_admitted"] and not m["numerical_component_sum_certified"] and not m["physical_W_export_enabled"]
    return _res("manifest_open", p, manifest=m)


def check_T_w_row_bundle_sum_bridge_export_lock_still_false():
    lock = export_lock_report()
    pred = release_predicate()
    p = (not bool(pred)) and not lock.get("physical_W_export_enabled", False)
    return _res("export_lock_false", p, export_lock=lock)


def check_T_w_row_bundle_sum_bridge_no_physical_mass_export():
    r = bridge_report(dry_target_sum_bundle_rows(), metadata=default_bundle_metadata(bundle_id="dry_target_sum"), covariance_supplied=True, uncertainty_supplied=True, tolerance=Decimal("1e-9"))
    p = not r["physical_W_export_enabled"] and not r["exports_physical_M_W"] and not EXPORTS_PHYSICAL_M_W
    return _res("no_physical_mass_export", p, report=r)


def check_T_w_row_bundle_sum_bridge_forbidden_inputs_named():
    needed = {"observed_M_W_column", "APF_ANCHOR_DELTA_R_TARGET", "component_sum_residual_to_apf_target", "physical_W_export_request"}
    return _res("forbidden_named", needed.issubset(set(FORBIDDEN_BRIDGE_INPUTS)), forbidden=FORBIDDEN_BRIDGE_INPUTS)


def check_T_w_row_bundle_sum_bridge_bank_closure():
    deps = [
        check_T_w_row_bundle_sum_bridge_status_declared(),
        check_T_w_row_bundle_sum_bridge_depends_on_v109_bundle_gate(),
        check_T_w_row_bundle_sum_bridge_depends_on_v104_sum_harness(),
        check_T_w_row_bundle_sum_bridge_default_empty_no_invocation(),
        check_T_w_row_bundle_sum_bridge_manifest_remains_open(),
        check_T_w_row_bundle_sum_bridge_no_physical_mass_export(),
    ]
    p = all(_passed(d) for d in deps) and not NUMERICAL_COMPONENT_SUM_CERTIFIED and not PHYSICAL_W_EXPORT_ENABLED
    return _res("bank_closure", p, deps=deps, manifest=manifest())


CHECKS = {
    "T_w_row_bundle_sum_bridge_status_declared": check_T_w_row_bundle_sum_bridge_status_declared,
    "T_w_row_bundle_sum_bridge_depends_on_v109_bundle_gate": check_T_w_row_bundle_sum_bridge_depends_on_v109_bundle_gate,
    "T_w_row_bundle_sum_bridge_depends_on_v104_sum_harness": check_T_w_row_bundle_sum_bridge_depends_on_v104_sum_harness,
    "T_w_row_bundle_sum_bridge_policy_blocks_export": check_T_w_row_bundle_sum_bridge_policy_blocks_export,
    "T_w_row_bundle_sum_bridge_required_fields_declared": check_T_w_row_bundle_sum_bridge_required_fields_declared,
    "T_w_row_bundle_sum_bridge_default_empty_no_invocation": check_T_w_row_bundle_sum_bridge_default_empty_no_invocation,
    "T_w_row_bundle_sum_bridge_default_export_locked": check_T_w_row_bundle_sum_bridge_default_export_locked,
    "T_w_row_bundle_sum_bridge_empty_bundle_cannot_certify": check_T_w_row_bundle_sum_bridge_empty_bundle_cannot_certify,
    "T_w_row_bundle_sum_bridge_rejected_bundle_cannot_certify": check_T_w_row_bundle_sum_bridge_rejected_bundle_cannot_certify,
    "T_w_row_bundle_sum_bridge_admitted_bundle_constructs_summands": check_T_w_row_bundle_sum_bridge_admitted_bundle_constructs_summands,
    "T_w_row_bundle_sum_bridge_summand_translation_preserves_order": check_T_w_row_bundle_sum_bridge_summand_translation_preserves_order,
    "T_w_row_bundle_sum_bridge_summand_translation_preserves_symbols": check_T_w_row_bundle_sum_bridge_summand_translation_preserves_symbols,
    "T_w_row_bundle_sum_bridge_zero_rows_do_not_certify_sum": check_T_w_row_bundle_sum_bridge_zero_rows_do_not_certify_sum,
    "T_w_row_bundle_sum_bridge_dry_target_rows_can_certify_mechanics": check_T_w_row_bundle_sum_bridge_dry_target_rows_can_certify_mechanics,
    "T_w_row_bundle_sum_bridge_dry_target_rows_do_not_unlock_export": check_T_w_row_bundle_sum_bridge_dry_target_rows_do_not_unlock_export,
    "T_w_row_bundle_sum_bridge_requires_covariance_for_certification": check_T_w_row_bundle_sum_bridge_requires_covariance_for_certification,
    "T_w_row_bundle_sum_bridge_requires_uncertainty_for_certification": check_T_w_row_bundle_sum_bridge_requires_uncertainty_for_certification,
    "T_w_row_bundle_sum_bridge_rejects_order_mismatch": check_T_w_row_bundle_sum_bridge_rejects_order_mismatch,
    "T_w_row_bundle_sum_bridge_forbids_observed_w_consumption": check_T_w_row_bundle_sum_bridge_forbids_observed_w_consumption,
    "T_w_row_bundle_sum_bridge_forbids_apf_anchor_consumption": check_T_w_row_bundle_sum_bridge_forbids_apf_anchor_consumption,
    "T_w_row_bundle_sum_bridge_forbids_residual_fit_consumption": check_T_w_row_bundle_sum_bridge_forbids_residual_fit_consumption,
    "T_w_row_bundle_sum_bridge_blocks_physical_export_request": check_T_w_row_bundle_sum_bridge_blocks_physical_export_request,
    "T_w_row_bundle_sum_bridge_manifest_remains_open": check_T_w_row_bundle_sum_bridge_manifest_remains_open,
    "T_w_row_bundle_sum_bridge_export_lock_still_false": check_T_w_row_bundle_sum_bridge_export_lock_still_false,
    "T_w_row_bundle_sum_bridge_no_physical_mass_export": check_T_w_row_bundle_sum_bridge_no_physical_mass_export,
    "T_w_row_bundle_sum_bridge_forbidden_inputs_named": check_T_w_row_bundle_sum_bridge_forbidden_inputs_named,
    "T_w_row_bundle_sum_bridge_bank_closure": check_T_w_row_bundle_sum_bridge_bank_closure,
}

if __name__ == "__main__":
    failures = []
    for name, fn in CHECKS.items():
        out = fn()
        ok = _passed(out)
        print(("PASS" if ok else "FAIL") + " " + name)
        if not ok:
            failures.append((name, out))
    if failures:
        raise SystemExit(1)
    print("W_TRACE_ROW_BUNDLE_TO_COMPONENT_SUM_BRIDGE_BANK_PASS")

# Bank registry compatibility -------------------------------------------------
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
        "status": "W_TRACE_ROW_BUNDLE_TO_COMPONENT_SUM_BRIDGE_BANK_PASS" if ok else "W_TRACE_ROW_BUNDLE_TO_COMPONENT_SUM_BRIDGE_BANK_FAIL",
        "checks": rows,
        "manifest": manifest(),
    }
