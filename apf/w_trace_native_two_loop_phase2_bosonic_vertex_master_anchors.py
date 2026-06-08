"""APF-native two-loop Phase-2 bosonic vertex master anchors I4-I10 (MASTERS ONLY) — Tier-4.

CAF 2006 (hep-ph/0602029, Eq. 7) hard-region bosonic two-loop master integrals
I4-I10 banked as named anchors with pole-order ledger and symbolic finite-part
expressions. Numeric values evaluable via sandboxed eval using S2 (Watson) and
zeta(3) constants.

CRITICAL: I4-I10 are MASTER INTEGRALS. The electroweak diagram coefficients
multiplying these masters in every bosonic two-loop diagram are NOT supplied
here. Coefficient ledger remains OPEN per v24.3.154 no-go.

Pole-order ledger: I4/I7 simple poles; I5/I8 double poles; I6/I9/I10 finite.

Sibling APF_TWO_LOOP_PHASE2_BOSONIC_VERTEX_MASTER_ANCHORS_v2 via
APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v5.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict

from apf.apf_utils import check, _result


S2 = 0.2604341376321621
ZETA3 = 1.2020569031595942


@dataclass(frozen=True)
class MasterAnchor:
    name: str
    pole_order: int
    leading_pole_coefficient: str
    finite_part_symbolic: str


ANCHORS: Dict[str, MasterAnchor] = {
    "I4":  MasterAnchor("I4",  1, "pi^2/9", "3*pi*S2/sqrt(3)-2*zeta3/9"),
    "I5":  MasterAnchor("I5",  2, "1/2",    "19/2+pi^2/18-9*S2/4-5*pi/sqrt(3)+pi*log(3)/sqrt(3)+9*pi*S2/(2*sqrt(3))-8*zeta3/3"),
    "I6":  MasterAnchor("I6",  0, "0",      "9*pi*S2/(2*sqrt(3))-8*zeta3/3"),
    "I7":  MasterAnchor("I7",  1, "pi^2/18", "-15*pi*S2/(2*sqrt(3))+23*zeta3/9"),
    "I8":  MasterAnchor("I8",  2, "1/2",    "5/2+pi^2/36+pi/sqrt(3)-9*pi*S2/(2*sqrt(3))+zeta3/3"),
    "I9":  MasterAnchor("I9",  0, "0",      "-pi^3/(54*sqrt(3))+3*pi*S2/(2*sqrt(3))+2*zeta3/9"),
    "I10": MasterAnchor("I10", 0, "0",      "3*pi*S2/sqrt(3)-5*zeta3/9"),
}


def eval_master_expr(expr: str, *, S2_val: float = S2, zeta3_val: float = ZETA3) -> float:
    env = {"pi": math.pi, "sqrt": math.sqrt, "log": math.log,
           "S2": S2_val, "zeta3": zeta3_val}
    return float(eval(expr.replace("^", "**"), {"__builtins__": {}}, env))


def finite_value(name: str) -> float:
    return eval_master_expr(ANCHORS[name].finite_part_symbolic)


EXPORT_FLAGS = {
    "Export_bosonic_I4_I10_master_anchor_P": 1,
    "Export_bosonic_ultrasoft_reduction_anchor_P": 1,
    "Export_bosonic_73_master_count_ledger_P": 1,
    "Export_bosonic_diagram_coefficient_rows_P": 0,
    "Export_evaluated_bosonic_Zll_2L_vertex_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_phase2_bosonic_vertex_master_anchors_I4_I10_P():
    """T: CAF 2006 bosonic hard-region masters I4-I10 with pole-order ledger,
    symbolic finite parts, and numeric evaluator using S2 + zeta3 constants.
    Diagram coefficient rows NOT banked.
    [P_two_loop_phase2_bosonic_vertex_master_anchors_I4_I10;
     C_bosonic_diagram_coefficient_rows_pending]."""

    check(set(ANCHORS) == {"I4", "I5", "I6", "I7", "I8", "I9", "I10"},
          f"anchor set mismatch: got {sorted(ANCHORS)}")
    check(ANCHORS["I5"].pole_order == 2, "I5 double pole")
    check(ANCHORS["I8"].pole_order == 2, "I8 double pole")
    check(ANCHORS["I4"].pole_order == 1, "I4 simple pole")
    check(ANCHORS["I7"].pole_order == 1, "I7 simple pole")
    for fa in ("I6", "I9", "I10"):
        check(ANCHORS[fa].pole_order == 0, f"{fa} finite")

    values = {name: finite_value(name) for name in ANCHORS}
    for name, v in values.items():
        check(math.isfinite(v), f"{name} finite part not finite: {v}")
        check(abs(v) < 50.0, f"{name} magnitude bounded: got {v}")

    # Sensitivity: S2 -> 0 must shift I4 finite part (I4 contains S2 in finite part)
    v_I4_no_S2 = eval_master_expr(ANCHORS["I4"].finite_part_symbolic, S2_val=0.0)
    check(abs(values["I4"] - v_I4_no_S2) > 1e-6,
          f"I4 must depend on S2: with-S2={values['I4']}, without-S2={v_I4_no_S2}")
    # Sensitivity: zeta3 -> 0 must shift I6 (purely S2 + zeta3, no poles)
    v_I6_no_z3 = eval_master_expr(ANCHORS["I6"].finite_part_symbolic, zeta3_val=0.0)
    check(abs(values["I6"] - v_I6_no_z3) > 1e-6,
          f"I6 must depend on zeta3: with={values['I6']}, without={v_I6_no_z3}")

    check(abs(S2 - 0.260434137632) < 1e-10, f"S2 drift: {S2}")
    check(abs(ZETA3 - 1.2020569031595942) < 1e-15, f"zeta3 drift: {ZETA3}")

    check(EXPORT_FLAGS["Export_bosonic_I4_I10_master_anchor_P"] == 1, "master anchor flag")
    check(EXPORT_FLAGS["Export_bosonic_diagram_coefficient_rows_P"] == 0, "diagram coeff rows must be 0")
    check(EXPORT_FLAGS["Export_evaluated_bosonic_Zll_2L_vertex_P"] == 0, "evaluated vertex must be 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_two_loop_phase2_bosonic_vertex_master_anchors_I4_I10: "
              "CAF 2006 bosonic hard-region masters I4-I10 with pole-order "
              "ledger + symbolic + numeric finite-part evaluator using S2 + "
              "zeta3 constants. Sensitivity-tested vs constants. Diagram "
              "coefficients multiplying masters NOT supplied. "
              "[P_two_loop_phase2_bosonic_vertex_master_anchors_I4_I10; "
              "C_bosonic_diagram_coefficient_rows_pending]"),
        tier=4,
        epistemic="P_two_loop_phase2_bosonic_vertex_master_anchors_I4_I10",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v5 / "
            "APF_TWO_LOOP_PHASE2_BOSONIC_VERTEX_MASTER_ANCHORS_v2. "
            "I4-I10 banked as named MasterAnchor records with pole_order "
            "(I4/I7 simple, I5/I8 double, I6/I9/I10 finite), "
            "leading_pole_coefficient and finite_part_symbolic strings, and "
            "numeric eval via sandboxed Python using S2 = (4/(9 sqrt(3))) * "
            "Cl_2(pi/3) ~ 0.260434 and zeta(3) ~ 1.202057. Constants are "
            "sensitivity-tested: S2 -> 0 shifts I4; zeta3 -> 0 shifts I6. "
            "Magnitudes verified bounded |v| < 50. Master integrals only; "
            "diagram coefficient rows remain at v24.3.154 no-go boundary."
        ),
        key_result=(
            "I4-I10 bosonic master anchors + pole-order ledger + numeric "
            "finite-part evaluator. Diagram coefficient rows OPEN. "
            "[P_two_loop_phase2_bosonic_vertex_master_anchors_I4_I10; "
            "C_bosonic_diagram_coefficient_rows_pending]"
        ),
        dependencies=[
            "T_two_loop_phase2_ew_tex_source_exact_extraction_v2",
            "T_two_loop_phase2_ew_source_table_extraction_aggregate_and_convention",
        ],
        cross_refs=[
            "T_two_loop_sunrise_2d_finite_core_and_boundary",
            "T_two_loop_two_point_5line_euclidean_master_arbitrary_mass",
        ],
        artifacts={
            "anchor_names": sorted(ANCHORS),
            "double_pole_anchors": ["I5", "I8"],
            "simple_pole_anchors": ["I4", "I7"],
            "finite_anchors": ["I6", "I9", "I10"],
            "constants": {"S2": S2, "zeta3": ZETA3},
            "numeric_finite_parts": {n: finite_value(n) for n in ANCHORS},
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_phase2_bosonic_vertex_master_anchors_I4_I10":
        check_T_two_loop_phase2_bosonic_vertex_master_anchors_I4_I10_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
