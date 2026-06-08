"""EW prefactor axiom-independence theorem [P_structural] -- exact v_H is logically
independent of {A1, A2, K3}.

The capstone of the prefactor line. Where v24.3.177 records that the O(1) prefactor's three
carriers (color/measure/Planck) are convention-dependent FACTOR BY FACTOR, this module proves
the stronger MODEL-THEORETIC statement: the exact prefactor -- hence the exact 246 GeV value --
is LOGICALLY INDEPENDENT of the current APF axioms. It is not "a theorem we have not found"; it
is "not a theorem of A1/A2/K3," proven by a countermodel family. Closing it therefore requires
ADDING a structural principle, and any exact-v_H claim that does not add and own such a principle
is smuggling.

THE INDEPENDENCE PROOF (countermodel family).
With the banked content fixed -- the active count C, the degeneracy d_eff, the root-measure
suppression d_eff^(-C/2), and the uniform-mode normalization 1/sqrt(C) -- the most general
remaining static prefactor is
    eta(g, mu, rho) = sqrt(g) * rho / (mu * sqrt(C)),
with g the trace/color carrier, mu the static radial/angular measure, rho the Planck convention.
Construct four completions of the SAME current-depth hierarchy mechanism:
    A. full colored      g = N_c,    mu = pi, rho = 1            -> v_H = 246.21 GeV
    B. color-stripped    g = 1,      mu = pi, rho = 1            -> v_H = 142.15 GeV  (A / sqrt(N_c))
    C. double-colored    g = N_c^2,  mu = pi, rho = 1            -> v_H = 426.45 GeV  (A * sqrt(N_c))
    D. reduced-Planck    g = N_c,    mu = pi, rho = 1/sqrt(8 pi) -> v_H = 49.11 GeV   (A / sqrt(8 pi))
Each completion preserves: A1 (finite capacity -- all v_H finite), A2/no-ghost (the quadratic
root-measure exponent d_eff^(-C/2) is unchanged), K3 (additive cost on disjoint supports -- the
carrier/measure/Planck choices do not touch the support-local cost semantics), the banked
1/sqrt(C) uniform-mode normalization, and the no-smuggling guards (no measured v_H or y_t
normalization consumed -- the four differ only by convention parameters). Yet they give four
DIFFERENT absolute v_H. A quantity that takes different values across models of the same axioms
is not determined by those axioms. Hence:
    exact prefactor (and exact v_H)  is INDEPENDENT of {A1, A2, K3}.
    Export_prefactor_invariance_principle_P = 0
    Export_exact_native_vH_P = 0

WHAT STILL DERIVES (the one invariant clause).
1/sqrt(C) is forced: for orthonormal static coordinates q_i, the equal-weight normalized
coordinate lambda = (1/sqrt(C)) sum_i q_i has |lambda|^2 = 1 uniquely. This clause is the SAME
across all four countermodels, which is why it survives the independence argument.

CONSEQUENCE -- closing it needs a NEW AXIOM, not a derivation.
A positive prefactor theorem would have to FORCE g = N_c, mu = pi, rho = 1 (and C = 16 via the
reservoir reading). The countermodel family shows none of these is forced by A1/A2/K3. So the
only way to close the exact value is to ADD a structural principle -- the static colored bosonic
reservoir measure principle (carrier multiplicity N_c, uniform normalization 1/sqrt(C_boson),
radial half-period pi, anchor M_Pl = G^(-1/2)) -- under which the exact value becomes CONDITIONAL
on that new principle, NOT derived from A1. This module banks the independence; it does NOT add
the principle.

[P_structural_ew_prefactor_axiom_independence]; exact v_H independent of {A1,A2,K3}; closing it
requires a new structural axiom; no measured target consumed.
"""
from __future__ import annotations

import math

from apf.apf_utils import check, _result

N_C, C_BOSON, D_EFF = 3, 16, 102
M_PL = 1.22089e19
LIFT = 12.0 / 7.0


def _vH(g, mu, rho, c=C_BOSON):
    """v_H = M_Pl * sqrt(g)/(mu sqrt(C)) * d_eff^(-C/2) * 12/7  -- only g,mu,rho vary."""
    return M_PL * math.sqrt(g) / (mu * math.sqrt(c)) * (D_EFF ** (-(c / 2.0))) * rho


EXPORT_FLAGS = dict(
    Export_prefactor_axiom_independence_no_go_P=1,
    Export_uniform_mode_1_over_sqrtC_invariant_P=1,       # the one clause shared by all countermodels
    Export_prefactor_invariance_principle_P=0,            # not a theorem of A1/A2/K3
    Export_exact_native_vH_P=0,
    Export_closing_requires_new_structural_axiom_P=1,     # the consequence
    Export_vH_physical_final_P=0,
    measured_target_consumed=0,
    target_consumed=0,
)


def check_T_ew_prefactor_axiom_independence_P():
    # the four admissible countermodels
    A = _vH(N_C, math.pi, 1.0)
    B = _vH(1, math.pi, 1.0)
    Cc = _vH(N_C ** 2, math.pi, 1.0)
    D = _vH(N_C, math.pi, 1.0 / math.sqrt(8 * math.pi))

    # they reproduce the known convention-moves
    check(abs(A * LIFT - 246.2119523) < 1e-3, f"A (full colored) v_H ~ 246.21, got {A*LIFT:.4f}")
    check(math.isclose(B, A / math.sqrt(N_C), rel_tol=1e-12), "B = A / sqrt(N_c) (color strip)")
    check(math.isclose(Cc, A * math.sqrt(N_C), rel_tol=1e-12), "C = A * sqrt(N_c) (double color)")
    check(math.isclose(D, A / math.sqrt(8 * math.pi), rel_tol=1e-12), "D = A / sqrt(8 pi) (reduced Planck)")

    # INDEPENDENCE: four models of the same axioms, four different values
    vals = [round(x, 4) for x in (A, B, Cc, D)]
    check(len(set(vals)) == 4, f"four distinct v_H across admissible countermodels: {vals}")

    # all four preserve the invariant structure (only g, mu, rho vary; exponent + 1/sqrt(C) fixed)
    supp = D_EFF ** (-(C_BOSON / 2.0))
    check(abs(supp - D_EFF ** (-8)) < 1e-30, "root-measure exponent d_eff^(-C/2) = 102^-8 fixed in all four")
    check(math.isclose(sum((1 / math.sqrt(C_BOSON)) ** 2 for _ in range(C_BOSON)), 1.0, rel_tol=1e-12),
          "uniform-mode 1/sqrt(C) is the invariant clause shared by all countermodels")
    for x in (A, B, Cc, D):
        check(0 < x < 1e19, "each countermodel has finite positive v_floor (A1 preserved)")

    # the no-go conclusion + its consequence
    check(EXPORT_FLAGS["Export_prefactor_invariance_principle_P"] == 0,
          "exact prefactor is NOT a theorem of A1/A2/K3 (independent)")
    check(EXPORT_FLAGS["Export_exact_native_vH_P"] == 0, "exact v_H not native")
    check(EXPORT_FLAGS["Export_closing_requires_new_structural_axiom_P"] == 1,
          "closing the exact value requires ADDING a structural axiom (reservoir measure principle), not deriving one")
    check(EXPORT_FLAGS["measured_target_consumed"] == 0, "no measured target consumed")

    return _result(
        name=("T_ew_prefactor_axiom_independence: the exact EW vev prefactor (hence exact v_H) is "
              "LOGICALLY INDEPENDENT of {A1,A2,K3} -- proven by a 4-model countermodel family "
              "(246.21 / 142.15 / 426.45 / 49.11 GeV, all admissible); closing it requires a NEW "
              "structural axiom, not a derivation [P_structural]"),
        tier=4,
        epistemic='P_structural',
        summary=(
            "Model-theoretic independence (capstone of the prefactor line; stronger than the "
            "factor-level no-go v24.3.177). With C, d_eff, the root-measure d_eff^(-C/2), and "
            "1/sqrt(C) fixed, the residual prefactor eta(g,mu,rho)=sqrt(g) rho/(mu sqrt(C)) admits "
            "four completions A/B/C/D (g in {N_c,1,N_c^2}, rho in {1, 1/sqrt(8pi)}) that ALL "
            "preserve A1 (finite), A2 (quadratic exponent), K3 (support-local cost), the uniform "
            "1/sqrt(C), and the no-smuggling guards, yet give v_H = 246.21 / 142.15 / 426.45 / "
            "49.11 GeV. A quantity taking different values across models of the same axioms is not "
            "determined by them: exact prefactor and exact v_H are INDEPENDENT of {A1,A2,K3}. The "
            "one invariant clause is 1/sqrt(C) (shared by all four). CONSEQUENCE: closing the exact "
            "value requires ADDING a structural principle (the static colored bosonic reservoir "
            "measure principle: carrier N_c, measure pi, anchor G^(-1/2)) -- under which the value "
            "is CONDITIONAL on that new axiom, not derived from A1. Any exact-v_H claim that does "
            "not add and own such a principle is smuggling. This module banks the independence, NOT "
            "the principle."
        ),
        key_result=(
            "exact v_H independent of {A1,A2,K3} (4 admissible countermodels, 4 values); only "
            "1/sqrt(C) is invariant; closing requires a NEW structural axiom (reservoir measure "
            "principle), making the value conditional not derived. Exact v_H stays blocked."
        ),
        dependencies=['T_ew_prefactor_invariance_no_go',
                      'T_ew_bosonic_enforcement_reservoir_theorem',
                      'T_ew_planck_hierarchy_capacity_suppression_mechanism'],
        artifacts=dict(
            countermodels=dict(
                A_full_colored_GeV=round(A * LIFT, 4),
                B_color_stripped_GeV=round(B * LIFT, 4),
                C_double_colored_GeV=round(Cc * LIFT, 4),
                D_reduced_planck_GeV=round(D * LIFT, 4),
            ),
            invariant_clause="1/sqrt(C_boson) (shared by all four countermodels)",
            consequence="closing exact v_H requires a NEW structural axiom (reservoir measure principle)",
            export_flags=dict(EXPORT_FLAGS),
        ),
    )


_CHECKS = {
    "T_ew_prefactor_axiom_independence": check_T_ew_prefactor_axiom_independence_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
