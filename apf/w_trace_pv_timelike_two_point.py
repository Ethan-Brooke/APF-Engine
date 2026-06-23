"""APF-native PV two-point functions on the TIMELIKE / above-threshold branch -- Tier-4.

Stage 1 of the native OS-W one-loop evaluator (work plan 2026-05-24): extend the
native two-point PV functions from the spacelike / finite-real domain to TIMELIKE
external momenta above threshold, where the Feynman denominator
F(x) = x m1^2 + (1-x) m0^2 - x(1-x) p^2 goes negative for some x. This is the
prerequisite for the on-shell self-energies Re Pi_WW(M_W^2) and Re Pi_ZZ(M_Z^2)
(the pieces that live off p^2 = 0).

Construction (principal value + absorptive part)
------------------------------------------------
With the Feynman iε prescription F -> F - iε, ln(F-iε) = ln|F| - iπ θ(-F), so the
real parts are principal-value integrals over ln|F| and B0 acquires an imaginary
(absorptive) part where F < 0:

    Re B0  = - int_0^1 ln(|F|/mu^2) dx
    Re B1  = + int_0^1 x   ln(|F|/mu^2) dx
    Re B11 = - int_0^1 x^2 ln(|F|/mu^2) dx
    Re B00 = + int_0^1 (F/2)(1 - ln(|F|/mu^2)) dx     (F prefactor keeps its sign)
    Im B0  = + pi int_0^1 theta(-F) dx  = pi sqrt(lambda)/p^2   (above threshold)

These reduce EXACTLY to the banked spacelike functions
(apf.w_trace_pv_scalar_integral_substrate.b0_fin /
apf.w_trace_pv_tensor_reduction.b1_direct/b11_direct/b00_direct) wherever F > 0
throughout (spacelike, or timelike below threshold).

Self-validation (no external target)
------------------------------------
- massless closed form: Re B0(p^2,0,0) = 2 - ln(|p^2|/mu^2) (all p^2),
  Im B0(p^2>0,0,0) = pi.
- equal-mass timelike (s>4m^2): Re B0 = 2 - ln(m^2/mu^2) + beta ln((1-beta)/
  (1+beta)), Im B0 = pi beta, beta = sqrt(1-4m^2/s).
- unequal-mass timelike (s>(m1+m2)^2): the standard two-log closed form;
  Im B0 = pi sqrt(lambda)/s, lambda = (s-(m1+m2)^2)(s-(m1-m2)^2).
- spacelike/sub-threshold OVERLAP: Re B-functions equal the banked spacelike
  functions exactly where F>0.
- real-part trace relation above threshold:
  4 Re B00 + p^2 Re B11 - (m0^2/2 + m1^2/2 - p^2/6) = A0(m1^2) + m0^2 Re B0.

Honest scope
------------
The timelike two-point branch (Re B0/B1/B11/B00 + Im B0). The three-/four-point
functions on the timelike branch, the assembled Re Pi_WW(M_W^2)/Re Pi_ZZ(M_Z^2),
the bosonic loops, delta_VB, and UV cancellation remain to be assembled; no
Delta r_rem / M_W is produced here. DIZET stays the publishable OS-W closure.

Status
------
- Export_native_timelike_two_point_branch          = 1
- Export_OSW_APF_internal_delta_r_rem_evaluated     = 0   (OPEN, unchanged)
"""
from __future__ import annotations

import math
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_pv_scalar_integral_substrate import a0_fin, b0_fin, MU2
from apf.w_trace_pv_tensor_reduction import b1_direct, b11_direct, b00_direct

_N = 120000


def _delta(x: float, p2: float, m02: float, m12: float) -> float:
    return x * m12 + (1.0 - x) * m02 - x * (1.0 - x) * p2


def re_b0_timelike(p2: float, m02: float, m12: float, mu2: float = MU2, n: int = _N) -> float:
    acc = 0.0
    for i in range(n):
        x = (i + 0.5) / n
        acc += math.log(abs(_delta(x, p2, m02, m12)) / mu2)
    return -acc / n


def im_b0_timelike(p2: float, m02: float, m12: float, n: int = _N) -> float:
    cnt = sum(1 for i in range(n) if _delta((i + 0.5) / n, p2, m02, m12) < 0.0)
    return math.pi * cnt / n


def re_b1_timelike(p2: float, m02: float, m12: float, mu2: float = MU2, n: int = _N) -> float:
    acc = 0.0
    for i in range(n):
        x = (i + 0.5) / n
        acc += x * math.log(abs(_delta(x, p2, m02, m12)) / mu2)
    return acc / n


def re_b11_timelike(p2: float, m02: float, m12: float, mu2: float = MU2, n: int = _N) -> float:
    acc = 0.0
    for i in range(n):
        x = (i + 0.5) / n
        acc += x * x * math.log(abs(_delta(x, p2, m02, m12)) / mu2)
    return -acc / n


def re_b00_timelike(p2: float, m02: float, m12: float, mu2: float = MU2, n: int = _N) -> float:
    acc = 0.0
    for i in range(n):
        x = (i + 0.5) / n
        F = _delta(x, p2, m02, m12)
        acc += 0.5 * F * (1.0 - math.log(abs(F) / mu2))
    return acc / n


# --- closed-form references (validation only) ------------------------------
def _reb0_massless_closed(p2, mu2=MU2):
    return 2.0 - math.log(abs(p2) / mu2)


def _reb0_equal_mass_closed(s, m2, mu2=MU2):
    beta = math.sqrt(1.0 - 4.0 * m2 / s)
    return 2.0 - math.log(m2 / mu2) + beta * math.log((1.0 - beta) / (1.0 + beta))


def _reb0_general_closed(s, m02, m12, mu2=MU2):
    lam = (s - (math.sqrt(m02) + math.sqrt(m12)) ** 2) * (s - (math.sqrt(m02) - math.sqrt(m12)) ** 2)
    sl = math.sqrt(abs(lam))
    return (2.0 - math.log(math.sqrt(m02 * m12) / mu2)
            + (m12 - m02) / (2.0 * s) * math.log(m02 / m12)
            - sl / (2.0 * s) * math.log(abs((s - m02 - m12 + sl) / (s - m02 - m12 - sl))))


EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_timelike_two_point_branch": 1,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


# ===========================================================================
# checks
# ===========================================================================
def check_T_w_trace_pv_timelike_b0_massless_closed_P() -> Dict[str, Any]:
    """T: timelike Re B0 / Im B0 reproduce the massless closed forms [P]."""
    mx = 0.0
    for p2 in (5000.0, 26569.0, 80000.0):
        re = re_b0_timelike(p2, 0.0, 0.0)
        mx = max(mx, abs(re - _reb0_massless_closed(p2)))
        im = im_b0_timelike(p2, 0.0, 0.0)
        check(abs(im - math.pi) < 1e-6, f"Im B0(p2,0,0) must be pi, got {im}")
    check(mx < 5e-4, f"Re B0(p2,0,0) vs 2-ln(|p2|/mu2) max abs err {mx:.2e}")
    return _result(
        name="T_w_trace_pv_timelike_b0_massless_closed: "
             "timelike Re B0 / Im B0 reproduce the massless closed forms [P]",
        tier=4, epistemic="P",
        summary=(
            f"On the timelike branch the principal-value Re B0(p^2,0,0) reproduces "
            f"2 - ln(|p^2|/mu^2) to {mx:.1e} and the absorptive Im B0(p^2,0,0) = pi "
            f"exactly. Native, no external input."
        ),
        key_result=f"timelike massless Re B0 (err {mx:.1e}), Im B0 = pi. [P]",
        dependencies=["check_T_w_trace_pv_b0_finite_gate"],
        artifacts={"max_abs_err": mx},
    )


def check_T_w_trace_pv_timelike_b0_threshold_closed_P() -> Dict[str, Any]:
    """T: timelike Re B0 / Im B0 reproduce equal- and unequal-mass closed forms [P]."""
    mx = 0.0
    # equal mass
    for s, m in [(200.0, 5.0), (600.0, 5.0), (2000.0, 5.0)]:
        m2 = m * m
        re = re_b0_timelike(s, m2, m2)
        mx = max(mx, abs(re - _reb0_equal_mass_closed(s, m2)))
        beta = math.sqrt(1.0 - 4.0 * m2 / s)
        im = im_b0_timelike(s, m2, m2)
        check(abs(im - math.pi * beta) < 2e-3, f"Im B0 equal-mass: {im} vs {math.pi*beta}")
    # unequal mass
    for s, m02, m12 in [(400.0, 9.0, 25.0), (8000.0, 100.0, 400.0)]:
        re = re_b0_timelike(s, m02, m12)
        mx = max(mx, abs(re - _reb0_general_closed(s, m02, m12)))
        lam = (s - (math.sqrt(m02) + math.sqrt(m12)) ** 2) * (s - (math.sqrt(m02) - math.sqrt(m12)) ** 2)
        im = im_b0_timelike(s, m02, m12)
        check(abs(im - math.pi * math.sqrt(lam) / s) < 3e-3, f"Im B0 general: {im}")
    check(mx < 5e-4, f"Re B0 timelike vs closed forms max abs err {mx:.2e}")
    return _result(
        name="T_w_trace_pv_timelike_b0_threshold_closed: "
             "timelike Re B0 / Im B0 reproduce equal- and unequal-mass closed forms [P]",
        tier=4, epistemic="P",
        summary=(
            f"Above threshold the principal-value Re B0 reproduces both the "
            f"equal-mass form 2 - ln(m^2/mu^2) + beta ln((1-beta)/(1+beta)) and the "
            f"unequal-mass two-log closed form to {mx:.1e}, with the absorptive part "
            f"Im B0 = pi sqrt(lambda)/s matching to <3e-3. Three independent "
            f"closed-form validations; native, no external input."
        ),
        key_result=f"timelike Re/Im B0 reproduce closed forms (err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_timelike_b0_massless_closed"],
        artifacts={"max_abs_err": mx},
    )


def check_T_w_trace_pv_timelike_spacelike_overlap_P() -> Dict[str, Any]:
    """T: timelike Re B-functions equal the banked spacelike functions where F>0 [P]."""
    mx = 0.0
    # spacelike + timelike-sub-threshold points (F>0 throughout)
    pts = [(-8315.0, 6458.0, 8315.0), (10000.0, 6400.0, 8100.0), (-26569.0, 26569.0, 100.0)]
    for p2, m02, m12 in pts:
        mx = max(mx, abs(re_b0_timelike(p2, m02, m12) - b0_fin(p2, m02, m12)))
        mx = max(mx, abs(re_b1_timelike(p2, m02, m12) - b1_direct(p2, m02, m12)))
        mx = max(mx, abs(re_b11_timelike(p2, m02, m12) - b11_direct(p2, m02, m12)))
        mx = max(mx, abs(re_b00_timelike(p2, m02, m12) - b00_direct(p2, m02, m12)) / max(1.0, abs(b00_direct(p2, m02, m12))))
    check(mx < 1e-3, f"timelike-vs-banked overlap max err {mx:.2e}")
    return _result(
        name="T_w_trace_pv_timelike_spacelike_overlap: "
             "timelike Re B-functions reduce to the banked spacelike functions where F>0 [P]",
        tier=4, epistemic="P",
        summary=(
            f"Wherever F>0 (spacelike, or timelike below threshold) the timelike "
            f"Re B0/B1/B11/B00 reduce exactly to the banked spacelike "
            f"b0_fin/b1_direct/b11_direct/b00_direct (max err {mx:.1e}) -- the "
            f"branch is a consistent continuation of the banked substrate, not a "
            f"separate object."
        ),
        key_result=f"timelike branch == banked spacelike where F>0 (err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_timelike_b0_massless_closed"],
        artifacts={"max_err": mx},
    )


def check_T_w_trace_pv_timelike_trace_relation_P() -> Dict[str, Any]:
    """T: the rank-2 trace relation holds for the timelike real parts [P]."""
    mx = 0.0
    for p2, m02, m12 in [(400.0, 9.0, 25.0), (2000.0, 25.0, 25.0), (50000.0, 26569.0, 0.0025)]:
        lhs = 4.0 * re_b00_timelike(p2, m02, m12) + p2 * re_b11_timelike(p2, m02, m12) \
            - (m02 / 2.0 + m12 / 2.0 - p2 / 6.0)
        rhs = a0_fin(m12) + m02 * re_b0_timelike(p2, m02, m12)
        mx = max(mx, abs(lhs - rhs) / max(1.0, abs(rhs)))
    check(mx < 1e-3, f"timelike trace relation max rel err {mx:.2e}")
    return _result(
        name="T_w_trace_pv_timelike_trace_relation: "
             "rank-2 metric-trace relation holds for the timelike real parts [P]",
        tier=4, epistemic="P",
        summary=(
            f"Above threshold the real parts satisfy the rank-2 trace relation "
            f"4 Re B00 + p^2 Re B11 - (m0^2/2+m1^2/2-p^2/6) = A0(m1^2) + m0^2 Re B0 "
            f"to max rel err {mx:.1e}, jointly validating the timelike Re B00/B11/B0 "
            f"against the banked A0."
        ),
        key_result=f"timelike real-part trace relation holds (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_timelike_spacelike_overlap"],
        artifacts={"max_rel_err": mx},
    )


def check_T_w_trace_pv_timelike_subgate_partial_P() -> Dict[str, Any]:
    """T: timelike two-point branch done; 3-/4-point timelike + assembly OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_native_timelike_two_point_branch"] == 1, "timelike branch flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no Delta r_rem evaluated by this rung")
    return _result(
        name="T_w_trace_pv_timelike_subgate_partial: "
             "timelike two-point branch done; assembly toward Re Pi(M^2) OPEN [P_structural]",
        tier=4, epistemic="P_structural_partial",
        summary=(
            "The native two-point PV functions now extend to the timelike / "
            "above-threshold branch (Re B0/B1/B11/B00 via principal value + the "
            "absorptive Im B0), reducing to the banked spacelike functions where "
            "F>0 -- the prerequisite for Re Pi_WW(M_W^2) / Re Pi_ZZ(M_Z^2). Still "
            "OPEN toward the APF-internal Delta r_rem: assembling the on-shell "
            "self-energies at timelike p^2 (light-fermion loops above threshold + "
            "the sub-threshold top via the existing functions), the "
            "bosonic/Goldstone/ghost loops, the vertex+box delta_VB, and UV-pole "
            "cancellation. No Delta r_rem / M_W produced; DIZET stays the "
            "publishable OS-W closure."
        ),
        key_result="Timelike two-point branch done; Re Pi(M^2) assembly OPEN. [P_structural]",
        dependencies=["T_w_trace_pv_timelike_trace_relation"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_pv_timelike_b0_massless_closed": check_T_w_trace_pv_timelike_b0_massless_closed_P,
    "T_w_trace_pv_timelike_b0_threshold_closed": check_T_w_trace_pv_timelike_b0_threshold_closed_P,
    "T_w_trace_pv_timelike_spacelike_overlap": check_T_w_trace_pv_timelike_spacelike_overlap_P,
    "T_w_trace_pv_timelike_trace_relation": check_T_w_trace_pv_timelike_trace_relation_P,
    "T_w_trace_pv_timelike_subgate_partial": check_T_w_trace_pv_timelike_subgate_partial_P,
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
