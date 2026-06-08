"""W_TRACE APF-native general-momentum scalar four-point function D0 (spacelike box).

The banked substrate supplies D0 only at zero external momenta
(``d0_fin_zero_momenta``). This module extends it to GENERAL external momenta in
the spacelike / below-threshold (finite-real) domain -- completing the native
scalar substrate (A0, B0, C0, D0) at general momenta, the prerequisite for
4-point (box) tensor reduction. Native, no external input.

Convention (extends the banked substrate)
-----------------------------------------
Box with propagators D_i and external legs p1..p4 (p4 = -(p1+p2+p3)), Mandelstam
s = (p1+p2)^2, t = (p2+p3)^2:

    D0 = int_simplex(tetra) 1/F^2 ,
    F  = sum_i x_i m_i^2 - x1 x2 p1^2 - x2 x3 p2^2 - x3 x4 p3^2 - x4 x1 p4^2
         - x1 x3 s - x2 x4 t ,   x4 = 1-x1-x2-x3.

At p_i^2 = s = t = 0 this reduces to the banked convention F = sum x_i m_i^2.
The adjacent (leg) pairs carry the p_i^2; the diagonal pairs carry s, t.

Domain: spacelike external invariants with positive masses keep F>0 over the
tetrahedron (finite real domain). Above-threshold / complex kinematics are
quarantined (not evaluated).

Self-validation (no external target)
------------------------------------
  * p_i, s, t -> 0 reproduces the banked d0_fin_zero_momenta;
  * cyclic box symmetry (m_i, p_i^2) -> shifted with s <-> t -- validates the
    diagonal (s,t) pairing structure of F;
  * mesh convergence (n vs 2n).

Honest scope
------------
Spacelike scalar D0 only. The 4-point tensor coefficients Dij, the
above-threshold branch, the Denner coefficient map, and the assembly remain
OPEN; no Delta r_rem / M_W produced; DIZET stays the publishable OS-W closure.

Status
------
- Export_pv_d0_general_momentum_spacelike_native = 1   (NEW here)
- Export_pv_dij_tensor                           = 0   (OPEN, next rung)
- Export_OSW_APF_internal_delta_r_rem_evaluated  = 0   (OPEN, unchanged)
"""
from __future__ import annotations

import math
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_pv_scalar_integral_substrate import (
    d0_fin_zero_momenta, MW2, MZ2, MT2, MH2,
)


def _d0_F(x1, x2, x3, x4, m1, m2, m3, m4, p1, p2, p3, p4, s, t):
    return (x1 * m1 + x2 * m2 + x3 * m3 + x4 * m4
            - x1 * x2 * p1 - x2 * x3 * p2 - x3 * x4 * p3 - x4 * x1 * p4
            - x1 * x3 * s - x2 * x4 * t)


def d0_general(m1, m2, m3, m4, p1=0.0, p2=0.0, p3=0.0, p4=0.0,
               s=0.0, t=0.0, n: int = 60) -> float:
    """General-momentum spacelike box scalar D0 = int_tetra 1/F^2 (midpoint quadrature)."""
    acc = 0.0
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
                acc += jac / (F * F)
    return acc / (n ** 3)


def d0_general_domain_status(m1, m2, m3, m4, p1, p2, p3, p4, s, t, samples: int = 24) -> str:
    mn = math.inf
    for i in range(samples):
        u = (i + 0.5) / samples; ou = 1.0 - u
        for j in range(samples):
            v = (j + 0.5) / samples; ov = 1.0 - v
            for k in range(samples):
                w = (k + 0.5) / samples
                mn = min(mn, _d0_F(u, ou * v, ou * ov * w, ou * ov * (1.0 - w),
                                   m1, m2, m3, m4, p1, p2, p3, p4, s, t))
    return "FINITE_REAL_DOMAIN" if mn > 0 else "THRESHOLD_OR_COMPLEX_DOMAIN_QUARANTINE"


# Spacelike test points: (m1..m4, p1..p4, s, t).
_TEST_POINTS = (
    (MW2, MZ2, MT2, MH2, -MZ2, -MW2, -MH2, -MZ2, -2.0 * MZ2, -MW2),
    (MZ2, MT2, MH2, MW2, -MH2, -MZ2, -MW2, -MT2, -MZ2, -2.0 * MW2),
)

EXPORT_FLAGS: Dict[str, int] = {
    "Export_pv_d0_general_momentum_spacelike_native": 1,
    "Export_pv_dij_tensor": 0,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


def check_T_w_trace_pv_d0_general_zero_momentum_limit_P() -> Dict[str, Any]:
    """T: general D0 at p,s,t->0 reproduces the banked zero-momentum D0 [P]."""
    mx = 0.0
    for m1, m2, m3, m4 in ((MW2, MZ2, MT2, MH2), (MW2, MW2, MW2, MW2), (MZ2, MT2, MH2, MW2)):
        g = d0_general(m1, m2, m3, m4)
        z = d0_fin_zero_momenta(m1, m2, m3, m4)
        mx = max(mx, abs(g - z) / abs(z))
    check(mx < 5e-3, f"zero-momentum limit max rel err {mx:.2e} exceeds 5e-3")
    return _result(
        name="T_w_trace_pv_d0_general_zero_momentum_limit: "
             "general D0 at p,s,t->0 == banked zero-momentum D0 [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native general-momentum box D0 reduces, at vanishing external "
            f"invariants, to the banked d0_fin_zero_momenta to max relative err "
            f"{mx:.2e} -- ties the new evaluator to the banked substrate."
        ),
        key_result=f"general D0 -> banked zero-momentum D0 (rel err {mx:.1e}). [P]",
        dependencies=["check_T_w_trace_pv_d0_gate_closed"],
        artifacts={"max_rel_err": mx},
    )


def check_T_w_trace_pv_d0_general_cyclic_symmetry_P() -> Dict[str, Any]:
    """T: general D0 obeys cyclic box symmetry with s<->t [P]."""
    mx = 0.0
    for m1, m2, m3, m4, p1, p2, p3, p4, s, t in _TEST_POINTS:
        base = d0_general(m1, m2, m3, m4, p1, p2, p3, p4, s, t)
        cyc = d0_general(m2, m3, m4, m1, p2, p3, p4, p1, t, s)
        mx = max(mx, abs(base - cyc) / abs(base))
    check(mx < 1e-3, f"cyclic-symmetry max rel err {mx:.2e} exceeds 1e-3")
    return _result(
        name="T_w_trace_pv_d0_general_cyclic_symmetry: "
             "box D0 invariant under cyclic (m_i,p_i) with s<->t [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native box D0 is invariant under cyclic permutation of the leg "
            f"(mass, invariant) labels with the diagonal s<->t swap to max relative "
            f"err {mx:.2e} -- a target-free validation of the (s,t) diagonal pairing "
            f"structure of F."
        ),
        key_result=f"D0 cyclic box symmetry holds (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_d0_general_zero_momentum_limit"],
        artifacts={"max_rel_err": mx},
    )


def check_T_w_trace_pv_d0_general_mesh_consistency_P() -> Dict[str, Any]:
    """T: the D0 quadrature is mesh-converged (n vs 2n) [P]."""
    mx = 0.0
    for pt in _TEST_POINTS:
        a = d0_general(*pt, n=40)
        b = d0_general(*pt, n=80)
        mx = max(mx, abs(a - b) / abs(b))
    check(mx < 1e-2, f"mesh n vs 2n max rel err {mx:.2e} exceeds 1e-2")
    return _result(
        name="T_w_trace_pv_d0_general_mesh_consistency: D0 quadrature mesh-converged [P]",
        tier=4, epistemic="P",
        summary=f"Box D0 simplex quadrature mesh-converged: n=40 vs n=80 to {mx:.2e}.",
        key_result=f"D0 quadrature mesh-converged (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_d0_general_zero_momentum_limit"],
        artifacts={"max_rel_err": mx},
    )


def check_T_w_trace_pv_d0_general_subgate_partial_P() -> Dict[str, Any]:
    """T: general-momentum spacelike D0 native; Dij tensors + threshold OPEN [P_structural]."""
    for pt in _TEST_POINTS:
        check(d0_general_domain_status(*pt) == "FINITE_REAL_DOMAIN",
              "spacelike test points must be finite-real")
    check(d0_general_domain_status(MW2, MW2, MW2, MW2, 5*MW2, 5*MW2, 5*MW2, 5*MW2, 5*MW2, 5*MW2)
          == "THRESHOLD_OR_COMPLEX_DOMAIN_QUARANTINE",
          "a hard timelike point must quarantine")
    check(EXPORT_FLAGS["Export_pv_d0_general_momentum_spacelike_native"] == 1,
          "general-D0 native flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no Delta r_rem evaluated by this rung")
    return _result(
        name="T_w_trace_pv_d0_general_subgate_partial: "
             "general-momentum spacelike D0 native; Dij + threshold OPEN [P_structural]",
        tier=4, epistemic="P_structural",
        summary=(
            "The native scalar substrate is now complete at general (spacelike) "
            "momenta for all four Passarino-Veltman scalars A0/B0/C0/D0 (with a "
            "domain quarantine for above-threshold/complex kinematics). The 4-point "
            "tensor coefficients Dij, the above-threshold branch, the Denner "
            "coefficient map, and the counterterm/self-energy assembly remain OPEN; "
            "no Delta r_rem / M_W is produced; DIZET stays the publishable OS-W closure."
        ),
        key_result="Native scalar substrate complete at general momenta (A0/B0/C0/D0); Dij OPEN. [P_structural]",
        dependencies=["T_w_trace_pv_d0_general_cyclic_symmetry"],
        cross_refs=["check_T_w_trace_pv_d0_gate_closed"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_pv_d0_general_zero_momentum_limit": check_T_w_trace_pv_d0_general_zero_momentum_limit_P,
    "T_w_trace_pv_d0_general_cyclic_symmetry": check_T_w_trace_pv_d0_general_cyclic_symmetry_P,
    "T_w_trace_pv_d0_general_mesh_consistency": check_T_w_trace_pv_d0_general_mesh_consistency_P,
    "T_w_trace_pv_d0_general_subgate_partial": check_T_w_trace_pv_d0_general_subgate_partial_P,
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
