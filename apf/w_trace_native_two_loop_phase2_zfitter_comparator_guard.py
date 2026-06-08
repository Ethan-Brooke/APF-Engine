"""APF-native two-loop Phase-2 ZFITTER comparator guard (FORMAL ROLE LEDGER) — Tier-4.

Formal role guard: ZFITTER 6.42 / DIZET program source may participate as a
COMPARATOR or same-input total-evaluator audit reference, but NEVER as a
component value supplying an APF self-energy / Δr_rem coefficient row.

Allowed roles (closed set of 4):
  * `comparator` — black-box regression target
  * `same_input_total_evaluator_audit` — running on the same inputs and
    auditing aggregate residuals
  * `implementation_context` — discussion of ZFITTER's two-loop conventions
  * `regression_target` — reference value for the assembled OS-W Δr_rem

Forbidden component tokens (5):
  * DIZET_AGGREGATE_COMPONENT
  * ZFITTER_TOTAL_INPUT
  * PUBLISHED_TOTAL_SM_MW
  * FITTED_COUNTERTERM
  * MEASURED_MW

Honest non-claims preserved:
  * Export_ZFITTER_or_DIZET_component_consumed = 0
  * Export_ZFITTER_row_local_coefficients_imported = 0
  * Export_DIZET_row_covariance_imported = 0

Sibling APF_TWO_LOOP_PHASE2_ZFITTER_COMPARATOR_GUARD_v1 via
APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v6.
"""
from __future__ import annotations

from typing import Tuple

from apf.apf_utils import check, _result


FORBIDDEN_COMPONENT_TOKENS: Tuple[str, ...] = (
    "DIZET_AGGREGATE_COMPONENT",
    "ZFITTER_TOTAL_INPUT",
    "PUBLISHED_TOTAL_SM_MW",
    "FITTED_COUNTERTERM",
    "MEASURED_MW",
)

ALLOWED_ROLES = frozenset({
    "comparator",
    "same_input_total_evaluator_audit",
    "implementation_context",
    "regression_target",
})


def validate_role(role: str) -> bool:
    return role in ALLOWED_ROLES


def refuse_component_value(source_label: str) -> bool:
    upper = source_label.upper()
    return any(tok in upper for tok in FORBIDDEN_COMPONENT_TOKENS)


def component_consumption_allowed(source_label: str, role: str) -> bool:
    return (validate_role(role)
            and not refuse_component_value(source_label)
            and role != "component_value")


EXPORT_FLAGS = {
    "Export_ZFITTER_comparator_role_P": 1,
    "Export_DIZET_same_input_total_evaluator_audit_role_P": 1,
    "Export_ZFITTER_component_consumption_refusal_P": 1,
    "Export_ZFITTER_or_DIZET_component_consumed_P": 0,
    "Export_ZFITTER_row_local_coefficients_imported_P": 0,
    "Export_DIZET_row_covariance_imported_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_phase2_zfitter_comparator_guard_v1_P():
    """T: Formal ZFITTER / DIZET role guard. 4 allowed roles (comparator,
    same_input_total_evaluator_audit, implementation_context, regression_target).
    5 forbidden component tokens. Component value role never allowed.
    [P_two_loop_phase2_zfitter_comparator_guard_v1;
     C_zfitter_component_consumption_permanently_refused]."""

    # (a) Allowed-role set integrity.
    check(len(ALLOWED_ROLES) == 4,
          f"allowed-role count: {len(ALLOWED_ROLES)}")
    for role in ["comparator", "same_input_total_evaluator_audit",
                 "implementation_context", "regression_target"]:
        check(validate_role(role), f"role {role!r} must be allowed")
    check(not validate_role("component_value"),
          "component_value role must NOT be allowed")
    check(not validate_role("aggregate_input"),
          "aggregate_input role must NOT be allowed")

    # (b) Forbidden-token coverage.
    check(len(FORBIDDEN_COMPONENT_TOKENS) == 5,
          f"forbidden-token count: {len(FORBIDDEN_COMPONENT_TOKENS)}")
    for tok in ["DIZET_AGGREGATE_COMPONENT", "ZFITTER_TOTAL_INPUT",
                "PUBLISHED_TOTAL_SM_MW", "FITTED_COUNTERTERM", "MEASURED_MW"]:
        check(refuse_component_value(tok), f"token {tok!r} must be refused")

    # (c) Forbidden-token refusal also catches embedded substrings.
    for label in ["something_DIZET_AGGREGATE_COMPONENT_value",
                  "MY_PUBLISHED_TOTAL_SM_MW_anchor",
                  "fit_MEASURED_MW_blob"]:
        check(refuse_component_value(label),
              f"embedded forbidden token in {label!r} must be refused")

    # (d) Clean labels with allowed roles pass.
    check(component_consumption_allowed("ZFITTER_total_aggregate_for_residual_audit",
                                        "same_input_total_evaluator_audit"),
          "clean same_input audit label must be allowed under same_input role")
    check(component_consumption_allowed("ACFW_2004_MW_fit_aggregate", "comparator"),
          "comparator role on aggregate label must be allowed")
    check(component_consumption_allowed("Denner_OS_convention_reference",
                                        "implementation_context"),
          "implementation_context role must be allowed")

    # (e) Forbidden tokens override allowed role.
    check(not component_consumption_allowed("DIZET_AGGREGATE_COMPONENT_payload",
                                            "comparator"),
          "forbidden token must override comparator role")
    check(not component_consumption_allowed("PUBLISHED_TOTAL_SM_MW_value",
                                            "regression_target"),
          "forbidden token must override regression_target role")

    # (f) component_value role never allowed.
    check(not component_consumption_allowed("clean_label", "component_value"),
          "component_value role must always be rejected even on clean labels")

    # (g) Honest non-claim flags.
    for ec in ["Export_ZFITTER_comparator_role_P",
               "Export_DIZET_same_input_total_evaluator_audit_role_P",
               "Export_ZFITTER_component_consumption_refusal_P"]:
        check(EXPORT_FLAGS[ec] == 1, f"{ec} must be 1")
    for nc in ["Export_ZFITTER_or_DIZET_component_consumed_P",
               "Export_ZFITTER_row_local_coefficients_imported_P",
               "Export_DIZET_row_covariance_imported_P"]:
        check(EXPORT_FLAGS[nc] == 0, f"{nc} must remain 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_two_loop_phase2_zfitter_comparator_guard_v1: "
              "Formal ZFITTER/DIZET role guard with 4 allowed roles "
              "(comparator, same_input_total_evaluator_audit, "
              "implementation_context, regression_target) and 5 forbidden "
              "component tokens (DIZET_AGGREGATE_COMPONENT, ZFITTER_TOTAL_INPUT, "
              "PUBLISHED_TOTAL_SM_MW, FITTED_COUNTERTERM, MEASURED_MW). "
              "component_value role never allowed. "
              "[P_two_loop_phase2_zfitter_comparator_guard_v1; "
              "C_zfitter_component_consumption_permanently_refused]"),
        tier=4,
        epistemic="P_two_loop_phase2_zfitter_comparator_guard_v1",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v6 / "
            "APF_TWO_LOOP_PHASE2_ZFITTER_COMPARATOR_GUARD_v1. Closed-set role "
            "allowlist with 4 entries permitting ZFITTER/DIZET as black-box "
            "comparator, same-input total-evaluator audit reference, "
            "implementation_context for two-loop conventions, or regression "
            "target. 5-token forbidden component blocklist refuses "
            "DIZET_AGGREGATE_COMPONENT, ZFITTER_TOTAL_INPUT, "
            "PUBLISHED_TOTAL_SM_MW, FITTED_COUNTERTERM, MEASURED_MW. The "
            "guard catches embedded forbidden substrings (case-insensitive "
            "via .upper()). Forbidden tokens override any allowed role. The "
            "component_value role is permanently rejected even on clean "
            "labels."
        ),
        key_result=(
            "ZFITTER/DIZET formal role guard with 4 allowed roles + 5 "
            "forbidden component tokens. Component consumption permanently "
            "refused. "
            "[P_two_loop_phase2_zfitter_comparator_guard_v1; "
            "C_zfitter_component_consumption_permanently_refused]"
        ),
        dependencies=[
            "T_two_loop_phase2_missing_terms_source_and_derivation_plan",
            "T_two_loop_phase2_osw_deltar_connector_refusal_toy",
            "T_two_loop_phase2_ew_self_energy_assembly_gate_toy_ledger",
        ],
        cross_refs=[],
        artifacts={
            "allowed_role_count": len(ALLOWED_ROLES),
            "allowed_roles": sorted(ALLOWED_ROLES),
            "forbidden_token_count": len(FORBIDDEN_COMPONENT_TOKENS),
            "forbidden_tokens": list(FORBIDDEN_COMPONENT_TOKENS),
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_phase2_zfitter_comparator_guard_v1":
        check_T_two_loop_phase2_zfitter_comparator_guard_v1_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
