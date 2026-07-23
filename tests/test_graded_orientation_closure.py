from fractions import Fraction as F
from pathlib import Path
import importlib.util
import json
import os
import subprocess
import sys

import pytest

from apf import graded_orientation_closure as m

# Bank-landing adaptation (v24.3.433): the verifier/DATA/AUDIT integration
# tests require the PACKET layout (DATA/, verify_orientation_network_certificate.py,
# AUDIT/run_hostile_audit.py). In the bank tree they SKIP with a pointer to the
# packet drop (holonomy_gate_intake / APF_Graded_Orientation_Closure_v0.5),
# where they run green. The module-level checks run unconditionally.
_PACKET_ROOT = Path(m.__file__).resolve().parents[1]
_PACKET_LAYOUT = (
    (_PACKET_ROOT / "verify_orientation_network_certificate.py").is_file()
    and (_PACKET_ROOT / "DATA" / "orientation_network_certificate_template.json").is_file()
)
requires_packet = pytest.mark.skipif(
    not _PACKET_LAYOUT,
    reason="packet-layout integration test; green in the packet drop "
           "(holonomy_gate_intake, APF_Graded_Orientation_Closure_v0.5)")
_AUDIT_LAYOUT = (_PACKET_ROOT / "AUDIT" / "run_hostile_audit.py").is_file()
requires_audit = pytest.mark.skipif(
    not _AUDIT_LAYOUT,
    reason="packet AUDIT-layout test; green in the packet drop "
           "(holonomy_gate_intake, APF_Graded_Orientation_Closure_v0.5)")


def test_all_schema_checks_pass():
    rows = m.run_all()
    assert len(rows) == 9
    assert all(row["passed"] for row in rows.values())


def test_reflections_anticommute_with_local_J():
    assert m._mm(m.S0, m.J) == m._scale(F(-1), m._mm(m.J, m.S0))
    assert m._mm(m.SU, m.J) == m._scale(F(-1), m._mm(m.J, m.SU))


def test_local_J_is_not_central_in_undoubled_algebra():
    basis = m._algebra_closure((m.I2, m.S0, m.SU))
    assert len(basis) == 4
    assert m._center_dimension(basis) == 1
    assert m._mm(m.J, m.S0) != m._mm(m.S0, m.J)


def test_even_algebra_is_complex_line():
    basis = m._algebra_closure((m.I2, m.R))
    assert len(basis) == 2
    assert m._mm(m.J, m.J) == m._scale(F(-1), m.I2)
    assert all(m._mm(x, m.J) == m._mm(m.J, x) for x in basis)


def test_wrong_same_orientation_doubling_fails_naturality():
    wrong_J = m._block(m.J, m.Z2, m.Z2, m.J)
    assert m._mm(wrong_J, m.D0) != m._mm(m.D0, wrong_J)
    assert m._mm(wrong_J, m.DU) != m._mm(m.DU, wrong_J)


def test_oriented_double_cover_commutes_with_both_exchanges():
    assert m.J_OR == m._block(m.J, m.Z2, m.Z2, m._scale(F(-1), m.J))
    assert m._mm(m.J_OR, m.D0) == m._mm(m.D0, m.J_OR)
    assert m._mm(m.J_OR, m.DU) == m._mm(m.DU, m.J_OR)


def test_oriented_linking_algebra_is_eight_dimensional():
    basis = m._algebra_closure((m.I4, m.P_PLUS, m.P_MINUS, m.D0, m.DU))
    assert len(basis) == 8
    assert m._commutant_dimension(m.J_OR) == 8
    assert m._center_dimension(basis) == 2


def test_object_projections_are_load_bearing():
    without_projections = m._algebra_closure((m.I4, m.D0, m.DU))
    with_projections = m._algebra_closure((m.I4, m.P_PLUS, m.P_MINUS, m.D0, m.DU))
    assert len(without_projections) < len(with_projections)
    assert len(with_projections) == 8


def test_orientable_parity_cycle_has_sign_assignment():
    result = m.solve_orientation_signs(
        ("A", "B", "C"),
        (("A", "B", -1), ("B", "C", -1), ("C", "A", 1)),
    )
    assert result["orientable"]
    signs = result["signs"]
    assert signs["B"] == -signs["A"]
    assert signs["C"] == -signs["B"]
    assert signs["A"] == signs["C"]


def test_odd_parity_cycle_is_nonorientable():
    result = m.solve_orientation_signs(
        ("A", "B", "C"),
        (("A", "B", -1), ("B", "C", 1), ("C", "A", 1)),
    )
    assert not result["orientable"]
    assert result["failures"]


def test_double_cover_repairs_nonorientable_network():
    vertices = ("A", "B", "C")
    edges = (("A", "B", -1), ("B", "C", 1), ("C", "A", 1))
    cover = m.orientation_double_cover_graph(vertices, edges)
    names = [f"{v}:{s:+d}" for v, s in cover["vertices"]]
    lifted = [
        (f"{u[0]}:{u[1]:+d}", f"{v[0]}:{v[1]:+d}", eps)
        for u, v, eps in cover["edges"]
    ]
    result = m.solve_orientation_signs(names, lifted)
    assert result["orientable"]


def test_invalid_parity_rejected():
    result = m.solve_orientation_signs(("A", "B"), (("A", "B", 0),))
    assert not result["orientable"]
    assert "invalid parity" in result["failures"][0]


def test_unknown_vertex_rejected():
    result = m.solve_orientation_signs(("A",), (("A", "B", 1),))
    assert not result["orientable"]
    assert "unknown vertex" in result["failures"][0]


def test_transpose_choi_has_negative_antisymmetric_expectation():
    row = m.check_T_odd_fixed_sheet_map_not_CP()
    assert row["passed"]
    assert row["artifacts"]["negative_expectation"] == "-2"
    assert not row["artifacts"]["transpose_CP"]


def test_dependency_graph_is_acyclic_and_separated():
    assert m._cycle(m.DEPENDENCY_GRAPH) is None
    assert "T_POSITIVE_REAL_CSTAR" not in m._deps(m.DEPENDENCY_GRAPH, "T_LOCAL_J")
    assert "T_LOCAL_J" not in m._deps(m.DEPENDENCY_GRAPH, "T_POSITIVE_REAL_CSTAR")


def test_cycle_mutation_is_detected():
    graph = dict(m.DEPENDENCY_GRAPH)
    graph["T_LOCAL_J"] = (*graph["T_LOCAL_J"], "T_COMPLEX_QUANTUM_CORE")
    assert m._cycle(graph) is not None


def test_ungraded_and_retired_gate_names_are_forbidden():
    nodes = m._all_nodes(m.DEPENDENCY_GRAPH)
    assert "UNRESTRICTED_GENERATOR_COMPLETENESS" not in nodes
    # Pre-fortification renames are retired (cold audit 2026-07-21, MAJOR-3).
    assert "EVEN_GENERATOR_COMPLETENESS" not in nodes
    assert "GLOBAL_PARITY_COCYCLE_OR_DOUBLE_COVER" not in nodes
    assert set(m.DEPENDENCY_GRAPH["T_CENTRAL_J"]) == set(m.CENTRAL_J_REQUIRED_GATES)


def test_central_j_antecedent_matches_banked_inventory_when_available():
    gates, source = m._find_banked_central_j_gates()
    if gates is None:
        pytest.skip(source)
    assert tuple(sorted(gates)) == tuple(sorted(m.CENTRAL_J_REQUIRED_GATES)), (
        f"central-J antecedent drift vs banked inventory at {source}"
    )


def test_central_j_gate_deletion_drift_is_caught():
    for gate in m.CENTRAL_J_REQUIRED_GATES:
        mutated = dict(m.DEPENDENCY_GRAPH)
        mutated["T_CENTRAL_J"] = tuple(
            g for g in mutated["T_CENTRAL_J"] if g != gate
        )
        assert m._central_j_drift(mutated), f"deletion of {gate} not caught"


def test_pre_fortification_gate_rename_drift_is_caught():
    mutated = dict(m.DEPENDENCY_GRAPH)
    mutated["T_CENTRAL_J"] = (
        "T_LOCAL_J",
        "NATURALITY",
        "GLOBAL_PARITY_COCYCLE_OR_DOUBLE_COVER",
        "GENERATOR_COMPLETENESS",
    )
    assert m._central_j_drift(mutated)
    mutated["T_CENTRAL_J"] = (
        "T_LOCAL_J",
        "NATURALITY",
        "ORIENTATION_SYNCHRONIZATION",
        "EVEN_GENERATOR_COMPLETENESS",
    )
    assert m._central_j_drift(mutated)


def test_orientation_synchronization_carries_realization_typing():
    sync_deps = m._deps(m.DEPENDENCY_GRAPH, "ORIENTATION_SYNCHRONIZATION")
    assert "ORIENTATION_COVER_REALIZED" in sync_deps
    assert "ORIENTATION_SHEET_TYPING" in sync_deps


def _load_verifier():
    path = _PACKET_ROOT / "verify_orientation_network_certificate.py"
    vspec = importlib.util.spec_from_file_location("orientation_verifier", path)
    assert vspec and vspec.loader
    v = importlib.util.module_from_spec(vspec)
    sys.modules[vspec.name] = v
    vspec.loader.exec_module(v)
    return v


@requires_packet
def test_shipped_template_passes_shipped_verifier_uncertified():
    root = _PACKET_ROOT
    v = _load_verifier()
    payload = json.loads(
        (root / "DATA" / "orientation_network_certificate_template.json").read_text(encoding="utf-8")
    )
    report = v.verify(payload, root)
    assert report["failures"] == []
    # Intentionally uncertified physical verdicts, passing structural validation.
    assert report["orientation_cover_realized_certified"] is False
    assert report["physical_premises_certified"] is False
    assert report["single_sheet_central_J_certified"] is False


@requires_packet
def test_verifier_realization_leg_is_failable():
    root = _PACKET_ROOT
    v = _load_verifier()
    payload = json.loads(
        (root / "DATA" / "orientation_network_certificate_template.json").read_text(encoding="utf-8")
    )
    realized = dict(payload)
    realized["orientation_cover_realized"] = True
    report = v.verify(realized, root)
    assert any("ORIENTATION_COVER_REALIZED" in f for f in report["failures"])
    undeclared = dict(payload)
    undeclared.pop("orientation_cover_realized")
    report2 = v.verify(undeclared, root)
    assert any("orientation_cover_realized" in f for f in report2["failures"])


@requires_packet
def test_verifier_verdict_fields_never_true_on_failure():
    root = _PACKET_ROOT
    v = _load_verifier()
    payload = {
        "schema_version": "0.5",
        "claim_single_sheet_central_J": True,
        "claim_double_cover_central_J": True,
        "orientation_cover_realized": False,
        "physical_premises_certified": False,
        "vertices": ["A", "B", "C"],
        "edges": [
            {"source": "A", "target": "B", "parity": -1},
            {"source": "B", "target": "C", "parity": 1},
            {"source": "C", "target": "A", "parity": 1},
        ],
        "evidence": json.loads(
            (root / "DATA" / "orientation_network_certificate_template.json").read_text(encoding="utf-8")
        )["evidence"],
    }
    report = v.verify(payload, root)
    assert report["failures"]
    assert report["single_sheet_central_J_certified"] is False
    assert report["double_cover_central_J_conditional_certified"] is False


@requires_audit
def test_hostile_audit_script_runs_ship_relative_without_crash(tmp_path):
    if os.environ.get("GRADED_AUDIT_INNER"):
        pytest.skip("inside a hostile-audit run; recursion guard")
    root = _PACKET_ROOT
    script = root / "AUDIT" / "run_hostile_audit.py"
    shipped_json = root / "AUDIT" / "HOSTILE_AUDIT.json"
    shipped_md = root / "AUDIT" / "HOSTILE_AUDIT.md"
    before = (shipped_json.read_bytes(), shipped_md.read_bytes())
    env = dict(os.environ)
    env["HOSTILE_AUDIT_OUTDIR"] = str(tmp_path)
    env["GRADED_AUDIT_NO_PYTEST"] = "1"
    proc = subprocess.run(
        [sys.executable, str(script)], capture_output=True, text=True, env=env
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # The script writes fresh timestamped files and never overwrites the record.
    outputs = list(tmp_path.glob("HOSTILE_AUDIT_*.json"))
    assert outputs, "timestamped audit output missing"
    assert (shipped_json.read_bytes(), shipped_md.read_bytes()) == before


def test_certificate_never_self_certifies_physics():
    cert = m.build_certificate()
    assert cert.oriented_linking_algebra_is_M2C
    assert cert.physical_premises_certified is False
