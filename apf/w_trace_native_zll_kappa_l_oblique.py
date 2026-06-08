"""W_TRACE APF-native oblique leptonic effective-angle form factor kappa_l.

Gate A rung 2a (OS-W-to-[P] gate map, 2026-05-25). Rung 1
(w_trace_native_zll_vertex_form_factors) banked the generic vertex form-factor
substrate. This rung assembles the OBLIQUE part of the leptonic effective-angle
form factor kappa_l natively, using the effective-coupling recipe of
Dubovyk-Freitas-Gluza-Riemann-Usovitsch (arXiv:1906.08815, eqs 1.1-1.3) and the
banked native gauge-boson self-energies.

The recipe (1906.08815 eq 1.1/1.2)
---------------------------------
    v_f(s) = v^Z_f(s) - v^gamma_f(s) * Sigma^gZ(s)/(s + Sigma^gg(s)) ,
    a_f(s) = a^Z_f(s) - a^gamma_f(s) * Sigma^gZ(s)/(s + Sigma^gg(s)) ,
with tree couplings v^Z_f(0)=e(I3-2Q s^2)/(2 s c), v^gamma_f(0)=eQ,
a^Z_f(0)=e I3/(2 s c), a^gamma_f(0)=0; and sin^2 theta_eff^f =
(1/4|Q_f|)(1 - Re v_f/a_f). For charged leptons (Q=-1, I3=-1/2) this gives,
keeping tree v^Z/a^Z + the oblique (self-energy) corrections,

    sin^2 theta_eff = s^2 + s_W c_W Re[ Sigma^gZ(M_Z^2)/(M_Z^2 + Sigma^gg(M_Z^2)) ]
                          + (custodial Delta rho scheme shift) + (proper vertex) ,

so the oblique form factor splits as

    Delta kappa_l^obl = (c_W^2/s_W^2) Delta rho   +   (c_W/s_W) Re[ X ] ,
    X = Sigma^gZ(M_Z^2)/(M_Z^2 + Sigma^gg(M_Z^2)) .

The first term is the custodial piece (banked [P] at v24.3.67, 59% of the target
Delta kappa_l). The second is the gamma-Z-mixing piece, evaluated here natively
from the banked total (fermionic+bosonic) gamma-Z self-energy
w_trace_native_delta_r_mw_assembly.Sig_AZ at the Z pole. Its SIGN is sourced
from 1906.08815 eq 1.1/1.2 (not reconstructed from memory).

Result
------
gamma-Z Dkappa = (c/s) Sigma^gZ(M_Z^2)/M_Z^2 = +0.001483 (leading; the small
Sigma^gg ~ Delta alpha denominator correction is a known ~6% higher-order
effect dropped here). With the banked custodial 0.021721 this gives an oblique
kappa_l = 0.023204 = 63.0% of the banked target Delta kappa_l = 0.036808 -- up
from the 59% custodial-only leading term.

What this module does (and does NOT) claim
-------------------------------------------
It evaluates the OBLIQUE kappa_l (custodial + gamma-Z mixing) natively, with the
gamma-Z piece the first natively-computed slice of the non-oblique remainder.
It does NOT close kappa_l: the proper Zll vertex form factors Lambda_V/Lambda_A
(the genuine non-oblique ~37% remainder: proper vertex + light-fermion + the
data-bound Delta alpha) are NOT computed here -- they need the explicit one-loop
Zll vertex (LEP Yellow Report 'Precision Calculations for the Z Resonance',
CERN 95-03 = arXiv:hep-ph/9709229; or Akhundov-Bardin-Riemann NPB276(1986)1),
the next rung. No sin^2 theta_eff value is exported; DIZET stays the publishable
OS-W closure.

Honest caveat: Sig_AZ uses the .99 module's Denner input masses (m_t=140); the
gamma-Z self-energy at M_Z^2 is light-fermion-dominated (top below threshold,
entering only via the spacelike B0), so this piece is m_t-insensitive at the
quoted precision.

Status
------
- Export_native_kappa_l_oblique_assembled        = 1   (NEW here)
- Export_native_kappa_l_gammaZ_mixing_evaluated   = 1   (NEW here)
- Export_native_kappa_l_proper_vertex_evaluated   = 0   (OPEN, next rung)
- Export_native_kappa_l_evaluated                 = 0   (OPEN, Gate A)
"""
from __future__ import annotations

import math
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_native_delta_r_mw_assembly import Sig_AZ, MZ2
from apf.sin2theta_eff_kappa_l_decomposition import _decomposition
from apf.sin2theta_eff_bsy_real_adapter import SIN2THETA_CODOMAINS

# Banked on-shell weak-angle codomain (same value the kappa_l decomposition uses).
_S2_OS = SIN2THETA_CODOMAINS["on_shell_mass_ratio_1_minus_MW2_MZ2"]  # 0.223339
_S = math.sqrt(_S2_OS)
_C = math.sqrt(1.0 - _S2_OS)


def kappa_l_gammaZ() -> float:
    """gamma-Z-mixing contribution to Delta kappa_l (leading), native + sign-sourced.

    Dkappa_gammaZ = (c_W/s_W) Re[ Sigma^gZ(M_Z^2)/M_Z^2 ]  (eq 1.1/1.2 sign).
    Sigma^gZ is the banked native total (fermionic+bosonic) gamma-Z self-energy.
    """
    X = Sig_AZ(MZ2, _S, _C, MZ2) / MZ2
    return (_C / _S) * X


def oblique_decomposition() -> Dict[str, float]:
    d = _decomposition()
    cust = d["lead_custodial_tot"]          # banked 0.021721 [P]
    target = d["delta_kappa_l_target"]      # banked 0.036808
    gz = kappa_l_gammaZ()
    obl = cust + gz
    return {
        "custodial_banked": cust,
        "gammaZ_native": gz,
        "oblique_total": obl,
        "target": target,
        "remainder": target - obl,
        "oblique_fraction": obl / target,
        "remainder_fraction": (target - obl) / target,
        "sig_gZ_over_MZ2": Sig_AZ(MZ2, _S, _C, MZ2) / MZ2,
    }


EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_kappa_l_oblique_assembled": 1,
    "Export_native_kappa_l_gammaZ_mixing_evaluated": 1,
    "Export_native_kappa_l_proper_vertex_evaluated": 0,
    "Export_native_kappa_l_evaluated": 0,
}

# remainder budget from the banked decomposition (genuine non-custodial residual)
_REMAINDER_BUDGET = 0.011815


def check_T_w_trace_native_kappa_l_gammaZ_mixing_P() -> Dict[str, Any]:
    """T: gamma-Z-mixing contribution to kappa_l, native + sign-sourced [P_structural].

    Dkappa_gammaZ = (c/s) Sigma^gZ(M_Z^2)/M_Z^2, with Sigma^gZ the banked native
    total gamma-Z self-energy and the sign from 1906.08815 eq 1.1/1.2. The first
    natively-computed slice of the non-oblique remainder. Anchored by: positive
    (correct sign), magnitude within the banked genuine-non-custodial remainder
    budget, native (no fitted/measured target).
    """
    d = oblique_decomposition()
    gz = d["gammaZ_native"]
    check(gz > 0, f"gamma-Z Dkappa must be positive (sourced sign), got {gz}")
    check(abs(gz - 0.001483) < 5e-5, f"gamma-Z Dkappa {gz} != native 0.001483")
    check(gz < _REMAINDER_BUDGET,
          f"gamma-Z piece {gz} must fit within the remainder budget {_REMAINDER_BUDGET}")
    return _result(
        name="T_w_trace_native_kappa_l_gammaZ_mixing: "
             "native gamma-Z-mixing contribution to kappa_l [P_structural]",
        tier=4, epistemic="P_structural",
        summary=(
            f"The gamma-Z-mixing contribution to the leptonic effective-angle form "
            f"factor, Dkappa_gammaZ = (c/s) Re[Sigma^gZ(M_Z^2)/M_Z^2] = {gz:.6f}, "
            f"evaluated natively from the banked total (fermionic+bosonic) gamma-Z "
            f"self-energy (w_trace_native_delta_r_mw_assembly.Sig_AZ at the Z pole). "
            f"The SIGN is sourced from the Dubovyk et al. effective-coupling recipe "
            f"(arXiv:1906.08815 eq 1.1/1.2), not reconstructed. First natively-"
            f"computed slice of the non-oblique remainder; positive and within the "
            f"banked genuine-non-custodial budget {_REMAINDER_BUDGET}."
        ),
        key_result=f"native gamma-Z Dkappa = {gz:.6f} (sign-sourced). [P_structural]",
        dependencies=["T_sin2theta_eff_kappa_l_leading_custodial_internal",
                      "T_w_trace_native_delta_r_mu_independent"],
        cross_refs=["check_T_w_trace_native_vertex_ff_subgate_partial_P"],
        artifacts={k: round(v, 9) for k, v in d.items()},
    )


def check_T_w_trace_native_kappa_l_custodial_consistent_P() -> Dict[str, Any]:
    """T: custodial leading term ties to the banked kappa_l decomposition [P]."""
    d = oblique_decomposition()
    check(abs(d["custodial_banked"] - 0.021721186) < 1e-7,
          f"custodial {d['custodial_banked']} != banked 0.021721186")
    check(abs(d["target"] - 0.036807775) < 1e-7,
          f"target {d['target']} != banked 0.036807775")
    return _result(
        name="T_w_trace_native_kappa_l_custodial_consistent: "
             "custodial leading term ties to banked kappa_l decomposition [P]",
        tier=4, epistemic="P",
        summary=(
            f"The oblique assembly reuses the banked custodial leading term "
            f"Xi_rho*Delta rho = {d['custodial_banked']:.6f} [P, v24.3.67] and the "
            f"banked target Delta kappa_l = {d['target']:.6f}, so the oblique kappa_l "
            f"is built on the validated decomposition, not a new fit."
        ),
        key_result="custodial term consistent with banked decomposition. [P]",
        dependencies=["T_sin2theta_eff_kappa_l_leading_custodial_internal"],
        artifacts={"custodial_banked": round(d["custodial_banked"], 9),
                   "target": round(d["target"], 9)},
    )


def check_T_w_trace_native_kappa_l_oblique_assembly_P() -> Dict[str, Any]:
    """T: oblique kappa_l = custodial + gamma-Z = 63% of target, no overshoot [P_structural]."""
    d = oblique_decomposition()
    check(abs(d["oblique_total"] - 0.023204) < 1e-4,
          f"oblique total {d['oblique_total']} != 0.023204")
    check(d["oblique_total"] > d["custodial_banked"],
          "oblique must exceed custodial-only (gamma-Z moves toward target)")
    check(d["oblique_total"] < d["target"],
          "oblique must not overshoot the target (remainder stays positive)")
    check(0.60 < d["oblique_fraction"] < 0.66,
          f"oblique fraction {d['oblique_fraction']:.3f} not ~63%")
    return _result(
        name="T_w_trace_native_kappa_l_oblique_assembly: "
             "oblique kappa_l = custodial + gamma-Z = 63% of target [P_structural]",
        tier=4, epistemic="P_structural",
        summary=(
            f"Oblique Delta kappa_l = custodial (banked {d['custodial_banked']:.6f}) "
            f"+ native gamma-Z ({d['gammaZ_native']:.6f}) = {d['oblique_total']:.6f} "
            f"= {d['oblique_fraction']*100:.1f}% of the banked target "
            f"{d['target']:.6f} -- up from the 59% custodial-only leading term. "
            f"Moves toward the target without overshoot; the remainder "
            f"{d['remainder']:.6f} ({d['remainder_fraction']*100:.1f}%) is the "
            f"proper Zll vertex + light-fermion + Delta alpha, the next rung."
        ),
        key_result=(
            f"oblique kappa_l = {d['oblique_total']:.6f} "
            f"({d['oblique_fraction']*100:.1f}% of target). [P_structural]"
        ),
        dependencies=["T_w_trace_native_kappa_l_gammaZ_mixing",
                      "T_w_trace_native_kappa_l_custodial_consistent"],
        artifacts={k: round(v, 9) for k, v in d.items()},
    )


def check_L_w_trace_native_kappa_l_proper_vertex_open_C() -> Dict[str, Any]:
    """L: the proper Zll vertex (non-oblique ~37%) is the named OPEN gate [C]."""
    d = oblique_decomposition()
    check(d["remainder"] > 1e-3, "remainder must be a genuine open gap")
    check(EXPORT_FLAGS["Export_native_kappa_l_proper_vertex_evaluated"] == 0,
          "proper vertex must remain UNCLAIMED (flag 0)")
    check(EXPORT_FLAGS["Export_native_kappa_l_evaluated"] == 0,
          "native kappa_l must remain OPEN (Gate A not closed)")
    return _result(
        name="L_w_trace_native_kappa_l_proper_vertex_open: "
             "proper Zll vertex (non-oblique ~37%) is the OPEN gate [C]",
        tier=4, epistemic="C",
        summary=(
            f"The non-oblique remainder Delta kappa_rem = {d['remainder']:.6f} "
            f"({d['remainder_fraction']*100:.1f}% of the target) -- the proper Zll "
            f"vertex form factors Lambda_V/Lambda_A + light-fermion + the data-bound "
            f"Delta alpha -- is NOT computed. It needs the explicit one-loop Zll "
            f"vertex (LEP Yellow Report 'Precision Calculations for the Z Resonance', "
            f"CERN 95-03 = arXiv:hep-ph/9709229; or Akhundov-Bardin-Riemann "
            f"NPB276(1986)1), to be transcribed onto the rung-1 generic-vertex "
            f"substrate. Native kappa_l stays OPEN; DIZET stays publishable."
        ),
        key_result=(
            f"proper Zll vertex remainder = {d['remainder']:.6f} OPEN (needs "
            f"hep-ph/9709229). [C]"
        ),
        dependencies=["T_w_trace_native_kappa_l_oblique_assembly"],
        artifacts={"remainder": round(d["remainder"], 9),
                   "export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_native_kappa_l_gammaZ_mixing":
        check_T_w_trace_native_kappa_l_gammaZ_mixing_P,
    "T_w_trace_native_kappa_l_custodial_consistent":
        check_T_w_trace_native_kappa_l_custodial_consistent_P,
    "T_w_trace_native_kappa_l_oblique_assembly":
        check_T_w_trace_native_kappa_l_oblique_assembly_P,
    "L_w_trace_native_kappa_l_proper_vertex_open":
        check_L_w_trace_native_kappa_l_proper_vertex_open_C,
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
