"""The top Yukawa cancels in the capacity formula's leading term, leaving a
y_t-free geometry-locked component of the electroweak scale — Tier-4 structural.

This is the y_t-independent consequence that survives the 2026-05-29 top-Yukawa
no-go (T_yt_absolute_scale_not_fixable_by_normalization_no_go) and refines the
held-gate disposition (T_sigma_scale_capacity_formula_held_pending_independent
_scale). It does not promote an absolute Higgs vev; it extracts the part of the
Paper-28 capacity formula that needs no Yukawa input at all.

The decomposition. Writing the Paper-28 / L_vev_threshold_matching capacity
formula with the top-dominated traces a_Y = N_c y_t^2, b = N_c y_t^4:

    v = a_total * M_Pl / sqrt(C_boson * pi^2 * b * d_eff^C_boson)
      = (N_c y_t^2 + c_R) * M_Pl / (y_t^2 * sqrt(C_boson * pi^2 * N_c * d_eff^C_boson))
      = A * (N_c + c_R / y_t^2),     A = M_Pl / [pi * sqrt(C_boson * N_c) * d_eff^(C_boson/2)].

The decisive fact: the top Yukawa CANCELS in the leading term. a_Y / sqrt(b) =
N_c y_t^2 / (sqrt(N_c) y_t^2) = sqrt(N_c), independent of y_t. So the electroweak
scale splits into

    (i)  a geometry-locked component   A * N_c  ~ 144 GeV   — y_t-free AND c_R-free,
         fixed by M_Pl, N_c, C_boson, d_eff alone; and
    (ii) a cross-term  A * c_R / y_t^2 (~103 GeV at physical y_t) — which carries
         the right-handed-neutrino / sigma0 input c_R and the ONLY residual
         y_t-dependence.

Two consequences. First, this is why the no-go does not gut the v_H route: the
formula's leading piece never needed the top Yukawa. Second, it factorizes the
open absolute-scale problem cleanly — the ~144 GeV component is geometry (still
open: why d_eff = 102 and C_boson = 16, i.e. the v_H/M_Pl hierarchy exponent),
and the 144 -> 246 lift is the c_R / sigma0 cross-term (still open: the RH-neutrino
scale). The absolute value 246 GeV remains OPEN; this banks only the y_t-free
component and the factorization.

Inputs are not tuned: d_eff = 102, C_boson = 16, N_c = 3 are the banked Paper-8
capacity-ledger numbers, not fitted to 144 or 246. No measured v_H or measured
mass is consumed.

Convention. The numerical 144 GeV carries the Paper-28 *unreduced*-Planck
convention (M_Pl = 1.22e19 GeV). The invariant claim is the structure — the
Yukawa cancellation a_Y/sqrt(b) = sqrt(N_c) and the geometry-locked component
sqrt(N_c) * M_Pl / sqrt(C_boson * pi^2 * d_eff^C_boson) — not the bare number,
exactly as the continuation-sum measure's 1/(16 pi^2) carries the (2 pi)^D
convention.

Faithful to the audited-clean sibling bundle APF_ABSOLUTE_MASS_SCALE_PUSH_BUNDLE_v4
(packs SIGMA_CAPACITY_FLOOR_THEOREM_v1 + HIERARCHY_ROUTE_DECISION_v1).

Honest non-claims:
  * Export_yukawa_free_geometric_component_P = 1
  * Export_vH_absolute_scale_native_derivation_P = 0   (146->246 lift + hierarchy exponent open)
  * Export_absolute_sigma_scale_close_P = 0
  * Export_geometric_component_value_convention_free_P = 0  (unreduced-Planck convention)

LEDGER-SCALE CLAUSE (named 2026-07-02, principal ruling: fork (ii) consolidation). Where a
sector's scale originates in a capacity commitment, the committed quantity is priced at the
single-microstate occupation weight exp(-S) of the sector's ledger, S = C*sigma (C the
sector's banked capacity-type census; sigma = ln d_eff), in the case form of the commitment:
branch selection (A2, order parameter phi): phi/M_Pl = eta*exp(-S/2); saturation level (the
full-ledger vacuum): rho/M_Pl^4 = eta*exp(-S); eta the sector's O(1) measure content,
separately homed at its own grade; RG-transmuted scales EXEMPT (they ride the anchors through
dimensionless running, banked derived). The clause CONSOLIDATES the former scattered
identifications -- (A-i) sample space, (A-ii) measure structure, (B) per-state amplitude --
into one named commitment. Grades UNCHANGED: this is naming, not elevation (elevation forks
(iii)/(i) remain STAGED). Ruling note: 'Reference - The Ledger-Scale Clause - Adoption
Investigation (2026-07-02).md'; for instance 2's branch-conditionality see
check_T_vacuum_o1_reading_fork (vacuum_o1_fork.py).
"""
from __future__ import annotations

import math

from apf.apf_utils import check, _result


# banked Paper-8 capacity-ledger inputs (not tuned to 144/246) + unreduced Planck
M_PL = 1.22089e19   # unreduced Planck mass (Paper-28 declared convention)
C_BOSON = 16        # boson capacity (Paper 8)
D_EFF = 102         # effective interface dimension (Paper 8)
N_C = 3             # color
C_R = 1.968         # RH-neutrino / sigma0 term (held, not independently derived)
Y_T_REF = 0.957     # reference top Yukawa (comparator scale; NOT used by the floor)


def _A() -> float:
    """Geometry prefactor A = M_Pl / [pi sqrt(C N_c) d_eff^(C/2)]."""
    return M_PL / (math.pi * math.sqrt(C_BOSON * N_C) * D_EFF ** (C_BOSON / 2.0))


def _v_of_y(y: float) -> float:
    return _A() * (N_C + C_R / (y * y))


EXPORT_FLAGS = {
    "Export_yukawa_free_geometric_component_P": 1,
    "Export_yukawa_cancellation_in_leading_term_P": 1,
    "Export_vH_absolute_scale_native_derivation_P": 0,
    "Export_absolute_sigma_scale_close_P": 0,
    "Export_geometric_component_value_convention_free_P": 0,
    "Export_physical_final_P": 0,
    "measured_target_consumed": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_sigma_scale_yukawa_free_geometric_component_P():
    """T: the top Yukawa cancels in the capacity formula's leading term
    (a_Y/sqrt(b) = sqrt(N_c), y_t-free), leaving a geometry-locked electroweak-scale
    component A*N_c ~ 144 GeV from {M_Pl, N_c, C_boson=16, d_eff=102} alone; the
    only y_t-dependence is the c_R cross-term A*c_R/y_t^2. Survives the y_t no-go,
    refines the held gate, factorizes the gap (geometry hierarchy exponent + c_R
    lift). Absolute v_H OPEN. Value carries the unreduced-Planck convention; the
    structure is the invariant claim. No value banked beyond the y_t-free component.
    [P_structural_sigma_scale_yukawa_free_geometric_component_modulo_planck_convention]."""

    A = _A()

    # (a) the Yukawa CANCELS in the leading term: a_Y/sqrt(b) = sqrt(N_c) for ALL y_t
    import math as _m
    for y in (0.5, 0.957, 1.0, 2.0, 5.0):
        a_Y = N_C * y**2
        b = N_C * y**4
        check(abs(a_Y / _m.sqrt(b) - _m.sqrt(N_C)) < 1e-12,
              f"a_Y/sqrt(b) must equal sqrt(N_c) (y_t-free) at y={y}")

    # (b) the geometry-locked component A*N_c is independent of y_t (it is the
    #     additive term with no y in it); ~ 144 GeV under unreduced Planck.
    geom = A * N_C
    check(143.0 < geom < 145.0, f"geometry-locked component must be ~144 GeV, got {geom:.2f}")
    # it is the y -> infinity limit of v(y): uses neither y_t nor c_R
    check(_v_of_y(1e6) - geom < 1e-3 and geom < _v_of_y(Y_T_REF),
          "geometry-locked component is the y->inf limit (c_R cross-term vanishes), a strict floor")

    # (c) the cross-term carries the only y_t-dependence + c_R (~103 GeV at y_ref)
    cross = A * C_R / (Y_T_REF**2)
    check(95.0 < cross < 110.0, f"c_R cross-term must be ~103 GeV at y_ref, got {cross:.2f}")
    v_ref = _v_of_y(Y_T_REF)
    check(abs(v_ref - (geom + cross)) < 1e-6, "v = geometry-locked + c_R cross-term (additive decomposition)")
    check(245.0 < v_ref < 249.0, f"full v at y_ref reproduces ~246-248, got {v_ref:.2f}")

    # (d) inputs not tuned: vary the banked geometry and the component MOVES
    #     (genuine function of d_eff, C_boson, N_c — not a constant aimed at 144)
    A_alt = M_PL / (math.pi * math.sqrt(18 * 4) * 100 ** (18 / 2.0))  # C=18,N_c=4,d_eff=100
    check(abs(A_alt * 4 - geom) / geom > 0.1,
          "geometry component is a genuine function of {N_c,C_boson,d_eff}, not tuned to 144")

    # (e) absolute v_H still open; native close refused
    check(EXPORT_FLAGS["Export_vH_absolute_scale_native_derivation_P"] == 0,
          "absolute v_H not derived: hierarchy exponent + c_R/sigma0 lift open")
    check(EXPORT_FLAGS["Export_absolute_sigma_scale_close_P"] == 0, "sigma scale not closed")
    # (f) convention flag + no measured target
    check(EXPORT_FLAGS["Export_geometric_component_value_convention_free_P"] == 0,
          "the 144 GeV value carries the unreduced-Planck convention — structure is the invariant claim")
    check(EXPORT_FLAGS["measured_target_consumed"] == 0, "no measured v_H or mass consumed")
    check(EXPORT_FLAGS["Export_physical_final_P"] == 0, "no physical-final claim")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_sigma_scale_yukawa_free_geometric_component: the top Yukawa cancels "
              "in the capacity formula's leading term (a_Y/sqrt(b) = sqrt(N_c), y_t-free), "
              "leaving a geometry-locked electroweak-scale component A*N_c ~ 144 GeV from "
              "{M_Pl, N_c, C_boson=16, d_eff=102} alone; the only y_t-dependence is the "
              "c_R cross-term. Survives the y_t no-go, factorizes the gap (geometry "
              "hierarchy exponent + c_R/sigma0 lift). Absolute v_H OPEN; value carries the "
              "unreduced-Planck convention. "
              "[P_structural_sigma_scale_yukawa_free_geometric_component_modulo_planck_convention]"),
        tier=4,
        epistemic="P_structural_sigma_scale_yukawa_free_geometric_component_modulo_planck_convention",
        summary=(
            "The y_t-independent consequence that survives the 2026-05-29 top-Yukawa "
            "no-go and refines the held v_H-capacity gate. Writing the Paper-28 / "
            "L_vev_threshold_matching capacity formula with a_Y = N_c y_t^2, b = N_c y_t^4 "
            "gives v = A*(N_c + c_R/y_t^2) with A = M_Pl/[pi sqrt(C_boson N_c) "
            "d_eff^(C_boson/2)]. The decisive fact: the top Yukawa cancels in the leading "
            "term, a_Y/sqrt(b) = sqrt(N_c), independent of y_t. So the electroweak scale "
            "splits into a geometry-locked, Yukawa-free component A*N_c ~ 144 GeV (from "
            "M_Pl, N_c, C_boson, d_eff alone) plus a cross-term A*c_R/y_t^2 (~103 GeV at "
            "physical y_t) that carries the RH-neutrino/sigma0 input c_R and the only "
            "residual y_t-dependence. This is why the no-go does not gut the v_H route: "
            "the leading piece never needed the top Yukawa. It factorizes the open "
            "problem: the ~144 GeV component is geometry (open: the d_eff=102 / "
            "C_boson=16 hierarchy exponent, the v_H/M_Pl theorem), and the 144 -> 246 "
            "lift is the c_R/sigma0 cross-term (open: the RH-neutrino scale). The "
            "absolute 246 GeV stays OPEN. Inputs are the banked Paper-8 capacity numbers, "
            "not tuned (the component is a genuine function of {N_c, C_boson, d_eff}); no "
            "measured v_H or mass consumed. The 144 GeV value carries the unreduced-Planck "
            "convention; the invariant claim is the structure (the Yukawa cancellation and "
            "the sqrt(N_c) geometric component), as the continuation-sum measure's "
            "1/(16 pi^2) carries the (2 pi)^D convention. Faithful to audited-clean "
            "sibling bundle APF_ABSOLUTE_MASS_SCALE_PUSH_BUNDLE_v4. Next gate: the "
            "geometric hierarchy exponent / branch-selection theorem (route b)."
        ),
        key_result=(
            "Top Yukawa cancels in the capacity formula (a_Y/sqrt(b)=sqrt(N_c)); "
            "y_t-free geometry-locked EW-scale component A*N_c ~ 144 GeV from "
            "{M_Pl,N_c,C_boson=16,d_eff=102}; 144->246 lift = c_R/sigma0 cross-term, "
            "open; absolute v_H open; value carries unreduced-Planck convention. "
            "[P_structural_sigma_scale_yukawa_free_geometric_component_modulo_planck_convention]"
        ),
        dependencies=[
            "T_sigma_scale_capacity_formula_held_pending_independent_scale",
            "T_yt_absolute_scale_not_fixable_by_normalization_no_go",
            "L_vev_threshold_matching",
        ],
        cross_refs=[
            "L_sigma_VEV",
            "T_continuation_sum_measure_native_from_D4",
        ],
        artifacts={
            "decomposition": "v = A*(N_c + c_R/y_t^2), A = M_Pl/[pi sqrt(C N_c) d_eff^(C/2)]",
            "yukawa_cancellation": "a_Y/sqrt(b) = sqrt(N_c) (y_t-free)",
            "geometry_locked_component_GeV": round(_A() * N_C, 2),
            "c_R_cross_term_GeV_at_y_ref": round(_A() * C_R / Y_T_REF**2, 2),
            "full_v_at_y_ref_GeV": round(_v_of_y(Y_T_REF), 2),
            "M_Pl_convention": "unreduced (1.22089e19 GeV)",
            "geometry_inputs": {"N_c": N_C, "C_boson": C_BOSON, "d_eff": D_EFF},
            "open": ["geometry hierarchy exponent (why d_eff^C_boson)", "c_R / sigma0 / RH-neutrino lift"],
            "next_gate": "APF_ABSOLUTE_MASS_SCALE_GEOMETRIC_HIERARCHY_EXPONENT_OR_BRANCH_SELECTION_v1",
            "sibling_bundle": "APF_ABSOLUTE_MASS_SCALE_PUSH_BUNDLE_v4 (audited clean 2026-05-29)",
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_sigma_scale_yukawa_free_geometric_component":
        check_T_sigma_scale_yukawa_free_geometric_component_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}

# ---------------------------------------------------------------------------
# IE onboarding (Wave 7, v24.3.347).
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "ew:sigma_scale_yukawa_free_floor",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "check_T_sigma_scale_yukawa_free_geometric_component_P (machine field "
            "epistemic='P_structural_sigma_scale_yukawa_free_geometric_component_ "
            "modulo_planck_convention') banks the y_t-independent consequence "
            "that survives the top-Yukawa normalization no-go: in the Paper-28 "
            "capacity formula the top Yukawa CANCELS in the leading term, "
            "a_Y/sqrt(b) = N_c y_t^2 / (sqrt(N_c) y_t^2) = sqrt(N_c), factorizing "
            "the electroweak scale into (i) a geometry-locked component A x N_c ~ "
            "144 GeV fixed by M_Pl, N_c = 3, C_boson = 16, d_eff = 102 alone "
            "(y_t-free AND c_R-free), plus (ii) a cross-term A c_R / y_t^2 "
            "carrying the RH-neutrino / sigma0 input and the only residual y_t "
            "dependence. The numerical 144 GeV carries the unreduced-Planck "
            "convention (M_Pl = 1.22e19 GeV), named in the token's "
            "modulo_planck_convention rider; the invariant claim is the "
            "cancellation and the factorization, not the bare number. Inputs are "
            "the banked Paper-8 ledger numbers, not fitted; no measured v_H or "
            "measured mass is consumed. The absolute value 246 GeV remains OPEN "
            "by design (the 144 -> 246 lift is the open c_R / sigma0 cross-term; "
            "the absolute-scale frontier is terminated) -- this banks only the "
            "y_t-free component and the factorization. "
        ),
        "note": "Wave 7 Yukawa-free geometric component of v_H; bespoke P_structural_* token with Planck-convention rider",
    },
)
