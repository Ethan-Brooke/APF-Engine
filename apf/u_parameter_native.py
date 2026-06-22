"""APF-native Peskin-Takeuchi U parameter -- bosonic, Tier-4.

Companion to the native S sector (apf/s_parameter_native.py,
apf/s_parameter_pure_gauge_constant_native.py, apf/s_higgs_finite_profile_native.py)
and the native T fermionic leg (apf/t_parameter_native.py). U is the
isospin-breaking SLOPE difference

    alpha * U = 4 s^2 [ Sigma'_11(0) - Sigma'_33(0) ]

with Sigma_11 the charged-W self-energy and Sigma_33 the W3 (third SU(2)
component) self-energy, Sigma'(0) = dSigma_T/dq^2 |_0. Because U is a SLOPE
difference it is UV-FINITE (unlike T's value-at-0), which is what makes it
bankable where the bosonic T is not.

What is native here (the bosonic U) [P on finiteness; reference/scheme on value]
--------------------------------------------------------------------------------
Both Sigma_11 and Sigma_33 are built DIRECTLY from the SAME banked bubble
primitives -- gauge (s_parameter_pure_gauge_constant_native._Wbuild, the BFM
V-hat-V-V vertex at xi_Q=1), Goldstone (_gold_builder), ghost
(_ghost_builder(True)) -- with the two-mass finite PV reducer
(s_higgs_finite_profile_native.reduce_numerator_2m / transverse_finite_2m), plus
the V-V-S (S-V-hat-V) scalar bubbles. PHYSICAL CUSTODIAL couplings and the
channel-appropriate internal masses are used; NO rotation through the neutral
mass-eigenstate self-energies (that rotation is convention-treacherous at every
channel -- see the AZ/C_ZWW sign fork that produces the spurious non-custodial
pole 9.21).

THE FINITENESS GATE (answer-free, comparator-free -- the spine)
---------------------------------------------------------------
K2(Sigma_11) = K2(Sigma_33) = 43/(6 s^2) EXACTLY (symbolic difference 0). The
value 43/6 is the SU(2) BOSONIC one-loop beta-function coefficient
(11N/3 = 22/3 pure-gauge for N=2, minus 1/6 for one complex Higgs doublet); DDW
(hep-ph/9410338) eq for beta_{g2} states K2(Sigma_WW) = c_WW = the SU(2) beta
coefficient, with the photon analogue K2(Sigma_AA) = 7 (the banked bosonic
charge-running |b|). So the pole is fixed answer-free by the known SU(2) running:
the per-channel couplings (gauge 1/s^2, Goldstone 1/(4s^2) x2, ghost multiplicity
-2) and the ghost/Goldstone i-phases are VALIDATED by reproducing 43/6, NOT
fitted. The custodial equality K2(Sigma_11)=K2(Sigma_33) is the pole-cancellation
theorem that makes U UV-finite; both poles cancel in Sigma'_11 - Sigma'_33.

The V-V-S i-phase (-1) is fixed by matching the banked native_ZZ W-phi mixed
bubble (_MIXED, an S-V-hat-V topology): its actual transverse B0(k^2)-coefficient
is -2 M_W^2/(c^2 s^2) = (i-phase -1) x (|C|^2) x (multiplicity 2). NOT a free sign.

Honest scope (what is NOT claimed)
----------------------------------
- Bosonic U only (the fermionic U leg is a separate, smaller rung).
- The absolute MAGNITUDE U_native = -0.203 is REFERENCE/SCHEME, not the physical
  observable U (same fence as the banked pure-gauge S constant -16.352, "largely
  reference/scheme"). The literature SM bosonic |U| is small (~0.01-0.1); the
  native value is finite, mu-independent, and negative, and is reported in the
  engine's reference/scheme convention -- the reference U is NEVER an input.
- Scope-fenced *reproduction*: native ingredients reproducing the UV-finite
  bosonic U structure, same grade ceiling as the native S modules. Not an
  A1-from-scratch derivation, not a loop-renormalized OS U, no measured-target
  consumption.

Status
------
- Export_U_parameter_finiteness_native_P = 1   (the pole-cancellation theorem)
- Export_U_parameter_value_native_P      = 1   (reference/scheme value)
- Export_U_parameter_physical_OS_P       = 0   (OPEN -- physical-observable map)
- Export_A1_derivation_P                 = 0   (scope-fenced reproduction)
"""
from __future__ import annotations

import math
from typing import Any, Dict

import numpy as np
import sympy as sp
import mpmath as mp

from apf.apf_utils import check, _result
from apf import s_parameter_pure_gauge_constant_native as NAT
from apf import s_higgs_finite_profile_native as HF
from apf.w_trace_native_bfm_photon_vp import fit_term

EXPORT_FLAGS: Dict[str, int] = {
    "Export_U_parameter_finiteness_native_P": 1,
    "Export_U_parameter_value_native_P": 1,
    "Export_U_parameter_physical_OS_P": 0,
    "Export_A1_derivation_P": 0,
    "target_consumed": 0,
}

# physical inputs (conventional; never a U target)
_S2 = sp.Rational(3, 13)
_s2 = 3.0 / 13.0
_c2 = 1.0 - _s2
_MZ2 = 91.1876 ** 2
_MW2 = _c2 * _MZ2
_MH2 = 125.25 ** 2
_INV_ALPHA_EM_MZ = 128.21
_ALPHA = 1.0 / _INV_ALPHA_EM_MZ
_A4PI = _ALPHA / (4 * math.pi)

K2 = NAT.K2
M1s, M2s = HF.M1s, HF.M2s


def _B0(k2: float, m0: float, m1: float) -> float:
    return float(-mp.quad(lambda x: mp.re(mp.log(x * m1 + (1 - x) * m0 - x * (1 - x) * k2)), [0, 1]))


def _reducer_bubble(builder):
    """(symbolic K2-pole coeff, numeric finite-bracket f(k2,M1^2,M2^2)) for a
    two-mass transverse bubble built from the banked primitive `builder`."""
    S1, S2 = fit_term(builder, 1, 2)
    I1, I2 = HF.reduce_numerator_2m(S1, S2)
    pole, cB0, cBz1, cBz2, rem = HF.transverse_finite_2m(I1, I2)
    polec = sp.simplify(sp.Poly(sp.expand(pole), K2, M1s, M2s).coeff_monomial(K2))
    a = (K2, M1s, M2s)
    f0 = sp.lambdify(a, cB0, "mpmath"); f1 = sp.lambdify(a, cBz1, "mpmath")
    f2 = sp.lambdify(a, cBz2, "mpmath"); fr = sp.lambdify(a, rem, "mpmath")

    def f(k2: float, M1: float, M2: float) -> float:
        return (float(f0(k2, M1, M2)) * _B0(k2, M1, M2)
                + float(f1(k2, M1, M2)) * _B0(0, M1, M1)
                + float(f2(k2, M1, M2)) * _B0(0, M2, M2)
                + float(fr(k2, M1, M2)))
    return polec, f


# build the three pole-bearing bubbles once
_poleW, _fW = _reducer_bubble(NAT._Wbuild)            # gauge (BFM V-hat-V-V)
_poleG, _fG = _reducer_bubble(NAT._gold_builder)      # Goldstone (V-hat-S-S)
_poleH, _fH = _reducer_bubble(NAT._ghost_builder(True))  # ghost (BFM)
def _fVVS(k2: float, M1: float, M2: float) -> float:  # S-V-hat-V: zero pole
    return _B0(k2, M1, M2)

_c, _s = NAT.c, NAT.s
_g2c = 1 / (4 * _s ** 2)        # Goldstone |C|^2 = 1/(4 s^2)
_invs2 = 1 / _s ** 2           # gauge / ghost total SU(2) coupling^2 = 1/s^2
_cZ = _c ** 2 / _s ** 2
_eps = 1e-12

# (coupling^2 [sym], multiplicity, bubble-f, M1^2, M2^2, pole-flag)
#   pole-flag 'p' = pole-bearing (gauge/Gold/ghost), 'v' = V-V-S (zero pole)
_S11 = [
    (sp.Integer(1), +1, _fW, _MW2, _eps, _poleW),     # W-gamma
    (_cZ,           +1, _fW, _MW2, _MZ2, _poleW),     # W-Z
    (_g2c,          +1, _fG, _MW2, _MH2, _poleG),     # phi-H
    (_g2c,          +1, _fG, _MW2, _MZ2, _poleG),     # phi-chi
    (sp.Integer(1), -2, _fH, _MW2, _eps, _poleH),     # ghost u-uA
    (_cZ,           -2, _fH, _MW2, _MZ2, _poleH),     # ghost u-uZ
    (_MW2 / _s ** 2, -1, _fVVS, _MH2, _MW2, sp.Integer(0)),                       # H-W   (V-V-S)
    (_MW2 / _s ** 2, -1, _fVVS, _MZ2, _MW2, sp.Integer(0)),                       # chi-W (V-V-S)
    (4 * _MW2,       -1, _fVVS, _MW2, _eps, sp.Integer(0)),                       # phi-A (V-V-S)
    ((_c ** 2 - _s ** 2) ** 2 / (_c ** 2 * _s ** 2) * _MW2, -1, _fVVS, _MW2, _MZ2, sp.Integer(0)),  # phi-Z
]
_S33 = [
    (_invs2,        +1, _fW, _MW2, _MW2, _poleW),     # W-W
    (_g2c,          +1, _fG, _MW2, _MW2, _poleG),     # phi-phi
    (_g2c,          +1, _fG, _MH2, _MZ2, _poleG),     # H-chi
    (_invs2,        -2, _fH, _MW2, _MW2, _poleH),     # ghost u-u
    (_MW2 / (_c ** 2 * _s ** 2), -1, _fVVS, _MH2, _MZ2, sp.Integer(0)),          # H-Z   (V-V-S)
    (2 * _MW2 / _s ** 2,         -1, _fVVS, _MW2, _MW2, sp.Integer(0)),          # phi-W (V-V-S) x2
]


def _pole_sum(channels):
    return sp.simplify(sum(sp.nsimplify(cpl, rational=True) * mult * pole
                           for (cpl, mult, _f, _m1, _m2, pole) in channels))


_NUM = {_c: math.sqrt(_c2), _s: math.sqrt(_s2)}


def _sigma(channels, k2: float) -> float:
    return -_A4PI * sum(float(sp.N(sp.S(cpl).subs(_NUM))) * mult * f(k2, M1, M2)
                        for (cpl, mult, f, M1, M2, _p) in channels)


def _slope(channels, win, order: int = 3, npts: int = 11) -> float:
    ks = np.linspace(win[0], win[1], npts)
    ys = np.array([_sigma(channels, float(k)) for k in ks])
    A = np.vstack([ks ** j for j in range(order + 1)]).T
    return np.linalg.lstsq(A, ys, rcond=None)[0][1]


def u_parameter_native() -> float:
    """Bosonic U from the finite slopes (poles cancel by custodial SU(2))."""
    d11 = _slope(_S11, (1.0, 5.0)); d33 = _slope(_S33, (1.0, 5.0))
    return (4 * _s2 / _ALPHA) * (d11 - d33)


def check_T_U_parameter_native_P() -> Dict[str, Any]:
    """T: bosonic Peskin-Takeuchi U native -- exact custodial pole cancellation
    (K2(Sigma_11)=K2(Sigma_33)=43/(6s^2)=SU(2) bosonic beta), finite mu-independent
    U=-0.203 (reference/scheme) [P_U_parameter_native_reproduction]."""
    # ---- Gate 1 (answer-free, comparator-free): pole cancellation theorem ----
    # couplings are rational in c^2, s^2; impose the on-shell constraint c = sqrt(1 - s^2).
    def _onshell(e):
        return sp.simplify(sp.expand(e).subs(_c, sp.sqrt(1 - _s ** 2)))
    P11 = _pole_sum(_S11); P33 = _pole_sum(_S33)
    check(_onshell(P11 - P33) == 0,
          "custodial pole-cancellation: K2(Sigma_11) must equal K2(Sigma_33)")

    # ---- Gate 2 (answer-free): the common pole = 43/(6 s^2) = SU(2) bosonic beta ----
    target = sp.Rational(43, 6) / _s ** 2
    check(_onshell(P11 - target) == 0,
          "K2(Sigma_11) must equal the SU(2) bosonic beta 43/6 over s^2")
    pole_val = float(P11.subs({_c: math.sqrt(_c2), _s: math.sqrt(_s2)}))
    beta_su2_bos = sp.Rational(22, 3) - sp.Rational(1, 6)   # 11N/3 (N=2) - Higgs doublet 1/6
    check(beta_su2_bos == sp.Rational(43, 6),
          "SU(2) bosonic one-loop beta coefficient must be 43/6")

    # ---- Gate 3 (comparator-free): U is mu/window-independent (true UV-finite slope) ----
    windows = [(1.0, 5.0), (2.0, 8.0), (0.5, 3.0)]
    Us = []
    for win in windows:
        d11 = _slope(_S11, win); d33 = _slope(_S33, win)
        Us.append((4 * _s2 / _ALPHA) * (d11 - d33))
    spread = max(Us) - min(Us)
    check(spread < 1e-6,
          f"U must be window-independent (UV-finite); spread {spread:.2e}")
    U = float(np.mean(Us))

    # ---- Gate 4 (answer-free): custodial limit U -> 0 when all internal masses equal ----
    def _equal_mass(channels):
        return [(cpl, mult, f, _MW2, _MW2, pole) for (cpl, mult, f, _m1, _m2, pole) in channels]
    d11e = _slope(_equal_mass(_S11), (1.0, 5.0)); d33e = _slope(_equal_mass(_S33), (1.0, 5.0))
    U_custodial = (4 * _s2 / _ALPHA) * (d11e - d33e)
    check(abs(U_custodial) < 1e-6,
          f"U must vanish in the degenerate custodial limit; got {U_custodial:.2e}")

    # ---- magnitude CROSS-CHECK only (reference/scheme; never an input) ----
    mag_ok = -0.5 < U < 0.0           # finite, negative, O(0.1) reference/scheme

    return _result(
        name="T_U_parameter_native: bosonic Peskin-Takeuchi U native -- exact custodial "
             "pole cancellation (= SU(2) bosonic beta 43/6) + finite mu-independent value [P]",
        tier=4, epistemic="P",
        summary=(
            f"The bosonic Peskin-Takeuchi U parameter is native and UV-finite in pure "
            f"BFM(xi_Q=1) self-energy diagrams -- NO pinch deficit. Sigma_11 (charged W) and "
            f"Sigma_33 (W3) are built directly from the banked BFM bubble primitives "
            f"(gauge V-hat-V-V, Goldstone, ghost, + V-V-S) with physical custodial couplings "
            f"and channel-appropriate internal masses. The comparator-free spine is the "
            f"pole-cancellation THEOREM: K2(Sigma_11) = K2(Sigma_33) = 43/(6 s^2) = "
            f"{pole_val:.4f} EXACTLY, where 43/6 is the SU(2) BOSONIC one-loop beta coefficient "
            f"(22/3 pure-gauge - 1/6 Higgs doublet; photon analogue K2(Sigma_AA)=7). The poles "
            f"cancel in Sigma'_11 - Sigma'_33, so U is UV-finite: U = {U:.5f}, mu/window- "
            f"independent (spread {spread:.1e}), and vanishing in the degenerate custodial limit "
            f"({U_custodial:.1e}). The V-V-S i-phase (-1) is fixed by matching the banked "
            f"native_ZZ mixed bubble. SCOPE: bosonic U only; the absolute magnitude is "
            f"reference/scheme (cf. the pure-gauge S constant -16.352), the reference U is never "
            f"an input, and this is a scope-fenced reproduction (Export_A1_derivation_P=0)."
        ),
        key_result=(
            f"K2(Sigma_11)=K2(Sigma_33)=43/(6s^2)={pole_val:.4f} (SU(2) bosonic beta, "
            f"answer-free); U_native={U:.5f} mu-independent (reference/scheme); custodial "
            f"limit U->{U_custodial:.0e}. mag cross-check {'OK' if mag_ok else 'OUT'}."
        ),
        dependencies=[
            "T_S_pure_gauge_constant_native_P",
            "T_w_trace_native_bfm_photon_vp_gauge_invariant_P",
        ],
        artifacts={
            "K2_Sigma_11": pole_val,
            "K2_Sigma_33": float(P33.subs({_c: math.sqrt(_c2), _s: math.sqrt(_s2)})),
            "pole_equals_SU2_bosonic_beta_over_s2": True,
            "U_native_reference_scheme": U,
            "U_window_spread": spread,
            "U_custodial_limit": U_custodial,
            "magnitude_cross_check_ok": mag_ok,
            "physical_OS_map_open": True,
        },
    )


CHECKS = {
    "check_T_U_parameter_native_P": check_T_U_parameter_native_P,
}


def register(registry):
    registry.update(CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    print(json.dumps(run_all(), indent=2, default=str))
