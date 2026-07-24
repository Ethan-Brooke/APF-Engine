"""Adversarial tests for :mod:`apf.zipper_bridge_bank_concordance`."""
from apf import zipper_bridge_bank_concordance as zbc


def _passed(result):
    assert result["passed"], result["fail_reasons"]
    assert result["physical_premises_certified"] is False
    return result


def test_exact_matrix_concordance_with_banked_two_exchange_route():
    r = _passed(zbc.check_T_zipper_two_exchange_matrix_concordance())
    assert all(r["artifacts"]["checks"].values())
    assert r["artifacts"]["zipper_Su"] == r["artifacts"]["banked_Su"]
    assert r["artifacts"]["zipper_R"] == r["artifacts"]["banked_R"]
    assert r["artifacts"]["trace_R"] == "-14/25"


def test_bridge_premises_map_to_existing_banked_root_vocabulary():
    r = _passed(zbc.check_T_zipper_bridge_premise_reconciliation())
    a = r["artifacts"]
    assert a["mapping_keys_exact"]
    assert a["missing_mapped_targets"] == {}
    assert a["physical_discharge_claimed"] is False
    assert set(a["bridge_to_banked_roots"]) == set(a["bridge_premises"])


def test_banked_routes_and_candidate_execute_without_physical_overclaim():
    r = _passed(zbc.check_T_banked_routes_and_bridge_execute_concordantly())
    a = r["artifacts"]
    assert a["failed"] == []
    assert a["incorrectly_physical_certified"] == []
    assert a["all_physical_premises_certified_false"]
    assert all(status == "PASS" for status in a["selected_status"].values())


def test_concordance_contract_rejects_physical_discharge_and_novelty_overclaim():
    r = _passed(zbc.check_T_zipper_bridge_bank_concordance_dependency_contract())
    a = r["artifacts"]
    assert a["forbidden_present"] == []
    assert a["physical_discharge_mutation_caught"]
    assert "PHYSICAL_PREMISES_DISCHARGED" in a["forbidden_claims"]
    assert a["bank_registration"] is False


def test_aggregate_certificate_is_concordance_only():
    results = zbc.run_all()
    assert all(row["passed"] for row in results.values())
    cert = zbc.build_certificate(results)
    assert cert.matrices_concordant
    assert cert.banked_checks_green
    assert cert.premise_vocabulary_reconciled
    assert cert.no_duplicate_physical_certification
    assert cert.dependency_contract_clean
    assert cert.physical_premises_certified is False
