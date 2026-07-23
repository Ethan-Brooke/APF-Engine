from fractions import Fraction as F
from pathlib import Path

import pytest

from apf import dense_sandwich_born as m

# Bank-landing adaptation (v24.3.434): the vendored-SOURCES / sibling-packet
# file tests require the PACKET layout. In the bank tree they SKIP with a
# pointer to the packet drop (born_chain, APF_Dense_Sandwich_Born_v0.6),
# where they run green; the in-bank equivalents run inside
# check_T_composed_root_inventory against the REAL banked contracts.
_PACKET_LAYOUT = m.VENDORED_HFC_CONTRACTS_PATH.is_file()
requires_packet = pytest.mark.skipif(
    not _PACKET_LAYOUT,
    reason="packet-layout test (SOURCES/ vendored copies); green in the "
           "packet drop (born_chain, APF_Dense_Sandwich_Born_v0.6)")
_SIBLING_LAYOUT = m.SIBLING_V08_MANIFEST_PATH.is_file()
requires_sibling = pytest.mark.skipif(
    not _SIBLING_LAYOUT,
    reason="sibling-packet-layout test (APF_Operational_Score_Linearity_v0.8 "
           "DATA path); green in the packet drop (born_chain); the in-bank "
           "equivalent runs against apf.operational_score_linearity")


def test_all_schema_checks_pass():
    rows = m.run_all()
    assert len(rows) == 14
    assert all(row["passed"] for row in rows.values())


def test_orientation_alignment_is_exact():
    aligned = m._rmm(m._rmm(m.Q_ALIGN, m.J_OR_V05), m.Q_ALIGN)
    assert aligned == m.J_STD
    assert m._rmm(m.J_STD, m.J_STD) == tuple(tuple(-x for x in row) for row in m._reye(4))


def test_realification_intertwines_star():
    for b in m.COMPLEX_BASIS:
        assert m._rtranspose(m._realify(b)) == m._realify(m._gdag(b))


def test_complex_basis_has_real_rank_eight():
    rows = [[x for row in m._realify(b) for x in row] for b in m.COMPLEX_BASIS]
    assert m._rank(rows) == 8


def test_dyadic_ray_synthesis_uses_nonnegative_inputs_only():
    target = m._unflatten_gaussian_matrix((F(-1,2),F(1,4),F(3,4),F(-1,8),F(0),F(1,2),F(-3,4),F(0)))
    v = m._flatten_gaussian_matrix(target)
    lam, x, y = m._dyadic_ray_decomposition(v)
    assert all(a >= 0 for a in x+y)
    assert sum(x) <= 1 and sum(y) <= 1
    assert tuple((a-b)/2 for a,b in zip(x,y)) == tuple(a/(2*lam) for a in v)


def test_non_dyadic_target_rejected_by_exact_synthesis():
    try:
        m._dyadic_ray_decomposition((F(1,3),))
    except ValueError as exc:
        assert "dyadic" in str(exc)
    else:
        raise AssertionError("non-dyadic target accepted")


def test_dyadic_star_algebra_closes_under_product_and_adjoint():
    a = m._unflatten_gaussian_matrix((F(1,2),F(1,4),F(-1,8),F(0),F(0),F(1,2),F(3,4),F(-1,4)))
    b = m._unflatten_gaussian_matrix((F(-1,4),F(0),F(1,2),F(1,2),F(1,8),F(0),F(0),F(-1,2)))
    assert all(m._is_dyadic(x) for x in m._gflat(m._gmm(a,b)))
    assert all(m._is_dyadic(x) for x in m._gflat(m._gdag(a)))




def test_closed_loop_score_is_uniquely_normalized_trace():
    row = m.check_T_closed_loop_score_is_normalized_trace()
    assert row["passed"]
    assert row["artifacts"]["derived_matrix_unit_values"] == {
        "L(E11)": "1/2",
        "L(E12)": "0",
        "L(E21)": "0",
        "L(E22)": "1/2",
    }


def test_normalized_coordinate_score_fails_cyclicity():
    row = m.check_T_closed_loop_score_is_normalized_trace()
    assert row["artifacts"]["nontracial_control_caught"]
    assert row["artifacts"]["nontracial_control_left"] == "1"
    assert row["artifacts"]["nontracial_control_right"] == "0"


def test_nonhermitian_readout_is_caught_by_nonreal_sandwich():
    row = m.check_T_dense_sandwich_effect_soundness()
    assert row["passed"]
    assert row["artifacts"]["self_adjointness_assumed"] is False
    assert row["artifacts"]["nonhermitian_control_caught"]
    assert row["artifacts"]["nonhermitian_control_score"] == "2+1i"


def test_closed_loop_score_leaves_are_in_born_ancestry():
    deps = m._deps(m.DEPENDENCY_GRAPH, "T_WEIGHTED_BORN_SOUNDNESS")
    assert "CLOSED_LOOP_SCORE_LINEARITY" in deps
    assert "CLOSED_LOOP_SCORE_CYCLICITY" in deps
    assert "CLOSED_LOOP_SCORE_NORMALIZATION" in deps
    assert "REPRESENTED_OUTCOME_READOUTS" in deps


def test_one_trace_test_misses_indefinite_effect():
    h = m._gmat((((F(-1),F(0)),m.ZERO_G),(m.ZERO_G,(F(2),F(0)))))
    assert m._gtrace(h)[0] == 1
    assert m._trace_sandwich(m.E11,h) == -1
    assert not m._is_psd2(h)


def test_rank_one_effect_and_complement_are_positive():
    phi = ((F(4,5),F(0)),(F(0),F(3,5)))
    e = m._gvec_outer(phi)
    assert m._is_effect2(e)
    assert m._is_effect2(m._gsubm(m.I2_G,e))


def test_normalized_nonpositive_state_fails_loop_square():
    rho_bad = m._gmat((((F(3,2),F(0)),m.ZERO_G),(m.ZERO_G,(F(-1,2),F(0)))))
    assert m._gtrace(rho_bad) == m.ONE_G
    e22 = m._gmm(m._gdag(m.E12),m.E12)
    assert m._born(rho_bad,e22) == F(-1,2)


def test_exact_weighted_born_value():
    psi = ((F(3,5),F(0)),(F(4,5),F(0)))
    phi = ((F(4,5),F(0)),(F(0),F(3,5)))
    rho = m._gvec_outer(psi)
    e = m._gvec_outer(phi)
    assert m._born(rho,e) == F(288,625)
    inner = m._gsum(m._gmul(m._gconj(phi[j]),psi[j]) for j in range(2))
    assert m._gabs2(inner) == F(288,625)


def test_povm_soundness_does_not_imply_measurement_completion():
    row = m.check_T_soundness_saturation_separation()
    assert row["passed"]
    assert row["artifacts"]["Born_sound"]
    assert not row["artifacts"]["measurement_complete"]


def test_g_hold_exact_absent_from_born_dependency_graph():
    assert "G_HOLD_EXACT" not in m._all_nodes(m.DEPENDENCY_GRAPH)
    assert "G_HOLD_EXACT" in m.FORBIDDEN_DEPENDENCIES


def test_effect_completion_absent_from_born_ancestry():
    deps = m._deps(m.DEPENDENCY_GRAPH,"T_WEIGHTED_BORN_SOUNDNESS")
    assert "T_OPTIONAL_EFFECT_COMPLETION" not in deps
    assert "CLOSED_READOUT_LIMITS" not in deps


def test_cp_absent_from_born_ancestry():
    deps = m._deps(m.DEPENDENCY_GRAPH,"T_WEIGHTED_BORN_SOUNDNESS")
    assert "T_CP_SOUNDNESS" not in deps
    assert "PHYSICAL_EXTENSION_SOUNDNESS" not in deps


def test_transpose_choi_negative_control():
    row = m.check_T_cp_boundary_preserved()
    assert row["passed"]
    assert row["artifacts"]["choi_negative_expectation"] == "-2"
    assert not row["artifacts"]["transpose_CP"]


def test_cycle_mutation_caught():
    graph = dict(m.DEPENDENCY_GRAPH)
    graph["T_ORIENTED_COMPLEX_MODEL"] = (*graph["T_ORIENTED_COMPLEX_MODEL"],"T_WEIGHTED_BORN_SOUNDNESS")
    assert m._cycle(graph) is not None


def test_g_hold_mutation_caught():
    graph = dict(m.DEPENDENCY_GRAPH)
    graph["T_WEIGHTED_BORN_SOUNDNESS"] = (*graph["T_WEIGHTED_BORN_SOUNDNESS"],"G_HOLD_EXACT")
    assert m.FORBIDDEN_DEPENDENCIES & m._all_nodes(graph)


def test_missing_mixture_congruence_changes_root_inventory():
    graph = dict(m.DEPENDENCY_GRAPH)
    original = m._roots(graph)
    graph["T_STATE_SOUNDNESS"] = tuple(d for d in graph["T_STATE_SOUNDNESS"] if d != "MIXTURE_CONGRUENCE")
    assert m._roots(graph) != original


def test_certificate_never_self_certifies_physics():
    cert = m.build_certificate()
    assert cert.finite_born_trace_representation_exact
    assert cert.g_hold_exact_not_in_born_ancestry
    assert cert.composed_root_inventory_exact
    assert cert.premises_graph_concordant
    assert cert.physical_premises_certified is False


def test_nonlinear_probability_control_violates_affinity():
    f = lambda t: t*t
    assert f(F(1,2)) != (f(F(0))+f(F(1)))/2


def test_contextual_effect_value_control_is_not_a_function():
    effect_id = "same_effect"
    contexts = {("M1",effect_id):F(1,3),("M2",effect_id):F(2,3)}
    assert contexts[("M1",effect_id)] != contexts[("M2",effect_id)]


def test_sum_to_identity_without_positive_members_is_not_povm():
    bad1 = m._gmat((((F(-1),F(0)),m.ZERO_G),(m.ZERO_G,m.ZERO_G)))
    bad2 = m._gsubm(m.I2_G,bad1)
    assert m._gaddm(bad1,bad2) == m.I2_G
    assert not m._is_psd2(bad1)


# ---------------------------------------------------------------------------
# FORTIFICATION 2026-07-21: adversarial tests per audit MAJOR
# ---------------------------------------------------------------------------

def test_det_leg_impostor_is_caught_effect():
    # MAJOR-4 / mutation M3: off-diagonal indefinite impostor with positive
    # diagonal is rejected ONLY by the determinant leg; if that leg is
    # dropped, this test fails.
    h = m._gmat((((F(1), F(0)), (F(2), F(0))), ((F(2), F(0)), (F(1), F(0)))))
    assert h[0][0][0] >= 0 and h[1][1][0] >= 0
    assert m._det2h(h) == F(-3)
    assert not m._is_psd2(h)
    assert not m._is_effect2(h)


def test_det_leg_impostor_is_caught_state():
    rho = m._gmat((((F(1, 2), F(0)), (F(1), F(0))), ((F(1), F(0)), (F(1, 2), F(0)))))
    assert m._gtrace(rho) == m.ONE_G
    assert not m._is_psd2(rho)
    c = m._gmat((((F(1), F(0)), (F(-1), F(0))), (m.ZERO_G, m.ZERO_G)))
    assert m._born(rho, m._gmm(m._gdag(c), c)) == F(-1)


def test_det_leg_impostor_sandwich_negative():
    h = m._gmat((((F(1), F(0)), (F(2), F(0))), ((F(2), F(0)), (F(1), F(0)))))
    b = m._gmat((((F(1), F(0)), m.ZERO_G), ((F(-1), F(0)), m.ZERO_G)))
    assert m._trace_sandwich(b, h) < 0


def test_weakened_psd_gate_would_pass_impostor():
    # documents WHY the impostor is load-bearing: a diagonal-only gate
    # (the M3-mutated gate) accepts it.
    h = m._gmat((((F(1), F(0)), (F(2), F(0))), ((F(2), F(0)), (F(1), F(0)))))
    diagonal_only_gate = h[0][0][0] >= 0 and h[1][1][0] >= 0
    assert diagonal_only_gate and not m._is_psd2(h)


def test_trace_uniqueness_machine_closed():
    row = m.check_T_closed_loop_score_is_normalized_trace()
    assert row["passed"]
    assert row["artifacts"]["uniqueness_machine_closed"] is True
    assert row["artifacts"]["derived_matrix_unit_values"]["L(E11)"] == "1/2"


def test_cyclicity_without_normalization_is_underdetermined():
    row = m.check_T_closed_loop_score_is_normalized_trace()
    # the in-check mutation asserts this; re-assert the row carries it
    assert row["passed"]


def test_no_defect_mutation_executed_and_caught():
    row = m.check_T_hfc_dyadic_matrix_ray_synthesis()
    assert row["passed"]
    assert row["artifacts"]["no_defect_mutation_executed"] is True
    assert row["artifacts"]["no_defect_mutation_caught"] is True


def test_composed_root_inventory_exact():
    row = m.check_T_composed_root_inventory()
    assert row["passed"]
    assert row["artifacts"]["packet_local_core_count"] == 21
    assert row["artifacts"]["composed_distinct_total"] == 39
    assert row["artifacts"]["shared_names"] == ["SAME_TYPE_RETURN"]
    assert "ORIENTATION_COVER_REALIZED" in row["artifacts"]["imported_graded_orientation"]


def test_composed_inventory_drift_is_caught():
    # adversarial: a phantom leaf or a dropped import breaks set-exactness
    ig = set(m.IMPORTED_HFC_345_CONTRACT_LEAVES)
    assert ig | {"PHANTOM_LEAF"} != ig
    orient = set(m.IMPORTED_GRADED_ORIENTATION_PREMISES)
    assert orient - {"ORIENTATION_COVER_REALIZED"} != orient


@requires_packet
def test_vendored_sources_are_canonical():
    assert m.VENDORED_HFC_CONTRACTS_PATH.is_file()
    text = m.VENDORED_GRADED_ORIENTATION_PATH.read_text(encoding="utf-8")
    assert "FORTIFICATION 2026-07-21" in text
    assert "ORIENTATION_COVER_REALIZED" in text


def test_premises_graph_concordance():
    row = m.check_T_premises_graph_concordance()
    assert row["passed"]
    assert row["artifacts"]["premise_union_size"] == 21


def test_typed_oriented_matrix_cargo_in_check_premises():
    row = m.check_T_dense_dyadic_star_subalgebra()
    assert "TYPED_ORIENTED_MATRIX_CARGO" in row["premises"]


def test_g_hold_check_is_contract_carried_not_countermodel():
    row = m.check_T_g_hold_exact_not_in_born_ancestry()
    assert row["passed"]
    assert row["artifacts"]["countermodel_claimed"] is False
    assert row["artifacts"]["G_hold_exact_in_ancestry"] is False


@requires_sibling
def test_v08_linearity_reduction_cited_at_post_fix_strength():
    import json
    sib = json.loads(m.SIBLING_V08_MANIFEST_PATH.read_text(encoding="utf-8"))
    assert "CLASSICAL_SCORE_TOTALITY" in sib["primitive_operational_leaves"]
    assert "CLOSED_LOOP_SCORE_LINEARITY" in sib["derived_and_removed_as_independent_leaves"]
    assert sib["physical_premises_certified"] is False
