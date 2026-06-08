"""APF-native two-loop Phase-2 fermionic vertex reduction method ledger (METHODS ONLY) — Tier-4.

ACFW 2004 (`hep-ph/0408207`) fermionic two-loop sin²θ_eff methods banked as
named row records. Five methods banked:

  * `top_large_mass` — top-quark closed fermion loops via x = M_Z²/m_t²
    expansion to order x⁵.
  * `light_LF1_DE` — light-fermion subloop LF1 differential equation +
    Nielsen polylog finite part.
  * `idsolver_prototype` — DiaGen/IdSolver Prototype/PrototypeList topology
    matching + subprototype hierarchy + IBP/Lorentz identities.
  * `idsolver_integral` — Integral/IntegralList linear-combination
    expressions over masters with rational coefficients.
  * `evaluation_homomorphism` — projection to rational field for master
    identification.

Every row carries `status='coefficient_table_open'`. The methods are
banked; the source does NOT print a complete row-local EW coefficient table
for all fermionic Z→ll vertex diagrams, so the coefficient table itself
remains OPEN and explicitly requires either (a) DiaGen/IdSolver output
tables (additional source upload) OR (b) APF-internal reproduction of the
reduction.

Honest non-claims preserved:
  * Export_fermionic_full_coefficient_table = 0
  * Export_evaluated_fermionic_Zll_2L_vertex = 0

Sibling APF_TWO_LOOP_PHASE2_FERMIONIC_VERTEX_REDUCTION_LEDGER_v1 via
APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v5.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Set

from apf.apf_utils import check, _result


@dataclass(frozen=True)
class FermionicReductionRow:
    row_id: str
    diagram_family: str
    source_object: str
    promotion_class: str
    status: str = "coefficient_table_open"


REQUIRED_ROWS: Set[str] = {
    "top_large_mass",
    "light_LF1_DE",
    "idsolver_prototype",
    "idsolver_integral",
    "evaluation_homomorphism",
}


REDUCTION_LEDGER = (
    FermionicReductionRow(
        row_id="top_large_mass",
        diagram_family="top-quark closed fermion loops",
        source_object="x=MZ^2/mt^2 expansion to order x^5",
        promotion_class="method_anchor",
    ),
    FermionicReductionRow(
        row_id="light_LF1_DE",
        diagram_family="light-fermion subloop",
        source_object="differential equation for LF1 and Nielsen polylog finite part",
        promotion_class="example_integral_anchor",
    ),
    FermionicReductionRow(
        row_id="idsolver_prototype",
        diagram_family="reduction infrastructure",
        source_object=("Prototype/PrototypeList topology matching, "
                       "subprototype hierarchy, IBP/Lorentz identities"),
        promotion_class="reduction_contract",
    ),
    FermionicReductionRow(
        row_id="idsolver_integral",
        diagram_family="reduction infrastructure",
        source_object=("Integral/IntegralList expressions as linear "
                       "combinations of masters with rational coefficients"),
        promotion_class="reduction_contract",
    ),
    FermionicReductionRow(
        row_id="evaluation_homomorphism",
        diagram_family="master identification",
        source_object="projection to rational field for master identification",
        promotion_class="method_anchor",
    ),
)


EXPORT_FLAGS = {
    "Export_fermionic_vertex_reduction_method_ledger_P": 1,
    "Export_fermionic_top_large_mass_method_anchor_P": 1,
    "Export_fermionic_light_DE_polylog_method_anchor_P": 1,
    "Export_DiaGen_IdSolver_reduction_contract_P": 1,
    "Export_fermionic_full_coefficient_table_P": 0,
    "Export_evaluated_fermionic_Zll_2L_vertex_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_phase2_fermionic_vertex_reduction_ledger_P():
    """T: ACFW 2004 fermionic two-loop sin²θ_eff methods banked as 5 named
    rows (top-large-mass, light-LF1 DE, DiaGen prototype, IdSolver integral,
    evaluation homomorphism). Every row at status='coefficient_table_open';
    full coefficient table requires DiaGen/IdSolver outputs or APF
    reproduction.
    [P_two_loop_phase2_fermionic_vertex_reduction_ledger;
     C_fermionic_full_coefficient_table_pending]."""

    row_ids = {r.row_id for r in REDUCTION_LEDGER}
    check(row_ids == REQUIRED_ROWS,
          f"row id mismatch: got {sorted(row_ids)}, expected {sorted(REQUIRED_ROWS)}")
    for r in REDUCTION_LEDGER:
        check(r.status == "coefficient_table_open",
              f"row {r.row_id}: status must be coefficient_table_open, got {r.status}")
        check(r.promotion_class in
              {"method_anchor", "example_integral_anchor", "reduction_contract"},
              f"row {r.row_id}: bad promotion class {r.promotion_class}")
        check(r.diagram_family.strip() != "" and r.source_object.strip() != "",
              f"row {r.row_id}: empty diagram_family or source_object")

    check(EXPORT_FLAGS["Export_fermionic_vertex_reduction_method_ledger_P"] == 1,
          "method ledger flag must be 1")
    check(EXPORT_FLAGS["Export_DiaGen_IdSolver_reduction_contract_P"] == 1,
          "DiaGen/IdSolver contract flag must be 1")
    check(EXPORT_FLAGS["Export_fermionic_full_coefficient_table_P"] == 0,
          "full coefficient table must remain 0")
    check(EXPORT_FLAGS["Export_evaluated_fermionic_Zll_2L_vertex_P"] == 0,
          "evaluated fermionic Zll 2L vertex must remain 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_two_loop_phase2_fermionic_vertex_reduction_ledger: "
              "ACFW 2004 fermionic two-loop sin²θ_eff method ledger — 5 rows "
              "(top-large-mass expansion, light-LF1 differential equation + "
              "Nielsen polylog, DiaGen Prototype topology matching, IdSolver "
              "Integral linear combinations over masters, evaluation "
              "homomorphism to rational field). All rows status="
              "'coefficient_table_open'. Full row-local EW coefficient table "
              "requires DiaGen/IdSolver outputs or APF reproduction. "
              "[P_two_loop_phase2_fermionic_vertex_reduction_ledger; "
              "C_fermionic_full_coefficient_table_pending]"),
        tier=4,
        epistemic="P_two_loop_phase2_fermionic_vertex_reduction_ledger",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v5 / "
            "APF_TWO_LOOP_PHASE2_FERMIONIC_VERTEX_REDUCTION_LEDGER_v1. Five "
            "named FermionicReductionRow records: (1) top_large_mass — "
            "top-quark closed fermion loops via x = M_Z²/m_t² expansion to "
            "order x⁵, method_anchor; (2) light_LF1_DE — light-fermion "
            "subloop with LF1 differential equation + Nielsen polylog finite "
            "part, example_integral_anchor; (3) idsolver_prototype — "
            "DiaGen/IdSolver Prototype/PrototypeList topology matching + "
            "subprototype hierarchy + IBP/Lorentz identities, "
            "reduction_contract; (4) idsolver_integral — Integral/IntegralList "
            "linear combinations of masters with rational coefficients, "
            "reduction_contract; (5) evaluation_homomorphism — projection to "
            "rational field for master identification, method_anchor. The "
            "ACFW 2004 paper establishes methods + examples; it does NOT "
            "print the full row-local coefficient table for all fermionic "
            "Z→ll diagrams. Coefficient-table promotion requires either "
            "additional DiaGen/IdSolver outputs (next-gate source upload) or "
            "APF-internal reproduction of the reduction."
        ),
        key_result=(
            "Fermionic reduction method ledger (5 rows) + DiaGen/IdSolver "
            "contract; full coefficient table OPEN. "
            "[P_two_loop_phase2_fermionic_vertex_reduction_ledger; "
            "C_fermionic_full_coefficient_table_pending]"
        ),
        dependencies=[
            "T_two_loop_phase2_ew_tex_source_exact_extraction_v2",
        ],
        cross_refs=[
            "T_two_loop_phase2_bosonic_vertex_master_anchors_I4_I10",
        ],
        artifacts={
            "row_count": len(REDUCTION_LEDGER),
            "row_ids": sorted(REQUIRED_ROWS),
            "promotion_classes_present": sorted(
                {r.promotion_class for r in REDUCTION_LEDGER}),
            "status_field_uniform": "coefficient_table_open",
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_phase2_fermionic_vertex_reduction_ledger":
        check_T_two_loop_phase2_fermionic_vertex_reduction_ledger_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
