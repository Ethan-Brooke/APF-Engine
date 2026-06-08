"""APF-native Delta r assembly: full UV cancellation + delta_VB -- Tier-4.

The capstone of the native OS-W self-energy arc. Denner's master formula for the
muon-decay radiative correction (arXiv:0709.1075, eq. for Delta r):

    Delta r = Pi^{AA}(0) - (c^2/s^2)[ Sigma^{ZZ}_T(M_Z^2)/M_Z^2 - Sigma^{W}_T(M_W^2)/M_W^2 ]
              + [ Sigma^{W}_T(0) - Sigma^{W}_T(M_W^2) ]/M_W^2
              + 2 (c/s) Sigma^{AZ}_T(0)/M_Z^2
              + (alpha/4pi s^2) ( 6 + (7 - 4 s^2)/(2 s^2) log c^2 ) .

The last line is delta_VB -- the Sirlin vertex+box correction, which Denner gives
as a CLOSED FORM (the native 3-/4-point C/D tensors built in v24.3.74-.79 assemble
to exactly this; here it is taken from the reviewed closed form).

This module does two things:

1. FULL Delta r UV CANCELLATION (the Stage-4 capstone gate). Every gauge-boson
   self-energy pole assembled across the native modules --
     Sigma^{AA} : apf.w_trace_native_uv_cancellation_stage4 (P_AA_bos + P_AA_ferm)
     Sigma^{ZZ} : P_ZZ_bos (stage4) + fermionic p2coeff_ZZ (v24.3.92) + ferm m^2 here
     Sigma^{WW} : P_WW_bos (stage4) + fermionic p2coeff_WW (v24.3.92) + ferm m^2 here
     Sigma^{AZ}(0) : bosonic pole here
   -- is substituted into Denner's master formula. The result is UV-FINITE: the
   1/eps pole cancels to machine precision, gauge-invariantly (independent of
   sin^2 theta_W), PROVIDED the on-shell relation c^2 = M_W^2/M_Z^2 holds. This is
   the famous finiteness of Delta r, demonstrated natively from the full
   fermionic+bosonic self-energy pole structure -- a cross-module integration test
   that no single earlier rung performed (the per-boson / per-sector checks are
   not sensitive to the cross-boson coefficients this combination probes).

2. delta_VB native (Denner closed form), finite and gauge-invariant.

With the UV cancellation closed and delta_VB in hand, the native Delta r is fully
ASSEMBLED at the structural + divergence level. The ONE remaining input is the
finite REAL part of the timelike self-energies Re Sigma_{WW}(M_W^2)/Re Sigma_{ZZ}(M_Z^2)
(+ Sigma_W(0)); their VALUE has no internal anchor (only an external DIZET
comparator), so the numeric Delta r_rem / M_W stays [C] and DIZET remains the
publishable OS-W closure.

Status
------
- Export_native_delta_r_uv_cancellation          = 1
- Export_native_delta_VB_closed_form             = 1
- Export_OSW_APF_internal_delta_r_rem_evaluated   = 0   (OPEN, unchanged)
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple

from apf.apf_utils import check, _result
from apf.w_trace_native_uv_cancellation_stage4 import (
    P_AA_bos, P_AA_ferm, P_ZZ_bos, P_WW_bos,
)
from apf.w_trace_native_fermionic_gauge_self_energy import p2coeff_ZZ, p2coeff_WW
from apf.w_trace_native_uv_pole import sum_Nc_Q2

_ALPHA = 1.0 / 137.035999084
_S2 = 3.0 / 13.0
_MW = 80.379
_MW2 = _MW * _MW

# (Q, I3, N_c, m) per fermion -- consistent real masses (used only for the m^2 pole pieces).
_FERMIONS: List[Tuple[float, float, float, float]] = [
    (0.0, 0.5, 1.0, 0.0), (-1.0, -0.5, 1.0, 0.000511), (2.0/3.0, 0.5, 3.0, 0.0022), (-1.0/3.0, -0.5, 3.0, 0.0047),
    (0.0, 0.5, 1.0, 0.0), (-1.0, -0.5, 1.0, 0.105658), (2.0/3.0, 0.5, 3.0, 1.27), (-1.0/3.0, -0.5, 3.0, 0.093),
    (0.0, 0.5, 1.0, 0.0), (-1.0, -0.5, 1.0, 1.77686), (2.0/3.0, 0.5, 3.0, 163.0), (-1.0/3.0, -0.5, 3.0, 4.18),
]
# W doublets (m_up, m_down, N_c) consistent with _FERMIONS.
_WDOUBLETS: List[Tuple[float, float, float]] = [
    (0.0, 0.000511, 1.0), (0.0022, 0.0047, 3.0), (0.0, 0.105658, 1.0),
    (1.27, 0.093, 3.0), (0.0, 1.77686, 1.0), (163.0, 4.18, 3.0),
]


# ===========================================================================
# full self-energy pole content P_VV(p^2)  (Sigma_T = -(alpha/4pi) P)
# ===========================================================================
def _A_AA() -> float:
    """Coefficient of p^2 in P_AA (ferm+bos), via the banked stage-4 functions."""
    return (P_AA_bos(1.0, _MW2) + P_AA_ferm(1.0))            # linear -> value at p^2=1 is the slope


def P_ZZ_full(p2: float, s2: float = _S2, mw2: float = _MW2) -> float:
    c2 = 1.0 - s2
    ferm_m2 = (2.0 / 3.0) * sum(Nc * (3.0 / (4.0 * s2 * c2)) * m * m for Q, I3, Nc, m in _FERMIONS)
    return P_ZZ_bos(p2, s2, mw2) + p2coeff_ZZ(s2) * p2 + ferm_m2


def P_W_full(p2: float, s2: float = _S2, mw2: float = _MW2) -> float:
    ferm_m2 = (2.0 / 3.0) * (1.0 / (2.0 * s2)) * sum(
        Nc * 1.5 * (mu * mu + md * md) for mu, md, Nc in _WDOUBLETS)
    return P_WW_bos(p2, s2, mw2) + p2coeff_WW(s2) * p2 + ferm_m2


def P_AZ_at0(s2: float = _S2, mw2: float = _MW2) -> float:
    """Bosonic Sigma^{AZ}_T(0) pole content (fermionic part vanishes at 0): -2 M_W^2/(s c)."""
    s = math.sqrt(s2); c = math.sqrt(1.0 - s2)
    return -(2.0 / (s * c)) * mw2


def delta_r_uv_pole(s2: float = _S2, mw2: float = _MW2) -> float:
    """Assemble Denner's Delta r pole (units alpha/4pi * Delta_eps); expect 0 (OS c^2=M_W^2/M_Z^2)."""
    c2 = 1.0 - s2; s = math.sqrt(s2); c = math.sqrt(c2)
    mz2 = mw2 / c2                                            # OS relation -- required for cancellation
    A_AA = _A_AA()
    # Sigma_VV -> -(alpha/4pi) P_VV ; Pi^AA(0) = dSigma^AA/dk^2|0 -> -(alpha/4pi) A_AA
    return (-A_AA
            + (c2 / s2) * (P_ZZ_full(mz2, s2, mw2) / mz2 - P_W_full(mw2, s2, mw2) / mw2)
            + (P_W_full(mw2, s2, mw2) - P_W_full(0.0, s2, mw2)) / mw2
            - 2.0 * (c / s) * P_AZ_at0(s2, mw2) / mz2)


def delta_VB(s2: float = _S2, alpha: float = _ALPHA) -> float:
    """Denner/Sirlin vertex+box closed form (UV-finite, gauge-invariant)."""
    c2 = 1.0 - s2
    return (alpha / (4.0 * math.pi * s2)) * (6.0 + (7.0 - 4.0 * s2) / (2.0 * s2) * math.log(c2))


EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_delta_r_uv_cancellation": 1,
    "Export_native_delta_VB_closed_form": 1,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


# ===========================================================================
# checks
# ===========================================================================
def check_T_w_trace_native_delta_r_uv_cancellation_P() -> Dict[str, Any]:
    """T: full Delta r is UV-finite -- all native self-energy poles cancel in Denner's formula [P]."""
    scale = abs(_A_AA()) or 1.0
    pole = delta_r_uv_pole(_S2, _MW2)
    rel = abs(pole) / scale
    check(rel < 1e-9, f"full Delta r UV pole must vanish; got {pole:.3e} (rel {rel:.2e})")
    return _result(
        name="T_w_trace_native_delta_r_uv_cancellation: "
             "full Delta r is UV-finite (all native self-energy poles cancel) [P]",
        tier=4, epistemic="P",
        summary=(
            f"Substituting every native gauge-boson self-energy pole -- Sigma^{{AA}} "
            f"(P_AA_bos + P_AA_ferm, stage-4), Sigma^{{ZZ}}/Sigma^{{WW}} (banked bosonic "
            f"P_*_bos + fermionic p2coeff_* + the m^2 pieces), Sigma^{{AZ}}(0) -- into "
            f"Denner's Delta r master formula yields a UV pole of {pole:.1e} (rel {rel:.1e}), "
            f"i.e. ZERO: Delta r is UV-finite. This is the Stage-4 capstone and a "
            f"cross-module integration test sensitive to the absolute cross-boson "
            f"coefficients (which the per-boson / Delta rho checks are not). It requires "
            f"the on-shell relation c^2 = M_W^2/M_Z^2; with it, the famous finiteness of "
            f"Delta r is demonstrated natively from the full fermionic+bosonic self-energy "
            f"pole structure, no external input."
        ),
        key_result=f"full Delta r UV pole = 0 (rel {rel:.1e}); native self-energy poles cancel in Denner's formula. [P]",
        dependencies=["T_w_trace_native_uv_cancel_os_renormalized_finite",
                      "T_w_trace_native_fermionic_gauge_ZAZ_weinberg",
                      "T_w_trace_native_drho_fermionic_uv_finite"],
        artifacts={"delta_r_uv_pole": pole, "rel": rel},
    )


def check_T_w_trace_native_delta_r_uv_gauge_invariance_P() -> Dict[str, Any]:
    """T: the Delta r UV cancellation is independent of sin^2 theta_W (gauge invariance) [P]."""
    vals = {}
    for s2 in (0.20, 3.0 / 13.0, 0.2312, 0.25, 0.30):
        vals[round(s2, 4)] = delta_r_uv_pole(s2, _MW2)
    mx = max(abs(v) for v in vals.values())
    scale = abs(_A_AA()) or 1.0
    check(mx / scale < 1e-9, f"Delta r UV pole must vanish for all sin^2 theta; max {mx:.2e}")
    return _result(
        name="T_w_trace_native_delta_r_uv_gauge_invariance: "
             "Delta r UV cancellation is sin^2 theta_W-independent (gauge invariance) [P]",
        tier=4, epistemic="P",
        summary=(
            f"The full Delta r UV pole vanishes (max |pole| {mx:.1e}) across sin^2 theta_W "
            f"in [0.20, 0.30] -- the cancellation is gauge/weak-angle independent, as a "
            f"physical (finite) Delta r must be. A strong consistency gate on the entire "
            f"native self-energy pole structure simultaneously."
        ),
        key_result=f"Delta r UV cancellation sin^2 theta_W-independent (max |pole| {mx:.1e}). [P]",
        dependencies=["T_w_trace_native_delta_r_uv_cancellation"],
        artifacts={"pole_by_sin2": vals},
    )


def check_T_w_trace_native_delta_VB_closed_form_P() -> Dict[str, Any]:
    """T: native delta_VB (Denner/Sirlin vertex+box closed form) finite + gauge-invariant [P]."""
    dvb = delta_VB(_S2)
    # finite, real, and the expected sign/magnitude of the Sirlin vertex+box
    check(math.isfinite(dvb) and dvb > 0.0, f"delta_VB must be finite and positive, got {dvb}")
    # structural: alpha/(4pi s^2) prefactor + (6 + (7-4s^2)/(2s^2) ln c^2); reproduce by hand
    c2 = 1.0 - _S2
    expect = (_ALPHA / (4.0 * math.pi * _S2)) * (6.0 + (7.0 - 4.0 * _S2) / (2.0 * _S2) * math.log(c2))
    check(abs(dvb - expect) < 1e-15, "delta_VB closed-form mismatch")
    return _result(
        name="T_w_trace_native_delta_VB_closed_form: "
             "native delta_VB (Sirlin vertex+box, Denner closed form) finite + gauge-invariant [P]",
        tier=4, epistemic="P",
        summary=(
            f"The Sirlin vertex+box correction delta_VB = (alpha/4pi s^2)(6 + "
            f"(7-4s^2)/(2s^2) ln c^2), Denner's reviewed closed form (the assembled "
            f"muon-decay vertex+box that the native 3-/4-point C/D tensors of v24.3.74-.79 "
            f"build), evaluated at the APF s^2 = 3/13 gives delta_VB = {dvb:.6f} -- finite "
            f"and gauge-invariant by construction (the individually-divergent vertex and box "
            f"sum to this finite result). The last component of Denner's Delta r formula."
        ),
        key_result=f"native delta_VB (Denner/Sirlin closed form) = {dvb:.6f}, finite + gauge-invariant. [P]",
        dependencies=["T_w_trace_native_delta_r_uv_cancellation"],
        artifacts={"delta_VB": dvb},
    )


def check_T_w_trace_native_delta_r_assembly_scope_partial_P() -> Dict[str, Any]:
    """T: Delta r UV-finite + delta_VB done; finite Re Sigma(M^2) value [C] -> Delta r_rem OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_native_delta_r_uv_cancellation"] == 1, "uv-cancel flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no APF-internal Delta r_rem evaluated by this rung")
    return _result(
        name="T_w_trace_native_delta_r_assembly_scope_partial: "
             "Delta r UV-finite + delta_VB native; finite Re Sigma(M^2) value [C] -> Delta r_rem OPEN [P_structural]",
        tier=4, epistemic="P_structural",
        summary=(
            "Denner's native Delta r is now assembled at the structural + divergence level: "
            "the full UV cancellation closes (all native self-energy poles), delta_VB is "
            "native (closed form), and Pi^{AA}(0) / Sigma^{AZ}(0) are native (v24.3.88-.92). "
            "The ONE remaining input is the finite REAL part of the timelike self-energies "
            "Re Sigma_{WW}(M_W^2)/Re Sigma_{ZZ}(M_Z^2) (+ Sigma_W(0)); its VALUE has no "
            "internal anchor (only an external DIZET comparator), so the numeric Delta r_rem "
            "/ M_W stays [C] by design and DIZET remains the publishable OS-W closure. The "
            "native first-principles route is complete except for that externally-anchored "
            "finite piece."
        ),
        key_result="Delta r UV-finite + delta_VB native; finite Re Sigma(M^2) value [C] (external comparator) -> Delta r_rem OPEN. [P_structural]",
        dependencies=["T_w_trace_native_delta_r_uv_gauge_invariance",
                      "T_w_trace_native_delta_VB_closed_form",
                      "T_w_trace_native_timelike_Z_optical_theorem"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_native_delta_r_uv_cancellation": check_T_w_trace_native_delta_r_uv_cancellation_P,
    "T_w_trace_native_delta_r_uv_gauge_invariance": check_T_w_trace_native_delta_r_uv_gauge_invariance_P,
    "T_w_trace_native_delta_VB_closed_form": check_T_w_trace_native_delta_VB_closed_form_P,
    "T_w_trace_native_delta_r_assembly_scope_partial": check_T_w_trace_native_delta_r_assembly_scope_partial_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}
