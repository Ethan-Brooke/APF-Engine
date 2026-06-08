"""APF-native two-loop sunrise 2D finite-core + p²=0 Clausen boundary evaluator — Tier-4.

Source-certified implementation of the arbitrary-mass two-loop sunrise master
integral via the Adams-Bogner-Weinzierl 2014 (arXiv:1405.5640) two-dimensional
Feynman-parameter representation, plus the p²=0 Clausen/dilogarithm boundary
formula in the positive-Delta (triangle-inequality) region.

  * Adams-Bogner-Weinzierl 2014, Eq. (1)-(3): 2D arbitrary-mass sunrise integral
    + graph polynomial F_E = p_E² x1 x2 x3 + (Σ_i x_i m_i²)(x1 x2 + x2 x3 + x3 x1).
  * Adams-Bogner-Weinzierl 2014, Eq. (17)-(20): 2D second-order DE in p².
  * Adams-Bogner-Weinzierl 2014, Eq. (21)-(25): p²=0 boundary value in
    Clausen/dilog form on the positive-Delta branch.
  * Caffo-Czyz-Laporta-Remiddi 1998 (hep-th/9805118v2): companion n-dimensional
    first-order DE matrix for F0-F3 (banked separately at v24.3.140).
  * Laporta-Remiddi 2004 (hep-ph/0406160) Eq.(2.8)-(3.9): equal-mass DE +
    d=2 ↔ d=4 dimensional recurrence.

Honest non-claims: scoped at [P_two_loop_sunrise_2d_finite_core_and_boundary];
NOT full d=4 MSbar all-physical-sheets evaluator; NOT absorptive-threshold
all-region evaluator; NOT a renormalized two-loop master.

Sibling APF_NATIVE_TWO_LOOP_SUNSET_FINITE_CORE_AND_BOUNDARY_v2 via
APF_TWO_LOOP_PHASE1_CLOSURE_PUSH_BUNDLE_v2.
"""
from __future__ import annotations

import math

import mpmath as mp
import numpy as np
from numpy.polynomial.legendre import leggauss

from apf.apf_utils import check, _result


# =============================================================================
# Source-certified kernel
# =============================================================================


def _pos(x: float, name: str) -> float:
    x = float(x)
    if x <= 0:
        raise ValueError(f"{name} must be positive")
    return x


def graph_U(x1: float, x2: float, x3: float) -> float:
    """First Symanzik polynomial U = x1 x2 + x2 x3 + x3 x1."""
    return x1 * x2 + x2 * x3 + x3 * x1


def graph_F_euclidean(
    p2_E: float,
    m1sq: float,
    m2sq: float,
    m3sq: float,
    x1: float,
    x2: float,
    x3: float,
) -> float:
    """ABW Euclidean graph polynomial: F_E = p_E² x1 x2 x3 + (Σ x_i m_i²) U."""
    U = graph_U(x1, x2, x3)
    mass_linear = x1 * m1sq + x2 * m2sq + x3 * m3sq
    return p2_E * x1 * x2 * x3 + mass_linear * U


def sunrise_2d_euclidean(
    p2_E: float,
    m1sq: float,
    m2sq: float,
    m3sq: float,
    *,
    mu2: float = 1.0,
    n_quad: int = 80,
) -> float:
    """ABW 2D arbitrary-mass sunrise integral in Euclidean region via Gauss-Legendre."""
    p2_E = float(p2_E)
    if p2_E < 0:
        raise ValueError("p2_E must be Euclidean nonnegative")
    m1sq = _pos(m1sq, "m1sq")
    m2sq = _pos(m2sq, "m2sq")
    m3sq = _pos(m3sq, "m3sq")
    if n_quad < 8:
        raise ValueError("n_quad must be >= 8")
    nodes, weights = leggauss(int(n_quad))
    us = 0.5 * (nodes + 1.0)
    ws = 0.5 * weights
    total = 0.0
    for i, u in enumerate(us):
        one_minus_u = 1.0 - u
        for j, v in enumerate(us):
            x1 = u
            x2 = one_minus_u * v
            x3 = one_minus_u * (1.0 - v)
            F = graph_F_euclidean(p2_E, m1sq, m2sq, m3sq, x1, x2, x3)
            total += ws[i] * ws[j] * one_minus_u / F
    return float(mu2) * float(total)


def clausen2(theta: float) -> float:
    """Clausen function order 2 via mpmath polylog."""
    return float(mp.im(mp.polylog(2, mp.e ** (1j * theta))))


def delta_positive(m1: float, m2: float, m3: float) -> float:
    """Triangle-inequality discriminant."""
    return (m1 + m2 - m3) * (m1 - m2 + m3) * (-m1 + m2 + m3) * (m1 + m2 + m3)


def sunrise_2d_zero_boundary_clausen(
    m1: float, m2: float, m3: float, *, mu2: float = 1.0
) -> float:
    """ABW Eq.(21)-(25) p²=0 boundary value, positive-Delta branch."""
    m1 = _pos(m1, "m1")
    m2 = _pos(m2, "m2")
    m3 = _pos(m3, "m3")
    Delta = delta_positive(m1, m2, m3)
    if Delta <= 0:
        raise ValueError("Clausen boundary requires positive-Delta (triangle) branch")
    sd = math.sqrt(Delta)
    deltas = [
        -m1 * m1 + m2 * m2 + m3 * m3,
        m1 * m1 - m2 * m2 + m3 * m3,
        m1 * m1 + m2 * m2 - m3 * m3,
    ]
    alphas = []
    for d in deltas:
        a = 2.0 * math.atan2(sd, d)
        if a < 0:
            a += 2.0 * math.pi
        alphas.append(a)
    return 2.0 * float(mu2) / sd * sum(clausen2(a) for a in alphas)


def singular_points_minkowski(m1: float, m2: float, m3: float):
    """Catalog of Minkowski-t singular points."""
    m1 = _pos(m1, "m1")
    m2 = _pos(m2, "m2")
    m3 = _pos(m3, "m3")
    return {
        "threshold": (m1 + m2 + m3) ** 2,
        "pseudothreshold_12_minus_3": (m1 + m2 - m3) ** 2,
        "pseudothreshold_1_minus_2_plus_3": (m1 - m2 + m3) ** 2,
        "pseudothreshold_minus_1_plus_2_plus_3": (-m1 + m2 + m3) ** 2,
        "zero_boundary": 0.0,
    }


def classify_sunrise_region(
    p2_E: float, m1: float, m2: float, m3: float, tol: float = 1e-10
):
    """Region router."""
    pts = singular_points_minkowski(m1, m2, m3)
    t = -float(p2_E)
    for name, val in pts.items():
        if abs(t - val) <= tol * max(1.0, abs(val)):
            return {
                "region": "singular_or_boundary",
                "point": name,
                "minkowski_t": t,
                "singular_points_t": pts,
            }
    if p2_E >= 0:
        return {
            "region": "euclidean_spacelike_regular",
            "point": None,
            "minkowski_t": t,
            "singular_points_t": pts,
        }
    return {
        "region": "timelike_guarded",
        "point": None,
        "minkowski_t": t,
        "singular_points_t": pts,
    }


# =============================================================================
# Export flags + bank check
# =============================================================================

EXPORT_FLAGS = {
    "Export_two_loop_sunrise_2d_finite_core_P": 1,
    "Export_two_loop_sunrise_p2_zero_boundary_clausen_P": 1,
    "Export_two_loop_sunrise_d4_all_sheets_MSbar": 0,
    "Export_two_loop_sunrise_threshold_absorptive_all_regions": 0,
    "Export_two_loop_sunrise_full_master_renormalized": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_sunrise_2d_finite_core_and_boundary_P():
    """T: APF-native 2D arbitrary-mass sunrise finite-core evaluator + p²=0
    Clausen boundary anchor. Source-certified to Adams-Bogner-Weinzierl 2014
    Eq.(1)-(3), (17)-(20), (21)-(25). Composes with v24.3.140 CCLR DE matrix.
    Full d=4 MSbar all-sheets evaluator OPEN
    [P_two_loop_sunrise_2d_finite_core_and_boundary]."""

    # (a) p²=0 quadrature matches Clausen boundary.
    m_triple = (1.0, 1.2, 1.3)
    masses_sq = tuple(mm * mm for mm in m_triple)
    numeric_zero = sunrise_2d_euclidean(0.0, *masses_sq, n_quad=90)
    clausen_zero = sunrise_2d_zero_boundary_clausen(*m_triple)
    rel_zero = abs(numeric_zero - clausen_zero) / max(1.0, abs(clausen_zero))
    check(rel_zero < 1.5e-3,
          f"p²=0 quadrature vs Clausen boundary: numeric={numeric_zero}, clausen={clausen_zero}, rel={rel_zero}")

    # (b) Mass-permutation symmetry.
    p2_E = 1.7
    val_orig = sunrise_2d_euclidean(p2_E, 1.0, 1.44, 1.69, n_quad=54)
    val_perm1 = sunrise_2d_euclidean(p2_E, 1.44, 1.0, 1.69, n_quad=54)
    val_perm2 = sunrise_2d_euclidean(p2_E, 1.69, 1.44, 1.0, n_quad=54)
    rel1 = abs(val_orig - val_perm1) / max(1.0, abs(val_orig))
    rel2 = abs(val_orig - val_perm2) / max(1.0, abs(val_orig))
    check(max(rel1, rel2) < 3e-3, f"mass-permutation symmetry: rel1={rel1}, rel2={rel2}")

    # (c) Homogeneous scaling under (p², m², μ²) → λ·(p², m², μ²).
    lam = 2.75
    s0 = sunrise_2d_euclidean(1.3, 1.0, 1.44, 1.69, mu2=1.0, n_quad=46)
    s1 = sunrise_2d_euclidean(lam * 1.3, lam * 1.0, lam * 1.44, lam * 1.69, mu2=lam, n_quad=46)
    rel_scale = abs(s0 - s1) / max(1.0, abs(s0))
    check(rel_scale < 3e-4, f"homogeneous scaling: s0={s0}, s1={s1}, rel={rel_scale}")

    # (d) Euclidean positivity + monotone decrease with p²_E.
    z0 = sunrise_2d_euclidean(0.0, 1.0, 1.44, 1.69, n_quad=46)
    z1 = sunrise_2d_euclidean(2.0, 1.0, 1.44, 1.69, n_quad=46)
    check(z1 < z0 and z1 > 0,
          f"Euclidean positivity/monotonicity: z0={z0}, z1={z1}")

    # (e) Region router.
    reg_eucl = classify_sunrise_region(2.0, 1.0, 1.2, 1.3)
    reg_zero = classify_sunrise_region(0.0, 1.0, 1.2, 1.3)
    check(reg_eucl["region"] == "euclidean_spacelike_regular",
          f"euclidean router: got {reg_eucl['region']}")
    check(reg_zero["region"] == "singular_or_boundary",
          f"zero-boundary router: got {reg_zero['region']}")

    # (f) Honest non-claim flags.
    check(EXPORT_FLAGS["Export_two_loop_sunrise_2d_finite_core_P"] == 1,
          "2D finite-core flag must be 1")
    check(EXPORT_FLAGS["Export_two_loop_sunrise_p2_zero_boundary_clausen_P"] == 1,
          "p²=0 Clausen boundary flag must be 1")
    check(EXPORT_FLAGS["Export_two_loop_sunrise_d4_all_sheets_MSbar"] == 0,
          "d=4 all-sheets MSbar must remain 0")
    check(EXPORT_FLAGS["Export_two_loop_sunrise_threshold_absorptive_all_regions"] == 0,
          "absorptive all-regions must remain 0")
    check(EXPORT_FLAGS["Export_two_loop_sunrise_full_master_renormalized"] == 0,
          "renormalized master must remain 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False,
          "gdrive flag must be False")

    return _result(
        name=("T_two_loop_sunrise_2d_finite_core_and_boundary: "
              "ABW 2D arbitrary-mass finite-core sunrise evaluator + p²=0 "
              "Clausen/dilog boundary on positive-Delta branch. "
              "p²=0 numeric/analytic agreement to rel<1.5e-3 at (1, 1.2, 1.3); "
              "mass-permutation symmetry; homogeneous (p,m,μ²)-scaling; "
              "Euclidean positivity + monotone decrease. "
              "Source-certified to ABW 2014 Eq.(1)-(3), (17)-(20), (21)-(25). "
              "Composes with v24.3.140 CCLR DE matrix. Full d=4 MSbar all-sheets "
              "evaluator OPEN. [P_two_loop_sunrise_2d_finite_core_and_boundary]"),
        tier=4,
        epistemic="P_two_loop_sunrise_2d_finite_core_and_boundary",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE1_CLOSURE_PUSH_BUNDLE_v2 / "
            "APF_NATIVE_TWO_LOOP_SUNSET_FINITE_CORE_AND_BOUNDARY_v2. "
            "Three-piece kernel: (a) ABW 2D Feynman-parameter quadrature "
            "S(p_E²; m_i²) = μ² ∫_σ ω/F_E with F_E = p_E² x1 x2 x3 + "
            "(Σ x_i m_i²) U via Gauss-Legendre on the unit square with "
            "stick-breaking simplex parametrization x1=u, x2=(1-u)v, "
            "x3=(1-u)(1-v); (b) closed-form Clausen boundary value at p²=0 "
            "in the positive-Delta (triangle-inequality) branch — "
            "2 μ²/√Δ · (Cl2(α1) + Cl2(α2) + Cl2(α3)) with α_i derived from "
            "the three mass-squared deltas; (c) singular-point catalog "
            "(threshold + 3 pseudothresholds + zero boundary) + 3-region "
            "router. Bank check verifies p²=0 numeric vs Clausen anchor "
            "agreement at (m=1, 1.2, 1.3) to rel < 1.5e-3, mass-permutation "
            "symmetry under 3 cyclic shifts, homogeneous (p², m², μ²) → "
            "λ·(p², m², μ²) scaling, Euclidean positivity + monotone "
            "decrease with p²_E, and region-router correctness at "
            "Euclidean point + p²=0 boundary."
        ),
        key_result=(
            "ABW 2D arbitrary-mass finite sunrise core evaluator + p²=0 Clausen "
            "boundary anchor source-certified; full d=4 MSbar all-sheets master "
            "OPEN. [P_two_loop_sunrise_2d_finite_core_and_boundary]"
        ),
        dependencies=[
            "T_two_loop_sunrise_DE_matrix_source_certified",
        ],
        cross_refs=[
            "T_two_loop_two_point_BFT_DST_coefficient_family_current_depth",
        ],
        artifacts={
            "source_papers": {
                "ABW": "Adams-Bogner-Weinzierl 2014, arXiv:1405.5640, Eq.(1)-(3), (17)-(20), (21)-(25)",
                "CCLR": "Caffo-Czyz-Laporta-Remiddi 1998, hep-th/9805118 (companion DE matrix)",
                "LR2004": "Laporta-Remiddi 2004, hep-ph/0406160, Eq.(2.8)-(3.9) (d=2 ↔ d=4 recurrence)",
            },
            "p2_zero_anchor": "Clausen formula on positive-Delta branch",
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_sunrise_2d_finite_core_and_boundary":
        check_T_two_loop_sunrise_2d_finite_core_and_boundary_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
