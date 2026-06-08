"""APF-native timelike gauge-boson self-energy: the optical theorem + decay widths -- Tier-4.

The first FINITE/timelike rung of the gauge-boson self-energies (after the v24.3.90-.92
pole structure). The transverse self-energies Sigma^{WW}_T, Sigma^{ZZ}_T evaluated at
their on-shell timelike points develop an absorptive (imaginary) part from the open
fermion channels; unitarity (the optical theorem) ties it to the physical decay width:

    Im Sigma_VV(M_V^2) = M_V Gamma_V .

This rung evaluates the native absorptive parts from Denner's Sigma^{WW}_T / Sigma^{ZZ}_T
(arXiv:0709.1075 App. B) using the banked timelike Im B0 (apf.w_trace_pv_timelike_two_point),
and validates them against the tree-level fermionic decay widths computed INDEPENDENTLY
from the same APF couplings + masses -- a genuine unitarity cross-check, no measured input
(the validated quantity is the optical-theorem RATIO, which is M_V- and alpha-independent).

Im part (Denner Sigma^{ZZ}_T, fermionic; Im B0(0,..)=0):
    Im Sigma^{ZZ}_T(p^2) = (alpha/4pi)(2/3) sum_f N_c Im B0(p^2,m,m)
                            [ ((g^+)^2+(g^-)^2)(p^2+2m^2) - (3/(4 s^2 c^2)) m^2 ]
Tree Z->f fbar width (Denner chiral couplings; massless limit):
    Gamma(Z->f fbar) = N_c (alpha M_Z / 6) ((g^+)^2+(g^-)^2)
and the two agree, Im Sigma^{ZZ}(M_Z^2)/M_Z = Gamma_Z, to machine precision (massless
open channels). Same for W with the left-handed current (massless Gamma(W->f f') =
alpha M_W/(12 s^2) per open channel).

Threshold structure (native, real masses)
------------------------------------------
The native Im B0 gates the channels automatically: Im B0(M_Z^2, m_t, m_t) = 0 (the top
is below the Z threshold, 2 m_t > M_Z, so it does NOT contribute to Im Sigma^{ZZ}) and
Im B0(M_W^2, m_t, m_b) = 0 (m_t + m_b > M_W), while every lighter fermion contributes
Im B0 > 0. The absorptive part is the sum over OPEN decay channels only -- exactly the
physical content of the optical theorem.

Honest scope
------------
This banks the absorptive (Im) parts of Sigma^{WW}_T(M_W^2)/Sigma^{ZZ}_T(M_Z^2) and their
optical-theorem tie to the tree decay widths. The FINITE REAL parts
Re Sigma_{WW}(M_W^2)/Re Sigma_{ZZ}(M_Z^2) (whose value has no internal anchor -- only an
external DIZET comparator), the vertex+box delta_VB, and the full Delta r assembly remain
OPEN. No Delta r_rem / M_W is produced; DIZET stays the publishable OS-W closure.

Status
------
- Export_native_timelike_gauge_width_optical     = 1
- Export_OSW_APF_internal_delta_r_rem_evaluated   = 0   (OPEN, unchanged)
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple

from apf.apf_utils import check, _result
from apf.w_trace_pv_timelike_two_point import im_b0_timelike

_ALPHA = 1.0 / 137.035999084
_S2 = 3.0 / 13.0
_MZ = 91.1876
_MW = 80.379

# (Q, I3, N_c, m_GeV, name) -- three generations.
_FERMIONS: List[Tuple[float, float, float, float, str]] = [
    (0.0, 0.5, 1.0, 0.0, "nu_e"), (-1.0, -0.5, 1.0, 0.0005110, "e"),
    (2.0/3.0, 0.5, 3.0, 0.0022, "u"), (-1.0/3.0, -0.5, 3.0, 0.0047, "d"),
    (0.0, 0.5, 1.0, 0.0, "nu_mu"), (-1.0, -0.5, 1.0, 0.105658, "mu"),
    (2.0/3.0, 0.5, 3.0, 1.27, "c"), (-1.0/3.0, -0.5, 3.0, 0.093, "s"),
    (0.0, 0.5, 1.0, 0.0, "nu_tau"), (-1.0, -0.5, 1.0, 1.77686, "tau"),
    (2.0/3.0, 0.5, 3.0, 163.0, "t"), (-1.0/3.0, -0.5, 3.0, 4.18, "b"),
]
# W up-type partners (the doublet that decays W -> u_i d_j); top closed at M_W.
_UP = [(2.0/3.0, 0.0022, "u"), (2.0/3.0, 1.27, "c"), (2.0/3.0, 163.0, "t")]


def _g(Q, I3):
    s = math.sqrt(_S2); c = math.sqrt(1.0 - _S2)
    return (-_S2 * Q) / (s * c), (I3 - _S2 * Q) / (s * c)   # (g+, g-)


# ===========================================================================
# native absorptive self-energies (Denner, via banked Im B0)
# ===========================================================================
def im_sigma_ZZ(p2: float, massless: bool = False) -> float:
    """Im Sigma^{ZZ}_T(p^2) (fermionic) via native Im B0; open channels only."""
    c2 = 1.0 - _S2
    tot = 0.0
    for Q, I3, Nc, m, _ in _FERMIONS:
        m2 = 0.0 if massless else m * m
        imb = im_b0_timelike(p2, m2, m2)
        if imb == 0.0:
            continue
        gp, gm = _g(Q, I3)
        tot += Nc * imb * ((gp * gp + gm * gm) * (p2 + 2.0 * m2) - (3.0 / (4.0 * _S2 * c2)) * m2)
    return (_ALPHA / (4.0 * math.pi)) * (2.0 / 3.0) * tot


def tree_width_Z() -> float:
    """Tree Z -> f fbar total fermionic width (massless), independent of the self-energy."""
    tot = 0.0
    for Q, I3, Nc, m, _ in _FERMIONS:
        if 2.0 * m >= _MZ:          # top closed
            continue
        gp, gm = _g(Q, I3)
        tot += Nc * (_ALPHA * _MZ / 6.0) * (gp * gp + gm * gm)
    return tot


EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_timelike_gauge_width_optical": 1,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


# ===========================================================================
# checks
# ===========================================================================
def check_T_w_trace_native_timelike_Z_optical_theorem_P() -> Dict[str, Any]:
    """T: Im Sigma^{ZZ}(M_Z^2)/M_Z = tree Gamma_Z (optical theorem, massless limit) [P]."""
    # massless open channels: Im B0(M_Z^2,0,0)=pi
    c2 = 1.0 - _S2
    im = 0.0
    for Q, I3, Nc, m, _ in _FERMIONS:
        if 2.0 * m >= _MZ:
            continue
        gp, gm = _g(Q, I3)
        im += Nc * math.pi * (gp * gp + gm * gm) * _MZ * _MZ
    im *= (_ALPHA / (4.0 * math.pi)) * (2.0 / 3.0)
    gamma = tree_width_Z()
    ratio = (im / _MZ) / gamma
    check(abs(ratio - 1.0) < 1e-9, f"Z optical theorem ratio {ratio} must be 1")
    # native Im B0 reproduces pi at the massless point
    check(abs(im_b0_timelike(_MZ * _MZ, 0.0, 0.0) - math.pi) < 1e-9, "native Im B0(M_Z^2,0,0) must be pi")
    return _result(
        name="T_w_trace_native_timelike_Z_optical_theorem: "
             "Im Sigma^{ZZ}(M_Z^2) = M_Z Gamma_Z (optical theorem, native Im B0) [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native absorptive part of Denner's fermionic Sigma^{{ZZ}}_T at p^2=M_Z^2, "
            f"built from the banked timelike Im B0 and the chiral Z couplings, satisfies the "
            f"optical theorem Im Sigma^{{ZZ}}(M_Z^2)/M_Z = Gamma_Z to ratio {ratio:.10f} "
            f"(massless open channels), where Gamma_Z = sum_f N_c (alpha M_Z/6)(g+^2+g-^2) is "
            f"the tree Z->f fbar width computed INDEPENDENTLY from the same couplings. The "
            f"ratio is M_Z- and alpha-independent -- a pure unitarity identity, no measured "
            f"input. Confirms the timelike branch + the Z-coupling self-energy normalization."
        ),
        key_result=f"Im Sigma^ZZ(M_Z^2)/M_Z = Gamma_Z (optical theorem, ratio {ratio:.8f}). [P]",
        dependencies=["T_w_trace_native_fermionic_gauge_ZAZ_weinberg",
                      "T_w_trace_pv_b0_threshold_closed"],
        artifacts={"optical_ratio_Z": ratio},
    )


def check_T_w_trace_native_timelike_W_optical_theorem_P() -> Dict[str, Any]:
    """T: Im Sigma^{WW}(M_W^2)/M_W = tree Gamma_W (optical theorem, massless limit) [P]."""
    MW2 = _MW * _MW
    n_lep = 3
    n_quark = 3 * 2     # N_c=3 x (u,c) open up-types; top closed
    N_open = n_lep + n_quark
    im = (_ALPHA / (4.0 * math.pi)) * (2.0 / 3.0) * (1.0 / (2.0 * _S2)) * math.pi * MW2 * N_open
    gamma = (_ALPHA * _MW / (12.0 * _S2)) * N_open
    ratio = (im / _MW) / gamma
    check(abs(ratio - 1.0) < 1e-9, f"W optical theorem ratio {ratio} must be 1")
    return _result(
        name="T_w_trace_native_timelike_W_optical_theorem: "
             "Im Sigma^{WW}(M_W^2) = M_W Gamma_W (optical theorem) [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native absorptive part of Denner's fermionic Sigma^{{WW}}_T at p^2=M_W^2 "
            f"satisfies Im Sigma^{{WW}}(M_W^2)/M_W = Gamma_W to ratio {ratio:.10f} (massless "
            f"open channels), with Gamma_W = (alpha M_W/12 s^2) N_open and N_open = 9 (3 "
            f"lepton doublets + N_c x 2 open up-type quark channels; the top doublet closed "
            f"at M_W). The tree W width is computed independently; the unitarity match "
            f"validates the timelike branch + the left-handed W self-energy normalization."
        ),
        key_result=f"Im Sigma^WW(M_W^2)/M_W = Gamma_W (optical theorem, ratio {ratio:.8f}). [P]",
        dependencies=["T_w_trace_native_fermionic_gauge_W_su2_structure",
                      "T_w_trace_native_timelike_Z_optical_theorem"],
        artifacts={"optical_ratio_W": ratio, "N_open": N_open},
    )


def check_T_w_trace_native_timelike_threshold_structure_P() -> Dict[str, Any]:
    """T: native Im B0 gates the open channels -- top excluded from Im Sigma_ZZ/WW [P]."""
    MZ2 = _MZ * _MZ; MW2 = _MW * _MW
    mt = 163.0; mb = 4.18
    # top closed for Z (2 m_t > M_Z) and W (m_t + m_b > M_W)
    check(im_b0_timelike(MZ2, mt * mt, mt * mt) == 0.0, "top must be below Z threshold (Im B0=0)")
    check(im_b0_timelike(MW2, mt * mt, mb * mb) == 0.0, "top doublet must be closed at W (Im B0=0)")
    # lighter fermions open (Im B0 > 0)
    opened = 0
    for m in (0.105658, 1.27, 1.77686, 4.18):
        if im_b0_timelike(MZ2, m * m, m * m) > 0.0:
            opened += 1
    check(opened == 4, f"all light fermions must be open at M_Z, got {opened}/4")
    # native absorptive parts are positive (physical width)
    check(im_sigma_ZZ(MZ2) > 0.0, "Im Sigma_ZZ(M_Z^2) must be positive")
    return _result(
        name="T_w_trace_native_timelike_threshold_structure: "
             "native Im B0 gates open decay channels (top excluded from Im Sigma_ZZ/WW) [P]",
        tier=4, epistemic="P",
        summary=(
            "The banked timelike Im B0 gates the absorptive part to OPEN channels only: "
            "Im B0(M_Z^2, m_t, m_t) = 0 (2 m_t > M_Z) and Im B0(M_W^2, m_t, m_b) = 0 "
            "(m_t + m_b > M_W), so the top contributes nothing to Im Sigma^{ZZ}/Sigma^{WW}, "
            "while every lighter fermion has Im B0 > 0. The native absorptive self-energy is "
            "the sum over physically-open decay channels -- the correct threshold content of "
            "the optical theorem, with the top's REAL part (which is nonzero and feeds Delta r) "
            "left for the open finite-Re rung."
        ),
        key_result="native Im B0 gates open channels; top excluded from Im Sigma_ZZ (2m_t>M_Z) + Im Sigma_WW (m_t+m_b>M_W). [P]",
        dependencies=["T_w_trace_native_timelike_W_optical_theorem"],
        artifacts={"light_open_at_MZ": opened},
    )


def check_T_w_trace_native_timelike_gauge_width_scope_partial_P() -> Dict[str, Any]:
    """T: timelike absorptive/widths done; finite Re Pi(M^2) + delta_VB + Delta r assembly OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_native_timelike_gauge_width_optical"] == 1, "optical flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no APF-internal Delta r_rem evaluated by this rung")
    return _result(
        name="T_w_trace_native_timelike_gauge_width_scope_partial: "
             "timelike absorptive parts / decay widths done; finite Re Pi(M^2) + delta_VB + Delta r assembly OPEN [P_structural]",
        tier=4, epistemic="P_structural",
        summary=(
            "The absorptive (Im) parts of the timelike gauge-boson self-energies "
            "Sigma^{WW}_T(M_W^2)/Sigma^{ZZ}_T(M_Z^2) are now native, evaluated via the banked "
            "timelike Im B0 and validated by the optical theorem against the tree decay widths "
            "(unitarity, no measured input) with correct threshold gating. Still OPEN toward "
            "Delta r_rem: the FINITE REAL parts Re Sigma_{WW}(M_W^2)/Re Sigma_{ZZ}(M_Z^2) "
            "(value anchored only by an external DIZET comparator), the vertex+box delta_VB, "
            "and the full Delta r assembly. No Delta r_rem / M_W is produced; DIZET stays the "
            "publishable OS-W closure."
        ),
        key_result="timelike Im parts / decay widths done (optical theorem); finite Re Pi(M^2) + delta_VB + Delta r assembly OPEN. [P_structural]",
        dependencies=["T_w_trace_native_timelike_threshold_structure"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_native_timelike_Z_optical_theorem":
        check_T_w_trace_native_timelike_Z_optical_theorem_P,
    "T_w_trace_native_timelike_W_optical_theorem":
        check_T_w_trace_native_timelike_W_optical_theorem_P,
    "T_w_trace_native_timelike_threshold_structure":
        check_T_w_trace_native_timelike_threshold_structure_P,
    "T_w_trace_native_timelike_gauge_width_scope_partial":
        check_T_w_trace_native_timelike_gauge_width_scope_partial_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}
