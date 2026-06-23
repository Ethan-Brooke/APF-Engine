"""APF-native charged-scalar (Goldstone) contribution to the photon VP -- Tier-4.

Stage 3 (first bosonic sub-rung) of the native OS-W one-loop evaluator (work plan
2026-05-24). The full bosonic photon self-energy Pi_gamma_gamma in 't Hooft-
Feynman gauge is the sum of three charged-particle loops: the W gauge boson, the
would-be Goldstone phi^pm (mass M_W at xi=1), and the Faddeev-Popov ghost c^pm.
This module builds the FIRST of the three -- the charged scalar (Goldstone) loop,
i.e. scalar QED -- and validates it. The W gauge loop and ghost loop (which,
summed with this, give the famous -7 bosonic contribution to the photon
beta-function) remain the next rungs.

Construction (scalar QED, two diagrams)
---------------------------------------
- bubble:  gamma-phi-phi vertex  -ieQ(2k+p)^mu, two scalar propagators;
- seagull: gamma-gamma-phi-phi vertex +2ie^2Q^2 g^{mu nu}, one propagator.
Summed, the g^{mu nu} coefficient of the photon self-energy Pi^{mu nu}(p) is

    [Pi^{mu nu}]_{g} = (e^2 Q^2 / 16 pi^2) ( 4 B00(p^2,m^2,m^2) - 2 A0(m^2) ) ,

so the transverse form factor (Pi^{mu nu} = (p^2 g^{mu nu} - p^mu p^nu) Pi_phi) is
Pi_phi(p^2) = (e^2 Q^2/16 pi^2)(4 B00 - 2 A0)/p^2, evaluated with the native
A0/B00 (real parts on the timelike branch where needed).

Validation (no external target)
-------------------------------
1. Transversality. The g^{mu nu} numerator 4 B00 - 2 A0 vanishes at p^2 = 0
   (because 2 B00(0,m^2,m^2) = A0(m^2)), so Sigma^{mu nu}(0) = 0 and the
   self-energy is purely transverse -- the U(1)_em Ward identity.
2. Pole = one quarter of a Dirac fermion. Using the v24.3.86 UV-pole layer,
   4 B00_pole - 2 A0_pole = -p^2/3, so the scalar form-factor pole is
   -(e^2 Q^2/48 pi^2) = (1/3) Q^2 in beta-function units -- exactly 1/4 of a
   Dirac fermion's (4/3) Q^2.
3. Finite closed form. The on-shell-subtracted running reproduces the scalar-QED
   closed form (e^2 Q^2/16 pi^2)(1/3)[ln(q^2/m^2) - 8/3] for q^2 >> m^2 (the
   scalar's 8/3 vs the fermion's 5/3), with the leading coefficient exactly 1/4
   of the fermion's.

Honest scope
------------
This is the Goldstone (charged-scalar) piece of Pi_gamma_gamma only. The W gauge
loop and the FP-ghost loop -- which complete the bosonic photon VP and, summed,
give the -7 bosonic beta-function coefficient -- remain OPEN, as do Pi_WW/Pi_ZZ
bosonic, the vertex+box delta_VB, and the Stage-4 UV cancellation. No Delta r_rem
/ M_W is produced; DIZET stays the publishable OS-W closure.

Status
------
- Export_native_bosonic_scalar_photon_vp        = 1
- Export_OSW_APF_internal_delta_r_rem_evaluated  = 0   (OPEN, unchanged)
"""
from __future__ import annotations

import math
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_pv_scalar_integral_substrate import a0_fin
from apf.w_trace_pv_timelike_two_point import re_b00_timelike
from apf.w_trace_native_uv_pole import a0_pole, b00_pole, photon_vp_bracket_pole

_ALPHA_0 = 1.0 / 137.035999084
_E2 = 4.0 * math.pi * _ALPHA_0
_PREF = _E2 / (16.0 * math.pi ** 2)        # e^2 Q^2 / 16pi^2 with Q^2 folded per call
_N = 120000


def scalar_vp_numerator(p2: float, m: float, n: int = _N) -> float:
    """g^{mu nu} numerator of the scalar-loop photon self-energy: 4 B00 - 2 A0 (real)."""
    m2 = m * m
    return 4.0 * re_b00_timelike(p2, m2, m2, n=n) - 2.0 * a0_fin(m2)


def scalar_vp_numerator_pole(p2: float, m: float) -> float:
    """UV-pole coefficient of the numerator: 4 B00_pole - 2 A0_pole = -p^2/3."""
    m2 = m * m
    return 4.0 * b00_pole(p2, m2, m2) - 2.0 * a0_pole(m2)


def Pi_phi(Q: float, p2: float, m: float, n: int = _N) -> float:
    """Charged-scalar transverse photon-VP form factor."""
    return _PREF * Q * Q * scalar_vp_numerator(p2, m, n) / p2


def _analytic_scalar_running(Q: float, q2: float, m: float) -> float:
    """High-energy scalar-QED running: (e^2Q^2/16pi^2)(1/3)[ln(q^2/m^2) - 8/3]."""
    return _PREF * Q * Q * (1.0 / 3.0) * (math.log(q2 / (m * m)) - 8.0 / 3.0)


EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_bosonic_scalar_photon_vp": 1,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


# ===========================================================================
# checks
# ===========================================================================
def check_T_w_trace_native_scalar_vp_transversality_P() -> Dict[str, Any]:
    """T: charged-scalar photon self-energy is transverse, numerator(0)=0 [P]."""
    spread = 0.0
    for m in (5.0, 80.4):
        num0 = scalar_vp_numerator(1e-6 * m * m, m)       # p^2 ~ 0
        rel = abs(num0) / abs(a0_fin(m * m))
        spread = max(spread, rel)
        check(rel < 1e-5, f"m={m}: 4B00-2A0 at p^2~0 = {num0:.3e} must vanish (rel {rel:.1e})")
        # genuinely transverse: g^{mu nu} numerator nonzero away from 0
        check(abs(scalar_vp_numerator(-100.0, m)) > 1e-3, "numerator must be nontrivial off p^2=0")
    return _result(
        name="T_w_trace_native_scalar_vp_transversality: "
             "charged-scalar (Goldstone) photon self-energy is transverse [P]",
        tier=4, epistemic="P",
        summary=(
            f"The charged-scalar photon self-energy (gamma-phi-phi bubble + "
            f"gamma-gamma-phi-phi seagull) has g^{{mu nu}} numerator 4 B00 - 2 A0, "
            f"which vanishes at p^2 = 0 to rel {spread:.1e} (because "
            f"2 B00(0,m^2,m^2) = A0(m^2)), so Sigma^{{mu nu}}(0) = 0 and the "
            f"self-energy is purely transverse -- the U(1)_em Ward identity, the "
            f"bosonic analogue of the fermionic photon-transversality gate. The "
            f"seagull diagram is exactly what enforces this; the bubble alone is "
            f"not transverse."
        ),
        key_result=f"scalar photon self-energy transverse: 4B00-2A0 -> 0 at p^2=0 (rel {spread:.1e}). [P]",
        dependencies=["T_w_trace_native_photon_transversality",
                      "T_w_trace_pv_b00_b11_trace_relation"],
        artifacts={"transversality_rel": spread},
    )


def check_T_w_trace_native_scalar_vp_pole_one_quarter_P() -> Dict[str, Any]:
    """T: scalar VP pole = (1/3)Q^2 = exactly 1/4 of a Dirac fermion [P]."""
    p2 = -500.0
    # scalar form-factor pole
    scalar_ff_pole = _PREF * 1.0 * scalar_vp_numerator_pole(p2, 5.0) / p2
    # one Dirac fermion (Q=1, N_c=1) form-factor pole from the banked uv_pole layer
    ferm_ff_pole = -(1.0 / (16.0 * math.pi ** 2)) * photon_vp_bracket_pole(1.0, 5.0, p2) / p2
    ratio = scalar_ff_pole / ferm_ff_pole
    # numerator pole must equal -p^2/3 exactly
    np_err = abs(scalar_vp_numerator_pole(p2, 5.0) - (-p2 / 3.0))
    check(np_err < 1e-9, f"scalar numerator pole {scalar_vp_numerator_pole(p2,5.0)} != -p^2/3")
    check(abs(ratio - 0.25) < 1e-10, f"scalar/fermion pole ratio {ratio:.8f} must be 1/4")
    return _result(
        name="T_w_trace_native_scalar_vp_pole_one_quarter: "
             "charged-scalar photon-VP pole is exactly 1/4 of a Dirac fermion [P]",
        tier=4, epistemic="P",
        summary=(
            f"Via the v24.3.86 UV-pole layer, the scalar numerator pole "
            f"4 B00_pole - 2 A0_pole = -p^2/3, so the scalar form-factor pole is "
            f"-(e^2 Q^2/48 pi^2) = (1/3) Q^2 in beta-function units -- exactly "
            f"1/4 of a Dirac fermion's (4/3) Q^2 (ratio {ratio:.6f}). This is the "
            f"correct scalar-QED contribution to the photon beta-function and the "
            f"first bosonic building block of the eventual -7 bosonic coefficient "
            f"(W gauge loop + ghost still to come)."
        ),
        key_result=f"scalar photon-VP pole = (1/3)Q^2 = 1/4 x Dirac fermion (ratio {ratio:.6f}). [P]",
        dependencies=["T_w_trace_native_photon_vp_pole_beta_function",
                      "T_w_trace_native_scalar_vp_transversality"],
        artifacts={"scalar_ff_pole": scalar_ff_pole, "fermion_ff_pole": ferm_ff_pole,
                   "ratio": ratio, "numerator_pole_err": np_err},
    )


def check_T_w_trace_native_scalar_vp_finite_closed_form_P() -> Dict[str, Any]:
    """T: scalar VP finite running == (e^2Q^2/16pi^2)(1/3)[ln(q^2/m^2)-8/3] [P]."""
    q2 = 91.1876 ** 2
    mx = 0.0
    per = {}
    for m in (0.3, 0.5):
        run = Pi_phi(1.0, q2, m) - Pi_phi(1.0, -1e-4 * m * m, m)
        an = _analytic_scalar_running(1.0, q2, m)
        rel = abs(run - an) / abs(an)
        per[m] = rel
        mx = max(mx, rel)
        check(rel < 5e-3, f"m={m}: scalar running {run:.6e} vs analytic {an:.6e} rel {rel:.2e}")
        check(run > 0, "scalar running must be positive (screening)")
    return _result(
        name="T_w_trace_native_scalar_vp_finite_closed_form: "
             "scalar VP finite running reproduces the scalar-QED closed form [P]",
        tier=4, epistemic="P",
        summary=(
            f"The on-shell-subtracted charged-scalar running Pi_phi(M_Z^2) - "
            f"Pi_phi(0) reproduces the scalar-QED closed form "
            f"(e^2 Q^2/16 pi^2)(1/3)[ln(q^2/m^2) - 8/3] to max rel {mx:.1e} -- the "
            f"leading coefficient 1/3 (one quarter of the fermion's 4/3) and the "
            f"scalar constant 8/3 (vs the fermion's 5/3). Confirms the finite part "
            f"of the scalar loop, not just its pole, with no external input."
        ),
        key_result=f"scalar VP running == (1/3)[ln(q^2/m^2)-8/3] closed form (max rel {mx:.1e}). [P]",
        dependencies=["T_w_trace_native_scalar_vp_pole_one_quarter",
                      "T_w_trace_native_delta_alpha_lep_timelike"],
        artifacts={"per_mass_rel": per, "max_rel_err": mx},
    )


def check_T_w_trace_native_bosonic_scalar_vp_scope_partial_P() -> Dict[str, Any]:
    """T: Goldstone piece of Pi_gamma_gamma done; W gauge loop + ghost OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_native_bosonic_scalar_photon_vp"] == 1, "scalar VP flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no APF-internal Delta r_rem evaluated by this rung")
    return _result(
        name="T_w_trace_native_bosonic_scalar_vp_scope_partial: "
             "Goldstone piece of bosonic Pi_gamma_gamma done; W gauge loop + ghost OPEN [P_structural]",
        tier=4, epistemic="P_structural_partial",
        summary=(
            "The first bosonic piece of the photon self-energy -- the charged "
            "Goldstone (scalar-QED) loop -- is built and validated three ways "
            "(transversality, the 1/4-of-a-fermion pole, the 8/3 finite constant), "
            "reusing the v24.3.86 UV-pole layer. Still OPEN toward the bosonic "
            "Pi_gamma_gamma and the APF-internal Delta r_rem: the W gauge-boson "
            "loop + seagull and the Faddeev-Popov ghost loop (which, summed with "
            "this Goldstone piece, give the -7 bosonic photon beta-function "
            "coefficient), then the bosonic Pi_WW/Pi_ZZ, the vertex+box delta_VB, "
            "and the Stage-4 UV cancellation. No Delta r_rem / M_W is produced; "
            "DIZET stays the publishable OS-W closure."
        ),
        key_result="Goldstone (scalar) photon-VP piece done; W gauge loop + ghost OPEN. [P_structural]",
        dependencies=["T_w_trace_native_scalar_vp_finite_closed_form"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_native_scalar_vp_transversality": check_T_w_trace_native_scalar_vp_transversality_P,
    "T_w_trace_native_scalar_vp_pole_one_quarter": check_T_w_trace_native_scalar_vp_pole_one_quarter_P,
    "T_w_trace_native_scalar_vp_finite_closed_form": check_T_w_trace_native_scalar_vp_finite_closed_form_P,
    "T_w_trace_native_bosonic_scalar_vp_scope_partial":
        check_T_w_trace_native_bosonic_scalar_vp_scope_partial_P,
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
