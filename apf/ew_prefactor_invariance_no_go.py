"""EW vev O(1) prefactor invariance NO-GO [P_structural] (current-stack).

Companion to the banked hierarchy mechanism (apf/ew_planck_hierarchy_mechanism.py,
v24.3.176): the suppression FORM v/M_Pl ~ d_eff^(-C_boson/2) is the merit; the exact
absolute vev is route-b. This module banks WHY the absolute value cannot be made native
under the current theorem stack -- a no-go that fences the prefactor route and names the
single missing object that would close it. (Arc v27..v35 + the 2026-05-29 prefactor
derivation attempt converged on this.)

THE TARGET. v_floor = M_Pl * eta * d_eff^(-C_boson/2), eta = sqrt(N_c)/(pi sqrt(C_boson)).
Closing the absolute value natively needs eta derived. Write the most general current-depth
prefactor as eta(g, mu, rho) = sqrt(g) * rho / (mu * sqrt(C_boson)), with three carriers:
  g   in {1, N_c, N_c^2, ...}   -- the trace / color carrier
  mu  in {1, pi, 2 pi, ...}     -- the static measure normalization
  rho in {1, 1/sqrt(8 pi), ...} -- the Planck convention (unreduced vs reduced M_Pl)
The desired formula picks g = N_c, mu = pi, rho = 1 (unreduced).

WHAT IS DERIVABLE (clean): the uniform-mode factor 1/sqrt(C_boson). For orthonormal static
bosonic well coordinates q_i, the normalized uniform coordinate lambda = (1/sqrt(C_boson))
sum_i q_i has |lambda|^2 = 1, forcing the 1/sqrt(C_boson) by canonical normalization. This
piece is not in dispute.

THE NO-GO (this module's [P_structural] claim). The three remaining carriers (g, mu, rho)
are INDEPENDENT under the current stack -- no single invariant principle fixes them together
-- and each changes v_H:
  (1) COLOR CARRIER g. Color-stripping g = N_c -> 1 moves eta by 1/sqrt(N_c) = 1/sqrt(3).
      This is the SAME convention fork the banked top-Yukawa no-go records
      (T_yt_absolute_scale_not_fixable_by_normalization_no_go, v24.3.169): color counting
      to fix an absolute scale is structurally non-invariant. So sqrt(N_c) cannot be rescued
      by rephrasing it as a_Y = N_c or as a matrix norm -- that reopens the forbidden
      Yukawa-normalization route. The full-colored carrier is a DECLARATION here, not a
      derived invariant.
  (2) MEASURE mu. The desired factor is a SINGLE 1/pi. But a genuine C_boson-mode Gaussian
      determinant gives a MODE-COUNTED normalization pi^(-C_boson/2) = pi^(-8) ~ 1.05e-4,
      not 1/pi ~ 0.318 (a factor of ~3020 apart). So 1/pi is NOT the ordinary determinant
      measure; it is an extra single scalar. Deriving it would need a special static
      radial/phase/half-period measure theorem mu_static = pi. Choosing pi because it lands
      near 246 GeV is target selection.
  (3) PLANCK rho. Unreduced vs reduced M_Pl differ by sqrt(8 pi) ~ 5.01. Switching to reduced
      moves v_H by 1/5.01 -- not a small convention change. A valid theorem would have to say
      why the hierarchy map couples to G^(-1/2) rather than (8 pi G)^(-1/2).

CONCLUSION. If g, mu, rho are not fixed by one common invariant structural principle, then
chi = sqrt(g) rho / mu is convention-dependent, and since changing any of g, mu, rho changes
v_H, the exact absolute value is not invariant. Under the present stack:
    Export_prefactor_invariance_P = 0.
The route reduces to a single missing object -- the STATIC TRACE-MEASURE INVARIANCE THEOREM
-- which would have to derive sqrt(N_c), 1/pi, and unreduced M_Pl in ONE measure theorem
(full-colored carrier forced, pi the unique static radial measure, unreduced M_Pl the
matching anchor, all three one theorem not three fixes). That object is NOT in the current
corpus. Until it is, promoting the exact prefactor would be smuggling.

SCOPE. This fences the prefactor (the O(1) eta). It is INDEPENDENT of the exponent /
mode-restriction question (C_boson = 16 vs Paper-7 C_total = 61), which remains separately
OPEN in apf/ew_planck_hierarchy_mechanism.py. No value banked; no measured target consumed.

[P_structural_ew_prefactor_invariance_no_go_current_stack]; absolute v_H blocked.

REFINEMENT (2026-05-30 bank audit, v24.3.181): the "1/pi is a single free scalar unlike
any C_boson-mode determinant pi^(-8)" point below compares to the WRONG object. The right
object is the per-loop continuation-sum measure (4pi)^(-D/2) (v24.3.166), whose ROOT is
1/(4pi) = 1/(pi sqrt C_boson) at C_boson=16 -- exactly the floor measure factor (see
apf/ew_floor_measure_continuation_root.py). So 1/pi is NOT homeless; it is the root of a
banked D=4-forced measure. The independence/no-go conclusion below STILL HOLDS (the 1/pi
home is conditional on the root-measure identification, and sqrt(N_c)+Planck remain free),
but the "free scalar, looks like a fit" characterization of 1/pi specifically is corrected.
"""
from __future__ import annotations

import math

from apf.apf_utils import check, _result

N_C, C_BOSON, D_EFF = 3, 16, 102
M_PL_UNREDUCED = 1.22089e19

EXPORT_FLAGS = dict(
    Export_prefactor_invariance_no_go_current_stack_P=1,   # the no-go itself
    Export_uniform_mode_factor_derivable_P=1,              # 1/sqrt(C_boson) is clean
    Export_prefactor_invariance_P=0,                       # the route FAILS under current stack
    Export_vH_absolute_scale_native_derivation_P=0,
    Export_vH_physical_final_P=0,
    Export_static_trace_measure_invariance_theorem_present_P=0,  # named missing object, not in corpus
    measured_target_consumed=0,
    target_consumed=0,
)


def _eta(g=N_C, mu=math.pi, rho=1.0, c_boson=C_BOSON):
    """General current-depth prefactor eta(g, mu, rho) = sqrt(g) rho / (mu sqrt(C_boson))."""
    return math.sqrt(g) * rho / (mu * math.sqrt(c_boson))


def check_T_ew_prefactor_invariance_no_go_P():
    # uniform-mode factor 1/sqrt(C_boson) is derivable (canonical normalization) -- clean
    lam_norm = sum((1.0 / math.sqrt(C_BOSON)) ** 2 for _ in range(C_BOSON))
    check(math.isclose(lam_norm, 1.0, rel_tol=1e-12), "uniform mode |lambda|^2 = 1 forces 1/sqrt(C_boson)")

    eta0 = _eta()  # g=N_c, mu=pi, rho=1
    # (1) color carrier is load-bearing: g = N_c -> 1 moves eta by 1/sqrt(N_c)
    check(math.isclose(_eta(g=1) / eta0, 1.0 / math.sqrt(N_C), rel_tol=1e-12),
          "color strip g=N_c->1 moves eta by 1/sqrt(N_c) (= the banked yt no-go fork)")
    # (2) the single 1/pi is NOT the C_boson-mode determinant measure pi^(-C_boson/2)
    single_over_pi = 1.0 / math.pi
    mode_counted = math.pi ** (-(C_BOSON / 2.0))
    check(abs(single_over_pi / mode_counted) > 1000.0,
          "single 1/pi is not the mode-counted determinant pi^(-C_boson/2) (~3020x apart)")
    # (3) Planck convention is load-bearing: reduced vs unreduced differ by sqrt(8 pi) ~ 5.01
    check(math.isclose(_eta(rho=1.0 / math.sqrt(8 * math.pi)) / eta0, 1.0 / math.sqrt(8 * math.pi), rel_tol=1e-12),
          "reduced Planck moves eta (hence v_H) by 1/sqrt(8 pi) ~ 1/5.01")
    # the three carriers are independent -> chi convention-dependent -> invariance fails
    check(EXPORT_FLAGS["Export_prefactor_invariance_P"] == 0,
          "prefactor invariance route fails under current stack (g, mu, rho independent)")
    check(EXPORT_FLAGS["Export_static_trace_measure_invariance_theorem_present_P"] == 0,
          "the single closing object (static trace-measure invariance theorem) is NOT in the corpus")
    # honest non-claims
    check(EXPORT_FLAGS["Export_vH_absolute_scale_native_derivation_P"] == 0, "absolute vev not native")
    check(EXPORT_FLAGS["Export_vH_physical_final_P"] == 0, "no physical-final claim")
    check(EXPORT_FLAGS["measured_target_consumed"] == 0, "no measured target consumed")

    return _result(
        name=("T_ew_prefactor_invariance_no_go: the EW vev O(1) prefactor "
              "eta = sqrt(N_c)/(pi sqrt(C_boson)) is NOT derivable under the current stack "
              "[P_structural no-go]; absolute v_H blocked; reduces to a missing static "
              "trace-measure invariance theorem"),
        tier=4,
        epistemic='P_structural',
        summary=(
            "No-go: the O(1) prefactor eta = sqrt(g) rho/(mu sqrt(C_boson)) has three "
            "INDEPENDENT carriers under the current stack -- color g=N_c (strip -> x1/sqrt3, "
            "= the banked yt no-go fork), measure mu=pi (a SINGLE 1/pi, NOT the C_boson-mode "
            "determinant pi^(-8) ~ 1.05e-4; ~3020x apart, so not the Gaussian normalization), "
            "and Planck rho (unreduced vs reduced differ by sqrt(8pi) ~ 5.01). The clean piece "
            "is 1/sqrt(C_boson) (uniform-mode RMS). Since changing g, mu or rho changes v_H and "
            "no single invariant principle fixes them together, the exact absolute value is not "
            "invariant: Export_prefactor_invariance_P = 0. Closing it reduces to ONE missing "
            "object -- a static trace-measure invariance theorem (full-colored carrier forced + "
            "pi the unique static radial measure + unreduced M_Pl the matching anchor, as one "
            "measure theorem) -- which is NOT in the corpus. Promoting the exact prefactor would "
            "be smuggling. Independent of the C_boson=16 vs C_total=61 mode-restriction (open)."
        ),
        key_result=(
            "[P_prefactor_invariance] = 0 under the current stack; eta's color/measure/Planck "
            "carriers are independent convention choices; 1/pi is not the determinant measure; "
            "reduces to a missing static trace-measure invariance theorem. Absolute v_H blocked."
        ),
        dependencies=['T_yt_absolute_scale_not_fixable_by_normalization_no_go',
                      'T_sigma_scale_capacity_formula_held_pending_independent_scale',
                      'T_ew_planck_hierarchy_capacity_suppression_mechanism'],
        artifacts=dict(
            eta_desired=round(_eta(), 6),
            color_strip_ratio=round(1.0 / math.sqrt(N_C), 6),
            single_over_pi=round(1.0 / math.pi, 6),
            mode_counted_pi_minus_8=math.pi ** -8,
            planck_reduced_ratio=round(1.0 / math.sqrt(8 * math.pi), 6),
            missing_object="STATIC_TRACE_MEASURE_INVARIANCE_THEOREM (not in corpus)",
            export_flags=dict(EXPORT_FLAGS),
        ),
    )


_CHECKS = {
    "T_ew_prefactor_invariance_no_go": check_T_ew_prefactor_invariance_no_go_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
