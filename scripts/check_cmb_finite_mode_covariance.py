#!/usr/bin/env python3
"""Standalone runner for the CMB finite-mode covariance projection verifier.

Lands the implementation registry referenced by Paper 19 v0.2 sec.10:
  apf/cmb_finite_mode_covariance.py
  scripts/check_cmb_finite_mode_covariance.py    <- THIS FILE
  results/cmb_finite_mode_covariance_verifier_report.json
  results/cmb_finite_mode_multiplier_table.csv
  results/cmb_finite_mode_toy_data_comparison.csv

Usage:
    python scripts/check_cmb_finite_mode_covariance.py

Writes the 3 results files, prints a summary, exits 0 on PASS.

The verifier status reported (per Paper 19 v0.2 sec.10):
    CMB_FINITE_MODE_COVARIANCE_BANK_PASS  iff all 6 bank checks pass.

This is a model-integrity verifier. It is not a Planck likelihood, not a
public-data comparison, and not a C2 promotion. Paper 19 v0.2 sec.1 status
ladder applies: C1+ banked finite-mode covariance prototype.

Closes Paper 19 v0.2 audit memo G1 flag (`Reference - Paper 19 v0.2 Audit
(2026-05-12).md`).
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

# Locate the codebase root from this file's location
HERE = Path(__file__).resolve().parent
CODEBASE_ROOT = HERE.parent
sys.path.insert(0, str(CODEBASE_ROOT))

from apf.cmb_finite_mode_covariance import (
    run_all,
    run_projection,
    ELL_MIN,
    ELL_MAX,
    THETA_C_DEG,
    LAMBDA_PRESSURE,
)

RESULTS_DIR = CODEBASE_ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def write_verifier_report():
    bank_results = run_all()
    proj = run_projection()
    all_passed = bank_results["passed"] == bank_results["total"]
    status = "CMB_FINITE_MODE_COVARIANCE_BANK_PASS" if all_passed else "CMB_FINITE_MODE_COVARIANCE_BANK_FAIL"
    report = {
        "verifier_status": status,
        "all_passed": all_passed,
        "bank_check_count": bank_results["total"],
        "bank_checks_passed": bank_results["passed"],
        "projection_config": {
            "ell_min": ELL_MIN,
            "ell_max": ELL_MAX,
            "theta_c_deg": THETA_C_DEG,
            "lambda_pressure": LAMBDA_PRESSURE,
            "reference_spectrum": "toy_sachs_wolfe_plateau",
        },
        "projection_result": {
            "S_proj": proj.S_proj,
            "S_std": proj.S_std,
            "ratio": proj.ratio,
            "success": proj.success,
        },
        "bank_check_results": bank_results["results"],
        "paper_reference": "Paper 19 v0.2 §10 (working draft 2026-05-12)",
        "audit_reference": "Reference - Paper 19 v0.2 Audit (2026-05-12).md — G1 closure",
        "promotion_status": "C1+ (banked finite-mode covariance prototype)",
        "non_claims": [
            "Not a Planck likelihood result",
            "Not a public-data comparison",
            "Not a C2 promotion (adversarial-alternatives comparison deferred)",
            "Not a C4 derivation (theta_c and lambda still conventional, not APF-derived)",
        ],
    }
    out = RESULTS_DIR / "cmb_finite_mode_covariance_verifier_report.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out.relative_to(CODEBASE_ROOT)}")
    return report, proj


def write_multiplier_table(proj):
    out = RESULTS_DIR / "cmb_finite_mode_multiplier_table.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ell", "a_ell", "m_ell", "a_ell_times_m_ell", "qualitative_role"])
        for ell, a_e, m_e in zip(proj.ells, proj.a_ell, proj.m_ell):
            if m_e < 0.3:
                role = "strong_suppression"
            elif m_e < 0.6:
                role = "partial_suppression"
            elif m_e < 0.9:
                role = "mild_suppression"
            elif m_e <= 1.1:
                role = "near_standard"
            elif m_e <= 1.3:
                role = "mild_rebound"
            else:
                role = "strong_rebound"
            w.writerow([int(ell), f"{float(a_e):.6e}", f"{float(m_e):.6f}", f"{float(a_e * m_e):.6e}", role])
    print(f"Wrote {out.relative_to(CODEBASE_ROOT)}")


def write_toy_data_comparison(proj):
    """Toy diagonal chi^2 comparison.

    Constructs a 'toy observed' low-ell spectrum that mimics the Planck low-ell
    suppression pattern qualitatively (quadrupole and octupole low, neighboring
    multipoles rebound, higher ell standard). Compares against std reference
    (m_ell = 1) and projected (m_ell = optimized) via the diagonal chi^2.

    This is a toy comparison only — it has no Planck content and is not a
    public-data likelihood. See Paper 19 v0.2 §6 + §10 audit-box.
    """
    import math
    # Toy observed pattern: low quadrupole + octupole, near-standard elsewhere
    # (these are toy multipliers applied to the reference, not Planck data)
    obs_pattern = {2: 0.30, 3: 0.55, 4: 0.85, 5: 1.20, 6: 1.10}
    # Toy diagonal errors (constant fraction of reference; ad hoc, not cosmic variance)
    sigma_frac = 0.18

    D_std = proj.a_ell * proj.ells * (proj.ells + 1) / (2 * proj.ells + 1)  # back-recover D_ell
    D_obs = []
    sigma = []
    for ell, d in zip(proj.ells, D_std):
        mult = obs_pattern.get(int(ell), 1.0)
        D_obs.append(float(mult * d))
        sigma.append(float(sigma_frac * d))

    chi2_std = sum(((d_obs - d_std) / s) ** 2 for d_obs, d_std, s in zip(D_obs, D_std, sigma))
    D_proj = proj.a_ell * proj.m_ell * proj.ells * (proj.ells + 1) / (2 * proj.ells + 1)
    chi2_proj = sum(((d_obs - d_proj) / s) ** 2 for d_obs, d_proj, s in zip(D_obs, D_proj, sigma))

    out = RESULTS_DIR / "cmb_finite_mode_toy_data_comparison.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value"])
        w.writerow(["chi2_std", f"{chi2_std:.4f}"])
        w.writerow(["chi2_projected", f"{chi2_proj:.4f}"])
        w.writerow(["delta_chi2", f"{chi2_std - chi2_proj:.4f}"])
        w.writerow(["S_proj_over_S_std", f"{proj.ratio:.6e}"])
        w.writerow(["n_multipoles", str(len(proj.ells))])
        w.writerow(["theta_c_deg", str(THETA_C_DEG)])
        w.writerow(["lambda_pressure", str(LAMBDA_PRESSURE)])
        w.writerow([])
        w.writerow(["# Toy diagonal comparison, not a Planck likelihood result."])
        w.writerow(["# Paper 19 v0.2 §6 reports different specific numerics from a"])
        w.writerow(["# different toy input pattern; both are honest at C1+."])
    print(f"Wrote {out.relative_to(CODEBASE_ROOT)}")
    return chi2_std, chi2_proj


def main():
    report, proj = write_verifier_report()
    write_multiplier_table(proj)
    chi2_std, chi2_proj = write_toy_data_comparison(proj)

    print()
    print("=" * 60)
    print(f"Verifier status: {report['verifier_status']}")
    print(f"Bank checks: {report['bank_checks_passed']}/{report['bank_check_count']} PASS")
    print(f"S_proj / S_std: {proj.ratio:.4e}")
    print(f"Toy chi^2 std: {chi2_std:.2f}")
    print(f"Toy chi^2 projected: {chi2_proj:.2f}")
    print(f"Toy delta chi^2: {chi2_std - chi2_proj:.2f}")
    print(f"Quadrupole m_2: {float(proj.m_ell[0]):.4f}")
    print("=" * 60)

    return 0 if report["all_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
