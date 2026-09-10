"""Adversarial tests for :mod:`apf.zipper_reduction_frontier`."""

from apf import zipper_reduction_frontier as zf


def _passed(row):
    assert row["passed"], row["fail_reasons"]
    assert row["physical_premises_certified"] is False
    return row


def test_orientation_sync_and_double_cover_controls():
    r = _passed(zf.check_T_frontier_orientation_synchronization())
    assert r["artifacts"]["trivial_cocycle_assignment"] is not None
    assert r["artifacts"]["obstructed_one_sheet_assignment"] is None
    assert r["artifacts"]["double_cover_sheet_transport_exact"] is True


def test_arbitrary_finite_tensor_schema_and_orientation_control():
    r = _passed(zf.check_T_frontier_finite_tensor_composition())
    for rec in r["artifacts"]["dimension_records"]:
        assert rec["generated_matrix_algebra_rank"] == rec["expected_matrix_algebra_rank"]
        assert rec["complex_tensor_real_dim"] == rec["expected_complex_tensor_real_dim"]
        assert rec["same_i_descends_with_opposite_orientation"] is False


def test_reduced_event_cp_dilation_and_transpose_control():
    r = _passed(zf.check_T_frontier_reduced_event_complete_positivity())
    for rec in r["artifacts"]["dimension_records"]:
        assert rec["trace_preserving_exact"]
        assert rec["isometry_exact"]
        assert rec["choi_is_explicit_gram_sum"]
        assert rec["transpose_choi_antisymmetric_quadratic_value"] == "-2"


def test_finite_dimensional_trace_uniqueness_and_born_normalization():
    r = _passed(zf.check_T_frontier_finite_dimensional_born_weighting())
    for rec in r["artifacts"]["dimension_records"]:
        assert rec["offdiagonal_score_zero"]
        assert rec["coordinate_score_normalized_but_not_cyclic"]
        assert rec["sample_probabilities_sum"] == "1"


def test_action_scale_residue_is_one_dimensional():
    r = _passed(zf.check_T_frontier_action_scale_residue())
    assert r["artifacts"]["free_scale_dimension"] == 1
    assert r["artifacts"]["sample_inferred_action_scale"] == "3/2"
    for rec in r["artifacts"]["scale_gauge_records"]:
        assert rec["phase"] == rec["scaled_phase"]


def test_universal_moving_frame_claim_is_reduced():
    r = _passed(zf.check_T_frontier_moving_frame_empirical_scope())
    c = r["artifacts"]["classifications"]
    assert c["coherent_moving"] == "MOVING_FRAME_COHERENT_BRANCH"
    assert c["valid_static"] == "STATIC_FRAME"
    assert c["discrete_C2"] == "DISCRETE_FRAME_JUMP"
    assert c["recording_boundary"] == "EVENT_BOUNDARY_OR_OPEN_SYSTEM"
    assert r["artifacts"]["universal_every_interface_claim"] is False


def test_frontier_dependency_contract_and_cycle_mutation():
    r = _passed(zf.check_T_frontier_dependency_contract())
    assert r["artifacts"]["cycle"] is None
    assert r["artifacts"]["empirical_cycle_mutation_caught"]
    statuses = r["artifacts"]["progress_statuses"]
    assert "OPEN" in statuses["hbar_action_scale"]
    assert "REDUCED" in statuses["moving_frame_every_interface"]


def test_certificate_is_unbanked_and_physical_gates_uncertified():
    rows = zf.run_all()
    cert = zf.build_certificate(rows)
    assert all(row["passed"] for row in rows.values())
    assert cert.physical_premises_certified is False
    assert cert.orientation_sync_math_exact
    assert cert.finite_tensor_schema_exact
    assert cert.reduced_event_cp_schema_exact
    assert cert.finite_dimensional_born_form_exact
    assert cert.action_scale_residue_exact
    assert cert.moving_frame_scope_reduced
