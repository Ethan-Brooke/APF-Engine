"""APF-native EWWGR §6 Zff / γff proper-vertex 3-pt form factors -- Tier-4.

R1b of the OS-W Gate A "native kappa_l" arc. Thin layer on R1's BHM
Lambda_2(s, M^2) and Lambda_3(s, M^2) (apf.w_trace_pv_lambda_bhm_vertex,
v24.3.106), assembling the Zff and γff vertex form factors per the LEP
Yellow Report "Precision Calculations for the Z Resonance" (CERN 95-03 =
arXiv:hep-ph/9709229, EWWGR.tex L6005-6055, equations vertex / zvertex /
emvertex):

    Neutral-current vertex (charged fermion):
        F_V^Zf(s) = (α/4π) [ v_f (v_f^2 + 3 a_f^2) / (4 s_W^2 c_W^2)
                              * Lambda_2(s, M_Z^2)  +  F_L^f(s) ]
        F_A^Zf(s) = (α/4π) [ a_f (3 v_f^2 + a_f^2) / (4 s_W^2 c_W^2)
                              * Lambda_2(s, M_Z^2)  +  F_L^f(s) ]
        v_f = I_3^f - 2 Q_f s_W^2 ,  a_f = I_3^f

    Neutrino vertex (F_V^Zν = F_A^Zν):
        F^Zν(s) = (α/4π) [ 1/(8 c_W^2 s_W^2) Lambda_2(s, M_Z^2)
                          + (2 s_W^2 - 1)/(4 s_W^2) Lambda_2(s, M_W^2)
                          + 3 c_W^2/(2 s_W^2) Lambda_3(s, M_W^2) ]

    Channel-specific F_L^f:
        F_L^ell = (1/4s_W^2) Lambda_2(M_W) - (3 c_W^2/2 s_W^2) Lambda_3(M_W)
        F_L^u   = -(1 - 2 s_W^2/3)/(4 s_W^2) Lambda_2(M_W)
                  + (3 c_W^2/2 s_W^2) Lambda_3(M_W)
        F_L^d   =  (1 - 4 s_W^2/3)/(4 s_W^2) Lambda_2(M_W)
                  - (3 c_W^2/2 s_W^2) Lambda_3(M_W)

    Electromagnetic vertex (charged fermion):
        F_V^γf(s) = (α/4π) [ Q_f (v_f^2 + a_f^2)/(4 s_W^2 c_W^2)
                              * Lambda_2(s, M_Z^2)  +  G_L^f(s) ]
        F_A^γf(s) = (α/4π) [ Q_f 2 v_f a_f / (4 s_W^2 c_W^2)
                              * Lambda_2(s, M_Z^2)  +  G_L^f(s) ]

    Channel-specific G_L^f:
        G_L^ell = -(3/4 s_W^2) Lambda_3(M_W)
        G_L^u   = -(1/12 s_W^2) Lambda_2(M_W) + (3/4 s_W^2) Lambda_3(M_W)
        G_L^d   =  (1/6 s_W^2) Lambda_2(M_W) - (3/4 s_W^2) Lambda_3(M_W)

Honest framing (corrected 2026-05-27)
-------------------------------------
These F_V / F_A objects are the 3-point function piece of the renormalized
one-loop vertex correction in EWWGR's bookkeeping (Eqs 166/167); they are
NOT "bare" form factors awaiting a separate counterterm. Per EWWGR
section 4.1.2 lines 5424-5427: "'vertex corrections' denote the
renormalized gamma(Z)ff three-point functions in one-loop order, together
with the finite wave function renormalizations for external fermions."
The renormalization of the W-triangle is structurally absorbed into the
UV-finite PV combinations Lambda_2, Lambda_3
(apf.w_trace_pv_lambda_bhm_vertex, v24.3.106), not by a separate
counterterm acting on F_V / F_A.

This module evaluates the 3-pt function piece ONLY -- it does NOT include
external fermion wavefunction renormalization. The full physical vertex
composition (3-pt + wavefunction) is the EWWGR Eqs 248-249 layer; the BSY
recipe (EWWGR Eq 175) consumes the 3-pt piece (this module's value) with
the wavefunction handled by the common [(1 - Delta r)/(1 + Pi_hat^Z)]^{1/2}
factor that cancels in the g_V / g_A ratio entering sin^2 theta_eff.

With APF's native sin^2 theta_W = 3/13 and alpha = alpha(0) = 1/137.0359895,
|F_L^ell| ~ 17.77 at s = M_Z^2 -- matching the working-doc "F_L ~ 18"
target. |F_L| ~ 18 is the kinematic-function magnitude INSIDE the
EWWGR Eq.166/167 bracket; the alpha/(4 pi) prefactor outside the bracket
already makes F_V^Zell, F_A^Zell ~ 10^-2. Other channels reach |F_L| in
the same ballpark (charged fermions ~17-18; G_L^ell ~ 10.6) consistent
with the gauge-theoretic structure.

Retraction of earlier framing (2026-05-27, wiki/Log.md LATER-17 +4).
Prior versions of this docstring described F_V / F_A as "BARE" form
factors and asserted a "WWZ counterterm cancellation taking |F_L| from
~18 down to |Lambda_hat| ~ 1e-4" at the R2 gate. That framing was a
misreading: there is no factor-10^5 counterterm cancellation in EWWGR's
one-loop bookkeeping; F_V / F_A as defined here are already the
renormalized 3-pt objects, the |F_L| ~ 18 is in-bracket kinematics, and
the small |Lambda_hat| ~ 1e-4 the original brief invoked does not
correspond to a counterterm-subtracted version of these objects. The
"_bare_" infix in the check function names and the "bare_proper_vertex"
filename are retained as identifiers for bank-registry stability; the
framing they describe is the one in this docstring.

Self-validation (no fitted/measured target)
-------------------------------------------
  * F_L^ell sanity: |F_L^ell|(s=M_Z^2, sin^2 theta_W = 3/13) ~ 17.77,
    within 1% of the working-doc "~18" target.
  * neutrino consistency: F_V^Zν = F_A^Zν per EWWGR.
  * spacelike reality: F's real for s < 0.
  * physical-kinematics reference: F_V^Zell, F_A^Zell, F_L^ell, F_L^u,
    F_L^d, F^Zν, F_V^γell, F_A^γell, G_L^ell all match an INDEPENDENT
    mpmath dps=40 computation (Lambda from polylog(2,.), Feynman iepsilon)
    to relative 1e-12 at s = M_Z^2 with sin^2 theta_W = 3/13 and
    alpha = 1/137.0359895.

Honest scope
------------
The 3-pt function piece of the renormalized one-loop vertex correction
only (EWWGR Eqs 166/167). External fermion wavefunction renormalization
is composed at the next layer (EWWGR Eqs 248-249) together with the
common [(1 - Delta r)/(1 + Pi_hat^Z)]^{1/2} factor that cancels in
g_V / g_A for sin^2 theta_eff. The bosonic Delta kappa (R3),
light-fermion / Delta alpha (R4), and assembled native kappa_l (R5)
remain OPEN. DIZET stays the publishable OS-W closure.

Status
------
- Export_native_bare_proper_vertex_form_factors    = 1   (NEW here)
- Export_native_zll_renormalized_vertex            = 0   (OPEN, R2)
- Export_native_kappa_l_evaluated                  = 0   (OPEN, R5)
- Export_OSW_APF_internal_delta_r_rem_evaluated    = 0   (OPEN, unchanged)
"""
from __future__ import annotations

import math
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_pv_lambda_bhm_vertex import Lambda_2, Lambda_3
from apf.w_trace_pv_scalar_integral_substrate import MW2, MZ2


_PI = math.pi
_ALPHA_0 = 1.0 / 137.0359895   # PDG alpha(0); user can override via the alpha kwarg


def _tree_couplings(fermion: str, sW2: float):
    """Return (I_3, Q, v_f, a_f) tree EW couplings for a given fermion."""
    if fermion in ("e", "mu", "tau", "ell", "l", "lepton"):
        I3, Q = -0.5, -1.0
    elif fermion in ("nu", "neutrino"):
        I3, Q = 0.5, 0.0
    elif fermion in ("u", "c", "t", "up"):
        I3, Q = 0.5, 2.0 / 3.0
    elif fermion in ("d", "s", "b", "down"):
        I3, Q = -0.5, -1.0 / 3.0
    else:
        raise ValueError(f"unknown fermion: {fermion!r}")
    v = I3 - 2.0 * Q * sW2
    a = I3
    return I3, Q, v, a


def F_L(fermion: str, s: float, sW2: float) -> complex:
    """Channel-specific F_L^f(s) per EWWGR L6025-6030. (Without α/4π factor.)"""
    cW2 = 1.0 - sW2
    L2_W = Lambda_2(s, MW2)
    L3_W = Lambda_3(s, MW2)
    coef3 = 3.0 * cW2 / (2.0 * sW2)
    if fermion in ("e", "mu", "tau", "ell", "l", "lepton"):
        return (1.0 / (4.0 * sW2)) * L2_W - coef3 * L3_W
    if fermion in ("u", "c", "t", "up"):
        return -((1.0 - 2.0 * sW2 / 3.0) / (4.0 * sW2)) * L2_W + coef3 * L3_W
    if fermion in ("d", "s", "b", "down"):
        return ((1.0 - 4.0 * sW2 / 3.0) / (4.0 * sW2)) * L2_W - coef3 * L3_W
    raise ValueError(f"F_L not defined for fermion: {fermion!r}")


def G_L(fermion: str, s: float, sW2: float) -> complex:
    """Channel-specific G_L^f(s) per EWWGR L6047-6053. (Without α/4π factor.)"""
    L2_W = Lambda_2(s, MW2)
    L3_W = Lambda_3(s, MW2)
    if fermion in ("e", "mu", "tau", "ell", "l", "lepton"):
        return -(3.0 / (4.0 * sW2)) * L3_W
    if fermion in ("u", "c", "t", "up"):
        return -(1.0 / (12.0 * sW2)) * L2_W + (3.0 / (4.0 * sW2)) * L3_W
    if fermion in ("d", "s", "b", "down"):
        return (1.0 / (6.0 * sW2)) * L2_W - (3.0 / (4.0 * sW2)) * L3_W
    raise ValueError(f"G_L not defined for fermion: {fermion!r}")


def F_V_Z(fermion: str, s: float, sW2: float,
          alpha: float = _ALPHA_0) -> complex:
    """Bare neutral-current vector form factor F_V^Zf(s), with α/(4π) prefactor."""
    if fermion in ("nu", "neutrino"):
        return F_Znu(s, sW2, alpha)
    I3, Q, v, a = _tree_couplings(fermion, sW2)
    cW2 = 1.0 - sW2
    L2_Z = Lambda_2(s, MZ2)
    coef = (v * (v * v + 3.0 * a * a)) / (4.0 * sW2 * cW2)
    return (alpha / (4.0 * _PI)) * (coef * L2_Z + F_L(fermion, s, sW2))


def F_A_Z(fermion: str, s: float, sW2: float,
          alpha: float = _ALPHA_0) -> complex:
    """Bare neutral-current axial form factor F_A^Zf(s), with α/(4π) prefactor."""
    if fermion in ("nu", "neutrino"):
        return F_Znu(s, sW2, alpha)
    I3, Q, v, a = _tree_couplings(fermion, sW2)
    cW2 = 1.0 - sW2
    L2_Z = Lambda_2(s, MZ2)
    coef = (a * (3.0 * v * v + a * a)) / (4.0 * sW2 * cW2)
    return (alpha / (4.0 * _PI)) * (coef * L2_Z + F_L(fermion, s, sW2))


def F_Znu(s: float, sW2: float, alpha: float = _ALPHA_0) -> complex:
    """Bare neutral-current neutrino form factor F_V^Zν = F_A^Zν (EWWGR L6005-6010)."""
    cW2 = 1.0 - sW2
    L2_Z = Lambda_2(s, MZ2)
    L2_W = Lambda_2(s, MW2)
    L3_W = Lambda_3(s, MW2)
    bracket = ((1.0 / (8.0 * cW2 * sW2)) * L2_Z
               + ((2.0 * sW2 - 1.0) / (4.0 * sW2)) * L2_W
               + (3.0 * cW2 / (2.0 * sW2)) * L3_W)
    return (alpha / (4.0 * _PI)) * bracket


def F_V_gamma(fermion: str, s: float, sW2: float,
              alpha: float = _ALPHA_0) -> complex:
    """Bare electromagnetic vector form factor F_V^γf(s)."""
    if fermion in ("nu", "neutrino"):
        return 0.0 + 0.0j  # neutrinos have no EM coupling at tree level
    I3, Q, v, a = _tree_couplings(fermion, sW2)
    cW2 = 1.0 - sW2
    L2_Z = Lambda_2(s, MZ2)
    coef = (Q * (v * v + a * a)) / (4.0 * sW2 * cW2)
    return (alpha / (4.0 * _PI)) * (coef * L2_Z + G_L(fermion, s, sW2))


def F_A_gamma(fermion: str, s: float, sW2: float,
              alpha: float = _ALPHA_0) -> complex:
    """Bare electromagnetic axial form factor F_A^γf(s)."""
    if fermion in ("nu", "neutrino"):
        return 0.0 + 0.0j
    I3, Q, v, a = _tree_couplings(fermion, sW2)
    cW2 = 1.0 - sW2
    L2_Z = Lambda_2(s, MZ2)
    coef = (Q * 2.0 * v * a) / (4.0 * sW2 * cW2)
    return (alpha / (4.0 * _PI)) * (coef * L2_Z + G_L(fermion, s, sW2))


# Reference values via mpmath dps=40 with the SAME conventions (Lambda from
# polylog(2, .) and Feynman iepsilon). Computed for sW2 = 3/13 (APF native)
# at s = M_Z^2 with alpha = 1/137.0359895.
_REF: Dict[str, complex] = {
    "F_L_ell":   complex( 17.61878538895243,    2.282464196106458),
    "F_L_u":     complex(-17.42203232758785,   -1.931315858243926),
    "F_L_d":     complex( 17.22527926622326,    1.580167520381394),
    "G_L_ell":   complex( 10.62092881855371,    0.0),
    "G_L_u":     complex(-11.04722711817698,   -0.7608213987021528),
    "G_L_d":     complex( 11.47352541780024,    1.521642797404306),
    "F_Znu":     complex(-0.009447030488981557, -1.334170007260984e-5),
    "F_V_Zell":  complex( 0.01020579268465159,   0.001284953323720006),
    "F_A_Zell":  complex( 0.0101189761717406,    0.00114724112860142),
    "F_V_gell":  complex( 0.005945560096394528, -0.0003522499435324951),
    "F_A_gell":  complex( 0.006133662541034999, -5.387352077555808e-5),
}

_sW2_APF = 3.0 / 13.0


EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_bare_proper_vertex_form_factors": 1,
    "Export_native_zll_renormalized_vertex": 0,
    "Export_native_kappa_l_evaluated": 0,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


# ===========================================================================
# checks
# ===========================================================================
def check_T_w_trace_pv_ewwgr_bare_F_L_ell_target_P() -> Dict[str, Any]:
    """T: |F_L^ell|(s = M_Z^2, sW2 = 3/13) is the working-doc "~18" target [P]."""
    F = F_L("lepton", MZ2, _sW2_APF)
    mag = abs(F)
    # working doc target: F_L ≈ 18
    check(17.0 < mag < 18.5, f"|F_L^ell| = {mag:.4f} outside [17, 18.5]")
    check(F.imag > 0.0, f"Im F_L^ell must be positive (absorptive), got {F.imag:.2e}")
    return _result(
        name=("T_w_trace_pv_ewwgr_bare_F_L_ell_target: "
              "|F_L^ell|(M_Z^2, sW2=3/13) ~ 18 (working-doc target) [P]"),
        tier=4, epistemic="P",
        summary=(
            f"At the Z pole with the APF-native sin^2 theta_W = 3/13, the "
            f"channel-specific F_L^ell = (1/4 sW^2) Lambda_2(M_W^2) - "
            f"(3 cW^2/2 sW^2) Lambda_3(M_W^2) evaluates to {F.real:.4f} + "
            f"{F.imag:.4f}i, |F_L^ell| = {mag:.4f}. This is the kinematic-"
            f"function magnitude INSIDE the EWWGR Eq.166/167 bracket; with the "
            f"alpha/(4 pi) prefactor outside the bracket, the renormalized "
            f"F_V^Zell / F_A^Zell are ~ 10^-2. The working-doc 'F_L ~ 18' "
            f"target refers to this in-bracket kinematic piece (per the "
            f"corrected 2026-05-27 framing in the module docstring), not a "
            f"counterterm-cancellation scale."
        ),
        key_result=f"|F_L^ell|(M_Z^2, sW2=3/13) = {mag:.4f} (~18 target). [P]",
        dependencies=["T_w_trace_pv_lambda_bhm_physical_values"],
        artifacts={"F_L_ell": F, "magnitude": mag},
    )


def check_T_w_trace_pv_ewwgr_bare_neutrino_consistency_P() -> Dict[str, Any]:
    """T: F_V^Zν = F_A^Zν per EWWGR L6005-6010 [P]."""
    fv = F_V_Z("nu", MZ2, _sW2_APF)
    fa = F_A_Z("nu", MZ2, _sW2_APF)
    diff = abs(fv - fa)
    check(diff < 1e-15, f"F_V^Zν - F_A^Zν = {diff:.2e}, must be 0 by construction")
    return _result(
        name=("T_w_trace_pv_ewwgr_bare_neutrino_consistency: "
              "F_V^Zν = F_A^Zν per EWWGR L6005-6010 [P]"),
        tier=4, epistemic="P",
        summary=(
            f"The neutrino bare proper-vertex form factors satisfy "
            f"F_V^Zν = F_A^Zν (the standard left-handed-only coupling structure "
            f"of the SM neutrino sector reflected at one loop) to {diff:.1e} -- "
            f"a structural consistency check on the wrapper layer."
        ),
        key_result=f"F_V^Zν = F_A^Zν (diff {diff:.1e}). [P]",
        dependencies=["T_w_trace_pv_ewwgr_bare_F_L_ell_target"],
        artifacts={"F_Znu": fv, "diff": diff},
    )


def check_T_w_trace_pv_ewwgr_bare_spacelike_real_P() -> Dict[str, Any]:
    """T: bare vertex form factors are real on spacelike s [P]."""
    mx = 0.0
    for s in (-MZ2, -2.0 * MZ2, -5000.0):
        for fn in (F_V_Z, F_A_Z):
            for f in ("lepton", "u", "d"):
                mx = max(mx, abs(fn(f, s, _sW2_APF).imag))
        mx = max(mx, abs(F_Znu(s, _sW2_APF).imag))
        for fn in (F_V_gamma, F_A_gamma):
            for f in ("lepton", "u", "d"):
                mx = max(mx, abs(fn(f, s, _sW2_APF).imag))
    check(mx < 1e-12, f"spacelike bare-vertex max |Im| {mx:.2e}")
    return _result(
        name=("T_w_trace_pv_ewwgr_bare_spacelike_real: "
              "F_V^{Z,γ}f, F_A^{Z,γ}f, F_Zν real for s < 0 [P]"),
        tier=4, epistemic="P",
        summary=(
            f"For spacelike external invariant s < 0, all bare proper-vertex "
            f"form factors (F_V^Zf, F_A^Zf, F_Zν, F_V^γf, F_A^γf for "
            f"f in {{ell, u, d}}) are real to max |Im| {mx:.1e} -- inherits the "
            f"spacelike reality of Lambda_2, Lambda_3 (R1, v24.3.106) through "
            f"linear combination with tree EW couplings."
        ),
        key_result=f"bare vertex form factors real for s<0 (max |Im| {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_ewwgr_bare_neutrino_consistency"],
        artifacts={"max_abs_im": mx},
    )


def check_T_w_trace_pv_ewwgr_bare_reference_values_P() -> Dict[str, Any]:
    """T: bare proper-vertex form factors match mpmath dps=40 reference [P]."""
    mx = 0.0
    # F_L^f (no α/4π)
    pairs = [
        (F_L("lepton", MZ2, _sW2_APF), _REF["F_L_ell"]),
        (F_L("u",      MZ2, _sW2_APF), _REF["F_L_u"]),
        (F_L("d",      MZ2, _sW2_APF), _REF["F_L_d"]),
        (G_L("lepton", MZ2, _sW2_APF), _REF["G_L_ell"]),
        (G_L("u",      MZ2, _sW2_APF), _REF["G_L_u"]),
        (G_L("d",      MZ2, _sW2_APF), _REF["G_L_d"]),
        (F_Znu(MZ2, _sW2_APF),               _REF["F_Znu"]),
        (F_V_Z("lepton",   MZ2, _sW2_APF),   _REF["F_V_Zell"]),
        (F_A_Z("lepton",   MZ2, _sW2_APF),   _REF["F_A_Zell"]),
        (F_V_gamma("lepton", MZ2, _sW2_APF), _REF["F_V_gell"]),
        (F_A_gamma("lepton", MZ2, _sW2_APF), _REF["F_A_gell"]),
    ]
    for v, ref in pairs:
        denom = max(1.0, abs(ref))
        mx = max(mx, abs(v - ref) / denom)
    check(mx < 1e-12, f"bare vertex max rel err vs mpmath {mx:.2e}")
    return _result(
        name=("T_w_trace_pv_ewwgr_bare_reference_values: "
              "F_V^Z, F_A^Z, F_Zν, F_V^γ, F_A^γ, F_L^f, G_L^f all match "
              "mpmath dps=40 at s = M_Z^2 with sW2 = 3/13 [P]"),
        tier=4, epistemic="P",
        summary=(
            f"Eleven bare proper-vertex form factors (F_L^f and G_L^f for "
            f"f in {{ell, u, d}}, the neutrino F^Zν, the leptonic Z-channel "
            f"F_V^Zell + F_A^Zell, and the leptonic photon-channel F_V^γell + "
            f"F_A^γell) match an INDEPENDENT mpmath dps=40 computation "
            f"(Lambda from polylog(2,.), Feynman iepsilon) at s = M_Z^2 with "
            f"sW2 = 3/13 and alpha = 1/137.0359895 to max rel err {mx:.1e} -- "
            f"a machine-precision tight anchor on the EWWGR L6005-6055 wrapper."
        ),
        key_result=f"11 bare vertex form factors == mpmath dps=40 (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_ewwgr_bare_spacelike_real"],
        artifacts={"max_rel_err": mx, "reference_count": len(pairs)},
    )


def check_T_w_trace_pv_ewwgr_bare_subgate_partial_P() -> Dict[str, Any]:
    """T: 3-pt proper-vertex form factors done; full renormalized vertex (incl. wavefunction renorm) + kappa_l OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_native_bare_proper_vertex_form_factors"] == 1,
          "bare vertex form-factor flag must be 1")
    check(EXPORT_FLAGS["Export_native_zll_renormalized_vertex"] == 0,
          "renormalized Zll vertex (R2) must remain OPEN")
    check(EXPORT_FLAGS["Export_native_kappa_l_evaluated"] == 0,
          "no kappa_l evaluated")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no Delta r_rem evaluated")
    return _result(
        name=("T_w_trace_pv_ewwgr_bare_subgate_partial: "
              "3-pt Zff/γff proper-vertex form factors native (renormalized 3-pt piece "
              "per EWWGR Eqs 166/167, NOT including external fermion wavefunction "
              "renormalization); full vertex composition + kappa_l OPEN [P_structural]"),
        tier=4, epistemic="P_structural",
        summary=(
            "The EWWGR section 6 Zff and γff proper-vertex 3-pt form factors -- "
            "F_V^Zf, F_A^Zf, F_Zν, F_V^γf, F_A^γf, plus the channel-specific "
            "F_L^f and G_L^f for f in {ell, u, d} -- are now native, built as "
            "a thin layer on the R1 BHM Lambda_2, Lambda_3 (v24.3.106) and "
            "wrapped with the tree EW couplings v_f, a_f. These are the 3-pt "
            "function piece of the renormalized one-loop vertex correction in "
            "EWWGR's bookkeeping (Eqs 166/167); they do NOT include external "
            "fermion wavefunction renormalization (framing corrected 2026-05-27 "
            "per module docstring; check identifiers retain '_bare_' for bank-"
            "registry stability). With APF's sin^2 theta_W = 3/13 and "
            "alpha = 1/137.0359895, |F_L^ell| = 17.77 matches the working-doc "
            "in-bracket kinematic target. Still OPEN toward kappa_l: R2 "
            "(full vertex composition including external fermion wavefunction "
            "renormalization per EWWGR Eqs 248-249; the 3-pt piece here is one "
            "of the inputs, with the wavefunction handled by the common "
            "[(1 - Delta r)/(1 + Pi_hat^Z)]^{1/2} factor that cancels in g_V/g_A "
            "for sin^2 theta_eff), R3 (bosonic Delta kappa), R4 (light-fermion / "
            "Delta alpha), R5 (assemble kappa_l = 0.036808 / sin^2 theta_eff = "
            "0.23155). DIZET stays the publishable OS-W closure."
        ),
        key_result=("3-pt Zff/γff proper-vertex form factors native; full "
                    "renormalized vertex (incl. wavefunction renorm) + kappa_l "
                    "OPEN. [P_structural]"),
        dependencies=["T_w_trace_pv_ewwgr_bare_reference_values"],
        cross_refs=["T_w_trace_pv_lambda_bhm_subgate_partial"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_pv_ewwgr_bare_F_L_ell_target":      check_T_w_trace_pv_ewwgr_bare_F_L_ell_target_P,
    "T_w_trace_pv_ewwgr_bare_neutrino_consistency": check_T_w_trace_pv_ewwgr_bare_neutrino_consistency_P,
    "T_w_trace_pv_ewwgr_bare_spacelike_real":      check_T_w_trace_pv_ewwgr_bare_spacelike_real_P,
    "T_w_trace_pv_ewwgr_bare_reference_values":    check_T_w_trace_pv_ewwgr_bare_reference_values_P,
    "T_w_trace_pv_ewwgr_bare_subgate_partial":     check_T_w_trace_pv_ewwgr_bare_subgate_partial_P,
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
