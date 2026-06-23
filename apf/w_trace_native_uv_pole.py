"""APF-native UV-pole (Delta_eps) bookkeeping layer for the PV toolkit -- Tier-4.

Prerequisite B of the native OS-W one-loop evaluator (work plan 2026-05-24,
Stage 4). The native PV functions in ``apf.w_trace_pv_scalar_integral_substrate``
and ``apf.w_trace_pv_tensor_reduction`` return the FINITE parts of the
Passarino-Veltman integrals in a declared scheme. Each bare integral also carries
a 1/epsilon ultraviolet pole,

    X(...) = X_pole * Delta_eps + X_fin(...; mu^2) ,   Delta_eps = 1/eps_bar (MSbar),

whose coefficient X_pole must be tracked so that UV finiteness of the assembled,
renormalized Delta r is an explicit, checkable property (the poles cancel against
the banked counterterms). This module supplies the exact pole coefficients and
validates them three ways, with no external input.

Pole coefficients (exact)
-------------------------
    A0(m^2)            -> m^2
    B0(p^2,m0^2,m1^2)  -> 1
    B1(p^2,m0^2,m1^2)  -> -1/2
    B11(p^2,m0^2,m1^2) -> 1/3
    B00(p^2,m0^2,m1^2) -> (m0^2 + m1^2)/4 - p^2/12

Validation (no external target)
-------------------------------
1. Pole == mu-running slope. Each pole coefficient equals the renormalization-
   scale slope d X_fin / d ln(mu^2) of the corresponding banked finite function
   (since X = X_pole*Delta_eps - X_pole*ln(p^2/mu^2) + ..., the mu-running of the
   finite part exposes the same coefficient). Checked by finite difference of the
   banked a0_fin and the native re_b*_timelike at a spacelike point -- ties the
   pole layer to the already-banked finite toolkit.
2. Pole-level trace relation. The exact rank-2 metric-trace relation
   4 B00 + p^2 B11 - (m0^2/2 + m1^2/2 - p^2/6) = A0(m1^2) + m0^2 B0, taken at the
   pole level (the finite constant drops), reads 4 B00_pole + p^2 B11_pole =
   A0_pole(m1^2) + m0^2 B0_pole and holds identically -- mutual consistency of
   the coefficients.
3. QED beta-function. The assembled fermion-loop photon-VP pole reproduces the
   one-loop QED beta-function coefficient: the form-factor pole is
   -(e^2/12pi^2) * sum_f N_c Q^2, with sum_f N_c Q^2 = 8 over the three SM
   generations, and the bare photon bracket pole is purely transverse
   (~ p^2, mass-independent) -- the Ward identity at the divergent level. This
   is the pole half of the same photon VP whose finite part reproduces
   Delta alpha_lep (apf.w_trace_native_timelike_self_energy).

Honest scope
------------
This establishes Prerequisite B (the UV-pole layer) and validates it on the
fermionic photon VP. The full Stage-4 UV-cancellation gate (bosonic/Goldstone/
ghost loop poles cancelling against the banked counterterms) requires the Stage-3
bosonic loops and remains OPEN. No Delta r_rem / M_W is produced; DIZET stays the
publishable OS-W closure.

Status
------
- Export_native_uv_pole_layer                   = 1
- Export_OSW_APF_internal_delta_r_rem_evaluated  = 0   (OPEN, unchanged)
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple

from apf.apf_utils import check, _result
from apf.w_trace_pv_scalar_integral_substrate import a0_fin, MU2
from apf.w_trace_pv_timelike_two_point import (
    re_b0_timelike, re_b1_timelike, re_b11_timelike, re_b00_timelike,
)

# APF-internal input (same alpha(0) as the photon-VP finite part).
_ALPHA_0 = 1.0 / 137.035999084
_E2 = 4.0 * math.pi * _ALPHA_0


# ===========================================================================
# Exact UV-pole coefficients (coefficient of Delta_eps = 1/eps_bar)
# ===========================================================================
def a0_pole(m2: float) -> float:
    return m2


def b0_pole(p2: float, m02: float, m12: float) -> float:
    return 1.0


def b1_pole(p2: float, m02: float, m12: float) -> float:
    return -0.5


def b11_pole(p2: float, m02: float, m12: float) -> float:
    return 1.0 / 3.0


def b00_pole(p2: float, m02: float, m12: float) -> float:
    return (m02 + m12) / 4.0 - p2 / 12.0


def photon_vp_bracket_pole(Q: float, m: float, p2: float) -> float:
    """Pole coefficient of the equal-mass photon transverse bracket (g_L=g_R=eQ).

    Same algebraic bracket as the finite photon VP
    (apf.w_trace_native_timelike_self_energy), with the pole coefficients in
    place of the finite B-functions. Equals (4/3) e^2 Q^2 p^2 (transverse).
    """
    g2 = _E2 * Q * Q
    gg = 2.0 * g2
    m2 = m * m
    return (4.0 * gg * b00_pole(p2, m2, m2)
            - 2.0 * gg * (a0_pole(m2) + m2 * b0_pole(p2, m2, m2) + p2 * b1_pole(p2, m2, m2))
            + 4.0 * g2 * m2 * b0_pole(p2, m2, m2))


# SM fermion content: (Q, N_c), three generations.
SM_FERMIONS: List[Tuple[float, float]] = (
    [(-1.0, 1.0)] * 3            # charged leptons
    + [(2.0 / 3.0, 3.0)] * 3     # up-type quarks
    + [(-1.0 / 3.0, 3.0)] * 3    # down-type quarks
    + [(0.0, 1.0)] * 3           # neutrinos
)


def sum_Nc_Q2() -> float:
    return sum(Nc * Q * Q for Q, Nc in SM_FERMIONS)


def photon_vp_pole_coeff(p2: float = -500.0, m: float = 5.0) -> float:
    """Assembled fermionic photon-VP form-factor pole coefficient
    (= sum_f -(N_c/16pi^2) * bracket_pole/p^2). Mass-independent."""
    return sum(-(Nc / (16.0 * math.pi ** 2)) * photon_vp_bracket_pole(Q, m, p2) / p2
               for Q, Nc in SM_FERMIONS)


EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_uv_pole_layer": 1,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


# ===========================================================================
# checks
# ===========================================================================
def check_T_w_trace_native_uv_pole_coeffs_match_mu_running_P() -> Dict[str, Any]:
    """T: UV-pole coefficients equal the mu-running slopes of the finite functions [P]."""
    p2, m02, m12 = -1234.0, 25.0, 81.0
    n = 6000
    # slope d f / d ln(mu^2): step ln(mu^2) by 1 (mu^2 -> e*mu^2)
    def slope(fn):
        return fn(MU2 * math.e) - fn(MU2)
    pairs = {
        "A0": (slope(lambda mu2: a0_fin(m12, mu2)), a0_pole(m12)),
        "B0": (slope(lambda mu2: re_b0_timelike(p2, m02, m12, mu2=mu2, n=n)), b0_pole(p2, m02, m12)),
        "B1": (slope(lambda mu2: re_b1_timelike(p2, m02, m12, mu2=mu2, n=n)), b1_pole(p2, m02, m12)),
        "B11": (slope(lambda mu2: re_b11_timelike(p2, m02, m12, mu2=mu2, n=n)), b11_pole(p2, m02, m12)),
        "B00": (slope(lambda mu2: re_b00_timelike(p2, m02, m12, mu2=mu2, n=n)), b00_pole(p2, m02, m12)),
    }
    mx = 0.0
    for k, (sl, pole) in pairs.items():
        rel = abs(sl - pole) / max(1.0, abs(pole))
        mx = max(mx, rel)
        check(rel < 1e-3, f"{k}: mu-slope {sl:.6f} vs pole {pole:.6f} rel {rel:.2e}")
    return _result(
        name="T_w_trace_native_uv_pole_coeffs_match_mu_running: "
             "UV-pole coefficients equal the mu-running slopes of the finite functions [P]",
        tier=4, epistemic="P",
        summary=(
            f"The exact UV-pole coefficients A0->m^2, B0->1, B1->-1/2, B11->1/3, "
            f"B00->(m0^2+m1^2)/4 - p^2/12 each equal the renormalization-scale "
            f"slope d X_fin/d ln(mu^2) of the corresponding banked finite function "
            f"(a0_fin + native re_b*_timelike), to max rel {mx:.1e} by finite "
            f"difference. This ties the new pole layer to the already-banked finite "
            f"toolkit: the divergent coefficient and the mu-running of the finite "
            f"part are the same number, as they must be."
        ),
        key_result=f"pole coeffs == mu-running slopes of finite PV functions (max rel {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_b00_b11_trace_relation",
                      "T_w_trace_pv_timelike_spacelike_overlap"],
        artifacts={k: {"mu_slope": sl, "pole": pole} for k, (sl, pole) in pairs.items()},
    )


def check_T_w_trace_native_uv_pole_trace_relation_P() -> Dict[str, Any]:
    """T: the rank-2 trace relation holds at the pole level [P]."""
    mx = 0.0
    for p2, m02, m12 in [(-1234.0, 25.0, 81.0), (500.0, 9.0, 9.0), (-9999.0, 0.0, 144.0)]:
        lhs = 4.0 * b00_pole(p2, m02, m12) + p2 * b11_pole(p2, m02, m12)
        rhs = a0_pole(m12) + m02 * b0_pole(p2, m02, m12)
        mx = max(mx, abs(lhs - rhs))
    check(mx < 1e-9, f"pole-level trace relation max |LHS-RHS| {mx:.2e}")
    return _result(
        name="T_w_trace_native_uv_pole_trace_relation: "
             "rank-2 metric-trace relation holds at the pole level [P]",
        tier=4, epistemic="P",
        summary=(
            f"At the pole level the finite constant in the rank-2 trace relation "
            f"drops and it reads 4 B00_pole + p^2 B11_pole = A0_pole(m1^2) + "
            f"m0^2 B0_pole, which holds identically (max |LHS-RHS| {mx:.1e}) over "
            f"spacelike and timelike test points -- the pole coefficients of "
            f"B00/B11 are mutually consistent with those of A0/B0."
        ),
        key_result=f"pole-level rank-2 trace relation holds (max abs {mx:.1e}). [P]",
        dependencies=["T_w_trace_native_uv_pole_coeffs_match_mu_running"],
        artifacts={"max_abs_err": mx},
    )


def check_T_w_trace_native_photon_vp_pole_beta_function_P() -> Dict[str, Any]:
    """T: fermionic photon-VP pole = QED beta-function (sum N_c Q^2 = 8), transverse [P]."""
    # (a) pole-level transversality: bracket_pole/p^2 constant + mass-independent
    spread = 0.0
    ref = photon_vp_bracket_pole(1.0, 5.0, -100.0) / (-100.0)
    for m in (0.1, 5.0, 173.0):
        for p2 in (-10.0, 500.0, -2000.0):
            v = photon_vp_bracket_pole(1.0, m, p2) / p2
            spread = max(spread, abs(v - ref) / abs(ref))
    check(spread < 1e-9, f"photon bracket pole/p^2 not constant (transversality) spread {spread:.2e}")
    check(abs(ref - (4.0 / 3.0) * _E2) / ((4.0 / 3.0) * _E2) < 1e-12,
          "photon bracket pole/p^2 must equal (4/3)e^2")
    # (b) beta-function coefficient
    s = sum_Nc_Q2()
    check(abs(s - 8.0) < 1e-12, f"sum N_c Q^2 over 3 generations must be 8, got {s}")
    native = photon_vp_pole_coeff()
    analytic = -(_E2 / (12.0 * math.pi ** 2)) * s
    rel = abs(native - analytic) / abs(analytic)
    check(rel < 1e-10, f"native VP pole {native:.8e} vs beta-function {analytic:.8e} rel {rel:.2e}")
    return _result(
        name="T_w_trace_native_photon_vp_pole_beta_function: "
             "fermionic photon-VP pole reproduces the QED beta-function (sum N_c Q^2 = 8) [P]",
        tier=4, epistemic="P",
        summary=(
            f"The bare fermion-loop photon-VP bracket pole is purely transverse "
            f"(bracket_pole/p^2 = (4/3)e^2, constant and mass-independent to "
            f"{spread:.0e}) -- the Ward identity at the divergent level. The "
            f"assembled form-factor pole sum_f -(N_c/16pi^2) bracket_pole/p^2 = "
            f"-(e^2/12pi^2) sum_f N_c Q^2 with sum_f N_c Q^2 = {s:.0f} over the "
            f"three SM generations (3 leptons + up 4/3 + down 1/3 per generation), "
            f"reproducing the exact one-loop QED beta-function coefficient to rel "
            f"{rel:.0e}. This is the pole half of the same photon VP whose finite "
            f"part reproduces Delta alpha_lep; no external input."
        ),
        key_result=f"fermionic photon-VP pole = -(e^2/12pi^2) * sum N_c Q^2, sum = {s:.0f} (rel {rel:.0e}). [P]",
        dependencies=["T_w_trace_native_uv_pole_trace_relation",
                      "T_w_trace_native_delta_alpha_lep_timelike"],
        artifacts={"sum_Nc_Q2": s, "native_pole": native, "analytic_beta": analytic,
                   "transversality_spread": spread},
    )


def check_T_w_trace_native_uv_pole_scope_partial_P() -> Dict[str, Any]:
    """T: UV-pole layer (Prereq B) done; bosonic poles + counterterm cancellation OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_native_uv_pole_layer"] == 1, "UV-pole layer flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no APF-internal Delta r_rem evaluated by this rung")
    return _result(
        name="T_w_trace_native_uv_pole_scope_partial: "
             "UV-pole layer (Prereq B) established; bosonic poles + counterterm cancellation OPEN [P_structural]",
        tier=4, epistemic="P_structural_partial",
        summary=(
            "Prerequisite B of the native OS-W evaluator is in place: the PV toolkit "
            "now carries exact UV-pole coefficients (A0/B0/B1/B11/B00), validated "
            "against the mu-running of the banked finite functions, against the "
            "pole-level trace relation, and against the one-loop QED beta-function "
            "via the fermionic photon VP. Still OPEN toward the APF-internal "
            "Delta r_rem: the Stage-3 bosonic/Goldstone/ghost loops (whose poles this "
            "layer will track), and the Stage-4 UV-cancellation gate proving the "
            "assembled renormalized Delta r is pole-free against the banked "
            "counterterms. No Delta r_rem / M_W is produced; DIZET stays the "
            "publishable OS-W closure."
        ),
        key_result="UV-pole layer (Prereq B) done; bosonic poles + counterterm cancellation OPEN. [P_structural]",
        dependencies=["T_w_trace_native_photon_vp_pole_beta_function"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_native_uv_pole_coeffs_match_mu_running": check_T_w_trace_native_uv_pole_coeffs_match_mu_running_P,
    "T_w_trace_native_uv_pole_trace_relation": check_T_w_trace_native_uv_pole_trace_relation_P,
    "T_w_trace_native_photon_vp_pole_beta_function": check_T_w_trace_native_photon_vp_pole_beta_function_P,
    "T_w_trace_native_uv_pole_scope_partial": check_T_w_trace_native_uv_pole_scope_partial_P,
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
