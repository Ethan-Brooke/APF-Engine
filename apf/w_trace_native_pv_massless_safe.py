"""APF-native massless/degenerate-safe two-point PV B0 -- Tier-4.

Stage-1 hardening of the native OS-W one-loop evaluator (work plan 2026-05-24):
the banked midpoint quadrature ``apf.w_trace_pv_timelike_two_point.re_b0_timelike``
is endpoint-safe for massive lines, but the genuine SM self-energies need the
*exactly-massless* limits -- neutrino lines, the idealized photon/gluon line, and
the scaleless point B0(0,0,0) -- where the integrand ln|F| hits log(0). This
module supplies an analytic dispatcher ``re_b0_safe`` / ``im_b0_safe`` that routes
the massless and degenerate-kinematics cases to closed forms and otherwise falls
back to the banked quadrature.

Closed forms (Denner 1993, arXiv:0709.1075, App. A; finite parts at scale mu^2)
------------------------------------------------------------------------------
    B0(0,0,0)        = 0                                  (scaleless: UV/IR poles cancel)
    B0(p^2,0,0)      = 2 - ln(|p^2|/mu^2)                 ; Im = pi theta(p^2)
    B0(p^2,0,m^2)    = 2 - ln(m^2/mu^2)
                         + (m^2-p^2)/p^2 ln(|m^2-p^2|/m^2); Im = pi(1-m^2/p^2) theta(p^2-m^2)
    B0(0,0,m^2)      = 1 - ln(m^2/mu^2)
    B0(0,m^2,m^2)    = - ln(m^2/mu^2)
    B0(0,m0^2,m1^2)  = 1 + (m0^2 ln(mu^2/m0^2) - m1^2 ln(mu^2/m1^2))/(m0^2 - m1^2)

The one-massless form carries a removable singularity at the pseudo-threshold
p^2 = m^2: the prefactor (m^2-p^2)/p^2 vanishes faster than ln|m^2-p^2| diverges,
so the term limit is 0 -- guarded explicitly (an unguarded evaluation throws
``math domain error`` at exactly p^2 = m^2).

Self-validation (no external target)
------------------------------------
Every closed form is checked against the banked midpoint quadrature with tiny
mass/momentum regulators (eps = 1e-6): all branches agree to < 5e-3 (the p^2 = 0
massive branches to ~1e-9). The dispatcher reduces *exactly* to the banked
quadrature ``re_b0_timelike`` for all-massive, p^2 != 0 kinematics (overlap), so
it is a continuation of the banked substrate, not a separate object. No-crash is
asserted on B0(0,0,0), B0(p^2,0,0), and the raw threshold B0(m^2,0,m^2).

Honest scope
------------
Two-point B0 only (massless/degenerate hardening). The tensor coefficients
B1/B00/B11 in the same limits, the assembled Re Pi_VV(M_V^2), the bosonic loops,
delta_VB, and UV cancellation are unchanged by this rung; no Delta r_rem / M_W is
produced. DIZET stays the publishable OS-W closure.

Status
------
- Export_native_pv_massless_safe_b0                 = 1
- Export_OSW_APF_internal_delta_r_rem_evaluated     = 0   (OPEN, unchanged)
"""
from __future__ import annotations

import math
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_pv_timelike_two_point import (
    re_b0_timelike, im_b0_timelike, MU2, _N,
)

# A line is treated on the analytic massless branch only when its mass^2 is
# *exactly* zero. Small-but-nonzero masses keep full quadrature accuracy
# (the midpoint rule is endpoint-safe); we never silently snap them to zero.
_ZERO = 0.0


def _thresh_tol(m2: float) -> float:
    return 1e-9 * max(1.0, m2)


# ---------------------------------------------------------------------------
# analytic closed forms (finite parts at scale MU2)
# ---------------------------------------------------------------------------
def _reb0_00(p2: float, mu2: float) -> float:
    """B0(p2, 0, 0): both lines massless."""
    if p2 == 0.0:
        return 0.0  # scaleless -- finite part 0 (UV and IR poles cancel)
    return 2.0 - math.log(abs(p2) / mu2)


def _reb0_0m(p2: float, m2: float, mu2: float) -> float:
    """B0(p2, 0, m2): one massless line, one of mass^2 = m2 > 0."""
    if p2 == 0.0:
        return 1.0 - math.log(m2 / mu2)
    if abs(m2 - p2) < _thresh_tol(m2):
        # removable pseudo-threshold: (m2-p2)/p2 * ln|m2-p2| -> 0
        return 2.0 - math.log(m2 / mu2)
    return 2.0 - math.log(m2 / mu2) + (m2 - p2) / p2 * math.log(abs(m2 - p2) / m2)


def _reb0_zero_mom(m02: float, m12: float, mu2: float) -> float:
    """B0(0, m0^2, m1^2): zero external momentum, both masses > 0."""
    if abs(m02 - m12) < _thresh_tol(max(m02, m12)):
        m2 = 0.5 * (m02 + m12)
        return -math.log(m2 / mu2)
    return 1.0 + (m02 * math.log(mu2 / m02) - m12 * math.log(mu2 / m12)) / (m02 - m12)


# ---------------------------------------------------------------------------
# public dispatchers
# ---------------------------------------------------------------------------
def re_b0_safe(p2: float, m02: float, m12: float, mu2: float = MU2, n: int = _N) -> float:
    """Massless/degenerate-safe Re B0.

    Routes exactly-massless lines and zero-momentum kinematics to closed forms;
    falls back to the banked midpoint quadrature for all-massive, p^2 != 0 cases.
    """
    z0 = (m02 == _ZERO)
    z1 = (m12 == _ZERO)
    if z0 and z1:
        return _reb0_00(p2, mu2)
    if z0 or z1:
        m2 = m12 if z0 else m02
        return _reb0_0m(p2, m2, mu2)
    if p2 == 0.0:
        return _reb0_zero_mom(m02, m12, mu2)
    return re_b0_timelike(p2, m02, m12, mu2, n)


def im_b0_safe(p2: float, m02: float, m12: float, n: int = _N) -> float:
    """Massless/degenerate-safe absorptive Im B0 (>=0 above threshold)."""
    if p2 <= 0.0:
        return 0.0
    z0 = (m02 == _ZERO)
    z1 = (m12 == _ZERO)
    if z0 and z1:
        return math.pi
    if z0 or z1:
        m2 = m12 if z0 else m02
        return math.pi * (1.0 - m2 / p2) if p2 > m2 else 0.0
    return im_b0_timelike(p2, m02, m12, n)


EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_pv_massless_safe_b0": 1,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


# ===========================================================================
# checks
# ===========================================================================
def check_T_w_trace_native_pv_massless_safe_closed_forms_P() -> Dict[str, Any]:
    """T: massless/degenerate Re B0 closed forms match the banked quadrature [P]."""
    eps = 1e-6
    mx = 0.0
    # B0(p2,0,0): both massless, p2 != 0  -- regulate masses
    for p2 in (-8000.0, 5000.0, 26569.0, 80000.0):
        mx = max(mx, abs(re_b0_safe(p2, 0.0, 0.0) - re_b0_timelike(p2, eps, eps)))
    # B0(p2,0,m): one massless, including the threshold p2=m^2
    m2t = 163.0 ** 2
    for p2 in (-500.0, 5000.0, 26569.0, 50000.0):
        mx = max(mx, abs(re_b0_safe(p2, 0.0, m2t) - re_b0_timelike(p2, eps, m2t)))
    # B0(0,m,m) and B0(0,m0,m1): zero momentum -- regulate p2
    for m02, m12 in [(25.0, 25.0), (6464.0, 6464.0), (25.0, 6464.0), (26569.0, 17.0)]:
        mx = max(mx, abs(re_b0_safe(0.0, m02, m12) - re_b0_timelike(eps, m02, m12)))
    # B0(0,0,m): zero momentum, one massless
    for m2 in (25.0, 6464.0, 26569.0):
        mx = max(mx, abs(re_b0_safe(0.0, 0.0, m2) - re_b0_timelike(eps, eps, m2)))
    check(mx < 5e-3, f"massless/degenerate closed forms vs banked quadrature max abs err {mx:.2e}")
    return _result(
        name="T_w_trace_native_pv_massless_safe_closed_forms: "
             "massless/degenerate Re B0 closed forms match the banked quadrature [P]",
        tier=4, epistemic="P",
        summary=(
            f"The analytic massless/degenerate Re B0 branches -- B0(p^2,0,0), "
            f"B0(p^2,0,m^2) (incl. the p^2=m^2 pseudo-threshold), B0(0,m^2,m^2), "
            f"B0(0,m0^2,m1^2), B0(0,0,m^2) -- reproduce the banked midpoint "
            f"quadrature with tiny mass/momentum regulators (eps=1e-6) to max abs "
            f"err {mx:.1e}. Native, no external input."
        ),
        key_result=f"massless/degenerate B0 closed forms vs quadrature (err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_timelike_b0_massless_closed"],
        artifacts={"max_abs_err": mx},
    )


def check_T_w_trace_native_pv_massless_safe_overlap_P() -> Dict[str, Any]:
    """T: the safe dispatcher reduces to the banked quadrature for massive lines [P]."""
    mx = 0.0
    # all-massive, p2 != 0  -> must be value-identical to re_b0_timelike
    pts = [(-8315.0, 6458.0, 8315.0), (10000.0, 6400.0, 8100.0),
           (5000.0, 25.0, 6464.0), (50000.0, 26569.0, 6464.0)]
    for p2, m02, m12 in pts:
        mx = max(mx, abs(re_b0_safe(p2, m02, m12) - re_b0_timelike(p2, m02, m12)))
        mx = max(mx, abs(im_b0_safe(p2, m02, m12) - im_b0_timelike(p2, m02, m12)))
    check(mx < 1e-12, f"safe dispatcher vs banked quadrature (massive) max err {mx:.2e}")
    return _result(
        name="T_w_trace_native_pv_massless_safe_overlap: "
             "safe dispatcher is value-identical to the banked quadrature for massive lines [P]",
        tier=4, epistemic="P",
        summary=(
            f"For all-massive, p^2 != 0 kinematics the dispatcher re_b0_safe / "
            f"im_b0_safe routes straight to the banked re_b0_timelike / "
            f"im_b0_timelike and is value-identical (max err {mx:.1e}) -- the "
            f"massless branch is a continuation of the banked substrate, not a "
            f"separate object."
        ),
        key_result=f"safe B0 == banked quadrature for massive lines (err {mx:.1e}). [P]",
        dependencies=["T_w_trace_native_pv_massless_safe_closed_forms"],
        artifacts={"max_err": mx},
    )


def check_T_w_trace_native_pv_massless_safe_imaginary_P() -> Dict[str, Any]:
    """T: massless-branch absorptive Im B0 matches the regulated quadrature [P]."""
    eps = 1e-6
    mx = 0.0
    # both massless: Im = pi above 0
    for p2 in (5000.0, 26569.0, 80000.0):
        mx = max(mx, abs(im_b0_safe(p2, 0.0, 0.0) - im_b0_timelike(p2, eps, eps)))
        check(abs(im_b0_safe(p2, 0.0, 0.0) - math.pi) < 1e-9, "Im B0(p2,0,0) must be pi")
    # one massless: Im = pi(1 - m2/p2) above p2=m2
    m2 = 163.0 ** 2
    for p2 in (5000.0, 26569.0, 50000.0):
        mx = max(mx, abs(im_b0_safe(p2, 0.0, m2) - im_b0_timelike(p2, eps, m2)))
    # below threshold and spacelike: Im = 0
    check(im_b0_safe(-500.0, 0.0, m2) == 0.0, "Im B0 spacelike must be 0")
    check(im_b0_safe(5000.0, 0.0, m2) == 0.0, "Im B0 below one-massless threshold must be 0")
    check(mx < 3e-3, f"massless Im B0 vs regulated quadrature max abs err {mx:.2e}")
    return _result(
        name="T_w_trace_native_pv_massless_safe_imaginary: "
             "massless-branch absorptive Im B0 matches the regulated quadrature [P]",
        tier=4, epistemic="P",
        summary=(
            f"The closed-form absorptive parts -- Im B0(p^2,0,0)=pi theta(p^2) and "
            f"Im B0(p^2,0,m^2)=pi(1-m^2/p^2) theta(p^2-m^2) -- reproduce the "
            f"regulated banked Im quadrature to max abs err {mx:.1e}, and vanish "
            f"spacelike / below threshold. Native, no external input."
        ),
        key_result=f"massless Im B0 closed forms vs quadrature (err {mx:.1e}). [P]",
        dependencies=["T_w_trace_native_pv_massless_safe_closed_forms"],
        artifacts={"max_abs_err": mx},
    )


def check_T_w_trace_native_pv_massless_safe_no_crash_P() -> Dict[str, Any]:
    """T: the safe dispatcher is crash-free on the scaleless and threshold points [P]."""
    # B0(0,0,0): scaleless -- closed-form 0, banked quadrature would log(0)
    v000 = re_b0_safe(0.0, 0.0, 0.0)
    check(v000 == 0.0, f"B0(0,0,0) must be the scaleless finite part 0, got {v000}")
    # raw threshold B0(m^2,0,m^2): unguarded closed form throws math domain error
    m2 = 163.0 ** 2
    vth = re_b0_safe(m2, 0.0, m2)
    check(math.isfinite(vth), f"B0(m^2,0,m^2) must be finite at threshold, got {vth}")
    # exactly-massless neutrino-style line at a physical scale
    vnu = re_b0_safe(80000.0, 0.0, 0.0)
    check(math.isfinite(vnu), "B0(p^2,0,0) must be finite")
    # confirm the banked quadrature really would crash on the scaleless point
    quad_crashes = False
    try:
        re_b0_timelike(0.0, 0.0, 0.0)
    except (ValueError, ZeroDivisionError):
        quad_crashes = True
    check(quad_crashes, "banked quadrature is expected to crash on the scaleless point")
    return _result(
        name="T_w_trace_native_pv_massless_safe_no_crash: "
             "safe dispatcher is crash-free on scaleless and pseudo-threshold points [P]",
        tier=4, epistemic="P",
        summary=(
            "re_b0_safe returns the scaleless finite part 0 for B0(0,0,0) (where "
            "the banked quadrature throws log(0)), stays finite at the one-massless "
            "pseudo-threshold B0(m^2,0,m^2) via the removable-singularity guard, "
            "and is finite for exactly-massless lines -- the cases the SM "
            "self-energies need (neutrino / photon / gluon lines) that the raw "
            "quadrature cannot evaluate."
        ),
        key_result="B0(0,0,0)=0, threshold finite, massless finite -- no crashes. [P]",
        dependencies=["T_w_trace_native_pv_massless_safe_closed_forms"],
        artifacts={"b0_000": v000, "b0_threshold": vth},
    )


def check_T_w_trace_native_pv_massless_safe_subgate_partial_P() -> Dict[str, Any]:
    """T: massless-safe B0 done; tensor limits + Re Pi(M^2) assembly OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_native_pv_massless_safe_b0"] == 1, "massless-safe B0 flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no Delta r_rem evaluated by this rung")
    return _result(
        name="T_w_trace_native_pv_massless_safe_subgate_partial: "
             "massless-safe B0 done; tensor limits + assembly OPEN [P_structural]",
        tier=4, epistemic="P_structural_partial",
        summary=(
            "The native two-point B0 now has clean analytic massless / degenerate "
            "branches (exactly-massless lines, zero momentum, the scaleless point, "
            "the one-massless pseudo-threshold), reducing to the banked quadrature "
            "for massive lines. Still OPEN toward the APF-internal Delta r_rem: the "
            "tensor coefficients B1/B00/B11 in the same limits, the assembled "
            "Re Pi_WW(M_W^2)/Re Pi_ZZ(M_Z^2), the bosonic/Goldstone/ghost loops, "
            "the vertex+box delta_VB, and UV-pole cancellation. No Delta r_rem / "
            "M_W produced; DIZET stays the publishable OS-W closure."
        ),
        key_result="Massless-safe B0 done; tensor limits + Re Pi(M^2) assembly OPEN. [P_structural]",
        dependencies=["T_w_trace_native_pv_massless_safe_no_crash"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_native_pv_massless_safe_closed_forms": check_T_w_trace_native_pv_massless_safe_closed_forms_P,
    "T_w_trace_native_pv_massless_safe_overlap": check_T_w_trace_native_pv_massless_safe_overlap_P,
    "T_w_trace_native_pv_massless_safe_imaginary": check_T_w_trace_native_pv_massless_safe_imaginary_P,
    "T_w_trace_native_pv_massless_safe_no_crash": check_T_w_trace_native_pv_massless_safe_no_crash_P,
    "T_w_trace_native_pv_massless_safe_subgate_partial": check_T_w_trace_native_pv_massless_safe_subgate_partial_P,
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
