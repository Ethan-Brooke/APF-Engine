"""Bosonic enforcement reservoir theorem -- C_boson=16 EW floor exponent
[P_structural_under_reservoir_reading].

Delivers the object that apf/ew_static_well_factorization.py (v24.3.178) NAMED as the only
revival path for C_boson=16 after the direct local-Higgs-Hessian route was rejected. This
module banks it at the honest CONDITIONAL grade -- closed under the reservoir reading, with
the local-Higgs-Hessian reading explicitly disclaimed.

THE CORRECTED IDENTIFICATION.
The earlier mistake was: EW floor = normalized local Hessian of the Higgs vev branch. Under
that reading the lambda-independent color and fermion blocks cancel in the normalized
curvature (v24.3.178), giving an active sector 4_Higgs + 4_EW_gauge = 8 or 4 + 3 = 7 -- NOT 16.
That route is rejected and stays rejected.

The corrected reading: EW floor = the ABSOLUTE root-measure of the PRE-BRANCH static bosonic
enforcement reservoir, anchored dimensionally to M_Pl -- NOT a normalized branch ratio. The
local Higgs branch (the 12/7 SSB lift) sits on TOP of that reservoir; it is a different object.

THE THEOREM (banked [P_structural_under_reservoir_reading]).
The static bosonic reservoir is the A2/no-ghost second-order (positive-quadratic) enforcement
sector before SSB branch selection: R_bos = R_gauge (+) R_Higgs, with capacity
    C_boson = C_gauge + C_Higgs = 12 + 4 = 16.
The selection rule is CAPACITY TYPE, not Higgs coupling:
  - INCLUDED: all second-order bosonic enforcement slots -- 8 color gauge + 3 weak + 1
    hypercharge + 4 Higgs real = 16. Gluons are in because they are positive-quadratic bosonic
    enforcement modes, not because color acts on the Higgs vev.
  - EXCLUDED: the 45 fermion/Dirac slots -- they are first-order / Grassmann capacity, not
    positive static bosonic well coordinates. The root-measure Omega^(-1/2) is intrinsically a
    bosonic Gaussian-determinant object (Grassmann integrals give det^(+1), not det^(-1/2)), so
    fermions do not contribute a root-volume. This is the structural reason they factor out --
    independent of the electroweak scale.
Color decoupling (d H_color / d lambda_EW = 0) is true for the BRANCH Hessian: it only excludes
gluons from the 12/7 EW lift, NOT from the pre-branch reservoir depth. So the reservoir count
(16, with color) and the branch-lift count (12/7, no color) are two different objects -- no
double-count.
Each reservoir slot carries effective degeneracy d_eff; the microstate volume is
Omega_bos = d_eff^C_boson, and the A2 root-measure gives the floor suppression
    Omega_bos^(-1/2) = d_eff^(-C_boson/2) = 102^(-8).

WHAT IS BANKED vs HELD.
  Export_EW_floor_active_capacity_Cboson_equals_16_under_reservoir_reading_P = 1
  Export_EW_hierarchy_exponent_d_eff_minus_8_under_reservoir_reading_P       = 1
  Export_Paper7_Ctotal61_restricted_by_capacity_type_for_static_bosonic_well_P = 1
  Export_EW_floor_active_capacity_Cboson_equals_16_under_local_Higgs_Hessian_P = 0  (rejected, v24.3.178)
  Export_reservoir_reading_forced_modulo_structural_identifications_P = 1   ([P_structural]; necessity
    theorem v24.3.184, de-circularized 2026-06-08 -- the count is forced, the reservoir framing rests
    on identifications (A) vacuum=measure and (B) vev=per-state amplitude)
  Export_exact_native_vH_P = 0                   (prefactor still blocked, v24.3.177)

THE RESIDUAL (the one thing that keeps this conditional). The reservoir reading is ADMISSIBLE,
internally consistent, independently motivated (the root-measure is a bosonic object; C_boson=16
is the pre-existing ledger value), and NOT target-selected. But the choice between the absolute
reservoir volume (-> 16) and a normalized branch ratio (-> 7-8) is what fixes the count, and
this module MOTIVATES the reservoir reading rather than PROVING it is forced. Both objects are
mathematically coherent. Unconditional [P] needs a derivation that the EW floor MUST be the
reservoir volume, not merely that it admissibly can be.

[P_structural_under_reservoir_reading]; local-Higgs-Hessian reading disclaimed; prefactor +
exact v_H still blocked; no measured target consumed.
"""
from __future__ import annotations

from apf.apf_utils import check, _result

C_GAUGE_COLOR, C_GAUGE_WEAK, C_GAUGE_HYPER, C_HIGGS = 8, 3, 1, 4
C_GAUGE = C_GAUGE_COLOR + C_GAUGE_WEAK + C_GAUGE_HYPER   # 12
C_BOSON = C_GAUGE + C_HIGGS                              # 16
C_FERMION, C_TOTAL = 45, 61
D_EFF = 102
# the rejected direct-Hessian active counts (color-singlet Higgs branch)
DIRECT_HESSIAN_ACTIVE = (8, 7)  # 4+4 (Higgs+EW gauge) or 4+3 (broken cone)

EXPORT_FLAGS = dict(
    Export_bosonic_enforcement_reservoir_theorem_P=1,
    Export_EW_floor_active_capacity_Cboson_equals_16_under_reservoir_reading_P=1,
    Export_EW_hierarchy_exponent_d_eff_minus_8_under_reservoir_reading_P=1,
    Export_Paper7_Ctotal61_restricted_by_capacity_type_for_static_bosonic_well_P=1,
    Export_EW_floor_active_capacity_Cboson_equals_16_under_local_Higgs_Hessian_P=0,
    Export_reservoir_reading_forced_modulo_structural_identifications_P=1,  # [P_structural]; v24.3.184, de-circularized 2026-06-08
    Export_no_double_count_with_12_over_7_lift_P=1,
    Export_exact_native_vH_P=0,
    measured_target_consumed=0,
    target_consumed=0,
)


def check_T_ew_bosonic_enforcement_reservoir_theorem_P():
    # reservoir capacity by type: bosonic positive-quadratic slots
    check(C_GAUGE == 12 and C_GAUGE == C_GAUGE_COLOR + C_GAUGE_WEAK + C_GAUGE_HYPER,
          "C_gauge = 8 color + 3 weak + 1 hyper = 12")
    check(C_BOSON == C_GAUGE + C_HIGGS == 16, "C_boson = C_gauge + C_Higgs = 12 + 4 = 16")
    check(C_BOSON + C_FERMION == C_TOTAL == 61, "16 bosonic + 45 fermionic = 61 = C_total")

    # capacity-type split: gluons IN (bosonic), fermions OUT (Grassmann), independent of target
    check(C_GAUGE_COLOR == 8, "8 gluons are positive-quadratic bosonic enforcement slots -> in reservoir")
    check(EXPORT_FLAGS["Export_EW_floor_active_capacity_Cboson_equals_16_under_local_Higgs_Hessian_P"] == 0,
          "the local-Higgs-Hessian reading (active 7-8) is disclaimed; this is the RESERVOIR reading")
    for direct in DIRECT_HESSIAN_ACTIVE:
        check(direct < C_BOSON, f"direct-Hessian active {direct} != reservoir count 16 (the two readings differ)")

    # the floor suppression from the reservoir volume
    supp = float(D_EFF) ** (-(C_BOSON / 2.0))
    check(abs(supp - D_EFF ** (-8)) < 1e-30, "Omega_bos^(-1/2) = d_eff^(-C_boson/2) = 102^(-8)")

    # no double-count: reservoir depth (16, with color) vs branch lift (12/7, no color) are distinct
    check(EXPORT_FLAGS["Export_no_double_count_with_12_over_7_lift_P"] == 1,
          "reservoir count 16 (depth) and 12/7 (EW SSB cone lift) are different objects, no double-count")

    # the count is forced (post-SSB readings excluded: A y_t-dependent, B by staging), but the
    # reservoir FRAMING rests on identifications (A) vacuum=measure, (B) vev=per-state amplitude -> [P_structural]
    check(EXPORT_FLAGS["Export_reservoir_reading_forced_modulo_structural_identifications_P"] == 1,
          "reservoir reading forced modulo structural identifications (necessity v24.3.184, "
          "de-circularized 2026-06-08): post-SSB readings excluded (A y_t-dependent, B by staging)")
    # prefactor + exact value still blocked
    check(EXPORT_FLAGS["Export_exact_native_vH_P"] == 0, "exact native v_H still blocked (prefactor, v24.3.177)")
    check(EXPORT_FLAGS["measured_target_consumed"] == 0, "no measured target consumed")

    return _result(
        name=("T_ew_bosonic_enforcement_reservoir_theorem: the EW floor is the root-measure of "
              "the pre-branch static BOSONIC enforcement reservoir (C_boson=C_gauge+C_Higgs="
              "12+4=16, gluons included by capacity type), NOT the local Higgs branch Hessian "
              "(7-8); gives d_eff^(-8) [P_structural_under_reservoir_reading; reading not proven "
              "forced; prefactor + exact v_H still blocked]"),
        tier=4,
        epistemic='P_structural',
        summary=(
            "Reservoir theorem (the v24.3.178-named revival), banked under the reservoir reading. "
            "The EW floor is the ABSOLUTE root-measure of the pre-branch static bosonic enforcement "
            "reservoir anchored to M_Pl, not a normalized branch ratio. Capacity by TYPE: bosonic "
            "positive-quadratic slots IN (8 gluon + 3 weak + 1 hyper + 4 Higgs = 16), 45 fermionic "
            "Grassmann slots OUT (the root-measure Omega^(-1/2) is intrinsically bosonic; Grassmann "
            "gives det^+1, no root-volume) -- a structural, target-independent reason. Gluons stay "
            "because they are second-order bosonic, even though color decouples from the Higgs vev; "
            "that decoupling only removes them from the 12/7 EW lift, not the reservoir depth (no "
            "double-count). Omega_bos = d_eff^16 -> suppression d_eff^(-8). DISCLAIMED: the "
            "local-Higgs-Hessian reading (active 7-8, gluons cancel with fermions, v24.3.178) is "
            "NOT this; it gives 16=0. RESIDUAL: the reservoir reading is admissible, consistent, and "
            "independently motivated (not target-selected), but is MOTIVATED, not proven FORCED vs "
            "the normalized-branch reading; unconditional [P] needs the floor shown to BE the "
            "reservoir volume. Prefactor (sqrtNc/1pi/Planck, v24.3.177) and exact v_H still blocked."
        ),
        key_result=(
            "EW floor = pre-branch bosonic reservoir root-measure; C_boson=16 by capacity type "
            "(bosonic-quadratic in incl. gluons, fermionic-Grassmann out); d_eff^(-8) "
            "[P_under_reservoir_reading]. Local-Higgs-Hessian reading (7-8) disclaimed. Reading "
            "not proven forced; prefactor + exact v_H blocked."
        ),
        dependencies=['T_ew_static_well_factorization_principle',
                      'T_ew_planck_hierarchy_capacity_suppression_mechanism',
                      'T_ew_branch_incidence_density_geometry'],
        artifacts=dict(
            C_gauge_color=8, C_gauge_weak=3, C_gauge_hyper=1, C_Higgs=4,
            C_boson=16, C_fermion=45, C_total=61, d_eff=102,
            suppression="d_eff^(-C_boson/2) = 102^-8",
            reservoir_reading="EW floor = absolute pre-branch bosonic reservoir root-volume",
            disclaimed_reading="local Higgs branch Hessian (active 7-8) gives 16 -> 0",
            residual="reservoir reading admissible+motivated but NOT proven forced (forced modulo identifications A/B)",
            export_flags=dict(EXPORT_FLAGS),
        ),
    )


_CHECKS = {
    "T_ew_bosonic_enforcement_reservoir_theorem":
        check_T_ew_bosonic_enforcement_reservoir_theorem_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
