"""APF OS-W reviewed-formula evaluator harness (architecture-only) -- Tier-4.

Reconciled landing of the sibling delivery
``EW_OSW_EVALUATOR_HARNESS_PACKS_v1`` (six packs:
RENORMALIZED_SELF_ENERGY_EVALUATOR_CONTRACT / REVIEWED_FORMULA_EVALUATOR_SCAFFOLD
/ REVIEWED_FORMULA_COMPONENT_IMPLEMENTATION / REMAINDER_COMPONENT_IMPLEMENTATION /
FULL_REMAINDER_FORMULA_IMPLEMENTATION_CONTRACTS / REVIEWED_FORMULA_COEFFICIENT_LANDING;
archived verbatim under ``Codebase/EW_OSW_EVALUATOR_HARNESS_PACKS_v1/``).

What this module is
-------------------
A single, deduplicated encoding of the genuinely-new architecture the sibling
delivered: a *fail-closed* on-shell-W renormalized-self-energy evaluator harness
-- the scheme card, the diagram/component-family ledgers, the formula-family
contract DAG, the forbidden-input ledger, the coefficient source-card schema,
and the Ward/gauge-cancellation gate names -- WITHOUT re-banking anything the
codebase already carries.

Reconciliation against the banked w_trace ladder (the no-duplication discipline)
--------------------------------------------------------------------------------
The sibling packs re-built two things the bank already has; those are NOT
re-banked here, they are *referenced*:

  * the finite PV scalar substrate (sibling ``pv_finite_integrals.py``) is the
    already-banked ``apf.w_trace_pv_scalar_integral_substrate`` (a0_fin / b0_fin
    / c0_fin, verified 45/45). This harness delegates to it; it defines no PV
    kernels of its own.
  * the two implemented component kernels (leptonic Delta alpha; leading-top
    custodial Delta rho) are the already-banked ``apf.delta_alpha_leptonic``
    (Delta alpha_lep = 0.031421) and ``apf.gauge.check_L_W_mass``
    (Delta rho_top = 0.008379). They are referenced, not re-derived.

What this module does (and does NOT) claim
------------------------------------------
Architecture only. It claims the harness is structurally well-formed, fails
closed, and points at the banked substrate -- nothing about a physical value.
Every value-level export stays 0: no evaluated Delta r_rem, no DeltaRhobarW, no
numeric M_W, no DIZET replacement, no fitted counterterm. As of v24.3.80 six of
the original 14 reviewed-formula component families are source-certified
(fail-closed coefficient maps; see apf.ew_osw_source_transcription_families); the
remaining 8 remain OPEN, awaiting a source-certified coefficient import
(the sibling's named next gate ``SOURCE_CERTIFIED_COEFFICIENT_IMPORT``). Per the
sibling integrator notes, the imported DIZET-mediated route stays the publishable
OS-W closure (M_W = 80.357 GeV, [P_imported_physical_one_route_closure]).

Status
------
- Export_OSW_reviewed_formula_evaluator_harness_contract = 1  (architecture)
- Export_OSW_harness_fails_closed                        = 1  (architecture)
- Export_OSW_harness_wired_to_banked_substrate           = 1  (architecture)
- Export_OSW_APF_internal_delta_r_rem_evaluated          = 0  (OPEN gate)
- Export_OSW_APF_internal_DeltaRhobarW_evaluated         = 0  (OPEN gate)
- Export_OSW_full_reviewed_formula_evaluator             = 0  (OPEN gate)
- Export_numeric_MW_prediction_from_this_module          = 0
- Export_DIZET_replacement_evaluator                     = 0
- Export_fitted_counterterm                              = 0
"""
from __future__ import annotations

from typing import Any, Dict

from apf.apf_utils import check, _result


# ============================================================================
# Scheme card (on-shell renormalized EW self-energy convention)
# ============================================================================

SCHEME_CARD: Dict[str, str] = {
    "renormalization_scheme": "on_shell",
    "counterterm_convention": "Denner_Sirlin",
    "tadpole_convention": "Denner_FJ_explicit",
    "finite_part_scheme": "inherits_banked_w_trace_pv_substrate",
    "gauge": "Rxi_with_ward_gauge_cancellation_gates",
}

# Canonical (banked) dependencies this harness delegates to -- NOT re-defined.
CANONICAL_PV_SUBSTRATE = "apf.w_trace_pv_scalar_integral_substrate"
BANKED_COMPONENT_KERNELS: Dict[str, str] = {
    "leptonic_delta_alpha": "apf.delta_alpha_leptonic",          # Da_lep = 0.031421
    "leading_top_delta_rho": "apf.gauge.check_L_W_mass",         # Drho_top = 0.008379
}

# 16 reviewed-formula component families. Two are implemented (banked elsewhere),
# six are source-certified (fail-closed coefficient maps, v24.3.80); the
# remaining eight require a source-certified reviewed-formula coefficient import.
COMPONENT_FAMILIES_TOTAL = 16
COMPONENT_FAMILIES_IMPLEMENTED = ("leptonic_delta_alpha", "leading_top_delta_rho")
# Six families source-certified (fail-closed coefficient maps) by the v24.3.80
# SOURCE_TRANSCRIBE packs -> apf.ew_osw_source_transcription_families. A
# source-certified map is NOT an evaluated value: each still requires the
# self-energy VALUE as an input, so the harness still fails closed.
COMPONENT_FAMILIES_SOURCE_CERTIFIED = 6
COMPONENT_FAMILIES_SOURCE_CERTIFIED_NAMES = (
    "W_transverse_self_energy", "gamma_Z_mixing", "Z_transverse_self_energy",
    "vertex_box_terms", "gamma_gamma_vacuum_polarization",
    "mass_charge_weak_angle_counterterms",
)
COMPONENT_FAMILIES_PENDING_SOURCE_CERTIFIED = 8  # = 16 - 2 - 6

# Formula-family contract DAG (from FULL_REMAINDER_FORMULA_IMPLEMENTATION_CONTRACTS).
FORMULA_FAMILY_CONTRACTS = 14
WARD_GAUGE_GATES = (
    "ward_identity_transversality",
    "gauge_parameter_independence",
    "goldstone_ghost_cancellation",
)

# Forbidden-input ledger (no-smuggling surface; verbatim from the sibling packs).
FORBIDDEN_INPUTS = frozenset({
    "measured_M_W_value",
    "DIZET_ZFITTER_aggregate_output",
    "published_total_SM_M_W_as_component_value",
    "fitted_counterterm",
    "post_hoc_tolerance",
    "four_over_5063_weak_angle_shortcut",
    "measured_sin2theta_eff",
})

# Audit comparator intervals -- COMPARATOR ONLY, never consumed as inputs.
AUDIT_INTERVALS_COMPARATOR_ONLY: Dict[str, tuple] = {
    "DeltaRhobarW_MZ": (-1.260, -1.136),
    "Delta_r_rem_alpha": (0.003518, 0.003839),
    "Delta_r_rem_target": (0.009409, 0.009730),
}

EXPORT_FLAGS: Dict[str, int] = {
    "Export_OSW_reviewed_formula_evaluator_harness_contract": 1,
    "Export_OSW_harness_fails_closed": 1,
    "Export_OSW_harness_wired_to_banked_substrate": 1,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
    "Export_OSW_APF_internal_DeltaRhobarW_evaluated": 0,
    "Export_OSW_full_reviewed_formula_evaluator": 0,
    "Export_numeric_MW_prediction_from_this_module": 0,
    "Export_DIZET_replacement_evaluator": 0,
    "Export_fitted_counterterm": 0,
}


# ============================================================================
# Fail-closed evaluator surface
# ============================================================================

def evaluate_delta_r_rem() -> Dict[str, Any]:
    """Fail-closed: refuses to produce a value until all families are implemented.

    Returns a structured refusal (value_evaluated=False) rather than raising, so
    the bank check can assert the fail-closed contract. No numeric Delta r_rem is
    produced while pending_source_certified > 0.
    """
    return {
        "value_evaluated": False,
        "reason": "OPEN_SOURCE_CERTIFIED_COEFFICIENT_IMPORT_REQUIRED",
        "pending_source_certified": COMPONENT_FAMILIES_PENDING_SOURCE_CERTIFIED,
        "publishable_closure": "imported_DIZET_route_MW_80p357",
    }


def harness_report() -> Dict[str, Any]:
    return {
        "scheme_card": dict(SCHEME_CARD),
        "canonical_pv_substrate": CANONICAL_PV_SUBSTRATE,
        "banked_component_kernels": dict(BANKED_COMPONENT_KERNELS),
        "component_families_total": COMPONENT_FAMILIES_TOTAL,
        "component_families_implemented": list(COMPONENT_FAMILIES_IMPLEMENTED),
        "component_families_source_certified": COMPONENT_FAMILIES_SOURCE_CERTIFIED,
        "component_families_source_certified_names": list(COMPONENT_FAMILIES_SOURCE_CERTIFIED_NAMES),
        "component_families_pending_source_certified": COMPONENT_FAMILIES_PENDING_SOURCE_CERTIFIED,
        "formula_family_contracts": FORMULA_FAMILY_CONTRACTS,
        "forbidden_inputs": sorted(FORBIDDEN_INPUTS),
        "export_flags": dict(EXPORT_FLAGS),
        "evaluate": evaluate_delta_r_rem(),
    }


# ============================================================================
# Bank-registered checks (architecture-only: structural + honest-non-claim)
# ============================================================================

def check_T_ew_osw_harness_contract_wellformed_P() -> Dict[str, Any]:
    """T: the OS-W evaluator harness contract is structurally well-formed [P_structural]."""
    for k in ("renormalization_scheme", "counterterm_convention",
              "tadpole_convention", "finite_part_scheme", "gauge"):
        check(k in SCHEME_CARD and SCHEME_CARD[k], f"scheme card missing {k}")
    check(len(COMPONENT_FAMILIES_IMPLEMENTED) == 2,
          "exactly 2 component families are implemented (banked elsewhere)")
    check(len(COMPONENT_FAMILIES_IMPLEMENTED) == 2,
          "exactly 2 component families are implemented (banked elsewhere)")
    check(COMPONENT_FAMILIES_SOURCE_CERTIFIED == 6,
          "six component families are source-certified (coefficient maps)")
    check(len(COMPONENT_FAMILIES_IMPLEMENTED) + COMPONENT_FAMILIES_SOURCE_CERTIFIED
          + COMPONENT_FAMILIES_PENDING_SOURCE_CERTIFIED == COMPONENT_FAMILIES_TOTAL,
          "implemented + source_certified + pending must sum to the family total")
    check(len(FORBIDDEN_INPUTS) == 7, "forbidden-input ledger must have 7 entries")
    check(FORBIDDEN_INPUTS.isdisjoint(set(COMPONENT_FAMILIES_IMPLEMENTED)),
          "forbidden inputs must be disjoint from implemented families")
    check(len(WARD_GAUGE_GATES) == 3, "three Ward/gauge-cancellation gates declared")
    return _result(
        name="T_ew_osw_harness_contract_wellformed: "
             "OS-W reviewed-formula evaluator harness contract well-formed [P_structural]",
        tier=4, epistemic="P_structural_instrument",
        summary=(
            f"Scheme card complete (on-shell, Denner/Sirlin counterterm + tadpole, "
            f"finite-part inherited from the banked PV substrate). "
            f"{COMPONENT_FAMILIES_TOTAL} component families: "
            f"{len(COMPONENT_FAMILIES_IMPLEMENTED)} implemented (banked elsewhere) + "
            f"{COMPONENT_FAMILIES_PENDING_SOURCE_CERTIFIED} pending source-certified; "
            f"{FORMULA_FAMILY_CONTRACTS} formula-family contracts; 7-entry "
            f"forbidden-input ledger; 3 Ward/gauge gates."
        ),
        key_result="OS-W evaluator harness contract is well-formed. [P_structural]",
        dependencies=[],
        artifacts={
            "scheme_card": dict(SCHEME_CARD),
            "component_families_total": COMPONENT_FAMILIES_TOTAL,
            "pending_source_certified": COMPONENT_FAMILIES_PENDING_SOURCE_CERTIFIED,
        },
    )


def check_T_ew_osw_harness_fails_closed_P() -> Dict[str, Any]:
    """T: the harness fails closed -- no value while families are pending [P_structural]."""
    r = evaluate_delta_r_rem()
    check(r["value_evaluated"] is False, "harness must NOT evaluate a value while pending")
    check(r["pending_source_certified"] > 0, "there must be pending families to fail closed on")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "delta_r_rem value export must stay 0")
    check(EXPORT_FLAGS["Export_numeric_MW_prediction_from_this_module"] == 0,
          "no numeric M_W prediction from this module")
    return _result(
        name="T_ew_osw_harness_fails_closed: "
             "evaluator refuses a value until source-certified import lands [P_structural]",
        tier=4, epistemic="P_structural_instrument",
        summary=(
            f"evaluate_delta_r_rem() returns value_evaluated=False with "
            f"{r['pending_source_certified']} families pending source-certified "
            f"import; no numeric Delta r_rem / M_W is produced. The publishable "
            f"closure remains the imported DIZET route."
        ),
        key_result="Harness fails closed; no value exported. [P_structural]",
        dependencies=["T_ew_osw_harness_contract_wellformed"],
        artifacts={"evaluate": r},
    )


def check_T_ew_osw_harness_no_substrate_duplication_P() -> Dict[str, Any]:
    """T: harness delegates to the banked PV substrate + kernels, no duplication [P_structural]."""
    import importlib
    sub = importlib.import_module(CANONICAL_PV_SUBSTRATE)
    check(hasattr(sub, "a0_fin") and hasattr(sub, "b0_fin"),
          "canonical banked PV substrate must expose a0_fin/b0_fin")
    # this harness module defines no PV kernels of its own
    import apf.ew_osw_reviewed_formula_evaluator_harness as selfmod
    for kern in ("a0_fin", "b0_fin", "c0_fin", "c0_fin_zero_momenta"):
        check(not hasattr(selfmod, kern),
              f"harness must NOT redefine PV kernel {kern} (delegate to banked substrate)")
    # the 2 implemented component kernels point at banked modules
    da = importlib.import_module("apf.delta_alpha_leptonic")
    check(abs(da._leptonic_running()["da_lep_one_loop"] - 0.031421) < 1e-4,
          "leptonic Delta alpha kernel must be the banked delta_alpha_leptonic value")
    g = importlib.import_module("apf.gauge")
    check(abs(g.check_L_W_mass()["artifacts"]["Drho_top"] - 0.008379) < 1e-5,
          "leading-top Delta rho kernel must be the banked gauge.L_W_mass value")
    return _result(
        name="T_ew_osw_harness_no_substrate_duplication: "
             "delegates to banked PV substrate + kernels, no duplication [P_structural]",
        tier=4, epistemic="P_structural_instrument",
        summary=(
            "The harness delegates the finite PV scalar substrate to the banked "
            "apf.w_trace_pv_scalar_integral_substrate (a0_fin/b0_fin present) and "
            "defines no PV kernels of its own; the two implemented component "
            "families reference the banked apf.delta_alpha_leptonic (0.031421) and "
            "apf.gauge.check_L_W_mass (0.008379). No banked substrate or kernel is "
            "re-banked (no-duplication discipline)."
        ),
        key_result="Harness wired to banked substrate/kernels; no duplication. [P_structural]",
        dependencies=["T_ew_osw_harness_contract_wellformed"],
        cross_refs=["check_T_w_trace_pv_a0_gate_closed"],
        artifacts={
            "canonical_pv_substrate": CANONICAL_PV_SUBSTRATE,
            "banked_component_kernels": dict(BANKED_COMPONENT_KERNELS),
        },
    )


def check_C_ew_osw_full_evaluator_open_C() -> Dict[str, Any]:
    """L: the full reviewed-formula evaluator + evaluated Delta r_rem are OPEN [C]."""
    check(COMPONENT_FAMILIES_PENDING_SOURCE_CERTIFIED == 8,
          "8 component families remain pending source-certified import (6 now source-certified)")
    check(EXPORT_FLAGS["Export_OSW_full_reviewed_formula_evaluator"] == 0,
          "full reviewed-formula evaluator must remain OPEN (flag 0)")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_DeltaRhobarW_evaluated"] == 0,
          "DeltaRhobarW must remain unevaluated (flag 0)")
    check(EXPORT_FLAGS["Export_DIZET_replacement_evaluator"] == 0,
          "this is not a DIZET replacement (flag 0)")
    return _result(
        name="C_ew_osw_full_evaluator_open: "
             "full reviewed-formula evaluator + Delta r_rem OPEN [C]",
        tier=4, epistemic="C",
        summary=(
            "The full reviewed-formula evaluator requires a source-certified "
            "coefficient import for the 8 pending component families (6 of the "
            "original 14 are now source-certified coefficient maps; the named "
            "next gate continues with Goldstone/ghost/gauge/tadpole). Until then "
            "no Delta r_rem / DeltaRhobarW value is "
            "evaluated; all value exports stay 0; the imported DIZET route "
            "(M_W = 80.357) remains the publishable OS-W closure. The audit "
            "intervals (DeltaRhobarW [-1.260,-1.136], Delta r_rem [0.009409,"
            "0.009730]) are comparator-only, never consumed."
        ),
        key_result=(
            "Full OS-W reviewed-formula evaluator OPEN (8 source-certified "
            "families pending; 6 now source-certified maps); DIZET stays publishable. [C]"
        ),
        dependencies=["T_ew_osw_harness_contract_wellformed"],
        artifacts={
            "pending_source_certified": COMPONENT_FAMILIES_PENDING_SOURCE_CERTIFIED,
            "audit_intervals_comparator_only": AUDIT_INTERVALS_COMPARATOR_ONLY,
            "publishable_closure": "imported_DIZET_route",
        },
    )


# ============================================================================
# Registration
# ============================================================================

_CHECKS = {
    "T_ew_osw_harness_contract_wellformed": check_T_ew_osw_harness_contract_wellformed_P,
    "T_ew_osw_harness_fails_closed": check_T_ew_osw_harness_fails_closed_P,
    "T_ew_osw_harness_no_substrate_duplication": check_T_ew_osw_harness_no_substrate_duplication_P,
    "C_ew_osw_full_evaluator_open": check_C_ew_osw_full_evaluator_open_C,
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
    print(json.dumps(harness_report(), indent=2, default=str))
