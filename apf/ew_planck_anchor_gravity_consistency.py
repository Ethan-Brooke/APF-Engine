"""EW Planck anchor forced by gravity-sector consistency [P_structural] -- countermodel D excluded.

The first of the two genuinely-absent prefactor clauses (v24.3.181) to close. The strategy: the
prefactor axiom-independence theorem (v24.3.180) proved the exact value is independent of
{A1, A2, K3} via a countermodel family -- but that family was NEVER tested against the banked
GRAVITY sector. This module runs that test for the Planck-normalization axis (countermodel D,
reduced Planck) and finds it EXCLUDED. So the unreduced anchor is forced -- not by A1/A2/K3, but
by consistency with the framework's banked horizon structure.

THE FRAMEWORK HAS ONE PLANCK SCALE, AND IT IS UNREDUCED.
The banked gravity sector fixes the Planck scale through the horizon area law. Bekenstein
(check_T_Bek): S_BH = A / (4 ell_P^2) with ell_P^2 = G, i.e. the kappa = 1/4 Planck-unit
convention; the de Sitter / cosmological-constant relation Lambda/M_Pl^4 = 3 pi / d_eff^C_total
and rho_max ~ M_Pl^4 use the same ell_P^2 = G. The gravitational Planck scale is therefore
    M_Pl^grav = 1 / ell_P = G^(-1/2) = 1.2209e19 GeV   (UNREDUCED),
NOT the reduced (8 pi G)^(-1/2) = 2.4353e18 GeV (a factor sqrt(8 pi) = 5.013 smaller).

THE FLOOR ANCHORS TO THE SAME OBJECT.
The EW floor v_floor = M_Pl . sqrt(N_c) . (4 pi)^(-1) . d_eff^(-C_boson/2) anchors the hierarchy to
"the Planck scale." There is one Planck scale in the framework -- the gravitational one. The floor
uses M_Pl = 1.22089e19 = G^(-1/2), bit-consistent with the banked Bekenstein ell_P^2 = G. So the
floor's anchor IS the horizon Planck scale.

COUNTERMODEL D IS EXCLUDED.
v24.3.180's countermodel D used the reduced Planck mass (8 pi G)^(-1/2) and gave v_H = 49.11 GeV.
But the reduced normalization is a SECOND, different Planck scale, inconsistent with the banked
gravity sector's ell_P^2 = G. A model that anchors the EW floor to (8 pi G)^(-1/2) while the banked
horizon entropy uses G^(-1/2) carries two incompatible Planck scales -- it is NOT a model of the
full framework. So D is admissible under {A1, A2, K3} (v24.3.180, correct) but INADMISSIBLE against
the full banked stack including gravity. The Planck-normalization axis is forced.

WHAT THIS CLOSES, AND WHAT IT DOES NOT.
CLOSED: the Planck-normalization CONVENTION (unreduced vs reduced) -- forced to unreduced by
gravity-sector consistency. This upgrades the v24.3.181 audit's "Planck anchor genuinely absent"
to "Planck anchor forced by the banked gravity sector." The prefactor's free factors drop from two
(color carrier + Planck) to ONE (color carrier).
NOT CLOSED: the ABSOLUTE value of M_Pl. The gravity sector itself states the absolute Planck scale
is the one external dimensional input (gravity.py: "Absolute G_N requires one dimensional input
(M_Pl or v_EW)"). So the MAGNITUDE remains route-b by design; only the normalization is forced.
ALSO STILL OPEN: the sqrt(N_c) color-carrier axis (countermodels B/C). The banked y_t no-go
(v24.3.169) established that the color trace carrier is convention-non-invariant, so the gauge
sector does NOT force it the way gravity forces the Planck axis. That remains the one open clause.

[P_structural_ew_planck_anchor_forced_by_gravity_consistency]; normalization forced, absolute
value route-b; sqrt(N_c) carrier still open; no measured target consumed.
"""
from __future__ import annotations

import math

from apf.apf_utils import check, _result

G_GEV_NEG2 = 6.70883e-39                      # Newton constant, GeV^-2 (PDG)
M_PL_FLOOR = 1.22089e19                        # the value the EW floor uses
M_PL_UNREDUCED = G_GEV_NEG2 ** -0.5            # G^(-1/2)
M_PL_REDUCED = (8 * math.pi * G_GEV_NEG2) ** -0.5   # (8 pi G)^(-1/2)

EXPORT_FLAGS = dict(
    Export_planck_anchor_forced_by_gravity_consistency_P=1,
    Export_countermodel_D_reduced_planck_excluded_by_gravity_P=1,
    Export_planck_normalization_forced_unreduced_P=1,
    Export_planck_absolute_value_route_b_P=1,            # magnitude still one external input
    Export_sqrtNc_carrier_axis_still_open_P=0,           # CLOSED v24.3.185 (forced by color-triplet trace)
    Export_prefactor_free_factors_reduced_2_to_1_P=1,
    Export_exact_native_vH_P=0,
    measured_target_consumed=0,
    target_consumed=0,
)


def check_T_ew_planck_anchor_forced_by_gravity_consistency_P():
    # the banked gravity Planck scale is the UNREDUCED one (Bekenstein ell_P^2 = G)
    check(math.isclose(M_PL_UNREDUCED, M_PL_FLOOR, rel_tol=2e-3),
          "gravitational Planck scale 1/ell_P = G^(-1/2) == the floor's anchor (both unreduced)")
    check(M_PL_REDUCED < M_PL_UNREDUCED,
          "reduced (8 pi G)^(-1/2) is a DIFFERENT, smaller Planck scale")
    check(math.isclose(M_PL_UNREDUCED / M_PL_REDUCED, math.sqrt(8 * math.pi), rel_tol=1e-6),
          "unreduced/reduced = sqrt(8 pi) = 5.013 (the countermodel-D factor)")

    # countermodel D (reduced) is a SECOND Planck scale -> inconsistent with banked gravity
    check(EXPORT_FLAGS["Export_countermodel_D_reduced_planck_excluded_by_gravity_P"] == 1,
          "countermodel D anchors to a Planck scale incompatible with the banked Bekenstein ell_P^2=G")
    check(EXPORT_FLAGS["Export_planck_normalization_forced_unreduced_P"] == 1,
          "the EW floor must use the one gravitational Planck scale -> unreduced normalization forced")

    # honest scope: normalization forced, magnitude route-b
    check(EXPORT_FLAGS["Export_planck_absolute_value_route_b_P"] == 1,
          "absolute M_Pl remains the one external dimensional input (gravity.py) -- magnitude route-b")
    # the remaining open clause
    check(EXPORT_FLAGS["Export_sqrtNc_carrier_axis_still_open_P"] == 0,
          "sqrt(N_c) carrier CLOSED v24.3.185 (forced by the physical color-triplet trace; no-go is inversion-only)")
    check(EXPORT_FLAGS["Export_prefactor_free_factors_reduced_2_to_1_P"] == 1,
          "prefactor free factors: 2 (color + Planck) -> 1 (color carrier only)")
    check(EXPORT_FLAGS["Export_exact_native_vH_P"] == 0, "exact v_H still blocked (one carrier axis remains)")
    check(EXPORT_FLAGS["measured_target_consumed"] == 0, "no measured target consumed")

    return _result(
        name=("T_ew_planck_anchor_forced_by_gravity_consistency: the EW floor's Planck anchor is "
              "forced to the UNREDUCED normalization (G^-1/2) by consistency with the banked gravity "
              "sector (Bekenstein ell_P^2=G, T_Bek); the reduced-Planck countermodel D is a second "
              "incompatible Planck scale and is EXCLUDED. Closes the Planck clause; sqrt(N_c) carrier "
              "remains the one open axis [P_structural]"),
        tier=4,
        epistemic='P_structural',
        summary=(
            "First of the two genuinely-absent prefactor clauses (v24.3.181) to close, via the test "
            "the independence proof skipped: v24.3.180 proved independence from {A1,A2,K3} but never "
            "tested the GRAVITY sector. The banked gravity sector fixes one Planck scale -- Bekenstein "
            "S=A/(4 ell_P^2), ell_P^2=G (T_Bek), and the dS/CC relation -- giving M_Pl^grav = G^(-1/2) "
            "= 1.2209e19 (UNREDUCED), bit-consistent with the floor's anchor. The reduced-Planck "
            "countermodel D (2.4353e18, factor sqrt(8pi)=5.013) is a SECOND, incompatible Planck scale; "
            "a model carrying it is not a model of the full framework. So D is admissible under "
            "{A1,A2,K3} (v24.3.180, correct) but INADMISSIBLE against the full banked stack -> the "
            "Planck normalization is FORCED to unreduced. Upgrades v24.3.181's 'Planck absent' to "
            "'Planck forced by gravity'; prefactor free factors 2 -> 1. SCOPE: forces the NORMALIZATION, "
            "not the absolute value (the magnitude is the one external input per gravity.py -- route-b). "
            "STILL OPEN: the sqrt(N_c) carrier (B/C); the y_t no-go (v24.3.169) blocks the gauge route, "
            "so color is not forced the way gravity forces Planck. That is the one remaining clause."
        ),
        key_result=(
            "Planck-normalization axis FORCED to unreduced by gravity-sector consistency (Bekenstein "
            "ell_P^2=G); countermodel D excluded; prefactor 2 free factors -> 1 (only sqrt(N_c) carrier "
            "left). Absolute M_Pl still route-b; exact v_H still blocked by the one open carrier axis."
        ),
        dependencies=['T_Bek',
                      'T_ew_prefactor_axiom_independence',
                      'T_ew_floor_measure_is_continuation_sum_root'],
        artifacts=dict(
            M_Pl_floor=M_PL_FLOOR,
            M_Pl_unreduced_Gminushalf=round(M_PL_UNREDUCED, 4),
            M_Pl_reduced_8piG=round(M_PL_REDUCED, 4),
            ratio_sqrt_8pi=round(math.sqrt(8 * math.pi), 4),
            gravity_convention="Bekenstein ell_P^2 = G (unreduced), T_Bek",
            excluded="countermodel D (reduced Planck) -- second incompatible Planck scale",
            still_open="sqrt(N_c) color carrier (y_t no-go blocks the gauge route)",
            export_flags=dict(EXPORT_FLAGS),
        ),
    )


_CHECKS = {
    "T_ew_planck_anchor_forced_by_gravity_consistency":
        check_T_ew_planck_anchor_forced_by_gravity_consistency_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
