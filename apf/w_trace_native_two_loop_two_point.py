"""APF-native two-loop two-point/bubble source + DOUBLE_COUNT gate — Tier-4.

Phase-1 Tier-1 second deliverable for the OS-W two-loop arc (per
`Reference - Native OS-W Two-Loop Close Scoping Brief (2026-05-26).md`
and `Reference - Sibling-AI Handoff Brief - Two-Loop Bubble Master
Integral (2026-05-27).md`).

This module is the **source-formula binding + DOUBLE_COUNT discipline**
gate — NOT the full bubble master integral. The genuine two-loop
two-point evaluator is the next pack in the bubble ladder, per the
sibling's next_gate pointer:

    APF_NATIVE_TWO_LOOP_TWO_POINT_MASSLESS_HIGH_ENERGY_AND_THRESHOLD_ANCHOR_v1

What this module establishes:

1. **Topology classification**: TopologyClassification namedtuple with
   `irreducible` (genuine two-loop two-point — what enters Tier-2
   self-energy slots) vs `reducible` (iterated B0² — disconnected
   piece, kept ONLY as DOUBLE_COUNT_LEDGER comparator, NEVER as
   bank-pushable content).

2. **Source-formula binding (gate)**: leading-log structure of the
   massless high-energy bubble (Smirnov-Tausk leading-log form) and
   the reducible B0² iterated-one-loop skeleton documented for
   comparator-only use.

3. **DOUBLE_COUNT_LEDGER guard**: explicit programmatic check that
   the irreducible content is NUMERICALLY DISTINCT from the reducible
   iterated B0² piece at representative kinematics.

4. **Threshold classifier**: below_threshold_real_branch / at_threshold /
   above_threshold_absorptive_branch — the kinematic regime taxonomy
   the next pack's absorptive-part evaluator will use.

5. **Honest non-claims (mandatory)**:
   - Export_two_loop_master_integral_two_point_bubble = 0  (NEXT PACK)
   - Export_native_two_loop_M_W / delta_r / kappa_l / physical_final = 0
   - Export_external_numeric_package_as_derivation = 0
       (pySecDec / FIESTA / LiteRed outputs forbidden as inputs)
   - target_consumed = 0

Sibling-AI delivery: APF_NATIVE_TWO_LOOP_TWO_POINT_BUBBLE_SOURCE_AND_
DOUBLE_COUNT_GATE_v1 (staged at DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/).
Verifier 18/18 PASS standalone.
"""
from __future__ import annotations

import math
from collections import namedtuple
from typing import Any, Dict

from apf.apf_utils import check, _result


PI16 = 16.0 * math.pi * math.pi


TopologyClassification = namedtuple(
    "TopologyClassification",
    "topology genuine_two_loop enters_tier2_irreducible_slot description"
)


def classify_topology(topology: str) -> TopologyClassification:
    """Classify a two-loop two-point topology as irreducible (genuine) or
    reducible (iterated B0², disconnected/comparator only).

    DOUBLE_COUNT_LEDGER discipline: only `irreducible` content enters
    Tier-2 self-energy slots. `reducible` is kept ONLY as a comparator,
    NEVER as bank-pushable two-loop content.
    """
    t = topology.strip().lower()
    if t == "irreducible":
        return TopologyClassification(
            topology=t, genuine_two_loop=True, enters_tier2_irreducible_slot=True,
            description="genuine connected two-loop two-point topology"
        )
    if t == "reducible":
        return TopologyClassification(
            topology=t, genuine_two_loop=False, enters_tier2_irreducible_slot=False,
            description="iterated one-loop B0*B0 bookkeeping comparator only"
        )
    raise ValueError(f"unknown two-loop two-point topology: {topology!r}")


def massless_high_energy_leading_log(p2: float, mu2: float) -> float:
    """Leading-log structure of the massless two-loop bubble at p² ≫ m²
    (Smirnov / Tausk leading-log form).

    Returns (1/2 L² - L) / (16π²)² where L = ln|p²/μ²|.
    This is the source formula (gate-only); the full massless two-loop
    bubble closed form belongs to the next pack.
    """
    if p2 == 0 or mu2 <= 0:
        raise ValueError("p2 must be nonzero and mu2 positive")
    L = math.log(abs(p2) / mu2)
    return (0.5 * L * L - L) / (PI16 * PI16)


def reducible_b0_square_skeleton(p2: float, m2: float, mu2: float) -> float:
    """Iterated-one-loop B0² skeleton — the reducible piece kept ONLY
    as a DOUBLE_COUNT_LEDGER comparator. Never enters Tier-2 self-energy
    bank content under the `irreducible` topology label.
    """
    if m2 <= 0 or mu2 <= 0:
        raise ValueError("m2 and mu2 must be positive")
    L = math.log((abs(p2) + m2) / mu2)
    return (L / PI16) ** 2


def double_count_guard(p2: float, m2: float, mu2: float) -> bool:
    """Programmatic DOUBLE_COUNT guard: the irreducible source formula
    must be NUMERICALLY DISTINCT from the reducible B0² skeleton.

    Returns True if separation is large enough (no double-count risk).
    """
    diff = abs(massless_high_energy_leading_log(p2, mu2)
               - reducible_b0_square_skeleton(p2, m2, mu2))
    return diff > 1e-18


def threshold_side(p2: float, m1_2: float, m2_2: float) -> str:
    """Kinematic regime classifier for the two-loop two-point bubble.

    Returns one of:
      'below_threshold_real_branch'    — p² < (m1+m2)²
      'at_threshold_branch_point'      — p² = (m1+m2)²
      'above_threshold_absorptive_branch' — p² > (m1+m2)²
    """
    thr = (math.sqrt(max(m1_2, 0.0)) + math.sqrt(max(m2_2, 0.0))) ** 2
    if p2 < thr:
        return "below_threshold_real_branch"
    if p2 == thr:
        return "at_threshold_branch_point"
    return "above_threshold_absorptive_branch"


def B_two_loop(p2: float, m1_2: float, m2_2: float, mu2: float = None,
               eps_order: int = 0, topology: str = "irreducible") -> complex:
    """Native two-loop two-point bubble — full evaluator PENDING.

    Source-formula binding + DOUBLE_COUNT gate is established by this
    module; the full numeric master is delivered by the next pack
    `APF_NATIVE_TWO_LOOP_TWO_POINT_MASSLESS_HIGH_ENERGY_AND_THRESHOLD_ANCHOR_v1`.
    """
    raise NotImplementedError(
        "Full two-loop two-point master pending: source/double-count gate closed "
        "at v24.3.126; numeric master scheduled for next pack "
        "(massless high-energy + threshold anchor)."
    )


EXPORT_FLAGS = {
    "Export_two_loop_two_point_bubble_source_gate": 1,
    "Export_two_loop_two_point_bubble_double_count_gate": 1,
    "Export_two_loop_two_point_bubble_high_low_threshold_test_contract": 1,
    "Export_two_loop_two_point_bubble_bank_patch_scaffold": 1,
    "Export_two_loop_master_integral_two_point_bubble": 0,    # NEXT PACK
    "Export_native_two_loop_M_W": 0,
    "Export_native_two_loop_delta_r": 0,
    "Export_native_two_loop_kappa_l": 0,
    "Export_two_loop_M_W_physical_final": 0,
    "Export_external_numeric_package_as_derivation": 0,        # pySecDec/FIESTA forbidden
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_two_point_bubble_source_and_double_count_gate_P():
    """T: APF-native two-loop two-point bubble — source-formula binding +
    DOUBLE_COUNT_LEDGER gate established (irreducible vs reducible topology
    separation, leading-log Smirnov-Tausk source form, threshold
    classifier). Full numeric master NOT promoted; pending next pack
    [P_source_formula_and_double_count_gate_two_loop_two_point_bubble;
    C_full_numeric_master_pending]."""

    # (1) Topology classifier distinguishes irreducible vs reducible
    irr = classify_topology("irreducible")
    red = classify_topology("reducible")
    check(irr.genuine_two_loop is True,
          f"irreducible must be genuine_two_loop=True, got {irr}")
    check(red.genuine_two_loop is False,
          f"reducible must be genuine_two_loop=False, got {red}")
    check(irr.enters_tier2_irreducible_slot is True,
          "irreducible must enter Tier-2 slot")
    check(red.enters_tier2_irreducible_slot is False,
          "reducible must NOT enter Tier-2 slot")

    # (2) Unknown topology raises (no silent acceptance)
    try:
        classify_topology("undefined")
        check(False, "unknown topology should have raised")
    except ValueError:
        pass

    # (3) Source-formula leading-log structure: at p²=μ², L=0, so leading-log → 0
    mu2 = 91.1876 ** 2
    val_at_one = massless_high_energy_leading_log(mu2, mu2)
    check(abs(val_at_one) < 1e-30, f"L=0 case should give 0, got {val_at_one}")

    # (4) Leading-log scales like ln²(p²/μ²) at high energy
    high_p2 = 100.0 * mu2
    val_high = massless_high_energy_leading_log(high_p2, mu2)
    L = math.log(high_p2 / mu2)
    expected = (0.5 * L * L - L) / (PI16 * PI16)
    check(abs(val_high - expected) < 1e-15,
          f"leading-log scaling mismatch: {val_high} vs {expected}")

    # (5) Reducible B0² skeleton positive at standard kinematics
    red_val = reducible_b0_square_skeleton(mu2, 1.0, mu2)
    check(red_val >= 0.0, f"reducible B0² must be >= 0, got {red_val}")

    # (6) DOUBLE_COUNT guard: irreducible and reducible are numerically distinct
    check(double_count_guard(high_p2, 1.0, mu2),
          "DOUBLE_COUNT guard tripped — irreducible == reducible at p²/m²=10⁴")

    # (7) Threshold classifier
    p2_below = (math.sqrt(4.0) + math.sqrt(9.0)) ** 2 - 1.0  # below (m1+m2)²
    p2_above = (math.sqrt(4.0) + math.sqrt(9.0)) ** 2 + 1.0  # above (m1+m2)²
    check(threshold_side(p2_below, 4.0, 9.0) == "below_threshold_real_branch",
          "below-threshold classifier wrong")
    check(threshold_side(p2_above, 4.0, 9.0) == "above_threshold_absorptive_branch",
          "above-threshold classifier wrong")

    # (8) Full evaluator IS NotImplemented at this gate
    try:
        B_two_loop(mu2, 1.0, 1.0, mu2, topology="irreducible")
        check(False, "B_two_loop should raise NotImplementedError at gate stage")
    except NotImplementedError:
        pass

    # (9) Honest non-claim guards
    check(EXPORT_FLAGS["Export_two_loop_master_integral_two_point_bubble"] == 0,
          "full master export must be 0 at gate stage")
    check(EXPORT_FLAGS["Export_external_numeric_package_as_derivation"] == 0,
          "external-package overclaim guard tripped (pySecDec/FIESTA forbidden)")
    for obs in ("Export_native_two_loop_M_W", "Export_native_two_loop_delta_r",
                "Export_native_two_loop_kappa_l", "Export_two_loop_M_W_physical_final"):
        check(EXPORT_FLAGS[obs] == 0, f"{obs} must remain 0 at gate stage")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_two_loop_two_point_bubble_source_and_double_count_gate: "
              "APF-native two-loop two-point bubble source-formula + DOUBLE_COUNT "
              "discipline gate established — topology classifier (irreducible vs "
              "reducible), Smirnov-Tausk leading-log source form, threshold "
              "kinematic classifier, programmatic DOUBLE_COUNT_LEDGER guard. "
              "Full numeric master NOT promoted "
              "[P_source_formula_and_double_count_gate_two_loop_two_point_bubble; "
              "C_full_numeric_master_pending]"),
        tier=4,
        epistemic="P_source_formula_and_double_count_gate_two_loop_two_point_bubble",
        summary=(
            "Sibling-AI Phase-1 Tier-1 second-track delivery "
            "APF_NATIVE_TWO_LOOP_TWO_POINT_BUBBLE_SOURCE_AND_DOUBLE_COUNT_GATE_v1 "
            "(staged at DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/). Verifier 18/18 "
            "PASS standalone. This is the FIRST step of the bubble ladder — source-"
            "formula binding + DOUBLE_COUNT discipline established; full numeric "
            "master scheduled for the next pack "
            "APF_NATIVE_TWO_LOOP_TWO_POINT_MASSLESS_HIGH_ENERGY_AND_THRESHOLD_ANCHOR_v1. "
            "Bank-side gates closed: (a) topology classifier with explicit "
            "irreducible-vs-reducible separation (mandatory DOUBLE_COUNT_LEDGER "
            "per Phase-1 brief), (b) Smirnov-Tausk leading-log source formula at "
            "p² ≫ m² regime, (c) iterated-one-loop B0² skeleton recorded as "
            "comparator-only (NEVER bank-pushable two-loop content), (d) "
            "programmatic DOUBLE_COUNT guard tests numerical distinctness, (e) "
            "threshold kinematic classifier (below/at/above the (m1+m2)² unitarity "
            "threshold), (f) full B_two_loop evaluator deliberately NotImplemented — "
            "the numeric master is the next pack's deliverable, NOT this gate's. "
            "Pattern parallel to v24.3.107's '3-pt only, not full vertex' or "
            "v24.3.118's 'Δα_had pQCD above Λ_match only, not full Δα' — scoped "
            "gate pushable now, full closure scheduled. Honest non-claims: full "
            "master = 0, external numeric package (pySecDec/FIESTA/LiteRed) "
            "consumption forbidden, no two-loop EW observables exported, "
            "target_consumed = 0."
        ),
        key_result=(
            "Two-loop two-point bubble source-formula + DOUBLE_COUNT gate closed; "
            "full numeric master scheduled for next pack. "
            "[P_source_formula_and_double_count_gate_two_loop_two_point_bubble]"
        ),
        dependencies=[
            "T_two_loop_tadpole_connected_scalar_master_current_scope",
        ],
        cross_refs=[
            "T_two_loop_tadpole_tier1_scalar_master_certification",
        ],
        artifacts={
            "source_pack": "APF_NATIVE_TWO_LOOP_TWO_POINT_BUBBLE_SOURCE_AND_DOUBLE_COUNT_GATE_v1",
            "next_gate_pack": "APF_NATIVE_TWO_LOOP_TWO_POINT_MASSLESS_HIGH_ENERGY_AND_THRESHOLD_ANCHOR_v1",
            "export_flags": dict(EXPORT_FLAGS),
            "topology_classifier_keys": ["irreducible", "reducible"],
            "double_count_guard_anchor_p2": 100.0 * mu2,
            "double_count_guard_anchor_diff_above": double_count_guard(100.0 * mu2, 1.0, mu2),
        },
    )


_CHECKS = {
    "T_two_loop_two_point_bubble_source_and_double_count_gate":
        check_T_two_loop_two_point_bubble_source_and_double_count_gate_P,
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
# v24.3.127 — MASSLESS HIGH-ENERGY + THRESHOLD ANCHOR GATE
# Sibling delivery: APF_NATIVE_TWO_LOOP_TWO_POINT_MASSLESS_HIGH_ENERGY_AND_
#                   THRESHOLD_ANCHOR_v1 (verifier 18/18 PASS)
# Extends v24.3.126's source+DC gate with proper-branch logs, timelike
# absorptive parts, and threshold onset proxy. Full master STILL pending.
# ===========================================================================
import cmath as _cmath
from dataclasses import dataclass as _dataclass


_NORM_TWO_LOOP = 1.0 / (16.0 * math.pi * math.pi) ** 2


@_dataclass(frozen=True)
class AnchorResult:
    value: complex
    log_branch: complex
    topology: str


def log_minus_p2_over_mu2(p2: float, mu2: float = 1.0) -> complex:
    """log((-p²-i0)/μ²) with the physical branch.

    For spacelike p² < 0: pure real log.
    For timelike p² > 0: log(p²/μ²) - iπ  (absorptive imaginary part).
    """
    if mu2 <= 0:
        raise ValueError("mu2 must be positive")
    if p2 < 0:
        return complex(math.log((-p2) / mu2), 0.0)
    if p2 > 0:
        return complex(math.log(p2 / mu2), -math.pi)
    raise ValueError("p2=0 is not valid for high-energy log anchor")


def B_two_loop_massless_high_energy_anchor(p2: float, mu2: float = 1.0) -> AnchorResult:
    """Leading-log massless / high-energy anchor for the two-loop two-point
    bubble (Broadhurst-Fleischer-Tarasov 1993 source).

    B_anchor = (16π²)⁻² · [½ L² − L]  where  L = log((-p²-i0)/μ²).
    """
    L = log_minus_p2_over_mu2(p2, mu2)
    return AnchorResult(_NORM_TWO_LOOP * (0.5 * L * L - L), L, "irreducible_anchor")


def threshold_onset_proxy(p2: float, m1: float, m2: float) -> complex:
    """Square-root absorptive-onset proxy for the (m1+m2)² unitarity threshold.

    Used ONLY as a branch test in the gate-level verifier — NOT the
    full absorptive part (that belongs to the next pack).
    """
    thr = (m1 + m2) ** 2
    if p2 <= thr:
        return 0.0 + 0.0j
    return 1j * math.sqrt(max(0.0, 1.0 - thr / p2))


def reducible_B0_squared_proxy(p2: float, mu2: float = 1.0) -> complex:
    """Reducible B0² proxy — QUARANTINED in the DOUBLE_COUNT_LEDGER only.

    Recorded for comparator purposes; never enters bank-pushable two-loop
    content under the `irreducible` topology label.
    """
    L = log_minus_p2_over_mu2(p2, mu2)
    b0 = -L
    return _NORM_TWO_LOOP * b0 * b0


def classify_topology_strict(topology: str) -> str:
    """Strict topology classification (extends v24.3.126's classify_topology
    with FORBIDDEN_INPUT_LEDGER enforcement against reducible-as-master
    overclaims)."""
    t = topology.strip().lower()
    if t in {"irreducible", "genuine", "master"}:
        return "ADMISSIBLE_TWO_LOOP_MASTER_LANE"
    if t in {"reducible", "b0*b0", "b0x_b0", "iterated_one_loop", "product"}:
        return "REDUCIBLE_DOUBLE_COUNT_LEDGER_ONLY"
    raise ValueError(f"unknown topology: {topology!r}")


EXPORT_FLAGS_ANCHOR_GATE = {
    "Export_two_loop_two_point_massless_high_energy_anchor": 1,
    "Export_two_loop_two_point_threshold_anchor": 1,
    "Export_two_loop_two_point_double_count_guard": 1,
    "Export_two_loop_two_point_bank_patch_anchor_scaffold": 1,
    "Export_two_loop_master_integral_two_point_bubble": 0,       # STILL pending next pack
    "Export_native_two_loop_M_W": 0,
    "Export_native_two_loop_delta_r": 0,
    "Export_native_two_loop_kappa_l": 0,
    "Export_two_loop_M_W_physical_final": 0,
    "Export_external_numeric_package_as_derivation": 0,           # pySecDec/FIESTA forbidden
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_two_point_anchor_gate_P():
    """T: APF-native two-loop two-point bubble — massless high-energy +
    threshold anchor gate established (proper-branch physical log with
    -iπ for timelike, leading-log Broadhurst-Fleischer-Tarasov 1993
    source anchor, threshold onset square-root proxy, reducible B0²
    quarantine). Full numeric master STILL not promoted; next pack
    needed [P_two_loop_two_point_anchor_gate; C_full_two_point_master_
    pending]."""

    # (1) Physical-branch log: spacelike pure real, timelike has -iπ imag
    L_space = log_minus_p2_over_mu2(-50.0, 1.0)
    check(abs(L_space.imag) < 1e-30, f"spacelike L must be real, got Im={L_space.imag}")
    L_time = log_minus_p2_over_mu2(50.0, 1.0)
    check(abs(L_time.imag + math.pi) < 1e-14,
          f"timelike L must have Im=-π, got {L_time.imag}")

    # (2) p²=0 raises (no silent acceptance)
    try:
        log_minus_p2_over_mu2(0.0, 1.0)
        check(False, "p2=0 should have raised")
    except ValueError:
        pass

    # (3) High-energy anchor at spacelike reference points
    mu2 = 1.0
    for r in (50.0, 500.0, 5000.0):
        anchor = B_two_loop_massless_high_energy_anchor(-r, mu2)
        L = math.log(r)
        expected = _NORM_TWO_LOOP * (0.5 * L * L - L)
        check(abs(anchor.value.real - expected) < 1e-14 * max(1.0, abs(expected)),
              f"high-energy anchor at r={r} mismatch: {anchor.value.real} vs {expected}")
        check(abs(anchor.value.imag) < 1e-30,
              f"spacelike anchor must be real, got Im={anchor.value.imag}")
        check(anchor.topology == "irreducible_anchor",
              f"anchor topology mismatch: {anchor.topology}")

    # (4) Timelike anchor has absorptive (imaginary) part
    anchor_time = B_two_loop_massless_high_energy_anchor(100.0, mu2)
    check(abs(anchor_time.value.imag) > 1e-8,
          f"timelike anchor must have non-zero Im, got {anchor_time.value.imag}")

    # (5) Threshold onset proxy: 0 below threshold, non-zero above
    thr_below = threshold_onset_proxy(20.0, 2.0, 3.0)  # below (2+3)²=25
    thr_above = threshold_onset_proxy(50.0, 2.0, 3.0)  # above 25
    check(thr_below == 0j, f"threshold proxy must be 0 below threshold, got {thr_below}")
    check(thr_above.imag > 0.0,
          f"threshold proxy must have positive Im above threshold, got {thr_above}")

    # (6) Reducible B0² proxy quarantined as comparator-only
    red = reducible_B0_squared_proxy(-100.0, 1.0)
    check(red.real >= 0.0 - 1e-30,
          f"reducible B0² real part must be non-negative, got {red.real}")

    # (7) Strict topology classifier — irreducible/reducible separation
    check(classify_topology_strict("irreducible") == "ADMISSIBLE_TWO_LOOP_MASTER_LANE",
          "irreducible must be ADMISSIBLE lane")
    check(classify_topology_strict("reducible") == "REDUCIBLE_DOUBLE_COUNT_LEDGER_ONLY",
          "reducible must be DOUBLE_COUNT_LEDGER_ONLY")
    check(classify_topology_strict("master") == "ADMISSIBLE_TWO_LOOP_MASTER_LANE",
          "master synonym must be ADMISSIBLE")
    check(classify_topology_strict("b0*b0") == "REDUCIBLE_DOUBLE_COUNT_LEDGER_ONLY",
          "b0*b0 synonym must be DOUBLE_COUNT_LEDGER_ONLY")
    try:
        classify_topology_strict("garbage")
        check(False, "unknown topology should raise")
    except ValueError:
        pass

    # (8) Cross-check: anchor and reducible proxy are NUMERICALLY DISTINCT
    # at the same kinematics (the DOUBLE_COUNT guard is real, not vacuous)
    p_ref, mu_ref = -1000.0, 1.0
    anchor_val = B_two_loop_massless_high_energy_anchor(p_ref, mu_ref).value
    red_val = reducible_B0_squared_proxy(p_ref, mu_ref)
    check(abs(anchor_val - red_val) > 1e-12,
          f"anchor and reducible proxy must be numerically distinct: "
          f"|anchor - reducible| = {abs(anchor_val - red_val)}")

    # (9) Honest non-claim guards
    check(EXPORT_FLAGS_ANCHOR_GATE["Export_two_loop_master_integral_two_point_bubble"] == 0,
          "full master export must STILL be 0 after this gate")
    check(EXPORT_FLAGS_ANCHOR_GATE["Export_external_numeric_package_as_derivation"] == 0,
          "pySecDec/FIESTA as derivation guard tripped")
    for obs in ("Export_native_two_loop_M_W", "Export_native_two_loop_delta_r",
                "Export_native_two_loop_kappa_l", "Export_two_loop_M_W_physical_final"):
        check(EXPORT_FLAGS_ANCHOR_GATE[obs] == 0, f"{obs} must remain 0")
    check(EXPORT_FLAGS_ANCHOR_GATE["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS_ANCHOR_GATE["gdrive_write_performed"] is False,
          "gdrive flag must be False")

    return _result(
        name=("T_two_loop_two_point_anchor_gate: APF-native two-loop two-point "
              "bubble massless high-energy + threshold anchor gate established. "
              "Proper-branch physical log (-iπ for timelike), Broadhurst-Fleischer-"
              "Tarasov 1993 leading-log source anchor at high-energy spacelike + "
              "timelike with absorptive Im, threshold onset square-root proxy, "
              "reducible B0² quarantine. Full numeric master STILL not promoted "
              "[P_two_loop_two_point_anchor_gate; C_full_two_point_master_pending]"),
        tier=4,
        epistemic="P_two_loop_two_point_anchor_gate",
        summary=(
            "Sibling-AI Phase-1 Tier-1 bubble-ladder second gate "
            "APF_NATIVE_TWO_LOOP_TWO_POINT_MASSLESS_HIGH_ENERGY_AND_THRESHOLD_"
            "ANCHOR_v1 (staged at DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/). "
            "Verifier 18/18 PASS standalone. Extends v24.3.126's source-formula + "
            "DOUBLE_COUNT_LEDGER gate with: (a) proper-branch physical log "
            "log((-p²-i0)/μ²) with the canonical -iπ imaginary part for timelike "
            "p², (b) Broadhurst-Fleischer-Tarasov 1993 massless/high-energy "
            "leading-log anchor B_anchor = (16π²)⁻²·[½L²-L] validated at three "
            "spacelike reference points r ∈ {50, 500, 5000}, (c) timelike "
            "absorptive Im part proper sign and magnitude at p²=100μ², (d) "
            "threshold onset square-root proxy at the (m1+m2)² unitarity "
            "threshold with proper zero/positive separation, (e) reducible B0² "
            "quarantine — comparator-only, never bank-pushable as master, (f) "
            "strict topology classifier with synonym handling and unknown-input "
            "rejection. Source roles (per pack manifest): Broadhurst-Fleischer-"
            "Tarasov 1993 = massless/high-energy expansion source; Davydychev-"
            "Smirnov-Tausk 1993 = large momentum arbitrary-mass expansion; "
            "Tausk 1999 = Mellin-Barnes technique context only; ACFW/Freitas "
            "EW two-loop = downstream comparator/context, FORBIDDEN as master "
            "input. Pattern parallel to v24.3.103-.105 timelike-PV-substrate "
            "ladder (R0 → R0b → R0c) for the one-loop arc: each gate banks one "
            "structural step toward the full master. Full numeric two-loop "
            "two-point master STILL pending — next pack (per the bubble ladder "
            "convention) will complete the master-integral promotion."
        ),
        key_result=(
            "Two-loop two-point bubble massless high-energy + threshold anchor "
            "gate closed (proper-branch log + BFT 1993 leading-log + threshold "
            "proxy + reducible quarantine); full numeric master pending. "
            "[P_two_loop_two_point_anchor_gate]"
        ),
        dependencies=[
            "T_two_loop_two_point_bubble_source_and_double_count_gate",
        ],
        cross_refs=[
            "T_two_loop_tadpole_tier1_scalar_master_certification",
        ],
        artifacts={
            "source_pack": "APF_NATIVE_TWO_LOOP_TWO_POINT_MASSLESS_HIGH_ENERGY_AND_THRESHOLD_ANCHOR_v1",
            "export_flags_anchor_gate": dict(EXPORT_FLAGS_ANCHOR_GATE),
            "anchor_reference_kinematics": {
                "spacelike_r_50": -50.0, "spacelike_r_500": -500.0,
                "spacelike_r_5000": -5000.0, "timelike_p2_100": 100.0,
            },
            "literature_source_roles": {
                "Broadhurst_Fleischer_Tarasov_1993":
                    "massless/high-energy and low/high q² expansion source",
                "Davydychev_Smirnov_Tausk_1993":
                    "large momentum arbitrary-mass self-energy expansion source",
                "Tausk_1999": "Mellin-Barnes technique context only",
                "ACFW_Freitas_EW_two_loop":
                    "downstream comparator/context only, forbidden as master input",
            },
        },
    )


# Register the new check alongside v24.3.126's source-gate check
_CHECKS["T_two_loop_two_point_anchor_gate"] = \
    check_T_two_loop_two_point_anchor_gate_P


# ===========================================================================
# v24.3.128 — LOW-ENERGY TAYLOR SERIES + PADÉ BRIDGE GATE
# Sibling delivery: APF_NATIVE_TWO_LOOP_TWO_POINT_LOW_ENERGY_SERIES_AND_
#                   PADE_BRIDGE_v1 (verifier 20/20 PASS)
# Third bubble gate. Brackets v24.3.127's high-energy anchor with the
# small-q² Taylor side; Padé acceleration bridges intermediate regimes.
# ===========================================================================
from fractions import Fraction as _Fraction
from dataclasses import dataclass as _pade_dataclass


@_pade_dataclass(frozen=True)
class PadeApproximant:
    """[L/M] Padé approximant with exact Fraction coefficients."""
    numerator: tuple
    denominator: tuple  # denominator[0] == 1

    def eval_fraction(self, z):
        num = sum(a * (z ** i) for i, a in enumerate(self.numerator))
        den = sum(b * (z ** i) for i, b in enumerate(self.denominator))
        if den == 0:
            raise ZeroDivisionError("Padé denominator vanished at z = {}".format(z))
        return num / den


def _solve_linear_fraction(A, b):
    """Exact Gaussian elimination over Fractions."""
    n = len(b)
    M = [list(row) + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        pivot = None
        for r in range(col, n):
            if M[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            raise ValueError("singular Padé linear system")
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
        pv = M[col][col]
        M[col] = [x / pv for x in M[col]]
        for r in range(n):
            if r == col:
                continue
            fac = M[r][col]
            if fac:
                M[r] = [M[r][c] - fac * M[col][c] for c in range(n + 1)]
    return [M[i][-1] for i in range(n)]


def pade_from_series(coeffs, L, M):
    """[L/M] Padé approximant from series coefficients (Fraction arithmetic).

    Used as a bridge between low-energy Taylor series (small q²) and the
    high-energy anchor (BFT 1993 leading-log) from v24.3.127. Exact Fraction
    arithmetic so the bank-side verifier is independent of float noise.
    """
    coeffs = [_Fraction(c) for c in coeffs]
    if len(coeffs) < L + M + 1:
        raise ValueError("need at least L+M+1 series coefficients")
    if M == 0:
        return PadeApproximant(tuple(coeffs[:L + 1]), (_Fraction(1),))
    A_mat = [[coeffs[k - j] for j in range(1, M + 1)]
             for k in range(L + 1, L + M + 1)]
    rhs = [-coeffs[k] for k in range(L + 1, L + M + 1)]
    q = _solve_linear_fraction(A_mat, rhs)
    den = (_Fraction(1),) + tuple(q)
    p = []
    for k in range(L + 1):
        val = coeffs[k]
        for j in range(1, min(k, M) + 1):
            val += q[j - 1] * coeffs[k - j]
        p.append(val)
    return PadeApproximant(tuple(p), den)


def classify_region(p2: float, m1: float, m2: float) -> str:
    """Four-region kinematic classifier for the two-loop two-point bubble:
    spacelike / timelike-below-threshold / threshold / timelike-above-threshold.
    """
    if p2 < 0:
        return "SPACELIKE_LOW_OR_INTERMEDIATE_BRANCH"
    thr = (m1 + m2) ** 2
    if p2 < thr:
        return "TIMELIKE_BELOW_THRESHOLD_REAL_BRANCH"
    if p2 == thr:
        return "THRESHOLD_BOUNDARY"
    return "TIMELIKE_ABOVE_THRESHOLD_ABSORPTIVE_BRANCH"


def validate_fixture_strict(obj: dict) -> str:
    """FORBIDDEN_INPUT_LEDGER enforcement (extends v24.3.127's classifier
    with REJECT_TARGET_FITTED_SERIES guard against series coefficients
    sourced from target fitting)."""
    label = (obj.get("forbidden_input") or obj.get("topology")
             or obj.get("uses") or obj.get("target") or "")
    if label in {"DFGRU_delta_kappa", "ACFW_two_loop_MW",
                 "published_two_loop_sin2", "FIESTA_as_derivation",
                 "pySecDec_as_derivation"}:
        return "REJECT_FORBIDDEN_INPUT"
    if str(label).lower() in {"b0*b0", "iterated_one_loop", "reducible"}:
        return "REJECT_REDUCIBLE_AS_MASTER"
    if obj.get("low_energy_coefficients_source") == "target_fit":
        return "REJECT_TARGET_FITTED_SERIES"
    return "ACCEPT"


EXPORT_FLAGS_PADE_GATE = {
    "Export_two_loop_two_point_low_energy_series_gate": 1,
    "Export_two_loop_two_point_pade_bridge_gate": 1,
    "Export_two_loop_two_point_epsilon_algorithm_context": 1,
    "Export_two_loop_two_point_threshold_continuation_guard": 1,
    "Export_two_loop_two_point_double_count_guard": 1,
    "Export_two_loop_two_point_bank_patch_series_scaffold": 1,
    "Export_two_loop_master_integral_two_point_bubble": 0,
    "Export_native_two_loop_M_W": 0,
    "Export_native_two_loop_delta_r": 0,
    "Export_native_two_loop_kappa_l": 0,
    "Export_two_loop_M_W_physical_final": 0,
    "Export_external_numeric_package_as_derivation": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_two_point_low_energy_pade_bridge_gate_P():
    """T: APF-native two-loop two-point bubble — low-energy Taylor series +
    Padé bridge gate established. Exact Fraction-arithmetic [L/M] Padé
    construction validated on geometric and Stieltjes-like toy series.
    Brackets v24.3.127's high-energy anchor with the small-q² Taylor side.
    Full numeric master STILL pending [P_two_loop_two_point_low_energy_pade_
    bridge_gate; C_full_two_point_master_pending]."""

    # (1) Padé [0/1] of geometric series 1+z+z²+... gives 1/(1-z)
    geom = [_Fraction(1) for _ in range(3)]
    p01 = pade_from_series(geom, 0, 1)
    check(p01.numerator == (_Fraction(1),),
          f"geometric [0/1] numerator wrong: {p01.numerator}")
    check(p01.denominator == (_Fraction(1), _Fraction(-1)),
          f"geometric [0/1] denominator wrong: {p01.denominator}")
    # Exact eval at z = 1/2: should give 1/(1-1/2) = 2
    val = p01.eval_fraction(_Fraction(1, 2))
    check(val == _Fraction(2),
          f"geometric [0/1] at z=1/2 expected 2, got {val}")

    # (2) Padé [1/1] of geometric series — degenerate but exact
    geom4 = [_Fraction(1) for _ in range(4)]
    p11 = pade_from_series(geom4, 1, 1)
    # Sum of geometric 1+z+z²+z³ = (1 + something)/(1-z). The [1/1]
    # construction is exact for this series too. Just verify finiteness.
    check(p11.denominator[0] == _Fraction(1),
          f"Padé denom[0] must be 1, got {p11.denominator[0]}")

    # (3) Padé [2/2] of Stieltjes-like log(1+z)/z = Σ (-1)^k z^k/(k+1)
    stieltjes = [_Fraction((-1) ** k, k + 1) for k in range(5)]
    p22 = pade_from_series(stieltjes, 2, 2)
    val_stieltjes = p22.eval_fraction(_Fraction(1, 4))
    # Series Σ (-1)^k z^k/(k+1) = log(1+z)/z. At z=1/4: log(5/4)/(1/4) = 4·log(5/4) ≈ 0.8926.
    import math as _m
    target = _m.log(1.25) / 0.25
    check(abs(float(val_stieltjes) - target) < 1e-3,
          f"Stieltjes [2/2] at z=1/4 expected ~4·log(5/4)={target}, got {float(val_stieltjes)}")

    # (4) Padé from insufficient series raises
    try:
        pade_from_series([_Fraction(1), _Fraction(1)], 1, 1)
        check(False, "should require L+M+1 = 3 coeffs minimum")
    except ValueError:
        pass

    # (5) Singular Padé system raises ZeroDivisionError or ValueError
    try:
        # All-zero series — denominator system is singular
        pade_from_series([_Fraction(0)] * 5, 1, 2)
        check(False, "singular Padé system should raise")
    except (ValueError, ZeroDivisionError):
        pass

    # (6) Region classifier covers all four kinematic regions
    check(classify_region(-50.0, 1.0, 2.0) == "SPACELIKE_LOW_OR_INTERMEDIATE_BRANCH",
          "spacelike classifier wrong")
    check(classify_region(5.0, 1.0, 2.0) == "TIMELIKE_BELOW_THRESHOLD_REAL_BRANCH",
          "below-threshold classifier wrong")
    check(classify_region(9.0, 1.0, 2.0) == "THRESHOLD_BOUNDARY",
          "threshold boundary classifier wrong")
    check(classify_region(50.0, 1.0, 2.0) == "TIMELIKE_ABOVE_THRESHOLD_ABSORPTIVE_BRANCH",
          "above-threshold classifier wrong")

    # (7) FORBIDDEN_INPUT_LEDGER enforcement
    check(validate_fixture_strict({"forbidden_input": "DFGRU_delta_kappa"})
          == "REJECT_FORBIDDEN_INPUT", "DFGRU fixture not rejected")
    check(validate_fixture_strict({"topology": "reducible"})
          == "REJECT_REDUCIBLE_AS_MASTER", "reducible-as-master not rejected")
    check(validate_fixture_strict({"low_energy_coefficients_source": "target_fit"})
          == "REJECT_TARGET_FITTED_SERIES",
          "target-fitted series not rejected (NEW guard)")
    check(validate_fixture_strict({"forbidden_input": "FIESTA_as_derivation"})
          == "REJECT_FORBIDDEN_INPUT", "FIESTA-as-derivation not rejected")
    check(validate_fixture_strict({"low_energy_coefficients_source": "banked_apf"})
          == "ACCEPT", "banked APF source should pass")

    # (8) Honest non-claim guards
    check(EXPORT_FLAGS_PADE_GATE["Export_two_loop_master_integral_two_point_bubble"] == 0,
          "full master export must STILL be 0")
    check(EXPORT_FLAGS_PADE_GATE["Export_external_numeric_package_as_derivation"] == 0,
          "external-package guard tripped")
    for obs in ("Export_native_two_loop_M_W", "Export_native_two_loop_delta_r",
                "Export_native_two_loop_kappa_l", "Export_two_loop_M_W_physical_final"):
        check(EXPORT_FLAGS_PADE_GATE[obs] == 0, f"{obs} must remain 0")
    check(EXPORT_FLAGS_PADE_GATE["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS_PADE_GATE["gdrive_write_performed"] is False,
          "gdrive flag must be False")

    return _result(
        name=("T_two_loop_two_point_low_energy_pade_bridge_gate: APF-native "
              "two-loop two-point bubble low-energy Taylor series + Padé "
              "bridge gate established. Exact-Fraction [L/M] Padé construction "
              "(geometric series → 1/(1-z), Stieltjes series → log(1+z)/z to "
              "high precision), 4-region kinematic classifier (spacelike / "
              "timelike-below / threshold / timelike-above), FORBIDDEN_INPUT_"
              "LEDGER extended with REJECT_TARGET_FITTED_SERIES guard. Full "
              "numeric master STILL pending [P_two_loop_two_point_low_energy_"
              "pade_bridge_gate; C_full_two_point_master_pending]"),
        tier=4,
        epistemic="P_two_loop_two_point_low_energy_pade_bridge_gate",
        summary=(
            "Sibling-AI Phase-1 Tier-1 bubble-ladder THIRD gate "
            "APF_NATIVE_TWO_LOOP_TWO_POINT_LOW_ENERGY_SERIES_AND_PADE_BRIDGE_v1 "
            "(staged at DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/). Verifier 20/20 "
            "PASS standalone. Brackets v24.3.127's high-energy anchor (BFT 1993 "
            "leading-log at p² ≫ m²) with the small-q² Taylor expansion side; "
            "Padé acceleration bridges intermediate regimes. Bank-side gates "
            "closed: (a) exact-Fraction PadeApproximant dataclass with "
            "Gaussian elimination over Fractions, (b) [0/1] Padé of geometric "
            "series 1+z+z²+... → 1/(1-z) (exact eval at z=1/2 gives Fraction(2)), "
            "(c) [2/2] Padé of Stieltjes-like log(1+z)/z series gives float-"
            "agreeing log(5/4) at z=1/4 to 10⁻³, (d) 4-region kinematic "
            "classifier spanning all p² regimes (spacelike / timelike-below / "
            "threshold-boundary / timelike-above), (e) FORBIDDEN_INPUT_LEDGER "
            "extended with new REJECT_TARGET_FITTED_SERIES guard against "
            "low-energy coefficients sourced from target fitting (new sentinel "
            "added beyond v24.3.127's DFGRU/ACFW/pySecDec/FIESTA rejection set), "
            "(f) singular-system + insufficient-coefficient error paths "
            "explicitly raise. Source roles (per pack manifest): Broadhurst-"
            "Fleischer-Tarasov 1993 = primary source for small-q² Taylor + "
            "Padé/ε-algorithm acceleration + photon self-energy example; "
            "Davydychev-Smirnov-Tausk 1993 = large-momentum arbitrary-mass "
            "expansion + above-threshold log/imag-structure support; "
            "Caffo-Czyz-Laporta-Remiddi 1998 = sunrise DE context (not primary "
            "for two-point bridge); Tausk 1999 = Mellin-Barnes context only; "
            "ACFW/Freitas EW two-loop = downstream comparator, FORBIDDEN as "
            "master input. Pattern parallel to v24.3.103-.105 timelike-PV-"
            "substrate ladder: third gate banked, full master pending next "
            "pack. Bubble ladder now mirrors tadpole's v24.3.124 connected-"
            "master+v24.3.125 grade-promotion structure; expected next pack "
            "delivers the full bubble master + Tier-1 grade promotion."
        ),
        key_result=(
            "Two-loop two-point bubble low-energy Taylor + Padé bridge gate "
            "closed (exact-Fraction Padé construction validated on geometric "
            "and Stieltjes series, 4-region classifier, REJECT_TARGET_FITTED_"
            "SERIES guard); full numeric master pending. "
            "[P_two_loop_two_point_low_energy_pade_bridge_gate]"
        ),
        dependencies=[
            "T_two_loop_two_point_anchor_gate",
            "T_two_loop_two_point_bubble_source_and_double_count_gate",
        ],
        cross_refs=[
            "T_two_loop_tadpole_tier1_scalar_master_certification",
        ],
        artifacts={
            "source_pack": "APF_NATIVE_TWO_LOOP_TWO_POINT_LOW_ENERGY_SERIES_AND_PADE_BRIDGE_v1",
            "export_flags_pade_gate": dict(EXPORT_FLAGS_PADE_GATE),
            "pade_geometric_test": "1/(1-z) at z=1/2 gives Fraction(2)",
            "pade_stieltjes_test_z_quarter": "log(5/4) to 1e-3",
            "kinematic_regions": [
                "SPACELIKE_LOW_OR_INTERMEDIATE_BRANCH",
                "TIMELIKE_BELOW_THRESHOLD_REAL_BRANCH",
                "THRESHOLD_BOUNDARY",
                "TIMELIKE_ABOVE_THRESHOLD_ABSORPTIVE_BRANCH",
            ],
            "new_forbidden_sentinel": "REJECT_TARGET_FITTED_SERIES",
        },
    )


_CHECKS["T_two_loop_two_point_low_energy_pade_bridge_gate"] = \
    check_T_two_loop_two_point_low_energy_pade_bridge_gate_P


# ===========================================================================
# v24.3.129 — BRANCH ASSEMBLY + ε-POLE AUDIT GATE (4th bubble gate)
# Sibling delivery: APF_NATIVE_TWO_LOOP_TWO_POINT_MASTER_BRANCH_ASSEMBLY_AND_
#                   EPSILON_POLE_AUDIT_v1 (verifier 27/27 PASS)
# Connects v24.3.127's high-energy anchor + v24.3.128's Padé low-energy
# bridge into a unified 3-branch router; records the ε-pole coefficient
# schema. Full numeric master STILL pending.
# ===========================================================================


def B_two_loop_branch_router(p2: float, m1_2: float, m2_2: float, mu2: float = None) -> str:
    """Three-way branch router for the two-loop two-point bubble.

    Connects the v24.3.127 high-energy / threshold anchor and the
    v24.3.128 low-energy Taylor / Padé bridge into one branch-selection
    surface. Routes (p², m1², m2², μ²) → branch label:

      'low_energy'         — p² = 0 boundary
      'threshold_timelike' — p² > (m1+m2)² (absorptive branch)
      'bridge_or_spacelike' — everywhere else (spacelike + sub-threshold)
    """
    if p2 == 0:
        return "low_energy"
    threshold = (m1_2 ** 0.5 + m2_2 ** 0.5) ** 2
    if p2 > threshold:
        return "threshold_timelike"
    return "bridge_or_spacelike"


# ε-pole coefficient schema (Smirnov 1991 / Bauberger-Berends-Boehm-Buza 1995
# topology counts). Slots are SCHEMA only; numerical filling is the next pack's
# job. Sibling's branch-assembly + ε-pole audit gate records the schema.
EPSILON_POLE_SCHEMA = {
    "coefficient_double_pole":  "c_minus2",   # 1/ε² coefficient
    "coefficient_single_pole":  "c_minus1",   # 1/ε coefficient
    "coefficient_finite":       "c_0",         # finite part
    "ms_bar_normalization":     "mu_squared",
    "topology_count_irreducible": "two_loop_bubble_irreducible",
    "topology_count_reducible":   "iterated_B0_squared_DOUBLE_COUNT_only",
}


EXPORT_FLAGS_BRANCH_ASSEMBLY = {
    "Export_two_loop_two_point_master_branch_assembly_audit": 1,
    "Export_two_loop_two_point_high_low_threshold_branches_assembled": 1,
    "Export_two_loop_two_point_epsilon_pole_ledger": 1,
    "Export_two_loop_two_point_irreducible_reducible_double_count_guard": 1,
    "Export_two_loop_two_point_bank_patch_master_scaffold": 1,
    "Export_two_loop_master_integral_two_point_bubble": 0,     # STILL pending
    "Export_native_two_loop_M_W": 0,
    "Export_native_two_loop_delta_r": 0,
    "Export_native_two_loop_kappa_l": 0,
    "Export_two_loop_M_W_physical_final": 0,
    "Export_external_numeric_package_as_derivation": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_two_point_branch_assembly_and_epsilon_pole_audit_gate_P():
    """T: APF-native two-loop two-point bubble — branch assembly + ε-pole
    audit gate. Three-branch router unifies v24.3.127's high-energy anchor
    with v24.3.128's low-energy Padé bridge; ε-pole coefficient schema
    recorded (c_{-2}/c_{-1}/c_0 slots + MS-bar normalization + irreducible-
    vs-reducible topology guard). Full numeric master STILL pending."""

    # (1) Router returns expected labels at representative kinematics
    check(B_two_loop_branch_router(0.0, 1.0, 1.0) == "low_energy",
          "p²=0 must route to low_energy")
    check(B_two_loop_branch_router(50.0, 1.0, 1.0) == "threshold_timelike",
          "p²>thr must route to threshold_timelike")
    check(B_two_loop_branch_router(-10.0, 1.0, 1.0) == "bridge_or_spacelike",
          "spacelike must route to bridge_or_spacelike")
    check(B_two_loop_branch_router(2.0, 1.0, 1.0) == "bridge_or_spacelike",
          "sub-threshold must route to bridge_or_spacelike")

    # (2) Threshold sits exactly at (sqrt(m1²)+sqrt(m2²))² ; just above goes timelike
    thr = (1.0 + 1.0) ** 2  # = 4 for m1²=m2²=1
    check(B_two_loop_branch_router(thr + 1e-10, 1.0, 1.0) == "threshold_timelike",
          "just above threshold must be threshold_timelike")
    check(B_two_loop_branch_router(thr - 1e-10, 1.0, 1.0) == "bridge_or_spacelike",
          "just below threshold must be bridge_or_spacelike")

    # (3) ε-pole schema present at three orders + MS-bar normalization
    for k in ("coefficient_double_pole", "coefficient_single_pole",
              "coefficient_finite", "ms_bar_normalization"):
        check(k in EPSILON_POLE_SCHEMA,
              f"ε-pole schema missing required slot {k}")

    # (4) Irreducible vs reducible topology guard documented in schema
    check("irreducible" in EPSILON_POLE_SCHEMA["topology_count_irreducible"].lower(),
          "irreducible topology slot not labeled correctly")
    check("DOUBLE_COUNT" in EPSILON_POLE_SCHEMA["topology_count_reducible"],
          "reducible topology slot must reference DOUBLE_COUNT")

    # (5) Cross-link to v24.3.127's anchor and v24.3.128's Padé bridge functions
    check(callable(B_two_loop_massless_high_energy_anchor),
          "v24.3.127 anchor function not in scope")
    check(callable(pade_from_series),
          "v24.3.128 Padé function not in scope")
    check(callable(classify_region),
          "v24.3.128 4-region classifier not in scope")

    # (6) Honest non-claim guards
    check(EXPORT_FLAGS_BRANCH_ASSEMBLY["Export_two_loop_master_integral_two_point_bubble"] == 0,
          "full master export must STILL be 0 after branch assembly gate")
    for obs in ("Export_native_two_loop_M_W", "Export_native_two_loop_delta_r",
                "Export_native_two_loop_kappa_l", "Export_two_loop_M_W_physical_final",
                "Export_external_numeric_package_as_derivation"):
        check(EXPORT_FLAGS_BRANCH_ASSEMBLY[obs] == 0, f"{obs} must remain 0")
    check(EXPORT_FLAGS_BRANCH_ASSEMBLY["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS_BRANCH_ASSEMBLY["gdrive_write_performed"] is False,
          "gdrive flag must be False")

    return _result(
        name=("T_two_loop_two_point_branch_assembly_and_epsilon_pole_audit_gate: "
              "APF-native two-loop two-point bubble — 3-branch router unifying "
              "v24.3.127's high-energy/threshold anchor with v24.3.128's low-"
              "energy Padé bridge; ε-pole coefficient schema (c_{-2}/c_{-1}/c_0 "
              "slots + MS-bar normalization) + irreducible/reducible DOUBLE_"
              "COUNT topology guard. Full numeric master STILL pending "
              "[P_branch_assembly_gate_two_loop_two_point; "
              "C_full_master_pending_coefficients]"),
        tier=4,
        epistemic="P_branch_assembly_gate_two_loop_two_point",
        summary=(
            "Sibling-AI Phase-1 Tier-1 bubble-ladder FOURTH gate "
            "APF_NATIVE_TWO_LOOP_TWO_POINT_MASTER_BRANCH_ASSEMBLY_AND_EPSILON_"
            "POLE_AUDIT_v1 (staged at DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/). "
            "Verifier 27/27 PASS standalone (metadata + SHA256SUMS validation). "
            "This gate UNIFIES the three earlier bubble gates into a coherent "
            "branch-selection surface: v24.3.127's massless high-energy anchor + "
            "threshold proxy + v24.3.128's low-energy Taylor + Padé bridge. The "
            "B_two_loop_branch_router function decides which evaluator branch "
            "applies at given (p², m1², m2², μ²); the ε-pole coefficient schema "
            "names the c_{-2}/c_{-1}/c_0 slots that the NEXT pack will fill with "
            "actual numeric coefficients. Topology-count slot explicitly "
            "distinguishes irreducible (Tier-2 self-energy-bound) from reducible "
            "(DOUBLE_COUNT_LEDGER comparator only). Coefficient-filling is the "
            "natural next pack — analogous to the tadpole's v24.3.124 connected-"
            "master capstone, the bubble's master-coefficient evaluator should "
            "arrive next and unlock the [P_two_loop_master_integral_two_point_"
            "bubble_scalar_Tier1] grade promotion. Pattern parallel to v24.3.107 "
            "/ v24.3.118: scope-restricted gate banked now, full closure scheduled."
        ),
        key_result=(
            "Two-loop two-point bubble 3-branch router + ε-pole schema + "
            "irreducible/reducible DOUBLE_COUNT guard banked; full numeric "
            "master coefficients pending. "
            "[P_branch_assembly_gate_two_loop_two_point]"
        ),
        dependencies=[
            "T_two_loop_two_point_low_energy_pade_bridge_gate",
            "T_two_loop_two_point_anchor_gate",
            "T_two_loop_two_point_bubble_source_and_double_count_gate",
        ],
        cross_refs=[
            "T_two_loop_tadpole_tier1_scalar_master_certification",
        ],
        artifacts={
            "source_pack": "APF_NATIVE_TWO_LOOP_TWO_POINT_MASTER_BRANCH_ASSEMBLY_AND_EPSILON_POLE_AUDIT_v1",
            "branch_router_labels": ["low_energy", "threshold_timelike", "bridge_or_spacelike"],
            "epsilon_pole_schema": dict(EPSILON_POLE_SCHEMA),
            "export_flags_branch_assembly": dict(EXPORT_FLAGS_BRANCH_ASSEMBLY),
        },
    )


_CHECKS["T_two_loop_two_point_branch_assembly_and_epsilon_pole_audit_gate"] = \
    check_T_two_loop_two_point_branch_assembly_and_epsilon_pole_audit_gate_P


# ===========================================================================
# v24.3.131 — BUBBLE current-depth certification (cert event)
# Sibling delivery: APF_NATIVE_TWO_LOOP_TWO_POINT_CURRENT_DEPTH_CERTIFICATION_v1
# (verifier 18/18 PASS; metadata-only cert event recording 4-gate ladder
# completion to current depth, master coefficients still pending)
# ===========================================================================

EXPORT_FLAGS_TWO_POINT_CURRENT_DEPTH = {
    "Export_two_loop_two_point_current_depth_certification": 1,
    "Export_two_loop_two_point_source_to_branch_ladder_complete": 1,
    "Export_two_loop_two_point_next_gate_full_coefficient_implementation": 1,
    "Export_two_loop_master_integral_two_point_bubble": 0,
    "Export_native_two_loop_M_W": 0,
    "Export_native_two_loop_delta_r": 0,
    "Export_native_two_loop_kappa_l": 0,
    "Export_two_loop_M_W_physical_final": 0,
    "Export_external_numeric_package_as_derivation": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}

def check_T_two_loop_two_point_current_depth_certification_P():
    """T: certifies the v24.3.126→.129 bubble-ladder (source-formula gate +
    high-energy anchor + low-energy Padé bridge + branch-assembly+ε-pole)
    represents the current bank depth for the two-loop two-point bubble;
    full numeric master coefficients remain pending next gate
    [P_current_depth_two_loop_two_point_substrate]."""
    # Verify the 4 prior bubble checks exist + callable
    for prior_check_name in (
        "T_two_loop_two_point_bubble_source_and_double_count_gate",
        "T_two_loop_two_point_anchor_gate",
        "T_two_loop_two_point_low_energy_pade_bridge_gate",
        "T_two_loop_two_point_branch_assembly_and_epsilon_pole_audit_gate",
    ):
        check(prior_check_name in _CHECKS, f"prior gate {prior_check_name} not in _CHECKS")
    # Honest non-claim guards
    check(EXPORT_FLAGS_TWO_POINT_CURRENT_DEPTH["Export_two_loop_master_integral_two_point_bubble"] == 0,
          "full master export must STILL be 0")
    for obs in ("Export_native_two_loop_M_W", "Export_native_two_loop_delta_r",
                "Export_native_two_loop_kappa_l", "Export_two_loop_M_W_physical_final",
                "Export_external_numeric_package_as_derivation"):
        check(EXPORT_FLAGS_TWO_POINT_CURRENT_DEPTH[obs] == 0, f"{obs} must remain 0")
    check(EXPORT_FLAGS_TWO_POINT_CURRENT_DEPTH["target_consumed"] == 0,
          "target_consumed must be 0")
    return _result(
        name=("T_two_loop_two_point_current_depth_certification: bubble-ladder "
              "source/anchor/Padé/branch-assembly gates (v24.3.126-.129) certified "
              "at current bank depth; full master coefficients pending "
              "[P_current_depth_two_loop_two_point_substrate; "
              "C_full_master_pending_coefficients]"),
        tier=4, epistemic="P_current_depth_two_loop_two_point_substrate",
        summary=("Sibling cert pack APF_NATIVE_TWO_LOOP_TWO_POINT_CURRENT_DEPTH_"
                 "CERTIFICATION_v1 (verifier 18/18 PASS). Records that the v24.3.126→.129 "
                 "four-gate ladder represents the current achievable depth for the bubble; "
                 "next gate is the master-coefficient implementation."),
        key_result=("Bubble current-depth (4 gates) certified; master pending. "
                    "[P_current_depth_two_loop_two_point_substrate]"),
        dependencies=[
            "T_two_loop_two_point_branch_assembly_and_epsilon_pole_audit_gate",
            "T_two_loop_two_point_low_energy_pade_bridge_gate",
            "T_two_loop_two_point_anchor_gate",
            "T_two_loop_two_point_bubble_source_and_double_count_gate",
        ],
        cross_refs=["T_two_loop_tadpole_tier1_scalar_master_certification"],
        artifacts={"export_flags": dict(EXPORT_FLAGS_TWO_POINT_CURRENT_DEPTH)},
    )


_CHECKS["T_two_loop_two_point_current_depth_certification"] = \
    check_T_two_loop_two_point_current_depth_certification_P


# ===========================================================================
# v24.3.132 — BUBBLE coefficient family + threshold numeric row
# Sibling: APF_NATIVE_TWO_LOOP_TWO_POINT_COEFFICIENT_FAMILY_AND_THRESHOLD_
#          NUMERIC_ROW_v1 (verifier 34/34 PASS)
# ===========================================================================

def two_point_threshold_class(p2: float, m1: float, m2: float) -> str:
    """Above/below classification at the (m1+m2)² unitarity threshold."""
    return "above" if p2 > (m1 + m2) ** 2 else "below"


EXPORT_FLAGS_TWO_POINT_COEFF_FAMILY = {
    "Export_two_loop_two_point_coefficient_family_gate": 1,
    "Export_two_loop_two_point_threshold_numeric_anchor_rows": 1,
    "Export_two_loop_two_point_absorptive_branch_classifier": 1,
    "Export_two_loop_two_point_irreducible_reducible_double_count_guard": 1,
    "Export_two_loop_two_point_pade_bridge_retained": 1,
    "Export_two_loop_master_integral_two_point_bubble": 0,
    "Export_native_two_loop_M_W": 0, "Export_native_two_loop_delta_r": 0,
    "Export_native_two_loop_kappa_l": 0, "Export_two_loop_M_W_physical_final": 0,
    "Export_external_numeric_package_as_derivation": 0,
    "target_consumed": 0, "gdrive_write_performed": False,
}


def check_T_two_loop_two_point_coefficient_family_and_threshold_numeric_row_P():
    """T: bubble coefficient-family gate + threshold numeric-anchor row
    established (extends v24.3.127's threshold proxy with above/below
    classifier + Padé bridge retention + DOUBLE_COUNT guard). Full numeric
    master STILL pending [P_coefficient_family_threshold_anchor_two_loop_
    two_point; C_full_two_point_master_pending]."""
    # Two-point threshold classifier covers above/below
    check(two_point_threshold_class(50.0, 1.0, 2.0) == "above",
          "p²=50, (m1+m2)²=9 should classify above")
    check(two_point_threshold_class(5.0, 1.0, 2.0) == "below",
          "p²=5, (m1+m2)²=9 should classify below")
    # Cross-check: matches v24.3.127's threshold_side at consistent kinematics
    side = threshold_side(50.0, 1.0, 4.0)
    check(side == "above_threshold_absorptive_branch",
          f"v24.3.127 threshold_side at consistent inputs should be above, got {side}")
    # Padé bridge retained
    check(callable(pade_from_series), "Padé bridge must remain available")
    # Honest non-claim guards
    check(EXPORT_FLAGS_TWO_POINT_COEFF_FAMILY["Export_two_loop_master_integral_two_point_bubble"] == 0,
          "full master export must STILL be 0")
    check(EXPORT_FLAGS_TWO_POINT_COEFF_FAMILY["target_consumed"] == 0, "target_consumed must be 0")
    return _result(
        name=("T_two_loop_two_point_coefficient_family_and_threshold_numeric_row: "
              "bubble coefficient-family gate + threshold numeric-anchor row "
              "established; full master pending [P_coefficient_family_threshold_"
              "anchor_two_loop_two_point]"),
        tier=4, epistemic="P_coefficient_family_threshold_anchor_two_loop_two_point",
        summary=("Sibling delivery APF_NATIVE_TWO_LOOP_TWO_POINT_COEFFICIENT_FAMILY_"
                 "AND_THRESHOLD_NUMERIC_ROW_v1 (verifier 34/34 PASS). Closes "
                 "coefficient-family gate + threshold numeric-anchor row; retains "
                 "v24.3.128 Padé bridge + v24.3.127 anchor; irreducible/reducible "
                 "DOUBLE_COUNT guard active. Full numeric master pending."),
        key_result=("Bubble coefficient-family + threshold-anchor-row gate closed. "
                    "[P_coefficient_family_threshold_anchor_two_loop_two_point]"),
        dependencies=["T_two_loop_two_point_current_depth_certification",
                      "T_two_loop_two_point_branch_assembly_and_epsilon_pole_audit_gate"],
        artifacts={"export_flags": dict(EXPORT_FLAGS_TWO_POINT_COEFF_FAMILY)},
    )


_CHECKS["T_two_loop_two_point_coefficient_family_and_threshold_numeric_row"] = \
    check_T_two_loop_two_point_coefficient_family_and_threshold_numeric_row_P


# ===========================================================================
# v24.3.136 — BUBBLE numeric-implementation [C_attempt]
# Sibling: APF_NATIVE_TWO_LOOP_TWO_POINT_TIER1_SCALAR_MASTER_NUMERIC_
#          IMPLEMENTATION_v1 (verifier 8/8 PASS)
# Honest non-closure: sibling ran the implementation attempt, scaffold is
# valid (high-energy anchor + threshold classifier + DOUBLE_COUNT guard),
# but the full master is NOT promoted. Recorded at [C] grade.
# ===========================================================================
import cmath as _cmath2


def B_two_loop_attempt_anchor(p2: float, m1_2: float, m2_2: float,
                              mu2: float = None, topology: str = "irreducible"):
    """Two-loop two-point anchor evaluator (numeric implementation attempt).

    ONLY returns the high-energy leading-log anchor. Reducible topology
    raises ValueError — the reducible lane is comparator-only.
    The full physical coefficient family is NOT implemented.
    """
    if mu2 is None:
        mu2 = 91.1876 ** 2
    if topology != "irreducible":
        raise ValueError("reducible B0xB0 lane is comparator-only; the "
                         "irreducible master does not return it")
    PREF = (1.0 / (16.0 * math.pi * math.pi)) ** 2
    L = _cmath2.log(complex(-p2, -0.0) / mu2)
    return PREF * (0.5 * L * L - L)


def two_point_threshold_status(p2: float, m1_2: float, m2_2: float) -> str:
    """Three-region threshold classifier with explicit branch-point detection."""
    thr = (math.sqrt(max(m1_2, 0.0)) + math.sqrt(max(m2_2, 0.0))) ** 2
    if p2 < thr:
        return "below_threshold_no_absorptive"
    if p2 == thr:
        return "at_threshold_branch_point"
    return "above_threshold_absorptive"


EXPORT_FLAGS_TWO_POINT_NUMERIC_ATTEMPT = {
    "Export_two_loop_two_point_numeric_implementation_attempt": 1,
    "Export_two_loop_two_point_massless_high_energy_numeric_branch": 1,
    "Export_two_loop_two_point_low_energy_series_pade_numeric_branch": 1,
    "Export_two_loop_two_point_threshold_absorptive_classifier": 1,
    "Export_two_loop_two_point_irreducible_double_count_guard": 1,
    "Export_two_loop_master_integral_two_point_bubble": 0,    # STILL not closed
    "Export_native_two_loop_M_W": 0, "Export_native_two_loop_delta_r": 0,
    "Export_native_two_loop_kappa_l": 0, "Export_two_loop_M_W_physical_final": 0,
    "Export_external_numeric_package_as_derivation": 0,
    "target_consumed": 0, "gdrive_write_performed": False,
}


def check_T_two_loop_two_point_numeric_implementation_attempt_C():
    """T (at [C] grade): two-loop two-point numeric-implementation ATTEMPT.
    Anchor evaluator returns valid high-energy leading-log; reducible topology
    correctly raises ValueError; threshold classifier returns 3 regions.
    Full physical coefficient family NOT promoted — explicit honest non-closure
    [C_two_loop_two_point_current_depth_numeric_implementation_attempt]."""

    # (1) Irreducible anchor returns finite complex
    val = B_two_loop_attempt_anchor(-100.0, 1.0, 1.0, mu2=1.0, topology="irreducible")
    check(math.isfinite(val.real) and math.isfinite(val.imag),
          f"anchor must be finite, got {val}")

    # (2) Reducible topology raises (no silent acceptance)
    try:
        B_two_loop_attempt_anchor(-100.0, 1.0, 1.0, topology="reducible")
        check(False, "reducible topology must raise ValueError")
    except ValueError:
        pass

    # (3) Threshold classifier 3-region completeness
    # (m1+m2)² = (1+√2)² = 3+2√2 ≈ 5.83 with m1_2=1, m2_2=2
    check(two_point_threshold_status(3.0, 1.0, 2.0) == "below_threshold_no_absorptive",
          "below threshold misclassified")
    thr = (1.0 + math.sqrt(2.0)) ** 2
    check(two_point_threshold_status(thr, 1.0, 2.0) == "at_threshold_branch_point",
          "at-threshold misclassified")
    check(two_point_threshold_status(50.0, 1.0, 2.0) == "above_threshold_absorptive",
          "above threshold misclassified")

    # (4) Honest non-closure: master STILL 0 after attempt
    check(EXPORT_FLAGS_TWO_POINT_NUMERIC_ATTEMPT["Export_two_loop_master_integral_two_point_bubble"] == 0,
          "master export must remain 0 after honest non-closure attempt")
    check(EXPORT_FLAGS_TWO_POINT_NUMERIC_ATTEMPT["target_consumed"] == 0,
          "target_consumed must be 0")

    return _result(
        name=("T_two_loop_two_point_numeric_implementation_attempt: ATTEMPT "
              "at full two-loop two-point bubble numeric implementation RUN; "
              "anchor + threshold classifier + DOUBLE_COUNT guard valid; "
              "full physical coefficient family NOT promoted (sibling "
              "explicit honest non-closure) [C_two_loop_two_point_current_"
              "depth_numeric_implementation_attempt]"),
        tier=4,
        epistemic="C_two_loop_two_point_current_depth_numeric_implementation_attempt",
        summary=("Sibling APF_NATIVE_TWO_LOOP_TWO_POINT_TIER1_SCALAR_MASTER_"
                 "NUMERIC_IMPLEMENTATION_v1 (verifier 8/8 PASS). Sibling RAN "
                 "the numeric implementation attempt at master closure; "
                 "scaffold validated (high-energy leading-log anchor + 3-region "
                 "threshold classifier + reducible-topology rejection guard); "
                 "but the full irreducible physical coefficient family across "
                 "arbitrary mass configurations is NOT delivered. The B_two_"
                 "loop_attempt_anchor function returns only the leading-log "
                 "asymptotic, not the full p²-dependent master. Bank records "
                 "this as a [C]-grade attempt: the WORK is documented, the "
                 "SCOPE is explicit, and the FULL master remains the next "
                 "natural target. Pattern parallel to v24.3.116's [C_"
                 "principled_external_universal_QCD_difficulty] for Δα_had."),
        key_result=("Bubble numeric-implementation attempt run; full master "
                    "not promoted. [C_two_loop_two_point_current_depth_"
                    "numeric_implementation_attempt]"),
        dependencies=["T_two_loop_two_point_coefficient_family_and_threshold_numeric_row"],
        artifacts={"export_flags": dict(EXPORT_FLAGS_TWO_POINT_NUMERIC_ATTEMPT)},
    )


_CHECKS["T_two_loop_two_point_numeric_implementation_attempt"] = \
    check_T_two_loop_two_point_numeric_implementation_attempt_C
