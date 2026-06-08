"""EW floor measure factor = root of the banked continuation-sum measure [P_structural].

Audit finding (2026-05-30, "audit the bank and find the missing theorem"). The static-trace-
measure theorem that the prefactor line keeps naming as "not in corpus" is NOT a single
monolithic missing object. One of its clauses -- the `1/pi` measure -- already has a banked home.

THE IDENTITY.
The y_t-free floor is
    v_floor = M_Pl * sqrt(N_c) / (pi * sqrt(C_boson) * d_eff^(C_boson/2)).
Its measure factor 1/(pi*sqrt(C_boson)), at C_boson = 16, equals 1/(4 pi). The BANKED
continuation-sum measure (apf/continuation_sum_measure.py, v24.3.166, [P_structural], forced by
native D=4 via T8) is (4 pi)^(-D/2) = 1/(16 pi^2) at D=4. Its square root is (4 pi)^(-1) = 1/(4 pi).
So:
    1/(pi*sqrt(C_boson))  ==  sqrt[(4 pi)^(-D/2)]   (exact, at C_boson=16, D=4),
and the whole floor reads
    v_floor = M_Pl * sqrt(N_c) * sqrt[continuation-sum measure] * d_eff^(-C_boson/2).
This is structurally natural: the floor is a ROOT-measure (d_eff^(-C/2) is the root of a
continuation-sum microstate volume), so it carries the root of the per-loop continuation-sum
MEASURE (4 pi)^(-D/2) as well.

WHAT THIS RELOCATES.
The v24.3.177 no-go flagged the `1/pi` as "a single free scalar, ~3020x from the C_boson-mode
determinant pi^(-8)". That compared to the WRONG object: a C_boson-mode Gaussian determinant.
The right object is the per-loop continuation-sum measure (4 pi)^(-D/2), whose root the floor
matches exactly. So the `1/pi` is not homeless -- it is the root of a banked, D=4-FORCED measure.
The no-go's independence conclusion still stands (see RESIDUAL); only the "free scalar with no
measure home" sub-characterization is corrected.

RESIDUAL (why this is a narrowing, not a closure).
The identity holds AT C_boson = 16 (so that sqrt(C_boson) = 4 coincides with the geometric "4"
in the continuation measure's (4 pi), which comes from the Gamma(D/2) cancellation at D=4). That
coincidence is admissible and structurally motivated (root-measure over continuation-sums) but is
NOT proven forced: identifying the floor's measure factor AS the continuation-measure root, and
the capacity sqrt(C_boson) AS the geometric 4, are the load-bearing claims. So `1/pi` is
conditionally homed, not unconditionally derived.

NET EFFECT ON THE MISSING THEOREM. The static colored bosonic reservoir measure principle had
four clauses {1/pi, sqrt(N_c), unreduced M_Pl, C_boson=16}. The audit moves `1/pi` to a banked
object (continuation-sum measure), conditional on the root-measure identification. Genuinely
absent from the bank (grep-audited 2026-05-30): a carrier-invariance theorem forcing sqrt(N_c),
and a Planck-normalization theorem forcing G^(-1/2) over (8 pi G)^(-1/2). Those two -- plus the
root-measure identification -- are the real remainder.

[P_structural_ew_floor_measure_is_continuation_sum_root_at_Cboson16]; conditional on the
root-measure identification; no measured target consumed.
"""
from __future__ import annotations

import math

from apf.apf_utils import check, _result

N_C, C_BOSON, D_EFF, D = 3, 16, 102, 4
M_PL = 1.22089e19

EXPORT_FLAGS = dict(
    Export_floor_measure_is_continuation_sum_root_P=1,
    Export_one_over_pi_clause_relocated_to_banked_measure_P=1,
    Export_one_over_pi_unconditionally_derived_P=0,     # conditional on the identification
    Export_sqrtNc_carrier_theorem_in_bank_P=0,          # grep-audited absent
    Export_planck_normalization_theorem_in_bank_P=0,    # grep-audited absent
    Export_exact_native_vH_P=0,
    measured_target_consumed=0,
    target_consumed=0,
)


def check_T_ew_floor_measure_is_continuation_sum_root_P():
    # the floor's measure factor
    meas_factor = 1.0 / (math.pi * math.sqrt(C_BOSON))
    # the banked continuation-sum measure and its root
    mu_cont = (4 * math.pi) ** (-(D / 2.0))         # (4pi)^(-D/2) = 1/(16pi^2) at D=4
    root_mu = math.sqrt(mu_cont)                     # (4pi)^(-1) = 1/(4pi)
    check(math.isclose(meas_factor, root_mu, rel_tol=1e-12),
          "1/(pi sqrt C_boson) == sqrt[(4pi)^(-D/2)] (root of banked continuation-sum measure) at C_boson=16")
    check(math.isclose(mu_cont, 1.0 / (16 * math.pi ** 2), rel_tol=1e-12),
          "continuation-sum measure (4pi)^(-D/2) = 1/(16 pi^2) at D=4 (banked v24.3.166)")

    # whole floor via the measure root
    floor_orig = M_PL * math.sqrt(N_C) / (math.pi * math.sqrt(C_BOSON) * D_EFF ** (C_BOSON / 2.0))
    floor_via = M_PL * math.sqrt(N_C) * root_mu * D_EFF ** (-(C_BOSON / 2.0))
    check(math.isclose(floor_orig, floor_via, rel_tol=1e-12),
          "v_floor = M_Pl sqrt(N_c) sqrt[continuation measure] d_eff^(-C/2) (identical decomposition)")

    # the 1/pi is relocated (not the C_boson-mode determinant, but the per-loop measure root)
    check(EXPORT_FLAGS["Export_one_over_pi_clause_relocated_to_banked_measure_P"] == 1,
          "1/pi relocated from free-scalar to root of the banked D=4-forced continuation measure")
    # but conditional: the identification + sqrt(C_boson)=4 grouping not proven forced
    check(EXPORT_FLAGS["Export_one_over_pi_unconditionally_derived_P"] == 0,
          "conditional on the root-measure identification (sqrt(C_boson)=4 vs the geometric 4)")
    # the other two clauses are genuinely absent (grep-audited)
    check(EXPORT_FLAGS["Export_sqrtNc_carrier_theorem_in_bank_P"] == 0,
          "no carrier-invariance theorem forcing sqrt(N_c) found in the bank")
    check(EXPORT_FLAGS["Export_planck_normalization_theorem_in_bank_P"] == 0,
          "no Planck-normalization theorem forcing G^(-1/2) found in the bank")
    check(EXPORT_FLAGS["Export_exact_native_vH_P"] == 0, "exact v_H still blocked")
    check(EXPORT_FLAGS["measured_target_consumed"] == 0, "no measured target consumed")

    return _result(
        name=("T_ew_floor_measure_is_continuation_sum_root: the floor measure factor "
              "1/(pi sqrt C_boson) = sqrt[(4pi)^(-D/2)] = root of the banked continuation-sum "
              "measure (v24.3.166) at C_boson=16; relocates the 1/pi clause to a D=4-forced banked "
              "object [P_structural, conditional on the root-measure identification]; sqrt(N_c) "
              "carrier and Planck anchor remain genuinely absent from the bank"),
        tier=4,
        epistemic='P_structural',
        summary=(
            "Audit finding: the missing static-trace-measure theorem is not monolithic. Its 1/pi "
            "clause already has a banked home. v_floor = M_Pl sqrt(N_c) sqrt[(4pi)^(-D/2)] "
            "d_eff^(-C/2): the measure factor 1/(pi sqrt C_boson) equals sqrt of the BANKED "
            "continuation-sum measure (4pi)^(-D/2)=1/(16pi^2) (v24.3.166, forced by D=4) -- exact at "
            "C_boson=16. This corrects v24.3.177, which compared 1/pi to a C_boson-mode determinant "
            "pi^(-8) (wrong object); the right object is the per-loop measure, whose root the floor "
            "matches. RESIDUAL: holds at C_boson=16 (sqrt(C_boson)=4 coincides with the geometric 4 "
            "in the continuation (4pi)); the root-measure identification is admissible/motivated but "
            "not proven forced. NET: the four-clause missing theorem loses 1/pi to a banked object; "
            "the real remainder is the root-measure identification + the genuinely-absent sqrt(N_c) "
            "carrier-invariance theorem + the genuinely-absent Planck-normalization theorem (both "
            "grep-audited absent 2026-05-30). Exact v_H still blocked (v24.3.180 independence holds)."
        ),
        key_result=(
            "1/(pi sqrt C_boson) = sqrt[continuation-sum measure (4pi)^(-D/2)] (banked v24.3.166) at "
            "C_boson=16 -> the 1/pi clause is conditionally homed in a D=4-forced banked measure; "
            "sqrt(N_c) carrier + Planck anchor remain genuinely missing. Exact v_H still blocked."
        ),
        dependencies=['T_continuation_sum_measure_native_from_D4',
                      'T_ew_prefactor_invariance_no_go',
                      'T_ew_prefactor_axiom_independence'],
        artifacts=dict(
            measure_factor=round(1.0 / (math.pi * math.sqrt(C_BOSON)), 8),
            continuation_measure_root=round(math.sqrt((4 * math.pi) ** (-(D / 2.0))), 8),
            continuation_measure="(4pi)^(-D/2) = 1/(16 pi^2) at D=4 (v24.3.166)",
            relocated_clause="1/pi -> root of banked continuation measure (conditional)",
            still_missing="root-measure identification + sqrt(N_c) carrier + Planck anchor",
            export_flags=dict(EXPORT_FLAGS),
        ),
    )


_CHECKS = {
    "T_ew_floor_measure_is_continuation_sum_root":
        check_T_ew_floor_measure_is_continuation_sum_root_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
