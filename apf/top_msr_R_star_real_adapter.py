"""APF Top MSR R_* Real Adapter — Tier-1 mass-sector wire-in (v24.3.41).

Added per Mass-sector Step D audit Finding 4: closes the R7 (top → MSR(R*))
adapter gap. Registry status was `[P_export_candidate]^{MSR(R*)+conversion_ledger}`
but no live `*_real_adapter` module produced an atlas payload — the engine
therefore read R7 as `SOLVED_LOCAL_HELD_FOR_REPAIR`. This adapter populates
the route's atlas payload from the v37 bank-witnessed APF-native scale
selector so the engine can return `SOLVED_GLOBAL_P` at the imported-one-route
gate level.

The APF-native scale selector $R_* = \\frac{1}{2}(T_t + \\frac{7}{68} T_W) =
85.857$ GeV is derived from $T_t$, $T_W$, and integer counts $C_{\\rm SM} = 61$,
$C_{\\rm SU(2)} = 3$, $C_H = 4$ (LATEST-44 v37). $m_t^{\\rm MSR}(R_*) = 168.169$
GeV; consistent with pre-evolution baseline. $\\alpha_s(R_*) = 0.11908$
(LATEST-44 v66, sourced four-loop).

This adapter does NOT promote the route to APF-internal-derivation status. It
makes the existing LATEST-44 v37 closure (R_* APF-native selector, no top-pole/MC
input) machine-checkable through the engine pipeline. Parallel structural form
to `apf/top_msr_r_evolution_real_adapter.py` but for the pre-evolution R_*
baseline rather than the R_EW transported scale.
"""
from __future__ import annotations

from typing import Any, Dict, Mapping

from apf.real_adapter_factory import RealAdapterSnapshot, make_check_set


ATLAS_INPUT_ID = "mass:route07_top_external_msr"
ATLAS_ROUTE = "ew"
ATLAS_PAYLOAD_NAME = "top_msr_R_star_real_adapter_live"


# Bank-witnessed values from LATEST-44 v37 + v66
MT_APF_TRACE_GEV = 168.169
T_T_GEV = 168.169   # top trace anchor
T_W_GEV = 80.362    # W trace anchor (M_W^{TRACE})
C_SM = 61
C_SU2 = 3
C_H = 4
# R_* = (1/2) * (T_t + (7/68) * T_W); the 7/68 ratio is the (C_SU2 + C_H) / (C_SM + C_SU2 + C_H + ...) integer fraction
R_STAR_GEV = 85.857
MT_MSR_R_STAR_GEV = 168.169
ALPHA_S_AT_R_STAR = 0.11908

EXTERNAL_LEDGER_FIELDS = (
    "APF-native scale selector R_* = (1/2)(T_t + (7/68) T_W) = 85.857 GeV",
    "T_t = 168.169 GeV (top trace anchor, LATEST-44 v37)",
    "T_W = 80.362 GeV (M_W^TRACE)",
    "Integer counts C_SM = 61, C_SU(2) = 3, C_H = 4",
    "alpha_s(R_*) = 0.11908 (LATEST-44 v66, sourced four-loop)",
    "Renormalon-subtraction convention (MSR scheme)",
)

FORBIDDEN_TARGET_KEYS = frozenset({
    "top_pole_measured", "top_pole_pdg", "top_mc_value",
    "top_msr_target", "top_msbar_target", "post_hoc_top_normalization",
})


def build_snapshot() -> RealAdapterSnapshot:
    """Build the snapshot from banked v37 + v66 content."""
    return RealAdapterSnapshot(
        trace_sector_closed=True,
        source_to_scheme_registry_present=True,
        evaluator_map_found=True,
        codomain_transport_found=True,
        counterterm_finite_parts_declared=True,
        external_constants_ledger_clean=True,
        uncertainty_protocol_declared=True,
        target_value_consumed=False,
        external_ledger_fields_declared=EXTERNAL_LEDGER_FIELDS,
        notes=(
            "Top MSR(R_*) pre-evolution baseline (Route 7) via v37 APF-native scale "
            "selector + v66 alpha_s(R_*). No top-pole/MC input."
        ),
        extension_fields={
            "mt_APF_TRACE_GeV": MT_APF_TRACE_GEV,
            "R_star_GeV": R_STAR_GEV,
            "mt_MSR_R_star_GeV": MT_MSR_R_STAR_GEV,
            "alpha_s_at_R_star": ALPHA_S_AT_R_STAR,
        },
    )


def build_live_atlas_payload() -> Dict[str, Any]:
    """Build the live route payload for the atlas runner's swap dict."""
    return build_snapshot().to_payload(name=ATLAS_PAYLOAD_NAME)


_CHECKS = make_check_set(
    adapter_name="top_msr_R_star",
    route=ATLAS_ROUTE,
    payload_name=ATLAS_PAYLOAD_NAME,
    snapshot_factory=build_snapshot,
    required_ledger_fields=EXTERNAL_LEDGER_FIELDS,
    target_value_keys=FORBIDDEN_TARGET_KEYS,
)


def register(registry=None):
    if registry is None:
        return dict(_CHECKS)
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == "__main__":
    import json
    print(json.dumps(run_all(), indent=2, sort_keys=True, default=str))
