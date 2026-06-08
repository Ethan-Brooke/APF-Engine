"""Source-transcribed W transverse self-energy coefficient kernel for OS-W Delta r.

Boundary: this module does not compute Pi_WW. It only assembles the coefficient
structure by which sourced Pi_WW(0) and Re Pi_WW(m_W^2) enter Delta r.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping, Any

FORBIDDEN_INPUT_FIELDS = {
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
class WTransverseInput:
    Pi_WW_0: float
    RePi_WW_mW2: float
    mW2: float
    sW2: float
    cW2: float
    source_certified: bool = False

@dataclass(frozen=True)
class WTransverseResult:
    family: str
    delta_r_W: float
    term_Pi_WW_0: float
    term_RePi_WW_mW2_difference: float
    term_RePi_WW_mW2_custodial: float
    source_certified: bool
    target_consumed: bool = False
    value_is_full_delta_r: bool = False

def guard_forbidden_inputs(mapping: Mapping[str, Any]) -> None:
    bad = sorted(FORBIDDEN_INPUT_FIELDS.intersection(mapping.keys()))
    if bad:
        raise ForbiddenInputError(f"Forbidden OS-W target inputs present: {bad}")

def evaluate_w_transverse_family(inp: WTransverseInput) -> WTransverseResult:
    if inp.mW2 <= 0:
        raise ValueError("mW2 must be positive")
    if inp.sW2 <= 0 or inp.cW2 <= 0:
        raise ValueError("sW2 and cW2 must be positive")
    term_difference = (inp.Pi_WW_0 - inp.RePi_WW_mW2) / inp.mW2
    term_custodial = (inp.cW2 / inp.sW2) * (inp.RePi_WW_mW2 / inp.mW2)
    term_pi0 = inp.Pi_WW_0 / inp.mW2
    delta = term_difference + term_custodial
    return WTransverseResult(
        family="W_transverse_self_energy",
        delta_r_W=delta,
        term_Pi_WW_0=term_pi0,
        term_RePi_WW_mW2_difference=term_difference,
        term_RePi_WW_mW2_custodial=term_custodial,
        source_certified=inp.source_certified,
    )
