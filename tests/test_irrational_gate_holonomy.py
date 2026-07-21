from apf import irrational_gate_holonomy as ig


def _pass(fn):
    r = fn()
    assert r["passed"], r["fail_reasons"]
    assert r["physical_premises_certified"] is False
    return r


def test_apf_projector_pair_reproduces_12_over_25():
    r = _pass(ig.check_T_apf_345_projector_pair)
    assert r["artifacts"]["commutator"] == [["0", "12/25"], ["-12/25", "0"]]


def test_reflection_product_is_exact_orientation_preserving_gate():
    r = _pass(ig.check_T_reflection_product_irrational_gate)
    assert r["artifacts"]["trace_R"] == "-14/25"
    assert r["artifacts"]["det_R"] == "1"


def test_bounded_cyclic_orbit_supplies_compact_closure():
    r = _pass(ig.check_T_bounded_cyclic_orbit_compact_closure)
    assert r["artifacts"]["basis_determinant"] != "0"
    assert r["artifacts"]["separately_assumed_global_compact_body"] is False


def test_nonintegral_rational_trace_forces_infinite_order_in_compact_group():
    r = _pass(ig.check_T_rational_trace_forces_infinite_order)
    assert r["artifacts"]["trace"] == "-14/25"
    assert r["artifacts"]["powers_checked_nonidentity"] == 256


def test_finite_precision_cannot_prove_exact_infinite_order():
    r = _pass(ig.check_T_finite_precision_cannot_certify_infinite_order)
    assert r["artifacts"]["finite_order_control"]["order"] == 15188
    assert r["artifacts"]["trace_error"] < 3e-8
    assert r["artifacts"]["exact_holonomy_requires_structural_derivation"] is True


def test_one_gate_replaces_connected_sweep():
    r = _pass(ig.check_T_one_gate_dense_held_circle)
    assert r["artifacts"]["connected_sweep_required"] is False
    assert r["artifacts"]["closure"] == "SO(2)"


def test_orbit_mixture_constructs_disk():
    r = _pass(ig.check_T_orbit_mixture_constructs_disk)
    assert r["artifacts"]["all_profiles_distinct"] is True
    assert r["artifacts"]["four_outcome_readout_valid"] is True


def test_finite_resolution_cover_is_strong():
    r = _pass(ig.check_T_finite_resolution_orbit_cover)
    assert r["artifacts"]["N64_max_gap_degrees"] < 7
    assert r["artifacts"]["N256_radial_deficit"] < 2e-4


def test_born_fringe_from_disk_and_sharp_effect():
    r = _pass(ig.check_T_born_fringe_from_one_gate_circle)
    assert r["artifacts"]["probability_at_direct_345_point"] == "4/5"
    assert "cos(theta/2)^2" in r["artifacts"]["fringe_formula"]


def test_live_apf_generators_close_only_with_fpi_and_j():
    r = _pass(ig.check_T_live_apf_generator_closure)
    assert r["artifacts"]["generated_dimension"] == 8
    assert r["artifacts"]["dimension_without_F_Pi"] < 8
    assert r["artifacts"]["dimension_without_J"] < 8


def test_dependency_contract_removes_connected_sweep_and_ledger():
    r = _pass(ig.check_T_one_gate_dependency_contract)
    assert r["artifacts"]["connected_sweep_present"] is False
    assert r["artifacts"]["closed_global_state_body_premise_present"] is False
    assert r["artifacts"]["quadratic_ledger_present"] is False
    assert r["artifacts"]["gate_routes_are_alternatives"] is True
    assert "EXACT_REVERSIBLE_IRRATIONAL_HELD_GATE_DERIVATION" in r["artifacts"]["direct_roots"]
    assert "PHYSICAL_SHARP_REFLECTION_IMPLEMENTABILITY" in r["artifacts"]["reflection_roots"]
    assert "EXACT_REVERSIBLE_IRRATIONAL_HELD_GATE_DERIVATION" not in r["artifacts"]["reflection_roots"]
    assert r["artifacts"]["root_mutation_caught"] is True


def test_source_concordance_keeps_physical_gate_open():
    r = _pass(ig.check_T_source_concordance_and_nonclaim)
    assert "direct_gate" in r["artifacts"]["still_missing"]
    assert r["artifacts"]["headline_license"] == "research route, not APF closure"


def test_reference_certificate_fails_closed():
    r = _pass(ig.check_T_reference_interface_certificate_fail_closed)
    assert r["artifacts"]["synthetic_result"]["physical_premises_certified"] is False
    assert r["artifacts"]["experimental_finite_resolution_result"]["physical_premises_certified"] is False
    assert r["artifacts"]["experimental_finite_resolution_result"]["finite_resolution_interface_certified"] is True
    assert r["artifacts"]["structural_exact_result"]["physical_premises_certified"] is True
    assert r["artifacts"]["empty_digest_mutation"]["physical_premises_certified"] is False
    assert r["artifacts"]["finite_gate_mutation"]["physical_premises_certified"] is False


def test_all_checks_and_certificate():
    results = ig.run_all()
    assert all(r["passed"] for r in results.values())
    cert = ig.build_certificate(results)
    assert cert.finite_precision_exactness_guard
    assert cert.compact_closure_circle
    assert cert.connected_sweep_not_required
    assert cert.physical_gate_realized is False
    assert cert.physical_premises_certified is False


# ---------------------------------------------------------------------------
# Fortification tests (2026-07-20): one adversarial battery per carried
# cold-audit finding.  Physical certification stays refused everywhere.
# ---------------------------------------------------------------------------

from fractions import Fraction as F


def _structural_payload(gate):
    return {
        "evidence_class": "structural_derivation",
        "source_digest": "b" * 64,
        "finite_first_order_carrier_certified": True,
        "occupied_nonzero_profile_certified": True,
        "finite_separating_readout_certified": True,
        "classical_randomization_certified": True,
        "capacity_bounded_orbit_certified": True,
        "effective_gate_action_certified": True,
        "recombination_effect_witness_certified": True,
        "exact_gate_relation_certified": True,
        "finite_resolution_orbit_cover_certified": True,
        "gate_matrix": gate,
    }


def test_major1_verifier_rejects_so11_boost_payload():
    rep = ig.verify_physical_interface_certificate(
        _structural_payload([["5/4", "3/4"], ["3/4", "5/4"]]))
    assert rep["physical_premises_certified"] is False
    assert rep["mathematical_gate_check"] is False
    assert any("elliptic" in f for f in rep["failures"])


def test_major1_verifier_rejects_finite_order_and_nonelliptic_traces():
    for gate in ([["-1/2", "-1"], ["3/4", "-1/2"]],
                 [["1/2", "-1"], ["3/4", "1/2"]],
                 [["1", "1"], ["0", "1"]],
                 [["3", "1"], ["2", "1"]],
                 [["0", "-1"], ["1", "0"]]):
        rep = ig.verify_physical_interface_certificate(_structural_payload(gate))
        assert rep["physical_premises_certified"] is False
        assert rep["mathematical_gate_check"] is False


def test_major1_verifier_still_accepts_true_gate_structural():
    rep = ig.verify_physical_interface_certificate(
        _structural_payload([["-7/25", "-24/25"], ["24/25", "-7/25"]]))
    assert rep["physical_premises_certified"] is True
    assert rep["mathematical_gate_check"] is True


def test_major1_fail_closed_battery_includes_boost_and_trace_controls():
    r = _pass(ig.check_T_reference_interface_certificate_fail_closed)
    bm = r["artifacts"]["boost_gate_mutation"]
    assert bm["physical_premises_certified"] is False
    assert bm["mathematical_gate_check"] is False
    tsc = r["artifacts"]["trace_set_controls"]
    assert set(tsc) == {"order_3_trace_minus_1", "order_6_trace_plus_1",
                        "unipotent_shear_trace_2", "hyperbolic_trace_4"}
    for rep in tsc.values():
        assert rep["physical_premises_certified"] is False
        assert rep["mathematical_gate_check"] is False


def test_major2_compactness_check_executes_failure_directions():
    r = _pass(ig.check_T_bounded_cyclic_orbit_compact_closure)
    g = r["artifacts"]["boost_growth_certificate"]
    assert g["eigenvector"] == ["1", "1"] and g["eigenvalue"] == "2"
    assert g["orbit_sup_strictly_growing"] is True
    assert g["exits_readout_simplex"] is True
    s = r["artifacts"]["one_sided_insufficiency_control"]
    assert s["seed_cyclic"] is False
    assert s["forward_orbit_bounded"] is True
    assert s["backward_orbit_strictly_growing"] is True
    assert r["artifacts"]["forward_iterates_checked"] == \
        ig.EVIDENCE_STRENGTH["orbit_prefix_two_sided"]


def test_major3_named_math_imports_registered():
    assert set(ig.NAMED_MATH_IMPORTS) == {
        "BOUNDED_SUBGROUP_COMPACT_CLOSURE_general_case",
        "COMPACT_SUBGROUP_CONJUGATES_INTO_O2_averaging_John_ellipsoid",
        "CLOSED_SUBGROUPS_OF_SO2_finite_cyclic_or_full_Kronecker_density",
    }
    r = _pass(ig.check_T_one_gate_dense_held_circle)
    assert r["artifacts"]["named_math_imports"] == list(ig.NAMED_MATH_IMPORTS)


def test_major3_closure_conclusion_is_derived_with_live_controls():
    r = _pass(ig.check_T_one_gate_dense_held_circle)
    d = r["artifacts"]["closure_derivation"]
    assert d["branch"] == "infinite_compact_oriented"
    assert d["invariance_algebra_dim"] == 1 and d["so_n_expected_dim"] == 1
    assert d["carrier_dim"] == 2
    assert r["artifacts"]["closure"] == "SO(2)"
    assert r["artifacts"]["finite_cyclic_control"]["branch"] == "finite_cyclic"
    assert r["artifacts"]["boost_control"]["branch"] == "no_certified_compact_closure"


def test_major3_disposition_helper_cannot_reach_so2_on_wrong_instances():
    eye = ((F(1), F(0)), (F(0), F(1)))
    quarter = ((F(0), F(-1)), (F(1), F(0)))
    d = ig._closure_disposition(quarter, eye, False)
    assert d["branch"] == "finite_cyclic" and d["finite_order_found"] == 4
    boost = ((F(5, 4), F(3, 4)), (F(3, 4), F(5, 4)))
    d2 = ig._closure_disposition(boost, eye, True)
    assert d2["branch"] == "no_certified_compact_closure"


def test_major4_gaussian_integer_certificate_is_primary():
    r = _pass(ig.check_T_rational_trace_forces_infinite_order)
    assert r["artifacts"]["gaussian_certificate_primary"] is True
    g = r["artifacts"]["gaussian_integer_certificate"]
    assert g["square_relation_verified"] is True
    assert "(3+4i)^2" in g["square_relation"] and "(2+i)^4" in g["square_relation"]
    assert g["distinct_powers_computed"] == 24
    assert "banked H3" in g["prior_art"]


def test_minor2_minor4_powers_checked_derived_and_pinned():
    r = _pass(ig.check_T_rational_trace_forces_infinite_order)
    assert r["artifacts"]["powers_checked_nonidentity"] == \
        ig.EVIDENCE_STRENGTH["power_scan_nonidentity"] == 256
    rb = _pass(ig.check_T_bounded_cyclic_orbit_compact_closure)
    assert rb["artifacts"]["all_readouts_normalized"] is True
    ro = _pass(ig.check_T_orbit_mixture_constructs_disk)
    assert ro["artifacts"]["orbit_prefix_checked"] == \
        ro["artifacts"]["orbit_prefix_pinned"] == \
        ig.EVIDENCE_STRENGTH["disk_orbit_prefix"]


def test_minor1_born_fringe_boundedness_scan_executed():
    r = _pass(ig.check_T_born_fringe_from_one_gate_circle)
    assert r["artifacts"]["c_zero_bounded_on_orbit_prefix"] is True
    assert r["artifacts"]["orbit_scan_points"] == \
        ig.EVIDENCE_STRENGTH["fringe_scan_points"]
    assert len(r["artifacts"]["nonzero_tilt_violations"]) == 8


def test_minor5_projector_direction_pinned():
    r = _pass(ig.check_T_apf_345_projector_pair)
    assert r["artifacts"]["direction_pinned"] is True
    assert r["artifacts"]["P_u"][0][0] == "9/25"
    assert r["artifacts"]["P_u"][1][1] == "16/25"


def test_major4_source_concordance_discloses_h3_prior_art():
    r = _pass(ig.check_T_source_concordance_and_nonclaim)
    row = r["artifacts"]["live_sources"]["infinite_order_certificate_prior_art"]
    assert "R = R35^2" in row and "_held_holonomy_groups.py" in row
