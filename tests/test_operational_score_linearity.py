from fractions import Fraction as F
from apf.operational_score_linearity import *  # noqa: F401,F403
from apf import operational_score_linearity as m


def test_all_checks_pass():
    out = m.run_all()
    assert out["status"] == "PASS"
    assert len(out["checks"]) == 10
    assert out["physical_premises_certified"] is False


def test_classical_score_totality_is_a_named_leaf():
    out = m.run_all()
    assert "CLASSICAL_SCORE_TOTALITY" in out["remaining_physical_leaves"]
    assert "CLASSICAL_SCORE_TOTALITY" in m.DEPENDENCY_GRAPH["REAL_AFFINITY"]


# --- executed-derivation legs fail under axiom mutations (gate) ---

def test_affinity_derivation_fails_without_totality():
    lam = F(3, 8)
    congruence = [F(1), F(0), F(0), F(-1)]
    goal = [F(0), -lam, -(1 - lam), F(1)]
    assert not m._entailed([congruence], goal)


def test_affinity_derivation_fails_without_congruence():
    lam = F(3, 8)
    totality = [F(1), -lam, -(1 - lam), F(0)]
    goal = [F(0), -lam, -(1 - lam), F(1)]
    assert not m._entailed([totality], goal)


def test_affinity_derivation_succeeds_with_both():
    lam = F(3, 8)
    totality = [F(1), -lam, -(1 - lam), F(0)]
    congruence = [F(1), F(0), F(0), F(-1)]
    goal = [F(0), -lam, -(1 - lam), F(1)]
    assert m._entailed([totality, congruence], goal)


def test_additivity_derivation_fails_without_zero_axiom():
    tot1 = [F(1), F(0), F(0), F(-1, 2), F(-1, 2), F(0), F(0)]
    tot2 = [F(0), F(1), F(0), F(0), F(0), F(-1, 2), F(-1, 2)]
    cong1 = [F(1), F(0), F(-1), F(0), F(0), F(0), F(0)]
    cong2 = [F(0), F(1), F(-1), F(0), F(0), F(0), F(0)]
    goal = [F(0), F(0), F(0), F(-1), F(-1), F(1), F(0)]
    assert not m._entailed([tot1, tot2, cong1, cong2], goal)
    zero = [F(0), F(0), F(0), F(0), F(0), F(0), F(1)]
    assert m._entailed([tot1, tot2, cong1, cong2, zero], goal)


# --- the nonlinear impostor is rejected (gate) ---

def test_nonlinear_impostor_rejected_by_affinity():
    g = m.score_nonlinear_impostor
    lam = F(1, 2)
    mix = m._madd(m._mscale(lam, m.E11), m._mscale(1 - lam, m.I2))
    assert g(mix) != lam * g(m.E11) + (1 - lam) * g(m.I2)


def test_nonlinear_impostor_rejected_by_additivity():
    g = m.score_nonlinear_impostor
    assert g(m._madd(m.E11, m.E22)) != g(m.E11) + g(m.E22)


def test_old_equal_score_witness_was_degenerate_for_impostor():
    # documents audit finding N1: any function of the trace passes E11-vs-E22
    g = m.score_nonlinear_impostor
    lam = F(3, 8)
    mix = m._madd(m._mscale(lam, m.E11), m._mscale(1 - lam, m.E22))
    assert g(mix) == lam * g(m.E11) + (1 - lam) * g(m.E22)


def test_impostor_passes_bare_normalization():
    g = m.score_nonlinear_impostor
    assert g(m.I2) == 1 and g(m.ZERO2) == 0


# --- the trace is not forced by v0.8 leaves ---

def test_coordinate_score_is_a_model_of_all_leaves_but_not_the_trace():
    row = m.check_T_linear_noncyclic_model_within_leaves()
    assert row.passed
    s = m.score_coordinate_11
    assert s(m._mmul(m.E12, m.E21)) != s(m._mmul(m.E21, m.E12))


# --- extension determination (successor of the mislabeled check) ---

def test_spanning_effects_have_rank_four():
    span = [list(m._sa_coords(e)) for e in m.SPANNING_EFFECTS]
    assert m._rank(span) == 4


def test_generic_functional_reconstruction_roundtrip():
    span = [list(m._sa_coords(e)) for e in m.SPANNING_EFFECTS]
    u = (F(2, 7), F(3, 5), F(-1, 3), F(5, 11))
    svals = [sum(c * ui for c, ui in zip(m._sa_coords(e), u)) for e in m.SPANNING_EFFECTS]
    rec = m._solve(span, svals)
    assert tuple(rec) == u


def test_reconstruction_is_not_trace_theater():
    # the generic functional used is not the normalized trace
    u = (F(2, 7), F(3, 5), F(-1, 3), F(5, 11))
    assert u != (F(1, 2), F(1, 2), F(0), F(0))


# --- contextual and complexification controls ---

def test_contextual_score_control_is_computed_not_constants():
    row = m.check_T_contextual_score_violates_congruence()
    assert row.passed


def test_real_not_complex_control():
    assert m.check_T_real_not_complex_linear_control().passed


def test_complexification_generic_functional():
    assert m.check_T_J_complexification_unique_executed().passed


# --- dependency contract mutations (computed graph) ---

def test_g_hold_insertion_caught():
    g = dict(m.DEPENDENCY_GRAPH)
    g["TRACE_BORN"] = (*g["TRACE_BORN"], "G_HOLD_EXACT")
    assert m.FORBIDDEN_DEPENDENCIES & m._all_nodes(g)


def test_born_to_affinity_cycle_caught():
    g = dict(m.DEPENDENCY_GRAPH)
    g["REAL_AFFINITY"] = (*g["REAL_AFFINITY"], "TRACE_BORN")
    assert m._cycle(g) is not None


def test_trace_born_not_upstream_of_mixing():
    assert "TRACE_BORN" not in m._deps(m.DEPENDENCY_GRAPH, "REAL_AFFINITY")


def test_manifest_module_concordance():
    # Bank-landing adaptation (v24.3.434): the loader serves the packet DATA
    # copy when present, the embedded REDUCED_LEAF_MANIFEST constant in the
    # bank tree, so the concordance tripwire stays live in both layouts.
    d = m._load_reduced_leaf_manifest()
    assert set(d["primitive_operational_leaves"]) == set(m.REMAINING_PHYSICAL_LEAVES)
    assert set(d["convenience_axioms"]) == set(m.CONVENIENCE_AXIOMS)
    assert d["physical_premises_certified"] is False
