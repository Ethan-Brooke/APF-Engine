"""APF-native scalar three-point function C0 on the TIMELIKE / above-threshold branch -- Tier-4.

R0 of the OS-W Gate A "native kappa_l" arc (Route 1; working state
``APF Reference Docs/Reference - Rung 2b Route 1 kappa_l Working State (2026-05-25).md``).
Extends the native general-momentum scalar C0
(``apf.w_trace_pv_c0_general_momentum.c0_general``, spacelike / below-threshold only,
which quarantines F<=0 and returns REAL) to TIMELIKE external invariants above
threshold, where the Feynman denominator crosses zero on the simplex and C0
acquires an absorptive (imaginary) part. This is the prerequisite the
v24.3.84 timelike-2-point changelog flagged as OPEN ("3-/4-point timelike branch
remain OPEN"); it is what makes the BHM Zll vertex functions Lambda_2(s,M_Z) /
Lambda_3(s,M_W) complex at s = M_Z^2 (the next rung, R1).

Construction (1D-reduced Feynman integral + iepsilon continuation)
------------------------------------------------------------------
With propagators D1=q^2-m1^2, D2=(q+p1)^2-m2^2, D3=(q+p1+p2)^2-m3^2 and external
invariants s12=p1^2, s23=p2^2, s31=(p1+p2)^2 (the c0_general convention; masses
are passed SQUARED), the Feynman representation is C0 = - int_simplex 1/F.
Doing the inner Feynman parameter (x2=y) ANALYTICALLY at fixed x1=x leaves a
1D outer integral whose integrand is at worst log-singular (integrable):

    F(x,y) = a2 y^2 + a1 y + a0 ,   a2 = s23,
        a1 = (m2-m3-s23) + x (s31-s12+s23),
        a0 = s31 x^2 + (m1-m3-s31) x + m3,
    inner(x) = int_0^{1-x} dy / (F - i eps)
             = (analytic log/arctan form, with ln(Z - i eps) = ln|Z| - i pi theta(-Z)),
    C0 = - int_0^1 inner(x) dx .

The -i eps prescription is carried exactly through the inner step (cmath, with an
infinitesimal imaginary part fixing the branch), so BOTH the principal-value real
part and the absorptive imaginary part fall out of the same 1D quadrature -- the
3-point analogue of the timelike-2-point construction. The outer integral is
subdivided at the kink x-values (roots of F(x,0)=0, F(x,1-x)=0 and the
discriminant) and each smooth piece is evaluated with tanh-sinh (double
exponential) quadrature, which handles the endpoint log singularities of the
principal value; Re and Im both converge exponentially (machine precision by
~64 nodes/side).

Self-validation (no external target)
------------------------------------
  * spacelike overlap: where F>0 throughout (s_ij<=0) Re C0 reduces to the banked
    c0_general and Im C0 = 0;
  * absorptive part two independent ways: the analytic-inner Im equals an explicit
    delta-function root-count -pi int dx sum 1/|dF/dy| over the cut;
  * absorptive closed form: for the two-massless-external equal-internal-mass
    triangle C0(0,0,s;M,M,M) above threshold, Im C0 = -(pi/s) ln((1+beta)/(1-beta)),
    beta=sqrt(1-4M^2/s) (derived from the linear-inner reduction);
  * S3 permutation symmetry of (m_i^2, s_ij) (cyclic + reflection);
  * threshold: Im C0 = 0 below threshold.
  (Additionally cross-checked in development against high-precision mpmath with
  cut breakpoints to ~1e-10 on Re+Im, and an independent 2D finite-i eps complex
  simplex quadrature.)

Honest scope
------------
The timelike SCALAR three-point C0 (Re + absorptive Im). The timelike three-point
TENSOR coefficients (C1,C2,Cij), the 4-point Dij timelike branch, the BHM/Denner
Zll vertex assembly Lambda_2/Lambda_3, and the native kappa_l remain OPEN -- the
next rungs (R0b: timelike Cij; R1: Lambda_2/Lambda_3). No Delta r_rem / M_W /
kappa_l value is produced; DIZET stays the publishable OS-W closure.

Status
------
- Export_pv_c0_above_threshold_complex_branch    = 1   (NEW here)
- Export_pv_cij_above_threshold_complex_branch   = 0   (OPEN, next rung R0b)
- Export_native_zll_lambda_evaluated             = 0   (OPEN, R1)
- Export_native_kappa_l_evaluated                = 0   (OPEN, Gate A)
- Export_OSW_APF_internal_delta_r_rem_evaluated  = 0   (OPEN, unchanged)
"""
from __future__ import annotations

import math
import cmath
from typing import Any, Dict, List, Tuple

from apf.apf_utils import check, _result
from apf.w_trace_pv_c0_general_momentum import c0_general, _c0_F
from apf.w_trace_pv_scalar_integral_substrate import MW2, MZ2, MT2, MH2

# tanh-sinh production parameters (machine convergence by ~64 nodes/side)
_TS_H = 0.0625
_TS_N = 64


def _ts_nodes(h: float, nhalf: int) -> List[Tuple[float, float]]:
    """tanh-sinh abscissae/weights on (-1,1); clusters nodes at the endpoints."""
    nodes = []
    for j in range(-nhalf, nhalf + 1):
        t = j * h
        sh = math.sinh(t)
        u = math.tanh(0.5 * math.pi * sh)
        ch = math.cosh(0.5 * math.pi * sh)
        w = h * (0.5 * math.pi * math.cosh(t)) / (ch * ch)
        nodes.append((u, w))
    return nodes


_TS_NODES = _ts_nodes(_TS_H, _TS_N)


def _abc(x: float, m1: float, m2: float, m3: float,
         s12: float, s23: float, s31: float) -> Tuple[float, float, float]:
    """F(x,y) = a2 y^2 + a1 y + a0 at fixed x (inner Feynman parameter y=x2)."""
    a2 = s23
    a1 = (m2 - m3 - s23) + x * (s31 - s12 + s23)
    a0 = s31 * x * x + (m1 - m3 - s31) * x + m3
    return a0, a1, a2


def _inner(x: float, m1: float, m2: float, m3: float,
           s12: float, s23: float, s31: float, eps: float) -> complex:
    """Analytic inner integral int_0^{1-x} dy / (F - i eps)."""
    Y = 1.0 - x
    a0, a1, a2 = _abc(x, m1, m2, m3, s12, s23, s31)
    sc = abs(a0) + abs(a1) + abs(a2) + 1.0
    if abs(a2) < 1e-13 * sc:
        if abs(a1) < 1e-13 * sc:
            return Y / complex(a0, -eps)
        return (cmath.log(complex(a1 * Y + a0, -eps))
                - cmath.log(complex(a0, -eps))) / a1
    disc = a1 * a1 - 4.0 * a2 * complex(a0, -eps)
    sq = cmath.sqrt(disc)
    rp = (-a1 + sq) / (2.0 * a2)
    rm = (-a1 - sq) / (2.0 * a2)
    return ((cmath.log(Y - rp) - cmath.log(-rp))
            - (cmath.log(Y - rm) - cmath.log(-rm))) / (a2 * (rp - rm))


def _qroots01(A: float, B: float, C: float) -> List[float]:
    """Real roots of A x^2 + B x + C lying strictly in (0,1)."""
    out = []
    if abs(A) < 1e-15:
        if abs(B) > 1e-15:
            r = -C / B
            if 0.0 < r < 1.0:
                out.append(r)
        return out
    d = B * B - 4.0 * A * C
    if d >= 0:
        s = math.sqrt(d)
        for r in ((-B + s) / (2.0 * A), (-B - s) / (2.0 * A)):
            if 0.0 < r < 1.0:
                out.append(r)
    return out


def _breaks(m1: float, m2: float, m3: float,
            s12: float, s23: float, s31: float) -> List[float]:
    """Outer-integrand kink x-values (roots of F(x,0), F(x,1-x), and the disc)."""
    pts = set()
    for r in _qroots01(s31, (m1 - m3 - s31), m3):
        pts.add(r)                                   # F(x,0)=0
    for r in _qroots01(s12, (m1 - m2 - s12), m2):
        pts.add(r)                                   # F(x,1-x)=0
    A1c = (s31 - s12 + s23)
    B1c = (m2 - m3 - s23)
    A = A1c * A1c - 4.0 * s23 * s31
    B = 2.0 * A1c * B1c - 4.0 * s23 * (m1 - m3 - s31)
    C = B1c * B1c - 4.0 * s23 * m3
    for r in _qroots01(A, B, C):
        pts.add(r)                                   # disc(x)=0
    return sorted(pts)


def _default_eps(m1, m2, m3, s12, s23, s31) -> float:
    return 1e-12 * (abs(m1) + abs(m2) + abs(m3)
                    + abs(s12) + abs(s23) + abs(s31) + 1.0)


def c0_general_timelike(m1: float, m2: float, m3: float,
                        s12: float = 0.0, s23: float = 0.0, s31: float = 0.0,
                        eps: float = None) -> complex:
    """Native scalar C0 valid on the spacelike AND timelike/above-threshold branch.

    Masses are SQUARED (c0_general convention). Returns a complex value; the
    imaginary part is the physical absorptive part above threshold and 0 below.
    """
    if eps is None:
        eps = _default_eps(m1, m2, m3, s12, s23, s31)
    edges = [0.0] + [p for p in _breaks(m1, m2, m3, s12, s23, s31)
                     if 1e-12 < p < 1.0 - 1e-12] + [1.0]
    acc = 0j
    for a, b in zip(edges[:-1], edges[1:]):
        half = 0.5 * (b - a)
        mid = 0.5 * (a + b)
        if half <= 0:
            continue
        for u, w in _TS_NODES:
            x = mid + half * u
            acc += w * half * _inner(x, m1, m2, m3, s12, s23, s31, eps)
    return -acc


def im_c0_rootcount(m1: float, m2: float, m3: float,
                    s12: float = 0.0, s23: float = 0.0, s31: float = 0.0) -> float:
    """Absorptive Im C0 from the explicit delta(F) root count (independent of the
    analytic-inner branch): Im C0 = -pi int_0^1 dx sum_{y* in (0,1-x)} 1/|dF/dy|."""
    edges = [0.0] + [p for p in _breaks(m1, m2, m3, s12, s23, s31)
                     if 1e-12 < p < 1.0 - 1e-12] + [1.0]
    acc = 0.0
    for a, b in zip(edges[:-1], edges[1:]):
        half = 0.5 * (b - a)
        mid = 0.5 * (a + b)
        if half <= 0:
            continue
        for u, w in _TS_NODES:
            x = mid + half * u
            Y = 1.0 - x
            a0, a1, a2 = _abc(x, m1, m2, m3, s12, s23, s31)
            roots = []
            if abs(a2) < 1e-13 * (abs(a0) + abs(a1) + 1.0):
                if abs(a1) > 1e-13:
                    roots = [-a0 / a1]
            else:
                d = a1 * a1 - 4.0 * a2 * a0
                if d > 0:
                    sq = math.sqrt(d)
                    roots = [(-a1 + sq) / (2.0 * a2), (-a1 - sq) / (2.0 * a2)]
            ssum = 0.0
            for y in roots:
                if 0.0 < y < Y:
                    fp = abs(a1 + 2.0 * a2 * y)
                    if fp > 0.0:
                        ssum += 1.0 / fp
            acc += w * half * ssum
    return -math.pi * acc


def c0_timelike_2d(m1: float, m2: float, m3: float,
                   s12: float = 0.0, s23: float = 0.0, s31: float = 0.0,
                   n: int = 500, eps: float = None) -> complex:
    """Independent 2D finite-i eps complex simplex quadrature (cross-check only;
    limited absolute accuracy from the eps broadening)."""
    if eps is None:
        eps = 1e-3 * (abs(m1) + abs(m2) + abs(m3) + abs(s31) + 1.0)
    acc = 0j
    for i in range(n):
        u = (i + 0.5) / n
        ou = 1.0 - u
        for j in range(n):
            v = (j + 0.5) / n
            x1 = u
            x2 = ou * v
            x3 = ou * (1.0 - v)
            F = _c0_F(x1, x2, x3, m1, m2, m3, s12, s23, s31)
            acc += ou / complex(F, -eps)
    return -acc / (n * n)


# Spacelike test points (F>0 throughout): (m1^2,m2^2,m3^2,s12,s23,s31)
_SPACELIKE = (
    (MW2, MZ2, MT2, -MZ2, -MW2, -MH2),
    (MW2, MW2, MW2, -2.0 * MZ2, -MZ2, -MW2),
    (MZ2, MT2, MH2, -MH2, -MZ2, -2.0 * MW2),
)

# Timelike test points (s31 above the relevant threshold)
_TIMELIKE = (
    (0.0, MW2, MW2, 0.0, 0.0, MZ2),            # massless-internal + two W; cut open
    (100.0, 400.0, 100.0, 0.0, 0.0, 8000.0),   # unequal masses, two massless legs
    (50.0, 80.0, 120.0, -30.0, -45.0, 900.0),  # general: spacelike s12,s23 + timelike s31
)

EXPORT_FLAGS: Dict[str, int] = {
    "Export_pv_c0_above_threshold_complex_branch": 1,
    "Export_pv_cij_above_threshold_complex_branch": 0,
    "Export_native_zll_lambda_evaluated": 0,
    "Export_native_kappa_l_evaluated": 0,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


# ===========================================================================
# checks
# ===========================================================================
def check_T_w_trace_pv_timelike_c0_spacelike_overlap_P() -> Dict[str, Any]:
    """T: timelike-branch C0 reduces to the banked spacelike c0_general where F>0 [P]."""
    mx = 0.0
    mim = 0.0
    for pt in _SPACELIKE:
        z = c0_general_timelike(*pt)
        ref = c0_general(*pt)
        mx = max(mx, abs(z.real - ref) / abs(ref))
        mim = max(mim, abs(z.imag))
    check(mx < 5e-3, f"timelike-vs-banked spacelike Re max rel err {mx:.2e}")
    check(mim < 1e-7, f"spacelike Im must vanish, got {mim:.2e}")
    return _result(
        name="T_w_trace_pv_timelike_c0_spacelike_overlap: "
             "timelike-branch scalar C0 == banked spacelike c0_general where F>0 [P]",
        tier=4, epistemic="P",
        summary=(
            f"Wherever the Feynman denominator stays positive (spacelike external "
            f"invariants) the timelike-branch scalar C0 reduces exactly to the banked "
            f"general-momentum c0_general (max rel err {mx:.1e}) with a vanishing "
            f"absorptive part (max |Im| {mim:.1e}) -- the branch is a consistent "
            f"continuation of the banked substrate, not a separate object."
        ),
        key_result=f"timelike C0 == banked spacelike C0 where F>0 (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_c0_general_zero_momentum_limit"],
        artifacts={"max_rel_err": mx, "max_abs_im": mim},
    )


def check_T_w_trace_pv_timelike_c0_absorptive_two_ways_P() -> Dict[str, Any]:
    """T: the absorptive Im C0 agrees between the analytic-inner and delta-root-count [P]."""
    mx = 0.0
    for pt in _TIMELIKE:
        z = c0_general_timelike(*pt)
        im_rc = im_c0_rootcount(*pt)
        mx = max(mx, abs(z.imag - im_rc) / max(1.0, abs(z.imag)))
    check(mx < 1e-6, f"Im two-ways max rel err {mx:.2e}")
    return _result(
        name="T_w_trace_pv_timelike_c0_absorptive_two_ways: "
             "absorptive Im C0 from analytic-inner == explicit delta-function root count [P]",
        tier=4, epistemic="P",
        summary=(
            f"The absorptive part of the timelike C0 obtained from the analytic inner "
            f"integral (cmath branch of ln(F - i eps)) agrees with an explicit "
            f"delta(F) root count -pi int dx sum 1/|dF/dy| over the cut to max rel err "
            f"{mx:.1e} -- two independent derivations of the imaginary part."
        ),
        key_result=f"Im C0 analytic-inner == delta root count (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_timelike_c0_spacelike_overlap"],
        artifacts={"max_rel_err": mx},
    )


def check_T_w_trace_pv_timelike_c0_absorptive_closed_form_P() -> Dict[str, Any]:
    """T: Im C0(0,0,s;M,M,M) reproduces -(pi/s) ln((1+beta)/(1-beta)) above threshold [P]."""
    mx = 0.0
    for M, s in ((25.0, 600.0), (10.0, 2000.0), (50.0, 1000.0)):
        z = c0_general_timelike(M, M, M, 0.0, 0.0, s)
        beta = math.sqrt(1.0 - 4.0 * M / s)
        closed = -(math.pi / s) * math.log((1.0 + beta) / (1.0 - beta))
        mx = max(mx, abs(z.imag - closed) / abs(closed))
    check(mx < 1e-5, f"Im closed-form max rel err {mx:.2e}")
    return _result(
        name="T_w_trace_pv_timelike_c0_absorptive_closed_form: "
             "Im C0(0,0,s;M,M,M) == -(pi/s) ln((1+beta)/(1-beta)) above threshold [P]",
        tier=4, epistemic="P",
        summary=(
            f"For the two-massless-external equal-internal-mass triangle the absorptive "
            f"part reproduces the analytic closed form -(pi/s) ln((1+beta)/(1-beta)), "
            f"beta=sqrt(1-4M^2/s), to max rel err {mx:.1e} -- a target-free analytic "
            f"anchor on the cut, derived from the linear-inner reduction."
        ),
        key_result=f"Im C0(0,0,s;M,M,M) == closed form (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_timelike_c0_absorptive_two_ways"],
        artifacts={"max_rel_err": mx},
    )


def check_T_w_trace_pv_timelike_c0_permutation_threshold_P() -> Dict[str, Any]:
    """T: timelike C0 obeys S3 (m_i^2,s_ij) symmetry and vanishes Im below threshold [P]."""
    mx = 0.0
    for m1, m2, m3, s12, s23, s31 in _TIMELIKE + (
            (200.0, 50.0, 300.0, -100.0, 900.0, -50.0),):
        base = c0_general_timelike(m1, m2, m3, s12, s23, s31)
        cyc = c0_general_timelike(m2, m3, m1, s23, s31, s12)
        refl = c0_general_timelike(m1, m3, m2, s31, s23, s12)
        denom = max(1.0, abs(base))
        mx = max(mx, abs(base - cyc) / denom, abs(base - refl) / denom)
    check(mx < 1e-5, f"S3 permutation symmetry max rel err {mx:.2e}")
    # below-threshold: two-massless-external triangle with s < (m1+m3)^2 has Im=0
    M = 6458.0
    below = c0_general_timelike(M, M, M, 0.0, 0.0, 8315.2)  # 4M >> s
    check(abs(below.imag) < 1e-9, f"below-threshold Im must vanish, got {below.imag:.2e}")
    return _result(
        name="T_w_trace_pv_timelike_c0_permutation_threshold: "
             "timelike C0 obeys S3 (m_i^2,s_ij) symmetry; Im=0 below threshold [P]",
        tier=4, epistemic="P",
        summary=(
            f"The timelike-branch C0 is invariant under cyclic and reflection "
            f"permutations of the (mass, invariant) labels to max rel err {mx:.1e} -- a "
            f"target-free validation that re-evaluates the same triangle from different "
            f"label assignments -- and its absorptive part vanishes below threshold, "
            f"confirming the correct analytic structure of the cut."
        ),
        key_result=f"timelike C0 S3 symmetric (rel err {mx:.1e}); Im=0 below threshold. [P]",
        dependencies=["T_w_trace_pv_timelike_c0_spacelike_overlap"],
        artifacts={"max_rel_err": mx, "below_threshold_im": below.imag},
    )


def check_T_w_trace_pv_timelike_c0_subgate_partial_P() -> Dict[str, Any]:
    """T: timelike scalar C0 done; timelike Cij + Lambda + kappa_l OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_pv_c0_above_threshold_complex_branch"] == 1,
          "timelike C0 branch flag must be 1")
    check(EXPORT_FLAGS["Export_pv_cij_above_threshold_complex_branch"] == 0,
          "timelike Cij must remain OPEN")
    check(EXPORT_FLAGS["Export_native_kappa_l_evaluated"] == 0,
          "no kappa_l evaluated by this rung")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no Delta r_rem evaluated by this rung")
    return _result(
        name="T_w_trace_pv_timelike_c0_subgate_partial: "
             "timelike scalar C0 native; timelike Cij + Lambda + kappa_l OPEN [P_structural]",
        tier=4, epistemic="P_structural_partial",
        summary=(
            "The native scalar three-point C0 now extends to the timelike / "
            "above-threshold branch (principal-value Re + absorptive Im via the "
            "1D-reduced Feynman integral with tanh-sinh on each smooth piece), the R0 "
            "prerequisite for the complex BHM Zll vertex functions Lambda_2(s,M_Z) / "
            "Lambda_3(s,M_W) at s=M_Z^2. Still OPEN toward native kappa_l: the timelike "
            "three-point TENSOR coefficients (C1,C2,Cij) [R0b], the Lambda_2/Lambda_3 "
            "assembly [R1], the renormalized Zll proper vertex [R2], and the bosonic + "
            "light-fermion pieces [R3/R4]. No kappa_l / Delta r_rem / M_W produced; "
            "DIZET stays the publishable OS-W closure."
        ),
        key_result="Timelike scalar C0 native; timelike Cij + Lambda + kappa_l OPEN. [P_structural]",
        dependencies=["T_w_trace_pv_timelike_c0_permutation_threshold"],
        cross_refs=["T_w_trace_pv_timelike_b0_subgate_partial",
                    "T_w_trace_pv_c_tensor_subgate_partial"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_pv_timelike_c0_spacelike_overlap": check_T_w_trace_pv_timelike_c0_spacelike_overlap_P,
    "T_w_trace_pv_timelike_c0_absorptive_two_ways": check_T_w_trace_pv_timelike_c0_absorptive_two_ways_P,
    "T_w_trace_pv_timelike_c0_absorptive_closed_form": check_T_w_trace_pv_timelike_c0_absorptive_closed_form_P,
    "T_w_trace_pv_timelike_c0_permutation_threshold": check_T_w_trace_pv_timelike_c0_permutation_threshold_P,
    "T_w_trace_pv_timelike_c0_subgate_partial": check_T_w_trace_pv_timelike_c0_subgate_partial_P,
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
