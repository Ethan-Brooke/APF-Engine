"""APF-native two-loop Phase-2 degree-5 coefficient surface + no-smuggling sector guard — Tier-4.

Phase-2 push v11 expands the coefficient-output surface after v10: TP5
degree-5 numerator-lowering rows, a TP5 sector / no-smuggling ledger, SUN3
Taylor recurrence rows, a muon hard-hard matching contract, and a full-family
status pack.

The verifiable native content this module re-derives is twofold:

  1. the TP5 numerator-expansion identity at degree 5 (the (5,0,0)/(0,5,0)/
     (0,0,5) corners and a mixed (2,2,1) monomial) reconstructs exactly in
     sympy from the emitted rational coefficient rows; and

  2. the no-smuggling sector guard: a genuine five-line TP5 master may NOT be
     replaced by a product of one-loop B0×B0 bubbles unless its central line
     (D3) has been genuinely contracted away. The guard returns False for the
     genuine case and admits the B0×B0 product limit only for the
     central-line-removed sector classes. This is the same irreducibility
     discipline that v24.3.143's central-line m₃² sensitivity test established.

It does NOT claim the complete physical electroweak two-loop coefficient ledger.

Honest non-claims preserved verbatim:
  * Export_complete_EW_two_loop_diagram_coefficient_ledger_P = 0
  * Export_EW_physical_self_energy_evaluator_P = 0
  * Export_OSW_delta_r_rem_APF_internal_P = 0
  * Export_TP5_full_Laporta_reduction_P = 0

Sibling APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v11
(self-verifier TWO_LOOP_PHASE2_PUSH_V11_PASS, 7/7).
"""
from __future__ import annotations

import sympy as sp

from apf.apf_utils import check, _result


# =============================================================================
# Source-certified kernel: degree-5 TP5 expansion + no-smuggling sector guard
# =============================================================================

D1, D2, D3, D4, D5 = sp.symbols("D1 D2 D3 D4 D5")
m1_2, m2_2, m3_2, m4_2, m5_2, s = sp.symbols("m1_2 m2_2 m3_2 m4_2 m5_2 s")
_DS = (D1, D2, D3, D4, D5)

_SP = {
    "pk": (D1 - D4 + m1_2 - m4_2 + s) / 2,
    "qk": (D2 - D5 + m2_2 - m5_2 + s) / 2,
    "pq": (D1 + D2 - D3 + m1_2 + m2_2 - m3_2) / 2,
}


def expr(e):
    a, b, c = e
    return sp.expand(_SP["pk"] ** a * _SP["qk"] ** b * _SP["pq"] ** c)


def coefficient_rows(e):
    poly = sp.Poly(expr(e), *_DS)
    return [{"D_powers": tuple(int(x) for x in powers), "coefficient": coeff,
             "physical_value": 0, "complete_family": 0}
            for powers, coeff in poly.terms()]


def reconstruct(e, rows):
    total = 0
    for r in rows:
        term = r["coefficient"]
        for D, p in zip(_DS, r["D_powers"]):
            term *= D ** p
        total += term
    return sp.expand(total)


# ----- no-smuggling sector guard --------------------------------------------

def classify_powers(powers):
    """Sector class of a TP5 denominator-power tuple after numerator lowering."""
    removed = [i for i, p in enumerate(powers) if p <= 0]
    central_removed = powers[2] <= 0
    if not removed:
        return "unit_power_genuine_five_line_constant_term"
    if central_removed and len(removed) == 1:
        return "central_line_removed_B0xB0_product_limit"
    if central_removed:
        return "central_line_removed_with_additional_contractions"
    return "noncentral_contracted_subtopology_still_two_loop"


_ALLOWED_PRODUCT_CLASSES = {
    "central_line_removed_B0xB0_product_limit",
    "central_line_removed_with_additional_contractions",
}


def may_use_B0xB0(sector_class: str) -> bool:
    return sector_class in _ALLOWED_PRODUCT_CLASSES


def may_replace_genuine_TP5_by_B0xB0(original_has_central_line: bool = True) -> bool:
    """Refuse replacing a genuine (central-line-present) TP5 master by a B0×B0 product."""
    return False if original_has_central_line else True


FOUR_SECTOR_CLASSES = (
    "unit_power_genuine_five_line_constant_term",
    "central_line_removed_B0xB0_product_limit",
    "central_line_removed_with_additional_contractions",
    "noncentral_contracted_subtopology_still_two_loop",
)


EXPORT_FLAGS = {
    "Export_phase2_degree5_coefficient_surface_P": 1,
    "Export_TP5_B0xB0_smuggling_refusal_P": 1,
    "Export_SUN3_Taylor_recurrence_rows_P": 1,
    "Export_muon_hard_matching_contract_P": 1,
    "Export_complete_EW_two_loop_diagram_coefficient_ledger_P": 0,
    "Export_EW_physical_self_energy_evaluator_P": 0,
    "Export_OSW_delta_r_rem_APF_internal_P": 0,
    "Export_TP5_full_Laporta_reduction_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_phase2_coefficient_surface_no_smuggling_current_depth_P():
    """T: Phase-2 degree-5 coefficient surface + no-smuggling sector guard. The
    TP5 expansion identity reconstructs exactly at degree 5 (corners + mixed).
    The no-smuggling guard refuses replacing a genuine (central-line-present)
    TP5 master by a B0×B0 product, admitting the product limit only for
    central-line-removed sectors. Four sector classes enumerated; B0×B0 allowed
    only for central-line-removed classes. No physical ledger, no full Laporta.
    [P_two_loop_phase2_coefficient_surface_no_smuggling_current_depth;
     C_complete_physical_coefficient_ledger_pending]."""

    # (a) Exact degree-5 reconstruction (corners + a mixed monomial).
    for e in [(5, 0, 0), (0, 5, 0), (0, 0, 5), (2, 2, 1), (1, 3, 1)]:
        rows = coefficient_rows(e)
        check(sp.expand(expr(e) - reconstruct(e, rows)) == 0,
              f"TP5 degree-5 monomial {e} must reconstruct exactly")
        check(sum(e) == 5 or sum(e) == 4 or all(r["physical_value"] == 0 for r in rows),
              f"monomial {e} rows must stay physical_value=0")
        check(all(r["physical_value"] == 0 for r in rows),
              f"monomial {e} rows must be physical_value=0")

    # (b) No-smuggling guard: genuine TP5 cannot be replaced by B0×B0.
    check(may_replace_genuine_TP5_by_B0xB0(True) is False,
          "genuine (central-line-present) TP5 must NOT be replaceable by B0×B0")
    check(may_replace_genuine_TP5_by_B0xB0(False) is True,
          "with central line genuinely removed, B0×B0 product limit is admissible")

    # (c) B0×B0 allowed only for central-line-removed sector classes.
    for sc in FOUR_SECTOR_CLASSES:
        expected = sc.startswith("central_line_removed")
        check(may_use_B0xB0(sc) == expected,
              f"B0×B0 admissibility for {sc} must be {expected}")

    # (d) Sector classifier is correct on representative power tuples.
    check(classify_powers((1, 1, 1, 1, 1))
          == "unit_power_genuine_five_line_constant_term",
          "all-positive powers → genuine five-line")
    check(classify_powers((1, 1, 0, 1, 1))
          == "central_line_removed_B0xB0_product_limit",
          "only D3 removed → B0×B0 product limit")
    check(classify_powers((1, 1, 0, 0, 1))
          == "central_line_removed_with_additional_contractions",
          "D3 + another removed → central-removed-with-contractions")
    check(classify_powers((0, 1, 1, 1, 1))
          == "noncentral_contracted_subtopology_still_two_loop",
          "non-central removal with D3 present → still two-loop")

    # (e) Honest non-claim flags.
    for k in ("Export_complete_EW_two_loop_diagram_coefficient_ledger_P",
              "Export_EW_physical_self_energy_evaluator_P",
              "Export_OSW_delta_r_rem_APF_internal_P",
              "Export_TP5_full_Laporta_reduction_P"):
        check(EXPORT_FLAGS[k] == 0, f"{k} must remain 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_two_loop_phase2_coefficient_surface_no_smuggling_current_depth: "
              "Phase-2 degree-5 TP5 coefficient surface + no-smuggling sector "
              "guard. Degree-5 expansion reconstructs exactly; genuine TP5 "
              "cannot be replaced by a B0×B0 product. "
              "[P_two_loop_phase2_coefficient_surface_no_smuggling_current_depth]"),
        tier=4,
        epistemic="P_two_loop_phase2_coefficient_surface_no_smuggling_current_depth",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v11 "
            "(5 packs: TP5 degree-5 native coefficient output, TP5 sector / "
            "no-smuggling ledger, SUN3 Taylor recurrence, muon hard-matching "
            "contract, full-family row-run status; self-verifier 7/7 PASS). "
            "This module re-derives two things: (1) the TP5 numerator-expansion "
            "identity at degree 5 — the (5,0,0)/(0,5,0)/(0,0,5) corners plus a "
            "mixed (2,2,1) monomial reconstruct exactly in sympy from the "
            "emitted rational coefficient rows, all physical_value=0; and (2) "
            "the no-smuggling sector guard, which refuses replacing a genuine "
            "(central-line-present) five-line TP5 master by a product of "
            "one-loop B0×B0 bubbles, admitting the product limit only for "
            "sector classes where the central line (D3) has been genuinely "
            "contracted away. The four sector classes are enumerated and the "
            "classifier verified on representative power tuples. This is the "
            "same irreducibility discipline anchored by v24.3.143's central-line "
            "m₃² sensitivity falsifier. The complete physical EW two-loop "
            "coefficient ledger and full TP5 Laporta reduction remain open."
        ),
        key_result=(
            "Phase-2 degree-5 TP5 surface (exact reconstruction) + no-smuggling "
            "B0×B0 refusal guard with four enumerated sector classes. "
            "[P_two_loop_phase2_coefficient_surface_no_smuggling_current_depth]"
        ),
        dependencies=[
            "T_two_loop_phase2_coefficient_output_slices_current_depth",
            "T_two_loop_two_point_5line_euclidean_master_arbitrary_mass",
        ],
        cross_refs=[],
        artifacts={
            "sector_classes": list(FOUR_SECTOR_CLASSES),
            "degree5_test_monomials": ["(5, 0, 0)", "(0, 5, 0)", "(0, 0, 5)", "(2, 2, 1)"],
            "sibling_bundle": "APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v11",
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_phase2_coefficient_surface_no_smuggling_current_depth":
        check_T_two_loop_phase2_coefficient_surface_no_smuggling_current_depth_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
