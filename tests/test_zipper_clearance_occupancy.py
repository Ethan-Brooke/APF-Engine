"""Adversarial tests for :mod:`apf.zipper_clearance_occupancy`."""
from apf import zipper_clearance_occupancy as zco


def _passed(result):
    assert result["passed"], result["fail_reasons"]
    assert result["physical_premises_certified"] is False
    return result


def test_no_early_irreversible_winner_can_use_both_later_contexts():
    r = _passed(zco.check_T_premature_commitment_obstruction())
    a = r["artifacts"]
    assert a["early_functions_checked"] == 4
    assert a["successful_early_functions"] == 0
    assert a["minimum_mismatch_count"] == 2
    assert a["late_context_is_load_bearing"]


def test_context_only_local_rule_cannot_retain_preparation_dependence():
    r = _passed(zco.check_T_local_witness_requires_present_mediator())
    a = r["artifacts"]
    assert a["no_mediator_functions_checked"] == 4
    assert a["no_mediator_success_count"] == 0
    assert a["mediator_success"]


def test_global_oracle_is_exposed_as_load_bearing_countermodel():
    r = _passed(zco.check_T_local_witness_requires_present_mediator())
    a = r["artifacts"]
    assert a["global_oracle_success"]
    assert a["oracle_violates_local_factorization"]


def test_present_mediator_is_record_null_but_completion_distinguishable():
    r = _passed(zco.check_T_record_null_mediator_is_active_kernel())
    a = r["artifacts"]
    assert a["current_record_map"] == {"0": 0, "1": 0}
    assert a["distinguishing_completions"] == [0, 1]
    assert a["nontrivial_active_record_kernel"]
    assert a["quantum_noncommutativity_derived"] is False


def test_parallel_booking_is_possible_but_not_clearance():
    r = _passed(zco.check_T_parallel_booking_is_costly_rival_not_clearance())
    a = r["artifacts"]
    assert a["parallel_booking_logically_possible"]
    assert a["same_as_record_free_clearance"] is False
    assert a["two_branch_cost"] == "2"
    assert a["rejected_record_persists"]


def test_predetermined_structure_does_not_require_clearance():
    r = _passed(zco.check_T_predetermined_and_classical_controls())
    a = r["artifacts"]
    assert a["predetermined_control_success"]
    assert a["predetermined_structure_needs_clearance"] is False


def test_classical_hidden_mediator_survives_and_fences_quantum_overclaim():
    r = _passed(zco.check_T_predetermined_and_classical_controls())
    a = r["artifacts"]
    assert a["classical_hidden_mediator_success"]
    assert a["classical_context_updates_commute"]
    assert a["noncommutativity_derived"] is False
    assert a["complex_structure_derived"] is False
    assert a["Born_rule_derived"] is False


def test_clearance_dependency_contract_forbids_quantum_and_oracle_smuggling():
    r = _passed(zco.check_T_zipper_clearance_dependency_contract())
    a = r["artifacts"]
    assert a["cycle"] is None
    assert a["quantum_smuggling_mutation_caught"]
    assert a["oracle_smuggling_mutation_caught"]
    assert a["cycle_mutation_caught"]
    assert "QUANTUM_OCCUPANCY_ASSUMED" not in a["upstream_of_active_record_kernel"]
    assert "GLOBAL_FUTURE_ORACLE" not in a["upstream_of_active_record_kernel"]


def test_aggregate_clearance_certificate_is_conditional_and_unbanked():
    rows = zco.run_all()
    assert all(row["passed"] for row in rows.values())
    cert = zco.build_certificate(rows)
    assert cert.premature_commitment_obstruction_exact
    assert cert.local_witness_necessity_exact
    assert cert.held_kernel_witness_exact
    assert cert.parallel_booking_control_exact
    assert cert.oracle_control_exposed
    assert cert.predetermined_control_exposed
    assert cert.classical_mediator_scope_fenced
    assert cert.dependency_contract_clean
    assert cert.physical_premises_certified is False
