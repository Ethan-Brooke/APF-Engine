"""APF-native two-loop Phase-2 missing-terms source map + derivation plan — Tier-4.

Direct follow-on to the v24.3.154 current-source no-go: this module banks the
**source acquisition order**, the **gap-to-source matrix**, the **7-stage
derivation workplan** (A: freeze convention → B: generate diagram classes →
C: project amplitudes → D: reduce to masters → E: evaluate rows → F: assemble
+ audit → G: validate vs aggregates), the **allowed/prohibited claim
language**, and the **7-pack downstream sequence** for closing the EW
two-loop coefficient ledger.

Fourteen source-acquisition targets are named with arXiv IDs and explicit
`claim_use` tags (primary derivation, methods+benchmark, aggregate benchmark
only, convention only, forbidden comparator):

  * Priority-1 Δr / muon-lifetime: FH-Weiglein 2000 (hep-ph/0007091),
    FH-Weiglein 2002 (hep-ph/0202131), Awramik-Czakon 2002 bosonic muon
    lifetime (hep-ph/0208113), Awramik-Czakon-Onishchenko-Veretin 2003 bosonic
    Δr (hep-ph/0209084), Awramik-Czakon 2003 complete muon lifetime
    (hep-ph/0305248).
  * Priority-1 sin²θ_eff result: ACFW 2004 fermionic PRL
    (hep-ph/0407317), CAF 2006 bosonic methods (hep-ph/0602029, banked),
    ACF 2006 bosonic result (hep-ph/0605339), ACF 2006 complete
    (hep-ph/0608099, banked aggregate), ACFW fermionic methods
    (hep-ph/0408207, banked methods), ACFW 2004 W-mass aggregate
    (hep-ph/0311148, banked aggregate).
  * Priority-3 optional: ACFK 2008 b̄b sin²θ_eff (0811.1364).
  * Convention only: Denner 2007 (0709.1075).
  * Forbidden as component: ZFITTER 6.42 / DIZET program source
    (comparator-only-forbidden-as-component).

Seven gaps mapped to primary sources + calculation routes:
Σ_W^(2L), Σ_Z^(2L), Π_γγ^(2L), Π_γZ^(2L), Z→ℓℓ vertex form factors
(v̂_f^(2), â_f^(2), Δκ), muon-decay vertex/box finite remainder, and
OSW Δr_rem APF-internal.

Forbidden-input no-smuggling guards reasserted in Stage F:
  * UV poles cancel in every physical channel
  * IR/QED pieces cancel or routed to Fermi/QED matching ledger
  * gauge-parameter dependence cancels at tested order
  * Ward identities for photon + γZ mixing satisfied
  * no measured M_W input
  * no DIZET/ZFITTER aggregate consumed as component
  * no published total SM M_W consumed as component
  * no fitted counterterm

Honest non-claims preserved:
  * Export_source_certified_EW_2L_diagram_coefficient_ledger = 0
  * Export_evaluated_{Sigma_W, Sigma_Z, Pi_gammagamma, Pi_gammaZ}_2L = 0
  * Export_vertex_box_2L_finite_remainder = 0
  * Export_OSW_delta_r_rem_APF_internal = 0
  * Export_DIZET_as_component = 0

Sibling APF_TWO_LOOP_PHASE2_MISSING_TERMS_SOURCE_AND_DERIVATION_PLAN_v1.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from apf.apf_utils import check, _result


@dataclass(frozen=True)
class SourceTarget:
    priority: int
    source_key: str
    arxiv: str
    title: str
    role: str
    current_status: str
    claim_use: str


SOURCE_TARGETS: Tuple[SourceTarget, ...] = (
    SourceTarget(1, "FHWWeiglein_2000_complete_fermionic_MW_MZ", "hep-ph/0007091",
                 "Complete fermionic two-loop results for the MW-MZ interdependence",
                 "Delta r alpha^2 fermionic; muon-decay MW-MZ route; self-energy/counterterm/vertex-box component source family",
                 "NOT_UPLOADED", "primary_derivation_or_comparator"),
    SourceTarget(1, "FHWWeiglein_2002_MW_MZ_technical", "hep-ph/0202131",
                 "Electroweak two-loop corrections to the MW-MZ mass correlation in the Standard Model",
                 "Technical description of complete fermionic Delta r calculation; renormalization; IR-divergent QED treatment; partial bosonic Higgs dependence",
                 "NOT_UPLOADED", "primary_methods_and_benchmark"),
    SourceTarget(1, "Awramik_Czakon_2002_bosonic_muon_lifetime", "hep-ph/0208113",
                 "Complete Two Loop Bosonic Contributions to the Muon Lifetime in the Standard Model",
                 "Delta r alpha^2 bosonic source family; gauge/Higgs boson loops in muon lifetime",
                 "NOT_UPLOADED", "primary_delta_r_bosonic"),
    SourceTarget(1, "Awramik_Czakon_Onishchenko_Veretin_2003_bosonic_Delta_r", "hep-ph/0209084",
                 "Bosonic corrections to Delta r at the two-loop level",
                 "Detailed bosonic Delta r calculation; matching to Fermi theory; OS/MS comparison; numerical methods vs expansions",
                 "NOT_UPLOADED", "primary_delta_r_bosonic_detail"),
    SourceTarget(1, "Awramik_Czakon_2003_complete_muon_lifetime", "hep-ph/0305248",
                 "Complete Two Loop Electroweak Contributions to the Muon Lifetime in the Standard Model",
                 "Independent complete EW two-loop muon-lifetime/Delta r calculation; cross-check of fermionic and bosonic sums",
                 "NOT_UPLOADED", "primary_cross_check"),
    SourceTarget(2, "ACFW_2004_Wmass_param", "hep-ph/0311148",
                 "Precise Prediction for the W-Boson Mass in the Standard Model",
                 "Published MW/Delta r aggregate formula and contribution inventory",
                 "UPLOADED_PDF_AND_TEX", "aggregate_benchmark_only"),
    SourceTarget(1, "ACFW_2004_fermionic_sin2eff_PRL", "hep-ph/0407317_or_PRL93_201805",
                 "Complete two-loop electroweak fermionic corrections to the effective leptonic weak mixing angle",
                 "Fermionic alpha^2 Z-pole vertex/form-factor source; closed-fermion-loop corrections",
                 "NOT_UPLOADED_EXCEPT_CONFERENCE_DETAIL", "primary_delta_kappa_fermionic"),
    SourceTarget(1, "ACFW_2004_fermionic_methods", "hep-ph/0408207",
                 "Two-loop Fermionic Electroweak Corrections to the Effective Leptonic Weak Mixing Angle in the Standard Model",
                 "DiaGen/IdSolver; top expansion; light-fermion DE; rational master coefficients",
                 "UPLOADED_PDF_AND_TEX", "derivation_method_ledger"),
    SourceTarget(1, "CAF_2006_bosonic_sin2eff_methods", "hep-ph/0602029",
                 "Bosonic corrections to the effective leptonic weak mixing angle at the two-loop level",
                 "Bosonic Z vertex; expansion by regions; 73 master integrals; I4-I10 anchors",
                 "UPLOADED_PDF_AND_TEX", "bosonic_vertex_method_and_master_anchors"),
    SourceTarget(1, "ACF_2006_bosonic_sin2eff_result", "hep-ph/0605339",
                 "Bosonic Corrections to the Effective Weak Mixing Angle at O(alpha^2)",
                 "Complete bosonic alpha^2 weak-mixing-angle result",
                 "NOT_UPLOADED", "primary_delta_kappa_bosonic_result"),
    SourceTarget(1, "ACF_2006_complete_sin2eff", "hep-ph/0608099",
                 "Electroweak two-loop corrections to the effective weak mixing angle",
                 "Complete sin2eff/Delta kappa aggregate; pole-scheme connector; methods; fits",
                 "UPLOADED_PDF_AND_TEX", "aggregate_benchmark_and_connector"),
    SourceTarget(3, "ACFK_2008_bbar_sin2eff", "0811.1364",
                 "Two-loop electroweak fermionic corrections to sin^2 theta_eff^bb",
                 "Optional b-quark final-state extension; topologies with additional top propagators",
                 "NOT_UPLOADED", "optional_extension"),
    SourceTarget(1, "Denner_2007_on_shell_conventions", "0709.1075",
                 "Techniques for electroweak radiative corrections at one-loop and W physics at LEP200",
                 "On-shell convention/counterterm notation; self-energy definitions; field/mass/charge renormalization convention",
                 "UPLOADED_PDF_AND_TEX", "convention_only"),
    SourceTarget(2, "ZFITTER_6_42_DIZET", "CPC_ADMJ_v2_0_or_program_library",
                 "ZFITTER/DIZET 6.42 program source",
                 "Aggregate EW precision observable comparator; MW and sin2eff two-loop implementations",
                 "NOT_UPLOADED", "comparator_only_forbidden_as_component"),
)


@dataclass(frozen=True)
class GapRow:
    gap: str
    needed: str
    primary_sources: str
    calculation_route: str


GAP_MATRIX: Tuple[GapRow, ...] = (
    GapRow("Sigma_W_2L",
           "Transverse W self-energy finite part plus pole ledger in OS convention",
           "FHWWeiglein_2000/2002; Awramik_Czakon_2002; ACOv_2003; Awramik_Czakon_2003",
           "Generate 2-point W diagrams + CT insertions; project transverse part; IBP reduce; evaluate master basis; validate through Delta r and MW fits."),
    GapRow("Sigma_Z_2L",
           "Transverse Z self-energy finite part plus pole ledger in OS/pole convention",
           "FHWWeiglein_2000/2002; ACF_2006_complete_sin2eff; Denner convention layer",
           "Generate Z self-energy diagrams; include gamma-Z mixing; enforce pole scheme; validate through Delta rho/Delta r and Z-pole form-factor equations."),
    GapRow("Pi_gammagamma_2L",
           "Photon transverse self-energy, charge-renormalization finite/pole entries, Ward-normalized at q^2=0",
           "FHWWeiglein_2002; Denner convention layer; ZFITTER/DIZET comparator",
           "Generate photon self-energy diagrams; impose photon masslessness and charge-renormalization Ward identities; validate Delta alpha separation is not double counted."),
    GapRow("Pi_gammaZ_2L",
           "gamma-Z mixing finite/pole rows at OS points and Z-pole connector contribution",
           "ACF_2006_complete_sin2eff; ACFW_2004_fermionic_methods; FHWWeiglein_2002; Denner convention layer",
           "Generate gamma-Z two-point diagrams; map into zhat_f pole-scheme connector; enforce OS mixing renormalization and UV cancellation."),
    GapRow("Zll_vertex_2L_form_factors",
           "vhat_f^(2), ahat_f^(2), Delta kappa finite rows",
           "ACFW_2004_fermionic_sin2eff_PRL; ACFW_2004_fermionic_methods; CAF_2006_bosonic_sin2eff_methods; ACF_2006_bosonic_sin2eff_result; ACF_2006_complete_sin2eff",
           "Use projectors for vector/axial form factors; split top/light fermionic and bosonic; reduce with IBP; evaluate via expansions/DE/MB/sector checks; validate Delta kappa fits."),
    GapRow("muon_decay_vertex_box_2L_finite_remainder",
           "Finite two-loop vertex/box remainder after Fermi-theory matching and QED IR subtraction",
           "FHWWeiglein_2000/2002; Awramik_Czakon_2002; ACOv_2003; Awramik_Czakon_2003",
           "Compute muon decay amplitude classes; separate QED/Fermi matching; cancel IR regulators; combine with self-energy/counterterms into Delta r_rem."),
    GapRow("OSW_delta_r_rem_APF_internal",
           "Complete convention-stable Delta r remainder assembled from self-energies, vertex/box, counterterms, tadpoles",
           "All Delta r sources plus Denner convention layer",
           "Assemble rows into Delta r; reproduce ACFW MW parametrization and Delta r contribution tables; no measured MW/DIZET total/fitted counterterm input."),
)


WORKPLAN_STAGES: Tuple[str, ...] = (
    "A_freeze_convention",
    "B_generate_diagram_classes",
    "C_project_amplitudes",
    "D_reduce_to_masters",
    "E_evaluate_rows",
    "F_assemble_and_audit",
    "G_validate_against_aggregates",
)

DOWNSTREAM_PACK_SEQUENCE: Tuple[str, ...] = (
    "APF_TWO_LOOP_PHASE2_MISSING_SOURCE_ACQUISITION_v1",
    "APF_TWO_LOOP_PHASE2_EW_DELTA_R_SOURCE_IMPORT_v1",
    "APF_TWO_LOOP_PHASE2_ZPOLE_DELTA_KAPPA_SOURCE_IMPORT_v1",
    "APF_TWO_LOOP_PHASE2_EW_DIAGRAM_GENERATOR_AND_PROJECTORS_v1",
    "APF_TWO_LOOP_PHASE2_EW_IBP_REDUCTION_LEDGER_v1",
    "APF_TWO_LOOP_PHASE2_EW_COEFFICIENT_ROW_LEDGER_v1",
    "APF_TWO_LOOP_PHASE2_OSW_DELTAR_EVALUATOR_v1",
)

FORBIDDEN_INPUT_TOKENS_STAGE_F: Tuple[str, ...] = (
    "measured_M_W_input",
    "DIZET_or_ZFITTER_aggregate_consumed_as_component",
    "published_total_SM_M_W_consumed_as_component",
    "fitted_counterterm",
)

ALLOWED_CLAIM_LANGUAGE = (
    "The current pack identifies the missing EW two-loop coefficient sources "
    "and supplies a calculation plan with source-acquisition order, diagram "
    "families, projector requirements, reduction route, validation targets, "
    "and no-smuggling gates."
)

PROHIBITED_CLAIM_LANGUAGE: Tuple[str, ...] = (
    "The EW two-loop self-energy coefficients are extracted.",
    "The APF-internal OS-W Delta-r remainder is evaluated.",
    "The DIZET/ZFITTER output is an APF component.",
    "The aggregate MW or sin2eff parametrization closes the self-energy row ledger.",
)


EXPORT_FLAGS = {
    "Export_missing_terms_source_map_P": 1,
    "Export_EW_2L_derivation_plan_P": 1,
    "Export_source_acquisition_order_P": 1,
    "Export_forbidden_input_guard_P": 1,
    "Export_seven_pack_downstream_sequence_P": 1,
    "Export_source_certified_EW_2L_diagram_coefficient_ledger_P": 0,
    "Export_evaluated_Sigma_W_2L_P": 0,
    "Export_evaluated_Sigma_Z_2L_P": 0,
    "Export_evaluated_Pi_gammagamma_2L_P": 0,
    "Export_evaluated_Pi_gammaZ_2L_P": 0,
    "Export_vertex_box_2L_finite_remainder_P": 0,
    "Export_OSW_delta_r_rem_APF_internal_P": 0,
    "Export_DIZET_as_component_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_phase2_missing_terms_source_and_derivation_plan_P():
    """T: Missing-terms source map + derivation plan for the EW 2L coefficient
    ledger. 14 source targets (5 priority-1 Δr, 6 priority-1 sin²θ_eff, 1
    optional, 1 convention, 1 forbidden), 7 gaps mapped to primary sources +
    calculation routes, 7-stage workplan (A→G), 4 forbidden-input tokens,
    7-pack downstream sequence, allowed/prohibited claim language. NO
    physical coefficient closure.
    [P_two_loop_phase2_missing_terms_source_map_and_derivation_plan;
     C_seven_acquisition_packs_pending]."""

    # (a) 14 source targets, with required keys.
    check(len(SOURCE_TARGETS) == 14, f"source-target count: {len(SOURCE_TARGETS)}")
    keys_present = {t.source_key for t in SOURCE_TARGETS}
    required_keys = {
        "FHWWeiglein_2000_complete_fermionic_MW_MZ",
        "FHWWeiglein_2002_MW_MZ_technical",
        "Awramik_Czakon_2002_bosonic_muon_lifetime",
        "Awramik_Czakon_Onishchenko_Veretin_2003_bosonic_Delta_r",
        "Awramik_Czakon_2003_complete_muon_lifetime",
        "ACFW_2004_Wmass_param",
        "ACFW_2004_fermionic_methods",
        "CAF_2006_bosonic_sin2eff_methods",
        "ACF_2006_complete_sin2eff",
        "Denner_2007_on_shell_conventions",
        "ZFITTER_6_42_DIZET",
    }
    missing = required_keys - keys_present
    check(not missing, f"required source keys missing: {missing}")

    # (b) Denner stays convention-only; ZFITTER stays forbidden as component.
    denner = next(t for t in SOURCE_TARGETS if t.source_key == "Denner_2007_on_shell_conventions")
    check(denner.claim_use == "convention_only",
          f"Denner claim_use must be convention_only, got {denner.claim_use!r}")
    zfitter = next(t for t in SOURCE_TARGETS if t.source_key == "ZFITTER_6_42_DIZET")
    check(zfitter.claim_use == "comparator_only_forbidden_as_component",
          f"ZFITTER claim_use must be comparator_only_forbidden_as_component, "
          f"got {zfitter.claim_use!r}")

    # (c) Priority-1 sources include the 5 Δr / muon-lifetime papers.
    priority_1 = {t.source_key for t in SOURCE_TARGETS if t.priority == 1}
    delta_r_required = {
        "FHWWeiglein_2000_complete_fermionic_MW_MZ",
        "FHWWeiglein_2002_MW_MZ_technical",
        "Awramik_Czakon_2002_bosonic_muon_lifetime",
        "Awramik_Czakon_Onishchenko_Veretin_2003_bosonic_Delta_r",
        "Awramik_Czakon_2003_complete_muon_lifetime",
    }
    delta_r_missing = delta_r_required - priority_1
    check(not delta_r_missing, f"priority-1 Δr sources missing: {delta_r_missing}")

    # (d) 7 gaps covering all 4 self-energy channels + vertex form factors +
    #     vertex/box remainder + OSW Δr_rem.
    check(len(GAP_MATRIX) == 7, f"gap matrix row count: {len(GAP_MATRIX)}")
    gap_ids = {g.gap for g in GAP_MATRIX}
    required_gaps = {
        "Sigma_W_2L", "Sigma_Z_2L", "Pi_gammagamma_2L", "Pi_gammaZ_2L",
        "Zll_vertex_2L_form_factors",
        "muon_decay_vertex_box_2L_finite_remainder",
        "OSW_delta_r_rem_APF_internal",
    }
    check(gap_ids == required_gaps,
          f"gap ids mismatch: got {sorted(gap_ids)}, expected {sorted(required_gaps)}")
    for g in GAP_MATRIX:
        check(g.needed.strip() != "" and g.primary_sources.strip() != ""
              and g.calculation_route.strip() != "",
              f"gap {g.gap}: empty needed/primary_sources/calculation_route")

    # (e) 7-stage workplan stages A..G in order.
    check(len(WORKPLAN_STAGES) == 7, f"workplan stage count: {len(WORKPLAN_STAGES)}")
    check(WORKPLAN_STAGES[0].startswith("A_") and WORKPLAN_STAGES[-1].startswith("G_"),
          f"workplan stages not A..G: {WORKPLAN_STAGES}")

    # (f) Forbidden-input tokens for Stage F.
    check(len(FORBIDDEN_INPUT_TOKENS_STAGE_F) == 4,
          f"Stage F forbidden-input token count: {len(FORBIDDEN_INPUT_TOKENS_STAGE_F)}")
    check("DIZET_or_ZFITTER_aggregate_consumed_as_component" in FORBIDDEN_INPUT_TOKENS_STAGE_F,
          "DIZET/ZFITTER component-smuggling guard missing")
    check("measured_M_W_input" in FORBIDDEN_INPUT_TOKENS_STAGE_F,
          "measured_M_W guard missing")
    check("fitted_counterterm" in FORBIDDEN_INPUT_TOKENS_STAGE_F,
          "fitted_counterterm guard missing")

    # (g) 7-pack downstream sequence.
    check(len(DOWNSTREAM_PACK_SEQUENCE) == 7,
          f"downstream pack count: {len(DOWNSTREAM_PACK_SEQUENCE)}")
    check(DOWNSTREAM_PACK_SEQUENCE[0] == "APF_TWO_LOOP_PHASE2_MISSING_SOURCE_ACQUISITION_v1",
          "first downstream pack must be MISSING_SOURCE_ACQUISITION_v1")
    check(DOWNSTREAM_PACK_SEQUENCE[-1] == "APF_TWO_LOOP_PHASE2_OSW_DELTAR_EVALUATOR_v1",
          "last downstream pack must be OSW_DELTAR_EVALUATOR_v1")

    # (h) Claim-language guard: allowed + 4 prohibited.
    check("identifies the missing EW two-loop coefficient sources" in ALLOWED_CLAIM_LANGUAGE,
          "allowed claim language must identify missing sources without promoting closure")
    check(len(PROHIBITED_CLAIM_LANGUAGE) == 4,
          f"prohibited-language count: {len(PROHIBITED_CLAIM_LANGUAGE)}")
    for prohibited in PROHIBITED_CLAIM_LANGUAGE:
        check(prohibited not in ALLOWED_CLAIM_LANGUAGE,
              f"prohibited language leaked into allowed: {prohibited[:60]}...")

    # (i) Honest non-claim flags.
    check(EXPORT_FLAGS["Export_missing_terms_source_map_P"] == 1,
          "source map flag must be 1")
    check(EXPORT_FLAGS["Export_EW_2L_derivation_plan_P"] == 1,
          "derivation plan flag must be 1")
    check(EXPORT_FLAGS["Export_source_certified_EW_2L_diagram_coefficient_ledger_P"] == 0,
          "coefficient ledger must remain 0")
    for non_claim_key in [
        "Export_evaluated_Sigma_W_2L_P", "Export_evaluated_Sigma_Z_2L_P",
        "Export_evaluated_Pi_gammagamma_2L_P", "Export_evaluated_Pi_gammaZ_2L_P",
        "Export_vertex_box_2L_finite_remainder_P",
        "Export_OSW_delta_r_rem_APF_internal_P",
        "Export_DIZET_as_component_P",
    ]:
        check(EXPORT_FLAGS[non_claim_key] == 0,
              f"{non_claim_key} must remain 0, got {EXPORT_FLAGS[non_claim_key]}")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_two_loop_phase2_missing_terms_source_and_derivation_plan: "
              "Source map + derivation plan for the open EW 2L coefficient "
              "ledger. 14 source targets (5 priority-1 Δr/muon-lifetime: "
              "FHW 2000/2002, AC 2002 muon-lifetime, ACOv 2003 bosonic Δr, "
              "AC 2003 complete muon-lifetime; 6 priority-1 sin²θ_eff incl. "
              "ACFW 2004 fermionic PRL + ACF 2006 bosonic result + ACF 2006 "
              "complete + ACFW 2004 W-mass aggregate + CAF 2006 bosonic "
              "methods + ACFW 2004 fermionic methods; 1 optional ACFK 2008 "
              "b̄b; 1 convention-only Denner 2007; 1 forbidden ZFITTER/DIZET). "
              "7 gaps mapped (Σ_W/Σ_Z/Π_γγ/Π_γZ 2L + Z→ℓℓ form factors + "
              "muon-decay vertex/box remainder + OSW Δr_rem). 7-stage "
              "workplan A→G. 4 Stage-F forbidden-input tokens. 7-pack "
              "downstream sequence. Allowed + 4 prohibited claim-language "
              "guards. "
              "[P_two_loop_phase2_missing_terms_source_map_and_derivation_plan; "
              "C_seven_acquisition_packs_pending]"),
        tier=4,
        epistemic="P_two_loop_phase2_missing_terms_source_map_and_derivation_plan",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE2_MISSING_TERMS_"
            "SOURCE_AND_DERIVATION_PLAN_v1. Direct follow-on to the "
            "v24.3.154 current-source no-go: names the 14 acquisition "
            "targets (5 Δr / muon-lifetime + 6 sin²θ_eff + 1 b̄b optional + "
            "1 Denner convention-only + 1 ZFITTER forbidden-component); 7 "
            "gap-to-source rows for the 4 EW self-energy channels + Z→ℓℓ "
            "vertex form factors + muon-decay vertex/box finite remainder + "
            "OSW Δr_rem APF-internal; 7-stage workplan from convention "
            "freeze through aggregate validation; 4 Stage-F forbidden "
            "tokens (measured M_W, DIZET aggregate as component, published "
            "total SM M_W, fitted counterterm); 7-pack downstream sequence "
            "starting with MISSING_SOURCE_ACQUISITION → DELTA_R_SOURCE_IMPORT "
            "→ ZPOLE_DELTA_KAPPA_SOURCE_IMPORT → DIAGRAM_GENERATOR_AND_"
            "PROJECTORS → IBP_REDUCTION_LEDGER → COEFFICIENT_ROW_LEDGER → "
            "OSW_DELTAR_EVALUATOR. Allowed claim-language string + 4 "
            "prohibited claim-language strings banked as discipline guards. "
            "The plan is the next-gate response to the current-source no-go; "
            "executing the plan requires successive sibling packs."
        ),
        key_result=(
            "Missing-terms source map + 7-stage derivation plan + 7-pack "
            "downstream sequence + 4 forbidden-input tokens + claim-language "
            "guard banked. Coefficient ledger still OPEN. "
            "[P_two_loop_phase2_missing_terms_source_map_and_derivation_plan; "
            "C_seven_acquisition_packs_pending]"
        ),
        dependencies=[
            "T_two_loop_phase2_current_source_coefficient_no_go",
            "T_two_loop_phase2_ew_coefficient_ledger_audit_scaffold",
            "T_two_loop_phase2_ew_tex_source_exact_extraction_v2",
        ],
        cross_refs=[
            "T_two_loop_phase2_ew_source_table_extraction_aggregate_and_convention",
            "T_two_loop_phase2_osw_deltar_connector_refusal_toy",
            "T_two_loop_phase2_ew_self_energy_assembly_gate_toy_ledger",
        ],
        artifacts={
            "source_target_count": len(SOURCE_TARGETS),
            "priority_1_count": sum(1 for t in SOURCE_TARGETS if t.priority == 1),
            "uploaded_count": sum(1 for t in SOURCE_TARGETS
                                  if t.current_status.startswith("UPLOADED")),
            "not_uploaded_count": sum(1 for t in SOURCE_TARGETS
                                      if t.current_status.startswith("NOT_UPLOADED")),
            "gap_count": len(GAP_MATRIX),
            "workplan_stages": list(WORKPLAN_STAGES),
            "downstream_pack_sequence": list(DOWNSTREAM_PACK_SEQUENCE),
            "forbidden_input_tokens": list(FORBIDDEN_INPUT_TOKENS_STAGE_F),
            "prohibited_claim_language_count": len(PROHIBITED_CLAIM_LANGUAGE),
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_phase2_missing_terms_source_and_derivation_plan":
        check_T_two_loop_phase2_missing_terms_source_and_derivation_plan_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
