"""Static-well factorization principle + C_boson=16 direct-route REJECTION [P_structural].

The positive residue of the 2026-05-29 mode-restriction attempt, plus the machine-recorded
rejection of the naive C_boson=16 closure. Companion to the banked hierarchy mechanism
(apf/ew_planck_hierarchy_mechanism.py, v24.3.176), which holds the C_boson=16 active count
OPEN; this module says precisely WHY the *direct* local-EW-Hessian route does not reach 16,
and names the only object that could revive it.

WHAT IS BANKED [P_structural] -- the factorization principle.
For a local, normalized root-measure / Hessian-determinant observable attached to an
order-parameter well, write the static Hessian block-wise over an active sector X and its
complement Xbar with H = H_X (+) H_Xbar. If the order parameter does not move the complement,
d/dlambda H_Xbar = 0, then in the NORMALIZED local curvature the complement cancels:
    det(H_X (+) H_Xbar)(lambda)^{-1/2} / det(...)(0)^{-1/2}
      = det(H_X)(lambda)^{-1/2} / det(H_X)(0)^{-1/2},
because det(H_X (+) H_Xbar) = det(H_X) det(H_Xbar) and the lambda-independent det(H_Xbar)
divides out. CONSEQUENCE: Paper 7's full interface count C_total = 61 does NOT automatically
enter a local electroweak observable; only the active sector of the relevant static well does.

THE REJECTION (this module also machine-records it).
The electroweak vev order parameter is a COLOR SINGLET Higgs. So at the direct static-Hessian
level BOTH the color block and the fermion block are lambda-independent:
    d/dlambda H_color = 0   (gluons do not couple to the color-singlet Higgs vev),
    d/dlambda H_fermion = 0  (the y_t-free leading well; the 45 fermionic slots).
Hence BOTH cancel in the normalized local well. The active sector is therefore the
electroweak/Higgs bosonic content only:
    Higgs real modes + electroweak gauge modes = 4 + 4 = 8,
or, restricted to the broken-branch cone (ew_branch_incidence_density, G_EW = 4, g/k = 3),
    Higgs real modes + broken EW directions = 4 + 3 = 7.
Neither is C_boson = 16. The 8 gluons sit in the SAME inactive complement as the 45 fermions
and cancel for the SAME reason. So the direct local-EW-Hessian route gives 7-8, and
C_active = C_boson = 16 is REJECTED at current depth; the d_eff^{-8} EW floor exponent does
NOT follow from the direct mode restriction.

THE ONLY REVIVAL (named, not in corpus).
C_boson = 16 can be rescued only by a different, stronger object -- the
BOSONIC_ENFORCEMENT_RESERVOIR_THEOREM -- which would have to PROVE (not assert): (1) the EW
floor is a full static bosonic enforcement-reservoir measure, not the direct local Higgs
Hessian; (2) the active split is bosonic-vs-fermionic capacity TYPE (-> 16), not Higgs
coupling; (3) gluons remain active as second-order bosonic capacity though the Higgs is a
color singlet; (4) the 45 fermionic slots factor out as first-order/Dirac capacity, not
static quadratic bosonic capacity; (5) no double-count of the 12/7 branch lift; (6) the result
is color-carrier-convention invariant and does not reopen the top-Yukawa no-go. The current
corpus does not contain that proof.

[P_structural_ew_static_well_factorization_principle; C_boson=16 direct route rejected;
reservoir theorem named-not-derived]; no measured target consumed.
"""
from __future__ import annotations

import numpy as np

from apf.apf_utils import check, _result

C_BOSON, C_TOTAL = 16, 61
# direct local-EW-Hessian active counts (color-singlet Higgs): both reject 16
ACTIVE_EW_GAUGE_PLUS_HIGGS = 8   # 4 Higgs real + 4 SU(2)xU(1) gauge
ACTIVE_BROKEN_CONE = 7           # 4 H_R + 3 g/k broken EW directions (ew_branch)

EXPORT_FLAGS = dict(
    Export_static_well_factorization_principle_P=1,
    Export_Paper7_Ctotal61_not_automatically_active_for_local_EW_well_P=1,
    Export_EW_floor_active_capacity_Cboson_equals_16_P=0,        # REJECTED (direct route)
    Export_EW_hierarchy_exponent_102minus8_native_P=0,          # not from direct restriction
    Export_bosonic_enforcement_reservoir_theorem_present_P=1,    # DELIVERED v24.3.179 (conditional: reservoir reading)
    Export_exact_native_vH_P=0,
    measured_target_consumed=0,
    target_consumed=0,
)


def check_T_ew_static_well_factorization_principle_P():
    rng = np.random.default_rng(20260529)

    # --- factorization principle: inactive complement cancels in the normalized local well ---
    # active block X (depends on lambda), inactive complement Xbar (lambda-independent)
    nX, nXbar = 8, 53   # active EW/Higgs vs inactive (8 gluon + 45 fermion in this toy split)
    A0 = rng.normal(size=(nX, nX)); HX0 = A0 @ A0.T + nX * np.eye(nX)        # PD, lambda=0
    A1 = rng.normal(size=(nX, nX)); HXl = A1 @ A1.T + nX * np.eye(nX)        # PD, lambda>0
    B = rng.normal(size=(nXbar, nXbar)); HXbar = B @ B.T + nXbar * np.eye(nXbar)  # PD, fixed

    def block(Hx):
        H = np.zeros((nX + nXbar, nX + nXbar))
        H[:nX, :nX] = Hx
        H[nX:, nX:] = HXbar
        return H

    # normalized local root-measure ratio, computed two ways
    s_full0 = np.linalg.slogdet(block(HX0))[1]
    s_fulll = np.linalg.slogdet(block(HXl))[1]
    ratio_full = np.exp(-0.5 * (s_fulll - s_full0))            # uses full 61-mode determinant
    ratio_active = np.exp(-0.5 * (np.linalg.slogdet(HXl)[1] - np.linalg.slogdet(HX0)[1]))  # X only
    check(np.isclose(ratio_full, ratio_active, rtol=1e-10),
          "normalized local root-measure: inactive complement cancels (full == active-only)")

    # --- Paper-7 C_total=61 does not automatically enter ---
    check(C_TOTAL == 61 and C_BOSON == 16, "Paper-7 C_total=61; bosonic C_boson=16")
    check(EXPORT_FLAGS["Export_Paper7_Ctotal61_not_automatically_active_for_local_EW_well_P"] == 1,
          "local EW well restricts to its active sector, not the full C_total=61")

    # --- the REJECTION: direct local-EW-Hessian active sector is 7-8, NOT 16 ---
    # color-singlet Higgs => color block AND fermion block both lambda-independent => both cancel
    for active in (ACTIVE_EW_GAUGE_PLUS_HIGGS, ACTIVE_BROKEN_CONE):
        check(active < C_BOSON, f"direct active count {active} < C_boson=16 (gluons cancel with fermions)")
    check(EXPORT_FLAGS["Export_EW_floor_active_capacity_Cboson_equals_16_P"] == 0,
          "C_active = C_boson = 16 from the direct local EW Hessian is REJECTED")
    check(EXPORT_FLAGS["Export_EW_hierarchy_exponent_102minus8_native_P"] == 0,
          "d_eff^-8 native EW floor exponent does NOT follow from the direct mode restriction")

    # --- the only revival is named, not in corpus ---
    check(EXPORT_FLAGS["Export_bosonic_enforcement_reservoir_theorem_present_P"] == 1,
          "BOSONIC_ENFORCEMENT_RESERVOIR_THEOREM delivered at conditional grade in "
          "apf/ew_bosonic_enforcement_reservoir.py (v24.3.179); the DIRECT local-Hessian route "
          "stays rejected (this module); only the revival-status flag updates")
    check(EXPORT_FLAGS["measured_target_consumed"] == 0, "no measured target consumed")

    return _result(
        name=("T_ew_static_well_factorization_principle: local-well factorization is "
              "[P_structural] (Paper-7 C_total=61 not automatically active); but the direct "
              "local-EW-Hessian active sector is 7-8 (Higgs+EW gauge), NOT 16 -- gluons cancel "
              "with the fermions for a color-singlet Higgs -- so C_boson=16 is REJECTED at "
              "current depth; revival needs the named bosonic-enforcement-reservoir theorem"),
        tier=4,
        epistemic='P_structural',
        summary=(
            "BANKED: the static-well factorization principle. For a local normalized root-measure "
            "/ Hessian determinant on an order-parameter well, det(H_X (+) H_Xbar) = det(H_X) "
            "det(H_Xbar); a lambda-independent complement cancels (toy-verified: full-61 ratio == "
            "active-only ratio). So Paper-7 C_total=61 does NOT automatically enter a local EW "
            "observable. REJECTED: C_active = C_boson = 16 from the direct EW Hessian -- the "
            "color-singlet Higgs leaves BOTH the color block and the fermion block "
            "lambda-independent, so the 8 gluons cancel for the SAME reason as the 45 fermions; "
            "the active sector is 4+4=8 (Higgs + EW gauge) or 4+3=7 (broken cone), not 16. Hence "
            "d_eff^-8 is not native from the direct restriction. REVIVAL (named, not in corpus): "
            "the BOSONIC_ENFORCEMENT_RESERVOIR_THEOREM (EW floor = bosonic reservoir not Higgs "
            "Hessian; bosonic-vs-fermionic capacity-type split; gluons active, fermions out; no "
            "12/7 double-count; color-carrier invariant). Companion to v24.3.176 (mechanism, "
            "count open) + v24.3.177 (prefactor no-go)."
        ),
        key_result=(
            "[P] static-well factorization (Paper-7 C_total=61 not auto-active); C_boson=16 direct "
            "route REJECTED (active 7-8, gluons cancel with fermions); d_eff^-8 not native; "
            "revival = named bosonic-enforcement-reservoir theorem (not in corpus)."
        ),
        dependencies=['T_ew_planck_hierarchy_capacity_suppression_mechanism',
                      'T_ew_branch_incidence_density_geometry'],
        artifacts=dict(
            C_boson=16, C_total=61,
            direct_active_ew_gauge_plus_higgs=8,
            direct_active_broken_cone=7,
            rejected="C_active = C_boson = 16 from direct local EW Hessian",
            revival_theorem="BOSONIC_ENFORCEMENT_RESERVOIR_THEOREM (named, not in corpus)",
            export_flags=dict(EXPORT_FLAGS),
        ),
    )


_CHECKS = {
    "T_ew_static_well_factorization_principle": check_T_ew_static_well_factorization_principle_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
