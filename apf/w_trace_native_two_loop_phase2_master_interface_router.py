"""APF-native two-loop Phase-2 master-interface routing + region-catalog gate — Tier-4.

Phase-2 admissibility router that consumes the Phase-1 current-depth two-loop
master-integral substrate (tadpole, sunset, two-point) and exports routing
decisions for downstream electroweak self-energy assembly. Each master-topology
request is routed to either a PROMOTED lane (banked at scoped grade) or a
GUARDED lane (with the missing branch / convention explicitly named).

The router exports an admissibility decision per request, NOT a physical
self-energy value. It exists to prevent three common overclaims:

  1. using the 2D ABW finite sunrise core as an unrestricted d=4 MSbar finite
     part (sunset_d4_msbar_guarded);
  2. using the D=4 Euclidean two-point quadrature as a timelike absorptive
     evaluator (two_point_threshold_guarded, between_threshold_guarded);
  3. using Mellin-Barnes continuation / numerics as a fully automatic massive
     physical-region production method (mb_continuation_full_automation = False).

Source-certified to the same six papers anchoring the Phase-1 substrate
(Chetyrkin 2002 tadpole; Caffo-Czyz-Laporta-Remiddi 1998 sunset DE;
Adams-Bogner-Weinzierl 2014 2D finite sunrise; Broadhurst-Fleischer-Tarasov
1993 BFT one-mass; Davydychev-Smirnov-Tausk 1993 DST high-energy two-point;
Czakon 2006 MB continuation guardrail).

Honest non-claims preserved verbatim:
  * Export_unrestricted_physical_sheet_master_router_P = 0
  * Export_automatic_massive_physical_region_MB_P = 0
  * Export_sunset_d4_all_sheets_MSbar_finite_part_P = 0
  * Export_two_point_timelike_absorptive_all_thresholds_P = 0
  * No electroweak self-energy value, Δr value, or M_W finite part.

Sibling APF_TWO_LOOP_PHASE2_MASTER_INTERFACE_AND_REGION_ROUTER_v1 via
APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v1.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

from apf.apf_utils import check, _result


# =============================================================================
# Source-certified kernel
# =============================================================================


@dataclass(frozen=True)
class RouteDecision:
    topology: str
    region: str
    evaluator: str
    status: str
    promoted: bool
    reason: str
    required_next_gate: Optional[str] = None

    def asdict(self):
        return asdict(self)


@dataclass(frozen=True)
class MBContinuationLedger:
    """Mellin-Barnes guardrail: Euclidean comparator only, never automatic production."""

    euclidean_numeric_comparator_allowed: bool = True
    physical_massive_naive_numeric_guarded: bool = True
    full_automation_claimed: bool = False
    singularity_extraction_claimed: bool = True
    comment: str = (
        "MB continuation may extract singularities and can serve as a Euclidean "
        "comparator; massive physical-region numerical MB is guarded, not promoted."
    )


def sunset_singularities(m1: float, m2: float, m3: float) -> Dict[str, float]:
    """Catalog of Minkowski-t singular points for the sunrise/sunset master."""
    if min(m1, m2, m3) <= 0:
        raise ValueError("positive masses required")
    return {
        "threshold": (m1 + m2 + m3) ** 2,
        "pseudothreshold_12_minus_3": (m1 + m2 - m3) ** 2,
        "pseudothreshold_1_minus_2_plus_3": (m1 - m2 + m3) ** 2,
        "pseudothreshold_minus_1_plus_2_plus_3": (-m1 + m2 + m3) ** 2,
        "zero_boundary": 0.0,
    }


def two_point_thresholds(m1: float, m2: float, m3: float, m4: float, m5: float
                         ) -> Dict[str, float]:
    """Physical-sheet two- and three-particle threshold catalog for the 5-line master."""
    if min(m1, m2, m3, m4, m5) <= 0:
        raise ValueError("positive masses required")
    return {
        "two_particle_14": (m1 + m4) ** 2,
        "two_particle_25": (m2 + m5) ** 2,
        "three_particle_135": (m1 + m3 + m5) ** 2,
        "three_particle_234": (m2 + m3 + m4) ** 2,
    }


def route_tadpole(*, q2: float = 0.0, scalar: bool = True, tensor_rank: int = 0
                  ) -> RouteDecision:
    """Route a tadpole request to the Phase-1 scoped scalar bank or a guarded lane."""
    if abs(q2) > 1e-15:
        return RouteDecision(
            "tadpole", "external_momentum_nonzero", "none", "GUARDED", False,
            "Phase-1 tadpole bank is q=0 scalar only.",
            "supply nonzero-q two-loop tadpole/self-energy reduction",
        )
    if not scalar or tensor_rank != 0:
        return RouteDecision(
            "tadpole", "q0_tensor_or_non_scalar", "Chetyrkin_formula_source_lane",
            "SOURCE_LEDGERED_NOT_IMPLEMENTED", False,
            "Chetyrkin source supports tensor formula, but Phase-1 implementation promoted scalar only.",
            "implement tensor projection and denominator-power test ladder",
        )
    return RouteDecision(
        "tadpole", "q0_scalar", "Chetyrkin_scoped_scalar_bank", "PROMOTED_P", True,
        "Scoped scalar Tier-1 tadpole is banked and consumable by Phase 2.",
    )


def route_sunset(p2_E: float, masses: List[float], *, want_d4_msbar: bool = False
                 ) -> RouteDecision:
    """Route a sunset request to ABW/CCLR/Clausen lanes or a guarded branch."""
    m1, m2, m3 = map(float, masses)
    if want_d4_msbar:
        return RouteDecision(
            "sunset", "d4_msbar_requested", "none", "GUARDED", False,
            "Current promoted finite core is two-dimensional plus DE matrix, not unrestricted d=4 MSbar finite part.",
            "source-certified dimensional recurrence + full d=4 finite-part boundary ledger",
        )
    if p2_E >= 0:
        if abs(p2_E) < 1e-14:
            return RouteDecision(
                "sunset", "zero_boundary", "Adams_Bogner_Weinzierl_Clausen_boundary",
                "PROMOTED_P", True,
                "p²=0 boundary lane is promoted in Phase-1 v2.",
            )
        return RouteDecision(
            "sunset", "euclidean_spacelike_regular",
            "Adams_Bogner_Weinzierl_2D_core + CCLR_DE_scaffold",
            "PROMOTED_CURRENT_DEPTH", True,
            "Euclidean finite core and DE matrix are promoted at current depth.",
        )
    t = -float(p2_E)
    sing = sunset_singularities(m1, m2, m3)
    for name, val in sing.items():
        if abs(t - val) <= 1e-10 * max(1.0, abs(val)):
            return RouteDecision(
                "sunset", f"timelike_{name}", "Caffo_DE_router_guard",
                "GUARDED_BRANCH", False,
                "Singular/threshold branch requires declared analytic continuation and branch ledger.",
                "threshold/pseudothreshold finite-part and absorptive branch tests",
            )
    return RouteDecision(
        "sunset", "timelike_off_singular", "Caffo_DE_router_guard", "GUARDED_BRANCH", False,
        "Timelike physical sheet remains guarded until branch tests close.",
        "global branch-router with independent comparators",
    )


def route_two_point(s_E: float, masses: List[float], *, one_mass_BFT: bool = False
                    ) -> RouteDecision:
    """Route a 5-line two-point request to BFT/DST/Euclidean lanes or a guarded branch."""
    if one_mass_BFT:
        return RouteDecision(
            "two_point_5line", "one_mass_small_or_large_q2",
            "BFT_hypergeometric_plus_Pade_lane", "PROMOTED_CURRENT_DEPTH", True,
            "BFT one-mass hypergeometric/Pade lane is implemented at current depth.",
        )
    if s_E >= 0:
        return RouteDecision(
            "two_point_5line", "euclidean_spacelike_regular",
            "five_line_projective_Feynman_parameter_evaluator", "PROMOTED_P", True,
            "Finite D=4 Euclidean five-line master is promoted in Phase-1 v2.",
        )
    t = -float(s_E)
    th = two_point_thresholds(*map(float, masses))
    if t > max(th.values()):
        return RouteDecision(
            "two_point_5line", "timelike_above_highest_threshold",
            "DST_large_momentum_M0M1M2_lane", "PROMOTED_CURRENT_DEPTH", True,
            "DST high-energy lane M0/M1/M2 is implemented; M3+ ledgered, not promoted.",
        )
    hits = [k for k, v in th.items() if abs(t - v) <= 1e-10 * max(1.0, abs(v))]
    if hits:
        return RouteDecision(
            "two_point_5line", "timelike_threshold_" + "+".join(hits),
            "threshold_branch_guard", "GUARDED_BRANCH", False,
            "Threshold/absorptive branch is not an all-region production evaluator.",
            "source-certified threshold expansion coefficients and branch tests",
        )
    return RouteDecision(
        "two_point_5line", "timelike_between_thresholds", "between_threshold_guard",
        "GUARDED_BRANCH", False,
        "Between-threshold physical sheet is the explicit open region.",
        "low/high/threshold matched evaluator or independent numerical comparator",
    )


@dataclass(frozen=True)
class Phase2RouterClaim:
    phase2_master_interface_router_P: int = 1
    master_integral_region_catalog_P: int = 1
    mb_continuation_guard_P: int = 1
    phase1_substrate_consumable_by_phase2: int = 1
    unrestricted_physical_sheet_master_router_P: int = 0
    automatic_massive_physical_region_MB_P: int = 0
    sunset_d4_all_sheets_MSbar_finite_part_P: int = 0
    two_point_timelike_absorptive_all_thresholds_P: int = 0


# =============================================================================
# Export flags + bank check
# =============================================================================

EXPORT_FLAGS = {
    "Export_phase2_master_interface_router_P": 1,
    "Export_master_integral_region_catalog_P": 1,
    "Export_MB_continuation_guard_P": 1,
    "Export_phase1_substrate_consumable_by_phase2": 1,
    "Export_unrestricted_physical_sheet_master_router_P": 0,
    "Export_automatic_massive_physical_region_MB_P": 0,
    "Export_sunset_d4_all_sheets_MSbar_finite_part_P": 0,
    "Export_two_point_timelike_absorptive_all_thresholds_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_phase2_master_interface_router_current_depth_P():
    """T: Phase-2 master-interface router consuming Phase-1 current-depth
    substrate. Tadpole q=0 scalar → PROMOTED; tadpole q≠0 / tensor → GUARDED;
    sunset Euclidean / p²=0 → PROMOTED; sunset d=4 MSbar / timelike →
    GUARDED; two-point Euclidean → PROMOTED; two-point timelike high-energy
    DST lane → PROMOTED; timelike threshold / between-threshold → GUARDED;
    BFT one-mass lane → PROMOTED. MB continuation guarded, never automatic.
    [P_two_loop_phase2_master_interface_router_current_depth]."""

    # (a) Claim dataclass flag set.
    claim = Phase2RouterClaim()
    check(claim.phase2_master_interface_router_P == 1, "claim router export must be 1")
    check(claim.unrestricted_physical_sheet_master_router_P == 0,
          "claim unrestricted-physical-sheet must remain 0")
    check(claim.sunset_d4_all_sheets_MSbar_finite_part_P == 0,
          "claim d=4 MSbar must remain 0")
    check(claim.two_point_timelike_absorptive_all_thresholds_P == 0,
          "claim timelike-absorptive must remain 0")

    # (b) MB continuation guardrail.
    mb = MBContinuationLedger()
    check(mb.full_automation_claimed is False, "MB full automation must be False")
    check(mb.physical_massive_naive_numeric_guarded is True,
          "MB physical massive numeric must be guarded")
    check(mb.euclidean_numeric_comparator_allowed is True,
          "MB Euclidean comparator allowed")

    # (c) Tadpole routes.
    r = route_tadpole(q2=0, scalar=True)
    check(r.promoted is True and r.evaluator == "Chetyrkin_scoped_scalar_bank",
          f"tadpole q=0 scalar: promoted={r.promoted}, eval={r.evaluator}")
    r = route_tadpole(q2=1, scalar=True)
    check(r.promoted is False and r.status == "GUARDED",
          f"tadpole q≠0: promoted={r.promoted}, status={r.status}")
    r = route_tadpole(q2=0, scalar=False, tensor_rank=1)
    check(r.promoted is False and r.status == "SOURCE_LEDGERED_NOT_IMPLEMENTED",
          f"tadpole tensor: promoted={r.promoted}, status={r.status}")

    # (d) Sunset routes.
    r = route_sunset(1.0, [1.0, 1.2, 1.4])
    check(r.promoted is True and r.region == "euclidean_spacelike_regular",
          f"sunset Euclidean: promoted={r.promoted}, region={r.region}")
    r = route_sunset(0.0, [1.0, 1.0, 1.0])
    check(r.promoted is True and r.evaluator.endswith("Clausen_boundary"),
          f"sunset p²=0: promoted={r.promoted}, eval={r.evaluator}")
    r = route_sunset(-9.0, [1.0, 1.0, 1.0])
    check(r.status == "GUARDED_BRANCH",
          f"sunset timelike threshold: status={r.status}")
    r = route_sunset(1.0, [1.0, 1.0, 1.0], want_d4_msbar=True)
    check(r.promoted is False,
          f"sunset d=4 MSbar requested: promoted={r.promoted}")

    # (e) Two-point routes.
    r = route_two_point(2.0, [1, 1, 1, 1, 1])
    check(r.promoted is True and r.region == "euclidean_spacelike_regular",
          f"two-point Euclidean: promoted={r.promoted}, region={r.region}")
    r = route_two_point(-100.0, [1, 1, 1, 1, 1])
    check(r.promoted is True and r.evaluator.startswith("DST"),
          f"two-point high-energy: promoted={r.promoted}, eval={r.evaluator}")
    r = route_two_point(-4.0, [1, 1, 1, 1, 1])
    check(r.status == "GUARDED_BRANCH",
          f"two-point timelike threshold: status={r.status}")
    r = route_two_point(-3.0, [1, 1, 1, 1, 1])
    check(r.promoted is False,
          f"two-point between-threshold: promoted={r.promoted}")
    r = route_two_point(0.2, [1, 0.5, 1.3, 1, 0.5], one_mass_BFT=True)
    check(r.promoted is True and r.evaluator.startswith("BFT"),
          f"two-point BFT one-mass: promoted={r.promoted}, eval={r.evaluator}")

    # (f) Honest non-claim flags.
    check(EXPORT_FLAGS["Export_phase2_master_interface_router_P"] == 1,
          "Phase-2 router export flag must be 1")
    check(EXPORT_FLAGS["Export_unrestricted_physical_sheet_master_router_P"] == 0,
          "unrestricted-physical-sheet must remain 0")
    check(EXPORT_FLAGS["Export_sunset_d4_all_sheets_MSbar_finite_part_P"] == 0,
          "sunset d=4 MSbar must remain 0")
    check(EXPORT_FLAGS["Export_two_point_timelike_absorptive_all_thresholds_P"] == 0,
          "two-point timelike-absorptive must remain 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False,
          "gdrive flag must be False")

    return _result(
        name=("T_two_loop_phase2_master_interface_router_current_depth: "
              "Phase-2 admissibility router over Phase-1 two-loop master substrate. "
              "Tadpole / sunset / two-point routes catalog promoted lanes vs "
              "GUARDED branches with named open gates. MB continuation guardrail: "
              "Euclidean comparator allowed, massive physical-region numeric "
              "guarded, full automation never claimed. "
              "[P_two_loop_phase2_master_interface_router_current_depth]"),
        tier=4,
        epistemic="P_two_loop_phase2_master_interface_router_current_depth",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v1 / "
            "APF_TWO_LOOP_PHASE2_MASTER_INTERFACE_AND_REGION_ROUTER_v1. "
            "Routing kernel exports per-topology RouteDecision records with "
            "(topology, region, evaluator, status, promoted, reason, "
            "required_next_gate). Three families: (a) tadpole: q=0 scalar → "
            "Chetyrkin scoped scalar bank PROMOTED; q≠0 or tensor → GUARDED "
            "with next gate named (tensor projection ladder, nonzero-q "
            "self-energy reduction); (b) sunset: Euclidean spacelike → ABW 2D "
            "core + CCLR DE scaffold PROMOTED_CURRENT_DEPTH; p²=0 → ABW Clausen "
            "boundary PROMOTED; d=4 MSbar requested → GUARDED (needs dim "
            "recurrence + finite-part boundary ledger); timelike singular / "
            "off-singular → GUARDED_BRANCH (needs branch tests); (c) two-point: "
            "Euclidean → 5-line projective evaluator PROMOTED; t>max(threshold) "
            "→ DST M0/M1/M2 lane PROMOTED_CURRENT_DEPTH; threshold / "
            "between-threshold → GUARDED_BRANCH; one-mass small/large q² → BFT "
            "hypergeometric+Padé PROMOTED. MB continuation ledger declares "
            "Euclidean comparator and singularity extraction; refuses "
            "automatic massive physical-region production. Router exports "
            "admissibility decisions, not values."
        ),
        key_result=(
            "Phase-2 master-interface routing + region-catalog gate over the "
            "Phase-1 substrate, with MB continuation guardrail. "
            "[P_two_loop_phase2_master_interface_router_current_depth]"
        ),
        dependencies=[
            "T_two_loop_tadpole_tier1_scalar_master_certification",
            "T_two_loop_sunrise_DE_matrix_source_certified",
            "T_two_loop_sunrise_2d_finite_core_and_boundary",
            "T_two_loop_two_point_BFT_DST_coefficient_family_current_depth",
            "T_two_loop_two_point_5line_euclidean_master_arbitrary_mass",
        ],
        cross_refs=[],
        artifacts={
            "source_papers": {
                "Chetyrkin_2002": "scalar tadpole formula source lane",
                "CCLR_1998": "sunset DE matrix source",
                "ABW_2014": "2D finite sunrise + p²=0 Clausen boundary",
                "BFT_1993": "one-mass two-point BFT branches + Padé",
                "DST_1993": "arbitrary-mass high-energy two-point M0/M1/M2",
                "Czakon_2006": "MB continuation guardrail (not promoted)",
            },
            "guard_count": 6,
            "promoted_lanes_count": 6,
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_phase2_master_interface_router_current_depth":
        check_T_two_loop_phase2_master_interface_router_current_depth_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}

# ---------------------------------------------------------------------------
# IE onboarding declaration (v24.3.316, Full Bank Onboarding Wave 4 -- the
# systematic sector sweep). Claim-grade structural probe; the theorems stay
# with their banked checks; verdicts inherit banked grades, routing confers
# nothing. expect_export pinned by the observed engine verdict.
# ---------------------------------------------------------------------------

IE_DECLARATIONS = (
    {
        "input_id": "wtrace:two_loop_phase2_router",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "The two-loop Phase-2 program head: the master interface router "
            "assigns each master-topology request a PROMOTED or GUARDED "
            "lane over the Phase-1 substrate "
            "[P_two_loop_phase2_master_interface_router_current_depth]. It "
            "exports an admissibility decision, NOT a self-energy value: "
            "the export flags for unrestricted physical-sheet routing, "
            "automatic MB continuation, d=4 MSbar sunset, and all-threshold "
            "timelike two-point are all 0; no Delta-r or M_W finite part is "
            "exported. "
        ),
        "covers": ("apf.w_trace_native_two_loop_tadpole", "apf.w_trace_native_two_loop_sunrise_de", "apf.w_trace_native_two_loop_sunrise_2d_finite", "apf.w_trace_native_two_loop_two_point_bft_dst", "apf.w_trace_native_two_loop_two_point_euclidean_master"),
        "note": "Wave 4 head 3: the two-loop program head; covers = its promoted-lane composition only",
    },
)
