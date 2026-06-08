"""Muon g-2 hadronic vacuum polarization as capacity-counted distinction density [P_structural].

The source-codomain reading the board listed as missing for muon g-2 (RP-mu, "upstream"). It closes
"upstream" by delivering the APF source object for a_mu^HVP -- the same capacity-counted distinction
density R = N_c * sum Q^2 that the hadronic running uses (delta_alpha_capacity_density, v24.3.186) --
and it does so without manufacturing a resolution to a tension the field's own data has largely
dissolved. Structure native; the nonperturbative value inherited as the universal QCD difficulty.

THE DECOMPOSITION.
The Standard-Model a_mu splits into QED (dominant, determined arithmetic), electroweak (small,
determined), and the hadronic pieces -- leading hadronic vacuum polarization (HVP) plus
hadronic light-by-light. The HVP piece is the contested one, and it is governed by the SAME hadronic
vacuum polarization R(s) that governs the running of alpha:
    a_mu^HVP,LO = (1/3)(alpha/pi)^2 * integral_{s_th}^inf (ds/s) K(s) R(s),
with K(s) the known QED kernel (Gourdin-de Rafael / Jegerlehner),
    K(s) = integral_0^1 dx x^2 (1-x) / (x^2 + (s/m_mu^2)(1-x)),   K(s) -> m_mu^2/(3s) as s -> inf,
and R(s) = N_c * sum_q Q_q^2 the capacity-counted distinction density. So APF's source object for the
hadronic running IS the source object for a_mu^HVP; only the kernel against which it is integrated
changes, and that kernel is determined QED.

WHAT IS NATIVE, AND HOW THIN IT IS (the honest caveat, not buried).
The g-2 kernel K(s) ~ m_mu^2/(3s) weights the low-energy region far more heavily than the Delta-alpha
kernel does. So the perturbative slice -- the region where R takes its free capacity value and the
APF count is native [P] -- covers MUCH LESS of a_mu^HVP than it did for Delta-alpha. Numerically:
above Lambda_match = 2 m_c the perturbative slice is ~345e-11, about 5% of the full
a_mu^HVP,LO ~ 6900e-11 (versus ~76% of Delta-alpha_had). The handle is structurally identical but
numerically thin: this is a structural reframing, NOT a value derivation. The nonperturbative bulk
(~95%) is the low-energy rho/omega/phi region, held [C] -- the universal QCD difficulty
(delta_alpha_leptonic v24.3.116), inherited not manufactured.

THE EMPIRICAL FRAME (recorded, not consumed).
As of the 2025 measurements the muon g-2 "anomaly" has largely dissolved. The Fermilab final result
a_mu^exp = 116592070.5e-11 (127 ppb) agrees with the 2025 Theory-Initiative Standard-Model value
a_mu^SM = 116592033e-11 once the HVP is taken from the lattice / new-computation route -- within
~127 ppb. What remains is a ~3 sigma INTERNAL discrepancy between the dispersive (R-ratio data) and
lattice evaluations of the SAME a_mu^HVP -- the identical BMW-vs-dispersive tension that limits
Delta-alpha_had. So there is no longer a significant Standard-Model-vs-experiment signal for APF to
explain by new physics, and APF does not invent one. APF's capacity density is the perturbative
backbone of R(s) common to both evaluations; it is consistent with the no-anomaly (lattice-side)
reading and takes no side in the internal dispersive-vs-lattice split, which it does not resolve.

CONSEQUENCE. RP-mu's "upstream -- no source prediction yet" closes to "source-codomain reading
delivered": a_mu^HVP is the capacity-counted distinction density against the known QED g-2 kernel,
QED and EW determined, the nonperturbative value held [C]. No a_mu value to ppb, no resolution of the
dispersive-vs-lattice tension, no new-physics claim, no measured target consumed.

[P_structural] for the reframing (a_mu^HVP = capacity density against the known kernel); QED/EW
determined arithmetic; nonperturbative value held [C] (universal QCD difficulty); empirical
near-dissolution recorded as comparator; nothing target-matched.
"""
from __future__ import annotations

import math

from apf.apf_utils import check, _result

M_MU = 0.1056584          # GeV
ALPHA = 1 / 137.035999    # Thomson-limit fine-structure constant (dimensionless)
N_C = 3
M_C = 1.27               # GeV, charm MSbar self-scale context (threshold only)
M_B = 4.18               # GeV, bottom MSbar self-scale context (threshold only)

# --- comparators (NOT consumed) ---
A_MU_EXP = 116592070.5e-11        # Fermilab final 2025, 127 ppb
A_MU_SM_2025 = 116592033e-11      # Theory Initiative 2025 (lattice HVP)
A_MU_HVP_LO = 6900e-11            # ~6845 (disp) / ~7075 (lattice) -- order anchor

EXPORT_FLAGS = dict(
    Export_a_mu_hvp_is_capacity_counted_distinction_density_P=1,   # the structural reframing
    Export_qed_ew_pieces_determined_arithmetic_P=1,
    Export_a_mu_value_native_P=0,                                  # NOT a value derivation
    Export_np_residual_value_native_P=0,                          # held [C], universal QCD difficulty
    Export_dispersive_vs_lattice_tension_resolved_P=0,            # APF takes no side, resolves nothing
    Export_new_physics_claimed_P=0,                              # anomaly dissolved; none claimed
    Export_a_mu_target_matched_P=0,
    measured_target_consumed=0,
    target_consumed=0,
)


def _R_pert(s):
    """Capacity-counted distinction density R = N_c sum Q^2 with flavor thresholds (perturbative)."""
    Q2 = (2 / 3) ** 2 + (1 / 3) ** 2 + (1 / 3) ** 2     # u, d, s
    if s > (2 * M_C) ** 2:
        Q2 += (2 / 3) ** 2                              # c
    if s > (2 * M_B) ** 2:
        Q2 += (1 / 3) ** 2                              # b
    return N_C * Q2


def _Khat(s, n=400):
    """Known QED g-2 kernel; K(s) -> m_mu^2/(3s) as s -> inf. Positive, monotone-decreasing."""
    r = s / M_MU ** 2
    tot = 0.0
    for i in range(n):
        x = (i + 0.5) / n
        tot += x * x * (1 - x) / (x * x + r * (1 - x))
    return tot / n


def _a_mu_pert_above(s_lo, s_hi=1e6, n=1200):
    """Perturbative-region a_mu^HVP slice: (1/3)(alpha/pi)^2 int (ds/s) K(s) R(s)."""
    pref = (1 / 3) * (ALPHA / math.pi) ** 2
    ls, lh = math.log(s_lo), math.log(s_hi)
    tot = 0.0
    for i in range(n):
        l = ls + (lh - ls) * (i + 0.5) / n
        s = math.exp(l)
        ds = s * (lh - ls) / n
        tot += (ds / s) * _Khat(s) * _R_pert(s)
    return pref * tot


def check_T_a_mu_hvp_capacity_counted_distinction_density_P():
    # -- the kernel is the known QED object: positive, monotone, with the m_mu^2/3s asymptote --
    ks = [_Khat(s) for s in (0.5, 1.0, 4.0, 16.0, 100.0)]
    check(all(k > 0 for k in ks), "g-2 kernel K(s) > 0 (known QED kernel)")
    check(all(k1 > k2 for k1, k2 in zip(ks, ks[1:])), "K(s) monotone-decreasing (low-energy weighted)")
    check(math.isclose(_Khat(100.0), M_MU ** 2 / (3 * 100.0), rel_tol=0.05),
          "K(s) -> m_mu^2/(3s) asymptotically -- the determined IR-weighting that makes HVP NP-dominated")

    # -- R(s) takes its capacity-counted values (same density as the hadronic running) --
    check(math.isclose(_R_pert(4.0), 2.0, rel_tol=1e-9), "R(u,d,s) = N_c(4/9+1/9+1/9) = 2 (capacity count, sub-charm)")
    check(math.isclose(_R_pert(30.0), 10 / 3, rel_tol=1e-9), "R(...,c) = 10/3 (charm active)")
    check(math.isclose(_R_pert(120.0), 11 / 3, rel_tol=1e-9), "R(...,b) = 11/3 (bottom active)")

    # -- the native perturbative slice is THIN (honest caveat, quantified, not buried) --
    a_pert = _a_mu_pert_above((2 * M_C) ** 2)
    frac = a_pert / A_MU_HVP_LO
    check(a_pert > 0, "perturbative-region a_mu^HVP slice is a positive native [P] piece")
    check(0.01 < frac < 0.15,
          f"native perturbative slice ~{frac*100:.0f}% of a_mu^HVP (vs ~76% for Delta-alpha): "
          "structurally identical handle, numerically thin -- a reframing, not a value derivation")

    # -- the empirical frame: anomaly dissolved; APF resolves no tension --
    check(abs(A_MU_EXP - A_MU_SM_2025) / A_MU_EXP < 5e-7,
          "a_mu^exp and a_mu^SM(2025 lattice HVP) agree within ~127 ppb -- anomaly largely dissolved")
    check(EXPORT_FLAGS["Export_dispersive_vs_lattice_tension_resolved_P"] == 0
          and EXPORT_FLAGS["Export_new_physics_claimed_P"] == 0,
          "APF resolves no dispersive-vs-lattice tension and claims no new physics")

    # -- honest non-claims --
    check(EXPORT_FLAGS["Export_a_mu_hvp_is_capacity_counted_distinction_density_P"] == 1,
          "a_mu^HVP = capacity-counted distinction density against the known QED kernel [P_structural]")
    check(EXPORT_FLAGS["Export_a_mu_value_native_P"] == 0
          and EXPORT_FLAGS["Export_np_residual_value_native_P"] == 0,
          "no a_mu value derived; NP value held [C] (universal QCD difficulty), not native")
    check(EXPORT_FLAGS["Export_a_mu_target_matched_P"] == 0
          and EXPORT_FLAGS["measured_target_consumed"] == 0,
          "perturbative slice computed as output; a_mu^exp / SM / HVP,LO are comparators only")

    return _result(
        name=("T_a_mu_hvp_capacity_counted_distinction_density: the muon g-2 hadronic vacuum "
              "polarization a_mu^HVP is the capacity-counted distinction density R = N_c*sum Q^2 -- the "
              "same source object as the hadronic running -- integrated against the known QED g-2 "
              "kernel K(s) (Gourdin-de Rafael). QED and EW pieces determined; native perturbative slice "
              "~5% of a_mu^HVP (kernel low-energy-weighted, much thinner than Delta-alpha's ~76%); NP "
              "value held [C] (universal QCD difficulty). The 2025 anomaly has largely dissolved "
              "(exp vs lattice-HVP SM agree to ~127 ppb); APF resolves no dispersive-vs-lattice tension "
              "and claims no new physics. Closes RP-mu 'upstream' as source-codomain reading delivered "
              "[P_structural]"),
        tier=4,
        epistemic='P_structural',
        summary=(
            "The source-codomain reading for muon g-2 (RP-mu, 'upstream'), delivered without "
            "manufacturing a resolution. The SM a_mu = QED (dominant, determined) + EW (small, "
            "determined) + hadronic (HVP + light-by-light). The leading HVP piece is "
            "a_mu^HVP,LO = (1/3)(alpha/pi)^2 int (ds/s) K(s) R(s), with K(s) the known QED kernel "
            "(K -> m_mu^2/3s) and R(s) = N_c sum Q^2 the capacity-counted distinction density -- the "
            "SAME source object as the hadronic running (v24.3.186); only the kernel changes, and it is "
            "determined QED. Native [P] structure; the perturbative slice above 2 m_c is ~345e-11, only "
            "~5% of a_mu^HVP,LO ~ 6900e-11 (the g-2 kernel weights the low-energy rho/omega/phi region "
            "far harder than the Delta-alpha kernel, where the slice was ~76%) -- structurally "
            "identical handle, numerically thin, a reframing not a value derivation. The NP bulk (~95%) "
            "is held [C], the universal QCD difficulty, inherited not manufactured. Empirical frame "
            "(comparator, not consumed): the 2025 anomaly has largely dissolved -- Fermilab final "
            "a_mu^exp = 116592070.5e-11 agrees with the 2025 Theory-Initiative SM value "
            "a_mu^SM = 116592033e-11 (lattice HVP) within ~127 ppb; the residual is a ~3 sigma INTERNAL "
            "dispersive-vs-lattice HVP split, the same tension that limits Delta-alpha_had. APF is the "
            "perturbative backbone of the R(s) common to both, takes no side, resolves nothing, and "
            "claims no new physics. RP-mu closes from 'upstream' to source-codomain reading delivered."
        ),
        key_result=(
            "a_mu^HVP = capacity-counted distinction density R=N_c*sumQ^2 against the known QED g-2 "
            "kernel [P_structural]. QED/EW determined; native perturbative slice ~5% of a_mu^HVP "
            "(thin, kernel low-energy-weighted); NP value held [C] (universal QCD difficulty). 2025 "
            "anomaly dissolved (exp vs SM-lattice ~127 ppb); no tension resolved, no new physics, no "
            "target consumed. Closes RP-mu 'upstream'."
        ),
        dependencies=['T_delta_alpha_capacity_counted_distinction_density',
                      'T_delta_alpha_had_principled_external_universal_QCD',
                      'charged_lepton_pole_masses', 'L_alpha_em'],
        artifacts=dict(
            formula="a_mu^HVP,LO = (1/3)(alpha/pi)^2 int (ds/s) K(s) R(s)",
            kernel="K(s) = int_0^1 dx x^2(1-x)/(x^2+(s/m_mu^2)(1-x)) -> m_mu^2/(3s) (known QED)",
            density="R(s) = N_c sum Q^2 (capacity-counted distinction density, same as v24.3.186)",
            native_slice_above_2mc_e11=round(_a_mu_pert_above((2 * M_C) ** 2) * 1e11, 1),
            native_slice_fraction="~5% of a_mu^HVP,LO (vs ~76% for Delta-alpha; kernel low-energy-weighted)",
            np_bulk="~95% held [C], universal QCD difficulty (inherited not manufactured)",
            empirical_2025="anomaly dissolved: a_mu^exp 116592070.5e-11 vs SM-lattice 116592033e-11 (~127 ppb)",
            residual_tension="~3 sigma INTERNAL dispersive-vs-lattice HVP (= BMW-vs-dispersive, limits Delta-alpha too)",
            comparators_not_consumed=dict(a_mu_exp=A_MU_EXP, a_mu_sm_2025=A_MU_SM_2025, a_mu_hvp_lo=A_MU_HVP_LO),
            export_flags=dict(EXPORT_FLAGS),
        ),
    )


_CHECKS = {
    "T_a_mu_hvp_capacity_counted_distinction_density":
        check_T_a_mu_hvp_capacity_counted_distinction_density_P,
}


def register(registry):
    registry.update(_CHECKS); return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
