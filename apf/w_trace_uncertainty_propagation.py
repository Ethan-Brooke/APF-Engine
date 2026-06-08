"""W_TRACE covariance / uncertainty propagation harness bank.

v10.5 (2026-05-09 LATER-27): uncertainty-propagation harness after the
v10.4 component-sum certificate.  This module defines the covariance schema,
linear push-forward contract, and W-export uncertainty prerequisites for the
W_TRACE -> on-shell route.  It deliberately ships with no admitted real
finite-part rows, no supplied covariance matrix, and no physical W export.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation, getcontext
from typing import Any, Dict, Mapping, Sequence, Tuple

from apf.w_trace_component_sum_certificate import (
    W_COMPONENT_SUM_CERTIFICATE_STATUS,
    component_sum_certificate_report,
    shape_candidate_rows,
    _dry_rows_shifted_to_target,
    check_T_w_component_sum_certificate_bank_closure as _check_v104,
)
from apf.w_trace_finite_part_skeleton import FINITE_PART_COMPONENT_ORDER, COMPONENT_SYMBOLS
from apf.w_trace_finite_part_ledger import apf_anchor_delta_r_target
from apf.trace_transport_completion import (
    check_T_physical_export_gate_locked_until_all_certificates_filled as _check_completion,
)

getcontext().prec = 50

W_UNCERTAINTY_PROPAGATION_STATUS = "P_w_uncertainty_propagation_harness"
UNCERTAINTY_PROPAGATION_DECLARED = True
UNCERTAINTY_PROPAGATION_VERSION = "w_trace_uncertainty_propagation_harness_v0"
UNCERTAINTY_PROPAGATION_MODE = "HARNESS_ONLY_NO_REAL_COVARIANCE_NO_PHYSICAL_EXPORT"

REAL_COMPONENT_ROWS_ADMITTED = False
COVARIANCE_MATRIX_SUPPLIED = False
COVARIANCE_MATRIX_CERTIFIED = False
UNCERTAINTY_VECTOR_SUPPLIED = False
UNCERTAINTY_PROPAGATION_CERTIFIED = False
COMPONENT_SUM_NUMERICALLY_CERTIFIED = False
PHYSICAL_W_EXPORT_ENABLED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

COVARIANCE_REQUIRED_FIELDS: Tuple[str, ...] = (
    "component_order",
    "matrix_kind",
    "dimension",
    "entries",
    "units",
    "provenance_digest",
    "target_observables_consumed",
    "apf_target_consumed",
)

UNCERTAINTY_REPORT_FIELDS: Tuple[str, ...] = (
    "status",
    "version",
    "component_order",
    "covariance_supplied",
    "covariance_shape_ok",
    "covariance_symmetric",
    "covariance_diagonal_nonnegative",
    "covariance_forbidden_inputs_absent",
    "sigma_delta_r",
    "jacobian_declared",
    "sigma_M_W_symbolic",
    "uncertainty_propagation_certified",
    "physical_W_export_enabled",
    "failure_reasons",
)

FORBIDDEN_UNCERTAINTY_INPUTS: Tuple[str, ...] = (
    "observed_M_W",
    "observed_M_W_uncertainty",
    "observed_M_W_column",
    "M_W_world_average",
    "world_average_W_mass_column",
    "W_mass_residual",
    "W_mass_residual_column",
    "Delta_r_fit_to_observed_M_W",
    "APF_ANCHOR_DELTA_R_TARGET",
    "component_sum_residual_to_apf_target",
    "target_closure_residual_column",
    "physical_W_export_request",
)

DEFAULT_DELTA_R_TO_MW_JACOBIAN_LABEL = "dM_W/dDelta_r evaluated only after finite map/counterterm convention is certified"

@dataclass(frozen=True)
class CovarianceMatrixRecord:
    component_order: Tuple[str, ...]
    matrix_kind: str
    entries: Tuple[Tuple[str, ...], ...]
    units: str
    provenance_digest: str
    target_observables_consumed: Tuple[str, ...] = ()
    apf_target_consumed: bool = False

    @property
    def dimension(self) -> int:
        return len(self.component_order)


@dataclass(frozen=True)
class UncertaintyPropagationPolicy:
    require_exact_component_order: bool = True
    require_symmetric_covariance: bool = True
    require_nonnegative_diagonal: bool = True
    require_independent_covariance_provenance: bool = True
    allow_apf_anchor_as_comparison_target_only: bool = True
    allow_apf_anchor_as_covariance_input: bool = False
    allow_observed_w_as_uncertainty_input: bool = False
    allow_physical_export_from_harness: bool = False


def _passed(r: Mapping[str, Any]) -> bool:
    return bool(r.get("passed") is True or str(r.get("status", "")).upper() in {"PASS", "P"})


def policy() -> UncertaintyPropagationPolicy:
    return UncertaintyPropagationPolicy()


def empty_covariance_record() -> CovarianceMatrixRecord:
    return CovarianceMatrixRecord(
        component_order=FINITE_PART_COMPONENT_ORDER,
        matrix_kind="empty_placeholder_no_real_covariance",
        entries=tuple(tuple("UNSUPPLIED" for _ in FINITE_PART_COMPONENT_ORDER) for _ in FINITE_PART_COMPONENT_ORDER),
        units="dimensionless_delta_r_squared",
        provenance_digest="UNSUPPLIED",
    )


def diagonal_shape_covariance(value: str = "1e-8") -> CovarianceMatrixRecord:
    rows = []
    for i, _ in enumerate(FINITE_PART_COMPONENT_ORDER):
        rows.append(tuple(value if i == j else "0" for j, _ in enumerate(FINITE_PART_COMPONENT_ORDER)))
    return CovarianceMatrixRecord(
        component_order=FINITE_PART_COMPONENT_ORDER,
        matrix_kind="dryrun_diagonal_shape_not_real_payload",
        entries=tuple(rows),
        units="dimensionless_delta_r_squared",
        provenance_digest="DRYRUN_SHAPE_NOT_REAL_EXTERNAL_SOURCE",
    )


def _decimal(x: Any) -> Decimal | None:
    try:
        s = str(x)
        if s.upper() in {"UNSUPPLIED", "UNEVALUATED", "UNFILLED", "NONE", ""}:
            return None
        return Decimal(s)
    except (InvalidOperation, ValueError):
        return None


def _cov_shape_ok(cov: CovarianceMatrixRecord | None) -> bool:
    if cov is None:
        return False
    n = len(FINITE_PART_COMPONENT_ORDER)
    return cov.component_order == FINITE_PART_COMPONENT_ORDER and len(cov.entries) == n and all(len(row) == n for row in cov.entries)


def _cov_symmetric(cov: CovarianceMatrixRecord | None) -> bool:
    if not _cov_shape_ok(cov):
        return False
    n = len(cov.entries)
    for i in range(n):
        for j in range(n):
            a = _decimal(cov.entries[i][j])
            b = _decimal(cov.entries[j][i])
            if a is None or b is None or a != b:
                return False
    return True


def _cov_diagonal_nonnegative(cov: CovarianceMatrixRecord | None) -> bool:
    if not _cov_shape_ok(cov):
        return False
    for i in range(len(cov.entries)):
        a = _decimal(cov.entries[i][i])
        if a is None or a < 0:
            return False
    return True


def _cov_forbidden_inputs_absent(cov: CovarianceMatrixRecord | None) -> bool:
    if cov is None:
        return False
    if cov.apf_target_consumed:
        return False
    return not set(cov.target_observables_consumed).intersection(FORBIDDEN_UNCERTAINTY_INPUTS)


def sigma_delta_r_from_covariance(cov: CovarianceMatrixRecord | None) -> Decimal | None:
    """For Delta_r = sum_i component_i, variance is 1^T Cov 1."""
    if not (_cov_shape_ok(cov) and _cov_symmetric(cov) and _cov_diagonal_nonnegative(cov)):
        return None
    total = Decimal("0")
    for row in cov.entries:
        for x in row:
            v = _decimal(x)
            if v is None:
                return None
            total += v
    if total < 0:
        return None
    # Decimal sqrt is available in current supported runtime.
    return total.sqrt()


def uncertainty_propagation_report(
    cov: CovarianceMatrixRecord | None = None,
    covariance_supplied: bool = False,
    rows_admitted: bool = False,
    component_sum_certified: bool = False,
    jacobian_declared: bool = True,
    physical_export_requested: bool = False,
) -> Dict[str, Any]:
    shape_ok = _cov_shape_ok(cov)
    symmetric = _cov_symmetric(cov)
    diag_ok = _cov_diagonal_nonnegative(cov)
    forbidden_absent = _cov_forbidden_inputs_absent(cov)
    sigma_dr = sigma_delta_r_from_covariance(cov) if covariance_supplied else None
    sigma_mw_symbolic = None
    if sigma_dr is not None and jacobian_declared:
        sigma_mw_symbolic = f"|{DEFAULT_DELTA_R_TO_MW_JACOBIAN_LABEL}| * {sigma_dr:.17E}"
    certified = bool(
        covariance_supplied
        and rows_admitted
        and component_sum_certified
        and shape_ok
        and symmetric
        and diag_ok
        and forbidden_absent
        and sigma_dr is not None
        and jacobian_declared
    )
    failures = []
    if not covariance_supplied:
        failures.append("NO_COVARIANCE_MATRIX_SUPPLIED")
    if not rows_admitted:
        failures.append("NO_ADMITTED_REAL_COMPONENT_ROWS")
    if not component_sum_certified:
        failures.append("COMPONENT_SUM_NOT_CERTIFIED")
    if covariance_supplied and not shape_ok:
        failures.append("COVARIANCE_SHAPE_NOT_EXACT_COMPONENT_ORDER")
    if covariance_supplied and not symmetric:
        failures.append("COVARIANCE_NOT_SYMMETRIC_OR_UNEVALUATED")
    if covariance_supplied and not diag_ok:
        failures.append("COVARIANCE_DIAGONAL_NEGATIVE_OR_UNEVALUATED")
    if covariance_supplied and not forbidden_absent:
        failures.append("FORBIDDEN_TARGET_OR_APF_INPUT_CONSUMED_BY_COVARIANCE")
    if not jacobian_declared:
        failures.append("W_PUSHFORWARD_JACOBIAN_UNDECLARED")
    if physical_export_requested:
        failures.append("PHYSICAL_W_EXPORT_REQUEST_BLOCKED_AT_UNCERTAINTY_HARNESS")
    return {
        "status": W_UNCERTAINTY_PROPAGATION_STATUS,
        "version": UNCERTAINTY_PROPAGATION_VERSION,
        "component_order": FINITE_PART_COMPONENT_ORDER,
        "component_symbols": COMPONENT_SYMBOLS,
        "covariance_supplied": bool(covariance_supplied),
        "covariance_shape_ok": shape_ok,
        "covariance_symmetric": symmetric,
        "covariance_diagonal_nonnegative": diag_ok,
        "covariance_forbidden_inputs_absent": forbidden_absent,
        "sigma_delta_r": None if sigma_dr is None else f"{sigma_dr:.17E}",
        "jacobian_declared": bool(jacobian_declared),
        "sigma_M_W_symbolic": sigma_mw_symbolic,
        "uncertainty_propagation_certified": certified,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "exports_physical_scheme_masses": False,
        "failure_reasons": tuple(dict.fromkeys(failures)),
    }


def manifest() -> Dict[str, Any]:
    return {
        "status": W_UNCERTAINTY_PROPAGATION_STATUS,
        "upstream_status": W_COMPONENT_SUM_CERTIFICATE_STATUS,
        "version": UNCERTAINTY_PROPAGATION_VERSION,
        "mode": UNCERTAINTY_PROPAGATION_MODE,
        "covariance_required_fields": COVARIANCE_REQUIRED_FIELDS,
        "uncertainty_report_fields": UNCERTAINTY_REPORT_FIELDS,
        "forbidden_uncertainty_inputs": FORBIDDEN_UNCERTAINTY_INPUTS,
        "component_order": FINITE_PART_COMPONENT_ORDER,
        "policy": asdict(policy()),
        "real_component_rows_admitted": REAL_COMPONENT_ROWS_ADMITTED,
        "covariance_matrix_supplied": COVARIANCE_MATRIX_SUPPLIED,
        "covariance_matrix_certified": COVARIANCE_MATRIX_CERTIFIED,
        "uncertainty_vector_supplied": UNCERTAINTY_VECTOR_SUPPLIED,
        "uncertainty_propagation_certified": UNCERTAINTY_PROPAGATION_CERTIFIED,
        "component_sum_certified": COMPONENT_SUM_NUMERICALLY_CERTIFIED,
        "physical_W_export_enabled": PHYSICAL_W_EXPORT_ENABLED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "absence_certificate": uncertainty_propagation_report(),
    }


def check_T_w_uncertainty_propagation_status_declared():
    p = UNCERTAINTY_PROPAGATION_DECLARED and W_UNCERTAINTY_PROPAGATION_STATUS == "P_w_uncertainty_propagation_harness"
    return {"passed": p, "status": "PASS" if p else "FAIL", "mode": UNCERTAINTY_PROPAGATION_MODE}


def check_T_w_uncertainty_propagation_depends_on_component_sum_harness():
    d = _check_v104()
    p = _passed(d) and W_COMPONENT_SUM_CERTIFICATE_STATUS == "P_w_component_sum_certificate_harness"
    return {"passed": p, "status": "PASS" if p else "FAIL", "upstream": d.get("status")}


def check_T_w_uncertainty_propagation_schema_declared():
    r = uncertainty_propagation_report()
    p = set(UNCERTAINTY_REPORT_FIELDS).issubset(r.keys()) and len(COVARIANCE_REQUIRED_FIELDS) >= 6
    return {"passed": p, "status": "PASS" if p else "FAIL", "fields": UNCERTAINTY_REPORT_FIELDS}


def check_T_w_uncertainty_propagation_policy_blocks_export():
    pol = policy()
    p = (not pol.allow_physical_export_from_harness and not pol.allow_observed_w_as_uncertainty_input and not pol.allow_apf_anchor_as_covariance_input)
    return {"passed": p, "status": "PASS" if p else "FAIL", "policy": asdict(pol)}


def check_T_w_uncertainty_propagation_empty_by_default():
    r = uncertainty_propagation_report()
    p = not r["covariance_supplied"] and not r["uncertainty_propagation_certified"] and "NO_COVARIANCE_MATRIX_SUPPLIED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_uncertainty_propagation_component_order_matches_skeleton():
    cov = diagonal_shape_covariance()
    p = cov.component_order == FINITE_PART_COMPONENT_ORDER and tuple(COMPONENT_SYMBOLS.keys()) == FINITE_PART_COMPONENT_ORDER
    return {"passed": p, "status": "PASS" if p else "FAIL", "order": cov.component_order}


def check_T_w_uncertainty_propagation_covariance_shape_ok():
    p = _cov_shape_ok(diagonal_shape_covariance())
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_uncertainty_propagation_rejects_bad_shape():
    cov = CovarianceMatrixRecord(component_order=FINITE_PART_COMPONENT_ORDER[:-1], matrix_kind="bad", entries=(("1",),), units="dimensionless", provenance_digest="DRY")
    r = uncertainty_propagation_report(cov, covariance_supplied=True)
    p = not r["covariance_shape_ok"] and "COVARIANCE_SHAPE_NOT_EXACT_COMPONENT_ORDER" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_uncertainty_propagation_symmetric_required():
    cov = diagonal_shape_covariance()
    p = _cov_symmetric(cov)
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_uncertainty_propagation_rejects_asymmetric_covariance():
    rows = [list(r) for r in diagonal_shape_covariance().entries]
    rows[0][1] = "2e-8"
    cov = CovarianceMatrixRecord(FINITE_PART_COMPONENT_ORDER, "asymmetric", tuple(tuple(r) for r in rows), "dimensionless", "DRY")
    r = uncertainty_propagation_report(cov, covariance_supplied=True)
    p = not r["covariance_symmetric"] and "COVARIANCE_NOT_SYMMETRIC_OR_UNEVALUATED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_uncertainty_propagation_diagonal_nonnegative_required():
    cov = diagonal_shape_covariance()
    p = _cov_diagonal_nonnegative(cov)
    return {"passed": p, "status": "PASS" if p else "FAIL"}


def check_T_w_uncertainty_propagation_rejects_negative_variance():
    rows = [list(r) for r in diagonal_shape_covariance().entries]
    rows[0][0] = "-1e-8"
    cov = CovarianceMatrixRecord(FINITE_PART_COMPONENT_ORDER, "negative", tuple(tuple(r) for r in rows), "dimensionless", "DRY")
    r = uncertainty_propagation_report(cov, covariance_supplied=True)
    p = not r["covariance_diagonal_nonnegative"] and "COVARIANCE_DIAGONAL_NEGATIVE_OR_UNEVALUATED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_uncertainty_propagation_computes_sigma_delta_r():
    cov = diagonal_shape_covariance("1e-8")
    sig = sigma_delta_r_from_covariance(cov)
    # eight diagonal entries of 1e-8 => sqrt(8e-8)
    p = sig is not None and Decimal("0.00028") < sig < Decimal("0.00029")
    return {"passed": p, "status": "PASS" if p else "FAIL", "sigma_delta_r": None if sig is None else f"{sig:.17E}"}


def check_T_w_uncertainty_propagation_requires_rows_admitted():
    cov = diagonal_shape_covariance()
    r = uncertainty_propagation_report(cov, covariance_supplied=True, rows_admitted=False, component_sum_certified=True)
    p = not r["uncertainty_propagation_certified"] and "NO_ADMITTED_REAL_COMPONENT_ROWS" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_uncertainty_propagation_requires_component_sum_certified():
    cov = diagonal_shape_covariance()
    r = uncertainty_propagation_report(cov, covariance_supplied=True, rows_admitted=True, component_sum_certified=False)
    p = not r["uncertainty_propagation_certified"] and "COMPONENT_SUM_NOT_CERTIFIED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_uncertainty_propagation_dry_path_certifies_mechanics_only():
    cov = diagonal_shape_covariance()
    r = uncertainty_propagation_report(cov, covariance_supplied=True, rows_admitted=True, component_sum_certified=True)
    p = r["uncertainty_propagation_certified"] and not r["physical_W_export_enabled"] and r["sigma_delta_r"] is not None
    return {"passed": p, "status": "PASS" if p else "FAIL", "dry_report": r}


def check_T_w_uncertainty_propagation_jacobian_required_for_W_pushforward():
    cov = diagonal_shape_covariance()
    r = uncertainty_propagation_report(cov, covariance_supplied=True, rows_admitted=True, component_sum_certified=True, jacobian_declared=False)
    p = not r["uncertainty_propagation_certified"] and "W_PUSHFORWARD_JACOBIAN_UNDECLARED" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_uncertainty_propagation_rejects_apf_anchor_covariance_input():
    cov = CovarianceMatrixRecord(FINITE_PART_COMPONENT_ORDER, "bad", diagonal_shape_covariance().entries, "dimensionless", "DRY", ("APF_ANCHOR_DELTA_R_TARGET",), True)
    r = uncertainty_propagation_report(cov, covariance_supplied=True)
    p = not r["covariance_forbidden_inputs_absent"] and "FORBIDDEN_TARGET_OR_APF_INPUT_CONSUMED_BY_COVARIANCE" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_uncertainty_propagation_rejects_observed_w_uncertainty_input():
    cov = CovarianceMatrixRecord(FINITE_PART_COMPONENT_ORDER, "bad", diagonal_shape_covariance().entries, "dimensionless", "DRY", ("observed_M_W_uncertainty",), False)
    r = uncertainty_propagation_report(cov, covariance_supplied=True)
    p = not r["covariance_forbidden_inputs_absent"] and "FORBIDDEN_TARGET_OR_APF_INPUT_CONSUMED_BY_COVARIANCE" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_uncertainty_propagation_rejects_physical_export_request():
    cov = diagonal_shape_covariance()
    r = uncertainty_propagation_report(cov, covariance_supplied=True, rows_admitted=True, component_sum_certified=True, physical_export_requested=True)
    p = not r["physical_W_export_enabled"] and "PHYSICAL_W_EXPORT_REQUEST_BLOCKED_AT_UNCERTAINTY_HARNESS" in r["failure_reasons"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "report": r}


def check_T_w_uncertainty_propagation_manifest_remains_open():
    m = manifest()
    p = not m["covariance_matrix_supplied"] and not m["uncertainty_propagation_certified"] and not m["physical_W_export_enabled"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "manifest": m}


def check_T_w_uncertainty_propagation_apf_anchor_comparison_only():
    # Anchor is available for comparison in upstream certificate, but not a covariance input.
    target = apf_anchor_delta_r_target()
    m = manifest()
    p = Decimal("0.03") < target < Decimal("0.05") and not m["policy"]["allow_apf_anchor_as_covariance_input"]
    return {"passed": p, "status": "PASS" if p else "FAIL", "target": f"{target:.17E}"}


def check_T_w_uncertainty_propagation_no_physical_mass_exports():
    d = _check_completion()
    m = manifest()
    p = _passed(d) and not m["exports_physical_M_W"] and not m["physical_W_export_enabled"] and not EXPORTS_PHYSICAL_SCHEME_MASSES
    return {"passed": p, "status": "PASS" if p else "FAIL", "completion_gate": d.get("status"), "manifest": m}


def check_T_w_uncertainty_propagation_bank_closure():
    deps = [
        check_T_w_uncertainty_propagation_status_declared(),
        check_T_w_uncertainty_propagation_depends_on_component_sum_harness(),
        check_T_w_uncertainty_propagation_schema_declared(),
        check_T_w_uncertainty_propagation_empty_by_default(),
        check_T_w_uncertainty_propagation_manifest_remains_open(),
        check_T_w_uncertainty_propagation_no_physical_mass_exports(),
    ]
    p = all(_passed(d) for d in deps) and not UNCERTAINTY_PROPAGATION_CERTIFIED and not PHYSICAL_W_EXPORT_ENABLED
    return {
        "passed": p,
        "status": "PASS" if p else "FAIL",
        "tier": 4,
        "epistemic": W_UNCERTAINTY_PROPAGATION_STATUS,
        "dependencies": [str(d.get("status")) for d in deps],
        "manifest": manifest(),
        "closed_now": "covariance schema, sigma_Delta_r push-forward mechanics, W uncertainty Jacobian contract, and uncertainty anti-smuggling guards",
        "not_closed": "real covariance payload, certified component sum, numeric W uncertainty, physical W/on-shell export",
    }


_CHECKS: Dict[str, Any] = {
    "T_w_uncertainty_propagation_status_declared": check_T_w_uncertainty_propagation_status_declared,
    "T_w_uncertainty_propagation_depends_on_component_sum_harness": check_T_w_uncertainty_propagation_depends_on_component_sum_harness,
    "T_w_uncertainty_propagation_schema_declared": check_T_w_uncertainty_propagation_schema_declared,
    "T_w_uncertainty_propagation_policy_blocks_export": check_T_w_uncertainty_propagation_policy_blocks_export,
    "T_w_uncertainty_propagation_empty_by_default": check_T_w_uncertainty_propagation_empty_by_default,
    "T_w_uncertainty_propagation_component_order_matches_skeleton": check_T_w_uncertainty_propagation_component_order_matches_skeleton,
    "T_w_uncertainty_propagation_covariance_shape_ok": check_T_w_uncertainty_propagation_covariance_shape_ok,
    "T_w_uncertainty_propagation_rejects_bad_shape": check_T_w_uncertainty_propagation_rejects_bad_shape,
    "T_w_uncertainty_propagation_symmetric_required": check_T_w_uncertainty_propagation_symmetric_required,
    "T_w_uncertainty_propagation_rejects_asymmetric_covariance": check_T_w_uncertainty_propagation_rejects_asymmetric_covariance,
    "T_w_uncertainty_propagation_diagonal_nonnegative_required": check_T_w_uncertainty_propagation_diagonal_nonnegative_required,
    "T_w_uncertainty_propagation_rejects_negative_variance": check_T_w_uncertainty_propagation_rejects_negative_variance,
    "T_w_uncertainty_propagation_computes_sigma_delta_r": check_T_w_uncertainty_propagation_computes_sigma_delta_r,
    "T_w_uncertainty_propagation_requires_rows_admitted": check_T_w_uncertainty_propagation_requires_rows_admitted,
    "T_w_uncertainty_propagation_requires_component_sum_certified": check_T_w_uncertainty_propagation_requires_component_sum_certified,
    "T_w_uncertainty_propagation_dry_path_certifies_mechanics_only": check_T_w_uncertainty_propagation_dry_path_certifies_mechanics_only,
    "T_w_uncertainty_propagation_jacobian_required_for_W_pushforward": check_T_w_uncertainty_propagation_jacobian_required_for_W_pushforward,
    "T_w_uncertainty_propagation_rejects_apf_anchor_covariance_input": check_T_w_uncertainty_propagation_rejects_apf_anchor_covariance_input,
    "T_w_uncertainty_propagation_rejects_observed_w_uncertainty_input": check_T_w_uncertainty_propagation_rejects_observed_w_uncertainty_input,
    "T_w_uncertainty_propagation_rejects_physical_export_request": check_T_w_uncertainty_propagation_rejects_physical_export_request,
    "T_w_uncertainty_propagation_manifest_remains_open": check_T_w_uncertainty_propagation_manifest_remains_open,
    "T_w_uncertainty_propagation_apf_anchor_comparison_only": check_T_w_uncertainty_propagation_apf_anchor_comparison_only,
    "T_w_uncertainty_propagation_no_physical_mass_exports": check_T_w_uncertainty_propagation_no_physical_mass_exports,
    "T_w_uncertainty_propagation_bank_closure": check_T_w_uncertainty_propagation_bank_closure,
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
        "status": "W_TRACE_UNCERTAINTY_PROPAGATION_BANK_PASS" if ok else "W_TRACE_UNCERTAINTY_PROPAGATION_BANK_FAIL",
        "checks": rows,
        "manifest": manifest(),
    }


if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)
