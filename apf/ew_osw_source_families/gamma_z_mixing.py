"""Fail-closed coefficient kernels for the OS-W photon-Z mixing family.

This module intentionally computes only coefficient-level maps:
- Delta_r_gammaZ from Pi_Zgamma(0)
- Delta_kappa_gammaZ from Re Pi_Zgamma(mZ^2)

It does not compute the self-energy Pi_Zgamma itself.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping, Any

FORBIDDEN_INPUTS = {
    "measured_M_W_value",
    "DIZET_ZFITTER_aggregate_output",
    "published_total_SM_M_W_as_component_value",
    "fitted_counterterm",
    "post_hoc_tolerance",
    "four_over_5063_weak_angle_shortcut",
    "measured_sin2theta_eff",
}


class ForbiddenInputError(ValueError):
    """Raised when an input card consumes a forbidden target or shortcut."""


def guard_forbidden_inputs(input_card: Mapping[str, Any]) -> None:
    present = sorted(k for k in FORBIDDEN_INPUTS if k in input_card and input_card[k] not in (None, False))
    if present:
        raise ForbiddenInputError(f"Forbidden OS-W target/shortcut input(s): {present}")


@dataclass(frozen=True)
class GammaZMixingInput:
    c_w: float
    s_w: float
    m_z2: float
    pi_zgamma_0: float | None = None
    re_pi_zgamma_mz2: float | None = None

    def validate_common(self) -> None:
        if self.c_w <= 0 or self.s_w <= 0:
            raise ValueError("c_w and s_w must be positive")
        if self.m_z2 <= 0:
            raise ValueError("m_z2 must be positive")


def delta_r_gamma_z(inp: GammaZMixingInput) -> float:
    """Coefficient kernel: Delta r_gammaZ = 2 (cW/sW) Pi_Zgamma(0)/mZ^2."""
    inp.validate_common()
    if inp.pi_zgamma_0 is None:
        raise ValueError("pi_zgamma_0 is required for Delta r gamma-Z kernel")
    return 2.0 * (inp.c_w / inp.s_w) * (inp.pi_zgamma_0 / inp.m_z2)


def delta_kappa_gamma_z_bridge(inp: GammaZMixingInput) -> float:
    """Bridge kernel: Delta kappa_gammaZ = - (cW/sW) Re Pi_Zgamma(mZ^2)/mZ^2."""
    inp.validate_common()
    if inp.re_pi_zgamma_mz2 is None:
        raise ValueError("re_pi_zgamma_mz2 is required for Delta kappa gamma-Z bridge")
    return -1.0 * (inp.c_w / inp.s_w) * (inp.re_pi_zgamma_mz2 / inp.m_z2)


def evaluate_gamma_z_family(input_card: Mapping[str, Any]) -> dict[str, Any]:
    """Fail-closed family evaluator.

    Returns coefficient-level outputs only. Does not export Delta r_rem or M_W.
    """
    guard_forbidden_inputs(input_card)
    inp = GammaZMixingInput(
        c_w=float(input_card["c_w"]),
        s_w=float(input_card["s_w"]),
        m_z2=float(input_card["m_z2"]),
        pi_zgamma_0=(None if input_card.get("pi_zgamma_0") is None else float(input_card.get("pi_zgamma_0"))),
        re_pi_zgamma_mz2=(None if input_card.get("re_pi_zgamma_mz2") is None else float(input_card.get("re_pi_zgamma_mz2"))),
    )
    result = {
        "family": "gamma_Z_mixing",
        "target_consumed": False,
        "value_evaluated": False,
        "exports_Delta_r_rem": False,
        "exports_M_W": False,
    }
    if inp.pi_zgamma_0 is not None:
        result["Delta_r_gammaZ_coefficient_slice"] = delta_r_gamma_z(inp)
    if inp.re_pi_zgamma_mz2 is not None:
        result["Delta_kappa_gammaZ_bridge_slice"] = delta_kappa_gamma_z_bridge(inp)
    return result
