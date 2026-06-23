"""APF-native three-point TENSOR coefficients on the TIMELIKE branch -- rank-2 (C00, C11, C12, C22) -- Tier-4.

R0c of the OS-W Gate A "native kappa_l" arc (Route 1). Extends the timelike rank-1
tensor (apf.w_trace_pv_timelike_three_point_tensor, v24.3.104) to the rank-2
coefficients C^{munu} = g^{munu} C00 + p1^mu p1^nu C11 + p2^mu p2^nu C22 +
(p1^mu p2^nu + p2^mu p1^nu) C12 on the TIMELIKE / above-threshold branch.

Construction (1D-reduced Feynman integrals)
-------------------------------------------
In the c0_general convention (x1=x, x2=y, x3=1-x-y) with x2+x3 = Y(x) = 1-x and
x3 = Y-y, the rank-2 outer integrals reduce to four inner integrals over y:

    C11 = -int_0^1 dx Y^2 I(x) ,           I(x) = int_0^Y dy / (F - i eps)
    C12 = -int_0^1 dx [Y^2 I - Y J](x) ,   J(x) = int_0^Y dy y / (F - i eps)
    C22 = -int_0^1 dx [Y^2 I - 2 Y J + K](x) ,
                                            K(x) = int_0^Y dy y^2 / (F - i eps)
    C00 = -1/2 int_0^1 dx L(x) + (ln mu^2)/4 ,
                                            L(x) = int_0^Y dy ln(F - i eps)

I and J are reused from the rank-1 module. K and L are derived here in closed
form. K uses the same single-log stability as I:

    K_linear = Y^2/(2 a1) - Y (a0 - i eps)/a1^2 + (a0 - i eps)^2/a1^2 * I_stable
    K_quad   = Y/a2 + (rp + rm) J - rp rm I

L is computed via integration by parts (avoids branch-cut ambiguity that the
naive sum-of-three-logs form suffers in the quadratic case):

    L = Y * cln(F(Y) - i eps) - 2 a2 K - a1 J ,
    F(Y) = a2 Y^2 + a1 Y + a0

which is a single complex log of the quadratic at y=Y, no factoring required.

Self-validation (no external target)
------------------------------------
  * spacelike overlap: where F>0 throughout, Re(C00, C11, C12, C22) reduce to the
    banked spacelike cij_rank2_direct;
  * metric-trace relation (d=4-2eps finite Ward identity):
        4 C00 + s12 C11 + s23 C22 + 2 p1.p2 C12 - 1/2
            = B0(s23; m2^2, m3^2) + m1^2 C0
    Both sides complex on the timelike branch; ties native Cij to the banked
    complex B0 (re_b0_timelike + i im_b0_timelike) + native timelike C0;
  * threshold: Im(Cij) = 0 below threshold.

Honest scope
------------
The timelike rank-2 tensor coefficients (Re + absorptive Im). The
BHM/Denner Lambda_2/Lambda_3 assembly, the renormalized Zll vertex, the bosonic
and light-fermion contributions, and the native kappa_l remain OPEN -- the
next rungs (R1: Lambda assembly). No kappa_l / Delta r_rem / M_W value is
produced; DIZET stays the publishable OS-W closure.

Status
------
- Export_pv_cij_above_threshold_complex_branch    = 1   (NEW here)
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
    _abc, _breaks, _TS_NODES, _default_eps, c0_general_timelike,
)
from apf.w_trace_pv_timelike_three_point_tensor import _inner_stable, _innerJ
from apf.w_trace_pv_timelike_two_point import re_b0_timelike, im_b0_timelike
from apf.w_trace_pv_cij_three_point import cij_rank2_direct as _cij_spacelike
from apf.w_trace_pv_scalar_integral_substrate import MU2, MW2, MZ2, MT2, MH2


def _innerK(x: float, m1: float, m2: float, m3: float,
            s12: float, s23: float, s31: float, eps: float) -> complex:
    """Analytic inner integral int_0^Y dy y^2 / (F - i eps)."""
    Y = 1.0 - x
    a0, a1, a2 = _abc(x, m1, m2, m3, s12, s23, s31)
    sc = abs(a0) + abs(a1) + abs(a2) + 1.0
    if abs(a2) < 1e-13 * sc:
        if abs(a1) < 1e-13 * sc:
            return (Y**3 / 3.0) / complex(a0, -eps)
        I = _inner_stable(x, m1, m2, m3, s12, s23, s31, eps)
        a0c = complex(a0, -eps)
        return Y * Y / (2.0 * a1) - Y * a0c / (a1 * a1) + a0c * a0c / (a1 * a1) * I
    disc = a1 * a1 - 4.0 * a2 * complex(a0, -eps)
    sq = cmath.sqrt(disc)
    rp = (-a1 + sq) / (2.0 * a2)
    rm = (-a1 - sq) / (2.0 * a2)
    I = _inner_stable(x, m1, m2, m3, s12, s23, s31, eps)
    J = _innerJ(x, m1, m2, m3, s12, s23, s31, eps)
    return Y / a2 + (rp + rm) * J - rp * rm * I


def _innerL(x: float, m1: float, m2: float, m3: float,
            s12: float, s23: float, s31: float, eps: float) -> complex:
    """Analytic inner integral int_0^Y dy ln(F - i eps) via integration by parts
    (single complex log of F(Y), no branch-cut ambiguity)."""
    Y = 1.0 - x
    a0, a1, a2 = _abc(x, m1, m2, m3, s12, s23, s31)
    F_Y = a2 * Y * Y + a1 * Y + a0
    J = _innerJ(x, m1, m2, m3, s12, s23, s31, eps)
    K = _innerK(x, m1, m2, m3, s12, s23, s31, eps)
    return Y * cmath.log(complex(F_Y, -eps)) - 2.0 * a2 * K - a1 * J


def cij_rank2_timelike(m1: float, m2: float, m3: float,
                       s12: float = 0.0, s23: float = 0.0, s31: float = 0.0,
                       eps: float = None,
                       mu2: float = MU2) -> Dict[str, complex]:
    """Native rank-2 three-point coefficients (C00, C11, C12, C22) valid on
    spacelike AND timelike/above-threshold branches. Returns dict of complex."""
    if eps is None:
        eps = _default_eps(m1, m2, m3, s12, s23, s31)
    edges = [0.0] + [p for p in _breaks(m1, m2, m3, s12, s23, s31)
                     if 1e-12 < p < 1.0 - 1e-12] + [1.0]
    c00_acc = 0j
    c11_acc = 0j
    c12_acc = 0j
    c22_acc = 0j
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
            K = _innerK(x, m1, m2, m3, s12, s23, s31, eps)
            L = _innerL(x, m1, m2, m3, s12, s23, s31, eps)
            wh = w * half
            c00_acc += wh * (-0.5) * L
            c11_acc += wh * (-(Y * Y) * I)
            c12_acc += wh * (-(Y * Y * I - Y * J))
            c22_acc += wh * (-(Y * Y * I - 2.0 * Y * J + K))
    # C00 has an extra finite (ln mu^2)/4 from the F/mu^2 splitting:
    # -1/2 int_simplex ln(F/mu^2) dmu = -1/2 int dx L(x) + (ln mu^2)/2 * (simplex area = 1/2)
    c00 = c00_acc + 0.25 * math.log(mu2)
    return {"C00": c00, "C11": c11_acc, "C12": c12_acc, "C22": c22_acc}


def _b0_complex_tl(p2: float, m02: float, m12: float) -> complex:
    """Complex timelike B0 = banked re_b0_timelike + i banked im_b0_timelike;
    reduces to banked spacelike b0_fin where F>0."""
    return complex(re_b0_timelike(p2, m02, m12), im_b0_timelike(p2, m02, m12))


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
    "Export_pv_cij_above_threshold_complex_branch": 1,
    "Export_native_zll_lambda_evaluated": 0,
    "Export_native_kappa_l_evaluated": 0,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


def check_T_w_trace_pv_timelike_cij_rank2_spacelike_overlap_P() -> Dict[str, Any]:
    """T: timelike rank-2 (C00, C11, C12, C22) reduce to banked spacelike cij_rank2_direct [P]."""
    mx = 0.0
    mim = 0.0
    for pt in _SPACELIKE:
        c = cij_rank2_timelike(*pt)
        ref = _cij_spacelike(*pt)
        for k in ("C00", "C11", "C12", "C22"):
            denom = max(1.0, abs(ref[k]))
            mx = max(mx, abs(c[k].real - ref[k]) / denom)
            mim = max(mim, abs(c[k].imag))
    check(mx < 5e-3, f"timelike-vs-banked spacelike rank-2 Re max rel err {mx:.2e}")
    check(mim < 1e-6, f"spacelike Im must vanish, got max {mim:.2e}")
    return _result(
        name=("T_w_trace_pv_timelike_cij_rank2_spacelike_overlap: "
              "timelike-branch rank-2 Cij == banked spacelike cij_rank2_direct where F>0 [P]"),
        tier=4, epistemic="P",
        summary=(
            f"Wherever F>0 throughout the simplex the timelike-branch rank-2 "
            f"(C00, C11, C12, C22) reduce to the banked spacelike "
            f"cij_rank2_direct (max rel err {mx:.1e}) with vanishing absorptive "
            f"parts (max |Im| {mim:.1e}) -- a consistent continuation."
        ),
        key_result=f"timelike rank-2 == banked spacelike where F>0 (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_timelike_c1_c2_spacelike_overlap",
                      "T_w_trace_pv_cij_rank2_trace_relation"],
        artifacts={"max_rel_err": mx, "max_abs_im": mim},
    )


def check_T_w_trace_pv_timelike_cij_rank2_trace_relation_P() -> Dict[str, Any]:
    """T: rank-2 metric-trace relation holds on the timelike branch [P]."""
    mx = 0.0
    pts = _SPACELIKE + _TIMELIKE
    for m1, m2, m3, s12, s23, s31 in pts:
        c = cij_rank2_timelike(m1, m2, m3, s12, s23, s31)
        c0 = c0_general_timelike(m1, m2, m3, s12, s23, s31)
        p1p2 = (s31 - s12 - s23) / 2.0
        lhs = (4.0 * c["C00"] + s12 * c["C11"] + s23 * c["C22"]
               + 2.0 * p1p2 * c["C12"] - 0.5)
        rhs = _b0_complex_tl(s23, m2, m3) + m1 * c0
        denom = max(1.0, abs(rhs))
        mx = max(mx, abs(lhs - rhs) / denom)
    check(mx < 5e-3, f"rank-2 trace relation max rel err {mx:.2e}")
    return _result(
        name=("T_w_trace_pv_timelike_cij_rank2_trace_relation: "
              "4 C00 + s12 C11 + s23 C22 + 2 p1.p2 C12 - 1/2 = B0 + m1^2 C0 "
              "on the timelike branch [P]"),
        tier=4, epistemic="P",
        summary=(
            f"The native rank-2 coefficients satisfy the finite d=4-2 eps "
            f"metric-trace relation (Ward identity) against the banked complex "
            f"timelike B0 + native timelike C0 to max rel err {mx:.1e} across "
            f"spacelike + timelike test points -- a target-free validation that "
            f"ties the new rank-2 Cij to the banked B0 + native C0."
        ),
        key_result=f"rank-2 trace relation holds (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_timelike_cij_rank2_spacelike_overlap",
                      "T_w_trace_pv_timelike_c0_spacelike_overlap"],
        artifacts={"max_rel_err": mx},
    )


def check_T_w_trace_pv_timelike_cij_rank2_threshold_P() -> Dict[str, Any]:
    """T: Im(C00, C11, C12, C22) vanish below threshold [P]."""
    # class A sub-threshold: s < (m1 + m3)^2 = M^2 (when m1=0, m3=M)
    M = MW2
    c = cij_rank2_timelike(0.0, M, M, 0.0, 0.0, 0.5 * M)
    im_sum = sum(abs(c[k].imag) for k in ("C00", "C11", "C12", "C22"))
    check(im_sum < 1e-5, f"below-threshold rank-2 Im sum {im_sum:.2e}")
    # spacelike: same
    c_sp = cij_rank2_timelike(MW2, MZ2, MT2, -MZ2, -MW2, -MH2)
    im_sp = sum(abs(c_sp[k].imag) for k in ("C00", "C11", "C12", "C22"))
    check(im_sp < 1e-5, f"spacelike rank-2 Im sum {im_sp:.2e}")
    return _result(
        name=("T_w_trace_pv_timelike_cij_rank2_threshold: "
              "Im(rank-2 Cij) vanish below threshold and on spacelike [P]"),
        tier=4, epistemic="P",
        summary=(
            f"The absorptive parts of the native rank-2 coefficients vanish "
            f"below threshold (max sum |Im| {im_sum:.1e}) and in the spacelike "
            f"domain (max sum |Im| {im_sp:.1e}), confirming the correct "
            f"analytic structure of the cut."
        ),
        key_result=f"Im(rank-2) = 0 below threshold + spacelike (sum |Im| ~{max(im_sum,im_sp):.1e}). [P]",
        dependencies=["T_w_trace_pv_timelike_cij_rank2_spacelike_overlap"],
        artifacts={"below_threshold_im_sum": im_sum, "spacelike_im_sum": im_sp},
    )


def check_T_w_trace_pv_timelike_cij_rank2_subgate_partial_P() -> Dict[str, Any]:
    """T: timelike rank-2 Cij done; Lambda + kappa_l OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_pv_cij_above_threshold_complex_branch"] == 1,
          "timelike rank-2 Cij branch flag must be 1")
    check(EXPORT_FLAGS["Export_native_zll_lambda_evaluated"] == 0,
          "Lambda_2/Lambda_3 must remain OPEN")
    check(EXPORT_FLAGS["Export_native_kappa_l_evaluated"] == 0,
          "no kappa_l evaluated by this rung")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no Delta r_rem evaluated by this rung")
    return _result(
        name=("T_w_trace_pv_timelike_cij_rank2_subgate_partial: "
              "timelike rank-2 Cij native; Lambda + kappa_l OPEN [P_structural]"),
        tier=4, epistemic="P_structural_partial",
        summary=(
            "The native three-point rank-2 tensor coefficients (C00, C11, C12, C22) "
            "now extend to the timelike branch via the closed-form inner K and "
            "single-log L (integration by parts), with the same tanh-sinh + "
            "kink-subdivision outer quadrature. Together with the timelike scalar "
            "C0 (v24.3.103) and rank-1 (C1, C2) (v24.3.104) this completes the "
            "three-point complex tensor basis -- the substrate for the Lambda_2 / "
            "Lambda_3 vertex assembly (R1). No Lambda / kappa_l / Delta r_rem / M_W "
            "produced; DIZET stays the publishable OS-W closure."
        ),
        key_result="Timelike rank-2 Cij native; Lambda + kappa_l OPEN. [P_structural]",
        dependencies=["T_w_trace_pv_timelike_cij_rank2_trace_relation"],
        cross_refs=["T_w_trace_pv_timelike_c0_subgate_partial",
                    "T_w_trace_pv_timelike_c1_c2_subgate_partial",
                    "T_w_trace_pv_c_tensor_subgate_partial"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_pv_timelike_cij_rank2_spacelike_overlap": check_T_w_trace_pv_timelike_cij_rank2_spacelike_overlap_P,
    "T_w_trace_pv_timelike_cij_rank2_trace_relation": check_T_w_trace_pv_timelike_cij_rank2_trace_relation_P,
    "T_w_trace_pv_timelike_cij_rank2_threshold": check_T_w_trace_pv_timelike_cij_rank2_threshold_P,
    "T_w_trace_pv_timelike_cij_rank2_subgate_partial": check_T_w_trace_pv_timelike_cij_rank2_subgate_partial_P,
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
