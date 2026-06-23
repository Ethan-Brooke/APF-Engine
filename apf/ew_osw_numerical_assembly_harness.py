"""APF OS-W numerical assembly harness (architecture-only) -- Tier-4.

Reconciled landing of the sibling pack ``APF_EW_OS_W_NUMERICAL_ASSEMBLY_HARNESS_v1``
(archived verbatim under ``Codebase/EW_OSW_NUMERICAL_ASSEMBLY_HARNESS_v1/``).

What this module is
-------------------
The bank-side certificate layer for the fail-closed numerical assembly kernel
installed verbatim as ``apf.ew_osw_numerical_assembly_kernel``. The kernel is the
slot-algebra wiring that sits ON TOP of the six source-transcription families
(``apf.ew_osw_source_families`` / ``apf.ew_osw_source_transcription_families``):
given source-certified component VALUES it assembles

    Delta r_OS = Pi'_gamma_gamma(0)
               + [Pi_WW(0)/mW2 + (cW2/sW2 - 1) RePi_WW(mW2)/mW2]   (W-transverse)
               - (cW2/sW2) RePi_ZZ(mZ2)/mZ2                         (Z-transverse)
               + 2 (cW/sW) Pi_Zgamma(0)/mZ2                         (gamma-Z)
               + delta_VB                                           (vertex+box)

plus the helpers ``compute_delta_r_rem = Delta r_OS - Delta alpha + (cW2/sW2)
Delta rho`` and ``solve_mw_from_delta_r`` (the on-shell M_W <- G_F relation).

The slot algebra is exactly the SUM of the six banked family coefficient maps;
``check_T_ew_osw_numerical_assembly_slot_algebra`` proves this term-by-term
against ``apf.ew_osw_source_families.*`` -- the assembly introduces no new
physics, only the wiring. The kernel imports only math/dataclasses/typing; it
defines no PV kernels and duplicates no banked substrate.

What it does NOT claim
----------------------
Architecture only. No self-energy is computed; the included numerical run is a
synthetic unit test (placeholder values, manifestly non-physical). No physical
Delta r_OS / Delta r_rem / DeltaRhobarW / M_W is exported; no DIZET replacement;
no fitted counterterm. Every value-level export stays 0. The kernel fails closed
unless every required component value is source-certified and the (nested-key)
forbidden-input guard passes -- the guard ledger is the 7 family entries plus the
two target-interval entries (DeltaRhobarW / delta_r_rem windows). The named next
gate is COMPONENT_VALUE_SOURCING: actually computing the self-energy values, for
which the native APF PV tensor toolkit is the eventual provider. The imported
DIZET route stays the publishable OS-W closure.

Status
------
- Export_OSW_numerical_assembly_harness_landed                   = 1  (architecture)
- Export_OSW_numerical_assembly_slot_algebra_equals_banked_families = 1  (architecture)
- Export_OSW_physical_numerical_assembly_completed               = 0  (OPEN gate)
- Export_OSW_APF_internal_delta_r_rem_evaluated                  = 0  (OPEN gate)
- Export_numeric_MW_prediction_from_this_module                  = 0
"""
from __future__ import annotations

import importlib
import math
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.ew_osw_numerical_assembly_kernel import (
    assemble_delta_r_one_loop,
    compute_delta_r_rem,
    solve_mw_from_delta_r,
    REQUIRED_DELTA_R_SLOTS,
    FORBIDDEN_INPUTS,
    ForbiddenInputError,
    SourceCertificationRequired,
    InvalidAssemblyInput,
)

_FAMPKG = "apf.ew_osw_source_families"

# Forbidden-input ledger: the 7 family entries + 2 target-interval entries.
_FORBIDDEN_FAMILY_7 = (
    "measured_M_W_value",
    "DIZET_ZFITTER_aggregate_output",
    "published_total_SM_M_W_as_component_value",
    "fitted_counterterm",
    "post_hoc_tolerance",
    "four_over_5063_weak_angle_shortcut",
    "measured_sin2theta_eff",
)
_FORBIDDEN_TARGET_INTERVALS = ("target_DeltaRhobarW_interval", "target_delta_r_rem_interval")

# Synthetic unit-test component values (manifestly NON-PHYSICAL placeholders;
# the Pi_* values are O(0.1-1) toy numbers, not Standard-Model self-energies).
_SYNTH = {
    "mw2": 6400.0, "mz2": 8281.0,
    "pi_aa_prime_0": 0.01, "pi_ww_0": 1.0, "re_pi_ww_mw2": 0.5,
    "re_pi_zz_mz2": 0.3, "pi_zgamma_0": 0.2, "delta_vb_sm": 0.002,
}

EXPORT_FLAGS: Dict[str, int] = {
    "Export_OSW_numerical_assembly_harness_landed": 1,
    "Export_OSW_numerical_assembly_slot_algebra_equals_banked_families": 1,
    "Export_OSW_physical_numerical_assembly_completed": 0,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
    "Export_numeric_MW_prediction_from_this_module": 0,
}


def _synth_card():
    return {k: {"value": v, "source_certified": True, "source_ref": "synthetic_unit_test"}
            for k, v in _SYNTH.items()}


def _fam(name):
    return importlib.import_module(f"{_FAMPKG}.{name}")


# ===========================================================================
# checks
# ===========================================================================
def check_T_ew_osw_numerical_assembly_present_P() -> Dict[str, Any]:
    """T: the numerical assembly kernel is present with the expected interface [P_structural]."""
    check(callable(assemble_delta_r_one_loop) and callable(compute_delta_r_rem)
          and callable(solve_mw_from_delta_r), "kernel must expose the 3 assembly functions")
    expected_slots = {"mw2", "mz2", "pi_aa_prime_0", "pi_ww_0", "re_pi_ww_mw2",
                      "re_pi_zz_mz2", "pi_zgamma_0", "delta_vb_sm"}
    check(set(REQUIRED_DELTA_R_SLOTS) == expected_slots,
          "kernel must declare the 8 required Delta r component slots")
    check(set(_FORBIDDEN_FAMILY_7).issubset(FORBIDDEN_INPUTS),
          "guard must include the 7 family forbidden inputs")
    check(set(_FORBIDDEN_TARGET_INTERVALS).issubset(FORBIDDEN_INPUTS),
          "guard must additionally forbid the two target-interval inputs")
    check(len(FORBIDDEN_INPUTS) == 9, "forbidden-input ledger must have 9 entries")
    return _result(
        name="T_ew_osw_numerical_assembly_present: "
             "OS-W numerical assembly kernel present with expected interface [P_structural]",
        tier=4, epistemic="P_structural_instrument",
        summary=(
            "The fail-closed numerical assembly kernel (apf.ew_osw_numerical_assembly_kernel) "
            "exposes assemble_delta_r_one_loop / compute_delta_r_rem / solve_mw_from_delta_r, "
            "declares the 8 required Delta r component slots, and carries a 9-entry "
            "forbidden-input ledger (the 7 family entries + the two target-interval "
            "windows DeltaRhobarW / delta_r_rem)."
        ),
        key_result="Numerical assembly kernel present + 9-entry guard. [P_structural]",
        dependencies=["T_ew_osw_source_families_kernels_present"],
        artifacts={"required_slots": sorted(REQUIRED_DELTA_R_SLOTS),
                   "forbidden_inputs": sorted(FORBIDDEN_INPUTS)},
    )


def check_T_ew_osw_numerical_assembly_slot_algebra_P() -> Dict[str, Any]:
    """T: the assembly slot algebra equals the sum of the six banked family maps [P_structural].

    Exercised with synthetic placeholder values (non-physical). Each assembled
    term is cross-checked term-by-term against the banked family coefficient
    kernels in apf.ew_osw_source_families, proving the assembly introduces no new
    physics -- only the wiring.
    """
    out = assemble_delta_r_one_loop(_synth_card())
    check(out["physical_export"] is False and out["target_consumed"] is False,
          "assembly must not export a physical value or consume a target")
    terms = out["terms"]
    sw2 = out["weak_angle"]["sw2"]
    cw2 = out["weak_angle"]["cw2"]
    sw = out["weak_angle"]["sw"]
    cw = out["weak_angle"]["cw"]
    mw2, mz2 = _SYNTH["mw2"], _SYNTH["mz2"]

    # cross-check each slot against the corresponding banked family kernel
    gg = _fam("gamma_gamma_vacuum_polarization")
    w = _fam("w_transverse_self_energy")
    z = _fam("z_transverse_self_energy")
    gz = _fam("gamma_z_mixing")
    vb = _fam("vertex_box_terms")

    fam_gg = gg.delta_r_gamma_gamma_slot(
        gg.GammaGammaInput(PiPrime_gamma_gamma_0=_SYNTH["pi_aa_prime_0"], source_certified=True)).value
    fam_w = w.evaluate_w_transverse_family(
        w.WTransverseInput(Pi_WW_0=_SYNTH["pi_ww_0"], RePi_WW_mW2=_SYNTH["re_pi_ww_mw2"],
                           mW2=mw2, sW2=sw2, cW2=cw2)).delta_r_W
    fam_z = z.evaluate({"cW2": cw2, "sW2": sw2, "mZ2": mz2,
                        "rePiZZ_mZ2": _SYNTH["re_pi_zz_mz2"]})["Delta_r_Z"]
    fam_gz = gz.delta_r_gamma_z(
        gz.GammaZMixingInput(c_w=cw, s_w=sw, m_z2=mz2, pi_zgamma_0=_SYNTH["pi_zgamma_0"]))
    fam_vb = vb.assemble_vertex_box_from_card(
        {"delta_vb_sm": _SYNTH["delta_vb_sm"], "source_certified": True})["delta_r_vertex_box"]

    pairs = [
        ("gamma_gamma", terms["gamma_gamma"], fam_gg),
        ("W_transverse", terms["W_transverse"], fam_w),
        ("Z_transverse", terms["Z_transverse"], fam_z),
        ("gamma_Z", terms["gamma_Z"], fam_gz),
        ("vertex_box", terms["vertex_box"], fam_vb),
    ]
    mx = 0.0
    for nm, a, b in pairs:
        d = abs(a - b)
        mx = max(mx, d)
        check(d < 1e-12, f"assembly term {nm} {a} != banked family map {b}")
    fam_sum = fam_gg + fam_w + fam_z + fam_gz + fam_vb
    check(abs(out["delta_r_os"] - fam_sum) < 1e-12,
          "assembled Delta r_OS must equal the sum of the banked family maps")
    return _result(
        name="T_ew_osw_numerical_assembly_slot_algebra: "
             "assembly slot algebra == sum of the six banked family maps [P_structural]",
        tier=4, epistemic="P_structural_instrument",
        summary=(
            f"Under synthetic placeholder inputs the assembly's five slots "
            f"(gamma-gamma, W-transverse, Z-transverse, gamma-Z, vertex/box) match "
            f"the corresponding banked family coefficient maps term-by-term (max "
            f"abs diff {mx:.1e}), and the assembled Delta r_OS equals their sum. "
            f"The assembly introduces no new physics -- only the wiring; "
            f"physical_export=False, target_consumed=False. Placeholder inputs "
            f"only; no physical self-energy and no target value is involved."
        ),
        key_result="Assembly == sum of the six banked family maps. [P_structural]",
        dependencies=["T_ew_osw_numerical_assembly_present",
                      "T_ew_osw_source_families_coefficient_maps"],
        artifacts={"max_term_diff": mx, "synthetic_delta_r_os": out["delta_r_os"]},
    )


def check_T_ew_osw_numerical_assembly_fail_closed_P() -> Dict[str, Any]:
    """T: the assembly fails closed without certification / on invalid kinematics [P_structural]."""
    def _raises(fn, exc):
        try:
            fn()
            return False
        except exc:
            return True
        except Exception:
            return False

    # uncertified component -> SourceCertificationRequired
    bad = _synth_card()
    bad["pi_ww_0"] = {"value": 1.0, "source_certified": False}
    check(_raises(lambda: assemble_delta_r_one_loop(bad), SourceCertificationRequired),
          "uncertified component must fail closed")
    # missing slot -> InvalidAssemblyInput
    miss = _synth_card()
    del miss["delta_vb_sm"]
    check(_raises(lambda: assemble_delta_r_one_loop(miss), InvalidAssemblyInput),
          "missing component slot must fail closed")
    # invalid kinematics mw2 >= mz2 -> InvalidAssemblyInput
    badk = _synth_card()
    badk["mw2"] = {"value": 9000.0, "source_certified": True}
    check(_raises(lambda: assemble_delta_r_one_loop(badk), InvalidAssemblyInput),
          "mw2 >= mz2 must fail closed")
    check(_raises(lambda: compute_delta_r_rem(0.01, 0.05, 0.006, 9000.0, 8281.0),
                  InvalidAssemblyInput),
          "compute_delta_r_rem must reject mw2 >= mz2")
    return _result(
        name="T_ew_osw_numerical_assembly_fail_closed: "
             "assembly fails closed without certification / on invalid kinematics [P_structural]",
        tier=4, epistemic="P_structural_instrument",
        summary=(
            "The assembly fails closed: an uncertified component raises "
            "SourceCertificationRequired, a missing slot raises InvalidAssemblyInput, "
            "and unphysical kinematics (mW2 >= mZ2) raise InvalidAssemblyInput in "
            "both assemble_delta_r_one_loop and compute_delta_r_rem. No value is "
            "produced from incomplete or uncertified input."
        ),
        key_result="Assembly fails closed without certification. [P_structural]",
        dependencies=["T_ew_osw_numerical_assembly_present"],
        artifacts={},
    )


def check_T_ew_osw_numerical_assembly_forbidden_input_guard_P() -> Dict[str, Any]:
    """T: the (nested-key) forbidden-input guard rejects all 9 forbidden inputs [P_structural]."""
    rejected = 0
    for key in FORBIDDEN_INPUTS:
        card = _synth_card()
        card[key] = 1.0  # top-level forbidden key
        try:
            assemble_delta_r_one_loop(card)
        except ForbiddenInputError:
            rejected += 1
        except Exception:
            pass
    check(rejected == 9, f"expected 9 top-level rejections, got {rejected}")
    # nested forbidden key (buried inside a component object) must also be caught
    nested = _synth_card()
    nested["pi_ww_0"] = {"value": 1.0, "source_certified": True,
                         "measured_M_W_value": 80.4}
    caught_nested = False
    try:
        assemble_delta_r_one_loop(nested)
    except ForbiddenInputError:
        caught_nested = True
    except Exception:
        caught_nested = False
    check(caught_nested, "nested forbidden key must be caught by the recursive guard")
    return _result(
        name="T_ew_osw_numerical_assembly_forbidden_input_guard: "
             "nested-key guard rejects all 9 forbidden inputs [P_structural]",
        tier=4, epistemic="P_structural_instrument",
        summary=(
            "The no-smuggling surface holds and is stronger than the families': "
            "the recursive guard rejects all 9 forbidden inputs at the top level "
            "(the 7 family entries + the two target-interval windows) and also "
            "catches a forbidden key buried inside a nested component object."
        ),
        key_result="Nested-key guard rejects all 9 forbidden inputs. [P_structural]",
        dependencies=["T_ew_osw_numerical_assembly_present"],
        artifacts={"top_level_rejections": rejected, "nested_caught": True},
    )


def check_C_ew_osw_numerical_assembly_values_open_C() -> Dict[str, Any]:
    """L: the assembly is wiring only; physical values + component sourcing OPEN [C]."""
    check(EXPORT_FLAGS["Export_OSW_physical_numerical_assembly_completed"] == 0,
          "no physical numerical assembly is completed")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no Delta r_rem is evaluated")
    check(EXPORT_FLAGS["Export_numeric_MW_prediction_from_this_module"] == 0,
          "no numeric M_W from this module")
    return _result(
        name="C_ew_osw_numerical_assembly_values_open: "
             "assembly wiring only; physical values + component sourcing OPEN [C]",
        tier=4, epistemic="C",
        summary=(
            "The numerical assembly harness is the wiring layer: given "
            "source-certified component VALUES it assembles Delta r_OS / Delta r_rem "
            "/ M_W, but it computes no self-energy and the included run is synthetic "
            "only. All value exports stay 0. The named next gate is COMPONENT VALUE "
            "SOURCING -- actually computing Pi'_gamma_gamma(0), Pi_WW(0), "
            "RePi_WW(mW2), RePi_ZZ(mZ2), Pi_Zgamma(0), delta_VB from the SM particle "
            "content. The native APF PV tensor toolkit (A0/B0/C0/D0 + the complete "
            "2-/3-/4-point tensor bases) is the eventual provider; the imported "
            "DIZET route stays the publishable OS-W closure. With this landing the "
            "full stack is in place: native PV integrals -> 6 source-certified maps "
            "-> this assembly -> Delta r / M_W; only the self-energy construction "
            "from the SM content remains."
        ),
        key_result=(
            "Assembly wiring landed; physical values + component sourcing OPEN; "
            "native PV toolkit is the eventual provider. [C]"
        ),
        dependencies=["T_ew_osw_numerical_assembly_slot_algebra",
                      "C_ew_osw_source_families_values_open"],
        artifacts={"next_gate": "COMPONENT_VALUE_SOURCING",
                   "eventual_provider": "native_apf_pv_tensor_toolkit"},
    )


_CHECKS = {
    "T_ew_osw_numerical_assembly_present": check_T_ew_osw_numerical_assembly_present_P,
    "T_ew_osw_numerical_assembly_slot_algebra": check_T_ew_osw_numerical_assembly_slot_algebra_P,
    "T_ew_osw_numerical_assembly_fail_closed": check_T_ew_osw_numerical_assembly_fail_closed_P,
    "T_ew_osw_numerical_assembly_forbidden_input_guard": check_T_ew_osw_numerical_assembly_forbidden_input_guard_P,
    "C_ew_osw_numerical_assembly_values_open": check_C_ew_osw_numerical_assembly_values_open_C,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == "__main__":
    import json
    out = run_all()
    print(json.dumps({k: {"passed": v["passed"], "epistemic": v["epistemic"]}
                      for k, v in out.items()}, indent=2))
