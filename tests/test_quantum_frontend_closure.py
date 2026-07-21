from fractions import Fraction as F

from apf import quantum_frontend_closure as qfc


def _passed(result):
    assert result["passed"], result["fail_reasons"]
    assert result["physical_premises_certified"] is False
    return result


def test_finite_fragments_do_not_imply_uniform_rank():
    r = _passed(qfc.check_T_finite_protocol_fragment_rank())
    assert r["artifacts"]["fragment_rank"] == 3
    assert r["artifacts"]["deficient_control_rank"] == 2
    assert r["artifacts"]["growing_fragment_ranks"] == list(range(1, 8))
    assert r["artifacts"]["uniform_global_rank_derived"] is False


def test_fragment_rank_is_recomputed_not_asserted():
    r = _passed(qfc.check_T_finite_protocol_fragment_rank())
    table = [[F(x) for x in row] for row in r["artifacts"]["score_table"]]
    assert qfc._rank(table) == r["artifacts"]["fragment_rank"] == 3
    control = [[F(x) for x in row] for row in r["artifacts"]["deficient_control_table"]]
    assert qfc._rank(control) == 2


def test_ordered_score_derives_positive_symmetric_ledger():
    r = _passed(qfc.check_T_ordered_score_bilinearization())
    assert r["artifacts"]["symmetric_ledger_form"] == [["1", "0"], ["0", "1"]]
    assert r["artifacts"]["alternating_part"] != [["0", "0"], ["0", "0"]]
    assert r["artifacts"]["parallelogram_derived"]


def test_ordered_score_executes_jordan_von_neumann_leg():
    r = _passed(qfc.check_T_ordered_score_bilinearization())
    a = r["artifacts"]
    assert a["jvn_derived_bilinearity"] is True
    assert a["jvn_polarization_matches_symmetric_part"] is True
    assert a["jvn_cubic_control_fails"] is True
    assert a["jvn_polarization_cases"] > 0 and a["jvn_slot_additivity_cases"] > 0
    # The generating form is genuinely non-symmetric and its symmetric part
    # matches the artifact.
    k = [[F(x) for x in row] for row in a["jvn_generating_form"]]
    assert k != qfc._transpose(k)
    ksym = qfc._scal(F(1, 2), qfc._add(k, qfc._transpose(k)))
    assert qfc._matrix_strings(ksym) == a["jvn_symmetric_part"]
    assert "jordan_von_neumann_completion_beyond_the_finite_grid" in r["premises"]


def test_dual_action_does_not_require_physical_reverse():
    r = _passed(qfc.check_T_dual_action_without_physical_reverse_saturation())
    assert r["artifacts"]["dual_in_physical_upper_triangular_algebra"] is False
    assert r["artifacts"]["span_exclusion_symbolic"] is True
    assert r["artifacts"]["entry_10_identically_zero_on_span"] is True
    assert r["artifacts"]["N_T_entry_10"] == "1"


def test_readout_quotient_has_exact_null_ideal():
    r = _passed(qfc.check_T_canonical_readout_quotient())
    a = r["artifacts"]
    assert a["kernel_basis"] == [["0", "0", "1"]]
    assert a["kernel_derived_from_readout"] is True
    assert a["kernel_is_two_sided_ideal"] is True
    assert a["sample_kernel_size"] == 5


def test_readout_quotient_congruence_and_computed_table():
    r = _passed(qfc.check_T_canonical_readout_quotient())
    a = r["artifacts"]
    assert a["congruence_verified"] is True
    assert a["congruence_cases"] > 0
    assert a["quotient_table_matches_componentwise_R2"] is True
    assert a["quotient_product_table_cases"] > 0
    # Spot-check the computed table artifact.
    assert a["quotient_product_table_sample"]["(-1, 0)*(-1, 0)"] == ["1", "0"]


def test_readout_non_congruence_control_fails():
    r = _passed(qfc.check_T_canonical_readout_quotient())
    a = r["artifacts"]
    assert a["nc_kernel_not_ideal"] is True
    assert a["nc_congruence_fails"] is True
    # The exhibited witness product is nc-nonzero: nc((1,0,0)) = (1,0).
    w = [F(x) for x in a["nc_kernel_not_ideal_witness"]]
    assert (w[0] + w[2], w[1]) != (F(0), F(0))


def test_effect_soundness_is_weaker_than_saturation():
    r = _passed(qfc.check_T_effect_soundness_not_saturation())
    assert r["artifacts"]["sound"] is True
    assert r["artifacts"]["saturated"] is False


def test_density_representation_without_state_completion():
    r = _passed(qfc.check_T_operator_system_state_extension())
    assert r["artifacts"]["extensions_unique"] is False
    assert r["artifacts"]["density_extension_0"] != r["artifacts"]["density_extension_1"]


def test_tensor_faithfulness_is_optional_for_quantum_composite():
    r = _passed(qfc.check_T_composite_tensor_quotient())
    assert r["artifacts"]["tensor_faithful"] is False
    assert r["artifacts"]["quantum_composite_still_valid"] is True


def test_composite_executes_commutation_generation_multiplicativity():
    r = _passed(qfc.check_T_composite_tensor_quotient())
    a = r["artifacts"]
    assert a["commutation_verified"] is True and a["commutation_cases"] > 0
    assert a["unital"] is True and a["injective"] is True
    assert a["generation_rank"] == 4
    assert a["quotient_multiplicative"] is True
    assert a["quotient_multiplicativity_cases"] > 0
    assert a["quotient_surjective"] is True
    assert a["noncommuting_control_fails_commutation"] is True
    assert "orientation_synchronized_embeddings_across_typed_sectors" in r["premises"]


def test_same_type_reference_detects_non_cp_transpose():
    r = _passed(qfc.check_T_same_type_reference_chosen_cp())
    assert r["artifacts"]["negative_quadratic_value"] == "-1"
    assert r["artifacts"]["eigenvalue_minus_half_witnessed"] is True


def test_partial_transpose_is_computed_from_bell():
    r = _passed(qfc.check_T_same_type_reference_chosen_cp())
    a = r["artifacts"]
    assert a["partial_transpose_computed_from_bell"] is True
    bell = [[F(x) for x in row] for row in a["bell_state"]]
    pt = qfc._partial_transpose(bell, 2, 2)
    assert qfc._matrix_strings(pt) == a["partial_transpose"]
    # The Bell density itself comes from the shipped bell vector.
    v = [F(x) for x in a["bell_vector"]]
    assert bell == [[v[i] * v[j] / 2 for j in range(4)] for i in range(4)]


def test_choi_positive_arm_certified():
    r = _passed(qfc.check_T_same_type_reference_chosen_cp())
    a = r["artifacts"]
    assert a["choi_identity_psd"] is True
    assert a["choi_dephasing_psd"] is True
    assert a["choi_transpose_not_psd"] is True
    choi_id = [[F(x) for x in row] for row in a["choi_identity_channel"]]
    assert qfc._psd_by_principal_minors(choi_id)
    choi_t = [[F(x) for x in row] for row in a["choi_transpose_channel"]]
    assert not qfc._psd_by_principal_minors(choi_t)


def test_gap_reclassification_contract():
    r = _passed(qfc.check_T_quantum_gap_reclassification_contract())
    assert r["artifacts"]["canonical_cycle"] is None
    assert r["artifacts"]["ledger_cycle_mutation_detected"]
    assert r["artifacts"]["general_physical_reverse_saturation_load_bearing"] is False
    assert r["artifacts"]["held_consumes_ordered_score_ledger"] is True
    assert r["artifacts"]["ledger_depends_on_held"] is False
    assert r["artifacts"]["held_to_observable_descent_declared"] is True


def test_contract_held_holonomy_granularity_memberships():
    r = _passed(qfc.check_T_quantum_gap_reclassification_contract())
    dc = r["artifacts"]["dependency_contract"]
    assert "REVERSAL_IS_INVERSE" in dc["HELD_NATURAL_COMPLEX_ORIENTATION"]
    assert "Q2_LEDGER_ADJOINT" in dc["HELD_NATURAL_COMPLEX_ORIENTATION"]
    assert "JET_NATURALITY" in dc["HELD_NATURAL_COMPLEX_ORIENTATION"]
    assert "GENERATOR_NATURALITY" not in dc["HELD_NATURAL_COMPLEX_ORIENTATION"]
    assert "GENERATOR_COMPLETENESS" in dc["HELD_TO_OBSERVABLE_DESCENT"]
    assert "FINITE_REAL_CSTAR_CLASSIFICATION" in dc["HELD_TO_OBSERVABLE_DESCENT"]
    assert "ORIENTATION_SYNCHRONIZED_EMBEDDINGS" in dc["COMPOSITE_SOUNDNESS"]
    assert dc["PHYSICAL_REVERSE_SATURATION"] == []
    # Naturality-only names carry no generator completeness.
    assert not qfc._depends_on(qfc.CORE_DEPENDENCIES, "JET_NATURALITY",
                               "GENERATOR_COMPLETENESS")
    assert not qfc._depends_on(qfc.CORE_DEPENDENCIES,
                               "HELD_NATURAL_COMPLEX_ORIENTATION",
                               "GENERATOR_COMPLETENESS")
    # Mislabel fix: the negative-controls string names the actual mutation.
    assert r["negative_controls"] == [
        "ORDERED_SCORE_SELF_DUAL_LEDGER <- HELD_NATURAL_COMPLEX_ORIENTATION cycle mutation"
    ]


def test_contract_premise_reconciliation():
    r = _passed(qfc.check_T_quantum_gap_reclassification_contract())
    recon = r["artifacts"]["premise_reconciliation"]
    assert len(recon) >= 9
    assert recon["FAITHFUL_NONNEGATIVE_DIAGONAL_SCORE"] == "positive_quadratic_ledger_form"
    assert recon["Q2_LEDGER_ADJOINT"] == "Q2_reversal_is_ledger_adjoint"
    assert recon["REVERSAL_IS_INVERSE"] == "reversed_loop_is_inverse"
    assert recon["FAITHFUL_ACTION"] == "faithful_first_order_action"
    assert recon["EFFECTIVE_IMAGE_LIE_SUBGROUP"] == "effective_image_is_a_Lie_subgroup_of_SO2"
    assert recon["GENERATOR_COMPLETENESS"] == "generator_completeness"
    assert recon["FINITE_REAL_CSTAR_CLASSIFICATION"] == "finite_real_Cstar_completion"
    assert recon["ORIENTATION_SYNCHRONIZED_EMBEDDINGS"] == \
        "orientation_synchronization_across_typed_sectors"
    assert recon["JET_NATURALITY"] == "jet_functoriality"


def test_descent_premises_align_with_contract_vocabulary():
    r = _passed(qfc.check_T_held_to_observable_descent_criterion())
    prem = r["premises"]
    assert "faithful_action_of_the_Q2_observable_envelope_on_the_Held_carrier" in prem
    assert "generator_completeness_of_the_represented_observable_envelope" in prem
    assert "finite_real_Cstar_classification_of_the_descended_algebra" in prem


def test_aggregate_certificate():
    rs = qfc.run_all()
    assert all(r["passed"] for r in rs.values())
    cert = qfc.build_certificate(rs)
    assert cert.physical_premises_certified is False
    assert cert.dependency_contract_acyclic
    assert "all_density_operators_preparable" in cert.optional_saturation_claims
    assert len(cert.remaining_physical_kernel) == 6
    assert any("Held_to_observable" in item for item in cert.remaining_physical_kernel)


def test_held_to_observable_descent_requires_module_closure():
    r = _passed(qfc.check_T_held_to_observable_descent_criterion())
    assert r["artifacts"]["module_closed"] is True
    assert r["artifacts"]["commutation_only_contains_J"] is False
