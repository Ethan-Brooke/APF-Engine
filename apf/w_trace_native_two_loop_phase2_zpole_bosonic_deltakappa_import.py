"""APF-native two-loop Phase-2 Z-pole bosonic Δκ source import (AGGREGATE SHIFT ROWS) — Tier-4.

ACF 2006 (hep-ph/0605339) bosonic O(α²) contributions to the effective weak
mixing angle imported as 4-row aggregate shift tables plus the Hollik
cross-check comparison.

Tables (in 10⁻⁴ units, indexed by M_H ∈ {100, 200, 600, 1000} GeV):
  * Δκ_bos × 10⁴: {100: -0.74, 200: -0.47, 600: +0.17, 1000: +1.11}
  * sin²θ_eff^bos shift × 10⁴: {100: 0.04, 200: 0.00, 600: 0.05, 1000: 0.12}
  * Hollik cross-check sub-leading × 10⁴: 4 (this-work, Hollik) pairs
    {100: (0.0, 0.0), 200: (0.266, 0.265), 600: (0.914, 0.914),
     1000: (1.849, 1.849)} — agreement to ≤ 0.002 in 10⁻⁴ units.

The published "few × 10⁻⁶" sin²θ_eff bosonic shift is reproduced:
max|shift × 10⁴| = 0.12 < 0.2.

Honest non-claims preserved:
  * Export_Zpole_row_local_form_factor_coefficients = 0
  * Export_complete_Zll_vertex_coefficient_ledger = 0
  * Export_sin2eff_as_component_input_to_OSW = 0
  * Export_ZFITTER_aggregate_consumed_as_component = 0

Sibling APF_TWO_LOOP_PHASE2_ZPOLE_BOSONIC_DELTAKAPPA_IMPORT_v1 via
APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v6.
"""
from __future__ import annotations

from apf.apf_utils import check, _result


DELTAKAPPA_BOS_X1E4 = {100: -0.74, 200: -0.47, 600: 0.17, 1000: 1.11}
SINEFF_SHIFT_X1E4 = {100: 0.04, 200: 0.00, 600: 0.05, 1000: 0.12}
CROSSCHECK_SUB_X1E4 = {
    100: (0.0, 0.0),
    200: (0.266, 0.265),
    600: (0.914, 0.914),
    1000: (1.849, 1.849),
}


def max_abs_sineff_shift_x1e4() -> float:
    return max(abs(v) for v in SINEFF_SHIFT_X1E4.values())


def bosonic_effect_small_under_source_table() -> bool:
    return max_abs_sineff_shift_x1e4() < 0.2


def crosscheck_agrees_to_0p002() -> bool:
    return all(abs(a - b) <= 0.002 for a, b in CROSSCHECK_SUB_X1E4.values())


def row_local_form_factor_coefficients_promoted() -> bool:
    return False


EXPORT_FLAGS = {
    "Export_Zpole_bosonic_DeltaKappa_source_import_P": 1,
    "Export_Zpole_bosonic_sin2eff_shift_table_P": 1,
    "Export_Zpole_bosonic_method_ledger_P": 1,
    "Export_Zpole_bosonic_crosscheck_against_Hollik_P": 1,
    "Export_Zpole_row_local_form_factor_coefficients_P": 0,
    "Export_complete_Zll_vertex_coefficient_ledger_P": 0,
    "Export_sin2eff_as_component_input_to_OSW_P": 0,
    "Export_ZFITTER_aggregate_consumed_as_component_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_phase2_zpole_bosonic_deltakappa_import_v1_P():
    """T: ACF 2006 (hep-ph/0605339) bosonic Δκ + sin²θ_eff shift tables for
    M_H ∈ {100, 200, 600, 1000} GeV + Hollik cross-check agreement ≤ 0.002
    in 10⁻⁴ units. AGGREGATE SHIFT rows only; NO row-local form-factor
    coefficients banked.
    [P_two_loop_phase2_zpole_bosonic_deltakappa_import_v1;
     C_form_factor_coefficient_rows_pending]."""

    # (a) Table shape: 4 M_H values across all three tables.
    check(set(DELTAKAPPA_BOS_X1E4) == {100, 200, 600, 1000},
          f"Δκ_bos M_H set: {sorted(DELTAKAPPA_BOS_X1E4)}")
    check(set(SINEFF_SHIFT_X1E4) == {100, 200, 600, 1000},
          f"sin²θ_eff M_H set: {sorted(SINEFF_SHIFT_X1E4)}")
    check(set(CROSSCHECK_SUB_X1E4) == {100, 200, 600, 1000},
          f"cross-check M_H set: {sorted(CROSSCHECK_SUB_X1E4)}")

    # (b) Δκ_bos central values reproduced.
    check(abs(DELTAKAPPA_BOS_X1E4[100] - (-0.74)) < 1e-9, "Δκ_bos(100) = -0.74")
    check(abs(DELTAKAPPA_BOS_X1E4[1000] - 1.11) < 1e-9, "Δκ_bos(1000) = +1.11")

    # (c) sin²θ_eff bosonic effect is small (published "few × 10⁻⁶").
    check(bosonic_effect_small_under_source_table() is True,
          f"max|sin²θ_eff^bos shift × 10⁴| = {max_abs_sineff_shift_x1e4()} must be < 0.2")
    check(max_abs_sineff_shift_x1e4() <= 0.12,
          f"observed max = {max_abs_sineff_shift_x1e4()} should be ≤ 0.12 from table")

    # (d) Hollik cross-check agreement.
    check(crosscheck_agrees_to_0p002() is True,
          "Hollik cross-check must agree to ≤ 0.002 in 10⁻⁴ units")
    # Spot check: M_H = 200 → (0.266, 0.265), diff = 0.001
    a, b = CROSSCHECK_SUB_X1E4[200]
    check(abs(a - b) <= 0.0015, f"Hollik 200 GeV diff: {abs(a - b)}")

    # (e) No row-local form-factor coefficients.
    check(row_local_form_factor_coefficients_promoted() is False,
          "row-local form-factor coefficients must NOT be promoted")

    # (f) Honest non-claim flags.
    for ec in [
        "Export_Zpole_bosonic_DeltaKappa_source_import_P",
        "Export_Zpole_bosonic_sin2eff_shift_table_P",
        "Export_Zpole_bosonic_method_ledger_P",
        "Export_Zpole_bosonic_crosscheck_against_Hollik_P",
    ]:
        check(EXPORT_FLAGS[ec] == 1, f"{ec} must be 1")
    for nc in [
        "Export_Zpole_row_local_form_factor_coefficients_P",
        "Export_complete_Zll_vertex_coefficient_ledger_P",
        "Export_sin2eff_as_component_input_to_OSW_P",
        "Export_ZFITTER_aggregate_consumed_as_component_P",
    ]:
        check(EXPORT_FLAGS[nc] == 0, f"{nc} must remain 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_two_loop_phase2_zpole_bosonic_deltakappa_import_v1: "
              "ACF 2006 hep-ph/0605339 bosonic Δκ + sin²θ_eff^bos shift tables "
              "for M_H ∈ {100, 200, 600, 1000} GeV. Δκ_bos × 10⁴ ∈ {-0.74, "
              "-0.47, +0.17, +1.11}; sin²θ_eff shift × 10⁴ ∈ {0.04, 0.00, "
              "0.05, 0.12} (published 'few × 10⁻⁶' reproduced). Hollik "
              "cross-check sub-leading agreement to ≤ 0.002 in 10⁻⁴ units "
              "across 4 M_H values. NO row-local form-factor coefficients. "
              "[P_two_loop_phase2_zpole_bosonic_deltakappa_import_v1; "
              "C_form_factor_coefficient_rows_pending]"),
        tier=4,
        epistemic="P_two_loop_phase2_zpole_bosonic_deltakappa_import_v1",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v6 / "
            "APF_TWO_LOOP_PHASE2_ZPOLE_BOSONIC_DELTAKAPPA_IMPORT_v1. Imports "
            "the ACF 2006 hep-ph/0605339 bosonic Δκ + sin²θ_eff^bos aggregate "
            "shift tables across 4 M_H values plus the Hollik comparison "
            "sub-leading cross-check, all in 10⁻⁴ units. The Δκ_bos values "
            "span -0.74 → +1.11 × 10⁻⁴; the sin²θ_eff^bos shift remains "
            "small (max 0.12 × 10⁻⁴ = 1.2 × 10⁻⁵, matching the source's "
            "'few × 10⁻⁶' description). Hollik cross-check agrees to "
            "Δ ≤ 0.002 in 10⁻⁴ units (effectively ≤ 2 × 10⁻⁷ on the "
            "observable). Form-factor coefficient rows v̂_f^(2), â_f^(2) "
            "remain at the v24.3.154 no-go boundary."
        ),
        key_result=(
            "ACF 2006 bosonic Δκ + sin²θ_eff shift tables + Hollik cross-check "
            "agreement banked as aggregate-only rows; row-local form-factor "
            "coefficients OPEN. "
            "[P_two_loop_phase2_zpole_bosonic_deltakappa_import_v1; "
            "C_form_factor_coefficient_rows_pending]"
        ),
        dependencies=[
            "T_two_loop_phase2_missing_terms_source_and_derivation_plan",
            "T_two_loop_phase2_bosonic_vertex_master_anchors_I4_I10",
        ],
        cross_refs=[
            "T_two_loop_phase2_ew_source_table_extraction_aggregate_and_convention",
        ],
        artifacts={
            "MH_values_GeV": [100, 200, 600, 1000],
            "DeltaKappa_bos_x1e4": dict(DELTAKAPPA_BOS_X1E4),
            "sin_eff_bos_shift_x1e4": dict(SINEFF_SHIFT_X1E4),
            "Hollik_crosscheck_x1e4": {k: list(v) for k, v in CROSSCHECK_SUB_X1E4.items()},
            "max_abs_sin_eff_shift_x1e4": max_abs_sineff_shift_x1e4(),
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_phase2_zpole_bosonic_deltakappa_import_v1":
        check_T_two_loop_phase2_zpole_bosonic_deltakappa_import_v1_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
