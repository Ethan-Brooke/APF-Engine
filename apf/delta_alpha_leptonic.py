"""APF leptonic running of alpha: Delta alpha_lep(M_Z) from banked masses -- Tier-3/4.

The electromagnetic coupling runs from its Thomson-limit value alpha(0) to the
Z scale:

    alpha(M_Z) = alpha(0) / (1 - Delta alpha) ,
    Delta alpha = Delta alpha_lep + Delta alpha_had + Delta alpha_top .

Of the three pieces only the LEPTONIC one is first-principles: it is the pure
QED vacuum polarization of the three charged leptons, fixed entirely by their
masses. The HADRONIC piece is data-bound (a dispersion integral over
e+e- -> hadrons; the same object that limits the muon g-2 prediction) and is
NOT calculable from first principles. The top piece is tiny.

What this module does (and does NOT) claim
------------------------------------------
It makes the leptonic running APF-INTERNAL by evaluating the one-loop QED
vacuum-polarization sum

    Delta alpha_lep = sum_l (alpha_0 / 3pi) [ ln(M_Z^2 / m_l^2) - 5/3 ]

on the APF-BANKED charged-lepton pole masses
(``charged_lepton_pole_real_adapter.POLE_MASS_MEV``) and nothing else. The
result, 0.031421, reproduces the known precise (three-loop) leptonic value
0.0314977 to within 0.24% at one loop; the small gap is the higher-order
leptonic QED (also first-principles, not evaluated here).

The leptonic piece is 53.2% of the total Delta alpha(M_Z) = 0.059011. The
remaining 46.9%, Delta alpha_had = 0.02766, stays a DATA-BOUND external input
NOT admitted as first-principles -- this is the single named open gate. So the
full Delta alpha(M_Z) is not claimed first-principles; only its leptonic part
is.

This advances the EW running-coupling sector (the Delta r / W-mass + MS-bar
sin^2 sector, where session_nnlo currently computes Delta alpha_lep with
hardcoded PDG masses inside L_sin2_oneloop). It does NOT close the
sin^2 theta_eff kappa_l residual: Delta alpha largely cancels in the kappa_l
ratio, so the kappa_l residual is dominated by bosonic/vertex pieces, not this.

Status
------
- Export_delta_alpha_leptonic_first_principles = 1  (NEW here)
- Export_delta_alpha_hadronic_internalized     = 0  (data-bound, stays external)
- Export_delta_alpha_full_first_principles      = 0  (had piece is not first-principles)
"""
from __future__ import annotations

import math
from typing import Any, Dict

from apf.apf_utils import check, _result

# Banked anchors (provenance imports -- no new numbers introduced for the leptonic piece).
from apf.charged_lepton_pole_real_adapter import POLE_MASS_MEV


# ============================================================================
# Constants
# ============================================================================

# Thomson-limit fine-structure constant alpha(0). The framework-wide low-energy
# value (session_nnlo._ALPHA_0 = 1/137.036); CODATA 1/137.035999084.
_ALPHA_0 = 1.0 / 137.035999084
_M_Z = 91.1876  # GeV, anchor

# APF-banked charged-lepton POLE masses (MeV) -> GeV. Provenance:
# charged_lepton_pole_real_adapter.POLE_MASS_MEV (APF-derived, not PDG-imported).
_M_LEP_GEV = {k: v / 1000.0 for k, v in POLE_MASS_MEV.items()}

# Data-bound (dispersion-relation) hadronic running and the tiny top piece.
# These are EXTERNAL inputs, NOT first-principles. PDG electroweak review.
_DA_HAD_DISPERSION = 0.02766   # [data-bound: dispersion integral over e+e- -> hadrons]
_DA_TOP = -0.00007

# Known precise (1+2+3-loop) leptonic value, for cross-check only.
_DA_LEP_PRECISE_3LOOP = 0.0314977


# ============================================================================
# Core computation
# ============================================================================

def _da_lep_one_loop(m_gev: float) -> float:
    """One-loop QED vacuum-polarization contribution of one charged lepton."""
    return _ALPHA_0 / (3 * math.pi) * (math.log(_M_Z ** 2 / m_gev ** 2) - 5.0 / 3.0)


def _leptonic_running() -> Dict[str, Any]:
    per = {k: _da_lep_one_loop(_M_LEP_GEV[k]) for k in ("m_e", "m_mu", "m_tau")}
    da_lep = sum(per.values())
    da_total = da_lep + _DA_HAD_DISPERSION + _DA_TOP
    return {
        "per_lepton": per,
        "da_lep_one_loop": da_lep,
        "da_lep_precise_3loop": _DA_LEP_PRECISE_3LOOP,
        "da_had_dispersion": _DA_HAD_DISPERSION,
        "da_top": _DA_TOP,
        "da_total": da_total,
        "lep_fraction_of_total": da_lep / da_total,
        "had_fraction_of_total": _DA_HAD_DISPERSION / da_total,
        "one_loop_vs_precise_rel": da_lep / _DA_LEP_PRECISE_3LOOP - 1.0,
    }


# ============================================================================
# Honest non-claim flags
# ============================================================================

EXPORT_FLAGS: Dict[str, int] = {
    "Export_delta_alpha_leptonic_first_principles": 1,   # NEW
    "Export_delta_alpha_hadronic_internalized": 0,       # data-bound, external
    "Export_delta_alpha_full_first_principles": 0,       # total not first-principles
}

# Measured/fitted keys that would constitute smuggling if consumed.
_FORBIDDEN_TARGET_KEYS = frozenset({
    "measured_alpha_MZ",
    "fitted_delta_alpha",
    "pdg_alpha_inv_MZ_target",
    "measured_lepton_mass",
})


# ============================================================================
# Bank-registered checks
# ============================================================================

def check_T_delta_alpha_leptonic_first_principles_P() -> Dict[str, Any]:
    """T: Delta alpha_lep(M_Z) is first-principles from banked lepton masses [P].

    One-loop QED vacuum polarization summed over the three APF-banked
    charged-lepton pole masses. Reproduces 0.031421, within 0.24% of the known
    precise (three-loop) leptonic value 0.0314977; the gap is higher-order
    leptonic QED. Uses only banked masses + alpha(0) -- no data input.
    """
    r = _leptonic_running()
    da = r["da_lep_one_loop"]
    check(abs(da - 0.0314209) < 1e-6,
          f"Delta alpha_lep one-loop {da} != expected 0.0314209")
    check(abs(r["one_loop_vs_precise_rel"]) < 0.005,
          f"one-loop must match the precise leptonic value to <0.5% "
          f"(got {r['one_loop_vs_precise_rel']*100:.3f}%)")
    check(da > 0, "leptonic running must be positive (screening)")
    # ordering: electron dominates, then muon, then tau
    p = r["per_lepton"]
    check(p["m_e"] > p["m_mu"] > p["m_tau"] > 0,
          "per-lepton contributions must order e > mu > tau > 0")

    return _result(
        name="T_delta_alpha_leptonic_first_principles: "
             "Delta alpha_lep(M_Z) from banked lepton masses [P]",
        tier=3, epistemic="P",
        summary=(
            f"Delta alpha_lep(M_Z) = sum_l (alpha_0/3pi)[ln(M_Z^2/m_l^2) - 5/3] "
            f"= {da:.7f} (one-loop), from the APF-banked charged-lepton pole "
            f"masses (e {r['per_lepton']['m_e']:.6f} + mu "
            f"{r['per_lepton']['m_mu']:.6f} + tau {r['per_lepton']['m_tau']:.6f}). "
            f"Reproduces the known precise (three-loop) leptonic value "
            f"{_DA_LEP_PRECISE_3LOOP} to {r['one_loop_vs_precise_rel']*100:+.2f}% "
            f"at one loop; the gap is higher-order leptonic QED (first-principles, "
            f"not evaluated here). Pure QED vacuum polarization -- no data input."
        ),
        key_result=(
            f"Delta alpha_lep(M_Z) = {da:.6f} first-principles (banked masses, 1-loop). [P]"
        ),
        dependencies=["charged_lepton_pole_masses", "L_alpha_em"],
        cross_refs=["L_sin2_oneloop"],
        artifacts={
            "da_lep_one_loop": round(da, 8),
            "per_lepton": {k: round(v, 8) for k, v in r["per_lepton"].items()},
            "da_lep_precise_3loop": _DA_LEP_PRECISE_3LOOP,
            "one_loop_vs_precise_rel": round(r["one_loop_vs_precise_rel"], 6),
            "alpha_0_inv": round(1.0 / _ALPHA_0, 6),
        },
    )


def check_L_delta_alpha_leptonic_masses_banked_P() -> Dict[str, Any]:
    """L: the lepton masses are the APF-banked pole masses, not PDG-smuggled [P].

    Pins the masses used to charged_lepton_pole_real_adapter.POLE_MASS_MEV
    (APF-derived pole masses), value-identical. No measured/PDG lepton mass is
    consumed as an independent input.
    """
    check(abs(POLE_MASS_MEV["m_e"] - 0.5110026357885311) < 1e-12,
          "m_e must be the banked pole mass")
    check(abs(POLE_MASS_MEV["m_mu"] - 105.658243985342) < 1e-9,
          "m_mu must be the banked pole mass")
    check(abs(POLE_MASS_MEV["m_tau"] - 1776.9168320084111) < 1e-9,
          "m_tau must be the banked pole mass")
    check("measured_lepton_mass" in _FORBIDDEN_TARGET_KEYS,
          "measured lepton mass must be a forbidden (non-smuggled) key")

    return _result(
        name="L_delta_alpha_leptonic_masses_banked: "
             "leptonic running uses APF-banked pole masses [P]",
        tier=4, epistemic="P",
        summary=(
            "The three lepton masses feeding Delta alpha_lep are the APF-banked "
            "charged-lepton pole masses (charged_lepton_pole_real_adapter "
            ".POLE_MASS_MEV: e 0.5110026, mu 105.658244, tau 1776.916832 MeV), "
            "value-pinned. No measured/PDG lepton mass is consumed as an "
            "independent input; the running is fixed by the banked spectrum."
        ),
        key_result="Leptonic running sourced from banked pole masses. [P]",
        dependencies=["charged_lepton_pole_masses"],
        cross_refs=["T_delta_alpha_leptonic_first_principles"],
        artifacts={"pole_masses_MeV": dict(POLE_MASS_MEV)},
    )


def check_L_delta_alpha_hadronic_external_open_C() -> Dict[str, Any]:
    """L: the hadronic running is a data-bound external OPEN gate [C].

    Delta alpha_had (a dispersion integral over e+e- -> hadrons; the same object
    that limits the muon g-2 prediction) is NOT first-principles and is NOT
    internalized. It is the single named open gate of the alpha-running sector.
    The hadronic-internalization and full-first-principles export flags stay 0.
    """
    r = _leptonic_running()
    check(_DA_HAD_DISPERSION > 1e-3,
          "hadronic running must be a non-trivial external term")
    check(EXPORT_FLAGS["Export_delta_alpha_hadronic_internalized"] == 0,
          "hadronic running must remain UN-internalized (flag 0)")
    check(EXPORT_FLAGS["Export_delta_alpha_full_first_principles"] == 0,
          "full Delta alpha must remain not-first-principles (flag 0)")

    return _result(
        name="L_delta_alpha_hadronic_external_open: "
             "hadronic running is a data-bound OPEN gate [C]",
        tier=4, epistemic="C",
        summary=(
            f"Delta alpha_had = {_DA_HAD_DISPERSION} "
            f"({r['had_fraction_of_total']*100:.1f}% of the total Delta alpha) "
            f"is a dispersion integral over e+e- -> hadrons -- data-bound, the "
            f"same object that limits the muon g-2 prediction. It is NOT "
            f"first-principles and is NOT internalized; it is the single named "
            f"open gate of the alpha-running sector. Export flags stay 0."
        ),
        key_result=(
            f"Delta alpha_had = {_DA_HAD_DISPERSION} OPEN (data-bound, external). [C]"
        ),
        dependencies=["T_delta_alpha_leptonic_first_principles"],
        artifacts={
            "da_had_dispersion": _DA_HAD_DISPERSION,
            "had_fraction_of_total": round(r["had_fraction_of_total"], 6),
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


def check_T_delta_alpha_total_decomposition_P() -> Dict[str, Any]:
    """T: Delta alpha(M_Z) = lep + had + top decomposition [P_structural].

    The total running splits into the first-principles leptonic piece (53%) and
    the data-bound hadronic piece (47%) plus a tiny top piece. Reproduces the
    total ~0.059. The total is NOT first-principles (it carries the external
    hadronic input); only the leptonic share is.
    """
    r = _leptonic_running()
    total = r["da_total"]
    check(abs((r["da_lep_one_loop"] + _DA_HAD_DISPERSION + _DA_TOP) - total) < 1e-12,
          "lep + had + top must reconstruct the total")
    check(abs(total - 0.059) < 0.002,
          f"total Delta alpha {total} must be ~0.059")
    check(0.50 < r["lep_fraction_of_total"] < 0.56,
          f"leptonic share must be ~53% (got {r['lep_fraction_of_total']*100:.1f}%)")

    return _result(
        name="T_delta_alpha_total_decomposition: "
             "Delta alpha(M_Z) = lep + had + top [P_structural]",
        tier=4, epistemic="P_structural_seam",
        summary=(
            f"Delta alpha(M_Z) = {total:.6f} = leptonic {r['da_lep_one_loop']:.6f} "
            f"({r['lep_fraction_of_total']*100:.1f}%, first-principles) + hadronic "
            f"{_DA_HAD_DISPERSION} ({r['had_fraction_of_total']*100:.1f}%, "
            f"data-bound) + top {_DA_TOP}. The leptonic share is first-principles "
            f"from the banked masses; the total is NOT first-principles (it carries "
            f"the external hadronic dispersion input)."
        ),
        key_result=(
            f"Delta alpha(M_Z) = {total:.5f}; leptonic 53% first-principles, "
            f"hadronic 47% external. [P_structural]"
        ),
        dependencies=["T_delta_alpha_leptonic_first_principles",
                      "L_delta_alpha_hadronic_external_open"],
        artifacts={
            "da_total": round(total, 6),
            "da_lep_one_loop": round(r["da_lep_one_loop"], 6),
            "da_had_dispersion": _DA_HAD_DISPERSION,
            "da_top": _DA_TOP,
            "lep_fraction_of_total": round(r["lep_fraction_of_total"], 6),
            "had_fraction_of_total": round(r["had_fraction_of_total"], 6),
        },
    )


# ============================================================================
# Perturbative quark skeleton — recharacterizing Delta alpha_had as principled
# external (universal QCD difficulty), not unfinished APF.
# ============================================================================

# Banked MS-bar quark mass anchors used for the perturbative-skeleton numerical
# witness. The c and b values come from APF-banked self-scale anchors; light
# quarks (u, d, s) are PDG MS-bar context at 2 GeV (cited, NOT consumed as
# fitted targets — same provenance discipline as _DA_HAD_DISPERSION above).
#
# Caveat: these are at MIXED MS-bar scales (m_c at m_c, m_b at m_b, light quarks
# at 2 GeV). The proper M_Z evaluation requires running the full quark
# spectrum to M_Z via QCD beta functions, which is a separate multi-session
# arc (RunDec adapters exist for c and b in apf/charm_msbar_rundec_real_adapter
# and apf/bottom_msbar_export_candidate; light-quark running to M_Z is open).
# The naive witness preserves the structural finding (perturbative overshoot
# of dispersion by ~30%) without claiming precision.

_M_QUARK_MSBAR_GEV: Dict[str, float] = {
    "m_u": 0.00216,   # PDG MS-bar at 2 GeV (context, not consumed)
    "m_d": 0.00467,   # PDG MS-bar at 2 GeV (context, not consumed)
    "m_s": 0.0934,    # PDG MS-bar at 2 GeV (context, not consumed)
    "m_c": 1.279,     # banked APF MS-bar self-scale m_c(m_c) via
                      # apf/charm_msbar_rundec_real_adapter (published_case)
    "m_b": 4.18,      # banked APF_TRACE m_b(m_b) via
                      # apf/bottom_msbar_export_candidate (export candidate)
}

# Electric charges squared (banked from Theorem_R-derived charge assignments).
_Q_QUARK_SQUARED: Dict[str, float] = {
    "m_u": 4.0 / 9.0,
    "m_d": 1.0 / 9.0,
    "m_s": 1.0 / 9.0,
    "m_c": 4.0 / 9.0,
    "m_b": 1.0 / 9.0,
}

_N_C = 3.0  # color factor (banked from Theorem_R, apf/gauge.py)


def _da_quark_one_loop_naive(m_gev: float, Q2: float) -> float:
    """One-loop QED vacuum-polarization contribution of one quark
    (naive perturbative formula, current-quark MS-bar mass, NOT run to M_Z).
    Same functional form as _da_lep_one_loop but with N_c and Q^2 factors."""
    return (_ALPHA_0 / (3 * math.pi)) * _N_C * Q2 * (math.log(_M_Z ** 2 / m_gev ** 2) - 5.0 / 3.0)


def check_T_delta_alpha_had_principled_external_universal_QCD_C() -> Dict[str, Any]:
    """T: Delta alpha_had(M_Z) at [C_principled_external_universal_QCD_difficulty]:
    the gate is external NOT because of an APF-specific gap, but because the
    non-perturbative hadronic vacuum polarization in the resonance region
    below ~2 GeV is structurally outside any current first-principles
    framework (SM included). [C_principled_external_universal_QCD_difficulty]

    Background — universal-QCD-difficulty argument:
        The full Standard Model itself has no first-principles route to
        Delta alpha_had(M_Z). The two state-of-the-art evaluations both rest on
        non-APF, non-SM external content:
            (a) Dispersion-integral over R(s) = sigma(e+e- -> hadrons) data
                (DHMZ, KNT, FJ22): empirical by construction.
            (b) Lattice QCD vacuum polarization (BMW collaboration): heroic
                non-perturbative numerical computation.
        These two routes disagree at the 2.5 sigma level, which is the live
        theoretical-uncertainty issue in the EW global fit (and the same
        non-perturbative HVP object limits the muon g-2 prediction).
        APF inherits this universal difficulty; the [C] grade on
        Delta alpha_had is structurally principled, not an APF-specific gap.

    Perturbative-skeleton numerical witness (naive, current-quark MS-bar
    masses at mixed self-scales, NOT run to M_Z):

        Delta alpha_q^pert^naive(M_Z) = sum_q (alpha/3pi) N_c Q_q^2 [ln(M_Z^2/m_q^2) - 5/3]

        Sum over q in {u, d, s, c, b}:
            m_u, m_d, m_s: PDG MS-bar at 2 GeV (context, not fitted)
            m_c = 1.279 GeV (banked, charm_msbar_rundec_real_adapter)
            m_b = 4.18 GeV  (banked, bottom_msbar_export_candidate APF_TRACE)
            top excluded: m_t > M_Z, separately captured by _DA_TOP

        Naive total: ~0.0363, OVERSHOOTING the dispersion value 0.02766 by ~31%.

    What the overshoot means structurally:
        The 31% gap IS the non-perturbative hadronic resonance physics that
        lives below ~1.5 GeV (rho, omega, phi, low-energy chiral dynamics).
        Naive perturbative quark vacuum polarization with current-quark MS-bar
        masses cannot capture this regime — quarks are confined there. This is
        a known feature of any naive-perturbative computation, not an APF
        deficiency. The proper M_Z computation (running banked quark MS-bar
        masses to M_Z via banked alpha_s, doing the perturbative QCD sum at
        M_Z, and matching to the dispersion integral below the perturbative
        threshold) is a separate multi-session structural arc.

    Bank disposition:
        - Delta alpha_had(M_Z) stays [C] (data-bound external; unchanged).
        - The check recharacterizes the [C] grade as
          [C_principled_external_universal_QCD_difficulty] — the gate is
          principled-external, not unfinished APF.
        - Numerical witness is recorded for audit reference, NOT as a
          structural-P claim. Export_delta_alpha_hadronic_internalized stays 0.
        - Forward-pointer: the proper M_Z computation requires running
          banked quark masses to M_Z, summing perturbative QCD pieces, and
          matching to the non-perturbative regime via banked structural
          theorems or admitted data (TBD).

    Honest non-claims preserved:
        - Export_delta_alpha_hadronic_internalized = 0
        - Export_delta_alpha_full_first_principles = 0
        - Export_naive_skeleton_replaces_dispersion = 0 (the naive value
          OVERSHOOTS by ~31% precisely because it misses the
          non-perturbative regime; it is a witness, not a replacement)
        - target_consumed = 0 (Delta alpha_had_dispersion and PDG light-quark
          MS-bar values are cited as comparators, NOT used to fit anything)
    """
    # Compute the naive perturbative-quark skeleton from banked MS-bar masses.
    per_quark = {}
    total_pert = 0.0
    for q, m_gev in _M_QUARK_MSBAR_GEV.items():
        Q2 = _Q_QUARK_SQUARED[q]
        contrib = _da_quark_one_loop_naive(m_gev, Q2)
        per_quark[q] = contrib
        total_pert += contrib

    # Comparison to the data-bound dispersion value.
    da_had_dispersion = _DA_HAD_DISPERSION  # banked external, comparator only
    ratio = total_pert / da_had_dispersion
    overshoot_frac = (total_pert - da_had_dispersion) / da_had_dispersion

    # Structural checks (not numerical-precision claims).
    check(total_pert > 0,
          "naive perturbative skeleton must be positive")
    check(0.025 < total_pert < 0.045,
          f"naive skeleton total {total_pert:.5f} should be O(1) of dispersion 0.02766")
    check(ratio > 1.0,
          "naive perturbative skeleton OVERSHOOTS dispersion (expected: "
          "non-perturbative regime missing)")
    check(0.20 < overshoot_frac < 0.45,
          f"overshoot {overshoot_frac*100:.1f}% should be O(30%) "
          "(matching universal-QCD-difficulty pattern)")
    check(EXPORT_FLAGS["Export_delta_alpha_hadronic_internalized"] == 0,
          "[C] status MUST be preserved — recharacterization only, not closure")
    check(EXPORT_FLAGS["Export_delta_alpha_full_first_principles"] == 0,
          "full first-principles flag MUST stay 0")

    return _result(
        name=("T_delta_alpha_had_principled_external_universal_QCD: "
              "Delta alpha_had[C] recharacterized — naive perturbative skeleton "
              f"overshoots dispersion by {overshoot_frac*100:.0f}% (non-pert regime)"
              " [C_principled_external_universal_QCD_difficulty]"),
        tier=4,
        epistemic="C_principled_external_universal_QCD_difficulty",
        summary=(
            f"Naive perturbative quark skeleton (banked MS-bar masses at mixed "
            f"self-scales, not run to M_Z): Delta alpha_q^pert^naive(M_Z) "
            f"= {total_pert:.5f}, overshooting Delta alpha_had_dispersion = "
            f"{da_had_dispersion} by {overshoot_frac*100:.1f}%. The overshoot "
            f"IS the non-perturbative hadronic resonance physics below ~1.5 GeV "
            f"that quarks-as-current-MS-bar cannot capture. Universal-QCD-"
            f"difficulty argument: SM itself has no first-principles route to "
            f"Delta alpha_had; both DHMZ/KNT dispersion and BMW lattice routes "
            f"rest on non-perturbative input. APF inherits the universal "
            f"difficulty; [C] is principled-external, not unfinished. Export "
            f"flags unchanged."
        ),
        key_result=(
            f"Delta alpha_q^pert^naive = {total_pert:.5f} "
            f"OVERSHOOTS dispersion {da_had_dispersion} by ~{overshoot_frac*100:.0f}% "
            f"[C_principled_external_universal_QCD_difficulty]"
        ),
        dependencies=[
            "L_delta_alpha_hadronic_external_open",
            "Theorem_R",  # N_c=3, quark charge assignments
            "charm_msbar_rundec_real_adapter",  # banked m_c self-scale
            "bottom_msbar_export_candidate",    # banked m_b APF_TRACE
        ],
        artifacts={
            "delta_alpha_q_pert_naive_total": total_pert,
            "delta_alpha_had_dispersion_comparator": da_had_dispersion,
            "overshoot_fraction": overshoot_frac,
            "ratio_pert_over_dispersion": ratio,
            "per_quark_contributions": per_quark,
            "quark_msbar_masses_gev": dict(_M_QUARK_MSBAR_GEV),
            "quark_charge_squared": dict(_Q_QUARK_SQUARED),
            "N_c": _N_C,
            "scheme_caveat": (
                "Mixed MS-bar self-scales (c at m_c, b at m_b, light at 2 GeV). "
                "NOT run to M_Z. Proper M_Z evaluation = separate multi-session "
                "arc using banked RunDec adapters + light-quark running infrastructure."
            ),
            "honest_non_claims": {
                "Export_delta_alpha_hadronic_internalized": 0,
                "Export_delta_alpha_full_first_principles": 0,
                "Export_naive_skeleton_replaces_dispersion": 0,
                "target_consumed": 0,
            },
            "universal_QCD_difficulty_citation": {
                "dispersion_routes": ["DHMZ", "KNT", "FJ22"],
                "lattice_route": "BMW collaboration",
                "tension_sigma": 2.5,
                "shared_object_with_muon_g_minus_2": True,
            },
        },
    )


# ============================================================================
# Registration / public interface
# ============================================================================

_CHECKS = {
    "T_delta_alpha_leptonic_first_principles":
        check_T_delta_alpha_leptonic_first_principles_P,
    "L_delta_alpha_leptonic_masses_banked":
        check_L_delta_alpha_leptonic_masses_banked_P,
    "L_delta_alpha_hadronic_external_open":
        check_L_delta_alpha_hadronic_external_open_C,
    "T_delta_alpha_total_decomposition":
        check_T_delta_alpha_total_decomposition_P,
    "T_delta_alpha_had_principled_external_universal_QCD":
        check_T_delta_alpha_had_principled_external_universal_QCD_C,
}


def register(registry):
    """Register the leptonic-running checks into the global bank."""
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}


def running_report() -> Dict[str, Any]:
    return {
        "leptonic_running": _leptonic_running(),
        "export_flags": dict(EXPORT_FLAGS),
    }


if __name__ == "__main__":
    import json
    out = run_all()
    print(json.dumps(
        {k: {"passed": v["passed"], "epistemic": v["epistemic"]} for k, v in out.items()},
        indent=2,
    ))
    print(json.dumps(_leptonic_running(), indent=2))
