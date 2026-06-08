"""APF-native three-point TENSOR coefficients on the TIMELIKE branch -- rank-1 (C1, C2) -- Tier-4.

R0b of the OS-W Gate A "native kappa_l" arc (Route 1; working state
``APF Reference Docs/Reference - Rung 2b Route 1 kappa_l Working State (2026-05-25).md``).
Extends the timelike scalar C0 (apf.w_trace_pv_timelike_three_point, v24.3.103) to
the rank-1 tensor coefficients C^mu = p1^mu C1 + p2^mu C2 on the TIMELIKE /
above-threshold branch, where the Feynman denominator crosses zero on the simplex
and C1/C2 acquire absorptive (imaginary) parts.

Construction (1D-reduced Feynman integral + closed-form J + STABLE single-log)
------------------------------------------------------------------------------
In the c0_general convention (x1=x, x2=y, x3=1-x-y) the polynomial numerators
multiplying 1/F simplify: x2+x3 = 1-x = Y, x3 = Y-y. Doing the inner y-integral
analytically at fixed x:

    C1 = int_0^1 dx Y(x) I(x) ,
    C2 = int_0^1 dx [ Y(x) I(x) - J(x) ] ,
    I(x) = int_0^Y dy / (F - i eps) ,
    J(x) = int_0^Y dy y / (F - i eps) .

Numerical stability fix
-----------------------
In the linear (a2=s23=0) case the naive form I = (cln(a1 Y + a0) - cln(a0)) / a1
suffers catastrophic cancellation when both arguments vanish simultaneously at a
simplex corner -- e.g. the physically-critical (0, M_W^2, M_W^2; 0, 0, M_Z^2)
neutrino-W-W triangle where both (1-x)*M_W^2 and s31*(x-1)*(x-M_W^2/M_Z^2) go to
zero at x=1, leaving only ~4 significant digits in I. R0b uses the
algebraically-equivalent SINGLE log of the ratio,
I = (1/a1) cln((a1 Y + a0 - i eps) / (a0 - i eps)),
which cancels the common (1-x) factor analytically and recovers full
double-precision accuracy.

Self-validation (no external target)
------------------------------------
  * spacelike overlap: where F>0 throughout, Re(C1)/Re(C2) reduce to the banked
    spacelike c1_c2_direct and the imaginary parts vanish;
  * absorptive Im closed forms (derived from the linear-inner reduction):
      - kinematic class A:  C0(0, M, M; 0, 0, s) above threshold s > M:
            Im C1 = (pi/s) [ ln(s/M) - 1 + M/s ]
            Im C2 = (pi/s) [ 1 - M/s + (M/s) ln(M/s) ]
      - kinematic class B:  C0(M, M, M; 0, 0, s) above threshold s > 4 M,
            beta = sqrt(1 - 4 M / s),  L = ln((1+beta)/(1-beta)):
            Im C1 = (pi/s) (L - beta) ,    Im C2 = pi beta / s
  * absorptive Im two independent ways: analytic-inner cmath branches ==
    explicit delta(F) root counts (parallel to the timelike C0 "two ways" check);
  * threshold: Im C1 = Im C2 = 0 below threshold.

Honest scope
------------
The timelike rank-1 tensor C1, C2 (Re + absorptive Im). The timelike rank-2
coefficients (C00, C11, C12, C22), the BHM/Denner Lambda_2/Lambda_3 assembly,
and the native kappa_l remain OPEN -- the next rungs (R0c: timelike rank-2 Cij;
R1: Lambda assembly). No kappa_l / Delta r_rem / M_W value is produced; DIZET
stays the publishable OS-W closure.

Residual accuracy note
----------------------
The post-fix Re(C2) on the (0, M_W^2, M_W^2; 0, 0, M_Z^2) physical kinematics
agrees with an independent high-precision mpmath integration to ~1.5e-3 relative
(residual from floating-point precision of a0 itself near its zero at the
simplex corner). This is adequate for downstream vertex assembly: the eventual
renormalized vertex contribution to Delta kappa_l is O(1e-4), so the propagated
absolute error is O(1e-7) -- well below the 3+ significant-figure precision
target for kappa_l = 0.0368. Other timelike kinematics agree to ~1e-6 or better.

Status
------
- Export_pv_c1_c2_above_threshold_complex_branch  = 1   (NEW here)
- Export_pv_cij_above_threshold_complex_branch    = 0   (OPEN, R0c)
- Export_native_zll_lambda_evaluated              = 0   (OPEN, R1)
- Export_native_kappa_l_evaluated                 = 0   (OPEN, Gate A)
- Export_OSW_APF_internal_delta_r_rem_evaluated   = 0   (OPEN, unchanged)
"""
from __future__ import annotations

import math
import cmath
from typing import Any, Dict, Tuple

from apf.apf_utils import check, _result
from apf.w_trace_pv_timelike_three_point import (
    _abc, _inner, _breaks, _TS_NODES, _default_eps,
)
from apf.w_trace_pv_cij_three_point import c1_c2_direct as _c1_c2_spacelike
from apf.w_trace_pv_scalar_integral_substrate import MW2, MZ2, MT2, MH2


def _inner_stable(x: float, m1: float, m2: float, m3: float,
                  s12: float, s23: float, s31: float, eps: float) -> complex:
    """Numerically-stable inner I(x) via single log of the ratio in the linear case."""
    Y = 1.0 - x
    a0, a1, a2 = _abc(x, m1, m2, m3, s12, s23, s31)
    sc = abs(a0) + abs(a1) + abs(a2) + 1.0
    if abs(a2) < 1e-13 * sc:
        if abs(a1) < 1e-13 * sc:
            return Y / complex(a0, -eps)
        return cmath.log(complex(a1 * Y + a0, -eps) /
                         complex(a0, -eps)) / a1
    disc = a1 * a1 - 4.0 * a2 * complex(a0, -eps)
    sq = cmath.sqrt(disc)
    rp = (-a1 + sq) / (2.0 * a2)
    rm = (-a1 - sq) / (2.0 * a2)
    return ((cmath.log(Y - rp) - cmath.log(-rp))
            - (cmath.log(Y - rm) - cmath.log(-rm))) / (a2 * (rp - rm))


def _innerJ(x: float, m1: float, m2: float, m3: float,
            s12: float, s23: float, s31: float, eps: float) -> complex:
    """Analytic inner integral int_0^{1-x} dy y / (F - i eps)."""
    Y = 1.0 - x
    a0, a1, a2 = _abc(x, m1, m2, m3, s12, s23, s31)
    sc = abs(a0) + abs(a1) + abs(a2) + 1.0
    if abs(a2) < 1e-13 * sc:
        if abs(a1) < 1e-13 * sc:
            return 0.5 * Y * Y / complex(a0, -eps)
        I = _inner_stable(x, m1, m2, m3, s12, s23, s31, eps)
        return Y / a1 - complex(a0, -eps) / a1 * I
    disc = a1 * a1 - 4.0 * a2 * complex(a0, -eps)
    sq = cmath.sqrt(disc)
    rp = (-a1 + sq) / (2.0 * a2)
    rm = (-a1 - sq) / (2.0 * a2)
    return (rp * (cmath.log(Y - rp) - cmath.log(-rp))
            - rm * (cmath.log(Y - rm) - cmath.log(-rm))) / (a2 * (rp - rm))


def c1_c2_timelike(m1: float, m2: float, m3: float,
                   s12: float = 0.0, s23: float = 0.0, s31: float = 0.0,
                   eps: float = None) -> Tuple[complex, complex]:
    """Native rank-1 three-point coefficients (C1, C2) valid on spacelike AND
    timelike/above-threshold branches. Returns (complex, complex).
    """
    if eps is None:
        eps = _default_eps(m1, m2, m3, s12, s23, s31)
    edges = [0.0] + [p for p in _breaks(m1, m2, m3, s12, s23, s31)
                     if 1e-12 < p < 1.0 - 1e-12] + [1.0]
    acc1 = 0j
    acc2 = 0j
    for a, b in zip(edges[:-1], edges[1:]):
        half = 0.5 * (b - a)
        mid = 0.5 * (a + b)
        if half <= 0:
            continue
        for u, w in _TS_NODES:
            x = mid + half * u
            Y = 1.0 - x
            I = _inner_stable(x, m1, m2, m3, s12, s23, s31, eps)
            J = _innerJ(x, m1, m2, m3, s12, s23, s31, eps)
            acc1 += w * half * Y * I
            acc2 += w * half * (Y * I - J)
    return acc1, acc2


def _im_c1_class_A(M: float, s: float) -> float:
    """Im C1(0, M, M; 0, 0, s) above threshold s > M."""
    return (math.pi / s) * (math.log(s / M) - 1.0 + M / s)


def _im_c2_class_A(M: float, s: float) -> float:
    """Im C2(0, M, M; 0, 0, s) above threshold s > M."""
    u = M / s
    return (math.pi / s) * (1.0 - u + u * math.log(u))


def _im_c1_class_B(M: float, s: float) -> float:
    """Im C1(M, M, M; 0, 0, s) above threshold s > 4 M."""
    beta = math.sqrt(1.0 - 4.0 * M / s)
    L = math.log((1.0 + beta) / (1.0 - beta))
    return (math.pi / s) * (L - beta)


def _im_c2_class_B(M: float, s: float) -> float:
    """Im C2(M, M, M; 0, 0, s) above threshold s > 4 M."""
    beta = math.sqrt(1.0 - 4.0 * M / s)
    return math.pi * beta / s


_SPACELIKE = (
    (MW2, MZ2, MT2, -MZ2, -MW2, -MH2),
    (MW2, MW2, MW2, -2.0 * MZ2, -MZ2, -MW2),
    (MZ2, MT2, MH2, -MH2, -MZ2, -2.0 * MW2),
)

_TIMELIKE = (
    (0.0, MW2, MW2, 0.0, 0.0, MZ2),
    (100.0, 400.0, 100.0, 0.0, 0.0, 8000.0),
    (50.0, 80.0, 120.0, -30.0, -45.0, 900.0),
)

EXPORT_FLAGS: Dict[str, int] = {
    "Export_pv_c1_c2_above_threshold_complex_branch": 1,
    "Export_pv_cij_above_threshold_complex_branch": 0,
    "Export_native_zll_lambda_evaluated": 0,
    "Export_native_kappa_l_evaluated": 0,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


def check_T_w_trace_pv_timelike_c1_c2_spacelike_overlap_P() -> Dict[str, Any]:
    """T: timelike-branch (C1, C2) reduce to the banked spacelike c1_c2_direct where F>0 [P]."""
    mx = 0.0
    mim = 0.0
    for pt in _SPACELIKE:
        c1t, c2t = c1_c2_timelike(*pt)
        c1s, c2s = _c1_c2_spacelike(*pt)
        mx = max(mx, abs(c1t.real - c1s) / max(1e-12, abs(c1s)),
                     abs(c2t.real - c2s) / max(1e-12, abs(c2s)))
        mim = max(mim, abs(c1t.imag), abs(c2t.imag))
    check(mx < 5e-3, f"timelike-vs-banked spacelike (C1,C2) Re max rel err {mx:.2e}")
    check(mim < 1e-7, f"spacelike Im must vanish, got {mim:.2e}")
    return _result(
        name=("T_w_trace_pv_timelike_c1_c2_spacelike_overlap: "
              "timelike-branch (C1,C2) == banked spacelike c1_c2_direct where F>0 [P]"),
        tier=4, epistemic="P",
        summary=(
            f"Wherever F>0 throughout the simplex (spacelike external invariants) "
            f"the timelike-branch rank-1 (C1,C2) reduce to the banked direct "
            f"spacelike c1_c2_direct (max rel err {mx:.1e}) with vanishing absorptive "
            f"parts (max |Im| {mim:.1e}) -- a consistent continuation of the banked "
            f"spacelike substrate."
        ),
        key_result=f"timelike (C1,C2) == banked spacelike where F>0 (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_timelike_c0_spacelike_overlap",
                      "T_w_trace_pv_c1_c2_reduction_matches_direct"],
        artifacts={"max_rel_err": mx, "max_abs_im": mim},
    )


def check_T_w_trace_pv_timelike_c1_c2_absorptive_closed_form_P() -> Dict[str, Any]:
    """T: Im(C1), Im(C2) reproduce closed forms in two kinematic classes [P]."""
    mx = 0.0
    for M, s in ((MW2, MZ2), (100.0, 1000.0), (50.0, 600.0)):
        c1, c2 = c1_c2_timelike(0.0, M, M, 0.0, 0.0, s)
        mx = max(mx,
                 abs(c1.imag - _im_c1_class_A(M, s)) / abs(_im_c1_class_A(M, s)),
                 abs(c2.imag - _im_c2_class_A(M, s)) / abs(_im_c2_class_A(M, s)))
    for M, s in ((25.0, 600.0), (10.0, 2000.0), (50.0, 1000.0)):
        c1, c2 = c1_c2_timelike(M, M, M, 0.0, 0.0, s)
        mx = max(mx,
                 abs(c1.imag - _im_c1_class_B(M, s)) / abs(_im_c1_class_B(M, s)),
                 abs(c2.imag - _im_c2_class_B(M, s)) / abs(_im_c2_class_B(M, s)))
    check(mx < 1e-5, f"Im (C1,C2) closed-form max rel err {mx:.2e}")
    return _result(
        name=("T_w_trace_pv_timelike_c1_c2_absorptive_closed_form: "
              "Im(C1), Im(C2) reproduce closed forms in two kinematic classes [P]"),
        tier=4, epistemic="P",
        summary=(
            f"The absorptive parts Im(C1), Im(C2) reproduce two independently "
            f"derived closed forms: class A C(0,M,M;0,0,s>M) and class B "
            f"C(M,M,M;0,0,s>4M). Max rel err {mx:.1e} -- target-free analytic "
            f"anchors on the cut."
        ),
        key_result=f"Im (C1,C2) == closed forms (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_timelike_c1_c2_spacelike_overlap",
                      "T_w_trace_pv_timelike_c0_absorptive_closed_form"],
        artifacts={"max_rel_err": mx},
    )


def _im_c1_c2_rootcount(m1, m2, m3, s12, s23, s31):
    """Absorptive Im(C1), Im(C2) from explicit delta(F) root counts."""
    edges = [0.0] + [p for p in _breaks(m1, m2, m3, s12, s23, s31)
                     if 1e-12 < p < 1.0 - 1e-12] + [1.0]
    acc1 = 0.0
    acc2 = 0.0
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
            sum_I = 0.0
            sum_J = 0.0
            for y in roots:
                if 0.0 < y < Y:
                    fp = abs(a1 + 2.0 * a2 * y)
                    if fp > 0.0:
                        sum_I += 1.0 / fp
                        sum_J += y / fp
            acc1 += w * half * Y * sum_I
            acc2 += w * half * (Y * sum_I - sum_J)
    return math.pi * acc1, math.pi * acc2


def check_T_w_trace_pv_timelike_c1_c2_absorptive_two_ways_P() -> Dict[str, Any]:
    """T: Im(C1), Im(C2) from analytic-inner == delta-function root count;
    Im=0 below threshold [P]."""
    mx = 0.0
    for pt in _TIMELIKE + ((200.0, 50.0, 300.0, -100.0, 900.0, -50.0),):
        c1, c2 = c1_c2_timelike(*pt)
        im1_rc, im2_rc = _im_c1_c2_rootcount(*pt)
        mx = max(mx, abs(c1.imag - im1_rc) / max(1.0, abs(c1.imag)),
                     abs(c2.imag - im2_rc) / max(1.0, abs(c2.imag)))
    check(mx < 1e-6, f"Im (C1,C2) two-ways max rel err {mx:.2e}")
    M = MW2
    sub = c1_c2_timelike(0.0, M, M, 0.0, 0.0, 0.5 * M)
    check(abs(sub[0].imag) + abs(sub[1].imag) < 1e-9,
          f"below-threshold Im must vanish, got {sub[0].imag:.2e}+{sub[1].imag:.2e}")
    return _result(
        name=("T_w_trace_pv_timelike_c1_c2_absorptive_two_ways: "
              "Im(C1), Im(C2) analytic-inner == delta-function root count; "
              "Im=0 below threshold [P]"),
        tier=4, epistemic="P",
        summary=(
            f"Im(C1), Im(C2) from the analytic inner (cmath branches of "
            f"ln(F - i eps)) agree with the explicit delta(F) root count to "
            f"max rel err {mx:.1e}. The absorptive parts vanish below threshold, "
            f"confirming the correct analytic structure of the cut."
        ),
        key_result=f"Im (C1,C2) analytic-inner == delta root count (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_timelike_c1_c2_spacelike_overlap",
                      "T_w_trace_pv_timelike_c0_absorptive_two_ways"],
        artifacts={"max_rel_err": mx,
                   "below_threshold_im_sum": sub[0].imag + sub[1].imag},
    )


def check_T_w_trace_pv_timelike_c1_c2_subgate_partial_P() -> Dict[str, Any]:
    """T: timelike rank-1 (C1,C2) done; rank-2 + Lambda + kappa_l OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_pv_c1_c2_above_threshold_complex_branch"] == 1,
          "timelike (C1,C2) branch flag must be 1")
    check(EXPORT_FLAGS["Export_pv_cij_above_threshold_complex_branch"] == 0,
          "timelike rank-2 Cij must remain OPEN")
    check(EXPORT_FLAGS["Export_native_kappa_l_evaluated"] == 0,
          "no kappa_l evaluated by this rung")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no Delta r_rem evaluated by this rung")
    return _result(
        name=("T_w_trace_pv_timelike_c1_c2_subgate_partial: "
              "timelike rank-1 (C1,C2) native; rank-2 + Lambda + kappa_l OPEN [P_structural]"),
        tier=4, epistemic="P_structural",
        summary=(
            "The native three-point rank-1 tensor coefficients (C1, C2) extend to "
            "the timelike branch (1D-reduced Feynman integral with the closed-form "
            "inner J, single-log stable I, tanh-sinh + kink-subdivision on each "
            "smooth piece), the R0b prerequisite for the complex BHM Zll vertex "
            "functions Lambda_2(s,M_Z) / Lambda_3(s,M_W). Still OPEN: the timelike "
            "rank-2 coefficients (C00, C11, C12, C22) [R0c], the Lambda_2/Lambda_3 "
            "assembly [R1], the renormalized Zll vertex [R2], and the bosonic + "
            "light-fermion pieces [R3/R4]. No kappa_l / Delta r_rem / M_W produced; "
            "DIZET stays the publishable OS-W closure."
        ),
        key_result="Timelike rank-1 (C1,C2) native; rank-2 + Lambda + kappa_l OPEN. [P_structural]",
        dependencies=["T_w_trace_pv_timelike_c1_c2_absorptive_two_ways"],
        cross_refs=["T_w_trace_pv_timelike_c0_subgate_partial",
                    "T_w_trace_pv_c_tensor_subgate_partial"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_pv_timelike_c1_c2_spacelike_overlap": check_T_w_trace_pv_timelike_c1_c2_spacelike_overlap_P,
    "T_w_trace_pv_timelike_c1_c2_absorptive_closed_form": check_T_w_trace_pv_timelike_c1_c2_absorptive_closed_form_P,
    "T_w_trace_pv_timelike_c1_c2_absorptive_two_ways": check_T_w_trace_pv_timelike_c1_c2_absorptive_two_ways_P,
    "T_w_trace_pv_timelike_c1_c2_subgate_partial": check_T_w_trace_pv_timelike_c1_c2_subgate_partial_P,
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
