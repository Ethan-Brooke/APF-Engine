"""W_TRACE Delta_r remainder-resolution sprint.

v15.4 (2026-05-09): source-remainder resolver after the v15.3
component-payload worksheet.  This layer does not invent finite parts.  It
turns the quarantined standard-total remainder into a named acquisition map:
which part of the W on-shell route is already numerically anchored, where the
APF/source residual sits, and which externally reviewed component rows would be
needed before physical export can be reconsidered.

Closed here:
    * dominant-proxy subtotal is reconciled against both the ACFW source total
      and the PDG electroweak-review context total;
    * the APF_TRACE residual after the same dominant proxies is isolated;
    * the source-vs-APF gap is proved to sit entirely in the unresolved
      finite-remainder sector, not in the leading Delta-alpha/top-rho scaffold;
    * named remainder buckets and acquisition requirements are generated.

Still open here:
    physical M_W export.  The remainder buckets are acquisition targets and
    obstruction labels, not numerical APF finite-part rows.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_delta_r_component_payload import (
    APF_DELTA_R_TARGET,
    M_W_TRACE_GEV,
    PDG_DELTA_R_TOTAL_CONTEXT,
    PDG_DELTA_R_TOTAL_ALPHA_SIGMA,
    PDG_DELTA_R_TOTAL_MT_SIGMA,
    NUMERIC_PROXY_COMPONENTS,
    component_payload_report,
    component_payload_rows,
    dominant_delta_alpha_row,
    dominant_rho_row,
    numeric_proxy_subtotal,
    source_proxy_closure_report,
    source_total_remainder_row,
    trace_on_shell_angle_values,
    check_T_w_delta_r_component_payload_bank_closure as _check_v153,
)
from apf.w_trace_delta_r_transport_buildout import (
    source_vs_trace_transport_values,
    transport_sensitivity_at_trace,
    dMW_dDelta_r,
)
from apf.w_trace_finite_part_skeleton import COMPONENT_SYMBOLS
from apf.w_trace_component_sum_certificate import component_sum_certificate_report
from apf.w_trace_uncertainty_propagation import uncertainty_propagation_report
from apf.w_trace_physical_export_lock import export_lock_report

STATUS = "P_w_delta_r_remainder_resolution"
VERSION = "v15_4"
PASS_STATUS = "W_TRACE_DELTA_R_REMAINDER_RESOLUTION_PASS"
TITLE = "W_TRACE Delta_r remainder-resolution worksheet"
PAYLOAD_ID = "W_TRACE_DELTA_R_REMAINDER_RESOLUTION_v15_4"

# The named unresolved finite buckets.  These are deliberately symbolic/open:
# v15.4 classifies the remainder and its acquisition path; it does not assign
# made-up numerical finite parts to the buckets.
REMAINDER_BUCKET_ORDER: Tuple[str, ...] = (
    "fermionic_nonleading_finite_remainder",
    "bosonic_finite_remainder",
    "vertex_box_muon_decay_remainder",
    "on_shell_counterterm_finite_remainder",
    "mixed_higher_order_EW_QCD_remainder",
    "covariance_and_export_uncertainty_remainder",
)

BUCKET_TO_REQUIRED_COMPONENTS: Dict[str, Tuple[str, ...]] = {
    "fermionic_nonleading_finite_remainder": ("fermionic_loop_finite_component",),
    "bosonic_finite_remainder": ("bosonic_loop_finite_component",),
    "vertex_box_muon_decay_remainder": ("vertex_box_finite_component",),
    "on_shell_counterterm_finite_remainder": ("scheme_conversion_counterterm_component",),
    "mixed_higher_order_EW_QCD_remainder": (
        "fermionic_loop_finite_component",
        "bosonic_loop_finite_component",
        "scheme_conversion_counterterm_component",
    ),
    "covariance_and_export_uncertainty_remainder": (
        "correlation_covariance_component",
        "uncertainty_propagation_component",
    ),
}

BUCKET_ROLE: Dict[str, str] = {
    "fermionic_nonleading_finite_remainder": "closed-fermion-loop and nonleading fermionic finite pieces not captured by the Delta-alpha/top-rho source proxies",
    "bosonic_finite_remainder": "pure bosonic electroweak finite terms in the on-shell Delta-r map",
    "vertex_box_muon_decay_remainder": "muon-decay vertex/box finite terms entering the on-shell relation",
    "on_shell_counterterm_finite_remainder": "finite parts of the chosen on-shell counterterm/convention map",
    "mixed_higher_order_EW_QCD_remainder": "mixed higher-order electroweak/QCD corrections included in precision source totals",
    "covariance_and_export_uncertainty_remainder": "covariance, error decomposition, and Delta-r-to-MW export uncertainty not supplied as real rows",
}

EXTERNAL_SOURCE_REQUIREMENTS: Tuple[str, ...] = (
    "reviewed_component_level_finite_part_rows",
    "declared_on_shell_counterterm_convention",
    "component_sum_reproduction_of_declared_total",
    "component_covariance_or_independence_certificate",
    "Delta_r_to_MW_uncertainty_pushforward_certificate",
    "no_observed_W_or_APF_anchor_used_as_fit_input",
)

BLOCKERS: Tuple[str, ...] = (
    "REMAINDER_BUCKETS_SYMBOLIC_ONLY",
    "NO_NUMERICAL_BUCKET_DECOMPOSITION",
    "NO_REVIEWED_COMPONENT_LEVEL_SOURCE_TABLE",
    "NO_COMPONENT_SUM_CERTIFICATE_FOR_REMAINDER",
    "NO_REAL_COVARIANCE_FOR_REMAINDER_BUCKETS",
    "PHYSICAL_EXPORT_STILL_LOCKED",
)

FORBIDDEN_TOKENS: Tuple[str, ...] = (
    "observed_M_W",
    "world_average_M_W",
    "CDF_II_M_W",
    "CMS_observed_M_W",
    "fit_to_observed_W",
    "component_residual_tuned_to_APF_anchor",
    "physical_export_override",
)


@dataclass(frozen=True)
class RemainderBucket:
    bucket_id: str
    role: str
    required_components: Tuple[str, ...]
    numeric_value: None
    uncertainty: None
    unit: str
    source_status: str
    admission_status: str
    promotes_to_component_row: bool = False
    consumes_observed_W: bool = False
    consumes_APF_anchor_as_fit_input: bool = False


@dataclass(frozen=True)
class RemainderIdentity:
    identity_id: str
    value: float
    unit: str
    meaning: str
    status: str


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


def _contains_forbidden_token(obj: Any) -> bool:
    txt = _canonical_json(obj)
    return any(tok in txt for tok in FORBIDDEN_TOKENS)


def proxy_rows_digest() -> str:
    rows = [asdict(dominant_delta_alpha_row()), asdict(dominant_rho_row())]
    return _digest(rows)


def source_total() -> float:
    return float(source_vs_trace_transport_values()["Delta_r_source_total"])


def apf_trace_delta_r() -> float:
    return float(APF_DELTA_R_TARGET)


def source_remainder() -> float:
    return float(source_total_remainder_row().value)


def apf_trace_remainder_after_proxies() -> float:
    return apf_trace_delta_r() - numeric_proxy_subtotal()


def pdg_context_remainder_after_proxies() -> float:
    return float(PDG_DELTA_R_TOTAL_CONTEXT) - numeric_proxy_subtotal()


def source_minus_apf_delta_r_gap() -> float:
    return source_total() - apf_trace_delta_r()


def source_minus_pdg_context_gap() -> float:
    return source_total() - float(PDG_DELTA_R_TOTAL_CONTEXT)


def remainder_gap_identity() -> RemainderIdentity:
    gap = source_remainder() - apf_trace_remainder_after_proxies()
    return RemainderIdentity(
        identity_id="source_remainder_minus_apf_remainder_equals_source_total_minus_apf_trace_total",
        value=gap,
        unit="dimensionless_Delta_r",
        meaning="With the same Delta-alpha and top-rho source proxies subtracted from both sides, the full source/APF Delta-r gap is carried by the unresolved finite-remainder sector.",
        status="IDENTITY_CLOSED_NOT_EXPORT",
    )


def mw_shift_from_delta_r_gap(delta_r_gap: float) -> float:
    jac = float(transport_sensitivity_at_trace()["dM_W_dDelta_r_GeV"])
    return jac * float(delta_r_gap) * 1000.0


def source_apf_gap_mw_shift_mev() -> float:
    return mw_shift_from_delta_r_gap(source_minus_apf_delta_r_gap())


def source_pdg_context_gap_mw_shift_mev() -> float:
    return mw_shift_from_delta_r_gap(source_minus_pdg_context_gap())


def remainder_bucket_rows() -> Tuple[RemainderBucket, ...]:
    rows = []
    for bid in REMAINDER_BUCKET_ORDER:
        rows.append(RemainderBucket(
            bucket_id=bid,
            role=BUCKET_ROLE[bid],
            required_components=BUCKET_TO_REQUIRED_COMPONENTS[bid],
            numeric_value=None,
            uncertainty=None,
            unit="dimensionless_Delta_r_remainder_piece",
            source_status="UNSUPPLIED_REVIEWED_NUMERICAL_BUCKET_ROW",
            admission_status="ACQUISITION_TARGET_ONLY_NOT_ADMITTED_FOR_EXPORT",
        ))
    return tuple(rows)


def remainder_resolution_table() -> Tuple[Dict[str, Any], ...]:
    out = []
    out.append({
        "row_id": "delta_alpha_running_proxy",
        "symbol": COMPONENT_SYMBOLS["delta_alpha_running_component"],
        "value": dominant_delta_alpha_row().value,
        "status": "NUMERIC_SOURCE_PROXY_PRESENT",
        "admission": dominant_delta_alpha_row().admission_status,
    })
    out.append({
        "row_id": "top_rho_oblique_proxy",
        "symbol": COMPONENT_SYMBOLS["delta_rho_oblique_component"],
        "value": dominant_rho_row().value,
        "status": "NUMERIC_SOURCE_PROXY_PRESENT",
        "admission": dominant_rho_row().admission_status,
    })
    out.append({
        "row_id": "proxy_subtotal",
        "symbol": "Delta_r_proxy_subtotal",
        "value": numeric_proxy_subtotal(),
        "status": "DIAGNOSTIC_SUBTOTAL",
        "admission": "NOT_COMPONENT_EXPORT",
    })
    out.append({
        "row_id": "source_total_remainder",
        "symbol": "Delta_r_remainder_source_total",
        "value": source_remainder(),
        "status": "AGGREGATE_REMAINDER_ISOLATED",
        "admission": "NOT_APF_COMPONENT_ROW",
    })
    out.append({
        "row_id": "apf_trace_remainder_after_same_proxies",
        "symbol": "Delta_r_remainder_APF_TRACE",
        "value": apf_trace_remainder_after_proxies(),
        "status": "TRACE_COMPARISON_REMAINDER",
        "admission": "COMPARISON_ONLY_NOT_COMPONENT_INPUT",
    })
    out.append({
        "row_id": "pdg_context_remainder_after_same_proxies",
        "symbol": "Delta_r_remainder_PDG_context",
        "value": pdg_context_remainder_after_proxies(),
        "status": "SOURCE_CONTEXT_CROSSWALK",
        "admission": "CONTEXT_ONLY_NOT_COMPONENT_EXPORT",
    })
    for b in remainder_bucket_rows():
        out.append({
            "row_id": b.bucket_id,
            "symbol": "+".join(COMPONENT_SYMBOLS[c] for c in b.required_components),
            "value": "UNSUPPLIED",
            "status": b.source_status,
            "admission": b.admission_status,
        })
    return tuple(out)


def acquisition_priority() -> Tuple[Dict[str, Any], ...]:
    return (
        {
            "priority": 1,
            "target": "component-level ACFW or equivalent electroweak table",
            "needed_for": "split aggregate remainder into finite fermionic/bosonic/counterterm/higher-order rows",
            "unlocks": "real component-sum attempt",
        },
        {
            "priority": 2,
            "target": "on-shell convention/counterterm finite-part row with sign convention",
            "needed_for": "avoid mixing source notation with APF component signs",
            "unlocks": "counterterm row admission",
        },
        {
            "priority": 3,
            "target": "covariance or independence certificate across component rows",
            "needed_for": "uncertainty propagation to M_W",
            "unlocks": "export uncertainty protocol",
        },
        {
            "priority": 4,
            "target": "no-target-input attestation for all rows",
            "needed_for": "no-smuggling release predicate",
            "unlocks": "physical-export readiness review",
        },
    )


def crosswalk_report() -> Dict[str, Any]:
    src = source_total()
    apf = apf_trace_delta_r()
    pdg = float(PDG_DELTA_R_TOTAL_CONTEXT)
    subtotal = numeric_proxy_subtotal()
    src_rem = source_remainder()
    apf_rem = apf_trace_remainder_after_proxies()
    pdg_rem = pdg_context_remainder_after_proxies()
    gap = source_minus_apf_delta_r_gap()
    identity = remainder_gap_identity()
    jac = float(transport_sensitivity_at_trace()["dM_W_dDelta_r_GeV"])
    return {
        "Delta_r_source_total_ACFW": src,
        "Delta_r_APF_TRACE": apf,
        "Delta_r_PDG_context_total": pdg,
        "numeric_proxy_subtotal": subtotal,
        "source_remainder_after_proxies": src_rem,
        "apf_trace_remainder_after_proxies": apf_rem,
        "pdg_context_remainder_after_proxies": pdg_rem,
        "source_minus_apf_delta_r_gap": gap,
        "source_minus_apf_gap_MW_shift_MeV": source_apf_gap_mw_shift_mev(),
        "source_minus_pdg_context_delta_r_gap": source_minus_pdg_context_gap(),
        "source_minus_pdg_context_gap_MW_shift_MeV": source_pdg_context_gap_mw_shift_mev(),
        "remainder_identity": asdict(identity),
        "remainder_identity_closure_error": identity.value - gap,
        "dM_W_dDelta_r_GeV": jac,
        "absolute_remainder_scale_MeV_if_moved_as_whole": abs(jac * src_rem * 1000.0),
    }


def obstruction_report() -> Dict[str, Any]:
    return {
        "status": STATUS,
        "blockers": BLOCKERS,
        "external_source_requirements": EXTERNAL_SOURCE_REQUIREMENTS,
        "remainder_buckets": tuple(asdict(b) for b in remainder_bucket_rows()),
        "physical_W_export_ready": False,
        "exports_physical_M_W": False,
        "sharp_obstruction": "the source/APF gap is localized to the unresolved finite-remainder sector, but no reviewed numerical bucket decomposition or covariance/export certificate is supplied",
    }


def component_certificate_after_resolution() -> Dict[str, Any]:
    cert = component_sum_certificate_report(
        rows=None,
        rows_admitted=False,
        covariance_supplied=False,
        uncertainty_supplied=False,
        physical_export_requested=False,
    )
    return {
        "component_sum_certified": False,
        "certificate": cert,
        "reason": "v15.4 resolves the acquisition map for the remainder, not numerical APF finite-part rows",
    }


def uncertainty_context_after_resolution() -> Dict[str, Any]:
    # Keep a standard context-only scale from the v15.3 source uncertainties.
    jac = float(transport_sensitivity_at_trace()["dM_W_dDelta_r_GeV"])
    sigma_dr = math.sqrt(float(PDG_DELTA_R_TOTAL_MT_SIGMA) ** 2 + float(PDG_DELTA_R_TOTAL_ALPHA_SIGMA) ** 2)
    return {
        "sigma_delta_r_context_quadrature": sigma_dr,
        "sigma_MW_context_MeV": abs(jac) * sigma_dr * 1000.0,
        "certified_export_uncertainty": False,
        "uncertainty_propagation_report": uncertainty_propagation_report(cov=None, physical_export_requested=False),
    }


def remainder_resolution_report() -> Dict[str, Any]:
    artifact = {
        "status": STATUS,
        "version": VERSION,
        "payload_id": PAYLOAD_ID,
        "title": TITLE,
        "upstream_required": "P_w_delta_r_component_payload_worksheet",
        "proxy_rows_digest": proxy_rows_digest(),
        "trace_on_shell_angle_values": trace_on_shell_angle_values(),
        "source_proxy_closure_upstream": source_proxy_closure_report(),
        "crosswalk": crosswalk_report(),
        "resolution_table": remainder_resolution_table(),
        "remainder_buckets": tuple(asdict(b) for b in remainder_bucket_rows()),
        "acquisition_priority": acquisition_priority(),
        "component_certificate_after_resolution": component_certificate_after_resolution(),
        "uncertainty_context_after_resolution": uncertainty_context_after_resolution(),
        "obstruction_report": obstruction_report(),
        "physical_export_lock": export_lock_report(physical_export_requested=False),
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "claim_boundary": "remainder localized and acquisition map closed; numerical finite-part export remains open",
    }
    artifact["payload_digest"] = _digest(artifact)
    return artifact


def terminal_report() -> Dict[str, Any]:
    return {
        "status": STATUS,
        "version": VERSION,
        "title": TITLE,
        "report": remainder_resolution_report(),
        "verdict": "P_remainder_resolution_plus_P_row_level_acquisition_map__not_physical_export",
    }


# --- Checks -----------------------------------------------------------------

def check_T_w_delta_r_remainder_resolution_status_declared():
    r = remainder_resolution_report()
    return _res("status_declared", r["status"] == STATUS and r["version"] == VERSION and not r["physical_W_export_enabled"])


def check_T_w_delta_r_remainder_resolution_depends_on_v153():
    d = _check_v153()
    return _res("depends_on_v153", _passed(d), upstream=d.get("status"), upstream_check=d.get("check"))


def check_T_w_delta_r_remainder_resolution_proxy_digest_stable():
    d1 = proxy_rows_digest(); d2 = proxy_rows_digest()
    return _res("proxy_digest_stable", d1 == d2 and d1.startswith("sha256:"), digest=d1)


def check_T_w_delta_r_remainder_resolution_bucket_order_declared():
    rows = remainder_bucket_rows()
    ids = tuple(r.bucket_id for r in rows)
    return _res("bucket_order_declared", ids == REMAINDER_BUCKET_ORDER and len(ids) == 6, bucket_ids=ids)


def check_T_w_delta_r_remainder_resolution_bucket_components_known():
    ok = True
    unknown = []
    for b in remainder_bucket_rows():
        for cid in b.required_components:
            if cid not in COMPONENT_SYMBOLS:
                ok = False; unknown.append(cid)
    return _res("bucket_components_known", ok, unknown=tuple(unknown))


def check_T_w_delta_r_remainder_resolution_buckets_symbolic_only():
    rows = remainder_bucket_rows()
    ok = all(r.numeric_value is None and r.uncertainty is None and not r.promotes_to_component_row for r in rows)
    return _res("buckets_symbolic_only", ok, buckets=tuple(asdict(r) for r in rows))


def check_T_w_delta_r_remainder_resolution_source_remainder_matches_upstream():
    upstream = source_proxy_closure_report()["unassigned_remainder"]
    return _res("source_remainder_matches_upstream", abs(source_remainder() - upstream) < 1e-18, source_remainder=source_remainder(), upstream=upstream)


def check_T_w_delta_r_remainder_resolution_apf_remainder_identity():
    lhs = numeric_proxy_subtotal() + apf_trace_remainder_after_proxies()
    return _res("apf_remainder_identity", abs(lhs - apf_trace_delta_r()) < 1e-18, lhs=lhs, apf_trace_delta_r=apf_trace_delta_r())


def check_T_w_delta_r_remainder_resolution_source_remainder_identity():
    lhs = numeric_proxy_subtotal() + source_remainder()
    return _res("source_remainder_identity", abs(lhs - source_total()) < 1e-18, lhs=lhs, source_total=source_total())


def check_T_w_delta_r_remainder_resolution_gap_localized_to_remainder():
    ident = remainder_gap_identity()
    gap = source_minus_apf_delta_r_gap()
    return _res("gap_localized_to_remainder", abs(ident.value - gap) < 1e-18, identity=asdict(ident), source_gap=gap)


def check_T_w_delta_r_remainder_resolution_gap_maps_to_known_mev_shift():
    mev = source_apf_gap_mw_shift_mev()
    # Sign is negative because increasing Delta_r lowers M_W; magnitude is the v15.2/v15.3 3.485 MeV scale.
    ok = mev < 0 and abs(abs(mev) - 3.484093) < 1e-3
    return _res("gap_maps_to_known_mev_shift", ok, MW_shift_MeV=mev)


def check_T_w_delta_r_remainder_resolution_pdg_context_crosswalk_present():
    rep = crosswalk_report()
    ok = rep["Delta_r_PDG_context_total"] == PDG_DELTA_R_TOTAL_CONTEXT and rep["pdg_context_remainder_after_proxies"] > rep["source_remainder_after_proxies"]
    return _res("pdg_context_crosswalk_present", ok, crosswalk=rep)


def check_T_w_delta_r_remainder_resolution_pdg_source_context_gap_small():
    gap = abs(source_minus_pdg_context_gap())
    return _res("pdg_source_context_gap_small", gap < 3e-4, delta_r_gap=source_minus_pdg_context_gap(), MW_shift_MeV=source_pdg_context_gap_mw_shift_mev())


def check_T_w_delta_r_remainder_resolution_table_contains_proxies_and_buckets():
    table = remainder_resolution_table()
    ids = tuple(r["row_id"] for r in table)
    ok = ids[:2] == ("delta_alpha_running_proxy", "top_rho_oblique_proxy") and all(bid in ids for bid in REMAINDER_BUCKET_ORDER)
    return _res("table_contains_proxies_and_buckets", ok, row_ids=ids)


def check_T_w_delta_r_remainder_resolution_table_has_twelve_rows():
    rows = remainder_resolution_table()
    return _res("table_has_twelve_rows", len(rows) == 12, rows=rows)


def check_T_w_delta_r_remainder_resolution_acquisition_requirements_complete():
    req = EXTERNAL_SOURCE_REQUIREMENTS
    ok = len(req) == 6 and "no_observed_W_or_APF_anchor_used_as_fit_input" in req
    return _res("acquisition_requirements_complete", ok, requirements=req)


def check_T_w_delta_r_remainder_resolution_priority_order_declared():
    pr = acquisition_priority()
    ok = tuple(x["priority"] for x in pr) == (1, 2, 3, 4)
    return _res("priority_order_declared", ok, priority=pr)


def check_T_w_delta_r_remainder_resolution_no_forbidden_tokens():
    safe = {
        "table": remainder_resolution_table(),
        "buckets": tuple(asdict(b) for b in remainder_bucket_rows()),
        "priority": acquisition_priority(),
    }
    return _res("no_forbidden_tokens", not _contains_forbidden_token(safe))


def check_T_w_delta_r_remainder_resolution_no_bucket_consumes_observed_w():
    rows = remainder_bucket_rows()
    ok = all(not r.consumes_observed_W for r in rows)
    return _res("no_bucket_consumes_observed_w", ok)


def check_T_w_delta_r_remainder_resolution_no_bucket_consumes_apf_anchor_as_fit_input():
    rows = remainder_bucket_rows()
    ok = all(not r.consumes_APF_anchor_as_fit_input for r in rows)
    return _res("no_bucket_consumes_apf_anchor_as_fit_input", ok)


def check_T_w_delta_r_remainder_resolution_component_certificate_still_blocked():
    cert = component_certificate_after_resolution()["certificate"]
    ok = not cert["component_sum_certified"] and "NO_COMPONENT_ROWS_SUPPLIED" in cert["failure_reasons"]
    return _res("component_certificate_still_blocked", ok, certificate=cert)


def check_T_w_delta_r_remainder_resolution_uncertainty_context_only():
    u = uncertainty_context_after_resolution()
    ok = u["sigma_MW_context_MeV"] > 0 and not u["certified_export_uncertainty"]
    return _res("uncertainty_context_only", ok, uncertainty=u)


def check_T_w_delta_r_remainder_resolution_export_lock_preserved():
    r = remainder_resolution_report()["physical_export_lock"]
    ok = not r.get("physical_W_export_enabled", True) and not r.get("exports_physical_M_W", True)
    return _res("export_lock_preserved", ok, export_lock=r)


def check_T_w_delta_r_remainder_resolution_obstruction_blockers_named():
    obs = obstruction_report()
    ok = tuple(obs["blockers"]) == BLOCKERS and not obs["physical_W_export_ready"]
    return _res("obstruction_blockers_named", ok, obstruction=obs)


def check_T_w_delta_r_remainder_resolution_sensitivity_consistent_with_v152():
    jac1 = float(transport_sensitivity_at_trace()["dM_W_dDelta_r_GeV"])
    jac2 = dMW_dDelta_r(apf_trace_delta_r())
    return _res("sensitivity_consistent_with_v152", abs(jac1 - jac2) < 1e-14 and jac1 < 0, jacobian=jac1)


def check_T_w_delta_r_remainder_resolution_digest_stable():
    d1 = remainder_resolution_report()["payload_digest"]
    d2 = remainder_resolution_report()["payload_digest"]
    return _res("digest_stable", d1 == d2 and d1.startswith("sha256:"), digest=d1)


def check_T_w_delta_r_remainder_resolution_terminal_verdict():
    r = terminal_report()
    ok = r["verdict"] == "P_remainder_resolution_plus_P_row_level_acquisition_map__not_physical_export"
    return _res("terminal_verdict", ok, verdict=r["verdict"])


def check_T_w_delta_r_remainder_resolution_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_delta_r_remainder_resolution_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))


_CHECKS = {
    "check_T_w_delta_r_remainder_resolution_status_declared": check_T_w_delta_r_remainder_resolution_status_declared,
    "check_T_w_delta_r_remainder_resolution_depends_on_v153": check_T_w_delta_r_remainder_resolution_depends_on_v153,
    "check_T_w_delta_r_remainder_resolution_proxy_digest_stable": check_T_w_delta_r_remainder_resolution_proxy_digest_stable,
    "check_T_w_delta_r_remainder_resolution_bucket_order_declared": check_T_w_delta_r_remainder_resolution_bucket_order_declared,
    "check_T_w_delta_r_remainder_resolution_bucket_components_known": check_T_w_delta_r_remainder_resolution_bucket_components_known,
    "check_T_w_delta_r_remainder_resolution_buckets_symbolic_only": check_T_w_delta_r_remainder_resolution_buckets_symbolic_only,
    "check_T_w_delta_r_remainder_resolution_source_remainder_matches_upstream": check_T_w_delta_r_remainder_resolution_source_remainder_matches_upstream,
    "check_T_w_delta_r_remainder_resolution_apf_remainder_identity": check_T_w_delta_r_remainder_resolution_apf_remainder_identity,
    "check_T_w_delta_r_remainder_resolution_source_remainder_identity": check_T_w_delta_r_remainder_resolution_source_remainder_identity,
    "check_T_w_delta_r_remainder_resolution_gap_localized_to_remainder": check_T_w_delta_r_remainder_resolution_gap_localized_to_remainder,
    "check_T_w_delta_r_remainder_resolution_gap_maps_to_known_mev_shift": check_T_w_delta_r_remainder_resolution_gap_maps_to_known_mev_shift,
    "check_T_w_delta_r_remainder_resolution_pdg_context_crosswalk_present": check_T_w_delta_r_remainder_resolution_pdg_context_crosswalk_present,
    "check_T_w_delta_r_remainder_resolution_pdg_source_context_gap_small": check_T_w_delta_r_remainder_resolution_pdg_source_context_gap_small,
    "check_T_w_delta_r_remainder_resolution_table_contains_proxies_and_buckets": check_T_w_delta_r_remainder_resolution_table_contains_proxies_and_buckets,
    "check_T_w_delta_r_remainder_resolution_table_has_twelve_rows": check_T_w_delta_r_remainder_resolution_table_has_twelve_rows,
    "check_T_w_delta_r_remainder_resolution_acquisition_requirements_complete": check_T_w_delta_r_remainder_resolution_acquisition_requirements_complete,
    "check_T_w_delta_r_remainder_resolution_priority_order_declared": check_T_w_delta_r_remainder_resolution_priority_order_declared,
    "check_T_w_delta_r_remainder_resolution_no_forbidden_tokens": check_T_w_delta_r_remainder_resolution_no_forbidden_tokens,
    "check_T_w_delta_r_remainder_resolution_no_bucket_consumes_observed_w": check_T_w_delta_r_remainder_resolution_no_bucket_consumes_observed_w,
    "check_T_w_delta_r_remainder_resolution_no_bucket_consumes_apf_anchor_as_fit_input": check_T_w_delta_r_remainder_resolution_no_bucket_consumes_apf_anchor_as_fit_input,
    "check_T_w_delta_r_remainder_resolution_component_certificate_still_blocked": check_T_w_delta_r_remainder_resolution_component_certificate_still_blocked,
    "check_T_w_delta_r_remainder_resolution_uncertainty_context_only": check_T_w_delta_r_remainder_resolution_uncertainty_context_only,
    "check_T_w_delta_r_remainder_resolution_export_lock_preserved": check_T_w_delta_r_remainder_resolution_export_lock_preserved,
    "check_T_w_delta_r_remainder_resolution_obstruction_blockers_named": check_T_w_delta_r_remainder_resolution_obstruction_blockers_named,
    "check_T_w_delta_r_remainder_resolution_sensitivity_consistent_with_v152": check_T_w_delta_r_remainder_resolution_sensitivity_consistent_with_v152,
    "check_T_w_delta_r_remainder_resolution_digest_stable": check_T_w_delta_r_remainder_resolution_digest_stable,
    "check_T_w_delta_r_remainder_resolution_terminal_verdict": check_T_w_delta_r_remainder_resolution_terminal_verdict,
    "check_T_w_delta_r_remainder_resolution_bank_closure": check_T_w_delta_r_remainder_resolution_bank_closure,
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
    cw = out["report"]["report"]["crosswalk"]
    print("source_remainder_after_proxies", f"{cw['source_remainder_after_proxies']:.12f}")
    print("apf_trace_remainder_after_proxies", f"{cw['apf_trace_remainder_after_proxies']:.12f}")
    print("source_minus_apf_gap_MW_shift_MeV", f"{cw['source_minus_apf_gap_MW_shift_MeV']:.6f}")
    raise SystemExit(0 if out["passed"] else 1)
