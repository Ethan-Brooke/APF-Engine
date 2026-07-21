"""Adversarial tests for :mod:`apf.hfc_345_closure`."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from apf import hfc_345_closure as h

# Bank-landing adaptation (v24.3.432): the verifier/DATA/tex integration tests
# require the PACKET layout (DATA/, verify_physical_interface_certificate.py,
# manuscript files). In the bank tree they SKIP with a pointer to the packet
# drop (Artifacts_2026-07-20_session/holonomy_gate_intake/), where they run
# green. The module-level checks run unconditionally.
_PACKET_LAYOUT = (h.PACKAGE_ROOT / "DATA" / "physical_leaf_manifest.json").is_file()
requires_packet = pytest.mark.skipif(
    not _PACKET_LAYOUT,
    reason="packet-layout integration test; green in the packet drop "
           "(holonomy_gate_intake)")


def _pass(name: str):
    result = h.CHECKS[name]()
    assert result["passed"], result["fail_reasons"]
    assert result["physical_premises_certified"] is False
    return result


def test_neutral_spectator_split_is_exact():
    r = _pass("T_345_neutral_spectator_restriction")
    assert r["artifacts"]["active_restriction"] == [["9/25", "12/25"], ["12/25", "16/25"]]
    assert r["artifacts"]["e2_fixed"] is True
    assert r["artifacts"]["e2_globally_null"] is False


def test_active_plane_is_character_carrier_not_first_jet():
    r = _pass("T_character_carrier_not_first_jet")
    assert r["artifacts"]["canonical_identification_claimed"] is False
    assert r["artifacts"]["first_order_character_lift_rank"] == 4


def test_hfc_345_dilation_columns_are_exact_ports():
    r = _pass("T_hfc_345_conservative_dilation")
    assert r["artifacts"]["F_345"] == [["-1/5", "7/5"], ["7/5", "1/5"]]
    assert r["artifacts"]["common_axis"] == ["3/5", "4/5"]
    assert r["artifacts"]["defect_axis"] == ["-4/5", "3/5"]
    assert r["artifacts"]["visible_commoning_Pu_F345"] == [["3/5", "3/5"], ["4/5", "4/5"]]
    assert r["artifacts"]["retained_defect_(I-Pu)_F345"] == [["-4/5", "4/5"], ["3/5", "-3/5"]]


def test_dseb_is_derived_not_a_root():
    r = _pass("T_DSEB_345_discharged_from_HFC")
    assert r["artifacts"]["DSEB_345_independent_root"] is False
    assert r["artifacts"]["first_jet_identification_consumed"] is False
    assert r["artifacts"]["transported_exchange"] == [["-7/25", "24/25"], ["24/25", "7/25"]]


def test_two_exchanges_give_exact_algebraic_J():
    r = _pass("T_two_exchange_gate_and_algebraic_J")
    assert r["artifacts"]["R"] == [["-7/25", "-24/25"], ["24/25", "-7/25"]]
    assert r["artifacts"]["J"] == [["0", "-1"], ["1", "0"]]
    assert r["artifacts"]["J_square"] == [["-1", "0"], ["0", "-1"]]
    assert r["artifacts"]["physical_J_process_claimed"] is False


def test_circle_is_optional_not_load_bearing_for_J():
    r = _pass("T_optional_dense_circle_corollary")
    assert r["artifacts"]["circle_load_bearing_for_J"] is False
    assert r["artifacts"]["finite_order_hit"] is None


def test_complete_defect_makes_exchange_effective():
    r = _pass("T_effectiveness_from_complete_defect")
    assert r["artifacts"]["signature_before"] != r["artifacts"]["signature_after"]
    assert r["artifacts"]["present_contender_record_formed"] is False


def test_hfc_is_logically_independent_of_minimal_base():
    r = _pass("T_HFC_independence_countermodel")
    assert r["artifacts"]["HFC_derived_from_A1_MD_A2_BW"] is False
    assert r["artifacts"]["nonzero_positive_exchange_odd_exists"] is False


def test_orientation_and_positivity_branches_are_parallel():
    r = _pass("T_parallel_orientation_positivity_no_cycle")
    assert r["artifacts"]["local_J_consumes_positivity"] is False
    assert r["artifacts"]["positivity_consumes_local_J"] is False
    assert r["artifacts"]["branches_meet_at"] == "T_COMPLEX_CSTAR"
    assert r["artifacts"]["cycle_mutation_caught"] is True


def test_dependency_contract_uses_independent_manifest():
    r = _pass("T_hfc_345_dependency_contract")
    assert r["artifacts"]["DSEB_345_is_root"] is False
    assert r["artifacts"]["added_root_mutation_caught"] is True
    assert r["artifacts"]["removed_leaf_mutation_caught"] is True
    assert r["artifacts"]["te_gate_removal_mutation_caught"] is True
    assert r["artifacts"]["first_jet_conflation_caught"] is True


def _complete_payload(tmp_path: Path, manifest_path: Path | None = None):
    path = manifest_path or h.LEAF_MANIFEST_PATH
    manifest = json.loads(path.read_text(encoding="utf-8"))
    evidence = {}
    evidence_dir = tmp_path / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    for name, meta in manifest["leaves"].items():
        evidence_class = "structural_derivation" if meta["type"] == "structural" else "principal_adoption"
        source = evidence_dir / f"{name}.txt"
        source.write_text(f"synthetic test evidence for {name}\n", encoding="utf-8")
        evidence[name] = {
            "certified": True,
            "evidence_class": evidence_class,
            "source_path": str(source),
            "source_digest": hashlib.sha256(source.read_bytes()).hexdigest(),
        }
    return {
        "schema_version": manifest["schema_version"],
        "claim": manifest["claim"],
        "evidence": evidence,
        "claimed_matrices": {
            "first_exchange": h._matrix_strings(h.S_0),
            "second_exchange": h._matrix_strings(h.S_U),
            "product_gate": h._matrix_strings(h.R_345),
            "derived_J": h._matrix_strings(h.J_345),
        },
        "physical_premises_certified": False,
    }


@requires_packet
def test_external_certificate_can_pass_only_with_all_manifest_leaves(tmp_path: Path):
    rep = h.verify_physical_interface_certificate(_complete_payload(tmp_path))
    assert rep["physical_premises_certified"] is True
    assert rep["DSEB_345_certified"] is True
    assert rep["local_J_certified"] is True


@requires_packet
def test_missing_hfc_fails_closed(tmp_path: Path):
    payload = _complete_payload(tmp_path)
    payload["evidence"]["LIVE_345_HELD_FAIR_COMMONING"]["certified"] = False
    rep = h.verify_physical_interface_certificate(payload)
    assert rep["physical_premises_certified"] is False
    assert any("LIVE_345_HELD_FAIR_COMMONING" in x for x in rep["failures"])


@requires_packet
def test_extra_empirical_root_fails_inventory(tmp_path: Path):
    payload = _complete_payload(tmp_path)
    payload["evidence"]["SECOND_EMPIRICAL_ROOT"] = {
        "certified": True,
        "evidence_class": "experiment",
        "source_digest": "c" * 64,
    }
    rep = h.verify_physical_interface_certificate(payload)
    assert rep["physical_premises_certified"] is False
    assert any("leaf inventory mismatch" in x for x in rep["failures"])


@requires_packet
def test_finite_precision_cannot_certify_exact_345_geometry(tmp_path: Path):
    payload = _complete_payload(tmp_path)
    payload["evidence"]["EXACT_345_DEFENDER_GEOMETRY"]["evidence_class"] = "experiment"
    rep = h.verify_physical_interface_certificate(payload)
    assert rep["physical_premises_certified"] is False
    assert any("exact geometry" in x for x in rep["failures"])


@requires_packet
def test_wrong_second_exchange_matrix_fails(tmp_path: Path):
    payload = _complete_payload(tmp_path)
    payload["claimed_matrices"]["second_exchange"] = h._matrix_strings(h.S_0)
    rep = h.verify_physical_interface_certificate(payload)
    assert rep["physical_premises_certified"] is False
    assert any("second_exchange" in x for x in rep["failures"])


@requires_packet
def test_wrong_J_matrix_fails(tmp_path: Path):
    payload = _complete_payload(tmp_path)
    payload["claimed_matrices"]["derived_J"] = h._matrix_strings(h._eye2())
    rep = h.verify_physical_interface_certificate(payload)
    assert rep["physical_premises_certified"] is False
    assert any("derived_J" in x for x in rep["failures"])


@requires_packet
def test_payload_may_not_self_declare_success(tmp_path: Path):
    payload = _complete_payload(tmp_path)
    payload["physical_premises_certified"] = True
    rep = h.verify_physical_interface_certificate(payload)
    assert rep["physical_premises_certified"] is False
    assert any("self-declare" in x for x in rep["failures"])


@requires_packet
def test_empty_digest_fails_closed(tmp_path: Path):
    payload = _complete_payload(tmp_path)
    payload["evidence"]["LIVE_345_HELD_FAIR_COMMONING"]["source_digest"] = ""
    rep = h.verify_physical_interface_certificate(payload)
    assert rep["physical_premises_certified"] is False
    assert any("source_digest" in x for x in rep["failures"])


@requires_packet
def test_fake_digest_fails_against_source_bytes(tmp_path: Path):
    payload = _complete_payload(tmp_path)
    payload["evidence"]["LIVE_345_HELD_FAIR_COMMONING"]["source_digest"] = "a" * 64
    rep = h.verify_physical_interface_certificate(payload)
    assert rep["physical_premises_certified"] is False
    assert any("does not match source bytes" in x for x in rep["failures"])


@requires_packet
def test_missing_source_file_fails_closed(tmp_path: Path):
    payload = _complete_payload(tmp_path)
    payload["evidence"]["LIVE_345_HELD_FAIR_COMMONING"]["source_path"] = str(tmp_path / "missing.txt")
    rep = h.verify_physical_interface_certificate(payload)
    assert rep["physical_premises_certified"] is False
    assert any("source_path does not exist" in x for x in rep["failures"])


@requires_packet
def test_manifest_mutation_is_detected(tmp_path: Path):
    manifest = json.loads(h.LEAF_MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["leaves"]["UNDECLARED_NEW_LEAF"] = {
        "type": "physical",
        "description": "mutation",
    }
    mutated = tmp_path / "manifest.json"
    mutated.write_text(json.dumps(manifest), encoding="utf-8")
    payload = _complete_payload(tmp_path)
    rep = h.verify_physical_interface_certificate(payload, manifest_path=mutated)
    assert rep["physical_premises_certified"] is False
    assert any("leaf inventory mismatch" in x for x in rep["failures"])


@requires_packet
def test_synthetic_template_stays_uncertified():
    template = json.loads((h.PACKAGE_ROOT / "DATA" / "physical_interface_certificate_template.json").read_text())
    rep = h.verify_physical_interface_certificate(template)
    assert rep["physical_premises_certified"] is False
    assert len(rep["failures"]) > 0


def test_all_schema_checks_pass_while_physics_stays_open():
    rows = h.run_all()
    assert all(r["passed"] for r in rows.values())
    cert = h.build_certificate(rows)
    assert cert.dseb_345_discharged_relative_to_hfc is True
    assert cert.algebraic_J_exact is True
    assert cert.physical_premises_certified is False
    assert cert.physical_interface_certificate_verified is False


# ---------------------------------------------------------------------------
# Fortification battery (2026-07-20 cold audit; one adversarial test per MAJOR)
# ---------------------------------------------------------------------------

CENTRAL_J_GATES = ("T_LOCAL_J", "NATURALITY", "ORIENTATION_SYNCHRONIZATION", "GENERATOR_COMPLETENESS")


def test_major1_central_j_gate_contract_kills_every_single_gate_deletion():
    """The audited M6 mutation (and every sibling deletion) must now fail a check."""
    r = _pass("T_central_j_gate_contract")
    assert set(r["artifacts"]["required_gates"]) == set(CENTRAL_J_GATES)
    assert r["artifacts"]["m6_mutation_caught"] is True
    orig = h.FULL_PARALLEL_GRAPH["T_CENTRAL_J"]
    assert set(orig) == set(CENTRAL_J_GATES)
    try:
        for gate in CENTRAL_J_GATES:
            h.FULL_PARALLEL_GRAPH["T_CENTRAL_J"] = tuple(g for g in orig if g != gate)
            res = h.CHECKS["T_central_j_gate_contract"]()
            assert res["passed"] is False, f"deletion of {gate} must fail the gate contract"
            assert any("drift" in x for x in res["fail_reasons"])
    finally:
        h.FULL_PARALLEL_GRAPH["T_CENTRAL_J"] = orig
    assert h.CHECKS["T_central_j_gate_contract"]()["passed"] is True


def test_major1_gate_inventory_is_stored_in_a_separate_module():
    from apf._hfc_345_contracts import CENTRAL_J_REQUIRED_GATES
    assert tuple(sorted(CENTRAL_J_REQUIRED_GATES)) == tuple(sorted(CENTRAL_J_GATES))
    assert (h.PACKAGE_ROOT / "apf" / "_hfc_345_contracts.py").is_file()


@requires_packet
def test_major2_restored_te_gates_are_leaves_and_removal_is_caught():
    manifest = json.loads(h.LEAF_MANIFEST_PATH.read_text(encoding="utf-8"))
    assert "ZIPPER_REVERSAL_IS_INVERSE" in manifest["leaves"]
    assert "EXCHANGE_CARGO_NATURALITY" in manifest["leaves"]
    assert len(manifest["leaves"]) == 13
    r = _pass("T_DSEB_345_discharged_from_HFC")
    assert "ZIPPER_REVERSAL_IS_INVERSE" in r["premises"]
    assert "EXCHANGE_CARGO_NATURALITY" in r["premises"]
    orig = h.DSEB_GRAPH["T_SECOND_EXCHANGE"]
    try:
        for gate in ("ZIPPER_REVERSAL_IS_INVERSE", "EXCHANGE_CARGO_NATURALITY"):
            h.DSEB_GRAPH["T_SECOND_EXCHANGE"] = tuple(d for d in orig if d != gate)
            res = h.CHECKS["T_hfc_345_dependency_contract"]()
            assert res["passed"] is False, f"removal of {gate} must fail the dependency contract"
    finally:
        h.DSEB_GRAPH["T_SECOND_EXCHANGE"] = orig
    assert h.CHECKS["T_hfc_345_dependency_contract"]()["passed"] is True


def _substituted_manifest(tmp_path: Path, leaf_names):
    manifest = json.loads(h.LEAF_MANIFEST_PATH.read_text(encoding="utf-8"))
    full = manifest["leaves"]
    manifest["leaves"] = {
        name: full.get(name, {"type": "physical", "description": "substituted"})
        for name in leaf_names
    }
    mp = tmp_path / "substituted_manifest.json"
    mp.write_text(json.dumps(manifest), encoding="utf-8")
    return mp


@requires_packet
def test_major3_v2_one_leaf_manifest_substitution_is_rejected(tmp_path: Path):
    """Reproduces the audit's V2 probe; it must now fail closed."""
    mp = _substituted_manifest(tmp_path, ["LIVE_345_HELD_FAIR_COMMONING"])
    payload = _complete_payload(tmp_path, manifest_path=mp)
    rep = h.verify_physical_interface_certificate(payload, manifest_path=mp)
    assert rep["physical_premises_certified"] is False
    assert rep["manifest_is_packet_pinned"] is False
    assert any("manifest override rejected" in x for x in rep["failures"])
    assert any("DSEB_GRAPH root inventory" in x for x in rep["failures"])


@requires_packet
def test_major3_supermanifest_with_extra_root_is_rejected(tmp_path: Path):
    manifest = json.loads(h.LEAF_MANIFEST_PATH.read_text(encoding="utf-8"))
    names = list(manifest["leaves"]) + ["FRIENDLY_EXTRA_LEAF"]
    mp = _substituted_manifest(tmp_path, names)
    payload = _complete_payload(tmp_path, manifest_path=mp)
    rep = h.verify_physical_interface_certificate(payload, manifest_path=mp)
    assert rep["physical_premises_certified"] is False
    assert any("manifest override rejected" in x for x in rep["failures"])
    assert any("extra=['FRIENDLY_EXTRA_LEAF']" in x for x in rep["failures"])


@requires_packet
def test_major3_verifier_consults_graph_even_for_packet_manifest(tmp_path: Path):
    """If the graph and manifest drift apart, the verifier itself must fail closed."""
    payload = _complete_payload(tmp_path)
    orig = h.DSEB_GRAPH["T_SECOND_EXCHANGE"]
    try:
        h.DSEB_GRAPH["T_SECOND_EXCHANGE"] = tuple(
            d for d in orig if d != "ZIPPER_REVERSAL_IS_INVERSE"
        )
        rep = h.verify_physical_interface_certificate(payload)
        assert rep["physical_premises_certified"] is False
        assert any("DSEB_GRAPH root inventory" in x for x in rep["failures"])
    finally:
        h.DSEB_GRAPH["T_SECOND_EXCHANGE"] = orig


@requires_packet
def test_major3_evidence_is_billed_as_digest_resolution_only(tmp_path: Path):
    rep = h.verify_physical_interface_certificate(_complete_payload(tmp_path))
    assert rep["evidence_semantics_verified"] is False
    assert "digest resolution only" in rep["evidence_billing"]


@requires_packet
def test_major4_phantom_provenance_is_gone():
    """The two phantom source theorems may not appear as pre-existing results."""
    scan = [
        "README.md",
        "APF_Fair_Commoning_Closes_345_Bridge_v0.4.tex",
        "AUDIT/SOURCE_CONCORDANCE.md",
        "AUDIT/CLAIM_LEDGER.md",
        "AUDIT/ROUTE_CONCORDANCE.md",
        "AUDIT/HOSTILE_AUDIT.md",
        "AUDIT/PHYSICAL_CERTIFICATION_CHARTER.md",
        "apf/hfc_345_closure.py",
        "apf/_hfc_345_contracts.py",
    ]
    withdrawal_markers = (
        "withdrawn", "false", "may-not-cite", "may not be cited", "not pre-existing",
        "new construction", "no such banked object",
    )
    phantom_phrases = (
        "already present in the APF architecture",
        "Conservative Dilation Theorem",
    )
    for rel in scan:
        text = (h.PACKAGE_ROOT / rel).read_text(encoding="utf-8")
        for line in text.splitlines():
            low = line.lower()
            for phrase in phantom_phrases:
                if phrase in line:
                    # A phantom name may survive only inside an explicit
                    # withdrawal / MAY-NOT-CITE context, never as billing.
                    assert any(k in low for k in withdrawal_markers), (rel, phrase, line)
            if "HFC-to-HOC reduction" in line:
                assert any(
                    k in low
                    for k in ("new", "this packet", "packet-local") + withdrawal_markers
                ), (rel, line)


def test_countermodel_grid_is_discriminating_not_theater():
    r = _pass("T_HFC_independence_countermodel")
    assert r["artifacts"]["nonpointed_odd_survivors"] == 9
    assert r["artifacts"]["nonpointed_nonzero_odd_survivors"] == 8
    assert r["artifacts"]["pointedness_is_load_bearing"] is True


def test_first_order_lift_rank_is_computed_not_asserted():
    r = _pass("T_character_carrier_not_first_jet")
    assert r["artifacts"]["first_order_lift_rank_computed_from_jet_matrix"] is True
    assert r["artifacts"]["zero_velocity_control_rank"] == 2
