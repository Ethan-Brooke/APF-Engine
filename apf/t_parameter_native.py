"""APF-native Peskin-Takeuchi T parameter -- the fermionic (custodial) leg -- Tier-4.

Companion to the native S sector (apf/s_parameter_native.py,
apf/s_parameter_pure_gauge_constant_native.py, apf/s_higgs_finite_profile_native.py).
Where S is a slope at q^2 -> 0, T is a *value* at q^2 = 0: the custodial /
isospin-breaking self-energy difference, in Peskin-Takeuchi normalization

    alpha * T = Delta rho = Sigma^{WW}_T(0)/M_W^2 - Sigma^{ZZ}_T(0)/M_Z^2 .

The physical content of T is therefore Delta rho, and APF already carries the
custodial Delta rho natively: this module does NOT recompute it. It reads the
banked native fermionic Delta rho and states the named oblique observable T it
normalizes to, with an answer-free degenerate-limit gate and a magnitude
cross-check.

What is native here (the fermionic leg) [P]
-------------------------------------------
- Native fermionic Delta rho from the APF-owned PV substrate (Veltman rho
  function): ``w_trace_native_drho_top.drho_top_native`` (= 0.008304 at the
  physical (m_t, m_b); reproduces the banked gauge.L_W_mass value to 7e-5).
  The custodial breaking is top-dominated; light doublets are negligible by the
  per-doublet custodial structure (each doublet's UV pole is custodial-symmetric,
  banked ``w_trace_native_drho_per_doublet_custodial``).
- The native invariant is Delta rho itself (= alpha*T). Presenting it as the
  named observable T uses the conventional Peskin-Takeuchi normalization by
  alpha_em(M_Z): T = Delta rho / alpha. alpha here is the PT unit-conversion
  constant, NOT derived in this module (the gauge sector's native alpha lives
  elsewhere and is deliberately not leaned on); it is also not a smuggled
  *target* -- the experimental T value is never read. So the [P] content is the
  native fermionic Delta rho; "T_ferm" is that same physics in PT units.

Gate-0 (answer-free, internal -- the spine)
-------------------------------------------
T -> 0 in the degenerate (custodial-symmetric) limit m_U = m_D. We drive
``drho_top_native`` to m_b = m_t and confirm Delta rho -> 0 (~1e-15). This is the
exact analog of the D3-tadpole-cancels gate in the native S Higgs profile: a
comparator-free zero that the assembly must reproduce before any magnitude is
quoted. The reference T value is NEVER an input; the magnitude below is a final
cross-check only.

Honest scope (what is NOT claimed)
----------------------------------
- This is the FERMIONIC leg of T only. The BOSONIC Delta rho is held [C]: in the
  R_xi route it carries a universal UV pole +4 (banked
  ``w_trace_native_drho_bosonic_pole_universal``) that the Stage-4 counterterms
  must absorb, so no finite native bosonic Delta rho exists yet. A fully native T
  awaits the gauge-invariant BFM/PT bosonic Delta rho at q^2 = 0 (the same
  machinery that closed the bosonic S constant in v24.3.259) -- the next rung.
- Scope-fenced *reproduction*: native ingredients reproducing the known PT T,
  same grade ceiling as the native S modules. Not an A1-from-scratch derivation,
  not a loop-renormalized OS T, no measured-target consumption.

Status
------
- Export_T_parameter_fermionic_native_P  = 1
- Export_T_parameter_bosonic_native_P     = 0   (OPEN -- BFM bosonic Delta rho rung)
- Export_T_parameter_full_native_P        = 0   (OPEN -- needs the bosonic leg)
"""
from __future__ import annotations

from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_native_drho_top import drho_top_native, _M_T
from apf.w_trace_native_gauge_boson_drho_uv import drho_pole_bos

# PT normalization constant: conventional alpha_em(M_Z). T's native content is
# Delta rho; alpha is the PT unit conversion, not an input target.
_INV_ALPHA_EM_MZ = 127.93
_ALPHA_EM_MZ = 1.0 / _INV_ALPHA_EM_MZ
_M_B = 4.18  # physical b-quark mass (GeV); the light doublets are negligible.

EXPORT_FLAGS: Dict[str, int] = {
    "Export_T_parameter_fermionic_native_P": 1,
    "Export_T_parameter_bosonic_native_P": 0,
    "Export_T_parameter_full_native_P": 0,
}


def delta_rho_fermionic_native(m_b: float = _M_B) -> float:
    """Native fermionic custodial Delta rho (top-dominated), read from the PV substrate."""
    return drho_top_native(m_b)


def t_parameter_fermionic_native(m_b: float = _M_B, alpha: float = _ALPHA_EM_MZ) -> float:
    """Fermionic leg of the Peskin-Takeuchi T: T_ferm = Delta rho_ferm / alpha."""
    return delta_rho_fermionic_native(m_b) / alpha


def check_T_T_parameter_fermionic_native_P() -> Dict[str, Any]:
    """T: Peskin-Takeuchi T fermionic leg native (alpha*T = native Delta rho), degenerate gate [P]."""
    drho = delta_rho_fermionic_native(_M_B)
    t_ferm = t_parameter_fermionic_native(_M_B)

    # Gate-0 (answer-free, comparator-free): T -> 0 in the degenerate custodial limit.
    drho_deg = delta_rho_fermionic_native(_M_T)          # m_b driven up to m_t
    scale = abs(drho) if drho else 1.0
    deg_rel = abs(drho_deg) / scale
    check(deg_rel < 1e-9,
          f"degenerate-limit Delta rho must vanish (custodial symmetry); rel {deg_rel:.2e}")

    # Monotone custodial restoration: Delta rho strictly shrinks as m_b -> m_t.
    seq = [abs(delta_rho_fermionic_native(mb)) for mb in (_M_B, 50.0, 150.0, 162.0)]
    monotone = all(seq[i] > seq[i + 1] for i in range(len(seq) - 1))
    check(monotone, "Delta rho must shrink monotonically toward the degenerate limit")

    # alpha*T == Delta rho exactly (the PT identity, by construction).
    identity_rel = abs(_ALPHA_EM_MZ * t_ferm - drho) / scale
    check(identity_rel < 1e-12, f"alpha*T must equal Delta rho; rel {identity_rel:.2e}")

    # Magnitude CROSS-CHECK only (never an input): top-dominated T ~ O(1).
    mag_ok = 0.9 < t_ferm < 1.3

    # Scope fence: the bosonic Delta rho is UV-divergent (+4 pole) -> bosonic T is [C].
    bos_pole = drho_pole_bos()
    bosonic_open = abs(bos_pole - 4.0) < 1e-6

    return _result(
        name="T_T_parameter_fermionic_native: Peskin-Takeuchi T fermionic leg native "
             "(alpha*T = native Delta rho), degenerate-limit gate [P]",
        tier=4, epistemic="P",
        summary=(
            f"The fermionic (custodial) leg of the Peskin-Takeuchi T parameter is native: "
            f"alpha*T = Delta rho, with Delta rho read from the APF-owned native PV substrate "
            f"(Veltman rho function, top-dominated) = {drho:.6f}, giving T_ferm = {t_ferm:.4f} "
            f"at the conventional alpha_em(M_Z) = 1/{_INV_ALPHA_EM_MZ}. The answer-free spine is "
            f"the degenerate custodial limit: driving m_b -> m_t sends Delta rho -> 0 "
            f"(rel {deg_rel:.1e}), the q^2=0 analog of the seagull-tadpole cancellation in the "
            f"native S Higgs profile, and Delta rho shrinks monotonically toward it. The O(1), "
            f"top-dominated magnitude is a final cross-check only (the reference T is never an "
            f"input). SCOPE: this is the fermionic leg; the bosonic Delta rho is UV-divergent "
            f"(universal +4 pole, here {bos_pole:.3f}) and held [C] pending the gauge-invariant "
            f"BFM/PT bosonic rho at q^2=0 -- a fully native T awaits that rung."
        ),
        key_result=(
            f"T_ferm = Delta rho/alpha = {t_ferm:.4f} (native fermionic leg [P]); "
            f"degenerate gate Delta rho->0 (rel {deg_rel:.0e}); bosonic leg [C] (+4 pole). "
            f"mag cross-check {'OK' if mag_ok else 'OUT'}."
        ),
        dependencies=[
            "T_w_trace_native_drho_top_reproduces_banked",
            "T_w_trace_native_drho_per_doublet_custodial",
        ],
        artifacts={
            "delta_rho_fermionic_native": drho,
            "t_ferm": t_ferm,
            "inv_alpha_em_mz": _INV_ALPHA_EM_MZ,
            "degenerate_rel": deg_rel,
            "alpha_T_identity_rel": identity_rel,
            "magnitude_cross_check_ok": mag_ok,
            "bosonic_pole": bos_pole,
            "bosonic_leg_open_C": bosonic_open,
        },
    )


CHECKS = {
    "check_T_T_parameter_fermionic_native_P": check_T_T_parameter_fermionic_native_P,
}


def register(registry):
    registry.update(CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    print(json.dumps(run_all(), indent=2, default=str))
