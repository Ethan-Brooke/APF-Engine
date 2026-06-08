"""W_TRACE APF-native PV three-point tensor reduction -- rank-1 (C1,C2) + rank-2 (C00,C11,C12,C22).

Native three-point tensor coefficients built on the general-momentum scalar C0
(apf.w_trace_pv_c0_general_momentum) and the banked B0/B1 two-point substrate.
No external input -- the native counterpart to the sibling reviewed-formula
route.

  v24.3.75: rank-1 C1, C2.
  v24.3.76: rank-2 C00, C11, C12, C22.

Tensor decomposition (D1=q^2-m1^2, D2=(q+p1)^2-m2^2, D3=(q+p1+p2)^2-m3^2;
s12=p1^2, s23=p2^2, s31=(p1+p2)^2; p1.p2=(s31-s12-s23)/2):

    C^mu      = p1^mu C1 + p2^mu C2
    C^{mu nu} = g^{mu nu} C00 + p1^mu p1^nu C11 + p2^mu p2^nu C22
                + (p1^mu p2^nu + p2^mu p1^nu) C12

Native finite-part forms (direct Feynman, loop-shift Q=(x2+x3)p1+x3 p2):
    C1  =  int dmu (x2+x3)/F ,        C2  =  int dmu x3/F
    C11 = -int dmu (x2+x3)^2/F ,      C22 = -int dmu x3^2/F ,
    C12 = -int dmu (x2+x3) x3 / F ,
    C00 = -1/2 int dmu ln(F/mu^2)     (carries the d=4-2eps metric-trace finite
                                       correction, VERIFIED via the trace relation)

Self-validation (no external target)
------------------------------------
  * rank-1: direct integral == PV Gram reduction (contraction identities tying
    C1,C2 to banked B0 sub-bubbles + C0), ~1e-5.
  * rank-2 metric-trace relation (ties to banked B0 + C0):
        4 C00 + s12 C11 + s23 C22 + 2 p1.p2 C12 - 1/2 = B0(s23;m2,m3) + m1^2 C0
  * rank-2 p1.p1 scalar contraction identity (ties to banked B0/B1 + C0/C1/C2):
        s12 C00 + s12^2 C11 + (p1.p2)^2 C22 + 2 s12 (p1.p2) C12
          = 1/2 [ (s12+p1.p2) B1(s31;m1,m3)
                  - ( (p1.p2) B1(s23;m2,m3) - s12 B0(s23;m2,m3) )
                  - (s12+m1^2-m2^2)(s12 C1 + p1.p2 C2) ]
  * mesh convergence (n vs 2n).

Honest scope
------------
Three-point coefficients (rank 1 + rank 2) in the spacelike domain. The 4-point
Dij, the above-threshold branch, the Denner coefficient map, and the
counterterm/self-energy assembly remain OPEN; no Delta r_rem / M_W produced;
DIZET stays the publishable OS-W closure.

Status
------
- Export_pv_c1_c2_rank1_threepoint_native = 1
- Export_pv_cij_rank2_threepoint          = 1   (NEW at v24.3.76)
- Export_pv_dij_four_point                = 0   (OPEN, next sector)
- Export_OSW_APF_internal_delta_r_rem_evaluated = 0  (OPEN, unchanged)
"""
from __future__ import annotations

import math
from typing import Any, Dict, Tuple

from apf.apf_utils import check, _result
from apf.w_trace_pv_scalar_integral_substrate import b0_fin, MU2, MW2, MZ2, MT2, MH2
from apf.w_trace_pv_c0_general_momentum import c0_general, _c0_F
from apf.w_trace_pv_tensor_reduction import b1_reduction


def c1_c2_direct(m1, m2, m3, s12, s23, s31, n: int = 300) -> Tuple[float, float]:
    """Direct Feynman-parameter rank-1 coefficients (C1, C2)."""
    a1 = 0.0
    a2 = 0.0
    for i in range(n):
        u = (i + 0.5) / n
        ou = 1.0 - u
        for j in range(n):
            v = (j + 0.5) / n
            x1 = u; x2 = ou * v; x3 = ou * (1.0 - v)
            F = _c0_F(x1, x2, x3, m1, m2, m3, s12, s23, s31)
            if F <= 0:
                F = abs(F) + 1e-30
            a1 += ou * (x2 + x3) / F
            a2 += ou * x3 / F
    return a1 / (n * n), a2 / (n * n)


def c1_c2_reduction(m1, m2, m3, s12, s23, s31) -> Tuple[float, float]:
    """PV Gram-matrix rank-1 coefficients (C1, C2) from banked B0 + native C0."""
    c0 = c0_general(m1, m2, m3, s12, s23, s31)
    p1p2 = (s31 - s12 - s23) / 2.0
    f1 = s12 + m1 - m2
    g2 = s23 + 2.0 * p1p2 + m2 - m3
    r1 = 0.5 * (b0_fin(s31, m1, m3) - b0_fin(s23, m2, m3) - f1 * c0)
    r2 = 0.5 * (b0_fin(s12, m1, m2) - b0_fin(s31, m1, m3) - g2 * c0)
    det = s12 * s23 - p1p2 * p1p2
    return (s23 * r1 - p1p2 * r2) / det, (s12 * r2 - p1p2 * r1) / det


def cij_rank2_direct(m1, m2, m3, s12, s23, s31, n: int = 260) -> Dict[str, float]:
    """Direct Feynman-parameter rank-2 coefficients (C00, C11, C22, C12)."""
    c00 = c11 = c22 = c12 = 0.0
    for i in range(n):
        u = (i + 0.5) / n
        ou = 1.0 - u
        for j in range(n):
            v = (j + 0.5) / n
            x1 = u; x2 = ou * v; x3 = ou * (1.0 - v)
            F = _c0_F(x1, x2, x3, m1, m2, m3, s12, s23, s31)
            Fp = F if F > 0 else abs(F) + 1e-30
            c00 += ou * (-0.5 * math.log(Fp / MU2))
            c11 += ou * (-(x2 + x3) ** 2 / Fp)
            c22 += ou * (-(x3 ** 2) / Fp)
            c12 += ou * (-(x2 + x3) * x3 / Fp)
    N = n * n
    return {"C00": c00 / N, "C11": c11 / N, "C22": c22 / N, "C12": c12 / N}


_TEST_POINTS = (
    (MW2, MZ2, MT2, -MZ2, -MW2, -MH2),
    (MZ2, MT2, MH2, -MH2, -MZ2, -2.0 * MW2),
    (MW2, MW2, MW2, -2.0 * MZ2, -MZ2, -MW2),
)

EXPORT_FLAGS: Dict[str, int] = {
    "Export_pv_c1_c2_rank1_threepoint_native": 1,
    "Export_pv_cij_rank2_threepoint": 1,
    "Export_pv_dij_four_point": 0,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


def check_T_w_trace_pv_c1_c2_reduction_matches_direct_P() -> Dict[str, Any]:
    """T: PV Gram reduction (banked B0 + native C0) == direct Feynman C1,C2 [P]."""
    mx = 0.0
    for m1, m2, m3, s12, s23, s31 in _TEST_POINTS:
        d1, d2 = c1_c2_direct(m1, m2, m3, s12, s23, s31)
        r1, r2 = c1_c2_reduction(m1, m2, m3, s12, s23, s31)
        mx = max(mx, abs(d1 - r1) / max(1e-12, abs(d1)), abs(d2 - r2) / max(1e-12, abs(d2)))
    check(mx < 1e-3, f"reduction vs direct max rel err {mx:.2e} exceeds 1e-3")
    return _result(
        name="T_w_trace_pv_c1_c2_reduction_matches_direct: "
             "PV Gram reduction == direct Feynman C1,C2 [P]",
        tier=4, epistemic="P",
        summary=(
            f"Rank-1 C1,C2 from the PV Gram reduction (contraction identities, banked "
            f"B0 sub-bubbles + native C0) agree with the direct Feynman integral to "
            f"max relative err {mx:.2e}."
        ),
        key_result=f"C1,C2 Gram reduction == direct (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_c0_general_zero_momentum_limit", "check_T_w_trace_pv_b0_gate_closed"],
        artifacts={"max_rel_err": mx},
    )


def check_T_w_trace_pv_c1_c2_mesh_consistency_P() -> Dict[str, Any]:
    """T: the direct C1,C2 quadrature is mesh-converged (n vs 2n) [P]."""
    mx = 0.0
    for m1, m2, m3, s12, s23, s31 in _TEST_POINTS:
        a1, a2 = c1_c2_direct(m1, m2, m3, s12, s23, s31, n=150)
        b1, b2 = c1_c2_direct(m1, m2, m3, s12, s23, s31, n=300)
        mx = max(mx, abs(a1 - b1) / max(1e-12, abs(b1)), abs(a2 - b2) / max(1e-12, abs(b2)))
    check(mx < 5e-3, f"mesh n vs 2n max rel err {mx:.2e} exceeds 5e-3")
    return _result(
        name="T_w_trace_pv_c1_c2_mesh_consistency: C1,C2 quadrature mesh-converged [P]",
        tier=4, epistemic="P",
        summary=f"Direct C1,C2 quadrature mesh-converged: n=150 vs n=300 to {mx:.2e}.",
        key_result=f"C1,C2 mesh-converged (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_c1_c2_reduction_matches_direct"],
        artifacts={"max_rel_err": mx},
    )


def check_T_w_trace_pv_cij_rank2_trace_relation_P() -> Dict[str, Any]:
    """T: rank-2 Cij satisfy the metric-trace relation vs banked B0 + C0 [P]."""
    mx = 0.0
    for m1, m2, m3, s12, s23, s31 in _TEST_POINTS:
        c0 = c0_general(m1, m2, m3, s12, s23, s31)
        c = cij_rank2_direct(m1, m2, m3, s12, s23, s31)
        p1p2 = (s31 - s12 - s23) / 2.0
        lhs = 4.0 * c["C00"] + s12 * c["C11"] + s23 * c["C22"] + 2.0 * p1p2 * c["C12"] - 0.5
        rhs = b0_fin(s23, m2, m3) + m1 * c0
        mx = max(mx, abs(lhs - rhs) / max(1.0, abs(rhs)))
    check(mx < 1e-4, f"trace-relation max rel err {mx:.2e} exceeds 1e-4")
    return _result(
        name="T_w_trace_pv_cij_rank2_trace_relation: "
             "4 C00 + s12 C11 + s23 C22 + 2 p1.p2 C12 - 1/2 = B0 + m1^2 C0 [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native rank-2 three-point coefficients satisfy the finite d=4-2eps "
            f"metric-trace relation against the banked B0 + native C0 to max relative "
            f"err {mx:.2e} -- validates C00 (incl. the -1/2 trace finite correction) "
            f"and the C11/C22/C12 combination, target-free."
        ),
        key_result=f"Cij trace relation holds vs banked B0/C0 (rel err {mx:.1e}). [P]",
        dependencies=["check_T_w_trace_pv_b0_gate_closed", "T_w_trace_pv_c0_general_zero_momentum_limit"],
        artifacts={"max_rel_err": mx},
    )


def check_T_w_trace_pv_cij_rank2_contraction_identity_P() -> Dict[str, Any]:
    """T: rank-2 Cij satisfy the p1.p1 scalar contraction vs banked B0/B1 + C0/C1/C2 [P]."""
    mx = 0.0
    for m1, m2, m3, s12, s23, s31 in _TEST_POINTS:
        c0 = c0_general(m1, m2, m3, s12, s23, s31)
        c = cij_rank2_direct(m1, m2, m3, s12, s23, s31)
        c1, c2 = c1_c2_direct(m1, m2, m3, s12, s23, s31)
        p1p2 = (s31 - s12 - s23) / 2.0
        f1 = s12 + m1 - m2
        lhs = (s12 * c["C00"] + s12 ** 2 * c["C11"] + p1p2 ** 2 * c["C22"]
               + 2.0 * s12 * p1p2 * c["C12"])
        rhs = 0.5 * ((s12 + p1p2) * b1_reduction(s31, m1, m3)
                     - (p1p2 * b1_reduction(s23, m2, m3) - s12 * b0_fin(s23, m2, m3))
                     - f1 * (s12 * c1 + p1p2 * c2))
        mx = max(mx, abs(lhs - rhs) / max(1.0, abs(rhs)))
    check(mx < 1e-3, f"p1.p1 contraction max rel err {mx:.2e} exceeds 1e-3")
    return _result(
        name="T_w_trace_pv_cij_rank2_contraction_identity: "
             "p1.p1 C^{mu nu} ties rank-2 Cij to banked B0/B1 + C0/C1/C2 [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native rank-2 Cij satisfy the p1.p1 scalar contraction identity "
            f"(p1_mu p1_nu C^{{mu nu}} expressed through the banked B1/B0 sub-bubbles "
            f"and C0/C1/C2) to max relative err {mx:.2e} -- a target-free validation "
            f"of the full rank-2 tensor structure against banked quantities."
        ),
        key_result=f"Cij p1.p1 contraction holds (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_cij_rank2_trace_relation",
                      "T_w_trace_pv_c1_c2_reduction_matches_direct"],
        artifacts={"max_rel_err": mx},
    )


def check_T_w_trace_pv_cij_rank2_mesh_consistency_P() -> Dict[str, Any]:
    """T: the rank-2 Cij quadrature is mesh-converged (n vs 2n) [P]."""
    mx = 0.0
    for m1, m2, m3, s12, s23, s31 in _TEST_POINTS:
        a = cij_rank2_direct(m1, m2, m3, s12, s23, s31, n=130)
        b = cij_rank2_direct(m1, m2, m3, s12, s23, s31, n=260)
        for k in ("C00", "C11", "C22", "C12"):
            mx = max(mx, abs(a[k] - b[k]) / max(1e-9, abs(b[k])))
    check(mx < 1e-2, f"rank-2 mesh n vs 2n max rel err {mx:.2e} exceeds 1e-2")
    return _result(
        name="T_w_trace_pv_cij_rank2_mesh_consistency: rank-2 Cij quadrature mesh-converged [P]",
        tier=4, epistemic="P",
        summary=f"Rank-2 Cij quadrature mesh-converged: n=130 vs n=260 to {mx:.2e}.",
        key_result=f"Cij rank-2 mesh-converged (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_cij_rank2_trace_relation"],
        artifacts={"max_rel_err": mx},
    )


def check_T_w_trace_pv_c_tensor_subgate_partial_P() -> Dict[str, Any]:
    """T: three-point tensors (rank 1+2) native; 4-point + assembly OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_pv_c1_c2_rank1_threepoint_native"] == 1, "rank-1 flag must be 1")
    check(EXPORT_FLAGS["Export_pv_cij_rank2_threepoint"] == 1, "rank-2 flag must be 1")
    check(EXPORT_FLAGS["Export_pv_dij_four_point"] == 0, "4-point Dij must remain OPEN")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no Delta r_rem evaluated by these rungs")
    return _result(
        name="T_w_trace_pv_c_tensor_subgate_partial: "
             "three-point tensors (rank 1+2) native; 4-point + assembly OPEN [P_structural]",
        tier=4, epistemic="P_structural",
        summary=(
            "The native three-point tensor basis is complete through rank 2 "
            "(C1,C2,C00,C11,C12,C22), built on the general-momentum C0 + banked "
            "B0/B1. The 4-point Dij, the above-threshold branch, the Denner "
            "coefficient map, and the self-energy/counterterm assembly remain OPEN; "
            "no Delta r_rem / M_W is produced; DIZET stays the publishable OS-W closure."
        ),
        key_result="Three-point tensor basis native through rank 2; 4-point OPEN. [P_structural]",
        dependencies=["T_w_trace_pv_cij_rank2_contraction_identity"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_pv_c1_c2_reduction_matches_direct": check_T_w_trace_pv_c1_c2_reduction_matches_direct_P,
    "T_w_trace_pv_c1_c2_mesh_consistency": check_T_w_trace_pv_c1_c2_mesh_consistency_P,
    "T_w_trace_pv_cij_rank2_trace_relation": check_T_w_trace_pv_cij_rank2_trace_relation_P,
    "T_w_trace_pv_cij_rank2_contraction_identity": check_T_w_trace_pv_cij_rank2_contraction_identity_P,
    "T_w_trace_pv_cij_rank2_mesh_consistency": check_T_w_trace_pv_cij_rank2_mesh_consistency_P,
    "T_w_trace_pv_c_tensor_subgate_partial": check_T_w_trace_pv_c_tensor_subgate_partial_P,
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
