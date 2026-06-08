"""W_TRACE APF-native PV derivative two-point functions B0', B1'.

The on-shell renormalization scheme needs the momentum derivatives of the
two-point functions: the wave-function (field) renormalization constants are
fixed by Sigma'(p^2) at the on-shell point, and the OS mass counterterms by
Sigma(M^2). This module supplies the native finite-part derivatives

    B0'(p^2,m0^2,m1^2) = dB0/dp^2  =  int_0^1 dx  x(1-x)/F ,
    B1'(p^2,m0^2,m1^2) = dB1/dp^2  = -int_0^1 dx  x^2(1-x)/F ,

with F(x) = x m1^2 + (1-x) m0^2 - x(1-x) p^2 (the banked-substrate Feynman
denominator). They are built ENTIRELY on the banked finite scalar substrate /
the native two-point reduction -- no external input, no reviewed-formula
import. This continues the native OS-W toolkit (parallel to the sibling
reviewed-formula route).

Self-validation (no external target)
------------------------------------
  * B0' and B1' agree with central finite differences of the banked
    b0_fin and the native b1_direct to ~1e-12.
  * Closed forms: B0'(0,m^2,m^2) = 1/(6 m^2); B0'(p^2,0,0) = 1/|p^2| (spacelike).

What this module does (and does NOT) claim
------------------------------------------
It supplies the native two-point momentum derivatives needed by the OS
wave-function/mass counterterms. It does NOT assemble a self-energy, a
counterterm, Delta r_rem, or any electroweak value; the 3-/4-point tensors, the
Denner coefficient map, and the counterterm assembly remain OPEN; the imported
DIZET route stays the publishable OS-W closure.

Status
------
- Export_pv_b0_prime_b1_prime_native = 1   (NEW here)
- Export_OSW_APF_internal_delta_r_rem_evaluated = 0  (OPEN, unchanged)
"""
from __future__ import annotations

import math
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_pv_scalar_integral_substrate import b0_fin, MU2, MW2, MZ2, MT2, MH2
from apf.w_trace_pv_tensor_reduction import b1_direct, _delta


def b0_prime(p2: float, m02: float, m12: float, n: int = 40000) -> float:
    """dB0/dp^2 = int_0^1 dx x(1-x)/F (finite, spacelike/below-threshold)."""
    h = 1.0 / n
    acc = 0.0
    for i in range(n):
        x = (i + 0.5) * h
        d = _delta(x, p2, m02, m12)
        if d <= 0:
            d = abs(d) + 1e-30
        acc += x * (1.0 - x) / d
    return h * acc


def b1_prime(p2: float, m02: float, m12: float, n: int = 40000) -> float:
    """dB1/dp^2 = -int_0^1 dx x^2(1-x)/F (finite, spacelike/below-threshold)."""
    h = 1.0 / n
    acc = 0.0
    for i in range(n):
        x = (i + 0.5) * h
        d = _delta(x, p2, m02, m12)
        if d <= 0:
            d = abs(d) + 1e-30
        acc += x * x * (1.0 - x) / d
    return -h * acc


_TEST_POINTS = (
    (-MZ2, MW2, MZ2),
    (-MW2, MT2, MH2),
    (-MH2, MZ2, MW2),
    (-2.0 * MZ2, MW2, MH2),
)

EXPORT_FLAGS: Dict[str, int] = {
    "Export_pv_b0_prime_b1_prime_native": 1,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


def check_T_w_trace_pv_b0_prime_matches_finite_difference_P() -> Dict[str, Any]:
    """T: B0' agrees with the central finite difference of the banked B0 [P]."""
    mx = 0.0
    for p2, m02, m12 in _TEST_POINTS:
        h = abs(p2) * 1e-4
        fd = (b0_fin(p2 + h, m02, m12) - b0_fin(p2 - h, m02, m12)) / (2.0 * h)
        mx = max(mx, abs(b0_prime(p2, m02, m12) - fd))
    check(mx < 1e-9, f"B0' vs finite-difference max diff {mx:.2e} exceeds 1e-9")
    return _result(
        name="T_w_trace_pv_b0_prime_matches_finite_difference: "
             "dB0/dp^2 == central finite difference of banked B0 [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native B0' = int x(1-x)/F dx agrees with the central finite "
            f"difference of the banked b0_fin to max diff {mx:.2e} across "
            f"{len(_TEST_POINTS)} spacelike points -- an independent confirmation."
        ),
        key_result=f"B0' == d/dp^2 of banked B0 (max diff {mx:.1e}). [P]",
        dependencies=["check_T_w_trace_pv_b0_gate_closed"],
        artifacts={"max_abs_diff": mx},
    )


def check_T_w_trace_pv_b0_prime_closed_forms_P() -> Dict[str, Any]:
    """T: B0'(0,m,m) = 1/(6 m^2) and B0'(p^2,0,0) = 1/|p^2| (spacelike) [P]."""
    errs = []
    for m2 in (MW2, MT2, MZ2):
        errs.append(abs(b0_prime(0.0, m2, m2) - 1.0 / (6.0 * m2)) * m2)  # relative
    for p2 in (-MZ2, -MW2, -3.0 * MZ2):
        errs.append(abs(b0_prime(p2, 0.0, 0.0) - 1.0 / abs(p2)) * abs(p2))  # relative
    mx = max(errs)
    check(mx < 1e-6, f"B0' closed-form max rel err {mx:.2e} exceeds 1e-6")
    return _result(
        name="T_w_trace_pv_b0_prime_closed_forms: "
             "B0'(0,m,m)=1/(6m^2), B0'(p^2,0,0)=1/|p^2| [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native B0' reproduces its analytic closed forms -- equal-mass "
            f"zero-momentum 1/(6 m^2) and massless 1/|p^2| (spacelike) -- to max "
            f"relative err {mx:.2e}."
        ),
        key_result=f"B0' closed forms reproduced (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_b0_prime_matches_finite_difference"],
        artifacts={"max_rel_err": mx},
    )


def check_T_w_trace_pv_b1_prime_matches_finite_difference_P() -> Dict[str, Any]:
    """T: B1' agrees with the central finite difference of the native B1 [P]."""
    mx = 0.0
    for p2, m02, m12 in _TEST_POINTS:
        h = abs(p2) * 1e-4
        fd = (b1_direct(p2 + h, m02, m12) - b1_direct(p2 - h, m02, m12)) / (2.0 * h)
        mx = max(mx, abs(b1_prime(p2, m02, m12) - fd))
    check(mx < 1e-9, f"B1' vs finite-difference max diff {mx:.2e} exceeds 1e-9")
    return _result(
        name="T_w_trace_pv_b1_prime_matches_finite_difference: "
             "dB1/dp^2 == central finite difference of native B1 [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native B1' = -int x^2(1-x)/F dx agrees with the central finite "
            f"difference of the native B1 to max diff {mx:.2e} across "
            f"{len(_TEST_POINTS)} spacelike points."
        ),
        key_result=f"B1' == d/dp^2 of B1 (max diff {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_b1_reduction_matches_direct"],
        artifacts={"max_abs_diff": mx},
    )


def check_T_w_trace_pv_derivative_two_point_subgate_partial_P() -> Dict[str, Any]:
    """T: native two-point derivatives present; assembly + 3-/4-point OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_pv_b0_prime_b1_prime_native"] == 1,
          "B0'/B1' native flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no Delta r_rem evaluated by these derivative functions")
    return _result(
        name="T_w_trace_pv_derivative_two_point_subgate_partial: "
             "native B0'/B1' present; self-energy assembly + 3-/4-point OPEN [P_structural]",
        tier=4, epistemic="P_structural",
        summary=(
            "The native OS-W toolkit gains the two-point momentum derivatives "
            "B0', B1' needed for on-shell wave-function/mass renormalization, on "
            "top of the two-point value tensors (B1,B00,B11). The self-energy "
            "assembly, the 3-/4-point Cij/Dij, the Denner coefficient map, and the "
            "counterterm assembly remain OPEN; no Delta r_rem / M_W value is "
            "produced; DIZET stays the publishable OS-W closure."
        ),
        key_result="Native two-point derivatives B0'/B1' added; assembly OPEN. [P_structural]",
        dependencies=["T_w_trace_pv_b0_prime_matches_finite_difference",
                      "T_w_trace_pv_b1_prime_matches_finite_difference"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_pv_b0_prime_matches_finite_difference": check_T_w_trace_pv_b0_prime_matches_finite_difference_P,
    "T_w_trace_pv_b0_prime_closed_forms": check_T_w_trace_pv_b0_prime_closed_forms_P,
    "T_w_trace_pv_b1_prime_matches_finite_difference": check_T_w_trace_pv_b1_prime_matches_finite_difference_P,
    "T_w_trace_pv_derivative_two_point_subgate_partial": check_T_w_trace_pv_derivative_two_point_subgate_partial_P,
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
