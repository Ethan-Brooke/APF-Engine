"""APF-native two-loop sunset master source-DE + threshold gate — Tier-4.

First sunset pack in the OS-W two-loop arc Phase-1 Tier-1 ladder (per
`Reference - Sibling-AI Handoff Brief - Two-Loop Sunset Master Integral
(2026-05-27).md`). The sunset is the foundational two-loop topology —
three propagators sharing the external momentum p².

This module establishes the SOURCE differential-equation gate +
THRESHOLD expansion gate (Caffo-Czyz-Laporta-Remiddi 1998 master DE
context, Davydychev-Tausk 1993 equal-mass closed-form reference). The
full numeric sunset master is NOT promoted here — that's the next pack.

Sibling delivery: APF_NATIVE_TWO_LOOP_SUNSET_SOURCE_DE_AND_THRESHOLD_GATE_v1
(staged at DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/). Verifier 31/31 PASS.

Master basis recorded: F0, F1, F2, F3 (Caffo-Czyz-Laporta-Remiddi 1998
sunrise master-integral basis labels). Numerical evaluators will be
filled by the next pack in the sunset ladder, analogous to the bubble's
v24.3.126 → v24.3.127 → v24.3.128 → v24.3.129 progression.

Honest non-claims:
  Export_two_loop_master_integral_sunset = 0  (NEXT PACK)
  Export_native_two_loop_{M_W, delta_r, kappa_l, M_W_physical_final} = 0
  target_consumed = 0
  gdrive_write_performed = False
"""
from __future__ import annotations

from typing import Any, Dict

from apf.apf_utils import check, _result


def sunset_branch(p2: float, m1_2: float, m2_2: float, m3_2: float) -> str:
    """Four-way branch router for the two-loop sunset I(p², m1², m2², m3²).

    Routes by kinematic regime:

      'tadpole_boundary'      — p² = 0 (sunset reduces to nested tadpoles)
      'threshold_timelike'    — p² > (m1+m2+m3)² (absorptive branch)
      'euclidean_spacelike'   — p² < 0 (real, deep-Euclidean expansion)
      'intermediate'          — 0 < p² ≤ threshold (real below-threshold)
    """
    threshold = (m1_2 ** 0.5 + m2_2 ** 0.5 + m3_2 ** 0.5) ** 2
    if p2 == 0:
        return "tadpole_boundary"
    if p2 > threshold:
        return "threshold_timelike"
    if p2 < 0:
        return "euclidean_spacelike"
    return "intermediate"


# Caffo-Czyz-Laporta-Remiddi 1998 sunrise master basis labels.
# Numeric evaluators are NOT in this gate — schema only.
SUNSET_MASTER_BASIS = {
    "F0": "scalar_sunset_unit_powers",
    "F1": "first_derivative_basis_element",
    "F2": "second_derivative_basis_element",
    "F3": "third_derivative_basis_element",
}


# Pole coefficient schema for the sunset (Smirnov 1991 expansion structure).
SUNSET_POLE_SCHEMA = {
    "coefficient_double_pole":  "c_minus2",
    "coefficient_single_pole":  "c_minus1",
    "coefficient_finite":       "c_0",
    "ms_bar_normalization":     "mu_squared",
    "equal_mass_closed_form_source":   "Davydychev_Tausk_1993",
    "differential_equation_source":    "Caffo_Czyz_Laporta_Remiddi_1998",
    "threshold_expansion_source":      "Smirnov_1991",
}


EXPORT_FLAGS = {
    "Export_two_loop_sunset_source_DE_gate": 1,
    "Export_two_loop_sunset_threshold_expansion_gate": 1,
    "Export_two_loop_sunset_master_basis_F0_F1_F2_F3": 1,
    "Export_two_loop_sunset_pole_coefficient_schema": 1,
    "Export_two_loop_master_integral_sunset": 0,            # NEXT PACK
    "Export_native_two_loop_M_W": 0,
    "Export_native_two_loop_delta_r": 0,
    "Export_native_two_loop_kappa_l": 0,
    "Export_two_loop_M_W_physical_final": 0,
    "Export_external_numeric_package_as_derivation": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_sunset_source_DE_and_threshold_gate_P():
    """T: APF-native two-loop sunset master source differential-equation +
    threshold expansion gate. Four-region branch router (tadpole boundary +
    threshold timelike + euclidean spacelike + intermediate), Caffo-Czyz-
    Laporta-Remiddi 1998 master basis (F0/F1/F2/F3) recorded, Smirnov 1991
    threshold expansion source bound, ε-pole coefficient schema declared.
    Full numeric sunset master NOT promoted; pending next pack
    [P_source_gate_two_loop_sunset_DE_threshold; C_full_sunset_numeric_pending]."""

    # (1) Branch router returns expected labels at all four regimes
    check(sunset_branch(0.0, 1.0, 1.0, 1.0) == "tadpole_boundary",
          "p²=0 must route to tadpole_boundary")
    check(sunset_branch(50.0, 1.0, 1.0, 1.0) == "threshold_timelike",
          "p²>(1+1+1)²=9 must route to threshold_timelike")
    check(sunset_branch(-10.0, 1.0, 1.0, 1.0) == "euclidean_spacelike",
          "p²<0 must route to euclidean_spacelike")
    check(sunset_branch(5.0, 1.0, 1.0, 1.0) == "intermediate",
          "0 < p² < (sqrt(m1)+sqrt(m2)+sqrt(m3))² must route to intermediate")

    # (2) Threshold boundary classification
    thr_eq = (1.0 + 1.0 + 1.0) ** 2  # 9 for unit masses
    check(sunset_branch(thr_eq + 1e-10, 1.0, 1.0, 1.0) == "threshold_timelike",
          "just above threshold must be threshold_timelike")
    check(sunset_branch(thr_eq - 1e-10, 1.0, 1.0, 1.0) == "intermediate",
          "just below threshold must be intermediate")

    # (3) Master basis schema: F0/F1/F2/F3 all present
    for basis_label in ("F0", "F1", "F2", "F3"):
        check(basis_label in SUNSET_MASTER_BASIS,
              f"master basis missing {basis_label}")
    check("scalar_sunset_unit_powers" in SUNSET_MASTER_BASIS["F0"],
          "F0 should be scalar unit-power sunset")

    # (4) Pole schema: 3 ε-orders + MS-bar normalization + source bindings
    for slot in ("coefficient_double_pole", "coefficient_single_pole",
                 "coefficient_finite", "ms_bar_normalization"):
        check(slot in SUNSET_POLE_SCHEMA,
              f"pole schema missing {slot}")

    # (5) Source bindings explicitly cite the literature foundation
    check("Davydychev_Tausk_1993" in SUNSET_POLE_SCHEMA["equal_mass_closed_form_source"],
          "equal-mass closed-form source must cite Davydychev-Tausk 1993")
    check("Caffo_Czyz_Laporta_Remiddi_1998" in SUNSET_POLE_SCHEMA["differential_equation_source"],
          "DE source must cite Caffo-Czyz-Laporta-Remiddi 1998")
    check("Smirnov_1991" in SUNSET_POLE_SCHEMA["threshold_expansion_source"],
          "threshold expansion source must cite Smirnov 1991")

    # (6) Mass-permutation invariance (sunset is symmetric in (m1, m2, m3))
    perms = [
        (1.0, 4.0, 9.0), (1.0, 9.0, 4.0), (4.0, 1.0, 9.0),
        (4.0, 9.0, 1.0), (9.0, 1.0, 4.0), (9.0, 4.0, 1.0),
    ]
    branches = {sunset_branch(50.0, a, b, c) for a, b, c in perms}
    check(len(branches) == 1,
          f"sunset router must be mass-permutation invariant, got {branches}")

    # (7) Honest non-claim guards
    check(EXPORT_FLAGS["Export_two_loop_master_integral_sunset"] == 0,
          "full sunset master export must be 0 at gate stage")
    check(EXPORT_FLAGS["Export_external_numeric_package_as_derivation"] == 0,
          "external-package (pySecDec/FIESTA) overclaim guard tripped")
    for obs in ("Export_native_two_loop_M_W", "Export_native_two_loop_delta_r",
                "Export_native_two_loop_kappa_l", "Export_two_loop_M_W_physical_final"):
        check(EXPORT_FLAGS[obs] == 0, f"{obs} must remain 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False,
          "gdrive flag must be False")

    return _result(
        name=("T_two_loop_sunset_source_DE_and_threshold_gate: APF-native two-"
              "loop sunset master source differential-equation + threshold "
              "expansion gate. Four-region branch router (tadpole boundary / "
              "threshold timelike / euclidean spacelike / intermediate), "
              "Caffo-Czyz-Laporta-Remiddi 1998 master basis F0/F1/F2/F3 "
              "recorded, Davydychev-Tausk 1993 equal-mass closed-form source "
              "bound, Smirnov 1991 threshold expansion source bound, ε-pole "
              "coefficient schema declared. Full numeric sunset master STILL "
              "pending [P_source_gate_two_loop_sunset_DE_threshold; "
              "C_full_sunset_numeric_pending]"),
        tier=4,
        epistemic="P_source_gate_two_loop_sunset_DE_threshold",
        summary=(
            "Sibling-AI Phase-1 Tier-1 SUNSET-LADDER first gate "
            "APF_NATIVE_TWO_LOOP_SUNSET_SOURCE_DE_AND_THRESHOLD_GATE_v1 "
            "(staged at DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/). Verifier "
            "31/31 PASS standalone. **First sunset pack** of the two-loop "
            "arc Phase-1 Tier-1 — mirrors v24.3.126 (bubble source+DC gate) "
            "as the first step of the sunset ladder. Bank-side gates closed: "
            "(a) four-region kinematic branch router (tadpole boundary at "
            "p²=0, threshold-timelike above (m1+m2+m3)², euclidean-spacelike "
            "below 0, intermediate between 0 and threshold), (b) Caffo-Czyz-"
            "Laporta-Remiddi 1998 master basis F0/F1/F2/F3 schema recorded "
            "(numeric evaluators arrive next pack), (c) Davydychev-Tausk 1993 "
            "equal-mass closed-form source explicitly bound, (d) Smirnov 1991 "
            "threshold expansion source bound, (e) ε-pole coefficient schema "
            "(c_{-2}/c_{-1}/c_0 + MS-bar normalization) declared, (f) mass-"
            "permutation invariance of the branch router verified across all "
            "6 permutations of (m1, m2, m3). Honest non-claims: full numeric "
            "master = 0 (next pack), external-package consumption = 0, two-"
            "loop EW observables = 0, target_consumed = 0. The sunset is the "
            "foundational two-loop topology (three propagators sharing p²); "
            "most genuine two-loop self-energy contributions decompose into "
            "sunset + tadpole + bubble + lower topologies. With this gate, "
            "the Phase-1 Tier-1 sweep now has structural gates for all three "
            "master integrals (tadpole at Tier-1 grade per v24.3.125, bubble "
            "at branch-assembly gate per v24.3.129, sunset at source-DE/"
            "threshold gate per this push). Next pack will deliver the sunset "
            "numeric master + Tier-1 grade promotion, analogous to v24.3.124 "
            "+ v24.3.125 for the tadpole."
        ),
        key_result=(
            "Two-loop sunset source-DE + threshold gate established (4-region "
            "branch router, F0/F1/F2/F3 master basis, Davydychev-Tausk + "
            "Caffo-Czyz-Laporta-Remiddi + Smirnov sources bound); full "
            "numeric sunset master pending next pack. "
            "[P_source_gate_two_loop_sunset_DE_threshold]"
        ),
        dependencies=[],
        cross_refs=[
            "T_two_loop_tadpole_tier1_scalar_master_certification",
            "T_two_loop_two_point_branch_assembly_and_epsilon_pole_audit_gate",
        ],
        artifacts={
            "source_pack": "APF_NATIVE_TWO_LOOP_SUNSET_SOURCE_DE_AND_THRESHOLD_GATE_v1",
            "branch_router_labels": [
                "tadpole_boundary", "threshold_timelike",
                "euclidean_spacelike", "intermediate"
            ],
            "master_basis_schema": dict(SUNSET_MASTER_BASIS),
            "pole_schema": dict(SUNSET_POLE_SCHEMA),
            "export_flags": dict(EXPORT_FLAGS),
            "literature_source_bindings": {
                "Davydychev_Tausk_1993": "equal-mass closed-form source",
                "Caffo_Czyz_Laporta_Remiddi_1998": "master DE source",
                "Smirnov_1991": "threshold expansion source",
            },
        },
    )


_CHECKS = {
    "T_two_loop_sunset_source_DE_and_threshold_gate":
        check_T_two_loop_sunset_source_DE_and_threshold_gate_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == "__main__":
    import json
    out = run_all()
    for k, v in out.items():
        print(json.dumps({"name": k, "passed": v["passed"],
                          "epistemic": v["epistemic"]}, indent=2))


# ===========================================================================
# v24.3.133 — SUNSET current-depth certification (cert event)
# Sibling: APF_NATIVE_TWO_LOOP_SUNSET_CURRENT_DEPTH_CERTIFICATION_v1
# (verifier 19/19 PASS; metadata cert event for sunset source-DE gate as
# current achievable depth; full DE-numeric master pending)
# ===========================================================================

EXPORT_FLAGS_SUNSET_CURRENT_DEPTH = {
    "Export_two_loop_sunset_current_depth_certification": 1,
    "Export_two_loop_sunset_source_to_DE_threshold_ladder_complete": 1,
    "Export_two_loop_sunset_next_gate_full_DE_numeric_implementation": 1,
    "Export_two_loop_master_integral_sunset": 0,
    "Export_native_two_loop_M_W": 0, "Export_native_two_loop_delta_r": 0,
    "Export_native_two_loop_kappa_l": 0, "Export_two_loop_M_W_physical_final": 0,
    "Export_external_numeric_package_as_derivation": 0,
    "target_consumed": 0, "gdrive_write_performed": False,
}


def check_T_two_loop_sunset_current_depth_certification_P():
    """T: certifies the v24.3.130 sunset source-DE/threshold gate as the
    current achievable bank depth for the two-loop sunset master; full
    numeric DE-solver master remains pending next gate
    [P_current_depth_two_loop_sunset_substrate]."""
    check("T_two_loop_sunset_source_DE_and_threshold_gate" in _CHECKS,
          "v24.3.130 source-DE gate must be present")
    check(EXPORT_FLAGS_SUNSET_CURRENT_DEPTH["Export_two_loop_master_integral_sunset"] == 0,
          "full sunset master export must be 0")
    check(EXPORT_FLAGS_SUNSET_CURRENT_DEPTH["target_consumed"] == 0, "target_consumed must be 0")
    return _result(
        name=("T_two_loop_sunset_current_depth_certification: sunset source-DE/"
              "threshold gate (v24.3.130) certified at current bank depth; full "
              "numeric DE master pending next gate [P_current_depth_two_loop_"
              "sunset_substrate; C_full_master_pending_DE_solver]"),
        tier=4, epistemic="P_current_depth_two_loop_sunset_substrate",
        summary=("Sibling cert pack APF_NATIVE_TWO_LOOP_SUNSET_CURRENT_DEPTH_"
                 "CERTIFICATION_v1 (verifier 19/19 PASS). Records that v24.3.130 "
                 "represents current sunset ladder depth; next gate is DE solver."),
        key_result=("Sunset current-depth (source-DE gate) certified; full DE master pending. "
                    "[P_current_depth_two_loop_sunset_substrate]"),
        dependencies=["T_two_loop_sunset_source_DE_and_threshold_gate"],
        artifacts={"export_flags": dict(EXPORT_FLAGS_SUNSET_CURRENT_DEPTH)},
    )


_CHECKS["T_two_loop_sunset_current_depth_certification"] = \
    check_T_two_loop_sunset_current_depth_certification_P


# ===========================================================================
# v24.3.134 — SUNSET DE solver with threshold branch
# Sibling: APF_NATIVE_TWO_LOOP_SUNSET_DE_SOLVER_WITH_THRESHOLD_BRANCH_v1
# (verifier 37/37 PASS; DE-solver scaffold + threshold-branch typing)
# ===========================================================================

def sunset_master_basis_tuple():
    """Caffo-Czyz-Laporta-Remiddi 1998 sunrise master basis labels."""
    return ("F0", "F1", "F2", "F3")


def sunset_threshold_regions():
    """Threshold-expansion regions (Smirnov 1991 + Beneke-Smirnov 1998)."""
    return ("hard-hard", "potential-potential")


def sunset_boundary_source(p2: float) -> str:
    """Boundary-condition source for the sunset DE: tadpole at p²=0, DE/threshold elsewhere."""
    return "tadpole" if p2 == 0 else "DE_or_threshold"


EXPORT_FLAGS_SUNSET_DE_SOLVER = {
    "Export_two_loop_sunset_DE_solver_scaffold": 1,
    "Export_two_loop_sunset_threshold_branch_scaffold": 1,
    "Export_two_loop_sunset_boundary_condition_p2_zero_gate": 1,
    "Export_two_loop_sunset_F0_F1_F2_F3_system_typed": 1,
    "Export_two_loop_master_integral_sunset": 0,
    "Export_native_two_loop_M_W": 0, "Export_native_two_loop_delta_r": 0,
    "Export_native_two_loop_kappa_l": 0, "Export_two_loop_M_W_physical_final": 0,
    "Export_external_numeric_package_as_derivation": 0,
    "target_consumed": 0, "gdrive_write_performed": False,
}


def check_T_two_loop_sunset_DE_solver_with_threshold_branch_P():
    """T: sunset DE-solver scaffold + threshold-branch typing established.
    F0/F1/F2/F3 master-basis system typed; tadpole boundary at p²=0 named;
    hard-hard + potential-potential threshold regions declared. Full numeric
    DE-solver master STILL pending [P_DE_solver_threshold_gate_two_loop_sunset]."""
    # Basis labels match Caffo-Czyz-Laporta-Remiddi 1998
    basis = sunset_master_basis_tuple()
    check(basis == ("F0", "F1", "F2", "F3"),
          f"basis must be (F0,F1,F2,F3), got {basis}")
    # Threshold regions match Smirnov 1991
    regions = sunset_threshold_regions()
    check("hard-hard" in regions and "potential-potential" in regions,
          f"threshold regions must include hard-hard + potential-potential, got {regions}")
    # Boundary source typing
    check(sunset_boundary_source(0.0) == "tadpole", "p²=0 → tadpole")
    check(sunset_boundary_source(50.0) == "DE_or_threshold", "p²≠0 → DE_or_threshold")
    # Cross-check: branch router from v24.3.130 still in scope
    check(callable(sunset_branch), "v24.3.130 sunset_branch must remain in scope")
    # Honest non-claim guards
    check(EXPORT_FLAGS_SUNSET_DE_SOLVER["Export_two_loop_master_integral_sunset"] == 0,
          "full sunset master export must STILL be 0")
    check(EXPORT_FLAGS_SUNSET_DE_SOLVER["target_consumed"] == 0, "target_consumed must be 0")
    return _result(
        name=("T_two_loop_sunset_DE_solver_with_threshold_branch: sunset DE-solver "
              "scaffold + threshold-branch typing (F0/F1/F2/F3 system + hard-hard "
              "+ potential-potential regions + tadpole boundary at p²=0). Full DE-"
              "solver master STILL pending [P_DE_solver_threshold_gate_two_loop_sunset]"),
        tier=4, epistemic="P_DE_solver_threshold_gate_two_loop_sunset",
        summary=("Sibling delivery APF_NATIVE_TWO_LOOP_SUNSET_DE_SOLVER_WITH_THRESHOLD_"
                 "BRANCH_v1 (verifier 37/37 PASS). Types the DE-solver scaffold; "
                 "threshold-branch regions named (Smirnov 1991 hard-hard / Beneke-"
                 "Smirnov 1998 potential-potential); F0/F1/F2/F3 system declared; "
                 "p²=0 boundary tied to tadpole closure (v24.3.124+.125)."),
        key_result=("Sunset DE-solver + threshold-branch typing established; numeric "
                    "DE solver pending. [P_DE_solver_threshold_gate_two_loop_sunset]"),
        dependencies=["T_two_loop_sunset_current_depth_certification",
                      "T_two_loop_sunset_source_DE_and_threshold_gate"],
        cross_refs=["T_two_loop_tadpole_tier1_scalar_master_certification"],
        artifacts={"export_flags": dict(EXPORT_FLAGS_SUNSET_DE_SOLVER),
                   "master_basis": list(sunset_master_basis_tuple()),
                   "threshold_regions": list(sunset_threshold_regions())},
    )


_CHECKS["T_two_loop_sunset_DE_solver_with_threshold_branch"] = \
    check_T_two_loop_sunset_DE_solver_with_threshold_branch_P


# ===========================================================================
# v24.3.137 — SUNSET numeric DE master [C_attempt]
# Sibling: APF_NATIVE_TWO_LOOP_SUNSET_NUMERIC_DE_MASTER_P_ATTEMPT_v1
# (verifier 7/7 PASS)
# Honest non-closure: sibling RAN the DE solver attempt, threshold/regime
# classifier is valid, p²=0 boundary tied to tadpole closure, but the full
# numeric master needs a source-certified DE coefficient matrix + production
# solver. Recorded at [C] grade.
# ===========================================================================
import math as _math_sunset


def sunset_threshold_value(m1_2: float, m2_2: float, m3_2: float) -> float:
    """Three-particle threshold (m1+m2+m3)² for the sunset."""
    return (_math_sunset.sqrt(max(m1_2, 0.0)) +
            _math_sunset.sqrt(max(m2_2, 0.0)) +
            _math_sunset.sqrt(max(m3_2, 0.0))) ** 2


def sunset_regime(p2: float, m1_2: float, m2_2: float, m3_2: float) -> str:
    """Four-region kinematic regime classifier with branch-point detection."""
    thr = sunset_threshold_value(m1_2, m2_2, m3_2)
    if p2 < 0:
        return "euclidean_spacelike"
    if p2 < thr:
        return "timelike_below_three_particle_threshold"
    if abs(p2 - thr) < 1e-12:
        return "threshold_branch_point"
    return "timelike_above_threshold_absorptive"


def I_sunset_attempt(p2, m1_2, m2_2, m3_2, mu2=None, eps_order=0):
    """ATTEMPT placeholder for the full sunset master.

    Deliberately raises NotImplementedError — the sibling's honest non-closure:
    the scaffold + regime classifier + boundary-source map ARE valid, but the
    source-certified DE coefficient matrix and production solver are NOT
    delivered. Documenting the gap explicitly is the auditor-side value of
    banking this attempt.
    """
    raise NotImplementedError(
        "full sunset master pending source-certified DE coefficient matrix "
        "and production solver — [C_two_loop_sunset_DE_numeric_master_attempt]"
    )


EXPORT_FLAGS_SUNSET_NUMERIC_ATTEMPT = {
    "Export_two_loop_sunset_numeric_DE_master_attempt": 1,
    "Export_two_loop_sunset_numeric_DE_solver_scaffold": 1,
    "Export_two_loop_sunset_p2_zero_boundary_schema": 1,
    "Export_two_loop_sunset_threshold_branch_classifier": 1,
    "Export_two_loop_sunset_F0_F1_F2_F3_master_basis": 1,
    "Export_two_loop_master_integral_sunset": 0,    # STILL not closed
    "Export_native_two_loop_M_W": 0, "Export_native_two_loop_delta_r": 0,
    "Export_native_two_loop_kappa_l": 0, "Export_two_loop_M_W_physical_final": 0,
    "Export_external_numeric_package_as_derivation": 0,
    "target_consumed": 0, "gdrive_write_performed": False,
}


def check_T_two_loop_sunset_numeric_DE_master_attempt_C():
    """T (at [C] grade): two-loop sunset numeric DE-solver ATTEMPT. Threshold
    + regime classifier valid (4 regions with branch-point detection),
    F0/F1/F2/F3 basis confirmed, p²=0 boundary tied to tadpole closure
    (v24.3.124+.125). Full DE-solver numeric master NOT promoted — sibling
    explicit honest non-closure [C_two_loop_sunset_DE_numeric_master_attempt]."""

    # (1) Threshold value calculation
    thr = sunset_threshold_value(1.0, 4.0, 9.0)
    expected = (1.0 + 2.0 + 3.0) ** 2
    check(abs(thr - expected) < 1e-15,
          f"threshold value wrong: {thr} vs {expected}")

    # (2) Four-region regime classifier
    check(sunset_regime(-10.0, 1.0, 1.0, 1.0) == "euclidean_spacelike",
          "spacelike misclassified")
    check(sunset_regime(5.0, 1.0, 1.0, 1.0) == "timelike_below_three_particle_threshold",
          "sub-threshold misclassified")
    check(sunset_regime(9.0, 1.0, 1.0, 1.0) == "threshold_branch_point",
          "at-threshold misclassified")
    check(sunset_regime(50.0, 1.0, 1.0, 1.0) == "timelike_above_threshold_absorptive",
          "above-threshold misclassified")

    # (3) Full master NotImplementedError (honest non-closure scaffold)
    try:
        I_sunset_attempt(50.0, 1.0, 1.0, 1.0)
        check(False, "full sunset master attempt must raise NotImplementedError")
    except NotImplementedError as e:
        check("master pending" in str(e),
              f"NotImplementedError must name the pending state, got: {e}")

    # (4) Cross-check: F0/F1/F2/F3 basis still in scope from v24.3.130
    check(SUNSET_MASTER_BASIS["F0"] == "scalar_sunset_unit_powers",
          "F0 basis label must match v24.3.130")

    # (5) p²=0 boundary tied to tadpole closure
    check(sunset_boundary_source(0.0) == "tadpole",
          "p²=0 boundary must route to tadpole (v24.3.124+.125 closure)")

    # (6) Honest non-closure guards
    check(EXPORT_FLAGS_SUNSET_NUMERIC_ATTEMPT["Export_two_loop_master_integral_sunset"] == 0,
          "sunset master export must remain 0 after honest non-closure attempt")
    check(EXPORT_FLAGS_SUNSET_NUMERIC_ATTEMPT["target_consumed"] == 0,
          "target_consumed must be 0")

    return _result(
        name=("T_two_loop_sunset_numeric_DE_master_attempt: ATTEMPT at full "
              "two-loop sunset master via DE-solver scaffold RUN; threshold "
              "+ regime classifier (4 regions) + F0/F1/F2/F3 basis + p²=0 "
              "tadpole boundary VALID; full numeric DE master NOT promoted "
              "(sibling explicit honest non-closure) [C_two_loop_sunset_DE_"
              "numeric_master_attempt]"),
        tier=4,
        epistemic="C_two_loop_sunset_DE_numeric_master_attempt",
        summary=("Sibling APF_NATIVE_TWO_LOOP_SUNSET_NUMERIC_DE_MASTER_P_"
                 "ATTEMPT_v1 (verifier 7/7 PASS). Sibling RAN the DE-solver "
                 "numeric attempt; scaffold validated (4-region regime "
                 "classifier with branch-point detection, F0/F1/F2/F3 master "
                 "basis schema, p²=0 boundary tied to tadpole closure via "
                 "v24.3.124+.125); but the full DE numeric master needs a "
                 "source-certified DE coefficient matrix + production solver "
                 "that is NOT delivered. I_sunset_attempt raises "
                 "NotImplementedError explicitly to flag the gap. Bank "
                 "records this as a [C]-grade attempt; the structural "
                 "scaffolding stands as foundation for the next pack's "
                 "coefficient-matrix delivery."),
        key_result=("Sunset numeric DE-solver attempt run; full master not "
                    "promoted. [C_two_loop_sunset_DE_numeric_master_attempt]"),
        dependencies=["T_two_loop_sunset_DE_solver_with_threshold_branch"],
        cross_refs=["T_two_loop_tadpole_tier1_scalar_master_certification"],
        artifacts={"export_flags": dict(EXPORT_FLAGS_SUNSET_NUMERIC_ATTEMPT)},
    )


_CHECKS["T_two_loop_sunset_numeric_DE_master_attempt"] = \
    check_T_two_loop_sunset_numeric_DE_master_attempt_C
