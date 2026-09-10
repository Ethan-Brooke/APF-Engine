"""Adversarial tests for :mod:`apf.zipper_reflection_bridge`."""
from apf import zipper_reflection_bridge as zrb


def _passed(result):
    assert result["passed"], result["fail_reasons"]
    assert result["physical_premises_certified"] is False
    return result


def test_binary_port_exchange_descends_to_metric_reflection():
    r = _passed(zrb.check_T_effective_port_exchange_is_operational_reflection())
    assert r["artifacts"]["tau_0"] == [["1", "0"], ["0", "-1"]]
    assert r["artifacts"]["common_fixed"]
    assert r["artifacts"]["defect_reversed"]


def test_defect_killed_label_swap_descends_to_identity():
    r = _passed(zrb.check_T_effective_port_exchange_is_operational_reflection())
    assert r["artifacts"]["total_only_rank"] == 1
    assert r["artifacts"]["total_only_swap_descends_to_identity"]
    assert r["artifacts"]["defect_killed_by_total_only_quotient"]


def test_static_effects_do_not_supply_exchange_process():
    r = _passed(zrb.check_T_effective_port_exchange_is_operational_reflection())
    assert r["artifacts"]["static_effects_exist"]
    assert r["artifacts"]["static_effects_supply_exchange_process"] is False


def test_active_conjugation_recovers_right_trivialized_generator():
    r = _passed(zrb.check_T_conjugated_exchange_orbit_recovers_holonomy_generator())
    assert r["artifacts"]["generic_identity"] == "A=(K-tau K tau)/2"
    assert r["artifacts"]["rank_two_SO2_reduction"] == "tau K tau=-K => A=K"
    assert len(r["artifacts"]["samples"]) == 6
    for row in r["artifacts"]["samples"]:
        assert row["K=U_dot_U_inv"] == row["A=(1/2)tau_dot_tau"]
        assert row["J"] == [["0", "-1"], ["1", "0"]]


def test_passive_convention_reverses_generator_sign():
    r = _passed(zrb.check_T_conjugated_exchange_orbit_recovers_holonomy_generator())
    for row in r["artifacts"]["samples"]:
        active = row["A=(1/2)tau_dot_tau"]
        passive = row["passive_A"]
        assert passive == [[str(-zrb.F(x)) for x in arow] for arow in active]


def test_commuting_transport_is_projected_out():
    r = _passed(zrb.check_T_conjugated_exchange_orbit_recovers_holonomy_generator())
    assert r["artifacts"]["commuting_transport_projection_control"]
    assert r["artifacts"]["moving_exchange_recovers_commuting_component"] is False


def test_live_345_zipper_transports_second_exchange():
    r = _passed(zrb.check_T_live_345_zipper_transports_second_exchange())
    assert r["artifacts"]["det_F345"] == "-2"
    assert r["artifacts"]["trace_R"] == "-14/25"
    assert r["artifacts"]["det_R"] == "1"
    assert r["artifacts"]["effective_second_path_required"]


def test_label_only_second_exchange_kills_rotation():
    r = _passed(zrb.check_T_live_345_zipper_transports_second_exchange())
    assert r["artifacts"]["label_only_second_exchange_image"] == [["1", "0"], ["0", "1"]]
    assert r["artifacts"]["label_only_product"] == [["1", "0"], ["0", "-1"]]


def test_dependency_contract_forbids_effect_and_quarter_turn_smuggling():
    r = _passed(zrb.check_T_operational_reflection_bridge_dependency_contract())
    a = r["artifacts"]
    assert a["cycle"] is None
    assert a["effect_saturation_smuggling_caught"]
    assert a["quarter_turn_smuggling_caught"]
    assert a["direct_gate_deletion_caught"]
    assert "QUARTER_TURN_ASSUMED" not in a["upstream_of_local_J"]


def test_cli_certificate_remains_unbanked_and_uncertified():
    results = zrb.run_all()
    assert all(row["passed"] for row in results.values())
    cert = zrb.build_certificate(results)
    assert cert.effective_port_exchange_reflection_exact
    assert cert.conjugated_exchange_generator_exact
    assert cert.live_345_transported_exchange_exact
    assert cert.label_only_exchange_rejected
    assert cert.static_effect_saturation_rejected
    assert cert.commuting_transport_projection_exposed
    assert cert.dependency_contract_clean
    assert cert.physical_premises_certified is False
