"""APF-native two-loop Phase-2 [P+IBP-tool] admission policy — Tier-4.

This module banks a framework epistemic-grade decision, not a physical value.

The two-loop EW evaluator needs IBP-reduced master-coefficient rows. Producing
the full symbolic reduction natively is a multi-month tooling effort; using an
external reducer (Kira/FireFly/FiniteFlow) produces the same coefficients in one
run. The decision recorded here distinguishes two categories the earlier
FORBIDDEN_INPUT_LEDGER had collapsed:

  * an IBP reduction coefficient is *determined algebra* — a rational function
    in the kinematics and dimension, fixed uniquely by the diagram topology, the
    way a polynomial expansion is fixed. A tool computing it is like a CAS
    expanding a product.
  * a physical result (measured M_W, a published total SM M_W, a DIZET/ZFITTER
    component value, a DFGRU fit output, a fitted counterterm) is the answer.
    Consuming it is smuggling.

The policy admits the first as [P+IBP-tool] — the same posture as [P+lattice]:
proved modulo a named, externally computed, *verified* input — but only when the
tool-computed coefficient carries an independent native spot-check. An unchecked
tool row is refused. Every physical-result category stays forbidden. Native IBP
identities and comparator-only total evaluators are admitted on their existing
terms.

Adopted 2026-05-28 (principal decision) from the sibling-AI encoding in
APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v26 /
APF_TWO_LOOP_PHASE2_EVALUATOR_REDIRECT_AND_PIBP_LEDGER_v1. The decision unblocks
the Δρ^(2) native benchmark pack: tool-reduced coefficients may be used with
verification; nothing physical may be consumed.

Honest non-claims:
  * Export_physical_two_loop_value_P = 0  (no Σ/Π/Δr/M_W/Δρ value here)
  * Export_tool_IBP_coefficient_admitted_without_spot_check_P = 0
  * Export_physics_result_component_admitted_P = 0

Sibling APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v26 (six packs;
self-verifiers all PASS, all physical exports open).
"""
from __future__ import annotations

from dataclasses import dataclass

from apf.apf_utils import check, _result


# =============================================================================
# Policy kernel (faithful to the v26 pibp_policy encoding)
# =============================================================================

FORBIDDEN_PHYSICS_INPUTS = {
    "measured_MW",
    "published_total_SM_MW",
    "DIZET_component_value",
    "ZFITTER_component_value",
    "DFGRU_fit_output_component",
    "fitted_counterterm",
    "target_observable",
}


@dataclass(frozen=True)
class InputRow:
    row_id: str
    kind: str
    source: str
    independently_spot_checked: bool = False
    target_consumed: bool = False


def classify(row: InputRow) -> str:
    """Admission verdict for a candidate evaluator input row."""
    if row.target_consumed:
        return "REFUSE_TARGET_CONSUMPTION"
    if row.kind in FORBIDDEN_PHYSICS_INPUTS:
        return "REFUSE_PHYSICS_COMPONENT_SMUGGLING"
    if row.kind == "tool_computed_IBP_coefficient":
        if row.independently_spot_checked:
            return "ADMIT_ALGEBRA_P_PLUS_IBP_TOOL"
        return "REFUSE_UNCHECKED_IBP_TOOL_ROW"
    if row.kind == "native_IBP_identity":
        return "ADMIT_NATIVE_ALGEBRA"
    if row.kind == "comparator_total_evaluator":
        return "ADMIT_COMPARATOR_ONLY"
    return "ADMIT_IF_SOURCE_CERTIFIED_NONPHYSICAL"


def critical_path_after_redirect() -> list:
    """The post-redirect fast path the policy unblocks."""
    return [
        "fixed_benchmark_numeric_IBP_solve",
        "two_loop_vacuum_master_delta_rho_benchmark",
        "master_DE_numeric_integration_for_momentum_dependent_rows",
        "real_numeric_UV_IR_Ward_cancellation",
        "comparator_only_DIZET_ACFW_DGS_audit",
    ]


EXPORT_FLAGS = {
    "Export_p_plus_ibp_tool_admission_policy_P": 1,
    "Export_tool_IBP_coefficient_admitted_only_with_spot_check_P": 1,
    "Export_physical_two_loop_value_P": 0,
    "Export_tool_IBP_coefficient_admitted_without_spot_check_P": 0,
    "Export_physics_result_component_admitted_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_phase2_p_plus_ibp_tool_admission_policy_P():
    """T: [P+IBP-tool] admission policy. A tool-computed IBP coefficient is
    admitted at [P+IBP-tool] (analogous to [P+lattice]) only with an independent
    native spot-check; unchecked → refused. Every physical-result category
    (measured/published M_W, DIZET/ZFITTER component, DFGRU fit, fitted
    counterterm, target observable) is refused. Native IBP identities admitted
    as native algebra; comparator total evaluators admitted comparator-only.
    Target consumption always refused. No physical value banked.
    [P_p_plus_ibp_tool_admission_policy]."""

    # (a) Tool-computed IBP coefficient: admitted ONLY with a spot-check.
    checked = InputRow("r1", "tool_computed_IBP_coefficient", "Kira+FireFly",
                       independently_spot_checked=True)
    unchecked = InputRow("r2", "tool_computed_IBP_coefficient", "Kira+FireFly",
                         independently_spot_checked=False)
    check(classify(checked) == "ADMIT_ALGEBRA_P_PLUS_IBP_TOOL",
          "spot-checked tool IBP coefficient must be admitted at [P+IBP-tool]")
    check(classify(unchecked) == "REFUSE_UNCHECKED_IBP_TOOL_ROW",
          "unchecked tool IBP coefficient must be refused")

    # (b) Every physical-result category is refused as smuggling.
    for kind in FORBIDDEN_PHYSICS_INPUTS:
        if kind == "target_observable":
            continue  # covered by the target_consumed path below as well
        row = InputRow("p", kind, "external")
        check(classify(row) == "REFUSE_PHYSICS_COMPONENT_SMUGGLING",
              f"physics-result kind {kind} must be refused as smuggling")

    # (c) Target consumption is refused regardless of kind.
    consumed = InputRow("t", "tool_computed_IBP_coefficient", "x",
                        independently_spot_checked=True, target_consumed=True)
    check(classify(consumed) == "REFUSE_TARGET_CONSUMPTION",
          "target consumption must be refused even for an otherwise-admissible row")

    # (d) Native algebra and comparator-only admitted on their own terms.
    check(classify(InputRow("n", "native_IBP_identity", "v17_deck"))
          == "ADMIT_NATIVE_ALGEBRA", "native IBP identity must be admitted")
    check(classify(InputRow("c", "comparator_total_evaluator", "DIZET"))
          == "ADMIT_COMPARATOR_ONLY", "comparator total evaluator must be admitted comparator-only")

    # (e) The policy unblocks the post-redirect fast path.
    cp = critical_path_after_redirect()
    check(cp[0] == "fixed_benchmark_numeric_IBP_solve",
          "fast path must begin with fixed-benchmark numeric IBP solve")
    check("two_loop_vacuum_master_delta_rho_benchmark" in cp,
          "fast path must include the Δρ vacuum-master benchmark")
    check(cp[-1] == "comparator_only_DIZET_ACFW_DGS_audit",
          "fast path must end with comparator-only audit")

    # (f) Honest non-claim flags.
    check(EXPORT_FLAGS["Export_physical_two_loop_value_P"] == 0,
          "no physical two-loop value is banked by a policy module")
    check(EXPORT_FLAGS["Export_tool_IBP_coefficient_admitted_without_spot_check_P"] == 0,
          "unchecked tool coefficient admission must stay 0")
    check(EXPORT_FLAGS["Export_physics_result_component_admitted_P"] == 0,
          "physics-result component admission must stay 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_two_loop_phase2_p_plus_ibp_tool_admission_policy: framework "
              "[P+IBP-tool] grade. Tool-computed IBP coefficients admitted "
              "(analogous to [P+lattice]) only with an independent native "
              "spot-check; all physical-result categories refused as smuggling; "
              "target consumption always refused. No physical value. "
              "[P_p_plus_ibp_tool_admission_policy]"),
        tier=4,
        epistemic="P_p_plus_ibp_tool_admission_policy",
        summary=(
            "Principal decision banked 2026-05-28 from the sibling-AI encoding "
            "in APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v26 / "
            "APF_TWO_LOOP_PHASE2_EVALUATOR_REDIRECT_AND_PIBP_LEDGER_v1. "
            "Establishes [P+IBP-tool] as a framework epistemic grade: an IBP "
            "reduction coefficient is determined algebra (a rational function "
            "fixed by the diagram topology), so an external reducer computing it "
            "is admissible the same way external lattice QCD is admissible at "
            "[P+lattice] — proved modulo a named, externally computed, verified "
            "input — but ONLY when the tool-computed coefficient carries an "
            "independent native spot-check (REFUSE_UNCHECKED_IBP_TOOL_ROW "
            "otherwise). Every physical-result category stays forbidden: "
            "measured/published M_W, DIZET/ZFITTER component values, DFGRU fit "
            "outputs, fitted counterterms, target observables, and any "
            "target-consuming row. Native IBP identities are admitted as native "
            "algebra; comparator total evaluators comparator-only. The policy "
            "unblocks the post-redirect fast path (fixed-benchmark numeric IBP "
            "solve → two-loop vacuum master Δρ → master-DE numeric integration → "
            "real Ward cancellation → comparator-only audit) without banking any "
            "physical value. The symbolic-reconstruction track (v18–v23) is "
            "re-tasked as the verifier layer that supplies the spot-checks this "
            "policy requires."
        ),
        key_result=(
            "[P+IBP-tool] admission grade: tool-computed IBP coefficients "
            "admissible only with an independent native spot-check; all physical "
            "results refused. [P_p_plus_ibp_tool_admission_policy]"
        ),
        dependencies=[
            "T_two_loop_phase2_zfitter_comparator_guard_v1",
            "T_two_loop_phase2_ibp_reduction_engine_tier0_current_depth",
        ],
        cross_refs=[],
        artifacts={
            "forbidden_physics_inputs": sorted(FORBIDDEN_PHYSICS_INPUTS),
            "admission_verdicts": [
                "ADMIT_ALGEBRA_P_PLUS_IBP_TOOL", "REFUSE_UNCHECKED_IBP_TOOL_ROW",
                "REFUSE_PHYSICS_COMPONENT_SMUGGLING", "REFUSE_TARGET_CONSUMPTION",
                "ADMIT_NATIVE_ALGEBRA", "ADMIT_COMPARATOR_ONLY",
                "ADMIT_IF_SOURCE_CERTIFIED_NONPHYSICAL",
            ],
            "critical_path_after_redirect": critical_path_after_redirect(),
            "analogous_grade": "P+lattice",
            "sibling_bundle": "APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v26",
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_phase2_p_plus_ibp_tool_admission_policy":
        check_T_two_loop_phase2_p_plus_ibp_tool_admission_policy_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
