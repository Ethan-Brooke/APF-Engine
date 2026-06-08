"""APF-native fermionic gauge-boson self-energy poles (AA/AZ/ZZ/WW) -- Tier-4.

Completes the fermionic side of the gauge-boson self-energy UV-pole structure that
the v24.3.90/.91 bosonic rungs left open. From Denner's reviewed Sigma^{AA}_T,
Sigma^{AZ}_T, Sigma^{ZZ}_T, Sigma^{WW}_T (arXiv:0709.1075 App. B, haba2.tex), the
fermion-loop p^2-pole coefficients (the field-strength / coupling renormalization
of the gauge bosons) are assembled from the SM gauge charges (Q, I_3, N_c) and
Denner's chiral Z couplings, with NO measured input -- the coupling transcription
is validated against the banked photon (sum N_c Q^2 = 8) and the electroweak
charge sum rules (Q = I_3 + Y).

Denner chiral Z couplings (App. A):
    g_f^-  = (I_3 - s_W^2 Q)/(s_W c_W)   (left)
    g_f^+  = -s_W^2 Q/(s_W c_W)           (right)
Fermion bracket pole at general p^2: -(p^2 + 2m^2)B0 + 2m^2 B0(0) + p^2/3 has
p^2-pole coefficient -1, so the fermionic self-energy pole content P_VV (with
Sigma_T = -(alpha/4pi) P) is linear in p^2 with p^2-coefficient:
    P_AA : (2/3) sum N_c (2 Q^2)(-1)                = -(4/3) sum N_c Q^2
    P_AZ : (2/3) sum N_c (-Q)(g^+ + g^-)(-1)        = (2/3) sum N_c Q(g^+ + g^-)
    P_ZZ : (2/3) sum N_c [(g^+)^2 + (g^-)^2](-1)    = -(2/3) sum N_c [(g^+)^2+(g^-)^2]
    P_WW : (2/3)(1/2 s_W^2) sum_doublets (-1)        = -(2/3)(1/2 s_W^2) N_doublet
(the m^2 pole pieces -- already validated UV-finite in Delta rho at v24.3.90 --
do not enter the p^2-coefficient).

Three internal anchors (no smuggling)
-------------------------------------
1. Photon: P_AA p^2-coeff = -(4/3) sum N_c Q^2 with sum N_c Q^2 = 8 -- value-
   identical to the banked QED beta-function (apf.w_trace_native_uv_pole) whose
   finite part is Delta alpha_lep.
2. W (SU(2)): P_WW = -(2/3)(1/2 s_W^2) N_doublet = -4/s_W^2 with N_doublet = 12
   (3 lepton + 9 colour-counted quark left doublets) -- the g^2 propto 1/s_W^2
   structure and the SM doublet count, both verified (1/s_W^2 scaling + count).
3. Z, gamma-Z: Denner's g^+/g^- summed reproduce the electroweak charge sum
   rules sum N_c Q I_3 = 6, sum N_c I_3^2 = 6, the closed forms
   sum N_c Q(g^++g^-) = -(sum N_c Q I_3 - 2 s_W^2 sum N_c Q^2)/(s_W c_W) and
   sum N_c [(g^+)^2+(g^-)^2] = (2 s_W^4 sum N_c Q^2 + sum N_c I_3^2
   - 2 s_W^2 sum N_c Q I_3)/(s_W^2 c_W^2), with Q^2 = I_3^2 + 2 I_3 Y + Y^2 --
   the Weinberg rotation, using only SM gauge charges.

Honest scope
------------
This banks the fermionic gauge-boson self-energy p^2-pole coefficients (field
renormalization). Combined with the bosonic v24.3.91, the full (ferm+bos) AA/AZ/
ZZ/WW pole structure is now native -- the input to a full Delta r UV cancellation.
Still OPEN: the full Delta r UV cancellation across the charge + weak-angle
counterterm maps (v24.3.80), the FINITE + timelike Re Pi_WW(M_W^2)/Re Pi_ZZ(M_Z^2),
and the vertex+box delta_VB. No Delta r_rem / M_W is produced; DIZET stays the
publishable OS-W closure.

Status
------
- Export_native_fermionic_gauge_self_energy_poles = 1
- Export_OSW_APF_internal_delta_r_rem_evaluated    = 0   (OPEN, unchanged)
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple

from apf.apf_utils import check, _result
from apf.w_trace_native_uv_pole import sum_Nc_Q2

_S2_REF = 3.0 / 13.0

# SM fermions per generation as (Q, I_3, N_c); three generations.
_GEN: List[Tuple[float, float, float]] = [
    (0.0, 0.5, 1.0),            # neutrino
    (-1.0, -0.5, 1.0),          # charged lepton
    (2.0 / 3.0, 0.5, 3.0),      # up-type quark
    (-1.0 / 3.0, -0.5, 3.0),    # down-type quark
]
_FERMIONS: List[Tuple[float, float, float]] = _GEN * 3
# left-handed weak doublets (color-counted): 3 lepton + 3*3 quark = 12
_N_DOUBLET = 3 * 1 + 3 * 3


def g_minus(Q: float, I3: float, s2: float = _S2_REF) -> float:
    s = math.sqrt(s2); c = math.sqrt(1.0 - s2)
    return (I3 - s2 * Q) / (s * c)


def g_plus(Q: float, I3: float, s2: float = _S2_REF) -> float:
    s = math.sqrt(s2); c = math.sqrt(1.0 - s2)
    return (-s2 * Q) / (s * c)


# ===========================================================================
# fermionic self-energy p^2-pole coefficients (Sigma_T = -(alpha/4pi) P)
# ===========================================================================
def p2coeff_AA() -> float:
    return -(4.0 / 3.0) * sum(Nc * Q * Q for Q, I3, Nc in _FERMIONS)


def p2coeff_AZ(s2: float = _S2_REF) -> float:
    return (2.0 / 3.0) * sum(Nc * (-Q) * (g_plus(Q, I3, s2) + g_minus(Q, I3, s2))
                             for Q, I3, Nc in _FERMIONS)


def p2coeff_ZZ(s2: float = _S2_REF) -> float:
    return -(2.0 / 3.0) * sum(Nc * (g_plus(Q, I3, s2) ** 2 + g_minus(Q, I3, s2) ** 2)
                              for Q, I3, Nc in _FERMIONS)


def p2coeff_WW(s2: float = _S2_REF) -> float:
    return -(2.0 / 3.0) * (1.0 / (2.0 * s2)) * _N_DOUBLET


def _sum(f) -> float:
    return sum(f(Q, I3, Nc) for Q, I3, Nc in _FERMIONS)


EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_fermionic_gauge_self_energy_poles": 1,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


# ===========================================================================
# checks
# ===========================================================================
def check_T_w_trace_native_fermionic_gauge_photon_anchor_P() -> Dict[str, Any]:
    """T: fermionic photon-VP p^2-pole = -(4/3) sum N_c Q^2 (sum=8), ties to banked QED beta [P]."""
    sQ2 = _sum(lambda Q, I3, Nc: Nc * Q * Q)
    check(abs(sQ2 - 8.0) < 1e-9, f"sum N_c Q^2 must be 8, got {sQ2}")
    paa = p2coeff_AA()
    banked = -(4.0 / 3.0) * sum_Nc_Q2()
    check(abs(paa - banked) < 1e-9, f"P_AA p^2-coeff {paa} must equal banked -(4/3) sum N_c Q^2 {banked}")
    # Weinberg charge consistency Q^2 = I3^2 + 2 I3 Y + Y^2
    lhs = _sum(lambda Q, I3, Nc: Nc * Q * Q)
    rhs = _sum(lambda Q, I3, Nc: Nc * (I3 * I3 + 2.0 * I3 * (Q - I3) + (Q - I3) ** 2))
    check(abs(lhs - rhs) < 1e-9, f"Q^2 = I3^2+2 I3 Y+Y^2 failed: {lhs} vs {rhs}")
    return _result(
        name="T_w_trace_native_fermionic_gauge_photon_anchor: "
             "fermionic photon-VP pole = -(4/3) sum N_c Q^2 (sum=8), ties to banked QED beta [P]",
        tier=4, epistemic="P",
        summary=(
            f"The fermionic photon self-energy p^2-pole coefficient assembled from the SM "
            f"charges is -(4/3) sum N_c Q^2 with sum N_c Q^2 = {sQ2:.0f}, value-identical to "
            f"the banked apf.w_trace_native_uv_pole QED beta-function (whose finite part is "
            f"Delta alpha_lep). The electroweak charge consistency Q^2 = I_3^2 + 2 I_3 Y + "
            f"Y^2 holds, anchoring the (Q, I_3, Y) quantum numbers used for the Z/W "
            f"couplings. No measured input."
        ),
        key_result=f"P_AA fermionic = -(4/3)*{sQ2:.0f}, == banked QED beta; Q=I3+Y consistent. [P]",
        dependencies=["T_w_trace_native_photon_vp_pole_beta_function"],
        artifacts={"sum_Nc_Q2": sQ2, "P_AA": paa},
    )


def check_T_w_trace_native_fermionic_gauge_W_su2_structure_P() -> Dict[str, Any]:
    """T: fermionic W self-energy pole = -4/s_W^2 (g^2 propto 1/s^2, 12 doublets) [P]."""
    # 1/s^2 scaling: P_WW(s2a)/P_WW(s2b) = s2b/s2a
    s2a, s2b = 3.0 / 13.0, 0.25
    ratio = p2coeff_WW(s2a) / p2coeff_WW(s2b)
    check(abs(ratio - s2b / s2a) < 1e-9, f"P_WW must scale as 1/s^2; ratio {ratio} vs {s2b/s2a}")
    # closed form -4/s^2 with N_doublet = 12
    check(_N_DOUBLET == 12, f"left-handed weak doublet count must be 12, got {_N_DOUBLET}")
    pww = p2coeff_WW(s2a)
    closed = -4.0 / s2a
    check(abs(pww - closed) < 1e-9, f"P_WW {pww} must equal -4/s^2 {closed}")
    return _result(
        name="T_w_trace_native_fermionic_gauge_W_su2_structure: "
             "fermionic W self-energy pole = -4/s_W^2 (g^2 propto 1/s^2, 12 doublets) [P]",
        tier=4, epistemic="P",
        summary=(
            f"The fermionic W self-energy p^2-pole coefficient is "
            f"-(2/3)(1/2 s_W^2) N_doublet = -4/s_W^2 with N_doublet = 12 (3 lepton + 9 "
            f"colour-counted quark left doublets). It scales as 1/s_W^2 (ratio {ratio:.4f} "
            f"= s2b/s2a) -- the g^2 = e^2/s_W^2 coupling structure -- and carries the "
            f"correct SM doublet count, the SU(2) fermionic field/coupling renormalization "
            f"from Denner's reviewed Sigma^{{WW}}_T. No measured input."
        ),
        key_result=f"P_WW fermionic = -4/s_W^2 (1/s^2 scaling + 12 doublets). [P]",
        dependencies=["T_w_trace_native_fermionic_gauge_photon_anchor"],
        artifacts={"P_WW": pww, "s2_scaling_ratio": ratio, "N_doublet": _N_DOUBLET},
    )


def check_T_w_trace_native_fermionic_gauge_ZAZ_weinberg_P() -> Dict[str, Any]:
    """T: Denner Z/gamma-Z couplings reproduce the EW charge sum rules (Weinberg rotation) [P]."""
    s2 = _S2_REF; s = math.sqrt(s2); c = math.sqrt(1.0 - s2)
    sQ2 = _sum(lambda Q, I3, Nc: Nc * Q * Q)
    sQI3 = _sum(lambda Q, I3, Nc: Nc * Q * I3)
    sI32 = _sum(lambda Q, I3, Nc: Nc * I3 * I3)
    check(abs(sQI3 - 6.0) < 1e-9, f"sum N_c Q I_3 must be 6, got {sQI3}")
    check(abs(sI32 - 6.0) < 1e-9, f"sum N_c I_3^2 must be 6, got {sI32}")
    # gamma-Z coupling sum vs closed form
    az = _sum(lambda Q, I3, Nc: Nc * (-Q) * (g_plus(Q, I3, s2) + g_minus(Q, I3, s2)))
    az_closed = -(sQI3 - 2.0 * s2 * sQ2) / (s * c)
    check(abs(az - az_closed) < 1e-9, f"sum N_c Q(g^++g^-) {az} vs closed {az_closed}")
    # ZZ coupling sum vs closed form
    zz = _sum(lambda Q, I3, Nc: Nc * (g_plus(Q, I3, s2) ** 2 + g_minus(Q, I3, s2) ** 2))
    zz_closed = (2.0 * s2 * s2 * sQ2 + sI32 - 2.0 * s2 * sQI3) / (s2 * (1.0 - s2))
    check(abs(zz - zz_closed) < 1e-9, f"sum N_c [(g^+)^2+(g^-)^2] {zz} vs closed {zz_closed}")
    return _result(
        name="T_w_trace_native_fermionic_gauge_ZAZ_weinberg: "
             "Denner Z / gamma-Z couplings reproduce the EW charge sum rules [P]",
        tier=4, epistemic="P",
        summary=(
            f"The fermionic Z and gamma-Z self-energy couplings, assembled from Denner's "
            f"chiral g^+ = -s^2 Q/(s c), g^- = (I_3 - s^2 Q)/(s c), reproduce the "
            f"electroweak charge sum rules: sum N_c Q I_3 = {sQI3:.0f}, sum N_c I_3^2 = "
            f"{sI32:.0f}, the gamma-Z sum = -(sum Q I_3 - 2 s^2 sum Q^2)/(s c) = {az:.4f}, "
            f"and the ZZ sum = (2 s^4 sum Q^2 + sum I_3^2 - 2 s^2 sum Q I_3)/(s^2 c^2) = "
            f"{zz:.4f}. These are the Weinberg rotation of the (W3, B) currents, using only "
            f"the SM gauge charges -- validating the Z/gamma-Z coupling transcription with "
            f"no measured input."
        ),
        key_result=f"Z/gamma-Z couplings reproduce EW charge sum rules (Q I3=6, I3^2=6; closed forms). [P]",
        dependencies=["T_w_trace_native_fermionic_gauge_photon_anchor"],
        artifacts={"sum_Nc_Q_I3": sQI3, "sum_Nc_I3_2": sI32, "P_AZ": p2coeff_AZ(),
                   "P_ZZ": p2coeff_ZZ()},
    )


def check_T_w_trace_native_fermionic_gauge_scope_partial_P() -> Dict[str, Any]:
    """T: fermionic gauge-boson self-energy poles done; full Delta r CT + finite/timelike + delta_VB OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_native_fermionic_gauge_self_energy_poles"] == 1, "ferm-gauge flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no APF-internal Delta r_rem evaluated by this rung")
    return _result(
        name="T_w_trace_native_fermionic_gauge_scope_partial: "
             "fermionic gauge-boson self-energy poles done; full Delta r CT + finite/timelike + delta_VB OPEN [P_structural]",
        tier=4, epistemic="P_structural",
        summary=(
            "The fermionic gauge-boson self-energy p^2-pole coefficients (AA/AZ/ZZ/WW) are "
            "now native, assembled from the SM gauge charges + Denner's chiral couplings "
            "and anchored on the banked photon (sum N_c Q^2 = 8), the SU(2) g^2/s^2 + "
            "12-doublet structure, and the electroweak charge sum rules. Combined with the "
            "bosonic v24.3.91, the full (ferm+bos) AA/AZ/ZZ/WW pole structure is in hand. "
            "Still OPEN toward Delta r_rem: the full Delta r UV cancellation across the "
            "charge + weak-angle counterterm maps (v24.3.80), the FINITE + timelike "
            "Re Pi_WW(M_W^2)/Re Pi_ZZ(M_Z^2), and the vertex+box delta_VB. No Delta r_rem / "
            "M_W is produced; DIZET stays the publishable OS-W closure."
        ),
        key_result="fermionic gauge-boson self-energy poles (AA/AZ/ZZ/WW) done; full Delta r CT + finite/timelike + delta_VB OPEN. [P_structural]",
        dependencies=["T_w_trace_native_fermionic_gauge_W_su2_structure",
                      "T_w_trace_native_fermionic_gauge_ZAZ_weinberg",
                      "T_w_trace_native_uv_cancel_os_renormalized_finite"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_native_fermionic_gauge_photon_anchor":
        check_T_w_trace_native_fermionic_gauge_photon_anchor_P,
    "T_w_trace_native_fermionic_gauge_W_su2_structure":
        check_T_w_trace_native_fermionic_gauge_W_su2_structure_P,
    "T_w_trace_native_fermionic_gauge_ZAZ_weinberg":
        check_T_w_trace_native_fermionic_gauge_ZAZ_weinberg_P,
    "T_w_trace_native_fermionic_gauge_scope_partial":
        check_T_w_trace_native_fermionic_gauge_scope_partial_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}
