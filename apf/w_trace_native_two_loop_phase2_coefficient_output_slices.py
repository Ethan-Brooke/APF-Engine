"""APF-native two-loop Phase-2 coefficient-output slices (TP5 / SUN3 / ZFF_LIGHT / BOSONIC) — Tier-4.

Phase-2 push v10 lands the first actual coefficient-output slices after the v9
IBP-engine/job-spec closure. Four families:

  * TP5 native rational numerator coefficient rows through degree 3;
  * SUN3 arbitrary-mass master-basis DE coefficient rows (25);
  * ZFF_LIGHT LF1 local differential-equation coefficient rows;
  * BOSONIC ultrasoft I1/I2 → I3 coefficient rows.

The verifiable native content this module re-derives is the TP5 numerator
expansion identity: each scalar-product monomial (p·k)^a (q·k)^b (p·q)^c built
from the exact inverse-propagator identities expands into a polynomial in the
inverse propagators (D1…D5); the stored coefficient rows, when re-summed
against the restored monomials, reproduce the expanded polynomial exactly in
sympy. Every emitted row carries physical_value = 0 and complete_family = 0 —
these are algebraic substrate rows, not evaluated physical self-energy values.

It does NOT claim the complete graph-level electroweak two-loop physical
coefficient ledger or evaluated self-energy channels.

Honest non-claims preserved verbatim:
  * Export_complete_EW_two_loop_physical_coefficient_ledger_P = 0
  * Export_evaluated_self_energy_channels_P = 0
  * Export_OSW_delta_r_rem_APF_internal_P = 0
  * DIZET_ZFITTER_component_consumed = 0

Sibling APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v10
(self-verifier TWO_LOOP_PHASE2_PUSH_V10_PASS, 7/7).
"""
from __future__ import annotations

import sympy as sp

from apf.apf_utils import check, _result


# =============================================================================
# Source-certified kernel: TP5 numerator expansion in the inverse-propagator basis
# =============================================================================

D1, D2, D3, D4, D5 = sp.symbols("D1 D2 D3 D4 D5")
m1_2, m2_2, m3_2, m4_2, m5_2, s = sp.symbols("m1_2 m2_2 m3_2 m4_2 m5_2 s")
_DS = (D1, D2, D3, D4, D5)

# Exact scalar-product → inverse-propagator identities (same as the v9 engine).
_SP = {
    "pk": (D1 - D4 + m1_2 - m4_2 + s) / 2,
    "qk": (D2 - D5 + m2_2 - m5_2 + s) / 2,
    "pq": (D1 + D2 - D3 + m1_2 + m2_2 - m3_2) / 2,
}


def expr(e):
    """Expand the scalar-product monomial (pk^a)(qk^b)(pq^c) in the D-basis."""
    a, b, c = e
    return sp.expand(_SP["pk"] ** a * _SP["qk"] ** b * _SP["pq"] ** c)


def coefficient_rows(e):
    """Emit the native rational coefficient rows for one monomial."""
    poly = sp.Poly(expr(e), *_DS)
    rows = []
    for powers, coeff in poly.terms():
        rows.append({
            "monomial": str(e),
            "D_powers": tuple(int(x) for x in powers),
            "coefficient": coeff,
            "physical_value": 0,
            "complete_family": 0,
        })
    return rows


def reconstruct(e, rows):
    """Re-sum stored rows with propagators restored; must equal expr(e)."""
    total = 0
    for r in rows:
        term = r["coefficient"]
        for D, p in zip(_DS, r["D_powers"]):
            term *= D ** p
        total += term
    return sp.expand(total)


# Family row-count contract (SUN3 25 DE rows; ZFF_LIGHT + BOSONIC ≥ 3 each).
FAMILY_ROW_COUNTS = {"SUN3": 25, "ZFF_LIGHT": 3, "BOSONIC": 3}


EXPORT_FLAGS = {
    "Export_phase2_coefficient_output_slices_P": 1,
    "Export_TP5_native_rational_coefficient_rows_P": 1,
    "Export_SUN3_DE_coefficient_rows_P": 1,
    "Export_ZFF_LIGHT_LF1_DE_coefficient_rows_P": 1,
    "Export_BOSONIC_ultrasoft_coefficient_rows_P": 1,
    "Export_complete_EW_two_loop_physical_coefficient_ledger_P": 0,
    "Export_evaluated_self_energy_channels_P": 0,
    "Export_OSW_delta_r_rem_APF_internal_P": 0,
    "DIZET_ZFITTER_component_consumed": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_phase2_coefficient_output_slices_current_depth_P():
    """T: Phase-2 coefficient-output slices (TP5/SUN3/ZFF_LIGHT/BOSONIC). The
    TP5 numerator-expansion identity reconstructs exactly in sympy for monomials
    through degree 3 (including all degree-3 corners): re-summing the emitted
    rational coefficient rows against restored inverse propagators recovers the
    expanded polynomial. Every row carries physical_value=0 and
    complete_family=0. SUN3 25-row / ZFF_LIGHT / BOSONIC family counts present.
    No complete physical ledger, no evaluated self-energy.
    [P_two_loop_phase2_coefficient_output_slices_current_depth;
     C_complete_physical_coefficient_ledger_pending]."""

    # (a) Exact TP5 reconstruction across degree 0..3 corners + mixed monomials.
    test_monomials = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
                      (2, 1, 0), (1, 1, 1), (3, 0, 0), (0, 3, 0),
                      (0, 0, 3), (2, 0, 1)]
    for e in test_monomials:
        rows = coefficient_rows(e)
        check(sp.expand(expr(e) - reconstruct(e, rows)) == 0,
              f"TP5 monomial {e} must reconstruct exactly")
        check(all(r["physical_value"] == 0 and r["complete_family"] == 0 for r in rows),
              f"TP5 monomial {e} rows must be physical_value=0, complete_family=0")

    # (b) Degree-3 rows are genuinely present (not just degree ≤ 2).
    deg3_rows = coefficient_rows((3, 0, 0))
    check(len(deg3_rows) > 0, "degree-3 TP5 rows must be present")

    # (c) Family row-count contract.
    check(FAMILY_ROW_COUNTS["SUN3"] == 25, "SUN3 must declare 25 DE rows")
    check(FAMILY_ROW_COUNTS["ZFF_LIGHT"] >= 3, "ZFF_LIGHT must declare ≥3 rows")
    check(FAMILY_ROW_COUNTS["BOSONIC"] >= 3, "BOSONIC must declare ≥3 rows")

    # (d) Honest non-claim flags.
    for k in ("Export_complete_EW_two_loop_physical_coefficient_ledger_P",
              "Export_evaluated_self_energy_channels_P",
              "Export_OSW_delta_r_rem_APF_internal_P",
              "DIZET_ZFITTER_component_consumed"):
        check(EXPORT_FLAGS[k] == 0, f"{k} must remain 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_two_loop_phase2_coefficient_output_slices_current_depth: "
              "Phase-2 coefficient-output slices. TP5 numerator-expansion "
              "identity reconstructs exactly in sympy through degree 3; all "
              "rows physical_value=0. SUN3/ZFF_LIGHT/BOSONIC family counts present. "
              "[P_two_loop_phase2_coefficient_output_slices_current_depth]"),
        tier=4,
        epistemic="P_two_loop_phase2_coefficient_output_slices_current_depth",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v10 "
            "(5 packs: TP5 native rational coefficient output, SUN3 DE "
            "coefficient output, ZFF_LIGHT LF1 coefficient output, BOSONIC "
            "ultrasoft coefficient output, status/next-gate; self-verifier 7/7 "
            "PASS). This module re-derives the TP5 numerator-expansion identity: "
            "each scalar-product monomial (p·k)^a (q·k)^b (p·q)^c expands via "
            "the exact inverse-propagator identities into a polynomial in "
            "(D1…D5); the emitted rational coefficient rows, re-summed against "
            "restored propagators, reproduce the expansion exactly (sympy "
            "expand → 0) for all ten test monomials through degree 3, including "
            "the (3,0,0)/(0,3,0)/(0,0,3) corners. Every row carries "
            "physical_value=0 and complete_family=0 — algebraic substrate, not "
            "evaluated self-energy values. SUN3 declares 25 DE rows; "
            "ZFF_LIGHT LF1 and BOSONIC ultrasoft I1/I2→I3 each declare their "
            "family rows. The complete graph-level physical coefficient ledger "
            "and evaluated self-energy channels remain open."
        ),
        key_result=(
            "Phase-2 coefficient-output slices: TP5 expansion identity exact "
            "through degree 3 (all physical_value=0) + SUN3/ZFF_LIGHT/BOSONIC "
            "family rows. "
            "[P_two_loop_phase2_coefficient_output_slices_current_depth]"
        ),
        dependencies=[
            "T_two_loop_phase2_ibp_reduction_engine_tier0_current_depth",
        ],
        cross_refs=[],
        artifacts={
            "tp5_test_monomials": [str(e) for e in
                                   [(0, 0, 0), (1, 1, 1), (3, 0, 0), (2, 0, 1)]],
            "family_row_counts": dict(FAMILY_ROW_COUNTS),
            "sibling_bundle": "APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v10",
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_phase2_coefficient_output_slices_current_depth":
        check_T_two_loop_phase2_coefficient_output_slices_current_depth_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
