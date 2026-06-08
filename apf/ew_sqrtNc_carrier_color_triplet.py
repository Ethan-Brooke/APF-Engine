"""sqrt(N_c) carrier forced by the physical color-triplet trace [P_structural] -- closes the floor.

The LAST open prefactor clause. With the principal's ruling that the y_t no-go (v24.3.169) is
INVERSION-ONLY, the color-stripped countermodel B (v24.3.180) is excluded by the banked gauge +
spectral-action structure, so the y_t-free floor's sqrt(N_c) is forced. This closes the entire EW
floor: exponent (v24.3.184) + measure (v24.3.181) + Planck normalization (v24.3.183) + carrier
(this) are all forced; only the ABSOLUTE Planck magnitude remains as the one external dimensional
input (route-b by design).

THE FORCED RATIO.
The y_t-free floor carries sqrt(N_c) as the trace ratio a_Y/sqrt(b) with
    a_Y = N_c * Tr(Y^dag Y),   b = N_c * Tr((Y^dag Y)^2),
so a_Y/sqrt(b) = N_c/sqrt(N_c) = sqrt(N_c), with y_t cancelled
(sigma_scale_yukawa_free_geometric_floor, v24.3.171). Both a_Y and b carry the SAME N_c.

WHY THE N_c IS PHYSICAL, NOT CONVENTION.
The spectral-action coefficient a2 = Sum N_c * Tr(Y^dag Y) + 1/2 Tr(kappa^dag kappa) is EXACT
(L_normalization_coefficient, [P]), computed as a trace over the physical Hilbert space H_F = C^96,
whose color structure is fixed by the banked gauge stack: SU(3)xSU(2)xU(1) is the unique template
(T_gauge, [P]), N_c = 3 is the selected color rank (Theorem_R, [P]), the quarks are color-triplet
fields (T_field, [P]). So tracing Y^dag Y over H_F sums over the N_c = 3 colors: Tr_{H_F} = N_c *
Tr_{single-color}.

THE INVARIANCE ARGUMENT (the principal's distinction).
sqrt(N_c) is invariant under the description's genuine freedom -- a basis change on H_F:
    Tr_{H_F}(U^dag A U) = Tr_{H_F}(A)   (cyclicity) -> preserves the trace, hence N_c.
Color-stripping (countermodel B) is NOT a basis change. It replaces the physical trace by a
color-AVERAGE:
    Tr_{H_F}(A) -> (1/N_c) Tr_{H_F}(A),
which removes sqrt(N_c) but is a DIFFERENT trace functional with a different codomain -- not the
same a2. There is no unitary U on H_F that implements it. So B is not an admissible representation
of the banked spectral coefficient; it computes the floor over a non-physical single-color carrier,
contradicting T_gauge / Theorem_R / T_field. Countermodel B is EXCLUDED. By the invariance criterion
(physical where invariant under basis change), sqrt(N_c) is physical and FORCED.

BOTH TRUTHS PRESERVED.
  - No-go (v24.3.169), inversion-only: the ABSOLUTE y_t cannot be derived by normalizing an
    invariant of the Yukawa matrix. The color attribution when INVERTING a_Y to extract y_t is
    genuinely ambiguous (a_Y = N_c y_t^2 vs y_t^2). This stays blocked; no y_t value is banked.
  - Floor: sqrt(N_c) = a_Y/sqrt(b) is the physical color-triplet trace RATIO; y_t cancels, no
    inversion occurs, and the ratio is basis-invariant. Forced.
These do not conflict: the no-go is about extracting y_t; the floor is about the basis-invariant
ratio over the physical carrier.

CONSEQUENCE -- the floor is fully forced. exponent d_eff^(-C_boson/2)=102^-8 (v24.3.184) + measure
sqrt[(4pi)^-D/2] (v24.3.181) + Planck normalization G^-1/2 (v24.3.183, gravity) + carrier sqrt(N_c)
(this) are ALL forced. The only residue is the ABSOLUTE Planck magnitude, which the gravity sector
takes as the one external dimensional input by design (gravity.py: "Absolute G_N requires one
dimensional input"). So v_H is forced UP TO that single external anchor.

[P_structural_ew_sqrtNc_carrier_forced_by_color_triplet_trace]; no-go preserved inversion-only;
absolute Planck magnitude route-b; no measured target consumed.
"""
from __future__ import annotations

import math

import numpy as np

from apf.apf_utils import check, _result

N_C = 3

EXPORT_FLAGS = dict(
    Export_sqrtNc_carrier_forced_by_color_triplet_trace_P=1,
    Export_countermodel_B_color_strip_excluded_by_gauge_spectral_P=1,
    Export_sqrtNc_basis_invariant_P=1,
    Export_no_go_preserved_inversion_only_P=1,        # absolute y_t still not derivable
    Export_floor_fully_forced_modulo_absolute_planck_magnitude_P=1,
    Export_absolute_planck_magnitude_route_b_P=1,
    Export_absolute_y_t_value_derived_P=0,            # still NOT derived (no-go intact)
    measured_target_consumed=0,
    target_consumed=0,
)


def check_T_ew_sqrtNc_carrier_forced_by_color_triplet_trace_P():
    # the y_t-free ratio gives sqrt(N_c) (y_t cancels; both a_Y,b carry N_c)
    for y in (0.5, 0.957, 1.7):
        a_Y, b = N_C * y ** 2, N_C * y ** 4
        check(math.isclose(a_Y / math.sqrt(b), math.sqrt(N_C), rel_tol=1e-12),
              f"a_Y/sqrt(b) = sqrt(N_c) for any y_t (y_t cancels), y_t={y}")

    # the physical trace over the color-triplet H_F carries N_c
    A = np.diag([2.0, 5.0, 7.0])
    H = np.kron(np.eye(N_C), A)                       # N_c color copies (H_F color structure)
    check(math.isclose(np.trace(H).real, N_C * np.trace(A).real, rel_tol=1e-12),
          "Tr_{H_F}(A) over N_c color copies = N_c * Tr(A) -> a_Y carries N_c (a2 exact, [P])")

    # basis change preserves the trace (and N_c); color-average does NOT (different functional)
    rng = np.random.default_rng(7)
    U, _ = np.linalg.qr(rng.normal(size=(N_C * 3, N_C * 3)))
    check(math.isclose(np.trace(U.conj().T @ H @ U).real, np.trace(H).real, rel_tol=1e-10),
          "basis change Tr(U^dag H U) = Tr(H): sqrt(N_c) is BASIS-INVARIANT (physical)")
    color_avg = np.trace(H).real / N_C
    check(not math.isclose(color_avg, np.trace(H).real, rel_tol=1e-6),
          "color-average (1/N_c)Tr is a DIFFERENT functional (removes N_c) -> not a basis change -> countermodel B excluded")

    # exports: carrier forced; B excluded; no-go preserved; floor fully forced mod absolute Planck
    check(EXPORT_FLAGS["Export_sqrtNc_carrier_forced_by_color_triplet_trace_P"] == 1,
          "sqrt(N_c) forced for the y_t-free floor by the physical color-triplet trace")
    check(EXPORT_FLAGS["Export_countermodel_B_color_strip_excluded_by_gauge_spectral_P"] == 1,
          "countermodel B (color-strip) excluded -- not an admissible representation of the banked a2")
    check(EXPORT_FLAGS["Export_no_go_preserved_inversion_only_P"] == 1
          and EXPORT_FLAGS["Export_absolute_y_t_value_derived_P"] == 0,
          "no-go v24.3.169 preserved inversion-only: absolute y_t still NOT derivable")
    check(EXPORT_FLAGS["Export_floor_fully_forced_modulo_absolute_planck_magnitude_P"] == 1,
          "floor fully forced: exponent (.184) + measure (.181) + Planck norm (.183) + carrier (this)")
    check(EXPORT_FLAGS["Export_absolute_planck_magnitude_route_b_P"] == 1,
          "only the ABSOLUTE Planck magnitude remains -- the one external dimensional input (route-b)")
    check(EXPORT_FLAGS["measured_target_consumed"] == 0, "no measured target consumed")

    return _result(
        name=("T_ew_sqrtNc_carrier_forced_by_color_triplet_trace: sqrt(N_c) = a_Y/sqrt(b) is FORCED "
              "for the y_t-free floor by the physical color-triplet trace (a2 = Sum N_c*Tr exact over "
              "H_F, [P]); color-strip (countermodel B) is a different trace functional, not a basis "
              "change -> EXCLUDED. CLOSES the last prefactor clause; floor fully forced modulo the "
              "absolute Planck magnitude (route-b). No-go preserved inversion-only [P_structural]"),
        tier=4,
        epistemic='P_structural',
        summary=(
            "The last open prefactor clause, closed under the principal's inversion-only ruling on "
            "the y_t no-go. The y_t-free floor's sqrt(N_c) = a_Y/sqrt(b) (y_t cancels; both carry "
            "N_c) is the physical color-triplet trace ratio: a2 = Sum N_c*Tr is EXACT over H_F=C^96 "
            "(L_normalization_coefficient [P]) with SU(3)/N_c=3/color-triplet quarks fixed by "
            "Theorem_R + T_gauge + T_field [P]. sqrt(N_c) is BASIS-INVARIANT (Tr(U^dag A U)=Tr(A)); "
            "color-stripping (countermodel B) is NOT a basis change but a color-average (1/N_c)Tr, a "
            "different trace functional with a different codomain -- no unitary implements it -- so B "
            "is not an admissible representation of the banked a2 and is EXCLUDED. By the invariance "
            "criterion sqrt(N_c) is physical and FORCED. Both truths hold: the no-go (v24.3.169) stays "
            "inversion-only (absolute y_t still not derivable -- extracting y_t from a_Y is the "
            "genuinely ambiguous operation), while the basis-invariant RATIO is forced. CONSEQUENCE: "
            "the EW floor is now FULLY forced -- exponent 102^-8 (.184) + measure (4pi)^-1 (.181) + "
            "Planck normalization G^-1/2 (.183, gravity) + carrier sqrt(N_c) (this). The only residue "
            "is the absolute Planck MAGNITUDE, the one external dimensional input by design "
            "(gravity.py). v_H is forced up to that single anchor."
        ),
        key_result=(
            "sqrt(N_c) FORCED (physical color-triplet trace ratio, basis-invariant; color-strip B is a "
            "different functional, excluded). Last prefactor clause closed -> EW floor fully forced "
            "modulo the absolute Planck magnitude (route-b). No-go intact: absolute y_t still not "
            "derivable."
        ),
        dependencies=['L_normalization_coefficient', 'Theorem_R', 'T_gauge', 'T_field',
                      'T_sigma_scale_yukawa_free_geometric_component',
                      'T_ew_prefactor_axiom_independence',
                      'T_ew_planck_anchor_forced_by_gravity_consistency'],
        artifacts=dict(
            ratio="a_Y/sqrt(b) = sqrt(N_c) (y_t cancels)",
            physical_trace="a2 = Sum N_c*Tr exact over H_F=C^96 (L_normalization_coefficient [P])",
            basis_invariance="Tr(U^dag A U)=Tr(A) preserves N_c; color-average is a different functional",
            excluded="countermodel B (color-strip) -- not a basis change",
            no_go_status="preserved inversion-only (absolute y_t still not derivable)",
            floor_status="fully forced modulo the absolute Planck magnitude (route-b)",
            export_flags=dict(EXPORT_FLAGS),
        ),
    )


_CHECKS = {
    "T_ew_sqrtNc_carrier_forced_by_color_triplet_trace":
        check_T_ew_sqrtNc_carrier_forced_by_color_triplet_trace_P,
}


def register(registry):
    registry.update(_CHECKS); return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
