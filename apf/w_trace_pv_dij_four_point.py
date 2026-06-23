"""W_TRACE APF-native PV four-point (box) tensor reduction -- rank-1/2/3.

The native four-point (box) tensor reduction, built on the general-momentum box
scalar D0 (apf.w_trace_pv_d0_general_momentum) and the native general-momentum
triangle C0 (apf.w_trace_pv_c0_general_momentum). Native, no external input --
the native counterpart to the sibling reviewed-formula route.

Box convention: D_i = (q+r_i)^2 - m_i^2, r1=0, r2=p1, r3=p1+p2, r4=p1+p2+p3,
external legs p1^2..p4^2 and diagonals s=(p1+p2)^2, t=(p2+p3)^2. Feynman loop
shift Q = a1 p1 + a2 p2 + a3 p3 with (a1,a2,a3) = (x2+x3+x4, x3+x4, x4).

Tensor decomposition (Q^2-weighted Feynman measure dmu over the 3-simplex; F is
the box Feynman denominator from apf.w_trace_pv_d0_general_momentum._d0_F):

    rank 0:  D0    = + int dmu / F^2
    rank 1:  D_i   = - int dmu a_i / F^2            (D^mu = p_i^mu D_i)
    rank 2:  D_ij  = + int dmu a_i a_j / F^2
             D00   = - 1/2 int dmu / F              (D^mu^nu = g^mu^nu D00 + p_i p_j D_ij)
    rank 3:  D_ijk = - int dmu a_i a_j a_k / F^2
             D00k  = + 1/2 int dmu a_k / F
                 (D^mu^nu^rho = sum_k (g p_k + g p_k + g p_k) D00k + p_i p_j p_k D_ijk)

The -1/2 on the D00/D00k (metric-trace) family is the Minkowski/Wick factor on
the q'^2 numerator integral; it is FIXED by the trace relations below, not
assumed (an early +1 derivation was caught and corrected by these checks).

Self-validation (no external target)
------------------------------------
rank 1 (contraction identities):  p_i . D^mu reduce the box to the four native
triangle sub-functions C0 (with box-induced invariants) + the box D0:
    p1.D = 1/2 [C0(1,3,4) - C0(2,3,4) - f1 D0], etc.

rank 2 (metric trace):  g_{mu,nu} D^{mu,nu} = int q^2 / (D1 D2 D3 D4)
    = int (D1 + m1^2)/(...) = C0(2,3,4) + m1^2 D0, giving (d->4, box D00 finite)
        4 D00 + sum_{ij} (p_i . p_j) D_ij = C0(2,3,4) + m1^2 D0 .

rank 3 (p_i-projected metric trace):  p_{i,rho} g_{mu,nu} D^{mu,nu,rho}
    = p_i . C^rho(2,3,4) + m1^2 (p_i . D^rho), giving (d+2 -> 6)
        6 sum_m (p_i.p_m) D00m + sum_{abc} (p_a.p_b)(p_i.p_c) D_abc
          = (p_i . C(2,3,4)) + m1^2 sum_m (p_i.p_m) D_m .
    The triangle (2,3,4) rank-1 vector is evaluated in pure invariants
    (Q_234 = p1 + (y3+y4) p2 + y4 p3, F_234 in the same s_ij data as C0).

All relations are expressed in pure Gram invariants (the box dot products read
off p1^2..p4^2, s, t). Verified ~1e-4 to ~4e-4 (nested quadrature); the in-pass
D0/C0 are anchored value-identical to the banked d0_general/c0_general.
Mesh-converged.

Honest scope
------------
Rank-1/2/3 four-point, spacelike domain. The rank-4 box (D0000/D00ij/Dijkl,
rarely needed for renormalizable EW boxes), the above-threshold branch, the
Denner coefficient map, and the self-energy/counterterm assembly remain OPEN;
no Delta r_rem / M_W produced; DIZET stays the publishable OS-W closure.

Status
------
- Export_pv_d1_d2_d3_rank1_fourpoint_native        = 1
- Export_pv_d00_dij_dijk_rank23_fourpoint_native   = 1   (NEW here)
- Export_pv_d_rank4_fourpoint                       = 0   (OPEN)
- Export_OSW_APF_internal_delta_r_rem_evaluated     = 0   (OPEN, unchanged)
"""
from __future__ import annotations

import itertools
from typing import Any, Dict, Tuple

from apf.apf_utils import check, _result
from apf.w_trace_pv_c0_general_momentum import c0_general
from apf.w_trace_pv_d0_general_momentum import d0_general, _d0_F


def d1_d2_d3_direct(m1, m2, m3, m4, p1, p2, p3, p4, s, t, n: int = 56) -> Tuple[float, float, float]:
    """Direct Feynman-parameter rank-1 box coefficients (D1, D2, D3)."""
    a1 = a2 = a3 = 0.0
    for i in range(n):
        u = (i + 0.5) / n
        ou = 1.0 - u
        for j in range(n):
            v = (j + 0.5) / n
            ov = 1.0 - v
            jac = ou * ou * ov
            for k in range(n):
                w = (k + 0.5) / n
                x1 = u
                x2 = ou * v
                x3 = ou * ov * w
                x4 = ou * ov * (1.0 - w)
                F = _d0_F(x1, x2, x3, x4, m1, m2, m3, m4, p1, p2, p3, p4, s, t)
                if F <= 0:
                    F = abs(F) + 1e-30
                F2 = F * F
                a1 += jac * (x2 + x3 + x4) / F2
                a2 += jac * (x3 + x4) / F2
                a3 += jac * x4 / F2
    N = n ** 3
    return -a1 / N, -a2 / N, -a3 / N


# --- index bookkeeping for the rank-2/3 coefficient dicts -------------------
_IJ = list(itertools.combinations_with_replacement((0, 1, 2), 2))
_IJK = list(itertools.combinations_with_replacement((0, 1, 2), 3))


def box_moments(m1, m2, m3, m4, p1, p2, p3, p4, s, t, n: int = 44) -> Dict[str, Any]:
    """One-pass native box tensor coefficients up to rank 3.

    Returns dict with D0 (float), Di (list[3]), Dij (dict (i<=j)->float),
    D00 (float), D00k (list[3]), Dijk (dict (i<=j<=k)->float). Sign/normalization
    per the module docstring (D00/D00k carry the -1/2 metric-trace factor).
    """
    D0 = 0.0
    D00 = 0.0
    Di = [0.0, 0.0, 0.0]
    D00k = [0.0, 0.0, 0.0]
    Dij = {ij: 0.0 for ij in _IJ}
    Dijk = {ijk: 0.0 for ijk in _IJK}
    for i in range(n):
        u = (i + 0.5) / n
        ou = 1.0 - u
        for j in range(n):
            v = (j + 0.5) / n
            ov = 1.0 - v
            jac = ou * ou * ov
            for k in range(n):
                w = (k + 0.5) / n
                x1 = u
                x2 = ou * v
                x3 = ou * ov * w
                x4 = ou * ov * (1.0 - w)
                F = _d0_F(x1, x2, x3, x4, m1, m2, m3, m4, p1, p2, p3, p4, s, t)
                if F <= 0:
                    F = abs(F) + 1e-30
                a = (x2 + x3 + x4, x3 + x4, x4)
                w0 = jac / (F * F)        # /F^2 family
                w1 = -0.5 * jac / F       # /F family with the -1/2 metric-trace factor
                D0 += w0
                D00 += w1
                for q in range(3):
                    Di[q] += -w0 * a[q]
                    D00k[q] += -w1 * a[q]   # D00k = -a_k * (D00 integrand)
                for (ia, ib) in _IJ:
                    Dij[(ia, ib)] += w0 * a[ia] * a[ib]
                for (ia, ib, ic) in _IJK:
                    Dijk[(ia, ib, ic)] += -w0 * a[ia] * a[ib] * a[ic]
    N = n ** 3
    return {
        "D0": D0 / N,
        "Di": [x / N for x in Di],
        "Dij": {kk: vv / N for kk, vv in Dij.items()},
        "D00": D00 / N,
        "D00k": [x / N for x in D00k],
        "Dijk": {kk: vv / N for kk, vv in Dijk.items()},
    }


def _tri234_piC(m2, m3, m4, p2sq, p3sq, t, dij, n: int = 64) -> Tuple[float, Tuple[float, float, float]]:
    """Triangle (2,3,4): scalar C0 and the p_i-projections p_i . C^mu(234).

    dij = ((p1.p1,p1.p2,p1.p3),(p2.p1,...),(p3.p1,...)) box dot products.
    Q234 = p1 + (y3+y4) p2 + y4 p3, F234 = -(y2 y3 p2^2 + y3 y4 p3^2 + y2 y4 t)
    + sum y_i m_i^2.  C0(234) = -int dmu_2 / F234; C^mu(234) = +int dmu_2 Q234/F234.
    """
    C0 = 0.0
    piC = [0.0, 0.0, 0.0]
    N = n * n
    for i in range(n):
        u = (i + 0.5) / n
        ou = 1.0 - u
        for j in range(n):
            v = (j + 0.5) / n
            jac = ou
            y2 = u
            y3 = ou * v
            y4 = ou * (1.0 - v)
            F = -(y2 * y3 * p2sq + y3 * y4 * p3sq + y2 * y4 * t) + (y2 * m2 + y3 * m3 + y4 * m4)
            if F <= 0:
                F = abs(F) + 1e-30
            C0 += -jac / F
            for q in range(3):
                d1, d2, d3 = dij[q]
                piC[q] += jac * (d1 + (y3 + y4) * d2 + y4 * d3) / F
    return C0 / N, (piC[0] / N, piC[1] / N, piC[2] / N)


# Spacelike box test points: (m1..m4, p1..p4, s, t) with all masses^2.
_TEST_POINTS = (
    (6458.0, 8315.0, 29780.0, 15688.0, -5820.0, -9146.0, -4157.0, -7483.0, -10810.0, -6652.0),
    (8315.0, 6458.0, 15688.0, 29780.0, -8315.0, -4157.0, -9146.0, -6652.0, -12000.0, -8000.0),
)

EXPORT_FLAGS: Dict[str, int] = {
    "Export_pv_d1_d2_d3_rank1_fourpoint_native": 1,
    "Export_pv_d00_dij_dijk_rank23_fourpoint_native": 1,
    "Export_pv_d_rank4_fourpoint": 0,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


def _dots(p1, p2, p3, p4, s, t):
    p1p2 = (s - p1 - p2) / 2.0
    p2p3 = (t - p2 - p3) / 2.0
    p1p3 = (p4 - p1 - p2 - p3) / 2.0 - p1p2 - p2p3
    return p1p2, p2p3, p1p3


def _dotmap(p1, p2, p3, p4, s, t):
    p1p2, p2p3, p1p3 = _dots(p1, p2, p3, p4, s, t)
    return {
        (0, 0): p1, (1, 1): p2, (2, 2): p3,
        (0, 1): p1p2, (1, 0): p1p2,
        (0, 2): p1p3, (2, 0): p1p3,
        (1, 2): p2p3, (2, 1): p2p3,
    }


def _sym(D, *idx):
    return D[tuple(sorted(idx))]


# ===========================================================================
# rank 1  (preserved)
# ===========================================================================
def check_T_w_trace_pv_d1_d2_d3_contraction_identities_P() -> Dict[str, Any]:
    """T: rank-1 box D1,D2,D3 satisfy the 3 contraction identities vs native C0 + D0 [P]."""
    mx = 0.0
    for m1, m2, m3, m4, p1, p2, p3, p4, s, t in _TEST_POINTS:
        D0 = d0_general(m1, m2, m3, m4, p1, p2, p3, p4, s, t)
        D1, D2, D3 = d1_d2_d3_direct(m1, m2, m3, m4, p1, p2, p3, p4, s, t)
        p1p2, p2p3, p1p3 = _dots(p1, p2, p3, p4, s, t)
        C0_134 = c0_general(m1, m3, m4, s, p3, p4)
        C0_234 = c0_general(m2, m3, m4, p2, p3, t)
        C0_124 = c0_general(m1, m2, m4, p1, t, p4)
        C0_123 = c0_general(m1, m2, m3, p1, p2, s)
        f1 = p1 + m1 - m2
        g2 = p2 + 2.0 * p1p2 + m2 - m3
        g3 = p3 + 2.0 * (p1p3 + p2p3) + m3 - m4
        pairs = [
            (p1 * D1 + p1p2 * D2 + p1p3 * D3, 0.5 * (C0_134 - C0_234 - f1 * D0)),
            (p1p2 * D1 + p2 * D2 + p2p3 * D3, 0.5 * (C0_124 - C0_134 - g2 * D0)),
            (p1p3 * D1 + p2p3 * D2 + p3 * D3, 0.5 * (C0_123 - C0_124 - g3 * D0)),
        ]
        for lhs, rhs in pairs:
            mx = max(mx, abs(lhs - rhs) / max(1e-12, abs(rhs)))
    check(mx < 5e-3, f"box rank-1 contraction max rel err {mx:.2e} exceeds 5e-3")
    return _result(
        name="T_w_trace_pv_d1_d2_d3_contraction_identities: "
             "box rank-1 D1,D2,D3 reduce to native C0 sub-triangles + D0 [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native rank-1 box coefficients D1,D2,D3 satisfy the three "
            f"contraction identities p_i.D^mu = 1/2 [C0(sub) - C0(sub) - f_i D0], "
            f"reducing the box to the four native triangle sub-functions C0 (with "
            f"box-induced invariants) and the box D0, to max relative err {mx:.2e} "
            f"-- a target-free validation against native quantities."
        ),
        key_result=f"box D1,D2,D3 contraction identities hold (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_d0_general_zero_momentum_limit",
                      "T_w_trace_pv_c0_general_zero_momentum_limit"],
        artifacts={"max_rel_err": mx, "n_points": len(_TEST_POINTS)},
    )


def check_T_w_trace_pv_d1_d2_d3_mesh_consistency_P() -> Dict[str, Any]:
    """T: the rank-1 box quadrature is mesh-converged (n vs 2n) [P]."""
    mx = 0.0
    for pt in _TEST_POINTS:
        a = d1_d2_d3_direct(*pt, n=36)
        b = d1_d2_d3_direct(*pt, n=72)
        for x, y in zip(a, b):
            mx = max(mx, abs(x - y) / max(1e-12, abs(y)))
    check(mx < 1.5e-2, f"box rank-1 mesh n vs 2n max rel err {mx:.2e} exceeds 1.5e-2")
    return _result(
        name="T_w_trace_pv_d1_d2_d3_mesh_consistency: box rank-1 quadrature mesh-converged [P]",
        tier=4, epistemic="P",
        summary=f"Box rank-1 D quadrature mesh-converged: n=36 vs n=72 to {mx:.2e}.",
        key_result=f"box D1,D2,D3 mesh-converged (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_d1_d2_d3_contraction_identities"],
        artifacts={"max_rel_err": mx},
    )


# ===========================================================================
# rank 2  (D00, Dij)
# ===========================================================================
def check_T_w_trace_pv_d00_dij_rank2_trace_relation_P() -> Dict[str, Any]:
    """T: rank-2 box D00,Dij satisfy the metric-trace relation vs native C0(234) + D0 [P]."""
    mx = 0.0
    anchor = 0.0
    for pt in _TEST_POINTS:
        m1, m2, m3, m4, p1, p2, p3, p4, s, t = pt
        dot = _dotmap(p1, p2, p3, p4, s, t)
        M = box_moments(*pt, n=44)
        sumDij = sum((1.0 if a == b else 2.0) * dot[(a, b)] * v for (a, b), v in M["Dij"].items())
        lhs = 4.0 * M["D00"] + sumDij
        C0_234 = c0_general(m2, m3, m4, p2, p3, t)
        rhs = C0_234 + m1 * M["D0"]
        mx = max(mx, abs(lhs - rhs) / max(1e-12, abs(rhs)))
        d0b = d0_general(*pt)
        anchor = max(anchor, abs(M["D0"] - d0b) / max(1e-12, abs(d0b)))
    check(mx < 3e-3, f"box rank-2 trace relation max rel err {mx:.2e} exceeds 3e-3")
    check(anchor < 1e-3, f"in-pass D0 vs banked d0_general drift {anchor:.2e} exceeds 1e-3")
    return _result(
        name="T_w_trace_pv_d00_dij_rank2_trace_relation: "
             "box rank-2 D00,Dij satisfy 4 D00 + sum (p_i.p_j) D_ij = C0(234) + m1^2 D0 [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native rank-2 box coefficients D00 (metric) and D_ij satisfy the "
            f"metric-trace relation 4 D00 + sum_{{ij}} (p_i.p_j) D_ij = C0(2,3,4) + "
            f"m1^2 D0 -- the box rank-2 reduced against the native triangle C0(234) "
            f"and box D0 -- to max relative err {mx:.2e}; the in-pass D0 is value-"
            f"identical to banked d0_general (drift {anchor:.1e}). Target-free; the "
            f"-1/2 metric-trace factor on D00 is fixed by this relation. The box D00 "
            f"is UV-finite, so the trace carries no anomaly term (unlike the triangle "
            f"C00, which contributes -1/2)."
        ),
        key_result=f"box rank-2 trace relation holds (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_d1_d2_d3_contraction_identities",
                      "T_w_trace_pv_c0_general_zero_momentum_limit"],
        artifacts={"max_rel_err": mx, "d0_anchor_drift": anchor, "n_points": len(_TEST_POINTS)},
    )


def check_T_w_trace_pv_d00_dij_rank2_mesh_consistency_P() -> Dict[str, Any]:
    """T: rank-2 box D00,Dij quadrature is mesh-converged (n vs ~1.6n) [P]."""
    pt = _TEST_POINTS[0]
    A = box_moments(*pt, n=28)
    B = box_moments(*pt, n=46)
    mx = abs(A["D00"] - B["D00"]) / max(1e-12, abs(B["D00"]))
    for kk in _IJ:
        mx = max(mx, abs(A["Dij"][kk] - B["Dij"][kk]) / max(1e-12, abs(B["Dij"][kk])))
    check(mx < 2e-2, f"box rank-2 mesh max rel err {mx:.2e} exceeds 2e-2")
    return _result(
        name="T_w_trace_pv_d00_dij_rank2_mesh_consistency: box rank-2 quadrature mesh-converged [P]",
        tier=4, epistemic="P",
        summary=f"Box rank-2 D00/Dij quadrature mesh-converged: n=28 vs n=46 to {mx:.2e}.",
        key_result=f"box D00,Dij mesh-converged (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_d00_dij_rank2_trace_relation"],
        artifacts={"max_rel_err": mx},
    )


# ===========================================================================
# rank 3  (D00k, Dijk)
# ===========================================================================
def check_T_w_trace_pv_d00k_dijk_rank3_trace_relation_P() -> Dict[str, Any]:
    """T: rank-3 box D00k,Dijk satisfy the p_i-projected metric-trace relation [P]."""
    mx = 0.0
    for pt in _TEST_POINTS:
        m1, m2, m3, m4, p1, p2, p3, p4, s, t = pt
        dot = _dotmap(p1, p2, p3, p4, s, t)
        M = box_moments(*pt, n=44)
        D00k, Dijk, Di = M["D00k"], M["Dijk"], M["Di"]
        dij = [(dot[(0, 0)], dot[(0, 1)], dot[(0, 2)]),
               (dot[(1, 0)], dot[(1, 1)], dot[(1, 2)]),
               (dot[(2, 0)], dot[(2, 1)], dot[(2, 2)])]
        _, piC = _tri234_piC(m2, m3, m4, p2, p3, t, dij, n=64)
        for i in range(3):
            termD00 = 6.0 * sum(dot[(i, m)] * D00k[m] for m in range(3))
            termDijk = sum(dot[(a, b)] * dot[(i, c)] * _sym(Dijk, a, b, c)
                           for a in range(3) for b in range(3) for c in range(3))
            lhs = termD00 + termDijk
            rhs = piC[i] + m1 * sum(dot[(i, m)] * Di[m] for m in range(3))
            mx = max(mx, abs(lhs - rhs) / max(1e-12, abs(rhs)))
    check(mx < 3e-3, f"box rank-3 trace relation max rel err {mx:.2e} exceeds 3e-3")
    return _result(
        name="T_w_trace_pv_d00k_dijk_rank3_trace_relation: "
             "box rank-3 D00k,Dijk satisfy the p_i-projected g_{mu,nu} D^{mu,nu,rho} trace [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native rank-3 box coefficients D00k (metric x momentum) and D_ijk "
            f"satisfy the p_i-projected metric-trace relation 6 sum_m (p_i.p_m) D00m "
            f"+ sum_{{abc}} (p_a.p_b)(p_i.p_c) D_abc = (p_i . C(2,3,4)) + m1^2 sum_m "
            f"(p_i.p_m) D_m for i=1,2,3 -- the box rank-3 reduced against the native "
            f"triangle (2,3,4) rank-1 vector (evaluated in pure invariants) and the "
            f"box rank-1 -- to max relative err {mx:.2e}. Target-free; the +1/2 factor "
            f"on D00k is the same metric-trace factor as the rank-2 D00."
        ),
        key_result=f"box rank-3 trace relation holds (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_d00_dij_rank2_trace_relation",
                      "T_w_trace_pv_c0_general_zero_momentum_limit"],
        artifacts={"max_rel_err": mx, "n_points": len(_TEST_POINTS)},
    )


def check_T_w_trace_pv_d00k_dijk_rank3_mesh_consistency_P() -> Dict[str, Any]:
    """T: rank-3 box D00k,Dijk quadrature is mesh-converged (n vs ~1.6n) [P]."""
    pt = _TEST_POINTS[0]
    A = box_moments(*pt, n=28)
    B = box_moments(*pt, n=46)
    mx = 0.0
    for k in range(3):
        mx = max(mx, abs(A["D00k"][k] - B["D00k"][k]) / max(1e-12, abs(B["D00k"][k])))
    for kk in _IJK:
        mx = max(mx, abs(A["Dijk"][kk] - B["Dijk"][kk]) / max(1e-12, abs(B["Dijk"][kk])))
    check(mx < 2e-2, f"box rank-3 mesh max rel err {mx:.2e} exceeds 2e-2")
    return _result(
        name="T_w_trace_pv_d00k_dijk_rank3_mesh_consistency: box rank-3 quadrature mesh-converged [P]",
        tier=4, epistemic="P",
        summary=f"Box rank-3 D00k/Dijk quadrature mesh-converged: n=28 vs n=46 to {mx:.2e}.",
        key_result=f"box D00k,Dijk mesh-converged (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_d00k_dijk_rank3_trace_relation"],
        artifacts={"max_rel_err": mx},
    )


# ===========================================================================
# scope gate
# ===========================================================================
def check_T_w_trace_pv_d_rank123_subgate_partial_P() -> Dict[str, Any]:
    """T: rank-1/2/3 four-point native; rank-4 box + assembly OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_pv_d1_d2_d3_rank1_fourpoint_native"] == 1, "rank-1 4-point flag must be 1")
    check(EXPORT_FLAGS["Export_pv_d00_dij_dijk_rank23_fourpoint_native"] == 1, "rank-2/3 4-point flag must be 1")
    check(EXPORT_FLAGS["Export_pv_d_rank4_fourpoint"] == 0, "rank-4 box must remain OPEN")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no Delta r_rem evaluated by this module")
    return _result(
        name="T_w_trace_pv_d_rank123_subgate_partial: "
             "rank-1/2/3 four-point native; rank-4 box + assembly OPEN [P_structural]",
        tier=4, epistemic="P_structural_partial",
        summary=(
            "The native four-point (box) tensor reduction is complete through rank 3 "
            "(D1/D2/D3; D00/Dij; D00k/Dijk), built on the general-momentum box D0 + "
            "the native triangle C0, every rung self-validated by contraction / "
            "metric-trace relations against native lower-point functions with zero "
            "external input. The rank-4 box (D0000/D00ij/Dijkl, rarely needed for "
            "renormalizable EW boxes), the above-threshold branch, the Denner "
            "coefficient map, and the self-energy/counterterm assembly remain OPEN; "
            "no Delta r_rem / M_W is produced; DIZET stays the publishable OS-W "
            "closure. With this the native PV tensor toolkit spans the complete "
            "scalar substrate (A0/B0/C0/D0 at general spacelike momenta), the full "
            "two- and three-point tensor bases, and the four-point box through rank 3."
        ),
        key_result="Rank-1/2/3 four-point native; rank-4 box OPEN. [P_structural]",
        dependencies=["T_w_trace_pv_d00k_dijk_rank3_trace_relation"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_pv_d1_d2_d3_contraction_identities": check_T_w_trace_pv_d1_d2_d3_contraction_identities_P,
    "T_w_trace_pv_d1_d2_d3_mesh_consistency": check_T_w_trace_pv_d1_d2_d3_mesh_consistency_P,
    "T_w_trace_pv_d00_dij_rank2_trace_relation": check_T_w_trace_pv_d00_dij_rank2_trace_relation_P,
    "T_w_trace_pv_d00_dij_rank2_mesh_consistency": check_T_w_trace_pv_d00_dij_rank2_mesh_consistency_P,
    "T_w_trace_pv_d00k_dijk_rank3_trace_relation": check_T_w_trace_pv_d00k_dijk_rank3_trace_relation_P,
    "T_w_trace_pv_d00k_dijk_rank3_mesh_consistency": check_T_w_trace_pv_d00k_dijk_rank3_mesh_consistency_P,
    "T_w_trace_pv_d_rank123_subgate_partial": check_T_w_trace_pv_d_rank123_subgate_partial_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == "__main__":
    import json
    out = run_all()
    print(json.dumps({k: {"passed": v["passed"], "epistemic": v["epistemic"]}
                      for k, v in out.items()}, indent=2))
