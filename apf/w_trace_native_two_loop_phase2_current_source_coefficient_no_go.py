"""APF-native two-loop Phase-2 current-source coefficient no-go (AUDIT-FIRST FINDING) — Tier-4.

Audit-first declaration that the **currently uploaded** EW two-loop source set
is INSUFFICIENT to populate a row-local EW two-loop diagram coefficient
ledger. The five row families that the uploaded sources actually deliver
are catalogued explicitly with their honest classification:

  * `connector_relation` → `connector_only` (Δr / pole / R_ZZ / sin²θ_eff
    connector formulas; not coefficient rows). Sources: ACF 2006, ACFW 2004.
  * `aggregate_parametrization` → `comparator_only` (M_W / sin²θ_eff / Δκ /
    Δr published fits; admitting these as coefficients would smuggle in
    the observable or the aggregate as a component). Sources: ACFW 2004,
    ACF 2006.
  * `convention_ledger` → `convention_only` (Denner on-shell counterterms
    + one-loop self-energy definitions; ONE-loop, not 2L EW self-energy
    coefficient table). Source: Denner 2007.
  * `method_row` → `method_only` (fermionic DiaGen/IdSolver + expansion
    methods; methods, not coefficient values). Source: ACFW fermionic 2004.
  * `master_anchor` → `master_anchor_only` (CAF bosonic I4-I10 master
    integrals; missing the diagram coefficients that multiply these masters).
    Source: CAF bosonic 2006.

The no-go is **scoped to current uploads** — NOT a physics impossibility
theorem. The next gate explicitly names two admissible paths:

  1. Additional source coefficient tables / code outputs (e.g. DiaGen /
     IdSolver / ZFITTER source extracts; published ancillary tables).
  2. APF-internal derivation from Feynman rules + IBP + renormalization.

Honest non-claims preserved:
  * Export_source_certified_EW_2L_coefficient_ledger_from_current_uploads = 0
  * Export_evaluated_EW_2L_self_energies = 0
  * No measured M_W / sin²θ_eff / target consumed.

Sibling APF_TWO_LOOP_PHASE2_CURRENT_SOURCE_COEFFICIENT_NO_GO_v1 via
APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v5.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Set

from apf.apf_utils import check, _result


FORBIDDEN_PROMOTIONS: Set[str] = {
    "aggregate_parametrization",
    "convention_ledger",
    "method_row",
    "master_anchor",
    "connector_relation",
}

REQUIRED_NEXT_GATE = (
    "additional source coefficient tables/code outputs or APF derivation "
    "from Feynman rules + IBP + renormalization"
)


@dataclass(frozen=True)
class CurrentSourceDecisionRow:
    row_family: str
    object_described: str
    decision: str
    reason: str


DECISION_MATRIX = (
    CurrentSourceDecisionRow(
        row_family="connector_relation",
        object_described="Delta r / pole / R_ZZ / sin²θ_eff connector formula",
        decision="admit_as_connector",
        reason="not coefficient row",
    ),
    CurrentSourceDecisionRow(
        row_family="aggregate_parametrization",
        object_described="MW / sin²θ_eff / Delta-kappa / Delta-r published fit",
        decision="admit_as_comparator_only",
        reason="fit row would smuggle observable/aggregate",
    ),
    CurrentSourceDecisionRow(
        row_family="convention_ledger",
        object_described="Denner on-shell counterterms and one-loop self-energies",
        decision="admit_as_convention",
        reason="one-loop, not 2L EW self-energy coefficient table",
    ),
    CurrentSourceDecisionRow(
        row_family="method_row",
        object_described="fermionic DiaGen/IdSolver and expansion methods",
        decision="admit_as_method",
        reason="method not coefficient values",
    ),
    CurrentSourceDecisionRow(
        row_family="master_anchor",
        object_described="CAF bosonic I4-I10 master anchors",
        decision="admit_as_master_anchor",
        reason="missing diagram coefficients multiplying masters",
    ),
)


def classify(row_family: str) -> str:
    mapping = {
        "connector_relation": "connector_only",
        "aggregate_parametrization": "comparator_only",
        "convention_ledger": "convention_only",
        "method_row": "method_only",
        "master_anchor": "master_anchor_only",
    }
    if row_family not in mapping:
        raise ValueError(f"unknown row family: {row_family}")
    return mapping[row_family]


EXPORT_FLAGS = {
    "Export_current_source_audit_complete_P": 1,
    "Export_current_source_row_family_classifier_P": 1,
    "Export_current_source_coefficient_no_go_P": 1,
    "Export_source_certified_EW_2L_coefficient_ledger_from_current_uploads_P": 0,
    "Export_evaluated_EW_2L_self_energies_P": 0,
    "Export_OSW_delta_r_rem_APF_internal_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_phase2_current_source_coefficient_no_go_P():
    """T: Audit-first declaration that the currently uploaded EW two-loop
    source set is INSUFFICIENT for a row-local EW 2L diagram coefficient
    ledger. 5 row families (connector / aggregate / convention / method /
    master_anchor) admitted at scoped grades only. Next-gate paths:
    additional source tables/code outputs OR APF-internal derivation. NOT
    a physics impossibility theorem.
    [P_two_loop_phase2_current_source_coefficient_no_go;
     C_coefficient_ledger_requires_additional_sources_or_apf_derivation]."""

    families = {r.row_family for r in DECISION_MATRIX}
    check(families == FORBIDDEN_PROMOTIONS,
          f"decision matrix families mismatch: got {sorted(families)}, "
          f"expected {sorted(FORBIDDEN_PROMOTIONS)}")

    for r in DECISION_MATRIX:
        classified = classify(r.row_family)
        check(classified.endswith("_only"),
              f"row {r.row_family}: classification must end in '_only', got {classified}")
        check(r.decision.startswith("admit_as_"),
              f"row {r.row_family}: decision must begin with 'admit_as_', got {r.decision}")
        check(r.reason.strip() != "" and r.object_described.strip() != "",
              f"row {r.row_family}: empty reason or object_described")

    # Classifier mapping integrity
    check(classify("aggregate_parametrization") == "comparator_only",
          "aggregate must classify as comparator_only")
    check(classify("master_anchor") == "master_anchor_only",
          "master_anchor must classify as master_anchor_only")
    check(classify("connector_relation") == "connector_only",
          "connector must classify as connector_only")
    check(classify("convention_ledger") == "convention_only",
          "convention must classify as convention_only")
    check(classify("method_row") == "method_only",
          "method must classify as method_only")

    # Unknown family refused
    try:
        classify("source_certified_diagram_coefficient_row")
    except ValueError:
        pass
    else:
        raise AssertionError("classifier did not refuse unknown row family")

    # Required next-gate language
    check("additional source coefficient tables" in REQUIRED_NEXT_GATE,
          "next gate must name additional source tables option")
    check("APF derivation from Feynman rules" in REQUIRED_NEXT_GATE,
          "next gate must name APF-internal derivation option")

    # Honest non-claim discipline
    check(EXPORT_FLAGS["Export_current_source_coefficient_no_go_P"] == 1,
          "no-go declaration export must be 1")
    check(EXPORT_FLAGS["Export_source_certified_EW_2L_coefficient_ledger_from_current_uploads_P"] == 0,
          "source-certified-from-current-uploads must be 0 (the no-go itself)")
    check(EXPORT_FLAGS["Export_evaluated_EW_2L_self_energies_P"] == 0,
          "evaluated EW 2L self-energies must remain 0")
    check(EXPORT_FLAGS["Export_OSW_delta_r_rem_APF_internal_P"] == 0,
          "OS-W Δr_rem APF-internal must remain 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_two_loop_phase2_current_source_coefficient_no_go: "
              "Audit-first declaration that the CURRENT uploaded EW two-loop "
              "source set is INSUFFICIENT for a row-local EW 2L diagram "
              "coefficient ledger. 5 row families catalogued + classifier "
              "+ next-gate options named (additional sources OR APF-internal "
              "derivation). NOT a physics impossibility theorem — a scoped "
              "current-source statement. "
              "[P_two_loop_phase2_current_source_coefficient_no_go; "
              "C_coefficient_ledger_requires_additional_sources_or_apf_derivation]"),
        tier=4,
        epistemic="P_two_loop_phase2_current_source_coefficient_no_go",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v5 / "
            "APF_TWO_LOOP_PHASE2_CURRENT_SOURCE_COEFFICIENT_NO_GO_v1. "
            "Strongest audit-first content in the Phase-2 arc: a decision "
            "matrix catalogues the 5 row families the currently uploaded "
            "sources actually deliver and explicitly DOES NOT promote any to "
            "the source-certified row-local 2L EW coefficient ledger — "
            "(1) connector_relation → connector_only (Δr / pole / R_ZZ / "
            "sin²θ_eff connector formulas; relations, not coefficients), "
            "(2) aggregate_parametrization → comparator_only (fitted "
            "formulas would smuggle observable/aggregate as component), "
            "(3) convention_ledger → convention_only (Denner one-loop "
            "self-energies + counterterms; 1L, not 2L), (4) method_row → "
            "method_only (DiaGen/IdSolver + expansion methods, not "
            "coefficient values), (5) master_anchor → master_anchor_only "
            "(CAF I4-I10 masters with missing diagram coefficients). "
            "Two admissible next-gate paths named: (a) additional source "
            "coefficient tables / code outputs (e.g. ZFITTER source extracts, "
            "DiaGen/IdSolver output tables, published ancillaries); "
            "(b) APF-internal derivation from Feynman rules + IBP + "
            "renormalization. Scope is explicitly 'current uploads', NOT "
            "a physics impossibility theorem — the no-go is correctible "
            "by either path."
        ),
        key_result=(
            "Current-source no-go declared at scoped grade; 5 row families "
            "admitted-only-at-scoped-classes; next-gate options named "
            "(additional sources OR APF-internal derivation). "
            "[P_two_loop_phase2_current_source_coefficient_no_go; "
            "C_coefficient_ledger_requires_additional_sources_or_apf_derivation]"
        ),
        dependencies=[
            "T_two_loop_phase2_ew_tex_source_exact_extraction_v2",
            "T_two_loop_phase2_zpole_form_factor_connector_dag",
            "T_two_loop_phase2_bosonic_vertex_master_anchors_I4_I10",
            "T_two_loop_phase2_fermionic_vertex_reduction_ledger",
        ],
        cross_refs=[
            "T_two_loop_phase2_ew_coefficient_ledger_audit_scaffold",
        ],
        artifacts={
            "row_family_count": 5,
            "row_families": sorted(FORBIDDEN_PROMOTIONS),
            "classifier_map": {
                "connector_relation": "connector_only",
                "aggregate_parametrization": "comparator_only",
                "convention_ledger": "convention_only",
                "method_row": "method_only",
                "master_anchor": "master_anchor_only",
            },
            "next_gate_paths": [
                "additional source coefficient tables / code outputs",
                "APF-internal derivation from Feynman rules + IBP + renormalization",
            ],
            "scope_note": "current-uploaded-source no-go, not physics impossibility",
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_phase2_current_source_coefficient_no_go":
        check_T_two_loop_phase2_current_source_coefficient_no_go_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
