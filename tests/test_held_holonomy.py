"""Adversarial tests for :mod:`apf.held_holonomy`."""

from apf import held_holonomy as hh


def _passed(result):
    assert result["passed"], result["fail_reasons"]
    assert result["physical_premises_certified"] is False
    return result


def test_relative_loop_group_well_defined():
    r = _passed(hh.check_T_held_relative_loop_group())
    assert r["artifacts"]["quotient_class_count"] == 2
    assert r["artifacts"]["torsor_group_distinction_kept"]


def test_one_sided_congruence_negative_control():
    r = _passed(hh.check_T_held_relative_loop_group())
    assert r["artifacts"]["one_sided_failure"] is not None


def test_recombination_forces_nontrivial_operational_loop():
    r = _passed(hh.check_T_held_recombination_nontriviality())
    assert r["artifacts"]["operational_relative_loop"] == 1


def test_multiplicity_alone_is_insufficient():
    r = _passed(hh.check_T_held_recombination_nontriviality())
    assert r["artifacts"]["multiplicity_only_relative_loop"] == 0


def test_discrete_exchange_fails_connectedness():
    r = _passed(hh.check_T_held_connected_subgroup_so2())
    assert r["artifacts"]["finite_disconnected_controls"]["C_2"]["connected"] is False


def test_nontrivial_connected_so2_subgroup_is_full_circle():
    r = _passed(hh.check_T_held_connected_subgroup_so2())
    assert r["artifacts"]["nontrivial_connected_result"] == "SO(2)"


def test_ledger_adjoint_inverse_forces_isometry():
    r = _passed(hh.check_T_reversible_ledger_isometry())
    assert r["artifacts"]["canonical_route"] == "T^sharp = T^-1"
    assert r["artifacts"]["T_inverse"] == r["artifacts"]["T_sharp"]


def test_forward_contraction_only_is_not_isometry():
    r = _passed(hh.check_T_reversible_ledger_isometry())
    assert r["artifacts"]["two_sided_monotonicity_role"] == "auxiliary only"
    assert r["artifacts"]["inverse_contraction_gap"][0][0].startswith("-")


def test_first_jet_minimum_rank_two():
    r = _passed(hh.check_T_bipolar_first_jet_rank_two())
    assert r["artifacts"]["minimum_complete_rank"] == 2
    assert r["artifacts"]["not_the_tesseract_rank_four_claim"]


def test_quarter_turn_defines_complex_structure():
    r = _passed(hh.check_T_held_circle_quarter_turn())
    assert "J^2=-I" in r["artifacts"]["relations"]
    assert r["artifacts"]["half_turn_is_derived"]


def test_scalar_jet_maps_are_natural():
    r = _passed(hh.check_T_held_jet_naturality())
    assert len(r["artifacts"]["scalar_derivatives_checked"]) >= 7


def test_anisotropic_map_negative_control():
    r = _passed(hh.check_T_held_jet_naturality())
    assert r["artifacts"]["anisotropic_control"] == [["2", "0"], ["0", "1"]]


def test_central_square_minus_one_selects_complex_blocks():
    r = _passed(hh.check_T_central_complex_block_exclusion())
    dims = r["artifacts"]["center_dimensions"]
    assert dims["M2(R)"] == 1
    assert dims["H"] == 1
    assert dims["realified_M2(C)"] == 2
    assert r["artifacts"]["quaternion_i_central"] is False
    assert r["artifacts"]["complex_J_central"] is True


def test_sat_countermodel_bypassed_not_refuted():
    r = _passed(hh.check_T_SAT_countermodel_is_bypassed_not_refuted())
    assert r["artifacts"]["SAT_status"] == "retired_as_unnecessary_not_refuted"
    assert r["artifacts"]["nontrivial_connected_holonomy_present"] is False


def test_dependency_graph_has_no_positivity_cycle():
    r = _passed(hh.check_T_held_holonomy_dependency_contract())
    assert r["artifacts"]["canonical_cycle"] is None
    assert r["artifacts"]["positivity_cycle_mutation_detected"]
    assert r["artifacts"]["centrality_requires_H7"]
    assert r["artifacts"]["centrality_requires_generator_completeness"]
    assert r["artifacts"]["H6_requires_Lie_image"]
    graph = r["artifacts"]["dependency_contract"]
    assert "EFFECTIVE_IMAGE_LIE_SUBGROUP" in graph["H6"]
    assert "GENERATOR_COMPLETENESS" not in graph["H7"]
    assert "GENERATOR_COMPLETENESS" in graph["CENTRAL_COMPLEX_TYPE"]
    assert r["artifacts"]["H1_requires_reversal_inverse"]
    assert r["artifacts"]["H2_is_operational_scope"]
    assert "REVERSAL_IS_INVERSE" in graph["H1"]
    assert "FAITHFUL_ACTION" not in graph["H2"]
    assert "FAITHFUL_ACTION" in graph["H6"]
    assert "CONTINUOUS_ORIENTATION_TRANSPORT" in graph["H7"]
    assert "CLOSED_WORLD_RECORD_COMPLETENESS" in graph["H7"]


def test_group_check_carries_monoid_countermodel_and_torsor_leg():
    r = _passed(hh.check_T_held_relative_loop_group())
    cm = r["artifacts"]["monoid_countermodel"]
    assert cm["reversal_admitted"] is True
    assert cm["inverse_exists"] is False
    assert r["artifacts"]["torsor_action_free_and_transitive"]
    assert "reversed_loop_is_inverse" in r["premises"]


def test_recombination_check_is_operationally_scoped():
    r = _passed(hh.check_T_held_recombination_nontriviality())
    assert r["artifacts"]["operational_relative_loop"] == 1
    assert "effective_relative_loop" not in r["artifacts"]
    kd = r["artifacts"]["kernel_death_control"]
    assert kd["operationally_distinguished"] is True
    assert kd["first_jet_action_is_identity"] is True
    assert r["artifacts"]["representation_constant_on_classes"] is True


def test_connected_subgroup_check_bills_import_and_computes_witnesses():
    r = _passed(hh.check_T_held_connected_subgroup_so2())
    assert "imported" in r["artifacts"]["classification_execution_status"]
    iow = r["artifacts"]["infinite_order_witness"]
    assert iow["distinct_powers_computed"] == 24
    pb = r["artifacts"]["parametrization_battery"]
    assert pb["compositions_checked"] > 0
    assert pb["half_turn"] == "R(1)^2"


def test_isometry_check_discriminates_indefinite_signature():
    r = _passed(hh.check_T_reversible_ledger_isometry())
    ind = r["artifacts"]["indefinite_form_control"]
    assert ind["passes_isometry_schema"] is True
    assert ind["passes_sharp_inverse_schema"] is True
    assert ind["orthogonal"] is False
    assert ind["power_growth_strict"] is True


def test_first_jet_check_computes_jets():
    r = _passed(hh.check_T_bipolar_first_jet_rank_two())
    assert r["artifacts"]["jets_computed_from_coefficients"] is True


def test_cli_certificate_marks_physical_premises_uncertified():
    results = hh.run_all()
    cert = hh.build_certificate(results)
    assert all(result["passed"] for result in results.values())
    assert cert.physical_premises_certified is False
    assert cert.dependency_contract_acyclic
    assert "effective_image_is_a_Lie_subgroup_of_SO2" in cert.dependencies
    assert "orientation_synchronization_across_typed_sectors" in cert.dependencies
    assert "finite_real_Cstar_completion" in cert.dependencies
    assert "continuous_conjugation_orientation_transport" in cert.dependencies
    assert "closed_world_record_completeness" in cert.dependencies

    mutated = {name: dict(result) for name, result in results.items()}
    mutated["T_held_relative_loop_group"]["passed"] = False
    assert hh.build_certificate(mutated).full_so2_image is False
