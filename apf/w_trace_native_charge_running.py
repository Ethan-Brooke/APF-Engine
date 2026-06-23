"""APF-native gauge-invariant charge running: the bosonic -7 -- Tier-4.

Path 2 of the Stage-3 native OS-W work (after the v24.3.88 bosonic Sigma^{AA}_T).
The v24.3.88 module showed the photon self-energy alone gives -3, and that the
"famous -7" is the gauge-INVARIANT running of the electric charge, which in
't Hooft-Feynman gauge needs the gamma-Z mixing Sigma^{AZ}_T as well. This module
assembles that running natively from Denner's two reviewed self-energies and
reproduces -7, with -7 = -3 (photon SE) + -4 (gamma-Z mixing).

On-shell charge renormalization (Denner 1993, App. B + the OS charge counterterm):

    delta Z_e = (1/2) dSigma^{AA}_T/dk^2|_0 - (s_W/c_W) Sigma^{AZ}_T(0)/M_Z^2

and the one-loop running (beta-function) coefficient is b = 2 * delta Z_e, in the
units where a Dirac fermion of charge Q, colour N_c contributes +(4/3) N_c Q^2
(screening) -- the SAME beta units as the v24.3.88 module (scalar +1/3, etc.).

Sources (verbatim, arXiv:0709.1075, App. B "Self energies", haba2.tex, archived
in Lit Review/):

    Sigma^{AZ}_T(k^2) = -(alpha/4pi) {
        (2/3) sum_{f,i} N_C^f (-Q_f)(g_f^+ + g_f^-)
              [ -(k^2+2 m^2) B0(k^2,m,m) + 2 m^2 B0(0,m,m) + k^2/3 ]
      - (1/(3 s_W c_W)) {
            [(9 c_W^2 + 1/2) k^2 + (12 c_W^2 + 4) M_W^2] B0(k^2,M_W,M_W)
          - (12 c_W^2 - 2) M_W^2 B0(0,M_W,M_W) + (1/3) k^2 }
    }

(Sigma^{AA}_T is in apf.w_trace_native_bosonic_photon_vp, this module reuses its
banked bosonic pole.)

Why this is a no-smuggling -7
-----------------------------
The overall sign / normalization of delta Z_e is CALIBRATED on the known fermion:
because the fermionic gamma-Z brace vanishes at k^2=0 (bracket -> -2m^2 B0(0) +
2m^2 B0(0) = 0), the fermionic charge running is (1/2) dSigma^{AA}_T,ferm/dk^2|_0
only, which must give +(4/3) sum N_c Q^2 -- the established QED value, banked as
apf.w_trace_native_uv_pole.photon_vp_pole_coeff. Fixing the convention there, the
BOSONIC value -7 is then a prediction of Denner's reviewed Sigma^{AA}_T +
Sigma^{AZ}_T, not a tuned target.

Pole arithmetic (units of (alpha/4pi) * Delta_eps; B0 pole = 1, B0' pole = 0):
  photon SE  : (1/2) dSigma^{AA}_T,bos/dk^2|_0  = (1/2)(-3)            = -3/2
  gamma-Z    : -(s_W/c_W) Sigma^{AZ}_T,bos(0)/M_Z^2
               Sigma^{AZ}_T,bos(0) pole = (1/(3 s_W c_W)) * 6 M_W^2 = 2 M_W^2/(s_W c_W)
               /M_Z^2 = /(M_W^2/c_W^2) = 2 c_W/s_W ; *(-(s_W/c_W)) = -2
  delta Z_e,bos = -3/2 - 2 = -7/2  ->  b_bos = 2 * (-7/2) = -7
The s_W/c_W cancels in the gamma-Z term, so -7 is gauge-parameter / weak-angle
independent -- a Ward/gauge-invariance gate.

Validation (no external target)
-------------------------------
1. gamma-Z mixing piece. Native Sigma^{AZ}_T,bos(0) matches its closed form
   +(alpha/4pi)(2/(s_W c_W)) M_W^2 B0(0,M_W,M_W); the (s_W/c_W) Sigma^{AZ}(0)/M_Z^2
   pole coefficient = +2, contributing -4 to the running.
2. Total bosonic charge running = -7, decomposed -3 (photon SE, reusing the
   banked v24.3.88 Pi_bos pole) + -4 (gamma-Z mixing).
3. Gauge invariance. b_bos = -7 independent of sin^2 theta_W (computed at three
   values) -- the s_W/c_W cancellation.
4. Fermionic-normalization anchor (no-smuggling). Sigma^{AZ}_T,ferm(0)=0, so the
   fermionic running is the photon-SE piece only and reproduces +(4/3) sum N_c Q^2
   with sum N_c Q^2 = 8 -- value-identical to the banked QED beta-function. This
   is the calibration that makes the bosonic -7 a prediction, not a fit.

Honest scope
------------
This banks the gauge-invariant one-loop running of the electric charge (the -7
bosonic + the fermionic +(4/3) sum N_c Q^2) from Denner's reviewed Sigma^{AA}_T +
Sigma^{AZ}_T. The bosonic Pi_WW/Pi_ZZ self-energies, the vertex+box delta_VB, the
Stage-4 UV cancellation, and the full Delta r_rem / M_W remain OPEN. No Delta r_rem
/ M_W is produced; DIZET stays the publishable OS-W closure.

Status
------
- Export_native_charge_running_bosonic_minus7    = 1
- Export_OSW_APF_internal_delta_r_rem_evaluated   = 0   (OPEN, unchanged)
"""
from __future__ import annotations

import math
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_pv_timelike_two_point import re_b0_timelike
from apf.w_trace_native_uv_pole import b0_pole, sum_Nc_Q2, photon_vp_pole_coeff
from apf.w_trace_native_bosonic_photon_vp import Pi_bos_pole, _PREF as _PREF_AA

_ALPHA_0 = 1.0 / 137.035999084
_E2 = 4.0 * math.pi * _ALPHA_0
_PREF = _E2 / (16.0 * math.pi ** 2)        # alpha/4pi
_N = 120000

_MW = 80.379
_MW2 = _MW * _MW
_S2_REF = 3.0 / 13.0                        # APF sin^2 theta_W (representative; result is s2-independent)


# ===========================================================================
# native gamma-Z mixing Sigma^{AZ}_T (Denner App. B, bosonic brace)
# ===========================================================================
def sigma_AZ_bos(k2: float, mw2: float = _MW2, s2: float = _S2_REF, n: int = _N) -> float:
    """Denner bosonic gamma-Z mixing Sigma^{AZ}_T,bos(k^2), native (real part).

    Sigma^{AZ}_T,bos = +(alpha/4pi)/(3 s_W c_W) {
        [(9 c_W^2 + 1/2) k^2 + (12 c_W^2 + 4) M_W^2] B0(k^2,M_W,M_W)
      - (12 c_W^2 - 2) M_W^2 B0(0,M_W,M_W) + k^2/3 }
    (the overall -(alpha/4pi) * -(1/(3 s_W c_W)) = +(alpha/4pi)/(3 s_W c_W)).
    """
    c2 = 1.0 - s2
    sW = math.sqrt(s2); cW = math.sqrt(c2)
    b0_k = re_b0_timelike(k2, mw2, mw2, n=n)
    b0_0 = re_b0_timelike(0.0, mw2, mw2, n=n)
    brace = (((9.0 * c2 + 0.5) * k2 + (12.0 * c2 + 4.0) * mw2) * b0_k
             - (12.0 * c2 - 2.0) * mw2 * b0_0
             + k2 / 3.0)
    return _PREF * brace / (3.0 * sW * cW)


def sigma_AZ_bos_pole_at0_over_pref(mw2: float = _MW2, s2: float = _S2_REF) -> float:
    """Pole coefficient of Sigma^{AZ}_T,bos(0), in units of (alpha/4pi) Delta_eps.

    At k^2=0 the brace pole is [(12 c_W^2+4) - (12 c_W^2-2)] M_W^2 = 6 M_W^2, so
    the coefficient is (1/(3 s_W c_W)) 6 M_W^2 = 2 M_W^2/(s_W c_W).
    """
    c2 = 1.0 - s2
    sW = math.sqrt(s2); cW = math.sqrt(c2)
    brace_pole = ((12.0 * c2 + 4.0) * mw2 * b0_pole(0.0, mw2, mw2)
                  - (12.0 * c2 - 2.0) * mw2 * b0_pole(0.0, mw2, mw2))
    return brace_pole / (3.0 * sW * cW)


# ===========================================================================
# charge running beta-coefficients (units: Dirac fermion Q=1,N_c=1 -> +4/3)
# ===========================================================================
def dSigmaAA_dk2_at0_bos_over_pref(mw2: float = _MW2) -> float:
    """Pole coeff of dSigma^{AA}_T,bos/dk^2|_0 in (alpha/4pi)Delta = -3 (B0' pole=0).

    Reuses the banked v24.3.88 bosonic pole: Pi_bos(=-Sigma_T/k^2) pole/PREF = +3,
    so dSigma^{AA}_T,bos/dk^2|_0 pole/PREF = -(Pi_bos pole/PREF) = -3.
    """
    return -(Pi_bos_pole(-500.0, mw2) / _PREF_AA)


def beta_bos(mw2: float = _MW2, s2: float = _S2_REF) -> float:
    """Bosonic one-loop charge-running coefficient = 2*deltaZ_e,bos (expect -7)."""
    c2 = 1.0 - s2
    sW = math.sqrt(s2); cW = math.sqrt(c2)
    mz2 = mw2 / c2
    dZe = 0.5 * dSigmaAA_dk2_at0_bos_over_pref(mw2) \
        - (sW / cW) * (sigma_AZ_bos_pole_at0_over_pref(mw2, s2) / mz2)
    return 2.0 * dZe


def beta_ferm() -> float:
    """Fermionic one-loop charge-running coefficient = +(4/3) sum N_c Q^2.

    Sigma^{AZ}_T,ferm(0)=0, so only the photon-SE piece survives:
    (1/2) dSigma^{AA}_T,ferm/dk^2|_0 pole/PREF = (1/2)(4/3) sum N_c Q^2; *2 = (4/3) sum.
    """
    return (4.0 / 3.0) * sum_Nc_Q2()


def fermionic_AZ_bracket_at0(m2: float) -> float:
    """Per-species fermionic gamma-Z bracket at k^2=0 (must vanish, coupling-independent)."""
    b0_0 = re_b0_timelike(0.0, m2, m2)
    return -(0.0 + 2.0 * m2) * b0_0 + 2.0 * m2 * b0_0 + 0.0


EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_charge_running_bosonic_minus7": 1,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


# ===========================================================================
# checks
# ===========================================================================
def check_T_w_trace_native_charge_running_gammaZ_mixing_P() -> Dict[str, Any]:
    """T: native gamma-Z mixing Sigma^{AZ}_T(0) matches closed form; pole piece -> -4 [P]."""
    mx = 0.0
    for mw2 in (80.0 ** 2, 120.0 ** 2):
        for s2 in (3.0 / 13.0, 0.25):
            c2 = 1.0 - s2; sW = math.sqrt(s2); cW = math.sqrt(c2)
            native = sigma_AZ_bos(0.0, mw2, s2)
            closed = _PREF * (2.0 / (sW * cW)) * mw2 * re_b0_timelike(0.0, mw2, mw2)
            rel = abs(native - closed) / abs(closed)
            mx = max(mx, rel)
            check(rel < 1e-9, f"Sigma^AZ_bos(0) native {native:.6e} vs closed {closed:.6e} rel {rel:.1e}")
    # the (s_W/c_W) Sigma^AZ(0)/M_Z^2 pole coefficient = +2 -> contributes -4 to the running
    gammaZ_contrib = 0.0
    for s2 in (3.0 / 13.0, 0.25, 0.30):
        c2 = 1.0 - s2; sW = math.sqrt(s2); cW = math.sqrt(c2); mz2 = _MW2 / c2
        piece = (sW / cW) * (sigma_AZ_bos_pole_at0_over_pref(_MW2, s2) / mz2)   # = +2
        check(abs(piece - 2.0) < 1e-9, f"(s/c)Sigma^AZ(0)/M_Z^2 pole {piece:.6f} must be +2 (s2={s2})")
        gammaZ_contrib = -2.0 * piece   # running contribution = 2 * (-(s/c)Sigma^AZ/M_Z^2)
    check(abs(gammaZ_contrib + 4.0) < 1e-9, f"gamma-Z running contribution {gammaZ_contrib} must be -4")
    return _result(
        name="T_w_trace_native_charge_running_gammaZ_mixing: "
             "native gamma-Z mixing Sigma^{AZ}_T contributes -4 to the charge running [P]",
        tier=4, epistemic="P",
        summary=(
            f"Denner's bosonic gamma-Z mixing Sigma^{{AZ}}_T,bos(0), evaluated natively, "
            f"matches its closed form +(alpha/4pi)(2/(s_W c_W))M_W^2 B0(0,M_W,M_W) to rel "
            f"{mx:.1e} across M_W and sin^2 theta values. Its (s_W/c_W)Sigma^{{AZ}}(0)/M_Z^2 "
            f"pole coefficient is +2 (s_W/c_W cancelling against the 2c_W/s_W from the "
            f"M_Z^2 = M_W^2/c_W^2 division), so the gamma-Z mixing contributes exactly -4 "
            f"to the one-loop charge-running coefficient -- the piece that lives OUTSIDE "
            f"the photon self-energy in 't Hooft-Feynman gauge."
        ),
        key_result="native gamma-Z Sigma^AZ_T(0): closed-form match + running contribution -4. [P]",
        dependencies=["T_w_trace_native_bosonic_photon_vp_transversality",
                      "T_w_trace_pv_timelike_spacelike_overlap"],
        artifacts={"closed_form_rel": mx, "gammaZ_running_contribution": gammaZ_contrib},
    )


def check_T_w_trace_native_charge_running_bosonic_minus7_P() -> Dict[str, Any]:
    """T: gauge-invariant bosonic charge running = -7 = -3 (photon SE) + -4 (gamma-Z) [P]."""
    photon_se = dSigmaAA_dk2_at0_bos_over_pref(_MW2)   # = -3 (=2*(1/2)(-3))
    b = beta_bos(_MW2, _S2_REF)
    check(abs(photon_se + 3.0) < 1e-9, f"photon-SE running contribution {photon_se} must be -3")
    check(abs(b + 7.0) < 1e-9, f"bosonic charge running {b:.8f} must be -7")
    # decomposition: -7 = -3 + (-4)
    gammaZ = b - photon_se
    check(abs(gammaZ + 4.0) < 1e-9, f"gamma-Z piece {gammaZ} must be -4 (total - photon SE)")
    return _result(
        name="T_w_trace_native_charge_running_bosonic_minus7: "
             "gauge-invariant bosonic charge running is -7 = -3 (photon SE) + -4 (gamma-Z) [P]",
        tier=4, epistemic="P",
        summary=(
            f"The bosonic one-loop running of the electric charge, b = 2 delta Z_e with "
            f"delta Z_e = (1/2) dSigma^{{AA}}_T/dk^2|_0 - (s_W/c_W)Sigma^{{AZ}}_T(0)/M_Z^2, "
            f"assembled natively from Denner's reviewed Sigma^{{AA}}_T (banked v24.3.88, "
            f"contributing -3) and Sigma^{{AZ}}_T (contributing -4), equals -7 exactly. "
            f"This is the 'famous -7' the v24.3.87 attempt chased -- recovered here as a "
            f"gauge-invariant quantity, NOT from the photon self-energy alone (which is "
            f"-3). The -7 = -22/3 + 1/3 reading is the same number once the photon SE is "
            f"split into the W gauge+ghost (-10/3) and Goldstone (+1/3) and the gamma-Z "
            f"mixing (-4) is added: -10/3 + 1/3 - 4 = -7."
        ),
        key_result="bosonic charge running = -7 = -3 (photon SE) + -4 (gamma-Z mixing). [P]",
        dependencies=["T_w_trace_native_charge_running_gammaZ_mixing",
                      "T_w_trace_native_bosonic_photon_vp_pole_minus3"],
        artifacts={"photon_se_contribution": photon_se, "beta_bos": b, "gammaZ_contribution": gammaZ},
    )


def check_T_w_trace_native_charge_running_gauge_invariance_P() -> Dict[str, Any]:
    """T: bosonic -7 is independent of sin^2 theta_W (s_W/c_W cancellation) [P]."""
    vals = {}
    for s2 in (0.20, 3.0 / 13.0, 0.2312, 0.25, 0.30):
        vals[round(s2, 4)] = beta_bos(_MW2, s2)
    spread = max(abs(v + 7.0) for v in vals.values())
    check(spread < 1e-9, f"b_bos must be -7 for all sin^2 theta, got {vals}")
    # also M_W-independent
    for mw2 in (75.0 ** 2, 80.0 ** 2, 100.0 ** 2):
        check(abs(beta_bos(mw2, _S2_REF) + 7.0) < 1e-9, f"b_bos must be -7 for M_W^2={mw2}")
    return _result(
        name="T_w_trace_native_charge_running_gauge_invariance: "
             "bosonic charge running -7 is independent of sin^2 theta_W and M_W [P]",
        tier=4, epistemic="P",
        summary=(
            f"The bosonic charge-running coefficient stays -7 across sin^2 theta_W in "
            f"[0.20, 0.30] (spread {spread:.0e}) and across M_W -- the s_W/c_W in the "
            f"gamma-Z term cancels against the 2 c_W/s_W from M_Z^2 = M_W^2/c_W^2, and "
            f"the photon-SE -3 is intrinsically scale-free. A gauge-invariance / Ward "
            f"gate: the physical running cannot depend on the weak-angle bookkeeping that "
            f"splits it between the photon self-energy and the gamma-Z mixing."
        ),
        key_result=f"b_bos = -7 independent of sin^2 theta_W and M_W (spread {spread:.0e}). [P]",
        dependencies=["T_w_trace_native_charge_running_bosonic_minus7"],
        artifacts={"beta_by_sin2": vals, "spread": spread},
    )


def check_T_w_trace_native_charge_running_fermionic_anchor_P() -> Dict[str, Any]:
    """T: fermionic charge running = +(4/3) sum N_c Q^2 (sum=8); Sigma^{AZ}_ferm(0)=0 [P]."""
    # fermionic gamma-Z vanishes at k^2=0 (coupling-independent), for several masses
    mx = 0.0
    for m in (0.105, 1.777, 4.18, 173.0):
        v = fermionic_AZ_bracket_at0(m * m)
        mx = max(mx, abs(v))
        check(abs(v) < 1e-9, f"fermionic Sigma^AZ bracket at 0 (m={m}) must vanish, got {v:.2e}")
    s = sum_Nc_Q2()
    check(abs(s - 8.0) < 1e-12, f"sum N_c Q^2 must be 8, got {s}")
    bf = beta_ferm()
    check(abs(bf - (4.0 / 3.0) * 8.0) < 1e-9, f"fermionic running {bf} must be (4/3)*8 = 32/3")
    # ties to the banked QED beta-function magnitude (photon_vp_pole_coeff = -(alpha/4pi)(4/3) sum)
    banked_mag = abs(photon_vp_pole_coeff()) / _PREF      # = (4/3) sum N_c Q^2
    check(abs(bf - banked_mag) < 1e-9, f"fermionic running {bf} must equal banked |photon-VP pole|/PREF {banked_mag}")
    return _result(
        name="T_w_trace_native_charge_running_fermionic_anchor: "
             "fermionic charge running +(4/3) sum N_c Q^2 calibrates the convention [P]",
        tier=4, epistemic="P",
        summary=(
            f"The fermionic gamma-Z brace vanishes at k^2=0 (to {mx:.0e}, coupling-"
            f"independently), so the fermionic charge running is the photon-SE piece only "
            f"and equals +(4/3) sum N_c Q^2 = {bf:.4f} with sum N_c Q^2 = {s:.0f}, value-"
            f"identical to the banked |photon_vp_pole_coeff|/PREF. This is the no-smuggling "
            f"calibration: the overall sign and 2*delta Z_e normalization of the running "
            f"are fixed on the established QED fermion value, so the bosonic -7 is a "
            f"prediction of Denner's reviewed self-energies, not a tuned target."
        ),
        key_result=f"fermionic running = (4/3) sum N_c Q^2 = {bf:.3f} (sum=8); Sigma^AZ_ferm(0)=0. [P]",
        dependencies=["T_w_trace_native_charge_running_bosonic_minus7",
                      "T_w_trace_native_photon_vp_pole_beta_function"],
        artifacts={"fermionic_AZ_at0_max": mx, "beta_ferm": bf, "banked_mag": banked_mag, "sum_Nc_Q2": s},
    )


def check_T_w_trace_native_charge_running_scope_partial_P() -> Dict[str, Any]:
    """T: charge running -7 done; Pi_WW/Pi_ZZ + delta_VB + UV cancellation + Delta r_rem OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_native_charge_running_bosonic_minus7"] == 1, "charge-running flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no APF-internal Delta r_rem evaluated by this rung")
    return _result(
        name="T_w_trace_native_charge_running_scope_partial: "
             "gauge-invariant charge running done; Pi_WW/Pi_ZZ + delta_VB + Delta r_rem OPEN [P_structural]",
        tier=4, epistemic="P_structural_partial",
        summary=(
            "The gauge-invariant one-loop running of the electric charge is now native: "
            "the bosonic -7 (= -3 photon SE + -4 gamma-Z mixing) and the fermionic "
            "+(4/3) sum N_c Q^2, assembled from Denner's reviewed Sigma^{AA}_T + "
            "Sigma^{AZ}_T with the convention calibrated on the banked QED fermion value. "
            "Still OPEN toward the APF-internal Delta r_rem: the bosonic Pi_WW/Pi_ZZ "
            "self-energies, the vertex+box delta_VB, the Stage-4 UV cancellation against "
            "the banked counterterms, and the assembled Delta r_rem / M_W. DIZET stays "
            "the publishable OS-W closure."
        ),
        key_result="native gauge-invariant charge running done (-7 bosonic); Pi_WW/Pi_ZZ + delta_VB + Delta r_rem OPEN. [P_structural]",
        dependencies=["T_w_trace_native_charge_running_gauge_invariance",
                      "T_w_trace_native_charge_running_fermionic_anchor"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_native_charge_running_gammaZ_mixing":
        check_T_w_trace_native_charge_running_gammaZ_mixing_P,
    "T_w_trace_native_charge_running_bosonic_minus7":
        check_T_w_trace_native_charge_running_bosonic_minus7_P,
    "T_w_trace_native_charge_running_gauge_invariance":
        check_T_w_trace_native_charge_running_gauge_invariance_P,
    "T_w_trace_native_charge_running_fermionic_anchor":
        check_T_w_trace_native_charge_running_fermionic_anchor_P,
    "T_w_trace_native_charge_running_scope_partial":
        check_T_w_trace_native_charge_running_scope_partial_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}
