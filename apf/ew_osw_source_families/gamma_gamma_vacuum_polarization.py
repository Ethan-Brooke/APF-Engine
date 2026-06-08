"""
Fail-closed source-transcribed coefficient-slot kernels for the OS-W gamma-gamma
vacuum-polarization family.

This module does not compute the photon self-energy. It only maps a source-certified
PiPrime_gamma_gamma_0 value into the Delta r coefficient slot.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Any, Iterable

FORBIDDEN_INPUTS = {
    'measured_M_W_value',
    'DIZET_ZFITTER_aggregate_output',
    'published_total_SM_M_W_as_component_value',
    'fitted_counterterm',
    'post_hoc_tolerance',
    'four_over_5063_weak_angle_shortcut',
    'measured_sin2theta_eff',
}

@dataclass(frozen=True)
class GammaGammaInput:
    PiPrime_gamma_gamma_0: float | None = None
    source_certified: bool = False
    target_consumed: bool = False
    metadata: Dict[str, Any] | None = None

@dataclass(frozen=True)
class KernelResult:
    family: str
    component: str
    value: float | None
    value_evaluated: bool
    target_consumed: bool
    source_certified: bool
    status: str

class ForbiddenInputError(ValueError):
    pass

class SourceCertificationRequired(ValueError):
    pass

def guard_forbidden_inputs(card: Dict[str, Any]) -> None:
    seen = FORBIDDEN_INPUTS.intersection(card.keys())
    if seen:
        raise ForbiddenInputError(f'Forbidden target-consuming inputs present: {sorted(seen)}')


def delta_r_gamma_gamma_slot(inp: GammaGammaInput) -> KernelResult:
    """Return Delta r_gamma_gamma = Pi'_gamma_gamma(0) for source-certified inputs.

    Fails closed when no source-certified self-energy derivative is supplied.
    """
    if inp.metadata:
        guard_forbidden_inputs(inp.metadata)
    if inp.target_consumed:
        raise ForbiddenInputError('target_consumed must be False')
    if inp.PiPrime_gamma_gamma_0 is None or not inp.source_certified:
        raise SourceCertificationRequired('PiPrime_gamma_gamma_0 must be source-certified before evaluation')
    return KernelResult(
        family='gamma_gamma_vacuum_polarization',
        component='Delta_r_gamma_gamma',
        value=float(inp.PiPrime_gamma_gamma_0),
        value_evaluated=True,
        target_consumed=False,
        source_certified=True,
        status='component_slot_evaluated_from_source_certified_input_only',
    )


def declare_running_alpha_split() -> Dict[str, Any]:
    """Return a ledger declaration, not a numerical evaluation."""
    return {
        'family': 'gamma_gamma_vacuum_polarization',
        'component': 'Delta_alpha_split',
        'slots': ['Delta_alpha_lept', 'Delta_alpha_had5', 'Delta_alpha_top_optional'],
        'value_evaluated': False,
        'target_consumed': False,
        'status': 'external_ledger_split_declared_no_value_evaluated',
    }
