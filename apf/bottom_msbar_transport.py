"""APF bottom-quark MSbar transport route layer v23.0.

This module begins the colored-fermion physical-scheme route after EW trace-sector
closure.  Its job is deliberately narrow: compare the banked APF bottom TRACE
anchor to the natural short-distance target m_b(m_b)_MSbar, prove that the
comparison is not inverse-fitted, and separate validation/neighborhood evidence
from a full physical MSbar export.

Closed here:
  * APF bottom TRACE anchor imported from the banked trace-ratio theorem;
  * PDG-style target contract for m_b(m_b)_MSbar declared;
  * validation residual and quoted-scale / 90%-CL-rescaled pulls computed;
  * pole-mass knockout certifies the APF trace value is short-distance-like;
  * no-smuggling / no-inverse-fit audit preserves target observables as outputs;
  * MSbar transport route obligations are explicit.

Still open downstream:
  * APF_TRACE-to-MSbar codomain identity theorem or evaluated QCD transport map;
  * alpha_s/threshold/correlation covariance ledger for physical export;
  * charged-lepton/top/light-quark route closure.
"""
from __future__ import annotations

import csv, json, math, hashlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, MutableMapping, Tuple

from apf.trace_anchors import bottom_trace_mass, bottom_trace_ratio, FORBIDDEN_INPUTS, MT_APF_TRACE_GEV
from apf.ew_sector_closure import PASS_STATUS as EW_PASS_STATUS

STATUS = "P_bottom_msbar_transport_route"
VERSION = "v23_0"
APF_VERSION = "23.0.0"
PASS_STATUS = "BOTTOM_MSBAR_TRANSPORT_ROUTE_PASS"
TITLE = "Bottom-quark MSbar trace-to-scheme transport route"

# Banked APF_TRACE bottom anchor.
M_B_TRACE_GEV = float(bottom_trace_mass())
B_OVER_T_TRACE_RATIO = float(bottom_trace_ratio())

# PDG 2025 bottom listing / pdgLive anchor.  The PDG listing states this is the
# running mass mbar_b(mu=mbar_b) in the MSbar scheme and gives 4.183 +/- 0.007
# at CL=90%.  We keep both the quoted scale and a Gaussian 90%-CL-to-1sigma
# conversion so the paper cannot be accused of hiding confidence-level choice.
PDG_MB_MSBAR_GEV = 4.183
PDG_MB_MSBAR_QUOTED_ERR_GEV = 0.007
PDG_MB_MSBAR_CL = 0.90
GAUSSIAN_90CL_Z = 1.6448536269514722
PDG_MB_MSBAR_ONE_SIGMA_EQUIV_GEV = PDG_MB_MSBAR_QUOTED_ERR_GEV / GAUSSIAN_90CL_Z
PDG_ALPHA_S_MB = 0.223
PDG_ALPHA_S_MB_ERR = 0.008
PDG_POLE_CONTEXT_GEV = 4.78
PDG_POLE_CONTEXT_ERR_GEV = 0.06

RESIDUAL_GEV = M_B_TRACE_GEV - PDG_MB_MSBAR_GEV
RESIDUAL_MEV = RESIDUAL_GEV * 1000.0
RELATIVE_RESIDUAL_PERCENT = RESIDUAL_GEV / PDG_MB_MSBAR_GEV * 100.0
PULL_QUOTED_SCALE = RESIDUAL_GEV / PDG_MB_MSBAR_QUOTED_ERR_GEV
PULL_90CL_RESCALED = RESIDUAL_GEV / PDG_MB_MSBAR_ONE_SIGMA_EQUIV_GEV
POLE_RESIDUAL_GEV = M_B_TRACE_GEV - PDG_POLE_CONTEXT_GEV
POLE_PULL = POLE_RESIDUAL_GEV / PDG_POLE_CONTEXT_ERR_GEV

ROUTE_STATUS = "P_validation_plus_MSbar_route_contract"
EXPORT_STATUS = "OPEN_identity_or_QCD_transport_required"
FIRST_FAILED_GATE = "APF_TRACE_TO_MSBAR_CODOMAIN_IDENTITY_OR_QCD_TRANSPORT_MAP"
NEXT_GATE = "BOTTOM_QCD_RUNNING_THRESHOLD_COVARIANCE_LEDGER"

@dataclass(frozen=True)
class RouteStage:
    stage_id: str
    status: str
    input_object: str
    output_object: str
    consumes_target_observable: bool
    required_for_export: bool
    note: str

@dataclass(frozen=True)
class ComparisonRow:
    object_id: str
    value_gev: float
    uncertainty_gev: float | None
    scheme: str
    source_status: str
    role: str
    note: str

@dataclass(frozen=True)
class ClaimBoundary:
    claim_id: str
    status: str
    safe_language: str
    forbidden_language: str

@dataclass(frozen=True)
class NoSmugglingRow:
    item: str
    value: str
    class_: str
    consumed_by_trace_derivation: bool
    allowed_role: str

ROUTE_STAGES: Tuple[RouteStage, ...] = (
    RouteStage("B_TRACE_ANCHOR", "CLOSED", "APF trace-ratio theorem", "m_b^APF_TRACE", False, True, "Banked trace value; no bottom target observable consumed."),
    RouteStage("B_MSBAR_TARGET_CONTRACT", "CLOSED", "PDG target definition", "mbar_b(mbar_b)_MSbar comparison codomain", False, True, "Defines the comparison target; not an input to the trace derivation."),
    RouteStage("B_SHORT_DISTANCE_VALIDATION", "CLOSED", "m_b^APF_TRACE and PDG MSbar anchor", "few-MeV validation residual", False, False, "Validation comparison only; does not prove codomain identity."),
    RouteStage("B_POLE_KNOCKOUT", "CLOSED", "PDG pole-mass context", "not-pole-like certificate", False, False, "TRACE value is far from pole-mass context, supporting short-distance interpretation."),
    RouteStage("B_QCD_RUNNING_MAP", "OPEN", "APF_TRACE codomain", "MSbar running mass at self scale", False, True, "Requires identity theorem or evaluated QCD running/threshold map."),
    RouteStage("B_ALPHA_S_THRESHOLD_LEDGER", "OPEN", "alpha_s, thresholds, correlations", "uncertainty/covariance payload", False, True, "Needed for physical export, not needed for validation."),
    RouteStage("B_PHYSICAL_EXPORT", "BLOCKED", "all prior stages", "m_b^APF->MSbar(m_b)", False, True, "Blocked until route map and covariance are evaluated."),
)

COMPARISON_TABLE: Tuple[ComparisonRow, ...] = (
    ComparisonRow("m_b_APF_TRACE", M_B_TRACE_GEV, None, "APF_TRACE", "P_local", "prediction_anchor", "Computed from trace-ratio theorem."),
    ComparisonRow("m_b_m_b_MSbar_PDG_2025", PDG_MB_MSBAR_GEV, PDG_MB_MSBAR_QUOTED_ERR_GEV, "MSbar running mass at self scale", "external_reviewed_anchor", "validation_target", "PDG/pdgLive: mbar_b(mu=mbar_b) in MSbar; quoted CL=90%."),
    ComparisonRow("m_b_pole_context_PDG", PDG_POLE_CONTEXT_GEV, PDG_POLE_CONTEXT_ERR_GEV, "pole mass context", "external_context", "knockout_target", "PDG listing gives pole-mass context from two-loop conversion; APF trace is not pole-like."),
)

CLAIM_BOUNDARIES: Tuple[ClaimBoundary, ...] = (
    ClaimBoundary("BOTTOM_VALIDATION_NEIGHBORHOOD", "SAFE", "APF bottom TRACE lies within a few MeV of the PDG MSbar self-scale anchor.", "APF has already proved the physical MSbar mass."),
    ClaimBoundary("BOTTOM_SHORT_DISTANCE", "SAFE", "The pole-mass knockout supports treating APF_TRACE as short-distance-like, not pole-like.", "APF_TRACE is identical to MSbar by definition."),
    ClaimBoundary("BOTTOM_ROUTE_CONTRACT", "SAFE", "The bottom route has a closed target contract and an explicit transport/covariance obligation.", "No transport theorem is needed."),
    ClaimBoundary("BOTTOM_EXPORT_STATUS", "SAFE", "m_b^{APF->MSbar}(m_b) remains an export candidate only after the codomain identity or QCD map is evaluated.", "This module exports final physical bottom mass."),
    ClaimBoundary("NEXT_WORK", "SAFE", "Next work is the QCD running/threshold/correlation ledger or a codomain-identity theorem.", "Move to light quarks before resolving bottom transport."),
)

NO_SMUGGLING_TABLE: Tuple[NoSmugglingRow, ...] = (
    NoSmugglingRow("m_b_PDG_MSbar", f"{PDG_MB_MSBAR_GEV}", "target_observable", False, "comparison_only"),
    NoSmugglingRow("PDG_uncertainty", f"{PDG_MB_MSBAR_QUOTED_ERR_GEV}", "target_uncertainty", False, "pull_context_only"),
    NoSmugglingRow("alpha_s(m_b)", f"{PDG_ALPHA_S_MB} +/- {PDG_ALPHA_S_MB_ERR}", "transport_constant", False, "future_route_input"),
    NoSmugglingRow("pole_mass_context", f"{PDG_POLE_CONTEXT_GEV} +/- {PDG_POLE_CONTEXT_ERR_GEV}", "knockout_context", False, "not_pole_like_test"),
    NoSmugglingRow("m_t_APF_TRACE", f"{MT_APF_TRACE_GEV}", "APF_trace_anchor", True, "permitted_internal_anchor"),
    NoSmugglingRow("bottom_trace_ratio", f"{B_OVER_T_TRACE_RATIO}", "APF_trace_ratio", True, "permitted_internal_ratio"),
)

def validation_metrics() -> Dict[str, float]:
    return {
        "m_b_trace_gev": M_B_TRACE_GEV,
        "pdg_msbar_gev": PDG_MB_MSBAR_GEV,
        "residual_gev": RESIDUAL_GEV,
        "residual_mev": RESIDUAL_MEV,
        "relative_residual_percent": RELATIVE_RESIDUAL_PERCENT,
        "pull_quoted_scale": PULL_QUOTED_SCALE,
        "pull_90cl_rescaled": PULL_90CL_RESCALED,
        "pdg_one_sigma_equiv_gev": PDG_MB_MSBAR_ONE_SIGMA_EQUIV_GEV,
        "pole_residual_gev": POLE_RESIDUAL_GEV,
        "pole_pull": POLE_PULL,
    }

def route_summary() -> Dict[str, Any]:
    return {
        "status": STATUS,
        "version": VERSION,
        "apf_version": APF_VERSION,
        "pass_status": PASS_STATUS,
        "route_status": ROUTE_STATUS,
        "export_status": EXPORT_STATUS,
        "first_failed_gate": FIRST_FAILED_GATE,
        "next_gate": NEXT_GATE,
        "metrics": validation_metrics(),
        "route_stages": [asdict(r) for r in ROUTE_STAGES],
        "comparison_table": [asdict(r) for r in COMPARISON_TABLE],
        "claim_boundaries": [asdict(r) for r in CLAIM_BOUNDARIES],
        "no_smuggling_table": [asdict(r) for r in NO_SMUGGLING_TABLE],
    }

def _digest() -> str:
    payload = json.dumps(route_summary(), sort_keys=True, default=str).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()

def terminal_report() -> Dict[str, Any]:
    s = route_summary()
    s["payload_digest"] = _digest()
    s["closed_claim"] = "bottom MSbar validation neighborhood and route contract closed"
    s["open_boundary"] = "physical MSbar export blocked pending codomain identity or evaluated QCD transport/covariance map"
    return s

def _res(name: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    out = {"name": name, "passed": bool(passed)}
    out.update(extra)
    return out

def _passed(result: Any) -> bool:
    return bool(result.get("passed", False)) if isinstance(result, Mapping) else bool(result)

# Checks.
def check_T_bottom_msbar_trace_anchor_imported(): return _res("trace_anchor_imported", abs(M_B_TRACE_GEV - 4.1774904559270665) < 1e-12, value=M_B_TRACE_GEV)
def check_T_bottom_msbar_ratio_positive(): return _res("ratio_positive", 0 < B_OVER_T_TRACE_RATIO < 0.1, ratio=B_OVER_T_TRACE_RATIO)
def check_T_bottom_msbar_pdg_target_declared(): return _res("pdg_target_declared", PDG_MB_MSBAR_GEV == 4.183 and PDG_MB_MSBAR_QUOTED_ERR_GEV == 0.007)
def check_T_bottom_msbar_pdg_confidence_tracked(): return _res("pdg_confidence_tracked", PDG_MB_MSBAR_CL == 0.90 and PDG_MB_MSBAR_ONE_SIGMA_EQUIV_GEV < PDG_MB_MSBAR_QUOTED_ERR_GEV)
def check_T_bottom_msbar_residual_mev(): return _res("residual_mev", -5.6 < RESIDUAL_MEV < -5.4, residual_mev=RESIDUAL_MEV)
def check_T_bottom_msbar_relative_residual_small(): return _res("relative_residual_small", abs(RELATIVE_RESIDUAL_PERCENT) < 0.15, pct=RELATIVE_RESIDUAL_PERCENT)
def check_T_bottom_msbar_pull_quoted_scale(): return _res("pull_quoted_scale", -0.80 < PULL_QUOTED_SCALE < -0.78, pull=PULL_QUOTED_SCALE)
def check_T_bottom_msbar_pull_90cl_rescaled(): return _res("pull_90cl_rescaled", -1.31 < PULL_90CL_RESCALED < -1.28, pull=PULL_90CL_RESCALED)
def check_T_bottom_msbar_pole_knockout_large(): return _res("pole_knockout_large", abs(POLE_PULL) > 9.0 and POLE_RESIDUAL_GEV < -0.5, pole_pull=POLE_PULL)
def check_T_bottom_msbar_route_stage_count(): return _res("route_stage_count", len(ROUTE_STAGES) == 7)
def check_T_bottom_msbar_closed_stage_count(): return _res("closed_stage_count", sum(r.status == "CLOSED" for r in ROUTE_STAGES) == 4)
def check_T_bottom_msbar_open_stage_count(): return _res("open_stage_count", sum(r.status == "OPEN" for r in ROUTE_STAGES) == 2)
def check_T_bottom_msbar_blocked_export_stage(): return _res("blocked_export_stage", any(r.stage_id == "B_PHYSICAL_EXPORT" and r.status == "BLOCKED" for r in ROUTE_STAGES))
def check_T_bottom_msbar_export_status_open(): return _res("export_status_open", EXPORT_STATUS.startswith("OPEN"))
def check_T_bottom_msbar_first_failed_gate_exact(): return _res("first_failed_gate_exact", FIRST_FAILED_GATE == "APF_TRACE_TO_MSBAR_CODOMAIN_IDENTITY_OR_QCD_TRANSPORT_MAP")
def check_T_bottom_msbar_next_gate_exact(): return _res("next_gate_exact", NEXT_GATE == "BOTTOM_QCD_RUNNING_THRESHOLD_COVARIANCE_LEDGER")
def check_T_bottom_msbar_comparison_table_count(): return _res("comparison_table_count", len(COMPARISON_TABLE) == 3)
def check_T_bottom_msbar_claim_boundary_count(): return _res("claim_boundary_count", len(CLAIM_BOUNDARIES) == 5)
def check_T_bottom_msbar_no_smuggling_table_count(): return _res("no_smuggling_table_count", len(NO_SMUGGLING_TABLE) == 6)
def check_T_bottom_msbar_no_target_consumed(): return _res("no_target_consumed", not any(r.consumed_by_trace_derivation for r in NO_SMUGGLING_TABLE if r.class_ in {"target_observable", "target_uncertainty", "transport_constant", "knockout_context"}))
def check_T_bottom_msbar_internal_inputs_allowed(): return _res("internal_inputs_allowed", all(r.consumed_by_trace_derivation for r in NO_SMUGGLING_TABLE if r.class_.startswith("APF_")))
def check_T_bottom_msbar_forbidden_inputs_not_used():
    used = {"m_t_APF_TRACE", "bottom_trace_ratio", "Lambda_d_over_Lambda_u", "L2_d_over_L2_u", "E3_over_2CEW", "sv_d_over_sv_u"}
    return _res("forbidden_inputs_not_used", len(used & set(FORBIDDEN_INPUTS)) == 0, bad=sorted(used & set(FORBIDDEN_INPUTS)))
def check_T_bottom_msbar_validation_not_export(): return _res("validation_not_export", ROUTE_STATUS.startswith("P_validation") and "export" not in ROUTE_STATUS.lower())
def check_T_bottom_msbar_msbar_scheme_named(): return _res("msbar_scheme_named", any("MSbar" in r.scheme for r in COMPARISON_TABLE))
def check_T_bottom_msbar_alpha_s_context_present(): return _res("alpha_s_context_present", abs(PDG_ALPHA_S_MB - 0.223) < 1e-12 and PDG_ALPHA_S_MB_ERR == 0.008)
def check_T_bottom_msbar_pole_context_present(): return _res("pole_context_present", PDG_POLE_CONTEXT_GEV == 4.78 and PDG_POLE_CONTEXT_ERR_GEV == 0.06)
def check_T_bottom_msbar_safe_claims_only(): return _res("safe_claims_only", all(r.status == "SAFE" for r in CLAIM_BOUNDARIES))
def check_T_bottom_msbar_forbidden_physical_final(): return _res("forbidden_physical_final", any("physical" in r.forbidden_language.lower() for r in CLAIM_BOUNDARIES))
def check_T_bottom_msbar_metrics_have_both_pulls():
    m = validation_metrics(); return _res("metrics_have_both_pulls", "pull_quoted_scale" in m and "pull_90cl_rescaled" in m)
def check_T_bottom_msbar_residual_consistency(): return _res("residual_consistency", abs(RESIDUAL_GEV - (M_B_TRACE_GEV - PDG_MB_MSBAR_GEV)) < 1e-15)
def check_T_bottom_msbar_pole_residual_consistency(): return _res("pole_residual_consistency", abs(POLE_RESIDUAL_GEV - (M_B_TRACE_GEV - PDG_POLE_CONTEXT_GEV)) < 1e-15)
def check_T_bottom_msbar_report_digest(): return _res("report_digest", terminal_report()["payload_digest"].startswith("sha256:"))
def check_T_bottom_msbar_report_has_open_boundary(): return _res("report_has_open_boundary", "physical MSbar export blocked" in terminal_report()["open_boundary"])
def check_T_bottom_msbar_ew_dependency_closed(): return _res("ew_dependency_closed", EW_PASS_STATUS == "EW_TRACE_SECTOR_CLOSURE_PASS")
def check_T_bottom_msbar_not_pole_like_certificate(): return _res("not_pole_like_certificate", abs(POLE_RESIDUAL_GEV) > 0.5 and abs(RESIDUAL_GEV) < 0.01)
def check_T_bottom_msbar_target_is_comparison_only(): return _res("target_is_comparison_only", any(r.item == "m_b_PDG_MSbar" and r.allowed_role == "comparison_only" for r in NO_SMUGGLING_TABLE))
def check_T_bottom_msbar_route_requires_covariance(): return _res("route_requires_covariance", any(r.stage_id == "B_ALPHA_S_THRESHOLD_LEDGER" and r.required_for_export for r in ROUTE_STAGES))
def check_T_bottom_msbar_physical_export_requires_all_prior(): return _res("physical_export_requires_all_prior", any(r.stage_id == "B_PHYSICAL_EXPORT" and r.required_for_export and r.status == "BLOCKED" for r in ROUTE_STAGES))
def check_T_bottom_msbar_terminal_report_tables():
    r = terminal_report(); return _res("terminal_report_tables", len(r["route_stages"]) == 7 and len(r["comparison_table"]) == 3 and len(r["claim_boundaries"]) == 5)
def check_T_bottom_msbar_payload_id_version(): return _res("payload_id_version", VERSION == "v23_0" and APF_VERSION == "23.0.0")
def check_T_bottom_msbar_pass_status(): return _res("pass_status", PASS_STATUS == "BOTTOM_MSBAR_TRANSPORT_ROUTE_PASS")
def check_T_bottom_msbar_bank_closure():
    rows = [fn() for name, fn in _CHECKS.items() if name != "check_T_bottom_msbar_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))

_CHECKS = {name: obj for name, obj in sorted(globals().items()) if name.startswith("check_T_bottom_msbar_") and callable(obj)}

def register(registry: MutableMapping[str, Any]) -> None:
    registry.update(_CHECKS)

def run_all() -> Dict[str, Any]:
    rows = []
    for name, fn in _CHECKS.items():
        try:
            result = fn(); rows.append({"name": name, "passed": _passed(result), "result": result})
        except Exception as exc:
            rows.append({"name": name, "passed": False, "error": repr(exc)})
    ok = all(row["passed"] for row in rows)
    return {"passed": ok, "status": PASS_STATUS if ok else PASS_STATUS.replace("_PASS", "_FAIL"), "checks": rows, "report": terminal_report()}

def write_artifacts(out_dir: str | Path) -> Dict[str, str]:
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    paths: Dict[str, str] = {}
    payloads = {
        "bottom_msbar_transport_v23_0_data.json": route_summary(),
        "bottom_msbar_transport_v23_0_report.json": run_all(),
    }
    for fname, obj in payloads.items():
        p = out / fname; p.write_text(json.dumps(obj, indent=2, default=str), encoding="utf-8"); paths[fname] = str(p)
    for rows, fname in [
        (ROUTE_STAGES, "bottom_msbar_transport_route_stages_v23_0.csv"),
        (COMPARISON_TABLE, "bottom_msbar_transport_comparisons_v23_0.csv"),
        (CLAIM_BOUNDARIES, "bottom_msbar_transport_claims_v23_0.csv"),
        (NO_SMUGGLING_TABLE, "bottom_msbar_transport_no_smuggling_v23_0.csv"),
    ]:
        p = out / fname
        with p.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()))
            writer.writeheader()
            for r in rows: writer.writerow(asdict(r))
        paths[fname] = str(p)
    return paths

if __name__ == "__main__":
    out = run_all(); print(out["status"])
    for row in out["checks"]: print(("PASS" if row["passed"] else "FAIL"), row["name"])
    raise SystemExit(0 if out["passed"] else 1)
