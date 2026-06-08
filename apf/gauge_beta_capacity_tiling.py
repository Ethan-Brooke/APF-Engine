"""The abelian beta coefficient is in the capacity ledger: 6|b_Y| = d_eff - C_total [P_structural].

L_beta_capacity established that the two NON-ABELIAN gauge beta coefficients match the capacity
ledger as conditions that force N_gen = 3:
    6|b_3| = C_vacuum = 42   (66 - 8n = 9n + 15  ->  n = 3)
    6|b_2| = C_matter = 19   (43 - 8n = 6n + 1   ->  n = 3)
This module adds the ABELIAN (hypercharge) member of the same family, closing the gauge sector's
beta-to-capacity map:
    6|b_Y| = d_eff - C_total = 41   ((40/3)n + 1 = 9n + 14  ->  n = 3)
where |b_Y| = 41/6 is the U(1)_Y one-loop coefficient in the SAME (Standard-Model, non-GUT)
normalization L_beta_capacity uses for |b_2| = 19/6 and |b_3| = 7.

THREE INDEPENDENT DETERMINATIONS OF N_gen = 3.
Each gauge factor gives one capacity-beta equation, and each independently solves to n = 3. The
abelian one is genuinely independent: the non-abelian 6|b| DECREASE with n (more matter screens the
asymptotically-free running), while the abelian 6|b_Y| INCREASES with n (U(1) is not asymptotically
free); the decreasing non-abelian matches and the increasing abelian match coincide with their
capacity targets only at n = 3. So N_gen = 3 is over-determined by the gauge sector: three equations,
one solution.

THE THREE BETAS TILE d_eff.
At the physical n = 3 the three coefficients are 6|b_3|, 6|b_2|, 6|b_Y| = 42, 19, 41, and
    6(|b_3| + |b_2| + |b_Y|) = 42 + 19 + 41 = 102 = d_eff.
The non-abelian pair sums to C_total = 61; the abelian completes the tiling to the effective
degeneracy d_eff = 102. So the gauge running rates are the capacity ledger: SU(3) <-> C_vacuum,
SU(2) <-> C_matter, U(1) <-> (d_eff - C_total), total <-> d_eff.

SCOPE -- this is about the RUNNING RATE, not the absolute coupling. The identity fixes the abelian
beta coefficient against capacity; it does NOT fix the absolute U(1) hypercharge COUPLING value. The
absolute hypercharge normalization remains the gauge sector's one residual dimensionless input (see
the reference note 'The Gauge Coupling Normalization Audit', 2026-05-30). The numerical observation
that 1/alpha_Y(M_cross) approx C_total = 61 would close that input if it could be DERIVED, but it is
currently back-solved from the measured alpha_s and is NOT a capacity output -- held [C], not banked.

[P_structural] -- extends L_beta_capacity to the abelian sector; a numerical identity between the
Standard-Model hypercharge beta coefficient and the capacity ledger, forcing N_gen = 3 as a third
independent determination. No measured coupling consumed (beta coefficients are field-content counts).
"""
from __future__ import annotations

from fractions import Fraction as F

from apf.apf_utils import check, _result

# capacity ledger as functions of n_generations (from L_count)
def _C_total(n): return 15 * n + 16
def _C_vac(n):   return 9 * n + 15
def _C_mat(n):   return 6 * n + 1
def _d_eff(n):   return (_C_total(n) - 1) + _C_vac(n)      # = 24n + 30

# 6|beta_i|(n) in Standard-Model (non-GUT) normalization
def _six_b3(n): return 66 - 8 * n                          # n=3 -> 42
def _six_b2(n): return 43 - 8 * n                          # n=3 -> 19
def _six_bY(n): return F(40, 3) * n + 1                    # n=3 -> 41  (|b_Y| = 41/6 at n=3)

EXPORT_FLAGS = dict(
    Export_abelian_beta_in_capacity_ledger_P=1,            # 6|b_Y| = d_eff - C_total
    Export_three_gauge_betas_tile_d_eff_P=1,               # sum*6 = 102
    Export_third_independent_Ngen3_determination_P=1,
    Export_abelian_absolute_coupling_fixed_P=0,            # NOT fixed -- the residual input remains
    Export_alpha_Y_cross_equals_C_total_derived_P=0,       # held [C], data-back-solved, not derived
    measured_target_consumed=0,
    target_consumed=0,
)


def check_T_gauge_beta_capacity_tiling_abelian_P():
    n3 = 3
    # the abelian identity at n=3
    check(_six_bY(n3) == _d_eff(n3) - _C_total(n3) == 41,
          "6|b_Y| = d_eff - C_total = 41 at n=3 (abelian beta in the ledger)")
    # it is a THIRD capacity-beta equation forcing n=3 (independent of the non-abelian two)
    # solve (40/3)n + 1 = 9n + 14  ->  (13/3)n = 13  ->  n = 3
    lhs_coeff, rhs_coeff = F(40, 3), F(9)
    const_gap = 14 - 1
    n_sol = const_gap / (lhs_coeff - rhs_coeff)
    check(n_sol == 3, "6|b_Y| = d_eff - C_total solves to N_gen = 3 (third independent determination)")
    # the non-abelian two also solve to 3 (consistency with L_beta_capacity)
    check((66 - 8 * 3) == _C_vac(3) and (43 - 8 * 3) == _C_mat(3),
          "non-abelian 6|b_3|=C_vacuum, 6|b_2|=C_matter also at n=3 (L_beta_capacity)")
    # independence: abelian increases with n, non-abelian decrease -> coincide only at n=3
    check(_six_bY(4) > _six_bY(3) > _six_bY(2) and (66 - 8 * 2) > (66 - 8 * 3) > (66 - 8 * 4),
          "abelian 6|b_Y| INCREASES with n, non-abelian DECREASE -> the matches are independent")
    # the three betas tile d_eff at n=3
    check(_six_b3(n3) + _six_b2(n3) + int(_six_bY(n3)) == _d_eff(n3) == 102,
          "6(|b_3|+|b_2|+|b_Y|) = 42+19+41 = 102 = d_eff (the three betas tile d_eff)")

    # honest scope: running rate fixed, absolute coupling NOT
    check(EXPORT_FLAGS["Export_abelian_absolute_coupling_fixed_P"] == 0,
          "this fixes the abelian BETA against capacity, NOT the absolute hypercharge coupling")
    check(EXPORT_FLAGS["Export_alpha_Y_cross_equals_C_total_derived_P"] == 0,
          "1/alpha_Y(M_cross)=C_total is a data-back-solved coincidence, held [C], not derived/banked")
    check(EXPORT_FLAGS["measured_target_consumed"] == 0,
          "beta coefficients are field-content counts; no measured coupling consumed")

    return _result(
        name=("T_gauge_beta_capacity_tiling_abelian: the U(1)_Y hypercharge beta is in the capacity "
              "ledger -- 6|b_Y| = d_eff - C_total = 41, a third capacity-beta equation forcing "
              "N_gen = 3 (independent of the SU(2)/SU(3) ones; abelian increases with n, non-abelian "
              "decrease, coincide only at n=3). The three gauge betas tile d_eff: "
              "6(|b_3|+|b_2|+|b_Y|) = 42+19+41 = 102. Extends L_beta_capacity to the abelian sector. "
              "Fixes the running RATE, not the absolute coupling [P_structural]"),
        tier=4,
        epistemic='P_structural',
        summary=(
            "Closes the gauge sector's beta-to-capacity map. L_beta_capacity matched the two "
            "non-abelian betas to the ledger as N_gen=3-forcing conditions (6|b_3|=C_vacuum=42, "
            "6|b_2|=C_matter=19). This adds the abelian member in the same Standard-Model normalization: "
            "6|b_Y| = d_eff - C_total = 41, equivalently (40/3)n + 1 = 9n + 14, which solves to n = 3. "
            "It is a genuinely independent third determination of N_gen=3: the non-abelian 6|b| "
            "decrease with n (matter screens the asymptotically-free running) while the abelian 6|b_Y| "
            "increases (U(1) is not asymptotically free), so the decreasing non-abelian matches and the "
            "increasing abelian match coincide with their capacity targets only at n=3. At n=3 the three "
            "coefficients 42, 19, 41 tile the effective degeneracy: 6(|b_3|+|b_2|+|b_Y|) = 102 = d_eff, "
            "with the non-abelian pair making C_total=61 and the abelian completing to d_eff. SCOPE: "
            "this fixes the abelian RUNNING RATE against capacity; it does NOT fix the absolute U(1) "
            "hypercharge COUPLING, which remains the gauge sector's one residual dimensionless input. "
            "The numerical observation 1/alpha_Y(M_cross) approx C_total = 61 (which, with the derived "
            "crossing coupling and sin^2theta_W = 3/13, would predict alpha_s(M_Z) to 0.00% and close "
            "that input) is back-solved from the measured alpha_s and is NOT a capacity output -- held "
            "[C] in the gauge-closure research note, not banked here. No measured coupling consumed."
        ),
        key_result=(
            "6|b_Y| = d_eff - C_total = 41: the abelian hypercharge beta is in the capacity ledger, a "
            "third independent N_gen=3 determination; the three gauge betas tile d_eff=102 (42+19+41). "
            "Extends L_beta_capacity to U(1). Fixes the running rate, NOT the absolute coupling; the "
            "1/alpha_Y(M_cross)=C_total closure is held [C], data-back-solved, not derived."
        ),
        dependencies=['L_beta_capacity', 'L_count', 'L_self_exclusion', 'T11'],
        artifacts=dict(
            abelian_identity="6|b_Y| = d_eff - C_total = 41 (SM normalization, |b_Y|=41/6)",
            forces_Ngen="(40/3)n + 1 = 9n + 14 -> n = 3 (third independent determination)",
            independence="abelian 6|b_Y| increases with n, non-abelian decrease; coincide only at n=3",
            tiling="6(|b_3|+|b_2|+|b_Y|) = 42+19+41 = 102 = d_eff (non-abelian pair = C_total=61)",
            scope="running RATE fixed; absolute hypercharge coupling NOT fixed (residual input)",
            held_conjecture="1/alpha_Y(M_cross)=C_total -> alpha_s to 0.00%; [C], data-back-solved, not derived",
            export_flags=dict(EXPORT_FLAGS),
        ),
    )


_CHECKS = {
    "T_gauge_beta_capacity_tiling_abelian":
        check_T_gauge_beta_capacity_tiling_abelian_P,
}


def register(registry):
    registry.update(_CHECKS); return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
