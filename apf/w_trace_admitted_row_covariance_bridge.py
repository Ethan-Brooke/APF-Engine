"""W_TRACE admitted-row covariance bridge bank.

v11.1 (2026-05-09 LATER-35): bridge from admitted real finite-part row
bundles to the covariance / uncertainty propagation harness.  This module wires
v10.9 row-bundle admission and v11.0 row-bundle-to-component-sum into the v10.5
uncertainty harness.  It deliberately ships with no admitted real rows and no
certified covariance payload, so the W physical export lock remains closed.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation, getcontext
from typing import Any, Dict, Mapping, Sequence, Tuple

from apf.w_trace_finite_part_skeleton import FINITE_PART_COMPONENT_ORDER
from apf.w_trace_real_row_bundle_admission import (
    W_REAL_ROW_BUNDLE_STATUS,
    BUNDLE_ADMISSION_VERSION,
    default_bundle_metadata,
    admit_bundle,
    real_candidate_rows_from_shape_template,
    check_T_w_real_row_bundle_bank_closure as _check_v109,
)
from apf.w_trace_row_bundle_to_component_sum import (
    W_ROW_BUNDLE_TO_COMPONENT_SUM_STATUS,
    ROW_BUNDLE_TO_COMPONENT_SUM_VERSION,
    bridge_report as component_sum_bridge_report,
    dry_target_sum_bundle_rows,
    check_T_w_row_bundle_sum_bridge_bank_closure as _check_v110,
)
from apf.w_trace_uncertainty_propagation import (
    W_UNCERTAINTY_PROPAGATION_STATUS,
    UNCERTAINTY_PROPAGATION_VERSION,
    CovarianceMatrixRecord,
    uncertainty_propagation_report,
    diagonal_shape_covariance,
    sigma_delta_r_from_covariance,
    check_T_w_uncertainty_propagation_bank_closure as _check_v105,
)
from apf.w_trace_physical_export_lock import export_lock_report, release_predicate

getcontext().prec = 50

W_ADMITTED_ROW_COVARIANCE_BRIDGE_STATUS = "P_w_admitted_row_covariance_bridge"
ADMITTED_ROW_COVARIANCE_BRIDGE_VERSION = "w_trace_admitted_row_covariance_bridge_v0"
ADMITTED_ROW_COVARIANCE_BRIDGE_MODE = "EMPTY_BY_DEFAULT_NO_REAL_COVARIANCE_NO_PHYSICAL_EXPORT"

REAL_ROW_BUNDLE_SUPPLIED = False
REAL_ROW_BUNDLE_ADMITTED = False
ROW_BUNDLE_COMPONENT_SUM_BRIDGED = False
ROW_BUNDLE_COVARIANCE_BRIDGED = False
NUMERICAL_COMPONENT_SUM_CERTIFIED = False
COVARIANCE_CERTIFIED = False
UNCERTAINTY_PROPAGATION_CERTIFIED = False
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

COVARIANCE_BRIDGE_REQUIRED_FIELDS: Tuple[str, ...] = (
    "status",
    "version",
    "mode",
    "bundle_admission_state",
    "bundle_admitted",
    "component_sum_certified",
    "covariance_record_constructed",
    "covariance_supplied",
    "covariance_certified",
    "uncertainty_propagation_certified",
    "physical_W_export_enabled",
    "failure_reasons",
)

FORBIDDEN_COVARIANCE_BRIDGE_INPUTS: Tuple[str, ...] = (
    "observed_M_W",
    "observed_M_W_uncertainty",
    "observed_M_W_column",
    "M_W_world_average",
    "world_average_W_mass_column",
    "W_mass_residual",
    "W_mass_residual_column",
    "Delta_r_fit_to_observed_M_W",
    "APF_ANCHOR_DELTA_R_TARGET",
    "APF_ANCHOR_DELTA_R_TARGET_AS_COVARIANCE_VALUE",
    "component_sum_residual_to_apf_target",
    "target_closure_residual_column",
    "posthoc_covariance_fit",
    "physical_W_export_request",
)

@dataclass(frozen=True)
class CovarianceBridgePolicy:
    require_admitted_bundle_before_covariance: bool = True
    require_component_sum_certificate_before_uncertainty: bool = True
    require_exact_component_order: bool = True
    require_row_uncertainties_nonnegative: bool = True
    require_independent_covariance_provenance: bool = True
    allow_empty_bundle_to_certify_covariance: bool = False
    allow_rejected_bundle_to_certify_covariance: bool = False
    allow_apf_anchor_as_covariance_input: bool = False
    allow_observed_w_as_covariance_input: bool = False
    allow_physical_export_from_bridge: bool = False


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def policy() -> CovarianceBridgePolicy:
    return CovarianceBridgePolicy()


def _decimal(x: Any) -> Decimal | None:
    try:
        return Decimal(str(x))
    except (InvalidOperation, ValueError):
        return None


def covariance_from_rows(
    rows: Sequence[Mapping[str, Any]],
    *,
    provenance_digest: str = "sha256:dry-row-uncertainty-covariance-not-real-payload",
    target_observables_consumed: Tuple[str, ...] = (),
    apf_target_consumed: bool = False,
) -> CovarianceMatrixRecord:
    """Build a diagonal covariance record from row uncertainty fields.

    This is an adapter contract, not a claim that the shipped rows are physical
    data.  The values are read from row uncertainties; no APF target or observed
    W quantity is used.
    """
    by_id = {str(r.get("component_id")): r for r in rows}
    entries = []
    for ci in FINITE_PART_COMPONENT_ORDER:
        row = []
        for cj in FINITE_PART_COMPONENT_ORDER:
            if ci == cj:
                u = _decimal(by_id.get(ci, {}).get("uncertainty"))
                row.append("UNSUPPLIED" if u is None else str(u * u))
            else:
                row.append("0")
        entries.append(tuple(row))
    return CovarianceMatrixRecord(
        component_order=FINITE_PART_COMPONENT_ORDER,
        matrix_kind="row_uncertainty_diagonal_bridge_not_real_payload",
        entries=tuple(entries),
        units="dimensionless_delta_r_squared",
        provenance_digest=provenance_digest,
        target_observables_consumed=target_observables_consumed,
        apf_target_consumed=apf_target_consumed,
    )


def dry_covariance_rows() -> Tuple[Dict[str, Any], ...]:
    """Dry rows with positive uncertainties for bridge mechanics only."""
    rows = []
    for i, r in enumerate(real_candidate_rows_from_shape_template(), start=1):
        x = dict(r)
        x["value"] = 0.0
        x["uncertainty"] = float(Decimal("1e-6") * Decimal(i))
        x["source_title"] = "dry-path covariance bridge mechanics row; not physical payload"
        x["provenance_chain"] = tuple(x.get("provenance_chain", ())) + ("dry covariance bridge mechanics only",)
        rows.append(x)
    return tuple(rows)


def bridge_report(
    rows: Sequence[Mapping[str, Any]] | None = None,
    *,
    metadata: Mapping[str, Any] | None = None,
    component_sum_certified: bool = False,
    covariance_supplied: bool = False,
    physical_export_requested: bool = False,
    covariance_record: CovarianceMatrixRecord | None = None,
) -> Dict[str, Any]:
    md = default_bundle_metadata() if metadata is None else dict(metadata)
    supplied_rows = tuple(rows or ())
    bundle = admit_bundle(supplied_rows if rows is not None else None, metadata=md, physical_export_requested=physical_export_requested)
    sum_bridge = component_sum_bridge_report(
        supplied_rows if rows is not None else None,
        metadata=md,
        covariance_supplied=covariance_supplied,
        uncertainty_supplied=covariance_supplied,
        physical_export_requested=physical_export_requested,
    )

    failures = []
    forbidden = []
    for row in supplied_rows:
        for x in tuple(row.get("consumed_inputs", ())):
            if x in FORBIDDEN_COVARIANCE_BRIDGE_INPUTS:
                forbidden.append(x)
        if row.get("physical_export_request"):
            forbidden.append("physical_W_export_request")
    for x in tuple(md.get("consumed_inputs", ())):
        if x in FORBIDDEN_COVARIANCE_BRIDGE_INPUTS:
            forbidden.append(x)
    if physical_export_requested or md.get("physical_export_request"):
        forbidden.append("physical_W_export_request")
    if forbidden:
        failures.append("FORBIDDEN_COVARIANCE_BRIDGE_INPUT_CONSUMED")

    bundle_admitted = bool(bundle.get("bundle_admitted"))
    if not bundle_admitted:
        failures.append("NO_ADMITTED_ROW_BUNDLE_AVAILABLE_FOR_COVARIANCE")

    component_sum_ok = bool(component_sum_certified or sum_bridge.get("component_sum_certified"))
    if not component_sum_ok:
        failures.append("COMPONENT_SUM_NOT_CERTIFIED_FOR_COVARIANCE_PUSHFORWARD")

    constructed = False
    cov = covariance_record
    if cov is None and bundle_admitted and supplied_rows:
        cov = covariance_from_rows(supplied_rows)
        constructed = True
    if covariance_supplied and cov is None:
        failures.append("COVARIANCE_SUPPLIED_FLAG_WITHOUT_RECORD")

    uncertainty = uncertainty_propagation_report(
        cov,
        covariance_supplied=bool(covariance_supplied and cov is not None and not forbidden),
        rows_admitted=bundle_admitted and not forbidden,
        component_sum_certified=component_sum_ok and not forbidden,
        physical_export_requested=physical_export_requested,
    )
    if covariance_supplied:
        failures.extend(tuple(uncertainty.get("failure_reasons", ())))
    if physical_export_requested:
        failures.append("PHYSICAL_EXPORT_REQUEST_BLOCKED_AT_COVARIANCE_BRIDGE")

    covariance_certified = bool(uncertainty.get("covariance_shape_ok") and uncertainty.get("covariance_symmetric") and uncertainty.get("covariance_diagonal_nonnegative") and uncertainty.get("covariance_forbidden_inputs_absent") and covariance_supplied and bundle_admitted and not forbidden)
    uncertainty_certified = bool(uncertainty.get("uncertainty_propagation_certified") and component_sum_ok and covariance_certified)

    return {
        "status": W_ADMITTED_ROW_COVARIANCE_BRIDGE_STATUS,
        "version": ADMITTED_ROW_COVARIANCE_BRIDGE_VERSION,
        "mode": ADMITTED_ROW_COVARIANCE_BRIDGE_MODE,
        "upstream_bundle_status": W_REAL_ROW_BUNDLE_STATUS,
        "upstream_bundle_version": BUNDLE_ADMISSION_VERSION,
        "upstream_sum_bridge_status": W_ROW_BUNDLE_TO_COMPONENT_SUM_STATUS,
        "upstream_sum_bridge_version": ROW_BUNDLE_TO_COMPONENT_SUM_VERSION,
        "upstream_uncertainty_status": W_UNCERTAINTY_PROPAGATION_STATUS,
        "upstream_uncertainty_version": UNCERTAINTY_PROPAGATION_VERSION,
        "bundle_admission_state": bundle.get("admission_state"),
        "bundle_supplied": bool(bundle.get("bundle_supplied")),
        "bundle_admitted": bundle_admitted,
        "row_count": int(bundle.get("row_count", 0)),
        "component_sum_certified": component_sum_ok,
        "covariance_record_constructed": constructed,
        "covariance_supplied": bool(covariance_supplied),
        "covariance_certified": covariance_certified,
        "sigma_delta_r": uncertainty.get("sigma_delta_r"),
        "uncertainty_propagation_certified": uncertainty_certified,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "exports_physical_scheme_masses": False,
        "forbidden_covariance_inputs_hit": tuple(dict.fromkeys(forbidden)),
        "failure_reasons": tuple(dict.fromkeys(failures)),
        "bundle_report": bundle,
        "sum_bridge_report": sum_bridge,
        "uncertainty_report": uncertainty,
    }


def manifest() -> Dict[str, Any]:
    return {
        "status": W_ADMITTED_ROW_COVARIANCE_BRIDGE_STATUS,
        "version": ADMITTED_ROW_COVARIANCE_BRIDGE_VERSION,
        "mode": ADMITTED_ROW_COVARIANCE_BRIDGE_MODE,
        "policy": asdict(policy()),
        "required_fields": COVARIANCE_BRIDGE_REQUIRED_FIELDS,
        "forbidden_covariance_bridge_inputs": FORBIDDEN_COVARIANCE_BRIDGE_INPUTS,
        "component_order": FINITE_PART_COMPONENT_ORDER,
        "real_row_bundle_supplied": REAL_ROW_BUNDLE_SUPPLIED,
        "real_row_bundle_admitted": REAL_ROW_BUNDLE_ADMITTED,
        "row_bundle_component_sum_bridged": ROW_BUNDLE_COMPONENT_SUM_BRIDGED,
        "row_bundle_covariance_bridged": ROW_BUNDLE_COVARIANCE_BRIDGED,
        "numerical_component_sum_certified": NUMERICAL_COMPONENT_SUM_CERTIFIED,
        "covariance_certified": COVARIANCE_CERTIFIED,
        "uncertainty_propagation_certified": UNCERTAINTY_PROPAGATION_CERTIFIED,
        "physical_W_export_enabled": PHYSICAL_W_EXPORT_ENABLED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "default_report": bridge_report(),
    }


def _res(name: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    return {"passed": bool(passed), "status": "PASS" if passed else "FAIL", "tier": 4, "epistemic": W_ADMITTED_ROW_COVARIANCE_BRIDGE_STATUS, "check": name, **extra}


def check_T_w_admitted_row_covariance_bridge_status_declared():
    m = manifest(); return _res("status_declared", m["status"] == W_ADMITTED_ROW_COVARIANCE_BRIDGE_STATUS and not m["physical_W_export_enabled"], manifest=m)


def check_T_w_admitted_row_covariance_bridge_depends_on_v109_bundle_gate():
    d = _check_v109(); return _res("depends_on_v109", _passed(d) and W_REAL_ROW_BUNDLE_STATUS == "P_w_real_row_bundle_admission")


def check_T_w_admitted_row_covariance_bridge_depends_on_v110_sum_bridge():
    d = _check_v110(); return _res("depends_on_v110", _passed(d) and W_ROW_BUNDLE_TO_COMPONENT_SUM_STATUS == "P_w_row_bundle_to_component_sum_bridge")


def check_T_w_admitted_row_covariance_bridge_depends_on_v105_uncertainty_harness():
    d = _check_v105(); return _res("depends_on_v105", _passed(d) and W_UNCERTAINTY_PROPAGATION_STATUS == "P_w_uncertainty_propagation_harness")


def check_T_w_admitted_row_covariance_bridge_policy_blocks_export():
    p = policy(); ok = not p.allow_physical_export_from_bridge and not p.allow_empty_bundle_to_certify_covariance and not p.allow_rejected_bundle_to_certify_covariance
    return _res("policy_blocks_export", ok, policy=asdict(p))


def check_T_w_admitted_row_covariance_bridge_required_fields_declared():
    r = bridge_report(); return _res("required_fields", set(COVARIANCE_BRIDGE_REQUIRED_FIELDS).issubset(r.keys()), fields=COVARIANCE_BRIDGE_REQUIRED_FIELDS)


def check_T_w_admitted_row_covariance_bridge_default_empty_no_covariance():
    r = bridge_report(); ok = r["bundle_admission_state"] == "EMPTY" and not r["covariance_certified"] and "NO_ADMITTED_ROW_BUNDLE_AVAILABLE_FOR_COVARIANCE" in r["failure_reasons"]
    return _res("default_empty_no_covariance", ok, report=r)


def check_T_w_admitted_row_covariance_bridge_default_export_locked():
    r = bridge_report(); return _res("default_export_locked", not r["physical_W_export_enabled"] and not r["exports_physical_M_W"], report=r)


def check_T_w_admitted_row_covariance_bridge_empty_bundle_cannot_certify_covariance():
    r = bridge_report(covariance_supplied=True, covariance_record=diagonal_shape_covariance())
    return _res("empty_bundle_cannot_certify", not r["covariance_certified"] and "NO_ADMITTED_ROW_BUNDLE_AVAILABLE_FOR_COVARIANCE" in r["failure_reasons"])


def check_T_w_admitted_row_covariance_bridge_rejected_bundle_cannot_certify_covariance():
    rows = list(dry_covariance_rows()); rows.pop()
    r = bridge_report(rows, metadata=default_bundle_metadata(bundle_id="rejected_covariance"), component_sum_certified=True, covariance_supplied=True)
    return _res("rejected_bundle_cannot_certify", r["bundle_admission_state"] == "REJECTED" and not r["covariance_certified"])


def check_T_w_admitted_row_covariance_bridge_admitted_rows_construct_covariance_record():
    rows = dry_covariance_rows(); r = bridge_report(rows, metadata=default_bundle_metadata(bundle_id="dry_covariance"), component_sum_certified=True, covariance_supplied=True)
    return _res("admitted_rows_construct_covariance", r["bundle_admitted"] and r["covariance_record_constructed"] and r["covariance_certified"], report=r)


def check_T_w_admitted_row_covariance_bridge_covariance_preserves_order():
    cov = covariance_from_rows(dry_covariance_rows()); return _res("covariance_preserves_order", cov.component_order == FINITE_PART_COMPONENT_ORDER)


def check_T_w_admitted_row_covariance_bridge_diagonal_from_row_uncertainties():
    rows = dry_covariance_rows(); cov = covariance_from_rows(rows); first = Decimal(str(rows[0]["uncertainty"])) ** 2
    return _res("diagonal_from_uncertainties", Decimal(cov.entries[0][0]) == first and cov.entries[0][1] == "0", covariance=cov.entries)


def check_T_w_admitted_row_covariance_bridge_sigma_delta_r_computable():
    cov = covariance_from_rows(dry_covariance_rows()); s = sigma_delta_r_from_covariance(cov)
    return _res("sigma_delta_r_computable", s is not None and s > 0, sigma=None if s is None else str(s))


def check_T_w_admitted_row_covariance_bridge_requires_component_sum_certificate():
    rows = dry_covariance_rows(); r = bridge_report(rows, metadata=default_bundle_metadata(bundle_id="no_sum"), component_sum_certified=False, covariance_supplied=True)
    return _res("requires_component_sum", not r["uncertainty_propagation_certified"] and "COMPONENT_SUM_NOT_CERTIFIED_FOR_COVARIANCE_PUSHFORWARD" in r["failure_reasons"])


def check_T_w_admitted_row_covariance_bridge_component_sum_bridge_integrates():
    rows = dry_target_sum_bundle_rows(); r = bridge_report(rows, metadata=default_bundle_metadata(bundle_id="sum_integrates"), covariance_supplied=True)
    return _res("sum_bridge_integrates", r["sum_bridge_report"]["sum_certificate_invoked"] and isinstance(r["component_sum_certified"], bool), report=r)


def check_T_w_admitted_row_covariance_bridge_dry_path_certifies_uncertainty_mechanics():
    rows = dry_target_sum_bundle_rows(); r = bridge_report(rows, metadata=default_bundle_metadata(bundle_id="dry_uncertainty"), component_sum_certified=True, covariance_supplied=True)
    return _res("dry_path_certifies_mechanics", r["covariance_certified"] and r["uncertainty_propagation_certified"] and not r["physical_W_export_enabled"], report=r)


def check_T_w_admitted_row_covariance_bridge_dry_path_does_not_unlock_export():
    rows = dry_target_sum_bundle_rows(); r = bridge_report(rows, metadata=default_bundle_metadata(bundle_id="dry_no_export"), component_sum_certified=True, covariance_supplied=True)
    return _res("dry_path_no_export", not r["physical_W_export_enabled"] and not r["exports_physical_M_W"], report=r)


def check_T_w_admitted_row_covariance_bridge_forbids_observed_w_uncertainty_input():
    cov = covariance_from_rows(dry_covariance_rows(), target_observables_consumed=("observed_M_W_uncertainty",))
    r = bridge_report(dry_covariance_rows(), metadata=default_bundle_metadata(bundle_id="obs_w_cov"), component_sum_certified=True, covariance_supplied=True, covariance_record=cov)
    return _res("forbid_observed_w_uncertainty", not r["uncertainty_propagation_certified"] and "FORBIDDEN_TARGET_OR_APF_INPUT_CONSUMED_BY_COVARIANCE" in r["failure_reasons"])


def check_T_w_admitted_row_covariance_bridge_forbids_apf_anchor_covariance_input():
    cov = covariance_from_rows(dry_covariance_rows(), apf_target_consumed=True)
    r = bridge_report(dry_covariance_rows(), metadata=default_bundle_metadata(bundle_id="apf_cov"), component_sum_certified=True, covariance_supplied=True, covariance_record=cov)
    return _res("forbid_apf_anchor_covariance", not r["uncertainty_propagation_certified"] and "FORBIDDEN_TARGET_OR_APF_INPUT_CONSUMED_BY_COVARIANCE" in r["failure_reasons"])


def check_T_w_admitted_row_covariance_bridge_forbids_residual_fit_consumption():
    rows = list(dry_covariance_rows()); rows[0] = dict(rows[0]); rows[0]["consumed_inputs"] = ("component_sum_residual_to_apf_target",)
    r = bridge_report(rows, metadata=default_bundle_metadata(bundle_id="residual_cov"), component_sum_certified=True, covariance_supplied=True)
    return _res("forbid_residual_fit", not r["covariance_certified"] and "FORBIDDEN_COVARIANCE_BRIDGE_INPUT_CONSUMED" in r["failure_reasons"])


def check_T_w_admitted_row_covariance_bridge_blocks_physical_export_request():
    rows = dry_covariance_rows(); r = bridge_report(rows, metadata=default_bundle_metadata(bundle_id="export_cov", physical_export_request=True), component_sum_certified=True, covariance_supplied=True, physical_export_requested=True)
    return _res("blocks_export_request", not r["physical_W_export_enabled"] and "PHYSICAL_EXPORT_REQUEST_BLOCKED_AT_COVARIANCE_BRIDGE" in r["failure_reasons"])


def check_T_w_admitted_row_covariance_bridge_rejects_bad_covariance_shape():
    bad = CovarianceMatrixRecord(component_order=("bad",), matrix_kind="bad", entries=(("1",),), units="dimensionless_delta_r_squared", provenance_digest="sha256:bad")
    r = bridge_report(dry_covariance_rows(), metadata=default_bundle_metadata(bundle_id="bad_cov"), component_sum_certified=True, covariance_supplied=True, covariance_record=bad)
    return _res("rejects_bad_covariance_shape", not r["uncertainty_propagation_certified"] and "COVARIANCE_SHAPE_NOT_EXACT_COMPONENT_ORDER" in r["failure_reasons"])


def check_T_w_admitted_row_covariance_bridge_rejects_negative_variance():
    cov = covariance_from_rows(dry_covariance_rows()); rows = [list(row) for row in cov.entries]; rows[0][0] = "-1e-9"
    bad = CovarianceMatrixRecord(cov.component_order, cov.matrix_kind, tuple(tuple(r) for r in rows), cov.units, cov.provenance_digest)
    r = bridge_report(dry_covariance_rows(), metadata=default_bundle_metadata(bundle_id="neg_cov"), component_sum_certified=True, covariance_supplied=True, covariance_record=bad)
    return _res("rejects_negative_variance", not r["uncertainty_propagation_certified"] and "COVARIANCE_DIAGONAL_NEGATIVE_OR_UNEVALUATED" in r["failure_reasons"])


def check_T_w_admitted_row_covariance_bridge_rejects_asymmetric_covariance():
    cov = covariance_from_rows(dry_covariance_rows()); rows = [list(row) for row in cov.entries]; rows[0][1] = "1e-9"; rows[1][0] = "0"
    bad = CovarianceMatrixRecord(cov.component_order, cov.matrix_kind, tuple(tuple(r) for r in rows), cov.units, cov.provenance_digest)
    r = bridge_report(dry_covariance_rows(), metadata=default_bundle_metadata(bundle_id="asym_cov"), component_sum_certified=True, covariance_supplied=True, covariance_record=bad)
    return _res("rejects_asymmetric_covariance", not r["uncertainty_propagation_certified"] and "COVARIANCE_NOT_SYMMETRIC_OR_UNEVALUATED" in r["failure_reasons"])


def check_T_w_admitted_row_covariance_bridge_manifest_remains_open():
    m = manifest(); ok = not m["real_row_bundle_admitted"] and not m["covariance_certified"] and not m["physical_W_export_enabled"]
    return _res("manifest_open", ok, manifest=m)


def check_T_w_admitted_row_covariance_bridge_export_lock_still_false():
    lock = export_lock_report(); pred = release_predicate(); return _res("export_lock_false", (not bool(pred)) and not lock.get("physical_W_export_enabled", False), export_lock=lock)


def check_T_w_admitted_row_covariance_bridge_no_physical_mass_export():
    r = bridge_report(dry_covariance_rows(), metadata=default_bundle_metadata(bundle_id="no_mass_export"), component_sum_certified=True, covariance_supplied=True)
    return _res("no_physical_mass_export", not r["physical_W_export_enabled"] and not r["exports_physical_M_W"] and not EXPORTS_PHYSICAL_M_W, report=r)


def check_T_w_admitted_row_covariance_bridge_forbidden_inputs_named():
    needed = {"observed_M_W_uncertainty", "APF_ANCHOR_DELTA_R_TARGET", "component_sum_residual_to_apf_target", "physical_W_export_request"}
    return _res("forbidden_named", needed.issubset(set(FORBIDDEN_COVARIANCE_BRIDGE_INPUTS)), forbidden=FORBIDDEN_COVARIANCE_BRIDGE_INPUTS)


def check_T_w_admitted_row_covariance_bridge_bank_closure():
    deps = [
        check_T_w_admitted_row_covariance_bridge_status_declared(),
        check_T_w_admitted_row_covariance_bridge_depends_on_v109_bundle_gate(),
        check_T_w_admitted_row_covariance_bridge_depends_on_v110_sum_bridge(),
        check_T_w_admitted_row_covariance_bridge_depends_on_v105_uncertainty_harness(),
        check_T_w_admitted_row_covariance_bridge_default_empty_no_covariance(),
        check_T_w_admitted_row_covariance_bridge_manifest_remains_open(),
        check_T_w_admitted_row_covariance_bridge_no_physical_mass_export(),
    ]
    ok = all(_passed(d) for d in deps) and not COVARIANCE_CERTIFIED and not PHYSICAL_W_EXPORT_ENABLED
    return _res("bank_closure", ok, deps=deps, manifest=manifest())


CHECKS = {
    "T_w_admitted_row_covariance_bridge_status_declared": check_T_w_admitted_row_covariance_bridge_status_declared,
    "T_w_admitted_row_covariance_bridge_depends_on_v109_bundle_gate": check_T_w_admitted_row_covariance_bridge_depends_on_v109_bundle_gate,
    "T_w_admitted_row_covariance_bridge_depends_on_v110_sum_bridge": check_T_w_admitted_row_covariance_bridge_depends_on_v110_sum_bridge,
    "T_w_admitted_row_covariance_bridge_depends_on_v105_uncertainty_harness": check_T_w_admitted_row_covariance_bridge_depends_on_v105_uncertainty_harness,
    "T_w_admitted_row_covariance_bridge_policy_blocks_export": check_T_w_admitted_row_covariance_bridge_policy_blocks_export,
    "T_w_admitted_row_covariance_bridge_required_fields_declared": check_T_w_admitted_row_covariance_bridge_required_fields_declared,
    "T_w_admitted_row_covariance_bridge_default_empty_no_covariance": check_T_w_admitted_row_covariance_bridge_default_empty_no_covariance,
    "T_w_admitted_row_covariance_bridge_default_export_locked": check_T_w_admitted_row_covariance_bridge_default_export_locked,
    "T_w_admitted_row_covariance_bridge_empty_bundle_cannot_certify_covariance": check_T_w_admitted_row_covariance_bridge_empty_bundle_cannot_certify_covariance,
    "T_w_admitted_row_covariance_bridge_rejected_bundle_cannot_certify_covariance": check_T_w_admitted_row_covariance_bridge_rejected_bundle_cannot_certify_covariance,
    "T_w_admitted_row_covariance_bridge_admitted_rows_construct_covariance_record": check_T_w_admitted_row_covariance_bridge_admitted_rows_construct_covariance_record,
    "T_w_admitted_row_covariance_bridge_covariance_preserves_order": check_T_w_admitted_row_covariance_bridge_covariance_preserves_order,
    "T_w_admitted_row_covariance_bridge_diagonal_from_row_uncertainties": check_T_w_admitted_row_covariance_bridge_diagonal_from_row_uncertainties,
    "T_w_admitted_row_covariance_bridge_sigma_delta_r_computable": check_T_w_admitted_row_covariance_bridge_sigma_delta_r_computable,
    "T_w_admitted_row_covariance_bridge_requires_component_sum_certificate": check_T_w_admitted_row_covariance_bridge_requires_component_sum_certificate,
    "T_w_admitted_row_covariance_bridge_component_sum_bridge_integrates": check_T_w_admitted_row_covariance_bridge_component_sum_bridge_integrates,
    "T_w_admitted_row_covariance_bridge_dry_path_certifies_uncertainty_mechanics": check_T_w_admitted_row_covariance_bridge_dry_path_certifies_uncertainty_mechanics,
    "T_w_admitted_row_covariance_bridge_dry_path_does_not_unlock_export": check_T_w_admitted_row_covariance_bridge_dry_path_does_not_unlock_export,
    "T_w_admitted_row_covariance_bridge_forbids_observed_w_uncertainty_input": check_T_w_admitted_row_covariance_bridge_forbids_observed_w_uncertainty_input,
    "T_w_admitted_row_covariance_bridge_forbids_apf_anchor_covariance_input": check_T_w_admitted_row_covariance_bridge_forbids_apf_anchor_covariance_input,
    "T_w_admitted_row_covariance_bridge_forbids_residual_fit_consumption": check_T_w_admitted_row_covariance_bridge_forbids_residual_fit_consumption,
    "T_w_admitted_row_covariance_bridge_blocks_physical_export_request": check_T_w_admitted_row_covariance_bridge_blocks_physical_export_request,
    "T_w_admitted_row_covariance_bridge_rejects_bad_covariance_shape": check_T_w_admitted_row_covariance_bridge_rejects_bad_covariance_shape,
    "T_w_admitted_row_covariance_bridge_rejects_negative_variance": check_T_w_admitted_row_covariance_bridge_rejects_negative_variance,
    "T_w_admitted_row_covariance_bridge_rejects_asymmetric_covariance": check_T_w_admitted_row_covariance_bridge_rejects_asymmetric_covariance,
    "T_w_admitted_row_covariance_bridge_manifest_remains_open": check_T_w_admitted_row_covariance_bridge_manifest_remains_open,
    "T_w_admitted_row_covariance_bridge_export_lock_still_false": check_T_w_admitted_row_covariance_bridge_export_lock_still_false,
    "T_w_admitted_row_covariance_bridge_no_physical_mass_export": check_T_w_admitted_row_covariance_bridge_no_physical_mass_export,
    "T_w_admitted_row_covariance_bridge_forbidden_inputs_named": check_T_w_admitted_row_covariance_bridge_forbidden_inputs_named,
    "T_w_admitted_row_covariance_bridge_bank_closure": check_T_w_admitted_row_covariance_bridge_bank_closure,
}

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
        "status": "W_TRACE_ADMITTED_ROW_COVARIANCE_BRIDGE_BANK_PASS" if ok else "W_TRACE_ADMITTED_ROW_COVARIANCE_BRIDGE_BANK_FAIL",
        "checks": rows,
        "manifest": manifest(),
    }


if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
