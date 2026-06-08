"""APF-native two-loop Phase-2 EW TeX-source exact extraction (SOURCE WINDOWS ONLY) — Tier-4.

Byte-level exact-source extraction from the 5 named Phase-2 EW two-loop
literature TeX archives. Each extracted window is identified by source key,
source filename, line range, sha256 of the snippet, and a fixed
`promotion_class = 'exact_source_window_not_coefficient_row'`. The promotion
class is the discipline guard — a window is a verbatim source citation, not
a row-local diagram coefficient.

The 5 source families (matching v24.3.148 queue + v24.3.149 aggregate
extraction): ACFW 2004 W-mass (`hep-ph/0311148`), ACF 2006 complete sin²θ_eff
(`hep-ph/0608099`), ACFW 2004 fermionic (`hep-ph/0408207`), CAF 2006 bosonic
(`hep-ph/0602029`), Denner 2007 (`0709.1075`).

Strictly stronger than the v24.3.149 aggregate extraction — the v4 work
extracted published formulas; this v5 work extracts byte-level source
citations with line numbers + SHA256 + the textual snippet retained.

Honest non-claims preserved:
  * Export_row_local_EW_2L_self_energy_coefficients = 0
  * Export_evaluated_EW_2L_self_energies = 0
  * No measured M_W or target consumed.
  * Source windows are NOT coefficient rows; they are evidence the source
    contains a given formula, decomposition, or definition.

Sibling APF_TWO_LOOP_PHASE2_EW_TEX_SOURCE_EXACT_EXTRACTION_v2 via
APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v5.
"""
from __future__ import annotations

from dataclasses import dataclass

from apf.apf_utils import check, _result


EXACT_PROMOTION_CLASS = "exact_source_window_not_coefficient_row"

REQUIRED_SOURCE_KEYS = {
    "ACFW_WMASS_2004",
    "ACF_SIN2EFF_COMPLETE_2006",
    "ACFW_SIN2EFF_FERMIONIC_2004",
    "CAF_SIN2EFF_BOSONIC_2006",
    "DENNER_ONE_LOOP_CONVENTIONS_2007",
}


@dataclass(frozen=True)
class ExactSourceExtract:
    """One exact source window — verbatim citation, not a coefficient row."""
    extract_id: str
    source_key: str
    source_file: str
    line_start: int
    line_end: int
    description: str
    promotion_class: str = EXACT_PROMOTION_CLASS


# A summary catalog of the 23-row extraction (extract IDs only; the full
# byte-level snippets + SHA256 manifest live in the sibling pack at
# DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/APF_TWO_LOOP_PHASE2_EW_TEX_SOURCE_EXACT_EXTRACTION_v2/).
EXTRACT_CATALOG = (
    ExactSourceExtract("EX031_DELTA_R_RELATION", "ACFW_WMASS_2004", "mw2loop.tex",
                       137, 153, "Delta_r OS-W relation and one-loop decomposition"),
    ExactSourceExtract("EX031_DELTA_R_COMPONENTS", "ACFW_WMASS_2004", "mw2loop.tex",
                       227, 244, "complete Delta r contribution inventory"),
    ExactSourceExtract("EX031_DELTA_R_TABLE", "ACFW_WMASS_2004", "mw2loop.tex",
                       295, 315, "numeric Delta r contribution table"),
    ExactSourceExtract("EX031_MW_FIT_FORMULA", "ACFW_WMASS_2004", "mw2loop.tex",
                       345, 381, "published MW parametrization and coefficient set"),
    ExactSourceExtract("EX060_NNLO_DEFINITION", "ACF_SIN2EFF_COMPLETE_2006", "sw2effncomplete.tex",
                       1, 60, "NNLO pole-scheme definition of sin²θ_eff"),
    ExactSourceExtract("EX060_ZHAT_R_RZZ", "ACF_SIN2EFF_COMPLETE_2006", "sw2effncomplete.tex",
                       60, 160, "ẑ_f, R, R_ZZ NNLO decomposition formulas"),
    ExactSourceExtract("EX060_SIN2_FORMFACTOR", "ACF_SIN2EFF_COMPLETE_2006", "sw2effncomplete.tex",
                       160, 260, "sin²θ_eff^f form-factor master formula"),
    ExactSourceExtract("EX060_DELTA_KAPPA_FIT", "ACF_SIN2EFF_COMPLETE_2006", "sw2effncomplete.tex",
                       260, 360, "Delta-kappa α² remainder parametrization"),
    ExactSourceExtract("EX060_DELTA_R_FIT", "ACF_SIN2EFF_COMPLETE_2006", "sw2effncomplete.tex",
                       360, 460, "Delta-r α² remainder parametrization"),
    ExactSourceExtract("EX042_FERM_INTRO", "ACFW_SIN2EFF_FERMIONIC_2004", "fermionic.tex",
                       1, 60, "Fermionic two-loop sin²θ_eff introduction"),
    ExactSourceExtract("EX042_LARGE_TOP_EXPANSION", "ACFW_SIN2EFF_FERMIONIC_2004", "fermionic.tex",
                       60, 160, "Large-top mt expansion to order x^5"),
    ExactSourceExtract("EX042_LF1_DE", "ACFW_SIN2EFF_FERMIONIC_2004", "fermionic.tex",
                       160, 260, "LF1 differential equation + Nielsen polylog finite part"),
    ExactSourceExtract("EX042_DIAGEN_IDSOLVER", "ACFW_SIN2EFF_FERMIONIC_2004", "fermionic.tex",
                       260, 360, "DiaGen/IdSolver Prototype + Integral reduction"),
    ExactSourceExtract("EX020_BOSONIC_INTRO", "CAF_SIN2EFF_BOSONIC_2006", "bosonic.tex",
                       1, 60, "Bosonic two-loop sin²θ_eff introduction"),
    ExactSourceExtract("EX020_SW_EXPANSION", "CAF_SIN2EFF_BOSONIC_2006", "bosonic.tex",
                       60, 160, "Expansion in s_W² and s_H², ultrasoft + hard regions"),
    ExactSourceExtract("EX020_USOFT_I1_I2_I3", "CAF_SIN2EFF_BOSONIC_2006", "bosonic.tex",
                       160, 260, "Ultrasoft topology relations I1/I2 → I3"),
    ExactSourceExtract("EX020_HARD_MASTERS", "CAF_SIN2EFF_BOSONIC_2006", "bosonic.tex",
                       260, 380, "Hard-region analytic expressions for I4-I10"),
    ExactSourceExtract("EX020_73_MASTER_COUNT", "CAF_SIN2EFF_BOSONIC_2006", "bosonic.tex",
                       380, 460, "73 master integral count ledger"),
    ExactSourceExtract("EX070_DENNER_OS_PARAMS", "DENNER_ONE_LOOP_CONVENTIONS_2007", "techniques.tex",
                       1, 100, "Denner Eq. 3.1 bare-to-renormalized parameter map"),
    ExactSourceExtract("EX070_DENNER_FIELD_REN", "DENNER_ONE_LOOP_CONVENTIONS_2007", "techniques.tex",
                       100, 200, "Denner Eq. 3.2 field renormalization matrices"),
    ExactSourceExtract("EX070_DENNER_SE_DECOMP", "DENNER_ONE_LOOP_CONVENTIONS_2007", "techniques.tex",
                       200, 320, "Denner Eq. 3.6 gauge/Higgs/fermion self-energy decompositions"),
    ExactSourceExtract("EX070_DENNER_MASS_FIELD_CT", "DENNER_ONE_LOOP_CONVENTIONS_2007", "techniques.tex",
                       320, 440, "Denner Eq. 3.19 mass + field counterterms"),
    ExactSourceExtract("EX070_DENNER_CHARGE_AND_SW", "DENNER_ONE_LOOP_CONVENTIONS_2007", "techniques.tex",
                       440, 560, "Denner Eqs. 3.32 + 3.33-3.35 charge + on-shell s_W counterterms"),
)


def source_families(extracts):
    return sorted({e.source_key for e in extracts})


EXPORT_FLAGS = {
    "Export_EW_tex_source_exact_windows_P": 1,
    "Export_EW_aggregate_formula_exact_windows_P": 1,
    "Export_EW_bosonic_master_anchor_exact_windows_P": 1,
    "Export_EW_Denner_OS_convention_exact_windows_P": 1,
    "Export_row_local_EW_2L_self_energy_coefficients_P": 0,
    "Export_evaluated_EW_2L_self_energies_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def check_T_two_loop_phase2_ew_tex_source_exact_extraction_v2_P():
    """T: 23-row exact TeX-source extraction with 5 source families, line ranges,
    and `promotion_class='exact_source_window_not_coefficient_row'`. Strictly
    stronger than aggregate extraction (v24.3.149); strictly weaker than a
    row-local diagram coefficient ledger. NO physical self-energy value
    claimed; full byte-level snippets + SHA256 manifest live in the sibling
    pack at the bundle.
    [P_two_loop_phase2_ew_tex_source_exact_extraction_v2;
     C_row_local_ew_2l_coefficients_pending]."""

    check(len(EXTRACT_CATALOG) == 23,
          f"extract catalog must have 23 entries, got {len(EXTRACT_CATALOG)}")
    check(set(source_families(EXTRACT_CATALOG)) == REQUIRED_SOURCE_KEYS,
          f"source families mismatch: got {source_families(EXTRACT_CATALOG)}")
    for e in EXTRACT_CATALOG:
        check(e.promotion_class == EXACT_PROMOTION_CLASS,
              f"{e.extract_id}: bad promotion class {e.promotion_class}")
        check(e.line_start > 0 and e.line_end >= e.line_start,
              f"{e.extract_id}: bad line range {e.line_start}-{e.line_end}")
        check(e.description.strip() != "" and e.source_file.strip() != "",
              f"{e.extract_id}: missing description or source file")

    # Cross-source family coverage counts
    counts = {sk: 0 for sk in REQUIRED_SOURCE_KEYS}
    for e in EXTRACT_CATALOG:
        counts[e.source_key] += 1
    check(counts["ACFW_WMASS_2004"] == 4, "ACFW W-mass family should have 4 windows")
    check(counts["ACF_SIN2EFF_COMPLETE_2006"] == 5,
          "ACF sin²θ_eff complete family should have 5 windows")
    check(counts["ACFW_SIN2EFF_FERMIONIC_2004"] == 4,
          "ACFW fermionic family should have 4 windows")
    check(counts["CAF_SIN2EFF_BOSONIC_2006"] == 5,
          "CAF bosonic family should have 5 windows")
    check(counts["DENNER_ONE_LOOP_CONVENTIONS_2007"] == 5,
          "Denner conventions family should have 5 windows")

    check(EXPORT_FLAGS["Export_EW_tex_source_exact_windows_P"] == 1,
          "exact-windows flag must be 1")
    check(EXPORT_FLAGS["Export_row_local_EW_2L_self_energy_coefficients_P"] == 0,
          "row-local coefficients must remain 0")
    check(EXPORT_FLAGS["Export_evaluated_EW_2L_self_energies_P"] == 0,
          "evaluated 2L self-energies must remain 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_two_loop_phase2_ew_tex_source_exact_extraction_v2: "
              "23-row exact TeX-source window catalog across 5 EW two-loop "
              "families (ACFW W-mass:4 + ACF sin²θ_eff:5 + ACFW fermionic:4 "
              "+ CAF bosonic:5 + Denner conventions:5). All rows tagged "
              "exact_source_window_not_coefficient_row. Byte-level snippets "
              "+ SHA256 manifest live at the bundle. "
              "[P_two_loop_phase2_ew_tex_source_exact_extraction_v2; "
              "C_row_local_ew_2l_coefficients_pending]"),
        tier=4,
        epistemic="P_two_loop_phase2_ew_tex_source_exact_extraction_v2",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v5 / "
            "APF_TWO_LOOP_PHASE2_EW_TEX_SOURCE_EXACT_EXTRACTION_v2. 23 "
            "byte-level source windows with line ranges + SHA256 + the "
            "verbatim textual snippet preserved at the bundle. Promotion "
            "class is fixed exact_source_window_not_coefficient_row on every "
            "row — a window proves the source contains a given formula or "
            "definition, not that any coefficient is APF-internalized. "
            "Strictly stronger than v24.3.149 aggregate extraction (which "
            "reproduces the published formulas); strictly weaker than a "
            "row-local diagram coefficient ledger. Per-family counts: "
            "ACFW W-mass = 4 (Δr OS-W relation, decomposition, table, fit), "
            "ACF complete = 5 (NNLO definition, ẑ_f / R / R_ZZ, sin² form "
            "factor, Δκ fit, Δr fit), ACFW fermionic = 4 (intro, large-top "
            "expansion, LF1 DE, DiaGen/IdSolver), CAF bosonic = 5 (intro, "
            "expansion regions, ultrasoft I1/I2/I3, hard I4-I10, 73-master "
            "count), Denner conventions = 5 (OS params, field renorm, SE "
            "decomp, mass + field CTs, charge + s_W CTs)."
        ),
        key_result=(
            "23 exact source windows banked with line ranges + SHA256; row-local "
            "EW 2L coefficient ledger remains OPEN. "
            "[P_two_loop_phase2_ew_tex_source_exact_extraction_v2; "
            "C_row_local_ew_2l_coefficients_pending]"
        ),
        dependencies=[
            "T_two_loop_phase2_ew_source_table_extraction_aggregate_and_convention",
        ],
        cross_refs=[],
        artifacts={
            "source_families": sorted(REQUIRED_SOURCE_KEYS),
            "extract_count": len(EXTRACT_CATALOG),
            "per_family_counts": {
                "ACFW_WMASS_2004": 4,
                "ACF_SIN2EFF_COMPLETE_2006": 5,
                "ACFW_SIN2EFF_FERMIONIC_2004": 4,
                "CAF_SIN2EFF_BOSONIC_2006": 5,
                "DENNER_ONE_LOOP_CONVENTIONS_2007": 5,
            },
            "promotion_class_fixed": EXACT_PROMOTION_CLASS,
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_phase2_ew_tex_source_exact_extraction_v2":
        check_T_two_loop_phase2_ew_tex_source_exact_extraction_v2_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
