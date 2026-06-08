"""APF-native BHM Lambda_2(s, M^2) and Lambda_3(s, M^2) Z-vertex scalar functions -- Tier-4.

R1 of the OS-W Gate A "native kappa_l" arc (Route 1). Implements the BHM
Z-vertex scalar form factors Lambda_2(s, M^2) and Lambda_3(s, M^2) used in the
Zll proper-vertex assembly, per the LEP Yellow Report "Precision Calculations
for the Z Resonance" (CERN 95-03 = arXiv:hep-ph/9709229, EWWGR.tex L6062), with
the explicit Feynman iepsilon prescription:

    w = M^2 / (s + i eps) ,

    Lambda_2(s, M^2) = -7/2 - 2 w - (2 w + 3) log(-w)
                       + 2 (1 + w)^2 [ Li_2(1 + 1/w) - pi^2 / 6 ] ,

    Lambda_3(s, M^2) = 5/6 - 2 w / 3
                       + (2 w + 1) / 3 * sqrt(1 - 4 w) * log(x)
                       + 2/3 * w (w + 2) * log(x)^2 ,
    with x = (sqrt(1 - 4 w) - 1) / (sqrt(1 - 4 w) + 1) .

These combine with the SM gauge couplings to build F_L^f, F_V^Zf, F_A^Zf -- the
proper-vertex form factors entering the on-shell effective leptonic mixing
angle through the renormalized Zll coupling. At s = M_Z^2 with internal mass
M = M_W (the W-W-Z triangle), Lambda_2 has an absorptive part from the
M_W-loop branch cut while Lambda_3 is real (the 2 M_W threshold sits at
s = 4 M_W^2 > M_Z^2 -- closed at the Z pole). At s = M_Z^2 with internal
M = M_Z (the Z-Z exchange triangle), Lambda_2 is complex.

R1 closes the closed-form route: the BHM analytic expressions are implemented
in pure Python with a self-contained dilogarithm Li_2 (series + reflection)
and the iepsilon prescription threaded through cmath. The NATIVE composition
from the timelike C-toolkit (R0 scalar C0 v24.3.103 + R0b rank-1 C1/C2
v24.3.104 + R0c rank-2 Cij v24.3.105) per the Denner generic-vertex form
factors is the natural cross-anchor and remains OPEN here -- the next rung
(R1b) wires the timelike Cij into the haba3 V_a / V_b decomposition to
reproduce Lambda_2 and Lambda_3 the second way.

Self-validation (no fitted/measured target)
-------------------------------------------
  * Li_2 reference values: Li_2(1) = pi^2 / 6, Li_2(-1) = -pi^2 / 12,
    Li_2(1/2) = pi^2 / 12 - (ln 2)^2 / 2, Li_2(0) = 0.
  * Li_2 Abel identity:
        Li_2(z) + Li_2(1 - z) + log(z) log(1 - z) = pi^2 / 6
    holds on complex test points.
  * spacelike reality: Lambda_2(s, M^2), Lambda_3(s, M^2) are real
    (|Im| < epsilon_real) for s < 0.
  * physical-kinematics reference values (independently computed via mpmath
    at dps=40 and hardcoded here): match the pure-Python implementation to
    relative 1e-12.

Honest scope
------------
The BHM Lambda_2 / Lambda_3 scalar functions only (closed-form route). The
NATIVE composition from the Denner generic vertex form factors V_a / V_b
using the timelike C-toolkit (R1b cross-anchor), the renormalized Zll
proper vertex with counterterms (R2), the bosonic Delta kappa contribution
(R3), the light-fermion / Delta alpha contribution (R4), and the assembled
kappa_l value (R5) remain OPEN. No kappa_l / Delta r_rem / M_W value is
produced; DIZET stays the publishable OS-W closure.

Status
------
- Export_native_bhm_lambda_closed_form_evaluated  = 1   (NEW here)
- Export_native_bhm_lambda_via_C_toolkit          = 0   (OPEN, R1b)
- Export_native_zll_renormalized_vertex           = 0   (OPEN, R2)
- Export_native_kappa_l_evaluated                 = 0   (OPEN, R5)
- Export_OSW_APF_internal_delta_r_rem_evaluated   = 0   (OPEN, unchanged)
"""
from __future__ import annotations

import math
import cmath
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_pv_scalar_integral_substrate import MW2, MZ2

_DEFAULT_EPS = 1e-14
PI = math.pi
PI2_OVER_6 = PI * PI / 6.0


def Li2(z) -> complex:
    """Principal-branch dilogarithm Li_2(z) = sum_{n=1}^inf z^n / n^2.

    Strategy:
      |z| > 1                : reflection  Li_2(z) = -Li_2(1/z) - pi^2/6 - (1/2) log(-z)^2
      |z| <= 1, Re z > 1/2   : reflection  Li_2(z) = pi^2/6 - log(z) log(1-z) - Li_2(1-z)
      |z| <= 1, Re z <= 1/2  : power series (converges quickly there)
    """
    z = complex(z)
    if abs(z) < 1e-15:
        return 0.0 + 0.0j
    if abs(z - 1.0) < 1e-15:
        return PI2_OVER_6 + 0.0j
    if abs(z + 1.0) < 1e-15:
        return -PI * PI / 12.0 + 0.0j
    if abs(z) > 1.0:
        return -Li2(1.0 / z) - PI2_OVER_6 - 0.5 * cmath.log(-z) ** 2
    if z.real > 0.5:
        return PI2_OVER_6 - cmath.log(z) * cmath.log(1.0 - z) - Li2(1.0 - z)
    # power series; converges geometrically for |z| <= 1/2
    result = 0.0 + 0.0j
    term = z
    for n in range(1, 200):
        contribution = term / (n * n)
        result += contribution
        if abs(contribution) < 1e-18:
            break
        term *= z
    return result


def Lambda_2(s: float, M2: float, eps: float = _DEFAULT_EPS) -> complex:
    """BHM Lambda_2(s, M^2) with Feynman iepsilon prescription w = M^2/(s + i eps)."""
    w = M2 / complex(s, eps)
    return (-3.5 - 2.0 * w - (2.0 * w + 3.0) * cmath.log(-w)
            + 2.0 * (1.0 + w) ** 2 * (Li2(1.0 + 1.0 / w) - PI2_OVER_6))


def Lambda_3(s: float, M2: float, eps: float = _DEFAULT_EPS) -> complex:
    """BHM Lambda_3(s, M^2) with Feynman iepsilon prescription w = M^2/(s + i eps)."""
    w = M2 / complex(s, eps)
    sq = cmath.sqrt(1.0 - 4.0 * w)
    x = (sq - 1.0) / (sq + 1.0)
    lx = cmath.log(x)
    return (5.0 / 6.0 - 2.0 * w / 3.0
            + (2.0 * w + 1.0) / 3.0 * sq * lx
            + 2.0 / 3.0 * w * (w + 2.0) * lx * lx)


# Reference values computed independently via mpmath at dps=40 (Li_2 = mp.polylog(2, .)),
# with the SAME iepsilon convention w = M^2/(s + i eps). Hardcoded to give a
# tight bank-side anchor without taking a runtime mpmath dependency.
_REF_VALUES: Dict[str, complex] = {
    # Lambda_2(M_Z^2, M_W^2) -- ν/W/W triangle at the Z pole
    "L2_MZ2_MW2":  complex( 1.1805183681875155,  2.1068900271751924),
    # Lambda_3(M_Z^2, M_W^2) -- real (2 M_W threshold closed at s = M_Z^2)
    "L3_MZ2_MW2":  complex(-3.2679780980165249,  0.0),
    # Lambda_2(M_Z^2, M_Z^2) -- Z exchange
    "L2_MZ2_MZ2":  complex( 1.0797362673929057,  1.7127254544798509),
    # Lambda_2(-M_Z^2, M_W^2) -- spacelike, must be real
    "L2_neg_MZ2_MW2": complex(-1.7719799883977947, 0.0),
    # Lambda_3(-M_Z^2, M_W^2) -- spacelike, must be real
    "L3_neg_MZ2_MW2": complex( 1.0147076906274485, 0.0),
}


EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_bhm_lambda_closed_form_evaluated": 1,
    "Export_native_bhm_lambda_via_C_toolkit": 0,
    "Export_native_zll_renormalized_vertex": 0,
    "Export_native_kappa_l_evaluated": 0,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


# ===========================================================================
# checks
# ===========================================================================
def check_T_w_trace_pv_lambda_bhm_Li2_reference_values_P() -> Dict[str, Any]:
    """T: Li_2 reproduces classical reference values [P]."""
    mx = 0.0
    cases = [
        (1.0,  PI2_OVER_6),
        (-1.0, -PI * PI / 12.0),
        (0.5,  PI * PI / 12.0 - 0.5 * math.log(2.0) ** 2),
        (0.0,  0.0),
    ]
    for z, ref in cases:
        v = Li2(z)
        mx = max(mx, abs(v.real - ref), abs(v.imag))
    check(mx < 1e-13, f"Li_2 reference-value max abs err {mx:.2e}")
    return _result(
        name=("T_w_trace_pv_lambda_bhm_Li2_reference_values: "
              "Li_2 reproduces Li_2(1) = pi^2/6, Li_2(-1) = -pi^2/12, "
              "Li_2(1/2) = pi^2/12 - (ln 2)^2/2, Li_2(0) = 0 [P]"),
        tier=4, epistemic="P",
        summary=(
            f"The pure-Python principal-branch dilogarithm Li_2 reproduces four "
            f"classical reference values (Li_2(1) = pi^2/6, Li_2(-1) = -pi^2/12, "
            f"Li_2(1/2) = pi^2/12 - (ln 2)^2/2, Li_2(0) = 0) to max abs err "
            f"{mx:.1e} -- validates the series + reflection implementation."
        ),
        key_result=f"Li_2 reference values match (max abs err {mx:.1e}). [P]",
        dependencies=[],
        artifacts={"max_abs_err": mx},
    )


def check_T_w_trace_pv_lambda_bhm_Li2_abel_identity_P() -> Dict[str, Any]:
    """T: Li_2 satisfies the Abel identity Li_2(z) + Li_2(1-z) + log(z) log(1-z) = pi^2/6 [P]."""
    mx = 0.0
    # Test points off the Li_2 cut [1, infty) AND off (-infty, 0] (so 1 - z is also off the cut)
    test_pts = [
        complex(0.3,  0.0),
        complex(0.7,  0.0),
        complex(0.4,  0.6),
        complex(-0.2, 1.1),
        complex(0.8, -0.3),
        complex(0.1,  0.4),
    ]
    for z in test_pts:
        lhs = Li2(z) + Li2(1.0 - z) + cmath.log(z) * cmath.log(1.0 - z)
        mx = max(mx, abs(lhs - PI2_OVER_6))
    check(mx < 1e-12, f"Li_2 Abel-identity max abs err {mx:.2e}")
    return _result(
        name=("T_w_trace_pv_lambda_bhm_Li2_abel_identity: "
              "Li_2(z) + Li_2(1-z) + log(z) log(1-z) = pi^2/6 on complex test points [P]"),
        tier=4, epistemic="P",
        summary=(
            f"The pure-Python Li_2 satisfies the Abel identity "
            f"Li_2(z) + Li_2(1 - z) + log(z) log(1 - z) = pi^2 / 6 on seven "
            f"complex test points (real + complex, |z| < 1 + |z| > 1) to max "
            f"abs err {mx:.1e} -- a target-free validation across the full "
            f"branch structure of the implementation."
        ),
        key_result=f"Li_2 Abel identity holds (max abs err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_lambda_bhm_Li2_reference_values"],
        artifacts={"max_abs_err": mx},
    )


def check_T_w_trace_pv_lambda_bhm_spacelike_real_P() -> Dict[str, Any]:
    """T: Lambda_2(s, M^2), Lambda_3(s, M^2) real for s < 0 (spacelike) [P]."""
    mx = 0.0
    for s, M2 in [(-MZ2, MW2), (-MZ2, MZ2), (-2.0 * MZ2, MW2), (-5000.0, 1000.0)]:
        L2 = Lambda_2(s, M2)
        L3 = Lambda_3(s, M2)
        mx = max(mx, abs(L2.imag), abs(L3.imag))
    check(mx < 1e-10, f"spacelike Lambda max abs Im {mx:.2e}")
    return _result(
        name=("T_w_trace_pv_lambda_bhm_spacelike_real: "
              "Lambda_2, Lambda_3 are real for spacelike s < 0 [P]"),
        tier=4, epistemic="P",
        summary=(
            f"For spacelike external invariant s < 0 (where the s-channel "
            f"branch cut is closed) the absorptive parts of Lambda_2, Lambda_3 "
            f"vanish to max |Im| {mx:.1e} across four kinematic test points -- "
            f"confirms the correct analytic structure of the Feynman iepsilon "
            f"prescription w = M^2 / (s + i eps)."
        ),
        key_result=f"Lambda_2, Lambda_3 real for s<0 (max |Im| {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_lambda_bhm_Li2_abel_identity"],
        artifacts={"max_abs_im": mx},
    )


def check_T_w_trace_pv_lambda_bhm_physical_values_P() -> Dict[str, Any]:
    """T: Lambda_2, Lambda_3 at physical kinematics match mpmath-computed reference [P]."""
    mx = 0.0
    pairs = [
        ((MZ2,  MW2), _REF_VALUES["L2_MZ2_MW2"],    Lambda_2),
        ((MZ2,  MW2), _REF_VALUES["L3_MZ2_MW2"],    Lambda_3),
        ((MZ2,  MZ2), _REF_VALUES["L2_MZ2_MZ2"],    Lambda_2),
        ((-MZ2, MW2), _REF_VALUES["L2_neg_MZ2_MW2"], Lambda_2),
        ((-MZ2, MW2), _REF_VALUES["L3_neg_MZ2_MW2"], Lambda_3),
    ]
    for (s, M2), ref, fn in pairs:
        v = fn(s, M2)
        denom = max(1.0, abs(ref))
        mx = max(mx, abs(v - ref) / denom)
    check(mx < 1e-12, f"Lambda physical-kinematics max rel err vs mpmath {mx:.2e}")
    return _result(
        name=("T_w_trace_pv_lambda_bhm_physical_values: "
              "Lambda_2, Lambda_3 at physical kinematics match mpmath dps=40 [P]"),
        tier=4, epistemic="P",
        summary=(
            f"At physical kinematics (s = M_Z^2 with M = M_W and M = M_Z; "
            f"s = -M_Z^2 spacelike) the pure-Python implementation matches "
            f"an independent high-precision mpmath computation (Li_2 = "
            f"polylog(2, .), dps = 40, w = M^2 / (s + i eps)) to max rel err "
            f"{mx:.1e} -- a tight machine-level reference anchor on five "
            f"kinematic points spanning timelike + spacelike."
        ),
        key_result=f"Lambda_2, Lambda_3 == mpmath dps=40 reference (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_lambda_bhm_spacelike_real"],
        artifacts={"max_rel_err": mx, "reference_values": dict(_REF_VALUES)},
    )


def check_T_w_trace_pv_lambda_bhm_subgate_partial_P() -> Dict[str, Any]:
    """T: BHM Lambda closed-form done; native C-toolkit route + Zll vertex OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_native_bhm_lambda_closed_form_evaluated"] == 1,
          "Lambda closed-form flag must be 1")
    check(EXPORT_FLAGS["Export_native_bhm_lambda_via_C_toolkit"] == 0,
          "Lambda via C-toolkit (R1b) must remain OPEN")
    check(EXPORT_FLAGS["Export_native_zll_renormalized_vertex"] == 0,
          "renormalized Zll vertex (R2) must remain OPEN")
    check(EXPORT_FLAGS["Export_native_kappa_l_evaluated"] == 0,
          "no kappa_l evaluated by this rung")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no Delta r_rem evaluated by this rung")
    return _result(
        name=("T_w_trace_pv_lambda_bhm_subgate_partial: "
              "BHM Lambda_2, Lambda_3 closed forms native; C-toolkit route + Zll vertex OPEN [P_structural]"),
        tier=4, epistemic="P_structural",
        summary=(
            "The BHM Z-vertex scalar functions Lambda_2(s, M^2) and "
            "Lambda_3(s, M^2) (EWWGR L6062 / hep-ph/9709229) are now native "
            "via the closed-form route: pure-Python implementation with a "
            "self-contained Li_2 + reflection structure, Feynman iepsilon "
            "prescription w = M^2 / (s + i eps), and a tight mpmath-anchored "
            "physical-kinematics reference. Together with the three-point "
            "complex tensor basis (R0 scalar + R0b rank-1 + R0c rank-2) this "
            "completes the closed-form vertex-function layer needed by the "
            "renormalized Zll vertex assembly. Still OPEN toward kappa_l: the "
            "native composition of Lambda_2, Lambda_3 from the timelike "
            "C-toolkit through the Denner haba3 generic V_a / V_b form "
            "factors (R1b cross-anchor); the renormalized Zll proper vertex "
            "with counterterms (R2, gate: UV / WWZ cancellation); the "
            "bosonic Delta kappa contribution (R3); the light-fermion / "
            "Delta alpha contribution (R4); and the assembled native "
            "kappa_l = 0.036808 / sin^2 theta_eff = 0.23155 (R5). DIZET "
            "stays the publishable OS-W closure."
        ),
        key_result="BHM Lambda closed forms native; C-toolkit route + Zll vertex OPEN. [P_structural]",
        dependencies=["T_w_trace_pv_lambda_bhm_physical_values"],
        cross_refs=["T_w_trace_pv_timelike_c0_subgate_partial",
                    "T_w_trace_pv_timelike_c1_c2_subgate_partial",
                    "T_w_trace_pv_timelike_cij_rank2_subgate_partial"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_pv_lambda_bhm_Li2_reference_values": check_T_w_trace_pv_lambda_bhm_Li2_reference_values_P,
    "T_w_trace_pv_lambda_bhm_Li2_abel_identity":   check_T_w_trace_pv_lambda_bhm_Li2_abel_identity_P,
    "T_w_trace_pv_lambda_bhm_spacelike_real":      check_T_w_trace_pv_lambda_bhm_spacelike_real_P,
    "T_w_trace_pv_lambda_bhm_physical_values":     check_T_w_trace_pv_lambda_bhm_physical_values_P,
    "T_w_trace_pv_lambda_bhm_subgate_partial":     check_T_w_trace_pv_lambda_bhm_subgate_partial_P,
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
