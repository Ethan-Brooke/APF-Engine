"""APF-native FULL bosonic photon vacuum polarization Sigma^{AA}_T -- Tier-4.

Stage 3 of the native OS-W one-loop evaluator (work plan 2026-05-24), completing
the bosonic photon self-energy that the v24.3.87 Goldstone-scalar rung opened.
Rather than reconstruct the W / ghost / Goldstone vertices from memory (the
v24.3.87 session attempt, which FAILED transversality and was held), this module
evaluates Denner's REVIEWED closed form for the transverse photon self-energy
natively with the banked PV toolkit -- a legitimately native result (native PV
evaluation of a checked vertex algebra).

Source (verbatim, arXiv:0709.1075 = Denner, Fortschr. Phys. 41 (1993) 307, App. B
"Self energies", haba2.tex, archived in Lit Review/):

    Sigma^{AA}_T(k^2) = -(alpha/4pi) {
        (2/3) sum_{f,i} N_C^f 2 Q_f^2 [ -(k^2+2 m^2) B0(k^2,m,m)
                                        + 2 m^2 B0(0,m,m) + k^2/3 ]
      + [ (3 k^2 + 4 M_W^2) B0(k^2,M_W,M_W) - 4 M_W^2 B0(0,M_W,M_W) ]
    }

The SECOND brace is the COMPLETE bosonic part: the W gauge loop + seagull, the
would-be Goldstone phi^pm, and the Faddeev-Popov ghost c^pm, already summed in
't Hooft-Feynman gauge (xi=1, all three internal masses = M_W). This module
evaluates that brace natively (re_b0_timelike on the banked substrate + the
v24.3.86 b0_pole layer).

Key correction to the v24.3.87 expectation (AUDIT FINDING)
---------------------------------------------------------
The v24.3.87 scalar module asserted the bosonic total would be the "famous -7".
Denner's reviewed Sigma^{AA}_T gives -3, NOT -7:

    pole of {(3 k^2 + 4 M_W^2) - 4 M_W^2} = 3 k^2   ->   coefficient -3

in the convention where a Dirac fermion is +4/3 and a charged scalar +1/3
(screening). The M_W^2 pieces cancel at both the pole and at k^2=0, so
transversality Sigma^{AA}_T,bos(0)=0 is automatic. Decomposition:

    Goldstone (banked scalar)        : +1/3   (screening)
    W gauge + seagull + ghost        : -10/3
    total bosonic Sigma^{AA}_T       : -3

The -7 (= -22/3 + 1/3) is a DIFFERENT object: the gauge-INVARIANT running of the
electric charge. In xi=1 gauge the SM charge counterterm is
delta Z_e = (1/2) dSigma^{AA}_T/dk^2|_0 + (s_W/c_W) Sigma^{AZ}_T(0)/M_Z^2, so the
extra -4 that takes -3 -> -7 lives in the gamma-Z mixing Sigma^{AZ}_T, NOT in the
photon self-energy. Sigma^{AZ}_T is in hand (same haba2.tex) for the follow-on
charge-running rung; this module banks Sigma^{AA}_T only.

Sign convention
---------------
This module reports the photon-VP form factor in the SAME convention as the
banked apf.w_trace_native_uv_pole / apf.w_trace_native_bosonic_scalar_vp:
Pi = -Sigma_T/k^2, so a SCREENING field (fermion, scalar) has a NEGATIVE Pi-pole
and the (anti-screening) bosonic W-sector has a POSITIVE Pi-pole. In these units
Pi_bos-pole/PREF = +3 (PREF = alpha/4pi); the "-3" quoted above is the same
number in the screening-positive convention where a Dirac fermion is +4/3.

Validation (no external target)
-------------------------------
1. Transversality. The bosonic numerator (3k^2+4M_W^2)B0(k^2)-4M_W^2 B0(0)
   vanishes at k^2=0 (the M_W^2 terms cancel), for any M_W -- the U(1)_em Ward
   identity. Nontrivial off k^2=0.
2. Pole / beta-function. The bosonic Pi-pole = +3 PREF (M_W-independent), i.e.
   -3 in screening-positive beta units; ratio to one Dirac fermion (Q=1,N_c=1)
   = -9/4; and Pi_bos-pole minus the banked Goldstone-scalar pole = +10/3 PREF,
   the implied W gauge+seagull+ghost piece (-10/3 in beta units). Ties the new
   total to the v24.3.87 banked Goldstone piece.
3. Finite <-> pole consistency. The finite bosonic running d Pi_bos/d ln(-k^2)
   at deeply spacelike k^2 equals the pole coefficient (-3 PREF), confirming the
   finite part (native re_b0_timelike quadrature) is consistent with the pole.
4. Fermionic-normalization anchor (no-smuggling). Denner's fermionic brace pole,
   assembled over the SM fermion content, reproduces the banked fermionic
   photon-VP pole = -(e^2/12pi^2) sum N_c Q^2 with sum N_c Q^2 = 8 -- the same
   normalization whose finite part is the banked Delta alpha_lep. This proves the
   normalization that yields the bosonic -3 is the one that yields the correct
   QED beta-function, so the bosonic number is not an artifact of a misread
   prefactor.

Honest scope
------------
This banks the bosonic transverse photon self-energy Sigma^{AA}_T only. The
gauge-invariant charge-running -7 (which needs Sigma^{AZ}_T mixing), the bosonic
Pi_WW/Pi_ZZ, the vertex+box delta_VB, and the Stage-4 UV cancellation remain
OPEN. No Delta r_rem / M_W is produced; DIZET stays the publishable OS-W closure.

Status
------
- Export_native_bosonic_photon_vp_AA            = 1
- Export_OSW_APF_internal_delta_r_rem_evaluated  = 0   (OPEN, unchanged)
"""
from __future__ import annotations

import math
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_pv_timelike_two_point import re_b0_timelike
from apf.w_trace_native_uv_pole import (
    b0_pole, photon_vp_pole_coeff, sum_Nc_Q2, SM_FERMIONS,
)
from apf.w_trace_native_bosonic_scalar_vp import scalar_vp_numerator_pole

_ALPHA_0 = 1.0 / 137.035999084
_E2 = 4.0 * math.pi * _ALPHA_0
_PREF = _E2 / (16.0 * math.pi ** 2)        # alpha/4pi
_N = 120000

# Representative W-mass scale (GeV). The BANKED quantities (transversality, pole,
# ratios) are M_W-INDEPENDENT -- verified in the checks by using two different
# M_W values -- so no measured M_W is consumed. M_W enters only the (non-exported)
# finite-running display in check 3.
_MW = 80.379
_MW2 = _MW * _MW


# ===========================================================================
# native bosonic photon self-energy (Denner App. B, second brace)
# ===========================================================================
def bosonic_numerator(k2: float, mw2: float = _MW2, n: int = _N) -> float:
    """Denner bosonic brace (real): (3k^2+4M_W^2)B0(k^2,M_W,M_W) - 4M_W^2 B0(0,M_W,M_W)."""
    b0_k = re_b0_timelike(k2, mw2, mw2, n=n)
    b0_0 = re_b0_timelike(0.0, mw2, mw2, n=n)
    return (3.0 * k2 + 4.0 * mw2) * b0_k - 4.0 * mw2 * b0_0


def bosonic_numerator_pole(k2: float, mw2: float = _MW2) -> float:
    """UV-pole coefficient of the bosonic numerator: (3k^2+4M_W^2)-4M_W^2 = 3k^2."""
    return (3.0 * k2 + 4.0 * mw2) * b0_pole(k2, mw2, mw2) - 4.0 * mw2 * b0_pole(0.0, mw2, mw2)


def Pi_bos(k2: float, mw2: float = _MW2, n: int = _N) -> float:
    """Bosonic transverse photon-VP form factor, codebase convention Pi = -Sigma_T/k^2.

    Sigma_T,bos = -(alpha/4pi)*numerator  =>  Pi_bos = +(alpha/4pi)*numerator/k^2.
    """
    return _PREF * bosonic_numerator(k2, mw2, n) / k2


def Pi_bos_pole(k2: float, mw2: float = _MW2) -> float:
    """Pole of the bosonic Pi form factor = +3*PREF (M_W-independent)."""
    return _PREF * bosonic_numerator_pole(k2, mw2) / k2


def denner_fermionic_pi_pole() -> float:
    """Pi-pole of Denner's fermionic brace assembled over SM fermions.

    Per species the bracket pole is -(k^2+2m^2)+2m^2 = -k^2, so
    Sigma_T,ferm-pole = -(alpha/4pi)(2/3)(N_c 2 Q^2)(-k^2) and
    Pi_ferm-pole = -Sigma_T/k^2 = -(alpha/4pi)(4/3) sum N_c Q^2. M_W- and m-independent.
    """
    return sum(-_PREF * (4.0 / 3.0) * Nc * Q * Q for Q, Nc in SM_FERMIONS)


EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_bosonic_photon_vp_AA": 1,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


# ===========================================================================
# checks
# ===========================================================================
def check_T_w_trace_native_bosonic_photon_vp_transversality_P() -> Dict[str, Any]:
    """T: full bosonic photon self-energy is transverse, numerator(0)=0 for any M_W [P]."""
    spread = 0.0
    for mw2 in (80.0 ** 2, 120.0 ** 2):
        b0_0 = re_b0_timelike(0.0, mw2, mw2)
        ref = abs(4.0 * mw2 * b0_0)
        num0 = bosonic_numerator(1e-5 * mw2, mw2)        # k^2 ~ 0
        rel = abs(num0) / ref
        spread = max(spread, rel)
        check(rel < 1e-3, f"M_W^2={mw2:.0f}: bosonic numerator at k^2~0 = {num0:.3e} must vanish (rel {rel:.1e})")
        check(abs(bosonic_numerator(-200.0 * mw2, mw2)) > 1e-3, "bosonic numerator must be nontrivial off k^2=0")
    return _result(
        name="T_w_trace_native_bosonic_photon_vp_transversality: "
             "full bosonic (W+Goldstone+ghost) photon self-energy is transverse [P]",
        tier=4, epistemic="P",
        summary=(
            f"Denner's bosonic brace (3k^2+4M_W^2)B0(k^2,M_W,M_W) - 4M_W^2 B0(0,M_W,M_W) "
            f"vanishes at k^2=0 to rel {spread:.1e} for two distinct M_W values -- the "
            f"M_W^2 pieces cancel, leaving Sigma^{{AA}}_T,bos(0)=0, the U(1)_em Ward "
            f"identity. This is the gauge gate the v24.3.87 memory-vertex attempt "
            f"failed; the reviewed closed form satisfies it by construction, M_W-"
            f"independently. Nontrivial off k^2=0."
        ),
        key_result=f"bosonic Sigma^AA_T,bos(0)=0 (transverse), M_W-independent (rel {spread:.1e}). [P]",
        dependencies=["T_w_trace_native_scalar_vp_transversality",
                      "T_w_trace_pv_timelike_spacelike_overlap"],
        artifacts={"transversality_rel": spread},
    )


def check_T_w_trace_native_bosonic_photon_vp_pole_minus3_P() -> Dict[str, Any]:
    """T: bosonic photon-VP pole = -3 (beta units); ratio -9/4 to Dirac; W+ghost = -10/3 [P]."""
    p2 = -500.0
    coeff_mw = {}
    for mw2 in (80.0 ** 2, 120.0 ** 2):
        coeff_mw[mw2] = Pi_bos_pole(p2, mw2) / _PREF
    spread = max(abs(c - 3.0) for c in coeff_mw.values())
    check(spread < 1e-9, f"bosonic Pi-pole/PREF must be +3 (M_W-independent), got {coeff_mw}")
    dirac_pole_over_pref = -(4.0 / 3.0)
    ratio = (Pi_bos_pole(p2) / _PREF) / dirac_pole_over_pref
    check(abs(ratio + 9.0 / 4.0) < 1e-9, f"bosonic/Dirac pole ratio {ratio:.8f} must be -9/4")
    goldstone_pole_over_pref = (1.0 * scalar_vp_numerator_pole(p2, _MW)) / p2  # = -1/3
    w_ghost = Pi_bos_pole(p2) / _PREF - goldstone_pole_over_pref
    check(abs(goldstone_pole_over_pref + 1.0 / 3.0) < 1e-9,
          f"banked Goldstone pole/PREF {goldstone_pole_over_pref:.6f} must be -1/3")
    check(abs(w_ghost - 10.0 / 3.0) < 1e-9,
          f"W+seagull+ghost = total - Goldstone = {w_ghost:.6f} must be +10/3")
    return _result(
        name="T_w_trace_native_bosonic_photon_vp_pole_minus3: "
             "bosonic photon-VP pole is -3 (beta units), NOT -7; W+ghost = -10/3 [P]",
        tier=4, epistemic="P",
        summary=(
            f"The bosonic Pi-pole = +3 PREF (M_W-independent to {spread:.1e}), i.e. -3 in "
            f"the screening-positive beta convention (Dirac +4/3, scalar +1/3); ratio to "
            f"one Dirac fermion = {ratio:.4f} = -9/4. Subtracting the v24.3.87 banked "
            f"Goldstone piece (-1/3 in beta units) leaves the W gauge+seagull+ghost piece "
            f"= -10/3. This CORRECTS the v24.3.87 docstring's expectation of a -7 total: "
            f"the reviewed Sigma^{{AA}}_T bosonic part is -3. The -7 (= -22/3 + 1/3) is the "
            f"gauge-invariant charge running, which additionally needs the gamma-Z mixing "
            f"Sigma^{{AZ}}_T -- a separate (in-hand) rung, not the photon self-energy."
        ),
        key_result="bosonic Sigma^AA_T pole = -3 beta-units (Goldstone +1/3, W+ghost -10/3); ratio -9/4 to Dirac. [P]",
        dependencies=["T_w_trace_native_bosonic_photon_vp_transversality",
                      "T_w_trace_native_scalar_vp_pole_one_quarter"],
        artifacts={"pole_over_pref_by_mw2": coeff_mw, "ratio_to_dirac": ratio,
                   "goldstone_over_pref": goldstone_pole_over_pref, "w_ghost_seagull": w_ghost},
    )


def check_T_w_trace_native_bosonic_photon_vp_finite_pole_consistency_P() -> Dict[str, Any]:
    """T: finite bosonic running log-slope == pole coefficient (-3 PREF) [P]."""
    k2a, k2b = -1.0e9, -1.0e9 * math.e        # step ln(-k^2) by 1, deeply spacelike
    slope = (Pi_bos(k2b) - Pi_bos(k2a)) / _PREF
    pole_coeff = Pi_bos_pole(-500.0) / _PREF   # = +3 ; running slope carries the opposite sign
    rel = abs(slope - (-pole_coeff)) / abs(pole_coeff)
    check(rel < 2e-3, f"finite log-slope {slope:.5f} vs -pole {-pole_coeff:.5f} (rel {rel:.2e})")
    return _result(
        name="T_w_trace_native_bosonic_photon_vp_finite_pole_consistency: "
             "finite bosonic running log-slope equals the pole coefficient [P]",
        tier=4, epistemic="P",
        summary=(
            f"At deeply spacelike k^2 the native finite bosonic running d Pi_bos/d ln(-k^2) "
            f"= {slope:.4f} PREF reproduces minus the pole coefficient (-3 PREF) to rel "
            f"{rel:.1e}, confirming the finite part (native re_b0_timelike quadrature of "
            f"(3k^2+4M_W^2)B0) is consistent with the exact UV pole. Finite and divergent "
            f"halves of the same reviewed self-energy agree, with no external input."
        ),
        key_result=f"bosonic finite log-slope = -3 PREF, matches the pole (rel {rel:.1e}). [P]",
        dependencies=["T_w_trace_native_bosonic_photon_vp_pole_minus3"],
        artifacts={"finite_log_slope_over_pref": slope, "pole_coeff_over_pref": pole_coeff,
                   "rel_err": rel},
    )


def check_T_w_trace_native_bosonic_photon_vp_fermionic_norm_anchor_P() -> Dict[str, Any]:
    """T: Denner fermionic brace pole == banked QED beta-function (sum N_c Q^2 = 8) [P]."""
    s = sum_Nc_Q2()
    check(abs(s - 8.0) < 1e-12, f"sum N_c Q^2 must be 8, got {s}")
    native = denner_fermionic_pi_pole()
    banked = photon_vp_pole_coeff()
    rel = abs(native - banked) / abs(banked)
    check(rel < 1e-10, f"Denner fermionic pole {native:.8e} vs banked photon-VP pole {banked:.8e} rel {rel:.2e}")
    analytic = -(_E2 / (12.0 * math.pi ** 2)) * s
    rel2 = abs(native - analytic) / abs(analytic)
    check(rel2 < 1e-10, f"Denner fermionic pole vs -(e^2/12pi^2) sum N_c Q^2 rel {rel2:.2e}")
    return _result(
        name="T_w_trace_native_bosonic_photon_vp_fermionic_norm_anchor: "
             "Denner fermionic brace pole reproduces the banked QED beta-function [P]",
        tier=4, epistemic="P",
        summary=(
            f"The fermionic brace of the SAME Denner Sigma^{{AA}}_T -- bracket pole -k^2 per "
            f"species -- assembled over the SM fermion content gives the photon-VP pole "
            f"-(e^2/12pi^2) sum N_c Q^2 with sum N_c Q^2 = {s:.0f}, value-identical to the "
            f"banked apf.w_trace_native_uv_pole.photon_vp_pole_coeff (rel {rel:.0e}). This "
            f"is the no-smuggling anchor: the prefactor/normalization that yields the "
            f"bosonic -3 is the very one whose fermionic finite part is the banked "
            f"Delta alpha_lep, so the bosonic number is not an artifact of a misread "
            f"convention."
        ),
        key_result=f"Denner fermionic pole == banked QED beta (sum N_c Q^2 = {s:.0f}, rel {rel:.0e}). [P]",
        dependencies=["T_w_trace_native_photon_vp_pole_beta_function",
                      "T_w_trace_native_bosonic_photon_vp_pole_minus3"],
        artifacts={"sum_Nc_Q2": s, "native_pole": native, "banked_pole": banked, "rel": rel},
    )


def check_T_w_trace_native_bosonic_photon_vp_scope_partial_P() -> Dict[str, Any]:
    """T: bosonic Sigma^AA_T done; gamma-Z charge-running -7 + Pi_WW/Pi_ZZ + delta_VB OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_native_bosonic_photon_vp_AA"] == 1, "bosonic AA flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no APF-internal Delta r_rem evaluated by this rung")
    return _result(
        name="T_w_trace_native_bosonic_photon_vp_scope_partial: "
             "bosonic Sigma^AA_T complete; gauge-invariant -7 (gamma-Z mixing) + Pi_WW/Pi_ZZ + delta_VB OPEN [P_structural]",
        tier=4, epistemic="P_structural",
        summary=(
            "The complete bosonic transverse photon self-energy Sigma^{AA}_T (W gauge + "
            "seagull + Goldstone + FP ghost, 't Hooft-Feynman gauge) is now native, "
            "evaluated from Denner's reviewed closed form with the banked PV toolkit and "
            "validated by transversality, the -3 pole (with the banked Goldstone piece "
            "consistent at +1/3 and the implied W+ghost at -10/3), finite<->pole "
            "consistency, and the fermionic-normalization anchor against the banked QED "
            "beta-function. Still OPEN toward Delta r_rem: the gauge-invariant charge "
            "running -7 (needs the gamma-Z mixing Sigma^{AZ}_T, in hand from the same "
            "source), the bosonic Pi_WW/Pi_ZZ, the vertex+box delta_VB, and the Stage-4 "
            "UV cancellation. No Delta r_rem / M_W is produced; DIZET stays the "
            "publishable OS-W closure."
        ),
        key_result="native bosonic Sigma^AA_T done (-3); gamma-Z charge-running -7 + Pi_WW/Pi_ZZ + delta_VB OPEN. [P_structural]",
        dependencies=["T_w_trace_native_bosonic_photon_vp_finite_pole_consistency",
                      "T_w_trace_native_bosonic_photon_vp_fermionic_norm_anchor"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_native_bosonic_photon_vp_transversality":
        check_T_w_trace_native_bosonic_photon_vp_transversality_P,
    "T_w_trace_native_bosonic_photon_vp_pole_minus3":
        check_T_w_trace_native_bosonic_photon_vp_pole_minus3_P,
    "T_w_trace_native_bosonic_photon_vp_finite_pole_consistency":
        check_T_w_trace_native_bosonic_photon_vp_finite_pole_consistency_P,
    "T_w_trace_native_bosonic_photon_vp_fermionic_norm_anchor":
        check_T_w_trace_native_bosonic_photon_vp_fermionic_norm_anchor_P,
    "T_w_trace_native_bosonic_photon_vp_scope_partial":
        check_T_w_trace_native_bosonic_photon_vp_scope_partial_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}
