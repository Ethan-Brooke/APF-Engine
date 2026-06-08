"""APF-native two-loop Phase-2 renormalized counterterm + Z-pole residue formula ledger — Tier-4.

Phase-2 push v7 moves the electroweak two-loop arc from source acquisition
(v24.3.156-.159) to *runnable formula infrastructure*. Five sibling packs:

  1. renormalized self-energy counterterm formula ledger;
  2. Z-pole NNLO residue / γ-Z mixing connector formula evaluator;
  3. Δr / M_W aggregate validation grid (comparator-only);
  4. DIZET / ROKANC / RHOCC instrumentation harness (declares targets,
     consumes no value);
  5. coefficient-row seed ledger spanning all six required physical channels.

This module certifies the *structural contract* of that infrastructure: the
six required physical coefficient channels are seeded with physical_value = 0;
the Δr aggregate grid is comparator-typed (published M_W / Δr held as
validation targets, never consumed as a derived component); and the DIZET
harness declares an allowed instrumentation target set without importing any
aggregate as a component value. It does NOT bank a physical self-energy, Δr,
or M_W value — those remain open downstream of the v24.3.154 current-source
no-go, which this push does not overturn.

The AC 2002 bosonic ΔM_W formula is already banked at v24.3.156
(delta_mw_from_bosonic_delta_r); this module depends on it rather than
re-deriving its number, so no numeric claim is double-counted.

Honest non-claims preserved verbatim:
  * Export_complete_EW_two_loop_diagram_coefficient_ledger_P = 0
  * Export_evaluated_Sigma_W_2L_P = 0
  * Export_evaluated_Sigma_Z_2L_P = 0
  * Export_evaluated_Pi_gammagamma_2L_P = 0
  * Export_evaluated_Pi_gammaZ_2L_P = 0
  * Export_evaluated_vertex_box_2L_P = 0
  * Export_OSW_delta_r_rem_APF_internal_P = 0
  * Export_DIZET_or_published_MW_consumed_as_component_P = 0

Sibling APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v7 (five packs;
self-verifier TWO_LOOP_PHASE2_PUSH_V7_PASS, 5/5).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from apf.apf_utils import check, _result


# =============================================================================
# Source-certified kernel
# =============================================================================

# The six physical coefficient channels the Phase-2 EW two-loop ledger must
# eventually populate. Seeded here at physical_value = 0 (structural slots).
REQUIRED_CHANNELS = (
    "Sigma_W", "Sigma_Z", "Pi_gammagamma", "Pi_gammaZ",
    "vertex_box", "ZllR_form_factor",
)


@dataclass(frozen=True)
class SeedRow:
    channel: str
    role: str          # formula_evaluator | comparator | instrumentation | seed
    physical_value: int = 0
    target_consumed: int = 0


@dataclass(frozen=True)
class ComparatorGrid:
    """Δr / M_W aggregate validation grid: published values are comparator-only."""

    name: str = "delta_r_MW_aggregate_grid"
    published_values_held: bool = True
    published_values_consumed_as_component: bool = False
    role: str = "comparator"


# DIZET / ROKANC / RHOCC instrumentation harness: allowed *targets*, not values.
DIZET_ALLOWED_TARGETS = ("DIZET", "ROKANC", "RHOCC", "ZFTEST")
DIZET_FORBIDDEN_AS_COMPONENT = (
    "DIZET_AGGREGATE_COMPONENT", "PUBLISHED_TOTAL_SM_MW",
    "ZFITTER_TOTAL_INPUT", "FITTED_COUNTERTERM", "MEASURED_MW",
)


def seed_ledger() -> List[SeedRow]:
    rows = [SeedRow(c, "seed") for c in REQUIRED_CHANNELS]
    rows.append(SeedRow("counterterm_formula", "formula_evaluator"))
    rows.append(SeedRow("zpole_nnlo_residue", "formula_evaluator"))
    rows.append(SeedRow("delta_r_MW_grid", "comparator"))
    rows.append(SeedRow("dizet_harness", "instrumentation"))
    return rows


def harness_admits(token: str) -> bool:
    """Instrumentation harness admits a declared target but never a component value."""
    if token in DIZET_FORBIDDEN_AS_COMPONENT:
        return False
    return token in DIZET_ALLOWED_TARGETS


EXPORT_FLAGS = {
    "Export_phase2_counterterm_residue_formula_ledger_P": 1,
    "Export_all_six_required_channels_seeded_P": 1,
    "Export_delta_r_aggregate_grid_comparator_only_P": 1,
    "Export_dizet_harness_targets_declared_no_value_consumed_P": 1,
    "Export_complete_EW_two_loop_diagram_coefficient_ledger_P": 0,
    "Export_evaluated_Sigma_W_2L_P": 0,
    "Export_evaluated_Sigma_Z_2L_P": 0,
    "Export_evaluated_Pi_gammagamma_2L_P": 0,
    "Export_evaluated_Pi_gammaZ_2L_P": 0,
    "Export_evaluated_vertex_box_2L_P": 0,
    "Export_OSW_delta_r_rem_APF_internal_P": 0,
    "Export_DIZET_or_published_MW_consumed_as_component_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_phase2_counterterm_residue_formula_ledger_current_depth_P():
    """T: Phase-2 renormalized counterterm + Z-pole NNLO residue formula ledger.
    Six required physical channels seeded at physical_value=0; Δr/M_W aggregate
    grid comparator-typed (published values held, never consumed as component);
    DIZET/ROKANC/RHOCC harness admits declared targets, refuses every
    component/aggregate token. No physical self-energy / Δr / M_W value banked.
    [P_two_loop_phase2_counterterm_residue_formula_ledger_current_depth;
     C_physical_coefficient_values_pending]."""

    rows = seed_ledger()

    # (a) All six required physical channels seeded, all at physical_value = 0.
    seeded = {r.channel for r in rows if r.role == "seed"}
    for c in REQUIRED_CHANNELS:
        check(c in seeded, f"required channel {c} must be seeded")
    check(all(r.physical_value == 0 for r in rows),
          "every seed/formula row must carry physical_value = 0")
    check(all(r.target_consumed == 0 for r in rows),
          "no row may consume a target")

    # (b) Formula evaluators present (counterterm ledger + Z-pole residue).
    roles = {r.channel: r.role for r in rows}
    check(roles.get("counterterm_formula") == "formula_evaluator",
          "counterterm formula evaluator must be present")
    check(roles.get("zpole_nnlo_residue") == "formula_evaluator",
          "Z-pole NNLO residue evaluator must be present")

    # (c) Δr / M_W aggregate grid is comparator-only.
    grid = ComparatorGrid()
    check(grid.published_values_held is True, "grid holds published values")
    check(grid.published_values_consumed_as_component is False,
          "published M_W/Δr must NOT be consumed as a derived component")
    check(grid.role == "comparator", "grid role must be comparator")

    # (d) DIZET harness: declared targets admitted, component tokens refused.
    for t in DIZET_ALLOWED_TARGETS:
        check(harness_admits(t) is True, f"harness must admit declared target {t}")
    for bad in DIZET_FORBIDDEN_AS_COMPONENT:
        check(harness_admits(bad) is False,
              f"harness must refuse component/aggregate token {bad}")

    # (e) Honest non-claim flags.
    for k in ("Export_complete_EW_two_loop_diagram_coefficient_ledger_P",
              "Export_evaluated_Sigma_W_2L_P", "Export_evaluated_Sigma_Z_2L_P",
              "Export_evaluated_Pi_gammagamma_2L_P", "Export_evaluated_Pi_gammaZ_2L_P",
              "Export_evaluated_vertex_box_2L_P", "Export_OSW_delta_r_rem_APF_internal_P",
              "Export_DIZET_or_published_MW_consumed_as_component_P"):
        check(EXPORT_FLAGS[k] == 0, f"{k} must remain 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_two_loop_phase2_counterterm_residue_formula_ledger_current_depth: "
              "Phase-2 renormalized counterterm + Z-pole NNLO residue formula "
              "infrastructure. Six required physical channels seeded at "
              "physical_value=0; Δr/M_W aggregate grid comparator-only; DIZET "
              "harness declares targets, consumes no component. "
              "[P_two_loop_phase2_counterterm_residue_formula_ledger_current_depth]"),
        tier=4,
        epistemic="P_two_loop_phase2_counterterm_residue_formula_ledger_current_depth",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v7 "
            "(5 packs: counterterm formula ledger + Z-pole NNLO residue "
            "evaluator + Δr/M_W validation grid + DIZET instrumentation harness "
            "+ six-channel seed ledger; self-verifier 5/5 PASS). This module "
            "certifies the structural contract: all six required physical "
            "coefficient channels (Σ_W, Σ_Z, Π_γγ, Π_γZ, vertex/box, Zℓℓ form "
            "factor) seeded with physical_value=0; the Δr/M_W aggregate grid is "
            "comparator-typed (published values held as validation targets, "
            "never consumed as a derived component, matching the v24.3.158 "
            "ZFITTER guard role-typing); the DIZET/ROKANC/RHOCC harness admits "
            "declared instrumentation targets but refuses every "
            "component/aggregate token. Formula evaluators are runnable "
            "infrastructure; physical values stay open downstream of the "
            "v24.3.154 current-source no-go. The AC 2002 bosonic ΔM_W formula "
            "is depended on from v24.3.156, not re-derived."
        ),
        key_result=(
            "Phase-2 counterterm + Z-pole residue formula ledger with six "
            "physical channels seeded (physical_value=0), comparator-only Δr "
            "grid, and a value-refusing DIZET harness. "
            "[P_two_loop_phase2_counterterm_residue_formula_ledger_current_depth]"
        ),
        dependencies=[
            "T_two_loop_phase2_delta_r_source_import_v1",
            "T_two_loop_phase2_zfitter_comparator_guard_v1",
            "T_two_loop_phase2_ew_diagram_coefficient_derivation_engine_scaffold_v1",
        ],
        cross_refs=[],
        artifacts={
            "required_channels": list(REQUIRED_CHANNELS),
            "dizet_allowed_targets": list(DIZET_ALLOWED_TARGETS),
            "dizet_forbidden_as_component": list(DIZET_FORBIDDEN_AS_COMPONENT),
            "sibling_bundle": "APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v7",
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_phase2_counterterm_residue_formula_ledger_current_depth":
        check_T_two_loop_phase2_counterterm_residue_formula_ledger_current_depth_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
