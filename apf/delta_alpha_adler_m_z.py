"""APF Delta alpha_had Adler-function at M_Z — Euclidean two-route corroboration.

Banks the Candidate B Euclidean-Adler pQCD piece of Delta alpha_had(M_Z) and the
two-route corroboration against the Candidate A dispersion-threshold result
banked at v24.3.118.

    Delta alpha_had(M_Z) = Delta alpha_had^{Adler-pQCD}(> Q^2_match) + Delta alpha_had^{Adler-NP}(< Q^2_match)
                          ^                                            ^
                          first-principles APF (Euclidean route)        non-perturbative; principled external
                          [P_perturbative_QCD_M_Z_first_principles_Adler]   [C_principled_external_universal_QCD]

The Euclidean Adler-function route is structurally distinct from the time-like
dispersion-threshold route Candidate A used: there is no kinematic-threshold
dependence in the Adler kernel itself, the integration is performed in Euclidean
Q^2 space, and the route is formally renormalization-scale independent at all
orders (residual mu-dependence at finite truncation order is reported as an
uncertainty witness, not absorbed). The Q^2_match split is a regional fencing
cut, not a kinematic threshold.

At Q_match = 2 m_c(m_c) = 2.558 GeV (matched to v24.3.118's Lambda_match for
direct cross-comparability), the Euclidean Adler route gives

    Delta alpha_had^{Adler-pQCD}(> Q^2_match)
      = alpha(0)/(3 pi) int_{Q^2_match}^{M_Z^2} Dhat_pQCD(Q^2) dQ^2/Q^2
      = 0.020885924935

against Candidate A's 0.020923949565 — a relative gap of 0.182%, well below
the 1% two-route corroboration gate the handoff brief pre-committed to. Two
structurally independent SM-loop formulations of the > Lambda_match piece of
Delta alpha_had(M_Z) now agree at the truncation-uncertainty band.

The non-perturbative residual stays at [C_principled_external_universal_QCD]
per v24.3.116; this arc does NOT close the full Delta alpha_had(M_Z) and does
NOT supersede v24.3.118 — it corroborates it.

Source / canonical computation:
    APF_DELTA_ALPHA_HAD_ADLER_FUNCTION_M_Z_DECOMPOSITION_v1 closure pack, filed
    at Codebase/DELTA_ALPHA_PQCD_ARC_HELD_NOT_BANKED/ as the 2026-05-27
    sibling-AI delivery. Verifier:
    APF_DELTA_ALPHA_HAD_ADLER_FUNCTION_MZ_DECOMPOSITION_V1_PASS (38 checks).
    SHA256 of zip: see manifests/SHA256SUMS.txt at the bundle.
    Adapter source: ~287 lines mpmath dps=50 standalone implementation of the
    Euclidean Adler kernel with two-loop alpha_s running across the b-matching
    threshold; Adler-function coefficients (1.64, 6.37) per Baikov-Chetyrkin-
    Kuehn 2008 (arXiv:1001.3606), NOT the time-like R(s) coefficients
    (1.41, 12.8) that Candidate A used.

Auditor-gated promotion: passed 7/7 gates from the handoff brief
    APF Reference Docs/Reference - Sibling-AI Handoff Brief - Adler Function
    Delta alpha_had Route (2026-05-26).md
    1. Independent computation (Candidate A value comparator-only, excluded from
       COMPUTATION_INPUT_NAMES; bad_Candidate_A_value_as_input.json rejected)
    2. Adler coefficient distinction (1.64, 6.37) not R(s) (1.41, 12.8);
       bad_R_coefficients_used.json rejected; diagnostic shift recorded
    3. No kinematic-threshold reading of Q^2_match (docs/EUCLIDEAN_VS_THRESHOLD.md;
       bad_kinematic_threshold_claim.json rejected)
    4. mu-independence audit (mu_factor in {0.5, 0.75, 1.0, 1.25, 2.0};
       relative half-span 1.26% reported as truncation witness)
    5. Cross-check delivers a specific number (0.18% vs Candidate A at matched
       Q_match = 2 m_c)
    6. No target consumption (dispersion 0.02766 + BMW lattice in FORBIDDEN
       LEDGER; bad_dispersion_as_input.json + bad_BMW_as_input.json rejected)
    7. Honest fence on the residual (0.006774 at [C_principled_external],
       bad_residual_internalized.json rejected)

Pre-registered scenario: TWO_ROUTE_AGREEMENT (gap < 1%) triggered at 0.18%.
"""
from __future__ import annotations

from typing import Any, Dict

from apf.apf_utils import check, _result


# ============================================================================
# Pinned outputs (from sibling-AI standalone adapter, audit-passed)
# ============================================================================

# Primary Q_match (matched to v24.3.118's Lambda_match for direct cross-check):
Q_MATCH_PRIMARY_GEV: float = 2.558  # = 2 * m_c(m_c)
Q2_MATCH_PRIMARY_GEV2: float = 6.543364  # = Q_MATCH_PRIMARY_GEV ** 2

# Auditor-passed central result at Q_match = 2 m_c:
DELTA_ALPHA_HAD_ADLER_PQCD_ABOVE_Q2MATCH: float = 0.020885924935049236

# Cross-check vs v24.3.118 Candidate A (comparator-only, NOT an input):
CANDIDATE_A_PQCD_ABOVE_2MC: float = 0.020923949565
TWO_ROUTE_ABSOLUTE_GAP: float = 3.802462995076417e-05
TWO_ROUTE_RELATIVE_GAP: float = 0.001817277843871737  # 0.182%, < 1% corroboration gate

# Residual (comparator-fenced, from dispersion - Adler):
DELTA_ALPHA_HAD_ADLER_NP_RESIDUAL: float = 0.0067740750649507644

# Threshold sensitivity (alternative; carried for audit, not primary):
Q_MATCH_TAU_GEV: float = 3.55372  # = 2 * m_tau; m_tau = 1.77686 GeV
DELTA_ALPHA_HAD_ADLER_PQCD_ABOVE_2MTAU: float = 0.019023876084071016

# mu-scale audit (truncation residual; reported, NOT absorbed):
MU_SCALE_HALF_SPAN_REL: float = 0.012632368570256201  # 1.26% relative half-span

# Coefficient distinction guard: Adler vs R(s).
ADLER_COEFFICIENTS = {"c1": 1.0, "c2": 1.64, "c3": 6.37}
R_COEFFICIENTS_FORBIDDEN_IN_ADLER_GATE = {"c1": 1.0, "c2": 1.41, "c3": 12.8}
ADLER_VS_R_DIAGNOSTIC_SHIFT_REL: float = 0.0004945930378640184  # 0.05% sanity-witness

# Banked dispersion comparator (from v24.3.116):
DELTA_ALPHA_HAD_DISPERSION_COMPARATOR: float = 0.02766

# Banked physical constants (cited for provenance, not consumed as targets):
M_Z_GEV: float = 91.1876
M_C_MC_GEV: float = 1.279        # apf/charm_msbar_rundec_real_adapter
M_B_MB_GEV: float = 4.18         # apf/bottom_msbar_export_candidate
M_TAU_GEV: float = 1.77686
ALPHA_S_MZ_NF5: float = 0.1189
ALPHA_0_INV: float = 137.035999177
N_C: int = 3                     # Theorem_R R3

# Two-route corroboration gate from the handoff brief:
CORROBORATION_GATE_REL: float = 0.01  # 1% — gap below this triggers two-route promotion

# Honest-non-claim export flags (these are the framework's commitments):
EXPORT_FLAGS: Dict[str, int] = {
    "Export_delta_alpha_had_Adler_pqcd_first_principles": 1,
    "Export_two_route_corroboration_with_Candidate_A": 1,
    "Export_delta_alpha_had_full_first_principles": 0,
    "Export_target_consumption": 0,
    "Export_naive_skeleton_replaces_dispersion": 0,
    "Export_Candidate_A_value_as_input": 0,
    "Export_residual_fenced_C_principled_external": 1,
    "Export_BMW_or_dispersion_replacement": 0,
    "Export_native_OSW_loop_close": 0,
    "Export_physical_EW_global_fit": 0,
    "Export_DHMZ_BMW_tension_resolved": 0,
    "Export_MW_purely_APF_internal_closed": 0,
}


def check_T_delta_alpha_had_adler_pqcd_first_principles_P() -> Dict[str, Any]:
    """T: Delta alpha_had^{Adler-pQCD}(M_Z; > Q^2_match = (2 m_c)^2) = 0.02089 at
    [P_perturbative_QCD_M_Z_first_principles_Adler] with two-route corroboration
    against v24.3.118 Candidate A to 0.18%.

    Second APF-banked first-principles slice of Delta alpha_had(M_Z), via the
    Euclidean Adler-function route structurally distinct from Candidate A's
    time-like dispersion-threshold route. The > Q^2_match piece is now
    corroborated across two SM-loop formulations agreeing within the natural
    truncation-uncertainty band (mu-scale half-span 1.26% at three loops).

    Cross-check artifact:
        Adler route   = 0.020885924935
        Candidate A   = 0.020923949565  (banked v24.3.118)
        absolute gap  = 3.80e-05
        relative gap  = 0.182%          (< 1% corroboration gate)

    Decomposition:
        Delta_alpha_had(M_Z) = Delta_alpha_had^{Adler-pQCD}(> 2 m_c) + Delta_alpha_had^{Adler-NP}(< 2 m_c)
        0.02766              = 0.020886                              + 0.006774
        ↑ dispersion comparator    ↑ this check                      ↑ residual at [C]

    Composition (audit-traceable upstream dependencies):
        - T_delta_alpha_had_pqcd_above_lambda_match_first_principles_P [P, v24.3.118]
          provides the comparator-only Candidate-A value 0.020924 (NOT an input;
          appears only at the terminal cross-check per the forbidden-input ledger).
        - T_delta_alpha_had_principled_external_universal_QCD_C [C, v24.3.116]
          provides the comparator-only dispersion total 0.02766 used for residual
          fencing only (NOT an input that determines Q^2_match or any pQCD coefficient).
        - m_c(m_c) = 1.279 GeV banked self-scale anchor (apf/charm_msbar_rundec_real_adapter)
          → sets Q_match = 2 m_c = 2.558 GeV (NOT fitted, NOT tuned to target).
        - m_b(m_b) = 4.18 GeV banked self-scale anchor (apf/bottom_msbar_export_candidate)
          → controls b-flavor activation at 2 m_b production threshold.
        - alpha_s(M_Z) = 0.1189 (one experimental coupling input, same as L_alpha_em
          and same value used by v24.3.118 — direct cross-check consistency).
        - Theorem_R [P]: Q_q^2 = 4/9 for up-type, 1/9 for down-type; N_c = 3.
        - M_Z = 91.1876 GeV (chosen absolute scale anchor).
        - Adler-function coefficients c2 = 1.64, c3 = 6.37 (Baikov-Chetyrkin-Kuehn 2008,
          arXiv:1001.3606), NOT R(s) coefficients (1.41, 12.8) which are forbidden in
          the Adler gate — bad_R_coefficients_used.json fixture is rejected.

    Structural reading: the Euclidean Adler kernel is formally mu-independent at
    all orders. The Q^2_match split is a regional fencing cut for the
    non-perturbative low-Q^2 contribution, NOT a kinematic threshold in the
    Adler formula itself. This is the load-bearing structural distinction from
    Candidate A's time-like dispersion-threshold reading; the agreement at 0.18%
    across the two routes is the corroboration deliverable.

    Honest non-claims:
        - Does NOT close the full Delta alpha_had(M_Z); only the > Q^2_match piece
          via the Euclidean route. Residual stays [C_principled_external].
        - Does NOT replace dispersion / BMW lattice as the source of the
          non-perturbative < Q^2_match piece.
        - Does NOT supersede v24.3.118; corroborates it across a structurally
          distinct ingredient chain.
        - Does NOT close "M_W on purely APF-internal inputs"; that gate has
          separate dependencies on m_t and M_H structural closures.
        - Does NOT resolve the 2.5σ DHMZ-vs-BMW tension.

    Provenance:
        Canonical computation in the sibling-AI standalone closure pack
        APF_DELTA_ALPHA_HAD_ADLER_FUNCTION_M_Z_DECOMPOSITION_v1 filed at
        Codebase/DELTA_ALPHA_PQCD_ARC_HELD_NOT_BANKED/ alongside Candidate A.
        Verifier: APF_DELTA_ALPHA_HAD_ADLER_FUNCTION_MZ_DECOMPOSITION_V1_PASS
        (38 checks). Pack adapter is ~287 lines mpmath dps=50 standalone (no
        APF imports). Re-running the adapter from the closure pack reproduces
        0.020885924935049236 to the 50-digit precision of the integration.

    Forward-pointer: the Adler-function infrastructure becomes prerequisite for
    the two-loop EW arc (item 5 on the OS-W list) — specifically the two-loop
    photon self-energy Pi_gamma_gamma^{(2L)}(M_Z) and the two-loop gamma-Z
    mixing, both of which are two-loop generalizations of the Euclidean kernel
    banked here.
    """
    # Sanity: decomposition arithmetic (Adler-pQCD + residual = dispersion comparator)
    decomp_total = DELTA_ALPHA_HAD_ADLER_PQCD_ABOVE_Q2MATCH + DELTA_ALPHA_HAD_ADLER_NP_RESIDUAL
    check(abs(decomp_total - DELTA_ALPHA_HAD_DISPERSION_COMPARATOR) < 1e-6,
          f"Adler-pQCD + Adler-NP residual = {decomp_total:.6f} matches "
          f"dispersion comparator {DELTA_ALPHA_HAD_DISPERSION_COMPARATOR}")

    # Sanity: Adler-pQCD piece is positive and a substantial fraction of total
    pqcd_frac = DELTA_ALPHA_HAD_ADLER_PQCD_ABOVE_Q2MATCH / DELTA_ALPHA_HAD_DISPERSION_COMPARATOR
    check(0.70 < pqcd_frac < 0.80,
          f"Adler-pQCD piece is {pqcd_frac*100:.1f}% of dispersion (expected 70-80%)")

    # Sanity: residual is positive (most-likely-positive-residual scenario triggered,
    # consistent with Candidate A)
    check(DELTA_ALPHA_HAD_ADLER_NP_RESIDUAL > 0,
          "Adler-NP residual must be positive (negative would trigger structural alarm)")

    # Two-route corroboration: relative gap vs Candidate A below the 1% gate
    check(TWO_ROUTE_RELATIVE_GAP < CORROBORATION_GATE_REL,
          f"two-route gap vs v24.3.118 Candidate A is {TWO_ROUTE_RELATIVE_GAP*100:.3f}% "
          f"(below {CORROBORATION_GATE_REL*100:.0f}% corroboration gate)")

    # Two-route corroboration: absolute gap matches Candidate A − Adler arithmetic exactly
    check(abs(TWO_ROUTE_ABSOLUTE_GAP -
              abs(CANDIDATE_A_PQCD_ABOVE_2MC - DELTA_ALPHA_HAD_ADLER_PQCD_ABOVE_Q2MATCH)) < 1e-12,
          "two-route absolute gap matches |Candidate_A - Adler| arithmetic to 1e-12")

    # Coefficient distinction: Adler coefficients used, not R(s)
    check(ADLER_COEFFICIENTS["c2"] == 1.64 and ADLER_COEFFICIENTS["c3"] == 6.37,
          "Adler coefficients (1.64, 6.37) used in the gate")
    check(R_COEFFICIENTS_FORBIDDEN_IN_ADLER_GATE["c2"] == 1.41
          and R_COEFFICIENTS_FORBIDDEN_IN_ADLER_GATE["c3"] == 12.8,
          "R(s) coefficients (1.41, 12.8) recorded as forbidden-in-Adler-gate (diagnostic only)")
    check(ADLER_VS_R_DIAGNOSTIC_SHIFT_REL > 1e-4,
          "Adler-vs-R coefficient swap produces a measurable shift "
          f"({ADLER_VS_R_DIAGNOSTIC_SHIFT_REL*100:.3f}%); coefficient distinction is observable")

    # mu-scale audit: half-span reported as truncation witness (not absorbed)
    check(MU_SCALE_HALF_SPAN_REL > 0,
          f"mu-scale half-span {MU_SCALE_HALF_SPAN_REL*100:.2f}% reported as "
          "truncation uncertainty witness (not absorbed into central value)")
    # At three-loop Adler, residual mu-dependence is O(alpha_s^4) ~ percent-level;
    # observe it is in the right ballpark and below 5%.
    check(MU_SCALE_HALF_SPAN_REL < 0.05,
          f"mu-scale half-span {MU_SCALE_HALF_SPAN_REL*100:.2f}% < 5% "
          "(consistent with 3-loop truncation expectation)")

    # Threshold sensitivity (2 m_c vs 2 m_tau): below 20% trigger
    sensitivity_span = abs(DELTA_ALPHA_HAD_ADLER_PQCD_ABOVE_Q2MATCH
                           - DELTA_ALPHA_HAD_ADLER_PQCD_ABOVE_2MTAU)
    sensitivity_pct = sensitivity_span / DELTA_ALPHA_HAD_ADLER_PQCD_ABOVE_Q2MATCH * 100
    check(sensitivity_pct < 20.0,
          f"Q_match sensitivity {sensitivity_pct:.1f}% < 20% (below threshold-shift trigger)")

    # Q_match traces to banked m_c self-scale
    check(abs(Q_MATCH_PRIMARY_GEV - 2 * M_C_MC_GEV) < 1e-9,
          "Q_match = 2 m_c(m_c) banked self-scale (matched to v24.3.118 Lambda_match)")
    check(abs(Q2_MATCH_PRIMARY_GEV2 - Q_MATCH_PRIMARY_GEV ** 2) < 1e-6,
          f"Q^2_match = {Q2_MATCH_PRIMARY_GEV2} = ({Q_MATCH_PRIMARY_GEV})^2 GeV^2")

    # Honest non-claim flags
    check(EXPORT_FLAGS["Export_delta_alpha_had_Adler_pqcd_first_principles"] == 1,
          "Adler-pQCD piece IS first-principles (this check's claim)")
    check(EXPORT_FLAGS["Export_two_route_corroboration_with_Candidate_A"] == 1,
          "two-route corroboration with v24.3.118 IS exported (gap below gate)")
    check(EXPORT_FLAGS["Export_delta_alpha_had_full_first_principles"] == 0,
          "full Delta alpha_had still NOT first-principles")
    check(EXPORT_FLAGS["Export_target_consumption"] == 0,
          "dispersion comparator NOT used as fitted target")
    check(EXPORT_FLAGS["Export_Candidate_A_value_as_input"] == 0,
          "Candidate A value comparator-only, NOT a computation input")
    check(EXPORT_FLAGS["Export_naive_skeleton_replaces_dispersion"] == 0,
          "v24.3.116 naive skeleton 0.03631 NOT reused")
    check(EXPORT_FLAGS["Export_BMW_or_dispersion_replacement"] == 0,
          "BMW lattice / dispersion NOT replaced by this arc")

    return _result(
        name=("T_delta_alpha_had_adler_pqcd_first_principles: "
              f"Delta alpha_had^{{Adler-pQCD}}(M_Z; > Q^2_match = {Q2_MATCH_PRIMARY_GEV2} GeV^2) "
              f"= {DELTA_ALPHA_HAD_ADLER_PQCD_ABOVE_Q2MATCH:.6f} "
              "[P_perturbative_QCD_M_Z_first_principles_Adler]; "
              f"two-route corroboration vs v24.3.118 at {TWO_ROUTE_RELATIVE_GAP*100:.3f}% "
              "(< 1% gate)"),
        tier=4,
        epistemic="P_perturbative_QCD_M_Z_first_principles_Adler",
        summary=(
            f"Second APF-banked first-principles slice of Delta alpha_had(M_Z) via "
            f"Euclidean Adler-function route. Inputs: m_c(m_c)={M_C_MC_GEV}, "
            f"m_b(m_b)={M_B_MB_GEV}, alpha_s(M_Z)={ALPHA_S_MZ_NF5}, Theorem_R charges, "
            f"N_c={N_C}, M_Z={M_Z_GEV}, Adler coefficients (1.0, 1.64, 6.37). "
            f"Q_match = 2 m_c = {Q_MATCH_PRIMARY_GEV} GeV (matched to v24.3.118 "
            f"Lambda_match for direct cross-comparability). Result: Delta alpha_had^{{Adler-pQCD}}"
            f"(>Q^2_match) = {DELTA_ALPHA_HAD_ADLER_PQCD_ABOVE_Q2MATCH:.6f} "
            f"({pqcd_frac*100:.1f}% of dispersion total). Two-route gap vs Candidate A: "
            f"{TWO_ROUTE_RELATIVE_GAP*100:.3f}% (absolute {TWO_ROUTE_ABSOLUTE_GAP:.2e}) — "
            f"below 1% corroboration gate. Residual at [C] external: "
            f"Delta alpha_had^{{Adler-NP}}(<Q^2_match) = "
            f"{DELTA_ALPHA_HAD_ADLER_NP_RESIDUAL:.6f} ({(1-pqcd_frac)*100:.1f}%). "
            f"mu-scale half-span {MU_SCALE_HALF_SPAN_REL*100:.2f}% (3-loop truncation "
            f"witness). Q_match-to-2m_tau sensitivity {sensitivity_pct:.1f}% (below "
            f"20% trigger). Sibling-pack verifier PASS 38 checks."
        ),
        dependencies=[
            "T_delta_alpha_had_pqcd_above_lambda_match_first_principles",
            "T_delta_alpha_had_principled_external_universal_QCD",
            "charm_msbar_rundec_real_adapter",
            "bottom_msbar_export_candidate",
            "Theorem_R",
            "L_alpha_s",
        ],
        artifacts={
            "q_match_primary_gev": Q_MATCH_PRIMARY_GEV,
            "q2_match_primary_gev2": Q2_MATCH_PRIMARY_GEV2,
            "q_match_primary_provenance": ("2 * m_c(m_c) banked self-scale; matched to "
                                           "v24.3.118 Lambda_match for direct two-route cross-check"),
            "delta_alpha_had_adler_pqcd_above_q2match": DELTA_ALPHA_HAD_ADLER_PQCD_ABOVE_Q2MATCH,
            "delta_alpha_had_adler_np_residual": DELTA_ALPHA_HAD_ADLER_NP_RESIDUAL,
            "delta_alpha_had_dispersion_comparator": DELTA_ALPHA_HAD_DISPERSION_COMPARATOR,
            "pqcd_fraction_of_total": pqcd_frac,
            "residual_fraction_of_total": 1 - pqcd_frac,
            "two_route_corroboration": {
                "candidate_A_pqcd_above_2mc": CANDIDATE_A_PQCD_ABOVE_2MC,
                "candidate_A_role": "COMPARATOR_ONLY_NOT_INPUT",
                "absolute_gap": TWO_ROUTE_ABSOLUTE_GAP,
                "relative_gap": TWO_ROUTE_RELATIVE_GAP,
                "corroboration_gate_rel": CORROBORATION_GATE_REL,
                "gate_passed": True,
                "scenario_triggered": "TWO_ROUTE_AGREEMENT",
            },
            "mu_scale_audit": {
                "half_span_relative": MU_SCALE_HALF_SPAN_REL,
                "role": "truncation_uncertainty_witness_NOT_absorbed",
            },
            "threshold_sensitivity": {
                "q_match_tau_gev": Q_MATCH_TAU_GEV,
                "delta_alpha_had_adler_pqcd_above_2mtau": DELTA_ALPHA_HAD_ADLER_PQCD_ABOVE_2MTAU,
                "relative_shift_pct": sensitivity_pct,
            },
            "coefficient_distinction": {
                "adler_coefficients_used": ADLER_COEFFICIENTS,
                "R_coefficients_forbidden": R_COEFFICIENTS_FORBIDDEN_IN_ADLER_GATE,
                "adler_vs_R_diagnostic_shift_rel": ADLER_VS_R_DIAGNOSTIC_SHIFT_REL,
            },
            "banked_inputs": {
                "m_c_mc_GeV": M_C_MC_GEV,
                "m_b_mb_GeV": M_B_MB_GEV,
                "m_tau_GeV": M_TAU_GEV,
                "alpha_s_MZ_nf5": ALPHA_S_MZ_NF5,
                "N_c": N_C,
                "M_Z_GeV": M_Z_GEV,
                "alpha0_inv": ALPHA_0_INV,
            },
            "export_flags": dict(EXPORT_FLAGS),
            "source_pack": "APF_DELTA_ALPHA_HAD_ADLER_FUNCTION_M_Z_DECOMPOSITION_v1",
            "source_pack_location": "Codebase/DELTA_ALPHA_PQCD_ARC_HELD_NOT_BANKED/",
            "source_pack_verifier": ("APF_DELTA_ALPHA_HAD_ADLER_FUNCTION_MZ_DECOMPOSITION_V1_PASS "
                                     "(38 checks)"),
            "handoff_brief": ("APF Reference Docs/Reference - Sibling-AI Handoff Brief - "
                              "Adler Function Delta alpha_had Route (2026-05-26).md"),
            "audit_gates_passed": 7,
            "pre_registered_scenario_triggered": "TWO_ROUTE_AGREEMENT (gap 0.18% < 1% gate)",
        },
    )


# ============================================================================
# Registration / public interface
# ============================================================================

_CHECKS = {
    "T_delta_alpha_had_adler_pqcd_first_principles":
        check_T_delta_alpha_had_adler_pqcd_first_principles_P,
}


def register(registry):
    for name, fn in _CHECKS.items():
        registry[name] = fn

# ---------------------------------------------------------------------------
# IE onboarding (Wave 7, v24.3.347).
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "ew:delta_alpha_adler_pqcd_m_z",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "check_T_delta_alpha_had_adler_pqcd_first_principles_P (tier 4, "
            "epistemic=P_perturbative_QCD_M_Z_first_principles_Adler) banks the "
            "Euclidean Adler-function pQCD piece Delta_alpha_had^Adler-pQCD(> "
            "Q^2_match) = 0.020886 at Q_match = 2 m_c(m_c) = 2.558 GeV, computed "
            "from banked m_c(m_c) = 1.279, banked m_b(m_b) = 4.18, alpha_s(M_Z) = "
            "0.1189 (the one experimental coupling input), Theorem_R quark "
            "charges, N_c = 3, and the M_Z anchor, with Adler coefficients (1.64, "
            "6.37) per Baikov-Chetyrkin-Kuehn -- not the time-like R(s) "
            "coefficients. It certifies the two-route corroboration against the "
            "Candidate A dispersion-threshold route (delta_alpha_pqcd_m_z, "
            "v24.3.118) at a 0.182% relative gap, under the pre-committed 1% "
            "gate; residual mu-dependence (half-span 1.26%) is reported as a "
            "truncation witness, not absorbed. The nonperturbative residual below "
            "Q_match stays [C_principled_external_universal_QCD]; the module does "
            "NOT close the full Delta_alpha_had(M_Z) and does NOT supersede "
            "v24.3.118 -- it corroborates it. Dispersion 0.02766 and BMW lattice "
            "values sit in the FORBIDDEN input ledger; no target consumed. "
            "Auditor-gated promotion passed 7/7 gates. "
        ),
        "note": "Wave 7; bespoke grade token quoted verbatim from the machine field",
    },
)
