"""APF-native OS-renormalized transverse self-energy Sigma_hat -- Tier-4.

Step 2 of the native OS-W precision close. The bare finite Re Sigma_VV(p^2) at a
fixed scale mu^2 carries an un-subtracted wave-function running (mu-dependent)
that only cancels with the OS counterterms -- the defect that spoiled the
term-by-term precision attempt (~1.3 GeV M_W miss). This rung builds the
twice-subtracted OS-renormalized self-energy and proves it mu-independent.

A(p^2; mu^2) is the v24.3.83 slot-by-slot transverse bracket
    A = -(N_c/16 pi^2){4(gL^2+gR^2)B00 - 2(gL^2+gR^2)[A0(m2^2)+m1^2 B0+p^2 B1]
                       + 4 gL gR m1 m2 B0}
evaluated with the timelike / massless-safe B-functions (valid at p^2=M^2). The
OS-renormalized self-energy subtracts mass+wavefn counterterms:
    Sigma_hat(p^2) = A(p^2) - A(M^2) - (p^2-M^2) A'(M^2)
so Sigma_hat(M^2)=Sigma_hat'(M^2)=0 by construction.

mu-independence (load-bearing): the running is affine in p^2
    dA/dln mu^2 = -(N_c/16 pi^2){(gL^2+gR^2)[2p^2/3-(m1^2+m2^2)] + 4 gL gR m1 m2}
                = alpha + beta p^2,
and a twice-subtracted quantity kills any affine function exactly. This is the
renormalized counterpart of the banked "self-energy poles linear in p^2"
(v24.3.91): the same affine structure that makes the UV pole removable by an OS
counterterm makes the finite self-energy scale-free.

Validated (no external target): OS conditions to FD precision; mu-independence at
the float floor (~5e-8) vs bare shift ~1e-3 (>1e4 suppression); the bare mu-shift
equals the analytic affine pole P(p^2) ln 4 to ~1e-10.

Scope: the mu-independent OS-renormalized self-energy function per fermion loop.
OPEN toward Delta r_rem / M_W: the full SM fermion+boson sum into
Re Pi_WW(M_W^2)/Re Pi_ZZ(M_Z^2), bosonic/Goldstone/ghost loops, vertex+box
delta_VB, GFloop resummation. No Delta r_rem / M_W; DIZET stays publishable.
"""
from __future__ import annotations

import math
from typing import Any, Dict, Tuple

from apf.apf_utils import check, _result
from apf.w_trace_pv_scalar_integral_substrate import a0_fin, MU2
from apf.w_trace_pv_timelike_two_point import re_b00_timelike, re_b1_timelike
from apf.w_trace_native_pv_massless_safe import re_b0_safe

_SIN2_W = 3.0 / 13.0
_C = math.sqrt(1.0 - _SIN2_W)
_ALPHA_EM = 1.0 / 128.21
_E2 = 4.0 * math.pi * _ALPHA_EM
_G = math.sqrt(_E2 / _SIN2_W)
_M_T = 163.0
_M_Z = 91.1876
_M_W = _M_Z * _C
_N_C = 3.0
_PREF = _N_C / (16.0 * math.pi ** 2)
_NQ = 40000


def A_transverse_mu(gL: float, gR: float, m1: float, m2: float,
                    p2: float, mu2: float = MU2) -> float:
    """Native transverse self-energy coefficient A(p^2; mu^2) (real part)."""
    m12 = m1 * m1
    m22 = m2 * m2
    gg = gL * gL + gR * gR
    B0 = re_b0_safe(p2, m12, m22, mu2)
    B00 = re_b00_timelike(p2, m12, m22, mu2, _NQ)
    B1 = re_b1_timelike(p2, m12, m22, mu2, _NQ)
    A0 = a0_fin(m22, mu2)
    bracket = (4.0 * gg * B00
               - 2.0 * gg * (A0 + m12 * B0 + p2 * B1)
               + 4.0 * gL * gR * m1 * m2 * B0)
    return -_PREF * bracket


def _A_prime(gL, gR, m1, m2, M2, mu2, h=1.0):
    """Central finite-difference dA/dp^2 at p^2 = M2."""
    return (A_transverse_mu(gL, gR, m1, m2, M2 + h, mu2)
            - A_transverse_mu(gL, gR, m1, m2, M2 - h, mu2)) / (2.0 * h)


def sigma_hat(gL, gR, m1, m2, p2, M2, mu2=MU2, h=1.0) -> float:
    """OS-renormalized self-energy: A(p2) - A(M2) - (p2-M2) A'(M2)."""
    A_p = A_transverse_mu(gL, gR, m1, m2, p2, mu2)
    A_M = A_transverse_mu(gL, gR, m1, m2, M2, mu2)
    Ap_M = _A_prime(gL, gR, m1, m2, M2, mu2, h)
    return A_p - A_M - (p2 - M2) * Ap_M


def _pole_affine(gL, gR, m1, m2, p2) -> float:
    """Analytic mu-running dA/dln mu^2 = P(p^2) (affine in p^2)."""
    m12, m22 = m1 * m1, m2 * m2
    gg = gL * gL + gR * gR
    return -_PREF * (gg * (2.0 * p2 / 3.0 - (m12 + m22)) + 4.0 * gL * gR * m1 * m2)


def _gLZ(T3, Q):
    return (_G / _C) * (T3 - Q * _SIN2_W)


def _gRZ(Q):
    return (_G / _C) * (-Q * _SIN2_W)


# (label, gL, gR, m1, m2, M2) -- all massive (no scaleless A0)
_CONFIGS: Tuple = (
    ("W(t,b)", _G / math.sqrt(2.0), 0.0, _M_T, 4.18, _M_W ** 2),
    ("W(c,s)", _G / math.sqrt(2.0), 0.0, 1.27, 0.10, _M_W ** 2),
    ("Z(t,t)", _gLZ(0.5, 2.0 / 3.0), _gRZ(2.0 / 3.0), _M_T, _M_T, _M_Z ** 2),
)

EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_os_renormalized_self_energy_mu_independent": 1,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


# ===========================================================================
# checks
# ===========================================================================
def check_T_w_trace_native_os_renorm_os_conditions_P() -> Dict[str, Any]:
    """T: OS-renormalized Sigma_hat satisfies Sigma_hat(M^2)=0, Sigma_hat'(M^2)=0 [P]."""
    mx_val = 0.0
    mx_der = 0.0
    h = 1.0
    for label, gL, gR, m1, m2, M2 in _CONFIGS:
        mx_val = max(mx_val, abs(sigma_hat(gL, gR, m1, m2, M2, M2, MU2, h)))
        der = (sigma_hat(gL, gR, m1, m2, M2 + h, M2, MU2, h)
               - sigma_hat(gL, gR, m1, m2, M2 - h, M2, MU2, h)) / (2.0 * h)
        mx_der = max(mx_der, abs(der))
    check(mx_val < 1e-10, f"Sigma_hat(M^2) must vanish, max {mx_val:.2e}")
    check(mx_der < 1e-8, f"Sigma_hat'(M^2) must vanish, max {mx_der:.2e}")
    return _result(
        name="T_w_trace_native_os_renorm_os_conditions: "
             "OS-renormalized Sigma_hat satisfies the on-shell conditions [P]",
        tier=4, epistemic="P",
        summary=(
            f"The twice-subtracted Sigma_hat(p^2)=A(p^2)-A(M^2)-(p^2-M^2)A'(M^2) "
            f"satisfies the OS conditions Sigma_hat(M^2)=0 (max {mx_val:.1e}) and "
            f"Sigma_hat'(M^2)=0 (max {mx_der:.1e}) for the W(t,b), W(c,s) and Z(t,t) "
            f"fermion loops -- the renormalized self-energy entering the OS Delta r, "
            f"by construction free of the bare wave-function running."
        ),
        key_result=f"Sigma_hat(M^2)=0 ({mx_val:.0e}), Sigma_hat'(M^2)=0 ({mx_der:.0e}). [P]",
        dependencies=["T_w_trace_native_drho_slot_by_slot",
                      "T_w_trace_native_pv_massless_safe_overlap"],
        artifacts={"max_value": mx_val, "max_derivative": mx_der},
    )


def check_T_w_trace_native_os_renorm_mu_independence_P() -> Dict[str, Any]:
    """T: OS-renormalized Sigma_hat is mu-independent while bare A is not [P]."""
    mx_hat = 0.0
    min_bare_shift = 1e30
    mu2a = MU2
    mu2b = 4.0 * MU2
    for label, gL, gR, m1, m2, M2 in _CONFIGS:
        for p2 in (-M2, 0.25 * M2, 2.0 * M2, -3.0 * M2):
            s_a = sigma_hat(gL, gR, m1, m2, p2, M2, mu2a)
            s_b = sigma_hat(gL, gR, m1, m2, p2, M2, mu2b)
            mx_hat = max(mx_hat, abs(s_a - s_b))
            ba = A_transverse_mu(gL, gR, m1, m2, p2, mu2a) / M2
            bb = A_transverse_mu(gL, gR, m1, m2, p2, mu2b) / M2
            min_bare_shift = min(min_bare_shift, abs(ba - bb))
    check(mx_hat < 1e-6, f"Sigma_hat mu-dependence must vanish, max {mx_hat:.2e}")
    check(min_bare_shift > 1e-5, f"bare A/M^2 must be mu-dependent, min {min_bare_shift:.2e}")
    supp = min_bare_shift / max(mx_hat, 1e-30)
    check(supp > 1e3, f"renormalization must suppress mu-dependence by >1e3, got {supp:.1e}")
    return _result(
        name="T_w_trace_native_os_renorm_mu_independence: "
             "OS-renormalized Sigma_hat is mu-independent; bare self-energy is not [P]",
        tier=4, epistemic="P",
        summary=(
            f"Under mu^2 -> 4 mu^2 the OS-renormalized Sigma_hat(p^2) is invariant to "
            f"{mx_hat:.1e} (float floor of the twice-subtraction) across spacelike and "
            f"timelike p^2 for all three loops, whereas the bare ratio Re A(p^2)/M^2 "
            f"-- whose un-subtracted scale dependence spoiled the term-by-term "
            f"precision attempt -- shifts by at least {min_bare_shift:.1e}: a "
            f"{supp:.0e}x suppression. The twice subtraction removes the affine-in-p^2 "
            f"running exactly. Native, no external input."
        ),
        key_result=f"Sigma_hat mu-invariant ({mx_hat:.0e}) vs bare shift >= {min_bare_shift:.0e} ({supp:.0e}x). [P]",
        dependencies=["T_w_trace_native_os_renorm_os_conditions"],
        artifacts={"sigma_hat_mu_residual": mx_hat, "min_bare_mu_shift": min_bare_shift,
                   "suppression_factor": supp},
    )


def check_T_w_trace_native_os_renorm_running_matches_pole_P() -> Dict[str, Any]:
    """T: the bare mu-running equals the analytic affine pole P(p^2) ln 4 [P]."""
    mx = 0.0
    ln4 = math.log(4.0)
    for label, gL, gR, m1, m2, M2 in _CONFIGS:
        for p2 in (-M2, 0.5 * M2, 2.0 * M2):
            shift = (A_transverse_mu(gL, gR, m1, m2, p2, 4.0 * MU2)
                     - A_transverse_mu(gL, gR, m1, m2, p2, MU2))
            pred = _pole_affine(gL, gR, m1, m2, p2) * ln4
            mx = max(mx, abs(shift - pred) / max(1e-6, abs(pred)))
    check(mx < 1e-6, f"bare mu-running vs analytic affine pole max rel err {mx:.2e}")
    return _result(
        name="T_w_trace_native_os_renorm_running_matches_pole: "
             "bare mu-running equals the analytic affine pole P(p^2) ln 4 [P]",
        tier=4, epistemic="P",
        summary=(
            f"The bare self-energy mu-shift A(p^2;4 mu^2)-A(p^2;mu^2) reproduces the "
            f"analytic affine running P(p^2) ln 4, P(p^2)=-(N_c/16 pi^2)"
            f"[(gL^2+gR^2)(2 p^2/3-m1^2-m2^2)+4 gL gR m1 m2], to max rel err {mx:.1e}. "
            f"The running is affine in p^2 -- the same linear-pole structure that "
            f"makes the UV divergence OS-removable (v24.3.91) -- which is exactly why "
            f"the twice-subtracted Sigma_hat is mu-independent."
        ),
        key_result=f"bare mu-running == affine pole P(p^2) ln 4 (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_native_os_renorm_mu_independence",
                      "T_w_trace_native_uv_cancel_poles_linear"],
        artifacts={"max_rel_err": mx},
    )


def check_T_w_trace_native_os_renorm_scope_partial_P() -> Dict[str, Any]:
    """T: mu-independent OS-renormalized self-energy done; Delta r_rem assembly OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_native_os_renormalized_self_energy_mu_independent"] == 1,
          "OS-renormalized flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no Delta r_rem evaluated by this rung")
    return _result(
        name="T_w_trace_native_os_renorm_scope_partial: "
             "mu-independent OS-renormalized self-energy done; Delta r_rem assembly OPEN [P_structural]",
        tier=4, epistemic="P_structural",
        summary=(
            "The OS-renormalized transverse self-energy Sigma_hat(p^2) is native and "
            "proven mu-independent (per fermion loop), OS conditions "
            "Sigma_hat(M^2)=Sigma_hat'(M^2)=0 built in -- closing the bare "
            "term-by-term scale-dependence that spoiled the precision attempt. OPEN "
            "toward Delta r_rem: the full SM fermion+boson sum into "
            "Re Pi_WW(M_W^2)/Re Pi_ZZ(M_Z^2), bosonic/Goldstone/ghost loops, "
            "vertex+box delta_VB, GFloop resummation. No Delta r_rem / M_W; DIZET "
            "stays the publishable OS-W closure."
        ),
        key_result="mu-independent OS-renormalized Sigma_hat done; Delta r_rem assembly OPEN. [P_structural]",
        dependencies=["T_w_trace_native_os_renorm_running_matches_pole"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_native_os_renorm_os_conditions": check_T_w_trace_native_os_renorm_os_conditions_P,
    "T_w_trace_native_os_renorm_mu_independence": check_T_w_trace_native_os_renorm_mu_independence_P,
    "T_w_trace_native_os_renorm_running_matches_pole": check_T_w_trace_native_os_renorm_running_matches_pole_P,
    "T_w_trace_native_os_renorm_scope_partial": check_T_w_trace_native_os_renorm_scope_partial_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == "__main__":
    import json
    print(json.dumps({k: {"passed": v["passed"], "epistemic": v["epistemic"]}
                      for k, v in run_all().items()}, indent=2))
