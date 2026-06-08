"""W_TRACE same-input evaluator terminal closeout.

v15.8 (2026-05-09): closes the W on-shell route at the honest
literature/evaluator boundary.  v15.7 already evaluated the ACFW Table-1 row
shape at the APF route input point with covariance propagation, but deliberately
kept the physical-export lock because that transfer is a model worksheet rather
than a reviewed per-row same-input electroweak evaluator.  This module audits
candidate evaluator/source families and certifies the terminal route state.

Closed here:
    * the same-input route-input worksheet and covariance propagation from
      v15.7 are accepted as model-limited, reproducible APF-route evaluation;
    * reviewed source families are classified by what they actually provide
      (total parametrization, source-local rows, implementation, or formal
      component machinery);
    * every candidate fails the exact export gate for a named reason;
    * the W route is terminally closed as a publication-safe APF_TRACE result,
      a model-limited same-input worksheet, and a named physical-export
      obstruction.

Still open here:
    physical M_W export.  The first failed gate is a reviewed per-row same-input
    evaluator that returns Delta-r component rows at the APF route input point
    with row covariance and counterterm provenance.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.w_trace_delta_r_route_input_evaluation import (
    APF_DELTA_R_TARGET,
    M_W_TRACE_GEV,
    ROW_ORDER,
    covariance_summary,
    export_boundary_report as v157_export_boundary_report,
    route_input_evaluation_report,
    route_input_point,
    terminal_report as v157_terminal_report,
    transport_error_budget,
    transferred_rows,
    check_T_w_delta_r_route_input_evaluation_bank_closure as _check_v157,
)
from apf.w_trace_delta_r_transport_buildout import mw_from_delta_r
from apf.w_trace_final_export_readiness import readiness_report
from apf.w_trace_physical_export_lock import export_lock_report

STATUS = "P_w_same_input_evaluator_terminal_closeout"
VERSION = "v15_8"
PASS_STATUS = "W_TRACE_SAME_INPUT_EVALUATOR_TERMINAL_CLOSEOUT_PASS"
TITLE = "W_TRACE same-input evaluator terminal closeout"
PAYLOAD_ID = "W_TRACE_SAME_INPUT_EVALUATOR_TERMINAL_CLOSEOUT_v15_8"

FIRST_FAILED_GATE = "REVIEWED_PER_ROW_SAME_INPUT_EVALUATOR_WITH_COVARIANCE"
TERMINAL_ROUTE_STATUS = "P_terminal_route_closeout_not_physical_export"
MODEL_LIMITED_STATUS = "P_model_limited_same_input_evaluation_plus_covariance"
PHYSICAL_EXPORT_STATUS = "OPEN_BLOCKED"

REQUIRED_EVALUATOR_CAPABILITIES: Tuple[str, ...] = (
    "same_input_rows_at_APF_route_point",
    "rowwise_Delta_r_finite_parts",
    "counterterm_convention_provenance",
    "row_covariance_or_uncertainty_protocol",
    "component_sum_equals_declared_total",
    "no_observed_MW_or_inverse_fit_input",
    "reviewed_source_or_reproducible_code_reference",
)

FORBIDDEN_TOKENS: Tuple[str, ...] = (
    "observed_M_W", "world_average_M_W", "CDF_II_M_W", "CMS_observed_M_W",
    "fit_to_observed_W", "manual_export_override", "physical_export_unlock",
    "claim_physical_M_W_export", "reviewed_rows_admitted_without_evaluator",
)

@dataclass(frozen=True)
class EvaluatorCandidate:
    candidate_id: str
    source_family: str
    source_type: str
    provides_total_evaluator: bool
    provides_source_local_rows: bool
    provides_same_input_row_evaluator: bool
    provides_row_covariance: bool
    reviewed_or_standard: bool
    allowed_role: str
    failed_gate: str
    verdict: str
    notes: str

@dataclass(frozen=True)
class CloseoutGate:
    gate_id: str
    requirement: str
    satisfied: bool
    evidence: str
    closeout_action: str

@dataclass(frozen=True)
class TerminalCloseoutRow:
    layer: str
    status: str
    closed: bool
    physical_export_ready: bool
    claim_language: str


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
    text = _canonical_json(obj)
    return any(tok in text for tok in FORBIDDEN_TOKENS)


def evaluator_candidates() -> Tuple[EvaluatorCandidate, ...]:
    """Candidate same-input evaluators/source families audited in v15.8.

    These are not external web calls; they encode the literature/source roles
    already banked in v15.5-v15.7 plus the final evaluator-use decision.
    """
    return (
        EvaluatorCandidate(
            candidate_id="ACFW_2004_MW_PARAMETRIZATION",
            source_family="Awramik-Czakon-Freitas-Weiglein precision SM W-mass parametrization",
            source_type="reviewed total M_W / Delta-r source evaluator",
            provides_total_evaluator=True,
            provides_source_local_rows=True,
            provides_same_input_row_evaluator=False,
            provides_row_covariance=False,
            reviewed_or_standard=True,
            allowed_role="standard-total benchmark and source-local Table-1 row shape",
            failed_gate=FIRST_FAILED_GATE,
            verdict="REJECT_FOR_PHYSICAL_EXPORT__ADMIT_FOR_TOTAL_AND_SOURCE_LOCAL_ROWS",
            notes="ACFW gives a high-precision total parametrization and a component table at its fixed source point, but not reviewed arbitrary-input per-row Delta-r evaluators with covariance.",
        ),
        EvaluatorCandidate(
            candidate_id="FREITAS_HOLLIK_WALTER_WEIGLEIN_FERMIONIC_TWO_LOOP",
            source_family="complete fermionic two-loop MW-MZ interdependence papers",
            source_type="reviewed fermionic two-loop calculation / parametrization family",
            provides_total_evaluator=True,
            provides_source_local_rows=False,
            provides_same_input_row_evaluator=False,
            provides_row_covariance=False,
            reviewed_or_standard=True,
            allowed_role="fermionic two-loop source authority and comparison scaffold",
            failed_gate=FIRST_FAILED_GATE,
            verdict="REJECT_FOR_PHYSICAL_EXPORT__ADMIT_FOR_SOURCE_AUTHORITY",
            notes="The papers provide exact fermionic two-loop results and parametrizations/uncertainty context, but not an APF-route row table with covariance split into the required finite-part slots.",
        ),
        EvaluatorCandidate(
            candidate_id="BOSONIC_TWO_LOOP_DELTA_R_SOURCE",
            source_family="bosonic two-loop Delta-r source family",
            source_type="reviewed bosonic two-loop component source",
            provides_total_evaluator=False,
            provides_source_local_rows=False,
            provides_same_input_row_evaluator=False,
            provides_row_covariance=False,
            reviewed_or_standard=True,
            allowed_role="bosonic finite-remainder source authority",
            failed_gate=FIRST_FAILED_GATE,
            verdict="REJECT_FOR_PHYSICAL_EXPORT__ADMIT_FOR_BUCKET_PROVENANCE",
            notes="The source family identifies the bosonic correction sector but does not by itself supply the full APF-route same-input row evaluator/covariance bundle.",
        ),
        EvaluatorCandidate(
            candidate_id="GFITTER_SM_IMPLEMENTATION",
            source_family="Gfitter Standard Model electroweak implementation",
            source_type="standard total-observable fit implementation",
            provides_total_evaluator=True,
            provides_source_local_rows=False,
            provides_same_input_row_evaluator=False,
            provides_row_covariance=False,
            reviewed_or_standard=True,
            allowed_role="external total-prediction cross-check context",
            failed_gate=FIRST_FAILED_GATE,
            verdict="REJECT_FOR_PHYSICAL_EXPORT__ADMIT_FOR_TOTAL_CONTEXT",
            notes="Gfitter implements the ACFW-style full two-loop plus known higher-order W-mass prediction, but does not expose the APF-required reviewed per-row Delta-r finite-part covariance ledger.",
        ),
        EvaluatorCandidate(
            candidate_id="FEYNHIGGS_MW_OBSERVABLE_CONTEXT",
            source_family="FeynHiggs electroweak observable machinery",
            source_type="public phenomenology code context",
            provides_total_evaluator=True,
            provides_source_local_rows=False,
            provides_same_input_row_evaluator=False,
            provides_row_covariance=False,
            reviewed_or_standard=True,
            allowed_role="code/tool context only",
            failed_gate=FIRST_FAILED_GATE,
            verdict="REJECT_FOR_PHYSICAL_EXPORT__ADMIT_FOR_TOOL_CONTEXT",
            notes="Useful evidence that public EW-observable machinery exists; not a reviewed SM Delta-r row evaluator tailored to the APF on-shell route contract.",
        ),
    )


def evaluator_audit_summary() -> Dict[str, Any]:
    rows = evaluator_candidates()
    exact = [c for c in rows if c.provides_same_input_row_evaluator and c.provides_row_covariance]
    total_context = [c.candidate_id for c in rows if c.provides_total_evaluator]
    source_local = [c.candidate_id for c in rows if c.provides_source_local_rows]
    return {
        "required_capabilities": REQUIRED_EVALUATOR_CAPABILITIES,
        "candidate_count": len(rows),
        "candidates": tuple(asdict(c) for c in rows),
        "total_evaluator_contexts": tuple(total_context),
        "source_local_row_sources": tuple(source_local),
        "exact_same_input_evaluators": tuple(c.candidate_id for c in exact),
        "exact_evaluator_found": bool(exact),
        "first_failed_gate": FIRST_FAILED_GATE,
        "audit_verdict": "NO_REVIEWED_PER_ROW_SAME_INPUT_EVALUATOR_FOUND",
    }


def closeout_gates() -> Tuple[CloseoutGate, ...]:
    r157 = route_input_evaluation_report()
    audit = evaluator_audit_summary()
    return (
        CloseoutGate("G1", "APF route input point declared", True, r157["route_input_point"]["point_id"], "retain from v15.7"),
        CloseoutGate("G2", "source-local reviewed rows extracted", True, "ACFW Table-1 rows extracted in v15.6", "retain as source-local rows"),
        CloseoutGate("G3", "same-input model transfer evaluated", True, "v15.7 APF-target transferred rows sum to APF trace Delta-r", "admit as model-limited worksheet"),
        CloseoutGate("G4", "covariance propagation performed", True, "rank-one and diagonal reference covariance worksheets in v15.7", "admit as uncertainty worksheet"),
        CloseoutGate("G5", "reviewed per-row same-input evaluator located", False, audit["audit_verdict"], "terminal blocker"),
        CloseoutGate("G6", "row covariance supplied by reviewed evaluator", False, "no candidate exposes APF-route row covariance", "terminal blocker"),
        CloseoutGate("G7", "physical export enabled", False, "physical export lock preserved", "keep locked"),
    )


def terminal_closeout_rows() -> Tuple[TerminalCloseoutRow, ...]:
    return (
        TerminalCloseoutRow(
            layer="APF_TRACE W value",
            status="P_local_trace_value",
            closed=True,
            physical_export_ready=False,
            claim_language="APF_TRACE anchor value; not an on-shell physical export by itself.",
        ),
        TerminalCloseoutRow(
            layer="publication validation",
            status="P_validation",
            closed=True,
            physical_export_ready=False,
            claim_language="Comparison to the standard electroweak prediction neighborhood; validation comparison only.",
        ),
        TerminalCloseoutRow(
            layer="trace-to-scheme theorem",
            status="P_theorem",
            closed=True,
            physical_export_ready=False,
            claim_language="Necessary and sufficient export gates stated and checked.",
        ),
        TerminalCloseoutRow(
            layer="source-local row extraction",
            status="P_reviewed_source_local_rows",
            closed=True,
            physical_export_ready=False,
            claim_language="ACFW component rows extracted at their source input point.",
        ),
        TerminalCloseoutRow(
            layer="APF same-input evaluation",
            status=MODEL_LIMITED_STATUS,
            closed=True,
            physical_export_ready=False,
            claim_language="Model-limited row-shape transfer to APF route inputs with covariance propagation.",
        ),
        TerminalCloseoutRow(
            layer="physical W export",
            status=PHYSICAL_EXPORT_STATUS,
            closed=False,
            physical_export_ready=False,
            claim_language="Blocked until a reviewed same-input per-row evaluator with covariance exists.",
        ),
    )


def terminal_numerics() -> Dict[str, Any]:
    b = transport_error_budget()
    p = route_input_point()
    sig = covariance_summary("APF_TRACE_TARGET_TOTAL", "rank_one_correlated_source_theory")
    return {
        "M_W_TRACE_GeV": float(M_W_TRACE_GEV),
        "Delta_r_APF_TRACE": float(APF_DELTA_R_TARGET),
        "M_W_from_APF_Delta_r_GeV": float(mw_from_delta_r(float(APF_DELTA_R_TARGET))),
        "Delta_r_source_total_at_route_inputs": p.Delta_r_source_total_at_route_inputs,
        "M_W_source_total_at_route_inputs_GeV": p.M_W_source_total_at_route_inputs_GeV,
        "Delta_r_source_minus_APF": b["Delta_r_source_minus_APF"],
        "abs_M_W_gap_MeV": b["abs_M_W_gap_MeV"],
        "sigma_delta_r_rank_one": sig.sigma_delta_r,
        "sigma_MW_MeV_rank_one": sig.sigma_MW_MeV,
        "pull_source_minus_APF_sigma": b["pull_source_minus_apf_in_sigma"],
        "row_count": len(ROW_ORDER),
    }


def terminal_publication_claim() -> Dict[str, Any]:
    n = terminal_numerics()
    return {
        "allowed_boxed_claim": (
            "The W on-shell trace-to-scheme route is terminally closed at the current literature boundary: "
            "APF supplies a local trace value and a reproducible same-input Delta-r worksheet with covariance propagation, "
            "but physical W export remains blocked by the absence of a reviewed per-row same-input evaluator."
        ),
        "forbidden_claim": "APF has produced a final physical on-shell W mass prediction.",
        "route_status": TERMINAL_ROUTE_STATUS,
        "model_limited_status": MODEL_LIMITED_STATUS,
        "physical_export_status": PHYSICAL_EXPORT_STATUS,
        "first_failed_gate": FIRST_FAILED_GATE,
        "numeric_summary": n,
    }


def terminal_export_lock_report() -> Dict[str, Any]:
    lock = export_lock_report(physical_export_requested=False)
    ready = readiness_report(physical_export_requested=False)
    return {
        "physical_export_requested": False,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "physical_W_export_ready": False,
        "export_lock_report": lock,
        "final_readiness_report": ready,
        "first_failed_gate": FIRST_FAILED_GATE,
        "remaining_action_to_unlock": "supply reviewed same-input Delta-r row evaluator plus covariance/counterterm provenance, then rerun export-gate theorem",
    }


def closeout_report() -> Dict[str, Any]:
    artifact = {
        "status": STATUS,
        "version": VERSION,
        "payload_id": PAYLOAD_ID,
        "title": TITLE,
        "upstream_required": "P_w_delta_r_route_input_evaluation",
        "upstream_v157_verdict": v157_terminal_report()["verdict"],
        "route_input_point": asdict(route_input_point()),
        "terminal_numerics": terminal_numerics(),
        "transferred_rows_apf_trace_target": tuple(asdict(r) for r in transferred_rows("APF_TRACE_TARGET_TOTAL")),
        "covariance_summary_rank_one": asdict(covariance_summary("APF_TRACE_TARGET_TOTAL", "rank_one_correlated_source_theory")),
        "evaluator_audit": evaluator_audit_summary(),
        "closeout_gates": tuple(asdict(g) for g in closeout_gates()),
        "terminal_closeout_ladder": tuple(asdict(r) for r in terminal_closeout_rows()),
        "publication_claim": terminal_publication_claim(),
        "export_lock": terminal_export_lock_report(),
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "terminal_verdict": "P_terminal_W_route_closeout__model_limited_same_input_evaluation__not_physical_export",
    }
    artifact["payload_digest"] = _digest(artifact)
    return artifact


def terminal_report() -> Dict[str, Any]:
    return {
        "status": STATUS,
        "version": VERSION,
        "title": TITLE,
        "report": closeout_report(),
        "verdict": closeout_report()["terminal_verdict"],
    }

# --- checks -----------------------------------------------------------------

def check_T_w_same_input_evaluator_closeout_status_declared():
    r = closeout_report()
    return _res("status_declared", r["status"] == STATUS and r["version"] == VERSION and not r["physical_W_export_enabled"])


def check_T_w_same_input_evaluator_closeout_depends_on_v157():
    d = _check_v157()
    return _res("depends_on_v157", _passed(d), upstream=d.get("status"), upstream_check=d.get("check"))


def check_T_w_same_input_evaluator_closeout_required_capabilities_named():
    ok = len(REQUIRED_EVALUATOR_CAPABILITIES) == 7 and "same_input_rows_at_APF_route_point" in REQUIRED_EVALUATOR_CAPABILITIES
    return _res("required_capabilities_named", ok, requirements=REQUIRED_EVALUATOR_CAPABILITIES)


def check_T_w_same_input_evaluator_closeout_candidate_audit_nonempty():
    c = evaluator_candidates()
    ok = len(c) >= 5 and all(x.reviewed_or_standard for x in c)
    return _res("candidate_audit_nonempty", ok, candidates=tuple(asdict(x) for x in c))


def check_T_w_same_input_evaluator_closeout_acfw_role_split():
    acfw = [c for c in evaluator_candidates() if c.candidate_id == "ACFW_2004_MW_PARAMETRIZATION"][0]
    ok = acfw.provides_total_evaluator and acfw.provides_source_local_rows and not acfw.provides_same_input_row_evaluator
    return _res("acfw_role_split", ok, candidate=asdict(acfw))


def check_T_w_same_input_evaluator_closeout_no_exact_evaluator_found():
    a = evaluator_audit_summary()
    ok = not a["exact_evaluator_found"] and a["audit_verdict"] == "NO_REVIEWED_PER_ROW_SAME_INPUT_EVALUATOR_FOUND"
    return _res("no_exact_evaluator_found", ok, audit=a)


def check_T_w_same_input_evaluator_closeout_first_failed_gate_locked():
    ok = evaluator_audit_summary()["first_failed_gate"] == FIRST_FAILED_GATE
    return _res("first_failed_gate_locked", ok, first_failed_gate=FIRST_FAILED_GATE)


def check_T_w_same_input_evaluator_closeout_gate_ladder_has_terminal_blockers():
    gates = closeout_gates()
    failed = [g for g in gates if not g.satisfied]
    ok = len(gates) == 7 and len(failed) == 3 and all(g.closeout_action in ("terminal blocker", "keep locked") for g in failed)
    return _res("gate_ladder_has_terminal_blockers", ok, gates=tuple(asdict(g) for g in gates))


def check_T_w_same_input_evaluator_closeout_route_input_preserved():
    p = route_input_point()
    ok = p.point_id.startswith("APF_TRACE_ON_SHELL_ROUTE_INPUT_POINT") and p.Delta_r_APF_TRACE > 0 and p.M_W_TRACE_GeV > 80
    return _res("route_input_preserved", ok, route_input=asdict(p))


def check_T_w_same_input_evaluator_closeout_apf_rows_still_sum_to_target():
    rows = transferred_rows("APF_TRACE_TARGET_TOTAL")
    total = sum(r.value_at_route_input for r in rows)
    ok = abs(total - float(APF_DELTA_R_TARGET)) < 1e-14
    return _res("apf_rows_still_sum_to_target", ok, total=total, target=float(APF_DELTA_R_TARGET))


def check_T_w_same_input_evaluator_closeout_eight_transferred_rows_retained():
    rows = transferred_rows("APF_TRACE_TARGET_TOTAL")
    ok = len(rows) == 8 and tuple(r.row_id for r in rows) == ROW_ORDER
    return _res("eight_transferred_rows_retained", ok, row_ids=tuple(r.row_id for r in rows))


def check_T_w_same_input_evaluator_closeout_no_row_admitted_for_export():
    ok = not any(r.admitted_for_physical_export or r.reviewed_same_input_row for r in transferred_rows("APF_TRACE_TARGET_TOTAL"))
    return _res("no_row_admitted_for_export", ok)


def check_T_w_same_input_evaluator_closeout_covariance_sigma_preserved():
    sig = covariance_summary("APF_TRACE_TARGET_TOTAL", "rank_one_correlated_source_theory")
    ok = 3.99 < sig.sigma_MW_MeV < 4.01 and sig.sigma_delta_r > 0
    return _res("covariance_sigma_preserved", ok, covariance=asdict(sig))


def check_T_w_same_input_evaluator_closeout_pull_under_one_sigma():
    n = terminal_numerics()
    ok = n["pull_source_minus_APF_sigma"] < 1.0 and 3.0 < n["abs_M_W_gap_MeV"] < 4.0
    return _res("pull_under_one_sigma", ok, numerics=n)


def check_T_w_same_input_evaluator_closeout_mw_roundtrip_preserved():
    n = terminal_numerics()
    ok = abs(n["M_W_from_APF_Delta_r_GeV"] - n["M_W_TRACE_GeV"]) < 1e-10
    return _res("mw_roundtrip_preserved", ok, numerics=n)


def check_T_w_same_input_evaluator_closeout_publication_claim_allowed():
    c = terminal_publication_claim()
    ok = "not physical export" in c["route_status"] or c["physical_export_status"] == "OPEN_BLOCKED"
    ok = ok and "final physical" in c["forbidden_claim"] and c["first_failed_gate"] == FIRST_FAILED_GATE
    return _res("publication_claim_allowed", ok, claim=c)


def check_T_w_same_input_evaluator_closeout_forbidden_claim_present_only_as_forbidden():
    c = terminal_publication_claim()
    ok = c["forbidden_claim"] == "APF has produced a final physical on-shell W mass prediction."
    return _res("forbidden_claim_present_only_as_forbidden", ok, forbidden=c["forbidden_claim"])


def check_T_w_same_input_evaluator_closeout_export_lock_preserved():
    r = terminal_export_lock_report()
    ok = not r["physical_W_export_enabled"] and not r["exports_physical_M_W"] and r["first_failed_gate"] == FIRST_FAILED_GATE
    return _res("export_lock_preserved", ok, export_lock=r)


def check_T_w_same_input_evaluator_closeout_final_readiness_blocked():
    r = terminal_export_lock_report()
    ready = r["final_readiness_report"]
    ok = not r["physical_W_export_ready"] and not ready.get("physical_W_export_ready", True) and not ready.get("exports_physical_M_W", True)
    return _res("final_readiness_blocked", ok, readiness=ready)


def check_T_w_same_input_evaluator_closeout_ladder_has_open_physical_row():
    rows = terminal_closeout_rows()
    phys = [r for r in rows if r.layer == "physical W export"][0]
    ok = len(rows) == 6 and not phys.closed and phys.status == PHYSICAL_EXPORT_STATUS
    return _res("ladder_has_open_physical_row", ok, ladder=tuple(asdict(r) for r in rows))


def check_T_w_same_input_evaluator_closeout_ladder_prior_layers_closed():
    rows = [r for r in terminal_closeout_rows() if r.layer != "physical W export"]
    ok = all(r.closed and not r.physical_export_ready for r in rows)
    return _res("ladder_prior_layers_closed", ok, layers=tuple(asdict(r) for r in rows))


def check_T_w_same_input_evaluator_closeout_terminal_status_exact():
    r = closeout_report()
    ok = r["terminal_verdict"] == "P_terminal_W_route_closeout__model_limited_same_input_evaluation__not_physical_export"
    return _res("terminal_status_exact", ok, verdict=r["terminal_verdict"])


def check_T_w_same_input_evaluator_closeout_v157_boundary_consistent():
    b = v157_export_boundary_report()
    ok = b["first_failed_gate_after_v156"] == "REVIEWED_PER_ROW_SAME_INPUT_EVALUATOR"
    return _res("v157_boundary_consistent", ok, v157_boundary=b)


def check_T_w_same_input_evaluator_closeout_no_forbidden_tokens():
    r = closeout_report()
    safe = {"audit": r["evaluator_audit"], "gates": r["closeout_gates"], "ladder": r["terminal_closeout_ladder"]}
    return _res("no_forbidden_tokens", not _contains_forbidden_token(safe))


def check_T_w_same_input_evaluator_closeout_payload_digest_present():
    d = closeout_report()["payload_digest"]
    return _res("payload_digest_present", isinstance(d, str) and d.startswith("sha256:") and len(d) == 71, digest=d)


def check_T_w_same_input_evaluator_closeout_candidate_verdicts_reject_export():
    ok = all(c.verdict.startswith("REJECT_FOR_PHYSICAL_EXPORT") for c in evaluator_candidates())
    return _res("candidate_verdicts_reject_export", ok, verdicts=tuple((c.candidate_id, c.verdict) for c in evaluator_candidates()))


def check_T_w_same_input_evaluator_closeout_total_contexts_admitted_only_as_context():
    a = evaluator_audit_summary()
    ok = len(a["total_evaluator_contexts"]) >= 3 and not a["exact_evaluator_found"]
    return _res("total_contexts_admitted_only_as_context", ok, audit=a)


def check_T_w_same_input_evaluator_closeout_source_local_rows_do_not_unlock():
    a = evaluator_audit_summary()
    ok = "ACFW_2004_MW_PARAMETRIZATION" in a["source_local_row_sources"] and not a["exact_evaluator_found"]
    return _res("source_local_rows_do_not_unlock", ok, audit=a)


def check_T_w_same_input_evaluator_closeout_model_limited_status_named():
    c = terminal_publication_claim()
    ok = c["model_limited_status"] == MODEL_LIMITED_STATUS and c["route_status"] == TERMINAL_ROUTE_STATUS
    return _res("model_limited_status_named", ok, claim=c)


def check_T_w_same_input_evaluator_closeout_remaining_action_specific():
    r = terminal_export_lock_report()
    ok = "reviewed same-input Delta-r row evaluator" in r["remaining_action_to_unlock"] and "covariance" in r["remaining_action_to_unlock"]
    return _res("remaining_action_specific", ok, remaining_action=r["remaining_action_to_unlock"])


def check_T_w_same_input_evaluator_closeout_candidate_ids_unique():
    ids = [c.candidate_id for c in evaluator_candidates()]
    ok = len(ids) == len(set(ids))
    return _res("candidate_ids_unique", ok, ids=tuple(ids))


def check_T_w_same_input_evaluator_closeout_route_numerics_stable():
    n = terminal_numerics()
    ok = abs(n["Delta_r_source_minus_APF"] - 0.00020700271122760933) < 1e-15 and abs(n["abs_M_W_gap_MeV"] - 3.484092760784031) < 1e-6
    return _res("route_numerics_stable", ok, numerics=n)


def check_T_w_same_input_evaluator_closeout_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_w_same_input_evaluator_closeout_bank_closure"]
    ok = all(_passed(r) for r in rows)
    return _res("bank_closure", ok, passed_count=sum(_passed(r) for r in rows), total=len(rows))


_CHECKS: Dict[str, Any] = {
    "check_T_w_same_input_evaluator_closeout_status_declared": check_T_w_same_input_evaluator_closeout_status_declared,
    "check_T_w_same_input_evaluator_closeout_depends_on_v157": check_T_w_same_input_evaluator_closeout_depends_on_v157,
    "check_T_w_same_input_evaluator_closeout_required_capabilities_named": check_T_w_same_input_evaluator_closeout_required_capabilities_named,
    "check_T_w_same_input_evaluator_closeout_candidate_audit_nonempty": check_T_w_same_input_evaluator_closeout_candidate_audit_nonempty,
    "check_T_w_same_input_evaluator_closeout_acfw_role_split": check_T_w_same_input_evaluator_closeout_acfw_role_split,
    "check_T_w_same_input_evaluator_closeout_no_exact_evaluator_found": check_T_w_same_input_evaluator_closeout_no_exact_evaluator_found,
    "check_T_w_same_input_evaluator_closeout_first_failed_gate_locked": check_T_w_same_input_evaluator_closeout_first_failed_gate_locked,
    "check_T_w_same_input_evaluator_closeout_gate_ladder_has_terminal_blockers": check_T_w_same_input_evaluator_closeout_gate_ladder_has_terminal_blockers,
    "check_T_w_same_input_evaluator_closeout_route_input_preserved": check_T_w_same_input_evaluator_closeout_route_input_preserved,
    "check_T_w_same_input_evaluator_closeout_apf_rows_still_sum_to_target": check_T_w_same_input_evaluator_closeout_apf_rows_still_sum_to_target,
    "check_T_w_same_input_evaluator_closeout_eight_transferred_rows_retained": check_T_w_same_input_evaluator_closeout_eight_transferred_rows_retained,
    "check_T_w_same_input_evaluator_closeout_no_row_admitted_for_export": check_T_w_same_input_evaluator_closeout_no_row_admitted_for_export,
    "check_T_w_same_input_evaluator_closeout_covariance_sigma_preserved": check_T_w_same_input_evaluator_closeout_covariance_sigma_preserved,
    "check_T_w_same_input_evaluator_closeout_pull_under_one_sigma": check_T_w_same_input_evaluator_closeout_pull_under_one_sigma,
    "check_T_w_same_input_evaluator_closeout_mw_roundtrip_preserved": check_T_w_same_input_evaluator_closeout_mw_roundtrip_preserved,
    "check_T_w_same_input_evaluator_closeout_publication_claim_allowed": check_T_w_same_input_evaluator_closeout_publication_claim_allowed,
    "check_T_w_same_input_evaluator_closeout_forbidden_claim_present_only_as_forbidden": check_T_w_same_input_evaluator_closeout_forbidden_claim_present_only_as_forbidden,
    "check_T_w_same_input_evaluator_closeout_export_lock_preserved": check_T_w_same_input_evaluator_closeout_export_lock_preserved,
    "check_T_w_same_input_evaluator_closeout_final_readiness_blocked": check_T_w_same_input_evaluator_closeout_final_readiness_blocked,
    "check_T_w_same_input_evaluator_closeout_ladder_has_open_physical_row": check_T_w_same_input_evaluator_closeout_ladder_has_open_physical_row,
    "check_T_w_same_input_evaluator_closeout_ladder_prior_layers_closed": check_T_w_same_input_evaluator_closeout_ladder_prior_layers_closed,
    "check_T_w_same_input_evaluator_closeout_terminal_status_exact": check_T_w_same_input_evaluator_closeout_terminal_status_exact,
    "check_T_w_same_input_evaluator_closeout_v157_boundary_consistent": check_T_w_same_input_evaluator_closeout_v157_boundary_consistent,
    "check_T_w_same_input_evaluator_closeout_no_forbidden_tokens": check_T_w_same_input_evaluator_closeout_no_forbidden_tokens,
    "check_T_w_same_input_evaluator_closeout_payload_digest_present": check_T_w_same_input_evaluator_closeout_payload_digest_present,
    "check_T_w_same_input_evaluator_closeout_candidate_verdicts_reject_export": check_T_w_same_input_evaluator_closeout_candidate_verdicts_reject_export,
    "check_T_w_same_input_evaluator_closeout_total_contexts_admitted_only_as_context": check_T_w_same_input_evaluator_closeout_total_contexts_admitted_only_as_context,
    "check_T_w_same_input_evaluator_closeout_source_local_rows_do_not_unlock": check_T_w_same_input_evaluator_closeout_source_local_rows_do_not_unlock,
    "check_T_w_same_input_evaluator_closeout_model_limited_status_named": check_T_w_same_input_evaluator_closeout_model_limited_status_named,
    "check_T_w_same_input_evaluator_closeout_remaining_action_specific": check_T_w_same_input_evaluator_closeout_remaining_action_specific,
    "check_T_w_same_input_evaluator_closeout_candidate_ids_unique": check_T_w_same_input_evaluator_closeout_candidate_ids_unique,
    "check_T_w_same_input_evaluator_closeout_route_numerics_stable": check_T_w_same_input_evaluator_closeout_route_numerics_stable,
    "check_T_w_same_input_evaluator_closeout_bank_closure": check_T_w_same_input_evaluator_closeout_bank_closure,
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
    n = out["report"]["report"]["terminal_numerics"]
    print("M_W_TRACE_GeV", f"{n['M_W_TRACE_GeV']:.12f}")
    print("Delta_r_APF_TRACE", f"{n['Delta_r_APF_TRACE']:.18f}")
    print("abs_M_W_gap_MeV", f"{n['abs_M_W_gap_MeV']:.6f}")
    print("pull_sigma", f"{n['pull_source_minus_APF_sigma']:.6f}")
    raise SystemExit(0 if out["passed"] else 1)
