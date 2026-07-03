"""The trans-Planckian U(1)_Y Landau pole, quantified (v24.3.315).

The bank has long carried the QUALITATIVE fact (extensions.py: b1 < 0, U(1) not
asymptotically free -> Landau pole; generations.py: 'Landau pole = asymptotic
non-freedom'; the rank-1 crossing story in abelian_coupling_capacity_count.py).
This module banks the QUANTIFICATION flagged at the 2026-06-23 consolidation:
the one-loop U(1)_Y pole sits at ~1.7-2.2 x 10^41 GeV -- twenty-two decades
above the Planck mass -- so the abelian sector's UV self-consistency margin is
enormous, and the continuum triviality problem is never imported into the
framework's regime.

WHAT IS [P] HERE (grading carve, explicit):
  * b_Y = 41/6, computed EXACTLY (Fraction) from the banked hypercharge content
    -- the same Y assignments L_anomaly_free certifies -- via the one-loop
    formula b_Y = (2/3) sum_Weyl Y^2 + (1/3) sum_cplx_scalar Y^2. Pure count.
  * The per-generation increment Delta b_Y = 20/9 (same count, one generation).
  * The pole arithmetic, CONDITIONAL on an anchor: ln(Lambda/mu0) =
    (2 pi / b_Y) * (1/alpha_Y(mu0)) -- exact one-loop algebra.
  * The CONCLUSION -- the pole is trans-Planckian by > 22 decades -- which is
    ANCHOR-ROBUST: the two available anchors agree on 1/alpha_Y(M_Z) to 0.26%
    and land within a factor ~1.3 of each other at 10^41 GeV.

ANCHORS (both computed):
  * APF anchor: 1/alpha_Y(M_cross) = C_total = 61, the banked rank-1 capacity
    count (abelian_coupling_capacity_count.py). NOTE: that reading is graded
    [P_structural_reading] (v24.3.284 -- adopted rank-1 reading, alpha_s-
    corroborated at 0.11 sigma, not A1-derived); the specific APF-anchor pole
    VALUE (2.20e41 GeV) inherits it.
  * Comparator anchor: PDG M_Z inputs (1/alpha_em(M_Z) = 127.95,
    sin^2theta_W(MSbar, M_Z) = 0.23122) -> 1/alpha_Y(M_Z) = 98.37 ->
    pole = 1.74e41 GeV. Standard measured comparator (bank precedent:
    confirmed-comparison checks carry measured values under [P]).

GENERATION HEADROOM (the 2026-06-23 flag's second clause, made exact -- and
CORRECTED: the flag's '~7 generations' was the rough estimate): each extra
generation adds Delta b_Y = 20/9; computed exactly, the pole stays trans-
Planckian through SIX total generations and lands marginally BELOW M_Pl at
n_g = 7 (pole = 0.88 x M_Pl -- a whisker; the flag's ~7 sat on this boundary).
Strict headroom: n_g <= 6, i.e. three extra generations of matter before the
one-loop pole reaches the Planck scale.

SCOPE FENCES (explicit non-claims):
  * ONE-LOOP only. Higher loops and threshold effects move the pole's location;
    at 22 decades of margin no plausible correction threatens the trans-
    Planckian conclusion, but no two-loop number is computed or claimed here.
  * The pole is an EFT-breakdown signal, not a physical scale reached: the
    framework's finite structure terminates far below (the crossing/Planck
    scales); nothing here claims physics AT 10^41 GeV.
  * No falsifier claim: this is a consistency MARGIN, not a prediction row.
    It does not enter the scorecard.

Grade [P] per the carve above; tier 4. Flagged by Ethan at the 2026-06-23
consolidation signoff; banked 2026-07-02.
"""

from __future__ import annotations

import math
from fractions import Fraction


M_Z_GEV = 91.1876
M_PL_GEV = 1.221e19          # Planck mass, GeV
PDG_INV_ALPHA_EM_MZ = 127.95
PDG_SIN2_THETA_W_MZ = 0.23122


def b_Y_exact(n_generations: int = 3) -> Fraction:
    """One-loop U(1)_Y coefficient (SM normalization, coupling-growth convention):
    b_Y = (2/3) sum_Weyl Y^2 + (1/3) sum_complex_scalar Y^2, from the banked
    hypercharge content (the L_anomaly_free assignments)."""
    Y_Q, Y_u, Y_d, Y_L, Y_e = (Fraction(1, 6), Fraction(2, 3), Fraction(-1, 3),
                               Fraction(-1, 2), Fraction(-1))
    per_gen = (2 * 3 * Y_Q ** 2      # Q_L: SU(2) doublet x 3 colours
               + 3 * Y_u ** 2        # u_R x 3 colours
               + 3 * Y_d ** 2        # d_R x 3 colours
               + 2 * Y_L ** 2        # L_L: SU(2) doublet
               + 1 * Y_e ** 2)       # e_R
    higgs = 2 * Fraction(1, 2) ** 2  # one complex doublet, Y = 1/2
    return Fraction(2, 3) * n_generations * per_gen + Fraction(1, 3) * higgs


def pole_scale_gev(inv_alpha_Y_at_mu0: float, mu0_gev: float,
                   b_y: float | None = None) -> float:
    """One-loop Landau-pole scale: 1/alpha_Y(mu) = 1/alpha_Y(mu0) - (b_Y/2pi) ln(mu/mu0) -> 0."""
    b = float(b_Y_exact()) if b_y is None else b_y
    return mu0_gev * math.exp((2 * math.pi / b) * inv_alpha_Y_at_mu0)


def check_T_u1y_landau_pole_trans_planckian():
    """The U(1)_Y Landau pole is trans-Planckian by more than twenty-two decades,
    anchor-robustly; b_Y = 41/6 exact from the banked hypercharge content.
    See the module docstring for the grading carve and scope fences.
    """
    failures = []
    bY = b_Y_exact()
    if bY != Fraction(41, 6):
        failures.append("b_Y from banked hypercharges = %s != 41/6" % (bY,))
    per_gen = b_Y_exact(4) - b_Y_exact(3)
    if per_gen != Fraction(20, 9):
        failures.append("per-generation increment = %s != 20/9" % (per_gen,))

    # APF anchor: the banked rank-1 count at the banked crossing scale
    from apf.abelian_coupling_capacity_count import _alpha_s_forward, C_total
    _, _, t = _alpha_s_forward()
    m_cross = M_Z_GEV * math.exp(t)
    pole_apf = pole_scale_gev(float(C_total), m_cross)
    inv_aY_mz_apf = float(C_total) + float(bY) / (2 * math.pi) * t

    # Comparator anchor: PDG M_Z inputs
    inv_aY_mz_pdg = PDG_INV_ALPHA_EM_MZ * (1 - PDG_SIN2_THETA_W_MZ)
    pole_pdg = pole_scale_gev(inv_aY_mz_pdg, M_Z_GEV)

    dec_apf = math.log10(pole_apf / M_PL_GEV)
    dec_pdg = math.log10(pole_pdg / M_PL_GEV)

    if not (2.0e41 < pole_apf < 2.4e41):
        failures.append("APF-anchor pole %.3e GeV outside the pinned window" % pole_apf)
    if not (1.6e41 < pole_pdg < 1.9e41):
        failures.append("PDG-anchor pole %.3e GeV outside the pinned window (flagged 1.7e41)" % pole_pdg)
    if not (dec_apf > 22.0 and dec_pdg > 22.0):
        failures.append("trans-Planckian margin below 22 decades: %.1f / %.1f" % (dec_apf, dec_pdg))
    if not abs(inv_aY_mz_apf - inv_aY_mz_pdg) / inv_aY_mz_pdg < 0.005:
        failures.append("anchors disagree on 1/alpha_Y(M_Z) beyond 0.5%%: %.2f vs %.2f"
                        % (inv_aY_mz_apf, inv_aY_mz_pdg))

    # Generation headroom (exact; the 2026-06-23 '~7' flag corrected): the pole stays
    # above M_Pl through n_g = 6 and crosses at n_g = 7 (0.89 x M_Pl -- marginal).
    # Anchor held at the PDG 1/alpha_Y(M_Z); extra generations change the running
    # coefficient, not the M_Z anchor value.
    headroom = None
    for n_g in range(3, 12):
        p = pole_scale_gev(inv_aY_mz_pdg, M_Z_GEV, b_y=float(b_Y_exact(n_g)))
        if p < M_PL_GEV:
            headroom = n_g - 1
            break
    if headroom != 6:
        failures.append("generation headroom = %s != 6" % (headroom,))
    p7 = pole_scale_gev(inv_aY_mz_pdg, M_Z_GEV, b_y=float(b_Y_exact(7)))
    if not (0.8 < p7 / M_PL_GEV < 1.0):
        failures.append("n_g=7 marginality broken: pole/M_Pl = %.3f" % (p7 / M_PL_GEV))  # 0.882

    passed = not failures
    return {
        "name": ("T_u1y_landau_pole_trans_planckian: the one-loop U(1)_Y Landau pole "
                 "quantified -- b_Y = 41/6 exact from the banked hypercharge content; "
                 "pole at ~1.7e41 (PDG anchor) / ~2.2e41 GeV (banked rank-1 anchor), "
                 ">22 decades above M_Pl, anchor-robust; trans-Planckian through six "
                 "generations (n_g=7 marginal at 0.88 M_Pl) [P]"),
        "passed": passed,
        "epistemic": "P",
        "tier": 4,
        "dependencies": [
            "L_anomaly_free",                                    # the hypercharge content
            "T_abelian_coupling_fixed_by_rank1_capacity_count",  # registry key (no _P suffix); the APF anchor (P_structural_reading, inherited by that anchor's VALUE only)
        ],
        "failures": failures,
        "key_result": (
            "b_Y = 41/6 exact; Landau pole = 1.74e41 GeV (PDG anchor) / 2.20e41 GeV "
            "(banked 61-count anchor), 22.15-22.26 decades above M_Pl; anchors agree on "
            "1/alpha_Y(M_Z) to 0.26%; per-generation Delta b_Y = 20/9, pole trans-"
            "Planckian through n_g = 6 (n_g = 7 marginal: 0.88 M_Pl -- the 2026-06-23 "
            "'~7' flag corrected by the exact computation). One-loop; consistency "
            "margin, not a scorecard "
            "row; the framework's finite structure terminates far below the pole. [P]"
        ),
        "artifacts": {
            "b_Y": str(bY),
            "pole_apf_anchor_gev": pole_apf,
            "pole_pdg_anchor_gev": pole_pdg,
            "decades_above_M_Pl": [round(dec_apf, 2), round(dec_pdg, 2)],
            "inv_alpha_Y_MZ": {"apf": round(inv_aY_mz_apf, 2), "pdg": round(inv_aY_mz_pdg, 2)},
            "per_generation_delta_bY": str(per_gen),
            "generation_headroom": headroom,
            "M_cross_gev": m_cross,
        },
    }


_CHECKS = {
    "T_u1y_landau_pole_trans_planckian": check_T_u1y_landau_pole_trans_planckian,
}


def register(registry):
    registry.update(_CHECKS)


if __name__ == "__main__":
    r = check_T_u1y_landau_pole_trans_planckian()
    print(("PASS" if r["passed"] else "FAIL"), r["name"])
    for f in r["failures"]:
        print("   -", f)


# ---------------------------------------------------------------------------
# IE onboarding (Wave 6, v24.3.346).
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "ew:u1y_landau_pole_trans_planckian",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "The one-loop U(1)_Y Landau pole is trans-Planckian by more "
            "than twenty-two decades [P] "
            "(check_T_u1y_landau_pole_trans_planckian, v24.3.315): b_Y = 41/6 "
            "exact from the banked hypercharge content (20/9 per "
            "generation), anchor-robust across the banked anchor readings; "
            "generation bound n_g <= 6 from pole > M_Pl. No claim that the "
            "pole is physical -- the content is that the abelian sector "
            "cannot self-obstruct below the Planck scale. "
        ),
        "note": "Wave 6",
    },
)
