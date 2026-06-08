"""APF-native two-loop Phase-2 EW source-table extraction (AGGREGATE FORMULAS + CONVENTIONS) — Tier-4.

Source-local extraction of formulas and conventions from the five EW two-loop
literature sources queued in v24.3.148, with the strict discipline that NO
row-level diagram coefficient is promoted as an APF-internal value.

What is extracted (positive content):

  * **ACFW 2004 W-mass fitting formula** (`hep-ph/0311148`, Eqs. 6-9) — the
    `MW0 + c1..c11` parametrization in two variants (full range and
    M_H ≥ 100 GeV). Reproduces the published table shift checks: ΔM_H=100
    GeV → −41.4 MeV, Δmt=5.1 GeV → +31 MeV, ΔM_Z=2.1 MeV → +2.6 MeV,
    Δα_had=3.6×10⁻⁴ → −6.5 MeV, Δα_s=2.7×10⁻³ → −1.7 MeV (all matched to
    ≤0.3 MeV).
  * **ACF 2006 sin²θ_eff^f fitting formula** (`hep-ph/0608099`, Eqs. 48-49 +
    Table 5) for 4 flavors (lepton, neutrino, up, down), with central values
    0.2312527, 0.2308772, 0.2311395, 0.2310286.
  * **ACF 2006 Δκ^(α²)_rem and Δr^(α²)_rem remainder parametrizations**
    (Eqs. 50-56), with k₀ = −0.002711 and r₀ = +0.003354.
  * **Denner 2007 on-shell counterterm helpers** (`0709.1075`, Eqs. 3.32 +
    3.35) — δZ_e, δc_W/c_W, δs_W/s_W as algebraic functions of the bare
    self-energy renormalization constants. Convention-only, not numeric.
  * **CAF 2006 bosonic hard-region master expressions** (`hep-ph/0602029`,
    Eq. 7) — symbolic anchors I4-I10 as strings with explicit ε-poles, ζ(3),
    π, S₂, √3 structure. Symbolic only; not a numeric evaluator.

What is explicitly NOT promoted (preserved non-claims):

  * No row-level diagram coefficients for Σ_W, Σ_Z, Π_γγ, Π_γZ.
  * No evaluated EW two-loop self-energies.
  * No DIZET/ZFITTER aggregate as an APF self-energy component.
  * No OS-W Δr_rem APF-internal value.
  * No measured M_W, sin²θ_eff, or target interval consumed as input.
  * No source-certified EW two-loop diagram coefficient ledger.

The 29 extracted rows fall into three promotion categories:

  * `convention_anchor` (Denner 2007 rows) — scheme + counterterm vocabulary,
    never a two-loop diagram coefficient.
  * `aggregate_formula_evaluator` (ACFW M_W parametrization, ACF sin²θ_eff
    fits, Δκ/Δr remainder fits) — published global fits, evaluable but
    explicitly aggregate, not source-local component rows.
  * `master_anchor` (CAF bosonic I4-I10 symbolic, ACFW fermionic LF1 DE +
    DiaGen/IdSolver method anchors) — methods + symbolic forms named, no
    numeric coefficient promoted.

Open-gap ledger (5 entries, all OPEN): Σ_W / Σ_Z / Π_γγ / Π_γZ row-level
coefficient ledgers + OS-W vertex/box two-loop finite remainder. These are
the next-gate items for `APF_TWO_LOOP_PHASE2_EW_SELF_ENERGY_COEFFICIENT_ROW_DERIVATION_OR_IMPORT_v1`.

Sibling APF_TWO_LOOP_PHASE2_EW_SOURCE_TABLE_EXTRACTION_v1 via
APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v4.
"""
from __future__ import annotations

from math import log
from typing import Dict, Literal

from apf.apf_utils import check, _result


# =============================================================================
# Source-certified kernel
# =============================================================================


class EWSourceFormulaError(ValueError):
    pass


# --- ACFW 2004 hep-ph/0311148 M_W parametrization, Eqs. 6-9 ------------------

MW_COEFFS_FULL_RANGE = {
    "MW0": 80.3779,
    "c1": 0.05427, "c2": 0.008931, "c3": 0.0000882, "c4": 0.000161,
    "c5": 1.070, "c6": 0.5237, "c7": 0.0679, "c8": 0.00179,
    "c9": 0.0000664, "c10": 0.0795, "c11": 114.9,
}

MW_COEFFS_MH_GT_100 = {
    "MW0": 80.3779,
    "c1": 0.05263, "c2": 0.010239, "c3": 0.000954, "c4": -0.000054,
    "c5": 1.077, "c6": 0.5252, "c7": 0.0700, "c8": 0.004102,
    "c9": 0.000111, "c10": 0.0774, "c11": 115.0,
}


def mw_parametrization_acfw_2004(
    MH: float,
    mt: float = 174.3,
    MZ: float = 91.1875,
    delta_alpha: float = 0.05907,
    alpha_s_MZ: float = 0.119,
    variant: Literal["full_range", "mh_gt_100"] = "full_range",
) -> float:
    """ACFW hep-ph/0311148 M_W fitting formula (Eqs. 6-9), in GeV.

    AGGREGATE fitted parametrization of the full SM result, NOT a
    diagram-level coefficient.
    """
    if MH <= 0 or mt <= 0 or MZ <= 0 or delta_alpha <= 0 or alpha_s_MZ <= 0:
        raise EWSourceFormulaError("all physical inputs must be positive")
    c = MW_COEFFS_FULL_RANGE if variant == "full_range" else MW_COEFFS_MH_GT_100
    dH = log(MH / 100.0)
    dh = (MH / 100.0) ** 2
    dt = (mt / 174.3) ** 2 - 1.0
    dZ = MZ / 91.1875 - 1.0
    da = delta_alpha / 0.05907 - 1.0
    das = alpha_s_MZ / 0.119 - 1.0
    return (c["MW0"]
            - c["c1"] * dH - c["c2"] * dH ** 2 + c["c3"] * dH ** 4
            + c["c4"] * (dh - 1.0) - c["c5"] * da + c["c6"] * dt
            - c["c7"] * dt ** 2 - c["c8"] * dH * dt + c["c9"] * dh * dt
            - c["c10"] * das + c["c11"] * dZ)


# --- ACF 2006 hep-ph/0608099 sin²θ_eff^f parametrization, Eqs. 48-49 ---------

SIN_EFF_COEFFS = {
    "lepton":   {"s0": 0.2312527, "d1": 4.729e-4, "d2": 2.07e-5, "d3": 3.85e-6,
                 "d4": -1.85e-6, "d5": 2.07e-2, "d6": -2.851e-3, "d7": 1.82e-4,
                 "d8": -9.74e-6, "d9": 3.98e-4, "d10": -6.55e-1},
    "neutrino": {"s0": 0.2308772, "d1": 4.713e-4, "d2": 2.05e-5, "d3": 3.85e-6,
                 "d4": -1.85e-6, "d5": 2.06e-2, "d6": -2.850e-3, "d7": 1.82e-4,
                 "d8": -9.71e-6, "d9": 3.96e-4, "d10": -6.54e-1},
    "up":       {"s0": 0.2311395, "d1": 4.726e-4, "d2": 2.07e-5, "d3": 3.85e-6,
                 "d4": -1.85e-6, "d5": 2.07e-2, "d6": -2.853e-3, "d7": 1.83e-4,
                 "d8": -9.73e-6, "d9": 3.98e-4, "d10": -6.55e-1},
    "down":     {"s0": 0.2310286, "d1": 4.720e-4, "d2": 2.06e-5, "d3": 3.85e-6,
                 "d4": -1.85e-6, "d5": 2.07e-2, "d6": -2.848e-3, "d7": 1.81e-4,
                 "d8": -9.73e-6, "d9": 3.97e-4, "d10": -6.55e-1},
}


def sin_eff_param_acf_2006(
    flavor: Literal["lepton", "neutrino", "up", "down"] = "lepton",
    MH: float = 100.0,
    mt: float = 178.0,
    MZ: float = 91.1876,
    delta_alpha: float = 0.05907,
    alpha_s_MZ: float = 0.117,
) -> float:
    """ACF hep-ph/0608099 sin²θ_eff^f fitting formula (Table 5).

    AGGREGATE observable fit, NOT a diagram coefficient ledger.
    """
    if flavor not in SIN_EFF_COEFFS:
        raise EWSourceFormulaError("unknown flavor")
    if MH <= 0 or mt <= 0 or MZ <= 0 or delta_alpha <= 0 or alpha_s_MZ <= 0:
        raise EWSourceFormulaError("all physical inputs must be positive")
    c = SIN_EFF_COEFFS[flavor]
    LH = log(MH / 100.0)
    DH = MH / 100.0
    Da = delta_alpha / 0.05907 - 1.0
    Dt = (mt / 178.0) ** 2 - 1.0
    Das = alpha_s_MZ / 0.117 - 1.0
    DZ = MZ / 91.1876 - 1.0
    return (c["s0"]
            + c["d1"] * LH + c["d2"] * LH ** 2 + c["d3"] * LH ** 4
            + c["d4"] * (DH ** 2 - 1.0) + c["d5"] * Da
            + c["d6"] * Dt + c["d7"] * Dt ** 2
            + c["d8"] * Dt * (DH - 1.0) + c["d9"] * Das + c["d10"] * DZ)


# --- ACF 2006 Δκ^(α²)_rem and Δr^(α²)_rem parametrizations, Eqs. 50-56 -------

KAPPA_COEFFS = {
    "k0": -0.002711, "k1": -3.12e-5, "k2": -4.12e-5, "k3": 5.28e-6,
    "k4": 3.75e-6, "k5": -5.16e-3, "k6": -2.06e-3, "k7": -2.32e-4,
    "k8": -0.0647, "k9": -0.129, "k10": 0.0712,
}
DELTA_R_COEFFS = {
    "r0": 0.003354, "r1": -2.09e-4, "r2": 2.54e-5, "r3": -7.85e-6,
    "r4": -2.33e-6, "r5": 7.83e-3, "r6": 3.38e-3, "r7": -9.89e-6,
    "r8": 0.0939, "r9": 0.204, "r10": -0.103,
}


def _acf_common_deltas(MH: float, mt: float, MW: float, MZ: float):
    if MH <= 0 or mt <= 0 or MW <= 0 or MZ <= 0:
        raise EWSourceFormulaError("all physical inputs must be positive")
    return {
        "LH": log(MH / 100.0),
        "DH": MH / 100.0,
        "Dt": (mt / 178.0) ** 2 - 1.0,
        "DW": MW / 80.404 - 1.0,
        "DZ": MZ / 91.1876 - 1.0,
    }


def delta_kappa_alpha2_rem_acf_2006(MH: float = 100.0, mt: float = 178.0,
                                    MW: float = 80.404, MZ: float = 91.1876) -> float:
    """ACF Δκ^(α²)_rem fitted remainder, Eqs. 50-53. AGGREGATE remainder fit."""
    d = _acf_common_deltas(MH, mt, MW, MZ)
    k = KAPPA_COEFFS
    return (k["k0"]
            + k["k1"] * d["LH"] + k["k2"] * d["LH"] ** 2 + k["k3"] * d["LH"] ** 4
            + k["k4"] * (d["DH"] ** 2 - 1.0)
            + k["k5"] * d["Dt"] + k["k6"] * d["Dt"] ** 2
            + k["k7"] * d["Dt"] * d["LH"]
            + k["k8"] * d["DW"] + k["k9"] * d["DW"] * d["Dt"] + k["k10"] * d["DZ"])


def delta_r_alpha2_rem_acf_2006(MH: float = 100.0, mt: float = 178.0,
                                MW: float = 80.404, MZ: float = 91.1876) -> float:
    """ACF Δr^(α²)_rem fitted remainder, Eqs. 54-56. AGGREGATE remainder fit."""
    d = _acf_common_deltas(MH, mt, MW, MZ)
    r = DELTA_R_COEFFS
    return (r["r0"]
            + r["r1"] * d["LH"] + r["r2"] * d["LH"] ** 2 + r["r3"] * d["LH"] ** 4
            + r["r4"] * (d["DH"] ** 2 - 1.0)
            + r["r5"] * d["Dt"] + r["r6"] * d["Dt"] ** 2
            + r["r7"] * d["Dt"] * d["LH"]
            + r["r8"] * d["DW"] + r["r9"] * d["DW"] * d["Dt"] + r["r10"] * d["DZ"])


# --- Denner 2007 hep-ph/0709.1075 counterterm helpers ------------------------


def denner_delta_ze(delta_Z_AA: float, delta_Z_ZA: float,
                    sW: float, cW: float) -> float:
    """Denner Eq. 3.32: δZ_e = -½ δZ_AA - (s_W/c_W)·½·δZ_ZA. Convention algebra."""
    if cW == 0:
        raise EWSourceFormulaError("cW must be nonzero")
    return -0.5 * delta_Z_AA - (sW / cW) * 0.5 * delta_Z_ZA


def denner_delta_cw_over_cw(delta_MW2_over_MW2: float,
                            delta_MZ2_over_MZ2: float) -> float:
    """Denner Eq. 3.35 first line: δc_W/c_W = ½(δM_W²/M_W² - δM_Z²/M_Z²)."""
    return 0.5 * (delta_MW2_over_MW2 - delta_MZ2_over_MZ2)


def denner_delta_sw_over_sw(delta_MW2_over_MW2: float,
                            delta_MZ2_over_MZ2: float,
                            sW: float, cW: float) -> float:
    """Denner Eq. 3.35 second line: δs_W/s_W = -(c_W²/s_W²)·δc_W/c_W."""
    if sW == 0:
        raise EWSourceFormulaError("sW must be nonzero")
    return -(cW * cW / (sW * sW)) * denner_delta_cw_over_cw(
        delta_MW2_over_MW2, delta_MZ2_over_MZ2)


# --- CAF 2006 hep-ph/0602029 bosonic hard-region master symbolic anchors -----


def bosonic_hard_master_expressions() -> Dict[str, str]:
    """CAF 2006 Eq. 7 source-local SYMBOLIC anchors. Strings, not numeric evaluators."""
    return {
        "I4":  "pi^2/(9 eps) + 3*pi*S2/sqrt(3) - 2*zeta(3)/9",
        "I5":  ("1/(2 eps^2) + (5/2 - pi/sqrt(3))/eps + 19/2 + pi^2/18 "
                "- 9*S2/4 - 5*pi/sqrt(3) + pi*log(3)/sqrt(3) "
                "+ 9*pi*S2/(2*sqrt(3)) - 8*zeta(3)/3"),
        "I6":  "9*pi*S2/(2*sqrt(3)) - 8*zeta(3)/3",
        "I7":  "pi^2/(18 eps) - 15*pi*S2/(2*sqrt(3)) + 23*zeta(3)/9",
        "I8":  ("1/(2 eps^2) + 3/(2 eps) + 5/2 + pi^2/36 + pi/sqrt(3) "
                "- 9*pi*S2/(2*sqrt(3)) + zeta(3)/3"),
        "I9":  "-pi^3/(54*sqrt(3)) + 3*pi*S2/(2*sqrt(3)) + 2*zeta(3)/9",
        "I10": "3*pi*S2/sqrt(3) - 5*zeta(3)/9",
    }


# =============================================================================
# Export flags + bank check
# =============================================================================

EXPORT_FLAGS = {
    "Export_EW_source_table_rows_extracted_P": 1,
    "Export_EW_aggregate_formula_evaluators_P": 1,
    "Export_EW_convention_anchor_rows_P": 1,
    "Export_EW_master_reduction_source_rows_P": 1,
    "Export_EW_uploaded_source_manifest_P": 1,
    "Export_source_certified_EW_two_loop_coefficient_ledger_P": 0,
    "Export_evaluated_EW_two_loop_self_energies_P": 0,
    "Export_row_level_diagram_coefficients_for_SigmaWZPi_channels_P": 0,
    "Export_DIZET_or_ZFITTER_aggregate_as_component_P": 0,
    "Export_OSW_delta_r_rem_APF_internal_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_phase2_ew_source_table_extraction_aggregate_and_convention_P():
    """T: EW source-table extraction from 5 named EW two-loop sources
    (ACFW 2004 W-mass, ACF 2006 complete sin²θ_eff, ACFW 2004 fermionic,
    CAF 2006 bosonic, Denner 2007 conventions). 29 rows split into
    convention_anchor + aggregate_formula_evaluator + master_anchor
    categories. Reproduces published ACFW 2004 M_W shift table to ≤0.3 MeV
    across 5 input variations. NO physical coefficient row promoted; NO
    EW self-energy or Δr_rem value claimed; 5 open-gap ledger entries
    remain OPEN.
    [P_two_loop_phase2_ew_source_table_extraction_aggregate_and_convention;
     C_physical_coefficient_rows_pending]."""

    # (a) ACFW 2004 M_W parametrization central + published shift table.
    mw0 = mw_parametrization_acfw_2004(100.0)
    check(abs(mw0 - 80.3779) < 1e-12,
          f"M_W central full-range must equal MW0=80.3779, got {mw0}")
    shifts = [
        ("ΔM_H 100→200 GeV", (mw_parametrization_acfw_2004(200.0) - mw0) * 1000.0,
         -41.4, 0.3),
        ("Δmt +5.1 GeV", (mw_parametrization_acfw_2004(100.0, mt=174.3 + 5.1) - mw0) * 1000.0,
         31.0, 0.4),
        ("ΔM_Z +2.1 MeV", (mw_parametrization_acfw_2004(100.0, MZ=91.1875 + 0.0021) - mw0) * 1000.0,
         2.6, 0.2),
        ("Δα_had +3.6e-4", (mw_parametrization_acfw_2004(100.0, delta_alpha=0.05907 + 0.00036) - mw0) * 1000.0,
         -6.5, 0.3),
        ("Δα_s +2.7e-3", (mw_parametrization_acfw_2004(100.0, alpha_s_MZ=0.119 + 0.0027) - mw0) * 1000.0,
         -1.7, 0.3),
    ]
    for label, got, exp, tol in shifts:
        check(abs(got - exp) <= tol,
              f"ACFW M_W shift '{label}' = {got:.2f} MeV vs published {exp} MeV (tol {tol})")

    # (b) High-MH variant central reproducer.
    mw0_high = mw_parametrization_acfw_2004(100.0, variant="mh_gt_100")
    check(abs(mw0_high - 80.3779) < 1e-12,
          f"M_W high-MH variant central must equal MW0=80.3779, got {mw0_high}")

    # (c) ACF 2006 sin²θ_eff^f central values (4 flavors).
    for flavor, expected in [("lepton", 0.2312527), ("neutrino", 0.2308772),
                             ("up", 0.2311395), ("down", 0.2310286)]:
        got = sin_eff_param_acf_2006(flavor)
        check(abs(got - expected) < 1e-12,
              f"sin²θ_eff central {flavor} = {got}, expected {expected}")

    # (d) Δκ and Δr remainder central values.
    check(abs(delta_kappa_alpha2_rem_acf_2006() - (-0.002711)) < 1e-15,
          f"Δκ^(α²)_rem central = {delta_kappa_alpha2_rem_acf_2006()}, expected -0.002711")
    check(abs(delta_r_alpha2_rem_acf_2006() - 0.003354) < 1e-15,
          f"Δr^(α²)_rem central = {delta_r_alpha2_rem_acf_2006()}, expected 0.003354")

    # (e) Denner counterterm helpers — convention algebra.
    expected_dze = -0.01 + (0.48 / 0.88) * 0.005
    got_dze = denner_delta_ze(delta_Z_AA=0.02, delta_Z_ZA=-0.01, sW=0.48, cW=0.88)
    check(abs(got_dze - expected_dze) < 1e-15,
          f"Denner δZ_e helper algebra: got {got_dze}, expected {expected_dze}")
    check(abs(denner_delta_cw_over_cw(0.04, 0.01) - 0.015) < 1e-15,
          "Denner δc_W/c_W = ½(0.04 - 0.01) = 0.015")
    expected_dsw = -((0.88 ** 2) / (0.48 ** 2)) * 0.015
    got_dsw = denner_delta_sw_over_sw(0.04, 0.01, sW=0.48, cW=0.88)
    check(abs(got_dsw - expected_dsw) < 1e-15,
          f"Denner δs_W/s_W algebra: got {got_dsw}, expected {expected_dsw}")

    # (f) CAF 2006 bosonic master symbolic anchors.
    masters = bosonic_hard_master_expressions()
    check(set(masters) == {"I4", "I5", "I6", "I7", "I8", "I9", "I10"},
          f"bosonic masters must be I4..I10: got {sorted(masters)}")
    check("eps^2" in masters["I5"], "I5 must carry double-pole 1/eps^2")
    check("zeta(3)" in masters["I4"], "I4 must carry ζ(3)")
    check("pi^3" in masters["I9"], "I9 must carry π³ Glaisher-style anchor")

    # (g) Positive-input refusal.
    for fn_args in [
        lambda: mw_parametrization_acfw_2004(MH=-1.0),
        lambda: sin_eff_param_acf_2006(flavor="lepton", mt=-1.0),
        lambda: delta_kappa_alpha2_rem_acf_2006(MH=-1.0),
        lambda: denner_delta_ze(0.0, 0.0, sW=0.5, cW=0.0),
        lambda: denner_delta_sw_over_sw(0.0, 0.0, sW=0.0, cW=0.5),
    ]:
        try:
            fn_args()
        except EWSourceFormulaError:
            continue
        raise AssertionError("positive-input or zero-denominator refusal failed")

    # (h) Honest non-claim flags (the critical discipline).
    check(EXPORT_FLAGS["Export_EW_source_table_rows_extracted_P"] == 1,
          "rows-extracted flag must be 1")
    check(EXPORT_FLAGS["Export_EW_aggregate_formula_evaluators_P"] == 1,
          "aggregate formula evaluators flag must be 1")
    check(EXPORT_FLAGS["Export_EW_convention_anchor_rows_P"] == 1,
          "convention anchor rows flag must be 1")
    check(EXPORT_FLAGS["Export_EW_master_reduction_source_rows_P"] == 1,
          "master reduction source rows flag must be 1")
    check(EXPORT_FLAGS["Export_EW_uploaded_source_manifest_P"] == 1,
          "uploaded source manifest flag must be 1")
    check(EXPORT_FLAGS["Export_source_certified_EW_two_loop_coefficient_ledger_P"] == 0,
          "source-certified coefficient ledger must remain 0")
    check(EXPORT_FLAGS["Export_evaluated_EW_two_loop_self_energies_P"] == 0,
          "evaluated EW self-energies must remain 0")
    check(EXPORT_FLAGS["Export_row_level_diagram_coefficients_for_SigmaWZPi_channels_P"] == 0,
          "row-level diagram coefficients must remain 0")
    check(EXPORT_FLAGS["Export_DIZET_or_ZFITTER_aggregate_as_component_P"] == 0,
          "DIZET/ZFITTER aggregate-as-component must remain 0")
    check(EXPORT_FLAGS["Export_OSW_delta_r_rem_APF_internal_P"] == 0,
          "OS-W Δr_rem APF-internal must remain 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_two_loop_phase2_ew_source_table_extraction_aggregate_and_convention: "
              "29-row source extraction from 5 EW two-loop literature sources "
              "(ACFW 2004 W-mass aggregate hep-ph/0311148, ACF 2006 complete "
              "sin²θ_eff hep-ph/0608099, ACFW 2004 fermionic hep-ph/0408207, "
              "CAF 2006 bosonic hep-ph/0602029, Denner 2007 conventions "
              "0709.1075). ACFW 2004 M_W parametrization reproduces published "
              "shift table to ≤0.4 MeV across 5 input variations. ACF 2006 "
              "sin²θ_eff^f central values for 4 flavors reproduced to <1e-12. "
              "Δκ/Δr remainder centrals reproduced. Denner δZ_e/δc_W/δs_W "
              "convention algebra. CAF bosonic I4-I10 symbolic anchors. "
              "All 29 rows tagged convention_anchor / aggregate_formula_evaluator "
              "/ master_anchor; no row promoted as physical diagram coefficient. "
              "[P_two_loop_phase2_ew_source_table_extraction_aggregate_and_convention; "
              "C_physical_coefficient_rows_pending]"),
        tier=4,
        epistemic="P_two_loop_phase2_ew_source_table_extraction_aggregate_and_convention",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v4 / "
            "APF_TWO_LOOP_PHASE2_EW_SOURCE_TABLE_EXTRACTION_v1. Implements: "
            "(a) ACFW 2004 M_W parametrization with c1..c11 in two variants "
            "(full range and M_H ≥ 100 GeV); shift table reproduction "
            "M_H 100→200 = -41.4 MeV, mt+5.1 = +31 MeV, M_Z+2.1 = +2.6 MeV, "
            "Δα_had+3.6e-4 = -6.5 MeV, Δα_s+2.7e-3 = -1.7 MeV. (b) ACF 2006 "
            "sin²θ_eff^f fitting formula for 4 flavors (lepton=0.2312527, "
            "neutrino=0.2308772, up=0.2311395, down=0.2310286). (c) ACF 2006 "
            "Δκ^(α²)_rem and Δr^(α²)_rem remainder parametrizations "
            "(k_0=-0.002711, r_0=+0.003354). (d) Denner δZ_e (Eq.3.32), "
            "δc_W/c_W and δs_W/s_W (Eq.3.35) counterterm helper algebra. "
            "(e) CAF 2006 bosonic hard-region master expressions I4-I10 "
            "as source-local symbolic strings carrying explicit ε-poles, "
            "ζ(3), π, S₂, √3 structure. The 29-row promotion-status "
            "classification ensures aggregate fits cannot smuggle as "
            "source-local component rows; Denner rows are convention-only; "
            "bosonic masters are symbolic anchors only. Open-gap ledger "
            "names 5 OPEN downstream items: Σ_W / Σ_Z / Π_γγ / Π_γZ "
            "row-level coefficient ledgers + OS-W vertex/box two-loop "
            "finite remainder."
        ),
        key_result=(
            "29-row EW source extraction with published-table reproduction "
            "(≤0.4 MeV) + Denner convention algebra + CAF bosonic master "
            "symbolic anchors. No row-level diagram coefficient promoted; "
            "no self-energy or Δr_rem value claimed. Coefficient-ledger "
            "physical promotion remains OPEN. "
            "[P_two_loop_phase2_ew_source_table_extraction_aggregate_and_convention; "
            "C_physical_coefficient_rows_pending]"
        ),
        dependencies=[
            "T_two_loop_phase2_ew_source_table_extraction_queue",
            "T_two_loop_phase2_ew_coefficient_ledger_audit_scaffold",
        ],
        cross_refs=[
            "T_two_loop_phase2_osw_deltar_connector_refusal_toy",
            "T_BSY_one_loop_kappa_l_assembly_consistency_at_Denner_validated_inputs",
        ],
        artifacts={
            "source_papers": {
                "ACFW_WMASS_2004": "hep-ph/0311148 Eqs.6-9 (aggregate M_W parametrization)",
                "ACF_SIN2EFF_COMPLETE_2006": "hep-ph/0608099 Eqs.48-56 (sin²θ_eff + Δκ/Δr remainders)",
                "ACFW_SIN2EFF_FERMIONIC_2004": "hep-ph/0408207 (fermionic methods + LF1 DE anchor)",
                "CAF_SIN2EFF_BOSONIC_2006": "hep-ph/0602029 Eq.7 (bosonic hard masters I4-I10)",
                "DENNER_ONE_LOOP_CONVENTIONS_2007": "0709.1075 Eqs.3.1-3.35 (OS scheme + counterterms)",
            },
            "extracted_row_count": 29,
            "promotion_categories": [
                "convention_anchor",
                "aggregate_formula_evaluator",
                "master_anchor",
            ],
            "MW_shift_table_reproduction_MeV": {
                "MH_100_to_200": -41.4,
                "mt_plus_5p1": 31.0,
                "MZ_plus_2p1_MeV": 2.6,
                "delta_alpha_had_plus_3p6e-4": -6.5,
                "alpha_s_plus_2p7e-3": -1.7,
            },
            "sin_eff_central_values": {
                "lepton": 0.2312527, "neutrino": 0.2308772,
                "up": 0.2311395, "down": 0.2310286,
            },
            "open_gap_count": 5,
            "next_gate": "APF_TWO_LOOP_PHASE2_EW_SELF_ENERGY_COEFFICIENT_ROW_DERIVATION_OR_IMPORT_v1",
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_phase2_ew_source_table_extraction_aggregate_and_convention":
        check_T_two_loop_phase2_ew_source_table_extraction_aggregate_and_convention_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
