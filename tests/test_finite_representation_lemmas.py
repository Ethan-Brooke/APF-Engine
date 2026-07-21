"""Pytest suite for finite_representation_lemmas, including the mandatory
ten-mutation kill battery from RULINGS_OF_RECORD_2026-07-20.

Every mutation is applied by parameterization (never by editing source), and
every test asserts the mutation is CAUGHT: the mutated check fails, or the
reconciliation instrument fails, exactly as the rulings require.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import apf.finite_representation_lemmas as frl
from fractions import Fraction as F


def _fresh_results():
    return {name: fn() for name, fn in frl._CHECKS.items()}


# ---------------------------------------------------------------------------
# Green path
# ---------------------------------------------------------------------------


def test_all_checks_pass():
    results = frl.run_all()
    assert len(results) == 11
    for name, r in results.items():
        assert r["passed"], (name, r["fail_reasons"])
        assert r["status"] == "PASS"


def test_every_result_is_honestly_billed():
    for name, r in frl.run_all().items():
        assert r["physical_premises_certified"] is False, name
        assert set(r["premises"]) <= set(frl.PHYSICAL_PREMISES), name
        assert r["epistemic"] in ("P_math", "P_structural_instrument"), name


def test_reconciliation_green():
    r = frl.check_L_physical_premise_reconciliation()
    assert r["passed"], r["fail_reasons"]
    assert set(r["artifacts"]["consumed_premise_union"]) == set(
        frl.PHYSICAL_PREMISES)


def test_physical_premise_manifest_is_complete_and_typed():
    assert len(frl.PHYSICAL_PREMISES) == 11
    for p in frl.PHYSICAL_PREMISES:
        assert frl.PREMISE_TYPING[p]["type"] == "physical"


def test_licensed_claim_and_may_not_cite():
    assert frl.LICENSED_CLAIM.startswith("Given a separately supplied")
    assert "recover the standard finite-dimensional quantum formalism" in \
        frl.LICENSED_CLAIM
    assert "all finite quantum seams are closed" in frl.MAY_NOT_CITE
    assert "G-hold-exact is discharged" in frl.MAY_NOT_CITE
    assert len(frl.MAY_NOT_CITE) == 10


def test_determinism():
    a = json.dumps(frl.run_all(), sort_keys=True, default=str)
    b = json.dumps(frl.run_all(), sort_keys=True, default=str)
    assert a == b


def test_module_executes_as_script():
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env = dict(os.environ, PYTHONPATH=repo)
    proc = subprocess.run([sys.executable, "-m",
                           "apf.finite_representation_lemmas"],
                          capture_output=True, text=True, timeout=300,
                          cwd=repo, env=env)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "pass: 11" in proc.stdout


def test_boost_orbit_strictly_grows():
    r = frl.check_L_nonexpansion_pair_forces_isometry()
    norms = [F(x) for x in r["artifacts"]["boost_orbit_norms"]]
    assert all(norms[i] < norms[i + 1] for i in range(len(norms) - 1))


def test_haar_invariant_form_is_nontrivial():
    r = frl.check_L_conjugated_finite_haar_invariant_form()
    form = r["artifacts"]["invariant_form"]
    assert F(form[0][1]) != 0  # non-diagonal: conjugation made it non-trivial


def test_flipped_j_adversary_detected_by_default():
    r = frl.check_L_composite_orientation_synchronization()
    assert r["artifacts"]["flipped_adversary_is_homomorphism"] is True
    assert r["artifacts"]["flipped_adversary_detected"] is True


def test_transpose_choi_negative_witness_is_computed():
    r = frl.check_L_kraus_choi_complete_positivity()
    assert F(r["artifacts"]["transpose_min_value"]) < 0
    assert r["artifacts"]["transpose_min_witness"] is not None


def test_kernel_death_reported_killed_by_default():
    r = frl.check_L_kernel_death_holonomy_control()
    assert r["passed"]
    assert r["artifacts"]["dead_holonomy_status"] == "KILLED"
    assert r["artifacts"]["dead_loop_billed_live"] is False


def test_g_hold_exact_reported_open():
    r = frl.check_L_operational_quotient_conservativity()
    assert "OPEN_NAMED_GRANT" in r["artifacts"]["g_hold_exact_status"]


# ---------------------------------------------------------------------------
# Mandatory mutation battery (RULINGS_OF_RECORD, salvage instrument standard)
# ---------------------------------------------------------------------------


def test_mutation_01_second_empirical_root_caught():
    """Adding a second empirical root to the premise graph must fail
    reconciliation (stage-2 MAJOR-1)."""
    results = _fresh_results()
    tampered = frl.check_L_effects_povm_density_born(
        premises_override=("POSITIVE_STATE_STRUCTURE",
                           "INSTRUMENT_FAMILY_EXHAUSTIVENESS",
                           "QAC_Held_complete_empirical_certificate"))
    assert tampered["passed"]  # the math legs still pass...
    results["check_L_effects_povm_density_born"] = tampered
    rec = frl.check_L_physical_premise_reconciliation(results=results)
    assert not rec["passed"]  # ...but the bookkeeping instrument catches it
    assert any("second-empirical-root" in f or "undeclared" in f
               for f in rec["fail_reasons"])


def test_mutation_02_generator_completeness_removal_caught():
    """Removing GENERATOR_COMPLETENESS from a consumer must fail
    reconciliation (Ruling 3)."""
    results = _fresh_results()
    tampered = frl.check_L_composite_orientation_synchronization(
        premises_override=("ORIENTATION_SYNCHRONIZED_EMBEDDINGS",
                           "COMPOSITE_REALIZATION"))
    results["check_L_composite_orientation_synchronization"] = tampered
    rec = frl.check_L_physical_premise_reconciliation(results=results)
    assert not rec["passed"]
    assert any("premise-manifest mismatch" in f for f in rec["fail_reasons"])


def test_mutation_03_orientation_sync_removal_caught():
    """With orientation synchronization removed, the flipped-J (conjugate)
    embedding becomes the embedding of record and MUST be detected as a
    failure (stage-1 M9, stage-2 MAJOR-3)."""
    r = frl.check_L_composite_orientation_synchronization(
        orientation_synchronized=False)
    assert not r["passed"]
    assert any("ORIENTATION_SYNCHRONIZED_EMBEDDINGS" in f
               for f in r["fail_reasons"])


def test_mutation_04_positive_state_premise_removal_caught():
    """Removing the positive-state premise name must fail the reconciliation
    certificate (stage-1 M8)."""
    results = _fresh_results()
    tampered = frl.check_L_effects_povm_density_born(
        premises_override=("INSTRUMENT_FAMILY_EXHAUSTIVENESS",))
    results["check_L_effects_povm_density_born"] = tampered
    rec = frl.check_L_physical_premise_reconciliation(results=results)
    assert not rec["passed"]
    assert any("premise-manifest mismatch" in f for f in rec["fail_reasons"])
    # And if BOTH consumers drop it, the union itself becomes deficient.
    results["check_L_kraus_choi_complete_positivity"] = (
        frl.check_L_kraus_choi_complete_positivity(
            premises_override=("FINITE_RESOLVED_EVENT_BRANCHES",)))
    rec2 = frl.check_L_physical_premise_reconciliation(results=results)
    assert not rec2["passed"]
    assert any("set-exactly" in f for f in rec2["fail_reasons"])


def test_mutation_05_boost_family_fails_averaging_leg():
    """Replacing the compact (finite, closed) group with the SO(1,1) boost
    family must fail the Haar averaging check (stage-1 M1/M2)."""
    powers = []
    p = [[F(1), F(0)], [F(0), F(1)]]
    for _ in range(8):
        powers.append([row[:] for row in p])
        p = frl._mm(p, frl.BOOST)
    r = frl.check_L_conjugated_finite_haar_invariant_form(
        group_override=powers)
    assert not r["passed"]
    assert any("closed" in f or "inversion" in f for f in r["fail_reasons"])


def test_mutation_06_kernel_death_billing_live_caught():
    """A nontrivial abstract quotient with a dead represented action must be
    flagged killed; billing it live must fail (H2 kernel-death control)."""
    r = frl.check_L_kernel_death_holonomy_control(claim_live_when_dead=True)
    assert not r["passed"]
    assert any("kernel-death" in f for f in r["fail_reasons"])


def test_mutation_07_cost_distinct_identification_caught():
    """Two mechanisms with identical readouts but different cost rows must
    NOT be identified; the attempt must fire
    NONCONSERVATIVE_OPERATIONAL_QUOTIENT (Ruling 5)."""
    r = frl.check_L_operational_quotient_conservativity(
        attempt_identification_of_cost_distinct=True)
    assert not r["passed"]
    assert any(frl.NONCONSERVATIVE_OPERATIONAL_QUOTIENT in f
               for f in r["fail_reasons"])


def test_mutation_08_missing_instrument_relation_caught():
    """Removing one declared instrument relation must fail the completeness
    leg (split clause: algebraic half executed, exhaustiveness physical)."""
    declared = tuple(x for x in frl.REQUIRED_INSTRUMENT_RELATIONS
                     if x != "effects_sum_to_identity")
    r = frl.check_L_effects_povm_density_born(declared_relations=declared)
    assert not r["passed"]
    assert any("match the required set exactly" in f
               for f in r["fail_reasons"])


def test_mutation_09_broken_fragment_composition_caught():
    """Breaking one fragment-restriction composition law must fail the
    functoriality check (stage-2 fold-in item 5)."""
    r = frl.check_L_pro_cstar_fragment_functoriality(break_composition=True)
    assert not r["passed"]
    assert any("functorial coherence" in f or "direct restriction" in f
               for f in r["fail_reasons"])


def test_mutation_10_phantom_coderef_caught():
    """Inserting a nonexistent coderef into the provenance table must fail
    the coderef-existence leg (stage-1 M7)."""
    phantom = {
        "leg": "phantom leg",
        "coderef": "check_T_quantum_gap_closure_phantom",
        "packet_source": "RULINGS_OF_RECORD_2026-07-20",
        "audit_findings": ("Ruling-2",),
    }
    r = frl.check_L_provenance_coderef_existence(extra_rows=(phantom,))
    assert not r["passed"]
    assert any("phantom" in f or "not in the allowlist" in f
               for f in r["fail_reasons"])
