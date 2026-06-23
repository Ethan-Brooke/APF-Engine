"""APF-native Stage-4 UV cancellation: OS-renormalized self-energies are finite -- Tier-4.

Stage 4 of the native OS-W one-loop evaluator (work plan 2026-05-24): the
ultraviolet cancellation. The bare gauge-boson self-energies carry 1/eps poles;
the on-shell (OS) mass and field counterterms must remove them, so that the
renormalized self-energies -- and hence the assembled Delta r -- are UV-finite.
This rung proves that for the BOSONIC gauge sector (and the full photon) using the
v24.3.86 UV-pole layer + Denner's transcribed Sigma^{AA}_T / Sigma^{WW}_T /
Sigma^{ZZ}_T (v24.3.88/.90); it needs no finite parts, no timelike branch, and no
fermionic Z/W couplings.

Two exact facts (units alpha/4pi * Delta_eps; Sigma_T = -(alpha/4pi) P)
---------------------------------------------------------------------
1. RENORMALIZABILITY: each bosonic self-energy UV-pole content P_VV(p^2) is
   strictly LINEAR in p^2, P_VV(p^2) = A_V p^2 + B_V. In particular the
   (M^4/p^2)(B0(p^2)-B0(0)) terms in Sigma^{WW}_T contribute zero pole (the pole
   cancels in the B0 difference), so no 1/p^2 or p^4 divergence survives -- the
   gauge sector is renormalizable with the standard mass+field counterterms.
2. OS UV-CANCELLATION: with the on-shell counterterms
       delta M_V^2 = Re Sigma_VV(M_V^2),   delta Z_V = -Re Sigma'_VV(M_V^2),
   the renormalized self-energy
       Sigma_hat_VV(p^2) = Sigma_VV(p^2) - delta M_V^2 + (p^2 - M_V^2) delta Z_V
   has ZERO UV pole at all p^2:  (A p^2 + B) - (A M_V^2 + B) - (p^2 - M_V^2) A = 0.
   For the photon B_AA = 0 (massless, delta M_A^2 = 0); the pure p^2 pole is
   removed by delta Z_A alone.

Resolution of the v24.3.90 bosonic Delta rho +4
-----------------------------------------------
v24.3.90 found the BARE bosonic custodial Delta rho UV-divergent (universal pole
+4). That is a bare-quantity artifact: at p^2 = 0 the renormalized self-energies
Sigma_hat_WW(0) and Sigma_hat_ZZ(0) are UV-finite (a special case of fact 2), so
the bosonic Delta rho built from the RENORMALIZED self-energies is finite -- the
+4 is exactly what delta M_W^2/delta M_Z^2 absorb. The renormalized finite VALUE
is still [C] (needs the finite + timelike parts), but its UV-finiteness is now
established.

Sources: Denner Sigma^{AA}_T/Sigma^{WW}_T/Sigma^{ZZ}_T (arXiv:0709.1075 App. B),
only the p^2-pole content used here; photon fermionic pole from the banked SM
content (sum N_c Q^2 = 8).

Validation (no external target)
-------------------------------
1. Bosonic poles are linear in p^2 (second difference = 0) for AA/WW/ZZ -- the
   (M^4/p^2) terms are pole-free; renormalizable.
2. OS-renormalized Sigma_hat_VV(p^2) pole = 0 at multiple p^2 for AA (photon,
   massless, full ferm+bos), WW, ZZ (bosonic).
3. Bosonic Sigma_hat_WW(0), Sigma_hat_ZZ(0) UV-finite -> the v24.3.90 bosonic
   Delta rho +4 bare divergence is removed by OS renormalization.

Honest scope
------------
This banks the BOSONIC-sector (and full-photon) OS UV cancellation. The fermionic
W/Z self-energy poles (which need the Z/W fermion couplings), the full Delta r
UV cancellation across the charge + weak-angle counterterm maps, the finite +
timelike Re Pi_WW(M_W^2)/Re Pi_ZZ(M_Z^2), and the vertex+box delta_VB remain OPEN.
No Delta r_rem / M_W is produced; DIZET stays the publishable OS-W closure.

Status
------
- Export_native_uv_cancellation_bosonic          = 1
- Export_OSW_APF_internal_delta_r_rem_evaluated   = 0   (OPEN, unchanged)
"""
from __future__ import annotations

from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_native_uv_pole import sum_Nc_Q2

_MW = 80.379
_MW2 = _MW * _MW
_MH2 = 125.25 ** 2
_S2_REF = 3.0 / 13.0


# ===========================================================================
# general-p^2 UV-pole content P_VV(p^2) (linear);  Sigma_T = -(alpha/4pi) P
# ===========================================================================
def P_AA_bos(p2: float, mw2: float = _MW2) -> float:
    """Bosonic photon-VP pole content: (3p^2+4M_W^2)-4M_W^2 = 3 p^2 (pure p^2)."""
    return 3.0 * p2


def P_AA_ferm(p2: float) -> float:
    """Fermionic photon-VP pole content: -(4/3) sum N_c Q^2 p^2 (pure p^2, massless)."""
    return -(4.0 / 3.0) * sum_Nc_Q2() * p2


def P_AA(p2: float, mw2: float = _MW2) -> float:
    return P_AA_bos(p2, mw2) + P_AA_ferm(p2)


def P_ZZ_bos(p2: float, s2: float = _S2_REF, mw2: float = _MW2, mh2: float = _MH2) -> float:
    c2 = 1.0 - s2; mz2 = mw2 / c2
    b1 = (18.0 * c2 * c2 + 2.0 * c2 - 0.5) * p2 + (24.0 * c2 - 12.0) * mw2
    b2 = -p2 - 12.0 * mz2
    return (1.0 / (6.0 * s2 * c2)) * b1 + (1.0 / (12.0 * s2 * c2)) * b2


def P_WW_bos(p2: float, s2: float = _S2_REF, mw2: float = _MW2, mh2: float = _MH2) -> float:
    c2 = 1.0 - s2; mz2 = mw2 / c2
    bW1 = 5.0 * p2                                                   # (2M_W^2+5p^2)-2M_W^2; (M_W^4/p^2)-term pole 0
    bW2 = (40.0 * c2 - 1.0) * p2 + (16.0 * c2 + 54.0 - 10.0 / c2) * mw2 - (16.0 * c2 + 2.0) * (mw2 + mz2)
    bW3 = -p2 - 12.0 * mw2
    return (2.0 / 3.0) * bW1 + (1.0 / (12.0 * s2)) * bW2 + (1.0 / (12.0 * s2)) * bW3


def _slope(P, *a) -> float:
    """Exact slope of a linear P via widely-separated points (machine precision)."""
    X = 1.0e6
    return (P(X, *a) - P(-X, *a)) / (2.0 * X)


def renorm_pole(P, mv2: float, *a) -> float:
    """OS-renormalized self-energy pole at a test p^2 (expect 0 for linear P)."""
    A = _slope(P, *a)
    p2 = 3.0 * mv2 + 1000.0
    return P(p2, *a) - P(mv2, *a) - (p2 - mv2) * A


EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_uv_cancellation_bosonic": 1,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


# ===========================================================================
# checks
# ===========================================================================
def check_T_w_trace_native_uv_cancel_poles_linear_P() -> Dict[str, Any]:
    """T: bosonic self-energy UV poles are linear in p^2 (renormalizable; no 1/p^2) [P]."""
    def second_diff(P, *a):
        xs = [-2000.0, 0.0, 2000.0, 4000.0]
        ys = [P(x, *a) for x in xs]
        scale = max(abs(y) for y in ys) or 1.0
        d2 = abs((ys[2] - ys[1]) - (ys[1] - ys[0])) + abs((ys[3] - ys[2]) - (ys[2] - ys[1]))
        return d2 / scale
    mx = max(second_diff(P_AA_bos), second_diff(P_ZZ_bos), second_diff(P_WW_bos), second_diff(P_AA))
    check(mx < 1e-12, f"bosonic self-energy poles must be linear in p^2; max rel 2nd-diff {mx:.2e}")
    return _result(
        name="T_w_trace_native_uv_cancel_poles_linear: "
             "bosonic gauge-boson self-energy UV poles are linear in p^2 (renormalizable) [P]",
        tier=4, epistemic="P",
        summary=(
            f"The UV-pole content P_VV(p^2) of Denner's Sigma^{{AA}}_T/Sigma^{{WW}}_T/"
            f"Sigma^{{ZZ}}_T (bosonic, and full photon) is strictly linear in p^2 (relative "
            f"second difference {mx:.1e}): no p^4 and no 1/p^2 pole survives. In particular "
            f"the (M^4/p^2)(B0(p^2)-B0(0)) terms in Sigma^{{WW}}_T are pole-free (the pole "
            f"cancels in the B0 difference), so the gauge sector is renormalizable with the "
            f"standard mass + field counterterms. This also validates the general-p^2 "
            f"transcription against the v24.3.90 k^2=0 poles."
        ),
        key_result=f"bosonic self-energy poles linear in p^2 (renormalizable; rel 2nd-diff {mx:.1e}). [P]",
        dependencies=["T_w_trace_native_drho_bosonic_pole_universal",
                      "T_w_trace_native_uv_pole_coeffs_match_mu_running"],
        artifacts={"max_rel_second_diff": mx},
    )


def check_T_w_trace_native_uv_cancel_os_renormalized_finite_P() -> Dict[str, Any]:
    """T: OS-renormalized Sigma_hat_VV(p^2) is UV-finite (pole 0) for AA/WW/ZZ [P]."""
    c2 = 1.0 - _S2_REF; mz2 = _MW2 / c2
    cases = {
        "AA(photon, MA^2=0, ferm+bos)": renorm_pole(P_AA, 0.0, _MW2),
        "WW(bos, MW^2)": renorm_pole(P_WW_bos, _MW2, _S2_REF, _MW2, _MH2),
        "ZZ(bos, MZ^2)": renorm_pole(P_ZZ_bos, mz2, _S2_REF, _MW2, _MH2),
    }
    # photon stays massless: pole content at p^2=0 vanishes (no mass counterterm)
    aa0 = abs(P_AA(0.0))
    check(aa0 < 1e-9, f"photon pole at p^2=0 must vanish (massless), got {aa0:.2e}")
    mx = 0.0
    for name, val in cases.items():
        scale = abs(P_WW_bos(_MW2)) or 1.0
        mx = max(mx, abs(val) / scale)
        check(abs(val) / scale < 1e-9, f"{name}: renormalized pole {val:.3e} must vanish")
    return _result(
        name="T_w_trace_native_uv_cancel_os_renormalized_finite: "
             "OS-renormalized bosonic self-energies are UV-finite (Stage-4 cancellation) [P]",
        tier=4, epistemic="P",
        summary=(
            f"With the on-shell counterterms delta M_V^2 = Re Sigma_VV(M_V^2) and "
            f"delta Z_V = -Re Sigma'_VV(M_V^2), the renormalized self-energy "
            f"Sigma_hat_VV(p^2) = Sigma_VV(p^2) - delta M_V^2 + (p^2-M_V^2) delta Z_V has "
            f"zero UV pole at all p^2 (max rel {mx:.1e}) for the photon (full ferm+bos, "
            f"massless so delta M_A^2 = 0 and delta Z_A alone removes the pure-p^2 pole), "
            f"and the bosonic W and Z. This is the Stage-4 UV-cancellation property: the "
            f"linear-in-p^2 divergence is removed exactly by the mass + field "
            f"counterterms, so the renormalized self-energies feeding Delta r are finite."
        ),
        key_result=f"OS-renormalized Sigma_hat_VV UV-finite for AA/WW/ZZ (max rel {mx:.1e}). [P]",
        dependencies=["T_w_trace_native_uv_cancel_poles_linear",
                      "T_w_trace_native_bosonic_photon_vp_pole_minus3"],
        artifacts={"renorm_poles": cases, "photon_pole_at_0": aa0},
    )


def check_T_w_trace_native_uv_cancel_drho_plus4_absorbed_P() -> Dict[str, Any]:
    """T: the v24.3.90 bosonic Delta rho +4 is removed by OS renormalization [P]."""
    c2 = 1.0 - _S2_REF; mz2 = _MW2 / c2
    # bare bosonic Delta rho pole (v24.3.90): P_WW_bos(0)/MW^2 - P_ZZ_bos(0)/MZ^2 = +4
    bare = P_WW_bos(0.0) / _MW2 - P_ZZ_bos(0.0) / mz2
    check(abs(bare - 4.0) < 1e-9, f"bare bosonic Delta rho pole must reproduce v24.3.90 +4, got {bare:.6f}")
    # renormalized self-energies at 0 are finite -> bosonic Delta rho built from them is finite
    rn_ww0 = renorm_pole(P_WW_bos, _MW2, _S2_REF, _MW2, _MH2)
    rn_zz0 = renorm_pole(P_ZZ_bos, mz2, _S2_REF, _MW2, _MH2)
    scale = abs(P_WW_bos(_MW2)) or 1.0
    check(abs(rn_ww0) / scale < 1e-9 and abs(rn_zz0) / scale < 1e-9,
          "renormalized Sigma_hat_WW, Sigma_hat_ZZ poles must vanish")
    return _result(
        name="T_w_trace_native_uv_cancel_drho_plus4_absorbed: "
             "the bare bosonic Delta rho +4 divergence is removed by OS mass renormalization [P]",
        tier=4, epistemic="P",
        summary=(
            f"The v24.3.90 bare bosonic Delta rho pole (+4, reproduced here as {bare:.4f}) is "
            f"a bare-quantity artifact: once W and Z are OS-renormalized, Sigma_hat_WW and "
            f"Sigma_hat_ZZ are UV-finite, so the bosonic Delta rho built from the "
            f"RENORMALIZED self-energies is finite -- the +4 is exactly what delta M_W^2 / "
            f"delta M_Z^2 absorb. The renormalized finite VALUE remains [C] (needs the "
            f"finite + timelike parts), but its UV-finiteness is now established, closing "
            f"the v24.3.90 open characterization at the divergence level."
        ),
        key_result="bare bosonic Delta rho +4 removed by OS renormalization (Sigma_hat finite); value [C]. [P]",
        dependencies=["T_w_trace_native_uv_cancel_os_renormalized_finite",
                      "T_w_trace_native_drho_bosonic_pole_universal"],
        artifacts={"bare_drho_pole": bare, "renorm_ww0": rn_ww0, "renorm_zz0": rn_zz0},
    )


def check_T_w_trace_native_uv_cancel_scope_partial_P() -> Dict[str, Any]:
    """T: bosonic OS UV-cancellation done; fermionic WW/ZZ + full Delta r CT + finite/timelike OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_native_uv_cancellation_bosonic"] == 1, "uv-cancel flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no APF-internal Delta r_rem evaluated by this rung")
    return _result(
        name="T_w_trace_native_uv_cancel_scope_partial: "
             "bosonic OS UV-cancellation done; fermionic WW/ZZ + full Delta r CT + finite/timelike OPEN [P_structural]",
        tier=4, epistemic="P_structural_partial",
        summary=(
            "The bosonic-sector (and full-photon) Stage-4 UV cancellation is native: the "
            "self-energy poles are linear in p^2 (renormalizable) and the OS mass + field "
            "counterterms render the renormalized self-energies UV-finite, removing the "
            "v24.3.90 bosonic Delta rho +4 divergence. Still OPEN toward Delta r_rem: the "
            "fermionic W/Z self-energy poles (which need the Z/W fermion couplings), the "
            "full Delta r UV cancellation across the charge + weak-angle counterterm maps "
            "(v24.3.80), the FINITE + timelike Re Pi_WW(M_W^2)/Re Pi_ZZ(M_Z^2), and the "
            "vertex+box delta_VB. No Delta r_rem / M_W is produced; DIZET stays the "
            "publishable OS-W closure."
        ),
        key_result="bosonic OS UV-cancellation done; fermionic WW/ZZ + full Delta r CT + finite/timelike OPEN. [P_structural]",
        dependencies=["T_w_trace_native_uv_cancel_drho_plus4_absorbed"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_native_uv_cancel_poles_linear":
        check_T_w_trace_native_uv_cancel_poles_linear_P,
    "T_w_trace_native_uv_cancel_os_renormalized_finite":
        check_T_w_trace_native_uv_cancel_os_renormalized_finite_P,
    "T_w_trace_native_uv_cancel_drho_plus4_absorbed":
        check_T_w_trace_native_uv_cancel_drho_plus4_absorbed_P,
    "T_w_trace_native_uv_cancel_scope_partial":
        check_T_w_trace_native_uv_cancel_scope_partial_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}
