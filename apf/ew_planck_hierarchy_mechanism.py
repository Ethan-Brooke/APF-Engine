"""EW/Planck hierarchy as capacity suppression [P_structural] (mechanism, modulo O(1)).

The electroweak scale sits ~17 orders of magnitude below the Planck scale. This module
banks APF's STRUCTURAL account of that gap -- the hierarchy MECHANISM -- at the honest
grade, and is scrupulous that the absolute electroweak vev is NOT a native physical-final
export. (Arc: APF_ABSOLUTE_MASS_SCALE_PUSH_BUNDLE_v27..v33, converged 2026-05-29.)

WHAT IS BANKED [P_structural] -- the suppression FORM.
The EW/Planck ratio has the form of a bosonic-interface root-measure suppression
    v / M_Pl  ~  d_eff^(-C_boson/2),
the inverse square root of a microstate/branch-count volume Omega_boson = d_eff^C_boson over
the bosonic capacity directions. With the banked ledger numbers C_boson = 16 and d_eff = 102
the suppression is 102^(-8), which carries M_Pl ~ 1.2e19 GeV down to the order of a kilo-GeV
using NO electroweak-tuned integer. This is the hard part of the hierarchy problem, and it
comes out of the framework's existing capacity accounting (C_boson from the 3+16+42=61 ledger;
d_eff = 60+42 from the interface-sector bridge).

THE OPEN STRUCTURAL QUESTION (named here, not closed).
The exponent is C_boson/2 = 8 because the bosonic well is read over C_boson = 16 directions.
But the framework's own saturation microstate count (Paper 7: Z0 = (1 + d_eff e^{-beta eps*})
^C_total, N_micro = d_eff^C_total) runs over C_total = 61, NOT 16; at face value that count
gives exponent 61/2 = 30.5. The restriction from 61 to the 16 bosonic directions is PLAUSIBLE
(the electroweak order-parameter well is a bosonic object) but is ASSERTED, not derived. So the
suppression FORM is [P_structural]; the specific mode-count C_boson = 16 is the open structural
question -- why the bosonic well sees 16 modes, and why d_eff is the right per-mode degeneracy,
against Paper 7's C_total = 61. This module banks the form and NAMES the restriction as open.

WHAT IS NOT CLAIMED (route-b, by design).
The O(1) prefactor sqrt(N_c)/(pi sqrt(C_boson)) and the absolute vev are NOT native. The vev
moves by sqrt(N_c) under the color-counting convention (banked no-go,
T_yt_absolute_scale_not_fixable_by_normalization_no_go), by sqrt(8 pi) under the unreduced-vs-
reduced Planck choice, and by pi under the measure normalization. By the framework's own
invariance criterion a quantity that moves under a counting convention is not physical until
the convention is derived. So the absolute scale stays route-b (one external dimensionful
input), as T_sigma_scale_capacity_formula_held_pending_independent_scale states. The diagnostic
composition v_floor * 12/7 = 246.21 GeV is a CONVENTION-FIXED diagnostic, not a native export.

[P_structural -- hierarchy mechanism modulo O(1); bosonic mode-restriction C_boson=16 vs
C_total=61 OPEN; absolute value route-b]; no measured target consumed.
"""
from __future__ import annotations

import math
from fractions import Fraction

from apf.apf_utils import check, _result

# banked ledger numbers (fixed elsewhere in the framework; NOT tuned to the EW scale)
N_C, C_BOSON, C_TOTAL, D_EFF = 3, 16, 61, 102
M_PL = 1.22089e19               # unreduced Planck mass (convention carried; see route-b note)
FERMI_VEV = 246.21965079413738  # comparator only


EXPORT_FLAGS = dict(
    Export_EW_Planck_hierarchy_capacity_suppression_mechanism_P=1,  # the suppression FORM
    Export_hierarchy_mechanism_modulo_O1_prefactor_P=1,            # form; O(1) prefactor held
    Export_bosonic_mode_restriction_derived_P=0,                   # C_boson=16 vs C_total=61 OPEN
    Export_vH_absolute_scale_native_derivation_P=0,
    Export_vH_physical_final_P=0,
    Export_prefactor_full_native_P=0,
    Export_absolute_top_yukawa_value_P=0,
    measured_target_consumed=0,
    target_consumed=0,
)


def _suppression(c_boson=C_BOSON, d_eff=D_EFF):
    """Root-measure suppression d_eff^{-C_boson/2} = (microstate volume d_eff^C_boson)^{-1/2}."""
    return float(d_eff) ** (-(c_boson / 2.0))


def _floor():
    """y_t-free capacity floor (carries the diagnostic O(1) prefactor; see geometric-floor module)."""
    return M_PL * math.sqrt(N_C) / (math.pi * math.sqrt(C_BOSON) * (D_EFF ** (C_BOSON / 2.0)))


def check_T_ew_planck_hierarchy_capacity_suppression_mechanism_P():
    # the suppression FORM: inverse square root of the bosonic microstate volume
    Omega = float(D_EFF) ** C_BOSON
    check(math.isclose(_suppression(), Omega ** -0.5, rel_tol=1e-12),
          "suppression is inverse-sqrt of microstate volume Omega = d_eff^C_boson")
    check(math.isclose(_suppression(), D_EFF ** (-(C_BOSON / 2.0)), rel_tol=1e-12),
          "suppression = d_eff^{-C_boson/2}")
    # exponent is half the capacity (parameterized by C_boson, not a hardcoded 8)
    check(C_BOSON / 2.0 == 8.0, "exponent C_boson/2 = 8 at C_boson = 16")
    # it carries the Planck -> EW hierarchy using bank-fixed integers (floor ~ O(100) GeV)
    floor = _floor()
    check(100.0 < floor < 200.0, f"floor ~ O(100) GeV from M_Pl x suppression, got {floor:.2f}")
    # the mode-restriction is OPEN: Paper 7 saturation count runs over C_total = 61, not C_boson = 16
    check(C_TOTAL == 61 and C_BOSON == 16 and C_TOTAL != C_BOSON,
          "Paper-7 saturation count runs over C_total=61; bosonic restriction to 16 is asserted, not derived")
    check(EXPORT_FLAGS["Export_bosonic_mode_restriction_derived_P"] == 0,
          "mode-restriction C_boson=16 vs C_total=61 is the OPEN structural question")
    # honest non-claims: the absolute value is route-b, not native
    check(EXPORT_FLAGS["Export_vH_absolute_scale_native_derivation_P"] == 0, "absolute vev not native")
    check(EXPORT_FLAGS["Export_vH_physical_final_P"] == 0, "no physical-final claim")
    check(EXPORT_FLAGS["Export_prefactor_full_native_P"] == 0, "O(1) prefactor not native")
    check(EXPORT_FLAGS["measured_target_consumed"] == 0, "no measured vev consumed")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    # diagnostic-only composition reproduces the vev window (convention-fixed, NOT an export)
    vH_diag = floor * float(Fraction(12, 7))
    check(abs(vH_diag - 246.2119523) < 1e-3, f"diagnostic v_floor*12/7 ~ 246.21 GeV, got {vH_diag:.4f}")

    return _result(
        name=("T_ew_planck_hierarchy_capacity_suppression_mechanism: EW/Planck hierarchy as "
              "bosonic root-measure suppression v/M_Pl ~ d_eff^(-C_boson/2) [P_structural, "
              "mechanism modulo O(1); bosonic mode-restriction C_boson=16 vs C_total=61 OPEN; "
              "absolute value route-b]"),
        tier=4,
        epistemic='P_structural_convention',
        summary=(
            "The EW/Planck hierarchy has the FORM of a bosonic root-measure suppression "
            "v/M_Pl ~ d_eff^(-C_boson/2) = 102^(-8), the inverse-sqrt of microstate volume "
            "Omega_boson = d_eff^C_boson. C_boson=16, d_eff=102 are bank-fixed (no EW tuning); "
            "this carries M_Pl to O(100 GeV) -- the hard part of the hierarchy. OPEN: the "
            "restriction to C_boson=16 modes (Paper 7 saturation count runs over C_total=61; "
            "face-value 61/2=30.5). The bosonic restriction is plausible (EW order-parameter "
            "well is bosonic) but ASSERTED, not derived. The O(1) prefactor "
            "sqrt(N_c)/(pi sqrt(C_boson)) and the absolute vev are route-b: vev moves by "
            "sqrt(N_c) under color convention (yt no-go), sqrt(8pi) under Planck normalization, "
            "pi under measure. Diagnostic v_floor*12/7=246.21 GeV is convention-fixed, not native."
        ),
        key_result=(
            "v/M_Pl ~ d_eff^(-C_boson/2) [P_structural form, modulo O(1)]; C_boson=16-vs-C_total=61 "
            "mode-restriction OPEN; absolute value route-b (no native prefactor, no physical-final)."
        ),
        dependencies=['T_sigma_scale_yukawa_free_geometric_component',
                      'T_sigma_scale_capacity_formula_held_pending_independent_scale',
                      'T_yt_absolute_scale_not_fixable_by_normalization_no_go'],
        artifacts=dict(
            suppression="d_eff^(-C_boson/2) = 102^-8",
            C_boson=16, C_total_paper7=61, d_eff=102,
            floor_GeV=round(_floor(), 4),
            vH_diagnostic_GeV=round(_floor() * 12 / 7, 4),
            fermi_comparator_GeV=FERMI_VEV,
            open_question="why the bosonic well counts C_boson=16 modes vs Paper-7 C_total=61",
            export_flags=dict(EXPORT_FLAGS),
        ),
    )


_CHECKS = {
    "T_ew_planck_hierarchy_capacity_suppression_mechanism":
        check_T_ew_planck_hierarchy_capacity_suppression_mechanism_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
