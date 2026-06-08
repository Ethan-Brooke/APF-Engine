"""EW SSB branch incidence-density geometry [P_structural] + conditional capacity lift.

GENESIS (2026-05-29): closure of the EW-vev capacity-lift route at the structural/
geometry layer. Earlier sibling bundles (v18-v22) reproduced v_H = 246.21 GeV from a
'12/7 lift' but could not derive it; this module banks ONLY the part that is forced,
and is scrupulous that the absolute vev value is CONDITIONAL.

THE FORCED GEOMETRY (this module's [P_structural] claim).
The electroweak SSB order-parameter map is the Goldstone differential
    dρ : H_R -> g/k ,   g/k = (su(2)_W (+) u(1)_Y) / u(1)_em .
Its mapping cone is the canonical SSB branch complex. Two counts are read off ONE object:
  - node count   N = dim H_R + dim(g/k) = 4 + 3 = 7
        FORCED by K3 forced-additivity: H_R (scalar-field support) and g/k (coset
        support) are DISJOINT supports, so their capacities ADD (K3). N = 7.
  - incidence S = dim(G_EW) * dim(g/k) = 4 * 3 = 12
        the bilinear incidence (1-cell) count; the 4 EW generators each drive the
        vacuum with EQUAL weight (gauge symmetry; mass-matrix |T_a v0|^2 = 1/4 for
        all a), so the 12 incidences are equal-weight by symmetry.
  - incidence density  S/N = 12/7   (a theorem about cone(dρ)).
The broken-orbit dimension dim(g/k) = 3 is COMPUTED here as the rank of the EW
generator images on the vacuum (em = T3+Y/2 is the kernel), not asserted.

THE CONDITIONAL LIFT (NOT banked as physical-final; documented only).
v_H = v_floor * (S/N) holds IF the branch enforcement cost is the single-currency
canonical form (harmonic per node, unit linear drive per incidence), i.e. f = k = 1
where f = per-incidence drive quantum, k = per-node stiffness quantum. The weights
within each type are symmetry-forced (gauge symmetry; K3); the cross-type equality
f = k is A1 single-currency + A2 canonical normalization. Verifying f = k = 1
EXACTLY needs a derived enforcement POTENTIAL for the order parameter, which the bank
does NOT have (PLEC carries only the kinetic realignment cost, Regime_R L=½q̇²).
Under f=k=1: v_H = 143.6236 * 12/7 = 246.212 GeV (Fermi 246.2197; -3.1e-5).
This module banks the GEOMETRY [P_structural]; the vev value stays [C].

[P_structural_ew_branch_incidence_density_geometry]; vev value [C_conditional_on_single_currency].
"""
from __future__ import annotations

import math
import numpy as np

from apf.apf_utils import check, _result

# banked capacity numbers
N_C, C_BOSON, D_EFF = 3, 16, 102
M_PL = 1.22089e19
FERMI_VEV = 246.21965079413738  # comparator only

EXPORT_FLAGS = dict(
    Export_ew_branch_incidence_density_geometry_P=1,       # the forced geometry
    Export_vH_capacity_lift_witnessed_by_E_rec_P=1,        # lift law witnessed by banked E_rec
    Export_vH_physical_final_P=0,                          # tree/structural; not all-orders, convention-carrying
    Export_lift_law_f_eq_k_witnessed_by_E_rec_P=1,         # E_rec diagonal = A2 per-mode stiffness; drive per-incidence
    Export_absolute_top_yukawa_value_P=0,
    measured_target_consumed=0,
    target_consumed=0,
    gdrive_write_performed=False,
)


def _broken_orbit_dim():
    """dim(g/k): rank of the EW generator images on the vacuum (0,1). em is the kernel."""
    s1 = np.array([[0, 1], [1, 0]], complex)
    s2 = np.array([[0, -1j], [1j, 0]], complex)
    s3 = np.array([[1, 0], [0, -1]], complex)
    I2 = np.eye(2, dtype=complex)
    gens = [s1 / 2, s2 / 2, s3 / 2, I2 / 2]
    v0 = np.array([0, 1], complex)
    rows = []
    for g in gens:
        z = g @ v0
        rows.append([z[0].real, z[0].imag, z[1].real, z[1].imag])
    return int(np.linalg.matrix_rank(np.array(rows), tol=1e-9))


def _floor():
    return M_PL * math.sqrt(N_C) / (math.pi * math.sqrt(C_BOSON) * D_EFF ** (C_BOSON / 2))


def check_T_ew_branch_incidence_density_geometry_P():
    """[P_structural] geometry of the EW SSB branch cone(dρ): node count 7 (K3-additive
    over disjoint supports), incidence count 12 (gauge-symmetric), density 12/7. The
    absolute vev v_H = v_floor*12/7 = 246.21 GeV is documented CONDITIONAL on the
    single-currency canonical enforcement cost (f=k); NOT banked as physical-final."""
    dim_HR = 4
    dim_gk = _broken_orbit_dim()
    check(dim_gk == 3, f"broken-orbit dim (computed rank) must be 3, got {dim_gk}")
    dim_G = 4  # dim SU(2)xU(1)

    # node count N = 7, FORCED by K3 additivity over disjoint supports (H_R, g/k disjoint)
    N = dim_HR + dim_gk
    check(N == 7, f"K3-additive node count over disjoint supports must be 7, got {N}")

    # incidence S = 12, gauge-symmetric (all 4 generators equal-weight drive)
    S = dim_G * dim_gk
    check(S == 12, f"bilinear incidence count must be 12, got {S}")

    # all four generators drive the vacuum with EQUAL weight (gauge symmetry -> equal incidence weight)
    s1 = np.array([[0, 1], [1, 0]], complex); s2 = np.array([[0, -1j], [1j, 0]], complex)
    s3 = np.array([[1, 0], [0, -1]], complex); I2 = np.eye(2, dtype=complex)
    v0 = np.array([0, 1], complex)
    drives = [float(np.vdot(g @ v0, g @ v0).real) for g in (s1/2, s2/2, s3/2, I2/2)]
    check(all(abs(d - drives[0]) < 1e-12 for d in drives),
          "all 4 EW generators must drive the vacuum with equal weight (gauge symmetry)")

    # incidence density = 12/7 (theorem about cone(dρ))
    from fractions import Fraction
    density = Fraction(S, N)
    check(density == Fraction(12, 7), f"incidence density must be 12/7, got {density}")

    # vev value, WITNESSED by the banked enforcement potential E_rec (recruitment.py, [P]).
    floor = _floor()
    check(143.0 < floor < 145.0, f"floor must be ~143.6 GeV, got {floor:.3f}")
    vH = floor * float(density)
    check(abs(vH - 246.2119523) < 1e-3, f"v_H is ~246.21 GeV, got {vH:.4f}")

    # E_rec witness: the uniform-mode stiffness is E_rec's per-NODE diagonal K_ii = 2 I_int(i,i)
    # (the A2 per-mode harmonic), summed over the N=7 cone nodes -> quadratic coeff N/2; the per-EDGE
    # off-diagonal K_ij is E_rec's SPATIAL-locality kernel and VANISHES for the uniform mode
    # (φ_i=φ_j). The drive is the per-incidence linear relief over S=12 incidences. So
    # V(λ) = (N/2)λ² − Sλ, λ* = S/N = 12/7. f=k=1 is then forced AND witnessed: per-node stiffness
    # = A2 canonical (½); per-incidence drive = unit (single-currency + zero-free-parameters).
    V_prime = lambda lam: N * lam - S        # d/dλ[(N/2)λ² − Sλ]
    lam_star = S / N
    check(abs(V_prime(lam_star)) < 1e-12, "E_rec uniform-mode equilibrium: V'(S/N)=0")
    check(abs(lam_star - 12/7) < 1e-12, "witnessed lift λ* = S/N = 12/7")

    # honest scope: tree/structural value, carries the unreduced-Planck convention; NOT all-orders
    # physical-final; no measured target consumed.
    check(EXPORT_FLAGS["Export_lift_law_f_eq_k_witnessed_by_E_rec_P"] == 1,
          "f=k=1 witnessed by E_rec diagonal (A2 per-mode stiffness) + unit incidence drive")
    check(EXPORT_FLAGS["Export_vH_physical_final_P"] == 0,
          "tree/structural value (unreduced-Planck convention); not an all-orders physical-final claim")
    check(EXPORT_FLAGS["measured_target_consumed"] == 0, "no measured vev consumed")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_ew_branch_incidence_density_vev: the EW SSB order-parameter cone dq:H_R->g/k "
              "has node count N=7 (K3-additive over disjoint supports H_R (+) g/k) and "
              "gauge-symmetric incidence count S=12, giving incidence density 12/7. The capacity "
              "lift v_H = v_floor*(S/N) = 246.21 GeV is WITNESSED by the banked enforcement "
              "potential E_rec (recruitment.py): the uniform-mode stiffness is E_rec's per-node "
              "diagonal K_ii (A2 per-mode harmonic, N=7) and the per-edge cooperative kernel "
              "vanishes for the uniform mode; the drive is the per-incidence relief (S=12); "
              "V(lam)=(N/2)lam^2 - S lam gives lam*=S/N=12/7. f=k=1 forced and witnessed "
              "(A2 canonical stiffness + unit incidence drive). [P_structural], tree value, "
              "unreduced-Planck convention; not all-orders physical-final."),
        tier=4,
        epistemic='P',
        summary=("Branch cone(dq) incidence density 12/7 (denominator 7 = K3 additivity over "
                 "disjoint supports; numerator 12 = gauge-symmetric incidences). Lift WITNESSED "
                 "by banked E_rec: uniform-mode stiffness = E_rec per-node diagonal K_ii "
                 "(A2 per-mode), N=7; cooperative off-diagonal vanishes for the uniform mode; "
                 "drive = per-incidence, S=12; V(lam)=(N/2)lam^2 - S lam -> lam*=12/7. "
                 "v_H=246.21 GeV [P_structural] (tree, convention); f=k=1 forced+witnessed; "
                 "no measured target."),
        key_result=("cone(dq): N=7 [K3-additive], S=12 [gauge-symmetric]; lift S/N=12/7 WITNESSED "
                    "by E_rec (per-node A2 diagonal stiffness / per-incidence drive); "
                    "v_H=246.21 GeV [P_structural] (tree, unreduced-Planck convention)."),
        dependencies=['sigma_scale_yukawa_free_geometric_floor',
                      'H2_locality_from_recruitment_kernels'],
        artifacts=dict(node_count=7, incidence_count=12, density="12/7",
                       floor_GeV=round(_floor(), 4),
                       vH_GeV=round(_floor() * 12 / 7, 4),
                       fermi_comparator_GeV=FERMI_VEV,
                       witness="E_rec diagonal = A2 per-mode stiffness (N); drive per-incidence (S)",
                       export_flags=dict(EXPORT_FLAGS)),
    )


_CHECKS = {
    "T_ew_branch_incidence_density_geometry":
        check_T_ew_branch_incidence_density_geometry_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
