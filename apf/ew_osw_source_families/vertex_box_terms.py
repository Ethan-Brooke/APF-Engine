
"""Fail-closed vertex/box coefficient slot for OS-W Delta r assembly.

This module does not compute delta_VB^SM. It only accepts a source-certified
value and returns the additive contribution to Delta r.
"""

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

class SourceCertificationRequired(ValueError):
    pass


def guard_forbidden_inputs(card: dict) -> None:
    keys = set(card.keys())
    bad = sorted(keys & FORBIDDEN_INPUTS)
    if bad:
        raise ForbiddenInputError(f"Forbidden target-consuming inputs present: {bad}")


def delta_r_vertex_box(delta_vb_sm: float, *, source_certified: bool, target_consumed: bool=False) -> float:
    """Return the additive vertex/box contribution Delta r_VB.

    Parameters
    ----------
    delta_vb_sm:
        Source-certified finite vertex+box correction. The function does not
        derive this value.
    source_certified:
        Must be true; otherwise the evaluator fails closed.
    target_consumed:
        Must be false; this value cannot be fitted from M_W, DIZET/ZFITTER, or
        published total SM M_W.
    """
    if target_consumed:
        raise ForbiddenInputError("target_consumed must be false")
    if not source_certified:
        raise SourceCertificationRequired("delta_VB^SM requires source certification before use")
    return float(delta_vb_sm)


def assemble_vertex_box_from_card(card: dict) -> dict:
    """Validate and return the additive vertex/box contribution."""
    guard_forbidden_inputs(card)
    value = delta_r_vertex_box(
        card.get('delta_vb_sm'),
        source_certified=bool(card.get('source_certified', False)),
        target_consumed=bool(card.get('target_consumed', False)),
    )
    return {
        'family': 'vertex_box_terms',
        'delta_r_vertex_box': value,
        'target_consumed': False,
        'computed_delta_vb': False,
        'status': 'coefficient_slot_applied_from_source_certified_value',
    }
