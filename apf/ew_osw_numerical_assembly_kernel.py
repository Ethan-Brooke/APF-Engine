"""Fail-closed OS-W numerical assembly harness.

This module assembles source-certified component values into the one-loop on-shell Delta r slot algebra.
It does not compute physical electroweak self-energies.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, Mapping

FORBIDDEN_INPUTS = {
    "measured_M_W_value",
    "DIZET_ZFITTER_aggregate_output",
    "published_total_SM_M_W_as_component_value",
    "fitted_counterterm",
    "post_hoc_tolerance",
    "four_over_5063_weak_angle_shortcut",
    "measured_sin2theta_eff",
    "target_DeltaRhobarW_interval",
    "target_delta_r_rem_interval",
}

REQUIRED_DELTA_R_SLOTS = (
    "mw2",
    "mz2",
    "pi_aa_prime_0",
    "pi_ww_0",
    "re_pi_ww_mw2",
    "re_pi_zz_mz2",
    "pi_zgamma_0",
    "delta_vb_sm",
)

class ForbiddenInputError(ValueError):
    pass

class SourceCertificationRequired(ValueError):
    pass

class InvalidAssemblyInput(ValueError):
    pass


def _walk_keys(obj: Any):
    if isinstance(obj, Mapping):
        for k, v in obj.items():
            yield str(k)
            yield from _walk_keys(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from _walk_keys(item)


def guard_forbidden_inputs(input_card: Mapping[str, Any]) -> None:
    present = sorted(FORBIDDEN_INPUTS.intersection(set(_walk_keys(input_card))))
    if present:
        raise ForbiddenInputError(f"Forbidden target-side inputs present: {present}")


def _component_value(card: Mapping[str, Any], key: str, require_source_certification: bool) -> float:
    if key not in card:
        raise InvalidAssemblyInput(f"Missing required component slot: {key}")
    entry = card[key]
    if not isinstance(entry, Mapping) or "value" not in entry:
        raise InvalidAssemblyInput(f"Component slot {key} must be an object with a value")
    if require_source_certification and not bool(entry.get("source_certified", False)):
        raise SourceCertificationRequired(f"Component slot {key} is not source-certified")
    try:
        return float(entry["value"])
    except Exception as exc:
        raise InvalidAssemblyInput(f"Component slot {key} has non-numeric value") from exc


def assemble_delta_r_one_loop(
    component_values: Mapping[str, Any],
    *,
    require_source_certification: bool = True,
) -> Dict[str, Any]:
    """Assemble one-loop OS Delta r from already-evaluated component values.

    Required slots are declared in REQUIRED_DELTA_R_SLOTS. This function does not compute any self-energy;
    it only assembles numeric values supplied by a source-certified evaluator.
    """
    guard_forbidden_inputs(component_values)
    vals = {k: _component_value(component_values, k, require_source_certification) for k in REQUIRED_DELTA_R_SLOTS}
    mw2 = vals["mw2"]
    mz2 = vals["mz2"]
    if mw2 <= 0 or mz2 <= 0 or mw2 >= mz2:
        raise InvalidAssemblyInput("Require 0 < MW^2 < MZ^2 for physical branch assembly")
    cw2 = mw2 / mz2
    sw2 = 1.0 - cw2
    if sw2 <= 0:
        raise InvalidAssemblyInput("Invalid weak-angle relation: sW^2 <= 0")
    cw = math.sqrt(cw2)
    sw = math.sqrt(sw2)
    term_gamma_gamma = vals["pi_aa_prime_0"]
    term_w = vals["pi_ww_0"] / mw2 + (cw2 / sw2 - 1.0) * vals["re_pi_ww_mw2"] / mw2
    term_z = -(cw2 / sw2) * vals["re_pi_zz_mz2"] / mz2
    term_gamma_z = 2.0 * cw / sw * vals["pi_zgamma_0"] / mz2
    term_vb = vals["delta_vb_sm"]
    delta_r_os = term_gamma_gamma + term_w + term_z + term_gamma_z + term_vb
    return {
        "delta_r_os": delta_r_os,
        "terms": {
            "gamma_gamma": term_gamma_gamma,
            "W_transverse": term_w,
            "Z_transverse": term_z,
            "gamma_Z": term_gamma_z,
            "vertex_box": term_vb,
        },
        "weak_angle": {"sw2": sw2, "cw2": cw2, "sw": sw, "cw": cw},
        "target_consumed": False,
        "physical_export": False,
        "status": "assembly_only_not_physical_export",
    }


def compute_delta_r_rem(delta_r_os: float, delta_alpha: float, delta_rho: float, mw2: float, mz2: float) -> float:
    if mw2 <= 0 or mz2 <= 0 or mw2 >= mz2:
        raise InvalidAssemblyInput("Require 0 < MW^2 < MZ^2")
    cw2 = mw2 / mz2
    sw2 = 1.0 - cw2
    return float(delta_r_os) - float(delta_alpha) + (cw2 / sw2) * float(delta_rho)


def solve_mw_from_delta_r(delta_r_os: float, alpha0: float, G_F: float, M_Z: float) -> Dict[str, float]:
    """Solve the on-shell relation for MW given Delta r.

    This helper is for certified Delta-r inputs only. It is not a prediction in this pack.
    """
    if alpha0 <= 0 or G_F <= 0 or M_Z <= 0:
        raise InvalidAssemblyInput("alpha0, G_F, and M_Z must be positive")
    mz2 = M_Z * M_Z
    A = math.pi * alpha0 / (math.sqrt(2.0) * G_F) * (1.0 + delta_r_os)
    disc = 1.0 - 4.0 * A / mz2
    if disc < 0:
        raise InvalidAssemblyInput("No real MW solution for supplied Delta r")
    sqrt_disc = math.sqrt(disc)
    high = 0.5 * mz2 * (1.0 + sqrt_disc)
    low = 0.5 * mz2 * (1.0 - sqrt_disc)
    return {"MW2_high_branch": high, "MW_high_branch": math.sqrt(high), "MW2_low_branch": low, "MW_low_branch": math.sqrt(low), "target_consumed": False}
