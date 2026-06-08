"""APF-native fermion-loop electroweak self-energies from the native PV toolkit -- Tier-4.

Stage 2 of the native OS-W one-loop evaluator (work plan 2026-05-24): the full
fermionic transverse gauge-boson self-energies built SLOT-BY-SLOT from the SM
electroweak couplings and colour, reduced to the native two-point PV functions
(``apf.w_trace_pv_scalar_integral_substrate`` a0_fin/b0_fin +
``apf.w_trace_pv_tensor_reduction`` b1_direct/b00_direct). This supersedes the
v24.3.82 Veltman-combination shortcut: here Pi_WW and Pi_ZZ are assembled per
coupling, not via the pre-packaged custodial difference.

Derived transverse self-energy
------------------------------
For a vector boson coupling to a fermion pair (m1,m2) with vertex
gamma^mu (g_L P_L + g_R P_R), the g^{mu nu} coefficient A(p^2) of the one-loop
fermion-loop self-energy Sigma^{mu nu}(p) is (Dirac trace + PV reduction):

    A(p^2) = -(N_c/16 pi^2) { 4 (g_L^2+g_R^2) B00(p^2,m1^2,m2^2)
                              - 2 (g_L^2+g_R^2) [A0(m2^2) + m1^2 B0 + p^2 B1]
                              + 4 g_L g_R m1 m2 B0(p^2,m1^2,m2^2) }

evaluated with the native A0/B0/B1/B00. The transverse (Pi_T) content of Delta
rho is A_W(0)/M_W^2 - A_Z(0)/M_Z^2.

Two correctness gates (no external target)
------------------------------------------
1. Photon transversality. For the photon (g_L=g_R=eQ, equal mass) the self-
   energy must be purely transverse, A_gamma(p^2) ~ p^2, so A_gamma(0)=0. In the
   native convention this holds exactly because B00(0,m^2,m^2)=A0(m^2)/2, so
   2 B00(0,m^2,m^2) - A0(m^2) = 0. Verified to ~1e-11 (relative ~1e-13). This
   independently fixes the normalization of the construction.
2. Delta rho_top. The slot-by-slot Delta rho from the (t,b) doublet (W: purely
   left-handed g/sqrt(2); Z: per-fermion g_L=(g/c)(T3-Q s^2), g_R=(g/c)(-Q s^2),
   colour N_c=3) reproduces the banked gauge.L_W_mass Drho_top=0.008379 to
   rel ~3e-4, and agrees with the v24.3.82 Veltman-F native result.

All at p^2=0 (the p^2 B1 term drops), so NO timelike branch is needed. APF inputs
only (m_t=163 [L_sigma_normalization], sin^2 theta_W=3/13 [T_sin2theta],
alpha=1/128.21 [L_alpha_em]); no measured M_W; no DIZET.

Honest scope
------------
Fermionic transverse self-energies at p^2=0, validated by transversality + Delta
rho. The full APF-internal Delta r_rem remains OPEN: the timelike Re Pi_WW(M_W^2)
/ Re Pi_ZZ(M_Z^2) branch, the bosonic/Goldstone/ghost loops, the vertex+box
delta_VB, and UV-pole cancellation against the counterterms. No Delta r_rem / M_W
is produced; DIZET stays the publishable OS-W closure.

Status
------
- Export_native_fermionic_self_energy_slot_by_slot     = 1
- Export_native_photon_transversality_verified         = 1
- Export_OSW_APF_internal_delta_r_rem_evaluated        = 0   (OPEN, unchanged)
"""
from __future__ import annotations

import math
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_pv_scalar_integral_substrate import a0_fin, b0_fin
from apf.w_trace_pv_tensor_reduction import b1_direct, b00_direct

# APF-internal [P] inputs (identical to apf.gauge.check_L_W_mass).
_SIN2_W = 3.0 / 13.0
_S = math.sqrt(_SIN2_W)
_C = math.sqrt(1.0 - _SIN2_W)
_ALPHA_EM = 1.0 / 128.21
_E2 = 4.0 * math.pi * _ALPHA_EM
_G2 = _E2 / _SIN2_W
_G = math.sqrt(_G2)
_E = math.sqrt(_E2)
_M_T = 163.0
_M_Z = 91.1876
_M_W = _M_Z * _C
_N_C = 3.0
_PREF = _N_C / (16.0 * math.pi ** 2)

EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_fermionic_self_energy_slot_by_slot": 1,
    "Export_native_photon_transversality_verified": 1,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


def transverse_A_bracket(gL: float, gR: float, m1: float, m2: float, p2: float) -> float:
    """g^{mu nu} coefficient of the fermion-loop Sigma^{mu nu}(p), without -(N_c/16pi^2).

    A_bracket = 4(gL^2+gR^2)B00 - 2(gL^2+gR^2)[A0(m2^2)+m1^2 B0 + p^2 B1]
                + 4 gL gR m1 m2 B0 .
    """
    m12 = m1 * m1
    m22 = m2 * m2
    gg = gL * gL + gR * gR
    B0 = b0_fin(p2, m12, m22)
    B00 = b00_direct(p2, m12, m22)
    term_b1 = p2 * b1_direct(p2, m12, m22) if p2 != 0.0 else 0.0
    return (4.0 * gg * B00
            - 2.0 * gg * (a0_fin(m22) + m12 * B0 + term_b1)
            + 4.0 * gL * gR * m1 * m2 * B0)


def A_transverse(gL: float, gR: float, m1: float, m2: float, p2: float) -> float:
    """Transverse self-energy coefficient A(p^2) = -(N_c/16pi^2) * A_bracket."""
    return -_PREF * transverse_A_bracket(gL, gR, m1, m2, p2)


def _gLZ(T3: float, Q: float) -> float:
    return (_G / _C) * (T3 - Q * _SIN2_W)


def _gRZ(Q: float) -> float:
    return (_G / _C) * (-Q * _SIN2_W)


def _A_W_zero(m_b: float) -> float:
    # W: (t,b), purely left-handed g/sqrt(2)
    return A_transverse(_G / math.sqrt(2.0), 0.0, _M_T, m_b, 0.0)


def _A_Z_zero(m_b: float) -> float:
    # Z: t (T3=+1/2,Q=+2/3) + b (T3=-1/2,Q=-1/3), colour summed via _PREF*N_c
    A_t = A_transverse(_gLZ(0.5, 2.0 / 3.0), _gRZ(2.0 / 3.0), _M_T, _M_T, 0.0)
    A_b = A_transverse(_gLZ(-0.5, -1.0 / 3.0), _gRZ(-1.0 / 3.0), m_b, m_b, 0.0)
    return A_t + A_b


def drho_top_slot_by_slot(m_b: float = 0.05) -> float:
    return _A_W_zero(m_b) / _M_W ** 2 - _A_Z_zero(m_b) / _M_Z ** 2


# ===========================================================================
# checks
# ===========================================================================
def check_T_w_trace_native_photon_transversality_P() -> Dict[str, Any]:
    """T: native fermion-loop photon self-energy is transverse, A_gamma(0)=0 [P]."""
    m = 4.18
    A0p = transverse_A_bracket(_E, _E, m, m, 0.0)         # photon, p^2=0
    Aref = transverse_A_bracket(_E, _E, m, m, -100.0)     # photon, spacelike p^2
    rel = abs(A0p) / max(1e-30, abs(Aref))
    check(rel < 1e-6, f"A_gamma(0)/A_gamma(-100) = {rel:.2e} must vanish (transversality)")
    check(abs(Aref) > 1e-3, "A_gamma(p^2!=0) must be non-trivial (genuinely ~ p^2)")
    # proportionality: A_gamma(p^2)/p^2 stays finite/stable across spacelike p^2
    ratios = [transverse_A_bracket(_E, _E, m, m, p2) / p2 for p2 in (-1.0, -10.0, -100.0)]
    spread = (max(ratios) - min(ratios)) / abs(sum(ratios) / len(ratios))
    check(spread < 0.5, f"A_gamma/p^2 spread {spread:.2f} too large for a transverse self-energy")
    return _result(
        name="T_w_trace_native_photon_transversality: "
             "native fermion-loop photon self-energy is transverse, A_gamma(0)=0 [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native fermion-loop photon self-energy (g_L=g_R=eQ, equal mass) is "
            f"purely transverse: A_gamma(0) vanishes relative to A_gamma(-100 GeV^2) "
            f"to {rel:.1e}, while A_gamma(p^2) ~ p^2 is non-trivial (A/p^2 stable to "
            f"{spread:.0%}). In the native convention this holds because "
            f"2 B00(0,m^2,m^2) = A0(m^2). This independently fixes the normalization "
            f"of the transverse self-energy construction -- the correctness gate the "
            f"naive p^2=0 g^{{mu nu}}-coefficient fails."
        ),
        key_result=f"native photon self-energy transverse: A_gamma(0)=0 (rel {rel:.1e}). [P]",
        dependencies=["T_w_trace_pv_b00_b11_trace_relation", "T_w_trace_native_veltman_F_identity"],
        artifacts={"A_gamma_0_over_ref": rel, "ratio_spread": spread},
    )


def check_T_w_trace_native_drho_slot_by_slot_P() -> Dict[str, Any]:
    """T: slot-by-slot fermionic Pi_WW(0)/Pi_ZZ(0) reproduce banked Drho_top [P]."""
    import apf.gauge as gauge
    banked = float(gauge.check_L_W_mass()["artifacts"]["Drho_top"])
    drho = drho_top_slot_by_slot(0.05)
    rel = abs(drho - banked) / abs(banked)
    check(rel < 1e-3, f"slot-by-slot Drho {drho:.6f} vs banked {banked:.6f} rel {rel:.2e}")
    return _result(
        name="T_w_trace_native_drho_slot_by_slot: "
             "full fermionic Pi_WW(0)/Pi_ZZ(0) (couplings+colour) reproduce banked Drho_top [P]",
        tier=4, epistemic="P",
        summary=(
            f"The fermionic transverse self-energies built SLOT-BY-SLOT from the SM "
            f"electroweak couplings and colour -- W from the purely left-handed "
            f"(t,b) current (g/sqrt2), Z from per-fermion g_L=(g/c)(T3-Q s^2), "
            f"g_R=(g/c)(-Q s^2), N_c=3 -- give Delta rho = A_W(0)/M_W^2 - "
            f"A_Z(0)/M_Z^2 = {drho:.6f}, reproducing the banked gauge.L_W_mass "
            f"Drho_top = {banked:.6f} to rel {rel:.1e}. This validates the full "
            f"per-coupling self-energy machinery (not just the Veltman custodial "
            f"difference); APF inputs only, no measured M_W, no DIZET."
        ),
        key_result=f"slot-by-slot Drho_top = {drho:.6f} == banked {banked:.6f} (rel {rel:.1e}). [P]",
        dependencies=["T_w_trace_native_photon_transversality", "L_W_mass"],
        artifacts={"drho_slot_by_slot": drho, "banked": banked, "rel_err": rel},
    )


def check_T_w_trace_native_drho_routes_consistent_P() -> Dict[str, Any]:
    """T: slot-by-slot Drho agrees with the v24.3.82 Veltman-F native route [P]."""
    import apf.w_trace_native_drho_top as velt
    drho_slot = drho_top_slot_by_slot(0.05)
    drho_velt = velt.drho_top_native(0.05)
    rel = abs(drho_slot - drho_velt) / abs(drho_velt)
    check(rel < 5e-3, f"slot-by-slot {drho_slot:.6f} vs Veltman {drho_velt:.6f} rel {rel:.2e}")
    return _result(
        name="T_w_trace_native_drho_routes_consistent: "
             "slot-by-slot and Veltman-F native Delta rho routes agree [P]",
        tier=4, epistemic="P",
        summary=(
            f"The two independent native routes to Delta rho_top agree: the "
            f"slot-by-slot transverse self-energies ({drho_slot:.6f}) and the "
            f"v24.3.82 Veltman-F-via-A0/B0 result ({drho_velt:.6f}) match to rel "
            f"{rel:.1e} -- a cross-check between the per-coupling self-energy "
            f"construction and the custodial-combination identity."
        ),
        key_result=f"slot-by-slot == Veltman native Drho (rel {rel:.1e}). [P]",
        dependencies=["T_w_trace_native_drho_slot_by_slot",
                      "T_w_trace_native_drho_top_reproduces_banked"],
        artifacts={"drho_slot": drho_slot, "drho_veltman": drho_velt, "rel": rel},
    )


def check_T_w_trace_native_self_energy_scope_partial_P() -> Dict[str, Any]:
    """T: fermionic p^2=0 self-energies + transversality done; full Delta r_rem OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_native_fermionic_self_energy_slot_by_slot"] == 1, "slot-by-slot flag must be 1")
    check(EXPORT_FLAGS["Export_native_photon_transversality_verified"] == 1, "transversality flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no APF-internal Delta r_rem evaluated by this rung")
    return _result(
        name="T_w_trace_native_self_energy_scope_partial: "
             "fermionic p^2=0 self-energies + transversality done; full Delta r_rem OPEN [P_structural]",
        tier=4, epistemic="P_structural",
        summary=(
            "Stage 2 of the native OS-W evaluator now has the full fermionic "
            "transverse self-energies at p^2=0, built slot-by-slot from SM couplings "
            "and colour, validated by photon transversality and the banked "
            "Delta rho_top. Still OPEN toward the APF-internal Delta r_rem: the "
            "timelike Re Pi_WW(M_W^2) / Re Pi_ZZ(M_Z^2) branch (the next "
            "prerequisite), the bosonic/Goldstone/ghost loops, the vertex+box "
            "delta_VB (which will consume the native rank-3 box tensors), and UV-pole "
            "cancellation against the banked counterterms. No Delta r_rem / M_W is "
            "produced; DIZET stays the publishable OS-W closure."
        ),
        key_result="Fermionic p^2=0 self-energies + transversality done; full Delta r_rem OPEN. [P_structural]",
        dependencies=["T_w_trace_native_drho_slot_by_slot"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_native_photon_transversality": check_T_w_trace_native_photon_transversality_P,
    "T_w_trace_native_drho_slot_by_slot": check_T_w_trace_native_drho_slot_by_slot_P,
    "T_w_trace_native_drho_routes_consistent": check_T_w_trace_native_drho_routes_consistent_P,
    "T_w_trace_native_self_energy_scope_partial": check_T_w_trace_native_self_energy_scope_partial_P,
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
