"""APF OS-W finite-remainder source-transcription families (architecture-only) -- Tier-4.

Reconciled landing of the sibling delivery of six SOURCE_TRANSCRIBE packs
(W_TRANSVERSE_SELF_ENERGY / GAMMA_Z_MIXING / Z_TRANSVERSE_SELF_ENERGY /
VERTEX_BOX_TERMS / GAMMA_GAMMA_VACUUM_POLARIZATION /
MASS_CHARGE_WEAK_ANGLE_COUNTERTERMS; archived verbatim under
``Codebase/EW_OSW_SOURCE_TRANSCRIBE_PACKS_v1/``).

What this module is
-------------------
The bank-side certificate layer for the six fail-closed coefficient-map kernels
installed verbatim under ``apf.ew_osw_source_families``. Each kernel maps a
*source-certified* self-energy / counterterm value into the algebraic slot by
which it enters the one-loop on-shell-W Delta r (source-transcribed from
Dao/Gabelmann/Muehlleitner 2022 EPJC and Denner 1993 arXiv:0709.1075). This
module imports the kernels (does not re-derive them) and banks the
architecture-only certificates: the kernels are present, implement the documented
coefficient maps, fail closed without source certification, and reject every
forbidden (target/shortcut) input.

What it advances
----------------
These six families source-certify six of the fourteen families the banked
``apf.ew_osw_reviewed_formula_evaluator_harness`` left pending. With this landing
the harness accounting moves to 2 implemented + 6 source-certified + 8 pending =
16, and the harness still fails closed: a source-certified *coefficient map* is
not an evaluated value -- each kernel still requires the self-energy VALUE
(Pi_WW, Pi_ZZ, Pi_gamma_gamma', Pi_Zgamma, ...) as an input, which remains the
open gate (the native APF PV tensor toolkit is the eventual provider).

What it does NOT claim
----------------------
Architecture only. No self-energy is computed; no Delta r_rem / DeltaRhobarW /
numeric M_W is evaluated; no DIZET replacement; no fitted counterterm. Every
value-level export stays 0. The imported DIZET route stays the publishable OS-W
closure.

Status
------
- Export_OSW_source_transcription_families_landed       = 1  (architecture)
- Export_OSW_source_transcription_families_count        = 6  (architecture)
- Export_OSW_self_energy_values_computed                = 0  (OPEN gate)
- Export_OSW_APF_internal_delta_r_rem_evaluated         = 0  (OPEN gate)
- Export_numeric_MW_prediction_from_this_module         = 0
- Export_fitted_counterterm                             = 0
"""
from __future__ import annotations

import importlib
from typing import Any, Dict

from apf.apf_utils import check, _result

# ---------------------------------------------------------------------------
# the six verbatim kernels (apf.ew_osw_source_families.*)
# ---------------------------------------------------------------------------
_PKG = "apf.ew_osw_source_families"
FAMILY_MODULES = {
    "W_transverse_self_energy": "w_transverse_self_energy",
    "gamma_Z_mixing": "gamma_z_mixing",
    "Z_transverse_self_energy": "z_transverse_self_energy",
    "vertex_box_terms": "vertex_box_terms",
    "gamma_gamma_vacuum_polarization": "gamma_gamma_vacuum_polarization",
    "mass_charge_weak_angle_counterterms": "mass_charge_weak_angle_counterterms",
}
N_FAMILIES = 6

FORBIDDEN_INPUTS_CANON = (
    "measured_M_W_value",
    "DIZET_ZFITTER_aggregate_output",
    "published_total_SM_M_W_as_component_value",
    "fitted_counterterm",
    "post_hoc_tolerance",
    "four_over_5063_weak_angle_shortcut",
    "measured_sin2theta_eff",
)

EXPORT_FLAGS: Dict[str, int] = {
    "Export_OSW_source_transcription_families_landed": 1,
    "Export_OSW_source_transcription_families_count": 6,
    "Export_OSW_self_energy_values_computed": 0,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
    "Export_numeric_MW_prediction_from_this_module": 0,
    "Export_fitted_counterterm": 0,
}


def _mod(family: str):
    return importlib.import_module(f"{_PKG}.{FAMILY_MODULES[family]}")


def _forbidden_set(mod) -> set:
    return set(getattr(mod, "FORBIDDEN_INPUTS", None) or getattr(mod, "FORBIDDEN_INPUT_FIELDS"))


# ===========================================================================
# checks
# ===========================================================================
def check_T_ew_osw_source_families_kernels_present_P() -> Dict[str, Any]:
    """T: the six source-transcription kernels are present + carry the 7-entry guard [P_structural]."""
    check(len(FAMILY_MODULES) == N_FAMILIES, "must declare exactly 6 families")
    for fam, modname in FAMILY_MODULES.items():
        mod = _mod(fam)
        fset = _forbidden_set(mod)
        check(set(FORBIDDEN_INPUTS_CANON) == fset,
              f"{fam}: forbidden-input ledger must match the 7-entry canon")
    return _result(
        name="T_ew_osw_source_families_kernels_present: "
             "six OS-W source-transcription coefficient kernels present + guarded [P_structural]",
        tier=4, epistemic="P_structural_instrument",
        summary=(
            f"All {N_FAMILIES} OS-W finite-remainder source-transcription kernels "
            f"(W-transverse, gamma-Z mixing, Z-transverse, vertex/box, gamma-gamma "
            f"vacuum polarization, mass/charge/weak-angle counterterms) are installed "
            f"verbatim under apf.ew_osw_source_families and each carries the 7-entry "
            f"forbidden-input ledger. Source: Dao/Gabelmann/Muehlleitner 2022 EPJC + "
            f"Denner 1993."
        ),
        key_result="Six OS-W source-transcription kernels present + guarded. [P_structural]",
        dependencies=[],
        artifacts={"families": list(FAMILY_MODULES), "n_families": N_FAMILIES},
    )


def check_T_ew_osw_source_families_coefficient_maps_P() -> Dict[str, Any]:
    """T: each kernel implements its documented Delta r coefficient map (placeholder probe) [P_structural].

    Exercised with PLACEHOLDER unit inputs (manifestly non-physical, e.g. Pi=0.7,
    masses=2.0) purely to confirm the algebraic slot is wired as documented. No
    physical self-energy and no target value is involved.
    """
    errs = []

    # 1 W-transverse: delta_r_W = (Pi0 - RePi)/mW2 + (cW2/sW2)(RePi/mW2)
    w = _mod("W_transverse_self_energy")
    r = w.evaluate_w_transverse_family(
        w.WTransverseInput(Pi_WW_0=0.7, RePi_WW_mW2=0.3, mW2=2.0, sW2=0.25, cW2=0.75,
                           source_certified=True))
    exp = (0.7 - 0.3) / 2.0 + (0.75 / 0.25) * (0.3 / 2.0)
    if abs(r.delta_r_W - exp) > 1e-12:
        errs.append(f"W-transverse delta_r_W {r.delta_r_W} != {exp}")

    # 2 gamma-Z: dr = 2(cW/sW)Pi/mZ2 ; bridge = -(cW/sW)RePi/mZ2
    gz = _mod("gamma_Z_mixing")
    out = gz.evaluate_gamma_z_family(
        {"c_w": 0.8, "s_w": 0.6, "m_z2": 2.0, "pi_zgamma_0": 0.5, "re_pi_zgamma_mz2": 0.4})
    exp_dr = 2.0 * (0.8 / 0.6) * (0.5 / 2.0)
    exp_dk = -(0.8 / 0.6) * (0.4 / 2.0)
    if abs(out["Delta_r_gammaZ_coefficient_slice"] - exp_dr) > 1e-12:
        errs.append("gamma-Z dr slice mismatch")
    if abs(out["Delta_kappa_gammaZ_bridge_slice"] - exp_dk) > 1e-12:
        errs.append("gamma-Z dk bridge mismatch")
    if out["value_evaluated"] is not False:
        errs.append("gamma-Z value_evaluated must be False")

    # 3 Z-transverse: dr = -(cW2/sW2)RePi/mZ2 ; dk = +(...) ; anti-symmetric
    z = _mod("Z_transverse_self_energy")
    zo = z.evaluate({"cW2": 0.75, "sW2": 0.25, "mZ2": 2.0, "rePiZZ_mZ2": 0.4})
    exp_zr = -(0.75 / 0.25) * (0.4 / 2.0)
    if abs(zo["Delta_r_Z"] - exp_zr) > 1e-12:
        errs.append("Z-transverse dr mismatch")
    if not zo["anti_symmetric_check"]:
        errs.append("Z-transverse anti-symmetry failed")

    # 4 vertex/box: dr_VB = delta_vb_sm (identity, source-certified)
    vb = _mod("vertex_box_terms")
    vbo = vb.assemble_vertex_box_from_card({"delta_vb_sm": 0.123, "source_certified": True})
    if abs(vbo["delta_r_vertex_box"] - 0.123) > 1e-12 or vbo["computed_delta_vb"] is not False:
        errs.append("vertex/box identity slot mismatch")

    # 5 gamma-gamma: dr_gg = Pi'_gg(0) (identity, source-certified)
    gg = _mod("gamma_gamma_vacuum_polarization")
    kr = gg.delta_r_gamma_gamma_slot(
        gg.GammaGammaInput(PiPrime_gamma_gamma_0=0.077, source_certified=True))
    if abs(kr.value - 0.077) > 1e-12:
        errs.append("gamma-gamma identity slot mismatch")

    # 6 counterterms: bridge = 2 dZe - 2 dsW/sW ; OS relations
    ct = _mod("mass_charge_weak_angle_counterterms")
    dZe = ct.delta_Ze_OS(PiAA0=0.4, SigmaTAZ0_over_MZ2=0.1, sW=0.5, cW=0.866)
    exp_dZe = 0.5 * 0.4 - 1.0 * (0.5 / 0.866) * 0.1
    ds = ct.delta_sW_over_sW_OS(cW2=0.75, sW2=0.25, deltaMZ2_over_MZ2=0.05, deltaMW2_over_MW2=0.03)
    exp_ds = (0.75 / (2.0 * 0.25)) * (0.05 - 0.03)
    bridge = ct.delta_r_counterterm_bridge(dZe, ds)
    if abs(dZe - exp_dZe) > 1e-12 or abs(ds - exp_ds) > 1e-12:
        errs.append("counterterm OS relation mismatch")
    if abs(bridge - (2.0 * dZe - 2.0 * ds)) > 1e-12:
        errs.append("counterterm bridge mismatch")

    check(not errs, "coefficient-map probes failed: " + "; ".join(errs))
    return _result(
        name="T_ew_osw_source_families_coefficient_maps: "
             "each kernel implements its documented Delta r coefficient map [P_structural]",
        tier=4, epistemic="P_structural_instrument",
        summary=(
            "Each of the six kernels reproduces its documented Delta r coefficient "
            "slot under placeholder unit inputs: W-transverse difference+custodial; "
            "gamma-Z 2(cW/sW)Pi/mZ2 and -(cW/sW)RePi/mZ2; Z-transverse "
            "-(cW2/sW2)RePi/mZ2 (anti-symmetric with Delta kappa); vertex/box and "
            "gamma-gamma identity slots; counterterm bridge 2 dZe - 2 dsW/sW with the "
            "OS dZe / dsW relations. Placeholder inputs only -- no physical "
            "self-energy and no target value is involved."
        ),
        key_result="Six kernels implement their documented coefficient maps. [P_structural]",
        dependencies=["T_ew_osw_source_families_kernels_present"],
        artifacts={"probe_inputs": "placeholder_unit_values_non_physical"},
    )


def check_T_ew_osw_source_families_fail_closed_P() -> Dict[str, Any]:
    """T: every kernel fails closed without source certification [P_structural]."""
    gg = _mod("gamma_gamma_vacuum_polarization")
    vb = _mod("vertex_box_terms")
    ct = _mod("mass_charge_weak_angle_counterterms")
    gz = _mod("gamma_Z_mixing")

    def _raises(fn, exc):
        try:
            fn()
            return False
        except exc:
            return True
        except Exception:
            return False

    check(_raises(lambda: gg.delta_r_gamma_gamma_slot(gg.GammaGammaInput(PiPrime_gamma_gamma_0=None)),
                  gg.SourceCertificationRequired),
          "gamma-gamma must require a source-certified Pi'(0)")
    check(_raises(lambda: gg.delta_r_gamma_gamma_slot(
                      gg.GammaGammaInput(PiPrime_gamma_gamma_0=0.1, source_certified=False)),
                  gg.SourceCertificationRequired),
          "gamma-gamma must refuse uncertified input")
    check(_raises(lambda: vb.delta_r_vertex_box(0.1, source_certified=False),
                  vb.SourceCertificationRequired),
          "vertex/box must require source certification")
    check(_raises(lambda: ct.evaluate_counterterm_slice(
                      ct.CountertermInput(mW2=2.0, mZ2=2.0, sW=0.5, cW=0.866)),
                  ct.SourceValueRequired),
          "counterterms must require source self-energy values")
    check(_raises(lambda: gz.delta_r_gamma_z(gz.GammaZMixingInput(c_w=0.8, s_w=0.6, m_z2=2.0)),
                  ValueError),
          "gamma-Z must require pi_zgamma_0")
    # W-transverse + Z-transverse: no full-value / value_evaluated leak
    w = _mod("W_transverse_self_energy")
    rw = w.evaluate_w_transverse_family(
        w.WTransverseInput(Pi_WW_0=0.7, RePi_WW_mW2=0.3, mW2=2.0, sW2=0.25, cW2=0.75))
    check(rw.value_is_full_delta_r is False and rw.target_consumed is False,
          "W-transverse must not export a full delta_r or consume a target")
    z = _mod("Z_transverse_self_energy")
    zo = z.evaluate({"cW2": 0.75, "sW2": 0.25, "mZ2": 2.0, "rePiZZ_mZ2": 0.4})
    check(zo["value_evaluated"] is False and zo["target_consumed"] is False,
          "Z-transverse must not evaluate a value or consume a target")
    return _result(
        name="T_ew_osw_source_families_fail_closed: "
             "every source-transcription kernel fails closed without certification [P_structural]",
        tier=4, epistemic="P_structural_instrument",
        summary=(
            "Each kernel fails closed: gamma-gamma, vertex/box, and the counterterm "
            "slice raise (SourceCertificationRequired / SourceValueRequired) without "
            "source-certified self-energy inputs; gamma-Z raises without "
            "pi_zgamma_0; W-transverse and Z-transverse carry "
            "value_is_full_delta_r / value_evaluated = False and target_consumed = "
            "False. No kernel produces a value from nothing."
        ),
        key_result="All six kernels fail closed without source certification. [P_structural]",
        dependencies=["T_ew_osw_source_families_kernels_present"],
        artifacts={},
    )


def check_T_ew_osw_source_families_forbidden_input_guard_P() -> Dict[str, Any]:
    """T: every kernel's guard rejects all 7 forbidden (target/shortcut) inputs [P_structural]."""
    rejected = 0
    for fam in FAMILY_MODULES:
        mod = _mod(fam)
        guard = getattr(mod, "guard_forbidden_inputs")
        for key in FORBIDDEN_INPUTS_CANON:
            try:
                guard({key: 1.0})
                raise AssertionError(f"{fam}: guard accepted forbidden input {key}")
            except AssertionError:
                raise
            except Exception:
                rejected += 1
    check(rejected == N_FAMILIES * len(FORBIDDEN_INPUTS_CANON),
          f"expected {N_FAMILIES * len(FORBIDDEN_INPUTS_CANON)} rejections, got {rejected}")
    return _result(
        name="T_ew_osw_source_families_forbidden_input_guard: "
             "every kernel rejects all 7 forbidden inputs [P_structural]",
        tier=4, epistemic="P_structural_instrument",
        summary=(
            f"The no-smuggling surface holds: each of the {N_FAMILIES} kernels' "
            f"guard_forbidden_inputs rejects every one of the 7 forbidden "
            f"target/shortcut inputs (measured M_W, DIZET/ZFITTER aggregate, "
            f"published total SM M_W, fitted counterterm, post-hoc tolerance, "
            f"4/5063 weak-angle shortcut, measured sin2theta_eff) -- "
            f"{rejected} rejections total."
        ),
        key_result=f"All {N_FAMILIES} kernels reject all 7 forbidden inputs. [P_structural]",
        dependencies=["T_ew_osw_source_families_kernels_present"],
        artifacts={"rejections": rejected, "forbidden_inputs": list(FORBIDDEN_INPUTS_CANON)},
    )


def check_C_ew_osw_source_families_values_open_C() -> Dict[str, Any]:
    """L: the six families are coefficient maps only; self-energy values + Delta r_rem OPEN [C]."""
    # value-level exports stay 0
    check(EXPORT_FLAGS["Export_OSW_self_energy_values_computed"] == 0,
          "no self-energy value is computed by these families")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no Delta r_rem is evaluated")
    check(EXPORT_FLAGS["Export_numeric_MW_prediction_from_this_module"] == 0,
          "no numeric M_W from this module")
    # harness accounting now reflects the 6 source-certified families
    h = importlib.import_module("apf.ew_osw_reviewed_formula_evaluator_harness")
    check(getattr(h, "COMPONENT_FAMILIES_SOURCE_CERTIFIED", None) == 6,
          "harness must report 6 source-certified families")
    check(h.COMPONENT_FAMILIES_PENDING_SOURCE_CERTIFIED == 8,
          "harness must report 8 families still pending")
    check(h.evaluate_delta_r_rem()["value_evaluated"] is False,
          "harness must still fail closed")
    return _result(
        name="C_ew_osw_source_families_values_open: "
             "coefficient maps only; self-energy values + Delta r_rem OPEN [C]",
        tier=4, epistemic="C",
        summary=(
            "The six source-transcription families are coefficient MAPS only: each "
            "requires a source-certified self-energy / counterterm value as input "
            "and computes none. No Delta r_rem / DeltaRhobarW / M_W is evaluated; all "
            "value exports stay 0. The harness now reads 2 implemented + 6 "
            "source-certified + 8 pending = 16 and still fails closed. The open gate "
            "is the self-energy VALUES (Pi_WW, Pi_ZZ, Pi_gamma_gamma', Pi_Zgamma, "
            "...), which the native APF PV tensor toolkit is being built to supply; "
            "the imported DIZET route stays the publishable OS-W closure."
        ),
        key_result=(
            "Six families source-certified (maps only); self-energy values + "
            "Delta r_rem OPEN; harness fails closed (8 pending). [C]"
        ),
        dependencies=["T_ew_osw_source_families_coefficient_maps",
                      "T_ew_osw_harness_contract_wellformed"],
        artifacts={"source_certified": 6, "pending": 8, "implemented": 2, "total": 16},
    )


_CHECKS = {
    "T_ew_osw_source_families_kernels_present": check_T_ew_osw_source_families_kernels_present_P,
    "T_ew_osw_source_families_coefficient_maps": check_T_ew_osw_source_families_coefficient_maps_P,
    "T_ew_osw_source_families_fail_closed": check_T_ew_osw_source_families_fail_closed_P,
    "T_ew_osw_source_families_forbidden_input_guard": check_T_ew_osw_source_families_forbidden_input_guard_P,
    "C_ew_osw_source_families_values_open": check_C_ew_osw_source_families_values_open_C,
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
