"""Adversarial tests for :mod:`apf.two_exchange_holonomy`."""
from fractions import Fraction as F
from apf import two_exchange_holonomy as th


def _pass(name):
    r = th.CHECKS[name]()
    assert r["passed"], r["fail_reasons"]
    assert r["physical_premises_certified"] is False
    return r


def test_binary_exchange_decodes_to_reflection():
    r = _pass("T_binary_exchange_is_character_reflection")
    assert r["artifacts"]["decoded_exchange"] == [["1", "0"], ["0", "-1"]]
    assert r["artifacts"]["physical_idempotent_required"] is False


def test_rotated_exchange_is_exact_conjugated_swap():
    r = _pass("T_rotated_exchange_is_conjugated_swap")
    assert r["artifacts"]["transported_exchange"] == [["-7/25", "24/25"], ["24/25", "7/25"]]


def test_codespace_restricts_to_345_fixed_line():
    r = _pass("T_345_codespace_fixed_line_candidate")
    assert r["artifacts"]["fixed_line_u"] == ["3/5", "4/5"]
    assert r["artifacts"]["codespace_to_Held_identification_certified"] is False


def test_two_exchanges_generate_exact_candidate_gate():
    r = _pass("T_two_exchanges_generate_irrational_gate")
    assert r["artifacts"]["trace_R"] == "-14/25"
    assert r["artifacts"]["det_R"] == "1"


def test_effect_completeness_is_not_dynamic_saturation():
    r = _pass("T_effect_completeness_does_not_imply_process_saturation")
    assert r["artifacts"]["S_u_present_as_physical_process"] is False


def test_generic_reflection_premise_removed():
    r = _pass("T_two_exchange_dependency_contract")
    assert r["artifacts"]["generic_sharp_reflection_premise_present"] is False
    assert r["artifacts"]["quadratic_ledger_present"] is False
    assert "RELOCATED" in r["artifacts"]["quadratic_ledger_disposition"]
    assert "R-capacity-bounded-world" in r["artifacts"]["quadratic_ledger_disposition"]
    assert "retired" not in r["artifacts"]["quadratic_ledger_disposition"].lower()


def test_missing_second_exchange_mutation_is_caught():
    r = _pass("T_two_exchange_dependency_contract")
    assert r["artifacts"]["missing_second_exchange_caught"]


def test_label_only_exchange_dies_in_effective_quotient():
    r = _pass("T_exchange_effectiveness_requires_recombination")
    assert r["artifacts"]["identity_representation_kills_exchange"]
    assert r["artifacts"]["readout_before"] != r["artifacts"]["readout_after"]


def _complete_payload(evidence="structural_derivation"):
    return {
        "evidence_class": evidence,
        "source_digest": "b" * 64,
        "codespace_to_fixed_line_certified": True,
        "second_binary_presentation_certified": True,
        "first_exchange_path_certified": True,
        "second_exchange_path_certified": True,
        "exchange_naturality_certified": True,
        "same_carrier_return_certified": True,
        "intertwiner_reversal_is_inverse_certified": True,
        "recombination_effectiveness_certified": True,
        "exact_overlap_certified": True,
        "first_exchange_matrix": th._matrix_strings(th.S_0),
        "second_exchange_matrix": th._matrix_strings(th.S_U),
        "finite_resolution_orbit_cover_certified": True,
    }


def test_structural_two_exchange_certificate_can_pass():
    rep = th.verify_two_exchange_interface_certificate(_complete_payload())
    assert rep["physical_premises_certified"]
    assert rep["gate_trace"] == "-14/25"


def test_experiment_cannot_certify_exact_gate():
    rep = th.verify_two_exchange_interface_certificate(_complete_payload("experiment"))
    assert not rep["physical_premises_certified"]
    assert rep["finite_resolution_interface_certified"]


def test_synthetic_reference_certifies_nothing():
    rep = th.verify_two_exchange_interface_certificate(_complete_payload("synthetic_reference"))
    assert not rep["physical_premises_certified"]
    assert not rep["finite_resolution_interface_certified"]


def test_missing_exchange_path_fails_closed():
    p = _complete_payload()
    p["second_exchange_path_certified"] = False
    rep = th.verify_two_exchange_interface_certificate(p)
    assert not rep["physical_premises_certified"]


def test_identity_second_action_fails_closed():
    p = _complete_payload()
    p["second_exchange_matrix"] = th._matrix_strings(th._eye())
    rep = th.verify_two_exchange_interface_certificate(p)
    assert not rep["physical_premises_certified"]


def test_wrong_overlap_finite_order_control_fails():
    p = _complete_payload()
    p["second_exchange_matrix"] = th._matrix_strings(th.P_SWAP)
    rep = th.verify_two_exchange_interface_certificate(p)
    assert not rep["physical_premises_certified"]


def test_empty_source_digest_fails_closed():
    p = _complete_payload()
    p["source_digest"] = ""
    rep = th.verify_two_exchange_interface_certificate(p)
    assert not rep["physical_premises_certified"]


def test_all_schema_checks_pass_but_physics_stays_open():
    results = th.run_all()
    assert all(r["passed"] for r in results.values())
    cert = th.build_certificate(results)
    assert cert.physical_premises_certified is False
    assert cert.physical_two_exchange_certificate_verified is False


# ---------------------------------------------------------------------------
# Fortification 2026-07-20: adversarial tests for the carried cold-audit MAJORs
# ---------------------------------------------------------------------------


def test_reversal_root_is_named_everywhere():
    """MAJOR-1: the .429 H1-genre gate is carried on every surface."""
    from apf.two_exchange_roots import PHYSICAL_ROOTS
    assert "INTERTWINER_REVERSAL_IS_INVERSE" in PHYSICAL_ROOTS
    assert "INTERTWINER_REVERSAL_IS_INVERSE" in th._graph()["T_SECOND_EXCHANGE"]
    assert "intertwiner_reversal_is_inverse_certified" in th.REQUIRED_CERT_FIELDS
    r = _pass("T_localized_binary_exchange_suffices")
    assert "INTERTWINER_REVERSAL_IS_INVERSE" in r["premises"]
    assert r["epistemic"] == "P_structural_instrument"


def test_removing_reversal_root_from_manifest_fails_consumers(monkeypatch):
    """MAJOR-1: deleting the root from the manifest fails the consuming checks."""
    pruned = tuple(x for x in th.PHYSICAL_ROOTS if x != "INTERTWINER_REVERSAL_IS_INVERSE")
    monkeypatch.setattr(th, "PHYSICAL_ROOTS", pruned)
    r = th.CHECKS["T_localized_binary_exchange_suffices"]()
    assert not r["passed"]
    assert any("INTERTWINER_REVERSAL_IS_INVERSE" in f for f in r["fail_reasons"])
    r2 = th.CHECKS["T_two_exchange_dependency_contract"]()
    assert not r2["passed"]


def test_removing_reversal_root_from_graph_fails_contract(monkeypatch):
    """MAJOR-1: deleting the root from the graph edge alone is also caught."""
    real = th._graph()
    pruned = dict(real)
    pruned["T_SECOND_EXCHANGE"] = tuple(
        d for d in pruned["T_SECOND_EXCHANGE"] if d != "INTERTWINER_REVERSAL_IS_INVERSE")
    monkeypatch.setattr(th, "_graph", lambda: pruned)
    r = th.CHECKS["T_two_exchange_dependency_contract"]()
    assert not r["passed"]
    r2 = th.CHECKS["T_localized_binary_exchange_suffices"]()
    assert not r2["passed"]


def test_missing_reversal_certification_fails_closed():
    """MAJOR-1: the certificate leaf is load-bearing in the verifier."""
    p = _complete_payload()
    p["intertwiner_reversal_is_inverse_certified"] = False
    rep = th.verify_two_exchange_interface_certificate(p)
    assert not rep["physical_premises_certified"]


def test_barred_quadratic_ledger_head_absent():
    """MAJOR-2: no surface applies the barred head to the quadratic ledger.

    Of record (check_L_bounded_orbit_positivity, v24.3.431) the quadratic
    ledger premise is RELOCATED at reading grade, never retired.  Bank-tree
    form: scan the landed module surfaces (module + roots + one-gate sibling).
    The packet-layout scan (AUDIT/README/tex) runs in the packet drop
    (Artifacts_2026-07-20_session/holonomy_gate_intake/), green there.
    """
    import re
    from pathlib import Path
    here = Path(__file__).resolve().parent.parent / "apf"
    pat = re.compile(r"retir", re.IGNORECASE)
    for rel in ("two_exchange_holonomy.py", "two_exchange_roots.py",
                "irrational_gate_holonomy.py"):
        text = (here / rel).read_text(encoding="utf-8")
        for m in pat.finditer(text):
            window = text[max(0, m.start() - 200):m.start() + 200].lower()
            assert "quadratic" not in window, (rel, window[:120])

def test_composed_supersession_machine_closed():
    """MAJOR-3: the retirement of the reflection root is machine-executed."""
    r = _pass("T_composed_route_supersedes_reflection_gate")
    roots = set(r["artifacts"]["composed_roots"])
    assert "PHYSICAL_SHARP_REFLECTION_IMPLEMENTABILITY" not in roots
    assert "CODESPACE_TO_HELD_CARRIER_IDENTIFICATION" not in roots
    assert "INTERTWINER_REVERSAL_IS_INVERSE" in roots
    assert "T_IRRATIONAL_GATE" in r["artifacts"]["composed_graph"]["T_BOUNDED_CYCLIC_CLOSURE"]
    assert r["artifacts"]["readded_root_caught"] is True
    assert r["artifacts"]["unspliced_bridge_caught"] is True


def test_readding_old_root_to_composed_graph_fails():
    """MAJOR-3: re-adding the superseded root must fail validation."""
    composed = th._composed_graph()
    mutated = dict(composed)
    mutated["T_ONE_GATE_CIRCLE"] = mutated["T_ONE_GATE_CIRCLE"] + (
        "PHYSICAL_SHARP_REFLECTION_IMPLEMENTABILITY",)
    fails = th._validate_composed(mutated)
    assert fails, "reintroduced reflection root must be caught"


def test_removing_bridge_splice_fails(monkeypatch):
    """MAJOR-3: removing the splice must fail the composed contract check."""
    from apf import irrational_gate_holonomy as og
    composed = th._composed_graph()
    unspliced = dict(composed)
    unspliced["T_BOUNDED_CYCLIC_CLOSURE"] = og._dependency_graph(
        "reflection")["T_BOUNDED_CYCLIC_CLOSURE"]
    assert th._validate_composed(unspliced), "unspliced graph must fail validation"
    monkeypatch.setattr(th, "_composed_graph", lambda: unspliced)
    r = th.CHECKS["T_composed_route_supersedes_reflection_gate"]()
    assert not r["passed"]


def test_executed_negative_controls_and_computed_legs():
    """Minors m1/m3/m6/m7: the formerly declarative legs now execute."""
    r = _pass("T_two_exchanges_generate_irrational_gate")
    assert r["artifacts"]["coincident_axis_control_executed"] is True
    assert r["artifacts"]["order_four_45_degree_control_executed"] is True
    r2 = _pass("T_effect_completeness_does_not_imply_process_saturation")
    assert r2["artifacts"]["static_effect_membership_computed"] is True
    assert r2["artifacts"]["cone_preservation_computed"] is True
    r3 = _pass("T_345_codespace_fixed_line_candidate")
    assert r3["artifacts"]["commutator_13"] == "12/25"
    assert r3["artifacts"]["commutator_31"] == "-12/25"
    r4 = _pass("T_live_source_concordance_and_nonclaim")
    assert r4["artifacts"]["correspondence_computed"] is True
    assert set(r4["artifacts"]["root_to_certificate_field"]) == set(th.PHYSICAL_ROOTS)


def test_root_manifest_is_split_from_consumer():
    """Minor m4 / mutation M7: the manifest lives in its own module."""
    import apf.two_exchange_roots as manifest
    import os
    assert os.path.basename(manifest.__file__) == "two_exchange_roots.py"
    assert th.PHYSICAL_ROOTS is manifest.PHYSICAL_ROOTS
