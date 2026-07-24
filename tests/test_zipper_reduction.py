"""Adversarial tests for :mod:`apf.zipper_reduction`."""

from fractions import Fraction as F

import pytest

from apf import zipper_reduction as zr


def _passed(result):
    assert result["passed"], result["fail_reasons"]
    assert result["physical_premises_certified"] is False
    return result


def test_exact_formula_recovers_J_on_rational_family():
    r = _passed(zr.check_T_moving_exchange_formula_exact())
    assert r["artifacts"]["sample_count"] == 7
    assert all(row["J"] == [["0", "-1"], ["1", "0"]] for row in r["artifacts"]["samples"])


def test_constructor_returns_J_squared_minus_identity():
    tau, tau_dot = zr._moving_reflection(F(1, 3))
    cert = zr.derive_complex_structure(tau, tau_dot)
    assert zr._mm(cert["J"], cert["J"]) == zr._scale(F(-1), zr.I2)
    assert cert["omega"] == F(9, 5)


def test_metric_covariance_on_non_euclidean_positive_plane():
    r = _passed(zr.check_T_moving_exchange_metric_covariance())
    assert r["artifacts"]["J"] == r["artifacts"]["expected_J"]
    assert r["artifacts"]["omega"] == "18/13"


def test_orientation_sign_is_only_local_ambiguity():
    r = _passed(zr.check_T_moving_exchange_orientation_sign())
    assert r["artifacts"]["positive_speed_J"] == [["0", "-1"], ["1", "0"]]
    assert r["artifacts"]["negative_speed_J"] == [["0", "1"], ["-1", "0"]]
    assert r["artifacts"]["orientation_ambiguity"] == "J <-> -J"


def test_two_exchange_frames_generate_rotation_holonomy():
    r = _passed(zr.check_T_two_exchange_product_holonomy())
    assert r["artifacts"]["det_holonomy"] == "1"
    assert r["artifacts"]["individual_exchanges_reverse_J"]
    assert r["artifacts"]["product_commutes_with_J"]


def test_stationary_frame_fails_closed():
    with pytest.raises(ValueError, match="stationary"):
        zr.derive_complex_structure(zr.S0, zr._zero(2))


def test_bad_involution_tangent_fails_closed():
    with pytest.raises(ValueError, match="differentiated involution"):
        zr.derive_complex_structure(zr.S0, zr.I2)


def test_indefinite_signature_is_load_bearing_control():
    r = _passed(zr.check_T_zipper_formula_negative_controls())
    assert r["artifacts"]["indefinite_radicand"].startswith("-")
    assert "positive-definite" in r["artifacts"]["indefinite_error"]


def test_rank_two_scope_is_explicitly_fenced():
    r = _passed(zr.check_T_zipper_formula_negative_controls())
    assert r["artifacts"]["rank_four_A2_not_single_frequency"] is True
    assert "rank-two" in r["artifacts"]["rank_four_error"]


def test_dependency_contract_forbids_downstream_smuggling():
    r = _passed(zr.check_T_zipper_reduction_dependency_contract())
    assert r["artifacts"]["cycle"] is None
    assert r["artifacts"]["cycle_mutation_caught"]
    assert r["artifacts"]["hilbert_smuggling_mutation_caught"]
    assert r["artifacts"]["direct_gate_deletion_caught"]
    assert r["artifacts"]["extra_gate_mutation_caught"]
    assert "HILBERT_SPACE" in r["artifacts"]["forbidden_upstream"]
    assert "BORN_RULE" in r["artifacts"]["forbidden_upstream"]
    assert r["artifacts"]["bank_registration"] is False


def test_cli_certificate_keeps_physical_premises_uncertified():
    results = zr.run_all()
    cert = zr.build_certificate(results)
    assert all(row["passed"] for row in results.values())
    assert cert.moving_exchange_formula_exact
    assert cert.metric_covariance_exact
    assert cert.indefinite_signature_rejected
    assert cert.rank_two_scope_fenced
    assert cert.physical_premises_certified is False
