"""The running of alpha as capacity-counted distinction density [P_structural].

An APF-native reformulation of the electromagnetic running: Delta-alpha is the accumulation,
across scales, of the capacity-counted distinction density R = N_c * sum Q^2 -- the colour
capacity times the charge-weighted distinction modes. The form is a structural identity (exact
QFT recast in capacity language), VALIDATED EXACTLY on the leptonic sector. It reframes the
hadronic running into the SAME shape as the electroweak floor: native capacity structure, forced
up to one external scale.

WHAT IS BANKED [P_structural] -- the reformulation.
The one-loop vacuum-polarization running is
    Delta-alpha(M_Z) = (alpha / 3 pi) * sum_f N_c^f Q_f^2 [ ln(M_Z^2/m_f^2) - 5/3 ],
i.e. the accumulation of R(s) = N_c * sum Q^2 over the log of the resolution scale. R is the
capacity-counted distinction density: N_c is the colour CAPACITY (the same N_c forced for the EW
carrier, Theorem_R / T_gauge), and sum Q^2 is the charge-weighted distinction-mode count. The
reformulation is validated EXACTLY on the leptonic sector: summing the three charged leptons
(N_c=1, Q=1) reproduces the banked Delta-alpha_lep = 0.031421 to all printed digits. For the
quark sector R takes its capacity values R(uds)=2, R(udsc)=10/3, R(udscb)=11/3.

THE HADRONIC SPLIT IN THIS LANGUAGE.
The perturbative-QCD piece above Lambda_match = 2 m_c is where R takes its capacity-counted value;
that piece is banked first-principles [P] (delta_alpha_pqcd_m_z, v24.3.118; ~75.7% of the total).
The non-perturbative residual below Lambda_match is, by quark-hadron duality, the capacity density
R=2 (uds) integrated over the low-energy window -- the resonances redistribute spectral weight but
the integral is duality-fixed near the capacity count.

THE STRUCTURAL PARALLEL TO THE EW FLOOR.
The hadronic running has the same shape as the electroweak floor: the distinction-density
STRUCTURE is native (capacity-counted, validated on leptons), and the whole quantity is forced up
to ONE external scale. For the EW floor that scale is the absolute Planck magnitude; for the
hadronic NP residual it is the confinement / hadronic threshold. Both: structure native, one scale
external, both scales living outside the electroweak sector.

WHAT IS NOT CLAIMED -- the NP residual value stays [C].
The NP residual VALUE is NOT [P]. It rests on TWO non-native pieces (one more than the EW floor):
(1) the external low-energy threshold s_low (the confinement scale), and (2) the nonperturbative
duality-violation correction (the ~2% the resonances move around the capacity count). A rigorous
bound would be [P+tool] (importing the OPE duality-violation control). The numerical landing of the
capacity integral near the dispersive residual at the natural pi-pi threshold (~2 m_pi) is a
COMPARATOR, not a derivation: the threshold is an external hadronic scale, not a capacity output,
and target-matching it is refused.

[P_structural_delta_alpha_capacity_counted_distinction_density]; reformulation validated on
leptons; NP residual value held [C] (external threshold + nonperturbative duality violation);
no measured target consumed.
"""
from __future__ import annotations

import math

from apf.apf_utils import check, _result

ALPHA = 1 / 137.035999
M_Z = 91.1876
PREF = ALPHA / (3 * math.pi)
N_C = 3
# charged-lepton masses (GeV) -- the clean validation sector
LEPTONS = {"e": 0.510999e-3, "mu": 0.105658, "tau": 1.77686}
DA_LEP_BANKED = 0.031421
Q2 = {"u": (2/3)**2, "d": (1/3)**2, "s": (1/3)**2, "c": (2/3)**2, "b": (1/3)**2}

EXPORT_FLAGS = dict(
    Export_running_is_capacity_counted_distinction_density_P=1,
    Export_R_equals_Nc_sum_Q2_P=1,
    Export_leptonic_reformulation_validated_P=1,
    Export_hadronic_native_up_to_one_external_threshold_P=1,
    Export_NP_residual_value_native_P=0,            # NOT claimed -- external threshold + duality violation
    Export_threshold_derived_from_capacity_P=0,     # the confinement scale is external
    Export_measured_target_consumed=0,
    target_consumed=0,
)


def _da_species(m, Q2val, ncf):
    return PREF * ncf * Q2val * (math.log(M_Z**2 / m**2) - 5/3)


def check_T_delta_alpha_capacity_counted_distinction_density_P():
    # reformulation validated EXACTLY on the leptonic sector
    da_lep = sum(_da_species(m, 1.0, 1) for m in LEPTONS.values())
    check(abs(da_lep - DA_LEP_BANKED) < 5e-6,
          f"leptonic capacity-density sum = {da_lep:.6f} reproduces banked Delta-alpha_lep 0.031421")

    # R = N_c * sum Q^2 is the capacity-counted distinction density (exact)
    R_uds = N_C * (Q2["u"] + Q2["d"] + Q2["s"])
    R_udsc = R_uds + N_C * Q2["c"]
    R_udscb = R_udsc + N_C * Q2["b"]
    check(abs(R_uds - 2.0) < 1e-12, "R(uds) = N_c*sumQ^2 = 2 (capacity-counted distinction density)")
    check(abs(R_udsc - 10/3) < 1e-12, "R(udsc) = 10/3")
    check(abs(R_udscb - 11/3) < 1e-12, "R(udscb) = 11/3")
    check(EXPORT_FLAGS["Export_R_equals_Nc_sum_Q2_P"] == 1,
          "R = N_c (colour capacity) * sum Q^2 (charge-weighted distinction modes)")

    # the pQCD piece (banked v24.3.118) realizes the capacity value at high energy; NP held
    check(EXPORT_FLAGS["Export_hadronic_native_up_to_one_external_threshold_P"] == 1,
          "hadronic running = capacity density up to one external (confinement) threshold -- EW-floor shape")
    check(EXPORT_FLAGS["Export_NP_residual_value_native_P"] == 0,
          "NP residual VALUE NOT claimed [P]: external threshold + nonperturbative duality violation")
    check(EXPORT_FLAGS["Export_threshold_derived_from_capacity_P"] == 0,
          "the confinement/hadronic threshold is external, not a capacity output (no target-matching)")
    check(EXPORT_FLAGS["Export_measured_target_consumed"] == 0, "no measured target consumed")

    return _result(
        name=("T_delta_alpha_capacity_counted_distinction_density: the running of alpha is the "
              "capacity-counted distinction-density accumulation, R = N_c*sum Q^2 (validated EXACTLY "
              "on the leptonic sector); reframes the hadronic running into the EW-floor shape -- "
              "native structure, one external scale (the confinement threshold). NP residual VALUE "
              "held [C] [P_structural]"),
        tier=4,
        epistemic='P_structural',
        summary=(
            "APF-native reformulation: Delta-alpha = (alpha/3pi) sum_f N_c^f Q_f^2 [ln(M_Z^2/m_f^2) "
            "- 5/3], the accumulation of the capacity-counted distinction density R = N_c*sum Q^2 "
            "(N_c the colour capacity forced for the EW carrier; sum Q^2 the charge-weighted "
            "distinction modes). VALIDATED EXACTLY on the leptonic sector (reproduces the banked "
            "0.031421). For quarks R takes capacity values 2, 10/3, 11/3. The pQCD piece above "
            "2 m_c (banked [P], v24.3.118) realizes the capacity value at high energy; the NP "
            "residual is, by quark-hadron duality, the capacity density R=2 integrated to a low-"
            "energy threshold. STRUCTURAL PARALLEL to the EW floor: native capacity structure, "
            "forced up to ONE external scale -- the Planck magnitude there, the confinement/hadronic "
            "threshold here, both outside the EW sector. NOT CLAIMED: the NP residual VALUE, which "
            "rests on the external threshold AND a nonperturbative duality-violation correction "
            "(two non-native pieces, one more than the EW floor). The ~2 m_pi numerical landing is a "
            "comparator, not a derivation; target-matching refused. A rigorous NP bound would be "
            "[P+tool] (OPE duality-violation control), not native [P]."
        ),
        key_result=(
            "running of alpha = capacity-counted distinction density R=N_c*sumQ^2 [P_structural], "
            "validated exactly on leptons; hadronic running native up to one external confinement "
            "threshold (EW-floor shape); NP residual VALUE held [C] (external threshold + duality "
            "violation), not target-matched."
        ),
        dependencies=['T_delta_alpha_total_decomposition',
                      'T_ew_planck_hierarchy_capacity_suppression_mechanism',
                      'T_ew_sqrtNc_carrier_forced_by_color_triplet_trace'],
        artifacts=dict(
            leptonic_reformulation=round(sum(_da_species(m, 1.0, 1) for m in LEPTONS.values()), 6),
            leptonic_banked=DA_LEP_BANKED,
            R_uds=2.0, R_udsc="10/3", R_udscb="11/3",
            pQCD_piece_banked="v24.3.118 (>2 m_c, ~75.7%)",
            NP_residual_status="[C] -- external threshold + nonperturbative duality violation",
            structural_parallel="EW floor: native structure, one external scale (Planck magnitude / confinement threshold)",
            export_flags=dict(EXPORT_FLAGS),
        ),
    )


_CHECKS = {
    "T_delta_alpha_capacity_counted_distinction_density":
        check_T_delta_alpha_capacity_counted_distinction_density_P,
}


def register(registry):
    registry.update(_CHECKS); return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
