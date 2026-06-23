"""W_TRACE APF-native Passarino-Veltman tensor reduction -- two-point (B1, B00, B11).

Native rungs of the OPEN ``G2F_TENSOR_REDUCTION`` gate named by
``apf.w_trace_pv_scalar_integral_substrate`` ("PV tensor reduction coefficients
B1/B00/Cij/Dij -- not yet APF-owned"). This module makes the two-point tensor
coefficients APF-owned, built ENTIRELY on the already-banked finite scalar
substrate (A0/B0) -- no external input, no reviewed-formula import, no fitted
coefficient. It is the *native* counterpart to the sibling reviewed-formula
evaluator harness route.

  v24.3.71: rank-1 two-point B1.
  v24.3.72: rank-2 two-point B00, B11.

Convention (inherited from the banked substrate)
------------------------------------------------
On-shell finite parts, mu^2 = M_Z^2, A0_fin = m^2(1 - ln(m^2/mu^2)),
B0_fin = - int_0^1 dx ln(F/mu^2), with the Feynman denominator
F(x) = x m1^2 + (1-x) m0^2 - x(1-x) p^2 for propagators D0 = q^2 - m0^2,
D1 = (q+p)^2 - m1^2. Tensor decomposition B^mu = p^mu B1,
B^{mu nu} = g^{mu nu} B00 + p^mu p^nu B11.

Native finite-part forms (direct Feynman-parameter integrals)
-------------------------------------------------------------
  B1  =  int_0^1 dx  x   ln(F/mu^2)
  B11 = -int_0^1 dx  x^2 ln(F/mu^2)
  B00 =  int_0^1 dx (F/2) (1 - ln(F/mu^2))

The B00 form carries the d=4-2eps metric-trace finite correction (the
eps x 1/eps cross term contributes +F/4 inside the integrand); it is verified
below against the banked substrate, not assumed.

Self-validation (no external target)
------------------------------------
  * B1: two independent implementations (reduction formula on A0/B0 vs direct
    integral) cross-check ~1e-8; exact identities (equal-mass B1=-B0/2;
    argument-swap B1(m0,m1)+B1(m1,m0)=-B0 ~1e-15); massless closed form.
  * B00/B11: the finite metric-trace relation
        4 B00 + p^2 B11 - (m0^2/2 + m1^2/2 - p^2/6) = A0(m1^2) + m0^2 B0
    ties the native B00,B11 to the banked A0/B0 (~1e-8 relative); plus the
    massless closed forms B11(p^2,0,0) = -1/3 ln(|p^2|/mu^2) + 13/18 and
    B00(p^2,0,0) = |p^2|(2/9 - ln(|p^2|/mu^2)/12).

What this module does (and does NOT) claim
------------------------------------------
It closes the two-point tensor coefficients (B1, B00, B11) natively. It does
NOT close the 3-/4-point Cij/Dij, the Denner coefficient map, or the
counterterm assembly -- those remain OPEN. No Delta r_rem / DeltaRhobarW / M_W
value is produced; the imported DIZET route stays the publishable OS-W closure.

Status
------
- Export_pv_b1_rank1_twopoint_native = 1
- Export_pv_b00_b11_rank2_twopoint   = 1   (NEW at v24.3.72)
- Export_pv_cij_dij_three_four_point = 0   (OPEN, next rung)
- Export_OSW_APF_internal_delta_r_rem_evaluated = 0  (OPEN, unchanged)
"""
from __future__ import annotations

import math
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_pv_scalar_integral_substrate import (
    a0_fin, b0_fin, MU2, MW2, MZ2, MT2, MH2,
)


# ============================================================================
# Native two-point tensor coefficients
# ============================================================================

def _a0_safe(m2: float) -> float:
    """A0 finite part, massless-safe (A0(0) = 0 in dimensional regularization)."""
    return 0.0 if m2 == 0 else a0_fin(m2)


def _delta(x: float, p2: float, m02: float, m12: float) -> float:
    return x * m12 + (1.0 - x) * m02 - x * (1.0 - x) * p2


def b1_reduction(p2: float, m02: float, m12: float, mu2: float = MU2) -> float:
    """B1 finite part via the standard PV reduction on the banked A0/B0."""
    if p2 == 0:
        raise ValueError("b1_reduction requires p2 != 0 (use the p2->0 limit form)")
    f1 = p2 + m02 - m12
    return (_a0_safe(m02) - _a0_safe(m12) - f1 * b0_fin(p2, m02, m12, mu2)) / (2.0 * p2)


def b1_direct(p2: float, m02: float, m12: float, mu2: float = MU2, n: int = 20000) -> float:
    """B1 finite part via the direct Feynman-parameter integral (independent)."""
    h = 1.0 / n
    acc = 0.0
    for i in range(n):
        x = (i + 0.5) * h
        F = _delta(x, p2, m02, m12)
        if F <= 0:
            F = abs(F) + 1e-30
        acc += x * math.log(F / mu2)
    return h * acc


def b11_direct(p2: float, m02: float, m12: float, mu2: float = MU2, n: int = 40000) -> float:
    """B11 finite part: -int_0^1 dx x^2 ln(F/mu^2)."""
    h = 1.0 / n
    acc = 0.0
    for i in range(n):
        x = (i + 0.5) * h
        F = _delta(x, p2, m02, m12)
        if F <= 0:
            F = abs(F) + 1e-30
        acc += x * x * math.log(F / mu2)
    return -h * acc


def b00_direct(p2: float, m02: float, m12: float, mu2: float = MU2, n: int = 40000) -> float:
    """B00 finite part: int_0^1 dx (F/2)(1 - ln(F/mu^2)) (d=4-2eps trace-corrected)."""
    h = 1.0 / n
    acc = 0.0
    for i in range(n):
        x = (i + 0.5) * h
        F = _delta(x, p2, m02, m12)
        Fp = F if F > 0 else abs(F) + 1e-30
        acc += 0.5 * F * (1.0 - math.log(Fp / mu2))
    return h * acc


# Deterministic spacelike (finite-real-domain) test points: (p2, m0^2, m1^2).
_TEST_POINTS = (
    (-MZ2, MW2, MZ2),
    (-MW2, MT2, MH2),
    (-MH2, MZ2, MW2),
    (-2.0 * MZ2, MW2, MH2),
    (-MT2, MZ2, MT2),
)

EXPORT_FLAGS: Dict[str, int] = {
    "Export_pv_b1_rank1_twopoint_native": 1,
    "Export_pv_b00_b11_rank2_twopoint": 1,
    "Export_pv_cij_dij_three_four_point": 0,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}

# Sub-gate status of the parent G2F_TENSOR_REDUCTION gate.
G2F_SUBGATE_STATUS = {
    "B1_rank1_twopoint": "CLOSED_NATIVE",
    "B00_B11_rank2_twopoint": "CLOSED_NATIVE",
    "Cij_three_point": "OPEN",
    "Dij_four_point": "OPEN",
    "denner_coefficient_map": "OPEN",
    "counterterm_assembly": "OPEN",
}


# ============================================================================
# Bank-registered checks -- B1 (rank-1)
# ============================================================================

def check_T_w_trace_pv_b1_reduction_matches_direct_P() -> Dict[str, Any]:
    """T: B1 reduction agrees with the independent direct Feynman integral [P]."""
    errs = [abs(b1_reduction(*pt) - b1_direct(*pt)) for pt in _TEST_POINTS]
    mx = max(errs)
    check(mx < 1e-6, f"reduction vs direct max diff {mx:.2e} exceeds 1e-6")
    return _result(
        name="T_w_trace_pv_b1_reduction_matches_direct: "
             "native B1 reduction == direct Feynman integral [P]",
        tier=4, epistemic="P",
        summary=(
            f"The PV reduction B1 = [A0(m0)-A0(m1)-(p^2+m0^2-m1^2)B0]/(2p^2) on the "
            f"banked A0/B0 substrate agrees with the independent direct integral "
            f"int x ln(F/mu^2) dx across {len(_TEST_POINTS)} spacelike points; "
            f"max |diff| = {mx:.2e}."
        ),
        key_result=f"B1 reduction == direct integral (max diff {mx:.1e}). [P]",
        dependencies=["check_T_w_trace_pv_b0_gate_closed", "check_T_w_trace_pv_a0_gate_closed"],
        artifacts={"max_abs_diff": mx, "n_points": len(_TEST_POINTS)},
    )


def check_T_w_trace_pv_b1_argument_swap_identity_P() -> Dict[str, Any]:
    """T: B1(m0,m1) + B1(m1,m0) = -B0(m0,m1) (exact PV identity) [P]."""
    errs = []
    for p2, m02, m12 in _TEST_POINTS:
        lhs = b1_reduction(p2, m02, m12) + b1_reduction(p2, m12, m02)
        rhs = -b0_fin(p2, m02, m12)
        errs.append(abs(lhs - rhs))
    mx = max(errs)
    check(mx < 1e-9, f"argument-swap identity max err {mx:.2e} exceeds 1e-9")
    return _result(
        name="T_w_trace_pv_b1_argument_swap_identity: B1(m0,m1)+B1(m1,m0) = -B0 [P]",
        tier=4, epistemic="P",
        summary=(
            f"The exact PV identity B1(m0,m1)+B1(m1,m0) = -B0 holds to max err "
            f"{mx:.2e} across {len(_TEST_POINTS)} points -- a target-free "
            f"internal-consistency proof of the B1 reduction."
        ),
        key_result=f"B1 argument-swap identity holds (max err {mx:.1e}). [P]",
        dependencies=["check_T_w_trace_pv_b0_symmetry"],
        artifacts={"max_abs_err": mx},
    )


def check_T_w_trace_pv_b1_massless_closed_form_P() -> Dict[str, Any]:
    """T: B1(p^2,0,0) = -1 + 1/2 ln(|p^2|/mu^2) (spacelike) closed form [P]."""
    errs = []
    for p2 in (-MZ2, -MW2, -3.0 * MZ2, -MH2):
        cf = -1.0 + 0.5 * math.log(abs(p2) / MU2)
        errs.append(abs(b1_reduction(p2, 0.0, 0.0) - cf))
    mx = max(errs)
    check(mx < 5e-4, f"massless closed-form max err {mx:.2e} exceeds 5e-4 (B0 quadrature)")
    return _result(
        name="T_w_trace_pv_b1_massless_closed_form: B1(p^2,0,0) = -1 + 1/2 ln(|p^2|/mu^2) [P]",
        tier=4, epistemic="P",
        summary=(
            f"The massless B1 reproduces its analytic closed form to max err "
            f"{mx:.2e}; the residual is the banked B0 midpoint-quadrature error."
        ),
        key_result=f"B1 massless closed form reproduced (max err {mx:.1e}). [P]",
        dependencies=["check_T_w_trace_pv_b0_route_value_reasonable"],
        artifacts={"max_abs_err": mx},
    )


# ============================================================================
# Bank-registered checks -- B00, B11 (rank-2)
# ============================================================================

def check_T_w_trace_pv_b00_b11_trace_relation_P() -> Dict[str, Any]:
    """T: native B00,B11 satisfy the finite metric-trace relation vs banked A0/B0 [P].

    4 B00 + p^2 B11 - (m0^2/2 + m1^2/2 - p^2/6) = A0(m1^2) + m0^2 B0. The LHS uses
    the native direct-integral B00,B11; the RHS uses the banked A0/B0 substrate.
    Validates the rank-2 reduction (incl. the d=4-2eps trace correction in B00)
    against an independent banked quantity. No external target.
    """
    mx = 0.0
    for p2, m02, m12 in _TEST_POINTS:
        lhs = (4.0 * b00_direct(p2, m02, m12) + p2 * b11_direct(p2, m02, m12)
               - (m02 / 2.0 + m12 / 2.0 - p2 / 6.0))
        rhs = a0_fin(m12) + m02 * b0_fin(p2, m02, m12)
        rel = abs(lhs - rhs) / max(1.0, abs(rhs))
        mx = max(mx, rel)
    check(mx < 1e-5, f"trace-relation max rel err {mx:.2e} exceeds 1e-5")
    return _result(
        name="T_w_trace_pv_b00_b11_trace_relation: "
             "4 B00 + p^2 B11 - <Delta> = A0(m1^2) + m0^2 B0 [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native rank-2 coefficients B00, B11 satisfy the finite "
            f"d=4-2eps metric-trace relation against the banked A0/B0 substrate to "
            f"max relative err {mx:.2e} across {len(_TEST_POINTS)} spacelike points. "
            f"This ties B00 (incl. its trace finite correction) and B11 to an "
            f"independent banked quantity -- a target-free validation."
        ),
        key_result=f"B00/B11 trace relation holds vs banked A0/B0 (rel err {mx:.1e}). [P]",
        dependencies=["check_T_w_trace_pv_a0_gate_closed", "check_T_w_trace_pv_b0_gate_closed"],
        artifacts={"max_rel_err": mx, "n_points": len(_TEST_POINTS)},
    )


def check_T_w_trace_pv_b11_massless_closed_form_P() -> Dict[str, Any]:
    """T: B11(p^2,0,0) = -1/3 ln(|p^2|/mu^2) + 13/18 (spacelike) [P]."""
    errs = []
    for p2 in (-MZ2, -MW2, -3.0 * MZ2, -MH2):
        cf = -(1.0 / 3.0) * math.log(abs(p2) / MU2) + 13.0 / 18.0
        errs.append(abs(b11_direct(p2, 0.0, 0.0) - cf))
    mx = max(errs)
    check(mx < 5e-4, f"B11 massless closed-form max err {mx:.2e} exceeds 5e-4")
    return _result(
        name="T_w_trace_pv_b11_massless_closed_form: B11(p^2,0,0) = -1/3 ln(|p^2|/mu^2) + 13/18 [P]",
        tier=4, epistemic="P",
        summary=(
            f"The massless B11 reproduces its analytic closed form "
            f"-1/3 ln(|p^2|/mu^2) + 13/18 to max err {mx:.2e} (quadrature residual)."
        ),
        key_result=f"B11 massless closed form reproduced (max err {mx:.1e}). [P]",
        dependencies=["check_T_w_trace_pv_b00_b11_trace_relation"],
        artifacts={"max_abs_err": mx},
    )


def check_T_w_trace_pv_b00_massless_closed_form_P() -> Dict[str, Any]:
    """T: B00(p^2,0,0) = |p^2| (2/9 - ln(|p^2|/mu^2)/12) (spacelike) [P]."""
    mx = 0.0
    for p2 in (-MZ2, -MW2, -3.0 * MZ2, -MH2):
        a = abs(p2)
        cf = a * (2.0 / 9.0 - math.log(a / MU2) / 12.0)
        mx = max(mx, abs(b00_direct(p2, 0.0, 0.0) - cf) / max(1.0, abs(cf)))
    check(mx < 1e-4, f"B00 massless closed-form max rel err {mx:.2e} exceeds 1e-4")
    return _result(
        name="T_w_trace_pv_b00_massless_closed_form: B00(p^2,0,0) = |p^2|(2/9 - ln(|p^2|/mu^2)/12) [P]",
        tier=4, epistemic="P",
        summary=(
            f"The massless B00 reproduces its analytic closed form "
            f"|p^2|(2/9 - ln(|p^2|/mu^2)/12) to max relative err {mx:.2e} -- an "
            f"independent confirmation of the d=4-2eps trace finite correction."
        ),
        key_result=f"B00 massless closed form reproduced (rel err {mx:.1e}). [P]",
        dependencies=["check_T_w_trace_pv_b00_b11_trace_relation"],
        artifacts={"max_rel_err": mx},
    )


def check_T_w_trace_pv_twopoint_tensor_subgate_partial_P() -> Dict[str, Any]:
    """T: two-point tensors (B1,B00,B11) native; 3-/4-point + map + assembly OPEN [P_structural]."""
    check(G2F_SUBGATE_STATUS["B1_rank1_twopoint"] == "CLOSED_NATIVE",
          "B1 rank-1 two-point must be CLOSED_NATIVE")
    check(G2F_SUBGATE_STATUS["B00_B11_rank2_twopoint"] == "CLOSED_NATIVE",
          "B00/B11 rank-2 two-point must be CLOSED_NATIVE")
    for k in ("Cij_three_point", "Dij_four_point", "denner_coefficient_map", "counterterm_assembly"):
        check(G2F_SUBGATE_STATUS[k] == "OPEN", f"{k} must remain OPEN")
    check(EXPORT_FLAGS["Export_pv_b00_b11_rank2_twopoint"] == 1, "B00/B11 native flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no Delta r_rem evaluated by these rungs")
    return _result(
        name="T_w_trace_pv_twopoint_tensor_subgate_partial: "
             "two-point tensors native; 3-/4-point + map + assembly OPEN [P_structural]",
        tier=4, epistemic="P_structural_partial",
        summary=(
            "The OPEN G2F_TENSOR_REDUCTION gate now has its complete TWO-POINT "
            "tensor basis (B1, B00, B11) APF-owned and self-validated. The 3-point "
            "Cij, 4-point Dij, the Denner coefficient map, and the counterterm "
            "assembly remain OPEN. No Delta r_rem / DeltaRhobarW / M_W value is "
            "produced; DIZET stays the publishable OS-W closure. Native route, "
            "parallel to the sibling reviewed-formula harness."
        ),
        key_result="G2F two-point tensor basis (B1,B00,B11) native; 3-/4-point OPEN. [P_structural]",
        dependencies=["T_w_trace_pv_b1_reduction_matches_direct",
                      "T_w_trace_pv_b00_b11_trace_relation"],
        cross_refs=["check_T_w_trace_pv_tensor_reduction_gate_open"],
        artifacts={"g2f_subgate_status": dict(G2F_SUBGATE_STATUS),
                   "export_flags": dict(EXPORT_FLAGS)},
    )


# ============================================================================
# Registration
# ============================================================================

_CHECKS = {
    "T_w_trace_pv_b1_reduction_matches_direct": check_T_w_trace_pv_b1_reduction_matches_direct_P,
    "T_w_trace_pv_b1_argument_swap_identity": check_T_w_trace_pv_b1_argument_swap_identity_P,
    "T_w_trace_pv_b1_massless_closed_form": check_T_w_trace_pv_b1_massless_closed_form_P,
    "T_w_trace_pv_b00_b11_trace_relation": check_T_w_trace_pv_b00_b11_trace_relation_P,
    "T_w_trace_pv_b11_massless_closed_form": check_T_w_trace_pv_b11_massless_closed_form_P,
    "T_w_trace_pv_b00_massless_closed_form": check_T_w_trace_pv_b00_massless_closed_form_P,
    "T_w_trace_pv_twopoint_tensor_subgate_partial": check_T_w_trace_pv_twopoint_tensor_subgate_partial_P,
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
