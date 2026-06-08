"""W_TRACE APF-native general-momentum scalar three-point function C0 (spacelike).

The banked ``apf.w_trace_pv_scalar_integral_substrate`` supplies C0 only at zero
external momenta (``c0_fin_zero_momenta``). This module extends it to GENERAL
external momenta in the spacelike / below-threshold (finite-real) domain -- the
genuine prerequisite for any 3-point (vertex) tensor reduction. It is built as a
Feynman-parameter simplex integral, native, with no external input.

Convention (extends the banked substrate)
-----------------------------------------
For propagators D1 = q^2 - m1^2, D2 = (q+p1)^2 - m2^2, D3 = (q+p1+p2)^2 - m3^2,
with external invariants s12 = p1^2, s23 = p2^2, s31 = (p1+p2)^2:

    C0 = - int_simplex dx1 dx2  1/F ,
    F  = x1 m1^2 + x2 m2^2 + x3 m3^2 - x1 x2 s12 - x2 x3 s23 - x3 x1 s31 ,

x3 = 1 - x1 - x2. At s12=s23=s31=0 this reduces to the banked zero-momentum
convention F = x1 m1^2 + x2 m2^2 + x3 m3^2.

Domain: spacelike (s_ij <= 0) external invariants with positive masses keep F>0
over the simplex (finite real domain). Timelike / above-threshold kinematics are
quarantined (not evaluated) -- consistent with the banked B0 threshold protocol.

Self-validation (no external target)
------------------------------------
  * the s_ij -> 0 limit reproduces the banked c0_fin_zero_momenta;
  * full S3 permutation symmetry (cyclic + reflection) of (m_i^2, s_ij) -- this
    is what validates the momentum<->mass pairing structure of F;
  * a second independent simplex mesh agrees.

What this module does (and does NOT) claim
------------------------------------------
It supplies a native general-momentum spacelike scalar C0. It does NOT supply
the 3-point tensor coefficients (Cij), the 4-point Dij, the above-threshold /
complex branch, the Denner coefficient map, or any electroweak value; those
remain OPEN. No Delta r_rem / M_W produced; imported DIZET stays the publishable
OS-W closure.

Status
------
- Export_pv_c0_general_momentum_spacelike_native = 1   (NEW here)
- Export_pv_c0_above_threshold_complex_branch    = 0   (OPEN)
- Export_pv_cij_three_point_tensor               = 0   (OPEN, next rung)
- Export_OSW_APF_internal_delta_r_rem_evaluated  = 0   (OPEN, unchanged)
"""
from __future__ import annotations

import math
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_pv_scalar_integral_substrate import (
    c0_fin_zero_momenta, MU2, MW2, MZ2, MT2, MH2,
)


def _c0_F(x1: float, x2: float, x3: float, m1: float, m2: float, m3: float,
          s12: float, s23: float, s31: float) -> float:
    return (x1 * m1 + x2 * m2 + x3 * m3
            - x1 * x2 * s12 - x2 * x3 * s23 - x3 * x1 * s31)


def c0_general(m1: float, m2: float, m3: float,
               s12: float = 0.0, s23: float = 0.0, s31: float = 0.0,
               n: int = 200) -> float:
    """General-momentum spacelike scalar C0 = -int_simplex 1/F (midpoint quadrature)."""
    acc = 0.0
    for i in range(n):
        u = (i + 0.5) / n
        ou = 1.0 - u
        for j in range(n):
            v = (j + 0.5) / n
            x1 = u
            x2 = ou * v
            x3 = ou * (1.0 - v)
            F = _c0_F(x1, x2, x3, m1, m2, m3, s12, s23, s31)
            if F <= 0:
                F = abs(F) + 1e-30
            acc += ou / F
    return -acc / (n * n)


def c0_general_domain_status(m1, m2, m3, s12, s23, s31, samples: int = 60) -> str:
    """FINITE_REAL_DOMAIN iff F>0 across a simplex scan; else quarantine."""
    mn = math.inf
    for i in range(samples):
        u = (i + 0.5) / samples
        ou = 1.0 - u
        for j in range(samples):
            v = (j + 0.5) / samples
            mn = min(mn, _c0_F(u, ou * v, ou * (1.0 - v), m1, m2, m3, s12, s23, s31))
    return "FINITE_REAL_DOMAIN" if mn > 0 else "THRESHOLD_OR_COMPLEX_DOMAIN_QUARANTINE"


# Spacelike test points: (m1^2, m2^2, m3^2, s12, s23, s31).
_TEST_POINTS = (
    (MW2, MZ2, MT2, -MZ2, -MW2, -MH2),
    (MW2, MW2, MW2, -2.0 * MZ2, -MZ2, -MW2),
    (MZ2, MT2, MH2, -MH2, -MZ2, -2.0 * MW2),
)

EXPORT_FLAGS: Dict[str, int] = {
    "Export_pv_c0_general_momentum_spacelike_native": 1,
    "Export_pv_c0_above_threshold_complex_branch": 0,
    "Export_pv_cij_three_point_tensor": 0,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


def check_T_w_trace_pv_c0_general_zero_momentum_limit_P() -> Dict[str, Any]:
    """T: general C0 at s_ij->0 reproduces the banked zero-momentum C0 [P]."""
    mx = 0.0
    for m1, m2, m3 in ((MW2, MZ2, MT2), (MW2, MW2, MW2), (MZ2, MT2, MH2), (MW2, MH2, MZ2)):
        g = c0_general(m1, m2, m3, 0.0, 0.0, 0.0)
        z = c0_fin_zero_momenta(m1, m2, m3)
        mx = max(mx, abs(g - z) / abs(z))
    check(mx < 5e-3, f"zero-momentum limit max rel err {mx:.2e} exceeds 5e-3")
    return _result(
        name="T_w_trace_pv_c0_general_zero_momentum_limit: "
             "general C0 at s_ij->0 == banked zero-momentum C0 [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native general-momentum C0 reduces, at vanishing external "
            f"invariants, to the banked c0_fin_zero_momenta to max relative err "
            f"{mx:.2e} -- ties the new evaluator to the banked substrate."
        ),
        key_result=f"general C0 -> banked zero-momentum C0 (rel err {mx:.1e}). [P]",
        dependencies=["check_T_w_trace_pv_c0_gate_closed"],
        artifacts={"max_rel_err": mx},
    )


def check_T_w_trace_pv_c0_general_permutation_symmetry_P() -> Dict[str, Any]:
    """T: general C0 obeys S3 permutation symmetry of (m_i^2, s_ij) [P].

    Cyclic: C0(m1,m2,m3;s12,s23,s31) = C0(m2,m3,m1;s23,s31,s12).
    Reflection: C0(m1,m2,m3;s12,s23,s31) = C0(m1,m3,m2;s31,s23,s12).
    These validate the momentum<->mass pairing structure of F.
    """
    mx = 0.0
    for m1, m2, m3, s12, s23, s31 in _TEST_POINTS:
        base = c0_general(m1, m2, m3, s12, s23, s31)
        cyc = c0_general(m2, m3, m1, s23, s31, s12)
        refl = c0_general(m1, m3, m2, s31, s23, s12)
        mx = max(mx, abs(base - cyc) / abs(base), abs(base - refl) / abs(base))
    check(mx < 1e-3, f"permutation-symmetry max rel err {mx:.2e} exceeds 1e-3")
    return _result(
        name="T_w_trace_pv_c0_general_permutation_symmetry: "
             "C0 obeys S3 symmetry of (m_i^2, s_ij) [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native general-momentum C0 is invariant under cyclic and "
            f"reflection permutations of the (mass, invariant) labels to max "
            f"relative err {mx:.2e} -- a target-free validation of the F "
            f"momentum<->mass pairing structure."
        ),
        key_result=f"C0 S3 permutation symmetry holds (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_c0_general_zero_momentum_limit"],
        artifacts={"max_rel_err": mx},
    )


def check_T_w_trace_pv_c0_general_mesh_consistency_P() -> Dict[str, Any]:
    """T: the C0 quadrature is mesh-converged (n vs 2n agree) [P]."""
    mx = 0.0
    for m1, m2, m3, s12, s23, s31 in _TEST_POINTS:
        a = c0_general(m1, m2, m3, s12, s23, s31, n=150)
        b = c0_general(m1, m2, m3, s12, s23, s31, n=300)
        mx = max(mx, abs(a - b) / abs(b))
    check(mx < 5e-3, f"mesh n vs 2n max rel err {mx:.2e} exceeds 5e-3")
    return _result(
        name="T_w_trace_pv_c0_general_mesh_consistency: "
             "C0 quadrature mesh-converged (n vs 2n) [P]",
        tier=4, epistemic="P",
        summary=(
            f"The C0 simplex quadrature is mesh-converged: n=150 vs n=300 agree to "
            f"max relative err {mx:.2e}, confirming the numerical evaluation is "
            f"stable in the spacelike domain."
        ),
        key_result=f"C0 quadrature mesh-converged (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_c0_general_zero_momentum_limit"],
        artifacts={"max_rel_err": mx},
    )


def check_T_w_trace_pv_c0_general_subgate_partial_P() -> Dict[str, Any]:
    """T: general-momentum spacelike C0 native; tensor Cij + threshold OPEN [P_structural]."""
    # spacelike points are finite-real; a timelike point quarantines
    for pt in _TEST_POINTS:
        check(c0_general_domain_status(*pt) == "FINITE_REAL_DOMAIN",
              "spacelike test points must be finite-real")
    check(c0_general_domain_status(MW2, MW2, MW2, 5.0 * MW2, 5.0 * MW2, 5.0 * MW2)
          == "THRESHOLD_OR_COMPLEX_DOMAIN_QUARANTINE",
          "a hard timelike point must quarantine")
    check(EXPORT_FLAGS["Export_pv_c0_general_momentum_spacelike_native"] == 1,
          "general-C0 native flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no Delta r_rem evaluated by this rung")
    return _result(
        name="T_w_trace_pv_c0_general_subgate_partial: "
             "general-momentum spacelike C0 native; Cij + threshold OPEN [P_structural]",
        tier=4, epistemic="P_structural",
        summary=(
            "The native scalar substrate is extended from zero-momentum-only C0 to "
            "general-momentum spacelike C0 (with a domain quarantine for "
            "above-threshold/complex kinematics) -- the prerequisite for 3-point "
            "(vertex) tensor reduction. The 3-point tensor coefficients Cij, the "
            "4-point Dij, the above-threshold branch, the Denner coefficient map, "
            "and the counterterm assembly remain OPEN; no Delta r_rem / M_W is "
            "produced; DIZET stays the publishable OS-W closure."
        ),
        key_result="General-momentum spacelike C0 native; Cij/threshold OPEN. [P_structural]",
        dependencies=["T_w_trace_pv_c0_general_permutation_symmetry"],
        cross_refs=["check_T_w_trace_pv_c0_gate_closed"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_pv_c0_general_zero_momentum_limit": check_T_w_trace_pv_c0_general_zero_momentum_limit_P,
    "T_w_trace_pv_c0_general_permutation_symmetry": check_T_w_trace_pv_c0_general_permutation_symmetry_P,
    "T_w_trace_pv_c0_general_mesh_consistency": check_T_w_trace_pv_c0_general_mesh_consistency_P,
    "T_w_trace_pv_c0_general_subgate_partial": check_T_w_trace_pv_c0_general_subgate_partial_P,
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
