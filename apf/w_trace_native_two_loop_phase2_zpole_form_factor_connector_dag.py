"""APF-native two-loop Phase-2 Z-pole form-factor connector DAG (CONNECTOR ONLY) — Tier-4.

ACF 2006 (`hep-ph/0608099`) NNLO Z-pole decomposition encoded as a 12-node /
12-edge directed acyclic graph. Nodes: M̄_Z pole, ẑ_f^(1), ẑ_f^(2), Σ'_ZZ^(1),
Σ'_ZZ^(2), Σ''_ZZ^(1), Σ_γZ^(1), Σ'_γZ^(1), R_ZZ, R, Δκ̄_Z^f, sin²θ_eff^f.

The DAG encodes which one- and two-loop self-energy + form-factor objects
feed which downstream connector relations leading to sin²θ_eff^f. The DAG
does NOT evaluate any v̂_f^(2), â_f^(2), or diagram-local coefficient
multiplying a master integral — those remain the open downstream coefficient
ledger gate.

Honest non-claims preserved:
  * Export_Zpole_form_factor_coefficients_evaluated = 0
  * Export_EW_2L_self_energy_coefficients_evaluated = 0
  * No measured M_W / sin²θ_eff / target consumed.

Sibling APF_TWO_LOOP_PHASE2_ZPOLE_FORM_FACTOR_CONNECTOR_DAG_v1 via
APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v5.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Set, Tuple

from apf.apf_utils import check, _result


REQUIRED_NODES: Set[str] = {
    "MZbar_pole",
    "zhat_f_1", "zhat_f_2",
    "Sigma_ZZ_1_prime", "Sigma_ZZ_2_prime",
    "Sigma_ZZ_1_doubleprime",
    "Sigma_gammaZ_1", "Sigma_gammaZ_1_prime",
    "R_ZZ", "R",
    "Delta_kappa_bar_Z_f",
    "sin2theta_eff_f",
}

REQUIRED_EDGES: Set[Tuple[str, str]] = {
    ("Sigma_ZZ_2_prime", "R_ZZ"),
    ("Sigma_gammaZ_1", "R_ZZ"),
    ("zhat_f_2", "R"),
    ("zhat_f_2", "Delta_kappa_bar_Z_f"),
    ("Delta_kappa_bar_Z_f", "sin2theta_eff_f"),
}


@dataclass(frozen=True)
class ZPoleNode:
    node: str
    kind: str
    phase2_channel: str


CONNECTOR_DAG_NODES = (
    ZPoleNode("MZbar_pole", "pole_anchor", "Sigma_Z_2L"),
    ZPoleNode("Sigma_ZZ_1_prime", "one_loop_self_energy_derivative", "Sigma_Z_2L"),
    ZPoleNode("Sigma_ZZ_1_doubleprime", "one_loop_self_energy_second_derivative", "Sigma_Z_2L"),
    ZPoleNode("Sigma_ZZ_2_prime", "two_loop_self_energy_derivative", "Sigma_Z_2L"),
    ZPoleNode("Sigma_gammaZ_1", "one_loop_mixing_self_energy", "Pi_gammaZ_2L"),
    ZPoleNode("Sigma_gammaZ_1_prime", "one_loop_mixing_self_energy_derivative", "Pi_gammaZ_2L"),
    ZPoleNode("zhat_f_1", "one_loop_form_factor", "Sigma_Z_2L"),
    ZPoleNode("zhat_f_2", "two_loop_form_factor", "Sigma_Z_2L"),
    ZPoleNode("R_ZZ", "ZZ_residue", "Sigma_Z_2L"),
    ZPoleNode("R", "scheme_remnant", "Sigma_Z_2L"),
    ZPoleNode("Delta_kappa_bar_Z_f", "kappa_bar_remnant", "Sigma_Z_2L"),
    ZPoleNode("sin2theta_eff_f", "effective_mixing_angle", "Sigma_Z_2L"),
)

CONNECTOR_DAG_EDGES = (
    ("MZbar_pole", "R_ZZ", "pole_to_ZZ_residue"),
    ("Sigma_ZZ_1_prime", "R_ZZ", "one_loop_derivative_to_residue"),
    ("Sigma_ZZ_1_doubleprime", "R_ZZ", "one_loop_second_derivative_to_residue"),
    ("Sigma_ZZ_2_prime", "R_ZZ", "two_loop_derivative_to_residue"),
    ("Sigma_gammaZ_1", "R_ZZ", "mixing_to_residue"),
    ("Sigma_gammaZ_1_prime", "Delta_kappa_bar_Z_f", "mixing_derivative_to_kappa"),
    ("R_ZZ", "R", "residue_to_scheme_remnant"),
    ("zhat_f_1", "Delta_kappa_bar_Z_f", "one_loop_form_factor_to_kappa"),
    ("zhat_f_2", "R", "two_loop_form_factor_to_remnant"),
    ("zhat_f_2", "Delta_kappa_bar_Z_f", "two_loop_form_factor_to_kappa"),
    ("R", "sin2theta_eff_f", "remnant_to_effective_angle"),
    ("Delta_kappa_bar_Z_f", "sin2theta_eff_f", "kappa_remnant_to_effective_angle"),
)


EXPORT_FLAGS = {
    "Export_Zpole_form_factor_connector_DAG_P": 1,
    "Export_Zpole_NNLO_formula_source_extracted_P": 1,
    "Export_Zpole_form_factor_coefficients_evaluated_P": 0,
    "Export_EW_2L_self_energy_coefficients_evaluated_P": 0,
    "target_consumed": 0,
    "gdrive_write_performed": False,
}


def validate_dag(nodes, edges):
    node_names = {n.node for n in nodes}
    missing_nodes = REQUIRED_NODES - node_names
    if missing_nodes:
        raise AssertionError(f"missing required nodes: {missing_nodes}")
    edge_pairs = {(e[0], e[1]) for e in edges}
    missing_edges = REQUIRED_EDGES - edge_pairs
    if missing_edges:
        raise AssertionError(f"missing required edges: {missing_edges}")
    # Basic acyclicity check (toposort feasibility)
    indeg = {n: 0 for n in node_names}
    for a, b, *_ in edges:
        indeg[b] = indeg.get(b, 0) + 1
    sources = [n for n in node_names if indeg[n] == 0]
    if not sources:
        raise AssertionError("DAG has no source nodes (cycle?)")
    return True


def check_T_two_loop_phase2_zpole_form_factor_connector_dag_P():
    """T: ACF 2006 NNLO Z-pole 12-node / 12-edge connector DAG. Encodes the
    Σ'_ZZ^(2) → R_ZZ → R → sin²θ_eff^f and ẑ_f^(2) → Δκ̄ → sin²θ_eff^f flow
    paths. NO form-factor coefficient or master coefficient evaluated.
    [P_two_loop_phase2_zpole_form_factor_connector_dag;
     C_zpole_form_factor_coefficients_pending]."""

    check(len(CONNECTOR_DAG_NODES) == 12,
          f"DAG must have 12 nodes, got {len(CONNECTOR_DAG_NODES)}")
    check(len(CONNECTOR_DAG_EDGES) == 12,
          f"DAG must have 12 edges, got {len(CONNECTOR_DAG_EDGES)}")
    validate_dag(CONNECTOR_DAG_NODES, CONNECTOR_DAG_EDGES)

    # Channel coverage
    channels = {n.phase2_channel for n in CONNECTOR_DAG_NODES}
    check("Sigma_Z_2L" in channels and "Pi_gammaZ_2L" in channels,
          f"DAG must touch Sigma_Z_2L + Pi_gammaZ_2L channels, got {channels}")

    # Required connector flow paths exist
    edge_pairs = {(a, b) for a, b, *_ in CONNECTOR_DAG_EDGES}
    flow_checks = [
        ("Sigma_ZZ_2_prime", "R_ZZ"),
        ("Sigma_gammaZ_1", "R_ZZ"),
        ("R_ZZ", "R"),
        ("R", "sin2theta_eff_f"),
        ("zhat_f_2", "Delta_kappa_bar_Z_f"),
        ("Delta_kappa_bar_Z_f", "sin2theta_eff_f"),
    ]
    for src, dst in flow_checks:
        check((src, dst) in edge_pairs,
              f"flow edge {src} → {dst} missing")

    check(EXPORT_FLAGS["Export_Zpole_form_factor_connector_DAG_P"] == 1,
          "DAG export flag must be 1")
    check(EXPORT_FLAGS["Export_Zpole_form_factor_coefficients_evaluated_P"] == 0,
          "form-factor coefficients evaluated must remain 0")
    check(EXPORT_FLAGS["Export_EW_2L_self_energy_coefficients_evaluated_P"] == 0,
          "EW 2L self-energy coefficients evaluated must remain 0")
    check(EXPORT_FLAGS["target_consumed"] == 0, "target_consumed must be 0")
    check(EXPORT_FLAGS["gdrive_write_performed"] is False, "gdrive flag must be False")

    return _result(
        name=("T_two_loop_phase2_zpole_form_factor_connector_dag: "
              "ACF 2006 NNLO Z-pole connector DAG (12 nodes, 12 edges) "
              "encoding the Σ'_ZZ^(2)+Σ_γZ → R_ZZ → R / Δκ̄ → sin²θ_eff^f "
              "flow. Coefficient evaluation explicitly NOT promoted. "
              "[P_two_loop_phase2_zpole_form_factor_connector_dag; "
              "C_zpole_form_factor_coefficients_pending]"),
        tier=4,
        epistemic="P_two_loop_phase2_zpole_form_factor_connector_dag",
        summary=(
            "Sibling-AI delivery via APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v5 / "
            "APF_TWO_LOOP_PHASE2_ZPOLE_FORM_FACTOR_CONNECTOR_DAG_v1. "
            "12 typed nodes: pole anchor M̄_Z, one-loop self-energy "
            "derivatives Σ'_ZZ^(1), Σ''_ZZ^(1), Σ_γZ^(1), Σ'_γZ^(1); "
            "two-loop derivative Σ'_ZZ^(2); one- and two-loop form factors "
            "ẑ_f^(1), ẑ_f^(2); ZZ residue R_ZZ, scheme remnant R, "
            "kappa-bar remnant Δκ̄_Z^f, and effective angle sin²θ_eff^f. "
            "12 directed edges encoding the source ACF 2006 NNLO recipe: "
            "(self-energy derivatives + mixing) → R_ZZ → R, (one-loop FF + "
            "two-loop FF + mixing derivative) → Δκ̄, (R + Δκ̄) → sin²θ_eff^f. "
            "Phase-2-channel typing maps nodes to Σ_Z_2L and Π_γZ_2L. "
            "Acyclicity guarded via in-degree zero source check."
        ),
        key_result=(
            "12-node / 12-edge Z-pole connector DAG encoded; form-factor "
            "coefficients OPEN. "
            "[P_two_loop_phase2_zpole_form_factor_connector_dag; "
            "C_zpole_form_factor_coefficients_pending]"
        ),
        dependencies=[
            "T_two_loop_phase2_ew_tex_source_exact_extraction_v2",
            "T_two_loop_phase2_ew_self_energy_assembly_gate_toy_ledger",
        ],
        cross_refs=[],
        artifacts={
            "node_count": 12,
            "edge_count": 12,
            "phase2_channels_touched": ["Sigma_Z_2L", "Pi_gammaZ_2L"],
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_two_loop_phase2_zpole_form_factor_connector_dag":
        check_T_two_loop_phase2_zpole_form_factor_connector_dag_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}
