"""Fail-closed Z-transverse self-energy coefficient kernel for OS-W Delta r.

This module does not compute Pi_ZZ. It only maps a source-certified value of
Re Pi_ZZ^{1PI}(m_Z^2) into the coefficient slots exposed by the one-loop OS
Delta r and Delta kappa formulae.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping, Any, Dict

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
    pass

@dataclass(frozen=True)
class ZTransverseInput:
    cW2: float
    sW2: float
    mZ2: float
    rePiZZ_mZ2: float
    target_consumed: bool = False


def guard_forbidden_inputs(card: Mapping[str, Any]) -> None:
    present = sorted(FORBIDDEN_INPUTS.intersection(card.keys()))
    if present:
        raise ForbiddenInputError(f"Forbidden OS-W target inputs present: {present}")
    if card.get("target_consumed", False):
        raise ForbiddenInputError("target_consumed must remain false")


def delta_r_z_transverse(inp: ZTransverseInput) -> float:
    """Z transverse contribution to one-loop OS Delta r.

    Delta r_Z = -(cW2/sW2) * RePiZZ(mZ^2) / mZ^2.
    """
    if inp.target_consumed:
        raise ForbiddenInputError("target_consumed must remain false")
    if inp.sW2 <= 0 or inp.mZ2 <= 0:
        raise ValueError("sW2 and mZ2 must be positive")
    return -(inp.cW2 / inp.sW2) * (inp.rePiZZ_mZ2 / inp.mZ2)


def delta_kappa_z_bridge(inp: ZTransverseInput) -> float:
    """Z transverse bridge contribution to Delta kappa.

    Delta kappa_Z = +(cW2/sW2) * RePiZZ(mZ^2) / mZ^2.
    """
    if inp.target_consumed:
        raise ForbiddenInputError("target_consumed must remain false")
    if inp.sW2 <= 0 or inp.mZ2 <= 0:
        raise ValueError("sW2 and mZ2 must be positive")
    return +(inp.cW2 / inp.sW2) * (inp.rePiZZ_mZ2 / inp.mZ2)


def evaluate(card: Mapping[str, Any]) -> Dict[str, Any]:
    guard_forbidden_inputs(card)
    inp = ZTransverseInput(
        cW2=float(card["cW2"]),
        sW2=float(card["sW2"]),
        mZ2=float(card["mZ2"]),
        rePiZZ_mZ2=float(card["rePiZZ_mZ2"]),
        target_consumed=bool(card.get("target_consumed", False)),
    )
    dr = delta_r_z_transverse(inp)
    dk = delta_kappa_z_bridge(inp)
    return {
        "family": "Z_transverse_self_energy",
        "Delta_r_Z": dr,
        "Delta_kappa_Z": dk,
        "anti_symmetric_check": abs(dr + dk) < 1e-15,
        "target_consumed": False,
        "value_evaluated": False,
        "note": "Coefficient slot only; Pi_ZZ was supplied as a source-certified input and is not computed here.",
    }
