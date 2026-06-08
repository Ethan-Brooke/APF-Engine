"""APF-native bosonic gauge-boson self-energies (Denner App.B) -- Tier-4.

Step 4 of the native OS-W precision close: transcribe Denner's REVIEWED closed
forms for the bosonic transverse gauge-boson self-energies Sigma^AA_T, Sigma^ZZ_T,
Sigma^W_T (arXiv:0709.1075 App.B, the W/Z/Higgs/Goldstone/ghost loops) and
evaluate them NATIVELY with the PV toolkit (timelike + massless-safe B0). This is
the v24.3.87-held W-sector piece done the right way -- from the checked vertex
algebra, not memory-reconstructed vertices.

The bosonic part of each self-energy (the fermion sums are banked separately,
v24.3.97):

    Sigma^AA_bos = -(a/4pi){ [3k^2+4MW^2]B0(k^2,MW,MW) - 4MW^2 B0(0,MW,MW) }
    Sigma^ZZ_bos = -(a/4pi){ gauge-brace(MW) + Higgs-brace(MZ,MH) }
    Sigma^W_bos  = -(a/4pi){ W-photon-brace + W-Z-brace + W-H-brace }

(exact coefficient lists transcribed below).

Validation (against banked poles -- no fabrication)
---------------------------------------------------
The UV pole of B0 is mu-independent (dB0/dln mu^2 = +1), so the pole coefficient
equals dSigma/dln mu^2; the (1/k^2)(B0(k^2)-B0(0)) "regulator" terms are pole-free
(dB0/dln mu^2 cancels). Reading the pole numerically off the mu-running:
- photon bosonic pole = 3 k^2  -> photon VP coefficient -3 (banked v24.3.88).
- bosonic Delta rho pole = Sigma^W(0)/MW^2 - Sigma^ZZ(0)/MZ^2 pole = +4
  (banked v24.3.90), M_H-independent.
- k^2 -> 0 regularity: the 1/k^2 terms cancel, Sigma^ZZ_bos / Sigma^W_bos finite.

Both poles were confirmed analytically (sympy) before this rung; here they are
re-derived numerically from the native evaluator, validating the transcription.

Scope: the bosonic self-energies as native functions + their pole/regularity
validation. The finite OS-renormalized Re Sigma^VV_bos(M_V^2) at timelike p^2
(with the photon IR lambda + delta_VB handling) and the assembled Delta r_rem / M_W
remain OPEN. No Delta r_rem / M_W; DIZET stays the publishable OS-W closure.
"""
from __future__ import annotations

import math
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_native_pv_massless_safe import re_b0_safe

_S2 = 3.0 / 13.0
_C2 = 1.0 - _S2
_ALPHA = 1.0 / 128.21
_A4PI = _ALPHA / (4.0 * math.pi)
_M_Z = 91.1876
_MZ2 = _M_Z ** 2
_MW2 = _MZ2 * _C2
_MH2 = 125.25 ** 2   # SM Higgs mass^2 (input for finite parts; poles are MH-independent)
_LAM2 = 1e-6         # photon IR regulator^2 (poles/regularity are lambda-independent)


def _B0(k2, m02, m12, mu2):
    return re_b0_safe(k2, m02, m12, mu2)


def sigma_AA_bos(k2, mu2, MH2=_MH2):
    return -_A4PI * ((3.0*k2 + 4.0*_MW2) * _B0(k2, _MW2, _MW2, mu2)
                     - 4.0*_MW2 * _B0(0.0, _MW2, _MW2, mu2))


def sigma_ZZ_bos(k2, mu2, MH2=_MH2):
    gauge = (1.0/(6.0*_S2*_C2)) * (
        ((18.0*_C2**2 + 2.0*_C2 - 0.5)*k2 + (24.0*_C2**2 + 16.0*_C2 - 10.0)*_MW2)
        * _B0(k2, _MW2, _MW2, mu2)
        - (24.0*_C2**2 - 8.0*_C2 + 2.0)*_MW2 * _B0(0.0, _MW2, _MW2, mu2)
        + (4.0*_C2 - 1.0)*(1.0/3.0)*k2)
    higgs = (1.0/(12.0*_S2*_C2)) * (
        (2.0*MH2 - 10.0*_MZ2 - k2) * _B0(k2, _MZ2, MH2, mu2)
        - 2.0*_MZ2 * _B0(0.0, _MZ2, _MZ2, mu2)
        - 2.0*MH2 * _B0(0.0, MH2, MH2, mu2)
        - ((_MZ2 - MH2)**2 / k2) * (_B0(k2, _MZ2, MH2, mu2) - _B0(0.0, _MZ2, MH2, mu2))
        - (2.0/3.0)*k2)
    return -_A4PI * (gauge + higgs)


def sigma_W_bos(k2, mu2, MH2=_MH2, lam2=_LAM2):
    wph = (2.0/3.0) * (
        (2.0*_MW2 + 5.0*k2) * _B0(k2, _MW2, lam2, mu2)
        - 2.0*_MW2 * _B0(0.0, _MW2, _MW2, mu2)
        - (_MW2**2 / k2) * (_B0(k2, _MW2, lam2, mu2) - _B0(0.0, _MW2, lam2, mu2))
        + (1.0/3.0)*k2)
    wz = (1.0/(12.0*_S2)) * (
        ((40.0*_C2 - 1.0)*k2 + (16.0*_C2 + 54.0 - 10.0/_C2)*_MW2)
        * _B0(k2, _MW2, _MZ2, mu2)
        - (16.0*_C2 + 2.0) * (_MW2*_B0(0.0, _MW2, _MW2, mu2) + _MZ2*_B0(0.0, _MZ2, _MZ2, mu2))
        + (4.0*_C2 - 1.0)*(2.0/3.0)*k2
        - (8.0*_C2 + 1.0)*((_MW2 - _MZ2)**2 / k2)
        * (_B0(k2, _MW2, _MZ2, mu2) - _B0(0.0, _MW2, _MZ2, mu2)))
    wh = (1.0/(12.0*_S2)) * (
        (2.0*MH2 - 10.0*_MW2 - k2) * _B0(k2, _MW2, MH2, mu2)
        - 2.0*_MW2 * _B0(0.0, _MW2, _MW2, mu2)
        - 2.0*MH2 * _B0(0.0, MH2, MH2, mu2)
        - ((_MW2 - MH2)**2 / k2) * (_B0(k2, _MW2, MH2, mu2) - _B0(0.0, _MW2, MH2, mu2))
        - (2.0/3.0)*k2)
    return -_A4PI * (wph + wz + wh)


def _pole_units(func, k2, mu2=1.0e4, **kw):
    """dSigma/dln mu^2 / (-a/4pi) = coefficient of Delta (the UV pole)."""
    return (func(k2, math.e * mu2, **kw) - func(k2, mu2, **kw)) / (-_A4PI)


def drho_bos(k2, mu2):
    return sigma_W_bos(k2, mu2) / _MW2 - sigma_ZZ_bos(k2, mu2) / _MZ2


EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_bosonic_gauge_self_energy": 1,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


# ===========================================================================
# checks
# ===========================================================================
def check_T_w_trace_native_bosonic_photon_pole_P() -> Dict[str, Any]:
    """T: native bosonic Sigma^AA_T pole = 3 k^2 (photon VP -3) [P]."""
    mx = 0.0
    for k2 in (-1.0, -50.0, -1000.0):
        coef = _pole_units(sigma_AA_bos, k2) / k2
        mx = max(mx, abs(coef - 3.0))
    check(mx < 1e-6, f"photon bosonic pole coeff must be 3, max dev {mx:.2e}")
    return _result(
        name="T_w_trace_native_bosonic_photon_pole: "
             "native bosonic Sigma^AA_T pole = 3 k^2 (photon VP -3) [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native bosonic photon self-energy Sigma^AA_bos = -(a/4pi)"
            f"{{[3k^2+4MW^2]B0(k^2,MW,MW) - 4MW^2 B0(0,MW,MW)}} has UV pole 3 k^2 "
            f"(read off the mu-running to {mx:.1e}), i.e. photon vacuum-polarization "
            f"coefficient -3 -- reproducing the banked bosonic photon pole "
            f"(v24.3.88: Goldstone +1/3, W+ghost -10/3). Validates the W/Goldstone/"
            f"ghost transcription from Denner App.B."
        ),
        key_result=f"bosonic Sigma^AA_T pole = 3 k^2 (VP -3), dev {mx:.1e}. [P]",
        dependencies=["T_w_trace_native_bosonic_photon_vp_pole"],
        artifacts={"max_dev": mx},
    )


def check_T_w_trace_native_bosonic_drho_pole_P() -> Dict[str, Any]:
    """T: native bosonic Delta rho pole = +4, M_H-independent [P]."""
    devs = []
    for MH in (125.25, 200.0, 600.0):
        mh2 = MH * MH
        # affine in k^2: evaluate at two spacelike points, extrapolate to k^2=0
        def dr(k2, mu2):
            return (sigma_W_bos(k2, mu2, mh2) / _MW2) - (sigma_ZZ_bos(k2, mu2, mh2) / _MZ2)
        g1 = _pole_units(dr, -1.0)
        g2 = _pole_units(dr, -2.0)
        intercept = 2.0 * g1 - g2      # affine extrapolation to k^2 = 0
        devs.append(abs(intercept - 4.0))
    mx = max(devs)
    check(mx < 1e-5, f"bosonic Delta rho pole must be 4, max dev {mx:.2e}")
    return _result(
        name="T_w_trace_native_bosonic_drho_pole: "
             "native bosonic Delta rho pole = +4, M_H-independent [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native bosonic custodial pole Delta rho_bos = Sigma^W_bos(0)/MW^2 "
            f"- Sigma^ZZ_bos(0)/MZ^2 has UV pole +4 (affine k^2-extrapolation of the "
            f"mu-running to k^2=0, max dev {mx:.1e}) and is M_H-independent (checked "
            f"M_H = 125, 200, 600 GeV) -- reproducing the banked bosonic Delta rho "
            f"bare pole (v24.3.90: +4 universal). A strong correctness gate: the "
            f"W-Z, W-H, gauge and Higgs braces combine to exactly 4."
        ),
        key_result=f"bosonic Delta rho pole = +4 (M_H-indep), dev {mx:.1e}. [P]",
        dependencies=["T_w_trace_native_bosonic_photon_pole",
                      "T_w_trace_native_uv_cancel_drho_plus4_absorbed"],
        artifacts={"max_dev": mx},
    )


def check_T_w_trace_native_bosonic_regularity_P() -> Dict[str, Any]:
    """T: bosonic Sigma^ZZ_T regular at k^2 -> 0; Sigma^W_T stable in-regime [P]."""
    # Sigma^ZZ_bos has no massless line -> the (MZ^2-MH^2)^2/k^2 term cancels
    # cleanly; test convergence to a finite limit down to tiny k^2.
    zz = [sigma_ZZ_bos(k2, 1.0e4) for k2 in (1.0e-2, 1.0e-3, 1.0e-4)]
    zz_spread = (max(zz) - min(zz)) / max(1e-30, abs(sum(zz) / 3.0))
    check(zz_spread < 1e-3, f"Sigma^ZZ_bos must converge at k^2->0, spread {zz_spread:.2e}")
    for v in zz:
        check(math.isfinite(v), "Sigma^ZZ_bos must be finite near k^2=0")
    # Sigma^W_bos contains the photon (massless) loop: its (MW^4/k^2)(B0(k^2,MW,lam)
    # -B0(0,MW,lam)) term is analytically regular but a catastrophic cancellation
    # for k^2 << MW^2 (also photon-IR delicate). It is well-conditioned at moderate
    # / physical k^2; test smoothness there (the regime the OS point M_W^2 lives in).
    ww = [sigma_W_bos(k2, 1.0e4) for k2 in (50.0, 10.0, 2.0, 1.0, 0.5)]
    ww_spread = (max(ww) - min(ww)) / max(1e-30, abs(sum(ww) / len(ww)))
    check(ww_spread < 0.1, f"Sigma^W_bos must be smooth in-regime, spread {ww_spread:.2e}")
    for v in ww:
        check(math.isfinite(v), "Sigma^W_bos must be finite in-regime")
    return _result(
        name="T_w_trace_native_bosonic_regularity: "
             "bosonic Sigma^ZZ_T regular at k^2->0; Sigma^W_T stable in-regime [P]",
        tier=4, epistemic="P",
        summary=(
            f"Sigma^ZZ_bos has no massless line: the (MZ^2-MH^2)^2/k^2 (B0(k^2)-B0(0)) "
            f"regulator term cancels cleanly and Sigma^ZZ_bos converges to a finite "
            f"limit as k^2 -> 0 (relative spread {zz_spread:.1e} over k^2 1e-2..1e-4). "
            f"Sigma^W_bos contains the photon loop, whose (MW^4/k^2) term is "
            f"analytically regular but a catastrophic numerical cancellation for "
            f"k^2 << MW^2; in the well-conditioned regime (k^2 = 0.5..50) Sigma^W_bos "
            f"is smooth (spread {ww_spread:.1e}) -- the regime the OS point k^2=MW^2 "
            f"lives in. The 1/k^2 terms are genuinely regular; only the small-k^2 "
            f"photon piece needs the IR-aware evaluation deferred to the finite rung."
        ),
        key_result=f"Sigma^ZZ regular at k^2->0 ({zz_spread:.0e}); Sigma^W smooth in-regime ({ww_spread:.0e}). [P]",
        dependencies=["T_w_trace_native_bosonic_drho_pole"],
        artifacts={"zz_spread": zz_spread, "ww_spread": ww_spread},
    )


def check_T_w_trace_native_bosonic_scope_partial_P() -> Dict[str, Any]:
    """T: bosonic self-energies native + pole-validated; finite Delta r_rem OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_native_bosonic_gauge_self_energy"] == 1, "bosonic flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no Delta r_rem evaluated by this rung")
    return _result(
        name="T_w_trace_native_bosonic_scope_partial: "
             "bosonic self-energies native + pole-validated; finite Delta r_rem OPEN [P_structural]",
        tier=4, epistemic="P_structural",
        summary=(
            "Denner's reviewed bosonic Sigma^AA_T / Sigma^ZZ_T / Sigma^W_T (App.B) "
            "are now native functions on the PV toolkit, validated by the banked "
            "poles (photon -3, bosonic Delta rho +4, M_H-independent) and k^2->0 "
            "regularity -- the v24.3.87-held W-sector bosonic piece done from the "
            "checked vertex algebra. OPEN toward Delta r_rem / M_W: the finite "
            "OS-renormalized Re Sigma^VV_bos(M_V^2) at timelike p^2 (with the photon "
            "IR lambda + delta_VB handling), the assembled Delta r_rem, and the "
            "GFloop resummation. No Delta r_rem / M_W; DIZET stays the publishable "
            "OS-W closure."
        ),
        key_result="Bosonic self-energies native + pole-validated; finite Delta r_rem OPEN. [P_structural]",
        dependencies=["T_w_trace_native_bosonic_regularity"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_native_bosonic_photon_pole": check_T_w_trace_native_bosonic_photon_pole_P,
    "T_w_trace_native_bosonic_drho_pole": check_T_w_trace_native_bosonic_drho_pole_P,
    "T_w_trace_native_bosonic_regularity": check_T_w_trace_native_bosonic_regularity_P,
    "T_w_trace_native_bosonic_scope_partial": check_T_w_trace_native_bosonic_scope_partial_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}
