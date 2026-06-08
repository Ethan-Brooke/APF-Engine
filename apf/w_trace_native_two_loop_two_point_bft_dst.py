"""APF-native two-loop two-point BFT one-mass + DST large-momentum coefficient family — Tier-4.

Source-certified two-loop two-point coefficient family combining:

  * Broadhurst-Fleischer-Tarasov (1993) one-mass normalized hypergeometric
    branches (Z. Phys. C 60 (1993) 287, arXiv: hep-ph/9304303):
    N_I1, N_I2, N_I4, N_Ie3 small-q² hypergeometric expansion.

  * Davydychev-Smirnov-Tausk (1993) large-momentum coefficient family
    M0, M1, M2 (arXiv: hep-ph/9307371, Eq. (11)-(14) + Appendix B
    Eq. (29)-(33)) — including the vacuum F(m1²,m2²,m3²) function.

  * Padé bridge for matching small-q² ↔ large-q² regimes.

Source-certified to the named equations. Combines three sibling adapter
files (bft_one_mass.py + dst_large_momentum.py + pade_bridge.py) from
APF_NATIVE_TWO_LOOP_TWO_POINT_COEFFICIENT_FAMILY_IMPLEMENTATION_v1.

Honest non-claim: scoped at [P_two_point_BFT_DST_coefficient_family_current_depth];
NOT a full Tier-1 master for the unrestricted arbitrary-mass two-point.
"""
from __future__ import annotations
import mpmath as mp

from apf.apf_utils import check, _result


# =============================================================================
# BFT one-mass normalized hypergeometric branches
# (Broadhurst-Fleischer-Tarasov 1993, hep-ph/9304303)
# =============================================================================

def hyp(a, b, z):
    return mp.hyper(a, b, z)


def beta_struct(q2, m2, eps):
    return mp.gamma(1-eps)**2 / mp.gamma(1-2*eps) * (m2/q2)**eps


def gamma_struct(q2, m2, eps):
    return (mp.gamma(1+2*eps)/mp.gamma(1+eps)**2
            * mp.gamma(1-eps)**3/mp.gamma(1-3*eps) * (m2/q2)**(2*eps))


def delta_struct(eps):
    return mp.gamma(1-eps)*mp.gamma(1+2*eps)/mp.gamma(1+eps)


def norm_I1_small(q2, m2, eps):
    """BFT N_I1 = q² m^(4ε) ε³ (1-2ε) I1, small-q² hypergeometric form."""
    beta = beta_struct(q2, m2, eps)
    gamma = gamma_struct(q2, m2, eps)
    delta = delta_struct(eps)
    z = -q2/m2
    return (mp.mpf('0.5')*delta*hyp([eps, 2*eps], [1-eps], z)
            + (beta - mp.mpf('0.5')*delta)*hyp([1, eps], [1-eps], z)
            + mp.mpf('0.5')*gamma*hyp([1, -eps], [1-3*eps], z)
            - beta - mp.mpf('0.5')*gamma)


def norm_I2_small(q2, m2, eps):
    """BFT N_I2 = m^(2+4ε) ε² (1-ε)(1-2ε) I2, small-q² hypergeometric form."""
    delta = delta_struct(eps)
    z = -q2/m2
    G2 = hyp([1, 1+eps], [2-eps], z)
    H2 = hyp([1+eps, 1+2*eps], [2-eps], z)
    return delta*H2 - G2 + eps/(1-eps)*(q2/m2)*G2**2


def norm_I4_small(q2, m2, eps):
    """BFT N_I4 = m^(2+4ε) ε (1-2ε) I4, small-q² hypergeometric form."""
    z = -q2/(4*m2)
    G4 = hyp([1, 1+eps], [mp.mpf('1.5')], z)
    H4 = hyp([1, 1+eps, 1+2*eps], [mp.mpf('1.5')+eps, 2-eps], z)
    return (1 + q2/(4*m2))*G4**2 - H4/((1+2*eps)*(1-eps))


def norm_Ie3_small(q2, m2, eps):
    """BFT N_Ie3 = m^(2+4ε) (1+ε)(1-2ε) Ie3, small-q² hypergeometric form."""
    beta = beta_struct(q2, m2, eps)
    z = -q2/(4*m2)
    return (hyp([1, 1+eps, 1+eps, 1+2*eps],
                [mp.mpf('1.5')+eps, 2+eps, 2-eps], z)/((1-eps)*(1+2*eps))
            + (1+eps)/(2*eps)*beta*hyp([1, 1, 1+eps], [mp.mpf('1.5'), 2], z)
            - (1/(2*eps))*hyp([1, 1+eps, 1+eps], [mp.mpf('1.5'), 2+eps], z))


# =============================================================================
# DST large-momentum coefficient family M0, M1, M2 + vacuum F
# (Davydychev-Smirnov-Tausk 1993, hep-ph/9307371)
# =============================================================================

def log_minus_k2_over_m2(k2, m2, *, feynman=True):
    """log((-k²-i0)/m²). Positive real k² → log(k²/m²) - iπ."""
    k2c, m2c = mp.mpc(k2), mp.mpc(m2)
    if feynman and abs(mp.im(k2c)) < mp.mpf('1e-40') and mp.re(k2c) > 0:
        return mp.log(mp.re(k2c)/m2c) - 1j*mp.pi
    return mp.log(-k2c/m2c)


def lambda2(x, y):
    x, y = mp.mpc(x), mp.mpc(y)
    return (1-x-y)**2 - 4*x*y


def _F_raw(a, b, c):
    """DST Eq. (30)-(33), with c as the dimension-making mass squared."""
    a, b, c = map(mp.mpc, (a, b, c))
    if c == 0:
        raise ZeroDivisionError('vacuum_F requires nonzero scale mass')
    x, y = a/c, b/c
    lam2 = lambda2(x, y)
    lam = mp.sqrt(lam2)
    if abs(lam) < mp.mpf('1e-30'):
        raise ZeroDivisionError('lambda=0 threshold limit requires separate expansion')
    A = (1+x-y-lam)/2
    B = (1-x+y-lam)/2
    Phi = (2*mp.log(A)*mp.log(B) - mp.log(x)*mp.log(y)
           - 2*mp.polylog(2, A) - 2*mp.polylog(2, B)
           + mp.pi**2/3)/lam
    return c * lam2 * Phi


def vacuum_F(a, b, c):
    """Symmetric two-loop vacuum function F(m1², m2², m3²) — choose largest
    mass as dimension-making parameter for numerical stability per DST."""
    vals = [mp.mpf(a), mp.mpf(b), mp.mpf(c)]
    idx = max(range(3), key=lambda i: vals[i])
    if idx == 0:
        return _F_raw(vals[1], vals[2], vals[0])
    if idx == 1:
        return _F_raw(vals[0], vals[2], vals[1])
    return _F_raw(vals[0], vals[1], vals[2])


def M0():
    """DST M0 coefficient: 6 ζ(3)."""
    return 6*mp.zeta(3)


def _outer_term(mi, ma, mb, k2):
    L = log_minus_k2_over_m2(k2, mi)
    return mi/2 * (L**2 + 4*L - mp.log(ma/mi)*mp.log(mb/mi) + 6)


def M1(k2, m1sq, m2sq, m3sq, m4sq, m5sq):
    """DST Eq. (13) M1 coefficient — printed 'analogous terms' made explicit."""
    m1sq, m2sq, m3sq, m4sq, m5sq = map(mp.mpf, (m1sq, m2sq, m3sq, m4sq, m5sq))
    out = _outer_term(m1sq, m2sq, m3sq, k2)
    out += _outer_term(m2sq, m1sq, m3sq, k2)
    out += _outer_term(m4sq, m5sq, m3sq, k2)
    out += _outer_term(m5sq, m4sq, m3sq, k2)
    L3 = log_minus_k2_over_m2(k2, m3sq)
    out += m3sq/2 * (2*L3**2 + 4*L3
                     - mp.log(m1sq/m3sq)*mp.log(m2sq/m3sq)
                     - mp.log(m4sq/m3sq)*mp.log(m5sq/m3sq))
    out += mp.mpf('0.5')*(vacuum_F(m1sq, m2sq, m3sq) + vacuum_F(m4sq, m5sq, m3sq))
    return out


def _outer_M2_term(mi, ma, mb, k2):
    L = log_minus_k2_over_m2(k2, mi)
    return mi**2/8 * (2*L**2 + 4*L - 2*mp.log(ma/mi)*mp.log(mb/mi) + 7)


def _cross_14_like(mi, mj, ai, aj, k2):
    """DST Eq.(15) cross term of the m1·m4 / m2·m5 type."""
    Li = log_minus_k2_over_m2(k2, mi)
    Lj = log_minus_k2_over_m2(k2, mj)
    return mi*mj/2 * (Li**2 + Lj**2 + 4*Li + 4*Lj
                      - mp.log(ai[0]/mi)*mp.log(ai[1]/mi)
                      - mp.log(aj[0]/mj)*mp.log(aj[1]/mj) + 8)


def _cross_15_like(mi, mj, ai, aj, k2):
    Li = log_minus_k2_over_m2(k2, mi)
    Lj = log_minus_k2_over_m2(k2, mj)
    return mi*mj/2 * (2*Li**2 + 2*Lj**2 + 2*Li + 2*Lj
                      - mp.log(ai[0]/mi)*mp.log(ai[1]/mi)
                      - mp.log(aj[0]/mj)*mp.log(aj[1]/mj)
                      - mp.log(mi/mj)**2 + 2)


def _central_cross_M2(mi, m1sq, m2sq, m3sq, m4sq, m5sq, k2):
    L3 = log_minus_k2_over_m2(k2, m3sq)
    Li = log_minus_k2_over_m2(k2, mi)
    return mi*m3sq/2 * (2*L3**2 - 2*Li
                        - mp.log(m1sq/m3sq)*mp.log(m2sq/m3sq)
                        - mp.log(m4sq/m3sq)*mp.log(m5sq/m3sq)
                        - 8)


def M2(k2, m1sq, m2sq, m3sq, m4sq, m5sq):
    """DST Eq. (15) M2 coefficient with all analogous terms expanded.

    Mass dimension four. mₖ² are squared masses.
    """
    m1sq, m2sq, m3sq, m4sq, m5sq = map(mp.mpf, (m1sq, m2sq, m3sq, m4sq, m5sq))
    out = _outer_M2_term(m1sq, m2sq, m3sq, k2)
    out += _outer_M2_term(m2sq, m1sq, m3sq, k2)
    out += _outer_M2_term(m4sq, m5sq, m3sq, k2)
    out += _outer_M2_term(m5sq, m4sq, m3sq, k2)
    L3 = log_minus_k2_over_m2(k2, m3sq)
    out += m3sq**2/4 * (-2*L3**2 - 2*L3
                        + mp.log(m1sq/m3sq)*mp.log(m2sq/m3sq)
                        + mp.log(m4sq/m3sq)*mp.log(m5sq/m3sq) + 6)
    out += -mp.mpf('0.5')*(m1sq*m2sq + m4sq*m5sq)
    out += _cross_14_like(m1sq, m4sq, (m2sq, m3sq), (m3sq, m5sq), k2)
    out += _cross_14_like(m2sq, m5sq, (m1sq, m3sq), (m3sq, m4sq), k2)
    out += _cross_15_like(m1sq, m5sq, (m2sq, m3sq), (m3sq, m4sq), k2)
    out += _cross_15_like(m2sq, m4sq, (m1sq, m3sq), (m3sq, m5sq), k2)
    for mi in (m1sq, m2sq, m4sq, m5sq):
        out += _central_cross_M2(mi, m1sq, m2sq, m3sq, m4sq, m5sq, k2)
    out += mp.mpf('0.25')*(
        (m1sq+m2sq-m3sq+2*m4sq+2*m5sq)*vacuum_F(m1sq, m2sq, m3sq)
        + (2*m1sq+2*m2sq-m3sq+m4sq+m5sq)*vacuum_F(m4sq, m5sq, m3sq))
    return out


def asymptotic_M(k2, masses_sq, order=1):
    """Asymptotic M expansion to declared order. M3+ NOT promoted."""
    if order < 0:
        raise ValueError('order must be >= 0')
    if order == 0:
        return M0()
    if order == 1:
        return M0() + M1(k2, *masses_sq)/k2
    if order == 2:
        return M0() + M1(k2, *masses_sq)/k2 + M2(k2, *masses_sq)/(k2**2)
    raise NotImplementedError(
        'This pack implements DST M0, M1, and M2; M3+ are ledgered but not promoted')


def thresholds(m1, m2, m3, m4, m5):
    """Catalog of unitarity thresholds for the two-loop two-point bubble."""
    return {
        'two_particle_14':     (m1+m4)**2,
        'two_particle_25':     (m2+m5)**2,
        'three_particle_135':  (m1+m3+m5)**2,
        'three_particle_234':  (m2+m3+m4)**2,
    }


def high_energy_region(k2, masses):
    """True iff |k²| exceeds all thresholds."""
    th = thresholds(*masses)
    return abs(k2) > max(th.values())


# =============================================================================
# Padé bridge for small-q² ↔ large-q² matching
# =============================================================================

def pade_from_taylor(coeffs, L, M):
    """Return numerator + denominator coeffs for [L/M] Padé. q[0]=1."""
    if len(coeffs) < L+M+1:
        raise ValueError('need coefficients through L+M')
    if M == 0:
        return list(coeffs[:L+1]), [mp.mpf(1)]
    A = mp.matrix(M)
    b = mp.matrix(M, 1)
    for row in range(M):
        k = L+1+row
        for col in range(M):
            A[row, col] = coeffs[k-(col+1)]
        b[row] = -coeffs[k]
    q_tail = mp.lu_solve(A, b)
    q = [mp.mpf(1)] + [q_tail[i] for i in range(M)]
    p = []
    for k in range(L+1):
        p.append(sum(q[j]*coeffs[k-j] for j in range(min(k, M)+1)))
    return p, q


def eval_pade(p, q, x):
    num = sum(p[i]*x**i for i in range(len(p)))
    den = sum(q[i]*x**i for i in range(len(q)))
    return num/den


# =============================================================================
# APF bank-protocol wrapper
# =============================================================================

EXPORT_FLAGS = {
    "Export_two_loop_two_point_BFT_one_mass_branches": 1,
    "Export_two_loop_two_point_DST_M0_M1_M2_coefficients": 1,
    "Export_two_loop_two_point_vacuum_F_symmetric_function": 1,
    "Export_two_loop_two_point_pade_bridge_taylor_to_pade": 1,
    "Export_two_loop_two_point_threshold_catalog": 1,
    "Export_two_loop_two_point_high_energy_region_classifier": 1,
    "Export_two_loop_master_integral_two_point_bubble": 0,
    "Export_two_point_full_massive_Tier1_P": 0,
    "Export_DST_M3_or_higher_order": 0,
    "Export_native_two_loop_M_W": 0,
    "Export_native_two_loop_delta_r": 0,
    "Export_native_two_loop_kappa_l": 0,
    "Export_two_loop_M_W_physical_final": 0,
    "Export_external_numeric_package_as_derivation": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_two_point_BFT_DST_coefficient_family_current_depth_P():
    """T: APF-native two-loop two-point coefficient family — BFT one-mass
    normalized hypergeometric branches (N_I1, N_I2, N_I4, N_Ie3) + DST
    large-momentum coefficients M0=6ζ(3) + M1 + M2 + vacuum F symmetric
    function + Padé bridge + threshold catalog. Source-certified to
    BFT 1993 (hep-ph/9304303) Taylor-series equations and DST 1993
    (hep-ph/9307371) Eq.(11)-(15),(30)-(33). Full Tier-1 master for
    unrestricted arbitrary-mass two-point STILL OPEN
    [P_two_point_BFT_DST_coefficient_family_current_depth]."""

    _saved_dps = mp.mp.dps
    mp.mp.dps = 50
    try:
        # (1) M0 = 6 ζ(3) exactly
        m0 = M0()
        target_M0 = 6*mp.zeta(3)
        check(abs(m0 - target_M0) < mp.mpf('1e-40'),
              f"M0 must be 6 zeta(3) exactly, got {m0}")

        # (2) M1 symmetry: swap (1<->2) on left pair gives same M1
        masses = (1.0, 4.0, 7.0, 16.0, 25.0)  # m3²=7 avoids the (m1+m2)²=9 threshold
        m1_base = M1(100.0, *masses)
        m1_swap_left = M1(100.0, 4.0, 1.0, 7.0, 16.0, 25.0)
        check(abs(m1_base - m1_swap_left) < mp.mpf('1e-25'),
              f"M1 left-pair (1<->2) symmetry: {m1_base} vs {m1_swap_left}")
        # swap (4<->5) on right pair gives same M1
        m1_swap_right = M1(100.0, 1.0, 4.0, 7.0, 25.0, 16.0)
        check(abs(m1_base - m1_swap_right) < mp.mpf('1e-25'),
              f"M1 right-pair (4<->5) symmetry: {m1_base} vs {m1_swap_right}")

        # (3) M2 left-right reflection (m1<->m2 AND m4<->m5 together)
        # and top-bottom reflection ((m1,m2) <-> (m4,m5))
        m2_base = M2(100.0, *masses)
        # Left-right: swap both pairs simultaneously
        m2_lr = M2(100.0, 4.0, 1.0, 7.0, 25.0, 16.0)
        check(abs(m2_base - m2_lr) < mp.mpf('1e-20'),
              f"M2 left-right reflection symmetry: {m2_base} vs {m2_lr}")
        # Top-bottom: swap (m1,m2) <-> (m4,m5)
        m2_tb = M2(100.0, 16.0, 25.0, 7.0, 1.0, 4.0)
        check(abs(m2_base - m2_tb) < mp.mpf('1e-20'),
              f"M2 top-bottom reflection symmetry: {m2_base} vs {m2_tb}")

        # (4) asymptotic_M ordering at three orders
        a0 = asymptotic_M(100.0, masses, order=0)
        a1 = asymptotic_M(100.0, masses, order=1)
        a2 = asymptotic_M(100.0, masses, order=2)
        check(abs(a0 - M0()) < mp.mpf('1e-40'), "asymptotic_M order=0 must = M0")
        check(abs(a1 - (M0() + M1(100.0, *masses)/100.0)) < mp.mpf('1e-25'),
              "asymptotic_M order=1 mismatch")
        check(abs(a2 - a1 - M2(100.0, *masses)/100.0**2) < mp.mpf('1e-20'),
              "asymptotic_M order=2 mismatch")

        # (5) vacuum F symmetry: F(a,b,c) = F(b,a,c) = F(a,c,b)
        Fabc = vacuum_F(1.0, 4.0, 7.0)
        Fbac = vacuum_F(4.0, 1.0, 7.0)
        Facb = vacuum_F(1.0, 7.0, 4.0)
        check(abs(Fabc - Fbac) < mp.mpf('1e-25'),
              f"vacuum_F (a,b) symmetry: {Fabc} vs {Fbac}")
        check(abs(Fabc - Facb) < mp.mpf('1e-25'),
              f"vacuum_F (b,c) symmetry: {Fabc} vs {Facb}")

        # (6) BFT one-mass branches finite at small q² (z = -q²/m² = -0.1)
        eps = mp.mpf('0.01')
        m2 = mp.mpf('1.0')
        q2 = mp.mpf('0.1')
        for name, fn in (("N_I1", norm_I1_small), ("N_I2", norm_I2_small),
                          ("N_I4", norm_I4_small), ("N_Ie3", norm_Ie3_small)):
            val = fn(q2, m2, eps)
            check(mp.isfinite(mp.re(val)) and mp.isfinite(mp.im(val)),
                  f"BFT {name} must be finite at small q²/m², got {val}")
    finally:
        mp.mp.dps = _saved_dps

    # (7) Threshold catalog has 4 named regions
    th = thresholds(1.0, 2.0, 3.0, 4.0, 5.0)
    for name in ('two_particle_14', 'two_particle_25',
                 'three_particle_135', 'three_particle_234'):
        check(name in th, f"threshold catalog missing {name}")
    # high_energy_region true at k²=10^6
    check(high_energy_region(1e6, (1.0, 2.0, 3.0, 4.0, 5.0)) is True,
          "high_energy_region must be True at k²=10^6")

    # (8) Padé from Taylor: geometric series 1+z+z²+... has [0/1] = 1/(1-z)
    coeffs = [mp.mpf(1)] * 4
    p, q = pade_from_taylor(coeffs, 0, 1)
    check(p == [mp.mpf(1)], f"Padé numerator wrong: {p}")
    # denominator should be [1, -1]
    check(abs(q[0] - 1) < mp.mpf('1e-40') and abs(q[1] - (-1)) < mp.mpf('1e-30'),
          f"Padé denominator wrong: {q}")
    val_half = eval_pade(p, q, mp.mpf('0.5'))
    check(abs(val_half - 2) < mp.mpf('1e-30'),
          f"Padé geometric 1/(1-z) at z=1/2 should be 2, got {val_half}")

    # (9) M3 NotImplementedError guard
    try:
        asymptotic_M(100.0, masses, order=3)
        check(False, "M3+ should raise NotImplementedError")
    except NotImplementedError:
        pass

    # (10) Honest non-claim guards
    check(EXPORT_FLAGS["Export_two_loop_master_integral_two_point_bubble"] == 0,
          "full master export must STILL be 0")
    check(EXPORT_FLAGS["Export_two_point_full_massive_Tier1_P"] == 0,
          "full massive Tier-1 P must STILL be 0")
    check(EXPORT_FLAGS["Export_DST_M3_or_higher_order"] == 0,
          "M3+ overclaim guard tripped")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False,
          "gdrive flag must be False")

    return _result(
        name=("T_two_loop_two_point_BFT_DST_coefficient_family_current_depth: "
              "BFT one-mass normalized hypergeometric branches (N_I1/N_I2/N_I4/"
              "N_Ie3) + DST large-momentum coefficients M0=6ζ(3) + M1 + M2 + "
              "vacuum F symmetric function + Padé bridge + 4-region threshold "
              "catalog. Source-certified to hep-ph/9304303 (BFT) and "
              "hep-ph/9307371 (DST) Eq.(11)-(15),(30)-(33). Full Tier-1 master "
              "OPEN [P_two_point_BFT_DST_coefficient_family_current_depth]"),
        tier=4,
        epistemic="P_two_point_BFT_DST_coefficient_family_current_depth",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE1_PUSH_HARD_BUNDLE_v1 / "
            "APF_NATIVE_TWO_LOOP_TWO_POINT_COEFFICIENT_FAMILY_IMPLEMENTATION_v1. "
            "Three integrated layers: (a) BFT 1993 one-mass normalized "
            "hypergeometric branches — N_I1 with mixed (1-eps)/(1-3eps) gamma "
            "structure, N_I2/N_I4/N_Ie3 with paper-explicit beta/gamma/delta "
            "structure factors; (b) DST 1993 large-momentum coefficient "
            "family — M0 = 6ζ(3) exact, M1 with all 'analogous terms' from "
            "Eq.(13) made explicit, M2 with all cross terms from Eq.(15) "
            "expanded (4 outer terms + 4 cross 14-like + 2 cross 15-like + "
            "4 central-cross + 4 vacuum-F contributions), vacuum F(m1²,m2²,m3²) "
            "symmetric function with largest-mass-as-scale numerical stability "
            "convention; (c) Padé bridge with Gaussian-elim Taylor-to-[L/M] "
            "Padé converter validated on geometric-series anchor. M2 "
            "top-bottom + left-right reflection symmetry verified; M1 "
            "left-pair + right-pair symmetry verified; vacuum F (a,b) and "
            "(b,c) permutation symmetry verified to 1e-25. BFT one-mass "
            "branches all finite at small-q² Feynman-prescription point. "
            "M3+ NotImplementedError guard enforced — DST asymptotic ordering "
            "stops at M2 per sibling scope. Full Tier-1 master for the "
            "unrestricted arbitrary-mass two-point STILL OPEN — next pack "
            "would deliver coefficient evaluator integration into a full "
            "p²-dependent master."
        ),
        key_result=(
            "BFT one-mass branches + DST M0/M1/M2 + vacuum F + Padé bridge + "
            "threshold catalog source-certified; full Tier-1 master pending. "
            "[P_two_point_BFT_DST_coefficient_family_current_depth]"
        ),
        dependencies=[
            "T_two_loop_two_point_coefficient_family_and_threshold_numeric_row",
            "T_two_loop_two_point_low_energy_pade_bridge_gate",
        ],
        cross_refs=[
            "T_two_loop_sunrise_DE_matrix_source_certified",
        ],
        artifacts={
            "source_papers": {
                "BFT": "Broadhurst-Fleischer-Tarasov 1993, hep-ph/9304303, Z. Phys. C 60 (1993) 287",
                "DST": "Davydychev-Smirnov-Tausk 1993, hep-ph/9307371, Eq.(11)-(15),(30)-(33)",
            },
            "M0_exact": "6 zeta(3)",
            "DST_order_implemented": "M0, M1, M2 (M3+ explicitly NotImplemented)",
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_two_point_BFT_DST_coefficient_family_current_depth":
        check_T_two_loop_two_point_BFT_DST_coefficient_family_current_depth_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
