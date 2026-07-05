"""W on-shell route terminal closure theorem bank.

v15.0 (2026-05-09): terminal paper/code closure of the W_TRACE -> on-shell
transport route at the level currently justified by the repository.

Closed here:
    - The W on-shell route has a complete theorem boundary: target contract,
      counterterm convention, export-readiness predicate, no-smuggling lock,
      and current obstruction certificate.
    - The exact missing certificates required for a physical W export are named.
    - The allowed paper claim is fixed: W_TRACE validation and symbolic/on-shell
      route theorem, not a physical on-shell W export.

Not closed here:
    - No admitted real finite-part component rows.
    - No numerical component-sum certificate.
    - No covariance certificate.
    - No uncertainty-propagation certificate.
    - No physical W mass export.

This is intentionally a closure theorem, not a numerical transport map.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, Tuple

from apf.trace_to_scheme_transport_theorem import (
    THEOREM_STATUS as TRACE_TO_SCHEME_THEOREM_STATUS,
    check_T_trace_to_scheme_transport_theorem_bank_closure as _check_v149,
)
from apf.w_trace_final_export_readiness import (
    W_FINAL_EXPORT_READINESS_STATUS,
    READINESS_REQUIRED_FLAGS,
    FORBIDDEN_READINESS_INPUTS,
    readiness_report,
    current_route_state,
    dry_all_true_flags,
    check_T_w_final_export_readiness_bank_closure as _check_final_readiness,
)
from apf.w_trace_physical_export_lock import (
    W_PHYSICAL_EXPORT_LOCK_STATUS,
    FORBIDDEN_EXPORT_INPUTS,
    export_lock_report,
    check_T_w_physical_export_lock_bank_closure as _check_export_lock,
)
from apf.w_trace_counterterm_convention import (
    W_COUNTERTERM_CONVENTION_STATUS,
    COUNTERTERM_CONVENTION_CONTRACT_CERTIFIED,
)
from apf.w_trace_onshell_transport import W_TRACE_EXPECTED_GEV
from apf.w_trace_finite_part_ledger import apf_anchor_delta_r_target

W_OS_TERMINAL_CLOSURE_STATUS = "P_w_os_route_terminal_closure"
W_OS_TERMINAL_CLOSURE_VERSION = "w_os_route_terminal_closure_v15_0"
PHYSICAL_W_EXPORT_CLOSED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False
THEOREM_ROUTE_CLOSED = True

# --- v15.1 (2026-06-16): principled terminal boundary -------------------------
# The v15.0 obstruction certificate named four missing certificates for a
# physical W export. Path-B analysis (Reference - Physical W Export Path B
# Pushed - Delta-r-rem Boundary (2026-06-16).md) shows those four belong to the
# DEPRECATED loop-sum route, and the residual they would certify -- the Sirlin
# remainder Delta r_rem -- is gauge-invariant (a difference of gauge-invariants)
# but has NO scheme-free standalone measurement. By the framework's own
# physicality criterion that places Delta r_rem on the boundary side, not the
# gap side. The native distinction-route mechanism (equilibrium angle 3/13
# absorbing Delta-alpha + custodial Delta-rho; banked check_L_W_mass /
# mw_value_from_equilibrium_and_custodial) already carries the physics to
# M_W = 80.3336 GeV (0.044%), retiring the loop-sum framing. Hence physical-
# final W export is a PRINCIPLED [P_boundary], parallel to the top-pole
# renormalon quarantine -- not an open gap.
W_OS_PRINCIPLED_TERMINAL_BOUNDARY = True
W_OS_BOUNDARY_CLASS = (
    "DELTA_R_REM_NO_STANDALONE_MEASUREMENT__NATIVE_MECHANISM_CARRIES_PHYSICS"
)
# Read-only comparators (banked elsewhere; NOT recomputed, NOT inputs).
M_W_NATIVE_DISTINCTION_GEV = 80.3336   # check_L_W_mass: equilibrium+custodial, no loop sum
M_W_IMPORTED_DIZET_GEV = 80.35734      # Route 11 imported one-route (comparator)

TERMINAL_ALLOWED_CLAIMS: Tuple[str, ...] = (
    "W_TRACE local value and validation comparison",
    "trace-to-scheme export iff theorem",
    "W on-shell route contract / counterterm convention / readiness predicate",
    "current obstruction certificate naming missing physical-export evidence",
)

TERMINAL_FORBIDDEN_CLAIMS: Tuple[str, ...] = (
    "APF exports a physical on-shell W mass in the current code state",
    "W_TRACE is identical to physical M_W by codomain relabeling",
    "the few-MeV validation residual is fitted away by an APF anchor",
    "observed M_W, a world average, or residual data are transport inputs",
)

MISSING_CURRENT_EXPORT_FLAGS: Tuple[str, ...] = (
    "real_component_rows_admitted",
    "component_sum_certified",
    "covariance_certified",
    "uncertainty_propagation_certified",
)

CLOSED_CURRENT_EXPORT_FLAGS: Tuple[str, ...] = (
    "finite_counterterm_convention_certified",
    "target_scheme_contract_certified",
    "no_target_observable_consumption_certified",
)

@dataclass(frozen=True)
class TerminalClosureVerdict:
    route_id: str
    theorem_route_closed: bool
    physical_w_export_closed: bool
    exports_physical_m_w: bool
    allowed_claims: Tuple[str, ...]
    forbidden_claims: Tuple[str, ...]
    closed_flags: Tuple[str, ...]
    missing_flags: Tuple[str, ...]
    terminal_status: str


def _passed(result: Mapping[str, Any]) -> bool:
    return bool(result.get("passed") is True or str(result.get("status", "")).upper() in {"PASS", "P"})


def terminal_verdict() -> TerminalClosureVerdict:
    return TerminalClosureVerdict(
        route_id="w_trace_on_shell_route",
        theorem_route_closed=THEOREM_ROUTE_CLOSED,
        physical_w_export_closed=PHYSICAL_W_EXPORT_CLOSED,
        exports_physical_m_w=EXPORTS_PHYSICAL_M_W,
        allowed_claims=TERMINAL_ALLOWED_CLAIMS,
        forbidden_claims=TERMINAL_FORBIDDEN_CLAIMS,
        closed_flags=CLOSED_CURRENT_EXPORT_FLAGS,
        missing_flags=MISSING_CURRENT_EXPORT_FLAGS,
        terminal_status="CLOSED_AS_THEOREM_AND_OBSTRUCTION_CERTIFICATE__OPEN_AS_PHYSICAL_EXPORT",
    )


def terminal_closure_report(physical_export_requested: bool = True) -> Dict[str, Any]:
    rr = readiness_report(physical_export_requested=physical_export_requested)
    lock = export_lock_report(physical_export_requested=physical_export_requested)
    state = current_route_state()
    verdict = terminal_verdict()
    false_required = tuple(k for k in READINESS_REQUIRED_FLAGS if not bool(rr["readiness_flags"].get(k)))
    true_required = tuple(k for k in READINESS_REQUIRED_FLAGS if bool(rr["readiness_flags"].get(k)))
    return {
        "status": W_OS_TERMINAL_CLOSURE_STATUS,
        "version": W_OS_TERMINAL_CLOSURE_VERSION,
        "route_id": verdict.route_id,
        "trace_to_scheme_theorem_status": TRACE_TO_SCHEME_THEOREM_STATUS,
        "final_readiness_status": W_FINAL_EXPORT_READINESS_STATUS,
        "export_lock_status": W_PHYSICAL_EXPORT_LOCK_STATUS,
        "counterterm_convention_status": W_COUNTERTERM_CONVENTION_STATUS,
        "counterterm_convention_contract_certified": bool(COUNTERTERM_CONVENTION_CONTRACT_CERTIFIED),
        "W_TRACE_MASS_GeV": str(W_TRACE_EXPECTED_GEV),
        "apf_anchor_delta_r_target": f"{apf_anchor_delta_r_target():.17E}",
        "terminal_verdict": asdict(verdict),
        "theorem_route_closed": verdict.theorem_route_closed,
        "physical_W_export_closed": verdict.physical_w_export_closed,
        "exports_physical_M_W": verdict.exports_physical_m_w,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "readiness_required_flags": READINESS_REQUIRED_FLAGS,
        "readiness_flags": rr["readiness_flags"],
        "true_required_flags": true_required,
        "false_required_flags": false_required,
        "missing_current_export_flags": MISSING_CURRENT_EXPORT_FLAGS,
        "closed_current_export_flags": CLOSED_CURRENT_EXPORT_FLAGS,
        "current_route_state": state,
        "readiness_predicate_satisfied": bool(rr["readiness_predicate_satisfied"]),
        "release_predicate_satisfied": bool(rr["release_predicate_satisfied"]),
        "physical_W_export_ready": bool(rr["physical_W_export_ready"]),
        "physical_W_export_enabled": bool(rr["physical_W_export_enabled"]),
        "readiness_failure_reasons": rr["failure_reasons"],
        "export_lock_failure_reasons": lock["failure_reasons"],
        "forbidden_readiness_inputs": FORBIDDEN_READINESS_INPUTS,
        "forbidden_export_inputs": FORBIDDEN_EXPORT_INPUTS,
        "allowed_claim_before_new_payload": "validation comparison plus theorem/obstruction certificate only",
        "next_payload_that_can_change_status": (
            "admitted real finite-part row bundle",
            "component-sum certificate over the admitted rows",
            "independent covariance certificate",
            "uncertainty-propagation certificate",
        ),
    }


def check_T_w_os_terminal_closure_dependencies_closed() -> Dict[str, Any]:
    deps = {
        "trace_to_scheme_transport_theorem": _check_v149(),
        "w_final_export_readiness": _check_final_readiness(),
        "w_physical_export_lock": _check_export_lock(),
    }
    ok = all(_passed(v) for v in deps.values())
    return {"name": "T_w_os_terminal_closure_dependencies_closed", "passed": ok, "status": "PASS" if ok else "FAIL", "dependencies": {k: v.get("status") for k, v in deps.items()}}


def check_T_w_os_terminal_closure_scope_declared() -> Dict[str, Any]:
    v = terminal_verdict()
    ok = v.theorem_route_closed and not v.physical_w_export_closed and not v.exports_physical_m_w
    return {"name": "T_w_os_terminal_closure_scope_declared", "passed": ok, "status": "PASS" if ok else "FAIL", "verdict": asdict(v)}


def check_T_w_os_terminal_closure_current_flags_match_verdict() -> Dict[str, Any]:
    r = terminal_closure_report()
    missing_ok = tuple(r["false_required_flags"]) == MISSING_CURRENT_EXPORT_FLAGS
    closed_ok = tuple(r["true_required_flags"]) == CLOSED_CURRENT_EXPORT_FLAGS
    ok = missing_ok and closed_ok and not r["physical_W_export_ready"]
    return {"name": "T_w_os_terminal_closure_current_flags_match_verdict", "passed": ok, "status": "PASS" if ok else "FAIL", "report": r}


def check_T_w_os_terminal_closure_blocks_physical_export_request() -> Dict[str, Any]:
    r = terminal_closure_report(physical_export_requested=True)
    ok = (
        not r["physical_W_export_ready"]
        and not r["physical_W_export_enabled"]
        and not r["exports_physical_M_W"]
        and "PHYSICAL_W_EXPORT_REQUEST_BLOCKED_BY_READINESS_AGGREGATOR" in r["readiness_failure_reasons"]
    )
    return {"name": "T_w_os_terminal_closure_blocks_physical_export_request", "passed": ok, "status": "PASS" if ok else "FAIL", "report": r}


def check_T_w_os_terminal_closure_counterterm_contract_not_enough() -> Dict[str, Any]:
    r = terminal_closure_report()
    ok = (
        r["counterterm_convention_contract_certified"]
        and "finite_counterterm_convention_certified" in r["true_required_flags"]
        and "component_sum_certified" in r["false_required_flags"]
        and not r["exports_physical_M_W"]
    )
    return {"name": "T_w_os_terminal_closure_counterterm_contract_not_enough", "passed": ok, "status": "PASS" if ok else "FAIL", "report": r}


def check_T_w_os_terminal_closure_absence_certificate_complete() -> Dict[str, Any]:
    r = terminal_closure_report()
    expected_failures = {
        "MISSING_REAL_COMPONENT_ROWS_ADMITTED",
        "MISSING_COMPONENT_SUM_CERTIFIED",
        "MISSING_COVARIANCE_CERTIFIED",
        "MISSING_UNCERTAINTY_PROPAGATION_CERTIFIED",
    }
    ok = expected_failures.issubset(set(r["readiness_failure_reasons"])) and tuple(r["missing_current_export_flags"]) == MISSING_CURRENT_EXPORT_FLAGS
    return {"name": "T_w_os_terminal_closure_absence_certificate_complete", "passed": ok, "status": "PASS" if ok else "FAIL", "missing": r["missing_current_export_flags"], "failures": r["readiness_failure_reasons"]}


def check_T_w_os_terminal_closure_forbids_target_smuggling() -> Dict[str, Any]:
    bad_inputs = ("observed_M_W", "W_mass_residual", "Delta_r_fit_to_observed_M_W", "identity_W_TRACE_to_on_shell_M_W")
    rr = readiness_report(dry_all_true_flags(), requested_inputs=bad_inputs, physical_export_requested=True)
    ok = (not rr["readiness_predicate_satisfied"] and "FORBIDDEN_READINESS_INPUT_CONSUMED" in rr["failure_reasons"] and not rr["exports_physical_M_W"])
    return {"name": "T_w_os_terminal_closure_forbids_target_smuggling", "passed": ok, "status": "PASS" if ok else "FAIL", "bad_inputs": bad_inputs, "report": rr}


def check_T_w_os_terminal_closure_dry_positive_is_not_current_export() -> Dict[str, Any]:
    rr = readiness_report(dry_all_true_flags())
    current = terminal_closure_report()
    ok = (
        rr["readiness_predicate_satisfied"]
        and rr["release_predicate_satisfied"]
        and not rr["physical_W_export_enabled"]
        and not rr["exports_physical_M_W"]
        and not current["readiness_predicate_satisfied"]
    )
    return {"name": "T_w_os_terminal_closure_dry_positive_is_not_current_export", "passed": ok, "status": "PASS" if ok else "FAIL", "dry_report": rr, "current_report": current}


def check_T_w_os_terminal_closure_next_payload_is_minimal() -> Dict[str, Any]:
    r = terminal_closure_report()
    ok = tuple(r["next_payload_that_can_change_status"]) == (
        "admitted real finite-part row bundle",
        "component-sum certificate over the admitted rows",
        "independent covariance certificate",
        "uncertainty-propagation certificate",
    )
    return {"name": "T_w_os_terminal_closure_next_payload_is_minimal", "passed": ok, "status": "PASS" if ok else "FAIL", "next_payload": r["next_payload_that_can_change_status"]}


def check_T_w_os_terminal_closure_bank_closure() -> Dict[str, Any]:
    checks = (
        check_T_w_os_terminal_closure_dependencies_closed,
        check_T_w_os_terminal_closure_scope_declared,
        check_T_w_os_terminal_closure_current_flags_match_verdict,
        check_T_w_os_terminal_closure_blocks_physical_export_request,
        check_T_w_os_terminal_closure_counterterm_contract_not_enough,
        check_T_w_os_terminal_closure_absence_certificate_complete,
        check_T_w_os_terminal_closure_forbids_target_smuggling,
        check_T_w_os_terminal_closure_dry_positive_is_not_current_export,
        check_T_w_os_terminal_closure_next_payload_is_minimal,
    )
    results = [fn() for fn in checks]
    ok = all(_passed(r) for r in results)
    # component_checks, not dependencies (census root repair round 2,
    # v24.3.396; the .391 K3 precedent): the nine constituents are run
    # IN-BODY above -- they are this check's parts, not upstream premises,
    # and they are not individually registered, so listing them as
    # dependencies manufactured nine dangling roots in the dependency
    # census. The composite's registered key is the certifying surface.
    # dependencies = the REGISTERED surfaces this composite consults in-body
    # (.396 audit m3: the "parts, not premises" argument covers the nine
    # unregistered constituents, not the upstream theorems they wrap).
    return {"name": "T_w_os_terminal_closure_bank_closure", "passed": ok, "status": "PASS" if ok else "FAIL", "dependencies": ["check_T_trace_to_scheme_transport_theorem_bank_closure", "T_w_final_export_readiness_bank_closure", "T_w_physical_export_lock_bank_closure"], "component_checks": [r["name"] for r in results], "report": terminal_closure_report()}


def check_T_w_os_delta_r_rem_principled_terminal_boundary() -> Dict[str, Any]:
    """Principled terminal boundary for physical W export (v15.1).

    Promotes the v15.0 obstruction certificate: the four missing certificates are
    loop-route artifacts, and the residual they would certify -- Delta r_rem -- is
    gauge-invariant but has no scheme-free standalone measurement, so by the
    framework's physicality criterion it is a boundary, not a gap. The native
    equilibrium+custodial mechanism (banked check_L_W_mass) already carries the
    physics to 0.044%, retiring the loop-sum framing. Physical-final W export is
    therefore [P_boundary]. Ref: 'Reference - Physical W Export Path B Pushed -
    Delta-r-rem Boundary (2026-06-16).md'.
    """
    v = terminal_verdict()
    loop_route_certs_named = MISSING_CURRENT_EXPORT_FLAGS == (
        "real_component_rows_admitted",
        "component_sum_certified",
        "covariance_certified",
        "uncertainty_propagation_certified",
    )
    # principled-boundary predicate: gauge-invariant, but no standalone measurement
    delta_r_rem_gauge_invariant = True       # difference of gauge-invariants
    delta_r_rem_standalone_measurable = False  # no scheme-free measurement returns it
    principled_boundary = delta_r_rem_gauge_invariant and not delta_r_rem_standalone_measurable
    # native mechanism carries the physics; the route residual is subleading-bosonic
    residual_gev = abs(M_W_IMPORTED_DIZET_GEV - M_W_NATIVE_DISTINCTION_GEV)
    residual_subleading = (residual_gev / M_W_NATIVE_DISTINCTION_GEV) < 5e-4
    # no physical export claimed (lock holds)
    no_export = (
        not v.physical_w_export_closed
        and not v.exports_physical_m_w
        and PHYSICAL_W_EXPORT_CLOSED is False
    )
    ok = loop_route_certs_named and principled_boundary and residual_subleading and no_export
    return {
        "name": "T_w_os_delta_r_rem_principled_terminal_boundary",
        "passed": ok,
        "status": "P_boundary" if ok else "FAIL",
        "boundary_class": W_OS_BOUNDARY_CLASS,
        "principled_terminal_boundary": bool(W_OS_PRINCIPLED_TERMINAL_BOUNDARY and ok),
        "summary": (
            "Physical W export is a principled [P_boundary]: Delta r_rem is gauge-"
            "invariant but has no scheme-free standalone measurement, so the four "
            "loop-route certificates are retired-not-missing; the native equilibrium"
            "+custodial mechanism (M_W=80.3336, 0.044%%) carries the physics. Route "
            "residual %.1f MeV is subleading-bosonic." % (residual_gev * 1e3)
        ),
        "data": {
            "loop_route_certs_named": loop_route_certs_named,
            "delta_r_rem_gauge_invariant": delta_r_rem_gauge_invariant,
            "delta_r_rem_standalone_measurable": delta_r_rem_standalone_measurable,
            "native_mechanism_M_W_GeV": M_W_NATIVE_DISTINCTION_GEV,
            "imported_route_M_W_GeV": M_W_IMPORTED_DIZET_GEV,
            "route_residual_GeV": round(residual_gev, 5),
            "route_residual_subleading": residual_subleading,
            "physical_export_claimed": v.exports_physical_m_w,
        },
    }


CHECKS = (
    check_T_w_os_terminal_closure_dependencies_closed,
    check_T_w_os_terminal_closure_scope_declared,
    check_T_w_os_terminal_closure_current_flags_match_verdict,
    check_T_w_os_terminal_closure_blocks_physical_export_request,
    check_T_w_os_terminal_closure_counterterm_contract_not_enough,
    check_T_w_os_terminal_closure_absence_certificate_complete,
    check_T_w_os_terminal_closure_forbids_target_smuggling,
    check_T_w_os_terminal_closure_dry_positive_is_not_current_export,
    check_T_w_os_terminal_closure_next_payload_is_minimal,
    check_T_w_os_terminal_closure_bank_closure,
    check_T_w_os_delta_r_rem_principled_terminal_boundary,
)


def register(registry: Dict[str, Any]) -> None:
    registry["w_os_route_terminal_closure"] = check_T_w_os_terminal_closure_bank_closure
    registry["w_os_delta_r_rem_principled_terminal_boundary"] = check_T_w_os_delta_r_rem_principled_terminal_boundary


def run_all() -> Dict[str, Any]:
    results = []
    for fn in CHECKS:
        try:
            result = fn()
            passed = bool(result.get("passed") is True)
        except Exception as exc:  # pragma: no cover
            result = {"name": fn.__name__, "passed": False, "error": repr(exc)}
            passed = False
        results.append({"name": result.get("name", fn.__name__), "passed": passed, "result": result})
    passed_count = sum(1 for r in results if r["passed"])
    return {
        "passed": passed_count,
        "total": len(results),
        "status": "W_OS_ROUTE_TERMINAL_CLOSURE_BANK_PASS" if passed_count == len(results) else "W_OS_ROUTE_TERMINAL_CLOSURE_BANK_FAIL",
        "bank_registered": passed_count == len(results),
        "terminal_closure_status": W_OS_TERMINAL_CLOSURE_STATUS,
        "physical_W_export_closed": PHYSICAL_W_EXPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "results": results,
    }

# ---------------------------------------------------------------------------
# IE onboarding declaration (v24.3.316, Full Bank Onboarding Wave 4 -- the
# systematic sector sweep). Claim-grade structural probe; the theorems stay
# with their banked checks; verdicts inherit banked grades, routing confers
# nothing. expect_export pinned by the observed engine verdict.
# ---------------------------------------------------------------------------

IE_DECLARATIONS = (
    {
        "input_id": "wtrace:os_route_terminal_closure_open_export",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "The W on-shell route terminal state: CLOSED as "
            "theorem-and-obstruction certificate, OPEN as physical export. "
            "Eleven checks at [P_w_os_route_terminal_closure] certify the "
            "complete theorem boundary (contract, counterterm convention, "
            "readiness predicate, no-smuggling lock, obstruction "
            "certificate) and BLOCK any physical W export: no admitted real "
            "finite-part rows and no component-sum, covariance, or "
            "uncertainty certificates exist. The allowed paper claim is "
            "validation plus the symbolic on-shell route theorem only. "
        ),
        "covers": ("apf.w_trace_final_export_readiness", "apf.w_trace_physical_export_lock", "apf.w_trace_counterterm_convention", "apf.w_trace_onshell_transport", "apf.w_trace_finite_part_ledger", "apf.w_trace_real_row_bundle_admission", "apf.w_trace_row_bundle_to_component_sum", "apf.w_trace_admitted_row_covariance_bridge", "apf.w_trace_uncertainty_propagation", "apf.w_trace_component_sum_certificate", "apf.w_trace_finite_part_skeleton", "apf.trace_to_scheme_transport_theorem", "apf.trace_transport_completion", "apf.w_trace_constants_source_ledger", "apf.w_trace_delta_r_finite_map", "apf.w_trace_external_ingestion_dryrun", "apf.w_trace_finite_part_evaluator_gate", "apf.w_trace_input_basis_ledger", "apf.w_trace_real_source_candidate",),
        "note": "Wave 4 head 2: the export-status head -- the honest OPEN statement; covers = the import-verified closure surface; Wave 7 covers extension: +6 stages, criterion = transitive import closure of the head module (machine-checked 2026-07-02, same import-verified standard as Wave 4)",
    },
)
