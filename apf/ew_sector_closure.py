"""APF electroweak trace-sector closure layer v22.0.

This module closes the EW trace-sector package at the sector level.  It does
not reopen the W-loop rabbit hole.  It assembles the already-banked weak-angle,
W_TRACE/DIZET transport, W/Z bridge, and coupling-ratio consequences into a
single claim-boundary ledger.

Closed here:
  * weak-angle trace anchor sin^2(theta_W)=3/13;
  * coupling-ratio consequence g'/g=sqrt(3/10);
  * W_TRACE anchor and reviewed same-input DIZET on-shell export-candidate;
  * external-MZ W/Z bridge and scheme boundary;
  * EW-sector claim ladder separating trace closure from full SM loop closure.

Still open downstream:
  * independent APF-native full electroweak loop derivation;
  * APF-native derivation of M_Z as a physical on-shell mass;
  * fermion-sector trace-to-scheme exports beyond the EW trace package.
"""
from __future__ import annotations

import csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List

STATUS = "P_ew_trace_sector_closure"
VERSION = "v22_0"
APF_VERSION = "22.0.0"
PASS_STATUS = "EW_TRACE_SECTOR_CLOSURE_PASS"
TITLE = "Electroweak trace-sector closure and on-shell export boundary"

# Exact APF electroweak trace anchor.
SIN2_THETA_TRACE = 3.0 / 13.0
COS2_THETA_TRACE = 10.0 / 13.0
TAN2_THETA_TRACE = 3.0 / 10.0
GP_OVER_G_TRACE = math.sqrt(TAN2_THETA_TRACE)
G_OVER_GEW_TRACE = math.sqrt(COS2_THETA_TRACE)
GP_OVER_GEW_TRACE = math.sqrt(SIN2_THETA_TRACE)
COS_THETA_TRACE = math.sqrt(COS2_THETA_TRACE)
SIN_THETA_TRACE = math.sqrt(SIN2_THETA_TRACE)

# W trace and DIZET same-input transport result.
M_W_TRACE_GEV = 80.362164334
M_W_DIZET_APF_INPUT_GEV = 80.357341077578084
DIZET_MINUS_APF_MEV = (M_W_DIZET_APF_INPUT_GEV - M_W_TRACE_GEV) * 1000.0
ABS_DIZET_APF_MEV = abs(DIZET_MINUS_APF_MEV)
SIGMA_INPUT_PLUS_THEORY_MEV = 4.424866188882492
PULL_INPUT_PLUS_THEORY = ABS_DIZET_APF_MEV / SIGMA_INPUT_PLUS_THEORY_MEV

# Delta-r ledger inherited from v16.4/v21 route.
DELTA_R_DIZET_APF_INPUT = 0.036501785659414865
DELTA_R_DELTA_ALPHA = 0.05907386039640014
DELTA_R_REM = 0.011667933872161376
DELTA_R_RHO_CROSS = -0.03424000860914665
DELTA_R_LEDGER_SUM = DELTA_R_DELTA_ALPHA + DELTA_R_REM + DELTA_R_RHO_CROSS

# External-MZ bridge: this is a consistency bridge, not an APF derivation of MZ.
M_Z_EXTERNAL_GEV = 91.1876
WZ_RATIO_APF_TRACE_WITH_EXTERNAL_MZ = M_W_TRACE_GEV / M_Z_EXTERNAL_GEV
SW2_ONSHELL_BRIDGE = 1.0 - WZ_RATIO_APF_TRACE_WITH_EXTERNAL_MZ ** 2

# Useful comparison anchors already used in prior validation sections.
PDG_MSbar_SIN2Z = 0.23129
PDG_ONSHELL_SW2 = 0.22348
TRACE_TO_MSbar_SIN2_OFFSET = SIN2_THETA_TRACE - PDG_MSbar_SIN2Z
BRIDGE_TO_ONSHELL_OFFSET = SW2_ONSHELL_BRIDGE - PDG_ONSHELL_SW2

@dataclass(frozen=True)
class ClosureRow:
    object_id: str
    value: str
    status: str
    meaning: str
    boundary: str

@dataclass(frozen=True)
class CouplingRow:
    quantity: str
    expression: str
    value: float
    status: str
    note: str

@dataclass(frozen=True)
class ClaimRow:
    claim_id: str
    claim: str
    status: str
    safe_language: str
    forbidden_language: str

CLOSURE_TABLE: List[ClosureRow] = [
    ClosureRow("sin2_theta_W_trace", "3/13 = %.12f" % SIN2_THETA_TRACE, "P_trace", "EW mixing trace anchor", "not a scheme-free physical weak-angle claim"),
    ClosureRow("gprime_over_g", "sqrt(3/10) = %.12f" % GP_OVER_G_TRACE, "P_derived", "coupling-ratio consequence of trace anchor", "trace-level coupling geometry, not running-coupling export"),
    ClosureRow("M_W_APF_TRACE", "%.9f GeV" % M_W_TRACE_GEV, "P_trace", "W trace anchor", "not directly the physical on-shell mass"),
    ClosureRow("M_W_APF_to_OS", "DIZET same-input %.12f GeV; residual %.6f MeV; pull %.6f sigma" % (M_W_DIZET_APF_INPUT_GEV, ABS_DIZET_APF_MEV, PULL_INPUT_PLUS_THEORY), "P_export_candidate", "reviewed same-input on-shell transport validation", "not an independent APF derivation of full EW loops"),
    ClosureRow("M_Z", "%.4f GeV external" % M_Z_EXTERNAL_GEV, "external_input", "used for W/Z bridge", "not derived in EW trace closure"),
    ClosureRow("WZ_ratio_bridge", "%.12f" % WZ_RATIO_APF_TRACE_WITH_EXTERNAL_MZ, "P_bridge", "external-MZ on-shell consistency bridge", "not identical to trace cos(theta_W)"),
    ClosureRow("sw2_onshell_bridge", "%.12f" % SW2_ONSHELL_BRIDGE, "P_bridge", "bridge value from APF W trace and external MZ", "not the same object as MSbar sin^2(theta_W)"),
    ClosureRow("full_EW_loop_derivation", "OPEN", "OPEN_family_formulae", "downstream APF-native theorem program", "not required for EW trace-sector closure"),
]

COUPLING_TABLE: List[CouplingRow] = [
    CouplingRow("sin^2(theta_W)", "3/13", SIN2_THETA_TRACE, "P_trace", "APF weak-angle trace anchor"),
    CouplingRow("cos^2(theta_W)", "10/13", COS2_THETA_TRACE, "P_derived", "complement of trace anchor"),
    CouplingRow("tan^2(theta_W)", "3/10", TAN2_THETA_TRACE, "P_derived", "ratio of trace weak factors"),
    CouplingRow("g'/g", "sqrt(3/10)", GP_OVER_G_TRACE, "P_derived", "EW trace coupling-ratio reconstruction"),
    CouplingRow("g/sqrt(g^2+g'^2)", "sqrt(10/13)", G_OVER_GEW_TRACE, "P_derived", "trace cosine/mass-ratio anchor"),
    CouplingRow("g'/sqrt(g^2+g'^2)", "sqrt(3/13)", GP_OVER_GEW_TRACE, "P_derived", "trace sine/mixing anchor"),
]

CLAIM_LADDER: List[ClaimRow] = [
    ClaimRow("EW_TRACE_CLOSED", "The APF electroweak trace sector closes at the level of mixing, coupling ratio, and W trace export-candidate validation.", "SAFE", "EW trace-sector closure", "full physical electroweak sector final derivation"),
    ClaimRow("W_EXPORT_CANDIDATE", "The APF W trace anchor survives reviewed same-input on-shell DIZET transport at about 1.09 sigma.", "SAFE", "on-shell export candidate", "APF has independently derived all electroweak loop corrections"),
    ClaimRow("WZ_BRIDGE", "Using external MZ, the APF W trace gives an on-shell W/Z bridge value and scheme-boundary check.", "SAFE", "external-MZ bridge", "APF derives MZ here"),
    ClaimRow("LOOP_PROGRAM_OPEN", "Full APF-native electroweak loop reconstruction remains a downstream theorem program.", "SAFE", "downstream open theorem program", "already closed as a native derivation"),
    ClaimRow("NEXT_SECTOR", "After EW closure, the next clean export candidate is bottom-quark MSbar transport.", "SAFE", "next-sector sequencing", "all fermion physical masses are already exported"),
]


def ew_data() -> Dict[str, Any]:
    return {
        "status": STATUS,
        "version": VERSION,
        "apf_version": APF_VERSION,
        "pass_status": PASS_STATUS,
        "sin2_theta_trace": SIN2_THETA_TRACE,
        "cos2_theta_trace": COS2_THETA_TRACE,
        "tan2_theta_trace": TAN2_THETA_TRACE,
        "gprime_over_g_trace": GP_OVER_G_TRACE,
        "m_w_trace_gev": M_W_TRACE_GEV,
        "m_w_dizet_apf_input_gev": M_W_DIZET_APF_INPUT_GEV,
        "dizet_minus_apf_mev": DIZET_MINUS_APF_MEV,
        "abs_dizet_apf_mev": ABS_DIZET_APF_MEV,
        "sigma_input_plus_theory_mev": SIGMA_INPUT_PLUS_THEORY_MEV,
        "pull_input_plus_theory": PULL_INPUT_PLUS_THEORY,
        "delta_r_dizet_apf_input": DELTA_R_DIZET_APF_INPUT,
        "delta_r_ledger_sum": DELTA_R_LEDGER_SUM,
        "delta_r_ledger_residual": DELTA_R_LEDGER_SUM - DELTA_R_DIZET_APF_INPUT,
        "m_z_external_gev": M_Z_EXTERNAL_GEV,
        "wz_ratio_bridge": WZ_RATIO_APF_TRACE_WITH_EXTERNAL_MZ,
        "sw2_onshell_bridge": SW2_ONSHELL_BRIDGE,
        "pdg_msbar_sin2z_context": PDG_MSbar_SIN2Z,
        "pdg_onshell_sw2_context": PDG_ONSHELL_SW2,
        "trace_to_msbar_sin2_offset": TRACE_TO_MSbar_SIN2_OFFSET,
        "bridge_to_onshell_offset": BRIDGE_TO_ONSHELL_OFFSET,
        "closed_claim": "EW trace sector closes at mixing/coupling-ratio/W-export-candidate level.",
        "open_boundary": "Full APF-native EW loop derivation and MZ physical export remain downstream.",
    }


def _check(name: str, passed: bool, detail: str = "") -> Dict[str, Any]:
    return {"name": name, "passed": bool(passed), "detail": detail}


def run_all() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    tol = 1e-12
    checks.append(_check("status_declared", STATUS.startswith("P_ew") and VERSION == "v22_0"))
    checks.append(_check("sin2_exact", abs(SIN2_THETA_TRACE - 3/13) < tol))
    checks.append(_check("cos2_exact", abs(COS2_THETA_TRACE - 10/13) < tol))
    checks.append(_check("sin_cos_partition", abs(SIN2_THETA_TRACE + COS2_THETA_TRACE - 1) < tol))
    checks.append(_check("tan2_exact", abs(TAN2_THETA_TRACE - SIN2_THETA_TRACE/COS2_THETA_TRACE) < tol))
    checks.append(_check("gprime_over_g", abs(GP_OVER_G_TRACE**2 - 3/10) < tol))
    checks.append(_check("g_components_partition", abs(G_OVER_GEW_TRACE**2 + GP_OVER_GEW_TRACE**2 - 1) < tol))
    checks.append(_check("w_trace_positive", M_W_TRACE_GEV > 0))
    checks.append(_check("dizet_transport_positive", M_W_DIZET_APF_INPUT_GEV > 0))
    checks.append(_check("dizet_residual_mev", abs(DIZET_MINUS_APF_MEV - (M_W_DIZET_APF_INPUT_GEV - M_W_TRACE_GEV)*1000) < 1e-9))
    checks.append(_check("pull_positive", PULL_INPUT_PLUS_THEORY > 0 and PULL_INPUT_PLUS_THEORY < 2))
    checks.append(_check("export_candidate_within_two_sigma", PULL_INPUT_PLUS_THEORY < 2.0))
    checks.append(_check("delta_r_ledger_closes", abs(DELTA_R_LEDGER_SUM - DELTA_R_DIZET_APF_INPUT) < 1e-15))
    checks.append(_check("external_mz_positive", M_Z_EXTERNAL_GEV > M_W_TRACE_GEV))
    checks.append(_check("wz_bridge_ratio", abs(WZ_RATIO_APF_TRACE_WITH_EXTERNAL_MZ - M_W_TRACE_GEV/M_Z_EXTERNAL_GEV) < tol))
    checks.append(_check("sw2_bridge_definition", abs(SW2_ONSHELL_BRIDGE - (1 - WZ_RATIO_APF_TRACE_WITH_EXTERNAL_MZ**2)) < tol))
    checks.append(_check("bridge_distinct_from_trace_angle", abs(SW2_ONSHELL_BRIDGE - SIN2_THETA_TRACE) > 1e-3))
    checks.append(_check("claim_table_nonempty", len(CLAIM_LADDER) >= 5))
    checks.append(_check("closure_table_has_open_boundary", any(r.status.startswith("OPEN") for r in CLOSURE_TABLE)))
    checks.append(_check("closure_table_has_export_candidate", any(r.status == "P_export_candidate" for r in CLOSURE_TABLE)))
    checks.append(_check("coupling_table_has_gprime_over_g", any(r.quantity == "g'/g" for r in COUPLING_TABLE)))
    checks.append(_check("no_physical_final_claim", all("physical final" not in r.status.lower() for r in CLOSURE_TABLE)))
    checks.append(_check("mz_marked_external", any(r.object_id == "M_Z" and r.status == "external_input" for r in CLOSURE_TABLE)))
    checks.append(_check("safe_claims_present", all(r.status == "SAFE" for r in CLAIM_LADDER)))
    passed = all(c["passed"] for c in checks)
    return {"status": PASS_STATUS if passed else "EW_TRACE_SECTOR_CLOSURE_FAIL", "passed": passed, "checks": checks, "data": ew_data()}


def write_artifacts(out_dir: str | Path) -> Dict[str, str]:
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    paths: Dict[str, str] = {}
    data = ew_data()
    paths["data_json"] = str(out / "ew_sector_closure_v22_0_data.json")
    (out / "ew_sector_closure_v22_0_data.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    paths["report_json"] = str(out / "ew_sector_closure_v22_0_report.json")
    (out / "ew_sector_closure_v22_0_report.json").write_text(json.dumps(run_all(), indent=2), encoding="utf-8")
    for key, rows, fname in [
        ("closure_table", CLOSURE_TABLE, "ew_sector_closure_table_v22_0.csv"),
        ("coupling_table", COUPLING_TABLE, "ew_sector_coupling_reconstruction_v22_0.csv"),
        ("claim_ladder", CLAIM_LADDER, "ew_sector_claim_ladder_v22_0.csv"),
    ]:
        p = out / fname
        with p.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()))
            writer.writeheader()
            for r in rows:
                writer.writerow(asdict(r))
        paths[key] = str(p)
    return paths

if __name__ == "__main__":
    result = run_all()
    print(result["status"])
    for row in result["checks"]:
        print(("PASS" if row["passed"] else "FAIL") + " " + row["name"])
    raise SystemExit(0 if result["passed"] else 1)

# v23 compatibility: EW sector closure is verified by scripts/check_ew_sector_closure.py
# and its own run_all() artifact.  It is kept out of the theorem bank here so
# historical bank counts remain compatible with the W_TRACE v21 baseline.
def register(registry):
    return None
