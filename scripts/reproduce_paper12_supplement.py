#!/usr/bin/env python3
"""Reproduce the Paper 12 Technical Supplement's cited checks, end to end.

Runs exactly the bank checks the Paper 12 Technical Supplement coderefs --
the strong-sector record/contextuality corpus, the v24.3.372 review-2
landings (general-N record extension, the Delta-calculus, the SU(2)
string-cut testbed), and the foundational spine + carve anchors the
supplement's dependency lists cite (core.py spine, FD1 completeness, the
gauge.py anchors, the YM MD-bridge legs, the record-sector fences) --
and prints a result table:

    check name | module | passed | epistemic token

Runnable from the repo root:

    python3 scripts/reproduce_paper12_supplement.py

Exits nonzero on any failure (a check failing, raising, or failing to
import). Result-format note: older strong-sector checks return
{'consistent': bool, 'status': <token>}; newer modules return
{'passed': bool, 'epistemic': <token>} -- both are handled.
"""
import importlib
import os
import sys
import time

# make the script runnable from repo root OR from scripts/
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# (module, check function name) -- exactly the supplement's coderef surface.
SUPPLEMENT_CHECKS = (
    # --- the v24.3.372 review-2 landings (this pass) -----------------------
    ("apf.gauge_invariant_record", "check_T_gauge_invariant_colour_record_general_N"),
    ("apf.delta_calculus", "check_T_delta_disjoint_additivity"),
    ("apf.delta_calculus", "check_T_delta_coarse_graining_monotonicity"),
    ("apf.delta_calculus", "check_T_cost_count_characterization"),
    ("apf.su2_string_cut_testbed", "check_T_su2_string_cut_comovement"),
    ("apf.su2_string_cut_testbed", "check_T_su2_string_cut_native_algebra"),
    # Round-4/5/6 review-response checks (v24.3.379/.380/.381, 2026-07-04)
    ("apf.gauge_invariant_record", "check_T_su3_octet_M4_explicit_construction"),
    ("apf.anchor_center_correspondence", "check_T_anchor_set_is_electric_center_data"),
    ("apf.anchor_center_correspondence", "check_T_delta_vs_centre_entropy_diagnoses"),
    ("apf.delta_calculus", "check_T_delta_not_an_information_functional"),
    ("apf.delta_calculus", "check_T_register_reading_grounds_ceil_log2_count"),
    ("apf.delta_calculus", "check_T_delta_JR_derived"),
    ("apf.delta_calculus", "check_T_delta_chain_rule_conditional_expectation_dichotomy"),
    ("apf.anchor_support_algebra", "check_T_anchor_support_formalization"),
    # Round-7 review-response checks (v24.3.383, 2026-07-04)
    ("apf.su2_string_cut_testbed", "check_T_no_negative_delta_at_gauge_cut_family"),
    ("apf.gauge_invariant_record", "check_T_product_group_sharp_records_factorwise"),
    # --- the MD bridge + triality anchors ----------------------------------
    ("apf.yang_mills_md_bridge", "check_T_contextuality_implies_superadditive_cost"),
    ("apf.gauge", "check_T_center_order_parameter_triality"),
    # --- the record-family parents + multiplicity trichotomy + connection --
    ("apf.gauge_invariant_record",
     "check_T_only_gauge_invariant_sharp_colour_record_is_nonfactorizable_singlet_P"),
    ("apf.gauge_invariant_record",
     "check_T_unique_gauge_invariant_colour_state_of_N_fundamentals_is_entangled_baryon_P"),
    ("apf.gauge_invariant_record", "check_T_canonical_colour_record_iff_multiplicity_free_P"),
    ("apf.base_fiber_allocation", "check_T_gauge_connection_is_gauge_variant_convention_P"),
    # --- the contextuality census family (gauge_invariant_record) ----------
    ("apf.gauge_invariant_record", "check_T_gauge_invariant_colour_interface_is_contextual"),
    ("apf.gauge_invariant_record",
     "check_T_gauge_invariant_colour_interface_state_independent_contextual"),
    ("apf.gauge_invariant_record", "check_T_gauge_invariant_colour_KS_coloring_obstruction"),
    ("apf.gauge_invariant_record", "check_T_su3_octet_colour_KS_coloring_obstruction_exact"),
    ("apf.gauge_invariant_record",
     "check_T_chiral_condensate_flavour_density_interface_is_contextual"),
    ("apf.gauge_invariant_record", "check_T_exotic_gauge_invariant_algebra_is_nonabelian"),
    # --- branch verdict robustness ------------------------------------------
    ("apf.quantum_admissibility", "check_T_contextual_branch_verdict_threshold_robust"),
    # --- the drawn-content readings family (all six) ------------------------
    ("apf.drawn_content_readings", "check_T_magic_square_solution_group_rep_forces_4n"),
    ("apf.drawn_content_readings", "check_T_drawn_content_readings_functional"),
    ("apf.drawn_content_readings", "check_T_sm_interface_generation_qutrit_readings"),
    ("apf.drawn_content_readings", "check_T_gluonic_content_readings"),
    ("apf.drawn_content_readings", "check_T_reading_coverage_sweep"),
    ("apf.drawn_content_readings", "check_T_lr_divisibility_extended_scan"),
    # --- the 't Hooft anomaly-matching family (all five) --------------------
    ("apf.thooft_anomaly_matching_chiral",
     "check_T_thooft_matching_symmetric_vacuum_no_go_conditional"),
    ("apf.thooft_anomaly_matching_chiral",
     "check_T_vafa_witten_selects_su3v_pattern_conditional"),
    ("apf.thooft_anomaly_matching_chiral", "check_T_pi0_two_photon_anomaly_row"),
    ("apf.thooft_anomaly_matching_chiral",
     "check_T_stern_phase_custodial_exclusion_conditional"),
    ("apf.thooft_anomaly_matching_chiral",
     "check_T_vafa_witten_strong_parity_not_spontaneously_broken_conditional"),
    # --- the FeasBool engine / defender bridge / IE adapter trio ------------
    ("apf.ijc_feasbool_engine", "check_T_feasbool_general_contextuality"),
    ("apf.ijc_boolean_defender_bridge", "check_T_ijc_boolean_defender_bridge"),
    ("apf.interface_contextuality_adapter", "check_T_interface_contextuality_adapter"),
    # --- the foundational spine + carve anchors (cited by the Paper 12 carve
    #     and the supplement's dependency lists; completed 2026-07-04) --------
    ("apf.core", "check_T_M"),
    ("apf.core", "check_L_loc"),
    ("apf.core", "check_L_irr"),
    ("apf.core", "check_L_epsilon_star"),
    ("apf.core", "check_T_canonical"),
    ("apf.core", "check_T_alg"),
    ("apf.core", "check_T3"),
    ("apf.foundation_inputs", "check_FD1_structural_completeness"),
    ("apf.gauge", "check_T_gauge"),
    ("apf.gauge", "check_L_gauge_template_uniqueness"),
    ("apf.gauge", "check_T_field"),
    ("apf.gauge", "check_T_confinement"),
    ("apf.generations", "check_L_AF_capacity"),
    # --- the YM MD-bridge legs + the record-sector fences --------------------
    ("apf.yang_mills_md_bridge", "check_T_ym_ir_endpoint_trichotomy_branch2_open"),
    ("apf.yang_mills_md_bridge", "check_T_ym_conformal_phase_excluded_by_record_locking"),
    ("apf.yang_mills_md_bridge", "check_T_ym_lattice_substrate_admissible"),
    ("apf.gauge_invariant_record", "check_T_matter_free_colour_record_deep_superselection_no_go"),
    ("apf.gauge_invariant_record", "check_T_colour_contextuality_is_kstring_spectrum_blind"),
)


def _passed(result):
    if not isinstance(result, dict):
        return False
    if "passed" in result:
        return bool(result["passed"])
    if "consistent" in result:
        return bool(result["consistent"])
    return False


def _epistemic(result):
    if not isinstance(result, dict):
        return "?"
    return str(result.get("epistemic") or result.get("status") or "?")


def main():
    rows = []
    any_fail = False
    t_total = time.time()
    for mod_name, fn_name in SUPPLEMENT_CHECKS:
        t0 = time.time()
        try:
            mod = importlib.import_module(mod_name)
            fn = getattr(mod, fn_name)
            result = fn()
            ok = _passed(result)
            tok = _epistemic(result)
        except Exception as exc:  # noqa: BLE001 -- a raising check is a FAIL
            ok = False
            tok = f"RAISED: {type(exc).__name__}: {exc}"
        any_fail = any_fail or (not ok)
        rows.append((fn_name, mod_name.replace("apf.", "") + ".py",
                     "PASS" if ok else "FAIL", tok, time.time() - t0))

    w1 = max(len(r[0]) for r in rows)
    w2 = max(len(r[1]) for r in rows)
    print(f"{'check name':<{w1}} | {'module':<{w2}} | passed | epistemic token")
    print("-" * (w1 + w2 + 40))
    for name, mod, ok, tok, dt in rows:
        print(f"{name:<{w1}} | {mod:<{w2}} | {ok:<6} | {tok}  ({dt:.1f}s)")
    n_pass = sum(1 for r in rows if r[2] == "PASS")
    print("-" * (w1 + w2 + 40))
    print(f"{n_pass}/{len(rows)} PASS in {time.time() - t_total:.1f}s")
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
