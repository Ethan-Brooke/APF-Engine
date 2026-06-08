"""Fail-closed source-transcribed OS-W mass/charge/weak-angle counterterm kernels.

These kernels specify how source-certified on-shell counterterm values enter the
one-loop Delta r assembly. They do not compute self-energies or export a full value.
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
    pass

class SourceValueRequired(ValueError):
    pass


def guard_forbidden_inputs(input_card: Mapping[str, Any] | None) -> None:
    if not input_card:
        return
    present = sorted(k for k in FORBIDDEN_INPUTS if k in input_card and input_card[k] not in (None, False, 0, ""))
    if present:
        raise ForbiddenInputError("Forbidden OS-W target/shortcut input(s): " + ", ".join(present))


def delta_mW2_OS(re_pi_WW_mW2: float) -> float:
    """On-shell W mass counterterm: delta M_W^2 = Re Pi_WW(M_W^2)."""
    return float(re_pi_WW_mW2)


def delta_mZ2_OS(re_pi_ZZ_mZ2: float) -> float:
    """On-shell Z mass counterterm: delta M_Z^2 = Re Pi_ZZ(M_Z^2)."""
    return float(re_pi_ZZ_mZ2)


def delta_Ze_OS(PiAA0: float, SigmaTAZ0_over_MZ2: float, sW: float, cW: float, sign: float = 1.0) -> float:
    """On-shell charge counterterm in the source-card convention.

    The sign parameter is kept explicit because Sigma_AZ/Pi_Zgamma conventions vary
    between reviewed sources. sign=+1 reproduces the core-slice convention.
    """
    if sW <= 0 or cW <= 0:
        raise ValueError("sW and cW must be positive")
    return 0.5 * float(PiAA0) - float(sign) * (float(sW) / float(cW)) * float(SigmaTAZ0_over_MZ2)


def delta_sW_OS(cW2: float, sW: float, deltaMZ2_over_MZ2: float, deltaMW2_over_MW2: float) -> float:
    """On-shell weak-angle counterterm delta s_W."""
    if cW2 <= 0 or sW <= 0:
        raise ValueError("cW2 and sW must be positive")
    return (float(cW2) / (2.0 * float(sW))) * (float(deltaMZ2_over_MZ2) - float(deltaMW2_over_MW2))


def delta_sW_over_sW_OS(cW2: float, sW2: float, deltaMZ2_over_MZ2: float, deltaMW2_over_MW2: float) -> float:
    """On-shell weak-angle counterterm ratio delta s_W / s_W."""
    if cW2 <= 0 or sW2 <= 0:
        raise ValueError("cW2 and sW2 must be positive")
    return (float(cW2) / (2.0 * float(sW2))) * (float(deltaMZ2_over_MZ2) - float(deltaMW2_over_MW2))


def delta_r_counterterm_bridge(delta_Ze: float, delta_sW_over_sW: float) -> float:
    """Tree-coupling counterterm bridge: 2 delta_Ze - 2 delta s_W/s_W."""
    return 2.0 * float(delta_Ze) - 2.0 * float(delta_sW_over_sW)


def delta_r_counterterm_assembly_slice(pi_WW_0: float, delta_mW2: float, mW2: float,
                                       delta_Ze: float, delta_sW_over_sW: float,
                                       lepton_WF_half_sum: float = 0.0,
                                       vertex_box: float = 0.0) -> float:
    """Source-card one-loop Delta r assembly slice, with source-supplied pieces."""
    if mW2 <= 0:
        raise ValueError("mW2 must be positive")
    return ((float(pi_WW_0) - float(delta_mW2)) / float(mW2)
            + delta_r_counterterm_bridge(delta_Ze, delta_sW_over_sW)
            + float(lepton_WF_half_sum) + float(vertex_box))

@dataclass(frozen=True)
class CountertermInput:
    mW2: float
    mZ2: float
    sW: float
    cW: float
    pi_WW_0: float | None = None
    re_pi_WW_mW2: float | None = None
    re_pi_ZZ_mZ2: float | None = None
    PiAA0: float | None = None
    SigmaTAZ0_over_MZ2: float | None = None
    lepton_WF_half_sum: float = 0.0
    vertex_box: float = 0.0
    metadata: Mapping[str, Any] | None = None

    def validate_common(self) -> None:
        if self.mW2 <= 0 or self.mZ2 <= 0:
            raise ValueError("mW2 and mZ2 must be positive")
        if self.sW <= 0 or self.cW <= 0:
            raise ValueError("sW and cW must be positive")


def evaluate_counterterm_slice(inp: CountertermInput) -> dict[str, Any]:
    guard_forbidden_inputs(inp.metadata)
    inp.validate_common()
    if inp.re_pi_WW_mW2 is None:
        raise SourceValueRequired("re_pi_WW_mW2 required")
    if inp.re_pi_ZZ_mZ2 is None:
        raise SourceValueRequired("re_pi_ZZ_mZ2 required")
    if inp.PiAA0 is None or inp.SigmaTAZ0_over_MZ2 is None:
        raise SourceValueRequired("PiAA0 and SigmaTAZ0_over_MZ2 required")
    dmw = delta_mW2_OS(inp.re_pi_WW_mW2)
    dmz = delta_mZ2_OS(inp.re_pi_ZZ_mZ2)
    sW2 = inp.sW * inp.sW
    cW2 = inp.cW * inp.cW
    ds_over_s = delta_sW_over_sW_OS(cW2, sW2, dmz/inp.mZ2, dmw/inp.mW2)
    dZe = delta_Ze_OS(inp.PiAA0, inp.SigmaTAZ0_over_MZ2, inp.sW, inp.cW)
    out = {
        "family": "mass_charge_weak_angle_counterterms",
        "delta_mW2": dmw,
        "delta_mZ2": dmz,
        "delta_sW_over_sW": ds_over_s,
        "delta_Ze": dZe,
        "delta_r_counterterm_bridge": delta_r_counterterm_bridge(dZe, ds_over_s),
        "value_evaluated": False,
        "target_consumed": False,
    }
    if inp.pi_WW_0 is not None:
        out["delta_r_counterterm_assembly_slice"] = delta_r_counterterm_assembly_slice(
            inp.pi_WW_0, dmw, inp.mW2, dZe, ds_over_s, inp.lepton_WF_half_sum, inp.vertex_box
        )
    return out
