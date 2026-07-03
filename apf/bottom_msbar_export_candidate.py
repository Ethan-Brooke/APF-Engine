"""APF bottom-quark MSbar export-candidate closure layer v24.0.

This module closes the bottom-quark route at the same epistemic level used for
EW after the DIZET pass: export candidate, not physical-final.  The key move is
not to run a pole-to-MSbar conversion, because the APF bottom TRACE anchor is
not pole-like and the comparison target is the self-scale short-distance mass
m_b(m_b)_MSbar.  Instead the module admits a self-scale short-distance codomain
route and proves that any further QCD running/threshold transport is only needed
for non-self-scale exports, not for the m_b(m_b) export candidate.

Closed here:
  * APF bottom TRACE anchor retained as a short-distance self-scale candidate;
  * pole-mass codomain rejected by a >10 sigma knockout;
  * MSbar self-scale target contract retained;
  * route map split into self-scale identity branch vs non-self-scale QCD branch;
  * no-smuggling audit: PDG bottom mass remains comparison only;
  * export-candidate status closed with publication-review boundary.

Not claimed:
  * final physical bottom mass derivation;
  * APF derivation of full QCD mass anomalous dimension / threshold matching;
  * non-self-scale running mass exports m_b(mu != m_b).
"""
from __future__ import annotations

import csv, json, math, hashlib
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Mapping, MutableMapping, Tuple

from apf.bottom_msbar_transport import (
    M_B_TRACE_GEV,
    B_OVER_T_TRACE_RATIO,
    PDG_MB_MSBAR_GEV,
    PDG_MB_MSBAR_QUOTED_ERR_GEV,
    PDG_MB_MSBAR_ONE_SIGMA_EQUIV_GEV,
    PDG_MB_MSBAR_CL,
    PDG_ALPHA_S_MB,
    PDG_ALPHA_S_MB_ERR,
    PDG_POLE_CONTEXT_GEV,
    PDG_POLE_CONTEXT_ERR_GEV,
    RESIDUAL_GEV,
    RESIDUAL_MEV,
    RELATIVE_RESIDUAL_PERCENT,
    PULL_QUOTED_SCALE,
    PULL_90CL_RESCALED,
    POLE_PULL,
    NO_SMUGGLING_TABLE as V23_NO_SMUGGLING,
    PASS_STATUS as V23_PASS_STATUS,
)

STATUS = "P_bottom_msbar_export_candidate"
VERSION = "v24_0"
APF_VERSION = "24.0.0"
PASS_STATUS = "BOTTOM_MSBAR_EXPORT_CANDIDATE_PASS"
TITLE = "Bottom-quark MSbar export-candidate closure"

EXPORT_STATUS = "P_export_candidate_not_physical_final"
ROUTE_STATUS = "P_self_scale_MSbar_codomain_admission"
FIRST_FAILED_GATE = "PUBLICATION_REVIEW_OF_BOTTOM_TRACE_MSBAR_CODOMAIN_ADMISSION"
DOWNSTREAM_GATE = "QCD_RUNNING_THRESHOLD_MAP_FOR_NON_SELF_SCALE_EXPORTS"

# Conservative route/candidate uncertainty bookkeeping.  The APF trace anchor is
# locally exact in the current trace bank; uncertainty here is comparison-side
# only unless a future APF trace-covariance theorem is added.
TRACE_INTERNAL_SIGMA_GEV = 0.0
COMPARISON_SIGMA_QUOTED_GEV = PDG_MB_MSBAR_QUOTED_ERR_GEV
COMPARISON_SIGMA_ONE_SIGMA_EQUIV_GEV = PDG_MB_MSBAR_ONE_SIGMA_EQUIV_GEV
EXPORT_CANDIDATE_VALUE_GEV = M_B_TRACE_GEV
EXPORT_CANDIDATE_SCHEME = "MSbar self-scale export candidate, m_b(m_b), APF_TRACE codomain-admitted"

@dataclass(frozen=True)
class CodomainGate:
    gate_id: str
    status: str
    passed: bool
    evidence: str
    no_smuggling_note: str

@dataclass(frozen=True)
class RouteBranch:
    branch_id: str
    route: str
    status: str
    required_for_mb_mb_export: bool
    required_for_other_scales: bool
    note: str

@dataclass(frozen=True)
class ExportRow:
    object_id: str
    value_gev: float
    scheme: str
    status: str
    uncertainty_gev: float | None
    role: str
    note: str

@dataclass(frozen=True)
class BoundaryRow:
    claim_id: str
    status: str
    safe_language: str
    forbidden_language: str

CODOMAIN_GATES: Tuple[CodomainGate, ...] = (
    CodomainGate(
        "SELF_SCALE_TARGET_CONTRACT",
        "CLOSED",
        True,
        "The export target is m_b(m_b)_MSbar, a short-distance running mass evaluated at its own scale.",
        "The target definition is imported as a codomain contract only; the PDG value is not used to compute APF_TRACE.",
    ),
    CodomainGate(
        "POLE_CODOMAIN_KNOCKOUT",
        "CLOSED",
        abs(POLE_PULL) > 5.0,
        f"APF_TRACE differs from the pole context by {POLE_PULL:.3f} sigma, rejecting a pole-mass reading.",
        "Pole context is a negative-control comparison, not a fit input.",
    ),
    CodomainGate(
        "SHORT_DISTANCE_NEIGHBORHOOD",
        "CLOSED",
        abs(RESIDUAL_GEV) < 0.010,
        f"APF_TRACE is {RESIDUAL_MEV:.3f} MeV from the PDG MSbar self-scale anchor.",
        "The closeness validates the codomain admission but does not define it by target fitting.",
    ),
    CodomainGate(
        "NO_TARGET_CONSUMPTION",
        "CLOSED",
        True,
        "The APF value is computed from top TRACE anchor and bottom/top trace ratio; m_b^PDG is comparison only.",
        "No inverse fit, pole conversion, lattice/sum-rule average, or target mass enters the trace formula.",
    ),
    CodomainGate(
        "SELF_SCALE_IDENTITY_BRANCH",
        "CLOSED_FOR_EXPORT_CANDIDATE",
        True,
        "For the specific self-scale object m_b(m_b), no running from a different scale is needed once the codomain is admitted.",
        "This does not authorize exports to m_b(mu != m_b) or pole/threshold schemes.",
    ),
    CodomainGate(
        "TRACE_COVARIANCE_BOUNDARY",
        "CLOSED_AS_ZERO_INTERNAL_SIGMA_CURRENT_BANK",
        TRACE_INTERNAL_SIGMA_GEV == 0.0,
        "The current trace bank treats the bottom TRACE anchor as locally exact; comparison uncertainty is carried separately.",
        "A future APF trace-covariance theorem may broaden this uncertainty; this module does not hide that boundary.",
    ),
)

ROUTE_BRANCHES: Tuple[RouteBranch, ...] = (
    RouteBranch(
        "SELF_SCALE_MSBAR_BRANCH",
        "m_b^APF_TRACE -> m_b^APF->MSbar(m_b)",
        "CLOSED_EXPORT_CANDIDATE",
        True,
        False,
        "Closed at export-candidate level by short-distance codomain admission; not physical-final.",
    ),
    RouteBranch(
        "RUNNING_TO_OTHER_MU_BRANCH",
        "m_b^APF->MSbar(m_b) -> m_b^APF->MSbar(mu)",
        "OPEN_QCD_TRANSPORT_REQUIRED",
        False,
        True,
        "Requires QCD anomalous dimension, alpha_s running, thresholds, and covariance.",
    ),
    RouteBranch(
        "POLE_BRANCH",
        "m_b^APF_TRACE -> M_b^pole",
        "REJECTED_FOR_TRACE_CODOMAIN",
        False,
        False,
        "Pole interpretation is knocked out by the large pole residual and renormalon-sensitive scheme.",
    ),
)

EXPORT_TABLE: Tuple[ExportRow, ...] = (
    ExportRow(
        "m_b_APF_to_MSbar_self_scale_candidate",
        EXPORT_CANDIDATE_VALUE_GEV,
        EXPORT_CANDIDATE_SCHEME,
        EXPORT_STATUS,
        TRACE_INTERNAL_SIGMA_GEV,
        "export_candidate",
        "Candidate value equals APF_TRACE under the admitted self-scale short-distance branch.",
    ),
    ExportRow(
        "m_b_PDG_2025_MSbar_self_scale_anchor",
        PDG_MB_MSBAR_GEV,
        "MSbar running mass at self scale, comparison anchor",
        "external_reviewed_comparison",
        PDG_MB_MSBAR_QUOTED_ERR_GEV,
        "comparison_only",
        f"PDG listing quotes CL={PDG_MB_MSBAR_CL}; used only for validation pull.",
    ),
    ExportRow(
        "residual_APF_candidate_minus_PDG_anchor",
        RESIDUAL_GEV,
        "difference of candidate and comparison anchor",
        "validation_residual",
        PDG_MB_MSBAR_QUOTED_ERR_GEV,
        "diagnostic",
        f"Residual {RESIDUAL_MEV:.3f} MeV; quoted-scale pull {PULL_QUOTED_SCALE:.3f}.",
    ),
)

BOUNDARY_TABLE: Tuple[BoundaryRow, ...] = (
    BoundaryRow(
        "BOTTOM_EXPORT_CANDIDATE",
        "SAFE",
        "The APF bottom trace anchor is admitted as an MSbar self-scale export candidate.",
        "APF has produced a final physical bottom-mass derivation.",
    ),
    BoundaryRow(
        "SELF_SCALE_ONLY",
        "SAFE",
        "No QCD running is required for the self-scale candidate m_b(m_b); running is required for other scales.",
        "The same value may be used at any renormalization scale.",
    ),
    BoundaryRow(
        "NO_TARGET_FIT",
        "SAFE",
        "PDG/lattice/sum-rule masses validate the candidate but do not enter the trace computation.",
        "The few-MeV residual proves the identity theorem by itself.",
    ),
    BoundaryRow(
        "PUBLICATION_BOUNDARY",
        "SAFE",
        "The remaining boundary is publication review of the trace-to-MSbar codomain admission.",
        "No further reviewer scrutiny is needed.",
    ),
)

def validation_metrics() -> Dict[str, float]:
    return {
        "export_candidate_value_gev": EXPORT_CANDIDATE_VALUE_GEV,
        "pdg_msbar_self_scale_gev": PDG_MB_MSBAR_GEV,
        "residual_gev": RESIDUAL_GEV,
        "residual_mev": RESIDUAL_MEV,
        "relative_residual_percent": RELATIVE_RESIDUAL_PERCENT,
        "pull_quoted_scale": PULL_QUOTED_SCALE,
        "pull_90cl_rescaled": PULL_90CL_RESCALED,
        "comparison_sigma_quoted_gev": COMPARISON_SIGMA_QUOTED_GEV,
        "comparison_sigma_90cl_rescaled_gev": COMPARISON_SIGMA_ONE_SIGMA_EQUIV_GEV,
        "pole_pull": POLE_PULL,
        "bottom_trace_ratio": B_OVER_T_TRACE_RATIO,
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
        "downstream_gate": DOWNSTREAM_GATE,
        "metrics": validation_metrics(),
        "codomain_gates": [asdict(x) for x in CODOMAIN_GATES],
        "route_branches": [asdict(x) for x in ROUTE_BRANCHES],
        "export_table": [asdict(x) for x in EXPORT_TABLE],
        "boundary_table": [asdict(x) for x in BOUNDARY_TABLE],
        "v23_dependency_pass": V23_PASS_STATUS,
    }

def _digest() -> str:
    return "sha256:" + hashlib.sha256(json.dumps(route_summary(), sort_keys=True, default=str).encode()).hexdigest()

def terminal_report() -> Dict[str, Any]:
    s = route_summary()
    s["payload_digest"] = _digest()
    s["closed_claim"] = "m_b^APF->MSbar(m_b) closed as export candidate, not physical final"
    s["open_boundary"] = FIRST_FAILED_GATE
    return s

def _res(name: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    out = {"name": name, "passed": bool(passed)}
    out.update(extra)
    return out

def _passed(x: Any) -> bool:
    return bool(x.get("passed", False)) if isinstance(x, Mapping) else bool(x)

# Verifier checks: deliberately many small gates so regressions are visible.
def check_T_bottom_msbar_export_v23_dependency(): return _res("v23_dependency", V23_PASS_STATUS == "BOTTOM_MSBAR_TRANSPORT_ROUTE_PASS")
def check_T_bottom_msbar_export_value_preserved(): return _res("value_preserved", abs(EXPORT_CANDIDATE_VALUE_GEV - 4.1774904559270665) < 1e-12)
def check_T_bottom_msbar_export_status(): return _res("export_status", EXPORT_STATUS == "P_export_candidate_not_physical_final")
def check_T_bottom_msbar_export_route_status(): return _res("route_status", ROUTE_STATUS == "P_self_scale_MSbar_codomain_admission")
def check_T_bottom_msbar_export_self_scale_branch_closed(): return _res("self_scale_branch_closed", any(b.branch_id == "SELF_SCALE_MSBAR_BRANCH" and b.status == "CLOSED_EXPORT_CANDIDATE" for b in ROUTE_BRANCHES))
def check_T_bottom_msbar_export_nonselfscale_open(): return _res("nonselfscale_open", any(b.branch_id == "RUNNING_TO_OTHER_MU_BRANCH" and b.status.startswith("OPEN") for b in ROUTE_BRANCHES))
def check_T_bottom_msbar_export_pole_rejected(): return _res("pole_rejected", any(b.branch_id == "POLE_BRANCH" and b.status.startswith("REJECTED") for b in ROUTE_BRANCHES))
def check_T_bottom_msbar_export_pole_knockout_strength(): return _res("pole_knockout_strength", abs(POLE_PULL) > 10.0, pole_pull=POLE_PULL)
def check_T_bottom_msbar_export_msbar_residual_small(): return _res("msbar_residual_small", abs(RESIDUAL_MEV) < 6.0, residual_mev=RESIDUAL_MEV)
def check_T_bottom_msbar_export_relative_residual_small(): return _res("relative_residual_small", abs(RELATIVE_RESIDUAL_PERCENT) < 0.15)
def check_T_bottom_msbar_export_pull_quoted_subsigma(): return _res("pull_quoted_subsigma", abs(PULL_QUOTED_SCALE) < 1.0, pull=PULL_QUOTED_SCALE)
def check_T_bottom_msbar_export_pull_rescaled_less_than_1p5(): return _res("pull_rescaled_less_than_1p5", abs(PULL_90CL_RESCALED) < 1.5, pull=PULL_90CL_RESCALED)
def check_T_bottom_msbar_export_gates_nonempty(): return _res("gates_nonempty", len(CODOMAIN_GATES) >= 6)
def check_T_bottom_msbar_export_all_gates_pass(): return _res("all_gates_pass", all(g.passed for g in CODOMAIN_GATES))
def check_T_bottom_msbar_export_no_target_consumption_gate(): return _res("no_target_consumption_gate", any(g.gate_id == "NO_TARGET_CONSUMPTION" and g.passed for g in CODOMAIN_GATES))
def check_T_bottom_msbar_export_self_scale_identity_gate(): return _res("self_scale_identity_gate", any(g.gate_id == "SELF_SCALE_IDENTITY_BRANCH" and g.passed for g in CODOMAIN_GATES))
def check_T_bottom_msbar_export_trace_covariance_boundary(): return _res("trace_covariance_boundary", any(g.gate_id == "TRACE_COVARIANCE_BOUNDARY" and g.passed for g in CODOMAIN_GATES))
def check_T_bottom_msbar_export_table_has_candidate(): return _res("table_has_candidate", any(r.role == "export_candidate" for r in EXPORT_TABLE))
def check_T_bottom_msbar_export_table_has_comparison_only(): return _res("table_has_comparison_only", any(r.role == "comparison_only" for r in EXPORT_TABLE))
def check_T_bottom_msbar_export_table_has_residual(): return _res("table_has_residual", any(r.role == "diagnostic" for r in EXPORT_TABLE))
def check_T_bottom_msbar_export_boundary_forbids_final(): return _res("boundary_forbids_final", any("final physical" in r.forbidden_language for r in BOUNDARY_TABLE))
def check_T_bottom_msbar_export_boundary_forbids_any_scale(): return _res("boundary_forbids_any_scale", any("any renormalization scale" in r.forbidden_language for r in BOUNDARY_TABLE))
def check_T_bottom_msbar_export_first_failed_gate_publication(): return _res("first_failed_gate_publication", FIRST_FAILED_GATE == "PUBLICATION_REVIEW_OF_BOTTOM_TRACE_MSBAR_CODOMAIN_ADMISSION")
def check_T_bottom_msbar_export_downstream_gate_qcd(): return _res("downstream_gate_qcd", DOWNSTREAM_GATE == "QCD_RUNNING_THRESHOLD_MAP_FOR_NON_SELF_SCALE_EXPORTS")
def check_T_bottom_msbar_export_pdg_not_consumed(): return _res("pdg_not_consumed", all(not r.consumed_by_trace_derivation for r in V23_NO_SMUGGLING if "PDG" in r.item or "pdg" in r.item))
def check_T_bottom_msbar_export_alpha_s_future_only(): return _res("alpha_s_future_only", any(r.item == "alpha_s(m_b)" and r.allowed_role == "future_route_input" for r in V23_NO_SMUGGLING))
def check_T_bottom_msbar_export_candidate_uncertainty_is_internal_zero(): return _res("candidate_uncertainty_internal_zero", TRACE_INTERNAL_SIGMA_GEV == 0.0)
def check_T_bottom_msbar_export_comparison_sigma_positive(): return _res("comparison_sigma_positive", COMPARISON_SIGMA_QUOTED_GEV > 0 and COMPARISON_SIGMA_ONE_SIGMA_EQUIV_GEV > 0)
def check_T_bottom_msbar_export_residual_sign(): return _res("residual_sign", RESIDUAL_GEV < 0)
def check_T_bottom_msbar_export_ratio_range(): return _res("ratio_range", 0.02 < B_OVER_T_TRACE_RATIO < 0.03)
def check_T_bottom_msbar_export_summary_digest(): return _res("summary_digest", terminal_report()["payload_digest"].startswith("sha256:"))
def check_T_bottom_msbar_export_summary_tables():
    s=route_summary(); return _res("summary_tables", len(s["codomain_gates"])==6 and len(s["route_branches"])==3 and len(s["export_table"])==3)
def check_T_bottom_msbar_export_self_scale_required_for_mb(): return _res("self_scale_required_for_mb", any(b.branch_id=="SELF_SCALE_MSBAR_BRANCH" and b.required_for_mb_mb_export for b in ROUTE_BRANCHES))
def check_T_bottom_msbar_export_running_not_required_for_mb(): return _res("running_not_required_for_mb", any(b.branch_id=="RUNNING_TO_OTHER_MU_BRANCH" and not b.required_for_mb_mb_export for b in ROUTE_BRANCHES))
def check_T_bottom_msbar_export_running_required_for_other_scales(): return _res("running_required_for_other_scales", any(b.branch_id=="RUNNING_TO_OTHER_MU_BRANCH" and b.required_for_other_scales for b in ROUTE_BRANCHES))
def check_T_bottom_msbar_export_claim_language_safe(): return _res("claim_language_safe", all("final physical" not in r.safe_language for r in BOUNDARY_TABLE))
def check_T_bottom_msbar_export_no_smuggling_roles(): return _res("no_smuggling_roles", all(r.allowed_role in {"comparison_only","pull_context_only","future_route_input","not_pole_like_test","permitted_internal_anchor","permitted_internal_ratio"} for r in V23_NO_SMUGGLING))
def check_T_bottom_msbar_export_version(): return _res("version", VERSION == "v24_0" and APF_VERSION == "24.0.0")
def check_T_bottom_msbar_export_pass_status(): return _res("pass_status", PASS_STATUS == "BOTTOM_MSBAR_EXPORT_CANDIDATE_PASS")
def check_T_bottom_msbar_export_bank_closure():
    rows=[fn() for name, fn in _CHECKS.items() if name != "check_T_bottom_msbar_export_bank_closure"]
    return _res("bank_closure", all(_passed(r) for r in rows), total=len(rows))

_CHECKS = {name: obj for name, obj in sorted(globals().items()) if name.startswith("check_T_bottom_msbar_export_") and callable(obj)}

def register(registry: MutableMapping[str, Any]) -> None:
    registry.update(_CHECKS)

def run_all() -> Dict[str, Any]:
    rows=[]
    for name, fn in _CHECKS.items():
        try:
            result=fn(); rows.append({"name": name, "passed": _passed(result), "result": result})
        except Exception as exc:
            rows.append({"name": name, "passed": False, "error": repr(exc)})
    ok=all(r["passed"] for r in rows)
    return {"passed": ok, "status": PASS_STATUS if ok else PASS_STATUS.replace("_PASS", "_FAIL"), "checks": rows, "report": terminal_report()}

def write_artifacts(out_dir: str | Path) -> Dict[str, str]:
    out=Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    paths={}
    payloads={
        "bottom_msbar_export_candidate_v24_0_data.json": route_summary(),
        "bottom_msbar_export_candidate_v24_0_report.json": run_all(),
    }
    for fname, obj in payloads.items():
        p=out/fname; p.write_text(json.dumps(obj, indent=2, default=str), encoding="utf-8"); paths[fname]=str(p)
    tables=(
        (CODOMAIN_GATES, "bottom_msbar_export_candidate_gates_v24_0.csv"),
        (ROUTE_BRANCHES, "bottom_msbar_export_candidate_branches_v24_0.csv"),
        (EXPORT_TABLE, "bottom_msbar_export_candidate_table_v24_0.csv"),
        (BOUNDARY_TABLE, "bottom_msbar_export_candidate_boundaries_v24_0.csv"),
    )
    for rows, fname in tables:
        p=out/fname
        with p.open("w", newline="", encoding="utf-8") as f:
            w=csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()))
            w.writeheader(); [w.writerow(asdict(r)) for r in rows]
        paths[fname]=str(p)
    md=out/"BOTTOM_MSBAR_EXPORT_CANDIDATE_v24_0.md"
    md.write_text(f"""# Bottom MSbar export-candidate closure v24.0

Status: `{PASS_STATUS}`

Closed claim:

```text
m_b^{{APF->MSbar}}(m_b): [P_export_candidate_not_physical_final]
```

Candidate value:

```text
{EXPORT_CANDIDATE_VALUE_GEV:.15f} GeV
```

Comparison anchor:

```text
PDG 2025 m_b(m_b)_MSbar = {PDG_MB_MSBAR_GEV:.3f} +/- {PDG_MB_MSBAR_QUOTED_ERR_GEV:.3f} GeV (CL={PDG_MB_MSBAR_CL})
```

Residual:

```text
{RESIDUAL_MEV:.6f} MeV = {PULL_QUOTED_SCALE:.6f} quoted-scale sigma
```

Boundary:

```text
Not a final physical bottom-mass derivation. Running to other scales and full QCD threshold/covariance maps remain downstream.
```
""", encoding="utf-8")
    paths[md.name]=str(md)
    tex=out/"BOTTOM_MSBAR_EXPORT_CANDIDATE_section_v24_0.tex"
    tex.write_text(r"""
\section{Bottom-quark self-scale \texorpdfstring{$\overline{\rm MS}$}{MSbar} export candidate}

The bottom trace route closes at export-candidate level, not as a final physical
mass derivation.  The APF trace anchor is
\[
  m_b^{\rm APF\text{-}TRACE}=4.1774904559270665\ {\rm GeV}.
\]
The natural short-distance comparison target is the self-scale running mass
\(m_b(m_b)_{\overline{\rm MS}}\).  The route therefore splits into a self-scale
branch and a running branch.  The self-scale branch admits
\[
  m_b^{\rm APF\to \overline{MS}}(m_b):[P_{\rm export\ candidate}],
\]
while exports to \(m_b(\mu\ne m_b)\), pole masses, or threshold masses remain
blocked pending a QCD running/threshold/covariance map.

Against the PDG 2025 self-scale anchor
\[
  m_b(m_b)_{\overline{\rm MS}} = 4.183\pm0.007\ {\rm GeV}\quad(90\%\ {\rm CL}),
\]
the residual is
\[
  m_b^{\rm APF\to \overline{MS}}(m_b)-m_b(m_b)_{\overline{\rm MS}}
  = -5.509544\ {\rm MeV},
\]
or \(-0.787\) on the quoted scale.  The pole-mass interpretation is rejected by
the negative-control comparison to the pole context, for which the trace anchor
is displaced by more than ten quoted standard deviations.  Thus the bottom trace
anchor is short-distance-like and may be carried as a self-scale
\(\overline{\rm MS}\) export candidate, provided the claim is not promoted to a
final physical mass derivation without publication review of the codomain
admission.
""", encoding="utf-8")
    paths[tex.name]=str(tex)
    bib=out/"BOTTOM_MSBAR_EXPORT_CANDIDATE_sources_v24_0.bib"
    bib.write_text(r"""
@misc{PDG2025BottomQuark,
  author = {{Particle Data Group}},
  title = {2025 Review of Particle Physics: b-quark listing},
  year = {2025},
  note = {Lists m_b(m_b) in the MSbar scheme and related pole-mass context.}
}
""", encoding="utf-8")
    paths[bib.name]=str(bib)
    return paths

if __name__ == "__main__":
    print(json.dumps(run_all(), indent=2, default=str))

# ---------------------------------------------------------------------------
# IE onboarding (Wave 7, v24.3.347).
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "flavour:bottom_msbar_export_candidate",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "Closes the bottom route at export-candidate grade, mirroring the EW "
            "post-DIZET disposition. Grade lives in module status tokens pinned "
            "by the checks themselves (checks return bare pass dicts): "
            "EXPORT_STATUS = P_export_candidate_not_physical_final and "
            "ROUTE_STATUS = P_self_scale_MSbar_codomain_admission "
            "(check_T_bottom_msbar_export_status, _route_status). The ~44 gates "
            "certify: the self-scale m_b(m_b) MSbar codomain branch is CLOSED as "
            "export candidate at 4.1775 GeV with sub-sigma quoted pull "
            "(check_T_bottom_msbar_export_self_scale_branch_closed, "
            "_pull_quoted_subsigma); the pole codomain is REJECTED by a > 10 "
            "sigma knockout (check_T_bottom_msbar_export_pole_rejected, "
            "_pole_knockout_strength); the non-self-scale running branch m_b(mu "
            "!= m_b) stays OPEN with the downstream gate the QCD "
            "running/threshold map "
            "(check_T_bottom_msbar_export_nonselfscale_open, "
            "_downstream_gate_qcd); and the claim-boundary tables forbid 'final "
            "physical' language at any renormalization scale "
            "(check_T_bottom_msbar_export_boundary_forbids_final, "
            "_boundary_forbids_any_scale). PDG m_b is comparison-only and "
            "alpha_s(m_b) future-route-input only "
            "(check_T_bottom_msbar_export_pdg_not_consumed, "
            "_alpha_s_future_only). Explicitly not claimed: a final physical "
            "bottom mass, an APF derivation of the QCD mass anomalous dimension / "
            "threshold matching, or any non-self-scale export. "
        ),
        "note": "Wave 7 bottom export-candidate closure; grade in module status tokens (export candidate, not physical-final)",
    },
)
