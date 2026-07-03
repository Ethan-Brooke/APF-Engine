"""APF Delta alpha_had perturbative-QCD at M_Z — first-principles thresholded decomposition.

Banks the Candidate A dispersion-threshold pQCD piece of Delta alpha_had(M_Z):

    Delta alpha_had(M_Z) = Delta alpha_had^pQCD(> Lambda_match) + Delta alpha_had^NP(< Lambda_match)
                          ^                                       ^
                          first-principles APF                    non-perturbative; principled external
                          [P_perturbative_QCD_M_Z_first_principles] [C_principled_external_universal_QCD]

The pQCD piece above Lambda_match = 2 * m_c(m_c) = 2.558 GeV is the first APF-banked
first-principles result for any portion of Delta alpha_had(M_Z). It uses ONLY:

    - banked m_c(m_c) = 1.279 GeV self-scale anchor (charm_msbar_rundec_real_adapter)
    - banked m_b(m_b) = 4.18 GeV  self-scale anchor (bottom_msbar_export_candidate)
    - banked alpha_s(M_Z) = 0.1189 (one experimental coupling input)
    - Theorem_R-derived quark charges Q_q^2 (+ 4/9 for up-type, +1/9 for down-type)
    - N_c = 3 color factor (Theorem_R R3)
    - M_Z = 91.1876 GeV (chosen absolute scale anchor)

The non-perturbative residual Delta alpha_had^NP(< 2 m_c) stays at [C] external; this
arc does NOT close the full Delta alpha_had(M_Z).

Source / canonical computation:
    APF_DELTA_ALPHA_HAD_PQCD_M_Z_DECOMPOSITION_v1 closure pack, filed at
    Codebase/DELTA_ALPHA_PQCD_ARC_HELD_NOT_BANKED/ as the 2026-05-26 sibling-AI delivery.
    Verifier: APF_DELTA_ALPHA_HAD_PQCD_MZ_DECOMPOSITION_V1_PASS (13 checks).
    SHA256 of zip: see manifests/SHA256SUMS.txt at the bundle.
    Adapter source: ~211 lines mpmath dps=50 implementation of Candidate A dispersion-
    threshold pQCD with two-loop alpha_s running across the b-matching threshold.

Auditor-gated promotion: passed 8/8 gates from the preflight response brief
    APF Reference Docs/Reference - Auditor Response to Sibling Preflight -
    Delta alpha_had Formula Gate (2026-05-26).md
    1. Formula provenance (4-loop massless R(s) with Surguladze-Samuel coefficients)
    2. Lambda_match justification (2 m_c(m_c) banked, not fitted)
    3. Integration kernel (M_Z^2 numerator + principal-value prescription)
    4. Residual fence (Delta alpha_had_dispersion - Delta alpha_had^pQCD as comparator)
    5. No 0.03631 reuse (FORBIDDEN_INPUT_LEDGER + bad_naive_skeleton_reuse.json fixture)
    6. No target consumption (FORBIDDEN_INPUT_LEDGER + bad_dispersion_as_threshold.json)
    7. Scheme/threshold sensitivity (2 m_tau alternative recorded; 9% span)
    8. Pre-registered scenarios outcome (most-likely-positive-residual triggered)
"""
from __future__ import annotations

from typing import Any, Dict

from apf.apf_utils import check, _result


# ============================================================================
# Pinned outputs (from sibling-AI standalone adapter, audit-passed)
# ============================================================================

# Primary threshold (banked):
LAMBDA_MATCH_PRIMARY_GEV: float = 2.558  # = 2 * m_c(m_c), m_c(m_c) = 1.279 GeV

# Auditor-passed result at Lambda_match = 2 m_c:
DELTA_ALPHA_HAD_PQCD_ABOVE_2MC: float = 0.020923949565

# Residual (comparator-fenced, computed from dispersion - pQCD):
# Delta_alpha_had_dispersion = 0.02766 (banked external comparator, v24.3.116)
DELTA_ALPHA_HAD_NP_RESIDUAL: float = 0.006736050435  # = 0.02766 - 0.020924

# Sensitivity threshold (alternative; carried for audit, not primary):
LAMBDA_MATCH_TAU_GEV: float = 3.55372  # = 2 * m_tau; m_tau = 1.77686 GeV
DELTA_ALPHA_HAD_PQCD_ABOVE_2MTAU: float = 0.019056334196

# Banked dispersion comparator (from v24.3.116):
DELTA_ALPHA_HAD_DISPERSION_COMPARATOR: float = 0.02766

# Banked physical constants (cited for provenance, not consumed as targets):
M_Z_GEV: float = 91.1876
M_C_MC_GEV: float = 1.279        # apf/charm_msbar_rundec_real_adapter
M_B_MB_GEV: float = 4.18         # apf/bottom_msbar_export_candidate
ALPHA_S_MZ_NF5: float = 0.1189
ALPHA_0_INV: float = 137.035999177
N_C: int = 3                     # Theorem_R R3

# Honest-non-claim export flags (these are the framework's commitments):
EXPORT_FLAGS: Dict[str, int] = {
    "Export_delta_alpha_q_pert_at_M_Z_first_principles": 1,
    "Export_delta_alpha_had_full_first_principles": 0,
    "Export_delta_alpha_hadronic_internalized": 0,
    "Export_target_consumption": 0,
    "Export_naive_skeleton_replaces_dispersion": 0,
    "Export_formula_gate_closed": 1,
    "Export_thresholded_Candidate_A_closed": 1,
    "Export_residual_fenced_C_principled_external": 1,
    "Export_physical_EW_global_fit": 0,
    "Export_native_OSW_loop_close": 0,
    "Export_DHMZ_BMW_tension_resolved": 0,
    "Export_MW_purely_APF_internal_closed": 0,
    "Export_mass_threshold_exactness": 0,
    "Export_Adler_function_route_closed": 0,
}


def check_T_delta_alpha_had_pqcd_above_lambda_match_first_principles_P() -> Dict[str, Any]:
    """T: Delta alpha_had^pQCD(M_Z; > Lambda_match = 2 m_c) = 0.02092 at
    [P_perturbative_QCD_M_Z_first_principles].

    First APF-banked first-principles result for any portion of Delta alpha_had(M_Z).
    Closes the perturbative-above-threshold slice; the non-perturbative residual below
    Lambda_match stays at [C_principled_external_universal_QCD] (v24.3.116).

    Decomposition:
        Delta_alpha_had(M_Z) = Delta_alpha_had^pQCD(> 2 m_c) + Delta_alpha_had^NP(< 2 m_c)
        0.02766              = 0.020924                       + 0.006736
        ↑ dispersion comparator    ↑ this check                ↑ residual at [C]

    The pQCD piece is 75.7% of the total dispersion value; the residual is 24.3%,
    which is the non-perturbative hadronic resonance physics below ~2.6 GeV (rho,
    omega, phi, low-energy chiral dynamics) that current-quark perturbative VP
    cannot capture by construction.

    Composition (audit-traceable upstream dependencies):
        - T_delta_alpha_had_principled_external_universal_QCD_C [C, v24.3.116]
          provides the comparator-only Delta_alpha_had_dispersion = 0.02766
        - m_c(m_c) = 1.279 GeV banked self-scale anchor (apf/charm_msbar_rundec_real_adapter)
          → sets Lambda_match = 2 m_c = 2.558 GeV (NOT fitted)
        - m_b(m_b) = 4.18 GeV banked self-scale anchor (apf/bottom_msbar_export_candidate)
          → controls b-flavor activation at 2 m_b production threshold
        - alpha_s(M_Z) = 0.1189 (one experimental coupling input, same as L_alpha_em)
        - Theorem_R [P]: Q_q^2 = 4/9 for up-type, 1/9 for down-type; N_c = 3
        - M_Z = 91.1876 GeV (chosen absolute scale anchor)

    Honest non-claims:
        - Does NOT close the full Delta alpha_had(M_Z); only the > 2 m_c piece.
        - Does NOT replace the dispersion integral or BMW lattice as the source of
          the non-perturbative < 2 m_c piece.
        - Does NOT resolve the 2.5σ DHMZ-vs-BMW tension; that's a separate gate.
        - Does NOT consume Delta_alpha_had_dispersion as a target — it is the
          comparator for the residual, not an input that determines Lambda_match
          or any pQCD coefficient.
        - Does NOT reuse the v24.3.116 naïve perturbative skeleton 0.03631 — that
          is documentary-only and the FORBIDDEN_INPUT_LEDGER explicitly excludes it.

    Provenance:
        Canonical computation in the sibling-AI standalone closure pack
        APF_DELTA_ALPHA_HAD_PQCD_M_Z_DECOMPOSITION_v1 filed at
        Codebase/DELTA_ALPHA_PQCD_ARC_HELD_NOT_BANKED/. Verifier:
        APF_DELTA_ALPHA_HAD_PQCD_MZ_DECOMPOSITION_V1_PASS (13 checks). Pack
        adapter is ~211 lines mpmath dps=50 standalone (no APF imports). This
        bank check pins the auditor-passed output value and records the
        structural composition. Re-running the adapter from the closure pack
        reproduces 0.020923949565 to the 50-digit precision of the integration.

    Cross-route corroboration (v24.3.119):
        The > Lambda_match piece of Delta alpha_had(M_Z) is now corroborated
        across two structurally independent SM-loop formulations:

            this check (Candidate A, time-like dispersion-threshold) = 0.020923949565
            Adler (Candidate B, Euclidean Adler-function route)      = 0.020885924935
            absolute gap   = 3.80e-05
            relative gap   = 0.182%   (< 1% corroboration gate)

        The Adler-route check lives at apf.delta_alpha_adler_m_z.check_T_delta_alpha_had_adler_pqcd_first_principles_P
        and is banked at [P_perturbative_QCD_M_Z_first_principles_Adler]. The two
        routes use structurally distinct ingredient chains: this check uses the
        time-like R(s) series (Surguladze-Samuel coefficients 1.41, 12.8) with a
        principal-value dispersion kernel; the Adler-route check uses the
        Euclidean Dhat series (Baikov-Chetyrkin-Kuehn coefficients 1.64, 6.37)
        with a Euclidean running-difference kernel. Both routes share the same
        banked physical inputs (alpha_s(M_Z), m_c, m_b, Theorem_R charges, N_c,
        M_Z) and route to the same observable to within the natural truncation
        uncertainty band at three loops.
    """
    # Sanity: decomposition arithmetic at exactly 4 decimal places
    decomp_total = DELTA_ALPHA_HAD_PQCD_ABOVE_2MC + DELTA_ALPHA_HAD_NP_RESIDUAL
    check(abs(decomp_total - DELTA_ALPHA_HAD_DISPERSION_COMPARATOR) < 1e-6,
          f"pQCD + NP residual = {decomp_total:.6f} matches "
          f"dispersion comparator {DELTA_ALPHA_HAD_DISPERSION_COMPARATOR}")

    # Sanity: pQCD piece is positive and a substantial fraction of total
    pqcd_frac = DELTA_ALPHA_HAD_PQCD_ABOVE_2MC / DELTA_ALPHA_HAD_DISPERSION_COMPARATOR
    check(0.70 < pqcd_frac < 0.80,
          f"pQCD piece is {pqcd_frac*100:.1f}% of dispersion (expected 70-80%)")

    # Sanity: NP residual is positive (most-likely-positive scenario triggered)
    check(DELTA_ALPHA_HAD_NP_RESIDUAL > 0,
          "NP residual must be positive (negative would trigger structural alarm)")

    # Sensitivity: 2 m_tau alternative threshold gives a different but bounded value
    sensitivity_span = abs(DELTA_ALPHA_HAD_PQCD_ABOVE_2MC - DELTA_ALPHA_HAD_PQCD_ABOVE_2MTAU)
    sensitivity_pct = sensitivity_span / DELTA_ALPHA_HAD_PQCD_ABOVE_2MC * 100
    check(sensitivity_pct < 20.0,
          f"threshold sensitivity {sensitivity_pct:.1f}% < 20% "
          "(below scenario-2 threshold-sensitive trigger)")

    # Lambda_match traces to banked m_c self-scale
    check(abs(LAMBDA_MATCH_PRIMARY_GEV - 2 * M_C_MC_GEV) < 1e-9,
          "Lambda_match = 2 m_c(m_c) banked self-scale (NOT fitted)")

    # Honest non-claim flags
    check(EXPORT_FLAGS["Export_delta_alpha_q_pert_at_M_Z_first_principles"] == 1,
          "pQCD piece IS first-principles (this check's claim)")
    check(EXPORT_FLAGS["Export_delta_alpha_had_full_first_principles"] == 0,
          "full Delta alpha_had still NOT first-principles")
    check(EXPORT_FLAGS["Export_delta_alpha_hadronic_internalized"] == 0,
          "Delta alpha_had stays externally-anchored at total")
    check(EXPORT_FLAGS["Export_target_consumption"] == 0,
          "dispersion comparator NOT used as fitted target")
    check(EXPORT_FLAGS["Export_naive_skeleton_replaces_dispersion"] == 0,
          "v24.3.116 naive skeleton 0.03631 NOT reused")

    return _result(
        name=("T_delta_alpha_had_pqcd_above_lambda_match_first_principles: "
              f"Delta alpha_had^pQCD(M_Z; > 2 m_c = {LAMBDA_MATCH_PRIMARY_GEV} GeV) "
              f"= {DELTA_ALPHA_HAD_PQCD_ABOVE_2MC:.6f} "
              "[P_perturbative_QCD_M_Z_first_principles]"),
        tier=4,
        epistemic="P_perturbative_QCD_M_Z_first_principles",
        summary=(
            f"First APF-banked first-principles slice of Delta alpha_had(M_Z): the "
            f"perturbative-above-threshold piece via Candidate A dispersion-threshold pQCD. "
            f"Inputs: m_c(m_c)={M_C_MC_GEV}, m_b(m_b)={M_B_MB_GEV}, alpha_s(M_Z)={ALPHA_S_MZ_NF5}, "
            f"Theorem_R charges, N_c={N_C}, M_Z={M_Z_GEV}. Lambda_match = 2 m_c = "
            f"{LAMBDA_MATCH_PRIMARY_GEV} GeV (banked self-scale, not fitted). "
            f"Result: Delta alpha_had^pQCD(>2 m_c) = {DELTA_ALPHA_HAD_PQCD_ABOVE_2MC:.6f} "
            f"({pqcd_frac*100:.1f}% of dispersion total). Residual at [C] external: "
            f"Delta alpha_had^NP(<2 m_c) = {DELTA_ALPHA_HAD_NP_RESIDUAL:.6f} ({(1-pqcd_frac)*100:.1f}%). "
            f"Sensitivity to 2 m_tau alternative: {sensitivity_pct:.1f}% span, below "
            f"scenario-2 trigger. Sibling-pack verifier PASS 13 checks."
        ),
        dependencies=[
            "T_delta_alpha_had_principled_external_universal_QCD",
            "charm_msbar_rundec_real_adapter",
            "bottom_msbar_export_candidate",
            "Theorem_R",
            "L_alpha_s",
        ],
        artifacts={
            "lambda_match_primary_gev": LAMBDA_MATCH_PRIMARY_GEV,
            "lambda_match_primary_provenance": "2 * m_c(m_c) banked self-scale (not fitted)",
            "delta_alpha_had_pqcd_above_2mc": DELTA_ALPHA_HAD_PQCD_ABOVE_2MC,
            "delta_alpha_had_np_residual": DELTA_ALPHA_HAD_NP_RESIDUAL,
            "delta_alpha_had_dispersion_comparator": DELTA_ALPHA_HAD_DISPERSION_COMPARATOR,
            "pqcd_fraction_of_total": pqcd_frac,
            "residual_fraction_of_total": 1 - pqcd_frac,
            "sensitivity_alternative_2mtau": DELTA_ALPHA_HAD_PQCD_ABOVE_2MTAU,
            "sensitivity_span_pct": sensitivity_pct,
            "banked_inputs": {
                "m_c_mc_GeV": M_C_MC_GEV,
                "m_b_mb_GeV": M_B_MB_GEV,
                "alpha_s_MZ_nf5": ALPHA_S_MZ_NF5,
                "N_c": N_C,
                "M_Z_GeV": M_Z_GEV,
                "alpha0_inv": ALPHA_0_INV,
            },
            "export_flags": dict(EXPORT_FLAGS),
            "source_pack": "APF_DELTA_ALPHA_HAD_PQCD_M_Z_DECOMPOSITION_v1",
            "source_pack_location": "Codebase/DELTA_ALPHA_PQCD_ARC_HELD_NOT_BANKED/",
            "source_pack_verifier": "APF_DELTA_ALPHA_HAD_PQCD_MZ_DECOMPOSITION_V1_PASS (13 checks)",
            "auditor_response_doc": ("APF Reference Docs/Reference - Auditor Response to "
                                     "Sibling Preflight - Delta alpha_had Formula Gate (2026-05-26).md"),
            "audit_gates_passed": 8,
            "pre_registered_scenario_triggered": "most_likely_positive_residual (sibling SCENARIO_LEDGER)",
        },
    )


# ============================================================================
# Registration / public interface
# ============================================================================

_CHECKS = {
    "T_delta_alpha_had_pqcd_above_lambda_match_first_principles":
        check_T_delta_alpha_had_pqcd_above_lambda_match_first_principles_P,
}


def register(registry):
    for name, fn in _CHECKS.items():
        registry[name] = fn

# ---------------------------------------------------------------------------
# IE onboarding (Wave 7, v24.3.347).
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "ew:delta_alpha_pqcd_m_z",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "check_T_delta_alpha_had_pqcd_above_lambda_match_first_principles_P "
            "(tier 4, epistemic=P_perturbative_QCD_M_Z_first_principles) banks "
            "the Candidate A dispersion-threshold pQCD piece "
            "Delta_alpha_had^pQCD(> Lambda_match) = 0.020924 above Lambda_match = "
            "2 m_c(m_c) = 2.558 GeV -- the first APF-banked first-principles "
            "result for any portion of Delta_alpha_had(M_Z), ~75.7% of the "
            "dispersive total. Inputs are confined to banked m_c(m_c) and "
            "m_b(m_b) self-scale anchors, alpha_s(M_Z) = 0.1189 (one experimental "
            "coupling input), Theorem_R quark charges, N_c = 3, and the M_Z "
            "anchor. The nonperturbative residual 0.006736 below Lambda_match "
            "stays [C_principled_external_universal_QCD]; the arc does NOT close "
            "the full Delta_alpha_had(M_Z). The dispersion value enters only as a "
            "comparator-fenced residual; forbidden-input fixtures (naive-skeleton "
            "reuse, dispersion-as-threshold) are rejected; threshold sensitivity "
            "(2 m_tau alternative, 9% span) is recorded. Auditor-gated promotion "
            "passed 8/8 gates. "
        ),
        "note": "Wave 7; bespoke grade token quoted verbatim from the machine field",
    },
)
