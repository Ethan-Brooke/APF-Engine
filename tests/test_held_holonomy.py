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


def test_recombination_forces_nontrivial_effective_loop():
    r = _passed(hh.check_T_held_recombination_nontriviality())
    assert r["artifacts"]["effective_relative_loop"] == 1


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


def test_cli_certificate_marks_physical_premises_uncertified():
    results = hh.run_all()
    cert = hh.build_certificate(results)
    assert all(result["passed"] for result in results.values())
    assert cert.physical_premises_certified is False
    assert cert.dependency_contract_acyclic
