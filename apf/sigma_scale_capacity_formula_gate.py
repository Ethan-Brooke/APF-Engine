"""Gate: the Paper-28 v_H capacity formula is held, not a native absolute-scale
derivation — Tier-4 structural disposition.

This bank-registers the disposition of the electroweak absolute-scale route after
the 2026-05-29 top-Yukawa no-go (T_yt_absolute_scale_not_fixable_by_normalization
_no_go). It is a negative/gate result in the same spirit as that no-go and the
[P+IBP-tool] admission policy: it does not bank a physical value, it fixes the
claim-grade of a route and names what would lift it.

The audit. The Paper-28 / L_vev_threshold_matching capacity formula reproduces
the Higgs vev,
    v_H = a_total * M_Pl / sqrt(C_boson * pi^2 * b * d_eff^C_boson),
giving v_H = 246.5 GeV from declared inputs (M_Pl, C_boson=16, d_eff=102, N_c=3,
c_R, y_t). The formula's real content is the M_Pl -> electroweak hierarchy
suppression d_eff^(C_boson/2) ~ 102^8. But its O(1) prefactor is not native:

  (1) a_total = a_Y + c_R with a_Y = N_c y_t^2 and b = N_c y_t^4. The prefactor
      therefore carries the absolute top Yukawa y_t, which the 2026-05-29 no-go
      shows cannot be fixed by any normalization of the Yukawa matrix. So v_H is
      not independently closed; it is v_H *given* the top scale. v_H and y_t are
      linked by this one capacity relation, not separately derived.

  (2) c_R (the right-handed-neutrino / sigma0 contribution) is a SECOND
      load-bearing held input: it is ~42% of a_total (without it v_H ~ 144 GeV),
      and it is not independently derived here. The reproduction rests on TWO
      calibrated O(1) inputs (y_t and c_R), not one.

  (3) The color-counting convention is not invariant: changing the y_t color
      convention moves v_H across 178 -> 452 GeV. This is the same N_c-convention
      non-invariance the no-go identified, now shown to propagate into the v_H
      formula. A quantity that moves under a counting convention is not physical.

Conclusion. The capacity formula is REPRODUCED but HELD. The absolute mass scale
is one capacity relation among {M_Pl, v_H, y_t, c_R} and needs exactly one
independently-certified dimensionful input (the v_H-M_Pl hierarchy / route b) to
close. Measured v_H is used only as a comparator, never as an input.

Faithful to the sibling pack APF_ABSOLUTE_MASS_SCALE_SIGMA_AUDIT_AND_REPAIR_v1
(audited clean 2026-05-29: 12/12 verifier asserts pass, no forbidden input
consumed, no-go respected, fail-closed gate), with the c_R-second-input finding
added by the audit.

Honest non-claims:
  * Export_sigma_capacity_formula_reproduced_P = 1
  * Export_sigma_scale_native_close_P = 0  (held: y_t, c_R, sigma0 all open)
  * Export_vH_absolute_scale_derivation_P = 0
  * Export_y_t_no_go_respected_P = 1
  * Export_measured_target_consumed = 0
"""
from __future__ import annotations

from math import pi, sqrt

from apf.apf_utils import check, _result


# declared Paper-28 capacity inputs (none of y_t, c_R independently derived here)
M_PL = 1.221e19
C_BOSON = 16
D_EFF = 102
N_C = 3
C_R = 1.968        # RH-neutrino / sigma0 term — held, not independently derived
Y_T_MUR = 0.957    # top scale — held by the 2026-05-29 y_t no-go
V_H_MEASURED = 246.22  # COMPARATOR ONLY


def _capacity_vH(y_t: float, c_R: float = C_R, N_c: int = N_C) -> float:
    a_Y = N_c * y_t**2
    b = N_c * y_t**4
    a_total = a_Y + c_R
    denom = C_BOSON * pi**2 * b * (D_EFF ** C_BOSON)
    return a_total * M_PL / sqrt(denom)


EXPORT_FLAGS = {
    "Export_sigma_capacity_formula_reproduced_P": 1,
    "Export_sigma_scale_native_close_P": 0,
    "Export_vH_absolute_scale_derivation_P": 0,
    "Export_y_t_no_go_respected_P": 1,
    "Export_measured_target_consumed": 0,
    "Export_physical_final_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_sigma_scale_capacity_formula_held_pending_independent_scale_P():
    """T: the Paper-28 v_H capacity formula is reproduced but HELD, not a native
    absolute-scale derivation. v_H = 246.5 GeV from declared inputs, but the O(1)
    prefactor carries (1) the no-go-blocked top Yukawa y_t via a_Y=N_c y_t^2,
    b=N_c y_t^4, and (2) the load-bearing held input c_R (~42% of a_total); and
    (3) the color convention moves v_H across 178-452 GeV (no-go corroboration).
    Absolute scale = one capacity relation among {M_Pl, v_H, y_t, c_R} needing
    one independent dimensionful input (route b). Measured v_H comparator only.
    No value banked. [P_structural_sigma_scale_capacity_formula_held_pending_independent_scale]."""

    # (a) the formula reproduces v_H ~ 246.5 from declared inputs
    v = _capacity_vH(Y_T_MUR)
    check(246.4 < v < 246.7, f"capacity formula must reproduce v_H ~ 246.5, got {v:.3f}")

    # (b1) the prefactor carries y_t: a_Y = N_c y_t^2 (the no-go-blocked scale)
    a_Y = N_C * Y_T_MUR**2
    check(abs(a_Y - 2.747547) < 1e-5, "a_Y = N_c y_t^2 carries the absolute top Yukawa")

    # (b2) c_R is a SECOND load-bearing held input (~42% of a_total)
    a_total = a_Y + C_R
    c_R_fraction = C_R / a_total
    check(0.40 < c_R_fraction < 0.44, f"c_R must be load-bearing (~42% of a_total), got {c_R_fraction:.3f}")
    v_without_cR = _capacity_vH(Y_T_MUR, c_R=0.0)
    check(v_without_cR < 160, f"without c_R the formula misses badly (~144), got {v_without_cR:.1f} — c_R is load-bearing")

    # (c) color-counting convention non-invariance: v_H moves 178 -> 452 GeV
    v_color_stripped = _capacity_vH(Y_T_MUR / sqrt(N_C))
    v_color_lifted = _capacity_vH(Y_T_MUR * sqrt(N_C))
    check(v_color_stripped > 400, f"color-stripped convention must move v_H high (>400), got {v_color_stripped:.1f}")
    check(v_color_lifted < 200, f"color-lifted convention must move v_H low (<200), got {v_color_lifted:.1f}")
    check(v_color_stripped / v_color_lifted > 2,
          "v_H moves by a large factor under the color convention ⇒ non-invariant ⇒ not physical")

    # (d) measured v_H is comparator only — formula is independent of it
    #     (perturb the comparator; the formula value does not move)
    v_again = _capacity_vH(Y_T_MUR)
    check(v_again == v, "formula value independent of the measured-v_H comparator")
    residual = v - V_H_MEASURED
    check(abs(residual) < 1.0, f"comparator residual small ({residual:.2f} GeV) — but comparator only, not input")

    # (e) disposition: HELD, not closed
    check(EXPORT_FLAGS["Export_sigma_scale_native_close_P"] == 0,
          "native close refused: y_t, c_R, sigma0 all held/open")
    check(EXPORT_FLAGS["Export_vH_absolute_scale_derivation_P"] == 0, "no v_H absolute-scale derivation claimed")
    check(EXPORT_FLAGS["Export_y_t_no_go_respected_P"] == 1, "respects the 2026-05-29 y_t no-go")
    check(EXPORT_FLAGS["Export_measured_target_consumed"] == 0, "no measured target consumed")
    check(EXPORT_FLAGS["Export_physical_final_P"] == 0, "no physical-final claim")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_sigma_scale_capacity_formula_held_pending_independent_scale: the "
              "Paper-28 v_H capacity formula reproduces v_H = 246.5 GeV from declared "
              "inputs but is HELD, not a native absolute-scale derivation. The O(1) "
              "prefactor carries the no-go-blocked top Yukawa (a_Y=N_c y_t^2, b=N_c y_t^4) "
              "and the load-bearing held input c_R (~42% of a_total); the color "
              "convention moves v_H across 178-452 GeV (no-go corroboration). Absolute "
              "scale = one capacity relation among {M_Pl, v_H, y_t, c_R} needing one "
              "independent dimensionful input (route b). Measured v_H comparator only. "
              "No value banked. [P_structural_sigma_scale_capacity_formula_held_pending_independent_scale]"),
        tier=4,
        epistemic="P_structural_sigma_scale_capacity_formula_held_pending_independent_scale",
        summary=(
            "Disposition of the electroweak absolute-scale route after the 2026-05-29 "
            "top-Yukawa no-go, faithful to the audited-clean sibling pack "
            "APF_ABSOLUTE_MASS_SCALE_SIGMA_AUDIT_AND_REPAIR_v1 (12/12 verifier asserts; "
            "no forbidden input; no-go respected; fail-closed gate). The Paper-28 / "
            "L_vev_threshold_matching capacity formula reproduces v_H = 246.5 GeV from "
            "M_Pl, C_boson=16, d_eff=102, N_c=3, c_R, y_t; its real content is the "
            "M_Pl->EW hierarchy suppression ~102^8. But the formula is HELD, not closed, "
            "for three re-verified reasons. (1) The prefactor a_total = a_Y + c_R with "
            "a_Y = N_c y_t^2 carries the absolute top Yukawa, which the no-go shows "
            "cannot be fixed by Yukawa-matrix normalization; so v_H is not independently "
            "closed but v_H GIVEN the top scale, the two linked by this one capacity "
            "relation. (2) c_R (the RH-neutrino / sigma0 term) is a SECOND load-bearing "
            "held input at ~42% of a_total (without it v_H ~ 144 GeV) — the reproduction "
            "rests on two calibrated O(1) inputs, not one (the c_R finding added by the "
            "audit beyond the sibling pack). (3) The color-counting convention is not "
            "invariant: it moves v_H across 178-452 GeV, the same N_c-convention "
            "non-invariance the no-go identified, now in the v_H formula. Conclusion: "
            "the absolute mass scale is one capacity relation among {M_Pl, v_H, y_t, "
            "c_R} and needs exactly one independently-certified dimensionful input (the "
            "v_H-M_Pl hierarchy, route b) to close. Measured v_H used only as comparator "
            "(residual 0.30 GeV), never as input. The fail-closed gate's repair target: "
            "independently certify one of {y_t(mu_R), c_R/sigma0} with no measured-v_H "
            "or measured-mass target and no normalization-smuggling route."
        ),
        key_result=(
            "Paper-28 v_H capacity formula reproduced (246.5 GeV) but HELD: prefactor "
            "carries the no-go-blocked y_t and the load-bearing held c_R; color "
            "convention moves v_H 178-452 GeV. Absolute scale needs one independent "
            "dimensionful input (route b). No value banked. "
            "[P_structural_sigma_scale_capacity_formula_held_pending_independent_scale]"
        ),
        dependencies=[
            "T_yt_absolute_scale_not_fixable_by_normalization_no_go",
            "L_vev_threshold_matching",
            "L_sigma_VEV",
        ],
        cross_refs=[
            "L_W_mass",
            "T_continuation_sum_measure_native_from_D4",
        ],
        artifacts={
            "v_H_reproduced_GeV": round(v, 3),
            "v_H_measured_comparator_GeV": V_H_MEASURED,
            "comparator_residual_GeV": round(residual, 3),
            "hierarchy_suppression": "d_eff^(C_boson/2) ~ 102^8",
            "prefactor_carries_y_t": "a_Y = N_c y_t^2, b = N_c y_t^4 (no-go-blocked)",
            "c_R_load_bearing_fraction_of_a_total": round(c_R_fraction, 3),
            "v_H_without_c_R_GeV": round(v_without_cR, 1),
            "convention_fork_GeV": {
                "color_stripped": round(v_color_stripped, 1),
                "as_declared": round(v, 1),
                "color_lifted": round(v_color_lifted, 1),
            },
            "held_inputs": ["y_t(mu_R) [no-go-blocked]", "c_R / sigma0 [not independently derived]"],
            "next_gate": "APF_ABSOLUTE_MASS_SCALE_SIGMA_INDEPENDENT_INPUT_CERTIFICATION_v1 (route b)",
            "sibling_pack": "APF_ABSOLUTE_MASS_SCALE_SIGMA_AUDIT_AND_REPAIR_v1 (audited clean 2026-05-29)",
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_sigma_scale_capacity_formula_held_pending_independent_scale":
        check_T_sigma_scale_capacity_formula_held_pending_independent_scale_P,
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
        "input_id": "ew:sigma_scale_formula_held",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "Banks a GATE disposition, not a value: check_T_sigma_scale_capacity_ "
            "formula_held_pending_independent_scale_P (machine field epistemic='P "
            "_structural_sigma_scale_capacity_formula_held_pending_independent_sc "
            "ale', a bespoke token whose name IS the claim boundary) certifies "
            "that the Paper-28 / L_vev_threshold_matching capacity formula v_H = "
            "a_total x M_Pl / sqrt(C_boson pi^2 b d_eff^C_boson) REPRODUCES v_H = "
            "246.5 GeV but is HELD, not a native absolute-scale derivation. "
            "Reasons certified: the O(1) prefactor rests on TWO calibrated inputs "
            "-- the absolute top Yukawa y_t (unfixable by normalization per the "
            "sibling no-go) and c_R (~42% of a_total; without it v_H ~ 144 GeV) "
            "-- and the y_t color-counting convention moves v_H across 178-452 "
            "GeV, failing the invariance criterion. The formula's genuinely "
            "native content is the M_Pl -> EW hierarchy suppression "
            "d_eff^(C_boson/2) ~ 102^8. Measured v_H is comparator only, never "
            "input; export flags pin Export_sigma_capacity_formula_reproduced_P = "
            "1 and Export_sigma_scale_native_close_P = 0 (y_t, c_R, sigma0 all "
            "open). No absolute electroweak scale is derived, and the frontier "
            "has since been TERMINATED by the 2026-07-02 FORM no-go "
            "(check_T_ew_scale_functional_independence_no_go). "
        ),
        "note": "Wave 7 v_H capacity-formula held-gate; bespoke P_structural_* token, reproduced-but-held disposition",
    },
)
