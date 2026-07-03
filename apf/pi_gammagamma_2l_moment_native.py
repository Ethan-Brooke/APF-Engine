"""Two-loop photon vacuum polarization: native master-route reproduction of the
Kallen-Sabry moment M(0) = 82/81 (slope 41/162 in (alpha/pi)^2 units)
[P-family, scope-fenced: a native-master-route REPRODUCTION of a known two-loop QED
quantity, NOT an A1-derivation; grade tag P_pi_gammagamma_2L_photon_vp_native_master_route_reproduction].

The renormalized two-loop QED photon self-energy from a single fermion has a
low-q^2 slope Pi_R^(2)'(0) = 41/162, equivalently the Mellin moment M(0) = 82/81
(Kallen-Sabry 1955; Greynat-de Rafael arXiv:1712.02202; Broadhurst-Fleischer-
Tarasov Z.Phys.C 60 (1993) 287). This module certifies that the SAME number falls
out of APF's native two-loop machinery -- the d-dimensional Dirac trace engine,
IBP-style tensor reduction, and the BANKED single-scale two-loop vacuum master
chetyrkin_two_massive_one_massless_scalar (apf.w_trace_native_two_loop_tadpole) --
with on-shell mass renormalization. Nothing external is imported: the Kallen-Sabry
spectral function is a comparator only, never an input. Two independent native
routes (the dispersive comparator and this master-route assembly) land on the same
41/162.

DIAGRAM CONTENT (the load-bearing combinatorics).
The two-loop 1PI photon self-energy from one fermion has exactly three diagrams:
two self-energy insertions (the internal photon with both ends on the same fermion
arc -- upper and lower arc, equal by reflection) and ONE crossed/vertex diagram
(the internal photon connecting the two arcs). On the closed fermion loop the four
marked points {mu, nu, a, b} (two external vertices + two internal-photon ends)
fall into exactly two cyclic classes: {mu nu a b} (= {mu a b nu}) gives the two SE
insertions, and {mu a nu b} gives the single crossed diagram. The renormalized
slope is therefore

        Pi^(2)_slope (stripped) = 2*SE_a + 1*V_a + delta_m * dPi_1/dm,

where delta_m is the on-shell one-loop mass shift and Pi_1 the one-loop VP slope.
Only mass renormalization of the internal fermion is needed: by the Ward identity
Z_1 = Z_2 the fermion-field and vertex counterterms cancel entirely, and the charge
counterterm Z_3 drops from the slope (it is q^2-independent; Pi_hat(0) = 0). The
delta_m counterterm's relative sign is FORCED by the requirement that the 1/eps
subdivergence cancel -- it is not chosen.

WHAT IS BANKED [P, scope-fenced reproduction -- tag P_pi_gammagamma_2L_photon_vp_native_master_route_reproduction].
- This is a REPRODUCTION of a known two-loop QED quantity via APF's native two-loop
  engine, not a derivation of new physics from A1. "Native" means computed by APF's
  own machinery without importing the answer (KS is comparator-only), not "a
  consequence of the axiom". It inherits the scope caveat of the banked master
  (P_two_loop_tadpole_scalar_connected_master_current_scope).
- The one-loop counterterm pieces (on-shell delta_m, the one-loop VP slope Pi_1 and
  its mass-derivative) are re-derived live here from the native trace+reduction and
  the single-scale tadpole jbar masters; the one-loop VP slope anchor 4/15
  (stripped) -> 1/15 (physical) is checked.
- The two-loop diagrams SE_a and V_a are the eps-Laurent expansions produced by the
  native master-route reduction in the witness scripts (see ARTIFACTS); reproduced
  and pole-audited independently. They enter as certified constants.
- The assembly 2*SE_a + 1*V_a + delta_m*dPi_1/dm has its 1/eps pole cancel exactly
  AND its EulerGamma cancel exactly, leaving a pure rational with no pi^2 / zeta(3)
  (as required for the single-mass two-loop vacuum). Multiplying by the
  one-loop-consistent normalization K_2 = (1/4)^2 = +1/16 gives exactly 41/162.
- Bank-touch: the local (m,m,0) master closed form is verified byte-identical in
  value to the banked chetyrkin_two_massive_one_massless_scalar.
- Negative control: the same assembly with TWO crossed diagrams (2*V_a, the prior
  miscount) leaves a +8/(15 eps) residual that does not cancel -- the combinatorics
  is doing real work.

WHAT IS NOT CLAIMED.
This is a reproduction of a known two-loop QED quantity via native machinery, not a
new APF prediction. The fermion mass m is the on-shell (pole) mass; the result is
the standard on-shell renormalized slope. The full symbolic two-loop reduction lives
in the witness scripts (it is too slow for verify_all); this check certifies the
assembly + the banked-master identity.

ARTIFACTS (Drive):
  __APF Library/Artifacts_2026-06-16_session/pi_gammagamma_2L_proof_of_route/
    nat_twoloop_LANDING_assembly_2SE_1V.py        (the landing assembly)
    nat_twoloop_SE_insertion_reduced_via_banked_master.py   (SE_a reduction)
    nat_twoloop_vertex_reduced_via_banked_master.py         (V_a reduction)
    nat_twoloop_SEa_pole_audit_confirms_diagram.py          (SE_a pole audit)
    RESEARCH_NOTE_pi_gamma_gamma_2L_proof_of_route.md (Update 5 = resolution)

[P_pi_gammagamma_2L_photon_vp_native_master_route_reproduction]; native trace + IBP + banked vacuum master
reproduce Kallen-Sabry M(0)=82/81; no measured/external coefficient consumed.
"""
from __future__ import annotations

import sympy as sp

from apf.apf_utils import check, _result

TARGET = sp.Rational(41, 162)          # KS slope in (alpha/pi)^2  <=>  M(0) = 82/81
K2 = sp.Rational(1, 16)                 # stripped (alpha/4pi)^2 -> physical (alpha/pi)^2,
                                        # = (K1)^2 with one-loop K1 = 1/4 (4/15 -> 1/15)

# Certified two-loop diagram Laurent expansions (stripped, m=1), from the native
# master-route reduction witnesses (reproduced + pole-audited this session):
#   SE_a = -16/(15 eps) + 32 g/15 - 76/75            (g = EulerGamma; ln m -> 0 at m=1)
#   V_a  =  +8/(15 eps) + 4744/2025 - 16 g/15
_G = sp.EulerGamma
_EPS = sp.symbols('epsilon')
_SE_A = sp.Rational(-16, 15) / _EPS + (sp.Rational(32, 15) * _G - sp.Rational(76, 75))
_V_A = sp.Rational(8, 15) / _EPS + (sp.Rational(4744, 2025) - sp.Rational(16, 15) * _G)


def _bank_touch_max_diff():
    """Verify the local (m,m,0) master equals the banked chetyrkin master."""
    import mpmath as mp
    from apf.w_trace_native_two_loop_tadpole import (
        chetyrkin_two_massive_one_massless_scalar as BANK,
    )
    D = sp.Rational(37, 10)

    def chet_sym(al, be, ga):
        return (sp.Integer(1) ** (D - al - be - ga)
                * sp.gamma(D / 2 - ga) / (sp.gamma(al) * sp.gamma(be) * sp.gamma(D / 2))
                * sp.gamma(al + ga - D / 2) * sp.gamma(be + ga - D / 2)
                * sp.gamma(al + be + ga - D) / sp.gamma(al + be + 2 * ga - D))

    # Pin precision locally: other modules may have lowered the global mpmath dps,
    # which would degrade this otherwise-exact identity comparison.
    _saved_dps = mp.mp.dps
    mp.mp.dps = 60
    try:
        maxerr = mp.mpf(0)
        for (al, be, ga) in [(1, 1, 1), (2, 1, 1), (1, 2, 1), (2, 2, 1),
                             (3, 1, 1), (1, 1, 2), (2, 1, 2)]:
            a = mp.mpf(str(sp.N(chet_sym(al, be, ga), 55)))
            b = BANK(al, be, ga, mp.mpf('3.7'), 1)
            maxerr = max(maxerr, abs(a - b))
    finally:
        mp.mp.dps = _saved_dps
    return maxerr


def _one_loop_ct_pieces():
    """Re-derive (live) the on-shell delta_m and the one-loop VP slope Pi_1 and its
    mass-derivative, from the native trace+reduction and the single-scale jbar masters."""
    eps = _EPS
    mm = sp.symbols('mm', positive=True)
    m2 = mm ** 2
    dd = 4 - 2 * eps
    I0 = 1 / (1 - 2 * eps)
    I1 = 1 / (1 - 2 * eps) - 1 / (2 - 2 * eps)
    delta_m = mm ** (1 - 2 * eps) * sp.gamma(eps) * ((2 - dd) * I1 + dd * I0)
    k2s, kqs, q2s = sp.symbols('k2 kq q2')

    def jbar(n):
        if n <= 0:
            return sp.Integer(0)
        return (-1) ** n * m2 ** (dd / 2 - n) * sp.gamma(n - dd / 2) / sp.gamma(n)

    def red1(a, n):
        return sum(sp.binomial(a, j) * m2 ** (a - j) * jbar(n - j) for j in range(a + 1))

    num1 = 4 * (-(dd - 2) * (k2s + kqs) + dd * m2)
    qp = 2 * kqs + q2s
    sn = 0
    for r in range(5):
        cc = sp.expand(num1 * (-qp) ** r)
        pl = sp.Poly(cc, kqs, q2s)
        for (a, c), co in zip(pl.monoms(), pl.coeffs()):
            if a + 2 * c != 4 or a % 2:
                continue
            cc2 = a // 2
            nf = sp.factorial2(a - 1) if cc2 > 0 else 1
            den = 1
            for j in range(cc2):
                den *= (dd + 2 * j)
            sc = sp.expand(co * (nf / den) * (k2s ** cc2) * (q2s ** cc2) * q2s ** c)
            sc2 = sp.Poly(sc, q2s).coeff_monomial(q2s ** 2)
            if sc2 == 0:
                continue
            for (p,), cf in zip(sp.Poly(sc2, k2s).monoms(), sp.Poly(sc2, k2s).coeffs()):
                sn += cf * red1(p, r + 2)
    Pi1 = sn / (dd - 1)
    dPi1 = sp.diff(Pi1, mm)
    return delta_m.subs(mm, 1), dPi1.subs(mm, 1), Pi1.subs(mm, 1)


def _assemble(nV, sCT, delta_m1, dPi1_1):
    eps = _EPS
    tot = 2 * _SE_A + nV * _V_A + sCT * delta_m1 * dPi1_1
    ser = sp.expand(sp.series(tot, eps, 0, 1).removeO())
    pole = sp.nsimplify(ser.coeff(eps, -1), tolerance=1e-9, rational=True)
    fin = sp.limit(ser - ser.coeff(eps, -1) / eps, eps, 0)
    gam = sp.nsimplify(sp.expand(fin).coeff(_G, 1), tolerance=1e-9, rational=True)
    phys = sp.nsimplify(K2 * fin)
    return pole, gam, phys


def check_T_pi_gammagamma_2L_moment_native_P():
    # (1) bank-touch: local master == banked chetyrkin two-massive/one-massless master
    maxerr = _bank_touch_max_diff()
    check(float(maxerr) < 1e-25,
          f"bank-touch failed: local vs banked (m,m,0) master differ by {maxerr}")

    # (2) live one-loop counterterm pieces + one-loop VP slope anchor
    delta_m1, dPi1_1, Pi1_1 = _one_loop_ct_pieces()
    check(sp.nsimplify(sp.limit(Pi1_1, _EPS, 0)) == sp.Rational(4, 15),
          "one-loop VP slope anchor (stripped 4/15) failed")

    # (3) correct assembly: 2 SE_a + 1 V_a + delta_m CT  (sCT = -1 forced by finiteness)
    pole, gam, phys = _assemble(1, -1, delta_m1, dPi1_1)
    check(pole == 0, f"1/eps pole did not cancel: {pole}")
    check(gam == 0, f"EulerGamma did not cancel: {gam}")
    check(phys == TARGET, f"native slope {phys} != Kallen-Sabry 41/162")

    # (4) negative control: the two-crossed-diagram miscount leaves a +8/(15 eps) residual
    pole2, _, _ = _assemble(2, -1, delta_m1, dPi1_1)
    check(pole2 == sp.Rational(8, 15),
          f"negative control changed: 2-V assembly pole = {pole2}, expected 8/15")

    return _result(
        name=("T_pi_gammagamma_2L_moment_native: APF native two-loop machinery "
              "(d-dim trace + IBP reduction + the banked (m,m,0) chetyrkin vacuum "
              "master + on-shell mass renormalization) reproduces the two-loop QED "
              "photon-VP slope Pi_R^(2)'(0) = 41/162, i.e. the Kallen-Sabry moment "
              "M(0) = 82/81. Diagram content 2 SE-insertion + 1 crossed; only mass "
              "renormalization needed (Z1=Z2). 1/eps pole and EulerGamma both cancel; "
              "pure rational. No external coefficient consumed (KS comparator-only). Scope-fenced REPRODUCTION of a known QED quantity, not an A1-derivation; SE_a/V_a reductions are witness-certified (not re-run in verify_all). [P_pi_gammagamma_2L_photon_vp_native_master_route_reproduction]"),
        tier=4,
        epistemic='P_pi_gammagamma_2L_photon_vp_native_master_route_reproduction',
        summary=("Native master-route two-loop photon vacuum polarization: "
                 "renormalized slope = 41/162 = KS M(0)=82/81, exact. Pole and "
                 "EulerGamma cancel for the correct 2 SE + 1 V diagram combination; "
                 "the 2-V miscount leaves +8/(15 eps) (negative control). Bank-touch: "
                 "local (m,m,0) master identical to chetyrkin_two_massive_one_massless_scalar. Reproduction, not A1-derivation; SE_a/V_a witness-certified."),
        key_result="Pi_R^(2)'(0) = 41/162  (M(0) = 82/81)",
        dependencies=["chetyrkin_two_massive_one_massless_scalar"],
        cross_refs=["w_trace_native_two_loop_tadpole", "delta_alpha_capacity_density"],
        artifacts=["Artifacts_2026-06-16_session/pi_gammagamma_2L_proof_of_route/"],
    )


_CHECKS = {
    "T_pi_gammagamma_2L_moment_native": check_T_pi_gammagamma_2L_moment_native_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


if __name__ == "__main__":
    r = check_T_pi_gammagamma_2L_moment_native_P()
    print("PASS:", r["name"][:80], "...")
    print("key_result:", r["key_result"], "| epistemic:", r["epistemic"], "| tier:", r["tier"])

# ---------------------------------------------------------------------------
# IE onboarding (Wave 7, v24.3.347).
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "ew:pi_gammagamma_2l_moment_native",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "Single banked check check_T_pi_gammagamma_2L_moment_native_P (tier "
            "4, bespoke machine grade "
            "P_pi_gammagamma_2L_photon_vp_native_master_route_reproduction) "
            "certifying that APF's native two-loop machinery -- the d-dimensional "
            "Dirac trace engine, IBP-style tensor reduction, the banked (m,m,0) "
            "chetyrkin_two_massive_one_massless_scalar vacuum master, and on- "
            "shell mass renormalization -- reproduces the two-loop QED photon "
            "vacuum-polarization slope Pi_R^(2)'(0) = 41/162, i.e. the Kallen- "
            "Sabry moment M(0) = 82/81, exactly. The assembly 2 x SE + 1 x "
            "crossed + delta_m counterterm has its 1/eps pole AND EulerGamma "
            "cancel, leaving a pure rational; the negative control (the 2-crossed "
            "miscount) leaves a +8/(15 eps) residual, so the combinatorics is "
            "load-bearing. Scope fence carried in the grade token itself: this is "
            "a native-master-route REPRODUCTION of a known two-loop QED quantity, "
            "NOT an A1-derivation; Kallen-Sabry is comparator-only, never an "
            "input; the SE_a/V_a two-loop reductions enter as witness-certified "
            "constants (not re-run in verify_all); the check inherits the scope "
            "caveat of the banked master. "
        ),
        "note": "Wave 7; scope fence (reproduction, not A1-derivation) is part of the banked grade token",
    },
)
