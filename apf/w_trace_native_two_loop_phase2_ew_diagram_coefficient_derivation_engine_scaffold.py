"""APF-native two-loop Phase-2 EW diagram-coefficient derivation engine scaffold — Tier-4.

Direct execution of v24.3.155 derivation plan Stages C-G: typed contract +
7-stage derivation matrix + per-row validator that refuses uncertified /
target-consuming / fitted rows. No physical rows are populated; the scaffold
exposes the structural gate that closes the EW 2L coefficient ledger.

Required diagram families (8 total):
  * Σ_W_2L, Σ_Z_2L, Π_γγ_2L, Π_γZ_2L — the 4 EW self-energy channels.
  * muon_decay_vertex_box_2L, Zll_vertex_2L — 2 vertex/box families.
  * counterterm_products, tadpole_convention — 2 scheme families.

Of these, 6 are OPEN_PHYSICAL_FAMILIES (the 4 self-energies + 2 vertex/box).
The 2 scheme families are PARTIAL_SOURCE_IMPORTED / SOURCE_IMPORTED.

Forbidden inputs (6):
  * measured_MW
  * published_total_SM_MW
  * DIZET_aggregate_component
  * ZFITTER_total_input
  * target_interval
  * fitted_counterterm

7-stage derivation matrix (input → output → promotion_gate):
  1. diagram_inventory: FeynArts/QGRAF → diagram_class_ledger
  2. projectors: Denner/ACF/FHW conventions → projector definitions
  3. algebra_generation: amplitudes → pre-IBP scalar-integral coefficient rows
  4. IBP_reduction: scalar integrals → master-basis coefficient rows
  5. master_evaluation: masters → ε-pole + finite row values
  6. assembly: row ledger → Δr / Δκ aggregates
  7. same_input_comparator: optional ZFITTER/DIZET comparator (residuals only)

`validate_row(row)` enforces: family ∈ REQUIRED_FAMILIES, non-empty
source_key/expression/master_basis, target_consumed=False, fitted=False,
source_certified=True. `complete_physical_ledger(rows)` returns True only when
every OPEN_PHYSICAL_FAMILY is covered by at least one valid row — currently
False (no rows supplied).

Honest non-claims preserved:
  * Export_complete_physical_coefficient_ledger = 0
  * Export_evaluated_Sigma_{W,Z}_2L = Export_evaluated_Pi_{γγ,γZ}_2L = 0
  * Export_evaluated_vertex_box_2L = 0
  * Export_OSW_delta_r_rem_APF_internal = 0

Sibling APF_TWO_LOOP_PHASE2_EW_DIAGRAM_COEFFICIENT_DERIVATION_ENGINE_SCAFFOLD_v1
via APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v6.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Set, Tuple

from apf.apf_utils import check, _result


REQUIRED_FAMILIES: Set[str] = {
    "Sigma_W_2L", "Sigma_Z_2L", "Pi_gammagamma_2L", "Pi_gammaZ_2L",
    "muon_decay_vertex_box_2L", "Zll_vertex_2L",
    "counterterm_products", "tadpole_convention",
}

OPEN_PHYSICAL_FAMILIES: Set[str] = {
    "Sigma_W_2L", "Sigma_Z_2L", "Pi_gammagamma_2L", "Pi_gammaZ_2L",
    "muon_decay_vertex_box_2L", "Zll_vertex_2L",
}

FORBIDDEN_INPUTS: Set[str] = {
    "measured_MW", "published_total_SM_MW",
    "DIZET_aggregate_component", "ZFITTER_total_input",
    "target_interval", "fitted_counterterm",
}


@dataclass(frozen=True)
class CoefficientRow:
    family: str
    source_key: str
    expression: str
    master_basis: str
    source_certified: bool
    target_consumed: bool = False
    fitted: bool = False


def validate_row(row: CoefficientRow) -> bool:
    if row.family not in REQUIRED_FAMILIES:
        return False
    if not row.source_key or not row.expression or not row.master_basis:
        return False
    if row.target_consumed or row.fitted:
        return False
    if not row.source_certified:
        return False
    return True


def complete_physical_ledger(rows: List[CoefficientRow]) -> bool:
    fams = {r.family for r in rows if validate_row(r)}
    return OPEN_PHYSICAL_FAMILIES <= fams


def current_v6_promotes_complete_ledger() -> bool:
    return False


DERIVATION_STAGES: Tuple[Tuple[int, str, str, str, str], ...] = (
    (1, "diagram_inventory",
     "FeynArts/QGRAF Standard Model diagrams",
     "diagram_class_ledger.csv",
     "complete class coverage incl ghosts/Goldstones/tadpoles"),
    (2, "projectors",
     "Denner/ACF/FHW convention keys",
     "projector definitions for WW/ZZ/AA/AZ and Zll vector/axial",
     "Ward and pole-scheme consistency"),
    (3, "algebra_generation",
     "diagram amplitudes",
     "scalar-integral coefficient rows before IBP",
     "no target observable input"),
    (4, "IBP_reduction",
     "scalar integrals",
     "master-basis coefficient rows",
     "topology mapped to Phase-1 master substrate"),
    (5, "master_evaluation",
     "tadpole/sunset/two-point/vertex masters",
     "epsilon pole + finite row values",
     "UV/IR pole cancellation"),
    (6, "assembly",
     "row ledger",
     "Delta-r and Delta-kappa aggregates",
     "reproduce ACFW/ACF tables as regression only"),
    (7, "same_input_comparator",
     "ZFITTER/DIZET optional",
     "comparator residuals",
     "comparator not consumed as component"),
)


EXPORT_FLAGS = {
    "Export_EW_coefficient_derivation_engine_contract_P": 1,
    "Export_EW_required_coefficient_family_matrix_P": 1,
    "Export_EW_no_smuggling_row_validation_P": 1,
    "Export_EW_derivation_plan_P": 1,
    "Export_complete_physical_coefficient_ledger_P": 0,
    "Export_evaluated_Sigma_W_2L_P": 0,
    "Export_evaluated_Sigma_Z_2L_P": 0,
    "Export_evaluated_Pi_gammagamma_2L_P": 0,
    "Export_evaluated_Pi_gammaZ_2L_P": 0,
    "Export_evaluated_vertex_box_2L_P": 0,
    "Export_OSW_delta_r_rem_APF_internal_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_phase2_ew_diagram_coefficient_derivation_engine_scaffold_v1_P():
    """T: Derivation engine scaffold — 8 required families (6 OPEN_PHYSICAL),
    6 forbidden inputs, 7-stage derivation matrix, CoefficientRow validator.
    Toy row passes; uncertified/target-consuming/fitted rows refused.
    complete_physical_ledger([]) == False. NO physical rows populated.
    [P_two_loop_phase2_ew_diagram_coefficient_derivation_engine_scaffold_v1;
     C_physical_coefficient_rows_pending]."""

    # (a) Family-set integrity.
    check(len(REQUIRED_FAMILIES) == 8,
          f"required-family count: {len(REQUIRED_FAMILIES)}")
    check(len(OPEN_PHYSICAL_FAMILIES) == 6,
          f"open-physical-family count: {len(OPEN_PHYSICAL_FAMILIES)}")
    check(OPEN_PHYSICAL_FAMILIES <= REQUIRED_FAMILIES,
          "open physical must be subset of required")
    for fam in ["Sigma_W_2L", "Sigma_Z_2L", "Pi_gammagamma_2L", "Pi_gammaZ_2L",
                "muon_decay_vertex_box_2L", "Zll_vertex_2L"]:
        check(fam in OPEN_PHYSICAL_FAMILIES, f"open physical missing {fam}")
    for fam in ["counterterm_products", "tadpole_convention"]:
        check(fam in REQUIRED_FAMILIES and fam not in OPEN_PHYSICAL_FAMILIES,
              f"scheme family {fam} should be required but not OPEN_PHYSICAL")

    # (b) Forbidden-input set.
    check(len(FORBIDDEN_INPUTS) == 6,
          f"forbidden-input count: {len(FORBIDDEN_INPUTS)}")

    # (c) 7 derivation stages, ordered 1..7.
    check(len(DERIVATION_STAGES) == 7,
          f"derivation-stage count: {len(DERIVATION_STAGES)}")
    for i, stage in enumerate(DERIVATION_STAGES, start=1):
        check(stage[0] == i, f"stage {i} out of order: {stage}")

    # (d) Toy valid row passes.
    good = CoefficientRow(
        family="Sigma_W_2L",
        source_key="toy_FHW_2002",
        expression="toy_c1 * I4 + toy_c2 * tadpole",
        master_basis="B_two_point_5line_Euclidean",
        source_certified=True,
    )
    check(validate_row(good), "toy valid row must pass")

    # (e) Refusals.
    bad_family = CoefficientRow(family="not_a_family", source_key="x",
                                expression="x", master_basis="x",
                                source_certified=True)
    check(not validate_row(bad_family), "bad family must be refused")

    uncertified = CoefficientRow(family="Sigma_W_2L", source_key="x",
                                 expression="x", master_basis="x",
                                 source_certified=False)
    check(not validate_row(uncertified), "uncertified row must be refused")

    target_consuming = CoefficientRow(family="Sigma_W_2L", source_key="x",
                                      expression="x", master_basis="x",
                                      source_certified=True,
                                      target_consumed=True)
    check(not validate_row(target_consuming),
          "target-consuming row must be refused")

    fitted = CoefficientRow(family="Sigma_W_2L", source_key="x", expression="x",
                            master_basis="x", source_certified=True,
                            fitted=True)
    check(not validate_row(fitted), "fitted row must be refused")

    empty_field = CoefficientRow(family="Sigma_W_2L", source_key="",
                                 expression="x", master_basis="x",
                                 source_certified=True)
    check(not validate_row(empty_field),
          "row with empty source_key must be refused")

    # (f) complete_physical_ledger on empty list returns False.
    check(complete_physical_ledger([]) is False,
          "empty ledger cannot be complete")
    check(complete_physical_ledger([good]) is False,
          "single-row ledger cannot cover 6 OPEN_PHYSICAL_FAMILIES")
    check(current_v6_promotes_complete_ledger() is False,
          "v6 must NOT promote complete physical ledger")

    # (g) Honest non-claim flags.
    for ec in ["Export_EW_coefficient_derivation_engine_contract_P",
               "Export_EW_required_coefficient_family_matrix_P",
               "Export_EW_no_smuggling_row_validation_P",
               "Export_EW_derivation_plan_P"]:
        check(EXPORT_FLAGS[ec] == 1, f"{ec} must be 1")
    for nc in ["Export_complete_physical_coefficient_ledger_P",
               "Export_evaluated_Sigma_W_2L_P", "Export_evaluated_Sigma_Z_2L_P",
               "Export_evaluated_Pi_gammagamma_2L_P", "Export_evaluated_Pi_gammaZ_2L_P",
               "Export_evaluated_vertex_box_2L_P",
               "Export_OSW_delta_r_rem_APF_internal_P"]:
        check(EXPORT_FLAGS[nc] == 0, f"{nc} must remain 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_two_loop_phase2_ew_diagram_coefficient_derivation_engine_scaffold_v1: "
              "Derivation engine scaffold — 8 required families (6 OPEN physical: "
              "Σ_W/Σ_Z/Π_γγ/Π_γZ + muon-decay vertex/box + Zℓℓ vertex; 2 scheme: "
              "counterterm products + tadpole convention), 6 forbidden inputs, "
              "7-stage derivation matrix (diagram_inventory → projectors → "
              "algebra → IBP → master eval → assembly → comparator), "
              "CoefficientRow validator refusing uncertified/target-consuming/"
              "fitted rows. NO physical rows populated. "
              "[P_two_loop_phase2_ew_diagram_coefficient_derivation_engine_scaffold_v1; "
              "C_physical_coefficient_rows_pending]"),
        tier=4,
        epistemic="P_two_loop_phase2_ew_diagram_coefficient_derivation_engine_scaffold_v1",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v6 / "
            "APF_TWO_LOOP_PHASE2_EW_DIAGRAM_COEFFICIENT_DERIVATION_ENGINE_SCAFFOLD_v1. "
            "Executes v24.3.155 Stages C-G as a typed contract. REQUIRED_FAMILIES "
            "(8): the 4 EW self-energy channels Σ_W/Σ_Z/Π_γγ/Π_γZ + 2 vertex/box "
            "families (muon-decay, Z→ℓℓ) + 2 scheme families (counterterm "
            "products, tadpole convention). OPEN_PHYSICAL_FAMILIES (6): the 4 "
            "self-energies + 2 vertex/box. Forbidden inputs (6): measured_MW, "
            "published_total_SM_MW, DIZET_aggregate_component, ZFITTER_total_input, "
            "target_interval, fitted_counterterm. CoefficientRow validator "
            "refuses: bad family, missing source_key/expression/master_basis, "
            "target_consumed=True, fitted=True, source_certified=False. "
            "complete_physical_ledger() returns True only when the 6 OPEN "
            "physical families are all covered by valid rows — currently "
            "False (no rows supplied). 7-stage derivation matrix encoded as "
            "tuples with (stage_id, name, input, output, promotion_gate)."
        ),
        key_result=(
            "Derivation engine scaffold (8 families / 6 OPEN / 6 forbidden / "
            "7 stages) + validator + complete-ledger gate banked at scoped "
            "grade; no physical rows. "
            "[P_two_loop_phase2_ew_diagram_coefficient_derivation_engine_scaffold_v1; "
            "C_physical_coefficient_rows_pending]"
        ),
        dependencies=[
            "T_two_loop_phase2_missing_terms_source_and_derivation_plan",
            "T_two_loop_phase2_delta_r_source_import_v1",
            "T_two_loop_phase2_zpole_bosonic_deltakappa_import_v1",
            "T_two_loop_phase2_zfitter_comparator_guard_v1",
        ],
        cross_refs=[
            "T_two_loop_phase2_ew_coefficient_ledger_audit_scaffold",
            "T_two_loop_phase2_ew_self_energy_assembly_gate_toy_ledger",
        ],
        artifacts={
            "required_family_count": len(REQUIRED_FAMILIES),
            "open_physical_family_count": len(OPEN_PHYSICAL_FAMILIES),
            "required_families": sorted(REQUIRED_FAMILIES),
            "open_physical_families": sorted(OPEN_PHYSICAL_FAMILIES),
            "forbidden_inputs": sorted(FORBIDDEN_INPUTS),
            "derivation_stage_count": len(DERIVATION_STAGES),
            "stage_names": [s[1] for s in DERIVATION_STAGES],
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_phase2_ew_diagram_coefficient_derivation_engine_scaffold_v1":
        check_T_two_loop_phase2_ew_diagram_coefficient_derivation_engine_scaffold_v1_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
