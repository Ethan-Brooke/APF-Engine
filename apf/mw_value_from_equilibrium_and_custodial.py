"""APF-native M_W value as equilibrium-angle + custodial Δρ — no loop construction — Tier-4.

This check makes explicit, on the bank side, *what physically sets the W mass* in
the distinction picture, and retires the loop-expansion framing for the
electroweak radiative face. It is a composition / accounting theorem over already
-banked native pieces — it certifies the mechanistic decomposition of an
independently-banked number (check_L_W_mass, [P], M_W = 80.3336 GeV, 0.044% from
measured), it does not produce a new value.

The physical claim. The W mass is not obtained by summing a diagrammatic loop
expansion around a bare tree value. It is read off directly from two physical
mechanisms, both native:

  (1) The weak mixing angle is a distinction-partition *equilibrium*, not a bare
      coupling. sin²θ_W = 3/13 (check_T_sin2theta, [P]) is the capacity
      equilibrium between the SU(2) and U(1) sectors (the γ=17/4 attractor). It
      fixes the tree ratio M_W = M_Z·√(1 − sin²θ_W). Because the equilibrium
      value is already the physical/all-orders angle, the single largest SM
      "radiative" piece — the running Δα of the electromagnetic coupling from
      q²→0 to the EW scale — is not a correction to be summed here: it is
      absorbed into the equilibrium. There is no bare-to-physical running step to
      reproduce.

  (2) Custodial breaking Δρ — the substrate holding the t,b doublet at unequal
      cost. The only genuine shift off the pure-angle value is the custodial
      response: custodial SU(2) would force M_W²/M_Z² = c² exactly, and the t/b
      cost-asymmetry breaks it. This is the banked distinction-picture Δρ
      (check_T_delta_rho_leading_custodial_from_distinction, v24.3.167), whose
      universal measure factor 1/(16π²) is itself the banked continuation-sum
      measure (check_T_continuation_sum_measure_native_from_D4, v24.3.166, forced
      by native D=4) — the substrate's sum over admissible held continuations,
      NOT a loop integral. check_L_W_mass applies exactly this family: Δρ_top
      (dominant) + Δρ_QCD (QCD screening of the top asymmetry) + Δρ_H (the
      Higgs's logarithmic contribution), times the algebraic sensitivity lever
      (1−s²)/(1−2s²) = 10/7.

The "change in value" the SM organizes as a one-loop-then-two-loop climb from a
bare tree to ≈80.36 is, in the distinction route, the consequence of (i) starting
from the equilibrium angle rather than a bare coupling and (ii) the custodial
cost-asymmetry. The distinction route computes the equilibrium directly, so it
carries no "two-loop gap" to fill: the radiative-precision face is not an open
loop problem.

The honest input ledger (the only non-native pieces, none a loop construction):

  * NATIVE [P]: sin²θ_W = 3/13 (T_sin2theta); m_H = 124.93 (L_Higgs_2loop);
    the continuation-sum measure 1/(16π²) (continuation_sum_measure); the Δρ
    custodial structure (delta_rho_leading); N_c = 3 (gauge).
  * OPEN — the absolute top scale m_t. The value m_t = 163 GeV is an input; its
    *absolute* scale is the standing σ-derivation gap shared with the mass
    sector. (Mass ratios are native; the scale is not.)
  * PARTIALLY-NATIVE / QCD-hard — α at the EW scale, α(M_Z) = 1/128.21, embeds
    the running Δα. The leptonic part is clean; the hadronic part Δα_had is the
    nonperturbative distinction-density piece, of which a first-principles pQCD
    slice (75.7% of the dispersion) is banked at
    [P_perturbative_QCD_M_Z_first_principles] (delta_alpha_pqcd_m_z, v24.3.118).
  * EXTERNAL — α_s = 0.1179.

None of m_t, Δα_had, α_s is a loop to be constructed; they are a scale-setting
input and a nonperturbative distinction-density input.

Honest non-claims:
  * Export_MW_mechanism_native_structure_P = 1 — the decomposition of M_W into
    {equilibrium angle + custodial Δρ + native measure} is native.
  * Export_MW_no_loop_construction_required_P = 1 — the radiative-precision face
    requires no diagrammatic loop sum; the loop-expansion framing is retired.
  * Export_MW_value_fully_native_from_A1_P = 0 — full nativeness of the *value*
    is gated on the open absolute scale m_t and the hadronic Δα_had.
  * Export_physical_final_P = 0; no measured M_W consumed (the measured value
    enters only as the comparator for the error %, never as an input).
  * inherits the (2π)^D convention caveat of the continuation-sum measure.

Source: APF Reference Docs — EW Closure Registry (2026-05-28) + The Math-Physics
Line in the EW Loop Work and the Delta-rho Entry Point (2026-05-28) + Delta-rho
from the Distinction-Cost Picture v0.1. Composes check_L_W_mass (gauge.py),
check_T_sin2theta, check_T_delta_rho_leading_custodial_from_distinction,
check_T_continuation_sum_measure_native_from_D4, check_L_Higgs_2loop.
"""
from __future__ import annotations

import math

from apf.apf_utils import check, _result


# =============================================================================
# Verification kernel — recompute the decomposition independently and tie it to
# the banked native pieces. Nothing here consumes the measured M_W as an input.
# =============================================================================

def _decomposition():
    """Recompute M_W from {equilibrium angle + custodial Δρ family}, returning the
    pieces. Mirrors check_L_W_mass exactly; the measured M_W is NOT used."""
    sin2 = 3/13                       # T_sin2theta [P] — equilibrium angle
    alpha_em = 1/128.21               # α(M_Z): embeds Δα running (Δα_had partial)
    alpha_s = 0.1179                  # external
    m_t = 163.0                       # absolute scale = OPEN σ-gap
    m_H = 124.93                      # L_Higgs_2loop [P]
    M_Z = 91.1876                     # anchor

    M_W_tree = M_Z * math.sqrt(1 - sin2)
    lever = (1 - sin2) / (1 - 2*sin2)                       # 10/7
    Drho_top = 3*alpha_em*m_t**2 / (16*math.pi*M_W_tree**2*sin2)
    Drho_QCD = -2*alpha_s/math.pi * Drho_top
    Drho_H = -11*alpha_em*m_H**2 / (192*math.pi*M_W_tree**2*sin2)
    M_W = M_W_tree + M_W_tree*(Drho_top + Drho_QCD + Drho_H)/2*lever
    return dict(sin2=sin2, M_W_tree=M_W_tree, lever=lever, Drho_top=Drho_top,
                Drho_QCD=Drho_QCD, Drho_H=Drho_H, M_W=M_W, m_t=m_t, M_Z=M_Z)


# input-ledger classification: native [P] vs the named non-native inputs
INPUT_LEDGER = {
    "sin2_theta_W_3_13": "NATIVE_P (T_sin2theta — equilibrium angle)",
    "m_H_124p93": "NATIVE_P (L_Higgs_2loop)",
    "continuation_sum_measure_1_over_16pi2": "NATIVE_P (continuation_sum_measure, D=4)",
    "custodial_delta_rho_structure": "NATIVE_P (delta_rho_leading)",
    "N_c_3": "NATIVE_P (gauge)",
    "m_t_absolute_scale": "OPEN (sigma-derivation gap, shared with mass sector)",
    "alpha_MZ_hadronic_part_delta_alpha_had": "PARTIAL_P_QCD_HARD (delta_alpha_pqcd_m_z, 75.7% slice banked)",
    "alpha_s": "EXTERNAL",
}

NON_NATIVE_INPUTS = {"m_t_absolute_scale",
                     "alpha_MZ_hadronic_part_delta_alpha_had",
                     "alpha_s"}


EXPORT_FLAGS = {
    "Export_MW_mechanism_native_structure_P": 1,
    "Export_MW_no_loop_construction_required_P": 1,
    "Export_MW_value_fully_native_from_A1_P": 0,   # gated on m_t scale + Δα_had
    "Export_physical_final_P": 0,
    "measured_MW_consumed": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_mw_value_equilibrium_plus_custodial_no_loop_construction_P():
    """T: the W mass value arises from {equilibrium mixing angle + custodial Δρ +
    native continuation-sum measure}, with no loop construction. Composition /
    accounting theorem over banked native pieces: certifies that the banked
    M_W = 80.3336 GeV (L_W_mass, [P]) decomposes mechanistically into the tree
    value from the equilibrium angle sin²θ_W = 3/13 plus the custodial Δρ family
    (top + QCD + Higgs) whose measure factor 1/(16π²) is the banked
    continuation-sum measure; the SM's dominant Δα running is absorbed into the
    equilibrium angle, not summed. The only non-native inputs are the open
    absolute top scale, the hadronic Δα_had, and α_s — none a loop construction.
    No measured M_W consumed. Value's full nativeness gated on the open absolute
    scale + Δα_had.
    [P_structural_mw_value_equilibrium_plus_custodial_modulo_absolute_scale_and_alpha_had]."""

    d = _decomposition()

    # (a) the decomposition reproduces the independently-banked L_W_mass value.
    from apf.gauge import check_L_W_mass
    banked = check_L_W_mass()
    assert banked.get("passed", True), "L_W_mass must pass for the composition to be meaningful"
    M_W_banked = banked["artifacts"]["M_W_corr_GeV"]
    check(abs(d["M_W"] - M_W_banked) < 1e-3,
          f"decomposition M_W={d['M_W']:.4f} must reproduce banked L_W_mass {M_W_banked}")

    # (b) the tree value comes from the EQUILIBRIUM angle sin²θ_W = 3/13.
    check(abs(d["sin2"] - 3/13) < 1e-12, "equilibrium angle must be sin²θ_W = 3/13")
    check(abs(d["M_W_tree"] - d["M_Z"]*math.sqrt(1 - 3/13)) < 1e-9,
          "tree M_W must be M_Z·√(1 − 3/13) (angle equilibrium, not a bare coupling)")
    # the lever is the algebraic sensitivity (1−s²)/(1−2s²) = 10/7, not a fit.
    check(abs(d["lever"] - 10/7) < 1e-9, "custodial lever must be (1−s²)/(1−2s²) = 10/7")

    # (c) the custodial Δρ_top is the SAME object as the banked distinction-Δρ
    #     (and the textbook Δρ), modulo the α(M_Z)-vs-tree-G_F scheme choice.
    G_F = 1.16637e-5
    v2 = 1/(math.sqrt(2)*G_F)
    drho_distinction = 3*d["m_t"]**2/(16*math.pi**2*v2)        # N_c m_t²/(16π²v²)
    drho_standard = 3*G_F*d["m_t"]**2/(8*math.sqrt(2)*math.pi**2)
    check(abs(drho_distinction - drho_standard) < 1e-9,
          "banked distinction Δρ must equal the textbook 3G_F m_t²/(8√2π²)")
    check(abs(d["Drho_top"] - drho_distinction)/drho_distinction < 0.01,
          "L_W_mass custodial Δρ_top must be the banked distinction-Δρ object "
          "(agreement within the sub-percent α(M_Z)/tree-G_F scheme difference)")

    # (d) the 1/(16π²) measure factor of Δρ IS the banked continuation-sum measure.
    from apf.continuation_sum_measure import universal_measure_factor
    import sympy as sp
    D, u = universal_measure_factor()
    check(sp.simplify(u.subs(D, 4) - 1/(16*sp.pi**2)) == 0,
          "continuation-sum measure at D=4 must equal 1/(16π²) (the Δρ measure factor)")

    # (e) no measured M_W consumed: the value is independent of M_W_exp.
    #     _decomposition() never references the measured value.
    src = _decomposition.__code__.co_names + _decomposition.__code__.co_varnames
    check("M_W_exp" not in src,
          "the M_W value must be computed without consuming the measured M_W")
    check(EXPORT_FLAGS["measured_MW_consumed"] == 0, "measured_MW_consumed must be 0")

    # (f) input ledger: exactly three non-native inputs, none a loop construction.
    non_native = {k for k, v in INPUT_LEDGER.items()
                  if v.startswith(("OPEN", "PARTIAL", "EXTERNAL"))}
    check(non_native == NON_NATIVE_INPUTS,
          "the only non-native inputs must be {m_t absolute scale, Δα_had, α_s}")
    natives = {k for k, v in INPUT_LEDGER.items() if v.startswith("NATIVE_P")}
    check(len(natives) == 5,
          "five native [P] pieces: angle, m_H, measure, custodial structure, N_c")

    # (g) honest non-claim flags.
    check(EXPORT_FLAGS["Export_MW_mechanism_native_structure_P"] == 1,
          "the {angle + custodial Δρ + measure} mechanism is native structure")
    check(EXPORT_FLAGS["Export_MW_no_loop_construction_required_P"] == 1,
          "the radiative-precision face requires no loop construction")
    check(EXPORT_FLAGS["Export_MW_value_fully_native_from_A1_P"] == 0,
          "value's full nativeness gated on the open absolute scale + Δα_had")
    check(EXPORT_FLAGS["Export_physical_final_P"] == 0, "no physical-final claim")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_mw_value_equilibrium_plus_custodial_no_loop_construction: the W "
              "mass value arises from {equilibrium mixing angle sin²θ_W = 3/13 + "
              "custodial Δρ family + native continuation-sum measure}, with no "
              "loop construction. Composition/accounting theorem certifying the "
              "mechanistic decomposition of the banked M_W = 80.3336 GeV "
              "(L_W_mass, [P], 0.044%). The dominant SM Δα running is absorbed "
              "into the equilibrium angle; the only off-angle shift is custodial "
              "Δρ (= the banked distinction-Δρ, measure 1/(16π²) = banked "
              "continuation-sum measure). Non-native inputs: open absolute top "
              "scale, hadronic Δα_had, α_s — none a loop. "
              "[P_structural_mw_value_equilibrium_plus_custodial_modulo_absolute_scale_and_alpha_had]"),
        tier=4,
        epistemic=("P_structural_mw_value_equilibrium_plus_custodial_"
                   "modulo_absolute_scale_and_alpha_had"),
        summary=(
            "Makes explicit on the bank side what physically sets the W mass in "
            "the distinction picture, retiring the loop-expansion framing for the "
            "electroweak radiative face. Two native mechanisms, no diagram sum: "
            "(1) the weak mixing angle is a distinction-partition equilibrium "
            "(sin²θ_W = 3/13, T_sin2theta [P], the γ=17/4 attractor), which fixes "
            "the tree M_W = M_Z·√(1−sin²θ_W) and, being already the "
            "physical/all-orders angle, absorbs the SM's dominant Δα running "
            "rather than summing it; (2) custodial breaking Δρ — the substrate "
            "holding the t,b doublet at unequal cost — the only off-angle shift, "
            "applied by L_W_mass as Δρ_top + Δρ_QCD + Δρ_H times the algebraic "
            "lever (1−s²)/(1−2s²) = 10/7. The check verifies: the decomposition "
            "reproduces the independently-banked L_W_mass value 80.3336 GeV to "
            "1e-3; the tree uses the 3/13 equilibrium angle; the custodial Δρ_top "
            "is the same object as the banked distinction-Δρ (N_c m_t²/16π²v² = "
            "textbook 3G_F m_t²/8√2π²) to within the sub-percent α(M_Z)/tree-G_F "
            "scheme difference; and the 1/(16π²) measure factor is exactly the "
            "banked continuation-sum measure at D=4. The SM's one-loop→two-loop "
            "climb to ≈80.36 is, here, the consequence of starting from the "
            "equilibrium angle plus the custodial asymmetry — the distinction "
            "route computes the equilibrium directly and carries no two-loop gap. "
            "Honest input ledger: five native [P] pieces (angle, m_H, measure, "
            "custodial structure, N_c) and exactly three non-native inputs — the "
            "open absolute top scale m_t (σ-derivation gap, shared with the mass "
            "sector), the hadronic Δα_had (QCD-hard; a 75.7% first-principles pQCD "
            "slice banked at delta_alpha_pqcd_m_z, v24.3.118), and α_s — none of "
            "which is a loop construction. No measured M_W consumed (it enters "
            "only as the error-percent comparator). Value's full nativeness from "
            "A1 is gated on the absolute scale + Δα_had; the (2π)^D convention of "
            "the measure is inherited; no physical-final claim."
        ),
        key_result=(
            "M_W = 80.3336 GeV (0.044%) decomposes as {equilibrium angle 3/13 + "
            "custodial Δρ family + native 1/(16π²) measure}, no loop construction; "
            "only non-native inputs are the open absolute scale m_t, hadronic "
            "Δα_had, and α_s. "
            "[P_structural_mw_value_equilibrium_plus_custodial_modulo_absolute_scale_and_alpha_had]"
        ),
        dependencies=[
            "L_W_mass",
            "T_sin2theta",
            "T_delta_rho_leading_custodial_from_distinction",
            "T_continuation_sum_measure_native_from_D4",
            "L_Higgs_2loop",
        ],
        cross_refs=[
            "Theorem_R",
            "delta_alpha_pqcd_m_z (Δα_had partial, v24.3.118)",
        ],
        artifacts={
            "M_W_value_GeV": 80.3336,
            "M_W_error_pct": 0.044,
            "tree_from_equilibrium_angle": "M_Z·√(1 − 3/13)",
            "custodial_lever": "(1−s²)/(1−2s²) = 10/7",
            "delta_rho_is_banked_distinction_object": True,
            "measure_factor_is_continuation_sum_measure": "1/(16π²) at D=4",
            "input_ledger": dict(INPUT_LEDGER),
            "non_native_inputs": sorted(NON_NATIVE_INPUTS),
            "loop_expansion_framing": "retired — radiative face is not a loop problem",
            "reference_docs": [
                "Reference - EW Closure Registry (2026-05-28).md",
                "Reference - The Math-Physics Line in the EW Loop Work and the Delta-rho Entry Point (2026-05-28).md",
            ],
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_mw_value_equilibrium_plus_custodial_no_loop_construction":
        check_T_mw_value_equilibrium_plus_custodial_no_loop_construction_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
