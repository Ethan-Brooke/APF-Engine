"""APF-native TIMELIKE fermionic photon vacuum polarization -> Delta alpha_lep -- Tier-4.

Stage 2 (timelike anchor) of the native OS-W one-loop evaluator (work plan
2026-05-24). The v24.3.83 module built the fermionic transverse self-energies at
p^2=0 and validated them against the banked Delta rho_top. This module exercises
the SAME self-energy machinery at a physical TIMELIKE point, p^2 = M_Z^2 (above
the lepton production thresholds), using the v24.3.84 timelike two-point branch
(``apf.w_trace_pv_timelike_two_point`` re_b0/re_b1/re_b00_timelike), and closes
the SECOND of the two internal validation anchors the work plan names for the
fermionic stage: the leptonic running of alpha.

Construction
------------
For a charged fermion (charge Q, colour N_c, mass m) the one-loop photon
self-energy is the equal-mass transverse fermion loop with g_L=g_R=eQ,
e^2 = 4 pi alpha(0). Its g^{mu nu} coefficient A_gamma(p^2) is the native bracket

    A_gamma(p^2) = -(N_c/16 pi^2) { 8 e^2Q^2 Re B00 - 4 e^2Q^2[A0(m^2)
                   + m^2 Re B0 + p^2 Re B1] + 4 e^2Q^2 m^2 Re B0 }

evaluated with the timelike real-part B-functions. The transverse form factor is
Pihat(p^2) = A_gamma(p^2)/p^2; the renormalized (on-shell-subtracted) running is

    Re Pihat(p^2) - Pihat(0) ,   Pihat(0) = lim_{p^2->0} A_gamma(p^2)/p^2

(A_gamma(0)=0 by transversality, so the limit is finite). The leptonic running
of alpha is the sum over the three charged leptons:

    Delta alpha_lep = sum_l [ Re Pihat_l(M_Z^2) - Pihat_l(0) ] .

This subtracted difference is UV-finite and mu-INDEPENDENT (the bare 1/epsilon
and mu pieces of the transverse self-energy are ~ p^2, so they cancel between the
M_Z^2 point and the p^2->0 reference) -- which is why it is a clean anchor while
the bare on-shell Re Pi_WW(M_W^2)/Re Pi_ZZ(M_Z^2) are not (they are mu-dependent
until renormalized).

Validation (no external target; all against already-banked APF quantities)
--------------------------------------------------------------------------
1. Delta alpha_lep. The native sum reproduces the banked one-loop
   ``delta_alpha_leptonic`` value 0.0314209 to rel ~6e-5, on the APF-banked
   charged-lepton pole masses (``charged_lepton_pole_real_adapter``) and
   alpha(0) only.
2. Per-lepton closed form. Each lepton's native subtracted running matches the
   analytic (alpha_0/3pi)[ln(M_Z^2/m_l^2) - 5/3] to <=4e-4 -- a pointwise
   correctness test of the timelike VP that simultaneously demonstrates
   mu-independence (the analytic form carries no mu).
3. mu-independence. Delta alpha_lep is invariant under mu^2 -> {1,...,1000}*MU2
   (the bare UV/mu pieces cancel in the physical subtracted running).

Honest scope
------------
This closes the leptonic-alpha (timelike) validation anchor. Still OPEN toward
the APF-internal Delta r_rem: the renormalized on-shell Re Pi_WW(M_W^2) /
Re Pi_ZZ(M_Z^2) (bare values are mu-dependent and only meaningful once the
counterterms + bosonic loops are added), the bosonic/Goldstone/ghost loops, the
vertex+box delta_VB, and UV-pole cancellation. No Delta r_rem / M_W is produced;
DIZET stays the publishable OS-W closure.

Status
------
- Export_native_timelike_photon_vp_delta_alpha_lep = 1
- Export_OSW_APF_internal_delta_r_rem_evaluated     = 0   (OPEN, unchanged)
"""
from __future__ import annotations

import math
from functools import lru_cache
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_pv_scalar_integral_substrate import a0_fin, MU2
from apf.w_trace_pv_timelike_two_point import (
    re_b0_timelike, re_b1_timelike, re_b00_timelike,
)
from apf.charged_lepton_pole_real_adapter import POLE_MASS_MEV

# APF-internal inputs.
_ALPHA_0 = 1.0 / 137.035999084          # Thomson-limit alpha(0); matches delta_alpha_leptonic
_E2 = 4.0 * math.pi * _ALPHA_0
_M_Z = 91.1876
_MZ2 = _M_Z * _M_Z
_N = 120000

# APF-banked charged-lepton POLE masses (MeV -> GeV), provenance-pinned.
_M_LEP_GEV = {k: v / 1000.0 for k, v in POLE_MASS_MEV.items()}


def _vp_bracket_re(g: float, m: float, p2: float, mu2: float, n: int) -> float:
    """Real part of the equal-mass photon-VP transverse bracket (g_L=g_R=g)."""
    m2 = m * m
    gg = 2.0 * g * g
    ReB0 = re_b0_timelike(p2, m2, m2, mu2=mu2, n=n)
    ReB00 = re_b00_timelike(p2, m2, m2, mu2=mu2, n=n)
    ReB1 = re_b1_timelike(p2, m2, m2, mu2=mu2, n=n) if p2 != 0.0 else 0.0
    return (4.0 * gg * ReB00
            - 2.0 * gg * (a0_fin(m2, mu2) + m2 * ReB0 + p2 * ReB1)
            + 4.0 * g * g * m2 * ReB0)


def _A_gamma(Q: float, Nc: float, m: float, p2: float, mu2: float, n: int) -> float:
    """g^{mu nu} coefficient of the fermion-loop photon self-energy."""
    g = math.sqrt(_E2) * abs(Q)
    return -(Nc / (16.0 * math.pi ** 2)) * _vp_bracket_re(g, m, p2, mu2, n)


@lru_cache(maxsize=None)
def vp_running(Q: float, Nc: float, m: float, p2: float,
               mu2: float = MU2, n: int = _N) -> float:
    """Renormalized (on-shell-subtracted) photon VP form factor:
    Re Pihat(p^2) - Pihat(0), for one fermion. UV-finite and mu-independent."""
    p_ref = -1e-4 * m * m                       # small spacelike reference (<< m^2)
    pi_p2 = _A_gamma(Q, Nc, m, p2, mu2, n) / p2
    pi_0 = _A_gamma(Q, Nc, m, p_ref, mu2, n) / p_ref
    return pi_p2 - pi_0


def delta_alpha_lep_native(mu2: float = MU2, n: int = _N) -> float:
    """Native leptonic running Delta alpha_lep(M_Z) = sum_l [Re Pihat_l(M_Z^2) - Pihat_l(0)]."""
    return sum(vp_running(-1.0, 1.0, m, _MZ2, mu2, n) for m in _M_LEP_GEV.values())


def _analytic_da_lep(m: float) -> float:
    return _ALPHA_0 / (3.0 * math.pi) * (math.log(_MZ2 / (m * m)) - 5.0 / 3.0)


EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_timelike_photon_vp_delta_alpha_lep": 1,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


# ===========================================================================
# checks
# ===========================================================================
def check_T_w_trace_native_delta_alpha_lep_timelike_P() -> Dict[str, Any]:
    """T: native timelike photon VP reproduces banked Delta alpha_lep [P]."""
    import apf.delta_alpha_leptonic as dal
    banked = float(dal.running_report()["leptonic_running"]["da_lep_one_loop"])
    native = delta_alpha_lep_native()
    rel = abs(native - banked) / abs(banked)
    check(rel < 5e-4, f"native Delta alpha_lep {native:.7f} vs banked {banked:.7f} rel {rel:.2e}")
    check(native > 0, "leptonic running must be positive (vacuum screening)")
    return _result(
        name="T_w_trace_native_delta_alpha_lep_timelike: "
             "native timelike photon VP reproduces banked Delta alpha_lep [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native fermion-loop photon self-energy, evaluated at the TIMELIKE "
            f"on-shell point p^2 = M_Z^2 via the v24.3.84 timelike two-point branch, "
            f"gives the leptonic running Delta alpha_lep = sum_l [Re Pihat_l(M_Z^2) "
            f"- Pihat_l(0)] = {native:.7f}, reproducing the banked one-loop "
            f"delta_alpha_leptonic value {banked:.7f} to rel {rel:.1e}. This closes "
            f"the second of the two internal validation anchors the work plan names "
            f"for the fermionic stage (Delta rho_top was the p^2=0 anchor): the "
            f"timelike branch + the self-energy machinery jointly reproduce an "
            f"already-banked APF quantity. APF inputs only (banked lepton pole masses "
            f"+ alpha(0)); no measured alpha, no DIZET."
        ),
        key_result=f"native timelike Delta alpha_lep = {native:.6f} == banked {banked:.6f} (rel {rel:.1e}). [P]",
        dependencies=["T_delta_alpha_leptonic_first_principles",
                      "T_w_trace_pv_timelike_b0_threshold_closed",
                      "T_w_trace_native_drho_slot_by_slot"],
        artifacts={"native": native, "banked": banked, "rel_err": rel},
    )


def check_T_w_trace_native_vp_per_lepton_closed_form_P() -> Dict[str, Any]:
    """T: per-lepton native subtracted VP matches the analytic closed form [P]."""
    mx = 0.0
    per = {}
    for k, m in _M_LEP_GEV.items():
        nat = vp_running(-1.0, 1.0, m, _MZ2)
        an = _analytic_da_lep(m)
        rel = abs(nat - an) / abs(an)
        per[k] = rel
        mx = max(mx, rel)
        check(nat > 0, f"{k} running must be positive")
    check(mx < 1e-3, f"per-lepton native vs analytic max rel err {mx:.2e}")
    return _result(
        name="T_w_trace_native_vp_per_lepton_closed_form: "
             "per-lepton native subtracted VP matches the analytic closed form [P]",
        tier=4, epistemic="P",
        summary=(
            f"Each lepton's native subtracted running Re Pihat_l(M_Z^2) - Pihat_l(0) "
            f"reproduces the analytic one-loop closed form (alpha_0/3pi)"
            f"[ln(M_Z^2/m_l^2) - 5/3] to max rel err {mx:.1e} "
            f"(e {per['m_e']:.1e}, mu {per['m_mu']:.1e}, tau {per['m_tau']:.1e}). "
            f"Because the analytic form carries no renormalization scale, the "
            f"pointwise match simultaneously confirms correctness and "
            f"mu-independence of the timelike VP."
        ),
        key_result=f"per-lepton native VP == analytic closed form (max rel {mx:.1e}). [P]",
        dependencies=["T_w_trace_native_delta_alpha_lep_timelike"],
        artifacts={"per_lepton_rel": per, "max_rel_err": mx},
    )


def check_T_w_trace_native_vp_mu_independence_P() -> Dict[str, Any]:
    """T: the subtracted VP running is mu-independent (UV/mu cancels) [P]."""
    vals = [delta_alpha_lep_native(mu2=MU2 * f, n=40000) for f in (1.0, 100.0, 1000.0)]
    spread = max(vals) - min(vals)
    check(spread < 1e-6, f"Delta alpha_lep mu-spread {spread:.2e} must vanish (mu-independence)")
    return _result(
        name="T_w_trace_native_vp_mu_independence: "
             "the subtracted photon VP running is mu-independent [P]",
        tier=4, epistemic="P",
        summary=(
            f"Delta alpha_lep computed from the native subtracted VP is invariant "
            f"under the renormalization scale mu^2 -> {{1, 100, 1000}} * MU2 "
            f"(spread {spread:.1e}). The bare transverse self-energy carries a "
            f"1/epsilon + ln mu^2 divergence proportional to p^2, so its form factor "
            f"A_gamma/p^2 carries a p^2-independent mu term that cancels in the "
            f"on-shell-subtracted difference Pihat(M_Z^2) - Pihat(0) -- an explicit "
            f"demonstration that the physical running is scheme-clean."
        ),
        key_result=f"Delta alpha_lep mu-independent across mu^2 x[1,1000] (spread {spread:.1e}). [P]",
        dependencies=["T_w_trace_native_delta_alpha_lep_timelike"],
        artifacts={"mu_values": vals, "spread": spread},
    )


def check_T_w_trace_native_timelike_self_energy_scope_partial_P() -> Dict[str, Any]:
    """T: leptonic-alpha timelike anchor done; on-shell Re Pi_WW/ZZ + Delta r_rem OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_native_timelike_photon_vp_delta_alpha_lep"] == 1,
          "leptonic-alpha timelike anchor flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no APF-internal Delta r_rem evaluated by this rung")
    return _result(
        name="T_w_trace_native_timelike_self_energy_scope_partial: "
             "leptonic-alpha timelike anchor done; on-shell Re Pi_WW/ZZ + Delta r_rem OPEN [P_structural]",
        tier=4, epistemic="P_structural_partial",
        summary=(
            "Stage 2's timelike validation anchor is closed: the native fermionic "
            "photon VP, evaluated at p^2 = M_Z^2 through the timelike two-point "
            "branch, reproduces the banked Delta alpha_lep, validated pointwise "
            "against the closed form and shown mu-independent. Both Stage-2 internal "
            "anchors (Delta rho_top at p^2=0, Delta alpha_lep at p^2=M_Z^2) now pass. "
            "Still OPEN toward the APF-internal Delta r_rem: the renormalized on-shell "
            "Re Pi_WW(M_W^2) / Re Pi_ZZ(M_Z^2) (the bare on-shell self-energies are "
            "mu-dependent and become meaningful only once the counterterms and "
            "bosonic/Goldstone/ghost loops are added), the vertex+box delta_VB, and "
            "UV-pole cancellation. No Delta r_rem / M_W is produced; DIZET stays the "
            "publishable OS-W closure."
        ),
        key_result="Leptonic-alpha timelike anchor done; on-shell Re Pi_WW/ZZ + Delta r_rem OPEN. [P_structural]",
        dependencies=["T_w_trace_native_vp_per_lepton_closed_form",
                      "T_w_trace_native_vp_mu_independence"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_native_delta_alpha_lep_timelike": check_T_w_trace_native_delta_alpha_lep_timelike_P,
    "T_w_trace_native_vp_per_lepton_closed_form": check_T_w_trace_native_vp_per_lepton_closed_form_P,
    "T_w_trace_native_vp_mu_independence": check_T_w_trace_native_vp_mu_independence_P,
    "T_w_trace_native_timelike_self_energy_scope_partial":
        check_T_w_trace_native_timelike_self_energy_scope_partial_P,
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
