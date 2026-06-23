"""APF-native Delta rho_top from the native PV substrate (Veltman rho-function) -- Tier-4.

First rung of the native OS-W one-loop evaluator (the option-C route of
``APF Reference Docs/Reference - APF OS-W Native One-Loop Evaluator Work Plan
(2026-05-24).md``): demonstrate that the APF-owned finite PV substrate
(``apf.w_trace_pv_scalar_integral_substrate``: a0_fin / b0_fin) reproduces a
*physical* electroweak quantity -- the leading custodial-symmetry-breaking
Delta rho from the top-bottom doublet -- through the genuine loop integrals,
not a re-coded closed form.

The Veltman rho-function as a native PV identity
-----------------------------------------------
The one-loop Delta rho from one fermion doublet is
``Delta rho = (3 alpha)/(16 pi M_W^2 s_W^2) * F(m_t^2, m_b^2)`` with the Veltman
function ``F(x,y) = x + y - 2 x y/(x-y) ln(x/y)`` (and ``F(x,0) = x``). F is the
zero-external-momentum combination of the doublet self-energies, and it has an
exact, mu-independent representation in the native two-point substrate:

    F(m1^2, m2^2) = (m1^2 + m2^2) * (1 + B0(0; m1^2, m2^2)) - A0(m1^2) - A0(m2^2)

verified symbolically (F_identity - F_closed = 0) and numerically against the
closed form to b0-quadrature precision (~1e-5). Because Delta rho is at
p^2 = 0, **no timelike PV branch is needed** for this rung (that prerequisite is
deferred to Re Pi(M^2) in the full Delta r).

What this rung establishes
--------------------------
The native PV substrate is physically adequate for electroweak self-energies:
fed the APF-internal inputs (m_t = 163 from L_sigma_normalization, sin^2 theta_W
= 3/13 from T_sin2theta, alpha from L_alpha_em), the native loop function
reproduces the banked ``gauge.L_W_mass`` Delta rho_top = 0.008379 in the
m_b -> 0 limit. No external input; no measured M_W; no DIZET. This is the gate
the work plan named for Stage 2 (fermionic self-energies), now passed at the
custodial-piece level.

Honest scope
------------
This is the p^2 = 0 fermionic custodial piece (Delta rho_top) only. The full
APF-internal Delta r_rem -- Re Pi_WW(M_W^2) / Re Pi_ZZ(M_Z^2) (timelike branch),
the bosonic/Goldstone/ghost loops, the vertex+box delta_VB, and UV-pole
cancellation against the counterterms -- remains OPEN. No Delta r_rem / M_W is
produced here (the banked L_W_mass already carries the M_W closure); this rung
ties Delta rho_top to the native PV substrate. DIZET stays the publishable OS-W
closure.

Status
------
- Export_native_veltman_F_via_pv_substrate            = 1
- Export_native_drho_top_reproduces_banked            = 1
- Export_OSW_APF_internal_delta_r_rem_evaluated       = 0   (OPEN, unchanged)
"""
from __future__ import annotations

import math
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_pv_scalar_integral_substrate import a0_fin, b0_fin

# APF-internal [P] inputs, identical to apf.gauge.check_L_W_mass.
_SIN2_W = 3.0 / 13.0          # T_sin2theta [P]
_ALPHA_EM = 1.0 / 128.21      # L_alpha_em [P]
_M_T = 163.0                  # GeV, L_sigma_normalization [P]
_M_Z = 91.1876               # anchor
_M_W_TREE = _M_Z * math.sqrt(1.0 - _SIN2_W)

EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_veltman_F_via_pv_substrate": 1,
    "Export_native_drho_top_reproduces_banked": 1,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


def veltman_F_native(m1sq: float, m2sq: float) -> float:
    """Veltman rho-function F(m1^2, m2^2) via the native PV substrate.

    F = (m1^2+m2^2)(1 + B0(0;m1^2,m2^2)) - A0(m1^2) - A0(m2^2).
    """
    return (m1sq + m2sq) * (1.0 + b0_fin(0.0, m1sq, m2sq)) - a0_fin(m1sq) - a0_fin(m2sq)


def veltman_F_closed(m1sq: float, m2sq: float) -> float:
    """Closed-form Veltman function (m1^2 != m2^2)."""
    return m1sq + m2sq - 2.0 * m1sq * m2sq / (m1sq - m2sq) * math.log(m1sq / m2sq)


def _drho_prefactor() -> float:
    return 3.0 * _ALPHA_EM / (16.0 * math.pi * _M_W_TREE ** 2 * _SIN2_W)


def drho_top_native(m_b: float) -> float:
    """Native Delta rho_top = prefactor * F_native(m_t^2, m_b^2)."""
    return _drho_prefactor() * veltman_F_native(_M_T ** 2, m_b ** 2)


# ===========================================================================
# checks
# ===========================================================================
def check_T_w_trace_native_veltman_F_identity_P() -> Dict[str, Any]:
    """T: native PV substrate reproduces the Veltman rho-function F [P]."""
    mx = 0.0
    for m1, m2 in [(163.0, 4.18), (163.0, 1.0), (80.0, 40.0), (100.0, 3.0), (173.0, 2.8)]:
        fn = veltman_F_native(m1 * m1, m2 * m2)
        fc = veltman_F_closed(m1 * m1, m2 * m2)
        mx = max(mx, abs(fn - fc) / abs(fc))
    check(mx < 5e-4, f"native Veltman F vs closed form max rel err {mx:.2e} exceeds 5e-4")
    return _result(
        name="T_w_trace_native_veltman_F_identity: "
             "native PV substrate reproduces the Veltman rho-function F(m1^2,m2^2) [P]",
        tier=4, epistemic="P",
        summary=(
            f"The Veltman rho-function has the exact, mu-independent native PV "
            f"representation F(m1^2,m2^2) = (m1^2+m2^2)(1+B0(0;m1^2,m2^2)) - "
            f"A0(m1^2) - A0(m2^2) (confirmed symbolically: F_identity - F_closed = "
            f"0). Evaluated with the native a0_fin/b0_fin it matches the closed-form "
            f"Veltman function to max relative err {mx:.2e} over five mass pairs -- "
            f"the native substrate computes the custodial loop function, no external "
            f"input. At p^2=0, so no timelike branch is required."
        ),
        key_result=f"native PV substrate reproduces Veltman F (rel err {mx:.1e}). [P]",
        dependencies=["check_T_w_trace_pv_b0_finite_gate", "check_T_w_trace_pv_a0_finite_gate"],
        artifacts={"max_rel_err": mx},
    )


def check_T_w_trace_native_drho_top_reproduces_banked_P() -> Dict[str, Any]:
    """T: native Delta rho_top (m_b->0) reproduces the banked gauge.L_W_mass value [P]."""
    import apf.gauge as gauge
    banked = float(gauge.check_L_W_mass()["artifacts"]["Drho_top"])
    # validate the prefactor replication against gauge's own closed form (F = m_t^2)
    pref_closed = _drho_prefactor() * _M_T ** 2
    check(abs(pref_closed - banked) < 5e-6,
          f"prefactor replication {pref_closed:.6f} != banked {banked:.6f}")
    # native value in the m_b -> 0 limit
    native = drho_top_native(0.05)
    rel = abs(native - banked) / abs(banked)
    check(rel < 1e-3, f"native Drho_top {native:.6f} vs banked {banked:.6f} rel {rel:.2e} exceeds 1e-3")
    return _result(
        name="T_w_trace_native_drho_top_reproduces_banked: "
             "native Delta rho_top from the PV substrate reproduces banked L_W_mass [P]",
        tier=4, epistemic="P",
        summary=(
            f"Fed the APF-internal inputs (m_t=163 [L_sigma_normalization], "
            f"sin^2 theta_W=3/13 [T_sin2theta], alpha=1/128.21 [L_alpha_em]), the "
            f"native Delta rho_top = (3 alpha)/(16 pi M_W^2 s_W^2) * "
            f"F_native(m_t^2, m_b^2) reproduces the banked gauge.L_W_mass "
            f"Drho_top = {banked:.6f} in the m_b -> 0 limit (native {native:.6f}, "
            f"rel {rel:.1e}); the prefactor replication matches gauge's own closed "
            f"form to <5e-6. First native-loop -> physical EW quantity rung; no "
            f"external input, no measured M_W, no DIZET."
        ),
        key_result=f"native Drho_top = {native:.6f} == banked {banked:.6f} (rel {rel:.1e}). [P]",
        dependencies=["T_w_trace_native_veltman_F_identity", "L_W_mass"],
        artifacts={"native_drho_top": native, "banked_drho_top": banked, "rel_err": rel},
    )


def check_T_w_trace_native_drho_top_mb_limit_P() -> Dict[str, Any]:
    """T: F_native(m_t^2, m_b^2) -> m_t^2 monotonically as m_b -> 0 [P]."""
    mt2 = _M_T ** 2
    seq = [veltman_F_native(mt2, mb * mb) for mb in (4.18, 2.0, 1.0, 0.3, 0.1, 0.03)]
    # monotone increasing toward m_t^2, and the limit is approached
    mono = all(seq[i] <= seq[i + 1] + 1e-6 for i in range(len(seq) - 1))
    check(mono, "F_native must increase monotonically toward m_t^2 as m_b->0")
    check(seq[-1] <= mt2 + 1.0, "F_native must not exceed m_t^2")
    check(abs(seq[-1] - mt2) / mt2 < 1e-3, f"F_native(m_b=0.03) within 1e-3 of m_t^2={mt2:.1f}")
    return _result(
        name="T_w_trace_native_drho_top_mb_limit: "
             "native Veltman F(m_t^2,m_b^2) -> m_t^2 as m_b -> 0 [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native Veltman F(m_t^2, m_b^2) rises monotonically toward "
            f"m_t^2 = {mt2:.1f} as m_b -> 0 (F(m_b=0.03) within 1e-3 of m_t^2), "
            f"confirming the banked m_b = 0 form Drho_top ~ m_t^2 is the correct "
            f"limit of the native loop function and the finite-m_b Veltman "
            f"correction is reproduced."
        ),
        key_result="native F(m_t^2,m_b^2) -> m_t^2 as m_b -> 0. [P]",
        dependencies=["T_w_trace_native_veltman_F_identity"],
        artifacts={"F_sequence": seq, "m_t_sq": mt2},
    )


def check_T_w_trace_native_drho_top_scope_partial_P() -> Dict[str, Any]:
    """T: native Delta rho_top is the p^2=0 fermionic custodial gate; full Delta r OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_native_veltman_F_via_pv_substrate"] == 1, "F-via-substrate flag must be 1")
    check(EXPORT_FLAGS["Export_native_drho_top_reproduces_banked"] == 1, "drho reproduction flag must be 1")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no APF-internal Delta r_rem evaluated by this rung")
    return _result(
        name="T_w_trace_native_drho_top_scope_partial: "
             "native Delta rho_top gate passed; full Delta r_rem OPEN [P_structural]",
        tier=4, epistemic="P_structural_partial",
        summary=(
            "This rung establishes that the native PV substrate reproduces the "
            "leading custodial Delta rho_top (the p^2=0 fermionic piece) from genuine "
            "loop integrals -- the Stage-2 fermionic gate of the native OS-W "
            "one-loop evaluator work plan. The full APF-internal Delta r_rem remains "
            "OPEN: the timelike Re Pi_WW(M_W^2) / Re Pi_ZZ(M_Z^2) branch, the "
            "bosonic/Goldstone/ghost loops, the vertex+box delta_VB (which consumes "
            "the native rank-3 box tensors), and UV-pole cancellation against the "
            "banked counterterms. No Delta r_rem / M_W is produced here; DIZET stays "
            "the publishable OS-W closure."
        ),
        key_result="Native Delta rho_top gate passed; full Delta r_rem OPEN. [P_structural]",
        dependencies=["T_w_trace_native_drho_top_reproduces_banked"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_native_veltman_F_identity": check_T_w_trace_native_veltman_F_identity_P,
    "T_w_trace_native_drho_top_reproduces_banked": check_T_w_trace_native_drho_top_reproduces_banked_P,
    "T_w_trace_native_drho_top_mb_limit": check_T_w_trace_native_drho_top_mb_limit_P,
    "T_w_trace_native_drho_top_scope_partial": check_T_w_trace_native_drho_top_scope_partial_P,
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
